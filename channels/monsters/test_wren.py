"""Wren (mk/wren.py) test stills: a turnaround next to Kai, and face/bell close-ups.
    blender -b -y -P channels/monsters/test_wren.py -- OUTDIR [turn|face|all]
Writes OUTDIR/wren_turnaround.png (Kai front | Wren front, 3/4, side, back) and OUTDIR/wren_faces.png."""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import hero, look, wren  # noqa: E402
from channels.monsters.ep01v2 import xprl as x3  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
what = argv[1] if len(argv) > 1 else "all"
os.makedirs(out, exist_ok=True)


def scene(W, H):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = look.render_setup(W, H, 8)
    look.world()
    look.sun(elev=40, azim=-30)
    bpy.ops.mesh.primitive_plane_add(size=60)
    bpy.context.object.data.materials.append(look.paint("floor", look.hexc("#cfe3c8"), noise=0.0))
    return sc


def cam(sc, loc, tgt, lens):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    sc.camera = c
    return c


def pose_down(rig, f=1, bell=0.0, shake=0.0):
    P = x3.Pose(rig)
    P.reset()
    wren.hold_bell(P, bell, shake) if "bell" in rig else x3._arms_down(P)
    P.key(f)
    if "bell" in rig:
        wren.grip(rig, f)


if what in ("turn", "all"):
    sc = scene(1800, 900)
    k = hero.load((-1.6, 0, 0))
    pose_down(k)
    for i, rz in enumerate((0, 35, 90, 180)):
        w = wren.load((-0.55 + i * 0.75, 0, 0), rot_z=math.radians(rz))
        pose_down(w)
        wren.face(w, "stern" if i == 1 else "neutral", 1)
    cam(sc, (-0.4, -7.2, 0.82), (-0.4, 0, 0.76), 45)
    sc.render.filepath = os.path.join(out, "wren_turnaround.png")
    bpy.ops.render.render(write_still=True)

if what in ("face", "all"):
    sc = scene(1500, 600)
    for i, (fname, bell) in enumerate((("neutral", 0.0), ("stern", 0.0), ("stern_open", 0.0), ("stern", 1.0))):
        w = wren.load((i * 0.7, 0, 0), rot_z=math.radians(25))
        pose_down(w, bell=bell)
        wren.face(w, fname, 1)
        w["arm"].hide_render = False
    cam(sc, (1.05, -4.4, 1.25), (1.05, 0, 1.2), 50)
    sc.render.filepath = os.path.join(out, "wren_faces.png")
    bpy.ops.render.render(write_still=True)
