"""Build the whole film scene and save it as a .blend.

blender -b -P pelican/build.py -- --out scene.blend [--seconds 20] [--preview]
"""
import argparse
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
import numpy as np  # noqa: E402

from pb import anim, bicycle, environment, pelican, render, rig, shots, util  # noqa: E402
from pb import env_materials as em  # noqa: E402
from pb import compositor  # noqa: E402

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--out', default='/tmp/pelican.blend')
ap.add_argument('--seconds', type=float, default=shots.DURATION)
ap.add_argument('--samples', type=int, default=48)
args = ap.parse_args(argv)

t0 = time.time()
util.clear_scene()
scene = bpy.context.scene
T = anim.Timeline(args.seconds)
scene.frame_start = int(T.frames[0])
scene.frame_end = int(T.frames[-1])
scene.render.fps = anim.FPS

env_coll = util.collection("Environment")
env = environment.build(env_coll, T)
print(f"environment {time.time() - t0:.1f}s")

bike_coll = util.collection("Bike")
bike = bicycle.build(bike_coll)
bpy.context.view_layer.layer_collection.children['Bike'].children['ChainProtos'].exclude = True
pel_coll = util.collection("Pelican")
pel = pelican.build(pel_coll, bike)
rg = rig.build(pel_coll, bike, pel)
print(f"characters {time.time() - t0:.1f}s")

motion = anim.bike_motion(T, **shots.BIKE_PATH)
anim.apply_bike(T, bike, motion)
anim.apply_rider(T, rg['rig'], motion, shots.HEAD_KEYS, shots.JAW_KEYS)
anim.feather_wind(pel['plumage'], pel['plumage_arrays'], T)

world, sun, sky = environment.build_sky(scene, **shots.SUN)
birds_coll = util.collection("Birds")
environment.build_gulls(birds_coll, [em.gull_white(), em.gull_grey(), em.simple_material("GullBeak", (0.9, 0.7, 0.1), 0.4)],
                        T, n_fly=8, perched=shots.PERCHED_GULLS)
environment.build_far_pelicans(birds_coll, em.bird_silhouette(), T, **shots.FAR_PELICANS)
sign = environment.build_sign(env_coll, (em.sign_board(), em.sign_red(), em.sign_text(), env['paint']),
                              **shots.SIGN)

render.setup(scene, samples=args.samples)
cams = shots.setup(scene, T, bike, pel, rg, motion, sun, sky)
compositor.setup(scene)
np.savez(os.path.abspath(args.out).replace('.blend', '_motion.npz'),
         t=motion['t'], x=motion['x'], crank=motion['crank'], wheel=motion['wheel'], cog=motion['cog'],
         pedal_on=motion['pedal_on'], v=motion['v'],
         shots=np.array([[a, b] for _, a, b in shots.SHOTS]),
         jaw=np.array(shots.JAW_KEYS, dtype=float))
print(f"total build {time.time() - t0:.1f}s")
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.out), compress=True)
print("SAVED", args.out)
