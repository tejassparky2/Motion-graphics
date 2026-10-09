"""Body Facts 18: "Why You CAN'T Tickle Yourself" — sensory prediction. Script approved by the owner.

Facts (sources in research_notes/body_facts_15-18.md):
- The brain predicts the sensory result of our own movements from a copy of the motor command (an internal
  "forward model"); the cerebellum is thought to make that prediction, and expected touch is turned down
  (sensory attenuation). Blakemore, Wolpert & Frith, NeuroReport 2000; Nature Neuroscience 1998.
- Robot experiment: people moved a lever, a robot arm stroked their palm. With no delay it felt least ticklish;
  adding a delay (up to fractions of a second) made it more ticklish, because it no longer matched the prediction.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import brain
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "hand": dict(voice="am_michael", speed=0.95),
    "cereb": dict(voice="af_heart", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"tickle", "tickled", "predict", "predicts", "robot", "delay", "friend", "cerebellum"}

SCRIPT = [
    dict(id="t1", scene="body", text="Watch this. I'm going to tickle him!", speaker="hand"),
    dict(id="t2", scene="body", text="Nice try. I saw that coming.", speaker="cereb"),
    dict(id="t3", scene="body", text="How do you know? I haven't even moved yet!", speaker="hand"),
    dict(id="t4", scene="body", text="Every time you move, I get a copy of the plan. So I predict the touch.",
         speaker="cereb"),
    dict(id="t5", scene="body", text="And a touch I expected, I turn way down.", speaker="cereb"),
    dict(id="t6", scene="body", text="So who can tickle him?", speaker="hand"),
    dict(id="t7", scene="body", text="Someone else. I can't predict them.", speaker="cereb"),
    dict(id="w1", scene="ward", text="Doctor, why can't I tickle myself?", speaker="mike"),
    dict(id="w2", scene="ward", text="Your brain predicts the touch from your own movements, and turns it down.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Scientists tested it with a robot. People moved a lever, and a robot arm "
                                     "tickled their hand.", speaker="doctor"),
    dict(id="w4", scene="ward", text="With no delay, it barely tickled. With a small delay, it tickled more, "
                                     "because the brain couldn't predict it.", speaker="doctor"),
    dict(id="w5", scene="ward", text="So if I want to tickle myself, I need a robot, bro.", speaker="danny",
         gap=0.3),
    dict(id="w6", scene="ward", text="Or a friend. Please get a friend.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why You CAN'T Tickle Yourself 🤭",
    alt_titles=["Your Brain Won't Let You Tickle Yourself 🤭", "Try to Tickle Yourself. You Can't. Here's Why 😳"],
    description="""Try to tickle yourself. It doesn't work. Here's why. 🤭🧠

Every time you move, your brain gets a copy of the plan and predicts what you'll feel. A touch it expected gets turned way down, so your own fingers barely tickle. In a famous experiment, people moved a lever that made a robot arm tickle their hand. With no delay, it barely tickled. With a small delay, it tickled more, because the brain couldn't predict it.

Sources: Blakemore, Wolpert & Frith, "Why can't you tickle yourself?", NeuroReport (2000); Blakemore et al., Nature Neuroscience (1998).

(Cartoon, real facts. Not medical advice.)

💬 Did you just try to tickle yourself? 😂 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Tickle", "#BodyFacts", "#Brain"],
    tags=["why can't you tickle yourself", "tickle yourself", "brain prediction", "cerebellum", "tickling science",
          "body facts", "weird body facts", "brain facts", "doctor explains", "medical animation"],
    pinned_comment="Be honest: did you just try to tickle yourself? 😂 Did it work? 👇",
)

BG = hexc("#fde7c8")
SLEEVE_M, SLEEVE_D = hexc("#2f7fd6"), hexc("#7a3fb0")      # Mike's sleeve, the friend's sleeve
SKIN = hexc("#d8a272")


