"""Funny history (Halloween): "They Put a Dead Pope on Trial in 897" -- the Cadaver Synod, in the owner's reference
narration style (talks to the viewer, "bro", big set-up / flat landing).

Script: out/scripts_batch_oct26-31.md, row 66 (owner approved 18 Oct 2026). Cadaver Synod, Rome, January 897: Pope
Stephen VI had the corpse of Pope Formosus (died April 896) exhumed, dressed in papal robes and seated on a throne; a
deacon answered for him. Found guilty, his acts were annulled, the three fingers of his right hand used for blessings
were cut off, and the body was thrown into the Tiber. Later in 897 Stephen was deposed, imprisoned and strangled
("never comes out", to keep it ad-friendly). Turbo voice with tags (narrator only, stock female voice).
The corpse is drawn as a cartoon skeleton in robes: spooky, not gory.
"""
import math
import random

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, ellipse, enter, lin,
                           paint, rad, rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.9
BONE = hexc("#f2ecd8")
ROBE = hexc("#e8e0c8")

SCRIPT = [
    dict(id="d1", scene="court", text="[Eight ninety-seven.|897.] Rome. The court is packed. And the man on trial has "
                                      "been dead for nine months."),
    dict(id="d2", scene="dig", text="This is Pope Formosus. Bro was already buried. And the new pope, Stephen, said: "
                                    "dig him up."),
    dict(id="d3", scene="throne", text="They dress the corpse in full robes. And sit him on a throne. In court. "
                                       "[gasp]"),
    dict(id="d4", scene="deacon", text="Now you're thinking, how does a dead man answer questions? Easy. They make a "
                                       "deacon stand next to him, and answer for him."),
    dict(id="d5", scene="deacon", text="Imagine being that guy. Your job today: talk for a corpse. [laugh]"),
    dict(id="d6", scene="verdict", text="The verdict? Guilty. Obviously. He didn't say one word in his defence. "
                                        "[chuckle]"),
    dict(id="d7", scene="river", text="They cut off the three fingers he blessed people with. And throw him in the "
                                      "river."),
    dict(id="d8", scene="twist", text="But plot twist. A few months later, Rome turns on Stephen. He's thrown in "
                                      "prison. And never comes out."),
    dict(id="d9", scene="name", text="History calls it the Cadaver Synod. The creepiest court case ever."),
    dict(id="d10", scene="end", text="But here's the real question. We judge dead people all the time, in history "
                                     "books. Is that fair, or not?", gap=0.5),
]

