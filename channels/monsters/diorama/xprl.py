"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md): S22, S23, S24top, S24bot, restaged from the 3D shots
(helper 5's S22/S23 in ep01v2/helper5.py, the SAVE/RUN split in ep01v2/xprl.py) for the tilted toy world. Same beats
on the same frames as the 3D shots; the island after the snap (bgqrs._set: seed 31, the fan's trees gone, glowing
stumps), the thorn tree at diorama.MAP["thorn"], the shrimp drinking at the pond (MAP["shrimp"]), Kai knocked flat
at bgqrs.HIPS in S22/S23.

    S22 "That's when I saw the thorn tree." (57 frames): close on the larder (tiny shells skewered on thorns), then
        the camera cranes up and back (frames 8-36) to the thorn tree at the clearing's edge with the pond, the shrimp
        and Kai laid out below it. Camera on 1s.
    S23 "A butcher bird hangs its food on thorns." (82 frames): the bird drops onto the top of the thorn tree (f20),
        settles, lowers its head and glares up at the lens (f32: the hard top shadow and amber eye glints); f56 cuts to
        the insert: the one empty, shrimp-sized thorn, and its giant winged shadow on the grass reaching toward the
        pond. Locked cameras, the bird on 2s.
    S24top (SAVE, 97 frames, the action in y 80-600 for the in-place split): Kai walks up to the shrimp at the pond
        (f1-54), squats and holds out an open hand (f57-75) over the claw it lifts out of the water, wet and dripping
        (f16, drops from f27). The camera pushes in over f57-85 (1s).
    S24bot (RUN, 97 frames, the action in y 760-955 and x < 560): Kai west of the pond steps back toward the lens with
        his hands up (f10-40); the butcher bird glares from the thorn tree (f2), dives (f22-46) and mantles over the
        shrimp (f44-50); its giant shadow sweeps from Kai to the shrimp. Locked camera, everything on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama S24top OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
import numpy as np
from mathutils import Vector

from channels.monsters.diorama import bgqrs as d16
from channels.monsters.ep01v2 import helper5 as h5
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, butcherbird, diorama, hero, look, meadow, tuftwing

TAIL = 12
CUT = {"S22": 45, "S23": 70, "S24": 85}                  # ep01v2/TIMING.md
SHRIMP = (diorama.MAP["shrimp"][0], diorama.MAP["shrimp"][1], 0.0)
BLUR = 12.0
x3.SHRIMP_AT = SHRIMP                                    # the 3D helpers (_shrimp_wet, _bird_drop) build it here


def _twos(objs):
    """Characters on 2s (DIORAMA_EP01.md): every STEPPED modifier on these objects to a 2-frame step."""
    anim.on_twos(objs, step=2)
    for o in objs:
        ad = o.animation_data
        for fc in (anim.all_fcurves(ad.action) if ad and ad.action else []):
            for m in fc.modifiers:
                if m.type == "STEPPED":
                    m.frame_step = 2


def _cam(name, f, target, dist, tilt, yaw, lens, shift=(0.0, 0.0), cam=None):
    """diorama.camera's tilted toy camera, keyable: (re)place it at frame f and key the pose, lens, tilt-shift focus
    and the haze band (so a move keeps the miniature look constant)."""
    sc = bpy.context.scene
    if cam is None:
        cam = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=lens, blur=BLUR)
    t = Vector(target)
    el, az = math.radians(tilt), math.radians(yaw)
    cam.location = t + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.shift_x, cam.data.shift_y = shift
    cam.data.dof.focus_distance = dist
    cam.data.dof.aperture_fstop = diorama.fstop_for(dist, lens, BLUR)
    ms = sc.world.mist_settings
    ms.start, ms.depth = dist * 0.97, dist * 0.55
    if f is not None:
        for o, p in ((cam, "location"), (cam, "rotation_euler"), (cam.data, "lens"), (cam.data, "shift_y"),
                     (cam.data.dof, "focus_distance"), (cam.data.dof, "aperture_fstop"), (ms, "start"), (ms, "depth")):
            o.keyframe_insert(p, frame=f)
    return cam


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _move(name, f0, f1, a, b, n):
    """A camera move on 1s from pose a to pose b (target, dist, tilt, yaw, lens, shift_y) over f0..f1, held outside."""
    cam = None
    for f in range(1, n + 1):
        k = _smooth((f - f0) / (f1 - f0))
        t = tuple(a[0][i] + (b[0][i] - a[0][i]) * k for i in range(3))
        d, tl, yw, ln, sy = (a[i] + (b[i] - a[i]) * k for i in range(1, 6))
        cam = _cam(name, f, t, d, tl, yw, ln, (0.0, sy), cam)
    bpy.context.scene.camera = cam
    return cam


