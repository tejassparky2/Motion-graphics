"""Hook test H1 (contradict a belief): "This Teacher LET Her Class Cheat".

Script: out/scripts_hook_test.md, H1 (owner approved 15 Oct 2026). Original story (fiction): the cheat sheet is the
size of a sticky note, so making it IS the studying. Turbo voice with tags; the teacher through Turbo with a
synthetic Kokoro reference voice.
"""
import math
import random

from motion import thriller as th
from motion import voice
from motion.engine import W, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, enter, lin, paint, rrect, sign,
                           soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import (BLUE, GOLD, GREEN, PURPLE, RED, chalk, classroom, desk, mouth_of, room, sparkles,
                                   studio)

NARRATOR = dict(turbo=True)
TAIL = 0.9
voice.SPEAKERS.update({"teacher": dict(voice="af_bella", speed=1.0, turbo_ref="af_bella")})
NOTE = hexc("#ffe066")

SCRIPT = [
    dict(id="b1", scene="board", text="This teacher let her whole class cheat on the final exam."),
    dict(id="b2", scene="rule", text="One rule. You can bring one cheat sheet. The size of a sticky note."),
    dict(id="b3", scene="cheer", text="[gasp] The class went crazy."),
    dict(id="b4", scene="night", text="That night, everyone tried to squeeze the whole book onto one tiny note."),
    dict(id="b5", scene="note", text="They shortened every formula. Picked only the most important ones. Wrote them "
                                     "again and again to make them fit."),
    dict(id="b6", scene="exam", text="On exam day, the teacher said. Take out your cheat sheets.", speaker="teacher",
         speaker_from="Take"),
    dict(id="b7", scene="exam", text="Nobody looked at theirs.", gap=0.35),
    dict(id="b8", scene="smile", text="By making the cheat sheet, they had already learned everything on it. "
                                      "[chuckle]"),
    dict(id="b9", scene="end", text="So, was it cheating? Or the smartest homework ever?", gap=0.3),
]

