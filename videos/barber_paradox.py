"""The Barber Paradox -- Pinocchio-style paradox in the polished look.

The village barber shaves all and only those villagers who do not shave themselves: who shaves the barber? Bertrand
Russell mentions the puzzle (as one suggested to him) in "The Philosophy of Logical Atomism" (The Monist, 1918-19).
The usual resolution: no such barber can exist. Wikipedia "Barber paradox".
Script approved by the owner on 9 Oct 2026 (out/scripts_paradox_batch2.md) with an everyday example, a clever
closing question and character voices added at the owner's request; the rule (line r3) is said by the barber himself.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, calendar, card, check, knot,
                         red_x, shake, sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, ground_shadow,
                           light_rays, lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc,
                           soft_rrect, sprite, stamp, stroke_line, vignette)
from motion.toons import person, portrait

NARRATOR = dict(speed=0.92)
TAIL = 0.9
voice.SPEAKERS.update({"barber": dict(voice="bm_daniel", speed=1.04)})

SCRIPT = [
    dict(id="r1", scene="hook", text="This barber cannot exist. Here's why."),
    dict(id="r2", scene="rule", text="In one village, the barber has one rule."),
    dict(id="r3", scene="rule", text="I shave everyone who doesn't shave themselves. And only them!",
         speaker="barber", gap=0.3),
    dict(id="r4", scene="mirror", text="Simple. So who shaves the barber?", gap=0.3),
    dict(id="r5", scene="logic", text="If he shaves himself, he's a man who shaves himself. And the barber never "
                                      "shaves those men. So he can't."),
    dict(id="r6", scene="logic", text="If he doesn't shave himself, he's a man who doesn't shave himself. And the "
                                      "barber must shave all of those. So he has to."),
    dict(id="r7", scene="logic", text="Either way, he breaks his own rule.", pace=0.95),
    dict(id="r8", scene="sign", text="It's the same trap as a sign that says: ignore this sign. If you ignore it... "
                                     "you just followed it."),
    dict(id="r9", scene="russell", text="The famous thinker Bertrand Russell wrote about this puzzle in [nineteen "
                                        "eighteen.|1918.]"),
    dict(id="r10", scene="vanish", text="And the answer most people accept? A barber like that simply can't exist."),
    dict(id="r11", scene="end", text="So who shaves the barber? Wrong answers only.", gap=0.3, pace=0.95),
]

METADATA = dict(
    title="The Barber Who Can't Exist 💈 (Try to Solve It)",
    alt_titles=["Who Shaves the Barber? The Question That Breaks Logic 💈", "This Barber Cannot Exist. Here's Why 🤯"],
    description="""This barber cannot exist. Here's why. 💈

In one village, the barber has one rule: "I shave everyone who doesn't shave themselves. And only them!"
Simple. So who shaves the barber?

If he shaves himself, he's a man who shaves himself, and the barber never shaves those men. So he can't.
If he doesn't shave himself, he's a man who doesn't shave himself, and the barber must shave all of those. So he has to.
Either way, he breaks his own rule.

Same trap as a sign that says "ignore this sign": if you ignore it... you just followed it.

The famous thinker Bertrand Russell wrote about this puzzle in 1918 (The Philosophy of Logical Atomism). The answer most people accept: a barber like that simply can't exist.

💬 So who shaves the barber? Wrong answers only 👇

🔔 Interestingly Strange: mind-bending paradoxes, weird animals, bizarre history and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#Logic", "#Shorts"],
    tags=["barber paradox", "who shaves the barber", "russell paradox", "bertrand russell", "logic paradox",
          "paradox", "brain teaser", "mind blowing", "self reference", "interestingly strange"],
    pinned_comment="Who shaves the barber? WRONG answers only 💈😂👇",
)

TILE = hexc("#e8f4f0")


