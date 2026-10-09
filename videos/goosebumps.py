"""Body Facts 17: "Why You Get GOOSEBUMPS" — the arrector pili muscle. Script approved by the owner.

Facts (sources in research_notes/body_facts_15-18.md):
- Each hair has a tiny muscle (arrector pili); cold, fear or strong emotion (sympathetic nerves) make it contract,
  pulling the hair upright and raising a bump of skin around it.
- In furry mammals, raised fur traps an insulating layer of air; many animals (e.g. a scared cat) puff up and look
  bigger. In humans, with little body hair, the warming effect is largely vestigial.
- Hsu lab (Harvard), Cell 2020, in MICE: the same sympathetic nerve and muscle also regulate hair follicle stem
  cells, so cold can drive new hair growth. Script says "in mice" and doesn't call goosebumps "useless".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import WHITE, at, blob, cue, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "hair": dict(voice="af_nova", speed=0.95),
    "muscle": dict(voice="am_onyx", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"goosebumps", "cold", "muscle", "fur", "warm", "cat", "bigger", "bald"}

SCRIPT = [
    dict(id="g1", scene="skin", text="Brr! It's cold out here!", speaker="hair"),
    dict(id="g2", scene="skin", text="Hold on. I'll pull you up straight!", speaker="muscle"),
    dict(id="g3", scene="skin", text="Okay. I'm standing. Are we warmer now?", speaker="hair"),
    dict(id="g4", scene="skin", text="Well, our furry ancestors were. Raised fur traps warm air.", speaker="muscle"),
    dict(id="g5", scene="skin", text="And what about when he's scared?", speaker="hair"),
    dict(id="g6", scene="skin", text="Same move. A scared cat puffs up to look bigger.", speaker="muscle"),
    dict(id="g7", scene="skin", text="So we're doing a fur trick, with almost no fur.", speaker="hair"),
    dict(id="w1", scene="ward", text="Doctor, why do I get goosebumps?", speaker="mike"),
    dict(id="w2", scene="ward", text="Each hair has a tiny muscle that pulls it up straight. That makes the bump.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="In furry animals, raised fur traps warm air, and makes them look bigger.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="We kept the reflex, even though we lost most of the fur.", speaker="doctor"),
    dict(id="w5", scene="ward", text="And in mice, the same nerves even help wake up the cells that grow new hair.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="So goosebumps are just my body trying to be a cat, bro.", speaker="danny",
         gap=0.3),
    dict(id="w7", scene="ward", text="A very bald cat.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why You Get GOOSEBUMPS 🥶",
    alt_titles=["Goosebumps Are a Leftover From Fur 🥶😳", "What Goosebumps Are Really For 🐈"],
    description="""Goosebumps are your body doing a fur trick… with almost no fur. 🥶😳

Every hair has a tiny muscle. When you're cold or scared, it pulls the hair straight up and makes a little bump. In furry animals, raised fur traps warm air and makes them look bigger (think of a scared cat). We kept the reflex even though we lost most of our fur. And a 2020 Harvard study in mice found the same nerves and muscles also help wake up the stem cells that grow new hair.

Sources: NIH Research Matters, "What goosebumps are for"; Shwartz, Hsu et al., Cell 2020 (study in mice).

(Cartoon, real facts. Not medical advice.)

💬 What gives you goosebumps? Music? Cold? Horror movies? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Goosebumps", "#BodyFacts", "#Doctor"],
    tags=["goosebumps", "why do we get goosebumps", "arrector pili", "goosebumps evolution", "body facts",
          "weird body facts", "skin facts", "hair", "doctor explains", "medical animation"],
    pinned_comment="What gives YOU goosebumps? Music, cold, or a scary movie? 🥶 👇",
)

BG = hexc("#bfe3ef")
SKIN, SKIN_D, DERM = hexc("#f2c29b"), hexc("#d89a72"), hexc("#f7d6c0")
SURF = 560                              # skin surface line
HAIR_ROOT = (330, 840)
MUSCLE_RED, MUSCLE_D = hexc("#c4544b"), hexc("#8e2f2c")


