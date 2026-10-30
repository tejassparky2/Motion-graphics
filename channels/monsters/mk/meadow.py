"""The puff-shrimp's meadow (Episode 1 S01, S15-S18; Episode 2): ONE set in two states that share every position, so
the before and after shots cut together.

    build("before") : the puddle it drinks from, the forest wall right behind it (the trees the snap erases), far forest
    build("after")  : a crater where the puddle was; where the forest wall stood, a field of cleanly sliced stumps with
                      glowing cut tops on a scorched fan of ground; smoke; the far forest survives

Returns dict(trees=[(trunk, canopy), ...] (before), stumps=[...] (after), smoke_sources=[(x, y, z), ...] (after),
puddle=obj or None). The creature stands at the origin facing -Y; cameras look along +Y.
Painted background look (paintbg): no outlines, three painted bands, far things paler and bluer.
"""
import math
import random

import bpy

from . import anim, look, paintbg

WALL_SEED = 21
TREE = 4.5      # creature units (1 unit = 20 cm): Kai is ~8.7 units, so real trees are ~25-35 units (5-7 m) tall


def _wall_spots():
    """Where the forest wall stands (the same spots become stumps in the 'after' state)."""
    rnd = random.Random(WALL_SEED)
    spots = []
    for row, (y0, n) in enumerate(((6.0, 7), (8.5, 9), (12.0, 10), (15.5, 11))):
        for i in range(n):
            x = -15 + i * 30 / (n - 1) + rnd.uniform(-1.0, 1.0) + (row % 2) * 1.4
            y = y0 + rnd.uniform(-1.0, 1.0)
            # spread out by TREE so the trunks keep their spacing at the bigger size; the first row starts ~10 units
            # behind the creature
            spots.append((x * TREE * 0.7, 4 + (y - 4) * TREE, rnd.uniform(5.5, 7.5) * TREE, rnd.uniform(2.0, 2.8) * TREE,
                          i % 4))
    return spots


def _cyl(loc, r, depth, mat, verts=14):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc)
    o = bpy.context.object
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _ground():
    bpy.ops.mesh.primitive_plane_add(size=1200)
    bpy.context.object.data.materials.append(paintbg.grass_material())


def _far_forest():
    rnd = random.Random(5)
    for i in range(14):
        x = (-36 + i * 5.6 + rnd.uniform(-1.5, 1.5)) * TREE
        paintbg.tree((x, (34 + rnd.uniform(-3, 3)) * TREE, 0), height=rnd.uniform(8, 11) * TREE,
                     radius=rnd.uniform(3.2, 4.2) * TREE, seed=40 + i, variant=i % 4, far=0.45, res=0.2 * TREE)


def _flowers(avoid_r, seed=9, n=40):
    """Small painted flower dots and rounded bushes in the near grass (gives scale and colour)."""
    rnd = random.Random(seed)
    cols = [paintbg.paint3(f"flower{j}", *(look.hexc(c) for c in cs), noise=0.05) for j, cs in enumerate((
        ("#d9a400", "#ffd23f", "#fff2a8"), ("#d05a8a", "#ff8fb8", "#ffd0e2"), ("#c9c9e0", "#ffffff", "#ffffff")))]
    bush = paintbg.paint3("bush", *paintbg.greens(1), noise=0.15)
    for _ in range(n):
        x, y = rnd.uniform(-7, 7), rnd.uniform(-5, 7)
        if math.hypot(x, y * 1.15) < avoid_r:
            continue
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, location=(x, y, 0.08))
        o = bpy.context.object
        o.scale = (0.12, 0.12, 0.07)
        o.data.materials.append(rnd.choice(cols))
    for _ in range(7):
        x, y = rnd.choice((-1, 1)) * rnd.uniform(4.5, 8), rnd.uniform(2, 7)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=(x, y, 0.2))
        o = bpy.context.object
        s = rnd.uniform(0.5, 0.9)
        o.scale = (s * 1.3, s, s * 0.75)
        o.data.materials.append(bush)
        for p in o.data.polygons:
            p.use_smooth = True


