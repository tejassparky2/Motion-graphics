"""The Machine That Knows Your Choice -- Newcomb's problem as a one-rule-machine story, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 58 (owner approved 18 Oct 2026). Newcomb's problem (William Newcomb;
published by Robert Nozick, 1969): a predictor that is almost never wrong, a glass box with $1,000 and a closed box
with $1,000,000 only if it predicted you'd take the closed box alone. Both arguments (dominance: take both; evidence:
one-boxers get rich) are given fairly; philosophers still split. Original story framing (a machine at a fair).
Turbo stock female narrator with tags; the machine and the kid through Turbo with Kokoro reference voices.
"""
import math
import random

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, enter, lin, paint, rad,
                           rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, chalk, money, room, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0
voice.SPEAKERS.update({"machine": dict(voice="am_onyx", speed=0.95, pitch=-1.5, turbo_ref="am_onyx"),
                       "kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3")})

SCRIPT = [
    dict(id="n1", scene="fair", text="A kid walks past a machine at the fair. And the machine says his name. [gasp]"),
    dict(id="n2", scene="hello", text="Hello. I already know what you will choose.", speaker="machine"),
    dict(id="n3", scene="boxes", text="Two boxes. A glass one, with a thousand dollars inside. And a closed one."),
    dict(id="n4", scene="boxes", text="Take only the closed box. Or take both.", speaker="machine"),
    dict(id="n5", scene="predict", text="Last night, I predicted your choice. If you take only the closed box, it has a "
                                        "million dollars. If you take both, it's empty.", speaker="machine"),
    dict(id="n6", scene="record", text="It has played ten thousand times. It has never been wrong."),
    dict(id="n7", scene="think", text="So the kid thinks. The money is already in the box, or it isn't."),
    dict(id="n8", scene="think", text="So taking both always gets me a thousand dollars more."),
    dict(id="n9", scene="lines", text="But then. Everyone who took both, walked away with a thousand. Everyone who "
                                      "took one, walked away a millionaire."),
    dict(id="n10", scene="teacher", text="Like a teacher who knows who studied, and writes the exam the night "
                                         "before."),
    dict(id="n11", scene="named", text="Philosophers have argued about this for fifty years. It's called Newcomb's "
                                       "problem."),
    dict(id="n12", scene="nice", text="Okay, machine. What am I going to pick?", speaker="kid"),
    dict(id="n13", scene="nice", text="Nice try. [chuckle]", speaker="machine", gap=0.3),
    dict(id="n14", scene="end", text="So what do you take? One box, or both?", gap=0.3),
]

