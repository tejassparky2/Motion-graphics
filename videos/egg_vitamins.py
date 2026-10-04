"""Body Facts 11: "Can 5 Eggs a Day Replace Your Multivitamin?" — a fact-check of a viral claim.

The owner asked for this (via a scheduled request from the Interestingly Strange chat): a viral fitness reel says
3-5 eggs a day means you'd never need a multivitamin. Don't name or mock the creator: "a viral video says...".

Facts, per large egg (50 g), USDA FoodData Central (sources in research_notes/body_facts_11.md):
- protein 6.3 g; choline 147 mg (27% DV); selenium 15.4 µg (28%); riboflavin 0.23 mg (18%); B12 0.45 µg (19%).
  Five eggs: choline ~135%, selenium ~140%, B12 ~95% of a day's needs.
- vitamin D 1 µg (5%), vitamin A 80 µg RAE (9%), folate 24 µg (6%), iron 0.88 mg (5%).
- vitamin C 0, fiber 0, calcium 28 mg (2%; five eggs ~10%), magnesium 6 mg (1%), potassium 69 mg (1%).
- cholesterol 186 mg. AHA science advisory (Carson et al., Circulation 2020): healthy people can include about one
  whole egg a day in a heart-healthy diet (older people with normal cholesterol up to two). Script: "about one egg
  a day fits a healthy diet. Eating more? Check with your doctor, especially if your cholesterol is high."
- NIH Office of Dietary Supplements: get nutrients mainly from food; some groups need supplements (pregnancy:
  folic acid; vegans: B12). The script says "most healthy people with a varied diet don't need one".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.engine import INK, WHITE, at, blob, cue, ease_out, hexc, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import brain
from videos.kidney_donor import eyes, grad_fill, mouth
from videos.tooth_eye import tooth

# Voices: natural stock voices at their own pitch; the doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "egg": dict(voice="am_michael", speed=0.95),
    "brain": dict(voice="af_heart", speed=0.95),
    "blood": dict(voice="af_bella", speed=0.95),
    "bone": dict(voice="am_onyx", speed=0.95),
    "gums": dict(voice="af_nova", speed=0.95),
    "gut": dict(voice="am_liam", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"eggs", "multivitamin", "choline", "calcium", "fiber", "zero", "cholesterol"}

SCRIPT = [
    dict(id="e1", scene="plate", text="A viral video says five eggs a day can replace your multivitamin.",
         speaker="egg"),
    dict(id="e2", scene="plate", text="Honestly? Five eggs give me more choline than I need in a day.",
         speaker="brain"),
    dict(id="e3", scene="plate", text="And they cover almost all of my vitamin B12.", speaker="blood"),
    dict(id="e4", scene="plate", text="Then where's my calcium? Five eggs barely give me one tenth.", speaker="bone"),
    dict(id="e5", scene="plate", text="I'm still waiting for vitamin C. Eggs have zero.", speaker="gums"),
    dict(id="e6", scene="plate", text="Fiber? Also zero. I'm starving down here.", speaker="gut"),
    dict(id="e7", scene="plate", text="Okay. Maybe I'm not a whole multivitamin.", speaker="egg"),
    dict(id="p1", scene="ward", text="Doctor, I eat five eggs a day. Do I need a multivitamin?",
         speaker="mike"),
    dict(id="p2", scene="ward", text="Eggs are a great food. But they can't replace a multivitamin.",
         speaker="doctor"),
    dict(id="p3", scene="ward", text="They give you protein, choline, selenium and vitamin B12.", speaker="doctor"),
    dict(id="p4", scene="ward", text="But they have no vitamin C, no fiber, and very little calcium.",
         speaker="doctor"),
    dict(id="p5", scene="ward", text="Heart experts say about one egg a day fits a healthy diet.", speaker="doctor"),
    dict(id="p5b", scene="ward", text="Eating more? Ask your doctor, especially if your cholesterol is high.",
         speaker="doctor"),
    dict(id="p6", scene="ward", text="And most healthy people with a varied diet don't need one at all.",
         speaker="doctor"),
    dict(id="p7", scene="ward", text="So, how many eggs do you eat a day?", speaker="doctor"),
    dict(id="p8", scene="ward", text="Twelve, bro.", speaker="danny", gap=0.3),
    dict(id="p9", scene="ward", text="Danny. We need to talk.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Can 5 Eggs a Day Replace Your Multivitamin? 🥚",
    alt_titles=["Eggs vs Multivitamin: The Truth 🥚😳", "A Viral Video Says Eggs Replace Vitamins. Do They? 🥚"],
    description="""A viral video says 3 to 5 eggs a day means you'll never need a multivitamin. We checked. 🥚

