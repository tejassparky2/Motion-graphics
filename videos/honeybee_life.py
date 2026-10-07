"""What if you were a honeybee? A worker's whole life in about 70 seconds: second-person, deadpan, in the polished
look (motion/polish.py + motion/bees.py). Format inspired by the owner's reference video; script, jokes and art are
our own. Every fact is checked in out/research_honeybee.md.
"""
import math
import random

from motion.bees import BLUSH, GOLD, LIMB, OUTLINE, bee, comb_cell, larva, wasp
from motion.engine import W, H, cairo, clamp01, cue, ease_out, hexc, lerp, seg
from motion.polish import (WHITE, alpha, appear, bokeh, bold_text, camera, captions, counter, ellipse, enter,
                           ground_shadow, hexagon, light_rays, lin, paint, particles, put, rad, rrect, shade, sign,
                           smooth, soft_disc, soft_rrect, sprite, stamp, stroke_line, text_path, vignette)
from motion.kit import whip

NARRATOR = dict()
TAIL = 0.9

SCRIPT = [
    dict(id="h1", scene="hook", text="What if you were a honeybee?"),
    dict(id="h2", scene="hook", text="Spoiler. You're a girl. And you have about six weeks to live.", gap=0.35),
    dict(id="h3", scene="hive", text="You live with up to [sixty thousand|60,000] bees. Almost all of them are your "
                                     "sisters."),
    dict(id="h4", scene="queen", text="Your mom is the queen. She lays up to [two thousand|2,000] eggs."),
    dict(id="h5", scene="queen", text="A day.", gap=0.45),
    dict(id="h6", scene="clean", text="Day one. You're born. Your first job? Cleaning."),
    dict(id="h7", scene="clean", text="Starting with the room you were born in.", gap=0.3),
    dict(id="h8", scene="nanny", text="A few days later, you're a nanny. You feed the babies all day."),
    dict(id="h9", scene="wax", text="Then you start making wax. Out of your belly. And you build the house with it."),
    dict(id="h10", scene="guard", text="Next job: security. If a bee smells wrong, it doesn't get in."),
    dict(id="h11", scene="outside", text="At about three weeks old, you finally go outside."),
    dict(id="h12", scene="outside", text="Your wings beat over two hundred times a second. You visit up to a "
                                         "hundred flowers on one trip."),
    dict(id="h13", scene="dance", text="Found good flowers? You don't text your sisters. You dance."),
    dict(id="h14", scene="dance", text="The angle of your dance points to the food, using the sun as a compass."),
    dict(id="h15", scene="drones", text="Meanwhile. Your brothers."),
    dict(id="h16", scene="drones", text="They don't clean. They don't make honey. They can't even sting."),
    dict(id="h17", scene="drones", text="They have one job. Mating with a queen."),
    dict(id="h18", scene="drones", text="The ones who succeed? Die right after.", gap=0.4),
    dict(id="h19", scene="autumn", text="And in autumn, the sisters throw the rest out of the house."),
    dict(id="h20", scene="sunset", text="Back to you. You fly until your wings wear out. And one day, you just don't "
                                        "come home."),
    dict(id="h21", scene="spoon", text="Your whole life's work? One twelfth of a teaspoon of honey."),
    dict(id="h22", scene="spoon", text="One teaspoon is the life's work of twelve bees."),
    dict(id="h23", scene="tea", text="And someone stirs it into their tea.", gap=0.4),
    dict(id="h24", scene="end", text="So. Would you rather be the worker? Or the drone?", pace=0.95),
]

METADATA = dict(
    title="What If You Were a Honeybee? 🐝 (Your Whole Life in 70 Seconds)",
    alt_titles=["You're a Bee. You Have 6 Weeks to Live. 🐝", "The Brutal Life of a Honeybee (Explained Funny) 🍯"],
    description="""What if you were a honeybee? Spoiler: you're a girl, and you have about six weeks to live. 🐝

You live with up to 60,000 bees, almost all of them your sisters. Mom is the queen: she lays up to 2,000 eggs a day.
Day one, you're born and start cleaning, starting with your own room. Then you're a nanny, then you make wax out of your belly and build the house, then you guard the door. At about three weeks old you finally go outside: over 200 wing beats a second, up to 100 flowers a trip, and you tell your sisters where the food is by dancing.

Your brothers, the drones, don't clean, don't make honey and can't sting. Their one job is mating with a queen, and the ones who succeed die right after. In autumn, the sisters throw the rest out.

You work until your wings wear out. Your whole life's work: about 1/12 of a teaspoon of honey. So one teaspoon is the life's work of 12 bees. 🍯

Sources: National Honey Board; Wikipedia (Worker bee, Drone, Waggle dance); American Bee Journal. Full list: worker lifespan 5–7 weeks in summer, colony up to 60,000, queen up to 2,000 eggs a day, wing beats 200–230 per second, 50–100 flowers per trip.

💬 So would you rather be the worker, or the drone? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, animated in under a minute.""",
    hashtags=["#Bees", "#Animals", "#WhatIf"],
    tags=["what if you were a bee", "honeybee", "honey bee facts", "worker bee", "drone bee", "queen bee",
          "bee life cycle", "animal facts", "insects", "interestingly strange"],
    pinned_comment="Worker or drone? Pick one and defend it 👇🐝",
)

# ---------------------------------------------------------------- palette
PINK = hexc("#ff6fa5")
RED = hexc("#e8473f")
GREEN = hexc("#3fbf6a")
BLUE = hexc("#4aa3f0")
HONEY = hexc("#ffb21f")
AMBER = hexc("#c8770c")
WOOD = hexc("#b9824a")
CREAM = hexc("#fff4dc")
MAUVE = hexc("#9b6bd6")

HERO = dict(s=1.25)


# ---------------------------------------------------------------- backgrounds (cached, screen space)
def _meadow_layer(mood):
    skies = {"day": [(0, hexc("#5fb8ff")), (0.42, hexc("#a8dcff")), (0.6, hexc("#fff0c4"))],
             "sunset": [(0, hexc("#ff7f6a")), (0.35, hexc("#ffb27a")), (0.6, hexc("#ffe2a8"))],
             "autumn": [(0, hexc("#ffc36b")), (0.4, hexc("#ffdca0")), (0.6, hexc("#fff0cc"))]}[mood]
    grounds = {"day": (hexc("#97d86c"), hexc("#4e9e3a")), "sunset": (hexc("#c5b45a"), hexc("#6f6a2c")),
               "autumn": (hexc("#d9a64e"), hexc("#94652a"))}[mood]
    hills = {"day": (hexc("#b9e39a"), hexc("#8fcf72")), "sunset": (hexc("#e0b27c"), hexc("#b8925c")),
             "autumn": (hexc("#e8b878"), hexc("#cf9a52"))}[mood]

    def draw(c):
        c.rectangle(0, 0, W, H)
        c.set_source(lin(0, 0, 0, H, skies))
        c.fill()
        sx, sy = (520, 300) if mood != "sunset" else (360, 720)
        c.set_source(rad(sx, sy, 520, [(0, (1, 0.97, 0.85, 0.85)), (0.25, (1, 0.9, 0.6, 0.35)), (1, (1, 0.9, 0.6, 0))]))
        c.rectangle(0, 0, W, H)
        c.fill()
        c.arc(sx, sy, 70, 0, 2 * math.pi)
        c.set_source(rad(sx, sy, 70, [(0, (1, 1, 0.92, 1)), (1, (1, 0.93, 0.6, 1))]))
        c.fill()
        for k, (yy, amp, col) in enumerate(((720, 50, hills[0]), (770, 36, hills[1]))):
            c.move_to(-20, H)
            for x in range(-20, W + 41, 40):
                c.line_to(x, yy - amp * (0.5 + 0.5 * math.sin(x / 140.0 + k * 2)))
            c.line_to(W + 20, H)
            c.close_path()
            c.set_source_rgba(*col)
            c.fill()
        c.rectangle(0, 805, W, H)
        c.set_source(lin(0, 805, 0, H, [(0, grounds[0]), (1, grounds[1])]))
        c.fill()
        rng = random.Random(7)
        cols = [hexc("#ffffff"), hexc("#ffd84d"), hexc("#ff8fb5"), hexc("#b98cff")]
        for _ in range(260):
            x, y = rng.random() * W, 812 + (rng.random() ** 1.6) * 460
            r = 2 + (y - 800) / 120
            c.arc(x, y, r, 0, 2 * math.pi)
            c.set_source_rgba(*alpha(cols[rng.randrange(4)], 0.85))
            c.fill()
    return draw


