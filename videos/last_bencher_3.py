"""Episode 21: "The Last Bencher Meets His Match" — Part 3 of the trick-riddle series.

The teacher is off sick. The last bencher tries his riddles on the substitute, Mr. Carter, who answers every one
instantly: the tallest mountain before Everest was discovered (still Everest), how many times you can subtract 10 from
100 (once), and Emma's mom's fourth kid (Emma). The twist: the substitute sat in that same last seat twenty years ago,
and his initials have been carved into the kid's desk since the first shot.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import (BOARD, CHALK, CHALK_B, CHALK_P, CHALK_Y, CX, KID, KIDS, ROW, TEACH, TX, WIDE, big_q,
                                board, classroom, desk, stick)

NARRATOR = dict(speed=1.0)
TAIL = 1.0

SCRIPT = [
    dict(id="s1", scene="class",
         text="The teacher is sick today. A substitute walks in. And the last bencher smiles."),
    dict(id="s2", scene="class", text="I'm Mister Carter. Any questions?", speaker="sub"),
    dict(id="s3", scene="everest",
         text="Sir, before Mount Everest was discovered, what was the tallest mountain in the world?",
         speaker="chotu"),
    dict(id="s4", scene="everest2", text="Mount Everest. It was still the tallest. Nobody had found it yet.",
         speaker="sub"),
    dict(id="s5", scene="class", text="The last bencher blinks. Okay. Lucky guess.", speaker="chotu",
         speaker_from="okay"),
    dict(id="s6", scene="subtract", text="How many times can you subtract [ten|10] from [a hundred?|100?]",
         speaker="chotu"),
    dict(id="s7", scene="subtract2", text="Once. After that, you're subtracting from [ninety.|90.]", speaker="sub"),
    dict(id="s8", scene="class", text="The class goes quiet. Nobody has ever beaten him."),
    dict(id="s9", scene="kids",
         text="Emma's mom has four kids. April, May, June... What's the fourth one called?", speaker="chotu"),
    dict(id="s10", scene="kids2", text="Emma. Sit down.", speaker="sub"),
    dict(id="s11", scene="class", text="Sir... how do you know all of these?", speaker="chotu"),
    dict(id="s12", scene="class", text="Because [twenty years|20 years] ago, I sat in that exact seat.",
         speaker="sub", gap=0.25),
    dict(id="s13", scene="desk", text="Carved into that desk: his initials. The last bencher just met the original.",
         gap=0.2),
]

METADATA = dict(
    title="The Last Bencher Finally Met His Match 😳 (Trick Riddles Part 3)",
    alt_titles=["He Tried His Riddles on the Substitute… Big Mistake 😂", "The Substitute Knew EVERY Riddle 😳"],
    description="""The teacher is sick. A substitute walks in… and the last bencher thinks it's going to be easy. 😏

Riddle 1: Before Mount Everest was discovered, what was the tallest mountain in the world?
Riddle 2: How many times can you subtract 10 from 100?
Riddle 3: Emma's mom has four kids: April, May, June… what's the fourth one called?

The substitute answers every single one. Then we find out why. 👀 (Look at the desk in the first few seconds.)

💬 How many did you get before the substitute did?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Riddles", "#LastBencher", "#PlotTwist"],
    tags=["last bencher", "backbenchers", "riddles", "trick questions", "substitute teacher", "teacher vs student",
          "funny riddles", "brain teaser", "plot twist", "school jokes", "trick riddles part 3", "interestingly strange"],
    pinned_comment="Did you spot the initials on the desk before the reveal? 👀 Rewatch the first 3 seconds 😳",
)

BLUE = hexc("#3f6fb5")
CARVE = hexc("#6d4524")
RED_CHALK = hexc("#ff6b6b")
DESK_Y = 838                 # front panel of the desks, where the initials are carved


def carving(cr, x, size=17):
    write(cr, [("R.C. '06", CARVE)], x, DESK_Y + size * 0.45, size, align="center", bold=True)
    line(cr, [(x - size * 2.3, DESK_Y + size * 0.75), (x + size * 2.3, DESK_Y + size * 0.7)], max(1.5, size / 9),
         CARVE, seed=9001, amp=0.3)


def sub_board(cr):
    """Cover the old lesson with the substitute's name."""
    shape(cr, rrect_pts(-170, 420, 400, 220, 6, 20), BOARD, seed=9010, amp=0.3, lw=0, stroke=None)
    write(cr, [("Mr. R. Carter", CHALK)], 30, 500, 40, align="center")
    write(cr, [("(substitute)", CHALK_Y)], 30, 560, 30, align="center")


