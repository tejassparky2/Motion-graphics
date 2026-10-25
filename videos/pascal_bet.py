"""Big question: "A Bet You Can't Lose?" -- the maths teacher draws Pascal's Wager on the board and the Last Bencher
breaks it with one question ("Sir, which God?"), in the polished look.

Script: out/scripts_big_questions_batch2.md, video 4 (owner approved 25 Oct 2026). Blaise Pascal, Pensées (published
1670), the wager; Denis Diderot, Pensées philosophiques (1746), section 59: "an imam could reason just as well", the
"many gods" objection. "4,000+" is the commonly cited estimate of the number of religions, shown as an estimate.
Turbo stock female narrator with tags; Sir and the kid through Turbo with Kokoro reference voices.
"""
import math
import random

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, shake, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter, lin,
                           paint, rrect, sign, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from videos.bq_kit import mouth_of, talker
from videos.last_bencher_4 import CHALK, chalk, classroom, room

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "w6"          # music drops out on "Sir, which God?" (research 18 Oct 2026, A5)
SERIES = "The Last Bencher"
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "sir": dict(voice="am_michael", speed=1.0, turbo_ref="am_michael")})
CELLS = {"bg": (360, 300), "bn": (545, 300), "dg": (360, 455), "dn": (545, 455)}   # believe/don't x god/no god

