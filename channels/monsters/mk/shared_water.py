"""One water look for the whole spill sequence (S07 tank jet, S08 waterfall and spill, S08a puddle under the
sneakers, S08b electrified puddle): procedural, toon, readable at phone size, and lit by its own colours (unlit
emission like every lab glow), so the Q3 light pass and power_out() treat it like the rest of the lab.

    from channels.monsters.mk import shared_water as sw
    sw.adopt(R)                      # at the end of a lab builder: restyles R["puddle"]'s spill (and any object
                                     # using lab._water_floor()) and swaps its flat stream for falling_water()
    m = sw.spill_material()          # flat translucent cyan, bright rim (see rim()), drifting highlight streaks,
                                     # a faint reflection of the lab light
    sw.rim(obj)                      # the thin bright edge line under a puddle shape (unions read as one outline)
    sw.ripple_rings(obj_or_point, f0)                # rings for drops and footsteps, on 2s
    sw.falling_water(points, f0)     # a glassy ribbon with a white core and splash drops at its foot

Units are the diorama's (1 unit = 20 cm); `k` scales the small things (drops, rings) for other sets.
"""
import math
import random

import bpy
from mathutils import Vector

from . import anim, look

BODY = "#68d2e8"               # the water: light cyan, lighter than the teal floor tiles
DEEP = "#46b4d4"               # its gentle low-frequency tone
RIM = "#effeff"                # the edge line and the falling water's core
ALPHA = 0.84                   # slightly translucent


def _hex(c):
    return look.hexc(c)


