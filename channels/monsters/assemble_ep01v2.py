"""Episode 1 v2 picture assembler: shot mp4s in, the silent 720x1280 picture out.

    FPS=24 python channels/monsters/assemble_ep01v2.py [--version ep01v2|diorama|diorama_v3|diorama_ep02|diorama_ep03]
                                                       [--animatic]
                                                       [--check]
                                                       [--shots DIR] [--out PATH]

- Every shot in channels/monsters/ep01v2/timing.json comes from out/monsters/ep01v2/shots/<SHOT>.mp4, conformed
  to its exact frame count: the tail handle is trimmed, and a short shot holds its last frame (with a warning).
- S02 is built here: S01 played backwards under comp.glitch, landing on two frames of static and two of white
  (85% then 60%, so the S15 snap stays the brightest moment) into S03a.
- S24 is the A/B split (AB13): S24top.mp4 (SAVE) above, S24bot.mp4 (RUN) below, cut by fx2d_anime.split's jagged
  divider; the panels slide in at the shot's start.
- Captions are word-timed from timing.json in the 71% band (2-4 words, the spoken word highlighted); none in
  S15. The frame-0 hook text THIS SHRIMP ERASED A FOREST sits high in the frame until line 1 ends (TP16).
- Nothing else goes in the picture: no HUD, no logos, no series chip.
- Episode 2 (--version diorama_ep02, channels/monsters/DIORAMA_EP02.md): its own timing (ep02/timing.json), no rewind
  (its S02 is a plain shot), captions on every spoken shot, the hook I SAVED THE SHRIMP THAT TRIED TO KILL ME, and the
  A/B split on S20 (S20top.mp4 = A · HAND OVER, S20bot.mp4 = B · SHOW MARK). Per-version settings: the *_VERSION tables.
- Episode 3 (--version diorama_ep03, channels/monsters/DIORAMA_EP03.md): the same way, with ep03/timing.json, the hook
  THE VILLAGE RAN FROM MY WRIST and the A/B split on S19 (S19top.mp4 = A · GO TONIGHT, S19bot.mp4 = B · LEAVE AT DAWN).
- Every frame's outer 3 px are scanned for unpainted black: a run of 24+ px along an edge (a render that shows past
  the world's edge, or a gap in the composite). Deliberate black frames are skipped. The frames and edges are printed.

--animatic: a missing shot becomes a dark slate with its name in small grey type. Without it, a missing shot is an
error. --check: also writes a contact sheet of every 12th frame (out/monsters/ep01v2/picture_sheet.jpg) and prints
every shot boundary.
"""
import argparse
import json
import math
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

import numpy as np  # noqa: E402

from channels.monsters import comp, fx2d, fx2d_ab, fx2d_anime  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402
from motion.polish import text_width  # noqa: E402

TIMING = os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")
# Two cuts of the same episode (same timing, voice, captions and hook): the 3D one and the diorama 2.5D one
# (channels/monsters/DIORAMA_EP01.md). Each has its own shots folder, output and caption placements.
VERSIONS = {"ep01v2": os.path.join(ROOT, "out", "monsters", "ep01v2"),
            "diorama": os.path.join(ROOT, "out", "monsters", "diorama"),
            "diorama_v3": os.path.join(ROOT, "out", "monsters", "diorama_v3"),
            "diorama_ep02": os.path.join(ROOT, "out", "monsters", "diorama_ep02"),
            "diorama_ep03": os.path.join(ROOT, "out", "monsters", "diorama_ep03")}
