"""The pier at golden hour: deck, structure, railings, lamps, props, ocean,
shore, distant headland, sky and birds.  World space: deck top at z = 0,
pier runs along +X out to sea, water at z = WATER."""
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector

from . import env_materials as em
from .nodes import new_material, simple_material
from .util import (MeshBuilder, box, catmull, circle_profile, collection, empty, lathe, loft,
                   make_mesh, sweep, transform, uv_sphere, smoothstep)

WATER = -4.6
X0, X1 = -84.0, 168.0          # pier extent
HALF_W = 2.55
RNG = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Deck & structure
# ---------------------------------------------------------------------------

def build_deck(coll, mat):
    mb_v, mb_f, mb_uv, mb_rand = [], [], [], []
    nv = 0
    pitch = 0.152
    x = X0
    k = 0
    while x < X1:
        w = 0.140 + RNG.uniform(-0.002, 0.002)
        split = RNG.choice([-1.1, 0.0, 1.1]) + RNG.uniform(-0.02, 0.02)
        for (y0, y1) in ((-HALF_W, split - 0.004), (split + 0.004, HALF_W)):
            r = RNG.random()
            dz = RNG.uniform(-0.003, 0.002)
            tilt = RNG.uniform(-0.004, 0.004)
            L = y1 - y0
            # 2 x 6 top grid gives a little cupping/warp, plus sides
            ny = 8
            ys = np.linspace(y0, y1, ny)
            xs = np.array([x - w / 2, x + w / 2])
            warp = RNG.uniform(-0.002, 0.002) * np.sin(np.linspace(0, np.pi, ny))
            verts = []
            for yi, yy in enumerate(ys):
                for xi, xx in enumerate(xs):
                    zt = dz + warp[yi] + tilt * (xi - 0.5) - 0.0015 * 0  # top
                    verts.append([xx, yy, zt])
            for yi, yy in enumerate(ys):
                for xi, xx in enumerate(xs):
                    verts.append([xx, yy, dz - 0.05])
            verts = np.array(verts)
            faces = []
            top = 0
            bot = 2 * ny
            for yi in range(ny - 1):
                a, b = 2 * yi, 2 * (yi + 1)
                faces.append([top + a, top + a + 1, top + b + 1, top + b])           # top
                faces.append([bot + a, bot + b, bot + b + 1, bot + a + 1])           # bottom
                faces.append([top + a, top + b, bot + b, bot + a])                   # side -x
                faces.append([top + a + 1, bot + a + 1, bot + b + 1, top + b + 1])   # side +x
            faces.append([top + 0, bot + 0, bot + 1, top + 1])                       # end y0
            e = 2 * (ny - 1)
            faces.append([top + e, top + e + 1, bot + e + 1, bot + e])               # end y1
            uv = np.stack([(verts[:, 1] - y0) / 5.0 + r * 3, (verts[:, 0] - x) / 0.14], 1)
            mb_v.append(verts)
            mb_f.extend([[i + nv for i in f] for f in faces])
            mb_uv.append(uv)
            mb_rand.append(np.full(len(verts), r))
            nv += len(verts)
        x += pitch
        k += 1
    V = np.vstack(mb_v)
    ob = make_mesh("Deck", V, mb_f, coll=coll, uv=np.vstack(mb_uv), mat=mat, smooth=False)
    a = ob.data.attributes.new('board', 'FLOAT', 'POINT')
    a.data.foreach_set('value', np.concatenate(mb_rand).astype(np.float32))
    bev = ob.modifiers.new("Bevel", 'BEVEL')
    bev.width = 0.004
    bev.segments = 1
    bev.limit_method = 'ANGLE'
    return ob


def build_structure(coll, wood, pile_mat):
    mb = MeshBuilder()
    # stringers
    for y in (-2.25, -1.1, 0.0, 1.1, 2.25):
        v, f, uv = box((X1 - X0, 0.09, 0.26), ((X0 + X1) / 2, y, -0.18))
        mb.add(v, f, uv, mat=0)
    # outer fascia boards
    for s in (-1, 1):
        v, f, uv = box((X1 - X0, 0.05, 0.32), ((X0 + X1) / 2, s * (HALF_W + 0.03), -0.12))
        mb.add(v, f, uv, mat=0)
    x = X0 + 2.0
    piles = []
    while x < X1:
        v, f, uv = box((0.32, 2 * HALF_W + 0.5, 0.32), (x, 0, -0.47))
        mb.add(v, f, uv, mat=0)
        for y in (-2.3, -0.78, 0.78, 2.3):
            jx = RNG.uniform(-0.04, 0.04)
            jy = RNG.uniform(-0.04, 0.04)
            path = np.array([[x + jx, y + jy, -0.62], [x + jx * 1.5, y + jy * 1.5, WATER - 6.0]])
            v, f, uv = sweep(path, np.array([0.17, 0.185]), 14, caps=True)
            mb.add(v, f, uv, mat=1)
            piles.append((x + jx, y + jy))
        # X bracing between the outer pairs
        for (ya, yb) in ((-2.3, -0.78), (0.78, 2.3), (-0.78, 0.78)):
            for (za, zb) in ((-0.9, -3.6), (-3.6, -0.9)):
                p0 = np.array([x + 0.2, ya, za])
                p1 = np.array([x + 0.2, yb, zb])
                d = p1 - p0
                prof = np.array([[0.03, 0.10], [-0.03, 0.10], [-0.03, -0.10], [0.03, -0.10]])
                v, f, uv = sweep(np.array([p0, p1]), 1.0, profile=prof, up=np.array([1.0, 0, 0]))
                mb.add(v, f, uv, mat=0)
        x += 6.0
    ob = mb.build("PierStructure", coll, mats=[wood, pile_mat], smooth=False)
    return ob, piles


