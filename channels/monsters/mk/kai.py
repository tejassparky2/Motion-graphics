"""Kai, the hero of "Cute Things Kill Here" (design: HELPERS.md v3.2). A 19-year-old wildlife-biology student, anime-teen
proportions (about 6 heads, 1.75 m), messy dark-brown hair with one tall front cowlick, big amber anime eyes, an open
sage zip-up hoodie over a white tee, navy cargo trousers, orange-yellow sneakers, a black watch on the RIGHT wrist (the
left stays bare for the bond ring), and an open white lab coat for the lab.

All procedural (bpy + numpy, no downloaded assets), deterministic:
  - each colour region is its own smooth SDF mesh (sdf.build), so colour boundaries are single clean curves;
  - the body meshes are skinned to one armature with procedural weights from capsule distances to the bones;
  - head, hair, shoes and watch are rigid, parented to their bones;
  - the face is flat anime: eyes, lashes, brows, nose and the swappable mouths are 2D shapes projected onto the face as
    zero-thickness decals, so they read as drawn lines and stay flat in profile.

    rig = build(loc=(0, 0, 0), name="kai", outfit="world" | "lab")
    rig["root"]   empty: moves / turns the whole character (feet at z=0, facing -Y)
    rig["arm"]    the armature; pose bones: hips, spine, chest, neck, head, shoulder.L/R, upper_arm.L/R, forearm.L/R,
                  hand.L/R, thigh.L/R, shin.L/R, foot.L/R, and per hand thumb1/2, index1/2, middle1/2, ring1/2, pinky1/2
                  (".R" = the character's right, at -X)
    rig["eyes"]   eye pivots (blink: scale z; anim.blink(rig, f) works)
    rig["irises"] iris pivots (scale down for shock eyes)
    rig["brows"]  brow pivots (move / turn for expressions)
    rig["mouths"] {"neutral", "o", "smile", "teeth"}: mouth shapes, switched with set_mouth()
    rig["head_parts"] head, hair and face objects (hide them for POV shots: pov_camera() does)

Posing: every pose function resets to the rest pose, poses the bones and keys them at a frame:
    stand, sit_at_desk, tap_glass, reach_pov, thrown_back, shock, and expression(rig, name, f) for the face.
Lower-level: rot(rig, bone, (x, y, z) degrees) turns a bone about the character's axes (x: bend forward, z: turn to
the character's left, y: tilt); aim(rig, bone, direction, palm=None) points a bone; hand(rig, side, shape).
"""
import math
import random

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector
from mathutils.bvhtree import BVHTree

from . import look, sdf

SKIN, HAIR, IRIS, IRIS_LO, PUPIL = "#ffd9c2", "#4a3328", "#b5652b", "#f0b072", "#2a1712"
LASH, BROW, NOSE, MOUTH, TONGUE = "#2b1b18", "#3a2620", "#e7a990", "#5c2228", "#d8606c"
JACKET, TEE, TROUSERS, SNEAKER, SOLE = "#7fae8a", "#f7f6f1", "#2e3550", "#ffb340", "#f4f1ea"
WATCH, WATCH_FACE, COAT = "#1d1d22", "#3b4250", "#f6f8fa"
LINE_BODY, LINE_HEAD, LINE_SMALL = 0.003, 0.0022, 0.0016

# rest pose (A-pose) joints in character space: feet at z=0, facing -Y; the character's right is -X
J = dict(
    hips=(0, 0, 0.93), waist=(0, 0, 1.03), chest=(0, 0, 1.22), neck=(0, 0.01, 1.44), head=(0, 0.005, 1.53),
    top=(0, 0.005, 1.78))


def _side(s):
    """Per-side joints; s = +1 for the character's left (+X), -1 for the right."""
    return dict(
        clav=(s * 0.03, 0.01, 1.40), shoulder=(s * 0.185, 0.015, 1.385), elbow=(s * 0.36, 0.03, 1.17),
        wrist=(s * 0.50, 0.01, 0.96), hip=(s * 0.085, 0.0, 0.90), knee=(s * 0.095, -0.012, 0.50),
        ankle=(s * 0.10, 0.015, 0.085), toe=(s * 0.105, -0.12, 0.03))


# ---------------------------------------------------------------------------------------------------------- SDF tools
def _bounded(f, lo, hi):
    f.bounds = (np.asarray(lo, float), np.asarray(hi, float))
    return f


def _union(fs, k=0.0):
    def f(p):
        d = fs[0](p)
        for g in fs[1:]:
            d = sdf.smin(d, g(p), k) if k > 0 else np.minimum(d, g(p))
        return d
    lo = np.min([g.bounds[0] for g in fs], axis=0)
    hi = np.max([g.bounds[1] for g in fs], axis=0)
    return _bounded(f, lo, hi)


def _below(z0):
    """Cutter for everything below height z0 (negative there)."""
    return lambda p: p[..., 2] - z0


def _above(z0):
    """Cutter for everything above height z0."""
    return lambda p: z0 - p[..., 2]


def _front_gap(w_lo, w_hi, z_lo, z_hi, y0=0.0):
    """Cutter for an open front: a strip |x| < w in front of y0, w going from w_lo (at z_lo) to w_hi (at z_hi)."""
    def c(p):
        t = np.clip((p[..., 2] - z_lo) / (z_hi - z_lo), 0, 1)
        w = w_lo + (w_hi - w_lo) * t
        return np.maximum(np.abs(p[..., 0]) - w, p[..., 1] - y0)
    return c


def _cut(f, *cutters):
    """f minus every cutter (cutters are plain functions, negative inside the part to remove)."""
    def g(p):
        d = f(p)
        for c in cutters:
            d = np.maximum(d, -c(p))
        return d
    return _bounded(g, *f.bounds)


def _keep(f, *keepers):
    """f intersected with every keeper (negative inside the part to keep)."""
    def g(p):
        d = f(p)
        for c in keepers:
            d = np.maximum(d, c(p))
        return d
    return _bounded(g, *f.bounds)


def _grow(f, r):
    def g(p):
        return f(p) - r
    return _bounded(g, f.bounds[0] - r, f.bounds[1] + r)


def _oe(c, axes, r):
    """Oriented ellipsoid: centre c, rows of `axes` = its local x, y, z directions, radii r."""
    c, A, r = np.asarray(c, float), np.asarray(axes, float), np.asarray(r, float)
    e = sdf.ellipsoid(np.zeros(3), r)

    def f(p):
        return e((p - c) @ A.T)
    m = float(np.max(r))
    return _bounded(f, c - m, c + m)


def _mesh(name, f, mat, res, smooth=10, pad=0.02):
    o = sdf.build(name, [(f, mat.name, None)], k=0.0, res=res, pad=pad, smooth_iter=smooth)
    _outward(o)
    return o


def _outward(o):
    """sdf.build's meshes come out facing inward here (scikit-image 0.26), which pushes look.outline's inverted hull
    inside the body, where it never shows: turn them outward."""
    me = o.data
    c = np.array([p.center for p in me.polygons])
    n = np.array([p.normal for p in me.polygons])
    if np.mean(((c - c.mean(axis=0)) * n).sum(axis=1) > 0) < 0.5:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        me.update()


# ---------------------------------------------------------------------------------------------------------- armature
FINGERS = ("thumb", "index", "middle", "ring", "pinky")


def _hand_frame(s):
    """Rest-pose hand frame for side s: wrist point, hand direction u, palm normal n (out of the palm), thumb side b."""
    j = _side(s)
    w = Vector(j["wrist"])
    u = (Vector(j["wrist"]) - Vector(j["elbow"])).normalized()
    u = (u + Vector((0, -0.02, -0.1))).normalized()
    n = Vector((-s, 0.0, 0.0))
    n = (n - n.dot(u) * u).normalized()
    b = u.cross(n) * (-s)                     # toward the thumb, i.e. forward (-Y) in the A-pose
    if b.y > 0:
        b = -b
    return w, u, n, b


