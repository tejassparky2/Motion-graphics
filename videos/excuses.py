"""Episode 17: "The Excuses" — an original classroom comedy with a twist (same class as Who Is Kevin? etc.).

Three students, three fake excuses, each shot down by Mr. Miller. Then the principal asks why HE was late:
"My dog ate my car keys." The class: "Sir, you don't have a dog."
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import classroom, desk

NARRATOR = dict(speed=0.97)
TAIL = 0.8

SCRIPT = [
    dict(id="x1", scene="class", text="Monday morning. Three students, no homework, and three excuses."),
    dict(id="x2", scene="class", text="Tyler goes first. Sir, my dog ate my homework.", speaker="kid_c",
         speaker_from="sir"),
    dict(id="x3", scene="class", text="It was an online assignment.", speaker="teacher", gap=0.2),
    dict(id="x4", scene="class", text="He ate my laptop too.", speaker="kid_c", gap=0.2),
    dict(id="x5", scene="class", text="Then who posted a dance video on your account last night?", speaker="teacher",
         gap=0.2),
    dict(id="x6", scene="class", text="The dog.", speaker="kid_c", pace=0.9, gap=0.3),
    dict(id="x7", scene="class", text="Emma is next. She hands over a doctor's note, signed Doctor Smith."),
    dict(id="x8", scene="class", text="Funny. My wife is Doctor Smith. She's a vet.", speaker="teacher", gap=0.2),
    dict(id="x9", scene="class", text="Emma pauses. [Woof, woof.|Woof woof?]", speaker="kid_a", speaker_from="woof", gap=0.2),
    dict(id="x10", scene="class",
         text="Last, Jake from the back row. Sir, I was stuck in traffic for [three hours.|3 hours.]", speaker="chotu",
         speaker_from="sir", gap=0.3),
    dict(id="x11", scene="class", text="Jake, you live across the street.", speaker="teacher", gap=0.2),
    dict(id="x12", scene="class", text="Yes sir. Very long red light.", speaker="chotu", gap=0.2),
    dict(id="x13", scene="class",
         text="Then the door opens. It's the principal. Mr. Miller, why were you late to school today?",
         speaker="oldman", speaker_from="Mr.", gap=0.3),
    dict(id="x14", scene="class", text="Mr. Miller freezes. My dog ate my car keys.", speaker="teacher",
         speaker_from="my", gap=0.2),
    dict(id="x15", scene="end", text="The whole class: Sir, you don't have a dog.", speaker="kids", speaker_from="sir",
         gap=0.3),
]

METADATA = dict(
    title="3 Students, 3 Fake Excuses… Then the Teacher Got Caught 😂",
    alt_titles=["The Worst Homework Excuses Ever 😂", "\"My Dog Ate My Homework\"… It Was ONLINE 💀"],
    description="""Monday morning. Three students, no homework, and three excuses. 😂

The dog that ate an online assignment. A doctor's note from a doctor who happens to be the teacher's wife (she's a vet 🐶). And a 3-hour traffic jam… from across the street.

Then the principal walked in and asked the teacher why HE was late… 👀

💬 What's the best excuse you've ever used? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Funny", "#School", "#PlotTwist"],
    tags=["funny excuses", "homework excuse", "my dog ate my homework", "school comedy", "teacher vs student",
          "plot twist", "funny story", "classroom comedy", "animated story", "interestingly strange"],
    pinned_comment="Drop your best excuse that actually worked 😂👇",
)

GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
GOLD = hexc("#f2b632")
TX = 120
EMMA, TYLER, OLIVIA, JAKE = 330, 490, 650, 830
KIDS = (("kid_a", EMMA), ("kid_c", TYLER), ("kid_d", OLIVIA), ("chotu", JAKE))
WIDE = (0.85, 470, 770)
TEACH = (1.9, 150, 740)


def focus(x, z=2.0):
    return (z, x - 20, 730)


