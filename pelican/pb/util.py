"""Geometry and scene helpers shared by every builder module.

Everything is generated procedurally with numpy and pushed into Blender
meshes through the fast ``foreach_set`` path.
"""
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector


# ---------------------------------------------------------------------------
# Scene / collections
# ---------------------------------------------------------------------------

def clear_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.curves,
                 bpy.data.armatures, bpy.data.cameras, bpy.data.lights,
                 bpy.data.node_groups, bpy.data.images, bpy.data.textures,
                 bpy.data.actions, bpy.data.worlds):
        for block in list(coll):
            coll.remove(block)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def collection(name, parent=None):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(coll)
    return coll


def empty(name, coll, loc=(0, 0, 0), parent=None, size=0.1, kind='PLAIN_AXES'):
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_type = kind
    ob.empty_display_size = size
    coll.objects.link(ob)
    if parent is not None:
        ob.parent = parent
    ob.location = loc
    return ob


def parent_keep(child, parent):
    """Parent without moving the child in world space."""
    mw = child.matrix_world.copy()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()
    child.matrix_world = mw


# ---------------------------------------------------------------------------
# Mesh construction
# ---------------------------------------------------------------------------

def make_mesh(name, verts, faces, coll=None, smooth=True, uv=None,
              mat=None, loc=None, parent=None):
    """Create a mesh object.

    verts: (N,3) array.  faces: (M,k) int array or list of index sequences.
    uv: optional per-vertex (N,2) array or per-loop (L,2) array.
    """
    verts = np.asarray(verts, dtype=np.float32).reshape(-1, 3)
    if isinstance(faces, np.ndarray) and faces.ndim == 2:
        sizes = np.full(len(faces), faces.shape[1], dtype=np.int32)
        flat = faces.astype(np.int32).ravel()
    else:
        sizes = np.array([len(f) for f in faces], dtype=np.int32)
        flat = np.fromiter((i for f in faces for i in f), dtype=np.int32,
                           count=int(sizes.sum()))
    starts = np.zeros(len(sizes), dtype=np.int32)
    if len(sizes) > 1:
        starts[1:] = np.cumsum(sizes)[:-1]
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(verts))
    me.vertices.foreach_set("co", verts.ravel())
    me.loops.add(len(flat))
    me.loops.foreach_set("vertex_index", flat)
    me.polygons.add(len(sizes))
    me.polygons.foreach_set("loop_start", starts)
    me.polygons.foreach_set("loop_total", sizes)
    me.update(calc_edges=True)
    if uv is not None:
        uv = np.asarray(uv, dtype=np.float32)
        layer = me.uv_layers.new(name="UVMap")
        if len(uv) == len(verts):
            uv = uv[flat]
        layer.data.foreach_set("uv", uv.ravel())
    me.validate(clean_customdata=False)
    if smooth:
        me.polygons.foreach_set("use_smooth", np.ones(len(me.polygons), dtype=bool))
    if mat is not None:
        mats = mat if isinstance(mat, (list, tuple)) else [mat]
        for m in mats:
            me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    (coll or bpy.context.scene.collection).objects.link(ob)
    if parent is not None:
        ob.parent = parent
    if loc is not None:
        ob.location = loc
    return ob


