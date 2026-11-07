"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), helper 4.

    S01 "You said show her. So I did."  The hook, straight on from Ep 2's S20bot v2: close and low over Kai's left
        side, his raised left wrist big in the foreground with the coral mark blazing (2D: helper 9's zigzag via
        post_helper9.mark, bolder, a halo and sparkles; 3D: a strong coral point light on his arm). Behind it Wren
        stumbles back two steps, bell up like a ward (her 2D terror eyes carry on from Ep 2); the villagers flinch,
        turn and run back up the path, dropping their nets in the grass. Moving from frame 0 (a slow push-in on 1s,
        the characters on 2s). On "So I did." the shrimp hops from his right hand up onto his left shoulder.
    S11 "Moths don't fly at a light. They keep their backs to it."  The explainer, a clean graphic side view on a dark
        night ground (like Ep 2's S06): ONE fluffmoth flies level from the left past a coral glow (above and ahead of
        it): it does NOT fly at it. On "They keep their backs to it" its back tilts square to the glow
        (fluffmoth.back_to, helper 6) and that tilt bends its path into an arc round the light; a soft 2D glow line
        runs from the light to its back (post_helper4, EP=ep03). No text. A slow push-in on 1s, the moth on 2s.

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
LAST = {}                                       # the last build's rigs (for framing probes)


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
S01_LIGHT = 420.0                               # the mark's coral point light (close up, daylight: it has to show)


def _owner(o):
    while o is not None:
        if o.type == "ARMATURE":
            return o
        a = o.find_armature() if o.type == "MESH" else None
        if a is not None:
            return a
        o = o.parent
    return None


def _visible(cam, p, rig, tol):
    """Is world point p (on `rig`) seen by cam, or hidden behind something else (or deep inside its own body)?"""
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    o = cam.matrix_world.translation
    d = p - o
    hit, loc, _n, _i, ob, _m = sc.ray_cast(dg, o, d.normalized(), distance=d.length)
    if not hit or (loc - o).length >= d.length - 0.2:
        return True
    return _owner(ob) == rig and (loc - o).length >= d.length - tol


