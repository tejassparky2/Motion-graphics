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
from motion import pbody
from motion.clinic import watermark
from motion.engine import ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import GOLD, RED, tag
from motion.polish import OUTLINE, bold_text, camera, captions, counter, ellipse, enter, lin, paint, particles, \
    rrect, sign, stamp, stroke_line
from motion.pbody import blob, face, finish, step_card, tip_card, tube, spark, along, clinic, CLINIC_CAMS as C

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

PINK, PINK_D = hexc("#ff9fb0"), hexc("#e0788c")
VESSEL = hexc("#e8473f")
NERVE = hexc("#ffcf3f")
VPATH = [(80, 690), (220, 670), (380, 680), (540, 660), (660, 680)]          # the vessel along the roof of the mouth
NPATH = [(520, 700), (580, 600), (560, 480), (470, 360)]                    # the nerve up to the brain
BRAIN = (400, 300)
FOREHEAD = (190, 330)


def head_bg(cr, t):
    pbody.backdrop(cr, t, hexc("#ffd9c9"), hexc("#f2a99a"), seed=19)
    # the head in profile, facing left: skull outline with the forehead at the left
    cr.save()
    ellipse(cr, 380, 480, 330, 380)
    paint(cr, lin(0, 100, 0, 860, [(0, hexc("#f6c9a4")), (1, hexc("#e9aa82"))]), OUTLINE, 6)
    cr.restore()
    # the mouth below the roof (dark cavity) and the roof of the mouth (palate) itself
    rrect(cr, 90, 720, 560, 180, 80)
    paint(cr, lin(0, 720, 0, 900, [(0, hexc("#8a2a3a")), (1, hexc("#5a1424"))]), OUTLINE, 5)
    pbody.shape_fill(cr, [(80, 730), (200, 690), (380, 700), (560, 690), (660, 730), (600, 760), (380, 745),
                          (160, 760)], PINK, shadow=False)


