"""WW2 style frame (script lines 30-32): the Hitler-Stalin pact, 8 s, 1920x1080.

    0.0-2.1  Hitler walks in from the left, Stalin from the right (the sides' colours wash the two halves)
    2.1-2.5  they stop and reach out; 2.5- the handshake, both smiling, pumping
    3.0-4.5  the camera drifts down to their backs: each hides crossed fingers (a tick and a twinkle on each hand)
    4.6      back up; 5.0 the NON-AGGRESSION PACT stamp slams in (a little shake)
    6.0      a SECRET folder slides up between them; both glance down at it
    the AUG 1939 date tag sits in the corner throughout; a slow push-in over the shot

    /home/user/.venv-main/bin/python channels/ww2/style/leaders_pact.py [--still T OUT.png]
Writes out/ww2/style/leaders_pact.mp4 (and leaders_pact_mid.png at 6.6 s).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import (H, LABEL, PAL, ROOT, SLAB, STENCIL, TITLE, W, back_out, cairo, camera,  # noqa
                                   col, date_stamp, ease_in, ease_out, halftone, lerp, paper, print_finish, push_in,
                                   rays, render_clip, seg, shake, smooth, text)
from channels.ww2.kit import stick
from channels.ww2.kit.stick import Figure

DUR = 8.0
S = 1.42                                  # a ~600 px tall pair: a low, heroic poster two-shot
GROUND = 965
T_STOP, T_SHAKE, T_STAMP, T_FOLDER = 2.1, 2.5, 5.0, 6.0


def walk_in(t):
    return stick._walk(t, period=0.6, amp=0.5, arm=0.45, lean=0.08)


SHAKE_POSE = lambda t: dict(stick._shake(t), sh_f=-0.45, el_f=0.22, hand_f="crossed",   # noqa: E731
                            face={"mouth": "smile", "brow": "neutral"})
REACH_POSE = dict(sh_n=0.95, el_n=0.35, sh_f=-0.45, el_f=0.22, hand_f="crossed", turn=0.35,
                  face={"mouth": "smile"})


def _hand_dx():
    """How far the near hand reaches in front of the hips in the handshake pose (to put the two hands together)."""
    f = Figure(leader="hitler", x=0, y=GROUND, scale=S, facing=1)
    return f.joints(T_SHAKE + 0.5, [(0, SHAKE_POSE)])["hand_n"][0]


DX = _hand_dx()
X_H, X_S = W / 2 - DX + 4, W / 2 + DX - 4            # where they stop: the hands meet at the centre
HITLER = Figure(leader="hitler", x=X_H, y=GROUND, scale=S, facing=1, seed=3)
STALIN = Figure(leader="stalin", x=X_S, y=GROUND, scale=S, facing=-1, seed=8)


def track(face_down=False):
    tr = [(0.0, walk_in), (T_STOP, "stand"), (T_STOP + 0.25, REACH_POSE), (T_SHAKE, SHAKE_POSE)]
    if face_down:
        tr.append((T_FOLDER + 0.3, lambda t: dict(SHAKE_POSE(t), nod=0.25, face={"mouth": "smile",
                                                                                 "look": (0, 5)})))
    return tr


def backdrop(cr, t):
    """The poster ground: neutral khaki rays turning slowly from behind the handshake (never red) and the floor
    band printed in each side's colour under its man."""
    paper(cr)
    rays(cr, t, W / 2, 640, n=28, color="khaki", alpha=0.42, spin=0.025)       # neutral on both halves
    halftone(cr, lambda c: c.rectangle(0, 0, W, H), "ink", density=1, alpha=0.08)
    for side, x0, x1 in (("axis", 0, W / 2), ("soviet", W / 2, W)):              # each side's colour: the floor
        cr.rectangle(x0, GROUND + 4, x1 - x0, H - GROUND)
        cr.set_source_rgba(*col(side, 0.92))
        cr.fill()
    halftone(cr, lambda c: c.rectangle(0, GROUND + 4, W, H - GROUND), "ink", density=2, alpha=0.35)
    cr.move_to(0, GROUND + 4)
    cr.line_to(W, GROUND + 4)
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()


