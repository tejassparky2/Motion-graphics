"""Episode 1's storm and the death / rebirth transitions, built in front of whatever camera you pass, so they work in
any scene: rain(), lightning(), power_out(), white_out(), birds_and_light(). Nothing here is graphic: the "death" is a
power cut to black, then a slow fade to white, then a soft pastel sky.

Everything is simple geometry with unlit (emission) materials, parented to the camera at a fixed depth and sized to
fill its view. Screen areas are (x0, y0, x1, y1) in 0..1 with y up (Blender's window coordinates); screen_rect() finds
the area a window opening covers. Layering, nearest first: flash, white veil, white-out, black, birds, sun rays, sky;
rain and the lightning bolt sit at a chosen depth inside the scene (e.g. just beyond a window).

Typical use (frames are examples):
    storm.rain(cam, 1, 120, area=storm.screen_rect(cam, window_corners))
    storm.lightning(cam, 40, area=...)
    storm.power_out(cam, 96)
    storm.white_out(cam, 110, 150)
    storm.birds_and_light(cam, 150, 190)
"""
import math
import random

import bpy
from mathutils import Vector

from . import look

FULL = (0.0, 0.0, 1.0, 1.0)
# camera-space depths of the full-screen layers (nearest first); clip_start is raised below them if needed
D_FLASH, D_VEIL, D_WHITE, D_BLACK, D_BIRDS, D_RAYS, D_SKY = 0.20, 0.21, 0.22, 0.23, 0.26, 0.28, 0.30
_groups = {}   # camera name -> [(kind, empty)], so a later transition can retire an earlier one


# ---------------------------------------------------------------------------------------------------- camera helpers
def view_size(cam, depth, sc=None):
    """Width and height (metres) the camera sees at `depth` in front of it."""
    sc = sc or bpy.context.scene
    r = sc.render
    px, py = r.resolution_x * r.pixel_aspect_x, r.resolution_y * r.pixel_aspect_y
    d = cam.data
    fit = d.sensor_fit
    if fit == "AUTO":
        fit = "HORIZONTAL" if px >= py else "VERTICAL"
    sensor = d.sensor_width if (d.sensor_fit == "AUTO" or fit == "HORIZONTAL") else d.sensor_height
    span = depth * sensor / d.lens
    if d.type == "ORTHO":
        span = d.ortho_scale
    return (span, span * py / px) if fit == "HORIZONTAL" else (span * px / py, span)


