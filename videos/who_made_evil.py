"""Big question: "If God Made Everything, Did He Make Evil?" -- The Last Bencher, and the teacher answers with a light
switch (Augustine's privation theory), in the polished look.

Script: out/scripts_big_questions_batch2.md, video 2 (owner approved 25 Oct 2026). Augustine, Enchiridion, ch. 11
(c. 420 AD): "what is that which we call evil but the absence of good?" The viral "Einstein and the professor" story
that retells this answer is a myth (Snopes); the fake post on screen is a generic drawing, no real account. Turbo stock
female narrator with tags; the kid and the teacher through Turbo with Kokoro reference voices.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, shake, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, sign, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from videos.bq_kit import mouth_of, talker, two_doors
from videos.last_bencher_4 import chalk, classroom, room

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "e9"          # music drops out under the kid's comeback (research 18 Oct 2026, A5)
SERIES = "The Last Bencher"
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "teacher": dict(voice="af_bella", speed=1.0, turbo_ref="af_bella")})
NIGHT = (0.02, 0.03, 0.08)

SCRIPT = [
    dict(id="e1", scene="board", text="The teacher writes on the board: God made everything. The last bencher raises "
                                      "his hand."),
    dict(id="e2", scene="ask", text="Evil exists, right? So God made evil too?", speaker="kid"),
    dict(id="e3", scene="doors", text="If she says yes, God made evil. If she says no, God didn't make everything."),
    dict(id="e4", scene="switch", text="The teacher walks to the light switch. Click."),
    dict(id="e5", scene="dark", text="Is darkness a thing? Or is it just light missing?", speaker="teacher"),
    dict(id="e6", scene="dark", text="Light missing.", speaker="kid"),
    dict(id="e7", scene="dark", text="Augustine said evil works the same way. It isn't a thing God made. It's goodness "
                                     "missing.", speaker="teacher"),
    dict(id="e8", scene="myth", text="The internet loves to credit this answer to a young Einstein. He never said it. "
                                     "[chuckle]"),
    dict(id="e9", scene="comeback", text="Then who switched the goodness off?", speaker="kid", gap=0.4),
    dict(id="e10", scene="end", text="So, is evil just goodness missing, or is that a clever dodge?", gap=0.3),
]
clear_dialogue(SCRIPT, ids={"e2", "e5", "e6"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="Kid: If God Made Everything, Did He Make Evil? 😶",
    alt_titles=["The Teacher Turned Off the Lights to Answer 💡", "Who Made Evil? 1 Light Switch 💡"],
    description="""The teacher writes on the board: God made everything. The Last Bencher raises his hand: "Evil exists, right? So God made evil too?" 😶

If she says yes, God made evil. If she says no, God didn't make everything. So she turns off the lights: "Is darkness a thing? Or is it just light missing?"

Augustine said evil works the same way: it isn't a thing God made, it's goodness missing. (The internet loves to credit this answer to a young Einstein. He never said it.)

Then the Last Bencher fires back: "Then who switched the goodness off?"

Sources: Augustine, Enchiridion, ch. 11 (c. 420 AD); the "Einstein and the professor" story is a well-known myth.

💬 Is evil just goodness missing, or is that a clever dodge? Keep it respectful 🙏 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending questions, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#Philosophy", "#Shorts"],
    tags=["did god make evil", "who created evil", "augustine evil", "absence of good", "einstein professor myth",
          "the last bencher", "philosophy", "teacher vs student", "deep questions", "interestingly strange"],
    pinned_comment="GOODNESS MISSING or CLEVER DODGE? One reason, keep it respectful 🙏 👇",
)


def teacher(cr, t, tl, x, y, s, **kw):
    talker(cr, t, tl, "teacher", "teacher", x, y, s, rest=kw.pop("rest", "smile"), **kw)


def switch(cr, x, y, on=True):
    rrect(cr, x - 22, y - 34, 44, 68, 8)
    paint(cr, hexc("#f4efe6"), OUTLINE, 4)
    rrect(cr, x - 8, y - 20 if on else y - 2, 16, 22, 4)
    paint(cr, hexc("#d8d0c4"), OUTLINE, 3)


