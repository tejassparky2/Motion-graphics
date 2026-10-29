"""Explainer 4: "This Amoeba Eats Your Brain Through Your Nose" (Naegleria fowleri, Kerala 2025). Made 29 Oct 2026
under the owner's standing approval ("auto approved from next"), in the Hinglish channel's poster format and hook
rules (research_notes/from_shorts/). Script and sources: research_notes/explainer_4_amoeba.md."""
import json
import math
import os

from poster import (CORAL, framed_photo, CREAM, GOLD, GREEN, H, INK, MARGIN, RED, SLATE, W, _along, _round, calendar, card, clamp,
                    counter, cross, draw_text, ease, footnote, gauge, headline, icon_array, magnifier, path, person,
                    photo, prog, ring, stamp, strike, text_size, tick, yes_no_card, MONO_FONT, FADED)

# the narrator, music and pauses are channel-wide; render_doc reads them from this module
from channel import ASSETS_ROOT, GAP, REPO, MUSIC, NARRATOR, REVEAL_GAP, TAIL  # noqa: F401
from shots import T, asset_finder, checklist, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="Imagine you jump into a pond on a hot day. A few days later, something is eating your brain."),
    dict(id="b2", text="It got in through your nose. Then it climbed the nerve you smell with."),
    dict(id="b3", text="And by the time your head starts to hurt, it's already in your brain."),
    dict(id="b4", text="This isn't a horror movie. It's real."),
    dict(id="b5", text="It's called Naegleria fowleri. The brain-eating amoeba.", gap=REVEAL_GAP),
    dict(id="b6", text="In [twenty twenty-five,|2025,] brain infections from amoebas hit about one hundred and seventy "
                       "people in Kerala. Forty-two of them died."),
    dict(id="b7", text="So how can one tiny cell, thinner than a hair, kill a grown adult?"),
    dict(id="b8", text="It lives in warm, fresh water. Ponds, lakes, rivers, and badly kept pools."),
    dict(id="b9", text="It loves heat. Cases usually come after long, hot spells."),
    dict(id="b10", text="Drinking that water won't infect you. The danger is your nose."),
    dict(id="b11", text="When water shoots up your nose, the amoeba can travel to the very top."),
    dict(id="b12", text="There, the bone has tiny holes. Your smell nerves pass through them, into the brain."),
    dict(id="b13", text="It follows those nerves, straight into your brain. And it starts eating brain tissue."),
    dict(id="b14", text="And the scariest part? The first signs look like a normal fever.", gap=REVEAL_GAP),
    dict(id="b15", text="Headache. Fever. Vomiting."),
    dict(id="b16", text="Then a stiff neck. Confusion. Seizures. It moves very fast."),
    dict(id="b17", text="It's very rare. But nearly everyone who gets it dies."),
    dict(id="b18", text="So why did some patients in Kerala survive?", gap=REVEAL_GAP),
    dict(id="b19", text="Because doctors there started testing for it early, and treating it fast."),
    dict(id="b20", text="And it doesn't spread from person to person."),
    dict(id="b21", text="So, hold your nose, or wear a nose clip, when you jump into fresh water."),
    dict(id="b22", text="Don't stir up the mud in shallow, warm water."),
    dict(id="b23", text="If you rinse your nose, like with a neti pot, use boiled and cooled water. Never straight "
                        "from the tap."),
    dict(id="b24", text="And if you get a bad headache and fever after swimming, see a doctor right away. Tell them you "
                        "swam."),
    dict(id="b25", text="It's rare. But one splash up your nose is all it needs.", gap=REVEAL_GAP),
    dict(id="b26", text="Do you swim in ponds, rivers or lakes? Yes or no, tell me in the comments."),
]
for _b in SCRIPT:
    _b.setdefault("scene", _b["id"])
for _b in SCRIPT[1:]:
    _b.setdefault("gap", GAP)

METADATA = dict(
    title="This Amoeba Eats Your Brain Through Your Nose",
    alt_titles=["One Swim Can Let an Amoeba Into Your Brain", "The Brain-Eating Amoeba Hiding in Warm Water",
                "Why You Should Never Rinse Your Nose With Tap Water"],
    caption="One swim in a warm pond… and an amoeba can climb up your nose into your brain 😳 Kerala: ~170 cases "
            "in 2025.\n\n"
            "To stay safe:\n✅ Hold your nose or wear a nose clip when you jump into fresh water\n"
            "✅ Don't stir up mud in shallow, warm water\n"
            "✅ Rinsing your nose (jal neti)? Use boiled and cooled water\n"
            "✅ Bad headache and fever after a swim? See a doctor right away, and tell them you swam\n"
            "❌ It doesn't spread from person to person\n❌ Drinking the water doesn't infect you\n\n"
            "It's very rare, but almost always deadly.\n\n"
            "Do you swim in ponds, rivers or lakes? Comment YES or NO 👇",
    yt_title="This Amoeba Eats Your Brain Through Your Nose 😳",
    yt_description="Naegleria fowleri, the brain-eating amoeba, lives in warm fresh water. It goes up the nose, follows "
                   "the smell nerves into the brain, and destroys brain tissue. In 2025, Kerala reported about 170 "
                   "amoeba brain infections and 42 deaths. It's very rare, and early testing and fast treatment saved "
                   "some patients.\n\n"
                   "To stay safe:\n✅ Hold your nose or wear a nose clip when you jump into fresh water\n"
                   "✅ Don't stir up mud in shallow, warm water\n"
                   "✅ Rinse your nose only with boiled and cooled water\n"
                   "✅ Bad headache and fever after swimming? See a doctor right away, and tell them you swam\n"
                   "❌ It doesn't spread from person to person, and drinking the water doesn't infect you\n\n"
                   "General information, not medical advice.",
    hashtags=["#braineatingamoeba", "#naegleriafowleri", "#kerala", "#healthawareness", "#sciencefacts"],
    tags=["brain eating amoeba", "naegleria fowleri", "amoebic meningoencephalitis", "kerala amoeba", "PAM",
          "swimming safety", "jal neti", "nasal rinse", "health facts", "science explained"],
    pinned_comment="Do you swim in ponds, rivers or lakes? 🏊 YES or NO? 👇",
    sources=["CDC, Naegleria fowleri: about, causes, symptoms, prevention",
             "Government of India, Lok Sabha reply on amoebic meningoencephalitis, December 2025",
             "The Lancet, 2025, Naegleria fowleri in Kerala, India: prevention over panic"],
)

_find = asset_finder("amoeba")
KEYS = ("micrograph", "pond", "kerala_tank", "boy_jump", "kerala_map", "hair", "thermometer", "glass", "lake", "river", "pool",
        "gray_brain", "gray_nasal", "gray_olfactory", "gray_ethmoid", "neti_pot", "nose_clip", "boiling_pot", "tap",
        "hospital", "microscope", "hot_spring", "ambulance")
P = {k: _find(k) for k in KEYS}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, "amoeba", "credits.json")]

AMOEBA = (0.55, 0.30, 0.62)          # the amoeba's colour, the same in every shot (the recurring "intruder")
WATER = (0.36, 0.60, 0.68)
BRAIN = (0.86, 0.60, 0.58)
BONE = (0.90, 0.85, 0.74)
NERVE = (0.95, 0.78, 0.30)
HEAD = (490, 1160, 860)              # where the head cross-section sits in every slate shot (centre x, y, size)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


def _photo_or(cr, key, t, t0, cx, cy, frame, fallback):
    """A framed photo if the search found one, else the drawn stand-in (so a frame is never empty)."""
    if P.get(key):
        _pic(cr, key, cx, cy, 0, t, t0, frame=frame)
    else:
        fallback()


# ---------- drawn pieces ----------

def amoeba(cr, x, y, r, t, alpha=1.0, seed=0, color=AMOEBA):
    """The amoeba: a lumpy cell whose pseudopods slowly flow, with a nucleus, a nucleolus and a few vacuoles."""
    if alpha <= 0:
        return
    ph = [seed * 1.7 + k * 2.1 for k in range(4)]
    n = 60
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = (0.16 * math.sin(2 * a + ph[0] + 1.3 * t) + 0.12 * math.sin(3 * a + ph[1] - 0.9 * t)
             + 0.07 * math.sin(5 * a + ph[2] + 2.1 * t))
        pts.append((x + r * (1 + k) * math.cos(a), y + r * (1 + k) * math.sin(a)))
    cr.move_to(*pts[0])
    for i in range(n):                                     # smooth closed curve through the points
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, *p2)
    cr.close_path()
    cr.set_source_rgba(*color, 0.85 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(color[0] * 0.4, color[1] * 0.4, color[2] * 0.4, 0.95 * alpha)
    cr.set_line_width(max(2, r * 0.06))
    cr.stroke()
    nx, ny = x - r * 0.15 + r * 0.05 * math.sin(t), y - r * 0.1
    cr.set_source_rgba(0.80, 0.62, 0.85, 0.9 * alpha)
    cr.arc(nx, ny, r * 0.28, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.15, 0.08, 0.18, 0.9 * alpha)
    cr.arc(nx, ny, r * 0.11, 0, 2 * math.pi)
    cr.fill()
    for k, (dx, dy, rr) in enumerate(((0.4, 0.3, 0.12), (-0.35, 0.42, 0.09), (0.3, -0.42, 0.08))):
        cr.set_source_rgba(1, 1, 1, 0.35 * alpha)
        cr.arc(x + r * dx, y + r * dy + r * 0.04 * math.sin(t * 2 + k), r * rr, 0, 2 * math.pi)
        cr.fill()


# head cross-section (side view, facing right) in a 100-unit box, after poster.head_profile's outline
NASAL = [(47, 16), (41, 10), (35, 4), (29, -1), (23, -4)]                   # nostril -> top of the nose
NERVE_UP = [(23, -4), (20, -8), (14, -11), (6, -15)]                       # through the holes, along the bulb
INTO_BRAIN = [(6, -15), (-4, -21), (-14, -26)]


BRAIN_OUTLINE = [(26, -12), (33, -24), (30, -38), (18, -48), (0, -52), (-18, -50), (-32, -42), (-40, -28),
                 (-38, -16), (-30, -9), (-20, -8), (-12, -10), (-4, -12), (8, -10), (16, -12)]


def _smooth(cr, pts):
    """Closed smooth curve through the points (Catmull-Rom as Bezier)."""
    n = len(pts)
    cr.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, *p2)
    cr.close_path()


