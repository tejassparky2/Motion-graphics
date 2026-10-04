"""Body Facts 2: "They Cut Into His Brain While He Was AWAKE" — the brain panics, then finds out it can't feel pain.

Facts (kept general and uncontroversial; sources in research_notes/body_facts_2-4.md):
- Brain tissue itself has no pain receptors (UCSF Brain Tumor Center; St George's NHS awake-craniotomy leaflet).
- In an awake craniotomy the scalp is numbed with local anaesthetic, the patient is usually sedated for the
  opening and closing, and is awake for the mapping so they can talk, count or name pictures; that tells the team
  which areas (speech, movement) to leave alone (UCSF; St George's NHS).
- Headache pain comes from pain-sensing nerves in the coverings (meninges) and blood vessels around the brain, not
  from brain tissue (NINDS; Levy et al. 2019).
"""
import math

from motion.captions import captions
from motion.engine import RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.clinic import A_CLOSE, BED_A, DOC_CLOSE, TWO_SHOT, bed, doctor, label, patient, room, sheet, \
    watermark
from motion.organs import brain, head_bandage
from motion.surgery import DRAPE, DRAPE_D, SKIN, SKIN_D, clamp, cut_line, drapes, ellipse, scalpel_tip, slit, syringe, \
    wound
from videos.kidney_donor import eyes, mouth, scalpel

# Voices: natural stock voices at their own pitch (owner: the pitched-up voices weren't clear), a touch slower.
# The doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "brain": dict(voice="af_heart", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
})                                   # the doctor speaks in the narrator voice (the owner's clone)
TAIL = 1.0
EMPHASIS = {"craniotomy", "brain", "awake", "pain", "sensors", "headaches"}   # bigger captions