SCRIPT = [
    dict(id="w1", scene="board", text="The maths teacher draws a bet on the board. Believe in God, or don't."),
    dict(id="w2", scene="board", text="Believe and you're right, you win heaven. Believe and you're wrong, you lose "
                                      "almost nothing.", speaker="sir"),
    dict(id="w3", scene="board", text="But if you don't believe, and God is real, you lose everything. So believing "
                                      "is the smart bet.", speaker="sir"),
    dict(id="w4", scene="pascal", text="This is Pascal's Wager, from [sixteen seventy.|1670.] The whole class agrees."),
    dict(id="w5", scene="except", text="Everyone but the last bencher."),
    dict(id="w6", scene="which", text="Sir, which God?", speaker="kid", gap=0.4),
    dict(id="w7", scene="boxes", text="There are thousands of religions. Many say believing in the wrong one won't "
                                      "save you."),
    dict(id="w8", scene="boxes", text="So the bet isn't two boxes. It's thousands. And you can only pick one."),
    dict(id="w9", scene="diderot", text="The French writer Denis Diderot made this same point in [seventeen forty "
                                        "six.|1746.]"),
    dict(id="w10", scene="books", text="Then you'd better start studying all of them. [chuckle]", speaker="sir"),
    dict(id="w11", scene="end", text="So, is Pascal's bet still smart, or did one question break it?", gap=0.3),
]
clear_dialogue(SCRIPT, ids={"w6"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="A Bet You Can't Lose? 1 Question Broke It 🎲",
    alt_titles=["Believing Is a Free Bet... Or Is It? 🎲", "Pascal's Wager in 40 Seconds 🎲"],
    description="""The maths teacher draws a bet on the board: believe in God, or don't. Believe and you're right, you win heaven. Believe and you're wrong, you lose almost nothing. But if you don't believe, and God is real, you lose everything. So believing is the smart bet. 🎲

This is Pascal's Wager (Pensées, 1670). The whole class agrees. Everyone but the Last Bencher: "Sir, which God?"

There are thousands of religions, and many say believing in the wrong one won't save you. So the bet isn't two boxes, it's thousands, and you can only pick one. Denis Diderot made this same point in 1746 (Pensées philosophiques, §59).

Sources: Blaise Pascal, Pensées (1670); Denis Diderot, Pensées philosophiques (1746). "4,000+" is the commonly cited estimate of the number of religions.

💬 Is Pascal's bet still smart, or did one question break it? Keep it respectful 🙏 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending questions, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#Philosophy", "#Shorts"],
    tags=["pascal's wager", "which god", "many gods objection", "diderot", "is believing a safe bet",
          "the last bencher", "philosophy", "teacher vs student", "deep questions", "interestingly strange"],
    pinned_comment="STILL SMART or BROKEN? One reason, keep it respectful 🙏 👇",
)


def sir(cr, t, tl, x, y, s, **kw):
    talker(cr, t, tl, "sir", "sir", x, y, s, rest=kw.pop("rest", "smile"), **kw)


def grid(cr, t, start, fill=()):
    """The wager table in chalk; `fill` = [(cell, text, colour, start)]."""
    u = seg(t, start, start + 0.8)
    if u <= 0:
        return
    for p in ([(250, 230), (250 + 390 * u, 230)], [(80, 380), (80 + 560 * u, 380)],
              [(270, 160), (270, 160 + 370 * u)], [(455, 160), (455, 160 + 370 * u)]):
        stroke_line(cr, p, 5, CHALK, curve=False)
    if u >= 1:
        for txt, x, y in (("GOD", 362, 210), ("NO GOD", 547, 210), ("BELIEVE", 168, 318), ("DON'T", 168, 470)):
            bold_text(cr, txt, x, y, 30, CHALK, outline=None, shadow=0)
    for cell, txt, col, st in fill:
        if t < st:
            continue
        x, y = CELLS[cell]
        k = appear(t, st, 0.3)
        cr.save()
        cr.translate(x, y)
        cr.scale(k, k)
        lines = txt.split("\n")
        for j, ln in enumerate(lines):
            bold_text(cr, ln, 0, (j - (len(lines) - 1) / 2) * 34 + 10, 28, col, outline=None, shadow=0)
        cr.restore()
        if k < 1:
            cue("scribble", t, st, 0.3)


def table_fill(A):
    return [("bg", "WIN\nEVERYTHING", hexc("#9fffb0"), A("w2", "heaven")),
            ("bn", "LOSE A\nLITTLE", CHALK, A("w2", "nothing")),
            ("dg", "LOSE\nEVERYTHING", hexc("#ff8a8a"), A("w3", "everything")),
            ("dn", "SAVE A\nLITTLE", alpha(CHALK, 0.6), A("w3", "everything") + 0.3)]


# ---------------------------------------------------------------- scenes
def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    grid(cr, t, 0.0, table_fill(A))
    if t >= A("w3", "smart"):
        ellipse(cr, CELLS["bg"][0], CELLS["bg"][1], 92, 58)
        paint(cr, None, hexc("#ffd84d"), 6)
    sir(cr, t, tl, 120, 1190, 0.9, eyes="open", arms=("point", "down"), look=(0.6, -0.5))
    vignette(cr, 0.4)


def scene_pascal(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.05, 360, 640))]))
    classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross"), eyes="half", mouth="flat"), look_at=(200, 300))
    cr.restore()
    card(cr, t, tl.scene_at(t)[1], 360, 220, 420, 170, "PASCAL'S WAGER", ["1670"], col=BLUE, title_size=40,
         line_size=50)
    if t >= A("w4", "agrees"):
        tag(cr, t, A("w4", "agrees"), 360, 360, "EVERYONE AGREES", col=GREEN, size=42)
    vignette(cr, 0.4)


def scene_except(cr, t, tl):
    room(cr, t)
    s0 = tl.scene_at(t)[1]
    cr.save()
    enter(cr, camera(t, [(s0, (1.0, 360, 640)), (s0 + 0.35, (2.0, 555, 470))], dur=0.3))
    classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross"), eyes="half", mouth="smug", brows="raise"),
              look_at=(200, 300))
    cr.restore()
    vignette(cr, 0.45)


def scene_which(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    grid(cr, t, -1, table_fill(A))
    hit = A("w6", "God")
    cr.save()
    if t >= hit:
        dx, dy = shake(t, hit, 0.3, 6)
        cr.translate(dx, dy)
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.4, 220, 760))]))
    frozen = t >= hit
    sir(cr, t, None, 200, 1130, 1.0, eyes="wide" if frozen else "open", mouth="o" if frozen else "smile",
        brows="up" if frozen else None, arms=("front", "down"), sweat=frozen, look=(0.5, -0.2))
    if frozen:                                                    # the chalk falls out of his hand
        u = seg(t, hit, hit + 0.6)
        rrect(cr, 280, lerp(800, 1100, u * u), 34, 12, 4)
        paint(cr, WHITE, OUTLINE, 3)
    cr.restore()
    if frozen:
        stamp(cr, t, hit, 360, 230, "WHICH GOD?", col=RED, size=80)
    vignette(cr, 0.45)


def scene_boxes(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1e2638"), hexc("#3a3060"), seed=71)
    s0 = tl.scene_at(t)[1]
    u = seg(t, s0, s0 + 1.6)
    rng = random.Random(9)
    cols = [GREEN, BLUE, PURPLE, GOLD, RED, hexc("#ff8ab0"), hexc("#5af0ff")]
    n = int(lerp(2, 320, u * u))
    for k in range(n):                                            # two boxes become hundreds
        ang, dist = rng.uniform(0, 2 * math.pi), rng.uniform(0, 1) ** 0.6
        x = 360 + math.cos(ang) * dist * 330 * u if k >= 2 else 280 + 160 * k
        y = 600 + math.sin(ang) * dist * 380 * u if k >= 2 else 600
        sz = 70 if k < 2 else 18 + 10 * rng.random()
        rrect(cr, x - sz / 2, y - sz / 2, sz, sz, 4)
        paint(cr, alpha(cols[k % len(cols)], 0.9), OUTLINE, 2.5 if k >= 2 else 5)
    if t >= A("w8"):
        counter(cr, t, A("w8", "thousands"), 360, 300, 4000, size=130, dur=0.9, col=GOLD, suffix="+",
                sub="RELIGIONS (ESTIMATE)")
    if t >= A("w8", "pick"):
        sign(cr, t, A("w8", "pick"), 360, 1000 - 120, "PICK ONLY ONE", col=RED, size=54)
    vignette(cr, 0.4)


def scene_diderot(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=72)
    s0 = tl.scene_at(t)[1]
    card(cr, t, s0, 360, 420, 480, 260, "DENIS DIDEROT · 1746", ["SAME BET WORKS", "FOR ANY RELIGION"], col=PURPLE,
         title_size=34, line_size=40)
    tag(cr, t, s0 + 0.3, 360, 650, "76 YEARS AFTER PASCAL", col=GOLD, size=40)
    vignette(cr, 0.3)


def books(cr, x, y, n, s=1.0):
    cols = [hexc("#e8473f"), hexc("#4aa3f0"), hexc("#3fbf6a"), hexc("#ffcf3f"), hexc("#7a5bd0")]
    for k in range(n):
        rrect(cr, x - 80 * s + (k % 3 - 1) * 6 * s, y - (k + 1) * 26 * s, 160 * s, 26 * s, 4)
        paint(cr, cols[k % len(cols)], OUTLINE, 3)


def scene_books(cr, t, tl):
    A = tl.at
    room(cr, t)
    drop = A("w10", "studying")
    u = seg(t, drop - 0.2, drop + 0.25)
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (2.0, 555, 470))]))
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "up") if u >= 1 else ("cross", "cross"),
                                       eyes="wide" if u >= 1 else "half", mouth="o" if u >= 1 else "smug"),
              look_at=(200, 300))
    books(cr, 560, lerp(150, 560, u * u), 12, 0.56)
    cr.restore()
    if u >= 1:
        cue("thud", t, drop + 0.25, 0.3)
        tag(cr, t, drop + 0.25, 360, 230, "HOMEWORK: ALL OF THEM", col=PURPLE, size=44)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    grid(cr, t, -1, table_fill(A))
    for k in range(40):                                           # the table now cracks into many boxes
        x, y = 90 + (k % 8) * 70, 170 + (k // 8) * 70
        rrect(cr, x, y, 50, 50, 4)
        paint(cr, alpha(WHITE, 0.08), alpha(CHALK, 0.25), 2)
    sign(cr, t, A("w11", "smart"), 360, 640, "STILL SMART, OR BROKEN?", col=GOLD, size=46)
    buttons(cr, t, A("w11", "smart"), [("STILL SMART", GREEN), ("BROKEN", RED)], y=780, size=46)
    vignette(cr, 0.35)


SCENES = {"board": scene_board, "pascal": scene_pascal, "except": scene_except, "which": scene_which,
          "boxes": scene_boxes, "diderot": scene_diderot, "books": scene_books, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("A BET YOU", False), ("CAN'T LOSE?", True)], end=tl.at("w2"), y=600, size=80)
    captions(cr, t, tl)