def _loop(nt, sock, f0, v0, f1, v1):
    """Key a socket at two frames and extrapolate linearly: a slow drift that never stops."""
    sock.default_value = v0
    sock.keyframe_insert("default_value", frame=f0)
    sock.default_value = v1
    sock.keyframe_insert("default_value", frame=f1)
    path = sock.path_from_id("default_value")
    for fc in anim.all_fcurves(nt.animation_data.action):
        if fc.data_path == path:
            fc.extrapolation = "LINEAR"
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def spill_material(name="shared_spill", glint=None, glint_r=3.0, streak_scale=0.8):
    """The puddle: a flat, slightly translucent light-cyan body (world space, so overlapping discs read as one
    sheet), 2-3 soft white highlight streaks that drift slowly, and a faint reflection of the lab light: a soft
    lighter pool round `glint` (x, y) in world units (None: a broad soft brightening). Its Emission node carries the
    strength, so lab power_out()/dimming keys work on it as on lab._water_floor()."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    geo = N("ShaderNodeNewGeometry")
    # body: two close cyans, mixed by a very broad noise (no camo: one soft swell per few units)
    tone = N("ShaderNodeTexNoise")
    tone.inputs["Scale"].default_value = 0.12
    tone.inputs["Detail"].default_value = 0.0
    body = N("ShaderNodeMix")
    body.data_type = "RGBA"
    body.inputs[6].default_value = _hex(DEEP)
    body.inputs[7].default_value = _hex(BODY)
    tr = N("ShaderNodeMapRange")
    tr.inputs[1].default_value, tr.inputs[2].default_value = 0.35, 0.65
    tr.inputs[3].default_value, tr.inputs[4].default_value = 0.25, 1.0
    L(geo.outputs["Position"], tone.inputs["Vector"])
    L(tone.outputs["Fac"], tr.inputs[0])
    L(tr.outputs[0], body.inputs[0])
    # highlight streaks: long diagonal bands, thinned to soft lines, only where a broad mask lets them through (2-3
    # segments in a puddle), drifting along their length
    mp = N("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (0, 0, math.radians(35))
    L(geo.outputs["Position"], mp.inputs["Vector"])
    wave = N("ShaderNodeTexWave")
    wave.wave_type, wave.bands_direction = "BANDS", "Y"
    wave.inputs["Scale"].default_value = streak_scale
    wave.inputs["Distortion"].default_value = 1.2
    wave.inputs["Detail"].default_value = 0.0
    L(mp.outputs[0], wave.inputs["Vector"])
    thin = N("ShaderNodeValToRGB")
    thin.color_ramp.interpolation = "EASE"
    e0, e1 = thin.color_ramp.elements
    e0.position, e0.color = 0.83, (0, 0, 0, 1)
    e1.position, e1.color = 0.96, (1, 1, 1, 1)
    L(wave.outputs["Fac"], thin.inputs[0])
    mask = N("ShaderNodeTexNoise")
    mask.inputs["Scale"].default_value = streak_scale * 0.7
    mask.inputs["Detail"].default_value = 0.0
    mramp = N("ShaderNodeValToRGB")
    m0, m1 = mramp.color_ramp.elements
    m0.position, m0.color = 0.52, (0, 0, 0, 1)
    m1.position, m1.color = 0.62, (1, 1, 1, 1)
    L(mp.outputs[0], mask.inputs["Vector"])
    L(mask.outputs["Fac"], mramp.inputs[0])
    streak = N("ShaderNodeMath")
    streak.operation = "MULTIPLY"
    L(thin.outputs[0], streak.inputs[0])
    L(mramp.outputs[0], streak.inputs[1])
    st = N("ShaderNodeMath")
    st.operation = "MULTIPLY"
    st.inputs[1].default_value = 0.85
    L(streak.outputs[0], st.inputs[0])
    _loop(nt, mp.inputs["Location"], 0, (0, 0, 0), 100, (0.0, 1.2, 0))           # ~1 unit every 4 s
    # the lab light's reflection: a soft lighter pool
    if glint is not None:
        d = N("ShaderNodeVectorMath")
        d.operation = "DISTANCE"
        d.inputs[1].default_value = (glint[0], glint[1], 0.0)
        sep = N("ShaderNodeSeparateXYZ")
        comb = N("ShaderNodeCombineXYZ")
        L(geo.outputs["Position"], sep.inputs[0])
        L(sep.outputs[0], comb.inputs[0])
        L(sep.outputs[1], comb.inputs[1])
        L(comb.outputs[0], d.inputs[0])
        g = N("ShaderNodeMapRange")
        g.inputs[1].default_value, g.inputs[2].default_value = 0.0, glint_r
        g.inputs[3].default_value, g.inputs[4].default_value = 0.22, 0.0
        L(d.outputs["Value"], g.inputs[0])
        glow = g.outputs[0]
    else:
        gn = N("ShaderNodeTexNoise")
        gn.inputs["Scale"].default_value = 0.08
        gn.inputs["Detail"].default_value = 0.0
        g = N("ShaderNodeMapRange")
        g.inputs[1].default_value, g.inputs[2].default_value = 0.45, 0.7
        g.inputs[3].default_value, g.inputs[4].default_value = 0.0, 0.16
        L(geo.outputs["Position"], gn.inputs["Vector"])
        L(gn.outputs["Fac"], g.inputs[0])
        glow = g.outputs[0]
    lit = N("ShaderNodeMath")
    lit.operation = "ADD"
    L(st.outputs[0], lit.inputs[0])
    L(glow, lit.inputs[1])
    col = N("ShaderNodeMix")
    col.data_type = "RGBA"
    col.clamp_factor = True
    col.inputs[7].default_value = (1, 1, 1, 1)
    L(lit.outputs[0], col.inputs[0])
    L(body.outputs[2], col.inputs[6])
    em = N("ShaderNodeEmission")
    em.name = "Emission"
    em.inputs[1].default_value = 1.0
    L(col.outputs[2], em.inputs[0])
    tp = N("ShaderNodeBsdfTransparent")
    mix = N("ShaderNodeMixShader")
    mix.name = "Mix"
    mix.inputs[0].default_value = ALPHA
    L(tp.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    out = N("ShaderNodeOutputMaterial")
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def rim_material(name="shared_water_rim"):
    """The edge line: opaque, a touch brighter than the body's highlights."""
    m = look.flat(name, _hex(RIM), 1.25)
    return m


