"""The new world of Episode 1, painted like a Pokémon-anime background (mk/paintbg.py: three-band painted materials, no
outlines): soft rolling hills of brush-stroke grass, cauliflower trees in natural greens, giant candy-coloured mushrooms
as accents (some as big as houses), a sparkling pond, flower meadows, distant blue mountains, big cumulus clouds and a
cloud deck the camera falls through.

    paintbg.sky(); look.sun()
    h = world.build(seed=7)            # handles: clearing / puddle empties, ground(x, y), sparkles, cloud deck, ...
    cam = world.fall_camera(1, 108)    # 4.5 s: above the clouds -> through the deck -> eye level in the clearing
    world.twinkle(h, 1, 108)           # the pond sparkles pop on and off
    cam = world.pov_camera()           # S13: Kai's locked POV of the meadow (the fall's last frame)

Episode 1 plays the fall as two shots, world.S11 and world.S12 (sub-ranges of the same path), then S13 on pov_camera:
    world.fall_camera(f0, f0 + 22, *world.S11); world.fall_camera(f1, f1 + 51, *world.S12)

Units are metres. The clearing is at the origin at ground level 0; the puddle where a creature will drink is
h["puddle"] (left empty). The layout the camera depends on (clearing, puddle, pond, giant mushrooms, cloud deck) is
fixed; the seed only scatters trees, flowers, small mushrooms, hills and clouds. Every material fades toward the
pale-blue sky colour with camera distance, so far things read paler and bluer from any camera (the per-object `far=`
of paintbg, done in the shader so it stays right while the camera falls 185 m)."""
import math
import random

import bpy
import numpy as np
from mathutils import Quaternion, Vector

from . import look, paintbg

PUDDLE = (1.0, 2.5)                # the creature's puddle, in the clearing
# Kai's POV in S13 (and the last frame of the fall): sitting up in the grass, looking out over the meadow and up at the
# sky; the giant mushrooms frame the edges so the upper middle stays calm for the HUD
POV = ((-2.0, -6.0, 0.95), (-2.0, 14.0, 4.66))     # looking up 10.5 deg: horizon near y 800
PUDDLE_R, PUDDLE_Z = 0.78, -0.035
POND, POND_R, POND_Z = (7.5, 12.0), (8.0, 5.5), -0.12
DECK_C, DECK_Z, DECK_R = (-30.0, -108.0), (108.0, 132.0), 280.0     # cloud deck the camera falls through
HAZE_RGB, HAZE_DIST, HAZE_MAX = "#bfe3ff", 1100.0, 0.85            # paintbg's far colour
# fall_camera keys: (fraction of the shot, camera position, look-at target, roll in degrees)
FALL = [(0.00, (-40.0, -150.0, 185.0), (-10.0, 300.0, 70.0), 0.0),
        (0.30, (-33.0, -118.0, 135.0), (-15.0, 200.0, 30.0), 4.0),
        (0.50, (-27.0, -98.0, 105.0), (-10.0, 150.0, 10.0), -3.0),
        (0.72, (-16.0, -60.0, 55.0), (0.0, 5.0, 0.0), 2.0),
        (1.00, POV[0], POV[1], 0.0)]
# Episode 1 (EP01_SHOTS.md): the shots are sub-ranges of that one path, (start, end) as fractions of it
S11 = (0.38, 0.56)                 # 0.92 s: inside the deck, white opening onto the sky, falling out of the cloud
S12 = (0.66, 1.00)                 # 2.14 s: slow descent over the world, settling into S13's POV



def _ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _make_ground(rnd):
    """Height field: round gaussian hills (bigger farther out) and a gentle swell, flattened around the clearing, with
    a shallow basin for the pond and a dip for the puddle."""
    bumps = [(-40, 120, 45, 22), (60, 150, 55, 28), (10, 260, 80, 45), (-150, 330, 110, 60), (-70, 60, 35, 9),
             (55, 40, 30, 7)]
    for _ in range(56):
        d = 60 + 900 * rnd.random() ** 1.3
        a = rnd.uniform(0, 2 * math.pi)
        bumps.append((d * math.cos(a), d * math.sin(a), (18 + 0.16 * d) * rnd.uniform(0.6, 1.4),
                      (2 + 0.05 * d) * rnd.uniform(0.5, 1.3)))
    B = np.array(bumps, float)
    ph = [rnd.uniform(0, 2 * math.pi) for _ in range(4)]

    def ground(x, y):
        x, y = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float))
        h = np.zeros(x.shape)
        for cx, cy, r, a in B:
            h += a * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (r * r))
        h += 1.6 * np.sin(x / 41 + ph[0]) * np.sin(y / 37 + ph[1]) + 0.8 * np.sin(x / 17 + ph[2]) * np.cos(y / 23 + ph[3])
        h *= _ss(18.0, 60.0, np.hypot(x, y))
        e = ((x - POND[0]) / POND_R[0]) ** 2 + ((y - POND[1]) / POND_R[1]) ** 2
        dp = np.hypot(x - PUDDLE[0], y - PUDDLE[1])
        h += 0.12 * np.sin(x / 3.3 + ph[0]) * np.sin(y / 2.9 + ph[1]) * _ss(2.0, 4.0, dp) * _ss(1.0, 1.6, e)
        h -= 0.75 * (1 - _ss(0.55, 1.12, e))
        h -= 0.1 * (1 - _ss(0.6, 1.15, dp / PUDDLE_R))
        return h if h.ndim else float(h)
    return ground