def build_railings(coll, paint):
    mb = MeshBuilder()
    sp = 2.4
    xs = np.arange(X0 + 0.6, X1, sp)
    for s in (-1, 1):
        y = s * 2.46
        for x in xs:
            v, f, uv = box((0.10, 0.10, 1.10), (x, y, 0.55))
            mb.add(v, f, uv)
            v, f, uv = box((0.13, 0.13, 0.03), (x, y, 1.115))
            mb.add(v, f, uv)
        # rails
        v, f, uv = box((X1 - X0, 0.15, 0.045), ((X0 + X1) / 2, y - s * 0.01, 1.075))
        mb.add(v, f, uv)
        v, f, uv = box((X1 - X0, 0.07, 0.07), ((X0 + X1) / 2, y, 0.95))
        mb.add(v, f, uv)
        v, f, uv = box((X1 - X0, 0.07, 0.06), ((X0 + X1) / 2, y, 0.10))
        mb.add(v, f, uv)
        # balusters
        bx = np.arange(X0 + 0.7, X1, 0.16)
        for x in bx:
            if np.min(np.abs(xs - x)) < 0.08:
                continue
            v, f, uv = box((0.034, 0.034, 0.82), (x, y, 0.53))
            mb.add(v, f, uv)
    ob = mb.build("Railings", coll, mats=[paint], smooth=False)
    bev = ob.modifiers.new("Bevel", 'BEVEL')
    bev.width = 0.006
    bev.segments = 2
    bev.limit_method = 'ANGLE'
    return ob, xs


def lamp_post_geometry():
    """One Victorian lamp post at the origin (base on the deck)."""
    mb = MeshBuilder()
    MI, MG, MB = 0, 1, 2
    prof = np.array([[0.001, 0.0], [0.17, 0.0], [0.17, 0.05], [0.14, 0.07], [0.14, 0.12], [0.11, 0.16],
                     [0.10, 0.30], [0.075, 0.36], [0.085, 0.40], [0.06, 0.45], [0.055, 1.6], [0.07, 1.65],
                     [0.05, 1.70], [0.045, 2.55], [0.065, 2.60], [0.07, 2.66], [0.04, 2.70], [0.04, 2.78],
                     [0.10, 2.80], [0.10, 2.83], [0.001, 2.84]])
    v, f, uv = lathe(prof, 24)
    mb.add(v, f, uv, mat=MI)
    # flutes on the shaft
    for k in range(8):
        a = 2 * np.pi * k / 8
        p0 = np.array([math.cos(a) * 0.055, math.sin(a) * 0.055, 0.5])
        p1 = np.array([math.cos(a) * 0.047, math.sin(a) * 0.047, 1.58])
        v, f, uv = sweep(np.array([p0, p1]), 0.008, 6)
        mb.add(v, f, uv, mat=MI)
    # lantern: tapered hexagonal cage
    z0, z1 = 2.86, 3.30
    for k in range(6):
        a = 2 * np.pi * k / 6
        p0 = np.array([math.cos(a) * 0.11, math.sin(a) * 0.11, z0])
        p1 = np.array([math.cos(a) * 0.15, math.sin(a) * 0.15, z1])
        v, f, uv = sweep(np.array([p0, p1]), 0.008, 6)
        mb.add(v, f, uv, mat=MI)
    gl = np.array([[0.105, z0 + 0.01], [0.145, z1 - 0.01]])
    v, f, uv = lathe(gl, 6)
    mb.add(v, f, uv, mat=MG)
    roof = np.array([[0.17, z1], [0.17, z1 + 0.02], [0.10, z1 + 0.10], [0.03, z1 + 0.16], [0.03, z1 + 0.20],
                     [0.045, z1 + 0.22], [0.001, z1 + 0.26]])
    v, f, uv = lathe(roof, 6)
    mb.add(v, f, uv, mat=MI)
    v, f, uv = uv_sphere(0.045, 16, 8, center=(0, 0, (z0 + z1) / 2))
    mb.add(v, f, uv, mat=MB)
    return mb


def build_lamps(coll, mats, rail_xs):
    iron, glass, bulb = mats
    proto = lamp_post_geometry().build("LampPostProto", coll, mats=[iron, glass, bulb])
    proto.hide_render = True
    proto.hide_viewport = True
    lamps = []
    xs = np.arange(X0 + 4.2, X1 - 2, 16.8)
    for s in (-1, 1):
        for x in xs:
            # snap onto a railing post position
            xr = rail_xs[np.argmin(np.abs(rail_xs - x))]
            ob = bpy.data.objects.new(f"Lamp.{s:+d}.{x:.0f}", proto.data)
            coll.objects.link(ob)
            ob.location = (xr, s * 2.46, 0.0)
            lamps.append(ob)
    return lamps


