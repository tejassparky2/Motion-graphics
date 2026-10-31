"""WW2 channel kit, heads (helper 10): poster heads, faces and leader portraits in the 1940s poster look (STYLE.md).

stick.py's Figure calls draw_head(cr, spec, expression, t) through its head hook (stick.draw_head); this module is
picked up automatically. Head space: origin = the centre of the skull, +x = the way the figure faces, +y = down,
units = px, R = spec["R"] (the skull radius; the neck meets the skull around (-0.1R, +0.95R)).

    heads.draw_head(cr, spec, expression, t)      # one head (spec / expression as stick.draw_head documents)
    heads.portrait(cr, t, "churchill", cx, base_y, height=900, expr="determined", turn=0.45)   # chest-up portrait
    heads.EXPRESSIONS                              # neutral determined angry worried smug shocked sad smiling

How a head is built (poster planes, not a cartoon): one silhouette (skull, brow ridge, nose, lips, chin, jaw) whose 16
points are interpolated between three key views (profile 0, three-quarter 0.6, front 1.0) by spec["turn"], so a head
can turn smoothly; a hard shadow plane (shadow tone + halftone) on the side away from the light; hair as one solid
mass above a hairline; dark almond eyes under a brow bar that blink; a nose plane; the mouth; and per character a
silhouette tweak plus ONE trademark (CHARACTERS). Likeness through silhouette and trademark only: respectful poster
caricature, no symbols (STYLE.md: no Nazi or Imperial Japanese insignia on anyone).
"""
import math
import random

from channels.ww2.kit.core import cairo, col, halftone, rays, text, LABEL, SLAB  # noqa: F401
from channels.ww2.kit import stick as _st

SKIN = "#f2e2c4"                # the light side (STYLE.md: cream)
SKIN_SH = "#c9a582"             # the hard shadow plane
SKIN_DK = "#a7825f"             # cast shadows (under the brow, nose, lip, chin)
LIP = "#a4584a"

# ---------------------------------------------------------------- characters (ONE trademark each + silhouette)
_BASE = dict(width=1.0, jaw=0.0, chin=0.0, jowl=0.0, nose=1.0, brow=1.0, neck=1.0, hair="short", hair_col="#3b2f27",
             vol=1.03, recede=0.0, moustache=None, glasses=None, prop=None, hat=None, scale=1.0, dome=False)
CHARACTERS = {
    "generic": {},
    "hitler": dict(hair="fringe", hair_col="#221d1a", moustache="toothbrush", nose=1.08, width=0.97),
    "stalin": dict(hair="swept", hair_col="#2b2724", vol=1.09, moustache="walrus", prop="pipe", width=1.04, jowl=0.05,
                   nose=1.05),
    "churchill": dict(hair="thin", hair_col="#cdc4b2", width=1.2, jowl=0.36, chin=-0.06, nose=0.78, prop="cigar",
                      hat="bowler", neck=1.35, brow=1.15),   # (stick passes R 1.1x for him; portrait too)
    "roosevelt": dict(hair="receding", hair_col="#8f8b84", recede=0.18, jaw=0.12, chin=0.08, glasses="pincenez",
                      prop="holder", nose=1.06),
    "mussolini": dict(hair=None, dome=True, jaw=0.22, chin=0.1, width=1.05, brow=1.25, neck=1.25),
    "hirohito": dict(hair="part", hair_col="#1f1c1a", glasses="round", moustache="small", width=0.94),
    "chamberlain": dict(hair="receding", hair_col="#6f6a62", recede=0.22, moustache="clipped", hat="homburg",
                        nose=1.16, width=0.92, neck=0.85),
    "daladier": dict(hair="swept", hair_col="#2e2925", vol=1.07, width=1.13, jaw=0.06, neck=1.4, jowl=0.1,
                     nose=0.95),
    "chiang": dict(hair=None, dome=True, moustache="thin", width=0.93, chin=0.04, nose=0.95),
}
LEADERS = [k for k in CHARACTERS if k != "generic"]
NAMES = {"hitler": "ADOLF HITLER", "stalin": "JOSEPH STALIN", "churchill": "WINSTON CHURCHILL",
         "roosevelt": "FRANKLIN D. ROOSEVELT", "mussolini": "BENITO MUSSOLINI", "hirohito": "EMPEROR HIROHITO",
         "chamberlain": "NEVILLE CHAMBERLAIN", "daladier": "ÉDOUARD DALADIER", "chiang": "CHIANG KAI-SHEK"}


def character(name, seed=0):
    """The parameter set for a leader, or a generic soldier/civilian varied by seed (jaw, nose, hair, moustache)."""
    c = dict(_BASE)
    if name in CHARACTERS:
        c.update(CHARACTERS[name])
        return c
    r = random.Random(seed * 131 + 7)
    c.update(width=r.uniform(0.93, 1.07), jaw=r.uniform(-0.04, 0.1), chin=r.uniform(-0.03, 0.06),
             nose=r.uniform(0.88, 1.12), hair_col=r.choice(["#2f2620", "#4a3a2c", "#6b5236", "#2a2622", "#8a6a3e"]),
             moustache=r.choice([None, None, None, "clipped", "small"]))
    return c


# ---------------------------------------------------------------- expressions
EXPRESSIONS = {          # brow_in > 0 lowers the inner ends (anger); lid > 0 narrows the eyes, < 0 widens them
    "neutral": dict(brow_in=0.0, brow_out=0.0, lid=0.05, mouth="line"),
    "determined": dict(brow_in=0.07, brow_out=-0.02, lid=0.22, mouth="firm"),
    "angry": dict(brow_in=0.15, brow_out=-0.06, lid=0.3, mouth="shout"),
    "worried": dict(brow_in=-0.12, brow_out=0.04, lid=0.0, mouth="wobble"),
    "smug": dict(brow_in=0.02, brow_out=-0.07, lid=0.42, mouth="smirk"),
    "shocked": dict(brow_in=-0.13, brow_out=-0.13, lid=-0.35, mouth="o"),
    "sad": dict(brow_in=-0.11, brow_out=0.07, lid=0.38, mouth="frown"),
    "smiling": dict(brow_in=-0.04, brow_out=-0.04, lid=0.1, mouth="smile", happy=True),
}
_FROM_STICK = {("angry", "grit"): "angry", ("angry", None): "determined", ("worried", None): "worried",
               ("sad", None): "sad", (None, "smile"): "smiling", (None, "o"): "shocked", (None, "frown"): "sad",
               (None, "grit"): "angry"}


