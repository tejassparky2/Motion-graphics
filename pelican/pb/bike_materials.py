"""Materials for the bicycle."""
from .nodes import new_material, simple_material


def paint(name="BikePaint", color=(0.02, 0.32, 0.30)):
    """Deep glossy enamel with metallic flake under a clear coat."""
    m, n = new_material(name)
    obj = n.texcoord('Object')
    flake = n.voronoi(obj, scale=2600.0)
    fl = n.maprange(flake.outputs['Distance'], 0.0, 0.25, 1.0, 0.0)
    flake_n = n.bump(fl, strength=0.08, distance=0.0002)
    dirt = n.noise(obj, scale=18.0, detail=2.0, rough=0.6)
    grime = n.maprange(dirt.outputs['Fac'], 0.55, 0.8, 0.0, 0.18)
    base = n.mix(grime, color, (0.05, 0.05, 0.04))
    bsdf = n.principled(base=base, roughness=0.32, metallic=0.35, normal=flake_n,
                        coat=1.0, coat_rough=n.maprange(dirt.outputs['Fac'], 0.3, 0.8, 0.02, 0.09),
                        spec=0.5)
    n.out(bsdf)
    m.diffuse_color = (*color, 1)
    return m


def chrome(name="Chrome", rough=0.06):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    sm = n.noise(obj, scale=60.0, detail=2.0)
    r = n.maprange(sm.outputs['Fac'], 0.3, 0.75, rough * 0.6, rough * 2.2)
    pits = n.noise(obj, scale=900.0, detail=2.0)
    bump = n.bump(pits.outputs['Fac'], strength=0.03, distance=0.0002)
    n.out(n.principled(base=(0.92, 0.9, 0.86), roughness=r, metallic=1.0, normal=bump))
    m.diffuse_color = (0.8, 0.8, 0.8, 1)
    return m


