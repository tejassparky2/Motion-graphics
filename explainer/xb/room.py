"""A cosy living-room set seen behind the character (back wall at +Y, character at the origin facing -Y)."""
import math

import bpy
import numpy as np

from pb import util
from pb.nodes import new_material

WALL_Y = 2.0


def _mat_wall():
    m, n = new_material("Wall")
    co = n.texcoord('Object')
    nz = n.noise(co, scale=3.0, detail=4.0)
    fine = n.noise(co, scale=180.0, detail=2.0)
    base = n.mix(n.math('MULTIPLY', nz.outputs['Fac'], 0.25), (0.60, 0.56, 0.50), (0.52, 0.49, 0.44))
    bsdf = n.principled(base=base, roughness=0.85,
                        normal=n.bump(fine.outputs['Fac'], strength=0.04, distance=0.002))
    n.out(bsdf)
    return m


def _mat_floor():
    m, n = new_material("Floor")
    co = n.texcoord('Object')
    brick = n.node('ShaderNodeTexBrick', Vector=co, Scale=1.0, Mortar_Size=0.004, Bias=0.0,
                   Brick_Width=1.4, Row_Height=0.16,
                   Color1=(0.33, 0.20, 0.11), Color2=(0.42, 0.27, 0.15), Mortar=(0.08, 0.05, 0.03))
    brick.offset = 0.37
    brick.squash = 1.0
    grain = n.wave(n.mapping(co, scale=(1.0, 14.0, 1.0)), scale=3.0, dist=6.0, detail=3.0, axis='X')
    col = n.mix(n.math('MULTIPLY', grain.outputs['Fac'], 0.35), brick.outputs['Color'], (0.18, 0.10, 0.05),
                blend='MULTIPLY')
    bsdf = n.principled(base=col, roughness=0.35, coat=0.3, coat_rough=0.15,
                        normal=n.bump(brick.outputs['Fac'], strength=0.3, distance=0.002))
    n.out(bsdf)
    return m


def _simple(name, col, rough=0.5, **kw):
    m, n = new_material(name)
    n.out(n.principled(base=col, roughness=rough, **kw))
    return m


def _mat_sky():
    m, n = new_material("WindowSky")
    co = n.texcoord('Object')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=co)
    grad = n.ramp(n.maprange(sep.outputs['Z'], 0.0, 3.0), [(0.0, (0.75, 0.86, 0.80)), (0.45, (0.85, 0.92, 1.0)),
                                                         (1.0, (0.62, 0.78, 1.0))])
    # blurry tree canopy blobs in the lower part of the view
    trees = n.noise(n.mapping(co, scale=(1.2, 1.2, 1.6)), scale=2.5, detail=4.0, rough=0.6)
    mask = n.math('MULTIPLY', n.maprange(trees.outputs['Fac'], 0.48, 0.56),
                  n.maprange(sep.outputs['Z'], 2.2, 1.0))
    col = n.mix(mask, grad, (0.16, 0.30, 0.12))
    em = n.node('ShaderNodeEmission', Color=col, Strength=3.0)
    n.out(em)
    return m


def _mat_poster():
    m, n = new_material("Poster")
    uv = n.texcoord('UV')
    # bold mid-century print: a sun disc over layered hills
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    d = n.vmath('DISTANCE', uv, (0.62, 0.62, 0.0))
    sun = n.maprange(d.outputs['Value'] if hasattr(d, 'outputs') else d, 0.17, 0.16)
    hill1 = n.maprange(n.math('SUBTRACT', sep.outputs['Y'],
                              n.math('MULTIPLY', n.math('SINE', n.math('MULTIPLY', sep.outputs['X'], 5.0)), 0.06)),
                       0.36, 0.35)
    hill2 = n.maprange(n.math('SUBTRACT', sep.outputs['Y'],
                              n.math('MULTIPLY', n.math('COSINE', n.math('MULTIPLY', sep.outputs['X'], 3.0)), 0.05)),
                       0.22, 0.21)
    col = n.mix(sun, (0.93, 0.86, 0.72), (0.90, 0.42, 0.20))
    col = n.mix(hill1, col, (0.20, 0.38, 0.40))
    col = n.mix(hill2, col, (0.10, 0.20, 0.25))
    n.out(n.principled(base=col, roughness=0.6))
    return m


def _mat_lampshade():
    m, n = new_material("LampShade")
    bsdf = n.principled(base=(0.95, 0.90, 0.80), roughness=0.8, transmission=0.0,
                        emission=(1.0, 0.75, 0.45), emission_strength=1.5)
    n.out(bsdf)
    return m


