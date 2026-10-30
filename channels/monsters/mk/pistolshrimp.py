"""The pistol shrimp (Alpheidae) of Episode 1: the real Earth animal behind the series' first creature, living in a
glass tank in Kai's lab. A small, recognisable snapping shrimp in the series' anime look: a translucent orange-red
body (cel two-tone plus a soft peach edge where light passes through), a pale stripe down its back, ONE hugely
oversized snapping claw, a small second claw, long antennae, thin walking legs and a tail fan. Built as a rig of
parented objects so shots can animate it:

    rig = build(loc, turn)  ->  dict(root, body, shoulder, hinge, tail, eyes, antennae, tip)
    root      : moves/turns the whole shrimp (feet at z=0; head toward local -X, the big claw on the -Y side)
    body      : body pivot at the ground (recoil, squash)
    shoulder  : the big claw's pivot (rotation Z swings the claw in and out, Y raises/lowers it)
    hinge     : the snapping finger (dactyl) pivot: rotation Y = 0 shut, OPEN (about 1.15) cocked wide
    tail      : the tail pivot (rotation Y > 0 flicks the tail fan down and under)
    eyes      : eye pivots (scale z to blink)
    antennae  : antenna pivots (small rotations for wobble)
    tip       : an empty just in front of the claw, where the jet and the cavitation bubble come out

    t = tank(loc)           ->  dict(root, glass, surface, crack, crack_origin)
    A painted aquarium (no outlines): gravel, plants, a rock burrow, a water-blue back wall, the water surface line,
    glass with a subtle edge highlight and glare, and a hidden crack on the front pane.

Animation helpers (all deterministic):
    idle(rig, f0, f1)               breathing bob, antenna wobble, blinks, a lazy tail fan
    snap(rig, f, slow=1)            the claw cocks open, then shuts in 1-2 frames at f; spawns the bubble and the ring
    bubble(rig, f, slow=1)          the glowing white-blue cavitation bubble: swells, shrinks, flashes and pops
    shock(rig, f, slow=1)           a small water shock ring racing out from the claw tip
    crack(t, f)                     a crack line runs up the front glass
`slow` stretches the snap effects for a slow-motion shot (e.g. slow=4 for the "~4,700 °C" fact card).
"""
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

from . import anim, look, paintbg, sdf

BODY, EDGE, STRIPE = "#ff8a5f", "#ffe8d8", "#fff5ee"
CLAW, CLAW_TIP, FAN, INK, IRIS = "#ff6440", "#ffe4d2", "#ffa27a", "#1b1830", "#ffa040"
OPEN = 1.15                                       # dactyl rotation when cocked wide
TANK_X, TANK_FRONT, TANK_BACK, WATER_Z, TANK_TOP = 6.0, -2.6, 3.6, 4.2, 4.65


# --------------------------------------------------------------------------- small builders
def _empty(name, world, parent=None, size=0.15):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = size
    bpy.context.scene.collection.objects.link(e)
    if parent:
        e.parent = parent
    bpy.context.view_layer.update()
    e.matrix_world = Matrix.Translation(world)
    bpy.context.view_layer.update()
    return e


def _attach(o, parent):
    bpy.context.view_layer.update()
    o.parent = parent
    o.matrix_parent_inverse = parent.matrix_world.inverted()


def _smooth(o):
    o.data.polygons.foreach_set("use_smooth", [True] * len(o.data.polygons))