def head_cut(cr, cx, cy, s, t, alpha=1.0, damage=0.0, nerves=1.0, bulb_glow=0.0, pain=0.0, dark=False):
    """Side view of a head: outline, brain, the nose channel, the thin bone at its top with tiny holes, and the smell
    nerves going through them up into the brain. On paper it's line art like the reference's drawings (dark outlines,
    pink brain); dark=True is the "inside the body" look of the reference's slate shots: a flat grey silhouette.
    damage 0..1: dark-red patches spreading from the front of the brain. pain 0..1: red ache lines."""
    k = s / 100
    lw = 6 / k                                                   # a 6 px outline at any size

    def X(px, py):
        return cx + px * k, cy + py * k

    def ink(width=lw, a=1.0):
        cr.set_source_rgba(*INK, a * alpha)
        cr.set_line_width(width)
        cr.stroke()
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    cr.move_to(-30, 50)                                          # the head (poster.head_profile's outline)
    cr.curve_to(-48, 30, -52, -25, -30, -42)
    cr.curve_to(-12, -56, 26, -54, 38, -30)
    cr.curve_to(44, -18, 42, -8, 44, 0)
    cr.line_to(52, 12)
    cr.line_to(44, 16)
    cr.curve_to(46, 24, 44, 30, 38, 32)
    cr.curve_to(36, 40, 26, 42, 16, 40)
    cr.line_to(14, 52)
    if dark:
        cr.close_path()
        cr.set_source_rgba(0.40, 0.41, 0.42, alpha)
        cr.fill()
    else:
        cr.set_source_rgba(0.95, 0.92, 0.85, 0.35 * alpha)
        cr.fill_preserve()
        ink()
    soft = 0.55 if dark else 1.0
    cr.move_to(-12, -12)                                         # brainstem
    cr.curve_to(-10, 0, -8, 10, -9, 22)
    if not dark:
        cr.set_source_rgba(*INK, alpha)
        cr.set_line_width(7 + 2 * lw)
        cr.stroke_preserve()
    cr.set_source_rgba(*BRAIN, soft * alpha)
    cr.set_line_width(7)
    cr.stroke()
    _smooth(cr, BRAIN_OUTLINE)                                   # the brain
    cr.set_source_rgba(*BRAIN, soft * alpha)
    cr.fill_preserve()
    if not dark:
        ink()
    cr.save()
    _smooth(cr, BRAIN_OUTLINE)
    cr.clip()
    for i, (x0, y0) in enumerate(((-34, -30), (-20, -42), (-6, -34), (8, -44), (-24, -18), (14, -28), (-2, -20))):
        cr.move_to(x0, y0)                                       # crack-line folds, as in the reference's brain
        for j in range(1, 4):
            cr.line_to(x0 + 5 * j, y0 + (2.5 if j % 2 else -2.5) + (i % 3 - 1))
        ink(lw * 0.45, 0.55 if dark else 0.75)
    cr.restore()
    if damage > 0:                                               # eaten patches spread back from the front
        for i in range(9):
            f = clamp(damage * 9 - i)
            if f <= 0:
                continue
            px, py = 16 - 5.5 * i + 3 * math.sin(i * 2.3), -18 - 9 * math.sin(i * 1.7) * (i > 0)
            cr.set_source_rgba(0.45, 0.06, 0.08, 0.85 * alpha * f)
            cr.arc(px, py, 2.4 + 2.2 * f + (i % 3), 0, 2 * math.pi)
            cr.fill()
    cr.move_to(*NASAL[0])                                        # the nose channel
    for pt in NASAL[1:]:
        cr.line_to(*pt)
    if not dark:
        ink(5.5 + 2 * lw)
        cr.move_to(*NASAL[0])
        for pt in NASAL[1:]:
            cr.line_to(*pt)
    cr.set_source_rgba(0.62, 0.84, 0.92, (0.5 if dark else 1.0) * alpha)
    cr.set_line_width(5.5)
    cr.stroke()
    for a_, b_ in ((13, 16.5), (18, 21.5), (23, 26.5), (28, 31)):    # the thin bone at the top, with tiny holes
        cr.move_to(a_, -4.6 + (a_ - 13) * 0.05)
        cr.line_to(b_, -4.6 + (b_ - 13) * 0.05)
        if not dark:
            ink(1.6 + 2 * lw * 0.5)
            cr.move_to(a_, -4.6 + (a_ - 13) * 0.05)
            cr.line_to(b_, -4.6 + (b_ - 13) * 0.05)
        cr.set_source_rgba(*BONE, alpha)
        cr.set_line_width(1.6)
        cr.stroke()
    cr.save()                                                    # smell bulb + nerves through the holes
    cr.translate(15, -9)
    cr.rotate(-0.25)
    cr.scale(8, 2.4)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*NERVE, (0.7 + 0.3 * bulb_glow) * alpha)
    cr.fill_preserve()
    if not dark:
        ink(lw * 0.6)
    if bulb_glow > 0:
        cr.save()
        cr.translate(15, -9)
        cr.scale(13, 6)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*NERVE, 0.25 * bulb_glow * alpha)
        cr.fill()
    if nerves > 0:
        cr.set_source_rgba(*(NERVE if dark else (0.75, 0.55, 0.10)), alpha)
        cr.set_line_width(0.8)
        for hx in (17, 22, 27):
            cr.move_to(hx, -10)
            cr.line_to(hx + 0.6, -4.5)
            cr.line_to(hx + 2 * nerves, -1 + 3 * nerves)
            cr.stroke()
    cr.restore()
    if pain > 0:                                                 # ache lines around the forehead
        for i, a_ in enumerate((-2.2, -1.75, -1.3, -0.85)):
            r0 = 62 + 4 * math.sin(t * 9 + i)
            x0, y0 = X(-6 + r0 * math.cos(a_), -20 + r0 * math.sin(a_) * 0.9)
            x1, y1 = X(-6 + (r0 + 12) * math.cos(a_), -20 + (r0 + 12) * math.sin(a_) * 0.9)
            path(cr, [(x0, y0), ((x0 + x1) / 2 + 8, (y0 + y1) / 2 - 8), (x1, y1)], pain, 7, RED, 0.9 * alpha)
    return X


def nerve_route(f):
    """Point on the amoeba's way: nostril -> top of the nose -> along the smell nerve -> into the brain (f 0..1)."""
    return _along(NASAL + NERVE_UP[1:] + INTO_BRAIN[1:], f)


def sun(cr, x, y, r, t, alpha=1.0):
    cr.set_source_rgba(*GOLD, alpha)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.set_line_width(r * 0.16)
    cr.set_line_cap(1)
    for i in range(12):
        a = 2 * math.pi * i / 12 + 0.25 * t
        cr.move_to(x + 1.3 * r * math.cos(a), y + 1.3 * r * math.sin(a))
        cr.line_to(x + 1.65 * r * math.cos(a), y + 1.65 * r * math.sin(a))
    cr.stroke()


def water(cr, x, y, w, h, t, alpha=1.0, mud=0.0):
    """A pond seen from the side: water with moving ripples; mud 0..1 clouds it brown from the bottom."""
    cr.save()
    _round(cr, x, y, w, h, 40)
    cr.clip()
    cr.set_source_rgba(*WATER, 0.85 * alpha)
    cr.paint()
    cr.set_source_rgba(1, 1, 1, 0.35 * alpha)
    cr.set_line_width(5)
    for i in range(5):
        yy = y + 40 + i * (h - 60) / 5
        cr.move_to(x, yy)
        for j in range(13):
            xx = x + w * j / 12
            cr.line_to(xx, yy + 8 * math.sin(j * 1.3 + t * 2.5 + i))
        cr.stroke()
    if mud > 0:
        for i in range(14):
            bx = x + w * ((i * 0.37 + 0.1) % 1)
            rise = mud * (0.3 + 0.5 * ((i * 0.53) % 1)) * h
            cr.set_source_rgba(0.45, 0.33, 0.20, 0.55 * alpha * clamp(mud * 2))
            cr.arc(bx + 20 * math.sin(t * 2 + i), y + h - rise * 0.6, 40 + 30 * ((i * 0.71) % 1) * mud, 0, 2 * math.pi)
            cr.fill()
    cr.restore()


