"""Body Facts 7: "They Turned His Foot BACKWARDS… On Purpose" — rotationplasty.

Facts (kept general; sources in research_notes/body_facts_7-8.md):
- Done mostly for children and teenagers with a bone tumour (osteosarcoma) around the knee (Children's Hospital
  Colorado; OncoLink; Johns Hopkins).
- The part of the leg with the tumour (lower thigh bone, knee, top of the shin) is removed; the lower leg is turned
  around 180 degrees and joined to the thigh, so the foot points backwards and the ankle works as a knee; the main
  artery and the sciatic nerve are kept (OncoLink; Wikipedia).
- A prosthetic leg fits over the foot; the ankle bends it like a knee. Many patients run and play sports; function is
  generally better than an above-knee amputation (Children's Colorado; Johns Hopkins).
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, BED_A, DOC_CLOSE, TWO_SHOT, bed, doctor, label, patient, room, sheet, watermark
from motion.engine import at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.kit import camera, enter_world, set_camera, whip
from motion.surgery import BLOOD, BLOOD_D, SKIN, METAL, METAL_D, drapes, stitches
from videos.kidney_donor import eyes, mouth, scalpel

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "knee": dict(voice="af_heart", speed=0.95),
    "foot": dict(voice="am_michael", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"rotationplasty", "backwards", "knee", "ankle", "tumor", "prosthetic"}

SCRIPT = [
    dict(id="r1", scene="leg", text="Something is growing inside me. And it really hurts!", speaker="knee"),
    dict(id="r2", scene="leg", text="That's a bone tumor. I'm sorry, but the knee has to go.", speaker="scalpel"),
    dict(id="r3", scene="leg", text="Wait! If the knee goes, how will he bend his leg?", speaker="foot"),
    dict(id="r4", scene="leg", text="That's where you come in, foot. Turn around!", speaker="scalpel"),
    dict(id="r5", scene="leg", text="Turn around? You want me to face backwards?", speaker="foot"),
    dict(id="r6", scene="leg", text="Yes. Your ankle will bend like a brand new knee.", speaker="scalpel"),
    dict(id="r7", scene="leg", text="Okay. This is the weirdest promotion ever!", speaker="foot"),
    dict(id="w1", scene="ward", text="Doctor, why is my foot on backwards?", speaker="danny"),
    dict(id="w2", scene="ward", text="Because now it works as your knee. This is called a rotationplasty.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="We removed the bone tumor around your knee. Then we turned your lower leg "
                                     "around, and joined it to your thigh.", speaker="doctor"),
    dict(id="w4", scene="ward", text="Now your ankle bends like a knee, and your foot fits inside a prosthetic leg.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Many patients can run and play sports again.", speaker="doctor"),
    dict(id="w6", scene="ward", text="So my socks go on my knee now?", speaker="danny", gap=0.3),
    dict(id="w7", scene="ward", text="Exactly.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="They Turned His Foot BACKWARDS… On Purpose 😳",
    alt_titles=["Rotationplasty: The Foot That Became a Knee 😳", "His Ankle Is Now His Knee 🦶➡️🦵"],
    description="""A tumor took his knee. So surgeons turned his foot around… and made his ankle the new knee. 😳

It's real. In a rotationplasty, surgeons remove the part of the leg with the bone tumor, turn the lower leg around and join it to the thigh. The foot now points backwards, the ankle bends like a knee, and the foot fits inside a prosthetic leg. Many patients run and play sports again.

(Cartoon, real medicine. Not medical advice: talk to an orthopedic surgeon about your own case.)

💬 Did you know this surgery existed? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Rotationplasty", "#WeirdSurgery", "#Doctor"],
    tags=["rotationplasty", "foot turned backwards", "ankle as knee", "weird surgery", "rare surgery",
          "osteosarcoma", "bone cancer surgery", "prosthetic leg", "doctor explains", "medical animation"],
    pinned_comment="His ANKLE is his knee now. 😳 Did you know this surgery existed? 👇",
)