def scene_class(cr, t, tl):
    A = tl.at
    keys = [(0, (2.2, CX, 760)), (A("s1", "sick"), (1.5, 300, 760)), (A("s1", "substitute"), (1.2, 200, 760)),
            (A("s1", "walks"), TEACH), (A("s1", "last"), (1.6, 600, 770)), (A("s1", "bencher"), KID),
            (A("s1", "smiles"), (2.4, 830, 720)),
            (A("s2") - 0.1, TEACH), (A("s2", "carter"), (2.2, 130, 740)), (A("s2", "questions"), WIDE),
            (A("s5") - 0.1, KID), (A("s5", "blinks"), (2.5, 830, 715)), (A("s5", "okay"), (1.9, 800, 740)),
            (A("s5", "lucky"), (2.2, 820, 730)),
            (A("s8") - 0.1, WIDE), (A("s8", "quiet"), ROW), (A("s8", "nobody"), (1.7, 180, 760)),
            (A("s8", "beaten"), (2.3, 130, 735)),
            (A("s11") - 0.1, KID), (A("s11", "know"), (2.3, 825, 720)),
            (A("s12") - 0.1, TEACH), (A("s12", "20"), (2.2, 130, 735)), (A("s12", "sat"), (1.2, 480, 770)),
            (A("s12", "exact"), (1.8, 760, 770)), (A("s12", "seat"), (2.6, CX, 800))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t)
    if t >= A("s2"):
        sub_board(cr)
    # ---- the substitute walks in
    arrive = ease_out(seg(t, A("s1", "substitute"), A("s1", "walks", end=True) + 0.3))
    s = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    if arrive < 1:
        s.update(walk=t * 1.8)
    if A("s2") <= t < A("s3"):
        s.update(arms=("wave", "hip"), eyes="happy", mouth="grin")
    if A("s5") <= t < A("s6") or A("s8") <= t < A("s9"):
        s.update(arms=("hip", "hip"), eyes="sly", mouth="smirk")
    if A("s11") <= t < A("s12"):
        s.update(arms=("chin", "hip"), eyes="sly", mouth="smirk")
    if A("s12") <= t:
        s.update(arms=("point", "hip"), eyes="happy", mouth="grin")
    if tl.speaking("sub", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "smile"
    if t >= A("s1", "substitute") - 0.05:
        person(cr, "sub", lerp(-140, TX, arrive), 900, t, **s)
    # ---- kids
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if A("s8") <= t < A("s9") or A("s11") <= t:
            k.update(eyes="wide", mouth="o")
        if A("s12", "seat") <= t and who != "chotu":
            k.update(arms=("point", "hip"))
        if who == "chotu":
            stand = seg(t, A("s1", "smiles") - 0.1, A("s1", "smiles") + 0.15)
            y -= 36 * stand
            if A("s1", "smiles") <= t < A("s3"):
                k.update(eyes="sly", mouth="smirk", arms=("cheer", "hip"))
            if A("s5") <= t < A("s6"):
                k.update(eyes="wide", mouth="o", arms=("hip", "hip"))
                if t >= A("s5", "okay"):
                    k.update(eyes="sly", mouth="flat", arms=("chin", "hip"))
            if A("s8") <= t < A("s9"):
                k.update(eyes="wide", mouth="wobble", sweat=True)
            if A("s11") <= t:
                k.update(eyes="wide", mouth="wobble", sweat=True, arms=("down", "down"))
            if A("s12", "seat") <= t:
                k.update(shake=1.2)
            if tl.speaking("chotu", t):
                k["mouth"] = "o" if int(t * 12) % 2 else "smirk"
        person(cr, who, x, y, t, **k)
        desk(cr, x, 4200 + i * 10)
    carving(cr, CX)                       # there from the very first frame
    if A("s12", "seat") <= t:
        blob(cr, CX, DESK_Y + 4, 64, 26, None, seed=9020, amp=1.0, lw=4, stroke=RED)
    # ---- screen text
    hl(cr, t, [("SUBSTITUTE", BLUE), (" teacher", INK)], 215, 66, A("s1", "substitute"), end=A("s1", "bencher"),
       bold=True)
    hl(cr, t, [("the ", INK), ("LAST BENCHER", RED), (" smiles", INK)], 215, 58, A("s1", "bencher"),
       end=A("s2") - 0.05, bold=True)
    hl(cr, t, [("\"Any questions?\"", BLUE)], 215, 70, A("s2", "questions"), end=A("s3") - 0.05, bold=True)
    hl(cr, t, [("\"Lucky guess.\"", INK)], 215, 74, A("s5", "lucky"), end=A("s6") - 0.05, bold=True)
    hl(cr, t, [("nobody has ever ", INK), ("BEATEN", RED), (" him", INK)], 215, 54, A("s8", "nobody"),
       end=A("s9") - 0.05, bold=True)
    hl(cr, t, [("\"How do you ", INK), ("KNOW", RED), (" all these?\"", INK)], 215, 52, A("s11"),
       end=A("s12") - 0.05, bold=True)
    hl(cr, t, [("20 YEARS AGO", RED), ("...", INK)], 215, 70, A("s12", "20"), end=A("s12", "exact") - 0.05,
       bold=True)
    hl(cr, t, [("\"...in that ", INK), ("EXACT SEAT", RED), (".\"", INK)], 215, 62, A("s12", "exact"), bold=True,
       underline=True)
    for w in (A("s5", "blinks"), A("s12", "seat")):
        cue("hit", t, w)


# ------------------------------------------------------------------ chalkboard riddles
def mountain(cr, x, base, h, w, col, seed, snow=True):
    pk = (x, base - h)
    line(cr, [(x - w / 2, base), pk, (x + w / 2, base)], 5, col, seed=seed, amp=0.6)
    if snow:
        line(cr, [(x - w * 0.12, base - h * 0.78), (x - w * 0.04, base - h * 0.72), (x + 0.03 * w, base - h * 0.8),
                  (x + w * 0.12, base - h * 0.76)], 4, WHITE, seed=seed + 1, amp=0.4)


def cloud(cr, x, y, s, alpha=1.0, seed=0):
    for k in range(5):
        blob(cr, x - 120 * s + k * 60 * s, y + (k % 2) * 20 * s, 70 * s, 50 * s, hexc("#f4f1e6", 0.95 * alpha),
             seed=seed + k, amp=0.8, lw=3, stroke=hexc("#9aa5a0", alpha))


def scene_everest(cr, t, tl, part):
    A = tl.at
    base = 1150
    if part == 1:
        keys = [(A("s3") - 0.2, (1.15, 360, 860)), (A("s3", "mount"), (0.95, 360, 860)), (A("s3", "everest"), (1.25, 450, 760)),
                (A("s3", "discovered"), (1.05, 420, 800)), (A("s3", "tallest"), (0.95, 360, 860)),
                (A("s3", "world?"), (1.2, 260, 940))]
        cover = 1.0
    else:
        keys = [(A("s4") - 0.2, (0.95, 360, 860)), (A("s4", "everest"), (1.25, 460, 720)), (A("s4", "still"), (0.95, 360, 860)),
                (A("s4", "nobody"), (1.3, 450, 700)), (A("s4", "yet"), (1.05, 380, 840))]
        cover = 1.0 - ease_out(seg(t, A("s4", "everest") - 0.1, A("s4", "everest") + 0.4))
    board(cr, t, keys)
    line(cr, [(-300, base), (1100, base)], 5, CHALK, seed=9100, amp=0.8)
    mountain(cr, 130, base, 380, 300, CHALK_B, 9110)
    mountain(cr, 300, base, 300, 260, CHALK, 9120)
    mountain(cr, 480, base, 620, 400, CHALK_Y, 9130)       # Everest
    if part == 1 and t >= A("s3", "tallest"):
        for k, (x, h) in enumerate(((130, 380), (300, 300))):
            write(cr, [("?", CHALK_P)], x, base - h - 30, 60, align="center", bold=True)
    if cover > 0:
        cloud(cr, 480, base - 560, 1.4, cover, seed=9140)
        write(cr, [("not found yet", hexc("#5a6662", cover))], 480, base - 520, 34, align="center", bold=True)
    if part == 2:
        if t >= A("s4", "everest"):
            write(cr, [("EVEREST", CHALK_Y)], 480, base - 660, 52, align="center", bold=True)
            write(cr, [("8,849 m", CHALK)], 480, base - 610, 34, align="center")
            cue("whoosh", t, A("s4", "everest") - 0.1)
        if t >= A("s4", "still"):
            stamp(cr, t, A("s4", "still"), "STILL THE TALLEST", dur=0.7, y=330)
        hl(cr, t, [("\"Mount ", INK), ("EVEREST", BLUE), (".\"", INK)], 215, 74, A("s4", "everest"),
           end=A("s4", "still") - 0.05, bold=True)
        hl(cr, t, [("nobody had ", INK), ("found it", RED), (" yet", INK)], 215, 62, A("s4", "nobody"), bold=True)
    else:
        big_q(cr, t, A("s3", "world?"), 600, 520, 130)
        hl(cr, t, [("before ", INK), ("EVEREST", RED), (" was discovered", INK)], 215, 52, A("s3", "everest"),
           end=A("s3", "tallest") - 0.05, bold=True)
        hl(cr, t, [("what was the ", INK), ("TALLEST", RED), ("?", INK)], 215, 66, A("s3", "tallest"), bold=True)


def scene_subtract(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("s6") - 0.2, (1.0, 360, 760)), (A("s6", "times"), (1.6, 310, 700)), (A("s6", "subtract"), (1.0, 360, 780)),
                (A("s6", "10"), (1.7, 330, 690)), (A("s6", "100?"), (1.05, 360, 820))]
    else:
        keys = [(A("s7") - 0.2, (1.7, 360, 580)), (A("s7", "after"), (1.0, 360, 760)), (A("s7", "subtracting"), (1.35, 330, 840)),
                (A("s7", "90."), (1.0, 360, 800))]
    board(cr, t, keys)
    if part == 1:
        with at(cr, 200, 640, max(0.85, pop(t, A("s6"), 0.25))):
            write(cr, [("100", CHALK_Y)], 0, 40, 120, align="center", bold=True)
        if t >= A("s6", "subtract"):
            write(cr, [("- 10", CHALK_P)], 420, 680, 120, align="center", bold=True)
        if t >= A("s6", "times"):
            for k in range(4):   # the obvious guess: again and again
                if t >= A("s6", "times") + k * 0.15:
                    write(cr, [("- 10", hexc("#f4f1e6", 0.5))], 160 + k * 120, 860, 50, align="center", bold=True)
        big_q(cr, t, A("s6", "100?"), 360, 1100, 140)
        hl(cr, t, [("how many times? ", INK), ("100 - 10", RED)], 215, 58, A("s6", "times"), bold=True)
    else:
        write(cr, [("100", CHALK_Y)], 200, 680, 120, align="center", bold=True)
        write(cr, [("- 10", CHALK_P)], 420, 680, 120, align="center", bold=True)
        if A("s7") <= t < A("s7", "subtracting"):
            with at(cr, 360, 520, max(0.85, pop(t, A("s7"), 0.25)), rot=-0.06):
                write(cr, [("ONCE", RED_CHALK)], 0, 0, 90, align="center", bold=True)
            cue("hit", t, A("s7"))
        if t >= A("s7", "subtracting"):
            k = seg(t, A("s7", "subtracting"), A("s7", "subtracting") + 0.3)
            line(cr, [(110, 650), (110 + 180 * k, 650)], 9, RED_CHALK, seed=9200, amp=0.4)   # strike the 100
            write(cr, [("90", CHALK_B)], 300, 880, 150, align="center", bold=True)
            write(cr, [("- 10", hexc("#f4f1e6", 0.6))], 500, 880, 60, align="center", bold=True)
            write(cr, [("not 100 anymore!", CHALK)], 360, 960, 40, align="center")
        hl(cr, t, [("\"", INK), ("ONCE", BLUE), (".\"", INK)], 215, 90, A("s7"), end=A("s7", "subtracting") - 0.05,
           bold=True)
        hl(cr, t, [("then it's ", INK), ("90", RED)], 215, 84, A("s7", "subtracting"), bold=True)


