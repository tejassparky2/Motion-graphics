"""Cutaway of a finger knuckle (metacarpophalangeal joint) for the "gas bubble" shot.

Everything is a solid of revolution about the joint axis (local X), sliced in half at y = 0 so the
camera (looking along +Y) sees the cut faces: cortical bone, spongy bone, cartilage, the capsule and
the synovial fluid in between.  The phalanx pulls away, dissolved gas gathers and a bubble pops into being.
"""
import math

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

from pb import util
from pb.nodes import new_material
from xb.anim import fr, key_loc

ORIGIN = Vector((60.0, 0.0, 0.0))   # far from the room so its lights don't reach
C_H = -0.10            # centre of the metacarpal head sphere (local x)
R_HEAD = 0.105         # metacarpal head (bone)
CART = 0.012           # cartilage thickness
R_CUP = 0.140          # phalanx cup (bone)
PULL = 0.075           # how far the phalanx is drawn out


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

def _arc(r, th0, th1, n=24):
    th = np.linspace(th0, th1, n)
    return [(C_H + r * math.cos(t), r * math.sin(t)) for t in th]


def metacarpal_profile(t=0.0):
    """(x, r) outline from the shaft end to the tip of the head, inset by t."""
    p = [(-1.6, 0.0), (-1.6, 0.070 - t), (-0.34, 0.070 - t)]
    for s in np.linspace(0, 1, 10)[1:]:
        e = s * s * (3 - 2 * s)
        p.append((-0.34 + 0.24 * s, (0.070 - t) + (R_HEAD - 0.070) * e))
    p += _arc(R_HEAD - t, math.pi / 2, 0.0)[1:]
    return p


def phalanx_profile(t=0.0):
    """(x, r) outline from the cup centre around the base and down the shaft."""
    rim = 0.088
    th_rim = math.asin(min(0.99, (rim - 0.5 * t) / (R_CUP + t)))
    p = _arc(R_CUP + t, 0.0, th_rim, 16)
    x_rim, r_rim = p[-1]
    p += [(x_rim + 0.012, 0.098 - t), (0.10, 0.099 - t)]
    for s in np.linspace(0, 1, 10)[1:]:
        e = s * s * (3 - 2 * s)
        p.append((0.10 + 0.24 * s, (0.099 - t) - 0.035 * e))
    p += [(1.6, 0.064 - t), (1.6, 0.0)]
    return p


def head_cartilage_profile():
    outer = _arc(R_HEAD + CART, 0.0, math.radians(62), 18)
    inner = _arc(R_HEAD - 0.002, math.radians(62), 0.0, 18)
    return outer + inner


def cup_cartilage_profile():
    th = math.radians(36)
    inner = _arc(R_CUP - CART, 0.0, th, 14)
    outer = _arc(R_CUP + 0.002, th, 0.0, 14)
    return inner + outer


CAPSULE = [(-0.27, 0.080), (-0.22, 0.104), (-0.14, 0.136), (-0.05, 0.156), (0.04, 0.150),
           (0.12, 0.128), (0.19, 0.104), (0.25, 0.090)]


def _revolve(profile_xr, segments=72):
    """Lathe an (x, r) outline about the X axis."""
    prof = np.array([(r, x) for x, r in profile_xr], dtype=np.float64)
    v, f, uv = util.lathe(prof, segments=segments)
    v = v[:, [2, 0, 1]]          # lathe axis (z) -> x
    return v, f


