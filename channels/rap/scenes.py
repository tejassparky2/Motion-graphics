"""Dark flat-anime close-ups for the rap lyric videos (pycairo).

Every scene is draw(cr, p, beat) on a 1080x1920 canvas: p = 0..1 progress through the shot, beat = 0..1 pulse that
peaks on each beat. Palette: black / navy / teal with one red accent; grain and chromatic edges are added afterwards
in lyricvid.py.
"""
import math
import random

import cairo

W, H = 1080, 1920

BLACK = (0.02, 0.03, 0.05)
NAVY = (0.04, 0.08, 0.14)
TEAL = (0.07, 0.21, 0.25)
TEAL2 = (0.13, 0.36, 0.40)
MIST = (0.55, 0.75, 0.78)
PALE = (0.82, 0.90, 0.91)
SKIN = (0.20, 0.30, 0.34)
SKIN_LIT = (0.36, 0.50, 0.53)
RED = (0.90, 0.07, 0.16)
WARM = (1.00, 0.80, 0.42)


def rgb(cr, c, a=1.0):
    cr.set_source_rgba(c[0], c[1], c[2], a)


def bg(cr, top=NAVY, bottom=BLACK):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    cr.set_source(g)
    cr.paint()


def glow(cr, x, y, r, c, a=0.8):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()


def ink(cr, width=6, c=BLACK, a=1.0):
    """Anime line-art stroke."""
    rgb(cr, c, a)
    cr.set_line_width(width)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def speed_lines(cr, n, seed, cx=W / 2, cy=H / 2, c=MIST, a=0.10):
    rnd = random.Random(seed)
    for _ in range(n):
        ang = rnd.uniform(0, 2 * math.pi)
        r0 = rnd.uniform(520, 760)
        cr.move_to(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0)
        cr.line_to(cx + math.cos(ang) * 1600, cy + math.sin(ang) * 1600)
        rgb(cr, c, a)
        cr.set_line_width(rnd.uniform(2, 7))
        cr.stroke()


def crack(cr, x, y, ang, length, seed, grow=1.0, width=5, c=BLACK, a=1.0):
    rnd = random.Random(seed)
    pts = [(x, y)]
    steps = 9
    for i in range(steps):
        ang += rnd.uniform(-0.6, 0.6)
        x += math.cos(ang) * length / steps
        y += math.sin(ang) * length / steps
        pts.append((x, y))
    n = max(1, int(len(pts) * grow))
    cr.move_to(*pts[0])
    for pt in pts[1:n]:
        cr.line_to(*pt)
    ink(cr, width, c, a)
    for i in range(2, n, 3):
        b = pts[i]
        cr.move_to(*b)
        a2 = ang + rnd.choice([-1, 1]) * rnd.uniform(0.6, 1.2)
        cr.line_to(b[0] + math.cos(a2) * length * 0.22, b[1] + math.sin(a2) * length * 0.22)
        ink(cr, width * 0.6, c, a)


# ---------------------------------------------------------------- scenes

