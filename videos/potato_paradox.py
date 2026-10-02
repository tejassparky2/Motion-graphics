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
    dict(id="q1", scene="kitchen", text="You have [a hundred pounds|100 lb] of potatoes. They're [ninety-nine percent|99%] "
                                        "water."),
    dict(id="q2", scene="kitchen", text="You leave them in the sun, until they're [ninety-eight percent|98%] water. "
                                        "Just one percent less."),
    dict(id="q3", scene="kitchen", text="How much do they weigh now? Easy. [Ninety-eight pounds.|98 lb.]",
         speaker="farmer", speaker_from="easy."),
    dict(id="q4", scene="kitchen", text="Nope. [Fifty.|50 lb.]", pace=0.9, gap=0.3),
    dict(id="q5", scene="grid", text="Here's why. The part that isn't water is [one percent.|1%.] That's [one pound.|1 lb.]"),
    dict(id="q6", scene="grid", text="Drying only takes out water. So that pound stays. But now, it has to be "
                                     "[two percent|2%] of the pile."),
    dict(id="q7", scene="grid", text="If one pound is [two percent,|2%,] the whole pile is [fifty pounds.|50 lb.] "
                                     "Half the weight, gone."),
    dict(id="q8", scene="name", text="It's called the potato paradox. The math is easy. Your brain just refuses to "
                                     "believe it."),
    dict(id="q9", scene="end", text="So... did you guess [ninety-eight?|98?]", pace=0.95),
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
    dry = ease_out(seg(t, A("q2", "sun,"), A("q2", "water.", end=True)))
    weight = 100.0
    if t >= A("q4", "50"):
        weight = lerp(100, 50, ease_out(seg(t, A("q4", "50"), A("q4", "50") + 0.6)))
    keys = [(0, (1.5, 360, 720)), (A("q1", "100"), (1.8, 360, 900)), (A("q1", "potatoes."), (1.2, 360, 780)),
            (A("q1", "99%"), (1.6, 360, 520)), (A("q2"), (1.0, 360, 720)), (A("q2", "sun,"), (1.4, 560, 500)),
            (A("q2", "98%"), (1.6, 360, 520)), (A("q2", "just"), (1.2, 360, 700)),
            (A("q3"), (1.0, 360, 760)), (A("q3", "easy."), (2.0, 150, 740)), (A("q3", "98"), (1.6, 300, 760)),
            (A("q4"), (1.3, 360, 900)), (A("q4", "50"), (2.0, 360, 950))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    if A("q2", "sun,") <= t:   # the sun drying them
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
    if t >= A("q1", "99%"):
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


def grid(cr, t, x0, y0, n, solid, cell=52, appear=None):
    """n squares, 10 per row; `solid` of them are the potato part (brown), the rest water (blue)."""
    for k in range(n):
        r, c = divmod(k, 10)
        sc = 1.0 if appear is None else max(0.0, min(1.0, (t - appear - k * 0.008) / 0.15))
        if sc <= 0:
            continue
        x, y = x0 + c * cell, y0 + r * cell
        col = POTATO if k >= n - solid else WATER
        with at(cr, x + cell / 2, y + cell / 2, sc):
            shape(cr, rrect_pts(-cell / 2 + 3, -cell / 2 + 3, cell - 6, cell - 6, 6, 8), col, seed=3400 + k, amp=0.3,
                  lw=2.5)


def scene_grid(cr, t, tl):
    A = tl.at
    x0 = 360 - 260
    keys = [(A("q5") - 0.2, (1.0, 360, 700)), (A("q5", "isn't"), (1.4, 360, 820)), (A("q5", "1%."), (2.0, 600, 880)),
            (A("q5", "1lb"), (1.4, 520, 820)), (A("q6"), (1.0, 360, 700)), (A("q6", "stays."), (1.8, 600, 840)),
            (A("q6", "2%"), (1.2, 360, 700)), (A("q7"), (1.0, 360, 700)), (A("q7", "50"), (1.3, 360, 640)),
            (A("q7", "half"), (1.0, 360, 700))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    shrink = ease_out(seg(t, A("q6", "pile."), A("q7", "50") + 0.2))
    n = int(round(lerp(100, 50, shrink)))
    grid(cr, t, x0, 380, n, 1, appear=A("q5") - 0.1)
    if t >= A("q5", "isn't"):
        last = n - 1
        r, c = divmod(last, 10)
        cx, cy = x0 + c * 52 + 26, 380 + r * 52 + 26
        blob(cr, cx, cy, 36, 36, None, seed=3500, amp=0.6, lw=5, stroke=RED)
        write(cr, [("1 lb", RED)], cx - 60 if c > 6 else cx + 60, cy + 12, 36, align="center", bold=True)
    label = "100 squares = 100 lb" if t < A("q6", "pile.") else f"{n} squares = {n} lb"
    write(cr, [(label, WHITE)], 360, 1000, 44, align="center", bold=True)
    if t >= A("q6", "2%"):
        write(cr, [("1 out of 50 = ", WHITE), ("2%", hexc("#9fe0ff"))], 360, 1060, 42, align="center", bold=True)
    hl(cr, t, [("only ", INK), ("1 lb", RED), (" isn't water", INK)], 215, 62, A("q5", "isn't"),
       end=A("q6") - 0.05, bold=True)
    hl(cr, t, [("that pound ", INK), ("STAYS", RED)], 215, 70, A("q6", "stays."), end=A("q7") - 0.05, bold=True)
    hl(cr, t, [("HALF", RED), (" the weight, gone", INK)], 215, 64, A("q7", "half"), bold=True)
    for k in range(0, 50, 5):
        cue("pop", t, A("q6", "pile.") + k * 0.02)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("q8") - 0.2, (1.1, 360, 680)), (A("q8", "potato"), (1.4, 360, 560)), (A("q8", "math"), (1.0, 360, 700)),
            (A("q8", "brain"), (1.25, 360, 680))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    with at(cr, 360, 540, max(0.85, pop(t, A("q8", "potato"), 0.3)) if t < A("q8", "brain") else 1e-3, rot=-0.03):
        shape(cr, rrect_pts(-250, -90, 500, 180, 18, 14), hexc("#fdf6e3"), seed=3600, amp=0.5, lw=5)
        write(cr, [("THE POTATO", INK)], 0, -14, 58, align="center", bold=True)
        write(cr, [("PARADOX", RED)], 0, 56, 66, align="center", bold=True)
    pile(cr, t, 360, 960, 1.0, 1.0)
    if t >= A("q8", "brain"):   # a confused brain
        with at(cr, 360, 560, max(0.85, pop(t, A("q8", "brain"), 0.25)) * 1.4):
            blob(cr, 0, 0, 90, 64, hexc("#f5a3b5"), seed=3610, amp=1.0, lw=4)
            for k in range(3):
                line(cr, [(-60 + k * 40, -40), (-40 + k * 40, 0), (-60 + k * 40, 40)], 4, hexc("#c9607a"),
                     seed=3611 + k, amp=0.6)
            write(cr, [("NOPE.", RED)], 0, -84, 44, align="center", bold=True)
    hl(cr, t, [("the math is ", INK), ("EASY", GREEN)], 215, 66, A("q8", "math"), end=A("q8", "brain") - 0.05,
       bold=True)
    hl(cr, t, [("your brain ", INK), ("REFUSES", RED)], 215, 66, A("q8", "brain"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("q9") - 0.2, (1.2, 360, 760)), (A("q9", "guess"), (1.7, 360, 880)), (A("q9", "98?"), (1.2, 360, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    kitchen(cr)
    scale(cr, t, 360, 940, 50, 1.1)
    pile(cr, t, 360, 915, 1.25, 1.0)
    person(cr, "farmer", 120, 1240, t, facing=1, arms=("chin", "hip"), eyes="wide", mouth="o", scale=1.1)
    hl(cr, t, [("did you guess ", INK), ("98", RED), ("?", INK)], 215, 70, A("q9"), bold=True, underline=True)
    stamp(cr, t, A("q9", "98?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"kitchen": scene_kitchen, "grid": scene_grid, "name": scene_name, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
