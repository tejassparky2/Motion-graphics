"""Bill, gular pouch, eyes and legs/feet of the pelican (rest pose, bike space)."""
import math

import numpy as np

from . import pose as P
from .util import (MeshBuilder, catmull, circle_profile, loft, smoothstep, sweep,
                   uv_sphere, look_matrix, transform, resample)


def _interp(t, ts, vs):
    return np.interp(t, ts, vs)


# ---------------------------------------------------------------------------
# Bill
# ---------------------------------------------------------------------------
W_T = [0.0, 0.08, 0.35, 0.70, 0.88, 0.95, 0.985, 1.0]
W_V = [0.0262, 0.0232, 0.0192, 0.0172, 0.0184, 0.0160, 0.0090, 0.0030]
H_T = [0.0, 0.06, 0.20, 0.50, 0.85, 0.93, 0.97, 1.0]
H_V = [0.0300, 0.0215, 0.0125, 0.0088, 0.0092, 0.0125, 0.0095, 0.0030]


def bill_frame(s, y, z):
    return P.BILL_BASE + s * P.BILL_DIR + y * np.array([0, 1.0, 0]) + z * P.BILL_UP


def hook_dz(t):
    return -0.024 * smoothstep(0.90, 1.0, t) ** 1.6


def upper_mandible(nu=90, nv=40):
    rings = []
    uvs = []
    ts = np.concatenate([np.linspace(-0.04, 0.9, nu - 20), np.linspace(0.9, 1.0, 21)[1:]])
    for t in ts:
        tt = max(t, 0.0)
        w = _interp(tt, W_T, W_V)
        h = _interp(tt, H_T, H_V)
        dz = hook_dz(tt)
        ring = []
        for j in range(nv):
            a = 2 * np.pi * j / nv
            c, s = math.cos(a), math.sin(a)
            y = w * c
            if s >= 0:      # upper surface (culmen arch + central ridge)
                z = h * (s ** 0.62) + 0.0024 * math.exp(-(c * w / 0.0032) ** 2) * min(1, tt * 8) * s
            else:           # palate, slightly convex
                z = -0.0042 * (-s) ** 0.9 - 0.0009
            # the hook curls down: lower side follows faster than upper
            zz = z + dz * (1.0 if s >= 0 else 1.08)
            ring.append(bill_frame(t * P.BILL_LEN, y, zz))
        rings.append(ring)
    v, f, uv = loft(np.array(rings), closed_rings=True, cap_start=True, cap_end=True)
    # uv: u = along bill, v = around
    return v, f, uv


def ramus_path(side, n=80):
    """Lower mandible bar from the jaw hinge to the bill tip (one side)."""
    pts = []
    hinge = P.JAW_HINGE + np.array([0, side * 0.031, 0])
    pre = bill_frame(-0.025, side * 0.028, -0.010)
    pts.append(hinge)
    pts.append(pre)
    for t in np.linspace(0.0, 0.985, n):
        w = _interp(t, W_T, W_V)
        conv = 1 - smoothstep(0.86, 0.985, t)
        y = side * (w - 0.0032) * conv
        z = -0.0060 + hook_dz(t) * 0.55 - 0.0008
        pts.append(bill_frame(t * P.BILL_LEN, y, z))
    pts = np.array(pts)
    return resample(catmull(pts[::3], 6), 120)


def lower_mandible():
    mb = MeshBuilder()
    for side in (1, -1):
        path = ramus_path(side)
        n = len(path)
        prof = np.array([[1.0, 0.6], [0.6, 1.0], [-0.6, 1.0], [-1.0, 0.6], [-1.0, -0.6], [-0.6, -1.0],
                         [0.6, -1.0], [1.0, -0.6]])
        sc = np.stack([np.full(n, 0.0040), np.full(n, 0.0030)], 1)
        sc[:, 0] *= np.linspace(1.3, 0.9, n)
        v, f, uv = sweep(path, 1.0, profile=prof, scale2=sc, up=P.BILL_UP)
        mb.add(v, f, uv, mat=0)
    return mb


