"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md): XprL's Wren shots.

    S17 "A girl with a bell walked straight up to me." Over Kai's right shoulder (his back, the cap, the cupped
        hands out of sight): Wren comes up the path from the south, marching, the bell swinging in her right fist (it
        rings on her first steps), straight at him; she plants her feet in front of him with a little overshoot,
        chin up, stern. Slow push-in on 1s; characters on 2s.
    S18 "Step away from the snapper. It goes in the lake." (Wren's voice) Close on Wren, stern, speaking (mouth flaps
        from the line's text); behind her a villager holds a long-handled net up, ready. Push-in on 1s.
    S20top (A) "Option A: hand it over." Kai lowers the cupped shrimp into the net Wren holds out; she nods once.

Staging (shared with S16/S19/S20 B): Kai stands on the pond's north-east shore at KAI_AT holding the shrimp in his
cupped hands, facing WREN_FROM (the path from the south, where the villagers come over); Wren stops at WREN_STOP,
6.5 units (1.3 m) in front of him, facing him.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S17 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as v2
from channels.monsters.diorama_v3 import bgqrs as b3
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import diorama, hero, wren

SCALE = 5.8                                         # hero.blend / wren: 1.5 m model -> creature units (20 cm)
KAI_AT = Vector((5.0, -3.5, 0.0))                   # the pond's east shore, just south of the shrimp's drinking spot
WREN_FROM = Vector((-0.5, -23.0, 0.0))              # the top of the path from the south (the villagers' side)
QUIET_STUMPS = ((4.1, -14.6), (7.2, -9.9))           # grove stumps by Wren's path: no smoke left by Episode 2
BLUR, HAZE = 4.0, (2.5, 2.0)                        # character shots: a gentle tilt-shift, haze well behind them
_d = (WREN_FROM - KAI_AT).normalized()
WREN_STOP = KAI_AT + _d * 6.5                       # where she plants her feet, facing Kai
KAI_YAW = math.degrees(math.atan2(_d.x, -_d.y))     # rot_z so -Y (the model's front) points along _d
WREN_YAW = math.degrees(math.atan2(-_d.x, _d.y))


def _frames(shot, fallback):
    from channels.monsters.diorama_ep02.shots import ep02_frames        # lazy: shots.py imports this module
    try:
        return ep02_frames(shot)
    except (OSError, KeyError, ValueError):                              # timing.json not in yet
        return fallback


def _cam_move(name, n, a, b, f0=1, f1=None):
    """diorama/xprl._move (a camera move on 1s, poses (target, dist, tilt, yaw, lens, shift_y)) with this module's
    gentler blur and farther haze, so both characters stay readable."""
    old = v2.BLUR
    v2.BLUR = BLUR
    try:
        cam = v2._move(name, f0, f1 or n, a, b, n)
    finally:
        v2.BLUR = old
    ms = bpy.context.scene.world.mist_settings
    ad = bpy.context.scene.world.animation_data
    for f in range(1, n + 1):
        k = (f - f0) / max(1, (f1 or n) - f0)
        k = max(0.0, min(1.0, k))
        d = a[1] + (b[1] - a[1]) * (k * k * (3 - 2 * k))
        ms.start, ms.depth = d * HAZE[0], d * HAZE[1]
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    del ad
    return cam


def _world(n):
    """The island as Episode 1 left it (diorama_v3/bgqrs._set: the cut grove's stumps), no Kai lying down."""
    diorama.setup()
    b3._set(n)
    for o in list(bpy.data.objects):                                     # the stumps on Wren's path have burnt out
        if o.name.startswith("puff") and o.type == "EMPTY" and o.parent is None:
            x, y = o.location.x, o.location.y
            if any(math.hypot(x - sx, y - sy) < 1.5 for sx, sy in QUIET_STUMPS):
                for ch in o.children:
                    ch.hide_render = True
                o.hide_render = True
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n


def _kai(cupped=True):
    """Kai standing at KAI_AT facing Wren, the shrimp cupped in both hands at his chest (a slow breath)."""
    k = hero.load((0, 0, 0), scale=SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    k["arm"].rotation_euler = (0, 0, math.radians(KAI_YAW))
    k["arm"].location = KAI_AT
    bpy.context.view_layer.update()
    return k


def _cup(P):
    """Both hands cupped together in front of the chest (the shrimp in them)."""
    for sx, s in (("L", 1), ("R", -1)):
        P.aim(f"upper_arm.{sx}", (s * 0.12, -0.35, -1))
        P.aim(f"forearm.{sx}", (-s * 0.55, -0.85, 0.25))
        P.aim(f"hand.{sx}", (-s * 0.45, -0.9, -0.05))


def _wren(at, yaw):
    w = wren.load((0, 0, 0), scale=SCALE)
    w["arm"].rotation_euler = (0, 0, math.radians(yaw))
    w["arm"].location = at
    bpy.context.view_layer.update()
    return w


# ------------------------------------------------------------------------------------------------------------ S17
def _villagers_s17(n, s16_frames=None):
    """helper 1's villagers (S16) carrying on down the path behind Wren: from where S16 leaves them they keep
    marching (0.3 units a frame), slowing to a stop as a loose group well behind her; bells still swinging."""
    from channels.monsters.diorama_ep02 import helper1 as h1
    from channels.monsters.mk import anim
    n16 = s16_frames or _frames("S16", 47)
    out = []
    for i, (dx, y0, delay, has_net, bell) in enumerate(h1.VILLAGERS):
        v = h1.villager(i, 11 + i * 7, net=has_net, bell=bell)
        x0 = diorama._path_x(y0) + dx
        target = Vector((KAI_AT.x + dx * 0.4, KAI_AT.y - 6.0, 0))
        d = (target - Vector((x0, y0, 0))).normalized()
        v["root"].rotation_euler.z = math.atan2(d.x, -d.y)
        t_s16 = max(0, n16 - delay)                                # how far S16 walked it
        stop_at = 16.0 + 2.2 * i                                   # units short of Wren's stop (a loose group)
        max_walk = max(0.0, (target - Vector((x0, y0, 0))).length - stop_at)
        for f in range(1, n + 1, 2):
            # 0.3 units a frame, easing to a halt over the shot's first ~40 frames
            u = min(1.0, f / 30.0)                                 # they stop on the rise, watching her go on
            extra = 0.3 * 30.0 * (u - u * u / 2)
            walk = min(max_walk, 0.3 * t_s16 + extra)
            p = Vector((x0, y0, 0)) + d * walk
            p.z = h1.hill_height(p.x, p.y)
            anim.key(v["root"], "location", f, tuple(p), "CONSTANT")
            ph = (t_s16 + f) * 0.42 * (1 - u * 0.8) + i
            anim.key(v["body"], "location", f, (0, 0, 0.22 * abs(math.sin(ph)) * (1 - u * 0.7)), "CONSTANT")
            if v["bell"] is not None:
                anim.key(v["bell"], "rotation_euler", f, (0.55 * math.sin((n16 + f) * 1.3 + i) * (1 - u * 0.6), 0, 0),
                         "CONSTANT")
        out.append(v)
    return out


def s17():
    n = _frames("S17", 84)
    _world(n)
    from channels.monsters.diorama_ep02 import helper1 as h1
    h1.hill()
    _villagers_s17(n)
    k = _kai()
    PK = x3.Pose(k)
    for f in range(1, n + 1, 2):                                     # Kai holds still, breathing (his back to us)
        PK.reset()
        _cup(PK)
        PK.rot("chest", (2 * math.sin(f / 18.0), 0, 0))
        PK.rot("head 1", (-4, 3 * math.sin(f / 30.0), 0))
        PK.key(f)
    w = _wren(WREN_FROM, WREN_YAW)
    PW = x3.Pose(w)
    dist = (WREN_STOP - WREN_FROM).length / SCALE                    # armature units (model metres)
    f_stop = max(30, n - 25)                                          # planted on "...up to me"
    ring_until = 20

    def upper(P, t):
        f = 1 + t * (f_stop - 1)
        swing = math.sin(f / 3.0) * 6
        wren.hold_bell(P, 0.25, shake=(18 * math.sin(f * 1.6)) if f < ring_until else swing)
        P.rot("chest", (-4, 0, 0))
        P.rot("head 1", (-6, 0, 0))                                   # chin up
    feet = wren.march(w, PW, ((0, 0, 0), (0, -dist, 0)), 1, f_stop, step_len=0.31, upper=upper, every=2)
    mid = (feet["L"] + feet["R"]) / 2
    for f, lean, chin, sink in ((f_stop + 2, 7, -6, 0.035), (f_stop + 6, -3, -3, 0.02), (f_stop + 10, 0, -2, 0.012),
                                (n, 0, -2, 0.012)):
        PW.reset()                                                   # planted: overshoot forward, settle back,
        PW.hips(Vector((mid.x, mid.y, -sink)))                       # knees giving a little on the stop
        for side in ("L", "R"):
            PW.leg(side, feet[side] + Vector((0, 0, PW.ankle_h)))
        wren.hold_bell(PW, 0.45)
        PW.rot("chest", (lean, 0, 0))
        PW.rot("head 1", (chin, 0, 0))
        PW.key(f)
    wren.grip(w, 1)
    wren.ring(w, 1, ring_until)
    wren.face(w, "stern", 1)
    wren.face(w, "stern", f_stop + 2, value=1.0)
    wren.blink(w, 1, f_stop - 14, every=(200, 201), at=(18,))       # one blink mid-march; eyes open on Kai at the end
    wren.contact_shadows(w)
    v2._twos([k["arm"], w["arm"]])
    # camera: over Kai's right shoulder toward where she stops; a slow push-in on 1s
    tgt = WREN_STOP + Vector((0, 0, 5.2))
    back = (KAI_AT - WREN_STOP).normalized()
    side = Vector((back.y, -back.x, 0))
    cdir = (back - side * 0.33).normalized()                          # west of him: the smoking stumps stay off-frame
    yaw = math.degrees(math.atan2(-cdir.x, -cdir.y))
    _cam_move("S17cam", n, (tuple(tgt), 17.0, 9.0, yaw, 42.0, 0.0), (tuple(tgt), 15.2, 9.0, yaw, 42.0, 0.0))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"]])


SHOTS = {"S17": s17}


# ------------------------------------------------------------------------------------------------------------ props
def _line_words(lid):
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep02", "timing.json")
    d = json.load(open(p))
    line = next(ln for ln in d["lines"] if ln["id"] == lid)
    return line["words"]


def _shot_start(shot):
    import json
    import os
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep02", "timing.json")
    return next(s["start"] for s in json.load(open(p))["shots"] if s["shot"] == shot)


def net(name, length=13.0, hoop=1.6, depth=2.2):
    """A villager's long-handled net (creature units): a wooden pole along +Z from the origin (the grip end), a hoop
    at its top in the pole's XZ plane, and a loose cord bag hanging from the hoop (a wireframe cone). Returns the
    root empty (rotate/move it); toon look with outlines."""
    from channels.monsters.mk import look, sdf
    wood = look.toon("net_pole", look.hexc("#9a6a3c"))
    rim = look.toon("net_hoop", look.hexc("#6a4a2c"))
    cord = look.toon("net_cord", look.hexc("#efe3c2"))
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)
    pole = sdf.build(f"{name}_pole", [(sdf.C(Vector((0, 0, 0)), Vector((0, 0, length)), 0.16, 0.14), wood.name,
                                       None)], k=0.01, res=0.06, pad=0.2, smooth_iter=2)
    parts = []
    c = Vector((0, 0, length + hoop))
    for i in range(24):
        a0, a1 = 2 * math.pi * i / 24, 2 * math.pi * (i + 1) / 24
        p0 = c + Vector((hoop * math.cos(a0), 0, hoop * math.sin(a0)))
        p1 = c + Vector((hoop * math.cos(a1), 0, hoop * math.sin(a1)))
        parts.append((sdf.C(p0, p1, 0.09, 0.09), rim.name, 0.02))
    ring = sdf.build(f"{name}_hoop", parts, k=0.02, res=0.04, pad=0.2, smooth_iter=2)
    bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=hoop * 0.98, radius2=0.25, depth=depth, end_fill_type="NOTHING")
    bag = bpy.context.object
    bag.name = f"{name}_bag"
    bag.rotation_euler = (math.radians(-90), 0, 0)               # its wide end on the hoop, hanging along +Y
    bag.location = c + Vector((0, depth / 2, 0))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    me = bag.data
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=3, use_grid_fill=True)
    for v in bm.verts:                                     # a slack, sagging bag
        t = (v.co.y - c.y) / depth
        v.co.z -= 0.6 * t * t * hoop
    bm.to_mesh(me)
    bm.free()
    me.materials.append(cord)
    wf = bag.modifiers.new("cords", "WIREFRAME")
    wf.thickness = 0.06
    wf.use_replace = True
    for o in (pole, ring, bag):
        o.parent = root
        look.outline(o, 0.03)
    return root


