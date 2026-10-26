"""Big question 4: "She Tried to Stop Her Parents From Meeting" -- the grandfather paradox with a girl and her garage
time machine, in the polished look.

Script: out/scripts_big_questions_batch1.md, row 70 (owner approved 18 Oct 2026). Two physicists' answers, both ideas
rather than proven facts: the Novikov self-consistency principle (the past "fixes itself") and David Deutsch's
many-worlds view (1991: the traveller lands in another branch). Turbo stock female narrator with tags; the girl
through Turbo with a Kokoro reference voice.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, knot, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "g5"          # music drops out under this line (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"girl": dict(voice="af_sky", speed=1.05, turbo_ref="af_sky+3")})
GIRL = dict(skin="brown", hair="curly", hair_col=hexc("#1e130d"), shirt=hexc("#7a5bd0"), tie=None,
            pants=hexc("#2f3550"))
CYAN = hexc("#6ee6ff")

SCRIPT = [
    dict(id="g2", scene="plan", text="I'll go back, and stop my parents from meeting. Just to see what happens. "
                                     "[chuckle]", speaker="girl"),
    dict(id="g1", scene="garage", text="A girl just finished her time machine. Her first plan is terrible."),   # re-cut
    dict(id="g3", scene="fade", text="Think about it. If they never meet, she's never born."),
    dict(id="g4", scene="vanish", text="If she's never born, she never builds the machine. So nobody stops them."),
    dict(id="g5", scene="loop", text="So they meet. She's born. She goes back. And stops them again.", gap=0.45),
    dict(id="g6", scene="named", text="It's called the grandfather paradox. And physicists take it seriously."),
    dict(id="g7", scene="fixed", text="One idea. The past fixes itself. Whatever she tries, her parents meet anyway."),
    dict(id="g8", scene="branch", text="Another idea. She lands in a different branch of the universe, where she's "
                                       "never born. Her own world is untouched."),
    dict(id="g9", scene="shrug", text="Either way, she can't erase herself. [laugh]"),
    dict(id="g10", scene="end", text="So which is it? A past you can't change, or a second world?", gap=0.3),
]

METADATA = dict(
    title="She Went Back in Time to Stop Her Parents Meeting ⏳",
    alt_titles=["The Time Travel Plan That Breaks Reality ⏳ (Grandfather Paradox)",
                "If You Stop Your Parents Meeting, Who Stops Them? ⏳"],
    description="""A girl finishes her time machine, and her first plan is terrible: go back and stop her parents from meeting. ⏳

If they never meet, she's never born. If she's never born, she never builds the machine, so nobody stops them. So they meet, she's born, she goes back... and stops them again.

It's called the grandfather paradox, and physicists take it seriously. One idea: the past fixes itself (whatever she tries, her parents meet anyway). Another: she lands in a different branch of the universe where she's never born, and her own world is untouched. Neither is proven.

💬 Which is it: a past you can't change, or a second world? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#TimeTravel", "#Paradox", "#Shorts"],
    tags=["grandfather paradox", "time travel paradox", "time machine", "parallel universe", "many worlds",
          "novikov self consistency", "paradox", "science", "mind blowing", "interestingly strange"],
    pinned_comment="A past you can't change ⏳ or a second world 🌍? Pick one and say why 👇",
)


def girl(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("girl", t) else "smile")
    person(cr, t, x, y, s, "kid", **dict(GIRL, **kw))


