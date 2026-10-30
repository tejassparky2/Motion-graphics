"""The tuftwing (Episode 1, our own design): a palm-sized, very round, pale-butter-yellow fluffball of a bird with a
scalloped cream chest ruff, tiny stubby wings with teal tips, a swept-back teal head crest, big glossy eyes, a tiny
amber beak, peach cheeks, and three long ribbon tail feathers (teal, peach, lilac) that end in paddles.

Its creepy tell: its shadow is far too big. Under it lies a huge, spread-winged shadow, like a giant bird's: a dark
painted decal, not a real cast shadow (the bird itself casts none). The shadow stays on the ground when the bird hops,
and it beats its wings slowly, a beat behind the bird's flutters.

    rig = build(loc)   ->  dict(root, lift, body, head, eyes, crest, wings, tail, shadow)
    root    : moves/turns the whole creature and its shadow (feet at z=0, facing -Y)
    lift    : height above the ground (hops); the shadow does not follow it
    body    : squash & stretch pivot at the feet
    head    : head pivot at the centre of the ball (rotation Y tilts the head, Z turns it)
    eyes    : eye pivots (scale z to blink)
    crest   : crest pivot on top of the head (small X rotations for bounce)
    wings   : [left, right] shoulder pivots (rotation Y = -side * angle lifts a wing out and up; side -1 = left)
    tail    : where the three ribbons leave the body (rotation Z sways them, X lifts them)
    shadow  : the giant shadow decal (scale x below 1 folds its wings in)

    idle(rig, f0, f1)  breathing, head tilts, wing flutters, blinks, tail sway, the shadow's slow beats
    hop(rig, f)        crouch, spring, flap, land four holds later; the shadow stays put and beats once
Both hold poses like TV anime (anim.on_twos, with its default step); flaps and blinks are timed to that step.

At root scale 1 the ball is ~1.3 units across (about 2/3 of the puff-shrimp); scale the root to make it palm-sized
next to people. The shadow's wingspan is `shadow_span` units (default 7).
"""
import math
import random

import bmesh
import bpy
import numpy as np
from mathutils import Vector

from . import anim, look, sdf

BUTTER, CREAM, WING, TEAL, PEACH, LILAC = "#fbe7a1", "#fff7e0", "#f5d57e", "#2fbfb0", "#ffb48f", "#c3a4ff"
BEAK, FEET, INK, BLUSH, SHADOW_RGB = "#f2a33c", "#f59a6e", "#1b1830", "#ffa98a", "#1d1828"
CENTER, BALL = (0.0, 0.0, 0.74), (0.64, 0.6, 0.62)         # centre and radii of the ball


def _empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.15
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    if parent:
        _parent(e, parent)
    return e


def _parent(o, p):
    bpy.context.view_layer.update()
    o.parent = p
    o.matrix_parent_inverse = p.matrix_world.inverted()


def _line(o, width):
    """look.outline with high-quality normals for the shell: without them, sliver triangles from marching cubes throw
    long dark spikes through the body."""
    look.outline(o, width)
    m = o.modifiers.get("outline")
    if m:
        m.use_quality_normals = True
    return o


def _sphere(name, loc, scale, mat, line=0.0, seg=32, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.rotation_euler = rot                                    # turns about its own centre
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return _line(o, line)


def _catmull(pts, n):
    """n points along a Catmull-Rom spline through pts."""
    p = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]])
    segs = len(pts) - 1
    out = []
    for t in np.linspace(0, segs, n):
        i = min(int(t), segs - 1)
        u = t - i
        p0, p1, p2, p3 = p[i], p[i + 1], p[i + 2], p[i + 3]
        out.append(0.5 * (2 * p1 + (p2 - p0) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                          + (3 * p1 - p0 - 3 * p2 + p3) * u ** 3))
    return np.array(out)


def _ribbon_width(t):
    """A stem that swells into a teardrop paddle near the end."""
    stem = 0.08 * (1 - 0.35 * t)
    paddle = 0.3 * math.sin(math.pi * min(1.0, max(0.0, (t - 0.66) / 0.34)))
    return max(stem, paddle) * min(1.0, (1 - t) / 0.04) ** 0.5


