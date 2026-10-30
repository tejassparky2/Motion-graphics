"""WIP test renders of Kai (mk/kai.py), paused 30 Oct by the coordinator (v4: new story, no HUD).
    blender -b -P channels/monsters/test_kai.py -- OUTDIR VIEWS [POSE] [OUTFIT] [EXPR]
    VIEWS: comma list of full34, fullfront, fullside, head34, headfront, headside, hand, pov
    env W, H, SAMP (default 360x640, 8 samples)."""
import math, os, sys, time
import bpy
sys.path.insert(0, "/home/user/Motion-graphics")
import importlib
from channels.monsters.mk import look
from channels.monsters.mk import kai
argv = sys.argv[sys.argv.index("--") + 1:]
out, views = argv[0], argv[1].split(",")
pose = argv[2] if len(argv) > 2 else "rest"
outfit = argv[3] if len(argv) > 3 else "world"
expr = argv[4] if len(argv) > 4 else "neutral"
W, H, SAMP = int(os.environ.get("W", 360)), int(os.environ.get("H", 640)), int(os.environ.get("SAMP", 8))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, SAMP)
look.world()
look.sun(elev=38, azim=-30)
bpy.ops.mesh.primitive_plane_add(size=40)
bpy.context.object.data.materials.append(look.paint("floor", look.hexc("#cfe3c8"), noise=0.0))
t = time.time()
rig = kai.build((0, 0, 0), outfit=outfit)
print("BUILD_SECONDS %.1f" % (time.time() - t))
if pose != "rest":
    getattr(kai, pose)(rig, 1)
kai.expression(rig, expr)
CAMS = {   # name: (location, target, lens)
    "full34": ((2.3, -3.6, 1.15), (0, 0, 0.9), 50), "fullfront": ((0, -4.3, 1.0), (0, 0, 0.9), 50),
    "fullside": ((4.3, 0, 1.0), (0, 0, 0.9), 50),
    "head34": ((0.42, -0.62, 1.66), (0, 0, 1.64), 60), "headfront": ((0, -0.75, 1.64), (0, 0, 1.64), 60),
    "headside": ((0.75, 0, 1.64), (0, 0, 1.64), 60), "hand": ((-0.75, -0.55, 1.0), (-0.52, 0, 0.9), 60),
}
for v in views:
    if v == "pov":
        cam = kai.pov_camera(rig)
    else:
        loc, tgt, lens = CAMS[v]
        bpy.ops.object.camera_add(location=loc)
        cam = bpy.context.object
        cam.rotation_mode = "QUATERNION"
        from mathutils import Vector
        cam.rotation_quaternion = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y")
        cam.data.lens = lens
    sc.camera = cam
    sc.render.filepath = os.path.join(out, f"{v}_{pose}_{outfit}_{expr}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %s %.1f" % (v, time.time() - t))
