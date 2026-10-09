"""The Fermi paradox ("Where is everybody?") -- big-theory video in the polished look.

E. M. Jones, "Where Is Everybody?" An Account of Fermi's Question (Los Alamos LA-10311-MS, 1985): at lunch in Los
Alamos in summer 1950, with Konopinski, Teller and York, after talk about flying saucers, Fermi asked (as Teller
recalled it) "Where is everybody?". Milky Way: ~100-400 billion stars. Kepler-based estimate: at least 8.8 billion
Earth-size planets in the habitable zone of Sun-like stars (Petigura, Howard & Marcy, PNAS 2013). "Great Filter":
Robin Hanson (1996). Script pre-approved by the owner on 9 Oct 2026 (out/scripts_theories_batch1.md).
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, calendar, card, shake,
                         sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter,
                           lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite,
                           stamp, stroke_line, vignette)
from motion.toons import alien, head, person

NARRATOR = dict(speed=0.92)
TAIL = 0.9
voice.SPEAKERS.update({"fermi": dict(voice="am_michael", speed=0.98, pitch=-1.0)})

SCRIPT = [
    dict(id="f1", scene="hook", text="Our galaxy could have billions of planets like Earth. So where is everybody?"),
    dict(id="f2", scene="lunch", text="[Nineteen fifty.|1950.] The physicist Enrico Fermi is having lunch with "
                                      "friends, joking about flying saucers."),
    dict(id="f3", scene="lunch", text="Suddenly he asks. But where is everybody?", speaker="fermi",
         speaker_from="But", pace=0.95),
    dict(id="f4", scene="numbers", text="Here's why that's scary. Our galaxy has at least a [hundred billion|100 "
                                        "billion] stars.", gap=0.35),
    dict(id="f5", scene="numbers", text="And scientists estimate billions of Earth-size planets sit in the zone where "
                                        "water can be liquid."),
    dict(id="f6", scene="numbers", text="Even if only a tiny fraction had life, the galaxy should be buzzing."),
    dict(id="f7", scene="silence", text="But we've heard nothing. No signals. No visitors. Just silence.", pace=0.93),
    dict(id="f8", scene="answers", text="So, the answers. Maybe life is incredibly rare, and we're just lucky."),
    dict(id="f9", scene="answers", text="Maybe something wipes out civilizations before they reach the stars. Some "
                                        "scientists call it the Great Filter."),
    dict(id="f10", scene="answers", text="Or maybe they're out there, staying quiet on purpose."),
    dict(id="f11", scene="forest", text="It's like standing in a dark forest at night. Total silence. Either you're "
                                        "alone, or everyone else is hiding.", pace=0.95),
    dict(id="f12", scene="end", text="Which answer scares you more? That we're alone? Or that we're not?", gap=0.3,
         pace=0.95),
]

METADATA = dict(
    title="Where Is Everybody? 👽 (The Fermi Paradox Explained)",
    alt_titles=["Billions of Planets... So Why Is Space SILENT? 👽", "The Question That Haunts Scientists: Where Are the Aliens? 🌌"],
    description="""Our galaxy could have billions of planets like Earth. So where is everybody? 👽

1950: physicist Enrico Fermi is having lunch with friends, joking about flying saucers, when he suddenly asks: "But where is everybody?"

Here's why that's scary: our galaxy has at least 100 billion stars, and scientists estimate billions of Earth-size planets sit in the zone where water can be liquid. Even if only a tiny fraction had life, the galaxy should be buzzing. But we've heard nothing. No signals. No visitors. Just silence.

The answers? Maybe life is incredibly rare and we're just lucky. Maybe something wipes out civilizations before they reach the stars (the "Great Filter"). Or maybe they're out there, staying quiet on purpose. Like standing in a dark forest at night: either you're alone, or everyone else is hiding.

Sources: E. M. Jones, "Where Is Everybody?" An Account of Fermi's Question (Los Alamos, 1985); Petigura, Howard & Marcy, PNAS (2013); R. Hanson, "The Great Filter" (1996).

