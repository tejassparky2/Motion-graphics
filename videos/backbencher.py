"""Episode 7: "The Backbencher vs The Teacher" — follows the channel's reference beats, retold in our own words.

The kid in the last row asks three trick riddles (survivors on the border, ten mangoes, the parachute), the teacher gets
his revenge with a riddle of his own, and the last row sits empty for two weeks.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 1.0

SCRIPT = [
    dict(id="c1", scene="class", text="A kid in the last row raises his hand, and asks the teacher:"),
    dict(id="c2", scene="border",
         text="Sir, if a plane crashes right on the border of the US and Canada, where do they bury the survivors?",
         speaker="chotu"),
    dict(id="c3", scene="class", text="The teacher thinks, and says: in their own country, I guess?", speaker="teacher",
         speaker_from="their"),
    dict(id="c4", scene="class", text="No sir! Why would you bury survivors? They're alive!", speaker="chotu"),
    dict(id="c5", scene="class", text="The whole class loses it."),
    dict(id="c6", scene="mango",
         text="Sir, a man has [ten|10] mangoes. He gives [three|3] to his sister, [two|2] to his brother, "
              "and [four|4] to his friend. What's he left with?", speaker="chotu"),
    dict(id="c7", scene="class", text="The teacher shoots back: [one!|1!]", speaker="teacher", speaker_from="1!"),
    dict(id="c8", scene="class", text="No sir. [Three|3] enemies. Nobody got the same amount.", speaker="chotu"),
    dict(id="c9", scene="plane", text="Sir, a man jumps out of a plane with no parachute, and survives. How?",
         speaker="chotu"),
    dict(id="c10", scene="class", text="The teacher says: that's impossible.", speaker="teacher", speaker_from="that's"),
    dict(id="c11", scene="plane2", text="No sir. The plane was parked on the runway.", speaker="chotu"),
    dict(id="c12", scene="class", text="Now the teacher's face is red. He says: my turn.", speaker="teacher",
         speaker_from="my"),
    dict(id="c13", scene="count",
         text="[Thirty|30] kids in a class. One of them never stops talking. If he gets suspended for "
              "[two weeks,|2 weeks,] what's left?", speaker="teacher"),
    dict(id="c14", scene="class", text="The kid goes: [twenty-nine?|29?]", speaker="chotu", speaker_from="29?"),
    dict(id="c15", scene="class", text="No. Peace and quiet.", speaker="teacher", gap=0.2),
    dict(id="c16", scene="end", text="And for the next two weeks, the last row was totally empty.", gap=0.2),
]

METADATA = dict(
    title="The Last Row Kid vs The Teacher 😂 (Trick Riddles)",
    alt_titles=["Never Challenge the Backbencher… Or Should You? 😂", "3 Trick Riddles That Broke the Teacher 🤣"],
    description="""The kid in the last row raises his hand… and the teacher instantly regrets it. 😂

Riddle 1: A plane crashes right on the US–Canada border. Where do they bury the survivors?
Riddle 2: A man has 10 mangoes and gives away 3, 2 and 4. What's he left with?
Riddle 3: A man jumps out of a plane with no parachute and survives. How?

Then the teacher gets his revenge. 👀

💬 How many did you get right? Drop your best trick riddle below 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Riddles", "#Backbencher", "#Funny"],
    tags=["riddles", "trick questions", "backbenchers", "teacher vs student", "funny riddles", "school jokes",
          "brain teaser", "riddle challenge", "classroom comedy", "interestingly strange"],
    pinned_comment="Be honest: how many of the 3 riddles did you get? 😂 Drop a harder one for the teacher 👇",
)

WALL = hexc("#8fc7bd")
FLOOR = hexc("#c99a62")
BOARD = hexc("#2f5b46")
FRAME = hexc("#8e5a2e")
CHALK = hexc("#f4f1e6")
CHALK_Y = hexc("#f7d774")
CHALK_P = hexc("#f5a3b5")
CHALK_B = hexc("#9fd3f0")
MANGO = hexc("#f6a531")
GREEN = hexc("#3d8f45")
TX = 120                                                  # teacher
KIDS = (("kid_a", 330), ("kid_b", 490), ("kid_c", 650), ("chotu", 830))
CX = 830                                                  # the backbencher