def _sphere(name, loc, scale, mat, line=0.0, seg=24, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=max(6, seg // 2), location=tuple(loc), rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)   # keep the origin at the centre
    o.data.materials.append(mat)
    _smooth(o)
    return look.outline(o, line)


def _tube(name, pts, radius, mat, line=0.0, taper=None):
    """A bevelled Bezier tube through `pts`, converted to a mesh (so it can take an outline). `taper` = (r0, r1)
    shrinks the radius along the tube (antenna whips)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 3
    cu.resolution_u = 10
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for i, (bp, p) in enumerate(zip(sp.bezier_points, pts)):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
        if taper:
            bp.radius = taper[0] + (taper[1] - taper[0]) * i / max(1, len(pts) - 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    for s in bpy.context.selected_objects:
        s.select_set(False)
    o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.object
    o.data.materials.append(mat)
    _smooth(o)
    return look.outline(o, line)


def _shell(name, base, edge, amount=0.75, gloss=False):
    """The anime two-tone material plus a hard light band at the thin edges: reads as a translucent shell."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = look.toon(name, look.hexc(base), gloss=gloss)
    nt = m.node_tree
    em = next(n for n in nt.nodes if n.type == "EMISSION")
    src = em.inputs[0].links[0].from_socket
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    rr = nt.nodes.new("ShaderNodeValToRGB")
    rr.color_ramp.interpolation = "CONSTANT"                 # one hard light band (anime: mostly flat)
    rr.color_ramp.elements[0].position, rr.color_ramp.elements[0].color = 0.0, (0, 0, 0, 1)
    rr.color_ramp.elements[1].position, rr.color_ramp.elements[1].color = 0.7, (amount, amount, amount, 1)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs[7].default_value = look.hexc(edge)
    nt.links.new(lw.outputs["Facing"], rr.inputs[0])
    nt.links.new(rr.outputs[0], mix.inputs["Factor"])
    nt.links.new(src, mix.inputs[6])
    nt.links.new(mix.outputs[2], em.inputs[0])
    return m


def _gradient(name, bottom, top, noise=0.06):
    """Painted vertical gradient (the water-blue back wall): uses the object's Generated Z."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    gr = nt.nodes.new("ShaderNodeValToRGB")
    gr.color_ramp.interpolation = "EASE"
    gr.color_ramp.elements[0].position, gr.color_ramp.elements[0].color = 0.0, look.hexc(bottom)
    gr.color_ramp.elements[1].position, gr.color_ramp.elements[1].color = 1.0, look.hexc(top)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 3.0
    nz.inputs["Detail"].default_value = 3.0
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type, mx.blend_type = "RGBA", "OVERLAY"
    mx.inputs["Factor"].default_value = noise
    em = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    L(tc.outputs["Generated"], sep.inputs[0])
    L(sep.outputs["Z"], gr.inputs[0])
    L(gr.outputs[0], mx.inputs[6])
    L(nz.outputs["Color"], mx.inputs[7])
    L(mx.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def _glow(name, rgba, alpha):
    """A see-through glow shell whose emission is boosted (the cavitation bubble's halo)."""
    m = look.fade(name, rgba, alpha)
    m.use_backface_culling = True                      # each shell adds its glow once, not twice
    for n in m.node_tree.nodes:
        if n.type == "EMISSION":
            n.inputs[1].default_value = 1.6
    return m


def _alpha_keys(mat, keys):
    mix = mat.node_tree.nodes["Mix"]
    for fr, a in keys:
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    for fc in anim.all_fcurves(mat.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


# --------------------------------------------------------------------------- the shrimp
def _mark(name, parts, mat, parent, res=0.015, line=0.0, k=0.04):
    """A marking or patch as its OWN smooth shape pressed into the body: its edge is the clean curve where the two
    surfaces meet (per-face SDF materials come out jagged)."""
    o = sdf.build(name, [(f, mat.name, None) for f in parts], k=k, res=res, pad=0.06, smooth_iter=6)
    look.outline(o, line)
    _attach(o, parent)
    return o


def build(loc=(0, 0, 0), turn=0.0, name="pshrimp"):
    """The shrimp, standing on the gravel at `loc`, turned `turn` radians about Z (0: head toward -X)."""
    body_m = _shell(f"{name}_body", BODY, EDGE, 0.8)
    stripe_m = look.toon(f"{name}_stripe", look.hexc(STRIPE))
    fan_m = _shell(f"{name}_fan", FAN, "#ffe6d6", 0.9)
    claw_m = _shell(f"{name}_claw", CLAW, EDGE, 0.6, gloss=True)
    tip_m = look.toon(f"{name}_tip", look.hexc(CLAW_TIP), gloss=True)
    palm_m = look.toon(f"{name}_palm", look.hexc("#ff9a74"))
    eye_m = look.toon(f"{name}_eye", look.hexc(INK), gloss=True)
    iris_m = look.flat(f"{name}_iris", look.hexc(IRIS))          # the lighter crescent low in the eye
    hi_m = look.flat(f"{name}_hi", (1, 1, 1, 1))
    leg_m = _shell(f"{name}_leg", "#ff8a5c", EDGE, 0.6)
    E, C = sdf.E, sdf.C

    root = _empty(f"{name}_root", (0, 0, 0), size=0.4)
    body = _empty(f"{name}_body", (0, 0, 0), root)

    # carapace, head hood, rostrum and the first three abdomen segments: one smooth shape, one colour
    segs = [((0.33, 0, 0.56), (0.21, 0.27, 0.29)), ((0.62, 0, 0.54), (0.19, 0.25, 0.27)),
            ((0.9, 0, 0.51), (0.18, 0.23, 0.25))]
    parts = [(E((-0.25, 0, 0.56), (0.62, 0.3, 0.3)), body_m.name, None),
             (E((-0.78, 0, 0.61), (0.26, 0.25, 0.24)), body_m.name, 0.12),
             (C((-0.98, 0, 0.7), (-1.16, 0, 0.67), 0.055, 0.02), body_m.name, 0.05)]
    parts += [(E(c, r), body_m.name, 0.08) for c, r in segs]
    bodymesh = sdf.build(f"{name}_bodymesh", parts, k=0.1, res=0.02, pad=0.12, smooth_iter=14)
    look.outline(bodymesh, 0.016)
    _attach(bodymesh, body)
    # the pale stripe down its back: a tube pressed into the shell
    back = [(-0.62, 0, 0.74), (-0.25, 0, 0.825), (0.33, 0, 0.815), (0.62, 0, 0.775), (0.9, 0, 0.725)]
    _mark(f"{name}_stripe", [C(p, q, 0.06) for p, q in zip(back, back[1:])], stripe_m, body)

    # tail: last three segments on their own pivot (so it can flick), the stripe, and the tail fan as its own shape
    tail = _empty(f"{name}_tail", (1.0, 0, 0.5), body)
    tparts = [(E((1.17, 0, 0.47), (0.17, 0.21, 0.23)), body_m.name, None),
              (E((1.4, 0, 0.43), (0.15, 0.18, 0.2)), body_m.name, 0.08),
              (E((1.61, 0, 0.39), (0.13, 0.15, 0.17)), body_m.name, 0.08)]
    tailmesh = sdf.build(f"{name}_tailmesh", tparts, k=0.08, res=0.02, pad=0.12, smooth_iter=12)
    look.outline(tailmesh, 0.014)
    _attach(tailmesh, tail)
    tback = [(1.0, 0, 0.675), (1.17, 0, 0.665), (1.4, 0, 0.6), (1.61, 0, 0.53)]
    _mark(f"{name}_tstripe", [C(p, q, 0.05) for p, q in zip(tback, tback[1:])], stripe_m, tail)
    _mark(f"{name}_fan", [E((1.9, 0, 0.36), (0.26, 0.09, 0.05)), E((1.86, -0.18, 0.37), (0.27, 0.13, 0.04)),
                          E((1.86, 0.18, 0.37), (0.27, 0.13, 0.04)), E((1.68, 0, 0.38), (0.1, 0.1, 0.08))],
          fan_m, tail, res=0.016, line=0.012, k=0.06)

    # one big cute eye per side: black, a warm crescent low in the eye, two white highlights
    eyes = []
    for sy in (-1, 1):
        piv = _empty(f"{name}_eyepiv{sy}", (-0.84, sy * 0.2, 0.71), body)
        e = _sphere(f"{name}_eye{sy}", (-0.84, sy * 0.2, 0.71), (0.15, 0.095, 0.18), eye_m, 0.012)
        cr = _sphere(f"{name}_iris{sy}", (-0.835, sy * 0.268, 0.625), (0.105, 0.026, 0.066), iris_m, 0, 20)
        h1 = _sphere(f"{name}_hi{sy}", (-0.9, sy * 0.285, 0.79), (0.055, 0.02, 0.06), hi_m, 0, 12)
        h2 = _sphere(f"{name}_hi2{sy}", (-0.775, sy * 0.296, 0.64), (0.026, 0.012, 0.028), hi_m, 0, 10)
        for o in (e, cr, h1, h2):
            _attach(o, piv)
        eyes.append(piv)

    # antennae: a short forked pair (antennules) and two long whips that sweep back over the body
    antennae = []
    for sy in (-1, 1):
        base = Vector((-0.97, sy * 0.1, 0.7))
        piv = _empty(f"{name}_antpiv{sy}", base, body)
        whip = _tube(f"{name}_whip{sy}", [base, base + Vector((-0.55, sy * 0.12, 0.25)),
                                          base + Vector((-1.0, sy * 0.3, 0.95)), base + Vector((-0.55, sy * 0.45, 1.7)),
                                          base + Vector((0.6, sy * 0.55, 2.0)), base + Vector((1.9, sy * 0.6, 1.75))],
                     0.016, leg_m, 0.006, taper=(1.0, 0.45))
        _attach(whip, piv)
        for k, (dz, dy) in enumerate(((0.32, 0.04), (0.2, 0.12))):
            a = _tube(f"{name}_antl{sy}{k}", [base + Vector((0, 0, -0.02)), base + Vector((-0.3, sy * dy, dz * 0.6)),
                                              base + Vector((-0.55, sy * (dy + 0.05), dz))], 0.014, leg_m, 0.005,
                      taper=(1.0, 0.5))
            _attach(a, piv)
        antennae.append(piv)

    # walking legs: four thin pairs, knees out, feet on the ground
    for i in range(4):
        x = -0.52 + i * 0.21
        for sy in (-1, 1):
            leg = _tube(f"{name}_leg{i}{sy}", [(x, sy * 0.16, 0.34), (x - 0.04, sy * 0.38, 0.3),
                                                (x + 0.02 + i * 0.03, sy * 0.47, 0.13), (x + 0.07 + i * 0.04, sy * 0.5, 0.0)],
                        0.022, leg_m, 0.006, taper=(1.0, 0.6))
            _attach(leg, body)
    # the small second claw on the far side
    small = sdf.build(f"{name}_smallclaw", [
        (C((-0.62, 0.2, 0.36), (-0.95, 0.33, 0.4), 0.04, 0.045), claw_m.name, None),
        (E((-1.12, 0.34, 0.43), (0.17, 0.065, 0.07)), claw_m.name, 0.05),
        (C((-1.25, 0.34, 0.45), (-1.42, 0.34, 0.44), 0.035, 0.015), claw_m.name, 0.03),
        (C((-1.25, 0.34, 0.41), (-1.4, 0.34, 0.4), 0.03, 0.013), claw_m.name, 0.03)], k=0.05, res=0.015, pad=0.08,
        smooth_iter=6)
    look.outline(small, 0.008)
    _attach(small, body)

    # THE claw: shoulder pivot -> arm + huge palm + fixed finger -> hinge -> snapping finger (dactyl)
    shoulder = _empty(f"{name}_shoulder", (-0.62, -0.24, 0.36), body)
    arm = sdf.build(f"{name}_claw", [
        (C((-0.62, -0.24, 0.36), (-0.95, -0.4, 0.42), 0.06, 0.075), claw_m.name, None),
        (C((-0.95, -0.4, 0.42), (-1.18, -0.43, 0.5), 0.075, 0.1), claw_m.name, 0.06),
        (E((-1.58, -0.44, 0.58), (0.48, 0.25, 0.28)), claw_m.name, 0.12),
        (C((-1.95, -0.44, 0.47), (-2.2, -0.44, 0.46), 0.12, 0.065), claw_m.name, 0.08),
    ], k=0.1, res=0.018, pad=0.1, smooth_iter=8)
    look.outline(arm, 0.016)
    _attach(arm, shoulder)
    _mark(f"{name}_ptip", [E((-2.22, -0.44, 0.46), (0.075, 0.062, 0.062))], tip_m, shoulder, line=0.01)
    _mark(f"{name}_palmhi", [E((-1.5, -0.675, 0.62), (0.26, 0.035, 0.12))], palm_m, shoulder)
    hinge = _empty(f"{name}_hinge", (-1.93, -0.44, 0.7), shoulder)
    finger = sdf.build(f"{name}_dactyl", [
        (C((-1.93, -0.44, 0.7), (-2.24, -0.44, 0.615), 0.13, 0.075), claw_m.name, None),
        (E((-2.05, -0.44, 0.6), (0.09, 0.06, 0.06)), claw_m.name, 0.05),     # the plunger under the finger
    ], k=0.06, res=0.016, pad=0.1, smooth_iter=8)
    look.outline(finger, 0.014)
    _attach(finger, hinge)
    _mark(f"{name}_dtip", [E((-2.27, -0.44, 0.61), (0.08, 0.066, 0.066))], tip_m, hinge, line=0.01)
    tip = _empty(f"{name}_tip", (-2.45, -0.44, 0.53), shoulder)

    look.blob_shadow(f"{name}_shadow", (0.0, -0.1, 0.012), (1.9, 0.75), root)
    root.location = loc
    root.rotation_euler = (0, 0, turn)
    bpy.context.view_layer.update()
    return dict(root=root, body=body, shoulder=shoulder, hinge=hinge, tail=tail, eyes=eyes, antennae=antennae,
                tip=tip, name=name)


def reaction(rig, f, hold=6):
    """The shrimp's held "startled" pose (usable as a freeze frame): claw thrown wide open and raised, antennae
    flung up and apart, tail curled under, body squashed, eyes a little bigger. Keys it at f (snappy) and holds it
    for `hold` frames."""
    for fr in (f, f + hold):
        anim.key(rig["hinge"], "rotation_euler", fr, (0, OPEN, 0))
        anim.key(rig["shoulder"], "rotation_euler", fr, (0, -0.22, 0.18))
        anim.key(rig["tail"], "rotation_euler", fr, (0, 0.45, 0))
        anim.squash(rig["body"], fr, -0.06)
        for i, a in enumerate(rig["antennae"]):
            anim.key(a, "rotation_euler", fr, (0.35 * (-1) ** i, -0.3, 0.12 * (-1) ** i))
        for e in rig["eyes"]:
            anim.key(e, "scale", fr, (1.12, 1.12, 1.15))


# --------------------------------------------------------------------------- the tank
def tank(loc=(0, 0, 0), seed=7, crack_x=-1.6):
    """A painted aquarium around `loc` (gravel top at z=0). The front glass faces -Y at y = TANK_FRONT."""
    hx = look.hexc
    P = look.paint
    rnd = random.Random(seed)
    root = _empty("tank_root", (0, 0, 0), size=0.5)
    objs = []

    def keep(o):
        objs.append(o)
        return o

    # water-blue back wall and side walls, the sand floor
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, TANK_BACK, (WATER_Z - 1.0) / 2), rotation=(math.pi / 2, 0, 0))
    back = keep(bpy.context.object)
    back.name = "tank_back"
    back.scale = (2 * TANK_X + 0.2, WATER_Z + 1.0, 1)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    back.data.materials.append(_gradient("tank_water", "#1f6f8c", "#7fd0dc"))
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(sx * TANK_X, (TANK_FRONT + TANK_BACK) / 2, (WATER_Z - 1) / 2),
                                         rotation=(math.pi / 2, 0, math.pi / 2))
        s = keep(bpy.context.object)
        s.scale = (TANK_BACK - TANK_FRONT, WATER_Z + 1.0, 1)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        s.data.materials.append(_gradient("tank_side", "#1a5f7a", "#6cc0cf"))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (TANK_FRONT + TANK_BACK) / 2, -0.03))
    fl = keep(bpy.context.object)
    fl.scale = (2 * TANK_X, TANK_BACK - TANK_FRONT, 1)
    fl.data.materials.append(P("tank_sand", hx("#d9c39a"), noise=0.18, scale=9.0))

    # gravel: one mesh of seeded pebbles in four painted colours
    pebble_m = [P("peb0", hx("#cdb48a"), noise=0.1), P("peb1", hx("#a99a8c"), noise=0.1),
                P("peb2", hx("#e6dccb"), noise=0.1), P("peb3", hx("#8e7c6c"), noise=0.1)]
    me = bpy.data.meshes.new("tank_gravel")
    bm = bmesh.new()
    mats = []
    for i in range(520):
        x, y = rnd.uniform(-TANK_X + 0.2, TANK_X - 0.2), rnd.uniform(TANK_FRONT + 0.1, TANK_BACK - 0.2)
        if (x / 1.5) ** 2 + (y / 0.6) ** 2 < 1.0 and rnd.random() < 0.85:
            continue                                   # a little clearing under the shrimp
        s = rnd.uniform(0.06, 0.15)
        mtx = Matrix.Translation((x, y, s * 0.25)) @ Matrix.Rotation(rnd.uniform(0, 6.3), 4, "Z") @ \
            Matrix.Diagonal((s * rnd.uniform(1.0, 1.5), s, s * 0.6, 1))
        r = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mtx)
        k = rnd.randrange(4)
        faces = {f for v in r["verts"] for f in v.link_faces}
        mats.append((faces, k))
    for faces, k in mats:
        for f in faces:
            f.material_index = k
            f.smooth = True
    bm.to_mesh(me)
    bm.free()
    gravel = keep(bpy.data.objects.new("tank_gravel", me))
    bpy.context.scene.collection.objects.link(gravel)
    for m in pebble_m:
        gravel.data.materials.append(m)

    # a rock with the shrimp's burrow, and plants (no outlines: painted background)
    rock_m = paintbg.paint3("tank_rock", hx("#6f6488"), hx("#9b8fb0"), hx("#c4bad6"), noise=0.2, scale=4.0)
    hole_m = look.flat("tank_hole", hx("#2c2238"))
    rock = keep(_sphere("tank_rock", (1.9, 1.3, 0.35), (1.25, 0.95, 0.8), rock_m, 0, 28, (0.2, 0.1, 0.4)))
    keep(_sphere("tank_rock2", (2.9, 1.9, 0.25), (0.7, 0.6, 0.5), rock_m, 0, 20, (0.1, 0.3, 0.9)))
    keep(_sphere("tank_hole", (1.35, 0.55, 0.32), (0.42, 0.08, 0.26), hole_m, 0, 20, (0, 0, 0.5)))
    leaf_m = [paintbg.paint3(f"tank_leaf{v}", *paintbg.greens(v, 0.25), noise=0.2, scale=5.0) for v in range(3)]
    for px, py, n, h in ((-3.6, 2.3, 9, 3.6), (-2.0, 3.0, 7, 2.6), (4.2, 2.6, 10, 3.9), (3.2, 3.1, 6, 2.2),
                         (-4.8, 1.2, 6, 1.8), (0.4, 3.2, 7, 3.2)):
        for j in range(n):
            a = j / n * 2 * math.pi + rnd.uniform(-0.3, 0.3)
            tilt = rnd.uniform(0.08, 0.35)
            hh = h * rnd.uniform(0.6, 1.0)
            top = (px + math.cos(a) * tilt * hh * 0.5, py + math.sin(a) * tilt * hh * 0.5, hh)
            mid = (px + math.cos(a) * tilt * hh * 0.15 + rnd.uniform(-0.1, 0.1), py + math.sin(a) * 0.1, hh * 0.5)
            keep(_tube(f"tank_blade{px}_{j}", [(px, py, 0), mid, top], 0.07, rnd.choice(leaf_m), 0, taper=(1.0, 0.25)))
    for i in range(3):                                 # soft caustic light patches on the sand
        c = keep(_sphere(f"tank_caustic{i}", (rnd.uniform(-3, 3), rnd.uniform(-1.5, 1.5), 0.02),
                         (rnd.uniform(0.5, 0.9), rnd.uniform(0.3, 0.5), 0.01), look.fade("tank_caustic", hx("#f4fff8"), 0.18),
                         0, 16, (0, 0, rnd.uniform(0, 3))))
        c.visible_shadow = False

    # water: the surface seen from below, and a bright wavy surface line on the glass
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, (TANK_FRONT + TANK_BACK) / 2, WATER_Z))
    surf = keep(bpy.context.object)
    surf.name = "tank_surface"
    surf.scale = (2 * TANK_X, TANK_BACK - TANK_FRONT, 1)
    surf.data.materials.append(look.fade("tank_surface", hx("#c9f3ff"), 0.45))
    surf.visible_shadow = False
    line_pts = [(x, TANK_FRONT - 0.015, WATER_Z + 0.035 * math.sin(x * 2.3) + 0.02 * math.sin(x * 5.1))
                for x in [-TANK_X + i * 0.3 for i in range(int(2 * TANK_X / 0.3) + 1)]]
    sline = keep(_tube("tank_surfline", line_pts, 0.022, look.flat("tank_surfline", hx("#f2fdff"), 1.2)))
    sline.visible_shadow = False
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, TANK_FRONT - 0.01, (WATER_Z + TANK_TOP) / 2),
                                     rotation=(math.pi / 2, 0, 0))
    air = keep(bpy.context.object)
    air.scale = (2 * TANK_X, TANK_TOP - WATER_Z, 1)
    air.data.materials.append(look.fade("tank_air", hx("#e9fbff"), 0.16))
    air.visible_shadow = False

    # glass: a faint pane, edge highlights, two glare streaks; dark plastic rims top and bottom
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, TANK_FRONT, (TANK_TOP - 0.3) / 2), rotation=(math.pi / 2, 0, 0))
    glass = keep(bpy.context.object)
    glass.name = "tank_glass"
    glass.scale = (2 * TANK_X, TANK_TOP + 0.3, 1)
    glass.data.materials.append(look.fade("tank_glass", hx("#dff7ff"), 0.05))
    glass.visible_shadow = False
    edge_m = look.fade("tank_edge", hx("#ffffff"), 0.7)
    for sx in (-1, 1):
        for dx, w, a in ((0.0, 0.035, 1.0), (-sx * 0.09, 0.012, 0.6)):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * TANK_X + dx, TANK_FRONT - 0.02, (TANK_TOP - 0.3) / 2))
            e = keep(bpy.context.object)
            e.scale = (w, 0.01, TANK_TOP + 0.3)
            e.data.materials.append(edge_m)
            e.visible_shadow = False
    glare_m = look.fade("tank_glare", hx("#ffffff"), 0.1)
    for gx, gw in ((-4.3, 0.55), (-3.4, 0.18), (3.9, 0.3)):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(gx, TANK_FRONT - 0.03, 2.0), rotation=(math.pi / 2, 0.42, 0))
        g = keep(bpy.context.object)
        g.scale = (gw, 3.6, 1)
        g.data.materials.append(glare_m)
        g.visible_shadow = False
    rim_m = P("tank_rim", hx("#26323d"), noise=0.05)
    for z, h in ((TANK_TOP + 0.08, 0.22), (-0.42, 0.62)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, (TANK_FRONT + TANK_BACK) / 2, z))
        r = keep(bpy.context.object)
        r.scale = (2 * TANK_X + 0.3, TANK_BACK - TANK_FRONT + 0.25, h)
        r.data.materials.append(rim_m)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -2.0, -0.735))   # the lab bench the tank stands on
    bench = keep(bpy.context.object)
    bench.scale = (30, 16, 1)
    bench.data.materials.append(paintbg.paint3("tank_bench", hx("#34404d"), hx("#4c5d6e"), hx("#6a7f92"), noise=0.15,
                                               scale=2.0))
    # under the gravel line the front shows the gravel bed through the glass
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, TANK_FRONT + 0.02, -0.06), rotation=(math.pi / 2, 0, 0))
    bed = keep(bpy.context.object)
    bed.scale = (2 * TANK_X, 0.12, 1)
    bed.data.materials.append(P("tank_bed", hx("#b89e78"), noise=0.2, scale=14.0))

    # a few rising air bubbles at the back left
    bub_m = look.fade("tank_bubble", hx("#f4fdff"), 0.55)
    for i in range(9):
        b = keep(_sphere(f"tank_bub{i}", (-4.4 + rnd.uniform(-0.1, 0.1), 2.6, 0.4 + i * 0.42), (1, 1, 1), bub_m, 0, 12))
        b.scale = [rnd.uniform(0.05, 0.1)] * 3
        b.visible_shadow = False

    # the crack (hidden until crack()): a jagged main line up the front pane plus three branches, each a bright
    # line over a darker, wider one, revealed by keying the curves' bevel end
    cracks = _make_crack(crack_x, rnd)
    for o in objs + cracks:
        if o.parent is None:
            o.parent = root
    root.location = loc
    bpy.context.view_layer.update()
    return dict(root=root, glass=glass, surface=surf, crack=cracks, crack_origin=Vector((crack_x, TANK_FRONT, 0.35)))