def _finger_specs(s):
    """[(name, base, mid, tip, radius)] for one hand, rest pose."""
    w, u, n, b = _hand_frame(s)
    out = []
    # fingers 21 mm apart with 8.7 mm radius: a 3.6 mm gap (2 voxels at the hand's 1.8 mm resolution), so the mesh
    # never webs them together
    for fname, off, length, ang in (("index", 0.0315, 0.068, 6), ("middle", 0.0105, 0.075, 1),
                                    ("ring", -0.0105, 0.07, -4), ("pinky", -0.0315, 0.056, -10)):
        base = w + u * 0.086 + b * off
        d = (u * math.cos(math.radians(ang)) + b * math.sin(math.radians(ang))).normalized()
        out.append((fname, base, base + d * length * 0.55, base + d * length, 0.0087))
    tb = w + u * 0.022 + b * 0.024 + n * 0.006
    tm = tb + (u * 0.55 + b * 0.75 + n * 0.25).normalized() * 0.045
    tt = tm + (u * 0.85 + b * 0.35 + n * 0.25).normalized() * 0.036
    out.append(("thumb", tb, tm, tt, 0.0105))
    return out


def _armature(name):
    ad = bpy.data.armatures.new(f"{name}_armature")
    arm = bpy.data.objects.new(f"{name}_arm", ad)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    for o in bpy.context.selected_objects:
        o.select_set(False)
    arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = ad.edit_bones

    def bone(bn, h, t, parent=None, roll_z=None, connect=False):
        b = eb.new(bn)
        b.head, b.tail = Vector(h), Vector(t)
        if roll_z is not None:
            b.align_roll(Vector(roll_z))
        else:
            b.align_roll(Vector((0, -1, 0)) if abs(Vector(t)[2] - Vector(h)[2]) > abs(Vector(t)[1] - Vector(h)[1])
                         else Vector((0, 0, 1)))
        if parent:
            b.parent = eb[parent]
            b.use_connect = connect
        return b

    bone("hips", J["hips"], J["waist"])
    bone("spine", J["waist"], J["chest"], "hips", connect=True)
    bone("chest", J["chest"], J["neck"], "spine", connect=True)
    bone("neck", J["neck"], J["head"], "chest", connect=True)
    bone("head", J["head"], J["top"], "neck", connect=True)
    for s, sx in ((1, "L"), (-1, "R")):
        j = _side(s)
        bone(f"shoulder.{sx}", j["clav"], j["shoulder"], "chest")
        bone(f"upper_arm.{sx}", j["shoulder"], j["elbow"], f"shoulder.{sx}", connect=True)
        bone(f"forearm.{sx}", j["elbow"], j["wrist"], f"upper_arm.{sx}", connect=True)
        w, u, n, b = _hand_frame(s)
        bone(f"hand.{sx}", w, w + u * 0.086, f"forearm.{sx}", roll_z=n, connect=True)
        for fname, base, mid, tip, _ in _finger_specs(s):
            bone(f"{fname}1.{sx}", base, mid, f"hand.{sx}", roll_z=n)
            bone(f"{fname}2.{sx}", mid, tip, f"{fname}1.{sx}", roll_z=n, connect=True)
        bone(f"thigh.{sx}", j["hip"], j["knee"], "hips")
        bone(f"shin.{sx}", j["knee"], j["ankle"], f"thigh.{sx}", connect=True)
        bone(f"foot.{sx}", j["ankle"], j["toe"], f"shin.{sx}", connect=True)
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    return arm


def _segments(arm, names):
    out = []
    for bn in names:
        b = arm.data.bones[bn]
        out.append((bn, np.array(b.head_local), np.array(b.tail_local)))
    return out


def _skin(o, arm, bones, power=6.0, keep=3, bias=None):
    """Procedural weights: each vertex is shared between its nearest bones (inverse distance to the bone segments to
    `power`), at most `keep` bones. `bias` {bone: factor} makes a bone hold more (factor < 1 shrinks its distance)."""
    segs = _segments(arm, bones)
    V = np.array([v.co for v in o.data.vertices])
    D = []
    for bn, a, b in segs:
        ab = b - a
        h = np.clip(((V - a) @ ab) / (ab @ ab), 0, 1)
        d = np.linalg.norm(V - (a + h[:, None] * ab), axis=1)
        if bias and bn in bias:
            d = d * bias[bn]
        D.append(d)
    D = np.stack(D, axis=1)
    W = 1.0 / np.maximum(D, 1e-4) ** power
    order = np.argsort(-W, axis=1)[:, :keep]
    groups = {bn: o.vertex_groups.new(name=bn) for bn, _, _ in segs}
    names = [bn for bn, _, _ in segs]
    for vi in range(len(V)):
        idx = order[vi]
        w = W[vi, idx]
        w = w / w.sum()
        for j, wj in zip(idx, w):
            if wj > 0.01:
                groups[names[j]].add([vi], float(wj), "REPLACE")
    mod = o.modifiers.new("armature", "ARMATURE")
    mod.object = arm
    while o.modifiers[0].name != "armature":
        o.modifiers.move(len(o.modifiers) - 1, 0)
    o.parent = arm
    return o


def _bone_parent(o, arm, bone):
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy()
    o.parent = arm
    o.parent_type = "BONE"
    o.parent_bone = bone
    bpy.context.view_layer.update()
    o.matrix_world = mw
    return o


def _empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.03
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    if parent is not None:
        e.parent = parent
    return e


def _keep_parent(o, p):
    """Parent o to p without moving it (scaling p then scales o about p's origin: blinks, iris size)."""
    bpy.context.view_layer.update()
    o.parent = p
    o.matrix_parent_inverse = p.matrix_world.inverted()


# ---------------------------------------------------------------------------------------------------------- body
def _arm_bones(sx):
    return [f"shoulder.{sx}", f"upper_arm.{sx}", f"forearm.{sx}"]


TORSO = ["hips", "spine", "chest", "neck"]


def _torso_sdf(grow=0.0):
    E = sdf.E
    parts = [
        E((0, 0.006, 1.29), (0.150 + grow, 0.092 + grow, 0.13 + grow)),        # chest
        E((0, 0.004, 1.12), (0.128 + grow, 0.084 + grow, 0.12 + grow)),        # ribs / waist
        E((0, 0.004, 0.99), (0.135 + grow, 0.088 + grow, 0.09 + grow)),        # hips
        E((0.15, 0.015, 1.365), (0.065 + grow, 0.062 + grow, 0.05 + grow)),    # shoulder caps
        E((-0.15, 0.015, 1.365), (0.065 + grow, 0.062 + grow, 0.05 + grow)),
    ]
    if grow == 0.0:
        parts.append(E((0, 0.01, 1.448), (0.052, 0.048, 0.03)))      # the tee's crew neck, up the neck a little
    return _union(parts, 0.05)


def _sleeves(grow=0.0, cuff=0.86):
    C = sdf.C
    out = []
    for s in (1, -1):
        j = _side(s)
        sh, el, wr = (np.array(j[k], float) for k in ("shoulder", "elbow", "wrist"))
        end = el + (wr - el) * cuff
        out += [C(sh + (sh - el) * 0.12, el, 0.052 + grow, 0.046 + grow), C(el, end, 0.046 + grow, 0.043 + grow)]
    return out


def _jacket_sdf(open_w=(0.03, 0.055), length=0.885, grow=0.0, hood=True):
    torso = _grow(_torso_sdf(), 0.016 + grow)
    parts = [torso] + _sleeves(grow)
    if hood:
        E = sdf.E
        parts += [E((0, 0.075, 1.425), (0.105 + grow, 0.06 + grow, 0.052 + grow)),
                  E((0.068, 0.035, 1.43), (0.045 + grow, 0.07 + grow, 0.045 + grow)),
                  E((-0.068, 0.035, 1.43), (0.045 + grow, 0.07 + grow, 0.045 + grow)),
                  E((0.05, -0.035, 1.44), (0.03 + grow, 0.03 + grow, 0.04 + grow)),      # collar sides at the front
                  E((-0.05, -0.035, 1.44), (0.03 + grow, 0.03 + grow, 0.04 + grow))]
    f = _union(parts, 0.03)
    w0, w1 = open_w                            # the open front: narrow at the collar, wider at the hem
    return _cut(f, _front_gap(w1, w0, length, 1.45), _below(length))


