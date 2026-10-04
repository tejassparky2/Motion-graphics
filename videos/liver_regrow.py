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
from motion.engine import INK, RED, blob, cue, ease_out, hexc, lerp, line, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.organs import big_lobe_pts, calendar, card, lobe, small_lobe_pts
from motion.surgery import BLOOD, BLOOD_D, DRAPE, SKIN, SKIN_D, clamp, cut_line, drapes, ellipse, forceps, \
    scalpel_tip, slit, stitches, wound
from videos.kidney_donor import BLUE, GREEN, bed_back, bed_front, heart, room, scalpel

NARRATOR = dict(cast={
    # voices styled on the owner's reference Short (see brain_awake.py)
    "big": dict(voice="bm_daniel", speed=1.0, pitch=2),      # the big lobe
    "small": dict(voice="bm_george", speed=1.0, pitch=2),    # the small lobe
    "scalpel": dict(voice="af_jessica", speed=1.0, pitch=4),   # same scalpel voice as the brain episode
    "heart": dict(voice="af_river", speed=1.0, pitch=4),
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

WX, WY, WRX, WRY = 360, 640, 260, 210   # the incision in the belly
SLIT = slit(WX, WY, WRX, 30)
BIG = (285, 625)       # big lobe (the patient's right: screen left)
SMALL = (455, 635)     # small lobe
LS = 0.72              # lobe scale inside the belly


def belly(cr):
    """The patient's belly on the table (asleep under the drapes), like the knee in the reference."""
    shape(cr, [(40, 120), (680, 120), (700, 600), (690, 1300), (30, 1300), (20, 600)], SKIN, seed=600, amp=1.0,
          lw=4.5)
    for k in range(4):       # rib edges showing through, up top
        y = 230 + 44 * k
        line(cr, [(110, y + 40), (250, y), (360, y + 30 - 6 * k)], 3.5, SKIN_D, seed=601 + k, amp=0.6)
        line(cr, [(610, y + 40), (470, y), (360, y + 30 - 6 * k)], 3.5, SKIN_D, seed=605 + k, amp=0.6)
    blob(cr, 360, 1060, 16, 22, SKIN_D, seed=609, amp=0.4, lw=3.5)       # belly button
    for x0 in (-260, 980):   # drapes over his sides
        shape(cr, [(x0 - 300, 0), (x0 + 300 if x0 < 0 else x0 - 300, 0), (x0 + 330 if x0 < 0 else x0 - 330, 1400),
                   (x0 - 300, 1400)], DRAPE, seed=610 + x0, amp=1.0, lw=4)


def guts(cr):
    """Background inside the belly: the bowel loops underneath."""
    for k in range(6):
        blob(cr, 150 + 85 * k, 790 + 18 * (k % 2), 62, 40, hexc("#e58d8a"), seed=620 + k, amp=0.6, lw=3)
        line(cr, [(118 + 85 * k, 790), (182 + 85 * k, 800)], 2.5, hexc("#b8605e"), seed=630 + k, amp=0.4)


def scene_body(cr, t, tl):
    A = tl.at
    cut = seg(t, 0.05, A("l1", "liver") - 0.15)
    open_u = ease_out(seg(t, A("l1", "liver") - 0.15, A("l1", "liver") + 0.45))
    split = seg(t, A("l3", "big"), A("l3", end=True) + 0.5)               # cut between the lobes
    take = A("l5")
    gone = seg(t, take, take + 1.8) ** 1.6
    close = ease_out(seg(t, A("l6", "weeks"), A("l6", "weeks") + 0.5))
    sew = seg(t, A("l6", "weeks") + 0.3, A("l6", end=True) + 0.4)
    xray = ease_out(seg(t, A("l7") - 0.1, A("l7") + 0.3))
    grow = ease_out(seg(t, A("l7", "no"), A("l7", "huge", end=True) + 0.4))
    sx, sy = lerp(SMALL[0], 360, grow), lerp(SMALL[1], 630, grow)
    ss = LS * (1.0 + 0.3 * grow) + (0.02 * math.sin(t * 9) if A("l7", "no") <= t < A("l7", "huge", end=True) else 0)
    SMF, BGF, WIDE = (1.7, 477, 700), (1.7, 240, 690), (1.0, 360, 700)
    keys = [(0, (1.2, 360, 650)), (A("l1", "liver"), WIDE),
            (A("l2"), SMF), (A("l3"), (1.3, 380, 580)), (A("l3", "big"), BGF),
            (A("l4"), BGF), (A("l4", "alone"), WIDE),
            (take, (1.0, 360, 560)), (A("l5", "small"), SMF),
            (A("l6"), (1.5, 360, 560)), (A("l6", "weeks"), WIDE),
            (A("l7"), SMF), (A("l7", "no"), (1.15, 360, 660))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    belly(cr)
    # ---- moods
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
    bm = "calm" if t < A("l1", "liver") else "worried"
    if A("l3", "big") <= t:
        bm = "shock"
    if A("l4", "alone") <= t:
        bm = "cry"
    hm = "happy" if t >= A("l6") else ("worried" if A("l4") <= t < A("l6") else "calm")

    def small(c):
        lobe(c, t, small_lobe_pts(sx, sy, ss, grow), sx + lerp(22, 0, grow) * ss / LS, sy - 16 * ss / LS,
             0.65 + 0.3 * grow, sm, tl.speaking("small", t), look=-0.8 if t < take + 0.8 else 0,
             shake=2.0 if sm == "cry" else 0)

    def big(c, x, y):
        lobe(c, t, big_lobe_pts(x, y, LS), x - 45, y - 22, 0.72, bm, tl.speaking("big", t), look=0.6,
             shake=1.5 if A("l3", "big") <= t else 0)

    def inside(c):
        guts(c)
        heart(c, t, 360, 505, 0.6, hm, talking=tl.speaking("heart", t))      # peeking down from the chest
        if gone <= 0:
            big(c, *BIG)
        else:
            blob(c, BIG[0], BIG[1], 120, 70, hexc("#4a1a20"), seed=640, amp=0.6, lw=0, stroke=None)
        small(c)
        if split > 0:                                                         # the cut between the lobes
            n = int(20 * split)
            pts = [(372 + 6 * math.sin(k), 565 + 8 * k) for k in range(max(2, n))]
            line(c, pts, 7, BLOOD_D, seed=641, amp=0.4)
            line(c, pts, 4, BLOOD, seed=642, amp=0.4)

    # ---- the opening, then the stitched cut, then the x-ray view
    if open_u <= 0:
        tip = cut_line(cr, SLIT, cut)
    elif close < 1:
        tip = None
        wound(cr, t, WX, WY, WRX, WRY, open_u * (1 - close), inside, seed=1)
    else:
        tip = None
    if close >= 1:
        if xray > 0:
            cr.save()
            cr.new_path()
            pts = ellipse(WX, WY, WRX, WRY)
            cr.move_to(*pts[0])
            for p in pts[1:]:
                cr.line_to(*p)
            cr.close_path()
            cr.clip()
            cr.push_group()
            cr.set_source_rgba(*hexc("#5a2430"))
            cr.paint()
            inside(cr)
            cr.set_source_rgba(*hexc("#bfe3ff", 0.18))
            cr.paint()
            cr.pop_group_to_source()
            cr.paint_with_alpha(0.85 * xray)
            cr.restore()
            shape(cr, ellipse(WX, WY, WRX, WRY), None, seed=650, amp=0.4, lw=4, stroke=hexc("#2b3a66", xray))
            write(cr, [("X-RAY VIEW", hexc("#2b3a66", xray))], WX, WY - WRY - 18, 34, align="center", bold=True)
        stitches(cr, SLIT, sew if xray <= 0 else 1.0)
    # ---- clamps hold it open
    if open_u >= 1 and close < 0.3:
        hold = ease_out(seg(t, A("l1", "liver") + 0.45, A("l1", "liver") + 0.85)) * (1 - close / 0.3)
        cm = "happy" if t < A("l4") else "worried"
        clamp(cr, t, lerp(WX - WRX - 300, WX - WRX + 10, hold), WY, -1, 0.9, cm, look=0.5)
        clamp(cr, t, lerp(WX + WRX + 300, WX + WRX - 10, hold), WY, 1, 0.9, cm, look=0.5)
    # ---- the big lobe is lifted out with forceps, dripping
    if 0 < gone < 1:
        bx, by = BIG[0] + 40 * gone, BIG[1] - 1100 * gone
        forceps(cr, bx - 10, by - 70, 1.0, grip=1.0)
        big(cr, bx, by)
        for k in range(3):
            u = (t * 1.8 + k / 3) % 1
            blob(cr, bx - 60 + 50 * k, by + 70 + 220 * u, 6, 9, BLOOD, seed=660 + k, amp=0.2, lw=2, stroke=BLOOD_D)
    # ---- the scalpel: cuts in, greets, then cuts between the lobes
    sc = 1.15
    if t < A("l1", "liver") - 0.15:
        px, py = tip if tip is not None else SLIT[0]
        rot = math.pi - 0.25
        sx_, sy_ = scalpel_tip(px, py, rot, sc)
    elif A("l3", "big") <= t < take + 0.4:
        rot = math.pi - 0.1
        u = min(1.0, split)
        sx_, sy_ = scalpel_tip(372, 565 + 160 * u, rot, sc)
    else:
        rot, sx_, sy_ = 2.7, 560, 300
    if t < take + 0.4 or t >= A("l6") + 99:
        scalpel(cr, t, sx_, sy_, sc, rot, talking=tl.speaking("scalpel", t), mood="happy")
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
    for w in (A("l1", "liver") - 0.15, A("l3", "big"), take, A("l7", "huge")):
        cue("hit", t, w)
    cue("whoosh", t, take)
    cue("scribble", t, 0.05, 0.8)


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
