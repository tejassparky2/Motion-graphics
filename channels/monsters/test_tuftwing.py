"""Stills of the tuftwing on a small painted meadow: a three-quarter view, a front close-up, a high view on the grass
that shows its oversized shadow, and the top of a hop (the shadow stays on the ground).
    blender -b -P channels/monsters/test_tuftwing.py -- OUTDIR [threequarter front grass hop]
Writes OUTDIR/tuftwing_<shot>.png at 720x1280, 16 samples."""
import random
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import look, tuftwing  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
outdir, shots = args[0], args[1:] or ["threequarter", "front", "grass", "hop"]
HOP = 70


def meadow(seed=11, clear=(3.9, 2.9)):
    """Grass with tufts and flowers (none inside the shadow, so nothing pokes through it), trees and clouds behind."""
    hx, P = look.hexc, look.paint
    grass, trunk = P("grass", hx("#79c95f"), noise=0.12, scale=1.2), P("trunk", hx("#8a5a3b"))
    tufts = [P("tuft0", hx("#5fbf55")), P("tuft1", hx("#8edc72"))]
    flowers = [P("fl0", hx("#ffe066")), P("fl1", hx("#ff8fb1")), P("fl2", hx("#ffffff"))]
    leaves = [P("leaf0", hx("#4fb35a")), P("leaf1", hx("#ffb347")), P("leaf2", hx("#3f9e6a"))]
    far = [P("fleaf0", hx("#7fc79a")), P("fleaf1", hx("#ffc985")), P("fleaf2", hx("#79b8a0"))]
    cloud = P("cloud", hx("#e9f3ff"), top=hx("#ffffff"), noise=0.0)
    bpy.ops.mesh.primitive_plane_add(size=200)
    bpy.context.object.data.materials.append(grass)
    rnd = random.Random(seed)

    def sphere(loc, scale, mat, seg=16):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
        o = bpy.context.object
        o.scale = scale
        o.data.materials.append(mat)
        for p in o.data.polygons:
            p.use_smooth = True
        return o
    for i in range(420):
        x, y = rnd.uniform(-9, 9), rnd.uniform(-12, 12)
        if (x / clear[0]) ** 2 + ((y - 0.3) / clear[1]) ** 2 < 1:
            continue
        if rnd.random() < 0.8:
            bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.11, depth=0.32, location=(x, y, 0.16))
            bpy.context.object.data.materials.append(rnd.choice(tufts))
        else:
            sphere((x, y, 0.1), (0.09, 0.09, 0.05), rnd.choice(flowers), 10)
    for i in range(60):
        x, y, s = rnd.uniform(-24, 24), rnd.uniform(13, 40), rnd.uniform(1.1, 2.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * s, depth=1.2 * s, location=(x, y, 0.6 * s), vertices=10)
        bpy.context.object.data.materials.append(trunk)
        sphere((x, y, 1.9 * s), (1.1 * s, 1.1 * s, s), rnd.choice(far if y > 26 else leaves), 20)
    for i in range(6):
        cx, cz = rnd.uniform(-50, 50), rnd.uniform(16, 30)
        for j in range(6):
            r = rnd.uniform(4, 8)
            sphere((cx + rnd.uniform(-9, 9), 100 + rnd.uniform(-5, 5), cz + rnd.uniform(-2, 4)), (r * 1.4, r, r), cloud,
                   20)


def camera(loc, target, lens, focus=None, fstop=None):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    if focus is not None:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = focus
        cam.data.dof.aperture_fstop = fstop
    return cam


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(720, 1280, 16)
look.world()
look.sun()
meadow()
rig = tuftwing.build((0, 0, 0))
tuftwing.idle(rig, 1, HOP - 8)
land = tuftwing.hop(rig, HOP)
sc.frame_start, sc.frame_end = 1, land + 12


def tilted_frame():
    """The idle frame where the head is tilted furthest (a cuter pose for the three-quarter view)."""
    best, fb = 0.0, 1
    for f in range(1, HOP - 10):
        sc.frame_set(f)
        if abs(rig["head"].rotation_euler.y) > best and rig["eyes"][0].scale.z > 0.9:
            best, fb = abs(rig["head"].rotation_euler.y), f
    return fb


SHOTS = {
    "threequarter": lambda: (camera((4.4, -6.6, 2.4), (0.05, 0.35, 0.78), 50, rig["head"], 5.6), tilted_frame()),
    "front": lambda: (camera((0, -5.2, 1.0), (0, 0, 0.86), 85, rig["head"], 2.8), 1),
    "grass": lambda: (camera((2.2, -9.4, 8.6), (0, 0.45, 0.15), 34), 1),
    "hop": lambda: (camera((3.0, -9.6, 4.4), (0, 0.4, 0.7), 35), (HOP + land) // 2),
}
for shot in shots:
    cam, frame = SHOTS[shot]()
    sc.camera = cam
    sc.frame_set(frame)
    sc.render.filepath = f"{outdir}/tuftwing_{shot}.png"
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER %s frame %d: %.1f s" % (shot, frame, time.time() - t))
