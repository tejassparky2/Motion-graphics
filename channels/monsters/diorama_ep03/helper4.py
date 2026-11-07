"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), helper 4.

    S01 "You said show her. So I did."  The hook, straight on from Ep 2's S20bot v2: close and low over Kai's left
        side, his raised left wrist big in the foreground with the coral mark blazing (2D: helper 9's zigzag via
        post_helper9.mark, bolder, a halo and sparkles; 3D: a strong coral point light on his arm). Behind it Wren
        stumbles back two steps, bell up like a ward (her 2D terror eyes carry on from Ep 2); the villagers flinch,
        turn and run back up the path, dropping their nets in the grass. Moving from frame 0 (a slow push-in on 1s,
        the characters on 2s). On "So I did." the shrimp hops from his right hand up onto his left shoulder.
    S11 (the explainer, later)

The 2D passes are drawn by diorama_ep02/post_helper4.py (EP=ep03) from build/monsters/diorama_ep03/<SHOT>_mark.json.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S01 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import helper4 as E2
from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import bgqrs as s3d
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, diorama, puffshrimp, wren

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
FPS = 24
_smooth = E2._smooth


def _timing():
    with open(TIMING) as f:
        return json.load(f)


def _frames(shot, fallback):
    try:
        return next(s for s in _timing()["shots"] if s["shot"] == shot)["render_frames"]
    except (OSError, StopIteration, KeyError, ValueError):
        return fallback


def _words(line_id, fallback=()):
    """[(word, first frame, last frame)] of a line, 1-based, relative to its shot's first frame."""
    try:
        d = _timing()
        ln = next(x for x in d["lines"] if x["id"] == line_id)
        s0 = next(s["start"] for s in d["shots"] if s["shot"] == ln["scene"])
        return [(w["w"].strip(".,!?:").lower(), 1 + round((w["start"] - s0) * FPS), 1 + round((w["end"] - s0) * FPS))
                for w in ln["words"]]
    except (OSError, StopIteration, KeyError, ValueError):
        return list(fallback)


def _cam_from(name, n, c0, c1, t0, t1, lens):
    """X._cam_move from two camera positions and aim points (the diorama blur/haze), on 1s."""
    def pose(c, t):
        v = c - t
        dist = v.length
        tilt = math.degrees(math.asin(max(-1.0, min(1.0, v.z / dist))))
        yaw = math.degrees(math.atan2(-v.x, -v.y))
        return (tuple(t), dist, tilt, yaw, lens, 0.0)
    return X._cam_move(name, n, pose(c0, t0), pose(c1, t1))


# ------------------------------------------------------------------------------------------------------------ S01
S01_LIGHT = 140.0                               # the mark's coral point light (close up, daylight: it has to show)


def _raised_arm(PK, k, fwd, up, u=1.0, tremble=0.0):
    """S20bot v2's end pose: the left forearm up toward Wren at face height, the inner wrist turned out; the right
    hand down at his side (the shrimp on it)."""
    side = X._side_vec(k)
    waist = E2._bone_world(k, "chest") + fwd * 0.75 - up * 2.1 + side * -0.75
    X._reach(PK, k, "R", waist)
    shoulder = E2._bone_world(k, "upper_arm.L")
    low = E2._bone_world(k, "chest") + fwd * 1.1 - up * 0.6 + side * 0.3
    high = shoulder + fwd * 2.4 + up * (0.9 + tremble) + side * -0.25
    X._reach(PK, k, "L", low.lerp(high, u), bend=(0, 0, 0.0))
    PK.twist("forearm.L", -80.0 * u)


