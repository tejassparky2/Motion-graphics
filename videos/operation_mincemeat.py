"""Row 75: "This Spy Fooled Hitler. He Was Already Dead." -- Operation Mincemeat (1943), dramatized, in the polished
look, built on the Meanwhile Mayank frame-0 rules (one subject on a plain ground, two-tier hook with a red mark).

Script: out/scripts_slots_75-81.md (owner, 29 Oct 2026: "Make it from research currently did"). Facts: Ewen Montagu,
The Man Who Never Was (1953); Ben Macintyre, Operation Mincemeat (2010). The body, dressed as "Major William Martin,
Royal Marines", was released from HMS Seraph off Huelva, Spain, on 30 April 1943, with fake plans pointing at Greece
and Sardinia; the Allies landed in Sicily in July 1943. In 1996 Roger Morgan found records naming the man as
Glyndwr Michael, a Welshman; his family disputes parts of the official account of his death, so the video doesn't
say how he died. The officers are unnamed and their lines are dramatized. Turbo stock female narrator with tags;
the officers through Turbo with Kokoro reference voices.
"""
import math

from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, red_x, shake, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter, lin,
                           paint, rad, rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.bq_kit import hook2, plain, ring, talker

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "m8"          # music drops out on the name (research 18 Oct 2026, A5)
SERIES = "Interestingly Strange"
voice.SPEAKERS.update({"brit": dict(voice="bm_george", speed=1.0, turbo_ref="bm_george"),
                       "german": dict(voice="am_onyx", speed=0.95, turbo_ref="am_onyx")})
GERMAN = dict(skin="light", hair="short", hair_col=hexc("#c8b070"), shirt=WHITE, suit=hexc("#5a6070"),
              pants=hexc("#4a505e"), tie=hexc("#2b2b33"), shoes=hexc("#1b1b1f"), build="adult")
MARTIN = dict(skin="light", hair="short", hair_col=hexc("#3a2418"), shirt=hexc("#e8dcc0"), suit=hexc("#4a4a5e"),
              pants=hexc("#3a3a4e"), tie=hexc("#2b2b33"), shoes=hexc("#1b1b1f"), build="adult")
NAVY = "#1c2440"

SCRIPT = [
    dict(id="m1", scene="cuff", text="We need a dead man. And he has to lie to Hitler.", speaker="brit"),
    dict(id="m2", scene="dress", text="London, [nineteen forty three.|1943.] British spies dress a dead man as an "
                                      "officer. Major William Martin."),
    dict(id="m3", scene="map", text="His briefcase holds fake secret plans. The target is Greece. Not Sicily."),
    dict(id="m4", scene="sea", text="A submarine leaves him floating off the coast of Spain."),
    dict(id="m5", scene="german", text="The plans are real. Move the troops!", speaker="german"),
    dict(id="m6", scene="sicily", text="Hitler believes it. In July, the Allies land in Sicily."),
    dict(id="m7", scene="grave", text="But who was the dead man? For fifty three years, nobody knew."),
    dict(id="m8", scene="grave", text="Then a historian found his name. Glyndwr Michael. A poor Welsh man. Nobody had "
                                      "asked him. [sigh]", gap=0.4),
    dict(id="m9", scene="end", text="So, would you let them use your body to save thousands? Or is that never okay?",
         gap=0.3),
]

METADATA = dict(
    title="This Spy Fooled Hitler. He Was Already Dead. 💼",
    alt_titles=["A Dead Man Changed World War Two 💼", "Nobody Asked Him. He Saved Thousands. 💼"],
    description="""London, 1943. British spies need someone to lie to Hitler, and they pick a dead man. 💼

They dress him as "Major William Martin", chain a briefcase of fake secret plans to his wrist (attack Greece, not Sicily), and a submarine leaves him floating off the coast of Spain. The plans reach Germany. Hitler believes them. In July 1943 the Allies land in Sicily.

For 53 years nobody knew who the dead man really was. In 1996 a historian found the name: Glyndwr Michael, a poor Welshman. Nobody had asked him.

Dramatized from real events. Sources: Ewen Montagu, The Man Who Never Was (1953); Ben Macintyre, Operation Mincemeat (2010); Roger Morgan's 1996 identification from Public Record Office files.

💬 Would you let them use your body to save thousands? Or is that never okay? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and strange true stories, animated in under a minute.""",
    hashtags=["#OperationMincemeat", "#History", "#Shorts"],
    tags=["operation mincemeat", "the man who never was", "dead spy fooled hitler", "ww2 deception", "glyndwr michael",
          "world war 2 history", "spy story", "true story", "moral dilemma", "interestingly strange"],
    pinned_comment="Would YOU let them use your body to save thousands? YES or NEVER, and why? 👇",
)


