"""Dusk and night for the diorama island (Episode 3, DIORAMA_EP03.md; helper 9). Call AFTER the scene is built
(diorama.setup() + the set + the characters, so every material exists):

    from channels.monsters.mk import night
    night.apply("night")                      # or "dusk"; or night.apply("day") then night.transition(f0, f1, ...)
    lt = night.mark_light(k)                  # Kai's wrist mark: a coral point light on his left forearm (follows it)
    lh = night.lighthouse()                   # the ruined lighthouse on the rocky point across the lake

Why it works this way: the island's cel materials (look.toon / _anime, paint, paintbg, hero's) are emission shaders
whose light only picks a band (lit or shadow), so a dim sun can't make night and a coral lamp can't tint anything.
So:
- the sun becomes a cool MOON (same cel bands, so faces keep their light/shadow and read), the world fill goes cool,
  the painted sky goes to night (or dusk) colours, the haze goes dark blue;
- every material that has a ShaderToRGB also writes that light (the raw light colour reaching the surface) to a render
  AOV, "h9light";
- the compositor multiplies the frame by a night tint (dark blue), then adds back light where the AOV is coral: the
  moon and the fill are blue, the mark is coral, so (R - 0.62 B) is the mark's light alone, whatever the moon does.
  Surfaces near Kai's wrist come up warm, with the light's own falloff; the rest of the island is moonlit blue.
- unlit (flat) materials, which have no ShaderToRGB, just take the tint (glows stay glows through the bloom).

The coral is the mark's (helper 9's Ep 2 CORAL). The grade is keyable (transition()), for S04's sunset.
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.mk import look

CORAL = (1.0, 0.48, 0.36)                   # the mark (helper 9, Ep 2)
MOON = (0.62, 0.72, 1.0)                    # moonlight and the night fill: R = 0.62 B, so they drop out of the key
KEY_K = 0.62                                # the mark's light = (R - KEY_K * B) / (1 - KEY_K * CORAL[2])
AOV = "h9light"

# per mode: sky (zenith, horizon) as painted, sun (colour, energy, elevation), fill (colour, strength), haze colour,
# the frame tint (multiplies everything) and how strongly the mark's light comes back
MODES = {
    "day": dict(zenith="#7cc3f0", horizon="#e4f3fb", sun="#ffdcae", sun_e=4.2, sun_el=34.0, fill="#c4e2ff", fill_s=0.65,
                haze="#d9ecf6", tint=(1.0, 1.0, 1.0), key=0.0),
    "dusk": dict(zenith="#3b4f9a", horizon="#ff9a5c", sun="#ff9b5e", sun_e=3.6, sun_el=6.0, fill="#9db4ff",
                 fill_s=0.5, haze="#c99aa8", tint=(0.74, 0.56, 0.62), key=0.3),
    "night": dict(zenith="#22397c", horizon="#4d68b0", sun="#9eb6ff", sun_e=3.2, sun_el=48.0, fill="#9eb6ff",
                  fill_s=0.45, haze="#36507f", tint=(0.20, 0.20, 0.44), key=1.0),   # FINAL 7 Nov: greens -35 %
}
KEY_GAIN = 0.9                              # mark light -> brightness (AOV units: a lit face 3 units away ~ 1)
KEY_CAP = 1.0
KEY_POW = 1.7                               # > 1: bright at the wrist, dark a few units out
KEY_TINT = (1.0, 0.27, 0.16)                # what the mark's light multiplies (deeper than CORAL: green grass
                                            # x CORAL reads yellow)
KEY_ADD = 0.45 
KEY_COL = (1.0, 0.235, 0.133)               # #ff8466 in linear: the pool's colour (CORAL is the light's)                             # + a little coral on top, whatever the surface colour


def _hex(h):
    return look.hexc(h)


# ------------------------------------------------------------------------------------------------------- materials
def _tag_materials():
    """Every material with a ShaderToRGB writes its light colour to the AOV (once per material)."""
    vl = bpy.context.view_layer
    if AOV not in [a.name for a in vl.aovs]:
        a = vl.aovs.add()
        a.name, a.type = AOV, "COLOR"
    n = 0
    for m in bpy.data.materials:
        if not m.use_nodes or m.node_tree is None:
            continue
        nt = m.node_tree
        if any(nd.bl_idname == "ShaderNodeOutputAOV" and getattr(nd, "aov_name", "") == AOV for nd in nt.nodes):
            continue
        s2r = next((nd for nd in nt.nodes if nd.bl_idname == "ShaderNodeShaderToRGB"), None)
        if s2r is None:
            continue
        out = nt.nodes.new("ShaderNodeOutputAOV")
        out.aov_name = AOV
        nt.links.new(s2r.outputs["Color"], out.inputs["Color"])
        n += 1
    return n


# --------------------------------------------------------------------------------------------------------- world
def _sky_ramp():
    w = bpy.context.scene.world
    return next((nd for nd in w.node_tree.nodes if nd.bl_idname == "ShaderNodeValToRGB"), None) if w else None


def _fill_bg():
    w = bpy.context.scene.world
    return w.node_tree.nodes.get("Background") if w else None


def _sun():
    return next((o for o in bpy.context.scene.objects if o.type == "LIGHT" and o.data.type == "SUN"), None)


def _haze_mix():
    nt = bpy.context.scene.node_tree
    if nt is None:
        return None
    for nd in nt.nodes:                                       # diorama._compositor: Mist -> ramp -> MixRGB(fac)
        if nd.bl_idname == "CompositorNodeMixRGB" and nd.inputs[0].links and \
                nd.inputs[0].links[0].from_node.bl_idname == "CompositorNodeValToRGB":
            return nd
    return None


# ---------------------------------------------------------------------------------------------------- compositor
def _grade_nodes():
    """Insert (once) the night grade after the haze, before the bloom: out = img * tint + img * CORAL * key * m,
    m = clamp(KEY_GAIN * (R - 0.62 B) / (1 - 0.62 * 0.36), 0, KEY_CAP) from the AOV. Returns the keyable nodes."""
    sc = bpy.context.scene
    nt = sc.node_tree
    if "h9n_tint" in nt.nodes:
        return nt.nodes["h9n_tint"], nt.nodes["h9n_key"]
    rl = next(nd for nd in nt.nodes if nd.bl_idname == "CompositorNodeRLayers")
    hz = _haze_mix()
    if hz is not None and hz.outputs[0].links:
        src, dst = hz.outputs[0], [lk.to_socket for lk in hz.outputs[0].links]
    else:
        comp = next(nd for nd in nt.nodes if nd.bl_idname == "CompositorNodeComposite")
        src, dst = comp.inputs[0].links[0].from_socket, [comp.inputs[0]]
    N = nt.nodes.new
    tint = N("CompositorNodeMixRGB")
    tint.name, tint.blend_type = "h9n_tint", "MULTIPLY"
    tint.inputs[0].default_value = 1.0
    tint.inputs[2].default_value = (1, 1, 1, 1)
    nt.links.new(src, tint.inputs[1])
    sep = N("CompositorNodeSeparateColor")
    nt.links.new(rl.outputs[AOV], sep.inputs[0])
    mb = N("CompositorNodeMath")
    mb.operation, mb.inputs[1].default_value = "MULTIPLY", -KEY_K
    nt.links.new(sep.outputs[2], mb.inputs[0])
    ad = N("CompositorNodeMath")
    ad.operation = "ADD"
    nt.links.new(sep.outputs[0], ad.inputs[0])
    nt.links.new(mb.outputs[0], ad.inputs[1])
    sc_ = N("CompositorNodeMath")
    sc_.operation = "MULTIPLY"
    sc_.inputs[1].default_value = KEY_GAIN / (1 - KEY_K * CORAL[2])
    nt.links.new(ad.outputs[0], sc_.inputs[0])
    cl = N("CompositorNodeMath")
    cl.operation, cl.inputs[1].default_value = "MINIMUM", KEY_CAP
    cl0 = N("CompositorNodeMath")
    cl0.operation, cl0.inputs[1].default_value = "MAXIMUM", 0.0
    nt.links.new(sc_.outputs[0], cl0.inputs[0])
    pw = N("CompositorNodeMath")                               # a steeper falloff than the light's own 1/d^2
    pw.operation, pw.inputs[1].default_value = "POWER", KEY_POW
    nt.links.new(cl0.outputs[0], pw.inputs[0])
    nt.links.new(pw.outputs[0], cl.inputs[0])
    key = N("CompositorNodeMath")                              # x the mode's key strength (keyable)
    key.name, key.operation = "h9n_key", "MULTIPLY"
    key.inputs[1].default_value = 0.0
    nt.links.new(cl.outputs[0], key.inputs[0])
    lit = N("CompositorNodeMixRGB")                            # img * m
    lit.blend_type = "MULTIPLY"
    lit.inputs[0].default_value = 1.0
    nt.links.new(src, lit.inputs[1])
    nt.links.new(key.outputs[0], lit.inputs[2])
    warm = N("CompositorNodeMixRGB")                           # ... * coral
    warm.blend_type = "MULTIPLY"
    warm.inputs[0].default_value = 1.0
    warm.inputs[2].default_value = (*KEY_TINT, 1)
    nt.links.new(lit.outputs[0], warm.inputs[1])
    glow = N("CompositorNodeMixRGB")                           # + coral * m * KEY_ADD
    glow.blend_type = "MULTIPLY"
    glow.inputs[0].default_value = 1.0
    glow.inputs[1].default_value = (KEY_COL[0] * KEY_ADD, KEY_COL[1] * KEY_ADD, KEY_COL[2] * KEY_ADD, 1)
    nt.links.new(key.outputs[0], glow.inputs[2])
    add0 = N("CompositorNodeMixRGB")
    add0.blend_type = "ADD"
    add0.inputs[0].default_value = 1.0
    nt.links.new(warm.outputs[0], add0.inputs[1])
    nt.links.new(glow.outputs[0], add0.inputs[2])
    add = N("CompositorNodeMixRGB")
    add.name, add.blend_type = "h9n_out", "ADD"
    add.inputs[0].default_value = 1.0
    nt.links.new(tint.outputs[0], add.inputs[1])
    nt.links.new(add0.outputs[0], add.inputs[2])
    for d in dst:
        nt.links.new(add.outputs[0], d)
    return tint, key


# ----------------------------------------------------------------------------------------------------- the modes
def _set(mode, frame=None, azim=None):
    """Put the scene in `mode` (and key it at `frame` if given)."""
    g = MODES[mode]
    sc = bpy.context.scene
    keys = []
    r = _sky_ramp()
    if r is not None:
        r.color_ramp.elements[0].color = _hex(g["horizon"])
        r.color_ramp.elements[1].color = _hex(g["zenith"])
        keys += [(r.color_ramp.elements[0], "color"), (r.color_ramp.elements[1], "color")]
    bg = _fill_bg()
    if bg is not None:
        bg.inputs[0].default_value = _hex(g["fill"])
        bg.inputs[1].default_value = g["fill_s"]
        keys += [(bg.inputs[0], "default_value"), (bg.inputs[1], "default_value")]
    s = _sun()
    if s is not None:
        s.data.color = _hex(g["sun"])[:3]
        s.data.energy = g["sun_e"]
        az = s.rotation_euler[2] if azim is None else math.radians(azim)
        s.rotation_euler = (math.radians(90 - g["sun_el"]), 0, az)
        keys += [(s.data, "color"), (s.data, "energy"), (s, "rotation_euler")]
    hz = _haze_mix()
    if hz is not None:
        hz.inputs[2].default_value = _hex(g["haze"])
        keys.append((hz.inputs[2], "default_value"))
    tint, key = _grade_nodes()
    tint.inputs[2].default_value = (*g["tint"], 1)
    key.inputs[1].default_value = g["key"]
    keys += [(tint.inputs[2], "default_value"), (key.inputs[1], "default_value")]
    if frame is not None:
        for owner, path in keys:
            owner.keyframe_insert(path, frame=frame)
    return g


_MODE = {"mode": "day"}


def _on_render(*_args):
    _tag_materials()
    if _MODE["mode"] == "night":
        lake_night()


def _hook():
    """Tag materials again when a render starts, so characters and props built after apply() get the mark's light."""
    h = bpy.app.handlers.render_init
    if not any(getattr(f, "__name__", "") == "_on_render" for f in h):
        h.append(_on_render)


