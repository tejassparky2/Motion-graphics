"""Body Facts 25: "Your Heart Has Its Own ELECTRICITY" — reference style (real four-chamber heart cut-away,
googly-eyed parts, labels, then the masked doctor). Script approved by the owner.

Facts (sources in research_notes/body_facts_23-26.md):
- The sinoatrial (SA) node, a small patch of pacemaker cells in the wall of the right atrium, fires on its own and
  starts every normal heartbeat. The impulse spreads across both atria (they contract), is delayed briefly at the
  atrioventricular (AV) node, then runs down the bundle of His and the Purkinje fibres so the ventricles contract.
- Normal resting rate 60-100 beats a minute (Cleveland Clinic). The autonomic nerves only speed it up or slow it
  down; a transplanted heart (its nerves cut) still beats, driven by its own SA node, typically a bit faster at rest.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.explain import along, googly, sign, stamp, step_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "sa": dict(voice="af_heart", speed=0.95),
    "atria": dict(voice="bf_emma", speed=0.95),
    "relay": dict(voice="am_michael", speed=0.95),
    "vent": dict(voice="bm_george", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"spark", "beat", "squeezing", "pause", "squeeze", "body", "electricity", "transplanted", "nerves"}

SCRIPT = [
    dict(id="h1", scene="heart", text="Zap! Zap! I'm the heart's spark. Every beat starts with me.", speaker="sa"),
    dict(id="h2", scene="heart", text="Spark received! Squeezing blood down!", speaker="atria"),
    dict(id="h3", scene="heart", text="Hold on. I pause the signal for a split second.", speaker="relay"),
    dict(id="h4", scene="heart", text="Now us! Big squeeze, out to the body!", speaker="vent"),
    dict(id="h5", scene="heart", text="And again. About sixty to a hundred times a minute.", speaker="sa"),
    dict(id="w1", scene="ward", text="Doctor, what makes my heart beat?", speaker="mike"),
    dict(id="w2", scene="ward", text="Your heart makes its own electricity. Here's how.", speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. A tiny spot called the S A node fires an electric spark.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. The spark spreads across the top chambers, and they squeeze.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. It pauses in the middle, then spreads down, and the big chambers "
                                     "pump blood out.", speaker="doctor"),
    dict(id="w6", scene="ward", text="That's why a transplanted heart still beats, even with its nerves cut. Your "
                                     "nerves only speed it up or slow it down.", speaker="doctor"),
    dict(id="w7", scene="ward", text="So my heart runs on electricity, bro.", speaker="danny", gap=0.3),
    dict(id="w8", scene="ward", text="Yes. Please don't charge your phone with it.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Your Heart Has Its Own ELECTRICITY ⚡❤️",
    alt_titles=["What Makes Your Heart Beat? 3 Steps ❤️", "Your Heart Has a Built-In Spark Plug ⚡"],
    description="""Your heart makes its own electricity. Every beat, in 3 steps. ⚡❤️

1. A tiny spot called the SA node fires an electric spark.
2. The spark spreads across the top chambers, and they squeeze.
3. It pauses in the middle (the AV node), then spreads down, and the big chambers pump blood out.

That's why a transplanted heart still beats, even with its nerves cut. Your nerves only speed it up or slow it down. At rest, it's about 60 to 100 beats a minute.

Sources: Cleveland Clinic, "Heart conduction system"; Medical News Today, "The heart's natural pacemaker".

(Cartoon, real facts. Not medical advice.)

💬 What's your resting heart rate? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Heart", "#BodyFacts", "#Doctor"],
    tags=["heart electricity", "what makes your heart beat", "sa node", "heart conduction system",
          "natural pacemaker", "body facts", "weird body facts", "doctor explains", "medical animation",
          "science explained"],
    pinned_comment="Put two fingers on your neck: what's your heart rate right now? ❤️ 👇",
)

# ---------------------------------------------------------------- the heart, cut open (front view; the heart's
# right side is on the viewer's left, like every textbook diagram)
MUSCLE, MUSCLE_D = hexc("#d9575a"), hexc("#b23a40")
BLUE_BLOOD, RED_BLOOD = hexc("#6f8fd8"), hexc("#e8787a")
FAT = hexc("#f6d98a")
WIRE, WIRE_ON = hexc("#f2c032"), hexc("#fff07a")
HEART = [(170, 400), (200, 330), (300, 300), (420, 300), (540, 330), (590, 420), (590, 560), (560, 680),
         (500, 780), (420, 870), (380, 880), (300, 800), (200, 680), (160, 560)]