def meadow(cr, t, mood="day", rays=True):
    put(cr, sprite(("meadow", mood), W, H, _meadow_layer(mood)), 0, 0)
    if rays and mood == "day":
        light_rays(cr, t, 520, 300, n=6, a=0.07)
    bokeh(cr, t, 11, 16, [hexc("#ffffff"), hexc("#fff3b0")], rmin=10, rmax=40, area=(0, 0, W, 760),
          alpha_=(0.12, 0.3))
    particles(cr, t, 3, 26, (1, 0.95, 0.7, 0.7), area=(0, 0, W, 900), r=(1.5, 3.2), speed=10)


def _fg_flower_draw(col):
    def draw(c):
        for k in range(6):
            a = k * math.pi / 3
            ellipse(c, 150 + 70 * math.cos(a), 150 + 70 * math.sin(a), 66, 40, a)
            c.set_source_rgba(*col)
            c.fill()
        c.arc(150, 150, 46, 0, 2 * math.pi)
        c.set_source_rgba(*hexc("#ffcf3f"))
        c.fill()
    return draw


def dof_flowers(cr, t, mood="day"):
    """Big out-of-focus flowers in the foreground corners (depth of field)."""
    cols = {"day": (hexc("#ff8fb5"), hexc("#fff4fa")), "sunset": (hexc("#ff9a6b"), hexc("#ffd8b0")),
            "autumn": (hexc("#ff9a3c"), hexc("#ffd28a"))}[mood]
    for k, (x, y, sz, col) in enumerate(((-120, 1010, 1.25, cols[0]), (560, 1080, 1.05, cols[1]))):
        spr = sprite(("dof", mood, k), 300, 300, _fg_flower_draw(col), sigma=14, scale=0.5)
        put(cr, spr, x + math.sin(t * 0.6 + k) * 10, y + math.cos(t * 0.5 + k) * 6, a=0.85, size=sz)


def flower(cr, t, x, y, s=1.0, col=hexc("#ff8fb5"), stem=160, seed=0):
    sway = math.sin(t * 1.4 + seed) * 0.04
    cr.save()
    cr.translate(x, y + stem * s)
    cr.rotate(sway)
    stroke_line(cr, [(0, 0), (8 * s, -stem * s * 0.5), (0, -stem * s)], 9 * s, hexc("#3f8f3a"))
    ellipse(cr, 18 * s, -stem * s * 0.45, 26 * s, 11 * s, -0.5)
    paint(cr, lin(0, -stem * s * 0.6, 0, -stem * s * 0.3, [(0, hexc("#7fd36a")), (1, hexc("#3f8f3a"))]), OUTLINE,
          3.5)
    cr.translate(0, -stem * s)
    for k in range(6):
        a = k * math.pi / 3 + seed
        ellipse(cr, 34 * s * math.cos(a), 34 * s * math.sin(a), 30 * s, 19 * s, a)
        paint(cr, rad(0, 0, 70 * s, [(0, shade(col, 0.55)), (1, col)]), OUTLINE, 3.5)
    cr.arc(0, 0, 21 * s, 0, 2 * math.pi)
    paint(cr, rad(-6 * s, -6 * s, 24 * s, [(0, hexc("#fff0a0")), (1, hexc("#f2a81d"))]), OUTLINE, 3.5)
    for k in range(7):
        a = k * 0.9 + seed
        cr.arc(9 * s * math.cos(a), 9 * s * math.sin(a), 2.2 * s, 0, 2 * math.pi)
        paint(cr, hexc("#c9780c"), None, 0)
    cr.restore()


def _hive_layer(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#a8640f")), (0.5, hexc("#7a440a")), (1, hexc("#3c2006"))]))
    c.fill()
    rng = random.Random(4)
    r = 50
    for row in range(-1, 18):
        for col_ in range(-1, 9):
            cx = col_ * r * 1.732 + (row % 2) * r * 0.866
            cy = row * r * 1.5
            comb_cell(c, cx, cy, r, rng.choice(["honey", "honey", "capped", "empty"]))


def hive(cr, t):
    put(cr, sprite(("hive",), W, H, _hive_layer, sigma=3.5, scale=0.5), 0, 0)
    cr.rectangle(0, 0, W, H)
    cr.set_source(rad(W / 2, H * 0.42, H * 0.7, [(0, (1, 0.8, 0.4, 0.18)), (0.6, (0.3, 0.15, 0.0, 0.2)),
                                                 (1, (0.12, 0.05, 0.0, 0.55))]))
    cr.fill()
    bokeh(cr, t, 21, 14, [hexc("#ffd36b"), hexc("#ffefb0")], rmin=12, rmax=46, speed=4, alpha_=(0.10, 0.24))
    particles(cr, t, 8, 18, (1, 0.85, 0.5, 0.6), r=(1.5, 3), speed=6)


def kitchen(cr, t):
    def draw(c):
        c.rectangle(0, 0, W, H)
        c.set_source(lin(0, 0, 0, H, [(0, hexc("#ffe9cf")), (0.55, hexc("#f7d2a6")), (1, hexc("#e6b583"))]))
        c.fill()
        c.arc(560, 260, 420, 0, 2 * math.pi)
        c.set_source(rad(560, 260, 420, [(0, (1, 1, 0.95, 0.75)), (1, (1, 1, 0.9, 0))]))
        c.fill()
        c.rectangle(0, 760, W, H)
        c.set_source(lin(0, 760, 0, H, [(0, hexc("#c98a52")), (1, hexc("#8a5428"))]))
        c.fill()
        for k in range(9):
            c.move_to(0, 800 + k * 52)
            c.curve_to(240, 790 + k * 52, 480, 812 + k * 52, W, 798 + k * 52)
            c.set_source_rgba(0.35, 0.18, 0.05, 0.18)
            c.set_line_width(2)
            c.stroke()
    put(cr, sprite(("kitchen",), W, H, draw), 0, 0)
    bokeh(cr, t, 31, 10, [hexc("#ffffff"), hexc("#ffe7b8")], rmin=20, rmax=60, speed=3, area=(0, 0, W, 760))


# ---------------------------------------------------------------- props
def mop(cr, hx, hy):
    stroke_line(cr, [(hx, hy - 70), (hx, hy + 60)], 7, hexc("#8a5a2e"), curve=False)
    for k in range(7):
        stroke_line(cr, [(hx, hy + 56), (hx - 24 + k * 8, hy + 92 + (k % 2) * 6)], 6, hexc("#9ad7ff"))


def spoon(cr, hx, hy):
    stroke_line(cr, [(hx - 10, hy + 8), (hx + 50, hy - 10)], 6, hexc("#b8c0c8"), curve=False)
    ellipse(cr, hx + 62, hy - 14, 16, 10, -0.3)
    paint(cr, lin(0, hy - 24, 0, hy, [(0, hexc("#ffffff")), (1, hexc("#9aa4ae"))]), OUTLINE, 3)
    ellipse(cr, hx + 62, hy - 15, 9, 5, -0.3)
    paint(cr, HONEY, None, 0)


def phone(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(-0.12)
    rrect(cr, -48, -86, 96, 172, 16)
    paint(cr, lin(0, -86, 0, 86, [(0, hexc("#3a3f52")), (1, hexc("#151821"))]), OUTLINE, 5)
    rrect(cr, -40, -72, 80, 140, 8)
    paint(cr, lin(0, -72, 0, 68, [(0, hexc("#7fd0ff")), (1, hexc("#3c7fd8"))]), None, 0)
    rrect(cr, -30, -50, 52, 22, 10)
    paint(cr, WHITE, None, 0)
    rrect(cr, -14, -18, 46, 22, 10)
    paint(cr, hexc("#5ee08a"), None, 0)
    cr.restore()


def red_x(cr, t, start, x, y, r=40):
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.25))
    cue("hit", t, start)
    for d in (-1, 1):
        stroke_line(cr, [(x - r, y - r * d), (x - r + 2 * r * u, y - r * d + 2 * r * d * u)], 13, OUTLINE, curve=False)
        stroke_line(cr, [(x - r, y - r * d), (x - r + 2 * r * u, y - r * d + 2 * r * d * u)], 8, RED, curve=False)


