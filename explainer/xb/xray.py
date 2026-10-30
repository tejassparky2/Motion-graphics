"""X-ray look: translucent glowing skin, procedural hand bones riding on the rig, glowing joint capsules."""
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector

from pb import util
from pb.nodes import new_material

FINGER_R = {'index': 0.0050, 'middle': 0.0052, 'ring': 0.0048, 'pinky': 0.0042, 'thumb': 0.0058}


def xray_group():
    """Shader group: mixes an incoming surface with the x-ray look by the group's animated 'Amount'."""
    g = bpy.data.node_groups.get('XrayMix')
    if g:
        return g
    g = bpy.data.node_groups.new('XrayMix', 'ShaderNodeTree')
    g.interface.new_socket('Surface', in_out='INPUT', socket_type='NodeSocketShader')
    g.interface.new_socket('Shader', in_out='OUTPUT', socket_type='NodeSocketShader')
    N = g.nodes
    L = g.links
    gi = N.new('NodeGroupInput')
    go = N.new('NodeGroupOutput')
    amt = N.new('ShaderNodeValue')
    amt.name = amt.label = 'Amount'
    amt.outputs[0].default_value = 0.0
    lw = N.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    rim = N.new('ShaderNodeMath')
    rim.operation = 'POWER'
    L.new(lw.outputs['Facing'], rim.inputs[0])
    rim.inputs[1].default_value = 1.6
    em = N.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (0.25, 0.65, 1.0, 1.0)
    st = N.new('ShaderNodeMath')
    st.operation = 'MULTIPLY_ADD'
    L.new(rim.outputs[0], st.inputs[0])
    st.inputs[1].default_value = 3.0
    st.inputs[2].default_value = 0.15
    L.new(st.outputs[0], em.inputs['Strength'])
    tr = N.new('ShaderNodeBsdfTransparent')
    tr.inputs['Color'].default_value = (0.75, 0.9, 1.0, 1.0)
    add = N.new('ShaderNodeAddShader')
    L.new(tr.outputs[0], add.inputs[0])
    L.new(em.outputs[0], add.inputs[1])
    mix = N.new('ShaderNodeMixShader')
    L.new(amt.outputs[0], mix.inputs['Fac'])
    L.new(gi.outputs['Surface'], mix.inputs[1])
    L.new(add.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], go.inputs['Shader'])
    return g


def apply_to_material(mat):
    """Route a material's surface through the XrayMix group."""
    nt = mat.node_tree
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    link = next((l for l in nt.links if l.to_socket == out.inputs['Surface']), None)
    if link is None:
        return
    src = link.from_socket
    nt.links.remove(link)
    gn = nt.nodes.new('ShaderNodeGroup')
    gn.node_tree = xray_group()
    nt.links.new(src, gn.inputs['Surface'])
    nt.links.new(gn.outputs['Shader'], out.inputs['Surface'])


def key_amount(t_frames):
    """Keyframe the x-ray amount: [(frame, value), ...]."""
    node = xray_group().nodes['Amount']
    for f, v in t_frames:
        node.outputs[0].default_value = v
        node.outputs[0].keyframe_insert('default_value', frame=f)


def _bone_mat():
    m, n = new_material("XrayBone")
    lw = n.node('ShaderNodeLayerWeight', Blend=0.4)
    col = n.mix(lw.outputs['Facing'], (0.92, 0.96, 1.0), (0.55, 0.8, 1.0))
    bsdf = n.principled(base=col, roughness=0.35, coat=0.4, emission=(0.5, 0.75, 1.0),
                        emission_strength=n.math('MULTIPLY_ADD', lw.outputs['Facing'], 1.2, 0.25))
    n.out(bsdf)
    return m


def _glow_mat():
    """Joint capsules: warm glow, strength driven by the material's 'Glow' value (animated)."""
    m, n = new_material("JointGlow")
    v = n.node('ShaderNodeValue', _name='Glow')
    v.outputs[0].default_value = 0.0
    lw = n.node('ShaderNodeLayerWeight', Blend=0.5)
    em = n.node('ShaderNodeEmission', Color=(1.0, 0.72, 0.25),
                Strength=n.math('MULTIPLY', v.outputs[0], n.math('ADD', lw.outputs['Facing'], 0.3)))
    tr = n.node('ShaderNodeBsdfTransparent')
    mix = n.node('ShaderNodeMixShader', Fac=n.math('MULTIPLY', v.outputs[0], 0.25, clamp=True))
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(em.outputs[0], mix.inputs[2])
    n.out(mix)
    return m


