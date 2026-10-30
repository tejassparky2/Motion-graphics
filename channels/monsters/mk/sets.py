"""Sets for the monster series (toon look). crater_meadow(): the pastel meadow with the smoking crater the puff-shrimp
blasted, broken stumps behind it and the surviving forest beyond."""
import math
import random

import bpy

from . import look


def _sphere(name, loc, scale, mat, line=0.02, seg=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return look.outline(o, line)


def crater_meadow(seed=4, smoke=True):
    hx = look.hexc
    P = look.paint                                             # painted background: no lines, soft light
    grass, dirt, scorch = P("grass", hx("#79c95f"), noise=0.12, scale=1.2), P("dirt", hx("#b0835a")), \
        P("scorch", hx("#6e4a35"), noise=0.15, scale=2.0)
    rock, trunk = P("rock", hx("#b9b2c4")), P("trunk", hx("#8a5a3b"))
    leaves = [P("leaf0", hx("#4fb35a")), P("leaf1", hx("#ffb347")), P("leaf2", hx("#ff8fa3")), P("leaf3", hx("#3f9e6a"))]
    far_leaves = [P("fleaf0", hx("#7fc79a")), P("fleaf1", hx("#ffc985")), P("fleaf2", hx("#ffb3c1")),
                  P("fleaf3", hx("#79b8a0"))]
    tufts = [P("tuft0", hx("#5fbf55")), P("tuft1", hx("#8edc72"))]
    flowers = [P("fl0", hx("#ffe066")), P("fl1", hx("#ff8fb1")), P("fl2", hx("#ffffff"))]
    cloud = P("cloud", hx("#e9f3ff"), top=hx("#ffffff"), noise=0.0)
    crack = look.flat("crack", hx("#3b2a24"))
    bpy.ops.mesh.primitive_plane_add(size=160)
    bpy.context.object.data.materials.append(grass)
    _sphere("crater", (0, 0.2, -0.02), (4.2, 3.6, 0.06), scorch, 0, 64)
    bpy.ops.mesh.primitive_torus_add(major_radius=4.2, minor_radius=0.42, location=(0, 0.2, 0))
    rim = bpy.context.object
    rim.scale = (1.0, 0.86, 0.55)
    bpy.ops.object.transform_apply(scale=True)
    rim.data.materials.append(dirt)
    for p in rim.data.polygons:
        p.use_smooth = True

    rnd = random.Random(seed)
    for i in range(7):
        a = 0.12 * math.pi + i / 6 * 0.76 * math.pi
        bpy.ops.mesh.primitive_cube_add(location=(math.cos(a) * 5.0, 0.2 + math.sin(a) * 4.35, 0.01), rotation=(0, 0, a))
        c = bpy.context.object
        c.scale = (0.55, 0.04, 0.01)
        bpy.ops.object.transform_apply(scale=True)
        c.data.materials.append(crack)
    for i in range(18):
        a = i / 18 * 2 * math.pi + rnd.uniform(-0.1, 0.1)
        r = rnd.uniform(3.9, 4.6)
        s = rnd.uniform(0.25, 0.55)
        _sphere(f"rock{i}", (math.cos(a) * r, 0.2 + math.sin(a) * r * 0.86, s * 0.3), (s, s * 0.8, s * 0.6), rock, 0,
                12, (rnd.random(), rnd.random(), rnd.random()))
    for i in range(160):
        x, y = rnd.uniform(-9, 9), rnd.uniform(-6, 14)
        if (x / 4.9) ** 2 + ((y - 0.2) / 4.3) ** 2 < 1:
            continue
        if rnd.random() < 0.75:
            bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.12, depth=0.35, location=(x, y, 0.17))
            bpy.context.object.data.materials.append(rnd.choice(tufts))
        else:
            _sphere(f"fl{i}", (x, y, 0.12), (0.1, 0.1, 0.06), rnd.choice(flowers), 0, 10)
    for i in range(10):
        a = rnd.uniform(0.15 * math.pi, 0.85 * math.pi)
        r = rnd.uniform(5.2, 8)
        bpy.ops.mesh.primitive_cylinder_add(radius=rnd.uniform(0.18, 0.3), depth=rnd.uniform(0.3, 0.8),
                                            location=(math.cos(a) * r, 2 + math.sin(a) * r, 0.2), vertices=12)
        o = bpy.context.object
        o.data.materials.append(trunk)
    for i in range(70):
        x, y, s = rnd.uniform(-22, 22), rnd.uniform(13, 40), rnd.uniform(1.1, 2.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * s, depth=1.2 * s, location=(x, y, 0.6 * s), vertices=10)
        o = bpy.context.object
        o.data.materials.append(trunk)
        far = y > 26                                           # distant trees fade paler (atmospheric perspective)
        _sphere(f"tree{i}", (x, y, 1.9 * s), (1.1 * s, 1.1 * s, 1.0 * s), rnd.choice(far_leaves if far else leaves), 0, 20)
    for i in range(7):                                         # big cumulus clouds far behind
        cx, cz = rnd.uniform(-60, 60), rnd.uniform(18, 34)
        for j in range(6):
            r = rnd.uniform(4, 8)
            _sphere(f"cloud{i}_{j}", (cx + rnd.uniform(-9, 9), 110 + rnd.uniform(-5, 5), cz + rnd.uniform(-2, 4)),
                    (r * 1.4, r, r), cloud, 0, 20)
    puffs = []
    if smoke:
        sm = look.fade("smoke", hx("#f2ece6"), 0.4)
        for i in range(9):
            a = rnd.uniform(0.1 * math.pi, 0.9 * math.pi)
            r = rnd.uniform(2.6, 4.2)
            s = rnd.uniform(0.35, 0.7)
            puffs.append(_sphere(f"smoke{i}", (math.cos(a) * r, 0.5 + math.sin(a) * r, 0.5 + rnd.uniform(0, 2.2)),
                                 (s, s, s * 0.8), sm, 0, 16))
    return dict(smoke=puffs)
