"""Body Facts 11: "Are Eggs Veg? Can 5 Eggs Replace Your Multivitamin?" — a fact-check of a viral reel.

The owner asked for this (scheduled requests from the Interestingly Strange chat). The reel (93 s, Hindi) says:
eggs used to be non-veg because they came from mating; hens laid eggs as a by-product of a "menstrual cycle";
breeding made hens lay one unfertilised egg a day, so eggs are vegetarian; and 3-5 eggs a day work as a
multivitamin. Don't name or mock the creator: "a viral video says...". Sources: research_notes/body_facts_11.md.

What we say:
- Hens ovulate about every 24-26 hours; the yolk is the egg cell (ovum), wrapped in white and shell in the
  oviduct. Hens don't menstruate. Hens lay eggs with or without a rooster; mating only fertilises the egg.
- Layer farms keep no roosters, so their eggs are unfertilised and can never become chicks: TRUE.
- Breeding raised the number (modern layers ~285-300 a year; wild junglefowl only a few clutches, "a handful"),
  it didn't change where the egg comes from.
- Veg or non-veg is a definition, not science: India's FSSAI labelling rules list eggs as non-vegetarian (brown
  symbol). Left to the viewers (the closing question).
- Per large egg (USDA FoodData Central): protein 6.3 g; choline 147 mg (27% DV); selenium 15.4 µg (28%); B12
  0.45 µg (19%); vitamin C 0; fiber 0; calcium 28 mg (2%). Five eggs: choline ~135%, B12 ~95%, calcium ~10%.
- Cholesterol 186 mg; AHA science advisory (Circulation 2020): about one egg a day fits a healthy diet.
- Not used in the script (in the description): potassium is tiny (~1.5% DV per egg); egg vitamin K2 is MK-4,
  not MK-7; most healthy people with a varied diet don't need a multivitamin (NIH ODS).
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.engine import INK, WHITE, at, blob, cue, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import brain
from videos.kidney_donor import eyes, grad_fill, mouth
from videos.tooth_eye import tooth

# Voices: natural stock voices at their own pitch; the doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "egg": dict(voice="am_michael", speed=0.95),
    "ovary": dict(voice="af_bella", speed=0.95),
    "brain": dict(voice="af_heart", speed=0.95),
    "blood": dict(voice="af_sarah", speed=0.95),
    "bone": dict(voice="am_onyx", speed=0.95),
    "gums": dict(voice="af_nova", speed=0.95),
    "gut": dict(voice="am_liam", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"eggs", "vegetarian", "multivitamin", "ovary", "periods", "rooster", "chicks", "choline", "calcium",
            "fiber", "zero", "cholesterol", "non-veg"}

SCRIPT = [
    dict(id="o1", scene="hen", text="A viral video says I'm vegetarian. And a multivitamin!", speaker="egg"),
    dict(id="o2", scene="hen", text="Let's check. I'm the hen's ovary, and every day or so I release a yolk.",
         speaker="ovary"),
    dict(id="o3", scene="hen", text="Wait. So I don't come from a hen's period?", speaker="egg"),
    dict(id="o4", scene="hen", text="No. Hens don't have periods. The yolk is an egg cell, wrapped in white and "
                                    "shell.", speaker="ovary"),
    dict(id="o5", scene="hen", text="And if there's no rooster?", speaker="egg"),
    dict(id="o6", scene="hen", text="Then you're never fertilized. Farm eggs can never become chicks.",
         speaker="ovary"),
    dict(id="o7", scene="hen", text="Hens always laid eggs, rooster or not. Breeding just took them from a handful "
                                    "a year, to about three hundred.", speaker="ovary"),
    dict(id="o8", scene="hen", text="So am I veg, or non-veg?", speaker="egg"),
    dict(id="o9", scene="hen", text="That's a definition, not science. Indian food labels mark eggs as non-veg.",
         speaker="ovary"),
    dict(id="e2", scene="plate", text="Honestly? Five eggs give me more choline than I need in a day.",
         speaker="brain"),
    dict(id="e3", scene="plate", text="And they cover almost all of my vitamin B12.", speaker="blood"),
    dict(id="e4", scene="plate", text="Then where's my calcium? Five eggs barely give me one tenth.", speaker="bone"),
    dict(id="e5", scene="plate", text="I'm still waiting for vitamin C. Eggs have zero.", speaker="gums"),
    dict(id="e6", scene="plate", text="Fiber? Also zero. I'm starving down here.", speaker="gut"),
    dict(id="e7", scene="plate", text="Okay. Maybe I'm not a whole multivitamin.", speaker="egg"),
    dict(id="p1", scene="ward", text="Doctor, so can eggs replace a multivitamin?", speaker="mike"),
    dict(id="p2", scene="ward", text="No. Eggs are a great food, with protein, choline and vitamin B12.",
         speaker="doctor"),
    dict(id="p4", scene="ward", text="But they have no vitamin C, no fiber, and very little calcium.",
         speaker="doctor"),
    dict(id="p5", scene="ward", text="Heart experts say about one egg a day fits a healthy diet.", speaker="doctor"),
    dict(id="p5b", scene="ward", text="Eating more? Ask your doctor, especially if your cholesterol is high.",
         speaker="doctor"),
    dict(id="p7", scene="ward", text="So, are eggs veg or non-veg for you?", speaker="doctor"),
    dict(id="p8", scene="ward", text="Non-veg, bro. I eat twelve a day.", speaker="danny", gap=0.3),
    dict(id="p9", scene="ward", text="Danny. We need to talk.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Are Eggs Veg? Can 5 Eggs Replace Your Multivitamin? 🥚",
    alt_titles=["Eggs Are Vegetarian? Let's Check 🥚", "Can Eggs Replace Your Multivitamin? The Truth 🥚😳"],
    description="""A viral video says eggs are vegetarian, and that 3 to 5 eggs a day work as a multivitamin. We checked. 🥚

