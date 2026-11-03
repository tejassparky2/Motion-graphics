"""Vex as a cut-out puppet made from the owner's single flat drawing (assets/mascot/vex/vex_flat_front.png): his own
fists are painted out and redrawn as arms that can move to any pose, the mouth has three shapes for talking (open =
the drawing's own, half, closed with fangs), the cape billows, the eyes blink and the head leans. All coordinates are
in the drawing's pixels (1159 x 1358); feet at FOOT.

  puppet(cr, t, x, y, s, mouth=..., arms=(left, right), lean=..., billow=..., blink=None, hold=None)
  talk_mouth(tl, who, t)   the mouth shape for this frame from the voice timing (lip flap while the words run)
"""
import math
import os

import cairo
import numpy as np

from videos import vex_kit as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(ROOT, "assets/mascot/vex/vex_flat_front.png")
SKIN = (228 / 255, 202 / 255, 248 / 255, 1)
DARK = (48 / 255, 41 / 255, 50 / 255, 1)            # jacket and cape inside
JACKET = (40 / 255, 34 / 255, 42 / 255, 1)
WHITE = (0.965, 0.95, 0.95, 1)
INK = (0.04, 0.02, 0.04, 1)
MOUTH_IN = (106 / 255, 21 / 255, 30 / 255, 1)
TONGUE = (248 / 255, 123 / 255, 139 / 255, 1)
LW = 10                                              # outline width in drawing pixels

# the drawing's own fists and cuffs, painted out of the base
FIST_L = [(300, 842), (404, 842), (418, 878), (434, 905), (406, 962), (362, 1006), (286, 1006), (280, 930), (290, 878)]
FIST_R = [(674, 848), (792, 852), (812, 930), (812, 1010), (716, 1012), (666, 978), (664, 905), (668, 880)]
SHOULDER = {"l": (300, 952), "r": (792, 968)}        # where an arm comes out from under the cape
ARMS = {   # pose -> (wrist, fist centre); "rest" is where the drawing has them
    "l": {"rest": ((322, 960), (362, 906)), "up": ((300, 800), (300, 720)), "out": ((210, 900), (150, 870)),
          "chin": ((420, 880), (470, 830)), "front": ((380, 930), (440, 905))},
    "r": {"rest": ((764, 976), (722, 914)), "up": ((790, 805), (790, 725)), "out": ((880, 915), (945, 885)),
          "point": ((880, 930), (955, 925)), "front": ((700, 945), (640, 915))},
}
FOOT = (520, 1355)
_base = {}


def _poly(c, pts):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()


def _load():
    if _base:
        return _base
    img = cairo.ImageSurface.create_from_png(PNG)
    w, h = img.get_width(), img.get_height()
    base = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(base)
    c.set_source_surface(img, 0, 0)
    c.paint()
    for poly in (FIST_L, FIST_R):                    # the fists go: arms are drawn live
        _poly(c, poly)
        c.set_source_rgba(*DARK)
        c.fill()
    _base.update(img=img, base=base, w=w, h=h)
    return _base


