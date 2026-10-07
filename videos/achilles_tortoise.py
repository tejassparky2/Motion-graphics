"""Achilles and the Tortoise (Zeno's paradox) in the polished look (motion/polish.py + motion/toons.py).

Zeno of Elea (5th century BC), known through Aristotle's Physics VI.9: the fastest runner can never catch a slower
one, because he must first reach where it was, by which time it has moved on, and so on forever. Achilles is the
"swift-footed" hero of Homer's Iliad. The resolution: infinitely many steps can take a finite total time.
Numbers (all from line a3): Achilles 10 m/s, tortoise 1 m/s, 100 m head start -> steps of 10 s, 1 s, 0.1 s, 0.01 s...
total 100/9 = 11.11 s, when both are at 111.1 m. Sources: Britannica "Achilles paradox"; Wikipedia "Zeno's paradoxes".
Script approved by the owner on 7 Oct 2026 (out/scripts_polished_batch1.md).
"""
import math
import random

from motion.engine import W, H, cue, ease_out, hexc, lerp, seg, clamp01
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, ellipse, enter,
                           light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite,
                           stamp, stroke_line, vignette)
from motion.toons import person, portrait, tortoise

NARRATOR = dict()
TAIL = 0.9

SCRIPT = [
    dict(id="a1", scene="hook", text="A Greek thinker once proved that the fastest runner alive can never catch a "
                                     "tortoise."),
    dict(id="a2", scene="intro", text="His name was Zeno. And the runner was Achilles, the fastest hero in Greek "
                                      "stories."),
    dict(id="a3", scene="rules", text="Here's the race. Achilles runs [ten|10] meters every second. The tortoise "
                                      "runs one."),
    dict(id="a4", scene="race", text="So the tortoise gets a [hundred|100] meter head start."),
    dict(id="a5", scene="race", text="Achilles runs those [hundred|100] meters. That takes him [ten|10] seconds."),
    dict(id="a6", scene="race", text="But in [ten|10] seconds, the tortoise moved [ten|10] meters. It's still ahead."),
    dict(id="a7", scene="race", text="Achilles runs those [ten|10] meters. One second."),
    dict(id="a8", scene="race", text="The tortoise moved one more meter. Still ahead."),
    dict(id="a9", scene="steps", text="Every time Achilles reaches where the tortoise was, it has moved a little "
                                      "further."),
    dict(id="a10", scene="steps", text="The steps never end. So Zeno said, Achilles never catches it."),
    dict(id="a11", scene="math", text="Sounds right? Here's the trick. Add up the times."),
    dict(id="a12", scene="math", text="[Ten|10] seconds. Plus one. Plus a tenth. Plus a hundredth.", pace=0.95),
    dict(id="a13", scene="math", text="The steps never end. But the total never even reaches [eleven point two|11.2] "
                                      "seconds."),
    dict(id="a14", scene="pass", text="So after about [eleven|11] seconds, Achilles is level. Then he zooms past."),
    dict(id="a15", scene="summary", text="Endless steps. But a short race."),
    dict(id="a16", scene="end", text="So, did Zeno's trick fool you? Yes, or no?", gap=0.3),
]

