"""Body Facts 1: "The Kidney That Got Donated" — organs as characters, then a doctor answers the real question.

Format inspired by organ-comedy medical Shorts (organs argue about a surgery, then the doctor explains); story,
characters and art are our own, and the topic is advertiser-safe.

Facts (kept general and uncontroversial):
- People can live a normal life with one healthy kidney; living kidney donation is routine.
- After donation the remaining kidney grows (compensatory hypertrophy) and takes over much of the work; donors'
  kidney function typically settles at roughly 70% of their pre-donation total.
- Long-term outcomes for donors are good; follow-up care includes regular checkups and blood-pressure monitoring.
- Living liver donation is also real (a portion of the liver is donated) — used only as the brother's joke.
"""
import math

from motion.captions import captions
from motion.characters import bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(cast={
    # organs and tools: cute but clear. Bright voices pitched up 5-7 semitones (not 8-10: that went chipmunk and
    # smeared the words), spoken a little slower so every word lands
    "lefty": dict(voice="af_heart", speed=1.0, pitch=5),
    "righty": dict(voice="bf_emma", speed=1.0, pitch=5),
    "scalpel": dict(voice="am_puck", speed=1.0, pitch=7),
    "heart": dict(voice="af_bella", speed=1.0, pitch=6),
    "mike": dict(voice="am_michael", speed=1.08),
    "danny": dict(voice="am_adam", speed=1.08),
})                                   # the doctor speaks in the narrator voice (the owner's clone)
TAIL = 1.0

