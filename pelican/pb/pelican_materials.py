"""Materials for the great white pelican."""
from .nodes import new_material


def body_down(name="BodyDown"):
    """Underlying velvety plumage on the body mesh, with bare facial skin mask."""
    m, n = new_material(name)
    obj = n.texcoord('Object')
    skin_mask = n.attr('skin')
    blush = n.attr('blush')
    fine = n.noise(obj, scale=900.0, detail=3.0)
    streak = n.wave(n.mapping(obj, scale=(1.0, 1.0, 1.0)), scale=260.0, dist=6.0, detail=3.0, axis='Z')
    h = n.math('ADD', n.math('MULTIPLY', fine.outputs['Fac'], 0.6), n.math('MULTIPLY', streak.outputs['Fac'], 0.4))
    white = n.mix(blush, (0.93, 0.90, 0.86), (0.96, 0.80, 0.74))
    skin = n.mix(n.noise(obj, scale=300.0).outputs['Fac'], (0.98, 0.52, 0.34), (0.98, 0.70, 0.30))
    col = n.mix(skin_mask, white, skin)
    rough = n.mix(skin_mask, 0.62, 0.38, dtype='FLOAT')
    sheen = n.mix(skin_mask, 0.6, 0.0, dtype='FLOAT')
    feather_bump = n.bump(h, strength=0.18, distance=0.0008)
    skin_bump = n.bump(n.voronoi(obj, scale=1500.0).outputs['Distance'], strength=0.25, distance=0.0003)
    nrm = n.mix(skin_mask, feather_bump, skin_bump, dtype='VECTOR')
    bsdf = n.principled(base=col, roughness=rough, sheen=sheen, sheen_rough=0.35,
                        sheen_tint=(1.0, 0.95, 0.9), normal=nrm,
                        sss=n.mix(skin_mask, 0.25, 0.4, dtype='FLOAT'),
                        sss_radius=(0.8, 0.45, 0.3), sss_scale=0.006, spec=0.35)
    n.out(bsdf)
    m.diffuse_color = (0.9, 0.88, 0.85, 1)
    return m


def feather(name="Feather"):
    """Feather vanes: UV u = root->tip, v = across.  Colour from 'fcol' attribute."""
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    u, vv = sep.outputs['X'], sep.outputs['Y']
    across = n.math('ABSOLUTE', n.math('SUBTRACT', vv, 0.5))
    shaft_w = n.math('MULTIPLY', n.math('SUBTRACT', 1.0, u), 0.035)
    shaft = n.math('LESS_THAN', across, n.math('ADD', shaft_w, 0.006))
    # barbs: diagonal lines sweeping toward the tip
    barb_coord = n.math('ADD', n.math('MULTIPLY', u, 1.0), n.math('MULTIPLY', across, 0.9))
    barbs = n.math('SINE', n.math('MULTIPLY', barb_coord, 260.0))
    obj = n.texcoord('Object')
    split_n = n.noise(n.vmath('MULTIPLY', uv, (3.0, 18.0, 1.0)), scale=2.0, detail=2.0)
    splits = n.maprange(split_n.outputs['Fac'], 0.62, 0.70, 0.0, 1.0)
    h = n.math('ADD', n.math('MULTIPLY', barbs, 0.35), n.math('MULTIPLY', shaft, 1.2))
    h = n.math('SUBTRACT', h, n.math('MULTIPLY', splits, 0.6))
    bump = n.bump(h, strength=0.25, distance=0.0003)
    fcol = n.attr('fcol', out='Color')
    # slightly darker, greyer toward the base (fluffy afterfeather) and along the shaft
    base_dark = n.maprange(u, 0.0, 0.35, 0.82, 1.0)
    col = n.mix(n.math('MULTIPLY', shaft, 0.5), fcol, n.mix(0.5, fcol, (1.0, 0.98, 0.92)))
    shade = n.node('ShaderNodeCombineColor', Red=base_dark, Green=base_dark, Blue=base_dark).outputs[0]
    col = n.mix(1.0, col, shade, blend='MULTIPLY')
    dark = n.attr('dark')
    rough = n.mix(dark, 0.55, 0.38, dtype='FLOAT')
    p = n.principled(base=col, roughness=rough, normal=bump, sheen=n.mix(dark, 0.5, 0.25, dtype='FLOAT'),
                     sheen_rough=0.3, spec=0.4)
    tr = n.node('ShaderNodeBsdfTranslucent', Color=n.mix(dark, col, (0.02, 0.02, 0.02)))
    tr_amt = n.mix(dark, 0.22, 0.04, dtype='FLOAT')
    mixs = n.node('ShaderNodeMixShader', Fac=tr_amt)
    n.link(p.outputs[0], mixs.inputs[1])
    n.link(tr.outputs[0], mixs.inputs[2])
    # small body feathers do not cast hard card shadows; the body mesh shades the form
    lp = n.node('ShaderNodeLightPath')
    shadowless = n.math('MULTIPLY', lp.outputs['Is Shadow Ray'], n.attr('shadowless'))
    clear = n.node('ShaderNodeBsdfTransparent')
    final = n.node('ShaderNodeMixShader', Fac=shadowless)
    n.link(mixs.outputs[0], final.inputs[1])
    n.link(clear.outputs[0], final.inputs[2])
    n.out(final)
    m.diffuse_color = (0.9, 0.9, 0.9, 1)
    return m


