"""A small-wheeled vintage lugged-steel roadster, built procedurally.

Bike space: +X forward, +Y left, +Z up, origin on the ground under the rear
axle.  The drive side is the right side (-Y).
"""
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector

from . import bike_materials as bm
from .util import (MeshBuilder, box, catmull, circle_profile, collection, empty,
                   grid_faces, lathe, loft, make_mesh, resample, rot_matrix,
                   smoothstep, sweep, transform, uv_sphere, bezier)

# ---------------------------------------------------------------------------
# Geometry constants
# ---------------------------------------------------------------------------
R = 0.243                 # tyre outer radius
RIM_BED = 0.1965          # spoke bed radius
WHEELBASE = 0.84
A_R = np.array([0.0, 0.0, R])
A_F = np.array([WHEELBASE, 0.0, R])
BB = np.array([0.355, 0.0, 0.21])
CRANK = 0.10
CHAINLINE = -0.040
HEAD_ANGLE = math.radians(70)
SEAT_ANGLE = math.radians(71)
RAKE = 0.040
STEER_DIR = np.array([-math.cos(HEAD_ANGLE), 0, math.sin(HEAD_ANGLE)])
STEER_FWD = np.array([math.sin(HEAD_ANGLE), 0, math.cos(HEAD_ANGLE)])
STEER_FOOT = A_F - RAKE * STEER_FWD
SEAT_DIR = np.array([-math.cos(SEAT_ANGLE), 0, math.sin(SEAT_ANGLE)])
RING_T, COG_T = 44, 22
PITCH = 0.0127
RING_R = PITCH / (2 * math.sin(math.pi / RING_T))
COG_R = PITCH / (2 * math.sin(math.pi / COG_T))
GEAR = RING_T / COG_T


def steer_point(z):
    t = (z - STEER_FOOT[2]) / STEER_DIR[2]
    return STEER_FOOT + t * STEER_DIR


HT_BOT = steer_point(0.524)
HT_TOP = steer_point(0.628)
CROWN = steer_point(0.509)
ST_TOP = BB + 0.265 * SEAT_DIR
SADDLE_CLAMP = BB + 0.305 * SEAT_DIR
STEM_TOP = steer_point(0.715)


def seat_point(z):
    s = (z - BB[2]) / SEAT_DIR[2]
    return BB + s * SEAT_DIR


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def lathe_y(profile_ry, segments=64, closed=False):
    v, f, uv = lathe(profile_ry, segments, closed_top=closed)
    out = np.stack([v[:, 0], v[:, 2], v[:, 1]], axis=1)
    f = np.asarray(f)[:, ::-1] if isinstance(f, np.ndarray) else [list(reversed(x)) for x in f]
    return out, f, uv


def tube(a, b, r, sides=16, caps=True, r2=None, n=2):
    path = np.linspace(np.asarray(a, float), np.asarray(b, float), n)
    rad = np.linspace(r, r if r2 is None else r2, n)
    return sweep(path, rad, sides, caps=caps)


def extrude_outline(outline_xz, y0, y1, flip=False):
    """Extrude a closed 2D outline (in the XZ plane) between y0 and y1."""
    o = np.asarray(outline_xz, float)
    k = len(o)
    front = np.stack([o[:, 0], np.full(k, y0), o[:, 1]], 1)
    back = np.stack([o[:, 0], np.full(k, y1), o[:, 1]], 1)
    verts = np.vstack([front, back])
    faces = [[i, (i + 1) % k, k + (i + 1) % k, k + i] for i in range(k)]
    faces.append(list(range(k))[::-1])
    faces.append([k + i for i in range(k)])
    if flip:
        faces = [f[::-1] for f in faces]
    uv = np.zeros((2 * k, 2))
    uv[:, 0] = np.tile(np.arange(k) / k, 2)
    return verts, faces, uv


def ring_band(outer_xz, inner_r, y0, y1):
    """Annular plate: outer outline (k points, polar ordered) to inner circle."""
    o = np.asarray(outer_xz, float)
    k = len(o)
    ang = np.arctan2(o[:, 1], o[:, 0])
    inner = np.stack([np.cos(ang) * inner_r, np.sin(ang) * inner_r], 1)
    rings = []
    for y in (y0, y1):
        rings.append(np.stack([o[:, 0], np.full(k, y), o[:, 1]], 1))
        rings.append(np.stack([inner[:, 0], np.full(k, y), inner[:, 1]], 1))
    V = np.vstack(rings)  # 0: outer y0, 1: inner y0, 2: outer y1, 3: inner y1
    F = []
    for i in range(k):
        j = (i + 1) % k
        F.append([0 * k + i, 1 * k + i, 1 * k + j, 0 * k + j])       # face y0
        F.append([2 * k + i, 2 * k + j, 3 * k + j, 3 * k + i])       # face y1
        F.append([0 * k + i, 0 * k + j, 2 * k + j, 2 * k + i])       # outer wall
        F.append([1 * k + i, 3 * k + i, 3 * k + j, 1 * k + j])       # inner wall
    return V, F, np.zeros((len(V), 2))


def sprocket_outline(teeth, samples=20, roller=0.0079, phase=0.0):
    rp = PITCH / (2 * math.sin(math.pi / teeth))
    rs = roller / 2 + 0.00015
    tip = rp + 0.0032
    n = teeth * samples
    phi = np.linspace(0, 2 * np.pi, n, endpoint=False) + phase
    step = 2 * np.pi / teeth
    delta = (phi - phase + step / 2) % step - step / 2       # angle to nearest seat
    d = np.abs(delta) * rp
    r = np.where(d < rs, rp - np.sqrt(np.maximum(rs ** 2 - d ** 2, 0)),
                 rp + (d - rs) * 2.6)
    # soft-min against the tip circle for rounded tooth tops
    k = 0.0006
    r = -k * np.log(np.exp(-r / k) + np.exp(-tip / k))
    return np.stack([np.cos(phi) * r, np.sin(phi) * r], 1), rp


# ---------------------------------------------------------------------------
# Wheels
# ---------------------------------------------------------------------------

def rim_profile():
    half = [(0.1960, 0.0000), (0.1964, 0.0055), (0.1980, 0.0092), (0.2035, 0.0104),
            (0.2112, 0.0103), (0.2124, 0.0093), (0.2120, 0.0081), (0.2090, 0.0076),
            (0.2078, 0.0040), (0.2072, 0.0000)]
    prof = half + [(r, -y) for r, y in reversed(half[1:-1])]
    # order must loop around: start at inner centre, go to +y side, outer, back to -y
    return np.array(prof)


def tire_profile(n=36):
    rc, rt = 0.2262, 0.0172
    a = np.linspace(-2.25, 2.25, n)
    pts = [(rc + rt * math.cos(t), rt * math.sin(t)) for t in a]
    pts = [(0.2085, -0.0090)] + pts + [(0.2085, 0.0090)]
    return np.array(pts)


def hub_profile(flange_l=0.030, flange_r=0.030, width=0.050, barrel=0.0115):
    fr = 0.0235
    p = [(0.0045, -width), (0.0090, -width), (0.0090, -width + 0.004), (0.0070, -width + 0.005),
         (0.0075, -flange_r - 0.006), (0.0105, -flange_r - 0.003),
         (fr, -flange_r - 0.0014), (fr + 0.0006, -flange_r), (fr, -flange_r + 0.0014),
         (barrel, -flange_r + 0.004), (barrel * 0.92, 0.0), (barrel, flange_l - 0.004),
         (fr, flange_l - 0.0014), (fr + 0.0006, flange_l), (fr, flange_l + 0.0014),
         (0.0105, flange_l + 0.003), (0.0075, flange_l + 0.006), (0.0070, width - 0.005),
         (0.0090, width - 0.004), (0.0090, width), (0.0045, width)]
    return np.array(p)


