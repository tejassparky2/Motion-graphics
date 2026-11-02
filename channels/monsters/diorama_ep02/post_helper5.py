"""2D pass for helper 5's Episode 2 shots (DIORAMA_EP02.md), over the Blender frames with comp.py:

    S07 "So I turned it around."  A small sweat bead runs down his temple while he turns it (the bomb-tech focus).
    S12 "Then the shrimp looked at me."  The sweat drop pops in beside his head as the claw comes up (f37).
    S13 "And tapped my nose."  A tiny sparkle "tink" on his nose at the tap (f18); then his stunned dot eyes, held
        to the end (from f19).
    S11 has no 2D pass (the shot is final as rendered).

    FPS=24 python channels/monsters/diorama_ep02/post_helper5.py S13 [S07 S12]          (the shot: mp4 + sheet)
    FPS=24 python channels/monsters/diorama_ep02/post_helper5.py S13 --still 30 STILL.png OUT.png   (a preview)

Reads the frames from build/monsters/diorama_ep02/render/<SHOT>/0001.png ... (or the folder given by SRC=...) and
<SHOT>_anchors.json (written by diorama_ep02/helper5.py). The comic skin under the dot eyes is sampled from the plate
between his eyes, frame by frame, so it matches the lit render. No text.
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

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from channels.monsters import comp, fx2d_anime  # noqa: E402
from channels.monsters.diorama_v3.post_helper1 import CLEAN, sheet  # noqa: E402
from channels.monsters import fx2d  # noqa: E402
from motion.engine import FPS  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep02", "shots")
TAP = 18                                     # S13: the claw touches his nose (helper5.s13 TAP)
RAISE = 36                                   # S12: the claw comes up (helper5.s12 RAISE)


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(kk): v for kk, v in json.load(fh).items()}


def at(a, t, name):
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


def _face(a, t):
    (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
    d = math.hypot(rx - lx, ry - ly)
    tilt = math.atan2(ry - ly, rx - lx)
    if abs(tilt) > math.pi / 2:
        tilt -= math.copysign(math.pi, tilt)
    return (lx, ly), (rx, ry), d, tilt


def _skin(cr, pts, r):
    """The plate's skin colour: the median of small patches just beside each eye (outer cheek side)."""
    surf = cr.get_target()
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    buf = np.ndarray((h, w, 4), np.uint8, surf.get_data(), strides=(surf.get_stride(), 4, 1))
    px = []
    for x, y in pts:
        x0, x1 = int(max(0, x - r)), int(min(w, x + r))
        y0, y1 = int(max(0, y - r)), int(min(h, y + r))
        if x1 > x0 and y1 > y0:
            px.append(buf[y0:y1, x0:x1, :3].reshape(-1, 3))
    if not px:
        return fx2d_anime.SKIN
    b, g, rr = np.median(np.concatenate(px), axis=0) / 255.0       # cairo ARGB32 is BGRA in memory
    return (rr, g, b, 1.0)


def dots(a):
    def draw(cr, t, start, end=None):
        if t < start or (end is not None and t > end):
            return
        (lx, ly), (rx, ry), d, tilt = _face(a, t)
        er = 0.3 * d
        ux, uy = (rx - lx) / max(d, 1e-3), (ry - ly) / max(d, 1e-3)
        # sample below each eye, toward the cheek (the lids and brows sit above)
        nx, ny = -uy, ux
        if ny < 0:
            nx, ny = -nx, -ny
        samp = [(lx + nx * er * 2.4, ly + ny * er * 2.4), (rx + nx * er * 2.4, ry + ny * er * 2.4)]
        skin = _skin(cr, samp, max(2, er * 0.5))
        fx2d_anime.dot_eyes(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * 2.6, end=end,
                            eyes=((lx, ly), (rx, ry)), er=er, skin=skin, tilt=tilt)
    return draw


def sweat(a, bead=False, side=1, k=2.6):
    def draw(cr, t, start, end=None):
        _, _, d, tilt = _face(a, t)
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        fx2d_anime.sweat_drop(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * k, end=end, side=side,
                              bead=bead, tilt=tilt)
    return draw


def tink(a):
    def draw(cr, t, start, end=None):
        x, y = at(a, t, "nose")
        fx2d.sparkle(cr, t, start, x, y, size=34, life=0.6)
        fx2d.sparkle(cr, t, start + 0.04, x + 26, y - 22, size=18, life=0.5, phase=0.5)
    return draw


def overlays(shot):
    if shot not in ("S07", "S12", "S13"):          # S11 has no 2D pass (and no anchors)
        return []
    a = anchors(shot)
    n = max(a)
    if shot == "S07":
        return [(sweat(a, bead=True, side=-1, k=4.2), dict(start=5 / FPS, end=(n - 1) / FPS))]
    if shot == "S12":
        return [(sweat(a), dict(start=(RAISE + 1) / FPS, end=(n - 1) / FPS))]
    if shot == "S13":
        return [(tink(a), dict(start=(TAP - 1) / FPS)),
                (dots(a), dict(start=TAP / FPS, end=(n - 1) / FPS))]
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
    for i in range(1, f + 1):
        im.save(os.path.join(tmp, f"{i:04d}.png")) if i == f else os.symlink(os.path.join(tmp, f"{f:04d}.png"),
                                                                             os.path.join(tmp, f"{i:04d}.png"))
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