def screen_rect(cam, points, sc=None):
    """The 0..1 screen rectangle (x0, y0, x1, y1), y up, covering world-space `points`."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = sc or bpy.context.scene
    co = [world_to_camera_view(sc, cam, Vector(p)) for p in points]
    return (min(c.x for c in co), min(c.y for c in co), max(c.x for c in co), max(c.y for c in co))


def _group(cam, kind, f0=None, f1=None):
    """An empty parented to the camera; its scale is keyed 0 outside [f0, f1] so all its children vanish."""
    e = bpy.data.objects.new(f"storm_{kind}_{len(_groups.get(cam.name, []))}", None)
    bpy.context.scene.collection.objects.link(e)
    e.parent = cam
    if f0 is not None:
        _key(e, "scale", f0 - 1, (0, 0, 0))
        _key(e, "scale", f0, (1, 1, 1))
    if f1 is not None:
        _key(e, "scale", f1 + 1, (0, 0, 0))
    _groups.setdefault(cam.name, []).append((kind, e))
    if cam.data.clip_start > D_FLASH * 0.5:
        cam.data.clip_start = D_FLASH * 0.5
    return e


def _retire(cam, kinds, f):
    """Hide every earlier group of these kinds from frame f on."""
    for kind, e in _groups.get(cam.name, []):
        if kind in kinds:
            _key(e, "scale", f - 1, (1, 1, 1))
            _key(e, "scale", f, (0, 0, 0))


def _key(owner, path, frame, value, interp="CONSTANT"):
    setattr(owner, path, value)
    owner.keyframe_insert(data_path=path, frame=frame)
    _interp(owner.animation_data.action, frame, interp)


def _key_socket(sock, frame, value, interp="LINEAR"):
    sock.default_value = value
    sock.keyframe_insert("default_value", frame=frame)
    _interp(sock.id_data.animation_data.action, frame, interp)


def _interp(action, frame, interp):
    for fc in _all_fcurves(action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - frame) < 0.01:
                kp.interpolation = interp


def _all_fcurves(action):
    out = []
    try:
        out += list(action.fcurves)
    except Exception:
        pass
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out += list(bag.fcurves)
    return out


def _mesh(name, verts, faces, mat, parent, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.parent = parent
    o.location = loc
    return o


def _screen_plane(name, cam, depth, mat, parent):
    """A quad that fills the camera view (with a margin) at `depth`."""
    w, h = view_size(cam, depth)
    w, h = w * 0.56, h * 0.56
    return _mesh(name, [(-w, -h, 0), (w, -h, 0), (w, h, 0), (-w, h, 0)], [(0, 1, 2, 3)], mat, parent, (0, 0, -depth))


# ------------------------------------------------------------------------------------------------------- materials
def _overlay(name, rgba, alpha=1.0, area=None):
    """Unlit and see-through. Node 'Alpha' (a Value) scales the opacity and can be keyed; node 'Color' is the emission.
    With `area`, it only shows inside that screen rectangle (window coordinates), e.g. through a window."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.name = "Color"
    em.inputs[0].default_value = rgba
    a = nt.nodes.new("ShaderNodeValue")
    a.name = "Alpha"
    a.outputs[0].default_value = alpha
    fac = a.outputs[0]
    if area and tuple(area) != FULL:
        fac = _mul(nt, fac, _rect_mask(nt, area))
    L(fac, mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def _mul(nt, a, b):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = "MULTIPLY"
    nt.links.new(a, n.inputs[0])
    nt.links.new(b, n.inputs[1])
    return n.outputs[0]


def _rect_mask(nt, area):
    """1 inside the screen rectangle, 0 outside."""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Window"], sep.inputs[0])
    x0, y0, x1, y1 = area
    m = None
    for out, lo, hi in ((sep.outputs[0], x0, x1), (sep.outputs[1], y0, y1)):
        for op, v in (("GREATER_THAN", lo), ("LESS_THAN", hi)):
            n = nt.nodes.new("ShaderNodeMath")
            n.operation = op
            nt.links.new(out, n.inputs[0])
            n.inputs[1].default_value = v
            m = n.outputs[0] if m is None else _mul(nt, m, n.outputs[0])
    return m


def _alpha(m):
    return m.node_tree.nodes["Alpha"].outputs[0]


# ------------------------------------------------------------------------------------------------------------ rain
def rain(cam, f0, f1, area=FULL, depth=6.0, angle=14.0, density=1.0, color="#bfe3ff", seed=11):
    """Anime rain: thin, angled, light-blue streaks between frames f0 and f1, re-scattered every frame (on 1s), in
    three layers (near streaks longer and brighter). `area` limits it to a screen rectangle (e.g. a window);
    `depth` puts it inside the scene (beyond the window glass), `angle` tilts the fall to the left in degrees."""
    rnd = random.Random(seed)
    g = _group(cam, "rain", f0, f1)
    a = math.radians(angle)
    dx, dy = math.sin(a), -math.cos(a)                 # fall direction (down and to the left in screen space)
    nx, ny = -dy, dx
    objs = []
    for li, (dmul, n, lng, wid, alpha) in enumerate(((0.8, 70, 0.11, 0.0030, 0.85),
                                                       (1.0, 110, 0.08, 0.0022, 0.6),
                                                       (1.4, 150, 0.05, 0.0016, 0.4))):
        d = depth * dmul
        W, H = view_size(cam, d)
        verts, faces = [], []
        for i in range(int(n * density)):
            cx, cy = rnd.uniform(-W, W), rnd.uniform(-H, H)   # the layer covers 2x the view; it jumps each frame
            ln = H * lng * rnd.uniform(0.6, 1.4)
            hw = H * wid * 0.5
            x0, y0 = cx - dx * ln * 0.5, cy - dy * ln * 0.5
            x1, y1 = cx + dx * ln * 0.5, cy + dy * ln * 0.5
            k = len(verts)
            verts += [(x0 + nx * hw * 0.3, y0 + ny * hw * 0.3, 0), (x1 + nx * hw, y1 + ny * hw, 0),
                      (x1 - nx * hw, y1 - ny * hw, 0), (x0 - nx * hw * 0.3, y0 - ny * hw * 0.3, 0)]
            faces.append((k, k + 1, k + 2, k + 3))
        m = _overlay(f"rain_m{li}_{f0}", look.hexc(color), alpha, area)
        o = _mesh(f"rain{li}_{f0}", verts, faces, m, g, (0, 0, -d))
        for f in range(f0, f1 + 1):
            _key(o, "location", f, (rnd.uniform(-W, W) * 0.5, rnd.uniform(-H, H) * 0.5, -d))
        objs.append(o)
    return {"group": g, "layers": objs}


# ------------------------------------------------------------------------------------------------------- lightning
def _bolt_path(rnd, p0, p1, levels, jag):
    pts = [p0, p1]
    for lv in range(levels):
        nxt = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            nxt += [(mx + rnd.uniform(-1, 1) * seg * jag, my + rnd.uniform(-0.3, 0.3) * seg * jag), b]
        pts = nxt
    return pts


def _ribbon(pts, w0, w1):
    """A flat ribbon along a polyline with mitred joints (no gaps or overlaps), tapering from width w0 to w1."""
    n = len(pts)
    segs = []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1e-6
        segs.append((-dy / ln, dx / ln))
    verts = []
    for i, p in enumerate(pts):
        if i == 0 or i == n - 1:
            nx, ny = segs[0] if i == 0 else segs[-1]
            k = 1.0
        else:
            (ax, ay), (bx, by) = segs[i - 1], segs[i]
            nx, ny = ax + bx, ay + by
            ln = math.hypot(nx, ny) or 1e-6
            nx, ny = nx / ln, ny / ln
            k = min(2.0, 1.0 / max(0.3, nx * ax + ny * ay))     # keep the width across sharp turns
        w = (w0 + (w1 - w0) * i / (n - 1)) * 0.5 * k
        verts += [(p[0] + nx * w, p[1] + ny * w, 0), (p[0] - nx * w, p[1] - ny * w, 0)]
    faces = [(2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1) for i in range(n - 1)]
    return verts, faces


def lightning(cam, frame, area=FULL, depth=28.0, x=None, flash=True, seed=7, color="#ffffff", glow="#7cc4ff",
              flash_color="#e4f2ff"):
    """An anime lightning bolt in the sky (white core, blue glow, two forks) striking down through `area` at `frame`,
    flickering on-off-on over 4 frames, plus a full-screen blue-white flash. `x` is the strike's screen x (0..1);
    `depth` should be beyond the window and in front of the far sky."""
    rnd = random.Random(seed)
    g = _group(cam, "lightning", frame, frame + 4)
    W, H = view_size(cam, depth)
    x0a, y0a, x1a, y1a = area
    sx = x if x is not None else x0a + (x1a - x0a) * rnd.uniform(0.3, 0.7)
    to_local = lambda u, v: ((u - 0.5) * W, (v - 0.5) * H)   # noqa: E731
    top = to_local(sx + rnd.uniform(-0.03, 0.03), min(1.05, y1a + 0.05))
    bot = to_local(sx + rnd.uniform(-0.12, 0.12), y0a + (y1a - y0a) * rnd.uniform(0.0, 0.2))
    main = _bolt_path(rnd, top, bot, 5, 0.32)
    paths = [(main, 1.0)]
    for _ in range(2):
        i = rnd.randint(len(main) // 5, len(main) * 3 // 5)
        a = main[i]
        side = rnd.choice((-1, 1))
        b = (a[0] + side * H * rnd.uniform(0.08, 0.16), a[1] - H * rnd.uniform(0.10, 0.2))
        paths.append((_bolt_path(rnd, a, b, 4, 0.35), 0.55))
    core_m = _overlay(f"bolt_core_{frame}", look.hexc(color), 1.0, area)
    glow_m = _overlay(f"bolt_glow_{frame}", look.hexc(glow), 1.0, area)
    objs = []
    for j, (p, s) in enumerate(paths):
        v, f = _ribbon(p, H * 0.006 * s, H * 0.002 * s)
        objs.append(_mesh(f"bolt_core{j}_{frame}", v, f, core_m, g, (0, 0, -depth)))
        v, f = _ribbon(p, H * 0.024 * s, H * 0.008 * s)
        objs.append(_mesh(f"bolt_glow{j}_{frame}", v, f, glow_m, g, (0, 0, -depth - 0.05)))
    for m in (core_m, glow_m):
        for fr, k in ((frame - 1, 0), (frame, 1), (frame + 1, 1), (frame + 2, 0), (frame + 3, 1), (frame + 4, 0)):
            _key_socket(_alpha(m), fr, k, "CONSTANT")
    out = {"group": g, "bolt": objs}
    if flash:
        fg = _group(cam, "flash", frame, frame + 6)
        fm = _overlay(f"flash_m_{frame}", look.hexc(flash_color), 0.0)
        out["flash"] = _screen_plane(f"flash_{frame}", cam, D_FLASH, fm, fg)
        for fr, k in ((frame - 1, 0), (frame, 0.85), (frame + 1, 0.12), (frame + 2, 0), (frame + 3, 0.5),
                      (frame + 4, 0.1), (frame + 5, 0)):
            _key_socket(_alpha(fm), fr, k, "CONSTANT")
    return out


# ------------------------------------------------------------------------------------------------- the transitions
def power_out(cam, frame, flicker=True):
    """Everything cuts to black at `frame` (after a one-frame stutter if `flicker`) and stays black until a later
    white_out() or birds_and_light() takes over."""
    g = _group(cam, "black")
    m = _overlay(f"black_m_{frame}", (0, 0, 0, 1), 0.0)
    p = _screen_plane(f"black_{frame}", cam, D_BLACK, m, g)
    keys = [(frame - 1, 0.0), (frame, 1.0)]
    if flicker:
        keys = [(frame - 4, 0.0), (frame - 3, 1.0), (frame - 2, 0.0)] + keys
    for fr, k in keys:
        _key_socket(_alpha(m), fr, k, "CONSTANT")
    return {"group": g, "plane": p}


def _white_mat(name, color, aspect):
    """Emission that brightens from the centre out as node 'Progress' goes 0 -> 1 (pure `color` everywhere at 1)."""
    m = _overlay(name, (0, 0, 0, 1), 0.0)
    nt = m.node_tree
    L = nt.links.new
    pr = nt.nodes.new("ShaderNodeValue")
    pr.name = "Progress"
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (-0.5 * aspect, -0.5, 0)
    mp.inputs["Scale"].default_value = (aspect, 1, 0)
    L(tc.outputs["Window"], mp.inputs[0])
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    L(mp.outputs[0], ln.inputs[0])
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    L(pr.outputs[0], inv.inputs[1])
    edge = nt.nodes.new("ShaderNodeMath")                  # r * 0.9 * (1 - p)
    edge.operation = "MULTIPLY"
    L(ln.outputs[1], edge.inputs[0])
    L(_mul(nt, inv.outputs[0], _const(nt, 0.9)), edge.inputs[1])
    v = nt.nodes.new("ShaderNodeMath")                     # p * 1.25 - edge, clamped
    v.operation = "MULTIPLY_ADD"
    L(pr.outputs[0], v.inputs[0])
    v.inputs[1].default_value = 1.25
    neg = nt.nodes.new("ShaderNodeMath")
    neg.operation = "MULTIPLY"
    L(edge.outputs[0], neg.inputs[0])
    neg.inputs[1].default_value = -1.0
    L(neg.outputs[0], v.inputs[2])
    v.use_clamp = True
    lin = nt.nodes.new("ShaderNodeMath")                   # into linear light so the ramp looks even on screen
    lin.operation = "POWER"
    L(v.outputs[0], lin.inputs[0])
    lin.inputs[1].default_value = 2.2
    col = nt.nodes.new("ShaderNodeMix")
    col.data_type, col.blend_type = "RGBA", "MULTIPLY"
    col.inputs["Factor"].default_value = 1.0
    L(lin.outputs[0], col.inputs[6])
    col.inputs[7].default_value = color
    L(col.outputs[2], nt.nodes["Color"].inputs[0])
    return m


def _const(nt, v):
    n = nt.nodes.new("ShaderNodeValue")
    n.outputs[0].default_value = v
    return n.outputs[0]


def white_out(cam, f0, f1, color="#ffffff"):
    """From frame f0, the screen (black after power_out) glows white from the centre outward, reaching pure white
    everywhere at f1, and holds."""
    g = _group(cam, "white")
    r = bpy.context.scene.render
    m = _white_mat(f"white_m_{f0}", look.hexc(color), r.resolution_x / r.resolution_y)
    p = _screen_plane(f"white_{f0}", cam, D_WHITE, m, g)
    _key_socket(_alpha(m), f0 - 1, 0.0, "CONSTANT")
    _key_socket(_alpha(m), f0, 1.0, "CONSTANT")
    prog = m.node_tree.nodes["Progress"].outputs[0]
    steps = max(2, (f1 - f0) // 3)
    for i in range(steps + 1):
        t = i / steps
        _key_socket(prog, f0 + round((f1 - f0) * t), t * t * (3 - 2 * t), "LINEAR")
    return {"group": g, "plane": p}


def _sky_mat(name, sun, aspect):
    """Pastel anime sky in screen space: blue overhead, cream at the sun, pink low down, soft painted cloud bands."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    L(tc.outputs["Window"], sep.inputs[0])
    gr = nt.nodes.new("ShaderNodeValToRGB")
    cr = gr.color_ramp
    cr.interpolation = "EASE"
    cr.elements[0].position, cr.elements[0].color = 0.0, look.hexc("#ffd3e2")
    cr.elements[1].position, cr.elements[1].color = 1.0, look.hexc("#9fd0ff")
    e = cr.elements.new(0.42)
    e.color = look.hexc("#ffe9e4")
    e = cr.elements.new(0.7)
    e.color = look.hexc("#cfe6ff")
    L(sep.outputs[1], gr.inputs[0])
    # sun glow: distance from the sun in aspect-corrected screen space
    dx = nt.nodes.new("ShaderNodeMath")
    dx.operation = "SUBTRACT"
    L(sep.outputs[0], dx.inputs[0])
    dx.inputs[1].default_value = sun[0]
    dxa = nt.nodes.new("ShaderNodeMath")
    dxa.operation = "MULTIPLY"
    L(dx.outputs[0], dxa.inputs[0])
    dxa.inputs[1].default_value = aspect
    dy = nt.nodes.new("ShaderNodeMath")
    dy.operation = "SUBTRACT"
    L(sep.outputs[1], dy.inputs[0])
    dy.inputs[1].default_value = sun[1]
    cmb = nt.nodes.new("ShaderNodeCombineXYZ")
    L(dxa.outputs[0], cmb.inputs[0])
    L(dy.outputs[0], cmb.inputs[1])
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    L(cmb.outputs[0], ln.inputs[0])
    glow = nt.nodes.new("ShaderNodeValToRGB")
    g = glow.color_ramp
    g.interpolation = "EASE"
    g.elements[0].position, g.elements[0].color = 0.0, (1, 1, 1, 1)
    g.elements[1].position, g.elements[1].color = 0.34, (0, 0, 0, 1)
    e = g.elements.new(0.05)
    e.color = (0.95, 0.95, 0.95, 1)
    L(ln.outputs[1], glow.inputs[0])
    mg = nt.nodes.new("ShaderNodeMix")
    mg.data_type, mg.blend_type = "RGBA", "MIX"
    L(glow.outputs[0], mg.inputs[0])
    L(gr.outputs[0], mg.inputs[6])
    mg.inputs[7].default_value = look.hexc("#fffbea")
    # painted cloud bands: stretched noise, softly lifted toward white
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.6 * aspect, 5.0, 1.0)
    L(tc.outputs["Window"], mp.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 2.0
    L(mp.outputs[0], nz.inputs[0])
    cl = nt.nodes.new("ShaderNodeValToRGB")
    cl.color_ramp.interpolation = "EASE"
    cl.color_ramp.elements[0].position, cl.color_ramp.elements[0].color = 0.5, (0, 0, 0, 1)
    cl.color_ramp.elements[1].position, cl.color_ramp.elements[1].color = 0.68, (0.55, 0.55, 0.55, 1)
    L(nz.outputs[0], cl.inputs[0])
    mc = nt.nodes.new("ShaderNodeMix")
    mc.data_type, mc.blend_type = "RGBA", "SCREEN"
    L(cl.outputs[0], mc.inputs[0])
    L(mg.outputs[2], mc.inputs[6])
    mc.inputs[7].default_value = look.hexc("#ffffff")
    L(mc.outputs[2], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def _rays_mat(name, color, alpha, reach):
    """Soft sun rays: opacity fades with distance from the object's origin (the sun)."""
    m = _overlay(name, look.hexc(color), alpha)
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    nt.links.new(tc.outputs["Object"], ln.inputs[0])
    fall = nt.nodes.new("ShaderNodeMapRange")
    fall.inputs["From Min"].default_value = reach * 0.1
    fall.inputs["From Max"].default_value = reach
    fall.inputs["To Min"].default_value = 1.0
    fall.inputs["To Max"].default_value = 0.0
    nt.links.new(ln.outputs[1], fall.inputs[0])
    mix = next(n for n in nt.nodes if n.type == "MIX_SHADER")
    nt.links.new(_mul(nt, _alpha(m), fall.outputs[0]), mix.inputs[0])
    return m


def _bird(name, size, mat, parent):
    """A tiny distant bird: two curved wings in a soft 'm', as one flat ribbon."""
    pts = []
    for i in range(9):
        t = i / 8 * 2 - 1                                       # -1 .. 1 across the wingspan
        pts.append((t * size, (abs(t) ** 0.7 - abs(t) ** 2.2) * size * 0.55 - abs(t) * size * 0.1))
    v, f = _ribbon(pts, size * 0.2, size * 0.2)
    return _mesh(name, v, f, mat, parent)


def birds_and_light(cam, f0, f1, sun=(0.7, 0.74), birds=5, hold=72, seed=21):
    """Rebirth: the white screen dissolves (f0 to f1) into a soft pastel sky with a hazy sun, slowly turning sun rays
    and a few small distant birds flapping on 2s. Earlier black / white screens on this camera are retired at f0. The
    sky stays up (birds drifting, rays turning) for `hold` frames after f1."""
    rnd = random.Random(seed)
    _retire(cam, ("black", "white"), f0)
    g = _group(cam, "sky", f0)
    r = bpy.context.scene.render
    aspect = r.resolution_x / r.resolution_y
    sky = _screen_plane(f"sky_{f0}", cam, D_SKY, _sky_mat(f"sky_m_{f0}", sun, aspect), g)
    end = f1 + hold

    # sun rays: a fan of long thin wedges from the sun, slowly turning
    W, H = view_size(cam, D_RAYS)
    sun_local = ((sun[0] - 0.5) * W, (sun[1] - 0.5) * H, -D_RAYS)
    verts, faces = [(0, 0, 0)], []
    reach = H * 1.2
    n = 14
    for i in range(n):
        a = i / n * 2 * math.pi + rnd.uniform(-0.12, 0.12)
        hw = rnd.uniform(0.035, 0.08)
        rr = reach * rnd.uniform(0.7, 1.0)
        k = len(verts)
        verts += [(math.cos(a - hw) * rr, math.sin(a - hw) * rr, 0), (math.cos(a + hw) * rr, math.sin(a + hw) * rr, 0)]
        faces.append((0, k, k + 1))
    rays = _mesh(f"rays_{f0}", verts, faces, _rays_mat(f"rays_m_{f0}", "#fff6e0", 0.26, reach), g, sun_local)
    _key(rays, "rotation_euler", f0, (0, 0, 0), "LINEAR")
    _key(rays, "rotation_euler", end, (0, 0, math.radians(8)), "LINEAR")

    # birds: small, pale-violet (distant), drifting left to right on 2s, each flapping on 2s
    W, H = view_size(cam, D_BIRDS)
    bm = look.flat(f"bird_m_{f0}", look.hexc("#6f6a92"))
    flock = []
    for i in range(birds):
        size = H * rnd.uniform(0.016, 0.028)
        b = _bird(f"bird{i}_{f0}", size, bm, g)
        u, v = rnd.uniform(0.12, 0.55), rnd.uniform(0.5, 0.82)
        du, dv = rnd.uniform(0.10, 0.18), rnd.uniform(-0.01, 0.04)
        ph = rnd.randint(0, 7)
        for f in range(f0, end + 1, 2):
            t = (f - f0) / max(1, end - f0)
            _key(b, "location", f, ((u + du * t - 0.5) * W, (v + dv * t - 0.5) * H, -D_BIRDS))
            beat = ((f - f0 + ph) // 2) % 4                        # up, level, down, level
            _key(b, "scale", f, (1, (1.0, 0.35, -0.7, 0.35)[beat], 1))
        flock.append(b)

    # the white veil that dissolves into the sky
    vg = _group(cam, "veil", f0, f1)
    vm = _overlay(f"veil_m_{f0}", (1, 1, 1, 1), 1.0)
    veil = _screen_plane(f"veil_{f0}", cam, D_VEIL, vm, vg)
    steps = max(2, (f1 - f0) // 3)
    for i in range(steps + 1):
        t = i / steps
        _key_socket(_alpha(vm), f0 + round((f1 - f0) * i / steps), 1 - t * t * (3 - 2 * t), "LINEAR")
    return {"group": g, "sky": sky, "rays": rays, "birds": flock, "veil": veil}
