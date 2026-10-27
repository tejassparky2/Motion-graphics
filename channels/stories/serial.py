"""The end card shared by the serialized stories: no question, no A/B, just the next part (owner, 27 Oct 2026: "it will
just go as story part 1 2 3 so on leave every part with s strong hook so viewer can't resist for next part").

The last spoken line is the hook; this card fades in under it and holds over the tail."""
from motion.engine import W, H, clamp01

from channels.horror import hud2d


def next_card(cr, t, start, series, nxt, title=None, accent=hud2d.RED):
    """Darken the frame, then SERIES (small), NEXT (big, e.g. "PART 2") and TITLE (the next part's name, if known)."""
    if t < start:
        return
    k = clamp01((t - start) / 0.35)
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.72 * k)
    cr.paint()
    s = min(W, H) / 720                                       # same proportions on 9:16 and 16:9
    yc = H * (0.42 if H > W else 0.44)
    p = clamp01((t - start - 0.15) / 0.3)
    if p > 0:
        hud2d._text(cr, series, W / 2, yc - 110 * s, 26 * s, (1, 1, 1, 0.75 * p), hud2d.ROUND, "center")
        cr.set_source_rgba(*accent[:3], 0.9 * p)
        cr.rectangle(W / 2 - 90 * s * p, yc - 88 * s, 180 * s * p, 4 * s)
        cr.fill()
    p = clamp01((t - start - 0.3) / 0.3)
    if p > 0:
        hud2d._text(cr, nxt, W / 2, yc + 10 * s, 92 * s, (1, 1, 1, p), hud2d.ROUND, "center", shadow=0.6)
    p = clamp01((t - start - 0.55) / 0.3)
    if p > 0 and title:
        hud2d._text(cr, title, W / 2, yc + 80 * s, 38 * s, (*accent[:3], p), hud2d.ROUND, "center", shadow=0.5)
