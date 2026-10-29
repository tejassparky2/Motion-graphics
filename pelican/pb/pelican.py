"""Assembles the great white pelican rider (geometry in bike space)."""
import math
import time

import bpy
import numpy as np

from . import bicycle as B
from . import pelican_materials as pm
from . import pelican_parts as parts
from . import feathers as FE
from . import pose as P
from .pelican_body import build_body_mesh
from .util import MeshBuilder, make_mesh, look_matrix, transform, smoothstep, sweep, uv_sphere


def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(((p - a) @ ab) / np.dot(ab, ab), 0, 1)
    q = a + t[:, None] * ab
    return np.linalg.norm(p - q, axis=1)


def skin_mask(V):
    """Bare facial skin around the eye and toward the bill base."""
    skin = np.zeros(len(V))
    for s in (1, -1):
        eye = P.EYE * np.array([1, s, 1])
        bb = P.BILL_BASE + np.array([0.004, s * 0.021, -0.006])
        d = seg_dist(V, eye, bb)
        m = 1 - smoothstep(0.013, 0.021, d)
        m *= (V[:, 1] * s > 0.008)
        skin = np.maximum(skin, m)
        d2 = seg_dist(V, eye, P.JAW_HINGE + np.array([0.0, s * 0.030, -0.004]))
        skin = np.maximum(skin, (1 - smoothstep(0.004, 0.009, d2)) * (V[:, 1] * s > 0.01))
    return skin


def _add_fuzz(body, V, mats):
    """Short velvety down on the head and neck: softens silhouettes and rim light."""
    from .feathers import region_weights
    head, neck, tau = region_weights(V)
    w = np.clip(head + neck * 0.9, 0, 1) * (1 - skin_mask(V))
    vg = body.vertex_groups.new(name="fuzz")
    q = np.round(w, 2)
    for val in np.unique(q):
        if val <= 0:
            continue
        vg.add(np.nonzero(q == val)[0].tolist(), float(val), 'REPLACE')
    ps_mod = body.modifiers.new("Fuzz", 'PARTICLE_SYSTEM')
    psys = ps_mod.particle_system
    s = psys.settings
    s.type = 'HAIR'
    s.count = 36000
    s.hair_length = 0.0055
    s.emit_from = 'FACE'
    s.use_emit_random = True
    s.use_even_distribution = True
    s.distribution = 'RAND'
    s.hair_step = 3
    s.display_step = 2
    s.render_step = 3
    s.use_advanced_hair = True
    s.normal_factor = 1.0
    s.factor_random = 0.6
    s.brownian_factor = 0.0
    s.root_radius = 1.0
    s.tip_radius = 0.0
    s.radius_scale = 0.00045
    psys.vertex_group_density = "fuzz"
    psys.seed = 11
    fm = pm.fuzz()
    body.data.materials.append(fm)
    s.material_slot = fm.name
    return psys


def pedal_rest(side):
    """Pedal centre (bike space) at crank angle 0. side +1 = left."""
    x = -B.CRANK if side > 0 else B.CRANK
    return B.BB + np.array([x, side * (0.064 + 0.059), 0.0])


def toe_joint_rest(side):
    return pedal_rest(side) + np.array([-0.016, 0.0, 0.027])


