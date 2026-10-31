"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 3: S09, S13, S14 on the seed-31 island.
Every beat sits on the same frame as the 3D shot (ep01v2/helper3.py S09 v2, ep01v2/helper9.py S13/S14), because the
sound is synced to them.

    S09  "I woke up under a cracked sky." (66 frames) Diorama view of Kai on his back in the flower meadow
         (MAP["wake"]). f1-4 white; f4-12 the white blooms open onto him; his eyes open on "woke up" on 2s (closed,
         squint f14, wide open f18); f22-30 the camera tilts UP off him to the sky (SG5, on 1s); f30-66 the hairline
         crack (pistolshrimp.crack_path(), the tank's zigzag) held sharp and centred through "cracked sky", with a slow
         push under 10%; the haze eases off while the camera looks up, leaving a soft haze at the horizon.
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

import random

from channels.monsters.diorama import helper9 as d9
from channels.monsters.diorama.helper10 import LYING_RELAXED
from channels.monsters.ep01v2 import helper3 as h3d
from channels.monsters.ep01v2 import helper9 as h9
from channels.monsters.ep01v2 import helper10 as s15
from channels.monsters.mk import anim, diorama, hero, look, paintbg, world

MAP = diorama.MAP
KAI = 5.8                          # hero.load scale in creature units (1 unit = 20 cm): Kai ~8.7 units


def _lying_kai(head):
    """Kai on his back with his head at `head` (x, y), feet toward -y, in the relaxed lying pose the other diorama
    shots use (helper 10's LYING_RELAXED: one arm over his chest, knees a little bent, head tilted), so from above he
    reads as lying, not standing. Returns (rig, face point)."""
    rig = hero.load((0, 0, 0), scale=KAI, outfit="world")
    s15._pose(rig, LYING_RELAXED, (head[0], head[1] - 7.5, 1.0), (math.pi / 2, 0, math.pi))
    s15._ground(rig)
    hp = s15._world(rig, "head")
    rig["arm"].location += Vector((head[0] - hp.x, head[1] - hp.y, 0))
    bpy.context.view_layer.update()
    a, b = s15._world(rig, "head"), s15._world(rig, "head", tail=True)
    face = (a + b) / 2 + Vector((0, 0, 0.12 * KAI / 1.1))
    return rig, face


def _nestle(rig, n=170, seed=21):
    """Pink-flowered grass blades crowding his outline, some over his arms and legs: he lies IN the meadow."""
    rnd = random.Random(seed)
    arm = rig["arm"]
    bones = [s15._world(rig, b) for b in ("head", "chest", "hips", "left_upper_arm", "right_upper_arm",
                                          "left_lower_leg", "right_lower_leg", "left_foot", "right_foot")]
    greens = [paintbg.paint3(f"wake_blade{i}", *paintbg.greens(i), noise=0.1) for i in range(3)]
    pinks = [paintbg.paint3("wake_pink", look.hexc("#d05a8a"), look.hexc("#ff8fb8"), look.hexc("#ffd0e2"), noise=0.05),
             paintbg.paint3("wake_white", look.hexc("#c9c9e0"), look.hexc("#ffffff"), look.hexc("#ffffff"), noise=0.05)]
    blade = world._lathe([(0, 1.0), (1.0, 0.0), (0, -0.05)], 4)
    ball = world._sphere(8, 5)
    gb, fb = [world._Batch() for _ in greens], [world._Batch() for _ in pinks]
    for _ in range(n):
        c = rnd.choice(bones)
        a = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(0.7, 2.4)
        x, y = c.x + math.cos(a) * d, c.y + math.sin(a) * d
        for _ in range(3):
            ht = rnd.uniform(0.5, 1.1)
            tilt = world._rot(rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), rnd.uniform(0, 6))
            gb[rnd.randrange(3)].add(blade, (x + rnd.uniform(-0.15, 0.15), y + rnd.uniform(-0.15, 0.15), 0.0),
                                     (0.07, 0.07, ht), rot=tilt)
        if rnd.random() < 0.55:
            r = rnd.uniform(0.16, 0.26)
            fb[rnd.random() < 0.7 and 0 or 1].add(ball, (x, y, rnd.uniform(0.55, 1.0)), (r, r, r * 0.7))
    return [b.obj(f"wake_blades{i}", m) for i, (b, m) in enumerate(zip(gb, greens))] + \
           [b.obj(f"wake_flowers{i}", m) for i, (b, m) in enumerate(zip(fb, pinks))]


def _key_rot(cam, frames_q):
    for f, q in frames_q:
        cam.rotation_euler = q.to_euler("XYZ", cam.rotation_euler)
        cam.keyframe_insert("rotation_euler", frame=f)