def _ribbon(name, ctrl, mat, twist=0.4, tilt=0.7, n=72, thick=0.016, line=0.012):
    """A flat ribbon feather along a spline through `ctrl`, tilted `tilt` radians from upright (so its paddle reads from
    the side and from above) and twisting by `twist` radians from base to tip."""
    P = _catmull(np.asarray(ctrl, float), n)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    verts = []
    for i, (p, t) in enumerate(zip(P, T)):
        s = np.cross(t, (0.0, 0.0, 1.0))
        s /= np.linalg.norm(s)
        u = np.cross(s, t)
        a = math.copysign(tilt, twist) + twist * i / (n - 1)
        side = u * math.cos(a) + s * math.sin(a)
        w = _ribbon_width(i / (n - 1)) / 2
        verts += [tuple(p - side * w), tuple(p + side * w)]
    faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(n - 1)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    s = o.modifiers.new("thick", "SOLIDIFY")
    s.thickness = thick
    s.offset = 0.0
    return _line(o, line)


def _sculpt(name, parts, keep_islands=False, **kw):
    """sdf.build, minus its sliver triangles (and, unless keep_islands, everything but its largest piece), with the
    faces turned outward whichever way marching cubes wound them (with scikit-image 0.26 they come out inward after
    sdf.build's flip, which hides the inverted-hull outline inside the body)."""
    o = sdf.build(name, parts, **kw)
    me = o.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.dissolve_degenerate(bm, dist=kw.get("res", 0.025) * 0.3, edges=bm.edges)
    bad = [v for v in bm.verts if not v.is_manifold]          # pinched "bow-tie" spots: cut them out and patch them
    if bad:
        bmesh.ops.delete(bm, geom=list({f for v in bad for f in v.link_faces}), context="FACES")
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        for _ in range(4):                                    # iron out the patches
            bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    for _ in range(4):                                        # relax spikes (they throw dark folds of outline)
        bm.normal_update()
        for v in bm.verts:
            nb = [e.other_vert(v) for e in v.link_edges]
            if not nb:
                continue
            n = sum((u.normal for u in nb), Vector())
            if not v.is_manifold or (n.length > 0 and v.normal.dot(n.normalized()) < 0.5):
                v.co = sum((u.co for u in nb), Vector()) / len(nb)
    if not keep_islands:                                      # drop tiny bubbles marching cubes finds inside the body
        islands, seen = [], set()
        for f in bm.faces:
            if f in seen:
                continue
            stack, isl = [f], []
            seen.add(f)
            while stack:
                g = stack.pop()
                isl.append(g)
                for e in g.edges:
                    for h in e.link_faces:
                        if h not in seen:
                            seen.add(h)
                            stack.append(h)
            islands.append(isl)
        islands.sort(key=len)
        bmesh.ops.delete(bm, geom=[f for isl in islands[:-1] for f in isl], context="FACES")
    bm.to_mesh(me)
    bm.free()
    c = np.array([p.center[:] for p in me.polygons])
    nr = np.array([p.normal[:] for p in me.polygons])
    if np.mean(np.sum((c - c.mean(0)) * nr, axis=1) > 0) < 0.5:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        me.update()
    return o


def _on_eye(ec, a, radii, dx, dz):
    """The point on the front of an eye (centre ec, turned by `a` about Z) at world offsets dx, dz from its centre, so
    both eyes' highlights sit on the same side."""
    ys = np.linspace(-0.3, 0.0, 600)
    lx = dx * math.cos(a) + ys * math.sin(a)
    ly = -dx * math.sin(a) + ys * math.cos(a)
    inside = (lx / radii[0]) ** 2 + (ly / radii[1]) ** 2 + (dz / radii[2]) ** 2 <= 1
    y = ys[np.argmax(inside)] if inside.any() else 0.0
    return (ec[0] + dx, ec[1] + y, ec[2] + dz)


def _on_ball(d, scale=1.0):
    """The point on the ball's surface in direction d (times `scale`)."""
    d = np.asarray(d, float) / np.linalg.norm(d)
    t = 1.0 / math.sqrt(sum((d[i] / BALL[i]) ** 2 for i in range(3)))
    return tuple(float(v) for v in np.asarray(CENTER) + d * t * scale)


