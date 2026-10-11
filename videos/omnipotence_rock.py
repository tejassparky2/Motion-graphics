"""Can God make a rock so heavy that even God can't lift it? -- the omnipotence paradox in the polished look.

Thomas Aquinas, Summa Theologiae I, q.25, a.3 (about 1270): God's power covers everything possible, and "whatever
implies contradiction does not come within the scope of divine omnipotence, because it cannot have the aspect of
possibility". C.S. Lewis, The Problem of Pain (1940), ch. 2: "nonsense remains nonsense even when we talk it about
God". Line o12 is a paraphrase of Aquinas, not a quote. God is shown only as light, never as a figure.
First video made with the youtube-agent skills (yt-plan, yt-script, yt-package, yt-seo); script in
out/scripts_batch_47-50.md, made at the owner's request on 11 Oct 2026 ("Now make 1 video with new skills with analysis").
"""
import math

from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PURPLE, RED, buttons, card, check, knot, red_x, shake, sparkles,
                         studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, particles,
                           put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite, stamp, stroke_line,
                           vignette)
from motion.toons import person, portrait
from videos.first_cause import CANDLE, book, glow, monastery

NARRATOR = dict(speed=0.92)
TAIL = 0.9

SCRIPT = [
    dict(id="o1", scene="hook", text="Can God make a rock so heavy, that even God can't lift it?", pace=0.95),
    dict(id="o2", scene="choice", text="Think about it.", gap=0.3),
    dict(id="o3", scene="yes", text="If the answer is yes, there's a rock God can't lift."),
    dict(id="o4", scene="yes", text="So God isn't all-powerful."),
    dict(id="o5", scene="no", text="If the answer is no, there's a rock God can't make.", gap=0.3),
    dict(id="o6", scene="no", text="So, again, not all-powerful."),
    dict(id="o7", scene="trap", text="Either way, all-powerful loses. That's the trap.", gap=0.3),
    dict(id="o8", scene="square", text="Now, try this. Draw a square circle.", gap=0.3),
    dict(id="o9", scene="square", text="You can't. But not because you're weak."),
    dict(id="o10", scene="square", text="A square circle isn't a hard thing to draw. It's not a thing at all."),
    dict(id="o11", scene="aquinas", text="About [seven hundred and fifty years ago,|750 years ago,] Thomas Aquinas "
                                         "made the same move.", gap=0.3),
    dict(id="o12", scene="aquinas", text="His answer: all-powerful means able to do anything possible. And a "
                                         "contradiction isn't anything."),
    dict(id="o13", scene="words", text="So the impossible rock is just a square circle, made of words."),
    dict(id="o14", scene="lewis", text="Centuries later, [C. S. Lewis|C.S. Lewis] put it simply: nonsense remains "
                                       "nonsense, even when we talk it about God.", gap=0.3),
    dict(id="o15", scene="end", text="So, is that a clever answer, or a clever escape?", gap=0.3, pace=0.95),
]

