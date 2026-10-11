"""Body Facts 21: "Why Your Foot Falls ASLEEP" — pins and needles. Polished style, step-by-step explanation.
Script approved by the owner.

Facts (sources in research_notes/body_facts_19-22.md):
- Sitting or leaning on a limb squeezes a nerve and the small vessels that feed it; signals can't pass the squeezed
  point (a conduction block), so the foot goes numb.
- When the pressure is released, blood returns and the nerve restarts, firing disorganised signals: the buzzing
  "pins and needles" (transient paresthesia). Harmless; fades within minutes.
- Frequent numbness or tingling without pressure can mean another cause: see a doctor (Cleveland Clinic; UPMC).
"""
import math

from motion.clinic import watermark
from motion.engine import ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import GOLD, tag
from motion.polish import OUTLINE, bold_text, camera, captions, ellipse, enter, paint, rrect, sign, lin
from motion.pbody import CLINIC_CAMS as C, along, blob, clinic, face, finish, shape_fill, spark, step_card, \
    tip_card, tube
from motion import pbody

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "foot": dict(voice="am_michael", speed=0.95),
    "nerve": dict(voice="af_heart", speed=0.95),
    "vessel": dict(voice="af_nova", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"asleep", "nerve", "squished", "blood", "numb", "buzzing", "ants", "pressure", "minutes"}