def bench_geometry():
    mb = MeshBuilder()
    for k in range(4):   # seat slats
        v, f, uv = box((1.6, 0.075, 0.035), (0, -0.20 + k * 0.09, 0.44))
        mb.add(v, f, uv, mat=0)
    for k in range(3):   # back slats, reclined
        c = np.array([0, 0.12 + 0.03 * k, 0.56 + k * 0.11])
        v, f, uv = box((1.6, 0.035, 0.075), c)
        R = np.array(Matrix.Rotation(math.radians(-14), 4, 'X'))
        v = transform(v - c, R) + c
        mb.add(v, f, uv, mat=0)
    for x in (-0.65, 0.65):  # cast iron frames
        pts = np.array([[x, -0.24, 0.0], [x, -0.20, 0.25], [x, -0.24, 0.42], [x, 0.12, 0.44], [x, 0.18, 0.0]])
        v, f, uv = sweep(catmull(pts[:3], 6), 0.018, 8)
        mb.add(v, f, uv, mat=1)
        v, f, uv = sweep(catmull(np.array([[x, 0.20, 0.0], [x, 0.14, 0.30], [x, 0.17, 0.60], [x, 0.22, 0.85]]), 6), 0.018, 8)
        mb.add(v, f, uv, mat=1)
        v, f, uv = sweep(np.array([[x, -0.24, 0.42], [x, 0.16, 0.44]]), 0.016, 8)
        mb.add(v, f, uv, mat=1)
        # scrolled armrest
        arm = catmull(np.array([[x, -0.26, 0.62], [x, -0.10, 0.66], [x, 0.10, 0.64], [x, 0.16, 0.50]]), 6)
        v, f, uv = sweep(arm, 0.016, 8)
        mb.add(v, f, uv, mat=1)
        v, f, uv = sweep(np.array([[x, -0.24, 0.42], [x, -0.26, 0.62]]), 0.014, 8)
        mb.add(v, f, uv, mat=1)
    return mb


def build_benches(coll, wood, iron):
    proto = bench_geometry().build("BenchProto", coll, mats=[wood, iron])
    proto.hide_render = True
    proto.hide_viewport = True
    xs = np.arange(X0 + 12.6, X1 - 4, 16.8)
    for i, x in enumerate(xs):
        s = 1 if i % 2 == 0 else -1
        ob = bpy.data.objects.new(f"Bench.{i}", proto.data)
        coll.objects.link(ob)
        ob.location = (x, s * 2.05, 0.0)
        ob.rotation_euler = (0, 0, 0 if s > 0 else math.pi)


def build_life_rings(coll, ring_mat, rope_mat):
    for i, x in enumerate((19.3, 69.7, 120.1)):
        mb = MeshBuilder()
        prof = circle_profile(16) * np.array([0.055, 0.045])
        a = np.linspace(0, 2 * np.pi, 64, endpoint=False)
        path = np.stack([np.cos(a) * 0.26, np.zeros_like(a), np.sin(a) * 0.26], 1)
        v, f, uv = sweep(path, 1.0, profile=prof, closed=True, up=np.array([0, 1.0, 0]))
        mb.add(v, f, uv, mat=0)
        ring = mb.build(f"LifeRing.{i}", coll, mats=[ring_mat])
        ring.location = (x, 2.39, 0.62)
        mb2 = MeshBuilder()
        rp = catmull(np.array([[0, 0, 0.26], [0.1, -0.02, 0.34], [0.25, -0.02, 0.45], [0.3, 0.0, 0.48]]), 8)
        v, f, uv = sweep(rp, 0.008, 8)
        mb2.add(v, f, uv)
        rr = mb2.build(f"LifeRingRope.{i}", coll, mats=[rope_mat])
        rr.location = ring.location


def build_sign(coll, mats, loc, rot_z):
    """'NO CYCLING ON THE PIER' sign; returns the root empty."""
    board, red, text_mat, post_mat = mats
    root = empty("Sign", coll, loc=loc)
    root.rotation_euler = (0, 0, rot_z)
    mb = MeshBuilder()
    v, f, uv = box((0.08, 0.08, 1.9), (0, 0, 0.95))
    mb.add(v, f, uv, mat=3)
    v, f, uv = box((0.03, 0.92, 0.62), (0.055, 0, 1.55))
    mb.add(v, f, uv, mat=0)
    for (w, h, c) in ((0.92, 0.04, (0.072, 0, 1.84)), (0.92, 0.04, (0.072, 0, 1.26)),
                      (0.035, 0.62, (0.072, -0.44, 1.55)), (0.035, 0.62, (0.072, 0.44, 1.55))):
        v, f, uv = box((0.006, w, h), c)
        mb.add(v, f, uv, mat=1)
    post = mb.build("SignBoard", coll, mats=[board, red, text_mat, post_mat], parent=root)
    lines = [("NO CYCLING", 0.115, 1.66, red), ("ON THE PIER", 0.075, 1.53, text_mat),
             ("By order of the Harbour Master", 0.032, 1.42, text_mat)]
    for txt, size, z, mat in lines:
        cu = bpy.data.curves.new(f"SignText.{txt[:6]}", 'FONT')
        cu.body = txt
        cu.size = size
        cu.align_x = 'CENTER'
        cu.align_y = 'CENTER'
        cu.extrude = 0.002
        ob = bpy.data.objects.new(cu.name, cu)
        coll.objects.link(ob)
        ob.data.materials.append(mat)
        ob.parent = root
        ob.location = (0.073, 0, z)
        ob.rotation_euler = (math.pi / 2, 0, math.pi / 2)
    return root