def scene_head(cr, t, tl):
    A = tl.at
    squeeze = ease_out(seg(t, A("b2", "squeeze"), A("b2", "heat")))
    widen = ease_out(seg(t, A("b3", "open"), A("b3", "rush") + 0.3))
    w = lerp(lerp(30, 12, squeeze), 44, widen)
    alarm = A("b4", "alarm") - 0.3
    cams = [(0, (1.45, 380, 700)), (A("b2"), (1.6, 300, 660)), (A("b4"), (1.3, 470, 560)),
            (A("b5"), (1.3, 360, 480)), (A("b6"), (1.2, 400, 520)), (A("b7"), (1.5, 380, 700)),
            (A("b8"), (1.3, 440, 520))]
    cr.save()
    enter(cr, camera(t, cams), drift=0.004, t=t)
    head_bg(cr, t)
    tube(cr, VPATH, w, VESSEL, glow=widen)
    # warm blood rushing back in
    if widen > 0:
        for k in range(6):
            u = (t * 0.8 + k / 6) % 1
            x, y = along(VPATH, u)
            ellipse(cr, x, y, 8, 6)
            paint(cr, hexc("#ffb0a8"), None, 0)
    tube(cr, NPATH, 18, NERVE, glow=1.0 if alarm <= t < A("b7") else 0.0)
    if alarm <= t < A("b7"):
        for k in range(2):
            u = ((t - alarm) * 0.9 + k * 0.5) % 1
            x, y = along(NPATH, u)
            spark(cr, x, y, 0.9)
    # the brain, then the forehead where the pain is felt
    blob(cr, BRAIN[0], BRAIN[1], 150, 110, hexc("#f7a8c0"))
    for k in range(5):
        stroke_line(cr, [(BRAIN[0] - 110 + 50 * k, BRAIN[1] - 40), (BRAIN[0] - 90 + 50 * k, BRAIN[1] + 10),
                               (BRAIN[0] - 110 + 50 * k, BRAIN[1] + 50)], 4, hexc("#c75f7b"))
    if A("b7") <= t:
        bold_text(cr, "?", BRAIN[0] + 140, BRAIN[1] - 60, 110, GOLD)
    # the talking characters
    pm = "wide" if t < A("b2") else ("worried" if t < A("b5") else ("open" if t < A("b8") else "happy"))
    face(cr, t, 370, 728, 1.0, pm, tl.speaking("palate", t))
    vx, vy = along(VPATH, 0.3)
    vm = "angry" if A("b2") <= t < A("b3") else "happy"
    blob(cr, vx, vy - 14, 70 + 12 * widen, 56 + 10 * widen, VESSEL)
    face(cr, t, vx, vy - 24, 0.85, vm, tl.speaking("vessel", t))
    nx, ny = along(NPATH, 0.45)
    nm = "shock" if alarm <= t < A("b6") else ("happy" if t >= A("b8") else "open")
    blob(cr, nx, ny, 68, 58, NERVE)
    face(cr, t, nx, ny - 10, 0.85, nm, tl.speaking("nerve", t))
    # the ice cream arriving, frost on the palate
    if t < A("b3"):
        u = ease_out(seg(t, 0.0, 0.5))
        x = lerp(-150, 230, u)
        cr.move_to(x - 50, 830)
        cr.line_to(x + 50, 830)
        cr.line_to(x, 960)
        cr.close_path()
        paint(cr, lin(0, 830, 0, 960, [(0, hexc("#f2c27a")), (1, hexc("#c98a3a"))]), OUTLINE, 5)   # the cone
        ellipse(cr, x, 800, 70, 60)
        paint(cr, pbody.rad(x - 20, 780, 80, [(0, hexc("#ffe0ec")), (1, hexc("#ff8fb8"))]), OUTLINE, 5)
        particles(cr, t, 19, 14, hexc("#e9f6ff"), area=(60, 640, 600, 120), r=(2, 5), speed=8)
    tag(cr, t, 0.4, 470, 660, "Roof of mouth", end=A("b2") - 0.2)
    cr.restore()
    # signs and stamps (screen space)
    sign(cr, t, A("b1", "freezing") - 0.2, 360, 300, "-2°C", col=hexc("#4aa3f0"), size=64, end=A("b2"))
    sign(cr, t, A("b3", "warm"), 360, 300, "WARM BLOOD IN", col=RED, size=50, end=A("b4"))
    if A("b6", "forehead") - 0.1 <= t < A("b7"):
        stamp(cr, t, A("b6", "forehead") - 0.1, 220, 300, "OUCH!", size=70)


def scene_ward(cr, t, tl):
    A = tl.at
    cams = [(A("w1") - 0.1, C["mike"]), (A("w1", "brain"), C["two"]), (A("w2"), C["doc"]), (A("w3"), C["two"]),
            (A("w5"), C["doc"]), (A("w6"), C["two"]), (A("w8"), C["danny"]), (A("w9"), C["both"])]
    cam = camera(t, cams, dur=0.3)
    mike = dict(eyes="wide", mouth="o")
    if A("w2") <= t < A("w8"):
        mike = dict(eyes="open", mouth="smile")
    if A("w8") <= t:
        mike = dict(eyes="happy", mouth="grin")
    doc = dict(arms=("point", "down")) if A("w3") <= t < A("w8") else dict(arms=("hold", "down"))
    if A("w9") <= t:
        doc = dict(eyes="half", mouth="smug", arms=("hips", "down"))
    danny = dict(eyes="happy", mouth="grin", arms=("wave", "down")) if A("w8") <= t else dict()
    clinic(cr, t, tl, cam, mike, danny, doc)
    step_card(cr, t, A("w3"), 1, "Something very cold touches the roof of your mouth.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The vessels squeeze, then open wide again.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "A face nerve senses it: pain in the forehead.", end=A("w6") - 0.05)
    if A("w6", "minute") - 0.4 <= t < A("w7"):
        counter(cr, t, A("w6", "minute") - 0.4, 360, 330, 60, size=110, dur=1.0, suffix=" s",
                sub="usually gone within a minute")
    tip_card(cr, t, A("w7"), "Eat cold things slowly.", "ok", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_head)(cr, t, tl)
    cr.restore()
    finish(cr)
    captions(cr, t, tl)
    watermark(cr)
