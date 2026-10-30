"""The jelly-snail (Episode 1's meadow creature, our own design): a small, low snail with a soft lilac jelly body (a
lighter rim fakes the see-through look), two eye stalks with big glossy eyes, a blushing
smile, and a round glass-marble shell with a glowing pastel spiral inside. Its tell: wherever it has crawled, the slime
trail behind it has burned little smoking holes through the grass.

    rig = build(loc)        ->  dict(root, body, bodymesh, shell, stalks, eyes, mouths, trail)
    root      : moves/turns the whole creature (foot at z=0, facing -Y)
    body      : squash & stretch pivot at the ground
    bodymesh  : the jelly body; its "wave" modifier makes the ripple that runs along the foot
    shell     : the shell's pivot where it sits on the back (small rotations for a wobble)
    stalks    : eye-stalk pivots at the head (rotate X/Z to bob)
    eyes      : eye pivots at the stalk tips (scale z to blink)
    mouths    : dict(smile, o): swappable mouth shapes (see mouth())
    trail     : dict(root, holes, wisps): the burned slime trail; it stays on the ground (not parented to root)

    idle(rig, f0, f1)            the foot wave, stalk bob and blinks on 3s, the trail smoking on 1s
    pose(rig, f, kind)           a held pose keyed at f: "cute" (head tilt, stalks leaning), "delight", "shock"
    hold(rig, f0, f1, kind)      one held pose with a small bob on 3s (short close shots such as S14a)
    mouth(rig, f, shape)         switch the mouth to "smile" or "o" at f
"""
import math
import random

import bpy
import numpy as np

from . import anim, look, sdf
from .puffshrimp import _empty, _parent, _sphere
from .puffshrimp import _tube as _puff_tube

LILAC, RIM, INK, BLUSH, CRESCENT = "#c9a9f5", "#f3eaff", "#1b1830", "#ff9fc4", "#8f6bff"
GLASS, SWIRL = "#dfe8ff", ("#ffe36e", "#ff8fcf", "#b98cff", "#5fe0c0")
SLIME, CHAR, HOLE, EMBER, SMOKE = "#efe4ff", "#4b3326", "#191216", "#ff7b3a", "#5d5562"


