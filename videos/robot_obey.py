"""The Robot That Must Obey -- genie-style story #1 (out/scripts_genie_style_batch1.md, approved by the owner on
14 Oct 2026: "make the genie scripts"). A home robot's one rule is to obey every order; the kid orders it to
disobey this order. Original story. Narrated by ElevenLabs Chris (owner: "Chris is good ... for emotions").
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, INKC, PURPLE, RED, buttons, card, check, knot, shake, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, light_rays, lin, paint, particles, put, rad, rrect, shade, sign, smooth,
                           soft_disc, soft_rrect, sprite, stamp, stroke_line, vignette)
from motion.toons import person
from motion.toons import _limb

NARRATOR = dict(engine="elevenlabs")
TAIL = 0.9
voice.SPEAKERS.update({
    "robot": dict(el=voice.ELEVEN["daniel"], pitch=-1.0, tone="flat, robotic",
                  fx="flanger=delay=2:depth=2:speed=0.6,aecho=0.8:0.5:14:0.35"),
    "kid": dict(el=voice.ELEVEN["liam"], pitch=2.5, tone="mischievously"),
})

SCRIPT = [
    dict(id="r1", scene="rule", text="A robot has one rule. It must obey every order.", tone="curious"),
    dict(id="r2", scene="rule", text="Give me an order. I will obey.", speaker="robot", gap=0.3),
    dict(id="r3", scene="clean", text="Clean the room. Done.", gap=0.3, tone="excited"),
    dict(id="r4", scene="homework", text="Do the homework. Done.", tone="excited"),
    dict(id="r5", scene="smile", text="Then the kid smiles, and gives one more order.", tone="mischievously"),
    dict(id="r6", scene="order", text="Disobey this order.", speaker="kid", gap=0.4, pace=0.92),
    dict(id="r7", scene="freeze", text="The robot freezes.", gap=0.45, pace=0.92, tone="dramatic"),
    dict(id="r8", scene="logic", text="If it obeys, it has to disobey. So it breaks the rule."),
    dict(id="r9", scene="logic", text="If it disobeys, that's exactly what the order said. So it obeyed."),
    dict(id="r10", scene="logic", text="Either way, it can't follow its own rule.", pace=0.95),
    dict(id="r11", scene="smoke", text="Smoke comes out of its ears. Beep.", gap=0.3, tone="amused"),
    dict(id="r12", scene="relax", text="Meanwhile, the homework is done. Perfectly.", tone="amused"),
    dict(id="r13", scene="end", text="So what should the robot do? Obey, or disobey?", gap=0.3, pace=0.95,
         tone="curious"),
]

METADATA = dict(
    title="1 Order Broke This Robot 🤖",
    alt_titles=["The Robot Must Obey… Then the Kid Said THIS 🤖", "\"Disobey This Order.\" The Robot Froze 🤯",
                "The Order No Robot Can Follow 🤖"],
    description="""A robot has one rule: it must obey every order. 🤖

Clean the room. Done. Do the homework. Done. Then the kid smiles, and gives one more order:
"Disobey this order."

The robot freezes. If it obeys, it has to disobey, so it breaks the rule. If it disobeys, that's exactly what the order said, so it obeyed. Either way, it can't follow its own rule.

Smoke comes out of its ears. Beep. Meanwhile, the homework is done. Perfectly. 😏

An original story built on a self-referential paradox, the same trap as "this sentence is false".

💬 So what should the robot do? Obey, or disobey? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Paradox", "#Robot", "#Shorts"],
    tags=["robot paradox", "disobey this order", "obey paradox", "self reference paradox", "paradox",
          "brain teaser", "funny story", "logic puzzle", "mind blowing", "interestingly strange"],
    pinned_comment="Obey or disobey? Wrong answers only 🤖👇",
)

METAL = hexc("#cfd8e6")
GLOW = hexc("#4fe3ff")
WALL = hexc("#ffd9a8")