class MeshBuilder:
    """Accumulates many parts into one mesh (with per-face material index
    and optional per-vertex float / colour attributes)."""

    def __init__(self):
        self.parts = []
        self.nv = 0

    def add(self, verts, faces, uv=None, mat=0, **attrs):
        verts = np.asarray(verts, dtype=np.float64).reshape(-1, 3)
        if isinstance(faces, np.ndarray):
            faces = faces.tolist()
        if uv is None:
            uv = np.zeros((len(verts), 2))
        self.parts.append(dict(v=verts, f=[[i + self.nv for i in f] for f in faces],
                               uv=np.asarray(uv, dtype=np.float64).reshape(-1, 2),
                               mat=mat, attrs=attrs))
        self.nv += len(verts)
        return self

    def build(self, name, coll=None, mats=None, smooth=True, parent=None):
        V = np.concatenate([p['v'] for p in self.parts])
        UV = np.concatenate([p['uv'] for p in self.parts])
        F = [f for p in self.parts for f in p['f']]
        ob = make_mesh(name, V, F, coll=coll, smooth=smooth, uv=UV, mat=mats, parent=parent)
        if mats and len(mats) > 1:
            mi = np.concatenate([np.full(len(p['f']), p['mat'], dtype=np.int32) for p in self.parts])
            ob.data.polygons.foreach_set("material_index", mi)
        keys = {k for p in self.parts for k in p['attrs']}
        for k in sorted(keys):
            chunks = []
            dim = 1
            for p in self.parts:
                if k in p['attrs']:
                    a = np.asarray(p['attrs'][k], dtype=np.float64)
                    if a.ndim == 1 and len(a) in (3, 4) and len(p['v']) != len(a):
                        dim = len(a)
                    elif a.ndim == 2:
                        dim = a.shape[1]
            for p in self.parts:
                n = len(p['v'])
                a = np.asarray(p['attrs'].get(k, 0.0), dtype=np.float64)
                if dim == 1:
                    a = np.broadcast_to(a, (n,))
                else:
                    if a.ndim <= 1 and a.size != n * dim:
                        a = np.broadcast_to(a if a.ndim == 1 else np.full(dim, float(a)), (n, dim))
                    a = a.reshape(n, dim)
                chunks.append(np.array(a))
            data = np.concatenate(chunks)
            if dim == 1:
                at = ob.data.attributes.new(k, 'FLOAT', 'POINT')
                at.data.foreach_set("value", data.astype(np.float32))
            else:
                if dim == 3:
                    data = np.concatenate([data, np.ones((len(data), 1))], axis=1)
                at = ob.data.attributes.new(k, 'FLOAT_COLOR', 'POINT')
                at.data.foreach_set("color", data.astype(np.float32).ravel())
        ob.data.update()
        return ob


def grid_faces(nu, nv, wrap_u=False, wrap_v=False):
    """Quad faces for a vertex grid indexed [iu*nv + iv]."""
    us = nu if wrap_u else nu - 1
    vs = nv if wrap_v else nv - 1
    iu, iv = np.meshgrid(np.arange(us), np.arange(vs), indexing='ij')
    iu, iv = iu.ravel(), iv.ravel()
    iu1 = (iu + 1) % nu
    iv1 = (iv + 1) % nv
    return np.stack([iu * nv + iv, iu1 * nv + iv, iu1 * nv + iv1, iu * nv + iv1], axis=1)


def _normalize(v, axis=-1):
    n = np.linalg.norm(v, axis=axis, keepdims=True)
    return v / np.maximum(n, 1e-12)


def rmf_frames(pts, up=None, closed=False):
    """Rotation minimising frames along a polyline. Returns T, N, B arrays."""
    pts = np.asarray(pts, dtype=np.float64)
    n = len(pts)
    if closed:
        T = _normalize(np.roll(pts, -1, 0) - np.roll(pts, 1, 0))
    else:
        T = np.zeros_like(pts)
        T[1:-1] = pts[2:] - pts[:-2]
        T[0] = pts[1] - pts[0]
        T[-1] = pts[-1] - pts[-2]
        T = _normalize(T)
    if up is None:
        up = np.array([0.0, 0.0, 1.0])
        if abs(np.dot(up, T[0])) > 0.9:
            up = np.array([0.0, 1.0, 0.0])
    up = np.asarray(up, dtype=np.float64)
    N = np.zeros_like(pts)
    N[0] = _normalize(up - np.dot(up, T[0]) * T[0])
    for i in range(n - 1):
        # double reflection (Wang et al. 2008)
        v1 = pts[i + 1] - pts[i]
        c1 = np.dot(v1, v1)
        if c1 < 1e-18:
            N[i + 1] = N[i]
            continue
        rL = N[i] - (2.0 / c1) * np.dot(v1, N[i]) * v1
        tL = T[i] - (2.0 / c1) * np.dot(v1, T[i]) * v1
        v2 = T[i + 1] - tL
        c2 = np.dot(v2, v2)
        N[i + 1] = rL - (2.0 / c2) * np.dot(v2, rL) * v2 if c2 > 1e-18 else rL
        N[i + 1] = _normalize(N[i + 1] - np.dot(N[i + 1], T[i + 1]) * T[i + 1])
    B = np.cross(T, N)
    return T, N, B


def circle_profile(n, r=1.0):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([np.cos(a) * r, np.sin(a) * r], axis=1)


