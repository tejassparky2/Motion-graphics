"""Body Facts 19: "Why Ice Cream Hurts Your HEAD" — brain freeze. Polished style, step-by-step explanation.
Script approved by the owner.

Facts (sources in research_notes/body_facts_19-22.md):
- "Brain freeze" (cold stimulus headache, sphenopalatine ganglioneuralgia): something very cold on the roof of the
  mouth; the vessels there are thought to constrict and then rapidly dilate; the change is picked up by the
  trigeminal nerve and felt as pain in the forehead (referred pain). Usually gone within a minute; harmless.
- The 2012 Doppler study (Serrador et al., FASEB J. abstract) found only a trend toward increased anterior cerebral
  artery flow (p = 0.078), so the script says "Scientists still study the exact details".
- Prevention: eat cold things slowly. The "press your tongue to the roof of your mouth" trick isn't in the script
  (no evidence found).
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, seg, shape
from motion.explain import along, googly, sign, stamp, step_card, tip_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "palate": dict(voice="af_nova", speed=0.95),
    "vessel": dict(voice="af_heart", speed=0.95),
    "nerve": dict(voice="am_michael", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"freezing", "squeeze", "wide", "pain", "forehead", "brain", "cold", "slowly"}

SCRIPT = [
    dict(id="b1", scene="head", text="So cold! Something freezing just hit the roof of the mouth!", speaker="palate"),
    dict(id="b2", scene="head", text="Quick! I'll squeeze tight, to save heat.", speaker="vessel"),
    dict(id="b3", scene="head", text="Okay. Now I'll open wide, and rush warm blood back in!", speaker="vessel"),
    dict(id="b4", scene="head", text="Whoa! That sudden change! I'm sending a pain alarm!", speaker="nerve"),
    dict(id="b5", scene="head", text="But why does he feel it in his forehead?", speaker="palate"),
    dict(id="b6", scene="head", text="Because my message reaches the brain, and the brain blames the forehead.",
         speaker="nerve"),
    dict(id="b7", scene="head", text="So his brain isn't frozen at all?", speaker="palate"),
    dict(id="b8", scene="head", text="Nope. Just confused.", speaker="nerve"),
    dict(id="w1", scene="ward", text="Doctor, does brain freeze actually freeze my brain?", speaker="mike"),
    dict(id="w2", scene="ward", text="No. Doctors call it a cold stimulus headache. Here's how it works.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Something very cold touches the roof of your mouth.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. The blood vessels there quickly squeeze, then open wide again.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. A big nerve in your face senses the change, and your brain feels "
                                     "it as pain in your forehead.", speaker="doctor"),
    dict(id="w6", scene="ward", text="Scientists still study the exact details. But it's harmless, and it usually "
                                     "passes within a minute.", speaker="doctor"),
    dict(id="w7", scene="ward", text="To avoid it, eat cold things slowly.", speaker="doctor"),
    dict(id="w8", scene="ward", text="So brain freeze proves I have a brain, bro.", speaker="danny", gap=0.3),
    dict(id="w9", scene="ward", text="It's a start.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why Ice Cream Hurts Your HEAD 🧊🧠",
    alt_titles=["Brain Freeze Explained in 3 Steps 🧊", "Does Brain Freeze Freeze Your Brain? 🧠"],
    description="""Brain freeze doesn't freeze your brain. Here's what really happens, in 3 steps. 🧊🧠

1. Something very cold touches the roof of your mouth.
2. The blood vessels there quickly squeeze, then open wide again.
3. A big nerve in your face (the trigeminal nerve) senses the change, and your brain feels it as pain in your forehead.

Doctors call it a cold stimulus headache. Scientists still study the exact details, but it's harmless and usually passes within a minute. To avoid it, eat cold things slowly.

Sources: Serrador et al., "Cerebral vascular blood flow changes during 'brain freeze'", FASEB Journal (2012, abstract); Medical News Today, "Brain freeze: the science behind ice cream headache".

(Cartoon, real facts. Not medical advice.)

💬 What gives you the worst brain freeze? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#BrainFreeze", "#BodyFacts", "#Doctor"],
    tags=["brain freeze", "ice cream headache", "why does brain freeze happen", "cold stimulus headache",
          "trigeminal nerve", "body facts", "weird body facts", "doctor explains", "medical animation",
          "science explained"],
    pinned_comment="Ice cream, slushy or cold water: what gives YOU brain freeze? 🧊 👇",
)

# ---------------------------------------------------------------- the head, cut in half (side view, facing left)
SKIN, SKIN_D = hexc("#f6c9a4"), hexc("#e2a47c")
BONE, BONE_D = hexc("#f4ead6"), hexc("#d9c7a3")
BRAIN, BRAIN_D = hexc("#f2a8b8"), hexc("#c9768c")
CAVITY = hexc("#7a2a36")
TONGUE = hexc("#e2707e")
MUCOSA = hexc("#f19aa2")
ARTERY, NERVE = hexc("#d8363a"), hexc("#f2c032")

