"""#47 v2: the Last Bencher asks "Can God make a rock so heavy, that even God can't lift it?" -- the omnipotence
paradox told as a classroom scene, in the polished look.

Thomas Aquinas, Summa Theologiae I, q.25, a.3 (about 1270): God's power covers everything possible, and "whatever
implies contradiction does not come within the scope of divine omnipotence, because it cannot have the aspect of
possibility". Line q12 paraphrases him; it is not a quote. God is shown only as light, never as a figure.
v1 (narrator asks the question) was rendered on 11 Oct 2026; the owner asked for a stronger hook the same day, and
approved this v2 (out/scripts_batch_47-50.md doc, "Hook fix"): the question is in the kid's mouth at second 0, the
class reacts, and "the teacher just smiles" opens a loop the ending closes.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PURPLE, RED, buttons, card, check, knot, red_x, shake, sparkles,
                         studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           particles, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite, stamp,
                           stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person, portrait
from videos.first_cause import CANDLE, book, glow, monastery
from videos.last_bencher_4 import classroom, room

NARRATOR = dict(speed=0.92)
TAIL = 0.9
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5),
                       "sir": dict(voice="am_michael", speed=1.0)})

SCRIPT = [
    dict(id="q1", scene="ask", text="Sir, can God make a rock so heavy, that even God can't lift it?", speaker="kid"),
    dict(id="q2", scene="freeze", text="The whole class turns around. The teacher freezes."),
    dict(id="q3", scene="yes", text="Say yes, and there's a rock God can't lift.", speaker="kid"),
    dict(id="q4", scene="no", text="Say no, and there's a rock God can't make.", speaker="kid"),
    dict(id="q5", scene="trap", text="Either way, God isn't all-powerful. Checkmate, sir.", speaker="kid"),
    dict(id="q6", scene="smile", text="But the teacher just smiles, and hands him the chalk."),
    dict(id="q7", scene="board", text="Then draw me a square circle.", speaker="sir"),
    dict(id="q8", scene="board", text="That's impossible!", speaker="kid"),
    dict(id="q9", scene="board", text="Exactly. Not because you're weak. A square circle isn't a thing at all.",
         speaker="sir"),
    dict(id="q10", scene="words", text="And a rock too heavy for an all-powerful God? Same thing. A square circle, "
                                       "made of words.", speaker="sir"),
    dict(id="q11", scene="aquinas", text="That's the answer Thomas Aquinas gave, about [seven hundred and fifty years "
                                         "ago.|750 years ago.]"),
    dict(id="q12", scene="aquinas", text="All-powerful means able to do anything possible. And a contradiction isn't "
                                         "anything."),
    dict(id="q13", scene="end", text="So, did the teacher win? Or did he just dodge the question?", pace=0.95),
]
clear_dialogue(SCRIPT, pace=0.95)   # a riddle duel: clear turns between the kid and the teacher

METADATA = dict(
    title="1 Rock. 2 Answers. Both Break God?",
    alt_titles=["The Last Bencher Asked About God… Teacher's Reply 😳", "Can God Make a Rock He Can't Lift? 🪨",
                "Kid Traps Teacher With 1 Question About God 🪨"],
    description=""""Sir, can God make a rock so heavy, that even God can't lift it?" The omnipotence paradox, and the teacher's answer. 🪨

Say yes, and there's a rock God can't lift. Say no, and there's a rock God can't make. Either way, God isn't all-powerful. Checkmate?
But the teacher just smiles, and hands him the chalk: "Then draw me a square circle." Impossible. Not because you're weak: a square circle isn't a thing at all. And a rock too heavy for an all-powerful God? Same thing: a square circle, made of words.

That's the answer Thomas Aquinas gave, about 750 years ago: all-powerful means able to do anything possible, and a contradiction isn't anything.

Source: Thomas Aquinas, Summa Theologiae I, q.25, a.3.

💬 So, did the teacher win? Or did he just dodge the question? Keep it respectful 🙏👇

