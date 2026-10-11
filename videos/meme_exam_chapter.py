"""Meme M3: "Teacher: Chapter seven won't come in the exam." / "The exam:" -- every question is chapter 7, and the
kid's soul leaves his body. ~8 s loop.

Original meme in our own characters (owner picked M1, M3, M6 on 11 Oct 2026). No narrator: a top caption bar, one
line from the teacher, our own sound hits. The last frame cuts back to the first, so it loops.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.meme import class_wall, exam_paper, meme_bar, soul
from motion.pkit import red_x
from motion.polish import OUTLINE, appear, captions, stroke_line, vignette
from motion.toons import head, person
from videos.last_bencher_4 import chalk, desk

NARRATOR = dict(speed=0.92)
TAIL = 0.15
voice.SPEAKERS.update({"teacher": dict(voice="af_bella", speed=1.0)})

SCRIPT = [
    dict(id="e1", scene="board", text="Chapter seven won't come in the exam.", speaker="teacher"),
    dict(id="e2", scene="board", text="", hold=0.5),
    dict(id="e3", scene="exam", text="", hold=1.0),
    dict(id="e4", scene="paper", text="", hold=2.0),
    dict(id="e5", scene="soul", text="", hold=2.2),
]

METADATA = dict(
    title="Teacher: This Won't Come in the Exam. The Exam: 💀",
    alt_titles=["Chapter 7 Won't Come in the Exam… 💀", "When the Teacher Says 'Skip Chapter 7' 😭"],
    description="""Teacher: Chapter 7 won't come in the exam. 😌
The exam: 💀

Tag the friend who skipped it too 😭👇

🔔 Interestingly Strange: strange stories, school memes, mind-bending paradoxes and weird history, animated.""",
    hashtags=["#Memes", "#ExamMemes", "#Shorts"],
    tags=["exam memes", "school memes", "teacher memes", "this won't come in the exam", "relatable",
          "student life", "funny shorts", "animated memes", "interestingly strange"],
    pinned_comment="Which chapter did YOUR teacher lie about? 😭👇",
)


def scene_board(cr, t, tl):
    A = tl.at
    class_wall(cr)
    chalk(cr, t, 0.0, 120, 380, "CH. 7", 110, dur=0.4)
    x_t = A("e1", "won't")
    if t >= x_t:                     # the teacher crosses it out
        u = ease_out(seg(t, x_t, x_t + 0.35))
        stroke_line(cr, [(110, 280), (lerp(110, 470, u), lerp(280, 420, u))], 14, (0.95, 0.3, 0.3, 1), curve=False)
        if u > 0.5:
            v = (u - 0.5) * 2
            stroke_line(cr, [(470, 280), (lerp(470, 110, v), lerp(280, 420, v))], 14, (0.95, 0.3, 0.3, 1),
                        curve=False)
    talk = tl.speaking("teacher", t)
    person(cr, t, 560, 1000, 0.95, "teacher", eyes="happy", mouth="talk" if talk else "smile",
           arms=("point", "hips"), facing=-1)
    relieved = t >= A("e1", "exam.")
    person(cr, t, 180, 1070, 0.8, "kid", eyes="happy" if relieved else "open", mouth="grin" if relieved else "smile",
           arms=("up", "up") if relieved else ("front", "front"))
    desk(cr, 180, 1020, 220, 0.9)
    meme_bar(cr, t, 0.0, ["Teacher:"])
    vignette(cr, 0.3)


def scene_exam(cr, t, tl):
    A = tl.at
    s0 = A("e3")
    class_wall(cr)
    person(cr, t, 360, 1070, 1.0, "kid", eyes="happy", mouth="grin", arms=("hips", "hips"))
    desk(cr, 360, 1010, 320, 1.0)
    u = ease_out(seg(t, s0, s0 + 0.25))
    exam_paper(cr, 360, lerp(-400, 930, u), 0.42, rot=-0.06 * (1 - u))
    cue("thud", t, s0 + 0.25)
    meme_bar(cr, t, s0, ["The exam:"])
    vignette(cr, 0.35)


def scene_paper(cr, t, tl):
    A = tl.at
    s0 = A("e4")
    class_wall(cr)
    qs = ["Q1. (Chapter 7)", "Q2. (Chapter 7)", "Q3. (Chapter 7)", "Q4. (Chapter 7)", "BONUS: Chapter 7"]
    rows = []
    for k, q in enumerate(qs):
        st = s0 + 0.1 + 0.32 * k
        rows.append((q, appear(t, st, 0.2) if t >= st else 0.0))
        cue("hit" if k == len(qs) - 1 else "pop", t, st)
    k = 1 + 0.08 * ease_out(seg(t, s0, s0 + 2.0))
    exam_paper(cr, 360, 620, 1.0 * k, rows=rows)
    late = t >= s0 + 1.0
    head(cr, t, 600, 1070, 95, "kid", eyes="wide" if late else "open", mouth="o" if late else "smile",
         brows="up" if late else None, sweat=late)
    meme_bar(cr, t, s0 - 0.24, ["The exam:"])
    vignette(cr, 0.35)


def scene_soul(cr, t, tl):
    A = tl.at
    s0 = A("e5")
    class_wall(cr)
    u = seg(t, s0 + 0.3, s0 + 1.8)
    person(cr, t, 360, 1070, 1.0, "kid", eyes="x" if u > 0 else "wide", mouth="o", tilt=0.25 * ease_out(u),
           arms=("down", "down"))
    desk(cr, 360, 1010, 320, 1.0)
    exam_paper(cr, 360, 940, 0.35, rot=0.1, rows=[("Ch. 7", 1.0)])
    soul(cr, t, 360, 1070, 1.0, u)
    cue("fall", t, s0 + 0.3, 1.2)
    meme_bar(cr, t, s0, ["Me:"])
    vignette(cr, 0.4)


SCENES = {"board": scene_board, "exam": scene_exam, "paper": scene_paper, "soul": scene_soul}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
