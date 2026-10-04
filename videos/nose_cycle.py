"""Body Facts 3: "You're Breathing Through ONE Nostril Right Now" — the two sides of the nose work in shifts.

Facts (kept general and uncontroversial; sources in research_notes/body_facts_2-4.md):
- The nasal cycle: tissue (erectile tissue of the turbinates and septum) swells with blood on one side, so most
  airflow goes through the other side; then the sides swap (PMC5053491: all 33 subjects cycled, mean cycle about
  2 h awake; Cleveland Clinic: "every four to six hours"; reviews: 70-80% of adults). So: "every few hours",
  "most people".
- It is driven by the autonomic nervous system (one side sympathetic, the other parasympathetic), and it is
  normal; most people don't notice it.
"""
import math

from motion.captions import captions
from motion.engine import blob, cue, ease_out, hexc, lerp, line, seg, shape, write
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import airflow, brain, turbinate

# Voices: natural stock voices at their own pitch (owner: the pitched-up voices weren't clear), a touch slower.
# The doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "left": dict(voice="am_michael", speed=0.95),     # the side that's working
    "right": dict(voice="bf_emma", speed=0.95),       # the side on its break
    "brain": dict(voice="af_heart", speed=0.95),      # same brain as the awake-surgery episode
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})                                   # the doctor speaks in the narrator voice (the owner's clone)
TAIL = 1.0
EMPHASIS = {"nasal", "cycle", "swells", "breathing", "nervous", "hours", "left", "right"}   # bigger captions

