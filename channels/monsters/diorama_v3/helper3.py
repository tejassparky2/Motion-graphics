"""Episode 1 v3 (2.5D diorama), helper 3: S09 "Then I woke up. In another world." (channels/monsters/DIORAMA_EP01_V3.md,
out/monsters/story_v3_diorama.md). Built on the v2 diorama S09 (diorama/helper3.py): the same island, meadow spot, close
camera and sky crack; the beats are placed on the words of ep01v3/timing.json:

    black; the hairline crack draws on in the dark sky and glows, and the black opens out from it
    a small glowing spark (his soul) drops out of the crack with a trail; the camera tilts down after it (on 1s) into
        the pink-flower meadow and it lands on Kai's chest in a soft flash
    on "woke" his eyes snap open (surprised, brows up), then his hands come up in front of his face and he stares at
        them (anticipation, overshoot, settle; on 2s); a blink and an eye dart
    on "In another world." the camera tilts back up to the cracked sky and holds it, with a slow push

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S09 OUT [--still N --scale 0.5]
"""
import json
import math
import os

import bpy
from mathutils import Euler, Quaternion, Vector

from channels.monsters.diorama import helper3 as d3
from channels.monsters.ep01v2 import helper3 as h3d
from channels.monsters.ep01v2 import helper10 as s15
from channels.monsters.mk import anim, diorama, look

MAP = diorama.MAP
SPARK = {}
SPARK_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                          "out", "monsters", "diorama_v3", "shots", "S09_spark.json")
TIMING = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep01v3", "timing.json")
# Kai's own frame (+Y forward = up once he lies down, +Z toward his head, +X his right): his loose left hand comes up
# in front of his face and he stares at it (reborn); anticipation, overshoot, settle on 2s. The right arm stays flung
# over his head (acting.LYING_V3).
HAND_COCK = [("left_upper_arm", (-0.7, 0.3, -0.6)), ("left_lower_arm", (-0.3, 0.6, -0.5))]       # anticipation
HAND_REACH = [("left_upper_arm", (-0.28, 0.82, -0.5)), ("left_lower_arm", (0.3, 0.95, 0.12))]    # overshoot
HAND_UP = [("left_upper_arm", (-0.35, 0.72, -0.6)), ("left_lower_arm", (0.35, 0.93, 0.02))]      # held up over his
                                                                                                 # chest, to the sky
HEAD_AWAKE = [("neck", (0, 0.15, 1)), ("head", (-0.03, 0.35, 1))]   # the roll comes out, chin in a touch: his face
                                                                    # (wide eyes) turns to the camera


def _words(shot="S09"):
    """{word: first frame} for the shot's line (frame 1 = the shot's first frame), from ep01v3/timing.json."""
    with open(TIMING) as f:
        t = json.load(f)
    s = next(x for x in t["shots"] if x["shot"] == shot)
    out = {}
    for ln in t["lines"]:
        if ln.get("scene") == shot or ln.get("shot") == shot:
            for w in ln["words"]:
                key = w["w"].strip(".,!?").lower()
                out.setdefault(key, round((w["start"] - s["start"]) * 24) + 1)
    return out


def _spark(cam_loc, up, land, f0, f1, radius):
    """The soul: a bright little ball (core + halo) falling on an arc around the camera from the crack (straight ahead at
    `up`) to `land` between f0 and f1, eased; it stays in the scene's depth and blur. Its comet trail, twinkles and the
    landing flash and ring are drawn in 2D on top (spark_fx(), from the ball's screen path in S09_spark.json)."""
    core = look.flat("soul_core", look.hexc("#fffdf2"), 3.0)
    halo = look.fade("soul_halo", look.hexc("#ffe7a8"), 0.35)
    start = (up @ Vector((0, 0, -1))).normalized()
    end = (Vector(land) - Vector(cam_loc))
    dist_end = end.length
    end.normalize()

    def pos(u):
        u = u * u * (3 - 2 * u)
        d = start.slerp(end, u) if start.dot(end) > -0.999 else start
        r = radius + (dist_end - radius) * u
        return Vector(cam_loc) + d * r

    ball = world_sphere("soul", radius * 0.012, core)
    glow = world_sphere("soul_glow", radius * 0.03, halo)
    glow.parent = ball
    for f in range(f0 - 1, f1 + 1):
        anim.key(ball, "location", f, pos(max(0.0, min(1.0, (f - f0) / max(1, f1 - f0)))), "LINEAR")
    anim.key(ball, "scale", f0 - 2, 0.0, "CONSTANT")                # out of sight before the crack, gone on landing
    anim.key(ball, "scale", f0 - 1, 1.0, "CONSTANT")
    anim.key(ball, "scale", f1 + 1, 0.0, "CONSTANT")
    return ball


