"""Krishna for the toon rig (toon_rig.py), Nov 2026: a medium shot from the waist up, drawn entirely in code.

Design (our own, respectful): blue skin, long wavy black hair, a gold band with a crest and a peacock feather,
Vaishnava tilak, almond eyes, gold kundala earrings, a collar necklace with a ruby pendant and a long bead chain,
gold armlets and kadas, a dark-blue uttariya with a gold border over his left shoulder, a yellow pitambar with a
red-orange waist sash. Background: a warm palace hall with an arched window, softly blurred.

  draw(cr, S)     one frame from a state dict S (see STATE); every part moves:
                  camera push / background parallax, breathing torso, head roll + 2.5D yaw/pitch, hair and
                  earrings with follow-through, eyes (gaze, blink, lids, smile squint), brows (raise, frown, worry,
                  skew), mouth (open / wide / round / teeth / smile / smirk), two arms with 3D hands
  ARM_POSES       gesture library (rest, point_up, explain, raise, offer, ...) for toon_rig.Track
  EXPRESSIONS     face presets (neutral, intrigue, explain, firm, serious, worried, knowing)
Body space: origin at the pit of the neck, y down; it sits at BODY on the 1080x1920 frame.
Head space: origin between the eyes; the head turns about its pivot HEAD_UP below that.
"""
import functools
import math

import cairo

import toon_rig as R
from toon_rig import INK, Part, TAU, clamp, clip, ellipse, lerp, mix, multiply, rgb, smooth, spath, stroke_taper

W, H = 1080, 1920
BODY = (540.0, 1000.0)
NECK_PIVOT = -160.0          # body y of the head pivot
HEAD_UP = 150.0              # eye line above the pivot (head space y of the pivot)
HEAD_S = 1.12                # head scale against the body
CHAR_S, CHAR_PIVOT = 1.14, 1080.0  # whole-character scale (framing: shoulders near the edges, sash in view)

# ------------------------------------------------------------------ palette
SKIN = (0.47, 0.57, 0.95)
SKIN_SH = (0.33, 0.39, 0.82)
SKIN_HL = (0.61, 0.71, 1.00)
SKIN_DEEP = (0.24, 0.26, 0.62)
SHADOW = (0.68, 0.69, 0.89)              # multiply tint for cast shadows
HAIR = (0.10, 0.095, 0.17)
HAIR_HL = (0.19, 0.22, 0.38)
HAIR_HL2 = (0.32, 0.37, 0.60)
GOLD = (0.98, 0.76, 0.24)
GOLD_SH = (0.78, 0.48, 0.12)
GOLD_HL = (1.0, 0.95, 0.66)
PITA = (1.0, 0.80, 0.20)
PITA_SH = (0.93, 0.58, 0.12)
PITA_HL = (1.0, 0.92, 0.52)
SASH = (0.87, 0.30, 0.17)
SASH_SH = (0.62, 0.16, 0.12)
SASH_HL = (0.98, 0.50, 0.30)
STOLE = (0.12, 0.18, 0.47)
STOLE_SH = (0.065, 0.09, 0.27)
STOLE_HL = (0.25, 0.36, 0.72)
RUBY = (0.86, 0.12, 0.22)
EMERALD = (0.08, 0.62, 0.44)
PEARL = (0.99, 0.97, 0.92)
WHITE = (0.985, 0.985, 1.0)
MOUTH = (0.20, 0.05, 0.12)
TONGUE = (0.88, 0.42, 0.52)
IRIS = (0.15, 0.09, 0.08)
IRIS_LO = (0.47, 0.30, 0.20)

# ------------------------------------------------------------------ poses and expressions

HAND_REST = dict(tw=60, tip=10, ci=0.55, cm=0.62, cr=0.68, cp=0.72, sp=0.0, to=-6, tf=66, tc=0.55)
ARM_POSES = {
    "rest": dict(sh=14, el=-36, fu=1.0, ff=0.8, ha=-30, **HAND_REST),
    # elbow angles stay on one side (forearm swings up across the body, never round the back): -180..0
    "point_up": dict(sh=12, el=-176, fu=0.96, ff=0.92, ha=-8, tw=-10, tip=0, ci=0.0, cm=0.96, cr=1.0, cp=1.0,
                     sp=0.0, to=-4, tf=74, tc=0.45),
    "explain": dict(sh=8, el=-140, fu=0.97, ff=0.6, ha=20, tw=-120, tip=30, ci=0.14, cm=0.18, cr=0.24, cp=0.30,
                    sp=0.55, to=34, tf=12, tc=0.10),
    "explain2": dict(sh=10, el=-124, fu=0.97, ff=0.64, ha=34, tw=-140, tip=26, ci=0.08, cm=0.1, cr=0.14, cp=0.2,
                     sp=0.8, to=44, tf=6, tc=0.06),
    "raise": dict(sh=14, el=-184, fu=0.96, ff=0.88, ha=-2, tw=-6, tip=0, ci=0.05, cm=0.03, cr=0.06, cp=0.10,
                  sp=0.40, to=30, tf=8, tc=0.10),
    "offer": dict(sh=14, el=-100, fu=0.97, ff=0.62, ha=26, tw=-150, tip=30, ci=0.12, cm=0.16, cr=0.22, cp=0.28,
                  sp=0.60, to=36, tf=10, tc=0.08),
    "heart": dict(sh=6, el=-150, fu=0.97, ff=0.62, ha=25, tw=-180, tip=0, ci=0.1, cm=0.12, cr=0.15, cp=0.2,
                  sp=0.2, to=30, tf=10, tc=0.1),
    "rest_l": dict(sh=13, el=-34, fu=1.0, ff=0.8, ha=-28, **HAND_REST),
    "low_l": dict(sh=12, el=-44, fu=1.0, ff=0.76, ha=-30, **HAND_REST),
}
EXPRESSIONS = {
    "neutral": dict(smile=0.30, smirk=0.0, lid=0.14, squint=0.05, b_raise=0.0, b_frown=0.0, b_worry=0.0, b_skew=0.0),
    "intrigue": dict(smile=0.18, smirk=0.12, lid=0.0, squint=0.0, b_raise=0.55, b_frown=0.0, b_worry=0.0,
                     b_skew=0.35),
    "explain": dict(smile=0.22, smirk=0.0, lid=0.06, squint=0.05, b_raise=0.18, b_frown=0.0, b_worry=0.0,
                    b_skew=0.0),
    "firm": dict(smile=0.0, smirk=0.0, lid=0.14, squint=0.12, b_raise=0.0, b_frown=0.65, b_worry=0.0, b_skew=0.0),
    "serious": dict(smile=0.08, smirk=0.0, lid=0.10, squint=0.06, b_raise=0.05, b_frown=0.32, b_worry=0.0,
                    b_skew=0.0),
    "worried": dict(smile=0.0, smirk=0.0, lid=0.0, squint=0.0, b_raise=0.2, b_frown=0.0, b_worry=0.7, b_skew=0.0),
    "knowing": dict(smile=0.92, smirk=0.45, lid=0.16, squint=0.42, b_raise=0.18, b_frown=0.0, b_worry=0.0,
                    b_skew=0.55),
}

STATE = dict(cam_s=1.0, cam_x=0.0, cam_y=0.0, bx=0.0, by=0.0, brot=0.0, breath=0.0,
             roll=0.0, yaw=0.0, pitch=0.0, hx=0.0, hy=0.0, roll_lag=0.0, yaw_lag=0.0, pitch_lag=0.0,
             blink=0.0, gx=0.0, gy=0.0, m_open=0.0, m_wide=0.0, m_round=0.0, m_teeth=0.0,
             ear_swing=0.0, feather_swing=0.0, t=0.0, arm_r=dict(ARM_POSES["rest"]), arm_l=dict(ARM_POSES["rest_l"]),
             **EXPRESSIONS["neutral"])

# ------------------------------------------------------------------ background: a warm palace hall, blurred

BG_W, BG_H, BG_K = 1320, 2340, 0.5