# ---------------------------------------------------------------- props
def briefcase(cr, x, y, s=1.0, open_=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -120, -80, 240, 160, 14)
    paint(cr, lin(0, -80, 0, 80, [(0, hexc("#7a4a2a")), (1, hexc("#4a2a16"))]), OUTLINE, 6)
    rrect(cr, -40, -112, 80, 40, 14)
    paint(cr, None, OUTLINE, 10)
    for side in (-1, 1):
        rrect(cr, side * 70 - 14, -84, 28, 18, 4)
        paint(cr, GOLD, OUTLINE, 3)
    if open_ > 0:
        for k in range(3):
            rrect(cr, -90 + k * 10, -70 - 60 * open_ - k * 8, 170, 110, 4)
            paint(cr, hexc("#f4efe4"), OUTLINE, 3)
            bold_text(cr, "TOP SECRET", k * 10 - 5, -20 - 60 * open_ - k * 8, 22, RED, outline=None, shadow=0)
    cr.restore()


def cuffed_hand(cr, t, x, y, s=1.0):
    """A pale hand from the left edge, a chain to a briefcase handle."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -420, -40, 300, 80, 30)                              # sleeve
    paint(cr, hexc("#4a4a5e"), OUTLINE, 6)
    ellipse(cr, -100, 0, 70, 52)                                   # hand, grey and still
    paint(cr, hexc("#c8c4bc"), OUTLINE, 6)
    for k in range(4):
        rrect(cr, -70, -40 + k * 22, 70, 18, 9)
        paint(cr, hexc("#c0bcb4"), OUTLINE, 4)
    rrect(cr, -150, -48, 44, 96, 10)                               # the cuff
    paint(cr, hexc("#b8bcc8"), OUTLINE, 5)
    for k in range(9):                                             # chain from the cuff to the case handle
        ellipse(cr, -120 + k * 30, 50 + k * 2.6 + 6 * math.sin(t * 2 + k) * math.sin(k / 8 * math.pi), 14, 9)
        paint(cr, None, hexc("#9aa0ac"), 5)
    cr.restore()


def m_map(cr, t, arrow_at=None, cross_at=None, flags_at=None, tanks_at=None):
    """A simple Mediterranean: Italy's boot, Sicily, Sardinia, Greece."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#7ab8d8")), (1, hexc("#5a98c0"))]))
    cr.fill()
    cr.save()
    cr.translate(-50, 120)
    land = hexc("#e8d8a8")
    smooth(cr, [(250, 180), (330, 260), (380, 380), (450, 470), (470, 540), (420, 560), (390, 500), (330, 420),
                (270, 330), (220, 240)])                            # Italy
    paint(cr, land, OUTLINE, 5)
    smooth(cr, [(330, 600), (430, 590), (450, 630), (360, 660), (320, 640)])   # Sicily
    paint(cr, hexc("#f4c870"), OUTLINE, 5)
    smooth(cr, [(130, 330), (170, 330), (180, 430), (140, 450), (120, 400)])   # Sardinia
    paint(cr, land, OUTLINE, 5)
    smooth(cr, [(560, 420), (650, 400), (700, 470), (680, 560), (610, 600), (570, 520)])   # Greece
    paint(cr, land, OUTLINE, 5)
    for txt, x, y in (("SICILY", 385, 700), ("GREECE", 630, 650), ("SARDINIA", 150, 490), ("ITALY", 330, 330)):
        bold_text(cr, txt, x, y, 26, OUTLINE, outline=None, shadow=0)
    if arrow_at is not None and t >= arrow_at:
        ring(cr, t, arrow_at, 630, 500, 110, 140)
        bold_text(cr, "TARGET", 630, 330, 40, RED, shadow=0)
    if cross_at is not None and t >= cross_at:
        red_x(cr, t, cross_at, 385, 625, 60)
    if tanks_at is not None and t >= tanks_at:
        u = seg(t, tanks_at, tanks_at + 1.2)
        for k in range(3):
            tx, ty = lerp(420, 600 + k * 30, u), lerp(250 + k * 40, 470 + k * 30, u)
            rrect(cr, tx - 22, ty - 12, 44, 24, 6)
            paint(cr, hexc("#5a6070"), OUTLINE, 3)
            stroke_line(cr, [(tx, ty - 4), (tx + 30, ty - 10)], 5, OUTLINE, curve=False)
    if flags_at is not None and t >= flags_at:
        ring(cr, t, flags_at, 390, 625, 90, 60, col=GREEN)
        for k, (fx, fy) in enumerate(((345, 620), (395, 610), (440, 630))):
            if t < flags_at + 0.2 * k:
                continue
            stroke_line(cr, [(fx, fy), (fx, fy - 90)], 7, OUTLINE, curve=False)
            rrect(cr, fx, fy - 90, 56, 36, 4)
            paint(cr, (BLUE, RED, GREEN)[k], OUTLINE, 4)
    cr.restore()