# v3 (channels/monsters/DIORAMA_EP01_V3.md) has its own script and timing; the first two share ep01v2's.
TIMINGS = {"ep01v2": TIMING, "diorama": TIMING,
           "diorama_v3": os.path.join(ROOT, "channels", "monsters", "ep01v3", "timing.json"),
           "diorama_ep02": os.path.join(ROOT, "channels", "monsters", "ep02", "timing.json"),
           "diorama_ep03": os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")}
AB_VERSIONS = {"diorama_v3", "diorama_ep02", "diorama_ep03"}   # the split carries big A / B letters on "Option A", "Option B", "Comment"
SPLIT_SHOT_VERSION = {"diorama_ep02": "S20", "diorama_ep03": "S19"}   # the A/B split shot (<SHOT>top.mp4 above, <SHOT>bot.mp4 below); else S24
REWIND_VERSIONS = {"ep01v2", "diorama", "diorama_v3"}   # S02 is S01's glitch rewind (Episode 1 only)
AB_LABELS_VERSION = {"diorama_v3": ("SAVE", "RUN"), "diorama_ep02": ("HAND OVER", "SHOW MARK"),
                     "diorama_ep03": ("GO TONIGHT", "LEAVE AT DAWN")}
AB_LABELS = ("SAVE", "RUN")
SHOTS = os.path.join(VERSIONS["ep01v2"], "shots")
OUT = os.path.join(VERSIONS["ep01v2"], "picture.mp4")
SHEET = os.path.join(VERSIONS["ep01v2"], "picture_sheet.jpg")

# The repo's output hygiene (render.py CLEAN), video only: no container metadata, no encoder tags, no x264 SEI.
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:v", "encoder="]

HOOK = [("THIS SHRIMP", ()), ("ERASED", ("ERASED",)), ("A FOREST", ())]
HOOK_Y = 170                 # top baseline: high in the frame, over the sliced trees, above Kai's face
HOOK_SIZE = 108
HOOK_X = None                # centre x of the hook lines (default: the frame centre)
# Episode 2's frame-0 hook: four short lines, the threat in red. S01 keeps Kai's face and the diving bird in the top
# third and the shrimp at y 745+, so the hook sits in the middle band (over his legs and the tree trunk).
HOOK_VERSION = {"diorama_ep02": dict(lines=[("I SAVED", ()), ("THE SHRIMP", ()), ("THAT TRIED", ()),
                                            ("TO KILL ME", ("TO KILL ME",))], y=480, size=80),
                # Episode 3: three lines, the wrist in red. The re-staged S01 (helper 4's OK stills f1/f30: low over
                # Wren's shoulder, looking up at Kai) leaves open sky above his raised hand (top ~350) and Wren's braid
                # at the right edge, so the hook sits at the top, a little left of centre
                "diorama_ep03": dict(lines=[("THE VILLAGE", ()), ("RAN FROM", ()), ("MY WRIST", ("MY WRIST",))],
                                     y=120, size=84, x=345)}
NO_CAPTIONS = {"S15"}        # Episode 1's snap; Episode 2's wordless S09 has no words to caption anyway
NO_CAPTIONS_VERSION = {"diorama_ep02": set(), "diorama_ep03": set()}   # ep03's S14 (the flip) has no words
CAP_Y = 905                  # baseline in the 71% band (caption band 845-930)
CAP_SIZE = 60
CAP_MAX_W = 560              # clear of the right rail
# Per-version, per-shot caption baselines where the 71% band would cover a face or the subject.
CAP_Y_VERSION = {
    "ep01v2": {"S01": 940, "S02": 940, "S14": 150, "S16": 210, "S18": 145, "S19": 640, "S24": 748},
    "diorama": {"S05a": 180, "S06": 200, "S07": 560, "S13": 250, "S16": 200, "S17": 250, "S18": 380, "S24": 775},   # S05a: over the pebbles at the top, off the glowing bubble;
                                            # S06: in the dark above the room, off Kai at the desk;
                                            # S07: above the shrimp (tank and impact frame); S13: above Kai's cap, off the
                                            # shrimp at the pond; S16: above the pond, off the shrimp on his chest
                                            # through the push-in; S17: in the sky above his cap, off
                                            # the shrimp's eyes, the drop and the wet patch; S18: above Kai's cap, off the shrimp on his chest;
                                            # S24: RUN panel, between the
                                            # divider and Kai's cap. Shots still changing are checked when they land.
}
# v3 starts from the diorama placements for the shots it keeps; new and re-staged shots are checked as they land.
CAP_Y_VERSION["diorama_v3"] = {k: v for k, v in CAP_Y_VERSION["diorama"].items()
                               if k in ("S05a", "S06", "S13", "S16", "S17", "S18")}
CAP_Y_VERSION["diorama_v3"].update({
    "S07": 200,              # v3: over the pebbles above the shrimp, off the claw, the snap and the crack
    "S08": 945,              # under the power strip as it slides through the default band ("straight into the")
    "S08a": 620,             # over his shorts: the face, the sneakers in the spill and the sparking strip stay clear
    "S01": 945,              # the lowest legal line: off the shrimp's eyes, on its fluff (Kai and it fill the middle)
    "S02": 945,              # the rewind of S01, same layout
    "S08b": 945,             # below his feet and the skeleton's (text ends ~955, above the Shorts UI line at 960)
    "S15a": 250,             # above the shrimp's eyes, then the blurred trees above Kai's cap; off the raised claw
    "S22": [(0.0, CAP_Y), (0.9, 500)],
    "S23c": 860,
    "S24": [(0.0, CAP_Y), (3.3, 945)],   # from "Option B" Kai walks down the B panel: under his head
})
# S22: the tree close-up keeps the band; after the pull-back, the grass between the tree and Kai at the puddle.
# S23c: between the shrimp's antenna tips and its head fluff, which rises into 905 on the push-in.
# Episode 2: every shot starts on the 71% band; placements are checked on the real frames as the shots land.
CAP_Y_VERSION["diorama_ep02"] = {
    "S07": 150,              # in the sky above his cap: the turning claw fills the 71% band
    "S10": 600,              # above the upside-down bird in the thorn bush (its masked face is in the 71% band)
    "S20": 520,              # the B half puts Kai's face in the 71% band and the hide at chest height: the captions go
                             # in the A half, under the net (the shrimp is high, then inside it) and above the A card
}
# Episode 3: every shot starts on the 71% band; placements are checked on the real frames as the shots land.
CAP_Y_VERSION["diorama_ep03"] = {
    "S01": 760,              # over Kai's chest: at the band the line crosses the shrimp's face in his lower hand
    "S15": 300,              # in the dark sky over the trees: the band crosses the upside-down moths' faces (the laugh)
    "S19": 430,              # the split: the captions sit in the A half above the stacked A/B cards
}
CAP_Y_SHOT = CAP_Y_VERSION["ep01v2"]
HOOK_SHIFT = 0               # move the hook up (negative) if it touches Kai's eyes or the claw tip in S01
SLATE = (0.08, 0.085, 0.11)
# Output resolution: the overlays are designed on the 720x1280 canvas (W, H) and drawn under cr.scale(SCALE), so the
# text stays sharp at 1080x1920. v3 is delivered at 1080 (Q4: shots_1080/ from esrgan_shot.py, else lanczos).
RES = {"diorama_v3": 1.5, "diorama_ep02": 1.5, "diorama_ep03": 1.5}
SCALE = 1.0
OW, OH = W, H
SHOTS_HI = None              # the 1080 shots folder, preferred over SHOTS when SCALE > 1
S02_WHITE = (0.85, 0.60)     # the rewind's closing flash stays dimmer than the snap (the episode's brightest moment)
S24_FOCUS = [(W / 2, H / 4), (W / 2, H * 3 / 4)]   # the plates are framed as halves: each shows in place
# v3's B plate: Kai's cap and raised hand start ~20 px under the divider, so the plate drops 100 px instead of 60
S24_FOCUS_VERSION = {"diorama_v3": [(W / 2, H / 4), (W / 2, 860)],
                     # ep02's S20bot renders only the bottom 58% (rows 538+): the plate drops 80 px, not 60, so the
                     # divider's lowest jag (screen ~598) shows plate rows from 518 - a 20 px margin
                     "diorama_ep02": [(W / 2, H / 4), (W / 2, 880)]}
# card centres per version (default fx2d_ab.A_POS / B_POS); v3's B moves right of the bird at the pond's top-left
AB_POS_VERSION = {"diorama_v3": {"B": (200, 700)},
                  # ep02's S20 halves are full of Kai, Wren, the net and the shrimp: both cards straddle the divider,
                  # A over Kai's shins and the stump, B (SHOW MARK, 422 px wide at 85%) at x 286 so it stays in frame: in the sky
                  # right of Kai's cap, above his raised glowing arm and Wren's face (S20bot v2 stills, 2 Nov)
                  "diorama_ep02": {"A": (124, 585), "B": (286, 715)},
                  # ep03: LEAVE AT DAWN is 513 px right of its centre at 85%, so B's centre stays at x <= 197. The
                  # cards stack on the divider (A just above it, B in the dawn sky just under it): helper 5's S19bot v2
                  # (beach road into the sunrise) has Kai's whole body at screen y ~716-1040, so B clears his head, the
                  # shrimp and the look back; only the pill's end crosses the sun's edge
                  "diorama_ep03": {"A": (124, 515), "B": (124, 655)}}
AB_SCALE_VERSION = {"diorama_ep02": 0.85, "diorama_ep03": 0.85}
# Frames whose black edges are drawn on purpose, per version: {shot: (first, last) frame in the shot, why}. The scan
# reports them as intended instead of as a problem; re-check the range if the shot is re-rendered.
EDGE_OK_VERSION = {"diorama_ep02": {"S09": (28, 40, "the snap's ink impact frames (black ground, white speed lines)")}}   # the cards' size per version (1 = fx2d_ab's 168 px badge)


# ---------------------------------------------------------------- decoding shots
def decode(path, w=None, h=None):
    """All frames of an mp4 as BGRA arrays (cairo's ARGB32 layout), scaled (lanczos) to the output size."""
    w, h = w or OW, h or OH
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h}:flags=lanczos", "-f", "rawvideo",
           "-pix_fmt", "bgra", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    n = len(raw) // (w * h * 4)
    return [np.frombuffer(raw, np.uint8, w * h * 4, i * w * h * 4).reshape(h, w, 4).copy() for i in range(n)]