WIDE = (0.85, 470, 770)
TEACH = (1.75, 150, 745)
KID = (2.0, 805, 745)
ROW = (1.2, 600, 770)


def laughing(t, tl):
    A = tl.at
    return (A("c4", "alive") <= t < A("c6") or A("c8", "enemies") <= t < A("c9")
            or A("c12") <= t < A("c12", "my"))


# ------------------------------------------------------------------ classroom
def classroom(cr, t, day=None):
    cr.set_source_rgba(*WALL)
    cr.paint()
    for k in range(-4, 16):   # wall panels
        line(cr, [(k * 90, 250), (k * 90, 900)], 2.5, hexc("#7db6ab"), seed=4000 + k, amp=0.6)
    sharp_shape(cr, [(-800, 900), (1800, 890), (1800, 1900), (-800, 1900)], FLOOR, seed=4001, amp=1, lw=4)
    for k in range(-6, 22):   # floor boards
        line(cr, [(k * 80, 900), (k * 80 - 60, 1400)], 2.5, hexc("#b0824f"), seed=4002 + k, amp=0.5)
    # blackboard with leftover lessons
    shape(cr, rrect_pts(-190, 400, 440, 260, 8, 20), FRAME, seed=4030, amp=0.8, lw=4)
    shape(cr, rrect_pts(-176, 414, 412, 232, 6, 20), BOARD, seed=4031, amp=0.6, lw=3)
    write(cr, [("2 + 2 = 4", CHALK)], -150, 480, 36)
    write(cr, [("ABC", CHALK_Y)], 110, 480, 36)
    line(cr, [(-150, 540), (-60, 520), (20, 560), (100, 530)], 3, CHALK_B, seed=4032, amp=1.2)
    write(cr, [("no talking!", CHALK_P)], -150, 610, 32)
    shape(cr, rrect_pts(-150, 660, 110, 12, 3, 12), FRAME, seed=4033, amp=0.4, lw=2.5)   # chalk tray
    # clock
    blob(cr, 470, 470, 44, 44, WHITE, seed=4040, amp=0.6, lw=4)
    ang = t * 0.9
    line(cr, [(470, 470), (470 + 26 * math.sin(ang), 470 - 26 * math.cos(ang))], 3.5, INK, seed=4041, amp=0.2)
    line(cr, [(470, 470), (470 + 16 * math.sin(ang / 12), 470 - 16 * math.cos(ang / 12))], 4.5, INK, seed=4042, amp=0.2)
    # window
    shape(cr, rrect_pts(880, 380, 200, 200, 8, 20), hexc("#bfe6ff"), seed=4050, amp=0.8, lw=4)
    line(cr, [(980, 380), (980, 580)], 4, INK, seed=4051, amp=0.3)
    line(cr, [(880, 480), (1080, 480)], 4, INK, seed=4052, amp=0.3)
    blob(cr, 930, 430, 30, 14, WHITE, seed=4053, amp=0.8, lw=0, stroke=None)
    # calendar (counts the two empty weeks at the end)
    shape(cr, rrect_pts(620, 540, 110, 120, 6, 16), WHITE, seed=4060, amp=0.6, lw=3.5)
    shape(cr, rrect_pts(620, 540, 110, 30, 6, 16), RED, seed=4061, amp=0.5, lw=3)
    write(cr, [("DAY", INK)], 675, 600, 24, align="center", bold=True)
    write(cr, [(str(day or 1), RED)], 675, 648, 44, align="center", bold=True)


def desk(cr, x, seed):
    for dx in (-52, 52):
        line(cr, [(x + dx, 830), (x + dx, 898)], 6, hexc("#6d4524"), seed=seed + dx, amp=0.4)
    shape(cr, rrect_pts(x - 72, 796, 144, 20, 5, 16), hexc("#d9a15a"), seed=seed, amp=0.6, lw=3.5)
    shape(cr, rrect_pts(x - 60, 816, 120, 44, 5, 16), hexc("#b98040"), seed=seed + 1, amp=0.6, lw=3)