SCRIPT = [
    dict(id="n1", scene="leg", text="Hey! Why can't I feel anything down here?", speaker="foot"),
    dict(id="n2", scene="leg", text="He's been sitting on me. I'm squished, and my messages can't get through.",
         speaker="nerve"),
    dict(id="n3", scene="leg", text="And I'm squished too. So less blood reaches the nerve.", speaker="vessel"),
    dict(id="n4", scene="leg", text="So I'm not really asleep?", speaker="foot"),
    dict(id="n5", scene="leg", text="No. You're just cut off.", speaker="nerve"),
    dict(id="n6", scene="leg", text="Wait! He stood up! What's this buzzing?", speaker="foot"),
    dict(id="n7", scene="leg", text="That's me waking up. I'm firing messy signals while I restart.",
         speaker="nerve"),
    dict(id="n8", scene="leg", text="It feels like a thousand tiny ants!", speaker="foot"),
    dict(id="w1", scene="ward", text="Doctor, why does my foot fall asleep?", speaker="mike"),
    dict(id="w2", scene="ward", text="It's not asleep. Its nerve is blocked. Here's how it works.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Pressure squeezes a nerve, and the blood vessels that feed it.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. The nerve can't send messages properly, so your foot goes numb.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. When the pressure is gone, the nerve restarts and sends messy "
                                     "signals. That's the pins and needles.", speaker="doctor"),
    dict(id="w6", scene="ward", text="It's harmless, and it usually fades within minutes.", speaker="doctor"),
    dict(id="w7", scene="ward", text="But if it happens often, without any pressure, see a doctor.",
         speaker="doctor"),
    dict(id="w8", scene="ward", text="My whole leg fell asleep in class, bro.", speaker="danny", gap=0.3),
    dict(id="w9", scene="ward", text="And the rest of you?", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why Your Foot Falls ASLEEP 🦶⚡",
    alt_titles=["Pins and Needles Explained in 3 Steps ⚡", "Your Foot Isn't Asleep. Here's What Happens 🦶"],
    description="""Your foot doesn't really fall asleep. Its nerve gets blocked. 3 steps. 🦶⚡

1. Pressure squeezes a nerve, and the blood vessels that feed it.
2. The nerve can't send messages properly, so your foot goes numb.
3. When the pressure is gone, the nerve restarts and sends messy signals: that's the pins and needles.

It's harmless and usually fades within minutes. But if it happens often, without any pressure, see a doctor.

Sources: Cleveland Clinic, "What that pins-and-needles feeling really means"; UPMC HealthBeat, "Why does my foot fall asleep?"

(Cartoon, real facts. Not medical advice.)

💬 Where were you when your leg fell asleep? 😂 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#PinsAndNeedles", "#BodyFacts", "#Doctor"],
    tags=["foot fell asleep", "pins and needles", "why does my foot fall asleep", "paresthesia", "nerves",
          "body facts", "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Worst place your leg ever fell asleep? 😂 👇",
)

SKIN, NERVE, VESSEL = hexc("#f2c29b"), hexc("#ffcf3f"), hexc("#e8473f")
NPATH = [(250, 130), (270, 330), (300, 520), (330, 700), (360, 820)]
VPATH = [(330, 130), (350, 330), (380, 520), (410, 700), (440, 810)]
PINCH = 0.3                                   # where the weight squeezes (fraction along the leg)
FOOT = (470, 860)


def leg(cr, t):
    pbody.backdrop(cr, t, hexc("#e9e3fb"), hexc("#c7bdf0"), seed=21)
    shape_fill(cr, [(170, 60), (430, 60), (450, 400), (480, 760), (600, 820), (640, 900), (420, 930), (300, 900),
                    (250, 600), (190, 300)], SKIN)


def scene_leg(cr, t, tl):
    A = tl.at
    lift = ease_out(seg(t, A("n6", "stood") - 0.2, A("n6", "stood") + 0.4))
    press = 1 - lift
    awake = A("n6") <= t
    cams = [(0, (1.35, 440, 800)), (A("n2"), (1.3, 300, 400)), (A("n3"), (1.3, 380, 420)), (A("n4"), (1.35, 440, 800)),
            (A("n5"), (1.3, 300, 400)), (A("n6"), (1.05, 380, 560)), (A("n7"), (1.25, 320, 520)),
            (A("n8"), (1.4, 470, 820))]
    cr.save()
    enter(cr, camera(t, cams), drift=0.004, t=t)
    leg(cr, t)
    px, py = along(NPATH, PINCH)
    tube(cr, NPATH, 22, NERVE, glow=1.0 if awake else 0.0)
    tube(cr, VPATH, lerp(26, 10, press) if t >= A("n3") - 0.4 else 26, VESSEL)
    # the weight pressing on the thigh
    wy = lerp(py - 120, -200, lift)
    rrect(cr, 120, wy - 60, 380, 90, 20)
    paint(cr, lin(0, wy - 60, 0, wy + 30, [(0, hexc("#8a8f9c")), (1, hexc("#5a5f6a"))]), OUTLINE, 6)
    bold_text(cr, "HIS WEIGHT", 310, wy + 2, 40, hexc("#ffffff"))
    # messages piling up at the pinch (before), messy sparks along the nerve (after)
    if not awake and A("n2") <= t:
        for k in range(3):
            x, y = along(NPATH, PINCH + 0.05 + 0.05 * k)
            rrect(cr, x - 22, y - 14, 44, 28, 5)
            paint(cr, hexc("#ffffff"), OUTLINE, 3)
            pbody.stroke_line(cr, [(x - 22, y - 14), (x, y + 2), (x + 22, y - 14)], 3, OUTLINE, curve=False)
    if awake:
        for k in range(6):
            u = (t * 1.3 + k / 6) % 1
            x, y = along(NPATH, u)
            spark(cr, x + 14 * math.sin(t * 20 + k), y, 0.6)
    # characters
    nx, ny = along(NPATH, 0.55)
    nm = "angry" if A("n2") <= t < A("n6") else ("happy" if awake else "open")
    blob(cr, nx - 40, ny, 64, 54, NERVE)
    face(cr, t, nx - 40, ny - 8, 0.8, nm, tl.speaking("nerve", t))
    vx, vy = along(VPATH, 0.6)
    blob(cr, vx + 50, vy, 60, 50, VESSEL)
    face(cr, t, vx + 50, vy - 8, 0.75, "worried" if t < A("n6") else "happy", tl.speaking("vessel", t))
    numb = not awake
    fm = "sad" if numb else ("wide" if t < A("n8") else "happy")
    blob(cr, FOOT[0], FOOT[1], 110, 70, hexc("#c9c4d6") if numb else SKIN)
    face(cr, t, FOOT[0], FOOT[1] - 12, 0.85, fm, tl.speaking("foot", t))
    if A("n8") <= t:      # tiny ants marching on the foot
        for k in range(7):
            x = FOOT[0] - 90 + ((t * 80 + k * 30) % 180)
            y = FOOT[1] + 48 + 6 * math.sin(t * 12 + k)
            for j in range(3):
                ellipse(cr, x + j * 8, y, 5, 4)
                paint(cr, hexc("#2b1d16"), None, 0)
    tag(cr, t, A("n2", "squished") - 0.2, nx - 40, ny - 90, "Nerve", end=A("n4"))
    tag(cr, t, A("n3"), vx + 60, vy - 90, "Blood vessel", end=A("n4"))
    cr.restore()
    if A("n5", "cut") <= t < A("n6"):
        sign(cr, t, A("n5", "cut"), 360, 280, "SIGNAL BLOCKED", col=hexc("#e8473f"), size=52)
    if A("n7", "messy") <= t < A("n8"):
        sign(cr, t, A("n7", "messy"), 360, 280, "RESTARTING...", col=GOLD, size=56)


def scene_ward(cr, t, tl):
    A = tl.at
    cams = [(A("w1") - 0.1, C["mike"]), (A("w1", "asleep"), C["two"]), (A("w2"), C["doc"]), (A("w3"), C["two"]),
            (A("w5"), C["doc"]), (A("w6"), C["two"]), (A("w8"), C["danny"]), (A("w9"), C["both"])]
    cam = camera(t, cams, dur=0.3)
    mike = dict(eyes="sad", mouth="flat", arms=("down", "down"))
    if A("w2") <= t:
        mike = dict(eyes="open", mouth="smile")
    if A("w8") <= t:
        mike = dict(eyes="happy", mouth="grin")
    doc = dict(arms=("point", "down")) if A("w3") <= t < A("w8") else dict(arms=("hold", "down"))
    if A("w9") <= t:
        doc = dict(eyes="half", mouth="smug", arms=("hips", "down"))
    danny = dict(eyes="happy", mouth="grin", arms=("wave", "down")) if A("w8") <= t else dict()
    if A("w9") <= t:
        danny = dict(eyes="wide", mouth="o")
    clinic(cr, t, tl, cam, mike, danny, doc)
    step_card(cr, t, A("w3"), 1, "Pressure squeezes a nerve and its blood supply.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "Messages can't get through: the foot goes numb.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Pressure off: the nerve restarts with messy signals.", end=A("w6") - 0.05)
    tip_card(cr, t, A("w6"), "Harmless. It fades within minutes.", "ok", end=A("w7") - 0.05)
    tip_card(cr, t, A("w7"), "Often, and without any pressure", "warn", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_leg)(cr, t, tl)
    cr.restore()
    finish(cr)
    captions(cr, t, tl)
    watermark(cr)
