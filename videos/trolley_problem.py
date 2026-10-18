"""Big question 3: "Pull the Lever. But Don't Push?" -- the trolley problem and the footbridge, drawn on the board in
class, in the polished look.

Script: out/scripts_big_questions_batch1.md, row 69 (owner approved 18 Oct 2026). Philippa Foot introduced the
trolley case (1967); Judith Jarvis Thomson added the footbridge version (1976, 1985). Most people say they'd pull the
lever but wouldn't push, though the numbers are the same. Turbo stock female narrator with tags; the teacher through
Turbo with a Kokoro reference voice.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, red_x, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rrect,
                           sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import ROWS, desk, room

NARRATOR = dict(turbo=True)
TAIL = 0.9
voice.SPEAKERS.update({"teacher": dict(voice="af_bella", speed=1.0, turbo_ref="af_bella")})
CHALK = (0.97, 0.97, 0.94, 0.95)

SCRIPT = [
    dict(id="t1", scene="board", text="The teacher draws a runaway train on the board. Five people stand on the track "
                                      "ahead."),
    dict(id="t2", scene="lever", text="You can pull a lever. The train turns, and hits one person instead. Do you pull "
                                      "it?", speaker="teacher"),
    dict(id="t3", scene="hands", text="Almost every hand goes up. One life, to save five. Easy."),
    dict(id="t4", scene="bridge", text="New version. No lever. You're on a bridge, next to a big man. Push him, and the "
                                       "train stops. Five saved.", speaker="teacher"),
    dict(id="t5", scene="down", text="Every hand goes down. [gasp]"),
    dict(id="t6", scene="math", text="But it's the same math. One dies. Five live."),
    dict(id="t7", scene="named", text="Philosophers have argued about this since [nineteen sixty seven.|1967.]"),
    dict(id="t8", scene="sides", text="Some say only the result matters. Others say using a person as a tool is wrong, "
                                      "whatever the math."),
    dict(id="t9", scene="end", text="So, would you push him? And if not, why did you pull the lever?", gap=0.3),
]

METADATA = dict(
    title="Everyone Pulled the Lever. Nobody Would Push 🚃",
    alt_titles=["Would You Push Him? The Trolley Problem 🚃", "Same Math. Different Answer. Why? 🚃"],
    description="""A runaway train. Five people on the track. You can pull a lever: the train turns and hits one person instead. Almost everyone pulls it. 🚃

New version: no lever. You're on a bridge next to a big man. Push him, and the train stops. Five saved. Almost nobody pushes.

Same math: one dies, five live. So why do we answer differently? Some say only the result matters; others say using a person as a tool is wrong, whatever the math.

The trolley problem: Philippa Foot (1967); the footbridge version: Judith Jarvis Thomson.

💬 Would you push him? And if not, why did you pull the lever? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#TrolleyProblem", "#Philosophy", "#Shorts"],
    tags=["trolley problem", "would you push the man", "footbridge dilemma", "moral dilemma", "philosophy",
          "ethics", "thought experiment", "would you rather", "teacher asks class", "interestingly strange"],
    pinned_comment="Would you push him? PUSH or DON'T PUSH... and if not, why pull the lever? 👇",
)


def chalk_line(cr, pts, w=6, a=1.0, u=1.0):
    n = max(2, int(len(pts) * u))
    stroke_line(cr, pts[:n], w, (CHALK[0], CHALK[1], CHALK[2], CHALK[3] * a), curve=False)


def stick(cr, x, y, s=1.0, a=1.0, col=CHALK):
    c = (col[0], col[1], col[2], (col[3] if len(col) > 3 else 1) * a)
    cr.arc(x, y - 46 * s, 10 * s, 0, 2 * math.pi)
    cr.set_source_rgba(*c)
    cr.set_line_width(4)
    cr.stroke()
    for p in ([(x, y - 36 * s), (x, y - 10 * s)], [(x, y - 10 * s), (x - 9 * s, y + 8 * s)],
              [(x, y - 10 * s), (x + 9 * s, y + 8 * s)], [(x - 12 * s, y - 28 * s), (x + 12 * s, y - 28 * s)]):
        stroke_line(cr, p, 4, c, curve=False)


