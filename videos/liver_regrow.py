"""Body Facts 4: "He Gave Away Half His Liver… Then It Grew Back" — the sequel to the kidney episode (Danny asked
for half a liver at the end of it).

Facts (kept general and uncontroversial; sources in research_notes/body_facts_2-4.md):
- Living liver donors give part of their liver (UPMC: "anywhere from 25% to 65%"); adult recipients usually get the
  larger right lobe.
- The liver regrows: UPMC says it regrows "to full size and function in both the donor and the recipient" in about
  8-10 weeks, and is back to its pre-donation health within a few months. So: "in a few months, almost full size".
- The removed lobe does not reappear; the remaining liver gets bigger, so the mass comes back but not the original
  shape (compensatory growth; e.g. StatPearls / Wikipedia "Liver regeneration").
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, seg, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.organs import big_lobe_pts, calendar, card, lobe, small_lobe_pts
from videos.kidney_donor import BLUE, GREEN, bed_back, bed_front, body_bg, heart, room, scalpel

NARRATOR = dict(cast={
    # voices styled on the owner's reference Short (see brain_awake.py)
    "big": dict(voice="bm_daniel", speed=1.0, pitch=2),      # the big lobe
    "small": dict(voice="bm_george", speed=1.0, pitch=2),    # the small lobe
    "scalpel": dict(voice="bf_alice", speed=1.0, pitch=4),   # same scalpel voice as the brain episode
    "heart": dict(voice="af_jessica", speed=1.0, pitch=4),
    "mike": dict(voice="am_michael", speed=1.08),
    "danny": dict(voice="am_adam", speed=1.08),
})                                   # the doctor speaks in the narrator voice (the owner's clone)
TAIL = 1.0

SCRIPT = [
    dict(id="l1", scene="body", text="Hello again! I came for half a liver.", speaker="scalpel"),
    dict(id="l2", scene="body", text="Wait, which half?", speaker="small"),
    dict(id="l3", scene="body", text="The big guy!", speaker="scalpel"),
    dict(id="l4", scene="body", text="What, me? Little guy, you can't run this place alone!", speaker="big"),
    dict(id="l5", scene="body", text="Hey, come back! I'm way too small!", speaker="small"),
    dict(id="l6", scene="body", text="Relax. Just give it a few weeks.", speaker="heart"),
    dict(id="l7", scene="body", text="Wait, what? Oh no. Oh no! I'm getting huge!", speaker="small"),
    dict(id="h1", scene="ward", text="Doc, I gave my brother half my liver. Is it gone forever?", speaker="mike"),
    dict(id="h2", scene="ward", text="No. Your liver grows back.", speaker="doctor"),
    dict(id="h3", scene="ward", text="In a few months, it's almost full size again. Just a different shape.",
         speaker="doctor"),
    dict(id="h4", scene="ward", text="And your brother's half grows bigger too.", speaker="doctor"),
    dict(id="h5", scene="ward", text="So now we both have a whole liver?", speaker="danny"),
    dict(id="h6", scene="ward", text="Pretty much, yes.", speaker="doctor"),
    dict(id="h7", scene="ward", text="Thanks, bro. So, do lungs grow back too?", speaker="danny"),
    dict(id="h8", scene="ward", text="Doc. Can I live without a brother?", speaker="mike", gap=0.3),
    dict(id="h9", scene="ward", text="Medically? Still yes.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="He Gave Away Half His Liver… Then It Grew Back 😳",
    alt_titles=["Your Liver Can Grow Back. Here's How 😳", "One Liver Became Two 🤯"],
    description="""He gave his brother half his liver. A few months later, they both had a whole one. 😳

The liver can grow back. After a living donation, the part that's left gets bigger, and in a few months it's almost full size again. Not the same shape, but the same job. And the brother's half grows bigger too.

(Funny cartoon, real facts. Not medical advice: talk to a doctor about your own health.)

💬 Would you give half your liver to your brother? 👇

🔔 Body Facts: your organs argue, then the doctor explains what's really going on. (Part 1: the kidney.)""",
    hashtags=["#Liver", "#BodyFacts", "#Doctor"],
    tags=["liver regeneration", "liver grows back", "living liver donor", "can your liver grow back",
          "liver donation", "liver facts", "body facts", "doctor explains", "human body", "funny animation",
          "health facts"],
    pinned_comment="Danny already got a kidney AND half a liver. 😂 What should he ask for next? 👇",
)

BIG = (250, 640)       # big lobe (the patient's right: screen left)
SMALL = (440, 650)     # small lobe


