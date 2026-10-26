"""Big question: "Would You Press It?" -- a man who just lost his job meets a booth that offers a perfect life, in the
polished look. Original story around a real thought experiment and a real study.

Owner, 20 Oct 2026: "Make more 2 auto approved be creative be controversy ...". Robert Nozick's experience machine,
Anarchy, State, and Utopia (1974): most people say they would not plug in, because we want to actually do things, not
just have the experience of doing them. Felipe De Brigard, "If you like it, does it matter if it's real?",
Philosophical Psychology 23 (2010): told they were ALREADY plugged in, 46% of 72 students chose to stay (54% unplug);
told their real life was in a maximum-security prison, 87% stayed. De Brigard reads this as status-quo bias. Turbo
stock female narrator with tags; the booth through Turbo with a Kokoro reference voice.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter, lin,
                           paint, rad, rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "b7"          # music drops out when the question flips (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"booth": dict(voice="am_onyx", speed=0.95, turbo_ref="am_onyx")})
MAN = dict(skin="tan", hair="short", hair_col=hexc("#1e130d"), shirt=hexc("#cfe2f8"), suit=None,
           pants=hexc("#3a3e48"), tie=hexc("#8a2a2a"), shoes=hexc("#2b1d16"), build="adult", stache=None)
NEON = hexc("#5af0ff")

SCRIPT = [
    dict(id="b2", scene="booth", text="Press the button. Live the perfect life. Forever.", speaker="booth"),
    dict(id="b1", scene="street", text="A man just lost his job. And this booth just lit up."),   # re-cut 26 Oct
    dict(id="b3", scene="dream", text="A dream job. A full house. His mother, healthy again. [sigh]"),
    dict(id="b4", scene="catch", text="The catch? None of it is real. Once inside, you forget it's a machine."),
    dict(id="b5", scene="nozick", text="The philosopher Robert Nozick asked this in [nineteen seventy four.|1974.]"),
    dict(id="b6", scene="nozick", text="Most people say no. We want to really live, not just feel like we did."),
    dict(id="b7", scene="pod", text="But then, a researcher flipped the question.", gap=0.35),
    dict(id="b8", scene="pod", text="You're already inside the machine. This life is the fake one. Do you unplug?"),
    dict(id="b9", scene="stay", text="Almost half said: stay."),
    dict(id="b10", scene="prison", text="Told their real life was a prison? Nearly nine in ten stayed. [gasp]"),
    dict(id="b11", scene="habit", text="So maybe we don't love what's real. We love what we're used to."),
    dict(id="b12", scene="end", text="His finger is on the button. Would you press it, or walk away?", gap=0.3),
]

METADATA = dict(
    title="A Booth Offered Him a Perfect Life. One Catch 🔘",
    alt_titles=["Would You Press the Button for a Perfect Life? 🔘", "Almost Half Chose the Fake Life 🔘"],
    description="""A man just lost his job. On his way home, a strange booth lights up: "Press the button. Live the perfect life. Forever." 🔘

A dream job. A full house. His mother, healthy again. The catch: none of it is real, and once inside, you forget it's a machine.

Robert Nozick asked this in 1974 (the "experience machine"). Most people say no: we want to really live, not just feel like we did.

But in 2010, Felipe De Brigard flipped the question: you're ALREADY inside the machine, and this life is the fake one. Do you unplug? Almost half (46%) said stay. Told their real life was a prison, 87% stayed.

So maybe we don't love what's real. We love what we're used to.

Sources: Robert Nozick, Anarchy, State, and Utopia (1974); Felipe De Brigard, "If you like it, does it matter if it's real?", Philosophical Psychology (2010).

💬 Would you press it, or walk away? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#ExperienceMachine", "#Philosophy", "#Shorts"],
    tags=["experience machine", "would you press the button", "perfect life machine", "robert nozick",
          "simulation", "is reality better", "thought experiment", "philosophy", "would you rather",
          "interestingly strange"],
    pinned_comment="PRESS or WALK AWAY? And if you were already inside... would you unplug? 👇",
)


# ---------------------------------------------------------------- props
def man(cr, t, tl, x, y, s=0.9, **kw):
    person(cr, t, x, y, s, "fermi", **dict(MAN, **kw))


def box(cr, hx, hy):
    """The cardboard box of desk things he carries home."""
    rrect(cr, hx - 70, hy - 20, 140, 90, 6)
    paint(cr, lin(0, hy - 20, 0, hy + 70, [(0, hexc("#d8b07a")), (1, hexc("#b88a52"))]), OUTLINE, 5)
    rrect(cr, hx - 50, hy - 52, 30, 40, 4)                         # a plant pot
    paint(cr, hexc("#c86a3a"), OUTLINE, 3.5)
    ellipse(cr, hx - 35, hy - 62, 22, 14)
    paint(cr, hexc("#4aa860"), OUTLINE, 3.5)
    rrect(cr, hx, hy - 46, 46, 34, 4)                              # a photo frame
    paint(cr, WHITE, OUTLINE, 3.5)


