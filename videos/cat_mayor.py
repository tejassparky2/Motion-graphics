"""Hook test H2 ("did you know"): "A Cat Was Mayor for 20 Years".

Script: out/scripts_hook_test.md, H2 (owner approved 15 Oct 2026). True: Stubbs, honorary mayor of Talkeetna, Alaska,
1997-2017 (widely reported, e.g. NPR, Anchorage Daily News); the write-in origin is town legend, so "the story goes".
Turbo voice with tags (narrator only).
"""
import math
import random

from motion import thriller as th
from motion.engine import W, H, cue, hexc, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           particles, rad, rrect, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.9
ORANGE = hexc("#f29a3a")

SCRIPT = [
    dict(id="b1", scene="office", text="Did you know a town in Alaska had a cat as its mayor? For twenty years."),
    dict(id="b2", scene="town", text="His name was Stubbs. The town is [Tal-keet-na.|Talkeetna.]"),
    dict(id="b3", scene="vote", text="The story goes, in [nineteen ninety-seven,|1997,] people didn't like the human "
                                     "candidates. So they voted for the cat."),
    dict(id="b4", scene="vote", text="It was honorary. But the town loved it."),
    dict(id="b5", scene="store", text="His office? A general store. His favourite drink? Water in a wine glass, mixed "
                                      "with catnip. [chuckle]"),
    dict(id="b6", scene="tourists", text="Tourists came from all over the world just to meet him."),
    dict(id="b7", scene="record", text="In twenty years, Stubbs never raised taxes. Never broke a promise. Never gave "
                                       "a single speech."),
    dict(id="b8", scene="record", text="Honestly? Better record than most politicians. [laugh]"),
    dict(id="b9", scene="end", text="If your town could pick any animal as mayor, which one would you vote for?",
         gap=0.3),
]

