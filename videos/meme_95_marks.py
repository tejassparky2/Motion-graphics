"""Meme M1: "Me: I got 95/100!" / "Dad:" ... "Where are the other five marks?" -- ~7 s loop.

Original meme in our own characters (owner picked M1, M3, M6 on 11 Oct 2026; out/scripts_batch_47-50.md doc,
"Meme Shorts"). No narrator: a top caption bar, one line from Dad, our own sound hits. The last frame cuts back to
the first, so it loops.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.meme import (garden, hole, living_room, magnifier, meme_bar, metal_detector, report_card, sofa, torch)
from motion.pkit import GOLD, sparkles
from motion.polish import appear, captions, vignette
from motion.toons import person

NARRATOR = dict(speed=0.92)
TAIL = 0.15
voice.SPEAKERS.update({"dad": dict(voice="am_onyx", speed=0.98, pitch=-1.0)})

SCRIPT = [
    dict(id="m1", scene="report", text="", hold=1.5),
    dict(id="m2", scene="turn", text="", hold=0.9),
    dict(id="m3", scene="search", text="Where are the other five marks?", speaker="dad", pace=0.95),
    dict(id="m4", scene="search", text="", hold=0.5),
    dict(id="m5", scene="garden", text="", hold=2.0),
]

METADATA = dict(
    title="Me: 95/100. Dad: Where Are the Other 5? 😭",
    alt_titles=["95 Out of 100… Dad Wasn't Happy 😭", "Every Indian Dad After 95% 😂"],
    description="""Me: I got 95/100! 🎉
Dad: Where are the other five marks? 🔦

Tag the dad who'd do this 😂👇

🔔 Interestingly Strange: strange stories, school memes, mind-bending paradoxes and weird history, animated.""",
    hashtags=["#Memes", "#SchoolMemes", "#Shorts"],
    tags=["school memes", "indian parents", "95 marks", "where are the other 5 marks", "dad memes", "relatable",
          "funny shorts", "exam memes", "animated memes", "interestingly strange"],
    pinned_comment="Tag the person whose dad does this 😂👇",
)


def scene_report(cr, t, tl):
    living_room(cr)
    sofa(cr, 230, 1000, 0.75)
    person(cr, t, 170, 990, 0.85, "dad", eyes="half", mouth="flat", arms=("hold", "hold"))   # behind the paper
    # newspaper up, hiding Dad's face
    cr.rectangle(70, 620, 230, 200)
    cr.set_source_rgba(0.96, 0.95, 0.9, 1)
    cr.fill_preserve()
    cr.set_line_width(5)
    cr.set_source_rgba(0.1, 0.1, 0.1, 1)
    cr.stroke()
    for k in range(5):
        cr.rectangle(90, 645 + k * 32, 190, 10)
        cr.set_source_rgba(0.3, 0.3, 0.3, 0.5)
        cr.fill()
    u = ease_out(seg(t, 0, 0.6))
    x = lerp(640, 520, u)        # the kid bursts in from the right, already moving at frame 0
    person(cr, t, x, 1000, 0.85, "kid", eyes="happy", mouth="grin", arms=("up", "down"),
           walk=t * 12 if u < 1 else None, facing=-1)
    report_card(cr, x - 10, 520 + math.sin(t * 9) * 6, 1.0, rot=0.08)
    sparkles(cr, t, 0.2, x - 10, 520, n=7, seed=3, col=GOLD, spread=150)
    meme_bar(cr, t, 0.0, ["Me: I got 95/100!"])
    vignette(cr, 0.3)


def scene_turn(cr, t, tl):
    A = tl.at
    s0 = A("m2")
    living_room(cr)
    sofa(cr, 230, 1000, 0.75)
    u = ease_out(seg(t, s0, s0 + 0.5))
    cr.save()
    cr.translate(170, 600)          # slow push-in on Dad's face
    k = 1 + 0.9 * u
    cr.scale(k, k)
    cr.translate(-170 + 75 * u, -600 + 40 * u)
    person(cr, t, 170, 990, 0.85, "dad", eyes="angry" if u > 0.6 else "half", mouth="flat", brows="angry",
           arms=("down", "down"))
    cr.restore()
    person(cr, t, 520, 1000, 0.85, "kid", eyes="happy", mouth="grin", arms=("up", "down"), facing=-1)
    report_card(cr, 510, 520, 1.0, rot=0.08)
    cue("thud", t, s0)
    meme_bar(cr, t, s0, ["Dad:"])
    vignette(cr, 0.45)


def scene_search(cr, t, tl):
    A = tl.at
    s0 = A("m3")
    living_room(cr)
    lift = ease_out(seg(t, s0, s0 + 0.4))
    sofa(cr, 330, 1010, 0.8, cushion_lift=lift)
    talk = tl.speaking("dad", t)
    person(cr, t, 210, 1000, 0.85, "dad", eyes="wide", mouth="talk" if talk else "o", brows="angry",
           arms=("hold", "hold"), tilt=0.35, hold=lambda c, hx, hy: torch(c, hx, hy))
    magnifier(cr, 430 + math.sin(t * 5) * 20, 880 + math.sin(t * 7) * 10, 1.1)
    person(cr, t, 620, 1000, 0.7, "kid", eyes="half", mouth="flat", arms=("hold", "down"), facing=-1)
    report_card(cr, 600, 760, 0.6, rot=-0.1)
    meme_bar(cr, t, s0 - 0.25, ["Dad:"])
    vignette(cr, 0.4)


def scene_garden(cr, t, tl):
    A = tl.at
    s0 = A("m5")
    garden(cr)
    for x, y in ((150, 900), (470, 870), (330, 1000)):
        hole(cr, x, y)
    person(cr, t, 470, 1020, 0.85, "dad", eyes="wide", mouth="o", brows="angry", arms=("hold", "hold"),
           hold=lambda c, hx, hy: metal_detector(c, hx, hy, t), walk=t * 5)
    # the kid in the lit window, deadpan
    cr.save()
    cr.rectangle(90, 380, 180, 150)
    cr.clip()
    person(cr, t, 180, 760, 0.8, "kid", eyes="half", mouth="flat", arms=("hold", "down"), shadow=False)
    cr.restore()
    for k in range(3):              # beep beep
        cue("pop", t, s0 + 0.3 + k * 0.5)
    if (t - s0) % 0.5 < 0.2:
        cr.arc(560, 760, 14, 0, 2 * math.pi)
        cr.set_source_rgba(1, 0.3, 0.3, 0.9)
        cr.fill()
    meme_bar(cr, t, s0, ["Dad, 2 hours later:"])
    vignette(cr, 0.4)


SCENES = {"report": scene_report, "turn": scene_turn, "search": scene_search, "garden": scene_garden}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    if name != "turn":
        whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
