"""The Last Bencher Part 5: "One Guard Always Lies" -- the two-guards riddle, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 56 (owner approved 18 Oct 2026). Classic logic riddle (two doors, one
guard always tells the truth, one always lies, one question): ask either guard which door the OTHER guard would say
leads home, then take the opposite door. Closing debate: is the honest guard still honest if his true answer sends
you the wrong way? Turbo stock female narrator with tags; sir and the kid through Turbo with Kokoro reference voices.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rad, rrect,
                           shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person, portrait
from videos.last_bencher_4 import (BLUE, GOLD, GREEN, PURPLE, RED, chalk, classroom, mouth_of, red_x, room,
                                   sparkles, studio)

NARRATOR = dict(turbo=True)
TAIL = 0.8
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "sir": dict(voice="am_michael", speed=1.0, turbo_ref="am_michael")})

SCRIPT = [
    dict(id="g1", scene="lock", text="The teacher locks the classroom door. Nobody goes home, until someone solves "
                                     "this."),
    dict(id="g2", scene="rules", text="Two doors. One leads home. The other leads to a test. Every day. Forever. "
                                      "[chuckle]", speaker="sir"),
    dict(id="g3", scene="rules", text="Each door has a guard. One always tells the truth. One always lies. And you "
                                      "don't know which is which.", speaker="sir"),
    dict(id="g4", scene="rules", text="You get one question. To one guard.", speaker="sir"),
    dict(id="g5", scene="panic", text="The front row starts writing. Equations. Panic. [laugh]"),
    dict(id="g6", scene="panic", text="The last bencher doesn't even stand up."),
    dict(id="g7", scene="ask", text="Easy. I ask either guard. Which door would the other guard say leads home?",
         speaker="kid"),
    dict(id="g8", scene="ask", text="Then he walks through the opposite door.", gap=0.3),
    dict(id="g9", scene="chain", text="If he asks the honest guard, he honestly repeats the liar's answer. The wrong "
                                      "door."),
    dict(id="g10", scene="chain", text="If he asks the liar, he lies about the honest guard's answer. The wrong door "
                                       "again."),
    dict(id="g11", scene="flip", text="One true answer, one lie. The answer always comes out flipped. So the other "
                                      "door is home."),
    dict(id="g12", scene="out", text="Class dismissed. [sigh]", gap=0.3),
    dict(id="g13", scene="end", text="But wait. The honest guard just pointed you to the wrong door. Still honest? "
                                     "Yes, or no?", gap=0.3),
]
clear_dialogue(SCRIPT, ids={"g9", "g10"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="One Guard Always Lies. You Get 1 Question. 🚪",
    alt_titles=["2 Doors. 2 Guards. 1 Question. The Last Bencher Solved It 😏",
                "The Liar Riddle That Locks the Whole Class In 🚪"],
    description="""The teacher locks the classroom door: nobody goes home until someone solves this. 🚪

Two doors: one leads home, the other leads to a test, every day, forever. Each door has a guard. One always tells the truth, one always lies, and you don't know which is which. You get ONE question, to ONE guard.

The Last Bencher doesn't even stand up. 😏 (The answer is in the video.)

💬 The honest guard never lied... but his answer sent you to the wrong door. Is he still honest? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Riddle", "#TheLastBencher", "#Shorts"],
    tags=["two guards riddle", "liar and truth teller riddle", "two doors riddle", "logic riddle", "the last bencher",
          "riddles with answers", "brain teaser", "teacher vs student", "logic puzzle", "interestingly strange"],
    pinned_comment="The honest guard never lied, but he pointed you to the wrong door. Still honest? Yes or no 👇",
)

DOOR = hexc("#b5763e")
GUARD = dict(skin="tan", hair="short", hair_col=hexc("#1e130d"), stache=hexc("#1e130d"), shirt=hexc("#2f3f73"),
             suit=hexc("#2f3f73"), pants=hexc("#1f2a4d"), build="adult", glasses=False)
GUARD2 = dict(GUARD, skin="light", hair_col=hexc("#3a2418"), stache=hexc("#3a2418"))