def street(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#141a3a")), (0.62, hexc("#2a2f5a")), (0.62, hexc("#3a3a48")),
                                   (1, hexc("#24242e"))]))
    cr.fill()
    for k, (bx, bw, bh) in enumerate([(-20, 170, 360), (140, 150, 470), (280, 190, 300), (460, 160, 420),
                                       (610, 150, 340)]):
        rrect(cr, bx, 794 - bh, bw, bh, 4)                          # dark buildings
        paint(cr, hexc("#1c2246"), alpha(OUTLINE, 0.6), 3)
        for wy in range(int(794 - bh + 30), 770, 60):
            for wx in range(int(bx + 20), int(bx + bw - 30), 45):
                lit = (k * 7 + wx // 45 + wy // 60) % 4 == 0
                rrect(cr, wx, wy, 22, 30, 3)
                paint(cr, hexc("#ffd98a") if lit else hexc("#262c58"), None, 0)
    for lx in (90, 420):                                           # street lamps
        stroke_line(cr, [(lx, 794), (lx, 520)], 8, hexc("#555a6a"), curve=False)
        soft_disc(cr, lx, 520, 90, (1, 0.85, 0.5, 0.18))
        ellipse(cr, lx, 518, 18, 10)
        paint(cr, hexc("#ffe8a8"), OUTLINE, 3)


def booth(cr, t, x, y, s=1.0, glow=1.0, press=0.0):
    """A glowing kiosk with one big button; (x, y) = its base."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, -230, 260, (NEON[0], NEON[1], NEON[2], 0.18 * glow + 0.04 * math.sin(t * 4)))
    rrect(cr, -110, -460, 220, 460, 26)
    paint(cr, lin(-110, 0, 110, 0, [(0, hexc("#2a2f5a")), (1, hexc("#3e4680"))]), OUTLINE, 6)
    rrect(cr, -84, -430, 168, 120, 12)                             # screen
    paint(cr, lin(0, -430, 0, -310, [(0, hexc("#0e2a3a")), (1, hexc("#14465a"))]), NEON, 4)
    bold_text(cr, "PERFECT", 0, -380, 34, NEON, outline=None, shadow=0)
    bold_text(cr, "LIFE", 0, -340, 34, NEON, outline=None, shadow=0)
    r = 46 * (1 - 0.15 * press)
    soft_disc(cr, 0, -200, 80, (1, 0.3, 0.3, 0.25 + 0.15 * math.sin(t * 6)))
    cr.arc(0, -200, r, 0, 2 * math.pi)                             # THE button
    paint(cr, rad(-12, -212, r, [(0, hexc("#ff8a7a")), (1, hexc("#d8202a"))]), OUTLINE, 5)
    bold_text(cr, "PRESS", 0, -110, 30, WHITE, outline=None, shadow=0)
    cr.restore()


def mother(cr, t, x, y, s, **kw):
    person(cr, t, x, y, s, "mother", **kw)


def dream_world(cr, t, k=1.0, glitch=0.0, items=3):
    """The perfect life: warm sky, house, hired card, mother healthy and waving. `glitch` greys it and tears it."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#ffb8d0")), (0.6, hexc("#ffe8b8")), (0.6, hexc("#8ad88a")),
                                   (1, hexc("#5ab86a"))]))
    cr.fill()
    soft_disc(cr, 560, 240, 120, (1, 1, 0.8, 0.6))
    if items >= 2:                                                 # the full house
        cr.move_to(70, 580)
        cr.line_to(190, 470)
        cr.line_to(310, 580)
        cr.close_path()
        paint(cr, hexc("#d8473f"), OUTLINE, 5)
        rrect(cr, 90, 580, 200, 190, 6)
        paint(cr, hexc("#fff4e2"), OUTLINE, 5)
        rrect(cr, 165, 680, 50, 90, 4)
        paint(cr, hexc("#8a5a30"), OUTLINE, 4)
    if items >= 3:
        mother(cr, t, 470, 870, 0.62, eyes="happy", mouth="grin", arms=("wave", "down"))
        man(cr, t, None, 600, 880, 0.62, eyes="happy", mouth="grin", arms=("wave", "down"))
    if glitch > 0:
        cr.rectangle(0, 0, W, H)
        cr.set_source_rgba(0.35, 0.35, 0.4, 0.75 * glitch)
        cr.fill()
        for k_ in range(6):                                        # torn scan lines
            yy = (k_ * 197 + int(t * 900)) % H
            cr.rectangle(0, yy, W, 10 + 8 * (k_ % 3))
            cr.set_source_rgba(NEON[0], NEON[1], NEON[2], 0.35 * glitch)
            cr.fill()


