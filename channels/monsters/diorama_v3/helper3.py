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
RIFT_H = 0.144                       # the crack's height in the sky (radians): ~40% of the frame at lens 100
POV_SIZE = 2.0                       # ... and from his POV, opened up
POV_LENS, POV_ELEV = 30.0, 20.0      # his POV: lens, and how far above the horizon he looks
SPARK_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                          "out", "monsters", "diorama_v3", "shots", "S09_spark.json")
TIMING = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep01v3", "timing.json")
# Kai's own frame (+Y forward = up once he lies down, +Z toward his head, +X his right): his loose left hand comes up
# in front of his face and he stares at it (reborn); anticipation, overshoot, settle on 2s. The right arm stays flung
# over his head (acting.LYING_V3).
HAND_COCK = [("left_upper_arm", (-0.5, 0.2, -0.85)), ("left_lower_arm", (-0.15, 0.45, -0.88))]   # anticipation
HAND_REACH = [("left_upper_arm", (0.12, 1.0, 0.02)), ("left_lower_arm", (0.25, 0.9, 0.35)),       # overshoot
              ("left_hand", (0.2, 0.5, 0.85))]
HAND_UP = [("left_upper_arm", (0.15, 1.0, 0.1)), ("left_lower_arm", (0.3, 0.8, 0.5)),            # held up above his
           ("left_hand", (0.25, 0.4, 0.9))]   # face, just past the brim, fingers spread: one clear silhouette, his
                                              # eyes on it below (picked from a 4-way test)
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
    start = (up @ Vector((0, 0, -1))).normalized()
    end = (Vector(land) - Vector(cam_loc))
    dist_end = end.length
    end.normalize()

    def pos(u):
        u = u * u * (3 - 2 * u)
        d = start.slerp(end, u) if start.dot(end) > -0.999 else start
        r = radius + (dist_end - radius) * u
        return Vector(cam_loc) + d * r

    ball = world_sphere("soul", radius * 0.012, core)                # its halo is the 2D pass's glow
    for f in range(f0 - 1, f1 + 1):
        anim.key(ball, "location", f, pos(max(0.0, min(1.0, (f - f0) / max(1, f1 - f0)))), "LINEAR")
    anim.key(ball, "scale", f0 - 2, 0.0, "CONSTANT")                # out of sight before the crack, gone on landing
    anim.key(ball, "scale", f0 - 1, 1.0, "CONSTANT")
    anim.key(ball, "scale", f1 + 1, 0.0, "CONSTANT")
    return ball, lambda f: pos(max(0.0, min(1.0, (f - f0) / max(1, f1 - f0))))


def _pov_flowers(pov, f_in, seed=9):
    """Tall pink and white flowers close in front of his POV, out of focus along the bottom and sides of the frame
    (hidden until the cut, so they never stand over him in the overhead shots)."""
    import random
    from channels.monsters.mk import paintbg, world
    rnd = random.Random(seed)
    stem = paintbg.paint3("pov_stem", *paintbg.greens(1), noise=0.1)
    heads = [paintbg.paint3("pov_pink", look.hexc("#d05a8a"), look.hexc("#ff8fb8"), look.hexc("#ffd0e2"), noise=0.05),
             paintbg.paint3("pov_white", look.hexc("#c9c9e0"), look.hexc("#ffffff"), look.hexc("#ffffff"), noise=0.05)]
    sb, hb = world._Batch(), [world._Batch(), world._Batch()]
    base = pov.matrix_world.translation
    for ang, d, h in ((-34, 2.6, 1.45), (-26, 3.6, 1.7), (-17, 3.0, 1.3), (-6, 4.2, 1.35), (7, 3.4, 1.25),
                      (17, 2.8, 1.5), (27, 3.8, 1.75), (35, 2.6, 1.4), (-40, 4.4, 2.0), (40, 4.6, 2.05)):
        a = math.radians(ang + rnd.uniform(-3, 3))
        x, y = base.x + math.sin(a) * d, base.y + math.cos(a) * d
        top = h + rnd.uniform(-0.15, 0.15)
        sb.add(world._sphere(6, 3), (x, y, top / 2), (0.05, 0.05, top / 2))
        for _ in range(rnd.randint(1, 2)):
            r = rnd.uniform(0.3, 0.45)
            hb[0 if rnd.random() < 0.65 else 1].add(world._sphere(8, 5), (x + rnd.uniform(-0.2, 0.2),
                                                                        y + rnd.uniform(-0.2, 0.2), top), (r, r, r * 0.8))
    objs = [sb.obj("pov_stems", stem, shadow=False)] + [b.obj(f"pov_heads{i}", heads[i], shadow=False)
                                                         for i, b in enumerate(hb)]
    for o in objs:
        for f, hide in ((1, True), (f_in, False)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)