def _hazed(m):
    """Fade a material that ends in an Emission toward the sky colour with camera distance (aerial perspective)."""
    nt = m.node_tree
    if "haze" in nt.nodes:
        return m
    em = next(n for n in nt.nodes if n.type == "EMISSION")
    src = em.inputs[0].links[0].from_socket
    L = nt.links.new
    cam = nt.nodes.new("ShaderNodeCameraData")
    k = nt.nodes.new("ShaderNodeMath")
    k.operation, k.inputs[1].default_value = "MULTIPLY", -1.0 / HAZE_DIST
    ex = nt.nodes.new("ShaderNodeMath")
    ex.operation = "EXPONENT"
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation, inv.inputs[0].default_value = "SUBTRACT", 1.0
    amt = nt.nodes.new("ShaderNodeMath")
    amt.operation, amt.inputs[1].default_value = "MULTIPLY", HAZE_MAX
    mix = nt.nodes.new("ShaderNodeMix")
    mix.name = "haze"
    mix.data_type, mix.blend_type = "RGBA", "MIX"
    mix.inputs[7].default_value = look.hexc(HAZE_RGB)
    L(cam.outputs["View Distance"], k.inputs[0])
    L(k.outputs[0], ex.inputs[0])
    L(ex.outputs[0], inv.inputs[1])
    L(inv.outputs[0], amt.inputs[0])
    L(amt.outputs[0], mix.inputs["Factor"])
    L(src, mix.inputs[6])
    L(mix.outputs[2], em.inputs[0])
    return m


def _p3(name, dark, mid, light, cuts=(0.32, 0.68), noise=0.18, scale=3.0):
    """paintbg.paint3 (three painted bands) under a world-only name, with the distance haze."""
    hx = look.hexc
    return _hazed(paintbg.paint3("w_" + name, hx(dark), hx(mid), hx(light), cuts, noise, scale))