def apply(mode="night", azim=None):
    """The whole scene in `mode` ("day", "dusk" or "night"): sky, moon/sun, fill, haze and the grade. Call it any time
    after diorama.setup(): materials are tagged for the mark's light now and again when the render starts."""
    _tag_materials()
    _hook()
    _MODE["mode"] = mode
    if mode == "night":
        lake_night()                                           # (again at render start, if the lake comes later)
    return _set(mode, azim=azim)


def transition(f0, f1, a="day", b="dusk", c=None, f2=None, azim=None):
    """Key the scene from mode `a` at f0 to `b` at f1 (and on to `c` at f2): S04's sunset (day -> dusk -> night).
    The sun sinks with the modes' elevations. Linear between the keys."""
    _tag_materials()
    _hook()
    _set(a, f0, azim)
    _set(b, f1, azim)
    if c is not None:
        _set(c, f2, azim)
    for idb in (bpy.context.scene.world, bpy.context.scene, _sun(), _sun().data if _sun() else None):
        ad = getattr(idb, "animation_data", None) if idb is not None else None
        tree = getattr(idb, "node_tree", None) if idb is not None else None
        for holder in (ad, getattr(tree, "animation_data", None) if tree else None):
            if holder and holder.action:
                for fc in _fcurves(holder.action):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"