METADATA = dict(
    title="They Put a Dead Pope on Trial in 897 💀",
    alt_titles=["The Creepiest Court Case in History 💀 (Cadaver Synod)", "A Pope Dug Up His Rival. Then Sued Him 💀"],
    description="""Rome, 897. The court is packed... and the man on trial has been dead for nine months. 💀

Pope Stephen VI had his predecessor, Pope Formosus, dug up, dressed in full robes and sat on a throne in court. A deacon stood next to the corpse and answered for him. The verdict? Guilty, obviously: he didn't say one word in his defence. They cut off the three fingers he blessed people with and threw him in the river.

Plot twist: a few months later Rome turned on Stephen, and he was thrown in prison and never came out. History calls it the Cadaver Synod. 🎃

💬 We judge dead people all the time, in history books. Is that fair, or not? 👇

🔔 Interestingly Strange: funny history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FunnyHistory", "#Halloween", "#Shorts"],
    tags=["cadaver synod", "dead pope on trial", "pope formosus", "pope stephen vi", "weird history", "creepy history",
          "halloween history", "funny history", "history facts", "interestingly strange"],
    pinned_comment="Is it fair to judge people who can't answer back (like in history books)? Fair 👍 or not 👎? 👇",
)


# ---------------------------------------------------------------- props
def skeleton_pope(cr, t, x, y, s=1.0, slump=0.0, sway=True, fingers=True, eyes_glow=0.0):
    """A cartoon skeleton in papal robes and a mitre, seated (hips at (x, y)). Spooky-cute, not gory."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate((0.05 * math.sin(t * 1.3) if sway else 0) + 0.25 * slump)
    cr.move_to(-120, 0)                                              # robe
    cr.curve_to(-130, -120, -90, -260, -60, -300)
    cr.line_to(60, -300)
    cr.curve_to(90, -260, 130, -120, 120, 0)
    cr.close_path()
    paint(cr, lin(0, -300, 0, 0, [(0, ROBE), (1, shade(ROBE, -0.2))]), OUTLINE, 6)
    stroke_line(cr, [(0, -290), (0, -10)], 14, GOLD, curve=False)    # gold stole
    stroke_line(cr, [(-20, -150), (20, -150)], 10, RED, curve=False)
    stroke_line(cr, [(0, -170), (0, -130)], 10, RED, curve=False)
    for side in (-1, 1):                                             # bony arms resting
        stroke_line(cr, [(side * 70, -260), (side * 100, -150), (side * 70, -70)], 12, OUTLINE)
        stroke_line(cr, [(side * 70, -260), (side * 100, -150), (side * 70, -70)], 7, BONE)
        if fingers or side < 0:
            for k in range(3):
                stroke_line(cr, [(side * 70, -70), (side * (66 + k * 8), -48)], 4, OUTLINE, curve=False)
    cr.translate(0, -360)                                            # skull
    cr.rotate(0.15 * slump)
    ellipse(cr, 0, 0, 62, 66)
    paint(cr, rad(-14, -20, 80, [(0, WHITE), (1, BONE)]), OUTLINE, 6)
    for ex in (-24, 24):
        ellipse(cr, ex, -4, 16, 19)
        paint(cr, hexc("#2b2622"), None)
        if eyes_glow:
            soft_disc(cr, ex, -4, 14, (1, 0.4, 0.2, eyes_glow))
    cr.move_to(0, 18)
    cr.line_to(-8, 32)
    cr.line_to(8, 32)
    cr.close_path()
    paint(cr, hexc("#2b2622"), None)
    rrect(cr, -28, 42, 56, 16, 4)
    paint(cr, WHITE, OUTLINE, 3)
    for k in range(4):
        stroke_line(cr, [(-21 + k * 14, 42), (-21 + k * 14, 58)], 2, OUTLINE, curve=False)
    cr.move_to(-46, -44)                                             # mitre
    cr.line_to(0, -150)
    cr.line_to(46, -44)
    cr.close_path()
    paint(cr, lin(0, -150, 0, -44, [(0, WHITE), (1, ROBE)]), OUTLINE, 5)
    stroke_line(cr, [(0, -140), (0, -50)], 8, GOLD, curve=False)
    cr.restore()


def throne(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -150, -480, 300, 480, 30)
    paint(cr, lin(0, -480, 0, 0, [(0, hexc("#c8961e")), (1, hexc("#7a5410"))]), OUTLINE, 7)
    rrect(cr, -120, -440, 240, 330, 20)
    paint(cr, hexc("#8a1a2a"), OUTLINE, 5)
    rrect(cr, -170, -140, 340, 60, 14)
    paint(cr, hexc("#a8781a"), OUTLINE, 6)
    cr.restore()


def candles(cr, t, xs, y):
    for k, x in enumerate(xs):
        rrect(cr, x - 12, y - 80, 24, 80, 4)
        paint(cr, hexc("#f4efe0"), OUTLINE, 3)
        fl = 1 + 0.15 * math.sin(t * 13 + k * 2)
        soft_disc(cr, x, y - 100, 60 * fl, (1, 0.7, 0.3, 0.35))
        ellipse(cr, x, y - 98, 8 * fl, 16 * fl)
        paint(cr, hexc("#ffcf3f"), None)


def _hall(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#140c18")), (0.62, hexc("#2a1a2a")), (0.62, hexc("#3a2a24")),
                                   (1, hexc("#1a1210"))]))
    cr.fill()
    for k in range(4):                                               # gothic arches
        x = 40 + k * 190
        cr.move_to(x, 790)
        cr.line_to(x, 300)
        cr.curve_to(x, 200, x + 130, 200, x + 130, 300)
        cr.line_to(x + 130, 790)
        paint(cr, hexc("#1f1424"), alpha(OUTLINE, 0.7), 4)