def jelly(name, base, rim=RIM, threshold=0.45):
    """The anime cel (flat base + one hard cool shadow) with a hard lighter band at the silhouette, so the body reads as
    soft, slightly see-through jelly while staying a flat TV-anime colour."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, (*look.SHADOW_TINT, 1)
    cr.elements[1].position, cr.elements[1].color = threshold, (1, 1, 1, 1)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs[7].default_value = base
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    rr = nt.nodes.new("ShaderNodeValToRGB")
    rr.color_ramp.interpolation = "CONSTANT"
    rr.color_ramp.elements[0].position, rr.color_ramp.elements[0].color = 0.0, (0, 0, 0, 1)
    rr.color_ramp.elements[1].position, rr.color_ramp.elements[1].color = 0.62, (0.85, 0.85, 0.85, 1)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs[7].default_value = look.hexc(rim)
    em = nt.nodes.new("ShaderNodeEmission")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], mul.inputs[6])
    L(lw.outputs["Facing"], rr.inputs[0])
    L(rr.outputs[0], mix.inputs["Factor"])
    L(mul.outputs[2], mix.inputs[6])
    L(mix.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def glass(name, tint=GLASS, rim="#ffffff"):
    """See-through marble glass: mostly clear in the middle, a pale opaque rim, and a dark line at the very edge (an
    inverted-hull outline would show through the glass, so the outline is drawn by the material itself, in the glass's
    own darker line colour like look.outline()'s)."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.5
    col = nt.nodes.new("ShaderNodeValToRGB")
    cr = col.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, look.hexc(tint)
    cr.elements[1].position, cr.elements[1].color = 0.5, look.hexc(rim)
    cr.elements.new(0.67).color = look.line_color(look.hexc(tint))
    alpha = nt.nodes.new("ShaderNodeValToRGB")
    ar = alpha.color_ramp
    ar.interpolation = "CONSTANT"
    ar.elements[0].position, ar.elements[0].color = 0.0, (0.22, 0.22, 0.22, 1)
    ar.elements[1].position, ar.elements[1].color = 0.5, (0.75, 0.75, 0.75, 1)
    ar.elements.new(0.67).color = (1, 1, 1, 1)
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(lw.outputs["Facing"], col.inputs[0])
    L(lw.outputs["Facing"], alpha.inputs[0])
    L(col.outputs[0], em.inputs[0])
    L(alpha.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = True
    return m


def _tube(name, pts, radius, mat, line=0.012):
    """puffshrimp's tube, but with nothing else selected: its curve-to-mesh conversion would also apply the modifiers of
    any selected mesh (it ate the body's wave and outline)."""
    bpy.ops.object.select_all(action="DESELECT")
    return _puff_tube(name, pts, radius, mat, line)


def _pivot(name, world, parent):
    """An empty at a WORLD position, parented without moving (puffshrimp's _empty(name, loc, parent) puts it at
    parent + loc, which double-counts a pivot given in world space)."""
    e = _empty(name, world)
    bpy.context.view_layer.update()
    _parent(e, parent)
    return e


def _front(body, x, z):
    """The point on the body's front surface (local space) seen straight from -Y at (x, z)."""
    hit, p, _, _ = body.ray_cast((x, -5.0, z), (0.0, 1.0, 0.0))
    return (p.x, p.y, p.z) if hit else (x, -1.1, z)


def _disc(name, center, radius, mat, z, rnd, n=16, rough=0.25):
    """A flat irregular disc lying on the ground (burn marks)."""
    verts = []
    for i in range(n):
        a = i / n * 2 * math.pi
        r = radius * (1 + rnd.uniform(-rough, rough))
        verts.append((center[0] + math.cos(a) * r, center[1] + math.sin(a) * r, z))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], [list(range(n))])
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def burn_trail(loc=(0, 0, 0), name="jsnail", length=4.2, n=6, seed=7):
    """The tell: a glossy slime ribbon behind the snail (+Y) with little burned holes eaten through the grass, each with
    a charred ring, a glowing ember edge and smoke wisps (animated by idle()). Returns dict(root, holes, wisps, path);
    holes are (x, y, r) in world space so a set can leave the grass out around them."""
    rnd = random.Random(seed)
    wr = random.Random(seed + 1)                               # the smoke's own stream, so the holes stay put
    hx = look.hexc
    slime = look.fade(f"{name}_slime", hx(SLIME), 0.5)
    char_m = look.flat(f"{name}_char", hx(CHAR))
    hole_m = look.flat(f"{name}_hole", hx(HOLE))
    ember_m = look.flat(f"{name}_ember", hx(EMBER), 1.3)
    singed = look.paint(f"{name}_singed", hx("#5a4632"))
    root = _empty(f"{name}_trail", loc)
    y0 = loc[1] + 1.55

    def path(t):
        return loc[0] + 0.28 * math.sin(2 * math.pi * 0.8 * t + 0.3) * t, y0 + length * t

    samples = 40
    verts, faces, pts = [], [], []
    for i in range(samples + 1):
        t = i / samples
        x, y = path(t)
        pts.append((x, y))
        half = 0.4 * (1 - 0.35 * t)
        verts += [(x - half, y, loc[2] + 0.008), (x + half, y, loc[2] + 0.008)]
        if i:
            a = 2 * (i - 1)
            faces.append([a, a + 1, a + 3, a + 2])
    me = bpy.data.meshes.new(f"{name}_slime")
    me.from_pydata(verts, [], faces)
    me.materials.append(slime)
    rib = bpy.data.objects.new(f"{name}_slime", me)
    bpy.context.scene.collection.objects.link(rib)
    _parent(rib, root)

    holes, wisps = [], []
    for k in range(n):
        t = 0.14 + k / max(1, n - 1) * 0.8 + rnd.uniform(-0.04, 0.04)
        x, y = path(t)
        x += rnd.uniform(-0.14, 0.14)
        r = rnd.uniform(0.15, 0.25) * (1.15 - 0.3 * t)
        z = loc[2]
        for o in (_disc(f"{name}_char{k}", (x, y), r * 1.6, char_m, z + 0.012, rnd),
                  _disc(f"{name}_ember{k}", (x, y), r * 1.15, ember_m, z + 0.014, rnd, rough=0.18),
                  _disc(f"{name}_hole{k}", (x, y), r, hole_m, z + 0.016, rnd, rough=0.15)):
            _parent(o, root)
        for j in range(3):                                     # singed grass stubs at the rim
            a = rnd.uniform(0, 2 * math.pi)
            bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.035, depth=0.12,
                                            location=(x + math.cos(a) * r * 1.9, y + math.sin(a) * r * 1.9, z + 0.05),
                                            rotation=(rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), 0))
            st = bpy.context.object
            st.name = f"{name}_stub{k}_{j}"
            st.data.materials.append(singed)
            _parent(st, root)
        for j in range(3):                                     # a thin column: puffs a third of a cycle apart
            w = _sphere(f"{name}_wisp{k}_{j}", (x, y, z + 0.05), (1, 1, 1),
                        look.fade(f"{name}_wisp_m{k}_{j}", hx(SMOKE), 0.0), 0, 12)
            w.visible_shadow = False                           # smoke casts no shadow on the grass
            _parent(w, root)
            wisps.append(dict(obj=w, base=(x, y, z), r=r, phase=(j * 13 + wr.randint(0, 39)) % 40,
                              drift=wr.uniform(-0.15, 0.15)))
        holes.append((x, y, r))
    return dict(root=root, holes=holes, wisps=wisps, path=pts)