def bulb(cr, p, beat):
    """Cold room: a bare bulb flickers, then dies."""
    bg(cr, (0.05, 0.10, 0.15), BLACK)
    on = 1.0 if p < 0.45 else (0.0 if p > 0.8 else (1.0 if int(p * 40) % 3 else 0.15))
    # window light on the wall
    rgb(cr, TEAL, 0.5)
    cr.rectangle(120, 380, 300, 420)
    cr.fill()
    rgb(cr, BLACK, 0.9)
    cr.rectangle(262, 380, 16, 420)
    cr.rectangle(120, 582, 300, 16)
    cr.fill()
    glow(cr, W / 2, 1000, 900 * (0.6 + 0.4 * on), WARM, 0.35 * on)
    cr.move_to(W / 2, 0)
    cr.line_to(W / 2, 760)
    ink(cr, 10)
    rgb(cr, (0.12, 0.14, 0.16))
    cr.rectangle(W / 2 - 46, 740, 92, 90)
    cr.fill()
    # glass
    cr.move_to(W / 2 - 50, 830)
    cr.curve_to(W / 2 - 60, 900, W / 2 - 190, 960, W / 2 - 190, 1080)
    cr.curve_to(W / 2 - 190, 1200, W / 2 + 190, 1200, W / 2 + 190, 1080)
    cr.curve_to(W / 2 + 190, 960, W / 2 + 60, 900, W / 2 + 50, 830)
    cr.close_path()
    g = cairo.RadialGradient(W / 2, 1060, 10, W / 2, 1060, 220)
    g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.25 + 0.75 * on)
    g.add_color_stop_rgba(1, 0.30, 0.45, 0.50, 0.35)
    cr.set_source(g)
    cr.fill_preserve()
    ink(cr, 8)
    cr.move_to(W / 2 - 40, 1020)
    for i in range(6):
        cr.line_to(W / 2 - 40 + (i + 1) * 13.3, 1000 + (i % 2) * 40)
    ink(cr, 6, WARM if on > 0.5 else (0.2, 0.2, 0.2))
    # bed silhouette
    rgb(cr, BLACK)
    cr.move_to(0, 1600)
    cr.curve_to(300, 1520, 700, 1540, W, 1580)
    cr.line_to(W, H)
    cr.line_to(0, H)
    cr.fill()


def eye(cr, p, beat, veins=True):
    """Extreme close-up eye; red veins creep in from the corners."""
    bg(cr, (0.10, 0.17, 0.20), (0.04, 0.07, 0.09))
    cy = 960
    rgb(cr, SKIN)
    cr.rectangle(0, 0, W, H)
    cr.fill()
    glow(cr, W / 2, cy, 900, SKIN_LIT, 0.5)
    # lid crease
    cr.move_to(40, cy - 120)
    cr.curve_to(300, cy - 420, 780, cy - 420, 1040, cy - 120)
    ink(cr, 10, BLACK, 0.7)
    # sclera
    cr.move_to(20, cy)
    cr.curve_to(280, cy - 330, 800, cy - 330, 1060, cy)
    cr.curve_to(800, cy + 270, 280, cy + 270, 20, cy)
    cr.close_path()
    cr.save()
    cr.clip_preserve()
    rgb(cr, (0.70, 0.78, 0.78))
    cr.fill()
    if veins:
        for k, (x, y, a) in enumerate([(40, cy, 0.1), (1040, cy, math.pi - 0.1), (60, cy + 40, -0.3),
                                       (1020, cy - 30, math.pi + 0.3), (100, cy - 60, 0.4), (980, cy + 60, math.pi - 0.4)]):
            crack(cr, x, y, a, 360, 11 + k, grow=ease(p * 1.6), width=4, c=RED, a=0.85)
    # iris follows a little
    ix = W / 2 + 30 * math.sin(p * 3)
    g = cairo.RadialGradient(ix, cy - 20, 20, ix, cy - 20, 230)
    g.add_color_stop_rgb(0, *TEAL2)
    g.add_color_stop_rgb(0.75, *TEAL)
    g.add_color_stop_rgb(1, BLACK[0], BLACK[1], BLACK[2])
    cr.set_source(g)
    cr.arc(ix, cy - 20, 230, 0, 2 * math.pi)
    cr.fill()
    rgb(cr, BLACK)
    cr.arc(ix, cy - 20, 95 + 25 * beat, 0, 2 * math.pi)
    cr.fill()
    rgb(cr, PALE, 0.95)
    cr.arc(ix + 70, cy - 90, 34, 0, 2 * math.pi)
    cr.fill()
    rgb(cr, PALE, 0.6)
    cr.arc(ix - 60, cy + 40, 14, 0, 2 * math.pi)
    cr.fill()
    # lid shadow
    g = cairo.LinearGradient(0, cy - 300, 0, cy - 100)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.7)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    cr.move_to(20, cy)
    cr.curve_to(280, cy - 330, 800, cy - 330, 1060, cy)
    ink(cr, 18)
    for i in range(9):
        x = 140 + i * 100
        y = cy - 255 + abs(i - 4) ** 1.9 * 7
        cr.move_to(x, y)
        cr.line_to(x + (i - 4) * 14, y - 70)
        ink(cr, 9)
    cr.move_to(20, cy)
    cr.curve_to(280, cy + 270, 800, cy + 270, 1060, cy)
    ink(cr, 6, BLACK, 0.8)


