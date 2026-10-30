"""The puff-shrimp (Episode 1-2's creature, our own design): a chubby aqua body with a cream belly, a fluffy cream
collar, big glossy eyes, two antennae with coral tips, four stubby legs, a coral tail fan, and ONE huge coral pistol
claw on its right side. Built as a small rig of parented objects so shots can animate it:

    rig = build(loc)   ->  dict(root, body, shoulder, hinge, eyes, antennae)
    root      : moves/turns the whole creature (feet at z=0, facing -Y)
    body      : squash & stretch pivot at the ground (scale z up = stretch, x/y follow to keep volume)
    shoulder  : the claw arm's pivot (rotate X to raise/lower the claw)
    hinge     : the snapping finger's pivot (rotation X: 0 = open, -0.9 = snapped shut)
    eyes      : eye objects (scale z to blink)
    hi        : the upper eye highlights (anim.lids hides them while the lids are down)
    lids      : upper-lid pivots, hidden at rest (scale 0); anim.lids() lowers them for a half-shut, smug look
    antennae  : antenna pivots (small rotations for wobble)
"""
import math

import bpy

from . import look, sdf

AQUA, CREAM, CORAL, BLUSH, INK = "#8fe3d6", "#fff3dc", "#ff7a5c", "#ff9fb4", "#1b1830"


def _empty(name, loc, parent=None):
    """A pivot at `loc` in WORLD space. With a parent, the parent's current transform is cancelled (as _parent does
    for the meshes); before 30 Oct it wasn't, so nested pivots sat at twice their offset: the claw hinge swung the
    snapping finger off the claw and the lids closed in the wrong place (found by bGqrs)."""
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.2
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    if parent:
        bpy.context.view_layer.update()
        e.parent = parent
        e.matrix_parent_inverse = parent.matrix_world.inverted()
    return e


def _parent(o, p):
    o.parent = p
    o.matrix_parent_inverse = p.matrix_world.inverted()


