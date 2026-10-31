"""WW2 channel kit: the poster figures (channels/ww2/STYLE.md, "Characters"). Pure pycairo.

Animated 1940s-poster people on a joint skeleton: tapered filled limbs with an ink key line, uniforms in the side
colour, a hard shadow side with halftone dots, a profile / 3/4 face (jaw, nose, brow) with blinks and expressions,
nation headgear, leaders as respectful poster portraits with ONE trademark each, and one-tone silhouette crowds.
A hero figure is ~420 px tall at scale 1; crowds and soldiers use 0.3-0.6.

    from channels.ww2.kit.stick import Figure, crowd, POSES

    f = Figure(nation="germany", x=600, y=900, scale=1.0, facing=1)          # y = the ground line under the figure
    f.draw(cr, t, track=[(0.0, "stand"), (1.0, "walk"), (3.0, "salute")],     # keyframes: (time, pose name or dict)
           move=[(1.0, 600), (3.0, 900)])                                     # optional x path (t, x) or (t, x, y)

Figure(nation=None, leader=None, civilian=None, x, y, scale=1.0, facing=1, prop=None, color=None, seed=0, flat=False)
    nation:   "germany" "britain" "usa" "soviet" "france" "japan" "italy" (headgear and uniform in the side colour)
    civilian: "flatcap" "hat" "scarf" (khaki / olive coats)
    leader:   "hitler" "stalin" "churchill" "roosevelt" "mussolini" "hirohito" "chamberlain" (ONE trademark each;
              stalin gets his pipe, churchill his cigar, roosevelt his cigarette holder, chamberlain his umbrella)
    prop:     "rifle" "paper" "pen" "umbrella" (held in the hand), or None; leaders bring their own
    facing:   1 = right, -1 = left. A pose may also carry "turn" (-1..1): the head turns toward the viewer (3/4).
    flat / color: a one-tone silhouette with a rim of light (crowds; `color` = its tone).
Figure.draw(cr, t, track, move=None, face=None)
    track: [(t, pose)] sorted by time. A pose is a POSES name, a dict of joint angles (see REST) or a function of t
           returning one, and may carry a "face" dict. Each key's pose blends in with an eased curve over BLEND
           seconds before its time; looping actions (walk, run, march, wave, cheer, crawl, shiver, fire, shake) keep
           animating, and every pose breathes and shifts its weight, so nothing freezes.
    face:  overrides for the whole track: {"brow": "neutral|angry|worried|sad", "mouth": "line|smile|o|grit|frown",
           "sweat": 0..1, "look": (dx, dy)}. Eyes blink by themselves every 2-5 s.
Figure.joints(t, track, move): world positions of hips, neck, shoulders, elbows, hands, knees, feet, head.
crowd(cr, t, n, x0, x1, y0, y1, scale=0.45, nation=None, pose="cheer", seed=1, poses=None, tone=None)
    N small silhouette figures with varied timing and headgear; cheap enough for 40+ on screen.

Joint angles (radians): limbs are measured from straight down, positive = toward the way the figure faces.
    lean    torso lean (forward +)           nod   head tilt (down +)        turn  head 3/4 turn (-1..1)
    sh_n/sh_f  near/far upper arm            el_n/el_f  elbow bend (forearm swings forward/up +)
    hip_n/hip_f  near/far thigh              kn_n/kn_f  knee bend (shin swings back +)
    drop    crouch, px the hips sink (on top of keeping the feet on the ground)
    ground  "feet" (default: lowest foot on the ground) or "all" (lowest body point: diving, crawling, lying)
    hand_n/hand_f  "open" | "fist" | "crossed" (crossed fingers) | "splay"
"""
import math
import random

from channels.ww2.kit.core import PAL, SIDE, cairo, col, lerp, smooth  # noqa: F401

# ---------------------------------------------------------------- proportions (scale 1: a ~420 px hero figure)
HEAD_R = 36.0
NECK = 12.0
TORSO = 136.0
SH_DROP = 20.0
UPPER, FORE = 72.0, 66.0
THIGH, SHIN = 92.0, 88.0
BLEND = 0.28                     # seconds a pose takes to blend in before its key

REST = dict(lean=-0.035, nod=0.03, turn=0.0, sh_n=0.12, sh_f=-0.10, el_n=0.16, el_f=0.12, hip_n=0.1,
            hip_f=-0.04, kn_n=0.12, kn_f=0.02, drop=0.0, bob=0.0, sway=0.0, hand_n="open", hand_f="open", ground="feet",
            air=0.0, prop_up=0.0)

NATION_SIDE = {"germany": "axis", "britain": "allies", "usa": "allies", "soviet": "soviet", "france": "allies",
               "japan": "axis_jp", "italy": "axis_it", "china": "china"}

# ---------------------------------------------------------------- poses
def _cycle(t, period):
    return 2 * math.pi * t / period


def _walk(t, period=0.95, amp=0.42, arm=0.38, lean=0.06):
    p = _cycle(t, period)
    s = math.sin(p)
    return dict(lean=lean, hip_n=amp * s, hip_f=-amp * s,
                kn_n=0.12 + 0.75 * max(0.0, math.cos(p)) * 0.8, kn_f=0.12 + 0.75 * max(0.0, -math.cos(p)) * 0.8,
                sh_n=-arm * s, sh_f=arm * s, el_n=0.25 + 0.15 * max(0, -s), el_f=0.25 + 0.15 * max(0, s),
                bob=-3.0 * abs(math.cos(p)))


def _run(t):
    p = _cycle(t, 0.52)
    s = math.sin(p)
    return dict(lean=0.28, nod=-0.1, hip_n=0.75 * s + 0.1, hip_f=-0.75 * s + 0.1,
                kn_n=0.3 + 1.3 * max(0.0, math.cos(p)), kn_f=0.3 + 1.3 * max(0.0, -math.cos(p)),
                sh_n=-0.9 * s, sh_f=0.9 * s, el_n=1.5, el_f=1.5, bob=-7.0 * abs(math.cos(p)), hand_n="fist",
                hand_f="fist")


def _march(t):
    p = _cycle(t, 0.8)
    s = math.sin(p)
    return dict(lean=-0.02, nod=-0.06, hip_n=0.55 * max(-0.25, s), hip_f=-0.55 * min(0.25, s) * 1.0,
                kn_n=0.9 * max(0.0, math.cos(p)) * max(0, s) + 0.05, kn_f=0.9 * max(0.0, -math.cos(p)) * max(0, -s) + 0.05,
                sh_n=-0.5 * s, sh_f=0.5 * s, el_n=0.08, el_f=0.08, bob=-2.0 * abs(math.cos(p)), hand_n="fist",
                hand_f="fist")


def _idle(t, seed=0):
    """Breathing (a 2 px bob) and a slow weight shift: added under every pose so nothing ever freezes."""
    return dict(bob=-2.0 * (0.5 + 0.5 * math.sin(t * 2 * math.pi / 3.2 + seed)),
                sway=0.018 * math.sin(t * 2 * math.pi / 5.3 + seed * 1.7))


def _wave(t):
    return dict(sh_n=2.6, el_n=0.35 + 0.45 * math.sin(t * 2 * math.pi * 1.6), sh_f=-0.08, el_f=0.15, turn=0.4,
                face={"mouth": "smile"})


def _cheer(t):
    k = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 1.4)
    return dict(sh_n=2.7 + 0.25 * k, sh_f=-2.7 - 0.25 * k + 0.0, el_n=0.25, el_f=-0.25, nod=-0.25, turn=0.6,
                bob=-10.0 * k, hand_n="fist", hand_f="fist", face={"mouth": "o", "brow": "neutral"})


def _shiver(t):
    j = math.sin(t * 2 * math.pi * 9.0)
    return dict(lean=0.18, nod=0.15, sh_n=0.6, el_n=2.2, sh_f=0.5, el_f=2.3, kn_n=0.25, kn_f=0.25, drop=6,
                sway=0.03 * j, turn=0.5, face={"brow": "worried", "mouth": "grit"})