def door(cr, p, beat):
    """A hand knocks on a closed bedroom door; warm light under it."""
    bg(cr, (0.06, 0.12, 0.16), BLACK)
    rgb(cr, (0.08, 0.15, 0.18))
    cr.rectangle(150, 0, 780, 1640)
    cr.fill()
    for (x, y, w, h) in [(220, 120, 640, 620), (220, 840, 640, 680)]:
        cr.rectangle(x, y, w, h)
        ink(cr, 8, BLACK, 0.8)
        cr.rectangle(x + 14, y + 14, w - 28, h - 28)
        ink(cr, 3, TEAL2, 0.4)
    rgb(cr, BLACK)
    cr.rectangle(0, 1640, W, H - 1640)
    cr.fill()
    glow(cr, W / 2, 1650, 600, WARM, 0.55)
    rgb(cr, WARM, 0.9)
    cr.rectangle(150, 1636, 780, 10)
    cr.fill()
    # knocking fist from the right, jolts on the beat
    x = 760 - 60 * beat
    y = 760
    rgb(cr, SKIN)
    cr.move_to(W + 20, y + 40)
    cr.line_to(x + 160, y + 30)
    cr.curve_to(x + 40, y + 20, x - 30, y + 60, x - 20, y + 150)
    cr.curve_to(x - 10, y + 250, x + 100, y + 280, x + 200, y + 260)
    cr.line_to(W + 20, y + 300)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    for k in range(3):
        cr.move_to(x - 10, y + 105 + k * 48)
        cr.curve_to(x + 30, y + 95 + k * 48, x + 70, y + 100 + k * 48, x + 90, y + 115 + k * 48)
        ink(cr, 5, BLACK, 0.8)
    if beat > 0.3:
        for k in range(3):
            cr.move_to(x - 50, y + 60 + k * 70)
            cr.line_to(x - 120 - 40 * beat, y + 30 + k * 85)
            ink(cr, 7, PALE, beat)


def phone(cr, p, beat):
    """Phone face-up on the bed: black screen, nothing."""
    bg(cr, (0.06, 0.11, 0.15), (0.03, 0.05, 0.07))
    rnd = random.Random(4)
    for _ in range(14):
        y = rnd.uniform(0, H)
        cr.move_to(0, y)
        cr.curve_to(400, y + rnd.uniform(-120, 120), 700, y + rnd.uniform(-120, 120), W, y + rnd.uniform(-80, 80))
        ink(cr, rnd.uniform(3, 10), BLACK, 0.35)
    cr.save()
    cr.translate(W / 2, 980)
    cr.rotate(-0.12)
    rgb(cr, BLACK, 0.6)
    cr.rectangle(-270, -500, 560, 1040)
    cr.fill()
    rgb(cr, (0.09, 0.10, 0.12))
    _round_rect(cr, -280, -520, 560, 1040, 70)
    cr.fill_preserve()
    ink(cr, 8)
    rgb(cr, (0.01, 0.015, 0.02))
    _round_rect(cr, -250, -490, 500, 980, 50)
    cr.fill()
    # cold reflection streak
    cr.move_to(-250, -100)
    cr.line_to(-80, -490)
    cr.line_to(20, -490)
    cr.line_to(-250, 120)
    cr.close_path()
    rgb(cr, MIST, 0.08)
    cr.fill()
    cr.select_font_face("Anton")
    cr.set_font_size(54)
    rgb(cr, MIST, 0.35 + 0.15 * beat)
    _center_text(cr, "0 NEW MESSAGES", 0, 20)
    cr.set_font_size(110)
    rgb(cr, MIST, 0.25)
    _center_text(cr, "3:07", 0, -260)
    cr.restore()


