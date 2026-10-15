"""Body Facts 23: "Why Bright Sun Makes Some People SNEEZE" — the photic sneeze reflex. Reference style (real
anatomy cut-away, googly-eyed parts, labels, then the masked doctor). Script approved by the owner.

Facts (sources in research_notes/body_facts_23-26.md):
- Photic sneeze reflex (ACHOO syndrome): sneezing on sudden exposure to bright light. Prevalence estimates vary
  (about 18-35%); a large genetic study put it near one in four. Often runs in families (autosomal dominant).
- The mechanism isn't proven. The leading idea: the optic nerve (light) and the trigeminal nerve (which senses the
  nose) run close together, and the light signal "crosses over" and triggers the sneeze. So the doctor says
  "Scientists think".
- Never look straight at the sun (eye damage).
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, blob, cue, dot, ease_out, hexc, lerp, line, seg, shape
from motion.explain import along, googly, sign, stamp, step_card, vessel, zap
from motion.kit import camera, enter_world, set_camera, whip
from videos.brain_freeze import head

STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "eye": dict(voice="af_nova", speed=0.95),
    "optic": dict(voice="am_michael", speed=0.95),
    "trig": dict(voice="af_heart", speed=0.95),
    "nose": dict(voice="bm_george", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"sunlight", "brain", "tickled", "sneezing", "sneeze", "light", "families", "crossed", "sun"}

SCRIPT = [
    dict(id="s1", scene="head", text="Whoa! Bright sunlight, coming in!", speaker="eye"),
    dict(id="s2", scene="head", text="Got it! Sending the light message to the brain.", speaker="optic"),
    dict(id="s3", scene="head", text="Wait, that message is passing right by me. I'm getting tickled!",
         speaker="trig"),
    dict(id="s4", scene="head", text="If he's tickled, I'm sneezing! Ah-choo!", speaker="nose"),
    dict(id="s5", scene="head", text="So light made him sneeze?", speaker="eye"),
    dict(id="s6", scene="head", text="In some people, yes. Scientists call it the sun sneeze.", speaker="trig"),
    dict(id="w1", scene="ward", text="Doctor, why do I sneeze when I look at the sun?", speaker="mike"),
    dict(id="w2", scene="ward", text="It's called the photic sneeze reflex. About one in four people have it.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="Step one. Bright light hits your eyes, and a nerve carries the signal to "
                                     "your brain.", speaker="doctor"),
    dict(id="w4", scene="ward", text="Step two. That signal passes close to the nerve that senses your nose.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="Step three. Scientists think the signals get crossed, and your brain "
                                     "triggers a sneeze.", speaker="doctor"),
    dict(id="w6", scene="ward", text="It often runs in families. And please, never stare at the sun.",
         speaker="doctor"),
    dict(id="w7", scene="ward", text="So I'm allergic to the sun, bro.", speaker="danny", gap=0.3),
    dict(id="w8", scene="ward", text="No. Just to good weather.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Why Bright Sun Makes Some People SNEEZE ☀️🤧",
    alt_titles=["The Sun Sneeze Explained in 3 Steps ☀️", "Do YOU Sneeze in Sunlight? 🤧"],
    description="""About 1 in 4 people sneeze when they step into bright sunlight. Here's why, in 3 steps. ☀️🤧

1. Bright light hits your eyes, and a nerve carries the signal to your brain.
2. That signal passes close to the nerve that senses your nose (the trigeminal nerve).
3. Scientists think the signals get crossed, and your brain triggers a sneeze.

It's called the photic sneeze reflex, and it often runs in families. The exact cause isn't proven yet. And never stare at the sun.

Sources: Cleveland Clinic, "Photic sneeze reflex (ACHOO syndrome)"; Eriksson et al., genome-wide association study of the photic sneeze reflex (PLoS Genetics, 2010).

(Cartoon, real facts. Not medical advice.)

💬 Do YOU sneeze in sunlight? Yes or no 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#SunSneeze", "#BodyFacts", "#Doctor"],
    tags=["sun sneeze", "photic sneeze reflex", "why do i sneeze in sunlight", "achoo syndrome", "sneezing",
          "body facts", "weird body facts", "doctor explains", "medical animation", "science explained"],
    pinned_comment="Sun sneezers, where you at? ☀️🤧 👇",
)