def _crawl(t):
    p = _cycle(t, 1.1)
    s = math.sin(p)
    return dict(lean=1.45, nod=-1.2, sh_n=1.9 + 0.5 * s, el_n=-0.9 + 0.3 * s, sh_f=1.9 - 0.5 * s, el_f=-0.9 - 0.3 * s,
                hip_n=0.5 + 0.5 * max(0, s), kn_n=1.6, hip_f=0.5 + 0.5 * max(0, -s), kn_f=1.6, ground="all")


def _fire(t):
    k = (t * 1.5) % 1.0                                            # a shot every 0.67 s, a recoil kick
    rec = max(0.0, 1 - k * 6)
    return dict(_AIM, lean=0.12 - 0.08 * rec, flash=1.0 if k < 0.08 else 0.0, face={"brow": "angry", "mouth": "grit"})


def _shake(t):
    return dict(sh_n=0.95 + 0.12 * math.sin(t * 2 * math.pi * 2.2), el_n=0.35, turn=0.35,
                face={"mouth": "smile"})


_AIM = dict(lean=0.12, nod=0.05, sh_n=1.25, el_n=0.3, sh_f=1.05, el_f=1.1, hip_n=0.25, hip_f=-0.3, kn_n=0.15,
            kn_f=0.2, drop=6, aim=1.0)

POSES = {
    "stand": dict(),
    "idle": dict(),
    "walk": _walk,
    "run": _run,
    "march": _march,
    "point": dict(sh_n=1.6, el_n=0.05, turn=0.3, hand_n="fist", face={"brow": "angry"}),
    "shrug": dict(sh_n=0.55, el_n=1.9, sh_f=-0.55, el_f=-1.9, nod=-0.12, turn=0.8, drop=-3,
                  face={"brow": "worried", "mouth": "frown"}),
    "wave": _wave,
    "salute": dict(sh_n=1.75, el_n=2.6, lean=-0.03, nod=-0.05, hand_n="open", face={"mouth": "line"}),
    "cheer": _cheer,
    "hips": dict(sh_n=0.75, el_n=-1.9, sh_f=-0.75, el_f=1.9, turn=0.7, face={"brow": "angry", "mouth": "grit"}),
    "arms_crossed": dict(sh_n=0.25, el_n=2.0, sh_f=0.15, el_f=2.15, turn=0.7, face={"brow": "angry"}),
    "head_down": dict(lean=0.18, nod=0.5, sh_n=0.05, sh_f=-0.05, el_n=0.1, el_f=0.1, turn=0.3,
                      face={"brow": "sad", "mouth": "frown"}),
    "sign": dict(lean=0.42, nod=0.35, sh_n=0.95, el_n=0.8, sh_f=0.75, el_f=0.95, hip_n=1.45, kn_n=1.45,
                 hip_f=1.45, kn_f=1.45, ground="seat", face={"mouth": "line"}),
    "slam": dict(lean=0.25, nod=0.15, sh_n=2.8, el_n=0.4, turn=0.4, face={"brow": "angry", "mouth": "grit"}),
    "slam_down": dict(lean=0.35, nod=0.2, sh_n=1.0, el_n=0.0, hand_n="fist", turn=0.4,
                      face={"brow": "angry", "mouth": "grit"}),
    "shake": _shake,
    "hold_paper": dict(sh_n=2.35, el_n=0.35, turn=0.5, prop_up=1.0, face={"mouth": "smile"}),
    "aim": _AIM,
    "fire": _fire,
    "crouch": dict(lean=0.35, hip_n=1.2, kn_n=2.0, hip_f=0.9, kn_f=2.1, sh_n=0.6, el_n=0.6, sh_f=0.4, el_f=0.7,
                   face={"brow": "worried"}),
    "duck": dict(lean=0.55, nod=0.4, hip_n=1.3, kn_n=2.2, hip_f=1.1, kn_f=2.3, sh_n=2.4, el_n=1.9, sh_f=2.2,
                 el_f=2.0, face={"brow": "worried", "mouth": "grit", "sweat": 1.0}),
    "dive": dict(lean=1.5, nod=-1.1, sh_n=2.9, el_n=0.1, sh_f=2.7, el_f=0.1, hip_n=-0.2, kn_n=0.6, hip_f=-0.35,
                 kn_f=0.3, ground="all", air=20.0, face={"brow": "worried", "mouth": "o"}),
    "prone": dict(lean=1.5, nod=-1.2, sh_n=2.0, el_n=-1.0, sh_f=1.8, el_f=-1.1, hip_n=0.1, kn_n=0.2, hip_f=0.0,
                  kn_f=0.3, ground="all"),
    "crawl": _crawl,
    "sit": dict(lean=0.0, hip_n=1.5, kn_n=1.45, hip_f=1.45, kn_f=1.5, sh_n=0.45, el_n=0.6, sh_f=0.35, el_f=0.7,
                ground="seat"),
    "surrender": dict(sh_n=2.9, el_n=0.25, sh_f=-2.9, el_f=-0.25, turn=0.8, hand_n="splay", hand_f="splay",
                      face={"brow": "worried", "mouth": "o", "sweat": 1.0}),
    "shiver": _shiver,
    "behind_back": dict(sh_n=-0.55, el_n=-1.35, sh_f=-0.5, el_f=-1.4, hand_n="crossed", hand_f="crossed"),
}


def pose_at(name, t, seed=0):
    """A POSES entry (or a dict) evaluated at time t, merged over REST, with the idle breathing added."""
    p = POSES.get(name, {}) if isinstance(name, str) else name
    d = dict(REST)
    d.update(p(t) if callable(p) else p)
    idle = _idle(t, seed)
    d["bob"] = d.get("bob", 0.0) + idle["bob"]
    d["sway"] = d.get("sway", 0.0) + idle["sway"]
    return d


def blend(a, b, u):
    """Blend two evaluated poses: numbers ease, strings and faces switch at the midpoint."""
    out = {}
    for k in set(a) | set(b):
        va, vb = a.get(k, REST.get(k)), b.get(k, REST.get(k))
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            out[k] = lerp(va, vb, u)
        elif k == "face":
            fa, fb = va or {}, vb or {}
            out[k] = {**fa, **fb} if u >= 0.5 else {**fb, **fa}
        else:
            out[k] = vb if u >= 0.5 else va
    return out


def track_pose(track, t, seed=0):
    """The pose of a keyframe track at time t (each key's pose blends in over BLEND s before its time)."""
    if not track:
        return pose_at("stand", t, seed)
    track = sorted(track, key=lambda k: k[0])
    cur = track[0]
    for i, (tk, p) in enumerate(track):
        if t >= tk:
            cur = (tk, p)
    i = track.index(cur)
    pose = pose_at(cur[1], t, seed)
    if i + 1 < len(track):
        tn, pn = track[i + 1]
        if t > tn - BLEND:
            u = smooth((t - (tn - BLEND)) / BLEND)
            pose = blend(pose, pose_at(pn, t, seed), u)
    return pose


# ---------------------------------------------------------------- skeleton
def _dir(a):
    return math.sin(a), math.cos(a)


def skeleton(p):
    """Joint positions in the figure's own frame (facing +x, y down), hips at (0, 0) before grounding."""
    lean = p["lean"] + p.get("sway", 0.0)
    hip = (0.0, 0.0)
    neck = (TORSO * math.sin(lean), -TORSO * math.cos(lean))
    sh = (neck[0] - SH_DROP * math.sin(lean), neck[1] + SH_DROP * math.cos(lean))
    ha = lean + p["nod"] * 0.6
    head = (neck[0] + (NECK + HEAD_R) * math.sin(ha), neck[1] - (NECK + HEAD_R) * math.cos(ha))
    J = dict(hip=hip, neck=neck, sh=sh, head=head)
    for side in ("n", "f"):
        a = p["sh_" + side] + lean * 0.5
        dx, dy = _dir(a)
        el = (sh[0] + UPPER * dx, sh[1] + UPPER * dy)
        dx2, dy2 = _dir(a + p["el_" + side])
        J["el_" + side] = el
        J["hand_" + side] = (el[0] + FORE * dx2, el[1] + FORE * dy2)
        h = p["hip_" + side]
        dx, dy = _dir(h)
        kn = (THIGH * dx, THIGH * dy)
        dx2, dy2 = _dir(h - p["kn_" + side])
        J["kn_" + side] = kn
        J["ft_" + side] = (kn[0] + SHIN * dx2, kn[1] + SHIN * dy2)
    return J


