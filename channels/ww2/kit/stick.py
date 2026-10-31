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
HEAD_R = 31.0
NECK = 12.0
TORSO = 136.0
SH_DROP = 20.0
UPPER, FORE = 72.0, 66.0
THIGH, SHIN = 92.0, 88.0
BLEND = 0.28                     # seconds a pose takes to blend in before its key

REST = dict(lean=0.0, nod=0.0, turn=0.0, sh_n=0.12, sh_f=-0.10, el_n=0.12, el_f=0.10, hip_n=0.06, hip_f=-0.06,
            kn_n=0.04, kn_f=0.04, drop=0.0, bob=0.0, sway=0.0, hand_n="open", hand_f="open", ground="feet",
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


def _band(cr, path, d, color, dots=False):
    """The part of the shape left uncovered when a copy of it is slid d px toward the light (+x, the way the figure
    faces): its back edge. Solid in `color`, or halftone dots of it."""
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
    cr.translate(d, 0)
    path(cr)
    cr.restore()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.fill()
    cr.pop_group_to_source()
    cr.paint()
    cr.restore()


def _printed(cr, path, fill, d=0.0, key=None, key_w=5.0, dots=True, flat=False):
    """One printed shape: a flat fill, a halftone mid-tone and a hard shadow on its back edge, the ink key line."""
    if flat:
        path(cr)
        cr.set_source_rgba(*fill)
        cr.fill()
        return
    path(cr)
    cr.set_source_rgba(*fill)
    cr.fill()
    if d:
        if dots:
            _band(cr, path, d * 0.55, col("ink", 0.5), dots=True)
        _band(cr, path, d, _shade(fill))
    if key:
        path(cr)
        cr.set_source_rgba(*key)
        cr.set_line_width(key_w)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
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
        self.bulk = 1.25 if leader == "churchill" else 1.0
        side = NATION_SIDE.get(nation) or LEADER_SIDE.get(leader)
        if side:
            self.tunic = col(side)
            self.trousers = _shade(col(side), 0.3)
        else:                                                   # civilians: coats in khaki / olive
            r = random.Random(seed)
            self.tunic = col(r.choice(("khaki", "olive", "#8a7b5c")))
            self.trousers = _shade(col("olive"), 0.3)
        if leader == "churchill":
            self.tunic, self.trousers = col("#2f3a4a"), col("#262b33")

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
        self._arm(cr, J, "n", self.tunic, K, kw, flat, p)
        if self.prop in ("paper", "pen", "umbrella") and not flat:
            self._held(cr, J, p, t, K)
        cr.restore()

    # ------------------------------------------------------------ body parts
    def _leg(self, cr, J, side, c, K, kw, flat):
        hip, kn, ft = J["hip"], J["kn_" + side], J["ft_" + side]
        _printed(cr, _capsule(hip, kn, 25 * self.bulk, 19), self._fill(c), 12, K, kw, flat=flat)
        _printed(cr, _capsule(kn, ft, 19, 14), self._fill(c), 10, K, kw, flat=flat)
        boot = _poly([(ft[0] - 12, ft[1] - 14), (ft[0] + 10, ft[1] - 14), (ft[0] + 30, ft[1] - 4),
                      (ft[0] + 30, ft[1] + 6), (ft[0] - 14, ft[1] + 6)])
        _printed(cr, boot, self._fill(col("ink")), 0, K, kw * 0.7, flat=flat)

    def _arm(self, cr, J, side, c, K, kw, flat, p):
        sh, el, hd = J["sh"], J["el_" + side], J["hand_" + side]
        _printed(cr, _capsule(sh, el, 19, 15), self._fill(c), 9, K, kw, flat=flat)
        _printed(cr, _capsule(el, hd, 15, 12), self._fill(c), 8, K, kw, flat=flat)
        self._hand(cr, el, hd, p.get("hand_" + side, "open"), K, flat)

    def _hand(self, cr, el, hd, kind, K, flat):
        skin = self._fill(col("cream"))
        dx, dy = hd[0] - el[0], hd[1] - el[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        if kind == "crossed":                                       # two fingers crossed
            for sgn in (1, -1):
                a = (hd[0] + ux * 4 + px * 5 * sgn, hd[1] + uy * 4 + py * 5 * sgn)
                b = (hd[0] + ux * 26 - px * 6 * sgn, hd[1] + uy * 26 - py * 6 * sgn)
                _printed(cr, _capsule(a, b, 4.2, 3.6), skin, 0, K, 2.8, flat=flat)
        elif kind == "splay":
            for a_ in (-0.75, -0.25, 0.25, 0.75):
                ca, sa = math.cos(a_), math.sin(a_)
                vx, vy = ux * ca - uy * sa, ux * sa + uy * ca
                _printed(cr, _capsule(hd, (hd[0] + vx * 20, hd[1] + vy * 20), 4, 3.2), skin, 0, K, 2.6, flat=flat)
        cr.new_sub_path()
        _printed(cr, lambda c: (c.new_sub_path(), c.arc(hd[0] + ux * 4, hd[1] + uy * 4, 10.5, 0, 2 * math.pi)),
                 skin, 4, K, 3.2, dots=False, flat=flat)

    def _torso(self, cr, J, p, K, kw, flat):
        H_, N = J["hip"], J["neck"]
        L = math.hypot(N[0] - H_[0], N[1] - H_[1]) or 1
        u = ((N[0] - H_[0]) / L, (N[1] - H_[1]) / L)                # up the spine
        v = (-u[1], u[0])                                            # toward the front
        if v[0] < 0:
            v = (-v[0], -v[1])
        belly = 14 if self.leader == "churchill" else 0

        def P(a, b):
            return (H_[0] + u[0] * a * L + v[0] * b, H_[1] + u[1] * a * L + v[1] * b)
        b = self.bulk
        body = _poly([P(-0.04, -31 * b), P(0.3, -26 * b), P(0.74, -33 * b), P(0.98, -24), P(1.02, 0), P(0.98, 16),
                      P(0.72, 38 * b + belly * 0.5), P(0.38, 30 * b + belly), P(-0.04, 31 * b + belly * 0.5)])
        _printed(cr, body, self._fill(self.tunic), 18, K, kw, flat=flat)
        if flat:
            return
        _line(cr, [P(0.3, -26 * b), P(0.3, 30 * b + belly * 0.9)], 10, _shade(self.tunic, 0.6))  # belt
        _line(cr, [P(0.97, -14), P(0.84, 8), P(0.96, 15)], 4.5, col("ink"))                # collar
        nk = _capsule(P(1.0, 0), (N[0] + u[0] * 16, N[1] + u[1] * 16), 12, 11)
        _printed(cr, nk, col("cream"), 5, K, 3.2, dots=False)

    def _head(self, cr, t, J, p, face_over, K, kw, flat):
        hx, hy = J["head"]
        R = HEAD_R * (1.1 if self.leader == "churchill" else 1.0)
        turn = max(-1.0, min(1.0, p.get("turn", 0.0)))
        face = dict(brow="neutral", mouth="line", sweat=0.0, look=(0.0, 0.0))
        face.update(p.get("face") or {})
        face.update(face_over or {})
        cr.save()
        cr.translate(hx, hy)
        cr.rotate((p.get("lean", 0.0) + p.get("nod", 0.0) * 0.6) * 0.55)
        skin = self._fill(col("cream"))
        jaw = 0.98 if self.leader == "mussolini" else 0.82
        head = _poly_curve([(-0.98, 0.05), "c", (-1.05, -1.25), (0.85, -1.3), (0.88, -0.42), (0.93, -0.2),
                            (1.12, 0.12), (0.95, 0.24), (0.97, 0.46), (0.92, 0.58), (0.86, jaw),
                            (0.12, 0.98 if jaw > 0.9 else 0.94), "c", (-0.3, 0.86), (-0.55, 0.55), (-0.62, 0.42)], R)
        _printed(cr, head, skin, R * 0.55, K, kw, flat=flat)
        if flat:                                                    # a silhouette: a rim of light on the face
            _line(cr, [(0.88 * R, -0.42 * R), (0.95 * R, -0.18 * R), (1.22 * R, 0.14 * R)], 3.0, col("cream", 0.9))
            for path, c in _headgear_parts(self.nation or self.civilian or {"churchill": "bowler",
                                           "chamberlain": "homburg"}.get(self.leader, ""), R):
                _printed(cr, path, self.tone, 0, None, flat=True)
            cr.restore()
            return
        ink = col("ink")
        # hair
        hair = HAIR.get(self.leader)
        if self.leader == "hitler":                                   # side-swept: a fringe down over the brow
            hp = _poly_curve([(-0.98, 0.1), "c", (-1.08, -1.32), (0.8, -1.38), (0.86, -0.5), (0.72, -0.28),
                              (0.4, -0.62), (0.05, -0.55), (-0.45, -0.15)], R)
            _printed(cr, hp, col(hair), 0, K, 3.5)
        elif self.leader in ("stalin", "roosevelt", "hirohito"):       # swept back / short
            hl = -0.86 if self.leader == "stalin" else -0.78
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
        blink = _blink(t, self.seed)
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
        if self.leader in ("roosevelt", "hirohito"):                  # pince-nez / round glasses
            ex = eyes[0][0] * R
            cr.arc(ex, -0.14 * R, 0.3 * R if self.leader == "hirohito" else 0.24 * R, 0, 2 * math.pi)
            cr.set_source_rgba(*ink)
            cr.set_line_width(2.6)
            cr.stroke()
            _line(cr, [(ex + 0.27 * R, -0.16 * R), (0.92 * R, -0.12 * R)], 2.4, ink)
            if self.leader == "hirohito":
                _line(cr, [(ex - 0.3 * R, -0.16 * R), (-0.1 * R, -0.1 * R)], 2.4, ink)
        # moustache (under the nose)
        mo = {"hitler": ((0.84, 0.29), 0.2, 0.13), "stalin": ((0.68, 0.29), 0.48, 0.2),
              "chamberlain": ((0.72, 0.3), 0.32, 0.12), "hirohito": ((0.8, 0.3), 0.18, 0.08)}.get(self.leader)
        if mo:
            (mx, my), w, h = mo
            if self.leader == "stalin":
                pth = _poly_curve([(mx, my), "c", (mx + 0.1, my - 0.12), (mx + 0.36, my - 0.12), (mx + w, my + 0.04),
                                   "c", (mx + 0.36, my + 0.14), (mx + 0.12, my + 0.22), (mx - 0.05, my + 0.2)], R)
            else:
                pth = _poly([(mx * R, my * R), ((mx + w) * R, my * R), ((mx + w) * R, (my + h) * R),
                             (mx * R, (my + h) * R)])
            _printed(cr, pth, col(HAIR.get(self.leader, "#2b2724")), 0, None)
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
        if self.mouth_prop == "pipe":
            _line(cr, [(mx + 4, my + 1), (mx + 26, my + 9)], 4.4, col("#3b281c"))
            _printed(cr, _poly([(mx + 22, my + 2), (mx + 36, my + 2), (mx + 34, my + 22), (mx + 24, my + 22)]),
                     col("#5b3a26"), 3, ink, 2.6, dots=False)
        elif self.mouth_prop == "cigar":
            cr.save()
            cr.translate(mx + 4, my + 1)
            cr.rotate(0.15)
            _printed(cr, _poly([(0, -4.5), (34, -4.5), (34, 4.5), (0, 4.5)]), col("#7a4a2a"), 2, ink, 2.4,
                     dots=False)
            cr.arc(36, 0, 3.6, 0, 2 * math.pi)
            cr.set_source_rgba(*col("fire"))
            cr.fill()
            cr.restore()
            self._smoke(cr, t, mx + 46, my - 2)
        elif self.mouth_prop == "holder":
            _line(cr, [(mx + 4, my), (mx + 36, my - 20)], 3.0, ink)
            _line(cr, [(mx + 36, my - 20), (mx + 46, my - 26)], 5.0, col("white"))
            self._smoke(cr, t, mx + 48, my - 32)
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
        kind = self.nation or self.civilian or {"churchill": "bowler", "chamberlain": "homburg"}.get(self.leader)
        if kind:
            side_c = col(NATION_SIDE.get(self.nation, "axis")) if self.nation else None
            for path, c in _headgear_parts(kind, R):
                _printed(cr, path, col(c) if c else side_c, R * 0.6, ink, kw * 0.9)
        cr.restore()

    def _smoke(self, cr, t, x, y):
        for i in range(3):
            u = (t * 0.6 + i / 3.0) % 1.0
            cr.arc(x + 6 * math.sin(u * 5 + i), y - 34 * u, 4 + 7 * u, 0, 2 * math.pi)
            cr.set_source_rgba(*col("ink_soft", 0.3 * (1 - u)))
            cr.fill()

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