def dog(cr, x, y, t, s=1.0, facing=1, seed=0):
    with at(cr, x, y, s, flip=facing < 0):
        for lx in (-40, -16, 24, 46):
            line(cr, [(lx, -30), (lx, 0)], 9, hexc("#8e5a2e"), seed=seed + lx, amp=0.2)
        blob(cr, 0, -48, 64, 34, hexc("#c98b4f"), seed=seed + 1, amp=0.8, lw=4)
        line(cr, [(-62, -60), (-86, -84 - 10 * math.sin(t * 14))], 7, hexc("#c98b4f"), seed=seed + 2, amp=0.2)
        blob(cr, 66, -84, 32, 28, hexc("#c98b4f"), seed=seed + 3, amp=0.6, lw=4)
        blob(cr, 54, -110, 12, 22, hexc("#8e5a2e"), seed=seed + 4, amp=0.4, lw=3)
        blob(cr, 92, -80, 12, 9, INK, seed=seed + 5, amp=0.2)
        dot(cr, 72, -92, 5, INK)
        line(cr, [(78, -66), (90, -62)], 3, INK, seed=seed + 6, amp=0.1)


def thought(cr, t, t0, t1, x, y, draw_fn, w=280, h=210, seed=0):
    """Pop-in panel above a character, drawn by draw_fn(cr) centred on (0, 0)."""
    if not (t0 <= t < t1):
        return
    sc = pop(t, t0, 0.2)
    if sc <= 0:
        return
    with at(cr, x, y, sc):
        shape(cr, rrect_pts(-w / 2, -h / 2, w, h, 26, 20), WHITE, seed=seed, amp=0.8, lw=4)
        draw_fn(cr)


