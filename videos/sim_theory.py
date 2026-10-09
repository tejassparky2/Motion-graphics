"""Simulation theory (Bostrom's simulation argument) -- big-theory video in the polished look.

N. Bostrom, "Are You Living in a Computer Simulation?", Philosophical Quarterly 53 (2003): at least one is true --
(1) humanity goes extinct before reaching a "posthuman" stage, (2) posthumans run almost no ancestor simulations,
(3) we are almost certainly living in a simulation. Bostrom says he sees no strong argument for any one of the three.
Elon Musk, Code Conference 2016: "Forty years ago we had Pong, like two rectangles and a dot"; the odds we're in base
reality are "one in billions" (as reported by Game Informer and others). Pong: 1972.
Script pre-approved by the owner on 9 Oct 2026 (out/scripts_theories_batch1.md). Living people are named and quoted,
not drawn.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cairo, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, buttons, calendar, card, shake, sparkles,
                         studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter, lin,
                           paint, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite, stamp,
                           stroke_line, vignette)
from motion.toons import person

NARRATOR = dict(speed=0.93)
TAIL = 0.9

SCRIPT = [
    dict(id="v1", scene="hook", text="A philosopher at Oxford argued that you might be living inside a computer "
                                     "simulation."),
    dict(id="v2", scene="three", text="In [two thousand three,|2003,] Nick Bostrom said: at least one of these three "
                                      "things must be true."),
    dict(id="v3", scene="three", text="One. Humans die out before we can build super-realistic simulations."),
    dict(id="v4", scene="three", text="Two. We could build them, but we never bother."),
    dict(id="v5", scene="three", text="Three. We are almost certainly living inside one right now.", pace=0.93),
    dict(id="v6", scene="games", text="Why number three? Look at video games.", gap=0.35),
    dict(id="v7", scene="games", text="About fifty years ago, the best game was Pong. Two lines and a dot."),
    dict(id="v8", scene="games", text="Today, games look almost real. Keep improving, and one day you won't be able "
                                      "to tell them from reality."),
    dict(id="v9", scene="worlds", text="A future civilization could run billions of simulated worlds, full of people "
                                       "who think they're real."),
    dict(id="v10", scene="worlds", text="So for every real world, there could be billions of fake ones."),
    dict(id="v11", scene="dream", text="Imagine a billion dream worlds and one real one. You wake up somewhere. Where "
                                       "are you, probably?", pace=0.95),
    dict(id="v12", scene="quote", text="In [twenty sixteen,|2016,] Elon Musk said the odds that we are in base reality "
                                       "are one in billions."),
    dict(id="v13", scene="unsure", text="But Bostrom himself says he doesn't know which of the three is true."),
    dict(id="v14", scene="end", text="So be honest. If this were a simulation, what's the first thing you'd do?",
         gap=0.3, pace=0.95),
]

METADATA = dict(
    title="You Might Be Living Inside a Computer Game 🎮 (Simulation Theory)",
    alt_titles=["Are We Living in a Simulation? The Argument Explained Simply 🤯",
                "One of These 3 Things MUST Be True 🎮"],
    description="""A philosopher at Oxford argued that you might be living inside a computer simulation. 🎮

In 2003, Nick Bostrom said at least one of these three things must be true:
1️⃣ Humans die out before we can build super-realistic simulations.
2️⃣ We could build them, but we never bother.
3️⃣ We are almost certainly living inside one right now.

Why number three? Look at video games. About 50 years ago the best game was Pong: two lines and a dot. Today games look almost real. A future civilization could run billions of simulated worlds full of people who think they're real, so for every real world there could be billions of fake ones.
In 2016, Elon Musk said the odds that we are in base reality are "one in billions". But Bostrom himself says he doesn't know which of the three is true.

Sources: N. Bostrom, "Are You Living in a Computer Simulation?", Philosophical Quarterly (2003); Elon Musk at the 2016 Code Conference.

💬 Be honest: if this were a simulation, what's the first thing you'd do? 👇

🔔 Interestingly Strange: mind-bending theories, paradoxes, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#SimulationTheory", "#Philosophy", "#Shorts"],
    tags=["simulation theory", "are we living in a simulation", "nick bostrom", "simulation argument",
          "elon musk simulation", "philosophy", "mind blowing", "matrix", "reality", "interestingly strange"],
    pinned_comment="If this IS a simulation... what's the first thing you'd do? 🎮👇",
)

