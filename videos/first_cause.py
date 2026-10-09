"""Who made God? The first-cause debate (Aquinas vs Russell) -- big-theory video in the polished look.

Thomas Aquinas, Summa Theologiae I, q.2, a.3 (the "second way", written 1265-1274): nothing causes itself, a chain
of causes can't go back forever, so there is "a first efficient cause, to which everyone gives the name of God".
Bertrand Russell, "Why I Am Not a Christian" (lecture, 6 March 1927): "If everything must have a cause, then God must
have a cause. If there can be anything without a cause, it may just as well be the world as God..."
Line g9 gives the classical reply (only what begins to exist needs a cause). Both sides, no verdict; God is shown
only as light, never as a figure. Script pre-approved by the owner on 9 Oct 2026 (out/scripts_theories_batch1.md).
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, calendar, card, sparkles,
                         studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, light_rays,
                           lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite,
                           stamp, stroke_line, vignette)
from motion.toons import head, person

NARRATOR = dict(speed=0.92)
TAIL = 0.9
voice.SPEAKERS.update({"russell": dict(voice="bm_george", speed=0.95)})

SCRIPT = [
    dict(id="g1", scene="hook", text="Two brilliant minds. One huge question. Does God exist?", pace=0.95),
    dict(id="g2", scene="aquinas", text="Over seven hundred years ago, Thomas Aquinas made this argument."),
    dict(id="g3", scene="chain", text="Everything that happens has a cause. You exist because of your parents. They "
                                      "exist because of theirs."),
    dict(id="g4", scene="chain", text="Follow the chain back. It can't go back forever, he said. Something had to "
                                      "start it."),
    dict(id="g5", scene="first", text="A first cause. That, Aquinas wrote, is what everyone calls God.",
         pace=0.95),
    dict(id="g6", scene="dominoes", text="Like a line of falling dominoes. Someone had to push the first one."),
    dict(id="g7", scene="russell", text="Then, in [nineteen twenty-seven,|1927,] Bertrand Russell pushed back. If "
                                        "everything must have a cause, then God must have a cause.",
         speaker="russell", speaker_from="If", gap=0.35),
    dict(id="g8", scene="russell", text="And if anything can exist without a cause, he said, it may just as well be "
                                        "the world."),
    dict(id="g9", scene="reply", text="Believers have an answer too. God isn't something that began. So God doesn't "
                                      "need a cause.", gap=0.35),
    dict(id="g10", scene="still", text="Seven hundred years later, people are still arguing about it."),
    dict(id="g11", scene="end", text="So who wins this one? Aquinas, or Russell? Keep it respectful in the comments.",
         gap=0.3, pace=0.95),
]

METADATA = dict(
    title="Who Made God? The 700-Year-Old Debate ✨",
    alt_titles=["Does God Exist? Two Brilliant Minds, One Argument 🤯", "The Argument for God, and the Question That Answers It ✨"],
    description="""Two brilliant minds. One huge question. Does God exist? ✨

Over 700 years ago, Thomas Aquinas made this argument: everything that happens has a cause. You exist because of your parents, they exist because of theirs. Follow the chain back: it can't go back forever, so something had to start it. A first cause, "to which everyone gives the name of God". Like a line of falling dominoes: someone had to push the first one.

In 1927, Bertrand Russell pushed back: "If everything must have a cause, then God must have a cause." And if anything can exist without a cause, "it may just as well be the world".

Believers have an answer too: God isn't something that began, so God doesn't need a cause. Seven hundred years later, people are still arguing about it.

Sources: Thomas Aquinas, Summa Theologiae I, q.2, a.3 (the "second way"); Bertrand Russell, "Why I Am Not a Christian" (1927).

💬 So who wins this one: Aquinas, or Russell? Keep it respectful 🙏👇

🔔 Interestingly Strange: mind-bending theories, paradoxes, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Philosophy", "#God", "#Shorts"],
    tags=["does god exist", "first cause argument", "who made god", "thomas aquinas", "bertrand russell",
          "cosmological argument", "philosophy", "debate", "religion", "interestingly strange"],
    pinned_comment="Aquinas or Russell: who makes the better point? Respectful arguments only 🙏👇",
)

CANDLE = hexc("#ffd36b")


