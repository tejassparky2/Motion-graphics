"""Body Facts 6: "They Turned His TOE Into a THUMB" — toe-to-thumb transfer.

Facts (kept general; sources in research_notes/body_facts_5-6.md):
- A toe (the big toe or the second toe) is moved to the hand to make a new thumb (Thumb Reconstruction with Toe
  Transfer, PMC3122704; Waljee & Chung reviews).
- Under a microscope the surgeons join bone, tendons, arteries, veins and nerves (PMC3122704).
- Losing the thumb disables the hand most ("the king of the digits"); the new thumb restores grip and pinch.
- The foot works well without the toe; walking is largely unaffected (PMC3122704: "the foot functions quite
  adequately without a full complement of toes"). So: "most people still walk normally".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, BED_A, DOC_CLOSE, TWO_SHOT, bed, doctor, label, patient, room, sheet, watermark
from motion.engine import WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.kit import camera, enter_world, set_camera, whip
from motion.surgery import BLOOD, BLOOD_D, SKIN, SKIN_D, drapes, forceps, stitches
from videos.kidney_donor import eyes, mouth, scalpel

# Voices: natural stock voices at their own pitch; the doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "hand": dict(voice="af_heart", speed=0.95),
    "toe": dict(voice="am_michael", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"thumb", "toe", "toe-to-thumb", "microscope", "nerves", "transfer"}

SCRIPT = [
    dict(id="o1", scene="hand", text="I lost my thumb in an accident. Now I can't even hold a cup!", speaker="hand"),
    dict(id="o2", scene="hand", text="Don't worry, hand. I found you a new thumb.", speaker="scalpel"),
    dict(id="o3", scene="foot", text="Hey! Why is the scalpel looking at me?", speaker="toe"),
    dict(id="o4", scene="foot", text="Pack your things, big toe. You're moving to the hand.", speaker="scalpel"),
    dict(id="o5", scene="hand2", text="The hand? I've lived in a sock my whole life!", speaker="toe"),
    dict(id="o6", scene="hand2", text="Welcome! Can you hold this cup for me?", speaker="hand"),
    dict(id="o7", scene="hand2", text="Wow. I'm a thumb now!", speaker="toe"),
    dict(id="c1", scene="ward", text="Doctor, is that really my toe on my hand?", speaker="mike"),
    dict(id="c2", scene="ward", text="Yes. This is called a toe-to-thumb transfer.", speaker="doctor"),
    dict(id="c3", scene="ward", text="We moved your big toe to your hand. Under a microscope, we connected its bone, "
                                     "tendons, blood vessels, and nerves.", speaker="doctor"),
    dict(id="c4", scene="ward", text="Your thumb does a huge part of your hand's work. Now you can grip and pinch "
                                     "again.", speaker="doctor"),
    dict(id="c5", scene="ward", text="And most people still walk normally without that toe.", speaker="doctor"),
    dict(id="c6", scene="ward", text="So will my new thumb smell like feet?", speaker="mike", gap=0.3),
    dict(id="c7", scene="ward", text="Just wash your hands.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="They Turned His TOE Into a THUMB 😳",
    alt_titles=["Toe-to-Thumb Surgery Is Real 🦶👍", "Surgeons Moved His Big Toe to His Hand 😳"],
    description="""He lost his thumb in an accident. So surgeons moved his big toe… to his hand. 🦶👍

It's real. In a toe-to-thumb transfer, surgeons move the big toe or the second toe to the hand, and under a microscope they connect its bone, tendons, blood vessels and nerves. The new thumb lets you grip and pinch again, and most people still walk normally without the toe.

(Cartoon, real medicine. Not medical advice: talk to a hand surgeon about your own case.)

💬 Would you trade a toe for a thumb? 👇

🔔 Body Facts: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#ToeToThumb", "#BodyFacts", "#Surgery"],
    tags=["toe to thumb transfer", "toe to thumb surgery", "toe to hand transplant", "microsurgery", "weird surgery",
          "rare surgery", "thumb reconstruction", "body facts", "doctor explains", "medical animation"],
    pinned_comment="Would you trade your big toe for a new thumb? 🦶👍 And yes, he washes his hands. 😂👇",
)

NAIL = hexc("#f6d9d2")


def toe_char(cr, t, x, y, s, rot=0.0, mood="calm", talking=False, shake=0.0, wide=1.0):
    """A toe as a character: rounded skin capsule, toenail on top, face below it."""
    x += math.sin(t * 50) * shake
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-46 * wide, -78, 92 * wide, 170, 44 * wide, 14), SKIN, seed=1200, amp=0, lw=3.5)
        shape(cr, rrect_pts(-30 * wide, -70, 60 * wide, 52, 18, 12), NAIL, seed=1201, amp=0, lw=3)
        line(cr, [(-34 * wide, 70), (34 * wide, 70)], 2.5, SKIN_D, seed=1202, amp=0)
        eyes(cr, 0, 10, 0.58 * wide, mood)
        mouth(cr, 0, 44, 0.55 * wide, mood, talking, t)


