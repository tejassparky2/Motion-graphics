"""The channel's news look on every story video: a small "LATEST" badge with the topic and the date, top-left above
the headline (y ~120; the headline sits at 215). Screen space."""
from .engine import INK, WHITE, cairo, hexc, rrect_pts, shape, write

RED = hexc("#e0302f")
NAVY = hexc("#1f2a52")


def badge(cr, t, topic="US NEWS", date="5 OCT 2026"):
    cr.save()
    cr.identity_matrix()
    pulse = 0.85 + 0.15 * abs(__import__("math").sin(t * 3))
    shape(cr, rrect_pts(28, 92, 132, 48, 10, 10), RED, seed=17000, amp=0.2, lw=3)
    cr.set_source_rgba(1, 1, 1, pulse)
    cr.arc(48, 116, 7, 0, 6.3)
    cr.fill()
    write(cr, [("LATEST", WHITE)], 62, 126, 26, bold=True)
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(24)
    w = cr.text_extents(f"{topic}  ·  {date}").x_advance + 30
    shape(cr, rrect_pts(158, 92, w, 48, 10, 10), NAVY, seed=17001, amp=0.2, lw=3)
    write(cr, [(f"{topic}  ·  {date}", WHITE)], 172, 125, 24, bold=True)
    cr.restore()