def s01():
    from channels.monsters.diorama_ep02 import helper1 as h1
    from channels.monsters.diorama_ep02 import helper9 as H9
    n = _frames("S01", 72)
    W = _words("l1", [("you", 3, 8), ("said", 8, 14), ("show", 14, 22), ("her", 22, 30), ("so", 40, 45),
                      ("i", 45, 48), ("did", 48, 58)])
    fw = {}
    for w_, a_, b_ in W:
        fw.setdefault(w_, []).append((a_, b_))
    f_so = fw.get("so", [(int(n * 0.55), 0)])[0][0]                  # "So I did.": the shrimp hops
    X._world(n)
    h1.hill()
    k = X._kai()
    d = (X.WREN_STOP - X.KAI_AT).normalized()
    fwd = Vector((d.x, d.y, 0)).normalized()
    up = Vector((0, 0, 1))
    w0 = X.WREN_STOP + fwd * 0.75                                    # where S20bot v2 leaves her (half a step back)
    w = X._wren(w0, X.WREN_YAW)
    PK, PW = x3.Pose(k), x3.Pose(w)
    feet = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}

    # Wren: a stumble two steps back (anticipation, a heel catch, arms out), then she holds the bell up, trembling
    steps = [(1, 0.0), (5, 0.9), (9, 1.6), (13, 2.6), (17, 2.9), (21, 3.0)]   # (frame, distance back)

    def back_at(f):
        for (fa, da), (fb, db) in zip(steps[:-1], steps[1:]):
            if f < fb:
                return da + (db - da) * _smooth((f - fa) / (fb - fa))
        return steps[-1][1]

    for f in range(1, n + 1, 2):
        PW.reset()
        stumbling = f < 19
        for sd, ph in (("L", 0.0), ("R", math.pi)):
            lift = 0.35 * max(0.0, math.sin(f * 0.8 + ph)) if stumbling else 0.0
            PW.leg(sd, feet[sd] + Vector((0, 0, PW.ankle_h + lift)))
        wren.hold_bell(PW, 1.0, shake=3.0 * math.sin(f * 1.3))
        PW.aim("upper_arm.R", (-0.10, -0.80, 0.25))                 # the bell up like a ward (S20bot v2's end pose)
        PW.aim("forearm.R", (-0.04, -1.05, 0.6))
        PW.aim("hand.R", (-0.04, -0.3, -1))
        if stumbling:                                                # the free arm flung out for balance
            PW.aim("upper_arm.L", (0.9, -0.1, -0.2 + 0.3 * math.sin(f * 0.7)))
            PW.aim("forearm.L", (0.8, -0.4, 0.1))
        lean = 12.0 if f < 13 else 12.0 * (1 - _smooth((f - 13) / 10))
        PW.rot("chest", (-10.0 - lean + 1.0 * math.sin(f / 20.0), 0, 0))
        PW.rot("head 1", (-8.0, 0, 0))
        PW.key(f)
        dip = 0.25 * math.sin(math.pi * min(1.0, f / 18.0)) if stumbling else 0.0
        w["arm"].location = w0 + fwd * back_at(f) - up * dip
        w["arm"].keyframe_insert("location", frame=f)
    wren.FACES["fear"] = {"face_surprise": 1.0, "eye_black_small": 0.8, "eye_brow_up": 1.0, "lip_o": 0.5}
    wren.face(w, "fear", 1)
    wren.grip(w, 1)

    # Kai: holding the wrist up (a small push toward her at the start, a tremble), braced
    for f in range(1, n + 1, 2):
        PK.reset()
        for sd in ("L", "R"):
            PK.leg(sd, feet[sd] + Vector((0, 0, PK.ankle_h)))
        PK.rot("chest", (2.0 + 1.5 * math.sin(f / 20.0), 0, 0))
        bpy.context.view_layer.update()
        push = 0.25 * math.sin(math.pi * min(1.0, f / 14.0))
        _raised_arm(PK, k, fwd, up, 1.0, tremble=0.05 * math.sin(f * 1.7) + push)
        PK.rot("head 1", (-4.0, 0, 0))
        PK.key(f)
    E2._face({"eye_brow_down": 0.7, "face_angry": 0.25}, 1)          # steady
    E2._face({"eye_brow_down": 0.4, "face_sad": 0.3, "mouth_short": 0.4}, f_so)   # "So I did.": a wince at what it cost

    # the shrimp: on his right hand at his side, then a hop up onto his left shoulder ("So I did.")
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    sh["root"].scale = (E2.SHRIMP_IN_HAND,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW))      # facing out, with him
    sc = bpy.context.scene
    f_hop0, f_hop1 = f_so - 3, f_so + 9                              # crouch, jump, land
    base = Vector(sh["root"].scale)
    for f in range(1, n + 1):
        sc.frame_set(f)
        hand = X._world_of(k, "hand.R") + up * 0.3
        perch = E2._bone_world(k, "upper_arm.L") + up * 0.75 - fwd * 0.1
        if f < f_hop0 + 3:
            p, sq = hand, (1.0, 1.0, 0.82 if f >= f_hop0 else 1.0)    # a crouch before the jump
        elif f < f_hop1:
            u = (f - f_hop0 - 3) / (f_hop1 - f_hop0 - 3)
            p = hand.lerp(perch, u) + up * 2.2 * 4 * u * (1 - u)       # an arc up and over
            sq = (0.9, 0.9, 1.2) if u < 0.6 else (1.0, 1.0, 1.0)       # stretched in flight
        elif f < f_hop1 + 3:
            p, sq = perch, (1.15, 1.15, 0.78)                          # the landing squash
        else:
            p, sq = perch, (1.0, 1.0, 1.0)
        sh["root"].location = p
        sh["root"].keyframe_insert("location", frame=f)
        sh["root"].scale = (base.x * sq[0], base.y * sq[1], base.z * sq[2])
        sh["root"].keyframe_insert("scale", frame=f)
    for fc in anim.all_fcurves(sh["root"].animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.55, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.15, 0.0, 0.0), "CONSTANT")
    anim.blink(sh, 40)

    # the villagers: where S17 left them (a loose group on the rise behind Wren); they flinch, turn and run back up the
    # path, dropping their nets
    sc.frame_set(1)
    away_pt = Vector((X.KAI_AT.x, X.KAI_AT.y - 60.0, 0))
    for i, (dx, y0, delay, has_net, bell) in enumerate(h1.VILLAGERS):
        v = h1.villager(i, 11 + i * 7, net=has_net, bell=bell)
        x0 = diorama._path_x(y0) + dx
        target = Vector((X.KAI_AT.x + dx * 0.4, X.KAI_AT.y - 6.0, 0))
        start = Vector((x0, y0, 0))
        dd = (target - start).normalized()
        stop_at = 16.0 + 2.2 * i
        p0 = start + dd * max(0.0, (target - start).length - stop_at)
        face_in = math.atan2(dd.x, -dd.y)
        run = (away_pt + Vector((dx * 1.6, 0, 0)) - p0)
        run.z = 0
        run = run.normalized()
        face_out = math.atan2(run.x, -run.y)
        f_flinch = 2 + i % 3 * 2
        f_turn0 = f_flinch + 4
        f_run = f_turn0 + 6
        for f in range(1, n + 1, 2):
            if f < f_run:
                p = p0 - dd * (0.25 if f >= f_flinch else 0.0)
            else:
                p = p0 - dd * 0.25 + run * 0.55 * (f - f_run) * min(1.0, (f - f_run) / 6.0)
            p.z = h1.hill_height(p.x, p.y)
            anim.key(v["root"], "location", f, tuple(p), "CONSTANT")
            u = _smooth((f - f_turn0) / 6.0)
            dz = (face_out - face_in + math.pi) % (2 * math.pi) - math.pi
            anim.key(v["root"], "rotation_euler", f, (0, 0, face_in + dz * u), "CONSTANT")
            hop = 0.45 * abs(math.sin(f * 0.55 + i)) if f >= f_run else (0.3 if f_flinch <= f < f_flinch + 2 else 0.0)
            anim.key(v["body"], "location", f, (0, 0, hop), "CONSTANT")
            if v["bell"] is not None:
                anim.key(v["bell"], "rotation_euler", f, (0.6 * math.sin(f * 1.4 + i), 0, 0), "CONSTANT")
        if has_net:                                                  # the net drops: it falls free into the grass
            sc.frame_set(1)
            f_drop = f_turn0 + 2
            for nm in (f"vil{i}_pole", f"vil{i}_hoop", f"vil{i}_net"):
                o = bpy.data.objects.get(nm)
                if o is None:
                    continue
                sc.frame_set(f_drop)
                bpy.context.view_layer.update()
                mw = o.matrix_world.copy()
                ground = h1.hill_height(mw.translation.x, mw.translation.y)
                # it stays on its body until the drop, then a free copy falls and the attached one hides
                cp = o.copy()
                cp.data = o.data
                cp.parent = None
                sc.collection.objects.link(cp)
                cp.matrix_world = mw
                loc0 = mw.translation.copy()
                rot0 = cp.rotation_euler.copy()
                for f in range(1, n + 1, 2):
                    if f < f_drop:
                        cp.hide_render = True
                    else:
                        cp.hide_render = False
                        t = min(1.0, (f - f_drop) / 8.0)
                        z = loc0.z + (ground + 0.3 - loc0.z) * t * t
                        cp.location = (loc0.x, loc0.y, z)
                        cp.rotation_euler = (rot0.x + 1.2 * t, rot0.y, rot0.z)
                    cp.keyframe_insert("hide_render", frame=f)
                    cp.keyframe_insert("location", frame=f)
                    cp.keyframe_insert("rotation_euler", frame=f)
                    o.hide_render = f >= f_drop
                    o.keyframe_insert("hide_render", frame=f)
                for ob in (cp, o):
                    for fc in anim.all_fcurves(ob.animation_data.action):
                        for kp in fc.keyframe_points:
                            kp.interpolation = "CONSTANT"
    sc.frame_set(1)
    X.v2._twos([k["arm"], w["arm"], sh["body"], sh["hinge"]] + sh["eyes"])

    # camera: low and close behind Kai's left side, looking up past the raised wrist at Wren; a slow push-in on 1s
    sc.frame_set(1)
    bpy.context.view_layer.update()
    wrist = H9._forearm(k, H9.MARK_U)
    left = Vector((-fwd.y, fwd.x, 0))
    wren_head = w0 + fwd * 1.5 + up * 7.4
    c0 = wrist - fwd * float(os.environ.get("S01_BACK", "3.6")) + left * float(os.environ.get("S01_LEFT", "1.6")) \
        - up * float(os.environ.get("S01_LOW", "1.4"))
    t0 = wrist.lerp(wren_head, float(os.environ.get("S01_AIM", "0.55")))
    c1 = c0.lerp(wrist, 0.10)
    cam = _cam_from("S01cam", n, c0, c1, t0, t0, float(os.environ.get("S01_LENS", "24")))

    # the mark's light and its 2D anchors
    ld = bpy.data.lights.new("s01_mark_light", "POINT")
    ld.color = H9.CORAL
    ld.shadow_soft_size = 0.2
    lt = bpy.data.objects.new("s01_mark_light", ld)
    sc.collection.objects.link(lt)
    marks = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        m = H9._forearm(k, H9.MARK_U)
        lt.location = m + (cam.matrix_world.translation - m).normalized() * 0.45
        lt.keyframe_insert("location", frame=f)
        lvl = 1.15 + 0.12 * math.sin(f / 4.0)
        ld.energy = S01_LIGHT * lvl
        ld.keyframe_insert("energy", frame=f)
        marks[f] = dict(H9._mark_geo(k, cam), level=round(lvl, 3),
                        w_eye_l=H9._px(cam, s3d.kai_point(w, "eye_l")), w_eye_r=H9._px(cam, s3d.kai_point(w, "eye_r")))
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "S01_mark.json"), "w") as fh:
        json.dump(dict(meta=dict(f_so=f_so, f_fear=1), frames=marks), fh)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]],
                beats=dict(so=f_so, hop=(f_hop0, f_hop1)))


SHOTS = {"S01": s01}
