"""The heap (sorites) paradox, opened by the Last Bencher asking a bald teacher -- logic trap, polished look.

The sorites paradox is credited to Eubulides of Miletus (4th century BC): one grain isn't a heap, adding one grain never
turns a non-heap into a heap, so a million grains isn't a heap either. Everyday versions: baldness, becoming an
adult. The "one exact grain we can't know" view is Timothy Williamson's epistemicism.
Script approved by the owner on 13 Oct 2026 (out/scripts_batch_47-50.md doc, with the "Hook fix" first line).
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, calendar, card, check, red_x, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, put, rad,
                           rrect, shade, sign, smooth, soft_disc, sprite, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person, portrait
from videos.last_bencher_4 import classroom, room

NARRATOR = dict(speed=0.88)
TAIL = 0.9
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5)})

SCRIPT = [
    dict(id="h1", scene="ask", text="Sir, how many hairs do you have to lose, to be bald?", speaker="kid"),
    dict(id="h2", scene="hair", text="You are not bald.", gap=0.35),
    dict(id="h3", scene="hair", text="Lose one hair. Still not bald."),
    dict(id="h4", scene="hair", text="So which hair made you bald?"),
    dict(id="h5", scene="eubulides", text="This puzzle is over [two thousand three hundred|2,300] years old. A Greek "
                                          "thinker named Eubulides asked it with sand.", gap=0.3),
    dict(id="h6", scene="grains", text="One grain of sand is not a heap."),
    dict(id="h7", scene="grains", text="Add one grain. Still not a heap."),
    dict(id="h8", scene="grains", text="And one grain can never turn a not-heap into a heap."),
    dict(id="h9", scene="million", text="So, by that rule, a million grains is not a heap either."),
    dict(id="h10", scene="million", text="But that's obviously a heap."),
    dict(id="h11", scene="adult", text="It's everywhere. When do you become an adult?", gap=0.3),
    dict(id="h12", scene="adult", text="At midnight on your eighteenth birthday? So one second earlier, you're a kid?"),
    dict(id="h13", scene="law", text="The law needs a line, so it draws one. Nature doesn't."),
    dict(id="h14", scene="views", text="Some thinkers say words like heap are just fuzzy. Others say there is one exact "
                                       "grain, we just can't know which."),
    dict(id="h15", scene="end", text="So, which grain makes it a heap? Tell me your number.", gap=0.3, pace=0.95),
]
clear_dialogue(SCRIPT, ids=["h1"], pace=0.95)

METADATA = dict(
    title="Lose 1 Hair. Not Bald. Then When? 🧑‍🦲",
    alt_titles=["1 Grain Isn't a Heap. So Heaps Don't Exist?", "Which Grain of Sand Makes a Heap? Tell Me ⏳",
                "The Last Bencher Asked a Bald Teacher… 😳"],
    description="""When exactly do you go bald? The heap (sorites) paradox in 45 seconds: one grain, one hair, one second. ⏳

"Sir, how many hairs do you have to lose, to be bald?"
You are not bald. Lose one hair: still not bald. So which hair made you bald?
Over 2,300 years ago, Eubulides asked it with sand: one grain of sand is not a heap. Add one grain: still not a heap. And one grain can never turn a not-heap into a heap. So, by that rule, a million grains is not a heap either. But that's obviously a heap.
It's everywhere: when do you become an adult? At midnight on your 18th birthday? One second earlier, you're a kid? The law needs a line, so it draws one. Nature doesn't.
Some thinkers say words like "heap" are just fuzzy; others say there is one exact grain, we just can't know which.

Source: the sorites paradox, credited to Eubulides of Miletus (4th century BC).

💬 So, which grain makes it a heap? Tell me your number 👇