def check(cr, t, start, x, y, r=36):
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.25))
    cue("pop", t, start)
    pts = [(x - r, y), (x - r * 0.25, y + r * 0.7), (x + r, y - r * 0.8)]
    pts = pts[:2] + [(lerp(pts[1][0], pts[2][0], u), lerp(pts[1][1], pts[2][1], u))]
    stroke_line(cr, pts, 15, OUTLINE, curve=False)
    stroke_line(cr, pts, 9, GREEN, curve=False)


def hearts(cr, t, start, x, y, n=4, seed=1, col=PINK):
    if t < start:
        return
    rng = random.Random(seed)
    for k in range(n):
        u = seg(t, start + k * 0.12, start + k * 0.12 + 1.4)
        if u <= 0 or u >= 1:
            continue
        hx = x + rng.uniform(-60, 60) + math.sin(u * 6 + k) * 10
        hy = y - u * 160
        s = 0.6 + 0.6 * math.sin(u * math.pi)
        cr.save()
        cr.translate(hx, hy)
        cr.scale(s, s)
        cr.move_to(0, 14)
        cr.curve_to(-30, -6, -14, -30, 0, -14)
        cr.curve_to(14, -30, 30, -6, 0, 14)
        cr.close_path()
        paint(cr, alpha(col, 1 - u * 0.6), OUTLINE, 3)
        cr.restore()


def sparkles(cr, t, start, x, y, n=6, seed=2, col=WHITE, spread=80):
    if t < start:
        return
    rng = random.Random(seed)
    for k in range(n):
        u = seg(t, start + k * 0.05, start + k * 0.05 + 0.6)
        if u <= 0 or u >= 1:
            continue
        a = rng.uniform(0, 6.28)
        d = spread * ease_out(u)
        sx, sy = x + math.cos(a) * d, y + math.sin(a) * d
        r = 12 * math.sin(u * math.pi)
        cr.move_to(sx, sy - r)
        cr.line_to(sx + r * 0.3, sy - r * 0.3)
        cr.line_to(sx + r, sy)
        cr.line_to(sx + r * 0.3, sy + r * 0.3)
        cr.line_to(sx, sy + r)
        cr.line_to(sx - r * 0.3, sy + r * 0.3)
        cr.line_to(sx - r, sy)
        cr.line_to(sx - r * 0.3, sy - r * 0.3)
        cr.close_path()
        paint(cr, col, None, 0)


def arrow(cr, x0, y0, x1, y1, col=WHITE, lw=10):
    stroke_line(cr, [(x0, y0), ((x0 + x1) / 2 + 20, (y0 + y1) / 2 - 20), (x1, y1)], lw + 6, OUTLINE)
    stroke_line(cr, [(x0, y0), ((x0 + x1) / 2 + 20, (y0 + y1) / 2 - 20), (x1, y1)], lw, col)
    a = math.atan2(y1 - ((y0 + y1) / 2 - 20), x1 - ((x0 + x1) / 2 + 20))
    cr.move_to(x1 + 22 * math.cos(a), y1 + 22 * math.sin(a))
    cr.line_to(x1 + 20 * math.cos(a + 2.4), y1 + 20 * math.sin(a + 2.4))
    cr.line_to(x1 + 20 * math.cos(a - 2.4), y1 + 20 * math.sin(a - 2.4))
    cr.close_path()
    paint(cr, col, OUTLINE, 4)


