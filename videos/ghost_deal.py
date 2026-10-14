"""The Ghost's Deal -- genie-style story #5, the Last Bencher Halloween special for Oct 31
(out/scripts_genie_style_batch1.md, approved by the owner on 14 Oct 2026). A ghost: "Guess what I'll do next. Guess
right and I leave; guess wrong and I scare you forever." The kid: "You're going to scare me forever." Original story
(the crocodile-dilemma trap in a Halloween costume); narrated by ElevenLabs Chris.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, INKC, PURPLE, RED, card, shake, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc,
                           sprite, stamp, stroke_line, vignette)
from motion.rulekit import either_way, mouth, note
from motion.toons import person
from motion.toons import _limb

NARRATOR = dict(engine="elevenlabs")
TAIL = 0.9
voice.SPEAKERS.update({
    "ghost": dict(el=voice.ELEVEN["harry"], pitch=-2.0, tone="menacing", fx="aecho=0.8:0.7:220|380:0.22|0.1"),
    "kid": dict(el=voice.ELEVEN["liam"], pitch=2.5, tone="bored"),
})

SCRIPT = [
    dict(id="h1", scene="float", text="On Halloween night, a ghost floats into the last bencher's room.",
         tone="mysterious"),
    dict(id="h2", scene="deal", text="Guess what I'll do next. Guess right, and I leave. Guess wrong, and I scare "
                                     "you forever!", speaker="ghost", gap=0.3),
    dict(id="h3", scene="phone", text="The kid doesn't even look up from his phone.", gap=0.3, pace=0.95,
         tone="amused"),
    dict(id="h4", scene="answer", text="You're going to scare me forever.", speaker="kid", gap=0.4, pace=0.92),
    dict(id="h5", scene="freeze", text="The ghost freezes.", gap=0.45, pace=0.92, tone="dramatic"),
    dict(id="h6", scene="logic", text="If he scares the kid, the guess was right. And a right guess means he has to "
                                      "leave.", pace=0.9),
    dict(id="h7", scene="logic", text="If he leaves, the guess was wrong. And a wrong guess means he has to stay, and "
                                      "scare him.", pace=0.9),
    dict(id="h8", scene="logic", text="Either way, the ghost breaks his own deal.", pace=0.9),
    dict(id="h9", scene="homework", text="So the ghost sat down, and helped with the homework.", gap=0.3,
         tone="amused"),
    dict(id="h10", scene="end", text="What would you have guessed?", gap=0.3, pace=0.95, tone="curious"),
]

METADATA = dict(
    title="A Ghost Made a Deal With the Last Bencher 👻",
    alt_titles=["The Ghost Picked the Wrong Kid to Scare 👻", "Halloween: 1 Guess Broke the Ghost's Deal 🎃",
                "\"You're Going to Scare Me Forever.\" 👻🤯"],
    description="""On Halloween night, a ghost floats into the last bencher's room. 👻

"Guess what I'll do next. Guess right, and I leave. Guess wrong, and I scare you forever!"

The kid doesn't even look up from his phone. "You're going to scare me forever."

The ghost freezes. If he scares the kid, the guess was right, and a right guess means he has to leave. If he leaves, the guess was wrong, and a wrong guess means he has to stay and scare him. Either way, the ghost breaks his own deal.

So the ghost sat down, and helped with the homework. 🎃

A Last Bencher Halloween special, built on the ancient crocodile dilemma.

💬 What would YOU have guessed? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Halloween", "#LastBencher", "#Shorts"],
    tags=["halloween", "ghost", "last bencher", "ghost paradox", "crocodile dilemma", "paradox", "brain teaser",
          "funny halloween story", "logic puzzle", "interestingly strange"],
    pinned_comment="What would YOU have guessed? 👻 Best answer gets pinned 🎃👇",
)

NIGHT = hexc("#1e2448")
GHOST = hexc("#f4f6ff")
PUMPKIN = hexc("#ff8a1e")


