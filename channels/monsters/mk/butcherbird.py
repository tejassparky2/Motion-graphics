"""The butcher bird's moves (Episode 1 v2, S23-S24; Episode 2's threat), and a shrike-dressed variant of the bird.

In the episode the butcher bird IS the tuftwing (mk/tuftwing.py, the small fluffy bird whose shadow is far too big).
land(), stare(), dive() and idle_perch() work on any rig with the tuftwing's handles, so they drive it directly:

    rig = tuftwing.build((x, y, 0))                    # its root (and its giant shadow) on the ground
    rig["root"].scale = (s, s, s)                      # optional
    land(rig, f, drop=(0.5, 1.6, 2.8), rest=(0, 0, perch_z / s))   # perch on top of something perch_z high
    stare(rig, f + 12, down=0.5)
    dive(rig, f0, f1, target=(dx, dy, dz))             # plunge at something (rig units, relative to the root)

build() below is the alternative look: a small, round, fluffy shrike of our own design. Shrikes
really do impale their food on thorns to store it (the "butcher bird"). It is the tuftwing's body (mk/tuftwing.py)
re-dressed: a pale blue-grey ball, a black "bandit" mask through big black eyes (amber crescent, two highlights), a
white throat and belly with a scalloped edge, a little hooked beak, dark wings with a white patch, a small crest and
a black-and-white tail.

Clean colour boundaries (HELPERS "Frame-by-frame targets"): the ball is one smooth shape and the mask and belly are
their own smooth patches lying on it, each edge one curve (no per-face sdf materials).

    rig = build(loc, scale=1.6)  ->  dict(root, lift, body, head, eyes, crest, wings, tail)   (same handles as the
                                     tuftwing; feet at z=0, facing -Y; at scale 1.6 it is ~2.4 units tall, a bit
                                     taller than the 2-unit puff-shrimp)
    land(rig, f, drop=(0, 0.6, 3.0))   flaps down from `drop` above its perch and touches down at frame f
    stare(rig, f, down=0.38)           lowers its head and narrows its eyes at whatever is below it
    idle_perch(rig, f0, f1)            small breaths, a tail flick and blinks while perched
Action (land) is on 2s and acting (stare, idle) on 3s, like the series (IM2); call anim.on_twos yourself per shot.
"""
import math
import random

import bpy
import numpy as np

from . import anim, look, sdf
from .tuftwing import BALL, CENTER, _empty, _line, _on_eye, _parent, _ribbon, _sculpt, _sphere

GREY, BELLY, MASK, WING, WHITE = "#b7c2d8", "#fbf5ea", "#33314a", "#3a3850", "#f6f3ee"
BEAK, FEET, INK, CRESCENT, BLUSH = "#5b5872", "#9a93a8", "#0f0d18", "#ffb04a", "#f2a3a0"