def uniform(cr, x, y, s=1.0, swing=0.0):
    """An officer's jacket on a hanger (hook at (x, y))."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(swing)
    cr.scale(s, s)
    stroke_line(cr, [(0, 0), (0, -30), (14, -44)], 6, OUTLINE)
    stroke_line(cr, [(-110, 40), (0, 0), (110, 40)], 8, hexc("#8a5a2b"), curve=False)
    cr.move_to(-110, 40)
    cr.line_to(-140, 260)
    cr.line_to(140, 260)
    cr.line_to(110, 40)
    cr.line_to(30, 20)
    cr.line_to(0, 110)
    cr.line_to(-30, 20)
    cr.close_path()
    paint(cr, lin(0, 20, 0, 260, [(0, hexc("#5a5a6e")), (1, hexc("#3a3a4e"))]), OUTLINE, 6)
    for by in (140, 190, 240):
        ellipse(cr, 0, by, 8, 8)
        paint(cr, GOLD, OUTLINE, 3)
    cr.restore()


def gravestone(cr, x, y, s=1.0, name=None, k=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(-150, 0)
    cr.line_to(-150, -260)
    cr.curve_to(-150, -360, 150, -360, 150, -260)
    cr.line_to(150, 0)
    cr.close_path()
    paint(cr, lin(0, -360, 0, 0, [(0, hexc("#d8d8dc")), (1, hexc("#a8a8b0"))]), OUTLINE, 6)
    bold_text(cr, "MAJOR", 0, -250, 34, hexc("#5a5a66"), outline=None, shadow=0)
    bold_text(cr, "W. MARTIN", 0, -205, 38, hexc("#5a5a66"), outline=None, shadow=0)
    if name:
        cr.save()
        cr.translate(0, -120)
        cr.scale(k, k)
        rrect(cr, -140, -40, 280, 80, 10)
        paint(cr, hexc("#fff4d8"), OUTLINE, 5)
        bold_text(cr, name, 0, 12, 30, RED, outline=None, shadow=0)
        cr.restore()
    else:
        bold_text(cr, "?", 0, -90, 110, RED)
    cr.restore()


def grass(cr, y):
    cr.rectangle(0, y, W, H - y)
    cr.set_source(lin(0, y, 0, H, [(0, hexc("#7aa85a")), (1, hexc("#4a7a3a"))]))
    cr.fill()


def german(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "german", "fermi", x, y, s, rest="flat", **dict(GERMAN, **kw))


# ---------------------------------------------------------------- scenes
def scene_cuff(cr, t, tl):
    A = tl.at
    plain(cr, NAVY, "#141a30")
    cr.save()
    enter(cr, camera(t, [(0, (1.3, 330, 690)), (A("m1", "Hitler"), (1.45, 340, 700))], dur=1.0))
    cuffed_hand(cr, t, 330, 620, 1.0)
    briefcase(cr, 460 + 6 * math.sin(t * 2), 790, 0.9)
    ring(cr, t, A("m1", "dead"), 205, 620, 66, 86)
    cr.restore()
    vignette(cr, 0.5)


def scene_dress(cr, t, tl):
    A = tl.at
    plain(cr, "#e8e0cc", "#d0c4a8")
    s0 = tl.scene_at(t)[1]
    dressed = t >= A("m2", "dress")
    if not dressed:
        person(cr, t, 360, 1050, 1.0, "fermi", **dict(MARTIN, skin=hexc("#b8b8c4"), suit=None,
               shirt=hexc("#e8e8ee"), tie=None, eyes="closed", mouth="flat", arms=("down", "down")))
        if t >= A("m2", "spies"):                                  # the uniform swings in on a hanger
            u = seg(t, A("m2", "spies"), A("m2", "spies") + 0.4)
            uniform(cr, lerp(760, 560, u), 520, 0.8, swing=math.sin(t * 3) * 0.08)
    else:
        k = appear(t, A("m2", "dress"), 0.35)
        person(cr, t, 360, 1050 - 30 * (1 - k), 1.0, "fermi", **dict(MARTIN, eyes="closed", mouth="flat",
               arms=("down", "down")))
        sparkles(cr, t, A("m2", "dress"), 360, 760, n=8, col=GOLD, spread=160)
    if t >= A("m2", "officer"):                                    # a medal on his chest
        k = appear(t, A("m2", "officer"), 0.3)
        ellipse(cr, 320, 700, 16 * k, 16 * k)
        paint(cr, GOLD, OUTLINE, 4)
    tag(cr, t, s0, 360, 200, "LONDON · 1943", col=PURPLE, size=44)
    if t >= A("m2", "Martin"):
        card(cr, t, A("m2", "Major"), 360, 360, 460, 150, "ID CARD", ["MAJOR W. MARTIN"], col=BLUE, title_size=30,
             line_size=40)
        stamp(cr, t, A("m2", "Martin"), 520, 420, "FAKE", col=RED, size=50)
    vignette(cr, 0.35)


def scene_map(cr, t, tl):
    A = tl.at
    m_map(cr, t, arrow_at=A("m3", "Greece"), cross_at=A("m3", "Sicily"))
    briefcase(cr, 150, 330, 0.6, open_=seg(t, tl.scene_at(t)[1], A("m3", "plans", end=True)))
    if t >= A("m3", "fake"):
        tag(cr, t, A("m3", "fake"), 360, 150, "FAKE SECRET PLANS", col=RED, size=46)
    vignette(cr, 0.3)


def scene_sea(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#1a2a4a")), (0.5, hexc("#2a4a6a")), (1, hexc("#1a3a5a"))]))
    cr.fill()
    soft_disc(cr, 560, 200, 70, (1, 1, 0.9, 0.5))                 # moon
    s0 = tl.scene_at(t)[1]
    smooth(cr, [(560, 790), (640, 740), (720, 720), (760, 760), (760, 840), (560, 840)])   # the coast of Spain
    paint(cr, hexc("#e8d8a8"), OUTLINE, 5)
    up = seg(t, s0, A("m4", "submarine", end=True))
    stroke_line(cr, [(110, 800), (110, 800 - 260 * up)], 20, hexc("#5a6070"), curve=False)   # periscope
    stroke_line(cr, [(110, 800 - 260 * up), (170, 800 - 260 * up)], 20, hexc("#5a6070"), curve=False)
    if t >= A("m4", "submarine"):
        tag(cr, t, A("m4", "submarine"), 150, 450, "SUBMARINE", col=BLUE, size=34)
    drift = seg(t, A("m4", "floating"), A("m4", "Spain", end=True) + 0.8)
    cr.save()                                                      # the body, lying on the water
    cr.translate(lerp(420, 540, drift), 800 + 8 * math.sin(t * 2))
    cr.rotate(-math.pi / 2)
    person(cr, t, 0, 0, 0.75, "fermi", bob=False, shadow=False,
           **dict(MARTIN, eyes="closed", mouth="flat", arms=("down", "down")))
    cr.restore()
    for k in range(6):                                             # waves over it
        y = 820 + k * 70
        cr.move_to(0, y)
        for x in range(0, W + 40, 40):
            cr.line_to(x, y + 10 * math.sin(x / 40 + t * 2 + k))
        cr.line_to(W, H)
        cr.line_to(0, H)
        cr.close_path()
        paint(cr, alpha(hexc("#2a5a8a"), 0.5), None, 0)
    if t >= A("m4", "coast"):
        tag(cr, t, A("m4", "coast"), 360, 220, "OFF SPAIN · 30 APRIL 1943", col=GOLD, size=38)
    vignette(cr, 0.5)


def scene_german(cr, t, tl):
    A = tl.at
    plain(cr, "#3a3a44", "#2a2a32")
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.15, 360, 700))]))
    german(cr, t, tl, 250, 1100, 1.0, eyes="wide" if t >= A("m5", "real") else "half", brows="up",
           arms=("point", "down"), look=(0.6, 0.0))
    briefcase(cr, 520, 860, 0.8, open_=1.0)
    cr.restore()
    if t >= A("m5", "Move"):
        sign(cr, t, A("m5", "Move"), 360, 230, "MOVE THE TROOPS!", col=RED, size=56)
        cue("thud", t, A("m5", "Move"), 0.3)
    vignette(cr, 0.45)


def scene_sicily(cr, t, tl):
    A = tl.at
    m_map(cr, t, tanks_at=tl.scene_at(t)[1], flags_at=A("m6", "Sicily"))
    sign(cr, t, A("m6", "believes"), 360, 160, "HITLER BELIEVES IT", col=PURPLE, size=48, end=A("m6", "July") - 0.05)
    if t >= A("m6", "July"):
        tag(cr, t, A("m6", "July"), 360, 160, "JULY 1943: SICILY", col=GREEN, size=48)
    vignette(cr, 0.3)


def scene_grave(cr, t, tl):
    A = tl.at
    plain(cr, "#c8ccd4", "#a8acb8")
    grass(cr, 820)
    named = t >= A("m8", "Glyndwr")
    gravestone(cr, 360, 830, 1.2, name="GLYNDWR MICHAEL" if named else None,
               k=appear(t, A("m8", "Glyndwr"), 0.35) if named else 1.0)
    if A("m7") <= t < A("m8"):
        counter(cr, t, A("m7", "fifty"), 360, 300, 53, size=120, dur=0.8, col=GOLD, sub="YEARS. NOBODY KNEW.")
    if t >= A("m8", "historian"):
        tag(cr, t, A("m8", "historian"), 360, 220, "1996: A HISTORIAN FINDS THE NAME", col=BLUE, size=36,
            end=A("m8", "Welsh") - 0.05)
    if t >= A("m8", "Welsh"):
        tag(cr, t, A("m8", "Welsh"), 360, 220, "A POOR WELSHMAN", col=BLUE, size=44)
    if t >= A("m8", "Nobody"):
        stamp(cr, t, A("m8", "Nobody"), 360, 360, "NOBODY ASKED HIM", col=RED, size=52)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    plain(cr, "#c8ccd4", "#a8acb8")
    grass(cr, 820)
    gravestone(cr, 360, 830, 0.9, name="GLYNDWR MICHAEL")
    for k in range(5):                                             # flowers
        ellipse(cr, 260 + k * 50, 822, 14, 14)
        paint(cr, (RED, GOLD, WHITE, PURPLE, RED)[k], OUTLINE, 3)
    sign(cr, t, A("m9", "body"), 360, 210, "WOULD YOU?", col=GOLD, size=64)
    buttons(cr, t, A("m9", "never"), [("YES", GREEN), ("NEVER", RED)], y=360, size=50)
    vignette(cr, 0.35)


SCENES = {"cuff": scene_cuff, "dress": scene_dress, "map": scene_map, "sea": scene_sea, "german": scene_german,
          "sicily": scene_sicily, "grave": scene_grave, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    hook2(cr, t, "THE SPY WAS", "DEAD", end=tl.at("m1", end=True), y=200, big_at=tl.at("m1", "dead"),
          mark="circle", mark_at=tl.at("m1", "Hitler"))
    captions(cr, t, tl)
