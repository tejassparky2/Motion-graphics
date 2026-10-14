"""The Mirror That Never Lies -- genie-style story #3 (out/scripts_genie_style_batch1.md, approved by the owner on
14 Oct 2026). A magic mirror answers every question and never lies; a girl asks "Will your next answer be no?".
Original story; narrated by ElevenLabs Chris.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, check, shake, sparkles, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc,
                           sprite, stamp, stroke_line, vignette)
from motion.rulekit import either_way, mouth, note
from motion.toons import person

NARRATOR = dict(engine="elevenlabs")
TAIL = 0.9
voice.SPEAKERS.update({
    "mirror": dict(el=voice.ELEVEN["lily"], tone="mysterious", fx="aecho=0.8:0.7:45|80:0.3|0.18"),
    "girl": dict(el=voice.ELEVEN["jessica"], pitch=2.0, tone="curious"),
})

SCRIPT = [
    dict(id="m1", scene="mirror", text="A magic mirror answers every question. And it never lies.", tone="mysterious"),
    dict(id="m2", scene="mirror", text="Ask me anything. My answer is always the truth.", speaker="mirror", gap=0.3),
    dict(id="m3", scene="rain", text="Will it rain tomorrow? Yes. And it rains.", gap=0.3),
    dict(id="m4", scene="phone", text="Where's the lost phone? Under the sofa. And it's there."),
    dict(id="m5", scene="ask", text="Then the kid asks one more question.", tone="mischievously"),
    dict(id="m6", scene="ask", text="Will your next answer be no?", speaker="girl", gap=0.4, pace=0.92),
    dict(id="m7", scene="silent", text="The mirror goes silent.", gap=0.45, pace=0.92, tone="whispers"),
    dict(id="m8", scene="logic", text="If it says yes, its answer wasn't no. So yes is a lie."),
    dict(id="m9", scene="logic", text="If it says no, then its answer was no. So no is a lie too."),
    dict(id="m10", scene="crack", text="Either way, the mirror that never lies, has to lie.", pace=0.95,
         tone="dramatic"),
    dict(id="m11", scene="end", text="So, what should the mirror say? Yes, or no?", gap=0.3, pace=0.95, tone="curious"),
]

METADATA = dict(
    title="The Mirror Never Lies… Until This Question 🪞",
    alt_titles=["1 Question Broke the Magic Mirror 🪞", "\"Will Your Next Answer Be No?\" 🤯",
                "The Question a Mirror That Never Lies Can't Answer 🪞"],
    description="""A magic mirror answers every question. And it never lies. 🪞

Will it rain tomorrow? Yes. And it rains. Where's the lost phone? Under the sofa. And it's there.
Then the kid asks one more question: "Will your next answer be no?"

The mirror goes silent. If it says yes, its answer wasn't no, so yes is a lie. If it says no, then its answer was no, so no is a lie too. Either way, the mirror that never lies has to lie.

An original story built on a famous self-reference puzzle.

💬 So what should the mirror say? Yes, or no? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Paradox", "#MagicMirror", "#Shorts"],
    tags=["magic mirror", "mirror paradox", "will your next answer be no", "liar paradox", "paradox", "brain teaser",
          "logic puzzle", "funny story", "mind blowing", "interestingly strange"],
    pinned_comment="Ask the mirror a question it can't answer 🪞 Best one gets pinned 👇",
)

GLASS = hexc("#6a4ad8")
GIRL = dict(shirt=hexc("#ff7fb0"), tie=None, pants=hexc("#5a4ab8"))


# ---------------------------------------------------------------- the attic
def _attic(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 820, [(0, hexc("#2a1f3a")), (1, hexc("#4a3458"))]))
    c.fill()
    for x in range(-40, W + 60, 120):            # wooden wall planks
        c.rectangle(x, 0, 6, 820)
        c.set_source_rgba(0, 0, 0, 0.18)
        c.fill()
    for side in (-1, 1):                          # roof beams
        c.move_to(360, -40)
        c.line_to(360 + side * 520, 300)
        c.set_line_width(40)
        c.set_source_rgba(*hexc("#1e1428"))
        c.stroke()
    c.rectangle(0, 820, W, H - 820)
    c.set_source(lin(0, 820, 0, H, [(0, hexc("#6a4a3a")), (1, hexc("#3a281e"))]))
    c.fill()
    for k in range(6):
        c.rectangle(0, 820 + k * k * 14, W, 3)
        c.set_source_rgba(0, 0, 0, 0.25)
        c.fill()
    rng = random.Random(11)
    for _ in range(40):                           # dust motes
        c.arc(rng.random() * W, rng.random() * 800, rng.uniform(1, 3), 0, 2 * math.pi)
        c.set_source_rgba(1, 0.9, 0.7, rng.uniform(0.1, 0.4))
        c.fill()


