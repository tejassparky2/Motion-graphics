"""Episode 1 v2 shots by helper 9 (EP01V2_SHOTS.md): the storm in the lab (S06), the water and the power cut (S08), and
the meadow before the snap: Kai crawling to the puddle (S12), the puff-shrimp's claw in the water (S13, the clue) and
Kai's sceptical face (S14). Every shot carries the 12-frame tail handle.

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S06 OUTDIR
"""
import math

import bpy
from mathutils import Quaternion, Vector

from channels.monsters.mk import anim, hero, lab, look, meadow, puffshrimp, storm

TAIL = 12


def _frames(seconds):
    return round(seconds * 24) + TAIL


def _cam(name, loc, target, lens, fstop=None, focus=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    if fstop:
        c.data.dof.use_dof = True
        c.data.dof.aperture_fstop = fstop
        c.data.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    bpy.context.scene.camera = c
    return c


# ------------------------------------------------------------------------------------------------------------ lab
def s06():
    """S06 "Then the storm hit." (1.5 s): the lab window, locked. An anime bolt (storm.py, clipped to the window glass)
    on the lab's two-hit lightning (2-frame flashes of sky and room), then the room lights stutter on 2s."""
    h = lab.build()
    cam = h["cams"]["window"]
    bpy.context.scene.camera = cam
    bpy.data.objects["bolt"].hide_render = True          # the lab's simple bolt: storm.py draws the anime one
    win = bpy.data.objects["win_glass"]
    h["lightning"](8)
    storm.lightning(cam, 8, window=win, depth=7.5, flash=False, room_light=0, seed=3)
    h["flicker"]([16, 20, 23, 27])
    return dict(frames=_frames(1.5), step=1, subject=[])


def s08():
    """S08 "Water. Cables. Me." (2.2 s): floor level, locked. Water runs across the tiles to the power strip (0.8 s),
    a spark (0.6 s), then black (0.8 s, plus the tail). Nothing graphic: the cut to black is the whole event."""
    h = lab.build()
    cam = h["cams"]["floor"]
    bpy.context.scene.camera = cam
    h["crack_puddle"](-8, 19)                              # the leak started off-screen; it reaches the strip at 19
    h["flicker"]([24, 28])
    h["spark"](20)
    h["power_out"](34)
    storm.power_out(cam, 35, flicker=False)
    return dict(frames=_frames(2.2), step=1, subject=[])


# ------------------------------------------------------------------------------------------------------- meadow
SHRIMP_AT = (1.4, 0.4, 0.0)       # on the dry bank beside the puddle; its lowered claw lies in the water


def _dipped_shrimp(f0, f1):
    """The puff-shrimp drinking: claw lowered into the puddle, a slow bob and a little claw dip on 3s, ripples and a
    drop when the claw lifts a little."""
    rig = puffshrimp.build(SHRIMP_AT)
    sh, body = rig["shoulder"], rig["body"]
    for f, ang in ((f0, 1.76), (f0 + 18, 1.82), (f0 + 33, 1.7), (f0 + 48, 1.82), (f1, 1.76)):
        anim.key(sh, "rotation_euler", f, (ang, 0.0, 0.0))
    for f in range(f0, f1 + 1, 24):
        anim.squash(body, f, 0.0)
        anim.squash(body, f + 12, -0.04)
    anim.key(rig["hinge"], "rotation_euler", f0, (0.15, 0, 0))
    for e in rig["eyes"]:                                 # content, half-closed while it drinks
        anim.key(e, "scale", f0, (1, 1, 0.65), "CONSTANT")
    anim.blink(rig, f0 + 40)
    anim.on_twos([sh, body, rig["hinge"]] + rig["eyes"], step=3)
    return rig


def _ripples(center, f0, f1, every=12, seed=4):
    m = look.fade("ripple_m", look.hexc("#ffffff"), 0.0)
    mix = m.node_tree.nodes["Mix"]
    f = f0
    rings = []
    while f < f1:
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.035, location=center)
        r = bpy.context.object
        r.scale = (0.001, 0.001, 0.001)
        r.data.materials.append(m)
        anim.key(r, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(r, "scale", f, (0.5, 0.4, 0.3), "LINEAR")
        anim.key(r, "scale", f + 20, (1.25, 0.95, 0.3), "LINEAR")
        anim.key(r, "scale", f + 21, 0.001, "CONSTANT")
        rings.append(r)
        f += every
    for fr, a in ((f0 - 1, 0.0), (f0, 0.9)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    return rings


def s13():
    """S13 "Something else was already drinking." (2.5 s): insert of the clue (SG10, CH3): the puff-shrimp at the
    puddle with its big claw dipped in the water. Low, close, locked; acting on 3s, ripples on 1s."""
    meadow.build("before")
    n = _frames(2.5)
    _dipped_shrimp(1, n)
    tip = (SHRIMP_AT[0] - 1.5, SHRIMP_AT[1] - 1.7, 0.02)
    _ripples(tip, -20, n)
    c = _cam("cam_s13", (-2.9, -4.4, 1.9), (0.0, -0.9, 0.45), 34, fstop=2.8, focus=(-0.2, -1.3, 0.2))
    c.data.clip_end = 2000
    return dict(frames=n, step=1, subject=[])


# ---------------------------------------------------------------------------------------------------------- Kai
KAI_SCALE = 5.8                   # creature units (1 unit = 20 cm): Kai is ~8.7 units tall


def _aim(arm, name, d):
    """Turn a pose bone (about its head) so it points along armature-space direction d."""
    bpy.context.view_layer.update()
    pb = arm.pose.bones[name]
    m = pb.matrix.copy()
    q = (pb.tail - pb.head).normalized().rotation_difference(Vector(d).normalized())
    new = q.to_matrix().to_4x4() @ m
    new.translation = m.translation
    pb.matrix = new


# hands-and-knees pose, armature space (Kai faces -Y, +Z up); `reach` swaps which hand and knee lead
def _crawl_pose(arm, reach, look_up=0.0):
    lead = (-0.75, -0.35)                       # forward (y) component of the leading / trailing limb
    al, ar = (lead if reach > 0 else lead[::-1])
    kl, kr = (lead[::-1] if reach > 0 else lead)
    _aim(arm, "hips", (0, -1, 0.22))
    for n, d in (("spine", (0, -1, 0.3)), ("chest", (0, -1, 0.28)),
                 ("neck", (0, -0.75 + 0.45 * look_up, 0.66 + 0.3 * look_up)),
                 ("head 1", (0, -0.6 + 0.6 * look_up, 0.8 + 0.2 * look_up))):   # look_up 1: the face looks ahead
        _aim(arm, n, d)
    for side, a, k in (("L", al, kl), ("R", ar, kr)):
        sx = 1 if side == "L" else -1
        _aim(arm, f"upper_arm.{side}", (sx * 0.12, a * 0.7, -0.93))
        _aim(arm, f"forearm.{side}", (sx * 0.05, a * 0.5, -0.95))
        _aim(arm, f"hand.{side}", (sx * 0.1, -1, -0.15))
        _aim(arm, f"thigh.{side}", (sx * 0.08, k * 0.55, -0.9))
        _aim(arm, f"shin.{side}", (0, 1, -0.12))
        _aim(arm, f"foot.{side}", (0, 0.35, -0.94))


CRAWL_BONES = ["hips", "spine", "chest", "neck", "head 1"] + [f"{b}.{s}" for b in ("upper_arm", "forearm", "hand",
                                                                                     "thigh", "shin", "foot")
                                                               for s in "LR"]


def _key_pose(arm, frame):
    for n in CRAWL_BONES:
        pb = arm.pose.bones[n]
        pb.keyframe_insert("rotation_quaternion", frame=frame)
        if n == "hips":
            pb.keyframe_insert("location", frame=frame)


def _ground_offset(arm):
    """How far the posed body dips below z=0 (knees and hands should just touch the grass)."""
    bpy.context.view_layer.update()
    mw = arm.matrix_world
    low = min((mw @ arm.pose.bones[n].tail).z for n in ("forearm.L", "forearm.R", "thigh.L", "thigh.R"))
    return low


def _face_mix(rig, keys, frame):
    """Key several face shape keys at once (hero.face() keys one recipe and zeroes the rest)."""
    kb = bpy.data.objects["head"].data.shape_keys.key_blocks
    touched = set()
    for rv in hero.FACES.values():
        touched.update(rv.keys())
    touched.update(keys)
    for k in touched:
        if k in kb:
            kb[k].value = keys.get(k, 0.0)
            kb[k].keyframe_insert("value", frame=frame)
    ad = bpy.data.objects["head"].data.shape_keys.animation_data
    for fc in anim.all_fcurves(ad.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - frame) < 0.01:
                kp.interpolation = "CONSTANT"


def _crawling_kai(start, heading, f0, f1, dist, period=24, look_up=0.0):
    """Kai on hands and knees, crawling `dist` units along `heading` (radians, 0 = toward -Y) between f0 and f1. The
    limbs swap every half period; posed and keyed on 3s (acting), the body advances in steps with each reach."""
    rig = hero.load(start, scale=KAI_SCALE, rot_z=heading, outfit="world")
    arm = rig["arm"]
    arm.rotation_mode = "XYZ"                    # the appended armature is in quaternion mode; turn it to heading
    arm.rotation_euler = (0, 0, heading)
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    fwd = Vector((math.sin(heading), -math.cos(heading), 0))
    half = period // 2
    f, i = f0, 0
    while f <= f1 + half:
        for n in CRAWL_BONES:
            arm.pose.bones[n].rotation_quaternion = (1, 0, 0, 0)
        _crawl_pose(arm, 1 if i % 2 == 0 else -1, look_up)
        _key_pose(arm, f)
        f += half
        i += 1
    # lift the body so knees and hands sit on the grass, then step it forward with each reach (on 3s)
    bpy.context.scene.frame_set(f0)
    dz = -_ground_offset(arm) + 0.15
    n_steps = max(1, (f1 - f0) // 3)
    for k in range(n_steps + 1):
        fr = f0 + k * 3
        t = k / n_steps
        p = Vector(start) + fwd * dist * t
        arm.location = (p.x, p.y, start[2] + dz + 0.12 * math.sin(t * math.pi * (f1 - f0) / half))
        arm.keyframe_insert("location", frame=fr)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return rig


def s12():
    """S12 "I was so thirsty." (1.5 s): Kai crawls on hands and knees toward the puddle, low side view, locked. Tired
    face (droopy lids, mouth open). Acting on 3s, so only every 3rd frame is rendered."""
    meadow.build("before")
    n = _frames(1.5)
    rig = _crawling_kai((0.6, -11.0, 0.0), math.pi, 1, n, 3.0)
    _face_mix(rig, {"face_sad": 0.6, "eye_zitome": 0.5, "mouse_open": 0.6}, 1)
    _face_mix(rig, {"face_sad": 0.6, "eye_zitome": 0.7, "lip_a": 0.7}, 19)
    c = _cam("cam_s12", (13.5, -9.4, 1.4), (0.6, -9.4, 2.2), 26)
    c.data.clip_end = 2000
    return dict(frames=n, step=3, subject=[rig["arm"]])


def s14():
    """S14 "A shrimp. On land. Impossible." (2.5 s): Kai's sceptical face, close and locked, in two steps (SG2): first the
    eyes narrow (squint), then the brows come down and the head tilts. On 3s."""
    meadow.build("before")
    n = _frames(2.5)
    rig = _crawling_kai((0.6, -6.2, 0.0), math.pi, 1, n, 0.0, period=10000, look_up=1.0)   # stopped, head up
    arm = rig["arm"]
    hero.line_width(rig, 0.0015)
    _face_mix(rig, {"face_surprise": 0.4}, 1)
    _face_mix(rig, {"eye_zitome": 1.0, "mouth_short": 0.7}, 16)                       # step 1: flat stare
    _face_mix(rig, {"eye_zitome": 1.0, "eye_brow_down_L": 1.0, "eye_brow_up_R": 0.7, "mouth_short": 0.8,
                    "lip_down": 0.5, "look_down": 0.15}, 37)                            # step 2: one brow down, pout
    head = arm.pose.bones["head 1"]
    for f, tilt in ((1, 0.0), (36, 0.0), (37, 0.16)):          # the head cocks to one side with the second step
        bpy.context.scene.frame_set(f)
        head.rotation_quaternion = head.rotation_quaternion.copy() @ Quaternion((0, 1, 0), tilt)
        head.keyframe_insert("rotation_quaternion", frame=f)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    bpy.context.view_layer.update()
    hp = arm.matrix_world @ head.head
    eye = hp + Vector((0, 0, 0.75))
    c = _cam("cam_s14", (eye.x + 1.3, eye.y + 4.0, eye.z - 0.35), eye - Vector((0, 0, 0.3)), 58, fstop=2.0,
             focus=eye)
    c.data.clip_end = 2000
    return dict(frames=n, step=3, subject=[arm])


SHOTS = {"S06": s06, "S08": s08, "S12": s12, "S13": s13, "S14": s14}