def _expression(e):
    """stick's {"brow", "mouth", "look", "blink", "sweat"} or {"name": ...} -> the full expression parameters."""
    e = dict(e or {})
    name = e.get("name")
    if name is None:
        b, m = e.get("brow", "neutral"), e.get("mouth", "line")
        name = (_FROM_STICK.get((b, m)) or _FROM_STICK.get((b if b != "neutral" else None, None))
                or _FROM_STICK.get((None, m)) or "neutral")
    out = dict(EXPRESSIONS.get(name, EXPRESSIONS["neutral"]))
    out.update(name=name, look=e.get("look", (0.0, 0.0)), blink=e.get("blink", False), sweat=e.get("sweat", 0.0))
    if "mouth" in e and e.get("name") is None and e["mouth"] not in ("line",):
        out["mouth"] = {"grit": "grit", "o": "o", "smile": "smile", "frown": "frown"}.get(e["mouth"], out["mouth"])
    return out


# ---------------------------------------------------------------- view keys (profile 0, three-quarter 0.6, front 1)
_T = (0.0, 0.6, 1.0)
_SIL = (   # 16 silhouette points in R units: back-neck, back skull, crown, forehead, brow, nose, lips, chin, jaw
    [(-0.62, 0.55), (-0.98, 0.05), (-0.78, -0.8), (-0.1, -1.08), (0.55, -0.92), (0.84, -0.5), (0.93, -0.28),
     (0.86, -0.15), (1.16, 0.1), (0.95, 0.24), (1.0, 0.41), (0.93, 0.52), (0.98, 0.77), (0.8, 0.95), (0.3, 0.92),
     (-0.15, 0.72)],
    [(-0.62, 0.5), (-0.95, 0.0), (-0.8, -0.78), (-0.12, -1.08), (0.55, -0.9), (0.8, -0.52), (0.86, -0.3),
     (0.8, -0.13), (0.8, 0.06), (0.82, 0.22), (0.79, 0.4), (0.72, 0.57), (0.58, 0.79), (0.36, 0.95), (0.0, 0.88),
     (-0.34, 0.66)],
    [(-0.8, 0.35), (-0.88, -0.02), (-0.82, -0.62), (-0.36, -1.02), (0.36, -1.02), (0.82, -0.62), (0.88, -0.3),
     (0.86, -0.1), (0.88, 0.08), (0.84, 0.25), (0.78, 0.44), (0.66, 0.62), (0.42, 0.86), (0.0, 0.97),
     (-0.42, 0.86), (-0.66, 0.62)],
)
_SHADOW = (  # the shadow plane (the side away from the light), 9 points
    [(-1.5, -1.4), (-0.35, -1.12), (-0.3, -0.5), (-0.25, 0.15), (0.1, 0.55), (0.62, 0.8), (1.4, 1.02), (1.4, 1.6),
     (-1.5, 1.6)],
    [(-1.5, -1.4), (-0.02, -1.12), (0.04, -0.45), (-0.02, 0.12), (0.18, 0.56), (0.48, 0.9), (1.3, 1.02), (1.3, 1.6),
     (-1.5, 1.6)],
    [(-1.5, -1.4), (-0.5, -1.1), (-0.55, -0.45), (-0.5, 0.1), (-0.42, 0.55), (-0.2, 0.9), (0.3, 1.05), (0.3, 1.6),
     (-1.5, 1.6)],
)
_HAIRLINE = (  # the hairline from the back of the neck over to the front (hair is the head above it)
    [(-1.5, 0.3), (-0.38, -0.05), (0.12, -0.56), (0.6, -0.72), (0.95, -0.76), (1.6, -0.95)],
    [(-1.5, 0.25), (-0.55, -0.12), (-0.28, -0.56), (0.24, -0.72), (0.74, -0.62), (1.6, -0.75)],
    [(-1.5, 0.05), (-0.86, -0.18), (-0.62, -0.62), (0.0, -0.73), (0.62, -0.62), (1.5, 0.05)],
)
_ANCH = {  # features: (profile, three-quarter, front)
    "eye_n": ((0.64, -0.1), (0.13, -0.1), (-0.34, -0.1)),
    "eye_f": ((0.78, -0.1), (0.68, -0.1), (0.34, -0.1)),
    "ew_n": (0.075, 0.13, 0.135), "ew_f": (0.0, 0.075, 0.135),
    "nose_root": ((0.88, -0.17), (0.46, -0.21), (0.0, -0.17)),
    "nose_tip": ((1.16, 0.1), (0.95, 0.16), (0.03, 0.19)),
    "nose_base": ((0.97, 0.24), (0.62, 0.27), (0.0, 0.28)),
    "mouth": ((0.86, 0.5), (0.52, 0.53), (0.0, 0.53)),
    "mw_back": (0.13, 0.2, 0.21), "mw_front": (0.08, 0.16, 0.21),
    "ear": ((-0.14, 0.03), (-0.52, 0.03), (-0.9, 0.03)),
    "fringe": (  # hitler's swept lock: part, over, tip on the brow, back
        [(0.05, -1.02), (0.62, -0.88), (0.9, -0.42), (0.55, -0.62)],
        [(-0.2, -1.0), (0.45, -0.92), (0.7, -0.46), (0.3, -0.66)],
        [(-0.36, -1.0), (0.3, -0.98), (0.52, -0.5), (0.05, -0.7)],
    ),
}


def _w3(turn):
    """Interpolation weights over the three key views for a turn in 0..1."""
    u = max(0.0, min(1.0, turn))
    if u <= _T[1]:
        k = u / _T[1]
        return (1 - k, k, 0.0)
    k = (u - _T[1]) / (_T[2] - _T[1])
    return (0.0, 1 - k, k)


def _mix3(keys, w):
    a, b, c = keys
    if isinstance(a, (int, float)):
        return a * w[0] + b * w[1] + c * w[2]
    if isinstance(a[0], (int, float)):
        return (a[0] * w[0] + b[0] * w[1] + c[0] * w[2], a[1] * w[0] + b[1] * w[1] + c[1] * w[2])
    return [_mix3((p, q, r), w) for p, q, r in zip(a, b, c)]