def build_bollards(coll, iron):
    mb = MeshBuilder()
    prof = np.array([[0.001, 0.0], [0.13, 0.0], [0.12, 0.05], [0.10, 0.30], [0.12, 0.38], [0.14, 0.42],
                     [0.12, 0.47], [0.001, 0.48]])
    for x in np.arange(X0 + 9.0, X1, 12.0):
        for s in (-1, 1):
            v, f, uv = lathe(prof, 20)
            mb.add(v + np.array([x, s * 2.72, -0.12]), f, uv)
    return mb.build("Bollards", coll, mats=[iron])


def build_end_platform(coll, wood, paint):
    """A small wider platform at the seaward end with a flag pole."""
    mb = MeshBuilder()
    v, f, uv = box((6.0, 9.0, 0.06), (X1 + 3.0, 0, -0.03))
    mb.add(v, f, uv, mat=0)
    v, f, uv = box((0.12, 0.12, 9.0), (X1 + 4.5, 0, 4.5))
    mb.add(v, f, uv, mat=1)
    ob = mb.build("EndPlatform", coll, mats=[wood, paint], smooth=False)
    return ob


# ---------------------------------------------------------------------------
# Ocean and land
# ---------------------------------------------------------------------------

def build_ocean(coll, mat, far_mat, center=(40.0, 0.0), tile=50, repeat=4, res=11):
    me = bpy.data.meshes.new("OceanBase")
    ob = bpy.data.objects.new("Ocean", me)
    coll.objects.link(ob)
    ob.location = (center[0], center[1], WATER)
    m = ob.modifiers.new("Ocean", 'OCEAN')
    m.geometry_mode = 'GENERATE'
    m.resolution = res
    m.viewport_resolution = 6
    m.spatial_size = tile
    m.repeat_x = repeat
    m.repeat_y = repeat
    m.wind_velocity = 7.5
    m.wave_scale = 0.75
    m.wave_scale_min = 0.01
    m.choppiness = 0.9
    m.wave_alignment = 0.35
    m.wave_direction = math.radians(200)
    m.depth = 40
    m.spectrum = 'PIERSON_MOSKOWITZ'
    m.use_normals = True
    m.use_foam = True
    m.foam_coverage = 0.25
    m.foam_layer_name = "foam"
    m.random_seed = 3
    ob.data.materials.append(mat)
    sm = ob.modifiers.new("Smooth", 'SUBSURF') if False else None
    # far water to the horizon
    S = 20000.0
    far = make_mesh("OceanFar", np.array([[-S, -S, 0], [S, -S, 0], [S, S, 0], [-S, S, 0]]),
                    [[0, 1, 2, 3]], coll=coll, mat=far_mat)
    far.location = (0, 0, WATER - 0.08)
    return ob, m