def _cut_object(name, profile, coll, mats, y_cut=0.0, closed=True, segments=72, smooth=True):
    """Revolved solid sliced at y = y_cut (keeps y >= y_cut); the cut face gets material slot 1."""
    v, f = _revolve(profile, segments)
    me = bpy.data.meshes.new(name)
    me.from_pydata(v.tolist(), [], [list(x) for x in f])
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                                 plane_co=(0, y_cut, 0), plane_no=(0, -1, 0), clear_outer=True)
    for fc in bm.faces:
        fc.material_index = 0
        fc.smooth = smooth
    if closed:
        cut_edges = [e for e in res['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
        out = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=cut_edges,
                                      normal=(0, -1, 0))
        for fc in out['geom']:
            if isinstance(fc, bmesh.types.BMFace):
                fc.material_index = 1
                fc.smooth = False
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


def _pull_shape_key(ob, start=-0.12, end=0.12, amount=PULL):
    """Shape key that stretches the part of the mesh near the phalanx along +X."""
    ob.shape_key_add(name='Basis', from_mix=False)
    k = ob.shape_key_add(name='Pulled', from_mix=False)
    for i, vtx in enumerate(ob.data.vertices):
        x = vtx.co.x
        s = min(1.0, max(0.0, (x - start) / (end - start)))
        k.data[i].co.x = x + amount * s * s * (3 - 2 * s)
    return k


# ---------------------------------------------------------------------------
# materials
# ---------------------------------------------------------------------------

def _materials():
    M = {}
    m, n = new_material("JBoneSurface")
    co = n.texcoord('Object')
    nz = n.noise(co, scale=40.0, detail=6.0)
    col = n.mix(n.math('MULTIPLY', nz.outputs['Fac'], 0.5), (0.93, 0.86, 0.70), (0.80, 0.70, 0.55))
    n.out(n.principled(base=col, roughness=0.42, normal=n.bump(nz.outputs['Fac'], strength=0.15, distance=0.004)))
    M['bone'] = m
    m, n = new_material("JBoneCortex")
    co = n.texcoord('Object')
    w = n.wave(n.mapping(co, scale=(1.0, 1.0, 1.0)), scale=60.0, dist=3.0, detail=2.0, axis='X')
    col = n.mix(n.math('MULTIPLY', w.outputs['Fac'], 0.25), (0.96, 0.92, 0.82), (0.82, 0.76, 0.64))
    n.out(n.principled(base=col, roughness=0.55))
    M['cortex'] = m
    m, n = new_material("JBoneSpongy")
    co = n.texcoord('Object')
    vo = n.voronoi(co, scale=55.0, feature='DISTANCE_TO_EDGE')
    vo2 = n.voronoi(co, scale=140.0, feature='DISTANCE_TO_EDGE')
    strut = n.math('MAXIMUM', n.maprange(vo.outputs['Distance'], 0.06, 0.02),
                   n.math('MULTIPLY', n.maprange(vo2.outputs['Distance'], 0.08, 0.03), 0.6))
    col = n.mix(strut, (0.55, 0.16, 0.12), (0.93, 0.84, 0.66))
    n.out(n.principled(base=col, roughness=0.6, normal=n.bump(strut, strength=0.4, distance=0.003)))
    M['spongy'] = m
    m, n = new_material("JCartilage")
    lw = n.node('ShaderNodeLayerWeight', Blend=0.3)
    col = n.mix(lw.outputs['Facing'], (0.78, 0.86, 0.90), (0.55, 0.70, 0.82))
    n.out(n.principled(base=col, roughness=0.18, coat=0.6, coat_rough=0.1))
    M['cartilage'] = m
    m, n = new_material("JCartilageCut")
    n.out(n.principled(base=(0.70, 0.80, 0.86), roughness=0.4))
    M['cartilage_cut'] = m
    m, n = new_material("JCapsule")
    co = n.texcoord('Object')
    nz = n.noise(co, scale=25.0, detail=5.0)
    col = n.mix(n.math('MULTIPLY', nz.outputs['Fac'], 0.6), (0.78, 0.30, 0.30), (0.55, 0.15, 0.18))
    bsdf = n.principled(base=col, roughness=0.22, coat=0.7, coat_rough=0.08,
                        normal=n.bump(nz.outputs['Fac'], strength=0.25, distance=0.006))
    tr = n.node('ShaderNodeBsdfTransparent', Color=(1.0, 0.75, 0.72))
    lw = n.node('ShaderNodeLayerWeight', Blend=0.5)
    mix = n.node('ShaderNodeMixShader', Fac=n.maprange(lw.outputs['Facing'], 0.0, 0.6, 0.55, 1.0))
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(bsdf.outputs[0], mix.inputs[2])
    n.out(mix)
    M['capsule'] = m
    m, n = new_material("JCapsuleCut")
    n.out(n.principled(base=(0.62, 0.20, 0.22), roughness=0.5))
    M['capsule_cut'] = m
    # synovial fluid: clear golden liquid; 'Pressure' darkens it as the pressure drops
    m, n = new_material("JFluid")
    pv = n.node('ShaderNodeValue', _name='Pressure')
    pv.outputs[0].default_value = 1.0
    co = n.texcoord('Object')
    t = n.node('ShaderNodeValue', _name='Time')
    swirl = n.noise(co, scale=9.0, detail=3.0, dims='4D', w=t.outputs[0])
    tint = n.mix(n.math('MULTIPLY', swirl.outputs['Fac'], 0.7), (1.0, 0.78, 0.12), (0.95, 0.55, 0.04))
    dark = n.mix(pv.outputs[0], (0.25, 0.10, 0.22), tint)
    em = n.node('ShaderNodeEmission', Color=dark, Strength=n.math('MULTIPLY_ADD', pv.outputs[0], 0.5, 0.15))
    gl = n.node('ShaderNodeBsdfGlossy', Roughness=0.08)
    tr = n.node('ShaderNodeBsdfTransparent', Color=dark)
    mix = n.node('ShaderNodeMixShader', Fac=0.85)
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(em.outputs[0], mix.inputs[2])
    add = n.node('ShaderNodeAddShader')
    n.link(mix.outputs[0], add.inputs[0])
    gl_mix = n.node('ShaderNodeMixShader', Fac=0.85)
    n.link(gl.outputs[0], gl_mix.inputs[1])
    n.link(n.node('ShaderNodeBsdfTransparent').outputs[0], gl_mix.inputs[2])
    n.link(gl_mix.outputs[0], add.inputs[1])
    n.out(add)
    M['fluid'] = m
    M['fluid_time'] = t
    M['fluid_pressure'] = pv
    m, n = new_material("JBubble")
    lw = n.node('ShaderNodeLayerWeight', Blend=0.25)
    em = n.node('ShaderNodeEmission', Color=(0.75, 0.92, 1.0),
                Strength=n.math('MULTIPLY', n.math('POWER', lw.outputs['Facing'], 2.5), 6.0))
    gl = n.node('ShaderNodeBsdfGlossy', Roughness=0.02)
    tr = n.node('ShaderNodeBsdfTransparent', Color=(0.92, 0.97, 1.0))
    mix = n.node('ShaderNodeMixShader', Fac=n.math('MULTIPLY', lw.outputs['Fresnel'], 1.2))
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(gl.outputs[0], mix.inputs[2])
    add = n.node('ShaderNodeAddShader')
    n.link(mix.outputs[0], add.inputs[0])
    n.link(em.outputs[0], add.inputs[1])
    n.out(add)
    M['bubble'] = m
    m, n = new_material("JGas")
    n.out(n.node('ShaderNodeEmission', Color=(0.75, 0.92, 1.0), Strength=4.0))
    M['gas'] = m
    m, n = new_material("JShock")
    v = n.node('ShaderNodeValue', _name='Fade')
    v.outputs[0].default_value = 0.0
    em = n.node('ShaderNodeEmission', Color=(0.7, 0.9, 1.0), Strength=n.math('MULTIPLY', v.outputs[0], 8.0))
    tr = n.node('ShaderNodeBsdfTransparent')
    mix = n.node('ShaderNodeMixShader', Fac=v.outputs[0])
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(em.outputs[0], mix.inputs[2])
    n.out(mix)
    M['shock'] = m
    M['shock_fade'] = v
    m, n = new_material("JTendon")
    co = n.texcoord('Object')
    w = n.wave(co, scale=90.0, dist=2.0, detail=2.0, axis='X')
    col = n.mix(n.math('MULTIPLY', w.outputs['Fac'], 0.3), (0.92, 0.90, 0.86), (0.75, 0.72, 0.70))
    n.out(n.principled(base=col, roughness=0.25, aniso=0.6, normal=n.bump(w.outputs['Fac'], strength=0.2)))
    M['tendon'] = m
    m, n = new_material("JBackdrop")
    co = n.texcoord('Generated')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=co)
    col = n.ramp(sep.outputs['Z'], [(0.0, (0.004, 0.008, 0.02)), (0.5, (0.02, 0.05, 0.11)),
                                    (1.0, (0.006, 0.012, 0.03))])
    n.out(n.node('ShaderNodeEmission', Color=col, Strength=1.0))
    M['backdrop'] = m
    m, n = new_material("JMote")
    n.out(n.node('ShaderNodeEmission', Color=(0.35, 0.65, 1.0), Strength=2.5))
    M['mote'] = m
    return M


