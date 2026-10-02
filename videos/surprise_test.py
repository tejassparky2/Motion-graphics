"""Paradox x The Last Bencher: "The Surprise Test Paradox" (also called the unexpected hanging paradox).

The teacher announces a surprise test next week. The last bencher "proves" it can't happen by ruling out Friday, then
Thursday, and so on. Then the test comes on Wednesday, and he's surprised. Same structure as The Infinite Hotel:
impossible premise, a character line, step-by-step logic, the twist, the name, an open question.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.timeline import clear_dialogue
from videos.backbencher import (CHALK, CHALK_B, CHALK_P, CHALK_Y, CX, KID, KIDS, ROW, TEACH, TX, WIDE, board,
                                classroom, desk)

NARRATOR = dict(max_pause=0.42)
TAIL = 0.9

SCRIPT = [
    dict(id="s1", scene="class", text="The teacher says: there's a surprise test next week. You won't know the day, "
                                      "until it happens.", speaker="teacher", speaker_from="there's"),
    dict(id="s2", scene="class", text="The last bencher in class grins. Sir, that test is impossible.", speaker="chotu",
         speaker_from="sir,"),
    dict(id="s3", scene="days", text="If there's no test by Thursday, it has to be Friday. Then it's no surprise. So "
                                     "Friday's out.", speaker="chotu"),
    dict(id="s4", scene="days", text="Now Thursday is the last day. Same logic. Thursday's out. Then Wednesday. "
                                     "Tuesday. Monday.", speaker="chotu"),
    dict(id="s5", scene="days", text="No day works. So there's no test!", speaker="chotu"),
    dict(id="s6", scene="class2", text="He doesn't study at all. And on Wednesday, the teacher hands out the test."),
    dict(id="s7", scene="class2", text="He's totally surprised. Just like the teacher said."),
    dict(id="s8", scene="name", text="It's called the surprise test paradox. Every step of his logic sounds right. "
                                     "But the test still came."),
    dict(id="s9", scene="end", text="So... where did his logic go wrong?", pace=0.95),
]
clear_dialogue(SCRIPT)

METADATA = dict(
    title="He PROVED the Surprise Test Was Impossible… Then It Happened 😳",
    alt_titles=["The Last Bencher vs The Surprise Test Paradox 🤯", "This Logic Is Perfect… So Why Is It Wrong? 😳"],
    description="""The teacher announces a surprise test next week. The last bencher proves it's impossible: it can't be Friday (he'd know by Thursday), so then Thursday is the last day… and so on, all the way back to Monday. 🤯

So he doesn't study. On Wednesday, the test lands on his desk. He's totally surprised, exactly like the teacher said. 😳

It's called the surprise test paradox (also known as the unexpected hanging paradox), and philosophers still argue about where the logic breaks.

💬 So… where did his logic go wrong? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#LastBencher", "#MindBlown"],
    tags=["surprise test paradox", "unexpected hanging paradox", "paradox", "last bencher", "logic puzzle",
          "brain teaser", "mind blowing", "philosophy", "school story", "interestingly strange"],
    pinned_comment="Where EXACTLY does his logic break? 🤔 Best explanation gets pinned 👇",
)

BLUE = hexc("#3f6fb5")
RED_CHALK = hexc("#ff6b6b")
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
DX = [110, 235, 360, 485, 610]


def day_boxes(cr, t, crossed, test_on=None, circle=None):
    for k, (d, x) in enumerate(zip(DAYS, DX)):
        shape(cr, rrect_pts(x - 56, 560, 112, 150, 10, 14), None, seed=1000 + k, amp=0.5, lw=5,
              stroke=CHALK_Y if k == circle else CHALK)
        write(cr, [(d, CHALK_Y if k == circle else CHALK)], x, 620, 40, align="center", bold=True)
        if k in crossed:
            u = seg(t, crossed[k], crossed[k] + 0.18)
            line(cr, [(x - 46, 580), (x - 46 + 92 * u, 580 + 120 * u)], 9, RED_CHALK, seed=1010 + k, amp=0.3)
            line(cr, [(x + 46, 580), (x + 46 - 92 * u, 580 + 120 * u)], 9, RED_CHALK, seed=1020 + k, amp=0.3)
            cue("scribble", t, crossed[k])
        if k == test_on:
            write(cr, [("TEST!", RED_CHALK)], x, 690, 34, align="center", bold=True)


