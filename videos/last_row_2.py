"""Episode 18: "The Last Bencher Is Back" — a sequel to The Backbencher, with new trick riddles.

Riddles: what you can hold in your left hand but never in your right (your right elbow), how many months have 28 days
(all twelve), which way a rooster's egg rolls off a roof (roosters don't lay eggs). The teacher hits back with "what
goes up but never comes down" (your age) and fifty pages of homework, and the kid hands in fifty pages of new riddles.
"""
import math

from motion.captions import captions
from motion.timeline import clear_dialogue
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, seg, shape, sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import (CHALK, CHALK_B, CHALK_P, CHALK_Y, CX, KID, KIDS, ROW, TEACH, TX, WIDE, big_q, board,
                                classroom, desk, red_face)

NARRATOR = dict(speed=1.0, max_pause=0.42)
TAIL = 0.9

SCRIPT = [
    dict(id="r1", scene="class", text="The last bencher in class is back. And this time, the teacher is ready."),
    dict(id="r2", scene="class", text="The teacher says: no riddles today.", speaker="teacher", speaker_from="no"),
    dict(id="r3", scene="elbow",
         text="Sir, just one. What can you hold in your left hand, but never in your right?", speaker="chotu"),
    dict(id="r4", scene="class", text="The teacher thinks. Is it a pen? Or a phone?", speaker="teacher", speaker_from="is"),
    dict(id="r5", scene="elbow2", text="No sir. Your right elbow. Go on, try it.", speaker="chotu"),
    dict(id="r6", scene="class", text="And the teacher actually tries. In front of everyone."),
    dict(id="r7", scene="months", text="Sir, how many months have [twenty-eight|28] days?", speaker="chotu"),
    dict(id="r8", scene="class", text="Easy. Just one. February.", speaker="teacher"),
    dict(id="r9", scene="months2",
         text="No sir. All [twelve|12] of them. They all have [twenty-eight|28] days. Some just keep going.", speaker="chotu"),
    dict(id="r10", scene="rooster",
         text="Last one. A rooster lays an egg on a roof. Which side does it roll down?", speaker="chotu"),
    dict(id="r11", scene="class", text="The steeper side, obviously!", speaker="teacher"),
    dict(id="r12", scene="rooster2", text="Sir, roosters don't lay eggs.", speaker="chotu"),
    dict(id="r13", scene="class", text="The class loses it. And the teacher's face goes red."),
    dict(id="r14", scene="up", text="Okay. My turn. What goes up, but never comes down?", speaker="teacher"),
    dict(id="r15", scene="class", text="Your blood pressure, sir?", speaker="chotu"),
    dict(id="r16", scene="class", text="Wrong. It's your age. And your homework: [fifty pages.|50 pages.]", speaker="teacher",
         gap=0.2),
    dict(id="r17", scene="end", text="Next day, the kid hands in [fifty pages.|50 pages.] Of brand new riddles.",
         gap=0.2),
]
clear_dialogue(SCRIPT)   # riddles and answers: slower, with clear turns

