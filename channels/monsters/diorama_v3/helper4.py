"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 4:

    S08b "That's how I died."  The dollhouse lab at night. Kai stands up out of his chair in the spill (S08a ends on
         his feet in the water and his face dropping). A spark cracks at the power strip, and a blue spark runs
         through the water to his feet (on 1s), the arcs crawling over the puddle behind it. It hits: he jolts rigid
         (arms flung out, head back), arcs crawl over his body, and his skeleton flashes through in x-ray (a 3D
         placeholder until the Q5 2D x-ray lands: a blue ghost of his body with a white skeleton inside, on the
         x-ray frames only). Then every lab light dies, the last arcs fade, and the frame goes black (the flatline
         beep is in the sound). A slow push-in on 1s; Kai's acting on 2s, the jolt's shake and every effect on 1s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08b OUT [--frames A-B] [--still N --scale 0.5]

63 render frames (51 in the cut + 12), from ep01v3/timing.json; the beat frames are in _beats().
"""
import json
import math
import os
import random

try:
    import bpy
    from mathutils import Matrix, Quaternion, Vector

    from channels.monsters.mk import anim, diorama, diorama_lab, hero, look, storm
except ImportError:                                      # helper4_comp.py imports _beats/BUILD outside Blender
    bpy = None

KAI = 5.8                                       # hero.load scale in diorama units (diorama/helper1.KAI)
FX3D = os.environ.get("S08B_FX3D") == "1"       # the old 3D arcs and x-ray placeholder; default: the 2D pass (Q5)
BUILD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                     "build", "monsters", "diorama_v3")
FALLBACK_FRAMES = 63                            # ep01v3 S08b render_frames (51 + 12), if timing.json is missing
ARC_GLOW, ARC_CORE, GHOST = "#5fb6ff", "#f2f9ff", "#3d8cff"


def _frames():
    try:
        from channels.monsters.diorama_v3.shots import v3_frames
        return v3_frames("S08b")
    except (FileNotFoundError, KeyError):
        print("S08b: ep01v3/timing.json not there yet; using", FALLBACK_FRAMES, "frames", flush=True)
        return FALLBACK_FRAMES


def _beats(n):
    """The beat frames, on the v3 line (timing.json: "That's" 8, "how" 13, "I" 15, "died." 18, the line out by 26):
    the spark cracks at the strip on 4 and runs to his feet by 10; it hits on 11; the x-ray flashes 14-15, 18-19 (on
    "died.") and 22-23 (fx2d.xray_flash start 14, beat 2); the lights die on 27, the last arcs by 30, and it is black from 31 to the end (the flatline)."""
    return dict(spark=4, run=(4, 10), hit=11, xray=[14, 15, 18, 19, 22, 23], out=27, fade=30, black=31, land=29)


# ----------------------------------------------------------------------------------------------- Kai, standing
def _aim(rig, name, direction, twist=0.0):
    """Point a bone along `direction` in the character's frame (x = his left, y = his back, z = up)."""
    pb = rig["bone"](name)
    bpy.context.view_layer.update()
    m = pb.matrix.copy()
    cur = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    rot = cur.rotation_difference(Vector(direction).normalized()).to_matrix() @ m.to_3x3()
    if twist:
        rot = Matrix.Rotation(twist, 3, rot @ Vector((0, 1, 0))) @ rot
    pb.matrix = Matrix.Translation(m.translation) @ rot.to_4x4()
    bpy.context.view_layer.update()


BODY = ("spine", "chest", "neck", "head", "left_upper_leg", "right_upper_leg", "left_lower_leg", "right_lower_leg",
        "left_foot", "right_foot", "left_upper_arm", "right_upper_arm", "left_lower_arm", "right_lower_arm",
        "left_hand", "right_hand")


def _key(rig, f, interp="CONSTANT"):
    for n in BODY + SHOULDER_BONES:
        rig["bone"](n).keyframe_insert("rotation_quaternion", frame=f)
    for fc in anim.all_fcurves(rig["arm"].animation_data.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - f) < 0.01:
                kp.interpolation = interp


def _fingers(rig, curl):
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.rotation_mode = "QUATERNION"
            b.rotation_quaternion = Matrix.Rotation(curl * (0.4 if b.name.startswith("thumb") else 1.0), 4,
                                                    "X").to_quaternion()


def _reset(rig):
    for n in BODY:
        pb = rig["bone"](n)
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
    bpy.context.view_layer.update()