def _mouth(c, shape):
    """Mouth shapes over the drawing's open mouth (centre ~ (544, 725))."""
    if shape == "open":
        return
    c.move_to(470, 672)                              # cover everything below the upper lip
    c.line_to(626, 672)
    c.curve_to(626, 720, 610, 770, 590, 782)
    c.curve_to(570, 800, 518, 800, 498, 782)
    c.curve_to(478, 770, 464, 720, 470, 672)
    c.close_path()
    c.set_source_rgba(*SKIN)
    c.fill()
    if shape == "half":                              # a smaller opening: dark mouth, tongue, lower lip at ~740
        c.move_to(472, 668)
        c.line_to(622, 668)
        c.curve_to(620, 712, 590, 742, 547, 744)
        c.curve_to(504, 742, 474, 712, 472, 668)
        c.close_path()
        c.set_source_rgba(*MOUTH_IN)
        c.fill_preserve()
        c.save()
        c.clip()
        c.arc(547, 742, 52, 0, 2 * math.pi)
        c.set_source_rgba(*TONGUE)
        c.fill()
        c.restore()
        c.move_to(472, 668)
        c.curve_to(474, 712, 504, 742, 547, 744)
        c.curve_to(590, 742, 620, 712, 622, 668)
        c.set_source_rgba(*INK)
        c.set_line_width(LW)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    else:                                            # closed: the lip line with two fangs over it, a little smile
        c.move_to(466, 664)
        c.curve_to(500, 684, 590, 684, 628, 662)
        c.set_source_rgba(*INK)
        c.set_line_width(LW)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    for fx in (492, 600):                            # fangs
        c.move_to(fx - 13, 672)
        c.line_to(fx + 13, 672)
        c.line_to(fx, 700 if shape == "closed" else 696)
        c.close_path()
        c.set_source_rgba(*WHITE)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.stroke()


def _arm(c, side, wrist, fist, hold=None):
    sx, sy = SHOULDER[side]
    wx, wy = wrist
    fx, fy = fist
    mx, my = (sx + wx) / 2 + (18 if side == "l" else -18), (sy + wy) / 2 + 12   # a slight elbow curve
    for col, lw in ((INK, 78), (JACKET, 58)):        # sleeve
        c.move_to(sx, sy)
        c.curve_to(mx, my, mx, my, wx, wy)
        c.set_source_rgba(*col)
        c.set_line_width(lw)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    ang = math.atan2(fy - wy, fx - wx)
    c.save()                                         # white cuff across the wrist
    c.translate(wx, wy)
    c.rotate(ang)
    c.scale(26, 46)
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()
    c.set_source_rgba(*WHITE)
    c.fill_preserve()
    c.set_source_rgba(*INK)
    c.set_line_width(LW)
    c.stroke()
    if hold:                                         # a prop held in this fist, drawn behind the fingers
        hold(c, fx, fy, ang)
    c.save()                                         # fist: a soft rounded mitten with knuckle lines
    c.translate(fx, fy)
    c.rotate(ang)
    c.scale(64, 58)
    c.arc(0, 0, 1, 0, 2 * math.pi)
    c.restore()
    c.set_source_rgba(*SKIN)
    c.fill_preserve()
    c.set_source_rgba(*INK)
    c.set_line_width(LW)
    c.stroke()
    c.save()
    c.translate(fx, fy)
    c.rotate(ang)
    for k in (-1, 0, 1):
        c.move_to(34, k * 20 - 8)
        c.curve_to(50, k * 20 - 3, 50, k * 20 + 7, 38, k * 20 + 10)
    c.set_source_rgba(*INK)
    c.set_line_width(5)
    c.stroke()
    c.restore()


def _pose_pts(side, pose):
    """pose = name, or (name_a, name_b, u) to blend between two poses."""
    if isinstance(pose, tuple):
        a, b, u = pose
        (wa, fa), (wb, fb) = ARMS[side][a], ARMS[side][b]
        u = u * u * (3 - 2 * u)
        return ((wa[0] + (wb[0] - wa[0]) * u, wa[1] + (wb[1] - wa[1]) * u),
                (fa[0] + (fb[0] - fa[0]) * u, fa[1] + (fb[1] - fa[1]) * u))
    return ARMS[side][pose]