METADATA = dict(
    title="The Last Bencher Is BACK 😂 (Trick Riddles Part 2)",
    alt_titles=["The Last Bencher Strikes Again 😂", "The Teacher Said NO Riddles… 😂", "3 Trick Riddles That Broke the Teacher Again 🤣"],
    description="""The last bencher is back… and the teacher said NO riddles today. 😂

Riddle 1: What can you hold in your left hand, but never in your right?
Riddle 2: How many months have 28 days?
Riddle 3: A rooster lays an egg on a roof. Which side does it roll down?

Then the teacher strikes back. 👀

💬 How many did you get? Try the elbow one right now, we know you will 😂

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Riddles", "#LastBencher", "#Funny"],
    tags=["riddles", "trick questions", "last bencher", "backbenchers", "teacher vs student", "funny riddles", "school jokes",
          "brain teaser", "riddle challenge", "classroom comedy", "trick riddles part 2", "interestingly strange"],
    pinned_comment="Be honest: did you just try to grab your right elbow? 😂 Drop a riddle for Part 3 👇",
)

BLUE = hexc("#3f6fb5")
GREEN = hexc("#3d8f45")
RED_CHALK = hexc("#ff6b6b")


def laughing(t, tl):
    A = tl.at
    return (A("r6", "tries") <= t < A("r7") or A("r13") <= t < A("r13", "face")
            or A("r15", "pressure") <= t < A("r16"))


# ------------------------------------------------------------------ classroom
def scene_class(cr, t, tl):
    A = tl.at
    keys = [(0, (1.6, 760, 750)), (A("r1", "bencher"), (2.0, 815, 740)), (A("r1", "back"), KID),
            (A("r1", "time"), WIDE), (A("r1", "teacher"), (1.7, 170, 760)), (A("r1", "ready"), (2.2, 130, 730)),
            (A("r2") - 0.1, TEACH), (A("r2", "riddles"), (2.2, 140, 735)), (A("r2", "today"), (1.6, 300, 760)),
            (A("r4") - 0.1, TEACH), (A("r4", "thinks"), (2.2, 130, 740)), (A("r4", "pen"), (1.9, 160, 750)),
            (A("r4", "phone"), (2.3, 130, 730)),
            (A("r6") - 0.1, (1.5, 220, 770)), (A("r6", "tries"), (2.0, 140, 760)), (A("r6", "front"), ROW),
            (A("r6", "everyone"), WIDE),
            (A("r8") - 0.1, TEACH), (A("r8", "one"), (2.2, 130, 735)), (A("r8", "february"), (1.8, 170, 750)),
            (A("r11") - 0.1, TEACH), (A("r11", "side"), (2.2, 130, 735)), (A("r11", "obviously"), (1.8, 180, 750)),
            (A("r13") - 0.1, WIDE), (A("r13", "loses"), ROW), (A("r13", "teacher's"), TEACH),
            (A("r13", "red"), (2.4, 130, 730)),
            (A("r15") - 0.1, KID), (A("r15", "blood"), (2.3, 825, 720)), (A("r15", "pressure"), WIDE),
            (A("r15", "pressure") + 0.5, (2.4, 130, 730)),
            (A("r16") - 0.1, TEACH), (A("r16", "age"), (2.2, 130, 735)), (A("r16", "homework"), (1.6, 300, 760)),
            (A("r16", "50"), KID)]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    classroom(cr, t)
    lol = laughing(t, tl)
    # ---- teacher
    s = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    if t < A("r1", "ready"):
        s.update(facing=-1, arms=("point", "hip"))           # writing on the board
    elif t < A("r4"):
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
    if A("r4") <= t < A("r6"):
        s.update(arms=("chin", "hip"), eyes="sly", mouth="flat")
    spin = 0.0
    if A("r6", "tries") <= t < A("r7"):
        spin = 1.0          # chasing his own elbow
        s.update(facing=1 if int(t * 7) % 2 else -1, arms=("rub", "face"), eyes="wide", mouth="wobble", sweat=True,
                 shake=1.0)
    if A("r8") <= t < A("r9"):
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
    if A("r11") <= t < A("r12"):
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
    red = 0.0
    if A("r13") <= t < A("r16"):
        s.update(eyes="wide", mouth="wobble", sweat=True)
        red = seg(t, A("r13", "red") - 0.2, A("r13", "red") + 0.2)
        if t >= A("r15"):
            s.update(eyes="sly", mouth="flat", shake=1.5 if t >= A("r15", "pressure") else 0)
            red = 1.0
    if A("r16") <= t:
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
        if t >= A("r16", "homework"):
            s.update(eyes="happy", mouth="grin", arms=("cheer", "hip"))
    if tl.speaking("teacher", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "teacher", TX, 900, t, **s)
    red_face(cr, t, red)
    if spin:
        for k in range(3):   # spin swooshes
            a = t * 9 + k * 2.1
            cr.save()
            cr.translate(TX, 800)
            cr.scale(1.0, 0.35)
            cr.arc(0, 0, 90 + k * 14, a, a + 1.6)
            cr.restore()
            cr.set_source_rgba(*INK)
            cr.set_line_width(4)
            cr.stroke()
    # ---- kids (the last bencher stands for his riddles)
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if lol:
            k.update(eyes="closed", mouth="laugh", jump=abs(math.sin(t * 9 + i)) * 8)
        if A("r6", "front") <= t < A("r7") and who != "chotu":
            k.update(arms=("point", "hip"))
        if who == "chotu":
            stand = seg(t, A("r1", "back") - 0.1, A("r1", "back") + 0.15)
            y -= 36 * stand
            if A("r1", "back") <= t < A("r1", "time"):
                k.update(arms=("wave", "hip"), eyes="happy", mouth="grin")
            if A("r2") <= t < A("r4"):
                k.update(arms=("cheer", "hip"), eyes="sly", mouth="smirk")
            if A("r4") <= t < A("r6"):
                k.update(eyes="sly", mouth="smirk")
            if A("r8") <= t < A("r9") or A("r11") <= t < A("r12"):
                k.update(eyes="sly", mouth="smirk", arms=("chin", "hip"))
            if A("r15") <= t < A("r15", "pressure"):
                k.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
            if t >= A("r16", "homework"):
                k.update(eyes="wide", mouth="o", sweat=True, arms=("face", "down"), shake=1.2, jump=0)
            if tl.speaking("chotu", t):
                k["mouth"] = "o" if int(t * 12) % 2 else "smirk"
        person(cr, who, x, y, t, **k)
        desk(cr, x, 4200 + i * 10)
    # ---- screen text
    hl(cr, t, [("THE LAST BENCHER", RED), (" IS BACK", INK)], 215, 52, 0.0, end=A("r1", "teacher"), bold=True,
       sound=False)
    hl(cr, t, [("and the teacher is ", INK), ("READY", BLUE)], 215, 60, A("r1", "ready"), end=A("r2", "riddles") - 0.25,
       bold=True)
    hl(cr, t, [("\"NO RIDDLES", BLUE), (" today.\"", INK)], 215, 62, A("r2", "riddles"), end=A("r3") - 0.05,
       bold=True)
    hl(cr, t, [("\"A pen? Or a phone?\"", INK)], 215, 60, A("r4", "pen"), end=A("r5") - 0.05, bold=True)
    hl(cr, t, [("he actually ", INK), ("TRIES", RED)], 215, 72, A("r6", "tries"), end=A("r7") - 0.05, bold=True)
    hl(cr, t, [("\"ONE. ", BLUE), ("February.\"", INK)], 215, 70, A("r8", "one"), end=A("r9") - 0.05, bold=True)
    hl(cr, t, [("\"The ", INK), ("STEEPER", BLUE), (" side!\"", INK)], 215, 64, A("r11", "steeper"),
       end=A("r12") - 0.05, bold=True)
    hl(cr, t, [("face goes ", INK), ("RED", RED)], 215, 80, A("r13", "face"), end=A("r14") - 0.05, bold=True)
    hl(cr, t, [("\"Your ", INK), ("blood pressure", RED), (", sir?\"", INK)], 215, 52, A("r15", "blood"),
       end=A("r16") - 0.05, bold=True)
    hl(cr, t, [("\"Your ", INK), ("AGE", BLUE), (".\"", INK)], 215, 84, A("r16", "age"), end=A("r16", "homework"),
       bold=True)
    stamp(cr, t, A("r16", "50"), "50 PAGES", dur=0.8, y=230)
    for w in (A("r6", "tries"), A("r13", "loses"), A("r15", "pressure"), A("r16", "50")):
        cue("hit", t, w)


# ------------------------------------------------------------------ chalk scenes
def stick_big(cr, t, x, y, s, left=None, right=None, smile=True, col=CHALK):
    """Front-facing chalk figure. `left`/`right` are hand positions for the figure's own left (viewer's right) and
    right (viewer's left) hands, relative to the figure; None = hanging down."""
    with at(cr, x, y, s):
        blob(cr, 0, -230, 40, 40, None, seed=5000, amp=0.6, lw=5, stroke=col)
        for dx in (-14, 14):
            blob(cr, dx, -236, 4, 4, col, seed=5001 + dx, amp=0.2, lw=0, stroke=None)
        if smile:
            line(cr, [(-14, -218), (0, -210), (14, -218)], 4, col, seed=5003, amp=0.3)
        else:
            blob(cr, 0, -214, 8, 6, None, seed=5004, amp=0.3, lw=3.5, stroke=col)
        line(cr, [(0, -190), (0, -60)], 5, col, seed=5005, amp=0.5)
        line(cr, [(0, -60), (-40, 0)], 5, col, seed=5006, amp=0.5)
        line(cr, [(0, -60), (40, 0)], 5, col, seed=5007, amp=0.5)
        for side, hand in ((-1, right), (1, left)):
            sh = (side * 10, -170)
            if hand is None:
                el, hd = (side * 60, -130), (side * 70, -70)
            else:
                hd = hand
                el = (side * 70, -120)
            line(cr, [sh, el, hd], 5, col, seed=5010 + side, amp=0.5)
            blob(cr, hd[0], hd[1], 9, 9, None, seed=5020 + side, amp=0.3, lw=4, stroke=col)


def scene_elbow(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("r3") - 0.2, (1.0, 360, 640)), (A("r3", "just"), (1.3, 360, 560)), (A("r3", "hold"), (1.0, 360, 660)),
                (A("r3", "left"), (1.8, 500, 760)), (A("r3", "hand"), (1.5, 470, 740)),
                (A("r3", "never"), (1.2, 330, 720)), (A("r3", "right?"), (1.8, 220, 760)), (A("r3", "right?", end=True),
                                                                                         (1.1, 360, 680))]
    else:
        keys = [(A("r5") - 0.2, (1.2, 360, 660)), (A("r5", "right"), (1.6, 260, 660)), (A("r5", "elbow"), (2.2, 250, 640)),
                (A("r5", "go"), (1.1, 360, 680)), (A("r5", "try"), (1.4, 360, 700))]
    board(cr, t, keys)
    fx, fy = 360, 1000
    if part == 1:
        if t < A("r3", "what"):   # "just one": a big chalk 1 first
            if t >= A("r3", "just"):
                with at(cr, 360, 640, max(0.85, pop(t, A("r3", "just"), 0.25)), rot=-0.06):
                    write(cr, [("1", CHALK_Y)], 0, 120, 340, align="center", bold=True)
                    write(cr, [("just one", CHALK)], 0, 220, 60, align="center", bold=True)
            cue("pop", t, A("r3", "just"))
            return
        with at(cr, fx, fy, max(0.85, pop(t, A("r3", "what"), 0.25))):
            stick_big(cr, t, 0, 0, 1.7)
        # the figure's left hand is on the viewer's right
        if t >= A("r3", "left"):
            sc = pop(t, A("r3", "left"), 0.25)
            with at(cr, fx + 119, fy - 119, sc):
                blob(cr, 0, 0, 44, 44, None, seed=5100, amp=0.8, lw=5, stroke=CHALK_Y)
            write(cr, [("LEFT", CHALK_Y)], fx + 140, fy - 180, 54, align="center", bold=True)
            cue("pop", t, A("r3", "left"))
        if t >= A("r3", "right?"):
            sc = pop(t, A("r3", "right?"), 0.25)
            with at(cr, fx - 119, fy - 119, sc):
                blob(cr, 0, 0, 44, 44, None, seed=5101, amp=0.8, lw=5, stroke=CHALK_P)
            write(cr, [("RIGHT", CHALK_P)], fx - 140, fy - 180, 54, align="center", bold=True)
            cue("pop", t, A("r3", "right?"))
        big_q(cr, t, A("r3", "right?", end=True), 360, 560, 140)
        hl(cr, t, [("hold it in your ", INK), ("LEFT", BLUE)], 215, 62, A("r3", "hold"), end=A("r3", "never") - 0.05,
           bold=True)
        hl(cr, t, [("but ", INK), ("NEVER", RED), (" your right", INK)], 215, 62, A("r3", "never"), bold=True)
    else:
        # left hand crosses over and grabs the right elbow; then the right hand tries, and can't
        u = ease_out(seg(t, A("r5", "elbow") - 0.1, A("r5", "elbow") + 0.25))
        trying = t >= A("r5", "try")
        if not trying:
            left = (lerp(70, -68, u), lerp(-70, -122, u))
            stick_big(cr, t, fx, fy, 1.7, left=left, right=(-110, -60) if u > 0 else None)
            if t >= A("r5", "right"):
                with at(cr, fx - 119, fy - 204, pop(t, A("r5", "right"), 0.25)):
                    blob(cr, 0, 0, 40, 40, None, seed=5110, amp=0.8, lw=5, stroke=CHALK_Y)
            if u >= 1:
                write(cr, [("LEFT hand: easy", CHALK_B)], 360, 470, 46, align="center", bold=True)
        else:
            # spinning in circles, chasing the elbow
            k = math.cos((t - A("r5", "try")) * 14)
            with at(cr, fx, fy, 1.0):
                cr.scale(max(0.15, abs(k)), 1.0)
                stick_big(cr, t, 0, 0, 1.7, right=(-30, -150), smile=False)
            for j in range(3):
                line(cr, [(fx - 180, fy - 300 + j * 60), (fx - 230, fy - 280 + j * 60)], 4, CHALK, seed=5120 + j,
                     amp=0.6)
                line(cr, [(fx + 180, fy - 300 + j * 60), (fx + 230, fy - 280 + j * 60)], 4, CHALK, seed=5130 + j,
                     amp=0.6)
            write(cr, [("RIGHT hand: ", CHALK_P), ("impossible", RED_CHALK)], 360, 470, 46, align="center",
                  bold=True)
            cue("whoosh", t, A("r5", "try"))
        hl(cr, t, [("your ", INK), ("RIGHT ELBOW", RED)], 215, 70, A("r5", "right"), end=A("r5", "try") - 0.05,
           bold=True)
        hl(cr, t, [("go on, ", INK), ("try it", RED)], 215, 70, A("r5", "try"), bold=True)


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def scene_months(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("r7") - 0.2, (1.4, 360, 560)), (A("r7", "many"), (1.0, 360, 700)), (A("r7", "months"), (0.95, 360, 720)),
                (A("r7", "28"), (1.9, 360 + 0 * 190, 640)), (A("r7", "days"), (1.3, 360, 660))]
    else:
        keys = [(A("r9") - 0.2, (1.3, 360, 660)), (A("r9", "12"), (0.95, 360, 720)), (A("r9", "they"), (1.2, 360, 600)),
                (A("r9", "28"), (1.0, 360, 720)), (A("r9", "some"), (1.6, 170, 560)), (A("r9", "keep"), (1.0, 360, 720))]
    board(cr, t, keys)
    for k, (m, d) in enumerate(zip(MONTHS, DAYS)):
        r, c = divmod(k, 3)
        x, y = 170 + c * 190, 430 + r * 185
        sc = pop(t, (A("r7", "months") if part == 1 else A("r9") - 0.3) + k * 0.025, 0.2)
        if sc <= 0:
            continue
        feb = k == 1
        with at(cr, x, y, sc):
            sharp_shape(cr, [(-74, -70), (74, -70), (74, 76), (-74, 76)], None, seed=5200 + k, amp=0.7, lw=4,
                  stroke=CHALK_P if (feb and part == 1) else CHALK)
            line(cr, [(-74, -30), (74, -30)], 3.5, CHALK, seed=5220 + k, amp=0.4)
            write(cr, [(m, CHALK_Y if feb else CHALK)], 0, -40, 34, align="center", bold=True)
            if part == 1:
                if t >= A("r7", "28") and feb:
                    write(cr, [("28", CHALK_P)], 0, 46, 58, align="center", bold=True)
                    blob(cr, 0, 28, 52, 40, None, seed=5240, amp=0.8, lw=4, stroke=CHALK_P)
                elif t >= A("r7", "28"):
                    write(cr, [("?", CHALK)], 0, 46, 58, align="center", bold=True)
            else:
                tick = A("r9", "28") + k * 0.05
                if t >= tick:
                    write(cr, [("28", CHALK_Y)], -14, 46, 50, align="center", bold=True)
                    line(cr, [(30, 20), (42, 36), (64, 4)], 5, hexc("#8be38b"), seed=5260 + k, amp=0.3)
                if t >= A("r9", "keep") and d > 28:
                    n = 28 + min(d - 28, int((t - A("r9", "keep")) * 8))
                    write(cr, [(f"{n}", CHALK_B)], -14, 46, 50, align="center", bold=True)
    if part == 1:
        hl(cr, t, [("how many have ", INK), ("28", RED), (" days?", INK)], 215, 60, A("r7", "months"), bold=True)
    else:
        hl(cr, t, [("ALL ", RED), ("12", RED), (" of them", INK)], 215, 76, A("r9", "12"), end=A("r9", "some") - 0.05,
           bold=True)
        hl(cr, t, [("some just ", INK), ("keep going", BLUE)], 215, 64, A("r9", "some"), bold=True)
        cue("scribble", t, A("r9", "28"))