def _on_surface(a, e, lift=1.0):
    """The point on the ball at azimuth a (0 = straight ahead, -Y; + toward +X) and elevation e (radians)."""
    d = np.array((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    t = 1.0 / math.sqrt(sum((d[i] / BALL[i]) ** 2 for i in range(3)))
    return tuple(float(v) for v in np.asarray(CENTER) + d * t * lift)


def _patch(name, mat, az, lo, hi, n=120, m=20, lift=1.007):
    """A marking lying on the ball: at each azimuth a in [az0, az1] it covers elevations lo(a)..hi(a). Its edges are
    the smooth curves lo and hi, so the colour boundary is one clean line."""
    verts, faces = [], []
    for a in np.linspace(az[0], az[1], n):
        l, h = lo(a), hi(a)
        for t in np.linspace(0, 1, m):
            verts.append(_on_surface(a, l + (h - l) * t, lift))
    for i in range(n - 1):
        for j in range(m - 1):
            k = i * m + j
            faces.append((k, k + m, k + m + 1, k + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    me.update()
    c = np.array([p.center[:] for p in me.polygons]) - np.asarray(CENTER)
    nr = np.array([p.normal[:] for p in me.polygons])
    if np.mean(np.sum(c * nr, axis=1) > 0) < 0.5:              # face outward, like the ball
        me.flip_normals()
    return o


def _mask_half_width(a):
    """The bandit mask: a thin bridge over the beak, wide around the eyes, tapering away behind them."""
    w = 0.08 + 0.17 * math.exp(-((abs(a) - 0.42) / 0.36) ** 2)
    return w * min(1.0, max(0.0, (2.1 - abs(a)) / 0.9)) ** 0.7


def _mask_mid(a):
    return 0.2 + 0.07 * max(0.0, abs(a) - 0.5)                  # rises a little toward the back of the head


def _belly_top(a):
    """The white throat and belly: up to beak level in front, dropping low at the back, with a fluffy scalloped edge."""
    back = ((1 - math.cos(a)) / 2) ** 0.8
    return 0.02 - 1.05 * back + 0.035 * math.cos(9 * a) * (1 - back)


def build(loc=(0, 0, 0), name="shrike", scale=1.6):
    hx, T = look.hexc, look.toon
    C, E = sdf.C, sdf.E
    grey, belly, mask, wing_m, white = (T(f"{name}_{n}", hx(c)) for n, c in (
        ("grey", GREY), ("belly", BELLY), ("mask", MASK), ("wing", WING), ("white", WHITE)))
    beak_m, feet_m = T(f"{name}_beak", hx(BEAK), gloss=True), T(f"{name}_feet", hx(FEET))
    eye_m = T(f"{name}_eye", hx(INK), gloss=True)
    hi_m, cres_m, blush_m = (look.flat(f"{name}_{n}", c) for n, c in (
        ("hi", (1, 1, 1, 1)), ("crescent", hx(CRESCENT)), ("blush", hx(BLUSH))))

    root = _empty(f"{name}_root", (0, 0, 0))                    # built at the origin, moved and scaled at the end
    lift = _empty(f"{name}_lift", (0, 0, 0), root)
    body = _empty(f"{name}_body", (0, 0, 0), lift)
    head = _empty(f"{name}_head", CENTER, body)
    # the ball (a clean ellipsoid), then the mask and the belly lying on it
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, location=CENTER)
    ball = bpy.context.object
    ball.name = f"{name}_ball"
    ball.scale = BALL
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ball.data.materials.append(grey)
    for p in ball.data.polygons:
        p.use_smooth = True
    _line(ball, 0.022)
    _parent(ball, head)
    for o in (_patch(f"{name}_mask", mask, (-2.1, 2.1), lambda a: _mask_mid(a) - _mask_half_width(a),
                     lambda a: _mask_mid(a) + _mask_half_width(a)),
              _patch(f"{name}_belly", belly, (-math.pi, math.pi), lambda a: -math.pi / 2 + 0.001, _belly_top,
                     n=160, m=24, lift=1.004)):
        _parent(o, head)
    # crest: one grey tuft at the back of the crown
    crest = _empty(f"{name}_crest", (0, 0.05, 1.32), head)
    tuft = _sculpt(f"{name}_tuft", [
        (C((0, 0.0, 1.3), (0, 0.12, 1.5), 0.075, 0.045), grey.name, None),
        (C((0, 0.12, 1.5), (0, 0.3, 1.56), 0.045, 0.012), grey.name, None),
        (C((0.05, 0.06, 1.3), (0.13, 0.18, 1.44), 0.05, 0.012), grey.name, None),
    ], k=0.03, res=0.012, smooth_iter=8)
    _line(tuft, 0.014)
    _parent(tuft, crest)
    # eyes: big and black inside the mask, an amber crescent low in each, two highlights on the same side
    eyes = []
    for sx in (-1, 1):
        a, ec, er = sx * 0.4, (sx * 0.25, -0.515, 0.86), (0.13, 0.06, 0.17)
        piv = _empty(f"{name}_eyepiv{sx}", ec, head)
        for o in (_sphere(f"{name}_eye{sx}", ec, er, eye_m, 0.016, 32, (0, 0, a)),
                  _sphere(f"{name}_cres{sx}", _on_eye(ec, a, er, 0.0, -0.085), (0.085, 0.02, 0.045), cres_m, 0, 20,
                          (0, 0, a)),
                  _sphere(f"{name}_hi{sx}", _on_eye(ec, a, er, -0.035, 0.06), (0.048, 0.02, 0.058), hi_m, 0, 16,
                          (0, 0, a)),
                  _sphere(f"{name}_hi2{sx}", _on_eye(ec, a, er, 0.05, -0.02), (0.024, 0.014, 0.024), hi_m, 0, 12,
                          (0, 0, a))):
            _parent(o, piv)
        eyes.append(piv)
        b = _sphere(f"{name}_blush{sx}", _on_surface(sx * 0.82, -0.2, 1.01), (0.09, 0.03, 0.05), blush_m, 0, 16,
                    (0, 0, sx * 0.85))
        _parent(b, head)
    # a little hooked beak: the upper half curls down over the lower
    beak = _sculpt(f"{name}_beak", [
        (C((0, -0.55, 0.77), (0, -0.72, 0.77), 0.08, 0.055), beak_m.name, None),
        (C((0, -0.72, 0.77), (0, -0.8, 0.72), 0.055, 0.032), beak_m.name, None),
        (C((0, -0.8, 0.72), (0, -0.785, 0.65), 0.032, 0.01), beak_m.name, None),
        (C((0, -0.56, 0.71), (0, -0.69, 0.7), 0.055, 0.024), beak_m.name, None),
    ], k=0.02, res=0.008, smooth_iter=8)
    _line(beak, 0.012)
    _parent(beak, head)
    # stubby dark wings, each with a white patch
    wings = []
    for sx in (-1, 1):
        piv = _empty(f"{name}_wingpiv{sx}", (sx * 0.6, 0.0, 0.86), body)
        w = _sculpt(f"{name}_wing{sx}", [
            (E((sx * 0.65, 0.0, 0.76), (0.075, 0.17, 0.16)), wing_m.name, None),
            (E((sx * 0.67, 0.15, 0.6), (0.065, 0.15, 0.13)), wing_m.name, None),
            (E((sx * 0.67, 0.28, 0.46), (0.055, 0.13, 0.085)), wing_m.name, None),
        ], k=0.07, res=0.014, smooth_iter=12)
        _line(w, 0.016)
        _parent(w, piv)
        spot = _sphere(f"{name}_wingspot{sx}", (sx * 0.722, 0.08, 0.66), (0.012, 0.075, 0.05), white, 0, 20)
        _parent(spot, piv)
        wings.append(piv)
    feet = _sculpt(f"{name}_feet", [
        (E((sx * 0.15, -0.08, 0.05), (0.055, 0.085, 0.045)), feet_m.name, None) for sx in (-1, 1)
    ], keep_islands=True, k=0.0, res=0.014, smooth_iter=8)
    _line(feet, 0.012)
    _parent(feet, body)
    # tail: three dark feathers held up and back, like a shrike's
    tail = _empty(f"{name}_tail", (0, 0.5, 0.56), body)
    for nm, mat, ctrl, tw in (
            ("mid", wing_m, [(0, 0.44, 0.62), (0, 0.8, 0.86), (0, 1.15, 1.08), (0, 1.45, 1.28)], 0.2),
            ("l", wing_m, [(-0.05, 0.44, 0.6), (-0.18, 0.78, 0.8), (-0.33, 1.08, 0.98), (-0.45, 1.33, 1.12)], -0.2),
            ("r", wing_m, [(0.05, 0.44, 0.6), (0.18, 0.78, 0.8), (0.33, 1.08, 0.98), (0.45, 1.33, 1.12)], 0.2)):
        r = _ribbon(f"{name}_tail_{nm}", ctrl, mat, tw, tilt=1.2)
        _parent(r, tail)
    root.location = loc
    root.scale = (scale, scale, scale)
    return dict(root=root, lift=lift, body=body, head=head, eyes=eyes, crest=crest, wings=wings, tail=tail)


def objects(rig):
    """The animated handles, for anim.on_twos."""
    return [rig[k] for k in ("lift", "body", "head", "crest", "tail")] + rig["eyes"] + rig["wings"]


def land(rig, f, drop=(0.0, 0.6, 3.0), frames=18, rest=(0.0, 0.0, 0.0)):
    """Flap down from `drop` (rig units, above and behind the perch) onto `rest` (the perch, as the lift's location in
    rig units) and touch down at frame f: wings beating on 2s on the way down, a squash on touchdown, wings folding,
    a tail flick. Then it holds still."""
    lift, body, tail = rig["lift"], rig["body"], rig["tail"]
    f0 = f - frames
    for t in range(frames + 1):                               # ease out: fast at first, slowing to the perch
        k = 1 - (1 - t / frames) ** 2
        anim.key(lift, "location", f0 + t, tuple(r + d * (1 - k) for r, d in zip(rest, drop)), "LINEAR")
    for sx, w in zip((-1, 1), rig["wings"]):
        t, up = f0, True
        while t < f + 2:
            anim.key(w, "rotation_euler", t, (0, -sx * (1.45 if up else 0.55), 0))
            up = not up
            t += 2
        for dt, a in ((4, 1.5), (8, 0.7), (12, 0.0)):         # the last beat brakes, then the wings fold
            anim.key(w, "rotation_euler", f + dt, (0, -sx * a, 0))
    anim.squash(body, f0, 0.12)                                # stretched in flight
    anim.squash(body, f - 2, 0.1)
    anim.squash(body, f, -0.22, "LINEAR")                       # touchdown
    anim.squash(body, f + 4, 0.06)
    anim.squash(body, f + 8, 0.0)
    for dt, a in ((-frames, -0.25), (0, -0.2), (3, 0.45), (8, -0.1), (12, 0.0)):   # the shrike's tail flick
        anim.key(tail, "rotation_euler", f + dt, (a, 0, 0))
    anim.key(rig["head"], "rotation_euler", f0, (-0.15, 0, 0))   # head up in flight, level on the perch
    anim.key(rig["head"], "rotation_euler", f + 4, (0.05, 0, 0))
    anim.key(rig["crest"], "rotation_euler", f0, (-0.35, 0, 0))
    anim.key(rig["crest"], "rotation_euler", f + 3, (0.3, 0, 0))
    anim.key(rig["crest"], "rotation_euler", f + 9, (0.0, 0, 0))


def stare(rig, f, down=0.38, turn=0.0, hold=None):
    """Lower the head toward something below (a look straight down the camera from a perch), narrow the eyes and
    slant its eyes into a glare and raise the crest: the cute bird turning into a threat (SU5) without a new model."""
    head = rig["head"]
    anim.key(head, "rotation_euler", f, tuple(head.rotation_euler))
    anim.key(head, "rotation_euler", f + 6, (down, 0, turn))
    for sx, e in zip((-1, 1), rig["eyes"]):                    # narrowed and slanted in: a glare
        anim.key(e, "scale", f + 2, (1, 1, 1))
        anim.key(e, "rotation_euler", f + 2, (0, 0, 0))
        anim.key(e, "scale", f + 6, (1.05, 1, 0.72))
        anim.key(e, "rotation_euler", f + 6, (0, sx * 0.32, 0))
    anim.key(rig["crest"], "rotation_euler", f + 2, (0, 0, 0))
    anim.key(rig["crest"], "rotation_euler", f + 6, (-0.35, 0, 0))   # raised
    if hold:
        anim.key(head, "rotation_euler", f + hold, (down, 0, turn))


def dive(rig, f0, f1, target, start=None):
    """The dive pose and plunge: from `start` (the lift's location, rig units; default where it is) to `target` over
    f0..f1, accelerating. Body stretched, head pitched down at the prey, wings swept back half-open, tail up. Key the
    pose on 2s (action) with anim.on_twos(objects(rig), step=2)."""
    lift = rig["lift"]
    start = tuple(lift.location) if start is None else start
    n = f1 - f0
    for t in range(n + 1):                                    # ease in: slow off the perch, fast at the end
        k = (t / n) ** 2
        anim.key(lift, "location", f0 + t, tuple(a + (b - a) * k for a, b in zip(start, target)), "LINEAR")
    anim.squash(rig["body"], f0 - 4, -0.12)                   # a crouch before it goes
    anim.squash(rig["body"], f0, 0.25, "LINEAR")              # stretched like a dart
    anim.key(rig["head"], "rotation_euler", f0, (0.55, 0, 0))
    for sx, w in zip((-1, 1), rig["wings"]):
        anim.key(w, "rotation_euler", f0 - 4, (0, -sx * 1.3, 0))   # spread, then swept back for the plunge
        anim.key(w, "rotation_euler", f0 + 2, (0, -sx * 0.5, 0))
    anim.key(rig["tail"], "rotation_euler", f0, (0.45, 0, 0))
    anim.key(rig["crest"], "rotation_euler", f0, (-0.5, 0, 0))   # flattened by the wind


def idle_perch(rig, f0, f1, period=36, seed=3):
    """While perched: slow breaths, one tail flick, blinks. Acting on 3s."""
    rnd = random.Random(seed)
    f = f0
    while f <= f1:
        anim.squash(rig["body"], f, 0.03)
        anim.squash(rig["body"], f + period // 2, -0.02)
        f += period
    ft = f0 + rnd.randint(10, 20)
    for dt, a in ((0, 0.0), (3, 0.4), (9, 0.0)):
        anim.key(rig["tail"], "rotation_euler", ft + dt, (a, 0, 0))
    f = f0 + rnd.randint(14, 30)
    while f < f1 - 4:
        anim.blink(rig, f - (f + 1) % 3)
        f += rnd.randint(40, 70)