def _old_backdrop(cr, t):
    paper(cr)
    for side, x0, x1 in (("axis", 0, W * 0.55), ("soviet", W, W * 0.45)):
        g = cairo.LinearGradient(x0, 0, x1, 0)
        r, gg, b, _ = col(side)
        a = 0.22 * ease_out(seg(t, 0.0, 1.2))
        g.add_color_stop_rgba(0, r, gg, b, a)
        g.add_color_stop_rgba(1, r, gg, b, 0)
        cr.set_source(g)
        cr.paint()
    cr.set_source_rgba(*col("ink_soft", 0.35))
    cr.set_line_width(3)
    cr.move_to(140, GROUND + 6)
    for i in range(1, 40):
        x = 140 + i * (W - 280) / 39
        cr.line_to(x, GROUND + 6 + 2.5 * math.sin(i * 1.7))
    cr.stroke()


def shadow(cr, x):
    cr.save()
    cr.translate(x, GROUND + 4)
    cr.scale(1, 0.18)
    cr.arc(0, 0, 70, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*col("ink", 0.12))
    cr.fill()


def tick(cr, t, start, x, y, scale=1.0):
    """The 'gotcha' accent on a crossed hand: four short ink ticks popping out and a gold twinkle."""
    if t < start:
        return
    u = back_out(seg(t, start, start + 0.25))
    cr.save()
    cr.translate(x, y)
    cr.scale(scale * u, scale * u)
    for a in (-2.4, -1.6, -0.8, 0.0):
        cr.move_to(26 * math.cos(a), 26 * math.sin(a))
        cr.line_to(42 * math.cos(a), 42 * math.sin(a))
    cr.set_line_width(5)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*col("ink"))
    cr.stroke()
    k = 0.6 + 0.4 * math.sin((t - start) * 9)
    cr.move_to(0, -18 * k)
    for i in range(1, 8):
        a = i * math.pi / 4 - math.pi / 2
        r = 18 * k if i % 2 == 0 else 6 * k
        cr.line_to(r * math.cos(a) + 30, r * math.sin(a) - 30)
    cr.close_path()
    cr.set_source_rgba(*col("gold"))
    cr.fill()
    cr.restore()


def stamp(cr, t, start, label, x, y, size=118, tilt=-0.09, color="alert", font=SLAB):
    """A rubber stamp slamming onto the page: a double border, the word in Anton, worn ink."""
    if t < start:
        return
    u = back_out(seg(t, start, start + 0.18))
    sc = 2.2 - 1.2 * u
    a = min(1.0, (t - start) / 0.08)
    cr.push_group()                                                  # the worn-ink holes cut the stamp only
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(sc, sc)
    cr.select_font_face(font)
    cr.set_font_size(size)
    w = cr.text_extents(label).x_advance + 6 * (len(label) - 1)
    pad = 28
    r, g, b, _ = col(color)
    cr.set_source_rgba(r, g, b, 0.9 * a)
    for k, inset in ((7, 0), (3, 14)):
        cr.set_line_width(k)
        cr.rectangle(-w / 2 - pad + inset, -size * 0.62 - pad * 0.8 + inset, w + 2 * pad - 2 * inset,
                     size * 1.24 + pad * 1.6 - 2 * inset)
        cr.stroke()
    text(cr, label, 0, size * 0.36, size, font=font, color=color, bold=False, alpha=0.9 * a, spacing=6)
    cr.set_operator(cairo.OPERATOR_DEST_OUT)                        # worn ink: tiny gaps in the stamp
    import random
    rnd = random.Random(5)
    for _ in range(140):
        cr.arc(rnd.uniform(-w / 2 - pad, w / 2 + pad), rnd.uniform(-size * 0.7, size * 0.7), rnd.uniform(1, 3.2), 0,
               2 * math.pi)
        cr.set_source_rgba(0, 0, 0, 0.55)
        cr.fill()
    cr.restore()
    cr.pop_group_to_source()
    cr.paint()