CODE = hexc("#3fe07a")


# ---------------------------------------------------------------- backdrops and props
def code_rain(cr, t, a=1.0, seed=3):
    """Dark screen with falling green digits."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#06140c")), (1, hexc("#0c2a18"))]))
    cr.fill()
    rng = random.Random(seed)
    cr.select_font_face("Fredoka", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(26)
    for col in range(16):
        x = 12 + col * 45
        sp = rng.uniform(120, 260)
        off = rng.uniform(0, 1400)
        for j in range(14):
            y = (t * sp + off + j * 30) % 1400 - 60
            k = j / 13
            cr.move_to(x, y)
            cr.set_source_rgba(0.25, 0.9, 0.5, a * (0.15 + 0.75 * k))
            cr.show_text("01"[(int(t * 8) + j + col) % 2])


def monitor(cr, x, y, w, h, s=1.0):
    """A screen bezel; returns nothing (call clip inside for content)."""
    soft_rrect(cr, x - w / 2 - 20, y - h / 2 - 10, w + 40, h + 60, 30, (0, 0, 0, 0.4), sigma=14)
    rrect(cr, x - w / 2 - 22, y - h / 2 - 22, w + 44, h + 44, 26)
    paint(cr, lin(0, y - h / 2, 0, y + h / 2, [(0, hexc("#4a4f5c")), (1, hexc("#2b2e38"))]), OUTLINE, 6)


def pong(cr, t, x, y, w, h):
    cr.save()
    rrect(cr, x - w / 2, y - h / 2, w, h, 10)
    cr.clip()
    cr.set_source_rgba(0.02, 0.02, 0.03, 1)
    cr.paint()
    bx = x + math.sin(t * 2.4) * (w / 2 - 40)
    by = y + math.sin(t * 3.7) * (h / 2 - 30)
    py1 = y + math.sin(t * 3.7 - 0.3) * (h / 2 - 50)
    py2 = y + math.sin(t * 3.7 + 0.3) * (h / 2 - 50)
    for px, py in ((x - w / 2 + 24, py1), (x + w / 2 - 34, py2)):
        cr.rectangle(px, py - 36, 10, 72)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill()
    cr.rectangle(bx - 7, by - 7, 14, 14)
    cr.fill()
    for k in range(10):
        cr.rectangle(x - 2, y - h / 2 + 10 + k * h / 10, 4, h / 20)
        cr.set_source_rgba(1, 1, 1, 0.6)
        cr.fill()
    cr.restore()


def modern_game(cr, t, x, y, w, h):
    cr.save()
    rrect(cr, x - w / 2, y - h / 2, w, h, 10)
    cr.clip()
    cr.rectangle(x - w / 2, y - h / 2, w, h)
    cr.set_source(lin(0, y - h / 2, 0, y + h / 2, [(0, hexc("#7cc6ff")), (0.5, hexc("#ffe8c4")),
                                                    (0.52, hexc("#7fc86a")), (1, hexc("#3a7a2a"))]))
    cr.fill()
    for k in range(3):
        mx = x - w / 2 + k * w / 2.5
        cr.move_to(mx - 120, y + 2)
        cr.line_to(mx, y - 90 - 20 * k)
        cr.line_to(mx + 140, y + 2)
        cr.close_path()
        cr.set_source_rgba(*alpha(hexc("#8a94b8"), 0.8))
        cr.fill()
    person(cr, t, x + math.sin(t) * 60, y + h / 2 - 30, 0.38, "achilles", walk=t * 10, run=True, tilt=0.12,
           eyes="angry", mouth="grin", arms=("fist", "down"))
    soft_disc(cr, x + w / 3, y - h / 3, 60, (1, 1, 0.85, 0.7))
    cr.restore()


def planet(cr, x, y, r, real=False, t=0.0):
    soft_disc(cr, x, y, r * 1.35, alpha(GOLD if real else CODE, 0.35))
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, rad(x - r * 0.3, y - r * 0.3, r * 1.3, [(0, hexc("#9fe0ff")), (1, hexc("#2f6ab8"))]),
          OUTLINE, max(2, r * 0.08))
    for k in range(3):
        ellipse(cr, x - r * 0.3 + k * r * 0.35, y - r * 0.1 + (k % 2) * r * 0.3, r * 0.28, r * 0.18, 0.3 * k)
        paint(cr, hexc("#5aa043"), None, 0)


def you_kid(cr, t, x, y, s, **kw):
    kw.setdefault("eyes", "open")
    kw.setdefault("mouth", "smile")
    person(cr, t, x, y, s, "kid", **kw)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    sim = A("v1", "simulation.")
    zoom_out = seg(t, A("v1", "computer"), sim + 0.6)
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=1)
    z = lerp(1.0, 0.42, ease_out(zoom_out))
    cr.save()
    cr.translate(W / 2, H / 2 - 40 * zoom_out)
    cr.scale(z, z)
    cr.translate(-W / 2, -H / 2)
    if zoom_out > 0:
        monitor(cr, 360, 640, W, H)
    cr.save()
    cr.rectangle(0, 0, W, H)
    cr.clip()
    studio(cr, t, hexc("#ffd6a8"), hexc("#fff1d6"), seed=2)
    you_kid(cr, t, 360, 920, 1.05, eyes="wide" if t >= A("v1", "you") else "open",
            mouth="o" if t >= A("v1", "you") else "smile", arms=("down", "down") if t < A("v1", "you") else
            ("face", "face"), brows="up" if t >= A("v1", "you") else None)
    if zoom_out > 0.3:      # scan lines: it's a screen
        for k in range(0, H, 8):
            cr.rectangle(0, k, W, 3)
            cr.set_source_rgba(0, 0, 0, 0.08)
            cr.fill()
    cr.restore()
    cr.restore()
    if zoom_out > 0.6:
        tag(cr, t, sim, 360, 470, "YOU", col=GOLD)
    sign(cr, t, A("v1", "Oxford"), 360, 140, "OXFORD PHILOSOPHER", col=BLUE, size=52, end=A("v1", "you") - 0.05)
    stamp(cr, t, sim, 360, 160, "SIMULATION?", col=GREEN, size=80)
    vignette(cr, 0.4)


ICONS = {}


def option_card(cr, t, start, y, num, title, col, icon, dim=False):
    if t < start:
        return
    k = appear(t, start, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(360, y)
    cr.scale(k, k)
    soft_rrect(cr, -300, -70, 600, 150, 28, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -300, -80, 600, 150, 28)
    paint(cr, lin(0, -80, 0, 70, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    cr.arc(-226, -5, 52, 0, 2 * math.pi)
    paint(cr, lin(0, -57, 0, 47, [(0, shade(col, 0.35)), (1, shade(col, -0.15))]), OUTLINE, 5)
    bold_text(cr, str(num), -226, 18, 60, WHITE)
    bold_text(cr, title, 0, 14, 40, INKC, outline=None, shadow=0)
    icon(cr, 240, -5)
    cr.restore()
    if dim:
        cr.save()
        rrect(cr, 60, y - 80, 600, 150, 28)
        cr.set_source_rgba(1, 1, 1, 0.55)
        cr.fill()
        cr.restore()


def ic_skull(cr, x, y):
    cr.arc(x, y - 6, 26, 0, 2 * math.pi)
    paint(cr, WHITE, OUTLINE, 4)
    rrect(cr, x - 14, y + 12, 28, 18, 4)
    paint(cr, WHITE, OUTLINE, 4)
    for dx in (-10, 10):
        cr.arc(x + dx, y - 8, 7, 0, 2 * math.pi)
        paint(cr, OUTLINE, None, 0)


def ic_sleep(cr, x, y):
    bold_text(cr, "Zzz", x, y + 14, 40, BLUE)


def ic_glitch(cr, x, y):
    for k, col in enumerate((RED, GREEN, BLUE)):
        rrect(cr, x - 30 + k * 4, y - 26 + k * 3, 52, 44, 8)
        paint(cr, alpha(col, 0.6), None, 0)
    bold_text(cr, "?", x, y + 14, 40, WHITE)


def scene_three(cr, t, tl):
    A = tl.at
    code_rain(cr, t, 0.6)
    v3, v4, v5 = A("v3"), A("v4"), A("v5")
    calendar(cr, t, A("v2", "2003,"), 360, 330, "NICK BOSTROM", "2003", col=BLUE, end=v3 - 0.05)
    sign(cr, t, A("v2", "three"), 360, 130, "ONE MUST BE TRUE", col=GOLD, size=60, end=v3 - 0.05)
    if t >= v3:
        option_card(cr, t, v3, 260, 1, "WE DIE OUT", RED, ic_skull, dim=t >= v5)
        option_card(cr, t, v4, 450, 2, "WE DON'T BOTHER", BLUE, ic_sleep, dim=t >= v5)
        option_card(cr, t, v5, 640, 3, "WE'RE IN ONE", GREEN, ic_glitch)
        if t >= A("v5", "now."):
            dx, dy = shake(t, A("v5", "now."), 0.5, 8)
            stamp(cr, t, A("v5", "now."), 360 + dx, 800 + dy, "RIGHT NOW", col=GREEN, size=60)
    vignette(cr, 0.45)


def scene_games(cr, t, tl):
    A = tl.at
    v7, v8 = A("v7"), A("v8")
    studio(cr, t, hexc("#2b2e48"), hexc("#5a4a7a"), seed=4)
    if t < v8:
        monitor(cr, 360, 520, 560, 400)
        if t >= A("v7", "Pong."):
            pong(cr, t, 360, 520, 560, 400)
        else:
            rrect(cr, 80, 320, 560, 400, 10)
            paint(cr, hexc("#0a0a10"), None, 0)
            if t >= A("v6", "games."):
                bold_text(cr, "GAME", 360, 540, 80, CODE)
        calendar(cr, t, A("v7", "fifty"), 590, 230, "ABOUT", "1972", col=RED)
        sign(cr, t, A("v7", "Pong."), 300, 820, "TWO LINES AND A DOT", col=GOLD, size=40)
    else:
        real = ease_out(seg(t, A("v8", "tell"), A("v8", "reality.") + 0.4))
        gw, gh, gy = lerp(560, W + 40, real), lerp(400, H + 40, real), lerp(520, 640, real)
        if real < 1:      # the bezel fades: you can't tell it's a screen any more
            cr.push_group()
            monitor(cr, 360, gy, gw, gh)
            cr.pop_group_to_source()
            cr.paint_with_alpha(1 - real)
        modern_game(cr, t, 360, gy, gw, gh)
        sign(cr, t, v8, 360, 160, "TODAY", col=BLUE, size=72, end=A("v8", "Keep") - 0.05)
        sign(cr, t, A("v8", "Keep"), 360, 160, "ONE DAY...", col=PURPLE, size=72, end=A("v8", "tell") - 0.05)
        stamp(cr, t, A("v8", "tell"), 360, 830, "REAL OR GAME?", col=RED, size=64)
    vignette(cr, 0.45)


def scene_worlds(cr, t, tl):
    A = tl.at
    code_rain(cr, t, 0.35, seed=8)
    v10 = A("v10")
    start = A("v9", "billions")
    n = 0
    if t >= start:
        n = int(1 + 63 * ease_out(seg(t, start, start + 2.2)))
    else:                  # one world first, then it multiplies
        planet(cr, 360, 520, 120 * appear(t, A("v9"), 0.5) + 1, t=t)
    for k in range(n):     # a grid of simulated worlds filling up
        col, row = k % 8, k // 8
        planet(cr, 70 + col * 83, 250 + row * 76, 30, t=t)
    if t < v10:
        counter(cr, t, start, 360, 900 - 90, 1000000000, size=84, dur=2.2, col=CODE, sub="SIMULATED WORLDS")
    else:
        planet(cr, 360, 520, 120, real=True, t=t)
        tag(cr, t, v10, 360, 350, "1 REAL", col=GOLD, size=52)
        sign(cr, t, A("v10", "billions"), 360, 820, "VS BILLIONS OF FAKES", col=GREEN, size=50)
    sign(cr, t, A("v9"), 360, 140, "A FUTURE CIVILIZATION", col=BLUE, size=48, end=A("v9", "people") - 0.05)
    sign(cr, t, A("v9", "people"), 360, 140, "PEOPLE WHO THINK THEY'RE REAL", col=PURPLE, size=40, end=v10 - 0.05)
    vignette(cr, 0.45)


def scene_dream(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a2e5a"), hexc("#7a5a9a"), seed=7)
    rng = random.Random(11)
    real_k = 37
    for k in range(80):    # dream bubbles, one gold "real" one
        col, row = k % 10, k // 10
        x, y = 54 + col * 68, 240 + row * 66
        if k == real_k:
            cr.arc(x, y, 26, 0, 2 * math.pi)
            paint(cr, rad(x - 6, y - 8, 30, [(0, hexc("#fff3a8")), (1, GOLD)]), OUTLINE, 3)
        else:
            cr.arc(x, y + math.sin(t * 2 + k) * 3, 22, 0, 2 * math.pi)
            paint(cr, alpha(hexc("#cfe8ff"), 0.6), alpha(WHITE, 0.8), 2)
    wake = A("v11", "wake")
    if t >= wake:          # "you" drop into a random bubble
        u = ease_out(seg(t, wake, wake + 0.9))
        tx, ty = 54 + 6 * 68, 240 + 5 * 66
        x, y = lerp(360, tx, u), lerp(120, ty, u)
        cr.arc(x, y, 18, 0, 2 * math.pi)
        paint(cr, RED, OUTLINE, 4)
        tag(cr, t, wake, x, y - 40, "YOU", col=RED, size=36)
    sign(cr, t, A("v11", "billion"), 360, 130, "1 BILLION DREAMS", col=BLUE, size=54, end=A("v11", "real") - 0.05)
    sign(cr, t, A("v11", "real"), 360, 130, "1 REAL WORLD", col=GOLD, size=60, end=A("v11", "Where") - 0.05)
    stamp(cr, t, A("v11", "probably?"), 360, 830, "PROBABLY A DREAM", col=PINK, size=56)
    vignette(cr, 0.45)


def scene_quote(cr, t, tl):
    A = tl.at
    code_rain(cr, t, 0.4, seed=5)
    card(cr, t, A("v12", "Musk"), 360, 470, 600, 330, "ELON MUSK, 2016", ["Chance we're in", "base reality:"],
         col=hexc("#5a6478"), title_size=44, line_size=44)
    if t >= A("v12", "one"):
        bold_text(cr, "1 IN BILLIONS", 360, 600, 70 * appear(t, A("v12", "one"), 0.4), RED)
    calendar(cr, t, A("v12", "2016,"), 360, 200, "CODE CONFERENCE", "2016", col=BLUE, end=A("v12", "Musk") - 0.05)
    vignette(cr, 0.45)


def scene_unsure(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=9)
    for k, (num, col) in enumerate(((1, RED), (2, BLUE), (3, GREEN))):
        st = A("v13") + 0.12 * k
        if t < st:
            continue
        kk = appear(t, st, 0.35)
        x = 140 + k * 220
        cr.save()
        cr.translate(x, 480 + math.sin(t * 2 + k) * 6)
        cr.scale(kk, kk)
        cr.arc(0, 0, 90, 0, 2 * math.pi)
        paint(cr, rad(-25, -30, 120, [(0, shade(col, 0.45)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, str(num), 0, 26, 90, WHITE)
        bold_text(cr, "?", 60, -50, 70, GOLD)
        cr.restore()
    sign(cr, t, A("v13", "Bostrom"), 360, 160, "EVEN BOSTROM", col=PURPLE, size=62, end=A("v13", "doesn't") - 0.05)
    sign(cr, t, A("v13", "doesn't"), 360, 160, "DOESN'T KNOW", col=RED, size=66)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    code_rain(cr, t, 0.5, seed=2)
    rng = random.Random(int(t * 10))
    gl = 6 if rng.random() < 0.3 else 0
    for dx, col in ((-gl, (1, 0.2, 0.3)), (gl, (0.2, 0.9, 1))):
        if gl:
            cr.push_group()
            cr.translate(dx, 0)
            you_kid(cr, t, 360, 930, 1.0, eyes="half", mouth="smug", arms=("hips", "point"))
            cr.pop_group_to_source()
            cr.paint_with_alpha(0.3)
    you_kid(cr, t, 360, 930, 1.0, eyes="half", mouth="smug", arms=("hips", "point"), brows="raise")
    sign(cr, t, A("v14"), 360, 150, "IF THIS WERE A SIMULATION...", col=GREEN, size=40)
    sign(cr, t, A("v14", "first"), 360, 280, "FIRST THING YOU'D DO?", col=GOLD, size=52, rot=0.03)
    vignette(cr, 0.45)


SCENES = {"hook": scene_hook, "three": scene_three, "games": scene_games, "worlds": scene_worlds,
          "dream": scene_dream, "quote": scene_quote, "unsure": scene_unsure, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
