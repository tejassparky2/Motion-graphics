"""Materials for the pier, ocean, sky and props."""
import math

HAZE = (0.62, 0.56, 0.66)


def add_haze(n, color_socket, start=120.0, depth=1800.0, amount=0.85):
    """Aerial perspective: blend toward the horizon haze with view distance."""
    cam = n.node('ShaderNodeCameraData')
    d = n.maprange(cam.outputs['View Distance'], start, start + depth, 0.0, amount)
    return n.mix(d, color_socket, HAZE)

from .nodes import new_material, simple_material


def deck_wood(name="DeckWood"):
    """Weathered planks. Uses per-board attributes 'board' (random) and UV (u along board)."""
    m, n = new_material(name)
    obj = n.texcoord('Object')
    uv = n.texcoord('UV')
    rnd = n.attr('board')
    # grain: stretched along the board (UV u), distorted
    gcoord = n.vmath('ADD', n.mapping(uv, scale=(1.0, 14.0, 1.0)),
                     n.node('ShaderNodeCombineXYZ', X=n.math('MULTIPLY', rnd, 37.0), Y=0.0, Z=0.0).outputs[0])
    grain = n.wave(gcoord, scale=1.2, dist=7.0, detail=3.0, axis='Y', kind='BANDS', dscale=1.5)
    fine = n.noise(n.mapping(uv, scale=(3.0, 80.0, 1.0)), scale=4.0, detail=4.0, rough=0.65)
    cracks = n.noise(n.mapping(uv, scale=(0.6, 30.0, 1.0)), scale=6.0, detail=2.0)
    crack = n.maprange(cracks.outputs['Fac'], 0.66, 0.70, 0.0, 1.0)
    big = n.noise(obj, scale=0.35, detail=2.0)
    wet = n.maprange(big.outputs['Fac'], 0.58, 0.68, 0.0, 1.0)
    base = n.ramp(rnd, [(0.0, (0.31, 0.27, 0.23)), (0.35, (0.42, 0.37, 0.31)), (0.7, (0.36, 0.28, 0.21)),
                        (1.0, (0.47, 0.44, 0.40))])
    col = n.mix(n.math('MULTIPLY', grain.outputs['Fac'], 0.45), base, (0.20, 0.16, 0.12))
    col = n.mix(n.math('MULTIPLY', fine.outputs['Fac'], 0.25), col, (0.62, 0.58, 0.52))
    col = n.mix(crack, col, (0.06, 0.05, 0.04))
    col = n.mix(n.math('MULTIPLY', wet, 0.4), col, (0.14, 0.12, 0.10))
    rough = n.mix(wet, n.maprange(fine.outputs['Fac'], 0.3, 0.7, 0.62, 0.85), 0.35, dtype='FLOAT')
    h = n.math('ADD', n.math('MULTIPLY', grain.outputs['Fac'], 0.5), n.math('MULTIPLY', fine.outputs['Fac'], 0.4))
    h = n.math('SUBTRACT', h, crack)
    bump = n.bump(h, strength=0.35, distance=0.0015)
    n.out(n.principled(base=col, roughness=rough, normal=bump, spec=0.35))
    m.diffuse_color = (0.4, 0.35, 0.3, 1)
    return m


def painted_wood(name="RailPaint", color=(0.82, 0.80, 0.74)):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    peel_n = n.noise(obj, scale=9.0, detail=4.0, rough=0.7)
    peel = n.maprange(peel_n.outputs['Fac'], 0.60, 0.63, 0.0, 1.0)
    grain = n.wave(obj, scale=30.0, dist=6.0, detail=2.0, axis='Z')
    wood = n.mix(grain.outputs['Fac'], (0.30, 0.25, 0.20), (0.18, 0.14, 0.11))
    dirt = n.noise(obj, scale=3.0, detail=2.0)
    paint = n.mix(n.maprange(dirt.outputs['Fac'], 0.45, 0.75, 0.0, 0.35), color, (0.55, 0.50, 0.42))
    col = n.mix(peel, paint, wood)
    bump = n.bump(n.math('ADD', peel, n.math('MULTIPLY', peel_n.outputs['Fac'], 0.2)), strength=0.4, distance=0.001)
    n.out(n.principled(base=col, roughness=n.mix(peel, 0.45, 0.8, dtype='FLOAT'), normal=bump))
    m.diffuse_color = (*color, 1)
    return m