def scene_body(cr, t, tl):
    A = tl.at
    take = A("l5")
    gone = ease_out(seg(t, take - 0.1, take + 0.8))
    grow = ease_out(seg(t, A("l7", "no"), A("l7", "huge", end=True) + 0.4))
    sx0, sy0 = SMALL
    sx, sy = lerp(sx0, 360, grow), lerp(sy0, 650, grow)
    ss = 1.0 + 0.12 * grow + (0.03 * math.sin(t * 9) if A("l7", "no") <= t < A("l7", "huge", end=True) else 0)
    keys = [(0, (1.15, 360, 680)), (A("l1", "half"), (1.25, 420, 520)), (A("l1", "liver"), (1.0, 360, 660)),
            (A("l2"), (1.7, 470, 720)), (A("l3"), (1.3, 380, 560)), (A("l3", "big"), (1.6, 200, 720)),
            (A("l4"), (1.7, 210, 720)), (A("l4", "alone"), (1.0, 360, 660)),
            (take, (1.3, 400, 640)), (A("l5", "small"), (1.8, 470, 720)),
            (A("l6"), (1.7, 360, 420)), (A("l6", "weeks"), (1.1, 380, 560)),
            (A("l7"), (1.6, 460, 720)), (A("l7", "no"), (1.05, 360, 640))]
    set_camera(camera(t, keys))
    enter_world(cr)
    body_bg(cr)
    # ---- the heart, up top
    hm = "happy" if t >= A("l6") else ("worried" if A("l4") <= t < A("l6") else "calm")
    heart(cr, t, 360, 300, 1.0, hm, talking=tl.speaking("heart", t))
    # ---- the big lobe, until it leaves for the brother
    if gone < 1:
        bx, by = lerp(BIG[0], 300, gone), lerp(BIG[1], -600, gone)
        bm = "calm" if t < A("l1", "liver") else "worried"
        if A("l3", "big") <= t:
            bm = "shock"
        if A("l4", "alone") <= t:
            bm = "cry"
        lobe(cr, t, big_lobe_pts(bx, by, 1.0), bx - 60, by - 30, 1.0, bm, tl.speaking("big", t), look=0.6,
             shake=1.5 if A("l3", "big") <= t else 0)
    else:
        blob(cr, BIG[0] - 30, BIG[1], 150, 80, hexc("#000000", 0.07), seed=600, amp=0.6, lw=0, stroke=None)
    # ---- the small lobe
    sm = "calm"
    if A("l1", "liver") <= t < A("l3"):
        sm = "worried"
    if A("l3") <= t < take:
        sm = "happy"
    if take <= t < A("l6"):
        sm = "cry"
    if A("l6") <= t < A("l7", "no"):
        sm = "worried"
    if A("l7", "no") <= t:
        sm = "shock" if t < A("l7", "huge") else "happy"
    lobe(cr, t, small_lobe_pts(sx, sy, ss, grow), sx + lerp(30, 0, grow) * ss, sy - 22 * ss,
         0.85 + 0.25 * grow, sm, tl.speaking("small", t), look=-0.8 if t < take + 0.8 else 0,
         shake=2.0 if sm == "cry" else 0)
    # ---- the scalpel
    arrive = ease_out(seg(t, 0.0, 0.5))
    px, py, rot = lerp(760, 560, arrive), lerp(120, 360, arrive), -0.5
    if A("l3", "big") <= t < take:
        px, py, rot = BIG[0] + 30, BIG[1] - 250, 2.9
    elif t >= take:
        px, py, rot = lerp(BIG[0] + 30, 330, gone), lerp(BIG[1] - 250, -800, gone), 2.9
    if t < take + 1.0:
        scalpel(cr, t, px, py, 1.15, rot, talking=tl.speaking("scalpel", t), mood="happy")
    # ---- weeks ticking by while it regrows
    if A("l7", "no") <= t:
        wk = 1 + int(7 * seg(t, A("l7", "no"), A("l7", "huge", end=True)))
        cr.save()
        cr.identity_matrix()
        calendar(cr, t, 600, 380, f"WEEK {wk}", A("l7", "no"))
        cr.restore()
    # ---- screen text
    hl(cr, t, [("HALF", RED), (" a liver?!", INK)], 215, 70, 0.0, end=A("l2") - 0.05, bold=True, sound=False)
    hl(cr, t, [("\"The ", INK), ("BIG", RED), (" guy!\"", INK)], 215, 66, A("l3", "big"), end=A("l4", "alone"), bold=True)
    hl(cr, t, [("off to his ", INK), ("BROTHER", BLUE)], 215, 62, take, end=A("l6") - 0.05, bold=True)
    hl(cr, t, [("\"I'm getting ", INK), ("HUGE", RED), ("!\"", INK)], 215, 64, A("l7", "huge"), bold=True)
    stamp(cr, t, A("l1", "liver"), "HI AGAIN!", dur=0.6, y=330)
    for w in (A("l3", "big"), take, A("l7", "huge")):
        cue("hit", t, w)
    cue("whoosh", t, take)
    cue("whoosh", t, 0.05)


# ------------------------------------------------------------------ the ward
DOC_X, MIKE_X, DANNY_X = 360, 140, 580


def mini_liver(cr, x, y, s):
    blob(cr, x, y, 54 * s, 34 * s, hexc("#8e2f2a"), seed=610, amp=0.6, lw=3)
    blob(cr, x - 14 * s, y - 10 * s, 14 * s, 7 * s, hexc("#ffffff", 0.3), seed=611, amp=0.3, lw=0, stroke=None)