def pouch_sections():
    """List of (top_left, top_right, keel) for each pouch cross-section."""
    secs = []
    left = ramus_path(1)
    right = ramus_path(-1)
    # parameterise along the ramus path from tip backwards
    n = len(left)
    keel_ctrl = np.array([
        bill_frame(0.93 * P.BILL_LEN, 0, -0.012),
        bill_frame(0.70 * P.BILL_LEN, 0, -0.030),
        bill_frame(0.42 * P.BILL_LEN, 0, -0.044),
        bill_frame(0.18 * P.BILL_LEN, 0, -0.050),
        bill_frame(-0.02 * P.BILL_LEN, 0, -0.050),
        P.THROAT + np.array([0.040, 0, -0.030]),
        P.THROAT + np.array([0.012, 0, -0.022]),
    ])
    keel = resample(catmull(keel_ctrl, 10), 64)
    idx = np.linspace(n - 4, 2, 52).astype(int)
    for k, i in enumerate(idx):
        secs.append((left[i], right[i], keel[min(k, 51)]))
    # behind the hinge: wrap onto the sides of the throat and tuck into the neck
    hl = left[0]
    hr = right[0]
    for k, t in enumerate(np.linspace(0.15, 1.0, 10)):
        tl = hl + (P.THROAT + np.array([0.004, 0.030, 0.006]) - hl) * t
        tr = hr + (P.THROAT + np.array([0.004, -0.030, 0.006]) - hr) * t
        kk = keel[min(52 + k, 63)]
        secs.append((tl, tr, kk))
    return secs


def pouch(nv=34):
    rings = []
    for tl, tr, k in pouch_sections():
        mid = (tl + tr) / 2
        half = (tl - tr) / 2
        down = k - mid
        ring = []
        for j in range(nv):
            a = np.pi * j / (nv - 1)
            s = math.sin(a)
            bulge = 1.0 + 0.45 * s ** 1.5
            ring.append(mid + half * math.cos(a) * bulge + down * (s ** 0.85))
        rings.append(ring)
    v, f, uv = loft(np.array(rings), closed_rings=False)
    return v, f, uv


# ---------------------------------------------------------------------------
# Eyes
# ---------------------------------------------------------------------------

def eye_parts(side):
    """Eyeball (uv pole = pupil), cornea cap, eyelid ring. Returns MeshBuilder parts."""
    c = P.EYE * np.array([1, side, 1])
    look = np.array([0.30, side * 1.0, 0.12])
    look /= np.linalg.norm(look)
    M = look_matrix(c, look, np.array([0, 0, 1.0]))
    # sphere with pole along local +X: build along z then rotate
    v, f, uv = uv_sphere(P.EYE_R, 40, 24)
    # uv_sphere pole is +Z: map z->x
    v = v[:, [2, 1, 0]] * np.array([1, 1, 1])
    v[:, 1] *= -1 if False else 1
    f = [list(reversed(x)) for x in f]
    eyeball = (transform(v, M), f, uv)
    # cornea: a slightly larger cap over the front
    cap = []
    nu, nv = 40, 10
    for i in range(nv + 1):
        th = 0.95 * i / nv
        for j in range(nu):
            ph = 2 * np.pi * j / nu
            r = P.EYE_R * 1.06
            cap.append([r * math.cos(th) + 0.0006 * math.cos(th) ** 8, r * math.sin(th) * math.cos(ph),
                        r * math.sin(th) * math.sin(ph)])
    cap = np.array(cap)
    faces = []
    for i in range(nv):
        for j in range(nu):
            a = i * nu + j
            b = i * nu + (j + 1) % nu
            faces.append([a, b, b + nu, a + nu])
    cornea = (transform(cap, M), faces, np.zeros((len(cap), 2)))
    # eyelid ring (bare orbital skin)
    tor = []
    ring_n, tube_n = 40, 10
    for i in range(ring_n):
        a = 2 * np.pi * i / ring_n
        for j in range(tube_n):
            b = 2 * np.pi * j / tube_n
            R0 = P.EYE_R * 0.98
            rr = 0.0026
            x = 0.0024 + rr * math.cos(b) * 0.7
            yy = (R0 + rr * math.sin(b)) * math.cos(a)
            zz = (R0 + rr * math.sin(b)) * math.sin(a)
            tor.append([x * (1 + 0.15 * math.sin(a)), yy * 1.08, zz])
    faces = []
    for i in range(ring_n):
        for j in range(tube_n):
            a = i * tube_n + j
            b = ((i + 1) % ring_n) * tube_n + j
            c2 = ((i + 1) % ring_n) * tube_n + (j + 1) % tube_n
            d = i * tube_n + (j + 1) % tube_n
            faces.append([a, b, c2, d])
    lid = (transform(np.array(tor), M), faces, np.zeros((len(tor), 2)))
    return eyeball, cornea, lid, M


# ---------------------------------------------------------------------------
# Legs and feet
# ---------------------------------------------------------------------------