def _crack_curve(name, pts, radius, mat):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 1
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts):
        p.co = (*c, 1.0)
    cu.bevel_factor_mapping_end = "SPLINE"
    cu.bevel_factor_end = 0.0
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    o.visible_shadow = False
    return o


def _make_crack(x0, rnd):
    y = TANK_FRONT - 0.04
    lite = look.flat("crack_lite", look.hexc("#ffffff"), 2.0)
    dark = look.fade("crack_dark", look.hexc("#1d4656"), 0.45)
    pts, x, z = [], x0, 0.35
    while z < TANK_TOP - 0.05:
        pts.append((x, y, z))
        z += rnd.uniform(0.18, 0.34)
        x += rnd.uniform(-0.22, 0.22) + 0.04
    pts.append((x, y, TANK_TOP - 0.02))
    lines = [pts]
    for k in range(5):                                 # a little starburst where it starts
        a = -0.3 + k * 0.85 + rnd.uniform(-0.2, 0.2)
        ln = rnd.uniform(0.18, 0.34)
        lines.append([(x0, y, 0.35), (x0 + math.cos(a) * ln * 0.55, y, 0.35 + math.sin(a) * ln * 0.55 + 0.02),
                      (x0 + math.cos(a) * ln, y, 0.35 + math.sin(a) * ln)])
    for k in (2, 5, 8):                                # branches off the main line
        if k >= len(pts) - 1:
            continue
        bx, _, bz = pts[k]
        side = 1 if k % 2 else -1
        br = [(bx, y, bz)]
        for j in range(3):
            bx += side * rnd.uniform(0.18, 0.32)
            bz += rnd.uniform(0.05, 0.22)
            br.append((bx, y, bz))
        lines.append(br)
    out = []
    for i, line in enumerate(lines):
        r = 0.028 if i == 0 else 0.015
        out.append(_crack_curve(f"crack_dark{i}", [(p[0], p[1] + 0.005, p[2]) for p in line], r * 1.9, dark))
        out.append(_crack_curve(f"crack_lite{i}", line, r, lite))
    return out