# ------------------------------------------------------------------------------------------------------------ S18
def s18():
    """Close on Wren (Kai's eyeline), stern, speaking her line on the word timings; a villager's net raised behind
    her. A lean in on "Step away", a glance toward the lake on "lake"."""
    n = _frames("S18", 86)
    _world(n)
    t0 = _shot_start("S18")
    words = _line_words("l18")
    fr = {w["w"].strip(".").lower(): int(round((w["start"] - t0) * 24)) + 1 for w in words}
    w = _wren(WREN_STOP, WREN_YAW)
    feet = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}
    P = x3.Pose(w)
    f_step, f_lake = fr.get("step", 8), fr.get("lake", 60)
    for f in range(1, n + 1, 2):
        P.reset()
        lean = 4 if f_step <= f < f_step + 14 else 0                   # leans in on "Step away"
        nod = 6 if f_step + 2 <= f < f_step + 8 else 0
        turn = 22 if f_lake - 2 <= f < f_lake + 14 else 0              # a glance toward the lake
        for side in ("L", "R"):
            P.leg(side, feet[side] + Vector((0, 0, P.ankle_h)))
        wren.hold_bell(P, 0.12)
        P.rot("chest", (lean + 1.2 * math.sin(f / 20.0), 0, 0))
        P.rot("head 1", (-6 + nod, 0, -turn))
        P.key(f)
    wren.grip(w, 1)
    wren.face(w, "stern", 1)
    wren.talk_words(w, words, t0)
    wren.blink(w, 1, n, at=(fr.get("it", 46) - 4,))
    wren.contact_shadows(w)
    v2._twos([w["arm"]])
    back = (KAI_AT - WREN_STOP).normalized()                           # toward Kai (the camera side)
    side = Vector((back.y, -back.x, 0))
    from channels.monsters.diorama_ep02 import helper1 as h1
    from channels.monsters.mk import anim
    h1.hill()
    v = h1.villager(1, 18, net=True, bell=False)                       # S16/S17's net-carrier, right behind her
    v["root"].location = WREN_STOP - back * 8.0 - side * 6.0          # behind her, off her shoulder, in view
    v["root"].rotation_euler.z = math.atan2(back.x, -back.y)
    for f in range(1, n + 1, 2):                                       # a ready, slightly impatient sway
        anim.key(v["body"], "rotation_euler", f, (0, 0.04 * math.sin(f / 7.0), 0), "CONSTANT")
    tgt = WREN_STOP + Vector((0, 0, 6.6))
    yaw = math.degrees(math.atan2(-back.x, -back.y)) + 20.0           # a three-quarter view, her right side to us
    _cam_move("S18cam", n, (tuple(tgt), 8.6, 4.0, yaw, 45.0, 0.0), (tuple(tgt), 7.6, 4.0, yaw, 45.0, 0.0))
    return dict(frames=n, step=2, ones=(1, n), subject=[w["arm"]])