def bill(name="Bill"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    u, vv = sep.outputs['X'], sep.outputs['Y']
    obj = n.texcoord('Object')
    # v: 0 = right edge, 0.25 = culmen top, 0.5 = left edge, 0.75 = palate
    to_top = n.math('ABSOLUTE', n.math('SUBTRACT', vv, 0.25))
    culmen = n.maprange(to_top, 0.0, 0.05, 1.0, 0.0)
    edge = n.math('MAXIMUM', n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', vv, 0.5)), 0.0, 0.05, 1.0, 0.0),
                  n.math('MAXIMUM', n.maprange(vv, 0.0, 0.05, 1.0, 0.0), n.maprange(vv, 0.95, 1.0, 0.0, 1.0)))
    mott = n.noise(obj, scale=120.0, detail=6.0)
    slate = n.mix(mott.outputs['Fac'], (0.50, 0.50, 0.60), (0.62, 0.55, 0.62))
    col = n.mix(culmen, slate, (0.95, 0.70, 0.45))
    col = n.mix(n.math('MULTIPLY', edge, 0.9), col, (0.86, 0.32, 0.26))
    base = n.maprange(u, 0.0, 0.12, 1.0, 0.0)
    col = n.mix(base, col, (0.98, 0.70, 0.52))
    hook = n.maprange(u, 0.90, 0.95, 0.0, 1.0)
    col = n.mix(hook, col, (0.88, 0.22, 0.07))
    palate = n.maprange(vv, 0.55, 0.65, 0.0, 1.0)
    col = n.mix(n.math('MULTIPLY', palate, 0.6), col, (0.85, 0.50, 0.42))
    scratches = n.wave(n.mapping(uv, scale=(1.0, 1.0, 1.0)), scale=90.0, dist=12.0, detail=4.0, axis='X')
    bump = n.bump(n.math('ADD', scratches.outputs['Fac'], n.math('MULTIPLY', mott.outputs['Fac'], 0.5)),
                  strength=0.06, distance=0.0004)
    n.out(n.principled(base=col, roughness=n.maprange(mott.outputs['Fac'], 0.3, 0.7, 0.22, 0.42),
                       normal=bump, sss=0.15, sss_radius=(1.0, 0.4, 0.3), sss_scale=0.004,
                       coat=0.35, coat_rough=0.15))
    m.diffuse_color = (0.6, 0.55, 0.6, 1)
    return m


def pouch(name="Pouch"):
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    u, vv = sep.outputs['X'], sep.outputs['Y']
    obj = n.texcoord('Object')
    folds = n.wave(n.mapping(uv, scale=(1.0, 1.0, 1.0)), scale=24.0, dist=4.0, detail=3.0, axis='Y',
                   dscale=2.0)
    fine = n.noise(obj, scale=700.0, detail=4.0)
    veins = n.wave(obj, scale=60.0, dist=18.0, detail=6.0, kind='RINGS')
    vein_m = n.maprange(veins.outputs['Fac'], 0.0, 0.12, 1.0, 0.0)
    col = n.mix(n.noise(obj, scale=40.0).outputs['Fac'], (1.0, 0.62, 0.04), (0.98, 0.50, 0.04))
    col = n.mix(n.math('MULTIPLY', vein_m, 0.35), col, (0.85, 0.30, 0.06))
    rim = n.maprange(n.math('ABSOLUTE', n.math('SUBTRACT', vv, 0.5)), 0.38, 0.5, 0.0, 1.0)
    col = n.mix(n.math('MULTIPLY', rim, 0.5), col, (0.95, 0.45, 0.25))
    h = n.math('ADD', n.math('MULTIPLY', folds.outputs['Fac'], 1.0), n.math('MULTIPLY', fine.outputs['Fac'], 0.3))
    bump = n.bump(h, strength=0.22, distance=0.0012)
    n.out(n.principled(base=col, roughness=0.32, normal=bump, sss=0.7, sss_radius=(1.0, 0.45, 0.15),
                       sss_scale=0.008, spec=0.45, coat=0.25, coat_rough=0.2))
    m.diffuse_color = (1.0, 0.7, 0.15, 1)
    return m


def leg_skin(name="LegSkin", web=False):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    sc = n.voronoi(obj, scale=420.0 if not web else 900.0)
    crev = n.maprange(sc.outputs['Distance'], 0.0, 0.35, 0.0, 1.0)
    big = n.noise(obj, scale=40.0, detail=4.0)
    base = n.mix(big.outputs['Fac'], (0.98, 0.55, 0.40), (0.95, 0.62, 0.36))
    col = n.mix(n.math('MULTIPLY', n.math('SUBTRACT', 1.0, crev), 0.6), base, (0.55, 0.22, 0.15))
    bump = n.bump(crev, strength=0.5 if not web else 0.2, distance=0.0008)
    n.out(n.principled(base=col, roughness=n.maprange(crev, 0.0, 1.0, 0.6, 0.38), normal=bump,
                       sss=0.6 if web else 0.35, sss_radius=(1.0, 0.4, 0.25), sss_scale=0.006,
                       spec=0.4))
    m.diffuse_color = (0.95, 0.55, 0.4, 1)
    return m


def claw(name="Claw"):
    m, n = new_material(name)
    n.out(n.principled(base=(0.16, 0.13, 0.10), roughness=0.25, coat=0.4))
    return m


def iris(name="Iris"):
    """Eyeball with UV v = latitude (1 = front pole)."""
    m, n = new_material(name)
    uv = n.texcoord('UV')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=uv)
    lat = sep.outputs['Y']
    lon = sep.outputs['X']
    pupil = n.maprange(lat, 0.84, 0.855, 0.0, 1.0)
    iris_m = n.maprange(lat, 0.52, 0.55, 0.0, 1.0)
    streak = n.noise(n.node('ShaderNodeCombineXYZ', X=n.math('MULTIPLY', lon, 60.0), Y=n.math('MULTIPLY', lat, 6.0)),
                     scale=1.0, detail=3.0)
    iris_col = n.mix(streak.outputs['Fac'], (0.16, 0.03, 0.02), (0.42, 0.10, 0.04))
    ring = n.maprange(lat, 0.53, 0.58, 1.0, 0.0)
    iris_col = n.mix(n.math('MULTIPLY', ring, 0.8), iris_col, (0.05, 0.01, 0.01))
    sclera = (0.85, 0.80, 0.70)
    col = n.mix(iris_m, sclera, iris_col)
    col = n.mix(pupil, col, (0.0, 0.0, 0.0))
    n.out(n.principled(base=col, roughness=0.35, spec=0.2))
    return m