def _set(n, kai_down=True):
    """The island after the snap exactly as bgqrs builds it (seed 31, the fan's trees gone, hot-cut stumps smoking),
    keeping the island dict for the thorn tree; Kai knocked flat at his landing spot (S16-S21) if `kai_down`."""
    got, real = {}, diorama.island

    def keep(*a, **kw):
        got["isl"] = real(*a, **kw)
        return got["isl"]
    diorama.island = keep
    try:
        d16._set(n)
    finally:
        diorama.island = real
    rig = None
    if kai_down:
        rig = d16._kai()
        hero.line_width(rig, 0.0025)
    return got["isl"], rig


def _drinking(n):
    """The puff-shrimp at the pond's north edge, side-on (facing +X), its claw dipped in the water."""
    sh = x3._shrimp_wet(None, n)
    _twos([sh["shoulder"], sh["body"], sh["hinge"]] + sh["eyes"])
    return sh


# ------------------------------------------------------------------------------------------------------------- S22
# the thorn tree is seen from the clearing (from the south-west, over the open ground): the forest is behind it
YAW_THORN = math.degrees(math.atan2(diorama.MAP["thorn"][0], diorama.MAP["thorn"][1]))   # 64.7: camera south-west of it
def s22():
    n = CUT["S22"] + TAIL
    diorama.setup()
    isl, rig = _set(n)
    _drinking(n)
    th = isl["thorn"]
    shells = np.array(th["shell_spots"])
    near = shells[np.argsort(np.abs(shells[:, 2] - 2.4))[:4]].mean(axis=0)
    tree = Vector((diorama.MAP["thorn"][0], diorama.MAP["thorn"][1], 4.0))
    hips = Vector((d16.HIPS[0], d16.HIPS[1], 2.0))
    wide = tree.lerp(hips, 0.6)                                             # the tree at the top, Kai at the bottom
    _move("cam_s22", 8, 36, (tuple(near), 30.0, 44.0, 34.0, 100.0, 0.0),   # yaw 34: the tree and Kai on one line
          (tuple(wide), 100.0, 56.0, 34.0, 85.0, -0.06), n)
    return dict(frames=n, step=1, subject=[])


# ------------------------------------------------------------------------------------------------------------- S23
def _soft_shadow(rig, offset, tone="#24583f", opacity=0.82, soften=7.0):
    """The bird's giant shadow for the diorama: moved out over the open grass (as helper5's 3D insert does), but in the
    scene's cool shadow tone (the trees' shadows on this grass) with a soft painted edge, so from above it reads as a
    shadow and not as a hole in the ground."""
    from scipy import ndimage
    sh = rig["shadow"]
    bpy.context.view_layer.update()
    mw = sh.matrix_world.copy()
    mw.translation += Vector(offset)
    sh.matrix_world = mw
    nt = sh.data.materials[0].node_tree
    tex = next(nd for nd in nt.nodes if nd.type == "TEX_IMAGE")
    em = next(nd for nd in nt.nodes if nd.type == "EMISSION")
    em.inputs[0].default_value = look.hexc(tone)
    res = tex.image.size[0]
    a = ndimage.gaussian_filter(tuftwing.shadow_alpha(res), soften) * opacity / 0.72
    rgba = np.ones((res, res, 4), np.float32)
    rgba[..., 3] = np.clip(a, 0, 1)
    tex.image.pixels.foreach_set(rgba.ravel())
    tex.image.pack()