def build_shore(coll, sand_mat, hill_mat, bld_mat):
    from .util import grid_faces
    # beach: from the waterline at x=-62 rising to the promenade at x=-110
    nx, ny = 60, 80
    xs = np.linspace(-160, -40, nx)
    ys = np.linspace(-500, 500, ny)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    Z = WATER - 1.0 + (WATER * -1 + 1.0 - 0.2) * smoothstep(-55, -112, X) + 0.25 * np.sin(Y * 0.05)
    # gentle bay curving toward the sea at the sides
    Z -= 0.0
    V = np.stack([X + 0.00012 * Y ** 2, Y, Z], -1).reshape(-1, 3)
    from .util import grid_faces
    beach = make_mesh("Beach", V, grid_faces(nx, ny), coll=coll, mat=sand_mat)
    # hills behind the town
    nx, ny = 40, 120
    xs = np.linspace(-2600, -700, nx)
    ys = np.linspace(-4000, 4000, ny)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    h = (38 + 26 * np.sin(Y * 0.0017 + 1) + 14 * np.sin(Y * 0.006 + 2) + 5 * np.sin(Y * 0.02)) * smoothstep(-700, -1400, X)
    V = np.stack([X + 0.00008 * Y ** 2, Y, h - 1.0], -1).reshape(-1, 3)
    hills = make_mesh("Hills", V, grid_faces(nx, ny), coll=coll, mat=hill_mat)
    # town: a hazy seaside town behind the beach, climbing a gentle slope
    def slope(x, y):
        return 0.075 * np.clip(-x - 300, 0, None) + 3.0 * np.sin(y * 0.01) - 1.0
    nx, ny = 30, 90
    xs = np.linspace(-760, -290, nx)
    ys = np.linspace(-2200, 2200, ny)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    V = np.stack([X, Y, slope(X, Y) - 0.6], -1).reshape(-1, 3)
    make_mesh("TownSlope", V, grid_faces(nx, ny), coll=coll, mat=hill_mat)
    mb = MeshBuilder()
    walls = [(0.80, 0.74, 0.64), (0.76, 0.58, 0.46), (0.82, 0.80, 0.76), (0.58, 0.64, 0.68), (0.80, 0.70, 0.52)]
    for i in range(260):
        y = RNG.uniform(-650, 650)
        x = -320 - RNG.uniform(0, 380) * RNG.uniform(0.3, 1.0)
        w = RNG.uniform(6, 12)
        d = RNG.uniform(6, 10)
        hgt = RNG.uniform(5, 10) * (1.6 if RNG.random() < 0.05 else 1.0)
        base = slope(x, y) - 0.5
        v, f, uv = box((d, w, hgt), (x, y, base + hgt / 2))
        col = walls[RNG.integers(len(walls))]
        mb.add(v, f, uv, wall=col)
        rv = np.array([[x - d / 2, y - w / 2, base + hgt], [x + d / 2, y - w / 2, base + hgt],
                       [x + d / 2, y + w / 2, base + hgt], [x - d / 2, y + w / 2, base + hgt],
                       [x, y - w / 2, base + hgt + 2.5], [x, y + w / 2, base + hgt + 2.5]])
        mb.add(rv, [[0, 1, 4], [3, 5, 2], [0, 4, 5, 3], [1, 2, 5, 4]], wall=(0.35, 0.18, 0.12))
    # palm trees along the promenade
    for i in range(44):
        y = -420 + i * 19 + RNG.uniform(-4, 4)
        x = -305 - RNG.uniform(0, 12)
        hgt = RNG.uniform(8, 12) + slope(x, y)
        z0 = slope(x, y) - 0.5
        trunk = np.array([[x, y, z0], [x + 0.6, y + 0.3, (z0 + hgt) * 0.5], [x + 1.4, y + 0.6, hgt]])
        v, f, uv = sweep(catmull(trunk, 6), np.linspace(0.28, 0.16, 13), 8)
        mb.add(v, f, uv, wall=(0.30, 0.22, 0.14))
        top = trunk[-1]
        for k in range(13):
            a = 2 * np.pi * k / 13 + RNG.uniform(-0.2, 0.2)
            d = np.array([np.cos(a), np.sin(a), 0.0])
            frond = np.array([top, top + d * 1.8 + [0, 0, 0.7], top + d * 3.4 + [0, 0, -0.4], top + d * 4.2 + [0, 0, -1.6]])
            fp = catmull(frond, 5)
            v, f, uv = sweep(fp, np.linspace(0.65, 0.08, len(fp)), profile=np.array([[0, 1.0], [0.08, 0], [0, -1.0], [-0.03, 0]]),
                             up=np.array([0, 0, 1.0]))
            mb.add(v, f, uv, wall=(0.10, 0.16, 0.07))
    town = mb.build("Town", coll, mats=[bld_mat], smooth=False)
    from .util import grid_faces as _gf
    # promenade wall
    v, f, uv = box((4.0, 1000.0, 1.2), (-112.0, 0, -0.6))
    prom = make_mesh("Promenade", v, f, coll=coll, mat=sand_mat, smooth=False)
    return beach, hills, town


def build_headland(coll, hill_mat, paint, glass_emit):
    """Distant headland with a lighthouse, off to the left of the pier."""
    nx, ny = 50, 50
    xs = np.linspace(-1, 1, nx)
    ys = np.linspace(-1, 1, ny)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    r = np.sqrt(X ** 2 + Y ** 2)
    Hh = 70 * np.clip(1 - r, 0, 1) ** 0.8 * (1 + 0.15 * np.sin(X * 9) * np.cos(Y * 7))
    V = np.stack([X * 420 + 420, Y * 260 + 1350, Hh + WATER - 2], -1).reshape(-1, 3)
    from .util import grid_faces
    head = make_mesh("Headland", V, grid_faces(nx, ny), coll=coll, mat=hill_mat)
    top = np.array([420.0 + 60, 1350.0 - 40, WATER - 2 + 70 * 0.88])
    mb = MeshBuilder()
    prof = np.array([[0.001, 0], [5.0, 0], [4.0, 22], [3.2, 22.5], [3.2, 26], [2.4, 26.5], [2.0, 29], [0.001, 30]])
    v, f, uv = lathe(prof, 16)
    mb.add(v + top, f, uv, mat=0)
    v, f, uv = uv_sphere(1.6, 12, 6, center=top + np.array([0, 0, 24.2]))
    mb.add(v, f, uv, mat=1)
    lh = mb.build("Lighthouse", coll, mats=[paint, glass_emit])
    return head


