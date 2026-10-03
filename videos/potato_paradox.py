"""Paradox: "The Potato Paradox" — 100 lb of potatoes, 99% water; dried to 98% water, they weigh 50 lb.

Math: the non-water part is 1% of 100 lb = 1 lb. Drying removes only water, so 1 lb stays; if 1 lb is 2% of the
total, the total is 50 lb. Same structure as The Infinite Hotel: impossible premise, a character's guess, the
step-by-step logic with a picture (a 100-square grid), the name, an open question.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="q1", scene="kitchen", text="You have [a hundred pounds|100 lb] of potatoes. "
                                        "[Ninety-nine percent|99%] of that weight is water."),
    dict(id="q2", scene="kitchen", text="You leave them out to dry, until they're [ninety-eight percent|98%] water. "
                                        "Just one percent less water."),
    dict(id="q3", scene="kitchen", text="How much do they weigh now? Easy. [Ninety-eight pounds.|98 lb.]",
         speaker="farmer", speaker_from="easy."),
    dict(id="q4", scene="kitchen", text="Nope. Only [fifty pounds.|50 lb.]", pace=0.9, gap=0.3),
    dict(id="q5", scene="grid", text="Here's why. Split the [hundred pounds|100 lb] into [a hundred|100] blocks. "
                                     "Each block is one pound."),
    dict(id="q6", scene="grid", text="[Ninety-nine|99] blocks are water. Just one block is potato."),
    dict(id="q7", scene="grid", text="Drying removes only water. So the potato block stays."),
    dict(id="q8", scene="grid", text="But now the pile is [ninety-eight percent|98%] water. So that one potato block "
                                     "must be [two percent|2%] of the pile."),
    dict(id="q9", scene="grid", text="One out of fifty is two percent. So only fifty blocks are left. "
                                     "[Fifty pounds.|50 lb.]"),
    dict(id="q10", scene="name", text="It's called the potato paradox. One percent less water sounds tiny. But it cut "
                                      "the weight in half."),
    dict(id="q11", scene="end", text="So... did you guess [ninety-eight?|98?]", pace=0.95),
]

METADATA = dict(
    title="100 lb of Potatoes Lose 1% Water… and Weigh 50 lb?! 🥔🤯",
    alt_titles=["The Potato Paradox: Your Brain Will Refuse This 🥔", "Half the Weight Disappears… From 1% Water? 🤯"],
    description="""You have 100 pounds of potatoes that are 99% water. You dry them until they're 98% water. How much do they weigh now? 🥔

Not 98. FIFTY. 🤯

The part that isn't water is 1%: that's 1 pound. Drying only removes water, so that pound stays… but now it has to be 2% of the pile. If 1 pound is 2%, the whole pile is 50 pounds.

It's called the potato paradox. The math is easy; your brain just refuses to believe it.

💬 Be honest: did you guess 98? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Math", "#MindBlown"],
    tags=["potato paradox", "math paradox", "paradox", "percentages", "brain teaser", "math trick", "mind blowing math",
          "puzzle", "math shorts", "interestingly strange"],
    pinned_comment="Be honest: what was your first guess? 98? 99? 🥔👇",
)

POTATO, POTATO_D = hexc("#c9955a"), hexc("#8e6234")
WATER = hexc("#4fb3e8")
BLUE = hexc("#3f6fb5")
GREEN = hexc("#2e9e52")
WALL = hexc("#f6e3c2")


def potato(cr, x, y, s, seed, shrink=0.0):
    with at(cr, x, y, s * (1 - 0.35 * shrink)):
        blob(cr, 0, 0, 34, 24, POTATO, seed=seed, amp=1.2, lw=3.5)
        for k in range(3):
            dot(cr, -14 + k * 13, -4 + (k % 2) * 8, 2.5, POTATO_D)
        if shrink > 0.3:   # wrinkles
            line(cr, [(-18, 4), (-6, 0), (6, 6), (18, 0)], 2.5, POTATO_D, seed=seed + 1, amp=0.4)


def pile(cr, t, x, y, s, shrink=0.0):
    k = 0
    for r in range(4):
        for c in range(6 - r):
            potato(cr, x - (5 - r) * 32 + c * 64, y - r * 40, s, 3000 + k * 3, shrink)
            k += 1