def hand(cr, t, x, y, mood, talking, thumb=None, grip=0.0):
    """Back of the right hand, fingers up, on the drape. `thumb`: None (bandaged stump) or a callable drawing it."""
    shape(cr, rrect_pts(x - 100, y + 120, 200, 600, 60, 20), hexc("#2f7fd6"), seed=1210, amp=0, lw=3.5)   # sleeve
    for k, (fx, ln) in enumerate(((-105, 205), (-35, 240), (35, 228), (100, 175))):              # fingers
        curl = grip * 0.35 * (1 if k < 2 else 0.6)
        with at(cr, x + fx, y - 130, 1.0, rot=-curl * 0.4):
            shape(cr, rrect_pts(-30, -ln, 60, ln + 40, 30, 14), SKIN, seed=1211 + k, amp=0, lw=3.5)
            shape(cr, rrect_pts(-19, -ln + 6, 38, 34, 14, 10), NAIL, seed=1215 + k, amp=0, lw=2.5)
            line(cr, [(-18, -ln * 0.45), (18, -ln * 0.45)], 2.5, SKIN_D, seed=1219 + k, amp=0)
    shape(cr, rrect_pts(x - 150, y - 150, 300, 300, 90, 20), SKIN, seed=1223, amp=0, lw=4)                 # back of hand
    for k in range(4):
        line(cr, [(x - 100 + 66 * k, y - 120), (x - 96 + 66 * k, y - 100)], 3, SKIN_D, seed=1224 + k, amp=0)
    if thumb is None:   # bandaged stump
        with at(cr, x - 150, y + 10, 1.0, rot=-0.7):
            shape(cr, rrect_pts(-32, -70, 64, 90, 30, 12), SKIN, seed=1230, amp=0, lw=3.5)
            shape(cr, rrect_pts(-36, -76, 72, 50, 26, 12), WHITE, seed=1231, amp=0, lw=3)
            dot(cr, 0, -56, 8, hexc("#e06a6a"))
    else:
        thumb()
    eyes(cr, x + 6, y - 30, 0.9, mood)
    mouth(cr, x + 6, y + 30, 0.85, mood, talking, t)


def cup(cr, x, y):
    shape(cr, [(x - 50, y - 70), (x + 50, y - 70), (x + 40, y + 70), (x - 40, y + 70)], hexc("#f39a2b"), seed=1240,
          amp=0, lw=3.5)
    blob(cr, x, y - 70, 50, 12, hexc("#7a4a2e"), seed=1241, amp=0, lw=3)


def foot(cr, x, y, t, big=True):
    """Top of the right foot, toes up; the big toe (screen left) is the character, drawn by the caller."""
    shape(cr, rrect_pts(x - 150, y - 170, 300, 520, 140, 20), SKIN, seed=1250, amp=0, lw=4)
    shape(cr, rrect_pts(x - 110, y + 300, 220, 500, 60, 20), hexc("#2f7fd6"), seed=1251, amp=0, lw=3.5)   # trouser
    for k, (tx, ty, sc) in enumerate(((-30, -205, 0.55), (40, -195, 0.5), (95, -175, 0.45), (135, -145, 0.4))):
        toe_char(cr, t, x + tx, y + ty, sc, mood="happy")
    if not big:   # where the big toe was: stitched, a little blood
        blob(cr, x - 105, y - 170, 44, 30, hexc("#d9534f"), seed=1260, amp=0, lw=3)
        stitches(cr, [(x - 140 + 4 * k, y - 172) for k in range(18)], 1.0)


HX, HY = 380, 700     # the hand
FX, FY = 2000, 760    # the foot


