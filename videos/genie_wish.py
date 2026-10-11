"""The Genie's Last Wish -- an original Pinocchio-style story (liar-paradox wish) in the polished look.

A genie grants three wishes, "except more wishes". The kid, made the smartest in the world by wish two, wishes:
"I wish this wish does not come true." Granting it means it didn't come true; refusing means it did. Original
story, approved by the owner on 11 Oct 2026 (out/script_genie_wish.md).
"""
import math
import random

from motion import voice
from motion.engine import W, H, cairo, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, buttons, calendar, card, knot, shake,
                         sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter,
                           ground_shadow, lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc,
                           sprite, stamp, stroke_line, vignette)
from motion.toons import head, person
from motion.toons import _limb

NARRATOR = dict(speed=0.88)
TAIL = 0.9
voice.SPEAKERS.update({"genie": dict(voice="am_onyx", speed=0.95, pitch=-1.5),
                       "kid": dict(voice="am_puck", speed=1.04, pitch=2.5)})

SCRIPT = [
    dict(id="w1", scene="lamp", text="A genie gives a kid three wishes. With one rule."),
    dict(id="w2", scene="lamp", text="Anything you want. Except more wishes!", speaker="genie", gap=0.3),
    dict(id="w3", scene="choc", text="First wish. A mountain of chocolate.", gap=0.3),
    dict(id="w4", scene="smart", text="Second wish. To be the smartest kid in the world."),
    dict(id="w5", scene="smart", text="Now he's the smartest kid in the world. So he makes wish number three."),
    dict(id="w6", scene="wish3", text="I wish this wish does not come true.", speaker="kid", gap=0.4, pace=0.92),
    dict(id="w7", scene="freeze", text="The genie freezes.", gap=0.45, pace=0.92),
    dict(id="w8", scene="logic", text="If he grants it, the wish comes true. But the wish says it doesn't."),
    dict(id="w9", scene="logic", text="If he refuses, the wish doesn't come true. Which is exactly what the kid "
                                      "wished for."),
    dict(id="w10", scene="logic", text="Either way, the genie breaks his own magic.", pace=0.95),
    dict(id="w11", scene="wait", text="So the genie is still sitting there. Thinking.", gap=0.3),
    dict(id="w12", scene="eat", text="Meanwhile, the kid is on wish one. Still eating chocolate."),
    dict(id="w13", scene="end", text="So what should the genie do? Grant the wish, or not?", gap=0.3, pace=0.95),
]

