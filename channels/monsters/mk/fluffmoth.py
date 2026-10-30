"""The fluffmoth (Episode 1's hovering creature, our own design): a round, fluffy white moth with a cream fur collar,
big glossy black eyes, two big soft feathery antennae and four pastel wings (mint forewings, peach hindwings), each
with a round eye-spot. Its creepy tell: the wing eye-spots BLINK like real eyes (a painted upper and lower lid closes
over each one). Built as a small rig of parented objects so shots can animate it:

    rig = build(loc)   ->  dict(root, hover, body, wings, spots, eyes, antennae, shadow)
    root      : moves/turns the whole creature (ground at z=0, facing -Y)
    hover     : the hover height (animate location z for the bob)
    body      : squash & stretch pivot at the body's centre
    wings     : [fore L, fore R, hind L, hind R]; rotation_euler = (0, flap, sweep), see wing_pose()
    spots     : the four eye-spot discs; their custom property "lid" is 0 (open) .. 1 (shut), see spot_lid(), and
                "glow" 0 .. 1 lights the open irises (the creepy beat's local light, LC4)
    eyes      : the face's eye pivots (scale z to blink, anim.blink works)
    antennae  : antenna pivots at their bases (small rotations to wave)
    shadow    : the blob shadow on the ground

idle(rig, f0, f1) hovers it: wing beats on 1s, body bob, sway and antenna waves on 2s, face blinks, and a slow
eye-spot blink every few seconds.
"""
import math
import random

import bmesh
import bpy
import numpy as np

from . import anim, look, sdf

WHITE, CREAM, MINT, PEACH = "#fdfbff", "#fff0d4", "#a6ecd0", "#ffc6a6"
INK, PLUM, SCLERA, CORAL, TEAL, BLUSH = "#1b1830", "#3a2842", "#fff8ea", "#ff8466", "#2fae96", "#ffaabd"
CRESCENT = "#7b8cf0"     # the lighter colour low in the face eyes (anime eyes)
HOVER = 1.9                     # body centre above the ground
FORE_UP, HIND_UP = 0.12, -0.12   # resting wing tilt (radians, + = tip up)
FORE_SWEEP, HIND_SWEEP = 0.32, 0.42   # resting sweep back (radians)