def scene_hand(cr, t, tl, after=False):
    A = tl.at
    if not after:
        keys = [(0, (1.1, HX, 760)), (A("o1", "cup"), (1.0, 330, 720)), (A("o2"), (1.15, 420, 700))]
    else:
        keys = [(A("o5") - 0.1, (1.25, HX - 80, 720)), (A("o5", "sock"), (1.05, HX - 40, 740)),
                (A("o6"), (1.0, 330, 720)), (A("o7"), (1.35, HX - 140, 700))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    if not after:
        mood = "cry" if t < A("o2") else "shock"
        reach = math.sin(math.pi * seg(t, A("o1", "hold"), A("o1", "hold") + 1.0))
        hand(cr, t, HX, HY, mood, tl.speaking("hand", t), grip=reach)
        cup(cr, 130, 600)
        if A("o1", "cup") <= t < A("o2"):
            label(cr, "No thumb, no grip", 200, 400, 210, 620)
        if t >= A("o2") - 0.2:
            u = ease_out(seg(t, A("o2") - 0.2, A("o2") + 0.4))
            scalpel(cr, t, lerp(820, 600, u), lerp(200, 330, u), 1.1, -0.5, talking=tl.speaking("scalpel", t),
                    mood="happy")
        return
    sew = seg(t, A("o5"), A("o5", end=True))
    grab = ease_out(seg(t, A("o7") - 0.2, A("o7") + 0.4))
    tm = "angry" if t < A("o6") else ("worried" if t < A("o7") else "happy")

    def new_thumb():
        rot = lerp(-0.7, -0.25, grab)
        with at(cr, HX - 150, HY + 10, 1.0, rot=rot):
            toe_char(cr, t, 0, -40, 0.85, mood=tm, talking=tl.speaking("toe", t), wide=1.15)
        stitches(cr, [(HX - 190 + 4 * k, HY - 20 + 2 * k) for k in range(20)], sew)
    hm = "happy" if t >= A("o6") else "shock"
    hand(cr, t, HX, HY, hm, tl.speaking("hand", t), thumb=new_thumb, grip=grab * 0.8)
    if A("o6") <= t:
        cx = lerp(110, 150, grab)
        cup(cr, cx, lerp(560, 600, grab))
    if t < A("o6"):   # what the surgeons joined, under the microscope
        for k, (name, col) in enumerate((("Bone", hexc("#f2e6cf")), ("Tendons", WHITE), ("Blood vessels", BLOOD),
                                          ("Nerves", hexc("#ffd23f")))):
            if t >= A("o5") + 0.35 * k:
                line(cr, [(HX - 230, HY - 40 + 22 * k), (HX - 120, HY - 20 + 22 * k)], 7, col, seed=1270 + k, amp=0)
                label(cr, name, 560, 380 + 58 * k, HX - 120, HY - 20 + 22 * k, size=28)
                cue("pop", t, A("o5") + 0.35 * k)


def scene_foot(cr, t, tl):
    A = tl.at
    cut = ease_out(seg(t, A("o4", "moving") - 0.2, A("o4", "moving") + 0.5))
    lift = ease_out(seg(t, A("o4", "hand") - 0.1, A("o4", end=True) + 0.4))
    keys = [(A("o3") - 0.1, (1.3, FX - 90, 640)), (A("o4"), (1.05, FX, 700))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    foot(cr, FX, FY, t, big=cut < 1)
    bx, by = FX - 105, FY - 230
    if cut < 1:
        mood = "shock" if t < A("o4") else "cry"
        toe_char(cr, t, bx, by, 0.95, rot=-0.15, mood=mood, talking=tl.speaking("toe", t),
                 shake=1.5 if t >= A("o4") else 0)
        if t >= A("o4", "moving") - 0.2:
            line(cr, [(bx - 50, by + 80), (bx - 50 + 100 * cut, by + 80)], 6, BLOOD, seed=1280, amp=0)
    else:
        tx, ty = bx + 200 * lift, by - 700 * lift
        toe_char(cr, t, tx, ty, 0.95, rot=-0.15 + 0.5 * lift, mood="shock", talking=tl.speaking("toe", t))
        forceps(cr, tx, ty - 80, 1.0, grip=1.0)
        for k in range(3):
            u = (t * 1.6 + k / 3) % 1
            blob(cr, tx - 20 + 20 * k, ty + 100 + 160 * u, 6, 9, BLOOD, seed=1281 + k, amp=0, lw=2, stroke=BLOOD_D)
    if t < A("o4", "moving"):
        scalpel(cr, t, FX + 120, FY - 470, 1.1, -0.5, talking=tl.speaking("scalpel", t), mood="happy")
    label(cr, "Big toe", FX - 260, FY - 430, bx - 20, by - 70)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("c1") - 0.1, A_CLOSE), (A("c1", "hand"), TWO_SHOT),
            (A("c2"), DOC_CLOSE), (A("c3"), TWO_SHOT), (A("c3", "microscope"), DOC_CLOSE), (A("c4"), TWO_SHOT),
            (A("c5"), DOC_CLOSE), (A("c6"), A_CLOSE), (A("c7"), DOC_CLOSE), (A("c7", "hands"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    x, y, s = BED_A
    bed(cr, x)
    m = dict(eyes="wide", mouth="o", arms=("wave", "down"))
    if A("c2") <= t < A("c6"):
        m.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("c6") <= t:
        m.update(eyes="sly", mouth="smirk", arms=("thumb", "down"))
    if A("c7") <= t:
        m.update(eyes="wide", mouth="o", sweat=True)
    patient(cr, "mike_b", x, y, s, t, talking=tl.speaking("mike", t), **m)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("c2") <= t < A("c6"):
        d.update(arms=("hold", "down"), eyes="happy" if A("c4") <= t < A("c6") else "dot")
    if A("c6") <= t < A("c7"):
        d.update(eyes="wide")
    if A("c7") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    elif name == "foot":
        scene_foot(cr, t, tl)
    elif name == "hand2":
        scene_hand(cr, t, tl, after=True)
    else:
        scene_hand(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
