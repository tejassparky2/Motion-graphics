"""Funny history: "1835 News: Bat-People Found on the Moon" -- the Great Moon Hoax, in the owner's reference narration
style (Abhay Create: talks to the viewer, "bro", modern comparisons, big set-up / flat landing).

Script: out/scripts_batch_oct26-31.md, row 61 (owner approved 18 Oct 2026). The Sun (New York) ran six articles from
25 August 1835 crediting Sir John Herschel, then observing at the Cape of Good Hope, with seeing man-bats
("Vespertilio-homo"), unicorns and two-legged beavers on the moon through a huge new telescope; the paper's sales
jumped. The writer is usually said to be Richard Adams Locke, so the script only says "a writer". Turbo voice with
tags (narrator only, stock female voice).
"""
import math
import random

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, ellipse, enter, lin,
                           paint, rad, rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.9
PAPER = hexc("#f2ead6")
INK = hexc("#2b2622")

SCRIPT = [
    dict(id="h1", scene="paper", text="[Eighteen thirty-five.|1835.] A New York newspaper prints the biggest news in "
                                      "history. There is life. On the moon."),
    dict(id="h2", scene="moon", text="And not just germs, bro. Unicorns. Beavers walking on two legs. And people. With "
                                     "bat wings. [laugh]"),
    dict(id="h3", scene="scope", text="Who found them? A famous astronomer, with a giant new telescope. Very "
                                      "scientific. Very serious."),
    dict(id="h4", scene="crowd", text="New York goes crazy. Everyone wants a copy. The paper is selling faster than it "
                                      "can print."),
    dict(id="h5", scene="africa", text="Just one tiny problem. The astronomer was real. But he was busy in South "
                                       "Africa, and had no idea any of this was printed in his name. [chuckle]"),
    dict(id="h6", scene="office", text="The whole thing was made up. In an office. Bat-people. Invented by a writer "
                                       "with a deadline."),
    dict(id="h7", scene="click", text="Bro invented clickbait almost two hundred years ago. Before the internet. "
                                      "Before the light bulb."),
    dict(id="h8", scene="name", text="Today it's called the Great Moon Hoax."),
    dict(id="h9", scene="end", text="So who's really to blame for fake news? The people who make it, or the people "
                                    "who share it?", gap=0.5),
]

