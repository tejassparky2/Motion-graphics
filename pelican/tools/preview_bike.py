"""Turntable-style stills of the bicycle alone, for checking geometry.

blender -b -P pelican/tools/preview_bike.py -- OUTDIR
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import bpy  # noqa: E402
import numpy as np  # noqa: E402

from pb import bicycle, render, util  # noqa: E402
from pb.nodes import simple_material  # noqa: E402

out = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else '/tmp'
os.makedirs(out, exist_ok=True)
util.clear_scene()
sc = bpy.context.scene
coll = util.collection("Bike")
t0 = time.time()
info = bicycle.build(coll)
print("BUILD_TIME", time.time() - t0)
lc = bpy.context.view_layer.layer_collection.children['Bike'].children['ChainProtos']
lc.exclude = True
info['crank'].rotation_euler[1] = 0.6

ground = util.make_mesh("Ground", np.array([[-5, -5, 0], [5, -5, 0], [5, 5, 0], [-5, 5, 0]]),
                        [[0, 1, 2, 3]], mat=simple_material("G", (0.35, 0.33, 0.3), 0.8))
w = bpy.data.worlds.new("W")
sc.world = w
w.use_nodes = True
sky = w.node_tree.nodes.new("ShaderNodeTexSky")
sky.sky_type = 'NISHITA'
sky.sun_elevation = math.radians(25)
sky.sun_rotation = math.radians(200)
w.node_tree.links.new(sky.outputs[0], w.node_tree.nodes["Background"].inputs[0])
w.node_tree.nodes["Background"].inputs[1].default_value = 0.25

render.setup(sc, res=(960, 540), samples=24)
sc.view_settings.exposure = -1.0

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
target = util.empty("Target", coll, loc=(0.42, 0, 0.36))
tc = cam.constraints.new('TRACK_TO')
tc.target = target

views = {
    'side_right': ((0.42, -2.2, 0.45), 50),
    'front34': ((1.9, -1.1, 0.75), 50),
    'rear34': ((-1.2, 1.4, 0.9), 50),
    'drive_close': ((0.25, -0.75, 0.45), 50),
    'cockpit': ((0.35, 0.0, 1.15), 35),
}
which = sys.argv[sys.argv.index('--') + 2:] if '--' in sys.argv else []
for name, (loc, lens) in views.items():
    if which and name not in which:
        continue
    cam.location = loc
    cam_data.lens = lens
    if name == 'drive_close':
        target.location = (0.22, 0, 0.26)
    elif name == 'cockpit':
        target.location = (0.75, 0, 0.55)
    else:
        target.location = (0.42, 0, 0.36)
    sc.render.filepath = os.path.join(out, f"bike_{name}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name, time.time() - t0)
