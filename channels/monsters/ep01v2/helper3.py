"""Episode 1 (v2), helper 3: the new world shots (channels/monsters/EP01V2_SHOTS.md).

S09 "I woke up under a cracked sky." (2.3 s + 12-frame tail handle = 67 frames at 24 fps)
  f1-3    pure white (S08 ends on black, then white: the death)
  f4-16   the white blooms open from the middle onto a pastel sky with a hairline crack, the same zigzag as the tank crack
          (read from pistolshrimp.tank(), so it matches exactly)
  f17-24  hold on the cracked sky (pollen motes drift: LC10)
  f24-48  the camera tilts down (SG5, locked position, on 1s) past the giant mushrooms to Kai lying in pink-tinted grass
  f48-67  Kai blinks awake (acting on 3s, IM2): eyes closed, half open, open, one blink

Kai is a stand-in (toon primitives in his colours, world outfit: sage tunic, navy trousers, orange shoes) until the
coordinator's no-add-on hero.blend lands; _kai() is the only thing that changes then.

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S09 OUTDIR
"""
import math
import random

import bpy
import numpy as np
from mathutils import Euler, Quaternion, Vector

from channels.monsters.mk import anim, look, paintbg, pistolshrimp, world

FRAMES = 67
KAI_HEAD = (-2.0, -2.0)            # where Kai wakes: 5 m from the puddle he crawls to in S12, lying with his feet to -y
CAM = (-2.0, -2.41, 0.84)          # S09's camera: locked just above his chest, tilting from the sky down to his face
SKY_PITCH = 50.0                   # degrees above the horizon at the start (the crack is straight ahead)
TILT = (24, 48)                    # the tilt down, eased in and out


def _key(o, path, f, value, interp="CONSTANT"):
    anim.key(o, path, f, value, interp)


def _crack_lines():
    """The tank crack's zigzag (main line, branches, starburst) as 2D polylines, read from helper 2's tank so the sky
    crack is the same shape. Uses pistolshrimp.crack_path() when helper 2 exposes it."""
    if hasattr(pistolshrimp, "crack_path"):
        return [[(p[0], p[-1]) for p in line] for line in pistolshrimp.crack_path()]
    before = set(bpy.data.objects)
    t = pistolshrimp.tank()
    lines = []
    for o in t["crack"]:
        if "crack_lite" in o.name:
            lines.append([(p.co.x, p.co.z) for p in o.data.splines[0].points])
    for o in set(bpy.data.objects) - before:
        bpy.data.objects.remove(o)
    return lines


def _ribbon(lines, width, scale, origin):
    """Flat ribbons along 2D polylines (x right, y up), centred on `origin`, in metres."""
    verts, faces = [], []
    for line in lines:
        pts = (np.array(line, float) - origin) * scale
        for a, b in zip(pts[:-1], pts[1:]):
            d = b - a
            n = np.array((-d[1], d[0])) / max(np.linalg.norm(d), 1e-9) * width / 2
            i = len(verts)
            ext = d / max(np.linalg.norm(d), 1e-9) * width / 2       # overlap the joints
            verts += [(*(a - n - ext), 0), (*(b - n + ext), 0), (*(b + n + ext), 0), (*(a + n - ext), 0)]
            faces.append((i, i + 1, i + 2, i + 3))
    return np.array(verts), faces


def _sky_crack(cam_loc, look_q):
    """The hairline crack hung far away in the sky, facing the camera: a white core ~2 px wide at 720x1280 with a soft
    stepped glow, on a plane 900 m off along the camera's opening direction."""
    lines = _crack_lines()
    allp = np.vstack([np.array(ln) for ln in lines])
    lo, hi = allp.min(axis=0), allp.max(axis=0)
    origin = (lo + hi) / 2
    scale = 400.0 / (hi[1] - lo[1])                  # ~40% of the frame height at 900 m with a 35 mm lens
    root = bpy.data.objects.new("s09_crack", None)
    bpy.context.scene.collection.objects.link(root)
    fwd = look_q @ Vector((0, 0, -1))
    root.location = Vector(cam_loc) + fwd * 900
    root.rotation_euler = look_q.to_euler()
    layers = [(1.3, look.flat("s09_crack_core", look.hexc("#ffffff"), 1.6))]
    for k, (w, a) in enumerate(((4.0, 0.42), (9.0, 0.22), (17.0, 0.1))):
        layers.append((w, look.fade(f"s09_crack_glow{k}", look.hexc("#fff4fb"), a)))
    for k, (w, m) in enumerate(layers):
        v, f = _ribbon(lines, w, scale, origin)
        o = world._obj(f"s09_crack{k}", v + (0, 0, 0.05 * k * -1), f, m, smooth=False, shadow=False)
        o.parent = root
    return root


