"""Still tests of the fluffmoth hovering over a painted meadow:
    fluffmoth_hover.png        the hover in three-quarter view (idle animation, a frame on the wings' upstroke)
    fluffmoth_spots_open.png   close-up on the face and a forewing: the eye-spots open
    fluffmoth_spots_half.png   the same close-up with the eye-spots half shut (the tell)
    fluffmoth_s14c.png         shot S14c's framing (cute held pose, locked low camera), on its last beat as the eye-spots
                               shut; the face stays below the WILD tag (y > 200), nothing important below y 845 or in
                               the right rail (x > 620)
blender -b -P channels/monsters/test_fluffmoth.py -- OUTDIR [hover|open|half|s14c|all] [W H]
blender -b -P channels/monsters/test_fluffmoth.py -- OUTDIR anim F0 F1 [W H]   (idle frames, for checking motion)"""
import math
import os
import random
import sys
import time

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import fluffmoth, look, paintbg  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
outdir, which = argv[0], (argv[1] if len(argv) > 1 else "all")
nums = [int(a) for a in argv[2:]]
f0, f1 = (nums[0], nums[1]) if which == "anim" else (1, 96)
W, H = (nums[-2], nums[-1]) if len(nums) in (2, 4) and not (which == "anim" and len(nums) == 2) else (720, 1280)
os.makedirs(outdir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, 16)
paintbg.sky()
look.sun(elev=48, azim=-30)
bpy.ops.mesh.primitive_plane_add(size=200)
bpy.context.object.data.materials.append(paintbg.grass_material())
rnd = random.Random(5)
for i in range(12):                                            # a meadow edge of trees, then far trees
    x = -14 + i * 2.6 + rnd.uniform(-0.8, 0.8)
    paintbg.tree((x, 12 + rnd.uniform(-1.5, 2.5), 0), height=rnd.uniform(6, 8), radius=rnd.uniform(2.2, 3.0),
                 seed=60 + i, variant=i % 4)
for i in range(10):
    x = -26 + i * 5.5 + rnd.uniform(-1.5, 1.5)
    paintbg.tree((x, 30 + rnd.uniform(-3, 3), 0), height=rnd.uniform(8, 11), radius=rnd.uniform(3.2, 4.2),
                 seed=90 + i, variant=i % 4, far=0.45, res=0.2)
paintbg.grass_tufts((0, -1.0, 0), 4.5, n=90, seed=3)

rig = fluffmoth.build((0, 0.6, 0))
rig["root"].rotation_euler = (0, 0, math.radians(-28))        # three-quarter: turned toward camera left
bpy.ops.object.camera_add()
cam = bpy.context.object
sc.camera = cam
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 0.16                             # anime-strength background blur


def look_at(loc, target):
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()


def shot(path, frame=1):
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    sc.render.filepath = path
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %.1f %s" % (time.time() - t, path))


def hover_camera():
    """Low, at the moth's eye level, looking up a little against the sky; the moth big in frame."""
    look_at((-2.0, -6.2, 1.25), (0.15, 0.6, 2.2))
    cam.data.lens = 36
    cam.data.dof.focus_object = rig["body"]
    cam.data.dof.aperture_fstop = 0.16


def key_points(spots):
    """World points that must stay in frame: the face's extent and the rims of the given eye-spots."""
    bpy.context.view_layer.update()
    bw = rig["body"].matrix_world
    pts = [bw @ Vector(p) for p in ((-0.95, -0.4, 0.1), (0.95, -0.4, 0.1), (0, -0.6, 0.95), (0, -0.6, -0.7))]
    for s in spots:
        mw = s.matrix_world                                   # the disc's rim, in its own X-Z plane
        pts += [mw @ Vector((math.cos(a), 0, math.sin(a))) for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    return pts


def fit(pts, d, window=(0.06, 0.94, 0.06, 0.94), lens=35):
    """Locked camera looking along -d, as close as it can be with every point inside `window` (u0, u1, v0, v1 in
    0-1 image coordinates, v up), the points centred in the window with lens shift."""
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    mid = (lo + hi) / 2
    cam.data.lens = lens
    tu, tv = (window[0] + window[1]) / 2, (window[2] + window[3]) / 2
    for dist in np.arange(1.5, 14.0, 0.05):
        cam.data.shift_x = cam.data.shift_y = 0.0
        look_at(mid + d * dist, mid)
        for _ in range(3):
            uv = [world_to_camera_view(sc, cam, p) for p in pts]
            cam.data.shift_x += ((min(c.x for c in uv) + max(c.x for c in uv)) / 2 - tu) * W / H
            cam.data.shift_y += (min(c.y for c in uv) + max(c.y for c in uv)) / 2 - tv
            bpy.context.view_layer.update()
        uv = [world_to_camera_view(sc, cam, p) for p in pts]
        if all(window[0] < c.x < window[1] and window[2] < c.y < window[3] for c in uv):
            break
    return (cam.location - mid).length


def closeup_camera():
    """Close and a little low, off to the moth's right: its face and both right-side eye-spots staring out, framed as
    tight as they fit. Focus on their middle with a softer aperture so all three read; the background still melts."""
    d = (rig["root"].matrix_world.to_3x3() @ Vector((0.45, -1.0, -0.15))).normalized()
    dist = fit(key_points([rig["spots"][1], rig["spots"][3]]), d, (0.05, 0.95, 0.12, 0.9))
    cam.data.dof.focus_object = None
    cam.data.dof.focus_distance = dist
    cam.data.dof.aperture_fstop = 0.8


if which == "anim":
    fluffmoth.idle(rig, 1, max(f1, 96))
    hover_camera()
    for f in range(f0, f1 + 1):
        shot(os.path.join(outdir, "fluffmoth_anim_%04d.png" % f), f)
if which in ("all", "hover"):
    fluffmoth.idle(rig, 1, 96)
    hover_camera()
    shot(os.path.join(outdir, "fluffmoth_hover.png"), int(os.environ.get("FRAME", "10")))
if which in ("all", "s14c"):
    for o in [*rig["wings"], *rig["spots"], rig["hover"], rig["body"], *rig["antennae"], *rig["eyes"], rig["shadow"]]:
        o.animation_data_clear()
    f_end = fluffmoth.s14c(rig, 1)
    sc.frame_set(f_end - 4)
    d = (rig["root"].matrix_world.to_3x3() @ Vector((0.15, -1.0, -0.12))).normalized()
    pts = key_points(rig["spots"])
    pts += [c.matrix_world @ v.co for a in rig["antennae"] for c in a.children for v in list(c.data.vertices)[::40]]
    fit(pts, d, (0.03, 0.86, 1 - 845 / 1280 + 0.02, 1 - 200 / 1280))   # the safe window (see the docstring)
    cam.data.dof.focus_object = rig["body"]
    cam.data.dof.aperture_fstop = 0.3
    shot(os.path.join(outdir, "fluffmoth_s14c.png"), f_end - 4)
if which in ("all", "open", "half"):
    for o in [*rig["wings"], *rig["spots"], rig["hover"], rig["body"], *rig["antennae"], *rig["eyes"], rig["shadow"]]:
        o.animation_data_clear()
    rig["hover"].location = (0, 0, fluffmoth.HOVER)
    fluffmoth.wing_pose(rig, 1, 0.3)
    closeup_camera()
    for name, lid in (("open", 0.0), ("half", float(os.environ.get("HALF", "0.62")))):
        if which in ("all", name):
            for s in rig["spots"]:
                s["lid"] = lid
                s.update_tag()
            shot(os.path.join(outdir, f"fluffmoth_spots_{name}.png"))