def _mat_leaf():
    m, n = new_material("Leaf")
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    vein = n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', sep.outputs['Y'], 0.5)), 0.0, 0.04)
    col = n.mix(vein, (0.25, 0.42, 0.12), (0.10, 0.26, 0.07))
    bsdf = n.principled(base=col, roughness=0.45, sheen=0.2)
    tr = n.node('ShaderNodeBsdfTranslucent', Color=(0.25, 0.45, 0.08))
    mix = n.node('ShaderNodeMixShader', Fac=0.25)
    n.link(bsdf.outputs[0], mix.inputs[1])
    n.link(tr.outputs[0], mix.inputs[2])
    n.out(mix)
    return m


def _mat_curtain():
    m, n = new_material("Curtain")
    co = n.texcoord('Object')
    weave = n.noise(co, scale=400.0, detail=1.0)
    bsdf = n.principled(base=(0.86, 0.82, 0.74), roughness=0.9, sheen=0.5,
                        normal=n.bump(weave.outputs['Fac'], strength=0.05, distance=0.001))
    tr = n.node('ShaderNodeBsdfTranslucent', Color=(0.9, 0.85, 0.75))
    mix = n.node('ShaderNodeMixShader', Fac=0.35)
    n.link(bsdf.outputs[0], mix.inputs[1])
    n.link(tr.outputs[0], mix.inputs[2])
    n.out(mix)
    return m


def _box(mb, size, center, mat):
    v, f, uv = util.box(size, center)
    mb.add(v, f, uv=uv, mat=mat)


def build_walls(coll):
    wall, base, frame = _mat_wall(), _simple("Baseboard", (0.85, 0.84, 0.80), 0.4), _simple("WindowFrame", (0.92, 0.92, 0.90), 0.35)
    mb = util.MeshBuilder()
    t = 0.12
    y = WALL_Y + t / 2
    # back wall with a window hole at x in [-1.75, -0.55], z in [0.85, 2.25]
    wx0, wx1, wz0, wz1 = -1.75, -0.55, 0.85, 2.25
    _box(mb, (wx0 + 3.5, t, 2.9), ((-3.5 + wx0) / 2, y, 1.45), 0)
    _box(mb, (3.5 - wx1, t, 2.9), ((wx1 + 3.5) / 2, y, 1.45), 0)
    _box(mb, (wx1 - wx0, t, wz0), ((wx0 + wx1) / 2, y, wz0 / 2), 0)
    _box(mb, (wx1 - wx0, t, 2.9 - wz1), ((wx0 + wx1) / 2, y, (wz1 + 2.9) / 2), 0)
    # side wall on the right (bounce light) and ceiling
    _box(mb, (t, 6.0, 2.9), (2.6, -1.0, 1.45), 0)
    _box(mb, (7.0, 7.0, t), (0, -1.0, 2.9 + t / 2), 0)
    # baseboards
    _box(mb, (7.0, 0.02, 0.1), (0, WALL_Y - 0.01, 0.05), 1)
    _box(mb, (0.02, 6.0, 0.1), (2.53, -1.0, 0.05), 1)
    # window frame, sill and mullions
    fw = 0.06
    _box(mb, (wx1 - wx0 + 0.12, 0.2, 0.05), ((wx0 + wx1) / 2, WALL_Y - 0.04, wz0 - 0.01), 2)
    for x in (wx0 + fw / 2, wx1 - fw / 2, (wx0 + wx1) / 2):
        _box(mb, (fw if x != (wx0 + wx1) / 2 else 0.04, 0.1, wz1 - wz0), (x, y, (wz0 + wz1) / 2), 2)
    for z in (wz0 + fw / 2, wz1 - fw / 2, wz0 + (wz1 - wz0) * 0.62):
        _box(mb, (wx1 - wx0, 0.1, fw if z in (wz0 + fw / 2, wz1 - fw / 2) else 0.04), ((wx0 + wx1) / 2, y, z), 2)
    ob = mb.build("Walls", coll, mats=[wall, base, frame], smooth=False)
    # floor
    v, f, uv = util.box((7.0, 7.0, 0.02), (0, -1.0, -0.01))
    util.make_mesh("Floor", v, f, coll=coll, smooth=False, mat=_mat_floor())
    # view outside
    sky = util.make_mesh("Outside", np.array([[-4, 5, -1], [3, 5, -1], [3, 5, 4], [-4, 5, 4]], float),
                         [[0, 1, 2, 3]], coll=coll, smooth=False, mat=_mat_sky())
    sky.visible_shadow = False
    # curtains: gathered folds either side of the window
    cm = _mat_curtain()
    for x0, x1 in ((wx0 - 0.28, wx0 + 0.12), (wx1 - 0.12, wx1 + 0.28)):
        nu, nv = 60, 30
        u = np.linspace(0, 1, nu)
        zz = np.linspace(0.05, 2.55, nv)
        V = []
        for z in zz:
            for s in u:
                x = x0 + (x1 - x0) * s
                yy = WALL_Y - 0.12 - 0.035 * math.sin(s * 9 * math.pi + z * 0.4) * (0.7 + 0.3 * z / 2.5)
                V.append((x, yy, z))
        F = util.grid_faces(nv, nu)
        c = util.make_mesh("Curtain", np.array(V), F, coll=coll, mat=cm)
        sol = c.modifiers.new("Thick", 'SOLIDIFY')
        sol.thickness = 0.004
    # curtain rod
    v, f, uv = util.sweep(np.array([[wx0 - 0.4, WALL_Y - 0.12, 2.58], [wx1 + 0.4, WALL_Y - 0.12, 2.58]]),
                          radius=0.012, sides=10)
    util.make_mesh("CurtainRod", v, f, coll=coll, mat=_simple("Brass", (0.75, 0.55, 0.3), 0.3, metallic=1.0))
    return ob