Partly true. Five large eggs give you more than a day's choline and selenium, and almost all your vitamin B12, plus great protein. But eggs have zero vitamin C, zero fiber, and very little calcium, magnesium and potassium. So eggs are a great food, not a full multivitamin: add fruit, vegetables, whole grains and dairy (or other calcium sources).

Cholesterol: heart experts (American Heart Association) say about one egg a day fits a healthy diet for most people. If you have high cholesterol, diabetes or heart disease, ask your doctor how many eggs are right for you.

Do you need a multivitamin at all? Most healthy people with a varied diet don't. Some people do, for example during pregnancy (folic acid), vegans (vitamin B12), or anyone with a deficiency their doctor has found.

Sources: USDA FoodData Central (egg, whole, large); NIH Office of Dietary Supplements (multivitamin fact sheet); American Heart Association science advisory on dietary cholesterol (Circulation, 2020).

(Cartoon, real nutrition facts. Not medical advice: talk to a doctor about your own health.)

💬 How many eggs do you eat a day? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Eggs", "#Nutrition", "#Doctor"],
    tags=["eggs vs multivitamin", "are eggs healthy", "egg nutrition", "do I need a multivitamin", "choline",
          "vitamin B12", "eggs and cholesterol", "how many eggs a day", "nutrition facts", "doctor explains",
          "body facts"],
    pinned_comment="Be honest: how many eggs do you eat a day? 🥚 Danny says twelve. 😂 👇",
)

BG, BG_D = hexc("#ffe9b8"), hexc("#f6d58e")
EGG, EGG_D, YOLK = hexc("#fffaf0"), hexc("#e9dcc4"), hexc("#ffc928")
GOOD, LOW, NONE = hexc("#3fae5c"), hexc("#f2a33a"), hexc("#d8363a")
ROWS = [  # (speaker, nutrient, percent of a day's needs from five large eggs, line it appears with)
    ("brain", "CHOLINE", 135, "e2"),
    ("blood", "VITAMIN B12", 95, "e3"),
    ("bone", "CALCIUM", 10, "e4"),
    ("gums", "VITAMIN C", 0, "e5"),
    ("gut", "FIBER", 0, "e6"),
]
ROW_Y0, ROW_DY = 470, 90
BAR_X, BAR_W = 215, 345
EGG_Y = 300                        # clear of the corner logo


def egg(cr, t, x, y, s, mood="happy", talking=False, face=True):
    with at(cr, x, y + 3 * math.sin(t * 2.4 + x), s):
        pts = [(70 * math.sin(a), -96 * math.cos(a) * (1.0 if math.cos(a) > 0 else 0.8)) for a in
               [2 * math.pi * k / 80 for k in range(80)]]
        grad_fill(cr, pts, EGG, EGG_D, -20, -30, 110, lw=4)
        blob(cr, -26, -50, 14, 22, hexc("#ffffff", 0.7), seed=1700, amp=0, lw=0, stroke=None)
        if face:
            eyes(cr, 0, -6, 0.9, mood)
            mouth(cr, 0, 34, 0.8, mood, talking, t)