# Feather flicks that break the ball's outline at the cheeks, three a side.
_FLICKS = [(sx * x, y, z) for sx in (-1, 1) for x, y, z in ((0.93, -0.3, 0.2), (0.97, -0.18, -0.02),
                                                            (0.9, -0.12, -0.25))]


# The giant shadow, seen from above with its head toward -Y, in [-1, 1] plane coordinates. Right wing (x > 0): the
# leading edge out to the tip, five splayed primary "fingers", then scalloped secondaries back to the body.
_WING = [(0.06, -0.12), (0.25, -0.21), (0.45, -0.26), (0.65, -0.27), (0.83, -0.24), (0.97, -0.17),
         (0.995, -0.11), (0.88, -0.085), (0.96, -0.01), (0.83, 0.0), (0.9, 0.09), (0.76, 0.07), (0.8, 0.165),
         (0.67, 0.12), (0.69, 0.22), (0.57, 0.15), (0.5, 0.225), (0.42, 0.17), (0.34, 0.225), (0.26, 0.17),
         (0.18, 0.21), (0.1, 0.15), (0.05, 0.08)]
_TAIL = [(-0.07, 0.3), (0.07, 0.3), (0.21, 0.74), (0.13, 0.8), (0.07, 0.73), (0.0, 0.81), (-0.07, 0.73),
         (-0.13, 0.8), (-0.21, 0.74)]
_BEAK = [(-0.045, -0.37), (0.045, -0.37), (0.02, -0.47), (-0.012, -0.56), (-0.022, -0.47)]


def shadow_alpha(res=1024):
    """Alpha mask of the giant shadow (rows run along +Y, columns along +X): a soft painted edge and a slightly
    darker core."""
    from scipy import ndimage
    from skimage import draw

    m = np.zeros((res, res), bool)

    def px(x, y):
        return (np.asarray(y, float) + 1) / 2 * (res - 1), (np.asarray(x, float) + 1) / 2 * (res - 1)

    def poly(pts):
        pts = np.asarray(pts, float)
        rr, cc = draw.polygon(*px(pts[:, 0], pts[:, 1]), shape=m.shape)
        m[rr, cc] = True

    def ell(cx, cy, rx, ry):
        rr, cc = draw.ellipse(*px(cx, cy), ry * (res - 1) / 2, rx * (res - 1) / 2, shape=m.shape)
        m[rr, cc] = True

    ell(0.0, 0.04, 0.13, 0.33)                                # body
    ell(0.0, -0.31, 0.105, 0.11)                              # head
    poly(_BEAK)
    poly(_TAIL)
    for s in (-1, 1):
        poly([(s * x, y) for x, y in _WING])
    soft = ndimage.gaussian_filter(m.astype(np.float32), 1.6)
    core = np.clip(ndimage.distance_transform_edt(m) / (0.05 * res), 0, 1)
    return soft * (0.58 + 0.14 * core)


def _giant_shadow(name, span, parent):
    res = 1024
    rgba = np.ones((res, res, 4), np.float32)
    rgba[..., 3] = shadow_alpha(res)
    img = bpy.data.images.new(f"{name}_mask", res, res, alpha=True)
    img.pixels.foreach_set(rgba.ravel())
    img.pack()
    m = bpy.data.materials.new(f"{name}_mat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = look.hexc(SHADOW_RGB)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.extension = "CLIP"
    L(tex.outputs["Alpha"], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 0.012))
    sh = bpy.context.object
    sh.name = name
    sh.scale = (span / 2, span / 2, 1)
    bpy.ops.object.transform_apply(scale=True)
    sh.data.materials.append(m)
    _parent(sh, parent)
    return sh


