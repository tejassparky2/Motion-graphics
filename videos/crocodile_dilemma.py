"""The Crocodile Dilemma -- Pinocchio-style paradox in the polished look.

A crocodile that has stolen a child promises to return it if the parent correctly predicts what it will do; the
parent says "you will not return my child". Known in antiquity: the Roman teacher of rhetoric Quintilian mentions it
(Institutio Oratoria I.10.5, c. 95 AD). Wikipedia "Crocodile dilemma".
Script approved by the owner on 9 Oct 2026 (out/scripts_paradox_batch2.md) with an everyday example, a clever
closing question and character voices added at the owner's request.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, calendar, card, knot, shake,
                         sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, light_rays,
                           lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc, sprite, stamp, stroke_line,
                           vignette)
from motion.toons import baby_basket, crocodile, person

NARRATOR = dict(speed=0.9)
TAIL = 0.9
voice.SPEAKERS.update({"croc": dict(voice="am_onyx", speed=0.92, pitch=-2.0),
                       "mom": dict(voice="af_heart", speed=1.05)})

SCRIPT = [
    dict(id="k1", scene="hook", text="A crocodile steals a child. Then it offers the mother a deal."),
    dict(id="k2", scene="offer", text="Guess what I'm going to do. Guess right, and you get your child back.",
         speaker="croc", gap=0.3, pace=0.95),
    dict(id="k3", scene="answer", text="The mother thinks. Then she says. You will not give my child back!",
         speaker="mom", speaker_from="You", gap=0.35),
    dict(id="k4", scene="stuck", text="Now the crocodile is stuck.", gap=0.45, pace=0.92),
    dict(id="k5", scene="logic", text="If it gives the child back, her guess was wrong. So it shouldn't give it "
                                      "back."),
    dict(id="k6", scene="logic", text="If it keeps the child, her guess was right. So it has to give it back."),
    dict(id="k7", scene="logic", text="Whatever it does, it breaks its own promise.", pace=0.95),
    dict(id="k8", scene="example", text="Try it at home. Mom says: guess what I'll decide. Guess right, and you can "
                                        "go out. You say: you won't let me go."),
    dict(id="k9", scene="rome", text="Teachers in ancient Rome already knew this puzzle, almost two thousand years "
                                     "ago."),
    dict(id="k10", scene="end", text="So what should the crocodile do? Or better... what would you have said to save "
                                     "the child?", gap=0.3, pace=0.95),
]

METADATA = dict(
    title="A Crocodile Made a Deal. One Answer Breaks It. 🐊",
    alt_titles=["The Crocodile's Impossible Promise 🐊 (2,000-Year-Old Paradox)",
                "She Said ONE Sentence and the Crocodile Was Trapped 🤯🐊"],
    description="""A crocodile steals a child, then offers the mother a deal: "Guess what I'm going to do. Guess right, and you get your child back." 🐊

The mother thinks, then says: "You will NOT give my child back!"

Now the crocodile is stuck. If it gives the child back, her guess was wrong, so it shouldn't. If it keeps the child, her guess was right, so it has to give it back. Whatever it does, it breaks its own promise.

Try it at home: Mom says "guess what I'll decide, guess right and you can go out." You say: "you won't let me go." 😏

Teachers in ancient Rome already knew this puzzle almost 2,000 years ago (Quintilian, Institutio Oratoria, c. 95 AD). It's called the Crocodile Dilemma.

💬 What should the crocodile do? Or better... what would YOU have said to save the child? 👇

🔔 Interestingly Strange: mind-bending paradoxes, weird animals, bizarre history and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#Logic", "#Shorts"],
    tags=["crocodile dilemma", "crocodile paradox", "logic paradox", "paradox", "brain teaser", "riddle",
          "mind blowing", "ancient rome", "self reference paradox", "interestingly strange"],
    pinned_comment="What would YOU have said to the crocodile? 🐊 Best answer gets pinned 👇",
)

WATER = hexc("#3fa8d8")


