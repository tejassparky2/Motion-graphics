"""Big question 1: "God Already Knew. So Is It My Fault?" -- the Last Bencher's homework excuse (divine foreknowledge
vs free will), as a classroom scene in the polished look.

Script: out/scripts_big_questions_batch1.md, row 67 (owner approved 18 Oct 2026, after the God-rock video's numbers:
"focus on more video like this which is cotervinal hard to assume arrise questions"). Boethius, The Consolation of
Philosophy, Book V (written in prison, about 524 AD): God is outside time and sees all moments at once, like someone
looking down on a road; knowing an act does not cause it. The cards paraphrase him. God is never shown as a figure,
only as light. Turbo stock female narrator with tags; the kid and sir through Turbo with Kokoro reference voices.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, shake, sparkles, studio, tag
from motion import thriller as th
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, sign, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person, portrait
from videos.last_bencher_4 import classroom, room

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "f3"          # music drops out under this line (research 18 Oct 2026, A5)
SERIES = "The Last Bencher"
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "sir": dict(voice="am_michael", speed=1.0, turbo_ref="am_michael")})

SCRIPT = [
    dict(id="f1", scene="excuse", text="The last bencher hasn't done his homework. And he has the perfect excuse."),
    dict(id="f2", scene="ask", text="Sir, God knows everything, right? So yesterday, God already knew I wouldn't do "
                                    "it.", speaker="kid"),
    dict(id="f3", scene="ask", text="If God knew, I couldn't do anything else. So it's not my fault. [chuckle]",
         speaker="kid", gap=0.45),
    dict(id="f4", scene="silent", text="The class goes silent. Even sir stops writing."),
    dict(id="f5", scene="puzzle", text="Because it's a real puzzle. If someone knows your future for sure, can you "
                                       "still choose?"),
    dict(id="f6", scene="cell", text="Fifteen hundred years ago, a man named Boethius asked the same thing. In "
                                     "prison.", speaker="sir"),
    dict(id="f7", scene="hill", text="His answer. God isn't stuck in time like us. He sees every moment at once, like "
                                     "you see a whole road from a hill.", speaker="sir"),
    dict(id="f8", scene="knowing", text="Seeing you walk doesn't make you walk. Knowing your choice doesn't make it "
                                        "for you.", speaker="sir"),
    dict(id="f9", scene="wink", text="Then God also knows I'm copying from my friend tomorrow.", speaker="kid"),
    dict(id="f10", scene="wink", text="And I know about your detention.", speaker="sir", gap=0.3),
    dict(id="f11", scene="end", text="So, if your whole future is already known, are you still free? Yes, or no?",
         gap=0.3),
]
clear_dialogue(SCRIPT, ids={"f2", "f3", "f7", "f8"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="God Already Knew. So the Kid Says It's Not His Fault 😏",
    alt_titles=["If God Knows Your Future, Are You Free? 🤔", "The Last Bencher's Homework Excuse Broke the Class 😏"],
    description=""""Sir, God knows everything, right? So yesterday, God already knew I wouldn't do my homework. If God knew, I couldn't do anything else. So it's not my fault." 😏

It's a real puzzle: if someone knows your future for sure, can you still choose?

About 1,500 years ago, Boethius asked the same question, in prison. His answer: God isn't stuck in time like us. He sees every moment at once, like you see a whole road from a hill. Seeing you walk doesn't make you walk; knowing your choice doesn't make it for you.

Source: Boethius, The Consolation of Philosophy, Book V (about 524 AD).

💬 If your whole future is already known, are you still free? Yes or no, and why? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#FreeWill", "#Shorts"],
    tags=["free will", "does god know the future", "foreknowledge paradox", "boethius", "the last bencher",
          "philosophy", "teacher vs student", "deep questions", "god paradox", "interestingly strange"],
    pinned_comment="If God already knows what you'll do tomorrow, are you still free? FREE or NOT FREE 👇",
)


def mouth_of(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


def sir(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", mouth_of(tl, "sir", t, kw.pop("rest", "smile")))
    person(cr, t, x, y, s, "sir", **kw)


def notebook(cr, x, y, s=1.0, rot=0.0, empty=True):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -110, -80, 220, 160, 8)
    paint(cr, WHITE, OUTLINE, 5)
    stroke_line(cr, [(0, -80), (0, 80)], 4, OUTLINE, curve=False)
    for k in range(6):
        for sx in (-95, 15):
            stroke_line(cr, [(sx, -55 + k * 22), (sx + 80, -55 + k * 22)], 2, (0.6, 0.7, 0.9, 0.7), curve=False)
    if empty:
        bold_text(cr, "EMPTY", 0, 14, 40, RED)
    cr.restore()


def scene_excuse(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    sir(cr, t, tl, 150, 1120, 1.05, eyes="half", brows="raise", arms=("point", "hips"), rest="flat")
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("f1", "excuse."), (1.15, 420, 640))], dur=0.8))
    classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross"), eyes="half", mouth="smug", brows="raise"))
    cr.restore()
    notebook(cr, 520, 760, 0.8, -0.08)
    if t >= A("f1", "perfect"):
        tag(cr, t, A("f1", "perfect"), 360, 560, "THE PERFECT EXCUSE", col=PURPLE, size=44)
    vignette(cr, 0.45)