def _trousers_sdf():
    E, C = sdf.E, sdf.C
    parts = [E((0, 0.006, 0.96), (0.142, 0.094, 0.085))]
    for s in (1, -1):
        j = _side(s)
        hip, knee, ank = (np.array(j[k], float) for k in ("hip", "knee", "ankle"))
        parts += [C(hip + (0, 0, 0.03), knee, 0.072, 0.056), C(knee, ank + (0, 0, 0.02), 0.056, 0.05),
                  E((s * 0.142, 0.0, 0.69), (0.028, 0.06, 0.07))]                 # cargo pocket
    f = _union(parts, 0.03)
    return _cut(f, _below(0.105), _above(1.02))


def _neck_sdf():
    return sdf.C((0, 0.012, 1.36), (0, 0.006, 1.57), 0.037, 0.035)


def _hand_sdf(s):
    w, u, n, b = _hand_frame(s)
    A = np.array([b, u, n], float)
    palm = _oe(np.array(w + u * 0.048 + n * 0.002), A, (0.042, 0.05, 0.016))
    wrist = sdf.C(np.array(w - u * 0.07), np.array(w + u * 0.02), 0.024, 0.026)
    pw = _union([palm, wrist], 0.02)
    fingers = [sdf.C(np.array(base), np.array(tip), r, r * 0.84) for _, base, _, tip, r in _finger_specs(s)]

    def f(p):
        dp = pw(p)
        d = None
        for g in fingers:
            x = sdf.smin(dp, g(p), 0.008)
            d = x if d is None else np.minimum(d, x)
        return d
    lo = np.min([pw.bounds[0]] + [g.bounds[0] for g in fingers], axis=0)
    hi = np.max([pw.bounds[1]] + [g.bounds[1] for g in fingers], axis=0)
    return _bounded(f, lo, hi)


def _hand_bones(sx):
    return [f"forearm.{sx}", f"hand.{sx}"] + [f"{fn}{i}.{sx}" for fn in FINGERS for i in (1, 2)]


# ---------------------------------------------------------------------------------------------------------- head
def _head_sdf():
    E, C = sdf.E, sdf.C
    parts = [
        E((0, 0.012, 1.655), (0.098, 0.108, 0.115)),          # cranium
        E((0, -0.008, 1.585), (0.083, 0.088, 0.072)),         # cheeks
        C((0.07, 0.0, 1.585), (0, -0.05, 1.522), 0.028, 0.018),   # jaw line to a slightly pointed chin
        C((-0.07, 0.0, 1.585), (0, -0.05, 1.522), 0.028, 0.018),
        E((0, -0.097, 1.588), (0.0075, 0.012, 0.011)),        # tiny nose
        E((0.097, 0.012, 1.612), (0.016, 0.026, 0.036)),      # ears
        E((-0.097, 0.012, 1.612), (0.016, 0.026, 0.036)),
    ]
    return _union(parts, 0.022)


def _hair_sdf(seed=7):
    """Messy anime hair: a cap over the skull, cut away from the face, plus tapered spikes (bangs, side tufts, crown,
    back) and one tall front cowlick. Seeded, so it is the same every build."""
    return _hair_locks(seed)


def _hair_locks(seed=7):
    """Anime hair built from tapered locks flowing out of a crown whorl over a small inner cap: the locks leave
    grooves between them (clumps), and their tips make the spiky silhouette. Front locks end as uneven bangs above the
    brows, temple and side locks at ear level, back locks flare out at the nape; a few crown spikes stand up and back,
    and one tall cowlick rises at the front."""
    rnd = random.Random(seed)
    C = sdf.C
    hc = np.array((0.0, 0.015, 1.655))
    cap = _cut(sdf.E((0, 0.02, 1.672), (0.104, 0.114, 0.118)),
               lambda p: np.maximum(p[..., 1] + 0.03, p[..., 2] - (1.715 - 0.06 * (np.abs(p[..., 0]) / 0.1) ** 2)),
               _below(1.58))

    def at(theta, phi, r):
        t, f = math.radians(theta), math.radians(phi)
        return hc + r * np.array((math.cos(f) * math.cos(t), math.cos(f) * math.sin(t), math.sin(f)))

    locks = []

    def lock(theta, root_phi, tip_phi, tip_r, r0=0.03, mid_out=0.012, bend=0.0):
        a = at(theta, root_phi, 0.1)
        m = at(theta + bend * 0.5, (root_phi + tip_phi) / 2, 0.118 + mid_out)
        b = at(theta + bend, tip_phi, tip_r)
        locks.append(C(a, m, r0, r0 * 0.7))
        locks.append(C(m, b, r0 * 0.7, 0.0025))

    # bangs (theta -90 = front): uneven lengths, sweeping a little toward his left
    for th, tip_phi in ((-128, 14), (-112, 9), (-97, 13), (-82, 7), (-67, 12), (-54, 18)):
        lock(th + rnd.uniform(-3, 3), 72, tip_phi + rnd.uniform(-2, 2), 0.112, 0.028, 0.008, bend=8)
    # temples and sides, ending about ear level
    for th in (-40, -20, 0, 20, 40, 140, 160, 180, 200, 220):
        lock(th + rnd.uniform(-4, 4), 60, -28 + rnd.uniform(-6, 4), 0.132 + rnd.uniform(0, 0.012), 0.032)
    # back: flaring out at the nape
    for th in (60, 75, 90, 105, 120):
        lock(th + rnd.uniform(-4, 4), 60, -38 + rnd.uniform(-5, 5), 0.15 + rnd.uniform(0, 0.015), 0.034, 0.02)
    # crown spikes standing up and back
    for th, tip_phi, r in ((50, 30, 0.165), (90, 35, 0.17), (130, 28, 0.162), (70, 48, 0.158), (110, 50, 0.16),
                           (20, 40, 0.15), (160, 42, 0.152)):
        lock(th + rnd.uniform(-5, 5), 80, tip_phi, r, 0.03, 0.02)
    # the tall front cowlick: a thin lock that rises from the front of the hair and curls forward at the tip
    cw = [(0.012, -0.04, 1.775), (0.009, -0.058, 1.815), (0.003, -0.08, 1.838), (-0.004, -0.1, 1.836),
          (-0.01, -0.114, 1.82)]
    for (a, b), (ra, rb) in zip(zip(cw, cw[1:]), ((0.0072, 0.0055), (0.0055, 0.004), (0.004, 0.0025),
                                                  (0.0025, 0.001))):
        locks.append(C(np.array(a), np.array(b), ra, rb))

    def f(p):
        d = cap(p)
        for g in locks:
            d = sdf.smin(d, g(p), 0.006)
        return d
    lo = np.min([cap.bounds[0]] + [g.bounds[0] for g in locks], axis=0)
    hi = np.max([cap.bounds[1]] + [g.bounds[1] for g in locks], axis=0)
    return _bounded(f, lo, hi)