def brushed_alu(name="BrushedAlu"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    stretch = n.mapping(uv, scale=(1.0, 900.0, 1.0))
    st = n.noise(stretch, scale=4.0, detail=4.0)
    bump = n.bump(st.outputs['Fac'], strength=0.05, distance=0.0003)
    n.out(n.principled(base=(0.86, 0.86, 0.87), roughness=0.22, metallic=1.0, normal=bump,
                       aniso=0.6))
    return m


def tire(name="Tire"):
    """Black tread crown, tan gum-wall sidewalls, procedural chevron tread."""
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    u = sep.outputs['X']
    v = sep.outputs['Y']
    # v runs across the tire section (0..1), 0.5 = crown
    across = n.math('ABSOLUTE', n.math('SUBTRACT', v, 0.5))
    crown = n.maprange(across, 0.20, 0.25, 1.0, 0.0)
    # chevron tread: 120 blocks around
    chev = n.math('ADD', n.math('MULTIPLY', u, 120.0), n.math('MULTIPLY', across, 3.0))
    frac = n.math('FRACT', chev)
    block = n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', frac, 0.5)), 0.18, 0.24, 1.0, 0.0)
    rib = n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', across, 0.0)), 0.02, 0.035, 0.0, 1.0)
    tread_h = n.math('MULTIPLY', n.math('MULTIPLY', block, rib), crown)
    obj = n.texcoord('Object')
    gr = n.noise(obj, scale=300.0, detail=3.0)
    h = n.math('ADD', tread_h, n.math('MULTIPLY', gr.outputs['Fac'], 0.15))
    bump = n.bump(h, strength=0.6, distance=0.0012)
    gum = n.mix(n.noise(obj, scale=40.0).outputs['Fac'], (0.36, 0.20, 0.09), (0.30, 0.16, 0.07))
    side = n.maprange(across, 0.24, 0.27, 0.0, 1.0)
    dust = n.maprange(n.noise(obj, scale=25.0, detail=2.0).outputs['Fac'], 0.45, 0.75, 0.0, 0.5)
    black = n.mix(dust, (0.018, 0.017, 0.016), (0.09, 0.08, 0.07))
    col = n.mix(side, black, gum)
    rough = n.mix(side, 0.75, 0.55, dtype='FLOAT')
    n.out(n.principled(base=col, roughness=rough, normal=bump, spec=0.35))
    return m


def rubber(name="Rubber", color=(0.02, 0.02, 0.02)):
    return simple_material(name, color, roughness=0.7, spec=0.3)


def leather(name="Leather", color=(0.16, 0.055, 0.018)):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    grain = n.voronoi(obj, scale=700.0)
    g = n.maprange(grain.outputs['Distance'], 0.0, 0.5, 0.0, 1.0)
    big = n.noise(obj, scale=30.0, detail=3.0)
    wear = n.maprange(big.outputs['Fac'], 0.45, 0.7, 0.0, 1.0)
    col = n.mix(wear, color, (color[0] * 1.6, color[1] * 1.5, color[2] * 1.3))
    rough = n.maprange(big.outputs['Fac'], 0.3, 0.7, 0.28, 0.5)
    bump = n.bump(n.math('ADD', g, n.math('MULTIPLY', big.outputs['Fac'], 0.4)),
                  strength=0.25, distance=0.0006)
    n.out(n.principled(base=col, roughness=rough, normal=bump, coat=0.3, coat_rough=0.3,
                       sheen=0.1))
    return m


def cork(name="Cork"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    vor = n.voronoi(obj, scale=900.0)
    nz = n.noise(obj, scale=400.0, detail=4.0)
    h = n.math('MULTIPLY', vor.outputs['Distance'], nz.outputs['Fac'])
    col = n.ramp(nz.outputs['Fac'], [(0.3, (0.32, 0.18, 0.08)), (0.7, (0.55, 0.36, 0.18))])
    n.out(n.principled(base=col, roughness=0.75, normal=n.bump(h, strength=0.5, distance=0.0008)))
    return m


def chain_steel(name="ChainSteel"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    nz = n.noise(obj, scale=200.0, detail=4.0)
    col = n.mix(n.maprange(nz.outputs['Fac'], 0.4, 0.7), (0.20, 0.19, 0.18), (0.07, 0.06, 0.05))
    n.out(n.principled(base=col, roughness=n.maprange(nz.outputs['Fac'], 0.3, 0.7, 0.35, 0.6),
                       metallic=0.9))
    return m


def wicker(name="Wicker"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    obj = n.texcoord('Object')
    fib = n.wave(n.mapping(uv, scale=(220.0, 1.0, 1.0)), scale=1.0, dist=3.0, detail=3.0,
                 axis='X')
    nz = n.noise(obj, scale=60.0, detail=2.0)
    col = n.ramp(nz.outputs['Fac'], [(0.25, (0.42, 0.25, 0.10)), (0.55, (0.62, 0.42, 0.20)),
                                     (0.8, (0.50, 0.31, 0.13))])
    col2 = n.mix(n.math('MULTIPLY', fib.outputs['Fac'], 0.3), col, (0.25, 0.13, 0.05))
    n.out(n.principled(base=col2, roughness=0.55,
                       normal=n.bump(fib.outputs['Fac'], strength=0.3, distance=0.0005),
                       sheen=0.15, coat=0.2, coat_rough=0.35))
    return m


def lamp_glass(name="LampGlass"):
    m, n = new_material(name)
    n.out(n.principled(base=(1, 1, 1), roughness=0.02, transmission=1.0, ior=1.5))
    return m


def lamp_emit(name="LampEmit", color=(1.0, 0.72, 0.38), strength=6.0):
    m, n = new_material(name)
    em = n.node('ShaderNodeEmission', Color=color, Strength=strength)
    n.out(em)
    return m


def reflector(name="Reflector"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    vor = n.voronoi(obj, scale=1800.0, metric='MANHATTAN')
    bump = n.bump(vor.outputs['Distance'], strength=0.8, distance=0.0005)
    n.out(n.principled(base=(0.8, 0.02, 0.01), roughness=0.05, transmission=0.6, normal=bump,
                       emission=(1.0, 0.05, 0.02), emission_strength=0.6))
    return m


def gold(name="Gold"):
    return simple_material(name, (1.0, 0.70, 0.30), roughness=0.18, metallic=1.0)


def cream(name="Cream"):
    return simple_material(name, (0.85, 0.78, 0.62), roughness=0.35, coat=1.0, coat_rough=0.05)


def fish_skin(name="FishSkin"):
    """Mackerel: iridescent blue-green back with dark tiger bars, silver belly."""
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    u, v = sep.outputs['X'], sep.outputs['Y']
    # v: 0 belly .. 0.5 back .. 1 belly (around the body)
    back = n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', v, 0.5)), 0.12, 0.26, 1.0, 0.0)
    obj = n.texcoord('Object')
    bars_coord = n.vmath('ADD', n.mapping(uv, scale=(28.0, 3.0, 1.0)),
                         n.vmath('SCALE', n.noise(obj, scale=50.0).outputs['Color'], scale=0.6))
    bars = n.wave(bars_coord, scale=1.0, dist=2.5, detail=2.0, axis='X', profile='SIN')
    barsm = n.maprange(bars.outputs['Fac'], 0.55, 0.75, 0.0, 1.0)
    backcol = n.mix(barsm, (0.04, 0.22, 0.20), (0.005, 0.02, 0.03))
    col = n.mix(back, (0.75, 0.78, 0.80), backcol)
    scales = n.voronoi(n.mapping(uv, scale=(220.0, 60.0, 1.0)), scale=1.0)
    bump = n.bump(scales.outputs['Distance'], strength=0.15, distance=0.0003)
    tf = n.maprange(n.noise(obj, scale=30.0).outputs['Fac'], 0.3, 0.7, 250.0, 650.0)
    n.out(n.principled(base=col, roughness=0.18, metallic=n.mix(back, 0.85, 0.3, dtype='FLOAT'),
                       normal=bump, thin_film=tf, coat=0.5, coat_rough=0.05))
    return m


def fish_eye(name="FishEye"):
    return simple_material(name, (0.01, 0.01, 0.01), roughness=0.02, coat=1.0)


def fish_fin(name="FishFin"):
    m, n = new_material(name)
    n.out(n.principled(base=(0.25, 0.28, 0.30), roughness=0.3, alpha=0.85, metallic=0.4,
                       sss=0.3))
    return m