def _bg_far(cr):
    g = cairo.LinearGradient(0, 0, 0, BG_H)
    for o, c in ((0, (0.95, 0.87, 0.76)), (0.45, (0.93, 0.84, 0.70)), (0.75, (0.86, 0.72, 0.56)),
                 (1, (0.70, 0.54, 0.40))):
        g.add_color_stop_rgb(o, *c)
    cr.set_source(g)
    cr.paint()
    for x0 in (60, 1000):                                   # side panels: gold-framed niches with lamp glows
        cr.rectangle(x0, 520, 260, 820)
        rgb(cr, (0.90, 0.80, 0.66))
        cr.fill()
        cr.rectangle(x0 + 30, 560, 200, 740)
        rgb(cr, (0.84, 0.70, 0.52))
        cr.fill()
        spath(cr, [(x0 + 60, 1240, 1), (x0 + 60, 820), (x0 + 130, 700), (x0 + 200, 820), (x0 + 200, 1240, 1)])
        rgb(cr, (0.62, 0.42, 0.28))
        cr.fill()
        gl = cairo.RadialGradient(x0 + 130, 1120, 0, x0 + 130, 1120, 160)
        gl.add_color_stop_rgba(0, 1.0, 0.86, 0.50, 0.95)
        gl.add_color_stop_rgba(1, 1.0, 0.80, 0.45, 0.0)
        cr.set_source(gl)
        cr.arc(x0 + 130, 1120, 160, 0, TAU)
        cr.fill()
    cx, top, rad, bot = 660, 640, 330, 1680                 # the great arch window behind him

    def arch(cr, r=rad):
        cr.move_to(cx - r, bot)
        cr.line_to(cx - r, top)
        cr.arc(cx, top, r, math.pi, TAU)
        cr.line_to(cx + r, bot)
        cr.close_path()
    for r, c in ((rad + 70, (0.97, 0.91, 0.80)), (rad + 30, (0.90, 0.73, 0.40)), (rad + 16, (0.80, 0.64, 0.46))):
        arch(cr, r)
        rgb(cr, c)
        cr.fill()
    cr.save()
    arch(cr)
    cr.clip()
    g = cairo.LinearGradient(0, top - rad, 0, bot)
    for o, c in ((0, (0.55, 0.72, 0.93)), (0.45, (0.76, 0.87, 0.97)), (0.72, (0.99, 0.93, 0.80)),
                 (1, (0.98, 0.84, 0.62))):
        g.add_color_stop_rgb(o, *c)
    cr.set_source(g)
    cr.paint()
    for (x, y, rx, ry) in ((470, 520, 150, 60), (560, 470, 120, 70), (820, 600, 170, 55), (900, 560, 90, 50),
                           (420, 900, 130, 40), (880, 980, 160, 45)):
        ellipse(cr, x, y, rx, ry)
        rgb(cr, (1, 1, 1), 0.85)
        cr.fill()
    rgb(cr, (0.66, 0.74, 0.55))
    for x in range(330, 1000, 70):
        ellipse(cr, x, 1330 + 20 * math.sin(x), 60, 50)
        cr.fill()
    for col, dx in (((0.99, 0.88, 0.64), 0), ((0.97, 0.80, 0.52), 1)):   # distant golden palace
        rgb(cr, col)
        for (x, w_, h_) in ((520, 120, 200), (660, 170, 300), (800, 110, 180)):
            if dx:
                cr.rectangle(x + w_ * 0.1, 1300 - h_, w_ * 0.4, h_ + 60)
            else:
                cr.rectangle(x - w_ / 2, 1300 - h_, w_, h_ + 60)
                ellipse(cr, x, 1300 - h_, w_ * 0.42, w_ * 0.42)
            cr.fill()
    cr.restore()
    rgb(cr, (0.95, 0.88, 0.76))                             # balcony railing
    cr.rectangle(cx - rad - 20, 1500, 2 * rad + 40, 34)
    cr.fill()
    for x in range(cx - rad + 10, cx + rad, 52):
        spath(cr, [(x - 12, 1534), (x - 16, 1580), (x - 10, 1620), (x + 10, 1620), (x + 16, 1580), (x + 12, 1534)])
        rgb(cr, (0.93, 0.85, 0.72))
        cr.fill()
    cr.rectangle(cx - rad - 20, 1620, 2 * rad + 40, 40)
    rgb(cr, (0.90, 0.80, 0.66))
    cr.fill()
    g = cairo.LinearGradient(0, 1680, 0, BG_H)
    g.add_color_stop_rgb(0, 0.80, 0.63, 0.46)
    g.add_color_stop_rgb(1, 0.60, 0.42, 0.30)
    cr.rectangle(0, 1680, BG_W, BG_H - 1680)
    cr.set_source(g)
    cr.fill()
    gl = cairo.RadialGradient(cx, 1000, 50, cx, 1000, 900)  # warm sunlight from the arch
    gl.add_color_stop_rgba(0, 1.0, 0.95, 0.80, 0.55)
    gl.add_color_stop_rgba(1, 1.0, 0.90, 0.70, 0.0)
    cr.set_source(gl)
    cr.paint()


def _bg_near(cr):
    for x0 in (-30, BG_W - 175):                            # two carved pillars at the edges
        g = cairo.LinearGradient(x0, 0, x0 + 205, 0)
        g.add_color_stop_rgb(0, 0.86, 0.76, 0.62)
        g.add_color_stop_rgb(0.35, 0.99, 0.94, 0.84)
        g.add_color_stop_rgb(1, 0.80, 0.68, 0.52)
        cr.rectangle(x0 + 20, 0, 165, BG_H)
        cr.set_source(g)
        cr.fill()
        for y in (420, 470, 1650, 1700):
            cr.rectangle(x0 + 5, y, 195, 28)
            rgb(cr, (0.92, 0.72, 0.34))
            cr.fill()
        for y in range(560, 1600, 90):
            ellipse(cr, x0 + 102, y, 26, 34)
            rgb(cr, (0.90, 0.78, 0.60))
            cr.fill()
    spath(cr, [(120, -20, 1), (420, -20, 1), (360, 300), (260, 760), (200, 1040), (215, 1500), (160, 2000, 1),
               (60, 2000, 1), (110, 1400), (130, 1000), (120, 500)])   # a muted rose drape, tied with gold
    rgb(cr, (0.72, 0.40, 0.36))
    cr.fill()
    spath(cr, [(230, -20, 1), (420, -20, 1), (340, 360), (240, 820), (230, 600), (260, 300)])
    rgb(cr, (0.82, 0.52, 0.46))
    cr.fill()
    ellipse(cr, 180, 1030, 70, 26)
    rgb(cr, (0.95, 0.78, 0.40))
    cr.fill()
    cr.rectangle(1048, 0, 6, 520)                           # a brass lamp hanging on the right
    rgb(cr, (0.55, 0.40, 0.20))
    cr.fill()
    spath(cr, [(990, 540), (1050, 500), (1110, 540), (1090, 600), (1050, 620), (1010, 600)])
    rgb(cr, (0.85, 0.60, 0.25))
    cr.fill()
    gl = cairo.RadialGradient(1050, 560, 0, 1050, 560, 220)
    gl.add_color_stop_rgba(0, 1.0, 0.90, 0.55, 0.9)
    gl.add_color_stop_rgba(1, 1.0, 0.80, 0.40, 0.0)
    cr.set_source(gl)
    cr.arc(1050, 560, 220, 0, TAU)
    cr.fill()
    for (x, y, r_, c) in ((1150, 1820, 120, (0.36, 0.52, 0.34)), (1210, 1760, 100, (0.42, 0.58, 0.38)),
                          (1080, 1760, 90, (0.38, 0.55, 0.36))):
        ellipse(cr, x, y, r_, r_ * 0.8)
        rgb(cr, c)
        cr.fill()
    spath(cr, [(1060, 1880), (1250, 1880), (1230, 2100), (1080, 2100)])
    rgb(cr, (0.78, 0.52, 0.36))
    cr.fill()


@functools.lru_cache(maxsize=1)
def _bg_layers():
    out = []
    for fn, sigma in ((_bg_far, 7.0), (_bg_near, 13.0)):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(BG_W * BG_K), int(BG_H * BG_K))
        cr = cairo.Context(s)
        cr.scale(BG_K, BG_K)
        fn(cr)
        out.append(R.blur_surface(s, sigma))
    return out


