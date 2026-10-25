"""Tower 9, Night 1, in the illustrated 2D style (channels/horror/toon2d.py): the full episode.

Same script and narration takes as the 3D episode (tower9.py), redrawn shot by shot after the owner's "Yeah 2d better"
and their 2D reference (stats bar, blurred backgrounds, speech bubbles, A/B ending). You wear an orange ranger rain
jacket; rewatch detail: in the lightning, one of the figures holding a torch below the tower wears the same jacket.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py tower9_2d   -> out/horror/tower9_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import tower9 as ep3d
from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
SCRIPT = [dict(d) for d in ep3d.SCRIPT]
for _d in SCRIPT:
    if _d["id"] == "t17":
        _d["gap"] = 1.8          # the thunder rolls out before the voice under the hatch (it hid "Please" as "Wait")
# Quiet lines need room: the beds sit lower than in the 3D cut, and the voice under the hatch is less muffled
# (lowpass 1800 made "cold" into "cool"). Only the processing changes; the generated take is the same.
audio.GAINS.update(rain=0.2, generator=0.2)
voice.SPEAKERS["hatch"] = dict(voice.SPEAKERS["hatch"], fx="lowpass=f=2800,volume=1.6")
METADATA = hud2d.meta_2d(ep3d.METADATA)
KEY = ep3d.KEY
WARM = (1.0, 0.72, 0.38)                    # the bulb and the lantern
TORCH = (1.0, 0.55, 0.18)
BOLT = (0.75, 0.85, 1.0)                    # lightning
WARM_RIM = (1.0, 0.75, 0.45, 0.6)
COLD_RIM = (0.7, 0.82, 1.0, 0.6)
PLANK, PLANK_D = hexa("#6b4a30"), hexa("#4a3120")
STEEL, STEEL_D = hexa("#4c5650"), hexa("#2e3532")
_cache = {}


def flash_level(t, times):
    """Lightning: a bright double pulse at each time."""
    v = 0.0
    for ft in times:
        for off, a in ((0.0, 1.0), (0.14, 0.7)):
            d = t - ft - off
            if 0 <= d < 0.5:
                v = max(v, a * math.exp(-d * 9))
    return v


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0, pan=(0, 0)):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1) + pan[0] * k, cy + 3 * shake * noise(t * 0.6, 4) + pan[1] * k)
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ sets
def planks(cr, x0, y0, x1, y1, horizontal=True, seed=0, base=PLANK, dark=PLANK_D, board=46):
    """Wooden boards with seams, grain and knots."""
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_source_rgba(*base)
    cr.paint()
    n = int(((y1 - y0) if horizontal else (x1 - x0)) / board) + 2
    for k in range(n):
        tone = 0.06 * math.sin(k * 2.7 + seed)
        a = (y0 if horizontal else x0) + k * board
        cr.set_source_rgba(*mix(base, (0, 0, 0, 1), 0.12 + tone))
        if horizontal:
            cr.rectangle(x0, a, x1 - x0, board)
        else:
            cr.rectangle(a, y0, board, y1 - y0)
        cr.fill()
        cr.set_source_rgba(*mix(dark, INK, 0.5))
        if horizontal:
            cr.rectangle(x0, a, x1 - x0, 3)
        else:
            cr.rectangle(a, y0, 3, y1 - y0)
        cr.fill()
        cr.set_source_rgba(0, 0, 0, 0.12)                   # grain
        cr.set_line_width(1.5)
        for j in range(3):
            o = a + 10 + j * 12
            if horizontal:
                cr.move_to(x0, o)
                cr.curve_to(x0 + 200, o + 3, x0 + 400, o - 3, x1, o + 2)
            else:
                cr.move_to(o, y0)
                cr.curve_to(o + 3, y0 + 300, o - 3, y0 + 600, o + 2, y1)
            cr.stroke()
        kx = ((k * 0.618 + seed * 0.1) % 1)
        cx, cy = (x0 + kx * (x1 - x0), a + board / 2) if horizontal else (a + board / 2, y0 + kx * (y1 - y0))
        cr.set_source_rgba(*mix(dark, INK, 0.3)[:3], 0.6)
        cr.save()
        cr.translate(cx, cy)
        cr.scale(1.0, 0.55) if horizontal else cr.scale(0.55, 1.0)
        cr.arc(0, 0, 7, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    cr.restore()


def night_window(cr, t, x0, y0, x1, y1, flash=0.0, horizon=0.62):
    """Outside a lookout window: night sky, the forest far below the horizon, rain, lightning."""
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, *mix((0.03, 0.04, 0.09, 1), (0.6, 0.7, 0.9, 1), flash))
    g.add_color_stop_rgba(1, *mix((0.07, 0.08, 0.13, 1), (0.5, 0.58, 0.75, 1), flash))
    cr.set_source(g)
    cr.paint()
    hy = y0 + (y1 - y0) * horizon
    cr.set_source_rgba(0.015, 0.025, 0.03, 1)
    pts = [(x0 - 20, y1)]
    for k in range(0, int(x1 - x0) + 60, 24):
        pts.append((x0 + k, hy - 10 - 18 * abs(math.sin(k * 0.13)) - 8 * ((k * 7) % 3)))
    pts.append((x1 + 20, y1))
    poly(cr, pts)
    cr.fill()
    if flash > 0.3:                                        # the bolt
        cr.set_source_rgba(0.9, 0.95, 1, flash)
        cr.set_line_width(4)
        x = x0 + (x1 - x0) * 0.68
        cr.move_to(x, y0)
        y = y0
        k = 0
        while y < hy - 20:
            y += 40
            x += (-1) ** k * 22 + 6
            k += 1
            cr.line_to(x, y)
        cr.stroke()
    cr.set_source_rgba(0.7, 0.8, 0.95, 0.22 + 0.3 * flash)
    cr.set_line_width(2)
    for k in range(50):
        x = x0 + (k * 37.7) % (x1 - x0)
        y = y0 + ((k * 83.1 + t * 1100) % (y1 - y0 + 60)) - 30
        cr.move_to(x, y)
        cr.line_to(x - 5, y + 30)
        cr.stroke()
    cr.restore()


def bulb(cr, t, x, y, on=1.0, cord=0):
    """The bare bulb on its cord, swaying a little."""
    sw = 0.04 * math.sin(t * 1.1)
    bx, by = x + (y - cord) * math.sin(sw), y
    cr.set_source_rgba(0.08, 0.06, 0.05, 1)
    cr.set_line_width(4)
    cr.move_to(x, cord)
    cr.line_to(bx, by - 30)
    cr.stroke()
    toon(cr, lambda c: c.rectangle(bx - 14, by - 34, 28, 22), hexa("#3a3530"), None, (0, 0), None, lw=3)
    glow(cr, bx, by, 420, WARM, 0.45 * on)
    toon(cr, lambda c: c.arc(bx, by, 24, 0, 2 * math.pi), mix((0.45, 0.42, 0.38, 1), (1, 0.92, 0.7, 1), on), None,
         (0, 0), None, lw=3)


def cabin(cr, t, on=1.0, flash=0.0):
    """Inside the lookout cabin: boards, a band of windows on the storm, the bulb."""
    planks(cr, 0, 0, W, H, seed=2)
    x0, y0, x1, y1 = 30, 200, 690, 760
    night_window(cr, t, x0, y0, x1, y1, flash)
    for x in (30, 250, 470, 690):                        # mullions and frame
        toon(cr, lambda c, x=x: c.rectangle(x - 12, y0 - 12, 24, y1 - y0 + 24), PLANK, PLANK_D, (-4, -3), None, lw=4)
    toon(cr, lambda c: c.rectangle(0, y0 - 24, W, 24), PLANK, PLANK_D, (0, -4), None, lw=4)
    toon(cr, lambda c: c.rectangle(0, y1, W, 30), mix(PLANK, (1, 1, 1, 1), 0.1), PLANK_D, (0, -5), None, lw=4)
    bulb(cr, t, 360, 120, on)
    g = cairo.RadialGradient(360, 120, 40, 360, 300, 1000)   # the bulb's warm light, falling off into the dark
    g.add_color_stop_rgba(0, *WARM, 0.18 * on)
    g.add_color_stop_rgba(0.5, 0, 0, 0, 0.25)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.7)
    cr.set_source(g)
    cr.paint()


def radio_unit(cr, t, x, y, s, rx=0.0, ch="CH 09"):
    """The base-station radio on the desk: LCD, speaker grille, knobs, the RX light; a hand mic on its coiled cord."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: tk.tk_rrect(c, -260, -160, 520, 300, 24), hexa("#3c423c"), hexa("#262a26"), (-10, -8),
         WARM_RIM, (0, -8), lw=6)
    toon(cr, lambda c: tk.tk_rrect(c, -230, -130, 260, 110, 10), hexa("#141814"), None, (0, 0), None, lw=4)
    lcd = (0.62, 0.86, 0.52, 1)
    glow(cr, -100, -75, 170, (0.6, 0.9, 0.5), 0.2)
    cr.set_source_rgba(*lcd)
    tk.tk_rrect(cr, -222, -122, 244, 94, 6)
    cr.fill()
    hud2d._text(cr, ch, -205, -62, 46, (0.08, 0.15, 0.07, 1), "Liberation Mono")
    lvl = (0.5 + 0.5 * abs(noise(t * 9, 2))) * rx if rx > 0 else 0.15
    for k in range(5):                                       # signal bars jump while it receives
        on = k < 1 + int(lvl * 5)
        cr.set_source_rgba(0.08, 0.15, 0.07, 1 if on else 0.2)
        cr.rectangle(-30 + k * 9, -40 - k * 9, 6, 8 + k * 9)
        cr.fill()
    hud2d._text(cr, "162.475", -205, -36, 22, (0.08, 0.15, 0.07, 1), "Liberation Mono")
    toon(cr, lambda c: tk.tk_rrect(c, 60, -130, 170, 230, 16), hexa("#222622"), None, (0, 0), None, lw=4)
    cr.set_source_rgba(0.05, 0.05, 0.05, 1)                  # grille holes
    for i in range(7):
        for j in range(9):
            cr.arc(82 + i * 21, -108 + j * 24, 5.5, 0, 2 * math.pi)
            cr.fill()
    for k, kx in enumerate((-190, -90)):                     # knobs
        toon(cr, lambda c, kx=kx: c.arc(kx, 70, 34, 0, 2 * math.pi), hexa("#1d201d"), None, (0, 0), (1, 1, 1, 0.3),
             (0, -5), lw=4)
        a = -2.2 + k * 1.5
        cr.set_source_rgba(0.9, 0.9, 0.85, 1)
        cr.set_line_width(5)
        cr.move_to(kx, 70)
        cr.line_to(kx + 26 * math.cos(a), 70 + 26 * math.sin(a))
        cr.stroke()
    red = rx * (0.6 + 0.4 * (noise(t * 15, 1) > 0))
    toon(cr, lambda c: c.arc(10, 70, 13, 0, 2 * math.pi), mix((0.25, 0.05, 0.05, 1), (1, 0.15, 0.1, 1), red), None,
         (0, 0), None, lw=3)
    if red > 0:
        glow(cr, 10, 70, 90, (1, 0.15, 0.1), 0.6 * red)
    hud2d._text(cr, "RX", 32, 80, 22, (0.85, 0.85, 0.8, 1), "Liberation Mono")
    cr.set_source_rgba(0.15, 0.15, 0.15, 1)                  # antenna
    cr.set_line_width(8)
    cr.move_to(200, -160)
    cr.line_to(230, -420)
    cr.stroke()
    cr.set_source_rgba(0.06, 0.06, 0.06, 1)                  # the coiled cord and the hand mic
    cr.set_line_width(5)
    cr.move_to(240, 60)
    for k in range(14):
        cr.curve_to(250 + k * 7, 100 + 10 * (k % 2), 256 + k * 7, 120, 258 + k * 7, 130 + 4 * k)
    cr.stroke()
    toon(cr, lambda c: tk.tk_rrect(c, 300, 170, 120, 170, 40), hexa("#1d201d"), None, (0, 0), (1, 1, 1, 0.25), (0, -6),
         lw=5)
    cr.restore()


