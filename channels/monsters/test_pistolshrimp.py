"""Stills of the pistol shrimp in its tank (Episode 1): a close-up, the slow-motion cavitation-bubble frame for the
"~4,700 °C" fact card, and the frame where the crack runs up the glass. One animated scene (idle, a slow-motion
snap, a normal snap that cracks the glass), three cameras.
    blender -b -P channels/monsters/test_pistolshrimp.py -- OUTDIR [W H SAMPLES] [close,bubble,crack]
Writes OUTDIR/pistolshrimp_{close,bubble,crack}.png."""
import math
import os
import sys
import time

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from channels.monsters.mk import anim, look, pistolshrimp as ps  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280, 16)
only = argv[4].split(",") if len(argv) > 4 else ["close", "bubble", "crack"]

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(W, H, S)
sc.frame_start, sc.frame_end = 1, 110
look.world(sky="#16344c", horizon="#2f6680", fill="#c4ecff", fill_strength=0.6)
look.sun(elev=70, azim=-30, energy=4.0, color="#f2fbff")
t = ps.tank(crack_x=-2.0)
rig = ps.build((0.3, -0.2, 0.0), turn=math.radians(25))
ps.idle(rig, 1, 110)
SLOW = 40                                     # slow-motion snap (bubble peak at SLOW + 4)
ps.snap(rig, SLOW, slow=4)
CRACK = 86                                    # a normal snap; the glass cracks a frame later
ps.snap(rig, CRACK)
ps.crack(t, CRACK + 1)
anim.on_twos([rig["body"], rig["tail"], rig["shoulder"], *rig["eyes"], *rig["antennae"]])


def camera(name, loc, target, lens, focus=None, fstop=2.8):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    if focus is not None:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = focus
        cam.data.dof.aperture_fstop = fstop
    return cam


shots = {
    "close": (camera("cam_close", (-2.6, -7.3, 2.3), (-0.85, -1.0, 0.85), 55, rig["body"], 2.0), SLOW - 3),
    "bubble": (camera("cam_bubble", (-2.7, -5.9, 0.85), (-1.75, -1.6, 0.66), 55, rig["tip"], 2.8), SLOW + 4),
    "crack": (camera("cam_crack", (-1.7, -8.2, 2.3), (-1.4, -0.6, 2.0), 45, None), CRACK + 8),
}
os.makedirs(out, exist_ok=True)
for label in only:
    cam, frame = shots[label]
    sc.camera = cam
    sc.frame_set(frame)
    sc.render.filepath = os.path.join(out, f"pistolshrimp_{label}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %s frame %d: %.1f" % (label, frame, time.time() - t0))