METADATA = dict(
    title="The Kid Broke The Genie With ONE Wish 🧞‍♂️",
    alt_titles=["\"I Wish This Wish Doesn't Come True\" 🤯", "The Wish No Genie Can Grant 🧞"],
    description="""A genie gives a kid three wishes, with one rule: anything you want, except more wishes. 🧞‍♂️

First wish: a mountain of chocolate. Second wish: to be the smartest kid in the world. And the smartest kid in the world makes wish number three:
"I wish this wish does not come true."

The genie freezes. If he grants it, the wish comes true, but the wish says it doesn't. If he refuses, the wish doesn't come true, which is exactly what the kid wished for. Either way, the genie breaks his own magic.

So the genie is still sitting there, thinking. Meanwhile, the kid is still eating chocolate. 🍫

An original story built on the classic liar paradox ("this sentence is false").

💬 So what should the genie do? Grant it, or not? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Paradox", "#Genie", "#Shorts"],
    tags=["genie paradox", "three wishes", "wish paradox", "liar paradox", "paradox", "brain teaser",
          "funny story", "logic puzzle", "mind blowing", "interestingly strange"],
    pinned_comment="What would YOU have wished for instead? 🧞 Best wish gets pinned 👇",
)

GENIE = hexc("#5aa8ff")
VEST = hexc("#8a4fc9")
CHOC = hexc("#7a4a2a")


# ---------------------------------------------------------------- backgrounds and props
def _desert(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 820, [(0, hexc("#2a1e5a")), (0.6, hexc("#8a4fa8")), (1, hexc("#ff9a7a"))]))
    c.fill()
    rng = random.Random(3)
    for _ in range(90):
        c.arc(rng.uniform(0, W), rng.uniform(0, 520), rng.uniform(0.8, 2.2), 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, rng.uniform(0.3, 0.9))
        c.fill()
    c.arc(560, 230, 54, 0, 2 * math.pi)
    c.set_source(rad(560, 230, 54, [(0, (1, 1, 0.92, 1)), (1, (1, 0.9, 0.7, 1))]))
    c.fill()
    c.set_source_rgba(*hexc("#3a2458"))      # palace silhouette
    c.rectangle(60, 620, 300, 200)
    c.fill()
    for x, r in ((120, 50), (210, 74), (300, 50)):
        c.arc(x, 620, r, math.pi, 2 * math.pi)
        c.fill()
        c.move_to(x - 6, 620 - r)
        c.line_to(x, 620 - r - 40)
        c.line_to(x + 6, 620 - r)
        c.fill()
    for k, (col, y0, amp) in enumerate(((hexc("#e0a06a"), 800, 40), (hexc("#c9824a"), 860, 30))):
        c.move_to(0, H)
        for x in range(0, W + 41, 40):
            c.line_to(x, y0 - amp * math.sin(x / 150.0 + k * 1.7))
        c.line_to(W, H)
        c.close_path()
        c.set_source(lin(0, y0 - amp, 0, H, [(0, col), (1, shade(col, -0.3))]))
        c.fill()


def desert(cr, t):
    put(cr, sprite("desert_night", W, H, _desert), 0, 0)


def lamp(cr, t, x, y, s=1.0, glow=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if glow:
        soft_disc(cr, 0, -30, 120, (1, 0.85, 0.4, 0.4 * glow))
    ground_shadow(cr, 0, 6, 90, 0.25)
    gold = [(0, hexc("#fff0a8")), (0.45, GOLD), (1, hexc("#9a6a14"))]
    smooth(cr, [(-90, -20), (-60, -70), (40, -72), (80, -40), (150, -70), (170, -60), (110, -10), (40, 0), (-60, 0)])
    paint(cr, lin(-90, -72, 90, 0, gold), OUTLINE, 5)
    cr.arc(-110, -40, 28, -0.6 * math.pi, 0.6 * math.pi)       # handle
    paint(cr, None, OUTLINE, 12)
    cr.arc(-110, -40, 28, -0.6 * math.pi, 0.6 * math.pi)
    paint(cr, None, GOLD, 6)
    ellipse(cr, -10, -76, 40, 12)
    paint(cr, lin(-50, -88, 30, -64, gold), OUTLINE, 4)
    cr.arc(-10, -96, 12, 0, 2 * math.pi)
    paint(cr, lin(-22, -108, 2, -84, gold), OUTLINE, 3.5)
    ellipse(cr, -30, -46, 30, 8, -0.2)
    paint(cr, alpha(WHITE, 0.5), None, 0)
    cr.restore()


def smoke_tail(cr, t, x0, y0, x1, y1, w=90, col=GENIE):
    """The genie's swirling smoke tail from his waist (x0, y0) down to the lamp spout (x1, y1)."""
    n = 14
    for k in range(n):
        u = k / (n - 1)
        x = lerp(x0, x1, u) + math.sin(u * 7 + t * 3) * 40 * (1 - u)
        y = lerp(y0, y1, u)
        r = lerp(w, 10, u)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source(rad(x - r * 0.3, y - r * 0.3, r * 1.2, [(0, shade(col, 0.35)), (1, alpha(shade(col, -0.1), 0.9))]))
        cr.fill()


def genie(cr, t, x, y, s=1.0, eyes="open", mouth="smile", arms=("cross", "cross"), brows=None, look=(0.0, 0.0),
          lamp_xy=None, grey=0.0, cobwebs=0.0, rise=1.0, seed=0):
    """A big blue genie floating with his waist at (x, y); his smoke tail curls down to `lamp_xy`."""
    if rise <= 0.01:
        return
    cr.push_group()
    bob = math.sin(t * 2 + seed) * 6
    lx, ly = lamp_xy if lamp_xy else (x + 60, y + 330 * s)
    smoke_tail(cr, t, x, y + bob, lx, ly, 70 * s)
    cr.save()
    cr.translate(x, y + bob - (1 - rise) * 60)
    cr.scale(s * rise, s * rise)
    for side in (-1, 1):       # arms
        if arms[0] == "cross":
            pts = [(side * 100, -230), (side * 120, -150), (-side * 40, -150)]
        elif arms[0] == "up":
            pts = [(side * 100, -230), (side * 160, -310), (side * 150, -400)]
        elif arms[0] == "wag" and side > 0:
            pts = [(100, -230), (170, -270), (150 + 20 * math.sin(t * 12), -360)]
        elif arms[0] == "chin" and side > 0:
            pts = [(100, -230), (90, -170), (20, -260)]
        else:
            pts = [(side * 100, -230), (side * 130, -150), (side * 120, -70)]
        _limb(cr, pts, 44, GENIE)
        for bx, by in pts[1:2]:
            rrect(cr, bx - 26, by - 10, 52, 22, 8)
            paint(cr, GOLD, OUTLINE, 3.5)
        cr.arc(pts[-1][0], pts[-1][1], 26, 0, 2 * math.pi)
        paint(cr, rad(pts[-1][0] - 8, pts[-1][1] - 8, 30, [(0, shade(GENIE, 0.3)), (1, GENIE)]), OUTLINE, 4.5)
    smooth(cr, [(-110, -250), (0, -270), (110, -250), (90, -40), (0, -20), (-90, -40)])     # torso
    paint(cr, rad(-30, -200, 220, [(0, shade(GENIE, 0.35)), (0.6, GENIE), (1, shade(GENIE, -0.2))]), OUTLINE, 5.5)
    for side in (-1, 1):       # open purple vest
        smooth(cr, [(side * 110, -250), (side * 40, -258), (side * 30, -40), (side * 90, -40)])
        paint(cr, lin(0, -258, 0, -40, [(0, shade(VEST, 0.3)), (1, VEST)]), OUTLINE, 4.5)
    rrect(cr, -96, -60, 192, 34, 12)          # gold sash
    paint(cr, lin(0, -60, 0, -26, [(0, hexc("#fff0a8")), (1, GOLD)]), OUTLINE, 4.5)
    head(cr, t, 0, -350, 92, "seller", skin=GENIE, hair="topknot", hair_col=hexc("#1e130d"),
         stache=hexc("#1e130d"), eyes=eyes, mouth=mouth, brows=brows, look=look)
    for side in (-1, 1):       # gold earrings
        cr.arc(side * 94, -320, 12, 0, 2 * math.pi)
        paint(cr, None, GOLD, 5)
    cr.restore()
    pat = cr.pop_group()
    cr.set_source(pat)
    cr.paint()
    if grey > 0:               # turned to stone
        cr.set_source_rgba(0.62, 0.64, 0.68, 0.85 * grey)
        cr.mask(pat)
    if cobwebs > 0:
        for (cx, cy, d) in ((x - 150 * s, y - 520 * s, 1), (x + 150 * s, y - 470 * s, -1)):
            for k in range(5):
                a = math.pi / 2 * (k / 4)
                stroke_line(cr, [(cx, cy), (cx + d * math.cos(a) * 90 * cobwebs, cy + math.sin(a) * 90 * cobwebs)],
                            2, (1, 1, 1, 0.7), curve=False)
            for rr in (30, 55, 80):
                pts = [(cx + d * math.cos(math.pi / 2 * k / 4) * rr * cobwebs,
                        cy + math.sin(math.pi / 2 * k / 4) * rr * cobwebs) for k in range(5)]
                stroke_line(cr, pts, 2, (1, 1, 1, 0.6), curve=False)


def choc_mountain(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 6, 230, 0.3)
    cr.move_to(-230, 0)
    cr.curve_to(-160, -120, -60, -300, 0, -310)
    cr.curve_to(70, -300, 160, -120, 230, 0)
    cr.close_path()
    paint(cr, lin(-230, -310, 230, 0, [(0, shade(CHOC, 0.35)), (0.5, CHOC), (1, shade(CHOC, -0.3))]), OUTLINE, 6)
    for k in range(5):     # chocolate-bar squares
        for j in range(k + 1):
            bx, by = -20 * k + j * 40, -270 + k * 52
            rrect(cr, bx - 16, by - 18, 32, 36, 6)
            paint(cr, alpha(shade(CHOC, 0.2), 0.8), alpha(OUTLINE, 0.4), 2)
    smooth(cr, [(-60, -250), (0, -312), (60, -250), (30, -230), (0, -250), (-30, -228)])     # melted top
    paint(cr, shade(CHOC, -0.15), OUTLINE, 4)
    cr.restore()


def bar(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy - 20)
    cr.rotate(-0.3)
    rrect(cr, -18, -40, 36, 60, 5)
    paint(cr, lin(0, -40, 0, 20, [(0, shade(CHOC, 0.3)), (1, CHOC)]), OUTLINE, 3.5)
    rrect(cr, -20, 0, 40, 26, 4)
    paint(cr, RED, OUTLINE, 3)
    cr.restore()


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- scenes
def scene_lamp(cr, t, tl):
    A = tl.at
    desert(cr, t)
    pop = A("w1", "genie")
    rise = ease_out(seg(t, pop, pop + 0.9))
    cam = camera(t, [(0, (1.0, 360, 640)), (A("w2"), (1.08, 360, 600))], dur=0.6)
    cr.save()
    enter(cr, cam)
    rub = math.sin(t * 14) * 8 if t < pop else 0.0
    lamp(cr, t, 470 + rub, 900, 0.9, glow=1.0 if t >= pop - 0.3 else 0.0)
    if t >= pop:
        cue("whoosh", t, pop, 0.6)
        particles(cr, t, 5, 30, (0.75, 0.6, 1.0, 0.6 * (1 - seg(t, pop, pop + 1.5))), area=(380, 600, 260, 300),
                  r=(4, 12), speed=60)
    genie(cr, t, 380, 560, 0.85, eyes="happy" if t < A("w2") else "half", mouth=mouth(tl, "genie", t, "grin"),
          arms=("wag", "down") if t >= A("w2", "Except") else ("up", "up") if t < A("w2") else ("cross", "cross"),
          lamp_xy=(470 + 120 * 0.9, 900 - 62 * 0.9), rise=rise, brows="raise" if t >= A("w2", "Except") else None)
    person(cr, t, 170, 930, 0.75, "kid", eyes="wide" if t >= pop else "open", mouth="o" if t >= pop else "smile",
           arms=("face", "face") if pop <= t < A("w2") else ("hold", "down"), look=(0.6, -0.4))
    cr.restore()
    sign(cr, t, A("w1", "three"), 360, 140, "3 WISHES", col=GOLD, size=72, end=A("w1", "rule.") - 0.05)
    sign(cr, t, A("w1", "rule."), 360, 140, "ONE RULE", col=PURPLE, size=72, end=A("w2", "Except") - 0.05)
    stamp(cr, t, A("w2", "Except"), 360, 160, "NO EXTRA WISHES", col=RED, size=58)
    vignette(cr, 0.45)


def scene_choc(cr, t, tl):
    A = tl.at
    desert(cr, t)
    land = A("w3", "mountain")
    drop = ease_out(seg(t, land, land + 0.5))
    dx, dy = shake(t, land + 0.45, 0.35, 10)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, (1.0, 360, 640))
    if t >= land:
        choc_mountain(cr, t, 420, lerp(-200, 900, drop), 1.15)
        if drop >= 1:
            cue("thud", t, land + 0.45)
    person(cr, t, 140, 930, 0.72, "kid", eyes="happy" if t >= land + 0.5 else "open",
           mouth="grin" if t >= land + 0.5 else "o", arms=("up", "up") if t >= land + 0.5 else ("down", "down"))
    cr.restore()
    sparkles(cr, t, land + 0.5, 400, 600, n=10, seed=4, col=GOLD, spread=180)
    tag(cr, t, A("w3"), 360, 250, "WISH 1", col=GOLD, size=52)
    sign(cr, t, land, 360, 140, "A MOUNTAIN OF CHOCOLATE", col=hexc("#a8692e"), size=44)
    vignette(cr, 0.45)