def bow(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for d in (-1, 1):
        cr.move_to(0, 0)
        cr.curve_to(d * 30, -26, d * 44, 6, d * 6, 6)
        cr.close_path()
        paint(cr, lin(0, -20, 0, 10, [(0, shade(PINK, 0.3)), (1, PINK)]), OUTLINE, 3.5)
    cr.arc(0, 2, 8, 0, 2 * math.pi)
    paint(cr, shade(PINK, -0.15), OUTLINE, 3)
    cr.restore()


def halo(cr, x, y, s=1.0):
    ellipse(cr, x, y, 34 * s, 10 * s)
    cr.set_source_rgba(1, 0.92, 0.4, 0.95)
    cr.set_line_width(7 * s)
    cr.stroke()


def hive_door(cr, x, y, w=420):
    """The hive's entrance seen from outside: a wooden box face with a dark slot and a landing board."""
    rrect(cr, x - w / 2, y - 420, w, 430, 20)
    paint(cr, lin(0, y - 420, 0, y, [(0, hexc("#f2e2c2")), (1, hexc("#d8bf92"))]), OUTLINE, 6)
    for k in range(4):
        stroke_line(cr, [(x - w / 2 + 10, y - 400 + k * 100), (x + w / 2 - 10, y - 404 + k * 100)], 3,
                    alpha(hexc("#a88a5a"), 0.6), curve=False)
    rrect(cr, x - 130, y - 70, 260, 60, 30)
    paint(cr, lin(0, y - 70, 0, y - 10, [(0, hexc("#140a04")), (1, hexc("#3a2410"))]), OUTLINE, 5)
    rrect(cr, x - w / 2 - 30, y - 8, w + 60, 34, 10)
    paint(cr, lin(0, y - 8, 0, y + 26, [(0, hexc("#e0b47a")), (1, hexc("#a8763c"))]), OUTLINE, 5)


def teaspoon(cr, x, y, s=1.0, fill=0.0, drop=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 70, 260, 0.3)
    smooth(cr, [(-330, 30), (-120, 18), (60, 4), (60, -4), (-120, 6), (-330, 14)])
    paint(cr, lin(0, -4, 0, 30, [(0, hexc("#ffffff")), (0.5, hexc("#c8d0d8")), (1, hexc("#8a949e"))]), OUTLINE, 5)
    ellipse(cr, 150, 0, 110, 62)
    paint(cr, lin(0, -62, 0, 62, [(0, hexc("#ffffff")), (0.6, hexc("#c3ccd5")), (1, hexc("#8a949e"))]), OUTLINE, 6)
    ellipse(cr, 150, 2, 92, 48)
    paint(cr, lin(0, -48, 0, 48, [(0, hexc("#a9b3bd")), (1, hexc("#eef2f5"))]), None, 0)
    if fill > 0:
        cr.save()
        ellipse(cr, 150, 2, 92, 48)
        cr.clip()
        ry = 48 * clamp01(fill)
        ellipse(cr, 150, 2 + 48 - ry, 92 * min(1, 0.4 + fill), ry * 1.05)
        paint(cr, rad(140, 2, 100, [(0, hexc("#ffe08a")), (0.6, HONEY), (1, AMBER)]), None, 0)
        cr.restore()
    if drop > 0:
        r = 9 * drop
        cr.move_to(150, 20 - r * 2.2)
        cr.curve_to(150 + r, 20 - r * 0.6, 150 + r, 20 + r, 150, 20 + r)
        cr.curve_to(150 - r, 20 + r, 150 - r, 20 - r * 0.6, 150, 20 - r * 2.2)
        paint(cr, rad(147, 18, r * 1.6, [(0, hexc("#ffe7a0")), (1, AMBER)]), OUTLINE, 2.5)
    ellipse(cr, 120, -30, 40, 10, -0.15)
    cr.set_source_rgba(1, 1, 1, 0.7)
    cr.fill()
    cr.restore()


def teacup(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 150, 230, 0.32)
    ellipse(cr, 0, 150, 230, 34)
    paint(cr, lin(0, 120, 0, 184, [(0, WHITE), (1, hexc("#d8dee6"))]), OUTLINE, 5)
    cr.arc(190, 20, 56, -1.2, 1.4)
    paint(cr, None, OUTLINE, 22)
    cr.arc(190, 20, 56, -1.2, 1.4)
    paint(cr, None, hexc("#eef2f6"), 12)
    cr.move_to(-190, -60)
    cr.curve_to(-180, 90, -100, 140, 0, 140)
    cr.curve_to(100, 140, 180, 90, 190, -60)
    cr.close_path()
    paint(cr, lin(-190, 0, 190, 0, [(0, hexc("#e9eef4")), (0.4, WHITE), (1, hexc("#c9d2dc"))]), OUTLINE, 6)
    stroke_line(cr, [(-150, 40), (-60, 70), (60, 70), (150, 40)], 8, alpha(PINK, 0.8))
    ellipse(cr, 0, -60, 190, 40)
    paint(cr, rad(-30, -70, 200, [(0, hexc("#e0a35c")), (1, hexc("#8a4a16"))]), OUTLINE, 6)
    for k in range(3):   # steam
        ph = (t * 0.6 + k * 0.33) % 1.0
        sx = -60 + k * 60 + math.sin(t * 2 + k) * 14
        stroke_line(cr, [(sx, -110 - ph * 120), (sx + 18, -150 - ph * 120), (sx - 6, -190 - ph * 120)], 12,
                    (1, 1, 1, 0.45 * math.sin(ph * math.pi)))
    cr.restore()


def suitcase(cr, x, y, s=0.6, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -50, -36, 100, 72, 12)
    paint(cr, lin(0, -36, 0, 36, [(0, hexc("#e8735c")), (1, hexc("#b84a36"))]), OUTLINE, 5)
    rrect(cr, -18, -52, 36, 20, 8)
    paint(cr, None, OUTLINE, 6)
    cr.restore()


def couch(cr, x, y, w=560):
    rrect(cr, x - w / 2, y - 150, w, 120, 40)
    paint(cr, lin(0, y - 150, 0, y - 30, [(0, hexc("#d8743a")), (1, hexc("#a84e1e"))]), OUTLINE, 6)
    rrect(cr, x - w / 2 + 10, y - 60, w - 20, 80, 30)
    paint(cr, lin(0, y - 60, 0, y + 20, [(0, hexc("#ef8a4a")), (1, hexc("#c25e26"))]), OUTLINE, 6)
    for d in (-1, 1):
        rrect(cr, x + d * (w / 2 - 20) - 40, y - 110, 80, 140, 36)
        paint(cr, lin(0, y - 110, 0, y + 30, [(0, hexc("#e27e42")), (1, hexc("#b0561f"))]), OUTLINE, 6)


def honey_cup(cr, hx, hy):
    rrect(cr, hx - 18, hy - 46, 36, 46, 8)
    paint(cr, lin(0, hy - 46, 0, hy, [(0, hexc("#ffe08a")), (1, AMBER)]), OUTLINE, 4)
    stroke_line(cr, [(hx + 6, hy - 46), (hx + 14, hy - 82)], 5, hexc("#ff6fa5"), curve=False)


def calendar(cr, t, start, x, y, top, big, col=RED, s=1.0, end=None):
    """A hanging day card (sign variant): coloured header + big number/word."""
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    if k <= 0.01:
        return
    cue("pop", t, start)
    cr.save()
    cr.translate(x, y + math.sin(t * 2) * 3)
    cr.rotate(0.04 * math.sin(t * 1.6))
    cr.scale(k * s, k * s)
    stroke_line(cr, [(-60, -150), (-50, -76)], 4, OUTLINE, curve=False)
    stroke_line(cr, [(60, -150), (50, -76)], 4, OUTLINE, curve=False)
    soft_rrect(cr, -110, -76, 220, 200, 22, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -110, -86, 220, 200, 22)
    paint(cr, lin(0, -86, 0, 114, [(0, WHITE), (1, hexc("#e9e2d6"))]), OUTLINE, 6)
    cr.save()
    rrect(cr, -110, -86, 220, 200, 22)
    cr.clip()
    cr.rectangle(-110, -86, 220, 58)
    cr.set_source(lin(0, -86, 0, -28, [(0, shade(col, 0.2)), (1, col)]))
    cr.fill()
    cr.restore()
    bold_text(cr, top, 0, -42, 34, WHITE)
    bold_text(cr, big, 0, 82, 96 if len(big) <= 2 else 60, hexc("#2b1d16"), outline=None, shadow=0)
    cr.restore()


def buttons(cr, t, start, labels, y=1040):
    if t < start:
        return
    for k, (lab, col) in enumerate(labels):
        x = 200 if k == 0 else 520
        kk = appear(t, start + k * 0.12)
        if kk <= 0.01:
            continue
        cr.save()
        cr.translate(x, y)
        cr.scale(kk, kk)
        soft_rrect(cr, -130, -42, 260, 92, 46, (0, 0, 0, 0.3), sigma=10)
        rrect(cr, -130, -50, 260, 92, 46)
        paint(cr, lin(0, -50, 0, 42, [(0, shade(col, 0.3)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, lab, 0, 14, 46, WHITE)
        cr.restore()
    cue("pop", t, start)


def tag(cr, t, start, x, y, text, col=HONEY, size=40, end=None):
    """A small floating label with a pointer, e.g. 'YOU'."""
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.3)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 4) * 4)
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, col)
    cr.move_to(-12, 12)
    cr.line_to(12, 12)
    cr.line_to(0, 30)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    cr.restore()


# ---------------------------------------------------------------- crowd sprites
def bee_sprite(kind="worker", eyes="open", mouth="smile", arms=("down", "down"), extra=None):
    def draw(c):
        c.translate(110, 160)
        bee(c, 0.4, 0, 0, 1.0, kind=kind, eyes=eyes, mouth=mouth, arms=arms, bob=False, shadow=False)
        if extra:
            extra(c)
    return sprite(("bee", kind, eyes, mouth, arms, extra is not None), 220, 330, draw)