FOCUS_Y = 760.0


def camera(cr, S):
    cr.translate(W / 2, FOCUS_Y)
    cr.scale(S["cam_s"], S["cam_s"])
    cr.translate(-(W / 2 + S["cam_x"]), -(FOCUS_Y + S["cam_y"]))


def background(cr, S):
    far, near = _bg_layers()
    for surf, par in ((far, 0.35), (near, 0.8)):
        cr.save()
        sc = 1 + (S["cam_s"] - 1) * par
        cr.translate(W / 2 - S["cam_x"] * par * 0.6, H / 2 - S["cam_y"] * par * 0.6)
        cr.scale(sc / BG_K, sc / BG_K)
        cr.translate(-BG_W * BG_K / 2, -BG_H * BG_K / 2)
        cr.set_source_surface(surf, 0, 0)
        cr.get_source().set_filter(cairo.FILTER_GOOD)
        cr.paint()
        cr.restore()
    cr.save()                                                # a soft warm glow behind the head (not a halo)
    camera(cr, S)
    hx, hy = BODY[0] + S["bx"], BODY[1] + NECK_PIVOT - HEAD_UP - 60
    g = cairo.RadialGradient(hx, hy, 0, hx, hy, 560)
    g.add_color_stop_rgba(0, 1.0, 0.96, 0.84, 0.55)
    g.add_color_stop_rgba(0.6, 1.0, 0.93, 0.76, 0.18)
    g.add_color_stop_rgba(1, 1.0, 0.90, 0.70, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ body

TORSO_R = [(74, -236), (76, -150), (80, -92), (94, -48), (132, -18), (198, 4), (258, 28), (300, 62), (324, 116),
           (322, 186), (304, 262), (290, 352), (276, 452), (256, 560), (242, 652), (248, 760), (258, 880),
           (264, 1040)]
TORSO = TORSO_R + [(-x, y) for x, y in reversed(TORSO_R)]
SHOULDER = (296.0, 112.0)
LU, LF, WRIST = 392.0, 330.0, 304.0
UPPER = [(-80, -34), (-90, 16), (-66, 72), (-10, 104), (66, 106), (146, 92), (226, 80), (306, 72), (364, 64),
         (398, 36), (408, 0), (394, -36), (340, -58), (264, -72), (190, -80), (110, -76), (40, -70), (-34, -62)]
FORE = [(-40, 0), (-26, 52), (36, 66), (118, 60), (214, 46), (288, 36), (322, 22), (328, -4), (314, -30),
        (246, -36), (150, -46), (52, -58), (-18, -52)]
HAND_SCALE = 1.62


def _bone(o, d, n, pts, fx=1.0):
    return [(o[0] + x * fx * d[0] + y * n[0], o[1] + x * fx * d[1] + y * n[1]) for x, y in pts]


def _dirs(s, theta):
    return (s * math.sin(theta), math.cos(theta)), (s * math.cos(theta), -math.sin(theta))


def arm_geom(s, A):
    """Joint positions and outlines of one arm (s=+1 his left / viewer's right, -1 his right)."""
    J = (s * SHOULDER[0], SHOULDER[1])
    tu = math.radians(A["sh"])
    du, nu = _dirs(s, tu)
    E = (J[0] + du[0] * LU * A["fu"], J[1] + du[1] * LU * A["fu"])
    tf = tu + math.radians(A["el"])
    df, nf = _dirs(s, tf)
    Wp = (E[0] + df[0] * WRIST * A["ff"], E[1] + df[1] * WRIST * A["ff"])
    th = tf + math.radians(A["ha"])
    dh, _ = _dirs(s, th)
    return dict(J=J, E=E, W=Wp, du=du, nu=nu, df=df, nf=nf, ang=math.atan2(dh[1], dh[0]),
                upper=_bone(J, du, nu, UPPER, A["fu"]), fore=_bone(E, df, nf, FORE, A["ff"]))


def _band(cr, o, d, n, x0, x1, y0, y1, sag, fx=1.0):
    """A bracelet across a limb between local x0..x1, curved like a ring seen from above."""
    top = [(x0, y0, 1), (x0 + sag, (y0 + y1) / 2), (x0, y1, 1)]
    bot = [(x1, y1, 1), (x1 + sag, (y0 + y1) / 2), (x1, y0, 1)]
    pts = _bone(o, d, n, [q[:2] for q in top + bot], fx)
    spath(cr, [p + ((1,) if q[2:] else ()) for p, q in zip(pts, top + bot)])


def gold_fill(cr, pathfn, x0, y0, x1, y1, lw=2.6):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    g.add_color_stop_rgb(0, *GOLD_HL)
    g.add_color_stop_rgb(0.35, *GOLD)
    g.add_color_stop_rgb(1, *GOLD_SH)
    cr.new_path()
    pathfn(cr)
    cr.set_source(g)
    cr.fill_preserve()
    rgb(cr, INK)
    cr.set_line_width(lw)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()


def gem(cr, x, y, rx, ry, col, rot=0.0, lw=2.0):
    ellipse(cr, x, y, rx + 3.5, ry + 3.5, rot)
    rgb(cr, GOLD_SH)
    cr.fill()
    g = cairo.RadialGradient(x - rx * 0.35, y - ry * 0.4, 0, x, y, max(rx, ry) * 1.2)
    g.add_color_stop_rgb(0, *mix(col, (1, 1, 1), 0.45))
    g.add_color_stop_rgb(0.5, *col)
    g.add_color_stop_rgb(1, *mix(col, (0, 0, 0), 0.45))
    ellipse(cr, x, y, rx, ry, rot)
    cr.set_source(g)
    cr.fill_preserve()
    rgb(cr, INK)
    cr.set_line_width(lw)
    cr.stroke()
    ellipse(cr, x - rx * 0.32, y - ry * 0.36, rx * 0.26, ry * 0.2, rot)
    rgb(cr, (1, 1, 1), 0.9)
    cr.fill()


def armlet(o, d, n, x0, fx=1.0, ws=(-78, 94)):
    def post(cr):
        p = lambda c: _band(c, o, d, n, x0, x0 + 28, ws[0] - 3, ws[1] + 3, 10, fx)
        cx, cy = _bone(o, d, n, [(x0 + 14, (ws[0] + ws[1]) / 2)], fx)[0]
        gold_fill(cr, p, cx - 50, cy - 30, cx + 50, cy + 30)
        _band(cr, o, d, n, x0 + 7, x0 + 11, ws[0] + 6, ws[1] - 4, 10, fx)
        rgb(cr, GOLD_HL, 0.9)
        cr.fill()
        mx, my = _bone(o, d, n, [(x0 + 24, (ws[0] + ws[1]) / 2 - 6)], fx)[0]
        dia = [(mx, my - 24, 1), (mx + 16, my), (mx, my + 24, 1), (mx - 16, my)]
        gold_fill(cr, lambda c: spath(c, dia), mx - 15, my - 22, mx + 15, my + 22, 2.2)
        gem(cr, mx, my, 6.5, 8.0, EMERALD, lw=1.6)
    return post


def kada(o, d, n, fx=1.0):
    def post(cr):
        p = lambda c: _band(c, o, d, n, 262, 298, -42, 42, 8, fx)
        cx, cy = _bone(o, d, n, [(280, 0)], fx)[0]
        gold_fill(cr, p, cx - 40, cy - 30, cx + 40, cy + 30, 2.6)
        _band(cr, o, d, n, 268, 273, -36, 36, 8, fx)
        rgb(cr, GOLD_HL, 0.95)
        cr.fill()
        _band(cr, o, d, n, 288, 292, -36, 36, 8, fx)
        rgb(cr, GOLD_SH, 0.9)
        cr.fill()
    return post


def torso_shade(S):
    def f(cr):
        for s in (-1, 1):                                    # shadows under the pecs and the collarbones
            multiply(cr, lambda c: spath(c, [(s * 8, 300), (s * 120, 338), (s * 226, 302), (s * 286, 226),
                                             (s * 280, 290), (s * 220, 342), (s * 120, 380), (s * 10, 346)]),
                     SHADOW, 0.95)
            multiply(cr, lambda c: spath(c, [(s * 60, -24), (s * 150, 6), (s * 250, 36), (s * 250, 66),
                                             (s * 150, 46), (s * 60, 14)]), SHADOW, 0.5)
        multiply(cr, lambda c: spath(c, [(-50, 390), (50, 390), (44, 700), (0, 720), (-44, 700)]), SHADOW, 0.22)
        for s in (-1, 1):
            stroke_taper(cr, [(s * 16, 298), (s * 118, 334), (s * 214, 304), (s * 270, 236)], 4.4, prof="both")
            stroke_taper(cr, [(s * 34, 8), (s * 120, 22), (s * 226, 40)], 3.0, prof="both", color=SKIN_DEEP)
            stroke_taper(cr, [(s * 12, 452), (s * 56, 446), (s * 86, 436)], 2.6, prof="both", color=SKIN_DEEP)
            stroke_taper(cr, [(s * 12, 550), (s * 54, 546), (s * 80, 538)], 2.4, prof="both", color=SKIN_DEEP)
            stroke_taper(cr, [(s * 232, 420), (s * 212, 520), (s * 184, 640)], 2.8, prof="both", color=SKIN_DEEP)
            stroke_taper(cr, [(s * 56, -170), (s * 40, -90), (s * 16, -16)], 2.8, prof="both", color=SKIN_DEEP)
        stroke_taper(cr, [(0, 118), (0, 200), (0, 264)], 2.6, prof="both", color=SKIN_DEEP)
        stroke_taper(cr, [(0, 392), (0, 500), (0, 622)], 2.2, prof="both", color=SKIN_DEEP)
        stroke_taper(cr, [(-9, 664), (0, 674), (9, 664)], 2.6, prof="both")
        stroke_taper(cr, [(-9, -112), (0, -104), (9, -112)], 2.4, prof="both", color=SKIN_DEEP)
        g = cairo.RadialGradient(-130, 190, 0, -130, 190, 160)   # a soft sheen on the lit pec
        g.add_color_stop_rgba(0, 1, 1, 1, 0.16)
        g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
        cr.set_source(g)
        cr.paint()
        cr.save()                                                 # light falls off toward the lower right
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        g = cairo.LinearGradient(-200, 100, 260, 760)
        g.add_color_stop_rgba(0, 1, 1, 1, 0)
        g.add_color_stop_rgba(1, *SHADOW, 0.9)
        cr.set_source(g)
        cr.paint()
        cr.restore()
    return f


def necklace(cr, S):
    chain = [(-100, -34), (-82, 120), (-42, 292), (0, 352), (42, 292), (82, 120), (100, -34)]   # long bead chain
    stroke_taper(cr, chain, 8.0, prof="flat")
    stroke_taper(cr, chain, 4.4, prof="flat", color=GOLD)
    pts = R.sample(chain, False, 3.0)
    for i in range(6, len(pts) - 6, 9):
        x, y = pts[i]
        cr.arc(x, y, 5.6, 0, TAU)
        rgb(cr, INK)
        cr.fill()
        cr.arc(x, y, 3.9, 0, TAU)
        rgb(cr, GOLD if i % 18 else RUBY)
        cr.fill()
        cr.arc(x - 1.3, y - 1.3, 1.4, 0, TAU)
        rgb(cr, GOLD_HL)
        cr.fill()
    drop = [(0, 352, 1), (14, 372), (0, 402, 1), (-14, 372)]
    gold_fill(cr, lambda c: spath(c, drop), -14, 352, 14, 400, 2.2)
    gem(cr, 0, 375, 5, 7, EMERALD, lw=1.4)
    top = [(-92, -44, 1), (-56, 4), (0, 28), (56, 4), (92, -44, 1)]          # collar with the ruby pendant
    bot = [(98, -26, 1), (58, 26), (0, 50), (-58, 26), (-98, -26, 1)]
    gold_fill(cr, lambda c: spath(c, top + bot), -60, -40, 60, 48, 2.8)
    pts = R.sample([(-90, -34), (-56, 15), (0, 39), (56, 15), (90, -34)], False, 3.0)
    for i in range(3, len(pts) - 3, 7):
        x, y = pts[i]
        cr.arc(x, y, 3.2, 0, TAU)
        rgb(cr, GOLD_SH)
        cr.fill()
        cr.arc(x - 0.8, y - 0.9, 1.4, 0, TAU)
        rgb(cr, GOLD_HL)
        cr.fill()
    for dx in (-14, 0, 14):
        y = 94 + (8 if dx == 0 else 0)
        cr.arc(dx, y, 5.4, 0, TAU)
        rgb(cr, INK)
        cr.fill()
        cr.arc(dx, y, 4.0, 0, TAU)
        rgb(cr, PEARL)
        cr.fill()
    pend = [(0, 42, 1), (22, 58), (18, 82), (0, 94, 1), (-18, 82), (-22, 58)]
    gold_fill(cr, lambda c: spath(c, pend), -22, 42, 22, 94, 2.4)
    gem(cr, 0, 68, 11, 14, RUBY, lw=1.8)


def pitambar_parts(S):
    def cloth(c):
        spath(c, [(-272, 690, 1), (-140, 708), (0, 716), (140, 708), (272, 690, 1), (298, 820), (312, 1060, 1),
                  (-312, 1060, 1), (-298, 820)])

    def cloth_shade(cr):
        for x0, x1 in ((-210, -250), (-30, -50), (60, 50), (160, 200), (236, 284)):
            multiply(cr, lambda c: spath(c, [(x0, 730), (x0 + 22, 900), (x1 + 26, 1060), (x1 - 8, 1060),
                                             (x0 - 12, 880)]), (0.96, 0.80, 0.70), 0.9)
            stroke_taper(cr, [(x0, 740), (x0 + 6, 880), (x1, 1060)], 2.6, prof="end", color=PITA_SH)
        multiply(cr, lambda c: spath(c, [(-310, 720), (0, 748), (310, 720), (310, 770), (0, 800), (-310, 770)]),
                 (0.92, 0.74, 0.62), 1.0)

    def sash(c):
        spath(c, [(-282, 662, 1), (-130, 684), (0, 690), (130, 684), (282, 662, 1), (286, 722, 1), (130, 744),
                  (0, 752), (-130, 744), (-286, 722, 1)])

    def sash_shade(cr):
        for y0 in (676, 732):
            stroke_taper(cr, [(-290, y0 - 4), (-130, y0 + 16), (0, y0 + 22), (130, y0 + 16), (290, y0 - 4)], 7.0,
                         prof="flat", color=GOLD)
        for x in range(-250, 270, 46):
            stroke_taper(cr, [(x, 694), (x + 16, 712), (x + 8, 732)], 2.4, prof="both", color=SASH_SH)

    def tails(c):
        spath(c, [(-118, 742, 1), (-82, 744), (-70, 820), (-80, 940), (-96, 1060, 1), (-150, 1060, 1), (-140, 930),
                  (-136, 820)])
        spath(c, [(-70, 744, 1), (-40, 742), (-30, 800), (-12, 900), (6, 1060, 1), (-44, 1060, 1), (-58, 900),
                  (-70, 810)])

    def tails_shade(cr):
        stroke_taper(cr, [(-108, 770), (-108, 880), (-122, 1040)], 3.0, prof="both", color=SASH_SH)
        stroke_taper(cr, [(-48, 770), (-40, 880), (-24, 1040)], 2.6, prof="both", color=SASH_SH)

    def knot(c):
        spath(c, [(-128, 690), (-96, 670), (-58, 676), (-40, 704), (-54, 742), (-96, 756), (-126, 734)])

    def knot_shade(cr):
        stroke_taper(cr, [(-116, 700), (-90, 712), (-70, 736)], 2.8, prof="both", color=SASH_SH)
        stroke_taper(cr, [(-100, 680), (-78, 690), (-56, 694)], 2.4, prof="both", color=SASH_HL)
    return [Part(cloth, PITA, (PITA_SH, PITA_HL), (16, 6, 6, 5), shade=cloth_shade),
            Part(sash, SASH, (SASH_SH, None), (0, 8, 0, 0), shade=sash_shade),
            Part(tails, SASH, (SASH_SH, SASH_HL), (10, 4, 5, 3), shade=tails_shade),
            Part(knot, SASH, (SASH_SH, SASH_HL), (8, 6, 5, 4), shade=knot_shade)]


def _edge_ripple(pts, amp, freq, phase):
    n = len(pts)
    out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        k = amp * math.sin(freq * i / max(1, n - 1) * TAU + phase)
        out.append((x - dy / ln * k, y + dx / ln * k))
    return out


STOLE_C = [(332, 34), (268, 166), (180, 326), (76, 478), (-36, 606), (-126, 712), (-168, 790)]
STOLE_W = (220, 198, 170, 146, 128, 116, 110)


def stole_front_part(S):
    left, right = R.offset_band(STOLE_C, STOLE_W, 4.0)
    L = _edge_ripple(left[::12] + [left[-1]], 5.0, 2.2, 0.4)
    Rr = _edge_ripple(right[::12] + [right[-1]], 4.0, 2.6, 1.3)
    outline = [L[0] + (1,)] + L[1:-1] + [L[-1] + (1,), Rr[-1] + (1,)] + Rr[-2:0:-1] + [Rr[0] + (1,)]

    def path(c):
        spath(c, outline)

    def shade(cr):
        for (x, y, r_, a) in ((200, 230, 150, 0.55), (60, 450, 130, 0.42), (-80, 640, 110, 0.38)):
            gl = cairo.RadialGradient(x - 40, y - 20, 0, x - 40, y - 20, r_)
            gl.add_color_stop_rgba(0, *STOLE_HL, a)
            gl.add_color_stop_rgba(1, *STOLE_HL, 0.0)
            cr.set_source(gl)
            cr.paint()
        # tension folds running down the cloth, each with a lit edge beside it
        C = R.sample(STOLE_C, False, 4.0)
        for k, (u0, u1, off, w) in enumerate(((0.05, 0.85, -0.18, 3.4), (0.15, 0.95, 0.12, 3.0), (0.3, 0.9, 0.34, 2.6))):
            pts = []
            for u in (u0, (u0 + u1) / 2, u1):
                i = int(u * (len(C) - 1))
                lx, ly = left[min(i, len(left) - 1)]
                rx, ry = right[min(i, len(right) - 1)]
                f = 0.5 + off + 0.05 * math.sin(u * 7 + k)
                pts.append((lx + (rx - lx) * f, ly + (ry - ly) * f))
            stroke_taper(cr, pts, w, prof="both", color=STOLE_SH)
            stroke_taper(cr, [(x - 6, y - 3) for x, y in pts], w * 0.7, prof="both", color=STOLE_HL, alpha=0.7)
        # gold border along the lower edge (with a dotted motif)
        inner = []
        for (x, y), (cx, cy) in zip(L, R.sample(STOLE_C, False, 4.0)[::12] + [STOLE_C[-1]]):
            k = 14 / (math.hypot(x - cx, y - cy) or 1)
            inner.append((x + (cx - x) * k, y + (cy - y) * k))
        stroke_taper(cr, inner, 11.0, prof="flat", color=GOLD)
        stroke_taper(cr, inner, 2.2, prof="flat", color=GOLD_SH)
        for i, (x, y) in enumerate(R.sample(inner, False, 22.0)):
            cr.arc(x, y, 2.2, 0, TAU)
            rgb(cr, GOLD_SH if i % 2 else (0.9, 0.2, 0.2))
            cr.fill()
        multiply(cr, lambda c: spath(c, [(330, 30), (360, 80), (270, 180), (230, 130)]), (0.6, 0.6, 0.8), 0.7)
    return Part(path, STOLE, (STOLE_SH, None), (16, 8, 0, 0), shade=shade, cast=(10, 16, SHADOW, 1.0), lw=4.4)


def stole_back(cr, S):
    def path(c):
        spath(c, [(258, -14), (346, 8), (414, 110), (436, 380), (448, 760), (466, 1060, 1), (336, 1060, 1),
                  (344, 760), (334, 380), (312, 150)])

    def shade(c):
        stroke_taper(c, [(386, 200), (404, 520), (410, 900)], 3.0, color=STOLE_SH)
        stroke_taper(c, [(376, 220), (392, 520), (398, 900)], 2.0, color=STOLE_HL, alpha=0.6)
    R.ink(cr, [Part(path, STOLE, (STOLE_SH, STOLE_HL), (16, 8, 8, 6), shade=shade)], lw=4.4)


def body_parts(S):
    """The skin-and-cloth ink group: torso, pitambar, upper arms, stole, forearms, hands (back to front)."""
    arms = {s: arm_geom(s, S["arm_l" if s > 0 else "arm_r"]) for s in (1, -1)}
    form = (12, 6, 5, 4)
    tones = (SKIN_SH, SKIN_HL)
    parts = [Part(lambda c: spath(c, TORSO), SKIN, tones, (18, 6, 6, 5), shade=torso_shade(S),
                  post=lambda c: necklace(c, S))]
    parts += pitambar_parts(S)
    for s in (-1, 1):
        g = arms[s]
        A = S["arm_l" if s > 0 else "arm_r"]
        mask = [(s * 262, 40, 46), (s * 214, 30, 30)]
        parts.append(Part(lambda c, g=g: spath(c, g["upper"]), SKIN, tones, form, masks=mask,
                          shade=lambda c, g=g, s=s: _upper_shade(c, g, s),
                          post=armlet(g["J"], g["du"], g["nu"], 150, A["fu"])))
        if s == 1:
            parts.append(stole_front_part(S))
    for s in (1, -1):
        g = arms[s]
        A = S["arm_l" if s > 0 else "arm_r"]
        parts.append(Part(lambda c, g=g: spath(c, g["fore"]), SKIN, tones, form, masks=[(g["E"][0], g["E"][1], 54)],
                          shade=lambda c, g=g: _fore_shade(c, g), cast=(8, 12, SHADOW, 0.9)))
        hp = R.hand_parts(g["W"][0], g["W"][1], g["ang"], s, A, HAND_SCALE, SKIN, tones, (7, 4, 3, 2.5),
                          post=kada(g["E"], g["df"], g["nf"], A["ff"]))
        for p in hp:
            p.masks = list(p.masks) + [(g["W"][0], g["W"][1], 34)]
        parts += hp
    return parts, arms


def _upper_shade(cr, g, s):
    o, d, n = g["J"], g["du"], g["nu"]
    stroke_taper(cr, _bone(o, d, n, [(30, 84), (100, 76), (170, 44)]), 3.0, prof="both", color=SKIN_DEEP)
    stroke_taper(cr, _bone(o, d, n, [(250, -62), (320, -50), (376, -24)]), 2.6, prof="both", color=SKIN_DEEP)


def _fore_shade(cr, g):
    o, d, n = g["E"], g["df"], g["nf"]
    stroke_taper(cr, _bone(o, d, n, [(10, 36), (90, 46), (180, 30)]), 2.6, prof="both", color=SKIN_DEEP)


# ------------------------------------------------------------------ head

FACE = [(-136, -150), (-149, -80), (-151, -20), (-146, 36), (-135, 86), (-116, 134), (-90, 164), (-56, 188),
        (-24, 202), (0, 205), (24, 202), (56, 188), (90, 164), (116, 134), (135, 86), (146, 36), (151, -20),
        (149, -80), (136, -150), (76, -206), (0, -218), (-76, -206)]
EAR = [(140, -18), (160, -30), (178, -14), (180, 20), (170, 50), (154, 70), (140, 60)]
def _rev(pts):
    return list(reversed(pts))


def _hair_back_geom():
    rs = [(30, -306), (150, -284), (234, -216), (264, -124), (266, -30), (258, 50), (274, 140), (296, 240),
          (306, 320)]
    right, s1 = R.lock_edge(rs, 5, 20, lean=0.9, side=1, seed=3, sharp=False, var=0.35)
    bottom, s2 = R.lock_edge([(306, 320), (318, 420), (236, 430), (170, 370), (90, 284), (0, 254), (-90, 284),
                              (-170, 370), (-236, 430), (-318, 420), (-306, 320)], 7, 40, lean=0.35, side=1, seed=4,
                             var=0.35)
    left, s3 = R.lock_edge([(-x, y) for x, y in rs], 5, 20, lean=0.9, side=-1, seed=5, sharp=False, var=0.35)
    pts = right + bottom[1:] + _rev(left)[1:-1]
    strands = s1 + s3 + [
        [(-150, -250), (-226, -170), (-246, -60), (-236, 40), (-256, 140), (-280, 240), (-298, 330)],
        [(150, -250), (224, -170), (244, -60), (234, 40), (252, 140), (274, 240), (296, 340)],
        [(-80, -282), (-170, -226), (-214, -120)], [(80, -282), (170, -226), (212, -120)]]
    return pts, strands


def _hair_cap_geom():
    top, s1 = R.lock_edge([(-178, -50), (-214, -116), (-220, -176), (-198, -234), (-142, -278), (-60, -302),
                           (20, -306), (100, -294), (166, -264), (208, -214), (220, -160), (214, -110), (178, -50)],
                          6, 10, lean=0.5, side=1, seed=7, var=0.3, sharp=False)
    rbang, s2 = R.lock_edge([(178, -50), (150, -66), (124, -94), (90, -118), (50, -134), (0, -144)], 2, 22,
                            lean=-0.7, side=1, seed=8)
    lbang, s3 = R.lock_edge([(0, -144), (-50, -134), (-90, -118), (-124, -94), (-150, -66), (-178, -50)], 2, 22,
                            lean=0.7, side=1, seed=9)
    pts = top + rbang[1:-1] + [(0, -144, 1)] + lbang[1:-1]
    strands = [st for st in s1] + [
        [(6, -156), (60, -168), (124, -150), (178, -104)], [(12, -190), (90, -208), (166, -172), (206, -116)],
        [(-6, -156), (-60, -168), (-124, -150), (-180, -104)], [(-12, -192), (-92, -210), (-168, -174), (-208, -118)]]
    return pts, strands


HAIR_BACK, BACK_STRANDS = _hair_back_geom()
HAIR_CAP, CAP_STRANDS = _hair_cap_geom()
FRONT_LOCKS = [  # (centre line, widths): curling locks in front of the ears
    ([(150, -92), (158, -36), (154, 24), (142, 76), (122, 116), (104, 134)], (34, 30, 24, 16, 7, 0)),
    ([(-152, -90), (-162, -30), (-158, 30), (-146, 80), (-130, 112), (-112, 126)], (34, 30, 24, 15, 6, 0)),
]


def _lag(pts, d_roll, d_x=0.0, y0=-80.0, y1=380.0, piv=(0.0, HEAD_UP)):
    """Follow-through: lower hair points lag behind the head (rotated back by the roll difference)."""
    out = []
    for q in pts:
        w = smooth((q[1] - y0) / (y1 - y0))
        a = d_roll * w * 1.3
        ca, sa = math.cos(a), math.sin(a)
        x, y = q[0] - piv[0], q[1] - piv[1]
        nq = (piv[0] + x * ca - y * sa + d_x * w, piv[1] + x * sa + y * ca)
        out.append(nq + ((1,) if R._corner(q) else ()))
    return out


def head_frame(cr, S):
    cr.translate(0, NECK_PIVOT + S["hy"])
    cr.rotate(S["roll"])
    cr.scale(HEAD_S, HEAD_S)
    cr.translate(S["hx"], -HEAD_UP)


def hair_back(cr, S):
    cr.save()
    head_frame(cr, S)
    P = R.Head25D(S["yaw_lag"], S["pitch_lag"])
    dr = S["roll_lag"] - S["roll"]
    pts = P.pts(_lag(HAIR_BACK, dr), dz=-70, surf=False)

    def shade(c):
        for st in BACK_STRANDS:
            stroke_taper(c, P.pts(_lag(st, dr), dz=-70, surf=False), 4.2, prof="both", color=HAIR_HL)
    R.ink(cr, [Part(lambda c: spath(c, pts), HAIR, shade=shade)], lw=4.4)
    cr.restore()


def _mouth_geom(S):
    o, w, r = S["m_open"], S["m_wide"], S["m_round"]
    sm, sk = S["smile"], S["smirk"]
    hw = 33 * (1 + 0.22 * w - 0.36 * r + 0.14 * sm)
    base = 106
    cl = base - sm * 8 + o * 5 + sk * 3
    crr = base - sm * 8 + o * 5 - sk * 7
    up = base - 1 - o * 6 - r * 2 + sm * 1.5
    lo = base + 2 + o * 40 * (1 - 0.28 * max(0, w)) + r * 3
    bul = r * 0.22
    U = [(-hw, cl), (-hw * (0.55 + bul), lerp(cl, up, 0.8) - r * 3), (0, up),
         (hw * (0.55 + bul), lerp(crr, up, 0.8) - r * 3), (hw, crr)]
    L = [(-hw, cl), (-hw * (0.6 + bul), lerp(cl, lo, 0.82)), (0, lo), (hw * (0.6 + bul), lerp(crr, lo, 0.82)),
         (hw, crr)]
    return U, L, o


def draw_mouth(cr, S, P):
    U0, L0, o = _mouth_geom(S)
    U = P.pts(U0, dz=14)
    L = P.pts(L0, dz=14)
    if o > 0.035:
        def opening(c):
            spath(c, [U[0] + (1,)] + U[1:-1] + [U[-1] + (1,)] + L[-2:0:-1], closed=True)
        cr.new_path()
        opening(cr)
        rgb(cr, MOUTH)
        cr.fill()
        with clip(cr, opening):
            th = 10 * S["m_teeth"] * clamp(o * 3.5)
            if th > 0.5:
                spath(cr, U + [(q[0], q[1] + th) for q in reversed(U)], closed=True)
                rgb(cr, WHITE)
                cr.fill()
            if o > 0.22:
                ellipse(cr, L[2][0], L[2][1] + 2, abs(U[-1][0] - U[0][0]) * 0.33, 4 + 14 * o)
                rgb(cr, TONGUE)
                cr.fill()
        stroke_taper(cr, U, 4.8, prof=(0.45, 1.0, 0.85, 1.0, 0.45))
        stroke_taper(cr, L, 3.2, prof=(0.4, 0.9, 1.0, 0.9, 0.4))
        lo_y = L[2][1]
    else:
        stroke_taper(cr, U, 4.6, prof=(0.25, 0.9, 1.0, 0.9, 0.25))
        lo_y = U[2][1] + 6
    cx = U[2][0]                                              # lower-lip shade and smile dimples
    lip = P.pts([(-14, 0), (0, 2), (14, 0)], dz=12)
    stroke_taper(cr, [(q[0] - lip[1][0] + cx, q[1] - lip[1][1] + lo_y + 15) for q in lip], 3.2, color=SKIN_DEEP,
                 alpha=0.8)
    if S["smile"] > 0.3:
        a = clamp((S["smile"] - 0.3) * 2)
        for k, q in ((-1, U[0]), (1, U[-1])):
            stroke_taper(cr, [(q[0] - k * 2, q[1] - 8), (q[0] + k * 5, q[1] - 1), (q[0] + k * 3, q[1] + 7)], 3.0,
                         alpha=a)


def draw_eye(cr, S, P, s):
    c = clamp(S["blink"] + S["lid"])
    sq = S["squint"]
    U0 = [(26, 7), (36, -8), (57, -18), (81, -18), (99, -11), (108, -6)]
    L0 = [(26, 7), (45, 14), (67, 15), (89, 9), (108, -6)]
    Lsq = [(26, 7), (45, 8), (67, 6), (89, 1), (108, -6)]
    L1 = [(lerp(a[0], b[0], sq), lerp(a[1], b[1], sq)) for a, b in zip(L0, Lsq)]
    Lc = [L1[0], L1[1], ((L1[1][0] + L1[2][0]) / 2, (L1[1][1] + L1[2][1]) / 2 - 1), L1[2], L1[3], L1[4]]
    U1 = [(lerp(a[0], b[0], c), lerp(a[1], b[1], c) - 1.5 * c) for a, b in zip(U0, Lc)]
    m = lambda pts: [(s * x, y) for x, y in pts]
    U = P.pts(m(U1), dz=-4)
    L = P.pts(m(L1), dz=-4)

    def opening(cr_):
        spath(cr_, [U[0] + (1,)] + U[1:-1] + [U[-1] + (1,)] + L[-2:0:-1], closed=True)
    if c < 0.97:
        cr.new_path()
        opening(cr)
        rgb(cr, WHITE)
        cr.fill()
        with clip(cr, opening):
            gx, gy = S["gx"], S["gy"]
            ix, iy = s * 66 + gx * 16, 1 + gy * 7
            px, py = P.p(ix, iy, -2)
            sx = P.sx(ix, iy, -2)
            ry = 18.5
            g = cairo.RadialGradient(px, py + 7, 2, px, py, ry * 1.1)
            g.add_color_stop_rgb(0, *IRIS_LO)
            g.add_color_stop_rgb(0.75, *IRIS)
            g.add_color_stop_rgb(1, 0.06, 0.04, 0.05)
            ellipse(cr, px, py, ry * sx, ry)
            cr.set_source(g)
            cr.fill()
            ellipse(cr, px, py, 8.6 * sx, 8.8)
            rgb(cr, (0.03, 0.02, 0.04))
            cr.fill()
            ellipse(cr, px - 6 * sx, py - 7, 5.6 * sx, 5.4)
            rgb(cr, (1, 1, 1))
            cr.fill()
            ellipse(cr, px + 6.5 * sx, py + 6.5, 2.3 * sx, 2.3)
            rgb(cr, (1, 1, 1), 0.85)
            cr.fill()
            spath(cr, U + [(q[0], q[1] + 8) for q in reversed(U)], closed=True)     # lid shadow on the eyeball
            cr.save()
            cr.set_operator(cairo.OPERATOR_MULTIPLY)
            rgb(cr, (0.72, 0.74, 0.92))
            cr.fill()
            cr.restore()
        stroke_taper(cr, L[1:], 2.4, prof=(0.2, 0.8, 1.0, 0.6))
    fl = P.pts(m([(115, -10)]), dz=-6)[0]                    # upper lash line with a flick at the outer corner
    stroke_taper(cr, U + [fl], 7.2, prof=(0.35, 0.75, 1.0, 1.0, 0.9, 0.15))
    cz = P.pts(m([(40, -27 + 6 * c), (64, -34 + 8 * c), (92, -26 + 7 * c)]), dz=-2)
    stroke_taper(cr, cz, 2.6, prof="both", color=SKIN_DEEP)


def draw_brow(cr, S, P, s):
    r = S["b_raise"] + S["b_skew"] * (0.6 if s > 0 else -0.25)
    f, wo = S["b_frown"], S["b_worry"]
    pts = [(20 - 5 * f, -40 - 12 * r + 11 * f - 13 * wo), (52, -54 - 13 * r + 4 * f - 6 * wo),
           (88, -59 - 12 * r - 2 * f + 1 * wo), (122, -47 - 8 * r - 3 * f + 4 * wo)]
    pts = P.pts([(s * x, y) for x, y in pts], dz=2)
    stroke_taper(cr, pts, 17.0, prof=(0.55, 1.0, 0.95, 0.72, 0.18), color=HAIR, step=2.0, caps=False)


def draw_nose(cr, S, P):
    multiply(cr, lambda c: spath(c, [P.p(9, 2, 12), P.p(18, 28, 24), P.p(22, 48, 34), P.p(12, 60, 34),
                                     P.p(26, 56, 24), P.p(28, 32, 16), P.p(18, 4, 8)]), SHADOW, 0.9)
    multiply(cr, lambda c: ellipse(c, *P.p(4, 69, 26), 20, 6), SHADOW, 0.9)
    stroke_taper(cr, [P.p(13, 10, 12), P.p(18, 30, 22), P.p(23, 48, 32), P.p(17, 60, 34), P.p(4, 63, 34)], 3.6,
                 prof=(0.1, 0.5, 0.9, 1.0, 0.35))
    stroke_taper(cr, [P.p(-18, 52, 26), P.p(-13, 60, 30), P.p(-3, 63, 32)], 2.8, prof="both")


def draw_tilak(cr, S, P):
    u = [P.p(-11, -124, 6), P.p(-10, -72, 6), P.p(-7, -42, 6), P.p(0, -35, 6), P.p(7, -42, 6), P.p(10, -72, 6),
         P.p(11, -124, 6)]
    stroke_taper(cr, u, 9.5, prof="flat", color=INK)
    stroke_taper(cr, u, 6.2, prof="flat", color=WHITE)
    stroke_taper(cr, [P.p(0, -122, 6), P.p(0, -84, 6), P.p(0, -50, 6)], 5.2, prof=(0.6, 1, 1, 0.5),
                 color=(0.90, 0.20, 0.12))


def face_shade(S, P, cap):
    def f(cr):
        multiply(cr, lambda c: spath(c, [(q[0] + 5, q[1] + 22) + q[2:] for q in cap]), SHADOW, 1.0)
        for s in (-1, 1):
            ex, ey = P.p(s * 64, -24, -4)
            g = cairo.RadialGradient(ex, ey, 0, ex, ey, 56)
            g.add_color_stop_rgba(0, *SKIN_SH, 0.45)
            g.add_color_stop_rgba(1, *SKIN_SH, 0.0)
            cr.set_source(g)
            cr.paint()
            bx, by = P.p(s * 96, 58, 0)
            g = cairo.RadialGradient(bx, by, 0, bx, by, 38)
            g.add_color_stop_rgba(0, 0.84, 0.52, 0.86, 0.08)
            g.add_color_stop_rgba(1, 0.84, 0.52, 0.86, 0.0)
            cr.set_source(g)
            cr.paint()
        chin = P.p(0, 166, 20)
        g = cairo.RadialGradient(chin[0] - 6, chin[1], 0, chin[0], chin[1], 30)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.09)
        g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
        cr.set_source(g)
        cr.paint()
    return f