def scene_smart(cr, t, tl):
    A = tl.at
    desert(cr, t)
    w5 = A("w5")
    smart = A("w4", "smartest")
    cr.save()
    enter(cr, camera(t, [(A("w4") - 0.3, (1.0, 360, 640)), (w5, (1.25, 330, 580))], dur=0.6))
    if t >= smart:
        soft_disc(cr, 330, 520, 230, (0.6, 0.85, 1.0, 0.35 + 0.1 * math.sin(t * 6)))
    person(cr, t, 330, 930, 0.95, "kid", glasses=t >= smart, eyes="half" if t >= w5 else "happy",
           mouth="smug" if t >= w5 else "grin", arms=("chin", "hips") if t >= w5 else ("hips", "hips"),
           brows="raise" if t >= w5 else None)
    cr.restore()
    sparkles(cr, t, smart, 330, 330, n=8, seed=6, col=WHITE)
    tag(cr, t, A("w4"), 360, 250, "WISH 2", col=GOLD, size=52, end=w5 - 0.05)
    if t < w5:
        counter(cr, t, smart, 360, 160, 200, size=96, dur=1.0, col=GOLD, prefix="IQ ")
    card(cr, t, A("w5", "three."), 540, 250, 280, 160, "WISH 3", ["Hmm..."], col=PURPLE, line_size=46)
    vignette(cr, 0.45)