def red_face(cr, t, amount):
    """Teacher turns red and steams."""
    if amount <= 0:
        return
    hx, hy = TX + 6, 900 - 162
    blob(cr, hx, hy, 34, 30, hexc("#e53935", 0.4 * amount), seed=4100, amp=0.5, lw=0, stroke=None)
    for k in range(3):
        u = (t * 1.4 + k / 3) % 1
        blob(cr, hx - 30 + k * 30, hy - 50 - u * 60, 12 + u * 8, 10 + u * 6, hexc("#ffffff", 0.8 * (1 - u) * amount),
             seed=4110 + k, amp=0.8, lw=0, stroke=None)


def scene_class(cr, t, tl):
    A = tl.at
    keys = [(0, (1.5, 700, 760)), (A("c1", "row"), (1.8, 780, 750)), (A("c1", "raises"), KID), (A("c1", "hand"), (2.4, 830, 700)), (A("c1", "asks"), ROW), (A("c1", "teacher"), TEACH),
            (A("c3") - 0.15, TEACH), (A("c3", "their"), (2.1, 130, 740)), (A("c4") - 0.1, KID), (A("c4", "bury"), (2.3, 130, 740)), (A("c4", "they're"), KID), (A("c4", "alive"), (2.3, 820, 720)),
            (A("c5"), WIDE), (A("c5", "loses"), ROW),
            (A("c7") - 0.15, (1.6, 180, 760)), (A("c7", "1!"), (2.2, 130, 740)), (A("c8") - 0.1, KID),
            (A("c8", "enemies"), (2.1, 820, 730)), (A("c8", "nobody"), ROW),
            (A("c10") - 0.15, TEACH), (A("c10", "impossible"), (2.2, 130, 740)),
            (A("c12") - 0.15, ROW), (A("c12", "red"), (2.2, 130, 740)), (A("c12", "my"), (1.8, 200, 760)),
            (A("c14") - 0.15, KID), (A("c14", "29?"), (2.1, 820, 730)), (A("c15"), TEACH),
            (A("c15", "peace"), (1.4, 300, 760))]
    z, fx, fy = camera(t, keys)
    if t < A("c1", "raises"):
        z += 0.1 * seg(t, 0, A("c1", "raises"))
    set_camera((z, fx, fy))
    enter_world(cr)
    classroom(cr, t)
    lol = laughing(t, tl)
    # ---- teacher
    s = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    if t < A("c1", "asks"):
        s.update(facing=-1, arms=("point", "hip"))           # writing on the board
    if A("c3") <= t < A("c3", "their"):
        s.update(arms=("chin", "hip"), eyes="sly", mouth="flat")
    if A("c4") <= t < A("c7"):
        s.update(eyes="wide", mouth="o", sweat=True, shake=1.0 if t >= A("c4", "alive") else 0)
    if A("c7") <= t < A("c8"):
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
    if A("c8") <= t < A("c10"):
        s.update(eyes="wide", mouth="wobble", sweat=True)
    if A("c10") <= t < A("c12"):
        s.update(arms=("hip", "hip"), eyes="sly", mouth="smirk")
    red = 0.0
    if A("c12") <= t < A("c14"):
        red = seg(t, A("c12", "red") - 0.2, A("c12", "red") + 0.2)
        s.update(eyes="sly", mouth="flat", shake=1.5 if t < A("c12", "my") else 0,
                 arms=("point", "hip") if t >= A("c12", "my") else ("hip", "hip"))
    if A("c14") <= t:
        s.update(eyes="sly", mouth="smirk", arms=("point", "hip"))
    if t >= A("c15", "peace"):
        s.update(eyes="happy", mouth="grin", arms=("cheer", "hip"))
    if tl.speaking("teacher", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "teacher", TX, 900, t, **s)
    red_face(cr, t, red)
    # ---- kids (the backbencher stands up for his riddles)
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if lol:
            k.update(eyes="closed", mouth="laugh", jump=abs(math.sin(t * 9 + i)) * 8)
        if who == "chotu":
            stand = seg(t, A("c1", "raises") - 0.1, A("c1", "raises") + 0.15)
            y -= 36 * stand
            if A("c1", "raises") <= t < A("c3"):
                k.update(arms=("cheer", "hip"), eyes="sly", mouth="smirk")
            if A("c4") <= t < A("c5"):
                k.update(arms=("cheer", "hip") if t >= A("c4", "alive") else ("point", "hip"), eyes="happy", mouth="grin")
            if A("c8") <= t < A("c8", "enemies"):
                k.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
            if A("c10") <= t < A("c12"):
                k.update(eyes="sly", mouth="smirk")
            if A("c14") <= t:
                k.update(arms=("chin", "hip"), eyes="dot", mouth="flat")
            if t >= A("c15", "peace"):
                k.update(eyes="wide", mouth="o", sweat=True, arms=("down", "down"), shake=1.2)
            if tl.speaking("chotu", t):
                k["mouth"] = "o" if int(t * 12) % 2 else "smirk"
        person(cr, who, x, y, t, **k)
        desk(cr, x, 4200 + i * 10)
    # ---- screen text
    hl(cr, t, [("LAST ROW", RED), (" vs ", INK), ("TEACHER", hexc("#3f6fb5"))], 215, 58, 0.0, end=A("c1", "teacher"),
       bold=True, sound=False)
    hl(cr, t, [("\"In their own country?\"", INK)], 215, 56, A("c3", "their"), end=A("c4") - 0.05, bold=True)
    hl(cr, t, [("They're ", INK), ("ALIVE!", RED)], 215, 78, A("c4", "alive"), end=A("c6") - 0.05, bold=True)
    hl(cr, t, [("\"ONE!\"", hexc("#3f6fb5"))], 215, 90, A("c7", "1!"), end=A("c8") - 0.05, bold=True)
    hl(cr, t, [("nobody got the ", INK), ("same", RED)], 330, 52, A("c8", "nobody"), end=A("c9") - 0.05, bold=True)
    stamp(cr, t, A("c8", "enemies"), "3 ENEMIES", dur=0.8, y=230)
    hl(cr, t, [("\"IMPOSSIBLE.\"", hexc("#3f6fb5"))], 215, 76, A("c10", "impossible"), end=A("c11") - 0.05, bold=True)
    hl(cr, t, [("\"MY TURN.\"", RED)], 215, 90, A("c12", "my"), end=A("c13") - 0.05, bold=True)
    hl(cr, t, [("\"29?\"", INK)], 215, 90, A("c14", "29?"), end=A("c15") - 0.05, bold=True)
    stamp(cr, t, A("c15", "peace"), "PEACE & QUIET", dur=0.9, y=230)
    for w in (A("c4", "alive"), A("c8", "enemies"), A("c15", "peace")):
        cue("hit", t, w)


