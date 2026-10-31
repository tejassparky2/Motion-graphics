"""WW2 channel kit, core (1940s poster look): the 1920x1080 canvas, palette, fonts, paper, text, cards, camera and the frame loop.

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
PAL = {                         # 1940s poster inks (STYLE.md): few colours, printed on aged paper
    "paper": "#ecdfc1",       # aged poster paper
    "paper_dk": "#dccba4",
    "ink": "#1c1917",         # key line and solid black
    "ink_soft": "#4f4740",
    "cream": "#f4ead2",       # highlights, light side of faces
    "sea": "#9db3ad",         # grey-green printed sea
    "sea_dk": "#7f9893",
    "land": "#e3d3ad",        # neutral / not at war yet
    "axis": "#45434a",        # Germany (charcoal)
    "axis_it": "#6a6770",     # Italy
    "axis_jp": "#34323a",     # Japan
    "allies": "#2f5f8f",      # Britain, France, the US and the other Western Allies (poster navy-blue)
    "soviet": "#b5322a",      # the Soviet Union (poster red)
    "china": "#d39b2c",       # China (mustard gold)
    "alert": "#c8372d",       # attack arrows' core, explosions
    "fire": "#ec9a2c",
    "snow": "#f6f1e4",
    "white": "#f8f2e2",
    "gold": "#d9a63a",
    "olive": "#6f6a3c",       # uniforms, ground
    "khaki": "#a89566",
    "sky": "#c9c3a8",
}
SIDE = {"axis": PAL["axis"], "germany": PAL["axis"], "italy": PAL["axis_it"], "japan": PAL["axis_jp"],
        "allies": PAL["allies"], "britain": PAL["allies"], "france": PAL["allies"], "usa": PAL["allies"],
        "soviet": PAL["soviet"], "china": PAL["china"], "neutral": PAL["land"]}


def col(name, a=1.0):
    """A palette name, a side name or a #hex, as an (r, g, b, a) tuple."""
    h = PAL.get(name) or SIDE.get(name) or name
    return hexc(h, a)


# ---------------------------------------------------------------- fonts
TITLE = "Anton"                  # big condensed headlines, numbers, the date tag
SLAB = "Alfa Slab One"           # poster headlines and chapter titles (period slab serif)
STENCIL = "Big Shoulders Stencil"  # military labels, map unit names, stamps
LABEL = "Oswald"                 # map labels, name tags, small notes
HAND = LABEL                     # (old name, kept so early modules still import)
UI = "Inter"                     # small print only


