"""Body Facts 26: "Why Yawns Are CONTAGIOUS" — reference style (head in profile with the brain's movement area,
googly-eyed parts, labels, then the masked doctor). Script approved by the owner.

Facts (sources in research_notes/body_facts_23-26.md):
- Contagious yawning: seeing, hearing or even reading about a yawn triggers one. Studies put it at roughly 40-60% of
  adults ("about half").
- Brown et al., Current Biology 2017 (University of Nottingham): the urge to yawn after watching yawns tracked
  excitability in the primary motor cortex; being told to resist raised the urge and only changed how people
  yawned (stifled yawns). So: "Trying to hold it in rarely stops it. It just changes how the yawn looks."
- Stronger between friends and family than strangers (Norscia & Palagi 2011); dogs can catch human yawns
  (Joly-Mascheroni et al. 2008). The empathy explanation is debated, so the script doesn't claim it.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.explain import along, googly, sign, stamp, step_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip
from videos.brain_freeze import BONE, CAVITY, SKIN, TONGUE, head

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "eye": dict(voice="af_nova", speed=0.95),
    "brain": dict(voice="bm_george", speed=0.95),
    "jaw": dict(voice="am_michael", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"yawning", "yawn", "yawns", "movement", "automatic", "contagious", "half", "friends", "dogs"}

SCRIPT = [
    dict(id="y1", scene="head", text="Alert! Someone in front of us is yawning!", speaker="eye"),
    dict(id="y2", scene="head", text="Copy that. Sending it to the movement area.", speaker="brain"),
    dict(id="y3", scene="head", text="Uh oh. I can feel it coming.", speaker="jaw"),
    dict(id="y4", scene="head", text="Too late. Yawn, go!", speaker="brain"),
    dict(id="y5", scene="head", text="He didn't even want to yawn!", speaker="jaw"),
    dict(id="y6", scene="head", text="That's the funny part. It's mostly automatic.", speaker="brain"),
    dict(id="w1", scene="ward", text="Doctor, why do I yawn when someone else yawns?", speaker="mike"),
    dict(id="w2", scene="ward", text="It's called contagious yawning. About half of adults catch yawns.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Your eyes or ears catch someone yawning.", speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. Your brain's movement area copies it, almost automatically.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. Trying to hold it in rarely stops it. It just changes how the "
                                     "yawn looks.", speaker="doctor"),
    dict(id="w6", scene="ward", text="It spreads most between friends and family. Even dogs catch human yawns.",
         speaker="doctor"),
    dict(id="w7", scene="ward", text="Sorry, bro. I caught it.", speaker="danny", gap=1.6),
    dict(id="w8", scene="ward", text="And now, so did everyone watching.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why Yawns Are CONTAGIOUS 🥱",
    alt_titles=["Try Not to Yawn Watching This 🥱", "Why You Catch Other People's Yawns, in 3 Steps 🥱"],
    description="""Why do you yawn when someone else yawns? 3 steps. 🥱

1. Your eyes or ears catch someone yawning.
2. Your brain's movement area copies it, almost automatically.
3. Trying to hold it in rarely stops it. It just changes how the yawn looks.

About half of adults catch yawns. It spreads most between friends and family, and even dogs catch human yawns. Scientists still debate exactly why it happens.

Sources: Brown et al., "A neural basis for contagious yawning", Current Biology (2017); Norscia & Palagi, PLoS ONE (2011); Joly-Mascheroni et al., Biology Letters (2008).

(Cartoon, real facts. Not medical advice.)

💬 Be honest: did you yawn? 🥱👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Yawn", "#BodyFacts", "#Doctor"],
    tags=["contagious yawning", "why are yawns contagious", "yawning", "try not to yawn", "brain facts",
          "body facts", "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Did you yawn? Be honest 🥱 👇",
)

