"""The doctor channel's brand: name, mascot (the heart in a surgical mask and head mirror) and the small logo every
video carries in its top-left corner. make_doc_brand.py draws the profile picture and banner from the same pieces."""
import math

from motion import engine
from motion.engine import INK, WHITE, at, blob, cairo, hexc, line, rrect_pts, shape

CHANNEL = "Doc and the Organs"
TAGLINE = "Your organs argue. The doctor explains."
SKY = hexc("#86cfdc")
MASK = hexc("#2fa36f")
RED = hexc("#d8363a")


def cross(cr, x, y, r, col=WHITE):
    w = r * 0.62
    shape(cr, rrect_pts(x - w / 2, y - r, w, 2 * r, w * 0.25, 20), col, seed=1, amp=0, lw=0, stroke=None)
    shape(cr, rrect_pts(x - r, y - w / 2, 2 * r, w, w * 0.25, 20), col, seed=2, amp=0, lw=0, stroke=None)


def mascot(cr):
    """The heart as the doctor-in-chief: surgical mask and head mirror. About 480 wide, centred on (0, 0)."""
    from videos.kidney_donor import eyes, grad_fill
    pts = []
    for k in range(80):
        a = k / 80 * 2 * math.pi
        pts.append((16 * math.sin(a) ** 3 * 13, -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a)
                                                 - math.cos(4 * a)) * 13))
    grad_fill(cr, pts, hexc("#ff6b6b"), hexc("#b5222a"), 0, 0, 240, lw=9)
    blob(cr, -90, -110, 46, 26, hexc("#ffffff", 0.35), seed=3, amp=0, lw=0, stroke=None)
    eyes(cr, 0, -40, 2.4, "happy")
    line(cr, [(-118, 30), (-200, -10)], 7, hexc("#1f6f50"), seed=4, amp=0)
    line(cr, [(118, 30), (200, -10)], 7, hexc("#1f6f50"), seed=5, amp=0)
    shape(cr, [(-120, 20), (120, 20), (112, 92), (60, 128), (-60, 128), (-112, 92)], MASK, seed=6, amp=0, lw=8)
    for k in range(3):
        line(cr, [(-100, 46 + 24 * k), (100, 46 + 24 * k)], 5, hexc("#1f7f55"), seed=7 + k, amp=0)
    line(cr, [(-150, -170), (150, -170)], 14, hexc("#3a3d45"), seed=10, amp=0)
    blob(cr, 0, -205, 56, 56, hexc("#e8edf2"), seed=11, amp=0, lw=8)
    blob(cr, 0, -205, 22, 22, hexc("#3a3d45"), seed=12, amp=0, lw=0, stroke=None)
    blob(cr, -18, -222, 12, 8, WHITE, seed=13, amp=0, lw=0, stroke=None)


def avatar(cr, size=800):
    """Square profile picture (YouTube crops it to a circle; everything important sits inside it)."""
    cr.save()
    cr.scale(size / 800, size / 800)
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(10):   # soft drape folds
        line(cr, [(-50, 80 * k), (300, 80 * k + 30), (850, 80 * k - 10)], 6, hexc("#7cc3d1"), seed=20 + k, amp=0)
    blob(cr, 400, 400, 330, 330, hexc("#ffffff", 0.35), seed=30, amp=0, lw=0, stroke=None)
    cross(cr, 400, 400, 270, hexc("#ffffff", 0.9))
    with at(cr, 400, 455, 0.92):
        mascot(cr)
    cr.restore()


def name_runs(name=None):
    """The name split into coloured runs: a short first word (DOC) in red, the rest in ink."""
    words = (name or CHANNEL).upper().split()
    if len(words) > 1 and len(words[0]) <= 3:
        return [(words[0] + " ", RED), (" ".join(words[1:]), INK)]
    return [(" ".join(words), INK)]


_BADGE = {}


def _badge_surface():
    """The corner logo (round avatar + name tag), drawn once per style and reused every frame."""
    key = engine.FONT
    if key not in _BADGE:
        w, h, d = 400, 100, 92
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(s)
        cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(27)
        runs = name_runs()
        tw = sum(cr.text_extents(t).x_advance for t, _ in runs)
        x0 = d - 14
        shape(cr, rrect_pts(x0, 28, tw + 40, 44, 22, 20), WHITE, seed=60, amp=0, lw=3)
        cx = x0 + 26
        for t, col in runs:
            cr.move_to(cx, 61)
            cr.set_source_rgba(*col)
            cr.show_text(t)
            cx += cr.text_extents(t).x_advance
        cr.save()
        cr.arc(4 + d / 2, h / 2, d / 2, 0, 2 * math.pi)
        cr.clip()
        cr.translate(4, h / 2 - d / 2)
        avatar(cr, d)
        cr.restore()
        cr.arc(4 + d / 2, h / 2, d / 2, 0, 2 * math.pi)
        cr.set_source_rgba(*WHITE)
        cr.set_line_width(4)
        cr.stroke()
        _BADGE[key] = s
    return _BADGE[key]


def corner_logo(cr, x=18, y=92, alpha=0.95):
    """Channel logo in the top-left corner, in screen space (clear of the Shorts buttons and the captions)."""
    cr.save()
    cr.identity_matrix()
    cr.set_source_surface(_badge_surface(), x, y)
    cr.paint_with_alpha(alpha)
    cr.restore()