def _crack_norm():
    """The S07/S08 tank crack's zigzag (h3d._crack_lines), centred, 1 unit tall (x right, y up)."""
    import numpy as np
    pts = np.array(h3d._crack_lines()[0], float)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    pts = (pts - (lo + hi) / 2) / (hi[1] - lo[1])
    return [[round(x, 4), round(y, 4)] for x, y in pts]


def _rift_path(cam_at, cam_loc, up, n, f_in):
    """Per frame: where the rift sits on a 720x1280 frame and its two axes in px per crack-height unit (c, ex, ey). The
    rift hangs at infinity in the direction the shot opens on (the camera's `up` view): RIFT_H radians tall, POV_SIZE x
    that from his POV (a wider lens, and it has opened). Points behind the camera are dropped (None)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    fwd, rt, upv = up @ Vector((0, 0, -1)), up @ Vector((1, 0, 0)), up @ Vector((0, 1, 0))
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        c = cam_at(f)
        h = RIFT_H * (POV_SIZE if f >= f_in else 1.0)

        def px(x, y):
            d = (fwd + rt * x * h + upv * y * h).normalized()
            v = world_to_camera_view(sc, c, c.matrix_world.translation + d * 4000)
            return None if v.z <= 0 else (v.x * 720, (1 - v.y) * 1280)
        p0, px_, py_ = px(0, 0), px(0.05, 0), px(0, 0.05)
        if p0 is None or px_ is None or py_ is None:
            out[f] = None
            continue
        out[f] = dict(c=[round(p0[0], 1), round(p0[1], 1)],
                      ex=[round((px_[0] - p0[0]) / 0.05, 2), round((px_[1] - p0[1]) / 0.05, 2)],
                      ey=[round((py_[0] - p0[0]) / 0.05, 2), round((py_[1] - p0[1]) / 0.05, 2)])
    sc.frame_set(1)
    return out


def _screen_path(cam, at, f0, f1, trail=5.0, steps=18):
    """Per frame, on a 720x1280 frame: the ball, and its trail (where it was over the last `trail` frames, oldest
    first) as this frame's camera sees it, so the trail streaks behind it in the world while the camera follows."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene

    def px(p):
        v = world_to_camera_view(sc, cam, p)
        return [round(v.x * 720, 1), round((1 - v.y) * 1280, 1)]
    out = {}
    for f in range(f0 - 1, f1 + 1):
        sc.frame_set(f)
        out[f] = dict(ball=px(at(f)), trail=[px(at(f - trail * i / steps)) for i in range(steps, 0, -1)
                                             if f - trail * i / steps >= f0])
    sc.frame_set(1)
    return out


def world_sphere(name, r, mat):
    from channels.monsters.mk import world
    b = world._Batch()
    b.add(world._sphere(12, 6), (0, 0, 0), (r, r, r))
    return b.obj(name, mat, shadow=False)


def _key_pose(rig, extra, frame, loc, rot, roll=0.0):
    """LYING_V3 with `extra` bones replaced, the left hand rolled about its own length by `roll` (the wrist turn),
    remembered for `frame` (helper 10 keys them all at the end)."""
    from channels.monsters.mk import acting
    over = dict(extra)
    s15._pose(rig, [(b, over.pop(b, d)) for b, d in acting.LYING_V3] + list(over.items()), loc, rot)
    if roll:
        pb = rig["bone"]("left_hand")
        pb.rotation_quaternion = pb.rotation_quaternion @ Quaternion((0, 1, 0), roll)
    s15._key_pose(rig, frame)