def _fear(rig, sway=0.0):
    """Standing in the water, hunched and frozen: knees a little bent, shoulders up, hands lifted off his sides,
    head down to the water at his feet (S08a's last pose)."""
    _reset(rig)
    for s, sx in (("left", 1.0), ("right", -1.0)):
        _aim(rig, f"{s}_upper_leg", (sx * 0.09, -0.12, -1.0))
        _aim(rig, f"{s}_lower_leg", (sx * 0.05, 0.14, -1.0))
        _aim(rig, f"{s}_foot", (sx * 0.1, -1.0, -0.35))
    _aim(rig, "spine", (sway, -0.08, 1.0))
    _aim(rig, "chest", (sway, -0.16, 1.0))
    _aim(rig, "neck", (0.0, -0.04, 1.0))
    _aim(rig, "head", (0.0, -0.08, 1.0))                                 # level: from above his face reads; the
                                                                         # eyes (look_down) carry the look at the water
    for s, sx in (("left", 1.0), ("right", -1.0)):
        _aim(rig, f"{s}_upper_arm", (sx * 0.42, -0.12, -1.0))
        _aim(rig, f"{s}_lower_arm", (sx * 0.25, -0.75, -0.7))
        _aim(rig, f"{s}_hand", (sx * 0.2, -0.8, -0.5))


def _zap(rig, k=0.0):
    """Electrocuted (the coordinator's notes): rigid and arched, head thrown back, elbows bent with the hands clawed up
    by his head, the left leg locked and the right knee buckling, the two sides a little different. `k` (-1..1)
    shifts it a touch so the 1s shake reads."""
    _reset(rig)
    _shoulders_set(rig, 0.5 + 0.06 * k)                                   # shoulders jammed up
    _aim(rig, "left_upper_leg", (0.17 + 0.02 * k, 0.06, -1.0))           # locked straight
    _aim(rig, "left_lower_leg", (0.17, 0.03, -1.0))
    _aim(rig, "left_foot", (0.15, -1.0, -0.6))
    _aim(rig, "right_upper_leg", (-0.14, -0.42, -1.0))                   # the right knee buckles forward...
    _aim(rig, "right_lower_leg", (-0.06, 0.45, -1.0))                    # ...the shin back
    _aim(rig, "right_foot", (-0.1, -1.0, -0.3))
    _aim(rig, "spine", (0.05 * k, 0.22, 1.0))                             # back arched
    _aim(rig, "chest", (0.06 - 0.04 * k, 0.4, 1.0))
    _aim(rig, "neck", (0.0, 0.32, 1.0))
    _aim(rig, "head", (0.12 + 0.06 * k, 0.75, 1.0))                      # thrown back, tipped to his left
    _aim(rig, "left_upper_arm", (0.92, 0.18, 0.42 + 0.06 * k))           # elbows out, the upper arms up...
    _aim(rig, "left_lower_arm", (0.22, -0.2, 1.0))                       # ...forearms up: the hands by his head
    _aim(rig, "left_hand", (0.3, 0.35, 1.0))                             # wrists cocked back, a claw
    _aim(rig, "right_upper_arm", (-0.86, 0.06, 0.22 - 0.05 * k))         # the right arm lower and wider
    _aim(rig, "right_lower_arm", (-0.45, -0.3, 0.85))
    _aim(rig, "right_hand", (-0.4, 0.25, 0.9))


def _limp(rig):
    """The current stops: everything lets go. Head lolls forward, arms drop, both knees fold."""
    _reset(rig)
    _shoulders_set(rig, 0.0)
    for s, sx in (("left", 1.0), ("right", -1.0)):
        _aim(rig, f"{s}_upper_leg", (sx * 0.12, -0.75, -1.0))
        _aim(rig, f"{s}_lower_leg", (sx * 0.05, 0.85, -1.0))
        _aim(rig, f"{s}_foot", (sx * 0.1, -1.0, -0.2))
        _aim(rig, f"{s}_upper_arm", (sx * 0.3, 0.2, -1.0))
        _aim(rig, f"{s}_lower_arm", (sx * 0.2, 0.1, -1.0))
        _aim(rig, f"{s}_hand", (sx * 0.2, 0.0, -1.0))
    _aim(rig, "spine", (0.0, -0.1, 1.0))
    _aim(rig, "chest", (0.03, -0.2, 1.0))
    _aim(rig, "neck", (0.0, -0.35, 1.0))
    _aim(rig, "head", (0.15, -0.6, 1.0))