def build_sky(scene, sun_elev_deg=3.6, sun_az_deg=-32.0, strength=0.22):
    """Nishita sky (no disc) + procedural cloud layer + camera-visible sun disc.
    Returns the world and a Sun lamp aligned to the same direction."""
    w = bpy.data.worlds.new("GoldenHour")
    scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    from .nodes import Nodes
    n = Nodes(nt)
    sky = n.node('ShaderNodeTexSky', _props=dict(sky_type='NISHITA', sun_disc=False,
                                                 sun_elevation=math.radians(sun_elev_deg),
                                                 sun_rotation=math.radians(90 + sun_az_deg),
                                                 altitude=10.0, air_density=1.0, dust_density=1.5,
                                                 ozone_density=1.2))
    # direction vector of the background ray
    tc = n.texcoord('Generated')
    d = tc
    sep = n.node('ShaderNodeSeparateXYZ', Vector=d)
    dz = n.math('MAXIMUM', sep.outputs['Z'], 0.015)
    # project onto a cloud plane
    px = n.math('DIVIDE', sep.outputs['X'], dz)
    py = n.math('DIVIDE', sep.outputs['Y'], dz)
    plane = n.node('ShaderNodeCombineXYZ', X=n.math('MULTIPLY', px, 1.0), Y=n.math('MULTIPLY', py, 1.0), Z=0.0)
    warp = n.noise(plane.outputs[0], scale=0.35, detail=2.0)
    pc = n.vmath('ADD', plane.outputs[0], n.vmath('SCALE', warp.outputs['Color'], scale=0.9))
    cl = n.noise(n.mapping(pc, scale=(0.55, 1.6, 1.0)), scale=0.9, detail=6.0, rough=0.62)
    dens = n.maprange(cl.outputs['Fac'], 0.50, 0.70, 0.0, 1.0)
    horizon_fade = n.maprange(sep.outputs['Z'], 0.005, 0.10, 0.0, 1.0)
    high_fade = n.maprange(sep.outputs['Z'], 0.75, 0.35, 0.0, 1.0)
    dens = n.math('MULTIPLY', n.math('MULTIPLY', dens, horizon_fade), high_fade)
    # cloud colour: brighter / warmer toward the sun
    sun_dir = (math.cos(math.radians(sun_elev_deg)) * math.cos(math.radians(sun_az_deg)),
               math.cos(math.radians(sun_elev_deg)) * math.sin(math.radians(sun_az_deg)),
               math.sin(math.radians(sun_elev_deg)))
    cosang = n.vmath('DOT_PRODUCT', d, sun_dir)
    toward = n.maprange(cosang, -0.2, 1.0, 0.0, 1.0)
    cloud_col = n.ramp(toward, [(0.0, (0.62, 0.42, 0.50)), (0.45, (0.95, 0.50, 0.36)),
                                (0.80, (1.6, 0.75, 0.35)), (1.0, (4.0, 2.2, 1.0))])
    thick = n.maprange(cl.outputs['Fac'], 0.58, 0.80, 0.0, 1.0)
    cloud_col = n.mix(n.math('MULTIPLY', thick, 0.55), cloud_col,
                      n.mix(toward, (0.30, 0.22, 0.30), (0.55, 0.22, 0.12)))
    # dusk tint away from the sun: lift magenta/blue a touch (Belt of Venus)
    away = n.maprange(cosang, 0.2, -0.6, 0.0, 1.0)
    tinted = n.mix(away, sky.outputs['Color'], n.vmath('MULTIPLY', sky.outputs['Color'], (1.02, 0.86, 1.08)))
    sky_mix = n.mix(dens, tinted, cloud_col)
    # sun disc + glow (camera rays only, the Sun lamp does the lighting)
    disc = n.maprange(cosang, 0.99975, 0.99990, 0.0, 1.0)
    glow = n.math('POWER', n.maprange(cosang, 0.90, 1.0, 0.0, 1.0), 6.0)
    sun_em = n.math('ADD', n.math('MULTIPLY', disc, 900.0), n.math('MULTIPLY', glow, 3.0))
    sun_col = n.mix(0.5, (1.0, 0.55, 0.22), (1.0, 0.75, 0.45))
    lp = n.node('ShaderNodeLightPath')
    cam_only = lp.outputs['Is Camera Ray']
    sun_add = n.vmath('SCALE', sun_col, scale=n.math('MULTIPLY', sun_em, n.math('SUBTRACT', 1.0, n.math('MULTIPLY', dens, 0.85))))
    sun_add = n.vmath('SCALE', sun_add, scale=cam_only)
    col = n.vmath('ADD', sky_mix, sun_add)
    bg = n.node('ShaderNodeBackground', Color=col, Strength=strength)
    out = n.node('ShaderNodeOutputWorld')
    n.link(bg.outputs[0], out.inputs['Surface'])
    # Sun lamp
    sl = bpy.data.lights.new("Sun", 'SUN')
    sl.energy = 4.2
    sl.color = (1.0, 0.55, 0.26)
    sl.angle = math.radians(1.2)
    sun = bpy.data.objects.new("Sun", sl)
    scene.collection.objects.link(sun)
    dv = Vector(sun_dir)
    sun.rotation_euler = (-dv).to_track_quat('-Z', 'Y').to_euler()
    return w, sun, sky