def scene_class(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(0, (1.8, 160, 720)), (A("s1", "surprise"), (1.3, 300, 700)), (A("s1", "week."), (1.0, 470, 760)),
                (A("s1", "know"), (1.9, 140, 720)), (A("s1", "happens."), (1.2, 300, 740)),
                (A("s2"), KID), (A("s2", "grins."), (2.3, 830, 715)), (A("s2", "sir,"), (1.6, 700, 740)),
                (A("s2", "impossible."), (2.2, 830, 715))]
    else:
        keys = [(A("s6") - 0.1, KID), (A("s6", "study"), (2.2, 830, 720)), (A("s6", "wednesday,"), (1.0, 470, 760)),
                (A("s6", "hands"), (1.5, 600, 760)), (A("s6", "test.", nth=1), (2.0, 820, 760)),
                (A("s7"), (2.4, 830, 715)), (A("s7", "just"), (1.4, 300, 740)), (A("s7", "said."), (2.0, 140, 720))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t, day=None if part == 1 else 3)
    # the chalkboard: "SURPRISE TEST NEXT WEEK"
    shape(cr, rrect_pts(-170, 420, 400, 220, 6, 20), hexc("#2f5b46"), seed=1100, amp=0.3, lw=0, stroke=None)
    write(cr, [("SURPRISE TEST", CHALK_Y)], 30, 500, 40, align="center", bold=True)
    write(cr, [("next week", CHALK)], 30, 560, 34, align="center")
    teach = dict(facing=1, arms=("point", "hip"), eyes="sly", mouth="smirk")
    if part == 2:
        hand = A("s6", "hands")
        teach.update(arms=("give", "hip") if t < A("s7") else ("hip", "hip"), eyes="happy", mouth="grin")
        tx = lerp(TX, 690, ease_out(seg(t, A("s6", "wednesday,") - 0.4, hand)))
    else:
        tx = TX
    if tl.speaking("teacher", t):
        teach["mouth"] = "o" if int(t * 12) % 2 else "smirk"
    person(cr, "teacher", tx, 900, t, **teach)
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if who == "chotu":
            if part == 1:
                stand = seg(t, A("s2", "grins.") - 0.1, A("s2", "grins.") + 0.15)
                y -= 36 * stand
                if t >= A("s2", "grins."):
                    k.update(eyes="sly", mouth="smirk", arms=("cheer", "hip"))
            else:
                k.update(eyes="happy", mouth="grin", arms=("chin", "face"), lean=-0.1)   # relaxing, no studying
                if t >= A("s6", "test.", nth=1):
                    k.update(eyes="wide", mouth="o", sweat=True, arms=("face", "down"), shake=1.2, lean=0)
            if tl.speaking("chotu", t):
                k["mouth"] = "o" if int(t * 12) % 2 else "smirk"
        elif part == 2 and t >= A("s6", "test.", nth=1):
            k.update(eyes="sly", mouth="smirk")
        person(cr, who, x, y, t, **k)
        desk(cr, x, 4200 + i * 10)
    if part == 2:   # the test paper lands on his desk
        land = A("s6", "test.", nth=1)
        if t >= A("s6", "hands"):
            u = ease_out(seg(t, A("s6", "hands"), land))
            px, py = lerp(tx + 40, CX + 4, u), lerp(780, 792, u) - math.sin(u * math.pi) * 60
            sharp_shape(cr, [(px - 34, py - 6), (px + 34, py - 8), (px + 36, py + 6), (px - 32, py + 8)], WHITE,
                        seed=1120, amp=0.3, lw=2.5)
            if u >= 1:
                write(cr, [("TEST", RED)], px, py + 4, 16, align="center", bold=True)
        cue("thud", t, land)
    # screen text
    if part == 1:
        hl(cr, t, [("SURPRISE TEST", RED), (" next week", INK)], 215, 60, 0.0, end=A("s2") - 0.05, bold=True,
           sound=False)
        hl(cr, t, [("\"That test is ", INK), ("IMPOSSIBLE", RED), (".\"", INK)], 215, 56, A("s2", "impossible."),
           bold=True)
    else:
        hl(cr, t, [("he doesn't ", INK), ("STUDY", RED)], 215, 72, A("s6", "study"), end=A("s6", "wednesday,") - 0.05,
           bold=True)
        hl(cr, t, [("WEDNESDAY", RED), ("...", INK)], 215, 76, A("s6", "wednesday,"), end=A("s7") - 0.05, bold=True)
        stamp(cr, t, A("s7", "surprised."), "SURPRISE!", dur=0.7, y=330)
        hl(cr, t, [("just like the ", INK), ("TEACHER", BLUE), (" said", INK)], 215, 60, A("s7", "just"), bold=True)
        cue("hit", t, A("s7", "surprised."))