SHOTS["S18"] = s18


# ------------------------------------------------------------------------------------------------------------ S20top
SHRIMP_IN_HAND = 0.3          # fallback only: the shared value is helper4.SHRIMP_IN_HAND (one size for every shot)


def _shrimp_scale():
    try:
        from channels.monsters.diorama_ep02 import helper4        # lazy: helper4 imports this module's staging
        return helper4.SHRIMP_IN_HAND
    except (ImportError, AttributeError):
        return SHRIMP_IN_HAND


def _to_arm(rig, p):
    return rig["arm"].matrix_world.inverted() @ Vector(p)


def _world_of(rig, bone, tail=True):
    pb = rig["arm"].pose.bones[bone]
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _reach(P, rig, side, target_w, bend=(0, 0, -0.35)):
    """Point one arm at a world target: the upper arm toward it (a little down), then the forearm from the elbow."""
    sx = side
    T = _to_arm(rig, target_w)
    bpy.context.view_layer.update()
    sh = P.pb[f"upper_arm.{sx}"].head
    P.aim(f"upper_arm.{sx}", (T - sh).normalized() + Vector(bend))
    el = P.pb[f"forearm.{sx}"].head
    P.aim(f"forearm.{sx}", T - el)
    P.aim(f"hand.{sx}", (T - el).normalized() + Vector((0, 0, -0.3)))


