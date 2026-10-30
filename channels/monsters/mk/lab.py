"""Earth LAB set for Episode 1: a university wildlife-biology lab at night in a rainstorm. A desk with laptop, notebook,
lamp and a slot for the pistol shrimp's tank (mk/pistolshrimp.tank(), helper 2's); glowing aquarium shelves; a
rain-streaked window; a power strip with cables on a dark tiled floor.

Painted-background look (look.paint, no outlines); thin coloured lines only on the props a person touches (desk edge,
laptop, chair, mug, lamp base, power strip). Every room material runs through one shared grade ("lab_grade") that adds
a little of the coloured light (so the tanks tint the room cyan and the lamp warm) and holds two keyable values:
`level` (room brightness, for flicker and power-out) and `flash` (the blue lightning flash).

    handles = lab.build()
    handles["place_tank"](pistolshrimp.tank())   # helper 2's tank into the desk slot (scaled), before crack_puddle
    handles["lightning"](frame)          # the sky goes pale, a bolt shows in the window, the room flashes blue
    handles["flicker"]([40, 43, 47])     # the ceiling light and lamp stutter off for 2 frames at each frame listed
    handles["crack_puddle"](f0, f1)      # water leaks across the desk, pours off it and reaches the power strip at f1
    handles["spark"](frame)              # bright spark at the strip
    handles["power_out"](frame)          # every lab light goes out (the window stays lit by the storm)
    handles["floor_pan"](f0, f1)         # S09's short pan from the pouring water to the strip

Cameras: handles["cams"]["wide" | "desk" | "medium" | "window" | "floor"], framed for 720x1280 and the caption safe
areas. "desk" is over Kai's shoulder (the lower left is left for him); "medium" is S03 (Kai's seat with the glowing
tanks behind him); "window" is S07; "floor" is S09/S10.
For other pieces to plug in:
- "window": its centre and size, the sky and bolt materials and the moon / lightning suns (for helper 9's storm);
- "room_lights": the ceiling light and lamp, their glow materials, and the grade (for the flicker);
- "desk": top height, centre, laptop, screen material, "seat" (an empty on the chair cushion where Kai sits),
  "chair" (the chair's root: rotate z to swivel it toward the camera, e.g. for S03) and "tank_slot";
- "tank_slot": the slot empty, centre, size, the scale and root location place_tank uses, the leak point, its glow;
- "floor": the tiles object and the floor's extent (z = 0);
- "strip", "strip_end" (where the water arrives), "spark_at"; "tanks" (the four shelf tanks), "lights", "grade".
build() replaces the scene's world with a dark night world.
Everything is procedural and seeded; no downloaded assets."""
import math
import random

import bpy
from mathutils import Vector

from . import anim, look, paintbg

hx = look.hexc
WALL_Y = 2.5                 # back wall (the window and the tanks are on it)
ROOM = (-2.5, 2.5, -3.0, WALL_Y, 2.9)   # x0, x1, y0, y1, height
FLOOR_CAM, FLOOR_AIM = (0.35, 0.5, 0.32), (-0.5, 1.65, 0.05)
LIGHT_K = 0.42               # how much coloured light the grade adds on top of the painted colour
FLASH_RGB = (0.32, 0.5, 1.0)  # the room's lightning tint