# ---------------------------------------------------------------- path helpers
def _spline(pts, R, closed=True, tension=0.5):
    """A smooth (Catmull-Rom) path through points in R units."""
    P = [(x * R, y * R) for x, y in pts]
    n = len(P)

    def path(cr):
        cr.new_sub_path()
        cr.move_to(*P[0])
        last = n if closed else n - 1
        for i in range(last):
            p0, p1 = P[(i - 1) % n] if (closed or i > 0) else P[0], P[i]
            p2 = P[(i + 1) % n]
            p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
            k = tension / 3
            c1 = (p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k)
            c2 = (p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k)
            cr.curve_to(*c1, *c2, *p2)
        if closed:
            cr.close_path()
    return path


def _polyR(pts, R):
    def path(cr):
        cr.new_sub_path()
        cr.move_to(pts[0][0] * R, pts[0][1] * R)
        for x, y in pts[1:]:
            cr.line_to(x * R, y * R)
        cr.close_path()
    return path


def _fill(cr, path, c):
    path(cr)
    cr.set_source_rgba(*c)
    cr.fill()


def _stroke(cr, path, c, w):
    path(cr)
    cr.set_source_rgba(*c)
    cr.set_line_width(w)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()


def _ellipse(cx, cy, rx, ry, rot=0.0):
    def path(cr):
        cr.new_sub_path()
        cr.save()
        cr.translate(cx, cy)
        cr.rotate(rot)
        cr.scale(max(rx, 0.01), max(ry, 0.01))
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
    return path


# ---------------------------------------------------------------- the head
def _silhouette(c, w):
    pts = _mix3(_SIL, w)
    out = []
    for i, (x, y) in enumerate(pts):
        x *= c["width"]
        if i >= 10:                                         # lower face: jaw jut, chin, jowls
            k = (i - 9) / 6
            x += c["jaw"] * k * (1.0 - 0.6 * w[2])
            y += c["chin"] * k + c["jowl"] * 0.35 * k
            if i >= 12:
                x += c["jowl"] * (0.25 if i == 15 else 0.1) * (1 if x > 0 else -1) * (0.4 + w[2])
        if i in (5, 6, 7):                                  # the brow ridge
            x += (c["brow"] - 1.0) * 0.08 * (1 - w[2])
        if i == 8:                                          # the nose in profile
            x = 0.86 * c["width"] + (x - 0.86 * c["width"]) * c["nose"]
        out.append((x, y))
    return out


def _skull_scale(pts, k, cy=-0.15):
    return [(x * k, cy + (y - cy) * k) for x, y in pts]


def draw_head(cr, spec, expression, t):
    """One poster head in head space (see the module docstring and stick.draw_head)."""
    R = spec.get("R", 31.0)
    name = spec.get("leader") or "generic"
    c = character(name, spec.get("seed", 0))
    turn = abs(spec.get("turn", 0.0) or 0.0)
    w = _w3(turn)
    e = _expression(expression)
    kw = max(spec.get("key_w", 5.0) * (0.85 if R < 60 else 1.0), R * 0.04)
    dw = max(2.0, kw * 0.55)
    ink = col("ink")
    flat = spec.get("flat", False)
    hat = spec.get("headgear") or c["hat"]
    if c["scale"] != 1.0:
        cr.save()
        cr.translate(-0.1 * R, 0.95 * R)                 # grow about the neck joint
        cr.scale(c["scale"], c["scale"])
        cr.translate(0.1 * R, -0.95 * R)
    sil = _silhouette(c, w)
    head = _spline(sil, R)
    nx = -0.12 * w[0] + -0.06 * w[1] + 0.0 * w[2]
    neck = _st._capsule((nx * R, 0.55 * R), (nx * R, 1.5 * R), 0.44 * R * c["neck"], 0.5 * R * c["neck"])

    if flat:
        tone = spec.get("tone") or col("ink_soft")
        _fill(cr, neck, tone)
        _fill(cr, head, tone)
        if not hat:
            _fill(cr, _spline(_skull_scale(sil, 1.02), R), tone)
        _st._line(cr, [(0.84 * R, -0.42 * R), (0.92 * R, -0.18 * R), (1.1 * R, 0.1 * R)], max(2.0, R * 0.08),
                  col("cream", 0.85))
        for path, _c in _st._headgear_parts(hat or "", R):
            _fill(cr, path, tone)
        if c["scale"] != 1.0:
            cr.restore()
        return

    skin, sk_sh, sk_dk = col(SKIN), col(SKIN_SH), col(SKIN_DK)
    # neck (in the jaw's shadow)
    _fill(cr, neck, sk_sh)
    halftone(cr, neck, "ink", 2, 0.25, cell=int(max(5, R * 0.09)))
    _stroke(cr, neck, ink, kw)
    # ears behind the head (front view: both)
    ex, ey = _mix3(_ANCH["ear"], w)
    ears = [(ex * c["width"], ey)]
    if w[2] > 0.5:
        ears.append((-ex * c["width"], ey))
    for i, (ax, ay) in enumerate(ears):
        sx = -1 if (w[2] > 0.5 and i == 0) or (w[2] <= 0.5 and False) else 1
        er = _ellipse(ax * R, ay * R, 0.17 * R * (1 - 0.35 * w[1]) if w[2] <= 0.5 else 0.14 * R, 0.25 * R)
        if w[2] > 0.5:
            er = _ellipse((ax + 0.06 * (-1 if ax < 0 else 1)) * R, ay * R, 0.13 * R, 0.24 * R)
        _fill(cr, er, skin if i == 0 or w[2] <= 0.5 else sk_sh)
        _stroke(cr, er, ink, dw)
    # the head: light fill, the shadow plane, hair, outline
    _fill(cr, head, skin)
    cr.save()
    head(cr)
    cr.clip()
    shp = _polyR(_mix3(_SHADOW, w), R)
    _fill(cr, shp, sk_sh)
    halftone(cr, shp, "ink", 2, 0.22, cell=int(max(5, R * 0.08)))
    # cast shadows: under the brow, the nose, the lower lip, the chin
    for key, dy, rx, ry in (("eye_n", -0.03, 0.17, 0.075), ("eye_f", -0.03, 0.14, 0.07)):
        if key == "eye_f" and w[0] > 0.6:
            continue
        ax, ay = _mix3(_ANCH[key], w)
        _fill(cr, _ellipse(ax * c["width"] * R, (ay + dy) * R, rx * R * (0.6 if w[0] > 0.6 else 1), ry * R),
              _st._mix(skin, sk_sh, 0.45))
    nbx, nby = _mix3(_ANCH["nose_base"], w)
    _fill(cr, _ellipse((nbx * c["width"] - 0.05) * R, (nby + 0.05) * R, 0.14 * R, 0.05 * R), sk_dk)
    mx, my = _mix3(_ANCH["mouth"], w)
    _fill(cr, _ellipse((mx * c["width"]) * R, (my + 0.15) * R, 0.12 * R, 0.04 * R), _st._mix(skin, sk_sh, 0.8))
    _fill(cr, _ellipse((mx * c["width"] - 0.1) * R, (0.98 + c["chin"]) * R, 0.45 * R, 0.1 * R), sk_sh)
    cr.restore()
    # hair
    _hair(cr, c, sil, w, R, dw, hat, t)
    # the near ear, over the head (profile / three-quarter)
    if w[2] <= 0.5:
        ax, ay = ears[0]
        er = _ellipse(ax * R, ay * R, 0.17 * R * (1 - 0.35 * w[1]), 0.25 * R)
        _fill(cr, er, skin)
        cr.save()
        er(cr)
        cr.clip()
        _fill(cr, _ellipse((ax - 0.08) * R, ay * R, 0.12 * R, 0.25 * R), sk_sh)
        cr.restore()
        _stroke(cr, er, ink, dw)
        cr.arc(ax * R + 0.02 * R, ay * R, 0.08 * R, -1.6, 1.4)
        cr.set_source_rgba(*ink)
        cr.set_line_width(dw * 0.8)
        cr.stroke()
    _stroke(cr, head, ink, kw)                                   # outline first: the nose and props paint over it
    _face(cr, c, w, e, R, dw, kw, t, spec)
    # headgear last
    if hat:
        side_c = col(_st.NATION_SIDE.get(spec.get("nation"), "axis")) if spec.get("nation") else None
        for path, cc in _st._headgear_parts(hat, R):
            _st._printed(cr, path, col(cc) if cc else side_c, R * 0.5, ink, kw * 0.95)
    if c["scale"] != 1.0:
        cr.restore()


