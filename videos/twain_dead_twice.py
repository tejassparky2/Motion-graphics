"""Mark Twain was reported dead, twice -- clever words from history, in the polished look.

1897 (London): his cousin James Ross Clemens was seriously ill; reports spread that Twain was ill, then dead. Asked by
Frank Marshall White of the New York Journal, Twain wrote (note dated 31 May 1897, published 2 June 1897): "The report
of my illness grew out of his illness; the report of my death was an exaggeration." The popular "greatly/grossly
exaggerated" versions come later (Paine's 1912 biography has "grossly exaggerated").
1907: Twain sailed back from Norfolk, Virginia on H. H. Rogers' yacht Kanawha, which "slipped out of Hampton Roads
during a fog"; NYT 4 May 1907: "TWAIN AND YACHT DISAPPEAR AT SEA". NYT 5 May 1907, "Mark Twain Investigating": he was
"safe in his rooms in Fifth Avenue" and said: "I will make an exhaustive investigation of this report that I have been
lost at sea. If there is any foundation for the report, I will at once apprise the anxious public."
He died on 21 April 1910. Sources: Mental Floss; WIST; Wikisource (NYT 1907). Script approved 7 Oct 2026.
"""
import math
import random

from motion.engine import W, H, cairo, clamp01, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, light_rays, lin, paint, particles, put, rad, rrect, shade, sign, smooth,
                           soft_disc, soft_rrect, sprite, stamp, stroke_line, vignette)
from motion.toons import head, person, portrait

NARRATOR = dict()
TAIL = 0.9

SCRIPT = [
    dict(id="m1", scene="hook", text="Mark Twain had to tell the newspapers he wasn't dead. Twice."),
    dict(id="m2", scene="london", text="London. [Eighteen ninety-seven.|1897.]"),
    dict(id="m3", scene="rumor", text="His cousin is seriously ill. Soon people are saying it's Twain who's sick. "
                                      "Then, that he's dead."),
    dict(id="m4", scene="door", text="A New York reporter knocks on his door to check."),
    dict(id="m5", scene="door", text="Twain writes him a note."),
    dict(id="m6", scene="note", text="The report of my illness grew out of his illness. The report of my death was "
                                     "an exaggeration.", speaker="twain", pace=0.95),
    dict(id="m7", scene="misquote", text="That's the real line. Not \"greatly exaggerated.\" That version came "
                                         "later."),
    dict(id="m8", scene="yacht", text="Ten years later, [nineteen oh seven.|1907.] Twain sails home from Virginia on "
                                      "a friend's yacht."),
    dict(id="m9", scene="yacht", text="The yacht slips away in the fog. Nobody hears from it."),
    dict(id="m10", scene="paper", text="The New York Times prints: Twain and yacht disappear at sea."),
    dict(id="m11", scene="home", text="Twain was safe at home in New York. And he told reporters this."),
    dict(id="m12", scene="home", text="I will make an exhaustive investigation of this report that I have been lost "
                                      "at sea.", speaker="twain", pace=0.95),
    dict(id="m13", scene="home", text="If there is any foundation for the report, I will at once apprise the "
                                      "anxious public.", speaker="twain", pace=0.95),
    dict(id="m14", scene="final", text="He died for real in [nineteen ten.|1910.] That time, the papers got it "
                                       "right."),
    dict(id="m15", scene="end", text="Which comeback is funnier? The first, or the second?", gap=0.3),
]

METADATA = dict(
    title="Mark Twain Had To Tell The Papers He Wasn't Dead. Twice. 💀",
    alt_titles=["\"The Report of My Death Was an Exaggeration\" (The Real Story) 📰",
                "Mark Twain Was Declared Dead TWICE. His Replies Were Perfect. 😂"],
    description="""Mark Twain had to tell the newspapers he wasn't dead. Twice. 💀

1897, London: his cousin was seriously ill, and soon people were saying it was Twain who was sick... then that he was dead. A New York reporter came to check, and Twain wrote him a note: "The report of my illness grew out of his illness; the report of my death was an exaggeration."
That's the real line. The famous "greatly exaggerated" version came later.

1907: Twain sailed home from Virginia on a friend's yacht. It slipped away in the fog, nobody heard from it, and The New York Times printed: "Twain and yacht disappear at sea." He was safe at home in New York, and told reporters: "I will make an exhaustive investigation of this report that I have been lost at sea. If there is any foundation for the report, I will at once apprise the anxious public."

He died for real in 1910. That time, the papers got it right.

Sources: Twain's note of May 31, 1897 (New York Journal, June 2, 1897); The New York Times, May 4 and May 5, 1907; A. B. Paine's 1912 biography (the "grossly exaggerated" version).

💬 Which comeback is funnier, the first or the second? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, animated in under a minute.""",
    hashtags=["#MarkTwain", "#History", "#Shorts"],
    tags=["mark twain", "reports of my death are greatly exaggerated", "mark twain quote", "famous misquotes",
          "history facts", "funny history", "clever comebacks", "new york times 1907", "interestingly strange"],
    pinned_comment="1897 or 1907: which reply was funnier? 👇 (And yes, he never said \"greatly\" 😉)",
)