def _fcurves(action):
    try:
        from channels.monsters.mk import anim
        return anim.all_fcurves(action)
    except Exception:                                          # noqa: BLE001
        return list(getattr(action, "fcurves", []))


# ------------------------------------------------------------------------------------------------- the mark light
def mark_light(k, energy=6000.0, u=0.3, side="L", name="h9_mark_light", radius=0.25, key=None, core=0.13):
    """Kai's wrist mark as a light: a coral point light just off the inside of his left forearm (u of the way from
    the elbow to the wrist, as helper 9's Ep 2 mark), parented to the forearm bone so it follows every pose.
    `key` = [(frame, energy), ...] keys its power (a flare, a dim). Returns the light object."""
    arm = k["arm"]
    bpy.context.view_layer.update()
    pb = arm.pose.bones[f"forearm.{side}"]
    hand = arm.pose.bones[f"hand.{side}"]
    p_arm = pb.head.lerp(hand.head, u)                        # armature space, rest/current pose
    d = bpy.data.lights.new(name, "POINT")
    d.color = CORAL
    d.energy = energy
    d.shadow_soft_size = radius
    d.use_shadow = False                                      # a glow: his own arm and body must not block it
    if hasattr(d, "use_soft_falloff"):
        d.use_soft_falloff = True
    lt = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(lt)
    lt.parent = arm
    lt.parent_type = "BONE"
    lt.parent_bone = f"forearm.{side}"
    bpy.context.view_layer.update()
    # place it in world space at the mark, lifted 0.35 off the skin toward the palm side (the mark's side)
    M = arm.matrix_world
    w_mark = M @ p_arm
    w_up = (M.to_3x3() @ (pb.matrix.to_3x3() @ Vector((0, 0, 1)))).normalized()
    lt.matrix_world = lt.matrix_world.__class__.Translation(w_mark + w_up * 0.35)
    for f, e in key or []:
        d.energy = e
        d.keyframe_insert("energy", frame=f)
    if core:                                                   # the mark itself: a small hot coral core (blooms)
        import bmesh
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=core)
        me = bpy.data.meshes.new(f"{name}_core")
        bm.to_mesh(me)
        bm.free()
        c = bpy.data.objects.new(f"{name}_core", me)
        bpy.context.scene.collection.objects.link(c)
        c.data.materials.append(look.flat(f"{name}_core", (1.0, 0.30, 0.17, 1), strength=14.0))
        c.visible_shadow = False
        c.parent = arm
        c.parent_type = "BONE"
        c.parent_bone = f"forearm.{side}"
        bpy.context.view_layer.update()
        c.matrix_world = c.matrix_world.__class__.Translation(w_mark + w_up * 0.12)
        lt["core"] = c.name
    return lt