def crowd(cr, t, rows, seed=3, eyes="open", mouth="smile", watch=None):
    rng = random.Random(seed)
    for (y, n, s, x0, x1) in rows:
        for k in range(n):
            x = lerp(x0, x1, k / max(1, n - 1)) + rng.uniform(-12, 12)
            ph = rng.random() * 6.28
            e = rng.choice([eyes, eyes, "happy"]) if eyes == "open" else eyes
            spr = bee_sprite(eyes=e, mouth=mouth)
            put(cr, spr, x - 110 * s, y - 160 * s + math.sin(t * 2.4 + ph) * 3, size=s)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    meadow(cr, t)
    cam = camera(t, [(0, (1.0, 360, 640)), (A("h2", "six"), (1.12, 360, 600))])
    cr.save()
    enter(cr, cam)
    flower(cr, t, 130, 700, 1.0, hexc("#ff8fb5"), seed=1)
    flower(cr, t, 600, 640, 1.15, hexc("#b98cff"), seed=2)
    fly_in = ease_out(seg(t, 0.0, 1.0))
    x = lerp(860, 360, fly_in)
    shock = t >= A("h2", "six")
    girl = t >= A("h2", "girl.")
    bee(cr, t, x, 600, HERO["s"], fly=True, eyes="wide" if shock else ("happy" if girl else "open"),
        mouth="open" if shock else ("grin" if girl else "smile"), arms=("face", "face") if shock else ("wave", "down"),
        look=(-0.3, 0.1) if not shock else (0, 0))
    if girl:
        bow(cr, x + 34, 600 - 128 * HERO["s"] + math.sin(t * 6) * 7, 0.9)
    cr.restore()
    dof_flowers(cr, t)
    sign(cr, t, 0.05, 360, 225, "WHAT IF YOU WERE", size=54, end=A("h2") - 0.1)
    sign(cr, t, A("h1", "honeybee?"), 360, 335, "A HONEYBEE?", col=HONEY, size=74, rot=0.03, end=A("h2") - 0.1)
    stamp(cr, t, A("h2"), 360, 270, "SPOILER!", end=A("h2", "girl.") - 0.05)
    sign(cr, t, A("h2", "girl."), 360, 250, "IT'S A GIRL!", col=PINK, size=64, end=A("h2", "six") - 0.05)
    sign(cr, t, A("h2", "six"), 360, 250, "6 WEEKS", col=RED, size=78, sub="TO LIVE", sub_col=WHITE)
    vignette(cr)


def scene_hive(cr, t, tl):
    A = tl.at
    hive(cr, t)
    cam = camera(t, [(A("h3") - 0.3, (1.25, 360, 700)), (A("h3", "60,000"), (1.0, 360, 640))], dur=1.2)
    cr.save()
    enter(cr, cam)
    crowd(cr, t, [(430, 6, 0.4, 70, 650), (530, 6, 0.45, 40, 680), (640, 2, 0.5, 70, 650)], seed=5)
    bee(cr, t, 360, 760, 1.05, eyes="happy" if t >= A("h3", "sisters.") else "open", mouth="grin", arms=("wave", "down"))
    cr.restore()
    hearts(cr, t, A("h3", "sisters."), 200, 520, 5, seed=3)
    hearts(cr, t, A("h3", "sisters.") + 0.2, 540, 500, 5, seed=4)
    tag(cr, t, A("h3") + 0.2, 360, 600, "YOU")
    counter(cr, t, A("h3", "60,000"), 360, 250, 60000, size=104, dur=1.1, sub="BEES IN ONE HIVE")
    sign(cr, t, A("h3", "sisters."), 360, 380, "ALL SISTERS", col=PINK, size=50, rot=-0.04)
    vignette(cr, 0.45)


def scene_queen(cr, t, tl):
    A = tl.at
    hive(cr, t)
    cam = camera(t, [(A("h4") - 0.3, (1.0, 360, 640)), (A("h5"), (1.15, 360, 620))])
    cr.save()
    enter(cr, cam)
    for k in range(8):   # a row of comb cells; eggs appear faster and faster
        cx, cy = 70 + k * 84, 865
        comb_cell(cr, cx, cy, 46, "empty")
        st = A("h4", "lays") + 0.35 * k ** 0.8
        if t >= st:
            sc = appear(t, st, 0.25)
            ellipse(cr, cx, cy, 7 * sc, 14 * sc, 0.3)
            paint(cr, rad(cx - 2, cy - 4, 14, [(0, WHITE), (1, hexc("#efe6d2"))]), OUTLINE, 2)
    bee(cr, t, 330, 520, 1.45, kind="queen", eyes="half", mouth="smug", arms=("hips", "hips"))
    hero_x = lerp(820, 600, ease_out(seg(t, A("h4") + 0.2, A("h4") + 0.9)))
    shock = t >= A("h5")
    bee(cr, t, hero_x, 640, 0.8, eyes="wide" if shock else "open", mouth="open" if shock else "smile",
        arms=("face", "face") if shock else ("down", "down"), look=(-0.6, 0), squash=0.3 if shock else 0)
    cr.restore()
    sign(cr, t, A("h4", "queen."), 230, 190, "MOM", col=MAUVE, size=58, rot=-0.06, end=A("h4", "lays") - 0.05)
    counter(cr, t, A("h4", "2,000"), 360, 210, 2000, size=104, dur=0.9, sub="EGGS")
    stamp(cr, t, A("h5"), 360, 330, "A DAY!", size=86)
    vignette(cr, 0.45)


def comb_wall(cr, rows, cols, x0, y0, r, contents):
    for row in range(rows):
        for c in range(cols):
            cx = x0 + c * r * 1.732 + (row % 2) * r * 0.866
            cy = y0 + row * r * 1.5
            comb_cell(cr, cx, cy, r, contents(row, c))


def scene_clean(cr, t, tl):
    A = tl.at
    hive(cr, t)
    cam = camera(t, [(A("h6") - 0.3, (1.0, 360, 640)), (A("h7"), (1.12, 330, 640))])
    cr.save()
    enter(cr, cam)
    comb_wall(cr, 4, 5, 60, 460, 74, lambda r, c: "capped" if (r, c) == (1, 2) else ("empty" if (r + c) % 3 else "honey"))
    born = A("h6", "born.")
    cell = (60 + 2 * 74 * 1.732 + 74 * 0.866, 460 + 74 * 1.5)
    if t < born:
        for k in range(3):   # the cap wobbles before it breaks
            pass
    else:
        cracked = seg(t, born, born + 0.4)
        sparkles(cr, t, born, cell[0], cell[1], 8, seed=4, col=hexc("#fff6d8"))
        comb_cell(cr, cell[0], cell[1], 74, "empty")
        rise = ease_out(cracked)
        cleaning = t >= A("h6", "cleaning.")
        scrub = math.sin(t * 14) * 18 if cleaning else 0
        bx = lerp(cell[0], 470, ease_out(seg(t, A("h6", "first"), A("h6", "first") + 0.6)))
        by = lerp(cell[1] + 40, 660, rise)
        bee(cr, t, bx, by, 1.1 * lerp(0.4, 1.0, rise), eyes="half" if t >= A("h7") else "happy",
            mouth="flat" if t >= A("h7") else "grin", arms=((40, -10 + scrub), "down") if cleaning else ("up", "up"),
            hold=mop if cleaning else None, shadow=False)
        if cleaning:
            for k in range(5):
                ph = (t * 1.2 + k * 0.2) % 1.0
                ellipse(cr, 560 + math.sin(k * 2) * 40, 760 - ph * 120, 9 * (1 - ph) + 3, 9 * (1 - ph) + 3)
                paint(cr, (1, 1, 1, 0.7 * (1 - ph)), (0.6, 0.85, 1, 0.8 * (1 - ph)), 2)
    cr.restore()
    calendar(cr, t, A("h6"), 360, 260, "DAY", "1", end=A("h6", "first") - 0.05)
    sign(cr, t, A("h6", "first"), 360, 230, "JOB #1: CLEANER", col=BLUE, size=54, end=A("h7") - 0.05)
    if t >= A("h7"):
        sign(cr, t, A("h7"), 300, 230, "YOUR ROOM", col=HONEY, size=58, rot=0.04)
        if t >= A("h7") + 0.2:
            arrow(cr, 300, 300, cell[0] - 20, cell[1] - 70)
    vignette(cr, 0.45)