def chalk_wall(cr, p, beat):
    """A hand writes a whole life in chalk on a cracked wall."""
    bg(cr, (0.10, 0.17, 0.20), (0.05, 0.09, 0.11))
    for k, (x, y, a) in enumerate([(0, 300, 0.3), (W, 900, 2.9), (300, H, -1.3), (W, 1500, 3.4)]):
        crack(cr, x, y, a, 700, 30 + k, width=7)
    rnd = random.Random(8)
    lines = 9
    done = p * lines * 1.1
    for i in range(lines):
        f = min(max(done - i, 0), 1)
        if f <= 0:
            break
        y = 380 + i * 110
        x = 140
        cr.move_to(x, y)
        n = int(26 * f)
        for j in range(n):
            x += 26
            cr.line_to(x, y + rnd.uniform(-22, 22))
        ink(cr, 6, PALE, 0.8)
    # writing hand at the current point
    i = min(int(done), lines - 1)
    hx = 140 + 26 * 26 * min(done - i, 1)
    hy = 380 + i * 110
    rgb(cr, SKIN)
    cr.move_to(hx, hy)
    cr.line_to(hx + 40, hy + 30)
    cr.curve_to(hx + 160, hy + 60, hx + 240, hy + 200, hx + 220, hy + 320)
    cr.line_to(hx + 520, H + 100)
    cr.line_to(hx + 900, H + 100)
    cr.curve_to(hx + 400, hy + 200, hx + 260, hy - 40, hx + 60, hy - 20)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    rgb(cr, PALE)
    cr.move_to(hx - 6, hy + 4)
    cr.line_to(hx + 60, hy - 40)
    ink(cr, 18, PALE)


def pointers(cr, p, beat):
    """Faceless silhouettes point at you; mouths are red slashes."""
    bg(cr, (0.10, 0.20, 0.24), (0.02, 0.04, 0.06))
    glow(cr, W / 2, 700, 950, TEAL2, 0.7)
    speed_lines(cr, 40, 2, a=0.07)
    for k, (x, y, s) in enumerate([(200, 760, 0.8), (880, 700, 0.85), (540, 1050, 1.15)]):
        cr.save()
        cr.translate(x, y + 10 * math.sin(p * 6 + k))
        cr.scale(s, s)
        rgb(cr, BLACK)
        cr.arc(0, -260, 170, 0, 2 * math.pi)
        cr.fill()
        cr.move_to(-330, 400)
        cr.curve_to(-300, -60, 300, -60, 330, 400)
        cr.line_to(330, 900)
        cr.line_to(-330, 900)
        cr.fill()
        # arm pointing at the camera (foreshortened)
        cr.move_to(-60, 60)
        cr.line_to(60, 60)
        cr.line_to(30, 260)
        cr.line_to(-30, 260)
        cr.close_path()
        cr.fill()
        cr.arc(0, 290, 70 + 10 * beat, 0, 2 * math.pi)
        cr.fill()
        rgb(cr, RED)
        cr.move_to(-80, -200)
        cr.line_to(80, -230 - 20 * beat)
        cr.set_line_width(22)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
        rgb(cr, MIST, 0.25)
        cr.arc(0, -260, 172, math.pi * 1.1, math.pi * 1.6)
        cr.set_line_width(8)
        cr.stroke()
        cr.restore()


