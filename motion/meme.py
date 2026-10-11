"""Meme Shorts kit: the white top caption bar, rooms and props for the 6-9 second meme format.

The format (owner, 11 Oct 2026): readable in one second, the joke lands as a reaction, almost no talking, our own
characters and sounds only. Every meme loops: its last frame cuts back to the setup.
"""
import math

from .engine import W, H, cue, ease_out, hexc, seg
from .polish import (OUTLINE, WHITE, alpha, appear, bold_text, lin, paint, rad, rrect, smooth, soft_disc, soft_rrect,
                     sprite, put, stroke_line, text_width)

INK = hexc("#1b1b1f")


def meme_bar(cr, t, start, lines, y=40, size=68, h=None):
    """The classic meme caption: a white panel across the top with bold black text, popping in at `start`."""
    if t < start:
        return
    k = 0.85 + 0.15 * ease_out(seg(t, start, start + 0.12))
    n = len(lines)
    h = h or (size * 1.25 * n + 44)
    cr.save()
    cr.translate(W / 2, y + h / 2)
    cr.scale(k, k)
    soft_rrect(cr, -W / 2 + 24, -h / 2 + 8, W - 48, h, 22, (0, 0, 0, 0.35), sigma=10)
    rrect(cr, -W / 2 + 20, -h / 2, W - 40, h, 22)
    paint(cr, WHITE, OUTLINE, 5)
    y0 = -h / 2 + 22 + size * 0.95
    for ln in lines:
        tw = text_width(cr, ln, size, "Fredoka")
        sz = size * min(1.0, (W - 90) / max(tw, 1))
        bold_text(cr, ln, 0, y0, sz, INK, font="Fredoka", outline=None, shadow=0)
        y0 += size * 1.25
    cr.restore()
    cue("pop", t, start)


# ---------------------------------------------------------------- rooms (cached)
def _living(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 860, [(0, hexc("#f6d9b0")), (1, hexc("#f0c890"))]))
    c.fill()
    for x in range(0, W, 80):           # wallpaper stripes
        c.rectangle(x, 0, 40, 860)
        c.set_source_rgba(1, 1, 1, 0.12)
        c.fill()
    rrect(c, 430, 250, 220, 160, 10)     # a family photo
    paint(c, hexc("#8a5a2b"), OUTLINE, 5)
    rrect(c, 446, 266, 188, 128, 6)
    paint(c, lin(0, 266, 0, 394, [(0, hexc("#9fd6ff")), (1, hexc("#cdeccd"))]), OUTLINE, 3)
    c.rectangle(0, 860, W, H - 860)
    c.set_source(lin(0, 860, 0, H, [(0, hexc("#b77a48")), (1, hexc("#7a4a2a"))]))
    c.fill()


def living_room(cr):
    put(cr, sprite("meme_living", W, H, _living), 0, 0)


def sofa(cr, x, y, s=1.0, cushion_lift=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, 10, 300, (0, 0, 0, 0.18))
    rrect(cr, -280, -250, 560, 170, 40)                 # back
    paint(cr, lin(0, -250, 0, -80, [(0, hexc("#d8534a")), (1, hexc("#a8302a"))]), OUTLINE, 6)
    rrect(cr, -280, -110, 560, 110, 30)                 # base
    paint(cr, lin(0, -110, 0, 0, [(0, hexc("#c8403a")), (1, hexc("#8a2a24"))]), OUTLINE, 6)
    for side in (-1, 1):                                # arms
        rrect(cr, side * 280 - 45, -170, 90, 170, 34)
        paint(cr, hexc("#b8362f"), OUTLINE, 6)
    for k in (-1, 1):                                   # cushions
        lift = cushion_lift if k == 1 else 0.0
        cr.save()
        cr.translate(k * 120, -110 - lift * 160)
        cr.rotate(lift * 0.5)
        rrect(cr, -115, -40, 230, 60, 22)
        paint(cr, lin(0, -40, 0, 20, [(0, hexc("#ef7a6a")), (1, hexc("#c8403a"))]), OUTLINE, 5)
        cr.restore()
    for k in (-1, 1):
        rrect(cr, k * 230 - 12, 0, 24, 30, 6)
        paint(cr, hexc("#5a3a24"), OUTLINE, 4)
    cr.restore()


def report_card(cr, x, y, s=1.0, rot=0.0, text="95/100"):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_rrect(cr, -120, -110, 240, 230, 10, (0, 0, 0, 0.3), sigma=8)
    rrect(cr, -120, -120, 240, 230, 10)
    paint(cr, WHITE, OUTLINE, 5)
    for k in range(3):
        stroke_line(cr, [(-90, -90 + k * 22), (90, -90 + k * 22)], 4, alpha(OUTLINE, 0.3), curve=False)
    bold_text(cr, text, 0, 50, 46, hexc("#e8473f"), font="Fredoka", outline=None, shadow=0)
    cr.save()
    cr.translate(0, 34)
    cr.scale(1.5, 1)
    cr.arc(0, 0, 66, 0, 2 * math.pi)
    cr.restore()
    cr.set_line_width(5)
    cr.set_source_rgba(*hexc("#e8473f"))
    cr.stroke()
    cr.restore()


