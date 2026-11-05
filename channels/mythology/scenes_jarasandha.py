"""Scenes for videos/jarasandha.py: Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code.

One lamp-lit cloth screen for the whole reel; translucent punched-leather puppets on rods (puppet_core, puppet_cast)
move with the jerky, swinging rhythm of rod puppets, then hold. Every frame is a pure function of t. English text only
(shared by Hindi and Kannada); cues are line starts or fractions of a line, so both languages stay in sync.

Shot list (line: what is on the screen)
  j1  HOOK: frame 0 = the red half-baby, large; its eye, arm and leg pop on as each is spoken; ONE EYE. ONE ARM.
      ONE LEG. + red HALF A FACE (ghosted from frame 0, red and underlined when spoken)
  j2  the green half slides in; the two mothers loom as soft shadows; the halves snap together: ONE PERSON
  j3  HORROR FILM? crossed out; a palm-leaf book rises: MAHABHARATA + SABHA PARVA stamp
  j4  palace arch; King Brihadratha walks in, two queens follow, an empty cradle swings: NO CHILD
  j5  mango tree, the sage hands the king a mango / the king splits it, the halves fly to the queens
  j6  each queen holds up half a baby (red / green); both recoil
  j7  night, palace wall: the halves are thrown over it and land outside
  j8  Jara the rakshasi strides in from far away (out of focus -> sharp), picks the halves up, brings them together
  j9  close-up: the halves snap together in a flash; the baby roars: sound rings, thunder clouds, lightning
  j10 name card: JARA + SANDHA plaques slide together = JARASANDHA ("joined by Jara")
  j11 grown Jarasandha looms; 100 cages fill with kings, counter to 86 / 100; 14 empty cages blink; sacrificial fire
  j12 RE-HOOK: WHO STOPPED HIM? AND HOW? three blurred shadows approach
  j13 Krishna, Arjuna, Bhima walk in dressed as Brahmins (name plaques) / Jarasandha points: HE CHOSE BHIMA
  j14 the wrestlers locked; sun and moon cross 13 times, DAY 1..13 counter, day/night light; NO FOOD. NO REST.
  j15 night 14: Jarasandha droops; Bhima lifts him, whirls him (x1..x100), he splits in two halves in a lamp flash
  j16 Krishna raises his hand; the cage doors open in a wave, the kings rise free: 86 KINGS FREE
  j17 mirror of the opening: the halves join (BORN), the grown figure comes apart (ENDED IN TWO)
  j18 leather YES / NO card
"""
import math

import cairo

import puppet_cast as C
import puppet_core as pc
from poster import MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, dangle, depth, hop_walk, keyed, prop, puppet, sway
from shots import T, shot_at, starts

INK = (0.13, 0.08, 0.05)
RED = (0.72, 0.09, 0.06)
FADE = (0.42, 0.30, 0.20)
LIGHT = (1.0, 0.95, 0.82)
FEET = 1655


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        return T(tl, bid, frac)


def F(tl, bid, f):
    return T(tl, bid, f)


def man_y(s):
    return FEET - 434 * s


def woman_y(s):
    return FEET - 470 * s


# ------------------------------------------------------------------ text


def fit(text, size, maxw=W - 150):
    w, _ = text_size(text, size)
    return min(size, int(size * maxw / max(1, w)))


def small_line(cr, t, parts, y, size=62, color=INK, alpha=1.0):
    """A centred line built from pieces that appear one by one: parts = [(text, t_in), ...]."""
    gap = size * 0.34
    ws = [text_size(p, size)[0] for p, _ in parts]
    x = W / 2 - (sum(ws) + gap * (len(parts) - 1)) / 2
    for (p, t_in), w in zip(parts, ws):
        a = prog(t, t_in, 0.22)
        if a > 0:
            draw_text(cr, p, x, y + 16 * (1 - a), size, color, a * alpha)
        x += w + gap


def big_word(cr, t, text, t_in, y, size=160, color=RED, alpha=1.0, ghost_from=None, under=None):
    """The big key word: pops in at t_in (scale overshoot); shown as a faint ghost from ghost_from; under = time a red
    brush underline draws. Returns the box."""
    size = fit(text, size)
    w, h = text_size(text, size)
    if ghost_from is not None and ghost_from <= t < t_in + 0.25:
        draw_text(cr, text, W / 2, y, size, FADE, 0.28 * alpha * prog(t, ghost_from, 0.2) * (1 - prog(t, t_in, 0.25)),
                  anchor="ct")
    p = prog(t, t_in, 0.25)
    if p > 0:
        s = 1.18 - 0.18 * back(clamp((t - t_in) / 0.3))
        cr.save()
        cr.translate(W / 2, y + h / 2)
        cr.scale(s, s)
        draw_text(cr, text, 0, -h / 2, size, color, p * alpha, anchor="ct")
        cr.restore()
    if under is not None and t > under:
        q = ease((t - under) / 0.35)
        x0, x1 = W / 2 - w / 2 - 10, W / 2 + w / 2 + 10
        cr.set_source_rgba(*RED, 0.9 * alpha)
        cr.set_line_width(13)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x0, y + h + 22)
        cr.curve_to(x0 + (x1 - x0) * 0.3, y + h + 14, x0 + (x1 - x0) * 0.6, y + h + 30,
                    x0 + (x1 - x0) * q, y + h + 18)
        cr.stroke()
    return W / 2 - w / 2, y, w, h


def head2(cr, t, small, t_small, big, t_big, y=245, small_size=62, big_size=160, alpha=1.0, ghost=None, under=None,
          big_color=RED):
    if small:
        small_line(cr, t, [(wd, t_small + 0.08 * k) for k, wd in enumerate(small.split())], y, small_size,
                   alpha=alpha)
    if big:
        return big_word(cr, t, big, t_big, y + small_size * 1.25, big_size, big_color, alpha, ghost, under)