def thermometer(cr, x, y, h, level, alpha=1.0):
    """Drawn thermometer, bulb at the bottom (x, y); level 0..1 of the red column."""
    w = h * 0.13
    cr.set_source_rgba(0.95, 0.93, 0.88, alpha)
    _round(cr, x - w / 2, y - h, w, h, w / 2)
    cr.fill()
    cr.arc(x, y, w * 0.95, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(4)
    _round(cr, x - w / 2, y - h, w, h, w / 2)
    cr.stroke()
    cr.set_source_rgba(*RED, alpha)
    cr.arc(x, y, w * 0.7, 0, 2 * math.pi)
    cr.fill()
    top = y - (h - w) * clamp(level)
    cr.rectangle(x - w * 0.22, top, w * 0.44, y - top)
    cr.fill()
    for i in range(1, 8):
        yy = y - h * i / 8
        cr.set_source_rgba(*INK, 0.7 * alpha)
        cr.move_to(x + w / 2, yy)
        cr.line_to(x + w / 2 + 18, yy)
        cr.stroke()


def glass(cr, x, y, h, alpha=1.0):
    w0, w1 = h * 0.62, h * 0.48
    cr.move_to(x - w0 / 2, y - h)
    cr.line_to(x + w0 / 2, y - h)
    cr.line_to(x + w1 / 2, y)
    cr.line_to(x - w1 / 2, y)
    cr.close_path()
    cr.set_source_rgba(0.92, 0.95, 0.96, 0.6 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(5)
    cr.stroke()
    f = 0.3
    cr.move_to(x - (w0 - (w0 - w1) * f) / 2 + 4, y - h * (1 - f))
    cr.line_to(x + (w0 - (w0 - w1) * f) / 2 - 4, y - h * (1 - f))
    cr.line_to(x + w1 / 2 - 4, y - 4)
    cr.line_to(x - w1 / 2 + 4, y - 4)
    cr.close_path()
    cr.set_source_rgba(*WATER, 0.7 * alpha)
    cr.fill()


def tap(cr, x, y, s, t, alpha=1.0):
    """A wall tap with a drip; (x, y) = the spout's mouth."""
    cr.set_source_rgba(0.62, 0.64, 0.66, alpha)
    _round(cr, x - 3.2 * s, y - 1.6 * s, 3.4 * s, 0.7 * s, 0.3 * s)
    cr.fill()
    _round(cr, x - 0.5 * s, y - 1.6 * s, 0.7 * s, 1.6 * s, 0.3 * s)
    cr.fill()
    _round(cr, x - 2.1 * s, y - 2.5 * s, 0.6 * s, 1.0 * s, 0.2 * s)
    cr.fill()
    _round(cr, x - 2.8 * s, y - 2.7 * s, 2.0 * s, 0.35 * s, 0.15 * s)
    cr.fill()
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.rectangle(x - 3.6 * s, y - 2.0 * s, 0.5 * s, 1.5 * s)
    cr.fill()
    f = (t * 1.4) % 1
    cr.set_source_rgba(*WATER, alpha)
    cr.arc(x - 0.15 * s, y + 0.3 * s + f * 3 * s, 0.18 * s, 0, 2 * math.pi)
    cr.fill()


def pot(cr, x, y, w, t, alpha=1.0):
    """A pot of water on the boil: bubbles and steam."""
    h = w * 0.62
    cr.set_source_rgba(0.55, 0.57, 0.6, alpha)
    _round(cr, x - w / 2, y - h, w, h, w * 0.08)
    cr.fill()
    cr.rectangle(x - w * 0.62, y - h + 12, w * 1.24, 18)
    cr.fill()
    cr.set_source_rgba(*WATER, alpha)
    cr.rectangle(x - w / 2 + 10, y - h + 4, w - 20, 22)
    cr.fill()
    for i in range(7):
        f = (t * 1.5 + i / 7) % 1
        cr.set_source_rgba(1, 1, 1, 0.8 * alpha * (1 - f))
        cr.arc(x - w * 0.4 + w * 0.8 * ((i * 0.37) % 1), y - h + 14 - 20 * f, 7 + 6 * f, 0, 2 * math.pi)
        cr.fill()
    cr.set_line_width(10)
    cr.set_line_cap(1)
    for i in range(3):
        f = (t * 0.6 + i / 3) % 1
        sx = x - w * 0.25 + w * 0.25 * i
        cr.set_source_rgba(1, 1, 1, 0.55 * alpha * (1 - f))
        cr.move_to(sx, y - h - 30 - 200 * f)
        cr.curve_to(sx + 30, y - h - 80 - 200 * f, sx - 30, y - h - 130 - 200 * f, sx, y - h - 180 - 200 * f)
        cr.stroke()


def picto(cr, x, y, h, pose, color=INK, alpha=1.0, rot=0.0):
    """A pictogram person (thick round-capped limbs, round head), hips at (x, y), `h` = standing height.
    pose: angles in degrees from straight down (positive = toward the right) for "torso" (from straight up),
    "l_arm"/"r_arm" (upper, lower) and "l_leg"/"r_leg" (thigh, shin)."""
    lw = h * 0.085
    seg = h * 0.25
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(lw)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    ta = math.radians(pose.get("torso", 0))
    nx, ny = seg * 1.25 * math.sin(ta), -seg * 1.25 * math.cos(ta)       # neck
    cr.move_to(0, 0)
    cr.line_to(nx, ny)
    cr.stroke()
    cr.arc(nx + h * 0.11 * math.sin(ta), ny - h * 0.11 * math.cos(ta), h * 0.085, 0, 2 * math.pi)
    cr.fill()

    def limb(x0, y0, a1, a2, L):
        a1, a2 = math.radians(a1), math.radians(a2)
        x1, y1 = x0 + L * math.sin(a1), y0 + L * math.cos(a1)
        x2, y2 = x1 + L * math.sin(a2), y1 + L * math.cos(a2)
        cr.move_to(x0, y0)
        cr.line_to(x1, y1)
        cr.line_to(x2, y2)
        cr.stroke()
    sx, sy = nx * 0.92, ny * 0.92 + lw * 0.3                             # shoulders
    for k in ("l_arm", "r_arm"):
        a1, a2 = pose.get(k, (8 if k == "r_arm" else -8, 0))
        limb(sx, sy, a1, a2, seg * 0.92)
    for k in ("l_leg", "r_leg"):
        a1, a2 = pose.get(k, (6 if k == "r_leg" else -6, 0))
        limb(0, 0, a1, a2, seg * 1.05)
    cr.restore()


WOOD = (0.87, 0.69, 0.48)
WOOD_EDGE = (0.56, 0.38, 0.22)


def mannequin(cr, x, y, h, pose, alpha=1.0, rot=0.0, shadow=True):
    """The reference's stand-in for "you": a wooden artist's mannequin (capsule limbs, ball joints, egg head), drawn
    so it can take any pose. Same pose angles as picto(); hips at (x, y), `h` = standing height."""
    seg = h * 0.25
    lw = h * 0.075
    ta = math.radians(pose.get("torso", 0))
    nx, ny = seg * 1.25 * math.sin(ta), -seg * 1.25 * math.cos(ta)
    sx, sy = nx * 0.85, ny * 0.85

    def bone(pts, width):
        for wdt, col, a in ((width + 5, WOOD_EDGE, 1.0), (width, WOOD, 1.0), (width * 0.28, (0.96, 0.84, 0.66), 0.8)):
            cr.set_source_rgba(*col, a * alpha)
            cr.set_line_width(wdt)
            cr.move_to(*pts[0])
            for q in pts[1:]:
                cr.line_to(*q)
            cr.stroke()

    def joint(px, py, r):
        cr.set_source_rgba(*WOOD_EDGE, alpha)
        cr.arc(px, py, r, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.78, 0.58, 0.38, alpha)
        cr.arc(px - r * 0.15, py - r * 0.15, r * 0.7, 0, 2 * math.pi)
        cr.fill()

    def limb(x0, y0, a1, a2, L):
        a1, a2 = math.radians(a1), math.radians(a2)
        x1, y1 = x0 + L * math.sin(a1), y0 + L * math.cos(a1)
        x2, y2 = x1 + L * math.sin(a2), y1 + L * math.cos(a2)
        bone([(x0, y0), (x1, y1)], lw)
        bone([(x1, y1), (x2, y2)], lw * 0.85)
        joint(x1, y1, lw * 0.42)
        joint(x0, y0, lw * 0.5)
        cr.set_source_rgba(*WOOD_EDGE, alpha)                   # hand / foot
        cr.save()
        cr.translate(x2, y2)
        cr.rotate(-a2)
        cr.scale(lw * 0.45, lw * 0.75)
        cr.arc(0, 0.4, 1, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    if shadow and alpha > 0:
        cr.save()
        cr.translate(x + 14, y + 22)
        cr.rotate(rot)
        cr.set_source_rgba(0, 0, 0, 0.12 * alpha)
        cr.set_line_width(lw * 1.3)
        cr.set_line_cap(1)
        cr.move_to(0, 0)
        cr.line_to(nx, ny)
        cr.stroke()
        cr.restore()
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    px_, py_ = math.cos(ta), math.sin(ta)                      # across the body (shoulders, hips)
    so, ho = lw * 1.25, lw * 0.6
    for k in ("l_arm", "l_leg"):                                 # far limbs first
        a1, a2 = pose.get(k, (-8, 0))
        if k.endswith("arm"):
            limb(sx - px_ * so, sy - py_ * so, a1, a2, seg * 0.92)
        else:
            limb(-px_ * ho, -py_ * ho, a1, a2, seg * 1.05)
    bone([(0, 0), (nx * 0.42, ny * 0.42)], lw * 2.2)             # pelvis + chest blocks
    bone([(nx * 0.55, ny * 0.55), (nx * 0.88, ny * 0.88)], lw * 2.7)
    joint(nx * 0.47, ny * 0.47, lw * 0.55)
    bone([(nx * 0.9, ny * 0.9), (nx * 1.05, ny * 1.05)], lw * 0.6)   # neck
    hx, hy = nx * 1.0 + h * 0.10 * math.sin(ta), ny * 1.0 - h * 0.10 * math.cos(ta)
    cr.save()                                                    # egg-shaped head
    cr.translate(hx, hy)
    cr.rotate(ta)
    cr.scale(h * 0.068, h * 0.088)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*WOOD_EDGE, alpha)
    cr.set_line_width(5)
    cr.stroke_preserve()
    cr.set_source_rgba(*WOOD, alpha)
    cr.fill()
    cr.set_source_rgba(0.96, 0.84, 0.66, 0.7 * alpha)
    cr.arc(hx - h * 0.02, hy - h * 0.03, h * 0.022, 0, 2 * math.pi)
    cr.fill()
    for k in ("r_leg", "r_arm"):                                 # near limbs on top
        a1, a2 = pose.get(k, (8, 0))
        if k.endswith("arm"):
            limb(sx + px_ * so, sy + py_ * so, a1, a2, seg * 0.92)
        else:
            limb(px_ * ho, py_ * ho, a1, a2, seg * 1.05)
    cr.restore()


JUMP = dict(torso=-8, l_arm=(-150, -170), r_arm=(150, 170), l_leg=(-60, 20), r_leg=(-30, 40))   # arms up, knees up
PINCH = dict(torso=0, l_arm=(-12, -4), r_arm=(110, -102), l_leg=(-4, 0), r_leg=(6, 3))     # hand at the nose


STAND = dict(torso=0, l_arm=(-12, -4), r_arm=(12, 4), l_leg=(-4, 0), r_leg=(4, 0))


def jump_scene(cr, t, t_go, pinch=False, y=1200, h=440, alpha=1.0):
    """Side view of a pond with a grassy bank on the left: a person stands on the bank, jumps at t_go (arms up, or
    holding the nose with `pinch`), lands with a splash and sinks out of sight, leaving rings on the water."""
    x0, x1 = 90, 990
    water(cr, 300, y, x1 - 300, h, t, alpha)
    cr.set_source_rgba(0.42, 0.52, 0.30, alpha)                  # the bank
    cr.move_to(x0, y - 50)
    cr.line_to(330, y - 50)
    cr.curve_to(360, y - 30, 340, y + 40, 320, y + h)
    cr.line_to(x0, y + h)
    cr.close_path()
    cr.fill()
    cr.set_source_rgba(0.30, 0.40, 0.22, alpha)
    cr.rectangle(x0, y - 58, 250, 14)
    cr.fill()
    fig_h = 470
    q = clamp((t - t_go) / 0.85)
    land = t_go + 0.85
    sx, sy = 210, y - 50 - fig_h * 0.47                          # hips while standing on the bank
    lx, ly = 640, y - fig_h * 0.1                                # hips at the moment of landing
    if t < t_go:
        pose, fx, fy, rot = (PINCH if pinch else STAND), sx, sy, 0.0
    else:
        pose = PINCH if pinch else JUMP
        fx = sx + (lx - sx) * q
        fy = sy + (ly - sy) * q - 190 * math.sin(math.pi * q)
        fy += 420 * clamp((t - land) / 0.6) ** 1.5               # sinks after landing
        rot = 0.2 * math.sin(math.pi * q)
    cr.save()
    cr.rectangle(0, 0, W, y + 6)                                 # nothing shows under the water line
    cr.clip()
    mannequin(cr, fx, fy, fig_h, pose, alpha, rot, shadow=t < t_go)
    cr.restore()
    splash(cr, lx, y, t, land, alpha)
    for k in range(3):                                           # rings where they went in
        f = clamp((t - land - 0.2 - 0.35 * k) / 1.6)
        if 0 < f < 1:
            cr.set_source_rgba(1, 1, 1, 0.7 * (1 - f) * alpha)
            cr.set_line_width(5)
            cr.save()
            cr.translate(lx, y + 8)
            cr.scale(60 + 200 * f, 12 + 30 * f)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.stroke()


def splash(cr, x, y, t, t0, alpha=1.0):
    f = clamp((t - t0) / 0.7)
    if f <= 0 or f >= 1:
        return
    for i in range(14):
        a = math.pi + math.pi * (i + 0.5) / 14
        d = 60 + 220 * f
        cr.set_source_rgba(0.85, 0.93, 0.97, alpha * (1 - f))
        cr.arc(x + d * math.cos(a), y + d * math.sin(a) + 300 * f * f, 14 * (1 - 0.5 * f), 0, 2 * math.pi)
        cr.fill()


def nose_clip(cr, x, y, s, alpha=1.0):
    cr.set_source_rgba(0.20, 0.45, 0.80, alpha)
    cr.set_line_width(s * 0.12)
    cr.set_line_cap(1)
    cr.arc(x, y, s * 0.5, math.pi * 1.05, math.pi * 1.95)
    cr.stroke()
    for sx in (-1, 1):
        cr.set_source_rgba(0.12, 0.12, 0.14, alpha)
        _round(cr, x + sx * s * 0.5 - s * 0.14, y - s * 0.05, s * 0.28, s * 0.4, s * 0.1)
        cr.fill()


def neti(cr, x, y, s, alpha=1.0):
    """A neti pot (side view, spout to the right): rounded body, open top, long rising spout, handle at the back."""
    body = (0.30, 0.55, 0.62)
    cr.set_source_rgba(*body, alpha)
    cr.move_to(x - s, y)                                          # body
    cr.curve_to(x - s, y + s * 0.75, x + s, y + s * 0.75, x + s, y)
    cr.line_to(x + s * 0.8, y - s * 0.35)
    cr.line_to(x - s * 0.8, y - s * 0.35)
    cr.close_path()
    cr.fill()
    cr.move_to(x + s * 0.7, y + s * 0.1)                          # spout
    cr.curve_to(x + s * 1.3, y + s * 0.1, x + s * 1.5, y - s * 0.4, x + s * 1.9, y - s * 0.75)
    cr.line_to(x + s * 1.98, y - s * 0.62)
    cr.curve_to(x + s * 1.6, y - s * 0.2, x + s * 1.4, y + s * 0.35, x + s * 0.7, y + s * 0.4)
    cr.close_path()
    cr.fill()
    cr.set_line_width(s * 0.14)                                   # handle
    cr.arc(x - s * 1.05, y + s * 0.05, s * 0.32, math.pi * 0.5, math.pi * 1.5)
    cr.stroke()
    cr.set_source_rgba(0.18, 0.36, 0.42, alpha)                   # open top
    cr.save()
    cr.translate(x, y - s * 0.35)
    cr.scale(s * 0.8, s * 0.16)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.3 * alpha)                      # shine
    cr.set_line_width(s * 0.08)
    cr.arc(x - s * 0.1, y + s * 0.05, s * 0.6, math.pi * 0.85, math.pi * 1.1)
    cr.stroke()


def scene(cr, kind, x, y, w, h, t, alpha=1.0, algae=0.0):
    """A small drawn picture in a dark frame, like a print: "pond", "lake", "river" or "pool" (x, y = top left).
    algae 0..1 turns a pool's water green (badly kept)."""
    if alpha <= 0:
        return
    cr.save()
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha)
    cr.rectangle(x + 8, y + 16, w, h)
    cr.fill()
    cr.rectangle(x, y, w, h)
    cr.clip()
    cr.push_group()
    sky = (0.80, 0.88, 0.90)
    grass = (0.50, 0.62, 0.36)
    cr.set_source_rgb(*sky)
    cr.paint()
    sun(cr, x + w * 0.82, y + h * 0.16, h * 0.07, t)
    wv = lambda yy, amp=6: [(x + w * j / 16, yy + amp * math.sin(j * 1.4 + t * 2.4)) for j in range(17)]
    if kind == "pond":
        cr.set_source_rgb(*grass)
        cr.rectangle(x, y + h * 0.42, w, h)
        cr.fill()
        cr.set_source_rgb(*WATER)
        cr.save()
        cr.translate(x + w * 0.5, y + h * 0.7)
        cr.scale(w * 0.42, h * 0.2)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
        cr.set_source_rgb(0.30, 0.42, 0.22)                        # reeds
        cr.set_line_width(5)
        for i in range(9):
            rx = x + w * (0.08 + 0.1 * i) + (0 if i < 5 else w * 0.12)
            if 0.2 < (rx - x) / w < 0.8:
                continue
            cr.move_to(rx, y + h * 0.78)
            cr.line_to(rx + 6 * math.sin(t + i), y + h * 0.55)
            cr.stroke()
    elif kind == "lake":
        cr.set_source_rgb(0.42, 0.52, 0.48)                        # hills
        cr.move_to(x, y + h * 0.5)
        cr.curve_to(x + w * 0.2, y + h * 0.18, x + w * 0.4, y + h * 0.25, x + w * 0.55, y + h * 0.42)
        cr.curve_to(x + w * 0.7, y + h * 0.22, x + w * 0.9, y + h * 0.28, x + w, y + h * 0.45)
        cr.line_to(x + w, y + h)
        cr.line_to(x, y + h)
        cr.close_path()
        cr.fill()
        cr.set_source_rgb(*WATER)
        cr.rectangle(x, y + h * 0.5, w, h)
        cr.fill()
    elif kind == "river":
        cr.set_source_rgb(*grass)
        cr.rectangle(x, y + h * 0.3, w, h)
        cr.fill()
        cr.set_source_rgb(*WATER)
        cr.move_to(x + w * 0.45, y + h * 0.3)
        cr.curve_to(x + w * 0.2, y + h * 0.5, x + w * 0.8, y + h * 0.7, x + w * 0.25, y + h)
        cr.line_to(x + w * 0.75, y + h)
        cr.curve_to(x + w * 1.1, y + h * 0.7, x + w * 0.4, y + h * 0.5, x + w * 0.55, y + h * 0.3)
        cr.close_path()
        cr.fill()
    elif kind == "pool":
        cr.set_source_rgb(0.86, 0.84, 0.80)
        cr.rectangle(x, y + h * 0.3, w, h)
        cr.fill()
        g = clamp(algae)
        cr.set_source_rgb(0.30 + 0.15 * g, 0.66 - 0.06 * g, 0.80 - 0.45 * g)
        cr.rectangle(x + w * 0.08, y + h * 0.42, w * 0.84, h * 0.5)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.set_line_width(3)
        for i in range(1, 4):
            cr.move_to(x + w * 0.08, y + h * (0.42 + 0.125 * i))
            cr.line_to(x + w * 0.92, y + h * (0.42 + 0.125 * i))
            cr.stroke()
        cr.set_source_rgb(0.55, 0.57, 0.60)                         # ladder
        cr.set_line_width(5)
        for dx in (0.78, 0.86):
            cr.move_to(x + w * dx, y + h * 0.36)
            cr.line_to(x + w * dx, y + h * 0.56)
            cr.stroke()
        if g > 0:
            cr.set_source_rgba(0.30, 0.45, 0.18, 0.8 * g)          # scum and a floating leaf
            for i in range(7):
                cr.arc(x + w * (0.15 + 0.11 * i), y + h * (0.5 + 0.06 * math.sin(i * 2)), 10 + 4 * (i % 3), 0,
                       2 * math.pi)
                cr.fill()
    if kind != "pool":
        cr.set_source_rgba(1, 1, 1, 0.45)                           # ripples
        cr.set_line_width(3)
        y0 = y + h * (0.7 if kind == "pond" else 0.62)
        for k in range(2):
            pts = wv(y0 + 26 * k, 4)
            cr.move_to(*pts[0])
            for q in pts[1:]:
                cr.line_to(*q)
            cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)
    cr.reset_clip()
    cr.restore()
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.set_line_width(6)
    cr.rectangle(x, y, w, h)
    cr.stroke()