def _hair(cr, c, sil, w, R, dw, hat, t):
    hc = col(c["hair_col"])
    if c["dome"] and not hat:                                    # bald: a printed highlight on the dome
        cr.save()
        _spline(sil, R)(cr)
        cr.clip()
        _fill(cr, _ellipse((0.15 - 0.25 * w[2]) * R, -0.82 * R, 0.42 * R, 0.16 * R, -0.25), col("white", 0.55))
        cr.restore()
        return
    if not c["hair"]:
        return
    line = _mix3(_HAIRLINE, w)
    rec = c["recede"] + (0.35 if c["hair"] == "thin" else 0.0)
    line = [(x, y - (rec if 1 <= i <= 4 and x > -0.7 else 0.0) * (1.0 if i in (2, 3) else 0.6))
            for i, (x, y) in enumerate(line)]
    above = [(x, y) for x, y in line] + [(line[-1][0], -2.2), (line[0][0], -2.2)]
    mass = _spline(_skull_scale(sil[:9] + [(sil[8][0] * 0.4, 0.4), (-0.4, 0.6)], c["vol"]), R)
    cr.save()
    _polyR(above, R)(cr)
    cr.clip()
    _fill(cr, mass, hc)
    if c["hair"] in ("swept", "fringe", "part", "short"):        # a highlight streak and comb lines
        _st._line(cr, [(-0.55 * R, -0.62 * R), (0.0, -0.9 * R), (0.4 * R, -0.86 * R)], max(1.5, R * 0.035),
                  col("white", 0.35))
    _stroke(cr, mass, col("ink"), dw)
    cr.restore()
    if c["hair"] == "part":                                      # hirohito: a neat side part
        px = (-0.1 - 0.35 * w[2]) * R
        _st._line(cr, [(px, -1.0 * R), (px + 0.2 * R, -0.72 * R)], max(1.5, R * 0.03), col("cream", 0.6))
    if c["hair"] == "fringe":                                    # the side-swept lock over the brow
        pts = _mix3(_ANCH["fringe"], w)
        lock = _spline(pts, R, tension=0.35)
        _fill(cr, lock, hc)
        _stroke(cr, lock, col("ink"), dw)


def _brow(cr, ex, ey, ew, inner_dir, b_in, b_out, R, thick, ink):
    """A brow bar over an eye: inner end toward inner_dir (+1 / -1)."""
    ix, ox = ex + inner_dir * ew * 1.15, ex - inner_dir * ew * 1.2
    iy, oy = ey - 0.2 + b_in, ey - 0.22 + b_out
    _st._printed(cr, _polyR([(ix, iy), (ox, oy), (ox, oy - thick * 0.7), (ix, iy - thick)], R), ink, 0, None)


def _eye(cr, ex, ey, ew, eh, inner_dir, e, R, ink, t, wide_ring):
    lx, ly = e["look"]
    if e["blink"]:
        _st._line(cr, [((ex - ew) * R, ey * R), ((ex + ew) * R, ey * R)], max(1.8, R * 0.035), ink)
        return
    if e.get("happy"):                                           # smiling: closed upward arcs
        cr.move_to((ex - ew) * R, (ey + 0.02) * R)
        cr.curve_to((ex - ew * 0.4) * R, (ey - eh * 1.6) * R, (ex + ew * 0.4) * R, (ey - eh * 1.6) * R,
                    (ex + ew) * R, (ey + 0.02) * R)
        cr.set_source_rgba(*ink)
        cr.set_line_width(max(1.8, R * 0.04))
        cr.stroke()
        return
    h = eh * max(0.15, 1.0 - e["lid"])
    X, Y = ex * R + lx * 0.04 * R, ey * R + ly * 0.03 * R
    a, b = (X + inner_dir * ew * R, Y + h * 0.15 * R), (X - inner_dir * ew * R, Y - h * 0.1 * R)

    def almond(cr_):
        cr_.new_sub_path()
        cr_.move_to(*a)
        cr_.curve_to(a[0] - inner_dir * ew * 0.4 * R, Y - h * 1.25 * R, b[0] + inner_dir * ew * 0.35 * R,
                     Y - h * 1.2 * R, *b)
        cr_.curve_to(b[0] + inner_dir * ew * 0.4 * R, Y + h * 0.9 * R, a[0] - inner_dir * ew * 0.4 * R,
                     Y + h * 0.9 * R, *a)
        cr_.close_path()
    if wide_ring:                                                # shocked: the white shows round the dark
        _fill(cr, _ellipse(X, Y, ew * 1.05 * R, eh * 1.25 * R), col("white"))
        _stroke(cr, _ellipse(X, Y, ew * 1.05 * R, eh * 1.25 * R), ink, max(1.5, R * 0.025))
        _fill(cr, _ellipse(X, Y, ew * 0.45 * R, eh * 0.7 * R), ink)
        return
    _fill(cr, almond, ink)
    if R > 60:                                                   # a catch-light in big close-ups
        _fill(cr, _ellipse(X - inner_dir * ew * 0.25 * R, Y - h * 0.35 * R, ew * 0.16 * R, h * 0.22 * R),
              col("white", 0.85))