def rim(obj, width=0.06, drop=0.002):
    """A thin bright edge line round a flat puddle shape: a copy of `obj` a little bigger and just under it, as its
    child (it follows obj's animated scale). For a puddle made of overlapping discs, call it on each disc: the
    bigger copies only show round the union, so the whole puddle gets one outline. `width` = the line width as a
    fraction of the shape."""
    r = obj.copy()
    r.data = obj.data.copy()
    r.name = f"{obj.name}_rim"
    r.data.materials.clear()
    r.data.materials.append(rim_material())
    for c in obj.users_collection:
        c.objects.link(r)
    r.animation_data_clear()
    r.parent = obj
    r.matrix_parent_inverse.identity()
    r.location = (0, 0, -drop)
    r.rotation_euler = (0, 0, 0)
    r.scale = (1 + width, 1 + width, 1)
    r.visible_shadow = False
    return r


def _ring_mesh(name, r_in=0.86, segs=32):
    verts, faces = [], []
    for i in range(segs):
        a = i / segs * 2 * math.pi
        verts += [(math.cos(a), math.sin(a), 0), (math.cos(a) * r_in, math.sin(a) * r_in, 0)]
    for i in range(segs):
        j = (i + 1) % segs
        faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    return me


def ripple_rings(where, f0, n=2, every=4, radius=0.45, frames=8, k=1.0, color=RIM, name=None):
    """Rings for a drop or a footstep: `n` thin rings born `every` frames apart from f0 at `where` (a point, or an
    object: its world position), each spreading to `radius` x k over `frames` frames and fading, all on 2s."""
    p = Vector(where.matrix_world.translation if hasattr(where, "matrix_world") else where)
    name = name or f"ripple_{f0}_{int(p.x * 100)}_{int(p.y * 100)}"
    out = []
    for i in range(n):
        s = f0 + i * every
        m = look.fade(f"{name}_m{i}", _hex(color), 0.0)
        mix = m.node_tree.nodes["Mix"]
        o = bpy.data.objects.new(f"{name}_{i}", _ring_mesh(f"{name}_{i}"))
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(m)
        o.location = (p.x, p.y, p.z + 0.004)
        o.visible_shadow = False
        anim.key(o, "scale", s - 1, (0.0001,) * 3, "CONSTANT")
        for t in range(0, frames + 1, 2):
            u = t / frames
            r = radius * k * (0.2 + 0.8 * (1 - (1 - u) ** 2))
            anim.key(o, "scale", s + t, (r, r * 0.97, 1), "CONSTANT")
            mix.inputs[0].default_value = 0.9 * (1 - u)
            mix.inputs[0].keyframe_insert("default_value", frame=s + t)
        for fc in anim.all_fcurves(m.node_tree.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
        out.append(o)
    return out


def fall_material(name="shared_fall"):
    """The falling water's glassy body: translucent cyan, brighter at its silhouette (a glass tube), with faint
    lighter bands sliding down it."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    lw = N("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    edge = N("ShaderNodeValToRGB")
    a0, a1 = edge.color_ramp.elements
    a0.position, a0.color = 0.35, _hex(BODY)
    a1.position, a1.color = 0.8, _hex(RIM)
    L(lw.outputs["Facing"], edge.inputs[0])
    geo = N("ShaderNodeNewGeometry")
    mp = N("ShaderNodeMapping")
    L(geo.outputs["Position"], mp.inputs["Vector"])
    wave = N("ShaderNodeTexWave")
    wave.wave_type, wave.bands_direction = "BANDS", "Z"
    wave.inputs["Scale"].default_value = 1.6
    wave.inputs["Distortion"].default_value = 0.8
    wave.inputs["Detail"].default_value = 0.0
    L(mp.outputs[0], wave.inputs["Vector"])
    bands = N("ShaderNodeMapRange")
    bands.inputs[1].default_value, bands.inputs[2].default_value = 0.7, 1.0
    bands.inputs[3].default_value, bands.inputs[4].default_value = 0.0, 0.35
    L(wave.outputs["Fac"], bands.inputs[0])
    _loop(nt, mp.inputs["Location"], 0, (0, 0, 0), 24, (0, 0, 1.4))             # the bands slide down
    col = N("ShaderNodeMix")
    col.data_type = "RGBA"
    col.clamp_factor = True
    col.inputs[7].default_value = (1, 1, 1, 1)
    L(bands.outputs[0], col.inputs[0])
    L(edge.outputs[0], col.inputs[6])
    em = N("ShaderNodeEmission")
    em.name = "Emission"
    em.inputs[1].default_value = 1.15
    L(col.outputs[2], em.inputs[0])
    alpha = N("ShaderNodeMapRange")                                              # see-through in the middle
    alpha.inputs[3].default_value, alpha.inputs[4].default_value = 0.55, 0.95
    L(lw.outputs["Facing"], alpha.inputs[0])
    tp = N("ShaderNodeBsdfTransparent")
    mix = N("ShaderNodeMixShader")
    mix.name = "Mix"
    L(alpha.outputs[0], mix.inputs[0])
    L(tp.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    out = N("ShaderNodeOutputMaterial")
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def _tube(name, pts, radius, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, q in zip(sp.bezier_points, pts):
        bp.co = q
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.bevel_depth = radius
    cu.bevel_resolution = 4
    cu.resolution_u = 16
    cu.use_fill_caps = True
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    o.visible_shadow = False
    return o


def falling_water(points, f0, f1=None, radius=0.07, grow=3, k=1.0, drops=True, rings=True, name="fall", seed=5,
                  taper=(1.15, 0.85)):
    """Water falling along `points` (world, top to bottom: the desk-edge waterfall, the tank jet's arc) from f0:
    a glassy ribbon (fall_material) round a thin white core, reaching the foot in `grow` frames (on 1s), its
    thickness pulsing on 2s; at the foot, splash drops hopping on 2s and ripple rings (k scales them). `taper`
    = the radius at the top and at the foot. Returns dict(body, core, drops, rings)."""
    pts = [Vector(p) for p in points]
    f1 = f1 if f1 is not None else f0 + 96
    body = _tube(f"{name}_body", pts, radius, fall_material())
    core = _tube(f"{name}_core", pts, radius * 0.32, look.flat("shared_fall_core", _hex(RIM), 1.6))
    for o in (body, core):
        sp = o.data.splines[0]
        for i, bp in enumerate(sp.bezier_points):
            u = i / max(1, len(sp.bezier_points) - 1)
            bp.radius = taper[0] + (taper[1] - taper[0]) * u
        cu = o.data
        for i in range(grow + 1):
            cu.bevel_factor_end = 0.0 if i == 0 else i / grow
            cu.keyframe_insert("bevel_factor_end", frame=f0 - 1 + i)
        r0 = cu.bevel_depth
        for n in range(f0 + grow, f1 + 1, 2):
            cu.bevel_depth = r0 * (1.1 if (n - f0) % 4 == 0 else 0.92)
            cu.keyframe_insert("bevel_depth", frame=n)
        for fc in anim.all_fcurves(cu.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    foot = pts[-1]
    out = dict(body=body, core=core, drops=[], rings=[])
    t0 = f0 + grow
    if drops:
        rnd = random.Random(seed)
        m = look.flat("shared_drop", _hex(RIM), 1.4)
        for i in range(9):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035 * k, segments=10, ring_count=6, location=tuple(foot))
            d = bpy.context.object
            d.name = f"{name}_drop{i}"
            d.data.materials.append(m)
            d.visible_shadow = False
            a = rnd.uniform(0, 2 * math.pi)
            v = Vector((math.cos(a), math.sin(a), 0)) * rnd.uniform(0.18, 0.4) * k
            hgt = rnd.uniform(0.25, 0.5) * k
            anim.key(d, "scale", t0 - 1, (0.001,) * 3, "CONSTANT")
            f = t0 + rnd.randint(0, 3) * 2
            while f < f1:
                life = 6
                for t in range(0, life + 1, 2):
                    u = t / life
                    anim.key(d, "location", f + t, tuple(foot + v * u + Vector((0, 0, 4 * hgt * u * (1 - u)))),
                             "CONSTANT")
                    anim.key(d, "scale", f + t, (1.0 if t < life else 0.001,) * 3, "CONSTANT")
                f += life + rnd.choice((2, 4))
            out["drops"].append(d)
    if rings:
        for s in range(t0, f1, 8):
            out["rings"] += ripple_rings(foot, s, n=1, radius=0.5 * k, frames=8, k=1.0, name=f"{name}_ring{s}")
    return out


def _copy_strength(old, new):
    """Carry an old material's Emission-strength keys (power_out, flickers, dimming) over to the new material,
    relative to each one's base strength."""
    eo, en = _em(old), _em(new)
    if eo is None or en is None or not (old.node_tree.animation_data and old.node_tree.animation_data.action):
        return
    path = eo.inputs[1].path_from_id("default_value")
    base_o, base_n = eo.inputs[1].default_value or 1.0, en.inputs[1].default_value
    for fc in anim.all_fcurves(old.node_tree.animation_data.action):
        if fc.data_path != path:
            continue
        for kp in fc.keyframe_points:
            en.inputs[1].default_value = base_n * kp.co.y / base_o
            en.inputs[1].keyframe_insert("default_value", frame=kp.co.x)
        for nfc in anim.all_fcurves(new.node_tree.animation_data.action):
            if nfc.data_path == en.inputs[1].path_from_id("default_value"):
                for a, b in zip(nfc.keyframe_points, fc.keyframe_points):
                    a.interpolation = b.interpolation
        en.inputs[1].default_value = base_n
        break


def _em(m):
    return next((n for n in m.node_tree.nodes if n.type == "EMISSION"), None) if m and m.use_nodes else None


def adopt(R=None, rims=True, stream=True, old=("lab_spill",)):
    """Restyle a built lab scene's spill with the shared look: every object using a material whose name starts with
    one of `old` (lab._water_floor()'s "lab_spill" and copies) gets spill_material() (with the desk lamp's
    reflection when R is given), keeping its Emission keys (power_out); flat puddle shapes get a rim(); and
    diorama_lab's flat "dl_spill_stream" quad becomes a falling_water() ribbon with the same timing. Call it at the
    end of a builder, after everything that makes water."""
    glint = None
    if R is not None:
        lamp = R.get("lights", {}).get("lamp")
        if lamp is not None:
            glint = (lamp.location.x, lamp.location.y - 1.0)
    new = spill_material(glint=glint)
    swapped = set()
    for o in list(bpy.data.objects):
        if o.type != "MESH" or o.name.endswith("_rim"):
            continue
        hit = False
        for i, m in enumerate(o.data.materials):
            if m is not None and m.name.startswith(old) and m is not new:
                if m.name not in swapped:
                    _copy_strength(m, new)
                    swapped.add(m.name)
                o.data.materials[i] = new
                hit = True
        if not hit:
            continue
        if o.name == "dl_spill_stream":
            if stream:
                _restream(o)
            continue
        if rims and (o.dimensions.z < 0.02 or o.name.startswith("dl_spill")):
            rim(o)
    return new


def _restream(quad):
    """diorama_lab's waterfall (a flat quad growing down from the desk edge) as a falling_water() ribbon: the same
    top, the same start and floor frames."""
    keys = sorted({round(kp.co.x) for fc in anim.all_fcurves(quad.animation_data.action) for kp in fc.keyframe_points}) \
        if quad.animation_data and quad.animation_data.action else [1, 4]
    f0, f_floor = keys[0] + 1, keys[-1]
    top = quad.location.copy()
    pts = [top + Vector((0, -0.02, 0)), top + Vector((0, -0.12, -top.z * 0.35)), top + Vector((0, -0.2, -top.z * 0.75)),
           Vector((top.x, top.y - 0.24, 0.02))]
    quad.hide_render = True
    falling_water(pts, f0, grow=max(2, f_floor - f0), radius=0.09, k=1.0, name="dl_fall")