def torch(cr, hx, hy, beam=True):
    """A torch in the hand at (hx, hy), pointing right, with its light cone."""
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(0.35)
    if beam:
        cr.move_to(40, -10)
        cr.line_to(330, -110)
        cr.line_to(330, 110)
        cr.line_to(40, 10)
        cr.close_path()
        cr.set_source(lin(40, 0, 330, 0, [(0, (1, 0.97, 0.6, 0.6)), (1, (1, 0.97, 0.6, 0.0))]))
        cr.fill()
    rrect(cr, -30, -14, 70, 28, 10)
    paint(cr, hexc("#3a3e48"), OUTLINE, 4)
    rrect(cr, 34, -20, 18, 40, 6)
    paint(cr, hexc("#ffe680"), OUTLINE, 4)
    cr.restore()


def magnifier(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    stroke_line(cr, [(30, 30), (90, 90)], 18, hexc("#5a3a24"), curve=False)
    cr.arc(0, 0, 48, 0, 2 * math.pi)
    paint(cr, (0.85, 0.95, 1.0, 0.45), OUTLINE, 8)
    stroke_line(cr, [(-26, -14), (-10, -30)], 6, (1, 1, 1, 0.8))
    cr.restore()


def _garden(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 760, [(0, hexc("#141a34")), (1, hexc("#2e3a66"))]))
    c.fill()
    for k in range(50):
        c.arc((k * 131) % W, (k * 71) % 520, 1.2 + (k % 3) * 0.6, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.5)
        c.fill()
    c.arc(580, 210, 50, 0, 2 * math.pi)                 # moon
    paint(c, hexc("#fff4c8"), None, 0)
    rrect(c, 30, 300, 300, 460, 10)                     # the house wall + lit window
    paint(c, hexc("#5a4a6a"), OUTLINE, 5)
    rrect(c, 90, 380, 180, 150, 8)
    paint(c, lin(0, 380, 0, 530, [(0, hexc("#ffe7a0")), (1, hexc("#ffc860"))]), OUTLINE, 5)
    c.rectangle(0, 760, W, H - 760)
    c.set_source(lin(0, 760, 0, H, [(0, hexc("#3e6a3a")), (1, hexc("#1e3a1e"))]))
    c.fill()


def garden(cr):
    put(cr, sprite("meme_garden", W, H, _garden), 0, 0)


def hole(cr, x, y, w=120):
    smooth(cr, [(x - w / 2, y), (x - w / 3, y - 22), (x + w / 3, y - 22), (x + w / 2, y), (x + w / 3, y + 24),
                (x - w / 3, y + 24)])
    paint(cr, hexc("#2a1a10"), OUTLINE, 4)
    for k in (-1, 1):                                   # dirt piles
        smooth(cr, [(x + k * w * 0.75 - 40, y + 4), (x + k * w * 0.75, y - 36), (x + k * w * 0.75 + 40, y + 4)])
        paint(cr, hexc("#7a5030"), OUTLINE, 4)


def metal_detector(cr, hx, hy, t):
    cr.save()
    cr.translate(hx, hy)
    sway = 0.25 * math.sin(t * 6)
    cr.rotate(0.9 + sway)
    stroke_line(cr, [(0, 0), (0, 220)], 10, hexc("#9aa0ac"), curve=False)
    cr.save()
    cr.translate(0, 230)
    cr.scale(1, 0.4)
    cr.arc(0, 0, 50, 0, 2 * math.pi)
    paint(cr, hexc("#3a3e48"), OUTLINE, 10)
    cr.restore()
    cr.restore()


# ---------------------------------------------------------------- school
def _class_wall(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 860, [(0, hexc("#cfe6dc")), (1, hexc("#e8f2ea"))]))
    c.fill()
    rrect(c, 40, 220, 640, 420, 18)
    paint(c, hexc("#a8743e"), OUTLINE, 6)
    rrect(c, 62, 242, 596, 376, 8)
    paint(c, rad(330, 400, 480, [(0, hexc("#3e7a5a")), (1, hexc("#22503a"))]), OUTLINE, 4)
    c.rectangle(0, 860, W, H - 860)
    c.set_source(lin(0, 860, 0, H, [(0, hexc("#d9a46a")), (1, hexc("#a8713e"))]))
    c.fill()


def class_wall(cr):
    put(cr, sprite("meme_classwall", W, H, _class_wall), 0, 0)