def blood_cell(cr, t, x, y, s, mood, talking):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 70, 62, hexc("#d8363a"), seed=1710, amp=0, lw=4)
        blob(cr, 0, 2, 40, 32, hexc("#b5222a"), seed=1711, amp=0, lw=0, stroke=None)
        eyes(cr, 0, -6, 0.7, mood)
        mouth(cr, 0, 26, 0.6, mood, talking, t)


def bone(cr, t, x, y, s, mood, talking):
    with at(cr, x, y, s):
        col = hexc("#f6efdf")
        for sx in (-1, 1):
            for sy in (-1, 1):
                blob(cr, sx * 78, sy * 22, 28, 28, col, seed=1720 + sx + 2 * sy, amp=0, lw=4)
        shape(cr, rrect_pts(-82, -26, 164, 52, 20, 20), col, seed=1725, amp=0, lw=0, stroke=None)
        line(cr, [(-60, -26), (60, -26)], 4, INK, seed=1726, amp=0)
        line(cr, [(-60, 26), (60, 26)], 4, INK, seed=1727, amp=0)
        eyes(cr, 0, -4, 0.6, mood)
        mouth(cr, 0, 16, 0.45, mood, talking, t)


def gut_char(cr, t, x, y, s, mood, talking):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 80, 62, hexc("#f4a6a0"), seed=1730, amp=0, lw=4)
        for k in range(3):
            line(cr, [(-60, -30 + 24 * k), (-30, -40 + 24 * k), (0, -28 + 24 * k), (30, -40 + 24 * k),
                      (60, -30 + 24 * k)], 3, hexc("#d67a7c"), seed=1731 + k, amp=0)
        eyes(cr, 0, -4, 0.7, mood)
        mouth(cr, 0, 28, 0.6, mood, talking, t)


def organ(cr, t, who, x, y, s, mood, talking):
    if who == "brain":
        brain(cr, t, x, y, 0.36 * s, mood, talking)
    elif who == "blood":
        blood_cell(cr, t, x, y, 0.62 * s, mood, talking)
    elif who == "bone":
        bone(cr, t, x, y, 0.5 * s, mood, talking)
    elif who == "gums":
        tooth(cr, t, x, y + 6, 0.42 * s, mood, talking)
    else:
        gut_char(cr, t, x, y, 0.6 * s, mood, talking)


