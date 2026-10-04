"""Body Facts 8: "They Put Someone Else's POOP Inside Him… And It Cured Him" — fecal microbiota transplant (FMT).

Facts (kept general; sources in research_notes/body_facts_7-8.md):
- Used for C. difficile infection that keeps coming back; C. diff often takes over after antibiotics wipe out the
  normal gut bacteria (American College of Gastroenterology; AGA).
- Stool from a screened healthy donor is processed and its bacteria placed in the patient's gut: by colonoscopy,
  enema or capsules; the healthy bacteria crowd out C. diff and rebuild a normal gut (ACG; AGA; reviews).
- Most patients get better: cure rates in studies range from about 60% after one treatment to around 90% (Lancet
  eClinicalMedicine 2025 cohort; capsule vs colonoscopy studies). Script: "most patients get better".
- The FDA approved the first FMT products in 2022 (Rebyota) and 2023 (Vowst). Not used in the script.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.engine import at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.kit import camera, enter_world, set_camera, whip
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch; the doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "colon": dict(voice="af_heart", speed=0.95),
    "germ": dict(voice="am_onyx", speed=0.95),
    "good": dict(voice="af_nova", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"poop", "bacteria", "donor", "fecal", "microbiota", "transplant", "antibiotics"}

SCRIPT = [
    dict(id="f1", scene="gut", text="Oh no. These antibiotics wiped out all my good bacteria.", speaker="colon"),
    dict(id="f2", scene="gut", text="Finally! This whole gut belongs to me now!", speaker="germ"),
    dict(id="f3", scene="gut", text="Help! I've had diarrhea for weeks, and he keeps coming back!", speaker="colon"),
    dict(id="f4", scene="gut", text="Hi! We're healthy bacteria, from a donor.", speaker="good"),
    dict(id="f5", scene="gut", text="From a donor? You mean from someone else's poop?", speaker="germ"),
    dict(id="f6", scene="gut", text="Yep. And there are millions of us!", speaker="good"),
    dict(id="f7", scene="gut", text="Finally! My gut feels normal again.", speaker="colon"),
    dict(id="p1", scene="ward", text="Doctor, did you really put someone else's poop in me?", speaker="mike"),
    dict(id="p2", scene="ward", text="Yes. This is called a fecal microbiota transplant.", speaker="doctor"),
    dict(id="p3", scene="ward", text="Antibiotics killed your good gut bacteria, so a harmful germ took over.",
         speaker="doctor"),
    dict(id="p4", scene="ward", text="We took stool from a healthy, tested donor, and put its good bacteria into "
                                     "your gut.", speaker="doctor"),
    dict(id="p5", scene="ward", text="The good bacteria crowd out the bad germ, and most patients get better.",
         speaker="doctor"),
    dict(id="p6", scene="ward", text="So who was the donor?", speaker="mike", gap=0.3),
    dict(id="p7", scene="ward", text="You're welcome, bro.", speaker="danny", gap=0.35),
]

METADATA = dict(
    title="They Put Someone Else's POOP Inside Him… And It Cured Him 😳",
    alt_titles=["The Poop Transplant Is Real 💩😳", "Doctors Cured Him With a Stranger's Poop 😳"],
    description="""A dangerous gut germ kept coming back. So doctors gave him someone else's poop. 💩😳

It's real. A fecal microbiota transplant (FMT) is used when a gut infection called C. diff keeps coming back, often after antibiotics wipe out the good bacteria. Doctors take stool from a healthy, tested donor and put its good bacteria into the patient's gut. The good bacteria crowd out the bad germ, and most patients get better.

(Cartoon, real medicine. Not medical advice, and never try this at home: talk to a doctor.)

💬 Would you accept a poop transplant? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#PoopTransplant", "#WeirdSurgery", "#Doctor"],
    tags=["fecal microbiota transplant", "poop transplant", "FMT", "C diff", "gut bacteria", "weird medicine",
          "rare treatment", "microbiome", "doctor explains", "medical animation"],
    pinned_comment="Danny gave Mike a kidney story, a liver story… and now THIS. 😂 Would you accept a poop "
                   "transplant? 👇",
)

