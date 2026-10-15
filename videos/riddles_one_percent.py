"""Hook test H3 (numbered list): "3 Riddles. Only 1 in 100 Gets the Last One".

Script: out/scripts_hook_test.md, H3 (owner approved 15 Oct 2026; riddles swapped for ones the channel hasn't used:
towel, piano, stamp). Classic riddles. Turbo voice with tags (narrator only).
"""
import math

from motion import thriller as th
from motion.engine import W, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, sign, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, chalk, clock, room, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0

SCRIPT = [
    dict(id="b1", scene="hook", text="Three riddles. Most people get the first two. Only one in a hundred gets the "
                                     "last one."),
    dict(id="b2", scene="r1", text="Riddle one. What gets wetter, the more it dries?"),
    dict(id="b3", scene="r1", text="A towel. Easy."),
    dict(id="b4", scene="r2", text="Riddle two. What has keys, but can't open a single lock?"),
    dict(id="b5", scene="r2", text="A piano."),
    dict(id="b6", scene="r3", text="Riddle three. What can travel around the world, while staying in one corner?"),
    dict(id="b7", scene="r3", text="Three seconds."),
    dict(id="b8", scene="r3", text="A stamp. [chuckle]", gap=0.4),
    dict(id="b9", scene="end", text="Got it before the answer? Comment, one percent. If not, watch the third one "
                                    "again."),
]
clear_dialogue(SCRIPT, ids={"b2", "b4", "b6"}, pace=0.92)

