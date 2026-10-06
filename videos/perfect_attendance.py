"""Episode 18: "Perfect Attendance" — an original school twist story (same class as Who Is Kevin?, The Excuses).

Jake wins a 3-year perfect attendance award. His secret: an identical twin, Jack; they take turns. The principal asks
who gets the award... and then Mr. Miller confesses he has a twin too.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="p1", scene="stage",
         text="Jake just won an award. [Three years|3 years] of perfect attendance. Not one day missed."),
    dict(id="p2", scene="stage", text="The principal hands him the trophy: so Jake, what's your secret?",
         speaker="oldman", speaker_from="so"),
    dict(id="p3", scene="stage", text="Jake leans into the mic. Honestly, sir? My brother.", speaker="jake",
         speaker_from="honestly", gap=0.25),
    dict(id="p4", scene="stage", text="The curtain opens. And there's another Jake. His identical twin, Jack.", gap=0.25),
    dict(id="p5", scene="stage", text="We take turns. I come Monday, he comes Tuesday. Nobody ever noticed.",
         speaker="jack"),
    dict(id="p6", scene="stage",
         text="The whole school gasps. The principal turns red: so which one of you gets the award?",
         speaker="oldman", speaker_from="so"),
    dict(id="p7", scene="stage", text="Both twins point at each other.", gap=0.2),
    dict(id="p8", scene="stage", text="Then Mr. Miller starts laughing. Relax, kids. I have a confession too.",
         speaker="teacher", speaker_from="relax", gap=0.25),
    dict(id="p9", scene="stage", text="And through the side door walks, another Mr. Miller.", gap=0.25),
    dict(id="p10", scene="stage", text="Why do you think you only learned half the syllabus?", speaker="teacher2",
         gap=0.25),
]

METADATA = dict(
    title="He Never Missed a Day of School… His Secret Was Genius 😂",
    alt_titles=["3 Years of Perfect Attendance… With a Twin 😳", "The Twins Fooled the Whole School… Then the Teacher 💀"],
    description="""Jake won a trophy for 3 years of perfect attendance. Not one day missed. 🏆

When the principal asked for his secret, the curtain opened… and there was ANOTHER Jake. 😳

Then the teacher said he had a confession too… 👀

💬 Would you swap places with your twin for a week? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#Twins", "#School"],
    tags=["plot twist", "twins", "identical twins", "school story", "perfect attendance", "funny story",
          "twist ending", "storytime", "animated story", "interestingly strange"],
    pinned_comment="Plot twist: Mr. Miller's twin teaches math… or does he? 😂👇",
)

GOLD = hexc("#f2b632")
CURTAIN = hexc("#b8252e")
CURTAIN_D = hexc("#8e1c24")
BLUE = hexc("#3f6fb5")
GREEN = hexc("#3d8f45")
JX, JACKX, PX, TX, T2X = 330, 520, 150, -140, 700   # stage positions (world)


def stage_set(cr, t, curtain_open):
    cr.set_source_rgba(*hexc("#3a2230"))
    cr.paint()
    # back wall + banner
    shape(cr, rrect_pts(-300, 330, 1300, 580, 6, 20), hexc("#5a3140"), seed=15000, amp=0.6, lw=4)
    shape(cr, rrect_pts(80, 360, 560, 90, 10, 20), GOLD, seed=15001, amp=0.6, lw=4)
    write(cr, [("AWARDS DAY", CURTAIN)], 360, 422, 56, align="center", bold=True)
    # stage floor
    sharp_shape(cr, [(-900, 900), (1700, 900), (1700, 1000), (-900, 1000)], hexc("#b0773f"), seed=15002, amp=0.6, lw=4)
    for k in range(-8, 18):
        line(cr, [(k * 90, 900), (k * 90 - 20, 1000)], 3, hexc("#8e5a2e"), seed=15003 + k, amp=0.3)
    # curtains (centre pair opens to reveal the twin)
    u = ease_out(curtain_open)
    for side in (-1, 1):
        x0 = 520 + side * (20 + 220 * u)
        pts = [(x0, 330), (x0 + side * 240, 330), (x0 + side * 240, 900), (x0, 900)]
        sharp_shape(cr, pts, CURTAIN, seed=15010 + side, amp=0.8, lw=4)
        for k in range(4):
            xx = x0 + side * (40 + k * 55)
            line(cr, [(xx, 340), (xx + side * 8, 890)], 4, CURTAIN_D, seed=15020 + side * 10 + k, amp=0.6)
    # outer drapes
    for x0, x1 in ((-400, -250), (970, 1120)):
        sharp_shape(cr, [(x0, 250), (x1, 250), (x1 - 40, 1000), (x0, 1000)], CURTAIN, seed=15030 + x0, amp=0.8, lw=4)
    shape(cr, rrect_pts(-400, 250, 1520, 80, 10, 20), CURTAIN, seed=15040, amp=0.8, lw=4)
    # side door (stage left)
    shape(cr, rrect_pts(760, 620, 150, 280, 6, 16), hexc("#6b4a2e"), seed=15050, amp=0.5, lw=4)
    dot(cr, 890, 770, 6, GOLD)