# ------------------------------------------------------------------ chalkboard scenes
def board(cr, t, keys):
    cr.set_source_rgba(*FRAME)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.14)   # punch-ins, not slow eases
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    shape(cr, rrect_pts(-500, -300, 1720, 1880, 10, 40), BOARD, seed=4300, amp=1.0, lw=5)
    cr.set_line_width(22)
    for k in range(9):   # old eraser smudges, so camera moves read on screen
        cr.set_source_rgba(1, 1, 1, 0.05)
        x0, y0 = -300 + (k * 263) % 1300, -100 + (k * 397) % 1500
        cr.move_to(x0, y0)
        cr.curve_to(x0 + 80, y0 - 40, x0 + 160, y0 + 40, x0 + 260, y0)
        cr.stroke()


def chalk_plane(cr, x, y, s=1.0, rot=0.0, wheels=False):
    with at(cr, x, y, s, rot=rot):
        blob(cr, 0, 0, 110, 26, None, seed=4400, amp=0.8, lw=4.5, stroke=CHALK)
        line(cr, [(-20, -6), (30, -70), (60, -70), (40, -6)], 4.5, CHALK, seed=4401, amp=0.6)   # wing
        line(cr, [(-90, -10), (-120, -60), (-100, -60), (-70, -18)], 4.5, CHALK, seed=4402, amp=0.6)   # tail
        for k in range(4):
            blob(cr, 70 - k * 34, -6, 7, 7, None, seed=4403 + k, amp=0.3, lw=3, stroke=CHALK_B)
        line(cr, [(-20, 26), (-30, 34), (-10, 34)], 3.5, CHALK, seed=4410, amp=0.4)
        if wheels:
            for wx in (-60, 60):
                line(cr, [(wx, 24), (wx, 40)], 4, CHALK, seed=4411 + wx, amp=0.2)
                blob(cr, wx, 48, 10, 10, None, seed=4413 + wx, amp=0.3, lw=4, stroke=CHALK)