# --------------------------------------------------------------------------- animation
def _world(o, frame):
    sc = bpy.context.scene
    keep = sc.frame_current
    sc.frame_set(int(frame))
    m = o.matrix_world.copy()
    sc.frame_set(keep)
    return m


def idle(rig, f0, f1, seed=2):
    """Gentle breathing, antenna wobble, blinks and a lazy tail fan between f0 and f1."""
    anim.idle(rig, f0, f1, period=32, amount=0.012, seed=seed)
    f = f0
    while f <= f1:
        anim.key(rig["tail"], "rotation_euler", f, (0, 0.0, 0))
        anim.key(rig["tail"], "rotation_euler", f + 16, (0, 0.06, 0))
        f += 32
    anim.key(rig["hinge"], "rotation_euler", f0, (0, 0.08, 0))


def snap(rig, f, wind=10, slow=1.0, fx=True, ring_radius=1.3):
    """The claw cocks wide open over `wind` frames, holds, then shuts in 1-2 frames at f (CONSTANT, no in-betweens).
    The body recoils, the tail flicks, the antennae whip. With fx, also spawns bubble() and shock() at the claw tip.
    `slow` > 1 stretches the shut and the follow-through for slow motion."""
    sh, hg, body, tail = rig["shoulder"], rig["hinge"], rig["body"], rig["tail"]
    s = max(1.0, slow)
    anim.key(hg, "rotation_euler", f - wind, (0, 0.08, 0))
    anim.key(hg, "rotation_euler", f - wind + 4, (0, OPEN * 0.95, 0))
    anim.key(hg, "rotation_euler", f - 1 - round(s - 1), (0, OPEN, 0), "LINEAR")      # cocked, holding
    if s > 1:
        anim.key(hg, "rotation_euler", f, (0, 0.0, 0), "CONSTANT")
    else:
        anim.key(hg, "rotation_euler", f, (0, OPEN * 0.35, 0), "LINEAR")               # 1 in-between
        anim.key(hg, "rotation_euler", f + 1, (0, 0.0, 0), "CONSTANT")
    anim.key(hg, "rotation_euler", f + round(14 * s), (0, 0.0, 0))
    anim.key(hg, "rotation_euler", f + round(22 * s), (0, 0.08, 0))
    anim.key(sh, "rotation_euler", f - wind, (0, 0, 0))
    anim.key(sh, "rotation_euler", f - 1, (0, -0.1, 0.12))                             # claw cocked back and up
    anim.key(sh, "rotation_euler", f + 1, (0, 0.06, -0.08), "LINEAR")                  # thrown forward
    anim.key(sh, "rotation_euler", f + round(10 * s), (0, 0, 0))
    anim.key(body, "location", f - 1, (0, 0, 0))
    anim.key(body, "location", f + 1, (0.12, 0, 0.02), "LINEAR")                       # recoil
    anim.key(body, "location", f + round(12 * s), (0, 0, 0))
    anim.squash(body, f - 1, -0.05)
    anim.squash(body, f + 1, 0.06, "LINEAR")
    anim.squash(body, f + round(8 * s), 0.0)
    anim.key(tail, "rotation_euler", f - 1, (0, -0.05, 0))
    anim.key(tail, "rotation_euler", f + 2, (0, 0.55, 0), "LINEAR")                    # tail flick
    anim.key(tail, "rotation_euler", f + round(12 * s), (0, -0.08, 0))
    anim.key(tail, "rotation_euler", f + round(20 * s), (0, 0.0, 0))
    for i, a in enumerate(rig["antennae"]):
        sgn = (-1) ** i
        anim.key(a, "rotation_euler", f, (0, 0, 0))
        anim.key(a, "rotation_euler", f + 2, (0.25 * sgn, -0.18, 0.1 * sgn), "LINEAR")
        anim.key(a, "rotation_euler", f + round(7 * s), (-0.1 * sgn, 0.08, -0.05 * sgn))
        anim.key(a, "rotation_euler", f + round(14 * s), (0, 0, 0))
    out = {}
    if fx:
        out["bubble"] = bubble(rig, f, slow)
        out["ring"] = shock(rig, f, slow, radius=ring_radius)
    return out