def pod(cr, t, x, y, s=1.0, wake=0.0):
    """A glass capsule with the man asleep inside, cables to the top."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for k in range(3):
        stroke_line(cr, [(-60 + k * 60, -520), (-40 + k * 40, -700)], 10, hexc("#2a2f4a"))
    soft_disc(cr, 0, -270, 230, (NEON[0], NEON[1], NEON[2], 0.15))
    rrect(cr, -130, -520, 260, 520, 120)
    paint(cr, alpha(hexc("#bff6ff"), 0.25), NEON, 6)
    person(cr, t, 0, -40, 0.8, "fermi", **dict(MAN, eyes="closed" if wake < 0.5 else "wide",
                                                 mouth="smile" if wake < 0.5 else "o", arms=("down", "down"),
                                                 bob=False))
    rrect(cr, -130, -520, 260, 520, 120)
    paint(cr, None, NEON, 6)
    stroke_line(cr, [(-80, -470), (-60, -340)], 8, alpha(WHITE, 0.5))
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_street(cr, t, tl):
    A = tl.at
    street(cr, t)
    on = 1.0
    booth(cr, t, 520, 1000, 0.95, glow=max(0.25, on))
    walk = t * 7 if t < A("b1", "booth") else None
    mx = 210 + 20 * min(t, A("b1", "booth"))
    man(cr, t, tl, mx, 1010, 0.9, eyes="sad" if t < A("b1", "booth") else "wide",
        mouth="sad" if t < A("b1", "booth") else "o", arms=("hold", "hold"), walk=walk, hold=box,
        look=(0.6, -0.1))
    if t >= A("b1", "job"):
        tag(cr, t, A("b1", "job"), 200, 540, "FIRED TODAY", col=RED, size=40)
    vignette(cr, 0.45)


def scene_booth(cr, t, tl):
    A = tl.at
    street(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("b2"), (1.6, 520, 760)), (A("b2", "Forever"), (1.9, 520, 800))], dur=0.6))
    booth(cr, t, 520, 1000, 0.95, glow=1.0)
    man(cr, t, None, 330, 1010, 0.9, eyes="wide", mouth="o", arms=("hold", "hold"), hold=box, look=(0.7, -0.2))
    cr.restore()
    if tl.speaking("booth", t):                                    # the booth's voice as a waveform
        for k in range(14):
            h = 10 + 40 * abs(math.sin(t * 18 + k * 1.3)) * (0.4 + 0.6 * abs(math.sin(k)))
            rrect(cr, 150 + k * 32, 300 - h / 2, 18, h, 9)
            paint(cr, NEON, None, 0)
    sign(cr, t, A("b2", "Forever"), 360, 210, "FOREVER.", col=PURPLE, size=64)
    vignette(cr, 0.45)


def scene_dream(cr, t, tl):
    A = tl.at
    items = 1 + (t >= A("b3", "full")) + (t >= A("b3", "mother"))
    dream_world(cr, t, items=items)
    card(cr, t, tl.scene_at(t)[1], 200, 300, 300, 150, "NEW JOB", ["YOU'RE HIRED!"], col=GREEN, title_size=34,
         line_size=40, rot=-0.05)
    if t >= A("b3", "full"):
        sparkles(cr, t, A("b3", "full"), 190, 560, n=6, seed=31, col=WHITE)
    if t >= A("b3", "healthy"):
        sign(cr, t, A("b3", "healthy"), 470, 470, "MOM: HEALTHY", col=RED, size=40)
    vignette(cr, 0.25)


def scene_catch(cr, t, tl):
    A = tl.at
    g = seg(t, A("b4", "None"), A("b4", "real", end=True))
    dream_world(cr, t, glitch=g)
    stamp(cr, t, A("b4", "real"), 360, 300, "NOT REAL", col=RED, size=80)
    if t >= A("b4", "forget"):
        tag(cr, t, A("b4", "forget"), 360, 480, "AND YOU FORGET IT'S FAKE", col=PURPLE, size=40)
    if t >= A("b4", "None"):
        cue("sting", t, A("b4", "None"), 0.6)
    vignette(cr, 0.4)


def scene_nozick(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=32)
    card(cr, t, tl.scene_at(t)[1], 360, 300, 460, 220, "ROBERT NOZICK · 1974", ["THE EXPERIENCE", "MACHINE"], col=BLUE,
         title_size=32, line_size=46)
    if t >= A("b6"):
        sign(cr, t, A("b6", "no"), 360, 520, "MOST PEOPLE: NO", col=RED, size=58)
        card(cr, t, A("b6", "really"), 360, 700, 460, 170, "WHY?", ["LIVE IT, DON'T", "JUST FEEL IT"], col=GREEN,
             title_size=32, line_size=40)
    vignette(cr, 0.35)


def scene_pod(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#0e1430"), hexc("#1e2650"), seed=33)
    if t < A("b8"):
        cr.save()                                                  # the question card turns over
        cr.translate(360, 560)
        cr.scale(math.cos(math.pi * seg(t, A("b7", "flipped"), A("b7", "question", end=True))) or 0.01, 1)
        cr.translate(-360, -560)
        card(cr, t, tl.scene_at(t)[1], 360, 560, 460, 240, "THE QUESTION", ["WOULD YOU", "PLUG IN?"], col=BLUE,
             title_size=34, line_size=48)
        cr.restore()
        if t >= A("b7", "flipped"):
            cue("whoosh", t, A("b7", "flipped"), 0.3)
    else:
        cr.save()
        enter(cr, camera(t, [(A("b8"), (1.0, 360, 640)), (A("b8", "fake"), (1.15, 360, 600))], dur=0.6))
        pod(cr, t, 360, 860, 0.95)
        cr.restore()
        if t >= A("b8", "This"):
            tag(cr, t, A("b8", "This"), 360, 180, "THIS LIFE = THE FAKE ONE", col=RED, size=40)
        if t >= A("b8", "fake"):
            sign(cr, t, A("b8", "fake"), 360, 300, "UNPLUG?", col=GOLD, size=64)
    vignette(cr, 0.45)


def scene_stay(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1e2650"), hexc("#3a2f60"), seed=34)
    counter(cr, t, tl.scene_at(t)[1], 360, 500, 46, size=170, dur=0.9, col=NEON, suffix="%", sub="STAYED INSIDE")
    if t >= A("b9", "stay"):
        stamp(cr, t, A("b9", "stay"), 360, 760, "STAY", col=PURPLE, size=70)
    vignette(cr, 0.4)


def scene_prison(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2a2a30"), hexc("#3a3a44"), seed=35)
    if t < A("b10", "Nearly"):
        rrect(cr, 160, 330, 400, 360, 10)
        paint(cr, hexc("#4a4a54"), OUTLINE, 6)
        for k in range(6):                                         # bars
            stroke_line(cr, [(190 + k * 68, 330), (190 + k * 68, 690)], 14, hexc("#9a9aa8"), curve=False)
        tag(cr, t, A("b10", "prison"), 360, 260, "REAL LIFE = PRISON", col=RED, size=44)
    else:
        counter(cr, t, A("b10", "Nearly"), 360, 500, 87, size=170, dur=0.8, col=GOLD, suffix="%",
                sub="STAYED INSIDE")
    vignette(cr, 0.45)


def scene_habit(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8e0"), hexc("#fff0d8"), seed=36)
    card(cr, t, tl.scene_at(t)[1], 190, 470, 300, 220, "WHAT'S REAL", ["THE TRUTH"], col=BLUE, title_size=34,
         mark="x", mark_at=A("b11", "used"))
    card(cr, t, A("b11", "used"), 530, 470, 300, 220, "WHAT WE KNOW", ["OUR LIFE", "RIGHT NOW"], col=GREEN, title_size=34,
         mark="ok", mark_at=A("b11", "used") + 0.3)
    sign(cr, t, A("b11", "love"), 360, 220, "WE LOVE THE FAMILIAR", col=RED, size=48)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    street(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("b12"), (1.15, 470, 700))], dur=0.5))
    reach = seg(t, A("b12"), A("b12", "button", end=True))
    booth(cr, t, 560, 1000, 0.95, press=0.0)
    man(cr, t, None, 330, 1010, 0.9, eyes="half", mouth="flat", arms=((lerp(40, 140, reach),
        lerp(120, 132, reach)), "down"), look=(0.7, -0.2))
    cr.restore()
    if t >= A("b12", "Would"):
        sign(cr, t, A("b12", "Would"), 360, 190, "WOULD YOU PRESS IT?", col=GOLD, size=54)
        buttons(cr, t, A("b12", "press"), [("PRESS", RED), ("WALK AWAY", GREEN)], y=320, size=46)
    vignette(cr, 0.35)


SCENES = {"street": scene_street, "booth": scene_booth, "dream": scene_dream, "catch": scene_catch,
          "nozick": scene_nozick, "pod": scene_pod, "stay": scene_stay, "prison": scene_prison,
          "habit": scene_habit, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("A PERFECT LIFE.", False), ("ONE CATCH.", True)], end=min(tl.at("b3"), tl.at("b2", "Forever") - 0.2), y=150, size=90)
    captions(cr, t, tl)