def deacon(cr, t, x, y, s, **kw):
    person(cr, t, x, y, s, "aquinas", **kw)


def stephen(cr, t, x, y, s, **kw):
    person(cr, t, x, y, s, "judge", shirt=hexc("#f4efe6"), toga=hexc("#8a1a2a"), **kw)


# ---------------------------------------------------------------- scenes
def scene_court(cr, t, tl):
    A = tl.at
    _hall(cr, t)
    candles(cr, t, (60, 660), 820)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("d1", "dead"), (1.3, 360, 560))], dur=0.8))
    throne(cr, 360, 860, 0.9)
    skeleton_pope(cr, t, 360, 760, 0.85, eyes_glow=0.5 if t >= A("d1", "dead") else 0.0)
    for k in range(5):                                               # the packed court, from behind
        person(cr, t, 60 + k * 150, 1120, 0.5, ("reporter", "villager", "seller", "dad", "barber")[k], eyes="wide",
               mouth="o", look=(0, -0.7), seed=k)
    cr.restore()
    if t >= A("d1", "months."):
        sign(cr, t, A("d1", "months."), 360, 760, "DEAD FOR 9 MONTHS", col=RED, size=52)
        cue("sting", t, A("d1", "dead"))
    vignette(cr, 0.6)


def scene_dig(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)                                         # a graveyard at night
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#0c1028")), (0.7, hexc("#1f2450")), (0.7, hexc("#2a3a24")),
                                   (1, hexc("#141e12"))]))
    cr.fill()
    cr.arc(560, 220, 70, 0, 2 * math.pi)
    paint(cr, hexc("#f4efd8"), OUTLINE, 4)
    rrect(cr, 120, 620, 180, 280, 70)                                # gravestone
    paint(cr, lin(0, 620, 0, 900, [(0, hexc("#a8a8b8")), (1, hexc("#6a6a7a"))]), OUTLINE, 6)
    bold_text(cr, "R.I.P.", 210, 720, 40, hexc("#3a3a48"), outline=None, shadow=0)
    bold_text(cr, "FORMOSUS", 210, 780, 28, hexc("#3a3a48"), outline=None, shadow=0)
    stephen(cr, t, 520, 1040, 0.8, eyes="angry", brows="angry", mouth="talk" if t >= A("d2", "dig") else "smug",
            arms=("point", "hips") if t >= A("d2", "dig") else ("hips", "hips"))
    if t >= A("d2", "dig"):                                          # dirt flying
        rng = random.Random(3)
        for k in range(10):
            ph = (t * 1.4 + k / 10) % 1
            x = 210 + (rng.random() - 0.5) * 200 * ph
            cr.arc(x, 900 - 300 * ph + 400 * ph * ph, 10, 0, 2 * math.pi)
            paint(cr, hexc("#5a3a20"), OUTLINE, 2)
        sign(cr, t, A("d2", "dig"), 360, 170, "DIG HIM UP", col=RED, size=70)
    else:
        sign(cr, t, A("d2", "buried."), 360, 170, "ALREADY BURIED", col=PURPLE, size=56)
    vignette(cr, 0.55)


def scene_throne(cr, t, tl):
    A = tl.at
    _hall(cr, t)
    candles(cr, t, (90, 630), 860)
    cr.save()
    enter(cr, camera(t, [(A("d3") - 0.3, (1.0, 360, 640)), (A("d3", "court."), (1.4, 360, 470))], dur=0.6))
    throne(cr, 360, 900, 1.0)
    dressed = t >= A("d3", "robes.")
    if dressed:
        skeleton_pope(cr, t, 360, 790, 0.95)
    else:
        rrect(cr, 240, 700, 240, 110, 30)                             # a wrapped bundle waiting
        paint(cr, hexc("#8a7a6a"), OUTLINE, 5)
    cr.restore()
    sign(cr, t, A("d3", "robes."), 360, 170, "FULL ROBES", col=GOLD, size=64, end=A("d3", "court.") - 0.05)
    if t >= A("d3", "court."):
        stamp(cr, t, A("d3", "court."), 360, 230, "IN COURT", col=RED, size=76)
        cue("hit", t, A("d3", "court."))
    vignette(cr, 0.6)


