"""Still test of the jelly-snail on a painted grass patch: three-quarter view, front close-up, and a wide shot of its
burned, smoking trail.
    blender -b -P channels/monsters/test_jellysnail.py -- OUTDIR [W H SAMPLES]
writes OUTDIR/jellysnail_threequarter.png, jellysnail_front.png, jellysnail_grass.png.
    blender -b -P channels/monsters/test_jellysnail.py -- OUTDIR W H SAMPLES anim
renders the idle (frames 1-48, every 2nd) from the three-quarter camera instead, as OUTDIR/anim_####.png."""
import math
import os
import random
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import jellysnail, look  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280, 16)
ANIM = len(argv) > 4 and argv[4] == "anim"
STILL_FRAME = 9


def grass_set(trail, seed=11):
    """A plain painted meadow: grass ground, tufts and flowers (none where the trail has burned or slimed the grass),
    distant trees fading paler, and big clouds."""
    hx = look.hexc
    P = look.paint
    grass = P("grass", hx("#79c95f"), noise=0.12, scale=1.2)
    trunk = P("trunk", hx("#8a5a3b"))
    tufts = [P("tuft0", hx("#5fbf55")), P("tuft1", hx("#8edc72"))]
    flowers = [P("fl0", hx("#ffe066")), P("fl1", hx("#ff8fb1")), P("fl2", hx("#ffffff"))]
    leaves = [P("leaf0", hx("#4fb35a")), P("leaf1", hx("#ffb347")), P("leaf2", hx("#ff8fa3")), P("leaf3", hx("#3f9e6a"))]
    far_leaves = [P("fleaf0", hx("#7fc79a")), P("fleaf1", hx("#ffc985")), P("fleaf2", hx("#ffb3c1")),
                  P("fleaf3", hx("#79b8a0"))]
    cloud = P("cloud", hx("#e9f3ff"), top=hx("#ffffff"), noise=0.0)
    bpy.ops.mesh.primitive_plane_add(size=160)
    bpy.context.object.data.materials.append(grass)
    rnd = random.Random(seed)

    def clear(x, y):
        if (x / 0.95) ** 2 + ((y - 0.15) / 1.75) ** 2 < 1:            # under the snail
            return False
        if any((x - hx_) ** 2 + (y - hy) ** 2 < (2.1 * r) ** 2 for hx_, hy, r in trail["holes"]):
            return False
        return all((x - px) ** 2 + (y - py) ** 2 > 0.5 ** 2 for px, py in trail["path"])

    def sphere(name, loc, scale, mat, seg=16):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc)
        o = bpy.context.object
        o.name = name
        o.scale = scale
        o.data.materials.append(mat)
        for p in o.data.polygons:
            p.use_smooth = True
        return o

    for i in range(420):
        x, y = rnd.uniform(-7, 7), rnd.uniform(-6, 12)
        if not clear(x, y):
            continue
        if rnd.random() < 0.8:
            bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.1, depth=0.3, location=(x, y, 0.15))
            bpy.context.object.data.materials.append(rnd.choice(tufts))
        else:
            sphere(f"fl{i}", (x, y, 0.1), (0.09, 0.09, 0.05), rnd.choice(flowers), 10)
    for i in range(60):
        x, y, s = rnd.uniform(-22, 22), rnd.uniform(12, 40), rnd.uniform(1.1, 2.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * s, depth=1.2 * s, location=(x, y, 0.6 * s), vertices=10)
        bpy.context.object.data.materials.append(trunk)
        sphere(f"tree{i}", (x, y, 1.9 * s), (1.1 * s, 1.1 * s, s), rnd.choice(far_leaves if y > 26 else leaves), 20)
    for i in range(7):
        cx, cz = rnd.uniform(-60, 60), rnd.uniform(18, 34)
        for j in range(6):
            r = rnd.uniform(4, 8)
            sphere(f"cloud{i}_{j}", (cx + rnd.uniform(-9, 9), 110 + rnd.uniform(-5, 5), cz + rnd.uniform(-2, 4)),
                   (r * 1.4, r, r), cloud, 20)


def camera(name, loc, target, lens):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    return cam


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = 1, 48
look.world()
look.sun(elev=42, azim=-30)
rig = jellysnail.build((0, 0, 0))
grass_set(rig["trail"])
jellysnail.idle(rig, 1, 120)
shots = dict(threequarter=camera("cam_34", (-3.5, -5.2, 2.6), (0.05, -0.2, 0.85), 40),
             front=camera("cam_front", (0.1, -4.4, 1.45), (0.0, -0.9, 1.22), 50),
             grass=camera("cam_grass", (2.3, -5.2, 3.9), (-0.1, 1.5, 0.15), 30))
os.makedirs(out, exist_ok=True)
if ANIM:
    sc.camera = shots["threequarter"]
    sc.frame_step = 2
    sc.render.filepath = os.path.join(out, "anim_")
    t = time.time()
    bpy.ops.render.render(animation=True)
    print("RENDER_SECONDS %.1f for %d frames" % (time.time() - t, len(range(1, 49, 2))))
else:
    sc.frame_set(STILL_FRAME)
    for shot, cam in shots.items():
        sc.camera = cam
        sc.render.filepath = os.path.join(out, f"jellysnail_{shot}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        print("RENDER_SECONDS %s %.1f" % (shot, time.time() - t))