def cornea(name="Cornea"):
    m, n = new_material(name)
    n.out(n.principled(base=(1, 1, 1), roughness=0.0, transmission=1.0, ior=1.45, spec=1.0,
                       coat=1.0, coat_rough=0.0))
    return m


def eyelid(name="Eyelid"):
    m, n = new_material(name)
    obj = n.texcoord('Object')
    nz = n.noise(obj, scale=800.0, detail=3.0)
    n.out(n.principled(base=(0.98, 0.76, 0.42), roughness=0.35, sss=0.4, sss_radius=(1, 0.5, 0.3),
                       sss_scale=0.004, normal=n.bump(nz.outputs['Fac'], strength=0.3, distance=0.0003)))
    return m


def fuzz(name="Fuzz"):
    m, n = new_material(name)
    info = n.node('ShaderNodeHairInfo')
    tip = info.outputs['Intercept']
    col = n.mix(tip, (0.86, 0.84, 0.80), (0.98, 0.96, 0.93))
    p = n.principled(base=col, roughness=0.45, sheen=0.4, spec=0.3)
    tr = n.node('ShaderNodeBsdfTranslucent', Color=(0.95, 0.92, 0.88))
    mix = n.node('ShaderNodeMixShader', Fac=0.35)
    n.link(p.outputs[0], mix.inputs[1])
    n.link(tr.outputs[0], mix.inputs[2])
    n.out(mix)
    return m