def _sphere(name, loc, scale, mat, line=0.0, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return look.outline(o, line)


def _tube(name, pts, radius, mat, line=0.012):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.object
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return look.outline(o, line)


def _lid(name, loc, scale, mat):
    """An upper eyelid: the top half of a shell just bigger than the eye, in the body colour. Its cut edge gets the
    outline's rim, which draws the dark lid line."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.02], context="VERTS")
    for v in bm.verts:
        v.co.x, v.co.y, v.co.z = v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    look.outline(o, 0.018)
    md = o.modifiers["outline"]
    md.use_rim = True                                           # the rim along the cut edge is the lid line
    md.material_offset_rim = md.material_offset
    return o


def build(loc=(0, 0, 0), name="puff"):
    hx = look.hexc
    look.toon(f"{name}_aqua", hx(AQUA))
    look.toon(f"{name}_cream", hx(CREAM))
    look.toon(f"{name}_coral", hx(CORAL))
    eye_m = look.toon(f"{name}_eye", hx(INK), shade=0.8, gloss=True)
    hi_m = look.flat(f"{name}_hi", (1, 1, 1, 1))
    iris_m = look.flat(f"{name}_iris", hx("#3d6fd6"))           # the lighter colour low in the eye (anime eyes)
    blush_m = look.flat(f"{name}_blush", hx(BLUSH))
    aqua, cream, coral = (bpy.data.materials[f"{name}_{c}"] for c in ("aqua", "cream", "coral"))
    E, C = sdf.E, sdf.C

    root = _empty(f"{name}_root", loc)
    body_pivot = _empty(f"{name}_body", loc, root)
    bpy.context.view_layer.update()
    # body: one smooth shape (round body, belly patch, stubby legs, tail fan)
    body = sdf.build(f"{name}_bodymesh", [
        (E((0, 0, 1.0), (1.0, 0.92, 0.95)), aqua.name, None),
        (E((-0.5, -0.4, 0.18), (0.2, 0.22, 0.2)), aqua.name, 0.15),
        (E((0.5, -0.4, 0.18), (0.2, 0.22, 0.2)), aqua.name, 0.15),
        (E((-0.45, 0.35, 0.18), (0.2, 0.22, 0.2)), aqua.name, 0.15),
        (E((0.45, 0.35, 0.18), (0.2, 0.22, 0.2)), aqua.name, 0.15),
        (E((0, 0.98, 0.72), (0.3, 0.14, 0.42)), coral.name, 0.1),
        (E((0.32, 0.92, 0.66), (0.24, 0.12, 0.36)), coral.name, 0.1),
        (E((-0.32, 0.92, 0.66), (0.24, 0.12, 0.36)), coral.name, 0.1),
    ], k=0.12, res=0.03)
    look.outline(body, 0.025)
    body.location = (body.location.x + loc[0], body.location.y + loc[1], body.location.z + loc[2])
    _parent(body, body_pivot)
    # the belly: its own smooth shape pressed into the front of the body, so its edge is one clean curve
    bel = _sphere(f"{name}_belly", (loc[0], loc[1] - 0.5, loc[2] + 0.82), (0.62, 0.48, 0.58), cream, 0.0, 48)
    _parent(bel, body_pivot)
    # fluffy collar
    for i in range(14):
        a = i / 14 * 2 * math.pi
        f = _sphere(f"{name}_fluff{i}", (loc[0] + math.cos(a) * 0.82, loc[1] + math.sin(a) * 0.74,
                                         loc[2] + 1.55 + 0.05 * math.sin(3 * a)), (0.26, 0.26, 0.2), cream, 0.016, 20)
        _parent(f, body_pivot)
    # face
    eyes, lids, his = [], [], []
    for sx in (-1, 1):
        ex = sx * 0.36
        piv = _empty(f"{name}_eyepiv{sx}", (loc[0] + ex, loc[1] - 0.78, loc[2] + 1.2), body_pivot)
        bpy.context.view_layer.update()
        e = _sphere(f"{name}_eye{sx}", (loc[0] + ex, loc[1] - 0.78, loc[2] + 1.2), (0.23, 0.12, 0.31), eye_m, 0.02)
        cres = _sphere(f"{name}_iris{sx}", (loc[0] + ex, loc[1] - 0.86, loc[2] + 1.08), (0.15, 0.05, 0.1), iris_m, 0, 20)
        h1 = _sphere(f"{name}_hi{sx}", (loc[0] + ex + 0.08, loc[1] - 0.89, loc[2] + 1.33), (0.08, 0.03, 0.09), hi_m, 0, 16)
        h2 = _sphere(f"{name}_hi2{sx}", (loc[0] + ex - 0.07, loc[1] - 0.9, loc[2] + 1.1), (0.04, 0.02, 0.04), hi_m, 0, 12)
        for o in (e, cres, h1, h2):
            _parent(o, piv)
        eyes.append(piv)
        his.append(h1)
        lp = _empty(f"{name}_lidpiv{sx}", (loc[0] + ex, loc[1] - 0.78, loc[2] + 1.2), piv)
        bpy.context.view_layer.update()
        lid = _lid(f"{name}_lid{sx}", (loc[0] + ex, loc[1] - 0.78, loc[2] + 1.2), (0.233, 0.124, 0.313), aqua)
        _parent(lid, lp)
        lp.scale = (0.001, 0.001, 0.001)                           # hidden at rest
        lids.append(lp)
        b = _sphere(f"{name}_blush{sx}", (loc[0] + sx * 0.62, loc[1] - 0.7, loc[2] + 0.98), (0.14, 0.04, 0.08), blush_m, 0, 16)
        _parent(b, body_pivot)
    mo = _sphere(f"{name}_mouth", (loc[0], loc[1] - 0.87, loc[2] + 0.9), (0.1, 0.03, 0.07), eye_m, 0, 16)
    _parent(mo, body_pivot)
    antennae = []
    for sx in (-1, 1):
        base = (loc[0] + sx * 0.25, loc[1] - 0.2, loc[2] + 1.82)
        piv = _empty(f"{name}_antpiv{sx}", base, body_pivot)
        bpy.context.view_layer.update()
        t = _tube(f"{name}_ant{sx}", [base, (base[0] + sx * 0.2, base[1] - 0.15, base[2] + 0.55),
                                      (base[0] + sx * 0.6, base[1], base[2] + 0.85)], 0.035, aqua)
        tip = _sphere(f"{name}_antip{sx}", (base[0] + sx * 0.6, base[1], base[2] + 0.85), (0.09, 0.09, 0.09), coral, 0.014, 16)
        _parent(t, piv)
        _parent(tip, piv)
        antennae.append(piv)
    # the claw: shoulder pivot -> arm + palm + fixed finger (one smooth shape) -> hinge -> snapping finger
    sh_loc = (loc[0] - 0.82, loc[1] - 0.1, loc[2] + 1.05)
    shoulder = _empty(f"{name}_shoulder", sh_loc, body_pivot)
    bpy.context.view_layer.update()
    arm = sdf.build(f"{name}_claw", [
        (C((-0.8, -0.1, 1.0), (-1.45, -0.3, 1.75), 0.15, 0.17), aqua.name, None),
        (E((-1.7, -0.4, 2.2), (0.62, 0.5, 0.66)), coral.name, 0.18),
        (C((-1.38, -0.42, 2.62), (-1.25, -0.45, 3.3), 0.17, 0.09), coral.name, 0.1),
        (E((-1.95, -0.86, 2.1), (0.17, 0.06, 0.17)), cream.name, 0.02),
    ], k=0.15, res=0.03)
    look.outline(arm, 0.022)
    arm.location = (arm.location.x + loc[0], arm.location.y + loc[1], arm.location.z + loc[2])
    _parent(arm, shoulder)
    hinge = _empty(f"{name}_hinge", (loc[0] - 1.95, loc[1] - 0.42, loc[2] + 2.65), shoulder)
    bpy.context.view_layer.update()
    finger = sdf.build(f"{name}_dactyl", [
        (C((-1.95, -0.42, 2.65), (-2.02, -0.44, 3.2), 0.21, 0.17), coral.name, None),
        (C((-2.02, -0.44, 3.2), (-1.7, -0.45, 3.58), 0.17, 0.1), coral.name, None),
    ], k=0.1, res=0.03)
    look.outline(finger, 0.02)
    finger.location = (finger.location.x + loc[0], finger.location.y + loc[1], finger.location.z + loc[2])
    _parent(finger, hinge)
    look.blob_shadow(f"{name}_shadow", (loc[0] - 0.2, loc[1] - 0.05, loc[2] + 0.075), (1.35, 1.1), root)
    return dict(root=root, body=body_pivot, shoulder=shoulder, hinge=hinge, eyes=eyes, lids=lids, hi=his, antennae=antennae)