RA, LA = (255, 445), (480, 430)
RV, LV = (300, 640), (470, 640)
SA = (225, 385)
AV = (360, 535)
ATRIAL_PATHS = [[SA, (260, 450), (310, 500), AV], [SA, (330, 390), (440, 410), (500, 460)]]
BUNDLE = [AV, (372, 600), (380, 700), (385, 790)]
LEFT_BR = [(385, 790), (300, 760), (230, 650)]
RIGHT_BR = [(385, 790), (470, 800), (540, 660)]
PERIOD = 0.75                     # one heartbeat: 80 beats a minute


def beat_phase(t):
    return (t % PERIOD) / PERIOD


def heart(cr, t, live):
    cr.set_source_rgba(*hexc("#fde8e4"))
    cr.paint()
    p = beat_phase(t) if live else 0.5
    atria_sq = math.sin(math.pi * seg(p, 0.0, 0.22)) if live else 0.0
    vent_sq = math.sin(math.pi * seg(p, 0.32, 0.62)) if live else 0.0
    # big vessels on top: vena cava into the right atrium, aorta and pulmonary artery out
    vessel(cr, [(215, 140), (220, 260), (230, 380)], 46, BLUE_BLOOD, seed=7000)
    vessel(cr, [(360, 470), (370, 300), (390, 200), (470, 160), (560, 200), (580, 280)], 50, RED_BLOOD, seed=7001)
    vessel(cr, [(320, 520), (310, 330), (300, 240)], 40, BLUE_BLOOD, seed=7002)
    k = 1 - 0.04 * vent_sq
    cr.save()
    cr.translate(380, 600)
    cr.scale(k, k)
    cr.translate(-380, -600)
    shape(cr, HEART, MUSCLE, seed=7003, amp=0, lw=4.5)
    blob(cr, 230, 360, 30, 20, FAT, seed=7004, amp=0, lw=2.5)
    sa_k, v_k = 1 - 0.12 * atria_sq, 1 - 0.14 * vent_sq
    blob(cr, RA[0], RA[1], 78 * sa_k, 66 * sa_k, BLUE_BLOOD, seed=7005, amp=0, lw=3.5)
    blob(cr, LA[0], LA[1], 72 * sa_k, 58 * sa_k, RED_BLOOD, seed=7006, amp=0, lw=3.5)
    blob(cr, RV[0], RV[1], 82 * v_k, 120 * v_k, BLUE_BLOOD, seed=7007, amp=0, lw=3.5)
    blob(cr, LV[0], LV[1], 72 * v_k, 130 * v_k, RED_BLOOD, seed=7008, amp=0, lw=3.5)
    for x, y in ((290, 535), (440, 530)):           # valves between upper and lower chambers
        line(cr, [(x - 30, y - 10), (x, y + 14), (x + 30, y - 10)], 5, WHITE, seed=7009 + x, amp=0)
    cr.restore()
    return p


def wire(cr, pts, on):
    vessel(cr, pts, 7, WIRE_ON if on else WIRE, seed=7100 + int(pts[0][0]))