def exam_paper(cr, x, y, s=1.0, rot=0.0, rows=(), title="FINAL EXAM"):
    """An exam sheet; `rows` = [(text, alpha)] question lines."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_rrect(cr, -250, -320, 500, 660, 12, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -250, -330, 500, 660, 12)
    paint(cr, lin(0, -330, 0, 330, [(0, WHITE), (1, hexc("#f1ece2"))]), OUTLINE, 6)
    bold_text(cr, title, 0, -260, 46, INK, font="Fredoka", outline=None, shadow=0)
    stroke_line(cr, [(-200, -236), (200, -236)], 4, OUTLINE, curve=False)
    yy = -170
    for text, a in rows:
        if a > 0.01:
            cr.save()
            cr.translate(-210, yy)
            cr.scale(0.6 + 0.4 * a, 0.6 + 0.4 * a)
            bold_text(cr, text, 0, 0, 50, alpha(hexc("#c8302a") if "BONUS" in text else INK, a), font="Fredoka",
                      outline=None, shadow=0, align="left")
            cr.restore()
        yy += 92
    cr.restore()


def soul(cr, t, x, y, s, u, who="kid"):
    """The kid's ghost floating up out of his body (u: 0 -> 1) and waving goodbye."""
    from .toons import person
    if u <= 0.01:
        return
    cr.push_group()
    person(cr, t, x, y - 420 * ease_out(u), s, who, eyes="happy", mouth="smile", arms=("wave", "down"),
           shadow=False)
    pat = cr.pop_group()
    a = min(1.0, u * 3)
    cr.set_source(pat)
    cr.paint_with_alpha(0.3 * a)
    cr.set_source_rgba(0.88, 0.95, 1.0, 0.55 * a)
    cr.mask(pat)


# ---------------------------------------------------------------- bedroom
def _bedroom(c, dark):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#1a1e3a") if dark else hexc("#9fb8e8")),
                                  (1, hexc("#0e1024") if dark else hexc("#6a7ab8"))]))
    c.fill()
    rrect(c, 420, 180, 240, 280, 12)                    # window
    paint(c, lin(0, 180, 0, 460, [(0, hexc("#0c1030")), (1, hexc("#2a3060"))]), OUTLINE, 6)
    c.rectangle(536, 180, 8, 280)
    c.rectangle(420, 316, 240, 8)
    c.set_source_rgba(*hexc("#c8b8a0"))
    c.fill()
    c.arc(600, 240, 24, 0, 2 * math.pi)
    paint(c, hexc("#fff4c8"), None, 0)


def bedroom(cr, dark=False):
    put(cr, sprite(("meme_bedroom", dark), W, H, lambda c: _bedroom(c, dark)), 0, 0)


def bed(cr, x, y, blanket=hexc("#4aa3f0")):
    rrect(cr, x - 330, y - 220, 70, 300, 20)            # headboard
    paint(cr, hexc("#8a5a2b"), OUTLINE, 6)
    rrect(cr, x - 300, y - 150, 300, 90, 40)            # pillow
    paint(cr, WHITE, OUTLINE, 5)


def blanket(cr, x, y, col=hexc("#4aa3f0")):
    smooth(cr, [(x - 300, y - 90), (x - 120, y - 120), (x + 120, y - 110), (x + 330, y - 80), (x + 330, y + 90),
                (x - 300, y + 90)])
    paint(cr, lin(0, y - 120, 0, y + 90, [(0, col), (1, alpha(col, 1))]), OUTLINE, 6)
    for k in range(4):
        stroke_line(cr, [(x - 220 + k * 140, y - 100), (x - 200 + k * 140, y + 80)], 4, (1, 1, 1, 0.25))


def clock(cr, t, x, y, r, hours, minutes, dark=False):
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, hexc("#2b2b33") if dark else WHITE, OUTLINE, 6)
    for k in range(12):
        a = k * math.pi / 6
        stroke_line(cr, [(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8),
                         (x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9)], 4,
                    WHITE if dark else OUTLINE, curve=False)
    ha = (hours % 12 + minutes / 60) * math.pi / 6 - math.pi / 2
    ma = minutes * math.pi / 30 - math.pi / 2
    col = hexc("#ffcf3f") if dark else OUTLINE
    stroke_line(cr, [(x, y), (x + math.cos(ha) * r * 0.5, y + math.sin(ha) * r * 0.5)], 9, col, curve=False)
    stroke_line(cr, [(x, y), (x + math.cos(ma) * r * 0.75, y + math.sin(ma) * r * 0.75)], 6, col, curve=False)


def phone(cr, x, y, s=1.0, rot=0.0, glow=True, screen=None):
    """A phone (portrait) centred at (x, y); `screen(cr, w, h)` draws inside its screen."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    if glow:
        soft_disc(cr, 0, 0, 260, (0.55, 0.75, 1.0, 0.35))
    rrect(cr, -70, -130, 140, 260, 20)
    paint(cr, hexc("#1b1b1f"), OUTLINE, 5)
    rrect(cr, -60, -116, 120, 232, 12)
    paint(cr, hexc("#9fd0ff"), None, 0)
    if screen:
        cr.save()
        rrect(cr, -60, -116, 120, 232, 12)
        cr.clip()
        cr.translate(-60, -116)
        screen(cr, 120, 232)
        cr.restore()
    cr.restore()