def _face(cr, c, w, e, R, dw, kw, t, spec):
    ink = col("ink")
    W_ = c["width"]
    thick = 0.07 * c["brow"] if R > 60 else 0.1 * c["brow"]
    eh = 0.1 if R > 60 else 0.11
    wide = e["lid"] < -0.2
    eyes = []
    enx, eny = _mix3(_ANCH["eye_n"], w)
    efx, efy = _mix3(_ANCH["eye_f"], w)
    ewn, ewf = _mix3(_ANCH["ew_n"], w), _mix3(_ANCH["ew_f"], w)
    eyes.append((enx * W_, eny, ewn, 1 if w[2] < 0.5 or True else 1))
    if ewf > 0.03:
        eyes.append((efx * W_, efy, ewf, -1))
    smug = e["name"] == "smug"
    for i, (x, y, ew, d) in enumerate(eyes):
        if w[2] > 0.5:
            d = 1 if x < 0 else -1                               # front view: inner ends point at the nose
        _eye(cr, x, y, ew, eh, d, e, R, ink, t, wide)
        b_out = e["brow_out"] - (0.06 if smug and i == 0 else 0.0)
        _brow(cr, x, y, ew, d, e["brow_in"], b_out, R, thick, ink)
    # the nose plane (three-quarter / front); in profile the silhouette is the nose
    rx, ry = _mix3(_ANCH["nose_root"], w)
    tx, ty = _mix3(_ANCH["nose_tip"], w)
    bx, by = _mix3(_ANCH["nose_base"], w)
    rx, tx, bx = rx * W_, tx * W_, bx * W_
    tx = bx + (tx - bx) * c["nose"]
    if w[0] < 0.75:
        # the nose: a skin shape jutting from the bridge (it breaks the cheek's contour in three-quarter), its
        # side plane a thin shadow sliver, a dark nostril; key line on the bridge, the tip and the underside only
        k = 1 - w[0]
        nose = _spline([(rx, ry), (tx, ty - 0.03), (tx + 0.02, ty + 0.05), (tx - 0.06, ty + 0.11),
                        (bx - 0.05 * k, by + 0.01), (bx - 0.13 * k, by - 0.03), (rx - 0.02 * k, ry + 0.2)], R,
                       tension=0.3)
        _fill(cr, nose, col(SKIN))
        side = _polyR([(rx - 0.01, ry + 0.04), (tx - 0.05, ty + 0.02), (bx - 0.12 * k, by - 0.03),
                       (rx - 0.05 * k, ry + 0.2)], R)
        _fill(cr, side, col(SKIN_SH))
        halftone(cr, side, "ink", 2, 0.18, cell=int(max(5, R * 0.08)))
        _fill(cr, _ellipse((bx - 0.03 * k) * R, (by + 0.0) * R, 0.035 * R, 0.022 * R, 0.3), col(SKIN_DK))
        cr.move_to(rx * R, ry * R)
        cr.curve_to((rx + (tx - rx) * 0.5) * R, (ry + (ty - ry) * 0.45) * R, (tx - 0.02) * R, (ty - 0.06) * R,
                    (tx + 0.02) * R, (ty + 0.04) * R)
        cr.curve_to((tx + 0.02) * R, (ty + 0.1) * R, (tx - 0.06) * R, (ty + 0.12) * R, (bx - 0.02) * R,
                    (by + 0.02) * R)
        cr.set_source_rgba(*ink)
        cr.set_line_width(dw)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
    else:
        _st._line(cr, [((bx - 0.12) * R, (by - 0.04) * R), ((bx - 0.05) * R, (by + 0.01) * R)], dw, ink)
    # the cheekbone plane break (three-quarter / front, big heads)
    if R > 60 and w[0] < 0.7:
        cx0 = (-0.05 if w[2] < 0.5 else -0.52) * W_
        _st._line(cr, [(cx0 * R, 0.12 * R), ((cx0 + 0.12) * R, 0.32 * R)], dw * 0.8, col("ink", 0.7))
    _mouth(cr, c, w, e, R, dw, ink)
    _moustache(cr, c, w, R, dw)
    _glasses(cr, c, w, eyes, R, dw, ink)
    _prop(cr, c, w, R, dw, ink, t, spec)
    if e.get("sweat", 0) > 0:
        k = e["sweat"]
        sx, sy = -0.45 * R, (-0.75 + 0.05 * math.sin(t * 3)) * R
        drop = _ellipse(sx, sy, 0.07 * R * k, 0.11 * R * k)
        _fill(cr, drop, col("#9fc6d6"))
        _stroke(cr, drop, ink, dw * 0.7)