def _puddle(center=(0.1, -1.25), size=(1.5, 0.75), z=0.012, pebbles=True):
    """A painted puddle with two white glints. The creature dips its claw in water before every snap (its tell, the
    key to Episode 2), so a puddle is always beside it, before and after the blast."""
    water = paintbg.paint3("puddle", look.hexc("#4f9fd8"), look.hexc("#7cc4f0"), look.hexc("#c9ecff"), noise=0.25,
                           scale=1.5)
    cx, cy = center
    bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1.0, fill_type="NGON", location=(cx, cy, z))
    p = bpy.context.object
    p.name = "puddle"
    p.scale = (size[0], size[1], 1)
    p.data.materials.append(water)
    shine = look.flat("puddle_shine", look.hexc("#ffffff"))
    for (dx, dy, sx) in ((-0.4, -0.27, 0.23), (0.3, 0.33, 0.12)):
        bpy.ops.mesh.primitive_circle_add(vertices=24, radius=1.0, fill_type="NGON",
                                          location=(cx + dx * size[0], cy + dy * size[1], z + 0.004))
        o = bpy.context.object
        o.scale = (sx * size[0], 0.07 * size[1], 1)
        o.data.materials.append(shine)
    if not pebbles:
        return p
    rock = paintbg.paint3("pebble", look.hexc("#7f7a92"), look.hexc("#aaa6bd"), look.hexc("#d6d3e3"), noise=0.1)
    rnd = random.Random(3)
    for i in range(9):
        a = i / 9 * 2 * math.pi + rnd.uniform(-0.2, 0.2)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6,
                                             location=(0.1 + math.cos(a) * 1.6, -1.25 + math.sin(a) * 0.82, 0.05))
        o = bpy.context.object
        s = rnd.uniform(0.09, 0.17)
        o.scale = (s * 1.3, s, s * 0.7)
        o.data.materials.append(rock)
    return p


def _crater():
    dirt = paintbg.paint3("crater_dirt", look.hexc("#4a3024"), look.hexc("#6e4a34"), look.hexc("#93694a"))
    lip = paintbg.paint3("crater_lip", look.hexc("#6e5034"), look.hexc("#a07a52"), look.hexc("#c9a274"))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(0, 0.1, -0.02))
    o = bpy.context.object
    o.scale = (3.4, 2.9, 0.05)
    o.data.materials.append(dirt)
    bpy.ops.mesh.primitive_torus_add(major_radius=3.4, minor_radius=0.34, location=(0, 0.1, 0))
    o = bpy.context.object
    o.scale = (1.0, 0.85, 0.5)
    o.data.materials.append(lip)
    for p in o.data.polygons:
        p.use_smooth = True
    rock = paintbg.paint3("crater_rock", look.hexc("#6f6a80"), look.hexc("#9a95ad"), look.hexc("#c8c4d8"), noise=0.1)
    rnd = random.Random(11)
    for i in range(16):
        a = i / 16 * 2 * math.pi + rnd.uniform(-0.12, 0.12)
        r = rnd.uniform(3.55, 4.1)
        if math.sin(a) < -0.35:                                # keep the camera side of the rim clear
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, location=(math.cos(a) * r, 0.1 + math.sin(a) * r * 0.85,
                                                                         0.1))
        o = bpy.context.object
        s = rnd.uniform(0.15, 0.32)
        o.scale = (s * 1.2, s, s * 0.7)
        o.rotation_euler = (rnd.random(), rnd.random(), rnd.random())
        o.data.materials.append(rock)