def scene_deacon(cr, t, tl):
    A = tl.at
    _hall(cr, t)
    candles(cr, t, (60, 660), 860)
    cr.save()
    enter(cr, camera(t, [(A("d4") - 0.3, (1.0, 360, 640)), (A("d5"), (1.25, 440, 560))], dur=0.6))
    throne(cr, 280, 900, 0.85)
    skeleton_pope(cr, t, 280, 800, 0.8)
    awkward = t >= A("d5")
    deacon(cr, t, 540, 960, 0.85, eyes="half" if awkward else "open", mouth="flat" if awkward else "talk",
           brows="sad" if awkward else None, sweat=awkward, arms=("front", "front") if awkward else ("out", "down"))
    if t >= A("d4", "answer", nth=2):                                # speech bubble from the deacon
        rrect(cr, 430, 380, 240, 110, 30)
        paint(cr, WHITE, OUTLINE, 5)
        bold_text(cr, "NOT GUILTY?", 550, 450, 34, OUTLINE, outline=None, shadow=0)
    cr.restore()
    if t < A("d5"):
        sign(cr, t, A("d4", "Easy."), 360, 170, "EASY.", col=GREEN, size=70)
    else:
        sign(cr, t, A("d5", "job"), 360, 170, "JOB: TALK FOR A CORPSE", col=PURPLE, size=46)
    vignette(cr, 0.6)


def scene_verdict(cr, t, tl):
    A = tl.at
    _hall(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("d6") - 0.3, (1.15, 360, 600))]))
    throne(cr, 360, 900, 0.85)
    skeleton_pope(cr, t, 360, 800, 0.8, slump=0.4 if t >= A("d6", "Guilty.") else 0.0)
    cr.restore()
    if t >= A("d6", "Guilty."):
        stamp(cr, t, A("d6", "Guilty."), 360, 330, "GUILTY", col=RED, size=96)
        cue("hit", t, A("d6", "Guilty."))
    if t >= A("d6", "word"):
        sign(cr, t, A("d6", "word"), 360, 520, "0 WORDS IN HIS DEFENCE", col=GOLD, size=40)
    vignette(cr, 0.6)


def scene_river(cr, t, tl):
    A = tl.at
    if t < A("d7", "throw"):
        studio(cr, t, hexc("#1a1018"), hexc("#3a2030"), seed=3)
        cr.save()                                                    # the blessing hand: three fingers, then gone
        cr.translate(360, 640)
        rrect(cr, -70, -40, 140, 120, 30)
        paint(cr, BONE, OUTLINE, 6)
        gone = t >= A("d7", "cut") + 0.3
        for k in range(3):
            if not gone:
                rrect(cr, -54 + k * 40, -170, 28, 140, 12)
                paint(cr, BONE, OUTLINE, 5)
        for k in range(2):
            rrect(cr, 66, 0 + k * 40, 70, 24, 10)
            paint(cr, BONE, OUTLINE, 4)
        cr.restore()
        sign(cr, t, A("d7", "three"), 360, 170, "3 BLESSING FINGERS", col=PURPLE, size=50)
        if gone:
            bold_text(cr, "SNIP", 360, 420, 70, RED)
            cue("hit", t, A("d7", "cut") + 0.3)
    else:
        cr.rectangle(0, 0, W, H)                                     # the river Tiber at night
        cr.set_source(lin(0, 0, 0, H, [(0, hexc("#0c1028")), (0.55, hexc("#1f2450")), (0.55, hexc("#1a3a5a")),
                                       (1, hexc("#0c1a2a"))]))
        cr.fill()
        for k in range(6):
            y = 760 + k * 60
            stroke_line(cr, [(x, y + 8 * math.sin(x / 40 + t * 3 + k)) for x in range(0, W + 40, 40)], 4,
                        (1, 1, 1, 0.15), curve=True)
        u = seg(t, A("d7", "throw"), A("d7", "river.", end=True))
        x, y = lerp(120, 460, u), 500 - 300 * math.sin(math.pi * u) + 250 * u
        cr.save()
        cr.translate(x, y)
        cr.rotate(u * 6)
        rrect(cr, -80, -30, 160, 60, 24)
        paint(cr, ROBE, OUTLINE, 5)
        cr.restore()
        if u >= 1:
            for k in range(3):
                ph = (t * 1.2 + k / 3) % 1
                ellipse(cr, 460, 760, 40 + 120 * ph, 12 + 30 * ph)
                paint(cr, None, (1, 1, 1, 0.6 * (1 - ph)), 4)
        sign(cr, t, A("d7", "river."), 360, 170, "INTO THE RIVER", col=BLUE, size=60)
    vignette(cr, 0.55)