def build(loc=(0, 0, 0), name="tuft", shadow_span=7.0):
    hx = look.hexc
    butter, cream, wing_m = look.toon(f"{name}_butter", hx(BUTTER)), look.toon(f"{name}_cream", hx(CREAM)), \
        look.toon(f"{name}_wing", hx(WING))
    teal, peach, lilac = look.toon(f"{name}_teal", hx(TEAL)), look.toon(f"{name}_peach", hx(PEACH)), \
        look.toon(f"{name}_lilac", hx(LILAC))
    beak_m, feet_m = look.toon(f"{name}_beak", hx(BEAK)), look.toon(f"{name}_feet", hx(FEET))
    eye_m = look.toon(f"{name}_eye", hx(INK), gloss=True)
    hi_m, blush_m = look.flat(f"{name}_hi", (1, 1, 1, 1)), look.flat(f"{name}_blush", hx(BLUSH))
    E, C = sdf.E, sdf.C

    root = _empty(f"{name}_root", (0, 0, 0))                  # built at the origin, moved to `loc` at the end
    lift = _empty(f"{name}_lift", (0, 0, 0), root)
    body = _empty(f"{name}_body", (0, 0, 0), lift)
    head = _empty(f"{name}_head", CENTER, body)
    # the ball: one smooth shape with feather flicks at the cheeks and a scalloped cream ruff low on the chest
    parts = [(E(CENTER, BALL), butter.name, None)]
    for d in _FLICKS:
        tip = np.asarray(_on_ball(d, 1.17)) + (0, 0.03, -0.05)
        parts.append((C(_on_ball(d, 0.9), tip, 0.075, 0.012), butter.name, 0.03))
    parts.append((E((0, -0.36, 0.47), (0.38, 0.27, 0.3)), cream.name, 0.06))
    for i in range(-2, 3):
        parts.append((E((i * 0.14, -0.42 + 0.03 * abs(i), 0.24 + 0.04 * abs(i)), (0.095, 0.09, 0.08)), cream.name,
                      0.04))
    ball = _sculpt(f"{name}_ball", parts, k=0.08, res=0.022, smooth_iter=20)
    _line(ball, 0.022)
    _parent(ball, head)
    # crest: three long teal plumes rising from the forehead and sweeping back, the middle one tallest
    crest = _empty(f"{name}_crest", (0, -0.1, 1.32), head)
    fan = []
    for x, h, r in ((0.0, 1.0, 0.062), (-0.1, 0.72, 0.046), (0.1, 0.72, 0.046)):
        pts = [(x, -0.16, 1.27), (x * 1.3, -0.08, 1.27 + 0.3 * h), (x * 1.9, 0.12 + 0.05 * (1 - h), 1.27 + 0.47 * h),
               (x * 2.3, 0.34 - 0.08 * (1 - h), 1.27 + 0.45 * h)]
        radii = (r, r * 0.8, r * 0.55, 0.012)
        fan += [(C(pts[i], pts[i + 1], radii[i], radii[i + 1]), teal.name, 0.012 if i == 0 and x else None)
                for i in range(3)]
    plumes = _sculpt(f"{name}_plumes", fan, k=0.03, res=0.012, smooth_iter=10)
    _line(plumes, 0.016)
    _parent(plumes, crest)
    # face: big glossy eyes turned along the ball's curve, each with a big and a small highlight on the same side
    eyes = []
    for sx in (-1, 1):
        a, ec, er = sx * 0.4, (sx * 0.25, -0.515, 0.86), (0.13, 0.06, 0.17)
        piv = _empty(f"{name}_eyepiv{sx}", ec, head)
        for o in (_sphere(f"{name}_eye{sx}", ec, er, eye_m, 0.016, 32, (0, 0, a)),
                  _sphere(f"{name}_hi{sx}", _on_eye(ec, a, er, -0.035, 0.06), (0.045, 0.02, 0.055), hi_m, 0, 16,
                          (0, 0, a)),
                  _sphere(f"{name}_hi2{sx}", _on_eye(ec, a, er, 0.045, -0.06), (0.024, 0.014, 0.024), hi_m, 0, 12,
                          (0, 0, a))):
            _parent(o, piv)
        eyes.append(piv)
        b = _sphere(f"{name}_blush{sx}", _on_ball((sx * 0.75, -0.62, -0.24), 1.01), (0.11, 0.035, 0.065), blush_m, 0,
                    16, (0, 0, sx * 0.88))
        _parent(b, head)
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.075, depth=0.15, location=(0, -0.63, 0.73),
                                    rotation=(math.radians(100), 0, 0))
    beak = bpy.context.object
    beak.name = f"{name}_beak"
    beak.data.materials.append(beak_m)
    for p in beak.data.polygons:
        p.use_smooth = True
    _line(beak, 0.012)
    _parent(beak, head)
    # tiny stubby wings lying along the sides, each tipped with a teal feather pointing back and down
    wings = []
    for sx in (-1, 1):
        piv = _empty(f"{name}_wingpiv{sx}", (sx * 0.6, 0.0, 0.86), body)
        w = _sculpt(f"{name}_wing{sx}", [
            (E((sx * 0.65, 0.0, 0.76), (0.075, 0.17, 0.16)), wing_m.name, None),
            (E((sx * 0.67, 0.15, 0.6), (0.065, 0.15, 0.13)), wing_m.name, None),
            (E((sx * 0.67, 0.27, 0.45), (0.055, 0.13, 0.085)), teal.name, 0.03),
        ], k=0.07, res=0.014, smooth_iter=12)
        _line(w, 0.016)
        _parent(w, piv)
        wings.append(piv)
    feet = _sculpt(f"{name}_feet", [
        (E((sx * 0.17, -0.1, 0.06), (0.075, 0.11, 0.055)), feet_m.name, None) for sx in (-1, 1)
    ], keep_islands=True, k=0.0, res=0.014, smooth_iter=8)
    _line(feet, 0.012)
    _parent(feet, body)
    # three long ribbon tail feathers ending in paddles: teal trails straight back, peach and lilac sweep out
    tail = _empty(f"{name}_tail", (0, 0.5, 0.56), body)
    for nm, mat, ctrl, tw in (
            ("teal", teal, [(0, 0.44, 0.6), (0, 0.8, 0.9), (0, 1.2, 1.0), (0, 1.6, 0.85), (0, 1.95, 0.6),
                            (0, 2.2, 0.45)], 0.3),
            ("peach", peach, [(-0.06, 0.44, 0.56), (-0.25, 0.75, 0.72), (-0.6, 1.0, 0.78), (-0.95, 1.22, 0.62),
                              (-1.2, 1.4, 0.42), (-1.38, 1.55, 0.3)], -0.3),
            ("lilac", lilac, [(0.06, 0.44, 0.56), (0.27, 0.78, 0.76), (0.64, 1.06, 0.84), (1.0, 1.3, 0.68),
                              (1.25, 1.5, 0.46), (1.42, 1.66, 0.34)], 0.3)):
        r = _ribbon(f"{name}_tail_{nm}", ctrl, mat, tw)
        _parent(r, tail)
    shadow = _giant_shadow(f"{name}_shadow", shadow_span, root)
    for o in [root] + list(root.children_recursive):
        if o.type == "MESH":
            o.visible_shadow = False                          # its only shadow is the giant one
    root.location = loc
    return dict(root=root, lift=lift, body=body, head=head, eyes=eyes, crest=crest, wings=wings, tail=tail,
                shadow=shadow)