def scene_heart(cr, t, tl):
    A = tl.at
    live = t >= A("h1", "spark") - 0.2
    WIDE, SAC, AVC, VEN = (0.95, 380, 520), (1.6, 260, 430), (1.5, 370, 560), (1.15, 390, 680)
    keys = [(0, SAC), (A("h1", "every"), WIDE), (A("h2"), (1.25, 360, 450)), (A("h3"), AVC), (A("h4"), VEN),
            (A("h5"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    p = heart(cr, t, live)
    # the electric wiring: lights up in order every beat (SA node, atria, pause at the AV node, then down)
    fire = live and p < 0.08
    at_on = live and 0.02 <= p < 0.25
    av_on = live and 0.18 <= p < 0.34
    down_on = live and 0.3 <= p < 0.5
    for pts in ATRIAL_PATHS:
        wire(cr, pts, at_on)
    for pts in (BUNDLE, LEFT_BR, RIGHT_BR):
        wire(cr, pts, down_on)
    if live and p < 0.25:
        for pts in ATRIAL_PATHS:
            x, y = along(pts, seg(p, 0.0, 0.2))
            zap(cr, x, y, 0.45)
    if live and 0.3 <= p < 0.5:
        for pts in (BUNDLE + LEFT_BR[1:], BUNDLE + RIGHT_BR[1:]):
            x, y = along(pts, seg(p, 0.3, 0.48))
            zap(cr, x, y, 0.45)
    # the talking parts: the SA node, the upper chambers, the AV node (the relay), the lower chambers
    blob(cr, SA[0], SA[1], 26 * (1.25 if fire else 1), 22 * (1.25 if fire else 1), WIRE_ON if fire else WIRE,
         seed=7200, amp=0, lw=3.5)
    googly(cr, t, SA[0], SA[1] - 4, 0.38, "happy" if t >= A("h5") else "calm", tl.speaking("sa", t), mouth_dy=24)
    googly(cr, t, LA[0], LA[1] - 8, 0.5, "angry" if A("h2") <= t < A("h3") else "calm", tl.speaking("atria", t),
           mouth_dy=28)
    blob(cr, AV[0], AV[1], 26, 22, WIRE_ON if av_on else WIRE, seed=7201, amp=0, lw=3.5)
    googly(cr, t, AV[0], AV[1] - 4, 0.38, "worried" if A("h3") <= t < A("h4") else "calm", tl.speaking("relay", t),
           mouth_dy=24)
    googly(cr, t, LV[0], LV[1] + 10, 0.6, "angry" if A("h4") <= t < A("h5") else "calm", tl.speaking("vent", t),
           mouth_dy=32)
    # labels, like the references
    if t < A("h2"):
        label(cr, "SA node", 120, 300, 210, 372)
    if A("h2") <= t < A("h3"):
        label(cr, "Upper chambers", 360, 240, 270, 400)
        line(cr, [(380, 256), (470, 390)], 2.5, INK, seed=7300, amp=0)
    if A("h3") <= t < A("h4"):
        label(cr, "AV node", 360, 440, 360, 512)
    if A("h4") <= t < A("h5"):
        label(cr, "Lower chambers", 380, 930, 300, 760)
        line(cr, [(400, 912), (470, 770)], 2.5, INK, seed=7301, amp=0)
    if A("h5") <= t:
        label(cr, "Aorta", 560, 130, 520, 170)
    for w in (A("h1", "spark"), A("h3", "pause"), A("h4", "squeeze")):
        cue("hit", t, w)
    # screen-space signs and a heart trace (ECG) along the top
    stamp(cr, t, A("h1"), "ZAP!", x=560, y=250, size=64, end=A("h1", "every"))
    if A("h3", "split") <= t < A("h4"):
        sign(cr, t, A("h3", "split"), "0.1 s PAUSE", y=250, col=hexc("#7a5bd0"), size=52)
    if A("h5") <= t:
        sign(cr, t, A("h5", "sixty"), "60-100 BEATS A MINUTE", y=250, col=hexc("#d8363a"), size=44)
        ecg(cr, t)


def ecg(cr, t):
    cr.save()
    cr.identity_matrix()
    shape(cr, rrect_pts(60, 330, 600, 110, 16, 16), hexc("#1d2a33", 0.85), seed=7400, amp=0, lw=3)
    pts = []
    for i in range(121):
        x = 70 + i * 4.8
        ph = ((x / 180) - t / PERIOD * 0.9) % 1
        y = 395
        if 0.1 < ph < 0.16:
            y -= 10 * math.sin(math.pi * (ph - 0.1) / 0.06)
        elif 0.24 < ph < 0.26:
            y += 8
        elif 0.26 <= ph < 0.29:
            y -= 50 * math.sin(math.pi * (ph - 0.26) / 0.03)
        elif 0.29 <= ph < 0.31:
            y += 12
        elif 0.42 < ph < 0.52:
            y -= 14 * math.sin(math.pi * (ph - 0.42) / 0.1)
        pts.append((x, y))
    line(cr, pts, 4, hexc("#5ff0a0"), seed=7401, amp=0)
    cr.restore()


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "heart"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w7"), B_CLOSE), (A("w8"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("w7") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w7") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w8", "phone") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w7"):
        d.update(arms=("hold", "down"))
    if A("w8") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    if A("w2", "electricity") <= t < A("w3"):
        sign(cr, t, A("w2", "electricity"), "BUILT-IN ELECTRICITY", y=690, col=hexc("#f2b632"), size=48)
    step_card(cr, t, A("w3"), 1, "The SA node fires an electric spark.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "It spreads across the top chambers: they squeeze.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Short pause, then down: the big chambers pump.", end=A("w6") - 0.05)
    if A("w6") <= t < A("w6", "your"):
        sign(cr, t, A("w6"), "NERVES CUT: STILL BEATS", y=690, col=hexc("#d8363a"), size=44)
    if A("w6", "your") <= t < A("w7"):
        sign(cr, t, A("w6", "your"), "NERVES: FASTER OR SLOWER", y=690, col=hexc("#2f7fd6"), size=44)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_heart)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
