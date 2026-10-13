"""Body Facts 22: "Your Ears Clean THEMSELVES" — earwax and the ear's self-cleaning. Polished style, step-by-step
explanation. Script approved by the owner.

Facts (sources in research_notes/body_facts_19-22.md):
- Earwax (cerumen) forms from gland secretions in the outer ear canal mixed with shed skin; it traps dust and
  germs and keeps the canal from drying out.
- The canal's skin migrates outward, carrying the wax, helped by jaw movement (chewing, talking); wax usually
  falls out by itself (AAO-HNSF Clinical Practice Guideline: Earwax, 2017).
- Don't put cotton swabs or small objects in the ear: they can push wax deeper or injure the canal. See a doctor
  if the ear feels blocked or hearing drops (AAO-HNS patient handout "Dos and Don'ts of Earwax").
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.explain import googly, sign, stamp, step_card, tip_card
from motion.kit import camera, enter_world, set_camera, whip

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "wax": dict(voice="af_heart", speed=0.95),
    "skin": dict(voice="am_onyx", speed=0.95),
    "bud": dict(voice="am_liam", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"earwax", "wax", "escalator", "outward", "jaw", "deeper", "cotton", "bud", "themselves"}

SCRIPT = [
    dict(id="e1", scene="ear", text="Hi! I'm earwax. I trap dust and germs, and stop the ear from drying out.",
         speaker="wax"),
    dict(id="e2", scene="ear", text="And I'm the skin of the ear canal. I slowly move outward, like a tiny "
                                    "escalator.", speaker="skin"),
    dict(id="e3", scene="ear", text="And when he chews or talks, his jaw helps push me out too.", speaker="wax"),
    dict(id="e4", scene="ear", text="Don't worry! I'm here to clean your ear!", speaker="bud"),
    dict(id="e5", scene="ear", text="No! You just push me deeper, and pack me in tight!", speaker="wax"),
    dict(id="e6", scene="ear", text="So leave us alone. We've got this.", speaker="skin"),
    dict(id="w1", scene="ward", text="Doctor, do I need to clean my ears?", speaker="mike"),
    dict(id="w2", scene="ward", text="Usually not. Your ears clean themselves. Here's how.", speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Glands in the ear canal make wax, which traps dust and germs.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. The skin inside slowly moves outward, carrying the wax with it.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. Chewing and talking help it along, until it falls out on its own.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="Ear doctors say don't put cotton buds in your ear. They can push wax deeper, "
                                     "or hurt it.", speaker="doctor"),
    dict(id="w7", scene="ward", text="If your ear feels blocked, or your hearing drops, see a doctor.",
         speaker="doctor"),
    dict(id="w8", scene="ward", text="So my ears have an escalator, bro.", speaker="danny", gap=0.3),
    dict(id="w9", scene="ward", text="Yes. And cotton buds just block the escalator.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Your Ears Clean THEMSELVES 👂",
    alt_titles=["Stop Using Cotton Buds in Your Ears 👂", "Your Ear Has an Escalator 😳"],
    description="""Your ears clean themselves. Here's how, in 3 steps. 👂😳

1. Glands in the ear canal make wax, which traps dust and germs.
2. The skin inside slowly moves outward, carrying the wax with it, like a tiny escalator.
3. Chewing and talking help it along, until it falls out on its own.

Ear doctors say don't put cotton buds in your ear: they can push wax deeper or hurt the ear. If your ear feels blocked or your hearing drops, see a doctor.

Sources: American Academy of Otolaryngology–Head and Neck Surgery Foundation, Clinical Practice Guideline: Earwax (Cerumen Impaction), 2017; AAO-HNS "Dos and Don'ts of Earwax".

(Cartoon, real facts. Not medical advice.)

💬 Be honest: do you still use cotton buds? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Earwax", "#BodyFacts", "#Doctor"],
    tags=["earwax", "ears clean themselves", "cotton buds in ears", "how to clean ears", "ear canal",
          "body facts", "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Be honest: cotton buds, yes or no? 👂 👇",
)