def _down(rig):
    """Landed on his back (in his own frame; the rig object is tipped back): the left leg out straight, the right knee
    up, the left arm flung over his head, the right arm out to the side, the head rolled to one side."""
    _reset(rig)
    _shoulders_set(rig, 0.0)
    _aim(rig, "left_upper_leg", (0.15, 0.05, -1.0))
    _aim(rig, "left_lower_leg", (0.17, 0.05, -1.0))
    _aim(rig, "left_foot", (0.25, -0.6, -1.0))
    _aim(rig, "right_upper_leg", (-0.2, -0.9, -0.55))                    # the knee up
    _aim(rig, "right_lower_leg", (-0.1, 0.5, -1.0))
    _aim(rig, "right_foot", (-0.1, -1.0, -0.2))
    _aim(rig, "spine", (0.0, 0.05, 1.0))
    _aim(rig, "chest", (0.0, 0.08, 1.0))
    _aim(rig, "neck", (0.1, 0.0, 1.0))
    _aim(rig, "head", (0.55, -0.15, 1.0), twist=0.5)                     # rolled toward his left shoulder
    _aim(rig, "left_upper_arm", (0.55, 0.2, 0.85))                       # flung over his head
    _aim(rig, "left_lower_arm", (0.2, 0.35, 1.0))
    _aim(rig, "left_hand", (0.1, 0.3, 1.0))
    _aim(rig, "right_upper_arm", (-1.0, 0.25, -0.25))                    # out to the side
    _aim(rig, "right_lower_arm", (-1.0, 0.2, 0.15))
    _aim(rig, "right_hand", (-1.0, 0.15, 0.1))


SHOULDER_BONES = ("left_shoulder", "right_shoulder")


def _shoulders_set(rig, up):
    """Raise both shoulders by `up` (0 = rest); _key() keys them with the body."""
    for nm, sx in zip(SHOULDER_BONES, (1.0, -1.0)):
        pb = rig["bone"](nm)
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        if up:
            _aim(rig, nm, (sx * 1.0, 0.05, up))


def _fingers_key(rig, curl, f):
    _fingers(rig, curl)
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.keyframe_insert("rotation_quaternion", frame=f)
    _constant(rig["arm"], f)


def _constant(obj, f):
    for fc in anim.all_fcurves(obj.animation_data.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - f) < 0.01:
                kp.interpolation = "CONSTANT"


def _act(rig, B):
    """Kai's acting for S08b, on the v3 line (see _beats):
      1-10   FEAR_STAND (helper 1's S08a end pose, so the cut is seamless), trembling on 2s
      11-14  the hit: an overshoot (acting.ease "overshoot") from fear into the electrocution pose, on 1s
      15-23  held rigid, shaking on 1s
      24     the current stops: he goes limp, the knees fold
      26-28  he tips back and to his right, onto the open floor (the lights die on 27)
      29     he lands on his back (the body-fall thud); 30 settles; black from 31."""
    from channels.monsters.diorama_v3.helper1 import FEAR_FACE, fear_stand
    from channels.monsters.mk.acting import ease
    arm = rig["arm"]
    hit, out = B["hit"], B["out"]
    for f, sway in ((1, 0.0), (3, 0.03), (5, -0.03), (7, 0.03), (9, -0.02)):
        fear_stand(rig, f, sway)
        _fingers_key(rig, -0.12, f)
    base = arm["stand_z"]
    fear_stand(rig, None, -0.02)
    qa = _quats(rig)
    _reset(rig)
    _shoulders_set(rig, 0.0)
    arm.location.z = base
    bpy.context.view_layer.update()
    ank0 = min((arm.matrix_world @ rig["bone"](f"{s}_foot").head).z for s in ("left", "right"))

    yaw = arm.rotation_euler.z
    d = Matrix.Rotation(yaw, 3, "Z") @ Vector((-0.85, 0.5, 0.0)).normalized()   # back and to his right, in the world
    tip_axis = Vector((0, 0, 1)).cross(d).normalized()

    def plant(f, rot=0.0, lie=False):
        q = _quats(rig)                          # the pose just set; flush the pending re-evaluation of the last keys
        bpy.context.view_layer.update()          # (it would put the keyed pose back), then set it again
        for nm, v in q.items():
            rig["bone"](nm).rotation_quaternion = v
        arm.rotation_euler = (Matrix.Rotation(-rot, 3, tip_axis) @ Matrix.Rotation(yaw, 3, "Z")).to_euler("XYZ")
        arm.location.z = base
        bpy.context.view_layer.update()
        if lie:                                                           # his back on the floor
            low = min((arm.matrix_world @ rig["bone"](nm).head).z for nm in ("hips", "spine", "chest", "neck"))
            arm.location.z = base + KAI * 0.09 - low
        else:                                                             # the lower sole on the floor
            low = min((arm.matrix_world @ rig["bone"](f"{s}_foot").head).z for s in ("left", "right"))
            arm.location.z = base + ank0 - low
        bpy.context.view_layer.update()
        arm.keyframe_insert("location", frame=f)
        arm.keyframe_insert("rotation_euler", frame=f)
        _key(rig, f)
        _constant(arm, f)

    _zap(rig, 0.0)
    qb = _quats(rig)
    for f in range(hit, hit + 4):                                         # the overshoot into the jolt
        _between(rig, qa, qb, ease((f - hit + 1) / 4, "overshoot", 0.15))
        plant(f)
    _fingers_key(rig, 0.75, hit)                                          # the hands claw
    rnd = random.Random(8)
    for f in range(hit + 4, out - 3):                                     # rigid, shaking on 1s
        _zap(rig, rnd.uniform(-1, 1))
        plant(f)
    f_limp = out - 3
    _limp(rig)
    qc = _quats(rig)
    plant(f_limp)
    _fingers_key(rig, 0.3, f_limp)
    plant(f_limp + 1)
    _down(rig)
    qd = _quats(rig)
    for f, e, rot in ((f_limp + 2, 0.25, -0.45), (f_limp + 3, 0.5, -0.95), (f_limp + 4, 0.8, -1.3)):
        _between(rig, qc, qd, e)                                          # tipping back, unfolding as he falls
        plant(f, rot)
    _down(rig)
    plant(f_limp + 5, -1.52, lie=True)                                    # lands (the thud)
    plant(f_limp + 6, -1.47, lie=True)                                    # a small bounce, settled
    _face(rig, dict(FEAR_FACE, look_down=0.15), 1)
    _face(rig, {"face_surprise": 1.0, "eye_black_small": 1.0, "mouse_open": 1.0, "lip_a": 0.8,
                "shock_plane": 1.0}, hit)
    _face(rig, {"eye_close": 1.0, "mouse_open": 0.35, "eye_brow_down": 0.3}, f_limp)