def hand(cr, t, x, y, s, mood, talking, sleeve=SLEEVE_M, wiggle=0.0, face=True):
    with at(cr, x, y, s, rot=-0.3):
        line(cr, [(-260, 120), (-60, 30)], 90, sleeve, seed=2500, amp=0)
        blob(cr, 0, 0, 80, 66, SKIN, seed=2501, amp=0, lw=4)
        for k in range(4):
            w = 10 * math.sin(t * 18 + k) * wiggle
            line(cr, [(40, -40 + 26 * k), (110 + w, -50 + 30 * k)], 22, SKIN, seed=2502 + k, amp=0)
        if face:
            eyes(cr, -10, -10, 0.65, mood)
            mouth(cr, -10, 20, 0.55, mood, talking, t)


def cerebellum(cr, t, x, y, s, mood, talking):
    """The cerebellum: the striped little brain at the back, with its own face."""
    with at(cr, x, y, s):
        blob(cr, 0, 0, 110, 70, hexc("#e07a95"), seed=2510, amp=0, lw=4)
        for k in range(5):
            line(cr, [(-90, -40 + 20 * k), (0, -50 + 22 * k), (90, -40 + 20 * k)], 3, hexc("#b94f6c"),
                 seed=2511 + k, amp=0)
        eyes(cr, 0, -6, 0.75, mood)
        mouth(cr, 0, 26, 0.6, mood, talking, t)


def meter(cr, t, x, y, level):
    """The tickle-o-meter: a bar from 0 to MAX."""
    with at(cr, x, y, 1.0):
        shape(cr, rrect_pts(-40, -180, 80, 360, 20, 16), WHITE, seed=2520, amp=0, lw=4)
        h = 340 * level
        if h > 4:
            col = hexc("#3fae5c") if level < 0.5 else hexc("#d8363a")
            shape(cr, rrect_pts(-30, 170 - h, 60, h, 14, 16), col, seed=2521, amp=0, lw=0, stroke=None)
        write(cr, [("TICKLE", INK)], 0, -200, 30, align="center", bold=True)