# ---------------------------------------------------------------- backgrounds and props
def _shop(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 860, [(0, hexc("#bfe6dc")), (1, hexc("#e8f6f0"))]))
    c.fill()
    for y in range(0, 860, 60):       # tiled wall
        for x in range(0, W, 60):
            rrect(c, x + 3, y + 3, 54, 54, 6)
            c.set_source_rgba(1, 1, 1, 0.35 if (x // 60 + y // 60) % 2 else 0.18)
            c.fill()
    c.rectangle(0, 860, W, H - 860)
    for y in range(860, H, 70):       # checkered floor
        for x in range(0, W, 70):
            c.rectangle(x, y, 70, 70)
            c.set_source_rgba(*(hexc("#2b2b33") if (x // 70 + y // 70) % 2 else hexc("#f4f0e6")))
            c.fill()
    soft_rrect(c, 120, 170, 480, 400, 30, (0, 0, 0, 0.3), sigma=12)     # the big mirror
    rrect(c, 110, 160, 500, 400, 30)
    paint(c, lin(0, 160, 0, 560, [(0, hexc("#d9a64e")), (1, hexc("#9a6a20"))]), OUTLINE, 6)
    rrect(c, 130, 180, 460, 360, 20)
    paint(c, lin(130, 180, 590, 540, [(0, hexc("#e8f6ff")), (0.5, hexc("#bcd8ec")), (1, hexc("#dff0fa"))]),
          OUTLINE, 3)
    for k in range(3):
        stroke_line(c, [(180 + k * 40, 220), (240 + k * 40, 160 + 120)], 8, (1, 1, 1, 0.35), curve=False)


def shop(cr, t):
    put(cr, sprite("barbershop", W, H, _shop), 0, 0)
    light_rays(cr, t, 600, 0, n=3, a=0.05)


def pole(cr, t, x, y, h=300):
    rrect(cr, x - 30, y - h, 60, h, 30)
    cr.save()
    rrect(cr, x - 30, y - h, 60, h, 30)
    cr.clip()
    cr.set_source_rgba(*WHITE)
    cr.paint()
    off = (t * 60) % 60
    for k in range(-2, int(h / 30) + 3):
        yy = y - h + k * 30 - off
        cr.move_to(x - 40, yy)
        cr.line_to(x + 40, yy - 30)
        cr.line_to(x + 40, yy - 15)
        cr.line_to(x - 40, yy + 15)
        cr.close_path()
        cr.set_source_rgba(*(RED if k % 2 else BLUE))
        cr.fill()
    cr.restore()
    rrect(cr, x - 30, y - h, 60, h, 30)
    paint(cr, None, OUTLINE, 5)
    for yy in (y - h - 14, y + 4):
        rrect(cr, x - 38, yy - 10, 76, 22, 10)
        paint(cr, hexc("#cfd5df"), OUTLINE, 4)


def razor(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.7)
    rrect(cr, -6, 0, 12, 60, 5)
    paint(cr, hexc("#2b2b33"), OUTLINE, 3)
    rrect(cr, -10, -46, 20, 48, 4)
    paint(cr, lin(-10, 0, 10, 0, [(0, WHITE), (1, hexc("#b8c4d4"))]), OUTLINE, 3.5)
    cr.restore()


def scissors(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.4 + 0.15 * math.sin(hx))
    for side in (-1, 1):
        cr.save()
        cr.rotate(side * 0.18)
        cr.move_to(0, 0)
        cr.line_to(-5, -62)
        cr.line_to(5, -62)
        cr.close_path()
        paint(cr, hexc("#dfe6ee"), OUTLINE, 3)
        cr.arc(side * 10, 16, 10, 0, 2 * math.pi)
        paint(cr, None, RED, 5)
        cr.restore()
    cr.restore()


def chair(cr, x, y, s=1.0, spin=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s * (math.cos(spin) if abs(math.cos(spin)) > 0.15 else 0.15), s)
    rrect(cr, -12, -130, 24, 130, 6)
    paint(cr, hexc("#cfd5df"), OUTLINE, 4)
    ellipse(cr, 0, 0, 90, 16)
    paint(cr, hexc("#8a94a8"), OUTLINE, 4)
    rrect(cr, -100, -190, 200, 70, 24)
    paint(cr, lin(0, -190, 0, -120, [(0, hexc("#ff6a5a")), (1, hexc("#b8262a"))]), OUTLINE, 5)
    rrect(cr, -90, -370, 180, 190, 30)
    paint(cr, lin(0, -370, 0, -180, [(0, hexc("#ff6a5a")), (1, hexc("#b8262a"))]), OUTLINE, 5)
    cr.restore()


def glitchy(cr, t, draw, amount=1.0, seed=0):
    """Draw something with an RGB-split flicker, as if it can't decide whether it exists."""
    if amount <= 0:
        draw(cr)
        return
    rng = random.Random(int(t * 12) + seed)
    jx = rng.uniform(-10, 10) * amount
    for dx, col in ((-8 * amount + jx, (1, 0.2, 0.3)), (8 * amount + jx, (0.2, 0.9, 1.0))):
        cr.push_group()
        cr.translate(dx, 0)
        draw(cr)
        cr.pop_group_to_source()
        cr.paint_with_alpha(0.28 * amount)
    cr.push_group()
    draw(cr)
    cr.pop_group_to_source()
    cr.paint_with_alpha(1.0 - (0.5 * amount if rng.random() < 0.25 else 0.0))


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    shop(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("r1", "exist."), (1.15, 360, 600))], dur=0.6))
    pole(cr, t, 650, 860, 360)
    chair(cr, 260, 900, 0.9)
    glitchy(cr, t, lambda c: person(c, t, 430, 900, 0.95, "barber", eyes="wide", mouth="o", brows="up",
                                     arms=("hold", "down"), hold=scissors), amount=0.6 + 0.4 * math.sin(t * 5) ** 2)
    cr.restore()
    stamp(cr, t, A("r1", "cannot"), 360, 170, "CAN'T EXIST", col=RED, size=90, end=A("r1", "Here's") - 0.05)
    sign(cr, t, A("r1", "Here's"), 360, 170, "HERE'S WHY", col=GOLD, size=72)
    vignette(cr, 0.4)


def scene_rule(cr, t, tl):
    A = tl.at
    shop(cr, t)
    r3 = A("r3")
    cr.save()
    enter(cr, camera(t, [(A("r2") - 0.3, (1.0, 360, 640)), (r3, (1.0, 360, 640))]))
    pole(cr, t, 660, 860, 320)
    if t >= A("r3", "only"):         # a villager who shaves himself gets turned away
        u = ease_out(seg(t, A("r3", "only"), A("r3", "only") + 0.8))
        person(cr, t, lerp(560, 860, u), 920, 0.62, "villager", beard=None, skin="light", shirt=hexc("#4aa3f0"),
               eyes="sad", mouth="sad", arms=("hold", "down"), hold=razor, facing=1, walk=t * 8, seed=4)
        red_x(cr, t, A("r3", "only") + 0.1, lerp(560, 860, u), 560, 36)
    elif t >= A("r3", "everyone"):   # a queue of bearded villagers walks in
        for k in range(3):
            st = A("r3", "everyone") + 0.15 * k
            u = ease_out(seg(t, st, st + 0.8))
            person(cr, t, lerp(860 + k * 120, 420 + k * 120, u), 920, 0.6, "villager", eyes="happy",
                   mouth="smile", arms=("down", "down"), facing=-1, walk=t * 8 if u < 1 else None, seed=k,
                   skin=("tan", "light", "brown")[k])
    person(cr, t, 200, 920, 0.95, "barber", eyes="happy" if t < r3 else "half", mouth=mouth(tl, "barber", t, "grin"),
           arms=("hold", "point") if t >= r3 else ("hold", "hips"), hold=scissors)
    cr.restore()
    sign(cr, t, A("r2"), 360, 140, "ONE VILLAGE", col=BLUE, size=60, end=A("r2", "rule.") - 0.05)
    card(cr, t, A("r2", "rule."), 360, 240, 560, 230, "THE BARBER'S RULE",
         ["I shave everyone who", "doesn't shave themselves.", "And ONLY them!"], col=RED, title_size=40,
         line_size=38)
    vignette(cr, 0.4)


def scene_mirror(cr, t, tl):
    A = tl.at
    shop(cr, t)
    q = A("r4", "barber?")
    cr.save()
    enter(cr, camera(t, [(A("r4") - 0.3, (1.0, 360, 640)), (A("r4", "So"), (1.35, 360, 520))], dur=0.7))
    cr.save()      # his reflection in the mirror
    cr.rectangle(130, 180, 460, 360)
    cr.clip()
    person(cr, t, 360, 900, 0.95, "barber", beard=hexc("#3a2a20"), eyes="wide", mouth="o", brows="up",
           arms=("chin", "down"), facing=-1, shadow=False)
    cr.rectangle(130, 180, 460, 360)
    cr.set_source_rgba(0.85, 0.95, 1.0, 0.25)
    cr.fill()
    cr.restore()
    person(cr, t, 360, 1080, 1.1, "barber", beard=hexc("#3a2a20"), eyes="wide", mouth="o", brows="up",
           arms=("chin", "down"), shadow=False)
    cr.restore()
    if t >= q:
        bold_text(cr, "?", 600, 330 + math.sin(t * 5) * 8, 160 * appear(t, q, 0.4), GOLD)
    sign(cr, t, A("r4", "Simple."), 360, 110, "SIMPLE...", col=GREEN, size=60, end=A("r4", "So") - 0.05)
    sign(cr, t, A("r4", "So"), 360, 110, "WHO SHAVES THE BARBER?", col=PURPLE, size=46)
    vignette(cr, 0.45)


def scene_logic(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#bfe6dc"), hexc("#fff1d6"), seed=4)
    r5, r6, r7 = A("r5"), A("r6"), A("r7")
    if t < r7:
        card(cr, t, r5, 182, 320, 332, 330, "HE SHAVES", ["himself? Then he's", "a self-shaver.", "Rule: NEVER", "shave those."],
             col=GREEN, mark="no", mark_at=A("r5", "can't."), title_size=38, line_size=37)
        card(cr, t, r6, 538, 320, 332, 330, "HE DOESN'T?", ["Then he's NOT", "a self-shaver.", "Rule: MUST", "shave those."],
             col=RED, mark="no", mark_at=A("r6", "has"), title_size=38, line_size=37)
        if t >= r6:
            bold_text(cr, "OR", 360, 560, 60 * appear(t, r6, 0.3), GOLD)
        bearded = t >= r6
        person(cr, t, 360, 930, 0.62, "barber", beard=hexc("#3a2a20") if bearded else None, eyes="wide",
               mouth="o", arms=("hold", "chin") if not bearded else ("chin", "down"), hold=None if bearded else razor,
               brows="up")
    else:
        knot(cr, t, r7, 360, 360, 150, RED)
        flip = int((t - r7) * 6) % 2 == 0
        glitchy(cr, t, lambda c: person(c, t, 360, 930, 0.62, "barber", beard=hexc("#3a2a20") if flip else None,
                                        eyes="x" if t > r7 + 1.0 else "wide", mouth="o", arms=("face", "face"),
                                        brows="up"), amount=0.5)
        sign(cr, t, A("r7", "breaks"), 360, 140, "RULE BROKEN", col=RED, size=64)
    vignette(cr, 0.35)


def signpost(cr, t, x, y, text, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -14, -260, 28, 260, 6)
    paint(cr, hexc("#8a5a2b"), OUTLINE, 4)
    soft_rrect(cr, -215, -390, 430, 150, 16, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -215, -400, 430, 150, 16)
    paint(cr, lin(0, -400, 0, -250, [(0, hexc("#fff3a8")), (1, GOLD)]), OUTLINE, 6)
    bold_text(cr, text, 0, -308, 40, INKC, outline=None, shadow=0)
    cr.restore()


def scene_sign(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#d8f0c8"), seed=8)
    rrect(cr, 0, 900, W, 400, 0)
    paint(cr, lin(0, 900, 0, H, [(0, hexc("#8fcf72")), (1, hexc("#4e9e3a"))]), None, 0)
    signpost(cr, t, 480, 900, "IGNORE THIS SIGN", 1.0)
    turned = t >= A("r8", "ignore", nth=2)
    obeyed = t >= A("r8", "followed")
    person(cr, t, 170, 910, 0.85, "kid", eyes="happy" if turned and not obeyed else ("wide" if obeyed else "open"),
           mouth="smug" if turned and not obeyed else ("o" if obeyed else "smile"),
           arms=("hips", "hips") if turned else ("chin", "down"), facing=-1 if turned and not obeyed else 1,
           look=(0.6, -0.3) if not turned else (0, 0), brows="up" if obeyed else None, sweat=obeyed)
    sign(cr, t, A("r8", "same"), 360, 130, "SAME TRAP", col=PURPLE, size=64, end=A("r8", "If") - 0.05)
    if obeyed:
        check(cr, t, A("r8", "followed"), 620, 470, 46)
    stamp(cr, t, A("r8", "followed"), 360, 160, "YOU FOLLOWED IT!", col=GREEN, size=64)
    vignette(cr, 0.35)


def scene_russell(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8d0e8"), hexc("#fff1d6"), seed=2)
    portrait(cr, t, A("r9", "Bertrand"), 360, 420, 190, "russell", eyes="half", mouth="smile", bg=hexc("#9fc8ff"))
    tag(cr, t, A("r9", "Russell"), 360, 180, "BERTRAND RUSSELL", col=hexc("#9fc8ff"))
    sign(cr, t, A("r9", "famous"), 360, 690, "FAMOUS THINKER", col=GOLD, size=52, rot=-0.03, end=A("r9", "1918.") - 0.05)
    sign(cr, t, A("r9", "1918."), 360, 690, "WROTE ABOUT IT IN 1918", col=PURPLE, size=44, rot=0.03)
    vignette(cr, 0.35)


def scene_vanish(cr, t, tl):
    A = tl.at
    shop(cr, t)
    gone = A("r10", "barber")
    u = seg(t, gone, gone + 1.0)
    cr.save()
    enter(cr, (1.0, 360, 640))
    chair(cr, 300, 920, 0.95, spin=t * 4 if u >= 1 else 0.0)
    if u < 1:
        cr.push_group()
        glitchy(cr, t, lambda c: person(c, t, 470, 920, 0.95, "barber", eyes="wide", mouth="o", brows="up",
                                         arms=("face", "face")), amount=0.4 + u)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - u)
    if gone <= t < gone + 1.6:
        particles(cr, t, 9, 30, (1, 1, 1, 0.8 * (1 - seg(t, gone, gone + 1.6))), area=(330, 400, 280, 500),
                  r=(2, 6), speed=80)
    cr.restore()
    sign(cr, t, A("r10", "accept?"), 360, 150, "THE ANSWER?", col=GOLD, size=64, end=gone - 0.05)
    stamp(cr, t, A("r10", "exist."), 360, 170, "HE CAN'T EXIST", col=RED, size=72)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    shop(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    pole(cr, t, 650, 860, 320)
    glitchy(cr, t, lambda c: person(c, t, 330, 920, 0.95, "barber", beard=hexc("#3a2a20") if (t * 2) % 2 > 1 else None,
                                     eyes="half", mouth="smug", arms=("hold", "hips"), hold=scissors), amount=0.35)
    cr.restore()
    sign(cr, t, A("r11"), 360, 150, "WHO SHAVES THE BARBER?", col=PURPLE, size=46)
    stamp(cr, t, A("r11", "Wrong"), 360, 300, "WRONG ANSWERS ONLY", col=RED, size=52, rot=-0.05)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "rule": scene_rule, "mirror": scene_mirror, "logic": scene_logic, "sign": scene_sign,
          "russell": scene_russell, "vanish": scene_vanish, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
