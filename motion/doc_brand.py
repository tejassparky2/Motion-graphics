"""The doctor channel's brand: name, the owner's logo (assets/brand/doc_logo.png: the doctor with his arms crossed
among the organs, in a glowing blue circle) and the small logo every new video carries in its top-left corner.
make_doc_brand.py builds the profile picture and banner from the same pieces. The old heart mascot is kept for
anything drawn in the cartoon style."""
import math
import os

from motion.engine import INK, WHITE, at, blob, cairo, hexc, line, rrect_pts, shape

CHANNEL = CHANNEL_DEFAULT = "Doc and the Organs"
TAGLINE = "Your organs argue. The doctor explains."
SKY = hexc("#86cfdc")
NAVY, NAVY_D, GLOW, GOLD = hexc("#0c2a6b"), hexc("#06153a"), hexc("#3d8bff"), hexc("#ffc928")
LOGO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "brand", "doc_logo.png")
LOGO_C, LOGO_R = (627, 640), 612     # the logo's circle inside the 1254x1254 image (outside it is plain white)
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


_LOGO = []


def logo_image():
    if not _LOGO:
        _LOGO.append(cairo.ImageSurface.create_from_png(LOGO))
    return _LOGO[0]


def logo_disc(cr, x, y, d):
    """The owner's logo as a disc of diameter d, top-left corner at (x, y)."""
    img = logo_image()
    sc = d / (2 * LOGO_R)
    cr.save()
    cr.arc(x + d / 2, y + d / 2, d / 2, 0, 2 * math.pi)
    cr.clip()
    cr.translate(x + d / 2, y + d / 2)
    cr.scale(sc, sc)
    cr.set_source_surface(img, -LOGO_C[0], -LOGO_C[1])
    cr.get_source().set_filter(cairo.FILTER_BEST)
    cr.paint()
    cr.restore()


def name_tag_runs():
    """DOC in white, AND THE in white, ORGANS in gold: the logo's own colours."""
    return [("DOC ", WHITE), ("AND THE ", WHITE), ("ORGANS", GOLD)]


_BADGE = {}


def _badge_surface():
    """The corner logo (the owner's round logo + a navy name tag), drawn once and reused every frame."""
    if "badge" not in _BADGE:
        w, h, d = 420, 112, 104
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(s)
        cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(27)
        runs = name_tag_runs()
        tw = sum(cr.text_extents(t).x_advance for t, _ in runs)
        x0 = d - 16
        shape(cr, rrect_pts(x0, h / 2 - 22, tw + 40, 44, 22, 20), NAVY, stroke=GLOW, seed=60, amp=0, lw=3)
        cx = x0 + 26
        for t, col in runs:
            cr.move_to(cx, h / 2 + 11)
            cr.set_source_rgba(*col)
            cr.show_text(t)
            cx += cr.text_extents(t).x_advance
        logo_disc(cr, 4, (h - d) / 2, d)
        cr.arc(4 + d / 2, h / 2, d / 2, 0, 2 * math.pi)
        cr.set_source_rgba(*GLOW)
        cr.set_line_width(3)
        cr.stroke()
        _BADGE["badge"] = s
    return _BADGE["badge"]


def corner_logo(cr, x=18, y=92, alpha=0.95):
    """Channel logo in the top-left corner, in screen space (clear of the Shorts buttons and the captions)."""
    cr.save()
    cr.identity_matrix()
    cr.set_source_surface(_badge_surface(), x, y)
    cr.paint_with_alpha(alpha)
    cr.restore()