def _hair_spikes(seed=7):
    """First version (a cap with spikes), kept for comparison."""
    rnd = random.Random(seed)
    E, C = sdf.E, sdf.C
    cap = E((0, 0.018, 1.678), (0.11, 0.122, 0.13))

    def face_window(p):                         # the face and forehead below the hairline, in front of the ears
        x, y, z = p[..., 0], p[..., 1], p[..., 2]
        hairline = 1.712 - 0.06 * (np.abs(x) / 0.1) ** 2
        return np.maximum(y + 0.025, z - hairline)

    cap = _cut(cap, face_window, _below(1.565))
    spikes = []

    def spike(a, b, ra, rb=0.003):
        spikes.append(C(np.array(a, float), np.array(b, float), ra, rb))

    # bangs: five uneven, pointed locks sweeping a little to his left, tips above the brows
    for x, dz, sweep in ((-0.066, 0.012, 0.01), (-0.036, -0.004, 0.016), (-0.006, 0.006, 0.02),
                         (0.026, -0.008, 0.018), (0.058, 0.01, 0.012)):
        top = (x * 0.85, -0.075 + abs(x) * 0.3, 1.765)
        tip = (x * 1.05 + sweep, -0.107 + abs(x) * 0.42, 1.678 + dz + rnd.uniform(-0.003, 0.003))
        spike(top, tip, 0.022, 0.0025)
    # side tufts over the ears, pointing down and a little out, ending about ear level
    for s in (1, -1):
        for k, (dz, dy) in enumerate(((0.0, -0.035), (-0.012, 0.0), (0.0, 0.035))):
            a = (s * 0.09, dy, 1.685 + dz)
            b = (s * (0.118 + 0.008 * k), dy - 0.008, 1.6 + dz + rnd.uniform(-0.008, 0.008))
            spike(a, b, 0.02, 0.003)
    # crown and back: spikes fanning out backward, the spiky silhouette in 3/4 and profile
    for i in range(12):
        ang = math.radians(-77 + i * 14)
        a = (math.sin(ang) * 0.07, 0.035 + math.cos(ang) * 0.02, 1.76 - abs(math.sin(ang)) * 0.03)
        b = (math.sin(ang) * 0.15 + rnd.uniform(-0.01, 0.01), 0.14 + rnd.uniform(-0.012, 0.012),
             1.7 + rnd.uniform(-0.03, 0.03) - abs(math.sin(ang)) * 0.06)
        spike(a, b, 0.028, 0.003)
    for i in range(6):
        x = -0.06 + i * 0.024
        spike((x, 0.07, 1.66), (x * 1.35 + rnd.uniform(-0.008, 0.008), 0.125, 1.575 + rnd.uniform(-0.01, 0.01)),
              0.024, 0.003)
    # top: spikes standing up and back, so the crown is round, not flat
    for x, y, h in ((-0.05, 0.0, 1.81), (0.045, 0.01, 1.815), (0.0, 0.04, 1.825), (-0.02, -0.03, 1.818)):
        spike((x * 0.6, y, 1.76), (x * 1.5, y + 0.07, h + rnd.uniform(-0.006, 0.006)), 0.026, 0.003)
    # the tall front cowlick: a thin lock that rises from the front of the hair and curls forward at the tip
    cw = [(0.012, -0.05, 1.79), (0.006, -0.062, 1.845), (-0.004, -0.075, 1.885), (-0.012, -0.092, 1.9)]
    for (a, b), (ra, rb) in zip(zip(cw, cw[1:]), ((0.012, 0.0085), (0.0085, 0.005), (0.005, 0.0018))):
        spike(a, b, ra, rb)

    def f(p):
        d = cap(p)
        for g in spikes:
            d = sdf.smin(d, g(p), 0.012)
        return d
    lo = np.min([cap.bounds[0]] + [g.bounds[0] for g in spikes], axis=0)
    hi = np.max([cap.bounds[1]] + [g.bounds[1] for g in spikes], axis=0)
    return _bounded(f, lo, hi)


# ---------------------------------------------------------------------------------------------------------- face decals
def _ellipse(cx, cz, a, b, n=40, rot=0.0, top=1.0, bottom=1.0):
    pts = []
    cr, sr = math.cos(rot), math.sin(rot)
    for i in range(n):
        t = 2 * math.pi * i / n
        x, z = a * math.cos(t), b * math.sin(t) * (top if math.sin(t) > 0 else bottom)
        pts.append((cx + x * cr - z * sr, cz + x * sr + z * cr))
    return pts


def _clip(poly, clip):
    """Sutherland-Hodgman: poly clipped by a convex, counter-clockwise polygon (both [(x, z)])."""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

    def inter(p, q, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p, *q, *a, *b
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    out = list(poly)
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        src, out = out, []
        if not src:
            break
        for j in range(len(src)):
            p, q = src[j], src[(j + 1) % len(src)]
            if inside(q, a, b):
                if not inside(p, a, b):
                    out.append(inter(p, q, a, b))
                out.append(q)
            elif inside(p, a, b):
                out.append(inter(p, q, a, b))
    return out


class _Face:
    """Projects 2D shapes (x, z in the front view) onto the head surface as thin decals."""

    def __init__(self, head):
        dg = bpy.context.evaluated_depsgraph_get()
        self.bvh = BVHTree.FromObject(head, dg)

    def project(self, x, z, off):
        hit = self.bvh.ray_cast(Vector((x, -0.4, z)), Vector((0, 1, 0)))
        if hit[0] is None:
            return None
        n = hit[1] if hit[1].y < 0 else -hit[1]   # sdf.build meshes come out with inward normals: face the viewer
        return hit[0] + n * off

    def _obj(self, name, verts2d, faces, off, mat):
        V = []
        for x, z in verts2d:
            p = self.project(x, z, off)
            V.append(p if p is not None else Vector((x, -0.05, z)))
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(v) for v in V], [], faces)
        me.update()
        o = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(mat)
        return o

    def fan(self, name, poly, off, mat, rings=4):
        """A filled shape (star-shaped around its centroid)."""
        cx = sum(p[0] for p in poly) / len(poly)
        cz = sum(p[1] for p in poly) / len(poly)
        n = len(poly)
        verts = [(cx, cz)]
        for k in range(1, rings + 1):
            t = k / rings
            verts += [(cx + (x - cx) * t, cz + (z - cz) * t) for x, z in poly]
        faces = [(0, 1 + (i + 1) % n, 1 + i) for i in range(n)]
        for k in range(rings - 1):
            a0, b0 = 1 + k * n, 1 + (k + 1) * n
            faces += [(a0 + i, a0 + (i + 1) % n, b0 + (i + 1) % n, b0 + i) for i in range(n)]
        faces = [f[::-1] for f in faces]       # face the camera (-Y)
        return self._obj(name, verts, faces, off, mat)

    def strip(self, name, upper, lower, off, mat, rows=2):
        """A band between two curves with the same number of points (lines, lashes, brows, crescents)."""
        n = len(upper)
        verts = []
        for r in range(rows + 1):
            t = r / rows
            verts += [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for a, b in zip(upper, lower)]
        faces = []
        for r in range(rows):
            for i in range(n - 1):
                a, b = r * n + i, (r + 1) * n + i
                faces.append((a, a + 1, b + 1, b))
        if (upper[-1][0] - upper[0][0]) < 0:
            faces = [f[::-1] for f in faces]
        return self._obj(name, verts, faces, off, mat)


def _line(pts, w0, w1=None, n=24):
    """A tapered band along a polyline: (upper, lower) curves, width w0 at the start and w1 at the end."""
    w1 = w0 if w1 is None else w1
    P = np.array(pts, float)
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)]) / max(1e-9, seg.sum())
    ts = np.linspace(0, 1, n)
    X, Z = np.interp(ts, s, P[:, 0]), np.interp(ts, s, P[:, 1])
    up, lo = [], []
    for i in range(n):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        tx, tz = X[j1] - X[j0], Z[j1] - Z[j0]
        L = math.hypot(tx, tz) or 1
        nx, nz = -tz / L, tx / L
        w = (w0 + (w1 - w0) * ts[i]) * math.sin(math.pi * min(1.0, 0.15 + ts[i] * 0.85)) ** 0.25 / 2
        up.append((X[i] + nx * w, Z[i] + nz * w))
        lo.append((X[i] - nx * w, Z[i] - nz * w))
    return up, lo