def text(cr, s, x, y, size, font=LABEL, color="ink", align="center", bold=True, outline=None, outline_w=0.0,
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


def chapter_card(cr, t, start, number, title, dur=2.6, color="alert"):
    """Full-screen poster chapter title: a red band with rays, 'CHAPTER 2' in stencil, the title in slab serif."""
    u_in, u_out = ease_out(seg(t, start, start + 0.35)), ease_in(seg(t, start + dur - 0.3, start + dur))
    if u_in <= 0 or u_out >= 1:
        return
    a = 1 - u_out
    cr.save()
    cr.rectangle(0, H / 2 - 170 * u_in, W, 340 * u_in)
    cr.clip()
    cr.set_source_rgba(*col(color, a))
    cr.paint()
    rays(cr, t, W / 2, H / 2, n=28, color="ink", alpha=0.10 * a, spin=0.02)
    halftone(cr, lambda c: c.rectangle(0, H / 2 + 60, W, 120), "ink", density=2, alpha=0.25 * a)
    cr.restore()
    text(cr, f"CHAPTER {number}", W / 2, H / 2 - 62, 52, font=STENCIL, color="cream", alpha=a * u_in, spacing=8)
    text(cr, title.upper(), W / 2, H / 2 + 70, 112, font=SLAB, color="cream", bold=False, alpha=a * u_in,
         outline="ink", outline_w=10, spacing=2)


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
    text(cr, word, 0, size * 0.35, size, font=SLAB, color=color, bold=False, alpha=fade * min(1, u * 2),
         outline="paper", outline_w=size * 0.10, spacing=3)
    cr.restore()


def counter(cr, t, start, end, value, x, y, size=110, fmt="{:,.0f}", color="ink", label=None):
    """A number that counts up from 0 to `value` between start and end (eased), with an optional label under it."""
    if t < start:
        return
    v = value * ease_out(seg(t, start, end))
    text(cr, fmt.format(v), x, y, size, font=TITLE, color=color, bold=False, outline="paper", outline_w=size * 0.08)
    if label:
        text(cr, label, x, y + size * 0.48, size * 0.3, font=LABEL, color="ink_soft")


# ---------------------------------------------------------------- poster print tools
_DOTS = {}


def _dot_tile(density, cell=12, angle=0.785):
    """An alpha tile of round halftone dots (density 1..5 = dot size), rotated 45 degrees like a print screen."""
    key = (density, cell, angle)
    if key in _DOTS:
        return _DOTS[key]
    n = 48 * cell // 12 * 4
    surf = cairo.ImageSurface(cairo.FORMAT_A8, n, n)
    c = cairo.Context(surf)
    r = cell * (0.16 + 0.085 * density)
    c.set_source_rgba(0, 0, 0, 1)
    for i in range(-2, n // cell + 3):
        for j in range(-2, n // cell + 3):
            c.arc(i * cell + (cell / 2 if j % 2 else 0), j * cell * 0.866, r, 0, 2 * math.pi)
            c.fill()
    pat = cairo.SurfacePattern(surf)
    pat.set_extend(cairo.EXTEND_REPEAT)
    m = cairo.Matrix()
    m.rotate(angle)
    pat.set_matrix(m)
    _DOTS[key] = pat
    return pat


def halftone(cr, path, color="ink", density=3, alpha=1.0, cell=12):
    """Fill the area traced by path(cr) with halftone dots (the printed shadow / mid-tone of the poster look)."""
    cr.save()
    path(cr)
    cr.clip()
    cr.set_source_rgba(*col(color, alpha))
    cr.mask(_dot_tile(max(1, min(5, int(density))), cell))
    cr.restore()


def rays(cr, t, cx, cy, n=24, color="ink", alpha=0.12, spin=0.03, r=2600):
    """Poster sunburst: alternating wedges radiating from (cx, cy), turning slowly."""
    cr.save()
    cr.set_source_rgba(*col(color, alpha))
    a0 = t * spin
    for k in range(n):
        a = a0 + k * 2 * math.pi / n
        cr.move_to(cx, cy)
        cr.arc(cx, cy, r, a, a + math.pi / n)
        cr.close_path()
    cr.fill()
    cr.restore()


_FINISH = {}


def print_finish(cr, t=0.0, strength=1.0):
    """Last call of every frame: printed-paper grain, specks and a slight ink-wear, multiplied over the frame."""
    if "s" not in _FINISH:
        import numpy as np
        cache = os.path.join(ROOT, "build", "ww2", "finish.png")
        if os.path.exists(cache):
            _FINISH["s"] = cairo.ImageSurface.create_from_png(cache)
        else:
            rng = np.random.default_rng(11)
            g = 255 - np.abs(rng.normal(0, 9, (H, W))).astype(np.float32)          # grain
            sp = rng.random((H, W)) < 0.0009
            g[sp] -= rng.uniform(30, 90, sp.sum())                                     # ink specks
            lines = rng.random((H, 1)) < 0.004
            g -= np.where(lines, 6.0, 0.0)                                             # faint press streaks
            g = np.clip(g, 0, 255).astype(np.uint8)
            argb = np.dstack([g, g, g, np.full_like(g, 255)])
            surf = cairo.ImageSurface.create_for_data(bytearray(argb.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            surf.write_to_png(cache)
            _FINISH["s"] = surf
    cr.save()
    cr.identity_matrix()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    dx = (int(t * FPS) * 37) % 9 - 4                     # the grain shifts a little each frame, like film/print
    cr.set_source_surface(_FINISH["s"], dx, 0)
    cr.paint_with_alpha(strength)
    cr.restore()


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
           "-bsf:v", "filter_units=remove_types=6", "-movflags", "+faststart", out_mp4 + ".enc.mp4"]
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
    # a stream-copy remux drops the "Lavc libx264" encoder name the first pass leaves in the track header
    subprocess.run([ffmpeg(), "-y", "-v", "error", "-i", out_mp4 + ".enc.mp4", "-c", "copy", "-map_metadata", "-1",
                    "-fflags", "+bitexact", "-flags:v", "+bitexact", "-metadata:s:v", "handler_name=",
                    "-movflags", "+faststart", out_mp4], check=True)
    os.remove(out_mp4 + ".enc.mp4")
    return out_mp4