METADATA = dict(
    title="3 Riddles. Only 1% Get the Last One 🧠",
    alt_titles=["Riddle #3 Breaks Everyone 🧠", "Most People Fail Riddle Number 3 🤔"],
    description="""Three riddles. Most people get the first two. Only one in a hundred gets the last one. 🧠

1️⃣ What gets wetter, the more it dries?
2️⃣ What has keys, but can't open a single lock?
3️⃣ What can travel around the world, while staying in one corner?

Answers in the video... no peeking. 😏

💬 Got #3 before the answer? Comment "1%" 👇

🔔 Interestingly Strange: The Last Bencher, riddles, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Riddles", "#BrainTeaser", "#Shorts"],
    tags=["riddles", "riddles with answers", "brain teasers", "only 1 percent", "hard riddles", "trick questions",
          "stamp riddle", "towel riddle", "piano riddle", "interestingly strange"],
    pinned_comment="Did you get #3 before the answer? Be honest 👀 1% or 99%? 👇",
)


def board_cards(cr, t, lit):
    """Three numbered cards on the board; `lit` = the one being asked (1-3)."""
    for k in range(3):
        x = 150 + k * 210
        col = RED if k == 2 else (GREEN if k + 1 < lit else WHITE)
        rrect(cr, x - 80, 320, 160, 200, 18)
        paint(cr, (0.1, 0.25, 0.18, 0.8), col, 8)
        bold_text(cr, str(k + 1), x, 465, 140, col)


def scene_hook(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cam = camera(t, [(0.0, (1.0, 360, 640)), (A("b1", "last"), (1.5, 570, 360))], dur=0.9)
    cr.save()
    enter(cr, cam)
    board_cards(cr, t, 1 if t < A("b1", "first") else 3)
    if t >= A("b1", "first"):
        for k in range(2):
            stamp(cr, t, A("b1", "first") + 0.2 * k, 150 + k * 210, 420, "OK", col=GREEN, size=40)
    cr.restore()
    if t >= A("b1", "hundred"):
        stamp(cr, t, A("b1", "hundred"), 360, 820, "ONLY 1%", col=RED, size=80)
    vignette(cr, 0.4)


def towel(cr, t, x, y, s, wet):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(0.08 * math.sin(t * 3))
    rrect(cr, -130, -170, 260, 340, 16)
    paint(cr, lin(0, -170, 0, 170, [(0, hexc("#7ac8ff")), (1, hexc("#3a8ad0"))]), OUTLINE, 7)
    for k in range(3):
        cr.rectangle(-130, -100 + k * 40, 260, 14)
        paint(cr, WHITE, None)
    for k in range(int(8 * wet)):                                 # drips
        dx, ph = -100 + (k * 37) % 200, (t * 1.5 + k * 0.37) % 1
        ellipse(cr, dx, 180 + 120 * ph, 8, 12)
        paint(cr, (0.5, 0.75, 1, 1 - ph), None)
    cr.restore()


def scene_r1(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    ans = A("b3")
    cr.save()
    enter(cr, camera(t, [(A("b2") - 0.3, (1.0, 360, 640))]))
    chalk(cr, t, A("b2", "What"), 90, 270, "Gets WETTER", 60)
    chalk(cr, t, A("b2", "more"), 90, 360, "the more", 60)
    chalk(cr, t, A("b2", "dries?"), 90, 450, "it dries?", 60)
    cr.restore()
    if t >= ans:
        towel(cr, t, 360, 640, appear(t, ans, 0.4), seg(t, ans, ans + 1.0))
        sign(cr, t, ans, 360, 180, "A TOWEL", col=BLUE, size=80)
        cue("whoosh", t, ans)
    sign(cr, t, A("b2"), 360, 110, "RIDDLE 1", col=GREEN, size=54, end=ans - 0.05)
    vignette(cr, 0.4)


def piano(cr, t, x, y, s, lit_from):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -300, -150, 600, 300, 20)
    paint(cr, lin(0, -150, 0, 150, [(0, hexc("#3a2a20")), (1, hexc("#1a120c"))]), OUTLINE, 8)
    for k in range(10):
        lit = t >= lit_from + 0.08 * k and t < lit_from + 0.08 * k + 0.25
        rrect(cr, -280 + k * 56, -40, 52, 170, 6)
        paint(cr, GOLD if lit else WHITE, OUTLINE, 4)
    for k in (0, 1, 3, 4, 5, 7, 8):
        rrect(cr, -248 + k * 56, -40, 32, 100, 4)
        paint(cr, hexc("#111111"), None)
    cr.restore()


def scene_r2(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    ans = A("b5")
    cr.save()
    enter(cr, camera(t, [(A("b4") - 0.3, (1.0, 360, 640))]))
    chalk(cr, t, A("b4", "keys,"), 90, 270, "Has KEYS,", 60)
    chalk(cr, t, A("b4", "open"), 90, 360, "can't open", 60)
    chalk(cr, t, A("b4", "lock?"), 90, 450, "a LOCK?", 60)
    cr.restore()
    if t >= A("b4", "keys,"):
        k = appear(t, A("b4", "keys,"), 0.3)                       # a key that won't turn in a lock
        bold_text(cr, "KEY?", 360, 700, int(60 * k) + 1, GOLD)
    if t >= ans:
        piano(cr, t, 360, 700, appear(t, ans, 0.4), ans + 0.2)
        sign(cr, t, ans, 360, 180, "A PIANO", col=PURPLE, size=80)
        cue("whoosh", t, ans)
    sign(cr, t, A("b4"), 360, 110, "RIDDLE 2", col=GREEN, size=54, end=ans - 0.05)
    vignette(cr, 0.4)


def globe(cr, t, x, y, r):
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, rad(x - r * 0.3, y - r * 0.3, r * 1.3, [(0, hexc("#7ad0ff")), (1, hexc("#2a6ab0"))]), OUTLINE, 7)
    for k, (dx, dy, rx, ry) in enumerate(((-0.35, -0.2, 0.3, 0.22), (0.3, 0.1, 0.25, 0.32), (-0.1, 0.45, 0.2, 0.12))):
        ellipse(cr, x + dx * r + 8 * math.sin(t * 0.8), y + dy * r, rx * r, ry * r)
        paint(cr, hexc("#5ac06a"), OUTLINE, 4)


def envelope(cr, x, y, s, rot):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -90, -60, 180, 120, 8)
    paint(cr, hexc("#fff6e0"), OUTLINE, 6)
    stroke_line(cr, [(-90, -60), (0, 10), (90, -60)], 5, OUTLINE, curve=False)
    rrect(cr, 44, -50, 36, 42, 3)                                  # the stamp, in its corner
    paint(cr, RED, OUTLINE, 3)
    cr.restore()


def scene_r3(cr, t, tl):
    A = tl.at
    b7, ans = A("b7"), A("b8")
    if t < ans:
        room(cr, t, board=True)
        cr.save()
        enter(cr, camera(t, [(A("b6") - 0.3, (1.0, 360, 640)), (b7, (1.12, 360, 600))], dur=0.6))
        chalk(cr, t, A("b6", "travel"), 90, 270, "Travels the WORLD,", 54)
        chalk(cr, t, A("b6", "while"), 90, 360, "stays in", 54)
        chalk(cr, t, A("b6", "corner?"), 90, 450, "ONE CORNER?", 54)
        cr.restore()
        if t >= b7:                                                # the 3-2-1
            n = 3 - int((t - b7) / max(0.3, (ans - b7) / 3))
            if n >= 1:
                bold_text(cr, str(n), 360, 760, 220, RED)
                cue("thud", t, b7 + (3 - n) * max(0.3, (ans - b7) / 3))
            clock(cr, t, 600, 700, 60, 60 * seg(t, b7, ans))
        sign(cr, t, A("b6"), 360, 110, "RIDDLE 3", col=RED, size=54)
    else:
        studio(cr, t, hexc("#9fd0ff"), hexc("#fff1d6"), seed=3)
        globe(cr, t, 360, 600, 200)
        ang = (t - ans) * 2.2
        envelope(cr, 360 + 280 * math.cos(ang), 600 + 120 * math.sin(ang), 0.9, 0.2 * math.sin(ang))
        sign(cr, t, ans, 360, 200, "A STAMP", col=RED, size=86)
        sparkles(cr, t, ans + 0.2, 360, 600, n=10, seed=5, col=GOLD, spread=200)
        cue("hit", t, ans)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    k = appear(t, A("b9", "one"), 0.4)
    if k:
        cr.arc(360, 520, 150 * k, 0, 2 * math.pi)
        paint(cr, rad(330, 480, 180, [(0, hexc("#ffe27a")), (1, GOLD)]), OUTLINE, 8)
        bold_text(cr, "1%", 360, 560, int(110 * k) + 1, WHITE)
    sign(cr, t, A("b9"), 360, 190, "GOT IT?", col=GREEN, size=72, end=A("b9", "If") - 0.05)
    sign(cr, t, A("b9", "If"), 360, 190, "WATCH #3 AGAIN", col=RED, size=60)
    vignette(cr, 0.3)


SCENES = {"hook": scene_hook, "r1": scene_r1, "r2": scene_r2, "r3": scene_r3, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("ONLY 1% GET", False), ("RIDDLE #3", True)], end=tl.at("b1", "first"), y=170, size=96)
    captions(cr, t, tl)
