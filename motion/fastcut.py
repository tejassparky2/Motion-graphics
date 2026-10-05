"""Fast-cut full-animation format: one narrator, a new full-screen shot every 1-2 seconds, each shot cut on a spoken
word with a flash and a whoosh, a punch-in zoom, impacts that shake the frame, and big slam-in words.

A video lists its shots as [(beat_id, word_key, draw_fn)]; draw_fn(cr, t, t0, t1) draws in screen space (720x1280).
Keep pictures between y=240 and y=860 so captions (y~915) stay clear."""
import math

from .engine import INK, W, H, cue, ease_out, hexc, pop, seg, write
from .kit import HALO

FLASH = hexc("#ffffff")


def shot_times(tl, shots):
    return [tl.at(bid, key) if key else tl.at(bid) for bid, key, _ in shots]


def sunburst(cr, t, col, col2, rays=16, spin=0.15):
    cr.set_source_rgba(*col)
    cr.paint()
    cr.save()
    cr.translate(W / 2, H * 0.42)
    cr.rotate(t * spin)
    cr.set_source_rgba(*col2)
    for k in range(rays):
        a0 = k * 2 * math.pi / rays
        cr.move_to(0, 0)
        cr.arc(0, 0, 1600, a0, a0 + math.pi / rays)
        cr.close_path()
    cr.fill()
    cr.restore()


def shake(t, t_hit, amp=10.0, dur=0.25):
    if not (t_hit <= t < t_hit + dur):
        return 0.0, 0.0
    k = 1 - (t - t_hit) / dur
    return amp * k * math.sin(t * 90), amp * k * math.cos(t * 77)


def slam(cr, t, start, runs, y, size, end=None, halo=HALO):
    """A big word that slams in (overshoot) on its spoken word."""
    if t < start or (end is not None and t >= end):
        return
    s = 1.6 - 0.6 * ease_out(min(1.0, (t - start) / 0.16))
    cr.save()
    cr.translate(W / 2, y)
    cr.scale(s, s)
    write(cr, runs, 0, 0, size, align="center", bold=True, halo=halo)
    cr.restore()
    cue("hit", t, start)


def run(cr, t, tl, shots):
    """Draw the current shot with its cut, zoom and flash."""
    times = shot_times(tl, shots)
    idx = 0
    for i, st in enumerate(times):
        if t >= st - 0.02:
            idx = i
    t0 = times[idx]
    t1 = times[idx + 1] if idx + 1 < len(times) else tl.total
    cue("whoosh", t, t0, 0.2)
    cr.save()
    z = 1.08 - 0.08 * ease_out(min(1.0, (t - t0) / 0.18)) + 0.05 * seg(t, t0, t1)   # punch in, then slow push
    cr.translate(W / 2, H * 0.45)
    cr.scale(z, z)
    cr.translate(-W / 2, -H * 0.45)
    shots[idx][2](cr, t, t0, t1)
    cr.restore()
    a = 0.55 * (1 - min(1.0, (t - t0) / 0.07))   # a white flash on the cut
    if idx and a > 0:
        cr.set_source_rgba(1, 1, 1, a)
        cr.paint()