💬 Which answer scares you more: that we're alone, or that we're not? 👇

🔔 Interestingly Strange: mind-bending theories, paradoxes, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#FermiParadox", "#Space", "#Shorts"],
    tags=["fermi paradox", "where is everybody", "aliens", "are we alone", "great filter", "dark forest theory",
          "space facts", "enrico fermi", "extraterrestrial life", "interestingly strange"],
    pinned_comment="Alone or not alone: which one actually scares you more? 👽👇",
)

SPACE_TOP = hexc("#070818")
SPACE_BOT = hexc("#1e1640")


# ---------------------------------------------------------------- space
def _galaxy(c, size=900):
    rng = random.Random(42)
    cx = cy = size / 2
    for k in range(5200):
        arm = k % 2
        u = rng.random() ** 0.7
        r = 20 + u * size * 0.45
        ang = arm * math.pi + r / 70.0 + rng.gauss(0, 0.32 * (1.1 - u))
        x = cx + math.cos(ang) * r + rng.gauss(0, 10)
        y = cy + math.sin(ang) * r * 0.55 + rng.gauss(0, 6)
        b = 0.4 + 0.6 * rng.random()
        col = (1, 0.85 + 0.15 * rng.random(), 0.7 + 0.3 * rng.random()) if rng.random() < 0.7 else (0.7, 0.8, 1.0)
        c.arc(x, y, 0.8 + 1.6 * rng.random() * (1 - u * 0.5), 0, 2 * math.pi)
        c.set_source_rgba(col[0], col[1], col[2], b)
        c.fill()
    c.set_source(rad(cx, cy, 160, [(0, (1, 0.96, 0.85, 0.95)), (0.3, (1, 0.85, 0.6, 0.45)), (1, (1, 0.8, 0.6, 0))]))
    c.arc(cx, cy, 160, 0, 2 * math.pi)
    c.fill()


def galaxy(cr, t, x, y, s=1.0, a=1.0):
    spr = sprite("galaxy", 900, 900, _galaxy, sigma=0.6, scale=1.0)
    glow = sprite("galaxy_glow", 900, 900, _galaxy, sigma=14, scale=0.25)
    cr.save()
    cr.translate(x, y)
    cr.rotate(t * 0.04)
    cr.scale(s, s)
    put(cr, glow, -450, -450, a=0.8 * a)
    put(cr, spr, -450, -450, a=a)
    cr.restore()


def space(cr, t, seed=1):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, SPACE_TOP), (1, SPACE_BOT)]))
    cr.fill()
    rng = random.Random(seed)
    for k in range(120):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        tw = 0.5 + 0.5 * math.sin(t * (1 + rng.random() * 3) + k)
        cr.arc(x, y, rng.uniform(0.8, 2.2), 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.25 + 0.6 * tw * rng.random())
        cr.fill()


def earth(cr, x, y, r):
    soft_disc(cr, x, y, r * 1.5, (0.4, 0.7, 1.0, 0.3))
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, rad(x - r * 0.3, y - r * 0.3, r * 1.3, [(0, hexc("#9fe0ff")), (1, hexc("#2f6ab8"))]), OUTLINE,
          max(2, r * 0.06))
    for k in range(4):
        ellipse(cr, x - r * 0.35 + k * r * 0.28, y - r * 0.2 + (k % 2) * r * 0.35, r * 0.26, r * 0.16, 0.4 * k)
        paint(cr, hexc("#5aa043"), None, 0)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    space(cr, t)
    z = lerp(0.75, 0.95, seg(t, 0, A("f1", "So")))
    galaxy(cr, t, 360, 520, z)
    if t >= A("f1", "Earth."):
        earth(cr, 480, 600, 26 * appear(t, A("f1", "Earth."), 0.4) + 1)
        tag(cr, t, A("f1", "Earth."), 480, 548, "US", col=BLUE, size=36)
    sign(cr, t, A("f1", "billions"), 360, 140, "BILLIONS OF EARTHS?", col=BLUE, size=54, end=A("f1", "So") - 0.05)
    sign(cr, t, A("f1", "where"), 360, 140, "WHERE IS EVERYBODY?", col=GOLD, size=54)
    vignette(cr, 0.5)


