"""2D pass and encode for bGqrs's Episode 3 shot S13 (DIORAMA_EP03.md), over the Blender frames, from
build/monsters/diorama_ep03/S13_mark.json (written by diorama_ep03/bgqrs.py):

    S13 "So I put the light below them."  The coral zigzag on his left wrist (helper 9's post_helper9.mark), lit as in
        S10-S12 while the wrist is up; once he has laid it palm up on the grass it blooms on "below": a hot coral pool on
        the ground, a soft beam and thin rays rising from it up into the swarm (a coral wash on the moths' bellies),
        dark grass blades in front of the core (it glows up THROUGH the grass) and a few sparks drifting up. The 3D
        toon paint takes only the light's brightness, so the coral colour of the light is drawn here.

    /home/user/.venv-main/bin/python channels/monsters/diorama_ep03/post_bgqrs.py S13                 (mp4 + sheet)
    /home/user/.venv-main/bin/python channels/monsters/diorama_ep03/post_bgqrs.py S13 --still 40 IN.png OUT.png

Reads build/monsters/diorama_ep03/S13/0001.png ... (or SRC=...). Writes out/monsters/diorama_ep03/shots/S13.mp4 and
S13_sheet.jpg (crf 10, bitexact, stream-copy remux, no encoder strings).
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from channels.monsters import comp, fx2d  # noqa: E402
from channels.monsters.diorama_ep02 import post_helper9 as P9  # noqa: E402
from motion.engine import cairo  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
FPS = 24.0
CORAL, CORAL_HOT, PINK_WHITE = P9.CORAL, P9.CORAL_HOT, P9.PINK_WHITE
BLADE = (0.05, 0.09, 0.13)                 # the grass in front of the light, near-black blue-green
BEAM = (1.0, 0.518, 0.4)                   # #ff8466, the mark's coral (painted OVER, so it stays coral, not
WHITE_HOT = (1.0, 0.97, 0.95)              # yellow-white as an additive glow on a bright pool would)


def marks(shot):
    with open(os.path.join(BUILD, f"{shot}_mark.json")) as fh:
        d = json.load(fh)
    return d["meta"], {int(f): v for f, v in d["frames"].items()}


def _frame(t):
    return int(round(t * FPS)) + 1


def _soft(cr, x, y, r, col, a):
    """A soft radial glow painted OVER (the colour stays itself, unlike fx2d._glow's additive one)."""
    if r <= 0 or a <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(0.4, *col, a * 0.45)
    g.add_color_stop_rgba(1, *col, 0)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()


def _ground_glow(cr, x, y, lv, f):
    """The coral pool on the grass round the wrist (wide and flat) and the hot white core at the wrist."""
    a = min(1.0, lv)
    cr.save()
    cr.translate(x, y)
    cr.scale(1.0, 0.45)
    _soft(cr, 0, 0, 220 * lv, BEAM, 0.30 * a)
    cr.restore()
    _soft(cr, x, y, 52 * lv, BEAM, 0.55 * a)
    fx2d._glow(cr, x, y, 22 * lv, WHITE_HOT, 0.85 * a)                  # the hot white core
    fx2d._glow(cr, x, y, 8 * lv, WHITE_HOT, 1.0 * a)


def _beam(cr, x, y, top, lv, f):
    """The coral uplight cone rising from the wrist to the swarm (widening, fading upward) and soft rays flickering on
    2s, all in the mark's coral (#ff8466), painted OVER."""
    h = y - top
    if h <= 10 or lv <= 0:
        return
    cr.save()
    g = cairo.LinearGradient(0, y, 0, top)
    g.add_color_stop_rgba(0.0, *BEAM, 0.42 * lv)
    g.add_color_stop_rgba(0.3, *BEAM, 0.2 * lv)
    g.add_color_stop_rgba(1.0, *BEAM, 0.0)
    cr.new_path()
    cr.move_to(x - 30, y)
    cr.line_to(x + 30, y)
    cr.line_to(x + 170, top)
    cr.line_to(x - 170, top)
    cr.close_path()
    cr.set_source(g)
    cr.fill()
    rnd = random.Random(f // 2)
    for i in range(5):
        a = (i - 2) * 0.13 + rnd.uniform(-0.04, 0.04)
        ln = h * rnd.uniform(0.5, 0.85)
        w = rnd.uniform(10, 18)
        g = cairo.LinearGradient(x, y, x + math.sin(a) * ln, y - math.cos(a) * ln)
        g.add_color_stop_rgba(0.0, *BEAM, 0.3 * lv)
        g.add_color_stop_rgba(1.0, *BEAM, 0.0)
        cr.new_path()
        cr.move_to(x - w / 2, y)
        cr.line_to(x + w / 2, y)
        cr.line_to(x + math.sin(a) * ln, y - math.cos(a) * ln)
        cr.close_path()
        cr.set_source(g)
        cr.fill()
    # the coral wash up in the swarm (their bellies lit from below)
    cr.translate(x, y - h * 0.62)
    cr.scale(1.0, 0.8)
    _soft(cr, 0, 0, h * 0.62, BEAM, 0.14 * lv)
    cr.restore()


def _blades(cr, x, y, lv, seed=4):
    """Thin dark-green grass blades standing in front of the glow's core, a faint coral rim: the light comes up
    THROUGH the grass."""
    rnd = random.Random(seed)
    for _ in range(16):
        bx = x + rnd.uniform(-40, 40)
        h = rnd.uniform(12, 26)
        lean = rnd.uniform(-7, 7)
        w = rnd.uniform(2.2, 3.6)
        cr.new_path()
        cr.move_to(bx - w / 2, y + 8)
        cr.line_to(bx + w / 2, y + 8)
        cr.line_to(bx + lean, y + 8 - h)
        cr.close_path()
        cr.set_source_rgba(*CORAL_HOT, 0.35 * min(1.0, lv))
        cr.set_line_width(1.4)
        cr.stroke_preserve()
        cr.set_source_rgba(0.08, 0.2, 0.13, 0.72)
        cr.fill()


def _sparks(cr, x, y, top, lv, f, n_=9):
    rnd = random.Random(31)
    for i in range(n_):
        life = rnd.randint(14, 24)
        f0 = rnd.randint(0, life)
        u = ((f - f0) % life) / life
        px = x + rnd.uniform(-40, 40) + math.sin(f / 5.0 + i) * 8
        py = y - (y - top) * 0.7 * u
        a = (1 - u) * lv
        if a > 0.05:
            _soft(cr, px, py, 9, BEAM, 0.7 * a)
            fx2d._glow(cr, px, py, 3, WHITE_HOT, a)


def s13_overlay(meta, M):
    glow, land = meta["glow"], meta["land"]

    def draw(cr, t, start, end=None):
        f = min(max(1, _frame(t)), max(M))
        m = M[f]
        lv = m["level"]
        geo = dict(c=m["c"], ex=m["ex"], ey=m["ey"])
        wx, wy = m["wrist"][0], m["wrist"][1]
        mx, my = m["c"][0], m["c"][1]
        if f >= land:                                       # on the grass: the pool, the beam, the blades, the sparks
            on = min(1.0, max(0.0, (f - glow + 3) / 4.0))
            pool = lv * (0.35 + 0.65 * on)
            px, py = (wx + mx) / 2, (wy + my) / 2
            _beam(cr, px, py, 150, pool * on, f)
            _ground_glow(cr, px, py, pool, f)
            _sparks(cr, px, py, 150, pool * on, f)
        P9.mark(cr, geo, 1.0, 0.5, min(1.0, 0.45 + 0.4 * lv), f, bold=1.6)
        if f >= land:
            _blades(cr, (wx + mx) / 2, (wy + my) / 2 + 8, lv)
        if glow <= f < glow + 4:                            # the flash on "below"
            u = (f - glow) / 4.0
            fx2d._glow(cr, mx, my, 60 + 160 * u, PINK_WHITE, 0.7 * (1 - u))
    return draw


def overlays(shot):
    meta, M = marks(shot)
    return [(s13_overlay(meta, M), dict(start=0.0))]


def run(shot):
    src = comp.Source(os.environ.get("SRC") or os.path.join(BUILD, shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *P9.CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *P9.CLEAN, "-movflags",
                    "+faststart", mp4], check=True)
    os.remove(tmp)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", "select=not(mod(n\\,6)),scale=180:320,tile=5x2",
                    "-frames:v", "1", "-q:v", "3", os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg")], check=True)
    data = open(mp4, "rb").read()
    print(f"{shot}: {rep['frames']} frames -> {mp4}, tags",
          {s: data.count(s.encode()) for s in ("Lavf", "Lavc", "x264", "encoder")})


def still(shot, f, png, out):
    """Preview frame f: the overlay over one rendered still (scaled to 720x1280 if it is a half-scale still)."""
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