# ---------------------------------------------------------------- backdrops and props
def _monastery(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#5a4a3e")), (1, hexc("#2e241e"))]))
    c.fill()
    rng = random.Random(4)
    for row in range(22):        # stone blocks
        for col in range(6):
            x = col * 130 + (65 if row % 2 else 0) - 40
            y = row * 60
            rrect(c, x + 3, y + 3, 124, 54, 8)
            c.set_source_rgba(1, 0.92, 0.8, 0.05 + 0.05 * rng.random())
            c.fill()
    c.new_path()               # an arched window with blue night
    c.arc(360, 360, 140, math.pi, 2 * math.pi)
    c.line_to(500, 620)
    c.line_to(220, 620)
    c.close_path()
    paint(c, lin(0, 220, 0, 620, [(0, hexc("#2a3a6a")), (1, hexc("#5a6a9a"))]), OUTLINE, 8)
    for k in range(30):
        c.arc(240 + rng.random() * 240, 260 + rng.random() * 340, 1.5 + rng.random() * 1.5, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.8)
        c.fill()
    stroke_line(c, [(360, 220), (360, 620)], 8, OUTLINE, curve=False)
    stroke_line(c, [(220, 440), (500, 440)], 8, OUTLINE, curve=False)
    c.rectangle(0, 880, W, H - 880)
    c.set_source(lin(0, 880, 0, H, [(0, hexc("#6a5038")), (1, hexc("#3a2a1e"))]))
    c.fill()


def monastery(cr, t):
    put(cr, sprite("monastery", W, H, _monastery), 0, 0)
    for x in (90, 630):
        candle(cr, t, x, 860)


def candle(cr, t, x, y):
    soft_disc(cr, x, y - 120, 130, (1, 0.8, 0.4, 0.22 + 0.04 * math.sin(t * 9 + x)))
    rrect(cr, x - 16, y - 100, 32, 100, 6)
    paint(cr, lin(x - 16, 0, x + 16, 0, [(0, hexc("#fff4dc")), (1, hexc("#e0d0b0"))]), OUTLINE, 4)
    f = 1 + 0.1 * math.sin(t * 13 + x)
    smooth(cr, [(x, y - 100), (x - 11, y - 122), (x, y - 150 * f), (x + 11, y - 122)])
    paint(cr, rad(x, y - 118, 30, [(0, hexc("#fffbe0")), (1, CANDLE)]), hexc("#ff9a3c"), 2.5)


def _hall(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#3a4a5e")), (1, hexc("#1e2838"))]))
    c.fill()
    for k in range(0, W, 90):     # wood panelling
        rrect(c, k + 6, 520, 78, 360, 6)
        paint(c, lin(0, 520, 0, 880, [(0, hexc("#8a5a3a")), (1, hexc("#5a3a24"))]), alpha(OUTLINE, 0.6), 3)
    c.rectangle(0, 880, W, H - 880)
    c.set_source(lin(0, 880, 0, H, [(0, hexc("#4a3a2e")), (1, hexc("#2a201a"))]))
    c.fill()


def hall(cr, t):
    put(cr, sprite("hall1927", W, H, _hall), 0, 0)
    light_rays(cr, t, 360, -60, n=3, a=0.06, col=(0.8, 0.9, 1.0))


def book(cr, hx, hy):
    cr.save()
    cr.translate(hx + 20, hy - 20)
    cr.rotate(-0.15)
    rrect(cr, -50, -36, 100, 72, 6)
    paint(cr, lin(0, -36, 0, 36, [(0, hexc("#8a2a2a")), (1, hexc("#5a1a1a"))]), OUTLINE, 4)
    rrect(cr, -44, -30, 88, 60, 4)
    paint(cr, hexc("#fff6dc"), OUTLINE, 2.5)
    stroke_line(cr, [(0, -30), (0, 30)], 3, OUTLINE, curve=False)
    for k in range(3):
        for sx in (-34, 8):
            stroke_line(cr, [(sx, -16 + k * 14), (sx + 26, -16 + k * 14)], 2.5, alpha(OUTLINE, 0.5), curve=False)
    cr.restore()


def podium(cr, x, y):
    smooth(cr, [(x - 110, y - 230), (x + 110, y - 230), (x + 80, y), (x - 80, y)])
    paint(cr, lin(0, y - 230, 0, y, [(0, hexc("#9a6a42")), (1, hexc("#5a3a24"))]), OUTLINE, 6)
    rrect(cr, x - 130, y - 250, 260, 30, 8)
    paint(cr, hexc("#7a4a2a"), OUTLINE, 5)


def glow(cr, t, x, y, r, a=1.0):
    """A soft golden light (used for 'the first cause'; never a figure)."""
    soft_disc(cr, x, y, r * 2.2, (1, 0.9, 0.55, 0.28 * a))
    soft_disc(cr, x, y, r * 1.2, (1, 0.95, 0.75, 0.55 * a))
    cr.arc(x, y, r * 0.55, 0, 2 * math.pi)
    cr.set_source(rad(x, y, r * 0.55, [(0, (1, 1, 1, a)), (1, (1, 0.93, 0.6, 0.0))]))
    cr.fill()
    for k in range(12):
        ang = k * math.pi / 6 + t * 0.4
        ln = r * (1.3 + 0.2 * math.sin(t * 3 + k))
        stroke_line(cr, [(x + math.cos(ang) * r * 0.7, y + math.sin(ang) * r * 0.7),
                         (x + math.cos(ang) * ln, y + math.sin(ang) * ln)], 4, (1, 0.92, 0.6, 0.5 * a),
                    curve=False)


def domino(cr, x, y, ang, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(s, s)
    rrect(cr, -18, -120, 36, 120, 6)
    paint(cr, lin(-18, 0, 18, 0, [(0, hexc("#2b2b33")), (1, hexc("#4a4f5c"))]), OUTLINE, 4)
    stroke_line(cr, [(-12, -60), (12, -60)], 3, WHITE, curve=False)
    for dy in (-95, -30):
        cr.arc(0, dy, 5, 0, 2 * math.pi)
        paint(cr, WHITE, None, 0)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W / 2, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#6a4a2e")), (1, hexc("#2e1e14"))]))
    cr.fill()
    cr.rectangle(W / 2, 0, W / 2, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#3a4a6e")), (1, hexc("#1a2238"))]))
    cr.fill()
    k1 = appear(t, A("g1", "brilliant"), 0.4)
    person(cr, t, 180, 900, 0.82 * max(k1, 0.01), "aquinas", eyes="half", mouth="smile", arms=("hold", "down"),
           hold=book)
    person(cr, t, 540, 900, 0.82 * max(k1, 0.01), "russell", eyes="half", mouth="smug", arms=("chin", "down"),
           facing=-1)
    if t >= A("g1", "question."):
        bold_text(cr, "VS", 360, 520, 90 * appear(t, A("g1", "question."), 0.4), GOLD)
    sign(cr, t, A("g1", "question."), 360, 160, "ONE QUESTION", col=PURPLE, size=60, end=A("g1", "Does") - 0.05)
    sign(cr, t, A("g1", "Does"), 360, 160, "DOES GOD EXIST?", col=GOLD, size=62)
    vignette(cr, 0.4)


def scene_aquinas(cr, t, tl):
    A = tl.at
    monastery(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("g2") - 0.3, (1.15, 360, 600))]))
    person(cr, t, 360, 920, 1.0, "aquinas", eyes="happy" if t >= A("g2", "argument.") else "open", mouth="smile",
           arms=("hold", "point"), hold=book)
    cr.restore()
    tag(cr, t, A("g2", "Thomas"), 360, 300, "THOMAS AQUINAS", col=CANDLE)
    calendar(cr, t, A("g2", "seven"), 590, 520, "WRITTEN IN THE", "1270s", col=hexc("#8a2a2a"), s=0.8)
    sign(cr, t, A("g2", "argument."), 360, 130, "THE ARGUMENT", col=GOLD, size=60)
    vignette(cr, 0.45)


def scene_chain(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe0c0"), hexc("#fff4e4"), seed=3)
    g4 = A("g4")
    kids = [("kid", dict()), ("teacher", dict(glasses=False)), ("villager", dict(beard=None)),
            ("judge", dict()), ("twain", dict())]
    keys = [A("g3", "You"), A("g3", "parents."), A("g3", "theirs."), g4, A("g4", "back.")]
    back = seg(t, A("g4", "forever,"), A("g4", "forever,") + 1.5)
    if t < keys[0]:        # cause -> effect, before the family chain appears
        k0 = appear(t, A("g3", "cause."), 0.4) if t >= A("g3", "cause.") else 0
        if k0 > 0.01:
            bold_text(cr, "CAUSE", 360, 470, 80 * k0, GOLD)
            bold_text(cr, "EFFECT", 360, 650, 80 * k0, BLUE)
            stroke_line(cr, [(360, 500), (360, 590)], 10, OUTLINE, curve=False)
    for k, ((who, kw), st) in enumerate(zip(kids, keys)):
        if t < st:
            continue
        s = 1.15 * (0.8 ** k)
        x = 580 - sum(265 * (0.8 ** j) for j in range(k)) - back * 220 * k
        kk = appear(t, st, 0.35)
        head(cr, t, x, 520, 90 * s * max(kk, 0.01), who, eyes="happy", mouth="smile", **kw)
        if k:
            ax = x + 100 * s
            stroke_line(cr, [(ax + 50 * s, 520), (ax, 520)], 9, OUTLINE, curve=False)
            cr.move_to(ax - 12, 520)
            cr.line_to(ax + 8, 506)
            cr.line_to(ax + 8, 534)
            cr.close_path()
            paint(cr, OUTLINE, None, 0)
    if t >= A("g4", "forever,"):     # the chain fading off into the distance
        for j in range(12):
            x = 30 - j * 30 + 400 * (1 - back)
            if x < -40:
                break
            cr.arc(x, 520, 14 * (0.85 ** j), 0, 2 * math.pi)
            paint(cr, alpha(OUTLINE, 0.5 * (0.85 ** j)), None, 0)
    sign(cr, t, A("g3"), 360, 160, "EVERYTHING HAS A CAUSE", col=BLUE, size=46, end=g4 - 0.05)
    stamp(cr, t, A("g4", "forever,"), 360, 790, "CAN'T GO BACK FOREVER", col=RED, size=50,
          end=A("g4", "Something") - 0.05)
    sign(cr, t, A("g4", "Something"), 360, 160, "SOMETHING STARTED IT", col=GOLD, size=50)
    vignette(cr, 0.35)


def scene_first(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#1a1430")), (1, hexc("#3a2a5a"))]))
    cr.fill()
    particles(cr, t, 6, 50, (1, 1, 1, 0.6), r=(1, 2.5), speed=6)
    k = appear(t, A("g5", "first"), 0.6)
    glow(cr, t, 360, 520, 150 * max(k, 0.01), k)
    sign(cr, t, A("g5", "first"), 360, 160, "A FIRST CAUSE", col=GOLD, size=66, end=A("g5", "calls") - 0.05)
    if t >= A("g5", "God."):
        bold_text(cr, "GOD", 360, 830, 110 * appear(t, A("g5", "God."), 0.5), CANDLE)
    tag(cr, t, A("g5", "Aquinas"), 360, 300, "AQUINAS", col=CANDLE, end=A("g5", "calls") - 0.05)
    vignette(cr, 0.5)


def scene_dominoes(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8e8ff"), hexc("#fff4e4"), seed=5)
    rrect(cr, 0, 760, W, 520, 0)
    paint(cr, lin(0, 760, 0, H, [(0, hexc("#c99a6a")), (1, hexc("#8a5a3a"))]), None, 0)
    push = A("g6", "push")
    for k in range(9):
        x = 110 + k * 66
        st = push + 0.2 + k * 0.12
        ang = 1.15 * ease_out(seg(t, st, st + 0.25)) if t >= push else 0.0
        domino(cr, x, 760, ang, 1.2)
        if k == 0 and t >= st:
            cue("pop", t, st)
    if t >= push:
        glow(cr, t, 50, 640, 50, appear(t, push, 0.4))
    sign(cr, t, A("g6", "dominoes."), 360, 200, "LIKE DOMINOES", col=BLUE, size=62, end=push - 0.05)
    sign(cr, t, push, 360, 200, "WHO PUSHED THE FIRST?", col=GOLD, size=50)
    vignette(cr, 0.35)


def scene_russell(cr, t, tl):
    A = tl.at
    hall(cr, t)
    g8 = A("g8")
    talk = tl.speaking("russell", t)
    cr.save()
    enter(cr, camera(t, [(A("g7") - 0.3, (1.0, 360, 640)), (A("g7", "If"), (1.15, 300, 600))], dur=0.6))
    person(cr, t, 280, 900, 0.95, "russell", eyes="half", mouth="talk" if talk else "smug", brows="raise",
           arms=("point", "down") if t < g8 else ("shrug", "shrug"))
    podium(cr, 280, 920)
    cr.restore()
    calendar(cr, t, A("g7", "1927,"), 560, 300, "LONDON LECTURE", "1927", col=BLUE, end=A("g7", "If") - 0.05)
    tag(cr, t, A("g7", "Russell"), 280, 300, "BERTRAND RUSSELL", col=hexc("#9fc8ff"), end=A("g7", "If") - 0.05)
    card(cr, t, A("g7", "If"), 480, 330, 400, 230, "RUSSELL", ["Everything needs", "a cause?", "Then so does God."],
         col=BLUE, end=g8 - 0.05, line_size=38)
    card(cr, t, g8, 480, 330, 400, 230, "OR...", ["If something can", "need no cause,", "why not the world?"],
         col=PURPLE, line_size=38)
    vignette(cr, 0.45)


def scene_reply(cr, t, tl):
    A = tl.at
    monastery(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    person(cr, t, 200, 920, 0.9, "aquinas", eyes="happy", mouth="smile", arms=("point", "hold"), hold_back=book)
    cr.restore()
    card(cr, t, A("g9", "God"), 470, 360, 420, 280, "THE REPLY", ["Only things that", "BEGIN need a cause.",
                                                                 "God never began."], col=hexc("#c9900c"),
         line_size=38)
    sign(cr, t, A("g9", "Believers"), 360, 130, "BELIEVERS' ANSWER", col=GOLD, size=54)
    vignette(cr, 0.45)


def scene_still(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8d0e8"), hexc("#fff1d6"), seed=8)
    stops = [("1270s", "AQUINAS", hexc("#8a2a2a")), ("1927", "RUSSELL", BLUE), ("TODAY", "YOU", GREEN)]
    for k, (yr, who, col) in enumerate(stops):
        st = A("g10") + 0.35 * k
        if t < st:
            continue
        kk = appear(t, st, 0.35)
        x = 140 + k * 220
        cr.save()
        cr.translate(x, 420)
        cr.scale(kk, kk)
        cr.arc(0, 0, 80, 0, 2 * math.pi)
        paint(cr, rad(-20, -25, 100, [(0, shade(col, 0.45)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, yr, 0, 14, 40 if len(yr) > 4 else 46, WHITE)
        bold_text(cr, who, 0, 130, 40, col)
        cr.restore()
        if k:
            stroke_line(cr, [(x - 140, 420), (x - 90, 420)], 8, OUTLINE, curve=False)
    sign(cr, t, A("g10", "still"), 360, 160, "STILL DEBATED", col=PURPLE, size=62)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W / 2, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#6a4a2e")), (1, hexc("#2e1e14"))]))
    cr.fill()
    cr.rectangle(W / 2, 0, W / 2, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#3a4a6e")), (1, hexc("#1a2238"))]))
    cr.fill()
    person(cr, t, 180, 920, 0.82, "aquinas", eyes="happy", mouth="smile", arms=("hold", "down"), hold=book)
    person(cr, t, 540, 920, 0.82, "russell", eyes="half", mouth="smug", arms=("chin", "down"), facing=-1)
    sign(cr, t, A("g11"), 360, 140, "WHO WINS?", col=GOLD, size=70)
    buttons(cr, t, A("g11", "Aquinas,"), [("AQUINAS", hexc("#c9900c")), ("RUSSELL", BLUE)], y=290)
    sign(cr, t, A("g11", "respectful"), 360, 430, "KEEP IT RESPECTFUL", col=PINK, size=44, rot=0.03)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "aquinas": scene_aquinas, "chain": scene_chain, "first": scene_first,
          "dominoes": scene_dominoes, "russell": scene_russell, "reply": scene_reply, "still": scene_still,
          "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
