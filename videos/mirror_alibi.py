"""The Mirror Alibi -- an original detective twist, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 60 (owner approved 18 Oct 2026). Fiction. A diamond vanishes from a hotel
at 9 PM; the suspect says he slept from 8 and only woke once, when the clock "in the mirror said three". A mirror
flips a clock left to right, so 3 in the mirror is 9 on the clock: he was awake at the minute of the theft. Closing
debate: is one wrong detail enough to call someone guilty? Turbo stock female narrator with tags; the suspect and the
grandma detective through Turbo with Kokoro reference voices.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rad, rrect,
                           shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, clock, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0
voice.SPEAKERS.update({"suspect": dict(voice="am_adam", speed=1.0, turbo_ref="am_adam"),
                       "grandma": dict(voice="bf_emma", speed=0.95, turbo_ref="bf_emma")})

SCRIPT = [
    dict(id="m1", scene="case", text="A diamond vanishes from a hotel at nine o'clock at night. And the only suspect "
                                     "says he was fast asleep."),
    dict(id="m2", scene="suspect", text="I went to bed at eight. Slept like a baby.", speaker="suspect"),
    dict(id="m3", scene="mirror", text="I woke up only once. I saw the clock in the mirror across my bed. It said "
                                       "three. Then I went back to sleep.", speaker="suspect"),
    dict(id="m4", scene="grandma", text="The detective, a grandma with a cup of tea, puts her cup down. [chuckle]"),
    dict(id="m5", scene="grandma", text="In the mirror?", speaker="grandma", gap=0.3),
    dict(id="m6", scene="flip", text="Here's the thing. A mirror flips a clock, left to right."),
    dict(id="m7", scene="flip", text="So when the mirror shows three, the real clock shows nine."),
    dict(id="m8", scene="selfie", text="It's like your T-shirt in a mirror selfie. The words come out backwards."),
    dict(id="m9", scene="awake", text="So at nine, he wasn't asleep. He was wide awake. At the exact minute the "
                                      "diamond vanished. [gasp]"),
    dict(id="m10", scene="sweat", text="That proves nothing! I was just looking at a clock!", speaker="suspect"),
    dict(id="m11", scene="sweat", text="Then why did you say three?", speaker="grandma", gap=0.3),
    dict(id="m12", scene="end", text="Now you're the judge. Is one wrong detail enough to call him guilty? Or is he "
                                     "just bad at reading clocks?", gap=0.3),
]

METADATA = dict(
    title="His Alibi Had 1 Tiny Mistake. A Mirror. 🪞",
    alt_titles=["He Said He Was Asleep. The Mirror Said Otherwise 🪞", "Grandma Detective Caught Him With a Clock 🕘"],
    description="""A diamond vanishes from a hotel at 9 o'clock at night, and the only suspect says he was fast asleep. 🪞

"I went to bed at eight. I woke up only once: the clock in the mirror across my bed said three."

The detective (a grandma with a cup of tea) puts her cup down: a mirror flips a clock left to right... so three in the mirror is NINE on the clock. 🕘

A short detective story (fiction).

💬 Is one wrong detail enough to call him guilty, or is he just bad at reading clocks? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Detective", "#PlotTwist", "#Shorts"],
    tags=["detective riddle", "mirror clock riddle", "alibi", "mystery story", "plot twist", "logic puzzle",
          "brain teaser", "crime riddle", "grandma detective", "interestingly strange"],
    pinned_comment="Guilty 🔒 or just bad at clocks 🕒? One wrong detail: enough or not? 👇",
)

GRANDMA = dict(hair="bun", hair_col=hexc("#d8d8de"), shirt=hexc("#c86a8a"), pants=hexc("#5a3a5a"), skin="light")
SUSPECT = dict(skin="olive", hair="short", hair_col=hexc("#2b1a12"), stache=hexc("#2b1a12"), shirt=hexc("#9fc8ef"),
               pants=hexc("#9fc8ef"), build="adult")


def suspect(cr, t, x, y, s, tl=None, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("suspect", t) else "smug")
    person(cr, t, x, y, s, "sir", **dict(SUSPECT, **kw))


def mug(cr, hx, hy):
    rrect(cr, hx - 18, hy - 30, 36, 40, 6)
    paint(cr, WHITE, OUTLINE, 4)
    cr.arc(hx + 22, hy - 10, 10, -1.4, 1.4)
    paint(cr, None, OUTLINE, 4)


def grandma(cr, t, x, y, s, tl=None, cup=True, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("grandma", t) else "smile")
    person(cr, t, x, y, s, "teacher", hold=mug if cup else None, **dict(GRANDMA, **kw))


def _hotel_room(cr, t, night=True):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2a2440")), (0.62, hexc("#4a3a5a")), (0.62, hexc("#6a4a3a")),
                                   (1, hexc("#3a2820"))]))
    cr.fill()
    for k in range(6):                                              # wallpaper stripes
        cr.rectangle(k * 130, 0, 40, 790)
        cr.set_source_rgba(1, 1, 1, 0.04)
        cr.fill()
    rrect(cr, 420, 140, 230, 280, 12)                               # window with the night city
    paint(cr, lin(0, 140, 0, 420, [(0, hexc("#0c1428")), (1, hexc("#1f2f55"))]), OUTLINE, 6)
    for k in range(10):
        soft_disc(cr, 440 + (k * 47) % 200, 300 + (k * 31) % 100, 8, (1, 0.9, 0.5, 0.7))