# ----------------------------------------------------------------------------------------------- the lighthouse
LIGHTHOUSE_AT = Vector((120.0, -720.0, 0.0))  # a rocky point on the far side of the lake (shore y -190, lake to -1500)


def _cel_tex(name, col_node_fn, threshold=0.45):
    """An anime cel material whose base colour comes from a texture network: col_node_fn(nt) -> colour socket."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].color = (*look.SHADOW_TINT, 1)
    ramp.color_ramp.elements[1].position = threshold
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    em = nt.nodes.new("ShaderNodeEmission")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], mul.inputs[6])
    L(col_node_fn(nt), mul.inputs[7])
    L(mul.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def _stone_mat(name, a="#b4ad9f", b="#958d80", mortar="#5b5650", scale=0.22):
    """Rough stone blocks: a brick pattern (staggered courses, dark mortar) with painted noise across the blocks."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]

    def col(nt):
        tc = nt.nodes.new("ShaderNodeTexCoord")
        br = nt.nodes.new("ShaderNodeTexBrick")
        br.inputs["Scale"].default_value = scale
        br.inputs["Mortar Size"].default_value = 0.035
        br.inputs["Brick Width"].default_value = 1.6
        br.inputs["Row Height"].default_value = 0.75
        br.inputs["Color1"].default_value = _hex(a)
        br.inputs["Color2"].default_value = _hex(b)
        br.inputs["Mortar"].default_value = _hex(mortar)
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 0.9
        nz.inputs["Detail"].default_value = 3.0
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type, mx.blend_type = "RGBA", "OVERLAY"
        mx.inputs["Factor"].default_value = 0.35
        mp = nt.nodes.new("ShaderNodeMapping")                    # bricks on the walls: (x, z), not the floor plane
        mp.inputs["Rotation"].default_value = (math.pi / 2, 0, 0)
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs[0], br.inputs["Vector"])
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        nt.links.new(br.outputs["Color"], mx.inputs[6])
        nt.links.new(nz.outputs["Color"], mx.inputs[7])
        return mx.outputs[2]
    return _cel_tex(name, col)