def piling(name="Piling"):
    """Creosoted piles: dry above, wet/dark band, algae and barnacles near the water."""
    m, n = new_material(name)
    obj = n.texcoord('Object')
    gen = n.texcoord('Generated')
    z = n.node('ShaderNodeSeparateXYZ', Vector=n.texcoord('Object')).outputs['Z']
    # local z: 0 at the deck, negative going down; water at ~ -4.5
    wl = n.math('ADD', z, 4.5)
    wet = n.maprange(wl, 1.6, 0.4, 0.0, 1.0)
    algae = n.maprange(wl, 0.6, -0.2, 0.0, 1.0)
    grain = n.wave(obj, scale=3.0, dist=12.0, detail=3.0, axis='Z', kind='BANDS', dscale=3.0)
    base = n.mix(grain.outputs['Fac'], (0.22, 0.17, 0.12), (0.10, 0.08, 0.06))
    col = n.mix(wet, base, (0.05, 0.045, 0.035))
    alg = n.mix(n.noise(obj, scale=8.0).outputs['Fac'], (0.08, 0.12, 0.04), (0.03, 0.07, 0.03))
    col = n.mix(algae, col, alg)
    barn = n.voronoi(obj, scale=55.0)
    bmask = n.math('MULTIPLY', n.maprange(barn.outputs['Distance'], 0.0, 0.25, 1.0, 0.0),
                   n.maprange(wl, 1.2, 0.2, 0.0, 1.0))
    col = n.mix(n.math('MULTIPLY', bmask, 0.9), col, (0.55, 0.52, 0.47))
    h = n.math('ADD', n.math('MULTIPLY', grain.outputs['Fac'], 0.4), n.math('MULTIPLY', bmask, 1.5))
    rough = n.mix(wet, 0.8, 0.25, dtype='FLOAT')
    n.out(n.principled(base=col, roughness=rough, normal=n.bump(h, strength=0.6, distance=0.01)))
    m.diffuse_color = (0.15, 0.12, 0.1, 1)
    return m


def cast_iron(name="CastIron", color=(0.035, 0.07, 0.06)):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    rust = n.noise(obj, scale=14.0, detail=3.0, rough=0.7)
    rm = n.maprange(rust.outputs['Fac'], 0.62, 0.70, 0.0, 1.0)
    col = n.mix(rm, color, (0.25, 0.10, 0.04))
    n.out(n.principled(base=col, roughness=n.mix(rm, 0.35, 0.8, dtype='FLOAT'), metallic=n.mix(rm, 0.4, 0.0, dtype='FLOAT'),
                       coat=0.4, coat_rough=0.3,
                       normal=n.bump(rust.outputs['Fac'], strength=0.15, distance=0.002)))
    m.diffuse_color = (*color, 1)
    return m