# ---------------------------------------------------------------- the head in profile (from brain_freeze), plus
# the eye, the optic nerve (light, to the brain) and the trigeminal nerve (senses the nose) running side by side
EYE = (188, 402)
OPT = [(222, 404), (290, 414), (360, 422), (430, 426)]
TO_BACK = [(430, 426), (500, 400), (570, 360), (610, 320)]         # on to the back of the brain (vision)
TRIG = [(150, 505), (225, 476), (300, 452), (370, 446), (430, 454), (480, 476)]
NOSE_TIP = (40, 540)
OPTIC_C, TRIG_C = hexc("#f2c032"), hexc("#7fd0a6")


def sun(cr, t, x, y, bright):
    for k in range(12):
        a = k * math.pi / 6 + t * 0.6
        line(cr, [(x + 70 * math.cos(a), y + 70 * math.sin(a)), (x + 100 * math.cos(a), y + 100 * math.sin(a))], 8,
             hexc("#ffcf3a"), seed=5000 + k, amp=0)
    blob(cr, x, y, 56, 56, hexc("#ffd84a"), seed=5012, amp=0, lw=4)
    if bright > 0:
        cr.set_source_rgba(1, 0.97, 0.75, 0.25 * bright)
        cr.paint()


def scene_head(cr, t, tl):
    A = tl.at
    light = ease_out(seg(t, 0.1, A("s1", "sunlight") + 0.2))
    sent = A("s2", "sending")
    tickle = A("s3", "tickled") - 0.4
    boom = A("s4", "choo")
    WIDE, EYEC, NERV, NOSE = (1.0, 330, 520), (1.6, 240, 420), (1.55, 350, 440), (1.1, 210, 500)
    keys = [(0, WIDE), (A("s1", "bright") + 0.1, EYEC), (A("s2"), (1.25, 400, 420)), (A("s3"), NERV),
            (A("s4"), NOSE), (A("s5"), EYEC), (A("s6"), (1.2, 340, 470))]
    set_camera(camera(t, keys))
    enter_world(cr)
    head(cr, t, 0.0)
    sun(cr, t, -40, 230, light if t < A("s5") else 0.4)
    # light rays into the eye
    if light > 0 and t < A("s5"):
        for k in range(3):
            u = (t * 1.6 + k / 3) % 1
            x, y = lerp(10, EYE[0] - 30, u), lerp(290, EYE[1] - 4 + 8 * (k - 1), u)
            line(cr, [(x - 30, y - 22), (x, y)], 6, hexc("#ffd84a"), seed=5020 + k, amp=0)
    # the eyeball (in its socket) with the lens at the front
    blob(cr, EYE[0], EYE[1], 38, 36, WHITE, seed=5030, amp=0, lw=4)
    blob(cr, EYE[0] - 32, EYE[1], 8, 18, hexc("#9ad0ff"), seed=5031, amp=0, lw=2.5)
    # the two nerves, side by side
    vessel(cr, TRIG, 10, TRIG_C if t < tickle else hexc("#b6f0cf"), seed=5040)
    vessel(cr, OPT, 12, OPTIC_C, seed=5050)
    line(cr, TO_BACK, 5, hexc("#c9768c"), seed=5060, amp=0)
    if sent <= t < A("s5"):            # the light message runs to the brain
        for k in range(2):
            pts = OPT + TO_BACK[1:]
            x, y = along(pts, ((t - sent) * 0.9 + k * 0.5) % 1)
            zap(cr, x, y, 0.55)
    if tickle <= t < A("s6"):          # sparks jump across to the face nerve, then race down to the nose
        for k in range(3):
            x = 300 + 50 * k
            if int(t * 10 + k) % 2:
                zap(cr, x, 436, 0.45, col=hexc("#ff8a3a"))
        for k in range(2):
            x, y = along(TRIG[::-1], ((t - tickle) * 1.3 + k * 0.5) % 1)
            zap(cr, x, y, 0.5, col=hexc("#ff8a3a"))
    if boom - 0.1 <= t < boom + 1.4:   # the sneeze blasts out of the nose
        u = seg(t, boom - 0.1, boom + 1.2)
        for k in range(14):
            a = math.pi + (k - 7) * 0.07
            r = 30 + 380 * ease_out(u) * (0.6 + 0.4 * ((k * 37) % 10) / 10)
            dot(cr, NOSE_TIP[0] + r * math.cos(a), NOSE_TIP[1] + r * math.sin(a), 7 - 4 * u, hexc("#cdeefc"))
    # the talking parts: faces on the eye, the two nerves and the nose
    em = "shock" if t < A("s2") else ("worried" if t < A("s6") else "calm")
    googly(cr, t, EYE[0] + 6, EYE[1] - 8, 0.45, em, tl.speaking("eye", t), mouth_dy=34)
    ox, oy = along(OPT, 0.6)
    blob(cr, ox, oy - 26, 40, 34, OPTIC_C, seed=5070, amp=0, lw=3.5)
    googly(cr, t, ox, oy - 34, 0.5, "happy" if sent <= t < tickle else "calm", tl.speaking("optic", t), mouth_dy=26)
    tx, ty = along(TRIG, 0.72)
    blob(cr, tx + 10, ty + 34, 42, 34, TRIG_C, seed=5071, amp=0, lw=3.5)
    tm = "happy" if tickle <= t < A("s5") else ("shock" if A("s3") <= t < tickle else "calm")
    googly(cr, t, tx + 10, ty + 26, 0.5, tm, tl.speaking("trig", t), mouth_dy=26)
    nm = "shock" if A("s4") <= t < boom + 0.6 else ("happy" if t >= boom + 0.6 else "calm")
    googly(cr, t, 225, 515, 0.6, nm, tl.speaking("nose", t), mouth_dy=28)
    # labels, like the references
    if t < A("s2"):
        label(cr, "Eye", 190, 300, 190, 366)
    if A("s2") <= t < A("s3"):
        label(cr, "Optic nerve", 330, 330, 330, 395)
        label(cr, "Brain", 470, 220, 470, 270)
    if A("s3") <= t < A("s4"):
        label(cr, "Optic nerve", 330, 330, 330, 395)
        label(cr, "Face nerve", 470, 560, 440, 470)
    if A("s4") <= t < A("s5"):
        label(cr, "Nose", 200, 620, 220, 545)
    for w in (A("s1", "sunlight"), tickle, boom):
        cue("hit", t, w)
    # screen-space signs
    if A("s3", "tickled") <= t < A("s4"):
        sign(cr, t, A("s3", "tickled"), "SIGNALS CROSSING", y=250, col=hexc("#ff8a3a"), size=48)
    stamp(cr, t, boom, "ACHOO!", x=360, y=260, size=72, end=A("s5"))
    if A("s6", "sun") <= t:
        sign(cr, t, A("s6", "sun"), "THE SUN SNEEZE", y=250, col=hexc("#f2b632"), size=56)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "sun"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w5"), DOC_CLOSE), (A("w6"), TWO_SHOT), (A("w7"), B_CLOSE), (A("w8"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("w7") <= t:
        m.update(eyes="happy", mouth="grin")
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w7") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w8") <= t:
        n.update(eyes="wide", mouth="o", arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w7"):
        d.update(arms=("hold", "down"))
    if A("w8") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    if A("w2", "one") <= t < A("w3"):
        sign(cr, t, A("w2", "one"), "ABOUT 1 IN 4 PEOPLE", y=690, col=hexc("#2f7fd6"), size=46)
    step_card(cr, t, A("w3"), 1, "Bright light hits your eyes: signal to the brain.", end=A("w4") - 0.05)
    step_card(cr, t, A("w4"), 2, "It passes close to the nerve that senses your nose.", end=A("w5") - 0.05)
    step_card(cr, t, A("w5"), 3, "Signals get crossed (scientists think): SNEEZE!", end=A("w6") - 0.05)
    if A("w6") <= t < A("w6", "please"):
        sign(cr, t, A("w6"), "RUNS IN FAMILIES", y=690, col=hexc("#7a5bd0"), size=48)
    if A("w6", "please") <= t < A("w7"):
        sign(cr, t, A("w6", "please"), "NEVER STARE AT THE SUN", y=690, col=hexc("#d8363a"), size=44)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    (scene_ward if name == "ward" else scene_head)(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