def _diner(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 760, [(0, hexc("#c9e8d8")), (1, hexc("#e8f6ee"))]))
    c.fill()
    for k in range(0, W, 40):
        c.rectangle(k, 560, 20, 200)
        c.set_source_rgba(1, 1, 1, 0.25)
        c.fill()
    rrect(c, 420, 140, 240, 200, 10)      # a window onto the desert mesa
    paint(c, lin(0, 140, 0, 340, [(0, hexc("#ffb27a")), (1, hexc("#ffe2b8"))]), OUTLINE, 6)
    c.move_to(424, 300)
    c.line_to(500, 250)
    c.line_to(600, 250)
    c.line_to(656, 300)
    c.line_to(656, 336)
    c.line_to(424, 336)
    c.close_path()
    c.set_source_rgba(*hexc("#c96a3a"))
    c.fill()
    c.rectangle(0, 760, W, H - 760)
    for y in range(760, H, 60):
        for x in range(0, W, 60):
            c.rectangle(x, y, 60, 60)
            c.set_source_rgba(*(hexc("#e8473f") if (x // 60 + y // 60) % 2 else hexc("#f4f0e6")))
            c.fill()


def scene_lunch(cr, t, tl):
    A = tl.at
    put(cr, sprite("diner", W, H, _diner), 0, 0)
    asks = A("f3", "But")
    cam = camera(t, [(A("f2") - 0.3, (1.0, 360, 640)), (asks, (1.3, 330, 560))], dur=0.6)
    cr.save()
    enter(cr, cam)
    frozen = t >= asks
    for k, (x, who, kw) in enumerate(((560, "reporter", dict(fedora=None, suit=hexc("#5a6478"))),
                                       (110, "villager", dict(beard=None, shirt=hexc("#c9a46a"))))):
        person(cr, t, x, 900, 0.78, who, eyes="wide" if frozen else "happy", mouth="o" if frozen else "grin",
               arms=("down", "down") if frozen else ("hold", "down"), facing=-1 if x > 360 else 1, seed=k,
               look=(-0.5 if x > 360 else 0.5, 0), **kw)
    person(cr, t, 330, 900, 0.9, "fermi", eyes="half" if frozen else "happy",
           mouth="talk" if tl.speaking("fermi", t) else ("flat" if frozen else "grin"),
           arms=("up", "down") if frozen else ("hold", "down"), brows="raise" if frozen else None)
    rrect(cr, 20, 760, 680, 30, 10)        # the table
    paint(cr, lin(0, 760, 0, 790, [(0, hexc("#e8e0d0")), (1, hexc("#b8b0a0"))]), OUTLINE, 5)
    for px in (140, 330, 540):
        ellipse(cr, px, 758, 60, 12)
        paint(cr, WHITE, OUTLINE, 3.5)
    cr.restore()
    calendar(cr, t, A("f2", "1950."), 360, 330, "LOS ALAMOS", "1950", col=RED, end=A("f2", "joking") - 0.05)
    if A("f2", "joking") <= t < asks:      # a flying saucer doodle above them
        sx = 360 + math.sin(t * 2) * 120
        ellipse(cr, sx, 300, 90, 26)
        paint(cr, lin(0, 274, 0, 326, [(0, hexc("#dfe6ee")), (1, hexc("#8a94a8"))]), OUTLINE, 5)
        cr.new_path()
        cr.arc(sx, 290, 40, math.pi, 2 * math.pi)
        cr.close_path()
        paint(cr, (0.7, 0.9, 1.0, 0.85), OUTLINE, 4)
        bold_text(cr, "HA HA", 600, 420, 44, GOLD)
    tag(cr, t, A("f2", "Enrico"), 330, 240, "ENRICO FERMI", col=hexc("#9fc8ff"), end=asks - 0.05)
    bubble(cr, t, asks, 380, 160, "BUT WHERE IS EVERYBODY?", size=44, tail=-1, col=hexc("#fff3c4"))
    vignette(cr, 0.4)


def scene_numbers(cr, t, tl):
    A = tl.at
    space(cr, t, seed=3)
    f5, f6 = A("f5"), A("f6")
    galaxy(cr, t, 360, 540, 0.82)
    if t < f5:
        counter(cr, t, A("f4", "100"), 360, 830, 100000000000, size=64, dur=1.4, col=WHITE, sub="STARS (AT LEAST)")
        sign(cr, t, A("f4", "scary."), 360, 140, "HERE'S WHY", col=RED, size=62)
    else:
        rng = random.Random(7)
        n = int(60 * ease_out(seg(t, A("f5", "billions"), A("f5", "billions") + 1.5)))
        for k in range(n):        # habitable planets light up
            a = rng.uniform(0, 6.28)
            r = rng.uniform(40, 340)
            x, y = 360 + math.cos(a) * r, 540 + math.sin(a) * r * 0.55
            cr.arc(x, y, 6, 0, 2 * math.pi)
            paint(cr, GREEN, OUTLINE, 2)
            if t >= f6 and k % 4 == 0:     # ...and some of them with life
                st = A("f6", "buzzing.") - 0.4 + (k % 12) * 0.05
                if t >= st:
                    cr.save()
                    cr.translate(x, y - 6)
                    cr.scale(0.16, 0.16)
                    alien(cr, t, 0, 0, 1.0, mouth="grin", wave=True, seed=k)
                    cr.restore()
        sign(cr, t, A("f5", "billions"), 360, 140, "BILLIONS OF EARTH-SIZE PLANETS", col=GREEN, size=40,
             end=f6 - 0.05)
        sign(cr, t, f6, 360, 140, "SHOULD BE BUZZING!", col=GOLD, size=56)
    vignette(cr, 0.5)


def dish(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for side in (-1, 1):
        stroke_line(cr, [(side * 20, 0), (side * 70, 180)], 16, OUTLINE, curve=False)
        stroke_line(cr, [(side * 20, 0), (side * 70, 180)], 9, hexc("#cfd5df"), curve=False)
    cr.save()
    cr.rotate(-0.5)
    ellipse(cr, 0, -40, 170, 70)
    paint(cr, lin(0, -110, 0, 30, [(0, WHITE), (1, hexc("#9aa4b4"))]), OUTLINE, 6)
    stroke_line(cr, [(0, -40), (0, -170)], 8, OUTLINE, curve=False)
    cr.arc(0, -176, 12, 0, 2 * math.pi)
    paint(cr, RED, OUTLINE, 3)
    cr.restore()
    cr.restore()


def scene_silence(cr, t, tl):
    A = tl.at
    space(cr, t, seed=5)
    cr.rectangle(0, 820, W, H - 820)
    cr.set_source(lin(0, 820, 0, H, [(0, hexc("#2a2440")), (1, hexc("#120e22"))]))
    cr.fill()
    dish(cr, t, 360, 640, 1.2)
    # a flat signal line
    rrect(cr, 80, 120, 560, 140, 20)
    paint(cr, (0.05, 0.1, 0.08, 0.85), OUTLINE, 5)
    pts = [(100 + k * 13, 190 + (math.sin(k * 1.7 + t * 30) * 2.5)) for k in range(41)]
    stroke_line(cr, pts, 4, (0.3, 1.0, 0.5, 1), curve=False)
    keys = ("signals.", "visitors.", "silence.")
    for k, (txt, col) in enumerate((("NO SIGNALS", RED), ("NO VISITORS", PURPLE), ("SILENCE", hexc("#8a94a8")))):
        end = A("f7", keys[k + 1]) - 0.05 if k < 2 else None
        stamp(cr, t, A("f7", keys[k]), 360, 330, txt, col=col, size=64, end=end)
    sign(cr, t, A("f7"), 360, 330, "WE'VE HEARD...", col=BLUE, size=56, end=A("f7", "signals.") - 0.05)
    vignette(cr, 0.55)


def answer_card(cr, t, start, y, num, title, col, end=None):
    if t < start:
        return
    k = appear(t, start, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(360, y)
    cr.scale(k, k)
    soft_rrect(cr, -300, -56, 600, 120, 26, (0, 0, 0, 0.35), sigma=10)
    rrect(cr, -300, -64, 600, 120, 26)
    paint(cr, lin(0, -64, 0, 56, [(0, WHITE), (1, hexc("#e4e0f0"))]), OUTLINE, 6)
    cr.arc(-236, -4, 44, 0, 2 * math.pi)
    paint(cr, lin(0, -48, 0, 40, [(0, shade(col, 0.35)), (1, shade(col, -0.15))]), OUTLINE, 5)
    bold_text(cr, str(num), -236, 16, 52, WHITE)
    bold_text(cr, title, 30, 14, 42, INKC, outline=None, shadow=0)
    cr.restore()


def scene_answers(cr, t, tl):
    A = tl.at
    space(cr, t, seed=7)
    f9, f10 = A("f9"), A("f10")
    answer_card(cr, t, A("f8", "Maybe"), 220, 1, "LIFE IS RARE", GOLD)
    answer_card(cr, t, f9, 370, 2, "THE GREAT FILTER", RED)
    answer_card(cr, t, f10, 520, 3, "THEY'RE HIDING", PURPLE)
    if t < f9:          # lucky lonely Earth
        earth(cr, 360, 720, 90 * appear(t, A("f8", "Maybe"), 0.4) + 1)
        if t >= A("f8", "lucky."):
            sparkles(cr, t, A("f8", "lucky."), 360, 640, n=8, seed=3, col=GOLD)
            tag(cr, t, A("f8", "lucky."), 360, 610, "LUCKY US", col=GOLD)
    elif t < f10:       # civilizations hitting a wall
        rrect(cr, 540, 600, 50, 280, 8)
        paint(cr, lin(520, 0, 560, 0, [(0, RED), (1, shade(RED, -0.3))]), OUTLINE, 5)
        for k in range(3):
            st = f9 + 0.3 + k * 0.45
            u = seg(t, st, st + 0.6)
            if t >= st:
                x = lerp(100, 450, ease_out(u))
                y = 680 + k * 60
                cr.save()
                cr.translate(x, y)
                cr.rotate(0.6 if u >= 1 else 0)
                cr.scale(0.85, 0.85)
                rrect(cr, -60, -20, 120, 40, 18)
                paint(cr, lin(0, -20, 0, 20, [(0, hexc("#dfe6ee")), (1, hexc("#8a94a8"))]), OUTLINE, 4)
                cr.move_to(60, -12)
                cr.line_to(100, 0)
                cr.line_to(60, 12)
                cr.close_path()
                paint(cr, RED, OUTLINE, 3)
                cr.restore()
                if u >= 1:
                    cue("hit", t, st + 0.6)
        sign(cr, t, A("f9", "Great"), 360, 900 - 60, "THE GREAT FILTER", col=RED, size=40, rot=0.03)
    else:               # an alien hiding behind a planet: shh
        cr.arc(380, 760, 130, 0, 2 * math.pi)
        paint(cr, rad(340, 720, 170, [(0, hexc("#c98ad8")), (1, hexc("#5a2a7a"))]), OUTLINE, 6)
        peek = ease_out(seg(t, f10 + 0.3, f10 + 0.8))
        cr.save()
        cr.rectangle(0, 0, W, 760)
        cr.clip()
        alien(cr, t, 520, lerp(900, 760, peek), 0.6, mouth="o", eyes="half", seed=2)
        cr.restore()
        if peek > 0.9:
            bold_text(cr, "SHH...", 600, 620, 44, PINK)
    vignette(cr, 0.5)


def _forest(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#0c1830")), (1, hexc("#04080f"))]))
    c.fill()
    c.arc(540, 220, 70, 0, 2 * math.pi)
    c.set_source(rad(540, 220, 70, [(0, (1, 1, 0.92, 1)), (1, (0.85, 0.9, 1, 1))]))
    c.fill()
    rng = random.Random(9)
    for layer, (col, base, hgt) in enumerate(((hexc("#16264a"), 820, 420), (hexc("#0e1a34"), 900, 520),
                                               (hexc("#08101f"), 1000, 600))):
        x = -60
        while x < W + 60:
            w = rng.uniform(90, 150)
            h = hgt * rng.uniform(0.7, 1.0)
            for j in range(3):
                c.move_to(x - w / 2 + j * 10, base - j * h * 0.28)
                c.line_to(x, base - h - j * 10)
                c.line_to(x + w / 2 - j * 10, base - j * h * 0.28)
                c.close_path()
                c.set_source_rgba(*col)
                c.fill()
            x += w * 0.8
    c.rectangle(0, 980, W, H - 980)
    c.set_source_rgba(*hexc("#05080f"))
    c.fill()


def scene_forest(cr, t, tl):
    A = tl.at
    put(cr, sprite("forest", W, H, _forest), 0, 0)
    hide = A("f11", "hiding.")
    cr.save()
    enter(cr, camera(t, [(A("f11") - 0.3, (1.0, 360, 640)), (A("f11", "Either"), (1.12, 330, 640))], dur=1.0))
    person(cr, t, 240, 960, 0.85, "kid", eyes="wide", mouth="o" if t >= hide else "flat", arms=("hold", "down"),
           sweat=t >= hide, brows="up" if t >= hide else None,
           hold=lambda c, hx, hy: (stroke_line(c, [(hx, hy), (hx + 40, hy - 20)], 16, OUTLINE, curve=False)))
    cr.restore()
    beam = 0.18 + 0.05 * math.sin(t * 7)
    cr.move_to(300, 700)
    cr.line_to(720, 520)
    cr.line_to(720, 760)
    cr.close_path()
    cr.set_source_rgba(1, 0.95, 0.7, beam)
    cr.fill()
    if t >= A("f11", "everyone"):      # eyes open in the dark, one pair at a time
        rng = random.Random(4)
        for k in range(9):
            st = A("f11", "everyone") + 0.12 * k
            if t < st:
                continue
            x, y = rng.uniform(60, 680), rng.uniform(420, 880)
            blink = 1.0 if (t * 0.9 + k * 0.37) % 1 > 0.08 else 0.15
            for dx in (-12, 12):
                ellipse(cr, x + dx, y, 7, 9 * blink * appear(t, st, 0.3) + 0.5)
                paint(cr, (1, 0.95, 0.4, 0.95), None, 0)
            soft_disc(cr, x, y, 30, (1, 0.9, 0.3, 0.15))
    sign(cr, t, A("f11", "forest"), 360, 140, "A DARK FOREST", col=hexc("#3a4a6e"), size=58,
         end=A("f11", "Either") - 0.05)
    sign(cr, t, A("f11", "alone,"), 360, 140, "ALONE...", col=BLUE, size=64, end=A("f11", "everyone") - 0.05)
    sign(cr, t, A("f11", "everyone"), 360, 140, "...OR HIDING?", col=PURPLE, size=64)
    vignette(cr, 0.6)


def scene_end(cr, t, tl):
    A = tl.at
    space(cr, t, seed=9)
    alone = A("f12", "alone?")
    earth(cr, 360, 560, 130)
    if t >= A("f12", "not?"):
        for k, (x, y) in enumerate(((120, 380), (600, 420), (140, 760), (580, 760))):
            alien(cr, t, x, y, 0.45 * appear(t, A("f12", "not?") + 0.1 * k, 0.4) + 0.01, eyes="half", mouth="smug",
                  wave=k % 2 == 0, seed=k)
    sign(cr, t, A("f12"), 360, 140, "WHICH IS SCARIER?", col=PURPLE, size=56)
    buttons(cr, t, alone, [("ALONE", BLUE), ("NOT ALONE", GREEN)], y=290)
    vignette(cr, 0.5)


SCENES = {"hook": scene_hook, "lunch": scene_lunch, "numbers": scene_numbers, "silence": scene_silence,
          "answers": scene_answers, "forest": scene_forest, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