# ---------------------------------------------------------------- the head in profile (from brain_freeze) with a
# jaw that drops, the brain's movement strip, and a phone showing someone yawning
EYE = (188, 402)
MOTOR = [(420, 160), (440, 220), (465, 280), (490, 340)]
TO_MOTOR = [(222, 404), (300, 380), (380, 300), (440, 230)]
TO_JAW = [(470, 320), (470, 450), (455, 560), (440, 640)]
PIVOT = (440, 615)                       # the jaw joint
JAW = [(100, 705), (160, 740), (330, 748), (430, 700), (470, 760), (430, 840), (330, 830), (220, 805), (140, 780),
       (110, 745)]
PHONE = (-120, 420)


def phone(cr, t, open_):
    x, y = PHONE
    shape(cr, rrect_pts(x - 70, y - 120, 140, 240, 20, 16), hexc("#2a2f3a"), seed=8000, amp=0, lw=4)
    shape(cr, rrect_pts(x - 58, y - 104, 116, 208, 10, 16), hexc("#bfe3ef"), seed=8001, amp=0, lw=2)
    blob(cr, x, y - 10, 44, 48, hexc("#d9a37a"), seed=8002, amp=0, lw=3)            # a face yawning
    for s in (-1, 1):
        line(cr, [(x + 16 * s - 8, y - 26), (x + 16 * s + 8, y - 26)], 3.5, INK, seed=8003 + s, amp=0)
    blob(cr, x, y + 14, 12, 6 + 18 * open_, CAVITY, seed=8005, amp=0, lw=2.5)


def scene_head(cr, t, tl):
    A = tl.at
    other = 0.5 + 0.5 * math.sin(t * 3) if t < A("y2") else 0.0
    sent = A("y2", "sending")
    urge = 0.15 * ease_out(seg(t, A("y3"), A("y3", "coming")))
    big = ease_out(seg(t, A("y4", "yawn"), A("y4", "go") + 0.5)) * (1 - seg(t, A("y6"), A("y6") + 0.8))
    open_ = max(urge if t < A("y6") else 0.0, big)
    WIDE, EYEC, BRN, JAWC = (0.9, 230, 500), (1.4, 120, 420), (1.2, 400, 270), (1.2, 380, 640)
    keys = [(0, WIDE), (A("y1", "front"), EYEC), (A("y2"), BRN), (A("y3"), JAWC), (A("y4"), (1.0, 300, 560)),
            (A("y5"), JAWC), (A("y6"), (1.1, 340, 470))]
    set_camera(camera(t, keys))
    enter_world(cr)
    head(cr, t, 0.0)
    phone(cr, t, other)
    # the dropping jaw: a dark open mouth behind, then the lower jaw turning on its joint
    if open_ > 0.01:
        shape(cr, [(100, 640), (420, 640), (460, 700), (440, 860), (120, 860)], CAVITY, seed=8010, amp=0, lw=0,
              stroke=None)
        cr.save()
        cr.translate(*PIVOT)
        cr.rotate(-0.45 * open_)
        cr.translate(-PIVOT[0], -PIVOT[1])
        shape(cr, JAW, SKIN, seed=8011, amp=0, lw=4)
        shape(cr, [(150, 700), (260, 680), (380, 690), (410, 715), (200, 725)], TONGUE, seed=8012, amp=0, lw=3)
        shape(cr, [(96, 690), (118, 690), (116, 714), (98, 714)], WHITE, seed=8013, amp=0, lw=3)
        cr.restore()
    # the eye
    blob(cr, EYE[0], EYE[1], 38, 36, WHITE, seed=8020, amp=0, lw=4)
    blob(cr, EYE[0] - 32, EYE[1], 8, 18, hexc("#9ad0ff"), seed=8021, amp=0, lw=2.5)
    # the movement strip of the brain lights up; signals run eye -> strip -> jaw muscle
    lit = sent <= t
    line(cr, MOTOR, 26, hexc("#ffe066") if lit else hexc("#e98aa0"), seed=8030, amp=0)
    if A("y1", "yawning") <= t < A("y3"):
        x, y = along(TO_MOTOR, ((t - A("y1", "yawning")) * 1.2) % 1)
        zap(cr, x, y, 0.5)
    if A("y3") <= t < A("y6"):
        vessel(cr, TO_JAW, 6, hexc("#ffe066"), seed=8031)
        x, y = along(TO_JAW, ((t - A("y3")) * 1.3) % 1)
        zap(cr, x, y, 0.5)
    # the jaw muscle (masseter) on the side of the jaw, with its own face
    cr.save()
    if open_ > 0.01:
        cr.translate(*PIVOT)
        cr.rotate(-0.2 * open_)
        cr.translate(-PIVOT[0], -PIVOT[1])
    blob(cr, 420, 690, 40, 62, hexc("#c4544b"), seed=8040, amp=0, lw=3.5)
    for k in range(3):
        line(cr, [(400 + 14 * k, 640), (408 + 14 * k, 740)], 2.5, hexc("#a03a36"), seed=8041 + k, amp=0)
    jm = "worried" if A("y3") <= t < A("y4") else ("shock" if A("y4") <= t < A("y6") else "calm")
    googly(cr, t, 420, 680, 0.5, jm, tl.speaking("jaw", t), mouth_dy=28)
    cr.restore()
    # the talking parts
    em = "shock" if t < A("y2") else "calm"
    googly(cr, t, EYE[0] + 6, EYE[1] - 8, 0.45, em, tl.speaking("eye", t), mouth_dy=34)
    bm = "happy" if A("y4") <= t < A("y5") or A("y6") <= t else "calm"
    googly(cr, t, 330, 260, 0.75, bm, tl.speaking("brain", t), mouth_dy=34)
    # labels, like the references
    if t < A("y2"):
        label(cr, "Eye", 190, 300, 190, 366)
    if A("y2") <= t < A("y3"):
        label(cr, "Movement area", 520, 120, 450, 200)
    if A("y3") <= t < A("y4"):
        label(cr, "Jaw muscle", 300, 900, 410, 740)
    for w in (A("y1", "yawning"), sent, A("y4", "go")):
        cue("hit", t, w)
    # screen-space signs
    if A("y1", "yawning") <= t < A("y2"):
        sign(cr, t, A("y1", "yawning"), "YAWN SPOTTED", y=250, col=hexc("#2f7fd6"), size=52)
    stamp(cr, t, A("y4", "go"), "YAWN!", x=360, y=250, size=72, end=A("y5"))
    if A("y6", "automatic") <= t:
        sign(cr, t, A("y6", "automatic"), "MOSTLY AUTOMATIC", y=250, col=hexc("#7a5bd0"), size=52)