TRUE: Store eggs from layer farms are not fertilised (there are no roosters) and can never become chicks.

MISLEADING: Hens don't have periods. A hen ovulates about once a day, and the yolk is the egg cell, wrapped in white and shell. Hens always laid eggs, with or without a rooster: a rooster only fertilises them. Breeding raised the number (a modern laying hen lays about 300 eggs a year; wild junglefowl only a few clutches), not where the egg comes from.

VEG OR NON-VEG? That's a definition, not science. India's food labelling rules (FSSAI) mark eggs as non-vegetarian. People who eat eggs but no meat are often called ovo-vegetarians. You decide. 👇

MULTIVITAMIN? NO. Five large eggs give more than a day's choline and selenium and almost all your vitamin B12, plus great protein. But eggs have zero vitamin C, zero fiber, and very little calcium, magnesium and potassium (about 1-2% of a day's potassium per egg). The vitamin K2 in eggs is mainly MK-4, not MK-7. Calories (about 72), protein (about 6 g), carbs (about 0) and cholesterol (about 186 mg) per egg are right.

Cholesterol: the American Heart Association says about one egg a day fits a healthy diet for most people. If you have high cholesterol, diabetes or heart disease, ask your doctor. And most healthy people with a varied diet don't need a multivitamin at all; some do (pregnancy, vegans for B12, a diagnosed deficiency).

Sources: USDA FoodData Central (egg, whole, large); FSSAI Labelling and Display Regulations (veg/non-veg symbol); Hendrix Genetics and poultry science texts on hen ovulation; American Heart Association science advisory on dietary cholesterol (Circulation, 2020); NIH Office of Dietary Supplements (multivitamin fact sheet); studies on vitamin K2 (MK-4) in eggs.

(Cartoon, real facts. Not medical advice: talk to a doctor about your own health.)

💬 Are eggs veg or non-veg for you? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Eggs", "#VegOrNonVeg", "#Nutrition"],
    tags=["are eggs veg", "eggs veg or non veg", "eggs vs multivitamin", "unfertilized eggs", "egg nutrition",
          "do I need a multivitamin", "choline", "vitamin B12", "eggs and cholesterol", "doctor explains",
          "body facts"],
    pinned_comment="Settle it in the comments: are eggs veg or non-veg? 🥚 (Danny says non-veg… and eats twelve a "
                   "day. 😂) 👇",
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


