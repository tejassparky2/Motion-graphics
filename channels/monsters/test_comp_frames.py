"""Frames for the compositor test (channels/monsters/test_comp.py): the test_snap.py scene (the puff-shrimp idles in
its crater, winds up and snaps at frame 44, with Blender's own shockwave, flash, dust and shake), rendered twice:
the normal pass into OUTDIR/ (0001.png ...) and the subject pass (the creature alone on a transparent film,
look.subject_only) into OUTDIR/subject/.
    blender -b -P channels/monsters/test_comp_frames.py -- OUTDIR [W H SAMPLES FIRST LAST]"""
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
F0, F1 = (int(argv[4]), int(argv[5])) if len(argv) > 5 else (1, 72)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = F0, F1
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
os.makedirs(os.path.join(out, "subject"), exist_ok=True)
t = time.time()
sc.render.filepath = os.path.join(out, "")
bpy.ops.render.render(animation=True)
print("RENDER_SECONDS normal %.1f for %d frames" % (time.time() - t, F1 - F0 + 1))
look.subject_only([rig["root"]])
t = time.time()
sc.render.filepath = os.path.join(out, "subject", "")
bpy.ops.render.render(animation=True)
print("RENDER_SECONDS subject %.1f for %d frames" % (time.time() - t, F1 - F0 + 1))