def desk(cr, y0=820):
    """The front edge of the desk, seen from above."""
    planks(cr, 0, y0, W, H, horizontal=False, seed=5, base=hexa("#7a5638"), dark=hexa("#553a24"), board=90)
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.rectangle(0, y0, W, 14)
    cr.fill()


def radio_scene(cr, t, rx, flash=0.0):
    hud2d.blurred(cr, lambda c: cabin(c, t, flash=flash), sigma=8)
    desk(cr, 860)
    radio_unit(cr, t, 340, 760, 1.15, rx)
    glow(cr, 360, 300, 500, WARM, 0.12)


def logbook(cr, t, k1, k2):
    """The last ranger's logbook, open on the desk under the lantern; the two rules write themselves as they're read."""
    planks(cr, 0, 0, W, H, horizontal=False, seed=7, base=hexa("#7a5638"), dark=hexa("#553a24"), board=90)
    glow(cr, 620, 160, 600, WARM, 0.3)
    cr.save()
    cr.translate(360, 560)
    cr.rotate(-0.04)
    cr.scale(0.9, 0.9)
    cr.set_source_rgba(0, 0, 0, 0.45)
    tk.tk_rrect(cr, -330, -300, 670, 620, 14)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, -340, -310, 670, 610, 12), hexa("#5a2a1c"), None, (0, 0), None, lw=5)   # cover
    for side in (-1, 1):
        toon(cr, lambda c, side=side: tk.curve(c, [(0, -290), (side * 160, -300), (side * 318, -292), (side * 318, 280),
                                                   (side * 160, 286), (0, 278)]),
             hexa("#efe4c6"), hexa("#d9caa3"), (side * 6, -4), None, lw=4)
    g = cairo.LinearGradient(-40, 0, 40, 0)                 # the binding's shadow
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(0.5, 0, 0, 0, 0.35)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.rectangle(-40, -295, 80, 575)
    cr.fill()
    cr.set_source_rgba(0.2, 0.25, 0.45, 0.35)               # the old entries on the left page
    for k in range(11):
        cr.set_line_width(2)
        x = -290
        cr.move_to(x, -230 + k * 44)
        for j in range(14):
            x += 18
            cr.line_to(x, -230 + k * 44 + 4 * math.sin(j * 1.9 + k))
        cr.stroke()
    cr.set_source_rgba(0.45, 0.3, 0.15, 0.25)               # a coffee ring
    cr.set_line_width(6)
    cr.arc(-150, 160, 52, 0, 2 * math.pi)
    cr.stroke()
    ink = (0.12, 0.14, 0.3, 1)
    hud2d._text(cr, "TOWER 9", 30, -230, 40, ink, "Kalam")
    hud2d._text(cr, "night rules", 30, -188, 30, ink, "Kalam")
    rules = [(k1, ["1. NEVER answer", "the radio after 3 AM."]), (k2, ["2. NEVER open", "the hatch."])]
    y = -110
    for k, lines in rules:
        total = sum(len(s) for s in lines)
        left = int(total * clamp01(k))
        for j, ln in enumerate(lines):
            part = ln[:max(0, left)]
            left -= len(ln)
            if part:
                hud2d._text(cr, part, 24, y + j * 42, 31, ink, "Kalam")
        if k >= 1:
            cr.set_source_rgba(0.75, 0.08, 0.06, 0.9)       # NEVER, underlined twice in red
            cr.set_line_width(4)
            for d in (6, 13):
                cr.move_to(50, y + d)
                cr.line_to(152, y + d - 2)
                cr.stroke()
        y += 130
    hud2d._text(cr, "- R. Hale", 150, 230, 30, ink, "Kalam")
    cr.restore()
    cr.save()                                                # the pencil
    cr.translate(560, 980)
    cr.rotate(-0.6)
    toon(cr, lambda c: c.rectangle(-140, -12, 260, 24), hexa("#e7b93a"), hexa("#b88a1f"), (0, -4), None, lw=3)
    toon(cr, lambda c: poly(c, [(120, -12), (160, 0), (120, 12)]), hexa("#e8cfa2"), None, (0, 0), None, lw=3)
    cr.restore()