def _ground_offset(J, p):
    """How far down to move the hips so the figure stands on y = 0."""
    g = p.get("ground", "feet")
    if g == "all":
        low = max(v[1] for v in J.values()) + (HEAD_R if J["head"][1] >= max(J["ft_n"][1], J["ft_f"][1]) - 20 else 0)
        low = max(low, J["head"][1] + HEAD_R)
    elif g == "seat":
        low = max(J["ft_n"][1], J["ft_f"][1])
    else:
        low = max(J["ft_n"][1], J["ft_f"][1])
    return -low + 3.5 - p.get("air", 0.0)



# ---------------------------------------------------------------- print helpers
def _mix(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(4))


def _shade(c, k=0.4):
    """The hard shadow tone of an ink: mixed toward the key ink."""
    return _mix(c, col("ink"), k)


def _line(cr, pts, w, c):
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.move_to(*pts[0])
    for q in pts[1:]:
        cr.line_to(*q)
    cr.set_source_rgba(*c)
    cr.stroke()


def _capsule(a, b, ra, rb):
    """A tapered limb path: radius ra at a, rb at b, round ends."""
    def path(cr):
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        cr.new_sub_path()
        cr.arc(b[0], b[1], rb, ang - math.pi / 2, ang + math.pi / 2)
        cr.arc(a[0], a[1], ra, ang + math.pi / 2, ang + 3 * math.pi / 2)
        cr.close_path()
    return path


def _poly(pts):
    def path(cr):
        cr.new_sub_path()
        cr.move_to(*pts[0])
        for q in pts[1:]:
            cr.line_to(*q)
        cr.close_path()
    return path


_DOT = {}


def _dot_pattern(cell=7.0):
    """Round halftone dots on a 45-degree screen (an alpha mask)."""
    if cell in _DOT:
        return _DOT[cell]
    n = int(cell * 24)
    s = cairo.ImageSurface(cairo.FORMAT_A8, n, n)
    c = cairo.Context(s)
    for i in range(-1, 26):
        for j in range(-1, 30):
            c.arc(i * cell + (cell / 2 if j % 2 else 0), j * cell * 0.866, cell * 0.27, 0, 2 * math.pi)
            c.fill()
    p = cairo.SurfacePattern(s)
    p.set_extend(cairo.EXTEND_REPEAT)
    m = cairo.Matrix()
    m.rotate(0.785)
    p.set_matrix(m)
    _DOT[cell] = p
    return p


LIGHT = (1.0, -0.55)                 # light from the front and above (figure space): shadows fall back and down


def _band(cr, path, d, color, dots=False):
    """The part of the shape left uncovered when a copy of it is slid d px toward the light: its back/under edge
    (d > 0), or with d < 0 its lit edge. Solid in `color`, or halftone dots of it."""
    lx, ly = LIGHT
    n = math.hypot(lx, ly)
    cr.save()
    path(cr)
    cr.clip()
    cr.push_group()
    path(cr)
    cr.set_source_rgba(*color)
    if dots:
        cr.save()
        cr.clip()
        cr.mask(_dot_pattern())
        cr.restore()
    else:
        cr.fill()
    cr.save()
    cr.translate(d * lx / n, d * ly / n)
    path(cr)
    cr.restore()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.fill()
    cr.pop_group_to_source()
    cr.paint()
    cr.restore()


def _printed(cr, path, fill, d=0.0, key=None, key_w=5.0, dots=True, flat=False, rim=0.0):
    """One printed shape: a flat fill, a halftone mid-tone and one hard shadow plane on its back edge, a cream rim
    light `rim` px wide on its lit edge, and the ink key line."""
    path(cr)
    cr.set_source_rgba(*fill)
    cr.fill()
    if flat:
        return
    if d:
        if dots:
            _band(cr, path, d * 0.62, col("ink", 0.42), dots=True)
        _band(cr, path, d, _shade(fill, 0.36))
    if rim:
        _band(cr, path, -rim, _mix(fill, col("cream"), 0.55))
    if key:
        path(cr)
        cr.set_source_rgba(*key)
        cr.set_line_width(key_w)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()


def _smooth_side(cr, pts, first=True):
    """A smooth curve through pts (Catmull-Rom as cubic Beziers)."""
    if first:
        cr.move_to(*pts[0])
    else:
        cr.line_to(*pts[0])
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        cr.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])


def _limb(a, b, c, wa, wb, wc, round_top=True):
    """A continuous tapered sleeve or trouser leg through a -> b -> c (half-widths wa, wb, wc), bending smoothly at
    b: one shape, no visible joint. Returns (path, inner_point, bend) for the fold lines."""
    def unit(v):
        L = math.hypot(*v) or 1.0
        return v[0] / L, v[1] / L
    d1 = unit((b[0] - a[0], b[1] - a[1]))
    d2 = unit((c[0] - b[0], c[1] - b[1]))
    n1, n2 = (-d1[1], d1[0]), (-d2[1], d2[0])
    nb = unit((n1[0] + n2[0], n1[1] + n2[1])) if abs(n1[0] + n2[0]) + abs(n1[1] + n2[1]) > 1e-3 else n1
    k = min(1.35, 1.0 / max(0.55, nb[0] * n1[0] + nb[1] * n1[1]))
    L = [(a[0] + n1[0] * wa, a[1] + n1[1] * wa), (b[0] + nb[0] * wb * k, b[1] + nb[1] * wb * k),
         (c[0] + n2[0] * wc, c[1] + n2[1] * wc)]
    Rr = [(c[0] - n2[0] * wc, c[1] - n2[1] * wc), (b[0] - nb[0] * wb * k, b[1] - nb[1] * wb * k),
          (a[0] - n1[0] * wa, a[1] - n1[1] * wa)]
    cross = d1[0] * d2[1] - d1[1] * d2[0]
    bend = math.asin(max(-1.0, min(1.0, cross)))

    def path(cr):
        cr.new_sub_path()
        _smooth_side(cr, L)
        _smooth_side(cr, Rr, first=False)
        if round_top:
            ang = math.atan2(-d1[1], -d1[0])
            cr.arc_negative(a[0], a[1], wa, ang + math.pi / 2, ang - math.pi / 2) if False else None
        cr.close_path()
    inner = Rr[1] if cross > 0 else L[1]
    return path, inner, bend, nb


