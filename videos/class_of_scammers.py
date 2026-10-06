"""Episode 15: "The Class of Scammers" — follows the reference Short's story beats and ending, in our own words.

Beats kept: a teacher finds cigarettes in the classroom bin; the school cameras have been broken for years but the
kids don't know; he bluffs that the principal saw the footage and whoever confesses will be saved; after minutes of
silence one kid confesses stealing from the staff room and selling it online; another kid is outed as the teacher's
secret-teller; a student who'd been "injured" for six months admits faking it for easy PE marks; the backbencher admits
planting something in a teacher's bag to get him fired; the pack turns out to be fake; the whole class is suspended.

Changes for a US audience and advertiser safety: names; the planted item is exam answers (not drugs); the faked
condition is a broken leg on crutches (not a disability); the fake cigarettes are candy cigarettes. The reference's
"real story" claim is not repeated (unverified).
"""
import math

from motion.captions import captions
from motion.characters import bubble, person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import classroom, desk, red_face

NARRATOR = dict(speed=1.03)
TAIL = 0.8

SCRIPT = [
    dict(id="c1", scene="trash", text="A teacher finds a pack of cigarettes in the classroom trash can."),
    dict(id="c2", scene="cctv",
         text="The school's cameras have been broken for years. But the kids don't know that. So he makes a plan."),
    dict(id="c3", scene="class",
         text="He slams the desk. The principal already checked the cameras. Whoever did this, confess now, and "
              "you'll be saved.", speaker="teacher", speaker_from="principal"),
    dict(id="c4", scene="class", text="[Four minutes|4 minutes] of silence. Then Tyler stands up.", gap=0.25),
    dict(id="c5", scene="class",
         text="Sir, I'm sorry. I've been stealing stuff from the teachers' lounge, and selling it online.",
         speaker="kid_c"),
    dict(id="c6", scene="class", text="Emma gasps: so you're the thief!", speaker="kid_a", speaker_from="so"),
    dict(id="c7", scene="class",
         text="Oh, like you're so innocent. You're the one who tells the teacher everyone's secrets!", speaker="kid_c"),
    dict(id="c8", scene="class", text="The whole class turns to Emma. She says nothing."),
    dict(id="c9", scene="class",
         text="[Three more minutes|3 more minutes] of silence. Then Olivia, who's been on crutches for "
              "[six months,|6 months,] stands up, and walks.", gap=0.25),
    dict(id="c10", scene="class", text="My leg is fine. I faked it since September, to get an easy A in gym.",
         speaker="kid_d"),
    dict(id="c11", scene="class", text="The teacher's jaw drops. Then Jake, from the last row, stands up."),
    dict(id="c12", scene="class",
         text="If we're all confessing, remember when Mr. Miller got fired for having the exam answers in his bag? "
              "I put them there. He failed me on every test.", speaker="chotu"),
    dict(id="c13", scene="class",
         text="Now the teacher is furious. He holds up the pack: so who does this belong to?", speaker="teacher",
         speaker_from="so"),
    dict(id="c14", scene="reveal", text="Everyone leans in. And it's, candy cigarettes.", gap=0.2),
    dict(id="c15", scene="end",
         text="A pack of candy exposed the entire class. And every one of them got suspended.", gap=0.2),
]