def grass(name="w_grass", cols=("#2c8f36", "#46c046", "#7fdc58")):
    """The ground: paintbg's brush strokes stretched sideways, in its three greens (or `cols`), but driven by the light
    as well, so the rolling hills keep their shape; big soft patches break up the meadows."""
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
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.35, 3.0, 1.0)
    strokes = nt.nodes.new("ShaderNodeTexNoise")
    strokes.inputs["Scale"].default_value = 4.0
    strokes.inputs["Detail"].default_value = 6.0
    strokes.inputs["Roughness"].default_value = 0.65
    patch = nt.nodes.new("ShaderNodeTexNoise")
    patch.inputs["Scale"].default_value = 0.025
    patch.inputs["Detail"].default_value = 2.0
    s1 = nt.nodes.new("ShaderNodeMath")
    s1.operation, s1.inputs[1].default_value = "SUBTRACT", 0.5
    s2 = nt.nodes.new("ShaderNodeMath")
    s2.operation, s2.inputs[1].default_value = "SUBTRACT", 0.5
    a1 = nt.nodes.new("ShaderNodeMath")
    a1.operation, a1.inputs[1].default_value = "MULTIPLY_ADD", 0.45
    a2 = nt.nodes.new("ShaderNodeMath")
    a2.operation, a2.inputs[1].default_value = "MULTIPLY_ADD", 0.5
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, look.hexc(cols[0])
    cr.elements[1].position, cr.elements[1].color = 0.38, look.hexc(cols[1])
    e3 = cr.elements.new(0.66)
    e3.color = look.hexc(cols[2])
    em = nt.nodes.new("ShaderNodeEmission")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], bw.inputs[0])
    L(tc.outputs["Object"], mp.inputs[0])
    L(mp.outputs[0], strokes.inputs[0])
    L(tc.outputs["Object"], patch.inputs[0])
    L(strokes.outputs["Fac"], s1.inputs[0])
    L(patch.outputs["Fac"], s2.inputs[0])
    L(s1.outputs[0], a1.inputs[0])                             # light + (strokes - 0.5) * 0.45
    L(bw.outputs[0], a1.inputs[2])
    L(s2.outputs[0], a2.inputs[0])                             # ... + (patches - 0.5) * 0.5
    L(a1.outputs[0], a2.inputs[2])
    L(a2.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return _hazed(m)


def _water(name="w_water"):
    """Anime water: deep blue facing the camera, pale sky colour at grazing angles, lighter ripple streaks."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "EASE"
    cr.elements[0].position, cr.elements[0].color = 0.1, look.hexc("#2b8ad6")
    cr.elements[1].position, cr.elements[1].color = 0.9, look.hexc("#a6e0ff")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.35, 1.6, 1.0)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.4
    nz.inputs["Detail"].default_value = 2.0
    band = nt.nodes.new("ShaderNodeValToRGB")
    band.color_ramp.interpolation = "CONSTANT"
    band.color_ramp.elements[1].position = 0.63
    rip = nt.nodes.new("ShaderNodeMix")
    rip.data_type, rip.blend_type = "RGBA", "MIX"
    rip.inputs[7].default_value = look.hexc("#dff5ff")
    fac = nt.nodes.new("ShaderNodeMath")
    fac.operation, fac.inputs[1].default_value = "MULTIPLY", 0.7
    em = nt.nodes.new("ShaderNodeEmission")
    L(lw.outputs["Facing"], ramp.inputs[0])
    L(tc.outputs["Object"], mp.inputs[0])
    L(mp.outputs[0], nz.inputs[0])
    L(nz.outputs["Fac"], band.inputs[0])
    L(band.outputs[0], fac.inputs[0])
    L(fac.outputs[0], rip.inputs["Factor"])
    L(ramp.outputs[0], rip.inputs[6])
    L(rip.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return _hazed(m)


def _fog(name, k, radius, core=(35.0, 110.0), density=0.6):
    """One sheet of the cloud deck: white and see-through, broken into big soft holes and fading out at its rim, but
    solid around the middle (`core`), where the camera falls through."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (7.0 * k, 5.0 * k, 0.0)     # small shifts: the holes roughly line up
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.011
    nz.inputs["Detail"].default_value = 4.0
    holes = nt.nodes.new("ShaderNodeMapRange")
    holes.inputs["From Min"].default_value, holes.inputs["From Max"].default_value = 0.42, 0.56
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    rim = nt.nodes.new("ShaderNodeMapRange")
    rim.inputs["From Min"].default_value, rim.inputs["From Max"].default_value = 0.55 * radius, radius
    rim.inputs["To Min"].default_value, rim.inputs["To Max"].default_value = 1.0, 0.0
    mid = nt.nodes.new("ShaderNodeMapRange")
    mid.inputs["From Min"].default_value, mid.inputs["From Max"].default_value = core
    mid.inputs["To Min"].default_value, mid.inputs["To Max"].default_value = 1.0, 0.0
    mx = nt.nodes.new("ShaderNodeMath")
    mx.operation = "MAXIMUM"
    a = nt.nodes.new("ShaderNodeMath")
    a.operation = "MULTIPLY"
    d = nt.nodes.new("ShaderNodeMath")
    d.operation, d.inputs[1].default_value = "MULTIPLY", density
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = look.hexc("#f4f6ff")
    L(tc.outputs["Object"], mp.inputs[0])
    L(mp.outputs[0], nz.inputs[0])
    L(nz.outputs["Fac"], holes.inputs[0])
    L(tc.outputs["Object"], ln.inputs[0])
    L(ln.outputs["Value"], rim.inputs[0])
    L(ln.outputs["Value"], mid.inputs[0])
    L(holes.outputs[0], mx.inputs[0])
    L(mid.outputs[0], mx.inputs[1])
    L(mx.outputs[0], a.inputs[0])
    L(rim.outputs[0], a.inputs[1])
    L(a.outputs[0], d.inputs[0])
    L(d.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def _lathe(profile, seg=24, wobble=None):
    """Surface of revolution around z. `profile` [(r, z)] runs from the top down (r == 0 makes a pole); faces point
    outward. `wobble(theta)` scales r per angle (irregular mountains)."""
    th = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    w = wobble(th) if wobble else np.ones(seg)
    verts, rings = [], []
    for r, z in profile:
        if r < 1e-9:
            rings.append([len(verts)])
            verts.append((0.0, 0.0, z))
        else:
            rings.append(list(range(len(verts), len(verts) + seg)))
            verts.extend(zip(r * w * np.cos(th), r * w * np.sin(th), np.full(seg, z)))
    faces = []
    for A, B in zip(rings, rings[1:]):
        for j in range(seg):
            j1 = (j + 1) % seg
            if len(A) == 1:
                faces.append((A[0], B[j], B[j1]))
            elif len(B) == 1:
                faces.append((A[j], B[0], A[j1]))
            else:
                faces.append((A[j], B[j], B[j1], A[j1]))
    return np.array(verts, float), faces


def _sphere(seg=16, rings=10):
    return _lathe([(0.0 if i in (0, rings) else math.sin(math.pi * i / rings), math.cos(math.pi * i / rings))
                   for i in range(rings + 1)], seg)


def _star(inner=0.2):
    """Flat 4-point sparkle star in the XY plane, facing +z."""
    pts = [(0.0, 0.0, 0.0)]
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4
        r = 1.0 if i % 2 == 0 else inner
        pts.append((r * math.cos(a), r * math.sin(a), 0.0))
    return np.array(pts), [(0, 1 + i, 1 + (i + 1) % 8) for i in range(8)]


def _align(n):
    """Rotation matrix taking +z to the unit vector n."""
    n = np.asarray(n, float) / np.linalg.norm(n)
    v, c = np.cross((0, 0, 1), n), n[2]
    if c < -0.9999:
        return np.diag((1.0, -1.0, -1.0))
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx / (1 + c)


def _rot(rx, ry, rz):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    X = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Y = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Z = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Z @ Y @ X


class _Batch:
    """Many transformed copies of template meshes merged into one object (one material, few draw calls)."""

    def __init__(self):
        self.v, self.f, self.n = [], [], 0

    def add(self, tpl, loc, scale=(1, 1, 1), rotz=0.0, rot=None):
        v, faces = tpl
        v = v * np.asarray(scale, float)
        if rotz:
            v = v @ _rot(0, 0, rotz).T
        if rot is not None:
            v = v @ rot.T
        self.v.append(v + np.asarray(loc, float))
        self.f.extend(tuple(i + self.n for i in f) for f in faces)
        self.n += len(v)

    def obj(self, name, mat, shadow=True):
        if not self.v:
            return None
        return _obj(name, np.vstack(self.v), self.f, mat, shadow=shadow)


def _obj(name, verts, faces, mat, smooth=True, shadow=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(np.asarray(verts).tolist(), [], [list(f) for f in faces])
    me.update()
    if smooth:
        me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    if not shadow and hasattr(o, "visible_shadow"):
        o.visible_shadow = False
    return o


def _empty(name, loc):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    e.empty_display_size = 0.5
    bpy.context.scene.collection.objects.link(e)
    return e


def _seg_dist(p, a, b):
    p, a, b = (np.asarray(t, float) for t in (p, a, b))
    t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
    return float(np.linalg.norm(p - a - t * (b - a)))


def _terrain(ground, mat, n=321, extent=2500.0):
    """Grid that is dense at the clearing (~0.35 m) and coarse at the horizon (~85 m)."""
    b = 5.5
    a = extent / (math.exp(b) - 1)
    u = np.linspace(-1, 1, n)
    g = np.sign(u) * a * (np.exp(b * np.abs(u)) - 1)
    X, Y = np.meshgrid(g, g)
    Z = ground(X, Y)
    verts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    i, j = np.meshgrid(np.arange(n - 1), np.arange(n - 1), indexing="ij")
    k = (i * n + j).ravel()
    faces = np.column_stack([k, k + 1, k + n + 1, k + n])
    return _obj("w_terrain", verts, faces, mat)


def _tree_protos():
    """paintbg.tree() prototypes in four green variants at three levels of detail (canopy ~14k, ~3.5k, ~1.1k
    vertices), re-materialled with hazed copies of its paint so one mesh serves near and far."""
    trunk = _p3("trunk", "#4a2f22", "#6e4a33", "#8f6a4a", noise=0.1)
    protos = {}
    for lod, res in enumerate((None, 2.6 / 14, 2.6 / 8)):
        for v in range(4):
            t, c = paintbg.tree((0, 0, 0), height=6.0, radius=2.6, seed=100 + v, variant=v, res=res)
            leaf = _p3(f"leaf_v{v}", *(_hex(c) for c in paintbg.greens(v)))
            t.data.materials[0] = trunk
            for i in range(len(c.data.materials)):
                c.data.materials[i] = leaf
            protos[lod, v] = (t, c)
    return protos


def _hex(rgba):
    """Linear RGBA back to an sRGB hex string (paintbg.greens gives linear colours)."""
    s = [c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055 for c in rgba[:3]]
    return "#" + "".join(f"{round(min(1, max(0, c)) * 255):02x}" for c in s)


def _instance(proto, name, loc, scale, rotz):
    o = proto.copy()                                           # linked duplicate: shares the mesh
    o.name = name
    o.location = loc
    o.scale = (scale, scale, scale)
    o.rotation_euler = (0, 0, rotz)
    bpy.context.scene.collection.objects.link(o)
    return o


def build(seed=7):
    """Build the world into the current scene and return its handles. Set the sky (paintbg.sky()) and the sun
    (look.sun()) yourself."""
    rnd = random.Random(seed)
    ground = _make_ground(rnd)
    ev = bpy.context.scene.eevee
    if hasattr(ev, "shadow_pool_size") and int(ev.shadow_pool_size) < 1024:
        ev.shadow_pool_size = "1024"           # the sun's shadow over 5 km of land overflows the default 512 MB pool
    M = dict(
        sand=_p3("sand", "#d9c39a", "#efdcb5", "#fff0d0", noise=0.1),
        mud=_p3("mud", "#6e4a33", "#8f6a4a", "#a8845e", noise=0.12),
        stem=_p3("stem", "#d8c2a8", "#f3e4cf", "#fff8ee", noise=0.08),
        gill=_p3("gill", "#c49a86", "#e3bba6", "#f0cdb8", noise=0.05),
        spot=_p3("spot", "#e6dcef", "#ffffff", "#ffffff", noise=0.0),
        mountain=_p3("mountain", "#5b7fc0", "#7d9fd8", "#a9c3ee", cuts=(0.3, 0.62), noise=0.12, scale=2.0),
        snow=_p3("snow", "#b9c8ee", "#e3ecff", "#ffffff", noise=0.08, scale=2.0),
        cloud=_p3("cloud", "#c9c8ea", "#eef1ff", "#ffffff", cuts=(0.22, 0.5), noise=0.08),
        water=_water(),
        sparkle=look.flat("w_sparkle", look.hexc("#ffffff"), 1.6),
    )
    caps = [_p3("cap_pink", "#d9567c", "#ff8fab", "#ffc2d1"), _p3("cap_peach", "#e08a5c", "#ffb48a", "#ffd9bd"),
            _p3("cap_lilac", "#8a72d6", "#b8a4f0", "#ddd1ff"), _p3("cap_mint", "#4fb89a", "#8ee3c8", "#c8f5e6"),
            _p3("cap_butter", "#e0b43a", "#ffe17a", "#fff2b8"), _p3("cap_red", "#d9483c", "#ff7a66", "#ffb3a6")]
    flowers = [_p3("fl_white", "#d8dcef", "#ffffff", "#ffffff", noise=0.0),
               _p3("fl_yellow", "#e0b43a", "#ffe066", "#fff3a8", noise=0.0),
               _p3("fl_pink", "#e06a9a", "#ff9ec4", "#ffd0e3", noise=0.0),
               _p3("fl_lilac", "#9a7ae0", "#c7a8ff", "#e6d8ff", noise=0.0)]
    blades = [_p3(f"blade{i}", *(_hex(c) for c in paintbg.greens(i))) for i in range(3)]
    sph, ball = _sphere(16, 10), _sphere(8, 5)
    h = dict(ground=ground)

    h["terrain"] = _terrain(ground, grass())
    h["terrain"].visible_shadow = False                        # the painted light bands shade the hills already

    # --- keep-outs: the clearing, the pond, the camera's last stretch of fall ---------------------------------------
    path_a, path_b = np.array(FALL[3][1][:2]), np.array(FALL[4][1][:2])
    eye = np.array(FALL[4][1][:2])

    def pond_e(x, y):
        return ((x - POND[0]) / POND_R[0]) ** 2 + ((y - POND[1]) / POND_R[1]) ** 2

    def free(x, y, clear=10.0, pond=1.6, path=9.0):
        return (math.hypot(x, y) > clear and pond_e(x, y) > pond
                and _seg_dist((x, y), path_a, path_b) > path and not in_pov(x, y))

    def in_pov(x, y, half=18.0, reach=700.0):
        """Inside the middle of Kai's view in S13, which stays open meadow under the sky (the HUD sits there)."""
        dx, dy = x - POV[0][0], y - POV[0][1]
        return abs(math.degrees(math.atan2(dx, dy))) < half and math.hypot(dx, dy) < reach

    # --- pond and puddle ------------------------------------------------------------------------------------------
    disc = _lathe([(0, 0.0), (1.0, 0.0)], 48)
    pond = _Batch()
    pond.add(disc, (*POND, POND_Z), (POND_R[0] * 1.02, POND_R[1] * 1.02, 1))
    h["pond"] = pond.obj("w_pond", M["water"], shadow=False)
    pud = _Batch()
    pud.add(disc, (*PUDDLE, PUDDLE_Z), (PUDDLE_R, PUDDLE_R * 0.86, 1))
    h["puddle_water"] = pud.obj("w_puddle", M["water"], shadow=False)
    # a low rounded lip (the top half of a torus) that hides where the water meets the terrain
    ring = _lathe([(0.97 + 0.07 * math.cos(a), 0.035 * math.sin(a) + 0.01) for a in np.linspace(math.pi, 0, 9)], 48)
    shore = _Batch()
    shore.add(ring, (*POND, POND_Z), (POND_R[0], POND_R[1], 4.0))
    h["shore"] = shore.obj("w_shore", M["sand"])
    mud = _Batch()
    mud.add(ring, (*PUDDLE, PUDDLE_Z), (PUDDLE_R, PUDDLE_R * 0.86, 2.0))
    h["puddle_rim"] = mud.obj("w_puddle_rim", M["mud"])
    h["clearing"] = _empty("w_clearing", (0, 0, 0))
    h["puddle"] = _empty("w_puddle_spot", (*PUDDLE, PUDDLE_Z))

    stars = _star()
    h["sparkles"] = []
    for i in range(26):
        a, r = rnd.uniform(0, 2 * math.pi), math.sqrt(rnd.random()) * 0.85
        loc = (POND[0] + r * POND_R[0] * math.cos(a), POND[1] + r * POND_R[1] * math.sin(a), POND_Z + 0.12)
        h["sparkles"].append(_sparkle(f"w_sparkle{i}", stars, loc, rnd.uniform(0.12, 0.3), M["sparkle"]))
    for i in range(3):
        a = rnd.uniform(0, 2 * math.pi)
        loc = (PUDDLE[0] + 0.4 * math.cos(a), PUDDLE[1] + 0.3 * math.sin(a), PUDDLE_Z + 0.05)
        h["sparkles"].append(_sparkle(f"w_psparkle{i}", stars, loc, rnd.uniform(0.05, 0.08), M["sparkle"]))

    # --- giant candy mushrooms: accents, a few as big as houses ---------------------------------------------------
    stem_t = _lathe([(0, 1.0), (0.8, 1.0), (0.86, 0.7), (1.0, 0.3), (1.12, 0.07), (1.0, 0.0), (0, -0.05)], 20)
    dome_t = _lathe([(0.0 if a == 0 else math.sin(a), math.cos(a)) for a in np.linspace(0, 0.56 * math.pi, 10)], 32)
    under_t = _lathe([(math.sin(0.56 * math.pi), math.cos(0.56 * math.pi)), (0.6, -0.12), (0.25, -0.05), (0, -0.02)], 32)
    stems, unders, spots = _Batch(), _Batch(), _Batch()
    capb = [_Batch() for _ in caps]
    shrooms = [(-14.0, 18.0, 9.0, 6.0, 0), (16.0, 30.0, 13.0, 8.0, 2), (24.0, 44.0, 6.0, 4.0, 4),
               (-26.0, 14.0, 11.0, 7.0, 5), (31.0, -6.0, 8.0, 5.5, 1), (-30.0, 44.0, 14.0, 9.0, 3),
               (-38.0, -24.0, 9.0, 6.0, 0)]
    for x, y in [(-6.2, 6.2), (-7.0, 7.0), (-5.6, 7.2), (4.6, 5.4), (5.4, 6.1), (-6.5, 1.5)]:
        shrooms.append((x, y, rnd.uniform(0.35, 0.8), rnd.uniform(0.3, 0.6), rnd.randrange(len(caps))))
    tries = 0
    while len(shrooms) < 24 and tries < 2000:
        tries += 1
        d, a = 60 + 500 * rnd.random(), rnd.uniform(0, 2 * math.pi)
        x, y = d * math.cos(a), d * math.sin(a)
        if free(x, y, clear=14, path=14):
            s = rnd.uniform(1.0, 2.0) * (1 + d / 150)
            shrooms.append((x, y, 4.0 * s, 2.6 * s, rnd.randrange(len(caps))))
    for x, y, hs, rc, ci in shrooms:
        z0 = float(ground(x, y))
        rs = max(0.06, rc * 0.24)
        rz = rnd.uniform(0, 2 * math.pi)
        stems.add(stem_t, (x, y, z0 - 0.05 * hs), (rs, rs, hs), rz)
        hc = rc * rnd.uniform(0.55, 0.72)
        top = (x, y, z0 + hs * 0.93)
        capb[ci].add(dome_t, top, (rc, rc, hc), rz)
        unders.add(under_t, top, (rc, rc, hc), rz)
        for _ in range(rnd.randint(5, 9)):
            a, th = rnd.uniform(0.12, 0.42) * math.pi, rnd.uniform(0, 2 * math.pi)
            n = np.array((math.sin(a) * math.cos(th) / rc, math.sin(a) * math.sin(th) / rc, math.cos(a) / hc))
            p = np.array(top) + (rc * math.sin(a) * math.cos(th), rc * math.sin(a) * math.sin(th), hc * math.cos(a))
            s = rc * rnd.uniform(0.09, 0.17)
            spots.add(ball, p, (s, s * rnd.uniform(0.8, 1.1), 0.3 * s), rot=_align(n))
    h["mushrooms"] = [o for o in [stems.obj("w_mush_stems", M["stem"]), unders.obj("w_mush_gills", M["gill"]),
                                  spots.obj("w_mush_spots", M["spot"])] +
                      [b.obj(f"w_mush_caps{i}", caps[i]) for i, b in enumerate(capb)] if o]

    # --- cauliflower trees in groves (paintbg.tree prototypes, instanced; detail drops with distance) -------------
    protos = _tree_protos()
    groves = [(14, 38, 12), (-12, 40, 10), (25, 62, 10), (-30, 25, 9), (35, 15, 8), (-40, -10, 9), (20, -30, 8),
              (-5, 78, 12), (50, 45, 9), (-55, 55, 9)]
    groves += [(d * math.cos(a), d * math.sin(a), rnd.randint(6, 14)) for d, a in
               ((rnd.uniform(90, 1300), rnd.uniform(0, 2 * math.pi)) for _ in range(46))]
    h["trees"] = []
    for gx, gy, count in groves:
        d0 = math.hypot(gx, gy)
        spread = 7 + 0.05 * d0
        for _ in range(count):
            x, y = gx + rnd.gauss(0, spread), gy + rnd.gauss(0, spread)
            if not free(x, y, clear=12, path=10):
                continue
            d = math.hypot(x, y)
            lod = 0 if d < 70 else (1 if d < 320 else 2)
            s = rnd.uniform(0.75, 1.3) * (1 + max(0.0, d - 150) / 500)      # far forests a bit bigger
            t, c = protos[lod, rnd.randrange(4)]
            z0 = float(ground(x, y)) - 0.1
            rz = rnd.uniform(0, 2 * math.pi)
            n = len(h["trees"])
            h["trees"] += [_instance(t, f"w_trunk{n}", (x, y, z0), s, rz),
                           _instance(c, f"w_canopy{n}", (x, y, z0), s, rz)]
            if lod:                                            # past 70 m: no shadow casting (EEVEE's shadow pool)
                for o in h["trees"][-2:]:
                    o.visible_shadow = False
    for t, c in protos.values():
        bpy.data.objects.remove(t)
        bpy.data.objects.remove(c)

    # --- flower meadows and grass blades ---------------------------------------------------------------------------
    fb, bb = [_Batch() for _ in flowers], [_Batch() for _ in blades]
    patches = [(-1.0, -2.5, 2.6, 90), (-6.0, 3.0, 3.0, 110), (4.0, -2.0, 2.5, 90), (-4.0, 11.0, 3.5, 120),
               (13.0, 3.0, 3.5, 110), (-12.0, -6.0, 5.0, 150), (3.0, 22.0, 4.0, 120)]
    patches += [(d * math.cos(a), d * math.sin(a), rnd.uniform(5, 14), rnd.randint(80, 220)) for d, a in
                ((rnd.uniform(25, 260), rnd.uniform(0, 2 * math.pi)) for _ in range(22))]
    for px, py, spread, count in patches:
        pal = rnd.sample(range(len(flowers)), 2)
        for _ in range(count):
            x, y = px + rnd.gauss(0, spread * 0.5), py + rnd.gauss(0, spread * 0.5)
            if (math.hypot(x - PUDDLE[0], y - PUDDLE[1]) < 1.8 or pond_e(x, y) < 1.3
                    or math.hypot(x - eye[0], y - eye[1]) < 3.0):
                continue
            r = rnd.uniform(0.035, 0.06) * (1 + math.hypot(x, y) / 60)
            fb[rnd.choice(pal)].add(ball, (x, y, float(ground(x, y)) + 0.1), (r, r, r * 0.7))
    blade = _lathe([(0, 1.0), (1.0, 0.0), (0, -0.05)], 4)
    for _ in range(900):                                       # clumps of three blades, only near the clearing
        d, a = 2.0 + 28 * rnd.random() ** 1.5, rnd.uniform(0, 2 * math.pi)
        x, y = d * math.cos(a), d * math.sin(a)
        if (math.hypot(x - PUDDLE[0], y - PUDDLE[1]) < 1.3 or pond_e(x, y) < 1.15
                or math.hypot(x - eye[0], y - eye[1]) < 1.6):
            continue
        z = float(ground(x, y)) - 0.02
        for _ in range(3):
            ht = rnd.uniform(0.22, 0.45)
            bb[rnd.randrange(len(blades))].add(blade, (x + rnd.uniform(-0.08, 0.08), y + rnd.uniform(-0.05, 0.05), z),
                                               (0.035, 0.035, ht),
                                               rot=_rot(rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(0, 6)))
    h["flowers"] = [o for o in [b.obj(f"w_flowers{i}", flowers[i]) for i, b in enumerate(fb)] +
                    [b.obj(f"w_blades{i}", blades[i]) for i, b in enumerate(bb)] if o]

    # --- distant blue mountains ----------------------------------------------------------------------------------
    mts, snow = _Batch(), _Batch()
    peaks = [(math.radians(8), 1050, 360, 430), (math.radians(32), 1250, 300, 480), (math.radians(-22), 1150, 260, 380)]
    peaks += [(rnd.uniform(0, 2 * math.pi), rnd.uniform(850, 1500), rnd.uniform(180, 330), rnd.uniform(280, 480))
              for _ in range(14)]
    for az, d, ht, rad in peaks:
        x, y = d * math.sin(az), d * math.cos(az)
        ph1, ph2 = rnd.uniform(0, 6), rnd.uniform(0, 6)

        def wob(t, p1=ph1, p2=ph2):
            return 1 + 0.09 * np.sin(3 * t + p1) + 0.05 * np.sin(5 * t + p2)
        prof = [(rad * u, ht * math.cos(math.pi / 2 * u) ** 1.4) for u in np.linspace(0, 1, 14)] + [(rad * 1.05, -40), (0, -40)]
        prof[0] = (0, ht)
        mts.add(_lathe(prof, 40, wob), (x, y, float(ground(x, y)) - 5))
        if ht > 280:
            sp = [(r * 1.004, z + 0.5) for r, z in prof[:6]] + [(0, ht * 0.72)]
            snow.add(_lathe(sp, 40, wob), (x, y, float(ground(x, y)) - 5))
    h["mountains"] = [o for o in (mts.obj("w_mountains", M["mountain"], shadow=False),
                                  snow.obj("w_snowcaps", M["snow"], shadow=False)) if o]

    # --- clouds: a sea of cumulus around the deck (dense near the fall, thinning out), towering cumulus far away -----
    cl = _Batch()
    n = 0
    while n < 230:
        d, a = 45 + 420 * math.sqrt(rnd.random()), rnd.uniform(0, 2 * math.pi)
        if rnd.random() > (1.0 if d < 190 else max(0.12, 1 - (d - 190) / 230)):
            continue
        n += 1
        cx, cy = DECK_C[0] + d * math.cos(a), DECK_C[1] + d * math.sin(a)
        size = rnd.uniform(10, 22) if d < 220 else rnd.uniform(6, 14)
        _cumulus(cl, sph, rnd, (cx, cy, rnd.uniform(DECK_Z[0] - 2, DECK_Z[1] - 10)), size, rnd.randint(4, 8))
    for _ in range(26):                                        # small heads around the hole the camera falls through
        d, a = rnd.uniform(28, 45), rnd.uniform(0, 2 * math.pi)
        _cumulus(cl, sph, rnd, (DECK_C[0] + d * math.cos(a), DECK_C[1] + d * math.sin(a), rnd.uniform(118, 126)),
                 rnd.uniform(6, 10), rnd.randint(3, 5))
    for _ in range(12):
        az = rnd.uniform(-1.2, 1.2) if rnd.random() < 0.7 else rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(700, 1700)
        _cumulus(cl, sph, rnd, (d * math.sin(az), d * math.cos(az), rnd.uniform(110, 230)), rnd.uniform(25, 55),
                 rnd.randint(6, 11), tower=True)
    h["clouds"] = [cl.obj("w_clouds", M["cloud"], shadow=False)]
    deck_disc = _lathe([(0, 0.0), (DECK_R, 0.0)], 64)
    h["deck"] = []
    for k, z in enumerate(np.linspace(DECK_Z[0], DECK_Z[1], 6)):
        b = _Batch()
        b.add(deck_disc, (0, 0, 0))
        o = b.obj(f"w_deck{k}", _fog(f"w_fog{k}", k, DECK_R), shadow=False)
        o.location = (*DECK_C, z)
        h["deck"].append(o)
    return h


def _cumulus(batch, sph, rnd, c, size, n, tower=False):
    """A cluster of soft balls: a wide flat-bottomed base and rounder heads on top (taller when `tower`)."""
    cx, cy, cz = c
    for i in range(n):
        r = size * rnd.uniform(0.5, 1.0)
        up = (i / n) * size * (1.4 if tower else 0.5)
        x = cx + rnd.uniform(-1.1, 1.1) * size * (1 - 0.4 * i / n)
        y = cy + rnd.uniform(-0.6, 0.6) * size
        batch.add(sph, (x, y, cz + up + 0.35 * r), (r * 1.25, r, r * 0.8))


def _sparkle(name, star, loc, size, mat):
    b = _Batch()
    b.add(star, (0, 0, 0), (size, size, 1))
    o = b.obj(name, mat, shadow=False)
    o.location = loc
    o["world_sparkle"] = size
    return o


def aim_sparkles(cam):
    """Turn the pond sparkles to face `cam` (fall_camera and pov_camera do this; call it after switching to a camera
    of your own)."""
    for o in bpy.context.scene.objects:
        if "world_sparkle" in o:
            c = o.constraints.get("aim") or o.constraints.new("TRACK_TO")
            c.name = "aim"
            c.target, c.track_axis, c.up_axis = cam, "TRACK_Z", "UP_Y"


def _path():
    """The fall as smooth curves: FALL keyed on a scratch object with Blender's auto-clamped Bezier handles (the fall
    eases in, keeps a steady pace through the clouds and floats to a stop). Returns sample(fraction) -> (location,
    rotation, focus distance)."""
    tmp = bpy.data.objects.new("w_path", None)
    bpy.context.scene.collection.objects.link(tmp)
    prev = None
    for frac, pos, tgt, roll in FALL:
        q = (Vector(tgt) - Vector(pos)).to_track_quat("-Z", "Y") @ Quaternion((0, 0, 1), math.radians(roll))
        prev = q.to_euler("XYZ", prev) if prev else q.to_euler("XYZ")
        tmp.location, tmp.rotation_euler = pos, prev
        tmp["focus"] = (Vector(tgt) - Vector(pos)).length
        for path in ("location", "rotation_euler", '["focus"]'):
            tmp.keyframe_insert(path, frame=frac * 1000)
    from . import anim
    act = tmp.animation_data.action
    fcs = {(fc.data_path, fc.array_index): fc for fc in anim.all_fcurves(act)}
    bpy.data.objects.remove(tmp)

    def sample(frac):
        f = frac * 1000
        return (tuple(fcs["location", i].evaluate(f) for i in range(3)),
                tuple(fcs["rotation_euler", i].evaluate(f) for i in range(3)), fcs['["focus"]', 0].evaluate(f))
    return sample


def _camera(cam, name, lens, fstop):
    sc = bpy.context.scene
    if cam is None:
        cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
        sc.collection.objects.link(cam)
    cd = cam.data
    cd.lens = lens
    cd.clip_start, cd.clip_end = 0.1, 5000.0
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = fstop
    sc.camera = cam
    aim_sparkles(cam)
    return cam


def fall_camera(f0, f1, start=0.0, end=1.0, cam=None, lens=24, fstop=0.15):
    """The descent from above the cloud deck, through it (looking out at the sky), over the land, down to Kai's POV in
    the clearing. f0..f1 plays the path from fraction `start` to `end`: the whole fall (0, 1) is a 4-5 s shot
    (f1 - f0 = 96..120); Episode 1 plays world.S11 and world.S12 as two shots. Keyed on every frame (camera on 1s).
    Focus follows the look-at point; the f-stop is the series' anime-strength blur."""
    cam = _camera(cam, "w_fall_cam", lens, fstop)
    sample = _path()
    for f in range(f0, f1 + 1):
        loc, rot, focus = sample(start + (end - start) * (f - f0) / (f1 - f0))
        cam.location, cam.rotation_euler = loc, rot
        cam.data.dof.focus_distance = focus
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.keyframe_insert("dof.focus_distance", frame=f)
    return cam


def pov_camera(cam=None, lens=24, fstop=0.15, focus=20.0):
    """S13: Kai's locked POV of the meadow (the last frame of the fall). The upper middle (y 250-820 at 720x1280) is
    sky and soft distant hills for the HUD; the pond and flowers sit low, the giant mushrooms at the edges."""
    cam = _camera(cam, "w_pov_cam", lens, fstop)
    pos, tgt = POV
    cam.location = pos
    cam.rotation_euler = (Vector(tgt) - Vector(pos)).to_track_quat("-Z", "Y").to_euler("XYZ")
    cam.data.dof.focus_distance = focus
    return cam


def twinkle(h, f0, f1, seed=3):
    """The pond sparkles pop on and off (constant keys, anime timing)."""
    from . import anim
    rnd = random.Random(seed)
    for o in h["sparkles"]:
        f = f0 + rnd.randrange(0, 12)
        while f <= f1:
            on = rnd.uniform(0.6, 1.2)
            for df, s in ((0, 0.0), (2, on), (6, on * 0.55), (10, 0.0)):
                o.scale = (s, s, s)
                o.keyframe_insert("scale", frame=f + df)
            f += rnd.randrange(14, 30)
        for fc in anim.all_fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