def scene_wish3(cr, t, tl):
    A = tl.at
    desert(cr, t)
    cam = camera(t, [(A("w6") - 0.3, (1.15, 260, 600)), (A("w6", "not"), (1.3, 250, 580))], dur=0.6)
    cr.save()
    enter(cr, cam)
    person(cr, t, 250, 930, 0.95, "kid", glasses=True, eyes="half", mouth=mouth(tl, "kid", t, "smug"),
           arms=("point", "hips"), brows="raise")
    cr.restore()
    k = appear(t, A("w6") + 0.05, 0.4)
    if k > 0.01:
        cr.save()
        cr.translate(470, 330)
        cr.rotate(0.04)
        cr.scale(k, k)
        rrect(cr, -210, -150, 420, 300, 28)
        paint(cr, lin(0, -150, 0, 150, [(0, hexc("#fff8e6")), (1, hexc("#f4e4c4"))]), OUTLINE, 6)
        for j, ln in enumerate(("\"I WISH", "THIS WISH", "DOES NOT", "COME TRUE.\"")):
            bold_text(cr, ln, 0, -78 + j * 62, 52, RED if j == 2 else INKC, outline=None, shadow=0)
        cr.restore()
    vignette(cr, 0.5)


def scene_freeze(cr, t, tl):
    A = tl.at
    desert(cr, t)
    fr = A("w7", "freezes.")
    g = seg(t, fr, fr + 0.4)
    dx, dy = shake(t, fr, 0.3, 8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("w7") - 0.3, (1.15, 360, 520))]))
    lamp(cr, t, 470, 900, 0.9)
    genie(cr, t, 360, 600, 0.95, eyes="wide", mouth="o", brows="up", arms=("down", "down"),
          lamp_xy=(470 + 108, 900 - 56), grey=g)
    cr.restore()
    if t >= fr:
        cue("hit", t, fr)
    stamp(cr, t, fr, 360, 180, "FROZEN", col=hexc("#5a6478"), size=100)
    vignette(cr, 0.5)