def _bone_profile(L, r, head=1.35, base=1.25, n=20):
    """(r, z) lathe profile of a long bone of length L with flared base and rounded head."""
    zs = np.linspace(0, 1, n)
    prof = []
    for z in zs:
        waist = 0.62 + 0.38 * ((2 * z - 1) ** 4)
        flare = 1.0 + (base - 1.0) * max(0.0, 1 - z / 0.18) + (head - 1.0) * max(0.0, (z - 0.8) / 0.2)
        prof.append((r * waist * flare, z * L))
    prof = [(0.0, -r * 0.35)] + [(r * 0.8, 0.0)] + prof[1:-1] + [(r * head * 0.85, L), (r * 0.6, L + r * 0.6), (0.0, L + r * 0.75)]
    return np.array(prof)


def _parent_to_bone(ob, rig, bone):
    """Bone-parent keeping the current world transform (rig must be in rest pose)."""
    pb = rig.pose.bones[bone]
    tail = rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))
    ob.parent = rig
    ob.parent_type = 'BONE'
    ob.parent_bone = bone
    ob.matrix_parent_inverse = tail.inverted()


def build_hand_bones(rig, coll, side='R'):
    """Metacarpals, phalanges, carpals and the ends of radius/ulna, each skinned to its rig bone."""
    bone_m = _bone_mat()
    glow_m = _glow_mat()
    M = rig.matrix_world
    s = '.' + side
    joints = []
    objs = []

    def long_bone(name, a, b, r, frac0=0.0, frac1=1.0, head=1.35, base=1.25):
        a, b = Vector(a), Vector(b)
        p0 = a.lerp(b, frac0)
        p1 = a.lerp(b, frac1)
        L = (p1 - p0).length
        prof = _bone_profile(L * 0.94, r, head=head, base=base)
        v, f, uv = util.lathe(prof, segments=14)
        ax = (p1 - p0).normalized()
        Mx = Matrix(util.look_matrix(np.array(p0 + ax * L * 0.03), np.array(ax), np.array((0, 0, 1))).tolist()) \
            @ Matrix(((0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
        v = util.transform(v, Mx)
        return v, f

    b = rig.data.bones
    for finger, bones in (('thumb', ['finger1-1', 'finger1-2', 'finger1-3']),
                          ('index', ['metacarpal1', 'finger2-1', 'finger2-2', 'finger2-3']),
                          ('middle', ['metacarpal2', 'finger3-1', 'finger3-2', 'finger3-3']),
                          ('ring', ['metacarpal3', 'finger4-1', 'finger4-2', 'finger4-3']),
                          ('pinky', ['metacarpal4', 'finger5-1', 'finger5-2', 'finger5-3'])):
        r0 = FINGER_R[finger]
        for i, bn in enumerate(bones):
            bb = b[bn + s]
            h, t = M @ bb.head_local, M @ bb.tail_local
            meta = bn.startswith('metacarpal')
            r = r0 * (1.15 if meta else (1.0, 0.85, 0.72)[i - (0 if finger == 'thumb' else 1)])
            frac0 = 0.3 if meta else 0.04
            v, f = long_bone(bn, h, t, r, frac0=frac0, frac1=0.97, head=1.45 if meta else 1.3)
            ob = util.make_mesh('XBone_' + bn, v, f, coll=coll, mat=bone_m)
            _parent_to_bone(ob, rig, bn + s)
            objs.append(ob)
            if not meta and not (finger == 'thumb' and i == 0):   # MCP, PIP, DIP (thumb: MCP, IP)
                joints.append((bn + s, h, r * 1.7))
    # carpals: a cobbled cluster around the wrist
    wb = b['wrist' + s]
    wh = M @ wb.head_local
    mc_bases = [M @ b[f'metacarpal{k}' + s].head_local.lerp(b[f'metacarpal{k}' + s].tail_local, 0.22) for k in (1, 2, 3, 4)]
    rng = np.random.default_rng(7)
    mb = util.MeshBuilder()
    for row, frac in ((0, 0.35), (1, 0.75)):
        for k in range(4):
            c = wh.lerp(mc_bases[k], frac) + Vector(rng.normal(0, 0.0012, 3))
            v, f, uv = util.uv_sphere(0.0062, 10, 6, center=tuple(c), scale=(1.0, 0.85 + 0.2 * rng.random(), 0.8))
            mb.add(v, f, uv=uv)
    carp = mb.build('XBone_Carpals', coll, mats=[bone_m])
    _parent_to_bone(carp, rig, 'wrist' + s)
    objs.append(carp)
    # radius and ulna: distal ends of the forearm
    la = b['lowerarm02' + s]
    a, z = M @ la.head_local, M @ la.tail_local
    lat = (M @ b['metacarpal1' + s].tail_local - M @ b['metacarpal4' + s].tail_local).normalized()
    up = (z - a).normalized()
    lat = (lat - lat.dot(up) * up).normalized()
    for name, off, r in (('Radius', 0.011, 0.0085), ('Ulna', -0.011, 0.0065)):
        v, f = long_bone(name, a - up * 0.08 + lat * off, z - up * 0.004 + lat * off, r, head=1.6, base=1.0)
        ob = util.make_mesh('XBone_' + name, v, f, coll=coll, mat=bone_m)
        _parent_to_bone(ob, rig, 'lowerarm02' + s)
        objs.append(ob)
    # joint capsules (glow on "fluid")
    for bn, p, r in joints:
        v, f, uv = util.uv_sphere(r, 12, 8, center=tuple(p))
        ob = util.make_mesh('XJoint_' + bn, v, f, coll=coll, mat=glow_m)
        parent = rig.data.bones[bn].parent.name if rig.data.bones[bn].parent else bn
        _parent_to_bone(ob, rig, parent)
        ob.visible_shadow = False
        objs.append(ob)
    return objs, glow_m


def key_visibility(objs, f_on):
    """Bones exist only once the x-ray starts (hidden in shots where the skin is opaque)."""
    for ob in objs:
        for f, hide in ((1, True), (f_on, False)):
            ob.hide_render = hide
            ob.keyframe_insert('hide_render', frame=f)


def backdrop(cam, coll, dist=0.6):
    """Camera-locked dark blue screen that fades in behind the hand."""
    m, n = new_material("XrayBackdrop")
    v = n.node('ShaderNodeValue', _name='Amount')
    v.outputs[0].default_value = 0.0
    co = n.texcoord('Generated')
    sep = n.node('ShaderNodeSeparateXYZ', Vector=co)
    d = n.vmath('DISTANCE', co, (0.5, 0.5, 0.0))
    grad = n.ramp(d, [(0.0, (0.03, 0.10, 0.20)), (0.7, (0.005, 0.02, 0.05))])
    grid = n.maprange(n.math('ABSOLUTE', n.math('SINE', n.math('MULTIPLY', sep.outputs['Y'], 500.0))), 0.97, 1.0)
    col = n.mix(n.math('MULTIPLY', grid, 0.25), grad, (0.06, 0.22, 0.4))
    em = n.node('ShaderNodeEmission', Color=col, Strength=1.0)
    tr = n.node('ShaderNodeBsdfTransparent')
    mix = n.node('ShaderNodeMixShader', Fac=v.outputs[0])
    n.link(tr.outputs[0], mix.inputs[1])
    n.link(em.outputs[0], mix.inputs[2])
    n.out(mix)
    h = dist * 24.0 / cam.data.lens * 0.6
    w = h * 9 / 16 * 1.2
    verts = np.array([[-w, -h, -dist], [w, -h, -dist], [w, h, -dist], [-w, h, -dist]])
    ob = util.make_mesh('XrayBackdrop', verts, [[0, 1, 2, 3]], coll=coll, smooth=False, mat=m,
                        uv=np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float))
    ob.parent = cam
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_glossy = False
    return ob, v