def rooster(cr, x, y, s=1.0, facing=1, col=CHALK):
    with at(cr, x, y, s, flip=facing < 0):
        blob(cr, 0, 0, 52, 38, None, seed=5300, amp=0.8, lw=5, stroke=col)               # body
        blob(cr, 44, -50, 22, 22, None, seed=5301, amp=0.5, lw=5, stroke=col)             # head
        for k in range(3):   # comb
            blob(cr, 34 + k * 10, -76 - (k % 2) * 4, 8, 9, None, seed=5302 + k, amp=0.3, lw=4, stroke=RED_CHALK)
        shape(cr, [(64, -54), (86, -46), (64, -40)], None, seed=5306, amp=0.3, lw=4, stroke=CHALK_Y)   # beak
        blob(cr, 66, -34, 5, 8, None, seed=5307, amp=0.2, lw=3.5, stroke=RED_CHALK)       # wattle
        blob(cr, 48, -54, 3, 3, col, seed=5308, amp=0.1, lw=0, stroke=None)
        for k in range(4):   # tail
            a = -2.2 - k * 0.25
            line(cr, [(-44, -10), (-44 + math.cos(a) * 70, -10 + math.sin(a) * 70)], 5,
                 [CHALK_B, CHALK_P, CHALK_Y, CHALK][k], seed=5310 + k, amp=0.6)
        for dx in (-12, 14):
            line(cr, [(dx, 36), (dx, 66), (dx + 12, 70)], 4, CHALK_Y, seed=5320 + dx, amp=0.3)


