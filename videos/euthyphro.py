"""Big question 5: "Is It Wrong Because God Says So?" -- the Euthyphro dilemma as a Last Bencher classroom scene, in
the polished look.

Script: out/scripts_big_questions_batch1.md, row 71 (owner approved 18 Oct 2026). Plato, Euthyphro (about 399 BC):
is the pious loved by the gods because it is pious, or pious because it is loved? The teacher's reply is the classical
theist answer (goodness is God's nature, not a rule God picks; e.g. Aquinas, Summa Theologiae I, q.6). Both horns are
shown fairly; nobody is mocked. Turbo stock female narrator with tags; the kid and the teacher through Turbo.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, red_x, shake, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rrect,
                           sign, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person, portrait
from videos.last_bencher_4 import chalk, classroom, room

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "e3"          # music drops out under this line (research 18 Oct 2026, A5)
SERIES = "The Last Bencher"
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "teacher": dict(voice="af_bella", speed=1.0, turbo_ref="af_bella")})

SCRIPT = [
    dict(id="e2", scene="ask", text="Ma'am, is lying wrong because God says so? Or does God say so, because it's "
                                    "wrong?", speaker="kid"),
    dict(id="e3", scene="freeze", text="The teacher opens her mouth. And closes it.", gap=0.45),
    dict(id="e4", scene="doors", text="Because both answers have a problem."),
    dict(id="e5", scene="doors", text="If it's wrong only because God says so, then if God said lie, lying would be "
                                      "good."),
    dict(id="e6", scene="doors", text="If God says so because it's already wrong, then right and wrong exist without "
                                      "God."),
    dict(id="e7", scene="plato", text="This question is [two thousand four hundred years old.|2,400 years old.] Plato "
                                      "wrote it down."),
    dict(id="e8", scene="answer", text="Some thinkers answer. Goodness isn't a rule God picks. It's what God is.",
         speaker="teacher"),
    dict(id="e9", scene="kid", text="So God can't command a lie, because God is truth?", speaker="kid"),
    dict(id="e10", scene="answer2", text="Exactly. Now do your homework. Truthfully. [chuckle]", speaker="teacher",
         gap=0.3),
    dict(id="e11", scene="end", text="So, does right and wrong need God? Yes, or no?", gap=0.3),
]
clear_dialogue(SCRIPT, ids={"e2", "e5", "e6"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="1 Question. The Teacher Couldn't Pick an Answer 🤔",
    alt_titles=["Is It Wrong Because God Says So? 🤔", "The Last Bencher's 2,400-Year-Old Question 🤔"],
    description="""Moral science class. The teacher says lying is wrong, because God says so. Then the Last Bencher raises his hand: "Ma'am, is lying wrong because God says so? Or does God say so, because it's wrong?" 🤔

Both answers have a problem. If it's wrong only because God says so, then if God said "lie", lying would be good. If God says so because it's already wrong, then right and wrong exist without God.

This question is 2,400 years old: Plato wrote it down (the Euthyphro dilemma). Some thinkers answer that goodness isn't a rule God picks; it's what God is.

💬 Does right and wrong need God? Yes or no, and why? Keep it respectful 🙏 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#Philosophy", "#Shorts"],
    tags=["euthyphro dilemma", "is it wrong because god says so", "plato", "morality and god", "the last bencher",
          "philosophy", "teacher vs student", "deep questions", "moral dilemma", "interestingly strange"],
    pinned_comment="Does right and wrong need God? YES or NO, give one reason (and keep it respectful) 👇",
)


def mouth_of(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


def teacher(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", mouth_of(tl, "teacher", t, kw.pop("rest", "smile")))
    person(cr, t, x, y, s, "teacher", **kw)


def door(cr, x, y, s, label, col):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -110, -300, 220, 300, 12)
    paint(cr, lin(0, -300, 0, 0, [(0, col), (1, col)]), OUTLINE, 6)
    cr.arc(70, -150, 12, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 4)
    cr.restore()
    bold_text(cr, label, x, y - 330 * s, 34, WHITE)


def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk(cr, t, 0.0, 100, 390, "LYING IS WRONG", 52, dur=0.5)
    if t >= A("e1", "because"):
        chalk(cr, t, A("e1", "because"), 100, 470, "BECAUSE GOD SAYS SO", 42, dur=0.6)
    raised = t >= A("e1", "raises")
    teacher(cr, t, tl, 150, 1120, 1.0, eyes="open", arms=("point", "down"), rest="smile")
    if raised:
        cr.save()
        enter(cr, camera(t, [(A("e1", "raises") - 0.1, (1.0, 360, 640)), (A("e1", "hand."), (1.5, 520, 520))],
                         dur=0.6))
        classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth="smile", brows="raise"))
        cr.restore()
    vignette(cr, 0.45)


def scene_ask(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("e2") - 0.3, (2.0, 555, 470)), (A("e2", "Or"), (2.05, 575, 470))], dur=0.8))
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth=mouth_of(tl, "kid", t, "smug"),
                                       brows="raise"))
    cr.restore()
    card(cr, t, A("e2", "Or"), 360, 300, 600, 120, "GOD SAYS SO BECAUSE IT'S WRONG?", [], col=BLUE, title_size=32)
    vignette(cr, 0.45)