def build_shelf(coll, rng):
    wood = _simple("ShelfWood", (0.45, 0.30, 0.18), 0.45)
    book_mats = [_simple(f"Book{i}", c, 0.55) for i, c in enumerate(
        [(0.55, 0.12, 0.10), (0.12, 0.25, 0.45), (0.85, 0.70, 0.35), (0.20, 0.40, 0.30),
         (0.88, 0.86, 0.80), (0.10, 0.10, 0.12), (0.70, 0.35, 0.20), (0.45, 0.55, 0.65)])]
    mb = util.MeshBuilder()
    x0, x1, y0, depth = 0.55, 1.55, WALL_Y - 0.32, 0.30
    levels = [0.05, 0.45, 0.85, 1.25, 1.65, 2.0]
    for z in levels:
        _box(mb, (x1 - x0, depth, 0.03), ((x0 + x1) / 2, y0 + depth / 2, z), 0)
    for x in (x0, x1):
        _box(mb, (0.03, depth, 2.0), (x, y0 + depth / 2, 1.0), 0)
    _box(mb, (x1 - x0, 0.01, 2.0), ((x0 + x1) / 2, y0 + depth, 1.0), 0)
    for li, z in enumerate(levels[:-1]):
        x = x0 + 0.03
        while x < x1 - 0.06:
            if rng.random() < 0.12:
                x += rng.uniform(0.08, 0.2)
                continue
            w = rng.uniform(0.02, 0.045)
            h = rng.uniform(0.2, 0.32)
            dpt = rng.uniform(0.15, 0.22)
            lean = 0.0
            mi = 1 + int(rng.integers(len(book_mats)))
            v, f, uv = util.box((w, dpt, h), (0, 0, h / 2))
            if rng.random() < 0.06 and x < x1 - 0.3:
                lean = 0.3
            if lean:
                v = util.transform(v, util.rot_matrix((0, 1, 0), lean))
            v += np.array([x + w / 2, y0 + 0.02 + dpt / 2, z + 0.015])
            mb.add(v, f, uv=uv, mat=mi)
            x += w + 0.002
    ob = mb.build("Bookshelf", coll, mats=[wood] + book_mats, smooth=False)
    bev = ob.modifiers.new("Bevel", 'BEVEL')
    bev.width = 0.003
    bev.segments = 2
    return ob


def build_poster(coll):
    frame = _simple("PosterFrame", (0.05, 0.05, 0.05), 0.4)
    mb = util.MeshBuilder()
    cx, cz, w, h = -0.05, 1.62, 0.55, 0.72
    y = WALL_Y - 0.02
    for (sx, sz, px, pz) in ((w + 0.04, 0.03, cx, cz - h / 2), (w + 0.04, 0.03, cx, cz + h / 2),
                             (0.03, h, cx - w / 2, cz), (0.03, h, cx + w / 2, cz)):
        _box(mb, (sx, 0.03, sz), (px, y, pz), 0)
    mb.build("PosterFrame", coll, mats=[frame], smooth=False)
    v = np.array([[cx - w / 2, y - 0.005, cz - h / 2], [cx + w / 2, y - 0.005, cz - h / 2],
                  [cx + w / 2, y - 0.005, cz + h / 2], [cx - w / 2, y - 0.005, cz + h / 2]])
    util.make_mesh("Poster", v, [[0, 1, 2, 3]], coll=coll, smooth=False,
                   uv=np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float), mat=_mat_poster())