# ---------------------------------------------------------------------------
# build + animate
# ---------------------------------------------------------------------------

def build(coll, T):
    """T: dict of shot times (pull, pressure, bubble, start, end)."""
    M = _materials()
    root = bpy.data.objects.new('JointRoot', None)
    coll.objects.link(root)
    root.location = ORIGIN
    parts = []

    def add(ob, parent=root):
        ob.parent = parent
        parts.append(ob)
        return ob

    meta = add(_cut_object('Metacarpal', metacarpal_profile(), coll, [M['bone'], M['cortex']]))
    add(_cut_object('MetacarpalCore', metacarpal_profile(0.012), coll, [M['spongy'], M['spongy']],
                    y_cut=-0.0006))
    add(_cut_object('HeadCartilage', head_cartilage_profile(), coll, [M['cartilage'], M['cartilage_cut']]))
    phal = bpy.data.objects.new('PhalanxGroup', None)
    coll.objects.link(phal)
    add(phal)
    add(_cut_object('Phalanx', phalanx_profile(), coll, [M['bone'], M['cortex']]), phal)
    add(_cut_object('PhalanxCore', phalanx_profile(0.012), coll, [M['spongy'], M['spongy']],
                    y_cut=-0.0006), phal)
    add(_cut_object('CupCartilage', cup_cartilage_profile(), coll, [M['cartilage'], M['cartilage_cut']]), phal)
    for ob in list(parts):
        if ob.type == 'MESH' and 'Core' in ob.name:
            ob.visible_shadow = False
    # capsule: an open sleeve, sliced, then thickened
    cap = _cut_object('Capsule', CAPSULE, coll, [M['capsule'], M['capsule_cut']], closed=False, segments=96)
    add(cap)
    _pull_shape_key(cap)
    sol = cap.modifiers.new('Thick', 'SOLIDIFY')
    sol.thickness = 0.010
    sol.use_rim = True
    sol.material_offset_rim = 1
    sub = cap.modifiers.new('Smooth', 'SUBSURF')
    sub.levels = sub.render_levels = 1
    # synovial fluid fills the capsule; its cut face sits just behind the bones' cut faces
    fluid_prof = [(-0.25, 0.0)] + [(x, r - 0.008) for x, r in CAPSULE[1:-1]] + [(0.23, 0.0)]
    fluid = _cut_object('Fluid', fluid_prof, coll, [M['fluid'], M['fluid']], y_cut=0.0015)
    add(fluid)
    fluid.visible_shadow = False
    _pull_shape_key(fluid)
    # extensor tendon gliding over the back of the joint (half cross-section, sliced at y = 0)
    xs = np.linspace(-1.2, 1.2, 80)
    th = np.linspace(-math.pi / 2, math.pi / 2, 9)
    V = []
    for x in xs:
        z0 = 0.170 + 0.022 * math.exp(-((x + 0.03) / 0.12) ** 2)
        for t in th:
            V.append((x, 0.07 * math.cos(t), z0 + 0.014 * math.sin(t)))
    F = util.grid_faces(len(xs), len(th), wrap_v=True)
    ten = util.make_mesh('Tendon', np.array(V), F, coll=coll, mat=[M['tendon']])
    add(ten)
    _pull_shape_key(ten, start=-0.4, end=0.4, amount=PULL * 0.5)
    # backdrop and floating motes
    v, f, uv = util.uv_sphere(9.0, 48, 24)
    bd = util.make_mesh('JointBackdrop', v, f, coll=coll, mat=[M['backdrop']])
    add(bd)
    bd.visible_shadow = False
    rng = np.random.default_rng(5)
    mb = util.MeshBuilder()
    for i in range(70):
        c = (rng.uniform(-2.0, 2.0), rng.uniform(0.5, 3.5), rng.uniform(-1.6, 1.6))
        v, f, uv = util.uv_sphere(rng.uniform(0.004, 0.012), 8, 5, center=c)
        mb.add(v, f, uv=uv)
    motes = mb.build('Motes', coll, mats=[M['mote']])
    add(motes)
    motes.visible_shadow = False
    # dissolved gas and the bubble
    gas_objs = []
    tmp = util.make_mesh('GasMesh', *util.uv_sphere(0.0045, 8, 5)[:2], coll=coll, mat=[M['gas']])
    gas_mesh = tmp.data
    bpy.data.objects.remove(tmp)
    for i in range(40):
        g = bpy.data.objects.new(f'Gas{i:02d}', gas_mesh)
        coll.objects.link(g)
        add(g)
        g.visible_shadow = False
        gas_objs.append(g)
    bub = util.make_mesh('Bubble', *util.uv_sphere(1.0, 48, 24)[:2], coll=coll, mat=[M['bubble']])
    add(bub)
    bub.visible_shadow = False
    sh = util.make_mesh('Shockwave', *_torus(1.0, 0.035), coll=coll, mat=[M['shock']])
    add(sh)
    sh.rotation_euler = (math.pi / 2, 0, 0)
    sh.visible_shadow = False
    lights = _lights(coll, root)
    _animate(T, phal, cap, fluid, ten, gas_objs, bub, sh, M, lights, rng)
    return root


