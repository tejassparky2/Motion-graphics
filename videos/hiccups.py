"""Body Facts 20: "Why You HICCUP" — the hiccup reflex. Polished style, step-by-step explanation.
Script approved by the owner.

Facts (sources in research_notes/body_facts_19-22.md):
- A hiccup is a reflex (vagus and phrenic nerves, brainstem): the diaphragm contracts suddenly, air rushes in, and
  the glottis (vocal cords) snaps shut, making the "hic". Triggers include eating fast, fizzy drinks, swallowing
  air (a stretched stomach).
- Most episodes stop on their own within minutes; hiccups lasting more than 48 hours are "persistent" and need a
  doctor (Hiccups review, PMC5072913; Penn State Health).
- Folk cures like being scared are unproven: the script says "That's not proven".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import WHITE, at, blob, cue, hexc, lerp, line, seg, shape
from motion.explain import googly, sign, stamp, step_card, tip_card, vessel
from motion.kit import camera, enter_world, set_camera, whip

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "stomach": dict(voice="af_nova", speed=0.95),
    "diaphragm": dict(voice="am_onyx", speed=0.95),
    "cords": dict(voice="af_heart", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"hiccup", "hiccups", "diaphragm", "twitch", "twitching", "shut", "reflex", "minutes", "days"}

SCRIPT = [
    dict(id="h1", scene="chest", text="Oh no, he ate too fast, and now I'm all stretched.", speaker="stomach"),
    dict(id="h2", scene="chest", text="Hey! Something's poking my nerve! I'm twitching!", speaker="diaphragm"),
    dict(id="h3", scene="chest", text="And every twitch makes him gulp air!", speaker="diaphragm"),
    dict(id="h4", scene="chest", text="So we slam the door shut. And that's the hic sound.", speaker="cords"),
    dict(id="h5", scene="chest", text="And then it happens again. And again.", speaker="diaphragm"),
    dict(id="h6", scene="chest", text="How long will this last?", speaker="stomach"),
    dict(id="h7", scene="chest", text="Usually just a few minutes.", speaker="diaphragm"),
    dict(id="w1", scene="ward", text="Doctor, why do I get hiccups?", speaker="mike"),
    dict(id="w2", scene="ward", text="A hiccup is a reflex. Here's how it works.", speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Something irritates the nerves to your diaphragm, like eating fast "
                                     "or fizzy drinks.", speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. Your diaphragm, the big breathing muscle under your lungs, suddenly "
                                     "twitches, and you suck in air.", speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. Your vocal cords snap shut, and that makes the hic sound.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="Most hiccups stop on their own within minutes.", speaker="doctor"),
    dict(id="w7", scene="ward", text="But if they last more than two days, see a doctor.", speaker="doctor"),
    dict(id="w8", scene="ward", text="Bro, I fix mine by scaring myself.", speaker="danny", gap=0.3),
    dict(id="w9", scene="ward", text="That's not proven. But we'll allow it.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why You HICCUP 😳",
    alt_titles=["Hiccups Explained in 3 Steps 😳", "What Actually Happens When You Hiccup"],
    description="""What actually happens when you hiccup? 3 steps. 😳

1. Something irritates the nerves to your diaphragm, like eating fast or fizzy drinks.
2. Your diaphragm (the big breathing muscle under your lungs) suddenly twitches, and you suck in air.
3. Your vocal cords snap shut, and that makes the "hic" sound.

A hiccup is a reflex. Most hiccups stop on their own within minutes, but if they last more than two days (48 hours), see a doctor. Scaring someone? Not proven.

Sources: Steger, Schneemann & Fox, "Hiccups: a common problem with some unusual causes and cures" (PMC5072913); Penn State Health, "The Medical Minute: causes and cures of hiccups remain elusive".

(Cartoon, real facts. Not medical advice.)

💬 What's your secret hiccup cure? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Hiccups", "#BodyFacts", "#Doctor"],
    tags=["hiccups", "why do we hiccup", "how to stop hiccups", "diaphragm", "hiccup reflex", "body facts",
          "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Drop your weirdest hiccup cure. 😂 Doc will judge it. 👇",
)

# ---------------------------------------------------------------- the chest and belly, cut open (front view)
SKIN = hexc("#f6c9a4")
LUNG, LUNG_D = hexc("#f4a6b4"), hexc("#d7788c")
HEART = hexc("#d8363a")
DIA = hexc("#c4544b")
LIVER = hexc("#8e3b32")
STOMACH = hexc("#f0a08e")
BONE = hexc("#f4ead6")
TRACHEA = hexc("#f2d0c8")
NERVE = hexc("#f2c032")
DIA_Y = 640                               # top of the diaphragm domes