METADATA = dict(
    title="This Machine Knows What You'll Pick. 2 Boxes. 📦",
    alt_titles=["1 Box or 2? A Machine Already Knows Your Answer 📦", "The $1,000,000 Box Problem (Newcomb's Problem)"],
    description="""A machine at the fair says your name, and says it already knows what you will choose. 📦

Two boxes: a glass one with $1,000 inside, and a closed one. Take only the closed box, or take both. Last night the machine predicted your choice: if it saw you taking only the closed box, it put $1,000,000 inside. If it saw you taking both, it's empty. It has played 10,000 times and never been wrong.

The money is already in the box (or not), so taking both is always $1,000 more... but everyone who took one box walked away a millionaire. 🤯

This is Newcomb's problem (published by philosopher Robert Nozick in 1969). Philosophers still split on it.

💬 One box, or both? Tell us WHY 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Paradox", "#Philosophy", "#Shorts"],
    tags=["newcomb's problem", "newcomb paradox", "one box or two", "philosophy paradox", "decision theory",
          "mind bending", "thought experiment", "would you rather", "paradox", "interestingly strange"],
    pinned_comment="One box 📦 or both 📦📦? Pick a side and give your reason 👇",
)

MACH = hexc("#c0392b")
SCREEN = hexc("#7ff0d0")


def _fair_bg(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#1a1440")), (0.6, hexc("#3a2466")), (1, hexc("#2a1838"))]))
    cr.fill()
    bokeh(cr, t, 4, 18, [hexc("#ffcf3f"), hexc("#ff7ab8"), hexc("#7fd0ff")], rmin=10, rmax=40,
          area=(0, 0, W, 700), alpha_=(0.15, 0.4))
    cr.save()                                                      # a ferris wheel far behind
    cr.translate(150, 420)
    cr.rotate(t * 0.15)
    for k in range(10):
        a = k * math.pi / 5
        stroke_line(cr, [(0, 0), (190 * math.cos(a), 190 * math.sin(a))], 3, (1, 1, 1, 0.18), curve=False)
        cr.arc(190 * math.cos(a), 190 * math.sin(a), 14, 0, 2 * math.pi)
        paint(cr, alpha((hexc("#ffcf3f"), hexc("#ff7ab8"))[k % 2], 0.5), None)
    cr.restore()
    for k in range(9):                                             # string lights
        x = 40 + k * 80
        y = 140 + 30 * math.sin(k * 0.8)
        soft_disc(cr, x, y, 22, alpha((hexc("#ffcf3f"), hexc("#ff7ab8"), hexc("#7fd0ff"))[k % 3],
                                      0.6 + 0.3 * math.sin(t * 4 + k)))
    cr.rectangle(0, 900, W, H - 900)
    cr.set_source(lin(0, 900, 0, H, [(0, hexc("#3a2a3a")), (1, hexc("#1e141e"))]))
    cr.fill()


def machine(cr, t, x, y, s=1.0, talk=False, wink=0.0, screen_text=None, glow=1.0):
    """A fortune machine: red cabinet, round glass screen with one glowing eye, brass trim. (x, y) = bottom centre."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, -20, 220, (0, 0, 0, 0.35))
    soft_disc(cr, 0, -420, 260 * glow, (0.5, 1, 0.85, 0.18 * glow))
    rrect(cr, -150, -560, 300, 560, 30)
    paint(cr, lin(-150, 0, 150, 0, [(0, shade(MACH, -0.25)), (0.5, MACH), (1, shade(MACH, -0.3))]), OUTLINE, 7)
    rrect(cr, -170, -600, 340, 70, 30)
    paint(cr, GOLD, OUTLINE, 6)
    bold_text(cr, "ORACLE", 0, -553, 44, hexc("#7a2a10"), outline=None, shadow=0)
    cr.arc(0, -400, 110, 0, 2 * math.pi)                           # the screen
    paint(cr, rad(-30, -430, 140, [(0, shade(SCREEN, 0.4)), (1, hexc("#0f3a3a"))]), OUTLINE, 7)
    if screen_text:
        bold_text(cr, screen_text, 0, -385, 40, WHITE, outline=hexc("#0f3a3a"))
    else:
        open_ = 1 - wink
        cr.save()
        cr.translate(18 * math.sin(t * 0.9), -400)
        cr.scale(1, max(0.08, open_))
        cr.arc(0, 0, 42, 0, 2 * math.pi)
        paint(cr, WHITE, OUTLINE, 5)
        cr.arc(0, 0, 20 + (4 if talk and int(t * 9) % 2 else 0), 0, 2 * math.pi)
        paint(cr, hexc("#13283a"), None)
        cr.restore()
    if talk:                                                       # speaker grille pulses
        for k in range(3):
            stroke_line(cr, [(-60, -230 + k * 22), (60, -230 + k * 22)], 6 + 3 * abs(math.sin(t * 12 + k)),
                        GOLD, curve=False)
    else:
        for k in range(3):
            stroke_line(cr, [(-60, -230 + k * 22), (60, -230 + k * 22)], 5, shade(GOLD, -0.3), curve=False)
    rrect(cr, -50, -150, 100, 40, 8)                               # coin slot
    paint(cr, hexc("#3a1a14"), GOLD, 4)
    cr.restore()


def glass_box(cr, t, x, y, s=1.0, cash=True):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, 6, 120, (0, 0, 0, 0.3))
    if cash:
        for k in range(4):
            money(cr, -30 + k * 20, -40 - k * 14, 0.1 * (k - 1.5), 0.8)
    rrect(cr, -110, -180, 220, 180, 10)
    paint(cr, (0.75, 0.92, 1.0, 0.28), OUTLINE, 6)
    stroke_line(cr, [(-80, -160), (-40, -40)], 6, (1, 1, 1, 0.5), curve=False)
    cr.restore()