def _late_afternoon(fwd):
    """A warm low sun from behind Wren's side (onto Kai's face), the sky a touch warmer: late afternoon (S01; the
    mark still the brightest thing)."""
    sc = bpy.context.scene
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.color = (1.0, 0.78, 0.55)
            o.data.energy *= 0.85
            d = (fwd * 1.0 + Vector((0, 0, math.tan(math.radians(16.0))))).normalized()   # from her side, 16 deg up
            o.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def _raised_arm(PK, k, fwd, up, u=1.0, tremble=0.0):
    """S20bot v2's end pose: the left forearm up toward Wren at face height, the inner wrist turned out; the right
    hand down at his side (the shrimp on it)."""
    side = X._side_vec(k)
    waist = E2._bone_world(k, "chest") + fwd * 0.75 - up * 2.1 + side * -0.75
    X._reach(PK, k, "R", waist)
    shoulder = E2._bone_world(k, "upper_arm.L")
    low = E2._bone_world(k, "chest") + fwd * 1.1 - up * 0.6 + side * 0.3
    high = shoulder + fwd * 2.2 + up * (1.5 + tremble) + side * -0.25
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
    d = (X.WREN_STOP - X.KAI_AT).normalized()
    _late_afternoon(Vector((d.x, d.y, 0)).normalized())
    k = X._kai()
    fwd = Vector((d.x, d.y, 0)).normalized()
    up = Vector((0, 0, 1))
    w0 = X.WREN_STOP + fwd * 0.75                                    # where S20bot v2 leaves her (half a step back)
    w = X._wren(w0, X.WREN_YAW)
    PK, PW = x3.Pose(k), x3.Pose(w)
    feet = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}

    # Wren: a stumble two steps back (anticipation, a heel catch, arms out), then she holds the bell up, trembling
    steps = [(1, 0.0), (5, 0.55), (9, 1.0), (13, 1.55), (17, 1.75), (21, 1.8)]   # (frame, distance back)

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
        if stumbling:                                                # the free arm out a little for balance
            PW.aim("upper_arm.L", (0.45, 0.05, -0.85 + 0.15 * math.sin(f * 0.7)))
            PW.aim("forearm.L", (0.4, -0.2, -0.7))
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
    E2._face({"eye_brow_down": 0.9, "face_angry": 0.45, "mouth_wide": 0.35, "eye_zitome": 0.2}, 1)   # nervous, defiant
    E2._face({"eye_brow_down": 0.4, "face_sad": 0.3, "mouth_short": 0.4}, f_so)   # "So I did.": a wince at what it cost

    # the shrimp: on his right hand at his side, then a hop up onto his left shoulder ("So I did.")
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    sh["root"].scale = (0.5,) * 3                                     # helper 3's SHRIMP_K (it rides there from S02)
    sh["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW))      # facing out, with him
    sc = bpy.context.scene
    f_hop0, f_hop1 = f_so - 14, f_so - 2                             # crouch, jump, land (on his shoulder by ~f30)
    base = Vector(sh["root"].scale)
    for f in range(1, n + 1):
        sc.frame_set(f)
        hand = X._world_of(k, "hand.R") + up * 0.3
        perch = E2._bone_world(k, "upper_arm.L") + up * 0.34 + fwd * 0.1 + X._side_vec(k) * 0.5   # helper 3's
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

    # the villagers: behind Kai (on the meadow past him, clear of the pond), flinching, then scattering sideways and
    # away, nets dropping
    sc.frame_set(1)
    L = Vector((-fwd.y, fwd.x, 0))                                    # Kai's left
    SPOTS = [(13.0, -7.5), (16.0, -3.0), (14.5, 3.5), (18.5, 8.0), (21.0, -10.5), (22.5, 1.0), (12.0, 9.5)]
    for i, (dx, y0, delay, has_net, bell) in enumerate(h1.VILLAGERS):
        v = h1.villager(i, 11 + i * 7, net=has_net, bell=bell)
        back_d, side_d = SPOTS[i]
        p0 = X.KAI_AT - fwd * back_d + L * side_d
        dd = (X.KAI_AT - p0)
        dd.z = 0
        dd = dd.normalized()                                         # facing Kai
        face_in = math.atan2(dd.x, -dd.y)
        run = (-dd * 0.6 + L * (1.0 if side_d >= 0 else -1.0)).normalized()
        face_out = math.atan2(run.x, -run.y)
        f_flinch = 1 + i % 3 * 2
        f_turn0 = f_flinch + 3
        f_run = f_turn0 + 5
        for f in range(1, n + 1, 2):
            if f < f_run:
                p = p0 - dd * (0.25 if f >= f_flinch else 0.0)
            else:
                p = p0 - dd * 0.25 + run * 0.5 * (f - f_run) * min(1.0, (f - f_run) / 6.0)
            p.z = h1.hill_height(p.x, p.y)
            anim.key(v["root"], "location", f, tuple(p), "CONSTANT")
            u = _smooth((f - f_turn0) / 5.0)
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

    LAST.update(k=k, w=w, sh=sh, fwd=fwd, up=up, w0=w0)
    # camera: low, over Wren's left shoulder, looking up at Kai's face and raised wrist (she stumbles back toward the
    # lens: her hood and bell soft in the near foreground); a slow push-in on 1s
    LAST.update(k=k, w=w, sh=sh, fwd=fwd, up=up, w0=w0)
    sc.frame_set(1)
    bpy.context.view_layer.update()
    wrist = H9._forearm(k, H9.MARK_U)
    khead = s3d.kai_point(k, "eyes")
    c0 = w0 + fwd * float(os.environ.get("S01_BACK", "4.5")) - L * float(os.environ.get("S01_SIDE", "4.0")) \
        + up * float(os.environ.get("S01_H", "4.5"))
    t0 = wrist.lerp(khead, float(os.environ.get("S01_AIM", "0.4"))) - up * float(os.environ.get("S01_DROP", "0.6"))
    c1 = c0.lerp(t0, 0.06)
    cam = _cam_from("S01cam", n, c0, c1, t0, t0, float(os.environ.get("S01_LENS", "40")))

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
        lt.location = m.lerp(s3d.kai_point(k, "eyes"), 0.35) + (cam.matrix_world.translation - m).normalized() * 0.45
        lt.keyframe_insert("location", frame=f)
        lvl = 1.15 + 0.12 * math.sin(f / 4.0)
        ld.energy = S01_LIGHT * lvl
        ld.keyframe_insert("energy", frame=f)
        marks[f] = dict(H9._mark_geo(k, cam), level=round(lvl, 3), vis=_visible(cam, m, k["arm"], 1.0),
                        w_eye_l=H9._px(cam, s3d.kai_point(w, "eye_l")), w_eye_r=H9._px(cam, s3d.kai_point(w, "eye_r")))
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "S01_mark.json"), "w") as fh:
        json.dump(dict(meta=dict(f_so=f_so, f_fear=1, wren_eyes=False), frames=marks), fh)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]],
                beats=dict(so=f_so, hop=(f_hop0, f_hop1)))


# ------------------------------------------------------------------------------------------------------------ S11
S11_BG = "#0e1430"                                # the night ground (dark blue, the island's night tone)
S11_ORB = "#ff8466"                               # the glow: the mark's coral