def mirror(cr, p, beat):
    """An empty mirror; a red outline of someone appears in it."""
    bg(cr, (0.05, 0.10, 0.14), BLACK)
    cx, cy = W / 2, 900
    cr.save()
    cr.translate(cx, cy)
    cr.scale(1, 1.45)
    cr.arc(0, 0, 400, 0, 2 * math.pi)
    cr.restore()
    rgb(cr, (0.16, 0.20, 0.22))
    cr.fill_preserve()
    ink(cr, 40, (0.10, 0.12, 0.14))
    cr.save()
    cr.translate(cx, cy)
    cr.scale(1, 1.45)
    cr.arc(0, 0, 370, 0, 2 * math.pi)
    cr.restore()
    g = cairo.LinearGradient(0, 300, 0, 1500)
    g.add_color_stop_rgb(0, *TEAL)
    g.add_color_stop_rgb(1, *NAVY)
    cr.set_source(g)
    cr.fill()
    rgb(cr, PALE, 0.10)
    cr.move_to(cx - 260, cy - 300)
    cr.line_to(cx - 120, cy - 420)
    cr.line_to(cx - 20, cy - 420)
    cr.line_to(cx - 260, cy - 140)
    cr.fill()
    a = ease((p - 0.25) * 2.2)
    if a > 0:
        cr.arc(cx, cy - 150, 120, 0, 2 * math.pi)
        cr.move_to(cx - 260, cy + 450)
        cr.curve_to(cx - 240, cy + 40, cx + 240, cy + 40, cx + 260, cy + 450)
        ink(cr, 9 + 6 * beat, RED, a)
        glow(cr, cx, cy, 500, RED, 0.12 * a)


def fist_stone(cr, p, beat):
    """A fist closes around a stone."""
    bg(cr, (0.08, 0.16, 0.19), BLACK)
    glow(cr, W / 2, 1000, 700, TEAL2, 0.35)
    close = ease(p * 1.8)
    # stone
    rgb(cr, (0.30, 0.34, 0.36))
    cr.move_to(420, 900)
    cr.line_to(600, 860)
    cr.line_to(680, 980)
    cr.line_to(610, 1110)
    cr.line_to(450, 1090)
    cr.line_to(390, 980)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    cr.move_to(470, 940)
    cr.line_to(560, 1000)
    ink(cr, 4, BLACK, 0.6)
    # palm
    rgb(cr, SKIN)
    cr.move_to(300, 1900)
    cr.line_to(330, 1150)
    cr.curve_to(360, 1080, 720, 1080, 760, 1150)
    cr.line_to(800, 1900)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    # fingers curl over the stone
    for k in range(4):
        x = 360 + k * 105
        cr.save()
        cr.translate(x + 45, 1130)
        cr.rotate(-math.pi * (0.95 * (1 - close) + 0.05) * 0.9)
        _round_rect(cr, -48, -360 + 120 * close, 96, 360 - 120 * close, 44)
        rgb(cr, SKIN_LIT if k % 2 else SKIN)
        cr.fill_preserve()
        ink(cr, 7)
        cr.restore()
    # thumb
    cr.save()
    cr.translate(760, 1220)
    cr.rotate(-0.6 - 0.9 * close)
    _round_rect(cr, -50, -260, 100, 260, 48)
    rgb(cr, SKIN_LIT)
    cr.fill_preserve()
    ink(cr, 7)
    cr.restore()
    if close > 0.9:
        speed_lines(cr, 30, 9, cy=1050, c=PALE, a=0.2 * beat)


