"""Reusable shot tools for narration-driven videos: camera, handwritten headlines, stamps, props in flight,
scene transitions and colour grades. Every video in videos/ can build on these."""
import math

from .engine import INK, W, at, cairo, cue, ease_out, hexc, lerp, pop, seg, shape, smooth, write, write_t

ANCHOR = (360, 780)   # where the camera focus point lands on screen
_cam = [(1.2, 360, 760)]


DRIFT = [0.0]   # slow push-in per second of a held shot (news videos set it), so no shot is ever frozen


def camera(t, keys, dur=0.3):
    """Ease into each camera key [(time, (zoom, fx, fy))] from the previous one."""
    keys = sorted(keys, key=lambda k: k[0])
    active = [k for k in keys if k[0] <= t]
    if not active:
        kt, z, fx, fy = keys[0][0], *keys[0][1]
        return (z * (1 + DRIFT[0] * min(max(t, 0), 6)), fx, fy)
    kt, v = active[-1]
    before = active[-2][1] if len(active) > 1 else v
    u = ease_out(seg(t, kt, kt + dur))
    z, fx, fy = (lerp(a, b, u) for a, b in zip(before, v))
    return (z * (1 + DRIFT[0] * min(t - kt, 6)), fx, fy)


def set_camera(cam):
    _cam[0] = cam


def enter_world(cr):
    z, fx, fy = _cam[0]
    cr.translate(*ANCHOR)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


HALO = hexc("#fbf3e1", 0.92)


def hl(cr, t, runs, y, size, start, end=None, bold=False, underline=False, sound=True, halo=HALO):
    """Handwritten headline in the top safe band; writes on fast, starting on the spoken word."""
    if isinstance(runs, str):
        runs = [(runs, INK)]
    n = sum(len(s) for s, _ in runs)
    write_t(cr, runs, W / 2, y, size, t, start, dur=max(0.18, 0.022 * n), end=end, align="center", bold=bold,
            underline=underline, halo=halo)
    if sound:
        cue("pop", t, start)


def stamp(cr, t, start, text, dur=0.8, y=470, color="#ffd23f"):
    """Big rotated stamp that slams in and out: a pattern interrupt instead of a slow fade."""
    if not (start <= t < start + dur):
        return
    cue("whoosh", t, start, 0.3)
    s = pop(t, start, 0.18)
    a = 1 - seg(t, start + dur - 0.15, start + dur)
    cr.save()
    cr.identity_matrix()
    cr.push_group()
    cr.select_font_face("Kalam", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(80)
    half = cr.text_extents(text).x_advance / 2 + 36
    with at(cr, W / 2, y, s, rot=-0.1):
        shape(cr, [(-half, -70), (half, -70), (half, 48), (-half, 48)], INK, seed=33, amp=1.5, lw=0, stroke=None)
        write(cr, [(text, hexc(color))], 0, 20, 80, align="center", bold=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def fly(cr, t, start, dur, p0, p1, draw, height=150):
    """Animate a prop along an arc from p0 to p1 between start and start+dur."""
    u = seg(t, start, start + dur)
    if u <= 0 or u >= 1:
        return
    e = smooth(u)
    draw(lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e) - math.sin(u * math.pi) * height)


def sepia(cr, strength=1.0):
    """Flashback grade: warm multiply + vignette."""
    cr.save()
    cr.identity_matrix()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(1.0, 0.86, 0.62, 0.55 * strength)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    g = cairo.RadialGradient(W / 2, 640, 300, W / 2, 640, 820)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.2, 0.12, 0.05, 0.45 * strength)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def whip(cr, t, start, dur=0.16):
    """Whip-pan into a new scene: call before drawing it. Returns True while the whip is running."""
    if start <= 0 or t - start >= dur:
        return False
    u = ease_out((t - start) / dur)
    cr.set_source_rgba(*INK)
    cr.paint()
    cr.translate(W * (1 - u), 0)
    cue("whoosh", t, start, 0.25)
    return True


def confetti(cr, t, start, n=40, seed=3):
    if t < start:
        return
    import random
    r = random.Random(seed)
    cols = ["#ffd23f", "#e0487a", "#4fb3e8", "#79b061", "#ff8a3d", "#8a63d2"]
    for i in range(n):
        x0 = r.uniform(0, W)
        v = r.uniform(260, 520)
        k = (t - start) * v + r.uniform(-300, 0)
        y = -40 + k
        if y < -40 or y > 1320:
            continue
        x = x0 + math.sin((t - start) * 4 + i) * 30
        cr.save()
        cr.identity_matrix()
        cr.translate(x, y)
        cr.rotate((t - start) * r.uniform(-8, 8))
        cr.rectangle(-8, -4, 16, 8)
        cr.set_source_rgba(*hexc(r.choice(cols)))
        cr.fill()
        cr.restore()