def _empty(name, loc, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.2
    bpy.context.scene.collection.objects.link(e)
    e.parent = parent
    e.location = loc
    return e


def _attach(o, parent, loc=(0, 0, 0)):
    """Parent with an identity inverse, so `loc` is in the parent's space."""
    o.parent = parent
    o.matrix_parent_inverse.identity()
    o.location = loc
    return o


def _sphere(name, loc, scale, mat, parent, line=0.0, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=(0, 0, 0))
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    look.outline(o, line)
    return _attach(o, parent, loc)


def _flat_mesh(name, pts, mat, thick=0.0, line=0.0):
    """A flat shape in the local X-Z plane from a closed 2D outline [(x, z)], front face toward -Y."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0.0, z)) for x, z in pts]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=es)
    bm.normal_update()
    flip = [f for f in bm.faces if f.normal.y > 0]
    if flip:
        bmesh.ops.reverse_faces(bm, faces=flip)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    if thick:
        s = o.modifiers.new("thick", "SOLIDIFY")
        s.thickness = thick
        s.offset = 0.0
    look.outline(o, line)
    return o


def _catmull(ctrl, n=96):
    """Closed Catmull-Rom curve through 2D control points, sampled at n points."""
    P = np.asarray(ctrl, float)
    m = len(P)
    out = []
    for i in range(n):
        t = i / n * m
        k = int(t)
        u = t - k
        p0, p1, p2, p3 = P[(k - 1) % m], P[k % m], P[(k + 1) % m], P[(k + 2) % m]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
    return [tuple(p) for p in out]


def _disc(name, r, mat, n=48):
    return _flat_mesh(name, [(math.cos(a) * r, math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)],
                      mat)


# --- the eye-spot material: a painted eye whose lids close as the object's "lid" property goes 0 -> 1 ---------------
def _spot_mat(name, wing, iris):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    hx = look.hexc
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new

    def node(kind, **kw):
        n = nt.nodes.new(kind)
        for k, v in kw.items():
            setattr(n, k, v)
        return n

    def inp(n, i, v):
        if isinstance(v, bpy.types.NodeSocket):
            L(v, n.inputs[i])
        else:
            n.inputs[i].default_value = v

    def M(op, a, b=0.0):
        n = node("ShaderNodeMath", operation=op)
        inp(n, 0, a)
        inp(n, 1, b)
        return n.outputs[0]

    def dist(co, c):
        sub = node("ShaderNodeVectorMath", operation="SUBTRACT")
        L(co, sub.inputs[0])
        sub.inputs[1].default_value = (c[0], 0.0, c[1])
        ln = node("ShaderNodeVectorMath", operation="LENGTH")
        L(sub.outputs[0], ln.inputs[0])
        return ln.outputs["Value"]

    def mix(a, b, fac):
        n = node("ShaderNodeMix", data_type="RGBA", blend_type="MIX")
        inp(n, 0, fac)
        inp(n, 6, a)
        inp(n, 7, b)
        return n.outputs[2]

    co = node("ShaderNodeTexCoord").outputs["Object"]
    sep = node("ShaderNodeSeparateXYZ")
    L(co, sep.inputs[0])
    x, z = sep.outputs["X"], sep.outputs["Z"]
    r = dist(co, (0.0, 0.0))
    rp = dist(co, (0.04, -0.06))                               # the pupil looks a little down, toward the viewer
    iris_dark = tuple(c * 0.55 for c in hx(iris)[:3]) + (1,)
    c = mix(hx(PLUM), hx(SCLERA), M("LESS_THAN", r, 0.82))
    c = mix(c, iris_dark, M("LESS_THAN", rp, 0.58))
    c = mix(c, hx(iris), M("LESS_THAN", rp, 0.5))
    c = mix(c, hx(INK), M("LESS_THAN", rp, 0.27))
    c = mix(c, (1, 1, 1, 1), M("LESS_THAN", dist(co, (0.2, 0.22)), 0.13))
    c = mix(c, (1, 1, 1, 1), M("LESS_THAN", dist(co, (-0.14, -0.12)), 0.055))
    # lids: upper edge z = U - k x^2 (arched, flattening as it shuts), lower edge z = -Lo + 0.12 x^2
    lid = node("ShaderNodeAttribute", attribute_type="OBJECT", attribute_name="lid").outputs["Fac"]
    x2 = M("MULTIPLY", x, x)
    U = M("SUBTRACT", 1.25, M("MULTIPLY", lid, 1.22))
    k = M("ADD", 0.05, M("MULTIPLY", M("SUBTRACT", 1.0, lid), 0.3))
    zu = M("SUBTRACT", U, M("MULTIPLY", k, x2))
    Lo = M("SUBTRACT", 1.25, M("MULTIPLY", M("POWER", lid, 3.0), 1.25))
    zl = M("ADD", M("MULTIPLY", Lo, -1.0), M("MULTIPLY", x2, 0.12))
    shut = M("MAXIMUM", M("GREATER_THAN", z, zu), M("LESS_THAN", z, zl))
    c = mix(c, hx(wing), shut)
    lash = M("MAXIMUM", M("LESS_THAN", M("ABSOLUTE", M("SUBTRACT", z, zu)), 0.055),
             M("LESS_THAN", M("ABSOLUTE", M("SUBTRACT", z, zl)), 0.03))
    c = mix(c, hx(PLUM), lash)
    # the series' anime cel shading (as look.toon): one flat colour and one hard, cool shadow tone
    dif = node("ShaderNodeBsdfDiffuse")
    s2r = node("ShaderNodeShaderToRGB")
    ramp = node("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, (*look.SHADOW_TINT, 1)
    cr.elements[1].position, cr.elements[1].color = 0.45, (1, 1, 1, 1)
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], ramp.inputs[0])
    mul = node("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    mul.inputs[0].default_value = 1.0
    L(ramp.outputs[0], mul.inputs[6])
    L(c, mul.inputs[7])
    # "glow" (object property, 0-1): the open iris lights up, unshaded and brighter (the creepy beat's local light)
    glow = node("ShaderNodeAttribute", attribute_type="OBJECT", attribute_name="glow").outputs["Fac"]
    gfac = M("MULTIPLY", glow, M("MULTIPLY", M("LESS_THAN", rp, 0.58), M("SUBTRACT", 1.0, M("MAXIMUM", shut, lash))))
    bright = node("ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    bright.inputs[0].default_value = 1.0
    L(c, bright.inputs[6])
    bright.inputs[7].default_value = (1.8, 1.8, 1.8, 1)
    lit = mix(mul.outputs[2], bright.outputs[2], gfac)
    em = node("ShaderNodeEmission")
    L(lit, em.inputs[0])
    out = node("ShaderNodeOutputMaterial")
    L(em.outputs[0], out.inputs[0])
    return m


# --- wing outlines in wing space (u = out from the root, v = up) ----------------------------------------------------
FORE = [(0.0, 0.1), (0.7, 0.62), (1.4, 0.98), (1.95, 1.08), (2.22, 0.85), (2.17, 0.42), (1.75, 0.05), (1.1, -0.12),
        (0.5, -0.12), (0.12, -0.08)]
HIND = [(0.0, 0.0), (0.55, 0.02), (1.15, -0.12), (1.5, -0.45), (1.5, -0.85), (1.2, -1.1), (0.75, -1.1), (0.38, -0.82),
        (0.12, -0.42)]
# (centre u, v, radius) of each wing's big blinking eye-spot, and its small round dots
FORE_SPOT, HIND_SPOT = (1.38, 0.48, 0.38), (0.86, -0.56, 0.3)
FORE_DOTS, HIND_DOTS = [(0.62, 0.3, 0.065), (1.98, 0.64, 0.07), (1.84, 0.25, 0.055)], [(1.26, -0.9, 0.07), (0.42, -0.5, 0.06)]


def _wing(name, side, ctrl, spot, dots, wmat, smat, dmat, body, root_loc, up, sweep, back):
    pts = [(side * u, v) for u, v in _catmull(ctrl)]
    w = _flat_mesh(name, pts, wmat, thick=0.035, line=0.02)
    _attach(w, body, root_loc)
    w.rotation_euler = (0.0, -side * up, side * sweep)
    u, v, r = spot
    s = _disc(f"{name}_spot", 1.0, smat)
    _attach(s, w, (side * u, -0.024 - back, v))
    s.scale = (r, r, r)
    s["lid"] = 0.0
    s.id_properties_ui("lid").update(min=0.0, max=1.0)
    s["glow"] = 0.0
    s.id_properties_ui("glow").update(min=0.0, max=1.0)
    for i, (u, v, r) in enumerate(dots):
        d = _disc(f"{name}_dot{i}", r, dmat, 24)
        _attach(d, w, (side * u, -0.024 - back, v))
    return w, s


def _antenna(name, side, base, mat, tip, body):
    """A big soft feathery antenna: a shaft curling outward with a leaf-shaped feather blade and a comb of barbs along
    its edges (one smooth SDF shape), and a peach tip."""
    b = np.asarray(base, float)
    ctrl = [b, b + (side * 0.22, -0.14, 0.36), b + (side * 0.58, -0.16, 0.68), b + (side * 0.98, -0.08, 0.84),
            b + (side * 1.24, 0.02, 0.72)]
    # open Catmull-Rom through ctrl
    P = np.array([ctrl[0]] + ctrl + [ctrl[-1]])
    path = []
    for i in range(1, len(P) - 2):
        for u in np.linspace(0, 1, 6, endpoint=False):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            path.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                               + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
    path.append(P[-2])
    path = np.array(path)
    n = len(path)
    parts = []
    for i in range(n - 1):
        t = i / (n - 1)
        parts.append((sdf.C(path[i], path[i + 1], 0.045 - 0.02 * t, 0.045 - 0.02 * (i + 1) / (n - 1)), mat.name, 0.03))
    for j in range(15):
        s = 0.14 + j * 0.058
        i = min(int(s * (n - 1)), n - 2)
        p = path[i] + (path[i + 1] - path[i]) * (s * (n - 1) - i)
        t = path[i + 1] - path[i]
        t /= np.linalg.norm(t)
        nrm = np.array([-t[2], 0.0, t[0]])
        nrm /= np.linalg.norm(nrm)
        w = 0.035 + 0.13 * math.sin(math.pi * min(1.0, (s - 0.08) / 0.9)) ** 0.9   # leaf-shaped blade half-width
        parts.append((sdf.E(p, (w, 0.028, w)), mat.name, 0.03))
        for sgn in (-1, 1):
            d = sgn * nrm + 0.7 * t
            d /= np.linalg.norm(d)
            parts.append((sdf.C(p + sgn * nrm * w * 0.5, p + d * (w + 0.09), 0.022, 0.016), mat.name, 0.02))
    a = sdf.build(name, parts, k=0.03, res=0.012, pad=0.06, smooth_iter=3)
    look.outline(a, 0.01)
    piv = _empty(f"{name}_piv", tuple(b), body)
    _attach(a, piv, tuple(-b))
    _sphere(f"{name}_tip", tuple(path[-1] - b), (0.085, 0.07, 0.085), tip, piv, 0.01, 20)
    return piv


def build(loc=(0, 0, 0), name="moth"):
    hx = look.hexc
    white, cream = look.toon(f"{name}_white", hx(WHITE)), look.toon(f"{name}_cream", hx(CREAM))
    mint, peach = look.toon(f"{name}_mint", hx(MINT)), look.toon(f"{name}_peach", hx(PEACH))
    eye_m = look.toon(f"{name}_eye", hx(INK), gloss=True)
    hi_m = look.flat(f"{name}_hi", (1, 1, 1, 1))
    cres_m = look.flat(f"{name}_cres", hx(CRESCENT))
    blush_m = look.flat(f"{name}_blush", hx(BLUSH))
    fore_spot = _spot_mat(f"{name}_forespot", MINT, CORAL)
    hind_spot = _spot_mat(f"{name}_hindspot", PEACH, TEAL)
    E = sdf.E

    root = _empty(f"{name}_root", loc)
    hover = _empty(f"{name}_hover", (0, 0, HOVER), root)
    body = _empty(f"{name}_body", (0, 0, 0), hover)
    # body: a round fluffy ball (scalloped with fur bumps) and a soft abdomen behind
    rnd = random.Random(7)
    parts = [(E((0, 0, 0), (0.86, 0.8, 0.82)), white.name, None),
             (E((0, 0.52, -0.48), (0.46, 0.56, 0.54)), white.name, 0.2)]
    N = 40
    for i in range(N):
        yy = 1 - 2 * (i + 0.5) / N
        rr = math.sqrt(1 - yy * yy)
        th = i * math.pi * (3 - math.sqrt(5))
        d = np.array([math.cos(th) * rr, yy, math.sin(th) * rr])     # fibonacci sphere; y = front/back
        if d[1] < -0.3 and d[2] < 0.55:                              # keep the face smooth
            continue
        if d[2] < -0.6:                                              # and the underside
            continue
        s = rnd.uniform(0.17, 0.23)
        parts.append((E(d * (0.8, 0.75, 0.77), (s, s, s)), white.name, 0.07))
    bm = sdf.build(f"{name}_bodymesh", parts, k=0.1, res=0.03)
    look.outline(bm, 0.025)
    _attach(bm, body)
    # cream fur collar: a shawl of round fluff tufts around the back and sides of the neck, open in front (a band
    # across the face read as a beard), peeking out beside the cheeks and over the shoulders
    ring = []
    for i in range(24):
        a = i / 24 * 2 * math.pi
        sa, ca = math.sin(a), math.cos(a)
        if sa < -0.42:                                               # leave the front open
            continue
        r = 0.19 + 0.04 * (i % 2)
        ring.append((E((ca * 0.8, sa * 0.66 + 0.02, -0.1 + 0.2 * sa), (r, r, r * 0.85)), cream.name, 0.07))
    col = sdf.build(f"{name}_collar", ring, k=0.07, res=0.025, smooth_iter=6)
    look.outline(col, 0.016)
    _attach(col, body)
    for i, (x, y, z, s) in enumerate([(0, -0.08, 0.8, 0.2), (-0.17, 0.04, 0.78, 0.16), (0.17, 0.06, 0.79, 0.16)]):
        _sphere(f"{name}_tuft{i}", (x, y, z), (s, s, s * 0.85), white, body, 0.016, 20)
    # face: big glossy black eyes with two highlights, blush, a tiny mouth
    eyes = []
    for sx in (-1, 1):
        piv = _empty(f"{name}_eyepiv{sx}", (sx * 0.33, -0.7, 0.08), body)
        _sphere(f"{name}_eye{sx}", (0, 0, 0), (0.27, 0.13, 0.34), eye_m, piv, 0.02, 32)
        _sphere(f"{name}_cres{sx}", (0, -0.09, -0.19), (0.15, 0.05, 0.09), cres_m, piv, 0, 24)
        _sphere(f"{name}_hi{sx}", (0.09, -0.115, 0.13), (0.09, 0.03, 0.1), hi_m, piv, 0, 16)
        _sphere(f"{name}_hi2{sx}", (-0.08, -0.12, -0.12), (0.045, 0.02, 0.045), hi_m, piv, 0, 12)
        eyes.append(piv)
        _sphere(f"{name}_blush{sx}", (sx * 0.6, -0.56, -0.14), (0.14, 0.04, 0.08), blush_m, body, 0, 16)
    mo = _sphere(f"{name}_mouth", (0, -0.79, -0.17), (0.07, 0.03, 0.045), eye_m, body, 0, 16)
    mo.rotation_euler = (math.radians(12), 0, 0)
    # antennae
    antennae = [_antenna(f"{name}_ant{sx}", sx, (sx * 0.2, -0.36, 0.66), cream, peach, body) for sx in (-1, 1)]
    # wings: roots on the back of the body, behind the collar; hindwings sit just behind the forewings
    wings, spots = [None] * 4, [None] * 4
    for k, sx in enumerate((-1, 1)):
        wings[k], spots[k] = _wing(f"{name}_fore{sx}", sx, FORE, FORE_SPOT, FORE_DOTS, mint, fore_spot, peach, body,
                                   (sx * 0.48, 0.3, 0.16), FORE_UP, FORE_SWEEP, 0.0)
        wings[2 + k], spots[2 + k] = _wing(f"{name}_hind{sx}", sx, HIND, HIND_SPOT, HIND_DOTS, peach, hind_spot, mint,
                                           body, (sx * 0.46, 0.4, -0.12), HIND_UP, HIND_SWEEP, 0.0)
        _sphere(f"{name}_wingfluff{sx}", (sx * 0.6, 0.34, 0.02), (0.24, 0.22, 0.3), white, body, 0.016, 20)
    # the outline shells enclose the body and would shadow it (EEVEE shadows ignore backface culling): lines cast none
    for m in bpy.data.materials:
        if m.name.startswith(f"line_{name}_"):
            m.use_backface_culling_shadow = True
    bpy.context.view_layer.update()
    shadow = look.blob_shadow(f"{name}_shadow", (loc[0], loc[1] + 0.1, loc[2] + 0.03), (1.1, 0.8), root)
    return dict(root=root, hover=hover, body=body, wings=wings, spots=spots, eyes=eyes, antennae=antennae,
                shadow=shadow)


# --- posing and animation -------------------------------------------------------------------------------------------
WING_BEAT = [0.5, 0.15, -0.4, 0.15]   # flap offsets per frame of a 4-frame beat (radians, + = tips up), on 1s


def wing_pose(rig, frame, flap_fore, flap_hind=None, sweep=0.0):
    """Key all four wings at `frame`: flap adds to the resting tilt (+ = up), sweep adds to the resting sweep back."""
    flap_hind = flap_fore * 0.8 if flap_hind is None else flap_hind
    for i, w in enumerate(rig["wings"]):
        side = -1 if i % 2 == 0 else 1
        up, sw, fl = (FORE_UP, FORE_SWEEP, flap_fore) if i < 2 else (HIND_UP, HIND_SWEEP, flap_hind)
        anim.key(w, "rotation_euler", frame, (0.0, -side * (up + fl), side * (sw + sweep)), "LINEAR")


def spot_lid(rig, frame, value, spots=None, interp="BEZIER", prop="lid"):
    """Key the eye-spot lids at `frame` (0 = open, 1 = shut); prop="glow" keys the iris glow the same way."""
    for s in spots or rig["spots"]:
        s[prop] = value
        s.keyframe_insert(data_path=f'["{prop}"]', frame=frame)
        for fc in anim.all_fcurves(s.animation_data.action):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.01:
                    kp.interpolation = interp


def spot_blink(rig, f, close=10, hold=6, reopen=12, stagger=(0, 3, 2, 5)):
    """The creepy tell: every eye-spot slowly closes and opens, slightly out of step with the others."""
    for s, d in zip(rig["spots"], stagger):
        spot_lid(rig, f + d - 1, 0.0, [s])
        spot_lid(rig, f + d + close, 1.0, [s])
        spot_lid(rig, f + d + close + hold, 1.0, [s])
        spot_lid(rig, f + d + close + hold + reopen, 0.0, [s])


def idle(rig, f0, f1, bob=0.12, period=24, seed=2, step=2):
    """Hover between f0 and f1: fast wing beats on 1s; body bob, sway, antenna waves, blinks and the eye-spot blink
    held for `step` frames (anim.on_twos on everything but the wings; the hover is quick, so 2s by default)."""
    rnd = random.Random(seed)
    for f in range(f0, f1 + 1):
        ph = (f - f0) % 4
        wing_pose(rig, f, WING_BEAT[ph], WING_BEAT[(ph - 1) % 4] * 0.8, 0.12 * (ph == 2))
    hov, body = rig["hover"], rig["body"]
    f = f0
    while f <= f1 + period:
        anim.key(hov, "location", f, (0, 0, HOVER + bob))
        anim.key(hov, "location", f + period // 2, (0, 0, HOVER - bob))
        anim.squash(body, f, 0.025)
        anim.squash(body, f + period // 2, -0.03)
        anim.key(body, "rotation_euler", f, (0.04, -0.05, 0.0))
        anim.key(body, "rotation_euler", f + period // 2, (-0.03, 0.05, 0.0))
        anim.key(rig["shadow"], "scale", f, (0.9, 0.9, 1))
        anim.key(rig["shadow"], "scale", f + period // 2, (1.05, 1.05, 1))
        f += period
    for i, a in enumerate(rig["antennae"]):
        s = -1 if i == 0 else 1
        f = f0 + i * 4
        while f <= f1 + period:
            anim.key(a, "rotation_euler", f, (0.14, s * 0.1, -s * 0.12))
            anim.key(a, "rotation_euler", f + 10, (-0.1, -s * 0.06, s * 0.1))
            f += 20
    f = f0 + rnd.randint(12, 30)
    while f < f1 - 4:
        anim.blink(rig, f)
        f += rnd.randint(40, 70)
    spot_lid(rig, f0, 0.0)
    f = f0 + rnd.randint(24, 40)
    while f < f1 - 34:
        spot_blink(rig, f)
        f += rnd.randint(80, 110)
    anim.on_twos([hov, body, rig["shadow"], *rig["antennae"], *rig["eyes"], *rig["spots"]], step)


def cute_pose(rig, f, interp="CONSTANT"):
    """The held "delight" pose (usable as a freeze frame): head tilted, a little stretched, antennae perked forward."""
    anim.key(rig["body"], "rotation_euler", f, (0.08, 0.22, 0.0), interp)
    anim.squash(rig["body"], f, 0.04, interp)
    for i, a in enumerate(rig["antennae"]):
        s = -1 if i == 0 else 1
        anim.key(a, "rotation_euler", f, (-0.18, s * 0.08, -s * 0.2), interp)


def s14c(rig, f0, frames=22, step=2):
    """Shot S14c (~0.9 s, close, locked camera): the fluffmoth holds its cute pose while its wings keep beating (on
    1s), and on the shot's last beat the wing eye-spots blink shut and are just opening again at the cut."""
    f1 = f0 + frames - 1
    hov = rig["hover"]
    anim.key(hov, "location", f0, (0, 0, HOVER), "CONSTANT")
    cute_pose(rig, f0)
    for f in range(f0, f1 + 1):
        ph = (f - f0) % 4
        wing_pose(rig, f, 0.6 * WING_BEAT[ph] + 0.1, 0.6 * WING_BEAT[(ph - 1) % 4] * 0.8, 0.0)
    anim.key(hov, "location", f0 + frames // 2, (0, 0, HOVER + 0.04), "CONSTANT")
    spot_lid(rig, f0, 0.0)
    for s, d in zip(rig["spots"], (0, 1, 1, 2)):
        spot_lid(rig, f1 - 10 + d, 0.0, [s])
        spot_lid(rig, f1 - 5 + d, 1.0, [s])
        spot_lid(rig, f1 - 3 + d, 1.0, [s])
        spot_lid(rig, f1 + 4 + d, 0.0, [s])
    anim.on_twos([hov, rig["body"], *rig["antennae"], *rig["spots"]], step)
    return f1
