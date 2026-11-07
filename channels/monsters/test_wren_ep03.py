"""Wren's Episode 3 poses and faces (mk/wren.py), as test sheets for the other helpers who stage her:
    blender -b -y -P channels/monsters/test_wren_ep03.py -- OUTDIR [poses|faces|all]
Writes OUTDIR/wren_ep03_poses.png (standing, shield S07, ring hard S08, lowering the bell S16, kneel S17, whisper and
point S18, sitting in a boat S19 top) and OUTDIR/wren_ep03_faces.png (stern, shout, shocked, softening, worried,
whisper)."""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import look, wren  # noqa: E402
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
    bpy.ops.mesh.primitive_plane_add(size=80)
    bpy.context.object.data.materials.append(look.paint("floor", look.hexc("#cfe3c8"), noise=0.0))
    return sc


def cam(sc, loc, tgt, lens):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    sc.camera = c
    return c


def thwart(x, seat):
    """A plain plank seat for the boat pose."""
    bpy.ops.mesh.primitive_cube_add(location=(x, 0.06, seat / 2))
    o = bpy.context.object
    o.scale = (0.32, 0.14, seat / 2)
    o.data.materials.append(look.paint("plank", look.hexc("#8a5a3a"), noise=0.0))


POSES = [
    ("standing", None),
    ("shield (S07)", lambda P, w: (wren.shield(P, 1.0), wren.cape_up(w, 1))),
    ("ring hard (S08)", lambda P, w: wren.ring_hard(P, 1, 1.0)),
    ("lower bell (S16)", lambda P, w: wren.lower_bell(P, 0.45)),
    ("kneel (S17)", lambda P, w: wren.kneel(P)),
    ("whisper (S18)", lambda P, w: (wren.kneel(P), wren.whisper(P, 1.0, toward=(-1, -0.4, 0)))),
    ("point (S18)", lambda P, w: (wren.kneel(P), wren.point(P, (0.6, -1, 0.25)))),
    ("sit, boat (S19)", lambda P, w: wren.sit(P)),
]
FACE_OF = {"standing": "stern", "shield (S07)": "shocked", "ring hard (S08)": "shout", "lower bell (S16)": "softening",
           "kneel (S17)": "worried", "whisper (S18)": "whisper", "point (S18)": "worried", "sit, boat (S19)": "worried"}

if what in ("poses", "all"):
    sc = scene(2400, 700)
    gap = 0.78
    for i, (name, fn) in enumerate(POSES):
        x = (i - (len(POSES) - 1) / 2) * gap
        if name.startswith("sit"):
            thwart(x, 0.42)
        w = wren.load((x, 0, 0), rot_z=math.radians(28))
        P = x3.Pose(w)
        P.reset()
        if fn is None:
            wren.hold_bell(P, 0.25)
        else:
            fn(P, w)
        P.key(1)
        wren.grip(w, 1)
        if "point" in name:
            wren.point_fingers(w, 1)
        if "ring" in name:
            wren.grip(w, 1, side="L")
        wren.face(w, FACE_OF[name], 1)
    cam(sc, (0, -8.6, 0.95), (0, 0, 0.72), 44)
    sc.frame_set(1)
    sc.render.filepath = os.path.join(out, "wren_ep03_poses.png")
    bpy.ops.render.render(write_still=True)

if what in ("faces", "all"):
    sc = scene(1800, 500)
    names = ["stern", "shout", "shocked", "softening", "worried", "whisper"]
    for i, fname in enumerate(names):
        w = wren.load((i * 0.5, 0, 0), rot_z=math.radians(18))
        P = x3.Pose(w)
        P.reset()
        wren.hold_bell(P, 0.0)
        P.key(1)
        wren.face(w, fname, 1)
    cam(sc, (1.25, -4.2, 1.33), (1.25, 0, 1.3), 48)
    sc.frame_set(1)
    sc.render.filepath = os.path.join(out, "wren_ep03_faces.png")
    bpy.ops.render.render(write_still=True)