def scene_nanny(cr, t, tl):
    A = tl.at
    hive(cr, t)
    cam = camera(t, [(A("h8") - 0.3, (1.0, 360, 640))])
    cr.save()
    enter(cr, cam)
    xs = [130, 300, 470, 640]
    for k, cx in enumerate(xs):
        comb_cell(cr, cx, 760, 80, "empty")
        hungry = (int(t * 2 + k) % 2) == 0
        larva(cr, t, cx - 30, 760, 0.85, mouth="open" if hungry else "smile", seed=k)
    feed = seg(t, A("h8", "feed"), A("h8", "day.", end=True))
    pos = feed * (len(xs) - 1)
    i = min(int(pos), len(xs) - 2)
    u = pos - i
    bx = lerp(xs[i], xs[i + 1], ease_out(clamp01(u * 1.6))) - 20
    by = 540 - math.sin(clamp01(u * 1.6) * math.pi) * 40
    bee(cr, t, bx if t >= A("h8", "feed") else 360, by if t >= A("h8", "feed") else 560, 1.0, fly=True,
        eyes="happy", mouth="grin", arms=("hold", "down"), hold=spoon)
    cr.restore()
    hearts(cr, t, A("h8", "babies"), 300, 650, 6, seed=8)
    sign(cr, t, A("h8"), 360, 230, "JOB #2: NANNY", col=PINK, size=58)
    vignette(cr, 0.45)


def scene_wax(cr, t, tl):
    A = tl.at
    hive(cr, t)
    cam = camera(t, [(A("h9") - 0.3, (1.0, 360, 640)), (A("h9", "belly."), (1.25, 300, 640)),
                     (A("h9", "build"), (1.0, 360, 640))])
    cr.save()
    enter(cr, cam)
    build = A("h9", "build")
    for k in range(9):   # the new wall grows cell by cell
        st = build + 0.18 * k
        if t >= st:
            row, col_ = divmod(k, 3)
            cx, cy = 440 + col_ * 72 * 1.732 / 1.6 + (row % 2) * 36, 470 + row * 100
            cr.save()
            cr.translate(cx, cy)
            sc = max(appear(t, st, 0.3), 0.01)
            cr.scale(sc, sc)
            hexagon(cr, 0, 0, 52, math.pi / 6)
            paint(cr, lin(0, -52, 0, 52, [(0, hexc("#fff4c4")), (1, hexc("#f2d27a"))]), hexc("#b8730f"), 4)
            cr.restore()
    flaking = t >= A("h9", "belly.")
    bee(cr, t, 250, 640, 1.2, eyes="wide" if A("h9", "belly.") <= t < build else "happy",
        mouth="o" if A("h9", "belly.") <= t < build else "grin", arms=("out", "down") if t >= build else ("down", "down"))
    if flaking:   # wax flakes pop out from under the abdomen
        for k in range(6):
            ph = (t * 1.4 + k / 6) % 1.0
            fx = 250 + 30 + ph * (120 + k * 20)
            fy = 640 + 90 - math.sin(ph * math.pi) * (80 + k * 10)
            ellipse(cr, fx, fy, 11, 7, ph * 6)
            paint(cr, alpha(hexc("#fff8e0"), 1 - ph * 0.3), hexc("#c9a35c"), 2.5)
    cr.restore()
    sign(cr, t, A("h9"), 360, 230, "JOB #3: BUILDER", col=HONEY, size=56, end=A("h9", "belly.") - 0.05)
    sign(cr, t, A("h9", "belly."), 360, 230, "WAX FROM HER BELLY", col=hexc("#e0902a"), size=50,
         end=build - 0.05)
    sign(cr, t, build, 360, 230, "HOME, SWEET HOME", col=HONEY, size=52)
    vignette(cr, 0.45)


def scene_guard(cr, t, tl):
    A = tl.at
    meadow(cr, t, rays=False)
    cam = camera(t, [(A("h10") - 0.3, (1.0, 360, 640))])
    cr.save()
    enter(cr, cam)
    hive_door(cr, 360, 820)
    bee(cr, t, 250, 690, 1.05, eyes="shades", mouth="flat", arms=("hips", "hips"))
    sniff = A("h10", "smells")
    # a sister comes in fine; the wasp gets bounced
    sx = lerp(820, 470, ease_out(seg(t, A("h10") + 0.2, A("h10") + 1.0)))
    if t < sniff:
        bee(cr, t, sx, 640, 0.75, fly=True, eyes="happy", mouth="smile", facing=-1, seed=2)
        if t >= A("h10") + 1.0:
            check(cr, t, A("h10") + 1.0, sx, 470)
    else:
        bounce = seg(t, A("h10", "doesn't"), A("h10", "doesn't") + 0.7)
        wx = lerp(lerp(840, 480, ease_out(seg(t, sniff, sniff + 0.6))), 900, ease_out(bounce))
        wy = 620 - math.sin(bounce * math.pi) * 160
        cr.save()
        cr.translate(wx, wy)
        cr.rotate(bounce * 6)
        cr.translate(-wx, -wy)
        wasp(cr, t, wx, wy, 0.85, eyes="open", mouth="o" if bounce > 0 else "flat")
        cr.restore()
        for k in range(3):   # smell waves toward the guard
            u = (t * 1.3 + k / 3) % 1.0
            px = lerp(wx - 60, 330, u)
            stroke_line(cr, [(px, 560 - 20), (px - 10, 560), (px, 560 + 20)], 5, alpha(hexc("#8be06a"), 1 - u))
    cr.restore()
    sign(cr, t, A("h10"), 360, 230, "JOB #4: SECURITY", col=hexc("#5a6478"), size=54)
    stamp(cr, t, A("h10", "doesn't"), 470, 380, "NOPE!", size=84)
    vignette(cr)


