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

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.explain import along, googly, sign, step_card, tip_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip

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

# ---------------------------------------------------------------- a leg, cut open (side view, sitting on a chair)
SKIN, SKIN_NUMB = hexc("#f6c9a4"), hexc("#cfc6d8")
MUSCLE = hexc("#c4544b")
BONE = hexc("#f4ead6")
NERVE, ARTERY = hexc("#f2c032"), hexc("#d8363a")
# the thigh lies along the chair seat (left to right), the knee bends, the lower leg hangs down, the foot points left
THIGH = [(700, 300), (330, 300)]
KNEE = (300, 360)
SHIN = [(300, 360), (300, 720)]
LEG = [(720, 230), (330, 228), (250, 290), (240, 420), (250, 700), (240, 760), (90, 780), (70, 840), (330, 850),
       (370, 760), (370, 440), (400, 380), (720, 380)]
NPATH = [(720, 350), (420, 352), (340, 400), (330, 560), (320, 700), (250, 790), (130, 810)]   # sciatic nerve
APATH = [(720, 330), (430, 330), (355, 380), (345, 560), (335, 700), (270, 800), (150, 822)]   # artery
PINCH = 0.13                     # where the chair edge squeezes them (just behind the thigh)
FOOT = (170, 810)


def leg(cr, t, numb, press):
    cr.set_source_rgba(*hexc("#bfe3ef"))
    cr.paint()
    # the chair: seat under the thigh, its front edge pressing up into the back of the thigh
    shape(cr, rrect_pts(380, 380 - 8 * press, 400, 60, 14, 16), hexc("#8f6f4c"), seed=4400, amp=0, lw=4)
    shape(cr, rrect_pts(700, 440, 40, 400, 10, 16), hexc("#7a5c3e"), seed=4401, amp=0, lw=4)
    shape(cr, LEG, SKIN, seed=4402, amp=0, lw=4.5)
    # muscle under the skin
    shape(cr, [(710, 250), (340, 250), (275, 300), (268, 420), (275, 700), (345, 700), (350, 440), (380, 365),
               (710, 362)], hexc("#e58f88"), seed=4403, amp=0, lw=3)
    # bones: thigh bone (femur), kneecap, shin bone (tibia), foot bones
    line(cr, [(700, 290), (330, 290)], 40, BONE, seed=4404, amp=0)
    line(cr, [(700, 290), (330, 290)], 4, hexc("#d9c7a3"), seed=4405, amp=0)
    shape(cr, rrect_pts(250, 300, 70, 80, 30, 16), BONE, seed=4406, amp=0, lw=3.5)          # kneecap
    line(cr, [(300, 380), (300, 730)], 34, BONE, seed=4407, amp=0)
    line(cr, [(300, 740), (240, 780), (110, 800)], 22, BONE, seed=4408, amp=0)
    if numb > 0:           # the numb foot goes grey
        shape(cr, [(260, 740), (240, 760), (90, 780), (70, 840), (330, 850), (360, 760)],
              (*SKIN_NUMB[:3], numb), seed=4409, amp=0, lw=0, stroke=None)