HEAD = [(130, 300), (150, 190), (260, 120), (420, 110), (560, 150), (660, 250), (700, 400), (680, 540), (620, 640),
        (590, 760), (600, 880), (360, 880), (330, 800), (220, 790), (140, 770), (120, 720), (110, 690), (90, 650),
        (100, 620), (70, 600), (40, 540), (80, 500), (100, 430), (120, 380)]
SKULL = [(160, 300), (175, 205), (270, 145), (420, 135), (550, 172), (640, 262), (672, 400), (650, 520), (600, 560),
         (520, 540), (430, 470), (330, 430), (210, 410), (165, 360)]
BRAIN_PTS = [(185, 300), (200, 220), (280, 168), (420, 158), (540, 192), (620, 272), (648, 395), (620, 470),
             (560, 500), (480, 470), (400, 420), (300, 400), (210, 385), (185, 345)]
NASAL = [(80, 500), (120, 440), (200, 430), (330, 450), (380, 520), (360, 560), (120, 560), (90, 545)]
MOUTH = [(110, 620), (140, 595), (330, 600), (410, 640), (420, 720), (330, 740), (160, 730), (120, 690)]
PALATE = [(110, 580), (330, 582), (400, 600), (400, 618), (330, 602), (112, 600)]
TONGUE_PTS = [(150, 690), (180, 640), (260, 622), (360, 640), (410, 700), (380, 745), (200, 745)]
VESSEL = [(130, 573), (220, 568), (300, 570), (380, 590)]
NERVE_PTS = [(300, 575), (330, 520), (380, 470), (440, 455)]
FOREHEAD = (175, 300)


def head(cr, t, cold):
    cr.set_source_rgba(*hexc("#bfe3ef"))
    cr.paint()
    shape(cr, HEAD, SKIN, seed=4000, amp=0, lw=4.5)
    shape(cr, SKULL, BONE, seed=4001, amp=0, lw=4)
    shape(cr, BRAIN_PTS, BRAIN, seed=4002, amp=0, lw=4)
    for k, (x, y) in enumerate([(260, 230), (360, 200), (460, 210), (560, 260), (300, 320), (420, 300), (530, 360),
                                (600, 330), (250, 360)]):   # the folds of the brain
        line(cr, [(x - 40, y), (x - 14, y - 16), (x + 10, y + 8), (x + 38, y - 6)], 4, BRAIN_D, seed=4010 + k, amp=0)
    blob(cr, 590, 520, 46, 30, hexc("#e89aae"), seed=4020, amp=0, lw=3.5)          # cerebellum
    line(cr, [(520, 500), (500, 600)], 34, BRAIN, seed=4021, amp=0)                 # brainstem
    blob(cr, 175, 330, 22, 18, hexc("#fbe5c8"), seed=4022, amp=0, lw=3)            # frontal sinus
    shape(cr, NASAL, MUCOSA, seed=4023, amp=0, lw=3.5)
    for k in range(3):                                                              # turbinates
        blob(cr, 230 + 10 * k, 470 + 28 * k, 70, 12, hexc("#f7b6bc"), seed=4024 + k, amp=0, lw=2.5)
    shape(cr, MOUTH, CAVITY, seed=4030, amp=0, lw=3.5)
    shape(cr, TONGUE_PTS, TONGUE, seed=4031, amp=0, lw=3.5)
    line(cr, [(220, 690), (340, 690)], 3, hexc("#c45362"), seed=4032, amp=0)
    shape(cr, PALATE, BONE if cold < 0.3 else hexc("#d9f1ff"), seed=4033, amp=0, lw=3.5)   # the roof of the mouth
    shape(cr, [(395, 600), (440, 640), (430, 660), (390, 618)], MUCOSA, seed=4034, amp=0, lw=3)   # soft palate
    for tx, ty in ((104, 600), (106, 712)):                                        # front teeth
        shape(cr, [(tx - 12, ty - 14), (tx + 12, ty - 14), (tx + 10, ty + 14), (tx - 10, ty + 14)], WHITE,
              seed=4035 + ty, amp=0, lw=3)
    line(cr, [(430, 640), (450, 760), (470, 880)], 40, CAVITY, seed=4038, amp=0)   # throat
    # the eye and the outer face, so it reads as a head at a glance
    blob(cr, 150, 410, 26, 18, WHITE, seed=4039, amp=0, lw=3)
    dot(cr, 140, 412, 8, INK)