def build_lamp(coll):
    metal = _simple("LampMetal", (0.08, 0.08, 0.08), 0.3, metallic=1.0)
    x, y = 1.95, 1.35
    v, f, uv = util.lathe(np.array([[0.0, 0.0], [0.16, 0.0], [0.16, 0.02], [0.012, 0.03], [0.012, 1.55],
                                    [0.0, 1.56]]), segments=24)
    util.make_mesh("LampPole", v + [x, y, 0], f, coll=coll, mat=metal)
    v, f, uv = util.lathe(np.array([[0.22, 1.42], [0.15, 1.72]]), segments=40)
    shade = util.make_mesh("LampShade", v + [x, y, 0], f, coll=coll, mat=_mat_lampshade())
    sol = shade.modifiers.new("Thick", 'SOLIDIFY')
    sol.thickness = 0.004
    d = bpy.data.lights.new("LampBulb", 'POINT')
    d.energy = 25
    d.color = (1.0, 0.72, 0.42)
    d.shadow_soft_size = 0.05
    o = bpy.data.objects.new("LampBulb", d)
    coll.objects.link(o)
    o.location = (x, y, 1.6)


def build_plant(coll, rng, loc=(-0.25, 1.65, 0.0)):
    pot = _simple("Pot", (0.70, 0.36, 0.22), 0.6)
    v, f, uv = util.lathe(np.array([[0.0, 0.0], [0.11, 0.0], [0.15, 0.32], [0.16, 0.34], [0.13, 0.34],
                                    [0.12, 0.30], [0.0, 0.30]]), segments=36)
    util.make_mesh("Pot", v + np.array(loc), f, coll=coll, mat=pot)
    leaf_m = _mat_leaf()
    mb = util.MeshBuilder()
    for i in range(26):
        ang = rng.uniform(0, 2 * math.pi)
        tilt = rng.uniform(0.25, 1.05)
        L = rng.uniform(0.35, 0.65)
        nu, nv = 14, 5
        V, UV = [], []
        for a in range(nu):
            s = a / (nu - 1)
            width = 0.07 * math.sin(math.pi * min(1.0, s * 1.05)) ** 0.8 * (L / 0.5)
            # stem rises then arches over
            r = L * s * math.sin(tilt) + 0.02
            z = 0.30 + L * s * math.cos(tilt) - 0.25 * L * s * s * math.sin(tilt)
            for b in range(nv):
                t = b / (nv - 1) - 0.5
                fold = 0.012 * abs(t) * 4
                px = r * math.cos(ang) - t * width * math.sin(ang)
                py = r * math.sin(ang) + t * width * math.cos(ang)
                V.append((px + loc[0], py + loc[1], z + fold + loc[2]))
                UV.append((s, b / (nv - 1)))
        F = util.grid_faces(nu, nv)
        mb.add(np.array(V), F, uv=np.array(UV), mat=0)
    mb.build("PlantLeaves", coll, mats=[leaf_m])


def build_lights(coll):
    def area(name, loc, target, energy, size, color, shape='DISK', size_y=None):
        d = bpy.data.lights.new(name, 'AREA')
        d.energy = energy
        d.color = color
        d.shape = shape
        d.size = size
        if size_y:
            d.size_y = size_y
        o = bpy.data.objects.new(name, d)
        coll.objects.link(o)
        o.location = loc
        from mathutils import Vector
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        return o
    window = area("WindowLight", (-1.15, WALL_Y - 0.05, 1.55), (-0.9, -1.0, 1.1), 180, 1.2, (0.88, 0.94, 1.0),
                  shape='RECTANGLE', size_y=1.4)
    key = area("KeyLight", (-1.1, -1.5, 2.2), (0.0, -0.1, 1.45), 110, 1.0, (1.0, 0.93, 0.84))
    fill = area("FillLight", (1.5, -1.4, 1.5), (0.0, 0.0, 1.3), 30, 1.6, (0.86, 0.90, 1.0))
    rim = area("RimLight", (0.9, 1.1, 2.1), (0.0, 0.0, 1.45), 90, 0.6, (1.0, 0.88, 0.72))
    return dict(window=window, key=key, fill=fill, rim=rim)


def build(coll, seed=3):
    rng = np.random.default_rng(seed)
    build_walls(coll)
    build_shelf(coll, rng)
    build_poster(coll)
    build_lamp(coll)
    build_plant(coll, rng)
    return build_lights(coll)