def scene_body(cr, t, tl):
    A = tl.at
    reach = ease_out(seg(t, 0.2, A("t2")))
    if A("t3") <= t < A("t7"):
        reach = 0.6
    level = 0.0
    if A("t5", "down") - 0.2 <= t < A("t7"):
        level = lerp(0.6, 0.06, ease_out(seg(t, A("t5", "down") - 0.2, A("t5", "down") + 0.4)))
    elif A("t2") <= t < A("t5"):
        level = 0.6
    if A("t7") <= t:
        level = lerp(0.06, 1.0, ease_out(seg(t, A("t7"), A("t7") + 0.6)))
    BR, HN, WIDE = (1.15, 380, 470), (1.05, 360, 720), (1.0, 360, 640)
    keys = [(0, HN), (A("t2"), BR), (A("t3"), HN), (A("t4"), BR), (A("t5"), WIDE), (A("t6"), HN), (A("t7"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*BG)
    cr.paint()
    # the brain up top, with the cerebellum below it talking
    brain(cr, t, 360, 330, 0.6, "calm")
    cm = "happy" if t < A("t6") else "calm"
    cerebellum(cr, t, 360, 470, 1.0, cm, tl.speaking("cereb", t))
    # Mike's ribs at the bottom (his shirt) and his own hand reaching in
    shape(cr, rrect_pts(-100, 960, 920, 900, 60, 20), SLEEVE_M, seed=2530, amp=0, lw=4.5)
    for k in range(4):
        line(cr, [(60, 1040 + 70 * k), (660, 1040 + 70 * k)], 3, hexc("#1f5fa8"), seed=2531 + k, amp=0)
    hm = "happy" if t < A("t2") else ("shock" if t < A("t4") else ("sad" if t < A("t6") else "worried"))
    hand(cr, t, lerp(140, 280, reach), lerp(780, 860, reach), 1.15, hm, tl.speaking("hand", t),
         wiggle=1.0 if A("t1") <= t < A("t2") else 0.0)
    # the copy of the plan flying to the cerebellum, and the prediction bubble
    if A("t4", "copy") - 0.2 <= t < A("t5"):
        u = ease_out(seg(t, A("t4", "copy") - 0.2, A("t4", "copy") + 0.6))
        px, py = lerp(280, 470, u), lerp(800, 500, u)
        shape(cr, rrect_pts(px - 40, py - 30, 80, 60, 6, 10), WHITE, seed=2540, amp=0, lw=3)
        write(cr, [("PLAN", INK)], px, py + 10, 22, align="center", bold=True)
    if A("t4", "predict") - 0.1 <= t < A("t6"):
        blob(cr, 540, 250, 140, 70, WHITE, seed=2541, amp=0, lw=3.5)
        write(cr, [("Touch: ribs, now", INK)], 540, 260, 28, align="center", bold=True)
    # the friend's hand
    if A("t7") <= t:
        u = ease_out(seg(t, A("t7"), A("t7") + 0.5))
        hand(cr, t, lerp(900, 470, u), 900, 1.15, "happy", False, sleeve=SLEEVE_D, wiggle=1.0, face=False)
    meter(cr, t, 620, 680, level)
    if A("t2") <= t < A("t4"):
        label(cr, "Cerebellum", 150, 560, 260, 490)
    if A("t7") <= t:
        label(cr, "Someone else's hand", 400, 760, 480, 860)
    for w in (A("t2"), A("t5", "down"), A("t7")):
        cue("hit", t, w)


def robot_card(cr, t, start, delay):
    """The experiment: a lever, a robot arm, and the tickle level with no delay vs a small delay."""
    u = ease_out(seg(t, start, start + 0.3))
    if u <= 0:
        return
    with at(cr, 360, 690, 0.7 + 0.3 * u):     # over the bed sheet: clear of faces, above the captions
        shape(cr, rrect_pts(-320, -120, 640, 240, 22, 20), WHITE, seed=2550, amp=0, lw=4)
        line(cr, [(-260, 60), (-220, -40)], 10, INK, seed=2551, amp=0)               # the lever
        blob(cr, -220, -40, 14, 14, hexc("#d8363a"), seed=2552, amp=0, lw=3)
        line(cr, [(-80, 70), (0, -40), (90, -20)], 14, hexc("#7d8591"), seed=2553, amp=0)   # the robot arm
        blob(cr, 100, -14, 20, 16, hexc("#ffd23f"), seed=2554, amp=0, lw=3)
        lvl = 0.15 if not delay else 0.75
        shape(cr, rrect_pts(200, -80, 60, 160, 14, 14), hexc("#eef1f5"), seed=2555, amp=0, lw=3)
        shape(cr, rrect_pts(200, 80 - 160 * lvl, 60, 160 * lvl, 14, 14),
              hexc("#3fae5c") if not delay else hexc("#d8363a"), seed=2556, amp=0, lw=0, stroke=None)
        write(cr, [("small delay" if delay else "no delay", INK)], 0, 100, 30, align="center", bold=True)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "tickle"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), B_CLOSE), (A("w6"), NEXT_BED)]
    m = dict(eyes="sad", mouth="wobble", arms=("hold", "down"))
    if A("w2") <= t < A("w5"):
        m.update(eyes="dot", mouth="smile")
    if A("w5") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w5") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w6") <= t:
        n.update(eyes="sad", mouth="wobble", arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w5"):
        d.update(arms=("hold", "down"))
    if A("w6") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("w2", "predicts") - 0.1 <= t < A("w3"):
        label(cr, "Expected touch = turned down", 360, 320, size=36)
    if A("w3", "robot") - 0.2 <= t < A("w5"):
        robot_card(cr, t, A("w3", "robot") - 0.2, delay=t >= A("w4", "small"))
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_body(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