# ---------------------------------------------------------------- materials
def _grade():
    ng = bpy.data.node_groups.get("lab_grade")
    if ng:
        return ng
    ng = bpy.data.node_groups.new("lab_grade", "ShaderNodeTree")
    ng.interface.new_socket("Paint", in_out="INPUT", socket_type="NodeSocketColor")
    ng.interface.new_socket("Light", in_out="INPUT", socket_type="NodeSocketColor")
    ng.interface.new_socket("Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    N, L = ng.nodes.new, ng.links.new
    gi, go = N("NodeGroupInput"), N("NodeGroupOutput")
    vals = {}
    for name, v in (("level", 1.0), ("flash", 0.0), ("light_k", LIGHT_K)):
        n = N("ShaderNodeValue")
        n.name = n.label = name
        n.outputs[0].default_value = v
        vals[name] = n

    def scale(src, by):
        s = N("ShaderNodeVectorMath")
        s.operation = "SCALE"
        if isinstance(src, tuple):
            s.inputs[0].default_value = src
        else:
            L(src, s.inputs[0])
        L(by, s.inputs["Scale"])
        return s.outputs[0]

    def add(a, b):
        s = N("ShaderNodeVectorMath")
        s.operation = "ADD"
        L(a, s.inputs[0])
        L(b, s.inputs[1])
        return s.outputs[0]

    out = add(add(scale(gi.outputs["Paint"], vals["level"].outputs[0]), scale(gi.outputs["Light"],
                                                                                vals["light_k"].outputs[0])),
              scale(FLASH_RGB, vals["flash"].outputs[0]))
    L(out, go.inputs["Color"])
    return ng


def _paint(name, color, top=None, noise=0.08, scale=6.0):
    """look.paint() plus the shared lab grade (coloured light, flicker level, lightning flash)."""
    base = hx(color)
    lit = hx(top) if top else tuple(min(1.0, c * 1.25 + 0.04) for c in base[:3]) + (1,)
    m = paintbg.paint3("lab_" + name, tuple(c * 0.8 for c in base[:3]) + (1,), base, lit, cuts=(0.3, 0.62),
                       noise=0.1 + noise, scale=scale)
    m["base"] = hx(color)            # look.outline() derives each material's line colour from this
    nt = m.node_tree
    if "lab_grade" in nt.nodes:
        return m
    em = next(n for n in nt.nodes if n.type == "EMISSION")
    s2r = next(n for n in nt.nodes if n.type == "SHADERTORGB")
    src = em.inputs[0].links[0].from_socket
    g = nt.nodes.new("ShaderNodeGroup")
    g.node_tree = _grade()
    g.name = "lab_grade"
    nt.links.new(src, g.inputs["Paint"])
    nt.links.new(s2r.outputs[0], g.inputs["Light"])
    nt.links.new(g.outputs["Color"], em.inputs[0])
    return m


def _em(m):
    """A material's (first) Emission node: every lab, look.* and pistolshrimp material ends in one."""
    return next((n for n in m.node_tree.nodes if n.type == "EMISSION"), None) if m and m.use_nodes else None


def _glow(name, color, strength=1.0):
    """Unlit glow; strength is keyable (node "Emission", input 1)."""
    return look.flat("lab_" + name, hx(color), strength)


def _gradient(name, bottom, top, strength=1.0, noise=0.0, axis="Z"):
    """Unlit vertical gradient (tank water, the night sky). A 'Flash' mix toward white is keyable for lightning."""
    if "lab_" + name in bpy.data.materials:
        return bpy.data.materials["lab_" + name]
    m = bpy.data.materials.new("lab_" + name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    tc, sep, ramp = N("ShaderNodeTexCoord"), N("ShaderNodeSeparateXYZ"), N("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].color, ramp.color_ramp.elements[1].color = hx(bottom), hx(top)
    L(tc.outputs["Generated"], sep.inputs[0])
    L(sep.outputs[axis], ramp.inputs[0])
    col = ramp.outputs[0]
    if noise:
        nz, mx = N("ShaderNodeTexNoise"), N("ShaderNodeMix")
        nz.inputs["Scale"].default_value = 3.0
        nz.inputs["Detail"].default_value = 4.0
        mx.data_type, mx.blend_type = "RGBA", "OVERLAY"
        mx.inputs["Factor"].default_value = noise
        L(col, mx.inputs[6])
        L(nz.outputs["Color"], mx.inputs[7])
        col = mx.outputs[2]
    fl = N("ShaderNodeMix")
    fl.name = "Flash"
    fl.data_type = "RGBA"
    fl.inputs["Factor"].default_value = 0.0
    fl.inputs[7].default_value = hx("#a9bcff")
    L(col, fl.inputs[6])
    em, out = N("ShaderNodeEmission"), N("ShaderNodeOutputMaterial")
    em.name = "Emission"
    em.inputs[1].default_value = strength
    L(fl.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def _pool(name, loc, size, color, strength=0.5):
    """A painted pool of light on a surface: a soft radial glow decal (no shadows). Keyable: node "Emission"."""
    m = bpy.data.materials.new("lab_pool_" + name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    tc, gr, ramp = N("ShaderNodeTexCoord"), N("ShaderNodeTexGradient"), N("ShaderNodeValToRGB")
    gr.gradient_type = "SPHERICAL"
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.9, (1, 1, 1, 1)
    em, add, out = N("ShaderNodeEmission"), N("ShaderNodeAddShader"), N("ShaderNodeOutputMaterial")
    tr, mix = N("ShaderNodeBsdfTransparent"), N("ShaderNodeMixShader")
    em.name = "Emission"
    em.inputs[0].default_value, em.inputs[1].default_value = hx(color), strength
    L(tc.outputs["Object"], gr.inputs[0])
    L(gr.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], add.inputs[0])
    L(tr.outputs[0], add.inputs[1])
    L(add.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "BLENDED"
    bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1.0, fill_type="NGON", location=loc)
    o = bpy.context.object
    o.name = "pool_" + name
    o.scale = (size[0], size[1], 1)
    o.data.materials.append(m)
    o.visible_shadow = False
    return m


def _water_floor():
    """Spilled water: opaque, shaded in WORLD space so the overlapping puddle discs read as one puddle."""
    if "lab_spill" in bpy.data.materials:
        return bpy.data.materials["lab_spill"]
    m = bpy.data.materials.new("lab_spill")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    geo, nz, ramp = N("ShaderNodeNewGeometry"), N("ShaderNodeTexNoise"), N("ShaderNodeValToRGB")
    nz.inputs["Scale"].default_value = 7.0
    nz.inputs["Detail"].default_value = 2.0
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.38, hx("#3f8cc4")
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.62, hx("#8fe4ff")
    em, out = N("ShaderNodeEmission"), N("ShaderNodeOutputMaterial")
    em.name = "Emission"
    L(geo.outputs["Position"], nz.inputs["Vector"])
    L(nz.outputs["Fac"], ramp.inputs[0])
    L(ramp.outputs[0], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


# ---------------------------------------------------------------- geometry helpers
def _link(o):
    bpy.context.scene.collection.objects.link(o)
    return o


def _box(name, loc, size, mat, line=0.0, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        b = o.modifiers.new("bevel", "BEVEL")
        b.width, b.segments = bevel, 2
    return look.outline(o, line)


def _cyl(name, loc, r, depth, mat, line=0.0, rot=(0, 0, 0), verts=24, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc,
                                        rotation=rot)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = abs(p.normal.z) < 0.5
    return look.outline(o, line)


def _ball(name, loc, scale, mat, seg=14, rot=(0, 0, 0), line=0.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return look.outline(o, line)


def _mesh(name, verts, faces, mat, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    me.materials.append(mat)
    o = _link(bpy.data.objects.new(name, me))
    o.location = loc
    return o


def _cable(name, pts, mat, r=0.008):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = r, 2
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    cu.materials.append(mat)
    return _link(bpy.data.objects.new(name, cu))


def _light(name, kind, loc, rot, energy, color, size=0.1, size_y=None, shadow=True, spot=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy, ld.color, ld.use_shadow = energy, hx(color)[:3], shadow
    if kind == "AREA":
        ld.shape, ld.size, ld.size_y = "RECTANGLE", size, size_y or size
    else:
        ld.shadow_soft_size = size
    if kind == "SPOT":
        ld.spot_size, ld.spot_blend = spot, 0.5
    o = _link(bpy.data.objects.new(name, ld))
    o.location, o.rotation_euler = loc, rot
    return o


def _sun(name, direction, energy, color):
    """A sun shining along `direction`; from outside, only the window lets it in (a window-shaped patch)."""
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy, ld.color, ld.angle = energy, hx(color)[:3], math.radians(1.5)
    o = _link(bpy.data.objects.new(name, ld))
    o.rotation_euler = Vector(direction).to_track_quat("-Z", "Y").to_euler()
    return o


def _aim(loc, target):
    return (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def _cam(name, loc, target, lens, fstop=None, focus=None):
    """A camera aimed at `target`; with `fstop`, DOF focused on `focus` (default: the target)."""
    cd = bpy.data.cameras.new(name)
    cd.lens, cd.clip_start, cd.clip_end = lens, 0.02, 60
    o = _link(bpy.data.objects.new(name, cd))
    o.location = loc
    o.rotation_euler = _aim(loc, target)
    if fstop:
        cd.dof.use_dof, cd.dof.aperture_fstop = True, fstop
        cd.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    return o


# ---------------------------------------------------------------- keyframe helpers
def _interp(idb, path, frame, interp):
    for fc in anim.all_fcurves(idb.animation_data.action):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.01:
                    kp.interpolation = interp


def _ksock(sock, frame, value, interp="LINEAR"):
    """Key a node socket's default_value (works for material and node-group sockets)."""
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)
    _interp(sock.id_data, sock.path_from_id() + ".default_value", frame, interp)


def _kprop(idb, path, frame, value, interp="LINEAR"):
    setattr(idb, path, value)
    idb.keyframe_insert(path, frame=frame)
    _interp(idb, path, frame, interp)


def _cycle(o, path):
    for fc in anim.all_fcurves(o.animation_data.action):
        if fc.data_path == path and not any(m.type == "CYCLES" for m in fc.modifiers):
            fc.modifiers.new("CYCLES")


# ---------------------------------------------------------------- pieces of the room
def _night_world():
    w = bpy.data.worlds.new("lab_night")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = hx("#1b2a4a")
    bg.inputs[1].default_value = 0.28
    return w


def _room(rnd):
    x0, x1, y0, y1, h = ROOM
    wall = _paint("wall", "#34405e", "#46557a", 0.06, 3.0)
    band = _paint("wall_band", "#28314a", "#343f5e", 0.05, 4.0)
    ceil = _paint("ceiling", "#262e45", "#303a55", 0.04)
    grout, tile = _paint("grout", "#0b0f16", noise=0.0), _paint("tile", "#161d29", "#202a3a", 0.1, 2.0)
    # floor: grout slab + a grid of slightly raised tiles (one mesh)
    _box("floor_base", (0, (y0 + y1) / 2, -0.01), (x1 - x0, y1 - y0, 0.02), grout)
    t, g, verts, faces = 0.4, 0.012, [], []
    ys = y0
    while ys < y1 - 0.01:
        xs = x0
        while xs < x1 - 0.01:
            xe, ye = min(xs + t - g, x1), min(ys + t - g, y1)
            sh = rnd.uniform(-0.002, 0.002)
            i = len(verts)
            verts += [(xs + g, ys + g, 0.002 + sh), (xe, ys + g, 0.002 + sh), (xe, ye, 0.002 + sh),
                      (xs + g, ye, 0.002 + sh)]
            faces.append((i, i + 1, i + 2, i + 3))
            xs += t
        ys += t
    _mesh("floor_tiles", verts, faces, tile)
    # back wall with the window hole (x -1.85..-0.55, z 1.05..2.3)
    wx0, wx1, wz0, wz1 = -1.85, -0.55, 1.05, 2.3
    d = 0.12
    yb = y1 + d / 2
    _box("wall_back_l", ((x0 + wx0) / 2, yb, h / 2), (wx0 - x0, d, h), wall)
    _box("wall_back_r", ((wx1 + x1) / 2, yb, h / 2), (x1 - wx1, d, h), wall)
    _box("wall_back_b", ((wx0 + wx1) / 2, yb, wz0 / 2), (wx1 - wx0, d, wz0), wall)
    _box("wall_back_t", ((wx0 + wx1) / 2, yb, (wz1 + h) / 2), (wx1 - wx0, d, h - wz1), wall)
    _box("wall_left", (x0 - d / 2, (y0 + y1) / 2, h / 2), (d, y1 - y0, h), wall)
    _box("wall_right", (x1 + d / 2, (y0 + y1) / 2, h / 2), (d, y1 - y0, h), wall)
    _box("wall_front", (0, y0 - d / 2, h / 2), (x1 - x0, d, h), wall)
    _box("ceiling", (0, (y0 + y1) / 2, h + 0.03), (x1 - x0, y1 - y0, 0.06), ceil)
    # darker lower wall band + skirting, the painted-lab look
    for nm, loc, size in (("band_back", (0, y1 - 0.01, 0.45), (x1 - x0, 0.02, 0.9)),
                          ("band_left", (x0 + 0.01, (y0 + y1) / 2, 0.45), (0.02, y1 - y0, 0.9)),
                          ("band_right", (x1 - 0.01, (y0 + y1) / 2, 0.45), (0.02, y1 - y0, 0.9))):
        _box(nm, loc, size, band)
    skirt = _paint("skirt", "#1a2030", noise=0.0)
    _box("skirt_back", (0, y1 - 0.025, 0.05), (x1 - x0, 0.03, 0.1), skirt)
    _box("skirt_left", (x0 + 0.025, (y0 + y1) / 2, 0.05), (0.03, y1 - y0, 0.1), skirt)
    _box("skirt_right", (x1 - 0.025, (y0 + y1) / 2, 0.05), (0.03, y1 - y0, 0.1), skirt)
    # ceiling light fixture: housing + tube (the tube's glow is keyed by flicker / power_out)
    _box("fixture", (0.1, 0.2, h - 0.04), (1.3, 0.22, 0.07), _paint("fixture", "#4a5670", noise=0.0))
    tube = _box("fixture_tube", (0.1, 0.2, h - 0.08), (1.2, 0.14, 0.012), _glow("tube", "#dff3ff", 1.1))
    # left wall: a species chart; right wall: a whiteboard with notes
    _box("chart", (x0 + 0.03, 0.6, 1.6), (0.02, 1.0, 0.7), _paint("chart", "#c9d3e6", "#e3eaf7", 0.03))
    chart_cols = ["#e07a5f", "#f2cc8f", "#81b29a", "#3d5a80", "#e5989b", "#98c1d9"]
    for i in range(6):
        _ball(f"chart_fish{i}", (x0 + 0.045, 0.25 + (i % 3) * 0.33, 1.75 - (i // 3) * 0.3), (0.006, 0.11, 0.045),
              _paint(f"chartc{i}", chart_cols[i], noise=0.0), 10)
    _box("board", (x1 - 0.03, 0.2, 1.55), (0.02, 1.6, 0.9), _paint("board", "#7d89a3", "#98a4bd", 0.03))
    ink = [_paint("ink_b", "#3a5fa8", noise=0.0), _paint("ink_r", "#c0504d", noise=0.0)]
    for i in range(7):
        w = rnd.uniform(0.25, 0.9)
        _box(f"note{i}", (x1 - 0.042, -0.45 + w / 2 + rnd.uniform(0, 0.2), 1.85 - i * 0.1), (0.004, w, 0.018),
             ink[i % 5 == 0])
    return dict(tube=tube.data.materials[0])


def _window(rnd):
    """Window over the desk: frame, glass with sliding raindrops, falling rain outside, campus silhouettes and a stormy
    sky that flashes for lightning (plus a bolt that only shows on flash frames)."""
    wx0, wx1, wz0, wz1, y = -1.85, -0.55, 1.05, 2.3, WALL_Y
    frame_m = _paint("window_frame", "#5d6a86", "#7684a3", 0.03)
    t = 0.05
    for nm, loc, size in (("win_l", (wx0 + t / 2, y, (wz0 + wz1) / 2), (t, 0.14, wz1 - wz0)),
                          ("win_r", (wx1 - t / 2, y, (wz0 + wz1) / 2), (t, 0.14, wz1 - wz0)),
                          ("win_b", ((wx0 + wx1) / 2, y, wz0 + t / 2), (wx1 - wx0, 0.14, t)),
                          ("win_t", ((wx0 + wx1) / 2, y, wz1 - t / 2), (wx1 - wx0, 0.14, t)),
                          ("win_mid", ((wx0 + wx1) / 2, y, (wz0 + wz1) / 2), (0.035, 0.1, wz1 - wz0)),
                          ("win_bar", ((wx0 + wx1) / 2, y, wz0 + (wz1 - wz0) * 0.62), (wx1 - wx0, 0.1, 0.03))):
        _box(nm, loc, size, frame_m)
    _box("win_sill", ((wx0 + wx1) / 2, y - 0.09, wz0 - 0.015), (wx1 - wx0 + 0.16, 0.2, 0.03), frame_m)
    glass = look.fade("lab_glass", hx("#9cc4ff"), 0.1)
    _box("win_glass", ((wx0 + wx1) / 2, y + 0.01, (wz0 + wz1) / 2), (wx1 - wx0, 0.004, wz1 - wz0), glass)
    # the sky outside (a big gradient card) and dark campus buildings with a few lit windows
    sky = _gradient("sky", "#2a3a6a", "#0b1230", 1.0, noise=0.25)
    _box("sky", (-1.2, 9.0, 2.5), (14, 0.1, 9), sky)
    bld = _paint("building", "#0e1428", noise=0.0)
    lit = _glow("lit_window", "#ffcf7a", 1.2)
    for i in range(6):
        bx, bw, bh = -4.2 + i * 1.3 + rnd.uniform(-0.3, 0.3), rnd.uniform(0.8, 1.6), rnd.uniform(0.5, 1.5)
        by = 7.9 + rnd.uniform(0, 0.5)
        _box(f"bldg{i}", (bx, by, bh / 2), (bw, 0.6, bh), bld)
        for j in range(rnd.randint(1, 3)):
            _box(f"bldg{i}_w{j}", (bx + rnd.uniform(-bw / 3, bw / 3), by - 0.31, rnd.uniform(0.4, bh - 0.3)),
                 (0.12, 0.01, 0.09), lit)
    for i in range(9):
        _ball(f"tree_sil{i}", (-4 + i * 0.9 + rnd.uniform(-0.2, 0.2), 7.6, rnd.uniform(0.1, 0.4)),
              (rnd.uniform(0.5, 0.8), 0.4, rnd.uniform(0.5, 0.8)), bld, 10)
    # falling rain: two stacked copies of a streak field, slid down one period and cycled (seamless loop)
    def streaks(name, n, yy, length, alpha, period, x_rng, z_rng, seed):
        r = random.Random(seed)
        H = z_rng[1] - z_rng[0]
        verts, faces = [], []
        for c in (0, 1):
            for _ in range(n):
                x, z = r.uniform(*x_rng), r.uniform(*z_rng) + c * H
                w, dx = 0.004, -0.08 * length          # slanted by the wind
                i = len(verts)
                verts += [(x, yy, z), (x + w, yy, z), (x + w + dx, yy, z + length), (x + dx, yy, z + length)]
                faces.append((i, i + 1, i + 2, i + 3))
        o = _mesh(name, verts, faces, look.fade(f"lab_{name}_m", hx("#b9d4ff"), alpha))
        anim.key(o, "location", 0, (0, 0, 0), "LINEAR")
        anim.key(o, "location", period, (-0.08 * H, 0, -H), "LINEAR")
        _cycle(o, "location")
        return o
    streaks("rain_near", 70, y + 0.35, 0.22, 0.55, 10, (wx0 - 0.4, wx1 + 0.4), (wz0 - 0.4, wz1 + 0.4), 11)
    streaks("rain_far", 110, y + 1.6, 0.3, 0.3, 14, (wx0 - 1.2, wx1 + 1.2), (wz0 - 0.8, wz1 + 1.2), 12)
    # drops running down the glass (slow), plus a few short static trails
    r = random.Random(13)
    verts, faces = [], []
    H = wz1 - wz0
    for c in (0, 1):
        for _ in range(26):
            x, z, ln = r.uniform(wx0 + 0.07, wx1 - 0.07), r.uniform(wz0, wz1) + c * H, r.uniform(0.03, 0.12)
            i = len(verts)
            verts += [(x, 0, z), (x + 0.006, 0, z), (x + 0.006, 0, z + ln), (x, 0, z + ln)]
            faces.append((i, i + 1, i + 2, i + 3))
    # on the outside of the glass, inside the wall's thickness, so the window opening clips them
    drops = _mesh("glass_drops", verts, faces, look.fade("lab_drop_m", hx("#d8ebff"), 0.6), (0, y + 0.02, 0))
    anim.key(drops, "location", 0, (0, y + 0.02, 0), "LINEAR")
    anim.key(drops, "location", 96, (0, y + 0.02, -H), "LINEAR")
    _cycle(drops, "location")
    # lightning bolt: a jagged ribbon in the sky, alpha keyed by lightning()
    pts, x, z = [], -1.0, 4.6
    while z > 1.4:
        pts.append((x, z))
        x += r.uniform(-0.35, 0.35)
        z -= r.uniform(0.25, 0.45)
    verts, faces = [], []
    for i, ((xa, za), (xb, zb)) in enumerate(zip(pts, pts[1:])):
        k = len(verts)
        w = 0.05 * (1 - i / len(pts)) + 0.015
        verts += [(xa - w, 0, za), (xa + w, 0, za), (xb + w, 0, zb), (xb - w, 0, zb)]
        faces.append((k, k + 1, k + 2, k + 3))
    bolt = _mesh("bolt", verts, faces, look.fade("lab_bolt_m", hx("#f4f8ff"), 0.0), (0, 8.8, 0))
    return dict(sky=sky, bolt=bolt.data.materials[0])


def _tank(name, center, size, glow, rnd):
    """An aquarium: glowing back/side water panels, gravel, plants, rocks, fish, rising bubbles, a visible water
    surface with a bright waterline, a tinted front pane with highlight streaks, dark rims and a lit hood."""
    cx, cy, cz = center            # cz = bottom of the tank
    w, d, h = size
    wl = cz + h * 0.88             # water line
    deep = {"cyan": ("#0f4f86", "#56d6ff"), "teal": ("#0e5a63", "#4fe8cf"), "blue": ("#143a86", "#6aa8ff"),
            "violet": ("#2a2f86", "#8f9cff")}[glow]
    back = _gradient(f"water_{name}", deep[0], deep[1], 1.0)
    side = _gradient(f"waterside_{name}", deep[0], deep[1], 0.55)
    rim = _paint("tank_rim", "#141a26", "#222b3c", 0.0)
    _box(f"{name}_back", (cx, cy + d / 2 - 0.01, cz + (wl - cz) / 2), (w - 0.02, 0.01, wl - cz), back)
    for s in (-1, 1):
        _box(f"{name}_side{s}", (cx + s * (w / 2 - 0.012), cy, cz + (wl - cz) / 2), (0.01, d - 0.02, wl - cz), side)
    _box(f"{name}_gravel", (cx, cy, cz + 0.035), (w - 0.03, d - 0.03, 0.06), _paint("gravel", "#b8a98a", "#d8cfb4",
                                                                                       0.25, 30.0))
    surf = look.fade(f"lab_surface_{name}", hx(deep[1]), 0.55)
    _box(f"{name}_surface", (cx, cy, wl), (w - 0.02, d - 0.02, 0.004), surf)
    _box(f"{name}_waterline", (cx, cy - d / 2 + 0.008, wl - 0.004), (w - 0.03, 0.004, 0.008),
         _glow("waterline", "#e9fbff", 1.3))
    # rims, corner posts and the hood
    for z in (cz + 0.012, cz + h - 0.012):
        _box(f"{name}_rim{z:.2f}", (cx, cy, z), (w + 0.02, d + 0.02, 0.025), rim)
    for sx in (-1, 1):
        for sy in (-1, 1):
            _box(f"{name}_post{sx}{sy}", (cx + sx * w / 2, cy + sy * d / 2, cz + h / 2), (0.016, 0.016, h), rim)
    _box(f"{name}_hood", (cx, cy, cz + h + 0.025), (w + 0.03, d + 0.03, 0.05), rim)
    # plants and rocks
    greens = [_paint("plant0", "#2f9e6e", "#56c98d", 0.1), _paint("plant1", "#5cbf4a", "#8de070", 0.1),
              _paint("plant2", "#1f7f6a", "#3fae8f", 0.1)]
    rock = _paint("tank_rock", "#6c7488", "#8f98ad", 0.12)
    for i in range(rnd.randint(5, 8)):
        px = cx + rnd.uniform(-w / 2 + 0.05, w / 2 - 0.05)
        ph = rnd.uniform(0.35, 0.8) * (wl - cz)
        _cyl(f"{name}_plant{i}", (px, cy + rnd.uniform(0, d / 3), cz + 0.06 + ph / 2), rnd.uniform(0.018, 0.035), ph,
             rnd.choice(greens), verts=6, r2=0.002, rot=(rnd.uniform(-0.15, 0.15), rnd.uniform(-0.15, 0.15), 0))
    for i in range(2):
        s = rnd.uniform(0.04, 0.07)
        rx = cx + rnd.uniform(-w / 2.5, w / 2.5)
        _ball(f"{name}_rock{i}", (rx, cy + rnd.uniform(0, d / 4), cz + 0.065), (s * 1.3, s, s * 0.8), rock, 10)
    # fish swimming back and forth
    fish_cols = ["#ff9f45", "#ffd85e", "#ff6f91", "#7ae7ff"]
    for i in range(rnd.randint(2, 3)):
        fm = _paint(f"fish{i % 4}", fish_cols[i % 4], noise=0.0)
        fz = rnd.uniform(cz + 0.15, wl - 0.07)
        fy = cy + rnd.uniform(-d / 5, d / 5)
        body = _ball(f"{name}_fish{i}", (0, 0, 0), (0.045, 0.014, 0.028), fm, 12)
        tail = _cyl(f"{name}_fish{i}_tail", (-0.05, 0, 0), 0.022, 0.03, fm, rot=(0, math.radians(90), 0), verts=4,
                    r2=0.0)
        tail.scale = (1, 0.3, 1)
        tail.parent = body
        xa, xb = cx - w / 2 + 0.08, cx + w / 2 - 0.08
        P, t0 = rnd.randint(140, 220), -rnd.randint(0, 200)
        anim.key(body, "location", t0, (xa, fy, fz), "BEZIER")
        anim.key(body, "location", t0 + P // 2, (xb, fy, fz + rnd.uniform(-0.03, 0.03)), "BEZIER")
        anim.key(body, "location", t0 + P, (xa, fy, fz), "BEZIER")
        anim.key(body, "rotation_euler", t0, (0, 0, 0), "CONSTANT")
        anim.key(body, "rotation_euler", t0 + P // 2, (0, 0, math.pi), "CONSTANT")
        anim.key(body, "rotation_euler", t0 + P, (0, 0, 0), "CONSTANT")
        _cycle(body, "location")
        _cycle(body, "rotation_euler")
    # bubbles from an air stone in the back corner
    bub = _glow("bubble", "#e6fbff", 1.4)
    bx = cx - w / 2 + 0.06
    _ball(f"{name}_airstone", (bx, cy + d / 4, cz + 0.08), (0.02, 0.02, 0.015), rock, 8)
    for i in range(7):
        s = rnd.uniform(0.005, 0.011)
        b = _ball(f"{name}_bubble{i}", (bx, cy + d / 4, cz + 0.1), (s, s, s), bub, 8)
        P, t0 = rnd.randint(40, 64), -rnd.randint(0, 60)
        dx = rnd.uniform(-0.015, 0.015)
        anim.key(b, "location", t0, (bx + dx, cy + d / 4, cz + 0.1), "LINEAR")
        anim.key(b, "location", t0 + P, (bx - dx * 2, cy + d / 4, wl - 0.006), "LINEAR")
        _cycle(b, "location")
    # front pane: faint tint + two diagonal highlight streaks (painted glass)
    glass = look.fade(f"lab_tankglass_{name}", hx(deep[1]), 0.08)
    front = _box(f"{name}_glass", (cx, cy - d / 2, cz + h / 2), (w, 0.004, h), glass)
    hl = look.fade("lab_glass_hl", hx("#ffffff"), 0.14)
    for i, (u, ww) in enumerate(((0.16, 0.022), (0.22, 0.008))):
        _box(f"{name}_hl{i}", (cx - w / 2 + w * u, cy - d / 2 - 0.004, cz + h * 0.6), (ww, 0.002, h * 0.5), hl,
             rot=(0, math.radians(-28), 0))
    # hood light shining down into the water (no shadows: it's inside the tank)
    _light(f"{name}_hood_light", "AREA", (cx, cy, cz + h - 0.02), (0, 0, 0), 6.0 * w, deep[1], w * 0.9, d * 0.8,
           shadow=False)
    return dict(water=[back, side], surface=surf, glass=front, hood=bpy.data.objects[f"{name}_hood_light"],
                floor=(cx, cy, cz + 0.065), inner=(w - 0.03, d - 0.03, wl - cz - 0.065), waterline=wl,
                leak=(cx - w * 0.15, cy - d / 2 - 0.01, cz + 0.02))


def _shelf_and_tanks(rnd):
    metal = _paint("shelf_metal", "#3c475f", "#56637f", 0.04)
    x0, x1, yc, dd = 0.75, 2.35, WALL_Y - 0.25, 0.46
    for x in (x0, x1):
        for y in (yc - dd / 2, yc + dd / 2):
            _box(f"shelf_post{x}{y}", (x, y, 1.2), (0.035, 0.035, 2.4), metal)
    planks = (0.12, 0.88, 1.62, 2.36)
    for i, z in enumerate(planks):
        _box(f"shelf_plank{i}", ((x0 + x1) / 2, yc, z), (x1 - x0 + 0.05, dd + 0.02, 0.03), metal)
    tanks = [_tank("tankA", (1.55, yc, planks[0] + 0.015), (1.38, 0.4, 0.6), "cyan", rnd),
             _tank("tankB", (1.16, yc, planks[1] + 0.015), (0.66, 0.34, 0.5), "teal", rnd),
             _tank("tankC", (1.95, yc, planks[1] + 0.015), (0.66, 0.34, 0.5), "blue", rnd),
             _tank("tankD", (1.18, yc, planks[2] + 0.015), (0.56, 0.3, 0.42), "violet", rnd)]
    # specimen jars and boxes on the top shelves
    jar_cols = ["#9fd4a8", "#f2c879", "#c7a3e6", "#8cc9e8"]
    lid = _paint("jar_lid", "#2c3446", noise=0.0)
    for i in range(4):
        jx = 1.68 + i * 0.16
        jh = rnd.uniform(0.18, 0.3)
        _cyl(f"jar{i}", (jx, yc, planks[2] + 0.015 + jh / 2), 0.055, jh, _paint(f"jar{i}", jar_cols[i], noise=0.06))
        _cyl(f"jar{i}_lid", (jx, yc, planks[2] + 0.025 + jh), 0.058, 0.025, lid)
    for i in range(3):
        bw = rnd.uniform(0.3, 0.45)
        _box(f"box{i}", (0.98 + i * 0.48, yc, planks[3] + 0.015 + 0.13), (bw, 0.36, 0.26),
             _paint(f"box{i}", ["#6b5a4a", "#4f5f78", "#7a6a55"][i], noise=0.1), bevel=0.01)
    # one cool glow light per tank shelf, facing the room (tints the floor, chair and desk cyan)
    glow = [_light("shelf_glow_low", "AREA", (1.55, yc - 0.32, 0.55), (math.radians(-40), 0, 0), 30, "#56d6ff", 1.3,
                   0.5),
            _light("shelf_glow_mid", "AREA", (1.55, yc - 0.32, 1.2), (math.radians(-50), 0, 0), 20, "#5ec8ff", 1.4,
                   0.4)]
    return tanks, glow


def _cabinet(rnd):
    """A low lab cabinet between the desk and the shelf, with the microscope and a book stack on top."""
    cab = _paint("cabinet", "#3a3f57", "#4d5472", 0.05)
    sx, sy, sw, sd, sh = 0.1, WALL_Y - 0.27, 0.72, 0.5, 0.72
    _box("cabinet", (sx, sy, sh / 2), (sw, sd, sh), cab, bevel=0.008)
    knob = _paint("knob", "#9aa3b8", noise=0.0)
    _box("cabinet_door", (sx, sy - sd / 2 - 0.004, sh / 2 + 0.02), (sw - 0.06, 0.008, sh - 0.12), cab)
    _cyl("cabinet_knob", (sx + sw / 2 - 0.08, sy - sd / 2 - 0.015, sh * 0.62), 0.012, 0.02, knob,
         rot=(math.radians(90), 0, 0), verts=12)
    for i, c in enumerate(("#3d6b8f", "#8f5a3d", "#4f7a4a")):
        _box(f"book{i}", (sx + 0.17, sy + 0.05, sh + 0.02 + i * 0.035), (0.26 - i * 0.02, 0.19, 0.033),
             _paint(f"book{i}", c, noise=0.05), rot=(0, 0, math.radians(rnd.uniform(-8, 8))))
    scope = _paint("scope", "#e5e9f2", "#ffffff", 0.03)
    tube = _paint("scope_tube", "#3d4458", noise=0.0)
    mx, my = sx - 0.15, sy - 0.02
    _box("scope_base", (mx, my, sh + 0.015), (0.14, 0.18, 0.03), scope, bevel=0.008)
    _box("scope_arm", (mx, my + 0.06, sh + 0.12), (0.04, 0.04, 0.2), scope, bevel=0.01)
    _cyl("scope_tube", (mx, my + 0.01, sh + 0.2), 0.022, 0.16, tube, rot=(math.radians(-25), 0, 0))
    _box("scope_stage", (mx, my - 0.01, sh + 0.09), (0.11, 0.09, 0.008), tube)


def _desk(rnd):
    wood = _paint("desk_top", "#5b4a5e", "#76627a", 0.06, 3.0)
    side = _paint("desk_side", "#433a4f", "#574b66", 0.05)
    x0, x1, y0, y1, top = -2.05, -0.4, WALL_Y - 0.72, WALL_Y - 0.02, 0.75
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    _box("desk_top", (cx, cy, top - 0.02), (x1 - x0, y1 - y0, 0.04), wood, line=0.004, bevel=0.006)
    _box("desk_leg_l", (x0 + 0.03, cy, (top - 0.04) / 2), (0.04, y1 - y0 - 0.04, top - 0.04), side)
    _box("desk_drawers", (x1 - 0.22, cy, (top - 0.04) / 2), (0.4, y1 - y0 - 0.06, top - 0.04), side, bevel=0.006)
    knob = _paint("knob", "#9aa3b8", noise=0.0)
    for i in range(3):
        _box(f"drawer_handle{i}", (x1 - 0.22, y0 + 0.025, 0.6 - i * 0.22), (0.12, 0.015, 0.015), knob)
    _box("desk_modesty", (cx - 0.2, y1 - 0.06, 0.45), (x1 - x0 - 0.5, 0.02, 0.45), side)
    # laptop: base + lid opened ~110 degrees, glowing screen with a few UI bars (the night-shift data sheet)
    shell = _paint("laptop", "#a7afc4", "#c9d0e2", 0.03)
    lx, ly = cx - 0.22, cy - 0.04
    _box("laptop_base", (lx, ly, top + 0.009), (0.36, 0.25, 0.016), shell, line=0.003, bevel=0.004)
    _box("laptop_keys", (lx, ly + 0.02, top + 0.0175), (0.3, 0.12, 0.002), _paint("keys", "#4a5164", noise=0.0))
    tilt = math.radians(-18)
    hinge = Vector((lx, ly + 0.125, top + 0.017))
    up = Vector((0, -math.sin(tilt), math.cos(tilt)))
    lid_c = hinge + up * 0.115
    _box("laptop_lid", tuple(lid_c), (0.36, 0.012, 0.23), shell, line=0.003, rot=(tilt, 0, 0), bevel=0.004)
    screen = _glow("screen", "#bfe0ff", 1.15)
    nrm = Vector((0, -math.cos(tilt), -math.sin(tilt)))
    _box("laptop_screen", tuple(lid_c + nrm * 0.0065), (0.33, 0.002, 0.2), screen, rot=(tilt, 0, 0))
    ui = [_glow("ui0", "#5b8fd6", 1.0), _glow("ui1", "#7fd6c2", 1.0), _glow("ui2", "#ffb36b", 1.0)]
    for i, (ox, oz, ww) in enumerate(((-0.08, 0.06, 0.12), (-0.08, 0.035, 0.09), (-0.08, 0.01, 0.13),
                                      (0.08, -0.05, 0.1), (-0.05, -0.06, 0.06))):
        p = lid_c + nrm * 0.008 + Vector((ox, 0, 0)) + up * oz
        _box(f"ui{i}", tuple(p), (ww, 0.001, 0.012), ui[i % 3], rot=(tilt, 0, 0))
    # open notebook + pen (under the lamp) at the left end, a mug between the laptop and the tank
    page = _paint("page", "#e9e2cf", "#f6f1e3", 0.04)
    nx, ny = x0 + 0.33, cy - 0.1
    for s in (-1, 1):
        _box(f"notebook_page{s}", (nx + s * 0.085, ny, top + 0.006), (0.16, 0.22, 0.008), page,
             rot=(0, s * math.radians(-3), math.radians(8)))
    lines = _paint("page_line", "#9fb0cc", noise=0.0)
    for i in range(6):
        _box(f"nb_line{i}", (nx + 0.085, ny + 0.08 - i * 0.03, top + 0.0105), (0.12, 0.004, 0.0005), lines,
             rot=(0, 0, math.radians(8)))
    _cyl("pen", (nx + 0.02, ny - 0.13, top + 0.006), 0.005, 0.14, _paint("pen", "#2f5fb3", noise=0.0),
         rot=(0, math.radians(90), math.radians(30)), verts=8)
    mug_m = _paint("mug", "#d96c5a", "#f08a76", 0.04)
    mx_, my_ = cx + 0.13, cy - 0.21
    _cyl("mug", (mx_, my_, top + 0.05), 0.04, 0.1, mug_m, line=0.002)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.025, minor_radius=0.007,
                                     location=(mx_ + 0.045, my_, top + 0.05), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(mug_m)
    # the lamp at the back-left corner: base, two arm segments, a shade aimed at the notebook, bulb and spot light
    lampm = _paint("lamp", "#e3b04b", "#f5cd6e", 0.04)
    bx, by = x0 + 0.14, cy + 0.22
    _cyl("lamp_base", (bx, by, top + 0.012), 0.065, 0.024, lampm, line=0.002)
    a = Vector((bx, by, top + 0.02))
    b = Vector((bx + 0.03, by - 0.02, top + 0.38))
    c = Vector((bx + 0.13, by - 0.22, top + 0.44))
    for nm, p, q in (("lamp_arm0", a, b), ("lamp_arm1", b, c)):
        dvec = q - p
        o = _cyl(nm, tuple((p + q) / 2), 0.009, dvec.length, lampm, verts=10)
        o.rotation_euler = dvec.to_track_quat("Z", "Y").to_euler()
    aim = (Vector((nx, ny, top)) - c).normalized()
    shade = _cyl("lamp_shade", tuple(c + aim * 0.05), 0.085, 0.11, lampm, verts=24, r2=0.03)
    shade.rotation_euler = (-aim).to_track_quat("Z", "Y").to_euler()     # the wide end (-Z) faces the notebook
    for p in shade.data.polygons:
        p.use_smooth = True
    bulb_m = _glow("bulb", "#fff1c9", 2.0)
    _ball("lamp_bulb", tuple(c + aim * 0.085), (0.03, 0.03, 0.03), bulb_m, 12)
    lamp = _light("lamp_light", "SPOT", tuple(c + aim * 0.07), aim.to_track_quat("-Z", "Y").to_euler(), 90, "#ffd28a",
                  0.04, spot=math.radians(110))
    pool = _pool("lamp", (nx + 0.02, ny + 0.02, top + 0.0005), (0.42, 0.32), "#ffb85c", 0.35)
    # the slot for the pistol shrimp's tank (mk/pistolshrimp.tank(), helper 2) on the right of the desk, within reach
    # of Kai's right hand (S04a: he taps the glass). place_tank() scales that tank (12.3 x 6.45 x 5.6 units) to fit.
    sw, sd = 0.56, 0.3
    slot_c = Vector((x1 - 0.36, cy + 0.05, top))
    s_ = sw / 12.3
    bpy.ops.object.empty_add(type="CUBE", location=tuple(slot_c + Vector((0, 0, 0.13))))
    slot_e = bpy.context.object
    slot_e.name = "shrimp_tank_slot"
    slot_e.scale = (sw / 2, sd / 2, 0.13)
    glow = _light("tank_glow", "AREA", (slot_c.x, slot_c.y - 0.4, top + 0.28), (math.radians(-50), 0, 0), 14,
                  "#7fd0dc", 0.55, 0.3, shadow=False)
    hood = _light("tank_hood", "AREA", (slot_c.x, slot_c.y, top + 0.2), (0, 0, 0), 0.0, "#bff2ff", sw * 0.85,
                  sd * 0.8, shadow=False)  # lights the placed tank's sand and plants from above; place_tank turns it on
    slot = dict(empty=slot_e, center=tuple(slot_c), size=(sw, sd, 0.26), scale=s_,
                root_loc=(slot_c.x, slot_c.y - 0.5 * s_, top + 0.73 * s_), glow=glow, hood=hood,
                leak=(slot_c.x - 0.07, slot_c.y - sd / 2 - 0.005, top + 0.004))
    return dict(screen=screen, bulb=bulb_m, lamp=lamp, pool=pool, top=top, seat=(cx + 0.05, y0 - 0.55, 0.5),
                charger=(lx + 0.2, ly + 0.1, top), slot=slot, front_y=y0, x=(x0, x1), center=(cx, cy, top),
                laptop=(lx, ly, top))


def _chair(seat):
    fab = _paint("chair", "#2c3550", "#3e4a6e", 0.05)
    blk = _paint("chair_base", "#1b2030", noise=0.0)
    sx, sy, sz = seat
    _box("chair_seat", (sx, sy, sz - 0.03), (0.46, 0.44, 0.07), fab, line=0.002, bevel=0.02)
    _box("chair_back", (sx, sy - 0.24, sz + 0.27), (0.42, 0.05, 0.4), fab, line=0.002, bevel=0.02,
         rot=(math.radians(-8), 0, 0))
    _box("chair_spine", (sx, sy - 0.25, sz + 0.02), (0.05, 0.03, 0.18), blk)
    _cyl("chair_pole", (sx, sy, (sz - 0.06) / 2 + 0.04), 0.025, sz - 0.12, blk, verts=12)
    for i in range(5):
        a = i / 5 * 2 * math.pi + 0.3
        _box(f"chair_leg{i}", (sx + math.cos(a) * 0.16, sy + math.sin(a) * 0.16, 0.06), (0.3, 0.035, 0.03), blk,
             rot=(0, 0, a))
        _ball(f"chair_wheel{i}", (sx + math.cos(a) * 0.3, sy + math.sin(a) * 0.3, 0.025), (0.025, 0.025, 0.025), blk,
              10)
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(sx, sy, sz))
    e = bpy.context.object
    e.name = "kai_seat"
    # one root at the floor under the pole, so a shot can swivel the chair (rotation z) or roll it
    parts = [o for o in bpy.context.scene.objects if o.name.startswith("chair_")] + [e]
    root = _link(bpy.data.objects.new("chair_root", None))
    root.location = (sx, sy, 0)
    bpy.context.view_layer.update()
    for o in parts:
        o.parent = root
        o.matrix_parent_inverse = root.matrix_world.inverted()
    return root, e


def _power_strip(desk):
    """Power strip on the floor by the desk's right end, plugs and cables to the desk tank, laptop, shelf and wall."""
    body_m = _paint("strip", "#d7dbe4", "#eef1f6", 0.03)
    dark = _paint("socket", "#262a33", noise=0.0)
    cable = _paint("cable", "#1e222b", "#2c313c", 0.0)
    px, py, rz = -0.1, 1.32, math.radians(-14)
    strip = _box("power_strip", (px, py, 0.024), (0.44, 0.075, 0.042), body_m, line=0.0015, rot=(0, 0, rz),
                 bevel=0.008)
    ax = Vector((math.cos(rz), math.sin(rz), 0))
    plugs = []
    for i in range(4):
        p = Vector((px, py, 0.046)) + ax * (-0.12 + i * 0.075)
        _box(f"socket{i}", tuple(p), (0.03, 0.03, 0.004), dark, rot=(0, 0, rz))
        if i < 3:
            plugs.append(_box(f"plug{i}", tuple(p + Vector((0, 0, 0.018))), (0.034, 0.034, 0.034),
                              _paint("plug", "#2b2f3a", noise=0.0), line=0.0012, rot=(0, 0, rz), bevel=0.004))
    sw = Vector((px, py, 0.047)) + ax * 0.19
    _box("strip_switch", tuple(sw), (0.03, 0.03, 0.01), _glow("switch", "#ff5a4a", 1.4), rot=(0, 0, rz))
    # cords: strip -> the desk tank's filter, strip -> laptop charger (under the desk), strip -> shelf, strip -> wall
    p0, p1, p2 = (Vector(plugs[i].location) + Vector((0, 0, 0.02)) for i in range(3))
    top = desk["top"]
    sx_, sy_, _ = desk["slot"]["center"]
    _cable("cord_tank", [tuple(p0), (-0.25, 1.6, 0.008), (-0.36, 2.1, 0.008), (-0.42, WALL_Y - 0.04, 0.05),
                         (-0.42, WALL_Y - 0.04, top - 0.03), (sx_ + 0.22, sy_ + 0.18, top + 0.01)], cable)
    dx, dy, dz = desk["charger"]
    _cable("cord_desk", [tuple(p1), (-0.5, 1.62, 0.008), (-0.95, 2.15, 0.008), (-1.05, WALL_Y - 0.04, 0.05),
                         (-1.05, WALL_Y - 0.04, dz - 0.03), (dx, dy, dz + 0.005)], cable)
    _cable("cord_shelf", [tuple(p2), (0.35, 1.45, 0.008), (0.85, 2.0, 0.008), (0.82, WALL_Y - 0.03, 0.06),
                          (0.82, WALL_Y - 0.03, 1.3)], cable)
    _cable("cord_wall", [tuple(Vector((px, py, 0.024)) + ax * 0.23), (0.6, 1.1, 0.008), (1.6, 1.35, 0.008),
                         (2.47, 1.5, 0.05), (2.47, 1.5, 0.3)], cable)
    _box("wall_outlet", (2.49, 1.5, 0.32), (0.02, 0.08, 0.12), body_m)
    end = Vector((px, py, 0.0)) - ax * 0.23      # the end nearest the desk, where the water arrives
    return strip, end, Vector((px, py, 0.105)) - ax * 0.13 + Vector((0, -0.06, 0))   # in front of the end plug


# ---------------------------------------------------------------- the set
def build(seed=7):
    """Build the lab into the current scene and return handles (cameras, lights, tank slot, effect functions)."""
    rnd = random.Random(seed)
    _night_world()
    room = _room(rnd)
    win = _window(rnd)
    tanks, shelf_glow = _shelf_and_tanks(rnd)
    _cabinet(rnd)
    desk = _desk(rnd)
    slot = desk["slot"]
    chair, seat = _chair(desk["seat"])
    strip, strip_end, spark_at = _power_strip(desk)

    h = ROOM[4]
    ceiling = _light("ceiling_light", "AREA", (0.1, 0.2, h - 0.1), (0, 0, 0), 40, "#cfe4ff", 1.2, 0.16)
    moon = _sun("window_light", (0.25, -0.8, -0.55), 2.6, "#7f9cff")
    strike = _sun("lightning_light", (0.35, -0.85, -0.42), 0.0, "#d4e0ff")
    spark_l = _light("spark_light", "POINT", tuple(spark_at + Vector((0, -0.1, 0.25))), (0, 0, 0), 0.0, "#e8f3ff", 0.03)
    spark_l.data.use_custom_distance, spark_l.data.cutoff_distance = True, 1.4
    grade = _grade()

    sx, sy, _ = desk["seat"]
    head = (sx, sy, 1.25)                 # Kai's head when seated
    cams = dict(                          # see EP01_SHOTS.md: S03 medium, S07 window, S09/S10 floor
        wide=_cam("cam_wide", (-1.6, -1.45, 1.5), (0.25, 2.1, 0.9), 16),
        desk=_cam("cam_desk", (-0.6, 0.45, 1.45), (-1.1, 2.15, 0.88), 27, fstop=1.0, focus=desk["laptop"]),
        medium=_cam("cam_medium", (-2.05, -0.15, 1.12), (-0.3, 1.95, 0.98), 32, fstop=0.6, focus=head),
        window=_cam("cam_window", (-1.05, 0.3, 1.45), (-1.15, 2.5, 1.3), 24),
        floor=_cam("cam_floor", FLOOR_CAM, FLOOR_AIM, 24, fstop=0.6, focus=tuple(strip_end)),
    )
    room_lights = [ceiling, desk["lamp"]]
    room_glows = [(room["tube"], 1.1), (desk["bulb"], 2.0), (desk["pool"], 0.35)]
    tank_lights = [t["hood"] for t in tanks] + shelf_glow + [slot["glow"], slot["hood"]]
    spill_m = _water_floor()
    tank_glows = [(m, _em(m).inputs[1].default_value) for t in tanks for m in t["water"]]
    slot_glows = []              # the placed shrimp tank's materials (place_tank), dimmed by power_out
    base_energy = {o.name: o.data.energy for o in room_lights + tank_lights}

    def lightning(frame, strength=1.0):
        """Two quick hits: the window and sky go white, the bolt shows, and the room flashes blue."""
        fl_sky = win["sky"].node_tree.nodes["Flash"].inputs["Factor"]
        fl_bolt = win["bolt"].node_tree.nodes["Mix"].inputs[0]
        fl_room = grade.nodes["flash"].outputs[0]
        for f, v in ((frame - 1, 0.0), (frame, 1.0), (frame + 1, 0.25), (frame + 2, 0.85), (frame + 3, 0.5),
                     (frame + 6, 0.0)):
            it = "LINEAR" if f >= frame + 3 else "CONSTANT"
            _ksock(fl_sky, f, v * 0.9 * strength, it)
            _ksock(fl_room, f, v * 0.15 * strength, it)
            _kprop(strike.data, "energy", f, v * 10 * strength, it)
            _ksock(fl_bolt, f, (1.0 if frame <= f <= frame + 2 and v > 0.5 else 0.0) * strength, "CONSTANT")

    def flicker(frames):
        """The ceiling light and the lamp stutter off for 2 frames at each listed frame (on 2s)."""
        frames = sorted(frames)
        _set_room(frames[0] - 1, True)
        for f in frames:
            _set_room(f, False)
            _set_room(f + 2, True)

    def _set_room(f, on, level_off=0.55):
        lv = grade.nodes["level"].outputs[0]
        _ksock(lv, f, 1.0 if on else level_off, "CONSTANT")
        for o in room_lights:
            _kprop(o.data, "energy", f, base_energy[o.name] * (1.0 if on else 0.04), "CONSTANT")
        for m, s in room_glows:
            _ksock(_em(m).inputs[1], f, s if on else s * 0.08, "CONSTANT")

    def power_out(frame):
        """Every lab light dies at `frame` (tanks, lamp, ceiling, laptop); only the storm outside lights the room."""
        _set_room(frame - 1, True)
        _set_room(frame, False, level_off=0.3)
        for o in tank_lights:
            _kprop(o.data, "energy", frame - 1, base_energy[o.name], "CONSTANT")
            _kprop(o.data, "energy", frame, 0.0, "CONSTANT")
        for m, s in tank_glows + slot_glows + [(desk["screen"], 1.15), (spill_m, 1.0)]:
            em = _em(m).inputs[1]
            _ksock(em, frame - 1, s, "CONSTANT")
            _ksock(em, frame, s * 0.06, "CONSTANT")

    spill_parts = []

    def place_tank(t, dim_on_power_out=True):
        """Put mk/pistolshrimp.tank()'s result (helper 2's tank and its crack) into the desk slot, scaled to fit, and
        start crack_puddle's water at its crack. Call before crack_puddle and power_out (which then also darkens the
        tank, unless dim_on_power_out=False)."""
        root = t["root"]
        root.location, root.scale = slot["root_loc"], (slot["scale"],) * 3
        slot["hood"].data.energy = base_energy["tank_hood"] = 4.0
        bpy.context.view_layer.update()
        if dim_on_power_out:
            seen, todo = set(), [root]
            while todo:
                o = todo.pop()
                todo += list(o.children)
                for m in getattr(o.data, "materials", None) or []:
                    if m and m.name not in seen and _em(m):
                        seen.add(m.name)
                        slot_glows.append((m, _em(m).inputs[1].default_value))
        o = t.get("crack_origin")
        if o is not None:
            p = root.matrix_world @ Vector((o.x, o.y - 0.1, 0.0))
            slot["leak"] = (p.x, p.y, desk["top"] + 0.004)
        return t

    def crack_puddle(f0, f1):
        """Water leaks from the front of the tank in the slot, runs across the desk top, pours off the front edge,
        then spreads across the floor and touches the power strip at f1. (The crack itself is helper 2's:
        pistolshrimp.crack(t, f0).)"""
        spill = _water_floor()
        lx, ly, lz = slot["leak"]
        y0, top = desk["front_y"], desk["top"]
        t_edge, t_floor = f0 + (f1 - f0) * 0.15, f0 + (f1 - f0) * 0.3
        # the sheet of water on the desk, from the tank to the front edge
        sheet = _mesh("spill_desk", [(-0.035, -1, 0), (0.035, -1, 0), (0.05, 0, 0), (-0.05, 0, 0)], [(0, 1, 2, 3)],
                      spill, (lx, ly, lz))
        anim.key(sheet, "scale", f0 - 1, (1, 0.001, 1), "CONSTANT")
        anim.key(sheet, "scale", t_edge, (1, ly - y0 + 0.005, 1), "LINEAR")
        anim.key(sheet, "scale", f1, (1.5, ly - y0 + 0.005, 1), "LINEAR")
        # the stream pouring off the edge: a thin ribbon whose top is fixed and which grows down to the floor
        tr = _mesh("spill_stream", [(-0.01, 0, -1), (0.01, 0, -1), (0.012, 0, 0), (-0.012, 0, 0)], [(0, 1, 2, 3)],
                   spill, (lx, y0 - 0.012, top))
        tr.visible_shadow = False
        anim.key(tr, "scale", t_edge - 1, (1, 1, 0.001), "CONSTANT")
        anim.key(tr, "scale", t_floor, (1, 1, top), "LINEAR")
        anim.key(tr, "scale", f1, (1.4, 1, top), "LINEAR")
        # the floor puddle: overlapping irregular discs along a curving path from below the edge to the strip
        a = Vector((lx, y0 - 0.06, 0.0))
        b = Vector((strip_end.x - 0.02, strip_end.y + 0.03, 0.0))
        bend = Vector((0.05, -0.08, 0))
        r = random.Random(21)
        n = 14
        for i in range(n):
            u = i / (n - 1)
            p = a.lerp(b, u) + bend * math.sin(u * math.pi)
            rad = 0.09 + 0.06 * math.sin(u * math.pi) + r.uniform(-0.01, 0.02)
            verts = [(math.cos(k / 20 * 2 * math.pi) * rad * r.uniform(0.82, 1.1),
                      math.sin(k / 20 * 2 * math.pi) * rad * r.uniform(0.82, 1.1), 0) for k in range(20)]
            d = _mesh(f"spill{i}", verts, [tuple(range(20))], spill, (p.x, p.y, 0.0045 + i * 0.00001))
            ts = t_floor + (f1 - t_floor) * u
            anim.key(d, "scale", ts - 1, 0.001, "CONSTANT")
            anim.key(d, "scale", ts + 5, 1.0)
            spill_parts.append(d)
        for i in range(3):        # the pool under the stream keeps widening while the leak runs
            d = _mesh(f"spill_pool{i}", [(math.cos(k / 24 * 2 * math.pi) * 0.15 * r.uniform(0.85, 1.1),
                                          math.sin(k / 24 * 2 * math.pi) * 0.11 * r.uniform(0.85, 1.1), 0)
                                         for k in range(24)], [tuple(range(24))], spill,
                      (a.x + r.uniform(-0.06, 0.06), a.y + r.uniform(-0.04, 0.02), 0.0044))
            anim.key(d, "scale", t_floor - 1, 0.001, "CONSTANT")
            anim.key(d, "scale", f1, 1.0 + 0.2 * i, "LINEAR")
        hl = _glow("spill_hl", "#e6f8ff", 1.2)
        for i in (3, 7, 10, 12):  # a few white glints that arrive with their disc
            d = spill_parts[i]
            g = _mesh(f"spill_glint{i}", [(-0.03, -0.004, 0), (0.03, -0.004, 0), (0.03, 0.004, 0), (-0.03, 0.004, 0)],
                      [(0, 1, 2, 3)], hl, (0, 0, 0.0005))
            g.parent = d
            g.rotation_euler = (0, 0, r.uniform(-0.6, 0.6))

    def floor_pan(f0, f1):
        """S09's short pan on the floor camera: from the water pouring off the desk to the strip."""
        cam = cams["floor"]
        lx, _, _ = slot["leak"]
        anim.key(cam, "rotation_euler", f0, _aim(FLOOR_CAM, (lx, desk["front_y"], 0.3)), "BEZIER")
        anim.key(cam, "rotation_euler", f1, _aim(FLOOR_CAM, FLOOR_AIM), "BEZIER")

    def spark(frame):
        """A bright electric spark at the strip: light pop, a four-point star burst and sparks that fly and fade."""
        for f, v in ((frame - 1, 0), (frame, 1.0), (frame + 1, 0.25), (frame + 2, 0.8), (frame + 3, 0.15),
                     (frame + 5, 0)):
            _kprop(spark_l.data, "energy", f, v * 6, "CONSTANT")
        star_m = _glow("spark_star", "#f4fbff", 3.0)
        core_m = _glow("spark_core", "#9fd8ff", 2.0)
        verts = []
        for k in range(8):
            ang = k / 8 * 2 * math.pi
            rr = 1.0 if k % 2 == 0 else 0.09
            verts.append((math.cos(ang) * rr, 0, math.sin(ang) * rr))
        stars = []
        for j, rz in enumerate((0.0, math.pi / 2)):
            s = _mesh(f"spark_star{frame}_{j}", verts + [(0, 0, 0)], [(8, k, (k + 1) % 8) for k in range(8)],
                      star_m if j == 0 else core_m, tuple(spark_at))
            s.rotation_euler = (0, math.radians(45 if j == 0 else 0), 0.3)    # an X and a + facing the camera
            s.visible_shadow = False
            stars.append(s)
        for j, s in enumerate(stars):        # the two sparkles alternate: a twinkle
            seq = ((0.001, 0.12, 0.05, 0.14, 0.04, 0.001) if j == 0 else (0.001, 0.05, 0.09, 0.04, 0.07, 0.001))
            for f, sc in zip(range(frame - 1, frame + 5), seq):
                anim.key(s, "scale", f, sc, "CONSTANT")
        core = _ball(f"spark_core{frame}", tuple(spark_at), (0.018, 0.018, 0.018), _glow("spark_white", "#ffffff", 4.0),
                     10)
        core.visible_shadow = False
        for f, sc in zip(range(frame - 1, frame + 5), (0.001, 1.2, 0.6, 1.0, 0.4, 0.001)):
            anim.key(core, "scale", f, sc, "CONSTANT")
        r = random.Random(frame)
        arc_m = _glow("spark_arc", "#dff6ff", 3.0)
        for j in range(2):          # electric arcs jumping from the water's edge to the plug
            a, b = Vector(strip_end) + Vector((0.01 * j, 0.02, 0.004)), spark_at + Vector((0, 0, -0.01 * j))
            pts = [a.lerp(b, k / 6) + Vector((0, 0, r.uniform(-0.02, 0.02) if 0 < k < 6 else 0)) for k in range(7)]
            verts, faces = [], []
            for k, (pa, pb) in enumerate(zip(pts, pts[1:])):
                i0 = len(verts)
                verts += [tuple(pa + Vector((0, 0, -0.003))), tuple(pa + Vector((0, 0, 0.003))),
                          tuple(pb + Vector((0, 0, 0.003))), tuple(pb + Vector((0, 0, -0.003)))]
                faces.append((i0, i0 + 1, i0 + 2, i0 + 3))
            arc = _mesh(f"spark_arc{frame}_{j}", verts, faces, arc_m)
            arc.visible_shadow = False
            for f, sc in ((frame - 1, 0.0), (frame + j, 1.0), (frame + 2 + j, 0.0)):
                anim.key(arc, "scale", f, sc if sc else 0.001, "CONSTANT")
        fly = _glow("spark_bit", "#ffe9a8", 2.5)
        for i in range(12):
            bit = _ball(f"spark_bit{frame}_{i}", tuple(spark_at), (0.004, 0.004, 0.012), fly, 6)
            bit.visible_shadow = False
            ang, up = r.uniform(0, 2 * math.pi), r.uniform(0.6, 1.4)
            v = Vector((math.cos(ang) * r.uniform(0.2, 0.45), math.sin(ang) * r.uniform(0.2, 0.45), up))
            anim.key(bit, "scale", frame - 1, 0.001, "CONSTANT")
            anim.key(bit, "scale", frame, 1.0, "CONSTANT")
            for k in range(0, 9, 2):
                t = k / 24
                pos = spark_at + v * t + Vector((0, 0, -4.9 * t * t))
                pos.z = max(pos.z, 0.006)
                anim.key(bit, "location", frame + k, tuple(pos), "LINEAR")
            anim.key(bit, "scale", frame + 8, 0.6)
            anim.key(bit, "scale", frame + 10, 0.001, "CONSTANT")

    for o in bpy.context.scene.objects:
        see_through = o.type == "MESH" and any(m and getattr(m, "surface_render_method", "") == "BLENDED"
                                               for m in o.data.materials)
        if see_through or o.name.startswith(("sky", "bldg", "tree_sil", "bolt", "rain", "glass_drops")):
            o.visible_shadow = False
    return dict(cams=cams, seat=seat, chair=chair, tank_slot=slot, tanks=tanks, strip=strip,
                strip_end=tuple(strip_end), spark_at=tuple(spark_at), grade=grade,
                lights=dict(ceiling=ceiling, lamp=desk["lamp"], window=moon, lightning=strike, spark=spark_l,
                            tanks=tank_lights),
                window=dict(center=(-1.2, WALL_Y, 1.675), size=(1.3, 1.25), sky=win["sky"], bolt=win["bolt"],
                            moon=moon, lightning=strike),
                room_lights=dict(lights=room_lights, glows=[m for m, _ in room_glows], grade=grade),
                desk=dict(top=desk["top"], center=desk["center"], x=desk["x"], front_y=desk["front_y"],
                          laptop=desk["laptop"], screen=desk["screen"], seat=seat, chair=chair, tank_slot=slot),
                floor=dict(object=bpy.data.objects["floor_tiles"], z=0.0, x=ROOM[:2], y=ROOM[2:4]),
                place_tank=place_tank,
                lightning=lightning, flicker=flicker, crack_puddle=crack_puddle, spark=spark, power_out=power_out,
                floor_pan=floor_pan)