def closed_box(cr, t, x, y, s=1.0, open_=0.0, full=None):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, 6, 120, (0, 0, 0, 0.3))
    if open_ > 0 and full is not None:
        if full:
            for k in range(6):
                money(cr, -50 + (k % 3) * 50, -150 - (k // 3) * 30 - 40 * open_, 0.15 * (k - 2.5), 0.7)
        rrect(cr, -110, -180, 220, 180, 10)
        paint(cr, lin(0, -180, 0, 0, [(0, hexc("#5a3a20")), (1, hexc("#3a2414"))]), OUTLINE, 6)
    rrect(cr, -110, -180, 220, 180, 10)
    paint(cr, lin(0, -180, 0, 0, [(0, hexc("#c98a4a")), (1, hexc("#8a5a2e"))]), OUTLINE, 6)
    cr.save()
    cr.translate(-115, -180)
    cr.rotate(-1.9 * open_)
    rrect(cr, 0, -26, 230, 30, 8)
    paint(cr, hexc("#d89a5a"), OUTLINE, 6)
    cr.restore()
    if open_ == 0:
        bold_text(cr, "?", 0, -60, 90, GOLD)
    cr.restore()


def scene_fair(cr, t, tl):
    A = tl.at
    _fair_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("n1", "says"), (1.25, 430, 640))], dur=0.6))
    named = t >= A("n1", "name.")
    machine(cr, t, 490, 960, 0.85, screen_text="HELLO, SAM" if named else None)
    stop = A("n1", "says")
    kx = lerp(70, 230, ease_out(seg(t, 0.0, stop)))
    person(cr, t, kx, 1000, 0.75, "kid", eyes="wide" if named else "open", mouth="o" if named else "smile",
           arms=("down", "down"), walk=t * 9 if t < stop else None, look=(0.5, -0.3) if named else (0.3, 0))
    cr.restore()
    if named:
        cue("sting", t, A("n1", "name."))
    vignette(cr, 0.5)


def scene_hello(cr, t, tl):
    A = tl.at
    _fair_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("n2") - 0.3, (1.5, 360, 560))]))
    machine(cr, t, 360, 960, 0.9, talk=tl.speaking("machine", t))
    cr.restore()
    sign(cr, t, A("n2", "already"), 360, 170, "I ALREADY KNOW", col=PURPLE, size=64)
    vignette(cr, 0.5)