def build_wheel(name, coll, mats, rear=False, nspokes=32, cross=3):
    """Returns a wheel mesh object centred on its own origin (axis = Y)."""
    mb = MeshBuilder()
    MCH, MALU, MTIRE, MSPOKE = 0, 1, 2, 3
    v, f, uv = lathe_y(rim_profile(), 192, closed=True)
    mb.add(v, f, uv, mat=MALU)
    v, f, uv = lathe_y(tire_profile(), 240, closed=False)
    mb.add(v, f, uv, mat=MTIRE)
    fl_l, fl_r = (0.033, 0.024) if rear else (0.030, 0.030)
    v, f, uv = lathe_y(hub_profile(fl_l, fl_r, 0.055 if rear else 0.050), 40, closed=False)
    mb.add(v, f, uv, mat=MCH)
    # axle nuts
    for s in (-1, 1):
        y0 = s * (0.055 if rear else 0.050)
        nut = np.array([[math.cos(a) * 0.0085, math.sin(a) * 0.0085] for a in np.arange(6) * np.pi / 3])
        vv, ff, uu = extrude_outline(nut, y0, y0 + s * 0.007, flip=s < 0)
        mb.add(vv, ff, uu, mat=MCH)
        vv, ff, uu = tube((0, y0, 0), (0, y0 + s * 0.016, 0), 0.0042, 10)
        mb.add(vv, ff, uu, mat=MCH)
    # spokes, 3-cross
    half = nspokes // 2
    step = 2 * np.pi / nspokes
    off = cross * 4 * np.pi / nspokes
    r_fl = 0.0215
    for k in range(nspokes):
        side = 1 if k % 2 == 0 else -1
        j = k // 2
        rim_a = k * step
        hub_a = rim_a + (off if j % 2 == 0 else -off)
        fy = fl_l if side > 0 else -fl_r
        head_out = (j % 2 == 0)
        hy = fy + side * (0.0018 if head_out else -0.0018)
        p_hub = np.array([math.cos(hub_a) * r_fl, hy, math.sin(hub_a) * r_fl])
        p_rim = np.array([math.cos(rim_a) * (RIM_BED + 0.001), side * 0.0022,
                          math.sin(rim_a) * (RIM_BED + 0.001)])
        d = p_rim - p_hub
        L = np.linalg.norm(d)
        path = np.array([p_hub, p_hub + d * 0.03, p_rim - d * (0.012 / L), p_rim])
        vv, ff, uu = sweep(path, np.array([0.00095, 0.0009, 0.0009, 0.0009]), 6, caps=False)
        mb.add(vv, ff, uu, mat=MSPOKE)
        # nipple
        nip_a = p_rim - d * (0.014 / L)
        vv, ff, uu = tube(nip_a, p_rim + d * (0.003 / L), 0.0019, 8)
        mb.add(vv, ff, uu, mat=MCH)
        # spoke head bend
        hd = np.array([p_hub, p_hub + np.array([0, side * (0.003 if head_out else -0.003), 0])])
        vv, ff, uu = sweep(hd, 0.0016, 8)
        mb.add(vv, ff, uu, mat=MSPOKE)
    # valve stem between two spoke holes
    va = step * 0.5
    pv = np.array([math.cos(va), 0, math.sin(va)])
    vv, ff, uu = tube(pv * 0.2075, pv * 0.181, 0.003, 10)
    mb.add(vv, ff, uu, mat=MCH)
    vv, ff, uu = tube(pv * 0.181, pv * 0.170, 0.0042, 10)
    mb.add(vv, ff, uu, mat=MSPOKE)
    if rear:
        # freewheel body (cog is a separate object so it can freewheel)
        prof = [(0.008, -0.030), (0.016, -0.030), (0.017, -0.035), (0.017, -0.046), (0.008, -0.047)]
        vv, ff, uu = lathe_y(np.array(prof), 32)
        mb.add(vv, ff, uu, mat=MCH)
    ob = mb.build(name, coll, mats=mats)
    return ob


def build_cog(name, coll, mats):
    mb = MeshBuilder()
    outline, rp = sprocket_outline(COG_T, samples=16)
    v, f, uv = ring_band(outline, 0.016, CHAINLINE - 0.0012, CHAINLINE + 0.0012)
    mb.add(v, f, uv, mat=0)
    return mb.build(name, coll, mats=mats, smooth=False)


# ---------------------------------------------------------------------------
# Drivetrain
# ---------------------------------------------------------------------------

def build_crankset(coll, mats):
    """Chainring + spider + cranks, centred on the BB (local origin)."""
    mb = MeshBuilder()
    outline, rp = sprocket_outline(RING_T, samples=16)
    y0, y1 = CHAINLINE - 0.0013, CHAINLINE + 0.0013
    v, f, uv = ring_band(outline, rp - 0.0115, y0, y1)
    mb.add(v, f, uv, mat=0)
    # five swooping arms of the spider, as tapered bars
    for i in range(5):
        a = i * 2 * np.pi / 5 + 0.3
        a2 = a + 0.22
        p0 = np.array([math.cos(a) * 0.018, CHAINLINE + 0.004, math.sin(a) * 0.018])
        pm = np.array([math.cos(a + 0.12) * 0.045, CHAINLINE + 0.0015, math.sin(a + 0.12) * 0.045])
        p1 = np.array([math.cos(a2) * (rp - 0.010), CHAINLINE, math.sin(a2) * (rp - 0.010)])
        path = catmull([p0, pm, p1], 8)
        prof = np.array([[1, 0.35], [-1, 0.35], [-1, -0.35], [1, -0.35]]) * 1.0
        prof = circle_profile(12) * np.array([1.0, 0.32])
        vv, ff, uu = sweep(path, np.linspace(0.0085, 0.0055, len(path)), profile=prof,
                           up=np.array([0, 1, 0]))
        mb.add(vv, ff, uu, mat=1)
        # chainring bolt
        bp = np.array([math.cos(a2) * (rp - 0.010), 0, math.sin(a2) * (rp - 0.010)])
        vv, ff, uu = tube(bp + [0, CHAINLINE - 0.003, 0], bp + [0, CHAINLINE + 0.004, 0], 0.003, 10)
        mb.add(vv, ff, uu, mat=1)
    # spindle
    vv, ff, uu = tube((0, -0.062, 0), (0, 0.062, 0), 0.0075, 16)
    mb.add(vv, ff, uu, mat=1)
    # crank arms (right arm points forward at angle 0, left arm opposite)
    for side in (-1, 1):
        y = side * 0.058
        direc = np.array([1.0, 0, 0]) if side < 0 else np.array([-1.0, 0, 0])
        p0 = np.array([0, y, 0])
        p1 = p0 + direc * CRANK + np.array([0, side * 0.006, 0])
        path = np.array([p0 - direc * 0.012, p0, p0 + direc * 0.03, p1 - direc * 0.01, p1,
                         p1 + direc * 0.012])
        prof = circle_profile(16) * np.array([1.0, 0.55])
        rad = np.array([0.012, 0.013, 0.011, 0.0095, 0.010, 0.009])
        vv, ff, uu = sweep(path, rad, profile=prof, up=np.array([0, 1, 0]))
        mb.add(vv, ff, uu, mat=1)
        # cotter pin
        vv, ff, uu = tube(p0 + [0, 0, 0.010], p0 + [0.0, 0.0, 0.022], 0.0032, 10)
        mb.add(vv, ff, uu, mat=1)
    ob = mb.build("Crankset", coll, mats=mats, smooth=True)
    return ob


def build_pedal(name, coll, mats, side):
    """Rubber-block pedal centred on its spindle start; spindle along +-Y."""
    mb = MeshBuilder()
    s = side
    vv, ff, uu = tube((0, 0, 0), (0, s * 0.105, 0), 0.0045, 12)
    mb.add(vv, ff, uu, mat=0)
    # end plates
    for yy in (s * 0.018, s * 0.100):
        outline = np.array([[-0.034, -0.009], [0.034, -0.009], [0.036, 0.0], [0.034, 0.009],
                            [-0.034, 0.009], [-0.036, 0.0]])
        vv, ff, uu = extrude_outline(outline, yy - 0.0015, yy + 0.0015)
        mb.add(vv, ff, uu, mat=0)
    # rubber blocks front & back
    for xx in (-0.024, 0.024):
        vv, ff, uu = box((0.016, 0.080, 0.020), (xx, s * 0.059, 0))
        mb.add(vv, ff, uu, mat=1)
        # ridges
        for k in range(5):
            vv, ff, uu = box((0.017, 0.006, 0.021), (xx, s * (0.024 + k * 0.0175), 0))
            mb.add(vv, ff, uu, mat=1)
    # rails
    for xx in (-0.008, 0.008):
        for zz in (-0.006, 0.006):
            vv, ff, uu = tube((xx, s * 0.018, zz), (xx, s * 0.100, zz), 0.0018, 8)
            mb.add(vv, ff, uu, mat=0)
    ob = mb.build(name, coll, mats=mats, smooth=False)
    return ob