def stairs(cr, p, beat):
    """Feet climb a staircase whose steps are all the word NO."""
    bg(cr, (0.08, 0.16, 0.20), BLACK)
    shift = p * 220
    cr.select_font_face("Anton")
    for i in range(9):
        y = 1800 - i * 220 + shift
        x = 80 + i * 70
        w = W - 2 * x
        rgb(cr, (0.10 + i * 0.012, 0.18 + i * 0.012, 0.21 + i * 0.012))
        cr.rectangle(x, y - 60, w, 60)
        cr.fill_preserve()
        ink(cr, 6)
        rgb(cr, BLACK, 0.9)
        cr.rectangle(x, y, w, 160)
        cr.fill()
        cr.set_font_size(130)
        rgb(cr, RED if i % 3 == 1 else MIST, 0.55)
        _center_text(cr, "NO", W / 2, y + 140)
    # one sneaker stepping up on the beat
    fy = 1150 - 50 * beat
    rgb(cr, (0.85, 0.88, 0.88))
    cr.move_to(300, fy)
    cr.curve_to(300, fy - 120, 520, fy - 160, 600, fy - 60)
    cr.curve_to(760, fy - 40, 800, fy, 800, fy + 40)
    cr.line_to(300, fy + 40)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    rgb(cr, RED)
    cr.rectangle(300, fy + 20, 500, 22)
    cr.fill()
    rgb(cr, BLACK)
    cr.rectangle(330, fy - 700, 230, 600)
    cr.fill()


def slab(cr, p, beat):
    """A name carved in stone; cracks spread through it."""
    bg(cr, (0.06, 0.12, 0.16), BLACK)
    rgb(cr, (0.24, 0.29, 0.31))
    cr.move_to(170, 1700)
    cr.line_to(170, 640)
    cr.curve_to(170, 300, 910, 300, 910, 640)
    cr.line_to(910, 1700)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 10)
    glow(cr, 700, 600, 600, MIST, 0.15)
    cr.select_font_face("Anton")
    cr.set_font_size(170)
    rgb(cr, BLACK, 0.85)
    _center_text(cr, "MY NAME", W / 2, 1000)
    cr.set_font_size(60)
    _center_text(cr, "R.I.P.", W / 2, 760)
    for k, (x, y, a) in enumerate([(540, 400, 1.5), (300, 1100, -0.3), (860, 1300, 3.4)]):
        crack(cr, x, y, a, 650, 50 + k, grow=ease(p * 1.5 + 0.1), width=6)
    rgb(cr, BLACK)
    cr.rectangle(0, 1660, W, H)
    cr.fill()
    rnd = random.Random(3)
    for _ in range(40):
        x = rnd.uniform(0, W)
        cr.move_to(x, 1680)
        cr.line_to(x + rnd.uniform(-30, 30), 1680 - rnd.uniform(40, 140))
        ink(cr, 5, TEAL, 0.9)


def breath(cr, p, beat):
    """Close-up lips exhaling cold breath with a red glow inside."""
    bg(cr, (0.05, 0.10, 0.13), BLACK)
    rgb(cr, SKIN)
    cr.move_to(-50, 300)
    cr.curve_to(300, 250, 560, 600, 600, 860)
    cr.curve_to(640, 900, 560, 940, 640, 1000)
    cr.curve_to(560, 1060, 620, 1100, 560, 1180)
    cr.curve_to(560, 1400, 300, 1700, -50, 1750)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 10)
    glow(cr, 470, 800, 300, SKIN_LIT, 0.4)
    rgb(cr, RED, 0.7 + 0.3 * beat)
    cr.move_to(560, 990)
    cr.curve_to(600, 985, 620, 1000, 640, 1000)
    cr.curve_to(620, 1010, 600, 1020, 560, 1020)
    cr.close_path()
    cr.fill()
    glow(cr, 640, 1005, 120 + 60 * beat, RED, 0.45)
    rnd = random.Random(12)
    for k in range(26):
        d = (p * 1.4 + k / 26) % 1
        x = 660 + d * 520 + rnd.uniform(-40, 40)
        y = 1000 + rnd.uniform(-1, 1) * d * 320
        glow(cr, x, y, 40 + d * 160, MIST, 0.20 * (1 - d))