def set_sun(sun, sky_node, elev_deg, az_deg, frame=None):
    """Re-aim sun lamp and sky (optionally keyed at frame, constant interpolation)."""
    sun_dir = Vector((math.cos(math.radians(elev_deg)) * math.cos(math.radians(az_deg)),
                      math.cos(math.radians(elev_deg)) * math.sin(math.radians(az_deg)),
                      math.sin(math.radians(elev_deg))))
    sun.rotation_euler = (-sun_dir).to_track_quat('-Z', 'Y').to_euler()
    sky_node.sun_elevation = math.radians(elev_deg)
    sky_node.sun_rotation = math.radians(90 + az_deg)
    return sun_dir


# ---------------------------------------------------------------------------
# Birds
# ---------------------------------------------------------------------------

def gull_mesh():
    """Low-poly herring gull: body, head, beak; wings separate (flapping)."""
    mb = MeshBuilder()
    rings = []
    for i in range(16):
        t = i / 15
        x = 0.30 - t * 0.55
        r = 0.055 * math.sin(math.pi * min(1, t * 1.1 + 0.05)) ** 0.7 + 0.004
        ring = [[x, math.cos(a) * r, math.sin(a) * r * 0.9] for a in np.linspace(0, 2 * np.pi, 12, endpoint=False)]
        rings.append(ring)
    v, f, uv = loft(np.array(rings), cap_start=True, cap_end=True)
    mb.add(v, f, uv, mat=0)
    v, f, uv = uv_sphere(0.042, 12, 8, center=(0.30, 0, 0.03))
    mb.add(v, f, uv, mat=0)
    v, f, uv = sweep(np.array([[0.33, 0, 0.025], [0.40, 0, 0.018]]), np.array([0.011, 0.003]), 8)
    mb.add(v, f, uv, mat=2)
    wings = []
    for s in (1, -1):
        w = MeshBuilder()
        span = 0.62
        pts = np.array([[0.06, 0, 0], [0.10, s * span * 0.45, 0.01], [0.02, s * span, 0.0],
                        [-0.08, s * span * 0.95, 0.0], [-0.08, s * span * 0.4, 0], [-0.06, 0, 0]])
        tris = [[0, 1, 4, 5], [1, 2, 3, 4]] if s > 0 else [[5, 4, 1, 0], [4, 3, 2, 1]]
        w.add(pts, tris, mat=0)
        tip = np.array([[0.02, s * span, 0.0], [-0.08, s * span * 0.95, 0.0], [-0.03, s * span * 0.75, 0.001],
                        [0.05, s * span * 0.78, 0.001]])
        w.add(tip + np.array([0, 0, 0.001]), [[0, 1, 2, 3]] if s > 0 else [[3, 2, 1, 0]], mat=1)
        wings.append(w)
    return mb, wings


def build_gulls(coll, mats, T, n_fly=7, perched=()):
    """Flying gulls on looping paths + a few perched ones."""
    body_mb, wing_mbs = gull_mesh()
    body_data = body_mb.build("GullBodyProto", coll, mats=mats).data
    wl = wing_mbs[0].build("GullWingLProto", coll, mats=mats).data
    wr = wing_mbs[1].build("GullWingRProto", coll, mats=mats).data
    for nm in ("GullBodyProto", "GullWingLProto", "GullWingRProto"):
        bpy.data.objects[nm].hide_render = True
        bpy.data.objects[nm].hide_viewport = True
    from .anim import bake
    t = T.at_frames(T.t)
    gulls = []
    for i in range(n_fly):
        root = empty(f"Gull.{i}", coll, size=0.2)
        b = bpy.data.objects.new(f"GullBody.{i}", body_data)
        coll.objects.link(b)
        b.parent = root
        L = bpy.data.objects.new(f"GullWingL.{i}", wl)
        R = bpy.data.objects.new(f"GullWingR.{i}", wr)
        for w in (L, R):
            coll.objects.link(w)
            w.parent = root
            w.location = (0.05, 0, 0.02)
        cx = RNG.uniform(10, 90)
        cy = RNG.uniform(-40, 40)
        cz = RNG.uniform(7, 22)
        rad = RNG.uniform(8, 25)
        spd = RNG.uniform(0.25, 0.45) * (1 if RNG.random() < 0.5 else -1)
        ph = RNG.uniform(0, 2 * np.pi)
        ang = ph + spd * t
        x = cx + rad * np.cos(ang)
        y = cy + rad * np.sin(ang)
        z = cz + 1.5 * np.sin(t * 0.5 + ph)
        heading = ang + np.sign(spd) * np.pi / 2
        bank = -np.sign(spd) * 0.35
        for k, arr in enumerate((x, y, z)):
            bake(root, 'location', k, T.frames, arr)
        bake(root, 'rotation_euler', 2, T.frames, heading)
        bake(root, 'rotation_euler', 0, T.frames, np.full_like(t, bank))
        flap_f = RNG.uniform(2.2, 3.0)
        glide = (np.sin(t * 0.6 + ph) > 0.2).astype(float)
        glide = np.convolve(glide, np.ones(12) / 12, mode='same')
        flap = 0.55 * np.sin(2 * np.pi * flap_f * t + ph) * (1 - glide) + 0.08
        bake(L, 'rotation_euler', 0, T.frames, flap)
        bake(R, 'rotation_euler', 0, T.frames, -flap)
        gulls.append(root)
    for i, (loc, rz) in enumerate(perched):
        b = bpy.data.objects.new(f"GullPerched.{i}", body_data)
        coll.objects.link(b)
        b.location = loc
        b.rotation_euler = (0, -0.25, rz)
        for nm, data, s in (("L", wl, 1), ("R", wr, -1)):
            w = bpy.data.objects.new(f"GullPerchedWing{nm}.{i}", data)
            coll.objects.link(w)
            w.parent = b
            w.location = (0.05, 0, 0.03)
            w.rotation_euler = (s * 1.35, 0.0, -s * 0.15)
        # legs
        mb = MeshBuilder()
        for s in (1, -1):
            v, f, uv = sweep(np.array([[0.0, s * 0.02, -0.03], [0.02, s * 0.025, -0.12]]), 0.006, 6)
            mb.add(v, f, uv, mat=2)
        legs = mb.build(f"GullPerchedLegs.{i}", coll, mats=mats)
        legs.parent = b
    return gulls


