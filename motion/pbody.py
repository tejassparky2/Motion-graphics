"""Polished Body Facts kit (owner, 11 Oct 2026: "upgraded animation and upgraded explanation").

Glossy organ characters with faces, gradient tubes (vessels, nerves), the numbered step cards the doctor's
explanation uses ("Step one / two / three"), a tip card, and the polished clinic with the toons doctor and two
patients (Mike in a gown, Danny with a beard). Built on motion.polish / motion.pkit / motion.toons.
Layout: signs and step cards between y 230 and 400 (clear of the corner logo), faces above y 860, captions at 905.
"""
import math

from .bees import _eye, _mouth
from .engine import H, W, hexc, lerp, seg
from .pkit import GOLD, GREEN, RED, studio
from .polish import (OUTLINE, WHITE, alpha, appear, bold_text, ellipse, lin, paint, rad, rrect,
                     shade, smooth, soft_disc, soft_rrect, stroke_line, text_width, vignette)
from .toons import person

GOWN = hexc("#9fd0f0")


def face(cr, t, x, y, s, mood="open", talking=False, look=(0.0, 0.0)):
    """Two glossy eyes and a mouth (the toons/bees face), for organ characters. mood: open/happy/wide/sad/angry/
    closed/x; while talking the mouth animates."""
    eye = {"cry": "sad", "worried": "sad", "shock": "wide", "calm": "open"}.get(mood, mood)
    for side in (-1, 1):
        _eye(cr, x + side * 24 * s, y, 14 * s, 17 * s, look, eye)
        if mood in ("worried", "sad", "cry", "angry"):
            d = 1 if mood == "angry" else -1
            stroke_line(cr, [(x + side * 34 * s, y - 26 * s + d * 4 * s), (x + side * 12 * s, y - 26 * s - d * 6 * s)],
                        4.5 * s, OUTLINE, curve=False)
    if mood == "cry":
        ellipse(cr, x + 30 * s, y + 24 * s, 5 * s, 9 * s)
        paint(cr, hexc("#8fd3ff"), OUTLINE, 2)
    m = "talk" if talking else {"happy": "grin", "wide": "o", "shock": "o", "sad": "sad", "cry": "sad",
                                "worried": "sad", "angry": "flat"}.get(mood, "smile")
    cr.save()
    cr.translate(x, y + 34 * s)
    cr.scale(s, s)
    _mouth(cr, 0, 0, m, t)
    cr.restore()


def blob(cr, x, y, rx, ry, col, rot=0.0, shadow=True, gloss=True, lw=5):
    """A glossy organ shape: soft drop shadow, radial gradient, outline, top highlight."""
    if shadow:
        soft_disc(cr, x + 6, y + ry * 0.25 + 10, max(rx, ry) * 0.95, (0, 0, 0, 0.22))
    ellipse(cr, x, y, rx, ry, rot)
    paint(cr, rad(x - rx * 0.35, y - ry * 0.45, max(rx, ry) * 1.25,
                  [(0, shade(col, 0.35)), (0.55, col), (1, shade(col, -0.25))]), OUTLINE, lw)
    if gloss:
        ellipse(cr, x - rx * 0.35, y - ry * 0.5, rx * 0.32, ry * 0.16, -0.4)
        paint(cr, alpha(WHITE, 0.55), None, 0)


def shape_fill(cr, pts, col, closed=True, lw=5, shadow=True):
    """A smooth closed shape with a vertical gradient (organs that aren't ellipses)."""
    ys = [p[1] for p in pts]
    if shadow:
        cr.save()
        cr.translate(6, 10)
        smooth(cr, pts, closed)
        cr.set_source_rgba(0, 0, 0, 0.18)
        cr.fill()
        cr.restore()
    smooth(cr, pts, closed)
    paint(cr, lin(0, min(ys), 0, max(ys), [(0, shade(col, 0.3)), (0.6, col), (1, shade(col, -0.2))]), OUTLINE, lw)


def tube(cr, pts, w, col, glow=0.0):
    """A shaded tube (blood vessel, nerve): dark rim, body, light core; optional glow."""
    if glow > 0:
        stroke_line(cr, pts, w + 26, alpha(col, 0.25 * glow))
    stroke_line(cr, pts, w + 8, OUTLINE)
    stroke_line(cr, pts, w, col)
    stroke_line(cr, pts, max(2, w * 0.35), shade(col, 0.4))


def along(pts, u):
    u = min(1.0, max(0.0, u))
    f = u * (len(pts) - 1)
    i = min(len(pts) - 2, int(f))
    return lerp(pts[i][0], pts[i + 1][0], f - i), lerp(pts[i][1], pts[i + 1][1], f - i)