def earring(cr, S, P, s):
    x, y = P.p(s * 156, 66, -24)
    cr.save()
    cr.translate(x, y)
    cr.rotate(S["ear_swing"] * (1.0 if s > 0 else 0.85))
    gold_fill(cr, lambda c: c.arc(0, 0, 7.5, 0, TAU), -7, -7, 7, 7, 2.2)
    drop = [(0, 6), (12, 18), (14, 36), (6, 52), (0, 58, 1), (-6, 52), (-14, 36), (-12, 18)]
    gold_fill(cr, lambda c: spath(c, drop), -14, 6, 14, 58, 2.2)
    gem(cr, 0, 32, 6.0, 8.5, RUBY, lw=1.5)
    cr.arc(0, 64, 4.6, 0, TAU)
    rgb(cr, INK)
    cr.fill()
    cr.arc(0, 64, 3.3, 0, TAU)
    rgb(cr, PEARL)
    cr.fill()
    cr.restore()


CAP_SHEEN = [[(36, -252), (98, -258), (150, -234)], [(-40, -256), (-102, -262), (-152, -238)],
             [(70, -178), (128, -164)], [(-72, -180), (-130, -166)]]


def hair_cap_shade(S, P):
    def f(cr):
        for st in CAP_STRANDS:
            stroke_taper(cr, P.pts(st, dz=10), 3.6, prof="both", color=HAIR_HL)
        for st in CAP_SHEEN:
            stroke_taper(cr, P.pts(st, dz=12), 7.0, prof="both", color=HAIR_HL2, alpha=0.7)
    return f