def machine(cr, t, x, y, s=1.0, on=1.0, dial="2008", a=1.0):
    """A home-made time machine: a booth with a glowing ring, wires and a date dial. (x, y) = bottom centre."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.push_group()
    soft_disc(cr, 0, -230, 260 * max(0.05, on), (0.43, 0.9, 1.0, 0.35 * on))
    rrect(cr, -130, -440, 260, 440, 30)
    paint(cr, lin(-130, 0, 130, 0, [(0, hexc("#5a6a88")), (0.5, hexc("#8a9ab8")), (1, hexc("#4a5a78"))]), OUTLINE, 6)
    cr.arc(0, -260, 92, 0, 2 * math.pi)
    paint(cr, hexc("#0c1a2a"), OUTLINE, 6)
    for k in range(3):                                              # the swirling portal
        cr.arc(0, -260, 80 - k * 22, t * (3 + k) % (2 * math.pi), t * (3 + k) % (2 * math.pi) + 4.2)
        paint(cr, None, alpha(CYAN, on * (0.9 - 0.25 * k)), 8)
    rrect(cr, -80, -420, 160, 60, 10)                               # date dial
    paint(cr, hexc("#1a1a22"), OUTLINE, 4)
    bold_text(cr, dial, 0, -378, 40, (1, 0.35, 0.3, 1), outline=None, shadow=0)
    for k in range(3):
        cr.arc(-80 + k * 80, -100, 16, 0, 2 * math.pi)
        paint(cr, (RED, GOLD, GREEN)[k], OUTLINE, 4)
    stroke_line(cr, [(130, -60), (190, -20), (230, -60)], 6, hexc("#2b2b33"))
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def garage(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#3a3a48")), (0.64, hexc("#4a4a5a")), (0.64, hexc("#6a6a72")),
                                   (1, hexc("#48484e"))]))
    cr.fill()
    for k in range(6):                                              # garage door slats
        rrect(cr, 40, 120 + k * 70, 640, 56, 6)
        paint(cr, hexc("#5a5a6a"), alpha(OUTLINE, 0.5), 3)
    rrect(cr, 60, 700, 160, 120, 8)                                  # toolbox
    paint(cr, RED, OUTLINE, 5)
    soft_disc(cr, 360, 300, 360, (1, 0.95, 0.8, 0.12))


def photo(cr, x, y, s=1.0, fade=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.06)
    cr.scale(s, s)
    rrect(cr, -130, -160, 260, 320, 8)
    paint(cr, WHITE, OUTLINE, 6)
    rrect(cr, -110, -140, 220, 220, 4)
    paint(cr, hexc("#cfe8ff"), None)
    cr.rectangle(-110, -140, 220, 220)
    cr.clip()
    cr.push_group()
    person(cr, 0, 0, 160, 0.42, "kid", eyes="happy", mouth="grin", arms=("wave", "down"), shadow=False,
           **{k: v for k, v in GIRL.items()})
    cr.pop_group_to_source()
    cr.paint_with_alpha(1 - fade)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_garage(cr, t, tl):
    A = tl.at
    garage(cr, t)
    on = max(0.05, seg(t, 0.0, 0.6))
    machine(cr, t, 470, 1000, 1.0, on=on)
    if t < 0.6:
        sparkles(cr, t, 0.0, 470, 740, n=8, seed=2, col=CYAN, spread=160)
    girl(cr, t, None, 180, 1000, 0.85, eyes="happy", mouth="grin", arms=("up", "hips"))
    if t >= A("g1", "terrible."):
        stamp(cr, t, A("g1", "terrible."), 360, 560, "TERRIBLE PLAN", col=RED, size=62)
    vignette(cr, 0.45)


def scene_plan(cr, t, tl):
    A = tl.at
    garage(cr, t)
    machine(cr, t, 500, 1000, 0.95, dial="2008")
    cr.save()
    enter(cr, camera(t, [(A("g2") - 0.3, (1.25, 240, 640))]))
    girl(cr, t, tl, 200, 1000, 0.9, eyes="half", brows="raise", arms=("point", "hips"))
    cr.restore()
    card(cr, t, A("g2", "stop"), 360, 430, 560, 130, "MISSION", ["STOP MY PARENTS MEETING"], col=RED, title_size=34,
         line_size=34)
    vignette(cr, 0.45)


def scene_fade(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=3)
    f = seg(t, A("g3", "born."), A("g3", "born.", end=True) + 0.6)
    photo(cr, 360, 600, 1.4, fade=f)
    sign(cr, t, A("g3", "never"), 360, 200, "PARENTS NEVER MEET", col=PURPLE, size=52, end=A("g3", "she's") - 0.05)
    sign(cr, t, A("g3", "she's"), 360, 200, "SHE'S NEVER BORN", col=RED, size=58)
    vignette(cr, 0.45)


def scene_vanish(cr, t, tl):
    A = tl.at
    garage(cr, t)
    a = 1 - seg(t, A("g4", "machine."), A("g4", "machine.") + 0.6)
    machine(cr, t, 360, 1000, 1.0, a=a)
    if a < 1:
        sparkles(cr, t, A("g4", "machine."), 360, 760, n=10, seed=5, col=CYAN, spread=180)
    sign(cr, t, A("g4", "never"), 360, 200, "NO GIRL = NO MACHINE", col=BLUE, size=52, end=A("g4", "nobody") - 0.05)
    sign(cr, t, A("g4", "nobody"), 360, 200, "NOBODY STOPS THEM", col=GREEN, size=56)
    vignette(cr, 0.45)


def scene_loop(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=4)
    knot(cr, t, A("g5"), 360, 580, r=200, col=GOLD)
    steps = [("meet.", "THEY MEET", 360, 330), ("born.", "SHE'S BORN", 600, 580), ("back.", "SHE GOES BACK", 360, 830),
             ("again.", "STOPS THEM", 120, 580)]
    for (key, label, x, y), col in zip(steps, (GREEN, BLUE, PURPLE, RED)):
        if t >= A("g5", key):
            tag(cr, t, A("g5", key), x, y, label, col=col, size=36)
    sign(cr, t, A("g5", "again."), 360, 180, "FOREVER?", col=RED, size=70)
    vignette(cr, 0.4)


def scene_named(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b1f4a"), hexc("#5a3a6e"), seed=5)
    person(cr, t, 360, 1000, 0.8, "grandpa", eyes="happy", mouth="smile", arms=("wave", "down"))
    sign(cr, t, A("g6", "grandfather"), 360, 200, "THE GRANDFATHER PARADOX", col=GOLD, size=46)
    if t >= A("g6", "physicists"):
        tag(cr, t, A("g6", "physicists"), 360, 330, "PHYSICISTS TAKE IT SERIOUSLY", col=BLUE, size=38)
    vignette(cr, 0.4)


def scene_fixed(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8a0"), hexc("#fff1d6"), seed=6)
    meet = seg(t, A("g7", "Whatever"), A("g7", "anyway.", end=True))
    person(cr, t, lerp(120, 300, meet), 1000, 0.85, "dad", eyes="happy", mouth="smile", arms=("down", "down"),
           walk=t * 8 if meet < 1 else None)
    person(cr, t, lerp(600, 420, meet), 1000, 0.85, "mother", eyes="happy", mouth="smile", arms=("down", "down"),
           facing=-1, walk=t * 8 if meet < 1 else None)
    trip = seg(t, A("g7", "tries,"), A("g7", "tries,") + 0.5)
    girl(cr, t, None, 360, 1060, 0.5, eyes="x" if trip > 0.5 else "open", mouth="o", tilt=-1.2 * trip,
         arms=("up", "up"))
    if meet >= 1:
        soft_disc(cr, 360, 520, 60, (1, 0.4, 0.5, 0.5))
        bold_text(cr, "MET!", 360, 540, 60, RED)
    card(cr, t, A("g7", "idea."), 360, 260, 560, 130, "IDEA 1", ["THE PAST FIXES ITSELF"], col=GREEN, title_size=34,
         line_size=36)
    vignette(cr, 0.3)


def scene_branch(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#0c1028"), hexc("#2a2f5a"), seed=7)
    split = seg(t, A("g8", "branch"), A("g8", "branch") + 0.8)
    stroke_line(cr, [(360, 1000), (360, 700)], 14, GOLD, curve=False)
    stroke_line(cr, [(360, 700), (lerp(360, 180, split), lerp(700, 420, split))], 14, GOLD, curve=False)
    stroke_line(cr, [(360, 700), (lerp(360, 540, split), lerp(700, 420, split))], 14, CYAN, curve=False)
    if split >= 1:
        bold_text(cr, "HER WORLD", 180, 380, 34, GOLD)
        bold_text(cr, "NEW WORLD", 540, 380, 34, CYAN)
        person(cr, t, 540, 560, 0.35, "kid", eyes="open", mouth="o", arms=("shrug", "shrug"), **GIRL)
    if t >= A("g8", "untouched."):
        tag(cr, t, A("g8", "untouched."), 180, 470, "UNTOUCHED", col=GREEN, size=34)
    card(cr, t, A("g8", "idea."), 360, 230, 560, 130, "IDEA 2", ["A SECOND WORLD"], col=BLUE, title_size=34,
         line_size=40)
    vignette(cr, 0.35)


def scene_shrug(cr, t, tl):
    A = tl.at
    garage(cr, t)
    machine(cr, t, 500, 1000, 0.9)
    girl(cr, t, None, 220, 1000, 0.9, eyes="happy", mouth="grin", arms=("shrug", "shrug"))
    sign(cr, t, A("g9", "erase"), 360, 220, "CAN'T ERASE HERSELF", col=GOLD, size=54)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    machine(cr, t, 360, 1000, 0.75)
    sign(cr, t, A("g10", "which"), 360, 200, "WHICH IS IT?", col=GOLD, size=66)
    buttons(cr, t, A("g10", "past"), [("FIXED PAST", GREEN), ("NEW WORLD", BLUE)], y=380, size=44)
    vignette(cr, 0.3)


SCENES = {"garage": scene_garage, "plan": scene_plan, "fade": scene_fade, "vanish": scene_vanish, "loop": scene_loop,
          "named": scene_named, "fixed": scene_fixed, "branch": scene_branch, "shrug": scene_shrug, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("STOP MY PARENTS", False), ("MEETING?", True)], end=tl.at("g3"), y=170, size=96)
    captions(cr, t, tl)
