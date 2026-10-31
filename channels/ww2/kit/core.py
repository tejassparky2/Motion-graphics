"""WW2 channel kit, core: the 1920x1080 canvas, palette, fonts, paper, text, cards, camera and the frame loop.

Every chapter and every helper module (maps.py, stick.py, props.py) draws through these, so the whole video shares
one look. Style rules: channels/ww2/STYLE.md.

    from channels.ww2.kit.core import *          # W, H, FPS, PAL, SIDE, paper(), text(), camera(), render_clip()
"""
import math
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from motion.engine import (back_out, cairo, clamp01, ease_in, ease_out, hexc, lerp, seg,  # noqa: E402,F401
                           smooth, wobble)

W, H, FPS = 1920, 1080, 24

# ---------------------------------------------------------------- palette (STYLE.md)
PAL = {
    "paper": "#efe6d2",       # parchment background
    "paper_dk": "#e2d6bb",
    "ink": "#1f1c1a",         # every outline and stick figure
    "ink_soft": "#5b544c",    # secondary lines, labels
    "sea": "#b8cfd3",
    "sea_dk": "#9fbcc2",
    "land": "#ddd2b6",        # neutral / not in the war yet
    "axis": "#4b4b52",        # Germany (charcoal)
    "axis_it": "#6c6c72",     # Italy (lighter charcoal)
    "axis_jp": "#3a3a42",     # Japan (darker charcoal)
    "allies": "#3f6fb5",      # Britain, France, the US and the other Western Allies (blue)
    "soviet": "#b8382e",      # the Soviet Union (red)
    "china": "#cf9f2a",       # China (gold)
    "alert": "#d8452f",       # arrows of attack, explosions' core
    "fire": "#f2a33a",
    "snow": "#f7f5ef",
    "white": "#fbf8ef",
    "gold": "#e0b84a",
}
SIDE = {"axis": PAL["axis"], "germany": PAL["axis"], "italy": PAL["axis_it"], "japan": PAL["axis_jp"],
        "allies": PAL["allies"], "britain": PAL["allies"], "france": PAL["allies"], "usa": PAL["allies"],
        "soviet": PAL["soviet"], "china": PAL["china"], "neutral": PAL["land"]}


def col(name, a=1.0):
    """A palette name, a side name or a #hex, as an (r, g, b, a) tuple."""
    h = PAL.get(name) or SIDE.get(name) or name
    return hexc(h, a)


# ---------------------------------------------------------------- fonts
TITLE = "Anton"           # chapter cards, big numbers, stamps (condensed, documentary)
HAND = "Kalam"            # map labels, notes (hand-lettered sketchbook)
UI = "Inter"              # small captions, sources


def text(cr, s, x, y, size, font=HAND, color="ink", align="center", bold=True, outline=None, outline_w=0.0,
         alpha=1.0, spacing=0.0):
    """One line of text; (x, y) is the baseline point given by align ("left", "center", "right")."""
    cr.save()
    cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    ext = cr.text_extents(s)
    width = ext.x_advance + spacing * max(0, len(s) - 1)
    x0 = x - (width / 2 if align == "center" else width if align == "right" else 0)
    if spacing:
        cx = x0
        for ch in s:
            cr.move_to(cx, y)
            cr.text_path(ch)
            cx += cr.text_extents(ch).x_advance + spacing
    else:
        cr.move_to(x0, y)
        cr.text_path(s)
    if outline:
        cr.set_source_rgba(*col(outline, alpha))
        cr.set_line_width(outline_w or size * 0.12)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
    cr.set_source_rgba(*col(color, alpha))
    cr.fill()
    cr.restore()
    return width


# ---------------------------------------------------------------- paper background
_PAPER = {}