def _bloom(cam):
    """White over the whole frame that blooms open from the middle (f4-16): a plane on the camera whose alpha is a
    radial ramp with a keyed opening radius."""
    m = bpy.data.materials.new("s09_bloom")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sq = nt.nodes.new("ShaderNodeMapping")
    sq.inputs["Scale"].default_value = (2.016, 3.577, 1.0)      # 1 = the frame's side edge, round in pixels
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    edge = nt.nodes.new("ShaderNodeMath")
    edge.name = "open"
    edge.operation = "SUBTRACT"                                # r - opening radius
    soft = nt.nodes.new("ShaderNodeMapRange")
    soft.inputs["From Min"].default_value, soft.inputs["From Max"].default_value = -0.05, 0.45
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = look.hexc("#fffafd")
    L(tc.outputs["Object"], sq.inputs[0])
    L(sq.outputs[0], ln.inputs[0])
    L(ln.outputs["Value"], edge.inputs[0])
    L(edge.outputs[0], soft.inputs[0])
    L(soft.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "BLENDED"
    v = np.array([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], float)
    o = world._obj("s09_bloom", v, [(0, 1, 2, 3)], m, smooth=False, shadow=False)
    o.parent = cam
    o.location = (0, 0, -0.12)                       # just past the near clip, filling the frame
    o.scale = (0.07, 0.07 / 0.5625, 1)
    r = edge.inputs[1]
    for f, val in ((1, -0.6), (3, -0.6), (16, 2.6)):
        r.default_value = val
        r.keyframe_insert("default_value", frame=f)
    for fc in anim.all_fcurves(nt.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "SINE"
            kp.easing = "EASE_OUT"
    return o


def _pink_patch(ground, centre, radius=2.8, seed=9):
    """Pink-tinted grass where Kai wakes: a patch of painted pink strokes laid on the terrain with a ragged, dithered
    edge, and clumps of pink blades."""
    m = world.grass("s09_pink_grass", ("#c9628f", "#ec93ba", "#ffc8df")).copy()
    m.name = "s09_pink_patch"
    nt = m.node_tree
    L = nt.links.new
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    shader = out.inputs[0].links[0].from_socket
    tc = nt.nodes.new("ShaderNodeTexCoord")
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.6
    add = nt.nodes.new("ShaderNodeMath")
    add.operation, add.inputs[2].default_value = "MULTIPLY_ADD", 0.0
    add.inputs[1].default_value = 0.9
    edge = nt.nodes.new("ShaderNodeMapRange")
    edge.inputs["From Min"].default_value, edge.inputs["From Max"].default_value = radius * 0.62, radius * 0.95
    edge.inputs["To Min"].default_value, edge.inputs["To Max"].default_value = 1.0, 0.0
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = "ADD"
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    L(tc.outputs["Object"], ln.inputs[0])
    L(tc.outputs["Object"], nz.inputs[0])
    L(nz.outputs["Fac"], add.inputs[0])                        # ragged edge: radius pushed in and out by noise
    L(ln.outputs["Value"], sub.inputs[0])
    L(add.outputs[0], sub.inputs[1])
    L(sub.outputs[0], edge.inputs[0])
    L(edge.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(shader, mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "DITHERED"
    n = 48
    u = np.linspace(-radius, radius, n)
    X, Y = np.meshgrid(u, u)
    Z = ground(X + centre[0], Y + centre[1]) + 0.012
    verts = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    i, j = np.meshgrid(np.arange(n - 1), np.arange(n - 1), indexing="ij")
    k = (i * n + j).ravel()
    o = world._obj("s09_pink_patch", verts, np.column_stack([k, k + 1, k + n + 1, k + n]), m, shadow=False)
    o.location = (centre[0], centre[1], 0)
    rnd = random.Random(seed)
    mats = [world._p3(f"s09_blade{i}", *c) for i, c in
            enumerate((("#b04f7c", "#e283ad", "#ffbfd9"), ("#c76a96", "#f2a0c4", "#ffd6e8"),
                       ("#8a9a4a", "#b8c86a", "#e2ef9a")))]
    bb = [world._Batch() for _ in mats]
    blade = world._lathe([(0, 1.0), (1.0, 0.0), (0, -0.05)], 4)
    for _ in range(520):
        a, d = rnd.uniform(0, 2 * math.pi), radius * 0.9 * math.sqrt(rnd.random())
        x, y = centre[0] + d * math.cos(a), centre[1] + d * math.sin(a)
        if abs(x - KAI_HEAD[0]) < 0.32 and KAI_HEAD[1] - 1.75 < y < KAI_HEAD[1] + 0.2:
            continue                                               # not through his body
        z = float(ground(x, y))
        for _ in range(3):
            ht = rnd.uniform(0.12, 0.3)
            bb[rnd.choices((0, 1, 2), (5, 4, 1))[0]].add(
                blade, (x + rnd.uniform(-0.05, 0.05), y + rnd.uniform(-0.05, 0.05), z), (0.022, 0.022, ht),
                rot=world._rot(rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), rnd.uniform(0, 6)))
    return [o] + [b.obj(f"s09_blades{i}", mats[i]) for i, b in enumerate(bb)]


def _part(name, loc, scale, mat, parent, line=0.007, seg=20, rot=(0, 0, 0)):
    b = world._Batch()
    b.add(world._sphere(seg, max(8, seg // 2)), (0, 0, 0), scale)
    o = b.obj(name, mat)
    o.location, o.rotation_euler = loc, rot
    o.parent = parent
    return look.outline(o, line) if line else o


def _capsule(name, a, b, r, mat, parent, line=0.007):
    a, b = Vector(a), Vector(b)
    d = b - a
    ring = []
    for t in np.linspace(0, math.pi / 2, 5):                   # top cap, cylinder, bottom cap (unit length along z)
        ring.append((r * math.sin(t), d.length + r * math.cos(t)))
    for t in np.linspace(math.pi / 2, math.pi, 5):
        ring.append((r * math.sin(t), r * math.cos(t)))
    ring[0] = (0.0, ring[0][1])
    ring[-1] = (0.0, ring[-1][1])
    v, f = world._lathe(ring, 16)
    o = world._obj(name, v, f, mat)
    o.location = a
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    o.parent = parent
    return look.outline(o, line)


def _kai(head):
    """Stand-in Kai lying on his back in the grass, feet toward -y, face up, eyes closed. Returns (root, eyes) where
    eyes = dict(open=[objs], closed=[objs]) for the blink keys. Proportions: ~1.72 m, anime-teen (about 6 heads)."""
    hx = look.hexc
    skin = look.toon("kai_skin", hx("#ffd9bf"))
    hair = look.toon("kai_hair", hx("#4a3328"))
    tunic = look.toon("kai_tunic", hx("#7fae8a"))
    shirt = look.toon("kai_shirt", hx("#f4f4f0"))
    pants = look.toon("kai_pants", hx("#2e3550"))
    shoe = look.toon("kai_shoe", hx("#ffb340"))
    iris = look.toon("kai_iris", hx("#b5652b"))
    dark = look.flat("kai_dark", hx("#2a1a14"))
    white = look.flat("kai_white", hx("#ffffff"))
    blush = look.flat("kai_blush", hx("#ff9f9a"))
    root = bpy.data.objects.new("kai_standin", None)
    bpy.context.scene.collection.objects.link(root)
    root.location = (head[0], head[1], 0.0)
    P = root
    _part("kai_head", (0, 0, 0.14), (0.105, 0.115, 0.118), skin, P, line=0.006)
    _part("kai_hair_cap", (0, 0.035, 0.105), (0.118, 0.125, 0.112), hair, P, line=0.006)
    clump = world._lathe([(0, 1.0), (0.45, 0.72), (0.85, 0.38), (1.0, 0.14), (0.7, 0.0), (0, -0.02)], 12)
    c = Vector((0, 0, 0.14))
    tufts = [((x, 1.0, z), 0.1, 0.085, 0.042) for x, z in ((-0.75, 0.1), (-0.35, 0.35), (0.0, 0.3), (0.38, 0.32),
                                                             (0.72, 0.05), (-0.5, -0.25), (0.5, -0.2))]
    tufts += [((s * 1.0, 0.45, 0.2), 0.105, 0.065, 0.036) for s in (-1, 1)]               # side tufts over the ears
    tufts += [((0.12, 1.0, 0.75), 0.11, 0.12, 0.034)]                                     # the tall front cowlick
    for k, (d, base, length, w) in enumerate(tufts):
        d = Vector(d).normalized()
        b = world._Batch()
        b.add(clump, (0, 0, 0), (w, w * 0.6, length), rot=world._align(d))
        o = b.obj(f"kai_tuft{k}", hair)
        o.location, o.parent = c + d * base * 0.85, P
        look.outline(o, 0.005)
    for k, x in enumerate((-0.055, 0.0, 0.05)):                                          # bangs over the forehead
        d = Vector((x * 4, -1.0, 0.25)).normalized()
        b = world._Batch()
        b.add(clump, (0, 0, 0), (0.032, 0.016, 0.07), rot=world._align(d))
        o = b.obj(f"kai_bang{k}", hair)
        o.location, o.parent = (x, 0.085, 0.228), P
        look.outline(o, 0.004)
    eyes = dict(open=[], closed=[])
    lite = look.flat("kai_iris_lite", hx("#e9a25a"))
    for s in (-1, 1):
        x = s * 0.043
        eyes["open"] += [_part(f"kai_eye{s}", (x, -0.004, 0.252), (0.027, 0.04, 0.008), dark, P, line=0),
                         _part(f"kai_iris{s}", (x, -0.012, 0.256), (0.021, 0.027, 0.006), iris, P, line=0),
                         _part(f"kai_lite{s}", (x, -0.027, 0.2595), (0.014, 0.007, 0.003), lite, P, line=0),
                         _part(f"kai_hl{s}", (x + 0.009, 0.012, 0.2615), (0.008, 0.008, 0.003), white, P, line=0),
                         _part(f"kai_hl2{s}", (x - 0.008, -0.02, 0.2615), (0.0045, 0.0045, 0.003), white, P, line=0)]
        for t in (-1, 1):                                                                 # a soft curve: two strokes
            eyes["closed"].append(_part(f"kai_lid{s}{t}", (x + t * 0.012, -0.012, 0.252), (0.015, 0.0045, 0.006),
                                        dark, P, line=0, rot=(0, 0, -t * 0.32)))
        _part(f"kai_brow{s}", (x, 0.055, 0.247), (0.024, 0.006, 0.006), hair, P, line=0, rot=(0, 0, -s * 0.15))
        _part(f"kai_blush{s}", (s * 0.07, -0.035, 0.235), (0.016, 0.008, 0.004), blush, P, line=0)
    _part("kai_mouth", (0, -0.075, 0.243), (0.014, 0.004, 0.004), dark, P, line=0)
    _part("kai_ear_l", (-0.104, -0.005, 0.14), (0.018, 0.03, 0.022), skin, P, line=0.008)
    _part("kai_ear_r", (0.104, -0.005, 0.14), (0.018, 0.03, 0.022), skin, P, line=0.008)
    _capsule("kai_neck", (0, -0.1, 0.12), (0, -0.16, 0.12), 0.042, skin, P)
    _part("kai_shirt", (0, -0.2, 0.13), (0.07, 0.05, 0.05), shirt, P)
    _part("kai_torso", (0, -0.42, 0.11), (0.185, 0.27, 0.1), tunic, P)
    _part("kai_hips", (0, -0.68, 0.1), (0.16, 0.1, 0.09), pants, P)
    for s in (-1, 1):
        _capsule(f"kai_arm{s}", (s * 0.2, -0.22, 0.11), (s * 0.27, -0.5, 0.08), 0.05, tunic, P)
        _capsule(f"kai_forearm{s}", (s * 0.27, -0.5, 0.08), (s * 0.29, -0.74, 0.06), 0.042, tunic, P)
        _part(f"kai_hand{s}", (s * 0.295, -0.8, 0.06), (0.035, 0.05, 0.022), skin, P)
        _capsule(f"kai_thigh{s}", (s * 0.085, -0.7, 0.1), (s * 0.1, -1.12, 0.08), 0.072, pants, P)
        _capsule(f"kai_shin{s}", (s * 0.1, -1.12, 0.08), (s * 0.115, -1.52, 0.07), 0.058, pants, P)
        _part(f"kai_shoe{s}", (s * 0.12, -1.6, 0.11), (0.06, 0.1, 0.07), shoe, P, rot=(math.radians(-25), 0, 0))
    return root, eyes


def _blinks(eyes, keys):
    """keys: [(frame, openness)] with openness 0 (closed), 0.45 (half), 1 (open); CONSTANT keys (drawn on 3s). The
    open eye squashes vertically to half; closed shows the lid line instead."""
    for f, k in keys:
        for o in eyes["open"]:
            _key(o, "scale", f, (1.0, k, 1.0) if k else (0.0, 0.0, 0.0))
        for o in eyes["closed"]:
            _key(o, "scale", f, (1.0, 1.0, 1.0) if k == 0 else (0.0, 0.0, 0.0))


def _motes(centre, n=16, seed=4):
    """Pollen motes drifting up through the light (LC10); with the shallow focus they bloom into soft dots."""
    rnd = random.Random(seed)
    mats = [look.flat("s09_mote_w", look.hexc("#fffbe8"), 1.3), look.flat("s09_mote_p", look.hexc("#ffd6ea"), 1.3)]
    ball = world._sphere(8, 5)
    out = []
    while len(out) < n:
        p0 = Vector((centre[0] + rnd.uniform(-0.4, 0.4), centre[1] + rnd.uniform(-0.25, 0.4), rnd.uniform(0.12, 0.42)))
        if (p0 - Vector(CAM)).length < 0.5:
            continue                                                  # never a blur ball right on the lens
        b = world._Batch()
        r = rnd.uniform(0.004, 0.008)
        b.add(ball, (0, 0, 0), (r, r, r))
        o = b.obj(f"s09_mote{len(out)}", rnd.choice(mats), shadow=False)
        drift = Vector((rnd.uniform(-0.06, 0.06), rnd.uniform(-0.05, 0.05), rnd.uniform(0.05, 0.12)))
        _key(o, "location", 1, p0, "LINEAR")
        _key(o, "location", FRAMES, p0 + drift, "LINEAR")
        out.append(o)
    return out


def s09():
    sc = bpy.context.scene
    paintbg.sky(top="#4f9fe6", mid="#86c3f0", horizon="#e2f1ff")    # pastel: softer than the deep-blue default
    look.sun(elev=48, azim=-40)
    h = world.build(seed=7)
    for o in h["sparkles"] + h["clouds"] + h["deck"]:
        o.hide_render = True        # the pond is behind the camera; the cloud deck overhead would bury the crack
    _pink_patch(h["ground"], (KAI_HEAD[0], KAI_HEAD[1] - 0.8))
    root, eyes = _kai(KAI_HEAD)
    root.location.z = float(h["ground"](*KAI_HEAD)) + 0.03
    face = Vector((KAI_HEAD[0], KAI_HEAD[1] - 0.02, root.location.z + 0.26))
    aim = face + Vector((0, -0.07, -0.02))                         # his face just above the middle, chest below

    cam = bpy.data.objects.new("s09_cam", bpy.data.cameras.new("s09_cam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd = cam.data
    cd.lens = 35
    cd.clip_start, cd.clip_end = 0.1, 5000.0
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = 0.6                                   # f/0.15 blurs his own chest this close
    cam.location = CAM
    up = Quaternion(Euler((math.radians(90 + SKY_PITCH), 0, 0)))      # looking along +y, up into the sky
    down = (aim - Vector(CAM)).to_track_quat("-Z", "Y")
    for f, q in ((1, up), (TILT[0], up), (TILT[1], down)):
        cam.rotation_euler = q.to_euler("XYZ", cam.rotation_euler)
        cam.keyframe_insert("rotation_euler", frame=f)
    for f, focus in ((1, 1000.0), (TILT[0], 1000.0), (38, 25.0), (TILT[1] - 2, (face - Vector(CAM)).length)):
        cd.dof.focus_distance = focus                              # sky, then the meadow, then his face
        cd.keyframe_insert("dof.focus_distance", frame=f)
    _sky_crack(CAM, up)
    _bloom(cam)
    _motes(KAI_HEAD)
    _blinks(eyes, [(1, 0), (51, 0.45), (54, 1), (60, 0), (63, 1)])
    return dict(frames=FRAMES, step=1, subject=[root])


SHOTS = {"S09": s09}