🔔 Interestingly Strange: The Last Bencher, mind-bending paradoxes, big theories and weird history, animated.""",
    hashtags=["#TheLastBencher", "#Paradox", "#Shorts"],
    tags=["omnipotence paradox", "can god make a rock he can't lift", "the last bencher", "paradox", "philosophy",
          "aquinas", "logic puzzle", "teacher vs student", "square circle", "interestingly strange"],
    pinned_comment="Did the teacher win, or did he dodge it? 🪨 Defend your pick (respectfully) 👇",
)

STONE = hexc("#8a8f9c")
NIGHT_TOP, NIGHT_BOT = hexc("#141a34"), hexc("#3a3466")


# ---------------------------------------------------------------- backdrops and props
def _hill(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, NIGHT_TOP), (0.7, NIGHT_BOT), (1, hexc("#5a4a7a"))]))
    c.fill()
    for k in range(70):                       # fixed stars
        x, y = (k * 137) % W, (k * 89) % 760
        c.arc(x, y, 1.2 + (k % 3) * 0.7, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.35 + 0.15 * (k % 4))
        c.fill()
    smooth(c, [(-40, 900), (160, 805), (360, 785), (560, 805), (760, 890), (760, H + 20), (-40, H + 20)])
    paint(c, lin(0, 785, 0, H, [(0, hexc("#3e5a4a")), (1, hexc("#1e2e26"))]), OUTLINE, 6)


def hill(cr, t):
    put(cr, sprite("rock_hill", W, H, _hill), 0, 0)
    particles(cr, t, 11, 26, (1, 1, 1, 0.5), area=(0, 0, W, 760), r=(1, 2.2), speed=5)


def rock(cr, x, y, s=1.0, tremble=0.0, t=0.0, a=1.0):
    """A huge lumpy boulder sitting with its base at (x, y)."""
    if s <= 0.01 or a <= 0.01:
        return
    cr.save()
    cr.translate(x + tremble * math.sin(t * 60), y)
    cr.scale(s, s)
    if a < 1:
        cr.push_group()
    soft_disc(cr, 0, 6, 210, (0, 0, 0, 0.25))
    pts = [(-200, 0), (-215, -90), (-170, -200), (-80, -260), (30, -270), (140, -220), (205, -120), (200, 0)]
    smooth(cr, pts)
    paint(cr, rad(-60, -190, 330, [(0, shade(STONE, 0.35)), (0.6, STONE), (1, shade(STONE, -0.35))]), OUTLINE, 7)
    for (px, py, r) in ((-90, -150, 26), (60, -90, 34), (110, -190, 18), (-30, -60, 20)):
        cr.arc(px, py, r, 0.2, 2.6)
        cr.set_line_width(4)
        cr.set_source_rgba(*alpha(OUTLINE, 0.35))
        cr.stroke()
    stroke_line(cr, [(-140, -180), (-110, -215), (-60, -235)], 6, (1, 1, 1, 0.35))
    if a < 1:
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    cr.restore()


def ghost_rock(cr, t, x, y, s=1.0):
    """The rock that was never made: a dashed outline that flickers."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    smooth(cr, [(-200, 0), (-215, -90), (-170, -200), (-80, -260), (30, -270), (140, -220), (205, -120), (200, 0)])
    cr.set_dash([22, 16], t * 40)
    cr.set_line_width(6)
    cr.set_source_rgba(1, 1, 1, 0.45 + 0.2 * math.sin(t * 8))
    cr.stroke()
    cr.set_dash([])
    cr.restore()


def beam(cr, t, x0, y0, x1, y1, a=1.0):
    """Golden light reaching down from the glow to the rock."""
    if a <= 0.01:
        return
    w = 70 + 8 * math.sin(t * 6)
    cr.move_to(x0 - 20, y0)
    cr.line_to(x0 + 20, y0)
    cr.line_to(x1 + w, y1)
    cr.line_to(x1 - w, y1)
    cr.close_path()
    cr.set_source(lin(0, y0, 0, y1, [(0, (1, 0.95, 0.7, 0.55 * a)), (1, (1, 0.9, 0.5, 0.12 * a))]))
    cr.fill()


def square_circle(cr, x, y, r, u, col=INKC, lw=9):
    """A shape morphing between a circle (u=0) and a square (u=1)."""
    pts = []
    for k in range(72):
        ang = k * 2 * math.pi / 72
        cx, cy = math.cos(ang), math.sin(ang)
        m = max(abs(cx), abs(cy))
        sx, sy = cx / m, cy / m
        pts.append((x + r * lerp(cx, sx * 0.9, u), y + r * lerp(cy, sy * 0.9, u)))
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    cr.set_line_width(lw)
    cr.set_line_join(1)
    cr.set_source_rgba(*col)
    cr.stroke()


def chalkboard(cr, x, y, w, h):
    soft_rrect(cr, x - w / 2, y - h / 2 + 12, w, h, 20, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, x - w / 2, y - h / 2, w, h, 20)
    paint(cr, hexc("#a8743e"), OUTLINE, 6)
    rrect(cr, x - w / 2 + 18, y - h / 2 + 18, w - 36, h - 36, 10)
    paint(cr, lin(0, y - h / 2, 0, y + h / 2, [(0, hexc("#2f5a48")), (1, hexc("#1e3a2e"))]), OUTLINE, 4)


