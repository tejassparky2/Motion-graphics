"""Still test of the jelly-snail on the painted anime background (paintbg sky, brush-stroke grass, cauliflower trees,
anime-strength depth of field, low eye-level cameras):
    blender -b -P channels/monsters/test_jellysnail.py -- OUTDIR [W H SAMPLES]
writes OUTDIR/jellysnail_threequarter.png (idle), jellysnail_front.png (close-up), jellysnail_grass.png (its burned,
smoking trail), jellysnail_s14a.png (S14a in the v3.2 shot list: close, locked, the cute held pose; face between
y 200 and the captions at 845, clear of the right rail) and jellysnail_shock.png (the shock reaction pose, a freeze
frame).
    blender -b -P channels/monsters/test_jellysnail.py -- OUTDIR W H SAMPLES anim
renders the idle (frames 1-48, every 2nd) from the three-quarter camera instead, as OUTDIR/anim_####.png."""
import os
import random
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import jellysnail, look, paintbg  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280, 16)
ANIM = len(argv) > 4 and argv[4] == "anim"
IDLE, HOLD, SHOCK = (1, 60), (100, 122), 150                  # frame ranges for the three motions on one rig


def background(trail, seed=3):
    """The painted meadow: brush-stroke grass, a wall of cauliflower trees, paler far trees, grass tufts near the
    snail (none on its trail or in the burned holes)."""
    bpy.ops.mesh.primitive_plane_add(size=200)
    bpy.context.object.data.materials.append(paintbg.grass_material())
    rnd = random.Random(seed)
    for i in range(14):
        x = -16 + i * 2.5 + rnd.uniform(-0.8, 0.8)
        paintbg.tree((x, 11 + rnd.uniform(-1.5, 2.5), 0), height=rnd.uniform(6, 8), radius=rnd.uniform(2.2, 3.0),
                     seed=10 + i, variant=i % 4)
    for i in range(12):
        x = -30 + i * 5.5 + rnd.uniform(-1.5, 1.5)
        paintbg.tree((x, 30 + rnd.uniform(-3, 3), 0), height=rnd.uniform(8, 11), radius=rnd.uniform(3.2, 4.2),
                     seed=40 + i, variant=i % 4, far=0.45, res=0.2)

    def avoid(x, y):
        if (x / 0.95) ** 2 + ((y - 0.15) / 1.8) ** 2 < 1:             # under the snail
            return True
        if any((x - hx) ** 2 + (y - hy) ** 2 < (2.1 * r) ** 2 for hx, hy, r in trail["holes"]):
            return True
        return any((x - px) ** 2 + (y - py) ** 2 < 0.5 ** 2 for px, py in trail["path"])
    paintbg.grass_tufts((0, 0.5), 5.5, n=170, seed=seed, avoid=avoid)


def camera(name, loc, target, lens, focus, fstop=0.15):
    """A camera aimed at `target`, focused on the object `focus` (or a world point)."""
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    if isinstance(focus, tuple):
        cam.data.dof.focus_distance = (Vector(focus) - Vector(loc)).length
    else:
        cam.data.dof.focus_object = focus
    cam.data.dof.aperture_fstop = fstop                       # anime-strength background blur
    return cam


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = 1, 48
paintbg.sky()
look.sun(elev=45, azim=-30)
rig = jellysnail.build((0, 0, 0))
background(rig["trail"])
jellysnail.idle(rig, *IDLE)
jellysnail.hold(rig, *HOLD, kind="cute")
jellysnail.pose(rig, SHOCK, "shock")
mid = bpy.data.objects.new("trail_focus", None)               # the wide shot focuses between the snail and its holes
sc.collection.objects.link(mid)
mid.location = (0.1, 1.6, 0.3)
cams = dict(threequarter=camera("cam_34", (-2.6, -4.2, 1.15), (0.1, -0.1, 0.95), 40, rig["body"]),
            front=camera("cam_front", (0.1, -4.7, 1.35), (0.0, -0.9, 1.22), 45, (0.0, -1.15, 1.2)),
            grass=camera("cam_grass", (2.4, -5.0, 3.8), (-0.1, 1.6, 0.1), 30, mid, 0.5),
            s14a=camera("cam_s14a", (-1.82, -4.55, 1.32), (0.0, -1.1, 1.0), 42, (0.0, -1.1, 1.1)))
shots = [("threequarter", 9), ("front", 9), ("grass", 9), ("s14a", HOLD[0] + 6), ("shock", SHOCK)]
os.makedirs(out, exist_ok=True)
if ANIM:
    sc.camera = cams["threequarter"]
    sc.frame_step = 2
    sc.render.filepath = os.path.join(out, "anim_")
    t = time.time()
    bpy.ops.render.render(animation=True)
    print("RENDER_SECONDS %.1f for %d frames" % (time.time() - t, len(range(1, 49, 2))))
else:
    for shot, frame in shots:
        sc.frame_set(frame)
        sc.camera = cams.get(shot, cams["threequarter"])
        sc.render.filepath = os.path.join(out, f"jellysnail_{shot}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        print("RENDER_SECONDS %s %.1f" % (shot, time.time() - t))