def clock(cr, t, h=3, m=14, sec0=0.0):
    """A wall clock on the boards: 3:14, the second hand ticking."""
    planks(cr, 0, 0, W, H, seed=4)
    glow(cr, 360, 200, 700, WARM, 0.22)
    cx, cy, r = 360, 560, 240
    cr.set_source_rgba(0, 0, 0, 0.4)
    cr.arc(cx + 14, cy + 18, r + 18, 0, 2 * math.pi)
    cr.fill()
    toon(cr, lambda c: c.arc(cx, cy, r + 18, 0, 2 * math.pi), hexa("#2b2b2b"), hexa("#151515"), (-6, -5),
         (1, 1, 1, 0.3), (0, -6), lw=6)
    toon(cr, lambda c: c.arc(cx, cy, r, 0, 2 * math.pi), hexa("#f1ead8"), hexa("#d6ccb2"), (-10, -8), None, lw=4)
    for k in range(60):
        a = k / 60 * 2 * math.pi
        l0 = r - (26 if k % 5 == 0 else 12)
        cr.set_source_rgba(*INK)
        cr.set_line_width(6 if k % 5 == 0 else 2.5)
        cr.move_to(cx + l0 * math.sin(a), cy - l0 * math.cos(a))
        cr.line_to(cx + (r - 6) * math.sin(a), cy - (r - 6) * math.cos(a))
        cr.stroke()
    for n in (12, 3, 6, 9):
        a = n / 12 * 2 * math.pi
        hud2d._text(cr, str(n), cx + (r - 70) * math.sin(a), cy - (r - 70) * math.cos(a) + 20, 56, INK, hud2d.ROUND,
                    "center")
    sec = sec0 + int(t)
    mm = m + sec / 60
    hh = h + mm / 60
    for frac, ln, w, col in ((hh / 12, 120, 14, INK), (mm / 60, 185, 9, INK), (sec / 60, 200, 3, (0.8, 0.1, 0.08, 1))):
        a = frac * 2 * math.pi
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(cx - 30 * math.sin(a), cy + 30 * math.cos(a))
        cr.line_to(cx + ln * math.sin(a), cy - ln * math.cos(a))
        cr.stroke()
    cr.set_source_rgba(*INK)
    cr.arc(cx, cy, 14, 0, 2 * math.pi)
    cr.fill()
    g = cairo.LinearGradient(cx - r, cy - r, cx + r, cy + r)  # glass
    g.add_color_stop_rgba(0, 1, 1, 1, 0.25)
    g.add_color_stop_rgba(0.4, 1, 1, 1, 0.0)
    cr.set_source(g)
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.fill()