def chalk(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.6)
    rrect(cr, -6, -34, 12, 40, 4)
    paint(cr, WHITE, OUTLINE, 3)
    cr.restore()


def morph(t, speed=1.6):
    return 0.5 + 0.5 * math.sin(t * speed * math.pi)




def thought_rock(cr, t, start, x, y, s=1.0):
    """A thought bubble with a huge rock in it, popping in at `start`."""
    k = appear(t, start, 0.35) if t >= start else 0.0
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k * s, k * s)
    for (dx, dy, r) in ((-150, 150, 14), (-120, 115, 22)):
        cr.arc(dx, dy, r, 0, 2 * math.pi)
        paint(cr, WHITE, OUTLINE, 4)
    smooth(cr, [(-130, 40), (-120, -70), (-40, -120), (60, -115), (140, -60), (140, 50), (60, 100), (-60, 100)])
    paint(cr, WHITE, OUTLINE, 6)
    glow(cr, t, 70, -70, 26, 0.9)
    rock(cr, -10, 70, 0.42)
    cr.restore()


def mouth_of(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


def sir(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", mouth_of(tl, "sir", t, kw.pop("rest", "smile")))
    person(cr, t, x, y, s, "sir", **kw)


# ---------------------------------------------------------------- scenes
def scene_ask(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (2.0, 555, 470)), (A("q1", "heavy,"), (2.05, 575, 470))], dur=0.8))
    talk = tl.speaking("kid", t)
    classroom(cr, t, tl, kid_pose=dict(arms=("up", "down"), eyes="open", mouth="talk" if talk else "grin",
                                       brows="raise"))
    cr.restore()
    thought_rock(cr, t, A("q1", "rock"), 190, 340, 0.85)
    sign(cr, t, -0.5, 360, 120, "CAN GOD LIFT IT?", col=GOLD, size=64)
    vignette(cr, 0.45)