def board_text(cr, t):
    chalk(cr, t, -1, 100, 390, "GOD MADE", 60, dur=0.01)
    chalk(cr, t, -1, 100, 480, "EVERYTHING", 60, dur=0.01)


def darkness(cr, cx, cy, r=420, a=0.9):
    cr.rectangle(0, 0, W, H)
    cr.set_source(rad(cx, cy, r, [(0, (*NIGHT, 0.0)), (0.45, (*NIGHT, a * 0.55)), (1, (*NIGHT, a))]))
    cr.fill()


# ---------------------------------------------------------------- scenes
def scene_board(cr, t, tl):
    A = tl.at
    if t < A("e1", "raises"):
        room(cr, t, board=True)
        chalk(cr, t, 0.0, 100, 390, "GOD MADE", 60, dur=0.4)
        chalk(cr, t, A("e1", "everything"), 100, 480, "EVERYTHING", 60, dur=0.5)
        teacher(cr, t, tl, 560, 1120, 1.0, eyes="open", arms=("point", "down"), look=(-0.6, -0.4), rest="smile")
    else:
        room(cr, t)
        cr.save()
        enter(cr, camera(t, [(A("e1", "raises") - 0.1, (1.0, 360, 640)), (A("e1", "hand"), (1.5, 520, 520))],
                         dur=0.6))
        classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth="smile", brows="raise"),
                  look_at=(560, 500))
        cr.restore()
    vignette(cr, 0.45)


def scene_ask(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("e2") - 0.3, (2.0, 555, 470)), (A("e2", "So"), (2.05, 575, 470))], dur=0.8))
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth=mouth_of(tl, "kid", t, "smug"),
                                       brows="raise"), look_at=(560, 500))
    cr.restore()
    card(cr, t, A("e2", "Evil"), 360, 290, 560, 120, "EVIL EXISTS", [], col=PURPLE, title_size=40,
         end=A("e2", "So") - 0.05)
    card(cr, t, A("e2", "So"), 360, 290, 560, 120, "SO GOD MADE EVIL?", [], col=RED, title_size=40)
    vignette(cr, 0.45)


def scene_doors(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=51)
    two_doors(cr, t, ["YES", "NO"], [RED, BLUE], x_at=(A("e3", "evil"), A("e3", "everything")), label_size=44)
    card(cr, t, tl.scene_at(t)[1], 190, 380, 300, 120, "GOD MADE EVIL", [], col=RED, title_size=30)
    if t >= A("e3", "no"):
        card(cr, t, A("e3", "no"), 530, 380, 300, 120, "NOT EVERYTHING", [], col=BLUE, title_size=30)
    vignette(cr, 0.4)


def scene_switch(cr, t, tl):
    A = tl.at
    click = A("e4", "Click")
    room(cr, t, board=True)
    board_text(cr, t)
    switch(cr, 640, 700, on=t < click)
    u = seg(t, A("e4"), A("e4", "switch", end=True))
    teacher(cr, t, tl, lerp(300, 560, u), 1120, 1.0, eyes="half", mouth="smug", walk=t * 8 if u < 1 else None,
            arms=("down", (150, -40)) if u >= 1 else ("down", "down"), look=(0.6, 0.0))
    if t >= click:
        cue("lock", t, click, 0.2)
        darkness(cr, 470, 700, 380, a=0.93)
        stamp(cr, t, click, 360, 260, "CLICK", col=GOLD, size=70)
    vignette(cr, 0.45)