def _slice(loc, r, h, tilt, yaw, bark, ring, core):
    """A trunk cut clean by the blast: the cut face slants toward the creature (origin) and glows like hot metal."""
    import bmesh
    me = bpy.data.meshes.new("stump")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=r * 1.08, radius2=r, depth=h)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, h / 2))
    for v in bm.verts:                                         # slant the top: lower toward the creature
        if v.co.z > h * 0.5:
            v.co.z += v.co.y * math.tan(tilt)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("stump", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (0, 0, yaw)
    o.data.materials.append(bark)
    for p in o.data.polygons:
        p.use_smooth = True
    for rr, m, dz in ((r * 0.93, ring, 0.006), (r * 0.55, core, 0.012)):
        bpy.ops.mesh.primitive_circle_add(vertices=24, radius=rr, fill_type="NGON", location=(0, 0, 0))
        c = bpy.context.object
        c.data.materials.append(m)
        c.rotation_euler = (tilt, 0, 0)
        c.location = (0, 0, h + dz)
        c.parent = o
    return o


def _stumps(spots):
    """The erased forest: every tree sliced clean, the slanted cuts facing the creature and glowing like hot metal."""
    bark = paintbg.paint3("stump_bark", look.hexc("#3c261c"), look.hexc("#5e3e2c"), look.hexc("#80604a"), noise=0.12)
    ring = look.flat("stump_hot", look.hexc("#ff7a3d"))
    core = look.flat("stump_core", look.hexc("#ffe08a"))
    scorch = paintbg.paint3("scorch", look.hexc("#3a2c2a"), look.hexc("#54403a"), look.hexc("#6e5648"), noise=0.3,
                            scale=0.8)
    bpy.ops.mesh.primitive_circle_add(vertices=64, radius=1.0, fill_type="NGON", location=(0, 4 + 7.5 * TREE, 0.006))
    fan = bpy.context.object
    fan.name = "scorched_fan"
    fan.scale = (21 * TREE * 0.75, 8.5 * TREE, 1)
    fan.data.materials.append(scorch)
    rnd = random.Random(WALL_SEED + 1)
    stumps, smoke = [], []
    for (x, y, h, r, v) in spots:
        tr = r * 0.17
        sh = rnd.uniform(0.6, 1.7) * TREE * 0.6
        yaw = math.atan2(y, x) - math.pi / 2                    # local +Y points away from the creature
        s = _slice((x, y, 0), tr, sh, math.radians(rnd.uniform(28, 40)), yaw, bark, ring, core)
        stumps.append(s)
        if rnd.random() < 0.5:
            smoke.append((x, y, sh))
    for _ in range(26):                                        # sliced undergrowth between the stumps
        x, y = rnd.uniform(-17, 17) * TREE * 0.7, 4 + rnd.uniform(1.5, 13) * TREE
        _slice((x, y, 0), rnd.uniform(0.05, 0.12) * TREE, rnd.uniform(0.1, 0.3) * TREE, math.radians(30),
               math.atan2(y, x) - math.pi / 2, bark, ring, core)
    return stumps, smoke


def drips(origin, f0, f1, every=14, fall=3.4, seed=2):
    """Water drops falling from the claw tip into the puddle (the tell, shown quietly)."""
    rnd = random.Random(seed)
    m = look.flat("drip", look.hexc("#9fd8ff"))
    f = f0
    while f < f1:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.05, location=origin)
        d = bpy.context.object
        d.data.materials.append(m)
        anim.key(d, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(d, "scale", f, (0.8, 0.8, 1.3), "CONSTANT")
        anim.key(d, "location", f, origin)
        t = max(4, int(round((2 * fall / 9.8) ** 0.5 * 24)))
        anim.key(d, "location", f + t, (origin[0], origin[1], origin[2] - fall), "LINEAR")
        anim.key(d, "scale", f + t, 0.001, "CONSTANT")
        f += every + rnd.randint(-4, 4)


def smoke_mat():
    return paintbg.paint3("smoke", look.hexc("#b3a9c6"), look.hexc("#dcd5e6"), look.hexc("#f7f3f2"), cuts=(0.3, 0.62),
                          noise=0.06, scale=2.0)


def smoke(sources, f0, f1, every=12, rise=3.0, size=0.8, seed=1):
    """Painted smoke puffs that bud from each source, rise, swell and shrink away (no alpha: anime smoke breaks up)."""
    rnd = random.Random(seed)
    m = smoke_mat()
    puffs = []
    for si, (x, y, z) in enumerate(sources):
        f = f0 - rnd.randint(0, every * 3)
        while f < f1:
            life = rnd.randint(30, 44)
            p = bpy.data.objects.new("puff", None)
            bpy.context.scene.collection.objects.link(p)
            p.location = (x, y, z)
            for k in range(4):                                 # a cluster of round lobes reads as an anime cloud
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8,
                                                     location=(rnd.uniform(-0.6, 0.6), rnd.uniform(-0.3, 0.3),
                                                               rnd.uniform(-0.2, 0.5)), radius=rnd.uniform(0.55, 0.9))
                lobe = bpy.context.object
                lobe.data.materials.append(m)
                for pg in lobe.data.polygons:
                    pg.use_smooth = True
                lobe.parent = p
            s = size * rnd.uniform(0.7, 1.3)
            dx = rnd.uniform(-0.4, 0.4)
            anim.key(p, "scale", f - 1, 0.001, "CONSTANT")
            anim.key(p, "scale", f, s * 0.3, "LINEAR")
            anim.key(p, "location", f, (x, y, z))
            anim.key(p, "scale", f + life * 0.6, s)
            anim.key(p, "scale", f + life, 0.001)
            anim.key(p, "location", f + life, (x + dx, y + rnd.uniform(-0.2, 0.2), z + rise * rnd.uniform(0.8, 1.2)))
            puffs.append(p)
            f += every + rnd.randint(-3, 3)
    return puffs


def build(state="before", sky=True):
    """Cameras in this set need clip_end >= 1000 (the far forest stands ~150 units away)."""
    if sky:
        paintbg.sky()
    look.sun(elev=45, azim=-30)
    _ground()
    _far_forest()
    spots = _wall_spots()
    out = dict(trees=[], stumps=[], smoke_sources=[], puddle=None)
    if state == "before":
        out["puddle"] = _puddle()
        for i, (x, y, h, r, v) in enumerate(spots):
            out["trees"].append(paintbg.tree((x, y, 0), height=h, radius=r, seed=100 + i, variant=v))
        _flowers(2.6)
    else:
        _crater()
        out["puddle"] = _puddle(center=(-1.3, -0.4), size=(0.85, 0.45), z=0.04, pebbles=False)
        out["stumps"], hot = _stumps(spots)
        out["smoke_sources"] = hot[:7]
        out["rim_smoke"] = [(-2.4, 2.2, 0.15), (2.6, 1.8, 0.15), (-0.6, 3.1, 0.1)]
        _flowers(4.4, n=24)
    return out