# ---------------------------------------------------------------- the ear, cut open (front view of the right ear)
SKIN, SKIN_D = hexc("#f6c9a4"), hexc("#e2a47c")
CANAL_WALL = hexc("#e9a08a")
BONE = hexc("#f4ead6")
WAX = hexc("#e0a12a")
DRUM = hexc("#f7d8c8")
CANAL_Y = 520
CANAL = [(150, CANAL_Y - 50), (300, CANAL_Y - 58), (420, CANAL_Y - 40), (480, CANAL_Y - 46), (480, CANAL_Y + 46),
         (420, CANAL_Y + 40), (300, CANAL_Y + 56), (150, CANAL_Y + 52)]
DRUM_X = 486


def ear(cr, t, move, jaw):
    cr.set_source_rgba(*hexc("#bfe3ef"))
    cr.paint()
    # skull bone (the side of the head) and the skin over it
    shape(cr, [(160, 120), (720, 120), (720, 900), (160, 900), (190, 700), (200, 340)], SKIN, seed=4500, amp=0,
          lw=4.5)
    shape(cr, [(330, 200), (720, 200), (720, 840), (330, 840), (360, 650), (340, 380)], BONE, seed=4501, amp=0,
          lw=4)
    # the outer ear (pinna) on the left
    shape(cr, [(200, 250), (110, 230), (40, 320), (40, 520), (80, 680), (150, 760), (210, 720), (200, 600),
               (170, 560), (180, 470)], SKIN, seed=4502, amp=0, lw=4.5)
    line(cr, [(110, 300), (70, 400), (80, 560), (130, 680)], 5, SKIN_D, seed=4503, amp=0)
    # the ear canal: a tunnel to the eardrum; its outer part has tiny hairs and wax glands
    shape(cr, CANAL, CANAL_WALL, seed=4504, amp=0, lw=4)
    shape(cr, [(150, CANAL_Y - 30), (300, CANAL_Y - 36), (480, CANAL_Y - 26), (480, CANAL_Y + 26),
               (300, CANAL_Y + 34), (150, CANAL_Y + 32)], hexc("#5a1e26"), seed=4505, amp=0, lw=0, stroke=None)
    for k in range(8):                                                  # the skin "escalator": stripes moving out
        x = 470 - ((move * 40 + k * 42) % 330)
        for y in (CANAL_Y - 42, CANAL_Y + 44):
            line(cr, [(x, y - 6), (x - 10, y + 6)], 3, hexc("#c47a68"), seed=4506 + k, amp=0)
    for k in range(6):                                                  # hairs and wax glands, outer third
        x = 170 + 26 * k
        line(cr, [(x, CANAL_Y - 48), (x + 10, CANAL_Y - 30)], 2.5, INK, seed=4520 + k, amp=0)
        dot(cr, x + 6, CANAL_Y - 56, 5, hexc("#f2c032"))
    # eardrum, the three tiny ear bones, the snail-shaped cochlea
    shape(cr, [(DRUM_X - 6, CANAL_Y - 70), (DRUM_X + 10, CANAL_Y - 60), (DRUM_X + 10, CANAL_Y + 60),
               (DRUM_X - 6, CANAL_Y + 70)], DRUM, seed=4530, amp=0, lw=3.5)
    shape(cr, rrect_pts(DRUM_X + 14, CANAL_Y - 90, 120, 180, 30, 16), hexc("#f7e6dc"), seed=4531, amp=0, lw=3)
    for k, (x, y, r) in enumerate([(DRUM_X + 34, CANAL_Y - 20, 14), (DRUM_X + 66, CANAL_Y - 40, 12),
                                   (DRUM_X + 98, CANAL_Y - 10, 12)]):
        blob(cr, x, y, r, r * 1.4, BONE, seed=4532 + k, amp=0, lw=3)
    with at(cr, 680, CANAL_Y - 30, 1.0):
        for k in range(18):
            a = k * 0.6
            r = 46 - 2.2 * k
            dot(cr, r * math.cos(a), r * math.sin(a), 12 - 0.4 * k, hexc("#f2a8b8"))
    line(cr, [(DRUM_X + 20, CANAL_Y + 80), (560, 760)], 16, hexc("#e8a090"), seed=4540, amp=0)   # tube to throat
    # the jaw joint just under the canal: moves when he chews and talks
    with at(cr, 300, CANAL_Y + 170, 1.0, rot=0.12 * jaw):
        shape(cr, [(-60, -40), (40, -50), (70, 0), (40, 260), (-50, 260), (-70, 0)], BONE, seed=4550, amp=0, lw=4)
        blob(cr, 0, -40, 50, 34, BONE, seed=4551, amp=0, lw=4)