def _closed_smooth(pts, sharp=()):
    """A closed outline through pts, curved (Catmull-Rom) except at the indexes in `sharp` (hem corners)."""
    n = len(pts)

    def path(cr):
        cr.new_sub_path()
        cr.move_to(*pts[0])
        for i in range(n):
            p1, p2 = pts[i], pts[(i + 1) % n]
            if i in sharp or (i + 1) % n in sharp:
                cr.line_to(*p2)
                continue
            p0, p3 = pts[(i - 1) % n], pts[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            cr.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
        cr.close_path()
    return path


def _folds(cr, inner, nb, bend, w, color):
    """One or two fold creases on the inside of a bend."""
    if abs(bend) < 0.22:
        return
    sgn = 1 if bend > 0 else -1
    for i, f in enumerate((0.55, 0.85)[:1 + (abs(bend) > 0.7)]):
        x0, y0 = inner
        tx, ty = nb[0] * sgn * w * f, nb[1] * sgn * w * f
        cr.move_to(x0 - ty * 0.25, y0 + tx * 0.25)
        cr.curve_to(x0 + tx * 0.5, y0 + ty * 0.5, x0 + tx * 0.8, y0 + ty * 0.8 - 2, x0 + tx, y0 + ty)
    cr.set_source_rgba(*color)
    cr.set_line_width(3.0)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()


def _blink(t, seed):
    """True while the eyes are shut: a 0.12 s blink every 2-5 s."""
    r = random.Random(seed * 7919)
    tt = r.uniform(0.5, 2.5)
    while tt < t + 1:
        if tt <= t < tt + 0.12:
            return True
        tt += r.uniform(2.0, 5.0)
    return False


# ---------------------------------------------------------------- headgear (head space: centre (0,0), facing +x)
def _headgear_parts(kind, R):
    """[(path, colour name or None for the side colour)] for a nation's helmet or a civilian / leader hat."""
    P = []
    if kind == "germany":              # flared helmet: deep dome, the skirt flaring at the back and sides
        P.append((_poly_curve([(-1.05, 0.05), "c", (-1.15, -1.3), (1.1, -1.35), (1.05, -0.2), (1.12, -0.12),
                               (0.75, -0.18), "c", (0.2, -0.22), (-0.55, -0.2), (-0.8, -0.05), (-1.32, 0.38),
                               (-1.3, 0.2)], R), None))
    elif kind == "britain":            # flat dish: a wide flat brim and a shallow crown
        P.append((_ellipse(0.0, -0.62, 1.6, 0.26, R), None))
        P.append((_poly_curve([(-0.82, -0.66), "c", (-0.75, -1.3), (0.75, -1.3), (0.82, -0.66)], R), None))
    elif kind == "usa":                # round M1
        P.append((_poly_curve([(-1.12, -0.05), "c", (-1.2, -1.45), (1.2, -1.45), (1.12, -0.05), (1.28, 0.05),
                               (-1.28, 0.05)], R), None))
    elif kind == "soviet":             # rounded helmet with a slight flare
        P.append((_poly_curve([(-1.1, -0.05), "c", (-1.15, -1.38), (1.15, -1.38), (1.1, -0.05), (1.22, 0.1),
                               (-1.22, 0.1)], R), None))
    elif kind == "france":             # crested helmet
        P.append((_poly_curve([(-1.32, -0.08), (1.32, -0.08), (0.95, -0.32), "c", (0.95, -1.25), (-0.95, -1.25),
                               (-0.95, -0.32)], R), None))
        P.append((_poly_curve([(-0.6, -1.0), "c", (-0.35, -1.48), (0.35, -1.48), (0.6, -1.0), (0.42, -0.94), "c",
                               (0.2, -1.2), (-0.2, -1.2), (-0.42, -0.94)], R), None))
    elif kind == "japan":              # peaked cap with neck flaps at the back
        P.append((_poly_curve([(-0.98, -0.35), (-1.12, 0.6), (-0.5, 0.52), (-0.55, -0.3)], R), None))
        P.append((_poly_curve([(-0.95, -0.32), "c", (-0.95, -1.28), (0.95, -1.28), (0.95, -0.32)], R), None))
        P.append((_poly_curve([(0.4, -0.36), "c", (0.9, -0.44), (1.3, -0.34), (1.48, -0.18), (0.45, -0.26)], R),
                  "ink"))
    elif kind == "italy":              # helmet with a feather plume off the back
        P.append((_plume(R), "#2c3a2a"))
        P.append((_poly_curve([(-1.1, -0.08), "c", (-1.14, -1.38), (1.14, -1.38), (1.1, -0.08), (1.22, 0.04),
                               (-1.22, 0.04)], R), None))
    elif kind == "flatcap":
        P.append((_poly_curve([(-0.98, -0.32), "c", (-1.02, -1.22), (0.95, -1.18), (1.0, -0.42), "c", (1.4, -0.38),
                               (1.58, -0.26), (1.52, -0.16), (-0.98, -0.22)], R), "#7c6c52"))
    elif kind in ("hat", "homburg"):
        c = "#5d5348" if kind == "hat" else "#34302c"
        P.append((_ellipse(0.0, -0.66, 1.5, 0.24, R), c))
        top = -1.42 if kind == "homburg" else -1.22
        P.append((_poly_curve([(-0.8, -0.64), (-0.82, -1.36), "c", (-0.3, top - 0.1), (0.3, top - 0.1),
                               (0.82, -1.36), (0.8, -0.64)], R), c))
    elif kind == "bowler":
        P.append((_ellipse(0.0, -0.64, 1.32, 0.2, R), "#26221f"))
        P.append((_poly_curve([(-0.84, -0.66), "c", (-0.88, -1.7), (0.88, -1.7), (0.84, -0.66)], R), "#26221f"))
    elif kind == "scarf":
        P.append((_poly_curve([(-1.1, 0.25), "c", (-1.28, -1.38), (1.15, -1.38), (0.95, -0.1), (0.75, -0.2), "c",
                               (0.85, -0.95), (-0.9, -0.95), (-0.86, 0.15)], R), "#9b5446"))
    return P


def _poly_curve(spec, R):
    """A path from points in head units (x R); "c" makes the next three points a cubic curve."""
    def path(cr):
        cr.new_sub_path()
        it = iter(spec)
        x, y = next(it)
        cr.move_to(x * R, y * R)
        for q in it:
            if q == "c":
                a, b, c = next(it), next(it), next(it)
                cr.curve_to(a[0] * R, a[1] * R, b[0] * R, b[1] * R, c[0] * R, c[1] * R)
            else:
                cr.line_to(q[0] * R, q[1] * R)
        cr.close_path()
    return path


def _ellipse(cx, cy, rx, ry, R):
    def path(cr):
        cr.new_sub_path()
        cr.save()
        cr.translate(cx * R, cy * R)
        cr.scale(rx * R, ry * R)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
    return path


def _plume(R):
    def path(cr):
        cr.new_sub_path()
        cr.move_to(-0.7 * R, -0.75 * R)
        cr.curve_to(-1.3 * R, -1.25 * R, -2.0 * R, -0.7 * R, -2.25 * R, 0.25 * R)
        cr.curve_to(-1.75 * R, -0.25 * R, -1.3 * R, -0.45 * R, -0.75 * R, -0.45 * R)
        cr.close_path()
    return path


# ---------------------------------------------------------------- the figure
LEADER_SIDE = {"hitler": "axis", "stalin": "soviet", "churchill": "allies", "roosevelt": "allies",
               "mussolini": "axis_it", "hirohito": "axis_jp", "chamberlain": "allies"}
HAIR = {"hitler": "#221d1a", "stalin": "#2b2724", "roosevelt": "#8d8a84", "hirohito": "#1f1c1a",
        "chamberlain": "#9a958c", "churchill": "#b9b2a3"}


# What each figure wears (all plain, no symbols). skirt: where the jacket ends, in torso lengths from the hips
# (0.27 = at the belt, a battledress blouse; negative = below the hips: coats); boots: tall | ankle | puttees |
# gaiters | shoes; style adds the details (lapels and a tie for suits, a bow tie, a cape, a buttoned-back coat).
DRESS = {
    "germany": dict(skirt=0.02, boots="tall", pockets=True, buttons=4, straps=True),
    "britain": dict(skirt=0.27, boots="gaiters", pockets=True, buttons=2, straps=True),
    "usa": dict(skirt=0.04, boots="ankle", pockets=True, buttons=4, straps=False),
    "soviet": dict(skirt=-0.06, boots="tall", pockets=True, buttons=2, straps=True),
    "france": dict(skirt=-0.55, boots="puttees", pockets=False, buttons=5, straps=True, style="coat_back"),
    "japan": dict(skirt=0.04, boots="puttees", pockets=True, buttons=4, straps=True),
    "italy": dict(skirt=0.04, boots="puttees", pockets=True, buttons=4, straps=True),
    "china": dict(skirt=0.04, boots="puttees", pockets=True, buttons=4, straps=False),
    "civilian": dict(skirt=-0.3, boots="shoes", pockets=False, buttons=3, straps=False, style="coat"),
    "hitler": dict(jacket="axis", skirt=0.04, boots="shoes", pockets=True, buttons=4, straps=False),
    "stalin": dict(jacket="#7d6a52", trousers="#4d4134", skirt=-0.06, boots="tall", pockets=True, buttons=4,
                   straps=False),
    "churchill": dict(jacket="#2a3446", trousers="#262b33", skirt=-0.42, boots="shoes", pockets=False, buttons=3,
                      straps=False, style="coat", tie="bow"),
    "roosevelt": dict(jacket="#3a3f4a", trousers="#33363d", skirt=0.0, boots="shoes", pockets=False, buttons=2,
                      straps=False, style="suit", tie="tie", cape="#22324a"),
    "chamberlain": dict(jacket="#4a4a4c", trousers="#3b3b3e", skirt=0.0, boots="shoes", pockets=False, buttons=2,
                        straps=False, style="suit", tie="tie"),
    "mussolini": dict(jacket="axis_it", skirt=0.04, boots="tall", pockets=True, buttons=4, straps=True),
    "hirohito": dict(jacket="axis_jp", skirt=0.04, boots="shoes", pockets=True, buttons=5, straps=True),
}


class Figure:
    def __init__(self, nation=None, leader=None, civilian=None, x=0.0, y=0.0, scale=1.0, facing=1, prop=None,
                 color=None, seed=0, name=None, flat=False):
        self.nation, self.leader, self.civilian = nation, leader, civilian
        self.x, self.y, self.scale, self.facing = x, y, scale, facing
        self.seed = seed
        self.flat = flat or color is not None                 # crowd silhouettes: one tone, a highlight
        self.tone = col(color) if color else None
        self.prop = prop
        if leader and prop is None:
            self.prop = {"chamberlain": "umbrella"}.get(leader)
        self.mouth_prop = {"stalin": "pipe", "churchill": "cigar", "roosevelt": "holder"}.get(leader)
        self.name = name
        self.bulk = 1.22 if leader == "churchill" else 1.0
        self.dress = dict(DRESS.get(leader) or DRESS.get(nation) or DRESS["civilian"])
        side = NATION_SIDE.get(nation) or LEADER_SIDE.get(leader)
        jc = self.dress.get("jacket")
        if jc:
            self.tunic = col(jc)
        elif side:
            self.tunic = col(side)
        else:                                                   # civilians: coats in khaki / olive
            self.tunic = col(random.Random(seed).choice(("khaki", "olive", "#8a7b5c")))
        tc = self.dress.get("trousers")
        self.trousers = col(tc) if tc else _shade(self.tunic, 0.28)

    # ------------------------------------------------------------ public
    def draw(self, cr, t, track=None, move=None, face=None):
        p = track_pose(track or [(0.0, "stand")], t, self.seed)
        x, y = self._pos(t, move)
        self.draw_pose(cr, t, p, x, y, face)

    def joints(self, t, track=None, move=None):
        """World positions of the joints at time t (e.g. to attach props, or to place a handshake)."""
        p = track_pose(track or [(0.0, "stand")], t, self.seed)
        x, y = self._pos(t, move)
        J = skeleton(p)
        off = _ground_offset(J, p) + p.get("bob", 0.0) + p.get("drop", 0.0)
        s, f = self.scale, self.facing
        return {k: (x + f * s * v[0], y + s * (v[1] + off)) for k, v in J.items()}

    # ------------------------------------------------------------ internals
    def _pos(self, t, move):
        x, y = self.x, self.y
        if move:
            move = sorted(move, key=lambda m: m[0])
            m = move[0] if t <= move[0][0] else move[-1]
            for a, b in zip(move, move[1:]):
                if a[0] <= t <= b[0]:
                    u = (t - a[0]) / max(1e-6, b[0] - a[0])
                    m = (t, lerp(a[1], b[1], u), lerp(a[2], b[2], u) if len(a) > 2 and len(b) > 2 else None)
                    break
            x = m[1]
            if len(m) > 2 and m[2] is not None:
                y = m[2]
        return x, y

    def _k(self):
        return None if self.flat else col("ink")

    def _fill(self, c):
        return self.tone if self.flat else c

    def draw_pose(self, cr, t, p, x, y, face=None):
        J = skeleton(p)
        off = _ground_offset(J, p) + p.get("bob", 0.0) + p.get("drop", 0.0)
        s, f = self.scale, self.facing
        cr.save()
        cr.translate(x, y)
        cr.scale(s * f, s)
        cr.translate(0, off)
        K, flat = self._k(), self.flat
        kw = 5.0 / max(0.6, s) ** 0.3
        # far side first, in a darker tone (it is behind the body)
        far_tr, far_tu = _shade(self.trousers, 0.25), _shade(self.tunic, 0.25)
        self._leg(cr, J, "f", far_tr, K, kw, flat)
        self._arm(cr, J, "f", far_tu, K, kw, flat, p)
        if self.prop == "rifle" and not flat:
            self._rifle(cr, J, p, t, K)
        self._leg(cr, J, "n", self.trousers, K, kw, flat)
        self._torso(cr, J, p, K, kw, flat)
        self._head(cr, t, J, p, face, K, kw, flat)
        self._arm(cr, J, "n", self.tunic if not self.dress.get("cape") else self.tunic, K, kw, flat, p)
        if self.prop in ("paper", "pen", "umbrella") and not flat:
            self._held(cr, J, p, t, K)
        cr.restore()

    # ------------------------------------------------------------ body parts
    def _leg(self, cr, J, side, c, K, kw, flat):
        """Trouser leg (one continuous shape, hip to ankle), then the nation's boots."""
        hip, kn, ft = J["hip"], J["kn_" + side], J["ft_" + side]
        hip = (hip[0], hip[1] - 8)
        fill = self._fill(c)
        path, inner, bend, nb = _limb(hip, kn, ft, 31 * self.bulk, 23, 17)
        _printed(cr, path, fill, 14, K, kw, flat=flat, rim=0 if flat else 3.5)
        if not flat:
            _folds(cr, inner, nb, bend, 18, _shade(fill, 0.55))
        boots = self.dress.get("boots", "ankle")
        ink = self._fill(col("ink"))
        dx, dy = ft[0] - kn[0], ft[1] - kn[1]
        if boots == "tall":                                         # tall boots up to just below the knee
            top = (kn[0] + dx * 0.16, kn[1] + dy * 0.16)
            _printed(cr, _capsule(top, ft, 18, 16), ink, 6, K, kw * 0.8, dots=False, flat=flat, rim=0 if flat else 3)
        elif boots in ("puttees", "gaiters") and not flat:          # wrapped puttees / short gaiters
            top = (kn[0] + dx * (0.35 if boots == "puttees" else 0.7), kn[1] + dy * (0.35 if boots == "puttees"
                                                                                       else 0.7))
            _printed(cr, _capsule(top, ft, 17, 15), col("khaki"), 6, K, kw * 0.7, dots=False)
            n = 6 if boots == "puttees" else 2
            for i in range(1, n):
                u = i / n
                px, py = top[0] + (ft[0] - top[0]) * u, top[1] + (ft[1] - top[1]) * u
                _line(cr, [(px - 15, py - 4), (px + 15, py + 5)], 2.2, _shade(col("khaki"), 0.45))
        # the boot / shoe: a solid sole on the ground and a rounded toe
        h = 22 if boots != "shoes" else 16
        foot = _poly_curve([(-0.5, -0.9), (0.3, -0.95), "c", (0.9, -0.85), (1.55, -0.55), (1.6, 0.0), (1.62, 0.32),
                            (-0.62, 0.32)], h)
        cr.save()
        cr.translate(ft[0], ft[1])
        _printed(cr, foot, ink, 0, K, kw * 0.8, flat=flat, rim=0 if flat else 2.5)
        cr.restore()

    def _arm(self, cr, J, side, c, K, kw, flat, p):
        """Sleeve (one continuous shape, shoulder to cuff) and a mitten hand."""
        sh, el, hd = J["sh"], J["el_" + side], J["hand_" + side]
        fill = self._fill(c)
        dx, dy = hd[0] - el[0], hd[1] - el[1]
        L = math.hypot(dx, dy) or 1
        cuff = (hd[0] - dx / L * 12, hd[1] - dy / L * 12)
        path, inner, bend, nb = _limb(sh, el, cuff, 27 * self.bulk, 19, 15)
        _printed(cr, path, fill, 12, K, kw, flat=flat, rim=0 if flat else 3.5)
        if not flat:
            _folds(cr, inner, nb, bend, 15, _shade(fill, 0.55))
            _line(cr, [(cuff[0] - dy / L * 13, cuff[1] + dx / L * 13), (cuff[0] + dy / L * 13, cuff[1] - dx / L * 13)],
                  4.0, _shade(fill, 0.5))                           # the cuff seam
        self._hand(cr, el, hd, p.get("hand_" + side, "open"), K, flat)

    def _hand(self, cr, el, hd, kind, K, flat):
        """A big readable mitten with a thumb (or a fist, splayed fingers, crossed fingers)."""
        skin = self._fill(col("cream"))
        dx, dy = hd[0] - el[0], hd[1] - el[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        if px < 0:                                                   # the thumb on the front side
            px, py = -px, -py
        cr.save()
        cr.translate(hd[0] - ux * 8, hd[1] - uy * 8)
        cr.transform(cairo.Matrix(ux, uy, px, py, 0, 0))            # x along the forearm, y toward the front
        if kind == "fist":
            shape = _poly_curve([(-0.2, -0.75), "c", (0.6, -0.95), (1.25, -0.8), (1.25, 0.0), "c", (1.25, 0.8),
                                 (0.6, 0.95), (-0.2, 0.75)], 14)
        else:
            shape = _poly_curve([(-0.15, -0.7), "c", (0.9, -0.85), (1.75, -0.7), (1.75, -0.05), "c", (1.75, 0.55),
                                 (1.2, 0.68), (0.75, 0.62), (0.7, 0.95), "c", (0.55, 1.25), (0.15, 1.15),
                                 (0.05, 0.7)], 13)
        _printed(cr, shape, skin, 5, K, 3.4, dots=False, flat=flat)
        if not flat and kind == "crossed":                          # two fingers crossed, held up
            for sgn in (1, -1):
                a = (20, -4 * sgn)
                b = (44, 7 * sgn)
                _printed(cr, _capsule(a, b, 5.0, 4.2), skin, 0, K, 2.8)
        elif not flat and kind == "splay":
            for a_ in (-0.55, -0.18, 0.18, 0.55):
                _printed(cr, _capsule((18, 0), (18 + 24 * math.cos(a_), 24 * math.sin(a_)), 4.4, 3.6), skin, 0, K,
                         2.6)
        cr.restore()

    def _torso(self, cr, J, p, K, kw, flat):
        """The jacket: broad chest tapering to the belt, then the skirt flaring over the hips (or a battledress
        blouse ending at the belt, or a long coat), with collar, pocket flaps, buttons and shoulder straps."""
        H_, N = J["hip"], J["neck"]
        L = math.hypot(N[0] - H_[0], N[1] - H_[1]) or 1
        u = ((N[0] - H_[0]) / L, (N[1] - H_[1]) / L)                # up the spine
        v = (-u[1], u[0])                                            # toward the front
        if v[0] < 0:
            v = (-v[0], -v[1])
        b = self.bulk
        belly = 16 if self.leader == "churchill" else 0
        D = self.dress
        skirt = D.get("skirt", 0.04)
        fill = self._fill(self.tunic)

        def P(a, w):
            return (H_[0] + u[0] * a * L + v[0] * w, H_[1] + u[1] * a * L + v[1] * w)
        if skirt > 0.2 and not flat:                                 # a blouse: the trousers show at the hips
            hips = _poly([P(0.3, -27 * b), P(0.3, 27 * b + belly), P(-0.04, 30 * b + belly * 0.5),
                          P(-0.06, -29 * b)])
            _printed(cr, hips, self._fill(self.trousers), 12, K, kw, flat=flat)
        sk = min(skirt, 0.27)
        flare = 6 + max(0.0, -skirt) * 18
        w = 0.0 if belly else 1.0                                   # the waist nips in (not on Churchill)
        body = [P(sk, -33 * b - flare), P(0.3, -25 * b - 3 * (1 - w)), P(0.55, -30 * b), P(0.84, -35 * b),
                P(0.99, -28), P(1.04, -6), P(1.04, 16), P(0.9, 37 * b), P(0.72, 42 * b + belly * 0.4),
                P(0.48, 31 * b + belly - 2 * w), P(0.3, 27 * b + belly + 2 * (1 - w)), P(sk, 35 * b + belly * 0.6 +
                                                                                           flare)]
        if skirt < -0.05:                                            # a long coat: the skirts hang to the knees
            body = [P(skirt, -34 * b - flare)] + body[1:-1] + [P(skirt, 36 * b + flare)]
        path = _closed_smooth(body, sharp=(0, len(body) - 1))
        _printed(cr, path, fill, 22, K, kw, flat=flat, rim=0 if flat else 4.5)
        if flat:
            return
        dark = _shade(fill, 0.55)
        if D.get("style") == "coat_back":                            # skirts buttoned back: a folded-back corner
            fold = _poly([P(skirt + 0.02, 30 * b), P(0.05, 34 * b), P(skirt + 0.3, 14 * b)])
            _printed(cr, fold, _mix(fill, col("cream"), 0.25), 0, K, 3.0)
        # belt (or the line where a suit jacket buttons)
        if D.get("style") not in ("suit", "coat"):
            _printed(cr, _poly([P(0.33, -28 * b), P(0.33, 30 * b + belly), P(0.27, 30 * b + belly),
                                P(0.27, -28 * b)]), _shade(fill, 0.62), 0, K, 3.0)
            _printed(cr, _poly([P(0.335, 20 * b), P(0.335, 31 * b + belly), P(0.265, 31 * b + belly),
                                P(0.265, 20 * b)]), col("gold"), 0, K, 2.4)
        # buttons down the front edge
        for i in range(D.get("buttons", 3)):
            a_ = 0.4 + i * 0.5 / max(1, D.get("buttons", 3))
            x, y = P(a_, 25 * b + belly * (0.6 if a_ < 0.6 else 0.2))
            cr.arc(x, y, 3.6, 0, 2 * math.pi)
            cr.set_source_rgba(*col("gold") if D.get("style") != "suit" else dark)
            cr.fill()
        if D.get("pockets"):                                         # a chest pocket flap
            _printed(cr, _poly([P(0.74, 4), P(0.74, 24 * b), P(0.66, 24 * b), P(0.66, 4)]), _shade(fill, 0.18), 0,
                     K, 2.8)
            x, y = P(0.71, 14 * b)
            cr.arc(x, y, 3.0, 0, 2 * math.pi)
            cr.set_source_rgba(*col("gold"))
            cr.fill()
        if D.get("straps"):                                          # shoulder strap along the top of the shoulder
            _line(cr, [P(0.97, -16), P(0.97, 12)], 7, dark)
        if D.get("style") in ("suit", "coat"):                       # lapels
            _line(cr, [P(1.0, 14), P(0.7, 22 * b), P(0.55, 27 * b + belly * 0.6)], 3.4, col("ink"))
        tie = D.get("tie")
        if tie == "tie":
            _printed(cr, _poly([P(0.98, 14), P(0.98, 20), P(0.62, 25), P(0.58, 21)]), col("#7a2a24"), 0, K, 2.4)
        # collar (and a bow tie)
        _printed(cr, _poly([P(1.08, -8), P(1.08, 16), P(0.95, 20), P(0.95, -10)]), dark, 0, K, 3.0)
        if tie == "bow":
            x, y = P(1.0, 20)
            _printed(cr, _poly([(x - 9, y - 7), (x + 9, y + 7), (x + 9, y - 7), (x - 9, y + 7)]), col("#6a2a3a"), 0, K,
                     2.4)
        nk = _capsule(P(1.02, 4), (N[0] + u[0] * 16 + v[0] * 2, N[1] + u[1] * 16 + v[1] * 2), 12, 11)
        _printed(cr, nk, col("cream"), 5, K, 3.2, dots=False)
        if D.get("cape"):                                            # Roosevelt's cape over the shoulders
            cape = _poly_curve([(0, 0), (0, 0)], 1)
            pts = [P(1.02, -30 * b), P(1.02, 22 * b), P(0.5, 40 * b), P(0.42, -44 * b)]
            _printed(cr, _poly(pts), col(D["cape"]), 18, K, kw, rim=4)
            del cape

    def _head(self, cr, t, J, p, face_over, K, kw, flat):
        hx, hy = J["head"]
        face = dict(brow="neutral", mouth="line", sweat=0.0, look=(0.0, 0.0))
        face.update(p.get("face") or {})
        face.update(face_over or {})
        face["blink"] = _blink(t, self.seed)
        kind = self.nation or self.civilian or {"churchill": "bowler", "chamberlain": "homburg"}.get(self.leader)
        spec = dict(R=HEAD_R * (1.1 if self.leader == "churchill" else 1.0), leader=self.leader, nation=self.nation,
                    civilian=self.civilian, headgear=kind, side=NATION_SIDE.get(self.nation) or
                    LEADER_SIDE.get(self.leader), turn=max(-1.0, min(1.0, p.get("turn", 0.0))), flat=flat,
                    tone=self.tone, seed=self.seed, mouth_prop=self.mouth_prop, key_w=kw)
        cr.save()
        cr.translate(hx, hy)
        cr.rotate((p.get("lean", 0.0) + p.get("nod", 0.0) * 0.6) * 0.55)
        draw_head(cr, spec, face, t)
        cr.restore()

    def _rifle(self, cr, J, p, t, K):
        """The rifle: aimed level from the shoulder through the front hand, or carried up from the near hand."""
        wood, metal = col("#6b4a2e"), col("ink")
        if p.get("aim", 0) > 0.5:
            a = (J["sh"][0] + 8, J["sh"][1] + 14)
            front = J["hand_n"] if J["hand_n"][0] > J["hand_f"][0] else J["hand_f"]
            dx, dy = front[0] - a[0], (front[1] - a[1]) * 0.35
            back = 16
        else:
            a = J["hand_n"]
            dx, dy, back = 0.35, -1.0, 56
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        s = (a[0] - ux * back, a[1] - uy * back)
        m = (a[0] + ux * (120 - back), a[1] + uy * (120 - back))
        e = (a[0] + ux * (205 - back), a[1] + uy * (205 - back))
        _printed(cr, _capsule(s, m, 8, 5.5), wood, 4, K, 3.2, dots=False)
        _printed(cr, _capsule((m[0] - ux * 14, m[1] - uy * 14), e, 3.6, 3.0), metal, 0, None)
        if p.get("flash", 0) > 0.5:                                   # muzzle flash only
            cr.save()
            cr.translate(e[0] + ux * 20, e[1] + uy * 20)
            cr.rotate(math.atan2(uy, ux))
            pts = []
            for i in range(12):
                a_ = i / 12 * 2 * math.pi
                r = 30 if i % 2 == 0 else 11
                pts.append((r * math.cos(a_) * 1.35, r * math.sin(a_)))
            _printed(cr, _poly(pts), col("fire"), 0, col("alert"), 3.0)
            cr.restore()

    def _held(self, cr, J, p, t, K):
        hx, hy = J["hand_n"]
        ink = col("ink")
        if self.prop == "paper":
            cr.save()
            up = p.get("prop_up", 0.0)
            cr.translate(hx + 6, hy - 26 * up)
            cr.rotate(-0.12 + 0.05 * math.sin(t * 5) * up)
            _printed(cr, _poly([(-20, -30), (22, -30), (22, 26), (-20, 26)]), col("white"), 8, ink, 3.0)
            for i in range(4):
                _line(cr, [(-12, -18 + i * 11), (14, -18 + i * 11)], 2.2, col("ink_soft"))
            cr.restore()
        elif self.prop == "pen":
            _line(cr, [(hx - 3, hy + 6), (hx + 14, hy - 22)], 4.4, ink)
        elif self.prop == "umbrella":                                 # furled, held like a walking stick
            _line(cr, [(hx, hy - 8), (hx + 12, hy + 160)], 4.0, ink)
            _printed(cr, _poly([(hx + 3, hy + 12), (hx + 22, hy + 100), (hx + 6, hy + 106)]), col("#26221f"), 0, ink,
                     2.4)
            cr.arc(hx - 9, hy - 8, 10, math.pi, 2 * math.pi)
            cr.set_line_width(4.0)
            cr.set_source_rgba(*ink)
            cr.stroke()


# ---------------------------------------------------------------- heads (the hook and the fallback)
def draw_head(cr, spec, expression, t):
    """THE HEAD HOOK (helper 2 draws the heads and faces in channels/ww2/kit/heads.py; until that module exists,
    helper 1's poster head below is used). Called by every Figure in head space:

        origin = the centre of the skull, +x = the way the figure faces (profile front), +y = down, units = px,
        R = spec["R"] the skull radius (the neck meets the skull around (-0.1R, +0.95R)); the body has already been
        drawn, so the head paints over the collar. Any rotation (lean, nod) is already applied.

    spec:       {"R": float, "leader": str|None, "nation": str|None, "civilian": str|None,
                 "headgear": str|None (nation name, "flatcap", "hat", "homburg", "bowler", "scarf"),
                 "side": palette name|None, "turn": -1..1 (3/4 toward the viewer), "flat": bool (one-tone crowd
                 silhouette in spec["tone"]), "tone": rgba|None, "seed": int, "mouth_prop": "pipe"|"cigar"|
                 "holder"|None, "key_w": key-line width}
    expression: {"brow": "neutral|angry|worried|sad", "mouth": "line|smile|o|grit|frown", "sweat": 0..1,
                 "look": (dx, dy), "blink": bool}
    """
    fn = _HEAD_IMPL.get("fn")
    if fn is None:
        try:
            from channels.ww2.kit import heads
            fn = heads.draw_head
        except ImportError:
            fn = _head_fallback
        _HEAD_IMPL["fn"] = fn
    fn(cr, spec, expression, t)


_HEAD_IMPL = {}


def _head_fallback(cr, s, face, t):
    """helper 1's poster head (the fallback until channels/ww2/kit/heads.py lands): see draw_head()."""
    R, turn, flat = s["R"], s["turn"], s["flat"]
    K, kw = (None if flat else col("ink")), s.get("key_w", 5.0)
    skin = (s['tone'] if flat else col("cream"))
    jaw = 0.98 if s['leader'] == "mussolini" else 0.82
    head = _poly_curve([(-0.98, 0.05), "c", (-1.05, -1.25), (0.85, -1.3), (0.88, -0.42), (0.93, -0.2),
                        (1.12, 0.12), (0.95, 0.24), (0.97, 0.46), (0.92, 0.58), (0.86, jaw),
                        (0.12, 0.98 if jaw > 0.9 else 0.94), "c", (-0.3, 0.86), (-0.55, 0.55), (-0.62, 0.42)], R)
    _printed(cr, head, skin, R * 0.55, K, kw, flat=flat)
    if flat:                                                    # a silhouette: a rim of light on the face
        _line(cr, [(0.88 * R, -0.42 * R), (0.95 * R, -0.18 * R), (1.22 * R, 0.14 * R)], 3.0, col("cream", 0.9))
        for path, c in _headgear_parts(s['nation'] or s['civilian'] or {"churchill": "bowler",
                                       "chamberlain": "homburg"}.get(s['leader'], ""), R):
            _printed(cr, path, s['tone'], 0, None, flat=True)
        return
    ink = col("ink")
    # hair
    hair = HAIR.get(s['leader'])
    if s['leader'] == "hitler":                                   # side-swept: a fringe down over the brow
        hp = _poly_curve([(-0.98, 0.1), "c", (-1.08, -1.32), (0.8, -1.38), (0.86, -0.5), (0.72, -0.28),
                          (0.4, -0.62), (0.05, -0.55), (-0.45, -0.15)], R)
        _printed(cr, hp, col(hair), 0, K, 3.5)
    elif s['leader'] in ("stalin", "roosevelt", "hirohito"):       # swept back / short
        hl = -0.86 if s['leader'] == "stalin" else -0.78
        hp = _poly_curve([(-0.98, 0.15), "c", (-1.1, -1.32), (0.6, -1.4), (0.62, hl), "c", (0.2, -0.75),
                          (-0.4, -0.45), (-0.72, 0.2)], R)
        _printed(cr, hp, col(hair), 0, K, 3.5)
    # ear
    cr.arc(-0.12 * R, 0.05 * R, 0.2 * R, -1.9, 1.9)
    cr.set_source_rgba(*ink)
    cr.set_line_width(3.2)
    cr.stroke()
    # eyes and brows (profile; the second eye shows in a 3/4 turn)
    lx, ly = face["look"]
    blink = face.get("blink", False)
    eyes = [(0.62 + 0.06 * turn, -0.12)] + ([(0.2 + 0.2 * turn, -0.12)] if turn > 0.35 else [])
    for i, (ex, ey) in enumerate(eyes):
        X, Y = ex * R + lx * 0.5, ey * R + ly * 0.5
        k = 1.0 if i == 0 else 0.8
        if blink:
            _line(cr, [(X - 6 * k, Y), (X + 6 * k, Y)], 3.2, ink)
        else:
            cr.save()
            cr.translate(X, Y)
            cr.scale(3.6 * k, 5.0 * k)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(*ink)
            cr.fill()
        b = face["brow"]
        dy0, dy1 = {"angry": (-6, 3), "worried": (3, -7), "sad": (2, -5)}.get(b, (-2, -2))
        bx, by = ex * R, (ey - 0.36) * R
        path = _poly([(bx - 10 * k, by + dy0), (bx + 10 * k, by + dy1), (bx + 10 * k, by + dy1 + 4.5),
                      (bx - 10 * k, by + dy0 + 4.5)])
        path(cr)
        cr.set_source_rgba(*ink)
        cr.fill()
    if s['leader'] in ("roosevelt", "hirohito"):                  # pince-nez / round glasses
        ex = eyes[0][0] * R
        cr.arc(ex, -0.14 * R, 0.3 * R if s['leader'] == "hirohito" else 0.24 * R, 0, 2 * math.pi)
        cr.set_source_rgba(*ink)
        cr.set_line_width(2.6)
        cr.stroke()
        _line(cr, [(ex + 0.27 * R, -0.16 * R), (0.92 * R, -0.12 * R)], 2.4, ink)
        if s['leader'] == "hirohito":
            _line(cr, [(ex - 0.3 * R, -0.16 * R), (-0.1 * R, -0.1 * R)], 2.4, ink)
    # moustache (under the nose)
    mo = {"hitler": ((0.6, 0.28), 0.3, 0.18), "stalin": ((0.46, 0.29), 0.48, 0.2),
          "chamberlain": ((0.56, 0.3), 0.36, 0.13), "hirohito": ((0.64, 0.31), 0.26, 0.1)}.get(s['leader'])
    if mo:
        (mx, my), w, h = mo
        if s['leader'] == "stalin":
            pth = _poly_curve([(mx, my), "c", (mx + 0.1, my - 0.12), (mx + 0.36, my - 0.12), (mx + w, my + 0.04),
                               "c", (mx + 0.36, my + 0.14), (mx + 0.12, my + 0.22), (mx - 0.05, my + 0.2)], R)
        else:
            pth = _poly([(mx * R, my * R), ((mx + w) * R, my * R), ((mx + w) * R, (my + h) * R),
                         (mx * R, (my + h) * R)])
        _printed(cr, pth, col(HAIR.get(s['leader'], "#2b2724")), 0, None)
    # mouth
    mx, my = 0.8 * R, 0.55 * R
    m = face["mouth"]
    if m == "smile":
        cr.move_to(mx - 12, my - 4)
        cr.curve_to(mx - 6, my + 4, mx + 2, my + 4, mx + 8, my - 1)
        cr.set_source_rgba(*ink)
        cr.set_line_width(3.4)
        cr.stroke()
    elif m == "frown":
        cr.move_to(mx - 12, my + 4)
        cr.curve_to(mx - 6, my - 3, mx + 2, my - 3, mx + 7, my + 2)
        cr.set_source_rgba(*ink)
        cr.set_line_width(3.4)
        cr.stroke()
    elif m == "o":
        cr.save()
        cr.translate(mx, my + 2)
        cr.scale(5, 7)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*col("#4a2420"))
        cr.fill()
    elif m == "grit":
        _printed(cr, _poly([(mx - 12, my - 4), (mx + 7, my - 4), (mx + 7, my + 5), (mx - 12, my + 5)]),
                 col("white"), 0, ink, 2.4)
    else:
        _line(cr, [(mx - 12, my), (mx + 6, my)], 3.4, ink)
    # mouth props
    if s['mouth_prop'] == "pipe":
        _line(cr, [(mx + 4, my + 1), (mx + 26, my + 9)], 4.4, col("#3b281c"))
        _printed(cr, _poly([(mx + 22, my + 2), (mx + 36, my + 2), (mx + 34, my + 22), (mx + 24, my + 22)]),
                 col("#5b3a26"), 3, ink, 2.6, dots=False)
    elif s['mouth_prop'] == "cigar":
        cr.save()
        cr.translate(mx + 4, my + 1)
        cr.rotate(0.15)
        _printed(cr, _poly([(0, -4.5), (34, -4.5), (34, 4.5), (0, 4.5)]), col("#7a4a2a"), 2, ink, 2.4,
                 dots=False)
        cr.arc(36, 0, 3.6, 0, 2 * math.pi)
        cr.set_source_rgba(*col("fire"))
        cr.fill()
        cr.restore()
        _smoke(cr, t, mx + 46, my - 2)
    elif s['mouth_prop'] == "holder":
        _line(cr, [(mx + 4, my), (mx + 36, my - 20)], 3.0, ink)
        _line(cr, [(mx + 36, my - 20), (mx + 46, my - 26)], 5.0, col("white"))
        _smoke(cr, t, mx + 48, my - 32)
    # sweat
    if face.get("sweat", 0) > 0:
        k = face["sweat"] * 1.3
        sx, sy = -0.55 * R, -0.75 * R + 4 * math.sin(t * 3)
        pth = _poly_curve([(sx / R, (sy - 13 * k) / R), "c", ((sx + 7 * k) / R, (sy - 2 * k) / R),
                           ((sx + 7 * k) / R, (sy + 7 * k) / R), (sx / R, (sy + 7 * k) / R), "c",
                           ((sx - 7 * k) / R, (sy + 7 * k) / R), ((sx - 7 * k) / R, (sy - 2 * k) / R),
                           (sx / R, (sy - 13 * k) / R)], R)
        _printed(cr, pth, col("#9fc6d6"), 0, ink, 2.4)
    # headgear
    kind = s['nation'] or s['civilian'] or {"churchill": "bowler", "chamberlain": "homburg"}.get(s['leader'])
    if kind:
        side_c = col(NATION_SIDE.get(s['nation'], "axis")) if s['nation'] else None
        for path, c in _headgear_parts(kind, R):
            _printed(cr, path, col(c) if c else side_c, R * 0.6, ink, kw * 0.9)


def _smoke(cr, t, x, y):
    for i in range(3):
        u = (t * 0.6 + i / 3.0) % 1.0
        cr.arc(x + 6 * math.sin(u * 5 + i), y - 34 * u, 4 + 7 * u, 0, 2 * math.pi)
        cr.set_source_rgba(*col("ink_soft", 0.3 * (1 - u)))
        cr.fill()


# ---------------------------------------------------------------- crowds
_TONES = ("axis", "allies", "soviet", "olive", "khaki", "ink_soft")


def crowd(cr, t, n, x0, x1, y0, y1, scale=0.5, nation=None, pose="cheer", seed=1, facing=None, civilians=None,
          poses=None, tone=None):
    """N small one-tone silhouette figures over a box (back rows higher, a little smaller and lighter), each with its
    own timing offset and headgear: a nation's soldiers, or civilians when nation is None. `poses`: a list to pick
    from per figure (default: just `pose`). `tone`: the silhouette ink (default: the nation's side colour, shaded).
    Drawn back to front."""
    r = random.Random(seed)
    people = []
    base = col(tone) if tone else (_shade(col(NATION_SIDE[nation]), 0.35) if nation in NATION_SIDE else
                                   col("ink_soft"))
    for i in range(n):
        u = r.random()
        y = lerp(y0, y1, u)
        x = r.uniform(x0, x1)
        s = scale * (0.8 + 0.2 * u) * r.uniform(0.92, 1.06)
        kind = nation or (civilians[r.randrange(len(civilians))] if civilians else
                          ("flatcap", "hat", "scarf", None)[r.randrange(4)])
        c = _mix(base, col("paper"), 0.32 * (1 - u))                   # farther rows paler
        f = Figure(nation=kind if kind in NATION_SIDE else None, civilian=None if kind in NATION_SIDE else kind,
                   x=x, y=y, scale=s, facing=facing or r.choice((1, -1)), seed=seed * 1000 + i, flat=True)
        f.tone = c
        people.append((y, f, (poses or [pose])[r.randrange(len(poses or [pose]))], r.uniform(0, 3)))
    for y, f, p, off in sorted(people, key=lambda q: q[0]):
        f.draw(cr, t + off, [(0.0, p)])
