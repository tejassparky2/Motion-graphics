"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 1's shots:

    S08a  "And I was standing in it."  The night lab, close and low from the open (east) side: Kai has swivelled his
          chair toward the cracked tank, sneakers flat on the tiles. The spill from S08 slides in from the tank side
          and runs under his sneakers (ripples ring out from each shoe as it arrives); he glances down, a small lift
          first, then his head drops to his feet, and his face drops with it (fear). The camera rises on 1s from his
          sneakers to his face.
    S24bot  "Option B: run while I can."  See s24bot().

Frame counts come from ep01v3/timing.json (render_frames = frames + 12).
    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08a OUT [--frames A-B] [--still N --scale 0.5]
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper1 as d1
from channels.monsters.ep01v2 import helper1 as h3d
from channels.monsters.mk import acting, anim, diorama, hero, lab, look

BLUR = 10.0
GUESS = {"S08a": 54, "S24bot": 156}          # until ep01v3/timing.json lands


def _frames(shot):
    try:
        from channels.monsters.diorama_v3.shots import v3_frames
        return v3_frames(shot)
    except (OSError, KeyError):
        return GUESS[shot]


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _move(cam, f0, f1, path, n):
    """Key `cam` on every frame 1..n along `path(u)` -> (target, dist, tilt, yaw), u eased from f0 to f1: the slow
    1s move (DOF focus and the miniature f-stop follow the distance)."""
    for f in range(1, n + 1):
        t, dist, tilt, yaw = path(_ease((f - f0) / max(1, f1 - f0)))
        t = Vector(t)
        el, az = math.radians(tilt), math.radians(yaw)
        cam.location = t + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.dof.focus_distance = dist
        cam.data.dof.aperture_fstop = diorama.fstop_for(dist, cam.data.lens, BLUR)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)


def _bone_world(rig, name, tail=False):
    pb = rig["bone"](name)
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _disc(name, center, rad, mat, z, rnd, verts=22):
    vs = [(math.cos(k / verts * 2 * math.pi) * rad * rnd.uniform(0.84, 1.1),
           math.sin(k / verts * 2 * math.pi) * rad * rnd.uniform(0.84, 1.1), 0) for k in range(verts)]
    return lab._mesh(name, vs, [tuple(range(verts))], mat, (center[0], center[1], z))


def _spill_front(a, b, f0, f1, width=0.9, seed=8):
    """The water's front sliding from `a` to `b` (floor points) between f0 and f1: overlapping discs that swell into
    place one after another, each with a pale rim a touch larger under it (the meniscus catching the tank light)."""
    water = lab._water_floor()
    rim = look.flat("s08a_rim", look.hexc("#9fe2fb"), strength=1.2)
    rnd = random.Random(seed)
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    side = Vector((-(b - a).y, (b - a).x, 0)).normalized()
    k = 16
    for i in range(k):
        u = i / (k - 1)
        p = a.lerp(b, u) + side * 0.35 * math.sin(u * 5.0) * width
        rad = width * (0.75 + 0.35 * math.sin(u * math.pi)) * rnd.uniform(0.9, 1.1)
        ts = f0 + (f1 - f0) * u
        for nm, mat, r, z in (("w", water, rad, 0.032), ("r", rim, rad * 1.04, 0.031)):
            d = _disc(f"s08a_{nm}{i}", p, r, mat, z + i * 0.0001, random.Random(seed * 100 + i))
            d.visible_shadow = False
            anim.key(d, "scale", ts - 1, (0.001, 0.001, 1), "CONSTANT")
            anim.key(d, "scale", ts + 2, (1.12, 1.12, 1))                  # overshoot as it lands...
            anim.key(d, "scale", ts + 5, (1.0, 1.0, 1))                    # ...and settles


def _ripples(at, f0, n, rings=3):
    """Thin rings spreading from a sneaker when the water reaches it (on 2s, fading by shrinking their alpha)."""
    for j in range(rings):
        m = look.fade(f"s08a_rip_m{j}", look.hexc("#e6fbff"), 0.0)
        mix = m.node_tree.nodes["Mix"].inputs[0]
        vs, faces = [], []
        seg = 28
        for k in range(seg):
            a = k / seg * 2 * math.pi
            for r in (1.0, 1.08):
                vs.append((math.cos(a) * r, math.sin(a) * r, 0))
        for k in range(seg):
            i0, i1 = 2 * k, 2 * ((k + 1) % seg)
            faces.append((i0, i1, i1 + 1, i0 + 1))
        ring = lab._mesh(f"s08a_rip{j}", vs, faces, m, (at[0], at[1], 0.045))
        ring.visible_shadow = False
        s = f0 + j * 6
        anim.key(ring, "scale", s - 1, (0.2, 0.2, 1), "CONSTANT")
        anim.key(ring, "scale", s + 16, (1.5, 1.5, 1))
        lab._ksock(mix, s - 1, 0.0, "CONSTANT")
        lab._ksock(mix, s, 0.75, "LINEAR")
        lab._ksock(mix, s + 16, 0.0, "LINEAR")