def scene_ask(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("f2") - 0.3, (2.0, 555, 470)), (A("f3"), (2.05, 575, 470))], dur=0.8))
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down") if t < A("f3") else ("cross", "cross"), eyes="open",
                                       mouth=mouth_of(tl, "kid", t, "smug"), brows="raise"))
    cr.restore()
    soft_disc(cr, 190, 330, 150, (1, 0.95, 0.7, 0.35 + 0.1 * math.sin(t * 3)))      # God as light only
    bold_text(cr, "GOD KNEW", 190, 345, 46, GOLD)
    if t >= A("f3"):
        card(cr, t, A("f3", "couldn't"), 360, 760, 560, 150, "GOD KNEW", ["SO NO CHOICE?"], col=RED,
             title_size=40, line_size=44)
    vignette(cr, 0.45)


def scene_silent(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    frozen = t >= A("f4", "stops")
    classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross"), eyes="happy", mouth="smug"), look_at=(560, 0),
              gasp=True)
    cr.save()
    if frozen:
        dx, dy = shake(t, A("f4", "stops"), 0.3, 6)
        cr.translate(dx, dy)
    sir(cr, t, tl, 150, 1120, 1.05, eyes="wide", rest="o", brows="up", arms=("write", "down"), sweat=frozen)
    cr.restore()
    stamp(cr, t, A("f4", "silent."), 360, 170, "SILENCE", col=BLUE, size=84)
    vignette(cr, 0.45)


def scene_puzzle(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=3)
    for k in range(5):                                             # a road of tomorrow's moments, all lit
        x = 140 + k * 110
        cr.arc(x, 560 - 30 * math.sin(k), 34, 0, 2 * math.pi)
        paint(cr, alpha(GOLD, 0.25 + 0.15 * k), OUTLINE, 4)
    stroke_line(cr, [(100, 600), (240, 520), (360, 600), (480, 520), (620, 600)], 8, alpha(WHITE, 0.6))
    sign(cr, t, A("f5", "real"), 360, 190, "A REAL PUZZLE", col=GOLD, size=60, end=A("f5", "If") - 0.05)
    card(cr, t, A("f5", "If"), 360, 330, 600, 190, "FUTURE KNOWN FOR SURE", ["CAN YOU STILL CHOOSE?"], col=PURPLE,
         title_size=40, line_size=42)
    vignette(cr, 0.4)


