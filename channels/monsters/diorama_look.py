"""Diorama look-dev still (owner, 31 Oct 2026: the 2.5D game-diorama style test). One frame of the clearing: the forest
island, the puddle, the puff-shrimp drinking and Kai standing over it, seen by the tilted diorama camera.

    blender -b -y -P channels/monsters/diorama_look.py -- OUT.png [--scale 0.5] [--samples 16] [--tilt 52]
            [--dist 330] [--lens 85] [--fstop 0.35]
"""
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters.mk import diorama, hero, puffshrimp  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]


def opt(name, default):
    return type(default)(argv[argv.index(name) + 1]) if name in argv else default


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = diorama.setup(samples=opt("--samples", 16))
isl = diorama.island()
puffshrimp.build((0, 0.4, 0))
k = hero.load((3.2, -7.0, 0), scale=5.8, rot_z=0.5)
cam = diorama.camera("look", (0.5, -2.5, 3.0), dist=opt("--dist", 200.0), tilt=opt("--tilt", 48.0),
                     lens=opt("--lens", 85.0), blur=opt("--blur", 14.0))
sc.camera = cam
sc.render.resolution_percentage = int(opt("--scale", 0.5) * 100)
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("WROTE", out, len(isl["trees"]), "trees")