def build_far_pelicans(coll, mat, T, n=5, start=(150.0, 120.0, 6.0), vel=(-6.5, -1.0, 0.0)):
    """A loose line of pelicans gliding low over the water (silhouettes)."""
    from .anim import bake
    t = T.at_frames(T.t)
    birds = []
    for i in range(n):
        mb = MeshBuilder()
        rings = []
        for k in range(10):
            u = k / 9
            x = 0.45 - u * 1.1
            r = 0.10 * math.sin(math.pi * min(1, u * 1.05 + 0.04)) ** 0.7 + 0.01
            rings.append([[x, math.cos(a) * r, math.sin(a) * r] for a in np.linspace(0, 2 * np.pi, 10, endpoint=False)])
        v, f, uv = loft(np.array(rings), cap_start=True, cap_end=True)
        mb.add(v, f, uv)
        v, f, uv = sweep(np.array([[0.40, 0, 0.05], [0.50, 0, 0.08], [0.58, 0, 0.06]]), np.array([0.05, 0.045, 0.04]), 8)
        mb.add(v, f, uv)
        v, f, uv = sweep(np.array([[0.58, 0, 0.06], [0.98, 0, -0.02]]), np.array([0.025, 0.006]), 8)
        mb.add(v, f, uv)
        for s in (1, -1):
            wpts = np.array([[0.15, 0, 0.02], [0.18, s * 0.7, 0.06], [0.08, s * 1.45, 0.02], [-0.05, s * 1.40, 0.0],
                             [-0.12, s * 0.7, 0.03], [-0.15, 0, 0.0]])
            fl = [[0, 1, 4, 5], [1, 2, 3, 4]] if s > 0 else [[5, 4, 1, 0], [4, 3, 2, 1]]
            mb.add(wpts, fl)
        ob = mb.build(f"FarPelican.{i}", coll, mats=[mat])
        off = np.array([i * 4.5, i * 2.2 * (1 if i % 2 else -1) * 0.5 + i * 1.5, 0.3 * i])
        p0 = np.array(start) + off
        x = p0[0] + vel[0] * t
        y = p0[1] + vel[1] * t
        z = p0[2] + 0.25 * np.sin(t * 0.9 + i)
        for k, arr in enumerate((x, y, z)):
            bake(ob, 'location', k, T.frames, arr)
        ob.rotation_euler = (0, 0, math.atan2(vel[1], vel[0]))
        bake(ob, 'rotation_euler', 0, T.frames, 0.06 * np.sin(t * 0.7 + i))
        birds.append(ob)
    return birds


def build(coll, T):
    wood = em.deck_wood()
    beam = em.painted_wood("BeamWood", (0.24, 0.19, 0.14))
    pile = em.piling()
    paint = em.painted_wood()
    iron = em.cast_iron()
    glass = em.lantern_glass()
    bulb = em.bulb()
    deck = build_deck(coll, wood)
    struct, piles = build_structure(coll, beam, pile)
    rails, rail_xs = build_railings(coll, paint)
    lamps = build_lamps(coll, (iron, glass, bulb), rail_xs)
    build_benches(coll, em.deck_wood("BenchWood"), iron)
    build_life_rings(coll, em.life_ring(), em.rope())
    build_bollards(coll, iron)
    build_end_platform(coll, wood, paint)
    ocean, ocean_mod = build_ocean(coll, em.ocean(), em.ocean_far())
    from .anim import bake
    bake(ocean, 'modifiers["Ocean"].time', -1, T.frames, 20.0 + T.at_frames(T.t))
    build_shore(coll, em.sand(), em.hills(), em.building())
    build_headland(coll, em.hills("FarHills"), paint, bulb)
    return dict(deck=deck, rails=rails, rail_xs=rail_xs, ocean=ocean, lamps=lamps, piles=piles, iron=iron,
                paint=paint, wood=wood)