RED = hexc("#e8473f")
GOLD = hexc("#ffcf3f")
BLUE = hexc("#4aa3f0")
GREEN = hexc("#3fbf6a")
PURPLE = hexc("#7a5bd0")
PAPER = hexc("#f6efdc")
INKC = hexc("#2b1d16")


# ---------------------------------------------------------------- backgrounds (cached, screen space)
def _london(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#5a6a8a")), (0.55, hexc("#b9b4c8")), (0.56, hexc("#7a7488")),
                                  (1, hexc("#4a4658"))]))
    c.fill()
    # Big Ben and rooftops
    c.set_source_rgba(*hexc("#4a5068"))
    rrect(c, 470, 180, 110, 540, 4)
    c.fill()
    c.move_to(462, 186)
    c.line_to(525, 60)
    c.line_to(588, 186)
    c.close_path()
    c.fill()
    c.arc(525, 260, 38, 0, 2 * math.pi)
    c.set_source_rgba(*hexc("#f4e6b8"))
    c.fill()
    stroke_line(c, [(525, 260), (525, 234)], 4, hexc("#4a5068"), curve=False)
    stroke_line(c, [(525, 260), (543, 266)], 4, hexc("#4a5068"), curve=False)
    rng = random.Random(5)
    x = -20
    while x < W:
        w = rng.uniform(80, 150)
        h = rng.uniform(140, 300)
        c.rectangle(x, 720 - h, w, h)
        c.set_source_rgba(*hexc("#3e4258"))
        c.fill()
        for j in range(int(h // 60)):
            for i in range(int(w // 40)):
                if rng.random() < 0.45:
                    c.rectangle(x + 12 + i * 40, 720 - h + 20 + j * 60, 16, 22)
                    c.set_source_rgba(1, 0.86, 0.5, 0.8)
                    c.fill()
        x += w + 6
    for lx in (110, 610):     # gas lamps
        stroke_line(c, [(lx, 900), (lx, 610)], 10, hexc("#2b2b33"), curve=False)
        rrect(c, lx - 22, 570, 44, 50, 6)
        paint(c, hexc("#ffe8a0"), hexc("#2b2b33"), 5)
        soft_disc(c, lx, 595, 120, (1, 0.9, 0.55, 0.35))


def london(cr, t):
    put(cr, sprite("london", W, H, _london), 0, 0)
    fog(cr, t, 0.55)


def fog(cr, t, a=0.5, y0=520):
    for k in range(5):
        x = ((t * (14 + k * 6) + k * 260) % (W + 600)) - 300
        y = y0 + k * 70
        put(cr, sprite(("fog", k % 2), 600, 220, lambda c: (ellipse(c, 300, 110, 280, 80), c.set_source_rgba(
            1, 1, 1, 1), c.fill()), sigma=30, scale=0.25), x - 300, y - 110, a=a * 0.6)


def _room(c, door=False):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 860, [(0, hexc("#8a5a7a")), (1, hexc("#c99aa8"))]))
    c.fill()
    for k in range(0, W, 60):      # wallpaper stripes
        c.rectangle(k, 0, 24, 860)
        c.set_source_rgba(1, 1, 1, 0.06)
        c.fill()
    c.rectangle(0, 860, W, H - 860)
    c.set_source(lin(0, 860, 0, H, [(0, hexc("#a8713e")), (1, hexc("#6b4422"))]))
    c.fill()
    c.rectangle(0, 850, W, 14)
    c.set_source_rgba(*hexc("#5a3418"))
    c.fill()
    if not door:
        rrect(c, 420, 520, 260, 340, 10)      # fireplace
        paint(c, lin(0, 520, 0, 860, [(0, hexc("#c9b8a8")), (1, hexc("#9a8878"))]), OUTLINE, 6)
        rrect(c, 470, 640, 160, 220, 8)
        paint(c, hexc("#2b1d16"), OUTLINE, 5)
        rrect(c, 400, 500, 300, 30, 6)
        paint(c, hexc("#7a4a2a"), OUTLINE, 5)
        rrect(c, 70, 200, 200, 250, 8)       # a framed painting
        paint(c, lin(0, 200, 0, 450, [(0, hexc("#d9a64e")), (1, hexc("#9a6a20"))]), OUTLINE, 6)
        rrect(c, 92, 222, 156, 206, 4)
        paint(c, lin(0, 222, 0, 428, [(0, hexc("#9fd8ff")), (1, hexc("#5aa043"))]), OUTLINE, 3)


def room(cr, t, door=False):
    put(cr, sprite(("twroom", door), W, H, lambda c: _room(c, door)), 0, 0)
    if not door:
        flames(cr, t, 550, 850)


def flames(cr, t, x, y):
    soft_disc(cr, x, y - 60, 140, (1, 0.6, 0.2, 0.25 + 0.05 * math.sin(t * 9)))
    for k, (col, s) in enumerate(((hexc("#ff7a2a"), 1.0), (hexc("#ffd84d"), 0.6))):
        f = 1 + 0.08 * math.sin(t * 11 + k)
        smooth(cr, [(x - 60 * s, y - 10), (x - 40 * s, y - 90 * s * f), (x - 10 * s, y - 60 * s),
                    (x + 5 * s, y - 140 * s * f), (x + 30 * s, y - 70 * s), (x + 50 * s, y - 100 * s * f),
                    (x + 60 * s, y - 10)])
        paint(cr, col, None, 0)


def sea(cr, t, mood="day"):
    sky = {"day": [(0, hexc("#7cc6ff")), (0.55, hexc("#d9f0ff"))],
           "fog": [(0, hexc("#9aa4b4")), (0.55, hexc("#d4d8de"))]}[mood]
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, 700, sky))
    cr.fill()
    cr.rectangle(0, 700, W, H - 700)
    cr.set_source(lin(0, 700, 0, H, [(0, hexc("#3f8fc8") if mood == "day" else hexc("#6a8098")),
                                     (1, hexc("#1d4a7a") if mood == "day" else hexc("#3a4a5a"))]))
    cr.fill()
    for k in range(7):
        y = 730 + k * 70
        cr.move_to(0, y)
        for x in range(0, W + 41, 40):
            cr.line_to(x, y + 8 * math.sin(x / 50.0 + t * 2 + k))
        cr.set_source_rgba(1, 1, 1, 0.18)
        cr.set_line_width(4)
        cr.stroke()