# ---------------------------------------------------------------- the night bedroom
def _room(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 800, [(0, hexc("#1a1f3e")), (1, hexc("#2e3566"))]))
    c.fill()
    for x in range(-20, W + 40, 80):
        c.rectangle(x, 0, 36, 800)
        c.set_source_rgba(1, 1, 1, 0.03)
        c.fill()
    rrect(c, 410, 120, 250, 300, 14)            # window: full moon, bats
    paint(c, lin(0, 120, 0, 420, [(0, hexc("#0e1430")), (1, hexc("#3a2a6a"))]), OUTLINE, 6)
    c.arc(560, 220, 62, 0, 2 * math.pi)
    paint(c, rad(545, 205, 70, [(0, hexc("#fffbe0")), (1, hexc("#ffe28a"))]), None, 0)
    for bx, by in ((470, 190), (500, 300), (620, 330)):
        c.move_to(bx - 20, by)
        c.curve_to(bx - 12, by - 12, bx - 4, by - 6, bx, by)
        c.curve_to(bx + 4, by - 6, bx + 12, by - 12, bx + 20, by)
        c.curve_to(bx + 8, by + 2, bx, by + 8, bx - 20, by)
        c.set_source_rgba(0.05, 0.05, 0.1, 1)
        c.fill()
    c.rectangle(530, 120, 8, 300)
    c.rectangle(410, 266, 250, 8)
    c.set_source_rgba(*hexc("#3a3f6a"))
    c.fill()
    rrect(c, 400, 410, 270, 22, 6)              # windowsill
    paint(c, hexc("#4a4f7a"), OUTLINE, 4)
    c.rectangle(0, 800, W, H - 800)             # floor
    c.set_source(lin(0, 800, 0, H, [(0, hexc("#3a2e4a")), (1, hexc("#1e1828"))]))
    c.fill()
    c.rectangle(0, 796, W, 10)
    c.set_source_rgba(*hexc("#141020"))
    c.fill()
    rrect(c, 60, 170, 170, 120, 8)              # a poster
    paint(c, hexc("#5a4a8a"), OUTLINE, 4)
    bold_text(c, "ROCK", 145, 245, 40, GOLD, shadow=0)


def room(cr, t):
    put(cr, sprite("ghost_room", W, H, _room), 0, 0)
    pumpkin(cr, t, 600, 412, 0.5)


def pumpkin(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, -50, 110 + 8 * math.sin(t * 9), (1, 0.6, 0.2, 0.35))
    for ox, rx in ((-40, 50), (40, 50), (0, 60)):
        ellipse(cr, ox, -55, rx, 55)
        paint(cr, lin(0, -110, 0, 0, [(0, shade(PUMPKIN, 0.2)), (1, shade(PUMPKIN, -0.25))]), OUTLINE, 4)
    rrect(cr, -8, -128, 16, 26, 4)
    paint(cr, hexc("#3a7a2a"), OUTLINE, 3)
    glow = (1, 0.9, 0.4, 0.9 + 0.1 * math.sin(t * 12))
    for side in (-1, 1):
        cr.move_to(side * 30, -80)
        cr.line_to(side * 14, -58)
        cr.line_to(side * 46, -58)
        cr.close_path()
        cr.set_source_rgba(*glow)
        cr.fill()
    smooth(cr, [(-40, -40), (-20, -30), (0, -38), (20, -30), (40, -40), (20, -18), (0, -24), (-20, -18)])
    cr.set_source_rgba(*glow)
    cr.fill()
    cr.restore()


def phone(cr, hx, hy, glow=1.0):
    soft_disc(cr, hx, hy - 30, 90, (0.55, 0.85, 1.0, 0.35 * glow))
    cr.save()
    cr.translate(hx, hy - 20)
    cr.rotate(-0.2)
    rrect(cr, -18, -32, 36, 64, 7)
    paint(cr, hexc("#2b2b33"), OUTLINE, 3)
    rrect(cr, -14, -27, 28, 52, 4)
    paint(cr, hexc("#7ad0ff"), None, 0)
    cr.restore()