def scene_cell(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2a2a32")), (1, hexc("#14141a"))]))
    cr.fill()
    rrect(cr, 440, 160, 180, 160, 8)                               # high window with moonlight
    paint(cr, hexc("#1a2a4a"), OUTLINE, 5)
    for k in range(3):
        stroke_line(cr, [(480 + k * 50, 160), (480 + k * 50, 320)], 8, OUTLINE, curve=False)
    soft_disc(cr, 360, 760, 360, (0.6, 0.7, 1.0, 0.12))
    rrect(cr, 300, 820, 300, 30, 6)                                # desk
    paint(cr, hexc("#5a3a20"), OUTLINE, 5)
    person(cr, t, 330, 1000, 0.95, "zeno", eyes="half", mouth="flat", arms=("write", "write"), look=(0.4, 0.6))
    rrect(cr, 420, 780, 120, 40, 4)
    paint(cr, hexc("#f2ead6"), OUTLINE, 3)
    for k in range(7):                                             # cell bars in front
        x = 40 + k * 108
        stroke_line(cr, [(x, 80), (x, 1150)], 16, OUTLINE, curve=False)
        stroke_line(cr, [(x, 80), (x, 1150)], 9, hexc("#6a6a7a"), curve=False)
    tag(cr, t, A("f6", "Boethius"), 360, 200, "BOETHIUS, ABOUT 524 AD", col=hexc("#a8713e"), size=40)
    if t >= A("f6", "prison."):
        stamp(cr, t, A("f6", "prison."), 360, 560, "IN PRISON", col=RED, size=60)
    portrait(cr, t, A("f6"), 600, 470, 70, "sir", mouth=mouth_of(tl, "sir", t), eyes="open", bg=hexc("#9fc8ef"),
             end=A("f6", end=True))
    vignette(cr, 0.55)


def scene_hill(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#9fd6ff")), (0.5, hexc("#e8f6ff")), (0.5, hexc("#8fd06a")),
                                   (1, hexc("#4f9a4a"))]))
    cr.fill()
    pts = [(80 + 560 * (k / 20), 700 + 300 * (k / 20) + 70 * math.sin(k / 20 * 9)) for k in range(21)]
    stroke_line(cr, pts, 46, hexc("#7a7a86"))
    stroke_line(cr, pts, 6, (1, 1, 1, 0.8))
    for k in range(5):                                             # cars at every point of the road, all at once
        j = 2 + k * 4
        x, y = pts[j]
        rrect(cr, x - 22, y - 14, 44, 26, 8)
        paint(cr, (RED, BLUE, GOLD, GREEN, PURPLE)[k], OUTLINE, 3)
    if t >= A("f7", "every"):                                      # the view from above: light, not a figure
        u = appear(t, A("f7", "every"), 0.5)
        soft_disc(cr, 360, 340, 160 * u, (1, 0.95, 0.7, 0.6))
        for x, y in pts[2::4]:
            stroke_line(cr, [(360, 360), (x, y)], 3, (1, 0.9, 0.5, 0.35 * u), curve=False)
    sign(cr, t, A("f7", "time"), 360, 170, "NOT STUCK IN TIME", col=BLUE, size=56, end=A("f7", "every") - 0.05)
    sign(cr, t, A("f7", "every"), 360, 170, "EVERY MOMENT AT ONCE", col=GOLD, size=50)
    vignette(cr, 0.3)


def scene_knowing(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=5)
    x = lerp(140, 560, seg(t, A("f8"), A("f8", end=True)))
    person(cr, t, x, 980, 0.8, "kid", eyes="happy", mouth="smile", arms=("down", "down"), walk=t * 9)
    soft_disc(cr, 360, 330, 110, (1, 0.95, 0.7, 0.4))
    card(cr, t, A("f8", "Seeing"), 360, 540, 620, 150, "SEEING YOU WALK", ["DOESN'T MAKE YOU WALK"], col=BLUE,
         end=A("f8", "Knowing") - 0.05, title_size=40, line_size=40)
    card(cr, t, A("f8", "Knowing"), 360, 540, 620, 150, "KNOWING YOUR CHOICE", ["DOESN'T MAKE IT FOR YOU"],
         col=GREEN, title_size=40, line_size=40)
    vignette(cr, 0.4)


def scene_wink(cr, t, tl):
    A = tl.at
    room(cr, t)
    if t < A("f10"):
        cr.save()
        enter(cr, camera(t, [(A("f9") - 0.3, (2.0, 555, 470))]))
        wink = seg(t, A("f9", "tomorrow.", end=True) - 0.1, A("f9", "tomorrow.", end=True) + 0.1)
        classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross"), eyes="half" if wink > 0.5 else "open",
                                           mouth=mouth_of(tl, "kid", t, "grin"), brows="raise"))
        cr.restore()
        tag(cr, t, A("f9", "copying"), 360, 200, "COPYING TOMORROW", col=PURPLE, size=44)
    else:
        room(cr, t, board=True)
        cr.save()
        enter(cr, camera(t, [(A("f10") - 0.1, (1.6, 300, 560))]))
        sir(cr, t, tl, 300, 900, 1.0, eyes="happy", rest="smug", arms=("hips", "point"))
        cr.restore()
        stamp(cr, t, A("f10", "detention."), 360, 230, "DETENTION", col=RED, size=80)
        cue("hit", t, A("f10", "detention."))
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    soft_disc(cr, 360, 620, 130, (1, 0.95, 0.7, 0.45))
    person(cr, t, 360, 900, 0.6, "kid", eyes="open", mouth="o", arms=("shrug", "shrug"))
    sign(cr, t, A("f11", "free?"), 360, 200, "STILL FREE?", col=GOLD, size=66)
    buttons(cr, t, A("f11", "Yes,"), [("FREE", GREEN), ("NOT FREE", RED)], y=380, size=48)
    vignette(cr, 0.3)


SCENES = {"excuse": scene_excuse, "ask": scene_ask, "silent": scene_silent, "puzzle": scene_puzzle,
          "cell": scene_cell, "hill": scene_hill, "knowing": scene_knowing, "wink": scene_wink, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("GOD ALREADY", False), ("KNEW", True)], end=tl.at("f2"), y=170, size=110)
    captions(cr, t, tl)
