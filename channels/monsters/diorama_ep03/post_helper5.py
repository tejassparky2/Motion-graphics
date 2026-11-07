"""2D pass and encode for helper 5's Episode 3 shots (DIORAMA_EP03.md), over the Blender frames with comp.py:

    S15 "Every single moth landed on its back."  Over the four hero moths in the foreground (helper5.S15_HEROES):
        little dizzy stars (yellow and white 4-point sparkles) circling above each one on 2s, and a turning spiral
        over each of its two wing eye-spots, so "on its back, dazed" reads at phone size. From frame 1 to the end,
        each moth's loop out of step with the others.
    S07, S19bot: no 2D pass (the shots are final as rendered); this script only encodes them.

    FPS=24 python channels/monsters/diorama_ep03/post_helper5.py S15 [S07 S19bot]          (the shot: mp4 + sheet)
    FPS=24 python channels/monsters/diorama_ep03/post_helper5.py S15 --still 60 STILL.png OUT.png  (a preview)

Reads the frames from build/monsters/diorama_ep03/render/<SHOT>/0001.png ... (or the folder given by SRC=...) and,
for S15, build/monsters/diorama_ep03/S15_heroes.json (written by diorama_ep03/helper5.py). No text.
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

from channels.monsters import comp, fx2d  # noqa: E402
from channels.monsters.diorama_v3.post_helper1 import CLEAN, sheet  # noqa: E402
from motion.engine import FPS, cairo  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
INK = (0.06, 0.05, 0.10, 1.0)


def heroes(shot):
    with open(os.path.join(BUILD, f"{shot}_heroes.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def _row(a, t):
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f], f


def dizzy(a):
    """Stars circling over each hero moth and spirals over its wing eye-spots, on 2s."""
    def draw(cr, t, start, end=None):
        if t < start or (end is not None and t > end):
            return
        rows, f = _row(a, t)
        f2 = f - (f % 2)                                                 # on 2s
        for i, m in enumerate(rows):
            cx, cy, depth = m["c"]
            if depth <= 0:
                continue
            s = max(6.0, m["size"])                                      # px per moth unit
            # the stars: three, on a tilted ellipse above the body, one full turn a second
            ph = f2 / FPS * 2 * math.pi + i * 1.7
            rx, ry = s * 1.25, s * 0.42
            oy = cy - s * 1.25
            for j in range(3):
                a_ = ph + j * 2 * math.pi / 3
                x, y = cx + rx * math.cos(a_), oy + ry * math.sin(a_)
                r = s * (0.26 if j % 2 == 0 else 0.2) * (0.85 + 0.25 * math.sin(a_))
                fx2d._star4(cr, x, y, r, rot=a_ * 0.5, waist=0.22)
                cr.set_source_rgba(*(fx2d.YELLOW if j != 1 else fx2d.WHITE))
                cr.fill_preserve()
                cr.set_source_rgba(*INK)
                cr.set_line_width(max(1.5, s * 0.04))
                cr.stroke()
            # the spirals: over each wing eye-spot, turning (one each way)
            for k, (sx, sy, sd) in enumerate(m["spots"]):
                if sd <= 0:
                    continue
                rr = s * 0.24
                turn = (1 if k == 0 else -1) * (f2 / FPS * 2 * math.pi * 1.5 + i)
                for q in range(41):
                    v = q / 40
                    an = turn + (1 if k == 0 else -1) * v * 2.5 * 2 * math.pi
                    x, y = sx + math.cos(an) * rr * v, sy + math.sin(an) * rr * v
                    (cr.move_to if q == 0 else cr.line_to)(x, y)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.set_source_rgba(1, 1, 1, 0.95)
                cr.set_line_width(max(2.5, s * 0.075))
                cr.stroke_preserve()
                cr.set_source_rgba(*INK)
                cr.set_line_width(max(1.2, s * 0.035))
                cr.stroke()
    return draw


def overlays(shot):
    if shot != "S15":
        return []
    a = heroes(shot)
    return [(dizzy(a), dict(start=0.0))]


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
