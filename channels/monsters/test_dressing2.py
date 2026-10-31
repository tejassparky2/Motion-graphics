"""Before/after stills of the v3 set dressing (DIORAMA_EP01_V3.md, Q2): the island (wide, path, meadow) and the lab
dollhouse, with dressing=1 (v2) or dressing=2 (v3).
    blender -b -y -P channels/monsters/test_dressing2.py -- OUTDIR island|lab DRESSING [SCALE]"""
import os
import sys

import bpy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import diorama, diorama_lab  # noqa: E402

out, what, level = sys.argv[sys.argv.index("--") + 1:][:3]
scale = float(sys.argv[-1]) if len(sys.argv[sys.argv.index("--") + 1:]) > 3 else 0.5
level = int(level)
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = int(720 * scale), int(1280 * scale)
diorama.setup()
if what == "island":
    diorama.island(seed=31, dressing=level)
    views = [("wide", (0, 0, 0), dict(dist=190, tilt=62, lens=100, blur=12)),
             ("path", (-2.0, -55.0, 0), dict(dist=110, tilt=58, lens=100, blur=12)),
             ("meadow", (6.0, -132.0, 0), dict(dist=90, tilt=55, lens=100, blur=12))]
else:
    R = diorama_lab.room(dressing=level)
    views = [("lab", R["desk"]["center"], dict(diorama_lab.LAB_CAM))]
for i, (name, target, kw) in enumerate(views):
    for m in list(sc.timeline_markers):                      # camera() binds each new camera to frame 1 with a marker
        sc.timeline_markers.remove(m)
    cam = diorama.camera(f"cam_{name}", target, frame=1, **kw)
    sc.camera = cam
    sc.render.filepath = os.path.join(out, f"{name}_d{level}.png")
    bpy.ops.render.render(write_still=True)
    print("STILL", sc.render.filepath, flush=True)