def _mouth(cr, c, w, e, R, dw, ink):
    mx, my = _mix3(_ANCH["mouth"], w)
    mx *= c["width"]
    mb, mf = _mix3(_ANCH["mw_back"], w), _mix3(_ANCH["mw_front"], w)
    L, Rt = (mx - mb) * R, (mx + mf) * R
    Y = my * R
    m = e["mouth"]
    lw = max(2.0, R * 0.04)
    cr.set_source_rgba(*ink)
    if m in ("line", "firm"):
        dip = 0.02 * R if m == "firm" else 0.0
        cr.move_to(L, Y + dip)
        cr.curve_to(L + (Rt - L) * 0.3, Y - dip * 0.5, L + (Rt - L) * 0.7, Y - dip * 0.5, Rt, Y + dip)
        cr.set_line_width(lw * (1.25 if m == "firm" else 1.0))
        cr.stroke()
    elif m == "smile":
        cr.move_to(L, Y - 0.04 * R)
        cr.curve_to(L + (Rt - L) * 0.3, Y + 0.07 * R, L + (Rt - L) * 0.7, Y + 0.07 * R, Rt, Y - 0.05 * R)
        cr.set_line_width(lw)
        cr.stroke()
    elif m == "smirk":
        cr.move_to(L, Y + 0.01 * R)
        cr.curve_to(L + (Rt - L) * 0.4, Y + 0.02 * R, L + (Rt - L) * 0.75, Y + 0.0, Rt, Y - 0.07 * R)
        cr.set_line_width(lw)
        cr.stroke()
    elif m in ("frown", "wobble"):
        cr.move_to(L, Y + 0.05 * R)
        if m == "wobble":
            cr.curve_to(L + (Rt - L) * 0.33, Y - 0.03 * R, L + (Rt - L) * 0.66, Y + 0.04 * R, Rt, Y - 0.01 * R)
        else:
            cr.curve_to(L + (Rt - L) * 0.3, Y - 0.05 * R, L + (Rt - L) * 0.7, Y - 0.05 * R, Rt, Y + 0.05 * R)
        cr.set_line_width(lw)
        cr.stroke()
    elif m in ("o", "shout", "grit"):
        hh = {"o": 0.11, "shout": 0.13, "grit": 0.06}[m] * R
        ww = (Rt - L) * (0.55 if m == "o" else 1.0)
        cxm = (L + Rt) / 2
        shape = _ellipse(cxm, Y + hh * 0.3, ww / 2, hh) if m == "o" else _st._poly(
            [(L, Y - hh * 0.4), (Rt, Y - hh * 0.6), (Rt - ww * 0.12, Y + hh), (L + ww * 0.12, Y + hh * 1.1)])
        _fill(cr, shape, col("#3a1d1a") if m != "grit" else col("white"))
        if m == "shout":                                         # the top teeth
            _fill(cr, _st._poly([(L + ww * 0.08, Y - hh * 0.4), (Rt - ww * 0.06, Y - hh * 0.58),
                                 (Rt - ww * 0.08, Y - hh * 0.15), (L + ww * 0.1, Y)]), col("white"))
        if m == "grit":
            for k in range(1, 4):
                xx = L + ww * k / 4
                _st._line(cr, [(xx, Y - hh * 0.5), (xx, Y + hh)], max(1.2, lw * 0.5), ink)
        _stroke(cr, shape, ink, lw * 0.8)


_MOUST = {   # (half-width, height, droop, gap) in R units
    "toothbrush": (0.1, 0.1, 0.0, 0.0), "walrus": (0.3, 0.12, 0.09, 0.0), "clipped": (0.19, 0.07, 0.02, 0.0),
    "small": (0.13, 0.05, 0.01, 0.02), "thin": (0.17, 0.032, 0.03, 0.015),
}


def _moustache(cr, c, w, R, dw):
    kind = c["moustache"]
    if not kind:
        return
    hw, h, droop, gap = _MOUST[kind]
    bx, by = _mix3(_ANCH["nose_base"], w)
    mx, my = _mix3(_ANCH["mouth"], w)
    cx = ((bx + mx) / 2) * c["width"] + 0.03 * w[0]
    top = by + 0.035
    back = hw * (0.55 + 0.45 * w[1] + w[2])                       # foreshortened toward profile
    front = hw * (0.3 + 0.45 * w[1] + 0.7 * w[2])
    if kind == "toothbrush":
        back, front = hw * (0.6 + 0.4 * (1 - w[0])), hw * (0.35 + 0.65 * (1 - w[0]))
    # profile: never thinner than ~0.12 R, sitting under the nose tip (the clip trims only what passes the lip line)
    cx -= 0.07 * w[0]
    back = max(back, 0.075 * w[0] + back * (1 - w[0]))
    front = max(front, 0.09 * w[0] + front * (1 - w[0]))
    h = max(h, 0.07 * w[0] + h * (1 - w[0]))
    pts = [(cx - back, top + 0.01), (cx - gap, top), (cx + gap, top), (cx + front, top + 0.01),
           (cx + front + 0.02, top + h + droop), (cx + front * 0.4, top + h), (cx - back * 0.4, top + h),
           (cx - back - 0.02, top + h + droop)]
    path = _spline(pts, R, tension=0.25) if kind in ("walrus", "thin", "clipped") else _polyR(pts, R)
    cr.save()
    _spline(_silhouette(c, w), R)(cr)
    cr.clip()
    _fill(cr, path, col(c["hair_col"] if kind != "toothbrush" else "#1c1917"))
    cr.restore()


def _glasses(cr, c, w, eyes, R, dw, ink):
    g = c["glasses"]
    if not g:
        return
    rr = 0.19 if g == "round" else 0.14
    centres = []
    for x, y, ew, d in eyes:
        k = ew / 0.135
        centres.append((x, y))
        _stroke(cr, _ellipse(x * R, (y - 0.01) * R, rr * R * max(0.45, k), rr * R * (0.92 if g == "round" else 0.8)),
                ink, max(1.6, dw * 0.85))
    if len(centres) == 2:
        (x0, y0), (x1, y1) = centres
        _st._line(cr, [((x0 + (rr if x1 > x0 else -rr) * 0.9) * R, (y0 - 0.04) * R),
                       ((x1 - (rr if x1 > x0 else -rr) * 0.6) * R, (y1 - 0.04) * R)], max(1.4, dw * 0.7), ink)
    if g == "round":                                              # the arm back to the ear
        ex, ey = _mix3(_ANCH["ear"], w)
        x0, y0 = centres[0]
        if w[2] < 0.5:
            _st._line(cr, [((x0 - rr) * R, (y0 - 0.04) * R), (ex * c["width"] * R, (ey - 0.12) * R)],
                      max(1.4, dw * 0.7), ink)
    else:                                                         # pince-nez: a cord down to the collar
        x0, y0 = centres[0]
        cr.move_to((x0 - rr * 0.8) * R, y0 * R)
        cr.curve_to((x0 - 0.3) * R, 0.6 * R, (x0 - 0.5) * R, 0.9 * R, (x0 - 0.55) * R, 1.3 * R)
        cr.set_source_rgba(*ink)
        cr.set_line_width(max(1.0, dw * 0.4))
        cr.stroke()