BONE = hexc("#f2e6cf")
TUMOR = hexc("#7a3a6a")
X = 360                 # the leg's centre line
THIGH_TOP, KNEE_Y, ANKLE_Y = 120, 600, 1000


def thigh(cr):
    shape(cr, rrect_pts(X - 85, THIGH_TOP, 170, KNEE_Y - THIGH_TOP + 20, 60, 20), SKIN, seed=1300, amp=0, lw=4)
    shape(cr, rrect_pts(X - 120, THIGH_TOP - 200, 240, 260, 40, 20), hexc("#2f7fd6"), seed=1301, amp=0, lw=4)   # gown


def knee(cr, t, mood, talking, tumor=1.0):
    blob(cr, X, KNEE_Y, 95, 80, SKIN, seed=1302, amp=0, lw=4)
    blob(cr, X + 50, KNEE_Y - 6, 42, 46, hexc("#f2cdb0"), seed=1303, amp=0, lw=3)                 # kneecap
    if tumor > 0:
        blob(cr, X - 30, KNEE_Y + 10, 44 * tumor, 34 * tumor, TUMOR, seed=1304, amp=0, lw=3)
        for k in range(5):
            dot(cr, X - 44 + 9 * k, KNEE_Y + 6 + 5 * (k % 2), 3, hexc("#a8558f"))
    eyes(cr, X + 40, KNEE_Y - 18, 0.62, mood)
    mouth(cr, X + 40, KNEE_Y + 16, 0.55, mood, talking, t)


def lower_leg(cr, t, mood, talking, flex=0.0, shin=None):
    """Shin + ankle + foot, drawn with the ankle at (0, 0): shin going up, foot pointing to +x. `shin` = length."""
    ln = shin if shin is not None else ANKLE_Y - KNEE_Y - 20
    shape(cr, rrect_pts(-55, -ln - 20, 110, ln + 20, 46, 20), SKIN, seed=1310, amp=0, lw=4)
    with at(cr, 0, 0, 1.0, rot=-flex):
        shape(cr, [(-60, -30), (40, -40), (170, -10), (200, 20), (180, 56), (-50, 60), (-80, 30)], SKIN, seed=1311,
              amp=0, lw=4)
        for k in range(4):   # toes
            blob(cr, 185 - 6 * k, 6 + 14 * k, 18, 12, SKIN, seed=1312 + k, amp=0, lw=2.5)
        eyes(cr, 80, -6, 0.6, mood)
        mouth(cr, 80, 24, 0.55, mood, talking, t)
    blob(cr, 0, 0, 34, 34, hexc("#f2cdb0"), seed=1316, amp=0, lw=3)                              # ankle bone


def prosthesis(cr, appear):
    """A prosthetic leg: a socket around the backwards foot, a metal pole, a sneaker."""
    if appear <= 0:
        return
    cr.push_group()
    shape(cr, rrect_pts(X - 120, 640, 240, 170, 50, 20), hexc("#e8edf2", 0.85), seed=1320, amp=0, lw=4)
    shape(cr, rrect_pts(X - 18, 800, 36, 330, 12, 20), METAL, seed=1321, amp=0, lw=3.5)
    line(cr, [(X - 8, 820), (X - 8, 1110)], 3, METAL_D, seed=1322, amp=0)
    shape(cr, [(X - 70, 1120), (X + 120, 1120), (X + 140, 1160), (X - 80, 1170)], hexc("#d8363a"), seed=1323, amp=0,
          lw=4)
    cr.pop_group_to_source()
    cr.paint_with_alpha(appear)