def scene_leg(cr, t, tl):
    A = tl.at
    lift = ease_out(seg(t, A("n6", "stood") - 0.2, A("n6", "stood") + 0.4))
    press = 1 - lift
    awake = A("n6") <= t
    numb = 1.0 if not awake else max(0.0, 1 - seg(t, A("n6"), A("n8")))
    FOOTC, THIGHC, WIDE = (1.5, 240, 820), (1.4, 480, 360), (0.95, 400, 600)
    keys = [(0, FOOTC), (A("n2"), THIGHC), (A("n3"), THIGHC), (A("n4"), FOOTC), (A("n5"), THIGHC), (A("n6"), WIDE),
            (A("n7"), (1.25, 330, 520)), (A("n8"), FOOTC)]
    set_camera(camera(t, keys))
    enter_world(cr)
    leg(cr, t, numb, press)
    vessel(cr, APATH, lerp(16, 6, press) if t >= A("n3") - 0.4 else 16, ARTERY, seed=4410)
    vessel(cr, NPATH, 12, NERVE if not awake else hexc("#ffe066"), seed=4420)
    # messages piling up at the squeezed spot (before), messy sparks running down (after)
    if not awake and A("n2") <= t:
        for k in range(3):
            x, y = along(NPATH, PINCH - 0.03 - 0.03 * k)
            shape(cr, rrect_pts(x - 18, y - 30, 36, 24, 4, 8), WHITE, seed=4430 + k, amp=0, lw=2.5)
            line(cr, [(x - 18, y - 30), (x, y - 18), (x + 18, y - 30)], 2.5, INK, seed=4433 + k, amp=0)
        for k in range(2):
            x, y = along(NPATH, PINCH)
            line(cr, [(x - 30 + 60 * k, y - 46), (x - 18 + 36 * k, y - 22)], 5, hexc("#d8363a"), seed=4436 + k,
                 amp=0)
    if awake:
        for k in range(6):
            x, y = along(NPATH, (t * 1.2 + k / 6) % 1)
            zap(cr, x + 12 * math.sin(t * 22 + k), y, 0.5)
    # the talking parts
    nx, ny = along(NPATH, 0.24)         # faces sit on the nerve and the artery themselves, like the references
    nm = "angry" if A("n2") <= t < A("n6") else ("happy" if awake else "calm")
    blob(cr, nx + 6, ny + 4, 44, 38, NERVE if not awake else hexc("#ffe066"), seed=4440, amp=0, lw=3.5)
    googly(cr, t, nx + 6, ny - 6, 0.55, nm, tl.speaking("nerve", t), mouth_dy=28)
    vx, vy = along(APATH, 0.66)
    blob(cr, vx + 4, vy, 40, 36, ARTERY, seed=4441, amp=0, lw=3.5)
    googly(cr, t, vx + 4, vy - 8, 0.5, "worried" if t < A("n6") else "happy", tl.speaking("vessel", t), mouth_dy=28)
    fm = "sad" if not awake else ("shock" if t < A("n8") else "happy")
    googly(cr, t, 190, 795, 0.7, fm, tl.speaking("foot", t), mouth_dy=26)
    if A("n8") <= t:          # tiny ants marching on the foot
        for k in range(7):
            x = 90 + ((t * 80 + k * 34) % 230)
            y = 850 + 4 * math.sin(t * 12 + k)
            for j in range(3):
                dot(cr, x + j * 7, y, 4, INK)
    # labels, like the references
    if t < A("n2"):
        label(cr, "Foot", 120, 700, 160, 770)
    if A("n2") <= t < A("n4"):
        label(cr, "Sciatic nerve", 430, 170, 450, 350)
        label(cr, "Chair edge", 600, 480, 560, 400)
    if A("n3") <= t < A("n4"):
        label(cr, "Artery", 650, 120, 640, 328)
    if A("n5") <= t < A("n6"):
        label(cr, "Thigh bone", 520, 170, 520, 290)
    for w in (A("n2", "squished"), A("n6", "stood")):
        cue("hit", t, w)
    # screen-space signs
    if A("n5", "cut") <= t < A("n6"):
        sign(cr, t, A("n5", "cut"), "SIGNAL BLOCKED", y=250, col=hexc("#d8363a"), size=48)
    if A("n7", "messy") <= t < A("n8"):
        sign(cr, t, A("n7", "messy"), "RESTARTING...", y=250, size=52)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "asleep"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w8"), B_CLOSE), (A("w9"), NEXT_BED)]
    m = dict(eyes="sad", mouth="wobble", arms=("hold", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("w8") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w8") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w8"):
        d.update(arms=("hold", "down"))
    if A("w9") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    step_card(cr, t, A("w3"), 1, "Pressure squeezes a nerve and its blood supply.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "Messages can't get through: the foot goes numb.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Pressure off: the nerve restarts with messy signals.", end=A("w6") - 0.05)
    tip_card(cr, t, A("w6"), "Harmless. It fades within minutes.", "ok", end=A("w7") - 0.05)
    tip_card(cr, t, A("w7"), "It happens often, without any pressure.", "warn", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_leg)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
