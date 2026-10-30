"""Hero test stills: 3/4 view with three expressions and a front view, on the painted meadow.
    channels/monsters/setup_vrm.sh  (once)
    BLENDER_USER_SCRIPTS=/home/user/tools/blender_scripts blender -b -y -P channels/monsters/test_hero.py -- OUTDIR [W H]"""
import math
import os
import sys
import time

import bpy

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import hero, look, paintbg  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H = (int(argv[1]), int(argv[2])) if len(argv) > 2 else (720, 1280)
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, 16)
paintbg.sky()
look.sun(elev=45, azim=-30)
bpy.ops.mesh.primitive_plane_add(size=200)
bpy.context.object.data.materials.append(paintbg.grass_material())
rnd = __import__("random").Random(3)
for i in range(9):
    paintbg.tree((-14 + i * 3.5 + rnd.uniform(-1, 1), 12 + rnd.uniform(-2, 2), 0), height=rnd.uniform(6, 8),
                 radius=rnd.uniform(2.2, 2.8), seed=60 + i, variant=i % 4)
rig = hero.build((0, 0, 0), rot_z=math.radians(-25))
arm = rig["arm"]
for side, s in (("left", 1), ("right", -1)):                  # arms down from the T-pose
    b = rig["bone"](f"{side}_upper_arm")
    b.rotation_mode = "XYZ"
    b.rotation_euler = (0, 0, s * math.radians(-68))
bpy.context.view_layer.update()
head_z = (arm.matrix_world @ rig["bone"]("head").head).z
shots = [("34_neutral", "neutral", (0.55, -2.2, head_z - 0.35), 45),
         ("34_surprised", "surprised", (0.55, -2.2, head_z - 0.35), 45),
         ("34_happy", "happy", (0.55, -2.2, head_z - 0.35), 45),
         ("face_angry", "angry", (0.25, -0.95, head_z + 0.02), 55)]
for tag, ex, loc, lens in shots:
    for n in ("neutral", "surprised", "happy", "angry"):
        getattr(rig["expr"], n).preview = 1.0 if n == ex else 0.0
    if "cam" in dir():
        bpy.data.objects.remove(cam, do_unlink=True)  # noqa: F821
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    tgt = (0, 0, head_z - (0.25 if lens == 45 else 0.0))
    d = [tgt[i] - loc[i] for i in range(3)]
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = math.dist(loc, tgt)
    cam.data.dof.aperture_fstop = 0.4 if lens == 45 else 2.8
    sc.camera = cam
    sc.render.filepath = os.path.join(out, f"hero_{tag}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER", tag, round(time.time() - t, 1), "s", flush=True)
