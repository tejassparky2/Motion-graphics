"""The "forest erase" effect: the puff-shrimp snaps and a stand of trees vanishes into dust, leaving stumps.

    trees = [paintbg.tree(loc, ...) for loc in spots]  # (trunk, canopy) pairs; grove() makes a stand
    fx = erase_trees(trees, origin=claw_xyz, f0=1, cam=cam)

A streak of light (white core, pale-yellow soft edges) shoots from `origin` along the blast direction, a short white
flash pops for 2 frames, and a flat shockwave ring races out along the ground. As the ring reaches each tree (nearest
first), the tree squashes and shakes for 2 frames, then pops into a few painted dust puffs and leaf bits that fly
outward and shrink away, leaving a stump with a pale cut top and splinters; a wisp curls up off the stump.

Timing: the burst (streak, flash, ring, the pop and the first 4 frames of each cloud) is on 1s; the debris settling
(drifting puffs, falling leaves, stump wisps) is on 2s. Look: mk/paintbg.py (paint3, tree), no outlines. Everything is
deterministic (seeded RNG)."""
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

from . import anim, look, paintbg

DUST = ("#d8c5ad", "#f2e5cf", "#fffaf0")         # painted dust: warm shadow, cream, near-white where lit
STUMP = ("#4a2f22", "#6e4a33", "#9c7a58")
CUT_WOOD = ("#c9a274", "#e6c595", "#f6dfb5")
BURST = 4                                        # frames on 1s after each pop, then the debris goes on 2s


def _paint(name, cols, noise=0.18):
    return paintbg.paint3(name, *(look.hexc(c) for c in cols), noise=noise)


def _key_alpha(m, keys):
    mix = m.node_tree.nodes["Mix"]
    for fr, a in keys:
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)


def _twos_from(idblock, frame):
    """Hold every pose for 2 frames from `frame` on (the burst before it stays on 1s)."""
    ad = idblock.animation_data
    if not (ad and ad.action):
        return
    for fc in anim.all_fcurves(ad.action):
        mod = fc.modifiers.new("STEPPED")
        mod.frame_step = 2
        mod.frame_offset = frame
        mod.use_frame_start = True
        mod.frame_start = frame


def _empty(name, loc):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.3
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    return e


def _parent(o, p):
    bpy.context.view_layer.update()
    o.parent = p
    o.matrix_parent_inverse = p.matrix_world.inverted()