def build(coll, bike):
    t0 = time.time()
    mats = dict(down=pm.body_down(), bill=pm.bill(), pouch=pm.pouch(), leg=pm.leg_skin(),
                web=pm.leg_skin("WebSkin", web=True), claw=pm.claw(), iris=pm.iris(),
                cornea=pm.cornea(), lid=pm.eyelid(), feather=pm.feather())
    frame = bike['frame']

    # ---- body ---------------------------------------------------------------
    V, F = build_body_mesh()
    print(f"  body sdf: {len(V)} verts in {time.time() - t0:.1f}s")
    body = make_mesh("PelicanBody", V, F, coll=coll, mat=mats['down'], parent=frame)
    skin = skin_mask(V)
    chest = np.array(P.CHEST['c'])
    blush = 0.25 + 0.55 * (1 - smoothstep(0.05, 0.22, np.linalg.norm(V - chest, axis=1)))
    for name, data in (('skin', skin), ('blush', blush)):
        a = body.data.attributes.new(name, 'FLOAT', 'POINT')
        a.data.foreach_set('value', data.astype(np.float32))

    # ---- bill ---------------------------------------------------------------
    v, f, uv = parts.upper_mandible()
    upper = make_mesh("BillUpper", v, f, coll=coll, uv=uv, mat=mats['bill'], parent=frame)
    lower = parts.lower_mandible().build("BillLower", coll, mats=[mats['bill']], parent=frame)
    v, f, uv = parts.pouch()
    pouch = make_mesh("Pouch", v, f, coll=coll, uv=uv, mat=mats['pouch'], parent=frame)
    sol = pouch.modifiers.new("Thick", 'SOLIDIFY')
    sol.thickness = 0.0014
    sol.offset = 0.0
    sub = pouch.modifiers.new("Subsurf", 'SUBSURF')
    sub.levels = 1
    sub.render_levels = 1

    # ---- eyes ---------------------------------------------------------------
    eyes = []
    for s, nm in ((1, 'L'), (-1, 'R')):
        (ev, ef, euv), (cv, cf, cuv), (lv, lf, luv), M = parts.eye_parts(s)
        mb = MeshBuilder()
        mb.add(ev, ef, euv, mat=0)
        mb.add(cv, cf, cuv, mat=1)
        mb.add(lv, lf, luv, mat=2)
        eye = mb.build(f"Eye.{nm}", coll, mats=[mats['iris'], mats['cornea'], mats['lid']], parent=frame)
        eyes.append(eye)

    # ---- legs ---------------------------------------------------------------
    legs = {}
    for s, nm in ((1, 'L'), (-1, 'R')):
        knee = P.KNEE * np.array([1, s, 1])
        toe = toe_joint_rest(s)
        ankle, toe_end = parts.two_bone_ik(knee, toe, P.SHIN_LEN, P.TARSUS_LEN, np.array([-1.0, 0, 0.15]))
        path = parts.leg_path(knee, ankle, toe_end)
        n = len(path)
        seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
        u = seg / seg[-1]
        rad = np.interp(u, [0, 0.15, 0.50, 0.57, 0.62, 0.9, 1.0],
                        [0.030, 0.024, 0.0165, 0.0185, 0.0150, 0.0138, 0.0150])
        sc = np.stack([np.ones(n), np.interp(u, [0, 0.5, 1], [1.0, 0.85, 0.75])], 1)
        lv, lf, luv = sweep(path, rad, 20, scale2=sc, up=np.array([0, 1.0, 0]))
        leg = make_mesh(f"Leg.{nm}", lv, lf, coll=coll, uv=luv, mat=mats['leg'], parent=frame)
        fmb = parts.foot_geometry(s)
        foot = fmb.build(f"Foot.{nm}", coll, mats=[mats['leg'], mats['claw'], mats['web']], parent=frame)
        foot.location = tuple(toe_end)
        legs[nm] = dict(leg=leg, foot=foot, knee=knee, ankle=ankle, toe=toe_end, path=path)

    # ---- plumage ------------------------------------------------------------
    plum = FE.Plumage()
    nb = FE.body_feathers(plum, V, F, skin_mask)
    print(f"  body feathers: {nb} ({time.time() - t0:.1f}s)")
    wings = {}
    for s, nm in ((1, 'L'), (-1, 'R')):
        g0, g1 = bike['grips'][nm]
        wrist = (np.asarray(g0) * 0.45 + np.asarray(g1) * 0.55) + np.array([0.0, 0.0, 0.029])
        elbow = np.array([0.335, 0.140 * s, 0.790])
        tip = np.array([0.420, 0.166 * s, 0.735])
        FE.wing_feathers(plum, s, wrist, elbow, tip)
        edge = np.array([elbow + np.array([0.0, -0.012 * s, 0.006]), (elbow + wrist) / 2 + np.array([0, 0.004 * s, 0.006]),
                         wrist + np.array([0.004, 0, 0.002])])
        from .util import catmull
        ep = catmull(edge, 10)
        ev, ef, euv = sweep(ep, np.interp(np.linspace(0, 1, len(ep)), [0, 0.15, 0.7, 0.93, 1], [0.004, 0.013, 0.012, 0.010, 0.003]), 16)
        make_mesh(f"WingEdge.{nm}", ev, ef, coll=coll, uv=euv, mat=mats['down'], parent=frame)
        wings[nm] = dict(wrist=wrist, elbow=elbow, tip=tip, shoulder=P.SHOULDER * np.array([1, s, 1]))
    FE.tail_feathers(plum)
    FE.crest_feathers(plum)
    FE.trouser_feathers(plum, [(1, legs['L']['path']), (-1, legs['R']['path'])])
    arr = plum.arrays()
    plumage = make_mesh("Plumage", arr['V'], arr['F'], coll=coll, uv=arr['UV'], mat=mats['feather'],
                        parent=frame)
    me = plumage.data
    a = me.attributes.new('fcol', 'FLOAT_COLOR', 'POINT')
    a.data.foreach_set('color', np.hstack([arr['col'], np.ones((len(arr['col']), 1))]).astype(np.float32).ravel())
    a = me.attributes.new('shadowless', 'FLOAT', 'POINT')
    a.data.foreach_set('value', (arr['region'] == 0).astype(np.float32))
    for nm in ('dark', 'flex', 'side'):
        a = me.attributes.new(nm, 'FLOAT', 'POINT')
        a.data.foreach_set('value', arr[nm].astype(np.float32))
    a = me.attributes.new('region', 'INT', 'POINT')
    a.data.foreach_set('value', arr['region'].astype(np.int32))
    reg = arr['region']
    xfer = np.select([reg == 0, reg == 1, reg == 2, reg == 3], [0.85, 0.85, 0.12, 0.15], 0.25)
    xfer = np.where(arr['dark'] > 0.5, 0.0, xfer)
    xfer = xfer * (0.55 + 0.45 * np.clip(arr['flex'], 0, 1))
    vg = plumage.vertex_groups.new(name="normal_xfer")
    for val in np.unique(np.round(xfer, 2)):
        idx = np.nonzero(np.abs(np.round(xfer, 2) - val) < 1e-6)[0].tolist()
        vg.add(idx, float(val), 'REPLACE')
    dt = plumage.modifiers.new("SoftNormals", 'DATA_TRANSFER')
    dt.object = body
    dt.use_loop_data = True
    dt.data_types_loops = {'CUSTOM_NORMAL'}
    dt.loop_mapping = 'POLYINTERP_NEAREST'
    dt.vertex_group = "normal_xfer"
    dt.mix_factor = 1.0
    print(f"  plumage: {plum.count} feathers, {len(arr['V'])} verts ({time.time() - t0:.1f}s)")
    print(f"  pelican parts built in {time.time() - t0:.1f}s")
    return dict(body=body, upper=upper, lower=lower, pouch=pouch, eyes=eyes, legs=legs, mats=mats,
                plumage=plumage, plumage_arrays=arr, wings=wings, body_VF=(V, F))