def folder(cr, t, start, cx, y_end, k=1.0):
    """A manila folder sliding up between them, a red SECRET stamp on it."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.55))
    y = lerp(H + 260, y_end, u)
    cr.save()
    cr.translate(cx, y)
    cr.scale(k, k)
    cr.rotate(0.04 * (1 - u) - 0.02)
    tab = (-150, -150, 110, 34)
    cr.rectangle(*tab)
    cr.set_source_rgba(*col("#d9b46a"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()
    cr.rectangle(-170, -120, 340, 230)
    cr.set_source_rgba(*col("#e6c27a"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.stroke()
    cr.restore()
    if t > start + 0.4:
        cr.save()
        cr.translate(cx, y)
        cr.scale(k, k)
        stamp(cr, t, start + 0.45, "SECRET", 0, -4, size=92, tilt=-0.12, font=STENCIL)
        cr.restore()


def draw(cr, t):
    backdrop(cr, t)
    z = push_in(t, 0, DUR, 1.0, 1.06)
    # the camera: wide, then down to the hands behind their backs (3.0-4.5), then back up to the pair
    d = smooth(seg(t, 3.0, 3.8)) * (1 - smooth(seg(t, 4.3, 4.9)))
    cx = W / 2
    cy = lerp(H / 2 - 20, GROUND - 270, d)
    zz = z * lerp(1.0, 1.7, d)
    sx, sy = shake(t, T_STAMP + 0.12, amp=10)
    cr.save()
    cr.translate(sx, sy)
    cr.save()
    camera(cr, zz, cx, cy)
    for fig, mv in ((HITLER, [(0.0, -260), (T_STOP, X_H)]), (STALIN, [(0.0, W + 260), (T_STOP, X_S)])):
        shadow(cr, fig._pos(t, mv)[0])
    HITLER.draw(cr, t, track(face_down=True), move=[(0.0, -260), (T_STOP, X_H)])
    STALIN.draw(cr, t, track(face_down=True), move=[(0.0, W + 260), (T_STOP, X_S)])
    for fig, mv in ((HITLER, [(0.0, -260), (T_STOP, X_H)]), (STALIN, [(0.0, W + 260), (T_STOP, X_S)])):
        hx, hy = fig.joints(t, track(), mv)["hand_f"]
        tick(cr, t, 3.55 if fig is HITLER else 3.8, hx, hy, 0.9)
    if t > T_STOP:
        a = ease_out(seg(t, T_STOP + 0.1, T_STOP + 0.5)) * (1 - ease_in(seg(t, 4.7, 5.0)))
        for name, x in (("HITLER", X_H - 60), ("STALIN", X_S + 60)):
            text(cr, name, x, GROUND + 74, 46, font=STENCIL, color="cream", alpha=a, spacing=4)
    folder(cr, t, T_FOLDER, W / 2, GROUND - 150, 0.66)
    cr.restore()
    stamp(cr, t, T_STAMP, "NON-AGGRESSION PACT", W / 2, 190, size=88, tilt=-0.05)
    cr.restore()
    date_stamp(cr, t, "AUG 1939", start=0.2)
    print_finish(cr, t)


if __name__ == "__main__":
    out = os.path.join(ROOT, "out", "ww2", "style")
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        render_clip(draw, DUR, sys.argv[i + 2], still=float(sys.argv[i + 1]))
    else:
        render_clip(draw, DUR, os.path.join(out, "leaders_pact.mp4"))
        render_clip(draw, DUR, os.path.join(out, "leaders_pact_mid.png"), still=6.6)
