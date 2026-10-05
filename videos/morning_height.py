"""Body Facts 13: "You're TALLER Right Now Than You'll Be Tonight" — daily height change. Script approved by the owner.

Facts (sources in research_notes/body_facts_12-14.md):
- The intervertebral discs between the spine bones are squeezed all day while we're upright and slowly lose water;
  lying down overnight they soak it back up. People are tallest just after waking: about 1 cm (1-2 cm reported)
  taller than in the evening. There are 23 discs in the spine ("over twenty").
- In microgravity nothing squeezes the discs: astronauts can grow about 3% taller (NASA).
"""

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "disc": dict(voice="af_heart", speed=0.95),
    "bone": dict(voice="am_onyx", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"taller", "shorter", "disc", "discs", "water", "centimetre", "space", "gravity"}

SCRIPT = [
    dict(id="b1", scene="spine", text="Good morning! I'm a spine disc, full of water and nice and puffy.",
         speaker="disc"),
    dict(id="b2", scene="spine", text="Enjoy it while it lasts. He's about to stand up all day.", speaker="bone"),
    dict(id="b3", scene="spine", text="Ow. Every step squeezes a little water out of me.", speaker="disc"),
    dict(id="b4", scene="spine", text="And there are over twenty of you, all getting squished.", speaker="bone"),
    dict(id="b5", scene="spine", text="By tonight, he's about a centimetre shorter.", speaker="disc"),
    dict(id="b6", scene="spine", text="Then he lies down, and you soak it all back up.", speaker="bone"),
    dict(id="b7", scene="spine", text="Sleep. My favorite spa.", speaker="disc"),
    dict(id="w1", scene="ward", text="Doctor, am I really shorter in the evening?", speaker="mike"),
    dict(id="w2", scene="ward", text="Yes. You're tallest right after you wake up.", speaker="doctor"),
    dict(id="w3", scene="ward", text="The discs between your spine bones get squeezed all day, and lose water.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="At night, lying down, they soak it back up. The difference is about one "
                                     "centimetre.", speaker="doctor"),
    dict(id="w5", scene="ward", text="Astronauts have no gravity squeezing them, so in space they can grow about "
                                     "three percent taller.", speaker="doctor"),
    dict(id="w6", scene="ward", text="So I'll measure my height in the morning, bro.", speaker="danny", gap=0.3),
    dict(id="w7", scene="ward", text="Or in space.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="You're TALLER Right Now Than You'll Be Tonight 📏",
    alt_titles=["You Shrink Every Day. Here's Why 📏😳", "Why You're Taller in the Morning 📏"],
    description="""You're taller in the morning than at night. Every single day. 📏😳

Between your spine bones are soft discs full of water. Standing and walking squeezes them all day, and they slowly lose water, so by evening you're about a centimetre shorter. Lying down at night, they soak the water back up, and you're tallest right after you wake up. In space there's no gravity squeezing the discs, so astronauts can grow about 3% taller.

Sources: studies of daily height change and disc water loss (spine/ergonomics research); NASA research on astronauts' spines in microgravity.

(Cartoon, real facts. Not medical advice.)

💬 Have you ever measured yourself morning and night? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#BodyFacts", "#Spine", "#Doctor"],
    tags=["taller in the morning", "shorter at night", "spinal discs", "why am I taller in the morning",
          "astronauts grow taller", "body facts", "weird body facts", "spine facts", "doctor explains",
          "medical animation"],
    pinned_comment="Measure yourself tomorrow morning and tonight. 📏 Tell me the difference! 👇",
)

BONE, BONE_D = hexc("#f6efdf"), hexc("#d9c7a3")
DISC_C, DISC_D = hexc("#7fc8e8"), hexc("#3f9cc4")
BG, BG_N = hexc("#f4d7c8"), hexc("#27305a")


def vertebra(cr, x, y, w, s=1.0, mood=None, talking=False, t=0.0):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-w / 2, -48, w, 96, 26, 16), BONE, seed=2000, amp=0, lw=4)
        line(cr, [(-w / 2 + 20, -20), (w / 2 - 20, -24)], 3, BONE_D, seed=2001, amp=0)
        shape(cr, [(w / 2 - 6, -28), (w / 2 + 90, -10), (w / 2 + 96, 18), (w / 2 - 6, 24)], BONE, seed=2002, amp=0,
              lw=4)                                                                         # the bony spike at the back
        if mood:
            eyes(cr, 0, -10, 0.75, mood)
            mouth(cr, 0, 24, 0.6, mood, talking, t)


def disc(cr, x, y, w, h, s=1.0, mood=None, talking=False, t=0.0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, w / 2, h / 2, DISC_C, seed=2010, amp=0, lw=4)
        blob(cr, -w / 6, -h / 6, w / 7, h / 7, hexc("#ffffff", 0.45), seed=2011, amp=0, lw=0, stroke=None)
        if mood:
            eyes(cr, 0, -h * 0.1, 0.75 + 0.25 * h / 80, mood)
            mouth(cr, 0, h * 0.26, 0.65, mood, talking, t)


def scene_spine(cr, t, tl):
    A = tl.at
    squish = ease_out(seg(t, A("b3"), A("b5", "shorter") + 0.3))
    night = ease_out(seg(t, A("b6") - 0.2, A("b6") + 0.4))
    refill = ease_out(seg(t, A("b6", "soak"), A("b7") + 0.3))
    h = lerp(80, 50, squish) if refill <= 0 else lerp(50, 84, refill)
    CLOSE, COLUMN = (1.35, 380, 620), (0.75, 360, 640)
    keys = [(0, CLOSE), (A("b4"), COLUMN), (A("b5"), (0.85, 420, 640)), (A("b6"), CLOSE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    col = tuple(lerp(a, b, night) for a, b in zip(BG, BG_N))
    cr.set_source_rgba(*col)
    cr.paint()
    if night > 0:
        blob(cr, 600, 200, 46, 46, hexc("#fff3c4", night), seed=2020, amp=0, lw=0, stroke=None)
        blob(cr, 620, 190, 40, 40, (*col[:3], night), seed=2021, amp=0, lw=0, stroke=None)
    # a column of vertebrae and discs; the middle disc is the talker
    gap = h
    ys = []
    for k in range(-4, 5):
        ys.append((k, 640 + k * (96 + gap)))
    for k, yy in ys:
        vertebra(cr, 320, yy, 220, mood=("worried" if A("b3") <= t < A("b6") else "calm") if k == -1 else None,
                 talking=tl.speaking("bone", t) and k == -1, t=t)
    for k, yy in ys[:-1]:
        dy = yy + (96 + gap) / 2
        if k == -1:
            dm = "happy" if t < A("b3") else ("cry" if t < A("b6") else "happy")
            if A("b5") <= t < A("b6"):
                dm = "sad"
            disc(cr, 320, dy, 240, gap + 10, mood=dm, talking=tl.speaking("disc", t), t=t)
        else:
            disc(cr, 320, dy, 240, gap + 10)
    # water squeezed out while he walks
    if A("b3") <= t < A("b6"):
        for k in range(4):
            u = (t * 1.2 + k * 0.25) % 1
            dot(cr, 320 + (1 if k % 2 else -1) * (130 + 80 * u), 640 - (96 + gap) / 2 + 40 * u, 8, DISC_D)
    # height bar for b5
    if A("b5") <= t < A("b6"):
        with at(cr, 620, 640, 1.0):
            line(cr, [(0, -320), (0, 320)], 6, INK, seed=2030, amp=0)
            line(cr, [(-26, -320), (26, -320)], 6, INK, seed=2031, amp=0)
            line(cr, [(-26, -280), (26, -280)], 6, hexc("#d8363a"), seed=2032, amp=0)
            write(cr, [("-1 cm", hexc("#d8363a"))], 0, -220, 44, align="center", bold=True)
        cue("pop", t, A("b5"))
    if A("b4") <= t < A("b5"):
        label(cr, "23 discs in your spine", 360, 120, size=40)
    if t < A("b3"):
        label(cr, "Disc (full of water)", 500, 380, 400, 640 - (96 + gap) / 2)
        label(cr, "Spine bone", 520, 700, 420, 640)
    for w in (A("b3"), A("b5", "shorter"), A("b6", "soak")):
        cue("hit", t, w)


def astronaut(cr, t, x, y, s, start):
    u = ease_out(seg(t, start, start + 0.6))
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-50, -40, 100, 140 + 20 * u, 30, 20), WHITE, seed=2040, amp=0, lw=4)
        blob(cr, 0, -90, 58, 58, WHITE, seed=2041, amp=0, lw=4)
        blob(cr, 0, -88, 40, 34, hexc("#2b3a66"), seed=2042, amp=0, lw=3)
        blob(cr, -14, -98, 10, 6, hexc("#ffffff", 0.7), seed=2043, amp=0, lw=0, stroke=None)
        for sy in (-1, 1):   # stretch arrows
            line(cr, [(90, 30 + sy * (60 + 20 * u)), (90, 30 + sy * (110 + 20 * u))], 6, hexc("#3fae5c"),
                 seed=2044 + sy, amp=0)
        write(cr, [("+3%", hexc("#3fae5c"))], -150, 44, 56, align="center", bold=True)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "evening"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT), (A("w6"), B_CLOSE), (A("w7"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t < A("w5"):
        m.update(eyes="dot", mouth="smile")
    if A("w5") <= t:
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
    if A("w2", "tallest") <= t < A("w3"):
        label(cr, "Tallest: right after waking up", 360, 320, size=34)
    if A("w4", "difference") <= t < A("w5"):
        label(cr, "Morning vs night: about 1 cm", 360, 320, size=34)
        cue("pop", t, A("w4", "difference"))
    if A("w5", "astronauts") <= t < A("w6"):
        astronaut(cr, t, 600, 260, 0.8, A("w5", "astronauts"))
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_spine(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