def _quats(rig):
    return {n: rig["bone"](n).rotation_quaternion.copy() for n in BODY + SHOULDER_BONES}


def _between(rig, qa, qb, e):
    """Set the pose `e` of the way from qa to qb (e may leave 0..1: the overshoot), bone by bone."""
    bpy.context.view_layer.update()              # flush the pending re-evaluation of the keys just inserted first,
    for n in qa:                                 # or it would overwrite the pose set here
        a, b = qa[n], qb[n]
        d = a.inverted() @ b                                              # a @ d == b
        if d.w < 0:                                                       # the short way round
            d.negate()
        axis, ang = d.to_axis_angle()
        pb = rig["bone"](n)
        pb.rotation_quaternion = a @ Quaternion(axis, ang * e) if ang > 1e-6 else a
    bpy.context.view_layer.update()


def _face(rig, keys, f):
    kb = bpy.data.objects["head"].data.shape_keys.key_blocks
    touched = set(keys)
    for rv in hero.FACES.values():
        touched.update(rv.keys())
    for k in touched:
        if k in kb:
            kb[k].value = keys.get(k, 0.0)
            kb[k].keyframe_insert("value", frame=f)
    for fc in anim.all_fcurves(bpy.data.objects["head"].data.shape_keys.animation_data.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - f) < 0.01:
                kp.interpolation = "CONSTANT"


# ----------------------------------------------------------------------------------------------- the effects
def _ribbon(name, pts, cam_loc, width, mat):
    """A flat strip through `pts`, turned to face the camera (so arcs read from any angle)."""
    verts, faces = [], []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        side = d.cross((cam_loc - p).normalized())
        side = side.normalized() * width * 0.5 if side.length > 1e-6 else Vector((width * 0.5, 0, 0))
        verts += [p - side, p + side]
        if i:
            faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.visible_shadow = False
    return o


def _jag(a, b, rnd, amp, n=7):
    """A jagged lightning path from a to b: n segments, kinked sideways by up to `amp` (zero at the ends)."""
    d = b - a
    ref = Vector((0, 0, 1)) if abs(d.normalized().z) < 0.9 else Vector((1, 0, 0))
    u, v = d.cross(ref).normalized(), d.cross(d.cross(ref)).normalized()
    pts = [a.copy()]
    for i in range(1, n):
        t = i / n
        w = amp * math.sin(t * math.pi) ** 0.5
        pts.append(a + d * t + u * rnd.uniform(-w, w) + v * rnd.uniform(-w, w))
    pts.append(b.copy())
    return pts


def _show_on(objs, frames, n):
    """Key hide_render so `objs` render only on `frames` (sorted ints)."""
    on = set(frames)
    for o in objs:
        for f in sorted(on | {f - 1 for f in on} | {f + 1 for f in on} | {0, n + 1}):
            o.hide_render = f not in on
            o.keyframe_insert("hide_render", frame=f)


def _arc(name, pts, cam_loc, frames, n, scale=1.0, glow=None, core=None):
    g = _ribbon(name + "_g", pts, cam_loc, 0.34 * scale, glow)
    c = _ribbon(name + "_c", [p + (cam_loc - p).normalized() * 0.05 for p in pts], cam_loc, 0.1 * scale, core)
    _show_on([g, c], frames, n)
    return [g, c]