def _smoke(cr, t, x, y, R, rise=1.6, n=4, seed=0):
    """Flat poster smoke: puffs drifting up and swelling, each a cream shape with a soft ink edge."""
    for i in range(n):
        u = (t * 0.32 + i / n + seed * 0.13) % 1.0
        px = x + (math.sin(u * 5.0 + i * 1.7) * 0.25 + u * 0.35) * R
        py = y - u * rise * R
        r = (0.08 + 0.22 * u) * R
        a = 0.75 * (1 - u) ** 1.2
        p = _ellipse(px, py, r * 1.15, r * 0.85, u * 1.3)
        _fill(cr, p, col("cream", a))
        _stroke(cr, p, col("ink_soft", a * 0.6), max(1.0, R * 0.015))


def _prop(cr, c, w, R, dw, ink, t, spec):
    prop = spec.get("mouth_prop") or c["prop"]
    if not prop:
        return
    mx, my = _mix3(_ANCH["mouth"], w)
    mf = _mix3(_ANCH["mw_front"], w)
    x0 = (mx * c["width"] + mf * 0.6) * R
    y0 = (my + 0.01) * R
    reach = 0.55 + 0.45 * (1 - w[2])                              # foreshortened toward the front view
    if prop == "pipe":
        tip = (x0 + 0.42 * reach * R, y0 + 0.16 * R)
        _st._line(cr, [(x0, y0), tip], max(2.0, R * 0.055), col("#3b281c"))
        bowl = _st._poly([(tip[0] - 0.05 * R, tip[1] - 0.2 * R), (tip[0] + 0.16 * R, tip[1] - 0.2 * R),
                          (tip[0] + 0.13 * R, tip[1] + 0.12 * R), (tip[0] - 0.02 * R, tip[1] + 0.12 * R)])
        _st._printed(cr, bowl, col("#5b3a26"), 0.06 * R, ink, dw)
        _smoke(cr, t, tip[0] + 0.05 * R, tip[1] - 0.25 * R, R, seed=1)
    elif prop == "cigar":
        cr.save()
        cr.translate(x0, y0)
        cr.rotate(0.12)
        L = 0.6 * reach * R
        body = _st._poly([(0, -0.06 * R), (L, -0.065 * R), (L, 0.065 * R), (0, 0.06 * R)])
        _st._printed(cr, body, col("#7a4a2a"), 0.04 * R, ink, dw)
        _st._line(cr, [(L * 0.25, -0.06 * R), (L * 0.25, 0.06 * R)], max(1.5, R * 0.03), col("gold"))
        glow = 0.5 + 0.5 * math.sin(t * 2.3)
        _fill(cr, _ellipse(L + 0.02 * R, 0, 0.045 * R, 0.06 * R), _st._mix(col("ink_soft"), col("fire"), glow))
        cr.restore()
        _smoke(cr, t, x0 + (L + 0.05 * R) * math.cos(0.12), y0 + L * 0.12 - 0.1 * R, R, seed=2)
    elif prop == "holder":
        a = (x0, y0)
        b = (x0 + 0.62 * reach * R, y0 - 0.34 * R)
        _st._line(cr, [a, b], max(1.6, R * 0.035), ink)
        cig_end = (b[0] + 0.2 * reach * R, b[1] - 0.11 * R)
        _st._line(cr, [b, cig_end], max(2.4, R * 0.06), col("white"))
        _fill(cr, _ellipse(cig_end[0], cig_end[1], 0.03 * R, 0.03 * R), col("fire"))
        _smoke(cr, t, cig_end[0] + 0.03 * R, cig_end[1] - 0.08 * R, R, seed=3)


# ---------------------------------------------------------------- portraits (chest-up, on rays or a plain field)
OUTFIT = {   # (cloth colour, kind): suits, plain tunics and plain uniforms only; no insignia, no armbands
    "hitler": ("axis", "uniform"), "stalin": ("soviet", "tunic"), "churchill": ("allies", "bowtie"),
    "roosevelt": ("allies", "suit"), "mussolini": ("axis_it", "uniform"), "hirohito": ("axis_jp", "tunic"),
    "chamberlain": ("allies", "wing"), "daladier": ("allies", "suit"), "chiang": ("china", "tunic"),
}


def _blink_at(t, seed):
    return _st._blink(t, seed)


