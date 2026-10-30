"""Stills of the Earth LAB set (mk/lab.py), with helper 2's tank (pistolshrimp.tank) in the desk slot and Kai's chair
left empty: the wide establishing shot, the over-the-shoulder desk shot, the S03 medium (Kai's seat between the
glowing tanks), the S07 window during a lightning strike, the S09 low floor shot of the water reaching the power
strip, and the S10 spark.
    blender -b -P channels/monsters/test_lab.py -- OUT_DIR [PREVIEW]
Writes OUT_DIR/lab_wide.png, lab_desk.png, lab_medium.png, lab_window_lightning.png, lab_floor.png,
lab_floor_spark.png (720x1280, 16 samples; PREVIEW=1 renders 360x640 at 8 samples)."""
import os
import sys
import time

import bpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters.mk import lab, look, pistolshrimp  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
preview = len(args) > 1 and args[1] == "1"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(360, 640, 8) if preview else look.render_setup()
t = time.time()
L = lab.build()
tank = L["place_tank"](pistolshrimp.tank())     # helper 2's tank in the desk slot
pistolshrimp.crack(tank, 60)
L["lightning"](30)
L["flicker"]([40, 43, 47, 52])
L["crack_puddle"](60, 100)
L["spark"](104)
print("BUILD_SECONDS %.1f" % (time.time() - t))

shots = [("lab_wide", "wide", 12), ("lab_desk", "desk", 12), ("lab_medium", "medium", 12),
         ("lab_window_lightning", "window", 30), ("lab_floor", "floor", 101), ("lab_floor_spark", "floor", 104)]
os.makedirs(out, exist_ok=True)
for name, cam, frame in shots:
    sc.camera = L["cams"][cam]
    sc.frame_set(frame)
    sc.render.filepath = os.path.join(out, name + ".png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %s %.1f" % (name, time.time() - t))