# ---------------------------------------------------------------- the ghost
def ghost(cr, t, x, y, s=1.0, eyes="open", talk=False, arms="spooky", alpha_=0.92, g=0.0, flicker=0.0, seed=0):
    """A floating sheet ghost; (x, y) is the centre of its head."""
    a = alpha_ * (1 - 0.6 * flicker * (math.sin(t * 40) > 0))
    bob = math.sin(t * 2.4 + seed) * 12 * (1 - g)
    cr.save()
    cr.translate(x, y + bob)
    cr.scale(s, s)
    cr.push_group()
    for side in (-1, 1):                         # arms
        if arms == "spooky":
            pts = [(side * 90, 60), (side * 170, 0 + 10 * math.sin(t * 5 + side)), (side * 200, -60)]
        elif arms == "point":
            pts = [(side * 90, 60), (side * 160, 50), (side * 230, 30)] if side > 0 else \
                  [(-90, 60), (-130, 120), (-140, 170)]
        elif arms == "up":
            pts = [(side * 90, 40), (side * 150, -60), (side * 160, -150)]
        else:                                    # "write" / down
            pts = [(side * 90, 60), (side * 130, 130), (side * 120, 190)]
        _limb(cr, pts, 46, GHOST)
    cr.move_to(-120, 0)                          # body: dome head, wavy hem
    cr.curve_to(-120, -170, 120, -170, 120, 0)
    cr.line_to(130, 250)
    for k in range(5):
        x0 = 130 - k * 52
        cr.curve_to(x0 - 10, 250 + 34 * math.sin(t * 4 + k), x0 - 42, 250 - 20, x0 - 52, 250 + 10 * math.sin(t * 4 + k + 1))
    cr.line_to(-120, 0)
    cr.close_path()
    paint(cr, rad(-40, -60, 300, [(0, WHITE), (0.7, GHOST), (1, hexc("#c8cce8"))]), OUTLINE, 5.5)
    for side in (-1, 1):                         # eyes
        ex, ey = side * 44, -40
        if eyes == "x":
            for d in (-1, 1):
                stroke_line(cr, [(ex - 16, ey - 16 * d), (ex + 16, ey + 16 * d)], 8, OUTLINE, curve=False)
        else:
            ellipse(cr, ex, ey, 22 if eyes != "wide" else 28, 34 if eyes != "half" else 18)
            paint(cr, hexc("#141020"), None, 0)
            cr.arc(ex - 7, ey - 12, 6, 0, 2 * math.pi)
            paint(cr, WHITE, None, 0)
    if talk:
        ellipse(cr, 0, 40, 28, 12 + 20 * abs(math.sin(t * 15)))
    elif eyes == "wide":
        ellipse(cr, 0, 46, 22, 26)
    else:
        ellipse(cr, 0, 40, 30, 10)
    paint(cr, hexc("#141020"), None, 0)
    for side in (-1, 1):
        ellipse(cr, side * 80, 10, 18, 10)
        paint(cr, alpha(hexc("#ff9ab8"), 0.5), None, 0)
    pat = cr.pop_group()
    cr.set_source(pat)
    cr.paint_with_alpha(a)
    if g > 0:
        cr.set_source_rgba(0.55, 0.6, 0.72, 0.8 * g)
        cr.mask(pat)
    cr.restore()


def kid(cr, t, tl, x, y, s=1.0, **kw):
    kw.setdefault("mouth", mouth(tl, "kid", t, kw.pop("rest", "flat")))
    person(cr, t, x, y, s, "kid", shirt=hexc("#3a8a6a"), tie=None, **kw)


def kid_in_bed(cr, t, tl, look_up=False):
    """The last bencher sitting up in bed under the blanket, on his phone."""
    rrect(cr, 40, 640, 60, 400, 12)              # headboard
    paint(cr, lin(40, 0, 100, 0, [(0, hexc("#7a5238")), (1, hexc("#5a3a24"))]), OUTLINE, 5)
    ellipse(cr, 170, 800, 90, 46, -0.3)           # pillow
    paint(cr, rad(150, 780, 100, [(0, WHITE), (1, hexc("#c8c8dc"))]), OUTLINE, 4.5)
    kid(cr, t, tl, 230, 1090, 0.85, eyes="open" if look_up else "half", arms=("hold", "hold"),
        look=(0.3, -0.5) if look_up else (0.2, 0.6), hold=lambda c, hx, hy: phone(c, hx, hy - 40), bob=False)
    rrect(cr, 60, 1030, 600, 70, 12)             # mattress side
    paint(cr, lin(0, 1030, 0, 1100, [(0, hexc("#e8e8f4")), (1, hexc("#b8b8cc"))]), OUTLINE, 5)
    cr.move_to(70, 1040)                          # the blanket, wavy over the knees
    cr.curve_to(70, 960, 140, 925, 200, 945)
    cr.curve_to(300, 905, 360, 980, 450, 945)
    cr.curve_to(540, 915, 650, 960, 650, 1040)
    cr.close_path()
    paint(cr, lin(0, 915, 0, 1040, [(0, hexc("#9a7ad8")), (1, hexc("#5a3aa8"))]), OUTLINE, 5)
    for k in range(4):                            # quilt stitching
        stroke_line(cr, [(150 + k * 130, 960), (140 + k * 130, 1030)], 3, alpha(WHITE, 0.25), curve=False)


# ---------------------------------------------------------------- scenes
def scene_float(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.1, 360, 600)), (A("h1", "last"), (1.0, 360, 640))], dur=0.8))
    kid_in_bed(cr, t, tl)
    gx = lerp(-200, 470, ease_out(seg(t, A("h1", "ghost") - 0.6, A("h1", "room.") + 0.3)))
    ghost(cr, t, gx, 470, 0.8, alpha_=0.85)
    cr.restore()
    particles(cr, t, 4, 20, (0.8, 0.85, 1.0, 0.4), r=(2, 4), speed=10)
    sign(cr, t, -0.5, 360, 140, "GUESS RIGHT... OR ELSE", col=PURPLE, size=56)
    vignette(cr, 0.6)