def scene_rooster(cr, t, tl, part):
    A = tl.at
    rx, ry = 360, 700
    if part == 1:
        keys = [(A("r10") - 0.2, (1.2, 360, 760)), (A("r10", "rooster"), (1.9, 380, 680)), (A("r10", "egg"), (2.2, 380, 760)),
                (A("r10", "roof"), (1.0, 360, 820)), (A("r10", "side"), (1.3, 360, 820)),
                (A("r10", "roll"), (1.6, 540, 860))]
    else:
        keys = [(A("r12") - 0.2, (1.2, 360, 760)), (A("r12", "roosters"), (2.0, 380, 680)), (A("r12", "lay"), (1.4, 380, 760)),
                (A("r12", "eggs"), (1.0, 360, 800))]
    board(cr, t, keys)
    # the roof
    sharp_shape(cr, [(100, 1340), (100, 1060), (620, 1060), (620, 1340)], None, seed=5410, amp=0.8, lw=5, stroke=CHALK)
    sharp_shape(cr, [(320, 1340), (320, 1190), (400, 1190), (400, 1340)], None, seed=5411, amp=0.6, lw=4, stroke=CHALK_B)
    for k in range(1, 6):   # roof tiles
        line(cr, [(30 + k * 55, 1070 - k * 50), (690 - k * 55, 1070 - k * 50)], 2.5, hexc("#f4f1e6", 0.35),
             seed=5401 + k, amp=0.5)
    sharp_shape(cr, [(30, 1070), (360, 770), (690, 1070)], None, seed=5400, amp=0.8, lw=6, stroke=CHALK)
    rooster(cr, rx, ry, 1.3, facing=1 if part == 1 or t < A("r12", "lay") else -1)
    if part == 1:
        if t >= A("r10", "egg"):
            sc = pop(t, A("r10", "egg"), 0.25)
            with at(cr, rx - 8, ry + 66, sc):
                blob(cr, 0, 0, 18, 24, None, seed=5420, amp=0.3, lw=4.5, stroke=CHALK)
        if t >= A("r10", "side"):   # two guesses
            for side, col, sd in ((-1, CHALK_B, 5430), (1, CHALK_P, 5440)):
                sc = pop(t, A("r10", "side") + (0.1 if side > 0 else 0), 0.25)
                with at(cr, 360 + side * 190, 840, sc, rot=side * 0.75):
                    line(cr, [(-50, 0), (50, 0)], 6, col, seed=sd, amp=0.4)
                    line(cr, [(side * 30, -22), (side * 52, 0), (side * 30, 22)], 6, col, seed=sd + 1, amp=0.3)
            write(cr, [("LEFT?", CHALK_B)], 150, 960, 46, align="center", bold=True)
            write(cr, [("RIGHT?", CHALK_P)], 570, 960, 46, align="center", bold=True)
        big_q(cr, t, A("r10", "roll"), 360, 520, 120)
        hl(cr, t, [("a ", INK), ("ROOSTER", RED), (" lays an egg", INK)], 215, 60, A("r10", "rooster"),
           end=A("r10", "side") - 0.05, bold=True)
        hl(cr, t, [("which side does it ", INK), ("roll", RED), ("?", INK)], 215, 56, A("r10", "side"), bold=True)
    else:
        # the egg was never there
        if t < A("r12", "lay"):
            blob(cr, rx - 8, ry + 66, 18, 24, None, seed=5420, amp=0.3, lw=4.5, stroke=CHALK)
        else:
            k = seg(t, A("r12", "lay"), A("r12", "lay") + 0.3)
            for i in range(6):
                a = i * math.pi / 3
                blob(cr, rx - 8 + math.cos(a) * 50 * k, ry + 66 + math.sin(a) * 40 * k, 10 * (1 - k) + 1,
                     10 * (1 - k) + 1, None, seed=5450 + i, amp=0.5, lw=3, stroke=CHALK)
            cue("pop", t, A("r12", "lay"))
        if t >= A("r12", "eggs"):
            sc = pop(t, A("r12", "eggs"), 0.25)
            with at(cr, 360, 540, sc, rot=-0.05):
                write(cr, [("ROOSTERS = NO EGGS", CHALK_Y)], 0, 0, 52, align="center", bold=True)
            line(cr, [(150, 560), (570, 560)], 5, CHALK_Y, seed=5460, amp=0.6)
            cue("hit", t, A("r12", "eggs"))
        hl(cr, t, [("roosters ", INK), ("DON'T", RED), (" lay eggs", INK)], 215, 64, A("r12", "lay"), bold=True,
           underline=True)


