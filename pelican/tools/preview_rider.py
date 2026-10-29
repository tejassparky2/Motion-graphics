"""Stills of the pelican on the bicycle for look development.

blender -b -P pelican/tools/preview_rider.py -- OUTDIR [view ...] [--samples N] [--res WxH]
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import bpy  # noqa: E402
import numpy as np  # noqa: E402

from pb import bicycle, render, util, pelican  # noqa: E402
from pb.nodes import simple_material  # noqa: E402

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
out = argv[0] if argv else '/tmp'
args = argv[1:]
samples = 24
res = (960, 540)
views_req = []
i = 0
while i < len(args):
    if args[i] == '--samples':
        samples = int(args[i + 1])
        i += 2
    elif args[i] == '--res':
        res = tuple(int(x) for x in args[i + 1].split('x'))
        i += 2
    else:
        views_req.append(args[i])
        i += 1
os.makedirs(out, exist_ok=True)

util.clear_scene()
sc = bpy.context.scene
coll = util.collection("Bike")
t0 = time.time()
info = bicycle.build(coll)
bpy.context.view_layer.layer_collection.children['Bike'].children['ChainProtos'].exclude = True
pcoll = util.collection("Pelican")
pinfo = pelican.build(pcoll, info)
print("BUILD_TIME", time.time() - t0)

ground = util.make_mesh("Ground", np.array([[-5, -5, 0], [5, -5, 0], [5, 5, 0], [-5, 5, 0]]),
                        [[0, 1, 2, 3]], mat=simple_material("G", (0.35, 0.33, 0.3), 0.8))
w = bpy.data.worlds.new("W")
sc.world = w
w.use_nodes = True
sky = w.node_tree.nodes.new("ShaderNodeTexSky")
sky.sky_type = 'NISHITA'
sky.sun_elevation = math.radians(18)
sky.sun_rotation = math.radians(150)
w.node_tree.links.new(sky.outputs[0], w.node_tree.nodes["Background"].inputs[0])
w.node_tree.nodes["Background"].inputs[1].default_value = 0.25

render.setup(sc, res=res, samples=samples)
sc.view_settings.exposure = -1.0
sc.render.use_motion_blur = False

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
target = util.empty("Target", coll, loc=(0.5, 0, 0.6))
tc = cam.constraints.new('TRACK_TO')
tc.target = target

views = {
    'side': ((0.5, -3.2, 0.75), (0.5, 0, 0.62), 50),
    'front34': ((2.6, -1.7, 1.15), (0.5, 0, 0.66), 50),
    'rear34': ((-1.6, 1.9, 1.35), (0.45, 0, 0.66), 50),
    'head': ((1.25, -0.75, 1.15), (0.78, 0, 1.03), 60),
    'front': ((3.0, 0.0, 1.0), (0.5, 0, 0.66), 60),
    'top': ((0.5, -0.4, 3.0), (0.5, 0, 0.66), 50),
    'feet': ((0.75, -0.9, 0.35), (0.38, -0.1, 0.30), 50),
    'wing': ((0.9, -0.85, 0.95), (0.55, -0.2, 0.76), 55),
}
for name, (loc, tgt, lens) in views.items():
    if views_req and name not in views_req:
        continue
    cam.location = loc
    target.location = tgt
    cam_data.lens = lens
    sc.render.filepath = os.path.join(out, f"rider_{name}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name, time.time() - t0)