def scene_days(cr, t, tl):
    A = tl.at
    keys = [(A("s3") - 0.2, (1.0, 360, 640)), (A("s3", "thursday,"), (1.7, DX[3], 640)), (A("s3", "friday."), (1.7, DX[4], 640)),
            (A("s3", "surprise."), (1.0, 360, 660)), (A("s3", "out."), (1.8, DX[4], 640)),
            (A("s4"), (1.7, DX[3], 640)), (A("s4", "logic."), (1.0, 360, 660)), (A("s4", "thursday's"), (1.8, DX[3], 640)),
            (A("s4", "wednesday."), (1.7, DX[2], 640)), (A("s4", "tuesday."), (1.7, DX[1], 640)),
            (A("s4", "monday."), (1.7, DX[0], 640)), (A("s5"), (1.0, 360, 660)), (A("s5", "test!"), (1.3, 360, 820))]
    board(cr, t, keys)
    crossed = {}
    if t >= A("s3", "out."):
        crossed[4] = A("s3", "out.")
    for k, key in ((3, "thursday's"), (2, "wednesday."), (1, "tuesday."), (0, "monday.")):
        if t >= A("s4", key):
            crossed[k] = A("s4", key)
    day_boxes(cr, t, crossed)
    if A("s3", "thursday,") <= t < A("s3", "out."):   # "if no test by Thursday..." arrow to Friday
        line(cr, [(DX[3], 760), (DX[4], 760)], 6, CHALK_B, seed=1200, amp=0.4)
        line(cr, [(DX[4] - 20, 744), (DX[4], 760), (DX[4] - 20, 776)], 6, CHALK_B, seed=1201, amp=0.2)
        write(cr, [("he'd KNOW", CHALK_B)], 548, 820, 34, align="center", bold=True)
    if t >= A("s5", "test!"):
        with at(cr, 360, 900, max(0.85, pop(t, A("s5", "test!"), 0.25)), rot=-0.05):
            write(cr, [("NO TEST!", CHALK_Y)], 0, 0, 110, align="center", bold=True)
        cue("hit", t, A("s5", "test!"))
    hl(cr, t, [("Friday? He'd ", INK), ("KNOW", RED)], 215, 66, A("s3", "thursday,"), end=A("s4") - 0.05, bold=True)
    hl(cr, t, [("same logic, ", INK), ("every day", RED)], 215, 66, A("s4", "logic."), end=A("s5") - 0.05, bold=True)
    hl(cr, t, [("no day works", INK)], 215, 74, A("s5"), bold=True)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("s8") - 0.2, (1.0, 360, 620)), (A("s8", "surprise"), (1.25, 360, 540)), (A("s8", "every"), (1.0, 360, 640)),
            (A("s8", "right."), (1.25, 360, 700)), (A("s8", "still"), (1.5, DX[2], 680))]
    board(cr, t, keys)
    crossed = {k: -10 for k in (0, 1, 3, 4)}
    if t < A("s8", "still"):
        crossed[2] = -10
    day_boxes(cr, t, crossed, test_on=2 if t >= A("s8", "still") else None, circle=2 if t >= A("s8", "still") else None)
    with at(cr, 360, 430, max(0.85, pop(t, A("s8", "surprise"), 0.3)), rot=-0.03):
        write(cr, [("THE SURPRISE TEST", CHALK)], 0, 0, 52, align="center", bold=True)
        write(cr, [("PARADOX", CHALK_P)], 0, 64, 68, align="center", bold=True)
    if t >= A("s8", "right."):
        for k in range(5):
            line(cr, [(DX[k] - 18, 770), (DX[k] - 4, 786), (DX[k] + 20, 754)], 6, hexc("#8be38b"), seed=1300 + k,
                 amp=0.2)
    hl(cr, t, [("every step sounds ", INK), ("RIGHT", hexc("#2e9e52"))], 215, 58, A("s8", "every"),
       end=A("s8", "still") - 0.05, bold=True)
    hl(cr, t, [("...but the test ", INK), ("CAME", RED)], 215, 66, A("s8", "still"), bold=True)
    cue("hit", t, A("s8", "still"))


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("s9") - 0.2, (1.3, 760, 760)), (A("s9", "logic"), (2.2, 830, 715)), (A("s9", "wrong?"), (1.3, 600, 740))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t, day=3)
    person(cr, "teacher", TX, 900, t, facing=1, arms=("hip", "hip"), eyes="happy", mouth="grin")
    for i, (who, x) in enumerate(KIDS):
        if who == "chotu":
            person(cr, who, x, 900, t, facing=-1, arms=("chin", "face"), eyes="wide", mouth="o", sweat=True)
            for k in range(3):   # question marks over his head
                u = (t * 0.9 + k / 3) % 1
                write(cr, [("?", hexc("#e0483d", 1 - u))], x - 30 + k * 30, 690 - u * 90, 40 + k * 8, align="center",
                      bold=True)
        else:
            person(cr, who, x, 900, t, facing=-1)
        desk(cr, x, 4200 + i * 10)
    hl(cr, t, [("where did his logic go ", INK), ("WRONG", RED), ("?", INK)], 215, 54, A("s9"), bold=True,
       underline=True)
    stamp(cr, t, A("s9", "wrong?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "class":
        scene_class(cr, t, tl, 1)
    elif name == "class2":
        scene_class(cr, t, tl, 2)
    elif name == "days":
        scene_days(cr, t, tl)
    elif name == "name":
        scene_name(cr, t, tl)
    else:
        scene_end(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