def scene_case(cr, t, tl):
    A = tl.at
    _hotel_room(cr, t)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("m1", "only"), (1.1, 330, 660))], dur=0.7))
    clock(cr, t, 160, 250, 80, 540)                                 # 9:00 on the wall
    rrect(cr, 120, 640, 220, 200, 10)                               # the display stand
    paint(cr, hexc("#5a3a2a"), OUTLINE, 6)
    rrect(cr, 150, 520, 160, 130, 10)                               # empty glass case
    paint(cr, (0.75, 0.92, 1.0, 0.25), OUTLINE, 6)
    if t < A("m1", "vanishes") + 0.2:                               # the diamond, then gone
        k = 1 - seg(t, A("m1", "vanishes"), A("m1", "vanishes") + 0.2)
        cr.save()
        cr.translate(230, 600)
        cr.scale(k, k)
        cr.move_to(0, -40)
        cr.line_to(34, -6)
        cr.line_to(0, 36)
        cr.line_to(-34, -6)
        cr.close_path()
        paint(cr, hexc("#bff4ff"), OUTLINE, 4)
        cr.restore()
    else:
        bold_text(cr, "?", 230, 620, 80, GOLD)
    if t >= A("m1", "suspect"):
        suspect(cr, t, 520, 980, 0.8, eyes="closed", mouth="smug", arms=("cross", "cross"))
    cr.restore()
    if t >= A("m1", "vanishes"):
        cue("sting", t, A("m1", "vanishes"))
    sign(cr, t, A("m1", "asleep."), 360, 440, "\"I WAS ASLEEP\"", col=PURPLE, size=56)
    vignette(cr, 0.5)


def scene_suspect(cr, t, tl):
    A = tl.at
    _hotel_room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("m2") - 0.3, (1.4, 360, 560))]))
    suspect(cr, t, 360, 960, 1.0, tl, eyes="half", arms=("cross", "cross"), brows="raise")
    cr.restore()
    sign(cr, t, A("m2", "eight."), 360, 170, "BED AT 8", col=BLUE, size=64)
    vignette(cr, 0.45)


def mirrored_clock(cr, t, x, y, r, minutes):
    """The clock as seen in a mirror: drawn flipped left to right inside a mirror frame."""
    rrect(cr, x - r - 40, y - r - 60, 2 * r + 80, 2 * r + 120, 30)
    paint(cr, rad(x - 30, y - 40, r * 1.6, [(0, hexc("#e8f6ff")), (1, hexc("#a8c8dc"))]), hexc("#c99460"), 12)
    stroke_line(cr, [(x - r, y - r), (x - r + 50, y - r + 90)], 6, (1, 1, 1, 0.55), curve=False)
    cr.save()
    cr.translate(x, y)
    cr.scale(-1, 1)
    clock(cr, t, 0, 0, r, minutes)
    cr.restore()


def scene_mirror(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)                                        # his bedroom at night
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#141a33")), (1, hexc("#2a2a48"))]))
    cr.fill()
    rrect(cr, 60, 760, 420, 150, 20)                                # bed
    paint(cr, hexc("#e8e0f0"), OUTLINE, 6)
    rrect(cr, 60, 700, 120, 90, 20)
    paint(cr, WHITE, OUTLINE, 5)
    up = t >= A("m3", "woke")
    if up:                                                          # he sits up in bed
        person(cr, t, 200, 860, 0.55, "sir", eyes="half", mouth="flat", arms=("down", "down"), shadow=False,
               **SUSPECT)
    mirrored_clock(cr, t, 520, 470, 120, 540)                        # the real clock says 9; the mirror shows 3
    if t >= A("m3", "three."):
        sign(cr, t, A("m3", "three."), 520, 170, "\"IT SAID 3\"", col=GOLD, size=60)
    portrait(cr, t, A("m3"), 130, 300, 74, "sir", mouth="talk" if tl.speaking("suspect", t) else "smug",
             eyes="half", bg=hexc("#9fc8ef"), end=A("m3", end=True), **{k: v for k, v in SUSPECT.items()
                                                                         if k != "build"})
    vignette(cr, 0.55)


def scene_grandma(cr, t, tl):
    A = tl.at
    _hotel_room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("m4") - 0.3, (1.0, 360, 640)), (A("m5"), (1.5, 330, 540))], dur=0.5))
    down = t >= A("m4", "down.")
    grandma(cr, t, 330, 980, 1.0, tl, cup=not down, eyes="half" if down else "happy",
            brows="raise" if down else None, arms=("hold", "hips") if not down else ("chin", "hips"))
    if down:
        rrect(cr, 520, 820, 160, 20, 6)                             # little side table, cup on it
        paint(cr, hexc("#8a5a2e"), OUTLINE, 4)
        mug(cr, 590, 820)
    cr.restore()
    if t >= A("m5"):
        sign(cr, t, A("m5"), 360, 170, "IN THE MIRROR?", col=PURPLE, size=64)
    vignette(cr, 0.45)


