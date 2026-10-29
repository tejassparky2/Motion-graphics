"""Procedural plumage: contour feathers, folded wings, tail, crest and leg 'trousers'.

Every feather is a small curved vane mesh.  Body and wing feathers are draped
onto offset surfaces of the body's signed distance field so that they shingle
without ever penetrating the skin.
"""
import math

import numpy as np

from . import pose as P
from .pelican_body import body_field
from .util import grid_faces, smoothstep

RNG = np.random.default_rng(1234)

WHITE = np.array([0.93, 0.915, 0.89])
BLUSH = np.array([0.97, 0.85, 0.80])
BREAST = np.array([0.98, 0.86, 0.58])
CREAM = np.array([0.96, 0.92, 0.80])
BLACK = np.array([0.025, 0.022, 0.022])
GREY = np.array([0.30, 0.29, 0.30])


# ---------------------------------------------------------------------------
# SDF helpers
# ---------------------------------------------------------------------------

def sdf_grad(pts, h=0.0006):
    pts = np.asarray(pts, dtype=np.float32)
    d = body_field(pts)
    g = np.zeros_like(pts)
    for i in range(3):
        e = np.zeros(3, dtype=np.float32)
        e[i] = h
        g[:, i] = (body_field(pts + e) - body_field(pts - e)) / (2 * h)
    g /= np.maximum(np.linalg.norm(g, axis=1, keepdims=True), 1e-9)
    return d, g


def drape(verts, offset, iters=3):
    v = np.asarray(verts, dtype=np.float32).copy()
    off = np.broadcast_to(np.asarray(offset, dtype=np.float32), (len(v),))
    for _ in range(iters):
        d, g = sdf_grad(v)
        push = np.maximum(off - d, 0.0)
        if push.max() < 1e-5:
            break
        v += g * push[:, None]
    return v


# ---------------------------------------------------------------------------
# Feather vane
# ---------------------------------------------------------------------------

def vane(L, W, nu=7, nv=5, bend=0.10, cup=0.12, asym=0.0, pow_=0.75, notch=0.0, round_tip=True):
    """Feather in local space: +X root->tip, +Y across, +Z out of the body."""
    u = np.linspace(0, 1, nu)
    v = np.linspace(0, 1, nv)
    U, V = np.meshgrid(u, v, indexing='ij')
    if round_tip:
        grow = np.clip(U / 0.30, 0, 1) ** 0.6
        tip = np.sqrt(np.clip(1 - (np.clip(U - 0.5, 0, None) / 0.5) ** 2, 0, 1))
        prof = np.maximum(grow * tip, 0.14 * (1 - U))
        prof[-1] = np.maximum(prof[-1], 0.0)
    else:
        prof = np.sin(np.pi * np.clip(U * 0.92 + 0.08, 0, 1) ** pow_) ** 0.7
        prof = np.maximum(prof, 0.18 * (1 - U))
    across = 2 * V - 1
    side = np.where(across < 0, 1 - asym, 1 + asym)
    y = across * (W / 2) * prof * side
    x = U * L - notch * L * (1 - np.abs(across)) * U ** 6
    z = -bend * L * U ** 2 - cup * W * across ** 2 * prof
    verts = np.stack([x, y, z], -1).reshape(-1, 3)
    faces = grid_faces(nu, nv)
    uv = np.stack([U, V], -1).reshape(-1, 2)
    return verts, faces, uv


def frame_from(root, normal, flow, lift):
    n = normal / np.linalg.norm(normal)
    t = flow - np.dot(flow, n) * n
    t /= max(np.linalg.norm(t), 1e-9)
    X = math.cos(lift) * t + math.sin(lift) * n
    Z = n - np.dot(n, X) * X
    Z /= np.linalg.norm(Z)
    Y = np.cross(Z, X)
    return np.stack([X, Y, Z], 1)        # columns


