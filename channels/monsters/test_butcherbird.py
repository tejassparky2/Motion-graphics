"""Model-sheet stills of the butcher bird on the painted meadow: three-quarter, front close-up, and from below looking
up at it as it stares down (the S23 angle).
    blender -b -P channels/monsters/test_butcherbird.py -- OUTDIR [threequarter front below]
Writes OUTDIR/butcherbird_<shot>.png at 720x1280, 16 samples."""
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import butcherbird, look, meadow  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
outdir, shots = args[0], args[1:] or ["threequarter", "front", "below"]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(720, 1280, 16)
meadow.build("before")
rig = butcherbird.build((-2.4, -3.6, 0), scale=1.6)
butcherbird.stare(rig, 30)


def camera(loc, target, lens, fstop=0.6, focus=None):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    cam.data.dof.aperture_fstop = fstop
    return cam


SHOTS = {
    "threequarter": (lambda: camera((2.6, -11.4, 2.4), (-2.3, -3.2, 1.25), 50), 1),
    "front": (lambda: camera((-2.4, -10.6, 1.6), (-2.4, -3.6, 1.4), 70, focus=(-2.4, -4.6, 1.4)), 1),
    "below": (lambda: camera((-1.4, -6.6, 0.25), (-2.4, -3.6, 1.6), 30, focus=(-2.2, -4.4, 1.2)), 40),
}
for shot in shots:
    make, frame = SHOTS[shot]
    sc.camera = make()
    sc.frame_set(frame)
    sc.render.filepath = f"{outdir}/butcherbird_{shot}.png"
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER %s frame %d: %.1f s" % (shot, frame, time.time() - t))