def _step():
    """How many frames each pose holds in this series (anim.on_twos's default step)."""
    return anim.on_twos.__defaults__[0]


def _animated(rig):
    return [rig[k] for k in ("lift", "body", "head", "crest", "tail", "shadow")] + rig["eyes"] + rig["wings"]


def flutter(rig, f, flaps=3, amount=1.0):
    """A burst of quick wing flaps from frame f, one held pose up and one down per flap; the giant shadow answers
    with one slow beat."""
    st = _step()
    f -= f % st                                               # land the poses on the frames the step holds
    for i in range(flaps):
        for sx, w in zip((-1, 1), rig["wings"]):
            anim.key(w, "rotation_euler", f + 2 * st * i, (0, 0, 0))
            anim.key(w, "rotation_euler", f + 2 * st * i + st, (0, -sx * amount, 0))
    for w in rig["wings"]:
        anim.key(w, "rotation_euler", f + 2 * st * flaps, (0, 0, 0))
    beat(rig, f + 2)


def beat(rig, f, frames=16):
    """The shadow's own wing beat, slow and heavy: its wings fold in and spread out again."""
    sh = rig["shadow"]
    anim.key(sh, "scale", f, (1, 1, 1))
    anim.key(sh, "scale", f + frames * 0.45, (0.84, 1.04, 1))
    anim.key(sh, "scale", f + frames * 0.8, (1.04, 0.99, 1))
    anim.key(sh, "scale", f + frames, (1, 1, 1))