def gen_panel(cr, t, fuel=0.12, on=1.0):
    """The generator's remote panel on the cabin wall: fuel gauge in the red, RUN light; the bulb above it."""
    planks(cr, 0, 0, W, H, seed=8)
    bulb(cr, t, 360, 250, on)
    cr.set_source_rgba(0.08, 0.06, 0.05, 1)                  # the cable down to the panel
    cr.set_line_width(5)
    cr.move_to(560, 0)
    cr.curve_to(600, 200, 520, 380, 500, 430)
    cr.stroke()
    toon(cr, lambda c: tk.tk_rrect(c, 140, 420, 440, 430, 18), STEEL, STEEL_D, (-10, -8), WARM_RIM, (0, -8), lw=6)
    for (x, y) in ((165, 445), (555, 445), (165, 825), (555, 825)):
        cr.set_source_rgba(0.2, 0.22, 0.2, 1)
        cr.arc(x, y, 7, 0, 2 * math.pi)
        cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, 230, 450, 260, 46, 6), hexa("#d9c46a"), None, (0, 0), None, lw=3)
    hud2d._text(cr, "GENERATOR", 360, 485, 30, INK, "Liberation Sans", "center")
    cx, cy, r = 360, 680, 130
    toon(cr, lambda c: c.arc(cx, cy, r, 0, 2 * math.pi), hexa("#f0ead8"), hexa("#d0c7ad"), (-6, -5), None, lw=5)
    cr.set_line_width(22)                                    # the red zone near E
    cr.set_source_rgba(0.85, 0.12, 0.08, 1)
    cr.arc(cx, cy, r - 24, math.pi * 1.0, math.pi * 1.22)
    cr.stroke()
    for k in range(9):
        a = math.pi + k / 8 * math.pi
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.move_to(cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a))
        cr.line_to(cx + (r - 34) * math.cos(a), cy + (r - 34) * math.sin(a))
        cr.stroke()
    hud2d._text(cr, "E", cx - r + 40, cy + 8, 34, (0.8, 0.1, 0.08, 1), hud2d.ROUND)
    hud2d._text(cr, "F", cx + r - 60, cy + 8, 34, INK, hud2d.ROUND)
    hud2d._text(cr, "FUEL", cx, cy + 62, 28, INK, "Liberation Sans", "center")
    a = math.pi + clamp01(fuel + 0.01 * noise(t * 5, 3)) * math.pi
    cr.set_source_rgba(0.1, 0.1, 0.1, 1)
    cr.set_line_width(6)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(cx, cy)
    cr.line_to(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a))
    cr.stroke()
    cr.arc(cx, cy, 12, 0, 2 * math.pi)
    cr.fill()
    toon(cr, lambda c: c.arc(470, 800, 14, 0, 2 * math.pi), mix((0.1, 0.25, 0.1, 1), (0.3, 1, 0.4, 1), on), None,
         (0, 0), None, lw=3)
    if on > 0.5:
        glow(cr, 470, 800, 60, (0.3, 1, 0.4), 0.5)
    hud2d._text(cr, "RUN", 500, 810, 22, (0.9, 0.9, 0.85, 1), "Liberation Mono")
    g = cairo.RadialGradient(360, 250, 60, 360, 500, 1000)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.6 + 0.35 * (1 - on))
    cr.set_source(g)
    cr.paint()