def _screen_path(cam, ball, f0, f1):
    """{frame: [x, y]} of the ball on a 720x1280 frame (the camera moves, so frame by frame)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(f0, f1 + 1):
        sc.frame_set(f)
        v = world_to_camera_view(sc, cam, ball.matrix_world.translation)
        out[f] = [round(v.x * 720, 1), round((1 - v.y) * 1280, 1)]
    sc.frame_set(1)
    return out


def world_sphere(name, r, mat):
    from channels.monsters.mk import world
    b = world._Batch()
    b.add(world._sphere(12, 6), (0, 0, 0), (r, r, r))
    return b.obj(name, mat, shadow=False)


def _key_pose(rig, extra, frame, loc, rot):
    """LYING_V3 with `extra` bones replaced, remembered for `frame` (helper 10 keys them all at the end)."""
    from channels.monsters.mk import acting
    over = dict(extra)
    s15._pose(rig, [(b, over.pop(b, d)) for b, d in acting.LYING_V3] + list(over.items()), loc, rot)
    s15._key_pose(rig, frame)


def s09():
    diorama.setup()
    diorama.island(seed=31)
    from channels.monsters.diorama_v3.shots import v3_frames   # here: shots.py imports this module
    n = v3_frames("S09")
    w = _words()
    f_woke = w.get("woke", 14)
    f_in = w.get("in", f_woke + 14)
    f_world_end = min(n - 12, w.get("world", f_in + 12) + 10)
    crack_on = (2, 5)                                              # the crack draws on, then the black opens
    fall = (5, max(9, f_woke - 3))                                 # the spark drops into the meadow
    from channels.monsters.mk import acting, hero
    rig = hero.load((0, 0, 0), scale=d3.KAI, outfit="world")
    wake = MAP["wake"]
    acting.lie(rig, (wake[0], wake[1] - 4.4), 0, spec=acting.LYING_V3)      # head toward +Y, at the wake spot
    bpy.context.view_layer.update()
    hd, ht = s15._world(rig, "head"), s15._world(rig, "head", tail=True)
    face = (hd + ht) / 2 + Vector((0, 0, 0.12 * d3.KAI / 1.1))
    d3._nestle(rig)                                                # the pink flowers crowd his outline
    loc, rot = rig["arm"].location.copy(), (math.pi / 2, 0, math.pi)
    dist, lens = 28.0, 100.0
    cam = diorama.camera("cam_s09", face + Vector((0, -1.6, 0)), dist=dist, tilt=70, yaw=0, lens=lens, blur=12)
    cam.data.clip_end = 5000
    down = cam.rotation_euler.to_quaternion()
    up = Quaternion(Euler((math.radians(90 + 36), 0, 0)))
    crack = h3d._sky_crack(cam.location, up, dist=dist, height=0.4 * dist * 36 / lens, width=3.0)
    for o in crack.children:
        for node in o.data.materials[0].node_tree.nodes:
            if node.type == "EMISSION":
                node.inputs["Strength"].default_value = min(node.inputs["Strength"].default_value, 0.85)
                if "glow" in o.data.materials[0].name:
                    node.inputs["Color"].default_value = look.hexc("#dff1ff")
    for f, s in ((1, (1, 0.0, 1)), (crack_on[0], (1, 0.0, 1)), (crack_on[1], (1, 1, 1))):
        anim.key(crack, "scale", f, s, "LINEAR")                   # the crack runs open along its length
    # camera: on the crack, tilt down after the spark, hold on Kai, tilt back up on "In another world.", push
    rots = ((1, up), (fall[0] + 1, up), (fall[1] + 2, down), (f_in, down), (f_world_end, up))
    for f, q in rots:
        cam.rotation_euler = q.to_euler("XYZ", cam.rotation_euler)
        cam.keyframe_insert("rotation_euler", frame=f)
    for f, ln in ((1, lens), (n, lens * 1.08)):                    # a slow push all the way through (on 1s)
        cam.data.lens = ln
        cam.data.keyframe_insert("lens", frame=f)
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    ramp = next(nd for nd in bpy.context.scene.node_tree.nodes if nd.type == "VALTORGB")
    el = ramp.color_ramp.elements[1]
    for f, hz in ((1, 0.18), (fall[0] + 2, 0.18), (fall[1] + 2, 0.55), (f_in, 0.55), (f_world_end, 0.18)):
        el.color = (hz, hz, hz, 1)
        el.keyframe_insert("color", frame=f)
    # black all round, just behind the crack, so the crack glows in the dark; then the dark fades and the sky shows
    dark_m = look.fade("s09_dark_m", (0, 0, 0, 1), 1.0)
    dark = world_sphere("s09_dark", dist * 1.4, dark_m)
    dark.location = cam.location
    mix = dark_m.node_tree.nodes["Mix"].inputs[0]
    for f, a in ((1, 1.0), (crack_on[1], 1.0), (crack_on[1] + 6, 0.0)):
        mix.default_value = a
        mix.keyframe_insert("default_value", frame=f)
    for f, hide in ((1, False), (crack_on[1] + 7, True)):
        dark.hide_render = hide
        dark.keyframe_insert("hide_render", frame=f)
    chest = s15._world(rig, "chest") + Vector((0, 0, 0.8))
    ball = _spark(cam.location, up, chest, fall[0], fall[1], dist)
    SPARK.update(fall=list(fall), path=_screen_path(cam, ball, fall[0], fall[1]))
    os.makedirs(os.path.dirname(SPARK_JSON), exist_ok=True)
    with open(SPARK_JSON, "w") as fh:
        json.dump(SPARK, fh)
    # Kai (mk/acting): out cold, head rolled; on "woke" his eyes snap open wide (surprised); his left hand comes up
    # in front of his face (anticipation, overshoot, settle, on 2s) and he stares at it, dazed; on "In another world."
    # his eyes go up to the crack in the sky; blinks throughout once he's awake
    _key_pose(rig, [], 1, loc, rot)
    _key_pose(rig, HEAD_AWAKE, f_woke, loc, rot)
    _key_pose(rig, HEAD_AWAKE + HAND_COCK, f_woke + 2, loc, rot)
    _key_pose(rig, HEAD_AWAKE + HAND_REACH, f_woke + 6, loc, rot)
    _key_pose(rig, HEAD_AWAKE + HAND_UP, f_woke + 8, loc, rot)
    s15._flush_keys(rig)
    bpy.context.scene.frame_set(f_woke + 8)
    hand = s15._world(rig, "left_hand")
    sky = Vector(cam.location) + (up @ Vector((0, 0, -1))) * dist * 4
    bpy.context.scene.frame_set(1)
    acting.expression(rig, "neutral", 1)
    acting.expression(rig, "surprised", f_woke)
    acting.expression(rig, "dazed", f_woke + 10)
    acting.expression(rig, "surprised", f_in, value=0.75)
    acting._key("eye_close", 1, 1.0)                               # shut until "woke"
    acting._key("eye_close", f_woke, 0.0)
    acting._key("eye_open", 1, 0.0)
    acting._key("eye_open", f_woke, 0.8)                           # the snap: wide for a beat, then settles
    acting._key("eye_open", f_woke + 6, 0.0)
    acting.look_at(rig, hand, f_woke + 8, f_in - 2, seed=9)
    acting.look_at(rig, sky, f_in, n, darts=True, seed=4)
    acting.blink(rig, f_woke + 10, n, every=(40, 70), seed=5, at=(f_woke + 16,))
    for o in rig["arm"].users_collection[0].objects:               # nothing ghosts through the black
        for f, hide in ((1, True), (crack_on[1] + 2, False)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["arm"]])


SHOTS = {"S09": s09}
