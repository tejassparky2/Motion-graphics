"""Sculpt smooth creature bodies from signed-distance primitives (smooth-unioned, so a claw grows out of an arm and an
arm out of a body with no seams), polygonised with marching cubes and Taubin-smoothed (the pelican film's method).

Each primitive carries a material name; every face takes the material of the primitive nearest to it."""
import bmesh
import bpy
import numpy as np
from skimage import measure


def ellipsoid(c, r):
    c, r = np.asarray(c, float), np.asarray(r, float)

    def f(p):
        q = (p - c) / r
        k0 = np.linalg.norm(q, axis=-1)
        k1 = np.linalg.norm(q / r, axis=-1)
        return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)
    return f


def capsule(a, b, ra, rb=None):
    """A round cone from a (radius ra) to b (radius rb)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rb = ra if rb is None else rb

    def f(p):
        pa, ba = p - a, b - a
        h = np.clip((pa @ ba) / (ba @ ba), 0.0, 1.0)
        return np.linalg.norm(pa - h[..., None] * ba, axis=-1) - (ra + (rb - ra) * h)
    return f


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def build(name, parts, k=0.12, res=0.025, pad=0.25, smooth_iter=12):
    """parts: [(sdf, material_name, blend_k or None)]. Returns a Blender mesh object with per-face materials."""
    pts_lo, pts_hi = [], []
    for f, _, _ in parts:
        lo, hi = f.bounds
        pts_lo.append(lo)
        pts_hi.append(hi)
    lo = np.min(pts_lo, axis=0) - pad
    hi = np.max(pts_hi, axis=0) + pad
    axes = [np.arange(lo[i], hi[i], res) for i in range(3)]
    P = np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1)
    flat = P.reshape(-1, 3)
    dists = [f(flat) for f, _, _ in parts]
    d = dists[0]
    for di, (_, _, kk) in zip(dists[1:], parts[1:]):
        d = smin(d, di, k if kk is None else kk) if (k if kk is None else kk) > 0 else np.minimum(d, di)
    vol = d.reshape(P.shape[:3])
    verts, faces, _, _ = measure.marching_cubes(vol, 0.0, spacing=(res, res, res))
    verts += lo
    faces = faces[:, ::-1]                                     # marching cubes winds them inward
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts.tolist(), [], faces.tolist())
    me.update()
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=res * 0.2)
    # face outward whichever way marching cubes wound them: with scikit-image 0.26 the flip above left them inward,
    # which hid every SDF body's inverted-hull outline (helper 5, 30 Oct)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    sm = o.modifiers.new("smooth", "LAPLACIANSMOOTH")
    sm.iterations = smooth_iter
    sm.lambda_factor = 0.5
    sm.use_volume_preserve = True
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.modifier_apply(modifier="smooth")
    # per-face material: the nearest primitive wins
    mats = []
    for _, mname, _ in parts:
        if mname not in mats:
            mats.append(mname)
    for mname in mats:
        o.data.materials.append(bpy.data.materials[mname])
    centers = np.array([p.center for p in o.data.polygons])
    near = np.argmin(np.stack([f(centers) for f, _, _ in parts], axis=0), axis=0)
    idx = np.array([mats.index(parts[i][1]) for i in near])
    o.data.polygons.foreach_set("material_index", idx.astype(np.int32))
    o.data.polygons.foreach_set("use_smooth", np.ones(len(o.data.polygons), dtype=bool))
    o.data.update()
    return o


def with_bounds(f, lo, hi):
    f.bounds = (np.asarray(lo, float), np.asarray(hi, float))
    return f


def E(c, r):
    c, r = np.asarray(c, float), np.asarray(r, float)
    return with_bounds(ellipsoid(c, r), c - r, c + r)


def C(a, b, ra, rb=None):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = max(ra, rb or ra)
    return with_bounds(capsule(a, b, ra, rb), np.minimum(a, b) - m, np.maximum(a, b) + m)