TORSO = [(250, 100), (470, 100), (480, 200), (640, 250), (690, 330), (680, 700), (640, 900), (80, 900), (40, 700),
         (30, 330), (80, 250), (240, 200)]


def hiccup_times(tl):
    A = tl.at
    return [A("h2", "twitching") - 0.1, A("h4", "hic"), A("h5", "again"), A("h5", "again", nth=2)]


def torso(cr, t, jerk, shut):
    cr.set_source_rgba(*hexc("#bfe3ef"))
    cr.paint()
    shape(cr, TORSO, SKIN, seed=4200, amp=0, lw=4.5)
    shape(cr, [(70, 300), (650, 300), (660, 860), (60, 860)], hexc("#7a2a36"), seed=4201, amp=0, lw=3.5)   # cavity
    d = 34 * jerk                              # the diaphragm pulls down on each hiccup
    # lungs (they fill with air as the diaphragm drops)
    k = 1 + 0.05 * jerk
    with at(cr, 195, 470, k):
        shape(cr, [(-110, -120), (-40, -170), (40, -150), (90, -40), (100, 150 + d), (-120, 170 + d)], LUNG,
              seed=4202, amp=0, lw=4)
        line(cr, [(-60, 20), (60, -10)], 3, LUNG_D, seed=4203, amp=0)
    with at(cr, 525, 470, k):
        shape(cr, [(110, -120), (40, -170), (-40, -150), (-90, -40), (-60, 60), (-100, 150 + d), (120, 170 + d)],
              LUNG, seed=4204, amp=0, lw=4)
        line(cr, [(60, 30), (-40, 0)], 3, LUNG_D, seed=4205, amp=0)
    # heart between the lungs
    blob(cr, 400, 560, 90, 80, HEART, seed=4206, amp=0, lw=4)
    line(cr, [(380, 480), (390, 420), (430, 400)], 18, HEART, seed=4207, amp=0)
    # ribs over everything, light
    for k_ in range(6):
        y = 320 + 70 * k_
        for side in (-1, 1):
            line(cr, [(360 + side * 30, y), (360 + side * 200, y + 20), (360 + side * 300, y + 60)], 7,
                 hexc("#f4ead6", 0.55), seed=4210 + k_ + 10 * (side > 0), amp=0)
    line(cr, [(360, 300), (360, 640)], 22, hexc("#f4ead6", 0.7), seed=4230, amp=0)          # breastbone
    # windpipe from the voice box down to the lungs; the food pipe beside it
    vessel(cr, [(360, 120), (360, 260), (360, 330)], 34, TRACHEA, seed=4240)
    for k_ in range(6):
        line(cr, [(343, 150 + 30 * k_), (377, 150 + 30 * k_)], 3, hexc("#d9a8a0"), seed=4250 + k_, amp=0)
    line(cr, [(360, 330), (260, 400)], 22, TRACHEA, seed=4260, amp=0)
    line(cr, [(360, 330), (460, 400)], 22, TRACHEA, seed=4261, amp=0)
    vessel(cr, [(395, 140), (400, 400), (420, DIA_Y + 30), (450, DIA_Y + 90)], 14, hexc("#e8a090"), seed=4270)
    # voice box with the two vocal cords (seen from above, in a circle)
    blob(cr, 360, 160, 40, 34, hexc("#e8a090"), seed=4280, amp=0, lw=3.5)
    # liver and stomach under the diaphragm
    shape(cr, [(80, DIA_Y + 80 + d), (330, DIA_Y + 70 + d), (360, DIA_Y + 150 + d), (200, DIA_Y + 230 + d),
               (90, DIA_Y + 200 + d)], LIVER, seed=4290, amp=0, lw=4)
    shape(cr, [(420, DIA_Y + 70 + d), (600, DIA_Y + 60 + d), (640, DIA_Y + 160 + d), (580, DIA_Y + 240 + d),
               (470, DIA_Y + 230 + d), (430, DIA_Y + 160 + d)], STOMACH, seed=4291, amp=0, lw=4)
    # the diaphragm: two domes under the lungs
    dy = DIA_Y + d
    shape(cr, [(70, dy + 60), (190, dy - 10), (330, dy + 30), (360, dy + 40), (390, dy + 30), (530, dy - 10),
               (650, dy + 60), (650, dy + 90), (530, dy + 26), (390, dy + 64), (330, dy + 64), (190, dy + 26),
               (70, dy + 90)], DIA, seed=4292, amp=0, lw=4)
    # the phrenic nerves from the neck to the diaphragm
    for x0, x1 in ((330, 230), (390, 500)):
        vessel(cr, [(x0, 160), (x0 - 10 * (x0 < 360) + 10 * (x0 > 360), 380), (x1, dy)], 6, NERVE, seed=4300 + x0)
    # vocal cords inset
    with at(cr, 560, 170, 1.0):
        blob(cr, 0, 0, 92, 92, hexc("#7a2a36"), seed=4310, amp=0, lw=4)
        gap = lerp(34, 2, shut)
        for side in (-1, 1):
            shape(cr, [(side * 4, -70), (side * (gap + 8), -60), (side * (gap + 14), 60), (side * 4, 70)], WHITE,
                  seed=4311 + side, amp=0, lw=3)


