"""Body Facts 24: "Why Your Fingers WRINKLE in Water" — reference style (real fingertip cut-away, googly-eyed parts,
labels, then the masked doctor). Script approved by the owner.

Facts (sources in research_notes/body_facts_23-26.md):
- Water-induced finger wrinkling is driven by the sympathetic nerves: the small blood vessels in the finger pads
  constrict, the pulp loses volume, and the skin on top folds into wrinkles.
- Fingers with a damaged (cut) nerve don't wrinkle (Bull & Henry, BMJ 1977; O'Riain, BMJ 1973), which is also used
  as a bedside nerve test.
- The idea that wrinkles improve grip on wet objects (Kareklas et al. 2013) failed to replicate in a later study
  (Haseleu et al. 2014), so the doctor says "studies disagree".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.explain import along, googly, sign, stamp, step_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "skin": dict(voice="af_nova", speed=0.95),
    "nerve": dict(voice="am_michael", speed=0.95),
    "vessel": dict(voice="af_heart", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"water", "squeeze", "squeezing", "wrinkles", "purpose", "nerve", "nerves", "folds", "grip"}

SCRIPT = [
    dict(id="f1", scene="finger", text="Ten minutes in the bath. Here we go again.", speaker="skin"),
    dict(id="f2", scene="finger", text="Water detected! Blood vessels, squeeze!", speaker="nerve"),
    dict(id="f3", scene="finger", text="Squeezing! Less blood in the fingertip.", speaker="vessel"),
    dict(id="f4", scene="finger", text="So I'm the same size, but there's less under me. I fold up!",
         speaker="skin"),
    dict(id="f5", scene="finger", text="Wrinkles on purpose. Not just soaking.", speaker="nerve"),
    dict(id="w1", scene="ward", text="Doctor, why do my fingers go wrinkly in the bath?", speaker="mike"),
    dict(id="w2", scene="ward", text="It's not just water soaking in. Your nerves do it on purpose.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. When your fingers stay in water, a nerve signal is sent.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. Tiny blood vessels in the fingertips squeeze, so there's less "
                                     "tissue under the skin.", speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. The skin folds up into wrinkles.", speaker="doctor"),
    dict(id="w6", scene="ward", text="Proof? If the finger's nerve is damaged, it doesn't wrinkle.",
         speaker="doctor"),
    dict(id="w7", scene="ward", text="Some scientists think wrinkles help us grip wet things. But studies "
                                     "disagree.", speaker="doctor"),
    dict(id="w8", scene="ward", text="So my fingers turn into raisins on purpose, bro.", speaker="danny", gap=0.3),
    dict(id="w9", scene="ward", text="Grippy raisins.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why Your Fingers WRINKLE in Water 🫧",
    alt_titles=["Wrinkly Bath Fingers Explained in 3 Steps 🫧", "Your Nerves Wrinkle Your Fingers ON PURPOSE 😳"],
    description="""Wrinkly bath fingers aren't just water soaking in. Your nerves do it on purpose. 3 steps. 🫧

1. When your fingers stay in water, a nerve signal is sent.
2. Tiny blood vessels in the fingertips squeeze, so there's less tissue under the skin.
3. The skin folds up into wrinkles.

Proof: if the finger's nerve is damaged, it doesn't wrinkle. Some scientists think wrinkles help us grip wet things, but studies disagree.

Sources: Wilder-Smith & Chow, "Water-immersion wrinkling" (2003); O'Riain, "New and simple test of nerve function in hand", BMJ (1973); Haseleu et al., PLoS ONE (2014).

(Cartoon, real facts. Not medical advice.)

💬 How long until YOUR fingers go wrinkly? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#WrinklyFingers", "#BodyFacts", "#Doctor"],
    tags=["wrinkly fingers", "why do fingers wrinkle in water", "pruney fingers", "bath fingers", "nerves",
          "body facts", "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Raisin fingers after how many minutes? 🫧 👇",
)

# ---------------------------------------------------------------- a fingertip, cut open (side view, pointing right)
SKIN, SKIN_D = hexc("#f6c9a4"), hexc("#e2a47c")
PULP = hexc("#fbe0a8")
BONE = hexc("#f4ead6")
NAIL = hexc("#f7d9d9")
ARTERY, NERVE = hexc("#d8363a"), hexc("#f2c032")
WATER = 250                                 # the water line
Y0, Y1, TIPC, R = 380, 760, (460, 570), 190  # finger top, pad bottom, centre and radius of the rounded tip
VPTS = [(0, 690), (200, 692), (380, 688), (500, 660), (580, 600)]
NPTS = [(0, 722), (220, 724), (400, 716), (530, 680)]


def outline(wr, inset=0.0, lift=0.0):
    """The finger's outline; its underside (the pad) folds into waves as `wr` goes 0 to 1."""
    pts = [(-40, Y0 + inset), (TIPC[0], Y0 + inset)]
    for k in range(1, 13):                               # the rounded tip, top to bottom
        a = -math.pi / 2 + k * math.pi / 12
        r = R - inset - (lift if a > 0 else 0) * math.sin(max(0.0, a)) + (wr * 9 * math.sin(k * 2.3) if a > 0 else 0)
        pts.append((TIPC[0] + r * math.cos(a), TIPC[1] + r * math.sin(a)))
    for k in range(1, 21):                               # the pad, right to left, folding when wrinkled
        pts.append((TIPC[0] - k * 25, Y1 - inset - lift + wr * 14 * math.sin(k * 1.9)))
    pts.append((-40, Y1 - inset - lift))
    return pts