def scene_deal(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h2") - 0.3, (1.15, 400, 560))]))
    kid_in_bed(cr, t, tl)
    ghost(cr, t, 460, 560, 0.85, talk=tl.speaking("ghost", t), arms="spooky", eyes="half")
    cr.restore()
    card(cr, t, A("h2", "right,"), 185, 230, 320, 200, "GUESS RIGHT", ["= I LEAVE"], col=GREEN, line_size=42)
    card(cr, t, A("h2", "wrong,"), 535, 230, 320, 200, "GUESS WRONG", ["= SCARED", "FOREVER!"], col=RED,
         line_size=40)
    vignette(cr, 0.55)


def scene_phone(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h3") - 0.3, (1.0, 360, 640)), (A("h3", "phone."), (1.6, 290, 720))], dur=0.7))
    ghost(cr, t, 520, 520, 0.7, eyes="wide", arms="spooky")
    kid_in_bed(cr, t, tl)
    cr.restore()
    tag(cr, t, A("h3", "look"), 360, 180, "NOT EVEN LOOKING", col=BLUE, size=50)
    vignette(cr, 0.55)


def scene_answer(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h4") - 0.3, (1.3, 300, 760))]))
    kid_in_bed(cr, t, tl)
    cr.restore()
    note(cr, t, A("h4") + 0.05, 360, 330, ["\"YOU'RE GOING", "TO SCARE ME", "FOREVER.\""], hot=1, w=500, size=56)
    vignette(cr, 0.55)


def scene_freeze(cr, t, tl):
    A = tl.at
    room(cr, t)
    fr = A("h5", "freezes.")
    dx, dy = shake(t, fr, 0.3, 8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("h5") - 0.3, (1.15, 400, 560))]))
    kid_in_bed(cr, t, tl)
    ghost(cr, t, 460, 520, 0.9, eyes="wide", arms="up", g=ease_out(seg(t, fr, fr + 0.4)),
          flicker=seg(t, fr, fr + 0.6))
    cr.restore()
    if t >= fr:
        cue("hit", t, fr)
    stamp(cr, t, fr, 360, 170, "FROZEN", col=hexc("#7a8ab8"), size=100)
    vignette(cr, 0.55)


def _stuck(cr, t, spin):
    ghost(cr, t, 360, 760, 0.45, eyes="x" if spin and t % 1 > 0.5 else "wide", arms="up" if spin else "down",
          flicker=0.4 if spin else 0.0)


def scene_logic(cr, t, tl):
    studio(cr, t, hexc("#141a38"), hexc("#5a4a9a"), seed=8)
    either_way(cr, t, tl, "h6", "h7", "h8",
               ("SCARES HIM?", ["Guess was RIGHT...", "so he must", "LEAVE!"], GREEN),
               ("LEAVES?", ["Guess was WRONG...", "so he must", "STAY & SCARE!"], RED),
               "DEAL BROKEN", PURPLE, ("h6", "leave."), ("h7", "him."), figure=_stuck)
    vignette(cr, 0.45)


def scene_homework(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    rrect(cr, 120, 800, 480, 36, 8)              # a desk
    paint(cr, lin(0, 800, 0, 836, [(0, hexc("#9a6a3a")), (1, hexc("#6a4424"))]), OUTLINE, 5)
    for x in (150, 560):
        rrect(cr, x, 836, 20, 180, 4)
        paint(cr, hexc("#6a4424"), OUTLINE, 3.5)
    kid(cr, t, tl, 230, 1040, 0.8, eyes="happy", rest="grin", arms=("write", "hips"))
    ghost(cr, t, 470, 620, 0.62, eyes="half", arms="write")
    rrect(cr, 300, 770, 160, 34, 4)              # the notebook
    paint(cr, WHITE, OUTLINE, 3.5)
    stroke_line(cr, [(470, 690), (440, 770)], 8, GOLD, curve=False)      # the ghost's pencil
    cr.restore()
    if t >= A("h9", "helped"):
        cue("scribble", t, A("h9", "helped"), 1.0)
    sign(cr, t, A("h9", "homework."), 360, 160, "HOMEWORK BUDDY", col=GREEN, size=60)
    vignette(cr, 0.5)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    kid_in_bed(cr, t, tl, look_up=True)
    ghost(cr, t, 470, 560, 0.7, eyes="half", arms="down")
    cr.restore()
    sign(cr, t, A("h10"), 360, 150, "YOUR GUESS?", col=PURPLE, size=78)
    tag(cr, t, A("h10", "guessed?"), 360, 290, "TELL US IN THE COMMENTS", col=PUMPKIN, size=40)
    vignette(cr, 0.5)


SCENES = {"float": scene_float, "deal": scene_deal, "phone": scene_phone, "answer": scene_answer,
          "freeze": scene_freeze, "logic": scene_logic, "homework": scene_homework, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