SCRIPT = [
    dict(id="n1", scene="nose", text="Hey, you! Yes, you. Breathe in through your nose.", speaker="left"),
    dict(id="n2", scene="nose", text="Can you feel it? I'm doing most of the work!", speaker="left"),
    dict(id="n3", scene="nose", text="Because my partner over there is asleep!", speaker="left"),
    dict(id="n4", scene="nose", text="Let me sleep. I'm on my break.", speaker="right"),
    dict(id="n5", scene="nose", text="A break? We have to work together! Get up and help me!", speaker="left"),
    dict(id="n6", scene="nose", text="Okay, you two, switch sides. Right side, you're up.", speaker="brain"),
    dict(id="n7", scene="nose", text="Fine. It's my turn.", speaker="right"),
    dict(id="n8", scene="nose", text="Finally! Wake me up in a few hours.", speaker="left"),
    dict(id="d1", scene="ward", text="Doctor, one side of my nose keeps getting blocked. Is it broken?",
         speaker="danny"),
    dict(id="d2", scene="ward", text="No. That's the nasal cycle. Most people have it.", speaker="doctor"),
    dict(id="d3", scene="ward", text="The tissue inside one side swells up. So the other side does most of the "
                                     "breathing.", speaker="doctor"),
    dict(id="d4", scene="ward", text="Every few hours, your nervous system swaps them. You just don't notice.",
         speaker="doctor"),
    dict(id="d5", scene="ward", text="So one side of my nose is always taking a nap?", speaker="mike"),
    dict(id="d6", scene="ward", text="Just like you at work, bro.", speaker="danny", gap=0.3),
    dict(id="d7", scene="ward", text="Try it now. Block one side and breathe, then the other. Which side is working "
                                     "for you?", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="You're Breathing Through ONE Nostril Right Now 👃",
    alt_titles=["Your Nose Works in Shifts (Try It Now) 👃", "Why One Side of Your Nose Is Always Blocked 😳"],
    description="""Breathe through your nose. Notice anything? One side is probably doing most of the work. 👃

It's called the nasal cycle, and most people have it. Tissue inside one side of your nose swells up, so most of the air goes through the other side. Every few hours, your nervous system swaps them. You just don't notice.

Try it: block one side and breathe, then the other.

(Funny cartoon, real facts. Not medical advice: if one side is blocked all the time, see a doctor.)

💬 Which side is working for you right now? Left or right? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Nose", "#BodyFacts", "#Doctor"],
    tags=["nasal cycle", "one nostril", "why is one nostril blocked", "breathing through one nostril", "nose facts",
          "body facts", "doctor explains", "human body", "weird body facts", "funny animation", "health facts"],
    pinned_comment="Okay, test it right now: which side is working for you, LEFT or RIGHT? 👃👇",
)

SKIN_A, SKIN_B = hexc("#f6c9a8"), hexc("#d8956c")
WALL_L, SEPT_L, SEPT_R, WALL_R = 150, 340, 380, 570     # passage walls (world x)
TOP, BOT = 400, 1000                                   # passage top and bottom (world y)
TY = 690                                               # height of the two tissue characters


def nose_bg(cr, t):
    import cairo
    g = cairo.RadialGradient(360, 600, 80, 360, 600, 1000)
    g.add_color_stop_rgba(0, *SKIN_A)
    g.add_color_stop_rgba(1, *SKIN_B)
    cr.rectangle(-900, -900, 2600, 3200)
    cr.set_source(g)
    cr.fill()
    # the nose, in cutaway: bridge, wings, and two passages inside
    shape(cr, [(300, 120), (420, 120), (520, 520), (690, 960), (640, 1110), (80, 1110), (30, 960), (200, 520)],
          hexc("#f2b48e"), seed=500, amp=0.8, lw=4.5)
    for x0, x1 in ((WALL_L, SEPT_L), (SEPT_R, WALL_R)):
        shape(cr, [(x0, TOP), (x1, TOP), (x1, BOT), (x0, BOT)], hexc("#a8474f"), seed=501 + x0, amp=0.6, lw=4)
        shape(cr, [(x0 + 14, TOP + 10), (x1 - 14, TOP + 10), (x1 - 14, BOT - 6), (x0 + 14, BOT - 6)], hexc("#c45d63"),
              seed=505 + x0, amp=0, lw=0, stroke=None)                                  # moist lining
        for k, vx in enumerate((x0 + 8, x1 - 8)):                                       # blood vessels in the wall
            pts = [(vx + 6 * math.sin(j * 1.3 + k), TOP + 20 + j * 48) for j in range(13)]
            line(cr, pts, 4, hexc("#6b4fa8"), seed=507 + x0 + k, amp=0)
    shape(cr, [(SEPT_L, TOP - 20), (SEPT_R, TOP - 20), (SEPT_R + 4, BOT + 30), (SEPT_L - 4, BOT + 30)],
          hexc("#f2b48e"), seed=503, amp=0.4, lw=4)                                  # the middle wall
    for cx in ((WALL_L + SEPT_L) / 2, (SEPT_R + WALL_R) / 2):                         # nostrils
        blob(cr, cx, BOT + 40, 80, 34, hexc("#5a2430"), seed=504 + int(cx), amp=0.6, lw=4)


def scene_nose(cr, t, tl):
    A = tl.at
    swap = ease_out(seg(t, A("n6", "up") - 0.1, A("n6", "up") + 0.9))
    lsw, rsw = swap, 1 - swap               # swelling: left starts open (working), right starts swollen (resting)
    LF, RF = (1.6, 245, 760), (1.6, 475, 760)
    keys = [(0, (1.05, 360, 720)), (A("n1", "you", nth=2), LF), (A("n1", "breathe"), (1.1, 300, 760)),
            (A("n2"), LF), (A("n2", "work"), (1.0, 360, 720)),
            (A("n3", "asleep"), RF), (A("n4"), (1.8, 475, 760)),
            (A("n5"), LF), (A("n5", "help"), (1.0, 360, 700)),
            (A("n6"), (1.4, 360, 360)), (A("n6", "switch"), (1.25, 360, 480)), (A("n6", "up"), (1.0, 360, 700)),
            (A("n7"), RF), (A("n8"), LF), (A("n8", "hours"), (1.0, 360, 720))]
    set_camera(camera(t, keys))
    enter_world(cr)
    nose_bg(cr, t)
    # air through whichever side is open
    lx0 = WALL_L + 92 + 84 * lsw - 6
    rx1 = WALL_R - (92 + 84 * rsw) + 6
    airflow(cr, t, lx0, SEPT_L - 4, TOP + 20, BOT, 1 - lsw, seed=1)
    airflow(cr, t, SEPT_R + 4, rx1, TOP + 20, BOT, 1 - rsw, seed=2)
    # ---- the brain, the boss upstairs, with a nerve down to each side
    for x in (WALL_L + 40, WALL_R - 40):
        line(cr, [(360, 250), (x, 330), (x, TY - 170)], 4, hexc("#f7e27a"), seed=510 + x, amp=0.5)
    brain(cr, t, 360, 220, 0.55, "angry" if A("n6") <= t < A("n7") else "calm", tl.speaking("brain", t))
    # ---- the two sides
    lm = "happy" if t < A("n1") + 0.01 else "calm"
    if A("n1") <= t < A("n3"):
        lm = "happy"
    if A("n3") <= t < A("n6"):
        lm = "angry"
    if A("n6") <= t < A("n8"):
        lm = "happy"
    if A("n8") <= t:
        lm = "happy"       # eyes shut: off to sleep
    rm = "happy" if t < A("n6") else ("worried" if t < A("n7", "turn") else "angry")
    look_l = 0.0 if t < A("n3") else 1.0
    turbinate(cr, t, WALL_L, TY, -1, lsw, lm, tl.speaking("left", t), look=look_l,
              hat="hard" if lsw < 0.5 else "sleep")
    turbinate(cr, t, WALL_R, TY, 1, rsw, rm, tl.speaking("right", t), look=-1 if t < A("n6") else 0,
              hat="sleep" if rsw > 0.5 else "hard")
    # sleepy z's over whichever side is resting
    zx = lerp(WALL_R - 90, WALL_L + 90, swap)
    for k in range(3):
        u = (t * 0.7 + k / 3) % 1
        write(cr, [("z", hexc("#ffffff", 1 - u))], zx + 20 * k + 30 * u, TY - 230 - 70 * u, 34 + 10 * k, bold=True)
    # sweat drops on the worker before the swap
    if A("n2") <= t < A("n6", "up"):
        for k in range(2):
            u = (t * 1.3 + k * 0.5) % 1
            blob(cr, WALL_L + 40 + 50 * k, TY - 120 + 60 * u, 6, 10, hexc("#8fd3ff", 1 - u), seed=520 + k, amp=0.2,
                 lw=0, stroke=None)
    # ---- screen text
    # ---- anatomy tags, like the references
    label(cr, "Nasal septum", 360, 330, 360, 420)
    if t < A("n8"):
        label(cr, "Swollen tissue", lerp(590, 130, swap), 470, lerp(520, 200, swap), 560)
    if A("n2", "most") <= t < A("n6"):
        label(cr, "Open side", 130, 1050, 300, 960)
    if t >= A("n6", "switch"):
        label(cr, "Swap!", 360, 175, 360, 215, size=34)
    for w in (A("n3", "asleep"), A("n6", "switch")):
        cue("hit", t, w)
    cue("whoosh", t, A("n6", "up"))


# ------------------------------------------------------------------ the doctor's room
def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("d1") - 0.1, A_CLOSE), (A("d1", "broken"), TWO_SHOT),
            (A("d2"), DOC_CLOSE), (A("d2", "most"), TWO_SHOT), (A("d3"), DOC_CLOSE), (A("d3", "breathing"), TWO_SHOT),
            (A("d4"), DOC_CLOSE), (A("d4", "notice"), TWO_SHOT),
            (A("d5"), B_CLOSE), (A("d6"), NEXT_BED),
            (A("d7"), DOC_CLOSE), (A("d7", "which"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    n = dict(eyes="sad", mouth="sad", arms=("face", "down"))
    if A("d2") <= t:
        n.update(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("d6") <= t < A("d7"):
        n.update(eyes="sly", mouth="smirk", arms=("point", "down"), facing=1)
    patient(cr, "danny_b", xa, ya, sa, t, talking=tl.speaking("danny", t), **n)
    m = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("d5") <= t < A("d6"):
        m.update(eyes="wide", mouth="grin")
    if A("d6") <= t < A("d7"):
        m.update(eyes="wide", mouth="o", sweat=True)
    patient(cr, "mike_b", xb, yb, sb, t, talking=tl.speaking("mike", t), **m)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("d2") <= t < A("d5"):
        d.update(arms=("hold", "down"), eyes="happy" if t >= A("d4") else "dot")
    if A("d5") <= t < A("d7"):
        d.update(eyes="sly")
    if A("d7") <= t:     # to camera: hand up at the nose, like he's testing it
        d.update(arms=("face", "down"), eyes="happy")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    if A("d7", "which") <= t:   # the question to the viewer, as a tag
        cr.save()
        cr.identity_matrix()
        label(cr, "LEFT or RIGHT?", 360, 300, size=46)
        cr.restore()
        cue("pop", t, A("d7", "which"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_nose(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