def chalk_train(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_source_rgba(*CHALK)
    cr.set_line_width(5)
    cr.rectangle(-60, -50, 120, 50)
    cr.stroke()
    cr.rectangle(-40, -80, 50, 30)
    cr.stroke()
    for wx in (-35, 35):
        cr.arc(wx, 6, 12, 0, 2 * math.pi)
        cr.stroke()
    for k in range(3):                                              # speed lines
        stroke_line(cr, [(-80 - k * 6, -40 + k * 15), (-120 - k * 6, -40 + k * 15)], 3, CHALK, curve=False)
    cr.restore()


def teacher(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", "talk" if tl.speaking("teacher", t) else "smile")
    person(cr, t, x, y, s, "teacher", **kw)


def class_rows(cr, t, hands=0.0, gasp=False, seed=0):
    """All three rows of pupils; `hands` 0..1 = how many hands are up (front-left first)."""
    order = 0
    total = sum(len(k) for _, _, k in ROWS)
    for k, (dy, s, kids) in enumerate(ROWS):
        for j, (x, who) in enumerate(kids):
            up = order < hands * total
            order += 1
            person(cr, t, x, dy + 46 * s, s, who, eyes="wide" if gasp else ("happy" if up else "open"),
                   mouth="o" if gasp else "smile", arms=("up", "down") if up else ("front", "front"), seed=k * 5 + j)
            desk(cr, x, dy, 170, s)


def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    u = seg(t, 0.0, A("t1", "board.", end=True))
    chalk_line(cr, [(90, 470), (630, 470)], 6, u=1.0)
    for k in range(9):
        chalk_line(cr, [(110 + k * 62, 455), (110 + k * 62, 485)], 4)
    x = lerp(110, 260, u) + 6 * math.sin(t * 20)
    chalk_train(cr, x, 460, 1.0)
    if t >= A("t1", "Five"):
        for k in range(5):
            stick(cr, 470 + k * 34, 462, 0.9)
        cue("scribble", t, A("t1", "Five"), 0.6)
    teacher(cr, t, tl, 600, 1120, 1.0, eyes="open", arms=("point", "hips"))
    vignette(cr, 0.4)


def scene_lever(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk_line(cr, [(90, 470), (630, 470)], 6)
    chalk_line(cr, [(330, 470), (420, 380), (630, 380)], 6)        # the side track
    chalk_train(cr, 230 + 6 * math.sin(t * 20), 460, 0.9)
    for k in range(5):
        stick(cr, 470 + k * 34, 462, 0.85)
    stick(cr, 560, 372, 0.85, col=(1, 0.85, 0.4, 1))
    pulled = t >= A("t2", "turns,")
    cr.save()                                                      # the lever
    cr.translate(330, 520)
    cr.rotate(0.6 if pulled else -0.6)
    stroke_line(cr, [(0, 0), (0, -60)], 8, (1, 0.85, 0.4, 1), curve=False)
    cr.arc(0, -64, 10, 0, 2 * math.pi)
    cr.set_source_rgba(1, 0.85, 0.4, 1)
    cr.fill()
    cr.restore()
    teacher(cr, t, tl, 600, 1120, 1.0, eyes="open", arms=("point", "hips"))
    sign(cr, t, A("t2", "pull"), 360, 650, "PULL THE LEVER?", col=GOLD, size=56)
    vignette(cr, 0.4)


def scene_hands(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("t3") - 0.3, (1.05, 360, 640))]))
    class_rows(cr, t, hands=0.95 * seg(t, A("t3"), A("t3", "up.", end=True)))
    cr.restore()
    sign(cr, t, A("t3", "up."), 360, 180, "PULL: ALMOST EVERYONE", col=GREEN, size=50, end=A("t3", "Easy.") - 0.05)
    sign(cr, t, A("t3", "Easy."), 360, 180, "1 LIFE FOR 5. EASY.", col=GREEN, size=54)
    vignette(cr, 0.4)


