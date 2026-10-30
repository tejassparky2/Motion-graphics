"""Episode 1 v2 picture assembler: shot mp4s in, the silent 720x1280 picture out.

    FPS=24 python channels/monsters/assemble_ep01v2.py [--animatic] [--check] [--out PATH]

- Every shot in channels/monsters/ep01v2/timing.json comes from out/monsters/ep01v2/shots/<SHOT>.mp4, conformed
  to its exact frame count: the tail handle is trimmed, and a short shot holds its last frame (with a warning).
- S02 is built here: S01 played backwards under comp.glitch, landing on two frames of static and two of white
  into S03a.
- S24 is the A/B split (AB13): S24top.mp4 (SAVE) above, S24bot.mp4 (RUN) below, cut by fx2d_anime.split's jagged
  divider; the panels slide in at the shot's start.
- Captions are word-timed from timing.json in the 71% band (2-4 words, the spoken word highlighted); none in
  S15. The frame-0 hook text THIS SHRIMP ERASED A FOREST sits high in the frame until line 1 ends (TP16).
- Nothing else goes in the picture: no HUD, no logos, no series chip.

--animatic: a missing shot becomes a dark slate with its name in small grey type. Without it, a missing shot is an
error. --check: also writes a contact sheet of every 12th frame (out/monsters/ep01v2/picture_sheet.jpg) and prints
every shot boundary.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

import numpy as np  # noqa: E402

from channels.monsters import comp, fx2d, fx2d_anime  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402
from motion.polish import text_width  # noqa: E402

TIMING = os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")
SHOTS = os.path.join(ROOT, "out", "monsters", "ep01v2", "shots")
OUT = os.path.join(ROOT, "out", "monsters", "ep01v2", "picture.mp4")
SHEET = os.path.join(ROOT, "out", "monsters", "ep01v2", "picture_sheet.jpg")

# The repo's output hygiene (render.py CLEAN), video only: no container metadata, no encoder tags, no x264 SEI.
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]

HOOK = [("THIS SHRIMP", ()), ("ERASED", ("ERASED",)), ("A FOREST", ())]
HOOK_Y = 170                 # top baseline: high in the frame, over the sliced trees, above Kai's face
HOOK_SIZE = 108
NO_CAPTIONS = {"S15"}
CAP_Y = 905                  # baseline in the 71% band (caption band 845-930)
CAP_SIZE = 60
CAP_MAX_W = 560              # clear of the right rail
CAP_Y_SHOT = {}              # per-shot baseline where the 71% band would cover a face, e.g. {"S14": 1010}
HOOK_SHIFT = 0               # move the hook up (negative) if it touches Kai's eyes or the claw tip in S01
SLATE = (0.08, 0.085, 0.11)


# ---------------------------------------------------------------- decoding shots
def decode(path):
    """All frames of an mp4 as BGRA arrays (cairo's ARGB32 layout), scaled to the canvas."""
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo",
           "-pix_fmt", "bgra", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    n = len(raw) // (W * H * 4)
    return [np.frombuffer(raw, np.uint8, W * H * 4, i * W * H * 4).reshape(H, W, 4).copy() for i in range(n)]


def surface(arr):
    """A cairo view of a contiguous BGRA array (the caller keeps the array alive while the surface is used)."""
    return cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, W, H, W * 4)


def conform(frames, need, name, warn):
    """Exactly `need` frames: trim the handle, or hold the last frame of a short shot."""
    if len(frames) < need:
        warn.append(f"{name}: {len(frames)} frames, needs {need}; holding the last frame for {need - len(frames)}")
        frames = frames + [frames[-1]] * (need - len(frames))
    return frames[:need]


def slate(name):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(s)
    cr.set_source_rgb(*SLATE)
    cr.paint()
    fx2d._text(cr, name, W / 2, H * 0.42, 26, (0.55, 0.56, 0.6, 1), fx2d.ROUND, "center")
    return s


# ---------------------------------------------------------------- shots
class Shot:
    def __init__(self, info):
        self.name = info["shot"]
        self.first = info["first_frame"]
        self.frames = info["frames"]

    def path(self, suffix=""):
        return os.path.join(SHOTS, f"{self.name}{suffix}.mp4")


def build_plain(shot, animatic, warn, missing):
    if not os.path.exists(shot.path()):
        missing.append(shot.name)
        return None
    return conform(decode(shot.path()), shot.frames, shot.name, warn)