def front_lock_parts(S, P):
    parts = []
    dr = (S["roll_lag"] - S["roll"]) * 0.8
    for center, widths in FRONT_LOCKS:
        left, right = R.offset_band(_lag(center, dr, y0=-60, y1=140), widths, 4.0)
        pts = P.pts(left[::6] + [left[-1] + (1,)] + _rev(right)[1::6], dz=12)
        mid = P.pts(_lag(center, dr, y0=-60, y1=140)[1:-1], dz=14)
        parts.append(Part(lambda c, pts=pts: spath(c, pts), HAIR,
                          shade=lambda c, mid=mid: stroke_taper(c, mid, 3.2, prof="both", color=HAIR_HL)))
    return parts


def crown(cr, S, P):
    xs = [-180 + 22.5 * i for i in range(17)]
    yc = lambda x: -162 - 46 * (x / 180) ** 2
    top = P.pts([(x, yc(x) - 12) for x in xs], dz=10)
    bot = P.pts([(x, yc(x) + 12) for x in reversed(xs)], dz=10)
    mid = P.p(0, -162, 10)
    gold_fill(cr, lambda c: spath(c, top + bot, closed=True), mid[0] - 60, mid[1] - 20, mid[0] + 60, mid[1] + 20, 3.0)
    stroke_taper(cr, P.pts([(x, yc(x) - 5) for x in xs[2:-2]], dz=10), 2.4, prof="flat", color=GOLD_HL)
    for x in xs[1:-1:2]:
        px, py = P.p(x, yc(x) + 4, 10)
        cr.arc(px, py, 3.0, 0, TAU)
        rgb(cr, GOLD_SH)
        cr.fill()
    for x in (-94, 94):
        px, py = P.p(x, yc(x), 12)
        gem(cr, px, py, 6.0, 7.0, EMERALD, lw=1.5)
    crest = [(-30, -164, 1), (-34, -192), (-18, -216), (0, -242, 1), (18, -216), (34, -192), (30, -164, 1)]
    cp = P.pts(crest, dz=16)
    gold_fill(cr, lambda c: spath(c, cp), mid[0] - 30, mid[1] - 80, mid[0] + 30, mid[1], 3.0)
    inner = P.pts([(-18, -174), (-20, -192), (-10, -208), (0, -222, 1), (10, -208), (20, -192), (18, -174)], dz=17)
    spath(cr, inner)
    rgb(cr, GOLD_SH, 0.6)
    cr.fill()
    gx_, gy_ = P.p(0, -190, 18)
    gem(cr, gx_, gy_, 9.0, 12.0, RUBY, lw=1.8)