def _torus(R, r, nu=64, nv=12):
    path = np.array([[R * math.cos(a), R * math.sin(a), 0.0] for a in np.linspace(0, 2 * math.pi, nu, endpoint=False)])
    v, f, uv = util.sweep(path, radius=r, sides=nv, closed=True)
    return v, f


def _lights(coll, root):
    def area(name, loc, energy, size, color, aim=(0, 0, 0)):
        d = bpy.data.lights.new(name, 'AREA')
        d.energy = energy
        d.size = size
        d.color = color
        o = bpy.data.objects.new(name, d)
        coll.objects.link(o)
        o.parent = root
        o.location = loc
        o.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        return o
    area('JKey', (-0.5, -1.3, 0.9), 160, 1.0, (1.0, 0.97, 0.94))
    area('JRim', (0.9, 0.6, 1.0), 220, 0.8, (0.4, 0.75, 1.0))
    area('JFill', (0.8, -1.0, -0.8), 70, 1.2, (1.0, 0.6, 0.4))
    area('JBack', (-0.3, 1.2, -0.4), 120, 1.0, (0.5, 0.6, 1.0))
    d = bpy.data.lights.new('JFlash', 'POINT')
    d.energy = 0.0
    d.color = (0.7, 0.9, 1.0)
    d.shadow_soft_size = 0.05
    flash = bpy.data.objects.new('JFlash', d)
    coll.objects.link(flash)
    flash.parent = root
    return dict(flash=flash)


