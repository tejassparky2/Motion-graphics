"""Ep 3 shared-moth test (mk/fluffmoth.py): a level moth, a moth with its back to the coral light, one on its back
waving its legs, and a 40-moth swarm orbiting the light (backs tilted to it, small ones far away), at dusk.
    blender -b -y -P channels/monsters/test_moth3.py -- OUTDIR [--still N] [--frames A-B] [--scale 0.5]"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from channels.monsters.mk import diorama, fluffmoth as fm, look  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
opt = {k: (argv[i + 1] if i + 1 < len(argv) else "") for i, k in enumerate(argv) if k.startswith("--")}
scale = float(opt.get("--scale", 0.5))
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(int(720 * scale), int(1280 * scale), 16)
diorama.setup(sun_elev=8, haze=0.3)
sc.frame_start, sc.frame_end = 1, 48
for o in sc.objects:                                              # dusk: the sun low and dim
    if o.type == "LIGHT" and o.data.type == "SUN":
        o.data.energy = 0.8
bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0))
g = bpy.context.object
g.data.materials.append(diorama.lit_paint("t3_grass", "#1d3b2e", "#2e5a3c", "#4b7a4c"))
L = Vector((0.0, 0.0, 3.2))                                       # the mark's light, above the swarm
lb = bpy.data.lights.new("t3_mark", "POINT")
lb.color, lb.energy, lb.shadow_soft_size = look.hexc("#ff8466")[:3], 900.0, 0.3
lo = bpy.data.objects.new("t3_mark", lb)
sc.collection.objects.link(lo)
lo.location = L
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=L)
bpy.context.object.data.materials.append(look.flat("t3_glow", look.hexc("#ffd6c8"), 3.0))

# A: level flight (left)   B: back square to the light (right)   C: on its back, legs waving (front)
a = fm.build((-3.2, -1.0, 0), name="mA")
fm.flight_mode(a)
a["root"].location = (-3.4, -2.0, 2.6)
fm.face(a, 1, (1, 0, 0))
fm.flap(a)
b = fm.build((0, 0, 0), name="mB")
fm.flight_mode(b)
b["root"].location = (2.6, -1.6, 2.2)
fm.back_to(b, 1, L, (0, 1, 0))
fm.flap(b, phase=2)
c = fm.build((0, -4.2, 0), name="mC")
c["root"].location = (0.4, -4.4, 0)
fm.upside_down(c, 1, 48)


# D: the swarm orbiting the light (backs tilted toward it), near big, far small
def place(i, rnd):
    r = rnd.uniform(2.2, 7.5)
    return Vector((r, 0, 0)), (0.42 if r < 4 else 0.3) * rnd.uniform(0.85, 1.1)


sw = [] if "--noswarm" in argv else fm.swarm(40, place, name="sw", far=lambda i, loc, s: loc.length > 5.5)
import random  # noqa: E402
rnd = random.Random(5)
for i, r in enumerate(sw):
    rad = r["root"].location.length
    th0, z0 = rnd.uniform(0, 2 * math.pi), rnd.uniform(1.4, 5.0) + rad * 0.25
    w = 1.6 / rad                                                  # inner ones circle faster
    prev = None
    for f in range(1, 49, 2):
        th = th0 + w * (f - 1) / 24.0
        p = Vector((math.cos(th) * rad, math.sin(th) * rad + 6.0, z0 + 0.3 * math.sin(f * 0.2 + i)))
        r["root"].location = p
        r["root"].keyframe_insert("location", frame=f)
        prev = fm.back_to(r, f, L + Vector((0, 6.0, 0)), (-math.sin(th), math.cos(th), 0), amount=0.75, prev=prev)
lo2 = lo.copy()                                                    # the swarm's own light, behind
sc.collection.objects.link(lo2)
lo2.location = L + Vector((0, 6.0, 0))

cam = (diorama.camera("t3_cam", (0.4, -4.4, 0.9), dist=7, tilt=30, yaw=0, lens=50, blur=4) if "--close" in opt
       else diorama.camera("t3_cam", (0, 0.5, 2.0), dist=17, tilt=14, yaw=0, lens=35, blur=4))
sc.camera = cam
sc.world.mist_settings.start, sc.world.mist_settings.depth = 30, 60
if "--still" in opt:
    frames = [int(opt["--still"])]
else:
    A, B = map(int, opt.get("--frames", "1-48").split("-"))
    frames = range(A, B + 1)
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(out, f"{f:04d}.png" if "--still" not in opt else f"still_{f}.png")
    bpy.ops.render.render(write_still=True)
    print("FRAME", f, flush=True)
