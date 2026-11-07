"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), helper 1's shots (+ the shared villagers at night).

    S03 "The whole village backed away from me."  Late afternoon (dusk starts at S04), in the lane into the village
        (diorama_ep03/village.py): Kai stands in the middle of it, his left wrist still half raised with the mark
        glowing, the shrimp on his left shoulder. All round him the villagers step backwards, nets held out like
        wards, slip in through their doors, and the doors slam one after another; then the shutters bang shut down
        the lane. The last one runs. Kai is left alone in the empty lane: his arm drops, his head goes down a little.
        Camera: a slow crane up and back on 1s, from a medium shot of Kai to the whole empty lane round him.
    VN  (a test, not a shot) the villagers at night: the lane dark, Kai's mark the only light; one villager backing
        off with a net, one scratching a red blotch on a porch, porch bells swinging, a door slamming, shutters
        banging. Used for the coordinator's "push a still first".

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S03 OUT [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import helper9 as H9
from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.diorama_ep03 import village as V
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, hero, look, puffshrimp

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
GUESS = {"S03": 72, "S09": 92, "VN": 48}
SHRIMP_K = 0.42                      # the puff-shrimp on his shoulder (helper 3's SHRIMP_K)
CORAL = (1.0, 0.48, 0.36)
UP = Vector((0, 0, 1))


def _frames(shot):
    try:
        with open(TIMING) as fh:
            return {s["shot"]: s["render_frames"] for s in json.load(fh)["shots"]}[shot]
    except (OSError, KeyError, ValueError):
        return GUESS[shot]


def _smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _bw(rig, name, tail=False):
    pb = rig["arm"].pose.bones[name]
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _yaw_deg(face):
    return math.degrees(math.atan2(face.x, -face.y))              # the characters face their own -Y


def _world(n):
    """The island and helper 9's village and lake, then the lane's huts."""
    X._world(n)
    if "h9_lake" not in bpy.data.objects:
        H9.village_and_lake()
    return V.lane()


def _kai(at, face):
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    k["arm"].rotation_euler = (0, 0, math.radians(_yaw_deg(face)))
    k["arm"].location = at
    bpy.context.view_layer.update()
    return k


def _kai_face(keys, f):
    from channels.monsters.diorama_ep03.helper3 import _kai_face as kf
    kf(keys, f)


def _shoulder_shrimp(k, n, face, name="ep03_shrimp_h1"):
    """The puff-shrimp riding on Kai's left shoulder (helper 3's way), facing where he faces, breathing, blinking."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    sh["root"].scale = (SHRIMP_K,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(_yaw_deg(face)))
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        sh["root"].location = _bw(k, "upper_arm.L") + Vector((0, 0, 0.32))
        sh["root"].keyframe_insert("location", frame=f)
    sc.frame_set(1)
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 20)
    return sh


def _mark_light(k, n, energy=40.0, toward=None):
    """A coral point light at the mark (inside of his left forearm, helper 9's MARK_U), a slow pulse; follows the arm
    on 2s. (Helper 9's Ep 3 mark light replaces this when it lands.)"""
    d = bpy.data.lights.new("h1_mark_light", "POINT")
    d.color = CORAL
    d.shadow_soft_size = 0.2
    lt = bpy.data.objects.new("h1_mark_light", d)
    bpy.context.scene.collection.objects.link(lt)
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        m = H9._forearm(k, H9.MARK_U)
        off = (Vector(toward) - m).normalized() * 0.5 if toward is not None else UP * 0.4
        lt.location = m + off
        lt.keyframe_insert("location", frame=f)
        d.energy = energy * (0.92 + 0.08 * math.sin(f / 5.0))
        d.keyframe_insert("energy", frame=f)
    sc.frame_set(1)
    return lt


def _anchors(shot, n, fn):
    """{f: fn(f, cam)} -> build/monsters/diorama_ep03/<shot>_anchors.json, in 720x1280 pixels."""
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        out[f] = fn(f, sc.camera)
    sc.frame_set(1)
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(dict(frames=out), fh)


def _arm_anchors(k, c):
    """The mark (helper 9's geometry for post_helper9.mark) and his left forearm (elbow, wrist: Ep 2's three thin
    scratch marks, drawn by the 2D pass), on screen."""
    return dict(mark=H9._mark_geo(k, c), elbow=_px(c, H9._forearm(k, 0.0)), wrist=_px(c, H9._forearm(k, 1.0)))


def _px(cam, p):
    from bpy_extras.object_utils import world_to_camera_view
    q = world_to_camera_view(bpy.context.scene, cam, p)
    return [round(q.x * 720, 1), round((1 - q.y) * 1280, 1), round(q.z, 2)]


def _cam_pose(eye, tgt, lens, shift):
    """A camera pose (target, dist, tilt, yaw, lens, shift_y) for diorama/xprl._move that puts the lens at `eye`."""
    d = Vector(eye) - Vector(tgt)
    dist = d.length
    tilt = math.degrees(math.asin(d.z / dist))
    yaw = math.degrees(math.atan2(-d.x, -d.y))
    return (tuple(tgt), dist, tilt, yaw, lens, shift)


# ------------------------------------------------------------------------------------- the night (a stand-in)
def night_stub(dark=(0.055, 0.075, 0.19), glow=0.95, radius=0.46):
    """A stand-in night until helper 9's night grade lands: the frame multiplied down to a dark blue, then lifted back
    toward its own warm-tinted colours inside a soft circle round the mark (the mark is the only light; moved with
    the mark by keying the mask's x/y per frame, see _night_follow)."""
    sc = bpy.context.scene
    nt = sc.node_tree
    comp = next(n for n in nt.nodes if n.bl_idname == "CompositorNodeComposite")
    src = comp.inputs[0].links[0].from_socket
    mul = nt.nodes.new("CompositorNodeMixRGB")
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    mul.inputs[2].default_value = (*dark, 1.0)
    nt.links.new(src, mul.inputs[1])
    warm = nt.nodes.new("CompositorNodeMixRGB")
    warm.blend_type = "MULTIPLY"
    warm.inputs[0].default_value = 1.0
    warm.inputs[2].default_value = (1.0, 0.78, 0.7, 1.0)
    nt.links.new(src, warm.inputs[1])
    mask = nt.nodes.new("CompositorNodeEllipseMask")
    mask.name = "h1_night_mask"
    mask.inputs["Size"].default_value = (radius, radius * 720 / 1280)
    blur = nt.nodes.new("CompositorNodeBlur")
    blur.filter_type = "GAUSS"
    px = 0.16 * sc.render.resolution_x * sc.render.resolution_percentage / 100
    blur.inputs["Size"].default_value = (px, px)
    nt.links.new(mask.outputs[0], blur.inputs[0])
    gl = nt.nodes.new("CompositorNodeMath")
    gl.operation = "MULTIPLY"
    gl.inputs[1].default_value = glow
    nt.links.new(blur.outputs[0], gl.inputs[0])
    mix = nt.nodes.new("CompositorNodeMixRGB")
    nt.links.new(gl.outputs[0], mix.inputs[0])
    nt.links.new(mul.outputs[0], mix.inputs[1])
    nt.links.new(warm.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], comp.inputs[0])
    sc.world.color = (0.02, 0.03, 0.07)
    return mask


def _night_follow(mask, k, n):
    """Key the night mask's centre on the mark's screen position (on 2s, like the arm)."""
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        x, y, _ = _px(sc.camera, H9._forearm(k, H9.MARK_U))
        sock = mask.inputs["Position"]
        sock.default_value = (x / 720, 1 - y / 1280)
        sock.keyframe_insert("default_value", frame=f)
    sc.frame_set(1)


# ------------------------------------------------------------------------------------------------- Kai in the lane
def _pose_kai(P, k, f, face, arm_up=1.0, look=0.0, slump=0.0):
    """Standing, the left forearm half raised in front of him (the mark toward the lane), the right hand down; `look`
    turns his head (-1 right .. +1 left), `slump` drops the arm and the head (alone)."""
    left = Vector((-face.y, face.x, 0))
    P.reset()
    for sd, dx in (("L", 0.09), ("R", -0.09)):
        P.leg(sd, Vector((dx, 0, P.ankle_h)))
    P.rot("chest", (1.5 * math.sin(f / 20.0) + 6 * slump, 0, 0))
    bpy.context.view_layer.update()
    sho = _bw(k, "upper_arm.L")
    up_t = sho + face * 2.2 + UP * 0.2 + left * 0.1
    down_t = sho + face * 0.6 - UP * 2.6 + left * 0.5
    X._reach(P, k, "L", down_t.lerp(up_t, arm_up * (1 - slump)), bend=(0, 0, 0.0))
    P.twist("forearm.L", -80.0 * (1 - slump))
    X._reach(P, k, "R", _bw(k, "chest") + face * 0.7 - UP * 2.1 - left * 0.75)
    P.rot("neck", (4 * slump, 0, 14 * look))
    P.rot("head 1", (10 * slump, 0, 22 * look))
    P.key(f)


# ------------------------------------------------------------------------------------------------------------ S03
# who goes where: (hut, start: lane offset (across, along) from Kai, delay to start backing, frames to reach the door)
S03_CAST = [(2, (6.0, -2.0), 0, 15), (3, (-6.0, -1.0), 2, 15), (4, (5.0, 0.0), 4, 16), (5, (-4.5, 0.0), 6, 16),
            (4, (8.0, 4.0), 10, 16), (5, (-8.0, 4.0), 12, 16)]   # all beyond him from the camera: faces to camera
S03_NEAR = ((0, 12, 18), (1, 16, 24))  # the two huts by the camera: (hut, door slams, shutters bang) from inside
S03_RUNNER = ((1.0, 9.0), 12)        # (S03 is 55 frames: every door shut by ~f32, the shutters by ~f47)        # the last one: backs off up the lane, then turns and runs out of sight


def s03():
    n = _frames("S03")
    huts = _world(n)
    face = -V.LANE_DIR                                                  # he faces up the lane (toward the camera)
    left = Vector((-face.y, face.x, 0))
    k = _kai(V.LANE_AT, face)
    hero.line_width(k, 0.0028)
    P = x3.Pose(k)
    f_alone = 40                                                        # the last door is shut: he is alone
    for f in range(1, n + 1, 2):
        look = 0.9 * math.sin(f / 9.0) * (1 - _smooth((f - f_alone) / 8))   # he looks from one to the next
        _pose_kai(P, k, f, face, arm_up=1.0 - 0.25 * _smooth((f - 20) / 20), look=look,
                  slump=_smooth((f - f_alone) / 10))
    X.v2._twos([k["arm"]])
    _kai_face({"face_surprise": 0.35, "eye_brow_up": 0.6}, 1)          # wait: where are you all going?
    _kai_face({"face_sad": 0.45, "eye_brow_up": 0.8}, f_alone)         # alone
    _kai_face({"face_sad": 0.6, "eye_brow_up": 0.9, "look_down": 0.4}, f_alone + 8)
    sh = _shoulder_shrimp(k, n, face)
    anim.key(sh["body"], "rotation_euler", 1, (0, 0, 0.35), "CONSTANT")         # it looks round with him
    anim.key(sh["body"], "rotation_euler", 21, (0, 0, -0.35), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", f_alone, (0.25, 0, 0), "CONSTANT")   # then at him
    anim.on_twos(H9._shrimp_parts(sh), step=2)
    _mark_light(k, n, energy=28.0)
    # the villagers: each backs off to its own door, nets up, slips in, and the door slams; shutters follow
    rnd = random.Random(5)
    vs = []
    for i, (hi, (ax, al), delay, dur) in enumerate(S03_CAST):
        v = V.villager(i, 40 + i, net=(i % 3 != 2), bell=(i % 3 == 2))
        hut = huts[hi]
        p0 = hut["doorstep"].lerp(V.LANE_AT, 0.6) + left * ax * 0.15 + V.LANE_DIR * al * 0.1   # close round him
        f0, f1 = 1 + delay, 1 + delay + dur
        V.back_off(v, p0, hut["doorstep"], f0, f1, V.LANE_AT + UP * 6)
        V.slip_inside(v, hut, f1 + 2)
        vs.append(v)
        if i in (2, 3):                                                 # huts 4 and 5 take two: the second shuts it
            continue
        V.slam_door(hut, f1 + 5)
        V.bang_shutters(hut, f1 + 9 + rnd.randrange(0, 4))
    for hi, fd, fs in S03_NEAR:
        V.slam_door(huts[hi], fd)
        V.bang_shutters(huts[hi], fs)
    (ax, al), delay = S03_RUNNER
    v = V.villager(6, 46, net=True)
    p0 = V.LANE_AT + left * ax + V.LANE_DIR * al * 0.7
    p1 = p0 + V.LANE_DIR * 4.0
    V.back_off(v, p0, p1, 1 + delay, 1 + delay + 10, V.LANE_AT + UP * 6)
    for f in range(delay + 13, n + 1, 2):                               # turns and runs off down the lane
        u = (f - delay - 13) / 12.0
        anim.key(v["root"], "location", f, tuple(p1 + V.LANE_DIR * 16.0 * u), "CONSTANT")
        anim.key(v["root"], "rotation_euler", f, (0, 0, math.radians(_yaw_deg(V.LANE_DIR))), "CONSTANT")
        anim.key(v["body"], "location", f, (0, 0, 0.35 * (((f - delay) // 2) % 2)), "CONSTANT")
    vs.append(v)
    # camera: high 3/4 from up the lane (the square, the tower and the lake behind him), a slow crane up and back
    east = -left
    tgt = V.LANE_AT + UP * 3.0 + V.LANE_DIR * 3.0
    a = _cam_pose(V.LANE_AT - V.LANE_DIR * 27.0 + east * 5.0 + UP * 17.0, tgt, 35.0, -0.04)
    b = _cam_pose(V.LANE_AT - V.LANE_DIR * 35.0 + east * 6.0 + UP * 25.0, tgt, 35.0, -0.04)
    cam = X._cam_move("cam_s03", n, a, b)
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {o for o in bpy.data.objects if o.name.startswith(("vhut", "vil"))}
    for r in [k["arm"], sh["root"]]:
        keep.update([r, *r.children_recursive])
    _clear_view(cam, list(range(1, n + 1, 6)) + [n], V.LANE_AT, keep, reach=0.92)
    _anchors("S03", n, lambda f, c: _arm_anchors(k, c))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + [v["root"] for v in vs])


# ------------------------------------------------------------------------------------------------------------ VN
VN_EYE = V.LANE_AT - V.LANE_DIR * 32.0 + Vector((-V.LANE_DIR.y, V.LANE_DIR.x, 0)) * 1.5 + UP * 15.0


def vn():
    """The villagers at night, for the still: f30 has a door mid-slam, shutters banging, bells swinging."""
    n = _frames("VN")
    huts = _world(n)
    face = -V.LANE_DIR
    left = Vector((-face.y, face.x, 0))
    k = _kai(V.LANE_AT, face)
    hero.line_width(k, 0.0028)
    P = x3.Pose(k)
    for f in range(1, n + 1, 2):
        _pose_kai(P, k, f, face, arm_up=1.0, look=0.5 * math.sin(f / 9.0))
    X.v2._twos([k["arm"]])
    _kai_face({"eye_brow_down": 0.5, "eye_brow_up": 0.3}, 1)
    sh = _shoulder_shrimp(k, n, face)
    anim.on_twos(H9._shrimp_parts(sh), step=2)
    _mark_light(k, n, energy=60.0)
    vs = []
    v = V.villager(0, 40, net=True)                                     # backing off across the lane, net out
    V.back_off(v, V.LANE_AT + left * -3.5 + V.LANE_DIR * 3.0, V.LANE_AT + left * -6.5 + V.LANE_DIR * 6.0, 1, n,
               V.LANE_AT + UP * 6)
    vs.append(v)
    v = V.villager(1, 41, net=False)                                    # scratching on hut 2's porch
    anim.key(v["root"], "location", 1, tuple(huts[2]["porch"] + V.LANE_DIR * 1.2), "CONSTANT")
    anim.key(v["root"], "rotation_euler", 1, (0, 0, V._yaw_to(huts[2]["porch"], VN_EYE)), "CONSTANT")
    V.scratcher(v, 1, n)
    vs.append(v)
    for j, hi in enumerate((4, 0)):                                      # hand bells rung on porches
        v = V.villager(2 + j, 42 + j, net=False, bell=True)
        anim.key(v["root"], "location", 1, tuple(huts[hi]["porch"] - V.LANE_DIR * 1.5), "CONSTANT")
        anim.key(v["root"], "rotation_euler", 1, (0, 0, V._yaw_to(huts[hi]["porch"], V.LANE_AT)), "CONSTANT")
        for f in range(1, n + 1, 2):
            anim.key(v["bell"], "rotation_euler", f, (0, math.radians(30 * math.sin(f * 1.4 + j)), 0), "CONSTANT")
        vs.append(v)
    for j, h in enumerate(huts):
        V.ring_bell(h, 1, n, seed=j)
    V.slam_door(huts[4], 31)                                            # f30: mid-slam
    V.bang_shutters(huts[2], 30)
    V.bang_shutters(huts[0], 26)
    V.slam_door(huts[5], 18)
    east = -left                                                        # 3/4 onto the east huts' doors
    tgt = V.LANE_AT + UP * 3.5 + V.LANE_DIR * 7.0 + east * 4.5
    a = _cam_pose(VN_EYE, tgt, 30.0, -0.02)
    b = _cam_pose(VN_EYE + V.LANE_DIR * 2.5 + UP * -0.4, tgt, 30.0, -0.02)
    if os.environ.get("VN_CLOSE") == "1":                               # the scratcher's porch, close
        tgt = huts[2]["porch"] + UP * 5.0 + V.LANE_DIR * 0.5
        eye = tgt + huts[2]["face"] * 9.0 - V.LANE_DIR * 9.0 + UP * 1.5
        anim.key(vs[1]["root"], "rotation_euler", 1, (0, 0, V._yaw_to(huts[2]["porch"], eye)), "CONSTANT")
        a = _cam_pose(eye, tgt, 35.0, 0.0)
        b = _cam_pose(eye + (tgt - eye) * 0.08, tgt, 35.0, 0.0)
    cam = X._cam_move("cam_vn", n, a, b)
    mask = night_stub()
    _night_follow(mask, k, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + [v["root"] for v in vs])


# ------------------------------------------------------------------------------------------------------------ S09
S09_RINGERS = ((1, -0.6), (0, 0.4), (3, 0.2))     # (hut, yaw tweak): porch bell-ringers, from the camera to Kai
S09_MOTHS = 40


def _bez(p0, p1, p2, p3, u):
    a = 1 - u
    return p0 * a ** 3 + p1 * 3 * a * a * u + p2 * 3 * a * u * u + p3 * u ** 3


def s09():
    """S09 "The bells rang. The moths didn't even notice."  Night in the lane. Every bell rings from the first frames
    (porch bells and hand bells on the porches, the 2D ring lines in post); then, from behind the camera, the swarm
    streams in over the bell-ringers' heads and right past them without a flinch, down the lane to Kai's raised
    glowing wrist, where the first arrivals begin to circle it (backs tilting toward the light: S10's orbit)."""
    from channels.monsters.mk import fluffmoth as fm
    n = _frames("S09")
    huts = _world(n)
    sc = bpy.context.scene
    face = -V.LANE_DIR                                                  # he faces up the lane, toward the hill
    left = Vector((-face.y, face.x, 0))
    east = -left
    k = _kai(V.LANE_AT, face)
    hero.line_width(k, 0.0028)
    P = x3.Pose(k)
    f_see = 44                                                          # he sees them coming at him
    for f in range(1, n + 1, 2):
        _pose_kai(P, k, f, face, arm_up=1.0 + 0.15 * _smooth((f - 6) / 10), look=0.15 * math.sin(f / 11.0))
    X.v2._twos([k["arm"]])
    _kai_face({"eye_brow_down": 0.5, "eye_brow_up": 0.2}, 1)           # the wrist up, braced
    _kai_face({"face_surprise": 0.8, "eye_brow_up": 0.9, "eye_black_small": 0.5}, f_see)
    sh = _shoulder_shrimp(k, n, face)
    anim.key(sh["body"], "rotation_euler", 1, (0, 0, 0), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", f_see + 6, (0.45, 0, 0), "CONSTANT")    # it ducks behind his head
    anim.squash(sh["body"], f_see + 6, -0.25)
    anim.on_twos(H9._shrimp_parts(sh), step=2)
    _mark_light(k, n, energy=70.0)
    sc.frame_set(1)
    M = H9._forearm(k, H9.MARK_U)                                       # the light the swarm goes to
    # the bell-ringers on their porches (faces up the lane, ringing hard, never stopping) and every porch bell
    vs, ring_at = [], {}
    for j, (hi, tw) in enumerate(S09_RINGERS):
        v = V.villager(j, 60 + j, net=False, bell=True)
        hut = huts[hi]
        at = hut["porch"] - V.LANE_DIR * 1.2
        anim.key(v["root"], "location", 1, tuple(at), "CONSTANT")
        anim.key(v["root"], "rotation_euler", 1, (0, 0, V._yaw_to(at, at - V.LANE_DIR * 10) + tw), "CONSTANT")
        for f in range(1, n + 1, 2):
            anim.key(v["bell"], "rotation_euler", f, (0, math.radians(34 * math.sin(f * 1.5 + j * 2)), 0),
                     "CONSTANT")
            anim.key(v["body"], "rotation_euler", f, (0, 0, math.radians(4 * math.sin(f * 1.5 + j * 2))),
                     "CONSTANT")
        for sx in (-1, 1):                                              # eyes wide: they are ringing for their lives
            anim.key(bpy.data.objects[f"vil{j}_eye{sx}"], "scale", 1, (1.25, 0.5, 1.6), "CONSTANT")
        vs.append(v)
        ring_at[f"hand{j}"] = v["bell"]
    for j, h in enumerate(huts):
        V.ring_bell(h, 3 + j, n, amp=32.0, seed=j)
        ring_at[f"porch{j}"] = h["bell"]
    # the camera: low behind the first bell-ringer's porch, up the lane, looking down it at Kai; a slow push-in
    tgt = V.LANE_AT + UP * 5.0 - V.LANE_DIR * 3.0
    eye0 = V.LANE_AT - V.LANE_DIR * 26.0 - east * 5.5 + UP * 6.5
    a = _cam_pose(eye0, tgt, 32.0, -0.03)
    b = _cam_pose(eye0 + (tgt - eye0).normalized() * 3.0, tgt, 32.0, -0.03)
    cam = X._cam_move("cam_s09", n, a, b)
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {o for o in bpy.data.objects if o.name.startswith(("vhut", "vil"))}
    for r in [k["arm"], sh["root"]]:
        keep.update([r, *r.children_recursive])
    _clear_view(cam, [1, n], V.LANE_AT, keep, reach=0.95)
    # the swarm: from behind and above the camera, over and right past the ringers, down the lane to the wrist
    rnd = random.Random(9)
    ring_pts = [huts[hi]["porch"] - V.LANE_DIR * 1.2 + UP * rnd.uniform(9.0, 11.0) for hi, _ in S09_RINGERS]

    def place(i, r):
        return eye0 - V.LANE_DIR * r.uniform(6, 18) + east * r.uniform(-9, 9) + UP * r.uniform(3, 10), \
            r.uniform(0.36, 0.48)
    sw = fm.swarm(S09_MOTHS, place, name="s09m", seed=13,
                  far=lambda i, loc, s: False)
    for i, r in enumerate(sw):
        p0 = r["root"].location.copy()
        past = ring_pts[i % len(ring_pts)] + east * rnd.uniform(-2.5, 2.5) - V.LANE_DIR * rnd.uniform(-2, 2)
        rad, th0 = rnd.uniform(2.4, 5.5), rnd.uniform(0, math.tau)
        hz = rnd.uniform(-1.2, 2.2)
        entry = M + Vector((math.cos(th0) * rad, math.sin(th0) * rad, hz))
        c1 = p0.lerp(past, 0.6) + UP * rnd.uniform(-1, 1)
        c2 = past.lerp(entry, 0.5) + UP * rnd.uniform(0, 2.5) + east * rnd.uniform(-3, 3)
        t0 = int(rnd.uniform(18, 40))
        dur = int(rnd.uniform(28, 40))
        w = rnd.choice((-1, 1)) * rnd.uniform(1.6, 2.6) / rad           # orbit speed (rad/s), inner ones faster
        prev, last = None, p0
        for f in range(1, n + 3, 2):
            if f <= t0:
                p = p0
            elif f <= t0 + dur:
                u = (f - t0) / dur
                u = u * u * (3 - 2 * u) * 0.5 + u * 0.5                 # a little ease, mostly steady
                p = _bez(p0, c1, c2, entry, u)
            else:
                th = th0 + w * (f - t0 - dur) / 24.0
                p = M + Vector((math.cos(th) * rad, math.sin(th) * rad, hz + 0.25 * math.sin(f * 0.3 + i)))
            anim.key(r["root"], "location", f, tuple(p), "CONSTANT")       # on 2s, like the characters
            hd = (p - last) if (p - last).length > 1e-4 else -V.LANE_DIR
            if f > t0 + dur * 0.7:                                       # nearing the light: the back tilts to it
                amt = min(0.7, 0.7 * (f - t0 - dur * 0.7) / (dur * 0.5))
                r["root"].location = p
                prev = fm.back_to(r, f, M, hd, amount=amt, interp="CONSTANT", prev=prev)
            else:
                prev = fm.face(r, f, hd, bank=0.25 * math.sin(f * 0.2 + i), interp="CONSTANT", prev=prev)
            last = p
    _anchors("S09", n, lambda f, c: dict(_arm_anchors(k, c),
                                         **{f"bell_{nm}": _px(c, o.matrix_world @ Vector((0, 0, -1.2)))
                                            for nm, o in ring_at.items()}))
    mask = night_stub()
    _night_follow(mask, k, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + [v["root"] for v in vs] +
                [r["root"] for r in sw])


SHOTS = {"S03": s03, "S09": s09, "VN": vn}