def _animate(T, phal, cap, fluid, ten, gas, bub, sh, M, lights, rng):
    p0, p1 = T['pull']
    # the phalanx is drawn out; capsule, fluid and tendon stretch with it
    for t, s in ((T['start'], 0.0), (p0, 0.0), (p1, 1.0), (T['end'], 1.0)):
        key_loc(phal, t, (PULL * s, 0.0, 0.0))
        for ob in (cap, fluid, ten):
            k = ob.data.shape_keys.key_blocks['Pulled']
            k.value = s
            k.keyframe_insert('value', frame=fr(t))
    # pressure falls: the fluid darkens; dissolved gas comes out of solution
    pv = M['fluid_pressure'].outputs[0]
    for t, v in ((T['start'], 1.0), (T['pressure'][0], 1.0), (T['pressure'][1], 0.35), (T['bubble'], 0.3),
                 (T['bubble'] + 0.25, 0.85), (T['end'], 0.9)):
        pv.default_value = v
        pv.keyframe_insert('default_value', frame=fr(t))
    tv = M['fluid_time'].outputs[0]
    for t, v in ((T['start'], 0.0), (T['end'], 2.5)):
        tv.default_value = v
        tv.keyframe_insert('default_value', frame=fr(t))
    for fc in M['fluid'].node_tree.animation_data.action.fcurves:
        if 'Time' in fc.data_path:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'
    gap_c = Vector((C_H + 0.5 * (R_HEAD + CART + R_CUP - CART + PULL), 0.012, 0.0))
    for i, g in enumerate(gas):
        # scattered through the widened gap, drifting toward its centre
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0.02, 0.11)
        start = Vector((C_H + R_HEAD + CART + rng.uniform(0.005, PULL + 0.006),
                        rng.uniform(0.004, 0.03), rad * math.sin(ang)))
        t_in = rng.uniform(T['pressure'][0], T['pressure'][1] - 0.2)
        g.scale = (0, 0, 0)
        g.keyframe_insert('scale', frame=fr(T['start']))
        g.keyframe_insert('scale', frame=fr(t_in))
        key_loc(g, t_in, start)
        g.scale = (1, 1, 1)
        g.keyframe_insert('scale', frame=fr(t_in + 0.15))
        mid = start.lerp(gap_c, 0.6)
        key_loc(g, T['bubble'] - 0.08, mid)
        g.keyframe_insert('scale', frame=fr(T['bubble'] - 0.08))
        key_loc(g, T['bubble'], gap_c)
        g.scale = (0, 0, 0)
        g.keyframe_insert('scale', frame=fr(T['bubble']))
    # the bubble snaps into existence with an elastic overshoot
    b = T['bubble']
    rb = 0.036
    bub.location = gap_c
    for t, s in ((T['start'], 0.0), (b - 0.02, 0.0), (b + 0.05, 1.3), (b + 0.12, 0.88), (b + 0.2, 1.08),
                 (b + 0.3, 0.97), (b + 0.42, 1.0)):
        bub.scale = (rb * s,) * 3
        bub.keyframe_insert('scale', frame=fr(t))
    # gentle wobble afterwards
    for i, t in enumerate(np.arange(b + 0.5, T['end'], 0.25)):
        w = 0.03 * (-1) ** i
        bub.scale = (rb * (1 + w), rb * (1 - w), rb * (1 + w * 0.5))
        bub.keyframe_insert('scale', frame=fr(t))
    # shockwave ring and flash
    sh.location = gap_c + Vector((0, -0.02, 0))
    fade = M['shock_fade'].outputs[0]
    for t, s, a in ((T['start'], 0.01, 0.0), (b - 0.02, 0.01, 0.0), (b, 0.03, 1.0), (b + 0.35, 0.55, 0.0)):
        sh.scale = (s, s, s)
        sh.keyframe_insert('scale', frame=fr(t))
        fade.default_value = a
        fade.keyframe_insert('default_value', frame=fr(t))
    fl = lights['flash']
    fl.location = gap_c + Vector((0, -0.06, 0))
    for t, e in ((T['start'], 0.0), (b - 0.02, 0.0), (b + 0.02, 3.0), (b + 0.25, 0.0)):
        fl.data.energy = e
        fl.data.keyframe_insert('energy', frame=fr(t))