METADATA = dict(
    title="This Teacher LET Her Class Cheat 📝",
    alt_titles=["The Cheat Sheet Trick That Backfired (On Purpose) 📝", "She Allowed Cheating. Everyone Passed. Why?"],
    description="""This teacher let her whole class cheat on the final exam. 📝

One rule: one cheat sheet, the size of a sticky note.

That night, everyone tried to squeeze the whole book onto one tiny note... and on exam day, nobody even looked at theirs. 😏

A short story with a twist (fiction).

💬 Was it cheating, or the smartest homework ever? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Teacher", "#PlotTwist", "#Shorts"],
    tags=["teacher let class cheat", "cheat sheet", "smart teacher", "study hack", "exam story", "plot twist",
          "school story", "teacher vs student", "study tips", "interestingly strange"],
    pinned_comment="Cheating 😈 or genius homework 🧠? Which side are you on? 👇",
)


def sticky(cr, x, y, s, rot=0.0, lines=0, tiny=False, seed=1):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_disc(cr, 6, 10, 70, (0, 0, 0, 0.25))
    rrect(cr, -60, -60, 120, 120, 4)
    paint(cr, NOTE, OUTLINE, 5)
    rng = random.Random(seed)
    for k in range(lines):
        y0 = -48 + k * (6 if tiny else 14)
        if y0 > 52:
            break
        stroke_line(cr, [(-50, y0), (-50 + 60 + rng.random() * 40, y0)], 1.6 if tiny else 4,
                    (0.15, 0.15, 0.3, 0.9), curve=False)
    cr.restore()


def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cam = camera(t, [(0.0, (1.0, 360, 640)), (A("b1", "cheat"), (1.1, 330, 580))], dur=1.0)
    cr.save()
    enter(cr, cam)
    chalk(cr, t, 0.0, 110, 340, "FINAL EXAM:", 48, dur=0.4)
    chalk(cr, t, A("b1", "cheat"), 110, 430, "CHEATING", 58, dur=0.4)
    chalk(cr, t, A("b1", "final"), 110, 510, "ALLOWED", 58, dur=0.4)
    person(cr, t, 560, 900, 1.0, "teacher", facing=-1, eyes="happy", mouth="grin", arms=("point", "hips"))
    cr.restore()
    vignette(cr, 0.4)


def scene_rule(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8f0dc"), hexc("#fff6e8"), seed=2)
    sign(cr, t, A("b2"), 360, 170, "ONE RULE", col=RED, size=70, end=A("b2", "sticky") - 0.05)
    if t >= A("b2", "cheat"):
        k = appear(t, A("b2", "cheat"), 0.4)
        big = 1.0 - 0.55 * ease_out(seg(t, A("b2", "size"), A("b2", "note.", end=True)))
        sticky(cr, 360, 560, 3.2 * k * big, 0.05)
    if t >= A("b2", "size"):                                       # a ruler showing how small it is
        rrect(cr, 110, 820, 500, 60, 6)
        paint(cr, hexc("#f0d080"), OUTLINE, 5)
        for j in range(11):
            stroke_line(cr, [(130 + j * 46, 820), (130 + j * 46, 845 if j % 5 else 860)], 4, OUTLINE, curve=False)
    sign(cr, t, A("b2", "sticky"), 360, 170, "STICKY-NOTE SIZE", col=GOLD, size=58)
    vignette(cr, 0.3)


def scene_cheer(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("b3") - 0.3, (1.0, 360, 640)), (A("b3", "crazy."), (1.06, 360, 620))], dur=0.5))
    crazy = t >= A("b3", "went")
    classroom(cr, t, tl, gasp=not crazy, kid_pose=dict(arms=("up", "up") if crazy else ("front", "front"),
                                                      eyes="happy" if crazy else "wide", mouth="grin" if crazy else "o"))
    cr.restore()
    if crazy:
        for k in range(10):                                        # papers flying
            ph = (t * 0.9 + k * 0.13) % 1
            x = 60 + (k * 67) % 600
            y = 900 - ph * 800
            cr.save()
            cr.translate(x, y)
            cr.rotate(ph * 6 + k)
            rrect(cr, -26, -34, 52, 68, 3)
            paint(cr, WHITE, OUTLINE, 3)
            cr.restore()
        cue("whoosh", t, A("b3", "went"))
    vignette(cr, 0.4)


def scene_night(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, 1280)
    cr.set_source(lin(0, 0, 0, 1280, [(0, hexc("#14203a")), (1, hexc("#26365a"))]))
    cr.fill()
    rrect(cr, 430, 140, 220, 260, 12)                              # night window with a moon
    paint(cr, hexc("#0c1428"), OUTLINE, 6)
    cr.arc(560, 230, 34, 0, 2 * math.pi)
    paint(cr, hexc("#fff3c4"), None)
    soft_disc(cr, 230, 600, 300, (1, 0.9, 0.55, 0.35))             # desk-lamp glow
    person(cr, t, 330, 900, 1.0, "kid", eyes="half", mouth="flat", arms=("front", "front"), look=(0, 0.6))
    desk(cr, 330, 760, 360, 1.0)
    stroke_line(cr, [(160, 700), (160, 560), (230, 520)], 10, OUTLINE)   # the lamp
    stroke_line(cr, [(160, 700), (160, 560), (230, 520)], 6, hexc("#e8e8e8"))
    lines = int(18 * seg(t, A("b4", "squeeze"), A("b4", "note.", end=True) + 1.0))
    sticky(cr, 420, 700, 0.9, -0.05, lines, tiny=True)
    sign(cr, t, A("b4", "book"), 360, 120, "WHOLE BOOK -> 1 NOTE", col=PURPLE, size=44)
    vignette(cr, 0.5)


def scene_note(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=5)
    lines = int(4 + 40 * seg(t, A("b5"), A("b5", "fit.", end=True)))
    sticky(cr, 360, 560, 3.6, 0.03, lines, tiny=True, seed=3)
    if t >= A("b5", "Picked"):                                     # crossing out the unimportant bits
        for k in range(3):
            st = A("b5", "Picked") + 0.25 * k
            if t >= st:
                y = 420 + k * 80
                stroke_line(cr, [(200, y), (lerp(200, 520, seg(t, st, st + 0.25)), y + 6)], 8, RED, curve=False)
    sign(cr, t, A("b5", "shortened"), 360, 170, "SHRINK", col=BLUE, size=64, end=A("b5", "Picked") - 0.05)
    sign(cr, t, A("b5", "Picked"), 360, 170, "PICK", col=GREEN, size=64, end=A("b5", "Wrote") - 0.05)
    sign(cr, t, A("b5", "Wrote"), 360, 170, "REWRITE x10", col=PURPLE, size=64)
    vignette(cr, 0.3)


def scene_exam(cr, t, tl):
    A = tl.at
    room(cr, t)
    nobody = t >= A("b7")
    cr.save()
    enter(cr, camera(t, [(A("b6") - 0.3, (1.0, 360, 640)), (A("b7"), (1.25, 400, 600))], dur=0.6))

    def note_on_desk(c, tt, x, dy, s):
        sticky(c, x + 50 * s, dy - 10 * s, 0.35 * s, 0.2, 8, tiny=True)

    classroom(cr, t, tl, kid_pose=dict(arms=("front", "front"), eyes="half" if nobody else "open",
                                       mouth="smug" if nobody else "smile"), extra=note_on_desk)
    if t >= A("b6", "Take"):                                       # everyone's sticky note
        for k, (x, y) in enumerate(((140, 660), (330, 650), (560, 640), (265, 760), (440, 750))):
            sticky(cr, x, y, 0.3, 0.2 * math.sin(k), 6, tiny=True, seed=k)
    cr.restore()
    portrait(cr, t, A("b6", "Take"), 130, 300, 86, "teacher", mouth=mouth_of(tl, "teacher", t, "smile"),
             eyes="happy", bg=hexc("#cdb8ff"), end=A("b7") - 0.05)
    if nobody:
        stamp(cr, t, A("b7", "looked"), 360, 230, "NOBODY LOOKED", col=RED, size=62)
        cue("hit", t, A("b7", "looked"))
    vignette(cr, 0.4)


def scene_smile(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("b8") - 0.3, (1.3, 360, 560))]))
    person(cr, t, 360, 900, 1.0, "teacher", eyes="happy", mouth="grin", arms=("hips", "hips"))
    cr.restore()
    sign(cr, t, A("b8", "learned"), 360, 170, "ALREADY LEARNED IT", col=GREEN, size=54)
    sparkles(cr, t, A("b8", "learned"), 360, 520, n=10, seed=4, col=GOLD, spread=180)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b9", "cheating?"), 200, 480, "CHEATING", col=RED, size=54)
    sign(cr, t, A("b9", "smartest"), 520, 480, "GENIUS", col=GREEN, size=60)
    sticky(cr, 360, 700, 1.4, 0.08, 10, tiny=True)
    vignette(cr, 0.3)


SCENES = {"board": scene_board, "rule": scene_rule, "cheer": scene_cheer, "night": scene_night, "note": scene_note,
          "exam": scene_exam, "smile": scene_smile, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("SHE LET THEM", False), ("CHEAT", True)], end=tl.at("b2"), y=170, size=100)
    captions(cr, t, tl)