def surface(arr):
    """A cairo view of a contiguous BGRA array (the caller keeps the array alive while the surface is used)."""
    h, w = arr.shape[:2]
    return cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, w, h, w * 4)


def blank():
    """An output-size surface and a context drawing in canvas units."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, OW, OH)
    cr = cairo.Context(s)
    cr.scale(SCALE, SCALE)
    return s, cr


def paint_full(cr, src):
    """Paint an output-size surface over the whole frame from a canvas-unit context."""
    cr.save()
    cr.scale(1 / SCALE, 1 / SCALE)
    cr.set_source_surface(src, 0, 0)
    cr.paint()
    cr.restore()


def conform(frames, need, name, warn):
    """Exactly `need` frames: trim the handle, or hold the last frame of a short shot."""
    if len(frames) < need:
        warn.append(f"{name}: {len(frames)} frames, needs {need}; holding the last frame for {need - len(frames)}")
        frames = frames + [frames[-1]] * (need - len(frames))
    return frames[:need]


def slate(name, i=None, n=None, line="", y=None):
    """A placeholder for a shot that hasn't landed: its name, and with i/n its frame counter and its line, so the
    animatic reads as a timed storyboard. Dark grey, never black (the edge-band scan ignores it)."""
    s, cr = blank()
    cr.set_source_rgb(*SLATE)
    cr.paint()
    if i is None:
        fx2d._text(cr, name, W / 2, y or H * 0.42, 26, (0.55, 0.56, 0.6, 1), fx2d.ROUND, "center")
        return s
    grey = (0.55, 0.56, 0.6, 1)
    fx2d._text(cr, name, W / 2, H * 0.36, 120, (0.75, 0.76, 0.8, 1), fx2d.ROUND, "center")
    fx2d._text(cr, f"f {i + 1:3d} / {n}", W / 2, H * 0.36 + 70, 34, grey, fx2d.ROUND, "center")
    cr.set_source_rgba(*grey[:3], 0.8)                          # the shot's progress bar
    cr.rectangle(W * 0.2, H * 0.36 + 100, W * 0.6 * (i + 1) / n, 8)
    cr.fill()
    words, row, y = line.split(), "", H * 0.36 + 170
    for w in words + [None]:                                    # the line, wrapped, small
        if w is None or (row and text_width(cr, row + " " + w, 30, fx2d.ROUND) > W * 0.8):
            fx2d._text(cr, row, W / 2, y, 30, grey, fx2d.ROUND, "center")
            row, y = w or "", y + 40
        else:
            row = (row + " " + w).strip()
    return s


def _sha(path):
    """The first 8 hex digits of a shot file's SHA-1, printed by --check so every run shows exactly which version
    of each shot went into the cut (shots are decoded fresh on every run; nothing is cached)."""
    import hashlib
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


# ---------------------------------------------------------------- shots
class Shot:
    def __init__(self, info):
        self.name = info["shot"]
        self.first = info["first_frame"]
        self.frames = info["frames"]

    def path(self, suffix=""):
        """The shot file: the 1080 upscale when the cut is at 1080 and it exists, else the 720 render."""
        name = f"{self.name}{suffix}.mp4"
        if SHOTS_HI and os.path.exists(os.path.join(SHOTS_HI, name)):
            return os.path.join(SHOTS_HI, name)
        return os.path.join(SHOTS, name)


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
        s, cr = blank()
        if i < run:
            paint_full(cr, surface(rev[min(len(rev) - 1, int(i * len(rev) / run))]))
            comp.glitch(cr, i / FPS, 0.0, run / FPS, strength=1.0, seed=2, sound=False)
        elif i < run + 2:                                      # static
            noise = np.random.default_rng(i).integers(0, 256, (H // 4, W // 4), np.uint8)
            n = np.repeat(np.repeat(noise, 4, 0), 4, 1)
            a = np.ascontiguousarray(np.dstack([n, n, n, np.full_like(n, 255)]))
            cr.set_source_surface(surface(a), 0, 0)
            cr.paint()
        else:                                                  # white flash into S03a, below the S15 snap's
            paint_full(cr, surface(rev[-1]))                   # peak: 85% then 60% white over S01's first frame
            cr.set_source_rgba(1, 1, 1, S02_WHITE[i - run - 2])
            cr.paint()
        out.append(s)
    return out


def build_split(shot, animatic, warn, missing):
    plates = []
    for suffix in ("top", "bot"):
        p = shot.path(suffix)
        if os.path.exists(p):
            plates.append(conform(decode(p), shot.frames, shot.name + suffix, warn))
        else:
            missing.append(shot.name + suffix)
            plates.append(None)
    if not animatic and None in plates:                     # (the animatic splits two slates: the layout reads)
        return None
    return _Split(shot, plates)


class _Split:
    """The split shot's frames, composed one at a time as they are written (holding them all at 1080 would cost ~1.4 GB)."""

    def __init__(self, shot, plates):
        self.shot, self.plates = shot, plates
        self.slates = [slate(shot.name + sfx, y=y) if p is None else None      # each label in its own half
                       for p, sfx, y in zip(plates, (f"top · {AB_LABELS[0]}", f"bot · {AB_LABELS[1]}"),
                                            (H * 0.30, H * 0.80))]

    def __getitem__(self, i):
        s, cr = blank()
        panels = [surface(p[i]) if p is not None else sl for p, sl in zip(self.plates, self.slates)]
        fx2d_anime.split(cr, i / FPS, 0.0, self.shot.frames / FPS, panels, focus=S24_FOCUS_SHOT, sound=False)
        return s


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


