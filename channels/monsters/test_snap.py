"""3-second animation test: the puff-shrimp idles in its crater, blinks, winds up and snaps (shockwave, flash, dust,
camera shake). Renders PNG frames.
    blender -b -P channels/monsters/test_snap.py -- OUTDIR [W H SAMPLES]"""
import math
import os
import sys
import time

import bpy

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import anim, look, puffshrimp, sets  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (360, 640, 8)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = 1, 72
look.world()
look.sun()
sets.crater_meadow()
rig = puffshrimp.build((0, 0, 0))
rig["shoulder"].rotation_euler = (0, 0.6, 0)
bpy.ops.object.camera_add(location=(-1.0, -12.5, 3.6), rotation=(math.radians(80), 0, math.radians(-4)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 38
cam.data.dof.use_dof = True
cam.data.dof.focus_object = rig["body"]
cam.data.dof.aperture_fstop = 4.0
anim.key(cam, "location", 1, (-1.0, -12.5, 3.6))               # slow push-in
anim.key(cam, "location", 40, (-0.9, -11.0, 3.3))
anim.idle(rig, 1, 72)
SNAP = 44
anim.snap(rig, SNAP)
anim.shockwave((-1.0, -0.4, 0.15), SNAP, frames=10)
anim.flash(cam, SNAP)
anim.dust((-1.6, -0.4, 0.3), SNAP)
anim.shake(cam, SNAP)
os.makedirs(out, exist_ok=True)
sc.render.filepath = os.path.join(out, "f")
t = time.time()
bpy.ops.render.render(animation=True)
print("RENDER_SECONDS %.1f for %d frames" % (time.time() - t, sc.frame_end))
