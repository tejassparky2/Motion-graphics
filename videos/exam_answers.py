"""Episode 20: "The Last Bencher's Exam" — four technically-correct exam answers, and the teacher answers him back
the same way.

Answers: the Declaration of Independence was signed "at the bottom"; three apples in one hand and four in the other
means "very big hands"; a man can go eight days without sleep because "he sleeps at night"; you can drop an egg on a
concrete floor any way you like, because "concrete floors are really hard to crack". His grade: "a very big zero. At
the bottom." Then the teacher pins it up as the best paper of the year.
"""
import math

from motion.captions import captions
from motion.timeline import clear_dialogue
from motion.characters import person
from motion.engine import (INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, seg, shape,
                           sharp_shape, write)
from motion.kit import camera, enter_world, fly, hl, set_camera, stamp, whip
from videos.backbencher import CX, KID, KIDS, ROW, TEACH, TX, WIDE, classroom, desk

NARRATOR = dict(speed=1.0, max_pause=0.42)
TAIL = 0.9

SCRIPT = [
    dict(id="e1", scene="exam", text="Exam day. The last bencher finishes in [two minutes,|2 minutes,] and smiles."),
    dict(id="e2", scene="q1", text="Question one: where was the Declaration of Independence signed?"),
    dict(id="e3", scene="a1", text="His answer: at the bottom."),
    dict(id="e4", scene="q2",
         text="Question two: you have [three|3] apples in one hand, and [four|4] in the other. What do you have?"),
    dict(id="e5", scene="a2", text="Very big hands."),
    dict(id="e6", scene="q3", text="Question three: how can a man go [eight days|8 days] without sleep?"),
    dict(id="e7", scene="a3", text="Easy. He sleeps at night."),
    dict(id="e8", scene="q4", text="Question four: how do you drop an egg on a concrete floor without cracking it?"),
    dict(id="e9", scene="a4", text="Any way you like. Concrete floors are really hard to break."),
    dict(id="e10", scene="back", text="Next day, he gets his paper back. Sir, what did I get?", speaker="chotu",
         speaker_from="sir,"),
    dict(id="e11", scene="zero", text="A very big zero. At the bottom.", speaker="teacher"),
    dict(id="e12", scene="end", text="And then he pins it on the wall. Best paper of the year.", gap=0.2),
]
clear_dialogue(SCRIPT, ids={"e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11"})   # riddles and answers: slower, with clear turns