def s09():
    diorama.setup()
    diorama.island(seed=31)
    n = 66
    rig, face = _lying_kai(MAP["wake"])
    _nestle(rig)
    dist, lens = 28.0, 100.0                                       # close top-down: his face reads at phone size
    cam = diorama.camera("cam_s09", face + Vector((0, -1.6, 0)), dist=dist, tilt=70, yaw=0, lens=lens, blur=12)
    cam.data.clip_end = 5000
    down = cam.rotation_euler.to_quaternion()
    up = Quaternion(Euler((math.radians(90 + 36), 0, 0)))          # 36 deg above the horizon, looking north
    crack = h3d._sky_crack(cam.location, up, dist=dist, height=0.4 * dist * 36 / lens, width=3.0)
    for o in crack.children:                                       # below the bloom threshold; a white-blue glow
        for node in o.data.materials[0].node_tree.nodes:
            if node.type == "EMISSION":
                node.inputs["Strength"].default_value = min(node.inputs["Strength"].default_value, 0.85)
                if "glow" in o.data.materials[0].name:
                    node.inputs["Color"].default_value = look.hexc("#dff1ff")
    puff = world._p3("dio_cloud", "#c9d6ee", "#eef3ff", "#ffffff", cuts=(0.22, 0.5), noise=0.06)
    rnd = random.Random(2)
    for cx, cy, sz in ((-1.9, -1.6, 0.55), (1.7, 1.9, 0.4)):          # two small clouds for scale, beside the crack
        b = world._Batch()
        for i in range(5):
            r = sz * rnd.uniform(0.6, 1.0)
            b.add(world._sphere(16, 10), (cx + (i - 2) * sz * 0.7, cy + rnd.uniform(0, sz * 0.4) + abs(i - 2) * -0.15 * sz,
                                          -0.3), (r * 1.2, r, r * 0.8))
        cl = b.obj("s09_cloud", puff, shadow=False)
        cl.parent = crack
    _key_rot(cam, ((1, down), (22, down), (30, up)))
    for f, ln in ((30, lens), (n, lens * 1.08)):                   # a slow push on the crack, under 10%
        cam.data.lens = ln
        cam.data.keyframe_insert("lens", frame=f)
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    ramp = next(nd for nd in bpy.context.scene.node_tree.nodes if nd.type == "VALTORGB")
    el = ramp.color_ramp.elements[1]
    for f, hz in ((22, 0.55), (30, 0.18)):                         # looking up: only a soft haze at the horizon
        el.color = (hz, hz, hz, 1)
        el.keyframe_insert("color", frame=f)
    bloom = h3d._bloom(cam)
    z = 1.5                                                        # past the diorama camera's 1.0 near clip
    sx = z * (18 * 0.5625 / lens) / 0.496                          # keep the ramp's 1 = the frame's side edge
    bloom.location, bloom.scale = (0, 0, -z), (sx, sx / 0.5625, 1)
    for o in rig["arm"].users_collection[0].objects:               # nothing ghosts through the pure white
        for f, hide in ((1, True), (5, False)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=f)
    for f, names in ((1, ("blink",)), (12, ("blink",)), (14, ("squint",)), (18, ("surprised", "brows_up"))):
        h3d._faces(rig, names, f)                                  # his eyes open on "woke up", on 2s
    return dict(frames=n, step=2, ones=(22, n), subject=[rig["arm"]])


SHRIMP = (MAP["shrimp"][0], MAP["shrimp"][1], 0.0)
KAI_STOP = (0.6, -11.0)            # where Kai's crawl stops, at the pond's south bank (S13 end, S14)


def s13():
    diorama.setup()
    isl_h = diorama.island(seed=31)
    n = 62
    keep = h9.SHRIMP_AT
    h9.SHRIMP_AT = SHRIMP
    try:
        h9._dipped_shrimp(1, n)
    finally:
        h9.SHRIMP_AT = keep
    h9._ripples((SHRIMP[0] - 1.5, SHRIMP[1] - 1.7, 0.03), -20, n)
    isl = isl_h
    rig = h9._crawling_kai((KAI_STOP[0], KAI_STOP[1] - 2.0, 0.0), math.pi, 1, 40, 2.0, period=16, look_up=3.0,
                           step=2)                                 # S12's crawl, stopping at S14's spot
    hero.line_width(rig, 0.0025)
    tgt = (0.4, -5.0)
    cam = diorama.camera("cam_s13", (tgt[0], tgt[1], 1.0), dist=70, tilt=45, yaw=165, lens=100, blur=12)
    d9._cut_front(isl, cam, tgt)                                   # from the north, as S12: he crawls toward us
    return dict(frames=n, step=1, subject=[rig["arm"]])


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
        h9._aim(arm, "neck", (0, 0.15, 0.99))
        h9._aim(arm, "head 1", (0, 0.88, 0.48))                    # looking up past the brim, at the lens
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
    diorama.camera("cam_s14", eye, dist=38, tilt=42, yaw=180, lens=110, blur=12)
    return dict(frames=n, step=3, subject=[arm])


SHOTS = {"S09": s09, "S13": s13, "S14": s14}