def spark(cr, x, y, s=1.0, col=GOLD):
    """A lightning-bolt spark (nerve signal, pain alarm)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pts = [(-10, -40), (18, -6), (2, -2), (16, 34), (-20, -4), (-2, -8)]
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    cr.restore()


def backdrop(cr, t, top, bottom, seed=1, n=12):
    """Soft gradient backdrop with drifting bokeh."""
    studio(cr, t, top, bottom, seed=seed, n=n)


def finish(cr, strength=0.32):
    vignette(cr, strength)


# ---------------------------------------------------------------- the doctor's explanation
STEP_COLS = [hexc("#4aa3f0"), hexc("#7a5bd0"), hexc("#e8473f")]


def step_card(cr, t, start, n, text, end=None, y=300, col=None):
    """'Step n' card: a numbered badge and a line of text, bouncing in at `start` (screen space)."""
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start, 0.4)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    if k <= 0.01:
        return
    col = col or STEP_COLS[(n - 1) % 3]
    w, h = 640, 150
    cr.save()
    cr.identity_matrix()
    cr.translate(W / 2, y)
    cr.scale(k, k)
    soft_rrect(cr, -w / 2, -h / 2 + 12, w, h, 30, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -w / 2, -h / 2, w, h, 30)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    cx = -w / 2 + 78
    cr.arc(cx, 0, 52, 0, 2 * math.pi)
    paint(cr, rad(cx - 16, -18, 70, [(0, shade(col, 0.35)), (1, col)]), OUTLINE, 6)
    bold_text(cr, str(n), cx, 24, 66, WHITE)
    bold_text(cr, f"STEP {n}", -w / 2 + 150, -26, 30, col, align="left", ow=5, shadow=0)
    size = 34
    tw = text_width(cr, text, size, "Fredoka")
    size *= min(1.0, (w - 180) / max(1, tw))
    bold_text(cr, text, -w / 2 + 150, 30, size, hexc("#2b1d16"), font="Fredoka", outline=None, shadow=0,
              align="left")
    cr.restore()


def tip_card(cr, t, start, text, kind="ok", end=None, y=300):
    """A green 'Do this' (kind ok) or red 'Warning' (kind warn) / 'Myth?' (kind myth) card, screen space."""
    if t < start or (end is not None and t > end + 0.2):
        return
    k = appear(t, start, 0.4)
    if end is not None and t > end:
        k *= 1 - seg(t, end, end + 0.2)
    if k <= 0.01:
        return
    col, head = {"ok": (GREEN, "DO THIS"), "warn": (RED, "SEE A DOCTOR"), "myth": (GOLD, "MYTH?")}[kind]
    w, h = 640, 160
    cr.save()
    cr.identity_matrix()
    cr.translate(W / 2, y)
    cr.scale(k, k)
    soft_rrect(cr, -w / 2, -h / 2 + 12, w, h, 30, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -w / 2, -h / 2, w, h, 30)
    paint(cr, lin(0, -h / 2, 0, h / 2, [(0, WHITE), (1, hexc("#ece4d8"))]), OUTLINE, 6)
    rrect(cr, -w / 2, -h / 2, w, 56, 30)
    paint(cr, col, None, 0)
    bold_text(cr, head, 0, -h / 2 + 44, 36, WHITE, ow=6)
    size = 34
    tw = text_width(cr, text, size, "Fredoka")
    size *= min(1.0, (w - 40) / max(1, tw))
    bold_text(cr, text, 0, 46, size, hexc("#2b1d16"), font="Fredoka", outline=None, shadow=0)
    cr.restore()


# ---------------------------------------------------------------- the polished clinic
DOC_X, MIKE_X, DANNY_X, FLOOR = 190, 500, 1020, 1240
CLINIC_CAMS = {
    "two": (1.0, 360, 700),          # doctor + Mike
    "doc": (1.25, 230, 640),
    "mike": (1.25, 520, 640),
    "danny": (1.25, 1000, 640),
    "both": (0.9, 720, 680),         # Mike + Danny
}


def clinic_bg(cr, t):
    """Soft clinic wall, window light, a cross sign, and a floor."""
    from .polish import bokeh, light_rays
    cr.rectangle(-400, -400, W + 1200, H + 800)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#cfe9f2")), (0.62, hexc("#b5dbe8")), (0.63, hexc("#e6edf2")),
                                   (1, hexc("#c9d4dc"))]))
    cr.fill()
    light_rays(cr, t, -120, 200, n=4, length=1300, a=0.08)       # window light from the left
    for cx in (720, 1300):                                     # cross signs
        rrect(cr, cx - 18, 230, 36, 110, 8)
        paint(cr, RED, OUTLINE, 4)
        rrect(cr, cx - 55, 267, 110, 36, 8)
        paint(cr, RED, OUTLINE, 4)
    bokeh(cr, t, 77, 8, [WHITE, hexc("#ffe7a8")], rmin=20, rmax=60, area=(-300, 0, 1600, 700))


def clinic(cr, t, tl, cam, mike=None, danny=None, doc=None):
    """Draw the clinic through camera `cam` (zoom, fx, fy): doctor, Mike (gown) and Danny (gown, beard)."""
    from .polish import enter
    cr.save()
    enter(cr, cam, drift=0.004, t=t)
    clinic_bg(cr, t)
    d = dict(eyes="open", mouth="smile", arms=("hold", "down"))
    d.update(doc or {})
    m = dict(eyes="open", mouth="smile", arms=("down", "down"))
    m.update(mike or {})
    n = dict(eyes="open", mouth="smile", arms=("down", "down"))
    n.update(danny or {})
    for who, x, kw, spk, facing in (("doctor", DOC_X, d, "doctor", 1), ("patient", MIKE_X, m, "mike", -1)):
        if tl.speaking(spk, t):
            kw = dict(kw, mouth="talk")
        person(cr, t, x, FLOOR, 1.25, who=who, facing=facing, **kw)
    if tl.speaking("danny", t):
        n = dict(n, mouth="talk")
    person(cr, t, DANNY_X, FLOOR, 1.25, who="villager", facing=-1, shirt=GOWN, pants=GOWN, **n)
    cr.restore()