def scene_bridge(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk_line(cr, [(90, 500), (630, 500)], 6)
    chalk_line(cr, [(250, 380), (470, 380)], 6)                    # the bridge over the track
    for x in (270, 450):
        chalk_line(cr, [(x, 380), (x, 500)], 5)
    chalk_train(cr, 160 + 6 * math.sin(t * 20), 490, 0.8)
    for k in range(5):
        stick(cr, 500 + k * 28, 492, 0.75)
    if t >= A("t4", "bridge,"):
        stick(cr, 340, 372, 0.9, col=(1, 0.85, 0.4, 1))            # you
        bold_text(cr, "YOU", 340, 300, 28, GOLD, outline=None, shadow=0)
    if t >= A("t4", "big"):
        stick(cr, 390, 372, 1.35)                                  # the big man
    if t >= A("t4", "Push"):
        stroke_line(cr, [(352, 340), (378, 340)], 6, (1, 0.5, 0.4, 1), curve=False)
    teacher(cr, t, tl, 600, 1120, 1.0, eyes="half", arms=("point", "hips"))
    sign(cr, t, A("t4", "New"), 360, 650, "NEW VERSION", col=PURPLE, size=56, end=A("t4", "Push") - 0.05)
    sign(cr, t, A("t4", "Push"), 360, 650, "PUSH HIM?", col=RED, size=64)
    vignette(cr, 0.4)


def scene_down(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("t5") - 0.3, (1.05, 360, 640))]))
    class_rows(cr, t, hands=0.95 * (1 - seg(t, A("t5"), A("t5", "down.", end=True))), gasp=t >= A("t5", "down."))
    cr.restore()
    stamp(cr, t, A("t5", "down."), 360, 200, "PUSH: ALMOST NOBODY", col=RED, size=52)
    vignette(cr, 0.4)


def scene_math(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=3)
    card(cr, t, A("t6"), 190, 520, 300, 230, "LEVER", ["1 DIES", "5 LIVE"], col=GREEN, title_size=40, line_size=48)
    card(cr, t, A("t6") + 0.15, 530, 520, 300, 230, "PUSH", ["1 DIES", "5 LIVE"], col=RED, title_size=40,
         line_size=48)
    if t >= A("t6", "same"):
        bold_text(cr, "=", 360, 545, 90, GOLD)
    sign(cr, t, A("t6", "same"), 360, 200, "SAME MATH", col=GOLD, size=72)
    vignette(cr, 0.4)


def scene_named(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=4)
    for k, x in enumerate((200, 520)):                              # two philosophers arguing
        person(cr, t, x, 980, 0.75, ("russell", "aquinas")[k], facing=1 if k == 0 else -1, eyes="angry",
               brows="angry", mouth="talk" if int(t * 3 + k) % 2 else "open", arms=("point", "hips"), seed=k)
    sign(cr, t, A("t7", "Philosophers"), 360, 200, "THE TROLLEY PROBLEM", col=PURPLE, size=52)
    tag(cr, t, A("t7", "1967."), 360, 330, "SINCE 1967", col=GOLD, size=52)
    vignette(cr, 0.35)


def scene_sides(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=5)
    card(cr, t, A("t8", "result"), 190, 520, 310, 250, "SIDE A", ["ONLY THE", "RESULT", "MATTERS"], col=GREEN,
         title_size=34, line_size=40)
    card(cr, t, A("t8", "tool"), 530, 520, 310, 250, "SIDE B", ["A PERSON", "IS NOT", "A TOOL"], col=RED,
         title_size=34, line_size=40)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    chalk_line(cr, [(250, 380), (470, 380)], 6)
    stick(cr, 340, 372, 0.9, col=(1, 0.85, 0.4, 1))
    stick(cr, 390, 372, 1.35)
    sign(cr, t, A("t9", "push"), 360, 640, "WOULD YOU PUSH?", col=GOLD, size=56)
    buttons(cr, t, A("t9", "push"), [("PUSH", RED), ("DON'T PUSH", GREEN)], y=800, size=46)
    if t >= A("t9", "lever?"):
        tag(cr, t, A("t9", "lever?"), 360, 250, "THEN WHY PULL THE LEVER?", col=PURPLE, size=40)
    vignette(cr, 0.35)


SCENES = {"board": scene_board, "lever": scene_lever, "hands": scene_hands, "bridge": scene_bridge,
          "down": scene_down, "math": scene_math, "named": scene_named, "sides": scene_sides, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("5 PEOPLE.", False), ("1 LEVER.", True)], end=tl.at("t2"), y=170, size=110)
    captions(cr, t, tl)