WALL, WALL_D, FOLD = hexc("#e98a8a"), hexc("#c9686c"), hexc("#d67a7c")
GERM, GERM_D = hexc("#7bc043"), hexc("#4f8a2a")
GOOD = [hexc("#5fb6ff"), hexc("#ffd23f"), hexc("#ff9fc4"), hexc("#9be38a")]


def gut_bg(cr, t, colon_mood, talking):
    """Inside the large intestine: pink walls with folds; the colon's face sits on the wall up top."""
    cr.set_source_rgba(*WALL_D)
    cr.paint()
    shape(cr, [(120, -400), (600, -400), (640, 300), (600, 800), (640, 1600), (80, 1600), (120, 800), (80, 300)],
          hexc("#f4b3ae"), seed=1400, amp=0, lw=5)                                                # the inner lumen
    for k in range(9):   # the colon's folds (haustra)
        y = -200 + 170 * k
        line(cr, [(100, y), (220, y + 40), (360, y + 50), (500, y + 40), (620, y)], 5, FOLD, seed=1401 + k, amp=0)
    eyes(cr, 360, 230, 1.5, colon_mood)
    mouth(cr, 360, 300, 1.3, colon_mood, talking, t)


def germ(cr, t, x, y, s, mood="angry", talking=False, alpha=1.0):
    """C. diff: a green rod-shaped germ with spikes (flagella) and a mean face."""
    if alpha <= 0:
        return
    cr.push_group()
    with at(cr, x, y, s, rot=0.15 * math.sin(t * 2 + x)):
        for k in range(10):
            a = 2 * math.pi * k / 10 + t
            line(cr, [(70 * math.cos(a), 40 * math.sin(a)), (100 * math.cos(a + 0.2), 62 * math.sin(a + 0.3))], 4,
                 GERM_D, seed=1410 + k, amp=0)
        shape(cr, rrect_pts(-80, -46, 160, 92, 46, 16), GERM, seed=1420, amp=0, lw=4)
        eyes(cr, 0, -8, 0.7, mood)
        mouth(cr, 0, 22, 0.6, mood, talking, t)
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)


def good_bug(cr, t, x, y, s, k, mood="happy", talking=False):
    with at(cr, x, y + 4 * math.sin(t * 5 + k), s):
        blob(cr, 0, 0, 40, 34, GOOD[k % 4], seed=1430 + k, amp=0, lw=3.5)
        eyes(cr, 0, -4, 0.42, mood)
        mouth(cr, 0, 14, 0.36, mood, talking, t)


def scope(cr, tip_x, tip_y):
    """Colonoscope: the black tube coming down the gut, a camera light at its tip."""
    shape(cr, [(tip_x - 26, -400), (tip_x + 26, -400), (tip_x + 26, tip_y), (tip_x - 26, tip_y)], hexc("#2a2a30"),
          seed=1440, amp=0, lw=4)
    shape(cr, rrect_pts(tip_x - 34, tip_y - 10, 68, 44, 14, 12), hexc("#c9ced6"), seed=1441, amp=0, lw=4)
    dot(cr, tip_x, tip_y + 14, 10, hexc("#ffe28a"))