def lantern_glass(name="LanternGlass"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    frost = n.noise(obj, scale=200.0)
    em = n.node('ShaderNodeEmission', Color=(1.0, 0.62, 0.28), Strength=2.5)
    gl = n.principled(base=(1.0, 0.85, 0.7), roughness=0.25, transmission=1.0, ior=1.45)
    mix = n.node('ShaderNodeMixShader', Fac=0.6)
    n.link(gl.outputs[0], mix.inputs[1])
    n.link(em.outputs[0], mix.inputs[2])
    n.out(mix)
    return m


def bulb(name="Bulb"):
    m, n = new_material(name)
    n.out(n.node('ShaderNodeEmission', Color=(1.0, 0.58, 0.25), Strength=40.0))
    return m


def ocean(name="Ocean"):
    m, n = new_material(name)
    foam_attr = n.attr('foam')
    obj = n.texcoord('Object')
    geo = n.node('ShaderNodeNewGeometry')
    lw = n.node('ShaderNodeLayerWeight', Blend=0.35)
    ripple1 = n.noise(n.mapping(obj, scale=(1.0, 2.2, 1.0)), scale=6.0, detail=3.0, rough=0.55)
    ripple2 = n.noise(obj, scale=28.0, detail=3.0)
    h = n.math('ADD', ripple1.outputs['Fac'], n.math('MULTIPLY', ripple2.outputs['Fac'], 0.35))
    bump = n.bump(h, strength=0.12, distance=0.05)
    foam_noise = n.noise(obj, scale=3.5, detail=3.0, rough=0.7)
    foam = n.math('MULTIPLY', n.maprange(foam_attr, 0.25, 0.75, 0.0, 1.0),
                  n.maprange(foam_noise.outputs['Fac'], 0.42, 0.62, 0.0, 1.0))
    deep = (0.004, 0.032, 0.042)
    shallow = (0.02, 0.11, 0.10)
    body = n.mix(lw.outputs['Facing'], shallow, deep)
    col = n.mix(foam, body, (0.80, 0.82, 0.80))
    water = n.principled(base=col, roughness=n.mix(foam, 0.035, 0.6, dtype='FLOAT'), ior=1.333,
                         spec=0.6, normal=bump, sss=0.0)
    n.out(water)
    m.diffuse_color = (0.02, 0.08, 0.1, 1)
    return m


def ocean_far(name="OceanFar"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    r1 = n.noise(n.mapping(obj, scale=(0.4, 1.0, 1.0)), scale=0.6, detail=4.0, rough=0.6)
    bump = n.bump(r1.outputs['Fac'], strength=0.08, distance=0.3)
    n.out(n.principled(base=(0.004, 0.03, 0.04), roughness=0.05, ior=1.333, spec=0.6, normal=bump))
    return m


def sand(name="Sand"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    nz = n.noise(obj, scale=2.0, detail=3.0)
    col = n.mix(nz.outputs['Fac'], (0.62, 0.52, 0.38), (0.48, 0.40, 0.30))
    n.out(n.principled(base=col, roughness=0.9, normal=n.bump(n.noise(obj, scale=60.0).outputs['Fac'], strength=0.2)))
    return m


def hills(name="Hills"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    nz = n.noise(obj, scale=0.02, detail=3.0, rough=0.6)
    col = n.mix(nz.outputs['Fac'], (0.10, 0.12, 0.07), (0.20, 0.16, 0.10))
    hz = add_haze(n, col)
    cam = n.node('ShaderNodeCameraData')
    glow = n.maprange(cam.outputs['View Distance'], 300.0, 2500.0, 0.0, 0.55)
    n.out(n.principled(base=hz, roughness=0.95, emission=HAZE, emission_strength=glow))
    return m


def building(name="Building"):
    """Facade with procedural windows, some lit."""
    m, n = new_material(name)
    obj = n.texcoord('Object')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=obj)
    gx = n.math('FRACT', n.math('MULTIPLY', n.math('ADD', sep.outputs['X'], sep.outputs['Y']), 0.45))
    gz = n.math('FRACT', n.math('MULTIPLY', sep.outputs['Z'], 0.33))
    win = n.math('MULTIPLY', n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', gx, 0.5)), 0.22, 0.25, 1.0, 0.0),
                 n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', gz, 0.55)), 0.18, 0.21, 1.0, 0.0))
    cell = n.node('ShaderNodeCombineXYZ', X=n.math('FLOOR', n.math('MULTIPLY', n.math('ADD', sep.outputs['X'], sep.outputs['Y']), 0.45)),
                  Y=n.math('FLOOR', n.math('MULTIPLY', sep.outputs['Z'], 0.33)), Z=0.0)
    rnd = n.node('ShaderNodeTexWhiteNoise', _props=dict(noise_dimensions='3D'), Vector=cell.outputs[0])
    lit = n.math('MULTIPLY', win, n.math('GREATER_THAN', rnd.outputs['Value'], 0.82))
    walls = n.attr('wall', out='Color')
    col = n.mix(win, walls, (0.05, 0.06, 0.08))
    col = add_haze(n, col, start=150.0, depth=900.0, amount=0.6)
    em = n.math('MULTIPLY', lit, 2.5)
    n.out(n.principled(base=col, roughness=0.8, emission=(1.0, 0.70, 0.40), emission_strength=em))
    return m


def life_ring(name="LifeRing"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    stripes = n.math('GREATER_THAN', n.math('FRACT', n.math('MULTIPLY', sep.outputs['X'], 4.0)), 0.5)
    col = n.mix(stripes, (0.85, 0.06, 0.03), (0.92, 0.90, 0.85))
    n.out(n.principled(base=col, roughness=0.45, coat=0.4))
    return m


def rope(name="Rope"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    tw = n.wave(n.mapping(uv, scale=(60.0, 1.0, 1.0)), scale=1.0, dist=0.0, axis='X', kind='BANDS')
    n.out(n.principled(base=(0.55, 0.45, 0.30), roughness=0.85,
                       normal=n.bump(tw.outputs['Fac'], strength=0.6, distance=0.003)))
    return m


def sign_board(name="SignBoard"):
    return simple_material(name, (0.88, 0.86, 0.80), roughness=0.5)


def sign_red(name="SignRed"):
    return simple_material(name, (0.70, 0.04, 0.03), roughness=0.4)


def sign_text(name="SignText"):
    return simple_material(name, (0.03, 0.03, 0.03), roughness=0.5)


def gull_white(name="GullWhite"):
    return simple_material(name, (0.85, 0.85, 0.85), roughness=0.6, sheen=0.3)


def gull_grey(name="GullGrey"):
    return simple_material(name, (0.35, 0.38, 0.42), roughness=0.6)


def bird_silhouette(name="FarBird"):
    return simple_material(name, (0.06, 0.05, 0.05), roughness=0.7)