def scene_up(cr, t, tl):
    """Everything thrown up comes back down... except one thing."""
    A = tl.at
    keys = [(A("r14") - 0.2, (1.1, 360, 760)), (A("r14", "turn"), (1.3, 360, 700)), (A("r14", "goes"), (1.0, 360, 760)),
            (A("r14", "up,"), (1.3, 500, 560)), (A("r14", "never"), (1.0, 360, 760)), (A("r14", "comes"), (1.4, 300, 1000)),
            (A("r14", "down?"), (1.0, 360, 760))]
    board(cr, t, keys)
    line(cr, [(-200, 1240), (900, 1240)], 6, CHALK, seed=5530, amp=0.8)     # the ground
    t0 = A("r14")
    for x, d, kind, col in ((150, 0.0, "ball", CHALK_Y), (300, 0.35, "plane", CHALK_P), (450, 0.7, "ball", CHALK_B)):
        if t < t0 + d:
            continue
        u = ((t - t0 - d) / 1.3) % 1                # thrown up, falls back down, again and again
        y = 1200 - math.sin(u * math.pi) * 560
        if kind == "ball":
            blob(cr, x, y, 30, 30, None, seed=5500 + x, amp=0.5, lw=5, stroke=col)
        else:
            with at(cr, x, y, 1.0, rot=-0.4 if u < 0.5 else 0.5):
                shape(cr, [(-50, 0), (50, -16), (0, 20)], None, seed=5510, amp=0.4, lw=4.5, stroke=col)
        if u > 0.5:   # falling: motion lines above it
            for k in (-14, 14):
                line(cr, [(x + k, y - 50), (x + k, y - 90)], 3, CHALK, seed=5540 + k, amp=0.3)
        if int((t - t0 - d) / 1.3) != int((t - t0 - d - 1.0 / 30) / 1.3):
            cue("thud", t, t)
    if A("r14", "turn") <= t < A("r14", "goes"):   # the teacher's riddle, chalked big
        with at(cr, 360, 700, max(0.85, pop(t, A("r14", "turn"), 0.25)), rot=-0.05):
            write(cr, [("TEACHER'S", CHALK_P)], 0, -40, 80, align="center", bold=True)
            write(cr, [("RIDDLE", CHALK_Y)], 0, 70, 120, align="center", bold=True)
        cue("scribble", t, A("r14", "turn"))
    # the one thing that only goes up
    if t >= A("r14", "up,"):
        k = ease_out(seg(t, A("r14", "up,"), A("r14", "up,") + 0.35))
        top = 1200 - 760 * k
        line(cr, [(610, 1200), (610, top)], 9, CHALK_Y, seed=5520, amp=0.5)
        line(cr, [(570, top + 50), (610, top), (650, top + 50)], 9, CHALK_Y, seed=5521, amp=0.3)
        cue("whoosh", t, A("r14", "up,"))
    big_q(cr, t, A("r14", "down?"), 610, 340, 150)
    hl(cr, t, [("\"MY TURN.\"", RED)], 215, 88, A("r14", "turn"), end=A("r14", "goes") - 0.05, bold=True)
    hl(cr, t, [("goes ", INK), ("UP", BLUE), (", never comes ", INK), ("DOWN", RED)], 215, 56, A("r14", "goes"),
       bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("r17") - 0.2, (1.1, 470, 760)), (A("r17", "next"), (1.4, 560, 740)), (A("r17", "hands"), (1.7, 220, 780)),
            (A("r17", "50"), (2.3, 230, 740)), (A("r17", "brand"), (1.9, 200, 700)), (A("r17", "riddles"), (1.0, 470, 770)),
            (A("r17", "riddles") + 0.5, (2.0, 160, 740))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t, day=2)
    drop = A("r17", "hands")
    done = t >= A("r17", "brand")
    person(cr, "teacher", TX, 900, t, facing=1, arms=("face", "hip") if done else ("hip", "hip"),
           eyes="closed" if done else ("wide" if t >= drop else "dot"), mouth="wobble" if done else "o",
           sweat=done, shake=1.0 if t >= A("r17", "riddles") else 0)
    laugh = t >= A("r17", "riddles")
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, eyes="closed" if laugh else "dot", mouth="laugh" if laugh else "smile",
                 jump=abs(math.sin(t * 9 + i)) * 8 if laugh else 0)
        if who == "chotu":
            k.update(eyes="happy", mouth="grin", arms=("cheer", "hip") if t >= drop else ("hip", "hip"))
            person(cr, who, x, 864 if t >= drop else 900, t, **k)
        else:
            person(cr, who, x, 900, t, **k)
        desk(cr, x, 4200 + i * 10)
    # fifty pages thump down next to the teacher, one by one
    n = int(16 * seg(t, drop, A("r17", "50", end=True)))
    for k in range(n):
        y = 900 - k * 9
        shape(cr, [(190, y), (290, y - 2), (292, y - 10), (192, y - 8)], WHITE, seed=5600 + k, amp=0.4, lw=2.5)
        cue("pop", t, drop + k * (A("r17", "50", end=True) - drop) / 16)
    if done:
        with at(cr, 240, 900 - 16 * 9 - 50, pop(t, A("r17", "brand"), 0.25), rot=-0.06):
            shape(cr, [(-80, -34), (80, -34), (80, 34), (-80, 34)], WHITE, seed=5620, amp=0.5, lw=3.5)
            write(cr, [("RIDDLES", RED)], 0, 4, 32, align="center", bold=True)
            write(cr, [("vol. 2", INK)], 0, 28, 20, align="center")
    hl(cr, t, [("NEXT DAY", RED), ("...", INK)], 215, 76, A("r17", "next"), end=A("r17", "50") - 0.05, bold=True)
    stamp(cr, t, A("r17", "50"), "50 PAGES", dur=0.6, y=330)
    hl(cr, t, [("50 pages of ", INK), ("NEW RIDDLES", RED)], 215, 62, A("r17", "brand"), bold=True, underline=True)
    cue("hit", t, A("r17", "riddles"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "elbow":
        scene_elbow(cr, t, tl, 1)
    elif name == "elbow2":
        scene_elbow(cr, t, tl, 2)
    elif name == "months":
        scene_months(cr, t, tl, 1)
    elif name == "months2":
        scene_months(cr, t, tl, 2)
    elif name == "rooster":
        scene_rooster(cr, t, tl, 1)
    elif name == "rooster2":
        scene_rooster(cr, t, tl, 2)
    elif name == "up":
        scene_up(cr, t, tl)
    elif name == "end":
        scene_end(cr, t, tl)
    else:
        scene_class(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