# ---------------------------------------------------------------- the bedroom
def _bedroom(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 800, [(0, hexc("#ffe7c2")), (1, WALL)]))
    c.fill()
    for x in range(-20, W + 40, 72):             # wallpaper stripes
        c.rectangle(x, 0, 30, 800)
        c.set_source_rgba(1, 1, 1, 0.18)
        c.fill()
    soft_rrect(c, 420, 150, 240, 280, 14, (0, 0, 0, 0.2), sigma=10)     # window with a night sky
    rrect(c, 420, 140, 240, 280, 14)
    paint(c, lin(0, 140, 0, 420, [(0, hexc("#2a3a7a")), (1, hexc("#6a5ab8"))]), OUTLINE, 6)
    c.arc(560, 210, 30, 0, 2 * math.pi)
    paint(c, hexc("#fff4c8"), None, 0)
    rng = random.Random(8)
    for _ in range(14):
        c.arc(430 + rng.random() * 220, 150 + rng.random() * 260, 2.5, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.8)
        c.fill()
    c.rectangle(536, 140, 8, 280)
    c.rectangle(420, 276, 240, 8)
    c.set_source_rgba(*hexc("#f4efe6"))
    c.fill()
    rrect(c, 70, 170, 200, 130, 8)               # a poster of a rocket
    paint(c, hexc("#7ad0ff"), OUTLINE, 4)
    smooth(c, [(170, 190), (195, 240), (185, 280), (155, 280), (145, 240)])
    paint(c, WHITE, OUTLINE, 3)
    c.rectangle(0, 800, W, H - 800)              # floor
    c.set_source(lin(0, 800, 0, H, [(0, hexc("#b9855a")), (1, hexc("#8a5a34"))]))
    c.fill()
    c.rectangle(0, 796, W, 10)
    c.set_source_rgba(*hexc("#7a4a2a"))
    c.fill()
    ellipse(c, 360, 1000, 300, 70)               # rug
    paint(c, alpha(hexc("#e86a8a"), 0.6), None, 0)


def bedroom(cr, t):
    put(cr, sprite("robot_bedroom", W, H, _bedroom), 0, 0)
    light_rays(cr, t, 540, 160, n=3, a=0.05)


def bed(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 6, 200, 0.25)
    rrect(cr, -200, -150, 30, 160, 10)
    paint(cr, hexc("#7a4a2a"), OUTLINE, 4)
    rrect(cr, -190, -70, 390, 70, 14)
    paint(cr, lin(0, -70, 0, 0, [(0, hexc("#5a8ad8")), (1, hexc("#3a5aa8"))]), OUTLINE, 5)
    ellipse(cr, -130, -82, 52, 24)
    paint(cr, WHITE, OUTLINE, 4)
    cr.restore()


def mess(cr, t, k):
    """Toys, socks and paper all over the floor; `k` 0..1 is how far it has been swept away (to the right)."""
    rng = random.Random(5)
    for j in range(16):
        x0, y0 = 60 + rng.random() * 600, 830 + rng.random() * 220
        kind, rot, col = j % 4, rng.uniform(-1, 1), rng.choice([RED, GOLD, BLUE, GREEN, PURPLE])
        u = ease_out(seg(k, j / 32, j / 32 + 0.5))
        if u >= 1:
            continue
        x, y = lerp(x0, x0 + 900, u), lerp(y0, y0 - 200, u)
        cr.save()
        cr.translate(x, y)
        cr.rotate(rot + u * 6)
        if kind == 0:            # sock
            smooth(cr, [(-14, -30), (14, -30), (14, 10), (40, 18), (40, 34), (-14, 34)])
            paint(cr, col, OUTLINE, 3.5)
        elif kind == 1:          # crumpled paper
            cr.arc(0, 0, 20, 0, 2 * math.pi)
            paint(cr, hexc("#f4f0e6"), OUTLINE, 3.5)
            stroke_line(cr, [(-10, -6), (6, 2), (-4, 10)], 2, alpha(OUTLINE, 0.5))
        elif kind == 2:          # toy block
            rrect(cr, -20, -20, 40, 40, 6)
            paint(cr, col, OUTLINE, 3.5)
            bold_text(cr, "ABC"[j % 3], 0, 12, 30, WHITE, outline=None, shadow=0)
        else:                    # ball
            cr.arc(0, 0, 22, 0, 2 * math.pi)
            paint(cr, rad(-6, -6, 26, [(0, shade(col, 0.4)), (1, col)]), OUTLINE, 3.5)
        cr.restore()