def scene_kids(cr, t, tl, part):
    A = tl.at
    names = ["APRIL", "MAY", "JUNE", "?"]
    xs = [120, 280, 440, 600]
    if part == 1:
        keys = [(A("s9") - 0.2, (1.0, 360, 820)), (A("s9", "mom"), (1.5, 360, 660)), (A("s9", "four"), (1.0, 360, 880)),
                (A("s9", "april"), (1.6, 200, 960)), (A("s9", "may"), (1.0, 360, 900)),
                (A("s9", "june"), (1.6, 440, 960)), (A("s9", "fourth"), (1.0, 360, 900)),
                (A("s9", "called?"), (1.7, 560, 960))]
    else:
        keys = [(A("s10") - 0.2, (1.0, 360, 900)), (A("s10"), (1.8, 560, 960)), (A("s10", "sit"), (1.0, 360, 880))]
    board(cr, t, keys)
    # mom, with the name tag everyone skips over
    sc = 0.0 if (part == 2 or t >= A("s9", "april")) else pop(t, A("s9", "mom"), 0.25)
    if sc > 0:
        with at(cr, 360, 720, sc):
            stick(cr, 0, 0, 2.4, arms_up=False, seed=9300, col=CHALK_P)
            blob(cr, 0, -183, 44, 18, None, seed=9301, amp=0.5, lw=3.5, stroke=CHALK_P)
            write(cr, [("EMMA'S MOM", CHALK_P)], 0, 60, 44, align="center", bold=True)
    for k, (nm, x) in enumerate(zip(names, xs)):
        key = ["april", "may", "june", "fourth"][k]
        start = A("s9", key) if part == 1 else -1
        sc = pop(t, start, 0.25) if part == 1 else 1.0
        if sc <= 0:
            continue
        with at(cr, x, 1000, sc):
            stick(cr, 0, 0, 1.9, arms_up=(k == 3 and part == 2), seed=9310 + k * 7,
                  col=CHALK_Y if k < 3 else CHALK_B)
        label = nm
        if k == 3 and part == 2:
            label = "EMMA"
        write(cr, [(label, RED_CHALK if (k == 3 and part == 2) else CHALK)], x, 1060, 40 if k < 3 else 54,
              align="center", bold=True)
    if part == 1:
        if t >= A("s9", "june"):   # the pattern everybody expects
            write(cr, [("JULY?", hexc("#f4f1e6", 0.55))], xs[3], 830, 40, align="center", bold=True)
        hl(cr, t, [("EMMA'S", RED), (" mom has 4 kids", INK)], 215, 58, A("s9", "mom"), end=A("s9", "april") - 0.05,
           bold=True)
        hl(cr, t, [("April, May, June... ", INK), ("?", RED)], 215, 62, A("s9", "april"), bold=True)
    else:
        line(cr, [(xs[3] - 60, 830), (xs[3] + 60, 810)], 7, RED_CHALK, seed=9330, amp=0.3)   # cross out July
        write(cr, [("JULY?", hexc("#f4f1e6", 0.35))], xs[3], 830, 40, align="center", bold=True)
        cue("hit", t, A("s10"))
        hl(cr, t, [("\"", INK), ("EMMA", RED), (". Sit down.\"", INK)], 215, 76, A("s10"), bold=True)