def attic(cr, t):
    put(cr, sprite("mirror_attic", W, H, _attic), 0, 0)
    for x, y in ((90, 760), (630, 760)):           # candles
        soft_disc(cr, x, y - 70, 70 + 6 * math.sin(t * 9 + x), (1, 0.75, 0.35, 0.3))
        rrect(cr, x - 14, y - 60, 28, 70, 6)
        paint(cr, hexc("#f4ecd8"), OUTLINE, 3.5)
        flick = math.sin(t * 13 + x) * 3
        smooth(cr, [(x, y - 96 + flick), (x + 9, y - 72), (x, y - 62), (x - 9, y - 72)])
        paint(cr, hexc("#ffb43a"), None, 0)


def mirror(cr, t, x, y, s=1.0, face=1.0, talk=False, eyes="open", crack=0.0, flicker=0.0, glow=1.0):
    """The magic mirror on its stand; (x, y) is the centre of the glass."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if glow:
        soft_disc(cr, 0, 0, 330, alpha(hexc("#9a7aff"), 0.28 * glow))
    for side in (-1, 1):                          # stand legs
        stroke_line(cr, [(side * 120, 200), (side * 170, 420)], 16, OUTLINE, curve=False)
        stroke_line(cr, [(side * 120, 200), (side * 170, 420)], 9, hexc("#b8862a"), curve=False)
    gold = [(0, hexc("#fff0a8")), (0.5, GOLD), (1, hexc("#9a6a14"))]
    ellipse(cr, 0, 0, 205, 270)
    paint(cr, lin(-200, -270, 200, 270, gold), OUTLINE, 6)
    for k in range(10):                           # ornaments on the frame
        a = k / 10 * 2 * math.pi
        cr.arc(math.cos(a) * 205, math.sin(a) * 270, 16, 0, 2 * math.pi)
        paint(cr, lin(-16, -16, 16, 16, gold), OUTLINE, 3.5)
    smooth(cr, [(-40, -270), (0, -330), (40, -270)])
    paint(cr, lin(-40, -330, 40, -270, gold), OUTLINE, 4)
    cr.arc(0, -300, 14, 0, 2 * math.pi)
    paint(cr, RED, OUTLINE, 3)
    ellipse(cr, 0, 0, 170, 235)                   # glass
    cr.save()
    cr.clip_preserve()
    shim = 0.5 + 0.5 * math.sin(t * 2)
    on = 1.0 if flicker <= 0 else (0.35 + 0.65 * (math.sin(t * 40) > 0)) * (1 - 0.6 * flicker)
    cr.set_source(rad(-50, -80, 300, [(0, shade(GLASS, 0.5 * on)), (0.6, shade(GLASS, -0.1 + 0.2 * on)),
                                      (1, shade(GLASS, -0.5))]))
    cr.fill()
    for k in range(3):                            # swirling mist
        a = t * 0.8 + k * 2.1
        cr.arc(math.cos(a) * 70, math.sin(a) * 110, 60 + 10 * k, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.06 + 0.03 * shim)
        cr.fill()
    if face > 0:                                  # a calm face in the glass
        a = face * on
        for side in (-1, 1):
            if eyes == "closed":
                stroke_line(cr, [(side * 60 - 26, -40), (side * 60 + 26, -40)], 7, (1, 1, 1, a), curve=False)
            else:
                ellipse(cr, side * 60, -40, 26, 34 if eyes == "open" else 44)
                cr.set_source_rgba(1, 1, 1, a)
                cr.fill()
                cr.arc(side * 60, -36, 12, 0, 2 * math.pi)
                cr.set_source_rgba(*alpha(hexc("#3a1a7a"), a))
                cr.fill()
        if talk:
            ellipse(cr, 0, 70, 40, 10 + 18 * abs(math.sin(t * 16)))
        else:
            ellipse(cr, 0, 74, 34, 6)
        cr.set_source_rgba(1, 1, 1, 0.85 * a)
        cr.fill()
    stroke_line(cr, [(-120, -150), (-70, -200)], 10, (1, 1, 1, 0.35), curve=False)
    if crack > 0:                                 # cracks spreading from the centre
        rng = random.Random(4)
        for k in range(9):
            a = k / 9 * 2 * math.pi + rng.uniform(-0.2, 0.2)
            pts = [(0, 0)]
            r = 0
            while r < 260 * crack:
                r += rng.uniform(30, 55)
                a += rng.uniform(-0.35, 0.35)
                pts.append((math.cos(a) * r, math.sin(a) * r * 1.3))
            stroke_line(cr, pts, 6, (1, 1, 1, 0.9), curve=False)
            stroke_line(cr, pts, 2.5, alpha(OUTLINE, 0.7), curve=False)
    cr.restore()
    ellipse(cr, 0, 0, 170, 235)
    paint(cr, None, OUTLINE, 5)
    cr.restore()


def sofa(cr, x, y, s=1.0, phone=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ground_shadow(cr, 0, 4, 260, 0.3)
    if phone > 0:                                 # the phone, glowing under the sofa
        soft_disc(cr, 60, -16, 80 * phone, (0.6, 0.9, 1.0, 0.5 * phone))
        rrect(cr, 30, -26, 64, 22, 6)
        paint(cr, hexc("#2b2b33"), OUTLINE, 3)
        rrect(cr, 36, -23, 52, 16, 4)
        paint(cr, hexc("#7ad0ff"), None, 0)
    col = hexc("#3aa89a")
    for side in (-1, 1):
        rrect(cr, side * 240 - 40, -230, 80, 190, 30)
        paint(cr, lin(0, -230, 0, -40, [(0, shade(col, 0.25)), (1, col)]), OUTLINE, 5)
        rrect(cr, side * 200 - 8, -40, 16, 40, 4)
        paint(cr, hexc("#5a3a24"), OUTLINE, 3)
    rrect(cr, -210, -280, 420, 170, 40)
    paint(cr, lin(0, -280, 0, -110, [(0, shade(col, 0.3)), (1, shade(col, -0.05))]), OUTLINE, 5)
    rrect(cr, -220, -130, 440, 90, 26)
    paint(cr, lin(0, -130, 0, -40, [(0, shade(col, 0.15)), (1, shade(col, -0.2))]), OUTLINE, 5)
    cr.restore()


def girl(cr, t, tl, x, y, s=1.0, **kw):
    kw.setdefault("mouth", mouth(tl, "girl", t, kw.pop("rest", "smile")))
    person(cr, t, x, y, s, "student1", **GIRL, **kw)


# ---------------------------------------------------------------- scenes
def scene_mirror(cr, t, tl):
    A = tl.at
    attic(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.05, 360, 600)), (A("m2"), (1.15, 360, 540))], dur=0.8), drift=0.01, t=t)
    wake = A("m1", "answers")
    mirror(cr, t, 360, 470, 0.95, face=ease_out(seg(t, wake, wake + 0.6)), talk=tl.speaking("mirror", t),
           eyes="open" if t >= A("m1", "never") else "closed")
    cr.restore()
    particles(cr, t, 3, 20, (0.85, 0.75, 1.0, 0.6), area=(160, 200, 400, 560), r=(2, 5), speed=20)
    sign(cr, t, -0.5, 360, 130, "IT NEVER LIES", col=PURPLE, size=78)
    vignette(cr, 0.5)


def scene_rain(cr, t, tl):
    A = tl.at
    yes, rains = A("m3", "Yes."), A("m3", "rains.")
    cr.rectangle(0, 0, W, H)
    dark = seg(t, rains - 0.3, rains + 0.3)
    cr.set_source(lin(0, 0, 0, H, [(0, shade(hexc("#9fd6ff"), -0.45 * dark)), (1, shade(hexc("#e8f6ff"), -0.4 * dark))]))
    cr.fill()
    for k, (cx, cy) in enumerate(((200, 260), (470, 220), (360, 330))):     # clouds roll in
        dx = lerp(-400 if k % 2 == 0 else 400, 0, ease_out(seg(t, A("m3"), A("m3") + 0.8)))
        for j, (ox, oy, r) in enumerate(((-70, 10, 60), (0, -20, 80), (75, 8, 62))):
            cr.arc(cx + dx + ox, cy + oy, r, 0, 2 * math.pi)
            paint(cr, shade(WHITE, -0.35 * dark), alpha(OUTLINE, 0.6), 4)
    if t >= rains - 0.2:
        rng = random.Random(2)
        for _ in range(70):
            x0, sp = rng.random() * W, rng.uniform(900, 1300)
            y0 = (rng.random() * 1400 + (t - rains) * sp) % 1300 + 300
            stroke_line(cr, [(x0, y0), (x0 - 8, y0 + 34)], 4, (0.6, 0.8, 1.0, 0.8), curve=False)
    mirror(cr, t, 540, 660, 0.55, talk=yes <= t < yes + 0.5, glow=0.6)
    tag(cr, t, A("m3"), 360, 470, "RAIN TOMORROW?", col=BLUE, size=54)
    bubble(cr, t, yes, 300, 600, "YES.", col=WHITE, size=60, tail=1)
    check(cr, t, rains, 180, 760, 70)
    vignette(cr, 0.4)


def scene_phone(cr, t, tl):
    A = tl.at
    attic(cr, t)
    under, there = A("m4", "Under"), A("m4", "there.")
    cr.save()
    enter(cr, camera(t, [(A("m4") - 0.3, (1.0, 360, 640)), (there - 0.2, (1.5, 330, 700))], dur=0.6))
    sofa(cr, 300, 820, 0.9, phone=ease_out(seg(t, there - 0.2, there + 0.3)))
    mirror(cr, t, 600, 520, 0.45, talk=under <= t < under + 0.8, glow=0.6)
    cr.restore()
    tag(cr, t, A("m4"), 360, 160, "LOST PHONE?", col=PINK, size=56)
    bubble(cr, t, under, 360, 300, "UNDER THE SOFA.", col=WHITE, size=48, tail=1)
    check(cr, t, there, 560, 620, 70)
    vignette(cr, 0.45)


def scene_ask(cr, t, tl):
    A = tl.at
    attic(cr, t)
    m6 = A("m6")
    cr.save()
    enter(cr, camera(t, [(A("m5") - 0.3, (1.0, 360, 640)), (A("m5", "one"), (1.25, 300, 640)),
                         (m6, (1.15, 360, 600))], dur=0.6))
    mirror(cr, t, 480, 470, 0.75, eyes="open")
    girl(cr, t, tl, 190, 1050, 0.95, eyes="half", rest="smug", arms=("point", "hips") if t >= m6 else ("chin", "hips"),
         brows="raise", look=(0.7, -0.3))
    cr.restore()
    if t < m6:
        sign(cr, t, A("m5", "one"), 360, 150, "ONE MORE QUESTION", col=PINK, size=56)
    note(cr, t, m6 + 0.05, 360, 270, ["\"WILL YOUR NEXT", "ANSWER BE", "NO?\""], hot=2, w=520, size=56)
    vignette(cr, 0.45)


def scene_silent(cr, t, tl):
    A = tl.at
    attic(cr, t)
    sil = A("m7", "silent.")
    dx, dy = shake(t, sil, 0.3, 6)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("m7") - 0.3, (1.15, 360, 540))]))
    mirror(cr, t, 360, 470, 0.95, eyes="wide", flicker=ease_out(seg(t, A("m7", "mirror"), sil + 0.3)))
    cr.restore()
    if t >= sil:
        cue("hit", t, sil)
    stamp(cr, t, sil, 360, 170, "SILENT...", col=hexc("#9a7aff"), size=96)
    vignette(cr, 0.55)


def _stuck(cr, t, spin):
    mirror(cr, t, 360, 860, 0.38, eyes="wide", flicker=0.6 if spin else 0.3, glow=0.4)


def scene_logic(cr, t, tl):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2a1f4a")), (1, hexc("#8a6ad8"))]))
    cr.fill()
    particles(cr, t, 9, 30, (1, 1, 1, 0.35), r=(2, 5), speed=14)
    either_way(cr, t, tl, "m8", "m9", "m10",
               ("SAYS YES?", ["Answer isn't NO...", "so YES is", "a LIE!"], GREEN),
               ("SAYS NO?", ["Answer IS NO...", "so NO is", "a LIE!"], RED),
               "IT HAS TO LIE", PURPLE, ("m8", "lie."), ("m9", "too."), figure=_stuck)
    vignette(cr, 0.4)


def scene_crack(cr, t, tl):
    A = tl.at
    attic(cr, t)
    hit = A("m10", "lie.")
    dx, dy = shake(t, hit, 0.35, 10)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("m10") - 0.3, (1.05, 360, 580)), (hit, (1.2, 360, 540))], dur=0.5))
    mirror(cr, t, 360, 470, 0.95, eyes="wide", crack=ease_out(seg(t, hit - 0.1, hit + 0.5)),
           flicker=0.4 if t >= hit else 0.0)
    cr.restore()
    if t >= hit:
        cue("hit", t, hit)
    sign(cr, t, A("m10", "never"), 360, 130, "NEVER LIES...", col=PURPLE, size=64, end=hit - 0.05)
    stamp(cr, t, hit, 360, 150, "HAS TO LIE", col=RED, size=90)
    vignette(cr, 0.5)


def scene_end(cr, t, tl):
    A = tl.at
    attic(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    mirror(cr, t, 470, 560, 0.62, eyes="wide", crack=1.0, flicker=0.3)
    girl(cr, t, tl, 170, 1050, 0.85, eyes="happy", rest="grin", arms=("hips", "hips"), look=(0.6, -0.3))
    cr.restore()
    sign(cr, t, A("m11"), 360, 130, "WHAT SHOULD IT SAY?", col=PURPLE, size=56)
    buttons(cr, t, A("m11", "Yes,"), [("YES", GREEN), ("NO", RED)], y=270)
    vignette(cr, 0.45)


SCENES = {"mirror": scene_mirror, "rain": scene_rain, "phone": scene_phone, "ask": scene_ask, "silent": scene_silent,
          "logic": scene_logic, "crack": scene_crack, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