def s20top():
    """Option A, the top panel: Kai lowers the cupped shrimp into the net Wren holds out between them, opens his
    hands, the shrimp drops into the bag (a bounce, the net sags), Wren's face softens and she nods once; Kai lets
    out a breath. Framed in the top half (y 80-600) for the split; slow push-in on 1s."""
    from channels.monsters.mk import anim, puffshrimp
    n = _frames("S20", 156)
    _world(n)
    t0 = _shot_start("S20")
    words = {w["w"].strip(".:").lower() + str(i): w for i, w in enumerate(_line_words("l20"))}
    f_over = int(round((words["over.4"]["start"] - t0) * 24)) + 1 if "over.4" in words else 40
    f_low0, f_low1 = 6, max(20, f_over - 4)                    # lowering on "Option A: hand it..."
    f_rel = f_over + 2                                         # the hands open on "over"
    k = _kai()
    w = _wren(WREN_STOP, WREN_YAW)
    PW, PK = x3.Pose(w), x3.Pose(k)
    feetW = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}
    feetK = dict(feetW)

    def wren_pose(P, lift=0.0, nod=0.0, f=1):
        P.reset()
        for sd in ("L", "R"):
            P.leg(sd, feetW[sd] + Vector((0, 0, P.ankle_h)))
        P.aim("upper_arm.L", (0.16, -0.72, -0.68))
        P.aim("forearm.L", (-0.04, -1.0, 0.06 + lift))
        P.aim("hand.L", (-0.05, -1.0, 0.0 + lift))
        P.aim("upper_arm.R", (-0.24, -0.22, -1))
        P.aim("forearm.R", (0.12, -0.75, -0.25 + lift * 0.6))
        P.aim("hand.R", (0.1, -0.6, -0.8))
        P.rot("chest", (4 + 1.0 * math.sin(f / 22.0), 0, 0))
        P.rot("head 1", (8 + nod, 0, 0))                          # eyes on the net
    # the net in Wren's hands: the pole through both hands, the hoop out in front between them
    wren_pose(PW)
    bpy.context.view_layer.update()
    hl, hr = _world_of(w, "hand.L"), _world_of(w, "hand.R")
    d = Vector(((hl - hr).x, (hl - hr).y, 0.0)).normalized()     # a level pole: the hoop lies flat
    L = (hl - hr).length + 2.2
    nr = net("S20net", length=L, hoop=1.35, depth=1.9)
    up = Vector((0, 0, 1))
    zr = d
    yr = (-up - zr * (-up).dot(zr)).normalized()                 # the hoop's normal points down: the bag hangs
    xr = yr.cross(zr)
    from mathutils import Matrix
    M = Matrix((xr, yr, zr)).transposed().to_4x4()
    origin = Vector((hr.x, hr.y, (hl.z + hr.z) / 2)) - d * 0.8
    nr.matrix_world = Matrix.Translation(origin) @ M
    hoop_c = origin + d * (L + 1.35)                           # the hoop's centre (net(): pole L, hoop radius 1.35)
    nr.keyframe_insert("location", frame=1)
    # Kai: cupped at his chest, lowering his hands over the hoop, opening them on "over", then a breath
    above = hoop_c + up * 0.7
    for f in range(1, n + 1, 2):
        u = smooth01((f - f_low0) / max(1, f_low1 - f_low0))
        PK.reset()
        for sd in ("L", "R"):
            PK.leg(sd, feetK[sd] + Vector((0, 0, PK.ankle_h)))
        PK.rot("chest", (10 * u + 1.5 * math.sin(f / 20.0), 0, 0))
        PK.rot("head 1", (16 * u, 0, 0))
        if u <= 0:
            _cup(PK)
        else:
            for sd, s_ in (("L", 1), ("R", -1)):
                open_ = 0.45 if f >= f_rel else 0.0
                tgt = above + _side_vec(k) * s_ * (0.28 + open_)
                tgt.z += (1 - u) * 1.6
                _reach(PK, k, sd, tgt)
        PK.key(f)
        wren_pose(PW, nod=10 if f_rel + 10 <= f < f_rel + 18 else 0, f=f)   # one nod once it's in
        PW.key(f)
    # the shrimp: in his cupped hands until "over", then it drops into the bag, bounces and settles, blinking
    sh = puffshrimp.build((0, 0, 0), name="s20puff")
    sh["root"].scale = (_shrimp_scale(),) * 3
    bag_pt = hoop_c - up * 0.9
    for f in range(1, n + 1):
        bpy.context.scene.frame_set(f)
        if f <= f_rel:
            p = (_world_of(k, "hand.L") + _world_of(k, "hand.R")) / 2 + up * 0.25
        else:
            a = (f - f_rel) / 24.0
            start = (_hands_mid_at(k, f_rel))
            z = start.z - 0.5 * 30.0 * a * a
            p = Vector((lerp(start.x, bag_pt.x, min(1, a * 3)), lerp(start.y, bag_pt.y, min(1, a * 3)), max(bag_pt.z, z)))
            if z < bag_pt.z:                                           # landed: a little bounce in the bag
                tl = a - math.sqrt(2 * (start.z - bag_pt.z) / 30.0)
                p.z = bag_pt.z + 0.35 * abs(math.sin(tl * 9.0)) * math.exp(-tl * 5.0)
        sh["root"].location = p
        sh["root"].keyframe_insert("location", frame=f)
    face_k = (WREN_STOP - KAI_AT).normalized()
    sh["root"].rotation_euler = (0, 0, math.atan2(face_k.x, -face_k.y))
    anim.blink(sh, f_rel + 20)
    hero.face(k, "sad", 1)
    hero.face(k, "relaxed", f_rel + 14)
    wren.face(w, "stern", 1)
    wren.face(w, "softer", f_rel + 8)
    wren.grip(w, 1, "R")
    wren.grip(w, 1, "L")
    wren.blink(w, 1, n, at=(f_rel + 30,))
    wren.contact_shadows(w)
    v2._twos([k["arm"], w["arm"]])
    # camera: side-on from the west, the pair in the top half (shift the frame down), a slow push-in on 1s
    mid = (KAI_AT + WREN_STOP) / 2
    tgt = mid + Vector((0, 0, 5.6))
    line_ = (WREN_STOP - KAI_AT).normalized()
    perp = Vector((-line_.y, line_.x, 0))
    if perp.x > 0:
        perp = -perp                                             # from the west
    yaw = math.degrees(math.atan2(-perp.x, -perp.y))
    _cam_move("S20Acam", n, (tuple(tgt), 15.0, 5.0, yaw, 32.0, -0.21), (tuple(tgt), 13.6, 5.0, yaw, 32.0, -0.21))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]])


def smooth01(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def _side_vec(rig):
    """Kai's left (+X of his armature) in world space."""
    return rig["arm"].matrix_world.to_3x3() @ Vector((1, 0, 0)) / rig["arm"].scale.x


def _hands_mid_at(rig, f):
    sc = bpy.context.scene
    cur = sc.frame_current
    sc.frame_set(f)
    p = (_world_of(rig, "hand.L") + _world_of(rig, "hand.R")) / 2 + Vector((0, 0, 0.25))
    sc.frame_set(cur)
    return p


SHOTS["S20top"] = s20top
