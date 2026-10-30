"""Episode 1 (v2), helper 3: the new world shots (channels/monsters/EP01V2_SHOTS.md).

S09 "I woke up under a cracked sky." (2.3 s + 12-frame tail handle = 67 frames at 24 fps)
  f1-3    pure white (S08 ends on black, then white: the death)
  f4-16   the white blooms open from the middle onto a pastel sky with a hairline crack, the same zigzag as the tank crack
          (read from pistolshrimp.tank(), so it matches exactly)
  f17-24  hold on the cracked sky (pollen motes drift: LC10)
  f24-48  the camera tilts down (SG5, locked position, on 1s) past the giant mushrooms to Kai lying in pink-tinted grass
  f48-67  Kai blinks awake (acting on 3s, IM2): eyes closed, squint, open, one blink

Kai is mk/hero.py's hero.blend (world outfit), laid on his back with his arms down; faces are hero.face() keys.

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S09 OUTDIR
"""
import math
import random

import bpy
import numpy as np
from mathutils import Euler, Quaternion, Vector

from channels.monsters.mk import anim, hero, look, paintbg, pistolshrimp, world

FRAMES = 67
KAI_HEAD = (-2.0, -2.0)            # where Kai wakes: 5 m from the puddle he crawls to in S12, lying with his feet to -y
CAM = (-2.0, -2.12, 1.0)           # S09's camera: locked above his face, tilting from the sky down to it
SKY_PITCH = 50.0                   # degrees above the horizon at the start (the crack is straight ahead)
TILT = (24, 48)                    # the tilt down, eased in and out


def _key(o, path, f, value, interp="CONSTANT"):
    anim.key(o, path, f, value, interp)


def _crack_lines():
    """The tank crack's zigzag as 2D polylines: pistolshrimp.crack_path(), the same path as the lab's hero-tank crack
    (S07/S08), so all three shots show one crack. Falls back to the crack curves of pistolshrimp.tank()."""
    if hasattr(pistolshrimp, "crack_path"):
        return [pistolshrimp.crack_path()]
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
        if abs(x - KAI_HEAD[0]) < 0.4 and KAI_HEAD[1] - 1.6 < y < KAI_HEAD[1] + 0.3:
            continue                                               # not through his body
        z = float(ground(x, y))
        for _ in range(3):
            ht = rnd.uniform(0.12, 0.3)
            bb[rnd.choices((0, 1, 2), (5, 4, 1))[0]].add(
                blade, (x + rnd.uniform(-0.05, 0.05), y + rnd.uniform(-0.05, 0.05), z), (0.022, 0.022, ht),
                rot=world._rot(rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), rnd.uniform(0, 6)))
    return [o] + [b.obj(f"s09_blades{i}", mats[i]) for i, b in enumerate(bb)]


def _kai(head, ground):
    """Kai (mk/hero.py, world outfit) lying on his back in the grass, head at `head`, feet toward -y, face up, arms
    down at his sides. Returns (rig, face) with face = a point on his face for the camera to aim at."""
    z0 = float(ground(*head))
    rig = hero.load((head[0], head[1] - 1.465, z0 + 0.18), scale=1.1, outfit="world", line=0.002)
    arm = rig["arm"]
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (math.radians(-90), 0, 0)             # on his back (the rest pose stands facing -y)
    for name, side in (("left_upper_arm", -1), ("right_upper_arm", 1)):
        b = rig["bone"](name)
        b.rotation_mode = "XYZ"
        b.rotation_euler = (0, 0, math.radians(side * 72))     # arms down from the T-pose
    bpy.context.view_layer.update()
    hb = rig["bone"]("head")
    face = arm.matrix_world @ hb.head + Vector((0, 0.09, 0.12))
    return rig, face


def _clear_under_kai(objs):
    """Delete the world's meadow blades and flowers inside his body's footprint (they poke up through his chest)."""
    import bmesh
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        gone = [v for v in bm.verts
                if abs(v.co.x - KAI_HEAD[0]) < 0.45 and KAI_HEAD[1] - 1.6 < v.co.y < KAI_HEAD[1] + 0.35]
        bmesh.ops.delete(bm, geom=gone, context="VERTS")
        bm.to_mesh(o.data)
        bm.free()


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
    _clear_under_kai(h["flowers"])
    rig, face = _kai(KAI_HEAD, h["ground"])
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
    for f, name in ((1, "blink"), (51, "squint"), (54, "neutral"), (60, "blink"), (63, "neutral")):
        hero.face(rig, name, f)                                    # waking: closed, squint, open, one blink (on 3s)
    return dict(frames=FRAMES, step=1, subject=[rig["arm"]])


SHOTS = {"S09": s09}