def _face(head, name, head_bone, arm, mats):
    F = _Face(head)
    objs, eyes, irises, brows = [], [], [], []
    EYE_Z, EYE_X = 1.622, 0.041
    for s in (1, -1):
        cx = s * EYE_X
        piv = _empty(f"{name}_eyepiv{s}", (cx, -0.09, EYE_Z))
        white_poly = _ellipse(cx, EYE_Z - 0.001, 0.0215, 0.0175, 48, rot=s * math.radians(4), top=0.82)
        parts = [F.fan(f"{name}_eyewhite{s}", white_poly, 0.0007, mats["white"])]
        ix = cx - s * 0.002
        iris_poly = _clip(_ellipse(ix, EYE_Z - 0.0015, 0.0128, 0.0162, 40), white_poly)
        ipiv = _empty(f"{name}_irispiv{s}", (ix, -0.09, EYE_Z - 0.002))
        iris = F.fan(f"{name}_iris{s}", iris_poly, 0.0013, mats["iris"])
        pupil = F.fan(f"{name}_pupil{s}", _clip(_ellipse(ix, EYE_Z + 0.0005, 0.0068, 0.0092, 32), white_poly),
                      0.0019, mats["pupil"])
        # the lighter crescent low in the iris
        xs = np.linspace(ix - 0.0095, ix + 0.0095, 14)
        lo_c, up_c = [], []
        for x in xs:
            t = (x - ix) / 0.0128
            zl = EYE_Z - 0.0015 - 0.0162 * math.sqrt(max(0.0, 1 - t * t)) + 0.0016
            zu = EYE_Z - 0.0015 - 0.0098 * math.sqrt(max(0.0, 1 - ((x - ix) / 0.0098) ** 2)) + 0.0005
            lo_c.append((x, zl))
            up_c.append((x, max(zl, zu)))
        cres = F.strip(f"{name}_cres{s}", up_c, lo_c, 0.0024, mats["iris_lo"])
        hi1 = F.fan(f"{name}_hi{s}", _ellipse(ix - s * 0.0048, EYE_Z + 0.0065, 0.0042, 0.0052, 20,
                                              rot=s * 0.4), 0.0031, mats["hi"])
        hi2 = F.fan(f"{name}_hi2_{s}", _ellipse(ix + s * 0.0045, EYE_Z - 0.0072, 0.0018, 0.0018, 14),
                    0.0031, mats["hi"])
        for o in (iris, pupil, cres, hi1, hi2):
            _keep_parent(o, ipiv)
        # upper lash line: thick, with a small flick at the outer corner
        top = [p for p in white_poly if p[1] > EYE_Z - 0.004]
        top.sort(key=lambda p: p[0] * s)
        top = [(x, z + 0.0012) for x, z in top] + [(cx + s * 0.026, EYE_Z + 0.0045)]
        up, lo = _line(top, 0.0034, 0.0052, 30)
        lash = F.strip(f"{name}_lash{s}", up, lo, 0.0036, mats["lash"])
        low = [(cx + s * 0.006, EYE_Z - 0.0165), (cx + s * 0.016, EYE_Z - 0.0135), (cx + s * 0.021, EYE_Z - 0.0085)]
        up2, lo2 = _line(low, 0.0011, 0.0016, 12)
        lash2 = F.strip(f"{name}_lashlo{s}", up2, lo2, 0.0036, mats["lash"])
        parts += [lash, lash2]
        for o in parts:
            _keep_parent(o, piv)
        _keep_parent(ipiv, piv)
        eyes.append(piv)
        irises.append(ipiv)
        objs += parts + [iris, pupil, cres, hi1, hi2]
        # brow
        bpiv = _empty(f"{name}_browpiv{s}", (s * 0.044, -0.09, 1.664))
        bpts = [(s * 0.02, 1.659), (s * 0.034, 1.6655), (s * 0.05, 1.668), (s * 0.066, 1.6635)]
        up, lo = _line(bpts, 0.0052, 0.0028, 20)
        brow = F.strip(f"{name}_brow{s}", up, lo, 0.0016, mats["brow"])
        _keep_parent(brow, bpiv)
        brows.append(bpiv)
        objs.append(brow)
    # nose: a small shaded stroke under the tip
    up, lo = _line([(-0.006, 1.5805), (0.0, 1.578), (0.004, 1.5795)], 0.0018, 0.0012, 10)
    objs.append(F.strip(f"{name}_nose", up, lo, 0.0012, mats["nose"]))
    # mouths
    MZ = 1.546
    mouths = {}
    up, lo = _line([(-0.011, MZ + 0.0008), (0.0, MZ - 0.0004), (0.011, MZ + 0.0008)], 0.0019, 0.0019, 16)
    mouths["neutral"] = [F.strip(f"{name}_m_neutral", up, lo, 0.0012, mats["mouth"])]
    o_poly = _ellipse(0, MZ - 0.002, 0.0082, 0.0108, 32)
    tongue = _clip(_ellipse(0, MZ - 0.0105, 0.0065, 0.0055, 24), o_poly)
    mouths["o"] = [F.fan(f"{name}_m_o", o_poly, 0.0012, mats["mouth"]),
                   F.fan(f"{name}_m_o_t", tongue, 0.0018, mats["tongue"])]
    smile = [(0.014 * math.cos(t), MZ + 0.002 - 0.0115 * max(0.0, math.sin(t)) * (1 if math.sin(t) > 0 else 0))
             for t in np.linspace(math.pi, 2 * math.pi, 24)]
    smile = [(x, MZ + 0.002 - 0.0115 * math.sqrt(max(0.0, 1 - (x / 0.014) ** 2))) for x, _ in smile]
    smile_poly = smile + [(0.0145, MZ + 0.0026), (-0.0145, MZ + 0.0026)]
    smile_poly = [(x, z) for x, z in smile_poly]
    mouths["smile"] = [F.fan(f"{name}_m_smile", _ccw(smile_poly), 0.0012, mats["mouth"]),
                       F.fan(f"{name}_m_smile_t", _clip(_ellipse(0, MZ - 0.0075, 0.0075, 0.004, 24),
                                                         _ccw(smile_poly)), 0.0018, mats["tongue"])]
    tw, th = 0.0135, 0.0062
    rect = [(-tw, MZ - th), (tw, MZ - th), (tw, MZ + th), (-tw, MZ + th)]
    rect = _round_rect(0, MZ, tw, th, 0.003)
    ring_up, ring_lo = rect, [(x * 1.0, z) for x, z in _round_rect(0, MZ, tw + 0.0019, th + 0.0019, 0.0045)]
    mouths["teeth"] = [F.fan(f"{name}_m_teeth", rect, 0.0012, mats["white"]),
                       F.strip(f"{name}_m_teeth_o", ring_lo + ring_lo[:1], ring_up + ring_up[:1], 0.0016,
                               mats["mouth"], rows=1)]
    up, lo = _line([(-tw, MZ), (tw, MZ)], 0.0011, 0.0011, 8)
    mouths["teeth"].append(F.strip(f"{name}_m_teeth_l", up, lo, 0.0018, mats["mouth"]))
    for i, x in enumerate((-0.0068, 0.0, 0.0068)):
        up, lo = _line([(x, MZ - th), (x, MZ + th)], 0.0009, 0.0009, 4)
        mouths["teeth"].append(F.strip(f"{name}_m_teeth_v{i}", up, lo, 0.0018, mats["mouth"]))
    head_objs = objs + [o for v in mouths.values() for o in v]
    for o in head_objs:
        o.visible_shadow = False
    for piv in eyes + brows:
        _bone_parent(piv, arm, head_bone)
    for v in mouths.values():
        for o in v:
            _bone_parent(o, arm, head_bone)
    nose = [o for o in objs if o.name.endswith("_nose")]
    for o in nose:
        _bone_parent(o, arm, head_bone)
    for piv in eyes + brows + irises:             # rest transforms, so expressions compose on top of them
        piv.rotation_mode = "QUATERNION"
        piv["rest_loc"] = tuple(piv.location)
        piv["rest_rot"] = tuple(piv.rotation_quaternion)
    return dict(eyes=eyes, irises=irises, brows=brows, mouths=mouths, objs=head_objs + eyes + brows + irises)


def _ccw(poly):
    a = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
            for i in range(len(poly)))
    return poly if a > 0 else poly[::-1]


