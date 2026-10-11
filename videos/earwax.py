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

from motion.clinic import watermark
from motion.engine import ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import tag
from motion.polish import OUTLINE, camera, captions, ellipse, enter, lin, paint, particles, rrect, sign, stamp
from motion.pbody import CLINIC_CAMS as C, blob, clinic, face, finish, shape_fill, step_card, tip_card
from motion import pbody

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

SKIN, WAX, BUD = hexc("#f2b59a"), hexc("#f2b632"), hexc("#ffffff")
CANAL_Y = 560


def ear(cr, t, move):
    pbody.backdrop(cr, t, hexc("#ffe9d6"), hexc("#f6c8a8"), seed=22)
    # the ear canal: a tunnel from the outside (left) to the eardrum (right)
    shape_fill(cr, [(-60, CANAL_Y - 210), (700, CANAL_Y - 170), (760, CANAL_Y - 220), (760, CANAL_Y + 230),
                    (700, CANAL_Y + 170), (-60, CANAL_Y + 210)], SKIN)
    rrect(cr, -60, CANAL_Y - 120, 740, 240, 110)
    paint(cr, lin(0, CANAL_Y - 120, 0, CANAL_Y + 120, [(0, hexc("#7a3a3a")), (1, hexc("#4a1e22"))]), OUTLINE, 5)
    ellipse(cr, 690, CANAL_Y, 30, 110)
    paint(cr, hexc("#f7d8c8"), OUTLINE, 4)                                  # the eardrum
    # the skin "escalator": stripes on the canal wall moving outward (left)
    for k in range(14):
        x = 700 - ((move * 60 + k * 54) % 760)
        for y in (CANAL_Y - 112, CANAL_Y + 112):
            pbody.stroke_line(cr, [(x, y - 10), (x - 14, y + 10)], 4, hexc("#c98a70"), curve=False)


def scene_ear(cr, t, tl):
    A = tl.at
    move = t if A("e2") <= t else 0.0
    bud_in = ease_out(seg(t, A("e4") - 0.3, A("e4") + 0.4))
    push = ease_out(seg(t, A("e5", "deeper"), A("e5", "tight") + 0.3))
    cams = [(0, (1.35, 360, 580)), (A("e2"), (1.1, 360, 600)), (A("e3"), (1.0, 380, 680)), (A("e4"), (1.2, 260, 560)),
            (A("e5"), (1.2, 470, 580)), (A("e6"), (1.15, 360, 600))]
    cr.save()
    enter(cr, camera(t, cams), drift=0.004, t=t)
    ear(cr, t, move)
    particles(cr, t, 22, 12, hexc("#d9c9a8"), area=(0, CANAL_Y - 80, 680, 160), r=(2, 4), speed=6)
    # the wax: drifts outward with the skin, gets pushed deeper by the bud
    wx = 420 - 0.15 * (move * 20 % 400) * (1 - bud_in) + 220 * push
    wy = CANAL_Y + 20
    wm = "happy" if t < A("e4") else ("angry" if t < A("e6") else "happy")
    blob(cr, wx, wy, 80 + 10 * push, 64 - 8 * push, WAX)
    face(cr, t, wx, wy - 10, 0.9, wm, tl.speaking("wax", t))
    # the skin's face on the canal wall
    sm = "happy" if t < A("e4") else ("worried" if t < A("e6") else "happy")
    blob(cr, 200, CANAL_Y - 160, 70, 50, SKIN)
    face(cr, t, 200, CANAL_Y - 170, 0.75, sm, tl.speaking("skin", t))
    # the cotton bud
    if A("e4") - 0.3 <= t:
        bx = lerp(-300, lerp(160, 360, push), bud_in)
        rrect(cr, bx - 420, CANAL_Y - 14, 420, 28, 12)
        paint(cr, hexc("#e8eef7"), OUTLINE, 4)
        blob(cr, bx + 20, CANAL_Y, 56, 40, BUD)
        face(cr, t, bx + 20, CANAL_Y - 6, 0.7, "happy" if t < A("e5") else "shock", tl.speaking("bud", t))
    tag(cr, t, 0.4, wx, wy - 100, "Earwax", end=A("e2"))
    cr.restore()
    if A("e2", "escalator") - 0.2 <= t < A("e3"):
        sign(cr, t, A("e2", "escalator") - 0.2, 360, 280, "<<< OUTWARD", col=hexc("#3fbf6a"), size=56)
    if A("e3", "chews") - 0.2 <= t < A("e4"):
        sign(cr, t, A("e3", "chews") - 0.2, 360 + 10 * math.sin(t * 9), 280, "CHEW, CHEW", col=hexc("#ff8a3c"), size=58)
    if A("e5", "deeper") <= t < A("e6"):
        stamp(cr, t, A("e5", "deeper"), 360, 300, "PUSHED DEEPER", size=56)


def scene_ward(cr, t, tl):
    A = tl.at
    cams = [(A("w1") - 0.1, C["mike"]), (A("w1", "ears"), C["two"]), (A("w2"), C["doc"]), (A("w3"), C["two"]),
            (A("w5"), C["doc"]), (A("w6"), C["two"]), (A("w8"), C["danny"]), (A("w9"), C["both"])]
    cam = camera(t, cams, dur=0.3)
    mike = dict(eyes="open", mouth="smile", arms=("down", "down"))
    if A("w2") <= t:
        mike = dict(eyes="open", mouth="smile")
    if A("w6") <= t < A("w7"):
        mike = dict(eyes="wide", mouth="o")
    if A("w8") <= t:
        mike = dict(eyes="happy", mouth="grin")
    doc = dict(arms=("point", "down")) if A("w3") <= t < A("w8") else dict(arms=("hold", "down"))
    if A("w9") <= t:
        doc = dict(eyes="half", mouth="smug", arms=("hips", "down"))
    danny = dict(eyes="happy", mouth="grin", arms=("wave", "down")) if A("w8") <= t else dict()
    clinic(cr, t, tl, cam, mike, danny, doc)
    step_card(cr, t, A("w3"), 1, "Glands make wax that traps dust and germs.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The skin moves outward, carrying the wax.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Chewing and talking help it fall out.", end=A("w6") - 0.05)
    if A("w6") <= t < A("w7"):
        stamp(cr, t, A("w6", "cotton") - 0.1, 360, 320, "NO COTTON BUDS", size=54)
    tip_card(cr, t, A("w7"), "Ear feels blocked, or hearing drops", "warn", end=A("w8"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_ear)(cr, t, tl)
    cr.restore()
    finish(cr)
    captions(cr, t, tl)
    watermark(cr)