def stick(cr, x, y, s=1.0, arms_up=False, smile=True, seed=0, col=CHALK):
    with at(cr, x, y, s):
        blob(cr, 0, -70, 14, 14, None, seed=seed, amp=0.5, lw=4, stroke=col)
        line(cr, [(0, -56), (0, -22)], 4, col, seed=seed + 1, amp=0.4)
        line(cr, [(0, -22), (-12, 0)], 4, col, seed=seed + 2, amp=0.4)
        line(cr, [(0, -22), (12, 0)], 4, col, seed=seed + 3, amp=0.4)
        ay = -70 if arms_up else -30
        line(cr, [(-18, ay), (0, -46), (18, ay)], 4, col, seed=seed + 4, amp=0.4)
        if smile:
            line(cr, [(-6, -68), (0, -64), (6, -68)], 2.5, col, seed=seed + 5, amp=0.2)


def big_q(cr, t, start, x, y, size=150):
    sc = pop(t, start, 0.3)
    if sc > 0:
        with at(cr, x, y, sc, rot=0.12 * math.sin(t * 5)):
            write(cr, [("?", CHALK_Y)], 0, size * 0.35, size, align="center", bold=True)
        cue("pop", t, start)


def scene_border(cr, t, tl):
    A = tl.at
    crash = A("c2", "crashes", end=True)
    keys = [(A("c2") - 0.2, (1.6, 360, 700)), (A("c2", "plane"), (1.0, 480, 520)), (A("c2", "crashes"), (1.5, 380, 820)), (A("c2", "border"), (1.1, 360, 640)),
            (A("c2", "US"), (1.3, 220, 560)), (A("c2", "Canada"), (1.3, 500, 560)), (A("c2", "where"), (2.0, 370, 860)),
            (A("c2", "bury"), (1.2, 300, 800)), (A("c2", "survivors"), (1.6, 420, 930))]
    board(cr, t, keys)
    if A("c2", "crashes") <= t < crash + 0.35:
        cr.translate(math.sin(t * 70) * 8, math.cos(t * 55) * 6)
    # the border
    cr.set_dash([22, 16])
    line(cr, [(360, 380), (360, 1000)], 6, CHALK, seed=4500, amp=0.6)
    cr.set_dash([])
    for key, x0, col in (("US", -500, hexc("#4fb3e8", 0.35)), ("Canada", 360, hexc("#e0487a", 0.4))):
        u = seg(t, A("c2", key), A("c2", key) + 0.08)
        if u > 0:
            cr.rectangle(x0, -300, 860 * u if x0 < 0 else 860 * u, 1880)
            cr.set_source_rgba(*col)
            cr.fill()
    if t >= A("c2", "US"):
        write(cr, [("USA", CHALK_B)], 220, 470, 76, align="center", bold=True)
    if t >= A("c2", "Canada"):
        write(cr, [("CANADA", CHALK_P)], 510, 470, 64, align="center", bold=True)
    # the plane dives in and lands on the line
    u = ease_out(seg(t, A("c2", "plane"), crash))
    if t >= A("c2", "plane"):
        chalk_plane(cr, lerp(700, 380, u), lerp(260, 860, u), 1.0, rot=lerp(0.55, 0.15, u))
    if t >= crash:
        k = seg(t, crash, crash + 0.3)
        for i in range(6):
            a = i * math.pi / 3
            blob(cr, 360 + math.cos(a) * 70 * k, 880 + math.sin(a) * 40 * k, 34 * k + 1, 26 * k + 1, None,
                 seed=4510 + i, amp=1.2, lw=4, stroke=CHALK)
        cue("thud", t, crash - 0.15)
        fl = 1 - seg(t, crash, crash + 0.25)
        if fl > 0:
            cr.save()
            cr.identity_matrix()
            cr.set_source_rgba(1, 1, 1, 0.7 * fl)
            cr.paint()
            cr.restore()
    # three survivors pop up, waving
    for i, x in enumerate((250, 470, 560)):
        sc = pop(t, A("c2", "survivors") + i * 0.08, 0.25)
        if sc > 0:
            with at(cr, x, 1000, sc):
                stick(cr, 0, 0, 1.1, arms_up=int(t * 6 + i) % 2 == 0, seed=4520 + i * 10, col=CHALK_Y)
    if t >= A("c2", "bury"):   # a shovel doodle
        with at(cr, 150, 900, pop(t, A("c2", "bury"), 0.25), rot=-0.4):
            line(cr, [(0, -120), (0, 20)], 5, CHALK, seed=4540, amp=0.4)
            shape(cr, [(-24, 20), (24, 20), (0, 70)], None, seed=4541, amp=0.6, lw=4.5, stroke=CHALK)
    big_q(cr, t, A("c2", "survivors", end=True), 610, 830)
    hl(cr, t, [("plane crash on the ", INK), ("border", RED)], 215, 54, A("c2", "crashes"), end=A("c2", "where") - 0.05,
       bold=True)
    hl(cr, t, [("bury the ", INK), ("SURVIVORS", RED), ("?", INK)], 215, 64, A("c2", "bury"), bold=True)


