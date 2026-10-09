"""Body Facts 16: "Your Stomach Is Full of ACID… So Why Doesn't It Digest Itself?" Script approved by the owner.

Facts (sources in research_notes/body_facts_15-18.md):
- Layered defence: surface mucous cells secrete a thick mucus gel; bicarbonate trapped in it neutralises acid that
  seeps in, keeping the cell surface near neutral pH; tight junctions between surface cells stop acid leaking
  between them; stem cells in the gastric glands keep replacing the surface cells.
- The surface epithelium is replaced about every 3-6 days (most often quoted: 3-5). Script: "about every three to
  five days" / "every few days".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import calendar
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "acid": dict(voice="am_liam", speed=0.95),
    "lining": dict(voice="af_heart", speed=0.95),
    "mucus": dict(voice="af_nova", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"acid", "mucus", "blanket", "bicarbonate", "cells", "days", "layers", "socks"}

SCRIPT = [
    dict(id="s1", scene="stomach", text="I'm stomach acid. I can break down a whole steak!", speaker="acid"),
    dict(id="s2", scene="stomach", text="Great. Just don't break me down.", speaker="lining"),
    dict(id="s3", scene="stomach", text="Why not? You're right here.", speaker="acid"),
    dict(id="s4", scene="stomach", text="Because I'm hiding under a thick blanket of mucus.", speaker="lining"),
    dict(id="s5", scene="stomach", text="And I carry a base that turns acid weak, right at the wall.",
         speaker="mucus"),
    dict(id="s6", scene="stomach", text="And if you still burn a few of my cells, I just grow new ones.",
         speaker="lining"),
    dict(id="s7", scene="stomach", text="How often?", speaker="acid"),
    dict(id="s8", scene="stomach", text="My surface is replaced every few days.", speaker="lining"),
    dict(id="w1", scene="ward", text="Doctor, why doesn't my stomach acid eat my stomach?", speaker="mike"),
    dict(id="w2", scene="ward", text="Your stomach protects itself in layers.", speaker="doctor"),
    dict(id="w3", scene="ward", text="First, a thick mucus layer, with bicarbonate that neutralises acid at the "
                                     "wall.", speaker="doctor"),
    dict(id="w4", scene="ward", text="Second, its cells are packed tightly, so acid can't slip between them.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="And its surface cells are replaced about every three to five days.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="So my stomach changes its skin twice a week, bro.", speaker="danny", gap=0.3),
    dict(id="w7", scene="ward", text="More often than you change your socks.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Your Stomach Is Full of ACID… So Why Doesn't It Digest Itself? 🧪",
    alt_titles=["Why Stomach Acid Doesn't Eat Your Stomach 🧪", "Your Stomach Rebuilds Itself Every Few Days 😳"],
    description="""Your stomach acid can break down a steak. So why doesn't it eat your stomach? 🧪😳

Your stomach protects itself in layers. A thick blanket of mucus covers the wall, and bicarbonate inside it neutralises the acid right at the surface. The cells are packed tightly, so acid can't slip between them. And the surface cells are constantly replaced: roughly every three to five days, you have a new stomach surface.

Sources: human physiology texts on the gastric mucosal barrier (mucus-bicarbonate layer, tight junctions, epithelial renewal every ~3-6 days).

(Cartoon, real facts. Not medical advice: see a doctor for ongoing stomach pain or heartburn.)

💬 Did you know your stomach rebuilds itself this fast? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#BodyFacts", "#Stomach", "#Doctor"],
    tags=["stomach acid", "why doesn't stomach acid digest the stomach", "stomach lining", "mucus layer",
          "bicarbonate", "body facts", "weird body facts", "digestion", "doctor explains", "medical animation"],
    pinned_comment="Your stomach gets a new surface every few days. 😳 What else should Doc explain next? 👇",
)

BG = hexc("#7a2e3a")
ACID, ACID_D = hexc("#9be38a"), hexc("#4f8a2a")
WALL, WALL_D = hexc("#f4a6a0"), hexc("#d67a7c")
MUCUS = hexc("#e8f6ff", 0.75)
WALL_Y = 820                          # top of the stomach wall (lining) at the bottom of the frame


def acid_char(cr, t, x, y, mood, talking):
    with at(cr, x, y + 6 * math.sin(t * 3), 1.0):
        blob(cr, 0, 0, 110, 90, ACID, seed=2300, amp=0, lw=4.5)
        for k in range(5):
            u = (t * 0.7 + k * 0.2) % 1
            blob(cr, -80 + 40 * k, -90 - 120 * u, 10, 10, hexc("#c6f5b8", 1 - u), seed=2301 + k, amp=0, lw=2)
        eyes(cr, 0, -14, 0.95, mood)
        mouth(cr, 0, 34, 0.8, mood, talking, t)