def s09():
    diorama.setup()
    diorama.island(seed=31)
    from channels.monsters.diorama_v3.shots import v3_frames   # here: shots.py imports this module
    n = v3_frames("S09")
    w = _words()
    f_woke = w.get("woke", 14)
    f_in = w.get("in", f_woke + 14)
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
    # camera: on the crack, follows the spark down (same eased arc, so it stays in frame), holds on Kai, tilts back
    # up on "In another world.", and a slow push throughout
    def follow(f):
        u = max(0.0, min(1.0, (f - fall[0]) / max(1, fall[1] - fall[0])))
        return up.slerp(down, u * u * (3 - 2 * u))
    rots = [(1, up)] + [(f, follow(f)) for f in range(fall[0], fall[1] + 1)]
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
    for f, hz in ((1, 0.18), (fall[0] + 2, 0.18), (fall[1] + 2, 0.55), (f_in - 1, 0.55), (f_in, 0.18)):
        el.color = (hz, hz, hz, 1)
        el.keyframe_insert("color", frame=f)
    # "In another world.": cut to his POV (an eyeline match on his look up): low by his head, looking north up past
    # the treetops to the rift, pink flowers out of focus along the bottom, a slow push
    pov = diorama.camera("cam_s09_pov", face + Vector((0, 60, 0)), dist=60, tilt=0, yaw=0, lens=POV_LENS, blur=10,
                         frame=f_in)
    pov.location = face + Vector((0, 1.2, 0.9))
    pov.rotation_euler = (math.radians(90 + POV_ELEV), 0, 0)
    pov.data.clip_start, pov.data.clip_end = 0.1, 5000
    pov.data.dof.focus_distance = 80
    pov.data.dof.aperture_fstop = diorama.fstop_for(80, POV_LENS, 10) * 10     # the near flowers soft, not gone
    for f, ln in ((f_in, POV_LENS), (n, POV_LENS * 1.1)):
        pov.data.lens = ln
        pov.data.keyframe_insert("lens", frame=f)
    for fc in anim.all_fcurves(pov.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    _pov_flowers(pov, f_in)
    mist = bpy.context.scene.world.mist_settings
    for f, st, dp in ((1, dist * 0.97, dist * 0.55), (f_in - 1, dist * 0.97, dist * 0.55), (f_in, 120.0, 400.0)):
        mist.start, mist.depth = st, dp
        mist.keyframe_insert("start", frame=f)
        mist.keyframe_insert("depth", frame=f)
    for fc in anim.all_fcurves(bpy.context.scene.world.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    chest = s15._world(rig, "chest") + Vector((0, 0, 0.8))
    ball, at = _spark(cam.location, up, chest, fall[0], fall[1], dist)
    SPARK.update(fall=list(fall), path=_screen_path(cam, at, fall[0], fall[1]), crack_on=list(crack_on), f_in=f_in,
                 crack=_crack_norm(), rift=_rift_path(lambda f: pov if f >= f_in else cam, cam.location, up, n, f_in))
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
    _key_pose(rig, HEAD_AWAKE + HAND_UP, f_woke + 12, loc, rot, roll=0.25)   # a small turn of the wrist (on 2s)
    _key_pose(rig, HEAD_AWAKE + HAND_UP, f_woke + 14, loc, rot, roll=0.45)
    s15._flush_keys(rig)
    bpy.context.scene.frame_set(f_woke + 8)
    hand = s15._world(rig, "left_hand")
    sky = Vector(cam.location) + (up @ Vector((0, 0, -1))) * dist * 4
    bpy.context.scene.frame_set(1)
    acting.expression(rig, "neutral", 1)
    acting.expression(rig, "surprised", f_woke)
    acting.expression(rig, "dazed", f_woke + 10)
    acting.expression(rig, "surprised", f_in - 4, value=0.75)     # his eyes flick up to the sky: the cut to his POV
    acting._key("eye_close", 1, 1.0)                               # shut until "woke"
    acting._key("eye_close", f_woke, 0.0)
    acting._key("eye_open", 1, 0.0)
    acting._key("eye_open", f_woke, 0.8)                           # the snap: wide for a beat, then settles
    acting._key("eye_open", f_woke + 6, 0.0)
    acting.look_at(rig, hand, f_woke + 8, f_in - 5, seed=9)
    acting.look_at(rig, sky, f_in - 4, f_in - 4, darts=False)
    acting.blink(rig, f_woke + 10, n, every=(40, 70), seed=5, at=(f_woke + 16,))
    for o in rig["arm"].users_collection[0].objects:               # nothing ghosts through the black
        for f, hide in ((1, True), (crack_on[1] + 2, False)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["arm"]])


def s13():
    """S13 "Something else was already drinking." (v2 diorama S13 on the v3 island and timing): the puff-shrimp drinking
    at the pond beyond, ripples, and Kai crawling toward us (S12's crawl) to the pond's south bank, seen from the
    north."""
    from channels.monsters.diorama import helper9 as d9
    from channels.monsters.diorama_v3.shots import v3_frames
    from channels.monsters.ep01v2 import helper9 as h9
    from channels.monsters.mk import hero
    diorama.setup()
    isl = diorama.island(seed=31)
    n = v3_frames("S13")
    keep = h9.SHRIMP_AT
    h9.SHRIMP_AT = d3.SHRIMP
    try:
        h9._dipped_shrimp(1, n)
    finally:
        h9.SHRIMP_AT = keep
    h9._ripples((d3.SHRIMP[0] - 1.5, d3.SHRIMP[1] - 1.7, 0.03), -20, n)
    rig = h9._crawling_kai((d3.KAI_STOP[0], d3.KAI_STOP[1] - 2.0, 0.0), math.pi, 1, 40, 2.0, period=16, look_up=3.0,
                           step=2)                                 # S12's crawl, stopping at S14's spot
    hero.line_width(rig, 0.0025)
    tgt = (0.4, -5.0)
    cam = diorama.camera("cam_s13", (tgt[0], tgt[1], 1.0), dist=70, tilt=45, yaw=165, lens=100, blur=12)
    d9._cut_front(isl, cam, tgt)                                   # from the north, as S12: he crawls toward us
    return dict(frames=n, step=1, subject=[rig["arm"]])


def s14():
    """S14 "A shrimp. On land. Impossible." (v2 diorama S14 on the v3 island and timing): Kai on his belly at the pond,
    his face tipped up to the lens past the cap's brim, the shrimp drinking beyond him out of focus; a flat stare on
    "On land.", then a one-brow "Impossible." with a head tilt."""
    from channels.monsters.diorama_v3.shots import v3_frames
    from channels.monsters.ep01v2 import helper9 as h9
    from channels.monsters.mk import hero
    diorama.setup()
    diorama.island(seed=31)
    n = v3_frames("S14")
    w = _words("S14")
    f_on, f_imp = w.get("on", 29), w.get("impossible", 50)
    keep = h9.SHRIMP_AT
    h9.SHRIMP_AT = d3.SHRIMP
    try:
        h9._dipped_shrimp(1, n)                                    # still drinking beyond him (out of focus)
    finally:
        h9.SHRIMP_AT = keep
    rig = h9._crawling_kai((d3.KAI_STOP[0], d3.KAI_STOP[1], 0.0), math.pi, 1, n, 0.0, period=10000, look_up=1.0)
    arm = rig["arm"]
    hero.line_width(rig, 0.0015)
    for f in (1, 5001):                                            # the face tipped up toward the lens
        bpy.context.scene.frame_set(f)
        h9._aim(arm, "neck", (0, 0.15, 0.99))
        h9._aim(arm, "head 1", (0, 0.88, 0.48))                    # looking up past the brim, at the lens
        for b in ("neck", "head 1"):
            arm.pose.bones[b].keyframe_insert("rotation_quaternion", frame=f)
    h9._face_mix(rig, {"face_surprise": 0.4}, 1)
    h9._face_mix(rig, {"eye_zitome": 1.0, "mouth_short": 0.7}, f_on - 2)                  # "On land."
    h9._face_mix(rig, {"eye_zitome": 1.0, "eye_brow_down_L": 1.0, "eye_brow_up_R": 0.7, "mouth_short": 0.8,
                       "lip_down": 0.5, "look_down": 0.15}, f_imp - 2)                     # "Impossible."
    head = arm.pose.bones["head 1"]
    for f, tilt in ((1, 0.0), (f_imp - 3, 0.0), (f_imp - 2, 0.16)):
        bpy.context.scene.frame_set(f)
        head.rotation_quaternion = head.rotation_quaternion.copy() @ Quaternion((0, 1, 0), tilt)
        head.keyframe_insert("rotation_quaternion", frame=f)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    eye = arm.matrix_world @ head.head + Vector((0, 0, 0.7))
    diorama.camera("cam_s14", eye, dist=38, tilt=42, yaw=180, lens=110, blur=12)
    return dict(frames=n, step=3, subject=[arm])


SHOTS = {"S09": s09, "S13": s13, "S14": s14}
