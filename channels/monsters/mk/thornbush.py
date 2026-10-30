"""The butcher bird's thorn bush (Episode 1 v2, S22-S24): a wiry thorn bush beside the meadow puddle, about 6 creature
units (1.2 m) tall, its thorns hung with the bird's larder: tiny empty snail shells and beetle shells skewered on the
thorns (shells only, nothing gory). Near the top, one big thorn is empty and shrimp-sized.

Painted background look (paintbg): no outlines, three painted bands; the shells are the focal props and get thin
coloured lines.

    h = build(loc=BUSH_AT)  ->  dict(root, perch=(x, y, z), empty_thorn=(base, tip), shells=[objs], shell_spots=[...])
    perch       : the top of the leader, where the bird lands (feet at this point)
    empty_thorn : world base and tip of the big empty thorn (for the insert)
The bush is built facing -Y (the meadow cameras look along +Y), at BUSH_AT beside the puddle unless told otherwise.
"""
import math
import random

import bpy
import numpy as np
from mathutils import Vector

from . import look, paintbg
from .tuftwing import _catmull, _line

BUSH_AT = (-2.5, -0.5, 0.0)            # left of the puddle (centre (0.1, -1.25)); the puff-shrimp drinks on its right

PERCH_CLEAR = (0.08, 0.0, 7.1)        # (bush space) where the perched bird's body sits: no thorns through it
# The leader runs up to the perch; branches leave it at these heights (height, azimuth, length, rise).
LEADER = [(0, 0, 0), (0.06, 0.0, 1.0), (0.14, 0.05, 2.0), (0.06, 0.0, 3.2), (-0.08, -0.04, 4.4), (0.0, 0.0, 5.4),
          (0.08, 0.0, 6.0)]
BRANCHES = [(0.6, 2.4, 1.5, 0.6), (0.9, -0.3, 1.7, 0.9), (1.3, 1.6, 1.4, 0.8), (1.6, -1.9, 1.8, 1.0),
            (2.0, 3.4, 1.6, 1.0), (2.4, 0.5, 1.9, 1.2), (2.7, -2.8, 1.5, 1.0), (3.1, 2.1, 1.6, 1.1),
            (3.5, -0.9, 1.6, 1.2), (3.9, -2.2, 1.3, 1.0), (4.2, 1.2, 1.4, 0.8), (4.6, 2.8, 1.1, 0.5),
            (4.9, 0.2, 1.1, 0.4)]