def sweep(path, radius=0.01, sides=12, profile=None, closed=False, caps=True,
          up=None, twist=0.0, scale2=None):
    """Sweep a 2D profile along a 3D path.

    radius: scalar or per-point array (scales the profile).
    scale2: optional (n,2) per-point anisotropic scale for the profile.
    Returns verts, faces, uv.
    """
    path = np.asarray(path, dtype=np.float64)
    n = len(path)
    T, N, B = rmf_frames(path, up=up, closed=closed)
    prof = circle_profile(sides) if profile is None else np.asarray(profile, dtype=np.float64)
    k = len(prof)
    r = np.broadcast_to(np.asarray(radius, dtype=np.float64), (n,))
    s2 = np.ones((n, 2)) if scale2 is None else np.asarray(scale2, dtype=np.float64)
    tw = np.linspace(0, twist, n)
    verts = np.zeros((n, k, 3))
    for i in range(n):
        c, s = math.cos(tw[i]), math.sin(tw[i])
        px = (prof[:, 0] * c - prof[:, 1] * s) * r[i] * s2[i, 0]
        py = (prof[:, 0] * s + prof[:, 1] * c) * r[i] * s2[i, 1]
        verts[i] = path[i] + px[:, None] * N[i] + py[:, None] * B[i]
    verts = verts.reshape(-1, 3)
    faces = grid_faces(n, k, wrap_u=closed, wrap_v=True).tolist()
    seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    uu = np.repeat(seg / max(seg[-1], 1e-9), k)
    vv = np.tile(np.arange(k) / k, n)
    uv = np.stack([uu, vv], axis=1)
    if caps and not closed:
        c0 = len(verts)
        verts = np.vstack([verts, path[0], path[-1]])
        uv = np.vstack([uv, [[0, 0], [1, 0]]])
        for j in range(k):
            j1 = (j + 1) % k
            faces.append([c0, j1, j])
            faces.append([c0 + 1, (n - 1) * k + j, (n - 1) * k + j1])
    return verts, faces, uv


def lathe(profile_rz, segments=48, closed_top=False, angle=2 * np.pi):
    """Revolve a (r,z) polyline around Z. Returns verts, faces, uv."""
    prof = np.asarray(profile_rz, dtype=np.float64)
    m = len(prof)
    full = abs(angle - 2 * np.pi) < 1e-6
    nseg = segments if full else segments + 1
    a = np.linspace(0, angle, segments, endpoint=False) if full else np.linspace(0, angle, nseg)
    verts = np.zeros((nseg, m, 3))
    verts[:, :, 0] = np.cos(a)[:, None] * prof[None, :, 0]
    verts[:, :, 1] = np.sin(a)[:, None] * prof[None, :, 0]
    verts[:, :, 2] = prof[None, :, 1]
    faces = grid_faces(nseg, m, wrap_u=full, wrap_v=closed_top)
    uv = np.stack(np.meshgrid(np.arange(nseg) / nseg, np.linspace(0, 1, m), indexing='ij'), -1)
    return verts.reshape(-1, 3), faces, uv.reshape(-1, 2)


def loft(rings, closed_rings=True, cap_start=False, cap_end=False):
    """Skin a list of rings (each (k,3)) into a surface."""
    rings = np.asarray(rings, dtype=np.float64)
    n, k, _ = rings.shape
    verts = rings.reshape(-1, 3)
    faces = grid_faces(n, k, wrap_v=closed_rings).tolist()
    uv = np.stack(np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, k), indexing='ij'), -1).reshape(-1, 2)
    if cap_start or cap_end:
        verts = list(verts)
        uvl = list(uv)
        if cap_start:
            c = len(verts)
            verts.append(rings[0].mean(0))
            uvl.append([0, 0.5])
            for j in range(k):
                faces.append([c, (j + 1) % k, j])
        if cap_end:
            c = len(verts)
            verts.append(rings[-1].mean(0))
            uvl.append([1, 0.5])
            for j in range(k):
                faces.append([c, (n - 1) * k + j, (n - 1) * k + (j + 1) % k])
        verts = np.array(verts)
        uv = np.array(uvl)
    return verts, faces, uv


def box(size, center=(0, 0, 0)):
    sx, sy, sz = np.asarray(size) / 2
    v = np.array([[-sx, -sy, -sz], [sx, -sy, -sz], [sx, sy, -sz], [-sx, sy, -sz],
                  [-sx, -sy, sz], [sx, -sy, sz], [sx, sy, sz], [-sx, sy, sz]]) + np.asarray(center)
    f = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    uv = v[:, :2] * 0 + np.array([[0, 0], [1, 0], [1, 1], [0, 1]] * 2)
    return v, f, uv


