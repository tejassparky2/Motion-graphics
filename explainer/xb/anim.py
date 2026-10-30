"""Keyframing helpers for character performance (times in seconds)."""
import math

import bpy
from mathutils import Euler, Quaternion, Vector

from . import posing

FPS = 24


def fr(t):
    return 1 + t * FPS


def key_loc(ob, t, loc):
    ob.location = Vector(loc)
    ob.keyframe_insert('location', frame=fr(t))


def key_rotq(ob, t, q):
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = q
    ob.keyframe_insert('rotation_quaternion', frame=fr(t))


def key_hand(rig, side, target, t, wrist, f, n):
    posing.set_hand(rig, side, target, wrist, f, n)
    target.keyframe_insert('location', frame=fr(t))
    # keep quaternions on the same hemisphere as the previous key so the slerp takes the short way
    q = target.rotation_quaternion.copy()
    prev = target.get('_q_prev')
    if prev is not None and Quaternion(prev).dot(q) < 0:
        q.negate()
        target.rotation_quaternion = q
    target['_q_prev'] = list(q)
    target.keyframe_insert('rotation_quaternion', frame=fr(t))


def key_bone(rig, name, t, rot=None, loc=None):
    b = rig.pose.bones[name]
    if rot is not None:
        b.rotation_mode = 'XYZ'
        b.rotation_euler = rot
        b.keyframe_insert('rotation_euler', frame=fr(t))
    if loc is not None:
        b.location = loc
        b.keyframe_insert('location', frame=fr(t))


def key_fingers(rig, side, t, shape, blend=None, spread=0.0):
    posing.hand_shape(rig, side, shape, spread=spread, blend=blend)
    for bones in posing.FINGERS.values():
        for n in bones:
            rig.pose.bones[n + '.' + side].keyframe_insert('rotation_euler', frame=fr(t))


class Face:
    """Keys ARKit face units on the body and every child mesh that carries the same shape keys."""

    def __init__(self, body, meshes):
        self.meshes = [m for m in meshes if m.type == 'MESH' and m.data.shape_keys]
        self.used = set()
        self.body = body

    def key(self, t, **units):
        self.used.update(units)
        for m in self.meshes:
            kb = m.data.shape_keys.key_blocks
            for name in self.used:
                k = kb.get(name)
                if k is None:
                    continue
                k.value = units.get(name, 0.0)
                k.keyframe_insert('value', frame=fr(t))

    def blink(self, t, dur=0.16, base=None):
        """A quick blink centred on t (eyes return to `base` lids)."""
        base = base or {}
        for m in self.meshes:
            kb = m.data.shape_keys.key_blocks
            for side in ('Left', 'Right'):
                k = kb.get('eyeBlink' + side)
                if k is None:
                    continue
                b = base.get('eyeBlink' + side, 0.0)
                for dt, v in ((-dur / 2, b), (0.0, 1.0), (dur / 2 + 0.03, b)):
                    k.value = v
                    k.keyframe_insert('value', frame=fr(t + dt))


def wiggle(fcurve_owner, path, index, strength, scale, seed):
    """Add a noise modifier to an animated channel (handheld camera, idle sway)."""
    ad = fcurve_owner.animation_data
    if ad is None or ad.action is None:
        return
    for fc in ad.action.fcurves:
        if fc.data_path == path and fc.array_index == index:
            m = fc.modifiers.new('NOISE')
            m.strength = strength
            m.scale = scale
            m.phase = seed
            return m


def set_ease(ob, interp='BEZIER'):
    ad = ob.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = interp