def paper_surface(w=W, h=H, seed=7):
    """The parchment page: warm base, soft fibre noise, faint blotches and a vignette (made once, cached)."""
    key = (w, h, seed)
    if key in _PAPER:
        return _PAPER[key]
    cache = os.path.join(ROOT, "build", "ww2", f"paper_{w}x{h}_{seed}.png")
    if os.path.exists(cache):
        surf = cairo.ImageSurface.create_from_png(cache)
        _PAPER[key] = surf
        return surf
    import numpy as np
    rng = np.random.default_rng(seed)
    base = np.array([int(PAL["paper"][i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    img = np.ones((h, w, 3), np.float32) * base
    small = rng.normal(0, 1, (h // 8 + 1, w // 8 + 1)).astype(np.float32)
    for axis in (0, 1):                                                 # soft blotches: box-blurred coarse noise
        c = np.cumsum(np.pad(small, [(2, 2) if a == axis else (0, 0) for a in (0, 1)], mode="edge"), axis=axis)
        small = (np.take(c, range(4, c.shape[axis]), axis=axis) - np.take(c, range(0, c.shape[axis] - 4), axis=axis)) / 4
    blot = np.kron(small, np.ones((8, 8), np.float32))[:h, :w]
    img[:blot.shape[0], :blot.shape[1]] += blot[..., None] * 6.0
    img += rng.normal(0, 3.2, (h, w, 1)).astype(np.float32)           # grain
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - 0.16 * np.clip(d - 0.55, 0, 1) ** 1.6)[..., None]       # vignette
    img = np.clip(img, 0, 255).astype(np.uint8)
    argb = np.zeros((h, w, 4), np.uint8)
    argb[..., 0], argb[..., 1], argb[..., 2], argb[..., 3] = img[..., 2], img[..., 1], img[..., 0], 255
    surf = cairo.ImageSurface.create_for_data(bytearray(argb.tobytes()), cairo.FORMAT_ARGB32, w, h, w * 4)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    surf.write_to_png(cache)
    _PAPER[key] = surf
    return surf


def paper(cr):
    cr.set_source_surface(paper_surface(), 0, 0)
    cr.paint()


# ---------------------------------------------------------------- camera
def camera(cr, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0):
    """Look at world point (cx, cy) at `zoom`; call inside cr.save()/restore()."""
    cr.translate(W / 2, H / 2)
    if rot:
        cr.rotate(rot)
    cr.scale(zoom, zoom)
    cr.translate(-cx, -cy)


def push_in(t, start, end, z0=1.0, z1=1.06):
    """The slow push-in every shot carries (channel rule): zoom from z0 to z1 over the shot."""
    return lerp(z0, z1, smooth(seg(t, start, end)))


def shake(t, start, dur=0.35, amp=14.0, seed=1):
    """Screen shake offset (dx, dy) for an impact at `start`."""
    u = seg(t, start, start + dur)
    if u <= 0 or u >= 1:
        return 0.0, 0.0
    r = random.Random(int(t * FPS) * 31 + seed)
    k = amp * (1 - u) ** 2
    return r.uniform(-k, k), r.uniform(-k, k)


# ---------------------------------------------------------------- cards and stamps
def date_stamp(cr, t, label, start=0.0, x=70, y=86):
    """The corner date tag ("SEPT 1939"), on screen through every scene; pops in at `start`."""
    u = back_out(seg(t, start, start + 0.3)) if t >= start else 0
    if u <= 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(u, u)
    cr.select_font_face(TITLE)
    cr.set_font_size(40)
    w = cr.text_extents(label).x_advance + 1.5 * (len(label) - 1)
    cr.rectangle(-14, -46, w + 28, 60)
    cr.set_source_rgba(*col("ink", 0.88))
    cr.fill()
    text(cr, label, 0, 0, 40, font=TITLE, color="paper", align="left", bold=False, spacing=1.5)
    cr.restore()


def chapter_card(cr, t, start, number, title, dur=2.6):
    """Full-screen chapter title: 'CHAPTER 2' small, the title big, wiping in and out."""
    u_in, u_out = ease_out(seg(t, start, start + 0.35)), ease_in(seg(t, start + dur - 0.3, start + dur))
    if u_in <= 0 or u_out >= 1:
        return
    cr.save()
    cr.set_source_rgba(*col("ink", 0.94 * (1 - u_out)))
    cr.rectangle(0, H / 2 - 150 * u_in, W, 300 * u_in)
    cr.fill()
    a = u_in * (1 - u_out)
    text(cr, f"CHAPTER {number}", W / 2, H / 2 - 52, 44, font=TITLE, color="gold", bold=False, alpha=a, spacing=6)
    text(cr, title.upper(), W / 2, H / 2 + 62, 110, font=TITLE, color="paper", bold=False, alpha=a, spacing=2)
    cr.restore()


def word_card(cr, t, start, word, dur=1.4, y=H * 0.2, size=120, color="ink", tilt=-0.04):
    """A big stamped word ('BLITZKRIEG', 'PHONEY WAR') that slams in with a little overshoot."""
    if not (start <= t <= start + dur):
        return
    u = back_out(seg(t, start, start + 0.22))
    fade = 1 - ease_in(seg(t, start + dur - 0.25, start + dur))
    cr.save()
    cr.translate(W / 2, y)
    cr.rotate(tilt)
    cr.scale(1.6 - 0.6 * u, 1.6 - 0.6 * u)
    text(cr, word, 0, size * 0.35, size, font=TITLE, color=color, bold=False, alpha=fade * min(1, u * 2),
         outline="paper", outline_w=size * 0.10, spacing=3)
    cr.restore()


def counter(cr, t, start, end, value, x, y, size=110, fmt="{:,.0f}", color="ink", label=None):
    """A number that counts up from 0 to `value` between start and end (eased), with an optional label under it."""
    if t < start:
        return
    v = value * ease_out(seg(t, start, end))
    text(cr, fmt.format(v), x, y, size, font=TITLE, color=color, bold=False, outline="paper", outline_w=size * 0.08)
    if label:
        text(cr, label, x, y + size * 0.48, size * 0.3, font=HAND, color="ink_soft")


# ---------------------------------------------------------------- frame loop
def ffmpeg():
    py = os.path.join("/home/user/.venv-main/bin/python")
    return subprocess.check_output([py, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                                   text=True).strip()


def render_clip(draw, dur, out_mp4, frames=None, still=None, crf=12):
    """Render draw(cr, t) for `dur` seconds to out_mp4 (or one frame at time `still` to a .png when still is set).
    frames: optional (first, last) frame range for split renders. Output carries no metadata or encoder tags."""
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)), exist_ok=True)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if still is not None:
        cr = cairo.Context(surf)
        draw(cr, still)
        surf.write_to_png(out_mp4)
        return out_mp4
    n = int(round(dur * FPS))
    a, b = frames or (0, n - 1)
    cmd = [ffmpeg(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-crf", str(crf), "-preset", "medium", "-pix_fmt", "yuv420p",
           "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
           "-bsf:v", "filter_units=remove_types=6", "-movflags", "+faststart", out_mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(a, b + 1):
        cr = cairo.Context(surf)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        draw(cr, i / FPS)
        surf.flush()
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    p.wait()
    return out_mp4