def s11():
    from channels.monsters.diorama_ep02.helper4 import _backdrop
    from channels.monsters.diorama_ep02.helper9 import _px
    from channels.monsters.mk import diorama, fluffmoth as fm, look
    n = _frames("S11", 92)
    W = _words("l11", [("moths", 8, 15), ("they", 51, 55), ("backs", 63, 69)])
    fw = {}
    for w_, a_, b_ in W:
        fw.setdefault(w_, []).append((a_, b_))
    f_they = fw["they"][0][0]                                        # 51
    f_backs = fw["backs"][0][0]                                      # 63
    diorama.setup()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    sc.world.mist_settings.start, sc.world.mist_settings.depth = 500.0, 100.0
    for o in list(sc.objects):                                       # night: the sun down to a faint cool fill
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy *= 0.12
            o.data.color = (0.6, 0.7, 1.0)
    origin = Vector((0.0, -20.0, 0.0))
    _backdrop(S11_BG).location = origin + Vector((0, 0, -6.0))

    def P(sx, sz, depth=0.0):                                        # screen-right / up in the side view
        return origin + Vector((depth, -sx, sz))

    light = P(2.4, 9.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=light, segments=32, ring_count=16)
    orb = bpy.context.object
    orb.name = "s11_orb"
    orb.data.materials.append(look.flat("s11_orb", look.hexc("#ffe3d8"), 4.0))
    ld = bpy.data.lights.new("s11_orb_light", "POINT")
    ld.color, ld.energy, ld.shadow_soft_size = look.hexc(S11_ORB)[:3], 1400.0, 0.4
    lo = bpy.data.objects.new("s11_orb_light", ld)
    sc.collection.objects.link(lo)
    lo.location = light

    m = fm.build((0, 0, 0), name="s11moth")
    fm.flight_mode(m)
    m["root"].scale = (2.35,) * 3                                    # the biggest thing in frame
    fm.flap(m)
    # its path: level flight to screen right; from "They" its back tilts to the light (amount 0 -> 1 by "backs"+6)
    # and the tilt turns it: the heading swings round the light (an orbit starting)
    pos = P(-5.0, 2.4)
    speed = 0.15
    heading = Vector((0, -1, 0))                                     # screen right
    prev = None
    track = {}
    for f in range(1, n + 1):
        amt = _smooth((f - f_they) / max(1, f_backs + 6 - f_they))
        if f > 1:
            to_l = light - pos
            r = max(1.0, to_l.length)
            turn = amt * speed / r                                   # radians a frame: the tilt bends the path
            ax = Vector((1, 0, 0))                                   # the side view's normal (turn in the YZ plane)
            # turn the heading toward the light's side (counter-clockwise on screen when the light is above)
            from mathutils import Matrix
            sign = 1.0 if heading.cross(to_l).x > 0 else -1.0
            heading = (Matrix.Rotation(sign * turn, 3, ax) @ heading).normalized()
            pos = pos + heading * speed
        bob = 0.08 * math.sin(f * 0.5)
        track[f] = (pos + Vector((0, 0, bob)), heading.copy(), amt)
    for f in range(1, n + 1, 2):
        p, h, amt = track[f]
        m["root"].location = p
        m["root"].keyframe_insert("location", frame=f)
        prev = fm.back_to(m, f, light, h, amount=amt, prev=prev)
    for fc in anim.all_fcurves(m["root"].animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    fm.spot_blink(m, 30) if hasattr(fm, "spot_blink") else None

    # the camera: side-on from -X, level, a long lens, a slow push-in on 1s; everything above the caption band
    tgt = P(1.0, 5.6)
    az = math.radians(float(os.environ.get("S11_AZ", "30")))          # swung toward the moth's front: the wings
    el = math.radians(float(os.environ.get("S11_EL", "20")))           # show their faces, not edge-on
    bpy.ops.object.camera_add(location=tgt + 52.0 * Vector((-math.cos(az) * math.cos(el), -math.sin(az) * math.cos(el),
                                                             math.sin(el))))
    cam = bpy.context.object
    cam.name = "S11cam"
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = float(os.environ.get("S11_LENS", "52"))
    cam.data.shift_y = float(os.environ.get("S11_SHIFT", "-0.04"))
    cam.data.clip_end = 400
    sc.camera = cam
    c0 = cam.location.copy()
    for f in range(1, n + 1):
        cam.location = c0.lerp(tgt, 0.06 * _smooth((f - 1) / max(1, n - 1)))
        cam.keyframe_insert("location", frame=f)

    # the 2D pass's anchors: the light, the moth's body and its back (a point on the body's top)
    anchors = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        R = m["root"].matrix_world
        body = R.translation
        back = R @ Vector((0, 0, 0.55))
        anchors[f] = dict(light=_px(cam, light), body=_px(cam, body), back=_px(cam, back), r_orb=_px(
            cam, light + Vector((0, 0, 0.42))))
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "S11_anchors.json"), "w") as fh:
        json.dump(dict(meta=dict(f_they=f_they, f_backs=f_backs), frames=anchors), fh)
    sc.frame_set(1)
    return dict(frames=n, step=1, subject=[m["root"]], beats=dict(they=f_they, backs=f_backs))


SHOTS = {"S01": s01, "S11": s11}