def _jet(rig, f):
    """World position of the claw tip at frame f, and the jet's direction (out of the claw's front)."""
    tip = _world(rig["tip"], f).translation
    hinge = _world(rig["hinge"], f).translation
    d = tip - hinge
    d.z = 0.0
    return tip, d.normalized()


def bubble(rig, f, slow=1.0, size=0.17):
    """The cavitation bubble at the claw tip: a white-hot core in layered white-blue glow. It swells for a frame,
    shrinks, flashes brightest as it collapses, then pops (a last ring of light and a few micro-bubbles)."""
    s = max(1.0, slow)
    pos, d = _jet(rig, f + 1)
    pos = pos + d * size * 1.3
    n = f"bubble_{f}"
    holder = _empty(n, pos, size=0.2)
    core = _sphere(f"{n}_core", pos, (1, 1, 1), look.flat(f"{n}_corem", look.hexc("#ffffff"), 3.0), 0, 24)
    layers = [(1.0, core, None)]
    for k, (r, col, a) in enumerate(((1.5, "#e6f8ff", 0.6), (2.5, "#94dcff", 0.26), (4.0, "#5ab8ff", 0.1))):
        m = _glow(f"{n}_g{k}", look.hexc(col), a)
        o = _sphere(f"{n}_glow{k}", pos, (1, 1, 1), m, 0, 24)
        o.visible_shadow = False
        layers.append((r, o, (m, a)))
    t = [f + round(x * s) for x in (0, 1, 3, 5, 6, 7, 9)]
    t = sorted(set(t))
    t += [t[-1] + 1] * (7 - len(t))
    peak, shrink, collapse, pop = size, size * 0.72, size * 0.25, size * 1.6
    for r, o, ma in layers:
        o.visible_shadow = False
        _attach(o, holder)
        o.location = (0, 0, 0)
        o.matrix_parent_inverse = Matrix.Identity(4)
        anim.key(o, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(o, "scale", t[0], peak * 0.35 * r, "LINEAR")
        anim.key(o, "scale", t[1], peak * r, "BEZIER")
        anim.key(o, "scale", t[2], shrink * r, "BEZIER")
        anim.key(o, "scale", t[3], collapse * (r if r == 1.0 else r * 1.6), "LINEAR")
        anim.key(o, "scale", t[4], 0.001, "CONSTANT")
        if ma:
            m, a = ma
            _alpha_keys(m, [(f - 1, 0.0), (t[0], a), (t[2], a * 1.15), (t[3], min(1.0, a * 1.8)), (t[4], 0.0)])
    # the pop: a flash shell and a thin ring of light at the collapse, then micro-bubbles drifting up
    fm = _glow(f"{n}_flash", look.hexc("#f0fbff"), 0.0)
    fl = _sphere(f"{n}_flash", pos, (1, 1, 1), fm, 0, 20)
    fl.visible_shadow = False
    anim.key(fl, "scale", t[3] - 1, 0.001, "CONSTANT")
    anim.key(fl, "scale", t[3], pop, "LINEAR")
    anim.key(fl, "scale", t[5], pop * 1.4, "LINEAR")
    _alpha_keys(fm, [(t[3] - 1, 0.0), (t[3], 0.8), (t[5], 0.0)])
    rnd = random.Random(f)
    bm = look.fade(f"{n}_micro", look.hexc("#f2fdff"), 0.0)
    _alpha_keys(bm, [(t[4] - 1, 0.0), (t[4], 0.7), (t[6] + round(12 * s), 0.0)])
    for i in range(7):
        mb = _sphere(f"{n}_mb{i}", pos, (1, 1, 1), bm, 0, 10)
        mb.visible_shadow = False
        r = rnd.uniform(0.02, 0.05)
        anim.key(mb, "scale", t[4] - 1, 0.001, "CONSTANT")
        anim.key(mb, "scale", t[4], r)
        anim.key(mb, "location", t[4], pos)
        anim.key(mb, "location", t[6] + round(12 * s), pos + Vector((rnd.uniform(-0.4, 0.4), rnd.uniform(-0.3, 0.3),
                                                                     rnd.uniform(0.5, 1.2))))
    return holder


def shock(rig, f, slow=1.0, radius=1.3, color="#d8f6ff"):
    """A small water shock ring that races out from the claw tip, square to the jet, and fades."""
    s = max(1.0, slow)
    pos, d = _jet(rig, f + 1)
    ring = anim.shockwave(tuple(pos), f, frames=round(7 * s), radius=radius, color=color)
    ring.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    ring.visible_shadow = False
    return ring


def crack(t, f, frames=5):
    """The crack runs up the front glass: a starburst at the impact point on frame f, the main line from the bottom
    to the rim in `frames` frames, and the branches snapping out as the main line passes them (all done by
    f + frames + 1)."""
    cr = t["crack"]
    n = len(cr) // 2
    for i in range(n):
        if i == 0:
            start, dur = f, frames
        elif i <= 5:                                   # the starburst
            start, dur = f, 1
        else:                                          # the branches, low to high
            start, dur = f + min(frames - 1, 1 + 2 * (i - 6)), 2
        for o in cr[2 * i:2 * i + 2]:
            cu = o.data
            cu.bevel_factor_end = 0.0
            cu.keyframe_insert("bevel_factor_end", frame=start - 1)
            cu.bevel_factor_end = 0.02
            cu.keyframe_insert("bevel_factor_end", frame=start)
            cu.bevel_factor_end = 1.0
            cu.keyframe_insert("bevel_factor_end", frame=start + dur)
            for fc in anim.all_fcurves(cu.animation_data.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"


# --------------------------------------------------------------------------- ambient life and the placeholder finger
def bubbles(origin, f0, f1, n=8, seed=1, rise=4.0, spread=0.5):
    """Little air bubbles rising from the gravel (ambient life in every tank shot). Seeded; already on their way at
    f0."""
    rnd = random.Random(seed)
    m = look.fade("amb_bubble", look.hexc("#f4fdff"), 0.6)
    for i in range(n):
        x, y = origin[0] + rnd.uniform(-spread, spread), origin[1] + rnd.uniform(-spread * 0.4, spread * 0.4)
        b = _sphere(f"amb_bub{seed}_{i}", (x, y, origin[2]), (1, 1, 1), m, 0, 12)
        b.visible_shadow = False
        b.scale = [rnd.uniform(0.03, 0.07)] * 3
        dur = rnd.uniform(1.4, 2.2) * (f1 - f0)
        start = f0 - rnd.uniform(0.0, 0.7) * dur
        anim.key(b, "location", start, (x, y, origin[2]), "LINEAR")
        anim.key(b, "location", start + dur, (x + rnd.uniform(-0.2, 0.2), y, origin[2] + rise), "LINEAR")


def finger(touch, taps, away=(1.7, -1.2, 1.5)):
    """A simple placeholder fingertip (Kai's helper supplies the real hand) that comes in from the upper right,
    outside the glass, and taps the glass at `touch` on each frame in `taps`. Each tap sends a small ripple ring
    across the glass. Returns the finger's root empty."""
    skin = look.toon("finger_skin", look.hexc("#f3c6a5"))
    nail = look.toon("finger_nail", look.hexc("#ffe6df"))
    c = Vector((touch[0], TANK_FRONT - 0.19, touch[2]))          # fingertip centre: the pad just touches the glass
    d = Vector((0.7, -0.4, 0.6)).normalized()                  # along the finger, out toward the hand
    root = _empty("finger_root", c, size=0.3)
    fo = sdf.build("finger", [(sdf.C(c, c + d * 2.2, 0.18, 0.21), skin.name, None)], res=0.03, pad=0.1, smooth_iter=6)
    look.outline(fo, 0.016)
    _attach(fo, root)
    _mark("finger_nail", [sdf.E(c + d * 0.16 + Vector((0, -0.12, 0.08)), (0.12, 0.05, 0.1))], nail, root, res=0.012,
          line=0.008)
    lift = c + Vector((0.1, -0.28, 0.12))
    far = c + Vector(away)
    anim.key(root, "location", 1, far)
    anim.key(root, "location", taps[0] - 3, lift)
    for t in taps:
        anim.key(root, "location", t, c, "LINEAR")
        anim.key(root, "location", t + 2, lift)
        ring = anim.shockwave((c.x, TANK_FRONT - 0.03, c.z), t, frames=6, radius=0.7, color="#ffffff")
        ring.rotation_euler = (math.pi / 2, 0, 0)
        ring.visible_shadow = False
    anim.key(root, "location", taps[-1] + 9, far)
    return root


# --------------------------------------------------------------------------- Episode 1 shots (EP01_SHOTS.md)
# Frames at 24 fps. Each sequence is one continuous scene, so consecutive shots cut on matching action:
#   "tap"   S04a + S04b = 3.03 s  "My favourite animal was this little guy. | The pistol shrimp."
#   "snap"  S05a + S05b = 4.35 s  "Its claw snaps so fast, | it makes a bubble ..."  then S06 = 2.33 s
#   "crack" S08 = 0.38 s          "Snap."
# S05 is split at the comma (in the voiced take "fast," ends at 1.40 s and the next word starts at 1.66 s). S04's
# split point is an estimate: change LENGTHS and only the boundary moves.
LENGTHS = dict(S04a=42, S04b=31, S05a=37, S05b=67, S06=56, S08=9)
ORDER = dict(tap=["S04a", "S04b"], snap=["S05a", "S05b", "S06"], crack=["S08"])
SUBJECT_PASS = ("S08",)                                        # shots that also render the shrimp alone


def shot_range(sid):
    """(sequence, first frame, last frame) of a shot inside its sequence."""
    for seq, ids in ORDER.items():
        f = 1
        for k in ids:
            if k == sid:
                return seq, f, f + LENGTHS[k] - 1
            f += LENGTHS[k]
    raise KeyError(sid)


def _camera(name, loc, target, lens, focus=None, fstop=0.15):
    """A locked camera aimed at `target`. fstop 0.15 gives the anime-strength background blur (HELPERS.md)."""
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    if focus is not None:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = focus
        cam.data.dof.aperture_fstop = fstop
    return cam


def _stage(turn, w, h, samples, crack_x=-2.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = look.render_setup(w, h, samples)
    look.world(sky="#16344c", horizon="#2f6680", fill="#c4ecff", fill_strength=0.6)
    look.sun(elev=70, azim=-30, energy=4.0, color="#f2fbff")
    t = tank(crack_x=crack_x)
    rig = build((0.3, -0.2, 0.0), turn=turn)
    return sc, t, rig


def _breathe(rig, f0, f1, period=32, amount=0.012):
    """Breathing, antenna wobble and a lazy tail fan, without the random blinks of anim.idle (shots place blinks)."""
    f = f0
    while f <= f1:
        anim.squash(rig["body"], f, amount)
        anim.squash(rig["body"], f + period // 2, -amount)
        anim.key(rig["tail"], "rotation_euler", f, (0, 0.0, 0))
        anim.key(rig["tail"], "rotation_euler", f + period // 2, (0, 0.06, 0))
        f += period
    for i, a in enumerate(rig["antennae"]):
        f = f0 + i * 5
        while f <= f1:
            anim.key(a, "rotation_euler", f, (0.12, 0.0, (-1) ** i * 0.08))
            anim.key(a, "rotation_euler", f + period // 2, (-0.08, 0.0, -(-1) ** i * 0.05))
            f += period


def _neutral(rig, f):
    anim.key(rig["hinge"], "rotation_euler", f, (0, 0.08, 0))
    anim.key(rig["shoulder"], "rotation_euler", f, (0, 0, 0))
    anim.key(rig["tail"], "rotation_euler", f, (0, 0, 0))
    anim.squash(rig["body"], f, 0.0)
    for a in rig["antennae"]:
        anim.key(a, "rotation_euler", f, (0, 0, 0))
    for e in rig["eyes"]:
        anim.key(e, "scale", f, (1, 1, 1))


def _seq_tap(sc, t, rig):
    """S04a: Kai's finger taps the glass twice; the shrimp (facing away) startles, then turns to the glass.
    S04b: the close-up; it shows off its huge claw (the finger opens a little and shuts), bubbles rise."""
    root = rig["root"]
    anim.key(root, "rotation_euler", 1, (0, 0, math.radians(-35)))
    _breathe(rig, 1, 80)
    finger((0.95, 0, 1.55), (7, 12))
    reaction(rig, 14, hold=4)
    anim.key(root, "rotation_euler", 17, (0, 0, math.radians(-35)))
    anim.key(root, "rotation_euler", 31, (0, 0, math.radians(25)))        # turns to face the glass
    _neutral(rig, 28)
    anim.blink(rig, 36)
    anim.key(rig["hinge"], "rotation_euler", 48, (0, 0.08, 0))
    anim.key(rig["hinge"], "rotation_euler", 54, (0, 0.55, 0))
    anim.key(rig["hinge"], "rotation_euler", 64, (0, 0.55, 0))
    anim.key(rig["hinge"], "rotation_euler", 68, (0, 0.08, 0))
    anim.blink(rig, 61)
    bubbles((-0.9, -0.9, 0.0), 1, 73, n=7, seed=3)
    bubbles((1.4, 0.6, 0.0), 1, 73, n=5, seed=4)
    anim.on_twos([rig["body"], rig["tail"], rig["shoulder"], rig["hinge"], root, *rig["eyes"], *rig["antennae"]])
    return dict(
        S04a=_camera("cam_S04a", (0.6, -8.8, 1.25), (0.2, -1.0, 0.95), 38, rig["body"], 0.4),
        S04b=_camera("cam_S04b", (-2.4, -6.2, 0.85), (-0.95, -0.95, 0.42), 42, rig["shoulder"], 0.3))


def _seq_snap(sc, t, rig, slow=12.0):
    """S05a: slow motion, the claw opens wide, holds, and shuts (6 frames). S05b: the cavitation bubble swells
    white-hot, shrinks and collapses (flash at the collapse); the shock ring spreads; slow push-in. S06: the glow
    fades into micro-bubbles in the water; the shrimp blinks."""
    _, _, end_a = shot_range("S05a")
    shut = end_a                                           # the finger closes exactly on the cut to S05b
    _breathe(rig, 1, 170, period=40, amount=0.008)
    hg, sh, body, tail = rig["hinge"], rig["shoulder"], rig["body"], rig["tail"]
    anim.key(hg, "rotation_euler", 1, (0, 0.08, 0))
    anim.key(hg, "rotation_euler", 24, (0, OPEN, 0))
    anim.key(hg, "rotation_euler", shut - 6, (0, OPEN, 0), "LINEAR")
    anim.key(hg, "rotation_euler", shut, (0, 0.0, 0), "CONSTANT")
    anim.key(sh, "rotation_euler", 1, (0, 0, 0))
    anim.key(sh, "rotation_euler", 24, (0, -0.08, 0.1))
    anim.key(sh, "rotation_euler", shut, (0, 0.05, -0.06), "LINEAR")
    anim.key(sh, "rotation_euler", shut + 40, (0, 0, 0))
    anim.key(body, "location", shut - 1, (0, 0, 0))
    anim.key(body, "location", shut + 12, (0.1, 0, 0.015))
    anim.key(body, "location", shut + 60, (0, 0, 0))
    anim.key(tail, "rotation_euler", shut, (0, 0, 0))
    anim.key(tail, "rotation_euler", shut + 10, (0, 0.4, 0))
    anim.key(tail, "rotation_euler", shut + 50, (0, 0, 0))
    bubble(rig, shut, slow=slow)
    shock(rig, shut, slow=slow, radius=1.6)
    _, s06, _ = shot_range("S06")
    anim.blink(rig, s06 + 22)
    bubbles((-0.6, -0.8, 0.0), 1, 160, n=6, seed=5)
    anim.on_twos([rig["body"], rig["tail"], rig["shoulder"], *rig["eyes"], *rig["antennae"]])   # hinge on 1s
    c05b = _camera("cam_S05b", (-2.7, -5.9, 0.85), (-1.75, -1.6, 0.45), 45, rig["tip"], 0.3)
    _, b0, b1 = shot_range("S05b")
    fwd = c05b.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    anim.key(c05b, "location", b0, c05b.location.copy(), "LINEAR")
    anim.key(c05b, "location", b1, c05b.location + fwd * 0.9, "LINEAR")
    return dict(
        S05a=_camera("cam_S05a", (0.1, -4.3, 0.62), (-1.25, -1.4, 0.42), 45, rig["hinge"], 0.3),
        S05b=c05b,
        S06=_camera("cam_S06", (-2.6, -6.4, 0.9), (-1.1, -1.0, 0.45), 42, rig["shoulder"], 0.3))


def _seq_crack(sc, t, rig):
    """S08 ("Snap.", 9 frames): the claw is cocked on frame 1 and shuts on frame 2; then the shrimp FREEZES in its
    snapped pose while the effects move: bubble flash, ring, and the crack running up the glass. 2-frame shake."""
    hg = rig["hinge"]
    reaction(rig, 1, hold=0)
    anim.key(hg, "rotation_euler", 1, (0, OPEN, 0), "CONSTANT")
    anim.key(hg, "rotation_euler", 2, (0, 0.0, 0), "CONSTANT")
    anim.key(rig["shoulder"], "rotation_euler", 2, (0, 0.06, -0.08), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", 2, (0, 0.55, 0), "CONSTANT")
    bubble(rig, 2)
    shock(rig, 2)
    crack(t, 2, frames=5)
    cam = _camera("cam_S08", (-0.9, -6.8, 1.3), (-0.9, -1.6, 1.1), 32, t["root"], 0.5)
    cam.data.dof.focus_object = None
    cam.data.dof.focus_distance = (Vector((-1.3, TANK_FRONT, 1.0)) - cam.location).length
    anim.shake(cam, 2, frames=2, amp=0.08)
    return dict(S08=cam)


def shot(sid, w=720, h=1280, samples=16):
    """Build the whole scene for one Episode 1 shot (S04a, S04b, S05a, S05b, S06, S08): tank, shrimp, motion, camera,
    and set the scene's frame range to that shot. Returns dict(scene, camera, frames, rig, tank, subject). For the
    shots in SUBJECT_PASS, render the frames, call subject_pass(info), and render them again into subject/."""
    seq, f0, f1 = shot_range(sid)
    turn, crack_x = (45, -1.3) if seq == "crack" else (25, -2.0)    # S08: turned to the glass, the claw at it
    sc, t, rig = _stage(math.radians(turn), w, h, samples, crack_x)
    cams = dict(tap=_seq_tap, snap=_seq_snap, crack=_seq_crack)[seq](sc, t, rig)
    sc.camera = cams[sid]
    sc.frame_start, sc.frame_end = f0, f1
    sc.frame_set(f0)
    return dict(scene=sc, camera=cams[sid], frames=(f0, f1), rig=rig, tank=t, subject=[rig["root"]])


def subject_pass(info):
    """Switch a built shot to its subject pass: the shrimp alone on a transparent film (no contact shadow)."""
    sc = look.subject_only(info["subject"])
    bpy.data.objects[f"{info['rig']['name']}_shadow"].hide_render = True
    return sc