def skin(cr, t, up):
    """Cross-section of skin: surface, a hair growing out of its root, and the tiny muscle beside it."""
    cr.set_source_rgba(*BG)
    cr.paint()
    bump = 60 * up
    pts = [(-200, SURF), (230, SURF), (300, SURF - bump), (380, SURF - bump), (450, SURF), (920, SURF),
           (920, 1800), (-200, 1800)]
    shape(cr, pts, SKIN, seed=2400, amp=0, lw=4.5)
    shape(cr, [(-200, SURF + 60), (920, SURF + 60), (920, 1800), (-200, 1800)], DERM, seed=2401, amp=0, lw=0,
          stroke=None)
    # the hair follicle (root pocket)
    shape(cr, rrect_pts(HAIR_ROOT[0] - 34, SURF - bump + 20, 68, HAIR_ROOT[1] - SURF + bump, 30, 16), SKIN_D,
          seed=2402, amp=0, lw=3)
    blob(cr, HAIR_ROOT[0], HAIR_ROOT[1], 40, 34, hexc("#e8a36c"), seed=2403, amp=0, lw=3)


def hair(cr, t, up, mood, talking):
    """The hair: lies flat (up=0) or stands straight (up=1); its face sits on the hair shaft."""
    ang = lerp(-1.25, -0.05, up)                         # from lying right to pointing up
    x0, y0 = HAIR_ROOT[0], SURF - 60 * up
    L = 360
    x1, y1 = x0 - L * math.sin(ang), y0 - L * math.cos(ang)
    line(cr, [(x0, HAIR_ROOT[1]), (x0, y0), (x1, y1)], 22, hexc("#3a2a1e"), seed=2410, amp=0)
    fx, fy = lerp(x0, x1, 0.6), lerp(y0, y1, 0.6)
    blob(cr, fx, fy, 56, 50, hexc("#5a4030"), seed=2411, amp=0, lw=3)
    eyes(cr, fx, fy - 8, 0.8, mood)
    mouth(cr, fx, fy + 22, 0.65, mood, talking, t)
    return x1, y1


def muscle(cr, t, up, mood, talking):
    """The tiny goosebump muscle: from the hair root up to the skin, shorter and fatter when it pulls."""
    a = (HAIR_ROOT[0] + 20, HAIR_ROOT[1] - 70)
    b = (lerp(560, 520, up), lerp(SURF + 90, SURF + 120, up))
    w = lerp(30, 50, up)
    line(cr, [a, b], w + 8, MUSCLE_D, seed=2420, amp=0)
    line(cr, [a, b], w, MUSCLE_RED, seed=2421, amp=0)
    mx, my = lerp(a[0], b[0], 0.5), lerp(a[1], b[1], 0.5)
    blob(cr, mx, my, 52, 44, MUSCLE_RED, seed=2422, amp=0, lw=3.5)
    eyes(cr, mx, my - 6, 0.65, mood)
    mouth(cr, mx, my + 20, 0.55, mood, talking, t)


def furball(cr, t, x, y, s, puff, kind="fur"):
    """A furry animal (fur=puffed with a warm-air layer) or a cat that puffs up to look bigger."""
    with at(cr, x, y, s):
        r = 90 + 40 * puff
        for k in range(36):
            a = 2 * math.pi * k / 36
            line(cr, [(70 * math.cos(a), 60 * math.sin(a)), (r * math.cos(a), (r - 10) * math.sin(a))], 6,
                 hexc("#8a7a6a") if kind == "fur" else hexc("#3a3d45"), seed=2430 + k, amp=0)
        blob(cr, 0, 0, 78, 66, hexc("#b8a48c") if kind == "fur" else hexc("#5a5d66"), seed=2440, amp=0, lw=4)
        if kind == "cat":
            for sx in (-1, 1):
                shape(cr, [(sx * 30, -60), (sx * 60, -110 - 20 * puff), (sx * 70, -50)], hexc("#5a5d66"),
                      seed=2441 + sx, amp=0, lw=3.5)
            eyes(cr, 0, -6, 0.8, "shock")
        else:
            eyes(cr, 0, -6, 0.8, "happy")
            if puff > 0.5:
                write(cr, [("warm air", hexc("#d8363a"))], 0, -r - 16, 30, align="center", bold=True)


