"""2D pass for the chest scene (S01, S16-S21): the comic-face kit (TP7) and the shot effects, composited with comp.py
over the Blender frames, then the mp4 and contact sheet for out/monsters/ep01v2/shots/.

    FPS=24 python channels/monsters/ep01v2/bgqrs_post.py S19 [S20 ...]

Reads build/monsters/ep01v2/<SHOT>/0001.png ... (render_shot.py output; subject/ when rendered with --subject) and
the screen anchors the builder wrote (build/monsters/ep01v2/<SHOT>_anchors.json). No text and no HUD (owner's rule).
"""
import json
import math
import os
import subprocess
import sys

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from motion.engine import H, W, cairo, clamp01, ease_out  # noqa: E402
from channels.monsters import comp, fx2d, fx2d_extra  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "ep01v2")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "ep01v2", "shots")
FPS = 24
# render.py's output hygiene: no container metadata, no encoder tags, no x264 settings SEI
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def at(a, t, name):
    """Anchor `name` at shot time t (frame-accurate, held past the last frame)."""
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


# ---------------------------------------------------------------- the comic-face kit (TP7)

def sweat_drop(cr, t, start, x, y, size=30, slide=18, end=None, tilt=0.35):
    """The anime sweat bead: a fat teardrop (point up) beside the face, light blue with a white glint and a navy
    outline. It pops in on 2s and slides down `slide` px in steps of 3 frames."""
    if t < start or (end is not None and t > end):
        return
    el = t - start
    pop = (0.6, 1.15, 1.0)[min(2, int(el * FPS) // 2)]
    dy = slide * clamp01(math.floor(el * FPS / 3) * 3 / FPS / 1.5)
    cr.save()
    cr.translate(x, y + dy)
    cr.rotate(tilt)
    cr.scale(size * pop / 30, size * pop / 30)
    cr.move_to(0, -30)
    cr.curve_to(6, -14, 16, -2, 16, 10)
    cr.curve_to(16, 21, 8, 28, 0, 28)
    cr.curve_to(-8, 28, -16, 21, -16, 10)
    cr.curve_to(-16, -2, -6, -14, 0, -30)
    cr.close_path()
    g = cairo.LinearGradient(0, -30, 0, 28)
    g.add_color_stop_rgb(0, 0.86, 0.96, 1.0)
    g.add_color_stop_rgb(1, 0.45, 0.74, 0.98)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgb(0.12, 0.2, 0.42)
    cr.set_line_width(3.2)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
    cr.arc(-6, 12, 4.2, 0, 2 * math.pi)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()
    cr.restore()


def sun_glare(cr, t, start, x=610, y=70, strength=1.0):
    """Hot sun glare from the top corner: a warm bloom, slowly turning soft rays and three flare discs on a line
    toward the frame centre (on 1s, very slow)."""
    if t < start:
        return
    a = strength * clamp01((t - start) / 0.3)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    fx2d_extra._glow(cr, x, y, 420, (1.0, 0.82, 0.5), 0.55 * a)
    fx2d_extra._glow(cr, x, y, 150, (1.0, 0.97, 0.85), 0.8 * a)
    for k in range(9):
        ang = t * 0.05 + k * 2 * math.pi / 9
        cr.move_to(x, y)
        cr.arc(x, y, 900, ang, ang + 0.06)
        cr.close_path()
    g = cairo.RadialGradient(x, y, 0, x, y, 900)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.22 * a)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    cr.set_source(g)
    cr.fill()
    cx, cy = W / 2, H * 0.42
    for k, (u, r, col) in enumerate(((0.45, 38, (1.0, 0.7, 0.5)), (0.7, 22, (0.6, 0.85, 1.0)),
                                     (1.25, 60, (1.0, 0.85, 0.6)))):
        px, py = x + (cx - x) * u, y + (cy - y) * u
        cr.new_path()
        for j in range(6):
            ang = j * math.pi / 3 + 0.3
            (cr.move_to if j == 0 else cr.line_to)(px + r * math.cos(ang), py + r * math.sin(ang))
        cr.close_path()
        cr.set_source_rgba(*col, 0.12 * a)
        cr.fill()
    cr.restore()


def realisation_bg(cr, t, start, end, cx=W / 2, cy=H * 0.42):
    """The realisation background (SU16/IM6): deep navy to indigo, horizontal streaks racing past on 1s, and the
    classic diagonal white flash for the first two frames."""
    if t < start or t > end:
        return
    g = cairo.LinearGradient(0, 0, W * 0.3, H)
    g.add_color_stop_rgb(0, 0.06, 0.08, 0.24)
    g.add_color_stop_rgb(0.55, 0.16, 0.12, 0.42)
    g.add_color_stop_rgb(1, 0.05, 0.06, 0.2)
    cr.set_source(g)
    cr.paint()
    rng = np.random.default_rng(int(round(t * FPS)))
    for _ in range(46):
        yy = rng.uniform(0, H)
        ln = rng.uniform(200, 700)
        xx = rng.uniform(-ln, W)
        th = rng.uniform(1.5, 6)
        cr.move_to(xx, yy)
        cr.curve_to(xx + ln * 0.3, yy - th, xx + ln * 0.7, yy - th, xx + ln, yy)
        cr.curve_to(xx + ln * 0.7, yy + th, xx + ln * 0.3, yy + th, xx, yy)
        cr.set_source_rgba(0.75, 0.82, 1.0, rng.uniform(0.18, 0.5))
        cr.fill()
    if t - start < 2 / FPS:                                       # the "ping": one bright diagonal slash
        cr.move_to(-40, cy + 260)
        cr.line_to(W + 40, cy - 330)
        cr.line_to(W + 40, cy - 300)
        cr.line_to(-40, cy + 300)
        cr.close_path()
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.fill()


def glint(cr, t, start, x, y, size=26, life=0.3):
    """A sparkle on the eye as the thought lands."""
    u = (t - start) / life
    if 0 <= u < 1:
        fx2d_extra._sparkle(cr, x, y, size * math.sin(math.pi * u), (1, 1, 1), 1.0, rot=0.3)


def push(cr, t, start, end, cx=W / 2, cy=H / 2, amount=0.08):
    """A slow 2D push-in on the plate (TP13: <=10% push-ins are done in 2D)."""
    k = 1 + amount * ease_out(clamp01((t - start) / max(end - start, 1e-3)) ** 0.9)
    surf = cr.get_target()
    snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c2 = cairo.Context(snap)
    c2.set_source_surface(surf, 0, 0)
    c2.paint()
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    cr.translate(-cx, -cy)
    cr.set_source_surface(snap, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


def puff(cr, t, start, x, y, size=1.0, seed=0):
    """A tiny, sad "pff" of dust: three small cel puffs (no text)."""
    fx2d.dust_puffs(cr, t, start, x, y, n=3, spread=int(30 * size), size=int(15 * size), dur=0.5, seed=seed)


# ---------------------------------------------------------------- the shots' 2D

def overlays(shot):
    """Shot-local overlays [(fn, kwargs)] for each shot."""
    if shot == "S18":
        a = anchors("S18")
        ex, ey = at(a, 15 / FPS, "eyes")
        return [(comp.backdrop, dict(start=8 / FPS, end=99, fn=realisation_bg, args={})),
                (glint, dict(start=14 / FPS, x=ex + 60, y=ey - 30))]
    if shot == "S19":
        a = anchors("S19")
        tx, ty = at(a, 0.4, "temple")
        ex, ey = at(a, 0.4, "eyes")
        n = max(a)
        return [(sweat_drop, dict(start=0.4, x=tx - 6, y=ty - 10, size=30, slide=22)),
                (push, dict(start=0.0, end=n / FPS, cx=ex, cy=ey, amount=0.08)),
                (sun_glare, dict(start=0.0)),
                (fx2d_extra.ambient, dict(start=0.0, strength=0.8, keep_clear=(ex, ey, 170)))]
    if shot == "S20":
        a = anchors("S20")
        px, py = at(a, 13 / FPS, "tip")
        tx, ty = at(a, 47 / FPS, "temple")
        return [(puff, dict(start=13 / FPS, x=px, y=py, size=1.0)),
                (sweat_drop, dict(start=47 / FPS, x=tx - 4, y=ty - 6, size=34, slide=20))]
    if shot == "S21":
        a = anchors("S21")
        with open(os.path.join(BUILD, "S21_lands.json")) as fh:
            lands = json.load(fh)
        return [(puff, dict(start=(f - 1) / FPS, x=at(a, (f - 1) / FPS, "feet")[0],
                            y=at(a, (f - 1) / FPS, "feet")[1], size=1.3, seed=k)) for k, f in enumerate(lands)]
    return []


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:05d}.png")).convert("RGB") for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 6)
    rows = -(-len(ims) // cols)
    out = Image.new("RGB", (w * cols, h * rows), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path, quality=88)


def run(shot):
    src = comp.Source(os.path.join(BUILD, shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4 = os.path.join(SHOTS_OUT, f"{shot}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, mp4], check=True)
    sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    tags = {s: data.count(s.encode()) for s in ("x264 - core", "Lavf", "Lavc", "encoder")}
    print(f"{shot}: {rep['frames']} frames, 2D {rep['ms_per_frame']:.0f} ms/frame, {mp4} "
          f"({os.path.getsize(mp4) / 1e6:.1f} MB), tags {tags}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