def wall(cr, t, mood, talking, mucus_u, shed_u, burn):
    """The stomach lining: a row of cells along the bottom with a face; mucus slides over it."""
    shape(cr, [(-200, WALL_Y), (920, WALL_Y), (920, 1800), (-200, 1800)], WALL_D, seed=2310, amp=0, lw=0, stroke=None)
    for k in range(12):
        x = -40 + 70 * k
        old = shed_u > 0 and k in (5, 6) and shed_u < 1
        y = WALL_Y + (40 * shed_u if old else 0)
        col = hexc("#b35656") if (k in (5, 6) and burn) else WALL
        if k in (5, 6) and shed_u >= 1:
            col = hexc("#ffc2cf")                                   # fresh new cells
        shape(cr, rrect_pts(x, y, 64, 120, 14, 16), col, seed=2311 + k, amp=0, lw=3)
        dot(cr, x + 32, y + 64, 8, WALL_D)
    if mucus_u > 0:
        w = 1120 * mucus_u
        shape(cr, [(-200, WALL_Y - 70), (-200 + w, WALL_Y - 80), (-200 + w, WALL_Y + 4), (-200, WALL_Y + 4)], MUCUS,
              seed=2330, amp=0, lw=3)
    blob(cr, 360, WALL_Y + 80, 120, 70, WALL, seed=2335, amp=0, lw=3)       # the lining's face, on its cells
    eyes(cr, 360, WALL_Y + 62, 1.0, mood)
    mouth(cr, 360, WALL_Y + 108, 0.85, mood, talking, t)


def scene_stomach(cr, t, tl):
    A = tl.at
    mucus_u = ease_out(seg(t, A("s4", "blanket") - 0.3, A("s4", "mucus") + 0.4))
    shed_u = ease_out(seg(t, A("s6", "grow") - 0.2, A("s6", "ones") + 0.6))
    burn = A("s6") <= t < A("s6", "grow")
    TOP, WALLC, MID = (1.3, 360, 420), (1.4, 360, 930), (1.0, 360, 700)
    keys = [(0, TOP), (A("s2"), WALLC), (A("s3"), TOP), (A("s4"), WALLC), (A("s5"), (1.2, 360, 760)),
            (A("s6"), WALLC), (A("s7"), TOP), (A("s8"), MID)]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*BG)
    cr.paint()
    # the acid pool above the wall
    shape(cr, [(-200, 600), (920, 590), (920, WALL_Y - 70), (-200, WALL_Y - 70)], hexc("#7fbf6a", 0.55), seed=2340,
          amp=0, lw=0, stroke=None)
    am = "happy" if t < A("s2") else ("angry" if t < A("s4") else ("shock" if t < A("s7") else "calm"))
    acid_char(cr, t, 360, 420, am, tl.speaking("acid", t))
    if t < A("s2"):   # the steak dissolving
        u = seg(t, 0.2, A("s2"))
        blob(cr, 590, 560, 70 * (1 - 0.7 * u), 44 * (1 - 0.7 * u), hexc("#a2413a"), seed=2345, amp=0, lw=3)
    lm = "worried" if t < A("s4") else "happy"
    if burn:
        lm = "cry"
    wall(cr, t, lm, tl.speaking("lining", t), mucus_u, shed_u, burn)
    if mucus_u >= 1:   # the mucus's face, in the gel layer
        mm = "happy"
        eyes(cr, 560, WALL_Y - 40, 0.6, mm)
        mouth(cr, 560, WALL_Y - 14, 0.5, mm, tl.speaking("mucus", t), t)
    if A("s5", "base") - 0.2 <= t < A("s6"):
        for k in range(5):   # acid drops neutralised as they reach the gel
            u = (t * 0.9 + k * 0.2) % 1
            y = lerp(600, WALL_Y - 80, u)
            dot(cr, 100 + 120 * k, y, 10, ACID if u < 0.8 else hexc("#ffffff"))
    if A("s8", "few") - 0.2 <= t:
        calendar(cr, t, 560, 360, "3-5 DAYS", A("s8", "few") - 0.2)
    if A("s4", "mucus") <= t < A("s6"):
        label(cr, "Mucus shield", 170, 700, 200, WALL_Y - 50)
    if A("s5", "base") <= t < A("s6"):
        label(cr, "Bicarbonate: neutralises acid", 360, 560, size=28)
    if t < A("s2"):
        label(cr, "Stomach acid", 360, 250, 360, 330)
    if A("s2") <= t < A("s4"):
        label(cr, "Stomach lining", 520, 760, 430, WALL_Y + 40)
    if A("s6", "grow") <= t < A("s7"):
        label(cr, "New cells", 520, 1080, 420, WALL_Y + 120)
    for w in (A("s1", "steak"), A("s4", "blanket"), A("s6", "grow")):
        cue("hit", t, w)


def layers_card(cr, t, start, n):
    """Three layers of defence, revealed one by one."""
    u = ease_out(seg(t, start, start + 0.3))
    if u <= 0:
        return
    rows = ["1. Mucus + bicarbonate", "2. Tightly packed cells", "3. New cells every 3-5 days"]
    with at(cr, 360, 690, 0.7 + 0.3 * u):     # over the bed sheet: clear of faces, above the captions
        shape(cr, rrect_pts(-300, -110, 600, 220, 22, 20), WHITE, seed=2350, amp=0, lw=4)
        for k in range(n):
            write(cr, [(rows[k], INK)], -270, -50 + 60 * k, 32, bold=True)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "stomach"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT), (A("w6"), B_CLOSE), (A("w7"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t < A("w6"):
        m.update(eyes="dot", mouth="smile")
    if A("w6") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w7") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w6"):
        d.update(arms=("hold", "down"))
    if A("w7") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("w3") <= t < A("w6"):
        n_rows = 1 + (t >= A("w4")) + (t >= A("w5"))
        layers_card(cr, t, A("w3"), n_rows)
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_stomach(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
