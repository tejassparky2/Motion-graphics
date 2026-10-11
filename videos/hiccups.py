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

from motion.clinic import watermark
from motion.engine import hexc, lerp, seg
from motion.kit import whip
from motion.pkit import GOLD, RED, tag
from motion.polish import OUTLINE, camera, captions, counter, ellipse, enter, paint, particles, sign, stamp
from motion.pbody import CLINIC_CAMS as C, blob, clinic, face, finish, shape_fill, step_card, tip_card, tube
from motion import pbody

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

BG_TOP, BG_BOT = hexc("#d8eef7"), hexc("#a9d3e6")
LUNG, DIA, STOM, CORD = hexc("#ff9fb0"), hexc("#e8473f"), hexc("#f6b26b"), hexc("#ff8fa3")
DIA_Y = 640


def hiccup_times(tl):
    A = tl.at
    return [A("h2", "twitching") - 0.1, A("h4", "hic"), A("h5", "again"), A("h5", "again", nth=2)]


def scene_chest(cr, t, tl):
    A = tl.at
    hics = hiccup_times(tl)
    jerk = 0.0
    for h in hics:
        if h <= t < h + 0.5:
            jerk = math.sin(math.pi * seg(t, h, h + 0.5))
    shut = 0.0
    for h in hics[1:]:
        if h <= t < h + 0.4:
            shut = 1.0
    cams = [(0, (1.4, 400, 760)), (A("h2"), (1.3, 360, 640)), (A("h4"), (1.5, 360, 340)), (A("h5"), (1.1, 360, 560)),
            (A("h6"), (1.4, 400, 760)), (A("h7"), (1.2, 360, 620))]
    cr.save()
    enter(cr, camera(t, cams), drift=0.004, t=t)
    pbody.backdrop(cr, t, BG_TOP, BG_BOT, seed=20)
    # windpipe and lungs
    tube(cr, [(360, 140), (360, 330), (360, 400)], 46, hexc("#f2c7cf"))
    for side in (-1, 1):
        blob(cr, 360 + side * 150, 470 - 20 * jerk, 120, 150 + 18 * jerk, LUNG)
    # vocal cords: two flaps in the windpipe, snapping shut on each hiccup
    for side in (-1, 1):
        x = 360 + side * lerp(30, 6, shut)
        ellipse(cr, x, 250, 18, 34, side * 0.3)
        paint(cr, CORD, OUTLINE, 4)
    face(cr, t, 470, 250, 0.7, "shock" if shut else ("happy" if t < A("h4") else "open"), tl.speaking("cords", t))
    # the diaphragm: a dome under the lungs that jerks down on each twitch
    dy = DIA_Y + 40 * jerk
    shape_fill(cr, [(80, dy + 60), (200, dy - 20), (360, dy - 50), (520, dy - 20), (640, dy + 60),
                    (520, dy + 30), (360, dy + 10), (200, dy + 30)], DIA)
    dm = "wide" if jerk > 0.2 else ("angry" if A("h2") <= t < A("h4") else "open")
    if A("h7") <= t:
        dm = "happy"
    face(cr, t, 360, dy - 14, 0.8, dm, tl.speaking("diaphragm", t))
    # the stomach below, stretched and fizzy
    sm = "worried" if t < A("h7") else "happy"
    blob(cr, 420, 820, 150, 100, STOM)
    face(cr, t, 420, 810, 0.85, sm, tl.speaking("stomach", t))
    particles(cr, t, 20, 10, hexc("#fff7e0"), area=(300, 740, 240, 140), r=(3, 7), speed=14)
    if jerk > 0.2:    # air rushing in
        for k in range(3):
            pbody.stroke_line(cr, [(320 + 40 * k, 60), (330 + 40 * k, 160)], 6, hexc("#ffffff"))
    tag(cr, t, 0.3, 560, DIA_Y - 40, "Diaphragm", end=A("h3"))
    tag(cr, t, A("h4"), 300, 180, "Vocal cords", end=A("h5"))
    cr.restore()
    # screen-space signs
    for k, h in enumerate(hics[1:], 1):
        sign(cr, t, h, 360, 230 if k % 2 else 260, "HIC!", col=GOLD, size=80, end=h + 0.8, rot=-0.05 * k)
    if A("h5") <= t < A("h6"):
        counter(cr, t, A("h5"), 600, 330, 3, size=90, dur=1.6, prefix="x")
    if A("h7", "few") <= t:
        sign(cr, t, A("h7", "few"), 360, 300, "A FEW MINUTES", col=hexc("#3fbf6a"), size=54)


def scene_ward(cr, t, tl):
    A = tl.at
    cams = [(A("w1") - 0.1, C["mike"]), (A("w1", "hiccups"), C["two"]), (A("w2"), C["doc"]), (A("w3"), C["two"]),
            (A("w5"), C["doc"]), (A("w6"), C["two"]), (A("w8"), C["danny"]), (A("w9"), C["both"])]
    cam = camera(t, cams, dur=0.3)
    mike = dict(eyes="wide", mouth="o", arms=("face", "down"))
    if A("w2") <= t:
        mike = dict(eyes="open", mouth="smile")
    if A("w8") <= t:
        mike = dict(eyes="happy", mouth="grin")
    doc = dict(arms=("point", "down")) if A("w3") <= t < A("w8") else dict(arms=("hold", "down"))
    if A("w9") <= t:
        doc = dict(eyes="half", mouth="smug", arms=("shrug", "shrug"))
    danny = dict(eyes="angry", mouth="open", arms=("up", "up")) if A("w8") <= t else dict()
    clinic(cr, t, tl, cam, mike, danny, doc)
    step_card(cr, t, A("w3"), 1, "Eating fast or fizzy drinks irritate the nerves.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The diaphragm twitches: you suck in air.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "The vocal cords snap shut: HIC!", end=A("w6") - 0.05)
    tip_card(cr, t, A("w6"), "Most hiccups stop on their own in minutes.", "ok", end=A("w7") - 0.05)
    tip_card(cr, t, A("w7"), "Hiccups for more than 2 days (48 hours)", "warn", end=A("w8"))
    if A("w9", "proven") <= t:
        stamp(cr, t, A("w9", "proven"), 360, 330, "NOT PROVEN", col=RED, size=62)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_chest)(cr, t, tl)
    cr.restore()
    finish(cr)
    captions(cr, t, tl)
    watermark(cr)