def cap_y(place, chunk_start, shot_start):
    """A shot's caption baseline: a number, or [(seconds into the shot, y), ...] when the framing changes inside the
    shot (each chunk takes the last entry at or before its own start)."""
    if not isinstance(place, (list, tuple)):
        return place
    y = place[0][1]
    for at, yy in place:
        if chunk_start - shot_start >= at - 1e-6:
            y = yy
    return y


def draw_caption(cr, t, chunks, total, y=CAP_Y, shot_start=0.0):
    for i, ch in enumerate(chunks):
        start = ch[0]["start"]
        nxt = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else total
        stop = nxt if nxt - ch[-1]["end"] < 0.5 else ch[-1]["end"] + 0.25
        if not (start - 0.02 <= t < stop):
            continue
        y = cap_y(y, start, shot_start)
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
    """The frame-0 hook (Episode 1: THIS SHRIMP / ERASED / A FOREST): white, the key words red, thick dark outline.
    Static from frame 0 until line 1 ends."""
    for j, (line, red) in enumerate(HOOK):
        size = min(HOOK_SIZE, HOOK_SIZE * (W - 70) / text_width(cr, line, HOOK_SIZE, fx2d.ROUND))
        col = fx2d.RED if line in red else fx2d.WHITE
        fx2d._text(cr, line, HOOK_X if HOOK_X is not None else W / 2, HOOK_Y + HOOK_SHIFT + j * HOOK_SIZE * 1.02, size, col, fx2d.ROUND, "center",
                   outline=(0.05, 0.03, 0.06, 1), ow=size * 0.2, shadow=0.55)