def scene_twist(cr, t, tl):
    A = tl.at
    if t < A("d8", "prison."):
        _hall(cr, t)
        stephen(cr, t, 360, 1000, 1.0, eyes="wide" if t >= A("d8", "turns") else "happy",
                mouth="o" if t >= A("d8", "turns") else "smug", arms=("shrug", "shrug") if t >= A("d8", "turns")
                else ("hips", "hips"))
        if t >= A("d8", "turns"):
            for k in range(6):                                       # angry torches closing in
                x = 60 + k * 120
                stroke_line(cr, [(x, 1100), (x, 880)], 12, hexc("#5a3a20"), curve=False)
                soft_disc(cr, x, 860, 50, (1, 0.6, 0.2, 0.5 + 0.2 * math.sin(t * 9 + k)))
        sign(cr, t, A("d8", "twist."), 360, 170, "PLOT TWIST", col=GOLD, size=70)
    else:
        cr.rectangle(0, 0, W, H)                                      # behind bars
        cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2a2a32")), (1, hexc("#14141a"))]))
        cr.fill()
        stephen(cr, t, 360, 1000, 1.0, eyes="sad", mouth="sad", brows="sad", arms=("down", "down"))
        for k in range(7):
            x = 70 + k * 97
            stroke_line(cr, [(x, 120), (x, 1100)], 18, OUTLINE, curve=False)
            stroke_line(cr, [(x, 120), (x, 1100)], 10, hexc("#6a6a7a"), curve=False)
        sign(cr, t, A("d8", "never"), 360, 170, "NEVER CAME OUT", col=RED, size=62)
        cue("thud", t, A("d8", "prison."))
    vignette(cr, 0.55)


def scene_name(cr, t, tl):
    A = tl.at
    _hall(cr, t)
    candles(cr, t, (90, 630), 860)
    throne(cr, 360, 900, 0.8)
    skeleton_pope(cr, t, 360, 800, 0.75, eyes_glow=0.6)
    sign(cr, t, A("d9", "Cadaver"), 360, 170, "THE CADAVER SYNOD", col=PURPLE, size=56, end=A("d9", "creepiest") - 0.05)
    sign(cr, t, A("d9", "creepiest"), 360, 170, "CREEPIEST COURT CASE", col=RED, size=50)
    vignette(cr, 0.6)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a2040"), hexc("#7a4a3a"), seed=8)
    rrect(cr, 230, 470, 260, 330, 12)                                # a history book
    paint(cr, hexc("#8a1a2a"), OUTLINE, 6)
    bold_text(cr, "HISTORY", 360, 580, 44, GOLD, outline=None, shadow=0)
    skeleton_pope(cr, t, 360, 790, 0.35, sway=True)
    sign(cr, t, A("d10", "judge"), 360, 190, "WE JUDGE THE DEAD", col=GOLD, size=52)
    sign(cr, t, A("d10", "fair,"), 190, 400, "FAIR", col=GREEN, size=64, rot=-0.06)
    sign(cr, t, A("d10", "not?"), 530, 400, "NOT FAIR", col=RED, size=56, rot=0.05)
    vignette(cr, 0.35)


SCENES = {"court": scene_court, "dig": scene_dig, "throne": scene_throne, "deacon": scene_deacon,
          "verdict": scene_verdict, "river": scene_river, "twist": scene_twist, "name": scene_name, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("THE DEFENDANT", False), ("IS DEAD", True)], end=tl.at("d2"), y=170, size=104)
    captions(cr, t, tl)