def hospital(cr, x, y, w, alpha=1.0):
    """A hospital front (x, y = bottom centre) with a red cross sign."""
    h = w * 0.62
    cr.set_source_rgba(0.93, 0.92, 0.88, alpha)
    cr.rectangle(x - w / 2, y - h, w, h)
    cr.fill()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(5)
    cr.rectangle(x - w / 2, y - h, w, h)
    cr.stroke()
    cr.set_source_rgba(0.45, 0.62, 0.72, alpha)                   # windows and door
    for r in range(2):
        for c in range(4):
            if r == 1 and c in (1, 2):
                continue
            cr.rectangle(x - w / 2 + w * (0.08 + 0.23 * c), y - h + h * (0.38 + 0.3 * r), w * 0.14, h * 0.18)
            cr.fill()
    cr.set_source_rgba(0.35, 0.40, 0.45, alpha)
    cr.rectangle(x - w * 0.09, y - h * 0.32, w * 0.18, h * 0.32)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.arc(x, y - h * 0.82, h * 0.13, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(*RED, alpha)
    a = h * 0.17
    cr.rectangle(x - a / 2, y - h * 0.82 - a * 0.18, a, a * 0.36)
    cr.fill()
    cr.rectangle(x - a * 0.18, y - h * 0.82 - a / 2, a * 0.36, a)
    cr.fill()


def microscope(cr, x, y, s, alpha=1.0):
    """A lab microscope pictogram, base centred at (x, y), about 2.2 s tall."""
    cr.set_source_rgba(*INK, alpha)
    _round(cr, x - s * 0.8, y - s * 0.18, s * 1.6, s * 0.18, s * 0.05)       # base
    cr.fill()
    cr.set_line_width(s * 0.22)
    cr.set_line_cap(1)
    cr.move_to(x - s * 0.45, y - s * 0.15)                                    # arm
    cr.curve_to(x - s * 0.75, y - s * 0.9, x - s * 0.5, y - s * 1.5, x - s * 0.05, y - s * 1.65)
    cr.stroke()
    cr.save()                                                                 # tube
    cr.translate(x + s * 0.12, y - s * 1.45)
    cr.rotate(0.45)
    _round(cr, -s * 0.13, -s * 0.75, s * 0.26, s * 1.15, s * 0.06)
    cr.restore()
    cr.fill()
    cr.rectangle(x - s * 0.15, y - s * 0.78, s * 0.85, s * 0.08)              # stage
    cr.fill()
    cr.set_source_rgba(*AMOEBA, 0.9 * alpha)                                  # slide with a sample
    cr.rectangle(x + s * 0.05, y - s * 0.86, s * 0.4, s * 0.06)
    cr.fill()


_INDIA = json.load(open(os.path.join(REPO, "assets", "maps", "india.json")))["india"]   # Natural Earth, public domain
# Kerala, traced by hand from its lon/lat outline (coast and the border with Karnataka and Tamil Nadu)
_KERALA = [(74.87, 12.78), (75.15, 12.66), (75.50, 12.33), (75.85, 11.97), (76.10, 11.85), (76.42, 11.66),
           (76.40, 11.35), (76.60, 11.05), (76.88, 10.85), (76.82, 10.35), (77.20, 10.10), (77.25, 9.62),
           (77.18, 9.20), (77.17, 8.75), (77.17, 8.29), (76.95, 8.42), (76.55, 8.90), (76.30, 9.50), (76.20, 10.00),
           (76.00, 10.60), (75.80, 11.20), (75.55, 11.75), (75.30, 12.10), (75.00, 12.50)]


def kerala(cr, x, y, h, alpha=1.0, color=INK, lit=1.0):
    """India's outline (Natural Earth) centred at (x, y), `h` px tall, with Kerala filled red (lit 0..1).
    Returns Kerala's centre."""
    lat0, lat1, lon0, lon1 = 6.5, 37.2, 68.0, 97.5
    k = h / (lat1 - lat0)
    kx = k * math.cos(math.radians(22))

    def P(lon, lat):
        return x + (lon - (lon0 + lon1) / 2) * kx, y - (lat - (lat0 + lat1) / 2) * k

    def poly(pts):
        cr.move_to(*P(*pts[0]))
        for q in pts[1:]:
            cr.line_to(*P(*q))
        cr.close_path()
    for ring_ in _INDIA:
        poly(ring_)
    cr.set_source_rgba(0.93, 0.89, 0.80, 0.95 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(4)
    cr.stroke()
    poly(_KERALA)
    cr.set_source_rgba(*RED, alpha * lit)
    cr.fill()
    return P(76.4, 10.4)


def why(cr, t, t0, x, y, size=260):
    q = prog(t, t0, 0.3)
    draw_text(cr, "?", x, y, int(size * (0.8 + 0.2 * q)), RED, q, anchor="cm")


# ---------- shots ----------
# Rules (Hinglish channel style bible + parasite-reels study): a new picture every ~3 s cut on the spoken word, the
# literal noun on screen, red = threat, green = what to do, gold = numbers, dark slate for inside the body. The
# amoeba is the one recurring character: the same purple cell every time it appears.

def pond_bg(cr, t, t0, x=110, y=900, w=860, h=560):
    _photo_or(cr, "pond", t, t0, x + w / 2, y + h / 2, (w, h), lambda: water(cr, x, y, w, h, t))


def h_jump(cr, t, tl, t0):                               # b1 frame 0: "imagine you jump into a pond on a hot day"
    sun(cr, 860, 700, 70, t)
    jump_scene(cr, t, max(0.15, T(tl, "b1", "jump") - 0.1))
    headline(cr, t, "SOMETHING EATS YOUR", "BRAIN", -1, 1.2, t_ghost=-1)


def h_days(cr, t, tl, t0):                               # b1 "a few days later..."
    _photo_or(cr, "pond", t, -1, W / 2, 1440, (860, 420), lambda: scene(cr, "pond", 110, 1230, 860, 420, t))
    calendar(cr, t, t0 + 0.15, W / 2, 880, ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"], "AFTER THE SWIM",
             interval=0.3, circle_last=False)
    headline(cr, t, "A FEW DAYS", "LATER", t0, t0 + 0.2)


def h_eating(cr, t, tl, t0):                             # b1 "...something is eating your brain" (slate)
    te = T(tl, "b1", "eating")
    head_cut(cr, *HEAD, t, damage=clamp((t - te) / 2.0))
    for i in range(3):
        f = clamp((t - te + 0.3) / 1.5)
        amoeba(cr, 600 - 110 * i, 900 + 40 * math.sin(i * 2), 34, t + i, prog(t, te - 0.3 + 0.15 * i, 0.3), seed=i)
    headline(cr, t, "SOMETHING IS EATING", "YOUR BRAIN", t0, T(tl, "b1", "brain"))


def h_nose(cr, t, tl, t0):                               # b2 "it got in through your nose" (slate)
    X = head_cut(cr, *HEAD, t, dark=True)
    f = clamp((t - t0) / 2.2) * 0.32
    x, y = X(*nerve_route(f))
    amoeba(cr, x, y, 30, t, prog(t, t0, 0.3))
    ring(cr, *X(47, 13), 95, 85, prog(t, T(tl, "b2", "nose"), 0.4), color=CORAL)
    headline(cr, t, "IT GOT IN THROUGH YOUR", "NOSE", t0, T(tl, "b2", "nose"), small_color=CREAM, big_color=CORAL)


def h_climb(cr, t, tl, t0):                              # b2 "then it climbed the nerve you smell with"
    tc = T(tl, "b2", "smell")
    X = head_cut(cr, *HEAD, t, dark=True, bulb_glow=prog(t, tc, 0.3))
    f = 0.32 + clamp((t - t0) / 2.2) * 0.4
    amoeba(cr, *X(*nerve_route(f)), 30, t)
    card(cr, t, tc, 640, 1560, ["SMELL NERVE"], size=44, pin_line=X(16, -9))
    headline(cr, t, "UP THE NERVE YOU", "SMELL WITH", t0, tc, small_color=CREAM, big_color=CORAL)


def h_hurt(cr, t, tl, t0):                               # b3 "by the time your head starts to hurt, it's in your brain"
    th = T(tl, "b3", "hurt")
    ti = T(tl, "b3", "already")
    X = head_cut(cr, *HEAD, t, pain=prog(t, th, 0.4), damage=0.35 * prog(t, ti, 1.2))
    amoeba(cr, *X(*nerve_route(0.75 + 0.25 * prog(t, t0, 2.5))), 30, t)
    stamp(cr, t, "ALREADY INSIDE", ti, 540, 1640, 64, color=RED)
    headline(cr, t, "WHEN IT STARTS TO", "HURT", t0, th)


def h_movie(cr, t, tl, t0):                              # b4 "this isn't a horror movie. It's real."
    tr = T(tl, "b4", "real")
    card(cr, t, t0 + 0.1, 170, 820, ["HORROR MOVIE", "FICTION"], size=78, rot=-0.04)
    tw, _ = text_size("HORROR MOVIE", 78)
    strike(cr, 180, 900, 260 + tw, 880, prog(t, t0 + 0.6, 0.35))
    stamp(cr, t, "IT'S REAL", tr, 560, 1250, 120, rot=-0.1)
    headline(cr, t, "THIS ISN'T A", "MOVIE", t0, t0 + 0.3, strike_at=t0 + 0.6, struck=True)


def n_name(cr, t, tl, t0):                               # b5 "it's called Naegleria fowleri. The brain-eating amoeba."
    if P["micrograph"]:
        _pic(cr, "micrograph", W / 2, 880, 0, t, t0, frame=(820, 560))
    else:
        amoeba(cr, W / 2, 860, 200, t)
    tn = T(tl, "b5", "called")
    for i, (txt, ty, sz, cue) in enumerate((("NAEGLERIA FOWLERI", 1230, 92, tn),
                                            ("THE BRAIN-EATING AMOEBA", 1370, 60, T(tl, "b5", "brain")))):
        p = prog(t, cue, 0.3)
        if p > 0:
            tw_, th = text_size(txt, sz)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, sz, CREAM, clamp(p * 2 - 1))
    if P["micrograph"]:                                  # the reference labels real photos: "TISSUE CYST / REAL · USDA"
        card(cr, t, t0 + 0.3, 620, 1120 - 470, ["IN BRAIN TISSUE", "REAL · CDC"], size=34, rot=0.03)
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def n_kerala(cr, t, tl, t0):                             # b6 "in 2025, amoeba brain infections hit ~170 in Kerala"
    tk = T(tl, "b6", "Kerala")
    kx, ky = kerala(cr, 350, 1100, 680, prog(t, t0, 0.3), lit=prog(t, t0 + 0.4, 0.4))
    ring(cr, kx, ky, 55, 75, prog(t, tk + 0.2, 0.4))
    t170 = T(tl, "b6", "hundred")
    counter(cr, t, t170 - 0.3, 850, 940, "170", 140, color=GOLD)
    draw_text(cr, "CASES", 850, 1040, 54, INK, prog(t, t170, 0.3), anchor="ct")
    card(cr, t, t0 + 0.2, 640, 1250, ["KERALA, 2025", "AMOEBA BRAIN", "INFECTIONS"], size=40)
    headline(cr, t, "KERALA, 2025:", "170 CASES", t0, t170)


def n_died(cr, t, tl, t0):                               # b6 "...forty-two of them died"
    icon_array(cr, t, t0 - 0.2, 170, 17, 120, 640, 40, red=range(42), red_at=t0 + 0.4, step=0.004)
    counter(cr, t, t0 + 0.3, W / 2, 1480, "42", 170, color=RED)
    draw_text(cr, "DIED", W / 2, 1600, 60, RED, prog(t, t0 + 0.6, 0.3), anchor="ct")
    footnote(cr, "Govt of India, Lok Sabha reply, Dec 2025", prog(t, t0, 0.3), y=1700)
    headline(cr, t, "AND", "42 DIED", t0, t0 + 0.3)


def s_hair(cr, t, tl, t0):                               # b7 "one tiny cell, thinner than a hair"
    def inner(c):
        c.set_source_rgba(0.35, 0.22, 0.12, 1)                            # one hair, magnified
        c.rectangle(240, 960, 600, 150)
        c.fill()
        c.set_source_rgba(0.5, 0.33, 0.2, 1)
        for i in range(8):
            c.move_to(260 + 75 * i, 960)
            c.line_to(300 + 75 * i, 1110)
            c.set_line_width(4)
            c.stroke()
        amoeba(c, 540, 1240, 26, t)
    magnifier(cr, t, t0 + 0.1, 540, 1100, 360, inner)
    card(cr, t, T(tl, "b7", "hair"), 600, 1520, ["ONE HAIR", "vs ONE AMOEBA"], size=40)
    headline(cr, t, "THINNER THAN A", "HAIR", t0, T(tl, "b7", "hair"))


def s_kill(cr, t, tl, t0):                               # b7 "...kill a grown adult?"
    mannequin(cr, 380, 1180, 900, STAND, prog(t, t0, 0.3))
    amoeba(cr, 800, 1450, 18, t, prog(t, t0 + 0.2, 0.3))
    path(cr, [(780, 1420), (470, 1000)], prog(t, t0 + 0.4, 0.5), 4, RED, 0.8, dash=[10, 10], arrow=True)
    why(cr, t, T(tl, "b7", "adult"), 820, 950)
    headline(cr, t, "HOW CAN IT KILL", "AN ADULT?", t0, T(tl, "b7", "kill"), t_ghost=t0)


def w_warm(cr, t, tl, t0):                               # b8 "it lives in warm, fresh water"
    _photo_or(cr, "pond", t, t0, W / 2, 1140, (860, 640), lambda: water(cr, 110, 820, 860, 640, t))
    thermometer(cr, 860, 1340, 460, 0.3 + 0.45 * prog(t, T(tl, "b8", "warm"), 0.8))
    for i in range(3):
        amoeba(cr, 300 + 160 * i, 1200 + 60 * math.sin(i), 22, t + i, prog(t, t0 + 0.3 + 0.2 * i, 0.3), seed=i)
    headline(cr, t, "IT LIVES IN WARM", "FRESH WATER", t0, T(tl, "b8", "fresh"))


def w_where(cr, t, tl, t0):                              # b8 "ponds, lakes, rivers, and badly kept pools"
    items = (("pond", "Ponds", "PONDS"), ("lake", "lakes", "LAKES"), ("river", "rivers", "RIVERS"),
             ("pool", "pools", "BADLY KEPT POOLS"))
    for i, (key, cue, label) in enumerate(items):
        tc = T(tl, "b8", cue) - 0.2
        cx, cy = 290 + 500 * (i % 2), 760 + 520 * (i // 2)
        if t >= tc:
            scene(cr, key, cx - 220, cy - 165 + 40 * (1 - prog(t, tc, 0.3)), 440, 330, t + i, prog(t, tc, 0.3),
                  algae=1.0)
        draw_text(cr, label, cx, cy + 190, 40, INK, prog(t, tc, 0.3), anchor="ct")
    headline(cr, t, "PONDS, LAKES,", "RIVERS, POOLS", t0, T(tl, "b8", "pools"), big_size=130)


def w_heat(cr, t, tl, t0):                               # b9 "it loves heat. Cases usually come after long hot spells"
    sun(cr, 300, 820, 120, t)
    gauge(cr, t, t0 + 0.3, 760, 900, 190, 0.2, 0.92, labels=("COOL", "HOT"))
    tc = T(tl, "b9", "long")
    calendar(cr, t, tc - 0.1, W / 2, 1360, ["WEEK 1", "WEEK 2", "WEEK 3"], "HOT SPELL", interval=0.3, w=360, h=300,
             circle_last=False)
    headline(cr, t, "IT LOVES", "HEAT", t0, T(tl, "b9", "heat"))


def w_drink(cr, t, tl, t0):                              # b10 "drinking that water won't infect you"
    _photo_or(cr, "glass", t, t0, 380, 1080, (440, 560), lambda: glass(cr, 380, 1320, 480, prog(t, t0, 0.3)))
    tick(cr, 740, 1000, 170, prog(t, T(tl, "b10", "infect"), 0.4), color=GREEN)
    card(cr, t, T(tl, "b10", "infect"), 600, 1260, ["SWALLOWED:", "DOESN'T INFECT"], size=42)
    headline(cr, t, "DRINKING IT", "WON'T INFECT YOU", t0, T(tl, "b10", "infect"), big_color=GREEN, big_size=120)


def w_danger(cr, t, tl, t0):                             # b10 "...the danger is your nose" (Gray's nasal cavity)
    tn = T(tl, "b10", "nose")
    if P["gray_nasal"]:
        _pic(cr, "gray_nasal", W / 2, 1000, 0, t, t0, frame=(860, 830))
        ring(cr, W / 2 - 430 + 0.11 * 860, 1000 - 415 + 0.56 * 830, 90, 80, prog(t, tn, 0.4), width=12)
        stamp(cr, t, "WAY IN", tn + 0.2, 300, 1520, 60)
        headline(cr, t, "THE DANGER IS YOUR", "NOSE", t0, tn)
        return
    X = head_cut(cr, *HEAD, t)
    ring(cr, *X(47, 13), 95, 85, prog(t, tn, 0.4), width=12, color=CORAL)
    headline(cr, t, "THE DANGER IS YOUR", "NOSE", t0, tn, small_color=CREAM, big_color=CORAL)


def m_shoot(cr, t, tl, t0):                              # b11 "water shoots up your nose, the amoeba travels to the top"
    X = head_cut(cr, *HEAD, t)
    p = prog(t, t0 + 0.1, 0.9)
    path(cr, [X(60, 30), X(*NASAL[0]), X(*NASAL[2]), X(*NASAL[-1])], p, 22, (0.30, 0.62, 0.78), 0.9, arrow=True)
    ttop = T(tl, "b11", "top")
    f = 0.05 + 0.25 * clamp((t - t0 - 0.6) / max(0.5, ttop - t0 - 0.4))
    amoeba(cr, *X(*nerve_route(f)), 30, t, prog(t, t0 + 0.6, 0.3))
    headline(cr, t, "WATER UP YOUR NOSE,", "TO THE TOP", t0, ttop)


def plate_closeup(c, cx, cy, r, t, nerves=1.0, bug=0.0):
    """Inside the magnifier: the thin bone (a band with a row of holes), smell nerves threading up through the
    holes, nose lining below. bug 0..1: the amoeba climbs up through the middle hole."""
    c.set_source_rgba(0.55, 0.78, 0.86, 0.5)                    # the nose space below
    c.rectangle(cx - r, cy, 2 * r, r)
    c.fill()
    c.set_source_rgba(*BRAIN, 0.9)                              # the brain above
    c.rectangle(cx - r, cy - r, 2 * r, r - 70)
    c.fill()
    c.set_source_rgba(*BONE, 1)
    c.rectangle(cx - r, cy - 70, 2 * r, 90)
    c.fill()
    for i in range(-3, 4):
        hx = cx + i * 78
        c.set_source_rgba(0.22, 0.20, 0.20, 1)
        c.rectangle(hx - 15, cy - 70, 30, 90)
        c.fill()
        if nerves > 0:
            c.set_source_rgba(*NERVE, 1)
            c.set_line_width(9)
            c.set_line_cap(1)
            c.move_to(hx + 10 * math.sin(i), cy + r)
            c.curve_to(hx - 10, cy + 60, hx + 8, cy - 30, hx, cy - 70 - 60 * nerves)
            c.stroke()
    if bug > 0:
        amoeba(c, cx, cy + 160 - 300 * clamp(bug), 34, t)


def zoom_photo(c, key, lx, ly, u, v, w, h):
    """Inside a magnifier at (lx, ly): the photo drawn at w x h with its point (u, v) (fractions) at the lens centre."""
    framed_photo(c, P[key], lx - (u - 0.5) * w, ly - (v - 0.5) * h, w, h)


def m_there(cr, t, tl, t0):                              # b12 "there, ..." (slate): the top of the nose
    X = head_cut(cr, *HEAD, t)
    lx, ly = X(22, -5)
    ring(cr, lx, ly, 80, 46, prog(t, t0, 0.4), width=8, color=RED)
    amoeba(cr, *X(*nerve_route(0.3)), 30, t)
    headline(cr, t, "AT THE TOP OF", "YOUR NOSE", t0, t0 + 0.2)


def m_holes(cr, t, tl, t0):                              # b12 "...the bone has tiny holes" (Gray's ethmoid bone)
    th = T(tl, "b12", "holes")
    if P["gray_ethmoid"]:
        _pic(cr, "gray_ethmoid", W / 2, 900, 0, t, t0, frame=(760, 656))
        magnifier(cr, t, th - 0.2, 760, 1350, 230,
                  lambda c: zoom_photo(c, "gray_ethmoid", 760, 1350, 0.47, 0.5, 1900, 1640))
        path(cr, [(W / 2 - 25, 900), (640, 1180)], prog(t, th - 0.2, 0.3), 3, INK, 0.7)
    else:
        magnifier(cr, t, th - 0.2, 760, 1350, 230, lambda c: plate_closeup(c, 760, 1350, 230, t, nerves=0.0))
    stamp(cr, t, "TINY HOLES", th, 300, 1560, 58)
    headline(cr, t, "THE BONE HAS", "TINY HOLES", t0, th)


def m_nerves(cr, t, tl, t0):                             # b12 "your smell nerves pass through them, into the brain"
    ts = T(tl, "b12", "smell")
    if P["gray_olfactory"]:
        _pic(cr, "gray_olfactory", W / 2, 960, 0, t, t0, frame=(860, 620))
        card(cr, t, ts, 120, 1340, ["SMELL NERVES", "NOSE > BONE > BRAIN"], size=44)
        headline(cr, t, "SMELL NERVES GO", "STRAIGHT UP", t0, T(tl, "b12", "brain"))
        return
    X = head_cut(cr, *HEAD, t, bulb_glow=prog(t, ts, 0.4))
    lx, ly = X(22, -5)
    path(cr, [(lx, ly), (760, 1400)], 1.0, 3, CREAM, 0.7)
    magnifier(cr, t, -1, 760, 1400, 230, lambda c: plate_closeup(c, 760, 1400, 230, t, nerves=prog(t, ts, 0.6)),
              dark=True)
    headline(cr, t, "SMELL NERVES GO", "INTO THE BRAIN", t0, T(tl, "b12", "brain"), small_color=CREAM,
             big_color=CORAL, big_size=130)


def m_follow(cr, t, tl, t0):                             # b13 "it follows those nerves, straight into your brain"
    X = head_cut(cr, *HEAD, t, dark=True, bulb_glow=1.0)
    tb = T(tl, "b13", "brain")
    f = 0.42 + 0.58 * clamp((t - t0) / max(0.6, tb - t0 + 0.3))
    for i in range(3):
        amoeba(cr, *X(*nerve_route(max(0.0, f - 0.12 * i))), 28, t + i, prog(t, t0 + 0.2 * i, 0.3), seed=i)
    magnifier(cr, t, -1, 760, 1400, 230, lambda c: plate_closeup(c, 760, 1400, 230, t, bug=prog(t, t0, 1.6)),
              dark=True)
    headline(cr, t, "IT FOLLOWS THE", "NERVES", t0, T(tl, "b13", "nerves"), small_color=CREAM, big_color=CORAL)


def m_eat(cr, t, tl, t0):                                # b13 "...and it starts eating brain tissue"
    if P["gray_brain"]:
        _pic(cr, "gray_brain", W / 2, 1000, 0, t, t0, frame=(860, 640))
        card(cr, t, t0 + 0.4, 600, 1350, ["HUMAN BRAIN", "GRAY'S ANATOMY, 1918"], size=34)
        rng = [(0.12, 0.2), (-0.2, 0.05), (0.25, -0.15), (-0.05, -0.25), (0.3, 0.25), (-0.3, -0.1), (0.0, 0.1)]
        for i, (dx, dy) in enumerate(rng):
            f = prog(t, t0 + 0.3 + 0.25 * i, 0.5)
            if f > 0:
                cr.set_source_rgba(0.45, 0.05, 0.07, 0.7 * f)
                cr.arc(W / 2 + dx * 860, 1000 + dy * 640, 30 + 40 * f, 0, 2 * math.pi)
                cr.fill()
        for i in range(4):
            amoeba(cr, W / 2 + (rng[i][0] * 860), 1000 + rng[i][1] * 640, 34, t + i, prog(t, t0 + 0.2 * i, 0.3),
                   seed=i)
    else:
        head_cut(cr, *HEAD, t, damage=prog(t, t0, 2.5))
    headline(cr, t, "AND IT STARTS", "EATING", t0, T(tl, "b13", "eating"), big_color=CORAL)


def r_scary(cr, t, tl, t0):                              # b14 re-hook: "and the scariest part?"
    amoeba(cr, W / 2, 1080, 220, t, prog(t, t0, 0.4))
    why(cr, t, t0 + 0.3, W / 2, 1080, 300)
    headline(cr, t, "THE SCARIEST", "PART?", t0, T(tl, "b14", "part"), t_ghost=t0)


def r_fever(cr, t, tl, t0):                              # b14 "...the first signs look like a normal fever"
    _photo_or(cr, "thermometer", t, t0, 380, 1060, (460, 560),
              lambda: thermometer(cr, 380, 1320, 560, 0.3 + 0.5 * prog(t, t0 + 0.2, 1.0), prog(t, t0, 0.3)))
    card(cr, t, T(tl, "b14", "normal"), 560, 900, ["\"IT'S JUST", "A FEVER\""], size=52)
    headline(cr, t, "IT LOOKS LIKE A", "NORMAL FEVER", t0, T(tl, "b14", "fever"))


SIGNS = (("b15", "Headache", "HEADACHE"), ("b15", "Fever", "FEVER"), ("b15", "Vomiting", "VOMITING"),
         ("b16", "stiff", "STIFF NECK"), ("b16", "Confusion", "CONFUSION"), ("b16", "Seizures", "SEIZURES"))


def r_signs(cr, t, tl, t0):                              # b15 "headache. Fever. Vomiting."
    checklist(cr, t, 110, 640, 860, "FIRST SIGNS",
              [(lbl, T(tl, b, cue) - 0.15, "tick", T(tl, b, cue)) for b, cue, lbl in SIGNS[:3]])
    headline(cr, t, "THE FIRST", "SIGNS", t0, t0 + 0.3)


def r_worse(cr, t, tl, t0):                              # b16 "then a stiff neck. Confusion. Seizures."
    checklist(cr, t, 110, 640, 860, "THEN",
              [(lbl, T(tl, b, cue) - 0.15, "cross", T(tl, b, cue)) for b, cue, lbl in SIGNS[3:]])
    headline(cr, t, "THEN IT GETS", "WORSE", t0, T(tl, "b16", "stiff"), big_color=RED)


def r_fast(cr, t, tl, t0):                               # b16 "...it moves very fast"
    calendar(cr, t, t0 + 0.1, W / 2, 1050, ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"], "AFTER SYMPTOMS",
             interval=0.22)
    footnote(cr, "CDC: death usually within about 5 days of symptoms", prog(t, t0, 0.3), y=1500)
    headline(cr, t, "IT MOVES", "FAST", t0, T(tl, "b16", "fast"))


def r_rare(cr, t, tl, t0):                               # b17 "it's very rare. But nearly everyone who gets it dies."
    tn = T(tl, "b17", "nearly")
    if t < tn - 0.15:
        gauge(cr, t, t0 + 0.1, W / 2, 1150, 260, 0.6, 0.06, labels=("RARE", "COMMON"))
        stamp(cr, t, "VERY RARE", T(tl, "b17", "rare"), W / 2, 1400, 80, color=GREEN)
        headline(cr, t, "IT'S VERY", "RARE", t0, T(tl, "b17", "rare"), big_color=GREEN)
        return
    icon_array(cr, t, tn - 0.15, 100, 10, 170, 700, 52, red=range(97), red_at=T(tl, "b17", "dies"), step=0.006)
    footnote(cr, "CDC: over 97% of known US cases died (1962-2024)", prog(t, tn, 0.3), y=1640)
    headline(cr, t, "BUT 97 IN 100", "DIE", tn - 0.15, T(tl, "b17", "dies"))


def k_why(cr, t, tl, t0):                                # b18 re-hook: "so why did some patients in Kerala survive?"
    if P["kerala_tank"]:
        _pic(cr, "kerala_tank", W / 2, 1020, 0, t, t0, frame=(860, 645))
        card(cr, t, t0 + 0.3, 110, 1420, ["KERALA"], size=56)
        why(cr, t, t0 + 0.4, 820, 1450, 300)
    else:
        kx, ky = kerala(cr, 350, 1100, 680)
        ring(cr, kx, ky, 55, 75, 1.0)
        why(cr, t, t0 + 0.3, 800, 1060, 320)
    headline(cr, t, "SO WHY DID SOME", "SURVIVE?", t0, T(tl, "b18", "survive"), t_ghost=t0, big_color=GREEN)


def k_test(cr, t, tl, t0):                               # b19 "doctors there started testing for it early..."
    _photo_or(cr, "microscope", t, t0, 330, 1000, (500, 600), lambda: microscope(cr, 330, 1180, 230, prog(t, t0, 0.3)))
    tt = T(tl, "b19", "treating")
    _photo_or(cr, "hospital", t, tt - 0.2, 720, 1400, (520, 380),
              lambda: hospital(cr, 720, 1560, 480, prog(t, tt - 0.2, 0.3)))
    tick(cr, 700, 860, 150, prog(t, T(tl, "b19", "early"), 0.4), color=GREEN)
    draw_text(cr, "TEST EARLY", 640, 1000, 56, GREEN, prog(t, T(tl, "b19", "early"), 0.3), anchor="lm")
    small, big, tb = ("THEY TESTED", "EARLY", T(tl, "b19", "testing")) if t < tt - 0.1 else ("AND TREATED", "FAST", tt)
    headline(cr, t, small, big, t0 if big == "EARLY" else tt - 0.1, tb, big_color=GREEN)


def k_spread(cr, t, tl, t0):                             # b20 "and it doesn't spread from person to person"
    mannequin(cr, 260, 1150, 560, STAND, prog(t, t0, 0.3))
    mannequin(cr, 820, 1150, 560, STAND, prog(t, t0 + 0.1, 0.3))
    path(cr, [(400, 1100), (680, 1100)], prog(t, t0 + 0.3, 0.4), 10, INK, 0.8, arrow=True)
    cross(cr, 540, 1100, 160, prog(t, T(tl, "b20", "person"), 0.3))
    stamp(cr, t, "MYTH", T(tl, "b20", "spread"), 540, 1580, 80)
    headline(cr, t, "IT DOESN'T", "SPREAD", t0, T(tl, "b20", "spread"), big_color=GREEN)


def d_hold(cr, t, tl, t0):                               # b21 "hold your nose, or wear a nose clip"
    tj = T(tl, "b21", "jump")
    jump_scene(cr, t, tj - 0.1, pinch=True, y=1180, h=420)
    tc = T(tl, "b21", "clip")
    if P["nose_clip"]:
        _pic(cr, "nose_clip", 780, 820, 260, t, tc - 0.2)
    elif t >= tc - 0.2:
        nose_clip(cr, 780, 820, 200, prog(t, tc - 0.2, 0.3))
    tick(cr, 900, 700, 110, prog(t, tc + 0.2, 0.3), color=GREEN)
    headline(cr, t, "IN FRESH WATER:", "HOLD YOUR NOSE", t0, T(tl, "b21", "hold"), big_color=GREEN, big_size=130)


def d_mud(cr, t, tl, t0):                                # b22 "don't stir up the mud in shallow, warm water"
    water(cr, 110, 820, 860, 640, t, mud=prog(t, t0 + 0.2, 1.4))
    cross(cr, 540, 1140, 260, prog(t, T(tl, "b22", "mud"), 0.4))
    headline(cr, t, "DON'T STIR UP", "THE MUD", t0, T(tl, "b22", "mud"), big_color=GREEN)


def d_neti(cr, t, tl, t0):                               # b23 "rinse your nose (jal neti): boiled and cooled water"
    if P["neti_pot"]:
        _pic(cr, "neti_pot", 330, 1000, 380, t, t0)
    else:
        neti(cr, 300, 1000, 130, prog(t, t0, 0.3))
    tb = T(tl, "b23", "boiled")
    if P["boiling_pot"]:
        _pic(cr, "boiling_pot", 760, 1240, 400, t, tb - 0.2)
    elif t >= tb - 0.2:
        pot(cr, 760, 1420, 380, t, prog(t, tb - 0.2, 0.3))
    tick(cr, 760, 820, 140, prog(t, T(tl, "b23", "cooled"), 0.4), color=GREEN)
    card(cr, t, T(tl, "b23", "neti"), 110, 1300, ["NETI POT", "JAL NETI"], size=44)
    small, big = ("RINSING YOUR", "NOSE?") if t < tb - 0.2 else ("USE BOILED,", "COOLED WATER")
    headline(cr, t, small, big, t0 if big == "NOSE?" else tb - 0.2, T(tl, "b23", "rinse") if big == "NOSE?" else tb,
             big_color=GREEN, big_size=130)


def d_tap(cr, t, tl, t0):                                # b23 "...never straight from the tap"
    if P["tap"]:
        _pic(cr, "tap", W / 2, 1050, 520, t, t0)
    else:
        tap(cr, 640, 1000, 110, t, prog(t, t0, 0.3))
    cross(cr, W / 2, 1100, 300, prog(t, T(tl, "b23", "tap"), 0.4))
    headline(cr, t, "NEVER STRAIGHT", "FROM THE TAP", t0, T(tl, "b23", "tap"), big_size=130)


def d_doctor(cr, t, tl, t0):                             # b24 "bad headache and fever after swimming: see a doctor right away"
    _photo_or(cr, "pond", t, t0, W / 2, 680, (700, 300), lambda: scene(cr, "pond", 190, 530, 700, 300, t))
    checklist(cr, t, 110, 880, 860, "AFTER A SWIM", [("BAD HEADACHE", T(tl, "b24", "headache") - 0.15, "tick",
                                                       T(tl, "b24", "headache")),
                                                      ("FEVER", T(tl, "b24", "fever") - 0.15, "tick",
                                                       T(tl, "b24", "fever"))])
    td = T(tl, "b24", "doctor")
    _photo_or(cr, "hospital", t, td - 0.2, W / 2, 1320, (760, 380),
              lambda: hospital(cr, W / 2, 1560, 560, prog(t, td - 0.2, 0.3)))
    headline(cr, t, "AFTER A SWIM?", "SEE A DOCTOR", t0, td, big_color=GREEN, big_size=130)


def d_tell(cr, t, tl, t0):                               # b24 "...tell them you swam"
    _photo_or(cr, "hospital", t, -1, W / 2, 1320, (760, 380), lambda: hospital(cr, W / 2, 1560, 560))
    card(cr, t, t0 + 0.1, 170, 760, ["\"DOCTOR, I SWAM", "IN A POND 3 DAYS AGO\""], size=48, rot=0.02)
    tick(cr, 840, 1000, 120, prog(t, T(tl, "b24", "swam"), 0.4), color=GREEN)
    headline(cr, t, "TELL THEM", "YOU SWAM", t0, T(tl, "b24", "swam"), big_color=GREEN)


def e_bookend(cr, t, tl, t0):                            # b25 "it's rare. But one splash up your nose is all it needs."
    X = head_cut(cr, *HEAD, t)
    ts = T(tl, "b25", "splash")
    path(cr, [X(60, 30), X(*NASAL[0]), X(*NASAL[2])], prog(t, ts, 0.5), 22, (0.30, 0.62, 0.78), 0.9, arrow=True)
    amoeba(cr, *X(*nerve_route(0.1 + 0.15 * prog(t, ts + 0.3, 1.0))), 30, t, prog(t, ts + 0.3, 0.3))
    headline(cr, t, "ONE SPLASH IS", "ALL IT NEEDS", t0, T(tl, "b25", "needs"), t_ghost=t0, big_size=130)


def e_question(cr, t, tl, t0):                           # b26 "do you swim in ponds, rivers or lakes? YES or NO"
    _photo_or(cr, "pond", t, -1, W / 2, 1440, (860, 420), lambda: scene(cr, "pond", 110, 1230, 860, 420, t))
    yes_no_card(cr, t, T(tl, "b26", "Yes") - 0.2, 540, 960, w=700, h=320, question="COMMENT: YES OR NO")
    headline(cr, t, "DO YOU SWIM IN", "PONDS?", t0, T(tl, "b26", "ponds"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_jump, "paper"), ("b1", "few", h_days, "paper"), ("b1", "something", h_eating, "paper"),
    ("b2", None, h_nose, "slate"), ("b2", "climbed", h_climb, "slate"), ("b3", None, h_hurt, "paper"),
    ("b4", None, h_movie, "paper"), ("b5", None, n_name, "paper"), ("b6", None, n_kerala, "paper"),
    ("b6", "Forty", n_died, "paper"), ("b7", None, s_hair, "paper"), ("b7", "kill", s_kill, "paper"),
    ("b8", None, w_warm, "paper"), ("b8", "Ponds", w_where, "paper"), ("b9", None, w_heat, "paper"),
    ("b10", None, w_drink, "paper"), ("b10", "danger", w_danger, "paper" if P["gray_nasal"] else "slate"), ("b11", None, m_shoot, "paper"),
    ("b12", None, m_there, "paper"), ("b12", "bone", m_holes, "paper"), ("b12", "smell", m_nerves, "paper" if P["gray_olfactory"] else "slate"),
    ("b13", None, m_follow, "slate"), ("b13", "eating", m_eat, "paper" if P["gray_brain"] else "slate"),
    ("b14", None, r_scary, "paper"), ("b14", "first", r_fever, "paper"), ("b15", None, r_signs, "paper"),
    ("b16", None, r_worse, "paper"), ("b16", "moves", r_fast, "paper"), ("b17", None, r_rare, "paper"),
    ("b18", None, k_why, "paper"), ("b19", None, k_test, "paper"), ("b20", None, k_spread, "paper"),
    ("b21", None, d_hold, "paper"), ("b22", None, d_mud, "paper"), ("b23", None, d_neti, "paper"),
    ("b23", "Never", d_tap, "paper"), ("b24", None, d_doctor, "paper"), ("b24", "Tell", d_tell, "paper"),
    ("b25", None, e_bookend, "paper"), ("b26", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, a tick (and the bed dipping) before the name, each re-hook and the
    closing line, typing under the YES/NO card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b3", "already"), "thud", 0.0), (T(tl, "b4", "real"), "thud", 0.0),
           (T(tl, "b12", "holes"), "thud", 0.0), (T(tl, "b20", "spread"), "thud", 0.0),
           (T(tl, "b4", None) + 0.6, "scribble", 0.4)]
    for bid in ("b5", "b14", "b18", "b25"):
        ev.append((tl[bid].start - 0.45, "tick", 0.0))
    ev += [(T(tl, "b26", "Yes"), "typing", 1.0), (tl["b6"].start + 0.4, "pop", 0.0), (tl["b17"].start + 0.3, "pop", 0.0)]
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]
    return ev


def cover(cr):
    """Cover (Hinglish channel rule): a dark poster, one subject, at most three words, one big coloured key word,
    everything inside Instagram's 3:4 grid crop (y 240-1680)."""
    from poster import finish, slate
    slate(cr)
    X = head_cut(cr, 540, 1200, 820, 0.0, damage=0.6)
    for i in range(3):
        amoeba(cr, *X(*nerve_route(0.55 + 0.15 * i)), 40, 1.0 + i, seed=i)
    draw_text(cr, "IT EATS YOUR", W / 2, 360, 96, CREAM, anchor="ct")
    draw_text(cr, "BRAIN", W / 2, 480, 230, CORAL, anchor="ct")
    finish(cr)