# ---------------------------------------------------------------- backgrounds
def _river(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 640, [(0, hexc("#ffb27a")), (0.6, hexc("#ffe2b8")), (1, hexc("#fff1d6"))]))
    c.fill()
    c.arc(520, 300, 70, 0, 2 * math.pi)
    c.set_source(rad(520, 300, 70, [(0, (1, 1, 0.92, 1)), (1, (1, 0.85, 0.5, 1))]))
    c.fill()
    for k, x in enumerate((60, 180, 610)):    # palms on the far bank
        stroke_line(c, [(x, 600), (x + 10, 470), (x + 24, 360)], 14, hexc("#7a5a3a"))
        for j in range(6):
            a = -math.pi / 2 + (j - 2.5) * 0.55
            smooth(c, [(x + 24, 360), (x + 24 + math.cos(a) * 90, 360 + math.sin(a) * 50 + 30),
                       (x + 24 + math.cos(a) * 60, 360 + math.sin(a) * 30 + 10)], closed=True)
            c.set_source_rgba(*hexc("#3f8a3a"))
            c.fill()
    c.rectangle(0, 590, W, 40)
    c.set_source_rgba(*hexc("#c9b27a"))
    c.fill()
    c.rectangle(0, 620, W, 200)
    c.set_source(lin(0, 620, 0, 820, [(0, hexc("#5fc0e8")), (1, hexc("#2f88b8"))]))
    c.fill()
    c.move_to(0, 800)
    for x in range(0, W + 41, 40):
        c.line_to(x, 790 + 12 * math.sin(x / 60.0))
    c.line_to(W, H)
    c.line_to(0, H)
    c.close_path()
    c.set_source(lin(0, 790, 0, H, [(0, hexc("#e8cf8a")), (1, hexc("#b8945a"))]))
    c.fill()


def river(cr, t):
    put(cr, sprite("river_bg", W, H, _river), 0, 0)
    for k in range(6):    # glints on the water
        x = (k * 137 + t * 30) % W
        y = 650 + (k * 53) % 150
        stroke_line(cr, [(x, y), (x + 40, y)], 4, alpha(WHITE, 0.5), curve=False)
    for k, x in enumerate((40, 90, 660, 700)):   # reeds in front
        sway = math.sin(t * 1.6 + k) * 8
        stroke_line(cr, [(x, 1000), (x + sway * 0.5, 880), (x + sway, 780)], 10, OUTLINE)
        stroke_line(cr, [(x, 1000), (x + sway * 0.5, 880), (x + sway, 780)], 5, hexc("#5aa043"))
        ellipse(cr, x + sway, 770, 9, 26)
        paint(cr, hexc("#8a5a2b"), OUTLINE, 3)


def home(cr, t):
    studio(cr, t, hexc("#ffd6c0"), hexc("#fff1d6"), seed=7, n=8)
    rrect(cr, 470, 260, 200, 620, 10)    # a door
    paint(cr, lin(470, 0, 670, 0, [(0, hexc("#8a4a2a")), (1, hexc("#5a2a1a"))]), OUTLINE, 6)
    cr.arc(640, 580, 12, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 3)
    rrect(cr, 0, 880, W, 400, 0)
    paint(cr, lin(0, 880, 0, H, [(0, hexc("#c99a6a")), (1, hexc("#8a5a3a"))]), None, 0)


def talk_jaw(tl, t, who="croc"):
    return 0.12 + 0.4 * abs(math.sin(t * 13)) if tl.speaking(who, t) else 0.12


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


def basket_prop(t, s=0.42):
    return lambda c, hx, hy: baby_basket(c, t, hx + 10, hy + 40, s, eyes="wide", mouth="o")


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    river(cr, t)
    grab = A("k1", "steals")
    mom_in = A("k1", "mother")
    cam = camera(t, [(0, (1.0, 360, 640)), (mom_in, (1.0, 360, 640))])
    cr.save()
    enter(cr, cam)
    if t < grab:
        baby_basket(cr, t, 470, 900, 0.7, eyes="happy", mouth="grin")
        crocodile(cr, t, lerp(820, 600, seg(t, 0, grab)), 930, 0.75, facing=-1, eyes="half", jaw=0.3,
                  arms=("hold", "down"))
    else:
        crocodile(cr, t, 470, 930, 0.75, facing=-1, eyes="half", jaw=0.12, arms=("hold", "hips"),
                  hold=basket_prop(t))
    if t >= mom_in:
        mx = lerp(-120, 150, ease_out(seg(t, mom_in, mom_in + 0.5)))
        person(cr, t, mx, 930, 0.85, "mother", eyes="wide", mouth="open", brows="up", arms=("face", "out"),
               sweat=True)
    cr.restore()
    stamp(cr, t, grab, 360, 200, "STOLEN!", col=RED, size=90, end=A("k1", "deal.") - 0.05)
    sign(cr, t, A("k1", "deal."), 360, 190, "A DEAL?!", col=GREEN, size=80, rot=0.03)
    vignette(cr, 0.4)


