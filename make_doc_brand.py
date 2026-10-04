#!/usr/bin/env python3
"""Brand kit for the doctor channel ("Body Facts" series), in the videos' clean style.

  python make_doc_brand.py                 # name from NAME below
  python make_doc_brand.py --name "Doc & The Organs"

Writes out/doc_brand/:
  avatar.png     800x800 profile picture (YouTube crops it to a circle; everything sits inside it)
  banner.png     2560x1440 channel banner; the text sits inside the 1546x423 area every device shows
  lockup.png     mascot + name on transparent, 2000x700 (for thumbnails, end screens, watermark)
  watermark.png  150x150 video watermark (YouTube Studio > Customization > Branding)
  preview.png    how the avatar and banner look at real sizes
"""
import argparse
import math
import os

from motion import engine
from motion.engine import INK, WHITE, at, blob, cairo, hexc, line, rrect_pts, shape

NAME = "Organ ER"
TAGLINE = "Your organs argue. The doctor explains."
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "doc_brand")

SKY, SKY_D = hexc("#86cfdc"), hexc("#5fb3c4")
MASK = hexc("#2fa36f")
RED = hexc("#d8363a")


def cross(cr, x, y, r, col=WHITE):
    w = r * 0.62
    shape(cr, rrect_pts(x - w / 2, y - r, w, 2 * r, w * 0.25, 20), col, seed=1, amp=0, lw=0, stroke=None)
    shape(cr, rrect_pts(x - r, y - w / 2, 2 * r, w, w * 0.25, 20), col, seed=2, amp=0, lw=0, stroke=None)


def mascot(cr, t=0.0):
    """The channel mascot: the heart, with a surgical mask and a head mirror (it's the ER's doctor-in-chief)."""
    from videos.kidney_donor import grad_fill, eyes
    pts = []
    for k in range(80):
        a = k / 80 * 2 * math.pi
        pts.append((16 * math.sin(a) ** 3 * 13, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a)
                                                 - math.cos(4 * a)) * 13))
    grad_fill(cr, pts, hexc("#ff6b6b"), hexc("#b5222a"), 0, 0, 240, lw=9)
    blob(cr, -90, -110, 46, 26, hexc("#ffffff", 0.35), seed=3, amp=0, lw=0, stroke=None)
    eyes(cr, 0, -40, 2.4, "happy")
    # surgical mask
    line(cr, [(-118, 30), (-200, -10)], 7, hexc("#1f6f50"), seed=4, amp=0)
    line(cr, [(118, 30), (200, -10)], 7, hexc("#1f6f50"), seed=5, amp=0)
    shape(cr, [(-120, 20), (120, 20), (112, 92), (60, 128), (-60, 128), (-112, 92)], MASK, seed=6, amp=0, lw=8)
    for k in range(3):
        line(cr, [(-100, 46 + 24 * k), (100, 46 + 24 * k)], 5, hexc("#1f7f55"), seed=7 + k, amp=0)
    # head mirror
    line(cr, [(-150, -170), (150, -170)], 14, hexc("#3a3d45"), seed=10, amp=0)
    blob(cr, 0, -205, 56, 56, hexc("#e8edf2"), seed=11, amp=0, lw=8)
    blob(cr, 0, -205, 22, 22, hexc("#3a3d45"), seed=12, amp=0, lw=0, stroke=None)
    blob(cr, -18, -222, 12, 8, WHITE, seed=13, amp=0, lw=0, stroke=None)


def avatar(cr, size=800):
    cr.save()
    cr.scale(size / 800, size / 800)
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(10):   # soft drape folds
        line(cr, [(-50, 80 * k), (300, 80 * k + 30), (850, 80 * k - 10)], 6, hexc("#7cc3d1"), seed=20 + k, amp=0)
    blob(cr, 400, 400, 330, 330, hexc("#ffffff", 0.35), seed=30, amp=0, lw=0, stroke=None)
    cross(cr, 400, 400, 270, hexc("#ffffff", 0.9))
    with at(cr, 400, 455, 0.92):
        mascot(cr)
    cr.restore()


def name_text(cr, x, y, size, color=INK, halo=WHITE):
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    words = NAME.split()
    # last word in red if it's short (e.g. "ER"), the rest in ink
    runs = [(" ".join(words[:-1]) + " ", color), (words[-1], RED)] if len(words) > 1 and len(words[-1]) <= 3 else [(NAME, color)]
    total = sum(cr.text_extents(s).x_advance for s, _ in runs)
    cx = x - total / 2
    for s, col in runs:
        cr.move_to(cx, y)
        cr.text_path(s)
        cr.set_source_rgba(*halo)
        cr.set_line_width(size * 0.24)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
        cr.set_source_rgba(*col)
        cr.fill()
        cx += cr.text_extents(s).x_advance
    return total