def door(cr, x, y, s=1.0, label=None, col=DOOR, open_=0.0, glow=0.0):
    """A wooden door with its bottom centre at (x, y); `open_` swings it to show light."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, -150, 150, (0, 0, 0, 0.25))
    rrect(cr, -95, -330, 190, 330, 10)                              # frame + doorway
    paint(cr, hexc("#fff4c8") if open_ > 0 else hexc("#3a2a1e"), OUTLINE, 7)
    if glow > 0:
        soft_disc(cr, 0, -160, 220 * glow, (1, 0.95, 0.6, 0.45 * glow))
    w = 180 * (1 - 0.75 * open_)
    rrect(cr, -90, -325, w, 320, 8)
    paint(cr, lin(0, -325, 0, 0, [(0, shade(col, 0.2)), (1, shade(col, -0.15))]), OUTLINE, 6)
    if open_ < 0.7:
        for py in (-290, -150):
            rrect(cr, -70, py, w - 40, 110, 6)
            paint(cr, None, alpha(OUTLINE, 0.45), 4)
        cr.arc(-90 + w - 26, -160, 11, 0, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 4)
    cr.restore()
    if label:
        bold_text(cr, label, x, y - 360 * s, 44 * s, WHITE)


def guard(cr, t, x, y, s, which, eyes="open", mouth="flat", arms=("hips", "hips"), facing=1, badge=None, look=(0, 0)):
    person(cr, t, x, y, s, "sir", facing=facing, eyes=eyes, mouth=mouth, arms=arms, look=look, seed=which * 3,
           **(GUARD if which == 0 else GUARD2))
    if badge:
        bold_text(cr, badge, x, y - 600 * s, 64 * s, GOLD)


def arrow(cr, t, start, x0, y0, x1, y1, col, dur=0.35):
    if t < start:
        return
    u = ease_out(seg(t, start, start + dur))
    xe, ye = lerp(x0, x1, u), lerp(y0, y1, u)
    stroke_line(cr, [(x0, y0), (xe, ye)], 14, OUTLINE, curve=False)
    stroke_line(cr, [(x0, y0), (xe, ye)], 8, col, curve=False)
    if u > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        cr.move_to(x1 + 26 * math.cos(a), y1 + 26 * math.sin(a))
        cr.line_to(x1 + 22 * math.cos(a + 2.4), y1 + 22 * math.sin(a + 2.4))
        cr.line_to(x1 + 22 * math.cos(a - 2.4), y1 + 22 * math.sin(a - 2.4))
        cr.close_path()
        paint(cr, col, OUTLINE, 4)


def chip(cr, t, start, x, y, text, col, size=40):
    """A small rounded label that pops in."""
    if t < start:
        return
    k = appear(t, start, 0.3)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    w = 30 + 0.62 * size * len(text)
    rrect(cr, -w / 2, -size * 0.75, w, size * 1.5, size * 0.5)
    paint(cr, col, OUTLINE, 5)
    bold_text(cr, text, 0, size * 0.35, size, WHITE)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_lock(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("g1", "Nobody"), (1.15, 380, 660))], dur=0.8))
    chalk(cr, t, 0.2, 100, 395, "2 DOORS", 46, dur=0.4)
    chalk(cr, t, 0.6, 100, 460, "2 GUARDS", 46, dur=0.4)
    chalk(cr, t, A("g1", "Nobody"), 100, 525, "1 QUESTION", 46, dur=0.4)
    door(cr, 590, 880, 0.9, col=hexc("#8a5a2e"))
    turn = seg(t, A("g1", "locks"), A("g1", "locks") + 0.5)          # key turning in the lock
    cr.save()
    cr.translate(590 + 45, 880 - 150)
    cr.rotate(turn * math.pi / 2)
    stroke_line(cr, [(0, 0), (34, 0)], 10, GOLD, curve=False)
    cr.arc(-10, 0, 14, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 4)
    cr.restore()
    person(cr, t, 420, 920, 1.0, "sir", facing=1, eyes="half", mouth="smug", brows="raise",
           arms=("push", "hips"), look=(0.4, 0))
    cr.restore()
    if t >= A("g1", "locks"):
        cue("thud", t, A("g1", "locks") + 0.3)
    vignette(cr, 0.45)


def scene_rules(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=3)
    soft_disc(cr, 360, 640, 420, (1, 0.9, 0.6, 0.12))
    cr.save()
    enter(cr, camera(t, [(A("g2") - 0.3, (1.0, 360, 640)), (A("g4"), (1.06, 360, 640))]))
    for k, (x, word, label, col) in enumerate(((200, "home.", "HOME?", GREEN), (520, "test.", "TEST?", RED))):
        door(cr, x, 860, 1.1)
        if t >= A("g2", word):
            bold_text(cr, label, x, 660, 40, col)
    if t >= A("g3"):                                                # a guard steps in front of each door
        k = ease_out(seg(t, A("g3"), A("g3") + 0.4))
        guard(cr, t, 200 - 90 * (1 - k), 900, 0.72, 0)
        guard(cr, t, 520 + 90 * (1 - k), 900, 0.72, 1, facing=-1)
    cr.restore()
    if t >= A("g3", "which.", nth=1) and t < A("g4"):
        chip(cr, t, A("g3", "which.", nth=1), 200, 400, "TRUTH? LIE?", PURPLE, 44)
        chip(cr, t, A("g3", "which.", nth=1), 520, 400, "TRUTH? LIE?", PURPLE, 44)
    elif t < A("g4"):
        if t >= A("g3", "truth."):
            chip(cr, t, A("g3", "truth."), 300, 320, "ONE ALWAYS TRUTHFUL", BLUE, 40)
        if t >= A("g3", "lies."):
            chip(cr, t, A("g3", "lies."), 300, 420, "ONE ALWAYS LIES", PURPLE, 40)
    sign(cr, t, A("g2", "Forever."), 360, 170, "EVERY DAY. FOREVER.", col=RED, size=52, end=A("g3") - 0.05)
    sign(cr, t, A("g4"), 360, 170, "1 QUESTION. 1 GUARD.", col=GOLD, size=54)
    portrait(cr, t, A("g2"), 630, 300, 66, "sir", mouth=mouth_of(tl, "sir", t, "smug"), eyes="half",
             bg=hexc("#cdb8ff"), end=A("g4", end=True))
    vignette(cr, 0.5)


def scene_panic(cr, t, tl):
    A = tl.at
    room(cr, t)
    back = t >= A("g6")
    cr.save()
    enter(cr, camera(t, [(A("g5") - 0.3, (1.0, 360, 640)), (A("g6"), (1.7, 540, 470))], dur=0.7))
    classroom(cr, t, tl, gasp=not back, kid_pose=dict(arms=("cross", "cross"), eyes="half", mouth="smug",
                                                      brows="raise"))
    cr.restore()
    if not back:
        for k in range(12):                                       # paper and doodles flying
            ph = (t * 0.8 + k * 0.11) % 1
            x = 50 + (k * 61) % 620
            y = 860 - ph * 760
            cr.save()
            cr.translate(x, y)
            cr.rotate(ph * 5 + k)
            rrect(cr, -24, -30, 48, 60, 3)
            paint(cr, WHITE, OUTLINE, 3)
            bold_text(cr, ("x²", "?!", "=", "∑")[k % 4] if k % 4 != 3 else "+", 0, 10, 24, OUTLINE, outline=None,
                      shadow=0)
            cr.restore()
        sign(cr, t, A("g5", "Panic."), 360, 170, "PANIC", col=RED, size=80)
        cue("whoosh", t, A("g5", "Equations."))
    else:
        sign(cr, t, A("g6", "stand"), 360, 170, "NOT EVEN STANDING UP", col=GOLD, size=50)
    vignette(cr, 0.45)


def scene_ask(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=6)
    walk = t >= A("g8")
    cr.save()
    enter(cr, camera(t, [(A("g7") - 0.3, (1.0, 360, 640)), (A("g8"), (1.05, 360, 640))]))
    door(cr, 190, 820, 0.8, open_=0.0)
    opened = seg(t, A("g8", "walks"), A("g8", "walks") + 0.5)
    door(cr, 530, 820, 0.8, open_=opened, glow=opened)
    guard(cr, t, 110, 880, 0.5, 0)
    guard(cr, t, 620, 880, 0.5, 1, facing=-1)
    kx = 360 if not walk else lerp(360, 520, ease_out(seg(t, A("g8", "walks"), A("g8", "opposite"))))
    person(cr, t, kx, 940, 0.62, "kid", eyes="half" if not walk else "happy",
           mouth=mouth_of(tl, "kid", t, "smug"), arms=("point", "pocket") if tl.speaking("kid", t) else
           ("pocket", "pocket"), walk=t * 9 if walk and t < A("g8", "opposite") else None)
    if walk:
        arrow(cr, t, A("g8", "opposite"), 330, 430, 500, 430, GREEN)
    cr.restore()
    if t >= A("g7", "Which") and t < A("g8"):
        sign(cr, t, A("g7", "Which"), 360, 190, "WHICH DOOR WOULD", col=PURPLE, size=48,
             sub="THE OTHER GUARD SAY LEADS HOME?", sub_col=WHITE)
    if walk:
        sign(cr, t, A("g8", "opposite"), 360, 190, "TAKE THE OTHER DOOR", col=GREEN, size=52)
        cue("whoosh", t, A("g8", "walks"))
    vignette(cr, 0.45)


def _column(cr, t, x, title, first, second, c1, c2, key_times):
    """Ask a guard (first) -> his answer about the other guard (second) -> the wrong door, top to bottom."""
    t0, t1, t2, t3 = key_times
    if t < t0:
        return
    bold_text(cr, title, x, 300, 46, WHITE)
    chip(cr, t, t1, x, 375, first, c1, 54)
    arrow(cr, t, t2, x, 410, x, 470, WHITE)
    chip(cr, t, t2, x, 525, second, c2, 40 if len(second) > 10 else 50)
    arrow(cr, t, t3, x, 560, x, 640, WHITE)
    if t >= t3:
        door(cr, x, 860, 0.62)
        red_x(cr, t, t3, x, 760, 60)


def scene_chain(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=9)
    sign(cr, t, A("g9"), 360, 170, "ASK THE HONEST ONE", col=BLUE, size=50, end=A("g10") - 0.05)
    sign(cr, t, A("g10"), 360, 170, "ASK THE LIAR", col=PURPLE, size=58)
    _column(cr, t, 190, "HONEST GUARD", "TRUTH", "LIAR'S ANSWER", BLUE, PURPLE,
            (A("g9"), A("g9", "honest"), A("g9", "repeats"), A("g9", "wrong")))
    _column(cr, t, 530, "LYING GUARD", "LIE", "FLIPS IT", PURPLE, RED,
            (A("g10"), A("g10", "liar,"), A("g10", "lies"), A("g10", "wrong")))
    vignette(cr, 0.4)


def scene_flip(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=11)
    chip(cr, t, A("g11", "true"), 200, 400, "1 TRUTH", BLUE, 56)
    chip(cr, t, A("g11", "lie."), 520, 400, "1 LIE", PURPLE, 56)
    if t >= A("g11", "flipped."):
        k = ease_out(seg(t, A("g11", "flipped."), A("g11", "flipped.") + 0.5))
        cr.save()
        cr.translate(360, 560)
        cr.rotate(k * math.pi)
        bold_text(cr, "WRONG", 0, 30, 96, RED)
        cr.restore()
        sign(cr, t, A("g11", "flipped."), 360, 170, "ALWAYS FLIPPED", col=RED, size=62, end=A("g11", "So") - 0.05)
    if t >= A("g11", "So"):
        door(cr, 220, 900, 0.6)
        red_x(cr, t, A("g11", "So"), 220, 700, 50)
        door(cr, 500, 900, 0.6, open_=seg(t, A("g11", "home."), A("g11", "home.") + 0.4), glow=1.0)
        sign(cr, t, A("g11", "home."), 360, 170, "THE OTHER DOOR = HOME", col=GREEN, size=52)
        sparkles(cr, t, A("g11", "home."), 500, 650, n=8, seed=3, col=GOLD, spread=140)
    vignette(cr, 0.4)


def scene_out(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("g12") - 0.3, (1.3, 360, 600))]))
    door(cr, 590, 880, 0.9, col=hexc("#8a5a2e"), open_=seg(t, A("g12"), A("g12") + 0.5), glow=1.0)
    slump = t >= A("g12", "dismissed.", end=True)
    person(cr, t, 330, 920, 1.0, "sir", eyes="half" if slump else "sad", mouth="flat", brows="sad",
           arms=("down", "down") if slump else ("push", "down"), tilt=0.06 if slump else 0.0)
    cr.restore()
    stamp(cr, t, A("g12", "dismissed."), 360, 230, "CLASS DISMISSED", col=GREEN, size=60)
    if t >= A("g12", "dismissed."):
        cue("hit", t, A("g12", "dismissed."))
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    guard(cr, t, 360, 860, 0.7, 0, eyes="wide" if t >= A("g13", "honest?") else "open",
          mouth="o" if t >= A("g13", "honest?") else "flat", arms=("shrug", "shrug") if t >= A("g13", "honest?")
          else ("point", "hips"), badge="TRUTH" if t < A("g13", "honest?") else None)
    if t < A("g13", "honest?"):
        arrow(cr, t, A("g13", "pointed"), 470, 470, 640, 470, RED)
    sign(cr, t, A("g13", "honest?"), 360, 190, "STILL HONEST?", col=GOLD, size=64)
    sign(cr, t, A("g13", "Yes,"), 190, 420, "YES", col=GREEN, size=70, rot=-0.06)
    sign(cr, t, A("g13", "no?"), 530, 420, "NO", col=RED, size=70, rot=0.05)
    vignette(cr, 0.3)


SCENES = {"lock": scene_lock, "rules": scene_rules, "panic": scene_panic, "ask": scene_ask, "chain": scene_chain,
          "flip": scene_flip, "out": scene_out, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("ONE GUARD", False), ("ALWAYS LIES", True)], end=tl.at("g2"), y=170, size=100)
    captions(cr, t, tl)