METADATA = dict(
    title="1 Rock. 2 Answers. Both Break God?",
    alt_titles=["The Rock Even God Can't Lift 🪨", "Can God Make a Rock He Can't Lift? 🪨",
                "Yes or No? Either Way, God Loses 🪨"],
    description="""Can God make a rock so heavy He can't lift it? The omnipotence paradox in 45 seconds, and Aquinas's answer. 🪨

If the answer is yes, there's a rock God can't lift. So God isn't all-powerful.
If the answer is no, there's a rock God can't make. So, again, not all-powerful. Either way, all-powerful loses.

Now try to draw a square circle. You can't, but not because you're weak: a square circle isn't a hard thing to draw, it's not a thing at all.
About 750 years ago, Thomas Aquinas made the same move: all-powerful means able to do anything possible, and a contradiction isn't anything. So the impossible rock is just a square circle, made of words.
Centuries later, C.S. Lewis put it simply: "nonsense remains nonsense even when we talk it about God."

Sources: Thomas Aquinas, Summa Theologiae I, q.25, a.3; C.S. Lewis, The Problem of Pain (1940), ch. 2.

💬 So, is that a clever answer, or a clever escape? Keep it respectful 🙏👇

🔔 Interestingly Strange: mind-bending paradoxes, big theories, weird history and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#Philosophy", "#Shorts"],
    tags=["omnipotence paradox", "can god make a rock he can't lift", "paradox", "philosophy", "aquinas",
          "logic puzzle", "god paradox", "c.s. lewis", "square circle", "interestingly strange"],
    pinned_comment="Clever answer, or clever escape? 🪨 Defend your pick (respectfully) 👇",
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


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    hill(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("o1", "heavy,"), (1.12, 360, 700)),
                         (A("o1", "lift"), (1.2, 360, 620))], dur=0.6))
    k = 0.6 + 0.4 * appear(t, A("o1", "God"), 0.6)
    glow(cr, t, 360, 330, 100 * k, k)
    lifting = t >= A("o1", "lift")
    beam(cr, t, 360, 380, 360, 600, appear(t, A("o1", "lift"), 0.3) if lifting else 0)
    rock(cr, 360, 830, 1.0 + 0.1 * ease_out(appear(t, A("o1", "heavy,"), 0.5)), tremble=3 if lifting else 0, t=t)
    cr.restore()
    stamp(cr, t, A("o1", "heavy,"), 360, 105, "TOO HEAVY?", col=RED, size=62, rot=-0.06, end=A("o1", "lift") - 0.05)
    if lifting:
        bold_text(cr, "?", 620, 470 + math.sin(t * 5) * 8, 150 * appear(t, A("o1", "lift"), 0.4), GOLD)
    vignette(cr, 0.45)


def scene_choice(cr, t, tl):
    A = tl.at
    hill(cr, t)
    glow(cr, t, 360, 300, 90, 0.9)
    rock(cr, 360, 830, 0.85)
    buttons(cr, t, A("o2"), [("YES", GREEN), ("NO", RED)], y=480, size=60, w=280)
    sign(cr, t, A("o2", "Think"), 360, 150, "YES OR NO?", col=GOLD, size=70)
    vignette(cr, 0.45)


def scene_yes(cr, t, tl):
    A = tl.at
    hill(cr, t)
    strain = t >= A("o3", "can't")
    cr.save()
    enter(cr, camera(t, [(A("o3"), (1.0, 360, 640)), (A("o3", "can't"), (1.1, 360, 640))], dur=0.5))
    glow(cr, t, 360, 300, 90, 0.9)
    beam(cr, t, 360, 340, 360, 600, 1.0 if strain else appear(t, A("o3", "rock"), 0.4))
    rock(cr, 360, 830, 1.0, tremble=4 if strain else 0, t=t)
    if strain:
        for k in range(3):     # dust puffs: it won't budge
            ph = (t * 1.4 + k / 3) % 1
            soft_disc(cr, 160 + k * 200, 820 - ph * 60, 30 + ph * 30, (1, 1, 1, 0.35 * (1 - ph)))
    cr.restore()
    buttons(cr, t, A("o3"), [("YES", GREEN)], y=150, size=60, w=260)
    red_x(cr, t, A("o3", "can't"), 570, 560, 48)
    if t >= A("o4"):
        dx, dy = shake(t, A("o4", "isn't"), 0.4, 10)
        card(cr, t, A("o4"), 360 + dx, 380 + dy, 560, 150, "GOD CAN'T LIFT IT", ["so: NOT all-powerful"], col=RED,
             title_size=40, line_size=40)
    vignette(cr, 0.45)


def scene_no(cr, t, tl):
    A = tl.at
    hill(cr, t)
    glow(cr, t, 360, 300, 90, 0.9)
    ghost_rock(cr, t, 360, 830, 1.0)
    if t >= A("o5", "make."):
        sparkles(cr, t, A("o5", "make."), 360, 700, n=6, seed=3, col=(1, 0.95, 0.7, 1), spread=160)
    buttons(cr, t, A("o5"), [("NO", RED)], y=150, size=60, w=260)
    red_x(cr, t, A("o5", "make."), 570, 590, 48)
    if t >= A("o6"):
        dx, dy = shake(t, A("o6", "again,"), 0.4, 12)
        card(cr, t, A("o6"), 360 + dx, 420 + dy, 560, 150, "GOD CAN'T MAKE IT", ["so: NOT all-powerful"], col=RED,
             title_size=40, line_size=40)
    vignette(cr, 0.45)


def scene_trap(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2a2450"), hexc("#5a3a6a"), seed=6)
    hit = A("o7", "loses.")
    u = ease_out(seg(t, A("o7"), hit))
    for side, lab in ((-1, "YES"), (1, "NO")):
        x = lerp(360 + side * 230, 360 + side * 112, u)
        card(cr, t, A("o7"), x, 540, 220, 170, lab, [], col=GREEN if lab == "YES" else RED, title_size=46)
        red_x(cr, t, A("o7") + 0.1, x, 575, 44)
    if t >= hit:
        cue("hit", t, hit)
        sparkles(cr, t, hit, 360, 540, n=10, seed=7, col=(1, 0.9, 0.5, 1), spread=200)
    if t >= A("o7", "trap."):
        knot(cr, t, A("o7", "trap."), 360, 760, 100, RED, label=None)
    sign(cr, t, A("o7", "Either"), 360, 170, "EITHER WAY...", col=PURPLE, size=64, end=A("o7", "That's") - 0.05)
    stamp(cr, t, A("o7", "That's"), 360, 190, "THE TRAP", col=RED, size=84)
    vignette(cr, 0.4)


def scene_square(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe6ff"), hexc("#fff1d6"), seed=3)
    chalkboard(cr, 360, 400, 600, 420)
    drawing = A("o8", "Draw")
    verdict = A("o10")
    if drawing <= t < verdict:
        u = morph(t - drawing, 1.4)
        square_circle(cr, 360, 400, 130 * appear(t, drawing, 0.4), u, col=(1, 1, 1, 0.9))
    if t >= verdict:
        card(cr, t, verdict, 360, 400, 520, 230, "A SQUARE CIRCLE IS", ["not hard...", "NOT A THING."],
             col=PURPLE, title_size=40, line_size=48, mark="no", mark_at=A("o10", "thing", nth=2))
    stuck = t >= A("o9")
    person(cr, t, 150, 1000, 0.75, "kid", eyes="wide" if stuck else "open", mouth="o" if stuck else "smile",
           arms=("point", "down") if not stuck else ("face", "down"), hold=None if stuck else chalk,
           brows="up" if stuck else None, sweat=stuck)
    w0 = A("o9", "weak.")
    if w0 <= t < verdict:          # it's not about strength
        bold_text(cr, "STRENGTH", 500, 728, 50 * appear(t, w0, 0.3), GOLD)
        red_x(cr, t, w0 + 0.1, 500, 710, 70)
    sign(cr, t, A("o8", "try"), 360, 110, "TRY THIS", col=BLUE, size=64, end=A("o9") - 0.05)
    vignette(cr, 0.35)


def scene_aquinas(cr, t, tl):
    A = tl.at
    monastery(cr, t)
    answer = A("o12")
    if t < answer:
        person(cr, t, 360, 960, 1.0, "aquinas", eyes="happy" if t >= A("o11", "move.") else "open",
               mouth="talk" if tl.speaking("aquinas", t) else "smile", arms=("hold", "down"), hold=book)
        tag(cr, t, A("o11", "Thomas"), 360, 200, "THOMAS AQUINAS", col=CANDLE)
        sign(cr, t, A("o11", "750"), 360, 320, "~750 YEARS AGO", col=PURPLE, size=50, rot=0.03)
    else:
        person(cr, t, 150, 1010, 0.7, "aquinas", eyes="happy", mouth="smile", arms=("point", "down"))
        card(cr, t, answer, 400, 330, 560, 230, "ALL-POWERFUL MEANS", ["can do anything", "POSSIBLE"], col=GREEN,
             title_size=40, line_size=44, mark="ok", mark_at=A("o12", "possible."))
        card(cr, t, A("o12", "contradiction"), 400, 620, 560, 200, "A CONTRADICTION", ["isn't anything"], col=RED,
             title_size=40, line_size=44, mark="no", mark_at=A("o12", "anything.", nth=1))
    vignette(cr, 0.45)


def scene_words(cr, t, tl):
    A = tl.at
    hill(cr, t)
    s0 = A("o13")
    u = ease_out(seg(t, A("o13", "square"), A("o13", "square") + 0.8))
    rock(cr, 360, 830, 1.0 * (1 - u) + 0.01, a=1 - u)
    if u > 0:
        square_circle(cr, 360, 560, 150 * u, morph(t, 1.2), col=(1, 0.95, 0.7, 1), lw=10)
    if t >= A("o13", "words."):
        k = appear(t, A("o13", "words."), 0.4)
        for i, w in enumerate(("ROCK", "GOD", "CAN'T", "LIFT", "HEAVY")):
            ang = t * 0.8 + i * 2 * math.pi / 5
            bold_text(cr, w, 360 + math.cos(ang) * 240, 560 + math.sin(ang) * 210, 40 * k, WHITE)
    sign(cr, t, s0, 360, 170, "THE IMPOSSIBLE ROCK", col=GOLD, size=54, end=A("o13", "square") - 0.05)
    sign(cr, t, A("o13", "square"), 360, 170, "= A SQUARE CIRCLE", col=PURPLE, size=56, end=A("o13", "words.") - 0.05)
    stamp(cr, t, A("o13", "words."), 360, 190, "MADE OF WORDS", col=RED, size=70)
    vignette(cr, 0.45)


def scene_lewis(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#e8dcc8"), hexc("#fff4e4"), seed=9)
    portrait(cr, t, A("o14") + 0.1, 360, 330, 170, "lewis", eyes="half", mouth="smile", bg=hexc("#c9a46a"))
    tag(cr, t, A("o14", "Lewis"), 360, 120, "C.S. LEWIS, 1940", col=hexc("#c9a46a"))
    q = A("o14", "nonsense")
    if t >= q:
        card(cr, t, q, 360, 650, 600, 300, "“NONSENSE REMAINS", ["NONSENSE,", "even when we talk", "it about God.”"],
             col=PURPLE, title_size=40, line_size=44, rot=-0.02)
    sign(cr, t, A("o14", "Centuries"), 360, 580, "CENTURIES LATER", col=GOLD, size=50, end=q - 0.05)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    hill(cr, t)
    glow(cr, t, 360, 300, 80, 0.8)
    rock(cr, 360, 830, 0.8, tremble=1.5, t=t)
    buttons(cr, t, A("o15", "clever"), [("CLEVER ANSWER", GREEN), ("CLEVER ESCAPE", RED)], y=470, size=40, w=320)
    sign(cr, t, A("o15"), 360, 150, "YOUR VERDICT?", col=GOLD, size=64)
    vignette(cr, 0.45)


SCENES = {"hook": scene_hook, "choice": scene_choice, "yes": scene_yes, "no": scene_no, "trap": scene_trap,
          "square": scene_square, "aquinas": scene_aquinas, "words": scene_words, "lewis": scene_lewis,
          "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
