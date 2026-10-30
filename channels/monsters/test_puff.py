"""Still test of the puff-shrimp v2 (sculpted) in the crater meadow.
    blender -b -P channels/monsters/test_puff.py -- OUT.png"""
import math
import sys
import time

import bpy

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import look, puffshrimp, sets  # noqa: E402

out = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(360, 640, 8)
look.world()
look.sun()
sets.crater_meadow()
rig = puffshrimp.build((0, 0, 0))
import os
rig["shoulder"].rotation_euler = (float(os.environ.get("SHX", "0")), float(os.environ.get("SHY", "0")), 0)
bpy.ops.object.camera_add(location=(-1.0, -12.5, 3.6), rotation=(math.radians(80), 0, math.radians(-4)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 38
cam.data.dof.use_dof = True
cam.data.dof.focus_object = rig["body"]
cam.data.dof.aperture_fstop = 4.0
sc.render.filepath = out
t = time.time()
bpy.ops.render.render(write_still=True)
print("RENDER_SECONDS %.1f" % (time.time() - t))