def scale(cr, t, x, y, value, s=1.0):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-210, 0, 420, 130, 20, 16), hexc("#d9dde3"), seed=3100, amp=0.4, lw=4.5)
        shape(cr, rrect_pts(-110, 30, 220, 70, 12, 12), hexc("#1f2a4d"), seed=3101, amp=0.3, lw=3.5)
        write(cr, [(f"{value:.0f} lb", hexc("#6fffa0"))], 0, 82, 50, align="center", bold=True)
        shape(cr, rrect_pts(-240, -14, 480, 18, 8, 10), hexc("#b9bec7"), seed=3102, amp=0.3, lw=3.5)


def kitchen(cr):
    cr.set_source_rgba(*WALL)
    cr.rectangle(-900, -900, 2600, 3200)
    cr.fill()
    for k in range(-8, 20):   # tiles
        line(cr, [(-200 + k * 80, 300), (-200 + k * 80, 940)], 2, hexc("#e8d0a8"), seed=3200 + k, amp=0.3)
        line(cr, [(-400, 300 + k * 80), (1200, 300 + k * 80)], 2, hexc("#e8d0a8"), seed=3230 + k, amp=0.3)
    sharp_shape(cr, [(-900, 940), (1700, 935), (1700, 2200), (-900, 2200)], hexc("#a8774a"), seed=3260, amp=0.6, lw=4)


