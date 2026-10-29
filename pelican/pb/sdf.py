"""Small numpy signed-distance-field toolkit + marching cubes to a mesh."""
import numpy as np


def rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rot_x(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def ellipsoid(P, center, radii, R=None):
    """Approximate ellipsoid SDF (iq). R rotates the ellipsoid (local->world)."""
    q = P - np.asarray(center, dtype=np.float32)
    if R is not None:
        q = q @ np.asarray(R, dtype=np.float32)          # world -> local
    r = np.asarray(radii, dtype=np.float32)
    k0 = np.linalg.norm(q / r, axis=-1)
    k1 = np.linalg.norm(q / (r * r), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def round_cone(P, a, b, ra, rb):
    """Capsule with linearly varying radius (iq sdRoundCone, exact-ish)."""
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    ba = b - a
    l2 = float(np.dot(ba, ba))
    rr = ra - rb
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pa = P - a
    y = pa @ ba
    z = y - l2
    xv = pa * l2 - y[..., None] * ba
    x2 = np.einsum('...i,...i->...', xv, xv)
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    out = np.empty_like(y)
    c1 = np.sign(z) * a2 * z2 > k
    c2 = np.sign(y) * a2 * y2 < k
    out[c1] = np.sqrt(x2[c1] + z2[c1]) * il2 - rb
    m2 = c2 & ~c1
    out[m2] = np.sqrt(x2[m2] + y2[m2]) * il2 - ra
    m3 = ~(c1 | c2)
    out[m3] = (np.sqrt(x2[m3] * a2 * il2) + y[m3] * rr) * il2 - ra
    return out


def tube(P, pts, radii):
    d = None
    for i in range(len(pts) - 1):
        di = round_cone(P, pts[i], pts[i + 1], radii[i], radii[i + 1])
        d = di if d is None else np.minimum(d, di)
    return d


def smin(a, b, k):
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def smax(a, b, k):
    return -smin(-a, -b, k)


def grid(lo, hi, step):
    xs = np.arange(lo[0], hi[0] + step, step, dtype=np.float32)
    ys = np.arange(lo[1], hi[1] + step, step, dtype=np.float32)
    zs = np.arange(lo[2], hi[2] + step, step, dtype=np.float32)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
    P = np.stack([X, Y, Z], axis=-1)
    return P, (xs, ys, zs)


def polygonize(field, axes, step):
    from skimage import measure
    verts, faces, normals, _ = measure.marching_cubes(field, level=0.0, spacing=(step, step, step))
    verts = verts + np.array([axes[0][0], axes[1][0], axes[2][0]])
    return verts, faces


def laplacian_smooth(verts, faces, iterations=3, lam=0.5, mu=-0.53):
    """Taubin smoothing (no shrinkage) on a triangle mesh."""
    import scipy.sparse as sp
    n = len(verts)
    i = np.concatenate([faces[:, 0], faces[:, 1], faces[:, 2], faces[:, 1], faces[:, 2], faces[:, 0]])
    j = np.concatenate([faces[:, 1], faces[:, 2], faces[:, 0], faces[:, 0], faces[:, 1], faces[:, 2]])
    A = sp.coo_matrix((np.ones(len(i)), (i, j)), shape=(n, n)).tocsr()
    A.data[:] = 1.0
    deg = np.asarray(A.sum(axis=1)).ravel()
    deg[deg == 0] = 1
    Dinv = sp.diags(1.0 / deg)
    W = Dinv @ A
    v = verts.copy()
    for _ in range(iterations):
        v = v + lam * (W @ v - v)
        v = v + mu * (W @ v - v)
    return v