def idle(rig, f0, f1, period=32, seed=1):
    """Breathing, head tilts, wing flutters, blinks, tail sway and crest bob between f0 and f1. The giant shadow drifts
    its head a little on its own and beats its wings after each flutter."""
    rnd = random.Random(seed)
    body, head, tail, crest, sh = rig["body"], rig["head"], rig["tail"], rig["crest"], rig["shadow"]
    f = f0
    while f <= f1:
        anim.squash(body, f, 0.04)
        anim.squash(body, f + period // 2, -0.03)
        anim.key(tail, "rotation_euler", f + 4, (0.05, 0, 0.1))
        anim.key(tail, "rotation_euler", f + 4 + period // 2, (-0.03, 0, -0.1))
        anim.key(crest, "rotation_euler", f + 2, (0.1, 0, 0))
        anim.key(crest, "rotation_euler", f + 2 + period // 2, (-0.08, 0, 0))
        f += period
    f = f0
    while f <= f1:                                            # the shadow turns its head, slowly, by itself
        anim.key(sh, "rotation_euler", f, (0, 0, 0.0))
        anim.key(sh, "rotation_euler", f + 2 * period, (0, 0, 0.06))
        f += 4 * period
    f = f0 + rnd.randint(8, 16)
    side = rnd.choice((-1, 1))
    while f < f1 - 24:
        hold = rnd.randint(14, 24)
        tilt = (0, side * 0.26, side * 0.12)
        anim.key(head, "rotation_euler", f, (0, 0, 0))
        anim.key(head, "rotation_euler", f + 4, tilt)
        anim.key(head, "rotation_euler", f + 4 + hold, tilt)
        anim.key(head, "rotation_euler", f + 10 + hold, (0, 0, 0))
        side = -side
        f += hold + rnd.randint(26, 44)
    f = f0 + rnd.randint(22, 36)
    while f < f1 - 20:
        flutter(rig, f, rnd.choice((2, 3)))
        f += rnd.randint(50, 80)
    f = f0 + rnd.randint(10, 24)
    st = _step()
    while f < f1 - 4:
        anim.blink(rig, f - (f + 1) % st)                     # its shut frame (f + 1) must be a held frame
        f += rnd.randint(36, 64)
    anim.on_twos(_animated(rig))


def hop(rig, f, height=0.75):
    """Crouch, spring at f (moved back to a held frame), flap in the air, land four holds later and settle; the shadow
    stays on the ground and beats once. Returns the landing frame."""
    body, lift, tail, crest = rig["body"], rig["lift"], rig["tail"], rig["crest"]
    st = _step()
    f -= f % st
    air = 4 * st
    land = f + air
    for t, a, interp in ((f - 3 * st, 0.0, "BEZIER"), (f - st, -0.16, "BEZIER"), (f, 0.2, "LINEAR"),
                         (f + st, 0.06, "BEZIER"), (land - st, 0.12, "BEZIER"), (land, -0.2, "LINEAR"),
                         (land + st, 0.05, "BEZIER"), (land + 3 * st, 0.0, "BEZIER")):
        anim.squash(body, t, a, interp)                       # crouch, spring, stretch, land, settle
    for t in range(air + 1):                                  # a parabola, one key a frame
        anim.key(lift, "location", f + t, (0, 0, height * (1 - ((t - air / 2) / (air / 2)) ** 2)), "LINEAR")
    for sx, w in zip((-1, 1), rig["wings"]):
        for t, a in ((f - st, 0.0), (f, 0.6), (f + st, 1.2), (f + 2 * st, 0.3), (f + 3 * st, 1.2), (land, 0.4),
                     (land + 2 * st, 0.0)):
            anim.key(w, "rotation_euler", t, (0, -sx * a, 0))
    for t, a in ((f, 0.0), (f + st, -0.3), (f + 2 * st, 0.0), (land - st, 0.35), (land + st, -0.15),
                 (land + 3 * st, 0.0)):
        anim.key(tail, "rotation_euler", t, (a, 0, 0))
    for t, a in ((f, 0.0), (f + st, -0.25), (f + 2 * st, 0.0), (land + st, 0.3), (land + 3 * st, 0.0)):
        anim.key(crest, "rotation_euler", t, (a, 0, 0))
    beat(rig, f + st)
    anim.on_twos(_animated(rig))
    return land