def s23():
    n = CUT["S23"] + TAIL
    diorama.setup()
    isl, rig = _set(n)
    _drinking(n)
    th = isl["thorn"]
    perch = Vector(th["perch"])
    yaw = YAW_THORN
    el, az = math.radians(48.0), math.radians(yaw)
    to_cam = Vector((-math.sin(az), -math.cos(az), 0))
    bird = tuftwing.build((perch.x, perch.y, 0.0), shadow_span=10.0)
    bird["root"].scale = (h5.BIRD_SCALE,) * 3
    bird["root"].rotation_euler = (0, 0, math.atan2(to_cam.x, -to_cam.y))  # it faces the lens
    rest = (0.0, 0.0, perch.z / h5.BIRD_SCALE)
    butcherbird.land(bird, 20, drop=(0.6, 1.8, 3.2), rest=rest)
    tuftwing.beat(bird, 22)
    butcherbird.stare(bird, 32, down=-0.25, hold=n - 32)                    # head up: the glare is at the lens above
    h5._rage_light(bird, 32, perch.z + (tuftwing.CENTER[2] - 0.1) * h5.BIRD_SCALE)
    pond = Vector((diorama.MAP["pond"][0], diorama.MAP["pond"][1], 0.0))
    reach = (pond - Vector((perch.x, perch.y, 0))).normalized() * 6.5      # the shadow lies out toward the pond
    _soft_shadow(bird, (reach.x, reach.y, 0.0))
    anim.blink(bird, 29)
    _twos(tuftwing._animated(bird))
    sc = bpy.context.scene
    up = _cam("cam_s23_bird", None, tuple(perch + Vector((0, 0, 0.6))), 46.0, 48.0, yaw, 100.0)
    base, tip = (Vector(p) for p in th["empty_thorn"])
    mid = (base + tip) / 2
    ground = Vector((perch.x + reach.x, perch.y + reach.y, 0.0))
    ins = _cam("cam_s23_thorn", None, tuple(mid.lerp(ground, 0.22)), 36.0, 60.0, yaw, 100.0)
    h5._glint(tuple(tip + (tip - base).normalized() * 0.03), ins, 62)
    for m in list(sc.timeline_markers):
        sc.timeline_markers.remove(m)
    ms = sc.world.mist_settings
    for f, c, d in ((1, up, 46.0), (h5.INSERT_AT, ins, 36.0)):
        mk = sc.timeline_markers.new(c.name, frame=f)
        mk.camera = c
        ms.start, ms.depth = d * 0.97, d * 0.55                           # the haze band follows the cut
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    for c in anim.all_fcurves(sc.world.animation_data.action):
        for kp in c.keyframe_points:
            kp.interpolation = "CONSTANT"
    sc.camera = up
    return dict(frames=n, step=2, subject=[bird["root"]])


# ------------------------------------------------------------------------------------------------------------- S24
SAVE_END = (SHRIMP[0] + 4.65, SHRIMP[1] - 0.8)           # where Kai squats beside the shrimp (the 3D spacing)


def s24top():
    """SAVE: Kai walks in from the east along the pond's north shore, squats beside the shrimp and offers an open hand
    over the claw it has lifted, wet, out of the pond."""
    n = CUT["S24"] + TAIL
    diorama.setup()
    _set(n, kai_down=False)
    shrimp = x3._shrimp_wet(16, n)
    tip = x3._claw_tip(shrimp, 28)
    meadow.drips((tip.x, tip.y, tip.z - 0.05), 27, n, every=10, fall=max(0.5, tip.z - 0.05))
    _twos([shrimp["shoulder"], shrimp["body"], shrimp["hinge"]] + shrimp["eyes"])
    k = x3._hero((SAVE_END[0] + 5.8, SAVE_END[1], 0), -90)                 # facing -X, toward the shrimp
    hero.line_width(k, 0.0025)
    P = x3.Pose(k)
    start, end = Vector((0, 0, 0)), Vector((0, -1.0, 0))

    def walk_upper(P, t):
        P.rot("spine", (8 + 8 * t, 0, 0))
        P.rot("chest", (4 + 4 * t, 0, 0))
        P.rot("head 1", (-6, 0, 0))                                         # face up to the lens above
        x3._arms_down(P, 10)
        reach = min(1.0, t * 1.2)
        P.aim("upper_arm.R", (-0.15, -0.3 - 0.45 * reach, -1 + 0.45 * reach))
        P.aim("forearm.R", (-0.05, -0.45 - 0.4 * reach, -0.85 + 0.25 * reach))
        P.aim("upper_arm.L", (0.25, 0.1, -1))

    def squat_upper(P, t):
        P.rot("spine", (12 + 6 * t, 0, 0))
        P.rot("chest", (6 + 2 * t, 0, 0))
        P.rot("neck", (-20 * t, 0, 0))
        P.rot("head 1", (-50 * t, 0, 0))                                    # chin up: his face to the lens above
        x3._arms_down(P, 10)
        P.aim("upper_arm.R", (-0.12, -0.75 - 0.15 * t, -0.45 - 0.1 * t))   # reaching out over the claw
        P.aim("forearm.R", (-0.04, -0.95, -0.15 - 0.1 * t))
        P.aim("hand.R", (-0.02, -1, -0.1))
        P.twist("upper_arm.R", -90 * t)                                     # an open hand, offered
        P.aim("upper_arm.L", (0.3, 0.05, -1))
        P.aim("forearm.L", (0.15, -0.5, -0.8))

    feet = x3._walk(P, k, (start, end), 1, 54, 0.33, "R", crouch=(0.0, 0.12), upper=walk_upper)
    x3._squat(P, feet, 57, 75, 0.12, 0.36, squat_upper, hold_to=n)
    hero.face(k, "neutral", 1)
    hero.face(k, "happy", 52, 0.35)
    _twos([k["arm"]])
    mid = Vector((SHRIMP[0] + 2.4, SHRIMP[1] - 0.3, 2.6))
    a = (tuple(mid + Vector((1.6, 0, 0.8))), 78.0, 44.0, 66.0, 80.0, -0.2)     # from his front, past the shrimp
    b = (tuple(mid), 62.0, 44.0, 66.0, 96.0, -0.22)
    _move("cam_s24top", 57, 85, a, b, n)
    return dict(frames=n, step=2, ones=(57, 85), subject=[k["arm"]])