METADATA = dict(
    title="A Cat Was Mayor for 20 Years 🐱",
    alt_titles=["Did You Know a Cat Ran an Alaskan Town? 🐱", "This Town Voted for a Cat. He Stayed 20 Years."],
    description="""Did you know a town in Alaska had a cat as its mayor? For twenty years. 🐱

His name was Stubbs, the honorary mayor of Talkeetna, Alaska (1997-2017). The story goes that people didn't like the human candidates, so they voted for the cat.

His office: a general store. His favourite drink: water in a wine glass, mixed with catnip. Tourists came from all over the world to meet him.

In twenty years he never raised taxes, never broke a promise and never gave a single speech. 😂

💬 If your town could pick any animal as mayor, which one would you vote for? 👇

🔔 Interestingly Strange: weird history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#DidYouKnow", "#WeirdHistory", "#Shorts"],
    tags=["stubbs the cat", "cat mayor", "talkeetna alaska", "did you know", "weird history", "funny facts",
          "cats", "animal facts", "true story", "interestingly strange"],
    pinned_comment="My vote goes to a golden retriever. Free hugs for every citizen 🐶 Yours? 👇",
)


# ---------------------------------------------------------------- the mayor
def cat(cr, t, x, y, s=1.0, eyes="open", mouth="smile", tie=True, sit=True, blink=True, look=0.0):
    """Stubbs: a round orange tabby, sitting, feet at (x, y)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    sway = math.sin(t * 2.2) * 0.25
    stroke_line(cr, [(70, -40), (130, -90 + 30 * sway), (110, -170 + 40 * sway)], 30, OUTLINE)
    stroke_line(cr, [(70, -40), (130, -90 + 30 * sway), (110, -170 + 40 * sway)], 20, ORANGE)
    ellipse(cr, 0, -95, 95, 100)                                   # body
    paint(cr, rad(-30, -140, 160, [(0, hexc("#ffc27a")), (1, ORANGE)]), OUTLINE, 6)
    ellipse(cr, 0, -70, 55, 60)                                    # belly
    paint(cr, hexc("#fff1dc"), None)
    for side in (-1, 1):                                           # paws
        ellipse(cr, side * 40, -8, 30, 18)
        paint(cr, hexc("#fff1dc"), OUTLINE, 5)
    hy = -215
    for side in (-1, 1):                                           # ears
        cr.move_to(side * 30, hy - 60)
        cr.line_to(side * 80, hy - 120)
        cr.line_to(side * 88, hy - 40)
        cr.close_path()
        paint(cr, ORANGE, OUTLINE, 6)
        cr.move_to(side * 42, hy - 62)
        cr.line_to(side * 74, hy - 100)
        cr.line_to(side * 78, hy - 58)
        cr.close_path()
        paint(cr, hexc("#ff9fb0"), None)
    ellipse(cr, 0, hy, 98, 82)                                     # head
    paint(cr, rad(-30, hy - 40, 120, [(0, hexc("#ffc27a")), (1, ORANGE)]), OUTLINE, 6)
    for k in (-1, 0, 1):                                           # tabby stripes
        stroke_line(cr, [(k * 26, hy - 80), (k * 22, hy - 52)], 8, hexc("#c86b1f"), curve=False)
    closed = blink and (t * 0.7) % 3.1 < 0.12
    for side in (-1, 1):
        ex, ey = side * 36 + look * 8, hy - 8
        if eyes == "half" or closed:
            stroke_line(cr, [(ex - 16, ey), (ex + 16, ey)], 7, OUTLINE, curve=False)
        elif eyes == "happy":
            stroke_line(cr, [(ex - 16, ey + 4), (ex, ey - 10), (ex + 16, ey + 4)], 7, OUTLINE)
        else:
            ellipse(cr, ex, ey, 16, 19)
            paint(cr, hexc("#3a2a1a"), None)
            cr.arc(ex + 5, ey - 6, 5, 0, 2 * math.pi)
            paint(cr, WHITE, None)
    cr.move_to(-10, hy + 22)                                       # nose
    cr.line_to(10, hy + 22)
    cr.line_to(0, hy + 32)
    cr.close_path()
    paint(cr, hexc("#ff7a8a"), OUTLINE, 3)
    if mouth == "open":
        ellipse(cr, 0, hy + 48, 14, 12)
        paint(cr, hexc("#7a2a2a"), OUTLINE, 4)
    else:
        stroke_line(cr, [(-18, hy + 40), (0, hy + 34), (18, hy + 40)], 5, OUTLINE)
    for side in (-1, 1):                                           # whiskers
        for k in (-1, 0, 1):
            stroke_line(cr, [(side * 30, hy + 28 + k * 8), (side * 92, hy + 18 + k * 14)], 3, OUTLINE, curve=False)
    if tie:
        cr.move_to(-14, -170)
        cr.line_to(14, -170)
        cr.line_to(22, -100)
        cr.line_to(0, -82)
        cr.line_to(-22, -100)
        cr.close_path()
        paint(cr, RED, OUTLINE, 5)
    cr.restore()


def desk_office(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2f4a6e")), (1, hexc("#1d2f48"))]))
    cr.fill()
    rrect(cr, 120, 150, 480, 300, 16)                              # framed flag behind the desk
    paint(cr, lin(0, 150, 0, 450, [(0, hexc("#3a6ab0")), (1, hexc("#24497e"))]), OUTLINE, 8)
    for k in range(7):                                             # stars, Alaska-flag style
        cr.arc(220 + k * 45 + (40 if k == 6 else 0), 260 + (k == 6) * -60, 9 if k < 6 else 16, 0, 2 * math.pi)
        paint(cr, GOLD, None)


def scene_office(cr, t, tl):
    A = tl.at
    desk_office(cr, t)
    cam = camera(t, [(0.0, (1.0, 360, 640)), (A("b1", "twenty"), (1.15, 360, 600))], dur=1.0)
    cr.save()
    enter(cr, cam)
    cat(cr, t, 360, 760, 1.1, eyes="half" if t >= A("b1", "twenty") else "open")
    rrect(cr, 40, 740, 640, 300, 18)                               # the desk
    paint(cr, lin(0, 740, 0, 1040, [(0, hexc("#9a6a3a")), (1, hexc("#6a4424"))]), OUTLINE, 8)
    rrect(cr, 220, 690, 280, 80, 10)                               # nameplate
    paint(cr, GOLD, OUTLINE, 6)
    bold_text(cr, "MAYOR", 360, 748, 52, WHITE)
    cr.restore()
    vignette(cr, 0.4)


def scene_town(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#9fd0ff")), (0.55, hexc("#e8f4ff")), (0.56, WHITE),
                                   (1, hexc("#dbe8f4"))]))
    cr.fill()
    for k, (x, h) in enumerate(((120, 380), (360, 520), (600, 420))):   # mountains
        cr.move_to(x - 260, 700)
        cr.line_to(x, 700 - h)
        cr.line_to(x + 260, 700)
        cr.close_path()
        paint(cr, hexc("#8aa7c4"), OUTLINE, 6)
        cr.move_to(x - 70, 700 - h + 120)
        cr.line_to(x, 700 - h)
        cr.line_to(x + 70, 700 - h + 120)
        cr.close_path()
        paint(cr, WHITE, None)
    for k, (x, col) in enumerate(((140, hexc("#c8553a")), (330, hexc("#3a7ac8")), (530, hexc("#3aa86a")))):
        rrect(cr, x - 70, 720, 140, 130, 6)                            # little wooden houses
        paint(cr, col, OUTLINE, 6)
        cr.move_to(x - 85, 725)
        cr.line_to(x, 650)
        cr.line_to(x + 85, 725)
        cr.close_path()
        paint(cr, WHITE, OUTLINE, 6)
        rrect(cr, x - 20, 790, 40, 60, 4)
        paint(cr, hexc("#5a3a22"), OUTLINE, 4)
    particles(cr, t, 5, 60, (1, 1, 1, 0.9), r=(3, 7), speed=40)       # snow
    sign(cr, t, A("b2"), 360, 200, "STUBBS", col=ORANGE, size=80, end=A("b2", "town") - 0.05)
    sign(cr, t, A("b2", "town"), 360, 200, "TALKEETNA, ALASKA", col=BLUE, size=54)
    vignette(cr, 0.3)