def scene_skin(cr, t, tl):
    A = tl.at
    up = ease_out(seg(t, A("g2", "pull") - 0.1, A("g2", "straight") + 0.3))
    if A("g7") <= t:
        up = 1.0
    CLOSE, WIDE = (1.2, 380, 700), (1.0, 360, 680)
    keys = [(0, CLOSE), (A("g2"), (1.15, 440, 700)), (A("g3"), CLOSE), (A("g4"), WIDE), (A("g5"), CLOSE),
            (A("g6"), WIDE), (A("g7"), CLOSE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    skin(cr, t, up)
    hm = "cry" if t < A("g2") else ("happy" if t < A("g5") else ("worried" if t < A("g7") else "happy"))
    hair(cr, t, up, hm, tl.speaking("hair", t))
    mm = "calm" if t < A("g2") else "happy"
    muscle(cr, t, up, mm, tl.speaking("muscle", t))
    if t < A("g2"):   # cold: snowflakes
        for k in range(8):
            u = (t * 0.4 + k * 0.125) % 1
            blob(cr, 60 + 85 * k, lerp(80, SURF - 20, u), 8, 8, WHITE, seed=2450 + k, amp=0, lw=2)
    # the furry ancestor and the scared cat
    if A("g4", "furry") - 0.2 <= t < A("g5"):
        with at(cr, 0, 0, 1.0):
            shape(cr, rrect_pts(380, 120, 300, 260, 24, 20), hexc("#ffffff", 0.85), seed=2455, amp=0, lw=3)
        furball(cr, t, 530, 260, 0.75, ease_out(seg(t, A("g4", "fur"), A("g4", "air"))))
    if A("g6", "cat") - 0.2 <= t < A("g7"):
        with at(cr, 0, 0, 1.0):
            shape(cr, rrect_pts(380, 120, 300, 260, 24, 20), hexc("#ffffff", 0.85), seed=2456, amp=0, lw=3)
        furball(cr, t, 530, 260, 0.75, ease_out(seg(t, A("g6", "puffs"), A("g6", "bigger"))), kind="cat")
    if A("g2") <= t < A("g4"):
        label(cr, "Goosebump muscle", 560, 1000, 480, 760)
    if A("g2", "straight") <= t < A("g4"):
        label(cr, "Goosebump!", 520, 440, 340, SURF - 70)
    if t < A("g2"):
        label(cr, "Hair", 160, 380, 300, 470)
    if A("g7") <= t:
        label(cr, "Fur trick, almost no fur", 540, 420, size=32)
    for w in (A("g2", "pull"), A("g6", "cat")):
        cue("hit", t, w)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "goosebumps"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT), (A("w6"), B_CLOSE), (A("w7"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"), sweat=False)
    if A("w2") <= t < A("w6"):
        m.update(eyes="dot", mouth="smile")
    if A("w6") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w7") <= t:
        n.update(eyes="wide", mouth="o", arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w6"):
        d.update(arms=("hold", "down"))
    if A("w7") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("w2", "muscle") - 0.1 <= t < A("w3"):
        label(cr, "Tiny muscle pulls each hair up", 360, 320, size=34)
    if A("w3") <= t < A("w4"):
        label(cr, "Fur up = warm air + looks bigger", 360, 320, size=34)
    if A("w5", "mice") - 0.1 <= t < A("w6"):
        label(cr, "Study in mice (Harvard, 2020)", 360, 320, size=34)
        cue("pop", t, A("w5", "mice") - 0.1)
    if A("w7", "bald") <= t:
        with at(cr, 560, 300, 0.6):
            furball(cr, t, 0, 0, 1.0, 0.0, kind="cat")
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_skin(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