def scar(cr, p, beat):
    """A chest in shadow; a scar is drawn in red."""
    bg(cr, (0.08, 0.14, 0.17), BLACK)
    rgb(cr, SKIN)
    cr.move_to(0, 300)
    cr.curve_to(300, 260, 780, 260, W, 300)
    cr.line_to(W, H)
    cr.line_to(0, H)
    cr.close_path()
    cr.fill()
    glow(cr, 380, 900, 600, SKIN_LIT, 0.45)
    for side in (-1, 1):
        cr.move_to(W / 2 + side * 40, 650)
        cr.curve_to(W / 2 + side * 300, 760, W / 2 + side * 420, 1000, W / 2 + side * 380, 1150)
        ink(cr, 8, BLACK, 0.55)
    cr.move_to(W / 2, 500)
    cr.line_to(W / 2, 1500)
    ink(cr, 5, BLACK, 0.3)
    g = ease(p * 1.7)
    pts = [(250, 700), (420, 860), (560, 980), (720, 1130), (860, 1300)]
    cr.move_to(*pts[0])
    for i in range(1, len(pts)):
        f = min(max(g * (len(pts) - 1) - (i - 1), 0), 1)
        if f <= 0:
            break
        a, b = pts[i - 1], pts[i]
        cr.line_to(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
    ink(cr, 18 + 6 * beat, RED)
    for i in range(1, int(g * 8) + 1):
        x = 250 + i * 72
        y = 700 + i * 75
        cr.move_to(x - 30, y + 30)
        cr.line_to(x + 30, y - 30)
        ink(cr, 6, (0.5, 0.05, 0.1))


def fall(cr, p, beat):
    """A body hits the ground; dust."""
    bg(cr, (0.10, 0.18, 0.21), (0.03, 0.05, 0.07))
    gy = 1350
    rgb(cr, BLACK)
    cr.rectangle(0, gy, W, H - gy)
    cr.fill()
    drop = ease(p * 3)
    cr.save()
    cr.translate(W / 2, gy - 120 - (1 - drop) * 600)
    cr.rotate(-0.4 * (1 - drop) - 1.45 * drop)
    rgb(cr, BLACK)
    cr.arc(0, -330, 90, 0, 2 * math.pi)
    cr.fill()
    _round_rect(cr, -110, -240, 220, 420, 80)
    cr.fill()
    _round_rect(cr, -100, 160, 90, 360, 40)
    _round_rect(cr, 10, 160, 90, 360, 40)
    cr.fill()
    rgb(cr, MIST, 0.3)
    cr.arc(0, -330, 92, math.pi, math.pi * 1.6)
    cr.set_line_width(8)
    cr.stroke()
    cr.restore()
    if drop > 0.95:
        d = (p - 0.33) / 0.67
        rnd = random.Random(5)
        for _ in range(40):
            ang = rnd.uniform(math.pi, 2 * math.pi)
            r = d * rnd.uniform(150, 600)
            glow(cr, W / 2 + math.cos(ang) * r * 1.4, gy + math.sin(ang) * r * 0.4, 60 + 120 * d, MIST,
                 0.25 * (1 - d))
        speed_lines(cr, 30, 7, cy=gy, c=PALE, a=0.15 * (1 - d))


def reach(cr, p, beat):
    """A hand reaches up out of the dark for a huge pale moon."""
    bg(cr, (0.06, 0.13, 0.17), BLACK)
    glow(cr, W / 2, 560, 700, MIST, 0.25)
    rgb(cr, (0.93, 0.88, 0.62))
    cr.arc(W / 2 + 60, 560, 300, 0, 2 * math.pi)
    cr.fill()
    rgb(cr, (0.80, 0.74, 0.50), 0.6)
    for (x, y, r) in [(-40, -60, 60), (90, 80, 40), (-110, 120, 30), (140, -120, 28)]:
        cr.arc(W / 2 + 60 + x, 560 + y, r, 0, 2 * math.pi)
        cr.fill()
    lift = ease(p * 1.3)
    hx, hy = 470, 1150 - 260 * lift
    # forearm from the bottom edge
    rgb(cr, SKIN)
    cr.move_to(hx - 110, H + 50)
    cr.line_to(hx - 90, hy + 260)
    cr.line_to(hx + 90, hy + 260)
    cr.line_to(hx + 140, H + 50)
    cr.close_path()
    cr.fill_preserve()
    ink(cr, 8)
    # palm
    _round_rect(cr, hx - 110, hy + 40, 220, 250, 70)
    rgb(cr, SKIN_LIT)
    cr.fill_preserve()
    ink(cr, 8)
    # spread fingers straining upward
    for k, (dx, ln, ang) in enumerate([(-80, 190, -0.18), (-28, 240, -0.05), (28, 250, 0.04), (80, 210, 0.15)]):
        cr.save()
        cr.translate(hx + dx, hy + 60)
        cr.rotate(ang * (0.6 + 0.4 * lift))
        _round_rect(cr, -26, -ln, 52, ln + 30, 26)
        rgb(cr, SKIN_LIT if k % 2 else SKIN)
        cr.fill_preserve()
        ink(cr, 7)
        cr.restore()
    cr.save()
    cr.translate(hx + 110, hy + 190)
    cr.rotate(0.9)
    _round_rect(cr, -28, -170, 56, 190, 28)
    rgb(cr, SKIN)
    cr.fill_preserve()
    ink(cr, 7)
    cr.restore()
    # moonlight rim on the fingers
    cr.move_to(hx - 106, hy + 60)
    cr.line_to(hx - 120, hy - 120)
    ink(cr, 5, PALE, 0.5 + 0.4 * beat)


def sunrise(cr, p, beat):
    """A small figure stands against a huge rising sun."""
    bg(cr, (0.10, 0.20, 0.25), (0.03, 0.05, 0.08))
    sy = 1250 - 260 * ease(p)
    glow(cr, W / 2, sy, 1100, RED, 0.35)
    glow(cr, W / 2, sy, 700, WARM, 0.35)
    rgb(cr, (1.0, 0.86, 0.55))
    cr.arc(W / 2, sy, 420 + 10 * beat, 0, 2 * math.pi)
    cr.fill()
    for k in range(5):
        rgb(cr, (0.95, 0.40, 0.30), 0.35)
        cr.rectangle(0, sy + 60 + k * 70, W, 10 + k * 4)
        cr.fill()
    rgb(cr, BLACK)
    cr.move_to(0, 1450)
    cr.curve_to(300, 1330, 780, 1330, W, 1450)
    cr.line_to(W, H)
    cr.line_to(0, H)
    cr.fill()
    cr.save()
    cr.translate(W / 2, 1360)
    cr.arc(0, -330, 42, 0, 2 * math.pi)
    cr.fill()
    cr.move_to(-60, -280)
    cr.line_to(60, -280)
    cr.line_to(50, -120)
    cr.line_to(40, 0)
    cr.line_to(10, 0)
    cr.line_to(0, -110)
    cr.line_to(-10, 0)
    cr.line_to(-40, 0)
    cr.line_to(-50, -120)
    cr.close_path()
    cr.fill()
    # cape of torn cloth blowing
    cr.move_to(50, -270)
    cr.curve_to(150, -250, 220 + 30 * math.sin(p * 9), -200, 260, -150)
    cr.line_to(60, -170)
    cr.fill()
    cr.restore()


def _round_rect(cr, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    cr.close_path()


def _center_text(cr, text, x, y):
    ext = cr.text_extents(text)
    cr.move_to(x - ext.width / 2 - ext.x_bearing, y)
    cr.show_text(text)


SCENES = dict(bulb=bulb, eye=eye, door=door, phone=phone, chalk=chalk_wall, pointers=pointers, mirror=mirror,
              fist=fist_stone, stairs=stairs, slab=slab, breath=breath, scar=scar, fall=fall, reach=reach,
              sunrise=sunrise)