def _ghost_mat():
    m = bpy.data.materials.new("s08b_ghost")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = look.hexc(GHOST)
    em.inputs[1].default_value = 1.6
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.55
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = True
    return m


def _bone_parent(o, rig, name):
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy()
    arm = rig["arm"]
    o.parent, o.parent_type = arm, "BONE"
    o.parent_bone = rig["bone"](name).name
    bpy.context.view_layer.update()
    o.matrix_world = mw


def _prim(kind, name, loc, rot=(0, 0, 0), scale=(1, 1, 1), mat=None, **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(mat)
    o.visible_shadow = False
    return o


def _xray(rig, frames, n):
    """The x-ray flash placeholder: on `frames` Kai's body turns into a translucent blue ghost with a white skeleton
    inside (bone-parented, so it follows the shake). Q5's 2D x-ray replaces it."""
    arm = rig["arm"]
    def under(o):
        while o is not None:
            if o == arm:
                return True
            o = o.parent
        return False
    body = [o for o in bpy.data.objects if o.type == "MESH" and (under(o) or o.find_armature() == arm)]
    extra = list(rig.get("cap") or []) + list(rig.get("shoes") or [])
    extra += [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(("cap", "shoe"))]
    body += [o for o in dict.fromkeys(extra) if o.type == "MESH" and o not in body]
    ghost_m = _ghost_mat()
    ghosts = []
    for o in body:
        g = o.copy()
        bpy.context.scene.collection.objects.link(g)
        for md in [md for md in g.modifiers if md.type == "SOLIDIFY"]:
            g.modifiers.remove(md)                                    # no inverted-hull outline on the ghost
        for slot in g.material_slots:
            slot.link = "OBJECT"
            slot.material = ghost_m
        g.visible_shadow = False
        ghosts.append(g)
    bone_m = look.flat("s08b_bone", look.hexc("#f6fbff"), 2.6)
    hole_m = look.flat("s08b_hole", look.hexc("#0b1530"), 1.0)
    bpy.context.view_layer.update()
    W = lambda nm, end="head": arm.matrix_world @ getattr(rig["bone"](nm), end)   # noqa: E731
    fwd = (arm.matrix_world.to_3x3() @ Vector((0, -1, 0))).normalized()
    up = (W("neck") - W("hips") if "hips" in arm.pose.bones else W("neck") - W("spine")).normalized()
    shoulder = (W("left_upper_arm") - W("right_upper_arm")).length
    r = shoulder * 0.055                                               # limb-bone radius
    sk = []

    def rod(nm, a, b, rad, parent):
        d = b - a
        o = _prim("cylinder", nm, (a + b) / 2, Vector((0, 0, 1)).rotation_difference(d).to_euler(),
                  (rad, rad, d.length / 2), bone_m, vertices=10)
        for e, end in ((a, "a"), (b, "b")):                             # knobbly joints
            sk.append(_prim("uv_sphere", f"{nm}_{end}", e, scale=(rad * 1.6,) * 3, mat=bone_m, segments=10,
                            ring_count=6))
            _bone_parent(sk[-1], rig, parent)
        _bone_parent(o, rig, parent)
        sk.append(o)

    for s in ("left", "right"):
        rod(f"sk_{s}_humerus", W(f"{s}_upper_arm"), W(f"{s}_lower_arm"), r, f"{s}_upper_arm")
        rod(f"sk_{s}_radius", W(f"{s}_lower_arm"), W(f"{s}_hand"), r * 0.85, f"{s}_lower_arm")
        rod(f"sk_{s}_femur", W(f"{s}_upper_leg"), W(f"{s}_lower_leg"), r * 1.25, f"{s}_upper_leg")
        rod(f"sk_{s}_tibia", W(f"{s}_lower_leg"), W(f"{s}_foot"), r * 1.05, f"{s}_lower_leg")
    hip = (W("left_upper_leg") + W("right_upper_leg")) / 2
    neck = W("neck")
    rod("sk_spine", hip, neck, r * 0.8, "spine")
    hw = (W("left_upper_leg") - W("right_upper_leg")).length
    pel = _prim("uv_sphere", "sk_pelvis", hip + up * r, scale=(hw * 0.75, hw * 0.35, hw * 0.4), mat=bone_m,
                segments=12, ring_count=8)
    pel.rotation_euler = up.to_track_quat("Z", "Y").to_euler()
    _bone_parent(pel, rig, "spine")
    sk.append(pel)
    chest_lo, chest_hi = W("chest"), neck - up * shoulder * 0.12
    for i in range(4):                                                   # the ribcage: four rings
        t = (i + 0.5) / 4
        c = chest_lo.lerp(chest_hi, t) + fwd * shoulder * 0.08
        rr = shoulder * (0.3 + 0.08 * math.sin(t * math.pi))
        ring = _prim("torus", f"sk_rib{i}", c, up.to_track_quat("Z", "Y").to_euler(), (1, 0.62, 1), bone_m,
                     major_radius=rr, minor_radius=r * 0.55, major_segments=20, minor_segments=6)
        _bone_parent(ring, rig, "chest")
        sk.append(ring)
    hb = rig["bone"]("head")
    hlen = max(hb.length, shoulder * 0.3)
    skull_c = W("head") + up * hlen * 0.55 + fwd * hlen * 0.08
    skull = _prim("uv_sphere", "sk_skull", skull_c, scale=(hlen * 0.62, hlen * 0.66, hlen * 0.72), mat=bone_m,
                  segments=16, ring_count=10)
    _bone_parent(skull, rig, "head")
    sk.append(skull)
    side = fwd.cross(up).normalized()
    for sgn in (-1, 1):                                                   # the eye sockets
        e = _prim("uv_sphere", f"sk_eye{sgn}", skull_c + fwd * hlen * 0.55 + side * sgn * hlen * 0.24 + up * hlen *
                  0.05, scale=(hlen * 0.17,) * 3, mat=hole_m, segments=10, ring_count=6)
        _bone_parent(e, rig, "head")
        sk.append(e)
    jaw = _prim("uv_sphere", "sk_jaw", skull_c - up * hlen * 0.55 + fwd * hlen * 0.2,
                scale=(hlen * 0.4, hlen * 0.32, hlen * 0.2), mat=bone_m, segments=12, ring_count=6)
    _bone_parent(jaw, rig, "head")
    sk.append(jaw)
    _show_on(ghosts + sk, frames, n)
    off = [f for f in range(1, n + 1) if f not in set(frames)]
    _show_on(body, off, n)                                               # the real body hides on x-ray frames
    return ghosts, sk


def _export_2d(rig, cam, n, water_pts):
    """For the 2D pass (diorama_v3/helper4_comp.py): Kai's joints per frame (mk/joints) and the spark's path through
    the water (strip -> strip end -> the spill -> his feet) in full-res pixels per frame (the camera pushes in)."""
    from bpy_extras.object_utils import world_to_camera_view
    from channels.monsters.mk import joints
    os.makedirs(BUILD, exist_ok=True)
    joints.export(rig, cam, range(1, n + 1), os.path.join(BUILD, "S08b_joints.json"), head_up=KAI * 0.03)
    sc = bpy.context.scene
    rx, ry = sc.render.resolution_x, sc.render.resolution_y
    keep, paths = sc.frame_current, {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        pts = []
        for p in water_pts:
            v = world_to_camera_view(sc, cam, p)
            pts.append((round(v.x * rx, 1), round((1 - v.y) * ry, 1)))
        paths[str(f)] = pts
    sc.frame_set(keep)
    with open(os.path.join(BUILD, "S08b_water.json"), "w") as fh:
        json.dump(paths, fh)


# ----------------------------------------------------------------------------------------------- the shot
def s08b():
    n = _frames()
    B = _beats(n)
    diorama.setup()
    R = diorama_lab.room()
    R["puddle"](-60, -20)                                                 # S08 already flooded the floor
    leak, end = Vector(R["tank"]["leak"]), Vector(R["strip"]["end"])
    a, b = Vector((leak.x, R["desk"]["front_y"] - 0.4, 0)), Vector((end.x + 0.2, end.y + 0.2, 0))
    path = lambda u: a.lerp(b, u) + Vector((-0.6, -0.4, 0)) * math.sin(u * math.pi)   # noqa: E731 (puddle())
    feet = path(0.5)
    feet.z = 0.0
    chair = R["desk"]["chair"]
    chair.location.y -= 1.6                                               # he stood up and pushed it back
    chair.rotation_euler.z = math.radians(25)
    spill = next(m for m in bpy.data.objects["dl_spill0"].data.materials)
    pool = diorama_lab.lab._mesh("s08b_pool", [(math.cos(k / 24 * 2 * math.pi) * 2.1 * (1.0 + 0.12 * math.sin(k)),
                                                math.sin(k / 24 * 2 * math.pi) * 1.6, 0) for k in range(24)],
                                 [tuple(range(24))], spill, (feet.x, feet.y, 0.035))
    pool.visible_shadow = False

    # Kai, facing the front of the room, turned a little toward the camera
    rig = hero.load((feet.x, feet.y, 0.0), scale=KAI, outfit="earth")
    from channels.monsters.diorama.helper1 import _tilt_cap
    _tilt_cap(rig, 40.0)                                                  # the brim up, so his eyes read from above
    arm = rig["arm"]
    arm.rotation_mode = "XYZ"                                             # x tips him back in his own frame (the fall)
    arm.rotation_euler = (0, 0, math.radians(18))
    bpy.context.view_layer.update()
    hit, out, fade = B["hit"], B["out"], B["fade"]
    _act(rig, B)
    rnd = random.Random(9)                                                # the light's flicker

    # the camera: close and low for the beat, a slow push-in on 1s
    chest = Vector((feet.x, feet.y, KAI * 0.85))
    target = chest.lerp(Vector(R["strip"]["spark_at"]), 0.42)
    cam = R["cam"]("cam_s08b", tuple(target), dist=48.0, tilt=46.0, yaw=-34.0, lens=90.0, blur=9.0)
    cam.data.shift_y = -0.05                                              # the strip and its spark above the captions
    p0 = cam.location.copy()
    left = -(cam.matrix_world.to_3x3() @ Vector((1, 0, 0)))              # screen-left, in the world
    left.z = 0.0
    left = left.normalized() * 2.0                                        # the follow as he falls (~120 px)
    f_fall = B["out"] - 3
    for f in [1] + list(range(f_fall, B["black"] + 1)):                   # the push-in, plus the follow on the fall
        k = (f - 1) / (B["black"] - 1)
        u = min(1.0, max(0.0, (f - f_fall) / 5.0))
        cam.location = Vector(target).lerp(p0, 1.0 - 0.1 * k) + left * (u * u * (3 - 2 * u))
        cam.keyframe_insert("location", frame=f)
        d = (Vector(target).lerp(p0, 1.0 - 0.1 * k) - Vector(target)).length
        cam.data.dof.focus_distance = d
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    for fc in anim.all_fcurves(cam.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    bpy.context.scene.frame_set(1)
    cl = cam.location.copy()

    # the spark at the strip, then the run through the water to his feet (on 1s)
    glow = look.flat("s08b_arc_glow", look.hexc(ARC_GLOW), 3.2)
    core = look.flat("s08b_arc_core", look.hexc(ARC_CORE), 6.0)
    R["spark"](B["spark"])
    r0, r1 = B["run"]
    strip_pt = Vector(R["strip"]["spark_at"])
    water_pts = [strip_pt, Vector((end.x, end.y, 0.06))] + [path(1 - u) + Vector((0, 0, 0.06))
                                                           for u in (0.1, 0.2, 0.3, 0.4, 0.5)]
    run_len = len(water_pts) - 1
    head_m = look.flat("s08b_head", look.hexc(ARC_CORE), 8.0)
    head = _prim("uv_sphere", "s08b_spark_head", tuple(strip_pt), scale=(0.35,) * 3, mat=head_m, segments=12,
                 ring_count=8)
    lt = diorama_lab.lab._light("s08b_spark_light", "POINT", tuple(strip_pt), (0, 0, 0), 0.0, ARC_GLOW, 0.3,
                                shadow=False)
    for f in range(r0, r1 + 1):
        u = (f - r0) / max(1, r1 - r0) * run_len
        i = min(int(u), run_len - 1)
        pos = water_pts[i].lerp(water_pts[i + 1], u - i)
        head.location = pos
        head.keyframe_insert("location", frame=f)
        lt.location = pos + Vector((0, 0, 0.8))
        lt.keyframe_insert("location", frame=f)
        diorama_lab.lab._kprop(lt.data, "energy", f, 900.0 + 500 * rnd.random(), "CONSTANT")
        trail = water_pts[:i + 1] + [pos]
        for j in range(2 if FX3D else 0):                                                # the arcs crawling over the water behind
            pts = []
            for q0, q1 in zip(trail[:-1], trail[1:]):
                pts += _jag(q0, q1, rnd, 0.35, 4)[:-1]
            pts.append(trail[-1])
            _arc(f"s08b_warc{f}_{j}", pts, cl, [f], n, 0.9 - 0.3 * j, glow, core)
    _show_on([head], list(range(r0, r1 + 1)) if FX3D else [], n)
    for f in range(r1 + 1, out + 1):                                      # it lights him up from below
        lt.location = chest - Vector((0, 0, KAI * 0.4)) + Vector((0, -1.2, 0))
        lt.keyframe_insert("location", frame=f)
        diorama_lab.lab._kprop(lt.data, "energy", f, (1600.0 + 1400 * rnd.random()) if f < out else 600.0,
                               "CONSTANT")
    diorama_lab.lab._kprop(lt.data, "energy", fade + 1, 0.0, "CONSTANT")

    # the arcs over his body, re-drawn every frame of the jolt (fewer and dimmer after the lights die)
    for f in range(hit, fade + 1) if FX3D else ():
        bpy.context.scene.frame_set(f)
        W = lambda nm: arm.matrix_world @ rig["bone"](nm).head                        # noqa: E731
        T = lambda nm: arm.matrix_world @ rig["bone"](nm).tail                        # noqa: E731
        foot_l, foot_r = W("left_foot"), W("right_foot")
        chains = [[foot_l, W("left_lower_leg"), W("left_upper_leg"), W("chest")],
                  [foot_r, W("right_lower_leg"), W("right_upper_leg"), W("neck")],
                  [W("chest"), W("left_upper_arm"), W("left_lower_arm"), T("left_hand")],
                  [W("chest"), W("right_upper_arm"), W("right_lower_arm"), T("right_hand")],
                  [W("neck"), T("head")]]
        k = 1.0 if f < out else 0.6
        for j, ch in enumerate(chains if f < out else chains[:2]):
            pts = []
            for q0, q1 in zip(ch[:-1], ch[1:]):
                pts += _jag(q0 + (cl - q0).normalized() * 0.6, q1 + (cl - q1).normalized() * 0.6, rnd, 0.55, 4)[:-1]
            pts.append(ch[-1] + (cl - ch[-1]).normalized() * 0.6)
            _arc(f"s08b_barc{f}_{j}", pts, cl, [f], n, k, glow, core)
            if rnd.random() < 0.6:                                        # a stray fork off the chain
                q = pts[rnd.randrange(1, len(pts) - 1)]
                tip = q + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 1))) * 1.4
                _arc(f"s08b_fork{f}_{j}", _jag(q, tip, rnd, 0.25, 3), cl, [f], n, 0.6 * k, glow, core)
        for p in (foot_l, foot_r):                                        # splashes of light at his feet
            _arc(f"s08b_splash{f}_{p.x:.0f}", _jag(p, p + Vector((rnd.uniform(-1.6, 1.6), rnd.uniform(-1.2, 1.2),
                                                                    0.05)), rnd, 0.3, 3), cl, [f], n, 0.7 * k, glow,
                 core)
    bpy.context.scene.frame_set(1)

    # the x-ray flashes; the room's lights stutter with each one, then everything dies
    xr = B["xray"]
    if FX3D:
        _xray(rig, xr, n)
    room, lamp = R["lights"]["room"], R["lights"]["lamp"]
    base = {o.name: o.data.energy for o in (room, lamp)}
    for f in range(hit - 1, out):
        for o in (room, lamp):
            diorama_lab.lab._kprop(o.data, "energy", f, base[o.name] * (0.05 if f in xr else 1.0), "CONSTANT")
    R["power_out"](out)
    _export_2d(rig, cam, n, water_pts)
    black = storm.power_out(cam, B["black"], flicker=False)
    del black
    dof = cam.data.dof                                                    # no tilt-shift blur on the black plane
    dof.keyframe_insert("aperture_fstop", frame=B["black"] - 1)
    dof.aperture_fstop = 64.0
    dof.keyframe_insert("aperture_fstop", frame=B["black"])
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co.x >= B["black"] - 1:
                kp.interpolation = "CONSTANT"
    return dict(frames=n, step=1, subject=[arm] + list(rig.get("cap", [])))