def scene_dark(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    board_text(cr, t)
    switch(cr, 640, 700, on=False)
    cr.save()
    enter(cr, camera(t, [(A("e5") - 0.3, (1.3, 420, 700)), (A("e7"), (1.45, 440, 680))], dur=0.6))
    teacher(cr, t, tl, 470, 1120, 1.0, eyes="half" if t < A("e7") else "happy", rest="smile",
            arms=("hips", "point") if t >= A("e7") else ("down", (150, -40)), look=(-0.5, -0.1))
    cr.restore()
    darkness(cr, 450, 560, 360, a=0.92)
    sign(cr, t, A("e5", "darkness"), 360, 200, "IS DARKNESS A THING?", col=BLUE, size=50, end=A("e6") - 0.05)
    if A("e6") <= t < A("e7"):
        tag(cr, t, A("e6"), 360, 200, "LIGHT MISSING", col=GOLD, size=54)
    if t >= A("e7"):
        card(cr, t, A("e7", "Augustine"), 360, 250, 520, 200, "AUGUSTINE · ~400 AD", ["EVIL =", "GOODNESS MISSING"],
             col=GREEN, title_size=32, line_size=40)
    vignette(cr, 0.45)


def scene_myth(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1e2638"), hexc("#3a4a66"), seed=52)
    s0 = tl.scene_at(t)[1]
    k = min(1.0, 0.7 + 1.5 * (t - s0))
    cr.save()                                                      # a generic viral post (no real account)
    cr.translate(360, 560)
    cr.scale(k, k)
    rrect(cr, -270, -230, 540, 460, 26)
    paint(cr, WHITE, OUTLINE, 6)
    ellipse(cr, -200, -170, 34, 34)
    paint(cr, hexc("#c8c8d8"), OUTLINE, 4)
    rrect(cr, -150, -190, 200, 18, 9)
    paint(cr, hexc("#d8d8e4"), None, 0)
    rrect(cr, -150, -160, 120, 14, 7)
    paint(cr, hexc("#e4e4ee"), None, 0)
    bold_text(cr, "YOUNG EINSTEIN", 0, -70, 44, hexc("#2b2b33"), outline=None, shadow=0)
    bold_text(cr, "DESTROYS HIS", 0, -20, 44, hexc("#2b2b33"), outline=None, shadow=0)
    bold_text(cr, "PROFESSOR!", 0, 30, 44, hexc("#2b2b33"), outline=None, shadow=0)
    bold_text(cr, "2.1M SHARES", -110, 170, 30, hexc("#8a8a9a"), outline=None, shadow=0)
    cr.restore()
    if t >= A("e8", "never"):
        stamp(cr, t, A("e8", "never"), 360, 560, "MYTH", col=RED, size=120)
    vignette(cr, 0.4)


def scene_comeback(cr, t, tl):
    A = tl.at
    room(cr, t)
    off = t >= A("e9", "off")
    cr.save()
    enter(cr, camera(t, [(A("e9") - 0.3, (2.0, 555, 470)), (A("e9", "off"), (2.15, 560, 460))], dur=0.5))
    classroom(cr, t, tl, kid_pose=dict(arms=("think", "down"), eyes="half", mouth=mouth_of(tl, "kid", t, "smug"),
                                       brows="raise"), look_at=(560, 500), gasp=off)
    cr.restore()
    if off:
        sign(cr, t, A("e9", "off"), 360, 230, "WHO SWITCHED IT OFF?", col=RED, size=52)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("e10"), (1.1, 360, 700))]))
    teacher(cr, t, None, 470, 1120, 1.0, eyes="wide", mouth="o", brows="up", arms=("front", "down"))
    cr.restore()
    sign(cr, t, A("e10", "goodness"), 360, 220, "GOODNESS MISSING?", col=GREEN, size=50)
    buttons(cr, t, A("e10", "dodge"), [("GOOD MISSING", GREEN), ("CLEVER DODGE", RED)], y=380, size=40)
    vignette(cr, 0.35)


SCENES = {"board": scene_board, "ask": scene_ask, "doors": scene_doors, "switch": scene_switch, "dark": scene_dark,
          "myth": scene_myth, "comeback": scene_comeback, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("DID GOD", False), ("MAKE EVIL?", True)], end=tl.at("e2"), y=190, size=96)
    captions(cr, t, tl)