def tag(cr, t, t_in, text, x, y, size=44, alpha=1.0, color=INK, t_out=None):
    """A small leather name plaque that drops in on its rod."""
    p = clamp((t - t_in) / 0.3)
    if t_out is not None:
        p = min(p, 1 - clamp((t - t_out) / 0.25))
    if p <= 0:
        return
    w, h = text_size(text, size, MONO_FONT, 2)
    bw, bh = w + 54, h + 34
    yy = y - 40 * (1 - back(p))
    cr.save()
    cr.translate(x, yy)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    pc.poly(cr, [(-bw / 2, -bh / 2 + 10), (-bw / 2 + 10, -bh / 2), (bw / 2 - 10, -bh / 2), (bw / 2, -bh / 2 + 10),
                 (bw / 2, bh / 2 - 10), (bw / 2 - 10, bh / 2), (-bw / 2 + 10, bh / 2), (-bw / 2, bh / 2 - 10)])
    cr.set_source_rgba(*pc.PARCH, p * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, p * alpha)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_operator(cairo.OPERATOR_OVER)
    for k in range(int(bw // 18)):
        cr.arc(-bw / 2 + 12 + k * 18, -bh / 2 + 7, 2.2, 0, 2 * math.pi)
        cr.arc(-bw / 2 + 12 + k * 18, bh / 2 - 7, 2.2, 0, 2 * math.pi)
    cr.set_source_rgba(*LIGHT, 0.85 * p * alpha)
    cr.fill()
    draw_text(cr, text, 0, 1, size, color, p * alpha, MONO_FONT, "cm", tracking=2)
    cr.restore()
    pc.rod(cr, x, yy + bh / 2, x + 30, H + 50, alpha=0.5 * p * alpha)


def stamp(cr, t, t_in, text, x, y, size=70, rot=-0.08, color=RED, alpha=1.0):
    p = clamp((t - t_in) / 0.2)
    if p <= 0:
        return
    s = 1.7 - 0.7 * back(p, 2.0)
    w, h = text_size(text, size, tracking=4)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*color, 0.88 * p * alpha)
    cr.set_line_width(7)
    cr.rectangle(-w / 2 - 26, -h / 2 - 18, w + 52, h + 36)
    cr.stroke()
    draw_text(cr, text, 0, 0, size, color, 0.92 * p * alpha, anchor="cm", tracking=4)
    cr.restore()


def red_ring(cr, x, y, rx, ry, p, width=10, alpha=1.0):
    if p <= 0:
        return
    cr.set_source_rgba(*RED, 0.9 * alpha)
    cr.set_line_width(width)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    a0, span = -2.0, 2 * math.pi + 0.45
    n = max(2, int(90 * p))
    for i in range(n + 1):
        a = a0 + span * p * i / n
        wob = 1 + 0.035 * math.sin(3 * a + 1.1)
        (cr.move_to if i == 0 else cr.line_to)(x + rx * wob * math.cos(a), y + ry * wob * math.sin(a))
    cr.stroke()


def red_cross(cr, x, y, size, p, alpha=1.0):
    cr.set_source_rgba(*RED, 0.92 * alpha)
    cr.set_line_width(size * 0.11)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, (a, b) in enumerate((((-1, -1), (1, 1)), ((1, -1), (-1, 1)))):
        q = clamp(p * 2 - k)
        if q <= 0:
            continue
        cr.move_to(x + a[0] * size / 2, y + a[1] * size / 2)
        cr.line_to(x + (a[0] + (b[0] - a[0]) * q) * size / 2, y + (a[1] + (b[1] - a[1]) * q) * size / 2)
        cr.stroke()


def flip_counter(cr, t, x, y, text, size=130, color=RED, alpha=1.0, t_change=None):
    """A number on the screen that jumps (scale kick) whenever it changes."""
    k = 1.0
    if t_change is not None and 0 <= t - t_change < 0.18:
        k = 1.12 - 0.12 * (t - t_change) / 0.18
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    draw_text(cr, text, 0, 0, size, color, alpha, anchor="cm")
    cr.restore()


# ------------------------------------------------------------------ effects


def sound_rings(cr, x, y, t, t0, n=4, period=0.32, rmax=520, alpha=1.0, color=INK):
    for i in range(n):
        p = (t - t0 - i * period) / 1.1
        if 0 < p < 1:
            r = 60 + rmax * ease(p)
            cr.set_source_rgba(*color, 0.55 * (1 - p) * alpha)
            cr.set_line_width(14 * (1 - p) + 3)
            cr.arc(x, y, r, -0.9 * math.pi, -0.1 * math.pi)
            cr.stroke()
            cr.arc(x, y, r, 0.15 * math.pi, 0.85 * math.pi)
            cr.stroke()


def motes(cr, t, n=26, alpha=1.0):
    """Dust drifting in the lamp light."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(n):
        ph = i * 2.399
        x = (i * 397 + 40 * math.sin(t * 0.3 + ph)) % W
        y = H - ((t * (14 + 9 * (i % 5)) + i * 211) % (H + 100))
        r = 1.6 + (i % 4) * 0.9
        cr.set_source_rgba(1.0, 0.85, 0.55, (0.10 + 0.08 * math.sin(t * 2 + ph)) * alpha)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.fill()
    cr.restore()


def ground(cr, alpha=1.0, y=FEET + 6):
    prop(cr, "ground", W / 2, y, 0.82, alpha=alpha)


def stars(cr, t, alpha=1.0, pts=((150, 560), (300, 680), (860, 520), (980, 760), (620, 600))):
    for i, (x, y) in enumerate(pts):
        a = alpha * (0.75 + 0.25 * math.sin(t * 3 + i * 1.7))
        prop(cr, "star", x, y, 0.6 + 0.15 * (i % 2), rot=0.2 * i, alpha=a)


def glow(cr, x, y, r, a):
    """A soft warm light on the cloth (a second lamp brought close): behind Krishna, behind the joined child."""
    if a <= 0.01:
        return
    hs, n = pc._hotspot()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(x, y)
    cr.scale(r / n, r / n)
    cr.set_source_surface(hs, -n, -n)
    cr.paint_with_alpha(clamp(a))
    cr.restore()


def bob_rot(t, ph=0.0, amp=0.012):
    return sway(t, amp, 0.55, ph)


# ------------------------------------------------------------------ pose helpers


def baby_half(cr, t, k, x, y, s, rot=0.0, blur=0.0, alpha=1.0, eye=1.0, arm=1.0, leg=1.0, arm_hits=(), leg_hits=(),
              mouth=False, shut=False, rods=True, extra_rot=0.0):
    """One half-baby; eye/arm/leg 0..1 = how far each piece has popped on (0 hidden)."""
    sgn = -1 if k == "L" else 1
    rig = C.BABY[k]
    ang = {f"baby{k}_arm": sgn * (-2.4 * (1 - arm)) + dangle(t, arm_hits, 0.35, 1.5, 2.2) * sgn,
           f"baby{k}_leg": sgn * (-1.6 * (1 - leg)) + dangle(t, leg_hits, 0.25, 1.6, 2.6) * sgn}
    hide = []
    if eye <= 0:
        hide.append(f"baby{k}_eye")
    if arm <= 0:
        hide.append(f"baby{k}_arm")
    if leg <= 0:
        hide.append(f"baby{k}_leg")
    swap = {}
    if shut:
        swap[f"baby{k}_eye"] = f"baby{k}_eyeshut"
    pts = puppet(cr, rig, x, y, s, rot + extra_rot, angles=ang, alpha=alpha, blur=blur, hide=hide, swap=swap,
                 rods=rods, scales={f"baby{k}_eye": eye} if 0 < eye < 1.5 and eye != 1.0 else None)
    if mouth:
        cr.save()
        cr.translate(x, y)
        cr.rotate(rot + extra_rot)
        cr.scale(s, s)
        pc.paint_part(cr, f"baby{k}_mouth", alpha, blur)
        cr.restore()
    return pts


def baby_pair(cr, t, x, y, s, gap=0.0, rot=0.0, blur=0.0, alpha=1.0, mouth=False, shut=False, rods=True,
              arm_hits=(), dl=(0, 0, 0), dr=(0, 0, 0)):
    """Both halves; gap = design units between the cut edges; dl/dr = extra (dx, dy, rot) per half."""
    c, s_ = math.cos(rot), math.sin(rot)
    for k, sg, d in (("L", -1, dl), ("R", 1, dr)):
        ox = sg * gap / 2 * s
        baby_half(cr, t, k, x + ox * c + d[0], y + ox * s_ + d[1], s, rot + d[2], blur, alpha, mouth=mouth,
                  shut=shut, rods=rods, arm_hits=arm_hits)


def man_angles(key, t, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(), ph=0.0):
    d = dangle(t, hits, 0.22, 1.4, 2.4)
    return {key + "_armF_up": front[0] + 0.32 + d + sway(t, 0.03, 0.5, ph),
            key + "_armF_lo": front[1] + 0.55 + d * 0.6,
            key + "_armB_up": backa[0] - 0.30 - d * 0.5 + sway(t, 0.025, 0.45, ph + 1),
            key + "_armB_lo": backa[1] + 0.25,
            key + "_head": head + sway(t, 0.015, 0.4, ph + 2),
            key + "_legF": legs[0], key + "_legB": legs[1]}


def walk_legs(phase, amp=0.32):
    return (amp * phase, -amp * phase)


def woman_angles(key, t, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), ph=0.0):
    d = dangle(t, hits, 0.22, 1.4, 2.4)
    return {key + "_armF_up": front[0] + 0.08 + d + sway(t, 0.03, 0.5, ph),
            key + "_armF_lo": front[1] + 0.35 + d * 0.6,
            key + "_armB_up": backa[0] - 0.15 - d * 0.5,
            key + "_armB_lo": backa[1] + 0.2,
            key + "_head": head + sway(t, 0.015, 0.4, ph + 2)}


def walker(cr, t, rig, key, t0, t1, x0, x1, s, flip=False, kind="man", t_in=None, angles=None, alpha=1.0,
           blur_extra=0.0, **kw):
    """A puppet walking in with jerky rod-puppet steps, brought from away from the cloth (soft) onto it (sharp)."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1)
    b, k, a = depth(t, t_in if t_in is not None else t0, 0.5)
    yy = (man_y(s) if kind == "man" else woman_y(s)) + bob
    hits = [(t1, 1.0)]
    if kind == "man":
        ang = man_angles(key, t, legs=walk_legs(ph), hits=hits, ph=x0 * 0.01)
    else:
        ang = woman_angles(key, t, hits=hits, ph=x0 * 0.01)
    if angles:
        ang.update(angles)
    return puppet(cr, rig, x, yy - (k - 1) * 300 * s, s * k, rock + bob_rot(t, x0), flip=flip, angles=ang,
                  alpha=a * alpha, blur=b + blur_extra, **kw)


# ------------------------------------------------------------------ scenes (cr, t, tl, t0, t1) -> dict


def s_hook(cr, t, tl, t0, t1):
    tE = cue(tl, "j1", {"hi": "आंख", "kn": "ಕಣ್ಣು"}, 0.04)
    tA = cue(tl, "j1", {"hi": "हाथ", "kn": "ಕೈ"}, 0.28)
    tL = cue(tl, "j1", {"hi": "पैर", "kn": "ಕಾಲು"}, 0.52)
    tF = cue(tl, "j1", {"hi": "चेहरा", "kn": "ಮುಖ"}, 0.78)
    s = 1.42
    x, y = 700, 1480
    eye = back(clamp((t - tE + 0.05) / 0.25), 2.5) if t >= tE - 0.05 else 0
    arm = back(clamp((t - tA) / 0.3), 1.4)
    leg = back(clamp((t - tL) / 0.3), 1.4)
    bump = 0.035 * math.exp(-6 * max(0, t - tF)) * (t > tF)
    rot = bob_rot(t, 0.3) + 0.04 * math.exp(-4 * max(0, t - tA)) * math.sin(9 * max(0, t - tA)) * (t > tA)
    cr.save()
    cr.translate(540, 1000)
    cr.scale(1 + bump, 1 + bump)
    cr.translate(-540, -1000)
    baby_half(cr, t, "L", x, y + 6 * math.sin(t * 2.2), s, rot, eye=eye, arm=arm, leg=leg,
              arm_hits=[(tA + 0.3, 1.0)], leg_hits=[(tL + 0.3, 1.0)])
    cr.restore()
    face_x, face_y = x - 92 * s, y - 430 * s

    def ui(cr):
        small_line(cr, t, [("ONE EYE.", -1.0), ("ONE ARM.", tA - 0.05), ("ONE LEG.", tL - 0.05)], 245, 62)
        big_word(cr, t, "HALF A FACE", tF, 245 + 78, 168, ghost_from=-1.0, under=tF + 0.35)
        red_ring(cr, face_x, face_y, 190 * s * 0.92, 210 * s * 0.92, prog(t, tF + 0.15, 0.45), 11)
    return dict(ui=ui, flash=0.35 * math.exp(-5 * max(0, t - tF)) * (t > tF))


def s_two(cr, t, tl, t0, t1):
    tM = F(tl, "j2", 0.30)
    tJ = F(tl, "j2", 0.70)
    # the two mothers: big soft shadows standing away from the cloth
    m = prog(t, tM, 0.5)
    if m > 0:
        for rig, key, x, flip in ((C.QUEEN1, "queen1", 230, False), (C.QUEEN2, "queen2", 850, True)):
            puppet(cr, rig, x, 1240 - 60 * m, 0.92, bob_rot(t, x), flip=flip,
                   angles=woman_angles(key, t, front=(-0.6, -0.9)), alpha=0.75 * m, blur=10 + 12 * (1 - m),
                   rods=False)
    s = 0.92
    y = 1560
    # red half: from the hook position to the left; green half arrives from the right
    pL = ease((t - t0) / 0.4)
    xl0, xl1 = 700, 470
    # the join comes in two jerky rod-puppet pushes
    xl = xl0 + (xl1 - xl0) * pL + keyed(t, [(t0, 0.0), (tJ - 0.35, 30.0), (tJ, 70.0)], 0.22, 1.2)
    xr = keyed(t, [(t0, 1180.0), (t0 + 0.35, 640.0), (tJ - 0.35, 590.0), (tJ, 540.0)], 0.3, 1.3)
    br, kr, ar = depth(t, t0 + 0.1, 0.45)
    sL = s + (1.42 - s) * (1 - pL)
    yl = y + (1480 - y) * (1 - pL)
    baby_half(cr, t, "L", xl, yl, sL, bob_rot(t, 1), arm_hits=[(tJ, 0.8)])
    baby_half(cr, t, "R", xr, y, s * kr, bob_rot(t, 2), blur=br, alpha=ar, arm_hits=[(t0 + 0.4, 1.0), (tJ, 0.8)])
    fl = 0.4 * math.exp(-5 * max(0, t - tJ)) * (t > tJ)

    def ui(cr):
        if t < tJ:
            head2(cr, t, "TWO PIECES. TWO", t0 + 0.1, "MOTHERS", tM, alpha=1 - prog(t, tJ - 0.2, 0.2))
        else:
            head2(cr, t, "JOINED INTO", tJ, "ONE PERSON", tJ + 0.15, under=tJ + 0.5)
        if t > tJ:
            red_ring(cr, 540, y - 330 * s, 300, 380, prog(t, tJ + 0.1, 0.4), 9, alpha=1 - prog(t, tJ + 1.4, 0.4))
    return dict(ui=ui, flash=fl)


def s_text(cr, t, tl, t0, t1):
    tX = F(tl, "j3", 0.22)
    tB = F(tl, "j3", 0.45)
    tS = F(tl, "j3", 0.72)
    # the joined baby stays small at the bottom, then the book rises over it
    b, k, a = depth(t, tB - 0.2, 0.5)
    by = 1060 + 600 * (1 - ease((t - tB + 0.2) / 0.5))
    rot = -0.04 + sway(t, 0.02, 0.4)
    baby_pair(cr, t, 540, 1560 + 400 * prog(t, tB - 0.3, 0.5), 0.62, alpha=1 - prog(t, tB - 0.3, 0.4),
              rods=t < tB - 0.3)
    if t > tB - 0.25:
        cr.save()
        cr.translate(540, by)
        cr.rotate(rot)
        cr.scale(1.3 * k, 1.3 * k)
        pc.paint_part(cr, "book", a, b)
        if t > tB + 0.2:
            draw_text(cr, "MAHABHARATA", 0, -6, 88, INK, prog(t, tB + 0.2, 0.3) * a, anchor="cm")
        cr.restore()
        pc.rod(cr, 540 - 280, by + 140, 400, H + 60, alpha=a)
        pc.rod(cr, 540 + 280, by + 140, 700, H + 60, alpha=a)

    def ui(cr):
        draw_text(cr, "NOT A", W / 2, 300, 66, INK, prog(t, t0 + 0.05, 0.2), anchor="ct")
        struck = t > tX + 0.3
        bx, byy, bw, bh = big_word(cr, t, "HORROR FILM", t0 + 0.15, 380, 170, color=FADE if struck else INK)
        if t > tX:
            red_cross(cr, W / 2, byy + bh / 2, min(bw, bh * 2.4), prog(t, tX, 0.3))
        stamp(cr, t, tS, "SABHA PARVA", W / 2, by + 250, 76, rot=-0.06)
        if t > tS + 0.3:
            draw_text(cr, "BOOK 2 OF THE MAHABHARATA", W / 2, by + 350, 30, INK, prog(t, tS + 0.3, 0.3), MONO_FONT,
                      "ct", tracking=3)
    return dict(ui=ui)


def s_king(cr, t, tl, t0, t1):
    tQ = F(tl, "j4", 0.42)
    tC = F(tl, "j4", 0.72)
    ba, ka, aa = depth(t, t0, 0.4)
    prop(cr, "arch", 540, FEET + 10, 0.80 * ka, alpha=aa, blur=ba)
    # cradle hanging from the arch, swinging empty
    if t > tC - 0.3:
        p = ease((t - tC + 0.3) / 0.35)
        sw = 0.22 * math.exp(-0.8 * max(0, t - tC)) * math.sin(3.2 * (t - tC)) + 0.04 * math.sin(t * 1.7)
        prop(cr, "cradle", 540, 820 - 300 * (1 - p), 0.62, rot=sw, alpha=p)
        pc.rod(cr, 540, 820 - 300 * (1 - p), 540, 300, alpha=0.6 * p)
    walker(cr, t, C.KING, "king", t0, t0 + 1.0, -120, 300, 0.86)
    walker(cr, t, C.QUEEN1, "queen1", tQ, tQ + 0.9, 1200, 700, 0.8, flip=True, kind="woman")
    walker(cr, t, C.QUEEN2, "queen2", tQ + 0.15, tQ + 1.05, 1350, 880, 0.78, flip=True, kind="woman")

    def ui(cr):
        small_line(cr, t, [("KING", t0 + 0.2), ("OF", t0 + 0.28), ("MAGADHA", t0 + 0.36)], 245)
        if t < tC:
            big_word(cr, t, "BRIHADRATHA", t0 + 0.5, 323, 140, color=INK, alpha=1 - prog(t, tC - 0.15, 0.15))
            if t > tQ:
                tag(cr, t, tQ + 0.4, "2 QUEENS", 790, 520)
        else:
            big_word(cr, t, "NO CHILD", tC, 323, 160)
            red_cross(cr, 540, 1000, 200, prog(t, tC + 0.35, 0.3))
    return dict(ui=ui)


def s_mango(cr, t, tl, t0, t1):
    tG = F(tl, "j5", 0.14)
    tP = F(tl, "j5", 0.26)
    ba, ka, aa = depth(t, t0, 0.4)
    prop(cr, "tree", 850, FEET + 10, 0.80 * ka, rot=sway(t, 0.006, 0.3), alpha=aa, blur=ba)
    ground(cr)
    ang = man_angles("sage", t, front=keyed(t, [(t0, (-0.3, -0.5)), (tG, (-1.2, -0.3))], 0.3), hits=[(tG + 0.3, 0.6)])
    sp = puppet(cr, C.SAGE, 720, man_y(0.80), 0.80, bob_rot(t, 3), flip=True, angles=ang)
    kp = walker(cr, t, C.KING, "king", t0, t0 + 0.9, -150, 300, 0.86,
                angles={"king_armF_up": keyed(t, [(t0, 0.0), (tP - 0.2, -0.75)], 0.3),
                        "king_armF_lo": keyed(t, [(t0, 0.0), (tP - 0.2, 0.2)], 0.3)})
    # the mango: in the sage's hand, then an arc to the king's
    hx, hy = sp["handF"]
    kx, ky = kp["handF"]
    q = ease((t - tP) / 0.55)
    mx = hx + (kx - hx) * q
    my = hy + (ky - hy) * q - 160 * math.sin(math.pi * q)
    if t > tG - 0.1:
        prop(cr, "mango", mx, my - 30, 0.95, rot=0.5 * q, alpha=prog(t, tG - 0.1, 0.2))

    def ui(cr):
        head2(cr, t, "A SAGE GIVES THE KING", t0 + 0.2, "ONE MANGO", tP)
        if t > tG:
            red_ring(cr, mx, my - 30, 90, 90, prog(t, tP + 0.6, 0.4), 8)
    return dict(ui=ui)


def s_split(cr, t, tl, t0, t1):
    tS = F(tl, "j5", 0.66)
    tF = F(tl, "j5", 0.80)
    for rig, key, x, fl, sc in ((C.QUEEN1, "queen1", 175, False, 0.8), (C.QUEEN2, "queen2", 905, True, 0.8)):
        b, k, a = depth(t, t0 + 0.1, 0.4)
        reach = keyed(t, [(t0, 0.0), (tF + 0.2, 1.0)], 0.3)
        ang = woman_angles(key, t, front=(-0.08 - 0.9 * reach, -0.35 + 0.1 * reach), hits=[(tF + 0.5, 0.8)])
        puppet(cr, rig, x, woman_y(sc), sc * k, bob_rot(t, x), flip=fl, angles=ang, alpha=a, blur=b)
    ang = man_angles("king", t, front=keyed(t, [(t0, (-1.0, -0.6)), (tS, (-1.3, -0.3))], 0.25),
                     backa=keyed(t, [(t0, (0.3, -0.25)), (tS, (-0.9, -0.6))], 0.25))
    kp = puppet(cr, C.KING, 540, man_y(0.9), 0.9, bob_rot(t, 1), angles=ang)
    cx, cy = 540 + 60, 820
    sp = ease((t - tS) / 0.3)
    fly = ease((t - tF) / 0.6)
    lx, ly = cx - 70 * sp, cy
    rx_, ry_ = cx + 70 * sp, cy
    qlx, qrx = 290, 790
    lx += (qlx - lx) * fly
    rx_ += (qrx - rx_) * fly
    ly += (980 - ly) * fly - 200 * math.sin(math.pi * fly)
    ry_ += (980 - ry_) * fly - 200 * math.sin(math.pi * fly)
    if t < tS:
        prop(cr, "mango", cx, cy, 1.9, rot=sway(t, 0.05, 0.8))
    else:
        prop(cr, "mangoL", lx, ly, 1.9 - 0.7 * fly, rot=-0.4 * sp)
        prop(cr, "mangoR", rx_, ry_, 1.9 - 0.7 * fly, rot=0.4 * sp)
    fl = 0.4 * math.exp(-6 * max(0, t - tS)) * (t > tS)

    def ui(cr):
        head2(cr, t, "SPLIT FOR TWO QUEENS", t0 + 0.1, "HALF EACH", tS, under=tF)
    return dict(ui=ui, flash=fl)


def s_birth(cr, t, tl, t0, t1):
    tL = F(tl, "j6", 0.30)
    tR = F(tl, "j6", 0.48)
    tX = F(tl, "j6", 0.85)
    for rig, key, x, fl, ph in ((C.QUEEN1, "queen1", 200, False, 0), (C.QUEEN2, "queen2", 880, True, 1)):
        rec = keyed(t, [(t0, 0.0), (tX, 1.0)], 0.2, 2.0)
        ang = woman_angles(key, t, front=(-0.6 - 1.4 * rec, -1.0 + 0.4 * rec), backa=(0.15 - 1.2 * rec, -0.6),
                           head=-0.12 * rec, hits=[(tX + 0.2, 1.0)])
        puppet(cr, rig, x - (1 if not fl else -1) * 30 * rec, woman_y(0.86), 0.86, bob_rot(t, ph) - 0.06 * rec *
               (1 if not fl else -1), flip=fl, angles=ang)
    for k, x, tin in (("L", 470, tL), ("R", 610, tR)):
        p = back(clamp((t - tin) / 0.35), 1.8)
        if p > 0:
            baby_half(cr, t, k, x, 1330 - 30 * p, 0.62 * p, bob_rot(t, x), arm_hits=[(tin + 0.3, 1.0)])
    fl = 0.3 * (math.exp(-6 * max(0, t - tL)) * (t > tL) + math.exp(-6 * max(0, t - tR)) * (t > tR))

    def ui(cr):
        head2(cr, t, "EACH QUEEN GAVE BIRTH TO", t0 + 0.1, "HALF A CHILD", tL)
        tag(cr, t, tL + 0.15, "QUEEN 1", 330, 1580, 34)
        tag(cr, t, tR + 0.15, "QUEEN 2", 750, 1580, 34)
    return dict(ui=ui, flash=fl)


def s_thrown(cr, t, tl, t0, t1):
    tT = F(tl, "j7", 0.35)
    tLand = tT + 0.75
    mp = prog(t, t0, 1.2)
    prop(cr, "moon", 860, 620 - 80 * mp, 0.9, rot=-0.3, alpha=mp)
    stars(cr, t, mp)
    prop(cr, "wall", 200, FEET + 10, 0.72)
    ground(cr)
    for k, x0, x1, ph in (("L", 160, 790, 0.0), ("R", 300, 960, 0.12)):
        q = clamp((t - tT - ph) / 0.75)
        if t < tT + ph:
            x, y, r, bl = x0, 1350 + 40 * math.sin(t * 6 + ph * 20), 0.0, 0
        else:
            e = q
            x = x0 + (x1 - x0) * e
            y = 1350 - 520 * math.sin(math.pi * e) + (1520 - 1350) * e
            r = (1 if k == "L" else -1) * 6.0 * e
            bl = 6 * math.sin(math.pi * e)
        if q >= 1:
            dt = t - tT - ph - 0.75
            r = (1 if k == "L" else -1) * (6.0 + 0.15 * math.exp(-5 * dt) * math.sin(14 * dt)) + (
                1.2 if k == "L" else -1.4)
            y = 1540
        baby_half(cr, t, k, x, y, 0.42, r, blur=bl, rods=q <= 0)

    def ui(cr):
        head2(cr, t, "IN FEAR, THE PIECES WERE", t0 + 0.1, "THROWN OUT", tT)
    return dict(ui=ui, night=0.45 * mp)


def s_jara(cr, t, tl, t0, t1):
    tN = F(tl, "j8", 0.12)
    tB = F(tl, "j8", 0.40)
    tP = F(tl, "j8", 0.62)
    tJ = F(tl, "j8", 0.88)
    prop(cr, "moon", 860, 540, 0.9, rot=-0.3)
    stars(cr, t)
    ground(cr)
    # Jara strides in from far away (big, soft) to the cloth (sharp)
    x, bob, rock, ph = hop_walk(t, t0, tN + 0.6, -260, 360, 0.5)
    b, k, a = depth(t, t0, 1.0, far=24)
    bend = keyed(t, [(t0, 0.0), (tB, 0.32), (tP + 0.4, 0.05)], 0.35, 1.3)
    reach = keyed(t, [(t0, 0.0), (tB, 1.0), (tP + 0.4, 0.4), (tJ, 0.15)], 0.35, 1.3)
    s = 1.05
    ang = {"jara_armF_up": -0.1 - 0.9 * reach + dangle(t, [(tN + 0.6, 1)], 0.25),
           "jara_armF_lo": 0.35 - 0.3 * reach - 0.9 * (t > tJ) * ease((t - tJ) / 0.3),
           "jara_armB_up": -0.15 - 0.7 * reach,
           "jara_armB_lo": 0.2 - 0.6 * reach - 0.8 * (t > tJ) * ease((t - tJ) / 0.3),
           "jara_head": 0.1 * bend + sway(t, 0.02, 0.5)}
    jp = puppet(cr, C.JARA, x, woman_y(s) + bob - (k - 1) * 300, s * k, rock + bend + bob_rot(t, 5), angles=ang,
                alpha=a, blur=b)
    # the halves on the ground, then in her hands, then brought together
    hf, hb = jp["handF"], jp["handB"]
    for kk, gx, gr, hand, dx in (("L", 640, 1.2 + 6.0, hb, -60), ("R", 860, -1.4 - 6.0, hf, 60)):
        q = ease((t - tP) / 0.5)
        hx, hy = hand
        jx = (hf[0] + hb[0]) / 2 + 40
        tx = hx + (jx + dx * (1 - ease((t - tJ) / 0.4)) * 1.0 - hx) * ease((t - tJ) / 0.4)
        x_ = gx + (tx - gx) * q
        y_ = 1540 + (hy + 120 - 1540) * q
        r = gr * (1 - q) + (0.0 if kk == "L" else 0.0) * q
        baby_half(cr, t, kk, x_, y_, 0.42, r, rods=False)

    def ui(cr):
        if t < tP:
            head2(cr, t, "A RAKSHASI NAMED", t0 + 0.2, "JARA", tN, big_size=190)
        else:
            head2(cr, t, "TO CARRY THEM, SHE", tP, "PUT THEM TOGETHER", tJ - 0.3, big_size=130)
    return dict(ui=ui, night=0.35)


def s_join(cr, t, tl, t0, t1):
    tJ = t0 + 0.35
    tR = F(tl, "j9", 0.50)
    g = 120 * (1 - ease((t - t0) / 0.35))
    shake = 0.0
    if t > tR:
        dt = t - tR
        shake = 10 * math.exp(-2.2 * dt) * math.sin(47 * dt)
    roar = t > tR
    cr.save()
    cr.translate(shake, shake * 0.6)
    # thunder clouds and lightning
    if roar:
        p = ease((t - tR) / 0.35)
        for x, y, s_, ph in ((250, 640, 0.85, 0), (820, 600, 0.95, 1)):
            prop(cr, "cloud", x, y - 260 * (1 - p), s_, rot=sway(t, 0.02, 0.6, ph), alpha=p)
        for k, (bx, bt) in enumerate(((330, 0.05), (760, 0.45), (520, 0.9))):
            f = (t - tR - bt) % 1.3
            if f < 0.18:
                prop(cr, "bolt", bx, 690, 0.9, rot=0.1 * (k - 1), alpha=1 - f / 0.18)
    s = 1.12
    baby_pair(cr, t, 540, 1560, s, gap=g, mouth=roar, shut=roar, arm_hits=[(tJ, 1.0), (tR, 1.5)])
    cr.restore()
    fl = 0.7 * math.exp(-4 * max(0, t - tJ)) * (t > tJ)
    if roar:
        fl += 0.5 * math.exp(-3 * ((t - tR) % 1.3)) * (t - tR < 3)

    def ui(cr):
        if t < tR:
            head2(cr, t, "AND THE PIECES", t0 + 0.05, "JOINED", tJ, big_size=180)
        else:
            head2(cr, t, "HE ROARED LIKE", tR, "THUNDER", tR + 0.1, big_size=190)
            sound_rings(cr, 540, 1560 - 320 * s, t, tR, 6, 0.28, 560)
    return dict(ui=ui, flash=fl)


def s_name(cr, t, tl, t0, t1):
    tN = F(tl, "j10", 0.55)
    puppet(cr, C.JARA, 170, woman_y(1.0), 1.0, bob_rot(t, 5), angles=woman_angles("jara", t, front=(-0.9, -0.6)),
           alpha=0.55, blur=9, rods=False)
    baby_pair(cr, t, 600, 1640, 0.6)
    j = keyed(t, [(t0, 0.0), (t0 + 0.25, 0.4), (tN - 0.25, 1.0)], 0.3, 1.3)
    gap = 260 * (1 - j)
    y = 800
    wL = text_size("JARA", 110)[0]
    wR = text_size("SANDHA", 110)[0]
    tot = wL + wR + 10
    xL = W / 2 - tot / 2 - gap
    xR = W / 2 - tot / 2 + wL + 10 + gap
    cr.save()
    cr.translate(540, y)
    cr.scale(1.22, 1.22)
    pc.paint_part(cr, "plaque", alpha=prog(t, t0, 0.3))
    cr.restore()
    pc.rod(cr, 540, y + 130, 560, H + 60, alpha=prog(t, t0, 0.3))
    fl = 0.4 * math.exp(-6 * max(0, t - tN)) * (t > tN)

    def ui(cr):
        col = RED if t > tN - 0.05 else INK
        draw_text(cr, "JARA", xL, y, 110, col, prog(t, t0 + 0.1, 0.25), anchor="lm")
        draw_text(cr, "SANDHA", xR, y, 110, col, prog(t, t0 + 0.2, 0.25), anchor="lm")
        draw_text(cr, "SANDHA = JOINED", W / 2, 960, 40, INK, prog(t, t0 + 0.3, 0.3), MONO_FONT, "ct", tracking=3)
        head2(cr, t, "JOINED BY JARA, SO HIS NAME:", t0 + 0.05, "JARASANDHA", tN, big_size=170, ghost=t0)
    return dict(ui=ui, flash=fl)


GRID = dict(cols=10, rows=10, x0=150, y0=700, dx=86, dy=94, s=0.62)


def cage_grid(cr, t, filled, t_fill0=None, t_fill1=None, open_t=None, red_empty=None, g=GRID, alpha=1.0,
              free_t=None):
    n_show = 100
    for i in range(n_show):
        r, c = divmod(i, g["cols"])
        x = g["x0"] + c * g["dx"]
        y = g["y0"] + r * g["dy"]
        s = g["s"]
        prop(cr, "cage", x, y, s, alpha=alpha)
        has = i < filled
        if t_fill0 is not None and has:
            ti = t_fill0 + (t_fill1 - t_fill0) * i / max(1, filled - 1)
            p = clamp((t - ti) / 0.12)
            if p <= 0:
                continue
        else:
            p = 1.0
        if has:
            up = 0.0
            if free_t is not None:
                tf = free_t + 0.012 * i
                up = ease((t - tf - 0.25) / 0.7)
            prop(cr, f"kingS{i % 5}", x, y - 6 - 60 * up - 8 * (1 - p), s, alpha=alpha * p * (1 - up))
        if open_t is not None:
            to = open_t + 0.012 * i
            a = -1.9 * ease((t - to) / 0.3)
            prop(cr, "cage_door", x - 28 * s * 1.6, y - 75 * s * 1.25, s * 0.62, rot=a, alpha=alpha)
        elif red_empty is not None and not has and t > red_empty:
            k = 0.5 + 0.5 * math.sin((t - red_empty) * 9)
            cr.set_source_rgba(*RED, 0.85 * alpha * k)
            cr.set_line_width(4)
            cr.rectangle(x - 34, y - 98, 68, 104)
            cr.stroke()


GRID2 = dict(GRID, x0=420, y0=770, dx=62, dy=72, s=0.46)


def mace_in(key):
    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(-0.2)
        cr_.scale(0.8, 0.8)
        pc.paint_part(cr_, "mace")
        cr_.restore()
    return {key + "_armF_lo": fn}


def s_kings(cr, t, tl, t0, t1):
    tF0 = F(tl, "j11", 0.12)
    tF1 = F(tl, "j11", 0.48)
    tW = F(tl, "j11", 0.62)
    b, k, a = depth(t, t0, 0.5, far=24)
    lift = keyed(t, [(t0, 0.0), (t0 + 0.5, 1.0), (tW, 0.4)], 0.3, 1.5)
    ang = man_angles("jsandha", t, front=(-0.5 - 1.2 * lift, -0.6 + 0.3 * lift), hits=[(t0 + 0.5, 1.0), (tW, 0.6)])
    puppet(cr, C.JSANDHA, 200, man_y(0.95) - (k - 1) * 280, 0.95 * k, bob_rot(t, 4), angles=ang, alpha=a, blur=b,
           extra=mace_in("jsandha"))
    n = int(clamp((t - tF0) / max(0.1, tF1 - tF0)) * 85.999) + 1 if t > tF0 else 0
    cage_grid(cr, t, 86, tF0, tF1, red_empty=tW, g=GRID2)
    ground(cr)
    if t > tW - 0.2:
        p = prog(t, tW - 0.2, 0.4)
        prop(cr, "altar", 700, FEET + 14, 0.8, alpha=p)
        prop(cr, f"flame{int(t * 10) % 3}", 700, FEET - 50, 0.55 * p, alpha=p)

    def ui(cr):
        small_line(cr, t, [("KINGS", t0 + 0.1), ("IN", t0 + 0.18), ("HIS", t0 + 0.26), ("CAGES", t0 + 0.34)], 245)
        txt = f"{n}"
        tc = tF0 + (tF1 - tF0) * (n - 1) / 85 if n > 0 else None
        if t > tF0 - 0.1:
            flip_counter(cr, t, W / 2 - 110, 420, txt, 170, RED, t_change=tc)
            draw_text(cr, "/ 100", W / 2 + 10, 420, 110, INK, prog(t, tW, 0.3), anchor="lm")
        if t > tW:
            stamp(cr, t, tW + 0.3, "HE WANTED 100", 700, 590, 46, rot=-0.04)
    return dict(ui=ui)


def s_rehook(cr, t, tl, t0, t1):
    tH = F(tl, "j12", 0.55)
    ang = man_angles("jsandha", t, front=(-1.4, -0.4), hits=[(t0, 1.0)])
    puppet(cr, C.JSANDHA, 360, man_y(1.0), 1.0, bob_rot(t, 4), angles=ang)
    for i, (rig, key) in enumerate(((C.BHIMA, "bhima"), (C.ARJUNA, "arjuna"), (C.KRISHNA, "krishna"))):
        x = 760 + 130 * i - 60 * ease((t - t0) / 1.5)
        puppet(cr, rig, x, man_y(1.3) + 120, 1.3, bob_rot(t, i), flip=True,
               angles=man_angles(key, t, ph=i), alpha=0.5, blur=20, rods=False)
    ground(cr)

    def ui(cr):
        head2(cr, t, "SO...", t0, "WHO STOPPED HIM?", t0 + 0.15, big_size=150)
        draw_text(cr, "AND HOW?", W / 2, 560, 90, INK, prog(t, tH, 0.25), anchor="ct")
    return dict(ui=ui, night=0.2)


def s_three(cr, t, tl, t0, t1):
    tB = F(tl, "j13", 0.30)
    ground(cr)
    cast = ((C.BHIMA, "bhima", 230, 0.9, 0.0), (C.ARJUNA, "arjuna", 520, 0.8, 0.12), (C.KRISHNA, "krishna", 800, 0.8,
                                                                                      0.24))
    pts = []
    for rig, key, x1, s, d in cast:
        extra = None
        if key == "arjuna":
            def extra_fn(cr_):
                cr_.save()
                cr_.translate(0, 150)
                cr_.rotate(0.15)
                pc.paint_part(cr_, "bow")
                cr_.restore()
            extra = {"arjuna_armB_lo": extra_fn}
        p = walker(cr, t, rig, key, t0 + d - 0.2, t0 + d + 1.2, x1 - 380, x1, s, extra=extra, t_in=t0 - 0.3)
        pts.append(p)

    def ui(cr):
        for (rig, key, x1, s, d), p, nm in zip(cast, pts, ("BHIMA", "ARJUNA", "KRISHNA")):
            hx, hy = p["top"]
            tag(cr, t, t0 + 1.2 + d * 2, nm, x1 + 20, 650, 36)
        head2(cr, t, "DISGUISED AS", t0 + 0.2, "BRAHMINS", tB, big_size=160)
    return dict(ui=ui)


def s_choose(cr, t, tl, t0, t1):
    tP = F(tl, "j13", 0.80)
    ground(cr)
    for i, (rig, key, x) in enumerate(((C.KRISHNA, "krishna", 120), (C.ARJUNA, "arjuna", 230))):
        puppet(cr, rig, x, man_y(0.82), 0.82, bob_rot(t, i), angles=man_angles(key, t, ph=i), alpha=0.8, blur=7,
               rods=False)
    puppet(cr, C.BHIMA, 360, man_y(0.95), 0.95, bob_rot(t, 3), angles=man_angles("bhima", t))
    point = keyed(t, [(t0, 0.0), (tP - 0.2, 1.0)], 0.25, 1.8)
    ang = man_angles("jsandha", t, front=(-0.3 - 1.25 * point, -0.55 + 0.5 * point), hits=[(tP, 0.6)])
    puppet(cr, C.JSANDHA, 790, man_y(0.98), 0.98, bob_rot(t, 4), flip=True, angles=ang)

    def ui(cr):
        head2(cr, t, "TO WRESTLE, JARASANDHA CHOSE", t0 + 0.1, "BHIMA", tP, big_size=190)
        red_ring(cr, 360, man_y(0.95) - 120, 190, 430, prog(t, tP + 0.2, 0.45), 10)
    return dict(ui=ui)


def wrestlers(cr, t, push, tired=0.0, draw_j=True):
    """Bhima (left) and Jarasandha (right) locked; push = -1..1 sway of the struggle; tired droops Jarasandha."""
    bx = 430 + 30 * push
    jx = 650 + 30 * push
    sB, sJ = 0.92, 0.95
    angB = man_angles("bhima", t, front=(-1.55, -0.2), backa=(-1.2, -0.4), legs=(-0.35, 0.3))
    puppet(cr, C.BHIMA, bx, man_y(sB), sB, 0.10 + 0.04 * push, angles=angB)
    if draw_j:
        d = tired
        angJ = man_angles("jsandha", t, front=(-1.5 + 1.2 * d, -0.2 + 0.3 * d), backa=(-1.1 + 1.2 * d, -0.4),
                          head=0.45 * d, legs=(-0.3 + 0.2 * d, 0.3))
        puppet(cr, C.JSANDHA, jx + 40 * d, man_y(sJ) + 30 * d, sJ, -0.10 - 0.04 * push + 0.18 * d, flip=True,
               angles=angJ)
    return bx, jx


def s_days(cr, t, tl, t0, t1):
    tN = F(tl, "j14", 0.72)
    end = t1 - 0.2
    D = 13
    span = (end - (t0 + 0.4)) / D
    u = (t - t0 - 0.4) / span if t > t0 + 0.4 else 0.0
    day = int(clamp(u, 0, D - 0.001)) + 1 if t > t0 + 0.4 else 1
    f = u - int(u) if t > t0 + 0.4 else 0.0
    is_night = f >= 0.5 and t > t0 + 0.4
    g = (f * 2) % 1.0
    ax = 110 + 860 * g
    ay = 760 - 190 * math.sin(math.pi * g)
    prop(cr, "moon" if is_night else "sun", ax, ay, 0.6 if is_night else 0.42, rot=g * (0.5 if is_night else 2.0))
    if is_night:
        stars(cr, t, 0.8)
    ground(cr)
    beat = 0.45
    k = int((t - t0) / beat)
    push = keyed(t, [(t0 + i * beat, (0.8 if i % 2 else -0.8)) for i in range(max(1, k + 1))], 0.18, 1.6)
    wrestlers(cr, t, push)
    night = 0.0
    if t > t0 + 0.4:                                  # a gentle day/night swell of the light, never a strobe
        night = 0.22 * (0.5 - 0.5 * math.cos(2 * math.pi * (u - 0.25))) * clamp((t - t0 - 0.4) / 0.4)

    def ui(cr):
        small_line(cr, t, [("FROM", t0 + 0.05), ("THE", t0 + 0.1), ("1ST", t0 + 0.15), ("OF", t0 + 0.2),
                           ("KARTIKA", t0 + 0.25)], 245, 58)
        tc = t0 + 0.4 + (day - 1) * span
        draw_text(cr, "DAY", W / 2 - 40, 400, 120, INK, prog(t, t0 + 0.3, 0.2), anchor="rm")
        flip_counter(cr, t, W / 2 + 90, 400, f"{day}", 170, RED, t_change=tc)
        if t > tN:
            small_line(cr, t, [("NO FOOD.", tN), ("NO REST.", tN + 0.35)], 535, 70, color=RED)
    return dict(ui=ui, night=night)


def s_final(cr, t, tl, t0, t1):
    tL = F(tl, "j15", 0.22)
    tW0 = F(tl, "j15", 0.40)
    tW1 = F(tl, "j15", 0.74)
    tS = F(tl, "j15", 0.93)
    prop(cr, "moon", 860, 600, 0.75, rot=-0.3)
    stars(cr, t, 0.8)
    ground(cr)
    tired = keyed(t, [(t0, 0.0), (t0 + 0.35, 1.0)], 0.5, 1.1)
    lift = keyed(t, [(t0, 0.0), (tL, 1.0)], 0.4, 1.2)
    bx, sB = 430, 0.92
    HX, HY, sJ = 610, 640, 0.72              # where Bhima holds him overhead (his hip)
    # Bhima: locked arms -> both arms raised, holding him up
    wob = 0.12 * math.sin((t - tW0) * 2 * math.pi * 5) if tW0 <= t < tW1 else 0.0
    angB = man_angles("bhima", t, front=(-1.55 - 1.0 * lift + wob, -0.2 - 0.25 * lift),
                      backa=(-1.2 - 1.3 * lift + wob, -0.4 - 0.1 * lift), legs=(-0.35 - 0.1 * lift, 0.3 + 0.1 * lift))
    if t < tL:
        d = tired
        angJ = man_angles("jsandha", t, front=(-1.5 + 1.2 * d, -0.2 + 0.3 * d), backa=(-1.1 + 1.2 * d, -0.4),
                          head=0.45 * d, legs=(-0.3 + 0.2 * d, 0.3))
        puppet(cr, C.JSANDHA, 690, man_y(0.95) + 30 * d, 0.95, -0.10 + 0.18 * d, flip=True, angles=angJ)
    puppet(cr, C.BHIMA, bx, man_y(sB), sB, 0.10 - 0.12 * lift, angles=angB)
    if t >= tL:
        p = ease((t - tL) / 0.45)
        cx = 690 + (HX - 690) * p
        cy = man_y(0.95) + (HY - man_y(0.95)) * p
        sc = 0.95 + (sJ - 0.95) * p
        if t < tW0:
            rot = 1.57 * p + 0.08 * math.sin((t - tL) * 7)
        elif t < tW1:
            u = (t - tW0) / (tW1 - tW0)
            rot = 1.57 + (14 * math.pi + math.pi / 2) * (u ** 1.25)
        else:
            dt = t - tW1
            rot = math.pi + 0.18 * math.sin(dt * 6) * math.exp(-3 * dt)
        spinning = tW0 <= t < tW1
        blur = 8.0 if spinning else 0.0
        angJ = man_angles("jsandha", t, front=(0.3, 0.3), backa=(0.7, 0.2), head=0.4, legs=(0.25, -0.3),
                          hits=[(tW1, 1.2)])

        def draw_j(cr_):
            puppet(cr_, C.JSANDHA, cx, cy, sc, rot, flip=True, angles=angJ, blur=blur, rods=False)
        if t < tS:
            if spinning:
                u = (t - tW0) / (tW1 - tW0)
                w = (14 * math.pi + math.pi / 2) * 1.25 * max(u, 0.05) ** 0.25 / (tW1 - tW0)
                for g in (2, 1):
                    puppet(cr, C.JSANDHA, cx, cy, sc, rot - g * w / 30.0 * 1.5, flip=True, angles=angJ, blur=14,
                           alpha=0.2 * (3 - g) / 2, rods=False)
            draw_j(cr)
        else:
            q = ease((t - tS) / 0.8)
            fall = clamp((t - tS) / 1.3) ** 2
            pc.split_draw(cr, draw_j, (-280 * q, 700 * fall, -1.1 * q), (280 * q, 700 * fall, 1.1 * q), (cx, cy),
                          rot, sc, flip=True, seam_x=0.0)
    fl = 0.9 * math.exp(-3.5 * max(0, t - tS)) * (t > tS)
    n = 0
    if t > tW0:
        n = min(100, int(1 + 99 * clamp((t - tW0) / (tW1 - tW0)) ** 1.25))

    def ui(cr):
        if t < tL:
            small_line(cr, t, [("THE", t0), ("14TH", t0 + 0.08), ("NIGHT:", t0 + 0.16)], 245)
            big_word(cr, t, "HE TIRED", t0 + 0.4, 323, 160)
        elif t < tS:
            small_line(cr, t, [("BHIMA", tL), ("LIFTED", tL + 0.08), ("AND", tL + 0.16), ("WHIRLED", tL + 0.24),
                               ("HIM", tL + 0.32)], 245)
            if t > tW0:
                flip_counter(cr, t, W / 2, 400, f"x{n}", 160, RED)
        else:
            small_line(cr, t, [("AND", tS), ("BROKE", tS + 0.08), ("HIM", tS + 0.16)], 245)
            big_word(cr, t, "IN TWO", tS + 0.2, 323, 190, under=tS + 0.6)
    return dict(ui=ui, night=0.45 * (1 - 0.5 * fl), flash=fl)


def s_free(cr, t, tl, t0, t1):
    tO = F(tl, "j16", 0.30)
    cage_grid(cr, t, 86, open_t=tO, free_t=tO + 0.3, g=GRID2)
    raise_ = keyed(t, [(t0, 0.0), (tO - 0.3, 1.0)], 0.3, 1.5)
    ang = man_angles("krishna", t, front=(-0.3 - 1.9 * raise_, -0.55 + 0.4 * raise_), hits=[(tO, 0.5)])
    b, k, a = depth(t, t0, 0.4)
    glow(cr, 225, 960, 330, 0.55 * a * (0.8 + 0.2 * math.sin(t * 3)) + 0.3 * math.exp(-3 * max(0, t - tO)) * (t > tO))
    puppet(cr, C.KRISHNA, 210, man_y(0.82), 0.82 * k, bob_rot(t, 1), angles=ang, alpha=a, blur=b)
    ground(cr)
    n = int(86 * clamp((t - tO - 0.2) / 1.2))

    def ui(cr):
        head2(cr, t, "KRISHNA FREED ALL", t0 + 0.1, f"{max(n, 0)} KINGS", tO, big_size=170)
    return dict(ui=ui, flash=0.25 * math.exp(-3 * max(0, t - tO)) * (t > tO))


def s_mirror(cr, t, tl, t0, t1):
    tE = F(tl, "j17", 0.55)
    tSp = tE + 0.2
    # left: how he began, two halves joined; right: how he ended, the same seam coming apart
    j = ease((t - t0 - 0.25) / 0.4)
    baby_pair(cr, t, 280, 1560, 0.7, gap=150 * (1 - j))
    ang = man_angles("jsandha", t, front=(-0.4, -0.5))
    b, k, a = depth(t, t0 + 0.2, 0.5)

    def draw_j(cr_):
        puppet(cr_, C.JSANDHA, 800, man_y(0.86) - (k - 1) * 250, 0.86 * k, 0.0, angles=ang, rods=t < tSp, alpha=a,
               blur=b)
    q = ease((t - tSp) / 0.8) if t > tSp else 0.0
    fall = clamp((t - tSp) / 1.1) ** 2
    pc.split_draw(cr, draw_j, (-120 * q, 70 * fall, -0.16 * q), (150 * q, 70 * fall, 0.22 * q),
                  (800, man_y(0.86)), 0.0, 0.86, seam_x=0.0)
    ground(cr)
    fl = 0.55 * math.exp(-4 * max(0, t - tSp)) * (t > tSp)
    jt = t0 + 0.65

    def ui(cr):
        tag(cr, t, t0 + 0.3, "BORN", 280, 700, 40)
        tag(cr, t, tE, "ENDED", 800, 700, 40)
        head2(cr, t, "JOINED FROM TWO HALVES...", t0 + 0.1, "ENDED IN TWO", tE, big_size=170)
        if t > jt:
            red_ring(cr, 280, 1560 - 0.7 * 300, 170, 330, prog(t, jt, 0.4), 8, alpha=1 - prog(t, tE, 0.3))
    return dict(ui=ui, flash=fl)


def s_end(cr, t, tl, t0, t1):
    baby_pair(cr, t, 540, 1650, 0.5, gap=0)
    p = back(clamp((t - t0) / 0.4), 1.4)
    cr.save()
    cr.translate(540, 1000 + 80 * (1 - p))
    pc.paint_part(cr, "card", alpha=clamp(p))
    cr.restore()
    pc.rod(cr, 400, 1200, 380, H + 60, alpha=clamp(p))
    pc.rod(cr, 680, 1200, 700, H + 60, alpha=clamp(p))

    def ui(cr):
        a = clamp(p)
        yb = 1000 + 80 * (1 - p)
        draw_text(cr, "DID YOU KNOW", W / 2, 300, 66, INK, prog(t, t0, 0.2), anchor="ct")
        big_word(cr, t, "THIS STORY?", t0 + 0.12, 380, 160)
        for i, lab in enumerate(("YES", "NO")):
            bx = 540 - 175 + 350 * i
            cr.set_source_rgba(*INK, a)
            cr.set_line_width(7)
            cr.rectangle(bx - 118, yb - 38, 66, 66)
            cr.stroke()
            draw_text(cr, lab, bx - 32, yb - 5, 104, INK, a, anchor="lm")
        if t > t0 + 0.7:
            side = int((t - t0 - 0.7) / 0.9) % 2
            red_ring(cr, 540 - 175 + 350 * side + 20, yb - 5, 145, 85,
                     prog(t, t0 + 0.7 + 0.9 * int((t - t0 - 0.7) / 0.9), 0.35), 9)
    return dict(ui=ui)


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("j1", None, s_hook, {}),
    ("j2", None, s_two, {}),
    ("j3", None, s_text, {}),
    ("j4", None, s_king, {}),
    ("j5", None, s_mango, {}),
    ("j5", 0.52, s_split, {"z": (1.02, 1.08)}),
    ("j6", None, s_birth, {}),
    ("j7", None, s_thrown, {}),
    ("j8", None, s_jara, {}),
    ("j9", None, s_join, {"z": (1.0, 1.08)}),
    ("j10", None, s_name, {}),
    ("j11", None, s_kings, {}),
    ("j12", None, s_rehook, {"z": (1.0, 1.08)}),
    ("j13", None, s_three, {}),
    ("j13", 0.58, s_choose, {}),
    ("j14", None, s_days, {}),
    ("j15", None, s_final, {"z": (1.0, 1.06)}),
    ("j16", None, s_free, {}),
    ("j17", None, s_mirror, {}),
    ("j18", None, s_end, {}),
]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl, SHOTS)
    _, _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.05))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (540, 1060))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur): a whoosh on every cut, damaru beats for the puppet-show feel and the wrestling, pops as each
    piece lands, temple bell / conch / shimmer on the sacred beats, a dip of the music before each reveal."""
    st = starts(tl, SHOTS)
    ev = [(s, "whoosh", 0.45) for s in st[1:]]
    g = lambda bid, f: T(tl, bid, f)
    ev += [(0.0, "damaru", 0), (0.05, "bell", 0)]
    for w, f in (({"hi": "आंख", "kn": "ಕಣ್ಣು"}, 0.04), ({"hi": "हाथ", "kn": "ಕೈ"}, 0.28),
                 ({"hi": "पैर", "kn": "ಕಾಲು"}, 0.52)):
        ev.append((cue(tl, "j1", w, f), "pop", 0))
    tF = cue(tl, "j1", {"hi": "चेहरा", "kn": "ಮುಖ"}, 0.78)
    ev += [(tF - 0.3, "dip", 0.4), (tF, "hit", 0)]
    ev += [(g("j2", 0.30), "shimmer", 0), (g("j2", 0.70) - 0.3, "dip", 0.4), (g("j2", 0.70), "thud", 0),
           (g("j2", 0.70) + 0.05, "damaru", 0)]
    ev += [(g("j3", 0.22), "slam", 0), (g("j3", 0.45), "conch", 0), (g("j3", 0.72), "thud", 0)]
    ev += [(tl["j4"].start + 0.3 + 0.42 * i, "step", 0) for i in range(3)]
    ev += [(g("j4", 0.42) + 0.42 * i, "step", 0) for i in range(2)]
    ev += [(g("j4", 0.72), "creak", 0), (g("j4", 0.72) + 0.35, "tick", 0)]
    ev += [(g("j5", 0.14), "pop", 0), (g("j5", 0.26), "whoosh", 0.4), (g("j5", 0.66), "hit", 0),
           (g("j5", 0.80), "whoosh", 0.5)]
    ev += [(g("j6", 0.30), "pop", 0), (g("j6", 0.48), "pop", 0), (g("j6", 0.85) - 0.3, "dip", 0.4),
           (g("j6", 0.85), "sting", 0)]
    tT = g("j7", 0.35)
    ev += [(tT, "whoosh", 0.6), (tT + 0.75, "thud", 0), (tT + 0.87, "thud", 0), (tl["j7"].start, "hush", 0.25)]
    ev += [(tl["j8"].start + 0.3 + 0.5 * i, "step", 0) for i in range(4)]
    ev += [(g("j8", 0.12), "damaru", 0), (g("j8", 0.88) - 1.2, "riser", 1.2)]
    ev += [(tl["j9"].start + 0.35, "hit", 0), (tl["j9"].start + 0.4, "shimmer", 0), (g("j9", 0.50) - 0.3, "dip", 0.5),
           (g("j9", 0.50), "sting", 0), (g("j9", 0.50) + 0.05, "hit", 0), (g("j9", 0.50) + 1.35, "hit", 0)]
    ev += [(g("j10", 0.55) - 0.25, "thud", 0), (g("j10", 0.55), "bell", 0)]
    ev += [(g("j11", 0.12), "typing", g("j11", 0.48) - g("j11", 0.12)), (g("j11", 0.48), "ding", 0),
           (g("j11", 0.62), "slam", 0), (g("j11", 0.62) + 0.3, "thud", 0)]
    ev += [(tl["j12"].start - 0.35, "tick", 0), (tl["j12"].start - 0.3, "dip", 0.5), (tl["j12"].start, "sting", 0),
           (tl["j12"].start + 0.2, "heartbeat", 1.6)]
    ev += [(tl["j13"].start + 0.2 + 0.43 * i, "step", 0) for i in range(4)]
    ev += [(tl["j13"].start + 1.2 + 0.24 * i, "pop", 0) for i in range(3)]
    ev += [(g("j13", 0.80) - 0.3, "dip", 0.4), (g("j13", 0.80), "hit", 0)]
    b = tl["j14"]
    span = (b.end + 0.0 - (b.start + 0.4)) / 13
    ev += [(b.start + 0.4 + span * i, "damaru", 0) for i in range(13)]
    ev += [(g("j15", 0.0), "heartbeat", 1.5), (g("j15", 0.22), "whoosh", 0.5), (g("j15", 0.40), "riser", 1.0)]
    w0, w1 = g("j15", 0.40), g("j15", 0.74)
    ev += [(w0 + (w1 - w0) * i / 7, "whoosh", 0.35) for i in range(7)]
    ev += [(g("j15", 0.93) - 0.4, "dip", 0.6), (g("j15", 0.93), "slam", 0), (g("j15", 0.93) + 0.02, "hit", 0)]
    ev += [(g("j16", 0.30), "bell", 0), (g("j16", 0.30) + 0.3, "shimmer", 0), (g("j16", 0.10), "conch", 0)]
    ev += [(tl["j17"].start - 0.3, "dip", 0.5), (g("j17", 0.55) + 0.25, "hit", 0), (tl["j17"].start + 0.4, "bell", 0)]
    ev += [(tl["j18"].start, "pop", 0), (tl["j18"].start + 0.7, "ding", 0)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in ev]