SCRIPT = [
    dict(id="b1", scene="head", text="Hey! Who just opened the roof of my head?", speaker="brain"),
    dict(id="b2", scene="head", text="Relax, brain. It's just me, the scalpel. We're doing surgery today.", speaker="scalpel"),
    dict(id="b3", scene="head", text="Surgery? Then why is he still awake?", speaker="brain"),
    dict(id="b4", scene="head", text="He needs to stay awake, so he can talk to the doctors. Now hold still.", speaker="scalpel"),
    dict(id="b5", scene="head", text="No, no, please stop! This is going to hurt so much!", speaker="brain"),
    dict(id="b6", scene="head", text="Wait a second. I don't feel anything at all.", speaker="brain", gap=0.4),
    dict(id="b7", scene="head", text="Of course you don't. The brain has no pain sensors.", speaker="scalpel"),
    dict(id="b8", scene="head", text="So I feel every pain he has, but I can't feel my own?", speaker="brain"),
    dict(id="h1", scene="ward", text="Doctor, you operated on my brain while I was awake. Why didn't it hurt?",
         speaker="mike"),
    dict(id="h2", scene="ward", text="The brain itself has no pain sensors.", speaker="doctor"),
    dict(id="h3", scene="ward", text="We numbed your scalp. After that, the brain felt nothing.", speaker="doctor"),
    dict(id="h4", scene="ward", text="And you stayed awake, so you could talk while we worked. That told us which "
                                     "parts to leave alone.", speaker="doctor"),
    dict(id="h4b", scene="ward", text="This is called an awake craniotomy.", speaker="doctor"),
    dict(id="h5", scene="ward", text="Then why do I get headaches?", speaker="mike"),
    dict(id="h6", scene="ward", text="That pain comes from the layers and blood vessels around the brain. Not the "
                                     "brain itself.", speaker="doctor"),
    dict(id="h7", scene="ward", text="Doctor, did you find a brain in there?", speaker="mike", gap=0.3),
    dict(id="h8", scene="ward", text="Barely.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="They Cut Into His Brain… While He Was AWAKE 😳",
    alt_titles=["Why Brain Surgery Doesn't Hurt 🧠", "Your Brain Can't Feel Pain. Here's Why 😳"],
    description="""Surgeons opened his skull while he was wide awake. And his brain felt nothing. 🧠😳

Why? The brain itself has no pain sensors. In awake brain surgery the scalp is numbed, and the patient stays awake so they can talk while the surgeons work. That tells the team which parts of the brain to leave alone. So where do headaches come from? From pain-sensing nerves in the layers and blood vessels around the brain, not the brain itself.

(Funny cartoon, real facts. Not medical advice: talk to a doctor about your own health.)

💬 Would you stay awake for your own brain surgery? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Brain", "#BodyFacts", "#Doctor"],
    tags=["awake brain surgery", "brain can't feel pain", "awake craniotomy", "why doesn't brain surgery hurt",
          "brain facts", "where do headaches come from", "body facts", "doctor explains", "human body",
          "funny animation", "health facts"],
    pinned_comment="Be honest: could you stay awake while they operate on your brain? 😳 And what would you talk "
                   "about? 👇",
)

HX, HY = 360, 700                       # the patient's head on the table
WX, WY, WRX, WRY = 360, 520, 160, 105   # the window cut in the top of his head
BX, BY = WX, WY + 6                     # the brain, seen through it
SLIT = slit(WX, WY, WRX, -26)


def patient_head(cr, t, mood, hum=False):
    """Mike on the table, awake: the top of his head shaved for surgery, his face at the bottom."""
    hair = hexc("#2b1c14")
    for sx in (-1, 1):
        blob(cr, HX + sx * 262, HY + 110, 34, 56, SKIN_D, seed=420 + sx, amp=0.6, lw=3.5)        # ears
    shape(cr, ellipse(HX, HY, 268, 312), SKIN, seed=422, amp=0.8, lw=4.5)
    for sx in (-1, 1):                                                                       # hair at the sides
        shape(cr, [(HX + sx * 264, HY + 50), (HX + sx * 252, HY - 90), (HX + sx * 196, HY - 70),
                   (HX + sx * 222, HY + 70)], hair, seed=424 + sx, amp=0.6, lw=3)
    blob(cr, WX, WY + 8, 212, 150, hexc("#efd9bd"), seed=426, amp=0.6, lw=0, stroke=None)      # shaved patch
    for k in range(46):
        a, r = k * 2.39996, 0.25 + 0.75 * ((k * 0.618) % 1)
        dot(cr, WX + 196 * r * math.cos(a), WY + 8 + 136 * r * math.sin(a), 1.6, hexc("#8a7a6a", 0.6))
    blob(cr, HX - 150, HY + 205, 34, 18, hexc("#f2a0a0", 0.45), seed=427, amp=0.3, lw=0, stroke=None)   # cheeks
    blob(cr, HX + 150, HY + 205, 34, 18, hexc("#f2a0a0", 0.45), seed=428, amp=0.3, lw=0, stroke=None)
    eyes(cr, HX, HY + 120, 2.1, mood, 0.0, blink=(int(t * 10) % 37 == 0))
    line(cr, [(HX - 6, HY + 170), (HX + 12, HY + 205), (HX - 8, HY + 212)], 4, SKIN_D, seed=429, amp=0.3)   # nose
    mouth(cr, HX, HY + 250, 1.6, mood, False, t)
    # drape over his chin and shoulders
    shape(cr, [(-200, HY + 262), (180, HY + 282), (360, HY + 300), (540, HY + 282), (920, HY + 262), (920, 1700),
               (-200, 1700)], DRAPE, seed=430, amp=1.0, lw=4)
    for k in range(5):
        line(cr, [(60 + k * 150, HY + 300), (90 + k * 150, HY + 420)], 4, DRAPE_D, seed=431 + k, amp=0.8)
    if hum:   # he's fine: humming while the brain panics
        u = (t * 0.8) % 1
        write(cr, [("la la la", hexc("#2b3a66", 1 - u))], HX + 210, HY + 210 - 60 * u, 40, bold=True)


def ouch(cr, t, start, label, x0, y0, k):
    """A pain message from somewhere in the body flying into the brain."""
    u = ease_out(seg(t, start, start + 0.55))
    if t < start:
        return
    tx, ty = [(BX - 170, BY - 170), (BX + 170, BY - 120), (BX - 150, BY - 260)][k]
    x, y = lerp(x0, tx, u), lerp(y0, ty, u)
    a = 1 - seg(t, start + 1.4, start + 1.7)
    if a <= 0:
        return
    cr.push_group()
    with at(cr, x, y, 1.0, rot=0.08 * (k - 1)):
        blob(cr, 0, 0, 130, 46, WHITE, seed=410 + k, amp=0.5, lw=3.5)
        write(cr, [(label, RED)], 0, 13, 38, align="center", bold=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    if k == 0:
        cue("pop", t, start)


def scene_head(cr, t, tl):
    A = tl.at
    inject = seg(t, 0.0, 0.45)                                   # numbing shot in the scalp
    cut = seg(t, 0.35, A("b1", "roof") - 0.25)                   # the scalpel draws the cut
    open_u = ease_out(seg(t, A("b1", "roof") - 0.25, A("b1", "roof") + 0.35))
    flap = ease_out(seg(t, A("b1", "roof") - 0.1, A("b1", "roof") + 0.6))   # the piece of skull lifted out
    poke = A("b5", "hurt")
    touch = math.sin(math.pi * seg(t, poke, poke + 0.7)) if t >= poke else 0.0
    BRAIN, WIDE, MIKE = (1.8, BX, 600), (1.0, 360, 700), (1.6, HX, 860)
    keys = [(0, (1.3, 360, 620)), (A("b1", "roof"), BRAIN),
            (A("b2"), (1.3, 430, 520)), (A("b2", "surgery"), WIDE),
            (A("b3"), BRAIN), (A("b3", "awake"), MIKE),
            (A("b4"), (1.3, 430, 520)), (A("b4", "still"), (1.15, 380, 600)),
            (A("b5"), BRAIN), (poke, WIDE),
            (A("b6"), BRAIN),
            (A("b7"), (1.25, 400, 560)), (A("b7", "sensors"), (1.1, 360, 640)),
            (A("b8"), WIDE), (A("b8", "own"), BRAIN)]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    # ---- Mike, awake the whole time
    mm = "shock" if t < A("b1", "roof") + 0.4 else "calm"
    if A("b3", "awake") <= t < A("b4"):
        mm = "happy"
    if poke <= t < A("b7"):
        mm = "happy"
    patient_head(cr, t, mm, hum=poke <= t < A("b7"))
    # ---- the brain's mood follows the scene
    mood, shake = "shock", 0.0
    if A("b2") <= t < A("b3"):
        mood = "worried"
    if A("b3") <= t < A("b5"):
        mood, shake = "shock", (2.0 if t >= A("b3", "awake") else 0)
    if A("b5") <= t < A("b6"):
        mood, shake = ("cry", 2.5) if t < poke else ("shock", 1.0)
    if A("b6") <= t < A("b7"):
        mood = "calm"
    if A("b7") <= t < A("b8"):
        mood = "shock"
    if A("b8") <= t:
        mood = "sad" if t < A("b8", "own") else "worried"

    def inside(c):
        brain(c, t, BX, BY, 0.85, mood, tl.speaking("brain", t), look=-0.6 if A("b2") <= t < A("b5") else 0,
              shake=shake, squish=touch)
    tip = None
    if open_u <= 0:
        tip = cut_line(cr, SLIT, cut)
    else:
        wound(cr, t, WX, WY, WRX, WRY, open_u, inside, bone=True)
    if 0 < flap < 1:   # the bone flap lifts out and away
        with at(cr, lerp(WX, WX + 330, flap), lerp(WY, WY - 520, flap), 1.0, rot=1.2 * flap):
            shape(cr, ellipse(0, 0, WRX - 20, (WRY - 20) * min(1.0, 0.3 + open_u)), hexc("#f2e6cf"), seed=440,
                  amp=0.4, lw=3.5)
            blob(cr, 0, 0, WRX - 40, (WRY - 40) * 0.6, hexc("#e8d6b5"), seed=441, amp=0.4, lw=0, stroke=None)
    # ---- clamps hold the cut open once it's open
    if open_u >= 1:
        hold = ease_out(seg(t, A("b1", "roof") + 0.35, A("b1", "roof") + 0.75))
        cm = "happy" if t < A("b5") or t >= A("b7") else "worried"
        clamp(cr, t, lerp(WX - WRX - 260, WX - WRX + 8, hold), WY - 6, -1, 0.75, cm, look=0.5)
        clamp(cr, t, lerp(WX + WRX + 260, WX + WRX - 8, hold), WY - 6, 1, 0.75, cm, look=0.5)
    # ---- the numbing shot
    if t < 0.8:
        lift = ease_out(seg(t, 0.5, 0.8))
        syringe(cr, t, WX + 110, WY - 20 - 500 * lift, 0.9, 0.5, inject)
    # ---- the scalpel: cuts, then hovers, then boops the brain
    sc = 1.15
    if t < A("b1", "roof") - 0.25:
        px, py = tip if tip is not None else SLIT[0]
        rot = math.pi - 0.25
        sx, sy = scalpel_tip(px, py, rot, sc)
    else:
        rot = 2.7
        sx, sy = 540, 330
        if A("b4", "still") <= t < poke:
            u = ease_out(seg(t, A("b4", "still"), poke))
            rot = lerp(2.7, math.pi - 0.15, u)
            sx, sy = scalpel_tip(lerp(470, BX + 30, u), lerp(250, BY - 70, u), rot, sc)
        elif t >= poke:
            rot = math.pi - 0.15
            sx, sy = scalpel_tip(BX + 30, BY - 70 + 40 * touch, rot, sc)
            if t >= A("b7"):
                rot, sx, sy = 2.7, 540, 330
    if t >= 0.4:
        scalpel(cr, t, sx, sy, sc, rot, talking=tl.speaking("scalpel", t),
                mood="happy" if t < A("b5") or t >= A("b7") else "calm")
    # ---- pain messages from the rest of the body pour into the brain
    if A("b8") <= t:
        for k, (lab, x0, y0, w) in enumerate([("STUBBED TOE!", 120, 1100, "feel"), ("PAPER CUT!", 700, 980, "every"),
                                              ("HOT TEA!", 90, 300, "pain")]):
            ouch(cr, t, A("b8", w), lab, x0, y0, k)
    # ---- screen text
    # ---- anatomy tags, like the references
    if t < A("b1", "roof") - 0.25:
        label(cr, "Scalp (numbed)", 250, 360, 300, 450)
    elif t < A("b5"):
        label(cr, "Skull", 205, 395, 228, 470)
        label(cr, "Brain", 500, 395, 430, 480)
    if A("b7", "sensors") <= t < A("b8"):
        label(cr, "Pain sensors: 0", 500, 380, 420, 470, size=30)
        cue("pop", t, A("b7", "sensors"))
    for w in (A("b3", "awake"), poke, A("b6", "anything"), A("b1", "roof") - 0.25):
        cue("hit", t, w)
    cue("whoosh", t, A("b1", "roof") - 0.1)
    cue("scribble", t, 0.35, 0.6)


# ------------------------------------------------------------------ the doctor's room, after the surgery
def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("h1") - 0.1, A_CLOSE), (A("h1", "hurt"), TWO_SHOT),
            (A("h2"), DOC_CLOSE), (A("h3"), TWO_SHOT), (A("h4"), DOC_CLOSE), (A("h4", "parts"), TWO_SHOT),
            (A("h4b"), DOC_CLOSE), (A("h5"), A_CLOSE), (A("h6"), DOC_CLOSE), (A("h6", "itself"), TWO_SHOT),
            (A("h7"), A_CLOSE), (A("h8"), DOC_CLOSE), (A("h8", "barely"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    x, y, s = BED_A
    bed(cr, x)
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("h2") <= t < A("h5"):
        m.update(eyes="happy", mouth="grin")
    if A("h5") <= t < A("h6"):
        m.update(eyes="sad", mouth="sad", arms=("face", "down"))
    if A("h6") <= t < A("h7"):
        m.update(eyes="dot", mouth="smile")
    if A("h7") <= t:
        m.update(eyes="sly", mouth="smirk", arms=("point", "down"))
    if A("h8", "barely") <= t:
        m.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "mike_b", x, y, s, t, talking=tl.speaking("mike", t), **m)
    with at(cr, x, y, s):
        head_bandage(cr, 0, 0, t)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("h2") <= t < A("h7"):
        d.update(arms=("hold", "down"), eyes="happy" if A("h4") <= t < A("h5") else "dot")
    if A("h7") <= t < A("h8"):
        d.update(eyes="wide")
    if A("h8") <= t:
        d.update(eyes="sly", arms=("down", "down"))
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_head(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
