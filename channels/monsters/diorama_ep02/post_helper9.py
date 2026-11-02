"""2D pass for helper 9's Episode 2 shots (DIORAMA_EP02.md), over the Blender frames, from
build/monsters/diorama_ep02/<SHOT>_anchors.json (written by diorama_ep02/helper9.py):

    S14  the wrist mark: from "wrist" a thin coral zigzag draws on from its middle and flickers (on 2s); on "glow" it
         is lit (a white-hot core in a coral glow, a warm bloom on the skin, a small flash and sparkles), then a slow
         pulse.
    S15  the mark, lit (a brighter beat on "same" and "shape"); over the last 4 frames before the cut it eases onto
         the crack's exact screen spot and size; from the cut, the rift in the sky in helper 3's look (diorama_v3/
         helper3_fx.rift: a violet-black gap, a white-pink rim, a magenta glow, drifting shards), and one soft frame
         of glow at the cut so the two shapes read as one.
    S19  glints on the falling drops (on 1s) and a sparkle at the claw tip on "dry".

The zigzag is the Ep 1 crack (helper 3's S09_spark.json "crack", the tank crack normalised to 1 unit tall).

    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep02/post_helper9.py S14            # mp4 + sheet
    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep02/post_helper9.py S14 --still 52  # one frame

Reads build/monsters/diorama_ep02/<SHOT>/0001.png ... (render_shot.py's OUT_DIR), filling any frames rendered elsewhere
from the raw parts in out/monsters/diorama_ep02/parts/<SHOT>_fAAA-BBB.mp4; writes <SHOT>_post/ there, then
out/monsters/diorama_ep02/shots/<SHOT>.mp4 (crf 10, bitexact, stream-copy remux, no encoder strings) and
<SHOT>_sheet.jpg.
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import cairo  # noqa: E402
from channels.monsters import fx2d  # noqa: E402
from channels.monsters.diorama_v3 import helper3_fx as h3fx  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep02", "shots")
PARTS = os.path.join(ROOT, "out", "monsters", "diorama_ep02", "parts")
SPARK = os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots", "S09_spark.json")
CRACK = [[-0.1583, -0.5], [-0.1399, -0.347], [-0.0348, -0.2378], [0.0319, -0.0935], [0.0779, 0.0005],
         [-0.0014, 0.1177], [0.0614, 0.2237], [0.0758, 0.3353], [0.1583, 0.5]]      # S09_spark.json's, as a fallback
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]
CORAL = (1.0, 0.48, 0.36)
CORAL_HOT = (1.0, 0.66, 0.55)
PINK_WHITE = (1.0, 0.95, 0.93)
FPS = 24.0


def crack():
    try:
        with open(SPARK) as fh:
            return json.load(fh)["crack"]
    except (OSError, KeyError, ValueError):
        return CRACK


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        a = json.load(fh)
    return a["meta"], {int(f): v for f, v in a["frames"].items()}


# ------------------------------------------------------------------------------------------------------------ mark
def _pts(geo, k, band=0.5, steps=10):
    """The zigzag's points on screen (x, y, along) for a geometry {c, ex, ey}: the polyline sampled densely, keeping
    only |along| <= band (so it draws on from its middle as band grows to 0.5)."""
    cx, cy = geo["c"]
    ex, ey = geo["ex"], geo["ey"]
    pts = crack()
    out = []
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        for i in range(steps + 1):
            t = i / steps
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            if abs(y) <= band:
                out.append(((cx + ex[0] * x + ey[0] * y) * k, (cy + ex[1] * x + ey[1] * y) * k, y))
    return out


def mark(cr, geo, k, band, inten, f, seed=0):
    """The coral zigzag: `band` 0..0.5 drawn from its middle, `inten` 0..1 (faint line -> lit)."""
    if band <= 0 or inten <= 0 or geo is None:
        return
    line = _pts(geo, k, band)
    if len(line) < 2:
        return
    size = math.hypot(*geo["ey"]) * k                         # px per crack-height unit = the mark's length
    cx, cy = geo["c"][0] * k, geo["c"][1] * k
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)

    def path():
        cr.new_path()
        cr.move_to(line[0][0], line[0][1])
        for x, y, _ in line[1:]:
            cr.line_to(x, y)
    fx2d._glow(cr, cx, cy, size * 0.75, CORAL, 0.38 * inten)     # the warm bloom on the skin
    core = max(1.8 * k, size * 0.014)
    for wdt, a, col in ((core * 9, 0.10, CORAL), (core * 5, 0.22, CORAL), (core * 2.6, 0.55, CORAL_HOT)):
        path()
        cr.set_source_rgba(*col, a * inten)
        cr.set_line_width(wdt)
        cr.stroke()
    path()                                                     # the line itself: coral when faint, white-hot when lit
    w = min(1.0, inten * 1.4)
    cr.set_source_rgba(CORAL[0] + (PINK_WHITE[0] - CORAL[0]) * w, CORAL[1] + (PINK_WHITE[1] - CORAL[1]) * w,
                       CORAL[2] + (PINK_WHITE[2] - CORAL[2]) * w, min(1.0, 0.45 + inten))
    cr.set_line_width(core)
    cr.stroke()
    cr.restore()


def _lerp_geo(a, b, u):
    return dict(c=[a["c"][i] + (b["c"][i] - a["c"][i]) * u for i in range(2)],
                ex=[a["ex"][i] + (b["ex"][i] - a["ex"][i]) * u for i in range(2)],
                ey=[a["ey"][i] + (b["ey"][i] - a["ey"][i]) * u for i in range(2)])


# ------------------------------------------------------------------------------------------------------------ shots
def s14(cr, f, meta, A, k):
    fw, fg = meta["f_wrist"], meta["f_glow"]
    geo = A[f]["mark"]
    if f < fw:
        return
    rnd = random.Random(f // 2)
    if f < fg:                                                  # drawing on, flickering (on 2s)
        band = 0.5 * min(1.0, (f - fw + 1) / 10)
        inten = (0.18 + 0.32 * (f - fw) / (fg - fw)) * (0.35 if (f // 2) % 3 == 0 else 1.0) * rnd.uniform(0.7, 1.0)
        mark(cr, geo, k, band, inten, f)
        return
    u = (f - fg) / FPS
    inten = 1.0 + 0.25 * max(0.0, 1 - u / 0.25) - 0.1 * (0.5 + 0.5 * math.sin(u * 4.0))
    mark(cr, geo, k, 0.5, inten, f)
    x, y = geo["c"][0] * k, geo["c"][1] * k
    size = math.hypot(*geo["ey"]) * k
    t, t0 = f / FPS, fg / FPS
    fx2d.glow_burst(cr, t, t0, x, y, r=size * 1.6, col=CORAL_HOT, dur=0.45, rays=10, seed=3)
    fx2d.sparkles(cr, t, t0 + 0.04, x, y, n=7, radius=size * 0.9, size=size * 0.16,
                  cols=((1, 0.8, 0.7, 1), fx2d.WHITE, (1, 0.6, 0.5, 1)), life=1.0, seed=5)


def s15(cr, f, meta, A, k):
    fc = meta["fc"]
    if f < fc:
        geo = A[f]["mark"]
        if fc - 4 <= f and A.get(fc, {}).get("rift"):            # ease onto the crack's spot and size for the cut
            geo = _lerp_geo(geo, A[fc]["rift"], (f - (fc - 5)) / 4)
        beat = 0.0
        for w in meta.get("beats", []):
            beat = max(beat, max(0.0, 1 - abs(f - w) / 4))
        mark(cr, geo, k, 0.5, 1.0 + 0.25 * beat - 0.08 * (0.5 + 0.5 * math.sin(f / 5.0)), f)
        if f == fc - 1:
            x, y = geo["c"][0] * k, geo["c"][1] * k
            fx2d._glow(cr, x, y, math.hypot(*geo["ey"]) * k * 0.9, CORAL_HOT, 0.45)
        return
    spark = dict(rift={str(g): v.get("rift") for g, v in A.items() if g >= fc}, crack_on=[-30, -25], f_in=fc - 14,
                 crack=crack())
    h3fx.rift(cr, spark, f, k)
    if f == fc:                                                  # one soft frame of glow at the cut
        r = A[fc]["rift"]
        if r:
            fx2d._glow(cr, r["c"][0] * k, r["c"][1] * k, math.hypot(*r["ey"]) * k * 0.9, h3fx.GLOW, 0.4)


def s19(cr, f, meta, A, k):
    fc, fd = meta["fc"], meta["f_dry"]
    if f < fc:
        return
    for i, (x, y, z) in enumerate(A[f]["drops"]):                # a glint on each falling drop
        if z <= 0 or not (-20 < x < 740 and -20 < y < 1300):
            continue
        tw = 0.6 + 0.4 * math.sin(f * 1.7 + i)
        fx2d._glow(cr, x * k, y * k, 14 * k, (0.85, 0.95, 1.0), 0.5 * tw)
        fx2d._star4(cr, x * k - 3 * k, y * k - 4 * k, 6 * k * tw, 0.3)
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.fill()
    tip = A[f]["tip"]
    fx2d.sparkle(cr, f / FPS, fd / FPS, tip[0] * k, tip[1] * k, size=26 * k, col=(0.8, 0.95, 1.0, 1), life=0.9)


DRAW = {"S14": s14, "S15": s15, "S19": s19}


def frame(shot, f, src, dst, meta, A):
    surf = cairo.ImageSurface.create_from_png(src)
    if surf.get_format() != cairo.FORMAT_ARGB32:
        s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
        c2 = cairo.Context(s2)
        c2.set_source_surface(surf)
        c2.paint()
        surf = s2
    cr = cairo.Context(surf)
    DRAW[shot](cr, f, meta, A, surf.get_width() / 720)
    surf.flush()
    surf.write_to_png(dst)


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:04d}.png")).convert("RGB") for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 7)
    out = Image.new("RGB", (w * cols, h * (-(-len(ims) // cols))), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path, quality=88)


def join(shot, n):
    """Fill build/.../<SHOT>/NNNN.png from the raw parts other helpers rendered (parts/<SHOT>_fAAA-BBB.mp4, frame A
    first) wherever this container has no Blender frame; then check that every frame 1..n is there."""
    import glob
    import re
    src_dir = os.path.join(BUILD, shot)
    os.makedirs(src_dir, exist_ok=True)
    for part in sorted(glob.glob(os.path.join(PARTS, f"{shot}_f*.mp4"))):
        m = re.search(r"_f(\d+)-(\d+)\.mp4$", part)
        a, b = int(m.group(1)), int(m.group(2))
        if all(os.path.exists(os.path.join(src_dir, f"{f:04d}.png")) for f in range(a, b + 1)):
            continue
        tmp = os.path.join(BUILD, f"{shot}_join")
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", part, "-start_number", str(a),
                        os.path.join(tmp, "%04d.png")], check=True)
        got = sorted(os.listdir(tmp))
        if len(got) != b - a + 1:
            raise SystemExit(f"{part}: {len(got)} frames, expected {b - a + 1}")
        for g in got:
            if not os.path.exists(os.path.join(src_dir, g)):
                shutil.move(os.path.join(tmp, g), os.path.join(src_dir, g))
        shutil.rmtree(tmp)
        print("joined", os.path.basename(part))
    missing = [f for f in range(1, n + 1) if not os.path.exists(os.path.join(src_dir, f"{f:04d}.png"))]
    if missing:
        raise SystemExit(f"{shot}: missing frames {missing[0]}..{missing[-1]} ({len(missing)})")


def run(shot):
    meta, A = anchors(shot)
    join(shot, max(A))
    if shot == "S15":
        from_words = json.load(open(os.path.join(ROOT, "channels", "monsters", "ep02", "timing.json")))
        s = next(x for x in from_words["shots"] if x["shot"] == "S15")
        meta["beats"] = [round((w["start"] - s["start"]) * 24) + 1 for ln in from_words["lines"]
                         if ln.get("scene") == "S15" for w in ln["words"] if w["w"].strip(".,").lower() in
                         ("same", "shape")]
    src_dir, out_frames = os.path.join(BUILD, shot), os.path.join(BUILD, f"{shot}_post")
    shutil.rmtree(out_frames, ignore_errors=True)
    os.makedirs(out_frames)
    n = max(A)
    for f in range(1, n + 1):
        frame(shot, f, os.path.join(src_dir, f"{f:04d}.png"), os.path.join(out_frames, f"{f:04d}.png"), meta, A)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%04d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    sheet(out_frames, n, os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    print(mp4, n, "frames")


def still(shot, f, src, dst):
    meta, A = anchors(shot)
    if shot == "S15":
        meta.setdefault("beats", [])
    frame(shot, f, src, dst, meta, A)
    print(dst)


if __name__ == "__main__":
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        still(sys.argv[1], int(sys.argv[i + 1]), sys.argv[i + 2], sys.argv[i + 3])
    else:
        run(sys.argv[1])
