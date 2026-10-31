"""WW2 channel kit: the stick-figure rig (channels/ww2/STYLE.md, "Stick figures"). Pure pycairo.

    from channels.ww2.kit.stick import Figure, crowd, POSES

    f = Figure(nation="germany", x=600, y=900, scale=1.0, facing=1)          # y = the ground line under the figure
    f.draw(cr, t, track=[(0.0, "stand"), (1.0, "walk"), (3.0, "salute")],     # keyframes: (time, pose name or dict)
           move=[(1.0, 600), (3.0, 900)])                                     # optional x path (t, x) or (t, x, y)

Figure(nation=None, leader=None, civilian=None, x, y, scale=1.0, facing=1, prop=None, color=None, seed=0)
    nation:   "germany" "britain" "usa" "soviet" "france" "japan" "italy" (headgear in the side colour, STYLE.md)
    civilian: "flatcap" "hat" "scarf" (neutral colours)
    leader:   "hitler" "stalin" "churchill" "roosevelt" "mussolini" "hirohito" "chamberlain" (ONE trademark each;
              stalin gets his pipe, churchill his cigar, roosevelt his cigarette holder, chamberlain his umbrella)
    prop:     "rifle" "paper" "pen" "umbrella" (held in the hand), or None; leaders bring their own
    facing:   1 = right, -1 = left. A pose may also carry "turn" (-1..1): the head's 3/4 turn toward the viewer.
Figure.draw(cr, t, track, move=None, face=None)
    track: [(t, pose)] sorted by time. A pose is a POSES name or a dict of joint angles (see REST) and may carry a
           "face" dict. Between keys the pose blends with an eased curve over BLEND seconds before each key;
           looping actions (walk, run, march, wave, cheer, crawl, shiver, fire, shake, idle) keep animating.
    face:  overrides for the whole track: {"brow": "neutral|angry|worried|sad", "mouth": "line|smile|o|grit|frown",
           "sweat": 0..1, "look": (dx, dy)}. Eyes blink by themselves every 2-5 s.
crowd(cr, t, n, x0, x1, y0, y1, scale=0.5, nation=None, pose="cheer", seed=1, ...)
    N small figures with varied timing, colours and headgear; cheap enough for 40+ on screen.

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

from channels.ww2.kit.core import PAL, SIDE, cairo, col, lerp, smooth

# ---------------------------------------------------------------- proportions (scale 1: a 300 px figure)
HEAD_R = 32.0
NECK = 10.0
TORSO = 96.0
UPPER, FORE = 52.0, 50.0
THIGH, SHIN = 64.0, 62.0
LIMB_W, HEAD_W = 7.0, 6.0
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
    sh = (neck[0] - 8 * math.sin(lean), neck[1] + 8 * math.cos(lean))
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


# ---------------------------------------------------------------- drawing helpers
def _line(cr, pts, w, c):
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.move_to(*pts[0])
    for q in pts[1:]:
        cr.line_to(*q)
    cr.set_source_rgba(*c)
    cr.stroke()


def _fill_stroke(cr, fill, stroke=None, w=4.0):
    if fill is not None:
        cr.set_source_rgba(*fill)
        cr.fill_preserve() if stroke else cr.fill()
    if stroke:
        cr.set_source_rgba(*stroke)
        cr.set_line_width(w)
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


# ---------------------------------------------------------------- headgear (drawn in head space: centre (0,0), r=R)
def _helmet(cr, kind, c, R, ink):
    if kind == "germany":              # flared helmet: deep dome, the skirt flaring at the sides and back
        cr.move_to(-R * 1.08, -R * 0.02)
        cr.curve_to(-R * 1.1, -R * 1.25, R * 1.1, -R * 1.25, R * 1.04, -R * 0.12)
        cr.line_to(R * 1.06, R * 0.02)
        cr.line_to(R * 0.7, -R * 0.06)
        cr.line_to(-R * 0.55, -R * 0.06)
        cr.curve_to(-R * 0.9, -R * 0.02, -R * 1.18, R * 0.25, -R * 1.3, R * 0.32)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
    elif kind == "britain":            # flat dish: a wide flat brim and a shallow crown
        cr.save()
        cr.translate(0, -R * 0.55)
        cr.scale(1.0, 0.22)
        cr.arc(0, 0, R * 1.55, 0, 2 * math.pi)
        cr.restore()
        _fill_stroke(cr, c, ink, 4.5)
        cr.move_to(-R * 0.82, -R * 0.62)
        cr.curve_to(-R * 0.75, -R * 1.25, R * 0.75, -R * 1.25, R * 0.82, -R * 0.62)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
    elif kind == "usa":                # round M1: a round dome with a little rim
        cr.move_to(-R * 1.12, -R * 0.12)
        cr.curve_to(-R * 1.15, -R * 1.42, R * 1.15, -R * 1.42, R * 1.12, -R * 0.12)
        cr.line_to(R * 1.25, -R * 0.02)
        cr.line_to(-R * 1.25, -R * 0.02)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
    elif kind == "soviet":             # rounded helmet, a slight flare all round
        cr.move_to(-R * 1.1, -R * 0.08)
        cr.curve_to(-R * 1.12, -R * 1.35, R * 1.12, -R * 1.35, R * 1.1, -R * 0.08)
        cr.curve_to(R * 1.2, R * 0.0, R * 1.2, R * 0.05, R * 1.12, R * 0.08)
        cr.line_to(-R * 1.12, R * 0.08)
        cr.curve_to(-R * 1.2, R * 0.05, -R * 1.2, R * 0.0, -R * 1.1, -R * 0.08)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
        cr.arc(R * 0.0, -R * 0.62, R * 0.13, 0, 2 * math.pi)        # a plain red star stand-in: a red dot
        cr.set_source_rgba(*col("soviet"))
        cr.fill()
    elif kind == "france":             # crested: a dome, a brim, a crest along the top
        cr.move_to(-R * 1.3, -R * 0.1)
        cr.line_to(R * 1.3, -R * 0.1)
        cr.curve_to(R * 1.05, -R * 0.3, R * 1.0, -R * 0.35, R * 0.95, -R * 0.35)
        cr.curve_to(R * 0.95, -R * 1.25, -R * 0.95, -R * 1.25, -R * 0.95, -R * 0.35)
        cr.curve_to(-R * 1.0, -R * 0.35, -R * 1.05, -R * 0.3, -R * 1.3, -R * 0.1)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
        cr.move_to(-R * 0.55, -R * 1.02)
        cr.curve_to(-R * 0.3, -R * 1.42, R * 0.3, -R * 1.42, R * 0.55, -R * 1.02)
        cr.line_to(R * 0.4, -R * 0.95)
        cr.curve_to(R * 0.2, -R * 1.18, -R * 0.2, -R * 1.18, -R * 0.4, -R * 0.95)
        cr.close_path()
        _fill_stroke(cr, c, ink, 3.5)
    elif kind == "japan":              # peaked cap with neck flaps hanging at the back
        cr.move_to(-R * 1.0, -R * 0.35)
        cr.line_to(-R * 1.05, R * 0.55)
        cr.line_to(-R * 0.55, R * 0.45)
        cr.line_to(-R * 0.6, -R * 0.3)
        cr.close_path()
        _fill_stroke(cr, c, ink, 3.5)
        cr.move_to(-R * 0.95, -R * 0.35)
        cr.curve_to(-R * 0.95, -R * 1.25, R * 0.95, -R * 1.25, R * 0.95, -R * 0.35)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)
        cr.move_to(R * 0.4, -R * 0.38)
        cr.curve_to(R * 0.9, -R * 0.45, R * 1.3, -R * 0.35, R * 1.45, -R * 0.2)
        cr.line_to(R * 0.45, -R * 0.28)
        cr.close_path()
        _fill_stroke(cr, col("ink"), ink, 2.5)
        cr.arc(R * 0.55, -R * 0.68, R * 0.1, 0, 2 * math.pi)       # a plain small star stand-in
        cr.set_source_rgba(*col("gold"))
        cr.fill()
    elif kind == "italy":              # helmet with a feather plume off the side
        for i in range(7):
            a = -2.4 - i * 0.09
            cr.move_to(-R * 0.75, -R * 0.55)
            cr.curve_to(-R * 1.2, -R * 0.75 - i * 1.5, -R * 1.6 - i * 2.0, -R * 0.25 + i * 2.5,
                        -R * 1.6 + R * 1.15 * math.cos(a) * 0.4 - i * 2.4, -R * 0.1 + i * 3.2)
            cr.set_line_width(3.2)
            cr.set_source_rgba(*col("#2c3a2a"))
            cr.stroke()
        cr.move_to(-R * 1.1, -R * 0.1)
        cr.curve_to(-R * 1.12, -R * 1.35, R * 1.12, -R * 1.35, R * 1.1, -R * 0.1)
        cr.line_to(R * 1.2, R * 0.02)
        cr.line_to(-R * 1.2, R * 0.02)
        cr.close_path()
        _fill_stroke(cr, c, ink, 4.5)


def _civ_hat(cr, kind, R, ink):
    if kind == "flatcap":
        cr.move_to(-R * 0.95, -R * 0.35)
        cr.curve_to(-R * 1.0, -R * 1.2, R * 0.95, -R * 1.15, R * 1.0, -R * 0.4)
        cr.curve_to(R * 1.4, -R * 0.35, R * 1.55, -R * 0.25, R * 1.5, -R * 0.15)
        cr.line_to(-R * 0.95, -R * 0.25)
        cr.close_path()
        _fill_stroke(cr, col("#8a7a62"), ink, 4.0)
    elif kind in ("hat", "homburg"):
        crown = col("#6a5f55") if kind == "hat" else col("#3b3733")
        cr.save()
        cr.translate(0, -R * 0.62)
        cr.scale(1.0, 0.24)
        cr.arc(0, 0, R * 1.45, 0, 2 * math.pi)
        cr.restore()
        _fill_stroke(cr, crown, ink, 4.0)
        cr.move_to(-R * 0.8, -R * 0.6)
        cr.line_to(-R * 0.8, -R * 1.35)
        cr.curve_to(-R * 0.3, -R * 1.5 if kind == "homburg" else -R * 1.2, R * 0.3, -R * 1.5 if kind == "homburg"
                    else -R * 1.2, R * 0.8, -R * 1.35)
        cr.line_to(R * 0.8, -R * 0.6)
        cr.close_path()
        _fill_stroke(cr, crown, ink, 4.0)
        cr.rectangle(-R * 0.8, -R * 0.82, R * 1.6, R * 0.18)
        cr.set_source_rgba(*col("ink", 0.85))
        cr.fill()
    elif kind == "bowler":
        cr.save()
        cr.translate(0, -R * 0.6)
        cr.scale(1.0, 0.2)
        cr.arc(0, 0, R * 1.3, 0, 2 * math.pi)
        cr.restore()
        _fill_stroke(cr, col("#2b2826"), ink, 4.0)
        cr.move_to(-R * 0.82, -R * 0.62)
        cr.curve_to(-R * 0.85, -R * 1.65, R * 0.85, -R * 1.65, R * 0.82, -R * 0.62)
        cr.close_path()
        _fill_stroke(cr, col("#2b2826"), ink, 4.0)
    elif kind == "scarf":
        cr.move_to(-R * 1.08, R * 0.2)
        cr.curve_to(-R * 1.25, -R * 1.35, R * 1.25, -R * 1.35, R * 1.08, R * 0.2)
        cr.line_to(R * 0.85, R * 0.1)
        cr.curve_to(R * 0.95, -R * 0.95, -R * 0.95, -R * 0.95, -R * 0.85, R * 0.1)
        cr.close_path()
        _fill_stroke(cr, col("#a5574a"), ink, 3.5)
        cr.move_to(-R * 0.2, R * 0.95)
        cr.line_to(-R * 0.6, R * 1.35)
        cr.line_to(-R * 0.1, R * 1.25)
        cr.close_path()
        _fill_stroke(cr, col("#a5574a"), ink, 3.0)


# ---------------------------------------------------------------- the figure
class Figure:
    def __init__(self, nation=None, leader=None, civilian=None, x=0.0, y=0.0, scale=1.0, facing=1, prop=None,
                 color=None, seed=0, name=None):
        self.nation, self.leader, self.civilian = nation, leader, civilian
        self.x, self.y, self.scale, self.facing = x, y, scale, facing
        self.seed = seed
        self.ink = col(color) if color else col("ink")
        self.prop = prop
        if leader and prop is None:
            self.prop = {"chamberlain": "umbrella"}.get(leader)
        self.mouth_prop = {"stalin": "pipe", "churchill": "cigar", "roosevelt": "holder"}.get(leader)
        self.name = name

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
            if t <= move[0][0]:
                m = move[0]
            elif t >= move[-1][0]:
                m = move[-1]
            else:
                for a, b in zip(move, move[1:]):
                    if a[0] <= t <= b[0]:
                        u = (t - a[0]) / max(1e-6, b[0] - a[0])
                        m = (t, lerp(a[1], b[1], u), lerp(a[2], b[2], u) if len(a) > 2 and len(b) > 2 else None)
                        break
            x = m[1]
            if len(m) > 2 and m[2] is not None:
                y = m[2]
        return x, y

    def draw_pose(self, cr, t, p, x, y, face=None):
        J = skeleton(p)
        off = _ground_offset(J, p) + p.get("bob", 0.0) + p.get("drop", 0.0)
        s, f = self.scale, self.facing
        ink = self.ink
        cr.save()
        cr.translate(x, y)
        cr.scale(s * f, s)
        cr.translate(0, off)
        far = (ink[0], ink[1], ink[2], ink[3] * 0.9)
        # far limbs first, a hair thinner
        _line(cr, [J["hip"], J["kn_f"], J["ft_f"]], LIMB_W * 0.92, far)
        self._foot(cr, J["kn_f"], J["ft_f"], far)
        _line(cr, [J["sh"], J["el_f"], J["hand_f"]], LIMB_W * 0.92, far)
        self._hand(cr, J["el_f"], J["hand_f"], p.get("hand_f", "open"), far)
        if self.prop == "rifle":
            self._rifle(cr, J, p, t)
        # torso, near leg
        _line(cr, [J["hip"], J["neck"]], LIMB_W, ink)
        _line(cr, [J["hip"], J["kn_n"], J["ft_n"]], LIMB_W, ink)
        self._foot(cr, J["kn_n"], J["ft_n"], ink)
        self._collar(cr, J)
        self._head(cr, t, J, p, face)
        _line(cr, [J["sh"], J["el_n"], J["hand_n"]], LIMB_W, ink)
        self._hand(cr, J["el_n"], J["hand_n"], p.get("hand_n", "open"), ink)
        if self.prop in ("paper", "pen", "umbrella"):
            self._held(cr, J, p, t)
        cr.restore()

    def _foot(self, cr, kn, ft, c):
        _line(cr, [ft, (ft[0] + 11, ft[1] + 1)], LIMB_W * 0.95, c)

    def _hand(self, cr, el, hd, kind, c):
        dx, dy = hd[0] - el[0], hd[1] - el[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        if kind == "fist":
            cr.arc(hd[0], hd[1], 6.5, 0, 2 * math.pi)
            cr.set_source_rgba(*c)
            cr.fill()
        elif kind == "crossed":                                       # two fingers crossed
            bx, by = hd[0] + ux * 3, hd[1] + uy * 3
            px, py = -uy, ux
            _line(cr, [(bx - px * 3, by - py * 3), (bx + ux * 13 + px * 4, by + uy * 13 + py * 4)], 3.4, c)
            _line(cr, [(bx + px * 3, by + py * 3), (bx + ux * 13 - px * 4, by + uy * 13 - py * 4)], 3.4, c)
            cr.arc(hd[0], hd[1], 5.0, 0, 2 * math.pi)
            cr.set_source_rgba(*c)
            cr.fill()
        elif kind == "splay":
            for a in (-0.7, -0.25, 0.2, 0.65):
                ca, sa = math.cos(a), math.sin(a)
                vx, vy = ux * ca - uy * sa, ux * sa + uy * ca
                _line(cr, [hd, (hd[0] + vx * 11, hd[1] + vy * 11)], 3.0, c)
        else:
            cr.arc(hd[0], hd[1], 5.0, 0, 2 * math.pi)
            cr.set_source_rgba(*c)
            cr.fill()

    def _collar(self, cr, J):
        """A small nation-coloured neckerchief at the collar (the side colour, never a symbol)."""
        side = NATION_SIDE.get(self.nation) or {"hitler": "axis", "stalin": "soviet", "churchill": "allies",
                                                "roosevelt": "allies", "mussolini": "axis_it", "hirohito": "axis_jp",
                                                "chamberlain": "allies"}.get(self.leader)
        if not side:
            return
        nx, ny = J["neck"]
        cr.move_to(nx - 10, ny + 1)
        cr.line_to(nx + 10, ny + 1)
        cr.line_to(nx + 1, ny + 16)
        cr.close_path()
        _fill_stroke(cr, col(side), col("ink"), 2.5)

    def _head(self, cr, t, J, p, face_over):
        hx, hy = J["head"]
        R = HEAD_R * (1.1 if self.leader == "churchill" else 1.0)
        turn = max(-1.0, min(1.0, p.get("turn", 0.0)))
        nod = p.get("nod", 0.0)
        face = dict(brow="neutral", mouth="line", sweat=0.0, look=(0.0, 0.0))
        face.update(p.get("face") or {})
        face.update(face_over or {})
        cr.save()
        cr.translate(hx, hy)
        cr.rotate((p.get("lean", 0.0) + nod * 0.6) * 0.5)
        ink = col("ink")
        # head shape
        if self.leader == "mussolini":                                 # bald, a square jaw
            cr.move_to(-R, -R * 0.1)
            cr.curve_to(-R, -R * 1.35, R, -R * 1.35, R, -R * 0.1)
            cr.line_to(R * 0.95, R * 0.7)
            cr.curve_to(R * 0.9, R * 1.05, -R * 0.9, R * 1.05, -R * 0.95, R * 0.7)
            cr.close_path()
        else:
            cr.arc(0, 0, R, 0, 2 * math.pi)
        _fill_stroke(cr, col("paper"), ink, HEAD_W)
        # hair (under any hat)
        if self.leader == "hitler":                                    # side-swept hair: a fringe down over one brow
            cr.move_to(-R * 0.98, -R * 0.2)
            cr.curve_to(-R * 1.05, -R * 1.2, R * 0.95, -R * 1.25, R * 0.98, -R * 0.35)
            cr.curve_to(R * 0.8, -R * 0.55, R * 0.5, -R * 0.62, R * 0.2, -R * 0.6)
            cr.curve_to(-R * 0.1, -R * 0.45, -R * 0.35, -R * 0.2, -R * 0.55, R * 0.02)
            cr.curve_to(-R * 0.7, -R * 0.1, -R * 0.85, -R * 0.15, -R * 0.98, -R * 0.2)
            cr.close_path()
            _fill_stroke(cr, col("#2a2522"), None)
        elif self.leader == "stalin":                                  # swept-back hair
            cr.move_to(-R * 0.98, -R * 0.05)
            cr.curve_to(-R * 1.08, -R * 1.25, R * 0.8, -R * 1.3, R * 0.85, -R * 0.62)
            cr.curve_to(R * 0.2, -R * 0.88, -R * 0.4, -R * 0.75, -R * 0.98, -R * 0.05)
            cr.close_path()
            _fill_stroke(cr, col("#33302c"), None)
        # face (shifted toward the facing side by the 3/4 turn)
        fx = R * 0.28 * turn
        lx, ly = face["look"]
        blink = _blink(t, self.seed)
        ex = [fx - R * 0.3, fx + R * 0.3]
        if turn > 0.3:
            ex = [fx - R * 0.22, fx + R * 0.36]
        for i, e in enumerate(ex):
            ey = -R * 0.08 + ly
            if blink:
                _line(cr, [(e - 4 + lx, ey), (e + 4 + lx, ey)], 3.0, ink)
            else:
                cr.arc(e + lx, ey, 4.6, 0, 2 * math.pi)
                cr.set_source_rgba(*ink)
                cr.fill()
            b = face["brow"]
            side = -1 if i == 0 else 1
            by = ey - R * 0.3
            if b == "angry":
                pts = [(e - 8 * 1, by - 5 * -side), (e + 8, by - 5 * side)]
                pts = [(e - 8, by - 5 if side > 0 else by + 4), (e + 8, by + 4 if side > 0 else by - 5)]
            elif b in ("worried", "sad"):
                k = 6 if b == "worried" else 4
                pts = [(e - 8, by + k if side > 0 else by - k), (e + 8, by - k if side > 0 else by + k)]
            else:
                pts = [(e - 8, by), (e + 8, by)]
            _line(cr, pts, 3.4, ink)
        if self.leader in ("roosevelt", "hirohito"):                   # glasses: pince-nez or round
            for e in ex:
                cr.arc(e, -R * 0.08, 8.5 if self.leader == "hirohito" else 7.5, 0, 2 * math.pi)
                cr.set_line_width(2.4)
                cr.set_source_rgba(*ink)
                cr.stroke()
            _line(cr, [(ex[0] + 8, -R * 0.1), (ex[1] - 8, -R * 0.1)], 2.2, ink)
            if self.leader == "hirohito":
                _line(cr, [(ex[0] - 8, -R * 0.1), (-R * 0.95, -R * 0.15)], 2.2, ink)
        # moustache
        my = R * 0.3
        if self.leader == "hitler":                                    # toothbrush
            cr.rectangle(fx - 6, my - 6, 12, 8)
            cr.set_source_rgba(*col("#2a2522"))
            cr.fill()
        elif self.leader == "stalin":                                  # thick
            cr.move_to(fx - 17, my + 2)
            cr.curve_to(fx - 12, my - 10, fx + 12, my - 10, fx + 17, my + 2)
            cr.curve_to(fx + 8, my - 2, fx - 8, my - 2, fx - 17, my + 2)
            cr.close_path()
            _fill_stroke(cr, col("#33302c"), None)
        elif self.leader in ("chamberlain", "hirohito"):
            w = 13 if self.leader == "chamberlain" else 9
            cr.move_to(fx - w, my + 1)
            cr.curve_to(fx - w * 0.6, my - 6, fx + w * 0.6, my - 6, fx + w, my + 1)
            cr.curve_to(fx + w * 0.4, my - 1, fx - w * 0.4, my - 1, fx - w, my + 1)
            cr.close_path()
            _fill_stroke(cr, col("#4a443d"), None)
        # mouth
        mx, mY = fx, R * 0.48
        m = face["mouth"]
        if m == "smile":
            cr.arc(mx, mY - 9, 10, 0.25 * math.pi, 0.75 * math.pi)
            cr.set_line_width(3.4)
            cr.set_source_rgba(*ink)
            cr.stroke()
        elif m == "frown":
            cr.arc(mx, mY + 9, 9, 1.25 * math.pi, 1.75 * math.pi)
            cr.set_line_width(3.4)
            cr.set_source_rgba(*ink)
            cr.stroke()
        elif m == "o":
            cr.arc(mx, mY, 5.5, 0, 2 * math.pi)
            _fill_stroke(cr, col("#5a2a26"), ink, 2.6)
        elif m == "grit":
            cr.rectangle(mx - 10, mY - 4, 20, 9)
            _fill_stroke(cr, col("white"), ink, 2.6)
            _line(cr, [(mx - 10, mY + 0.5), (mx + 10, mY + 0.5)], 1.6, ink)
        else:
            _line(cr, [(mx - 8, mY), (mx + 8, mY)], 3.2, ink)
        # mouth props
        if self.mouth_prop == "pipe":
            _line(cr, [(mx + 6, mY + 1), (mx + 22, mY + 6)], 3.6, col("#4a3326"))
            cr.move_to(mx + 20, mY + 2)
            cr.line_to(mx + 31, mY + 2)
            cr.line_to(mx + 29, mY + 16)
            cr.line_to(mx + 22, mY + 16)
            cr.close_path()
            _fill_stroke(cr, col("#5b3a26"), ink, 2.2)
        elif self.mouth_prop == "cigar":
            cr.save()
            cr.translate(mx + 6, mY + 2)
            cr.rotate(0.18)
            cr.rectangle(0, -3.5, 30, 7)
            _fill_stroke(cr, col("#7a4a2a"), ink, 2.0)
            cr.arc(31, 0, 3.0, 0, 2 * math.pi)
            cr.set_source_rgba(*col("fire"))
            cr.fill()
            cr.restore()
            self._smoke(cr, t, mx + 38, mY - 2)
        elif self.mouth_prop == "holder":
            _line(cr, [(mx + 6, mY + 1), (mx + 34, mY - 16)], 2.6, ink)
            _line(cr, [(mx + 34, mY - 16), (mx + 42, mY - 21)], 4.0, col("white"))
            self._smoke(cr, t, mx + 44, mY - 26)
        # sweat
        if face.get("sweat", 0) > 0:
            k = face["sweat"]
            sx, sy = -R * 0.95 if turn > 0 else R * 0.95, -R * 0.35 + 6 * math.sin(t * 3)
            cr.move_to(sx, sy - 12 * k)
            cr.curve_to(sx + 6 * k, sy - 2 * k, sx + 6 * k, sy + 6 * k, sx, sy + 6 * k)
            cr.curve_to(sx - 6 * k, sy + 6 * k, sx - 6 * k, sy - 2 * k, sx, sy - 12 * k)
            _fill_stroke(cr, col("#9fd3ee"), ink, 2.2)
        # headgear
        if self.nation:
            _helmet(cr, self.nation, col(NATION_SIDE.get(self.nation, "axis")), R, ink)
        elif self.civilian:
            _civ_hat(cr, self.civilian, R, ink)
        elif self.leader == "churchill":
            _civ_hat(cr, "bowler", R, ink)
        elif self.leader == "chamberlain":
            _civ_hat(cr, "homburg", R, ink)
        cr.restore()

    def _smoke(self, cr, t, x, y):
        for i in range(3):
            u = (t * 0.6 + i / 3.0) % 1.0
            cr.arc(x + 6 * math.sin(u * 5 + i), y - 30 * u, 3 + 6 * u, 0, 2 * math.pi)
            cr.set_source_rgba(*col("ink_soft", 0.35 * (1 - u)))
            cr.fill()

    def _rifle(self, cr, J, p, t):
        """The rifle: aimed through both hands, or carried slung up from the near hand."""
        ink = col("ink")
        wood = col("#6b4a2e")
        if p.get("aim", 0) > 0.5:                                      # stock at the shoulder, level, forward
            a = (J["sh"][0] + 6, J["sh"][1] + 10)
            front = J["hand_n"] if J["hand_n"][0] > J["hand_f"][0] else J["hand_f"]
            dx, dy = front[0] - a[0], (front[1] - a[1]) * 0.35
        else:
            a = J["hand_n"]
            dx, dy = 0.35, -1.0
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        back = 12 if p.get("aim", 0) > 0.5 else 40
        s = (a[0] - ux * back, a[1] - uy * back)
        e = (a[0] + ux * (140 - back), a[1] + uy * (140 - back))
        mid = (a[0] + ux * (80 - back), a[1] + uy * (80 - back))
        _line(cr, [s, mid], 9.0, wood)
        _line(cr, [(mid[0] - ux * 10, mid[1] - uy * 10), e], 4.0, ink)
        if p.get("flash", 0) > 0.5:                                    # muzzle flash only
            cr.save()
            cr.translate(e[0] + ux * 14, e[1] + uy * 14)
            cr.rotate(math.atan2(uy, ux))
            cr.move_to(-6, 0)
            for i in range(10):
                a_ = i / 10 * 2 * math.pi
                r = 20 if i % 2 == 0 else 8
                cr.line_to(r * math.cos(a_) * 1.3, r * math.sin(a_))
            cr.close_path()
            _fill_stroke(cr, col("fire"), col("alert"), 2.5)
            cr.restore()

    def _held(self, cr, J, p, t):
        hx, hy = J["hand_n"]
        ink = col("ink")
        if self.prop == "paper":
            cr.save()
            up = p.get("prop_up", 0.0)
            cr.translate(hx + 4, hy - 18 * up)
            cr.rotate(-0.12 + 0.05 * math.sin(t * 5) * up)
            cr.rectangle(-14, -22, 30, 40)
            _fill_stroke(cr, col("white"), ink, 2.6)
            for i in range(4):
                _line(cr, [(-9, -14 + i * 8), (10, -14 + i * 8)], 1.6, col("ink_soft"))
            cr.restore()
        elif self.prop == "pen":
            _line(cr, [(hx - 2, hy + 4), (hx + 10, hy - 16)], 3.2, ink)
        elif self.prop == "umbrella":                                  # furled, held like a walking stick
            top, bot = (hx, hy - 6), (hx + 8, hy + 112)
            _line(cr, [top, bot], 3.0, ink)
            cr.move_to(hx + 2, hy + 8)
            cr.line_to(hx + 15, hy + 70)
            cr.line_to(hx + 4, hy + 74)
            cr.close_path()
            _fill_stroke(cr, col("#2b2826"), ink, 2.0)
            cr.arc(hx - 6, hy - 6, 7, math.pi, 2 * math.pi)
            cr.set_line_width(3.0)
            cr.set_source_rgba(*ink)
            cr.stroke()


# ---------------------------------------------------------------- crowds
_CIV = ("flatcap", "hat", "scarf", None)
_TINT = ("#3b3733", "#4a4038", "#2f3640", "#3d3a44", "#463c37")


def crowd(cr, t, n, x0, x1, y0, y1, scale=0.5, nation=None, pose="cheer", seed=1, facing=None, civilians=None,
          poses=None):
    """N small figures spread over a box (back rows higher and a little smaller), each with its own timing offset,
    ink tint and headgear: a nation's soldiers, or civilians when nation is None. `poses`: a list to pick from
    per figure (default: just `pose`). Drawn back to front."""
    r = random.Random(seed)
    people = []
    for i in range(n):
        u = r.random()
        y = lerp(y0, y1, u)
        x = r.uniform(x0, x1)
        s = scale * (0.82 + 0.18 * u) * r.uniform(0.92, 1.06)
        kind = nation or (civilians[r.randrange(len(civilians))] if civilians else None)
        f = Figure(nation=kind if kind in NATION_SIDE else None,
                   civilian=None if kind in NATION_SIDE else (kind if kind else _CIV[r.randrange(len(_CIV))]),
                   x=x, y=y, scale=s, facing=facing or r.choice((1, -1)), color=_TINT[r.randrange(len(_TINT))],
                   seed=seed * 1000 + i)
        people.append((y, f, (poses or [pose])[r.randrange(len(poses or [pose]))], r.uniform(0, 3)))
    for y, f, p, off in sorted(people, key=lambda q: q[0]):
        f.draw(cr, t + off, [(0.0, p)])