def scene_freeze(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    turned = t >= A("q2", "turns")
    frozen = t >= A("q2", "freezes.")
    classroom(cr, t, tl, kid_pose=dict(arms=("hips", "down"), eyes="happy", mouth="smug"),
              look_at=(560, 0) if turned else None, gasp=turned)
    cr.save()
    if frozen:
        dx, dy = shake(t, A("q2", "freezes."), 0.3, 8)
        cr.translate(dx, dy)
    sir(cr, t, tl, 150, 1120, 1.05, eyes="wide", rest="o", brows="up", arms=("write", "down"), sweat=frozen)
    if frozen:      # an ice-blue flash over the teacher
        k = 1 - seg(t, A("q2", "freezes."), A("q2", "freezes.") + 1.2)
        soft_disc(cr, 150, 760, 260, (0.6, 0.85, 1.0, 0.45 * k + 0.15))
    cr.restore()
    stamp(cr, t, A("q2", "freezes."), 360, 170, "FROZEN", col=BLUE, size=90)
    vignette(cr, 0.4)


def _corner_kid(cr, t, tl, start):
    portrait(cr, t, start, 610, 320, 82, "kid", eyes="happy" if not tl.speaking("kid", t) else "open",
             mouth=mouth_of(tl, "kid", t, "smug"), bg=hexc("#9fd8ff"))


def scene_yes(cr, t, tl):
    A = tl.at
    hill(cr, t)
    strain = t >= A("q3", "can't")
    glow(cr, t, 360, 330, 90, 0.9)
    beam(cr, t, 360, 380, 360, 600, 1.0 if strain else appear(t, A("q3", "rock"), 0.4))
    rock(cr, 360, 830, 1.0, tremble=4 if strain else 0, t=t)
    if strain:
        for k in range(3):     # dust puffs: it won't budge
            ph = (t * 1.4 + k / 3) % 1
            soft_disc(cr, 160 + k * 200, 820 - ph * 60, 30 + ph * 30, (1, 1, 1, 0.35 * (1 - ph)))
    buttons(cr, t, A("q3"), [("YES", GREEN)], y=150, size=60, w=260)
    red_x(cr, t, A("q3", "can't"), 570, 560, 48)
    if t >= A("q3", "lift."):
        card(cr, t, A("q3", "lift."), 330, 400, 480, 120, "GOD CAN'T LIFT IT", [], col=RED, title_size=40)
    _corner_kid(cr, t, tl, A("q3"))
    vignette(cr, 0.45)


def scene_no(cr, t, tl):
    A = tl.at
    hill(cr, t)
    glow(cr, t, 360, 330, 90, 0.9)
    ghost_rock(cr, t, 360, 830, 1.0)
    if t >= A("q4", "make."):
        sparkles(cr, t, A("q4", "make."), 360, 700, n=6, seed=3, col=(1, 0.95, 0.7, 1), spread=160)
    buttons(cr, t, A("q4"), [("NO", RED)], y=150, size=60, w=260)
    red_x(cr, t, A("q4", "make."), 570, 590, 48)
    if t >= A("q4", "make."):
        card(cr, t, A("q4", "make."), 330, 400, 480, 120, "GOD CAN'T MAKE IT", [], col=RED, title_size=40)
    _corner_kid(cr, t, tl, A("q4") - 0.3)
    vignette(cr, 0.45)


def scene_trap(cr, t, tl):
    A = tl.at
    room(cr, t)
    mate = A("q5", "Checkmate,")
    cr.save()
    enter(cr, camera(t, [(A("q5") - 0.3, (1.0, 360, 640)), (mate, (1.6, 520, 500))], dur=0.5))
    talk = tl.speaking("kid", t)
    classroom(cr, t, tl, kid_pose=dict(arms=("cross", "cross") if t >= mate else ("point", "down"),
                                       eyes="half" if t >= mate else "open", mouth="talk" if talk else "smug",
                                       brows="raise"),
              look_at=(560, 0), gasp=True)
    cr.restore()
    if t < mate:
        for side, lab, col in ((-1, "YES", GREEN), (1, "NO", RED)):
            x = 360 + side * 120
            card(cr, t, A("q5"), x, 330, 220, 150, lab, [], col=col, title_size=46)
            red_x(cr, t, A("q5") + 0.1, x, 360, 44)
        sign(cr, t, A("q5", "all-powerful."), 360, 150, "NOT ALL-POWERFUL", col=RED, size=56)
    else:
        stamp(cr, t, mate, 360, 170, "CHECKMATE", col=PURPLE, size=90)
        sign(cr, t, mate + 0.3, 360, 330, "OOOOH!", col=GOLD, size=64, rot=0.05)
    vignette(cr, 0.4)


def chalk_stick(cr, x, y, rot=0.0, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -30, -8, 60, 16, 6)
    paint(cr, WHITE, OUTLINE, 3)
    cr.restore()


def scene_smile(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    smiling = t >= A("q6", "smiles,")
    cr.save()
    enter(cr, camera(t, [(A("q6") - 0.3, (1.0, 360, 640)), (A("q6", "smiles,"), (1.35, 300, 600))], dur=0.6))
    sir(cr, t, tl, 280, 1080, 1.25, eyes="half" if smiling else "wide", rest="smug" if smiling else "o",
        brows="raise" if smiling else "up", arms=("out", "down") if t >= A("q6", "chalk.") else ("hips", "down"))
    cr.restore()
    c0 = A("q6", "hands")
    if t >= c0:                       # the chalk flies to the kid, off to the right
        u = seg(t, c0, c0 + 0.7)
        chalk_stick(cr, lerp(460, 760, u), 640 - 180 * math.sin(u * math.pi), rot=u * 9, s=1.3)
        cue("whoosh", t, c0, 0.5)
    if smiling:
        sparkles(cr, t, A("q6", "smiles,"), 330, 520, n=5, seed=6, col=GOLD, spread=120)
    sign(cr, t, A("q6", "But"), 360, 140, "BUT...", col=GOLD, size=72)
    vignette(cr, 0.4)


def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    draw0 = A("q7", "square")
    verdict = A("q9", "square")
    if draw0 <= t < verdict:
        u = morph(t - draw0, 1.4)
        square_circle(cr, 360, 310, 120 * appear(t, draw0, 0.4), u, col=(1, 1, 1, 0.92))
    if t >= verdict:
        card(cr, t, verdict, 360, 345, 540, 260, "A SQUARE CIRCLE IS", ["not hard...", "NOT A THING."],
             col=PURPLE, title_size=42, line_size=52, mark="no", mark_at=A("q9", "thing"))
    stuck = t >= A("q8")
    talk = tl.speaking("kid", t)
    person(cr, t, 200, 1060, 0.9, "kid", eyes="wide" if stuck else "open", mouth="talk" if talk else ("o" if stuck else "smile"),
           arms=("face", "down") if stuck else ("up", "down"), brows="up" if stuck else None, sweat=stuck, facing=1,
           hold=None if stuck else (lambda c, hx, hy: chalk_stick(c, hx, hy, -0.6)))
    sir(cr, t, tl, 560, 1060, 0.95, eyes="happy" if t >= A("q9") else "half", rest="smug",
        arms=("point", "hips") if t >= A("q9") else ("cross", "cross"), facing=-1)
    w0 = A("q9", "weak.")
    if w0 <= t < verdict:          # it's not about strength
        bold_text(cr, "STRENGTH", 360, 515, 44 * appear(t, w0, 0.3), GOLD)
        red_x(cr, t, w0 + 0.1, 360, 500, 56)
    sign(cr, t, A("q8"), 360, 110, "IMPOSSIBLE!", col=RED, size=60, end=A("q9") - 0.05)
    sign(cr, t, A("q9"), 360, 110, "EXACTLY.", col=GREEN, size=64, end=verdict - 0.05)
    vignette(cr, 0.35)


def scene_words(cr, t, tl):
    A = tl.at
    hill(cr, t)
    s0 = A("q10")
    sq = A("q10", "square")
    u = ease_out(seg(t, sq, sq + 0.8))
    glow(cr, t, 360, 330, 80, 0.8 * (1 - u))
    rock(cr, 360, 830, 1.0 * (1 - u) + 0.01, a=1 - u)
    if u > 0:
        square_circle(cr, 360, 560, 150 * u, morph(t, 1.2), col=(1, 0.95, 0.7, 1), lw=10)
    if t >= A("q10", "words."):
        k = appear(t, A("q10", "words."), 0.4)
        for i, w in enumerate(("ROCK", "GOD", "CAN'T", "LIFT", "HEAVY")):
            ang = t * 0.8 + i * 2 * math.pi / 5
            bold_text(cr, w, 360 + math.cos(ang) * 240, 560 + math.sin(ang) * 210, 40 * k, WHITE)
    sign(cr, t, s0, 360, 170, "THE IMPOSSIBLE ROCK", col=GOLD, size=54, end=A("q10", "Same") - 0.05)
    sign(cr, t, A("q10", "Same"), 360, 170, "SAME THING", col=PURPLE, size=60, end=A("q10", "words.") - 0.05)
    stamp(cr, t, A("q10", "words."), 360, 190, "MADE OF WORDS", col=RED, size=70)
    portrait(cr, t, s0, 610, 330, 76, "sir", eyes="happy", mouth=mouth_of(tl, "sir", t, "smug"), bg=hexc("#ffd84d"))
    vignette(cr, 0.45)


def scene_aquinas(cr, t, tl):
    A = tl.at
    monastery(cr, t)
    answer = A("q12")
    if t < answer:
        person(cr, t, 360, 960, 1.0, "aquinas", eyes="happy" if t >= A("q11", "750") else "open", mouth="smile",
               arms=("hold", "down"), hold=book)
        tag(cr, t, A("q11", "Thomas"), 360, 200, "THOMAS AQUINAS", col=CANDLE)
        sign(cr, t, A("q11", "750"), 360, 320, "~750 YEARS AGO", col=PURPLE, size=50, rot=0.03)
    else:
        person(cr, t, 150, 1010, 0.7, "aquinas", eyes="happy", mouth="smile", arms=("point", "down"))
        card(cr, t, answer, 400, 330, 560, 230, "ALL-POWERFUL MEANS", ["can do anything", "POSSIBLE"], col=GREEN,
             title_size=40, line_size=44, mark="ok", mark_at=A("q12", "possible."))
        card(cr, t, A("q12", "contradiction"), 400, 620, 560, 200, "A CONTRADICTION", ["isn't anything"], col=RED,
             title_size=40, line_size=44, mark="no", mark_at=A("q12", "anything."))
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    classroom(cr, t, tl, kid_pose=dict(arms=("chin", "down"), eyes="half", mouth="flat"), look_at=(360, 0))
    sir(cr, t, tl, 150, 1120, 1.0, eyes="happy", rest="smug", arms=("hips", "hips"))
    buttons(cr, t, A("q13", "teacher"), [("TEACHER WON", GREEN), ("HE DODGED IT", RED)], y=330, size=40, w=320)
    sign(cr, t, A("q13"), 360, 150, "YOUR VERDICT?", col=GOLD, size=64)
    vignette(cr, 0.4)


SCENES = {"ask": scene_ask, "freeze": scene_freeze, "yes": scene_yes, "no": scene_no, "trap": scene_trap,
          "smile": scene_smile, "board": scene_board, "words": scene_words, "aquinas": scene_aquinas,
          "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