RUN_KAI = (SHRIMP[0] - 6.1, SHRIMP[1] - 1.2)             # west of the pond, beside the shrimp's row


def s24bot():
    """RUN: Kai (west of the pond) steps back toward the lens, hands up, eyes on the bird; the butcher bird dives from
    the thorn tree onto the shrimp and mantles over it, its giant shadow sweeping from him to the shrimp."""
    n = CUT["S24"] + TAIL
    diorama.setup()
    isl, _ = _set(n, kai_down=False)
    shrimp = _drinking(n)
    bird = x3._bird_drop(isl["thorn"], 22, 46, n, kai_at=RUN_KAI)
    x3._mantle(bird, 44, 50)
    for e in shrimp["eyes"]:
        anim.key(e, "scale", 45, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 47, (0.78, 1, 0.78), "CONSTANT")
    for h in shrimp["hi"]:
        anim.key(h, "scale", 45, (1, 1, 1), "CONSTANT")
        anim.key(h, "scale", 47, (1.35, 1.35, 1.35), "CONSTANT")
    _twos(tuftwing._animated(bird) + shrimp["eyes"] + shrimp["hi"])
    k = x3._hero((RUN_KAI[0], RUN_KAI[1], 0), 15)                          # facing the lens, a touch toward the bird
    hero.line_width(k, 0.0025)
    P = x3.Pose(k)
    start, end = Vector((0, 0, 0)), Vector((0, -0.2, 0))

    def upper(P, t):
        P.rot("spine", (-8 - 4 * t, 0, 0))                                 # leaning back from it
        P.rot("chest", (-5, 0, 0))
        P.rot("neck", (-18, 0, 0))
        P.rot("head 1", (-40 - 6 * t, 0, 12))                               # face up: the bird (and the lens) above
        x3._arms_down(P, 14)
        P.aim("upper_arm.R", (-0.4, -0.6, -0.35))                           # both hands up by the shoulders
        P.aim("forearm.R", (-0.05, -0.3, 0.95))
        P.aim("upper_arm.L", (0.4, -0.6, -0.35))
        P.aim("forearm.L", (0.05, -0.3, 0.95))

    x3._walk(P, k, (start, end), 10, 40, 0.2, "L", crouch=(0.02, 0.06), upper=upper)
    x3._walk(P, k, (end, end + Vector((0, -0.001, 0))), 41, n, 0.2, "L", crouch=(0.06, 0.06), upper=upper)
    hero.FACES.setdefault("run_up", {"face_surprise": 1, "look_up": 0.18, "mouse_open": 0.7})
    hero.FACES.setdefault("run_wide", {"face_surprise": 1, "look_up": 0.18, "mouse_open": 0.85, "eye_black_small": 0.6})
    hero.face(k, "surprised", 1, 0.6)
    hero.face(k, "run_up", 10)
    hero.face(k, "run_wide", 46)
    _twos([k["arm"]])
    tgt = (SHRIMP[0] - 2.6, SHRIMP[1] - 0.9, 1.0)
    _cam("cam_s24bot", 1, tgt, 95.0, 70.0, 0.0, 90.0, (0.0, 0.19))                # near top-down: Kai's height folds
    return dict(frames=n, step=2, subject=[k["arm"]])


SHOTS = {"S22": s22, "S23": s23, "S24top": s24top, "S24bot": s24bot}
