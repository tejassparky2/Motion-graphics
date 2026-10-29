"""Armature for the pelican: torso, neck chain, head, jaw, pouch, tail,
IK legs locked to the pedals.  Skin weights are computed procedurally."""
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector
from scipy.spatial import cKDTree

from . import pose as P
from .util import empty

DEFORM = ['torso', 'neck.1', 'neck.2', 'neck.3', 'neck.4', 'neck.5', 'head', 'tail']


def _seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / max(np.dot(ab, ab), 1e-12), 0, 1)
    return np.linalg.norm(p - (a + t[:, None] * ab), axis=1), t


def build(coll, bike, pel):
    frame = bike['frame']
    arm = bpy.data.armatures.new("PelicanRig")
    arm.display_type = 'STICK'
    rig = bpy.data.objects.new("PelicanRig", arm)
    coll.objects.link(rig)
    rig.parent = frame
    bpy.context.view_layer.objects.active = rig
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.edit_bones

    def bone(name, head, tail, parent=None, connect=False, deform=True, roll=0.0):
        b = eb.new(name)
        b.head = Vector(np.asarray(head, float))
        b.tail = Vector(np.asarray(tail, float))
        b.roll = roll
        b.use_deform = deform
        if parent:
            b.parent = eb[parent]
            b.use_connect = connect
        return b

    bone('root', (0.29, 0, 0.56), (0.29, 0, 0.66), deform=False)
    bone('torso', (0.29, 0, 0.60), (0.50, 0, 0.80), 'root')
    pts = P.NECK_PTS
    prev = 'torso'
    for i in range(5):
        bone(f'neck.{i + 1}', pts[i], pts[i + 1], prev, connect=(i > 0))
        prev = f'neck.{i + 1}'
    bone('head', pts[5], P.BILL_BASE, 'neck.5', connect=True)
    bone('jaw', P.JAW_HINGE, P.JAW_HINGE + P.BILL_DIR * 0.30, 'head')
    pouch_c = P.BILL_BASE + P.BILL_DIR * 0.10 - P.BILL_UP * 0.012
    bone('pouch', pouch_c, pouch_c - P.BILL_UP * 0.05, 'jaw')
    bone('tail', (0.12, 0, 0.635), (-0.03, 0, 0.605), 'torso')
    for s, nm in ((1, 'L'), (-1, 'R')):
        leg = pel['legs'][nm]
        bone(f'shin.{nm}', leg['knee'], leg['ankle'], 'torso')
        bone(f'tarsus.{nm}', leg['ankle'], leg['toe'], f'shin.{nm}', connect=True)
        bone(f'foot.{nm}', leg['toe'], leg['toe'] + np.array([0.08, 0, 0]), f'tarsus.{nm}', connect=True)
    bpy.ops.object.mode_set(mode='OBJECT')

    # ---- IK targets on the pedals -------------------------------------------------
    bpy.context.view_layer.update()
    targets = {}
    for s, nm in ((1, 'L'), (-1, 'R')):
        leg = pel['legs'][nm]
        pedal = bike['pedals'][nm]
        tgt = empty(f"FootTarget.{nm}", coll, size=0.03, kind='SPHERE')
        tgt.parent = pedal
        tgt.matrix_parent_inverse = pedal.matrix_world.inverted()
        tgt.location = tuple(leg['toe'])
        pole = empty(f"KneePole.{nm}", coll, size=0.03, kind='CONE')
        pole.parent = rig
        pole.parent_type = 'BONE'
        pole.parent_bone = 'torso'
        bpy.context.view_layer.update()
        pole.matrix_world = Matrix.Translation(Vector(leg['knee'] + np.array([-0.45, 0.02 * s, -0.10])))
        pb = rig.pose.bones[f'tarsus.{nm}']
        ik = pb.constraints.new('IK')
        ik.target = tgt
        ik.pole_target = pole
        ik.chain_count = 2
        ik.use_tail = True
        # pole angle chosen so the rest pose is preserved (computed below)
        ik.pole_angle = _pole_angle(rig, f'shin.{nm}', pole, f'tarsus.{nm}')
        cr = rig.pose.bones[f'foot.{nm}'].constraints.new('COPY_ROTATION')
        cr.target = tgt
        cr.mix_mode = 'REPLACE'
        cr.target_space = 'WORLD'
        cr.owner_space = 'WORLD'
        targets[nm] = tgt
        # the target's rest orientation must equal the foot bone's rest orientation
        bpy.context.view_layer.update()
        fb = rig.data.bones[f'foot.{nm}']
        Mfoot = rig.matrix_world @ fb.matrix_local
        tgt.matrix_world = Mfoot
    for nm in ('L', 'R'):
        rig.pose.bones[f'shin.{nm}'].ik_stretch = 0.0
    _skin(rig, pel, coll)
    return dict(rig=rig, targets=targets)


def _pole_angle(rig, base_bone, pole, ik_bone=None):
    """Pole angle that keeps an IK chain in its rest plane."""
    bpy.context.view_layer.update()
    M = rig.matrix_world
    b = rig.data.bones[base_bone]
    ik = rig.data.bones[ik_bone] if ik_bone else b
    head = M @ b.head_local
    tail = M @ b.tail_local
    chain_end = M @ ik.tail_local
    x_axis = (M.to_3x3() @ b.matrix_local.to_3x3()) @ Vector((1, 0, 0))
    pole_loc = pole.matrix_world.translation
    pole_normal = (chain_end - head).cross(pole_loc - head)
    projected = pole_normal.cross(tail - head)
    ang = x_axis.angle(projected)
    if (tail - head).dot(x_axis.cross(projected)) < 0:
        ang = -ang
    return ang