def chain_path_points():
    """Closed chain path in the XZ plane (bike space, y = CHAINLINE).

    Ordered in the direction of chain travel when pedalling forwards.
    """
    c1 = np.array([BB[0], BB[2]])
    c2 = np.array([A_R[0], A_R[2]])
    r1, r2 = RING_R, COG_R
    d = np.linalg.norm(c2 - c1)
    u = (c2 - c1) / d
    w = np.array([-u[1], u[0]])
    beta = math.acos((r1 - r2) / d)
    n_top = math.cos(beta) * u + math.sin(beta) * w
    n_bot = math.cos(beta) * u - math.sin(beta) * w
    if n_top[1] < n_bot[1]:
        n_top, n_bot = n_bot, n_top
    t1_top, t2_top = c1 + r1 * n_top, c2 + r2 * n_top
    t1_bot, t2_bot = c1 + r1 * n_bot, c2 + r2 * n_bot

    def arc(c, r, a0, a1, cw, n):
        if cw:
            while a1 > a0:
                a1 -= 2 * np.pi
        else:
            while a1 < a0:
                a1 += 2 * np.pi
        a = np.linspace(a0, a1, n)
        return np.stack([c[0] + r * np.cos(a), c[1] + r * np.sin(a)], 1)

    ang = lambda c, p: math.atan2(p[1] - c[1], p[0] - c[0])
    pts = []
    # top run: cog -> ring (moves forward)
    pts.append(np.linspace(t2_top, t1_top, 40)[:-1])
    # around the ring front, clockwise when viewed with x right / z up
    pts.append(arc(c1, r1, ang(c1, t1_top), ang(c1, t1_bot), True, 80)[:-1])
    # bottom run: ring -> cog
    pts.append(np.linspace(t1_bot, t2_bot, 40)[:-1])
    # around the cog back
    pts.append(arc(c2, r2, ang(c2, t2_bot), ang(c2, t2_top), True, 50)[:-1])
    p2 = np.vstack(pts)
    return np.stack([p2[:, 0], np.full(len(p2), CHAINLINE), p2[:, 1]], 1)


def dogbone(length, r_end, waist, n=48):
    """Chain plate outline in XZ, centred, pins at +-length/2."""
    pts = []
    for i in range(n):
        a = 2 * np.pi * i / n
        x, z = math.cos(a), math.sin(a)
        cx = length / 2 if x >= 0 else -length / 2
        px = cx + x * r_end
        pz = z * r_end
        # pinch the waist
        t = 1 - min(1.0, abs(px) / (length / 2))
        pz *= 1 - (1 - waist / r_end) * smoothstep(0.0, 1.0, t) * 1.0
        pts.append((px, pz))
    return np.array(pts)


def build_chain_links(coll, mat):
    p = PITCH
    inner = MeshBuilder()
    for s in (-1, 1):
        v, f, uv = extrude_outline(dogbone(p, 0.0047, 0.0034), s * 0.0036 - 0.00045,
                                   s * 0.0036 + 0.00045)
        inner.add(v, f, uv)
    for x in (-p / 2, p / 2):
        v, f, uv = tube((x, -0.0033, 0), (x, 0.0033, 0), 0.0039, 12)
        inner.add(v, f, uv)
    outer = MeshBuilder()
    for s in (-1, 1):
        v, f, uv = extrude_outline(dogbone(p, 0.0047, 0.0036), s * 0.0049 - 0.00045,
                                   s * 0.0049 + 0.00045)
        outer.add(v, f, uv)
    for x in (-p / 2, p / 2):
        v, f, uv = tube((x, -0.0058, 0), (x, 0.0058, 0), 0.0018, 10)
        outer.add(v, f, uv)
    a = inner.build("ChainInner", coll, mats=[mat], smooth=False)
    b = outer.build("ChainOuter", coll, mats=[mat], smooth=False)
    return a, b


def chain_geonodes(protos_coll, count, pitch_eff):
    ng = bpy.data.node_groups.new("ChainLinks", 'GeometryNodeTree')
    ng.interface.new_socket('Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
    s_off = ng.interface.new_socket('Offset', in_out='INPUT', socket_type='NodeSocketFloat')
    ng.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes
    L = ng.links
    gi = N.new('NodeGroupInput')
    go = N.new('NodeGroupOutput')
    idx = N.new('GeometryNodeInputIndex')
    clen = N.new('GeometryNodeCurveLength')
    L.new(gi.outputs['Geometry'], clen.inputs['Curve'])

    def math_node(op, a=None, b=None):
        m = N.new('ShaderNodeMath')
        m.operation = op
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, bpy.types.NodeSocket):
                L.new(x, m.inputs[i])
            else:
                m.inputs[i].default_value = x
        return m.outputs[0]

    s = math_node('ADD', math_node('MULTIPLY', idx.outputs[0], pitch_eff), gi.outputs['Offset'])
    s = math_node('FLOORED_MODULO', s, clen.outputs[0])
    samp = N.new('GeometryNodeSampleCurve')
    samp.mode = 'LENGTH'
    L.new(gi.outputs['Geometry'], samp.inputs['Curves'])
    L.new(s, samp.inputs['Length'])
    pts = N.new('GeometryNodePoints')
    pts.inputs['Count'].default_value = count
    L.new(samp.outputs['Position'], pts.inputs['Position'])
    align = N.new('FunctionNodeAlignRotationToVector')
    align.axis = 'X'
    align.pivot_axis = 'Y'
    L.new(samp.outputs['Tangent'], align.inputs['Vector'])
    ci = N.new('GeometryNodeCollectionInfo')
    ci.inputs['Collection'].default_value = protos_coll
    ci.inputs['Separate Children'].default_value = True
    ci.inputs['Reset Children'].default_value = True
    ci.transform_space = 'ORIGINAL'
    iop = N.new('GeometryNodeInstanceOnPoints')
    L.new(pts.outputs[0], iop.inputs['Points'])
    L.new(ci.outputs[0], iop.inputs['Instance'])
    iop.inputs['Pick Instance'].default_value = True
    L.new(math_node('MODULO', idx.outputs[0], 2.0), iop.inputs['Instance Index'])
    L.new(align.outputs[0], iop.inputs['Rotation'])
    # stable ids for motion blur
    store = N.new('GeometryNodeStoreNamedAttribute')
    store.data_type = 'INT'
    store.domain = 'INSTANCE'
    store.inputs['Name'].default_value = 'id'
    L.new(iop.outputs[0], store.inputs['Geometry'])
    L.new(idx.outputs[0], store.inputs['Value'])
    L.new(store.outputs[0], go.inputs['Geometry'])
    return ng, s_off.identifier


# ---------------------------------------------------------------------------
# Frame
# ---------------------------------------------------------------------------