def scene_chest(cr, t, tl):
    A = tl.at
    hics = hiccup_times(tl)
    jerk = 0.0
    for h in hics:
        if h <= t < h + 0.5:
            jerk = math.sin(math.pi * seg(t, h, h + 0.5))
    shut = 1.0 if any(h <= t < h + 0.4 for h in hics[1:]) else 0.0
    WIDE, BELLY, NECK, DIAC = (1.0, 360, 560), (1.45, 500, 820), (1.6, 470, 230), (1.3, 360, 720)
    keys = [(0, BELLY), (A("h2"), DIAC), (A("h3"), WIDE), (A("h4"), NECK), (A("h5"), WIDE), (A("h6"), BELLY),
            (A("h7"), DIAC)]
    set_camera(camera(t, keys))
    enter_world(cr)
    torso(cr, t, jerk, shut)
    d = 34 * jerk
    # the talking parts
    sm = "worried" if t < A("h7") else "happy"
    googly(cr, t, 530, DIA_Y + 140 + d, 0.75, sm, tl.speaking("stomach", t))
    dm = "shock" if jerk > 0.2 else ("angry" if A("h2") <= t < A("h4") else "calm")
    if A("h7") <= t:
        dm = "happy"
    googly(cr, t, 190, DIA_Y + 28 + d, 0.55, dm, tl.speaking("diaphragm", t), mouth_dy=26)
    googly(cr, t, 560, 245, 0.5, "shock" if shut else ("happy" if t < A("h4") else "calm"),
           tl.speaking("cords", t), mouth_dy=-48)
    if jerk > 0.2:             # air rushing in through the windpipe
        for k in range(3):
            line(cr, [(330 + 30 * k, 40), (335 + 30 * k, 110)], 5, WHITE, seed=4320 + k, amp=0)
    # labels, like the references
    if t < A("h2"):
        label(cr, "Stomach", 600, 900 - 140, 560, DIA_Y + 120)
        label(cr, "Liver", 150, 900 - 140, 200, DIA_Y + 140)
    if A("h2") <= t < A("h4"):
        label(cr, "Diaphragm", 200, DIA_Y - 70, 190, DIA_Y)
        label(cr, "Nerve", 520, 360, 460, 420)
    if A("h3") <= t < A("h4"):
        label(cr, "Lungs", 200, 330, 200, 380)
    if A("h4") <= t < A("h5"):
        label(cr, "Vocal cords", 560, 50, 560, 82)
        label(cr, "Windpipe", 440, 330, 365, 280)
    for h in hics:
        cue("hit", t, h)
    # screen-space signs
    for k, h in enumerate(hics[1:], 1):
        sign(cr, t, h, "HIC!", x=360, y=230 + 20 * (k % 2), size=74, end=h + 0.8)
    if A("h7", "few") <= t:
        sign(cr, t, A("h7", "few"), "A FEW MINUTES", y=250, col=hexc("#3fae5c"), size=50)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "hiccups"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w8"), B_CLOSE), (A("w9"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("face", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w8") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w8") <= t:
        n.update(eyes="wide", mouth="o", arms=("thumb", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w8"):
        d.update(arms=("hold", "down"))
    if A("w9") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    step_card(cr, t, A("w3"), 1, "Eating fast or fizzy drinks irritate the nerves.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The diaphragm twitches: you suck in air.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "The vocal cords snap shut: HIC!", end=A("w6") - 0.05)
    tip_card(cr, t, A("w6"), "Most hiccups stop on their own in minutes.", "ok", end=A("w7") - 0.05)
    tip_card(cr, t, A("w7"), "They last more than 2 days (48 hours).", "warn", end=A("w8"))
    stamp(cr, t, A("w9", "proven"), "NOT PROVEN", y=690)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_chest)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