def _sphere(name, loc, r, mat, seg=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def grove(n=7, x=(-5.0, 5.0), y=(5.0, 11.5), seed=11, avoid=((0.0, 0.6), (4.8, 4.2))):
    """A stand of painted cauliflower trees to erase: a list of paintbg.tree() (trunk, canopy) pairs. `avoid` =
    (centre, half-axes) of an ellipse kept clear (the crater)."""
    rnd = random.Random(seed)
    trees, spots, tries = [], [], 0
    while len(trees) < n and tries < 4000:
        tries += 1
        px, py = rnd.uniform(*x), rnd.uniform(*y)
        h, r = rnd.uniform(4.6, 6.0), rnd.uniform(1.7, 2.3)
        if avoid and ((px - avoid[0][0]) / avoid[1][0]) ** 2 + ((py - avoid[0][1]) / avoid[1][1]) ** 2 < 1:
            continue
        if any(math.hypot(px - q[0], py - q[1]) < 0.8 * (r + q[2]) for q in spots):
            continue
        spots.append((px, py, r))
        trees.append(paintbg.tree((px, py, 0.0), height=h, radius=r, seed=500 + len(trees), variant=rnd.randrange(4)))
    return trees


def _as_tree(t, i):
    """One tree (a paintbg.tree() pair, a list of objects with the trunk first, or one mesh object) -> a dict with a
    root empty at its base (for squash and shake) and its size, crown and materials measured from its bounds."""
    parts = list(t) if isinstance(t, (list, tuple)) else [t]
    bpy.context.view_layer.update()

    def bounds(objs):
        pts = [p.matrix_world @ Vector(c) for p in objs for c in p.bound_box]
        return [Vector([f(v[k] for v in pts) for k in range(3)]) for f in (min, max)]
    lo, hi = bounds(parts)
    base = ((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z)
    root = _empty(f"etree{i}", base)
    for p in parts:
        _parent(p, root)
    mats = [s.material.name for p in parts for s in p.material_slots if s.material]
    if len(parts) > 1:                                         # trunk first, canopy last (paintbg.tree)
        tlo, thi = bounds(parts[:1])
        clo, chi = bounds(parts[-1:])
        trunk_r = max(thi.x - tlo.x, thi.y - tlo.y) / 2
        crown_r = max(chi.x - clo.x, chi.y - clo.y) / 2 / 1.2   # the clumps stick out ~20 % past the core
        crown = ((clo.x + chi.x) / 2, (clo.y + chi.y) / 2, clo.z + (chi.z - clo.z) * 0.42)
    else:
        w = max(hi.x - lo.x, hi.y - lo.y)
        trunk_r, crown_r = w * 0.08, w / 2.4
        crown = (base[0], base[1], lo.z + (hi.z - lo.z) * 0.65)
    return dict(root=root, parts=parts, base=base, crown=crown, crown_r=crown_r, trunk_r=trunk_r,
                leaf=mats[-1] if mats else None, wood=mats[0] if mats else None)


def _stump(name, base, r, h, rnd):
    """A short trunk with a pale cut top and a few splinters (erase_trees() keys it to appear when its tree pops)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=r * 1.1, radius2=r, depth=h,
                          matrix=Matrix.Translation((0, 0, h / 2)))
    n_body = len(bm.faces)
    for k in range(3):
        a = rnd.uniform(0, 2 * math.pi)
        sh = rnd.uniform(0.4, 0.75) * h
        m = Matrix.Translation((math.cos(a) * r * 0.65, math.sin(a) * r * 0.65, h + sh / 2)) @ \
            Matrix.Rotation(rnd.uniform(-0.25, 0.25), 4, "X")
        bmesh.ops.create_cone(bm, cap_ends=False, segments=5, radius1=r * 0.35, radius2=0.0, depth=sh, matrix=m)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = base
    o.data.materials.append(_paint("stump", STUMP))
    o.data.materials.append(_paint("stump_cut", CUT_WOOD, 0.1))
    for p in o.data.polygons:
        p.material_index = 1 if p.index < n_body and p.normal.z > 0.9 else 0
        p.use_smooth = p.material_index == 0
    return o


def erase_trees(trees, origin, f0, speed=None, seed=7, direction=None, ground=0.0, life=20, cam=None,
                stumps=None):
    """Erase `trees` with a blast from `origin` (x, y, z: the claw) at frame `f0`.

    trees     : paintbg.tree() (trunk, canopy) pairs, lists of objects (trunk first) or mesh objects, one per tree
    speed     : how fast the shockwave front travels, in metres per frame; each tree pops when it arrives. Default:
                the front reaches the farthest tree 14 frames after f0
    direction : blast direction for the light streak (default: from origin toward the trees' centre)
    life      : frames the debris takes to settle and shrink away after a tree pops
    cam       : if given, a 2-frame white flash in front of this camera at f0, and the streak faces it
    stumps    : optional objects, one per tree (e.g. a set's own "after" stumps), revealed when their tree pops
                instead of the built-in stumps
    Returns dict(order, pop_frames, puffs, bits, stumps, ring, streak, flash, speed, end) with `end` the last
    animated frame."""
    rnd = random.Random(seed)
    ox, oy, oz = origin
    trees = [_as_tree(t, i) for i, t in enumerate(trees)]
    dist = [math.hypot(t["base"][0] - ox, t["base"][1] - oy) for t in trees]
    order = sorted(range(len(trees)), key=lambda i: dist[i])
    speed = speed or max(max(dist) / 14.0, 0.1)
    if direction is None:
        direction = (sum(t["base"][0] for t in trees) / len(trees) - ox,
                     sum(t["base"][1] for t in trees) / len(trees) - oy)
    dl = math.hypot(*direction[:2]) or 1.0
    dirx, diry = direction[0] / dl, direction[1] / dl
    reach = max(dist) + 3.0

    streak = _streak(origin, (dirx, diry), reach + 4.0, f0, cam)
    ring = _ring((ox, oy, ground), f0, speed, reach)
    flash = _flash(cam, f0) if cam else None

    puffs, bits, left, pops = [], [], [], {}
    for i in order:
        t = trees[i]
        tp = f0 + max(2, round(dist[i] / speed))
        pops[i] = tp
        _pop(t, tp, rnd)
        st = stumps[i] if stumps else _stump(f"stump{i}", t["base"], t["trunk_r"],
                                             t["crown_r"] * rnd.uniform(0.2, 0.28), rnd)
        st.scale = (1, 1, 1)
        anim.key(st, "scale", f0 - 1, 0.0, "CONSTANT")
        anim.key(st, "scale", tp, 1.0, "CONSTANT")
        left.append(st)
        puffs += _cloud(t, tp, (ox, oy), rnd, life, f"{i}")
        bits += _leaf_bits(t, tp, (ox, oy), rnd, life, ground, f"{i}")
        puffs += _wisps(t, tp, rnd, life, f"{i}")
    end = max(pops.values()) + life + 10                                         # the stump wisps go last
    return dict(order=order, pop_frames=[pops[i] for i in range(len(trees))], puffs=puffs, bits=bits, stumps=left,
                ring=ring, streak=streak, flash=flash, speed=speed, end=end)


def _pop(t, tp, rnd):
    """Rest, then 2 frames of squash and shake on 1s, then gone."""
    root = t["root"]
    bx, by, bz = root.location
    jx, jy = rnd.choice((-1, 1)) * 0.15, rnd.uniform(-0.08, 0.08)
    anim.key(root, "scale", tp - 3, (1, 1, 1), "CONSTANT")
    anim.key(root, "location", tp - 3, (bx, by, bz), "CONSTANT")
    anim.key(root, "scale", tp - 2, (1.12, 1.12, 0.86), "CONSTANT")
    anim.key(root, "location", tp - 2, (bx + jx, by + jy, bz), "CONSTANT")
    anim.key(root, "scale", tp - 1, (1.24, 1.24, 0.72), "CONSTANT")
    anim.key(root, "location", tp - 1, (bx - jx, by - jy, bz), "CONSTANT")
    anim.key(root, "scale", tp, (0, 0, 0), "CONSTANT")
    anim.key(root, "location", tp, (bx, by, bz), "CONSTANT")


def _away(p, origin, rnd, spread=0.6):
    """A unit horizontal direction pointing away from the blast origin, with some scatter."""
    a = math.atan2(p[1] - origin[1], p[0] - origin[0]) + rnd.uniform(-spread, spread)
    return math.cos(a), math.sin(a)


def _cloud(t, tp, origin, rnd, life, tag, n=5):
    """The canopy bursts into a few painted puffs (on 1s), which then drift up and away and shrink (on 2s)."""
    m = _paint("erase_dust", DUST)
    cx, cy, cz = t["crown"]
    cr, out = t["crown_r"], []
    for k in range(n):
        if k == 0:
            off = (0.0, 0.0, 0.0)
        else:
            a = k / (n - 1) * 2 * math.pi + rnd.uniform(-0.4, 0.4)
            off = (math.cos(a) * cr * 0.55, math.sin(a) * cr * 0.5, rnd.uniform(-0.3, 0.4) * cr)
        p0 = (cx + off[0], cy + off[1], cz + off[2])
        ux, uy = _away(p0, origin, rnd, 0.9)
        r = cr * (0.5 if k == 0 else rnd.uniform(0.3, 0.42))
        d = _sphere(f"puff{tag}_{k}", p0, 1.0, m)
        drift = cr * rnd.uniform(0.6, 1.1)
        rise = cr * rnd.uniform(0.5, 1.0)
        anim.key(d, "scale", tp - 1, 0.0, "CONSTANT")
        anim.key(d, "location", tp - 1, p0, "CONSTANT")
        for j, (sc, mv) in enumerate(((0.55, 0.0), (1.05, 0.3), (1.15, 0.45), (1.1, 0.55))):   # burst on 1s
            anim.key(d, "scale", tp + j, r * sc, "LINEAR")
            anim.key(d, "location", tp + j, (p0[0] + ux * drift * mv, p0[1] + uy * drift * mv,
                                             p0[2] + rise * mv * 0.5), "LINEAR")
        anim.key(d, "scale", tp + life * 0.4, r * 0.95)                                        # then drift and shrink
        anim.key(d, "scale", tp + life, 0.0)
        anim.key(d, "location", tp + life, (p0[0] + ux * drift * 1.2, p0[1] + uy * drift * 1.2, p0[2] + rise * 1.4))
        _twos_from(d, tp + BURST)
        out.append(d)
    return out


def _leaf_bits(t, tp, origin, rnd, life, ground, tag, n=10):
    """Chunky leaf clumps (and a few wood chips) thrown outward, tumbling, falling and shrinking away."""
    leaf = bpy.data.materials.get(t["leaf"] or "") or _paint("erase_leaf", ("#1f6b3a", "#36a64a", "#9ee05a"))
    wood = bpy.data.materials.get(t.get("wood") or "") or _paint("stump", STUMP)
    cx, cy, cz = t["crown"]
    cr, out = t["crown_r"], []
    for k in range(n):
        p0 = (cx + rnd.uniform(-0.5, 0.5) * cr, cy + rnd.uniform(-0.5, 0.5) * cr, cz + rnd.uniform(-0.3, 0.4) * cr)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=p0)
        b = bpy.context.object
        b.name = f"leafbit{tag}_{k}"
        b.data.materials.append(wood if k % 4 == 3 else leaf)
        sz = cr * rnd.uniform(0.09, 0.15)
        shape = (sz, sz * 0.45, sz * 0.8)
        ux, uy = _away(p0, origin, rnd, 1.0)
        v = rnd.uniform(0.18, 0.34) * cr                       # metres per frame
        vz, g = rnd.uniform(0.15, 0.3) * cr, 0.03 * cr
        spin = [rnd.uniform(-0.6, 0.6) for _ in range(3)]
        anim.key(b, "scale", tp - 1, 0.0, "CONSTANT")
        landed = None
        for fr in list(range(tp, tp + BURST)) + list(range(tp + BURST, tp + life + 1, 2)):
            s = fr - tp
            z = p0[2] + vz * s - 0.5 * g * s * s
            if landed is None and z <= ground + sz * 0.4:
                landed = s
            se = s if landed is None else landed
            if landed is not None:
                z = ground + sz * 0.4
            anim.key(b, "location", fr, (p0[0] + ux * v * se, p0[1] + uy * v * se, z), "LINEAR")
            anim.key(b, "rotation_euler", fr, [w * se for w in spin], "LINEAR")
            fade = 1.0 if s < life * 0.6 else max(0.0, 1 - (s - life * 0.6) / (life * 0.4))
            anim.key(b, "scale", fr, tuple(c * fade for c in shape), "LINEAR")
        _twos_from(b, tp + BURST)
        out.append(b)
    return out


def _wisps(t, tp, rnd, life, tag, n=2):
    """Small puffs curling up off the fresh stump while the debris settles (on 2s)."""
    m = _paint("erase_dust", DUST)
    bx, by, bz = t["base"]
    out = []
    for k in range(n):
        f1 = tp + BURST + 2 + k * 4
        p0 = (bx + rnd.uniform(-0.15, 0.15), by + rnd.uniform(-0.15, 0.15), bz + t["crown_r"] * 0.3)
        d = _sphere(f"wisp{tag}_{k}", p0, 1.0, m, 10)
        r = t["trunk_r"] * rnd.uniform(0.75, 1.05)
        top = (p0[0] + rnd.uniform(-0.4, 0.4), p0[1] + rnd.uniform(-0.4, 0.4), p0[2] + rnd.uniform(1.8, 2.6))
        anim.key(d, "scale", f1 - 1, 0.0, "CONSTANT")
        anim.key(d, "location", f1 - 1, p0, "CONSTANT")
        anim.key(d, "scale", f1, r * 0.5)
        anim.key(d, "scale", f1 + 8, r)
        anim.key(d, "scale", tp + life + 10, 0.0)
        anim.key(d, "location", f1, p0)
        anim.key(d, "location", f1 + 8, tuple(a + (b - a) * 0.5 for a, b in zip(p0, top)))
        anim.key(d, "location", tp + life + 10, top)
        _twos_from(d, f1)
        out.append(d)
    return out


def _annulus(name, center, r0, r1, w0, w1, seg=128):
    """A flat ring of radius r0 and width w0, with a shape key 'grow' that takes it to radius r1 and width w1
    (scaling would fatten the band as it grows)."""
    verts, faces = [], []
    for i in range(seg):
        a = i / seg * 2 * math.pi
        c, s = math.cos(a), math.sin(a)
        verts += [(c * (r0 - w0 / 2), s * (r0 - w0 / 2), 0), (c * (r0 + w0 / 2), s * (r0 + w0 / 2), 0)]
        j, k = 2 * i, 2 * ((i + 1) % seg)
        faces.append((j, j + 1, k + 1, k))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = center
    o.shape_key_add(name="basis")
    kb = o.shape_key_add(name="grow")
    for i in range(seg):
        a = i / seg * 2 * math.pi
        c, s = math.cos(a), math.sin(a)
        kb.data[2 * i].co = (c * (r1 - w1 / 2), s * (r1 - w1 / 2), 0)
        kb.data[2 * i + 1].co = (c * (r1 + w1 / 2), s * (r1 + w1 / 2), 0)
    return o, kb


def _ring(center, f0, speed, reach):
    """A flat white shockwave ring on the ground that keeps pace with the erase front (radius = speed * frames),
    with a thinner, fainter echo just behind it. On 1s."""
    out = []
    for name, w0, w1, a_max, lag in (("erase_ring", 0.4, 0.22, 1.0, 0.0), ("erase_ring_echo", 0.14, 0.08, 0.6, 1.2)):
        r0 = 0.3
        o, kb = _annulus(name, (center[0], center[1], center[2] + 0.07), r0, reach, w0, w1)
        m = look.fade(f"{name}_m", look.hexc("#ffffff"), 0.0)
        o.data.materials.append(m)
        f_end = f0 + math.ceil((reach + lag) / speed)
        kb.value = 0.0
        kb.keyframe_insert("value", frame=f0 - 1)
        for fr in range(f0, f_end + 1):
            kb.value = (max(r0, (fr - f0) * speed - lag) - r0) / (reach - r0)
            kb.keyframe_insert("value", frame=fr)
        hold = f0 + round((f_end - f0) * 0.55)
        _key_alpha(m, ((f0 - 1, 0.0), (f0, a_max), (hold, a_max), (f_end, 0.0)))
        out.append(o)
    return out


def beam_mat(name="erase_beam"):
    """Soft glowing beam: white along the core, pale yellow toward the edges, alpha falling off to the edges
    (from the mesh's UV v: 1 on the centre line, 0 at the edges). Key node 'Alpha' input 1 to fade it."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    uv = nt.nodes.new("ShaderNodeUVMap")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    core = nt.nodes.new("ShaderNodeMath")
    core.operation = "POWER"
    core.inputs[1].default_value = 4.0
    col = nt.nodes.new("ShaderNodeMix")
    col.data_type = "RGBA"
    col.inputs[6].default_value = look.hexc("#ffe98a")
    col.inputs[7].default_value = (1, 1, 1, 1)
    soft = nt.nodes.new("ShaderNodeMath")
    soft.operation = "POWER"
    soft.inputs[1].default_value = 1.4
    alpha = nt.nodes.new("ShaderNodeMath")
    alpha.name = "Alpha"
    alpha.operation = "MULTIPLY"
    alpha.inputs[1].default_value = 0.0
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(uv.outputs["UV"], sep.inputs[0])
    L(sep.outputs["Y"], core.inputs[0])
    L(core.outputs[0], col.inputs["Factor"])
    L(col.outputs[2], em.inputs[0])
    L(sep.outputs["Y"], soft.inputs[0])
    L(soft.outputs[0], alpha.inputs[0])
    L(alpha.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def _ribbon(name, length, width):
    """A tapered strip along +X (widest just past the start, a long point at the far end), UV v = 1 on the centre
    line and 0 at the edges."""
    stations = (0.0, 0.025, 0.06, 0.2, 0.4, 0.6, 0.8, 1.0)
    verts, faces, vs = [], [], []
    for u in stations:
        w = width * (u / 0.06 if u < 0.06 else (1 - u) / 0.94 * 0.85 + 0.15 * (1 - u))
        verts += [(u * length, -w, 0), (u * length, 0, 0), (u * length, w, 0)]
        vs += [0.0, 1.0, 0.0]
    for i in range(len(stations) - 1):
        j = 3 * i
        faces += [(j, j + 3, j + 4, j + 1), (j + 1, j + 4, j + 5, j + 2)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            vi = me.loops[li].vertex_index
            uvl.data[li].uv = (verts[vi][0] / length, vs[vi])
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def _streak(origin, d, length, f0, cam=None):
    """A glowing blade of light from the claw along the blast direction: shoots out in 2 frames, then thins and fades
    (on 1s). With `cam` it turns about its length to face the camera; without, two crossed ribbons."""
    m = beam_mat()
    a = m.node_tree.nodes["Alpha"]
    for fr, v in ((f0 - 1, 0.0), (f0, 1.0), (f0 + 3, 1.0), (f0 + 7, 0.0)):
        a.inputs[1].default_value = v
        a.inputs[1].keyframe_insert("default_value", frame=fr)
    out = []
    for k, roll in enumerate((0.0,) if cam else (0.0, math.pi / 2)):
        o = _ribbon(f"erase_streak{k}", length, 0.9)
        o.data.materials.append(m)
        o.location = origin
        o.rotation_euler = (roll, 0, math.atan2(d[1], d[0]))
        if cam:
            c = o.constraints.new("LOCKED_TRACK")
            c.target = cam
            c.lock_axis, c.track_axis = "LOCK_X", "TRACK_Z"
        anim.key(o, "scale", f0 - 1, (0.0, 0.0, 0.0), "CONSTANT")
        anim.key(o, "scale", f0, (0.55, 1.3, 1.3), "LINEAR")
        anim.key(o, "scale", f0 + 1, (1.0, 1.0, 1.0), "LINEAR")
        anim.key(o, "scale", f0 + 3, (1.04, 0.55, 0.55), "LINEAR")
        anim.key(o, "scale", f0 + 7, (1.08, 0.0, 0.0), "LINEAR")
        out.append(o)
    return out


def _flash(cam, f0):
    """A short white flash: a plane just in front of the camera, strong on the snap frame, half on the next, gone."""
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    p = bpy.context.object
    p.name = "erase_flash"
    p.parent = cam
    p.location = (0, 0, -0.2)
    p.scale = (0.6, 0.6, 1)
    m = look.fade("erase_flash_m", look.hexc("#ffffff"), 0.0)
    p.data.materials.append(m)
    _key_alpha(m, ((f0 - 1, 0.0), (f0, 0.8), (f0 + 1, 0.35), (f0 + 2, 0.0)))
    for fc in anim.all_fcurves(m.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return p