def scene_freeze(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk(cr, t, -1, 100, 390, "LYING IS WRONG", 52, dur=0.01)
    opened = A("e3", "opens") <= t < A("e3", "closes")
    cr.save()
    if t >= A("e3", "closes"):
        dx, dy = shake(t, A("e3", "closes"), 0.3, 6)
        cr.translate(dx, dy)
    teacher(cr, t, tl, 360, 1080, 1.1, eyes="wide", rest="o" if opened else "flat", brows="up", arms=("front", "down"),
            sweat=t >= A("e3", "closes"))
    cr.restore()
    stamp(cr, t, A("e3", "closes"), 360, 230, "...", col=BLUE, size=100)
    vignette(cr, 0.45)


def scene_doors(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=3)
    door(cr, 190, 900, 0.9, "GOD SAYS SO", PURPLE)
    door(cr, 530, 900, 0.9, "ALREADY WRONG", BLUE)
    sign(cr, t, A("e4", "both"), 360, 190, "BOTH HAVE A PROBLEM", col=RED, size=52, end=A("e5") - 0.05)
    if t >= A("e5"):
        card(cr, t, A("e5", "said"), 360, 270, 620, 150, "IF GOD SAID LIE...", ["LYING WOULD BE GOOD?"], col=PURPLE,
             title_size=36, line_size=38, end=A("e6") - 0.05)
        red_x(cr, t, A("e5", "good."), 190, 750, 70)
    if t >= A("e6"):
        card(cr, t, A("e6", "exist"), 360, 270, 620, 150, "THEN RIGHT AND WRONG", ["EXIST WITHOUT GOD?"], col=BLUE,
             title_size=36, line_size=38)
        red_x(cr, t, A("e6", "God."), 530, 750, 70)
        red_x(cr, t, A("e6"), 190, 750, 70)
    vignette(cr, 0.4)


def scene_plato(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#e8d0a0"), seed=4)
    cr.save()                                                        # an old scroll
    cr.translate(360, 620)
    rrect(cr, -220, -170, 440, 340, 10)
    paint(cr, hexc("#f2e2b8"), OUTLINE, 6)
    for side in (-1, 1):
        rrect(cr, -240, side * 170 - 22, 480, 44, 22)
        paint(cr, hexc("#c8a868"), OUTLINE, 5)
    for k in range(6):
        stroke_line(cr, [(-170, -110 + k * 40), (170 - 40 * (k % 2), -110 + k * 40)], 4, alpha(OUTLINE, 0.35),
                    curve=False)
    cr.restore()
    tag(cr, t, A("e7", "2,400"), 360, 230, "2,400 YEARS OLD", col=GOLD, size=52)
    if t >= A("e7", "Plato"):
        sign(cr, t, A("e7", "Plato"), 360, 330, "PLATO, ABOUT 399 BC", col=hexc("#a8713e"), size=40)
    vignette(cr, 0.35)


def scene_answer(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk(cr, t, A("e8", "Goodness"), 100, 390, "GOODNESS =", 52, dur=0.4)
    chalk(cr, t, A("e8", "what"), 100, 470, "WHAT GOD IS", 52, dur=0.4)
    cr.save()
    enter(cr, camera(t, [(A("e8") - 0.3, (1.15, 360, 640))]))
    teacher(cr, t, tl, 560, 1100, 1.0, eyes="happy", arms=("point", "hips"))
    cr.restore()
    card(cr, t, A("e8", "rule"), 230, 640, 400, 110, "NOT A RULE GOD PICKS", [], col=GREEN, title_size=30,
         end=A("e8", "what") - 0.05)
    vignette(cr, 0.4)


def scene_kid(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("e9") - 0.3, (2.0, 555, 470))]))
    classroom(cr, t, tl, kid_pose=dict(arms=("think", "down"), eyes="half", mouth=mouth_of(tl, "kid", t, "flat"),
                                       brows="raise"))
    cr.restore()
    tag(cr, t, A("e9", "truth?"), 360, 230, "GOD IS TRUTH", col=GOLD, size=50)
    vignette(cr, 0.45)


def scene_answer2(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("e10") - 0.1, (1.5, 360, 560))]))
    teacher(cr, t, tl, 360, 900, 1.0, eyes="happy", arms=("hips", "point"))
    cr.restore()
    sign(cr, t, A("e10", "Exactly."), 360, 200, "EXACTLY", col=GREEN, size=70, end=A("e10", "homework.") - 0.05)
    if t >= A("e10", "homework."):
        stamp(cr, t, A("e10", "Truthfully."), 360, 230, "HOMEWORK: TRUTHFULLY", col=PURPLE, size=50)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    soft_disc(cr, 360, 640, 120, (1, 0.95, 0.7, 0.4))
    person(cr, t, 360, 920, 0.6, "kid", eyes="open", mouth="o", arms=("shrug", "shrug"))
    sign(cr, t, A("e11", "need"), 360, 200, "DOES RIGHT & WRONG", col=GOLD, size=48, sub="NEED GOD?", sub_col=WHITE)
    buttons(cr, t, A("e11", "Yes,"), [("YES", GREEN), ("NO", RED)], y=420, size=56)
    vignette(cr, 0.3)


SCENES = {"board": scene_board, "ask": scene_ask, "freeze": scene_freeze, "doors": scene_doors, "plato": scene_plato,
          "answer": scene_answer, "kid": scene_kid, "answer2": scene_answer2, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("WRONG BECAUSE", False), ("GOD SAYS SO?", True)], end=tl.at("e2", "Or") - 0.2, y=170, size=100)
    captions(cr, t, tl)