def scene_outside(cr, t, tl):
    A = tl.at
    meadow(cr, t)
    wings = A("h12")
    flowers_t = A("h12", "visit")
    cam = camera(t, [(A("h11") - 0.3, (1.3, 360, 700)), (A("h11", "outside."), (1.0, 360, 640)),
                     (flowers_t, (1.0, 360, 640))], dur=0.8)
    cr.save()
    enter(cr, cam)
    fxs = [(120, hexc("#ff8fb5")), (360, hexc("#ffd84d")), (600, hexc("#b98cff"))]
    for k, (fx_, col) in enumerate(fxs):
        flower(cr, t, fx_, 700 + (k % 2) * 40, 0.95, col, seed=k + 3)
    if t < flowers_t:
        x = lerp(-100, 360, ease_out(seg(t, A("h11", "outside."), A("h11", "outside.") + 0.8)))
        bee(cr, t, x, 520, HERO["s"], fly=True, flap=1.6 if t >= wings else 1.0,
            eyes="happy" if t < wings else "wide", mouth="grin" if t < wings else "open", arms=("up", "up"))
    else:
        hop = seg(t, flowers_t, A("h12", "trip.", end=True))
        pos = hop * (len(fxs) - 1)
        i = min(int(pos), len(fxs) - 2)
        u = clamp01((pos - i) * 1.5)
        bx = lerp(fxs[i][0], fxs[i + 1][0], ease_out(u))
        by = 560 - math.sin(u * math.pi) * 120 + (i % 2) * 20
        bee(cr, t, bx, by, 0.95, fly=True, eyes="happy", mouth="grin", arms=("up", "down"))
        for k in range(len(fxs)):
            sparkles(cr, t, flowers_t + k * (A("h12", "trip.", end=True) - flowers_t) / 2, fxs[k][0], 700 + (k % 2) * 40,
                     8, seed=k, col=hexc("#ffe066"), spread=70)
    cr.restore()
    calendar(cr, t, A("h11"), 360, 260, "3 WEEKS", "OUT!", col=GREEN, end=wings - 0.05)
    counter(cr, t, wings + 0.4, 360, 230, 200, size=110, dur=0.8, suffix="+", sub="WING BEATS A SECOND")
    if t >= flowers_t:
        counter(cr, t, flowers_t, 360, 380, 100, size=84, dur=0.9, sub="FLOWERS IN ONE TRIP")
    dof_flowers(cr, t)
    vignette(cr)


def scene_dance(cr, t, tl):
    A = tl.at
    hive(cr, t)
    dance = A("h13", "dance.")
    angle_t = A("h14")
    cam = camera(t, [(A("h13") - 0.3, (1.0, 360, 640)), (angle_t, (1.0, 360, 620))])
    cr.save()
    enter(cr, cam)
    crowd(cr, t, [(790, 6, 0.42, 60, 660)], seed=9, eyes="wide" if t >= dance else "open", mouth="o")
    cx, cy = 360, 650
    ang = math.radians(40)   # the food is 40 degrees right of the sun
    if t >= dance:
        d = (t - dance) * 0.55 % 1.0    # waggle run up the angle, loop back round
        if d < 0.5:
            u = d / 0.5
            px = cx + math.sin(ang) * lerp(-90, 90, u)
            py = cy - math.cos(ang) * lerp(-90, 90, u)
            wig = math.sin(t * 40) * 12
            px += math.cos(ang) * wig
            py += math.sin(ang) * wig
        else:
            u = (d - 0.5) / 0.5
            side = 1 if int((t - dance) * 0.55) % 2 else -1
            a0 = math.pi * u
            px = cx + math.sin(ang) * 90 * math.cos(a0) + side * math.cos(ang) * 90 * math.sin(a0)
            py = cy - math.cos(ang) * 90 * math.cos(a0) + side * math.sin(ang) * 90 * math.sin(a0)
        for side in (-1, 1):   # the figure-of-eight path, faintly
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(ang)
            ellipse(cr, side * 70, 0, 70, 95)
            cr.restore()
            cr.set_source_rgba(1, 0.95, 0.7, 0.35)
            cr.set_dash([10, 10])
            cr.set_line_width(5)
            cr.stroke()
            cr.set_dash([])
        bee(cr, t, px, py, 0.9, eyes="happy", mouth="grin", arms=("up", "up"), tilt=math.sin(t * 20) * 0.2,
            shadow=False)
    else:
        bee(cr, t, 360, 600, 1.1, eyes="open", mouth="smug", arms=("hips", "down"))
    if t >= angle_t:   # sun on top, vertical line, angle arc, flower at the end
        u = ease_out(seg(t, angle_t, angle_t + 0.6))
        stroke_line(cr, [(cx, cy), (cx, cy - 300)], 8, alpha(hexc("#ffe066"), 0.9), curve=False)
        stroke_line(cr, [(cx, cy), (cx + math.sin(ang * u) * 300, cy - math.cos(ang * u) * 300)], 8, WHITE,
                    curve=False)
        cr.arc(cx, cy, 120, -math.pi / 2, -math.pi / 2 + ang * u)
        paint(cr, None, hexc("#ffe066"), 6)
        soft_disc(cr, cx, cy - 330, 70, (1, 0.9, 0.4, 0.6), blur=0.4)
        cr.arc(cx, cy - 330, 34, 0, 2 * math.pi)
        paint(cr, rad(cx, cy - 330, 34, [(0, hexc("#fff6b0")), (1, hexc("#ffc21f"))]), OUTLINE, 4)
        if u >= 1:
            flower(cr, t, cx + math.sin(ang) * 330, cy - math.cos(ang) * 330 - 110, 0.55, hexc("#ff8fb5"), stem=150)
    cr.restore()
    if t < dance:
        if t >= A("h13", "text"):
            phone(cr, 560, 470, 0.9)
            red_x(cr, t, A("h13", "text") + 0.25, 560, 470, 60)
        sign(cr, t, A("h13"), 360, 230, "FOUND FOOD?", col=GREEN, size=60)
    else:
        sign(cr, t, dance, 360, 230, "DANCE!", col=PINK, size=78, end=angle_t - 0.05)
        sign(cr, t, angle_t, 360, 175, "ANGLE = DIRECTION", col=HONEY, size=48, sub="the sun is the compass")
    vignette(cr, 0.45)