def feather(cr, S, P):
    bx, by = P.p(100, -184, 4)
    ang = math.radians(-60) + S["feather_swing"]
    cr.save()
    cr.translate(bx, by)
    cr.rotate(ang)
    sq = P.sx(100, -184, 4)
    cr.scale(1.0, 0.9 + 0.1 * sq)
    vane = [(0, 0, 1), (54, 14), (120, 40), (178, 50), (220, 30), (238, 0), (220, -30), (178, -50), (120, -40),
            (54, -14)]

    def vpath(c):
        spath(c, vane)
    cr.new_path()
    vpath(cr)
    rgb(cr, INK)
    cr.set_line_width(7.0)
    cr.stroke()
    g = cairo.LinearGradient(0, -50, 0, 50)
    g.add_color_stop_rgb(0, 0.30, 0.74, 0.34)
    g.add_color_stop_rgb(0.5, 0.12, 0.52, 0.26)
    g.add_color_stop_rgb(1, 0.28, 0.70, 0.30)
    vpath(cr)
    cr.set_source(g)
    cr.fill()
    with clip(cr, vpath):
        for u in range(16, 236, 8):
            for k in (-1, 1):
                w_ = 50 * math.sin(math.pi * min(1, u / 240) ** 0.8)
                stroke_taper(cr, [(u, 0), (u + 20, k * w_ * 0.55), (u + 34, k * w_ * 1.05)], 1.6, prof="both",
                             color=(0.06, 0.36, 0.18), alpha=0.7)
        for u in range(30, 236, 16):
            stroke_taper(cr, [(u, 0), (u + 22, -26), (u + 38, -52)], 1.4, prof="both", color=(0.55, 0.88, 0.45),
                         alpha=0.6)
    stroke_taper(cr, [(0, 0), (90, 0), (150, 0)], 3.0, prof="start", color=INK)
    for (rx, ry, col) in ((46, 36, (0.84, 0.52, 0.16)), (37, 29, (0.86, 0.86, 0.34)), (29, 23, (0.10, 0.68, 0.78))):
        ellipse(cr, 174, 0, rx, ry)
        rgb(cr, col)
        cr.fill_preserve()
        rgb(cr, INK)
        cr.set_line_width(2.2)
        cr.stroke()
    heart = [(158, 0, 1), (168, -12), (184, -15), (194, -6), (194, 6), (184, 15), (168, 12)]
    spath(cr, heart)
    rgb(cr, (0.05, 0.10, 0.42))
    cr.fill_preserve()
    rgb(cr, INK)
    cr.set_line_width(2.0)
    cr.stroke()
    ellipse(cr, 182, -6, 4.0, 3.0)
    rgb(cr, (1, 1, 1), 0.9)
    cr.fill()
    cr.restore()