def scene_plate(cr, t, tl):
    A = tl.at
    rows_at = [A(r[3]) for r in ROWS]
    TOP = (1.35, 360, 330)
    keys = [(0, (1.15, 360, 420)), (A("e1"), TOP), (A("e1", "multivitamin"), (1.6, 360, 320))]
    for k, start in enumerate(rows_at):
        keys.append((start, (1.15, 360, ROW_Y0 + ROW_DY * k - 40)))
    keys += [(A("e7"), (0.82, 360, 740))]          # whole board, kept above the caption line
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*BG)
    cr.paint()
    for k in range(10):   # kitchen tiles
        line(cr, [(-400, -300 + 170 * k), (1200, -300 + 170 * k)], 3, BG_D, seed=1740 + k, amp=0)
    # the plate of five eggs, the talking one in front
    blob(cr, 400, EGG_Y + 60, 220, 46, WHITE, seed=1750, amp=0, lw=4)
    blob(cr, 400, EGG_Y + 57, 176, 30, hexc("#eef1f5"), seed=1751, amp=0, lw=0, stroke=None)
    for k, (ex, ey) in enumerate([(240, EGG_Y + 40), (310, EGG_Y + 26), (490, EGG_Y + 26), (560, EGG_Y + 40)]):
        egg(cr, t, ex, ey, 0.48, face=False)
    em = "happy"
    if A("e4") <= t < A("e7"):
        em = "worried"
    if A("e7") <= t:
        em = "sad"
    egg(cr, t, 400, EGG_Y, 0.85, em, tl.speaking("egg", t))
    # the scoreboard: one row per nutrient, filled as each organ speaks
    for k, (who, name, pct, line_id) in enumerate(ROWS):
        start = A(line_id)
        if t < start - 0.15:
            continue
        y = ROW_Y0 + ROW_DY * k
        u = ease_out(seg(t, start + 0.2, start + 1.0))
        col = GOOD if pct >= 80 else (LOW if pct > 0 else NONE)
        talking = tl.speaking(who, t) and t < A(ROWS[k + 1][3]) if k + 1 < len(ROWS) else tl.speaking(who, t)
        mood = "happy" if pct >= 80 else ("sad" if pct > 0 else "cry")
        if talking and pct < 80:
            mood = "worried"
        organ(cr, t, who, 125, y, 1.2, mood, talking)
        shape(cr, rrect_pts(BAR_X, y - 27, BAR_W, 54, 16, 16), WHITE, seed=1760 + k, amp=0, lw=3.5)
        w = BAR_W * min(1.0, pct / 100) * u
        if w > 6:
            shape(cr, rrect_pts(BAR_X, y - 27, w, 54, 16, 16), col, seed=1765 + k, amp=0, lw=3.5)
        write(cr, [(name, INK)], BAR_X + 16, y + 12, 32)
        shown = int(round(pct * u))
        write(cr, [(f"{shown}%", col if pct > 0 else NONE)], BAR_X + BAR_W + 12, y + 13, 36, bold=True)
        cue("pop", t, start + 0.2)
    if t >= A("e2") - 0.15:
        write(cr, [("WHAT 5 EGGS GIVE YOU (% OF A DAY)", INK)], 360, ROW_Y0 - 44, 26, align="center")
    for w in (A("e1", "multivitamin"), A("e5", "zero"), A("e6", "zero")):
        cue("hit", t, w)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("p1") - 0.1, A_CLOSE), (A("p1", "multivitamin"), TWO_SHOT),
            (A("p2"), DOC_CLOSE), (A("p3"), TWO_SHOT), (A("p4"), DOC_CLOSE), (A("p5"), TWO_SHOT),
            (A("p5b"), DOC_CLOSE), (A("p6"), TWO_SHOT), (A("p7"), DOC_CLOSE), (A("p8"), B_CLOSE),
            (A("p9"), NEXT_BED)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    m = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("p4") <= t < A("p6"):
        m.update(eyes="wide", mouth="o")
    if A("p6") <= t:
        m.update(eyes="happy", mouth="grin")
    if A("p8") <= t:
        m.update(eyes="wide", mouth="o", sweat=False)
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("p8") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("p9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("p2") <= t < A("p8"):
        d.update(arms=("hold", "down"), eyes="happy" if A("p6") <= t < A("p8") else "dot")
    if A("p9") <= t:
        d.update(eyes="wide")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    cr.save()
    cr.identity_matrix()
    if A("p3") <= t < A("p4"):
        label(cr, "YES: protein, choline, selenium, B12", 360, 320, size=30)
        cue("pop", t, A("p3"))
    if A("p4") <= t < A("p5"):
        label(cr, "NO vitamin C. NO fiber. Little calcium.", 360, 320, size=30)
        cue("pop", t, A("p4"))
    if A("p5") <= t < A("p6"):
        label(cr, "About 1 egg a day: fine for most people", 360, 320, size=30)
        if A("p5b") <= t:
            label(cr, "High cholesterol? Ask your doctor.", 360, 380, size=30)
    if A("p6") <= t < A("p7"):
        label(cr, "Eggs + fruit + veg + dairy", 360, 320, size=34)
    if A("p8", "twelve") <= t:
        with at(cr, 560, 330, 1.0):
            write(cr, [("12", hexc("#d8363a"))], 0, 0, 64, align="center", bold=True)
            for k in range(6):
                egg(cr, t, -120 + 48 * k, 60, 0.25, face=False)
        cue("hit", t, A("p8", "twelve"))
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_plate(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