def portrait(cr, t, who, cx, base_y, height=900, expr="determined", turn=0.45, look=(0.0, 0.0), shake=0.0,
             bg=None, ray_col="gold", seed=3, idle=True, nod=0.0):
    """A chest-up poster portrait whose bottom edge sits at (cx, base_y), ~`height` px tall, facing right (+x).
    idle: breath, blinks, a small head turn and tilt. shake: an extra head turn (e.g. a head shake, -1..1). bg:
    "rays" draws a sunburst behind (never red: gold, khaki, ink or allies blue), "plain" a flat disc, None nothing."""
    R = height * 0.155 * (1.1 if who == "churchill" else 1.0)       # as stick.py sizes his head
    kw = max(5.0, height * 0.007)
    br = math.sin(2 * math.pi * t / 3.6) if idle else 0.0
    if bg == "rays":
        rays(cr, t, cx, base_y - height * 0.62, n=28, color=ray_col if ray_col != "soviet" else "gold", alpha=0.22)
    elif bg == "plain":
        _fill(cr, _ellipse(cx, base_y - height * 0.55, height * 0.48, height * 0.48), col("paper_dk"))
    # the head first (the bust's collar covers the neck's base): idle turn, tilt, bob; blink
    tilt = (0.025 * math.sin(2 * math.pi * t / 5.3) if idle else 0.0) + nod
    turn_now = max(0.0, min(1.0, turn + (0.05 * math.sin(2 * math.pi * t / 7.0) if idle else 0.0) + shake))
    low = {"churchill": 0.045, "daladier": 0.03, "mussolini": 0.025}.get(who, 0.0)
    hx, hy = cx + height * 0.01, base_y - height * (0.6 - low + 0.004 * br)
    e = dict(name=expr, look=look, blink=_blink_at(t, seed) if idle else False)
    cloth_name = OUTFIT.get(who, ("khaki", "suit"))[0]
    spec = dict(R=R, leader=who if who in CHARACTERS else None, nation=None, civilian=None, headgear=None,
                side=cloth_name, turn=turn_now, flat=False, tone=None, seed=seed, mouth_prop=None, key_w=kw)
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(tilt)
    draw_head(cr, spec, e, t)
    cr.restore()
    cloth_name, kind = OUTFIT.get(who, ("khaki", "suit"))
    cloth = col(cloth_name)
    ink = col("ink")
    # the bust: shoulders breathing
    sy = base_y - height * (0.28 + 0.006 * br)
    sw = height * 0.42 * (1.12 if who in ("churchill", "daladier") else 1.0)
    neck_x = cx - height * 0.02
    bust = _spline([(-sw, height * 0.3), (-sw * 0.98, 0.06 * height), (-sw * 0.78, -0.04 * height),
                    (-sw * 0.3, -0.1 * height), (sw * 0.32, -0.1 * height), (sw * 0.8, -0.03 * height),
                    (sw, 0.07 * height), (sw * 1.02, height * 0.3)], 1.0, tension=0.4)
    cr.save()
    cr.translate(neck_x, sy)
    _fill(cr, bust, cloth)
    cr.save()
    bust(cr)
    cr.clip()
    back = _st._poly([(-sw * 1.2, -0.3 * height), (-sw * 0.25, -0.3 * height), (-sw * 0.38, height * 0.4),
                      (-sw * 1.2, height * 0.4)])
    _fill(cr, back, _st._shade(cloth, 0.38))
    halftone(cr, back, "ink", 2, 0.3, cell=10)
    _outfit(cr, kind, cloth, sw, height, ink, kw)
    cr.restore()
    _stroke(cr, bust, ink, kw)
    cr.restore()


def _outfit(cr, kind, cloth, sw, height, ink, kw):
    """Collar, lapels, shirt and tie (or a buttoned tunic collar) in bust space (origin at the neck base)."""
    hH = height
    white, dark = col("white"), _st._shade(cloth, 0.55)
    if kind in ("suit", "bowtie", "wing"):
        shirt = _st._poly([(-0.11 * hH, -0.1 * hH), (0.13 * hH, -0.1 * hH), (0.03 * hH, 0.3 * hH)])
        _fill(cr, shirt, white)
        _stroke(cr, shirt, ink, kw * 0.6)
        for s in (-1, 1):                                         # lapels
            lap = _st._poly([(s * 0.12 * hH, -0.1 * hH), (s * 0.26 * hH, -0.06 * hH), (s * 0.2 * hH, 0.04 * hH),
                             (s * 0.03 * hH + 0.02 * hH, 0.32 * hH)])
            _fill(cr, lap, dark)
            _stroke(cr, lap, ink, kw * 0.7)
        if kind == "bowtie":                                      # Churchill's spotted bow tie
            bt = _st._poly([(-0.07 * hH, -0.1 * hH), (0.02 * hH, -0.06 * hH), (0.11 * hH, -0.1 * hH),
                            (0.11 * hH, -0.01 * hH), (0.02 * hH, -0.05 * hH), (-0.07 * hH, -0.01 * hH)])
            _fill(cr, bt, col("#20324d"))
            for dx, dy in ((-0.045, -0.06), (-0.03, -0.03), (0.07, -0.075), (0.085, -0.035), (0.05, -0.055)):
                _fill(cr, _ellipse(dx * hH, dy * hH, 0.006 * hH, 0.006 * hH), white)
            _stroke(cr, bt, ink, kw * 0.6)
        else:
            tie = _st._poly([(0.0, -0.09 * hH), (0.04 * hH, -0.09 * hH), (0.05 * hH, 0.02 * hH),
                             (0.03 * hH, 0.3 * hH), (0.0, 0.3 * hH), (-0.01 * hH, 0.02 * hH)])
            _fill(cr, tie, col("#5a2a25") if kind == "suit" else col("#2b2b33"))
            _stroke(cr, tie, ink, kw * 0.6)
        if kind == "wing":                                        # the wing collar's tips
            for s in (-1, 1):
                _fill(cr, _st._poly([(s * 0.01 * hH + 0.02 * hH, -0.1 * hH), (s * 0.07 * hH + 0.02 * hH, -0.1 * hH),
                                     (s * 0.05 * hH + 0.02 * hH, -0.07 * hH)]), white)
    elif kind in ("tunic", "uniform"):
        coll = _st._poly([(-0.13 * hH, -0.12 * hH), (0.15 * hH, -0.12 * hH), (0.13 * hH, -0.04 * hH),
                          (-0.11 * hH, -0.04 * hH)])
        _fill(cr, coll, dark)
        _stroke(cr, coll, ink, kw * 0.7)
        _st._line(cr, [(0.02 * hH, -0.04 * hH), (0.03 * hH, 0.32 * hH)], kw * 0.6, ink)
        for k in range(4):                                        # plain buttons
            _fill(cr, _ellipse(0.055 * hH, (0.0 + k * 0.075) * hH, 0.011 * hH, 0.011 * hH), col("gold"))
        for s in (-1, 1):                                         # breast pockets (flaps only)
            _stroke(cr, _st._poly([(s * 0.2 * hH - 0.06 * hH, 0.08 * hH), (s * 0.2 * hH + 0.06 * hH, 0.08 * hH),
                                   (s * 0.2 * hH + 0.05 * hH, 0.12 * hH), (s * 0.2 * hH - 0.05 * hH, 0.12 * hH)]),
                    ink, kw * 0.5)
        if kind == "uniform":                                     # a plain shirt and tie at the open collar
            _fill(cr, _st._poly([(-0.04 * hH, -0.11 * hH), (0.06 * hH, -0.11 * hH), (0.01 * hH, -0.02 * hH)]),
                  col("khaki"))
            _fill(cr, _st._poly([(0.0, -0.08 * hH), (0.025 * hH, -0.08 * hH), (0.018 * hH, -0.0)]), col("ink"))