def scene_ward(cr, t, tl):
    A = tl.at
    DOCF, MIK, DAN = (1.8, DOC_X, 860), (1.8, MIKE_X + 30, 800), (1.8, DANNY_X - 30, 800)
    WIDE = (1.0, 370, 760)
    keys = [(A("h1") - 0.1, (1.05, 360, 770)), (A("h1", "liver"), MIK), (A("h1", "forever"), (1.3, 280, 760)),
            (A("h2"), DOCF), (A("h2", "grows"), WIDE),
            (A("h3"), DOCF), (A("h3", "different"), WIDE),
            (A("h4"), (1.3, 470, 760)), (A("h5"), DAN), (A("h6"), DOCF), (A("h6", "yes"), WIDE),
            (A("h7"), DAN), (A("h7", "lungs"), (1.4, 520, 700)),
            (A("h8"), (2.0, MIKE_X + 30, 800)), (A("h8", "brother"), (1.2, 370, 770)),
            (A("h9"), (2.2, DOC_X, 860)), (A("h9", "yes"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    room(cr, t)
    bed_back(cr, MIKE_X, 1)
    bed_back(cr, DANNY_X, -1)
    d = dict(facing=-1, arms=("hold", "hip"), eyes="dot", mouth="smile")
    if A("h2") <= t < A("h7"):
        d.update(arms=("point", "hip"), eyes="happy" if t >= A("h3") else "dot", facing=-1 if t < A("h4") else 1)
    if A("h7") <= t < A("h9"):
        d.update(eyes="wide", mouth="o", facing=1)
    if A("h9") <= t:
        d.update(eyes="sly", mouth="flat", facing=-1, arms=("hip", "hip"))
    if tl.speaking("doctor", t):
        d["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "doctor", DOC_X, 1010, t, scale=1.12, **d)
    m = dict(facing=1, arms=("hold", "down"), eyes="sad", mouth="sad")
    if A("h2") <= t < A("h7"):
        m.update(eyes="happy", mouth="grin")
    if A("h7", "lungs") <= t:
        m.update(eyes="wide", mouth="o", sweat=True, shake=1.0 if t < A("h8") else 0)
    if A("h8") <= t:
        m.update(eyes="sly", mouth="flat", arms=("point", "down"), shake=0)
    if tl.speaking("mike", t):
        m["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "mike", MIKE_X, 935, t, **m)
    n = dict(facing=-1, arms=("hold", "down"), eyes="happy", mouth="grin")
    if A("h7") <= t:
        n.update(arms=("thumb", "down"))
    if A("h9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    if tl.speaking("danny", t):
        n["mouth"] = "o" if int(t * 12) % 2 else "grin"
    person(cr, "danny", DANNY_X, 935, t, **n)
    bed_front(cr, MIKE_X)
    bed_front(cr, DANNY_X)
    write(cr, [("GAVE HALF", BLUE)], MIKE_X, 990, 28, align="center", bold=True)
    write(cr, [("GOT HALF", RED)], DANNY_X, 990, 28, align="center", bold=True)
    for key, end, runs in (("h2", "h3", [("the liver ", INK), ("GROWS BACK", GREEN)]),
                           ("h3", "h4", [("full size, ", GREEN), ("new shape", BLUE)]),
                           ("h4", "h5", [("his half ", INK), ("grows too", GREEN)])):
        if A(key) <= t < A(end):
            cr.save()
            cr.identity_matrix()
            card(cr, t, A(key), 360, 320, runs, size=44, w=520)
            cr.restore()
            cue("pop", t, A(key))
    if A("h5", "whole") <= t < A("h7"):        # one liver became two
        cr.save()
        cr.identity_matrix()
        for x in (250, 470):
            mini_liver(cr, x, 330, max(0.85, min(1.3, 5 * (t - A("h5", "whole")))))
        cr.restore()
        cue("pop", t, A("h5", "whole"))
    hl(cr, t, [("Gone ", INK), ("FOREVER", RED), ("?", INK)], 215, 64, A("h1", "forever"), end=A("h2") - 0.05,
       bold=True)
    hl(cr, t, [("NO", GREEN), (". It grows back.", INK)], 215, 62, A("h2"), end=A("h3") - 0.05, bold=True)
    hl(cr, t, [("in a ", INK), ("few months", BLUE)], 215, 64, A("h3", "months"), end=A("h4") - 0.05, bold=True)
    hl(cr, t, [("2 brothers, ", INK), ("2 livers", GREEN)], 215, 64, A("h5", "whole"), end=A("h7") - 0.05, bold=True)
    hl(cr, t, [("\"Do ", INK), ("LUNGS", RED), (" grow back?\"", INK)], 215, 58, A("h7", "lungs"), end=A("h8") - 0.05,
       bold=True)
    hl(cr, t, [("\"Can I live without a ", INK), ("BROTHER", RED), ("?\"", INK)], 215, 50, A("h8", "brother"),
       end=A("h9") - 0.05, bold=True)
    stamp(cr, t, A("h9", "yes"), "STILL YES.", dur=0.9, y=330)
    for w in (A("h7", "lungs"), A("h9", "yes")):
        cue("hit", t, w)


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
