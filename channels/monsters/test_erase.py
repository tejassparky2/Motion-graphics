"""Forest-erase test (shot S17, 1.5 s): a stand of painted trees behind the crater is erased by a snap from the
claw (streak, flash, shockwave ring; the trees squash, pop into dust and leaf bits, leave stumps) over 36 frames, seen
from a low camera with anime-strength background blur. Renders 4 key stills.
    blender -b -P channels/monsters/test_erase.py -- OUTDIR [W H SAMPLES] [--all]
--all renders every frame to OUTDIR/erase_fNNN.png instead (for checking motion; don't commit those)."""
import os
import random
import sys
import time

import bpy

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import anim, erase, look, paintbg  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
every = "--all" in argv
argv = [a for a in argv if a != "--all"]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280, 16)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = 1, 36
paintbg.sky()
look.sun(elev=45, azim=-30)
bpy.ops.mesh.primitive_plane_add(size=200)
bpy.context.object.data.materials.append(paintbg.grass_material())
# the crater (as in test_anime_bg.py): scorched dirt dish with a raised lip
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
# the grove that gets erased (paintbg.tree() pairs, as the shot places them), the surviving forest wall, far trees
trees = erase.grove()
rnd = random.Random(2)
for i in range(12):
    x = -18 + i * 3.4 + rnd.uniform(-0.8, 0.8)
    paintbg.tree((x, 27 + rnd.uniform(-1.5, 2.5), 0), height=rnd.uniform(6, 8), radius=rnd.uniform(2.2, 3.0),
                 seed=10 + i, variant=i % 4)
for i in range(10):
    x = -30 + i * 6.5 + rnd.uniform(-1.5, 1.5)
    paintbg.tree((x, 48 + rnd.uniform(-3, 3), 0), height=rnd.uniform(8, 11), radius=rnd.uniform(3.2, 4.2),
                 seed=40 + i, variant=i % 4, far=0.45, res=0.2)

target = erase._empty("cam_target", (0.4, 8.0, 3.6))
bpy.ops.object.camera_add(location=(-5.5, -5.5, 1.0))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 28
tt = cam.constraints.new("TRACK_TO")
tt.target = target
tt.track_axis, tt.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
cam.data.dof.use_dof = True
cam.data.dof.focus_object = target
cam.data.dof.aperture_fstop = 0.15                            # anime-strength background blur

SNAP = 3                                                       # S17 starts right after the snap shot (S16)
fx = erase.erase_trees(trees, origin=(-1.7, 0.2, 2.2), f0=SNAP, cam=cam)      # origin: the claw
anim.shake(cam, SNAP + 4, frames=10, amp=0.08)                 # "wide, then shake": the wave reaches the camera
print("POP_FRAMES", sorted(fx["pop_frames"]), "END", fx["end"])

os.makedirs(out, exist_ok=True)
stills = {SNAP - 1: "erase_1_before", SNAP + 2: "erase_2_snap", SNAP + 8: "erase_3_burst", 36: "erase_4_after"}
frames = range(1, 37) if every else sorted(stills)
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(out, f"erase_f{f:03d}.png" if every else stills[f] + ".png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("FRAME %d RENDER_SECONDS %.1f" % (f, time.time() - t))