def two_bone_ik(root, target, l1, l2, pole):
    d = target - root
    dist = np.linalg.norm(d)
    dist = min(dist, (l1 + l2) * 0.999)
    u = d / np.linalg.norm(d)
    p = pole - np.dot(pole, u) * u
    p /= np.linalg.norm(p)
    cos_a = (l1 * l1 + dist * dist - l2 * l2) / (2 * l1 * dist)
    a = math.acos(max(-1, min(1, cos_a)))
    mid = root + l1 * (math.cos(a) * u + math.sin(a) * p)
    end = root + u * dist
    return mid, end


TOES = [  # (angle from forward toward medial (deg), length, base offset)
    ('hallux', 42.0, 0.058, (-0.006, -0.011)),
    ('t2', 16.0, 0.082, (0.000, -0.006)),
    ('t3', -3.0, 0.104, (0.002, 0.000)),
    ('t4', -22.0, 0.096, (0.000, 0.007)),
]


def foot_geometry(side):
    """Webbed totipalmate foot in foot-local space: origin at the toe joint,
    +X forward, +Z up, medial = -Y for the left foot (side=+1)."""
    mb = MeshBuilder()
    MSKIN, MCLAW, MWEB = 0, 1, 2
    toe_lines = []
    for name, ang, length, off in TOES:
        a = math.radians(ang) * (-side)          # medial is toward the bike centre
        d = np.array([math.cos(a), math.sin(a), 0.0])
        base = np.array([off[0], off[1] * side, 0.0])
        pts = []
        n = 24
        for i in range(n):
            t = i / (n - 1)
            p = base + d * length * t
            x = p[0]
            # lie on the pedal, then curl down over its front edge
            z = 0.0
            over = max(0.0, x - 0.046)
            z -= 3.0 * over ** 2 + 0.12 * over
            pts.append([p[0] - 0.4 * over ** 2 * 10 * 0, p[1], z])
        pts = np.array(pts)
        toe_lines.append(pts)
        rad = 0.0088 * (1 - 0.55 * np.linspace(0, 1, n)) * (1 + 0.12 * np.sin(np.linspace(0, 1, n) * np.pi * 4) ** 2)
        if name == 'hallux':
            rad *= 0.8
        v, f, uv = sweep(pts, rad, 12, up=np.array([0, 0, 1.0]),
                         scale2=np.stack([np.ones(n), np.full(n, 1.0)], 1))
        mb.add(v, f, uv, mat=MSKIN)
        # claw
        tip = pts[-1]
        tdir = (pts[-1] - pts[-3])
        tdir /= np.linalg.norm(tdir)
        claw = np.array([tip - tdir * 0.002, tip + tdir * 0.006 + np.array([0, 0, -0.002]),
                         tip + tdir * 0.010 + np.array([0, 0, -0.006])])
        v, f, uv = sweep(claw, np.array([0.0030, 0.0020, 0.0004]), 8)
        mb.add(v, f, uv, mat=MCLAW)
    # webs between adjacent toes (scalloped edge)
    for a, b in ((0, 1), (1, 2), (2, 3)):
        A, B = toe_lines[a], toe_lines[b]
        rings = []
        nt = 18
        nw = 9
        for i in range(nt):
            t = i / (nt - 1)
            ring = []
            for j in range(nw):
                w = j / (nw - 1)
                reach = t * (1 - 0.30 * math.sin(math.pi * w)) * 0.97
                ia = reach * (len(A) - 1)
                pa = A[int(ia)] + (A[min(int(ia) + 1, len(A) - 1)] - A[int(ia)]) * (ia - int(ia))
                pb = B[int(ia)] + (B[min(int(ia) + 1, len(B) - 1)] - B[int(ia)]) * (ia - int(ia))
                p = pa * (1 - w) + pb * w
                p[2] -= 0.0025 * math.sin(math.pi * w) * t - 0.001
                ring.append(p)
            rings.append(ring)
        v, f, uv = loft(np.array(rings), closed_rings=False)
        mb.add(v, f, uv, mat=MWEB)
    # heel pad / toe-joint knuckle
    v, f, uv = uv_sphere(1.0, 20, 10, center=(0.0, 0, 0.002), scale=(0.016, 0.014, 0.010))
    mb.add(v, f, uv, mat=MSKIN)
    return mb


def leg_path(knee, ankle, toe_joint, n=60):
    """Smooth path knee->ankle->toe joint with a tight bend at the ankle."""
    a1 = knee + (ankle - knee) * 0.92
    a2 = ankle + (toe_joint - ankle) * 0.08
    p1 = np.linspace(knee, a1, 26)
    bend = np.array([a1, ankle + (a1 - ankle) * 0.2 + (a2 - ankle) * 0.0, a2])
    p2 = catmull(np.vstack([a1, ankle, a2]), 6)[1:-1]
    p3 = np.linspace(a2, toe_joint, 26)
    return np.vstack([p1, p2, p3])