def podium(cr, x):
    """A mic stand beside the award winner."""
    line(cr, [(x, 900), (x, 720)], 5, INK, seed=15101, amp=0.2)
    line(cr, [(x - 30, 900), (x + 30, 900)], 6, INK, seed=15103, amp=0.2)
    line(cr, [(x, 720), (x - 30, 700)], 4, INK, seed=15104, amp=0.2)
    blob(cr, x - 36, 694, 12, 16, hexc("#555a66"), seed=15102, amp=0.3, lw=3)


def trophy(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        shape(cr, [(-40, -90), (40, -90), (26, -30), (-26, -30)], GOLD, seed=15110, amp=0.5, lw=4)
        for sd in (-1, 1):
            blob(cr, sd * 48, -70, 14, 18, None, seed=15111 + sd, amp=0.3, lw=5, stroke=GOLD)
        shape(cr, rrect_pts(-10, -30, 20, 24, 3, 8), GOLD, seed=15113, amp=0.3, lw=3)
        shape(cr, rrect_pts(-30, -8, 60, 14, 3, 10), hexc("#6b4a2e"), seed=15114, amp=0.3, lw=3)


def audience(cr, t, gasp):
    for k in range(12):
        x = -120 + k * 90
        bob = abs(math.sin(t * 9 + k)) * 10 if gasp else 0
        blob(cr, x, 1110 - bob, 40, 44, hexc("#2b1c24"), seed=15200 + k, amp=0.6, lw=0, stroke=None)
        blob(cr, x, 1200 - bob, 60, 50, hexc("#2b1c24"), seed=15220 + k, amp=0.6, lw=0, stroke=None)


def tag(cr, x, y, name, col):
    shape(cr, rrect_pts(x - 44, y - 18, 88, 36, 8, 10), WHITE, seed=15300 + x, amp=0.4, lw=3)
    write(cr, [(name, col)], x, y + 10, 24, align="center", bold=True)


def talk(tl, who, t, rest="smile"):
    return ("o" if int(t * 12) % 2 else rest) if tl.speaking(who, t) else rest


def scene_stage(cr, t, tl):
    A = tl.at
    opened = seg(t, A("p4", "curtain"), A("p4", "opens", end=True) + 0.2)
    gasp = A("p6") <= t < A("p6", "principal")
    keys = [(0, (1.6, 330, 740)), (A("p1", "award"), (1.2, 360, 700)), (A("p1", "3"), (1.6, 360, 560)),
            (A("p1", "perfect"), (1.1, 360, 700)), (A("p1", "not"), (2.0, 330, 720)),
            (A("p2"), (1.4, 240, 740)), (A("p2", "trophy"), (1.8, 260, 700)), (A("p2", "secret"), (2.1, 180, 720)),
            (A("p3", "leans"), (2.2, 360, 700)), (A("p3", "honestly"), (1.8, 340, 720)), (A("p3", "brother"), (2.5, 330, 720)),
            (A("p4", "curtain"), (1.0, 440, 700)), (A("p4", "another"), (1.6, 520, 720)), (A("p4", "identical"), (1.2, 430, 720)),
            (A("p4", "Jack"), (2.2, 520, 720)),
            (A("p5", "turns"), (1.3, 430, 720)), (A("p5", "Monday"), (2.0, 330, 720)), (A("p5", "Tuesday"), (2.0, 520, 720)),
            (A("p5", "nobody"), (1.1, 430, 760)), (A("p6", "gasps"), (0.8, 400, 820)), (A("p6", "red"), (2.2, 150, 720)),
            (A("p6", "which"), (1.3, 300, 720)), (A("p6", "award"), (1.6, 430, 640)), (A("p7", "twins"), (1.5, 430, 720)),
            (A("p7", "point"), (2.0, 430, 700)),
            (A("p8"), (1.2, 100, 740)), (A("p8", "laughing"), (2.0, -120, 730)), (A("p8", "relax"), (1.5, -60, 740)),
            (A("p8", "confession"), (2.2, -130, 730)), (A("p9", "door"), (1.4, 780, 740)), (A("p9", "another"), (2.0, 720, 730)),
            (A("p9", "Miller"), (1.1, 300, 740)), (A("p10", "half"), (2.2, 690, 730)), (A("p10", "syllabus"), (0.9, 300, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    stage_set(cr, t, opened)
    # Jack behind the curtain
    if opened > 0:
        j = dict(facing=-1, arms=("wave", "hip"), eyes="happy", mouth=talk(tl, "jack", t, "grin"))
        if A("p7", "point") <= t:
            j.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
        if t >= A("p9"):
            j.update(eyes="wide", mouth="o")
        person(cr, "chotu", JACKX, 900, t, **j)
        tag(cr, JACKX, 640, "JACK", BLUE)
    podium(cr, JX + 110)
    # Jake
    k = dict(facing=1, arms=("hold", "hip") if A("p2", "trophy") <= t < A("p7") else ("hip", "hip"), eyes="happy",
             mouth=talk(tl, "jake", t, "grin"))
    if A("p6", "red") <= t < A("p7"):
        k.update(eyes="wide", mouth="o", sweat=True)
    if A("p7", "point") <= t:
        k.update(arms=("point", "hip"), eyes="sly", mouth="smirk", facing=1)
    if t >= A("p9"):
        k.update(eyes="wide", mouth="o")
    person(cr, "chotu", JX, 900, t, **k)
    tag(cr, JX, 640, "JAKE", RED)
    if A("p2", "trophy") <= t < A("p7"):
        trophy(cr, JX + 62, 872, 0.7)
    # principal
    p = dict(facing=1, arms=("give", "hip") if A("p2", "hands") <= t < A("p2", "trophy", end=True) + 0.3 else ("hip", "hip"),
             eyes="dot", mouth=talk(tl, "oldman", t, "smile"))
    if t >= A("p5"):
        p.update(eyes="wide", mouth=talk(tl, "oldman", t, "o"))
    person(cr, "oldman", PX, 905, t, **p)
    if A("p6", "red") <= t < A("p8"):
        blob(cr, PX + 6, 905 - 26 - 100 - 40 + 12, 36, 32, hexc("#e53935", 0.4), seed=15400, amp=0.4, lw=0, stroke=None)
    # Mr. Miller (and his twin)
    m = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth=talk(tl, "teacher", t, "smile"))
    if A("p8", "laughing") <= t < A("p8", "relax"):
        m.update(eyes="closed", mouth="laugh", jump=abs(math.sin(t * 9)) * 8)
    if t >= A("p9"):
        m.update(arms=("thumb", "hip"), eyes="sly", mouth="smirk")
    person(cr, "teacher", TX, 905, t, **m)
    if t >= A("p9", "door"):
        walk = seg(t, A("p9", "door"), A("p9", "Miller", end=True))
        person(cr, "teacher", lerp(840, T2X, walk), 905, t, facing=-1, walk=t * 2.5 if walk < 1 else None,
               arms=("wave", "hip") if walk >= 1 else ("hip", "hip"), eyes="sly",
               mouth=talk(tl, "teacher2", t, "smirk"))
        if walk >= 1:
            tag(cr, T2X, 620, "MILLER 2", GREEN)
    audience(cr, t, gasp or A("p9", "Miller") <= t < A("p10"))
    if t >= A("p1", "award") and t < A("p2"):
        confetti(cr, t, A("p1", "award"))
    # headlines
    hl(cr, t, [("3 YEARS", RED), (" perfect attendance", INK)], 215, 48, A("p1", "3"), end=A("p2", "secret") - 0.05,
       bold=True)
    hl(cr, t, [("the secret? ", INK), ("his BROTHER", RED)], 215, 58, A("p3", "brother"), end=A("p4", "Jack") - 0.05,
       bold=True)
    hl(cr, t, [("identical ", INK), ("TWIN", BLUE)], 215, 90, A("p4", "Jack"), end=A("p6") - 0.05, bold=True)
    hl(cr, t, [("MON: ", INK), ("Jake", RED), ("   TUE: ", INK), ("Jack", BLUE)], 330, 52, A("p5", "Monday"),
       end=A("p6") - 0.05, bold=True)
    hl(cr, t, [("who gets the ", INK), ("award", GOLD), ("?", INK)], 215, 70, A("p6", "which"), end=A("p8") - 0.05,
       bold=True)
    hl(cr, t, [("a confession ", INK), ("too", RED)], 215, 80, A("p8", "confession"), end=A("p9", "another") - 0.05,
       bold=True)
    hl(cr, t, [("ANOTHER", RED), (" Mr. Miller", INK)], 215, 76, A("p9", "another"), end=A("p10", "half") - 0.05, bold=True)
    hl(cr, t, [("only ", INK), ("HALF", RED), (" the syllabus", INK)], 215, 66, A("p10", "half"), bold=True, underline=True)
    if t >= A("p4", "another"):
        cue("hit", t, A("p4", "another"))
    if t >= A("p9", "another"):
        stamp(cr, t, A("p9", "another"), "TWINS AGAIN?!", dur=1.0, y=470)


def draw(cr, t, tl):
    cr.save()
    scene_stage(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