def tower_ext(cr, t, flash=0.0, measure=0.0, lit=1.0):
    """Tower 9 from the ground, far off: a steel lattice 30 m tall, its lit cabin, the forest, the storm."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *mix((0.03, 0.04, 0.09, 1), (0.55, 0.65, 0.85, 1), flash))
    g.add_color_stop_rgba(1, *mix((0.08, 0.09, 0.14, 1), (0.35, 0.42, 0.55, 1), flash))
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.05, 0.06, 0.1, 0.8)                 # clouds
    for k in range(6):
        tk.curve(cr, [(-80 + k * 160, 140), (-20 + k * 160, 60 + 30 * (k % 2)), (90 + k * 160, 80), (140 + k * 160, 150)])
        cr.fill()
    cx, top, ground = 360, 330, 1130
    leg = (0.1, 0.11, 0.12, 1) if flash < 0.3 else (0.05, 0.05, 0.06, 1)
    for sx in (-1, 1):
        cr.set_source_rgba(*leg)
        cr.set_line_width(10)
        cr.move_to(cx + sx * 60, top)
        cr.line_to(cx + sx * 200, ground)
        cr.stroke()
    cr.set_line_width(4)
    for k in range(6):                                       # cross bracing
        y0 = top + k * (ground - top) / 6
        y1 = top + (k + 1) * (ground - top) / 6
        w0 = 60 + 140 * (y0 - top) / (ground - top)
        w1 = 60 + 140 * (y1 - top) / (ground - top)
        cr.move_to(cx - w0, y0)
        cr.line_to(cx + w1, y1)
        cr.move_to(cx + w0, y0)
        cr.line_to(cx - w1, y1)
        cr.move_to(cx - w1, y1)
        cr.line_to(cx + w1, y1)
        cr.stroke()
    cr.set_line_width(3)                                     # the ladder up the middle
    for sx in (-1, 1):
        cr.move_to(cx + sx * 10, top)
        cr.line_to(cx + sx * 10, ground)
    for y in range(int(top), ground, 18):
        cr.move_to(cx - 10, y)
        cr.line_to(cx + 10, y)
    cr.stroke()
    toon(cr, lambda c: c.rectangle(cx - 90, top - 110, 180, 110), hexa("#3a2a1d"), hexa("#24180f"), (-5, -4), None,
         lw=4)
    toon(cr, lambda c: poly(c, [(cx - 115, top - 108), (cx, top - 175), (cx + 115, top - 108)]), hexa("#2b2f33"), None,
         (0, 0), None, lw=4)
    for k in range(3):                                       # lit windows (dark on Night 2: lit = 0)
        cr.set_source_rgba(*mix((0.03, 0.03, 0.04, 1), (1, 0.78, 0.42, 1), lit))
        cr.rectangle(cx - 78 + k * 54, top - 92, 44, 52)
        cr.fill()
        if lit > 0:
            glow(cr, cx - 56 + k * 54, top - 66, 60, WARM, 0.35 * lit)
    if lit > 0:
        cr.set_source_rgba(0.12, 0.08, 0.06, 1)             # you, a small shape in the middle window
        cr.arc(cx, top - 70, 8, 0, 2 * math.pi)
        cr.fill()
        cr.rectangle(cx - 10, top - 62, 20, 22)
        cr.fill()
    for layer, (y, col, step) in enumerate(((1020, (0.03, 0.05, 0.05), 46), (1100, (0.015, 0.03, 0.03), 60),
                                            (1190, (0.005, 0.01, 0.01), 80))):
        rim = flash * (0.5 - 0.15 * layer)
        pts = [(-40, H)]
        for x in range(-40, W + 80, step // 2):
            pts.append((x, y - (40 + 50 * layer) * (1 if (x // (step // 2)) % 2 else 0.25)))
        pts.append((W + 40, H))
        poly(cr, pts)
        cr.set_source_rgba(*mix((*col, 1), (0.35, 0.45, 0.6, 1), rim))
        cr.fill()
    cr.set_source_rgba(0.7, 0.8, 0.95, 0.25 + 0.3 * flash)   # rain
    cr.set_line_width(2)
    for k in range(70):
        x = (k * 41.3) % W
        y = ((k * 97.1 + t * 1300) % (H + 60)) - 30
        cr.move_to(x, y)
        cr.line_to(x - 6, y + 34)
        cr.stroke()
    if measure > 0:                                          # 30 M, measured on the side
        m = clamp01(measure)
        x = 610
        yb = top + (ground - top) * m
        cr.set_source_rgba(*hud2d.RED)
        cr.set_line_width(6)
        cr.move_to(x - 18, top)
        cr.line_to(x + 18, top)
        cr.move_to(x, top)
        cr.line_to(x, yb)
        cr.stroke()
        if m >= 1:
            cr.move_to(x - 18, ground)
            cr.line_to(x + 18, ground)
            cr.stroke()
            hud2d._text(cr, "30 M", x - 20, (top + ground) / 2 + 20, 56, hud2d.RED, hud2d.ROUND, "right",
                        outline=(0.05, 0.03, 0.06, 1), ow=8)


def trees_down(cr, t, n, flash=0.0):
    """Straight down from the cabin: the tower's legs, the clearing, the canopy; torches circling the base. In the
    lightning, the people holding them (one in your orange jacket)."""
    cr.set_source_rgba(*mix((0.02, 0.035, 0.03, 1), (0.25, 0.32, 0.38, 1), flash))
    cr.paint()
    cx, cy = 360, 700
    for k in range(70):                                      # the canopy: clumps of tree tops
        a = k * 2.399
        rr = 260 + (k * 37) % 420
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a) * 1.15
        r = 50 + (k * 13) % 40
        cr.set_source_rgba(*mix((0.05, 0.1, 0.075, 1), (0.25, 0.4, 0.38, 1), flash * 0.8))
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(*mix((0.08, 0.15, 0.11, 1), (0.4, 0.55, 0.55, 1), flash * 0.8))
        cr.arc(x - r * 0.25, y - r * 0.25, r * 0.55, 0, 2 * math.pi)
        cr.fill()
    cr.save()                                                # the clearing around the base
    cr.translate(cx, cy)
    cr.scale(1, 0.85)
    cr.arc(0, 0, 250, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*mix((0.11, 0.1, 0.085, 1), (0.4, 0.42, 0.45, 1), flash))
    cr.fill()
    glow(cr, cx, cy, 300, TORCH, 0.06 * min(n, 9))           # the torches light the clearing
    toon(cr, lambda c: c.rectangle(cx + 60, cy - 30, 70, 50), hexa("#2e3532"), None, (0, 0), None, lw=3)   # generator
    cr.set_source_rgba(0.2, 0.21, 0.22, 1)                   # legs from the cabin corners down to the base
    corners = [(-80, -80), (W + 80, -80), (W + 80, H + 80), (-80, H + 80)]
    base = [(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 34, cy + 30), (cx - 34, cy + 30)]
    cr.set_line_width(14)
    for (ax, ay), (bx, by) in zip(corners, base):
        cr.move_to(ax, ay)
        cr.line_to(bx, by)
    cr.stroke()
    cr.set_line_width(5)
    for k in range(1, 5):                                    # bracing rings, smaller toward the ground
        u = 1 - (1 - k / 5) ** 2
        ring = [(ax + (bx - ax) * u, ay + (by - ay) * u) for (ax, ay), (bx, by) in zip(corners, base)]
        poly(cr, ring)
        cr.stroke()
    m = max(0, n)
    for k in range(m):
        a = t * 0.35 + k * 2 * math.pi / max(m, 1) + 0.3 * math.sin(k * 1.7)
        rr = 175 + 45 * math.sin(k * 2.3)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.85
        if flash > 0.25:                                     # who is holding them
            col = tk.RANGER[0] if k == 1 else (0.05, 0.05, 0.06, 1)
            cr.set_source_rgba(*col)
            cr.save()
            cr.translate(x + 10, y + 12)
            cr.scale(1, 0.8)
            cr.arc(0, 0, 16, 0, 2 * math.pi)
            cr.restore()
            cr.fill()
            cr.set_source_rgba(0.08, 0.06, 0.06, 1)
            cr.arc(x + 10, y + 8, 8, 0, 2 * math.pi)
            cr.fill()
        fl = 0.8 + 0.2 * math.sin(t * 17 + k * 3)
        glow(cr, x, y, 46, TORCH, 0.7 * fl)
        cr.set_source_rgba(1, 0.85, 0.5, 1)
        cr.arc(x, y, 5, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(0.75, 0.85, 1, 0.3 + 0.3 * flash)     # rain falling away from you, toward the ground
    cr.set_line_width(2)
    for k in range(60):
        a = k * 2.399
        ph = (t * 1.6 + k * 0.137) % 1
        r0 = 900 * (1 - ph)
        x, y = cx + r0 * math.cos(a), cy + r0 * math.sin(a)
        cr.move_to(x, y)
        cr.line_to(cx + (r0 - 40) * math.cos(a), cy + (r0 - 40) * math.sin(a))
        cr.stroke()


def hatch(cr, t, light=0.0, frost=0.0, bumps=(), dust=(), boots=False, hand=0.0, tremble=0.0):
    """The trapdoor in the cabin floor, from above: boards, iron straps, ring, the bolt shut. Light from below
    leaks through the gaps; frost creeps out of them; each knock jumps it and shakes dust off."""
    planks(cr, 0, 0, W, H, horizontal=False, seed=11, base=hexa("#6e4c31"), dark=hexa("#4a3120"), board=72)
    glow(cr, 360, 120, 700, WARM, 0.2)
    x0, y0, x1, y1 = 170, 380, 550, 760
    jump = 0.0
    for b in bumps:
        d = t - b
        if 0 <= d < 0.35:
            jump = max(jump, 12 * math.exp(-d * 14) * math.cos(d * 40))
    cr.set_source_rgba(0.02, 0.01, 0.0, 1)                   # the gap around it
    cr.rectangle(x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20)
    cr.fill()
    if light > 0:
        cr.set_source_rgba(*TORCH, 0.9 * light)
        cr.set_line_width(7)
        cr.rectangle(x0 - 5, y0 - 5, x1 - x0 + 10, y1 - y0 + 10)
        cr.stroke()
        glow(cr, 360, 570, 380, TORCH, 0.22 * light)
    cr.save()
    cr.translate(0, -jump)
    planks(cr, x0, y0, x1, y1, horizontal=True, seed=13, base=hexa("#7b5536"), dark=hexa("#553a24"), board=63)
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.stroke()
    for y in (y0 + 70, y1 - 70):                             # iron straps with rivets
        toon(cr, lambda c, y=y: c.rectangle(x0, y - 14, x1 - x0, 28), hexa("#2c2d2f"), hexa("#1a1b1c"), (0, -4),
             (1, 0.8, 0.6, 0.25), (0, -4), lw=3)
        for x in range(int(x0) + 20, int(x1), 60):
            cr.set_source_rgba(0.5, 0.5, 0.5, 1)
            cr.arc(x, y, 4, 0, 2 * math.pi)
            cr.fill()
    cr.set_source_rgba(0.15, 0.15, 0.16, 1)                  # the ring
    cr.set_line_width(9)
    cr.arc(300, 570, 30, 0, 2 * math.pi)
    cr.stroke()
    toon(cr, lambda c: c.rectangle(286, 530, 28, 16), hexa("#2c2d2f"), None, (0, 0), None, lw=3)
    cr.restore()
    toon(cr, lambda c: c.rectangle(x1 - 70, 540 - jump, 70, 44), hexa("#3a3b3e"), hexa("#232427"), (0, -4), None, lw=3)
    toon(cr, lambda c: c.rectangle(x1 - 10, 548, 90, 28), hexa("#5d5f63"), hexa("#3a3b3e"), (0, -4),
         (1, 0.85, 0.6, 0.4), (0, -4), lw=3)                  # the bolt, shut into the floor
    toon(cr, lambda c: c.rectangle(x1 + 20, 530, 40, 64), hexa("#3a3b3e"), hexa("#232427"), (0, -4), None, lw=3)
    if frost > 0:                                            # frost creeping out of the gaps
        cr.set_source_rgba(0.85, 0.95, 1, 0.75 * clamp01(frost))
        cr.set_line_width(2.2)
        for k in range(48):
            side = k % 4
            u = ((k * 0.618) % 1)
            sx, sy = [(x0 + u * (x1 - x0), y0), (x1, y0 + u * (y1 - y0)), (x0 + u * (x1 - x0), y1),
                      (x0, y0 + u * (y1 - y0))][side]
            nx, ny = [(0, -1), (1, 0), (0, 1), (-1, 0)][side]
            L = (20 + 70 * ((k * 0.37) % 1)) * frost
            cr.move_to(sx, sy)
            ex, ey = sx + nx * L + ny * L * 0.3, sy + ny * L + nx * L * 0.3
            cr.line_to(ex, ey)
            for sgn in (-1, 1):
                cr.move_to(sx + (ex - sx) * 0.5, sy + (ey - sy) * 0.5)
                cr.line_to(sx + (ex - sx) * 0.5 + (nx + sgn * ny) * L * 0.3, sy + (ey - sy) * 0.5 + (ny + sgn * nx) * L * 0.3)
            cr.stroke()
        glow(cr, 360, 570, 300, (0.7, 0.85, 1), 0.15 * frost)
    for b in dust:                                           # dust shaken up
        d = t - b
        if 0 <= d < 1.2:
            for k in range(14):
                a = k * 2.399
                px = 360 + (200 + 30 * (k % 3)) * math.cos(a)
                py = 570 + (200 + 30 * (k % 3)) * math.sin(a) - 60 * d
                cr.set_source_rgba(0.85, 0.75, 0.6, 0.6 * (1 - d / 1.2))
                cr.arc(px + 20 * d * math.cos(a), py, 2.5, 0, 2 * math.pi)
                cr.fill()
    if boots:                                                # your boots, at the edge of the hatch
        for k, bx in enumerate((250, 450)):
            jx = 2 * math.sin(t * 37 + k) * tremble
            toon(cr, lambda c, bx=bx, jx=jx: tk.curve(c, [(bx - 60 + jx, H + 40), (bx - 66 + jx, 980), (bx - 50 + jx, 870),
                                                          (bx + jx, 840), (bx + 50 + jx, 870), (bx + 66 + jx, 980),
                                                          (bx + 60 + jx, H + 40)]),
                 hexa("#3d2a1b"), hexa("#24180f"), (-6, -5), WARM_RIM, (0, -6), lw=5)
            cr.set_source_rgba(0.85, 0.8, 0.7, 0.8)          # laces
            cr.set_line_width(3)
            for j in range(4):
                cr.move_to(bx - 20 + jx, 920 + j * 32)
                cr.line_to(bx + 20 + jx, 936 + j * 32)
                cr.move_to(bx + 20 + jx, 920 + j * 32)
                cr.line_to(bx - 20 + jx, 936 + j * 32)
            cr.stroke()
            toon(cr, lambda c, bx=bx, jx=jx: c.rectangle(bx - 70 + jx, 1180, 140, 140), hexa("#6d6a4c"),
                 hexa("#4a4833"), (-6, -5), None, lw=5)      # ranger trousers
    if hand > 0:
        tk.hand_point(cr, 690 - 90 * hand, 1180 - 560 * hand, 1.25, t, tremble=tremble, sleeve=tk.RANGER[:2])


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "hook_face"), (B["t2"].start - 0.2, "radio"), (B["t3"].start - 0.2, "face_t3"),
        (A("t3", "Alone.") - 0.1, "tower_ext"), (B["t4"].start - 0.2, "logbook"), (B["t6"].start - 0.2, "clock"),
        (B["t7"].start - 0.2, "gen"), (B["t8"].start - 0.2, "trees"), (B["t10"].start - 0.2, "face_t10"),
        (B["t11"].start - 0.2, "hatch_steps"), (B["t12"].start - 1.45, "boots"), (B["t13"].start - 0.2, "radio2"),
        (B["t15"].start - 0.2, "face_t15"), (B["t16"].start - 0.2, "hatch_frost"), (B["t17b"].start - 0.2, "hand_bolt"),
        (B["t17c"].start - 0.2, "gen_dark"), (B["t18"].start - 0.2, "choice"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    flashes = [B["t9"].start + 0.4, B["t16"].start + 0.2]
    fl = flash_level(t, flashes)
    knock = B["t12"].start - 1.25                             # three knocks, 0.32 s apart (the "knock" effect)
    knocks = [knock, knock + 0.32, knock + 0.64]
    steps = [B["t11"].start + 0.2 + k2 * 0.75 for k2 in range(4)]
    torches = [(A("t8", "torches"), 2), (A("t9", "Five."), 5), (A("t9", "nine."), 9), (A("t9", "many"), 23)]
    n_torch, bumped = 0, None
    for at, v in torches:
        if t >= at:
            n_torch, bumped = v, at
    rim_c = COLD_RIM if fl < 0.2 else (0.9, 0.95, 1, 1)
    coat = tk.RANGER

    def face(f, look=(0.0, 0.0), tremble=0.0, sweat=0.0, turn=0.0, y=930, s=1.42, x=360):
        hud2d.blurred(cr, lambda c: cabin(c, t, flash=fl), sigma=8)
        tk.you_bust(cr, x, y, s, f, t, look=look, turn=turn, rim=rim_c, rim_from=(-10, -4), sweat=sweat,
                    tremble=tremble, coat=coat)

    cr.save()
    if name == "hook_face":
        camera(cr, t, s0, s1, 1.0, 1.07)
        face(tk.face_mix("uneasy", "alarmed", seg(t, A("t1", "yours.") - 0.2, A("t1", "yours.") + 0.2)),
             look=(0.5, 0.9))
        glow(cr, 560, 1280, 420, (1, 0.15, 0.1), 0.35 * (0.7 + 0.3 * (noise(t * 15, 1) > 0)))   # the RX light below
    elif name in ("radio", "radio2"):
        camera(cr, t, s0, s1, 1.0, 1.1, cy=760)
        rx = (B["t2"].start - 0.1 <= t <= B["t2"].end + 0.2 if name == "radio"
              else B["t13"].start <= t <= B["t14"].end + 0.2)
        radio_scene(cr, t, 1.0 if rx else 0.0, flash=fl)
    elif name in ("face_t3", "face_t10", "face_t15"):
        camera(cr, t, s0, s1, 1.04, 1.12, shake=1.0 + (name != "face_t3"))
        if name == "face_t3":
            face(tk.face_mix("alarmed", "terror", seg(t, A("t3", "nine.") - 0.2, A("t3", "nine.") + 0.3)),
                 look=(-0.6 * math.sin(t * 2), 0), sweat=0.5)
        elif name == "face_t10":
            face(tk.face_mix("terror", "terror", 0), look=(0.6, 0.8), tremble=0.6, sweat=1.0)
        else:
            face(tk.face_mix("terror", "terror", 0), look=(0, 0.2), tremble=0.8, sweat=1.0)
    elif name == "tower_ext":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=500)
        tower_ext(cr, t, fl, measure=seg(t, A("t3", "Thirty") - 0.1, A("t3", "metres", end=True)))
    elif name == "logbook":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600)
        logbook(cr, t, seg(t, A("t5", "Never"), A("t5", "three", end=True)),
                seg(t, A("t5", "Never", nth=2), A("t5", "hatch.", end=True)))
    elif name == "clock":
        camera(cr, t, s0, s1, 1.0, 1.12, cy=560)
        clock(cr, t)
    elif name in ("gen", "gen_dark"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=640)
        if name == "gen":
            dip = A("t7", "lights") <= t <= A("t7", "out.", end=True) + 0.1 and noise(t * 19, 2) > 0.1
            gen_panel(cr, t, fuel=0.14, on=0.25 if dip else 1.0)
        else:
            dark = A("t17c", "dark") - 0.05
            on = 1.0 if t < dark else (0.0 if t < dark + 0.9 else 0.3 + 0.7 * (noise(t * 13, 5) > 0.3))
            gen_panel(cr, t, fuel=0.05, on=on)
    elif name == "trees":
        camera(cr, t, s0, s1, 1.0, 1.15, cy=700)
        trees_down(cr, t, n_torch, fl)
    elif name in ("hatch_steps", "boots", "hatch_frost", "hand_bolt", "choice"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600, shake=1.0 + 1.5 * (name == "boots"))
        light = {"hatch_steps": seg(t, s0, B["t11"].end), "boots": 1.0, "hatch_frost": 0.6 - 0.4 * seg(t, s0, s1),
                 "hand_bolt": 0.25, "choice": 0.25}[name]
        frost = {"hatch_frost": seg(t, A("t16", "voice"), B["t17"].end), "hand_bolt": 1.0, "choice": 1.0}.get(name, 0.0)
        hatch(cr, t, light=light, frost=frost, bumps=knocks, dust=steps + knocks, boots=name == "boots",
              hand=seg(t, s0 + 0.2, s0 + 1.6) if name == "hand_bolt" else 0.0, tremble=0.8)
        if name == "choice":
            tk.you_back(cr, 600, 1330, 1.15, t, rim=WARM_RIM, rim_from=(-10, 0), coat=coat)
        if fl > 0:
            glow(cr, 360, 0, 900, BOLT, 0.25 * fl)
    cr.restore()
    hud.finish(cr, t, flash_at=flashes, vig=0.55, grain=0.06)
    minute = 14 + int(max(0, t - B["t6"].start) / 20)
    fuel = ("FUEL", "1 HR", "warn") if t < B["t17c"].start else ("FUEL", "< 1 HR", "bad", B["t17c"].start)
    tor = ("TORCHES", "MANY" if n_torch > 9 else str(n_torch), "bad" if n_torch >= 9 else "warn" if n_torch else None,
           bumped) if bumped else ("TORCHES", "0", None)
    hud2d.stats(cr, t, [("TIME", f"3:{minute:02d} AM", None), fuel, tor])
    hud2d.hook(cr, t, [("THE VOICE ON", False), ("THE RADIO", False), ("IS YOURS", True)],
               end=B["t1"].end + 0.15, y=270)
    hud2d.rule_tag(cr, t, A("t5", "Never"), B["t5"].end + 0.4, "RULE: NO RADIO AFTER 3 AM. NO HATCH.", y=190)
    hud2d.stamp(cr, t, A("t15", "Two"), B["t15"].end + 0.4, ["FUEL: 1 HOUR", "HELP: 2 HOURS"], y=300)
    hud2d.bubble(cr, t, B["t2"].start, B["t2"].end, "Tower 9, can anyone hear me? Something's climbing the ladder.",
                 360, 300, (470, 560), creepy=True)
    hud2d.bubble(cr, t, B["t10"].start, B["t10"].end, "Please. Open the hatch. They're right behind me.",
                 330, 270, (700, 430), creepy=True)          # from the radio, off to the right
    hud2d.bubble(cr, t, B["t14"].start, B["t14"].end, "Tower 9, this is base. Don't open anything. Help is two hours "
                 "out.", 360, 300, (470, 560))
    hud2d.bubble(cr, t, B["t17"].start, B["t17"].end, "Please. I'm so cold.", 360, 260, (360, 380), creepy=True)
    hud2d.ab_card(cr, t, A("t19", "open"), "OPEN IT", "KEEP SHUT", kicker="TOWER 9 · NIGHT 1 · YOUR CHOICE",
                  decides="Night 2")
    hud2d.captions(cr, t, tl, KEY, skip=("t2", "t10", "t14", "t17"))
    cue("rain", t, B["t1"].end + 0.1, tl.total)              # after the hook line: right after "crackled" it read as "-s"
    cue("generator", t, 0.0, tl.total)
    cue("static", t, 0.0, 0.3)                                  # from the first frame, before "crackled"
    cue("static", t, B["t2"].start - 0.2, 0.3)
    cue("static", t, B["t10"].start - 0.2, 0.3)
    cue("static", t, A("t13", "again.", end=True) + 0.03, 0.32)     # in the pause, not on "crackles"
    cue("static", t, B["t14"].start - 0.2, 0.3)
    for at in (B["t9"].end + 0.05, B["t16"].end + 0.05):     # thunder follows its lightning, between lines
        cue("thunder", t, at)
    for at in steps:
        cue("ladder_step", t, at)
    cue("knock", t, knock)   # in the silence before the line (on the words, "knocks" was heard as "knots")
    cue("heartbeat", t, B["t15"].start, B["t17c"].end - B["t15"].start)
    cue("riser", t, B["t18"].start, B["t19"].start - B["t18"].start)