def _assign(ob, rig, weights):
    """weights: dict bone -> (N,) array."""
    for name, w in weights.items():
        vg = ob.vertex_groups.get(name) or ob.vertex_groups.new(name=name)
        idx = np.nonzero(w > 1e-3)[0]
        if len(idx) == 0:
            continue
        # group by quantised weight for speed
        q = np.round(w[idx], 3)
        for val in np.unique(q):
            sel = idx[q == val].tolist()
            vg.add(sel, float(val), 'REPLACE')
    mod = ob.modifiers.new("Armature", 'ARMATURE')
    mod.object = rig
    mod.use_deform_preserve_volume = True
    ob.modifiers.move(len(ob.modifiers) - 1, 0)


def _body_weights(V):
    """Smooth weights for body / neck / head / tail from bone capsules."""
    segs = {'torso': (np.array([0.10, 0, 0.64]), np.array([0.50, 0, 0.80])),
            'tail': (np.array([0.10, 0, 0.635]), np.array([-0.05, 0, 0.60]))}
    pts = P.NECK_PTS
    for i in range(5):
        segs[f'neck.{i + 1}'] = (pts[i], pts[i + 1])
    segs['head'] = (pts[5], P.BILL_BASE + P.BILL_DIR * 0.02)
    sig = {'torso': 0.10, 'tail': 0.05, 'head': 0.035}
    raw = {}
    for name, (a, b) in segs.items():
        d, t = _seg_dist(V, a, b)
        s = sig.get(name, 0.028)
        raw[name] = np.exp(-(d / s) ** 2) + 1e-9
    # vertices well inside the body hull belong to the torso
    tot = sum(raw.values())
    W = {k: v / tot for k, v in raw.items()}
    # sharpen: keep the head rigid
    return W


def _skin(rig, pel, coll):
    body = pel['body']
    V = np.array([v.co[:] for v in body.data.vertices])
    W = _body_weights(V)
    _assign(body, rig, W)
    # plumage: copy from nearest body vertex, with overrides per region
    arr = pel['plumage_arrays']
    PV = arr['V']
    tree = cKDTree(V)
    _, nn = tree.query(PV)
    PW = {k: w[nn].copy() for k, w in W.items()}
    reg = arr['region']
    side = arr['side']
    names = list(PW.keys()) + ['shin.L', 'shin.R']
    for k in ('shin.L', 'shin.R'):
        PW[k] = np.zeros(len(PV))
    def force(mask, bone):
        for k in names:
            PW[k][mask] = 0.0
        PW[bone][mask] = 1.0
    force(reg == 2, 'torso')
    force(reg == 3, 'head')
    force((reg == 4), 'shin.L')
    force((reg == 5), 'shin.R')
    _assign(pel['plumage'], rig, PW)
    # wing leading edges ride with the torso
    for nm in ('L', 'R'):
        ob = bpy.data.objects.get(f"WingEdge.{nm}")
        if ob:
            _assign(ob, rig, {'torso': np.ones(len(ob.data.vertices))})
    # legs: shin / tarsus by arc length
    for nm in ('L', 'R'):
        leg = pel['legs'][nm]
        ob = leg['leg']
        LV = np.array([v.co[:] for v in ob.data.vertices])
        ds, _ = _seg_dist(LV, leg['knee'], leg['ankle'])
        dt, _ = _seg_dist(LV, leg['ankle'], leg['toe'])
        ws = np.exp(-(ds / 0.012) ** 2)
        wt = np.exp(-(dt / 0.012) ** 2)
        tot = ws + wt + 1e-9
        _assign(ob, rig, {f'shin.{nm}': ws / tot, f'tarsus.{nm}': wt / tot})
        _bone_parent(leg['foot'], rig, f'foot.{nm}')
    # bill, eyes -> head; lower mandible -> jaw; pouch -> jaw/pouch/head
    _bone_parent(pel['upper'], rig, 'head')
    for e in pel['eyes']:
        _bone_parent(e, rig, 'head')
    _bone_parent(pel['lower'], rig, 'jaw')
    pouch = pel['pouch']
    PV = np.array([v.co[:] for v in pouch.data.vertices])
    rel = PV - P.BILL_BASE
    along = rel @ P.BILL_DIR
    depth = -(rel @ P.BILL_UP)
    w_pouch = np.clip((depth - 0.006) / 0.04, 0, 1) * np.clip((along + 0.05) / 0.08, 0, 1) * 0.8
    w_head = np.clip(-(along + 0.01) / 0.06, 0, 1)
    w_jaw = np.clip(1 - w_head - w_pouch, 0, 1)
    tot = w_pouch + w_head + w_jaw + 1e-9
    _assign(pouch, rig, {'pouch': w_pouch / tot, 'head': w_head / tot, 'jaw': w_jaw / tot})


def _bone_parent(ob, rig, bone):
    bpy.context.view_layer.update()
    mw = ob.matrix_world.copy()
    ob.parent = rig
    ob.parent_type = 'BONE'
    ob.parent_bone = bone
    bpy.context.view_layer.update()
    ob.matrix_world = mw
