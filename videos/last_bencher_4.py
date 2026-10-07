"""The Last Bencher Part 4: "The New Teacher" -- in the polished look (motion/polish.py + motion/toons.py).

Day one, the new teacher says nobody in her class is smarter than her. The last bencher bets her three riddles (get one
right and he sits in the front row for a year): three pills taken every half hour last one hour (now, 30 min, 60 min);
a greenhouse is made of glass; a man who pushes his car to a hotel and goes bankrupt is playing Monopoly. She answers
back with "what has to be broken before you can use it?" (an egg), lets him pick any seat, he picks the last bench,
and she sits next to him. Script approved by the owner on 7 Oct 2026 (out/scripts_polished_batch1.md).
Classic riddles; none repeat Parts 1-3 or the Principal video.
"""
import math
import random

from motion.engine import W, H, cairo, clamp01, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc,
                           soft_rrect, sprite, stamp, stroke_line, text_path, vignette)
from motion.timeline import clear_dialogue
from motion.toons import head, person, portrait

NARRATOR = dict()
TAIL = 0.9

SCRIPT = [
    dict(id="b1", scene="board1", text="Day one. The new teacher says nobody in her class is smarter than her."),
    dict(id="b2", scene="back", text="The last bencher raises his hand. Ma'am, three riddles. Get one right, and "
                                     "I'll sit in the front row for a year.", speaker="kid", speaker_from="Ma'am,"),
    dict(id="b3", scene="deal", text="Deal.", speaker="teacher"),
    dict(id="b4", scene="pills", text="A doctor gives you three pills. Take one every half hour. How long do they "
                                      "last?", speaker="kid"),
    dict(id="b5", scene="pills", text="An hour and a half.", speaker="teacher"),
    dict(id="b6", scene="pills", text="One hour, ma'am. First pill now. Second after thirty minutes. Third after "
                                      "sixty.", speaker="kid"),
    dict(id="b7", scene="houses", text="A red house is made of red bricks. A blue house is made of blue bricks. "
                                       "What's a greenhouse made of?", speaker="kid"),
    dict(id="b8", scene="houses", text="Green bricks.", speaker="teacher"),
    dict(id="b9", scene="houses", text="Glass, ma'am.", speaker="kid"),
    dict(id="b10", scene="street", text="Last one. A man pushes his car up to a hotel. Right away, he goes "
                                        "bankrupt. Why?", speaker="kid"),
    dict(id="b11", scene="street", text="Bad parking?", speaker="teacher"),
    dict(id="b12", scene="street", text="He's playing Monopoly, ma'am.", speaker="kid"),
    dict(id="b13", scene="egg", text="The teacher smiles. My turn. What has to be broken before you can use it?",
         speaker="teacher", speaker_from="My"),
    dict(id="b14", scene="egg", text="The school rules?", speaker="kid"),
    dict(id="b15", scene="egg", text="An egg. And fine, you win. Pick any seat you like.", speaker="teacher"),
    dict(id="b16", scene="seat", text="Last bench, ma'am.", speaker="kid"),
    dict(id="b17", scene="seat", text="Good. Then I'm sitting next to you.", speaker="teacher"),
    dict(id="b18", scene="end", text="Which riddle got you? Number one, two, or three?", gap=0.3),
]
clear_dialogue(SCRIPT)   # riddles and answers: slower, with clear turns