def scene_ward(cr, t, tl):
    A = tl.at
    yawn_b = A("w6", end=True) + 0.1 <= t < A("w7")
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "else"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w6", end=True), B_CLOSE), (A("w8"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("w8", "everyone") <= t:
        m.update(eyes="closed", mouth="o")              # Mike catches it too
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if yawn_b:
        n.update(eyes="closed", mouth="o", arms=("hold", "hold"))
    if A("w7") <= t:
        n.update(eyes="happy", mouth="grin")
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w7"):
        d.update(arms=("hold", "down"))
    if A("w8") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    if A("w2", "half") <= t < A("w3"):
        sign(cr, t, A("w2", "half"), "ABOUT HALF OF ADULTS", y=690, col=hexc("#2f7fd6"), size=46)
    step_card(cr, t, A("w3"), 1, "Your eyes or ears catch someone yawning.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "The brain's movement area copies it.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Holding it in rarely stops it.", end=A("w6") - 0.05)
    if A("w6") <= t < A("w6", "even"):
        sign(cr, t, A("w6"), "FRIENDS AND FAMILY MOST", y=690, col=hexc("#7a5bd0"), size=44)
    if A("w6", "even") <= t < A("w6", end=True) + 0.1:
        sign(cr, t, A("w6", "even"), "EVEN DOGS!", y=690, col=hexc("#f2b632"), size=52)
    if yawn_b:
        sign(cr, t, A("w6", end=True) + 0.1, "YAWN...", x=560, y=330, col=hexc("#2f7fd6"), size=48)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_head)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