def scene_gut(cr, t, tl):
    A = tl.at
    arrive = ease_out(seg(t, A("f4") - 0.6, A("f4") + 0.2))
    spread = ease_out(seg(t, A("f6"), A("f6", end=True) + 0.4))
    win = ease_out(seg(t, A("f6", "millions"), A("f7") + 0.3))
    keys = [(0, (1.05, 360, 640)), (A("f2"), (1.4, 360, 690)), (A("f3"), (1.2, 360, 420)),
            (A("f4"), (1.2, 360, 640)), (A("f5"), (1.4, 360, 690)), (A("f6"), (1.0, 360, 660)),
            (A("f7"), (1.2, 360, 420))]
    set_camera(camera(t, keys))
    enter_world(cr)
    cm = "sad" if t < A("f2") else ("cry" if t < A("f4") else ("worried" if t < A("f7") else "happy"))
    gut_bg(cr, t, cm, tl.speaking("colon", t))
    # antibiotics sweep through at the start, a few good bacteria fading out
    if t < A("f2"):
        for k in range(3):
            u = seg(t, 0.2 + 0.4 * k, 1.4 + 0.4 * k)
            with at(cr, 200 + 160 * k, lerp(-100, 1100, u), 1.0, rot=0.6):
                shape(cr, rrect_pts(-40, -18, 80, 36, 18, 12), hexc("#ffffff"), seed=1450 + k, amp=0, lw=3)
                shape(cr, rrect_pts(0, -18, 40, 36, 18, 12), hexc("#5fb6ff"), seed=1453 + k, amp=0, lw=3)
        for k in range(3):
            a = 1 - seg(t, 0.5 + 0.4 * k, 1.2 + 0.4 * k)
            if a > 0:
                cr.push_group()
                good_bug(cr, t, 220 + 140 * k, 900, 1.0, k, mood="shock")
                cr.pop_group_to_source()
                cr.paint_with_alpha(a)
    # the germs: one boss up front, more spreading; pushed out at the end
    n = 0 if t < A("f2") - 0.2 else 1 + int(5 * seg(t, A("f2"), A("f3", end=True)))
    for k in range(n):
        gx = [360, 200, 520, 230, 490, 360][k]
        gy = [680, 980, 960, 560, 560, 1120][k] + 900 * win
        germ(cr, t, gx, gy, 1.0 if k == 0 else 0.7, mood="angry" if t < A("f5") else "shock",
             talking=tl.speaking("germ", t) and k == 0, alpha=1 - win)
    # the colonoscope brings the donor's good bacteria
    if A("f4") - 0.6 <= t:
        tip = lerp(-200, 360, arrive) if win < 0.5 else lerp(360, -400, seg(t, A("f7"), A("f7") + 0.8))
        scope(cr, 560, tip)
        count = 3 + int(20 * spread)
        for k in range(count):
            r = 0.15 + 0.85 * ((k * 0.618) % 1)
            a = k * 2.39996
            bx = lerp(560, 360 + 220 * r * math.cos(a), min(1.0, spread * 1.3 + 0.2 * (k < 3)))
            by = lerp(tip + 60, 760 + 380 * r * math.sin(a), min(1.0, spread * 1.3 + 0.2 * (k < 3)))
            good_bug(cr, t, bx, by, 0.9, k, talking=tl.speaking("good", t) and k == 0)
    # tags
    if A("f2") <= t < A("f4"):
        label(cr, "C. diff (bad germ)", 500, 620, 400, 740)
    if A("f4") <= t < A("f7"):
        label(cr, "Colonoscope", 600, 300, 580, 400)
        label(cr, "Donor's good bacteria", 230, 420, 530, (tip if win < 0.5 else 360) + 80)
    if t < A("f2"):
        label(cr, "Antibiotics", 560, 560, 520, 700)
    label(cr, "Large intestine", 170, 120, 220, 200)
    for w in (A("f2"), A("f4"), A("f6", "millions")):
        cue("hit", t, w)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("p1") - 0.1, A_CLOSE), (A("p1", "poop"), TWO_SHOT),
            (A("p2"), DOC_CLOSE), (A("p3"), TWO_SHOT), (A("p4"), DOC_CLOSE), (A("p5"), TWO_SHOT),
            (A("p6"), A_CLOSE), (A("p7"), B_CLOSE), (A("p7", "bro"), NEXT_BED)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("p2") <= t < A("p6"):
        m.update(eyes="sad", mouth="wobble")
    if A("p5") <= t < A("p6"):
        m.update(eyes="happy", mouth="grin")
    if A("p6") <= t:
        m.update(eyes="dot", mouth="smile")
    if A("p7") <= t:
        m.update(eyes="wide", mouth="o", sweat=True)
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    n = dict(eyes="happy", mouth="grin", arms=("hold", "down"))
    if A("p7") <= t:
        n.update(arms=("thumb", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("p2") <= t < A("p6"):
        d.update(arms=("hold", "down"), eyes="happy" if A("p5") <= t < A("p6") else "dot")
    if A("p7") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    if A("p2", "fecal") <= t < A("p4"):
        cr.save()
        cr.identity_matrix()
        label(cr, "Fecal microbiota transplant", 360, 320, size=42)
        cr.restore()
        cue("pop", t, A("p2", "fecal"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_gut(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr, logo=False, name="Body Facts")   # made before the logo: stays as released