def build(loc=(0, 0, 0), name="jsnail", trail=True):
    hx = look.hexc
    lilac = jelly(f"{name}_lilac", hx(LILAC))
    eye_m = look.toon(f"{name}_eye", hx(INK), shade=0.8, gloss=True)
    hi_m = look.flat(f"{name}_hi", (1, 1, 1, 1))
    blush_m = look.flat(f"{name}_blush", hx(BLUSH))
    sheen_m = look.flat(f"{name}_sheen", hx(RIM))
    iris_m = look.flat(f"{name}_iris", hx(CRESCENT))          # the lighter colour low in the eye (anime eyes)
    E = sdf.E

    def W(x, y, z):
        return (loc[0] + x, loc[1] + y, loc[2] + z)

    root = _empty(f"{name}_root", loc)
    body_pivot = _empty(f"{name}_body", (0, 0, 0), root)
    bpy.context.view_layer.update()
    # body: a long low foot that rises into a round head at the front and tapers to a tail
    body = sdf.build(f"{name}_bodymesh", [
        (E((0, 0.15, 0.2), (0.6, 1.3, 0.22)), lilac.name, None),
        (E((0, -0.72, 0.62), (0.5, 0.45, 0.6)), lilac.name, 0.22),
        (E((0, 1.35, 0.14), (0.32, 0.5, 0.14)), lilac.name, 0.18),
    ], k=0.12, res=0.03, smooth_iter=16)
    mouth_pts = [_front(body, x, z) for x, z in ((-0.13, 0.66), (-0.065, 0.6), (0, 0.635), (0.065, 0.6), (0.13, 0.66))]
    mouth_c = _front(body, 0, 0.6)
    cheeks = [_front(body, sx * 0.3, 0.74) for sx in (-1, 1)]
    sheen = _front(body, -0.22, 1.0)
    # the ripple that runs forward along the foot: straight up (the marching-cubes normals are too noisy to push along),
    # weighted off at the sole so it stays on the ground and toward the head so the face stays still
    zs = np.array([v.co.z for v in body.data.vertices])
    vg = body.vertex_groups.new(name="foot")
    for i, w in enumerate(np.clip(zs / 0.12, 0.0, 1.0) * np.clip((0.8 - zs) / 0.35, 0.0, 1.0)):
        if w > 0:
            vg.add([i], float(w), "REPLACE")
    wave = body.modifiers.new("wave", "WAVE")
    wave.use_x, wave.use_y, wave.use_cyclic, wave.use_normal = False, True, True, False
    wave.speed, wave.width, wave.narrowness, wave.height = 0.0, 0.3, 2.5, 0.07
    wave.start_position_y = 6.0
    wave.vertex_group = "foot"
    look.outline(body, 0.025)
    body.location = W(*body.location)
    _parent(body, body_pivot)
    # face: a small cat-like "w" smile (a plain curve read as a closed eye from the side, since the real eyes are up
    # on the stalks) or a surprised "o", blush, and a jelly sheen on the head
    smile = _tube(f"{name}_mouth", [W(x, y - 0.012, z) for x, y, z in mouth_pts], 0.018, eye_m, 0)
    mouth_o = _sphere(f"{name}_mouth_o", W(mouth_c[0], mouth_c[1] - 0.01, mouth_c[2] + 0.03), (0.05, 0.025, 0.06),
                      eye_m, 0, 16)
    mouth_o.hide_render = mouth_o.hide_viewport = True
    for o in (smile, mouth_o):
        _parent(o, body_pivot)
    for sx, c in zip((-1, 1), cheeks):
        b = _sphere(f"{name}_blush{sx}", W(c[0], c[1] - 0.01, c[2]), (0.09, 0.03, 0.05), blush_m, 0, 16)
        _parent(b, body_pivot)
    s = _sphere(f"{name}_sheen", W(sheen[0], sheen[1] - 0.01, sheen[2]), (0.075, 0.02, 0.028), sheen_m, 0, 16)
    s.rotation_euler = (0, 0.6, 0)
    _parent(s, body_pivot)
    # eye stalks: pivots at the head, a jelly bulb at each tip carrying a big glossy eye
    stalks, eyes = [], []
    for sx in (-1, 1):
        base, mid, tip = W(sx * 0.16, -0.8, 1.1), W(sx * 0.24, -0.9, 1.5), W(sx * 0.36, -0.98, 1.82)
        piv = _pivot(f"{name}_stalkpiv{sx}", base, body_pivot)
        st = _tube(f"{name}_stalk{sx}", [base, mid, tip], 0.05, lilac)
        bulb = _sphere(f"{name}_bulb{sx}", tip, (0.17, 0.16, 0.17), lilac, 0.02, 24)
        for o in (st, bulb):
            _parent(o, piv)
        ec = (tip[0], tip[1] - 0.12, tip[2])
        epiv = _pivot(f"{name}_eyepiv{sx}", ec, piv)
        e = _sphere(f"{name}_eye{sx}", ec, (0.12, 0.06, 0.15), eye_m, 0.014, 24)
        h1 = _sphere(f"{name}_hi{sx}", (ec[0] + 0.045, ec[1] - 0.05, ec[2] + 0.06), (0.04, 0.02, 0.045), hi_m, 0, 12)
        cres = _sphere(f"{name}_iris{sx}", (ec[0], ec[1] - 0.042, ec[2] - 0.072), (0.085, 0.025, 0.05), iris_m, 0, 20)
        h2 = _sphere(f"{name}_hi2{sx}", (ec[0] - 0.04, ec[1] - 0.06, ec[2] - 0.035), (0.02, 0.01, 0.02), hi_m, 0, 10)
        for o in (e, cres, h1, h2):
            _parent(o, epiv)
        stalks.append(piv)
        eyes.append(epiv)
    # the shell: a glass marble with a glowing pastel spiral inside, sitting in the back
    c = (0.0, 0.32, 0.95)
    shell = _pivot(f"{name}_shell", W(0, 0.32, 0.4), body_pivot)
    gl = _sphere(f"{name}_glass", W(*c), (0.62, 0.62, 0.62), glass(f"{name}_glass"), 0, 48)
    _parent(gl, shell)
    turns, segs = 2.3, len(SWIRL) - 1
    pts = []
    for i in range(61):
        t = i / 60
        th = t * turns * 2 * math.pi + 0.6
        r = 0.04 + 0.42 * t
        pts.append(W(c[0], c[1] + math.cos(th) * r, c[2] + math.sin(th) * r))
    for k in range(segs):
        seg = pts[k * 60 // segs:(k + 1) * 60 // segs + 1]
        sw = _tube(f"{name}_swirl{k}", seg, 0.04 + 0.01 * k, look.flat(f"{name}_swirl_m{k}", hx(SWIRL[k + 1]), 1.6), 0)
        sw.scale = (1.6, 1, 1)                                 # a flat band, so it reads from the front too
        sw.location.x = -0.6 * W(*c)[0]                        # keep it centred after the x-scale about the origin
        _parent(sw, shell)
    core = _sphere(f"{name}_core", W(*c), (0.08, 0.08, 0.08), look.flat(f"{name}_core_m", hx(SWIRL[0]), 1.8), 0, 16)
    _parent(core, shell)
    for nm, d, rr in ((f"{name}_ghi", (-0.5, -0.5, 0.71), 0.085), (f"{name}_ghi2", (-0.3, -0.7, 0.42), 0.04)):
        d = np.array(d) / np.linalg.norm(d)
        g = _sphere(nm, W(*(np.array(c) + d * 0.6)), (rr, rr, rr), hi_m, 0, 12)
        _parent(g, shell)
    look.blob_shadow(f"{name}_shadow", W(0, 0.15, 0.03), (0.8, 1.55), root)
    tr = burn_trail(loc, name) if trail else None
    return dict(root=root, body=body_pivot, bodymesh=body, shell=shell, stalks=stalks, eyes=eyes,
                mouths=dict(smile=smile, o=mouth_o), trail=tr)


def _linear(o, path, frames, values):
    """Linear keys on any property path (e.g. a modifier setting)."""
    owner, prop = path.rsplit(".", 1)
    for f, v in zip(frames, values):
        setattr(o.path_resolve(owner), prop, v)
        o.keyframe_insert(data_path=path, frame=f)
    for fc in anim.all_fcurves(o.animation_data.action):
        if fc.data_path == path:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def _cycle(idblock):
    for fc in anim.all_fcurves(idblock.animation_data.action):
        if not any(m.type == "CYCLES" for m in fc.modifiers):
            fc.modifiers.new("CYCLES")


def smoke(trail, f0, period=40):
    """Each wisp rises from its hole, swells, drifts and fades, over and over (VFX: on 1s). Already-smoking wisps are
    left alone, so idle() and hold() can share one rig."""
    for w in trail["wisps"]:
        o, (x, y, z), r = w["obj"], w["base"], w["r"]
        if o.animation_data:
            continue
        mix = o.data.materials[0].node_tree.nodes["Mix"]
        s = f0 - w["phase"]
        for df, dz, sc, a, dx in ((0, 0.04, 0.3, 0.0, 0.0), (8, 0.2, 0.55, 0.5, 0.2), (24, 0.6, 0.85, 0.3, 0.6),
                                  (period, 1.0, 1.1, 0.0, 1.0)):
            anim.key(o, "location", s + df, (x + w["drift"] * dx, y + 0.05 * dx, z + dz), "LINEAR")
            anim.key(o, "scale", s + df, (r * sc, r * sc, r * sc * 1.4), "LINEAR")
            mix.inputs[0].default_value = a
            mix.inputs[0].keyframe_insert("default_value", frame=s + df)
        _cycle(o)
        _cycle(o.data.materials[0].node_tree)


def idle(rig, f0, f1, period=48, seed=2):
    """The foot ripple running forward, a slow breath and shell wobble, eye stalks bobbing out of step, and blinks,
    all on 3s (anim.on_twos's default step); the trail keeps smoking on 1s."""
    rnd = random.Random(seed)
    wl = 2 * rig["bodymesh"].modifiers["wave"].width
    _linear(rig["bodymesh"], 'modifiers["wave"].start_position_y', (f0, f1),
            (6.0, 6.0 - wl * (f1 - f0) / period))
    f = f0
    while f <= f1:
        anim.squash(rig["body"], f, 0.015)
        anim.squash(rig["body"], f + period // 2, -0.015)
        anim.key(rig["shell"], "rotation_euler", f + 6, (0.035, 0.0, 0.02))
        anim.key(rig["shell"], "rotation_euler", f + 6 + period // 2, (-0.03, 0.0, -0.015))
        f += period
    half = 16
    for i, s in enumerate(rig["stalks"]):
        sx = (-1) ** i
        f = f0 + i * 7
        while f <= f1:
            anim.key(s, "rotation_euler", f, (0.12, 0.0, sx * 0.07))
            anim.key(s, "rotation_euler", f + half, (-0.07, 0.0, -sx * 0.04))
            f += 2 * half
    f = f0 + rnd.randint(14, 30)
    while f < f1 - 4:
        anim.blink(rig, f)
        f += rnd.randint(40, 70)
    anim.on_twos([rig["body"], rig["bodymesh"], rig["shell"], *rig["stalks"], *rig["eyes"]])
    if rig.get("trail"):
        smoke(rig["trail"], f0)


# held poses: stalk (rotation x, rotation z, spread outward? else both lean the same way), eye scale, body squash
# (+ stretches up), body roll (a head tilt), mouth
POSES = dict(
    cute=dict(stalk=(0.06, 0.2, False), eye=1.0, body=0.0, roll=0.08, mouth="smile"),
    delight=dict(stalk=(-0.12, 0.3, True), eye=1.12, body=0.06, roll=0.0, mouth="smile"),
    shock=dict(stalk=(-0.32, 0.12, True), eye=1.25, body=0.1, roll=0.0, mouth="o"),
)


def mouth(rig, f, shape="smile"):
    """Show one mouth shape from frame f on (constant keys)."""
    for nm, o in rig["mouths"].items():
        o.hide_render = o.hide_viewport = nm != shape
        o.keyframe_insert("hide_render", frame=f)
        o.keyframe_insert("hide_viewport", frame=f)


def pose(rig, f, kind="cute"):
    """Key a held pose at frame f (usable as a freeze frame for a reaction beat). Returns the pose's values."""
    p = POSES[kind]
    rx, rz, spread = p["stalk"]
    for sx, s in zip((-1, 1), rig["stalks"]):
        anim.key(s, "rotation_euler", f, (rx, 0.0, sx * rz if spread else rz))
    for e in rig["eyes"]:
        anim.key(e, "scale", f, p["eye"])
    anim.squash(rig["body"], f, p["body"])
    anim.key(rig["body"], "rotation_euler", f, (0.0, p["roll"], 0.0))
    mouth(rig, f, p["mouth"])
    return p


def hold(rig, f0, f1, kind="cute", bob=0.02, period=12):
    """One held pose from f0 to f1 with only a small breathing bob and stalk sway on 3s (short close shots, e.g. S14a:
    about 0.9 s); the trail keeps smoking on 1s."""
    p = pose(rig, f0, kind)
    rx, rz, spread = p["stalk"]
    f, up = f0 + period // 2, True
    while f <= f1 + period // 2:
        anim.squash(rig["body"], f, p["body"] + (bob if up else -bob))
        for sx, s in zip((-1, 1), rig["stalks"]):
            d = 0.05 if up else -0.03
            anim.key(s, "rotation_euler", f, (rx + d, 0.0, (sx * rz if spread else rz) + sx * d * 0.5))
        f, up = f + period // 2, not up
    anim.on_twos([rig["body"], rig["shell"], *rig["stalks"], *rig["eyes"]])
    if rig.get("trail"):
        smoke(rig["trail"], f0)