def cast_row(cr, y, scale, t=0.0):
    """The channel's characters in a row: brain, kidney, liver, tooth, eye, toe."""
    from motion.organs import big_lobe_pts, brain, lobe
    from videos.kidney_donor import kidney
    from videos.toe_thumb import toe_char
    from videos.tooth_eye import eyeball, tooth
    items = [
        (lambda x: brain(cr, t, x, y, 0.62 * scale, "happy")),
        (lambda x: kidney(cr, t, x, y + 10, 0.8 * scale, 1, "happy")),
        (lambda x: lobe(cr, t, big_lobe_pts(x + 30 * scale, y, 0.62 * scale), x - 10 * scale, y - 20 * scale, 0.7 * scale,
                        "happy")),
        (lambda x: tooth(cr, t, x, y + 20 * scale, 0.75 * scale, "happy")),
        (lambda x: eyeball(cr, t, x, y, 0.38 * scale, "happy", cloudy=0.0)),
        (lambda x: toe_char(cr, t, x, y, 0.95 * scale, mood="happy")),
    ]
    return items


def banner(cr):
    W, H = 2560, 1440
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(14):
        line(cr, [(-100, 110 * k), (900, 110 * k + 40), (1800, 110 * k - 20), (2700, 110 * k + 30)], 8, hexc("#7cc3d1"),
             seed=40 + k, amp=0)
    # safe area (1546x423, centred): mascot left, name and tagline right; characters along the bottom edge of it
    sx = (W - 1546) / 2
    cross(cr, sx + 190, H / 2, 190, hexc("#ffffff", 0.9))
    with at(cr, sx + 190, H / 2 + 30, 0.62):
        mascot(cr)
    name_text(cr, sx + 870, H / 2 + 20, 190)
    cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(62)
    tw = cr.text_extents(TAGLINE).x_advance
    with at(cr, sx + 870, H / 2 + 120, 1.0):
        shape(cr, rrect_pts(-tw / 2 - 30, -56, tw + 60, 84, 16, 20), WHITE, seed=50, amp=0, lw=5)
        cr.move_to(-tw / 2, 6)
        cr.set_source_rgba(*INK)
        cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(62)
        cr.show_text(TAGLINE)
    # the cast, outside the text area (visible on TV/desktop; trimmed on phones, which is fine)
    items = cast_row(cr, 0, 1.0)
    xs = [300, 700, 1100, 1460, 1860, 2260]
    for x, draw in zip(xs, items):
        cr.save()
        cr.translate(0, H / 2 + 420)
        draw(x)
        cr.restore()


def lockup(cr):
    with at(cr, 330, 360, 0.95):
        mascot(cr)
    name_text(cr, 1240, 420, 300, halo=hexc("#ffffff", 0.0))


def main():
    global NAME
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=NAME)
    NAME = ap.parse_args().name
    engine.set_style("clean")
    os.makedirs(OUT, exist_ok=True)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    avatar(cairo.Context(s))
    s.write_to_png(os.path.join(OUT, "avatar.png"))
    w = cairo.ImageSurface(cairo.FORMAT_ARGB32, 150, 150)
    c = cairo.Context(w)
    c.arc(75, 75, 75, 0, 2 * math.pi)
    c.clip()
    avatar(c, 150)
    w.write_to_png(os.path.join(OUT, "watermark.png"))
    b = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2560, 1440)
    banner(cairo.Context(b))
    b.write_to_png(os.path.join(OUT, "banner.png"))
    lk = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2000, 700)
    lockup(cairo.Context(lk))
    lk.write_to_png(os.path.join(OUT, "lockup.png"))
    # preview: banner as a phone sees it (safe area), and the avatar as a circle at 176 px and 48 px
    p = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1600, 700)
    c = cairo.Context(p)
    c.set_source_rgb(0.97, 0.97, 0.97)
    c.paint()
    c.save()
    c.translate(20, 20)
    c.scale(1546 / 2560 * 0.98, 1546 / 2560 * 0.98)
    c.set_source_surface(b, 0, 0)
    c.paint()
    c.restore()
    for (x, y, d) in ((80, 480, 176), (300, 540, 48)):
        c.save()
        c.arc(x + d / 2, y + d / 2, d / 2, 0, 2 * math.pi)
        c.clip()
        c.translate(x, y)
        c.scale(d / 800, d / 800)
        c.set_source_surface(s, 0, 0)
        c.paint()
        c.restore()
    c.set_source_rgb(0.1, 0.1, 0.1)
    c.select_font_face("Anton")
    c.set_font_size(40)
    c.move_to(380, 580)
    c.show_text(NAME)
    p.write_to_png(os.path.join(OUT, "preview.png"))
    print(f"wrote {OUT}/ (avatar, banner, lockup, watermark, preview) for {NAME!r}")


if __name__ == "__main__":
    main()