def uv_sphere(r=1.0, nu=24, nv=12, center=(0, 0, 0), scale=(1, 1, 1)):
    th = np.linspace(0, np.pi, nv + 1)[1:-1]
    ph = np.linspace(0, 2 * np.pi, nu, endpoint=False)
    T, P = np.meshgrid(th, ph, indexing='ij')
    v = np.stack([np.sin(T) * np.cos(P), np.sin(T) * np.sin(P), np.cos(T)], -1).reshape(-1, 3)
    v = np.vstack([v, [[0, 0, 1], [0, 0, -1]]])
    faces = grid_faces(nv - 1, nu, wrap_v=True).tolist()
    top, bot = len(v) - 2, len(v) - 1
    for j in range(nu):
        faces.append([top, j, (j + 1) % nu])
        faces.append([bot, (nv - 2) * nu + (j + 1) % nu, (nv - 2) * nu + j])
    uv = np.zeros((len(v), 2))
    uv[:-2, 0] = (P.ravel() / (2 * np.pi))
    uv[:-2, 1] = 1 - T.ravel() / np.pi
    uv[-2] = [0.5, 1]
    uv[-1] = [0.5, 0]
    v = v * np.asarray(scale) * r + np.asarray(center)
    return v, faces, uv


def transform(verts, mat):
    """Apply a 4x4 (mathutils or numpy) matrix to (N,3) verts."""
    M = np.array(mat, dtype=np.float64)
    v = np.asarray(verts, dtype=np.float64)
    return v @ M[:3, :3].T + M[:3, 3]


def rot_matrix(axis, angle):
    return np.array(Matrix.Rotation(angle, 4, axis))


def look_matrix(origin, x_axis, z_hint):
    """Frame with X along x_axis and Z as close as possible to z_hint."""
    x = _normalize(np.asarray(x_axis, dtype=np.float64))
    z = np.asarray(z_hint, dtype=np.float64)
    z = _normalize(z - np.dot(z, x) * x)
    y = np.cross(z, x)
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, y, z, origin
    return M


def bezier(p0, p1, p2, p3, n):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = (np.asarray(p, dtype=np.float64) for p in (p0, p1, p2, p3))
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def catmull(points, n_per=8, closed=False):
    """Centripetal-ish Catmull-Rom through control points."""
    P = np.asarray(points, dtype=np.float64)
    if closed:
        P = np.vstack([P[-1], P, P[0], P[1]])
    else:
        P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t = np.linspace(0, 1, n_per, endpoint=False)[:, None]
        t2, t3 = t * t, t * t * t
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(P[-2][None])
    return np.vstack(out)


def resample(path, n):
    path = np.asarray(path, dtype=np.float64)
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, path[:, i]) for i in range(3)], axis=1)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------
# Modifiers / misc
# ---------------------------------------------------------------------------

def add_subsurf(ob, levels=1, render_levels=2):
    m = ob.modifiers.new("Subsurf", 'SUBSURF')
    m.levels = levels
    m.render_levels = render_levels
    return m


def add_bevel(ob, width=0.002, segments=2, angle=30):
    m = ob.modifiers.new("Bevel", 'BEVEL')
    m.width = width
    m.segments = segments
    m.limit_method = 'ANGLE'
    m.angle_limit = math.radians(angle)
    return m


def set_smooth_by_angle(ob, angle=30):
    """Auto-smooth equivalent for Blender 4.1+: mark sharp edges by angle."""
    me = ob.data
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(me)
    lim = math.radians(angle)
    for e in bm.edges:
        if len(e.link_faces) == 2:
            a = e.link_faces[0].normal.angle(e.link_faces[1].normal, 0.0)
            e.smooth = a < lim
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(me)
    bm.free()


def link_object_to(ob, coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)


def hash01(*args):
    """Deterministic hash -> [0,1)."""
    h = 0
    for a in args:
        h = (h * 1000003) ^ int(a * 9973 + 0.5) if isinstance(a, float) else (h * 1000003) ^ int(a)
        h &= 0xFFFFFFFF
    h ^= h >> 15
    h = (h * 0x2C1B3C6D) & 0xFFFFFFFF
    h ^= h >> 12
    h = (h * 0x297A2D39) & 0xFFFFFFFF
    h ^= h >> 15
    return (h & 0xFFFFFF) / float(0x1000000)


def v(*a):
    return Vector(a)