def scene_desk(cr, t, tl):
    A = tl.at
    keys = [(A("s13") - 0.2, (5.0, CX, DESK_Y - 4)), (A("s13", "initials"), (6.2, CX, DESK_Y - 2)),
            (A("s13", "last"), (1.5, 520, 770)), (A("s13", "original"), (2.0, 300, 740))]
    set_camera(camera(t, keys))
    enter_world(cr)
    classroom(cr, t)
    sub_board(cr)
    late = t >= A("s13", "last")
    person(cr, "sub", TX + 60, 900, t, facing=1, arms=("thumb", "hip") if late else ("hip", "hip"),
           eyes="happy" if late else "sly", mouth="grin")
    for i, (who, x) in enumerate(KIDS):
        if who == "chotu":
            person(cr, who, x, 900, t, facing=-1, eyes="wide", mouth="o", sweat=True, arms=("face", "down"))
        else:
            person(cr, who, x, 900, t, facing=-1, eyes="happy" if late else "dot", mouth="grin" if late else "o")
        desk(cr, x, 4200 + i * 10)
    carving(cr, CX)
    if t >= A("s13", "initials"):
        blob(cr, CX, DESK_Y + 4, 64, 26, None, seed=9020, amp=1.0, lw=3, stroke=RED)
    hl(cr, t, [("R.C.", RED), (" = Mr. ", INK), ("R.", RED), (" Carter", INK)], 215, 70, A("s13", "initials"),
       end=A("s13", "original") - 0.05, bold=True)
    hl(cr, t, [("He met the ", INK), ("ORIGINAL", RED)], 215, 70, A("s13", "original"), bold=True, underline=True)
    cue("hit", t, A("s13", "original"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "everest":
        scene_everest(cr, t, tl, 1)
    elif name == "everest2":
        scene_everest(cr, t, tl, 2)
    elif name == "subtract":
        scene_subtract(cr, t, tl, 1)
    elif name == "subtract2":
        scene_subtract(cr, t, tl, 2)
    elif name == "kids":
        scene_kids(cr, t, tl, 1)
    elif name == "kids2":
        scene_kids(cr, t, tl, 2)
    elif name == "desk":
        scene_desk(cr, t, tl)
    else:
        scene_class(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