def scene_logic(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#4a3a7a"), hexc("#c99adf"), seed=3)
    w8, w9, w10 = A("w8"), A("w9"), A("w10")
    if t < w10:
        card(cr, t, w8, 185, 330, 330, 300, "GRANT IT?", ["Wish comes true...", "but it says", "it DOESN'T!"],
             col=GREEN, mark="no", mark_at=A("w8", "doesn't."), line_size=36)
        card(cr, t, w9, 535, 330, 330, 300, "REFUSE?", ["Wish doesn't", "come true...", "so it DID!"],
             col=RED, mark="no", mark_at=A("w9", "wished"), line_size=36)
        if t >= w9:
            bold_text(cr, "OR", 360, 560, 60 * appear(t, w9, 0.3), GOLD)
        genie(cr, t, 360, 760, 0.42, eyes="wide", mouth="o", brows="up", arms=("chin", "down"),
              lamp_xy=(420, 900), grey=0.0)
    else:
        knot(cr, t, w10, 360, 380, 150, PURPLE)
        spin = (t - w10) * 5
        genie(cr, t, 360, 760, 0.42, eyes="x" if t > w10 + 0.8 else "wide", mouth="o", brows="up",
              arms=("up", "up"), lamp_xy=(360 + 120 * math.sin(spin), 900))
        sign(cr, t, A("w10", "breaks"), 360, 140, "MAGIC BROKEN", col=RED, size=64)
    vignette(cr, 0.4)


def scene_wait(cr, t, tl):
    A = tl.at
    desert(cr, t)
    th = A("w11", "Thinking.")
    pages = ("1 DAY", "1 YEAR", "300 YEARS")
    k = min(2, int(max(0.0, t - A("w11", "still")) / 0.5)) if t >= A("w11", "still") else 0
    cr.save()
    enter(cr, (1.0, 360, 640))
    lamp(cr, t, 470, 900, 0.9)
    genie(cr, t, 360, 600, 0.95, eyes="half", mouth="flat", arms=("chin", "down"), lamp_xy=(470 + 108, 900 - 56),
          grey=0.35, cobwebs=seg(t, A("w11", "still") + 0.6, th + 0.8))
    cr.restore()
    calendar(cr, t, A("w11", "still"), 580, 260, "STILL THINKING", pages[k], col=PURPLE, s=0.85)
    if t >= th:
        for j in range(3):
            if t >= th + 0.2 * j:
                cr.arc(250 - j * 40, 230 - j * 35, 12 + j * 5, 0, 2 * math.pi)
                paint(cr, WHITE, OUTLINE, 4)
    vignette(cr, 0.5)


def scene_eat(cr, t, tl):
    A = tl.at
    desert(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    choc_mountain(cr, t, 430, 900, 0.95)
    chew = abs(math.sin(t * 9))
    person(cr, t, 170, 930, 0.8, "kid", glasses=True, eyes="happy", mouth="talk" if chew > 0.5 else "grin",
           arms=("hold", "hips"), hold=bar)
    cr.restore()
    for k in range(4):     # crumbs
        u = ((t * 1.2 + k * 0.25) % 1.0)
        cr.arc(240 + k * 12, 600 + u * 300, 5, 0, 2 * math.pi)
        paint(cr, CHOC, None, 0)
    sign(cr, t, A("w12", "Meanwhile,"), 360, 140, "MEANWHILE...", col=hexc("#a8692e"), size=64)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    desert(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    lamp(cr, t, 470, 930, 0.85)
    genie(cr, t, 380, 640, 0.8, eyes="half", mouth="flat", arms=("chin", "down"), lamp_xy=(470 + 102, 930 - 53))
    person(cr, t, 150, 950, 0.7, "kid", glasses=True, eyes="half", mouth="smug", arms=("hips", "hold"),
           hold_back=bar)
    cr.restore()
    sign(cr, t, A("w13"), 360, 140, "WHAT SHOULD HE DO?", col=PURPLE, size=56)
    buttons(cr, t, A("w13", "Grant"), [("GRANT", GREEN), ("REFUSE", RED)], y=290)
    vignette(cr, 0.45)


SCENES = {"lamp": scene_lamp, "choc": scene_choc, "smart": scene_smart, "wish3": scene_wish3,
          "freeze": scene_freeze, "logic": scene_logic, "wait": scene_wait, "eat": scene_eat, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