HEN_BG, HEN_BG_D = hexc("#f7c6c0"), hexc("#eaa79f")
OV = (220, 420)                      # the ovary: a cluster of yolks
EGG_POS = (500, 760)                 # the egg character, at the end of the oviduct
TUBE = [(270, 470), (330, 540), (300, 620), (380, 680), (460, 700)]


def ovary_char(cr, t, mood, talking):
    """The hen's ovary: a bunch of yolks of different sizes, the biggest one with the face."""
    for k, (dx, dy, r) in enumerate([(-80, -60, 34), (-40, -100, 26), (20, -96, 22), (70, -50, 30), (-96, 10, 24),
                                     (80, 20, 20), (-50, 60, 18), (40, 64, 16)]):
        blob(cr, OV[0] + dx, OV[1] + dy, r, r, YOLK, seed=1800 + k, amp=0, lw=3)
    blob(cr, OV[0], OV[1], 70, 66, hexc("#ffb81c"), seed=1810, amp=0, lw=4)
    eyes(cr, OV[0], OV[1] - 10, 0.85, mood)
    mouth(cr, OV[0], OV[1] + 30, 0.75, mood, talking, t)


def cutaway(cr, x, y, s):
    """An egg cut in half: shell, white, yolk."""
    with at(cr, x, y, s):
        pts = [(70 * math.sin(a), -96 * math.cos(a) * (1.0 if math.cos(a) > 0 else 0.8)) for a in
               [2 * math.pi * k / 80 for k in range(80)]]
        shape(cr, pts, hexc("#f3e2c7"), seed=1820, amp=0, lw=4)
        shape(cr, [(x_ * 0.86, y_ * 0.86) for x_, y_ in pts], WHITE, seed=1821, amp=0, lw=0, stroke=None)
        blob(cr, 0, 10, 36, 36, YOLK, seed=1822, amp=0, lw=3)


def nonveg_mark(cr, x, y, s):
    """India's non-vegetarian food symbol: a brown triangle inside a brown square."""
    brown = hexc("#7b3f1c")
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-46, -46, 92, 92, 6, 12), WHITE, stroke=brown, seed=1830, amp=0, lw=7)
        shape(cr, [(0, -26), (26, 22), (-26, 22)], brown, seed=1831, amp=0, lw=0, stroke=None)