def scene_vote(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe0b8"), hexc("#fff6e8"), seed=4)
    honor = t >= A("b4")
    rrect(cr, 210, 620, 300, 280, 14)                                 # ballot box
    paint(cr, lin(0, 620, 0, 900, [(0, hexc("#4a7ad0")), (1, hexc("#2a4a8a"))]), OUTLINE, 8)
    rrect(cr, 290, 610, 140, 22, 6)
    paint(cr, hexc("#1a2a4a"), OUTLINE, 5)
    bold_text(cr, "VOTE", 360, 790, 64, WHITE)
    for k, x in enumerate((120, 600)):                                # the human candidates, frowned at
        if t >= A("b3", "human"):
            person(cr, t, x, 1060, 0.45, "reporter", eyes="half", mouth="flat", seed=k)
            sign(cr, t, A("b3", "human"), x, 760, "NOPE", col=RED, size=40, sound="pop")
    for k in range(5):                                                # ballots dropping with paw prints
        st = A("b3", "voted") + 0.15 * k
        if t >= st:
            u = seg(t, st, st + 0.5)
            y = 380 + 230 * u
            rrect(cr, 330 + (k % 2) * 20 - 10, y, 60, 44, 4)
            paint(cr, WHITE, OUTLINE, 4)
            cr.arc(360 + (k % 2) * 20, y + 22, 10, 0, 2 * math.pi)
            paint(cr, ORANGE, None)
    if t >= A("b3", "cat."):
        cat(cr, t, 360, 600, 0.55, eyes="happy")
    sign(cr, t, A("b3", "nineteen"), 360, 200, "1997", col=PURPLE, size=80, end=A("b4") - 0.05)
    if honor:
        stamp(cr, t, A("b4", "honorary."), 360, 420, "HONORARY", col=RED, size=78, end=A("b4", "loved") - 0.05)
        sign(cr, t, A("b4", "loved"), 360, 200, "TOWN: LOVED IT", col=GREEN, size=56)
        sparkles(cr, t, A("b4", "loved"), 360, 520, n=10, seed=6, col=GOLD, spread=180)
    vignette(cr, 0.3)


def scene_store(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#f6e2c0")), (1, hexc("#d9b27a"))]))
    cr.fill()
    for row in range(3):                                              # shelves of jars and cans
        y = 220 + row * 170
        rrect(cr, 30, y + 110, 660, 18, 4)
        paint(cr, hexc("#8a5a2e"), OUTLINE, 5)
        rng = random.Random(row)
        for k in range(8):
            x = 60 + k * 80
            col = hexc(rng.choice(["#e8473f", "#4aa3f0", "#3fbf6a", "#ffcf3f", "#7a5bd0"]))
            rrect(cr, x, y + 40, 52, 70, 8)
            paint(cr, col, OUTLINE, 4)
    rrect(cr, 0, 860, W, 420, 0)                                      # the counter
    paint(cr, lin(0, 860, 0, H, [(0, hexc("#9a6a3a")), (1, hexc("#6a4424"))]), OUTLINE, 8)
    cat(cr, t, 280, 880, 0.75, eyes="happy" if t >= A("b5", "catnip.") else "open")
    if t >= A("b5", "drink?"):                                        # the wine glass of catnip water
        gx, gy = 520, 860
        k = appear(t, A("b5", "drink?"), 0.4)
        cr.save()
        cr.translate(gx, gy)
        cr.scale(k, k)
        stroke_line(cr, [(0, 0), (0, -70)], 8, OUTLINE, curve=False)
        stroke_line(cr, [(-40, 0), (40, 0)], 8, OUTLINE, curve=False)
        cr.move_to(-55, -190)
        cr.curve_to(-55, -90, 55, -90, 55, -190)
        cr.close_path()
        paint(cr, (0.85, 0.95, 1.0, 0.6), OUTLINE, 6)
        if t >= A("b5", "catnip."):
            for j in range(4):
                ellipse(cr, -20 + j * 14, -150 + (j % 2) * 10, 10, 5, rot=0.5 * j)
                paint(cr, GREEN, OUTLINE, 2)
        cr.restore()
    sign(cr, t, A("b5", "office?"), 360, 130, "OFFICE: GENERAL STORE", col=BLUE, size=46, end=A("b5", "drink?") - 0.05)
    sign(cr, t, A("b5", "drink?"), 360, 130, "WATER + CATNIP", col=GREEN, size=56)
    vignette(cr, 0.3)


def scene_tourists(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd0ff"), hexc("#fff1d6"), seed=7)
    cat(cr, t, 360, 640, 0.75, eyes="happy")
    for k, x in enumerate((90, 220, 500, 630)):
        st = A("b6") + 0.15 * k
        if t >= st:
            person(cr, t, x, 1060, 0.5, ("student1", "student2", "student3", "reporter")[k],
                   eyes="happy", mouth="grin", arms=("up", "up"), seed=k)
            if int(t * 3 + k) % 4 == 0:                               # camera flashes
                soft_disc(cr, x, 760, 70, (1, 1, 1, 0.8))
                cue("pop", t, st)
    sign(cr, t, A("b6", "world"), 360, 180, "FROM ALL OVER THE WORLD", col=PURPLE, size=48)
    vignette(cr, 0.3)


def scene_record(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8f0dc"), hexc("#fff6e8"), seed=2)
    rows = [("RAISED TAXES", "taxes."), ("BROKE A PROMISE", "promise."), ("GAVE A SPEECH", "speech.")]
    for k, (txt, key) in enumerate(rows):
        st = A("b7", key)
        if t < st:
            continue
        y = 300 + k * 150
        rrect(cr, 70, y - 55, 580, 110, 18)
        paint(cr, WHITE, OUTLINE, 6)
        bold_text(cr, txt, 100, y + 18, 44, hexc("#2b1d16"), align="left", outline=None, shadow=0)
        stamp(cr, t, st, 560, y, "NEVER", col=GREEN, size=40, rot=-0.1)
    if t >= A("b8"):
        cr.arc(360, 790, 46, 0, 2 * math.pi)                          # the medal
        paint(cr, GOLD, OUTLINE, 6)
        bold_text(cr, "1", 360, 810, 50, WHITE)
        sign(cr, t, A("b8", "Better"), 360, 170, "BEST MAYOR EVER", col=GOLD, size=60)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b9"), 360, 180, "PICK YOUR MAYOR", col=GOLD, size=60)
    for k, (txt, col) in enumerate((("DOG", BLUE), ("CAT", ORANGE), ("GOAT", GREEN), ("???", PURPLE))):
        sign(cr, t, A("b9") + 0.4 + 0.2 * k, 200 + (k % 2) * 320, 420 + (k // 2) * 200, txt, col=col, size=64)
    vignette(cr, 0.3)


SCENES = {"office": scene_office, "town": scene_town, "vote": scene_vote, "store": scene_store,
          "tourists": scene_tourists, "record": scene_record, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("THE MAYOR", False), ("IS A CAT", True)], end=tl.at("b2"), y=170, size=96)
    captions(cr, t, tl)