def _round_rect(cx, cz, hw, hh, r, n=6):
    pts = []
    for qx, qz, a0 in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        ccx, ccz = cx + qx * (hw - r), cz + qz * (hh - r)
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((ccx + r * math.cos(a), ccz + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------------------------------------------------- props
def _shoe(name, s, mats):
    j = _side(s)
    x, ay = j["ankle"][0], j["ankle"][1]
    E, C = sdf.E, sdf.C
    upper = _union([E((x, -0.035, 0.06), (0.054, 0.122, 0.05)), E((x, -0.11, 0.048), (0.05, 0.06, 0.04)),
                    C((x, ay + 0.005, 0.05), (x, ay + 0.008, 0.125), 0.052, 0.047)], 0.03)
    upper = _cut(upper, _below(0.028), _above(0.128))
    up = _mesh(f"{name}_shoe{s}", upper, mats["sneaker"], 0.004, 8)
    sole = _keep(E((x, -0.04, 0.026), (0.06, 0.132, 0.04)), lambda p: p[..., 2] - 0.032, lambda p: -p[..., 2])
    so = _mesh(f"{name}_sole{s}", sole, mats["sole"], 0.004, 6)
    # laces: three short white bars across the top
    laces = []
    for i in range(3):
        y = -0.05 - i * 0.026
        z = 0.105 - i * 0.012
        laces.append(C((x - 0.022, y, z), (x + 0.022, y, z), 0.0055))
    la = _mesh(f"{name}_laces{s}", _union(laces), mats["sole"], 0.0025, 4)
    for o, w in ((up, LINE_BODY), (so, LINE_BODY), (la, LINE_SMALL)):
        look.outline(o, w)
    return [up, so, la]


def _watch(name, mats):
    j = _side(-1)
    el, wr = Vector(j["elbow"]), Vector(j["wrist"])
    u = (wr - el).normalized()
    c = wr - u * 0.012
    bpy.ops.mesh.primitive_torus_add(major_radius=0.0265, minor_radius=0.0062, major_segments=32, minor_segments=8,
                                     location=c)
    band = bpy.context.object
    band.name = f"{name}_watchband"
    band.rotation_mode = "QUATERNION"
    band.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(u)
    band.data.materials.append(mats["watch"])
    out = Vector((0, 0, 1)) - u * u.z
    out = (out + Vector((0, -0.4, 0)) - u * (Vector((0, -0.4, 0)).dot(u))).normalized()
    bpy.ops.mesh.primitive_cube_add(size=1, location=c + out * 0.029)
    face = bpy.context.object
    face.name = f"{name}_watchface"
    face.rotation_mode = "QUATERNION"
    q = Vector((0, 0, 1)).rotation_difference(out)
    face.rotation_quaternion = q
    face.scale = (0.017, 0.02, 0.0065)
    face.data.materials.append(mats["watch"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=c + out * 0.0325)
    scr = bpy.context.object
    scr.name = f"{name}_watchscreen"
    scr.rotation_mode = "QUATERNION"
    scr.rotation_quaternion = q
    scr.scale = (0.012, 0.014, 0.001)
    scr.data.materials.append(mats["watch_face"])
    for o in (band, face):
        for p in o.data.polygons:
            p.use_smooth = o is band
        look.outline(o, LINE_SMALL)
    return [band, face, scr]


def _cords(name, mats):
    C = sdf.C
    parts = [C((s * 0.034, -0.086, 1.405), (s * 0.038, -0.112, 1.29), 0.0045, 0.004) for s in (1, -1)]
    parts += [sdf.E((s * 0.038, -0.113, 1.283), (0.0075, 0.0075, 0.011)) for s in (1, -1)]
    o = _mesh(f"{name}_cords", _union(parts), mats["sole"], 0.002, 4)
    look.outline(o, LINE_SMALL)
    return o


# ---------------------------------------------------------------------------------------------------------- build
def _materials(name):
    hx = look.hexc
    T, Fl = look.toon, look.flat
    # skin: the same anime cel shader with a lower shadow threshold, so a face stays flat-lit like a drawn one and only
    # cast shadows (bangs, chin) and planes turned well away from the light go dark
    skin = bpy.data.materials.get(f"{name}_skin") or look._anime(f"{name}_skin", hx(SKIN), threshold=0.22)
    return dict(
        skin=skin, hair=T(f"{name}_hair", hx(HAIR)), jacket=T(f"{name}_jacket", hx(JACKET)),
        tee=T(f"{name}_tee", hx(TEE)), trousers=T(f"{name}_trousers", hx(TROUSERS)),
        sneaker=T(f"{name}_sneaker", hx(SNEAKER)), sole=T(f"{name}_sole", hx(SOLE)),
        watch=T(f"{name}_watch", hx(WATCH), gloss=True), watch_face=Fl(f"{name}_watchface", hx(WATCH_FACE)),
        coat=T(f"{name}_coat", hx(COAT)),
        white=Fl(f"{name}_eyewhite", hx("#ffffff")), iris=Fl(f"{name}_iris", hx(IRIS)),
        iris_lo=Fl(f"{name}_irislo", hx(IRIS_LO)), pupil=Fl(f"{name}_pupil", hx(PUPIL)),
        hi=Fl(f"{name}_hi", (1, 1, 1, 1)), lash=Fl(f"{name}_lash", hx(LASH)), brow=Fl(f"{name}_brow", hx(BROW)),
        nose=Fl(f"{name}_nose", hx(NOSE)), mouth=Fl(f"{name}_mouth", hx(MOUTH)),
        tongue=Fl(f"{name}_tongue", hx(TONGUE)))


def build(loc=(0, 0, 0), name="kai", outfit="world"):
    """Build Kai at `loc` (feet at z=0, facing -Y). outfit "lab" adds the open white lab coat."""
    mats = _materials(name)
    root = _empty(f"{name}_root", (0, 0, 0))
    root.empty_display_size = 0.3
    arm = _armature(name)
    arm.parent = root
    allb = [b.name for b in arm.data.bones]
    meshes, rigid = [], []
    side = {1: "L", -1: "R"}

    neck = _mesh(f"{name}_neck", _neck_sdf(), mats["skin"], 0.004, 8)
    _skin(neck, arm, ["chest", "neck", "head"])
    tee = _mesh(f"{name}_tee", _torso_sdf(), mats["tee"], 0.006, 10)
    _skin(tee, arm, TORSO + ["shoulder.L", "shoulder.R"])
    jacket = _mesh(f"{name}_jacket", _jacket_sdf(), mats["jacket"], 0.0055, 10)
    _skin(jacket, arm, TORSO + _arm_bones("L") + _arm_bones("R"))
    trousers = _mesh(f"{name}_trousers", _trousers_sdf(), mats["trousers"], 0.006, 10)
    _skin(trousers, arm, ["hips", "spine", "thigh.L", "shin.L", "thigh.R", "shin.R"], bias={"hips": 1.3})
    cords = _cords(name, mats)
    _skin(cords, arm, ["chest", "neck"])
    meshes += [neck, tee, jacket, trousers, cords]
    for s in (1, -1):
        h = _mesh(f"{name}_hand{side[s]}", _hand_sdf(s), mats["skin"], 0.0018, 6)
        _skin(h, arm, _hand_bones(side[s]), power=8)
        meshes.append(h)
    if outfit == "lab":
        coat = _mesh(f"{name}_coat", _coat_sdf(), mats["coat"], 0.006, 10)
        _skin(coat, arm, TORSO + _arm_bones("L") + _arm_bones("R") + ["thigh.L", "thigh.R"],
              bias={"hips": 0.55, "spine": 0.8})
        meshes.append(coat)
    for o in meshes:
        look.outline(o, LINE_SMALL if o is cords else LINE_BODY)
        for p in o.data.polygons:
            p.use_smooth = True

    head = _mesh(f"{name}_head", _head_sdf(), mats["skin"], 0.003, 10)
    hair = _mesh(f"{name}_hair", _hair_sdf(), mats["hair"], 0.0028, 6)
    look.outline(hair, LINE_HEAD)
    bpy.context.view_layer.update()
    face = _face(head, name, "head", arm, mats)          # before the head's outline, so decals sit on the skin
    look.outline(head, LINE_HEAD)
    for o in (head, hair):
        for p in o.data.polygons:
            p.use_smooth = True
    _bone_parent(head, arm, "head")
    _bone_parent(hair, arm, "head")
    for s in (1, -1):
        for o in _shoe(name, s, mats):
            _bone_parent(o, arm, f"foot.{side[s]}")
            rigid.append(o)
    for o in _watch(name, mats):
        _bone_parent(o, arm, "forearm.R")
        rigid.append(o)
    look.blob_shadow(f"{name}_shadow", (0, -0.02, 0.004), (0.32, 0.26), root)
    root.location = loc
    bpy.context.view_layer.update()
    rig = dict(root=root, arm=arm, name=name, outfit=outfit, meshes=meshes, rigid=rigid, head=head, hair=hair,
               eyes=face["eyes"], irises=face["irises"], brows=face["brows"], mouths=face["mouths"],
               head_parts=[head, hair] + face["objs"], bones=allb)
    set_mouth(rig, "neutral")
    return rig


def _coat_sdf():
    torso = _grow(_torso_sdf(), 0.034)
    E, C = sdf.E, sdf.C
    skirt = [C((0, 0.005, 0.98), (0, 0.01, 0.56), 0.17, 0.205)]
    collar = [E((0, 0.07, 1.45), (0.112, 0.07, 0.05)), E((0.08, 0.03, 1.445), (0.05, 0.075, 0.05)),
              E((-0.08, 0.03, 1.445), (0.05, 0.075, 0.05))]
    f = _union([torso] + _sleeves(0.016, cuff=0.84) + skirt + collar, 0.035)
    return _cut(f, _front_gap(0.105, 0.045, 0.56, 1.45), _below(0.56))   # a wider open front than the hoodie


# ---------------------------------------------------------------------------------------------------------- posing
def _pb(rig, bone):
    return rig["arm"].pose.bones[bone]


def reset(rig):
    """Back to the rest pose (A-pose), face neutral."""
    for pb in rig["arm"].pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)
    bpy.context.view_layer.update()


def rot(rig, bone, deg):
    """Turn `bone` (and its children) about the character's own axes by (x, y, z) degrees, on top of its current pose:
    x bends it forward (toward -Y), z turns it toward the character's left (+X), y tilts it toward -X."""
    pb = _pb(rig, bone)
    bpy.context.view_layer.update()
    M = pb.matrix.copy()
    h = M.translation.copy()
    R = Matrix.Rotation(math.radians(deg[2]), 4, "Z") @ Matrix.Rotation(math.radians(deg[1]), 4, "Y") @ \
        Matrix.Rotation(math.radians(deg[0]), 4, "X")
    pb.matrix = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
    bpy.context.view_layer.update()


def aim(rig, bone, direction, palm=None):
    """Point `bone` along `direction` (character space). `palm`: where the bone's local Z (palm side for hands and
    fingers) should face."""
    pb = _pb(rig, bone)
    bpy.context.view_layer.update()
    M = pb.matrix.copy()
    h = M.translation.copy()
    y = Vector(direction).normalized()
    if palm is None:
        cur = (M.to_3x3() @ Vector((0, 1, 0))).normalized()
        R = cur.rotation_difference(y).to_matrix()
        new = R @ M.to_3x3()
    else:
        z = Vector(palm)
        z = (z - z.dot(y) * y).normalized()
        x = y.cross(z)
        new = Matrix((x, y, z)).transposed()
    N = new.to_4x4()
    N.translation = h
    pb.matrix = N
    bpy.context.view_layer.update()


def move(rig, bone, offset):
    """Shift a bone (normally "hips") by `offset` in character space."""
    pb = _pb(rig, bone)
    bpy.context.view_layer.update()
    M = pb.matrix.copy()
    M.translation = M.translation + Vector(offset)
    pb.matrix = M
    bpy.context.view_layer.update()


HAND_SHAPES = {        # (base curl, tip curl) per finger, degrees; thumb separately
    "open": dict(f=(2, 2), spread=8, thumb=(0, 0)),
    "relax": dict(f=(22, 28), spread=2, thumb=(10, 15)),
    "point": dict(f=(80, 95), spread=0, thumb=(35, 40), index=(0, 0)),
    "fist": dict(f=(88, 100), spread=0, thumb=(45, 50)),
    "claw": dict(f=(35, 45), spread=10, thumb=(15, 20)),
}


def hand(rig, side, shape="relax"):
    """Curl the fingers of hand `side` ("L"/"R") into a shape: open, relax, point, fist, claw."""
    sh = HAND_SHAPES[shape]
    for fn in FINGERS:
        c1, c2 = sh.get(fn, sh["thumb"] if fn == "thumb" else sh["f"])
        spread = {"index": 1, "middle": 0.2, "ring": -0.5, "pinky": -1.2}.get(fn, 0) * sh["spread"]
        q1 = Quaternion((1, 0, 0), math.radians(c1)) @ Quaternion((0, 0, 1), math.radians(spread * (1 if side == "L" else -1)))
        _pb(rig, f"{fn}1.{side}").rotation_quaternion = q1
        _pb(rig, f"{fn}2.{side}").rotation_quaternion = Quaternion((1, 0, 0), math.radians(c2))
    bpy.context.view_layer.update()


def key(rig, f, interp="BEZIER"):
    """Key every bone's pose at frame f."""
    arm = rig["arm"]
    for pb in arm.pose.bones:
        pb.keyframe_insert(data_path="rotation_quaternion", frame=f, group=pb.name)
        pb.keyframe_insert(data_path="location", frame=f, group=pb.name)
    if interp != "BEZIER" and arm.animation_data and arm.animation_data.action:
        from .anim import all_fcurves
        for fc in all_fcurves(arm.animation_data.action):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - f) < 0.01:
                    kp.interpolation = interp


def _constant_keys(o):
    from .anim import all_fcurves
    if o.animation_data and o.animation_data.action:
        for fc in all_fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def set_mouth(rig, shape, f=None):
    """Show one mouth shape ("neutral", "o", "smile", "teeth"); keyed (constant) when f is given."""
    for k, objs in rig["mouths"].items():
        for o in objs:
            o.scale = (1, 1, 1) if k == shape else (0, 0, 0)
            if f is not None:
                o.keyframe_insert(data_path="scale", frame=f)
                _constant_keys(o)


EXPRESSIONS = {        # mouth, brow (raise, tilt deg: + = inner end up), eye open (z scale), iris scale
    "neutral": ("neutral", 0.0, 0, 1.0, 1.0),
    "shock": ("o", 0.006, 10, 1.12, 0.72),
    "smile": ("smile", 0.002, -4, 0.92, 1.0),
    "gritted": ("teeth", -0.002, -14, 0.7, 0.9),
}


def expression(rig, name, f=None):
    """Set (and key at f) a face: neutral, shock, smile, gritted."""
    mouth, raise_, tilt, eye_z, iris_s = EXPRESSIONS[name]
    set_mouth(rig, mouth, f)
    for i, b in enumerate(rig["brows"]):
        s = 1 if i == 0 else -1
        rl = b["rest_loc"]
        b.location = (rl[0], rl[1] + raise_, rl[2])          # the head bone's Y is world up at rest
        # tilt in the face plane, about the pivot's own Y (the face normal): + raises the inner end
        b.rotation_quaternion = Quaternion(b["rest_rot"]) @ Quaternion((0, 1, 0), s * math.radians(tilt))
    for e in rig["eyes"]:
        e.scale = (1.0, 1.0, eye_z)
    for e in rig["irises"]:
        e.scale = (iris_s, iris_s, iris_s)
    if f is not None:
        for b in rig["brows"]:
            b.keyframe_insert("location", frame=f)
            b.keyframe_insert("rotation_quaternion", frame=f)
        for e in rig["eyes"] + rig["irises"]:
            e.keyframe_insert("scale", frame=f)


def blink(rig, f):
    from . import anim
    anim.blink(rig, f)


# ---------------------------------------------------------------------------------------------------------- poses
def stand(rig, f=None):
    """Relaxed standing: arms down at the sides, hands relaxed."""
    reset(rig)
    for sx, s in (("L", 1), ("R", -1)):
        aim(rig, f"upper_arm.{sx}", (s * 0.16, 0.02, -1))
        aim(rig, f"forearm.{sx}", (s * 0.1, -0.22, -1))
        aim(rig, f"hand.{sx}", (s * 0.08, -0.12, -1), palm=(-s, 0.1, 0))
        hand(rig, sx, "relax")
    if f is not None:
        key(rig, f)


def sit_at_desk(rig, f=None, desk=0.76):
    """S03: sitting at the lab desk, leaning toward a tank, forearms on the desk (desk top at `desk` m)."""
    reset(rig)
    move(rig, "hips", (0, 0.04, -0.4))
    rot(rig, "hips", (-4, 0, 0))
    rot(rig, "spine", (20, 0, 0))
    rot(rig, "chest", (12, 0, -4))
    rot(rig, "neck", (6, 0, -6))
    rot(rig, "head", (8, 6, -10))
    for sx, s in (("L", 1), ("R", -1)):
        aim(rig, f"thigh.{sx}", (s * 0.08, -1, -0.06))
        aim(rig, f"shin.{sx}", (s * 0.02, 0.1, -1))
        aim(rig, f"foot.{sx}", (s * 0.05, -1, -0.25))
        aim(rig, f"upper_arm.{sx}", (s * 0.28, -0.55, -0.75))
        aim(rig, f"forearm.{sx}", (-s * 0.55, -1, -0.05))
        aim(rig, f"hand.{sx}", (-s * 0.35, -1, -0.12), palm=(0, 0, -1))
        hand(rig, sx, "relax")
    if f is not None:
        key(rig, f)


def tap_glass(rig, f=None, taps=2, every=6):
    """S04a: the right index finger reaches forward and taps the glass `taps` times (one every `every` frames)."""
    reset(rig)
    rot(rig, "spine", (6, 0, 0))
    rot(rig, "chest", (4, 0, 0))
    aim(rig, "upper_arm.R", (-0.25, -0.75, -0.45))
    aim(rig, "forearm.R", (0.12, -1, 0.05))
    aim(rig, "hand.R", (0.05, -1, 0.0), palm=(0.15, 0, -1))
    hand(rig, "R", "point")
    aim(rig, "upper_arm.L", (0.16, 0.02, -1))
    aim(rig, "forearm.L", (0.1, -0.2, -1))
    hand(rig, "L", "relax")
    if f is None:
        return
    key(rig, f)
    for i in range(taps):
        t0 = f + 2 + i * every
        pb = _pb(rig, "hand.R")
        base = pb.rotation_quaternion.copy()
        pb.rotation_quaternion = base @ Quaternion((1, 0, 0), math.radians(-14))   # lift the finger
        pb.keyframe_insert("rotation_quaternion", frame=t0, group=pb.name)
        pb.rotation_quaternion = base @ Quaternion((1, 0, 0), math.radians(8))     # tap
        pb.keyframe_insert("rotation_quaternion", frame=t0 + every // 2, group=pb.name)
        pb.rotation_quaternion = base
        pb.keyframe_insert("rotation_quaternion", frame=t0 + every - 1, group=pb.name)


def reach_pov(rig, f=None):
    """S15: the right arm reaches forward and down from the bottom of a POV camera, palm open and down."""
    reset(rig)
    rot(rig, "spine", (10, 0, 0))
    rot(rig, "chest", (8, 0, 4))
    rot(rig, "head", (22, 0, 0))
    aim(rig, "upper_arm.R", (-0.22, -0.95, -0.42))
    aim(rig, "forearm.R", (-0.04, -1, -0.38))
    aim(rig, "hand.R", (0.0, -1, -0.32), palm=(0.2, -0.3, -1))
    hand(rig, "R", "open")
    aim(rig, "upper_arm.L", (0.2, 0.0, -1))
    aim(rig, "forearm.L", (0.1, -0.25, -1))
    hand(rig, "L", "relax")
    if f is not None:
        key(rig, f)


def thrown_back(rig, f=None):
    """S17: blown off his feet: body arched back, arms and legs flung forward, head whipped."""
    reset(rig)
    move(rig, "hips", (0, 0.12, 0.18))
    rot(rig, "hips", (-38, 0, 0))
    rot(rig, "spine", (-12, 0, 0))
    rot(rig, "chest", (-6, 0, 0))
    rot(rig, "neck", (18, 0, 0))
    rot(rig, "head", (16, 0, 0))
    for sx, s in (("L", 1), ("R", -1)):
        aim(rig, f"upper_arm.{sx}", (s * 0.7, -0.7, 0.45))
        aim(rig, f"forearm.{sx}", (s * 0.35, -0.9, 0.55))
        aim(rig, f"hand.{sx}", (s * 0.2, -0.8, 0.6), palm=(0, -1, 0))
        hand(rig, sx, "claw")
        aim(rig, f"thigh.{sx}", (s * 0.25, -0.85, -0.3))
        aim(rig, f"shin.{sx}", (s * 0.1, -0.2, -1))
        aim(rig, f"foot.{sx}", (s * 0.05, -1, 0.2))
    if f is not None:
        key(rig, f)


def shock(rig, f=None):
    """The held reaction pose (freeze frames): leaning back, shoulders up, hands up and open in front of the chest,
    eyes wide with small irises, mouth "o". Keys the face too."""
    reset(rig)
    rot(rig, "spine", (-8, 0, 0))
    rot(rig, "chest", (-6, 0, 0))
    rot(rig, "neck", (8, 0, 0))
    rot(rig, "head", (-2, 0, 0))
    for sx, s in (("L", 1), ("R", -1)):
        rot(rig, f"shoulder.{sx}", (0, -s * 8, 0))
        aim(rig, f"thigh.{sx}", (s * 0.18, 0.04, -1))
        aim(rig, f"shin.{sx}", (s * 0.12, 0.06, -1))
        aim(rig, f"upper_arm.{sx}", (s * 0.75, -0.25, -0.55))
        aim(rig, f"forearm.{sx}", (-s * 0.2, -0.55, 1))
        aim(rig, f"hand.{sx}", (-s * 0.05, -0.2, 1), palm=(0, -1, 0))
        hand(rig, sx, "open")
    expression(rig, "shock", f)
    if f is not None:
        key(rig, f)


def pov_camera(rig, lens=24, down=18):
    """A POV camera at Kai's eyes, looking forward and `down` degrees down; hides his head for the shot."""
    for o in rig["head_parts"]:
        o.hide_render = True
    bpy.context.view_layer.update()
    M = rig["arm"].matrix_world @ _pb(rig, "head").matrix
    eye = M @ Vector((0, 0.09, -0.07))                    # head-bone space: Y up the head, Z toward the face
    fwd = (M.to_3x3() @ Vector((0, 0, 1))).normalized()
    bpy.ops.object.camera_add(location=eye + fwd * 0.02)
    cam = bpy.context.object
    cam.rotation_mode = "QUATERNION"
    look_dir = (Vector((fwd.x, fwd.y, 0)).normalized() * math.cos(math.radians(down))
                + Vector((0, 0, -math.sin(math.radians(down)))))
    cam.rotation_quaternion = look_dir.to_track_quat("-Z", "Y")
    cam.data.lens = lens
    _bone_parent(cam, rig["arm"], "head")
    return cam


def line_scale(rig, k):
    """Thicker or thinner outlines for this shot (e.g. 0.6 in a face close-up, 1.4 in a wide)."""
    for o in rig["meshes"] + rig["rigid"] + [rig["head"], rig["hair"]]:
        for m in o.modifiers:
            if m.type == "SOLIDIFY" and m.name == "outline":
                if "line0" not in m:
                    m["line0"] = m.thickness
                m.thickness = m["line0"] * k