def scene_hen(cr, t, tl):
    A = tl.at
    OVC, EGC, WIDE = (1.5, OV[0] + 40, OV[1] + 40), (1.5, EGG_POS[0] - 40, EGG_POS[1] - 40), (1.0, 360, 620)
    keys = [(0, (1.25, 430, 700)), (A("o2"), OVC), (A("o2", "release"), WIDE), (A("o3"), EGC), (A("o4"), WIDE),
            (A("o5"), EGC), (A("o6"), WIDE), (A("o7"), (1.1, 360, 560)), (A("o8"), EGC), (A("o9"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*HEN_BG)
    cr.paint()
    for k in range(9):   # soft tissue folds
        line(cr, [(-300, -200 + 190 * k), (300, -170 + 190 * k), (1100, -210 + 190 * k)], 4, HEN_BG_D,
             seed=1840 + k, amp=0)
    # the oviduct, from the ovary down to the egg
    line(cr, TUBE, 46, hexc("#e58f88"), seed=1845, amp=0)
    line(cr, TUBE, 30, hexc("#f9d3cd"), seed=1846, amp=0)
    om = "calm"
    if A("o4") <= t < A("o5") or A("o9") <= t:
        om = "happy"
    ovary_char(cr, t, om, tl.speaking("ovary", t))
    # a yolk released on "release", travelling down the oviduct and wrapped on the way
    rel = A("o2", "release")
    if rel <= t < A("o5"):
        u = ease_out(seg(t, rel, rel + 1.6))
        i = min(len(TUBE) - 2, int(u * (len(TUBE) - 1)))
        f = u * (len(TUBE) - 1) - i
        x, y = lerp(TUBE[i][0], TUBE[i + 1][0], f), lerp(TUBE[i][1], TUBE[i + 1][1], f)
        blob(cr, x, y, 22, 22, YOLK, seed=1850, amp=0, lw=3)
    em = "happy"
    if A("o3") <= t < A("o4") or A("o5") <= t < A("o6") or A("o8") <= t < A("o9"):
        em = "worried"
    if A("o6") <= t < A("o7"):
        em = "shock"
    egg(cr, t, EGG_POS[0], EGG_POS[1], 1.1, em, tl.speaking("egg", t))
    # what an egg is (o4)
    if A("o4", "yolk") <= t < A("o5"):
        cutaway(cr, 170, 760, 1.0)
        label(cr, "Yolk = the egg cell", 170, 610, 170, 740, size=26)
        label(cr, "White", 60, 880, 120, 820, size=24)
        label(cr, "Shell", 280, 900, 225, 840, size=24)
        cue("pop", t, A("o4", "yolk"))
    if A("o3", "period") <= t < A("o4", "yolk"):
        label(cr, "Hens don't have periods. They ovulate.", 360, 300, size=28)
    if A("o6") <= t < A("o7"):
        label(cr, "No rooster = not fertilized = can't become a chick", 360, 300, size=26)
        cue("pop", t, A("o6"))
    if A("o7", "breeding") <= t < A("o8"):
        label(cr, "Wild hen: a handful of eggs a year", 360, 300, size=28)
        if A("o7", "three") <= t:
            label(cr, "Farm hen: about 300 a year", 360, 360, size=28)
            cue("pop", t, A("o7", "three"))
    if A("o9", "non-veg") - 0.2 <= t:
        nonveg_mark(cr, 560, 470, 1.0)
        label(cr, "India: eggs get the non-veg mark", 400, 340, size=28)
        cue("pop", t, A("o9", "non-veg") - 0.2)
    label(cr, "Hen's ovary", OV[0], OV[1] - 170, OV[0], OV[1] - 120, size=26) if t < A("o3") else None
    for w in (A("o1", "vegetarian"), A("o1", "multivitamin"), A("o3", "period")):
        cue("hit", t, w)


def scene_plate(cr, t, tl):
    A = tl.at
    rows_at = [A(r[3]) for r in ROWS]
    TOP = (1.35, 360, 330)
    keys = [(0, TOP)]
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
    for w in (A("e5", "zero"), A("e6", "zero")):
        cue("hit", t, w)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("p1") - 0.1, A_CLOSE), (A("p1", "multivitamin"), TWO_SHOT),
            (A("p2"), DOC_CLOSE), (A("p4"), TWO_SHOT), (A("p5"), DOC_CLOSE), (A("p5b"), TWO_SHOT),
            (A("p7"), DOC_CLOSE), (A("p8"), B_CLOSE), (A("p9"), NEXT_BED)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    m = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("p4") <= t < A("p7"):
        m.update(eyes="wide", mouth="o")
    if A("p7") <= t:
        m.update(eyes="happy", mouth="grin")
    if A("p8") <= t:
        m.update(eyes="wide", mouth="o")
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("p8") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("p9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("p2") <= t < A("p8"):
        d.update(arms=("hold", "down"), eyes="happy" if A("p7") <= t < A("p8") else "dot")
    if A("p9") <= t:
        d.update(eyes="wide")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    cr.save()
    cr.identity_matrix()
    if A("p2", "great") <= t < A("p4"):
        label(cr, "YES: protein, choline, B12", 360, 320, size=32)
        cue("pop", t, A("p2", "great"))
    if A("p4") <= t < A("p5"):
        label(cr, "NO vitamin C. NO fiber. Little calcium.", 360, 320, size=30)
        cue("pop", t, A("p4"))
    if A("p5") <= t < A("p7"):
        label(cr, "About 1 egg a day: fine for most people", 360, 320, size=30)
        if A("p5b") <= t:
            label(cr, "High cholesterol? Ask your doctor.", 360, 380, size=30)
    if A("p7", "veg") <= t < A("p8"):
        label(cr, "Veg or non-veg? Comment below", 360, 320, size=32)
        cue("pop", t, A("p7", "veg"))
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
    elif name == "hen":
        scene_hen(cr, t, tl)
    else:
        scene_plate(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