def _smooth_water(n):
    """The shared spill material (lab._water_floor) restyled for a close shot: broader, softer ripples (its fine
    speckle reads as gravel this close) that shimmer on 2s (4D noise, W keyed)."""
    m = lab._water_floor()
    nz = next(x for x in m.node_tree.nodes if x.type == "TEX_NOISE")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 2.4
    nz.inputs["Detail"].default_value = 1.0
    w = nz.inputs["W"]
    for f in range(1, n + 2, 2):
        w.default_value = f * 0.035
        w.keyframe_insert("default_value", frame=f)
    for fc in anim.all_fcurves(m.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return m


def s08a():
    R, rig = d1._stage()
    n = _frames("S08a")
    # he has swivelled his chair right round, away from the desk, toward the open front of the dollhouse (south):
    # feet flat on the tiles in front of him, his face to the lens; the spill comes from the desk behind him
    turn = 2.75
    d1._tilt_cap(rig, 36.0)
    rig["arm"].rotation_euler.z = math.pi - turn
    R["desk"]["chair"].rotation_euler.z = -turn
    bpy.context.view_layer.update()
    k = h3d._key_pose
    h3d._sit(rig, lean=0.02, look=(-0.35, -0.12))                  # looking back over his shoulder at the tank
    k(rig, 1, h3d.BODY)
    k(rig, 10, h3d.BODY)
    h3d._sit(rig, lean=-0.02, look=(-0.2, -0.25))                  # anticipation: a small lift as he hears it
    k(rig, 14, h3d.BODY)
    h3d._sit(rig, lean=0.16, look=(0.0, 0.12))                     # head dips to his sneakers (overshoot)...
    k(rig, 20, h3d.BODY)
    h3d._sit(rig, lean=0.12, look=(0.0, -0.02))                    # ...and settles, eyes doing the rest
    k(rig, 24, h3d.BODY)
    h3d._sit(rig, lean=0.14, look=(0.03, 0.0))
    k(rig, n, h3d.BODY)
    sc = bpy.context.scene
    sc.frame_set(1)
    feet = [_bone_world(rig, f"{s}_foot", tail=True) for s in ("left", "right")]
    mid = (feet[0] + feet[1]) / 2
    sc.frame_set(24)
    head = h3d._head_pos(rig)
    sc.frame_set(1)
    # the S08 spill is already on the tiles (desk to the power strip); its front now slides under the chair to his
    # sneakers and on past them
    R["puddle"](-60, -12)
    _smooth_water(n)
    a = Vector((R["tank"]["leak"][0] - 1.2, R["desk"]["front_y"] - 0.5, 0))
    beyond = mid + (mid - a).normalized() * 1.6
    _spill_front(a, beyond, 2, 15)
    for i, ft in enumerate(feet):
        _ripples(ft, 11 + i * 2, n)
    # face (mk/acting): a blank look back at the tank, a blink, then his eyes drop to his shoes (with small darts)
    # and the face drops with them: surprised, then fear
    acting.expression(rig, "neutral", 1)
    acting.expression(rig, "surprised", 19, value=0.8)
    acting.expression(rig, "fear", 25)
    acting.look_at(rig, R["tank"]["center"], 1, 12)
    acting.look_at(rig, tuple(mid), 15, n)
    acting.blink(rig, 1, n, at=(7,))
    hero.line_width(rig, 0.0028)
    # from the open front, low: the camera rises on 1s from his sneakers in the water to his face
    face = head + Vector((0.0, 0.0, -0.4))
    cam = R["cam"]("cam_s08a", tuple(mid), dist=27.0, tilt=42.0, yaw=-18.0, lens=100.0, blur=BLUR)

    def path(u):
        return mid.lerp(face, 0.08 + 0.7 * u), 27.0 - 4.0 * u, 42.0 - 1.0 * u, -18.0 - 4.0 * u

    _move(cam, 1, n - 6, path, n)
    _light_face = h3d._tank_glow(side=Vector((0.6, 0.8, 0.0)))
    h3d._tint_hero(0.1)
    R["flicker"]([30, 33])                                         # the lights stutter: the plugs are fizzing
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["arm"]] + list(rig.get("cap", [])))


SHOTS = {"S08a": s08a}