def build_frame(coll, mats):
    """Lugged steel frame. mats: [paint, chrome, gold, cream]"""
    MP, MC, MG, MCR = 0, 1, 2, 3
    mb = MeshBuilder()
    sides = 24
    st_bot = BB + 0.012 * SEAT_DIR
    tt_rear = seat_point(0.444)
    tt_front = HT_TOP - 0.018 * STEER_DIR
    dt_front = HT_BOT + 0.016 * STEER_DIR
    # main tubes
    for a, b, r in ((st_bot, ST_TOP, 0.0125), (tt_rear, tt_front, 0.0112),
                    (BB, dt_front, 0.0135)):
        v, f, uv = tube(a, b, r, sides, n=6)
        mb.add(v, f, uv, mat=MP)
    v, f, uv = tube(HT_BOT - 0.008 * STEER_DIR, HT_TOP + 0.004 * STEER_DIR, 0.0158, sides)
    mb.add(v, f, uv, mat=MP)
    # head lugs (chrome sleeves with pointed tangs approximated by flares)
    for p, d in ((HT_TOP, 1), (HT_BOT, -1)):
        v, f, uv = tube(p - d * 0.016 * STEER_DIR, p + d * 0.004 * STEER_DIR, 0.0172, sides)
        mb.add(v, f, uv, mat=MC)
        v, f, uv = tube(p - d * 0.0175 * STEER_DIR, p - d * 0.0155 * STEER_DIR, 0.0175, sides)
        mb.add(v, f, uv, mat=MG)
    # top tube / down tube lug sleeves + gold pinstripe rings
    def sleeve(p, direction, length, r):
        direction = direction / np.linalg.norm(direction)
        v, f, uv = tube(p, p + direction * length, r + 0.0011, sides)
        mb.add(v, f, uv, mat=MC)
        q = p + direction * (length + 0.0015)
        v, f, uv = tube(q - direction * 0.0008, q + direction * 0.0008, r + 0.0006, sides)
        mb.add(v, f, uv, mat=MG)
    sleeve(tt_front, tt_rear - tt_front, 0.024, 0.0112)
    sleeve(tt_rear, tt_front - tt_rear, 0.022, 0.0112)
    sleeve(dt_front, BB - dt_front, 0.026, 0.0135)
    sleeve(ST_TOP, -SEAT_DIR, 0.036, 0.0125)
    # seat lug ears + binder bolt
    v, f, uv = tube(ST_TOP - 0.02 * SEAT_DIR + [-0.012, -0.012, 0], ST_TOP - 0.02 * SEAT_DIR + [-0.012, 0.012, 0], 0.0045, 10)
    mb.add(v, f, uv, mat=MC)
    # BB shell
    v, f, uv = tube(BB + [0, -0.034, 0], BB + [0, 0.034, 0], 0.0195, sides)
    mb.add(v, f, uv, mat=MP)
    for yy in (-0.035, 0.035):
        v, f, uv = tube(BB + [0, yy - 0.003, 0], BB + [0, yy + 0.003, 0], 0.0205, sides)
        mb.add(v, f, uv, mat=MC)
    # chainstays: from BB to rear dropouts, bowed out around the tyre
    for s in (-1, 1):
        cs = catmull([BB + [-0.02, s * 0.020, 0.0], BB + [-0.10, s * 0.032, 0.004],
                      A_R + [0.13, s * 0.046, -0.025], A_R + [0.012, s * 0.055, -0.002]], 10)
        v, f, uv = sweep(cs, np.linspace(0.0100, 0.0068, len(cs)), 16)
        mb.add(v, f, uv, mat=MP)
        ss = catmull([seat_point(0.432) + [0.004, s * 0.016, 0], seat_point(0.432) + [-0.06, s * 0.036, -0.02],
                      A_R + [0.03, s * 0.052, 0.07], A_R + [0.006, s * 0.055, 0.006]], 10)
        v, f, uv = sweep(ss, np.linspace(0.0082, 0.0062, len(ss)), 16)
        mb.add(v, f, uv, mat=MP)
        # seat stay caps (chrome bullets)
        v, f, uv = uv_sphere(0.0085, 16, 8, center=ss[0])
        mb.add(v, f, uv, mat=MC)
        # dropout plate
        outline = np.array([[-0.004, -0.010], [0.022, -0.004], [0.026, 0.012], [0.012, 0.016],
                            [-0.008, 0.010], [-0.011, 0.0]])
        vv, ff, uu = extrude_outline(outline, s * 0.055 - 0.0025, s * 0.055 + 0.0025)
        mb.add(vv + A_R * [1, 0, 1], ff, uu, mat=MC)
    # seat stay bridge + chainstay bridge
    v, f, uv = tube(seat_point(0.432) + [-0.10, -0.038, -0.038], seat_point(0.432) + [-0.10, 0.038, -0.038], 0.0055, 12)
    mb.add(v, f, uv, mat=MP)
    v, f, uv = tube(BB + [-0.075, -0.029, 0.002], BB + [-0.075, 0.029, 0.002], 0.006, 12)
    mb.add(v, f, uv, mat=MP)
    # cable guides on top tube
    for t in (0.25, 0.5, 0.75):
        p = tt_rear + (tt_front - tt_rear) * t + [0, 0, 0.0115]
        v, f, uv = box((0.008, 0.006, 0.004), p)
        mb.add(v, f, uv, mat=MC)
    # head badge (gold shield) on the front of the head tube
    hb_c = (HT_TOP + HT_BOT) / 2 + STEER_FWD * 0.0160
    shield = np.array([[0.0, -0.014], [0.010, -0.008], [0.010, 0.012], [0.0, 0.016], [-0.010, 0.012],
                       [-0.010, -0.008]])
    vv, ff, uu = extrude_outline(shield, -0.0006, 0.0006)
    # orient: plate faces forward (STEER_FWD), its long axis along steering axis
    M = np.eye(4)
    M[:3, 0] = [0, 1, 0]
    M[:3, 1] = STEER_FWD
    M[:3, 2] = STEER_DIR
    M[:3, 3] = hb_c
    vv = np.stack([vv[:, 0], vv[:, 1], vv[:, 2]], 1)
    mb.add(transform(vv, M), ff, uu, mat=MG)
    # kickstand (folded along left chainstay)
    ks0 = BB + [-0.06, 0.035, -0.012]
    v, f, uv = sweep(np.array([ks0, ks0 + [-0.08, 0.012, 0.01], ks0 + [-0.20, 0.022, 0.03]]),
                     np.array([0.0065, 0.0055, 0.0045]), 12)
    mb.add(v, f, uv, mat=MC)
    frame = mb.build("Frame", coll, mats=mats, smooth=True)
    return frame


def build_fork(coll, mats):
    MP, MC, MG = 0, 1, 2
    mb = MeshBuilder()
    # steerer visible above head tube (chrome headset cups)
    for p, d in ((HT_TOP + 0.004 * STEER_DIR, 1), (HT_BOT - 0.008 * STEER_DIR, -1)):
        v, f, uv = tube(p, p + d * 0.009 * STEER_DIR, 0.0185, 24)
        mb.add(v, f, uv, mat=MC)
    v, f, uv = tube(HT_TOP + 0.013 * STEER_DIR, HT_TOP + 0.020 * STEER_DIR, 0.0165, 6)
    mb.add(v, f, uv, mat=MC)
    # crown
    crown_c = CROWN
    v, f, uv = uv_sphere(1.0, 24, 12, center=crown_c, scale=(0.020, 0.045, 0.012))
    mb.add(v, f, uv, mat=MC)
    for s in (-1, 1):
        top = crown_c + np.array([0, s * 0.036, 0]) - 0.004 * STEER_DIR
        bot = A_F + np.array([0, s * 0.050, 0])
        mid1 = top - 0.12 * STEER_DIR
        path = bezier(top, mid1, bot + np.array([-0.02, 0, 0.10]), bot, 24)
        prof = circle_profile(16) * np.array([1.0, 0.7])
        v, f, uv = sweep(path, np.linspace(0.0115, 0.0065, len(path)), profile=prof,
                         up=np.array([0, 1, 0]))
        mb.add(v, f, uv, mat=MP)
        # chrome fork tips
        v, f, uv = sweep(path[-6:], np.linspace(0.0078, 0.0066, 6) + 0.0004, profile=prof,
                         up=np.array([0, 1, 0]))
        mb.add(v, f, uv, mat=MC)
    return mb.build("Fork", coll, mats=mats)