def scene_leg(cr, t, tl):
    A = tl.at
    cut = ease_out(seg(t, A("r2", "go") - 0.1, A("r2", "go") + 0.7))           # the tumour section comes out
    turn = ease_out(seg(t, A("r5") - 0.1, A("r5", end=True)))                    # the lower leg turns around
    rise = ease_out(seg(t, A("r6"), A("r6", "knee") + 0.3))                       # ...and joins the thigh
    pros = ease_out(seg(t, A("r7") - 0.2, A("r7") + 0.4))
    flex = 0.35 * max(0.0, math.sin((t - A("r7")) * 3)) if t >= A("r7") else 0.0
    keys = [(0, (1.3, X, 700)), (A("r2"), (1.0, X, 640)), (A("r3"), (1.35, X + 60, 1020)),
            (A("r4"), (0.9, X, 660)), (A("r5"), (1.0, X, 760)), (A("r6"), (1.0, X, 700)),
            (A("r7"), (0.95, X, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    thigh(cr)
    # the lower leg: drops away while the knee comes out, then turns round (a flip) and rises to the thigh
    km = "cry" if t < A("r2") else "shock"
    fm = "calm" if t < A("r3") else ("shock" if t < A("r6") else ("worried" if t < A("r7", "weirdest") else "happy"))
    ax = X
    ay = lerp(ANKLE_Y + 60 * cut, KNEE_Y + 100, rise)
    flip = math.cos(math.pi * turn)                                              # 1 -> -1: foot now points back
    with at(cr, ax, ay, 1.0):
        cr.scale(flip if abs(flip) > 0.05 else 0.05, 1.0)
        lower_leg(cr, t, fm, tl.speaking("foot", t), flex=flex, shin=lerp(ANKLE_Y - KNEE_Y - 20, 70, rise))
    if rise > 0.95:
        stitches(cr, [(X - 70 + 7 * k, KNEE_Y + 40) for k in range(20)], 1.0)
    prosthesis(cr, pros)
    # the knee with the tumour, lifted away
    if cut < 1:
        with at(cr, 0, -700 * cut):
            knee(cr, t, km, tl.speaking("knee", t))
        if cut > 0:
            for k in range(4):
                u = (t * 1.5 + k / 4) % 1
                blob(cr, X - 60 + 40 * k, KNEE_Y + 30 + 200 * u, 6, 9, BLOOD, seed=1330 + k, amp=0, lw=2,
                     stroke=BLOOD_D)
            line(cr, [(X - 85, KNEE_Y - 40), (X + 85, KNEE_Y - 40)], 6, BLOOD, seed=1335, amp=0)
    # the scalpel
    if t < A("r6", end=True):
        sx, sy = (600, 420) if t < A("r2", "go") else (620, 360)
        scalpel(cr, t, sx, sy, 1.05, -0.5, talking=tl.speaking("scalpel", t), mood="happy")
    # tags
    if t < A("r2", "go"):
        label(cr, "Bone tumor", 150, 520, X - 40, KNEE_Y + 10)
        label(cr, "Knee", 560, 700, X + 60, KNEE_Y + 10)
    if A("r6", "ankle") <= t:
        label(cr, "Ankle = new knee", 170, 560, X - 20, KNEE_Y + 100)
    if pros > 0.5:
        label(cr, "Prosthetic leg", 560, 980, X + 20, 980)
    for w in (A("r2", "go"), A("r5"), A("r7")):
        cue("hit", t, w)
    cue("whoosh", t, A("r5"))


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "backwards"), TWO_SHOT),
            (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT), (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT),
            (A("w6"), A_CLOSE), (A("w7"), DOC_CLOSE), (A("w7", "exactly"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    x, y, s = BED_A
    bed(cr, x)
    n = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t < A("w6"):
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w6") <= t:
        n.update(eyes="sly", mouth="smirk", arms=("point", "down"))
    patient(cr, "danny_b", x, y, s, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w6"):
        d.update(arms=("hold", "down"), eyes="happy" if A("w5") <= t < A("w6") else "dot")
    if A("w7") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    if A("w2", "rotationplasty") <= t < A("w4"):
        cr.save()
        cr.identity_matrix()
        label(cr, "Rotationplasty", 360, 320, size=48)
        cr.restore()
        cue("pop", t, A("w2", "rotationplasty"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_leg(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr, logo=False, name="Body Facts")   # made before the logo: stays as released