def scene_kitchen(cr, t, tl):
    A = tl.at
    dry = ease_out(seg(t, A("q2", "dry,"), A("q2", "water.", end=True)))
    weight = 100.0
    if t >= A("q4", "50"):
        weight = lerp(100, 50, ease_out(seg(t, A("q4", "50"), A("q4", "50") + 0.6)))
    keys = [(0, (1.5, 360, 720)), (A("q1", "100"), (1.8, 360, 900)), (A("q1", "potatoes."), (1.2, 360, 780)),
            (A("q1", "99%"), (1.6, 360, 520)), (A("q2"), (1.0, 360, 720)), (A("q2", "dry,"), (1.4, 560, 500)),
            (A("q2", "98%"), (1.6, 360, 520)), (A("q2", "just"), (1.2, 360, 700)),
            (A("q3"), (1.0, 360, 760)), (A("q3", "easy."), (2.0, 150, 740)), (A("q3", "98"), (1.6, 300, 760)),
            (A("q4"), (1.3, 360, 900)), (A("q4", "50"), (1.6, 360, 1010))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    if A("q2", "dry,") <= t:   # the sun drying them
        blob(cr, 600, 420, 60, 60, hexc("#ffd23f"), seed=3300, amp=0.4, lw=3.5)
        for k in range(8):
            a = k * math.pi / 4 + t * 0.6
            line(cr, [(600 + 76 * math.cos(a), 420 + 76 * math.sin(a)), (600 + 100 * math.cos(a), 420 + 100 * math.sin(a))],
                 5, hexc("#f2b632"), seed=3301 + k, amp=0.2)
        for k in range(4):   # steam
            u = (t * 0.8 + k / 4) % 1
            line(cr, [(250 + k * 60, 820 - u * 120), (262 + k * 60, 800 - u * 120), (250 + k * 60, 780 - u * 120)], 4,
                 hexc("#ffffff", 1 - u), seed=3310 + k, amp=0.3)
    scale(cr, t, 360, 940, weight, 1.1)
    pile(cr, t, 360, 915, 1.25, dry)
    # the percentage tag
    if A("q1", "99%") <= t < A("q4"):
        pct = "99% water" if t < A("q2", "98%") else "98% water"
        with at(cr, 360, 520, max(0.85, pop(t, A("q1", "99%"), 0.25)), rot=-0.03):
            shape(cr, rrect_pts(-190, -50, 380, 100, 20, 14), WATER, seed=3320, amp=0.4, lw=4)
            write(cr, [(pct, WHITE)], 0, 18, 54, align="center", bold=True)
    person(cr, "farmer", 120, 1240, t, facing=1, arms=("thumb", "hip") if A("q3", "easy.") <= t < A("q4") else ("hip", "hip"),
           eyes="wide" if t >= A("q4", "50") else "happy", mouth="o" if t >= A("q4", "50") else "grin",
           sweat=t >= A("q4", "50"), scale=1.1)
    if tl.speaking("farmer", t):
        pass
    hl(cr, t, [("100 lb", RED), (" of potatoes", INK)], 215, 66, 0.0, end=A("q1", "99%") - 0.05, bold=True, sound=False)
    hl(cr, t, [("dried to ", INK), ("98%", BLUE), (" water", INK)], 215, 66, A("q2", "98%"), end=A("q3") - 0.05, bold=True)
    hl(cr, t, [("how much now?", INK)], 215, 70, A("q3"), end=A("q3", "98") - 0.05, bold=True)
    hl(cr, t, [("\"", INK), ("98 lb", BLUE), ("\"", INK)], 215, 80, A("q3", "98"), end=A("q4") - 0.05, bold=True)
    stamp(cr, t, A("q4", "50"), "50 LB?!", dur=0.7, y=330)
    cue("hit", t, A("q4", "50"))


CELL, GX, GY = 46, 360 - 230, 290     # 10 x 10 blocks, 460 px square


def grid(cr, t, n, water_col, potato_t=None, appear=None):
    """n blocks, 10 per row. The last block is potato once `potato_t` has passed; the rest are water."""
    for k in range(n):
        r, c = divmod(k, 10)
        sc = 1.0 if appear is None else max(0.0, min(1.0, (t - appear - k * 0.006) / 0.15))
        if sc <= 0:
            continue
        x, y = GX + c * CELL, GY + r * CELL
        col = POTATO if (potato_t is not None and t >= potato_t and k == n - 1) else water_col
        with at(cr, x + CELL / 2, y + CELL / 2, sc):
            shape(cr, rrect_pts(-CELL / 2 + 3, -CELL / 2 + 3, CELL - 6, CELL - 6, 5, 8), col, seed=3400 + k, amp=0.3,
                  lw=2.5)


def scene_grid(cr, t, tl):
    A = tl.at
    keys = [(A("q5") - 0.2, (1.0, 360, 780)), (A("q6", "potato."), (1.08, 400, 760)), (A("q7"), (1.0, 360, 780)),
            (A("q7", "stays."), (1.08, 400, 760)), (A("q8"), (1.0, 360, 780)), (A("q9", "fifty"), (1.0, 360, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    shrink = ease_out(seg(t, A("q9", "left."), A("q9", "left.") + 1.0))
    n = int(round(lerp(100, 50, shrink)))
    water_col = WATER if t >= A("q6") else hexc("#d9c7a3")      # plain blocks until we say what they are
    grid(cr, t, n, water_col, potato_t=A("q6", "potato."), appear=A("q5", "blocks.") - 0.1)
    if t >= A("q6", "potato."):          # circle the potato block
        r, c = divmod(n - 1, 10)
        cx, cy = GX + c * CELL + CELL / 2, GY + r * CELL + CELL / 2
        blob(cr, cx, cy, 30, 30, None, seed=3500, amp=0.6, lw=5, stroke=RED)
    # the running explanation under the grid (clear of the captions)
    lines = []
    if t >= A("q5", "each"):
        lines = [[("1 block = 1 lb", WHITE)]]
    if t >= A("q6"):
        lines = [[("99 water", hexc("#9fe0ff")), (" + ", WHITE), ("1 potato", hexc("#f2c28a")), (" = 100 lb", WHITE)]]
    if t >= A("q7", "stays."):
        lines = [[("1 potato", hexc("#f2c28a")), (" STAYS", hexc("#ff8a80"))]]
    if t >= A("q8", "2%"):
        lines = [[("1 potato", hexc("#f2c28a")), (" must be ", WHITE), ("2%", hexc("#ff8a80"))]]
    if t >= A("q9"):
        lines = [[("1 out of 50", WHITE), (" = 2%", hexc("#ff8a80"))]]
    if t >= A("q9", "left."):
        lines = [[(f"{n - 1} water", hexc("#9fe0ff")), (" + ", WHITE), ("1 potato", hexc("#f2c28a")),
                  (f" = {n} lb", WHITE)]]
    for k, runs in enumerate(lines):
        shape(cr, rrect_pts(30, 766 + k * 64, 660, 64, 24, 12), hexc("#2b2d3a", 0.85), seed=3510, amp=0.2, lw=0,
              stroke=None)
        write(cr, runs, 360, 812 + k * 64, 46, align="center", bold=True)
    hl(cr, t, [("100 blocks = ", INK), ("100 lb", RED)], 215, 62, A("q5"), end=A("q6") - 0.05, bold=True)
    hl(cr, t, [("only ", INK), ("ONE", RED), (" is potato", INK)], 215, 66, A("q6", "just"), end=A("q7") - 0.05,
       bold=True)
    hl(cr, t, [("drying takes ", INK), ("only water", BLUE)], 215, 62, A("q7"), end=A("q8") - 0.05, bold=True)
    hl(cr, t, [("98%", BLUE), (" water, so potato = ", INK), ("2%", RED)], 215, 48, A("q8"), end=A("q9", "left.") - 0.05,
       bold=True)
    hl(cr, t, [("only ", INK), ("50 LB", RED), (" left!", INK)], 215, 76, A("q9", "left."), bold=True, underline=True)
    for k in range(0, 50, 5):
        cue("pop", t, A("q9", "left.") + k * 0.02)
    stamp(cr, t, A("q9", "50lb."), "HALF!", dur=0.7, y=640)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("q10") - 0.2, (1.1, 360, 680)), (A("q10", "potato"), (1.4, 360, 560)), (A("q10", "percent"), (1.0, 360, 700)),
            (A("q10", "cut"), (1.1, 360, 680))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    with at(cr, 360, 540, max(0.85, pop(t, A("q10", "potato"), 0.3)) if t < A("q10", "percent") else 1e-3,
            rot=-0.03):
        shape(cr, rrect_pts(-250, -90, 500, 180, 18, 14), hexc("#fdf6e3"), seed=3600, amp=0.5, lw=5)
        write(cr, [("THE POTATO", INK)], 0, -14, 58, align="center", bold=True)
        write(cr, [("PARADOX", RED)], 0, 56, 66, align="center", bold=True)
    pile(cr, t, 360, 960, 1.0, 1.0)
    if t >= A("q10", "percent"):     # 1% vs half, side by side
        for k, (big, small, col, x, st) in enumerate((("-1%", "water", BLUE, 200, A("q10", "percent")),
                                                     ("-50%", "weight", RED, 520, A("q10", "cut")))):
            if t >= st:
                with at(cr, x - 10 * k, 560, max(0.85, pop(t, st, 0.25)) * (1.0 if k == 0 else 1.2)):
                    shape(cr, rrect_pts(-130, -90, 260, 180, 20, 12), hexc("#fdf6e3"), seed=3620 + k, amp=0.4, lw=5)
                    write(cr, [(big, col)], 0, 10, 72, align="center", bold=True)
                    write(cr, [(small, INK)], 0, 66, 38, align="center", bold=True)
    hl(cr, t, [("1% less water: ", INK), ("tiny", GREEN)], 215, 62, A("q10", "percent"), end=A("q10", "cut") - 0.05,
       bold=True)
    hl(cr, t, [("...but ", INK), ("HALF", RED), (" the weight", INK)], 215, 66, A("q10", "cut"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("q11") - 0.2, (1.2, 360, 760)), (A("q11", "guess"), (1.7, 360, 880)), (A("q11", "98?"), (1.2, 360, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    scale(cr, t, 360, 940, 50, 1.1)
    pile(cr, t, 360, 915, 1.25, 1.0)
    person(cr, "farmer", 120, 1240, t, facing=1, arms=("chin", "hip"), eyes="wide", mouth="o", scale=1.1)
    hl(cr, t, [("did you guess ", INK), ("98", RED), ("?", INK)], 215, 70, A("q11"), bold=True, underline=True)
    stamp(cr, t, A("q11", "98?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"kitchen": scene_kitchen, "grid": scene_grid, "name": scene_name, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