def scene_ear(cr, t, tl):
    A = tl.at
    move = t if A("e2") <= t else 0.0
    jaw = math.sin(t * 7) if A("e3") <= t < A("e4") else 0.0
    bud_in = ease_out(seg(t, A("e4") - 0.3, A("e4") + 0.4))
    push = ease_out(seg(t, A("e5", "deeper"), A("e5", "tight") + 0.3))
    CAN, WIDE, JAW, DEEP = (1.6, 300, 520), (1.0, 380, 560), (1.25, 300, 600), (1.5, 400, 520)
    keys = [(0, CAN), (A("e2"), WIDE), (A("e3"), JAW), (A("e4"), (1.4, 200, 520)), (A("e5"), DEEP), (A("e6"), CAN)]
    set_camera(camera(t, keys))
    enter_world(cr)
    ear(cr, t, move, jaw)
    # the wax drifts outward with the skin; the cotton bud jams it deeper
    drift = 40 * math.sin(t * 0.8) if A("e2") <= t < A("e4") else 0.0
    wx = 300 - drift + 150 * push
    wy = CANAL_Y + 2
    wm = "happy" if t < A("e4") else ("angry" if t < A("e6") else "happy")
    blob(cr, wx, wy, 62 - 8 * push, 34, WAX, seed=4560, amp=0, lw=3.5)
    googly(cr, t, wx, wy - 6, 0.58, wm, tl.speaking("wax", t), mouth_dy=24)
    # the canal skin's face, on the wall
    sm = "happy" if t < A("e4") else ("worried" if t < A("e6") else "happy")
    googly(cr, t, 380, CANAL_Y - 84, 0.48, sm, tl.speaking("skin", t), mouth_dy=24)
    if A("e4") - 0.3 <= t:
        bx = lerp(-220, lerp(170, 300, push), bud_in)
        shape(cr, rrect_pts(bx - 360, CANAL_Y - 9, 360, 18, 8, 12), hexc("#e8eef7"), seed=4570, amp=0, lw=3)
        blob(cr, bx + 10, CANAL_Y, 40, 26, WHITE, seed=4571, amp=0, lw=3.5)
        googly(cr, t, bx + 10, CANAL_Y - 4, 0.4, "happy" if t < A("e5") else "shock", tl.speaking("bud", t),
               mouth_dy=22)
    # labels, like the references
    if t < A("e2"):
        label(cr, "Earwax", 300, 400, 300, CANAL_Y - 20)
        label(cr, "Ear canal", 200, 650, 230, CANAL_Y + 40)
    if A("e2") <= t < A("e3"):
        label(cr, "Eardrum", 470, 380, DRUM_X, CANAL_Y - 60)
        label(cr, "Canal skin", 250, 640, 300, CANAL_Y + 46)
    if A("e3") <= t < A("e4"):
        label(cr, "Jaw joint", 150, 760, 260, CANAL_Y + 160)
    for w in (A("e4"), A("e5", "deeper")):
        cue("hit", t, w)
    # screen-space signs
    if A("e2", "escalator") - 0.2 <= t < A("e3"):
        sign(cr, t, A("e2", "escalator") - 0.2, "<<< OUTWARD", y=250, col=hexc("#3fae5c"), size=52)
    if A("e3", "chews") - 0.2 <= t < A("e4"):
        sign(cr, t, A("e3", "chews") - 0.2, "CHEW, CHEW", y=250, col=hexc("#ff8a3c"), size=52)
    stamp(cr, t, A("e5", "deeper"), "PUSHED DEEPER", y=250, end=A("e6"))


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "ears"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w8"), B_CLOSE), (A("w9"), NEXT_BED)]
    m = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t < A("w7"):
        m.update(eyes="wide", mouth="o")
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
    step_card(cr, t, A("w3"), 1, "Glands make wax that traps dust and germs.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The skin moves outward, carrying the wax.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Chewing and talking help it fall out.", end=A("w6") - 0.05)
    stamp(cr, t, A("w6", "cotton") - 0.1, "NO COTTON BUDS", y=690, end=A("w7"))
    tip_card(cr, t, A("w7"), "Your ear feels blocked, or hearing drops.", "warn", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_ear)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