def scene_class(cr, t, tl):
    A = tl.at
    keys = [(0, WIDE), (A("x1", "three"), (1.2, 600, 760)), (A("x1", "homework"), (1.5, 470, 700)),
            (A("x1", "excuses"), (1.0, 470, 760)),
            (A("x2", "Tyler"), focus(TYLER)), (A("x2", "dog"), (1.6, 470, 620)), (A("x2", "homework"), focus(TYLER, 2.3)),
            (A("x3"), TEACH), (A("x3", "online"), (2.3, 140, 740)), (A("x4"), focus(TYLER, 2.2)),
            (A("x4", "laptop"), (1.6, 470, 620)), (A("x5"), TEACH), (A("x5", "dance"), (1.6, 380, 620)),
            (A("x5", "account"), (2.2, 150, 730)), (A("x6"), focus(TYLER, 2.5)),
            (A("x7", "Emma"), focus(EMMA)), (A("x7", "note"), (1.6, 230, 640)), (A("x7", "Smith"), (2.2, 230, 640)),
            (A("x8"), TEACH), (A("x8", "wife"), (2.2, 150, 720)), (A("x8", "vet"), (1.6, 230, 620)),
            (A("x9"), focus(EMMA, 2.2)), (A("x9", "woof"), focus(EMMA, 2.7)),
            (A("x10", "Jake"), focus(JAKE)), (A("x10", "traffic"), (1.6, 700, 620)), (A("x10", "hours"), focus(JAKE, 2.3)),
            (A("x11"), TEACH), (A("x11", "across"), (1.6, 700, 620)), (A("x12"), focus(JAKE, 2.2)),
            (A("x12", "red"), (1.8, 700, 620)),
            (A("x13", "door"), (1.2, 900, 740)), (A("x13", "principal"), (1.9, 980, 720)), (A("x13", "late"), (1.3, 700, 740)),
            (A("x14"), TEACH), (A("x14", "freezes"), (2.4, 140, 740)), (A("x14", "dog"), (1.6, 230, 640))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    # ---- teacher
    s = dict(facing=1, arms=("hip", "hip"), eyes="sly", mouth="flat")
    if A("x13") <= t:
        s.update(facing=1, eyes="wide", mouth="o", sweat=True)
    if A("x14", "freezes") <= t < A("x14", "my"):
        s.update(shake=1.5)
    if A("x14", "my") <= t:
        s.update(eyes="sly", mouth="smirk", arms=("chin", "hip"))
    if tl.speaking("teacher", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "flat"
    person(cr, "teacher", TX, 900, t, **s)
    # ---- students
    for i, (who, x) in enumerate(KIDS):
        k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
        y = 900
        if who == "kid_c" and A("x2") <= t < A("x7"):
            y -= 36
            k.update(eyes="sad" if t < A("x6") else "sly", mouth="wobble" if t < A("x6") else "smirk")
        if who == "kid_a" and A("x7") <= t < A("x10"):
            y -= 36
            k.update(arms=("give", "hip") if t < A("x8") else ("hip", "hip"), eyes="happy" if t < A("x8") else "wide",
                     mouth="smile" if t < A("x8") else "o")
        if who == "chotu" and A("x10") <= t < A("x13"):
            y -= 36
            k.update(eyes="sly", mouth="smirk")
        if t >= A("x14", "dog"):
            k.update(eyes="sly", mouth="smirk")
        if tl.speaking(who, t):
            k["mouth"] = "o" if int(t * 12) % 2 else "smile"
        person(cr, who, x, y, t, **k)
        desk(cr, x, 14000 + i * 10)
    # ---- principal at the door
    if t >= A("x13", "door"):
        shape(cr, rrect_pts(900, 600, 150, 300, 6, 16), hexc("#8e5a2e"), seed=14100, amp=0.5, lw=4)
        walk = seg(t, A("x13", "door"), A("x13", "principal", end=True))
        p = dict(facing=-1, arms=("hip", "hip"), eyes="sly", mouth="flat")
        if tl.speaking("oldman", t):
            p["mouth"] = "o" if int(t * 12) % 2 else "flat"
        person(cr, "oldman", lerp(1100, 980, walk), 905, t, walk=t * 2.5 if walk < 1 else None, **p)
    # ---- excuse panels
    def homework_dog(c):
        dog(c, -10, 70, t, 0.9, seed=14200)
        shape(c, rrect_pts(40, -20, 70, 50, 4, 10), WHITE, seed=14201, amp=0.4, lw=3)
    thought(cr, t, A("x2", "dog"), A("x3"), 470, 560, homework_dog, seed=14210)

    def online(c):
        shape(c, rrect_pts(-100, -70, 200, 130, 10, 14), INK, seed=14220, amp=0.4, lw=3)
        shape(c, rrect_pts(-88, -58, 176, 106, 6, 14), hexc("#dff5e3"), seed=14221, amp=0.3, lw=0, stroke=None)
        write(c, [("ONLINE", BLUE)], 0, -10, 34, align="center", bold=True)
        write(c, [("assignment", INK)], 0, 26, 24, align="center")
    thought(cr, t, A("x3", "online"), A("x4"), 380, 560, online, seed=14230)

    def laptop(c):
        shape(c, rrect_pts(-100, -60, 200, 110, 8, 14), hexc("#a9a2ae"), seed=14240, amp=0.4, lw=3.5)
        blob(c, 90, -50, 40, 40, WHITE, seed=14241, amp=1.2, lw=0, stroke=None)   # bite mark
        dog(c, -60, 90, t, 0.6, seed=14242)
    thought(cr, t, A("x4", "laptop"), A("x5"), 470, 560, laptop, seed=14250)

    def dance(c):
        shape(c, rrect_pts(-70, -95, 140, 190, 16, 14), INK, seed=14260, amp=0.4, lw=3)
        shape(c, rrect_pts(-60, -83, 120, 166, 10, 14), hexc("#ffd0e0"), seed=14261, amp=0.3, lw=0, stroke=None)
        person(c, "kid_c", 0, 70, t, facing=1, scale=0.55, arms=("cheer", "wave"), eyes="happy", mouth="grin",
               jump=abs(math.sin(t * 10)) * 8)
    thought(cr, t, A("x5", "dance"), A("x6"), 380, 560, dance, seed=14270)

    if A("x6") <= t < A("x7"):
        stamp(cr, t, A("x6"), "THE DOG?!", dur=0.9, y=470)

    def note(c):
        shape(c, rrect_pts(-100, -80, 200, 160, 6, 14), WHITE, seed=14280, amp=0.4, lw=3)
        write(c, [("DOCTOR'S NOTE", RED)], 0, -44, 24, align="center", bold=True)
        write(c, [("excused from ALL homework", INK)], 0, -6, 16, align="center")
        write(c, [("Dr. Smith", BLUE)], 20, 50, 30, align="center")
        if t >= A("x8", "vet"):
            write(c, [("VETERINARIAN", GREEN)], 0, 84, 24, align="center", bold=True)
    thought(cr, t, A("x7", "note"), A("x9"), 230, 560, note, h=230, seed=14290)
    if A("x9", "woof") <= t < A("x10"):
        stamp(cr, t, A("x9", "woof"), "WOOF WOOF?", dur=0.9, y=470)

    def traffic(c):
        shape(c, rrect_pts(-110, -80, 220, 160, 8, 14), hexc("#c9f0c4"), seed=14300, amp=0.3, lw=3)
        shape(c, rrect_pts(-90, -50, 60, 60, 6, 10), hexc("#e0487a"), seed=14301, amp=0.3, lw=2.5)
        write(c, [("HOME", INK)], -60, 30, 18, align="center", bold=True)
        shape(c, rrect_pts(30, -50, 60, 60, 6, 10), hexc("#f7d774"), seed=14302, amp=0.3, lw=2.5)
        write(c, [("SCHOOL", INK)], 60, 30, 18, align="center", bold=True)
        sharp_shape(c, [(-20, -70), (20, -70), (20, 70), (-20, 70)], hexc("#6b6f78"), seed=14303, amp=0.2, lw=2)
        if t >= A("x12", "red"):
            shape(c, rrect_pts(-12, -40, 24, 64, 6, 8), INK, seed=14304, amp=0.2, lw=2)
            dot(c, 0, -26, 8, RED)
    thought(cr, t, A("x10", "traffic"), A("x13"), 700, 560, traffic, seed=14310)

    def keys_dog(c):
        dog(c, -20, 70, t, 0.9, seed=14320)
        blob(c, 90, -30, 16, 16, None, seed=14321, amp=0.3, lw=5, stroke=hexc("#a9a2ae"))
        write(c, [("???", RED)], 70, -60, 30, bold=True)
    thought(cr, t, A("x14", "dog"), 99, 230, 560, keys_dog, seed=14330)
    # ---- headlines
    hl(cr, t, [("3 students, 3 ", INK), ("EXCUSES", RED)], 215, 66, 0.0, end=A("x2") - 0.05, bold=True, sound=False)
    hl(cr, t, [("excuse #1: ", INK), ("the dog", GOLD)], 215, 70, A("x2", "dog"), end=A("x7") - 0.05, bold=True)
    hl(cr, t, [("excuse #2: ", INK), ("doctor's note", BLUE)], 215, 62, A("x7", "note"), end=A("x10") - 0.05, bold=True)
    hl(cr, t, [("excuse #3: ", INK), ("traffic", RED)], 215, 70, A("x10", "traffic"), end=A("x13") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("PRINCIPAL", RED)], 215, 84, A("x13", "principal"), end=A("x14", "dog") - 0.05, bold=True)
    hl(cr, t, [("his excuse: ", INK), ("the dog", GOLD)], 215, 70, A("x14", "dog"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("x15") - 0.2, (1.0, 470, 760)), (A("x15", "class"), (1.3, 600, 760)), (A("x15", "sir"), (0.9, 470, 760)),
            (A("x15", "dog"), (2.0, 150, 740))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    classroom(cr, t)
    person(cr, "teacher", TX, 900, t, facing=1, eyes="wide", mouth="o", sweat=True, shake=1.2 if t >= A("x15", "dog") else 0)
    talking = A("x15", "sir") <= t <= A("x15", end=True)
    for i, (who, x) in enumerate(KIDS):
        person(cr, who, x, 900 - 36, t, facing=-1, arms=("point", "hip"), eyes="sly",
               mouth=("o" if int(t * 12 + i) % 2 else "smirk") if talking else "smirk")
        desk(cr, x, 14400 + i * 10)
    person(cr, "oldman", 980, 905, t, facing=-1, arms=("hip", "hip"), eyes="sly", mouth="flat")
    hl(cr, t, [("you don't have a ", INK), ("DOG", RED)], 215, 70, A("x15", "have"), bold=True, underline=True)
    if t >= A("x15", "dog"):
        stamp(cr, t, A("x15", "dog"), "BUSTED", dur=1.2, y=470)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"class": scene_class, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