def scene_head(cr, t, tl):
    A = tl.at
    cold = ease_out(seg(t, 0.2, A("b1", "freezing")))
    squeeze = ease_out(seg(t, A("b2", "squeeze"), A("b2", "heat")))
    widen = ease_out(seg(t, A("b3", "open"), A("b3", "rush") + 0.3))
    alarm = A("b4", "alarm") - 0.3
    PAL, BRN, FHD, WIDE = (1.7, 260, 600), (1.35, 400, 380), (1.6, 220, 380), (1.25, 380, 500)
    keys = [(0, WIDE), (A("b1", "freezing"), PAL), (A("b3"), (1.7, 280, 590)), (A("b4"), (1.25, 350, 520)),
            (A("b5"), FHD), (A("b6"), BRN), (A("b6", "forehead"), FHD), (A("b7"), WIDE), (A("b8"), BRN)]
    set_camera(camera(t, keys))
    enter_world(cr)
    head(cr, t, cold)
    # the artery along the roof of the mouth: squeezes, then opens wide
    w = lerp(lerp(14, 6, squeeze), 22, widen)
    vessel(cr, VESSEL, w, ARTERY, seed=4100)
    if widen > 0:
        for k in range(5):
            x, y = along(VESSEL, (t * 0.9 + k / 5) % 1)
            dot(cr, x, y, 4, hexc("#ffb0a8"))
    # the nerve from the roof of the mouth toward the brain; it lights up with the pain alarm
    lit = alarm <= t < A("b8")
    vessel(cr, NERVE_PTS, 9, NERVE if not lit else hexc("#ffe066"), seed=4110)
    if lit:
        for k in range(2):
            x, y = along(NERVE_PTS, ((t - alarm) * 1.2 + k * 0.5) % 1)
            zap(cr, x, y, 0.6)
        if A("b6", "brain") <= t:   # the brain sends the alarm to the forehead
            u = ((t - A("b6", "brain")) * 1.1) % 1
            zap(cr, lerp(420, FOREHEAD[0] + 10, u), lerp(260, FOREHEAD[1], u), 0.6)
    # the ice cream on the tongue, pressed to the roof of the mouth
    if t < A("b4"):
        u = ease_out(seg(t, 0.0, 0.5))
        x = lerp(-60, 210, u)
        blob(cr, x, 640, 56, 46, hexc("#ffd6e4"), seed=4120, amp=0, lw=3.5)
        for k in range(5):
            dot(cr, x - 30 + 15 * k, 628 + 6 * (k % 2), 3.5, hexc("#c9768c"))
    if A("b5") <= t:        # the forehead aches
        a = 0.35 + 0.25 * math.sin(t * 8)
        blob(cr, FOREHEAD[0] - 20, FOREHEAD[1], 50, 60, hexc("#d8363a", a), seed=4130, amp=0, lw=0, stroke=None)
    # the talking parts
    pm = "shock" if t < A("b2") else ("worried" if t < A("b5") else ("calm" if t < A("b8") else "happy"))
    googly(cr, t, 255, 540, 0.75, pm, tl.speaking("palate", t), mouth_dy=30)
    vm = "angry" if A("b2") <= t < A("b3") else "happy"
    googly(cr, t, 160, 528, 0.6, vm, tl.speaking("vessel", t), mouth_dy=30)
    nx, ny = along(NERVE_PTS, 0.55)
    nm = "shock" if alarm <= t < A("b6") else ("happy" if t >= A("b8") else "calm")
    googly(cr, t, nx + 44, ny - 10, 0.65, nm, tl.speaking("nerve", t))
    if A("b7") <= t:
        sign_x = 470
        cr.save()
        from motion.engine import write
        write(cr, [("?", hexc("#f2b632"))], sign_x, 250, 120, align="center", bold=True)
        cr.restore()
    # labels, like the references
    if t < A("b2"):
        label(cr, "Roof of mouth", 250, 500, 250, 585)
        label(cr, "Tongue", 290, 780, 290, 700)
    if A("b2") <= t < A("b4"):
        label(cr, "Blood vessel", 230, 500, 220, 566)
    if A("b4") <= t < A("b6"):
        label(cr, "Nerve", 470, 540, 400, 470)
    if A("b6") <= t:
        label(cr, "Brain", 440, 200, 440, 240)
        label(cr, "Forehead", 160, 220, 175, 280)
    for w_ in (A("b1", "freezing"), alarm, A("b6", "forehead")):
        cue("hit", t, w_)
    # screen-space signs
    sign(cr, t, A("b1", "freezing") - 0.2, "-2°C", y=260, col=hexc("#2f7fd6"), end=A("b2"))
    sign(cr, t, A("b3", "warm"), "WARM BLOOD IN", y=260, col=hexc("#d8363a"), size=48, end=A("b4"))
    stamp(cr, t, A("b6", "forehead"), "OUCH!", x=360, y=260, end=A("b7"))


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "brain"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w8"), B_CLOSE), (A("w9"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("w8") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w8") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w8"):
        d.update(arms=("hold", "down"))
    if A("w9") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    step_card(cr, t, A("w3"), 1, "Something very cold touches the roof of your mouth.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The vessels squeeze, then open wide again.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "A face nerve senses it: pain in the forehead.", end=A("w6") - 0.05)
    if A("w6", "harmless") <= t < A("w7"):
        sign(cr, t, A("w6", "harmless"), "HARMLESS: GONE IN UNDER A MINUTE", y=690, col=hexc("#3fae5c"), size=34)
    tip_card(cr, t, A("w7"), "Eat cold things slowly.", "ok", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_head)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