METADATA = dict(
    title="1835 News: Bat-People Found on the Moon 🌙",
    alt_titles=["The Newspaper That Found Unicorns on the Moon (1835) 🌙", "Clickbait Is 190 Years Old 🦇🌙"],
    description="""1835: a New York newspaper prints the biggest news in history. There is life on the moon. 🌙

Unicorns. Beavers walking on two legs. And people... with bat wings. 🦇 All "seen" by a famous astronomer through a giant new telescope. New York went crazy and the paper sold out.

One tiny problem: the astronomer (Sir John Herschel) was real, but he was busy in South Africa and had no idea any of it was printed in his name. The whole thing was made up in an office. Today it's called the Great Moon Hoax.

💬 Who's really to blame for fake news: the people who make it, or the people who share it? 👇

🔔 Interestingly Strange: funny history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FunnyHistory", "#FakeNews", "#Shorts"],
    tags=["great moon hoax", "moon hoax 1835", "bat people on the moon", "funny history", "fake news history",
          "the sun newspaper 1835", "john herschel", "weird history", "clickbait", "interestingly strange"],
    pinned_comment="Who's more to blame: the people who MAKE fake news 🖨️ or the people who SHARE it 📲? 👇",
)


# ---------------------------------------------------------------- props
def newspaper(cr, t, x, y, s=1.0, rot=0.0, headline="LIFE ON THE MOON!", art=True):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_disc(cr, 10, 20, 280, (0, 0, 0, 0.3))
    rrect(cr, -220, -300, 440, 600, 6)
    paint(cr, lin(0, -300, 0, 300, [(0, PAPER), (1, shade(PAPER, -0.08))]), OUTLINE, 6)
    bold_text(cr, "THE SUN", 0, -235, 54, INK, outline=None, shadow=0)
    stroke_line(cr, [(-190, -210), (190, -210)], 4, INK, curve=False)
    bold_text(cr, headline, 0, -150, 44 if len(headline) < 18 else 34, RED, outline=None, shadow=0)
    if art:
        rrect(cr, -170, -110, 340, 220, 4)
        paint(cr, hexc("#1c2240"), INK, 3)
        cr.arc(60, -20, 70, 0, 2 * math.pi)
        paint(cr, hexc("#f4efd8"), INK, 3)
        batperson(cr, t, -60, 60, 0.35)
    for k in range(6):
        stroke_line(cr, [(-180, 140 + k * 24), (180 - 40 * (k % 3), 140 + k * 24)], 4, alpha(INK, 0.35), curve=False)
    cr.restore()


def batperson(cr, t, x, y, s=1.0, flap=None, eyes="happy"):
    """A man-bat from the hoax: a little person with leathery wings. Feet at (x, y)."""
    f = math.sin(t * 9) if flap is None else flap
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for side in (-1, 1):
        cr.save()
        cr.translate(side * 50, -300)
        cr.rotate(side * (0.25 + 0.25 * f))
        cr.move_to(0, 0)
        cr.curve_to(side * 120, -110, side * 230, -60, side * 260, 30)
        cr.curve_to(side * 200, 10, side * 180, 60, side * 130, 50)
        cr.curve_to(side * 100, 90, side * 60, 80, 0, 90)
        cr.close_path()
        paint(cr, hexc("#8a5a6a"), OUTLINE, 5)
        cr.restore()
    cr.restore()
    person(cr, t, x, y, s, "kid", eyes=eyes, mouth="grin", arms=("wave", "down"), shirt=hexc("#c8a080"),
           pants=hexc("#8a5a6a"), tie=None, hair="curly", hair_col=hexc("#5a3a2a"), shadow=False)


def unicorn(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y - 6 * abs(math.sin(t * 4)) * s)
    cr.scale(s, s)
    for lx in (-50, -25, 25, 50):
        stroke_line(cr, [(lx, -60), (lx, 0)], 14, OUTLINE, curve=False)
        stroke_line(cr, [(lx, -60), (lx, -4)], 9, hexc("#f4f0ff"), curve=False)
    ellipse(cr, 0, -90, 80, 45)
    paint(cr, hexc("#f4f0ff"), OUTLINE, 5)
    ellipse(cr, 80, -150, 36, 30)
    paint(cr, hexc("#f4f0ff"), OUTLINE, 5)
    cr.move_to(88, -176)
    cr.line_to(100, -240)
    cr.line_to(108, -172)
    cr.close_path()
    paint(cr, GOLD, OUTLINE, 4)
    cr.arc(90, -150, 5, 0, 2 * math.pi)
    paint(cr, OUTLINE, None)
    for k in range(3):
        ellipse(cr, 40 - k * 16, -140 + k * 8, 14, 24)
        paint(cr, (hexc("#ff7ab8"), hexc("#7fd0ff"), GOLD)[k], OUTLINE, 3)
    cr.restore()


def beaver(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, -30, -30, 50, 18)                                   # tail
    paint(cr, hexc("#5a3a2a"), OUTLINE, 4)
    wob = 6 * math.sin(t * 8)
    for lx in (-14, 14):
        stroke_line(cr, [(lx, -60), (lx + (wob if lx > 0 else -wob), 0)], 12, OUTLINE, curve=False)
        stroke_line(cr, [(lx, -60), (lx + (wob if lx > 0 else -wob), -4)], 7, hexc("#8a5a3a"), curve=False)
    ellipse(cr, 0, -110, 40, 58)
    paint(cr, hexc("#a8703e"), OUTLINE, 5)
    ellipse(cr, 0, -180, 32, 28)
    paint(cr, hexc("#a8703e"), OUTLINE, 5)
    rrect(cr, -9, -164, 18, 16, 3)
    paint(cr, WHITE, OUTLINE, 3)
    for ex in (-12, 12):
        cr.arc(ex, -188, 5, 0, 2 * math.pi)
        paint(cr, OUTLINE, None)
    rrect(cr, -30, -250, 60, 34, 6)                                 # a tiny top hat
    paint(cr, hexc("#2b2b33"), OUTLINE, 4)
    cr.restore()


def moon_ground(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#0c1028")), (0.7, hexc("#1f2450"))]))
    cr.fill()
    rng = random.Random(7)
    for _ in range(60):
        x, y = rng.random() * W, rng.random() * 700
        cr.arc(x, y, 1 + rng.random() * 2.5, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.4 + 0.4 * math.sin(t * 3 + x))
        cr.fill()
    soft_disc(cr, 560, 200, 90, (0.5, 0.7, 1.0, 0.5))               # Earth in the sky
    cr.arc(560, 200, 60, 0, 2 * math.pi)
    paint(cr, rad(540, 180, 80, [(0, hexc("#7fd0ff")), (1, hexc("#2f6ab0"))]), OUTLINE, 4)
    cr.rectangle(0, 860, W, H - 860)
    cr.set_source(lin(0, 860, 0, H, [(0, hexc("#c8c8d0")), (1, hexc("#8a8a98"))]))
    cr.fill()
    for (cx, cy, r) in ((120, 950, 50), (480, 1000, 70), (640, 900, 30)):
        ellipse(cr, cx, cy, r, r * 0.35)
        paint(cr, hexc("#9a9aa8"), alpha(OUTLINE, 0.4), 3)


def telescope(cr, x, y, s=1.0, rot=-0.6):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for lx in (-60, 60):
        stroke_line(cr, [(0, -120), (lx, 0)], 10, OUTLINE, curve=False)
    cr.translate(0, -130)
    cr.rotate(rot)
    rrect(cr, -40, -36, 420, 72, 20)
    paint(cr, lin(0, -36, 0, 36, [(0, hexc("#e8c070")), (1, hexc("#a87a30"))]), OUTLINE, 6)
    rrect(cr, 360, -50, 60, 100, 14)
    paint(cr, hexc("#c89a40"), OUTLINE, 6)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_paper(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a2a1a"), hexc("#6a4a2a"), seed=2)
    spin = 1 - ease_out(seg(t, 0.0, 0.6))                            # the paper spins in from frame 0
    newspaper(cr, t, 360, 600, 0.95 - 0.3 * spin, rot=spin * 3.0)
    if t >= A("h1", "moon."):
        stamp(cr, t, A("h1", "moon."), 360, 640, "BREAKING NEWS", col=RED, size=56)
        cue("hit", t, A("h1", "moon."))
    vignette(cr, 0.5)


def scene_moon(cr, t, tl):
    A = tl.at
    moon_ground(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h2") - 0.3, (1.0, 360, 640)), (A("h2", "people."), (1.15, 360, 640))]))
    if t >= A("h2", "Unicorns."):
        unicorn(cr, t, lerp(-150, 160, ease_out(seg(t, A("h2", "Unicorns."), A("h2", "Unicorns.") + 0.6))), 930, 0.9)
    if t >= A("h2", "Beavers"):
        beaver(cr, t, lerp(820, 560, ease_out(seg(t, A("h2", "Beavers"), A("h2", "Beavers") + 0.6))), 960, 1.0)
    if t >= A("h2", "people."):
        k = appear(t, A("h2", "people."), 0.5)
        batperson(cr, t, 360, 620 + 40 * math.sin(t * 2), 0.75 * k)
    cr.restore()
    sign(cr, t, A("h2", "germs,"), 360, 170, "NOT JUST GERMS", col=PURPLE, size=56, end=A("h2", "Unicorns.") - 0.05)
    sign(cr, t, A("h2", "wings."), 360, 170, "BAT-PEOPLE", col=RED, size=76)
    vignette(cr, 0.45)


def scene_scope(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#0c1028"), hexc("#2a2f5a"), seed=4)
    telescope(cr, 300, 1000, 1.1)
    person(cr, t, 170, 1000, 0.85, "franklin", eyes="half", mouth="smug", arms=("chin", "point"), brows="raise")
    sign(cr, t, A("h3", "giant"), 360, 170, "GIANT TELESCOPE", col=GOLD, size=60, end=A("h3", "Very") - 0.05)
    sign(cr, t, A("h3", "scientific."), 360, 170, "VERY SCIENTIFIC", col=BLUE, size=60, end=A("h3", "serious.") - 0.05)
    sign(cr, t, A("h3", "serious."), 360, 170, "VERY SERIOUS", col=PURPLE, size=64)
    vignette(cr, 0.45)


def scene_crowd(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#c8b898"), hexc("#f2e6c8"), seed=5)
    cr.save()
    enter(cr, camera(t, [(A("h4") - 0.3, (1.0, 360, 640)), (A("h4", "faster"), (1.1, 360, 600))]))
    for k in range(7):
        x = 70 + k * 100
        person(cr, t, x, 1000 - (k % 2) * 30, 0.5, ("reporter", "kid", "teacher", "sir", "student1", "dad",
                                                     "cousin")[k], eyes="wide", mouth="o", arms=("up", "up"),
               seed=k, walk=t * 10 + k)
    for k in range(8):                                               # papers flying out of the press
        ph = (t * 1.1 + k * 0.125) % 1
        newspaper(cr, t, 360 + (k - 3.5) * 70 * ph, 520 - 300 * ph, 0.18, rot=ph * 4 + k, art=False)
    cr.restore()
    sign(cr, t, A("h4", "crazy."), 360, 170, "SOLD OUT", col=RED, size=76)
    vignette(cr, 0.35)


def scene_africa(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffb86a"), hexc("#ffe7a8"), seed=6)
    cr.arc(560, 260, 80, 0, 2 * math.pi)                             # big sun
    paint(cr, hexc("#ffe066"), OUTLINE, 5)
    telescope(cr, 470, 1000, 0.8, rot=-0.9)
    oblivious = t >= A("h5", "idea")
    person(cr, t, 300, 1000, 0.95, "franklin", eyes="happy" if oblivious else "open", mouth="smile",
           arms=("hips", "chin"))
    sign(cr, t, A("h5", "real."), 360, 170, "REAL ASTRONOMER", col=GREEN, size=56, end=A("h5", "busy") - 0.05)
    sign(cr, t, A("h5", "South"), 360, 170, "IN SOUTH AFRICA", col=GOLD, size=60, end=A("h5", "idea") - 0.05)
    if oblivious:
        bold_text(cr, "?", 300 + 70, 440, 90, PURPLE)
        sign(cr, t, A("h5", "idea"), 360, 170, "NO IDEA", col=RED, size=76)
    vignette(cr, 0.35)


def scene_office(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#3a3028")), (1, hexc("#5a4a3a"))]))
    cr.fill()
    soft_disc(cr, 360, 560, 360, (1, 0.85, 0.5, 0.25))              # lamp glow
    rrect(cr, 120, 760, 480, 40, 8)                                  # desk
    paint(cr, hexc("#7a4a2a"), OUTLINE, 6)
    person(cr, t, 360, 1000, 0.95, "reporter", eyes="half", mouth="smug", arms=("write", "write"))
    if t >= A("h6", "Bat-people."):
        rrect(cr, 380, 640, 180, 120, 6)                             # his doodle of a bat-person
        paint(cr, PAPER, OUTLINE, 4)
        batperson(cr, t, 470, 750, 0.18, flap=0.3)
    if t >= A("h6", "deadline."):
        cr.save()
        cr.translate(160, 420)
        cr.arc(0, 0, 70, 0, 2 * math.pi)
        paint(cr, WHITE, OUTLINE, 5)
        a = t * 6
        stroke_line(cr, [(0, 0), (50 * math.cos(a), 50 * math.sin(a))], 6, RED, curve=False)
        cr.restore()
    sign(cr, t, A("h6", "made"), 360, 170, "MADE UP", col=RED, size=76, end=A("h6", "deadline.") - 0.05)
    sign(cr, t, A("h6", "deadline."), 360, 170, "DEADLINE: TONIGHT", col=GOLD, size=52)
    vignette(cr, 0.5)


def scene_click(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1a1a2e"), hexc("#3a2a5a"), seed=7)
    rrect(cr, 190, 300, 340, 560, 40)                                # a phone with a clickbait thumbnail
    paint(cr, hexc("#1e1e24"), OUTLINE, 6)
    rrect(cr, 215, 360, 290, 420, 12)
    paint(cr, hexc("#0c1028"), None)
    batperson(cr, t, 330, 700, 0.3)
    bold_text(cr, "YOU WON'T", 360, 420, 36, GOLD)
    bold_text(cr, "BELIEVE THIS", 360, 460, 36, GOLD)
    if t >= A("h7", "internet."):
        stamp(cr, t, A("h7", "internet."), 360, 600, "NO INTERNET", col=RED, size=50)
    if t >= A("h7", "bulb."):
        cr.save()                                                    # a light bulb, crossed out
        cr.translate(600, 330)
        cr.arc(0, 0, 40, 0, 2 * math.pi)
        paint(cr, hexc("#fff3a8"), OUTLINE, 5)
        stroke_line(cr, [(-50, -50), (50, 50)], 10, RED, curve=False)
        cr.restore()
    sign(cr, t, A("h7", "clickbait"), 360, 170, "CLICKBAIT: 1835", col=PURPLE, size=60)
    vignette(cr, 0.45)


def scene_name(cr, t, tl):
    A = tl.at
    moon_ground(cr, t)
    newspaper(cr, t, 360, 600, 0.9, rot=0.05)
    sign(cr, t, A("h8", "Great"), 360, 170, "THE GREAT MOON HOAX", col=GOLD, size=52)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    newspaper(cr, t, 190, 700, 0.42, rot=-0.08, headline="FAKE!")
    rrect(cr, 450, 520, 150, 260, 24)                               # a phone with a share arrow
    paint(cr, hexc("#1e1e24"), OUTLINE, 6)
    stroke_line(cr, [(490, 690), (560, 620)], 12, GREEN, curve=False)
    sign(cr, t, A("h9", "make"), 190, 420, "WHO MAKES IT", col=RED, size=40, rot=-0.06)
    sign(cr, t, A("h9", "share"), 530, 420, "WHO SHARES IT", col=BLUE, size=40, rot=0.05)
    sign(cr, t, A("h9"), 360, 190, "WHO'S TO BLAME?", col=GOLD, size=60)
    vignette(cr, 0.3)


SCENES = {"paper": scene_paper, "moon": scene_moon, "scope": scene_scope, "crowd": scene_crowd,
          "africa": scene_africa, "office": scene_office, "click": scene_click, "name": scene_name, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("1835 NEWS:", False), ("LIFE ON THE MOON", True)], end=tl.at("h2"), y=170, size=92)
    captions(cr, t, tl)
