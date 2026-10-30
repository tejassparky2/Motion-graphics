"""Stills of the new world: above the clouds and mid-descent on world.fall_camera(), and Kai's eye-level POV in the
clearing (world.pov_camera(), S13).
    blender -b -P channels/monsters/test_world.py -- OUTDIR [--half] [--cloud]
Writes OUTDIR/world_above.png, world_mid.png, world_eye.png (and world_cloud.png, inside the deck, with --cloud)."""
import sys
import time
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from channels.monsters.mk import look, paintbg, world  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
out = Path(args[0])
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(360, 640, 8) if "--half" in args else look.render_setup()
paintbg.sky()
look.sun(elev=45, azim=-30)
t = time.time()
h = world.build(seed=7)
print("BUILD_SECONDS %.1f" % (time.time() - t))
F0, F1 = 1, 108                                    # the whole fall as one 4.5 s shot at 24 fps
stills = [("above", 0.0), ("mid", 0.8), ("eye", None)] + ([("cloud", 0.42)] if "--cloud" in args else [])
fall = world.fall_camera(F0, F1)
for name, frac in stills:
    if frac is None:
        world.pov_camera()
    else:
        sc.camera = fall
        world.aim_sparkles(fall)
        sc.frame_set(round(F0 + frac * (F1 - F0)))
    sc.render.filepath = str(out / f"world_{name}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER_SECONDS %s %.1f" % (name, time.time() - t))