def _tube(name, pts, r0, r1, mat):
    """A tapered woody stem through pts (radius r0 at the base, r1 at the tip)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 1.0
    cu.bevel_resolution = 3
    cu.resolution_u = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for i, (bp, p) in enumerate(zip(sp.bezier_points, pts)):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
        bp.radius = r0 + (r1 - r0) * i / (len(pts) - 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for s in bpy.context.selected_objects:
        s.select_set(False)
    o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.object
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _thorn(name, base, direction, length, r, mat):
    """A straight thorn: a sharp cone from `base` along `direction`."""
    d = np.asarray(direction, float)
    d /= np.linalg.norm(d)
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=r, radius2=0.0, depth=length,
                                    location=tuple(np.asarray(base) + d * length / 2))
    o = bpy.context.object
    o.name = name
    o.rotation_mode = "QUATERNION"
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(d))
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _snail(name, center, rot, size, mat):
    """An empty snail shell: a tube coiling up a short spire in 2.5 turns and fattening into the round body whorl, so
    its coloured outline draws the spiral."""
    pts = []
    for t in np.linspace(0.0, 2.5, 30):
        rr = size * 0.06 * math.exp(0.7 * t)
        pts.append((rr * math.cos(2 * math.pi * t), rr * math.sin(2 * math.pi * t), size * 0.55 * (1 - t / 2.5)))
    o = _tube(name, pts, size * 0.03, size * 0.3, mat)
    c = np.mean([v.co[:] for v in o.data.vertices], axis=0)
    for v in o.data.vertices:
        v.co = tuple(np.asarray(v.co[:]) - c)
    o.location = center
    o.rotation_euler = rot
    return o


def _beetle(name, center, rot, size, mat, seam, gloss):
    """An empty beetle shell: two domed wing-cases with a dark seam, a smaller head plate in front, a gloss streak."""
    def dome(nm, loc, sc, m):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc)
        o = bpy.context.object
        o.name = nm
        o.scale = sc
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.data.materials.append(m)
        for p in o.data.polygons:
            p.use_smooth = True
        return o
    o = dome(name, (0, 0, 0), (size * 0.55, size, size * 0.5), mat)
    head = dome(f"{name}_head", (0, -size * 0.95, -size * 0.05), (size * 0.36, size * 0.3, size * 0.3), mat)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0.05 * size, size * 0.49))
    sm = bpy.context.object
    sm.scale = (size * 0.025, size * 0.9, size * 0.02)
    sm.data.materials.append(seam)
    hl = dome(f"{name}_gloss", (-size * 0.22, -size * 0.2, size * 0.42), (size * 0.06, size * 0.32, size * 0.04), gloss)
    for c in (head, sm, hl):
        c.parent = o
    _line(head, 0.008)
    o.location = center
    o.rotation_euler = rot
    return o


def build(loc=BUSH_AT, seed=8):
    rnd = random.Random(seed)
    hx = look.hexc
    bark = paintbg.paint3("thorn_bark", hx("#3a2a2c"), hx("#5a4038"), hx("#7c5d4c"), noise=0.12, scale=6.0)
    thorn_m = paintbg.paint3("thorn", hx("#8a6a52"), hx("#c4a27e"), hx("#ecd6b2"), noise=0.05)
    bone = paintbg.paint3("thorn_big", hx("#6e5a4c"), hx("#b39a80"), hx("#efe2c8"), noise=0.04)
    leaf = paintbg.paint3("thorn_leaf", *paintbg.greens(2), noise=0.12)
    shell_ms = [look.toon("shell_cream", hx("#f3dcae")), look.toon("shell_peach", hx("#eeb48e")),
                look.toon("shell_lemon", hx("#f6e27a"))]
    beetle_ms = [look.toon("beetle_green", hx("#2f9e6e"), gloss=True), look.toon("beetle_blue", hx("#3d63c8"),
                                                                                  gloss=True)]
    seam = look.flat("beetle_seam", hx("#1b1830"))
    gloss = look.flat("beetle_gloss", hx("#e9fff6"))

    root = bpy.data.objects.new("thornbush", None)
    bpy.context.scene.collection.objects.link(root)
    parts = [_tube("bush_leader", LEADER, 0.2, 0.05, bark)]
    stems = [(_catmull(np.asarray(LEADER, float), 60), 0.2, 0.05)]
    for i, (h, az, ln, rise) in enumerate(BRANCHES):
        k = min(range(len(LEADER)), key=lambda j: abs(LEADER[j][2] - h))
        p0 = np.array((LEADER[k][0], LEADER[k][1], h))
        out = np.array((math.cos(az), math.sin(az), 0.0))
        pts = [p0, p0 + out * ln * 0.35 + (0, 0, rise * 0.3), p0 + out * ln * 0.7 + (0, 0, rise * 0.7),
               p0 + out * ln + (rnd.uniform(-0.1, 0.1), rnd.uniform(-0.1, 0.1), rise)]
        r0 = 0.09 - 0.007 * i
        parts.append(_tube(f"bush_branch{i}", [tuple(p) for p in pts], r0, 0.02, bark))
        stems.append((_catmull(np.asarray(pts, float), 30), r0, 0.02))
        tip = pts[-1]
        if h > 3.0:                                            # leafless up top: the bare thorns hold the perch
            continue
        for j in range(2):                                     # a few small leaves low down
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(
                tip[0] + rnd.uniform(-0.15, 0.15), tip[1] + rnd.uniform(-0.15, 0.15), tip[2] + rnd.uniform(-0.05, 0.1)))
            lf = bpy.context.object
            s = rnd.uniform(0.1, 0.15)
            lf.scale = (s, s * 0.8, s * 0.55)
            lf.data.materials.append(leaf)
            for pg in lf.data.polygons:
                pg.use_smooth = True
            parts.append(lf)
    # thorns all along every stem, alternating sides, pointing out and a little up
    thorns = []
    for si, (P, r0, r1) in enumerate(stems):
        T = np.gradient(P, axis=0)
        T /= np.linalg.norm(T, axis=1)[:, None]
        n = len(P)
        for i in range(2, n - 2, 3 if si == 0 else 2):
            t = T[i]
            side = np.cross(t, (0, 0, 1.0))
            if np.linalg.norm(side) < 1e-3:
                side = np.array((1.0, 0, 0))
            side /= np.linalg.norm(side)
            a = rnd.uniform(0, 2 * math.pi)
            d = side * math.cos(a) + np.cross(t, side) * math.sin(a) + t * 0.5 + (0, 0, 0.25)
            d /= np.linalg.norm(d)
            r = r0 + (r1 - r0) * i / (n - 1)
            base = P[i] + d * r * 0.6
            if np.linalg.norm(base + d * 0.5 - PERCH_CLEAR) < 1.35:        # keep the bird's seat clear
                continue
            larder = 1.0 < base[2] < 3.8 and d[1] < -0.2               # long thorns for the shells to hang on
            ln = rnd.uniform(0.6, 0.75) if larder else rnd.uniform(0.32, 0.52)
            o = _thorn(f"thorn{si}_{i}", base, d, ln, 0.045, thorn_m)
            parts.append(o)
            thorns.append((base, d, ln))
    # the larder: shells skewered on thorns at the shrimp's height and a little above, each pierced through so the
    # thorn's tip shows beyond it
    shells, spots = [], []
    cands = [t for t in thorns if 1.0 < t[0][2] < 3.8 and t[1][1] < -0.2]       # pointing toward the camera side
    rnd.shuffle(cands)
    for i, (base, d, ln) in enumerate(cands[:10]):
        c = tuple(base + d * ln * 0.5)
        if i % 3 == 2:                                         # beetles show their domed backs to the camera
            rot = (math.radians(rnd.uniform(70, 110)), rnd.uniform(-0.5, 0.5), rnd.uniform(-0.6, 0.6))
            o = _beetle(f"beetle{i}", c, rot, rnd.uniform(0.2, 0.26), beetle_ms[i % 2], seam, gloss)
        else:                                                  # snails show their spiral, spire tipped sideways
            rot = (math.radians(rnd.uniform(40, 80)), rnd.uniform(-0.8, 0.8), rnd.uniform(0, 6.3))
            o = _snail(f"snail{i}", c, rot, rnd.uniform(0.34, 0.44), shell_ms[i % 3])
        _line(o, 0.008)
        shells.append(o)
        spots.append(c)
    # the big empty thorn near the top, jutting out to the left into clear air: shrimp-sized, and nothing on it yet
    big_base = np.array((0.02, -0.08, 5.15))
    big_dir = np.array((-0.9, -0.35, 0.32))
    big_dir /= np.linalg.norm(big_dir)
    big = _thorn("thorn_empty", tuple(big_base), big_dir, 1.15, 0.1, bone)
    parts.append(big)
    for o in parts + shells:
        o.parent = root
    root.location = loc
    off = np.asarray(loc, float)
    return dict(root=root, perch=tuple(np.asarray(LEADER[-1]) + off), shells=shells,
                shell_spots=[tuple(np.asarray(s) + off) for s in spots],
                empty_thorn=(tuple(big_base + off), tuple(big_base + big_dir * 1.15 + off)))
