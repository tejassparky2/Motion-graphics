"""Render selected frames of the built scene.

blender -b scene.blend -P pelican/tools/render_frames.py -- OUTDIR --frames 1,60,120
        [--pct 50] [--samples 16] [--engine CYCLES|WORKBENCH] [--range A-B] [--step N] [--noblur]
"""
import os
import sys
import time

import bpy

argv = sys.argv[sys.argv.index('--') + 1:]
out = argv[0]
opts = {}
i = 1
while i < len(argv):
    if argv[i].startswith('--'):
        key = argv[i][2:]
        if i + 1 < len(argv) and not argv[i + 1].startswith('--'):
            opts[key] = argv[i + 1]
            i += 2
        else:
            opts[key] = True
            i += 1
    else:
        i += 1
os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
frames = []
if 'frames' in opts:
    frames = [int(x) for x in opts['frames'].split(',')]
if 'range' in opts:
    a, b = (int(x) for x in opts['range'].split('-'))
    frames += list(range(a, b + 1, int(opts.get('step', 1))))
sc.render.resolution_percentage = int(opts.get('pct', 50))
if 'samples' in opts:
    sc.cycles.samples = int(opts['samples'])
if 'threshold' in opts:
    sc.cycles.adaptive_threshold = float(opts['threshold'])
if opts.get('noblur'):
    sc.render.use_motion_blur = False
if opts.get('nocomp'):
    sc.render.use_compositing = False
if opts.get('engine') == 'WORKBENCH':
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'
    sc.display.shading.color_type = 'MATERIAL'
    sc.render.use_compositing = False
fmt = opts.get('format', 'PNG')
if fmt == 'JPEG':
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 92
    ext = 'jpg'
else:
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_depth = '16' if opts.get('deep') else '8'
    ext = 'png'
prefix = opts.get('prefix', 'f')
budget = float(opts.get('budget', 1e12))     # seconds; stop starting new frames after this
t_start = time.time()
for f in frames:
    if time.time() - t_start > budget:
        print("BUDGET_REACHED", flush=True)
        break
    sc.frame_set(f)
    sc.render.filepath = os.path.join(out, f"{prefix}_{f:04d}.{ext}")
    if opts.get('skip_existing') and os.path.exists(sc.render.filepath):
        continue
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"FRAME {f} {time.time() - t0:.1f}s", flush=True)
