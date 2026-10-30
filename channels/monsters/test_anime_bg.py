"""Anime background test: painted trees, painted grass, wispy sky, the crater and the puff-shrimp in a closer,
low, eye-level framing with depth of field. blender -b -P channels/monsters/test_anime_bg.py -- OUT.png [W H]"""
import math
import random
import sys
import time

import bpy

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import look, paintbg, puffshrimp, sdf  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H = (int(argv[1]), int(argv[2])) if len(argv) > 2 else (720, 1280)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, 16)
paintbg.sky()
look.sun(elev=45, azim=-30)
bpy.ops.mesh.primitive_plane_add(size=200)
bpy.context.object.data.materials.append(paintbg.grass_material())
# the crater: scorched dirt dish with a raised lip (painted, no lines)
dirt = paintbg.paint3("crater_dirt", look.hexc("#5a3a2a"), look.hexc("#7a5238"), look.hexc("#9c7350"))
lip = paintbg.paint3("crater_lip", look.hexc("#7a5a3a"), look.hexc("#a77f55"), look.hexc("#c9a274"))
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(0, 0.6, -0.02))
o = bpy.context.object
o.scale = (3.6, 3.0, 0.05)
o.data.materials.append(dirt)
bpy.ops.mesh.primitive_torus_add(major_radius=3.6, minor_radius=0.35, location=(0, 0.6, 0))
o = bpy.context.object
o.scale = (1.0, 0.84, 0.5)
o.data.materials.append(lip)
for p in o.data.polygons:
    p.use_smooth = True
rnd = random.Random(2)
# a broken stand of stumps right behind the crater, then the surviving forest wall, then far hills of trees
stump = paintbg.paint3("stump", look.hexc("#4a2f22"), look.hexc("#6e4a33"), look.hexc("#9c7a58"))
for i in range(9):
    a = rnd.uniform(0.2 * math.pi, 0.8 * math.pi)
    r = rnd.uniform(4.6, 7.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=rnd.uniform(0.18, 0.3), depth=rnd.uniform(0.3, 0.7), vertices=12,
                                        location=(math.cos(a) * r, 0.6 + math.sin(a) * r, 0.2))
    bpy.context.object.data.materials.append(stump)
for i in range(14):                                            # forest wall
    x = -16 + i * 2.5 + rnd.uniform(-0.8, 0.8)
    paintbg.tree((x, 14 + rnd.uniform(-1.5, 2.5), 0), height=rnd.uniform(6, 8), radius=rnd.uniform(2.2, 3.0),
                 seed=10 + i, variant=i % 4)
for i in range(12):                                            # far trees, paler and bluer
    x = -30 + i * 5.5 + rnd.uniform(-1.5, 1.5)
    paintbg.tree((x, 34 + rnd.uniform(-3, 3), 0), height=rnd.uniform(8, 11), radius=rnd.uniform(3.2, 4.2),
                 seed=40 + i, variant=i % 4, far=0.45, res=0.2)
look.LINE_SCALE = 1.5                                          # clean ~2-3 px lines on the character
rig = puffshrimp.build((0, 0.4, 0))
rig["shoulder"].rotation_euler = (0, 0.6, 0)
bpy.ops.object.camera_add(location=(0.4, -7.6, 1.5), rotation=(math.radians(86), 0, math.radians(2)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 35
cam.data.dof.use_dof = True
cam.data.dof.focus_object = rig["body"]
cam.data.dof.aperture_fstop = 0.16                             # anime-strength background blur
sc.render.filepath = out
t = time.time()
bpy.ops.render.render(write_still=True)
print("RENDER_SECONDS %.1f" % (time.time() - t))
