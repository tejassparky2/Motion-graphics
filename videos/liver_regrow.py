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
from motion.engine import blob, cue, ease_out, hexc, lerp, line, seg, shape, write
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import big_lobe_pts, calendar, lobe, small_lobe_pts
from motion.surgery import BLOOD, BLOOD_D, DRAPE, SKIN, SKIN_D, clamp, cut_line, drapes, ellipse, forceps, \
    scalpel_tip, slit, stitches, wound
from videos.kidney_donor import heart, scalpel

# Voices: natural stock voices at their own pitch (owner: the pitched-up voices weren't clear), a touch slower.
# The doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "big": dict(voice="am_michael", speed=0.95),      # the big lobe
    "small": dict(voice="af_heart", speed=0.95),      # the small lobe
    "scalpel": dict(voice="af_bella", speed=0.95),    # same scalpel voice as the brain episode
    "heart": dict(voice="af_sarah", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})                                   # the doctor speaks in the narrator voice (the owner's clone)
TAIL = 1.0
EMPHASIS = {"liver", "transplant", "donor", "grows", "months", "shape", "huge"}   # bigger captions

SCRIPT = [
    dict(id="l1", scene="body", text="Hello again, liver! I'm here to take half of you.", speaker="scalpel"),
    dict(id="l2", scene="body", text="Half of me? Which half?", speaker="small"),
    dict(id="l3", scene="body", text="The big one, on the right side.", speaker="scalpel"),
    dict(id="l4", scene="body", text="Me? But the little one can't do all this work alone!", speaker="big"),
    dict(id="l5", scene="body", text="Wait, come back! I'm way too small to do this!", speaker="small"),
    dict(id="l6", scene="body", text="Relax, little liver. Just give it a few weeks.", speaker="heart"),
    dict(id="l7", scene="body", text="What's happening to me? I'm getting huge!", speaker="small"),
    dict(id="h1", scene="ward", text="Doctor, I gave my brother half of my liver. Is it gone forever?", speaker="mike"),
    dict(id="h2", scene="ward", text="No. Your liver grows back.", speaker="doctor"),
    dict(id="h3", scene="ward", text="In a few months, it's almost full size again. Just a different shape.",
         speaker="doctor"),
    dict(id="h4", scene="ward", text="And your brother's half grows bigger too.", speaker="doctor"),
    dict(id="h4b", scene="ward", text="This surgery is called a living donor liver transplant.", speaker="doctor"),
    dict(id="h5", scene="ward", text="So now we both have a whole liver?", speaker="danny"),
    dict(id="h6", scene="ward", text="Pretty much, yes.", speaker="doctor"),
    dict(id="h7", scene="ward", text="Thanks, bro. Hey, do lungs grow back too?", speaker="danny"),
    dict(id="h8", scene="ward", text="Doctor, can I live without a brother?", speaker="mike", gap=0.3),
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
    grow = ease_out(seg(t, A("l7", "happening"), A("l7", "huge", end=True) + 0.4))
    sx, sy = lerp(SMALL[0], 360, grow), lerp(SMALL[1], 630, grow)
    ss = LS * (1.0 + 0.3 * grow) + (0.02 * math.sin(t * 9) if A("l7", "happening") <= t < A("l7", "huge", end=True) else 0)
    SMF, BGF, WIDE = (1.7, 477, 700), (1.7, 240, 690), (1.0, 360, 700)
    keys = [(0, (1.2, 360, 650)), (A("l1", "liver"), WIDE),
            (A("l2"), SMF), (A("l3"), (1.3, 380, 580)), (A("l3", "big"), BGF),
            (A("l4"), BGF), (A("l4", "alone"), WIDE),
            (take, (1.0, 360, 560)), (A("l5", "small"), SMF),
            (A("l6"), (1.5, 360, 560)), (A("l6", "weeks"), WIDE),
            (A("l7"), SMF), (A("l7", "happening"), (1.15, 360, 660))]
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
    if A("l6") <= t < A("l7", "happening"):
        sm = "worried"
    if A("l7", "happening") <= t:
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
    if A("l7", "happening") <= t:
        wk = 1 + int(7 * seg(t, A("l7", "happening"), A("l7", "huge", end=True)))
        cr.save()
        cr.identity_matrix()
        calendar(cr, t, 600, 380, f"WEEK {wk}", A("l7", "happening"))
        cr.restore()
    # ---- screen text
    # ---- anatomy tags, like the references
    if t < A("l1", "liver") - 0.15:
        label(cr, "Liver (under here)", 250, 470, 330, 600)
    elif close <= 0:
        if gone <= 0:
            label(cr, "Liver: right lobe", 170, 400, 240, 560)
        label(cr, "Liver: left lobe", 560, 400, 470, 580)
        label(cr, "Heart", 360, 380, 360, 450)
    if xray > 0 and grow > 0.5:
        label(cr, "Left lobe: growing", 540, 470, 430, 600)
    for w in (A("l1", "liver") - 0.15, A("l3", "big"), take, A("l7", "huge")):
        cue("hit", t, w)
    cue("whoosh", t, take)
    cue("scribble", t, 0.05, 0.8)


# ------------------------------------------------------------------ the doctor's room
def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("h1") - 0.1, A_CLOSE), (A("h1", "forever"), TWO_SHOT),
            (A("h2"), DOC_CLOSE), (A("h3"), TWO_SHOT), (A("h3", "different"), DOC_CLOSE),
            (A("h4"), NEXT_BED), (A("h4b"), DOC_CLOSE), (A("h5"), B_CLOSE), (A("h6"), DOC_CLOSE),
            (A("h7"), B_CLOSE), (A("h7", "lungs"), NEXT_BED),
            (A("h8"), A_CLOSE), (A("h9"), DOC_CLOSE), (A("h9", "yes"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    m = dict(eyes="sad", mouth="sad", arms=("hold", "down"))
    if A("h2") <= t < A("h7"):
        m.update(eyes="happy", mouth="grin")
    if A("h7", "lungs") <= t:
        m.update(eyes="wide", mouth="o", sweat=True)
    if A("h8") <= t:
        m.update(eyes="sly", mouth="flat", arms=("point", "down"), sweat=False)
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    n = dict(eyes="happy", mouth="grin", arms=("hold", "down"))
    if A("h7") <= t:
        n.update(arms=("thumb", "down"))
    if A("h9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("h2") <= t < A("h7"):
        d.update(arms=("hold", "down"), eyes="happy" if t >= A("h3") else "dot")
    if A("h7") <= t < A("h9"):
        d.update(eyes="wide")
    if A("h9") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)


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