def studio(cr, t, top, bottom, seed=1):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, top), (1, bottom)]))
    cr.fill()
    bokeh(cr, t, seed, 14, [WHITE, hexc("#ffe7a8")], rmin=20, rmax=70)


# ---------------------------------------------------------------- props
def newspaper(cr, t, x, y, s, headline, sub=None, date=None, rot=0.0, mast="THE DAILY NEWS"):
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_rrect(cr, -250, -300, 500, 620, 10, (0, 0, 0, 0.35), sigma=14)
    rrect(cr, -250, -310, 500, 620, 6)
    paint(cr, lin(0, -310, 0, 310, [(0, hexc("#fbf7ea")), (1, hexc("#e8dfc6"))]), OUTLINE, 5)
    cr.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(40)
    ext = cr.text_extents(mast)
    if ext.x_advance > 440:
        cr.set_font_size(40 * 440 / ext.x_advance)
        ext = cr.text_extents(mast)
    cr.move_to(-ext.x_advance / 2, -250)
    cr.set_source_rgba(*INKC)
    cr.show_text(mast)
    stroke_line(cr, [(-225, -232), (225, -232)], 3, INKC, curve=False)
    if date:
        cr.select_font_face("serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(20)
        ext = cr.text_extents(date)
        cr.move_to(-ext.x_advance / 2, -210)
        cr.show_text(date)
    stroke_line(cr, [(-225, -200), (225, -200)], 2, INKC, curve=False)
    y0 = -140
    for line in headline:
        bold_text(cr, line, 0, y0, 50, INKC, outline=None, shadow=0)
        y0 += 58
    if sub:
        cr.select_font_face("serif", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(24)
        ext = cr.text_extents(sub)
        cr.move_to(-ext.x_advance / 2, y0 - 10)
        cr.show_text(sub)
        y0 += 20
    for col in range(3):     # body-text lines
        for k in range(8):
            yy = y0 + 10 + k * 22
            if yy > 285:
                break
            stroke_line(cr, [(-225 + col * 155, yy), (-95 + col * 155 - (k % 3) * 10, yy)], 6,
                        alpha(INKC, 0.25), curve=False)
    cr.restore()


def quill(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.6)
    smooth(cr, [(0, 0), (-12, -60), (-4, -130), (10, -70), (6, 0)])
    paint(cr, lin(0, -130, 0, 0, [(0, WHITE), (1, hexc("#d8d8e0"))]), OUTLINE, 3.5)
    stroke_line(cr, [(2, 10), (-2, -110)], 2.5, alpha(OUTLINE, 0.5))
    cr.restore()


def magnifier(cr, hx, hy):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.5)
    rrect(cr, -9, 0, 18, 70, 8)
    paint(cr, hexc("#6b3f22"), OUTLINE, 4)
    cr.arc(0, -46, 46, 0, 2 * math.pi)
    paint(cr, (0.8, 0.93, 1.0, 0.45), OUTLINE, 9)
    stroke_line(cr, [(-22, -66), (-6, -80)], 5, alpha(WHITE, 0.9))
    cr.restore()


def teacup(cr, hx, hy):
    cr.save()
    cr.translate(hx + 8, hy - 8)
    ellipse(cr, 0, 18, 46, 10)
    paint(cr, WHITE, OUTLINE, 4)
    cr.move_to(-32, -18)
    cr.curve_to(-30, 22, 30, 22, 32, -18)
    cr.close_path()
    paint(cr, lin(0, -18, 0, 20, [(0, WHITE), (1, hexc("#dfe6ee"))]), OUTLINE, 4)
    ellipse(cr, 0, -18, 32, 8)
    paint(cr, hexc("#a8692e"), OUTLINE, 3.5)
    cr.restore()


def armchair(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    col = hexc("#3f7a5a")
    rrect(cr, -170, -420, 340, 380, 60)
    paint(cr, lin(0, -420, 0, -40, [(0, shade(col, 0.3)), (1, shade(col, -0.2))]), OUTLINE, 6)
    cr.restore()


def armchair_front(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    col = hexc("#3f7a5a")
    for side in (-1, 1):
        rrect(cr, side * 150 - 45, -230, 90, 230, 40)
        paint(cr, lin(0, -230, 0, 0, [(0, shade(col, 0.35)), (1, shade(col, -0.2))]), OUTLINE, 6)
    rrect(cr, -130, -110, 260, 110, 26)
    paint(cr, lin(0, -110, 0, 0, [(0, shade(col, 0.25)), (1, shade(col, -0.25))]), OUTLINE, 6)
    cr.restore()


def calendar(cr, t, start, x, y, top, big, col=RED, s=1.0, end=None):
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    if k <= 0.01:
        return
    cue("pop", t, start)
    cr.save()
    cr.translate(x, y + math.sin(t * 2) * 3)
    cr.rotate(0.04 * math.sin(t * 1.6))
    cr.scale(k * s, k * s)
    soft_rrect(cr, -120, -76, 240, 200, 22, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, -120, -86, 240, 200, 22)
    paint(cr, lin(0, -86, 0, 114, [(0, WHITE), (1, hexc("#e9e2d6"))]), OUTLINE, 6)
    cr.save()
    rrect(cr, -120, -86, 240, 200, 22)
    cr.clip()
    cr.rectangle(-120, -86, 240, 58)
    cr.set_source(lin(0, -86, 0, -28, [(0, shade(col, 0.2)), (1, col)]))
    cr.fill()
    cr.restore()
    bold_text(cr, top, 0, -42, 34, WHITE)
    bold_text(cr, big, 0, 72, 80, INKC, outline=None, shadow=0)
    cr.restore()


def bubble(cr, t, start, x, y, text, col=WHITE, size=40, tail=(-1, 1), end=None):
    """A speech bubble that pops in at `start`."""
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.35)
    if k <= 0.01:
        return
    from motion.polish import text_width
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    w = text_width(cr, text, size) + 50
    h = size * 1.6
    soft_rrect(cr, -w / 2, -h / 2 + 8, w, h, h / 2, (0, 0, 0, 0.3), sigma=8)
    cr.move_to(tail[0] * w * 0.2, h / 2 - 4)
    cr.line_to(tail[0] * w * 0.38, h / 2 + 34)
    cr.line_to(tail[0] * w * 0.05, h / 2 - 4)
    cr.close_path()
    paint(cr, col, OUTLINE, 5)
    rrect(cr, -w / 2, -h / 2, w, h, h / 2)
    paint(cr, col, OUTLINE, 5)
    bold_text(cr, text, 0, size * 0.36, size, INKC, outline=None, shadow=0)
    cr.restore()


def note_card(cr, t, lines, x, y, w=600, size=40):
    """Twain's handwritten note: each line writes itself from its start time."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.02)
    h = 90 + len(lines) * size * 1.35
    soft_rrect(cr, -w / 2, -h / 2 + 12, w, h, 14, (0, 0, 0, 0.35), sigma=12)
    rrect(cr, -w / 2, -h / 2, w, h, 14)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, hexc("#fffaf0")), (1, hexc("#efe4c8"))]), OUTLINE, 5)
    for k in range(len(lines) + 1):
        yy = -h / 2 + 60 + k * size * 1.35
        stroke_line(cr, [(-w / 2 + 30, yy + 10), (w / 2 - 30, yy + 10)], 2, alpha(hexc("#7aa8d8"), 0.4),
                    curve=False)
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    for k, (txt, st, dur) in enumerate(lines):
        if t < st:
            continue
        u = clamp01((t - st) / dur)
        yy = -h / 2 + 60 + k * size * 1.35
        tw = cr.text_extents(txt).x_advance
        cr.save()
        cr.rectangle(-w / 2 + 30, yy - size, (tw + 10) * u, size * 1.6)
        cr.clip()
        cr.move_to(-w / 2 + 36, yy)
        cr.text_path(txt)
        cr.set_source_rgba(*hexc("#1d2a5a"))
        cr.fill()
        cr.restore()
        cue("scribble", t, st, dur)
    cr.restore()


def red_x(cr, t, start, x, y, r=40):
    if t < start:
        return
    k = appear(t, start, 0.25)
    cue("hit", t, start)
    for d in (-1, 1):
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 16, OUTLINE, curve=False)
        stroke_line(cr, [(x - r * k, y - r * k * d), (x + r * k, y + r * k * d)], 10, RED, curve=False)


def check(cr, t, start, x, y, r=36):
    if t < start:
        return
    k = appear(t, start, 0.3)
    pts = [(x - r * k, y), (x - r * 0.3 * k, y + r * 0.7 * k), (x + r * k, y - r * 0.8 * k)]
    stroke_line(cr, pts, 16, OUTLINE, curve=False)
    stroke_line(cr, pts, 10, GREEN, curve=False)


def yacht(cr, t, x, y, s=1.0, twain=True):
    cr.save()
    cr.translate(x, y + math.sin(t * 1.8) * 6)
    cr.rotate(math.sin(t * 1.3) * 0.03)
    cr.scale(s, s)
    stroke_line(cr, [(0, -40), (0, -420)], 10, OUTLINE, curve=False)
    stroke_line(cr, [(0, -40), (0, -420)], 5, hexc("#c9a46a"), curve=False)
    cr.move_to(10, -410)
    cr.curve_to(150, -300, 170, -150, 180, -60)
    cr.line_to(10, -60)
    cr.close_path()
    paint(cr, lin(0, -410, 0, -60, [(0, WHITE), (1, hexc("#e4e8ee"))]), OUTLINE, 5)
    cr.move_to(-10, -380)
    cr.curve_to(-100, -280, -120, -160, -130, -70)
    cr.line_to(-10, -70)
    cr.close_path()
    paint(cr, lin(0, -380, 0, -70, [(0, WHITE), (1, hexc("#e4e8ee"))]), OUTLINE, 5)
    smooth(cr, [(-12, -420), (40, -440), (-12, -446)])
    paint(cr, RED, OUTLINE, 3)
    if twain:
        person(cr, t, -60, -40, 0.32, "twain", eyes="happy", mouth="grin", arms=("wave", "down"), shadow=False)
    cr.move_to(-260, -50)
    cr.line_to(270, -50)
    cr.curve_to(220, 30, -200, 30, -230, -10)
    cr.close_path()
    paint(cr, lin(0, -50, 0, 20, [(0, WHITE), (1, hexc("#c8d0dc"))]), OUTLINE, 6)
    rrect(cr, -240, -36, 480, 14, 6)
    paint(cr, hexc("#2b4a7a"), None, 0)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    room(cr, t)
    cam = camera(t, [(0, (1.0, 360, 640)), (A("m1", "Twice."), (1.12, 360, 600))], dur=0.6)
    cr.save()
    enter(cr, cam)
    shock = t >= A("m1", "dead.")
    armchair(cr, 360, 900, 1.0)
    person(cr, t, 360, 900, 0.95, "twain", eyes="wide" if shock else "open", mouth="o" if shock else "smile",
           brows="up" if shock else None, arms=("hold", "hold"))
    armchair_front(cr, 360, 905, 1.0)
    cr.restore()
    k = appear(t, 0.1, 0.5)
    newspaper(cr, t, 520, 660 + (1 - k) * 300, 0.46 * k, ["MARK TWAIN", "IS DEAD"], date="(they said)",
              rot=-0.04 + 0.02 * math.sin(t * 2), mast="THE MORNING PAPER")
    sign(cr, t, 0.2, 360, 140, "MARK TWAIN", col=hexc("#9fc8ff"), size=58, sub="FAMOUS WRITER", sub_col=WHITE,
         end=A("m1", "Twice.") - 0.05)
    stamp(cr, t, A("m1", "Twice."), 360, 160, "TWICE!", col=RED, size=110)
    vignette(cr, 0.45)


def scene_london(cr, t, tl):
    A = tl.at
    london(cr, t)
    calendar(cr, t, A("m2", "1897."), 360, 360, "LONDON", "1897", col=hexc("#5a6a8a"))
    sign(cr, t, A("m2"), 360, 150, "LONDON", col=hexc("#9fc8ff"), size=74)
    vignette(cr, 0.5)


def scene_rumor(cr, t, tl):
    A = tl.at
    london(cr, t)
    sick, dead = A("m3", "Twain"), A("m3", "dead.")
    # the cousin, sick in bed, in a lit window
    if t < sick + 0.2:
        k = appear(t, A("m3"), 0.4)
        cr.save()
        cr.translate(360, 470)
        cr.scale(max(k, 0.01), max(k, 0.01))
        rrect(cr, -240, -200, 480, 380, 20)
        paint(cr, lin(0, -200, 0, 180, [(0, hexc("#ffe8b0")), (1, hexc("#f4c880"))]), OUTLINE, 8)
        head(cr, t, -60, 10, 70, "cousin", eyes="half", mouth="sad", brows="sad", sweat=True)
        rrect(cr, -200, 60, 400, 110, 30)
        paint(cr, lin(0, 60, 0, 170, [(0, hexc("#8fb8e8")), (1, hexc("#5a82c0"))]), OUTLINE, 6)
        stroke_line(cr, [(10, 40), (60, 0)], 8, OUTLINE, curve=False)    # thermometer
        stroke_line(cr, [(10, 40), (60, 0)], 4, WHITE, curve=False)
        cr.arc(60, 0, 7, 0, 2 * math.pi)
        paint(cr, RED, OUTLINE, 3)
        cr.restore()
        sign(cr, t, A("m3", "cousin"), 360, 160, "HIS COUSIN", col=hexc("#9fc8ff"), size=60, sub="SERIOUSLY ILL",
             sub_col=WHITE)
    else:
        cam = camera(t, [(sick, (1.0, 360, 640)), (dead, (1.08, 360, 620))], dur=0.6)
        cr.save()
        enter(cr, cam)
        person(cr, t, 170, 900, 0.75, "teacher", glasses=False, shirt=hexc("#c86a8a"), hair_col=hexc("#3a2418"),
               eyes="wide", mouth="talk" if t < dead + 0.6 else "o", arms=("chin", "down"), look=(0.5, 0))
        person(cr, t, 550, 900, 0.75, "reporter", fedora=hexc("#3a3a48"), suit=hexc("#4a4a5c"), eyes="wide",
               mouth="o", arms=("face", "down"), facing=-1, brows="up", look=(-0.5, 0))
        cr.restore()
        bubble(cr, t, sick, 380, 300, "TWAIN IS SICK!", size=44, end=dead - 0.05)
        bubble(cr, t, dead, 380, 300, "TWAIN IS DEAD!", col=hexc("#ffd6d6"), size=48)
        if t >= dead:
            stamp(cr, t, dead + 0.15, 360, 150, "RUMOUR", col=RED, size=74)
    vignette(cr, 0.5)


def door_scene(cr, t, opened):
    put(cr, sprite(("twroom", True), W, H, lambda c: _room(c, True)), 0, 0)
    rrect(cr, 300, 300, 300, 560, 12)       # the doorway
    paint(cr, hexc("#3a2418"), OUTLINE, 8)
    if opened < 1:
        cr.save()
        cr.translate(300, 0)
        cr.scale(1 - 0.75 * opened, 1)
        rrect(cr, 0, 300, 300, 560, 10)
        paint(cr, lin(0, 300, 300, 300, [(0, hexc("#7a3a2a")), (1, hexc("#5a2a1a"))]), OUTLINE, 8)
        for yy in (340, 600):
            rrect(cr, 40, yy, 220, 220, 10)
            paint(cr, None, alpha(OUTLINE, 0.5), 5)
        cr.arc(250, 600, 14, 0, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 4)
        cr.restore()


def scene_door(cr, t, tl):
    A = tl.at
    m5 = A("m5")
    if t < m5:
        knock = A("m4", "knocks")
        opened = ease_out(seg(t, A("m4", "check.") - 0.1, A("m4", "check.") + 0.5))
        door_scene(cr, t, opened)
        if opened > 0.3:
            person(cr, t, 460, 860, 0.8, "twain", eyes="half", mouth="smug", arms=("hips", "down"), facing=-1)
        jolt = math.sin(t * 40) * 6 if knock <= t < knock + 0.5 else 0
        person(cr, t, 170 + jolt, 900, 0.85, "reporter", eyes="open", mouth="talk" if t < A("m4", "check.") + 0.4
               else "smile", arms=("fist", "write"), look=(0.6, 0))
        if knock <= t < knock + 0.6:
            for k in range(2):
                bold_text(cr, "KNOCK", 420 + k * 40, 440 + k * 70, 44 - k * 6, GOLD)
            cue("thud", t, knock)
            cue("thud", t, knock + 0.25)
        sign(cr, t, A("m4", "New"), 360, 160, "NEW YORK REPORTER", col=hexc("#c9a46a"), size=48)
    else:
        room(cr, t)
        cr.save()
        enter(cr, camera(t, [(m5 - 0.3, (1.3, 300, 560))]))
        rrect(cr, 60, 690, 520, 30, 10)     # desk
        paint(cr, lin(0, 690, 0, 720, [(0, hexc("#b9824a")), (1, hexc("#7a4a2a"))]), OUTLINE, 6)
        person(cr, t, 300, 900, 0.9, "twain", eyes="half", mouth="smug", arms=("write", "down"), hold=quill)
        rrect(cr, 60, 700, 520, 220, 10)
        paint(cr, lin(0, 700, 0, 920, [(0, hexc("#9a6a3a")), (1, hexc("#6b4422"))]), OUTLINE, 6)
        rrect(cr, 330, 660, 130, 40, 4)
        paint(cr, PAPER, OUTLINE, 3)
        cr.restore()
        sign(cr, t, m5, 360, 150, "THE NOTE", col=GOLD, size=72)
    vignette(cr, 0.45)


def scene_note(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d9c8a8"), hexc("#fff1d6"), seed=4)
    lines = [("The report of my illness", A("m6", "report"), 0.9),
             ("grew out of his illness.", A("m6", "grew"), 0.9),
             ("The report of my death", A("m6", "report", nth=2), 0.9),
             ("was an exaggeration.", A("m6", "was"), 0.9)]
    note_card(cr, t, lines, 360, 470, 620, 44)
    if t >= A("m6", "exaggeration.") + 0.2:
        stroke_line(cr, [(130, 600), (590, 600)], 6, alpha(RED, 0.8))
    portrait(cr, t, A("m6") + 0.05, 360, 175, 95, "twain", mouth="talk" if tl.speaking("twain", t) else "smug",
             eyes="half", bg=hexc("#ffd84d"))
    bold_text(cr, "- Mark Twain, 1897", 590, 760, 32, WHITE, font="Fredoka", align="right")
    vignette(cr, 0.35)


def scene_misquote(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd6a8"), hexc("#fff1d6"), seed=6)
    for k, (st, big, sub, col, ok) in enumerate((
            (A("m7"), "WAS AN EXAGGERATION", "HIS REAL WORDS, 1897", GREEN, True),
            (A("m7", "Not"), "GREATLY EXAGGERATED", "THE FAMOUS VERSION", RED, False))):
        if t < st:
            continue
        kk = appear(t, st, 0.4)
        y = 340 + k * 260
        cr.save()
        cr.translate(360, y)
        cr.scale(kk, kk)
        soft_rrect(cr, -300, -90, 600, 190, 26, (0, 0, 0, 0.3), sigma=10)
        rrect(cr, -300, -100, 600, 190, 26)
        paint(cr, lin(0, -100, 0, 90, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
        rrect(cr, -300, -100, 600, 60, 26)
        paint(cr, col, OUTLINE, 6)
        bold_text(cr, sub, 0, -55, 30, WHITE, font="Fredoka", ow=6)
        bold_text(cr, big, 0, 40, 44, INKC, outline=None, shadow=0)
        cr.restore()
        if ok:
            check(cr, t, st + 0.3, 610, y - 100, 34)
        else:
            red_x(cr, t, st + 0.5, 610, y - 100, 34)
    sign(cr, t, A("m7", "later."), 360, 820, "CAME LATER (1912 BOOK)", col=PURPLE, size=40)
    sign(cr, t, A("m7"), 360, 150, "THE REAL LINE", col=GOLD, size=64)
    vignette(cr, 0.35)


def scene_yacht(cr, t, tl):
    A = tl.at
    m9 = A("m9")
    fogk = seg(t, A("m9", "fog."), A("m9", "fog.") + 1.2) if t >= m9 else 0.0
    sea(cr, t, "fog" if fogk > 0.5 else "day")
    if fogk > 0:
        cr.rectangle(0, 0, W, H)
        cr.set_source_rgba(0.85, 0.87, 0.9, 0.35 * fogk)
        cr.fill()
    drift = seg(t, A("m8", "sails"), A("m9", "it.", end=True) + 1)
    yacht(cr, t, lerp(250, 460, drift), 790, 0.95, twain=fogk < 0.7)
    if fogk > 0:
        fog(cr, t, 1.6 * fogk, y0=420)
        fog(cr, t + 7, 1.6 * fogk, y0=640)
    calendar(cr, t, A("m8", "1907."), 560, 330, "10 YEARS LATER", "1907", col=hexc("#3f8fc8"),
             end=A("m8", "sails") - 0.1)
    sign(cr, t, A("m8", "sails"), 360, 160, "SAILING HOME", col=BLUE, size=58, sub="FROM VIRGINIA", sub_col=WHITE,
         end=m9 - 0.05)
    sign(cr, t, A("m9", "fog."), 360, 160, "FOG...", col=hexc("#8a94a8"), size=72, end=A("m9", "Nobody") - 0.05)
    sign(cr, t, A("m9", "Nobody"), 360, 160, "NO NEWS", col=hexc("#5a6478"), size=72)
    vignette(cr, 0.45)


def scene_paper(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#5a6478"), hexc("#a8b0c0"), seed=7)
    st = A("m10") + 0.05
    u = ease_out(seg(t, st, st + 0.7))
    newspaper(cr, t, 360, 520, 1.15 * max(u, 0.01), ["TWAIN AND YACHT", "DISAPPEAR", "AT SEA"],
              date="May 4, 1907", rot=(1 - u) * 6 - 0.03, mast="The New York Times")
    if u > 0.9:
        cue("hit", t, st + 0.65)
    vignette(cr, 0.4)


def scene_home(cr, t, tl):
    A = tl.at
    room(cr, t)
    m12, m13 = A("m12"), A("m13")
    cam = camera(t, [(A("m11") - 0.3, (1.0, 360, 640)), (m12, (1.15, 330, 590)), (m13, (1.25, 340, 580))], dur=0.7)
    cr.save()
    enter(cr, cam)
    armchair(cr, 300, 900, 1.0)
    talk = tl.speaking("twain", t)
    if t < m12:
        person(cr, t, 300, 900, 0.95, "twain", eyes="happy", mouth="smile", arms=("hold", "down"), hold=teacup)
    elif t < m13:
        person(cr, t, 300, 900, 0.95, "twain", eyes="half", mouth="talk" if talk else "smug", brows="raise",
               arms=("hold", "down"), hold=magnifier)
    else:
        person(cr, t, 300, 900, 0.95, "twain", eyes="half" if (t * 0.7) % 1 > 0.15 else "happy",
               mouth="talk" if talk else "smug", brows="raise", arms=("point", "hold"), hold_back=teacup)
    armchair_front(cr, 300, 905, 1.0)
    cr.restore()
    sign(cr, t, A("m11", "safe"), 360, 150, "SAFE AT HOME", col=GREEN, size=62, sub="NEW YORK", sub_col=WHITE,
         end=m12 - 0.05)
    sign(cr, t, A("m12", "exhaustive"), 360, 150, "AN EXHAUSTIVE", col=PURPLE, size=56, sub="INVESTIGATION",
         sub_col=WHITE, end=m13 - 0.05)
    sign(cr, t, A("m13", "apprise"), 360, 150, "THE ANXIOUS", col=GOLD, size=60, sub="PUBLIC", sub_col=WHITE)
    vignette(cr, 0.45)


def scene_final(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a3a58"), hexc("#8a7a9a"), seed=9)
    calendar(cr, t, A("m14") + 0.1, 360, 330, "APRIL 21", "1910", col=hexc("#5a6478"))
    st = A("m14", "papers")
    u = ease_out(seg(t, st, st + 0.6))
    if t >= st:
        newspaper(cr, t, 360, 640, 0.6 * max(u, 0.01), ["MARK TWAIN", "DIES"], date="April 1910", rot=-0.03,
                  mast="THE EVENING PAPER")
        check(cr, t, A("m14", "right.") + 0.1, 560, 520, 44)
    soft_disc(cr, 120, 760, 90, (1, 0.8, 0.4, 0.35 + 0.05 * math.sin(t * 8)))
    rrect(cr, 100, 700, 40, 120, 6)
    paint(cr, hexc("#fff4dc"), OUTLINE, 4)
    smooth(cr, [(120, 700), (108, 676), (120, 650 + 4 * math.sin(t * 9)), (132, 676)])
    paint(cr, hexc("#ffd84d"), hexc("#ff8a3c"), 3)
    vignette(cr, 0.5)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    armchair(cr, 360, 900, 1.0)
    person(cr, t, 360, 900, 0.95, "twain", eyes="happy", mouth="grin", arms=("wave", "down"))
    armchair_front(cr, 360, 905, 1.0)
    cr.restore()
    sign(cr, t, A("m15"), 360, 150, "WHICH IS FUNNIER?", col=GOLD, size=56)
    for k, (lab, col, key) in enumerate((("1897", GREEN, "first,"), ("1907", BLUE, "second?"))):
        st = A("m15", key)
        if t < st:
            continue
        kk = appear(t, st, 0.35)
        x = 180 if k == 0 else 540
        cr.save()
        cr.translate(x, 330)
        cr.scale(kk, kk)
        soft_rrect(cr, -130, -42, 260, 92, 46, (0, 0, 0, 0.3), sigma=10)
        rrect(cr, -130, -50, 260, 92, 46)
        paint(cr, lin(0, -50, 0, 42, [(0, shade(col, 0.3)), (1, shade(col, -0.15))]), OUTLINE, 6)
        bold_text(cr, lab, 0, 14, 50, WHITE)
        cr.restore()
        cue("pop", t, st)
    vignette(cr, 0.45)


SCENES = {"hook": scene_hook, "london": scene_london, "rumor": scene_rumor, "door": scene_door, "note": scene_note,
          "misquote": scene_misquote, "yacht": scene_yacht, "paper": scene_paper, "home": scene_home,
          "final": scene_final, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