def scene_offer(cr, t, tl):
    A = tl.at
    river(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("k2") - 0.3, (1.3, 400, 600))]))
    crocodile(cr, t, 440, 930, 0.9, facing=-1, eyes="half", jaw=talk_jaw(tl, t), arms=("hold", "point"),
              hold=basket_prop(t, 0.36), brows="angry")
    cr.restore()
    bubble(cr, t, A("k2", "Guess"), 360, 190, "GUESS WHAT I'LL DO", size=44, tail=1, end=A("k2", "right,") - 0.05)
    bubble(cr, t, A("k2", "right,"), 360, 190, "GUESS RIGHT = CHILD BACK", size=40, tail=1, col=hexc("#fff3c4"))
    vignette(cr, 0.45)


def scene_answer(cr, t, tl):
    A = tl.at
    river(cr, t)
    says = A("k3", "You")
    cam = camera(t, [(A("k3") - 0.3, (1.3, 260, 600)), (says, (1.4, 250, 590))], dur=0.4)
    cr.save()
    enter(cr, cam)
    thinking = t < says
    person(cr, t, 230, 930, 0.95, "mother", eyes="half" if thinking else "angry",
           mouth=mouth(tl, "mom", t, "flat" if thinking else "grin"), brows="flat" if thinking else "angry",
           arms=("chin", "down") if thinking else ("point", "hips"), look=(0.6, 0))
    cr.restore()
    if thinking:
        for k in range(3):    # thinking dots
            if t >= A("k3", "thinks.") + 0.15 * k:
                cr.arc(420 + k * 40, 380 - k * 30, 12 + k * 4, 0, 2 * math.pi)
                paint(cr, WHITE, OUTLINE, 4)
    bubble(cr, t, says, 400, 200, "YOU WON'T GIVE", size=50, tail=-1, col=hexc("#ffd6e4"))
    bubble(cr, t, A("k3", "child"), 400, 300, "MY CHILD BACK!", size=50, tail=0, col=hexc("#ffd6e4"))
    vignette(cr, 0.45)


def scene_stuck(cr, t, tl):
    A = tl.at
    river(cr, t)
    st = A("k4", "stuck.")
    dx, dy = shake(t, st, 0.4, 12)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("k4") - 0.3, (1.15, 400, 620)), (st, (1.35, 420, 560))], dur=0.25))
    crocodile(cr, t, 440, 930, 0.9, facing=-1, eyes="wide", jaw=0.55 if t >= st else 0.12,
              arms=("face", "face") if t >= st else ("hold", "down"), hold=None if t >= st else basket_prop(t, 0.36),
              brows="up", bob=False)
    cr.restore()
    if t >= st:
        cue("hit", t, st)
        baby_basket(cr, t, 600, 860, 0.5, eyes="happy", mouth="grin")
    stamp(cr, t, st, 360, 200, "STUCK!", col=RED, size=110)
    vignette(cr, 0.45)