class Plumage:
    def __init__(self):
        self.V, self.F, self.UV = [], [], []
        self.col, self.dark, self.flex, self.region, self.side = [], [], [], [], []
        self.nv = 0
        self.count = 0

    def add(self, verts, faces, uv, color, dark=0.0, region=0, side=0.0):
        n = len(verts)
        self.V.append(verts)
        self.F.append(faces + self.nv)
        self.UV.append(uv)
        self.col.append(np.tile(color, (n, 1)))
        self.dark.append(np.full(n, dark))
        self.flex.append(uv[:, 0].copy())
        self.region.append(np.full(n, region, dtype=np.int32))
        self.side.append(np.full(n, side))
        self.nv += n
        self.count += 1

    def arrays(self):
        return dict(V=np.vstack(self.V), F=np.vstack(self.F), UV=np.vstack(self.UV),
                    col=np.vstack(self.col), dark=np.concatenate(self.dark),
                    flex=np.concatenate(self.flex), region=np.concatenate(self.region),
                    side=np.concatenate(self.side))


# ---------------------------------------------------------------------------
# Body contour feathers
# ---------------------------------------------------------------------------

def spine_polyline():
    pts = [P.BILL_BASE, np.array(P.HEAD['c'])] + [p for p in P.NECK_PTS[::-1]] + \
          [np.array([0.44, 0, 0.765]), np.array([0.30, 0, 0.700]), np.array([0.12, 0, 0.630]),
           np.array([-0.06, 0, 0.585])]
    return np.array(pts, dtype=float)


def nearest_on_polyline(p, poly):
    """Returns (closest points, segment index, segment t) for many points p."""
    best_d = np.full(len(p), np.inf)
    best_q = np.zeros_like(p)
    best_i = np.zeros(len(p), dtype=int)
    best_t = np.zeros(len(p))
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        ab = b - a
        t = np.clip(((p - a) @ ab) / np.dot(ab, ab), 0, 1)
        q = a + t[:, None] * ab
        d = np.linalg.norm(p - q, axis=1)
        m = d < best_d
        best_d[m], best_q[m], best_i[m], best_t[m] = d[m], q[m], i, t[m]
    return best_q, best_i, best_t, best_d


def region_weights(p):
    head_c = np.array(P.HEAD['c'])
    dh = np.linalg.norm(p - head_c, axis=1)
    head = 1 - smoothstep(0.065, 0.085, dh)
    q, i, t, d = nearest_on_polyline(p, P.NECK_PTS)
    tau = (i + t) / (len(P.NECK_PTS) - 1)            # 0 at neck base, 1 at head
    neck = (1 - smoothstep(0.80, 0.86, p[:, 2])) * 0 + smoothstep(0.80, 0.87, p[:, 2]) * (1 - head)
    neck = np.clip(neck, 0, 1)
    return head, neck, tau


def body_feather_params(p, normal):
    head, neck, tau = region_weights(p)
    body = np.clip(1 - head - neck, 0, 1)
    # within body: back/scapulars vs belly vs breast vs tail
    up = normal[:, 2]
    back = smoothstep(0.2, 0.7, up) * body
    breast = (1 - smoothstep(0.05, 0.16, np.linalg.norm(p - np.array([0.60, 0, 0.80]), axis=1))) * body
    tail = (1 - smoothstep(0.08, 0.18, p[:, 0])) * body
    size = (head * (0.012 + 0.008 * np.clip(np.linalg.norm(p - np.array(P.HEAD['c']), axis=1) / 0.07, 0, 1))
            + neck * (0.028 - 0.010 * tau)
            + body * (0.050 + 0.026 * back + 0.016 * tail - 0.002 * breast))
    aspect = head * 0.70 + neck * 0.62 + body * (0.62 - 0.26 * breast)
    lift = np.radians(head * 1.5 + neck * 2.0 + body * (3.5 + 6 * breast))
    color = (WHITE[None] * (1 - breast[:, None]) + BREAST[None] * breast[:, None])
    color = color * (1 - 0.35 * back[:, None]) + BLUSH[None] * 0.35 * back[:, None]
    return size, aspect, lift, color, head, neck, body


def sample_surface(V, F, n):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    idx = RNG.choice(len(F), size=n, p=area / area.sum())
    r1 = np.sqrt(RNG.random(n))
    r2 = RNG.random(n)
    pts = (1 - r1)[:, None] * a[idx] + (r1 * (1 - r2))[:, None] * b[idx] + (r1 * r2)[:, None] * c[idx]
    return pts


