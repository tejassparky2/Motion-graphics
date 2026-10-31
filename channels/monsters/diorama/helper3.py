"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 3: S09, S13, S14 on the seed-31 island.
Every beat sits on the same frame as the 3D shot (ep01v2/helper3.py S09 v2, ep01v2/helper9.py S13/S14), because the
sound is synced to them.

    S09  "I woke up under a cracked sky." (66 frames) Diorama view of Kai on his back in the flower meadow
         (MAP["wake"]). f1-4 white; f4-12 the white blooms open onto him; his eyes open on "woke up" on 2s (closed,
         squint f14, wide open f18); f22-30 the camera tilts UP off him to the sky (SG5, on 1s); f30-66 the hairline
         crack (pistolshrimp.crack_path(), the tank's zigzag) held sharp and centred through "cracked sky", with a slow
         push under 10%. ORDER = "sky_first" plays the brief's other order (the crack first, then down to him).
    S13  "Something else was already drinking." (62 frames) The puff-shrimp drinking at the pond's north bank, claw
         dipped in the water, ripples on 1s, while Kai crawls up from the south and stops at the bank.
    S14  "A shrimp. On land. Impossible." (80 frames, step 3) A close diorama camera from above the pond: Kai on hands
         and knees, his face tipped up toward the lens, sceptical in two steps (eyes narrow f27, brow down and a head
         tilt f48), as in the 3D shot.

    blender -b -y -P channels/monsters/render_shot.py -- diorama S09 OUT_DIR [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Euler, Quaternion, Vector

from channels.monsters.ep01v2 import helper3 as h3d
from channels.monsters.ep01v2 import helper9 as h9
from channels.monsters.mk import anim, diorama, hero

MAP = diorama.MAP
KAI = 5.8                          # hero.load scale in creature units (1 unit = 20 cm): Kai ~8.7 units
ORDER = "v2"                       # S09: "v2" (Kai first, the crack held through "cracked sky") or "sky_first"


def _lying_kai(head):
    """Kai on his back at `head` (x, y), feet toward -y, face up, arms down at his sides. Returns (rig, face point)."""
    rig = hero.load((head[0], head[1] - 1.465 * KAI / 1.1, 0.18 * KAI / 1.1), scale=KAI, outfit="world")
    arm = rig["arm"]
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (math.radians(-90), 0, 0)
    for name, side in (("left_upper_arm", -1), ("right_upper_arm", 1)):
        b = rig["bone"](name)
        b.rotation_mode = "XYZ"
        b.rotation_euler = (0, 0, math.radians(side * 72))
    bpy.context.view_layer.update()
    face = arm.matrix_world @ rig["bone"]("head").head + Vector((0, 0.09, 0.12)) * (KAI / 1.1)
    return rig, face


def _key_rot(cam, frames_q):
    for f, q in frames_q:
        cam.rotation_euler = q.to_euler("XYZ", cam.rotation_euler)
        cam.keyframe_insert("rotation_euler", frame=f)


def s09():
    diorama.setup()
    diorama.island(seed=31)
    n = 66
    rig, face = _lying_kai(MAP["wake"])
    dist, lens = 55.0, 100.0
    cam = diorama.camera("cam_s09", face + Vector((0, -1.2, 0)), dist=dist, tilt=62, yaw=0, lens=lens, blur=12)
    cam.data.clip_end = 5000
    down = cam.rotation_euler.to_quaternion()
    up = Quaternion(Euler((math.radians(90 + 36), 0, 0)))          # 36 deg above the horizon, looking north
    h3d._sky_crack(cam.location, up, dist=dist, height=0.4 * dist * 36 / lens)   # at the focus distance: sharp
    if ORDER == "v2":
        _key_rot(cam, ((1, down), (22, down), (30, up)))
        push = (30, n)
    else:
        _key_rot(cam, ((1, up), (22, up), (30, down)))
        push = None
    if push:
        for f, ln in ((push[0], lens), (push[1], lens * 1.08)):     # a slow push on the crack, under 10%
            cam.data.lens = ln
            cam.data.keyframe_insert("lens", frame=f)
        for fc in anim.all_fcurves(cam.data.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    bloom = h3d._bloom(cam)
    z = 1.5                                                        # past the diorama camera's 1.0 near clip
    sx = z * (18 * 0.5625 / lens) / 0.496                          # keep the ramp's 1 = the frame's side edge
    bloom.location, bloom.scale = (0, 0, -z), (sx, sx / 0.5625, 1)
    for o in rig["arm"].users_collection[0].objects:               # nothing ghosts through the pure white
        for f, hide in ((1, True), (5, False)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)
    if ORDER == "v2":
        for f, names in ((1, ("blink",)), (12, ("blink",)), (14, ("squint",)), (18, ("surprised", "brows_up"))):
            h3d._faces(rig, names, f)                              # his eyes open on "woke up", on 2s
    else:
        for f, names in ((1, ("blink",)), (40, ("blink",)), (44, ("squint",)), (48, ("surprised", "brows_up"))):
            h3d._faces(rig, names, f)
    return dict(frames=n, step=2, ones=(22, n) if ORDER == "v2" else (1, 30), subject=[rig["arm"]])


SHRIMP = (MAP["shrimp"][0], MAP["shrimp"][1], 0.0)
KAI_STOP = (0.6, -11.0)            # where Kai's crawl stops, at the pond's south bank (S13 end, S14)


def s13():
    diorama.setup()
    diorama.island(seed=31)
    n = 62
    keep = h9.SHRIMP_AT
    h9.SHRIMP_AT = SHRIMP
    try:
        h9._dipped_shrimp(1, n)
    finally:
        h9.SHRIMP_AT = keep
    h9._ripples((SHRIMP[0] - 1.5, SHRIMP[1] - 1.7, 0.03), -20, n)
    h9._crawling_kai((KAI_STOP[0], KAI_STOP[1] - 6.0, 0.0), math.pi, 1, 40, 6.0, look_up=0.6)
    diorama.camera("cam_s13", (0.3, -6.0, 0.0), dist=95, tilt=56, yaw=0, lens=100, blur=12)
    return dict(frames=n, step=1, subject=[])


def s14():
    diorama.setup()
    diorama.island(seed=31)
    n = 80
    keep = h9.SHRIMP_AT
    h9.SHRIMP_AT = SHRIMP
    try:
        h9._dipped_shrimp(1, n)                                    # still drinking beyond him (out of focus)
    finally:
        h9.SHRIMP_AT = keep
    rig = h9._crawling_kai((KAI_STOP[0], KAI_STOP[1], 0.0), math.pi, 1, n, 0.0, period=10000, look_up=1.0)
    arm = rig["arm"]
    hero.line_width(rig, 0.0015)
    for f in (1, 5001):                                            # the face tipped up toward the lens
        bpy.context.scene.frame_set(f)
        h9._aim(arm, "neck", (0, -0.25, 0.97))
        h9._aim(arm, "head 1", (0, 0.42, 0.91))
        for b in ("neck", "head 1"):
            arm.pose.bones[b].keyframe_insert("rotation_quaternion", frame=f)
    h9._face_mix(rig, {"face_surprise": 0.4}, 1)
    h9._face_mix(rig, {"eye_zitome": 1.0, "mouth_short": 0.7}, 27)                    # "On land."
    h9._face_mix(rig, {"eye_zitome": 1.0, "eye_brow_down_L": 1.0, "eye_brow_up_R": 0.7, "mouth_short": 0.8,
                       "lip_down": 0.5, "look_down": 0.15}, 48)                        # "Impossible."
    head = arm.pose.bones["head 1"]
    for f, tilt in ((1, 0.0), (47, 0.0), (48, 0.16)):
        bpy.context.scene.frame_set(f)
        head.rotation_quaternion = head.rotation_quaternion.copy() @ Quaternion((0, 1, 0), tilt)
        head.keyframe_insert("rotation_quaternion", frame=f)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    eye = arm.matrix_world @ head.head + Vector((0, 0, 0.7))
    diorama.camera("cam_s14", eye, dist=50, tilt=50, yaw=180, lens=110, blur=12)
    return dict(frames=n, step=3, subject=[arm])


SHOTS = {"S09": s09, "S13": s13, "S14": s14}