SCRIPT = [
    dict(id="k1", scene="body", text="Hey. Why is there a surgeon in here? Nobody's sick!", speaker="lefty"),
    dict(id="k2", scene="body", text="The owner's brother needs a kidney. And he said yes!", speaker="righty"),
    dict(id="k3", scene="body", text="Wait. Which one of us is going?", speaker="lefty"),
    dict(id="k4", scene="body", text="And the lucky kidney is... This one!", speaker="scalpel", pace=0.92),
    dict(id="k5", scene="body", text="No, no, no! Righty, remember me!", speaker="lefty"),
    dict(id="k6", scene="body", text="Lefty? Lefty! I can't do this alone! I'm only half the team!", speaker="righty"),
    dict(id="k7", scene="body", text="Relax. You're about to get a promotion.", speaker="heart"),
    dict(id="k8", scene="body", text="Wait. Why am I getting bigger?", speaker="righty"),
    dict(id="k9", scene="hospital", text="Doc, I gave away a kidney. Can I really live with just one?",
         speaker="mike"),
    dict(id="k10", scene="hospital", text="Yes. One healthy kidney is enough.", speaker="doctor"),
    dict(id="k11", scene="hospital", text="Over the next few months, it grows bigger, and takes over most of the work.",
         speaker="doctor"),
    dict(id="k12", scene="hospital",
         text="Most donors live long, normal lives. Just get regular checkups, and watch your blood pressure.",
         speaker="doctor"),
    dict(id="k13", scene="hospital", text="Thanks, bro. Also, I might need half a liver.", speaker="danny"),
    dict(id="k14", scene="hospital", text="Doc. Can I live without a brother?", speaker="mike", gap=0.3),
    dict(id="k15", scene="hospital", text="Medically? Yes.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="He Donated a Kidney… Then His Other Kidney Did THIS 😳",
    alt_titles=["Can You Live With Just One Kidney? 🫘", "What Happens When You Donate a Kidney 😳"],
    description="""Two kidneys. One brother who needs one. Guess who's going. 😳

Can you really live with just one kidney? Yes. One healthy kidney is enough, and after a donation the other one grows bigger and takes over most of the work. Most living donors go on to live long, normal lives, with regular checkups and an eye on their blood pressure.

(Funny cartoon, real facts. Not medical advice: talk to a doctor about your own health.)

💬 Would you donate a kidney to your brother? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Kidney", "#BodyFacts", "#Doctor"],
    tags=["kidney donation", "one kidney", "can you live with one kidney", "kidney donor", "body facts", "doctor explains",
          "human body", "organ donation", "health facts", "funny animation", "interestingly strange"],
    pinned_comment="Be honest: would you give your brother a kidney? 😂 What about half a liver? 👇",
)

BLUE = hexc("#3f6fb5")
GREEN = hexc("#2e9e52")
KID_A, KID_B = hexc("#c85a4a"), hexc("#8e2f2a")      # kidney gradient: light -> dark
ART, VEIN = hexc("#d8433a"), hexc("#3f62b5")
URETER = hexc("#e8c08a")
BONE, BONE_D = hexc("#f2e6cf"), hexc("#d9c7a3")
LX, RX, KY = 175, 545, 660                          # kidney centres


# ------------------------------------------------------------------ drawing helpers
def grad_fill(cr, pts, c0, c1, cx, cy, r, stroke=INK, lw=4.0):
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    import cairo
    g = cairo.RadialGradient(cx - r * 0.35, cy - r * 0.4, r * 0.1, cx, cy, r * 1.15)
    g.add_color_stop_rgba(0, *c0)
    g.add_color_stop_rgba(1, *c1)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(*stroke)
    cr.set_line_width(lw)
    cr.set_line_join(1)
    cr.stroke()


def bean(cx, cy, rx, ry, notch_dir):
    """Kidney outline; the notch (hilum) points along notch_dir (+1 = right, -1 = left)."""
    a0 = 0.0 if notch_dir > 0 else math.pi
    pts = []
    for k in range(96):
        a = k / 96 * 2 * math.pi
        d = math.atan2(math.sin(a - a0), math.cos(a - a0))
        r = 1 - 0.3 * math.exp(-(d * d) / 0.16)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def eyes(cr, x, y, s, mood, look=0.0, blink=False):
    for side in (-1, 1):
        ex = x + side * 22 * s
        if blink or mood == "happy":
            line(cr, [(ex - 12 * s, y + 2 * s), (ex, y - 8 * s), (ex + 12 * s, y + 2 * s)], 4 * s, INK, seed=11 + side,
                 amp=0.1)
            continue
        big = 1.25 if mood in ("shock", "cry") else 1.0
        blob(cr, ex, y, 16 * s * big, 19 * s * big, WHITE, seed=12 + side, amp=0.2, lw=3.5 * s)
        pr = 7 * s if mood != "shock" else 5 * s
        dot(cr, ex + look * 6 * s, y + 3 * s, pr, INK)
        dot(cr, ex + look * 6 * s + 2.5 * s, y - 1 * s, 2 * s, WHITE)
        if mood == "angry":
            line(cr, [(ex - 16 * s * side * -1, y - 28 * s), (ex + 14 * s * side * -1, y - 18 * s)], 5 * s, INK,
                 seed=15 + side, amp=0.1)
        elif mood in ("sad", "cry", "worried"):
            line(cr, [(ex - 14 * s * side, y - 18 * s), (ex + 12 * s * side, y - 28 * s)], 4 * s, INK, seed=17 + side,
                 amp=0.1)
        if mood == "cry":
            blob(cr, ex + 8 * s, y + 30 * s, 5 * s, 9 * s, hexc("#8fd3ff"), seed=19 + side, amp=0.2, lw=2 * s)


def mouth(cr, x, y, s, mood, talking, t):
    if talking:
        o = 0.5 + 0.5 * abs(math.sin(t * 22))
        blob(cr, x, y, 11 * s, (4 + 10 * o) * s, hexc("#5a1f22"), seed=21, amp=0.2, lw=3 * s)
        return
    if mood in ("shock", "cry"):
        blob(cr, x, y, 10 * s, 13 * s, hexc("#5a1f22"), seed=22, amp=0.2, lw=3 * s)
    elif mood in ("sad", "worried", "angry"):
        line(cr, [(x - 12 * s, y + 5 * s), (x, y - 3 * s), (x + 12 * s, y + 5 * s)], 4 * s, INK, seed=23, amp=0.1)
    else:
        line(cr, [(x - 14 * s, y - 3 * s), (x, y + 7 * s), (x + 14 * s, y - 3 * s)], 4 * s, INK, seed=24, amp=0.1)


def kidney(cr, t, x, y, s, notch_dir, mood="calm", talking=False, look=0.0, shake=0.0):
    x += math.sin(t * 50) * shake
    y += math.sin(t * 2.3 + x) * 3
    grad_fill(cr, bean(x, y, 92 * s, 128 * s, notch_dir), KID_A, KID_B, x, y, 130 * s, lw=4.5)
    blob(cr, x - 30 * s * notch_dir, y - 62 * s, 16 * s, 26 * s, hexc("#ffffff", 0.25), seed=31, amp=0.2, lw=0,
         stroke=None)
    eyes(cr, x - 6 * s * notch_dir, y - 18 * s, s, mood, look, blink=(int(t * 10 + x) % 37 == 0))
    mouth(cr, x - 6 * s * notch_dir, y + 30 * s, s, mood, talking, t)


def heart(cr, t, x, y, s, mood="calm", talking=False):
    b = 1 + 0.06 * max(0, math.sin(t * 7.5)) ** 8          # heartbeat
    with at(cr, x, y, s * b):
        pts = []
        for k in range(80):
            a = k / 80 * 2 * math.pi
            pts.append((16 * math.sin(a) ** 3 * 4.2, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a)
                                                       - math.cos(4 * a)) * 4.2))
        grad_fill(cr, pts, hexc("#ff6b6b"), hexc("#b5222a"), 0, 0, 80, lw=4)
        eyes(cr, 0, -6, 0.75, mood)
        mouth(cr, 0, 22, 0.75, mood, talking, t)


def scalpel(cr, t, x, y, s, rot, talking=False, mood="calm"):
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-10, 20, 20, 120, 8, 12), hexc("#9aa3ad"), seed=41, amp=0.2, lw=3.5)
        for k in range(4):
            line(cr, [(-8, 40 + k * 22), (8, 40 + k * 22)], 2.5, hexc("#6b737d"), seed=42 + k, amp=0.1)
        sharp_shape(cr, [(-10, 22), (10, 22), (12, -30), (0, -80), (-6, -40)], hexc("#e7ecf1"), seed=46, amp=0.2,
                    lw=3.5)
        line(cr, [(4, -20), (2, -60)], 3, WHITE, seed=47, amp=0.1)
        eyes(cr, 0, 64, 0.55, mood)
        mouth(cr, 0, 92, 0.5, mood, talking, t)


def spine(cr):
    for k in range(14):
        y = 260 + k * 76
        shape(cr, rrect_pts(318, y, 84, 56, 16, 12), BONE, seed=60 + k, amp=0.3, lw=3.5)
        line(cr, [(330, y + 28), (390, y + 28)], 2.5, BONE_D, seed=80 + k, amp=0.2)
    line(cr, [(300, 200), (300, 1300)], 18, ART, seed=90, amp=0.3)       # aorta
    line(cr, [(420, 200), (420, 1300)], 18, VEIN, seed=91, amp=0.3)      # vena cava


def vessels(cr, x, s, side, cut=0.0):
    """Renal artery/vein from the kidney's notch to the big vessels, plus the ureter down to the bladder."""
    hx = x + side * 78 * s
    tx = 300 if side > 0 else 420
    for dy, col, tx2 in ((-18, ART, 300), (18, VEIN, 420)):
        end = lerp(tx2, hx, cut)
        line(cr, [(hx, KY + dy), (lerp(hx, end, 0.5), KY + dy - 10), (end, KY + dy)], 11, col, seed=100 + dy + side,
             amp=0.3)
    line(cr, [(hx - side * 6, KY + 40), (hx + side * 30, KY + 260), (360 - side * 40, 1150)], 10, URETER,
         seed=110 + side, amp=0.4)
    if cut:
        for dy in (-18, 18):    # surgical clips on the cut ends
            shape(cr, rrect_pts(lerp(tx, hx, 0) - 10 if side > 0 else tx - 10, KY + dy - 9, 20, 18, 3, 8),
                  hexc("#c9ccd2"), seed=120 + dy, amp=0.2, lw=2.5)


def bladder(cr):
    blob(cr, 360, 1185, 110, 70, hexc("#f2c38e"), seed=130, amp=0.5, lw=4)
    blob(cr, 330, 1160, 24, 12, hexc("#ffffff", 0.35), seed=131, amp=0.3, lw=0, stroke=None)


def body_bg(cr):
    import cairo
    g = cairo.RadialGradient(360, 640, 80, 360, 640, 900)
    g.add_color_stop_rgba(0, *hexc("#f7c9bd"))
    g.add_color_stop_rgba(1, *hexc("#c4675d"))
    cr.rectangle(-900, -900, 2600, 3200)
    cr.set_source(g)
    cr.fill()
    for k in range(9):   # soft tissue blobs
        blob(cr, -100 + (k * 173) % 900, 120 + (k * 311) % 1200, 140, 90, hexc("#ffffff", 0.06), seed=140 + k,
             amp=1.0, lw=0, stroke=None)


# ------------------------------------------------------------------ scene 1: inside the body
def scene_body(cr, t, tl):
    A = tl.at
    take = A("k5", "no,")
    gone = ease_out(seg(t, take, take + 0.9))          # Lefty lifted out
    grow = ease_out(seg(t, A("k8", "bigger") - 0.4, A("k8", "bigger") + 0.6))
    rs = 1.0 + 0.32 * grow + (0.04 * math.sin(t * 9) if A("k8") <= t else 0)
    keys = [(0, (1.25, 360, 660)), (A("k1", "surgeon"), (1.4, 520, 520)), (A("k1", "nobody's"), (1.9, LX, KY - 20)),
            (A("k2"), (1.9, RX, KY - 20)), (A("k2", "brother"), (1.2, 360, 640)), (A("k2", "yes"), (1.8, RX, KY - 20)),
            (A("k3"), (1.0, 360, 660)), (A("k3", "which"), (1.7, LX, KY - 30)),
            (A("k4"), (1.25, 360, 560)), (A("k4", "this"), (2.0, LX, KY - 60)),
            (take, (1.0, 260, 560)), (A("k5", "remember"), (1.3, 250, 420)),
            (A("k6"), (1.7, RX, KY - 20)), (A("k6", "alone"), (1.0, 360, 660)), (A("k6", "half"), (1.9, RX, KY - 40)),
            (A("k7"), (1.8, 360, 420)), (A("k7", "promotion"), (1.3, 430, 560)),
            (A("k8"), (1.6, RX, KY - 20)), (A("k8", "bigger"), (1.1, 450, 640))]
    set_camera(camera(t, keys))
    enter_world(cr)
    body_bg(cr)
    spine(cr)
    bladder(cr)
    vessels(cr, LX, 1.0, 1, cut=seg(t, take, take + 0.3))
    vessels(cr, RX, rs, -1)
    # ---- the heart, up top
    hmood = "happy" if t >= A("k7") else ("worried" if A("k5") <= t < A("k7") else "calm")
    heart(cr, t, 360, 330, 1.15, hmood, talking=tl.speaking("heart", t))
    # ---- Righty
    rmood = "calm"
    if A("k1") <= t < A("k2"):
        rmood = "worried"
    if A("k2") <= t < A("k3"):
        rmood = "happy"
    if A("k3") <= t < take:
        rmood = "worried"
    if take <= t < A("k7"):
        rmood = "cry" if t >= A("k6") else "shock"
    if A("k7") <= t < A("k8"):
        rmood = "worried"
    if A("k8") <= t:
        rmood = "shock"
    kidney(cr, t, RX, KY, rs, -1, rmood, tl.speaking("righty", t), look=-1 if t < take + 1 else -0.5,
           shake=2.0 if rmood == "cry" else 0)
    # ---- Lefty (until the scalpel takes it)
    if gone < 1:
        lmood = "worried" if A("k1") <= t < A("k4") else "calm"
        if A("k4") <= t:
            lmood = "shock"
        if A("k5") <= t:
            lmood = "cry"
        lx = lerp(LX, 260, gone)
        ly = lerp(KY, -500, gone)
        kidney(cr, t, lx, ly, 1.0, 1, lmood, tl.speaking("lefty", t), look=1 if t < A("k4") else 0,
               shake=1.5 if A("k4", "this") <= t else 0)
    else:
        blob(cr, LX, KY, 70, 100, hexc("#000000", 0.08), seed=150, amp=0.6, lw=0, stroke=None)   # empty spot
        if t >= A("k6"):
            write(cr, [("(empty)", hexc("#7a3a35"))], LX, KY + 10, 34, align="center", bold=True)
    # ---- the scalpel arrives, picks, and leaves with Lefty
    arrive = ease_out(seg(t, A("k1", "surgeon") - 0.2, A("k1", "surgeon") + 0.5))
    if t >= A("k1", "surgeon") - 0.2:
        sx, sy, rot = lerp(760, 560, arrive), lerp(120, 380, arrive), -0.5
        if A("k4") <= t < A("k4", "this"):      # "and the lucky kidney is...": pointing back and forth
            k = math.sin((t - A("k4")) * 9)
            sx, sy, rot = 360 + 150 * k, 430, 2.6 + 0.4 * k
        elif A("k4", "this") <= t < take:
            sx, sy, rot = LX + 40, KY - 230, 2.9
        elif t >= take:
            sx, sy, rot = lerp(LX + 40, 280, gone), lerp(KY - 230, -700, gone), 2.9
        scalpel(cr, t, sx, sy, 1.15, rot, talking=tl.speaking("scalpel", t), mood="happy" if t < A("k4") else "calm")
    # ---- screen text
    hl(cr, t, [("WHICH KIDNEY ", INK), ("GOES?", RED)], 215, 66, 0.0, end=A("k1", "nobody's") - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("brother needs a ", INK), ("KIDNEY", RED)], 215, 60, A("k2", "brother"), end=A("k3") - 0.05, bold=True)
    hl(cr, t, [("\"And the ", INK), ("LUCKY", RED), (" kidney is...\"", INK)], 215, 50, A("k4"), end=A("k4", "this") - 0.05, bold=True)
    stamp(cr, t, A("k4", "this"), "THIS ONE!", dur=0.6, y=330)
    hl(cr, t, [("\"I'm only ", INK), ("HALF", RED), (" the team!\"", INK)], 215, 56, A("k6", "half"),
       end=A("k7") - 0.05, bold=True)
    hl(cr, t, [("a ", INK), ("PROMOTION", GREEN), ("?", INK)], 215, 70, A("k7", "promotion"), end=A("k8") - 0.05,
       bold=True)
    hl(cr, t, [("\"Why am I getting ", INK), ("BIGGER", RED), ("?\"", INK)], 215, 54, A("k8", "bigger"), bold=True)
    for w in (A("k4", "this"), take, A("k8", "bigger")):
        cue("hit", t, w)
    cue("whoosh", t, take)


# ------------------------------------------------------------------ scene 2: the hospital
DOC_X, MIKE_X, DANNY_X = 360, 140, 580


def room(cr, t):
    import cairo
    g = cairo.LinearGradient(0, 0, 0, 1280)
    g.add_color_stop_rgba(0, *hexc("#dfe7ee"))
    g.add_color_stop_rgba(1, *hexc("#c6d3de"))
    cr.rectangle(-900, -900, 2600, 3200)
    cr.set_source(g)
    cr.fill()
    shape(cr, rrect_pts(-900, 640, 2600, 260, 0, 8), hexc("#7f9db8"), seed=200, amp=0.2, lw=0, stroke=None)
    shape(cr, rrect_pts(-900, 900, 2600, 1200, 0, 8), hexc("#e9edf1"), seed=201, amp=0.2, lw=3)
    # hospital sign
    shape(cr, rrect_pts(300, 330, 140, 140, 16, 12), hexc("#2f80d6"), seed=202, amp=0.3, lw=4)
    shape(cr, rrect_pts(355, 352, 30, 96, 4, 8), WHITE, seed=203, amp=0.2, lw=0, stroke=None)
    shape(cr, rrect_pts(322, 385, 96, 30, 4, 8), WHITE, seed=204, amp=0.2, lw=0, stroke=None)
    # window
    shape(cr, rrect_pts(520, 330, 170, 200, 10, 12), hexc("#bfe6ff"), seed=205, amp=0.3, lw=4)
    line(cr, [(605, 330), (605, 530)], 4, INK, seed=206, amp=0.2)
    # IV stand
    line(cr, [(60, 520), (60, 900)], 5, hexc("#9aa3ad"), seed=207, amp=0.2)
    shape(cr, rrect_pts(40, 520, 40, 60, 10, 10), hexc("#e8f4ff"), seed=208, amp=0.3, lw=3)


def bed_back(cr, x, side):
    hx = x - side * 110
    shape(cr, rrect_pts(hx - 12, 680, 24, 250, 8, 10), hexc("#9aa3ad"), seed=210 + x, amp=0.2, lw=3.5)
    blob(cr, hx + side * 50, 760, 60, 32, WHITE, seed=211 + x, amp=0.4, lw=3.5)          # pillow


def bed_front(cr, x):
    shape(cr, [(x - 125, 895), (x + 125, 888), (x + 135, 1030), (x - 130, 1035)], hexc("#f8f9fb"), seed=220 + x,
          amp=0.5, lw=4)
    line(cr, [(x - 115, 930), (x + 125, 924)], 3, hexc("#d6dce3"), seed=221 + x, amp=0.3)
    shape(cr, rrect_pts(x - 135, 1030, 270, 26, 6, 10), hexc("#9aa3ad"), seed=222 + x, amp=0.2, lw=3.5)


def scene_hospital(cr, t, tl):
    A = tl.at
    # faces must land above the caption line (screen y ~860); doctor's face is at world y ~813, the patients' ~767
    DOCF, MIK, DAN = (1.8, DOC_X, 860), (1.8, MIKE_X + 30, 800), (1.8, DANNY_X - 30, 800)
    WIDE, CARD = (1.0, 370, 760), (1.2, 380, 770)
    keys = [(A("k9") - 0.1, (1.05, 360, 770)), (A("k9", "kidney"), MIK), (A("k9", "live"), (1.3, 280, 760)),
            (A("k10"), DOCF), (A("k10", "enough"), CARD),
            (A("k11"), WIDE), (A("k11", "bigger"), (1.5, 380, 640)), (A("k11", "work"), DOCF),
            (A("k12"), WIDE), (A("k12", "checkups"), (1.5, 380, 640)), (A("k12", "blood"), DOCF),
            (A("k13"), DAN), (A("k13", "liver"), (1.4, 520, 640)),
            (A("k14"), (2.0, MIKE_X + 30, 800)), (A("k14", "brother"), (1.2, 370, 770)),
            (A("k15"), (2.2, DOC_X, 860)), (A("k15", "yes"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    room(cr, t)
    bed_back(cr, MIKE_X, 1)
    bed_back(cr, DANNY_X, -1)
    # the doctor, between the beds
    d = dict(facing=-1 if t < A("k13") else 1, arms=("hold", "hip"), eyes="dot", mouth="smile")
    if A("k10") <= t < A("k13"):
        d.update(arms=("point", "hip"), eyes="happy" if t < A("k12") else "dot")
    if A("k13") <= t < A("k15"):
        d.update(eyes="wide", mouth="o", facing=1)
    if A("k15") <= t:
        d.update(eyes="sly", mouth="flat", facing=-1, arms=("hip", "hip"))
    if tl.speaking("doctor", t):
        d["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "doctor", DOC_X, 1010, t, scale=1.12, **d)
    # Mike (the donor) and Danny (got the kidney), sitting up in bed
    m = dict(facing=1, arms=("hold", "down"), eyes="dot", mouth="smile")
    if A("k9") <= t < A("k10"):
        m.update(eyes="wide", mouth="o")
    if A("k10") <= t < A("k13"):
        m.update(eyes="happy", mouth="grin")
    if A("k13", "liver") <= t:
        m.update(eyes="wide", mouth="o", sweat=True, shake=1.0 if t < A("k14") else 0)
    if A("k14") <= t:
        m.update(eyes="sly", mouth="flat", arms=("point", "down"), shake=0)
    if tl.speaking("mike", t):
        m["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "mike", MIKE_X, 935, t, **m)
    n = dict(facing=-1, arms=("hold", "down"), eyes="happy", mouth="grin")
    if A("k13") <= t:
        n.update(arms=("thumb", "down"), eyes="happy", mouth="grin")
    if A("k15") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    if tl.speaking("danny", t):
        n["mouth"] = "o" if int(t * 12) % 2 else "grin"
    person(cr, "danny", DANNY_X, 935, t, **n)
    bed_front(cr, MIKE_X)
    bed_front(cr, DANNY_X)
    write(cr, [("DONOR", BLUE)], MIKE_X, 990, 30, align="center", bold=True)
    write(cr, [("GOT THE KIDNEY", RED)], DANNY_X, 990, 24, align="center", bold=True)
    # fact cards
    for key, end, txt, col in (("k10", "k11", "1 kidney = enough", GREEN), ("k11", "k12", "it grows bigger", BLUE),
                               ("k12", "k13", "checkups + blood pressure", INK)):
        if A(key) <= t < A(end):
            with at(cr, 380, 600, max(0.85, pop(t, A(key), 0.25))):
                shape(cr, rrect_pts(-210, -40, 420, 80, 18, 12), WHITE, seed=240, amp=0.3, lw=3.5)
                write(cr, [(txt, col)], 0, 14, 38 if len(txt) < 20 else 30, align="center", bold=True)
            cue("pop", t, A(key))
    if A("k13", "liver") <= t < A("k14"):   # the liver he wants next
        with at(cr, DANNY_X + 90, 560, max(0.85, pop(t, A("k13", "liver"), 0.25))):
            blob(cr, 0, 0, 90, 60, WHITE, seed=250, amp=0.6, lw=3.5)
            shape(cr, [(-60, -10), (-20, -34), (50, -26), (64, 0), (20, 30), (-50, 20)], hexc("#a0453a"), seed=251,
                  amp=0.6, lw=3)
            write(cr, [("1/2", WHITE)], 0, 12, 34, align="center", bold=True)
    hl(cr, t, [("Can you live with ", INK), ("ONE", RED), (" kidney?", INK)], 215, 56, A("k9", "live"),
       end=A("k10") - 0.05, bold=True)
    hl(cr, t, [("YES", GREEN), (". One is enough.", INK)], 215, 62, A("k10"), end=A("k11") - 0.05, bold=True)
    hl(cr, t, [("the other one ", INK), ("GROWS", BLUE)], 215, 62, A("k11", "bigger"), end=A("k12") - 0.05, bold=True)
    hl(cr, t, [("long, ", INK), ("normal", GREEN), (" lives", INK)], 215, 66, A("k12"), end=A("k13") - 0.05, bold=True)
    hl(cr, t, [("\"...", INK), ("HALF A LIVER", RED), (".\"", INK)], 215, 60, A("k13", "liver"), end=A("k14") - 0.05,
       bold=True)
    hl(cr, t, [("\"Can I live without a ", INK), ("BROTHER", RED), ("?\"", INK)], 215, 50, A("k14", "brother"),
       end=A("k15") - 0.05, bold=True)
    stamp(cr, t, A("k15", "yes"), "MEDICALLY: YES", dur=0.8, y=330)
    for w in (A("k13", "liver"), A("k15", "yes")):
        cue("hit", t, w)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "hospital":
        scene_hospital(cr, t, tl)
    else:
        scene_body(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