MANGO_POS = [(160 + (k % 5) * 100, 640 + (k // 5) * 110) for k in range(10)]
GROUPS = ((range(0, 3), "three", 150, "sister", CHALK_P), (range(3, 5), "two", 360, "brother", CHALK_B),
          (range(5, 9), "four", 570, "friend", CHALK_Y))


def mango(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s, rot=0.3):
        blob(cr, 0, 0, 34, 26, MANGO, seed=seed, amp=0.8, lw=3.5)
        blob(cr, 10, -8, 8, 5, hexc("#ffd27a"), seed=seed + 1, amp=0.3, lw=0, stroke=None)
        shape(cr, [(-22, -20), (-40, -38), (-18, -32)], hexc("#79b061"), seed=seed + 2, amp=0.4, lw=2.5)


def scene_mango(cr, t, tl):
    A = tl.at
    keys = [(A("c6") - 0.2, (1.1, 360, 700)), (A("c6", "man"), (2.0, 90, 700)), (A("c6", "10"), (1.0, 360, 690)), (A("c6", "mangoes"), (1.6, 360, 700)),
            (A("c6", "3"), (1.3, 300, 760)), (A("c6", "sister"), (1.7, 150, 960)), (A("c6", "2"), (1.3, 380, 760)),
            (A("c6", "brother"), (1.7, 360, 960)), (A("c6", "4"), (1.3, 470, 760)), (A("c6", "friend"), (1.7, 570, 960)),
            (A("c6", "left"), (2.0, 560, 740))]
    board(cr, t, keys)
    sc = pop(t, A("c6", "man"), 0.25)
    if sc > 0:
        with at(cr, 60, 780, sc):
            stick(cr, 0, 0, 2.0, arms_up=t < A("c6", "3"), seed=4650, col=CHALK_Y)
    for rng, word, gx, who, col in GROUPS:
        sc = pop(t, A("c6", who), 0.25)
        if sc > 0:
            with at(cr, gx, 1210, sc):
                stick(cr, 0, 0, 1.0, arms_up=True, seed=4660 + gx, col=col)
    for k, (x, y) in enumerate(MANGO_POS):
        sc = pop(t, A("c6", "10") + k * 0.03, 0.2)
        if sc <= 0:
            continue
        for rng, word, gx, _, _ in GROUPS:
            if k in rng:   # hop down to whoever gets it
                j = k - rng.start
                u = ease_out(seg(t, A("c6", word) + j * 0.05, A("c6", word) + j * 0.05 + 0.35))
                x = lerp(x, gx - 45 + (j % 2) * 90, u)
                y = lerp(y, 900 + (j // 2) * 70, u) - math.sin(u * math.pi) * 80
        wob = 0.08 * math.sin(t * 8) if k == 9 and t >= A("c6", "left") else 0
        with at(cr, x, y, sc, rot=wob):
            mango(cr, 0, 0, 1.0, seed=4600 + k * 3)
    for rng, word, gx, who, col in GROUPS:
        if t >= A("c6", word):
            write(cr, [("-" + {"three": "3", "two": "2", "four": "4"}[word], col)], gx, 1080, 56, align="center", bold=True)
            write(cr, [(who, col)], gx, 1130, 38, align="center")
            cue("pop", t, A("c6", word))
    big_q(cr, t, A("c6", "left"), 640, 600, 120)
    hl(cr, t, [("10", RED), (" mangoes", INK)], 215, 78, A("c6", "10"), end=A("c6", "left") - 0.05, bold=True)
    hl(cr, t, [("what's ", INK), ("left", RED), ("?", INK)], 215, 78, A("c6", "left"), bold=True)


def scene_plane(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("c9") - 0.2, (1.0, 360, 600)), (A("c9", "man"), (1.8, 300, 560)), (A("c9", "jumps"), (2.0, 330, 640)),
                (A("c9", "plane"), (1.2, 360, 700)), (A("c9", "parachute"), (1.8, 560, 800)),
                (A("c9", "survives"), (1.8, 330, 960)), (A("c9", "how"), (1.1, 420, 740))]
    else:
        keys = [(A("c11") - 0.2, (2.2, 330, 780)), (A("c11", "plane"), (1.5, 360, 800)), (A("c11", "parked"), (0.95, 360, 760)),
                (A("c11", "runway"), (0.9, 360, 820))]
    board(cr, t, keys)
    if part == 1:
        chalk_plane(cr, 360 + math.sin(t * 2) * 10, 520, 1.6)
        drop = seg(t, A("c9", "jumps"), A("c9", "survives"))
        if t >= A("c9", "jumps"):
            stick(cr, 330, 600 + ease_out(drop) * 380, 1.1, arms_up=True, smile=t >= A("c9", "survives"), seed=4700,
                  col=CHALK_Y)
        sc = pop(t, A("c9", "parachute"), 0.25)
        if sc > 0:   # a crossed-out parachute
            with at(cr, 560, 820, sc):
                shape(cr, [(-60, 0), (-30, -44), (30, -44), (60, 0)], None, seed=4710, amp=0.8, lw=4.5, stroke=CHALK)
                for dx in (-60, 0, 60):
                    line(cr, [(dx, 0), (0, 60)], 3, CHALK, seed=4711 + dx, amp=0.3)
                line(cr, [(-80, -60), (80, 80)], 8, hexc("#ff6b6b"), seed=4720, amp=0.5)
                line(cr, [(80, -60), (-80, 80)], 8, hexc("#ff6b6b"), seed=4721, amp=0.5)
        if t >= A("c9", "survives"):
            write(cr, [("ALIVE", CHALK_Y)], 330, 1060, 44, align="center", bold=True)
        big_q(cr, t, A("c9", "how"), 560, 560, 140)
        hl(cr, t, [("no ", INK), ("parachute", RED)], 215, 70, A("c9", "parachute"), end=A("c9", "how") - 0.05, bold=True)
        hl(cr, t, [("...and ", INK), ("survives", GREEN), ("?!", INK)], 215, 70, A("c9", "survives"), bold=True)
    else:
        chalk_plane(cr, 360, 820, 1.6, wheels=True)
        line(cr, [(-400, 902), (1200, 902)], 6, CHALK, seed=4730, amp=0.8)   # the ground was right there
        cr.set_dash([40, 30])
        line(cr, [(-400, 950), (1200, 950)], 5, CHALK_Y, seed=4731, amp=0.4)
        cr.set_dash([])
        stick(cr, 250, 902, 1.1, arms_up=True, seed=4700, col=CHALK_Y)
        if t >= A("c11", "runway"):
            write(cr, [("RUNWAY", CHALK_Y)], 360, 1040, 70, align="center", bold=True)
        if t >= A("c11", "parked"):
            write(cr, [("P", CHALK_B)], 610, 700, 90, align="center", bold=True)
            blob(cr, 610, 670, 52, 52, None, seed=4740, amp=0.6, lw=4.5, stroke=CHALK_B)
            cue("hit", t, A("c11", "parked"))
        hl(cr, t, [("It was ", INK), ("PARKED", RED)], 215, 82, A("c11", "parked"), bold=True, underline=True)


def scene_count(cr, t, tl):
    """30 chalk faces; the chatterbox gets erased."""
    A = tl.at
    tx, ty = 4 * 104 + 100, 3 * 104 + 520     # the talker's seat
    keys = [(A("c13") - 0.2, (1.0, 360, 700)), (A("c13", "kids"), (1.4, 360, 640)), (A("c13", "one"), (1.8, tx, ty)), (A("c13", "talking"), (2.6, tx + 20, ty - 10)),
            (A("c13", "suspended"), (1.3, tx - 60, ty)),
            (A("c13", "left"), (1.0, 360, 720))]
    board(cr, t, keys)
    gone = seg(t, A("c13", "suspended"), A("c13", "suspended") + 0.4)
    for k in range(30):
        r, c = divmod(k, 6)
        x, y = 100 + c * 104, 520 + r * 104
        sc = pop(t, A("c13") + k * 0.02, 0.2)
        if sc <= 0:
            continue
        talker = (r, c) == (3, 4)
        if talker and gone >= 1:
            continue
        with at(cr, x, y, sc):
            if talker:
                cr.push_group()
            blob(cr, 0, 0, 34, 34, None, seed=4800 + k, amp=0.6, lw=4, stroke=CHALK_P if talker else CHALK)
            dot(cr, -10, -6, 4, CHALK)
            dot(cr, 10, -6, 4, CHALK)
            if talker:
                blob(cr, 0, 14, 10, 6 + 5 * abs(math.sin(t * 14)), None, seed=4850, amp=0.3, lw=3, stroke=CHALK)
                if t >= A("c13", "talking"):
                    write(cr, [("blah blah", CHALK_Y)], 36, -40, 26, bold=True)
                cr.pop_group_to_source()
                cr.paint_with_alpha(1 - gone)
            else:
                line(cr, [(-10, 12), (0, 16), (10, 12)], 3, CHALK, seed=4860 + k, amp=0.2)
    if A("c13", "one") <= t < A("c13", "suspended") + 0.3:
        blob(cr, tx, ty, 54, 54, None, seed=4870, amp=1.0, lw=5, stroke=hexc("#ff6b6b"))
    big_q(cr, t, A("c13", "left"), 360, 1150, 130)
    hl(cr, t, [("30", RED), (" kids", INK)], 215, 78, A("c13", "30"), end=A("c13", "suspended") - 0.05, bold=True)
    stamp(cr, t, A("c13", "suspended"), "SUSPENDED", dur=0.7, y=330)
    hl(cr, t, [("2 weeks", RED), (" - what's left?", INK)], 215, 60, A("c13", "2 weeks"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("c16") - 0.2, (1.1, 560, 760)), (A("c16", "two"), (1.5, 680, 680)), (A("c16", "last"), (1.7, 820, 760)),
            (A("c16", "empty"), (1.6, 780, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    day = 1 + int(13 * seg(t, A("c16", "two"), A("c16", "row")))
    classroom(cr, t, day=day)
    person(cr, "teacher", TX, 900, t, facing=1, arms=("cheer", "hip"), eyes="closed", mouth="grin")
    for i, (who, x) in enumerate(KIDS):
        if who != "chotu":
            person(cr, who, x, 900, t, facing=-1, eyes="closed" if i == 1 else "dot", mouth="smile")
        desk(cr, x, 4200 + i * 10)
    if t >= A("c16", "empty"):   # crickets
        write(cr, [("chirp... chirp...", INK)], CX, 720, 34, align="center", bold=True)
    for k in range(3):   # the teacher humming
        u = (t * 0.8 + k / 3) % 1
        write(cr, [("~", hexc("#3f6fb5", 1 - u))], TX + 50 + k * 18, 700 - u * 80, 40, bold=True)
    hl(cr, t, [("2 WEEKS", RED), (" later...", INK)], 215, 70, A("c16", "two"), end=A("c16", "empty") - 0.05, bold=True)
    hl(cr, t, [("totally ", INK), ("EMPTY", RED)], 215, 82, A("c16", "empty"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "border":
        scene_border(cr, t, tl)
    elif name == "mango":
        scene_mango(cr, t, tl)
    elif name == "plane":
        scene_plane(cr, t, tl, 1)
    elif name == "plane2":
        scene_plane(cr, t, tl, 2)
    elif name == "count":
        scene_count(cr, t, tl)
    elif name == "end":
        scene_end(cr, t, tl)
    else:
        scene_class(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