METADATA = dict(
    title="A Tortoise Beats The Fastest Runner Alive?! 🐢 (Zeno's Paradox)",
    alt_titles=["Why Achilles Can NEVER Catch The Tortoise 🐢 (Or Can He?)",
                "The 2,400-Year-Old Paradox That Fooled Everyone 🏃‍♂️🐢"],
    description="""A Greek thinker once "proved" that the fastest runner alive can never catch a tortoise. 🐢

Zeno's race: Achilles runs 10 meters every second, the tortoise runs 1, and the tortoise gets a 100 meter head start.
Achilles runs those 100 meters in 10 seconds, but the tortoise has moved 10 meters. He runs those in 1 second, but it has moved 1 more meter. Every time he reaches where it was, it has moved a little further. The steps never end... so he never catches it?

The trick: add up the times. 10 + 1 + 0.1 + 0.01 + ... The steps never end, but the total never even reaches 11.2 seconds. After about 11.1 seconds both are at 111.1 meters, and then Achilles zooms past. Endless steps, short race.

Sources: Zeno of Elea's paradoxes, as recorded by Aristotle (Physics, Book VI); Encyclopaedia Britannica, "Achilles paradox".

💬 So, did Zeno fool you? Yes or no? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#Math", "#Shorts"],
    tags=["achilles and the tortoise", "zeno's paradox", "zeno paradox explained", "paradox", "infinite series",
          "math paradox", "greek philosophy", "achilles", "tortoise", "brain teaser", "interestingly strange"],
    pinned_comment="Be honest: did Zeno fool you for a second? Yes or no? 🐢👇",
)

RED = hexc("#e8473f")
GOLD = hexc("#ffcf3f")
BLUE = hexc("#4aa3f0")
GREEN = hexc("#3fbf6a")
PURPLE = hexc("#7a5bd0")
CLAY = hexc("#d98a5a")

PX = 10.0          # world pixels per metre on the track
GROUND = 760.0     # world y of the track
HERO_S = 0.8
TORT_S = 0.62


# ---------------------------------------------------------------- backgrounds
def _sky_layer(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#5fb0f0")), (0.5, hexc("#bfe4ff")), (0.62, hexc("#fff3d6")),
                                  (1, hexc("#fff3d6"))]))
    c.fill()
    c.set_source(rad(540, 260, 520, [(0, (1, 0.98, 0.85, 0.8)), (0.3, (1, 0.93, 0.7, 0.25)), (1, (1, 0.9, 0.6, 0))]))
    c.rectangle(0, 0, W, H)
    c.fill()
    c.arc(540, 260, 60, 0, 2 * math.pi)
    c.set_source(rad(540, 260, 60, [(0, (1, 1, 0.94, 1)), (1, (1, 0.93, 0.6, 1))]))
    c.fill()
    rng = random.Random(3)
    for k in range(4):      # soft clouds
        cx, cy = rng.uniform(60, 660), rng.uniform(120, 420)
        for j in range(4):
            c.arc(cx + j * 38 - 60, cy + (j % 2) * 10, 34 + 8 * (j % 2), 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.75)
        c.fill()


def sky(cr, t):
    put(cr, sprite("ach_sky", W, H, _sky_layer), 0, 0)


def _hills_layer(c):
    """Far hills with a little Greek temple, drawn wide so the camera can pan across."""
    for k, (yy, amp, col) in enumerate(((560, 70, hexc("#b8dca0")), (610, 50, hexc("#94c97c")))):
        c.move_to(0, 900)
        for x in range(0, 2401, 40):
            c.line_to(x, yy - amp * (0.5 + 0.5 * math.sin(x / 180.0 + k * 2.1)))
        c.line_to(2400, 900)
        c.close_path()
        c.set_source_rgba(*col)
        c.fill()
    tx, ty = 1500, 470
    c.move_to(tx - 130, ty)
    c.line_to(tx, ty - 60)
    c.line_to(tx + 130, ty)
    c.close_path()
    paint(c, hexc("#f4efe4"), alpha(OUTLINE, 0.5), 3)
    for k in range(6):
        rrect(c, tx - 110 + k * 42, ty + 4, 18, 90, 3)
        paint(c, hexc("#fbf8f0"), alpha(OUTLINE, 0.4), 2)
    rrect(c, tx - 130, ty + 92, 260, 14, 3)
    paint(c, hexc("#e8e0d0"), alpha(OUTLINE, 0.5), 3)


def stadium(cr, t, cam):
    """Sky (screen space), far hills with parallax, then the world-space running track."""
    sky(cr, t)
    z, fx, fy = cam
    cr.save()      # far hills: a fraction of the camera's movement
    cr.translate(W / 2, H / 2)
    pz = 1 + (z - 1) * 0.25
    cr.scale(pz, pz)
    cr.translate(-W / 2 - (fx - 550) * 0.15, -H / 2 - (fy - 520) * 0.1 + (GROUND - 760))
    put(cr, sprite("ach_hills", 2400, 900, _hills_layer, sigma=2.0, scale=0.5), -840, 40)
    cr.restore()


def track(cr, t, x0=-1500, x1=3000, marks=()):
    cr.rectangle(x0, GROUND - 70, x1 - x0, 2000)
    cr.set_source(lin(0, GROUND - 70, 0, GROUND + 300, [(0, hexc("#7fc86a")), (1, hexc("#4e9e3a"))]))
    cr.fill()
    cr.rectangle(x0, GROUND - 40, x1 - x0, 130)
    cr.set_source(lin(0, GROUND - 40, 0, GROUND + 90, [(0, shade(CLAY, 0.15)), (1, shade(CLAY, -0.15))]))
    cr.fill()
    for yy in (GROUND - 40, GROUND + 25, GROUND + 90):
        cr.rectangle(x0, yy - 3, x1 - x0, 6)
        cr.set_source_rgba(1, 1, 1, 0.85)
        cr.fill()
    for m in range(-50, 200, 10):      # a tick every 10 m
        x = m * PX
        cr.rectangle(x - 2, GROUND + 92, 4, 22)
        cr.set_source_rgba(1, 1, 1, 0.6)
        cr.fill()
    for m, lab in marks:
        flag(cr, t, m * PX, lab)


def flag(cr, t, x, label):
    stroke_line(cr, [(x, GROUND + 20), (x, GROUND - 230)], 8, OUTLINE, curve=False)
    stroke_line(cr, [(x, GROUND + 20), (x, GROUND - 230)], 4, hexc("#f4efe4"), curve=False)
    wv = math.sin(t * 5 + x * 0.01) * 6
    smooth(cr, [(x, GROUND - 228), (x + 120, GROUND - 214 + wv), (x + 120, GROUND - 160 + wv), (x, GROUND - 170)])
    paint(cr, lin(x, 0, x + 120, 0, [(0, GOLD), (1, shade(GOLD, -0.2))]), OUTLINE, 4)
    bold_text(cr, label, x + 58, GROUND - 180 + wv * 0.5, 30, WHITE, ow=6, shadow=0)


def studio(cr, t, top, bottom, seed=1):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, top), (1, bottom)]))
    cr.fill()
    bokeh(cr, t, seed, 14, [WHITE, hexc("#ffe7a8")], rmin=20, rmax=70)


# ---------------------------------------------------------------- props and UI
def scroll_prop(cr, hx, hy):
    cr.save()
    cr.translate(hx + 10, hy - 30)
    cr.rotate(-0.2)
    rrect(cr, -18, -60, 70, 120, 8)
    paint(cr, lin(0, -60, 0, 60, [(0, hexc("#fff6dc")), (1, hexc("#e8d6a8"))]), OUTLINE, 4)
    for k in range(4):
        stroke_line(cr, [(-6, -36 + k * 22), (40, -36 + k * 22)], 3, alpha(OUTLINE, 0.4), curve=False)
    for yy in (-60, 60):
        ellipse(cr, 17, yy, 42, 10)
        paint(cr, hexc("#c9a46a"), OUTLINE, 4)
    cr.restore()


def tag(cr, t, start, x, y, text, col=GOLD, size=40, end=None):
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.3)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 4) * 4)
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, col)
    cr.move_to(-12, 12)
    cr.line_to(12, 12)
    cr.line_to(0, 30)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    cr.restore()


def stopwatch(cr, t, x, y, secs, s=1.0, col=GOLD):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, 10, 84, (0, 0, 0, 0.3))
    rrect(cr, -16, -100, 32, 24, 6)
    paint(cr, hexc("#5a6478"), OUTLINE, 4)
    cr.arc(0, 0, 78, 0, 2 * math.pi)
    paint(cr, rad(-20, -30, 100, [(0, WHITE), (1, hexc("#dfe6ee"))]), OUTLINE, 6)
    cr.arc(0, 0, 66, -math.pi / 2, -math.pi / 2 + 2 * math.pi * ((secs % 60) / 60.0) + 1e-3)
    cr.line_to(0, 0)
    cr.close_path()
    cr.set_source_rgba(*alpha(col, 0.35))
    cr.fill()
    txt = f"{secs:.0f} s" if abs(secs - round(secs)) < 0.05 or secs >= 12 else f"{secs:.1f} s"
    bold_text(cr, txt, 0, 18, 46, OUTLINE, outline=None, shadow=0)
    cr.restore()


def bracket(cr, t, start, xa, xb, y, label, col=GOLD, size=40):
    """A measuring bracket between two world x positions (call inside the camera transform)."""
    if t < start:
        return
    k = appear(t, start, 0.35)
    if k <= 0.01:
        return
    xm = (xa + xb) / 2
    w = (xb - xa) * k
    for lw, c in ((12, OUTLINE), (6, col)):
        stroke_line(cr, [(xm - w / 2, y + 18), (xm - w / 2, y), (xm + w / 2, y), (xm + w / 2, y + 18)], lw, c,
                    curve=False)
    cr.save()
    cr.translate(xm, y - 18)
    cr.scale(k, k)
    bold_text(cr, label, 0, 0, size, col)
    cr.restore()


def buttons(cr, t, start, labels, y=700):
    if t < start:
        return
    for k, (lab, col) in enumerate(labels):
        x = 200 if k == 0 else 520
        kk = appear(t, start + k * 0.12)
        if kk <= 0.01:
            continue
        cr.save()
        cr.translate(x, y)
        cr.scale(kk, kk)
        soft_rrect(cr, -130, -42, 260, 92, 46, (0, 0, 0, 0.3), sigma=10)
        rrect(cr, -130, -50, 260, 92, 46)
        paint(cr, lin(0, -50, 0, 42, [(0, shade(col, 0.3)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, lab, 0, 14, 46, WHITE)
        cr.restore()
    cue("pop", t, start)


# ---------------------------------------------------------------- the race
def race_clock(tl, t):
    """Race time (seconds) driven by the narration."""
    A = tl.at
    tau = 0.0
    tau += 10.0 * seg(t, A("a5", "runs"), A("a5", "seconds.", end=True))
    tau += 1.0 * seg(t, A("a7", "runs"), A("a7", "second.", end=True))
    if t >= A("a14"):
        lv = A("a14", "level.")
        tau = 11.0 + (100 / 9 - 11.0) * seg(t, A("a14", "Achilles"), lv)
        tau += 3.0 * ease_out(seg(t, A("a14", "zooms"), A("a14", "past.", end=True) + 0.6))
    return tau


def draw_runners(cr, t, tl, tau, head_start=1.0, achilles_kw=None, tortoise_kw=None):
    a_pos = 10.0 * tau                  # Achilles' front foot (m)
    p_pos = 100.0 * head_start + tau    # the tortoise's tail (m)
    moving_a = tl.at("a5", "runs") <= t <= tl.at("a5", "seconds.", end=True) or \
        tl.at("a7", "runs") <= t <= tl.at("a7", "second.", end=True) or \
        (t >= tl.at("a14", "zooms") and t <= tl.at("a14", "past.", end=True) + 0.6)
    tx = p_pos * PX + 150 * TORT_S
    tkw = dict(eyes="half", mouth="smug", headband=True)
    tkw.update(tortoise_kw or {})
    tortoise(cr, t, tx, GROUND, TORT_S, walk=t * 6 if (moving_a or head_start < 1) else None, **tkw)
    ax = a_pos * PX - 46 * HERO_S
    akw = dict(eyes="angry" if moving_a else "open", mouth="grin" if moving_a else "smile",
               arms=("fist", "down") if moving_a else ("hips", "hips"), brows="angry" if moving_a else None)
    akw.update(achilles_kw or {})
    person(cr, t, ax, GROUND, HERO_S, "achilles", walk=t * 16 if moving_a else None, run=moving_a,
           tilt=0.15 if moving_a else 0.0, **akw)
    if moving_a:   # speed lines
        for k in range(4):
            y = GROUND - 120 - k * 70
            ln = 80 + 40 * ((t * 7 + k) % 1)
            stroke_line(cr, [(ax - 120 - ln, y), (ax - 120, y)], 6, alpha(WHITE, 0.8), curve=False)


def cam_y(z, screen_ground=800):
    return GROUND - (screen_ground - H / 2) / z


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    cam = camera(t, [(0, (1.25, 390, cam_y(1.25, 830))), (A("a1", "never"), (1.38, 400, cam_y(1.38, 830)))], dur=1.0)
    stadium(cr, t, cam)
    cr.save()
    enter(cr, cam)
    track(cr, t)
    runs = (t * 1.6) % 1.0
    person(cr, t, 210, GROUND, HERO_S, "achilles", walk=t * 16, run=True, tilt=0.15, eyes="angry",
           mouth="grin" if t < A("a1", "never") else "o", brows="angry", arms=("fist", "down"))
    for k in range(4):
        y = GROUND - 120 - k * 70
        ln = 80 + 40 * ((t * 7 + k) % 1)
        stroke_line(cr, [(90 - ln, y), (90, y)], 6, alpha(WHITE, 0.8), curve=False)
    tortoise(cr, t, 560, GROUND, TORT_S, walk=t * 6, eyes="half", mouth="smug", headband=True)
    cr.restore()
    sign(cr, t, 0.05, 360, 200, "FASTEST RUNNER ALIVE", col=RED, size=48, end=A("a1", "never") - 0.05)
    sign(cr, t, A("a1", "never"), 360, 200, "CAN'T CATCH", col=RED, size=62, sub="A TORTOISE?!", sub_col=WHITE)
    stamp(cr, t, A("a1", "tortoise."), 360, 400, "IMPOSSIBLE?", col=PURPLE, size=70, rot=-0.08)
    vignette(cr, 0.4)


def scene_intro(cr, t, tl):
    A = tl.at
    ach = A("a2", "Achilles,")
    cam = camera(t, [(A("a2") - 0.3, (1.0, 365, cam_y(1.0, 850))), (ach, (1.06, 380, cam_y(1.06, 850)))],
                 dur=0.7)
    stadium(cr, t, cam)
    cr.save()
    enter(cr, cam)
    track(cr, t)
    person(cr, t, 210, GROUND, 0.92, "zeno", eyes="half" if t < ach else "happy", mouth="smug",
           arms=("hold", "think"), hold=scroll_prop, look=(0.4, 0))
    person(cr, t, 520, GROUND, 0.92, "achilles", eyes="happy" if t >= A("a2", "fastest") else "open", mouth="grin",
           arms=("fist", "fist") if t >= A("a2", "fastest") else ("hips", "hips"), facing=-1)
    cr.restore()
    tag(cr, t, A("a2", "Zeno."), 205, 330, "ZENO", col=hexc("#9fc8ff"), end=ach - 0.05)
    tag(cr, t, ach, 530, 330, "ACHILLES", col=RED)
    sign(cr, t, A("a2", "fastest"), 360, 180, "FASTEST HERO", col=GOLD, size=60, sub="IN GREEK STORIES",
         sub_col=WHITE)
    vignette(cr, 0.4)


def speed_card(cr, t, start, x, y, who, big, sub, col):
    if t < start:
        return
    k = appear(t, start, 0.4)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 2 + x) * 4)
    cr.scale(k, k)
    soft_rrect(cr, -150, -190, 300, 400, 30, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -150, -200, 300, 400, 30)
    paint(cr, lin(0, -200, 0, 200, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    cr.save()
    rrect(cr, -150, -200, 300, 400, 30)
    cr.clip()
    cr.rectangle(-150, -200, 300, 210)
    cr.set_source(lin(0, -200, 0, 10, [(0, shade(col, 0.35)), (1, col)]))
    cr.fill()
    if who == "achilles":
        person(cr, t, 0, 60, 0.42, "achilles", walk=t * 16, run=True, tilt=0.15, eyes="angry", mouth="grin",
               arms=("fist", "down"), shadow=False)
    else:
        tortoise(cr, t, 0, -10, 0.55, walk=t * 6, eyes="half", mouth="smug", headband=True, shadow=False)
    cr.restore()
    bold_text(cr, big, 0, 110, 76, OUTLINE, outline=None, shadow=0)
    bold_text(cr, sub, 0, 160, 30, shade(col, -0.3), font="Fredoka", outline=None, shadow=0)
    cr.restore()


def scene_rules(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=2)
    sign(cr, t, A("a3"), 360, 200, "THE RACE", col=GOLD, size=72)
    speed_card(cr, t, A("a3", "10"), 190, 560, "achilles", "10 m", "EVERY SECOND", RED)
    speed_card(cr, t, A("a3", "tortoise"), 530, 560, "tortoise", "1 m", "EVERY SECOND", GREEN)
    vignette(cr, 0.35)


def scene_race(cr, t, tl):
    A = tl.at
    a4, a5, a6, a7, a8 = (A(k) for k in ("a4", "a5", "a6", "a7", "a8"))
    keys = [(a4 - 0.3, (0.64, 540, cam_y(0.64, 820))),
            (a6, (1.05, 1060, cam_y(1.05, 840))),
            (A("a7", "runs"), (1.05, 1090, cam_y(1.05, 840))),
            (a8, (1.45, 1105, cam_y(1.45, 870)))]
    cam = camera(t, keys, dur=0.8)
    stadium(cr, t, cam)
    tau = race_clock(tl, t)
    head = ease_out(seg(t, A("a4", "100"), A("a4", "start.", end=True))) if t < a5 else 1.0
    cr.save()
    enter(cr, cam)
    marks = [(0, "0 m")]
    if t >= A("a4", "100"):
        marks.append((100, "100 m"))
    if t >= A("a6", "10", nth=2):
        marks.append((110, "110 m"))
    if t >= a8:
        marks.append((111, "111"))
    track(cr, t, marks=marks)
    surprised = t >= a6 or (t >= A("a7", "second.", end=True))
    draw_runners(cr, t, tl, tau, head, achilles_kw=dict(eyes="wide", mouth="o", arms=("face", "down"),
                                                       brows="up") if (a6 <= t < A("a7", "runs") or t >= a8) else None)
    if a6 <= t < A("a7", "runs"):
        bracket(cr, t, A("a6", "10", nth=2), 1000, 1100, GROUND - 330, "10 m")
    if t >= a8:
        bracket(cr, t, A("a8", "one"), 1100, 1110, GROUND - 250, "1 m", size=30)
    cr.restore()
    stopwatch(cr, t, 600, 360, tau, 0.8)
    sign(cr, t, A("a4", "100"), 300, 200, "100 m HEAD START", col=GREEN, size=50, end=a5 - 0.05)
    sign(cr, t, a5, 300, 200, "10 SECONDS...", col=RED, size=56, end=A("a6", "still") - 0.05)
    sign(cr, t, A("a6", "still"), 300, 200, "STILL AHEAD!", col=GOLD, size=60, end=a7 - 0.05)
    sign(cr, t, a7, 300, 200, "1 SECOND...", col=RED, size=60, end=A("a8", "Still") - 0.05)
    sign(cr, t, A("a8", "Still"), 300, 200, "STILL AHEAD!", col=GOLD, size=60)
    vignette(cr, 0.4)


STEPS = [("100 m", "Every"), ("10 m", "reaches"), ("1 m", "tortoise"), ("0.1 m", "moved"), ("0.01 m", "little"),
         ("...", "further.")]


def scene_steps(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd6a8"), hexc("#fff1d6"), seed=5)
    a10 = A("a10")
    fade = 1 - seg(t, a10 + 0.2, a10 + 0.6)
    if fade > 0:
        cr.push_group()
        y = 300
        for k, (lab, key) in enumerate(STEPS):    # a staircase of ever-smaller steps
            st = A("a9", key)
            if t < st:
                continue
            kk = appear(t, st, 0.3)
            w = 420 * (0.6 ** k)
            h = max(16, 58 * (0.8 ** k))
            cr.save()
            cr.translate(70, y)
            cr.scale(1, max(kk, 0.01))
            if lab != "...":
                rrect(cr, 0, -h / 2, max(w, 8), h, min(14, h / 2))
                paint(cr, lin(0, -h / 2, 0, h / 2, [(0, shade(RED, 0.3)), (1, shade(RED, -0.15))]), OUTLINE, 5)
            bold_text(cr, lab, (max(w, 8) + 22) if lab != "..." else 0, 15, 44, WHITE, font="Fredoka",
                      align="left")
            cr.restore()
            y += h + 22
        cr.pop_group_to_source()
        cr.paint_with_alpha(fade)
    person(cr, t, 190, 870, 0.45, "achilles", eyes="half" if t >= a10 else "open",
           mouth="sad" if t >= a10 else "flat", arms=("down", "down"), sweat=t >= a10, brows="sad")
    tortoise(cr, t, 520, 870, 0.45, eyes="half", mouth="smug", headband=True)
    sign(cr, t, A("a9"), 360, 160, "THE GAP SHRINKS...", col=RED, size=54, end=a10 - 0.05)
    sign(cr, t, a10, 360, 160, "ENDLESS STEPS", col=PURPLE, size=64)
    portrait(cr, t, A("a10", "So"), 360, 420, 120, "zeno", mouth="smug", eyes="half", bg=hexc("#9fc8ff"))
    stamp(cr, t, A("a10", "never", nth=2), 360, 620, "NEVER CATCHES IT", col=RED, size=56)
    vignette(cr, 0.35)


def sum_line(cr, t, start, y, text, col=WHITE, size=64):
    if t < start:
        return
    k = appear(t, start, 0.3)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(560, y)
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, col, font="Fredoka", outline=None, shadow=0.12, align="right")
    cr.restore()


def scene_math(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#b8a8ff"), hexc("#fff1d6"), seed=7)
    a12, a13 = A("a12"), A("a13")
    if t < a12:
        sign(cr, t, A("a11", "trick."), 360, 230, "THE TRICK:", col=GOLD, size=70, end=A("a11", "Add") - 0.05)
        sign(cr, t, A("a11", "Add"), 360, 230, "ADD UP THE TIMES", col=GREEN, size=56)
        person(cr, t, 360, 840, 0.9, "zeno", eyes="wide" if t >= A("a11", "trick.") else "half",
               mouth="o" if t >= A("a11", "trick.") else "smug", arms=("chin", "down"), brows="up")
        return vignette(cr, 0.35)
    # the sum, line by line, and the running total
    soft_rrect(cr, 120, 160, 480, 500, 30, (0, 0, 0, 0.25), sigma=12)
    rrect(cr, 120, 150, 480, 500, 30)
    paint(cr, lin(0, 150, 0, 650, [(0, hexc("#ffffff")), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    items = [("10 s", "10"), ("+ 1 s", "one."), ("+ 0.1 s", "tenth."), ("+ 0.01 s", "hundredth.")]
    total = 0.0
    for k, (lab, key) in enumerate(items):
        st = A("a12", key)
        if t >= st:
            total = (10, 11, 11.1, 11.11)[k]
            cue("pop", t, st)
        sum_line(cr, t, st, 260 + k * 82, lab, OUTLINE if k else RED, 66)
    sum_line(cr, t, A("a12", "hundredth.") + 0.4, 590, "+ ...", alpha(OUTLINE, 0.6), 56)
    if t >= a13:
        crawl = 11.11 + 0.0011 * (1 - math.exp(-(t - a13) * 1.5))
        total = crawl
    if t >= a12:
        txt = f"{total:.2f}" if t < a13 else f"{total:.4f}"
        bold_text(cr, f"= {txt} s", 360, 740, 80, GOLD, font="Fredoka")
    if t >= a13:    # progress bar that never reaches the 11.2 line
        x0, x1, y = 90, 630, 820
        k = appear(t, a13, 0.3)
        rrect(cr, x0, y - 22, (x1 - x0) * k, 44, 22)
        paint(cr, alpha(WHITE, 0.6), OUTLINE, 5)
        fill = (total - 10) / 1.2
        rrect(cr, x0 + 4, y - 18, max(1, (x1 - x0 - 8) * fill * k), 36, 18)
        paint(cr, lin(x0, 0, x1, 0, [(0, GREEN), (1, shade(GREEN, 0.3))]), None, 0)
        lx = x0 + (x1 - x0) * (1.2 / 1.2) - 4
        stroke_line(cr, [(lx, y - 46), (lx, y + 46)], 8, RED, curve=False)
        bold_text(cr, "11.2", lx - 12, y - 52, 40, RED, font="Fredoka", ow=7, align="right")
    sign(cr, t, A("a13", "never"), 360, 100, "NEVER REACHES 11.2", col=RED, size=48)
    vignette(cr, 0.35)


def scene_pass(cr, t, tl):
    A = tl.at
    lv = A("a14", "level.")
    zoom = A("a14", "zooms")
    cam = camera(t, [(A("a14") - 0.3, (1.05, 1110, cam_y(1.05))), (zoom, (0.85, 1250, cam_y(0.85)))], dur=0.8)
    stadium(cr, t, cam)
    tau = race_clock(tl, t)
    cr.save()
    enter(cr, cam)
    track(cr, t, marks=[(100, "100 m"), (111.1, "111.1")])
    passed = t >= zoom
    draw_runners(cr, t, tl, tau, 1.0,
                 tortoise_kw=dict(eyes="wide", mouth="o", headband=not passed) if passed else None)
    if passed:   # the headband flies off
        u = seg(t, zoom, zoom + 1.2)
        hx = (100 + tau) * PX + 150 * TORT_S + 100 - 300 * u
        hy = GROUND - 200 - 260 * math.sin(u * math.pi)
        cr.save()
        cr.translate(hx, hy)
        cr.rotate(u * 9)
        rrect(cr, -50, -9, 100, 18, 8)
        paint(cr, RED, OUTLINE, 4)
        cr.restore()
    cr.restore()
    stopwatch(cr, t, 600, 360, tau, 0.8)
    sign(cr, t, A("a14", "11"), 300, 200, "ABOUT 11.1 SEC", col=GOLD, size=54, end=lv - 0.05)
    sign(cr, t, lv, 300, 200, "LEVEL!", col=GREEN, size=72, end=zoom - 0.05)
    stamp(cr, t, zoom, 330, 230, "ZOOM!", col=RED, size=96)
    vignette(cr, 0.4)


def scene_summary(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=9)
    for k, (st, big, sub, col) in enumerate(((A("a15"), "ENDLESS", "STEPS", PURPLE),
                                             (A("a15", "short"), "SHORT", "RACE", GREEN))):
        if t < st:
            continue
        kk = appear(t, st, 0.4)
        x = 190 + 340 * k
        cr.save()
        cr.translate(x, 480 + math.sin(t * 2 + k) * 5)
        cr.scale(kk, kk)
        soft_rrect(cr, -150, -170, 300, 340, 30, (0, 0, 0, 0.3), sigma=12)
        rrect(cr, -150, -180, 300, 340, 30)
        paint(cr, lin(0, -180, 0, 160, [(0, shade(col, 0.35)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, big, 0, -10, 60, WHITE)
        bold_text(cr, sub, 0, 70, 52, GOLD)
        cr.restore()
    if t >= A("a15", "short"):
        stopwatch(cr, t, 530, 760, 100 / 9, 0.7, GREEN)
    sign(cr, t, A("a15", "But"), 360, 180, "BUT", col=GOLD, size=60)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    cam = (1.0, 400, cam_y(1.0, 830))
    stadium(cr, t, cam)
    cr.save()
    enter(cr, cam)
    track(cr, t)
    person(cr, t, 200, GROUND, 0.75, "zeno", eyes="half", mouth="smug", arms=("hold", "think"), hold=scroll_prop)
    tortoise(cr, t, 560, GROUND, 0.55, eyes="happy", mouth="grin", headband=True)
    cr.restore()
    sign(cr, t, A("a16"), 360, 190, "DID ZENO FOOL YOU?", col=PURPLE, size=52)
    buttons(cr, t, A("a16", "Yes,"), (("YES", GREEN), ("NO", RED)), y=380)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "intro": scene_intro, "rules": scene_rules, "race": scene_race, "steps": scene_steps,
          "math": scene_math, "pass": scene_pass, "summary": scene_summary, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