def scene_flip(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=4)
    bold_text(cr, "REAL CLOCK", 180, 340, 38, WHITE)
    if t >= A("m6", "flips"):
        mirrored_clock(cr, t, 530, 520, 110, 540)
        bold_text(cr, "IN THE MIRROR", 530, 340, 38, WHITE)
    clock(cr, t, 180, 520, 110, 540)
    if t >= A("m6", "flips"):                                       # a swap arrow between them
        u = ease_out(seg(t, A("m6", "flips"), A("m6", "right.", end=True)))
        stroke_line(cr, [(300, 700), (lerp(300, 410, u), 700)], 10, GOLD, curve=False)
        stroke_line(cr, [(410, 740), (lerp(410, 300, u), 740)], 10, GOLD, curve=False)
    sign(cr, t, A("m6", "flips"), 360, 170, "LEFT <-> RIGHT", col=GOLD, size=58, end=A("m7") - 0.05)
    if t >= A("m7", "three,"):
        sign(cr, t, A("m7", "three,"), 530, 820, "SHOWS 3", col=BLUE, size=46)
    if t >= A("m7", "nine."):
        sign(cr, t, A("m7", "nine."), 180, 820, "REALLY 9", col=RED, size=50)
        sign(cr, t, A("m7", "nine."), 360, 170, "MIRROR 3 = REAL 9", col=RED, size=56)
    vignette(cr, 0.4)


def scene_selfie(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=6)
    rrect(cr, 150, 230, 420, 640, 30)                               # a bathroom mirror
    paint(cr, rad(330, 400, 500, [(0, hexc("#f4fbff")), (1, hexc("#c8dcea"))]), hexc("#c99460"), 12)
    cr.save()
    cr.rectangle(150, 230, 420, 640)
    cr.clip()
    person(cr, t, 360, 1000, 0.85, "kid", eyes="happy", mouth="grin", arms=("face", "down"), shirt=hexc("#ffcf3f"))
    cr.save()
    cr.translate(360, 840)
    cr.scale(-1, 1)                                                  # backwards shirt text
    bold_text(cr, "COOL", 0, 0, 38, RED)
    cr.restore()
    cr.restore()
    sign(cr, t, A("m8", "backwards."), 360, 170, "BACKWARDS!", col=PURPLE, size=64)
    vignette(cr, 0.3)


def scene_awake(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2a1420"), hexc("#5a2a3a"), seed=7)
    cr.save()
    cr.translate(360, 560)
    clock(cr, t, 0, 0, 150, 540)
    cr.restore()
    if t >= A("m9", "awake."):
        u = ease_out(seg(t, A("m9", "awake."), A("m9", "awake.") + 0.4))
        cr.arc(360, 560, 175 + 10 * math.sin(t * 6), -math.pi / 2, -math.pi / 2 + 2 * math.pi * u)
        paint(cr, None, RED, 12)
    sign(cr, t, A("m9", "asleep."), 360, 170, "NOT ASLEEP", col=BLUE, size=60, end=A("m9", "exact") - 0.05)
    if t >= A("m9", "exact"):
        stamp(cr, t, A("m9", "vanished."), 360, 230, "THE EXACT MINUTE", col=RED, size=60)
        cue("hit", t, A("m9", "vanished."))
    vignette(cr, 0.5)


def scene_sweat(cr, t, tl):
    A = tl.at
    _hotel_room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("m10") - 0.3, (1.3, 470, 600)), (A("m11"), (1.3, 250, 600))], dur=0.5))
    suspect(cr, t, 520, 980, 0.95, tl, eyes="wide", arms=("out", "out"), sweat=True,
            brows="sad" if t >= A("m11") else "angry")
    grandma(cr, t, 200, 980, 0.95, tl, cup=True, eyes="half", brows="raise", arms=("hold", "hips"))
    cr.restore()
    if t >= A("m11", "three?"):
        sign(cr, t, A("m11", "three?"), 360, 170, "WHY SAY 3?", col=GOLD, size=66)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    suspect(cr, t, 360, 900, 0.7, None, eyes="wide", mouth="o", arms=("shrug", "shrug"), sweat=True)
    sign(cr, t, A("m12", "judge."), 360, 190, "YOU'RE THE JUDGE", col=GOLD, size=56)
    sign(cr, t, A("m12", "guilty?"), 190, 420, "GUILTY", col=RED, size=58, rot=-0.06)
    sign(cr, t, A("m12", "clocks?"), 530, 420, "BAD AT CLOCKS", col=BLUE, size=40, rot=0.05)
    vignette(cr, 0.3)


SCENES = {"case": scene_case, "suspect": scene_suspect, "mirror": scene_mirror, "grandma": scene_grandma,
          "flip": scene_flip, "selfie": scene_selfie, "awake": scene_awake, "sweat": scene_sweat, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("HE SAYS HE", False), ("WAS ASLEEP", True)], end=tl.at("m2"), y=170, size=104)
    captions(cr, t, tl)