🔔 Interestingly Strange: The Last Bencher, mind-bending paradoxes, weird history and strange stories, animated.""",
    hashtags=["#Paradox", "#TheLastBencher", "#Shorts"],
    tags=["sorites paradox", "heap paradox", "bald paradox", "paradox explained", "logic puzzle", "philosophy",
          "eubulides", "vagueness", "the last bencher", "interestingly strange"],
    pinned_comment="Pick a number: how many grains make a heap? ⏳ Closest to the crowd's average gets pinned 👇",
)

SAND = hexc("#e8c070")


# ---------------------------------------------------------------- props
def grain(cr, x, y, r=7):
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, SAND, OUTLINE, 2.5)


def heap(cr, x, y, w, h, seed=3):
    """A sand heap with its base centred at (x, y)."""
    if w <= 1 or h <= 1:
        return
    smooth(cr, [(x - w / 2, y), (x - w * 0.28, y - h * 0.55), (x, y - h), (x + w * 0.28, y - h * 0.55), (x + w / 2, y)])
    paint(cr, lin(0, y - h, 0, y, [(0, shade(SAND, 0.2)), (1, shade(SAND, -0.2))]), OUTLINE, 5)
    rng = random.Random(seed)
    for _ in range(int(w * h / 900)):
        u, v = rng.random(), rng.random()
        yy = y - v * h * 0.95
        half = (w / 2) * (1 - v) * 0.9
        cr.arc(x + (u * 2 - 1) * half, yy, 2.2, 0, 2 * math.pi)
        cr.set_source_rgba(0.55, 0.38, 0.15, 0.45)
        cr.fill()


def table(cr, y=760):
    rrect(cr, 40, y, W - 80, 40, 10)
    paint(cr, lin(0, y, 0, y + 40, [(0, hexc("#b9824a")), (1, hexc("#8a5a2e"))]), OUTLINE, 5)


def hair_style(n):
    """Hair thins out as the count falls."""
    if n > 80000:
        return "curly"
    if n > 40000:
        return "short"
    if n > 8000:
        return "tonsure"
    return "bald"


def bald_sir(cr, t, x, y, s, **kw):
    person(cr, t, x, y, s, "sir", hair="bald", hair_col=hexc("#2b2b33"), **kw)


# ---------------------------------------------------------------- scenes
def scene_ask(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    talk = tl.speaking("kid", t)
    cr.save()
    enter(cr, camera(t, [(0, (1.9, 560, 460)), (A("h1", "bald?"), (1.0, 360, 640))], dur=0.7))
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth="talk" if talk else "grin",
                                       brows="raise"),
              look_at=(560, 0) if t >= A("h1", "bald?") else None, gasp=t >= A("h1", "bald?"))
    cr.restore()
    if t >= A("h1", "bald?"):
        bald_sir(cr, t, 150, 1120, 1.05, eyes="wide", mouth="o", brows="up", arms=("face", "down"), sweat=True)
        sparkles(cr, t, A("h1", "bald?"), 150, 700, n=6, seed=2, col=WHITE, spread=80)    # head shine
        cue("hit", t, A("h1", "bald?"))
    sign(cr, t, -0.5, 360, 120, "HOW MANY HAIRS?", col=GOLD, size=62)
    vignette(cr, 0.4)


def scene_hair(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe6ff"), hexc("#fff1d6"), seed=2)
    n = 100000
    if t >= A("h3", "Lose"):
        n = 99999
    spin0 = A("h4", "which")
    if t >= spin0:
        n = int(lerp(99999, 0, ease_out(seg(t, spin0, A("h4", end=True) + 0.3))))
    person(cr, t, 360, 920, 1.0, "fermi", hair=hair_style(n), eyes="wide" if t >= spin0 else "happy",
           mouth="o" if t >= spin0 else "smile", brows="up" if t >= spin0 else None, sweat=t >= spin0,
           arms=("face", "face") if t >= spin0 else ("hips", "hips"))
    if A("h3", "Lose") <= t < spin0:          # one hair floats away
        u = seg(t, A("h3", "Lose"), A("h3", "Lose") + 1.4)
        x, y = 360 + 160 * u, 420 - 80 * u + 20 * math.sin(u * 9)
        stroke_line(cr, [(x, y), (x + 14, y - 10), (x + 6, y - 26)], 3.5, hexc("#2b1a12"))
    bold_text(cr, f"HAIRS: {n:,}", 360, 260, 64, WHITE)
    tag(cr, t, A("h2"), 360, 130, "YOU", col=BLUE, size=50, end=A("h4") - 0.05)
    if A("h3", "Still") <= t < spin0:
        check(cr, t, A("h3", "Still"), 560, 420, 44)
        sign(cr, t, A("h3", "Still"), 360, 780, "STILL NOT BALD", col=GREEN, size=50)
    if t >= spin0:
        bold_text(cr, "?", 600, 420 + math.sin(t * 5) * 8, 160 * appear(t, spin0, 0.3), GOLD)
        sign(cr, t, spin0, 360, 130, "WHICH HAIR?", col=PURPLE, size=64)
    vignette(cr, 0.35)


def scene_eubulides(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e4c0"), hexc("#d8b878"), seed=6)
    person(cr, t, 250, 950, 1.0, "zeno", eyes="half", mouth="smile", arms=("out", "down"), brows="raise")
    sand = A("h5", "sand.")
    if t >= sand:                       # sand pours from his hand
        for k in range(14):
            ph = (t * 1.6 + k / 14) % 1
            grain(cr, 400 + math.sin(k) * 10, 560 + ph * 300, 5)
        heap(cr, 410, 900, 220 * min(1, (t - sand) / 2.5), 110 * min(1, (t - sand) / 2.5))
    tag(cr, t, A("h5", "Eubulides"), 360, 140, "EUBULIDES, ~350 BC", col=GOLD, size=44)
    sign(cr, t, A("h5", "2,300"), 360, 280, "2,300 YEARS OLD", col=PURPLE, size=52, rot=0.03,
         end=A("h5", "Eubulides") - 0.05)
    vignette(cr, 0.35)


def scene_grains(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#fff1d6"), hexc("#f4d8a8"), seed=3)
    table(cr)
    grain(cr, 330, 738, 22)
    if t >= A("h7", "Add"):
        u = ease_out(seg(t, A("h7", "Add"), A("h7", "Add") + 0.4))
        grain(cr, 390, lerp(560, 738, u), 22)
        if u >= 1:
            bold_text(cr, "+1", 400, 680, 50, GOLD)
    stamp(cr, t, A("h6", "not"), 360, 380, "NOT A HEAP", col=RED, size=72, end=A("h7") - 0.05)
    stamp(cr, t, A("h7", "Still"), 360, 380, "STILL NOT A HEAP", col=RED, size=58, end=A("h8") - 0.05)
    if t >= A("h8"):
        card(cr, t, A("h8"), 360, 330, 560, 220, "THE RULE", ["+1 grain never turns", "a not-heap into a heap"],
             col=PURPLE, title_size=44, line_size=40)
    vignette(cr, 0.35)


def scene_million(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe6ff"), hexc("#fff1d6"), seed=5)
    grow = ease_out(seg(t, A("h9"), A("h9", "million") + 0.8))
    heap(cr, 360, 860, 620 * grow + 10, 480 * grow + 6, seed=8)
    n = int(lerp(2, 1000000, grow))
    bold_text(cr, f"{n:,} GRAINS", 360, 220, 56, WHITE)
    obvious = t >= A("h10")
    if not obvious:
        if t >= A("h9", "not"):
            sign(cr, t, A("h9", "not"), 520, 420, "NOT A HEAP?", col=RED, size=44, rot=0.08)
    else:
        u = ease_out(seg(t, A("h10"), A("h10") + 0.5))
        cr.save()
        cr.translate(520 + 60 * u, 420 + 300 * u)
        cr.rotate(1.2 * u)
        sign(cr, t, 0, 0, 0, "NOT A HEAP?", col=RED, size=44)
        cr.restore()
        stamp(cr, t, A("h10", "obviously"), 360, 340, "OBVIOUSLY A HEAP", col=GREEN, size=56)
    vignette(cr, 0.35)


def cake(cr, t, x, y, n_candles):
    rrect(cr, x - 130, y - 110, 260, 110, 18)
    paint(cr, lin(0, y - 110, 0, y, [(0, hexc("#ffb8d0")), (1, hexc("#e87aa0"))]), OUTLINE, 5)
    rrect(cr, x - 140, y - 124, 280, 26, 12)
    paint(cr, WHITE, OUTLINE, 4)
    bold_text(cr, str(n_candles), x, y - 34, 64, WHITE)
    for k in range(5):
        cx = x - 100 + k * 50
        rrect(cr, cx - 6, y - 180, 12, 56, 4)
        paint(cr, hexc("#9fd0ff"), OUTLINE, 3)
        f = 1 + 0.12 * math.sin(t * 12 + k)
        smooth(cr, [(cx, y - 182), (cx - 8, y - 196), (cx, y - 214 * f / 1.0), (cx + 8, y - 196)])
        paint(cr, GOLD, hexc("#ff8a3c"), 2)


def scene_adult(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#e8dcff"), hexc("#fff1d6"), seed=9)
    mid = A("h12", "midnight")
    one = A("h12", "second")
    eighteen = t >= mid + 0.6 and t < one
    cake(cr, t, 360, 560, 18 if eighteen else 17)
    if t >= mid:
        secs = 59 if t < mid + 0.6 or t >= one else 0
        hh, mm = (11, 59) if secs == 59 else (12, 0)
        bold_text(cr, f"{hh:02d}:{mm:02d}:{secs:02d}", 360, 260, 76, RED if secs == 59 else GREEN)
    adult = eighteen
    if adult:
        person(cr, t, 360, 1080, 0.85, "fermi", eyes="happy", mouth="grin", arms=("up", "up"))
        tag(cr, t, mid + 0.6, 560, 700, "ADULT", col=GREEN, size=40)
    else:
        person(cr, t, 360, 1080, 0.85, "kid", eyes="wide" if t >= one else "open", mouth="o" if t >= one else "smile",
               arms=("hips", "hips"))
        if t >= one:
            tag(cr, t, one, 560, 700, "KID?!", col=RED, size=40)
    sign(cr, t, A("h11", "adult?"), 360, 130, "WHEN?", col=PURPLE, size=64, end=mid - 0.05)
    vignette(cr, 0.35)


def scene_law(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe6ff"), hexc("#fff1d6"), seed=4)
    x0, x1, y = 70, 650, 520
    cr.rectangle(x0, y - 60, x1 - x0, 120)
    cr.set_source(lin(x0, 0, x1, 0, [(0, hexc("#9fd8ff")), (1, hexc("#ff9a6a"))]))
    cr.fill()
    cr.rectangle(x0, y - 60, x1 - x0, 120)
    cr.set_line_width(5)
    cr.set_source_rgba(*OUTLINE)
    cr.stroke()
    bold_text(cr, "KID", x0 + 60, y + 16, 40, WHITE)
    bold_text(cr, "ADULT", x1 - 80, y + 16, 40, WHITE)
    line_t = A("h13", "draws")
    if t >= line_t:
        u = ease_out(seg(t, line_t, line_t + 0.4))
        lx = 430
        stroke_line(cr, [(lx, y - 100), (lx, y - 100 + 200 * u)], 10, RED, curve=False)
        tag(cr, t, line_t, lx, y - 150, "LAW: 18", col=RED, size=40)
    if t >= A("h13", "Nature"):
        bold_text(cr, "NATURE: no line", 360, 760, 54 * appear(t, A("h13", "Nature"), 0.3), GOLD)
    vignette(cr, 0.35)


def scene_views(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#e8dcff"), hexc("#fff1d6"), seed=7)
    heap(cr, 360, 860, 380, 230, seed=4)
    card(cr, t, A("h14", "fuzzy."), 190, 330, 320, 200, "FUZZY", ["no exact", "line"], col=BLUE, title_size=44,
         line_size=40)
    other = A("h14", "Others")
    card(cr, t, other, 530, 330, 320, 200, "SECRET GRAIN", ["one exact grain,", "we can't see it"], col=PURPLE,
         title_size=36, line_size=34)
    if t >= A("h14", "grain,"):
        k = appear(t, A("h14", "grain,"), 0.3)
        cr.arc(400, 700, 30 * k, 0, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 4)
        bold_text(cr, "?", 400, 716, 40 * k, WHITE)
    sign(cr, t, A("h14"), 360, 130, "TWO ANSWERS", col=GOLD, size=60, end=other - 0.05)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    classroom(cr, t, tl, kid_pose=dict(arms=("chin", "down"), eyes="half", mouth="smug"), look_at=(360, 0))
    bald_sir(cr, t, 150, 1120, 1.0, eyes="happy", mouth="smile", arms=("hips", "hips"))
    sparkles(cr, t, A("h15"), 150, 690, n=5, seed=3, col=WHITE, spread=70)
    sign(cr, t, A("h15"), 360, 140, "HOW MANY GRAINS?", col=GOLD, size=56)
    if t >= A("h15", "Tell"):
        sign(cr, t, A("h15", "Tell"), 360, 300, "COMMENT YOUR NUMBER", col=PURPLE, size=44, rot=0.03)
    vignette(cr, 0.4)


SCENES = {"ask": scene_ask, "hair": scene_hair, "eubulides": scene_eubulides, "grains": scene_grains,
          "million": scene_million, "adult": scene_adult, "law": scene_law, "views": scene_views, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