def build_cockpit(coll, mats):
    """Stem, North-Road handlebar, grips, brake levers, bell.
    mats: [chrome, cork, rubber, paint]"""
    MC, MK, MR, MP = 0, 1, 2, 3
    mb = MeshBuilder()
    # quill stem: up the steering axis then forward
    q0 = HT_TOP + 0.015 * STEER_DIR
    q1 = STEM_TOP
    v, f, uv = tube(q0, q1, 0.0110, 20)
    mb.add(v, f, uv, mat=MC)
    ext = catmull([q1 - 0.01 * STEER_DIR, q1 + np.array([0.02, 0, 0.012]), q1 + np.array([0.07, 0, 0.006])], 8)
    v, f, uv = sweep(ext, np.linspace(0.0115, 0.0105, len(ext)), 20)
    mb.add(v, f, uv, mat=MC)
    # expander bolt
    v, f, uv = tube(q1 + 0.0 * STEER_DIR, q1 + 0.012 * STEER_DIR, 0.0060, 12)
    mb.add(v, f, uv, mat=MC)
    clamp = q1 + np.array([0.072, 0, 0.006])
    v, f, uv = tube(clamp + [0, -0.022, 0], clamp + [0, 0.022, 0], 0.0145, 20)
    mb.add(v, f, uv, mat=MC)
    # bars
    def half_bar(s):
        pts = np.array([[0, 0, 0], [0.0, 0.050, 0.0], [-0.010, 0.115, 0.010], [-0.045, 0.168, 0.022],
                        [-0.095, 0.188, 0.028], [-0.150, 0.193, 0.028], [-0.205, 0.195, 0.026]])
        pts[:, 1] *= s
        return catmull(pts + clamp, 10)
    grips = {}
    for s in (-1, 1):
        path = half_bar(s)
        v, f, uv = sweep(path, 0.0112, 20)
        mb.add(v, f, uv, mat=MC)
        # grips over the last 10 cm
        g = resample(path[-18:], 30)
        u = np.linspace(0, 1, len(g))
        rad = 0.0158 + 0.0012 * np.sin(u * np.pi * 14) ** 2 - 0.0016 * (u < 0.06)
        rad[-1] = 0.0150
        v, f, uv = sweep(g, rad, 24)
        mb.add(v, f, uv, mat=MK)
        # grip end cap
        v, f, uv = uv_sphere(1.0, 16, 8, center=g[-1], scale=(0.010, 0.016, 0.016))
        mb.add(v, f, uv, mat=MC)
        grips['L' if s > 0 else 'R'] = (g[0], g[-1])
        # brake lever (pull-rod style lever in front of the grip)
        piv = path[-20] + np.array([0.022, 0, 0.0])
        lever = catmull([piv, piv + [0.030, s * 0.010, -0.012], piv + [0.020, s * 0.045, -0.032],
                         piv + [-0.010, s * 0.070, -0.038]], 8)
        v, f, uv = sweep(lever, np.linspace(0.0050, 0.0040, len(lever)), 12)
        mb.add(v, f, uv, mat=MC)
        v, f, uv = uv_sphere(1.0, 16, 8, center=piv, scale=(0.014, 0.012, 0.016))
        mb.add(v, f, uv, mat=MC)
    # bell on the left bar, inboard of the grip
    bp = half_bar(1)[-26] + np.array([0.0, 0.0, 0.016])
    prof = np.array([[0.0005, 0.0185], [0.008, 0.018], [0.016, 0.0155], [0.022, 0.010], [0.025, 0.004],
                     [0.0262, -0.002], [0.0255, -0.004], [0.0235, -0.002], [0.020, 0.006],
                     [0.012, 0.0125], [0.0005, 0.0145]])
    v, f, uv = lathe(prof, 48, closed_top=False)
    v = v + bp
    mb.add(v, f, uv, mat=MC)
    v, f, uv = tube(bp + [0, 0, 0.0185], bp + [0, 0, 0.0225], 0.003, 10)
    mb.add(v, f, uv, mat=MC)
    v, f, uv = tube(bp + [0, 0, -0.002], bp + [0, 0, -0.016], 0.0035, 10)
    mb.add(v, f, uv, mat=MC)
    bell_lever = catmull([bp + [-0.005, 0.0, -0.004], bp + [-0.02, -0.010, -0.006], bp + [-0.032, -0.016, -0.009]], 6)
    v, f, uv = sweep(bell_lever, 0.0024, 8)
    mb.add(v, f, uv, mat=MC)
    v, f, uv = uv_sphere(0.0045, 12, 6, center=bell_lever[-1])
    mb.add(v, f, uv, mat=MR)
    ob = mb.build("Cockpit", coll, mats=mats)
    return ob, grips, bp