def notebook(cr, t, x, y, s=1.0, flip=0.0, grade=0.0):
    """An open notebook; `flip` 0..1 riffles the pages, `grade` 0..1 stamps an A+."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_rrect(cr, -150, -90, 300, 200, 14, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -150, -100, 300, 200, 12)
    paint(cr, hexc("#3a5aa8"), OUTLINE, 5)
    for side in (-1, 1):
        rrect(cr, -140 if side < 0 else 4, -92, 136, 182, 6)
        paint(cr, hexc("#fffaf0"), OUTLINE, 3)
        for k in range(6):
            stroke_line(cr, [(side * 20 - (110 if side < 0 else -10), -60 + k * 26),
                             (side * 20 + (-20 if side < 0 else 100), -60 + k * 26)], 3, alpha(BLUE, 0.6), curve=False)
    if 0 < flip < 1:             # pages flying over
        for j in range(3):
            u = (flip * 3 - j) % 1.0
            cr.save()
            cr.scale(math.cos(u * math.pi), 1)
            rrect(cr, 0, -92, 136, 182, 6)
            paint(cr, hexc("#fffaf0"), OUTLINE, 3)
            cr.restore()
    if grade > 0:
        cr.save()
        cr.translate(70, 20)
        cr.rotate(-0.2)
        cr.scale(lerp(2, 1, grade), lerp(2, 1, grade))
        cr.arc(0, 0, 56, 0, 2 * math.pi)
        paint(cr, None, alpha(RED, grade), 7)
        bold_text(cr, "A+", 0, 20, 58, alpha(RED, grade), outline=None, shadow=0)
        cr.restore()
    cr.restore()


# ---------------------------------------------------------------- the robot
def robot(cr, t, x, y, s=1.0, eyes="open", talk=False, arms=("down", "down"), frozen=0.0, smoke=0.0, glow=0.0,
          seed=0):
    """A round home robot standing with its wheels at (x, y). eyes: open, happy, x, blink, spin."""
    cr.save()
    hover = math.sin(t * 3 + seed) * 4 * (1 - frozen)
    cr.translate(x, y + hover)
    cr.scale(s, s)
    ground_shadow(cr, 0, 6 - hover, 120, 0.3)
    jit = (math.sin(t * 60) * 3 if 0 < frozen < 1 else 0.0)
    cr.translate(jit, 0)
    for side in (-1, 1):         # wheels
        cr.arc(side * 60, -30, 34, 0, 2 * math.pi)
        paint(cr, rad(side * 60 - 8, -38, 40, [(0, hexc("#5a6478")), (1, hexc("#2b2f3a"))]), OUTLINE, 5)
        cr.arc(side * 60, -30, 12, 0, 2 * math.pi)
        paint(cr, METAL, OUTLINE, 3)
    for side in (-1, 1):         # arms (tubes with claw hands)
        a = arms[0] if side > 0 else arms[1]
        sx, sy = side * 104, -230
        hx, hy = {"down": (side * 140, -120), "up": (side * 150, -380), "salute": (side * 20, -400),
                  "out": (side * 220, -230), "hold": (side * 170, -180), "wave": (side * 200, -330)}[a]
        if a == "wave":
            hy += math.sin(t * 10) * 20
        _limb(cr, [(sx, sy), ((sx + hx) / 2 + side * 20, (sy + hy) / 2 + 10), (hx, hy)], 24, shade(METAL, -0.1))
        cr.arc(hx, hy, 20, 0, 2 * math.pi)
        paint(cr, rad(hx - 6, hy - 6, 24, [(0, WHITE), (1, METAL)]), OUTLINE, 4)
    rrect(cr, -110, -300, 220, 250, 60)       # body
    paint(cr, rad(-40, -240, 260, [(0, WHITE), (0.55, METAL), (1, shade(METAL, -0.25))]), OUTLINE, 6)
    rrect(cr, -60, -240, 120, 90, 18)        # chest panel
    paint(cr, hexc("#2b3550"), OUTLINE, 4)
    for k, col in enumerate((RED, GOLD, GREEN)):
        on = (math.sin(t * 6 + k * 2) > 0) and frozen < 0.5
        cr.arc(-30 + k * 30, -195, 11, 0, 2 * math.pi)
        paint(cr, col if on else shade(col, -0.55), OUTLINE, 2.5)
    stroke_line(cr, [(0, -440), (0, -500)], 6, OUTLINE, curve=False)    # antenna
    cr.arc(0, -505, 16, 0, 2 * math.pi)
    blink = 0.5 + 0.5 * math.sin(t * 8)
    paint(cr, alpha(RED, 0.5 + 0.5 * blink) if frozen < 0.5 else hexc("#7a8090"), OUTLINE, 3.5)
    ellipse(cr, 0, -380, 120, 92)            # head
    paint(cr, rad(-40, -420, 160, [(0, WHITE), (0.6, METAL), (1, shade(METAL, -0.2))]), OUTLINE, 6)
    for side in (-1, 1):                     # ear bolts
        cr.arc(side * 120, -380, 18, 0, 2 * math.pi)
        paint(cr, shade(METAL, -0.15), OUTLINE, 4)
    rrect(cr, -90, -430, 180, 90, 40)        # visor
    paint(cr, lin(0, -430, 0, -340, [(0, hexc("#1b2a44")), (1, hexc("#0e1626"))]), OUTLINE, 5)
    ec = GLOW if frozen < 0.5 else hexc("#8ab4c4")
    if glow > 0:
        soft_disc(cr, 0, -385, 140, alpha(GLOW, 0.35 * glow))
    for side in (-1, 1):
        ex, ey = side * 40, -388
        if eyes == "happy":
            cr.arc(ex, ey + 8, 18, math.pi * 1.1, math.pi * 1.9)
            paint(cr, None, ec, 7)
        elif eyes == "x":
            for d in (-1, 1):
                stroke_line(cr, [(ex - 14, ey - 14 * d), (ex + 14, ey + 14 * d)], 7, ec, curve=False)
        elif eyes == "spin":
            a = t * 9 * side
            cr.arc(ex, ey, 16, a, a + 4.5)
            paint(cr, None, ec, 6)
        else:
            h = 22 if eyes == "open" else 6
            ellipse(cr, ex, ey, 16, h)
            paint(cr, ec, None, 0)
    if talk:
        for k in range(5):
            hh = 6 + 12 * abs(math.sin(t * 18 + k))
            rrect(cr, -36 + k * 16, -352 - hh / 2, 9, hh, 4)
            paint(cr, ec, None, 0)
    else:
        stroke_line(cr, [(-30, -352), (30, -352)], 5, ec, curve=False)
    cr.restore()
    if frozen > 0:               # frost over the whole robot
        cr.save()
        cr.translate(x, y)
        cr.scale(s, s)
        rrect(cr, -130, -480, 260, 460, 70)
        cr.set_source_rgba(0.75, 0.9, 1.0, 0.35 * frozen)
        cr.fill()
        rng = random.Random(seed + 3)
        for _ in range(int(12 * frozen)):
            fx, fy = rng.uniform(-110, 110), rng.uniform(-470, -40)
            for a in range(3):
                ang = a * math.pi / 3
                stroke_line(cr, [(fx - 14 * math.cos(ang), fy - 14 * math.sin(ang)),
                                 (fx + 14 * math.cos(ang), fy + 14 * math.sin(ang))], 3, (1, 1, 1, 0.9), curve=False)
        cr.restore()
    if smoke > 0:                # smoke puffs from both ear bolts
        for side in (-1, 1):
            for k in range(5):
                u = ((t * 0.9 + k * 0.2) % 1.0)
                px = x + s * (side * 130 + side * u * 60 + math.sin(t * 3 + k) * 10)
                py = y + s * (-390 - u * 260)
                cr.arc(px, py, s * (18 + u * 34), 0, 2 * math.pi)
                cr.set_source_rgba(0.55, 0.55, 0.6, 0.55 * (1 - u) * smoke)
                cr.fill()


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


KID = dict(shirt=hexc("#ffb347"), tie=None, pants=hexc("#3a4a6a"))


# ---------------------------------------------------------------- scenes
def scene_rule(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.12, 360, 600)), (A("r2"), (1.0, 360, 640))], dur=0.8), drift=0.01, t=t)
    bed(cr, 470, 960, 0.8)
    sal = A("r1", "obey")
    robot(cr, t, 330, 1010, 0.95, eyes="happy" if t < A("r2") else "open", talk=tl.speaking("robot", t),
          arms=("salute", "down") if t >= sal else ("wave", "down"), glow=appear(t, A("r2"), 0.3))
    cr.restore()
    sign(cr, t, -0.5, 360, 150, "IT MUST OBEY", col=GOLD, size=78, end=A("r1", "It") - 0.05)
    card(cr, t, A("r1", "It"), 360, 190, 470, 150, "THE ONE RULE", ["OBEY EVERY ORDER"], col=BLUE, line_size=44,
         end=A("r2") - 0.05)
    if t >= A("r2"):
        tag(cr, t, A("r2", "obey."), 360, 160, "READY", col=GREEN, size=56)
    vignette(cr, 0.4)


def scene_clean(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    done = A("r3", "Done.")
    k = seg(t, A("r3", "room.") - 0.2, done + 0.3)
    cr.save()
    enter(cr, (1.0, 360, 640))
    bed(cr, 470, 960, 0.8)
    mess(cr, t, k)
    robot(cr, t, lerp(160, 560, ease_out(k)), 1010, 0.8, eyes="happy", arms=("out", "out"))
    if 0 < k < 1:
        cue("whoosh", t, A("r3", "room.") - 0.2, 0.6)
        particles(cr, t, 7, 24, (1, 1, 1, 0.7), area=(80, 820, 600, 220), r=(3, 8), speed=120)
    cr.restore()
    sign(cr, t, A("r3"), 360, 150, "ORDER 1: CLEAN THE ROOM", col=BLUE, size=46)
    check(cr, t, done, 360, 330, 70)
    vignette(cr, 0.4)


def scene_homework(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    done = A("r4", "Done.")
    cr.save()
    enter(cr, camera(t, [(A("r4") - 0.3, (1.0, 360, 640)), (A("r4") + 0.2, (1.25, 360, 700))], dur=0.6))
    robot(cr, t, 540, 1020, 0.8, eyes="spin" if t < done else "happy", arms=("hold", "hold"))
    notebook(cr, t, 300, 700, 1.0, flip=seg(t, A("r4"), done), grade=ease_out(seg(t, done, done + 0.3)))
    cr.restore()
    if t < done:
        cue("scribble", t, A("r4"), done - A("r4"))
    sign(cr, t, A("r4"), 360, 150, "ORDER 2: DO THE HOMEWORK", col=PURPLE, size=44)
    check(cr, t, done, 360, 330, 70)
    vignette(cr, 0.4)


def scene_smile(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("r5") - 0.3, (1.0, 360, 640)), (A("r5", "smiles,"), (1.35, 230, 600))], dur=0.7))
    robot(cr, t, 540, 1010, 0.8, eyes="happy", arms=("down", "down"))
    person(cr, t, 210, 1000, 0.85, "kid", eyes="half", mouth="smug" if t >= A("r5", "smiles,") else "smile",
           arms=("chin", "hips"), brows="raise" if t >= A("r5", "one") else None, look=(0.6, -0.2), **KID)
    cr.restore()
    sparkles(cr, t, A("r5", "smiles,"), 210, 560, n=6, seed=9, col=GOLD)
    sign(cr, t, A("r5", "one"), 360, 150, "ONE MORE ORDER", col=RED, size=62)
    vignette(cr, 0.45)


def scene_order(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("r6") - 0.3, (1.2, 260, 640)), (A("r6", "this"), (1.35, 250, 620))], dur=0.6))
    person(cr, t, 230, 1000, 0.9, "kid", eyes="half", mouth=mouth(tl, "kid", t, "smug"), arms=("point", "hips"),
           brows="raise", look=(0.8, -0.2), **KID)
    cr.restore()
    k = appear(t, A("r6") + 0.05, 0.4)
    if k > 0.01:
        cr.save()
        cr.translate(470, 330)
        cr.rotate(0.04)
        cr.scale(k, k)
        rrect(cr, -210, -140, 420, 280, 28)
        paint(cr, lin(0, -140, 0, 140, [(0, hexc("#fff8e6")), (1, hexc("#f4e4c4"))]), OUTLINE, 6)
        for j, ln in enumerate(("\"DISOBEY", "THIS", "ORDER.\"")):
            bold_text(cr, ln, 0, -54 + j * 70, 64, RED if j == 0 else INKC, outline=None, shadow=0)
        cr.restore()
    vignette(cr, 0.5)


def scene_freeze(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    fr = A("r7", "freezes.")
    dx, dy = shake(t, fr, 0.3, 8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("r7") - 0.3, (1.2, 360, 640))]))
    robot(cr, t, 360, 1010, 1.0, eyes="open" if t < fr else "blink", arms=("down", "down"),
          frozen=ease_out(seg(t, fr, fr + 0.4)))
    cr.restore()
    if t >= fr:
        cue("hit", t, fr)
    stamp(cr, t, fr, 360, 180, "FROZEN", col=hexc("#5a8ab8"), size=100)
    vignette(cr, 0.5)


def scene_logic(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a5a"), hexc("#6ab0d8"), seed=4)
    r8, r9, r10 = A("r8"), A("r9"), A("r10")
    if t < r10:
        card(cr, t, r8, 185, 330, 330, 300, "OBEY?", ["It must", "DISOBEY...", "rule broken!"],
             col=GREEN, mark="no", mark_at=A("r8", "breaks"), line_size=38)
        card(cr, t, r9, 535, 330, 330, 300, "DISOBEY?", ["That's what", "it was told...", "so it OBEYED!"],
             col=RED, mark="no", mark_at=A("r9", "obeyed."), line_size=38)
        if t >= r9:
            bold_text(cr, "OR", 360, 560, 60 * appear(t, r9, 0.3), GOLD)
        robot(cr, t, 360, 860, 0.5, eyes="spin", arms=("down", "down"))
    else:
        knot(cr, t, r10, 360, 380, 150, BLUE)
        robot(cr, t, 360, 860, 0.5, eyes="x" if t > r10 + 0.8 else "spin", arms=("up", "up"))
        sign(cr, t, A("r10", "can't"), 360, 140, "RULE BROKEN", col=RED, size=64)
    vignette(cr, 0.4)


def scene_smoke(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    beep = A("r11", "Beep.")
    dx, dy = shake(t, beep, 0.25, 6)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("r11") - 0.3, (1.15, 360, 600))]))
    robot(cr, t, 360, 1010, 1.0, eyes="x", arms=("down", "down"), frozen=0.3,
          smoke=ease_out(seg(t, A("r11", "Smoke"), A("r11", "Smoke") + 0.6)))
    cr.restore()
    if t >= beep:
        stamp(cr, t, beep, 360, 200, "BEEP.", col=RED, size=110)
    vignette(cr, 0.5)


def scene_relax(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    bed(cr, 400, 960, 0.9)
    robot(cr, t, 600, 1010, 0.6, eyes="x", arms=("down", "down"), smoke=0.6)
    person(cr, t, 250, 940, 0.75, "kid", eyes="happy", mouth="grin", arms=("hold", "chin"),
           hold=lambda c, hx, hy: notebook(c, t, hx + 40, hy - 40, 0.35, grade=1.0), tilt=-0.12, **KID)
    cr.restore()
    sign(cr, t, A("r12", "Meanwhile,"), 360, 150, "MEANWHILE...", col=GOLD, size=64)
    sparkles(cr, t, A("r12", "Perfectly."), 300, 600, n=8, seed=3, col=GOLD)
    if t >= A("r12", "Perfectly."):
        tag(cr, t, A("r12", "Perfectly."), 360, 290, "A+", col=RED, size=70)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    bedroom(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    robot(cr, t, 470, 1010, 0.8, eyes="spin", arms=("out", "out"), smoke=0.4)
    person(cr, t, 170, 1000, 0.7, "kid", eyes="half", mouth="smug", arms=("hips", "hips"), look=(0.6, -0.2), **KID)
    cr.restore()
    sign(cr, t, A("r13"), 360, 140, "WHAT SHOULD IT DO?", col=PURPLE, size=56)
    buttons(cr, t, A("r13", "Obey,"), [("OBEY", GREEN), ("DISOBEY", RED)], y=290)
    vignette(cr, 0.45)


SCENES = {"rule": scene_rule, "clean": scene_clean, "homework": scene_homework, "smile": scene_smile,
          "order": scene_order, "freeze": scene_freeze, "logic": scene_logic, "smoke": scene_smoke,
          "relax": scene_relax, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
