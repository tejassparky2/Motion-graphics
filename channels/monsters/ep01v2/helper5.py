"""Episode 1 v2 shots by helper 5 (EP01V2_SHOTS.md): the thorn bush and the butcher bird. Every shot carries the
12-frame tail handle.

    S22 "That's when I saw the thorn tree." (2.2 s): reveal by scale (SU2). Close on the larder, tiny shells
        skewered on thorns, then the camera cranes up and back (a vertical move, SG5) to the whole thorn bush towering
        beside the puddle, its big empty thorn near the top. Camera on 1s.
    S23 "A butcher bird hangs its food on thorns." (2.6 s): from the ground beside the puddle (the shrimp's eye
        level), looking up: the bird flaps down onto the top of the bush, settles, then lowers its head and glares
        down at us (SU4, SU5). Cut to the insert (SG10): the one empty thorn, shrimp-sized, a glint on its tip, the
        bird a blur above it. Locked cameras, the bird on 2s, so only even frames render (TP13).

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S22 OUTDIR
"""
import math

import bpy
import numpy as np
from mathutils import Vector

from channels.monsters.mk import anim, butcherbird, look, meadow, thornbush

TAIL = 12
BIRD_SCALE = 1.6


def _frames(seconds):
    return round(seconds * 24) + TAIL


def _target(name, loc):
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    return e


def _cam(name, loc, target, lens, fstop=1.0):
    """A camera that tracks an empty (so its aim can be keyed) and focuses on it."""
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.data.lens = lens
    t = _target(f"{name}_aim", target)
    con = c.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    c.data.dof.use_dof = True
    c.data.dof.focus_object = t
    c.data.dof.aperture_fstop = fstop
    return c, t


def _smooth(t):
    return t * t * (3 - 2 * t)


def _move(obj, f0, f1, a, b):
    """Key obj.location from a to b over f0..f1 with an ease in and out, one key a frame (camera moves on 1s)."""
    for f in range(f0, f1 + 1):
        k = _smooth((f - f0) / (f1 - f0))
        anim.key(obj, "location", f, tuple(a[i] + (b[i] - a[i]) * k for i in range(3)), "LINEAR")


def _glint(loc, cam, f, size=0.16):
    """A 4-point sparkle that pops on the tip of the empty thorn (2s, held between even frames)."""
    pts, n = [], 8
    for i in range(n):
        a = i / n * 2 * math.pi
        r = 1.0 if i % 2 == 0 else 0.22
        pts.append((math.cos(a) * r, math.sin(a) * r, 0))
    me = bpy.data.meshes.new("glint")
    me.from_pydata([(0, 0, 0)] + pts, [], [(0, i + 1, (i + 1) % n + 1) for i in range(n)])
    o = bpy.data.objects.new("glint", me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(look.flat("glint_m", (1, 1, 1, 1), 1.5))
    o.location = loc
    con = o.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = cam, "TRACK_Z", "UP_Y"
    for fr, s in ((f - 2, 0.001), (f, size * 0.5), (f + 2, size), (f + 4, size * 0.7), (f + 6, 0.001)):
        anim.key(o, "scale", fr, s, "CONSTANT")
    return o


def _set():
    meadow.build("before")
    return thornbush.build()


def s22():
    """S22 (2.2 s): close on the shells, hold a beat, then crane up and back to the whole bush (1.6 s), hold."""
    h = _set()
    n = _frames(2.2)
    bx, by, _ = thornbush.BUSH_AT
    shells = np.array(h["shell_spots"])
    near = shells[np.argsort(np.abs(shells[:, 2] - 2.2))[:4]].mean(axis=0)   # the cluster at the shrimp's height
    cam, aim = _cam("cam_s22", (near[0] + 0.25, near[1] - 2.3, near[2] - 0.15), tuple(near), 42, fstop=1.0)
    _move(cam, 8, 44, cam.location, (bx + 0.6, by - 9.4, 2.6))
    _move(aim, 8, 44, near, (bx, by, 4.1))
    bpy.context.scene.camera = cam
    return dict(frames=n, step=1, subject=[])


def s23():
    """S23 (2.6 s): the bird lands on the top of the bush (from below), glares down at us; cut on frame 44 to the
    empty thorn."""
    h = _set()
    n = _frames(2.6)
    perch = Vector(h["perch"])
    eye = Vector((perch.x + 2.6, perch.y - 5.0, 1.4))           # beside the puddle, low, looking up
    rig = butcherbird.build(tuple(perch), scale=BIRD_SCALE)
    to_cam = eye - perch
    rig["root"].rotation_euler = (0, 0, math.atan2(to_cam.x, -to_cam.y))   # it faces us
    butcherbird.land(rig, 20, drop=(0.5, 1.6, 2.8))
    butcherbird.stare(rig, 30, down=0.5, hold=n - 30)
    anim.blink(rig, 26)
    anim.on_twos(butcherbird.objects(rig), step=2)
    sc = bpy.context.scene
    up, _ = _cam("cam_s23_below", tuple(eye), tuple(perch + Vector((0, 0, 1.3))), 32, fstop=1.6)
    base, tip = (Vector(p) for p in h["empty_thorn"])
    mid = (base + tip) / 2
    d = (tip - base).normalized()
    ins, _ = _cam("cam_s23_thorn", tuple(mid + Vector((-0.25, -1.75, -0.2))), tuple(mid + Vector((-0.1, 0, 0.05))),
                  32, fstop=0.9)                               # level with it, in front: the thorn crosses the frame
    _glint(tuple(tip + d * 0.02), ins, 50)
    for f, c in ((1, up), (44, ins)):
        m = sc.timeline_markers.new(f"{c.name}", frame=f)
        m.camera = c
    sc.camera = up
    return dict(frames=n, step=2, subject=[rig["root"]])


SHOTS = {"S22": s22, "S23": s23}
