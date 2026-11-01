"""2D pass for helper 4's Episode 2 shots (DIORAMA_EP02.md), over the Blender frames with comp.py:

    S05 "...In my bare hands."  After the cut up to his face (f50) the anime sweat drop pops in beside his head on
        "In my" (fx2d_anime.sweat_drop, tracked to his eyes).
    S06 "...Straight ahead."  On "Straight", an arrow-like jet streak shoots straight out of the claw to the frame
        edge (the claw's own line, nothing in any other direction): a tapered white jet with an ink outline and an
        arrowhead front, two speed lines riding along it and a small pressure ring at the muzzle. No text.

    FPS=24 python channels/monsters/diorama_ep02/post_helper4.py S05 [S06]                (mp4 + sheet per shot)
    FPS=24 python channels/monsters/diorama_ep02/post_helper4.py S06 --still 70 STILL.png OUT.png   (a preview)

Reads build/monsters/diorama_ep02/render/<SHOT>/0001.png ... (or SRC=...) and <SHOT>_anchors.json (written by
diorama_ep02/helper4.py). Writes out/monsters/diorama_ep02/shots/<SHOT>.mp4 + <SHOT>_sheet.jpg (crf 10, no tags).
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from channels.monsters import comp, fx2d_anime  # noqa: E402
from channels.monsters.diorama_v3.post_helper1 import CLEAN, sheet  # noqa: E402
from motion.engine import FPS, cairo  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep02", "shots")
S05_CUT = 50                                  # helper4.S05_CUT
INK = (0.106, 0.094, 0.188, 1.0)              # puffshrimp INK #1b1830
JET = (0.93, 0.98, 1.0, 1.0)
JET_EDGE = (0.62, 0.88, 1.0, 1.0)


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def at(a, t, name):
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


def _words(line_id):
    with open(os.path.join(ROOT, "channels", "monsters", "ep02", "timing.json")) as f:
        d = json.load(f)
    ln = next(x for x in d["lines"] if x["id"] == line_id)
    s0 = next(s["start"] for s in d["shots"] if s["shot"] == ln["scene"])
    return {w["w"]: (w["start"] - s0, w["end"] - s0) for w in ln["words"]}


# ------------------------------------------------------------------------------------------------------------ S05
def sweat(a, side=1, k=2.6):
    def draw(cr, t, start, end=None):
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.sweat_drop(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * k, end=end, side=side,
                              tilt=tilt)
    return draw


def terror(a, k=0.34):
    """Pin-prick terror eyes over his own (fx2d_anime.terror_eyes, the blue shock lines included), tracked."""
    def draw(cr, t, start, end=None):
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.terror_eyes(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * 2.6, end=end,
                               eyes=((lx, ly), (rx, ry)), er=k * d, tilt=tilt)
    return draw


# ------------------------------------------------------------------------------------------------------------ S06
def _ease_out(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def jet(a):
    """The arrow-like jet: its front races from the muzzle to past the frame edge in 4 frames, holds 5, then the
    tail catches up and it thins away over 5 (on 1s, it's an effect)."""
    def draw(cr, t, start, end=None):
        u = t - start
        if u < 0 or u > 14 / FPS:
            return
        (x0, y0), (x1, y1) = at(a, t, "tip"), at(a, t, "ahead")
        ang = math.atan2(y1 - y0, x1 - x0)
        L = 900.0                                                         # past the frame edge
        front = L * _ease_out(u / (4 / FPS))
        tail = L * max(0.0, (u - 9 / FPS) / (5 / FPS)) ** 1.5
        thin = 1.0 - max(0.0, (u - 9 / FPS) / (5 / FPS))
        if front - tail < 4:
            return
        cr.save()
        cr.translate(x0, y0)
        cr.rotate(ang)
        w0, w1 = 7.0 * thin + 2, 26.0 * thin + 3                          # tapered: thin at the muzzle
        head = min(46.0, front - tail)

        def body(grow):
            cr.new_path()
            cr.move_to(tail, -(w0 + grow) / 2)
            cr.line_to(front - head, -(w1 + grow) / 2)
            cr.line_to(front - head, -(w1 * 1.7 + grow) / 2)               # the arrowhead's barbs
            cr.line_to(front + grow * 0.6, 0)
            cr.line_to(front - head, (w1 * 1.7 + grow) / 2)
            cr.line_to(front - head, (w1 + grow) / 2)
            cr.line_to(tail, (w0 + grow) / 2)
            cr.close_path()
        body(9.0)
        cr.set_source_rgba(*INK)
        cr.fill()
        body(3.0)
        cr.set_source_rgba(*JET_EDGE)
        cr.fill()
        body(-5.0)
        cr.set_source_rgba(*JET)
        cr.fill()
        for off, k in ((-1, 0.55), (1, 0.75)):                           # speed lines riding along it
            yy = off * (w1 * 1.4 + 14)
            xa, xb = tail + (front - tail) * 0.15, tail + (front - tail) * k
            if xb - xa > 10:
                cr.new_path()
                cr.move_to(xa, yy)
                cr.line_to(xb, yy)
                cr.set_line_width(6.0 * thin + 1)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.set_source_rgba(*INK)
                cr.stroke()
        if u < 6 / FPS:                                                   # the pressure ring at the muzzle
            r = 18 + 70 * _ease_out(u / (6 / FPS))
            cr.save()
            cr.scale(0.45, 1.0)
            cr.new_path()
            cr.arc(0, 0, r, 0, 2 * math.pi)
            cr.set_line_width(7.0 * (1 - u / (6 / FPS)) + 1)
            cr.set_source_rgba(*INK)
            cr.stroke()
            cr.restore()
        cr.restore()
    return draw


def overlays(shot):
    a = anchors(shot)
    n = max(a)
    if shot == "S05":
        w = _words("l5")
        return [(terror(a), dict(start=(S05_CUT - 1) / FPS, end=(n - 1) / FPS)),
                (sweat(a), dict(start=w["In"][0] - 2 / FPS, end=(n - 1) / FPS))]
    if shot == "S06":
        w = _words("l6")
        return [(jet(a), dict(start=w["Straight"][0]))]
    return []


def run(shot):
    src = comp.Source(os.environ.get("SRC") or os.path.join(BUILD, "render", shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    print(f"{shot}: {rep['frames']} frames -> {mp4}, tags",
          {s: data.count(s.encode()) for s in ("Lavf", "Lavc", "x264", "encoder")})


def still(shot, f, png, out):
    """Preview frame f: the overlays over one rendered still (scaled to 720x1280 if it is a half-scale still)."""
    tmp = tempfile.mkdtemp()
    im = Image.open(png).convert("RGB").resize((720, 1280))
    im.save(os.path.join(tmp, f"{f:04d}.png"))
    for i in range(1, f):
        os.symlink(os.path.join(tmp, f"{f:04d}.png"), os.path.join(tmp, f"{i:04d}.png"))
    o = tempfile.mkdtemp()
    comp.render([comp.Shot(comp.Source(tmp), overlays=overlays(shot), name=shot)], o, frames=(f - 1, f - 1),
                verbose=False, check=False)
    shutil.copy(os.path.join(o, f"{f:05d}.png"), out)
    shutil.rmtree(tmp)
    shutil.rmtree(o)


if __name__ == "__main__":
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        still(sys.argv[1], int(sys.argv[i + 1]), sys.argv[i + 2], sys.argv[i + 3])
    else:
        for s in sys.argv[1:]:
            run(s)