def camera(coll, T):
    """Looks at the cut face with the joint running up the frame; pushes in; shakes on the pop."""
    d = bpy.data.cameras.new('Cam3_Joint')
    d.lens = 50
    d.sensor_fit = 'VERTICAL'
    d.sensor_height = 24.0
    d.dof.use_dof = True
    d.dof.aperture_fstop = 5.6
    d.clip_start = 0.05
    cam = bpy.data.objects.new('Cam3_Joint', d)
    coll.objects.link(cam)
    up = Vector((1.0, 0.0, 0.30)).normalized()

    def place(t, target_x, dist, yaw=0.0):
        tgt = ORIGIN + Vector((target_x, 0.0, 0.0))
        view = Vector((math.sin(yaw) * 0.35, 1.0, -0.18)).normalized()
        loc = tgt - view * dist
        u = (up - up.dot(view) * view).normalized()
        cam.location = loc
        cam.rotation_euler = Matrix((view.cross(u), u, -view)).transposed().to_euler()
        cam.keyframe_insert('location', frame=fr(t))
        cam.keyframe_insert('rotation_euler', frame=fr(t))
        d.dof.focus_distance = dist
        d.keyframe_insert('dof.focus_distance', frame=fr(t))
    s, e, b = T['start'], T['end'], T['bubble']
    place(s, -0.02, 2.3, -0.25)
    place(T['pull'][1], 0.01, 2.0, -0.12)
    place(b - 0.05, 0.04, 1.55, 0.0)
    place(e, 0.05, 1.38, 0.08)
    # camera shake on the pop
    fcs = [fc for fc in cam.animation_data.action.fcurves if fc.data_path == 'location']
    fcs.sort(key=lambda fc: fc.array_index)
    shake = []
    for i, dt in enumerate((0.0, 0.04, 0.08, 0.12, 0.17, 0.23, 0.3)):
        base = Vector([fc.evaluate(fr(b + dt)) for fc in fcs])
        amp = 0.012 * (1 - i / 7)
        shake.append((b + dt, base + Vector((amp * (-1) ** i, 0, amp * 0.6 * (-1) ** (i + 1)))))
    for t, p in shake:
        cam.location = p
        cam.keyframe_insert('location', frame=fr(t))
    return cam
