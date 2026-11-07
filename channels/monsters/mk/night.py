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
                 fill_s=0.5, haze="#c99aa8", tint=(0.86, 0.68, 0.72), key=0.55),
    "night": dict(zenith="#1a2c63", horizon="#3d5596", sun="#9eb6ff", sun_e=3.2, sun_el=48.0, fill="#9eb6ff",
                  fill_s=0.45, haze="#36507f", tint=(0.26, 0.31, 0.56), key=1.0),
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


def _on_render(*_args):
    _tag_materials()


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


def lighthouse(at=LIGHTHOUSE_AT, scale=1.5, glow=1.0, name="h9_lighthouse"):
    """The old lighthouse: a squat, tapering stone tower on a rocky point, its top broken off in a jagged ring, an open
    lamp room with a faint coral glow (the mark's coral) and a small coral light inside that warms the broken stone.
    About 46 units tall at scale 1 (the village huts are ~10). Returns dict(root, glow_light, lamp)."""
    import bmesh
    rnd = __import__("random").Random(7)
    S = scale
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    root.location = at
    stone = look.toon(f"{name}_stone", _hex("#b9b3a6"))
    stone2 = look.toon(f"{name}_stone2", _hex("#9f988b"))
    rock = look.toon(f"{name}_rock", _hex("#6f6a66"))
    dark = look.toon(f"{name}_dark", _hex("#3b3a44"))
    glow_m = look.flat(f"{name}_glow", (1.0, 0.40, 0.18, 1), strength=4.0 * glow)   # coral after the night tint

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

    # the rocky point: a cluster of chunky boulders, the tower's plinth on top
    for i in range(22):
        bm = bmesh.new()
        r = (3 + rnd.random() * 3.5) * S * (1.3 if i == 0 else 1.0)
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
        for v in bm.verts:
            v.co.x *= 1.0 + rnd.random() * 0.5
            v.co.y *= 1.0 + rnd.random() * 0.5
            v.co.z *= 0.9 + rnd.random() * 0.5
            v.co += Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * r * 0.12
        a = rnd.random() * 2 * math.pi
        d = (0 if i == 0 else 4 + rnd.random() * 12) * S
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((math.cos(a) * d, math.sin(a) * d * 0.8,
                                                           r * (0.35 if i else 0.5))))
        obj(f"{name}_rock{i}", bm, rock, 0.05)
    base_z = 5.5 * S
    # the tower: 4 tapering stone drums with darker bands, 12 sides, a little lean
    H, R0, R1 = 34.0 * S, 6.2 * S, 4.4 * S
    drums = 4
    for i in range(drums):
        z0, z1 = base_z + H * i / drums, base_z + H * (i + 1) / drums
        r0, r1 = R0 + (R1 - R0) * i / drums, R0 + (R1 - R0) * (i + 1) / drums
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r0, radius2=r1, depth=z1 - z0)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, (z0 + z1) / 2)))
        obj(f"{name}_drum{i}", bm, stone if i % 2 == 0 else stone2)
        bm = bmesh.new()                                       # the band between drums
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r1 * 1.08, radius2=r1 * 1.08, depth=0.9 * S)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, z1)))
        obj(f"{name}_band{i}", bm, stone2)
    # a door and two slit windows (dark)
    for (zz, ww, hh) in ((base_z + 2.6 * S, 2.4 * S, 4.6 * S), (base_z + 14 * S, 1.0 * S, 2.6 * S),
                         (base_z + 23 * S, 1.0 * S, 2.6 * S)):
        rr = R0 + (R1 - R0) * (zz - base_z) / H
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((ww, 0.6 * S, hh)), verts=bm.verts)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, -rr + 0.15 * S, zz)))
        obj(f"{name}_hole{zz:.0f}", bm, dark, 0.0)
    # the lamp room: a short open drum of 8 stone posts, its roof gone; the top of the wall broken into a jagged ring
    top = base_z + H
    posts = 8
    for i in range(posts):
        a = 2 * math.pi * i / posts
        hgt = (6.5 if i % 3 else 3.0) * S * (0.6 + rnd.random() * 0.5)   # broken posts at different heights
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((1.3 * S, 1.3 * S, hgt)), verts=bm.verts)
        bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((math.cos(a) * R1 * 0.92, math.sin(a) * R1 * 0.92,
                                                           top + hgt / 2)))
        for v in bm.verts:                                     # jagged tops
            if v.co.z > top + hgt * 0.9:
                v.co.z += rnd.uniform(-0.9, 0.5) * S
        obj(f"{name}_post{i}", bm, stone)
    bm = bmesh.new()                                           # the lamp room floor
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=R1 * 1.15, radius2=R1 * 1.15, depth=0.8 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top)))
    obj(f"{name}_floor", bm, stone2)
    # the glow: a soft coral core in the lamp room (an old cracked lens) + a warm light
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.6 * S)
    bmesh.ops.translate(bm, verts=bm.verts, vec=Vector((0, 0, top + 2.2 * S)))
    lamp = obj(f"{name}_lamp", bm, glow_m, 0.0)
    lamp.visible_shadow = False                               # the glowing lens mustn't block its own light
    d = bpy.data.lights.new(f"{name}_light", "POINT")
    d.color = CORAL
    d.energy = 26000.0 * S * S * glow
    d.shadow_soft_size = 1.2 * S
    lt = bpy.data.objects.new(f"{name}_light", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.parent = root
    lt.location = (0, 0, top + 2.6 * S)
    _tag_materials()
    return dict(root=root, glow_light=lt, lamp=lamp, top=Vector(at) + Vector((0, 0, top + 2.2 * S)))