def _push(cam, n, k=0.08):
    """A slow push-in on 1s (DIORAMA_EP01_V3.md: a camera move in every shot): the camera eases `k` of the way to its
    focus point over the shot, the focus following, so the tilt-shift band stays on the subject."""
    fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
    target = cam.location + fwd * cam.data.dof.focus_distance
    p0, d0 = cam.location.copy(), cam.data.dof.focus_distance
    for f in range(1, n + 1, 2):
        u = (f - 1) / max(1, n - 1)
        e = u * u * (3 - 2 * u)
        cam.location = p0.lerp(target, k * e)
        cam.keyframe_insert("location", frame=f)
        cam.data.dof.focus_distance = d0 * (1 - k * e)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)


def _reused(builder, shot):
    """A v2 diorama shot of mine re-rendered for v3 (the Q2 dressing and Q3 light come through diorama.setup and the
    island): the same picture and beats, plus the push-in, so the camera now moves on 1s while the snail holds on 2s."""
    from channels.monsters.diorama_v3.shots import v3_frames
    info = builder()
    n = v3_frames(shot)
    if n != info["frames"]:
        print(f"{shot}: v3 wants {n} frames, the v2 builder makes {info['frames']}; rendering {n}", flush=True)
        info["frames"] = n
    _push(info["camera"], n)
    if info.get("step", 1) > 1:
        info["ones"] = (1, n)                                     # the camera on 1s; the snail keeps its 2s
    return info


def s10a():
    from channels.monsters.diorama import helper4 as d4
    return _reused(d4.s10a, "S10a")


def s11a():
    from channels.monsters.diorama import helper4 as d4
    return _reused(d4.s11a, "S11a")


SHOTS = {"S08b": s08b, "S10a": s10a, "S11a": s11a}