def scene_drones(cr, t, tl):
    A = tl.at
    hive(cr, t)
    one_job = A("h17")
    succeed = A("h18")
    die = A("h18", "die")
    cam = camera(t, [(A("h15") - 0.3, (1.0, 360, 640)), (succeed, (1.0, 360, 600))])
    cr.save()
    enter(cr, cam)
    if t < succeed:
        couch(cr, 360, 850)
        bee(cr, t, 210, 690, 0.95, kind="drone", eyes="shades", mouth="smug", arms=("hold", "hips"), hold=honey_cup,
            seed=1)
        bee(cr, t, 500, 700, 0.95, kind="drone", eyes="half", mouth="smile", arms=("hips", "hips"), seed=4)
    else:
        rise = seg(t, succeed, die)
        bee(cr, t, 360, lerp(760, 520, ease_out(rise)), 1.05, kind="drone", fly=True,
            eyes="happy" if t < die else "x", mouth="grin" if t < die else "o", arms=("up", "up"), seed=2)
        hearts(cr, t, succeed, 360, 520, 6, seed=11)
        if t >= die:
            halo(cr, 360, 520 - 175, 1.2)
    cr.restore()
    sign(cr, t, A("h15"), 360, 200, "MEANWHILE...", col=hexc("#5a6478"), size=58, end=A("h16") - 0.05)
    sign(cr, t, A("h15", "brothers."), 360, 330, "THE DRONES", col=HONEY, size=60, rot=0.04, end=A("h16") - 0.05)
    if A("h16") <= t < one_job:   # the to-do list
        k = max(appear(t, A("h16")), 0.01)
        cr.save()
        cr.translate(360, 330)
        cr.scale(k, k)
        soft_rrect(cr, -230, -150, 460, 300, 26, (0, 0, 0, 0.3))
        rrect(cr, -230, -160, 460, 300, 26)
        paint(cr, lin(0, -160, 0, 140, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
        for j, (w, key) in enumerate((("CLEAN", "clean."), ("MAKE HONEY", "honey."), ("STING", "sting."))):
            yy = -90 + j * 90
            bold_text(cr, w, -190, yy + 18, 50, hexc("#2b1d16"), outline=None, shadow=0, align="left")
            red_x(cr, t, A("h16", key), 160, yy, 28)
        cr.restore()
    sign(cr, t, one_job, 360, 260, "ONE JOB:", col=MAUVE, size=58, end=succeed - 0.05)
    sign(cr, t, A("h17", "mating"), 360, 380, "FIND A QUEEN", col=PINK, size=62, rot=0.04, end=succeed - 0.05)
    stamp(cr, t, die, 360, 230, "R.I.P.", col=hexc("#3f4656"), size=96)
    vignette(cr, 0.45)


def scene_autumn(cr, t, tl):
    A = tl.at
    meadow(cr, t, "autumn", rays=False)
    cr.save()
    enter(cr, camera(t, [(A("h19") - 0.3, (1.0, 360, 640))]))
    hive_door(cr, 360, 820)
    throw = A("h19", "throw")
    for k in range(3):   # leaves
        ph = (t * 0.35 + k * 0.33) % 1.0
        lx, ly = 100 + k * 240 + math.sin(t + k) * 40, -40 + ph * 1100
        ellipse(cr, lx, ly, 18, 9, t * 2 + k)
        paint(cr, (hexc("#e8743a"), hexc("#d9a028"), hexc("#c2502a"))[k], OUTLINE, 3)
    bee(cr, t, 250, 690, 1.0, eyes="angry", mouth="flat", arms=("push", "hips"), seed=3)
    for k in range(2):
        st = throw + k * 0.35
        u = ease_out(seg(t, st, st + 0.9))
        dx, dy = lerp(380 + k * 60, 760 + k * 40, u), 680 - math.sin(u * math.pi) * 180 + u * 120
        cr.save()
        cr.translate(dx, dy)
        cr.rotate(u * 4 * (1 if k else -1))
        cr.translate(-dx, -dy)
        bee(cr, t, dx, dy, 0.75, kind="drone", eyes="wide" if t >= st else "half", mouth="o" if t >= st else "smile",
            arms=("up", "up"), shadow=False, seed=k + 5)
        cr.restore()
        suitcase(cr, dx + 50, dy + 60, 0.5, u * 3)
    cr.restore()
    sign(cr, t, A("h19"), 360, 230, "AUTUMN", col=hexc("#e8743a"), size=70)
    stamp(cr, t, throw + 0.3, 400, 370, "EVICTED!", size=74)
    vignette(cr)


def scene_sunset(cr, t, tl):
    A = tl.at
    meadow(cr, t, "sunset", rays=False)
    worn = A("h20", "wear")
    home = A("h20", "one")
    cam = camera(t, [(A("h20") - 0.3, (1.0, 360, 640)), (home, (1.15, 360, 660))], dur=1.5)
    cr.save()
    enter(cr, cam)
    flower(cr, t, 400, 640, 1.1, hexc("#ff9a6b"), seed=7)
    land = ease_out(seg(t, home, home + 1.4))
    x = lerp(lerp(80, 300, ease_out(seg(t, A("h20"), worn))), 390, land)
    y = lerp(500, 600, land)
    bee(cr, t, x, y, 0.95, fly=land < 0.9, flap=0.6, wings_worn=t >= worn,
        eyes="closed" if land >= 0.9 else ("half" if t >= worn else "open"), mouth="smile" if land >= 0.9 else "flat",
        arms=("down", "down"), shadow=False, seed=6)
    cr.restore()
    cr.rectangle(0, 0, W, H)   # the light fades a little as she rests
    cr.set_source_rgba(0.2, 0.08, 0.15, 0.25 * seg(t, home + 0.6, home + 2.2))
    cr.fill()
    sign(cr, t, A("h20"), 360, 230, "6 WEEKS LATER", col=hexc("#ff9a6b"), size=58, end=worn - 0.05)
    sign(cr, t, worn, 360, 230, "WORN-OUT WINGS", col=hexc("#a86a9a"), size=54, end=home - 0.05)
    dof_flowers(cr, t, "sunset")
    vignette(cr, 0.5)


def scene_spoon(cr, t, tl):
    A = tl.at
    kitchen(cr, t)
    twelve = A("h22")
    cam = camera(t, [(A("h21") - 0.3, (1.5, 470, 700)), (twelve, (1.0, 360, 660))], dur=0.9)
    cr.save()
    enter(cr, cam)
    fill = clamp01((t - twelve - 0.3) / 1.6)
    teaspoon(cr, 300, 740, 1.0, fill=fill if t >= twelve else 0.0,
             drop=appear(t, A("h21", "one"), 0.4) if t < twelve else 0)
    if t >= twelve:
        for k in range(12):
            st = twelve + 0.08 * k
            if t >= st:
                put(cr, bee_sprite(eyes="happy", mouth="grin"), 40 + (k % 6) * 110 - 0.36 * 110,
                    430 + (k // 6) * 120 - 0.36 * 160 + math.sin(t * 3 + k) * 4, size=0.36)
    cr.restore()
    sign(cr, t, A("h21", "one"), 360, 230, "1/12 TEASPOON", col=HONEY, size=62, sub="ONE BEE'S WHOLE LIFE",
         end=twelve - 0.05)
    sign(cr, t, twelve, 360, 230, "12 BEES = 1 TEASPOON", col=HONEY, size=50)
    vignette(cr, 0.35)


def scene_tea(cr, t, tl):
    A = tl.at
    kitchen(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h23") - 0.3, (1.0, 360, 660))]))
    teacup(cr, t, 360, 660, 1.0)
    stir = seg(t, A("h23", "stirs"), A("h23", "tea.", end=True) + 0.6)
    if t >= A("h23", "stirs"):
        a = stir * 12
        sx, sy = 360 + math.cos(a) * 60, 600 + math.sin(a) * 12
        cr.save()
        cr.translate(sx, sy)
        cr.rotate(-0.9)
        cr.scale(0.45, 0.45)
        teaspoon(cr, -150, 0, 1.0, fill=0.9)
        cr.restore()
    for k, bx in enumerate((150, 590)):   # two bees peeking over the rim
        bee(cr, t, bx, 560, 0.7, eyes="wide", mouth="open" if t >= A("h23", "tea.") else "o",
            arms=("face", "face"), shadow=False, seed=k, facing=1 if k == 0 else -1)
    cr.restore()
    sign(cr, t, A("h23", "tea."), 360, 230, "...INTO TEA.", col=hexc("#8a4a16"), size=66)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    meadow(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h24") - 0.3, (1.0, 360, 640))]))
    bee(cr, t, 200, 640, 1.05, eyes="happy", mouth="grin", arms=("wave", "hips"), seed=1)
    bee(cr, t, 520, 640, 1.05, kind="drone", eyes="shades", mouth="smug", arms=("hips", "hips"), seed=2)
    cr.restore()
    sign(cr, t, A("h24"), 360, 230, "WHO WOULD YOU BE?", col=HONEY, size=52)
    buttons(cr, t, A("h24", "worker?"), (("WORKER", GREEN), ("DRONE", MAUVE)), y=1040)
    stamp(cr, t, A("h24", "drone?", end=True), 360, 380, "COMMENT BELOW!", col=RED, size=54, rot=-0.06)
    dof_flowers(cr, t)
    vignette(cr)


SCENES = {"hook": scene_hook, "hive": scene_hive, "queen": scene_queen, "clean": scene_clean, "nanny": scene_nanny,
          "wax": scene_wax, "guard": scene_guard, "outside": scene_outside, "dance": scene_dance,
          "drones": scene_drones, "autumn": scene_autumn, "sunset": scene_sunset, "spoon": scene_spoon,
          "tea": scene_tea, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