def _halo_mat(name, col, strength):
    """A soft additive glow ball: emission strongest where the surface faces the camera, transparent at the rim."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    else:
        m.blend_method = "BLEND"
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation, pw.inputs[1].default_value = "POWER", 4.5
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation, inv.inputs[0].default_value = "SUBTRACT", 1.0
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = col
    em.inputs[1].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    add = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lw.outputs["Facing"], inv.inputs[1])            # 1 - facing: 1 at the centre, 0 at the rim
    nt.links.new(inv.outputs[0], pw.inputs[0])
    nt.links.new(pw.outputs[0], add.inputs[0])
    nt.links.new(tr.outputs[0], add.inputs[1])
    nt.links.new(em.outputs[0], add.inputs[2])
    nt.links.new(add.outputs[0], out.inputs[0])
    return m


def lighthouse(at=LIGHTHOUSE_AT, scale=1.5, glow=1.0, name="h9_lighthouse"):
    """The old lighthouse: a squat, tapering tower of rough stone blocks on a rocky point (moss at its foot), a small
    dark door and one slit window, the top crumbled into an uneven broken ring with fallen stones on the rocks below,
    and in the open lamp room a soft coral glow (a cracked lens, a coral light that warms the broken stone and a halo):
    the only warm thing in its frame. About 46 units tall at scale 1 (the village huts are ~10).
    Returns dict(root, glow_light, lamp, halo, top)."""
    import bmesh
    rnd = __import__("random").Random(7)
    S = scale
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    root.location = at
    stone = _stone_mat(f"{name}_stone")
    stone2 = _stone_mat(f"{name}_stone2", a="#a39b8d", b="#867f73")
    rock = look.toon(f"{name}_rock", _hex("#6f6a66"))
    moss = look.toon(f"{name}_moss", _hex("#4f7a3c"))
    dark = look.flat(f"{name}_dark", (0.015, 0.015, 0.03, 1))
    glow_m = look.flat(f"{name}_glow", (1.0, 0.40, 0.18, 1), strength=6.5 * glow)   # coral after the night tint
    core_m = look.flat(f"{name}_core", (1.0, 0.72, 0.5, 1), strength=14.0 * glow)    # the hot core: near-white
    halo_m = _halo_mat(f"{name}_halo", (1.0, 0.36, 0.2, 1), 2.4 * glow)

    def obj(nm, bm, mat, line=0.06):
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new(nm, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(mat)
        o.parent = root
        for p in o.data.polygons:
            p.use_smooth = False
        if line:
            try:
                look.outline(o, line)
            except Exception:                                  # noqa: BLE001
                pass
        return o

    def boulder(nm, r, pos, mat, line=0.05, squash=1.0):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
        for v in bm.verts:
            v.co.x *= 1.0 + rnd.random() * 0.5
            v.co.y *= 1.0 + rnd.random() * 0.5
            v.co.z *= (0.9 + rnd.random() * 0.5) * squash
            v.co += Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * r * 0.12
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector(pos))
        return obj(nm, bm, mat, line)

    # the rocky point: a cluster of chunky boulders, the tower's plinth on top, moss tufts in the cracks
    for i in range(22):
        r = (3 + rnd.random() * 3.5) * S * (1.3 if i == 0 else 1.0)
        a = rnd.random() * 2 * math.pi
        d = (0 if i == 0 else 4 + rnd.random() * 12) * S
        boulder(f"{name}_rock{i}", r, (math.cos(a) * d, math.sin(a) * d * 0.8, r * (0.35 if i else 0.5)), rock)
    base_z = 5.5 * S
    H, R0, R1 = 34.0 * S, 6.2 * S, 4.4 * S
    for i in range(14):                                        # moss round the foot of the tower and on the rocks
        a = rnd.random() * 2 * math.pi
        d = R0 * (0.95 + rnd.random() * 0.5)
        boulder(f"{name}_moss{i}", (0.9 + rnd.random() * 1.2) * S,
                (math.cos(a) * d, math.sin(a) * d, base_z + rnd.uniform(-0.6, 0.6) * S), moss, 0.03, squash=0.45)
    # the tower: 4 tapering drums of stone blocks with plain bands between, 14 sides
    drums = 4
    for i in range(drums):
        z0, z1 = base_z + H * i / drums, base_z + H * (i + 1) / drums
        r0, r1 = R0 + (R1 - R0) * i / drums, R0 + (R1 - R0) * (i + 1) / drums
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=r0, radius2=r1, depth=z1 - z0)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, (z0 + z1) / 2)))
        obj(f"{name}_drum{i}", bm, stone if i % 2 == 0 else stone2)
        if i < drums - 1:
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=r1 * 1.07, radius2=r1 * 1.07,
                                  depth=0.8 * S)
            bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, z1)))
            obj(f"{name}_band{i}", bm, stone2)
    # a small dark door at the foot and one slit window high up (on the -Y side: toward the village shore)
    for (nm, zz, ww, hh) in (("door", base_z + 2.4 * S, 2.6 * S, 4.4 * S), ("slit", base_z + 21 * S, 0.9 * S, 3.2 * S)):
        rr = R0 + (R1 - R0) * (zz - base_z) / H
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((ww, 0.6 * S, hh)), verts=bm.verts)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, -rr + 0.12 * S, zz)))
        obj(f"{name}_{nm}", bm, dark, 0.0)
    # the crumbled top: a broken wall ring of uneven blocks round the open lamp room (tall stubs and gaps)
    top = base_z + H
    bm = bmesh.new()                                           # the lamp room floor
    bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=R1 * 1.12, radius2=R1 * 1.12, depth=0.8 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top)))
    obj(f"{name}_floor", bm, stone2)
    blocks = 14
    for i in range(blocks):
        if i in (3, 9, 10):                                    # gaps where the wall fell away
            continue
        a = 2 * math.pi * (i + 0.5) / blocks
        hgt = S * (1.2 + 7.0 * abs(math.sin(i * 1.7)) * rnd.uniform(0.5, 1.0))
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((2.0 * S, 1.2 * S, hgt)), verts=bm.verts)
        for v in bm.verts:                                     # a broken, slanted top on each stub
            if v.co.z > 0:
                v.co.z += rnd.uniform(-0.25, 0.25) * hgt
        bmesh.ops.rotate(bm, verts=bm.verts, cent=Vector((0, 0, 0)),
                         matrix=__import__("mathutils").Matrix.Rotation(a + math.pi / 2, 3, "Z"))
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((math.cos(a) * R1 * 0.95, math.sin(a) * R1 * 0.95,
                                                           top + hgt / 2)))
        obj(f"{name}_wall{i}", bm, stone)
    for i in range(9):                                         # fallen stones: on the floor and down on the rocks
        on_floor = i < 3
        a = rnd.random() * 2 * math.pi
        d = (rnd.uniform(0.3, 0.8) * R1) if on_floor else (R0 + rnd.uniform(1.5, 7.0) * S)
        z = (top + 0.9 * S) if on_floor else (base_z + rnd.uniform(-2.5, 0.5) * S)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((1.8, 1.1, 0.9)) * S * rnd.uniform(0.7, 1.2), verts=bm.verts)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=Vector((0, 0, 0)),
                         matrix=__import__("mathutils").Euler((rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6),
                                                               rnd.uniform(0, 3))).to_matrix())
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((math.cos(a) * d, math.sin(a) * d, z)))
        obj(f"{name}_fallen{i}", bm, stone2, 0.04)
    # the glow: a cracked coral lens, a halo round it, and a warm light that lights the broken stone from inside
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.5 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top + 2.2 * S)))
    lamp = obj(f"{name}_lamp", bm, glow_m, 0.0)
    lamp.visible_shadow = False
    bm = bmesh.new()                                           # a hot near-white core inside the lens
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.75 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, -0.6 * S, top + 2.4 * S)))
    core = obj(f"{name}_corelamp", bm, core_m, 0.0)
    core.visible_shadow = False
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=6.5 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top + 2.6 * S)))
    halo = obj(f"{name}_halo", bm, halo_m, 0.0)
    halo.visible_shadow = False
    for p_ in halo.data.polygons:                              # smooth: a flat-shaded halo shows its facets
        p_.use_smooth = True
    d = bpy.data.lights.new(f"{name}_light", "POINT")
    d.color = CORAL
    d.energy = 26000.0 * S * S * glow
    d.shadow_soft_size = 1.2 * S
    lt = bpy.data.objects.new(f"{name}_light", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.parent = root
    lt.location = (0, 0, top + 2.6 * S)
    _tag_materials()
    return dict(root=root, glow_light=lt, lamp=lamp, halo=halo, top=Vector(at) + Vector((0, 0, top + 2.2 * S)))


# ------------------------------------------------------------------------------------------------- the night lake
def lake_night(names=("h9_lake", "h9_lake_shallow"), navy="#0b1530", ripple="#7f97c9"):
    """Helper 9's Ep 2 lake (diorama_ep02/helper9.village_and_lake) at night: deep navy-black with thin, broken moonlit
    ripple lines (stretched noise, thresholded), still a cel material so the mark's / the lamp's light warms it."""
    def col(nt):
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (0.05, 0.9, 1.0)       # long in x: ripples run across the view
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 1.6
        nz.inputs["Detail"].default_value = 2.0
        rp = nt.nodes.new("ShaderNodeValToRGB")
        rp.color_ramp.interpolation = "CONSTANT"
        rp.color_ramp.elements[0].color = _hex(navy)
        rp.color_ramp.elements[1].position = 0.66
        rp.color_ramp.elements[1].color = _hex(ripple)
        e = rp.color_ramp.elements.new(0.69)
        e.color = _hex(navy)
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs[0], nz.inputs["Vector"])
        nt.links.new(nz.outputs["Fac"], rp.inputs[0])
        return rp.outputs[0]
    m = bpy.data.materials.get("h9_lake_night") or _cel_tex("h9_lake_night", col, threshold=0.3)
    for nm in names:
        o = bpy.data.objects.get(nm)
        if o is not None and o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(m)
    _tag_materials()
    return m


def reflection(src, toward, length=420.0, width=5.0, z=0.3, dashes=48, name="h9_reflect", strength=1.8, seed=3):
    """The lamp's long coral reflection on the water: broken horizontal dashes on a line from below `src` (the light)
    toward `toward` (the camera's position, projected on the water), wider and fainter as they come closer."""
    import bmesh
    rnd = __import__("random").Random(seed)
    a = Vector((src[0], src[1], z))
    b = Vector((toward[0], toward[1], z))
    dirv = (b - a)
    if dirv.length < 1e-3:
        return None
    dirv.normalize()
    side = Vector((-dirv.y, dirv.x, 0))
    bm = bmesh.new()
    for i in range(dashes):
        t = (i + rnd.random() * 0.6) / dashes
        c = a + dirv * (length * t ** 1.4)
        if rnd.random() < 0.18:                                # gaps: the water breaks the line up
            continue
        w = width * (0.4 + 2.2 * t) * rnd.uniform(0.3, 1.4)
        h = (0.5 + 2.2 * t) * rnd.uniform(0.4, 1.0)
        off = side * rnd.uniform(-0.6, 0.6) * width * (0.5 + 1.5 * t)
        p = [c + off + side * (w / 2) * sx + dirv * (h / 2) * sy for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        vs = [bm.verts.new(q) for q in p]
        bm.faces.new(vs)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(look.flat(f"{name}_mat", (1.0, 0.36, 0.2, 1), strength=strength))
    o.visible_shadow = False
    return o


def moon(az=200.0, el=24.0, dist=2600.0, r=55.0, name="h9_moon", origin=(0, 0, 0)):
    """A pale moon disc low in the sky (az / el in degrees, az 0 = north (+Y), 90 = east) with a soft halo; the moonlight
    (the scene's sun at night) comes from the same direction, so it rims what it lights."""
    import bmesh
    e, a = math.radians(el), math.radians(az)
    d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
    pos = Vector(origin) + d * dist                            # origin: e.g. the camera, to frame it exactly
    out = {}
    for nm, rad, mat in ((name, r, look.flat(f"{name}_mat", (2.2, 2.3, 2.6, 1), strength=1.4)),
                         (f"{name}_halo", r * 3.2, _halo_mat(f"{name}_halo", (0.55, 0.65, 1.0, 1), 1.2))):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=rad)
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        for p_ in me.polygons:
            p_.use_smooth = True
        o = bpy.data.objects.new(nm, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(mat)
        o.location = pos
        o.visible_shadow = False
        out[nm] = o
    s = _sun()
    if s is not None:                                          # the moonlight comes from the moon
        s.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    return out