METADATA = dict(
    title="The Last Bencher's Exam Answers 😂 (Technically Correct)",
    alt_titles=["He Answered Every Question… Technically 😂", "4 Exam Answers That Are Technically Right 🤣"],
    description="""The last bencher finished the exam in 2 minutes… and every answer is technically correct. 😂

Q1: Where was the Declaration of Independence signed?
Q2: 3 apples in one hand, 4 in the other. What do you have?
Q3: How can a man go 8 days without sleep?
Q4: How do you drop an egg on concrete without cracking it?

Then the teacher grades it… the same way. 👀

💬 Which answer deserves full marks?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Riddles", "#LastBencher", "#Funny"],
    tags=["funny exam answers", "trick questions", "last bencher", "backbenchers", "teacher vs student", "technically correct",
          "school jokes", "riddles", "brain teaser", "classroom comedy", "interestingly strange"],
    pinned_comment="Be honest: which answer would YOU give full marks? 😂 1, 2, 3 or 4?",
)

PAPER = hexc("#fdfcf6")
RULE = hexc("#a9c8ec")
MARGIN = hexc("#f08a8a")
PENCIL = hexc("#4a4a52")
RED_PEN = hexc("#e02b2b")
BLUE = hexc("#3f6fb5")
GOLD = hexc("#f2b51d")
DESKWOOD = hexc("#c99a62")

QUESTIONS = {
    1: (["Where was the Declaration", "of Independence signed?"], "At the bottom."),
    2: (["You have 3 apples in one hand", "and 4 in the other.", "What do you have?"], "Very big hands."),
    3: (["How can a man go 8 days", "without sleep?"], "He sleeps at night."),
    4: (["How do you drop an egg", "on a concrete floor", "without cracking it?"], "Concrete is hard to break!"),
}


# ------------------------------------------------------------------ the exam room
def scene_exam(cr, t, tl):
    A = tl.at
    keys = [(0, (1.3, 400, 760)), (A("e1", "exam"), (1.0, 470, 760)), (A("e1", "day"), ROW),
            (A("e1", "bencher"), (1.9, 820, 740)), (A("e1", "finishes"), KID), (A("e1", "2"), (1.6, 470, 520)),
            (A("e1", "smiles"), (2.4, 830, 720))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t)
    done = A("e1", "finishes")
    # the clock races through two minutes
    if A("e1", "2") <= t < A("e1", "smiles") + 0.3:
        for k in range(2):
            a = (t - A("e1", "2")) * 30 + k
            line(cr, [(470, 470), (470 + 30 * math.sin(a), 470 - 30 * math.cos(a))], 3, RED, seed=7600 + k, amp=0.2)
    person(cr, "teacher", TX, 900, t, facing=1, arms=("hip", "hip"), eyes="sly", mouth="flat")
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hold", "hold"), eyes="closed", mouth="flat")
        y = 900
        if who == "chotu":
            if t >= done:
                k.update(arms=("chin", "face"), eyes="happy", mouth="grin", lean=-0.12)
            if t >= A("e1", "smiles"):
                k.update(eyes="happy", mouth="grin", arms=("cheer", "face"))
        else:
            k["shake"] = 0.6       # scribbling furiously
            k["sweat"] = i == 1
        person(cr, who, x, y, t, **k)
        desk(cr, x, 4200 + i * 10)
        # their exam papers
        px = x + 6
        sharp_shape(cr, [(px - 30, 790), (px + 30, 788), (px + 32, 798), (px - 28, 800)], WHITE, seed=7610 + i,
                    amp=0.3, lw=2)
        if who == "chotu" and t >= done:
            write(cr, [("DONE", RED)], px, 780, 18, align="center", bold=True)
    hl(cr, t, [("EXAM DAY", RED)], 215, 84, 0.0, end=A("e1", "bencher"), bold=True, sound=False)
    hl(cr, t, [("done in ", INK), ("2 MINUTES", RED)], 215, 66, A("e1", "2"), bold=True)
    cue("pop", t, done)


# ------------------------------------------------------------------ the exam paper
def paper_bg(cr, t, keys, q):
    cr.set_source_rgba(*DESKWOOD)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.14)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(-6, 16):   # desk grain
        line(cr, [(-600, k * 140), (1400, k * 140 + 30)], 3, hexc("#b0824f"), seed=7700 + k, amp=0.8)
    sharp_shape(cr, [(10, 150), (710, 140), (720, 1300), (20, 1310)], PAPER, seed=7710, amp=1.0, lw=4)
    for k in range(20):
        y = 250 + k * 56
        line(cr, [(14, y), (716, y - 2)], 2, RULE, seed=7720 + k, amp=0.3)
    line(cr, [(92, 145), (98, 1306)], 2.5, MARGIN, seed=7750, amp=0.3)
    write(cr, [(f"Q{q}.", RED_PEN)], 50, 340, 34, align="center", bold=True)


def declaration(cr, t, x, y):
    sharp_shape(cr, [(x - 150, y - 160), (x + 150, y - 165), (x + 155, y + 170), (x - 150, y + 175)],
                hexc("#efdcae"), seed=7800, amp=1.2, lw=3.5)
    write(cr, [("Declaration", INK)], x, y - 120, 30, align="center", bold=True)
    for k in range(6):
        line(cr, [(x - 120, y - 80 + k * 26), (x + 120, y - 80 + k * 26)], 2.5, hexc("#8a7a5a"), seed=7810 + k,
             amp=1.2)
    for k in range(5):   # the signatures, at the bottom
        sx, sy = x - 110 + (k % 3) * 100, y + 100 + (k // 3) * 36
        line(cr, [(sx, sy), (sx + 20, sy - 14), (sx + 34, sy + 4), (sx + 56, sy - 10), (sx + 70, sy)], 2.5, INK,
             seed=7820 + k, amp=0.8)


def apple(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 20, 18, hexc("#e53935"), seed=seed, amp=0.5, lw=3)
        line(cr, [(0, -16), (3, -28)], 3, hexc("#6d4524"), seed=seed + 1, amp=0.2)
        blob(cr, 10, -24, 8, 4, hexc("#79b061"), seed=seed + 2, amp=0.2, lw=2)


def hands(cr, t, x, y, s):
    """A little stick person holding 3 apples and 4 apples; `s` scales just the hands."""
    line(cr, [(x, y - 120), (x, y - 40)], 4, INK, seed=7900, amp=0.4)
    blob(cr, x, y - 140, 18, 18, None, seed=7901, amp=0.4, lw=4, stroke=INK)
    dot(cr, x - 6, y - 144, 2.5, INK)
    dot(cr, x + 6, y - 144, 2.5, INK)
    line(cr, [(x, y - 40), (x - 16, y)], 4, INK, seed=7902, amp=0.3)
    line(cr, [(x, y - 40), (x + 16, y)], 4, INK, seed=7903, amp=0.3)
    for side, n in ((-1, 3), (1, 4)):
        hx = x + side * (60 + 60 * s)
        hy = y - 100 - 10 * s
        line(cr, [(x, y - 100), (hx, hy)], 4, INK, seed=7904 + side, amp=0.3)
        with at(cr, hx, hy, s):
            blob(cr, 0, 0, 40, 30, hexc("#f0c29c"), seed=7910 + side, amp=0.6, lw=3.5)
            for k in range(n):
                apple(cr, -24 + (k % 2) * 30 + (k // 2) * 8, -30 - (k // 2) * 26, 0.7, seed=7920 + side * 10 + k)


def sleeper(cr, t, x, y, night):
    # bed, man in it, and a window showing the moon at night
    sharp_shape(cr, [(x - 170, y), (x + 170, y), (x + 170, y + 50), (x - 170, y + 50)], hexc("#8e5a2e"), seed=8000,
                amp=0.6, lw=3.5)
    line(cr, [(x - 170, y + 50), (x - 170, y + 90)], 6, INK, seed=8001, amp=0.2)
    line(cr, [(x + 170, y + 50), (x + 170, y + 90)], 6, INK, seed=8002, amp=0.2)
    blob(cr, x - 120, y - 16, 34, 18, WHITE, seed=8003, amp=0.5, lw=3)
    blob(cr, x - 110, y - 40, 24, 24, hexc("#f0c29c"), seed=8004, amp=0.4, lw=3)
    sharp_shape(cr, [(x - 90, y - 30), (x + 160, y - 30), (x + 170, y + 4), (x - 90, y + 4)], hexc("#4fb3e8"),
                seed=8005, amp=0.6, lw=3.5)
    if night:
        line(cr, [(x - 120, y - 42), (x - 104, y - 42)], 3, INK, seed=8006, amp=0.2)   # eyes closed
        for k in range(3):
            u = (t * 0.9 + k / 3) % 1
            write(cr, [("z", hexc("#3f6fb5", 1 - u))], x - 80 + u * 60 + k * 14, y - 70 - u * 80 - k * 20, 30 + k * 8,
                  bold=True)
    else:
        dot(cr, x - 118, y - 42, 3, INK)
        dot(cr, x - 104, y - 42, 3, INK)
    wx, wy = x + 40, y - 230
    sharp_shape(cr, [(wx - 80, wy - 70), (wx + 80, wy - 70), (wx + 80, wy + 70), (wx - 80, wy + 70)],
                hexc("#1f2a4d") if night else hexc("#bfe6ff"), seed=8010, amp=0.5, lw=4)
    if night:
        blob(cr, wx + 20, wy - 10, 30, 30, hexc("#ffe08a"), seed=8011, amp=0.4, lw=0, stroke=None)
        blob(cr, wx + 34, wy - 20, 26, 26, hexc("#1f2a4d"), seed=8012, amp=0.4, lw=0, stroke=None)
        for k in range(4):
            dot(cr, wx - 60 + k * 30, wy - 40 + (k % 2) * 60, 3, WHITE)
    else:
        blob(cr, wx + 20, wy - 10, 28, 28, hexc("#ffd23f"), seed=8013, amp=0.4, lw=3)


def egg_drop(cr, t, x, y, start, splat):
    sharp_shape(cr, [(x - 220, y), (x + 220, y), (x + 220, y + 70), (x - 220, y + 70)], hexc("#b9bcc2"), seed=8100,
                amp=0.5, lw=4)
    for k in range(6):
        dot(cr, x - 180 + k * 70, y + 30 + (k % 2) * 16, 3, hexc("#8a8d94"))
    write(cr, [("CONCRETE", hexc("#6b6e75"))], x, y + 52, 24, align="center", bold=True)
    if not splat:
        u = (math.sin(t * 3) + 1) / 2
        blob(cr, x, y - 250 - u * 20, 22, 30, WHITE, seed=8110, amp=0.3, lw=3.5)
        line(cr, [(x, y - 200), (x, y - 20)], 3, hexc("#8a8d94"), seed=8111, amp=0.2)
        line(cr, [(x - 14, y - 44), (x, y - 20), (x + 14, y - 44)], 3, hexc("#8a8d94"), seed=8112, amp=0.2)
        return
    u = seg(t, start, start + 0.25)
    if u < 1:
        blob(cr, x, lerp(y - 250, y - 26, u * u), 22, 30, WHITE, seed=8110, amp=0.3, lw=3.5)
    else:   # the egg cracks... the floor does not
        blob(cr, x, y - 8, 70, 14, WHITE, seed=8120, amp=1.2, lw=3)
        blob(cr, x + 6, y - 12, 18, 10, hexc("#ffc23d"), seed=8121, amp=0.5, lw=2.5)
        cue("thud", t, start + 0.25)


def scene_paper(cr, t, tl, q, answered):
    A = tl.at
    qb, ab = f"e{2 * q}", f"e{2 * q + 1}"
    lines, ans = QUESTIONS[q]
    ay = 320 + len(lines) * 58 + 50          # answer baseline
    dy = ay + 250                            # doodle centre
    if not answered:
        mid = {1: "independence", 2: "4", 3: "without", 4: "concrete"}[q]
        keys = [(A(qb) - 0.2, (1.3, 360, 430 + len(lines) * 30)), (A(qb, mid), (1.15, 360, 560)), (A(qb, mid, end=True) + 0.15,
                (1.6, 360, dy)), (A(qb, end=True) - 0.45, (1.1, 360, 600))]
        keys.append((A(qb) + 1.0, (1.6, 360, dy)))     # punch in on the doodle while the question is read
        if q == 4:
            keys.append((A(qb, "egg"), (1.6, 360, dy - 200)))
    else:
        keys = [(A(ab) - 0.2, (1.3, 360, ay - 30)), (A(ab) + 0.35, (1.1, 360, 620)),
                (A(ab, end=True) - 0.4, (1.45, 360, dy))]
        if A(ab, end=True) - A(ab) > 2.0:
            keys.append(((A(ab) + A(ab, end=True)) / 2, (1.7, 360, dy + 60)))
    paper_bg(cr, t, keys, q)
    # the typed question
    start = A(qb)
    for k, ln in enumerate(lines):
        if answered:
            write(cr, [(ln, INK)], 110, 330 + k * 58, 40, bold=True)
        else:
            write(cr, [(ln, INK)], 110, 330 + k * 58, 40, seg(t, start + k * 0.3, start + k * 0.3 + 0.3), bold=True)
    # doodles
    if q == 1:
        with at(cr, 360, dy, 0.8):
            declaration(cr, t, 0, 0)
        if answered and t >= A(ab, "bottom"):
            u = seg(t, A(ab, "bottom"), A(ab, "bottom") + 0.2)
            line(cr, [(600, dy - 90), (600 - 110 * u, dy - 90 + 170 * u)], 6, RED_PEN, seed=8200, amp=0.5)
            blob(cr, 360, dy + 95, 140, 40, None, seed=8201, amp=1.2, lw=5, stroke=RED_PEN)
            write(cr, [("HERE", RED_PEN)], 610, dy - 110, 40, align="center", bold=True)
            cue("hit", t, A(ab, "bottom"))
    elif q == 2:
        s = 1.0
        if answered:
            s = 1.0 + 1.0 * ease_out(seg(t, A(ab, "big"), A(ab, "hands")))
            cue("whoosh", t, A(ab, "big"))
        hands(cr, t, 360, dy + 120, s)
    elif q == 3:
        night = answered and t >= A(ab, "night")
        sleeper(cr, t, 360, dy + 110, night)
        if not answered and t >= A(qb, "8"):
            with at(cr, 150, dy - 110, max(0.85, pop(t, A(qb, "8"), 0.25)), rot=-0.1):
                sharp_shape(cr, [(-70, -50), (70, -50), (70, 50), (-70, 50)], WHITE, seed=8300, amp=0.5, lw=3)
                write(cr, [("8 DAYS", RED_PEN)], 0, 12, 34, align="center", bold=True)
        if night:
            cue("pop", t, A(ab, "night"))
    elif q == 4:
        egg_drop(cr, t, 360, dy + 100, A(ab, "hard") if answered else 0, answered and t >= A(ab, "concrete"))
        if answered and t >= A(ab, "break"):
            with at(cr, 360, dy - 60, max(0.85, pop(t, A(ab, "break"), 0.25)), rot=-0.05):
                write(cr, [("floor: fine", hexc("#2e9e52"))], 0, 0, 52, align="center", bold=True)
            cue("hit", t, A(ab, "break"))
    # the handwritten answer
    if answered:
        write(cr, [(ans, PENCIL)], 110, ay, 52, seg(t, A(ab) + 0.05, A(ab) + 0.5))
        cue("scribble", t, A(ab) + 0.05)
    if not answered:
        cue("scribble", t, start, 0.6)
    hl(cr, t, [(f"QUESTION {q}", RED)], 215, 70, A(qb), end=A(ab) - 0.05 if not answered else None, bold=True,
       sound=not answered)
    if answered:
        hl(cr, t, [("his answer:", INK)], 215, 70, A(ab), end=A(ab) + 0.6, bold=True)
        if q == 2:
            stamp(cr, t, A(ab, "hands"), "VERY BIG HANDS", dur=0.7, y=300)


# ------------------------------------------------------------------ results
def scene_back(cr, t, tl):
    A = tl.at
    keys = [(A("e10") - 0.1, (1.2, 470, 760)), (A("e10", "next"), (1.5, 300, 740)), (A("e10", "paper"), (1.5, 640, 760)),
            (A("e10", "back"), (1.9, 820, 740)), (A("e10", "sir,"), KID), (A("e10", "did"), (2.4, 825, 720))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t, day=2)
    person(cr, "teacher", TX, 900, t, facing=1, arms=("point", "hip") if t >= A("e10", "paper") else ("hold", "hip"),
           eyes="sly", mouth="smirk")
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        if who == "chotu":
            k.update(eyes="happy", mouth="grin", arms=("cheer", "hip") if t >= A("e10", "sir,") else ("hold", "hip"))
            if tl.speaking("chotu", t):
                k["mouth"] = "o" if int(t * 12) % 2 else "grin"
        person(cr, who, x, 900, t, **k)
        desk(cr, x, 4200 + i * 10)

    def sheet(x, y):
        with at(cr, x, y, 1.0, rot=t * 6):
            sharp_shape(cr, [(-30, -20), (30, -22), (32, 20), (-28, 22)], WHITE, seed=8400, amp=0.3, lw=2.5)
    fly(cr, t, A("e10", "paper"), 0.5, (TX + 40, 760), (CX + 6, 790), sheet, height=180)
    if t >= A("e10", "paper") + 0.5:
        sharp_shape(cr, [(CX - 24, 790), (CX + 36, 788), (CX + 38, 798), (CX - 22, 800)], WHITE, seed=8401, amp=0.3,
                    lw=2)
    hl(cr, t, [("NEXT DAY", RED), ("...", INK)], 215, 76, A("e10", "next"), end=A("e10", "sir,") - 0.05, bold=True)
    hl(cr, t, [("\"What did I get?\"", INK)], 215, 70, A("e10", "sir,"), bold=True)


def scene_zero(cr, t, tl):
    A = tl.at
    keys = [(A("e11") - 0.2, (0.9, 360, 700)), (A("e11", "very"), (1.0, 360, 760)), (A("e11", "zero"), (1.15, 360, 900)),
            (A("e11", "bottom"), (1.4, 360, 1000))]
    cr.set_source_rgba(*DESKWOOD)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.14)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    sharp_shape(cr, [(10, 150), (710, 140), (720, 1300), (20, 1310)], PAPER, seed=7710, amp=1.0, lw=4)
    for k in range(20):
        line(cr, [(14, 250 + k * 56), (716, 248 + k * 56)], 2, RULE, seed=7720 + k, amp=0.3)
    line(cr, [(92, 145), (98, 1306)], 2.5, MARGIN, seed=7750, amp=0.3)
    write(cr, [("EXAM", INK)], 400, 220, 40, align="center", bold=True)
    for q in range(1, 5):   # the four answers, each crossed out in red
        y = 250 + q * 150
        write(cr, [(f"Q{q}.", RED_PEN)], 50, y, 30, align="center", bold=True)
        write(cr, [(QUESTIONS[q][1], PENCIL)], 110, y, 40)
        x0 = A("e11") + (q - 1) * 0.12
        if t >= x0:
            line(cr, [(500, y - 50), (600, y + 10)], 7, RED_PEN, seed=8500 + q, amp=0.4)
            line(cr, [(600, y - 50), (500, y + 10)], 7, RED_PEN, seed=8510 + q, amp=0.4)
            cue("pop", t, x0)
    if t >= A("e11", "zero"):   # a very big zero, at the bottom
        k = seg(t, A("e11", "zero"), A("e11", "zero") + 0.3)
        cr.save()
        cr.translate(360, 1110)
        cr.scale(1.0, 1.25)
        cr.arc(0, 0, 150, -math.pi / 2, -math.pi / 2 + 2 * math.pi * k)
        cr.restore()
        cr.set_source_rgba(*RED_PEN)
        cr.set_line_width(26)
        cr.stroke()
        cue("hit", t, A("e11", "zero"))
    hl(cr, t, [("\"A ", INK), ("VERY BIG", RED), (" zero.\"", INK)], 215, 70, A("e11", "very"),
       end=A("e11", "bottom") - 0.05, bold=True)
    hl(cr, t, [("\"At the ", INK), ("BOTTOM", RED), (".\"", INK)], 215, 80, A("e11", "bottom"), bold=True,
       underline=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("e12") - 0.1, (1.5, 300, 740)), (A("e12", "pins"), (2.0, 700, 470)), (A("e12", "wall"), (1.4, 560, 600)),
            (A("e12", "best"), (2.4, 720, 420)), (A("e12", "year"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t, day=2)
    pin = A("e12", "pins")
    # the paper on the wall, with a gold star
    if t >= pin:
        with at(cr, 710, 400, max(0.85, pop(t, pin, 0.25)), rot=-0.05):
            sharp_shape(cr, [(-70, -90), (70, -92), (72, 90), (-68, 92)], PAPER, seed=8600, amp=0.5, lw=3)
            for k in range(5):
                line(cr, [(-60, -50 + k * 22), (60, -50 + k * 22)], 2, RULE, seed=8601 + k, amp=0.2)
            cr.save()
            cr.translate(0, 50)
            cr.scale(1.0, 1.25)
            cr.arc(0, 0, 28, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(*RED_PEN)
            cr.set_line_width(7)
            cr.stroke()
            dot(cr, 0, -88, 7, RED)
        cue("thud", t, pin)
    if t >= A("e12", "best"):
        with at(cr, 775, 320, max(0.85, pop(t, A("e12", "best"), 0.3)), rot=0.2 + 0.1 * math.sin(t * 4)):
            pts = []
            for k in range(10):
                r = 44 if k % 2 == 0 else 20
                a = -math.pi / 2 + k * math.pi / 5
                pts.append((r * math.cos(a), r * math.sin(a)))
            sharp_shape(cr, pts, GOLD, seed=8620, amp=0.3, lw=3.5)
        cue("kaching", t, A("e12", "best"))
    person(cr, "teacher", TX if t < pin else 600, 900, t, facing=1 if t < pin else -1,
           arms=("point", "hip") if t < A("e12", "best") else ("thumb", "hip"), eyes="happy", mouth="grin")
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        if t >= A("e12", "year"):
            k.update(eyes="happy", mouth="grin", arms=("cheer", "hip"), jump=abs(math.sin(t * 9 + i)) * 8)
        if who == "chotu":
            k.update(eyes="happy", mouth="grin", arms=("cheer", "hip"))
        person(cr, who, x, 900, t, **k)
        desk(cr, x, 4200 + i * 10)
    hl(cr, t, [("pinned on the ", INK), ("WALL", BLUE)], 215, 66, A("e12", "pins"), end=A("e12", "best") - 0.05,
       bold=True)
    hl(cr, t, [("BEST PAPER", RED), (" of the year", INK)], 215, 62, A("e12", "best"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name[0] in "qa" and name[1:].isdigit():
        scene_paper(cr, t, tl, int(name[1:]), name[0] == "a")
    elif name == "back":
        scene_back(cr, t, tl)
    elif name == "zero":
        scene_zero(cr, t, tl)
    elif name == "end":
        scene_end(cr, t, tl)
    else:
        scene_exam(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