def edge_black(s, band=3, level=8, run=24):
    """Which frame edges show unpainted black: a run of at least `run` px along an edge where the whole outer `band`
    px are black (every channel at or below `level`), the mark of a render that shows past the world or a gap in the
    composite. Scattered dark pixels (static, outlines, the split's ink divider) don't make a run, and a frame that
    is black on purpose (a cut to black) is skipped."""
    a = np.ndarray((s.get_height(), s.get_width(), 4), np.uint8, s.get_data())[..., :3]
    dark = a[::8, ::8].max(axis=-1) <= level
    if dark.mean() > 0.9:                                      # a deliberate black frame
        return []
    out = []
    for name, strip, axis in (("top", a[:band], 0), ("bottom", a[-band:], 0), ("left", a[:, :band], 1),
                              ("right", a[:, -band:], 1)):
        black = (strip.max(axis=-1) <= level).all(axis=axis)   # per position along the edge
        if black.any():
            d = np.diff(np.concatenate(([0], black.astype(np.int8), [0])))
            if (np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max() >= run:
                out.append(name)
    return out


# ---------------------------------------------------------------- the A/B letters (v3)
def ab_times(lines, shot="S24"):
    """Episode times of the "A" in "Option A", the "B" in "Option B" and "Comment" in S24's line (the mix's A/B
    stingers land on those words)."""
    words = [w for ln in lines if ln["scene"] == shot for w in ln["words"]]
    opt = [i for i, w in enumerate(words) if w["w"].lower().startswith("option")]
    com = [w["start"] for w in words if w["w"].lower().startswith("comment")]
    if len(opt) < 2 or not com or opt[1] + 1 >= len(words):
        raise SystemExit(f"{shot}'s line needs 'Option A', 'Option B' and 'Comment' for the A/B cards")
    return words[opt[0] + 1]["start"], words[opt[1] + 1]["start"], com[0]


# ---------------------------------------------------------------- main
def main():
    global SHOTS, CAP_Y_SHOT, SCALE, OW, OH, SHOTS_HI, S24_FOCUS_SHOT, AB_POS_SHOT, AB_LABELS, NO_CAPTIONS
    global HOOK, HOOK_Y, HOOK_SIZE, HOOK_X
    ap = argparse.ArgumentParser()
    ap.add_argument("--animatic", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--version", choices=sorted(VERSIONS), default="ep01v2",
                    help="which cut: its shots/ folder, picture.mp4 and caption placements")
    ap.add_argument("--out", default=None, help="default out/monsters/<version>/picture.mp4")
    ap.add_argument("--shots", default=None, help="default out/monsters/<version>/shots")
    ap.add_argument("--res", type=int, choices=(720, 1080), default=None,
                    help="output width (default: 1080 for diorama_v3, else 720); 720 is quicker for animatics")
    ap.add_argument("--crf", type=int, default=14, help="x264 crf (default 14)")
    ap.add_argument("--only", nargs="+", default=None, metavar="SHOT",
                    help="placement tests: render only these shots (a short picture; not for delivery)")
    ap.add_argument("--max-mb", type=float, default=None,
                    help="size cap in MB (default 95 above 720 wide, so the file goes through git under GitHub's "
                         "100 MB limit); an oversized encode is redone from a lossless copy at the lowest crf "
                         "that fits")
    a = ap.parse_args()
    if a.version == "ep01v2" and a.shots and os.path.abspath(a.shots).startswith(VERSIONS["diorama"]):
        a.version = "diorama"                                  # --shots out/monsters/diorama/shots picks the diorama cut
    SHOTS = a.shots or os.path.join(VERSIONS[a.version], "shots")
    if a.res:
        SCALE = a.res / 720
    else:
        SCALE = RES.get(a.version, 1.0)
    OW, OH = int(round(W * SCALE)), int(round(H * SCALE))
    SHOTS_HI = (os.path.join(os.path.dirname(SHOTS), f"shots_{OW}") if SCALE > 1 else None)
    a.out = a.out or os.path.join(VERSIONS[a.version], "picture.mp4")
    CAP_Y_SHOT = CAP_Y_VERSION[a.version]
    S24_FOCUS_SHOT = S24_FOCUS_VERSION.get(a.version, S24_FOCUS)
    AB_POS_SHOT = AB_POS_VERSION.get(a.version, {})
    ab_scale = AB_SCALE_VERSION.get(a.version, 1.0)
    AB_LABELS = AB_LABELS_VERSION.get(a.version, ("SAVE", "RUN"))
    NO_CAPTIONS = NO_CAPTIONS_VERSION.get(a.version, NO_CAPTIONS)
    if a.version in HOOK_VERSION:
        hv = HOOK_VERSION[a.version]
        HOOK, HOOK_Y, HOOK_SIZE = hv["lines"], hv["y"], hv["size"]
        HOOK_X = hv.get("x")
    split = SPLIT_SHOT_VERSION.get(a.version, "S24")
    rewind = a.version in REWIND_VERSIONS
    if a.check:
        print(f"version {a.version}: shots {os.path.relpath(SHOTS, ROOT)} -> {os.path.relpath(a.out, ROOT)}"
              f" at {OW}x{OH}" + (f" (prefers {os.path.relpath(SHOTS_HI, ROOT)})" if SHOTS_HI else ""))

    tj = json.load(open(TIMINGS[a.version]))
    ab = ab_times(tj["lines"], split) if a.version in AB_VERSIONS else None
    line_of = {}
    for ln in tj["lines"]:
        line_of[ln["scene"]] = (line_of.get(ln["scene"], "") + " " + ln["text"]).strip()
    assert tj["fps"] == FPS, f"timing.json is {tj['fps']} fps, the canvas is {FPS}"
    shots = [Shot(s) for s in tj["shots"]]
    total = tj["total_frames"]
    assert shots[-1].first + shots[-1].frames == total, "shot frames don't add up to the total"
    hook_end = int(round(tj["lines"][0]["end"] * FPS))
    chunks = caption_chunks(tj["lines"])

    warn, missing = [], []
    if not a.animatic:                                         # delivery: refuse before doing any work
        need = [s.path("top") if s.name == split else s.path() for s in shots if not (rewind and s.name == "S02")]
        if any(s.name == split for s in shots):
            need.append(shots[[s.name for s in shots].index(split)].path("bot"))
        gone = [os.path.basename(p) for p in need if not os.path.exists(p)]
        if gone:
            sys.exit(f"missing shots (use --animatic to slate them): {', '.join(gone)}")

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    max_mb = a.max_mb if a.max_mb is not None else (95.0 if OW > W else None)
    lossless = a.out + ".lossless.mkv" if max_mb else None     # yuv420p qp 0: a re-encode from it loses nothing
    x264 = ["-c:v", "libx264", "-preset", "slow", "-pix_fmt", "yuv420p", *CLEAN]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{OW}x{OH}",
                            "-r", str(FPS), "-i", "-", "-crf", str(a.crf), *x264, a.out + ".tmp.mp4",
                            *(["-c:v", "libx264", "-qp", "0", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                               lossless] if lossless else [])], stdin=subprocess.PIPE)
    sheet, edges = [], {}
    s01 = None
    frame_no = 0
    for shot in shots:
        if a.only and shot.name not in a.only:
            continue
        if a.only:
            frame_no = shot.first                             # episode time stays right for captions and cards
        if rewind and shot.name == "S02":
            frames = build_s02(shot, s01, warn) if s01 is not None else None
            if frames is None:
                missing.append("S02 (needs S01)")
        elif shot.name == split:
            frames = build_split(shot, a.animatic, warn, missing)
        else:
            frames = build_plain(shot, a.animatic, warn, missing)
            if shot.name == "S01" and frames is not None:
                s01 = frames
        if a.check:
            srcs = [shot.path(x) for x in (("top", "bot") if shot.name == split else ("",))]
            have = [p for p in srcs if os.path.exists(p)]
            ids = " ".join(_sha(p) for p in have)
            if SCALE > 1 and have:                         # which source each shot used at 1080
                ids += " [" + ",".join("1080" if SHOTS_HI and p.startswith(SHOTS_HI) else f"{W}->{OW} lanczos"
                                       for p in have) + "]"
            print(f"{shot.name:5s} {ids or '-':17s} frames {shot.first:4d}-{shot.first + shot.frames - 1:4d} "
                  f"({shot.frames:3d}, {shot.frames / FPS:5.2f} s){'' if frames is not None else '  SLATE'}"
                  f"{f'  captions at y={CAP_Y_SHOT[shot.name]}' if shot.name in CAP_Y_SHOT else ''}")
        numbered = frames is None and not rewind                 # Episode 2+: a numbered card per frame
        sl = slate(shot.name) if frames is None and not numbered else None
        for i in range(shot.frames):
            if numbered:
                sl = slate(shot.name, i, shot.frames, line_of.get(shot.name, ""))
            src = sl if frames is None else frames[i]
            s, cr = blank()
            paint_full(cr, src if isinstance(src, cairo.ImageSurface) else surface(src))
            t = frame_no / FPS
            if frame_no <= hook_end:
                draw_hook(cr)
            if ab and shot.name == split:                       # helper 7's vote cards, under the captions
                t0 = shot.first / FPS
                for letter, label, at in (("A", AB_LABELS[0], ab[0]), ("B", AB_LABELS[1], ab[1])):
                    if ab_scale == 1.0:
                        fx2d_ab.ab_card(cr, t - t0, at - t0, letter, label, pos=AB_POS_SHOT.get(letter),
                                        pulse_at=ab[2] - t0)
                        continue
                    cr.save()                                  # a smaller card, scaled about its own centre
                    cr.translate(*(AB_POS_SHOT.get(letter) or (fx2d_ab.A_POS if letter == "A" else fx2d_ab.B_POS)))
                    cr.scale(ab_scale, ab_scale)
                    fx2d_ab.ab_card(cr, t - t0, at - t0, letter, label, pos=(0, 0), pulse_at=ab[2] - t0)
                    cr.restore()
            if shot.name not in NO_CAPTIONS:
                draw_caption(cr, t, chunks, tj["total"], CAP_Y_SHOT.get(shot.name, CAP_Y), shot.first / FPS)
            s.flush()
            bad = edge_black(s)
            if bad:
                edges.setdefault(shot.name, []).append((frame_no - shot.first, bad))
            enc.stdin.write(bytes(s.get_data()))
            if a.check and frame_no % 12 == 0:
                sheet.append((frame_no, shot.name, _thumb(s)))
            frame_no += 1
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit("ffmpeg failed")
    crf = a.crf
    if lossless:
        while os.path.getsize(a.out + ".tmp.mp4") / 1e6 > max_mb and crf < 30:
            mb = os.path.getsize(a.out + ".tmp.mp4") / 1e6
            # x264 shrinks ~15% per crf step on these frames; never jump more than the estimate, so the result is the lowest that fits
            crf += max(1, int(math.ceil(math.log(mb / max_mb) / -math.log(0.85))))
            print(f"{mb:.1f} MB > {max_mb:g} MB: re-encoding from the lossless copy at crf {crf}")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", lossless, "-crf", str(crf), *x264,
                            a.out + ".tmp.mp4"], check=True)
        os.remove(lossless)
    # A stream-copy remux clears the "encoder" tag that libx264 writes while encoding, whatever the flags say.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out + ".tmp.mp4", "-c", "copy", *CLEAN, a.out], check=True)
    os.remove(a.out + ".tmp.mp4")
    for w in warn:
        print("WARNING:", w)
    if missing:
        print(f"missing ({len(missing)}): {', '.join(missing)}")
    ok = EDGE_OK_VERSION.get(a.version, {})
    for name in list(edges):
        if name in ok:
            lo, hi, why = ok[name]
            fine = [h for h in edges[name] if lo <= h[0] <= hi]
            if fine:
                print(f"edge bands: {name} frames {fine[0][0]}-{fine[-1][0]} black at the edges on purpose ({why})")
            edges[name] = [h for h in edges[name] if not lo <= h[0] <= hi]
            if not edges[name]:
                del edges[name]
    if edges:
        for name, hits in edges.items():
            sides = sorted({e for _, b in hits for e in b})
            print(f"EDGE BAND: {name}: unpainted black on the {'/'.join(sides)} edge in {len(hits)} frame(s), "
                  f"shot frames {hits[0][0]}-{hits[-1][0]}")
    else:
        print("edge bands: clean (no unpainted black in the outer 3 px of any frame)")
    print(f"{a.out}: {frame_no} frames, {frame_no / FPS:.2f} s, crf {crf}, {os.path.getsize(a.out) / 1e6:.1f} MB")
    if a.check:
        write_sheet(sheet, os.path.join(os.path.dirname(a.out), os.path.basename(SHEET)))


def _thumb(s, tw=144, th=256):
    t = cairo.ImageSurface(cairo.FORMAT_ARGB32, tw, th)
    c = cairo.Context(t)
    c.scale(tw / s.get_width(), th / s.get_height())
    c.set_source_surface(s, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    return t


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
        cr.scale(tw / s.get_width(), th / s.get_height())
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
