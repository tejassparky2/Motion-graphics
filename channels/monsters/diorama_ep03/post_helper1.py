"""2D pass for helper 1's Episode 3 shots (DIORAMA_EP03.md), over the Blender frames with comp.py:

    S03  the late-afternoon grade S02 uses (post_helper3.late_afternoon: greens -25% saturation, level -10%, peach
         highlights), then the mark on his raised inner left forearm (helper 9's zigzag, post_helper9.mark: lit, soft
         pulse) and Ep 2's three thin scratch marks beside it (post_helper1.torn_sleeve, no blood).
    itch(a, name)  comic itch squiggles round an anchor (the scratcher's blotch: village.scratcher's "blotch"), for any
         shot that shows the scratcher (S07).
    S09  the same, brighter (night: the only light), and the bells ringing: arcs pulsing out on both sides of every
         porch bell and hand bell, on 2s, from the first frames to the end.

    FPS=24 python channels/monsters/diorama_ep03/post_helper1.py S03 [S09]       (the shot: mp4 + sheet)
    FPS=24 python channels/monsters/diorama_ep03/post_helper1.py S03 --still 20 STILL.png OUT.png   (a preview)

Reads build/monsters/diorama_ep03/<SHOT>/0001.png ... and <SHOT>_anchors.json (written by diorama_ep03/helper1.py).
No text.
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

from motion.engine import FPS  # noqa: E402
from channels.monsters import comp, fx2d  # noqa: E402
from channels.monsters.diorama_ep02 import post_helper1 as E2  # noqa: E402
from channels.monsters.diorama_ep02 import post_helper9 as P9  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
PINK = (1.0, 0.62, 0.62)


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh)["frames"].items()}


def mark(a, level=0.9, bold=1.6, halo=0.0):
    """The coral zigzag on his inner left forearm, every frame where it faces the camera."""
    def draw(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(a))
        g = a[f]["mark"]
        if g.get("z", 1) <= 0:
            return
        geo = P9._on_arm(g)
        x, y = geo["c"]
        size = math.hypot(*geo["ey"])
        lvl = level * (0.92 + 0.08 * math.sin(f / 5.0))
        if halo:
            fx2d._glow(cr, x, y, size * 1.6, PINK, halo)
        P9.mark(cr, geo, 1.0, 0.5, lvl, f, bold=bold)
    return draw


def grade_late_afternoon(cr, t, start, end=None):
    """The whole frame through helper 3's S02 grade (so S03 cuts with S02; the sun sets on S04)."""
    import numpy as np
    from channels.monsters.diorama_ep03.post_helper3 import late_afternoon
    surf = cr.get_target()
    surf.flush()
    h, w = surf.get_height(), surf.get_width()
    arr = np.ndarray((h, w, 4), np.uint8, buffer=surf.get_data(), strides=(surf.get_stride(), 4, 1))
    rgb = late_afternoon(arr[..., 2::-1].astype(np.float32))
    arr[..., 2::-1] = np.clip(rgb, 0, 255).astype(np.uint8)
    surf.mark_dirty()


def itch(a, name="blotch", size=1.6):
    """Comic itch squiggles: three short zigzag strokes popping round the anchor `name` on 2s (re-dealt each pair of
    frames, at different angles), white with a dark edge so they read on the night grade. No text."""
    import random

    def draw(cr, t, start, end=None):
        if t < start or (end is not None and t > end):
            return
        f = min(max(1, int(round(t * FPS)) + 1), max(a))
        x, y, z = a[f][name]
        if z <= 0:
            return
        f2 = f - f % 2
        rnd = random.Random(f2 * 7 + 3)
        for k in range(3):
            ang = -math.pi / 2 + (k - 1) * 0.9 + rnd.uniform(-0.25, 0.25)
            r0 = (26 + rnd.uniform(0, 8)) * size
            L = (22 + rnd.uniform(0, 8)) * size
            ux, uy = math.cos(ang), math.sin(ang)
            nx, ny = -uy, ux
            pts = []
            for i in range(5):
                d = r0 + L * i / 4
                o = (5 * size) * (1 if i % 2 else -1)
                pts.append((x + ux * d + nx * o, y + uy * d + ny * o))
            for wdt, col in ((6.5 * size, (0.15, 0.1, 0.15, 0.85)), (3.0 * size, (1, 1, 1, 0.95))):
                cr.new_path()
                cr.move_to(*pts[0])
                for q in pts[1:]:
                    cr.line_to(*q)
                cr.set_line_width(wdt)
                cr.set_source_rgba(*col)
                cr.stroke()
    return draw


def overlays(shot):
    a = anchors(shot)
    if shot == "S03":
        return [(grade_late_afternoon, dict(start=0.0)), (mark(a, 0.85, 1.8), dict(start=0.0)),
                (E2.torn_sleeve, dict(start=0.0, a=a))]
    if shot == "S09":
        bells = [k for k in a[1] if k.startswith("bell_")]
        out = [(mark(a, 1.15, 2.2, halo=0.35), dict(start=0.0)), (E2.torn_sleeve, dict(start=0.0, a=a))]
        out += [(E2.bell_rings, dict(start=(2 + 2 * i) / FPS, a=a, name=nm)) for i, nm in enumerate(bells)]
        return out
    if shot == "VN":
        return [(itch(a, "blotch"), dict(start=0.0))]
    return []


def run(shot):
    src = comp.Source(os.path.join(BUILD, shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    shutil.rmtree(out_frames, ignore_errors=True)
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *E2.CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *E2.CLEAN, "-movflags",
                    "+faststart", mp4], check=True)
    os.remove(tmp)
    E2.sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    print(f"{shot}: {rep['frames']} frames -> {mp4}, tags",
          {s: data.count(s.encode()) for s in ("Lavf", "Lavc", "x264", "encoder")})


def still(shot, f, png, out):
    """Preview frame f: the overlays over one rendered still (scaled up to 720x1280 if it is a half-scale still)."""
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
    args = sys.argv[1:]
    if "--still" in args:
        i = args.index("--still")
        still(args[0], int(args[i + 1]), args[i + 2], args[i + 3])
    else:
        for s in args:
            run(s)