METADATA = dict(
    title="The New Teacher Said Nobody Is Smarter Than Her 😏 #TheLastBencher",
    alt_titles=["The Last Bencher vs The New Teacher (3 Riddles) 🧠", "She Bet Him She Was Smarter. Big Mistake. 😂"],
    description="""Day one: the new teacher says nobody in her class is smarter than her. The Last Bencher raises his hand: three riddles, and if she gets one right, he sits in the front row for a year. 😏

1️⃣ A doctor gives you three pills. Take one every half hour. How long do they last?
2️⃣ A red house is made of red bricks, a blue house of blue bricks. What's a greenhouse made of?
3️⃣ A man pushes his car up to a hotel and right away goes bankrupt. Why?

Then she fires one back... and the ending is not what he planned. 😂

Answers: one hour (now, 30 minutes, 60 minutes) · glass · he's playing Monopoly · an egg.

💬 Which riddle got you? Number one, two or three? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and The Last Bencher, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#Riddles", "#Shorts"],
    tags=["the last bencher", "riddles", "riddles with answers", "trick questions", "brain teasers", "teacher vs student",
          "funny riddles", "greenhouse riddle", "three pills riddle", "monopoly riddle", "interestingly strange"],
    pinned_comment="Be honest: which one got you? 1, 2 or 3? 👇 (Mine was the pills 💊)",
)

# ---------------------------------------------------------------- palette
RED = hexc("#e8473f")
BLUE = hexc("#4aa3f0")
GREEN = hexc("#3fbf6a")
PURPLE = hexc("#7a5bd0")
GOLD = hexc("#ffcf3f")
WOOD = hexc("#b9824a")
CHALK = (0.97, 0.97, 0.94, 0.95)


# ---------------------------------------------------------------- backgrounds (cached, screen space)
def _wall(c, board):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 820, [(0, hexc("#bfe0d6")), (1, hexc("#e4f2e8"))]))
    c.fill()
    c.rectangle(0, 700, W, 120)
    c.set_source(lin(0, 700, 0, 820, [(0, hexc("#8cc0b2")), (1, hexc("#6ea596"))]))
    c.fill()
    c.rectangle(0, 700, W, 10)
    c.set_source_rgba(*hexc("#5b8f80"))
    c.fill()
    c.rectangle(0, 820, W, H - 820)
    c.set_source(lin(0, 820, 0, H, [(0, hexc("#d9a46a")), (1, hexc("#a8713e"))]))
    c.fill()
    for k in range(9):
        y = 820 + (k ** 1.35) * 22
        c.rectangle(0, y, W, 3)
        c.set_source_rgba(0.35, 0.2, 0.1, 0.25)
        c.fill()
    if board:
        soft_rrect(c, 40, 130, 640, 450, 20, (0, 0, 0, 0.35), sigma=14)
        rrect(c, 40, 120, 640, 450, 18)
        paint(c, lin(0, 120, 0, 570, [(0, hexc("#c99460")), (1, hexc("#8a5a2e"))]), OUTLINE, 6)
        rrect(c, 66, 144, 588, 400, 8)
        paint(c, rad(300, 300, 520, [(0, hexc("#3e7a5a")), (1, hexc("#22503a"))]), OUTLINE, 4)
        rng = random.Random(4)
        for _ in range(40):    # chalk dust smudges
            x, y = 80 + rng.random() * 560, 160 + rng.random() * 370
            c.arc(x, y, 6 + rng.random() * 20, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 0.025)
            c.fill()
        rrect(c, 60, 548, 600, 16, 6)
        paint(c, hexc("#a87444"), OUTLINE, 4)
        for k, col in enumerate((WHITE, hexc("#ffd84d"), hexc("#ff8fb5"))):
            rrect(c, 120 + k * 40, 538, 30, 10, 4)
            paint(c, col, OUTLINE, 2)
    else:
        for wx in (70, 410):      # two bright windows
            soft_rrect(c, wx, 150, 240, 300, 14, (0, 0, 0, 0.25), sigma=10)
            rrect(c, wx, 140, 240, 300, 14)
            paint(c, lin(0, 140, 0, 440, [(0, hexc("#9fd6ff")), (1, hexc("#e8f7ff"))]), OUTLINE, 6)
            c.rectangle(wx + 116, 140, 8, 300)
            c.rectangle(wx, 286, 240, 8)
            c.set_source_rgba(*hexc("#f4efe6"))
            c.fill()
            c.arc(wx + 60, 220, 26, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 0.55)
            c.fill()
        rrect(c, 310, 470, 100, 130, 8)    # a poster
        paint(c, hexc("#ffd84d"), OUTLINE, 4)
        c.arc(360, 520, 26, 0, 2 * math.pi)
        paint(c, hexc("#ff8a3c"), OUTLINE, 3)


def room(cr, t, board=False):
    put(cr, sprite(("room", board), W, H, lambda c: _wall(c, board)), 0, 0)
    if not board:
        light_rays(cr, t, 600, 120, n=4, a=0.07)


def studio(cr, t, top, bottom, seed=1):
    """A soft gradient backdrop with drifting bokeh for card scenes."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, top), (1, bottom)]))
    cr.fill()
    bokeh(cr, t, seed, 14, [WHITE, hexc("#ffe7a8")], rmin=20, rmax=70)


def chalk(cr, t, start, x, y, text, size=52, dur=None, align="left"):
    """Chalk handwriting that writes itself left to right from `start`."""
    if t < start:
        return
    cr.save()
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    w = cr.text_extents(text).x_advance
    dur = dur or 0.05 * len(text)
    k = clamp01((t - start) / dur)
    x0 = x - (w / 2 if align == "center" else 0)
    cr.rectangle(x0 - 10, y - size * 1.2, (w + 20) * k, size * 1.8)
    cr.clip()
    cr.move_to(x0, y)
    cr.text_path(text)
    cr.set_source_rgba(*CHALK)
    cr.fill()
    cr.restore()
    if k < 1:
        cue("scribble", t, start, dur)


# ---------------------------------------------------------------- props
def desk(cr, x, y, w=150, s=1.0):
    """A school desk seen from the front; (x, y) is the middle of the desk top."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for side in (-1, 1):
        rrect(cr, side * (w / 2 - 22) - 7, 10, 14, 120, 5)
        paint(cr, hexc("#5a6478"), OUTLINE, 3.5)
    rrect(cr, -w / 2 + 8, 14, w - 16, 70, 8)
    paint(cr, lin(0, 14, 0, 84, [(0, shade(WOOD, -0.05)), (1, shade(WOOD, -0.3))]), OUTLINE, 4)
    rrect(cr, -w / 2, -10, w, 26, 8)
    paint(cr, lin(0, -10, 0, 16, [(0, shade(WOOD, 0.35)), (1, WOOD)]), OUTLINE, 4.5)
    cr.restore()


def pill(cr, x, y, s=1.0, rot=0.6):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_rrect(cr, -52, -16, 104, 44, 22, (0, 0, 0, 0.25), sigma=6)
    cr.save()
    rrect(cr, -52, -22, 104, 44, 22)
    cr.clip()
    cr.rectangle(-52, -22, 52, 44)
    cr.set_source(lin(0, -22, 0, 22, [(0, hexc("#ff8a7a")), (1, hexc("#c8302a"))]))
    cr.fill()
    cr.rectangle(0, -22, 52, 44)
    cr.set_source(lin(0, -22, 0, 22, [(0, WHITE), (1, hexc("#d9dde6"))]))
    cr.fill()
    cr.restore()
    rrect(cr, -52, -22, 104, 44, 22)
    paint(cr, None, OUTLINE, 4.5)
    ellipse(cr, -22, -10, 18, 5)
    paint(cr, alpha(WHITE, 0.6), None, 0)
    cr.restore()


def clock(cr, t, x, y, r, minutes):
    if r <= 1:
        return
    cr.save()
    cr.translate(x, y)
    soft_disc(cr, 0, 8, r * 1.05, (0, 0, 0, 0.3))
    cr.arc(0, 0, r, 0, 2 * math.pi)
    paint(cr, rad(-r * 0.3, -r * 0.3, r * 1.3, [(0, WHITE), (1, hexc("#dfe6ee"))]), OUTLINE, 6)
    for k in range(12):
        a = k * math.pi / 6
        stroke_line(cr, [(math.cos(a) * r * 0.78, math.sin(a) * r * 0.78), (math.cos(a) * r * 0.88,
                                                                           math.sin(a) * r * 0.88)], 4, OUTLINE,
                    curve=False)
    a = minutes / 60 * 2 * math.pi - math.pi / 2
    stroke_line(cr, [(0, 0), (math.cos(a) * r * 0.72, math.sin(a) * r * 0.72)], 6, RED, curve=False)
    a2 = minutes / 720 * 2 * math.pi - math.pi / 2
    stroke_line(cr, [(0, 0), (math.cos(a2) * r * 0.48, math.sin(a2) * r * 0.48)], 8, OUTLINE, curve=False)
    cr.arc(0, 0, 8, 0, 2 * math.pi)
    paint(cr, OUTLINE, None, 0)
    cr.restore()


def red_x(cr, t, start, x, y, r=40):
    if t < start:
        return
    k = appear(t, start, 0.25)
    cue("hit", t, start)
    for d in (-1, 1):
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 16, OUTLINE, curve=False)
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 10, RED, curve=False)


def sparkles(cr, t, start, x, y, n=6, seed=2, col=WHITE, spread=90):
    if t < start or t > start + 1.2:
        return
    u = seg(t, start, start + 1.2)
    rng = random.Random(seed)
    for k in range(n):
        a = rng.random() * 6.28
        d = spread * ease_out(u) * (0.6 + 0.4 * rng.random())
        sx, sy = x + math.cos(a) * d, y + math.sin(a) * d
        r = 14 * (1 - u)
        cr.move_to(sx, sy - r)
        for j in range(1, 8):
            rr = r if j % 2 == 0 else r * 0.35
            aa = j * math.pi / 4 - math.pi / 2
            cr.line_to(sx + math.cos(aa) * rr, sy + math.sin(aa) * rr)
        cr.close_path()
        paint(cr, col, OUTLINE, 2.5)


def house(cr, x, y, col, s=1.0, glass=0.0, t=0.0):
    """A brick house standing at (x, y). `glass` 0..1 fades it into a glass greenhouse with plants."""
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 6, 110, 0.25)
    if glass < 1:
        cr.push_group()
        cr.move_to(-100, -150)
        cr.line_to(0, -235)
        cr.line_to(100, -150)
        cr.close_path()
        paint(cr, lin(0, -235, 0, -150, [(0, hexc("#7a4a3a")), (1, hexc("#4f2e24"))]), OUTLINE, 5)
        rrect(cr, -86, -152, 172, 152, 6)
        paint(cr, lin(-86, -152, 86, 0, [(0, shade(col, 0.25)), (1, shade(col, -0.2))]), OUTLINE, 5)
        cr.save()
        rrect(cr, -86, -152, 172, 152, 6)
        cr.clip()
        for row in range(8):
            yy = -152 + row * 19
            stroke_line(cr, [(-86, yy), (86, yy)], 2.5, alpha(shade(col, -0.45), 0.6), curve=False)
            for k in range(6):
                xx = -86 + k * 36 + (18 if row % 2 else 0)
                stroke_line(cr, [(xx, yy), (xx, yy + 19)], 2.5, alpha(shade(col, -0.45), 0.6), curve=False)
        cr.restore()
        rrect(cr, -24, -80, 48, 80, 6)
        paint(cr, hexc("#6b3f22"), OUTLINE, 4)
        rrect(cr, 34, -128, 40, 40, 4)
        paint(cr, hexc("#cfeaff"), OUTLINE, 4)
        rrect(cr, -74, -128, 40, 40, 4)
        paint(cr, hexc("#cfeaff"), OUTLINE, 4)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - glass)
    if glass > 0:
        cr.push_group()
        for k in range(3):     # plants inside
            px = -50 + k * 50
            for j in range(4):
                a = -math.pi / 2 + (j - 1.5) * 0.5
                ellipse(cr, px + math.cos(a) * 22, -30 + math.sin(a) * 26, 18, 9, a)
                paint(cr, GREEN, OUTLINE, 3)
            rrect(cr, px - 16, -22, 32, 22, 4)
            paint(cr, hexc("#c86a3a"), OUTLINE, 3)
        cr.move_to(-100, -150)
        cr.line_to(0, -235)
        cr.line_to(100, -150)
        cr.close_path()
        cr.rectangle(-86, -152, 172, 152)
        cr.set_source_rgba(0.75, 0.92, 1.0, 0.4)
        cr.fill()
        for xx in (-86, -43, 0, 43, 86):
            stroke_line(cr, [(xx, 0), (xx, -150)], 6, WHITE, curve=False)
        for yy in (0, -75, -150):
            stroke_line(cr, [(-86, yy), (86, yy)], 6, WHITE, curve=False)
        stroke_line(cr, [(-100, -150), (0, -235), (100, -150)], 7, WHITE, curve=False)
        stroke_line(cr, [(-60, -130), (-30, -100)], 6, alpha(WHITE, 0.8), curve=False)
        stroke_line(cr, [(40, -200), (60, -180)], 6, alpha(WHITE, 0.8), curve=False)
        cr.rectangle(-86, -152, 172, 152)
        paint(cr, None, alpha(OUTLINE, 0.7), 4)
        cr.pop_group_to_source()
        cr.paint_with_alpha(glass)
    cr.restore()


def car(cr, x, y, s=1.0, col=RED, t=0.0, spin=0.0):
    """A cartoon car (side view, facing right) with its wheels on the ground at (x, y)."""
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 4, 150, 0.25)
    smooth(cr, [(-150, -40), (-140, -92), (-70, -100), (-40, -150), (60, -150), (100, -100), (150, -88),
                (155, -40)])
    paint(cr, lin(0, -150, 0, -30, [(0, shade(col, 0.4)), (1, shade(col, -0.25))]), OUTLINE, 5)
    for x0, x1 in ((-30, 10), (22, 70)):
        smooth(cr, [(x0, -140), (x1 - (8 if x1 > 50 else 0), -140), (x1 + (14 if x1 > 50 else 0), -100),
                    (x0, -100)], closed=True)
        paint(cr, lin(0, -140, 0, -100, [(0, hexc("#dff3ff")), (1, hexc("#9fcbe8"))]), OUTLINE, 4)
    ellipse(cr, 146, -76, 10, 8)
    paint(cr, hexc("#fff3a8"), OUTLINE, 3)
    for wx in (-90, 90):
        cr.arc(wx, -28, 30, 0, 2 * math.pi)
        paint(cr, hexc("#2b2b33"), OUTLINE, 4)
        cr.arc(wx, -28, 13, 0, 2 * math.pi)
        paint(cr, hexc("#cfd5df"), OUTLINE, 3)
        a = spin
        stroke_line(cr, [(wx + math.cos(a) * 12, -28 + math.sin(a) * 12), (wx - math.cos(a) * 12,
                                                                           -28 - math.sin(a) * 12)], 3, OUTLINE,
                    curve=False)
    cr.restore()


def hotel(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 4, 140, 0.25)
    rrect(cr, -120, -430, 240, 430, 8)
    paint(cr, lin(-120, 0, 120, 0, [(0, hexc("#ff6a5a")), (1, hexc("#b8262a"))]), OUTLINE, 6)
    for row in range(5):
        for col in range(3):
            rrect(cr, -92 + col * 66, -400 + row * 66, 50, 44, 5)
            paint(cr, lin(0, 0, 0, 44, [(0, hexc("#fff3c4")), (1, hexc("#ffd36b"))]), OUTLINE, 3.5)
    rrect(cr, -36, -80, 72, 80, 6)
    paint(cr, hexc("#5a2a1a"), OUTLINE, 4)
    rrect(cr, -100, -500, 200, 64, 12)
    paint(cr, lin(0, -500, 0, -436, [(0, hexc("#fff0a8")), (1, GOLD)]), OUTLINE, 5)
    bold_text(cr, "HOTEL", 0, -452, 44, RED, shadow=0)
    cr.restore()


def die(cr, x, y, s, n, rot):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_rrect(cr, -50, -40, 100, 100, 18, (0, 0, 0, 0.3), sigma=8)
    rrect(cr, -50, -50, 100, 100, 18)
    paint(cr, rad(-20, -25, 90, [(0, WHITE), (1, hexc("#dfe3ea"))]), OUTLINE, 5)
    spots = {1: [(0, 0)], 2: [(-22, -22), (22, 22)], 3: [(-24, -24), (0, 0), (24, 24)],
             4: [(-22, -22), (22, -22), (-22, 22), (22, 22)], 5: [(-24, -24), (24, -24), (0, 0), (-24, 24), (24, 24)],
             6: [(-22, -26), (22, -26), (-22, 0), (22, 0), (-22, 26), (22, 26)]}[n]
    for sx, sy in spots:
        cr.arc(sx, sy, 9, 0, 2 * math.pi)
        paint(cr, OUTLINE, None, 0)
    cr.restore()


def money(cr, x, y, rot, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -70, -38, 140, 76, 8)
    paint(cr, lin(0, -38, 0, 38, [(0, hexc("#c8f2b0")), (1, hexc("#86c86a"))]), OUTLINE, 4)
    cr.arc(0, 0, 22, 0, 2 * math.pi)
    paint(cr, None, alpha(hexc("#2f6a2a"), 0.7), 3)
    bold_text(cr, "500", 0, 10, 26, hexc("#2f6a2a"), outline=None, shadow=0)
    cr.restore()


def egg(cr, t, crack_at, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    u = seg(t, crack_at, crack_at + 0.5) if t >= crack_at else 0.0
    if u <= 0:
        ellipse(cr, 0, 0, 40, 52)
        paint(cr, rad(-12, -18, 60, [(0, WHITE), (1, hexc("#f0dcbc"))]), OUTLINE, 5)
    else:
        cue("hit", t, crack_at)
        ellipse(cr, 0, 30 + 10 * u, 46 * (1 + u * 0.4), 18)
        paint(cr, alpha(WHITE, 0.9), OUTLINE, 3)
        cr.arc(0, 28 + 10 * u, 18, 0, 2 * math.pi)
        paint(cr, rad(-5, 22, 20, [(0, hexc("#ffe27a")), (1, hexc("#ffb21f"))]), OUTLINE, 3)
        for side in (-1, 1):
            cr.save()
            cr.translate(side * 30 * u, -12 * u)
            cr.rotate(side * 0.6 * u)
            cr.move_to(-40 if side < 0 else 0, -10)
            if side < 0:
                cr.arc_negative(0, 0, 40, math.pi, math.pi * 0.5)
            cr.new_path()
            cr.arc(0, -4, 40, math.pi if side < 0 else 1.5 * math.pi, 1.5 * math.pi if side < 0 else 2 * math.pi)
            cr.line_to(side * 0.0, 8)
            cr.line_to(side * 12, -2)
            cr.line_to(side * 26, 8)
            cr.line_to(side * 40, -4)
            cr.close_path()
            paint(cr, rad(-12, -18, 60, [(0, WHITE), (1, hexc("#f0dcbc"))]), OUTLINE, 4)
            cr.restore()
    cr.restore()


def trophy(cr, t, start, x, y, s=1.0):
    if t < start:
        return
    k = appear(t, start, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 3) * 4)
    cr.scale(k * s, k * s)
    soft_disc(cr, 0, -40, 120, alpha(GOLD, 0.35))
    for side in (-1, 1):
        cr.arc(side * 58, -70, 26, 0, 2 * math.pi)
        paint(cr, None, OUTLINE, 14)
        cr.arc(side * 58, -70, 26, 0, 2 * math.pi)
        paint(cr, None, GOLD, 8)
    cr.move_to(-62, -120)
    cr.line_to(62, -120)
    cr.curve_to(60, -20, 20, -10, 10, 10)
    cr.line_to(-10, 10)
    cr.curve_to(-20, -10, -60, -20, -62, -120)
    cr.close_path()
    paint(cr, lin(-62, 0, 62, 0, [(0, hexc("#fff0a8")), (0.4, GOLD), (1, hexc("#c8900c"))]), OUTLINE, 5)
    rrect(cr, -40, 10, 80, 36, 6)
    paint(cr, hexc("#6b3f22"), OUTLINE, 4)
    ellipse(cr, -28, -90, 10, 22, 0.2)
    paint(cr, alpha(WHITE, 0.6), None, 0)
    cr.restore()


def chair(cr, x, y, s=1.0):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for side in (-1, 1):
        rrect(cr, side * 50 - 6, -90, 12, 90, 4)
        paint(cr, hexc("#5a6478"), OUTLINE, 3.5)
    rrect(cr, -62, -230, 124, 120, 12)
    paint(cr, lin(0, -230, 0, -110, [(0, shade(WOOD, 0.3)), (1, shade(WOOD, -0.15))]), OUTLINE, 4.5)
    rrect(cr, -66, -104, 132, 20, 8)
    paint(cr, shade(WOOD, 0.2), OUTLINE, 4)
    cr.restore()


# ---------------------------------------------------------------- the class
ROWS = [  # desk-top y, scale, [(x, who)]
    (560, 0.56, [(140, "student2"), (340, "student1"), (560, "kid")]),
    (680, 0.66, [(80, "student3"), (265, "student2"), (440, "student1")]),
    (800, 0.78, [(150, "student1"), (410, "student3")]),
]


def classroom(cr, t, tl, kid_pose=None, look_at=None, gasp=False, kid_there=True, extra=None):
    """Three rows of pupils at their desks; the last bencher at the back right."""
    for k, (dy, s, kids) in enumerate(ROWS):
        for j, (x, who) in enumerate(kids):
            if who == "kid":
                if kid_there:
                    kp = kid_pose or {}
                    person(cr, t, x, dy + 46 * s, s, "kid", **kp)
                if extra:
                    extra(cr, t, x, dy, s)
                desk(cr, x, dy, 170, s)
                continue
            lk = (0.0, 0.0)
            if look_at is not None:
                lk = (clamp01((look_at[0] - x) / 200) - clamp01((x - look_at[0]) / 200), -0.6)
            person(cr, t, x, dy + 46 * s, s, who, eyes="wide" if gasp else "open", mouth="o" if gasp else "smile",
                   look=lk, arms=("front", "front"), seed=k * 5 + j, turn=lk[0] * 0.6)
            desk(cr, x, dy, 170, s)


def speaking(tl, who, t):
    return tl.speaking(who, t)


def mouth_of(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- scenes
def scene_board1(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cam = camera(t, [(0, (1.0, 360, 640)), (A("b1", "nobody"), (1.12, 330, 600))], dur=1.2)
    cr.save()
    enter(cr, cam)
    chalk(cr, t, A("b1", "Day"), 100, 230, "Day 1", 58, dur=0.5)
    chalk(cr, t, A("b1", "nobody"), 330, 300, "Nobody is", 50)
    chalk(cr, t, A("b1", "smarter"), 330, 370, "smarter", 50)
    chalk(cr, t, A("b1", "her."), 330, 440, "than ME.", 50, dur=0.4)
    turned = t >= A("b1", "nobody")
    person(cr, t, 190, 900, 1.0, "teacher", eyes="half" if turned else "open", mouth="smug" if turned else "smile",
           brows="raise" if turned else None, arms=("hips", "point") if turned else ("up", "down"),
           look=(0.4, 0) if turned else (-0.4, -0.5), facing=1)
    cr.restore()
    if t >= A("b1", "her."):   # the class gulps (blurred heads in the foreground)
        for k, (x, who) in enumerate(((90, "student1"), (330, "student2"), (610, "student3"))):
            spr = sprite(("fghead", who), 260, 260, lambda c, w=who: head(c, 0.0, 130, 130, 100, w, "wide", "o",
                                                                          brows="up"), sigma=5, scale=0.5)
            put(cr, spr, x - 130, 1040 + math.sin(t * 3 + k) * 4)
    sign(cr, t, A("b1"), 360, 100, "THE NEW TEACHER", col=PURPLE, size=50, end=A("b1", "nobody") - 0.05)
    vignette(cr, 0.4)


def scene_back(cr, t, tl):
    A = tl.at
    room(cr, t)
    raise_t = A("b2", "raises")
    cam = camera(t, [(A("b2") - 0.3, (1.0, 360, 640)), (raise_t, (1.7, 540, 470))], dur=0.7)
    cr.save()
    enter(cr, cam)
    up = t >= raise_t
    talk = tl.speaking("kid", t)
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down") if up else ("front", "front"),
                                       eyes="happy" if (up and not talk) else "open",
                                       mouth="talk" if talk else "grin", brows="raise" if up else None),
              look_at=(560, 0) if t >= A("b2", "Ma'am,") else None)
    cr.restore()
    sign(cr, t, A("b2", "three"), 360, 170, "3 RIDDLES", col=GOLD, size=70, end=A("b2", "right,") - 0.05)
    sign(cr, t, A("b2", "right,"), 360, 170, "GET ONE RIGHT...", col=GREEN, size=54, sub="AND I SIT IN THE FRONT ROW",
         sub_col=WHITE)
    vignette(cr, 0.45)


def scene_deal(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("b3") - 0.3, (1.6, 300, 560))]))
    crack = t >= A("b3") + 0.15
    person(cr, t, 300, 900, 1.0, "teacher", eyes="angry", mouth="talk" if tl.speaking("teacher", t) else "smug",
           brows="angry", arms=("front", "front") if crack else ("hips", "hips"))
    cr.restore()
    sparkles(cr, t, A("b3") + 0.15, 330, 760, n=5, seed=4, col=GOLD, spread=60)
    stamp(cr, t, A("b3"), 360, 230, "DEAL.", col=RED, size=110)
    vignette(cr, 0.45)


def scene_pills(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=3)
    b5, b6 = A("b5"), A("b6")
    # the three pills
    if t < b6:
        for k in range(3):
            st = A("b4", "three") + 0.15 * k
            if t >= st:
                kk = appear(t, st, 0.35)
                pill(cr, 200 + k * 160, 470 + math.sin(t * 2 + k) * 6, kk * 1.1, 0.5 + 0.2 * k)
        if t >= A("b4", "half"):
            clock(cr, t, 360, 680, 80 * appear(t, A("b4", "half")), 30 * seg(t, A("b4", "half"), A("b4", "half") + 0.8))
    else:   # the timeline: one pill at 0, 30 and 60 minutes
        x0, x1, y = 110, 610, 560
        k = appear(t, b6, 0.3)
        stroke_line(cr, [(x0, y), (lerp(x0, x1, k), y)], 14, OUTLINE, curve=False)
        stroke_line(cr, [(x0, y), (lerp(x0, x1, k), y)], 8, WHITE, curve=False)
        for j, (lab, key) in enumerate((("0", "now."), ("30", "thirty"), ("60", "sixty."), ("90", None))):
            x = lerp(x0, x1, j / 3)
            if t < b6 + 0.1 * j:
                continue
            stroke_line(cr, [(x, y - 22), (x, y + 22)], 8, OUTLINE, curve=False)
            bold_text(cr, lab, x, y + 80, 46, WHITE)
            if j == 0:
                bold_text(cr, "MIN", x, y + 120, 26, WHITE, font="Fredoka", ow=6)
            if key:
                st = A("b6", key)
                if t >= st:
                    pill(cr, x, y - 70 - 30 * (1 - appear(t, st, 0.35)), 0.9, 0.3)
                    cue("pop", t, st)
            else:
                red_x(cr, t, A("b6", "sixty."), x, y - 70, 34)
        clock(cr, t, 360, 790, 70, 60 * seg(t, A("b6", "First"), A("b6", "sixty.", end=True)))
    sign(cr, t, A("b4", "doctor"), 360, 200, "DOCTOR'S ORDERS", col=RED, size=54, end=A("b4", "half") - 0.05)
    sign(cr, t, A("b4", "half"), 360, 200, "1 EVERY 30 MIN", col=BLUE, size=58, end=A("b4", "How") - 0.05)
    sign(cr, t, A("b4", "How"), 360, 200, "HOW LONG?", col=GOLD, size=72, end=b5 - 0.05)
    sign(cr, t, b5, 360, 200, "1.5 HOURS?", col=PURPLE, size=72, end=A("b6", "hour,") - 0.05)
    sign(cr, t, A("b6", "hour,"), 360, 200, "1 HOUR!", col=GREEN, size=86, rot=0.03)
    portrait(cr, t, A("b4") + 0.05, 110, 330 if t >= b6 else 760, 82, "kid", mouth=mouth_of(tl, "kid", t, "grin"),
             eyes="open", end=b5 - 0.05, bg=hexc("#ffd84d"))
    portrait(cr, t, b5, 610, 760, 82, "teacher", mouth=mouth_of(tl, "teacher", t, "smug"),
             eyes="half" if t < b6 else "wide", brows="raise" if t < b6 else "up", end=None, bg=hexc("#cdb8ff"),
             sweat=t >= A("b6", "sixty."))
    portrait(cr, t, b6, 110, 760, 82, "kid", mouth=mouth_of(tl, "kid", t, "grin"), eyes="open", bg=hexc("#ffd84d"))
    vignette(cr, 0.35)


def scene_houses(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#7cc6ff")), (0.5, hexc("#d9f0ff")), (0.52, hexc("#9bd87a")),
                                   (1, hexc("#5aa043"))]))
    cr.fill()
    bokeh(cr, t, 6, 8, [WHITE], rmin=30, rmax=80, area=(0, 0, W, 600))
    b8, b9 = A("b8"), A("b9")
    cam = camera(t, [(A("b7") - 0.3, (1.0, 360, 640)), (A("b7", "greenhouse"), (1.04, 380, 640))], dur=0.8)
    cr.save()
    enter(cr, cam)
    gy = 690
    if t >= A("b7", "red"):
        k = appear(t, A("b7", "red"), 0.4)
        house(cr, 125, gy, RED, 1.0 * k)
    if t >= A("b7", "blue"):
        k = appear(t, A("b7", "blue"), 0.4)
        house(cr, 360, gy, BLUE, 1.0 * k)
    if t >= b8:
        k = appear(t, b8 + 0.1, 0.4)
        glass = seg(t, b9 + 0.05, b9 + 0.6)
        house(cr, 595, gy, GREEN, 1.0 * k, glass=glass, t=t)
    elif t >= A("b7", "greenhouse"):
        k = appear(t, A("b7", "greenhouse"), 0.4)
        bold_text(cr, "?", 590, gy - 40, 200 * k, GOLD)
    cr.restore()
    sparkles(cr, t, b9 + 0.3, 590, 560, n=8, seed=7, col=WHITE, spread=120)
    sign(cr, t, A("b7", "red"), 130, 340, "RED", col=RED, size=48, end=b8 - 0.05)
    sign(cr, t, A("b7", "blue"), 360, 340, "BLUE", col=BLUE, size=48, end=b8 - 0.05)
    sign(cr, t, A("b7", "greenhouse"), 360, 190, "GREENHOUSE = ?", col=GREEN, size=56, end=b8 - 0.05)
    sign(cr, t, b8, 360, 190, "GREEN BRICKS?", col=PURPLE, size=62, end=b9 - 0.05)
    sign(cr, t, b9, 360, 190, "GLASS!", col=hexc("#5cc8e8"), size=96, rot=0.03)
    if t < b8:
        portrait(cr, t, A("b7") + 0.05, 110, 800, 82, "kid", mouth=mouth_of(tl, "kid", t, "grin"), bg=hexc("#ffd84d"))
    portrait(cr, t, b8, 610, 800, 82, "teacher", mouth=mouth_of(tl, "teacher", t, "smug"),
             eyes="half" if t < b9 else "wide", brows="raise" if t < b9 else "up", bg=hexc("#cdb8ff"),
             sweat=t >= b9 + 0.3)
    portrait(cr, t, b9, 110, 800, 82, "kid", mouth=mouth_of(tl, "kid", t, "grin"), bg=hexc("#ffd84d"))
    vignette(cr, 0.35)


SQUARES = [hexc(c) for c in ("#8a5a2e", "#5cc8e8", "#ff8fb5", "#ff9a3c", "#e8473f", "#ffd84d", "#3fbf6a",
                             "#4a6ad0")]


SQ = (0, 260, 720, 520)    # the street's square on the game board (x, y, w, h)


def _board(cr):
    """The game board around the street (the street is one square of its bottom row)."""
    x0, y0, w, h = SQ
    cr.rectangle(-4000, -5000, 8720, 9000)
    cr.set_source(lin(0, -3000, 0, 2000, [(0, hexc("#2f6a4a")), (1, hexc("#1d4a33"))]))
    cr.fill()
    top = y0 - 4 * h
    rrect(cr, -2 * w - 40, top - 40, 5 * w + 80, 5 * h + 80, 30)
    paint(cr, hexc("#d8f0dc"), OUTLINE, 14)
    rrect(cr, -w, top + h, 3 * w, 3 * h, 20)
    paint(cr, rad(360, top + 2.5 * h, 1700, [(0, hexc("#e8f8ea")), (1, hexc("#bfe3c6"))]), OUTLINE, 10)
    bold_text(cr, "BUY  &  SELL", w / 2, top + 2.6 * h, 210, hexc("#e8473f"), ow=24)
    cells = [(k * w, y0) for k in (-2, -1, 1, 2)] + [(k * w, top) for k in range(-2, 3)]
    cells += [(-2 * w, top + j * h) for j in (1, 2, 3)] + [(2 * w, top + j * h) for j in (1, 2, 3)]
    for i, (x, y) in enumerate(cells):
        rrect(cr, x + 8, y + 8, w - 16, h - 16, 12)
        paint(cr, hexc("#f4fbf4"), OUTLINE, 9)
        rrect(cr, x + 8, y + 8, w - 16, 120, 12)
        paint(cr, SQUARES[i % len(SQUARES)], OUTLINE, 9)


def _street_bg(cr, full):
    x0, y0, w, h = SQ
    xa, xb, ya, yb = (-3000, 3720, -3000, 4000) if full else (x0, x0 + w, y0, y0 + h)
    cr.rectangle(xa, ya, xb - xa, 712 - ya)
    cr.set_source(lin(0, 0, 0, 712, [(0, hexc("#ffb27a")), (0.6, hexc("#ffe2b8")), (1, hexc("#fff1d6"))]))
    cr.fill()
    for k in range(5):     # far buildings
        bx = 20 + k * 150
        rrect(cr, bx, 712 - 160 - 50 * (k % 3), 110, 160 + 50 * (k % 3) + 10, 6)
        cr.set_source_rgba(*alpha(hexc("#e89a7a"), 0.55))
        cr.fill()
    cr.rectangle(xa, 712, xb - xa, yb - 712)
    cr.set_source(lin(0, 712, 0, 900, [(0, hexc("#8a8f9e")), (1, hexc("#5f6474"))]))
    cr.fill()
    for k in range(-20, 30):
        cr.rectangle(k * 120, 742, 60, 8)
        cr.set_source_rgba(1, 1, 1, 0.7)
        cr.fill()


def scene_street(cr, t, tl):
    A = tl.at
    b11, b12 = A("b11"), A("b12")
    reveal = A("b12", "playing")
    x0, y0, w, h = SQ
    z = camera(t, [(A("b10") - 0.3, (1.2, 360, 560)), (reveal, (0.17, 360, y0 - 1.5 * h))], dur=1.1)
    cr.rectangle(0, 0, W, H)
    cr.set_source_rgba(*hexc("#1d4a33"))
    cr.fill()
    cr.save()
    enter(cr, z)
    revealed = t >= reveal
    if revealed:
        _board(cr)
        cr.save()
        rrect(cr, x0 + 8, y0 + 8, w - 16, h - 16, 12)
        cr.clip()
    _street_bg(cr, not revealed)
    push = seg(t, A("b10", "pushes"), A("b10", "hotel.", end=True))
    cx = lerp(-120, 290, ease_out(push))
    hotel(cr, 570, 712, 0.7)
    car(cr, cx, 712, 0.62, RED, t, spin=-push * 12)
    person(cr, t, cx - 150, 712, 0.62, "reporter", fedora=None, suit=None, shirt=hexc("#3fbf6a"),
           pants=hexc("#c9a46a"), tie=None, eyes="sad" if t >= A("b10", "bankrupt.") else "open",
           mouth="o" if t >= A("b10", "bankrupt.") else "flat", arms=("push", "push"), tilt=0.12,
           walk=t * 9 if push < 1 else None, seed=3)
    if revealed:
        cr.restore()
        rrect(cr, x0 + 8, y0 + 8, w - 16, h - 16, 12)
        paint(cr, None, OUTLINE, 9)
    cr.restore()
    if t >= reveal:   # dice and paper money tumble onto the board
        cue("whoosh", t, reveal)
        for k, (x, y, n) in enumerate(((200, 520, 5), (360, 600, 3))):
            st = reveal + 0.45 + 0.15 * k
            if t >= st:
                u = ease_out(seg(t, st, st + 0.6))
                die(cr, lerp(x - 260, x, u), lerp(y - 300, y, u), 1.0, n, (1 - u) * 5 + 0.2 * k)
                cue("hit", t, st + 0.5)
        for k in range(4):
            st = reveal + 0.6 + 0.1 * k
            if t >= st:
                u = ease_out(seg(t, st, st + 0.7))
                money(cr, 500 + k * 36, lerp(300, 620 + k * 26, u), -0.3 + 0.2 * k + (1 - u) * 2, 0.9)
    stamp(cr, t, A("b10", "bankrupt."), 360, 330, "BANKRUPT!", col=RED, size=78, end=b11)
    sign(cr, t, A("b10", "Why?"), 360, 180, "WHY?", col=GOLD, size=80, end=b11 - 0.05)
    sign(cr, t, b11, 360, 180, "BAD PARKING?", col=PURPLE, size=64, end=b12 - 0.05)
    sign(cr, t, reveal, 360, 180, "IT'S A BOARD GAME!", col=GREEN, size=54, rot=0.03)
    if t < b11:
        portrait(cr, t, A("b10") + 0.05, 100, 330, 72, "kid", mouth=mouth_of(tl, "kid", t, "grin"),
                 bg=hexc("#ffd84d"), end=A("b10", "bankrupt.") - 0.1)
    portrait(cr, t, b11, 620, 340, 76, "teacher", mouth=mouth_of(tl, "teacher", t, "o"), eyes="open" if t < b12
             else "wide", brows="sad" if t < b12 else "up", bg=hexc("#cdb8ff"), sweat=True)
    portrait(cr, t, b12, 100, 340, 76, "kid", mouth=mouth_of(tl, "kid", t, "grin"), bg=hexc("#ffd84d"))
    vignette(cr, 0.4)


def scene_egg(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    b14, b15 = A("b14"), A("b15")
    win = A("b15", "win.")
    cam = camera(t, [(A("b13") - 0.3, (1.0, 360, 640)), (A("b13", "What"), (1.05, 360, 620))], dur=0.8)
    cr.save()
    enter(cr, cam)
    chalk(cr, t, A("b13", "What"), 110, 250, "What has to be", 46)
    chalk(cr, t, A("b13", "broken"), 110, 315, "BROKEN before", 46)
    chalk(cr, t, A("b13", "use"), 110, 380, "you can use it?", 46)
    talk = tl.speaking("teacher", t)
    hold_egg = t >= A("b15")

    def egg_prop(c, hx, hy):
        egg(c, t, A("b15", "egg."), hx + 20, hy - 50, 0.9)

    person(cr, t, 520, 900, 1.0, "teacher", facing=-1, eyes="happy" if (t < A("b13", "My") or t >= win) else "half",
           mouth="talk" if talk else ("grin" if t >= win else "smug"), brows="raise" if b14 <= t < b15 else None,
           arms=("hold", "hips") if hold_egg and t < win else (("wave", "down") if t >= win else ("point", "hips")),
           hold=egg_prop if hold_egg and t < win else None)
    cr.restore()
    if t >= win:
        trophy(cr, t, win, 200, 720, 1.0)
        sparkles(cr, t, win, 200, 620, n=10, seed=9, col=GOLD, spread=150)
    sign(cr, t, A("b13", "My"), 360, 95, "MY TURN", col=PURPLE, size=56, end=b14 - 0.05)
    sign(cr, t, b14, 360, 95, "THE SCHOOL RULES?", col=RED, size=52, end=b15 - 0.05)
    sign(cr, t, A("b15", "egg."), 360, 95, "AN EGG.", col=GOLD, size=70, end=win - 0.05)
    sign(cr, t, win, 360, 95, "YOU WIN.", col=GREEN, size=70, end=A("b15", "Pick") - 0.05)
    sign(cr, t, A("b15", "Pick"), 360, 95, "PICK ANY SEAT", col=BLUE, size=60)
    portrait(cr, t, b14, 130, 760, 84, "kid", mouth=mouth_of(tl, "kid", t, "grin"), eyes="happy" if t < b15 else
             "wide", bg=hexc("#ffd84d"), end=b15 + 0.6)
    vignette(cr, 0.4)


def scene_seat(cr, t, tl):
    A = tl.at
    room(cr, t)
    b17 = A("b17")
    nxt = A("b17", "next")
    cam = camera(t, [(A("b16") - 0.3, (1.0, 360, 640)), (A("b16") + 0.4, (1.55, 600, 470))], dur=0.8)
    cr.save()
    enter(cr, cam)
    glum = t >= nxt
    slide = ease_out(seg(t, A("b17", "Then"), A("b17", "Then") + 0.7))

    def teacher_seat(c, tt, x, dy, s):
        if t < A("b17", "Then"):
            return
        tx = lerp(900, 720, slide)
        chair(c, tx, dy + 90 * s, s)
        person(c, tt, tx, dy + 70 * s, s * 0.95, "teacher", facing=-1,
               eyes="happy" if not tl.speaking("teacher", tt) else "open",
               mouth="talk" if tl.speaking("teacher", tt) else "grin", arms=("front", "front"), look=(0.6, 0))

    classroom(cr, t, tl, kid_pose=dict(eyes="half" if glum else "happy", mouth="flat" if glum else (
        "talk" if tl.speaking("kid", t) else "grin"), arms=("front", "front") if t >= b17 else ("hips", "hips"),
        look=(0.6, 0) if glum else (0, 0), brows="flat" if glum else "raise"), extra=teacher_seat)
    cr.restore()
    sign(cr, t, A("b16"), 360, 170, "LAST BENCH!", col=GOLD, size=72, end=b17 - 0.05)
    sign(cr, t, b17, 360, 170, "GOOD.", col=PURPLE, size=72, end=nxt - 0.05)
    stamp(cr, t, nxt, 360, 190, "PLOT TWIST", col=RED, size=76)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b18"), 360, 190, "WHICH ONE GOT YOU?", col=GOLD, size=52)
    icons = ("pill", "house", "car")
    for k, (key, col) in enumerate((("one,", BLUE), ("two,", GREEN), ("three?", RED))):
        st = A("b18") + 0.15 * k
        if t < st:
            continue
        said = A("b18", key)
        kk = appear(t, st, 0.35) * (1 + 0.18 * math.sin(math.pi * seg(t, said, said + 0.35)))
        x, y = 140 + k * 220, 470
        cr.save()
        cr.translate(x, y + math.sin(t * 3 + k) * 5)
        cr.scale(kk, kk)
        soft_disc(cr, 0, 14, 104, (0, 0, 0, 0.3))
        cr.arc(0, 0, 96, 0, 2 * math.pi)
        paint(cr, rad(-30, -40, 130, [(0, shade(col, 0.45)), (1, shade(col, -0.2))]), OUTLINE, 7)
        if icons[k] == "pill":
            pill(cr, 0, -10, 0.85, 0.5)
        elif icons[k] == "house":
            house(cr, 0, 40, GREEN, 0.42, glass=1.0)
        else:
            car(cr, 0, 26, 0.38, hexc("#ffd84d"))
        bold_text(cr, str(k + 1), 0, 150, 74, WHITE)
        cr.restore()
    person(cr, t, 360, 858, 0.5, "kid", eyes="happy", mouth="grin", arms=("wave", "hips"))
    vignette(cr, 0.35)


SCENES = {"board1": scene_board1, "back": scene_back, "deal": scene_deal, "pills": scene_pills,
          "houses": scene_houses, "street": scene_street, "egg": scene_egg, "seat": scene_seat, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