def finger(cr, t, wr, squeeze):
    cr.set_source_rgba(*hexc("#fff6e6"))
    cr.paint()
    shape(cr, rrect_pts(-300, WATER, 1300, 1000, 0, 16), hexc("#9ad6f0"), seed=6000, amp=0, lw=0, stroke=None)
    for k in range(10):                                  # bubbles
        y = (WATER + 800) - ((t * 60 + k * 83) % 800)
        dot(cr, 80 + (k * 71) % 640, y, 6 + k % 3, hexc("#ffffff", 0.6))
    shape(cr, outline(wr), SKIN, seed=6001, amp=0, lw=4.5)
    shape(cr, outline(wr * 0.4, inset=26, lift=24 * squeeze), PULP, seed=6002, amp=0, lw=3)     # the soft pad
    shape(cr, rrect_pts(-40, 500, 520, 120, 50, 16), BONE, seed=6003, amp=0, lw=3.5)             # finger bones
    line(cr, [(200, 502), (200, 618)], 4, hexc("#d9c7a3"), seed=6004, amp=0)                    # the joint
    shape(cr, [(300, 368), (560, 380), (645, 445), (628, 462), (560, 408), (300, 396)], NAIL, seed=6005, amp=0,
          lw=3.5)
    shape(cr, rrect_pts(-300, WATER, 1300, 1000, 0, 16), hexc("#5fb8e6", 0.15), seed=6006, amp=0, lw=0,
          stroke=None)
    line(cr, [(-300, WATER), (1000, WATER)], 5, hexc("#2f7fd6"), seed=6007, amp=0)


def scene_finger(cr, t, tl):
    A = tl.at
    sig = A("f2", "detected")
    squeeze = ease_out(seg(t, A("f3", "squeezing"), A("f3", "fingertip")))
    wr = ease_out(seg(t, A("f4", "fold") - 0.2, A("f4", "fold") + 0.8))
    TIP, WIDE, PAD = (1.3, 500, 560), (0.9, 330, 580), (1.3, 360, 660)
    keys = [(0, WIDE), (A("f1", "bath"), TIP), (A("f2"), (1.2, 330, 640)), (A("f3"), PAD), (A("f4"), TIP),
            (A("f4", "fold"), (1.1, 380, 600)), (A("f5"), (1.0, 340, 580))]
    set_camera(camera(t, keys))
    enter_world(cr)
    finger(cr, t, wr, squeeze)
    vessel(cr, VPTS, lerp(14, 5, squeeze), ARTERY, seed=6010)
    for k, (x, y) in enumerate([(200, 692), (380, 688)]):              # small branches into the pad
        vessel(cr, [(x, y), (x + 40, y + 24)], lerp(8, 3, squeeze), ARTERY, seed=6020 + k)
    vessel(cr, NPTS, 10, NERVE if t < sig else hexc("#ffe066"), seed=6030)
    if sig <= t < A("f5"):
        for k in range(2):
            x, y = along(NPTS, ((t - sig) * 1.1 + k * 0.5) % 1)
            zap(cr, x, y, 0.5)
    # the talking parts
    sm = "calm" if t < A("f2") else ("worried" if t < A("f4", "fold") else "shock" if t < A("f5") else "happy")
    googly(cr, t, 575, 555, 0.65, sm, tl.speaking("skin", t), mouth_dy=30)
    nx, ny = along(NPTS, 0.3)
    blob(cr, nx, ny + 44, 46, 38, NERVE, seed=6040, amp=0, lw=3.5)
    googly(cr, t, nx, ny + 36, 0.55, "angry" if sig <= t < A("f3") else "happy" if t >= A("f5") else "calm",
           tl.speaking("nerve", t), mouth_dy=26)
    vx, vy = along(VPTS, 0.55)
    blob(cr, vx, vy - 10, 44, 36, ARTERY, seed=6041, amp=0, lw=3.5)
    googly(cr, t, vx, vy - 18, 0.52, "angry" if A("f3") <= t < A("f4") else "calm", tl.speaking("vessel", t),
           mouth_dy=26)
    # labels, like the references
    if t < A("f2"):
        label(cr, "Fingertip", 560, 200, 560, 382)
        label(cr, "Nail", 230, 300, 360, 375)
        label(cr, "Water", 80, 300)
    if A("f2") <= t < A("f3"):
        label(cr, "Nerve", 120, 850, 120, 726)
        label(cr, "Bone", 100, 440, 100, 505)
    if A("f3") <= t < A("f4"):
        label(cr, "Blood vessel", 220, 850, 140, 694)
    if A("f4") <= t < A("f5"):
        label(cr, "Soft pad", 330, 860, 330, 740)
    for w in (sig, A("f3", "squeezing"), A("f4", "fold")):
        cue("hit", t, w)
    # screen-space signs
    if t < A("f2"):
        sign(cr, t, A("f1", "minutes") - 0.2, "10 MIN", y=250, col=hexc("#2f7fd6"))
    if A("f3", "less") <= t < A("f4"):
        sign(cr, t, A("f3", "less"), "LESS BLOOD", y=250, col=hexc("#d8363a"), size=52)
    stamp(cr, t, A("f5"), "NERVE-CONTROLLED", x=360, y=260, size=52)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "wrinkly"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
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
    step_card(cr, t, A("w3"), 1, "Fingers stay in water: a nerve signal is sent.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "Fingertip vessels squeeze: less tissue under the skin.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "The skin folds up into wrinkles.", end=A("w6") - 0.05)
    if A("w6", "if") <= t < A("w7"):
        sign(cr, t, A("w6", "if"), "NERVE DAMAGED = NO WRINKLES", y=690, col=hexc("#7a5bd0"), size=40)
    if A("w7", "grip") <= t < A("w8"):
        sign(cr, t, A("w7", "grip"), "BETTER GRIP? STILL DEBATED", y=690, col=hexc("#2f7fd6"), size=40)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_finger)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