def head(cr, S, torso_path):
    cr.save()
    body_m = cr.get_matrix()
    head_frame(cr, S)
    P = R.Head25D(S["yaw"], S["pitch"])
    face = P.pts(FACE)

    def neck(c):
        c.save()
        c.set_matrix(body_m)
        torso_path(c)
        c.restore()
    with clip(cr, neck):                                      # the head's shadow on the neck
        multiply(cr, lambda c: spath(c, [(q[0] + 6, q[1] + 32) for q in face]), SHADOW, 1.0)
        multiply(cr, lambda c: spath(c, [(q[0] + 4, q[1] + 16) for q in face]), SHADOW, 0.6)
    cap = P.pts(_lag(HAIR_CAP, (S["roll_lag"] - S["roll"]) * 0.5, y0=-20, y1=100), dz=8)
    ears = [P.pts([(s * x, y) for x, y in EAR], dz=-26) for s in (-1, 1)]
    parts = [Part(lambda c, e=e: spath(c, e), SKIN, (SKIN_SH, None), (6, 4, 0, 0),
                  shade=lambda c, s=s: stroke_taper(c, P.pts([(s * 153, -12), (s * 166, 4), (s * 165, 30),
                                                                (s * 154, 48)], dz=-24), 2.8)) for s, e in
             zip((-1, 1), ears)]
    parts.append(Part(lambda c: spath(c, face), SKIN, (SKIN_SH, SKIN_HL), (12, 5, 4, 4), shade=face_shade(S, P, cap)))
    R.ink(cr, parts, lw=4.6)
    draw_tilak(cr, S, P)
    for s in (-1, 1):
        draw_eye(cr, S, P, s)
        draw_brow(cr, S, P, s)
    draw_nose(cr, S, P)
    draw_mouth(cr, S, P)
    for s in (-1, 1):
        earring(cr, S, P, s)
    R.ink(cr, [Part(lambda c: spath(c, cap), HAIR, shade=hair_cap_shade(S, P))] + front_lock_parts(S, P), lw=4.4,
          occ_w=2.4)
    feather(cr, S, P)
    crown(cr, S, P)
    cr.restore()


# ------------------------------------------------------------------ frame

def draw(cr, S):
    rgb(cr, (1, 1, 1))
    cr.paint()
    background(cr, S)
    cr.save()
    camera(cr, S)
    cr.translate(W / 2, CHAR_PIVOT)                          # medium-shot framing: shoulders near the frame edges
    cr.scale(CHAR_S, CHAR_S)
    cr.translate(-W / 2, -CHAR_PIVOT)
    cr.translate(BODY[0] + S["bx"], BODY[1] + S["by"])
    cr.rotate(S["brot"])
    b = S["breath"]
    cr.translate(0, 700)
    cr.scale(1 + 0.004 * b, 1 + 0.008 * b)
    cr.translate(0, -700)
    hair_back(cr, S)
    stole_back(cr, S)
    parts, _ = body_parts(S)
    R.ink(cr, parts, lw=4.8)
    head(cr, S, lambda c: spath(c, TORSO))
    cr.restore()