def scene_boxes(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b1f4a"), hexc("#5a3a6e"), seed=3)
    cr.save()
    enter(cr, camera(t, [(A("n3") - 0.3, (1.0, 360, 640)), (A("n4"), (1.05, 360, 620))]))
    k = max(0.01, appear(t, A("n3") - 0.5, 0.4)) if t >= A("n3") - 0.5 else 0.01
    glass_box(cr, t, 200, 800, 1.4 * k)
    k = max(0.01, appear(t, A("n3") - 0.3, 0.4)) if t >= A("n3") - 0.3 else 0.01
    closed_box(cr, t, 520, 800, 1.4 * k)
    cr.restore()
    sign(cr, t, A("n3", "thousand"), 200, 400, "$1,000", col=GREEN, size=56, end=A("n4") - 0.05)
    sign(cr, t, A("n3", "closed"), 520, 400, "???", col=GOLD, size=56, end=A("n4") - 0.05)
    sign(cr, t, A("n4", "only"), 520, 400, "CLOSED ONLY", col=BLUE, size=46)
    sign(cr, t, A("n4", "both."), 200, 400, "BOTH", col=PURPLE, size=56)
    vignette(cr, 0.45)


def scene_predict(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)                                        # flashback: sepia night
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#3a2a1a")), (1, hexc("#6a4a2a"))]))
    cr.fill()
    sign(cr, t, A("n5"), 360, 170, "LAST NIGHT...", col=hexc("#a8713e"), size=58, end=A("n5", "If") - 0.05)
    full = t < A("n5", "both,")
    machine(cr, t, 170, 980, 0.5, talk=tl.speaking("machine", t))
    if t >= A("n5", "If"):
        closed_box(cr, t, 470, 820, 1.0, open_=1.0, full=full)
        if full:
            sign(cr, t, A("n5", "million"), 470, 420, "$1,000,000", col=GREEN, size=56)
            sparkles(cr, t, A("n5", "million"), 470, 640, n=8, seed=2, col=GOLD, spread=120)
        else:
            sign(cr, t, A("n5", "empty."), 470, 420, "EMPTY", col=RED, size=70)
        bold_text(cr, "ONE BOX" if full else "BOTH", 470, 300, 50, WHITE)
    vignette(cr, 0.55)


def scene_record(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=5)
    n = int(10000 * ease_out(seg(t, A("n6", "played"), A("n6", "times.", end=True))))
    bold_text(cr, f"{n:,}", 360, 480, 130, GOLD)
    bold_text(cr, "GAMES", 360, 560, 54, WHITE)
    if t >= A("n6", "never"):
        stamp(cr, t, A("n6", "never"), 360, 760, "0 MISTAKES", col=RED, size=76)
        cue("hit", t, A("n6", "never"))
    vignette(cr, 0.4)


def scene_think(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b1f4a"), hexc("#5a3a6e"), seed=7)
    person(cr, t, 360, 1000, 0.72, "kid", eyes="half", mouth="flat", arms=("think", "down"), look=(0, -0.5))
    closed_box(cr, t, 520, 560, 0.8)
    if t >= A("n7", "already"):                                     # a padlock: the past is fixed
        cr.save()
        cr.translate(520, 480)
        cr.arc(0, -30, 30, math.pi, 2 * math.pi)
        paint(cr, None, OUTLINE, 12)
        rrect(cr, -40, -30, 80, 60, 10)
        paint(cr, GOLD, OUTLINE, 5)
        cr.restore()
    sign(cr, t, A("n7", "already"), 360, 170, "CAN'T CHANGE IT NOW", col=BLUE, size=52, end=A("n8") - 0.05)
    if t >= A("n8"):
        glass_box(cr, t, 200, 560, 0.8)
        sign(cr, t, A("n8", "both"), 360, 170, "BOTH = +$1,000", col=GREEN, size=60)
    vignette(cr, 0.4)


def scene_lines(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f2f4a"), hexc("#4a5a7e"), seed=9)
    rows = (("both,", "TOOK BOTH: $1,000", PURPLE, False, 540, 245), ("one,", "TOOK ONE: $1,000,000", GREEN, True, 860, 575))
    for row, (key, label, col, rich, y, ly) in enumerate(rows):
        st = A("n9", key)
        if t < st:
            continue
        for k in range(4):
            x = 120 + k * 160
            person(cr, t, x, y, 0.46, ("kid", "teacher", "sir", "reporter")[(k + row) % 4], eyes="happy" if rich else
                   "half", mouth="grin" if rich else "flat", arms=("up", "up") if rich else ("down", "down"),
                   seed=k + row * 4)
            if rich:
                for j in range(2):
                    money(cr, x - 20 + j * 40, y - 140 - 8 * math.sin(t * 3 + k + j), 0.2 * j, 0.45)
            else:
                money(cr, x + 40, y - 100, 0.2, 0.35)
        sign(cr, t, st, 360, ly, label, col=col, size=46)
    vignette(cr, 0.4)


def scene_teacher(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    soft_disc(cr, 360, 640, 600, (0.05, 0.05, 0.2, 0.55))          # night in the classroom
    cr.save()
    enter(cr, camera(t, [(A("n10") - 0.3, (1.15, 360, 620))]))
    chalk(cr, t, A("n10", "studied,"), 110, 330, "EXAM:", 54, dur=0.3)
    chalk(cr, t, A("n10", "writes"), 110, 420, "WHO STUDIED?", 54, dur=0.5)
    person(cr, t, 450, 920, 1.0, "teacher", eyes="half", mouth="smug", arms=("write", "hips"), look=(-0.5, -0.3))
    cr.restore()
    sign(cr, t, A("n10", "night"), 360, 170, "THE NIGHT BEFORE", col=PURPLE, size=56)
    vignette(cr, 0.5)


def scene_named(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#e8d0a0"), seed=11)
    for k, (x, s) in enumerate(((190, 0.78), (530, 0.78))):         # two thinkers arguing
        person(cr, t, x, 960, s, ("russell", "aquinas")[k], facing=1 if k == 0 else -1, eyes="angry", brows="angry",
               mouth="talk" if int(t * 3 + k) % 2 else "open", arms=("point", "hips"), seed=k)
    bold_text(cr, "ONE BOX!", 190, 440, 56, BLUE)
    bold_text(cr, "BOTH!", 530, 440, 56, PURPLE)
    sign(cr, t, A("n11", "fifty"), 360, 170, "50 YEARS OF ARGUING", col=RED, size=52, end=A("n11", "called") - 0.05)
    sign(cr, t, A("n11", "Newcomb's"), 360, 170, "NEWCOMB'S PROBLEM", col=GOLD, size=56, sub="1969", sub_col=WHITE)
    vignette(cr, 0.35)


def scene_nice(cr, t, tl):
    A = tl.at
    _fair_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("n12") - 0.3, (1.15, 400, 640)), (A("n13"), (1.45, 470, 580))]))
    wink = seg(t, A("n13", "try."), A("n13", "try.") + 0.15) * (1 - seg(t, A("n13", "try.") + 0.45,
                                                                       A("n13", "try.") + 0.6))
    machine(cr, t, 490, 960, 0.85, talk=tl.speaking("machine", t), wink=wink)
    person(cr, t, 210, 1000, 0.75, "kid", eyes="half", mouth="talk" if tl.speaking("kid", t) else "smug",
           brows="raise", arms=("point", "hips"), look=(0.5, -0.3))
    cr.restore()
    if t >= A("n13"):
        sign(cr, t, A("n13"), 360, 170, "NICE TRY", col=RED, size=70)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    closed_box(cr, t, 200, 700, 0.9)
    glass_box(cr, t, 440, 700, 0.7)
    closed_box(cr, t, 600, 700, 0.7)
    sign(cr, t, A("n14", "One"), 200, 420, "ONE BOX", col=BLUE, size=56, rot=-0.06)
    sign(cr, t, A("n14", "both?"), 520, 420, "BOTH", col=PURPLE, size=60, rot=0.05)
    sign(cr, t, A("n14"), 360, 190, "WHAT DO YOU TAKE?", col=GOLD, size=54)
    vignette(cr, 0.3)


SCENES = {"fair": scene_fair, "hello": scene_hello, "boxes": scene_boxes, "predict": scene_predict,
          "record": scene_record, "think": scene_think, "lines": scene_lines, "teacher": scene_teacher,
          "named": scene_named, "nice": scene_nice, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("IT ALREADY", False), ("KNOWS", True)], end=tl.at("n2"), y=170, size=110)
    captions(cr, t, tl)