def build_saddle(coll, mats):
    """Sprung leather saddle (B67 style). mats: [leather, chrome, copper]"""
    ML, MC, MCU = 0, 1, 2
    mb = MeshBuilder()
    top_c = SADDLE_CLAMP + np.array([0.012, 0, 0.048])
    nu, nv = 48, 34
    Ls = 0.255
    rings = []
    for i in range(nu):
        t = i / (nu - 1)               # 0 back -> 1 nose
        w = 0.052 + 0.150 * (1 - smoothstep(0.18, 0.80, t)) ** 1.15
        w *= (1 - 0.18 * (1 - smoothstep(0.0, 0.10, t)))
        x = -Ls * 0.42 + t * Ls
        z0 = 0.004 * math.sin(t * math.pi) - 0.006 * smoothstep(0.75, 1.0, t)
        ring = []
        for j in range(nv):
            vv = -1 + 2 * j / (nv - 1)
            y = vv * w / 2
            dome = -0.010 * vv * vv
            edge = smoothstep(0.80, 1.0, abs(vv))
            skirt = -0.034 * edge * (1 - 0.6 * t)
            xb = x - 0.010 * (1 - vv * vv) * (1 - t) ** 6
            backskirt = -0.03 * (1 - smoothstep(0.0, 0.07, t)) * (1 - edge)
            yy = y * (1 - 0.08 * edge)
            ring.append([xb, yy, z0 + dome + skirt + backskirt])
        rings.append(ring)
    rings = np.array(rings) + top_c
    v, f, uv = loft(rings, closed_rings=False)
    mb.add(v, f, uv, mat=ML)
    # rivets along the cantle
    back = rings[1]
    for k in range(5):
        j = int(round(5 + k * (nv - 11) / 4))
        p = back[j] + np.array([0.004, 0, 0.0])
        sv, sf, su = uv_sphere(1.0, 12, 6, center=p, scale=(0.0045, 0.0045, 0.0035))
        mb.add(sv, sf, su, mat=MCU)
    # nose rivet
    sv, sf, su = uv_sphere(1.0, 12, 6, center=rings[-2][nv // 2] + [0, 0, 0.002], scale=(0.004, 0.004, 0.003))
    mb.add(sv, sf, su, mat=MCU)
    # rails and springs
    nose = top_c + np.array([Ls * 0.50, 0, -0.012])
    for s in (-1, 1):
        sp_top = top_c + np.array([-0.080, s * 0.052, -0.022])
        sp_bot = sp_top + np.array([0.012, 0, -0.050])
        # coil spring
        tt = np.linspace(0, 1, 160)
        helix = np.stack([np.cos(tt * 2 * np.pi * 7) * 0.011, np.sin(tt * 2 * np.pi * 7) * 0.011,
                          -tt * 0.050], 1)
        axis = sp_bot - sp_top
        helix = helix + sp_top + np.outer(tt, axis - np.array([0, 0, -0.050]))
        v, f, uv = sweep(helix, 0.0017, 8)
        mb.add(v, f, uv, mat=MC)
        rail = catmull([nose + [0, s * 0.006, -0.002], nose + [-0.06, s * 0.020, -0.018],
                        SADDLE_CLAMP + [0.0, s * 0.026, 0.0], sp_bot + [0.004, 0, -0.002],
                        sp_bot + [-0.004, 0, 0.004]], 10)
        v, f, uv = sweep(rail, 0.0022, 10)
        mb.add(v, f, uv, mat=MC)
        v, f, uv = sweep(np.array([sp_top + [0, 0, 0.006], top_c + [-0.075, s * 0.040, -0.004]]), 0.003, 10)
        mb.add(v, f, uv, mat=MC)
    # cantle plate
    v, f, uv = tube(top_c + [-0.100, -0.060, -0.020], top_c + [-0.100, 0.060, -0.020], 0.0035, 10)
    mb.add(v, f, uv, mat=MC)
    # clamp
    v, f, uv = tube(SADDLE_CLAMP + [0, -0.030, 0], SADDLE_CLAMP + [0, 0.030, 0], 0.0075, 14)
    mb.add(v, f, uv, mat=MC)
    for s in (-1, 1):
        nut = SADDLE_CLAMP + [0, s * 0.033, 0]
        v, f, uv = tube(nut - [0, 0.003, 0], nut + [0, 0.003, 0], 0.0075, 6)
        mb.add(v, f, uv, mat=MC)
    # seatpost
    v, f, uv = tube(ST_TOP - 0.02 * SEAT_DIR, SADDLE_CLAMP + 0.006 * SEAT_DIR, 0.0108, 20)
    mb.add(v, f, uv, mat=MC)
    ob = mb.build("Saddle", coll, mats=mats)
    return ob, top_c


def fender(center_x, angle0, angle1, radius, width=0.052, n=90, tip_color=False):
    a = np.linspace(angle0, angle1, n)
    prof_y = np.linspace(-1, 1, 15)
    rings = []
    for ang in a:
        d = np.array([math.cos(ang), 0, math.sin(ang)])
        ring = []
        for yv in prof_y:
            rr = radius - 0.010 * (yv * yv) ** 1.2
            p = np.array([center_x, 0, R]) + d * rr + np.array([0, yv * width / 2, 0])
            ring.append(p)
        rings.append(ring)
    return loft(np.array(rings), closed_rings=False)


def build_fenders(coll, mats_paint_chrome, steer_mats):
    """Rear fender on the frame; front fender returned separately (steers)."""
    mb = MeshBuilder()
    v, f, uv = fender(0.0, math.radians(-12), math.radians(150), R + 0.016)
    mb.add(v, f, uv, mat=0)
    # rear stays
    for s in (-1, 1):
        for ang in (math.radians(140), math.radians(175)):
            d = np.array([math.cos(ang), 0, math.sin(ang)])
            pa = A_R + np.array([0, s * 0.057, 0])
            pb = A_R + d * (R + 0.014) + np.array([0, s * 0.024, 0])
            v, f, uv = tube(pa, pb, 0.0022, 8)
            mb.add(v, f, uv, mat=1)
    # rear reflector
    ang = math.radians(165)
    d = np.array([math.cos(ang), 0, math.sin(ang)])
    rp = A_R + d * (R + 0.022)
    v, f, uv = uv_sphere(1.0, 20, 10, center=rp, scale=(0.008, 0.020, 0.012))
    mb.add(v, f, uv, mat=2)
    rear = mb.build("RearFender", coll, mats=mats_paint_chrome)
    mb2 = MeshBuilder()
    v, f, uv = fender(WHEELBASE, math.radians(15), math.radians(150), R + 0.016, width=0.050)
    mb2.add(v, f, uv, mat=0)
    # white tip on front fender bottom (classic safety tip)
    v, f, uv = fender(WHEELBASE, math.radians(-25), math.radians(15), R + 0.0162, width=0.0505, n=20)
    mb2.add(v, f, uv, mat=2)
    for s in (-1, 1):
        ang = math.radians(25)
        d = np.array([math.cos(ang), 0, math.sin(ang)])
        pa = A_F + np.array([0, s * 0.052, 0])
        pb = A_F + d * (R + 0.014) + np.array([0, s * 0.024, 0])
        v, f, uv = tube(pa, pb, 0.0022, 8)
        mb2.add(v, f, uv, mat=1)
    front = mb2.build("FrontFender", coll, mats=steer_mats)
    return rear, front


def build_brakes(coll, mats, grips):
    """Side-pull calipers + cable housings (front set returned separately)."""
    MC, MR = 0, 1
    out = {}
    for which in ('front', 'rear'):
        mb = MeshBuilder()
        if which == 'front':
            piv = CROWN + STEER_FWD * 0.022 - STEER_DIR * 0.004
            wc = A_F
        else:
            piv = seat_point(0.432) + np.array([-0.10, 0, -0.038]) + np.array([-0.012, 0, 0.0])
            wc = A_R
        # caliper arms reaching around the tyre to the rim
        to_rim = wc + (piv - wc) / np.linalg.norm(piv - wc) * 0.205
        for s in (-1, 1):
            arm = catmull([piv + [0, s * 0.006, 0], piv + (to_rim - piv) * 0.35 + [0, s * 0.040, 0],
                           to_rim + [0, s * 0.020, 0]], 8)
            v, f, uv = sweep(arm, np.linspace(0.0045, 0.0035, len(arm)), profile=circle_profile(10) * [1, 0.5],
                             up=np.array([0, 1, 0]))
            mb.add(v, f, uv, mat=MC)
            v, f, uv = box((0.022, 0.004, 0.006), to_rim + [0, s * 0.015, 0])
            mb.add(v, f, uv, mat=MR)
        v, f, uv = tube(piv + [0, -0.012, 0], piv + [0, 0.012, 0], 0.005, 12)
        mb.add(v, f, uv, mat=MC)
        out[which] = (mb, piv)
    # cable housing from levers
    fr_mb, fr_piv = out['front']
    lever_L = grips['L'][0] + np.array([0.02, 0.0, -0.01])
    lever_R = grips['R'][0] + np.array([0.02, 0.0, -0.01])
    housing = catmull([lever_R, lever_R + [0.10, 0.02, -0.03], STEM_TOP + [0.10, -0.02, -0.02],
                       fr_piv + [0.012, -0.004, 0.05], fr_piv + [0.004, -0.008, 0.010]], 10)
    v, f, uv = sweep(housing, 0.0026, 10)
    fr_mb.add(v, f, uv, mat=MR)
    re_mb, re_piv = out['rear']
    housing2 = catmull([lever_L, lever_L + [0.10, -0.03, -0.04], STEM_TOP + [0.03, 0.035, -0.05],
                        HT_TOP + [-0.04, 0.01, -0.002]], 10)
    v, f, uv = sweep(housing2, 0.0026, 10)
    fr_mb.add(v, f, uv, mat=MR)
    tt_rear = seat_point(0.444)
    tt_front = HT_TOP - 0.018 * STEER_DIR
    cable = np.linspace(tt_front + [-0.03, 0, 0.0145], tt_rear + [0.03, 0, 0.0145], 8)
    v, f, uv = sweep(cable, 0.0009, 6)
    re_mb.add(v, f, uv, mat=MC)
    housing3 = catmull([tt_rear + [0.02, 0, 0.0145], tt_rear + [-0.03, 0.0, 0.03],
                        re_piv + [0.03, 0.004, 0.04], re_piv + [0.004, 0.006, 0.010]], 10)
    v, f, uv = sweep(housing3, 0.0026, 10)
    re_mb.add(v, f, uv, mat=MR)
    front = fr_mb.build("BrakeFront", coll, mats=mats)
    rear = re_mb.build("BrakeRear", coll, mats=mats)
    return front, rear


def build_headlamp(coll, mats, mount):
    """Bullet lamp bolted to the front of the basket. mats: [chrome, glass, emit]"""
    mb = MeshBuilder()
    c = np.asarray(mount) + np.array([0.045, 0, 0.0])
    prof = np.array([[0.0005, -0.050], [0.012, -0.046], [0.020, -0.036], [0.026, -0.018],
                     [0.029, 0.0], [0.0305, 0.004], [0.0305, 0.008], [0.027, 0.009]])
    v, f, uv = lathe(prof, 48)
    M = np.eye(4)
    M[:3, 0] = [0, 1, 0]
    M[:3, 1] = [0, 0, 1]
    M[:3, 2] = [1, 0, 0]
    M[:3, 3] = c
    mb.add(transform(v, M), f, uv, mat=0)
    lens = np.array([[0.0005, 0.0125], [0.012, 0.0115], [0.022, 0.0098], [0.0272, 0.0086]])
    v, f, uv = lathe(lens, 48)
    mb.add(transform(v, M), f, uv, mat=1)
    v, f, uv = uv_sphere(0.010, 16, 8, center=c + [0.002, 0, 0])
    mb.add(v, f, uv, mat=2)
    refl = np.array([[0.004, -0.012], [0.012, -0.008], [0.020, -0.0], [0.026, 0.008]])
    v, f, uv = lathe(refl, 48)
    mb.add(transform(v, M), f, uv, mat=0)
    v, f, uv = sweep(np.array([np.asarray(mount) + [-0.004, 0, 0], c + [-0.024, 0, 0.0]]), 0.0045, 10)
    mb.add(v, f, uv, mat=0)
    v, f, uv = box((0.004, 0.03, 0.03), np.asarray(mount))
    mb.add(v, f, uv, mat=0)
    return mb.build("Headlamp", coll, mats=mats)


def build_basket(coll, mats):
    """Woven wicker basket hung from the bars. mats: [wicker, leather, chrome]"""
    MW, ML, MC = 0, 1, 2
    mb = MeshBuilder()
    cx = WHEELBASE + 0.035
    bottom_z = 0.535
    height = 0.165
    hx, hy = 0.125, 0.155         # half extents at the bottom
    flare = 0.018                  # wider at the top
    corner = 0.045

    def outline(t, grow):
        """Rounded rectangle point at parameter t in [0,1)."""
        ax, ay = hx + grow, hy + grow
        cr = corner + grow * 0.5
        straight_x = 2 * (ax - cr)
        straight_y = 2 * (ay - cr)
        arc = 0.5 * np.pi * cr
        per = 2 * straight_x + 2 * straight_y + 4 * arc
        s = (t % 1.0) * per
        segs = [('L', np.array([ax - cr, -ay]), np.array([-1, 0]), straight_x),
                ('A', np.array([-ax + cr, -ay + cr]), -np.pi / 2, arc),
                ('L', np.array([-ax, -ay + cr]), np.array([0, 1]), straight_y),
                ('A', np.array([-ax + cr, ay - cr]), np.pi, arc),
                ('L', np.array([-ax + cr, ay]), np.array([1, 0]), straight_x),
                ('A', np.array([ax - cr, ay - cr]), np.pi / 2, arc),
                ('L', np.array([ax, ay - cr]), np.array([0, -1]), straight_y),
                ('A', np.array([ax - cr, -ay + cr]), 0.0, arc)]
        for kind, p, d, ln in segs:
            if s <= ln or kind == segs[-1][0] and s <= ln + 1e-9:
                if kind == 'L':
                    q = p + d * s
                    nrm = np.array([d[1], -d[0]])
                else:
                    a = d - s / cr
                    q = p + cr * np.array([math.cos(a + np.pi / 2 * 0), math.sin(a)])
                    q = p + cr * np.array([math.cos(a), math.sin(a)])
                    nrm = np.array([math.cos(a), math.sin(a)])
                return q, nrm, per
            s -= ln
        return segs[0][1], np.array([0, -1.0]), per

    # stakes
    _, _, per0 = outline(0.0, 0.0)
    n_stakes = int(per0 / 0.022)
    n_stakes += n_stakes % 2
    for k in range(n_stakes):
        t = k / n_stakes
        pts = []
        for h in np.linspace(-0.012, height + 0.004, 12):
            q, nrm, _ = outline(t, flare * h / height)
            pts.append([cx + q[0], q[1], bottom_z + h])
        v, f, uv = sweep(np.array(pts), 0.0022, 6)
        mb.add(v, f, uv, mat=MW)
    # weavers: over-under around stakes, alternating each row
    rows = int(height / 0.0072)
    samples = n_stakes * 8
    for r in range(rows):
        h = 0.004 + r * 0.0072
        grow = flare * h / height
        pts = []
        for i in range(samples + 1):
            t = i / samples
            q, nrm, _ = outline(t, grow)
            phase = (t * n_stakes + 0.5 * (r % 2)) * np.pi
            off = 0.0026 * math.cos(phase)
            pts.append([cx + q[0] + nrm[0] * off, q[1] + nrm[1] * off,
                        bottom_z + h + 0.0006 * math.sin(phase * 0.5)])
        pts = np.array(pts[:-1])
        prof = circle_profile(6) * np.array([1.0, 0.45])
        v, f, uv = sweep(pts, 0.0034, profile=prof, closed=True, up=np.array([0, 0, 1]))
        mb.add(v, f, uv, mat=MW)
    # braided rim
    rim_pts = []
    for i in range(400):
        t = i / 400
        q, nrm, _ = outline(t, flare * 1.03)
        rim_pts.append([cx + q[0], q[1], bottom_z + height + 0.006])
    rim_pts = np.array(rim_pts)
    for ph in (0, 2 * np.pi / 3, 4 * np.pi / 3):
        tw = []
        for i, p in enumerate(rim_pts):
            q, nrm, _ = outline(i / 400, flare * 1.03)
            a = i / 400 * 2 * np.pi * 70 + ph
            tw.append(p + np.array([nrm[0], nrm[1], 0]) * math.cos(a) * 0.0045 +
                      np.array([0, 0, 1]) * math.sin(a) * 0.0045)
        v, f, uv = sweep(np.array(tw), 0.0035, 6, closed=True)
        mb.add(v, f, uv, mat=MW)
    # base: woven floor
    for k in range(-6, 7):
        y = k * hy / 6.5
        v, f, uv = sweep(np.array([[cx - hx + 0.01, y, bottom_z - 0.004], [cx + hx - 0.01, y, bottom_z - 0.004]]),
                         0.004, profile=circle_profile(6) * [1, 0.4], up=np.array([0, 0, 1]))
        mb.add(v, f, uv, mat=MW)
    for k in range(-4, 5):
        x = cx + k * hx / 4.8
        v, f, uv = sweep(np.array([[x, -hy + 0.01, bottom_z - 0.008], [x, hy - 0.01, bottom_z - 0.008]]),
                         0.0042, profile=circle_profile(6) * [1, 0.4], up=np.array([0, 0, 1]))
        mb.add(v, f, uv, mat=MW)
    # leather straps to the handlebar and chrome support struts to the axle
    for s in (-1, 1):
        a0 = np.array([cx - hx - 0.004, s * 0.05, bottom_z + height - 0.01])
        strap = catmull([a0, a0 + [-0.03, 0, 0.04], STEM_TOP + [0.072, s * 0.05, 0.02],
                         STEM_TOP + [0.060, s * 0.05, -0.004]], 8)
        v, f, uv = sweep(strap, 1.0, profile=np.array([[0.0015, -0.009], [0.0015, 0.009],
                                                        [-0.0015, 0.009], [-0.0015, -0.009]]),
                         up=np.array([0, 1, 0]))
        mb.add(v, f, uv, mat=ML)
        st = np.array([A_F + [0.0, s * 0.056, 0.0], np.array([cx + hx * 0.4, s * 0.07, bottom_z - 0.01])])
        v, f, uv = tube(st[0], st[1], 0.0028, 10)
        mb.add(v, f, uv, mat=MC)
    v, f, uv = tube(np.array([cx + hx * 0.4, -0.08, bottom_z - 0.012]), np.array([cx + hx * 0.4, 0.08, bottom_z - 0.012]), 0.003, 10)
    mb.add(v, f, uv, mat=MC)
    return mb.build("Basket", coll, mats=mats), np.array([cx, 0, bottom_z]), (hx, hy, height)


def fish_mesh(length=0.26, n_u=40, n_v=24):
    """A mackerel: lofted body + tail + fins. Returns MeshBuilder (mats: skin, eye, fin)."""
    mb = MeshBuilder()
    rings = []
    for i in range(n_u):
        t = i / (n_u - 1)
        x = t * length
        # height and width profiles (head at t=0)
        hgt = 0.5 * length * 0.19 * (math.sin(math.pi * min(1, (t + 0.06) / 1.0)) ** 0.75) * (1 - 0.82 * smoothstep(0.75, 1.0, t))
        wid = hgt * 0.62
        if t < 0.08:
            hgt *= 0.55 + 0.45 * t / 0.08
            wid *= 0.6 + 0.4 * t / 0.08
        ring = []
        for j in range(n_v):
            a = 2 * np.pi * j / n_v - np.pi / 2
            ring.append([x, math.cos(a) * wid, math.sin(a) * hgt - 0.12 * hgt * math.cos(a) ** 2 * 0])
        rings.append(ring)
    v, f, uv = loft(np.array(rings), closed_rings=True, cap_start=True, cap_end=True)
    mb.add(v, f, uv, mat=0)
    # forked tail
    tail_base = np.array([length * 0.985, 0, 0])
    for s in (-1, 1):
        tip = tail_base + np.array([length * 0.16, 0, s * length * 0.11])
        mid = tail_base + np.array([length * 0.07, 0, s * length * 0.015])
        tri_v = np.array([tail_base + [0, 0, s * 0.006], tip, mid, tail_base + [0, 0, -s * 0.002]])
        tri_v2 = tri_v.copy()
        tri_v[:, 1] += 0.0008
        tri_v2[:, 1] -= 0.0008
        mb.add(np.vstack([tri_v, tri_v2]), [[0, 1, 2, 3], [7, 6, 5, 4]], mat=2)
    # dorsal finlets & fins
    for (t0, t1, hfac) in ((0.30, 0.45, 0.07), (0.55, 0.65, 0.05)):
        a = np.array([t0 * length, 0, length * 0.085])
        b = np.array([t1 * length, 0, length * 0.075])
        c = np.array([(t0 + 0.03) * length, 0, length * (0.085 + hfac)])
        tri = np.array([a, c, b])
        mb.add(np.vstack([tri + [0, 0.0006, 0], tri - [0, 0.0006, 0]]), [[0, 1, 2], [5, 4, 3]], mat=2)
    # eyes
    for s in (-1, 1):
        v, f, uv = uv_sphere(1.0, 12, 6, center=(length * 0.075, s * length * 0.032, length * 0.018),
                             scale=(0.0065, 0.004, 0.0065))
        mb.add(v, f, uv, mat=1)
    return mb


def build_fish(coll, mats, basket_c, dims):
    """Three mackerel lying in the basket, tails poking over the rim."""
    from .util import look_matrix
    hx, hy, height = dims
    bz = basket_c[2]
    spots = [  # head position (rel. basket centre), body direction, lateral hint
        ((0.075, -0.095, 0.030), (-0.30, 0.62, 0.72), (0.0, 0.0, 1.0)),
        ((-0.070, 0.105, 0.040), (0.42, -0.58, 0.62), (0.3, 0.2, 1.0)),
        ((0.085, 0.060, 0.022), (-0.88, -0.35, 0.22), (0.0, 0.1, 1.0)),
    ]
    fishes = []
    for i, (p, d, lat) in enumerate(spots):
        mb = fish_mesh(0.25 + 0.015 * i)
        ob = mb.build(f"Fish{i}", coll, mats=mats)
        d = np.array(d) / np.linalg.norm(d)
        # local Y (lateral) roughly vertical => the fish lies on its side
        M = look_matrix(basket_c + np.array(p), d, np.cross(d, np.array(lat)))
        ob.matrix_world = Matrix(M.tolist())
        fishes.append(ob)
    return fishes


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def build(coll):
    """Builds the full bicycle. Returns a dict of key objects and points."""
    paint = bm.paint()
    chrome = bm.chrome()
    alu = bm.brushed_alu()
    tire = bm.tire()
    rubber = bm.rubber()
    leather = bm.leather()
    cork = bm.cork()
    steel = bm.chain_steel()
    gold = bm.gold()
    cream = bm.cream()
    wick = bm.wicker()
    glass = bm.lamp_glass()
    emit = bm.lamp_emit()
    refl = bm.reflector()
    copper = bm.gold("Copper")
    copper.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.85, 0.42, 0.25, 1)
    fish_mats = [bm.fish_skin(), bm.fish_eye(), bm.fish_fin()]
    spoke_mat = bm.chrome("SpokeSteel", rough=0.15)

    root = empty("BikeRoot", coll, size=0.3, kind='ARROWS')
    lean = empty("BikeLean", coll, parent=root, size=0.2)
    frame = build_frame(coll, [paint, chrome, gold, cream])
    frame.parent = lean
    saddle, saddle_top = build_saddle(coll, [leather, chrome, copper])
    saddle.parent = frame

    rw_pivot = empty("RearWheelSpin", coll, loc=tuple(A_R), parent=frame, size=0.05)
    rw = build_wheel("RearWheel", coll, [chrome, alu, tire, spoke_mat], rear=True)
    rw.parent = rw_pivot
    cog_pivot = empty("CogSpin", coll, loc=tuple(A_R), parent=frame, size=0.03)
    cog = build_cog("Cog", coll, [steel])
    cog.parent = cog_pivot

    crank_pivot = empty("CrankSpin", coll, loc=tuple(BB), parent=frame, size=0.05)
    cs = build_crankset(coll, [steel, chrome])
    cs.parent = crank_pivot
    pedals = {}
    for side, name in ((-1, 'R'), (1, 'L')):
        x = CRANK if side < 0 else -CRANK
        pp = empty(f"PedalSpin.{name}", coll, loc=(x, side * 0.064, 0), parent=crank_pivot, size=0.03)
        pd = build_pedal(f"Pedal.{name}", coll, [chrome, rubber], side)
        pd.parent = pp
        pedals[name] = pp

    # chain
    protos = collection("ChainProtos", coll)
    ci, co = build_chain_links(protos, steel)
    path = chain_path_points()
    seglen = np.linalg.norm(np.diff(np.vstack([path, path[:1]]), axis=0), axis=1).sum()
    nlinks = int(round(seglen / PITCH))
    nlinks += nlinks % 2
    pitch_eff = seglen / nlinks
    cu = bpy.data.curves.new("ChainPath", 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY')
    sp.points.add(len(path) - 1)
    sp.points.foreach_set("co", np.hstack([path, np.ones((len(path), 1))]).ravel().astype(np.float32))
    sp.use_cyclic_u = True
    chain = bpy.data.objects.new("Chain", cu)
    coll.objects.link(chain)
    chain.parent = frame
    ng, off_id = chain_geonodes(protos, nlinks, pitch_eff)
    mod = chain.modifiers.new("Links", 'NODES')
    mod.node_group = ng

    # steering assembly
    steer = empty("Steer", coll, loc=tuple(HT_BOT), parent=frame, size=0.08, kind='SINGLE_ARROW')
    steer.rotation_euler = (0, -(math.pi / 2 - HEAD_ANGLE), 0)
    bpy.context.view_layer.update()
    steer_inv = steer.matrix_world.inverted()

    def to_steer(ob):
        ob.parent = steer
        ob.matrix_parent_inverse = steer_inv

    fork = build_fork(coll, [paint, chrome, gold])
    to_steer(fork)
    cockpit, grips, bell_pos = build_cockpit(coll, [chrome, cork, rubber, paint])
    to_steer(cockpit)
    rear_f, front_f = build_fenders(coll, [paint, chrome, refl], [paint, chrome, cream])
    rear_f.parent = frame
    to_steer(front_f)
    brf, brr = build_brakes(coll, [chrome, rubber], grips)
    to_steer(brf)
    brr.parent = frame
    basket, bc, dims = build_basket(coll, [wick, leather, chrome])
    to_steer(basket)
    lamp = build_headlamp(coll, [chrome, glass, emit],
                          bc + np.array([dims[0] + 0.022, 0.0, 0.07]))
    to_steer(lamp)
    fishes = build_fish(coll, fish_mats, bc, dims)
    for f in fishes:
        to_steer(f)
    fw_pivot = empty("FrontWheelSpin", coll, size=0.05)
    fw_pivot.location = tuple(A_F)
    to_steer(fw_pivot)
    fw = build_wheel("FrontWheel", coll, [chrome, alu, tire, spoke_mat], rear=False)
    fw.parent = fw_pivot

    return dict(root=root, lean=lean, frame=frame, steer=steer, crank=crank_pivot,
                pedals=pedals, rear_spin=rw_pivot, front_spin=fw_pivot, cog=cog_pivot,
                chain=chain, chain_socket=off_id, saddle_top=saddle_top, grips=grips,
                bell=bell_pos, basket=basket, protos=protos, fishes=fishes)