def build_s02(shot, s01, warn):
    """S01 backwards under the rewind glitch, squeezed into the shot, landing on static then white."""
    tail = 4
    run = shot.frames - tail
    rev = s01[::-1]
    out = []
    for i in range(shot.frames):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        cr = cairo.Context(s)
        if i < run:
            cr.set_source_surface(surface(rev[min(len(rev) - 1, int(i * len(rev) / run))]), 0, 0)
            cr.paint()
            comp.glitch(cr, i / FPS, 0.0, run / FPS, strength=1.0, seed=2, sound=False)
        elif i < run + 2:                                      # static
            noise = np.random.default_rng(i).integers(0, 256, (H // 4, W // 4), np.uint8)
            n = np.repeat(np.repeat(noise, 4, 0), 4, 1)
            a = np.dstack([n, n, n, np.full_like(n, 255)])
            cr.set_source_surface(surface(a), 0, 0)
            cr.paint()
        else:                                                  # white flash into S03a
            cr.set_source_rgb(1, 1, 1)
            cr.paint()
        out.append(s)
    return out


def build_s24(shot, animatic, warn, missing):
    plates = []
    for suffix in ("top", "bot"):
        p = shot.path(suffix)
        if os.path.exists(p):
            plates.append(conform(decode(p), shot.frames, shot.name + suffix, warn))
        else:
            missing.append(shot.name + suffix)
            plates.append(None)
    if plates == [None, None]:
        return None
    if not animatic and None in plates:
        return None
    out = []
    for i in range(shot.frames):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        cr = cairo.Context(s)
        panels = [surface(p[i]) if p is not None else slate(shot.name + sfx)
                  for p, sfx in zip(plates, ("top · SAVE", "bot · RUN"))]
        fx2d_anime.split(cr, i / FPS, 0.0, shot.frames / FPS, panels, sound=False)
        out.append(s)
    return out


# ---------------------------------------------------------------- captions and the hook
def caption_chunks(lines):
    """2-4 words per chunk (a lone word only when a sentence is one word), breaking at sentence ends, at a comma
    after 2+ words, and before 18 characters."""
    out = []
    for ln in lines:
        if ln["scene"] in NO_CAPTIONS:
            continue
        cur = []
        for w in ln["words"]:
            if len(cur) >= 2 and len(" ".join(x["w"] for x in cur + [w])) > 18:
                out.append(cur)                              # the next word would make the chunk too wide
                cur = []
            cur.append(w)
            if w["w"][-1] in ".!?" or (w["w"][-1] in ",;:" and len(cur) >= 2) or len(cur) == 4:
                out.append(cur)
                cur = []
        if cur:
            if len(cur) == 1 and out and out[-1][-1]["w"][-1] not in ".!?" and len(out[-1]) < 4:
                out[-1] = out[-1] + cur                     # don't leave a word alone
            else:
                out.append(cur)
    return out


def draw_caption(cr, t, chunks, total, y=CAP_Y):
    for i, ch in enumerate(chunks):
        start = ch[0]["start"]
        nxt = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else total
        stop = nxt if nxt - ch[-1]["end"] < 0.5 else ch[-1]["end"] + 0.25
        if not (start - 0.02 <= t < stop):
            continue
        words = [w["w"] for w in ch]
        space = text_width(cr, " ", CAP_SIZE, fx2d.ROUND) * 1.15
        widths = [text_width(cr, w, CAP_SIZE, fx2d.ROUND) for w in words]
        total_w = sum(widths) + space * (len(words) - 1)
        k = min(1.0, CAP_MAX_W / total_w)
        size = CAP_SIZE * k
        pop = 0.9 + 0.1 * min(1.0, (t - start) / 0.08)
        cr.save()
        cr.translate(W / 2, y - size * 0.35)
        cr.scale(pop, pop)
        x = -total_w * k / 2
        for w, wd, word in zip(words, widths, ch):
            active = word["start"] - 0.03 <= t < word["end"] + 0.05 or (t >= word["end"] and word is ch[-1])
            col = fx2d.YELLOW if active else fx2d.WHITE
            fx2d._text(cr, w, x, size * 0.35, size, col, fx2d.ROUND, outline=(0.05, 0.03, 0.06, 1), ow=size * 0.2,
                       shadow=0.45)
            x += (wd + space) * k
        cr.restore()
        return


def draw_hook(cr):
    """THIS SHRIMP / ERASED / A FOREST: white, the key word red, thick dark outline. Static from frame 0."""
    for j, (line, red) in enumerate(HOOK):
        size = min(HOOK_SIZE, HOOK_SIZE * (W - 70) / text_width(cr, line, HOOK_SIZE, fx2d.ROUND))
        col = fx2d.RED if line in red else fx2d.WHITE
        fx2d._text(cr, line, W / 2, HOOK_Y + HOOK_SHIFT + j * HOOK_SIZE * 1.02, size, col, fx2d.ROUND, "center",
                   outline=(0.05, 0.03, 0.06, 1), ow=size * 0.2, shadow=0.55)


# ---------------------------------------------------------------- main
def main():
    global SHOTS
    ap = argparse.ArgumentParser()
    ap.add_argument("--animatic", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--shots", default=None, help="folder of shot mp4s (default out/monsters/ep01v2/shots)")
    a = ap.parse_args()
    SHOTS = a.shots or SHOTS

    tj = json.load(open(TIMING))
    assert tj["fps"] == FPS, f"timing.json is {tj['fps']} fps, the canvas is {FPS}"
    shots = [Shot(s) for s in tj["shots"]]
    total = tj["total_frames"]
    assert shots[-1].first + shots[-1].frames == total, "shot frames don't add up to the total"
    hook_end = int(round(tj["lines"][0]["end"] * FPS))
    chunks = caption_chunks(tj["lines"])

    warn, missing = [], []
    if not a.animatic:                                         # delivery: refuse before doing any work
        need = [s.path("top") if s.name == "S24" else s.path() for s in shots if s.name != "S02"]
        if any(s.name == "S24" for s in shots):
            need.append(os.path.join(SHOTS, "S24bot.mp4"))
        gone = [os.path.basename(p) for p in need if not os.path.exists(p)]
        if gone:
            sys.exit(f"missing shots (use --animatic to slate them): {', '.join(gone)}")

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                            "-pix_fmt", "yuv420p", *CLEAN, a.out], stdin=subprocess.PIPE)
    sheet = []
    s01 = None
    frame_no = 0
    for shot in shots:
        if shot.name == "S02":
            frames = build_s02(shot, s01, warn) if s01 is not None else None
            if frames is None:
                missing.append("S02 (needs S01)")
        elif shot.name == "S24":
            frames = build_s24(shot, a.animatic, warn, missing)
        else:
            frames = build_plain(shot, a.animatic, warn, missing)
            if shot.name == "S01" and frames is not None:
                s01 = frames
        if a.check:
            print(f"{shot.name:5s} frames {shot.first:4d}-{shot.first + shot.frames - 1:4d} "
                  f"({shot.frames:3d}, {shot.frames / FPS:5.2f} s){'' if frames is not None else '  SLATE'}"
                  f"{f'  captions at y={CAP_Y_SHOT[shot.name]}' if shot.name in CAP_Y_SHOT else ''}")
        sl = slate(shot.name) if frames is None else None
        for i in range(shot.frames):
            src = sl if frames is None else frames[i]
            s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            cr = cairo.Context(s)
            cr.set_source_surface(src if isinstance(src, cairo.ImageSurface) else surface(src), 0, 0)
            cr.paint()
            t = frame_no / FPS
            if frame_no <= hook_end:
                draw_hook(cr)
            if shot.name not in NO_CAPTIONS:
                draw_caption(cr, t, chunks, tj["total"], CAP_Y_SHOT.get(shot.name, CAP_Y))
            s.flush()
            enc.stdin.write(bytes(s.get_data()))
            if a.check and frame_no % 12 == 0:
                sheet.append((frame_no, shot.name, s))
            frame_no += 1
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit("ffmpeg failed")
    for w in warn:
        print("WARNING:", w)
    if missing:
        print(f"missing ({len(missing)}): {', '.join(missing)}")
    print(f"{a.out}: {frame_no} frames, {frame_no / FPS:.2f} s")
    if a.check:
        write_sheet(sheet, os.path.join(os.path.dirname(a.out), os.path.basename(SHEET)))


def write_sheet(sheet, path, cols=10, tw=144, th=256):
    from PIL import Image
    rows = (len(sheet) + cols - 1) // cols
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * tw, rows * th)
    cr = cairo.Context(out)
    cr.set_source_rgb(0, 0, 0)
    cr.paint()
    for k, (n, name, s) in enumerate(sheet):
        cr.save()
        cr.translate((k % cols) * tw, (k // cols) * th)
        cr.scale(tw / W, th / H)
        cr.set_source_surface(s, 0, 0)
        cr.paint()
        cr.restore()
        fx2d._text(cr, f"{n} {name}", (k % cols) * tw + 5, (k // cols) * th + 18, 15, fx2d.YELLOW, fx2d.ROUND,
                   outline=fx2d.INK, ow=4)
    out.flush()
    a = np.ndarray((out.get_height(), out.get_width(), 4), np.uint8, out.get_data())
    Image.fromarray(a[..., [2, 1, 0]]).save(path, quality=88)
    print(f"{path}: {len(sheet)} frames (every 12th)")


if __name__ == "__main__":
    main()