METADATA = dict(
    title="The Teacher Bluffed… and the Whole Class Confessed 😳",
    alt_titles=["One Fake Pack Exposed the Entire Class 😂", "Class of Scammers: Every Kid Had a Secret 🤫"],
    description="""A teacher finds a pack of cigarettes in the classroom trash. The school cameras have been broken for years, but the kids don't know that… so he bluffs. 😏

One by one, the confessions start: a thief, a snitch, a fake injury, and a teacher who got fired for something he never did. Then he finally holds up the pack… 🤫

💬 Which confession was the worst? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#School", "#Storytime"],
    tags=["plot twist", "school story", "teacher bluff", "classroom story", "funny story", "twist ending",
          "confessions", "storytime", "animated story", "interestingly strange"],
    pinned_comment="Rank the confessions: thief, snitch, fake injury, or the backbencher? 😳👇",
)

GOLD = hexc("#f2b632")
GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
PURPLE = hexc("#6a45b5")
TX = 120
EMMA, TYLER, OLIVIA, JAKE = ("kid_a", 330), ("kid_c", 490), ("kid_d", 650), ("chotu", 830)
KIDS = (EMMA, TYLER, OLIVIA, JAKE)
TEACH = (1.8, 150, 745)
WIDE = (0.85, 470, 770)
ROW = (1.2, 600, 770)


def focus(x, z=2.0):
    return (z, x - 20, 730)


def cig_pack(cr, x, y, s=1.0, rot=0.0, candy=False, seed=0):
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-50, -70, 100, 140, 8, 14), WHITE, seed=seed, amp=0.5, lw=4)
        shape(cr, rrect_pts(-50, -70, 100, 50, 8, 14), PINK if candy else RED, seed=seed + 1, amp=0.4, lw=3.5)
        for k in range(4):   # sticks poking out
            line(cr, [(-30 + k * 20, -70), (-30 + k * 20, -104)], 11, WHITE, seed=seed + 2 + k, amp=0.1)
            blob(cr, -30 + k * 20, -104, 5.5, 4, PINK if candy else hexc("#e8a93b"), seed=seed + 8 + k, amp=0.2, lw=1.5)
        if candy:
            write(cr, [("CANDY", PINK)], 0, 20, 30, align="center", bold=True)
            write(cr, [("sugar sticks", INK)], 0, 50, 16, align="center")
        else:
            write(cr, [("???", RED)], 0, 30, 34, align="center", bold=True)


def trash_can(cr, x, y, seed=0):
    shape(cr, [(x - 55, y - 140), (x + 55, y - 140), (x + 42, y), (x - 42, y)], hexc("#6b7280"), seed=seed, amp=0.6, lw=4)
    for k in range(3):
        line(cr, [(x - 30 + k * 30, y - 125), (x - 24 + k * 24, y - 12)], 3, hexc("#555a66"), seed=seed + k, amp=0.3)
    blob(cr, x, y - 140, 62, 12, hexc("#8a8f99"), seed=seed + 5, amp=0.4, lw=3.5)


def cctv(cr, x, y, t, seed=0):
    line(cr, [(x + 70, y - 30), (x + 70, y + 10)], 6, INK, seed=seed, amp=0.2)
    with at(cr, x, y, 1.0, rot=0.35):
        shape(cr, rrect_pts(-70, -24, 130, 52, 8, 14), WHITE, seed=seed + 1, amp=0.5, lw=4)
        blob(cr, -74, 2, 16, 18, INK, seed=seed + 2, amp=0.3, lw=3)
    # cobweb + tape: broken for years
    for k in range(5):
        a = -0.2 + k * 0.35
        line(cr, [(x + 70, y - 30), (x + 70 + 70 * math.cos(a), y - 30 + 70 * math.sin(a))], 1.5, hexc("#9a958a"),
             seed=seed + 10 + k, amp=0.2)
    sharp_shape(cr, [(x - 60, y - 10), (x + 40, y + 30), (x + 34, y + 44), (x - 66, y + 4)], GOLD, seed=seed + 20, amp=0.3,
                lw=2.5)
    write(cr, [("BROKEN", INK)], x - 12, y + 28, 18, align="center", bold=True)


def crutches(cr, x, y, standing=True, seed=0):
    """Two crutches leaning on the desk beside her."""
    for k, dx in enumerate((0, 22)):
        for lw, col in ((13, INK), (8, hexc("#c7c2cc"))):
            line(cr, [(x + dx + 30, y), (x + dx, y - 200)], lw, col, seed=seed + k, amp=0.2)
        line(cr, [(x + dx - 16, y - 200), (x + dx + 16, y - 196)], 9, INK, seed=seed + 5 + k, amp=0.1)
        line(cr, [(x + dx + 4, y - 110), (x + dx + 26, y - 108)], 7, INK, seed=seed + 9 + k, amp=0.1)


def scene_trash(cr, t, tl):
    A = tl.at
    keys = [(0, (2.2, 40, 740)), (A("c1", "teacher"), (1.6, 90, 740)), (A("c1", "finds"), (2.0, 20, 780)),
            (A("c1", "cigarettes"), (2.6, 30, 720)), (A("c1", "trash"), (1.8, 30, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    person(cr, "teacher", 150, 900, t, facing=-1, arms=("give", "hip") if t >= A("c1", "finds") else ("hip", "hip"),
           eyes="wide" if t >= A("c1", "cigarettes") else "dot", mouth="o" if t >= A("c1", "cigarettes") else "smile")
    trash_can(cr, 20, 905, seed=12100)
    rise = ease_out(seg(t, A("c1", "finds"), A("c1", "cigarettes", end=True)))
    cig_pack(cr, 30, lerp(790, 690, rise), 0.8, rot=-0.2 * rise, seed=12110)
    hl(cr, t, [("a pack of ", INK), ("CIGARETTES", RED)], 215, 64, A("c1", "cigarettes"), bold=True)
    if rise > 0:
        cue("pop", t, A("c1", "finds"))


def scene_cctv(cr, t, tl):
    A = tl.at
    keys = [(A("c2") - 0.2, (1.2, 460, 600)), (A("c2", "cameras"), (2.2, 560, 420)), (A("c2", "broken"), (2.8, 560, 440)), (A("c2", "years"), (1.8, 560, 460)),
            (A("c2", "kids"), (1.1, 560, 760)), (A("c2", "know"), (1.5, 640, 760)), (A("c2", "plan"), (2.1, 150, 720))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    cctv(cr, 560, 400, t, seed=12200)
    for i, (who, x) in enumerate(KIDS):
        person(cr, who, x, 900, t, facing=-1, eyes="dot", mouth="smile")
        desk(cr, x, 12210 + i * 10)
    sly = t >= A("c2", "plan")
    person(cr, "teacher", TX, 900, t, facing=1, arms=("chin", "hip") if sly else ("hip", "hip"), eyes="sly" if sly else "dot",
           mouth="smirk" if sly else "smile")
    if sly:   # a light bulb
        with at(cr, TX + 10, 640, pop(t, A("c2", "plan"), 0.25) or 0.01):
            blob(cr, 0, 0, 26, 30, hexc("#ffe28a"), seed=12230, amp=0.4, lw=3.5)
            shape(cr, rrect_pts(-12, 26, 24, 16, 3, 8), hexc("#a9a2ae"), seed=12231, amp=0.2, lw=3)
        cue("pop", t, A("c2", "plan"))
    hl(cr, t, [("cameras: ", INK), ("BROKEN", RED)], 215, 80, A("c2", "broken"), end=A("c2", "kids") - 0.05, bold=True)
    hl(cr, t, [("the kids ", INK), ("don't know", BLUE)], 215, 76, A("c2", "kids"), end=A("c2", "plan") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("PLAN", GOLD)], 215, 96, A("c2", "plan"), bold=True)


def scene_class(cr, t, tl):
    A = tl.at
    tyler_up = A("c4", "stands")
    olivia_up = A("c9", "stands")
    jake_up = A("c11", "stands")
    keys = [(A("c3") - 0.2, TEACH), (A("c3", "slams"), (2.4, 140, 760)), (A("c3", "principal"), (1.5, 170, 740)),
            (A("c3", "cameras"), (1.0, 380, 740)), (A("c3", "confess"), (2.0, 150, 730)), (A("c3", "saved"), WIDE),
            (A("c4"), (1.3, 600, 760)), (A("c4", "Tyler"), focus(TYLER[1])), (A("c5", "sorry"), focus(TYLER[1], 2.3)),
            (A("c5", "stealing"), (1.5, 420, 700)), (A("c5", "lounge"), (2.0, 430, 560)), (A("c5", "selling"), (1.3, 450, 700)),
            (A("c5", "online"), focus(TYLER[1], 1.9)),
            (A("c6", "Emma"), focus(EMMA[1])), (A("c6", "thief"), focus(EMMA[1], 2.4)), (A("c7"), focus(TYLER[1], 2.1)), (A("c7", "innocent"), focus(EMMA[1], 2.2)),
            (A("c7", "one"), focus(TYLER[1], 1.7)),
            (A("c7", "tells"), (1.5, 420, 700)), (A("c7", "secrets"), (1.6, 380, 740)), (A("c8", "turns"), ROW),
            (A("c8", "nothing"), focus(EMMA[1], 2.3)),
            (A("c9"), (1.2, 560, 760)), (A("c9", "Olivia"), focus(OLIVIA[1])), (A("c9", "crutches"), (1.6, 650, 790)),
            (A("c9", "stands"), focus(OLIVIA[1], 1.8)), (A("c9", "walks"), (1.4, 560, 760)),
            (A("c10", "leg"), (2.2, 560, 760)), (A("c10", "fine"), (1.5, 560, 800)), (A("c10", "faked"), (1.6, 520, 700)),
            (A("c10", "September"), (2.3, 560, 720)), (A("c10", "easy"), (1.4, 520, 740)), (A("c10", "gym"), (1.9, 560, 740)),
            (A("c11", "jaw"), (2.3, 140, 740)), (A("c11", "Jake"), focus(JAKE[1])), (A("c11", "last"), ROW),
            (A("c12", "confessing"), focus(JAKE[1], 2.2)), (A("c12", "Miller"), (1.5, 680, 690)),
            (A("c12", "exam"), (2.1, 640, 470)), (A("c12", "bag"), (1.4, 700, 620)),
            (A("c12", "put"), focus(JAKE[1], 2.4)), (A("c12", "there"), (1.5, 760, 700)), (A("c12", "failed"), (1.6, 760, 740)),
            (A("c12", "every"), focus(JAKE[1], 2.3)),
            (A("c13", "furious"), (2.2, 140, 740)), (A("c13", "holds"), (1.6, 220, 700)), (A("c13", "belong"), WIDE)]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    # ---- teacher
    s = dict(facing=1, arms=("hip", "hip"), eyes="sly", mouth="flat")
    if A("c3", "slams") <= t < A("c3", "slams") + 0.4:
        s.update(arms=("point", "hip"), shake=2.5)
    if t >= A("c3", "principal"):
        s.update(arms=("point", "hip"), eyes="sly")
    if t >= A("c4"):
        s.update(arms=("hip", "hip"), eyes="dot", mouth="flat")
    if A("c5") <= t < A("c9"):
        s.update(eyes="wide", mouth="o")
    if A("c10") <= t < A("c13"):
        s.update(eyes="wide", mouth="o", sweat=True)
    if t >= A("c13"):
        s.update(eyes="sly", mouth="flat", arms=("cheer", "hip") if t >= A("c13", "holds") else ("hip", "hip"),
                 shake=1.5 if t < A("c13", "holds") else 0)
    if tl.speaking("teacher", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "flat"
    person(cr, "teacher", TX, 900, t, **s)
    red_face(cr, t, seg(t, A("c13"), A("c13") + 0.3))
    if t >= A("c13", "holds"):
        cig_pack(cr, TX + 60, 640, 0.6, rot=0.2, seed=12300)
    if A("c3", "slams") <= t < A("c3", "slams") + 0.5:
        write(cr, [("BAM!", RED)], 240, 700, 60, align="center", bold=True, halo=WHITE)
        cue("hit", t, A("c3", "slams"))
    # ---- kids
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if A("c3", "slams") <= t < A("c4"):
            k.update(eyes="wide", mouth="o", sweat=True)
        if who == "kid_c":
            y -= 36 * seg(t, tyler_up - 0.1, tyler_up + 0.15)
            if A("c5") <= t < A("c6"):
                k.update(eyes="sad", mouth="wobble")
            if A("c7") <= t < A("c8"):
                k.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
        if who == "kid_a":
            if A("c6") <= t < A("c7"):
                k.update(arms=("point", "hip"), eyes="wide", mouth="o")
            if A("c7", "tells") <= t < A("c9"):
                k.update(eyes="sad", mouth="flat", sweat=True)
        if who == "kid_d":
            if t < olivia_up:
                k.update(eyes="sad", mouth="flat")
            else:
                walk = seg(t, A("c9", "walks"), A("c9", "walks", end=True) + 0.4)
                x = lerp(OLIVIA[1], 560, walk)
                y = 900
                k.update(walk=t * 2.5 if 0 < walk < 1 else None, eyes="happy", mouth="grin",
                         arms=("wave", "hip") if t < A("c11") else ("hip", "hip"))
        if who == "chotu":
            y -= 36 * seg(t, jake_up - 0.1, jake_up + 0.15)
            if A("c12") <= t < A("c13"):
                k.update(eyes="sly", mouth="smirk", arms=("chin", "hip"))
        if A("c8", "turns") <= t < A("c9") and who != "kid_a":
            k.update(facing=1 if x < EMMA[1] + 1 else -1, eyes="wide", mouth="o")
        if t >= A("c13") and who in ("kid_c", "kid_a", "kid_d", "chotu"):
            k.update(eyes="wide", mouth="o", sweat=True)
        if tl.speaking(who, t):
            k["mouth"] = "o" if int(t * 12) % 2 else "smile"
        if who == "kid_d" and t < olivia_up:
            crutches(cr, x + 60, 900, seed=12310)
        person(cr, who, x, y, t, **k)
        if not (who == "kid_d" and t >= olivia_up):
            desk(cr, x if who != "kid_d" else OLIVIA[1], 12320 + i * 10)
        elif who == "kid_d":
            desk(cr, OLIVIA[1], 12320 + i * 10)
    if t >= olivia_up:   # dropped crutches on the floor
        line(cr, [(OLIVIA[1] + 20, 915), (OLIVIA[1] + 150, 905)], 6, hexc("#a9a2ae"), seed=12330, amp=0.2)
        line(cr, [(OLIVIA[1] + 30, 925), (OLIVIA[1] + 160, 918)], 6, hexc("#a9a2ae"), seed=12331, amp=0.2)
    # ---- flashback bubbles
    if A("c5", "stealing") <= t < A("c6"):
        bubble(cr, 420, 520, 260, 170, (TYLER[1], 700), [("", INK)], s=pop(t, A("c5", "stealing"), 0.2), thought=True)
        with at(cr, 420, 520, 1.0):
            shape(cr, rrect_pts(-50, -70, 100, 140, 10, 14), INK, seed=12340, amp=0.4, lw=3)
            shape(cr, rrect_pts(-40, -58, 80, 116, 6, 14), hexc("#dff5e3"), seed=12341, amp=0.3, lw=0, stroke=None)
            if t >= A("c5", "online"):
                write(cr, [("SOLD!", GREEN)], 0, 12, 26, align="center", bold=True)
    if A("c7", "tells") <= t < A("c8"):
        bubble(cr, 400, 520, 280, 130, (EMMA[1], 690), [("psst... secrets", PURPLE)], s=pop(t, A("c7", "tells"), 0.2),
               size=34)
    if A("c12", "Miller") <= t < A("c13"):
        bubble(cr, 640, 480, 280, 190, (JAKE[1], 690), [("", INK)], s=pop(t, A("c12", "Miller"), 0.2), thought=True)
        with at(cr, 640, 480, 1.0):
            shape(cr, rrect_pts(-60, -30, 120, 80, 10, 14), hexc("#8e5a2e"), seed=12350, amp=0.5, lw=3.5)
            shape(cr, rrect_pts(-30, -64, 60, 60, 3, 10), WHITE, seed=12351, amp=0.3, lw=2.5)
            write(cr, [("ANSWERS", RED)], 0, -30, 14, align="center", bold=True)
            if t >= A("c12", "fired"):
                write(cr, [("FIRED", RED)], 0, 30, 34, align="center", bold=True)
    # ---- headlines
    hl(cr, t, [("\"The principal ", INK), ("SAW", RED), ("\"", INK)], 215, 70, A("c3", "principal"),
       end=A("c3", "confess") - 0.05, bold=True)
    hl(cr, t, [("confess = ", INK), ("SAVED", GREEN)], 215, 84, A("c3", "confess"), end=A("c4") - 0.05, bold=True)
    stamp(cr, t, A("c4"), "4 MIN LATER", dur=0.8, y=470)
    hl(cr, t, [("the ", INK), ("THIEF", RED)], 215, 96, A("c6", "thief"), end=A("c7") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("SNITCH", PURPLE)], 215, 96, A("c7", "tells"), end=A("c9") - 0.05, bold=True)
    stamp(cr, t, A("c9"), "3 MIN LATER", dur=0.8, y=470)
    hl(cr, t, [("FAKE", RED), (" broken leg", INK)], 215, 80, A("c10", "faked"), end=A("c11") - 0.05, bold=True)
    hl(cr, t, [("he got a teacher ", INK), ("FIRED", RED)], 215, 60, A("c12", "put"), end=A("c13") - 0.05, bold=True)
    hl(cr, t, [("\"WHOSE is ", INK), ("THIS", RED), ("?\"", INK)], 215, 80, A("c13", "belong"), bold=True)


def scene_reveal(cr, t, tl):
    A = tl.at
    candy = A("c14", "candy")
    cr.set_source_rgba(*(hexc("#ffd0e0") if t >= candy else hexc("#fbf3e1")))
    cr.paint()
    for k in range(20):
        a = k * math.pi / 10 + t * 0.4
        cr.move_to(360, 620)
        cr.arc(360, 620, 1400, a, a + math.pi / 20)
        cr.close_path()
        cr.set_source_rgba(*hexc("#f7d774" if t < candy else "#f5a3b5", 0.45))
        cr.fill()
    z = camera(t, [(A("c14") - 0.2, (1.4,)), (A("c14", "leans"), (2.0,)), (A("c14", "and"), (1.6,)), (candy, (2.6,))],
               dur=0.15)[0]
    cig_pack(cr, 360, 640, z, rot=0.05 * math.sin(t * 3), candy=t >= candy, seed=12400)
    if t >= candy:
        cue("hit", t, candy)
    hl(cr, t, [("CANDY", PINK), (" cigarettes", INK)], 215, 84, candy, bold=True, underline=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("c15") - 0.2, WIDE), (A("c15", "pack"), (2.0, 180, 720)), (A("c15", "candy"), (1.4, 200, 740)),
            (A("c15", "exposed"), ROW), (A("c15", "entire"), (1.6, 600, 760)), (A("c15", "every"), (1.3, 400, 760)),
            (A("c15", "suspended"), (1.0, 480, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    person(cr, "teacher", TX, 900, t, facing=1, arms=("face", "hip"), eyes="closed", mouth="flat")
    cig_pack(cr, TX + 70, 700, 0.5, candy=True, seed=12500)
    for i, (who, x) in enumerate(KIDS):
        person(cr, who, x, 900 - 36, t, facing=-1, eyes="sad", mouth="wobble", sweat=True)
        desk(cr, x, 12510 + i * 10)
    if t >= A("c15", "suspended"):
        stamp(cr, t, A("c15", "suspended"), "SUSPENDED", dur=1.4, y=470)
    hl(cr, t, [("exposed by ", INK), ("CANDY", PINK)], 215, 80, A("c15", "exposed"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"trash": scene_trash, "cctv": scene_cctv, "class": scene_class, "reveal": scene_reveal, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