def scene_logic(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fe0c8"), hexc("#fff1d6"), seed=3)
    k5, k6, k7 = A("k5"), A("k6"), A("k7")
    if t < k7:
        card(cr, t, k5, 185, 330, 320, 300, "GIVE IT BACK?", ["Then her guess", "was WRONG.", "So: DON'T!"],
             col=GREEN, mark="no", mark_at=A("k5", "So"))
        card(cr, t, k6, 535, 330, 320, 300, "KEEP IT?", ["Then her guess", "was RIGHT.", "So: GIVE IT!"],
             col=RED, mark="no", mark_at=A("k6", "So"))
        if t >= k6:
            bold_text(cr, "OR", 360, 560, 60 * appear(t, k6, 0.3), GOLD)
        crocodile(cr, t, 360, 900, 0.62, facing=1, eyes="wide", jaw=0.12, arms=("chin", "down"), brows="sad")
    else:
        knot(cr, t, k7, 360, 360, 150, RED)
        spin = (t - k7) * 6
        cr.save()
        cr.translate(360, 900)
        cr.rotate(0.15 * math.sin(spin * 2))
        crocodile(cr, t, 0, 0, 0.62, facing=1 if math.sin(spin) > 0 else -1, eyes="x" if t > k7 + 0.8 else "wide",
                  jaw=0.4, arms=("face", "face"), brows="up")
        cr.restore()
        sign(cr, t, A("k7", "breaks"), 360, 140, "PROMISE BROKEN", col=RED, size=60)
    vignette(cr, 0.35)


def scene_example(cr, t, tl):
    A = tl.at
    home(cr, t)
    you = A("k8", "You", nth=2)    # "You say: ..."
    person(cr, t, 560, 900, 0.9, "mother", shirt=hexc("#e8743a"), eyes="half" if t < you else "wide",
           mouth="talk" if A("k8", "Mom") <= t < you else ("o" if t >= you else "smug"), arms=("hips", "point"),
           facing=-1, sweat=t >= you + 0.6)
    person(cr, t, 190, 900, 0.85, "kid", eyes="happy" if t >= you else "open", mouth="grin" if t >= you else "smile",
           arms=("hips", "point") if t >= you else ("down", "down"))
    sign(cr, t, A("k8"), 360, 140, "TRY IT AT HOME", col=BLUE, size=60, end=A("k8", "Mom") - 0.05)
    bubble(cr, t, A("k8", "guess"), 400, 170, "GUESS RIGHT = YOU GO OUT", size=40, tail=1, end=you - 0.05)
    bubble(cr, t, you, 320, 190, "YOU WON'T LET ME GO!", size=46, tail=-1, col=hexc("#fff3c4"))
    vignette(cr, 0.35)


def chalkboard(cr, t, start):
    rrect(cr, 300, 200, 380, 300, 12)
    paint(cr, lin(0, 200, 0, 500, [(0, hexc("#c99460")), (1, hexc("#8a5a2e"))]), OUTLINE, 6)
    rrect(cr, 318, 218, 344, 264, 6)
    paint(cr, rad(490, 350, 260, [(0, hexc("#3e7a5a")), (1, hexc("#22503a"))]), OUTLINE, 3)
    if t >= start:     # a chalk crocodile doodle
        k = min(1.0, (t - start) / 0.8)
        cr.save()
        cr.rectangle(318, 218, 344 * k, 264)
        cr.clip()
        stroke_line(cr, [(360, 380), (420, 340), (520, 350), (620, 330), (600, 370), (520, 380), (420, 400),
                         (360, 380)], 5, (1, 1, 1, 0.9))
        for j in range(5):
            stroke_line(cr, [(520 + j * 20, 352), (528 + j * 20, 364)], 3, (1, 1, 1, 0.9), curve=False)
        cr.arc(450, 336, 10, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.set_line_width(4)
        cr.stroke()
        stroke_line(cr, [(370, 450), (470, 450)], 4, (1, 1, 1, 0.8), curve=False)
        stroke_line(cr, [(370, 430), (440, 430)], 4, (1, 1, 1, 0.8), curve=False)
        cr.restore()


def scene_rome(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e2c8"), hexc("#fff1d6"), seed=5, n=8)
    for k in range(3):       # Roman columns
        x = 20 + k * 300
        rrect(cr, x, 120, 70, 780, 6)
        paint(cr, lin(x, 0, x + 70, 0, [(0, hexc("#e8e0d0")), (0.4, WHITE), (1, hexc("#cfc4b0"))]),
              alpha(OUTLINE, 0.4), 3)
    chalkboard(cr, t, A("k9", "puzzle,"))
    person(cr, t, 190, 920, 0.9, "judge", toga=hexc("#c9a42e"), eyes="happy", mouth="talk" if t < A("k9", "ago.")
           else "grin", arms=("point", "hips"), seed=2)
    calendar(cr, t, A("k9", "two"), 500, 690, "AROUND", "95 AD", col=hexc("#c9a42e"))
    sign(cr, t, A("k9", "Rome"), 360, 110, "ANCIENT ROME", col=RED, size=58)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    river(cr, t)
    better = A("k10", "better...")
    cr.save()
    enter(cr, (1.0, 360, 640))
    crocodile(cr, t, 520, 930, 0.72, facing=-1, eyes="half", jaw=0.12, arms=("hold", "chin"), hold=basket_prop(t))
    person(cr, t, 150, 930, 0.8, "mother", eyes="half", mouth="smug", arms=("hips", "hips"), look=(0.6, 0))
    cr.restore()
    sign(cr, t, A("k10"), 360, 140, "WHAT SHOULD IT DO?", col=GREEN, size=54, end=better - 0.05)
    if t < better:
        buttons(cr, t, A("k10", "do?"), [("GIVE BACK", GREEN), ("KEEP", RED)], y=290)
    sign(cr, t, better, 360, 170, "WHAT WOULD YOU SAY", col=PURPLE, size=50, sub="TO SAVE THE CHILD?", sub_col=WHITE)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "offer": scene_offer, "answer": scene_answer, "stuck": scene_stuck,
          "logic": scene_logic, "example": scene_example, "rome": scene_rome, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