def frame_sprite(t, mouth="closed", arms=("rest", "rest"), lean=0.0, billow=0.0, blink=0.0, hold=(None, None),
                 shake=0.0):
    """The finished puppet frame at the drawing's own size (ARGB, with a pad on each side)."""
    B = _load()
    w, h, pad = B["w"], B["h"], 90
    layer = cairo.ImageSurface(cairo.FORMAT_ARGB32, w + 2 * pad, h)
    c = cairo.Context(layer)
    c.translate(pad, 0)
    # cape billow: each row of the lower body scaled about the centre line (continuous, so no gaps); boots stay
    if abs(billow) > 0.002:
        for y0 in range(0, h, 4):
            g = 0.0 if y0 < 960 else min(1.0, (y0 - 960) / 200) * (1 - max(0.0, (y0 - 1180) / 80))
            k = 1 + billow * max(0.0, g)
            c.save()
            c.rectangle(-pad, y0, w + 2 * pad, 4)
            c.clip()
            c.translate(FOOT[0], 0)
            c.scale(k, 1)
            c.translate(-FOOT[0], 0)
            c.set_source_surface(B["base"], 0, 0)
            c.paint()
            c.restore()
    else:
        c.set_source_surface(B["base"], 0, 0)
        c.paint()
    _mouth(c, mouth)
    for side, pose, hd in (("l", arms[0], hold[0]), ("r", arms[1], hold[1])):
        wr, fi = _pose_pts(side, pose)
        if shake and pose not in ("rest",):
            fi = (fi[0] + shake * math.sin(t * 40), fi[1] + shake * math.cos(t * 37))
        _arm(c, side, wr, fi, hd)
    K._lids(c, K._pose("front"), min(1.0, blink * 1.6))
    if abs(lean) < 0.5:
        out = layer
    else:                                            # head lean: rows shift more the higher they are; boots planted
        out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w + 2 * pad, h)
        c = cairo.Context(out)
        for y0 in range(0, h, 4):
            c.save()
            c.rectangle(0, y0, w + 2 * pad, 4)
            c.clip()
            c.set_source_surface(layer, round(lean * (1 - y0 / h) ** 1.6), 0)
            c.paint()
            c.restore()
    soft = cairo.ImageSurface(cairo.FORMAT_ARGB32, w + 2 * pad + 8, h + 8)     # ~0.6 px soft focus
    c = cairo.Context(soft)
    c.set_operator(cairo.OPERATOR_ADD)
    for ox, oy in ((-3.5, 0), (3.5, 0), (0, -3.5), (0, 3.5)):
        c.set_source_surface(out, 4 + ox, 4 + oy)
        c.paint_with_alpha(0.25)
    return soft, pad


def puppet(cr, t, x, y, s=0.22, mouth="closed", arms=("rest", "rest"), lean=0.0, billow=None, blink=None,
           squash=0.0, rot=0.0, pivot="feet", lift=0.0, hold=(None, None), shake=0.0, flip=False, ground=True):
    """Draw the puppet with its feet at (x, y) on the floor photo."""
    if blink is None:
        blink = K.auto_blink(t)
    if billow is None:
        billow = 0.035 * math.sin(t * 2.3) + 0.015 * math.sin(t * 5.1)
    P = K._pose("front")
    if ground:
        K.shadows(cr, P, x, y, s, lift)
    spr, pad = frame_sprite(t, mouth, arms, lean, billow, blink, hold, shake)
    cr.save()
    cr.translate(x, y - lift)
    if pivot == "center":
        cr.translate(0, -FOOT[1] * s * 0.5)
        cr.rotate(rot)
        cr.translate(0, FOOT[1] * s * 0.5)
    else:
        cr.rotate(rot)
    cr.scale(s * (1 + 0.14 * squash) * (-1 if flip else 1), s * (1 - 0.16 * squash))
    cr.translate(-FOOT[0] - pad - 4, -FOOT[1] - 4)
    cr.set_source_surface(spr, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


def talk_mouth(tl, who, t, rest="closed"):
    """Lip flap from the timeline: while a word of `who` is being said, cycle open / half / closed."""
    for b in tl.beats:
        if b.speaker != who or not (b.start <= t <= b.end):
            continue
        for u in b.units:
            if u.start <= t <= u.end:
                ph = ((t - u.start) / 0.11) % 3
                return ("open", "half", "closed")[int(ph)] if (u.end - u.start) > 0.12 else "half"
        return rest
    return rest
