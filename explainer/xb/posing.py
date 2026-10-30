"""Posing helpers for MPFB 'default' rigs: IK arms driven by empties, finger curls, expressions."""
import math

import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

FINGERS = {  # MPFB naming: finger1 = thumb ... finger5 = pinky
    'thumb': ['finger1-1', 'finger1-2', 'finger1-3'],
    'index': ['finger2-1', 'finger2-2', 'finger2-3'],
    'middle': ['finger3-1', 'finger3-2', 'finger3-3'],
    'ring': ['finger4-1', 'finger4-2', 'finger4-3'],
    'pinky': ['finger5-1', 'finger5-2', 'finger5-3'],
}


def empty(name, loc, coll, size=0.03, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = size
    e.empty_display_type = 'ARROWS'
    coll.objects.link(e)
    e.location = loc
    if parent:
        e.parent = parent
    return e


def setup_arm_ik(rig, side, coll):
    """IK from upperarm01 to lowerarm02 with a hand target that also sets the wrist rotation."""
    s = '.' + side
    pb = rig.pose.bones
    M = rig.matrix_world
    wrist = rig.data.bones['wrist' + s]
    tgt = empty('HandTarget' + s, M @ wrist.head_local, coll)
    tgt.rotation_mode = 'QUATERNION'
    tgt.rotation_quaternion = (M @ wrist.matrix_local).to_quaternion()
    elbow = M @ rig.data.bones['lowerarm01' + s].head_local
    pole = empty('ElbowPole' + s, elbow + Vector((0.0, 0.35, -0.1)), coll)
    ik = pb['lowerarm02' + s].constraints.new('IK')
    ik.target = tgt
    ik.pole_target = pole
    ik.chain_count = 4
    ik.use_tail = True           # lowerarm tail (= wrist joint) goes to the target
    ik.pole_angle = _pole_angle(rig, 'upperarm02' + s, pole.location)
    cr = pb['wrist' + s].constraints.new('COPY_ROTATION')
    cr.target = tgt
    for n in ('upperarm01', 'upperarm02', 'lowerarm01', 'lowerarm02'):
        b = pb[n + s]
        b.ik_stretch = 0.0
    return tgt, pole


def _pole_angle(rig, bone_name, pole_loc):
    """Angle that keeps the rest pose unchanged when the pole sits at pole_loc."""
    b = rig.data.bones[bone_name]
    M = rig.matrix_world @ b.matrix_local
    x = M.to_3x3().col[0].normalized()
    y = M.to_3x3().col[1].normalized()
    p = Vector(pole_loc) - M.translation
    p = (p - p.dot(y) * y).normalized()
    ang = x.angle(p)
    if x.cross(p).dot(y) < 0:
        ang = -ang
    return -ang


def curl(rig, side, finger, amounts, spread=0.0, axis='X'):
    """Rotate a finger's three bones about their local flexion axis (radians)."""
    pb = rig.pose.bones
    for i, n in enumerate(FINGERS[finger]):
        b = pb[n + '.' + side]
        b.rotation_mode = 'XYZ'
        r = [0.0, 0.0, 0.0]
        r['XYZ'.index(axis)] = amounts[i]
        if i == 0:
            r[2] += spread
        b.rotation_euler = r


def hand_frame(rig, side):
    """Rest-pose (finger direction, palm normal) of a hand in world space."""
    s = '.' + side
    M = rig.matrix_world
    b = rig.data.bones
    f = (M @ b['metacarpal2' + s].tail_local - M @ b['metacarpal2' + s].head_local).normalized()
    lat = (M @ b['metacarpal1' + s].tail_local - M @ b['metacarpal4' + s].tail_local).normalized()
    n = lat.cross(f) if side == 'R' else f.cross(lat)
    n = (n - n.dot(f) * f).normalized()
    return f, n


def _basis(f, n):
    f = Vector(f).normalized()
    n = Vector(n)
    n = (n - n.dot(f) * f).normalized()
    return Matrix((f, n, f.cross(n))).transposed()


def hand_target_rotation(rig, side, f, n):
    """World rotation for the wrist so the hand's fingers point along f with the palm facing n."""
    f0, n0 = hand_frame(rig, side)
    R = _basis(f, n) @ _basis(f0, n0).transposed()
    rest = (rig.matrix_world @ rig.data.bones['wrist.' + side].matrix_local).to_3x3()
    return (R @ rest).to_quaternion()


def set_hand(rig, side, target, wrist, f, n):
    """Place the IK target so the wrist joint sits at `wrist` and the hand faces (f, n)."""
    target.location = Vector(wrist)
    target.rotation_quaternion = hand_target_rotation(rig, side, f, n)


HAND_SHAPES = {
    'relaxed': dict(thumb=(0.15, 0.2, 0.15), index=(0.15, 0.25, 0.15), middle=(0.2, 0.3, 0.2),
                    ring=(0.25, 0.35, 0.2), pinky=(0.3, 0.4, 0.25)),
    'fist': dict(thumb=(0.45, 0.5, 0.5), index=(1.45, 1.6, 1.0), middle=(1.5, 1.65, 1.0),
                 ring=(1.55, 1.65, 1.0), pinky=(1.6, 1.6, 1.0)),
    'tight': dict(thumb=(0.5, 0.55, 0.55), index=(1.65, 1.7, 1.05), middle=(1.7, 1.75, 1.05),
                  ring=(1.72, 1.75, 1.05), pinky=(1.75, 1.7, 1.05)),
    'cup': dict(thumb=(0.1, 0.2, 0.2), index=(0.55, 0.6, 0.4), middle=(0.6, 0.65, 0.4),
                ring=(0.65, 0.7, 0.45), pinky=(0.7, 0.7, 0.45)),
    'flat': dict(thumb=(0.0, 0.05, 0.05), index=(0.05, 0.05, 0.05), middle=(0.05, 0.05, 0.05),
                 ring=(0.05, 0.05, 0.05), pinky=(0.05, 0.05, 0.05)),
    'spread': dict(thumb=(-0.1, 0.0, 0.0), index=(0.0, 0.05, 0.05), middle=(0.0, 0.05, 0.05),
                   ring=(0.0, 0.05, 0.05), pinky=(0.0, 0.05, 0.05)),
}
SPREAD = {'index': 0.12, 'middle': 0.0, 'ring': -0.1, 'pinky': -0.22, 'thumb': 0.0}


def hand_shape(rig, side, shape, spread=0.0, blend=None):
    """Pose all fingers to a named shape; `blend` = (other_shape, t) mixes two shapes."""
    a = HAND_SHAPES[shape]
    for finger, bones in FINGERS.items():
        amt = list(a[finger])
        if blend:
            b = HAND_SHAPES[blend[0]][finger]
            amt = [x + (y - x) * blend[1] for x, y in zip(amt, b)]
        sp = SPREAD[finger] * spread * (-1 if side == 'R' else 1)
        curl(rig, side, finger, amt, spread=sp)


def fist_in_palm(wR, fR, nR, fL_hint=(-1.0, 0.0, -0.25), press=0.027):
    """Right fist at wR (fingers along fR, palm facing nR) with the left palm cupped over its knuckles.

    press is the gap from the knuckle line to the left hand's bones (0.027 = touching)."""
    fR = Vector(fR).normalized()
    nR = Vector(nR)
    nR = (nR - nR.dot(fR) * fR).normalized()
    knuckles = Vector(wR) + 0.09 * fR
    nL = -fR
    fL = Vector(fL_hint)
    fL = (fL - fL.dot(nL) * nL).normalized()
    wL = knuckles + press * fR - 0.05 * fL
    return (Vector(wR), fR, nR), (wL, fL, nL)


def add_eye_tracking(rig, coll, loc):
    """Both eyes aim at an empty (keyframe it to direct the gaze)."""
    look = empty('LookAt', loc, coll, size=0.05)
    for s in ('L', 'R'):
        c = rig.pose.bones['eye.' + s].constraints.new('DAMPED_TRACK')
        c.target = look
        c.track_axis = 'TRACK_Y'
    return look