def poisson_select(pts, radius):
    cell = radius.min()
    order = RNG.permutation(len(pts))
    grid = {}
    acc = []
    rmax = radius.max()
    reach = int(math.ceil(rmax / cell))
    for k in order:
        p = pts[k]
        r = radius[k]
        key = tuple((p // cell).astype(int))
        ok = True
        for dx in range(-reach, reach + 1):
            for dy in range(-reach, reach + 1):
                for dz in range(-reach, reach + 1):
                    lst = grid.get((key[0] + dx, key[1] + dy, key[2] + dz))
                    if not lst:
                        continue
                    for j in lst:
                        if np.sum((pts[j] - p) ** 2) < (0.5 * (r + radius[j])) ** 2:
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            acc.append(k)
            grid.setdefault(key, []).append(k)
    return np.array(acc)


def excluded(p, skin_fn):
    """Points where no contour feathers grow (bare face, under saddle, bill region)."""
    ex = skin_fn(p) > 0.3
    ex |= (p[:, 2] < 0.57) & (np.abs(p[:, 1]) < 0.07) & (p[:, 0] > 0.17) & (p[:, 0] < 0.42)
    # throat/gular area covered by the pouch
    q = P.THROAT
    ex |= (np.linalg.norm(p - (q + np.array([0.035, 0, 0.02])), axis=1) < 0.04) & (p[:, 0] > q[0] - 0.01)
    return ex


def body_feathers(plum, V, F, skin_fn, spacing=0.34):
    cand = sample_surface(V, F, 90000)
    d, nrm = sdf_grad(cand)
    cand = cand - nrm * d[:, None]
    keep = ~excluded(cand, skin_fn)
    cand, nrm = cand[keep], nrm[keep]
    size, aspect, lift, color, head, neck, body = body_feather_params(cand, nrm)
    # tiny feathers along the edge of the bare facial skin so the border stays soft
    sk = skin_fn(cand)
    size = size * np.clip(1.0 - 2.4 * sk, 0.35, 1.0)
    sel = poisson_select(cand, size * spacing)
    cand, nrm = cand[sel], nrm[sel]
    size, aspect, lift, color = size[sel], aspect[sel], lift[sel], color[sel]
    head, neck = head[sel], neck[sel]
    spine = spine_polyline()
    _, si, st, _ = nearest_on_polyline(cand, spine)
    flow = spine[si + 1] - spine[si]
    flow /= np.linalg.norm(flow, axis=1, keepdims=True)
    # feathers on the flanks sweep slightly downward
    side_down = np.clip(np.abs(nrm[:, 1]), 0, 1) * (1 - head)
    flow = flow + np.array([0, 0, -0.35])[None] * side_down[:, None]
    all_v, offs = [], []
    for k in range(len(cand)):
        L = size[k] * RNG.uniform(0.85, 1.15)
        W = L * aspect[k] * RNG.uniform(0.9, 1.1)
        ang = RNG.normal(0, 0.12)
        fl = flow[k]
        n = nrm[k]
        # rotate flow around the normal by a little noise
        fl = fl * math.cos(ang) + np.cross(n, fl) * math.sin(ang)
        nu, nv = (5, 4) if L < 0.03 else (7, 5)
        v, f, uv = vane(L, W, nu, nv, bend=0.30, cup=0.14)
        Mx = frame_from(cand[k], n, fl, lift[k])
        vw = v @ Mx.T + cand[k] - n * 0.0015
        all_v.append((vw, f, uv, color[k] * RNG.uniform(0.97, 1.02), uv[:, 0] * L * math.sin(lift[k]) + 0.0012))
    # drape all at once (vectorised)
    stack = np.vstack([a[0] for a in all_v])
    off = np.concatenate([a[4] for a in all_v])
    stack = drape(stack, np.maximum(off, 0.0008))
    pos = 0
    for vw, f, uv, c, _ in all_v:
        n = len(vw)
        reg = 1
        plum.add(stack[pos:pos + n], f, uv, np.clip(c, 0, 1), region=0)
        pos += n
    return len(cand)


# ---------------------------------------------------------------------------
# Folded wings
# ---------------------------------------------------------------------------

def wing_feathers(plum, side, wrist, elbow, hand_tip):
    """Folded, slightly abducted wing; the wrist rests on the handlebar grip.

    The wing is a feathered panel spanned by the forearm (elbow -> wrist, its
    leading edge) and the down-and-back direction the flight feathers hang in.
    Rows from the leading edge: lesser, median and greater coverts over the
    black secondaries; the black primaries hang from the folded hand beneath.
    """
    s = side
    W, E, T = np.asarray(wrist), np.asarray(elbow), np.asarray(hand_tip)
    f = (W - E) / np.linalg.norm(W - E)
    d0 = np.array([-0.55, 0.0, -0.83])
    n_w = np.cross(f, d0)
    n_w /= np.linalg.norm(n_w)
    if n_w[1] * s < 0:
        n_w = -n_w
    down = np.cross(n_w, f)
    down /= np.linalg.norm(down)
    if down[2] > 0:
        down = -down
    back = -f

    def fdir(beta):
        return math.cos(beta) * down + math.sin(beta) * back

    rows = []   # (root, dir, L, W, colour, dark, layer, tag, lift, nu, nv)
    # primaries: from the folded hand, swept back toward the tail (bottom layer)
    hand = [W + (T - W) * t for t in np.linspace(0.0, 1.0, 10)]
    for k, r in enumerate(hand):
        L = 0.30 + 0.07 * k / 9
        d = np.array([-1.0, 0.0, -0.10]) + down * 0.10
        rows.append((r + down * 0.025, d, L, 0.060, BLACK, 1.0, 0.000 + 0.0007 * k, 7, 0.02, 16, 7))
    # secondaries along the forearm
    n_sec = 17
    for k in range(n_sec):
        t = k / (n_sec - 1)
        r = E + (W - E) * (0.03 + 0.95 * t)
        beta = math.radians(58 - 18 * t)
        L = (0.245 - 0.045 * t) * RNG.uniform(0.96, 1.04)
        rows.append((r + down * 0.006, fdir(beta), L, 0.070, BLACK * 1.6 + 0.015, 1.0,
                     0.004 + 0.0004 * (n_sec - k), 8, 0.02, 14, 7))
    # tertials at the elbow, lying back over the rump
    for k in range(5):
        r = E + back * (0.02 - 0.015 * k) + down * 0.01 * k
        rows.append((r, fdir(math.radians(72)), 0.20 - 0.012 * k, 0.07, WHITE * 0.95, 0.0,
                     0.012, 9, 0.02, 12, 6))
    # covert rows: (offset down from the leading edge, length, width, colour, layer)
    covert_rows = [(0.030, 0.100, 0.058, WHITE * 0.97, 0.016),
                   (0.018, 0.074, 0.048, BLUSH, 0.020),
                   (0.008, 0.052, 0.040, WHITE, 0.024),
                   (0.000, 0.040, 0.034, WHITE, 0.028),
                   (-0.010, 0.036, 0.030, WHITE, 0.032)]
    for ri, (doff, L, Wd, col, layer) in enumerate(covert_rows):
        n_c = 18 + ri * 2
        for k in range(n_c):
            t = (k + 0.5 * (ri % 2)) / n_c
            r = E + (W - E) * (0.02 + 0.97 * t) + down * (doff + RNG.normal(0, 0.003))
            beta = math.radians(55 - 16 * t + RNG.normal(0, 4))
            rows.append((r, fdir(beta), L * RNG.uniform(0.90, 1.08), Wd, col, 0.0, layer,
                         10 + ri, 0.05, 8, 5))
    # primary coverts over the base of the primaries
    for k, r in enumerate(hand[:-1]):
        rows.append((r + down * 0.02, np.array([-1.0, 0, -0.2]) + down * 0.2, 0.095, 0.048,
                     WHITE * 0.93, 0.0, 0.010, 14, 0.02, 8, 5))
    # alula at the wrist
    for k in range(3):
        rows.append((W + n_w * 0.004 + np.array([0, 0, 0.004 * k]), fdir(math.radians(80)),
                     0.065 - 0.012 * k, 0.020, WHITE, 0.0, 0.03, 15, 0.05, 8, 3))

    verts_all = []
    for (r, d, L, Wd, col, dark, layer, tag, lift, nu, nv) in rows:
        dd = d / np.linalg.norm(d)
        flight = tag in (7, 8)
        v, f_, uv = vane(L, Wd, nu, nv, bend=0.05, cup=0.09, asym=0.35 if flight else 0.0,
                         pow_=0.55, round_tip=not flight)
        Mx = frame_from(r + n_w * layer, n_w, dd, lift)
        vw = v @ Mx.T + r + n_w * layer
        verts_all.append((vw, f_, uv, col, dark, 0.006 + layer + uv[:, 0] * 0.002, tag))
    stack = np.vstack([a[0] for a in verts_all])
    off = np.concatenate([a[5] for a in verts_all])
    stack = drape(stack, off)
    pos = 0
    for vw, f_, uv, col, dark, _, tag in verts_all:
        n = len(vw)
        c = np.clip(col * RNG.uniform(0.96, 1.03), 0, 1)
        plum.add(stack[pos:pos + n], f_, uv, c, dark=dark, region=2, side=s)
        pos += n


# ---------------------------------------------------------------------------
# Tail, crest, trousers
# ---------------------------------------------------------------------------

def tail_feathers(plum):
    base = np.array([0.010, 0.0, 0.618])
    n = 12
    for k in range(n):
        a = (k / (n - 1) - 0.5) * 0.55
        d = np.array([-math.cos(a), math.sin(a) * 0.9, -0.25])
        L = 0.105 - 0.02 * abs(a)
        r = base + np.array([0.015 * abs(a), 0.030 * math.sin(a), 0.003 * (k % 2)])
        v, f, uv = vane(L, 0.050, 9, 5, bend=0.14, cup=0.08)
        _, g = sdf_grad(r[None])
        Mx = frame_from(r, np.array([0, 0, 1.0]) * 0.6 + g[0] * 0.4, d, 0.02)
        vw = v @ Mx.T + r
        vw = drape(vw, 0.004 + uv[:, 0] * 0.003)
        plum.add(vw, f, uv, WHITE * 0.95, region=0)
    for k in range(12):
        a = (k / 11 - 0.5) * 0.8
        r = np.array([0.075, 0.034 * math.sin(a), 0.645])
        d = np.array([-math.cos(a), math.sin(a) * 0.8, -0.22])
        v, f, uv = vane(0.090, 0.040, 7, 5, bend=0.18, cup=0.10)
        _, g = sdf_grad(r[None])
        Mx = frame_from(r, g[0], d, 0.03)
        vw = drape(v @ Mx.T + r, 0.008 + uv[:, 0] * 0.003)
        plum.add(vw, f, uv, BLUSH, region=0)


def crest_feathers(plum):
    nape = np.array(P.NAPE['c'])
    for k in range(34):
        a = RNG.uniform(-1.1, 1.1)
        h = RNG.uniform(-0.2, 1.0)
        r = nape + np.array([-0.020 - 0.012 * h, 0.030 * math.sin(a), 0.026 + 0.012 * h * math.cos(a)])
        d, g = sdf_grad(r[None])
        r = r - g[0] * d[0]
        L = RNG.uniform(0.045, 0.075)
        v, f, uv = vane(L, 0.013, 9, 3, bend=0.10, cup=0.05)
        flow = np.array([-1.0, 0.25 * math.sin(a), -0.75])
        Mx = frame_from(r, g[0], flow, math.radians(RNG.uniform(10, 22)))
        vw = v @ Mx.T + r
        plum.add(vw, f, uv, CREAM * RNG.uniform(0.98, 1.02), region=3)


def trouser_feathers(plum, leg_paths, shin_frac=0.42):
    """Feathers down the upper tibiotarsus (attached to the leg, region 4/5)."""
    for side, path in leg_paths:
        seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
        u = seg / seg[-1]
        n_rings = 9
        for i in range(n_rings):
            t = 0.02 + shin_frac * i / (n_rings - 1) * 0.9
            k = np.searchsorted(u, t)
            c = path[k]
            tang = path[min(k + 1, len(path) - 1)] - path[max(k - 1, 0)]
            tang /= np.linalg.norm(tang)
            ref = np.array([0, 1.0, 0])
            b1 = np.cross(tang, ref)
            b1 /= np.linalg.norm(b1)
            b2 = np.cross(tang, b1)
            nf = 11
            rad = 0.031 - 0.010 * t / shin_frac
            for j in range(nf):
                ang = 2 * np.pi * (j + 0.5 * (i % 2)) / nf
                nrm = b1 * math.cos(ang) + b2 * math.sin(ang)
                r = c + nrm * rad * 0.9
                L = 0.050 + 0.012 * (1 - t / shin_frac)
                v, f, uv = vane(L, L * 0.7, 6, 4, bend=0.35, cup=0.16)
                Mx = frame_from(r, nrm, tang + nrm * 0.05, math.radians(9))
                vw = v @ Mx.T + r
                plum.add(vw, f, uv, WHITE * RNG.uniform(0.95, 1.0), region=4 if side > 0 else 5, side=side)
