"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md): helper 5's shots (comedy and acting).

    S07 "Their wing dust stings like nettles."  (to come: needs helper 6's swarm, helper 1's night villagers, XprL's
        cape pose and helper 9's night grade)
    S15 "Every single moth landed on its back."  The laugh hold, straight on from S14's end: the grass round Kai
        is a field of fluffmoths on their backs (helper 6's upside_down: legs waving on 2s, eye-spots dazed and
        blinking out of step, a wriggle now and then). Kai lies as bGqrs's S13 left him (on his back, head west, the
        left wrist laid out palm up, the mark glowing), then on "landed" sits up among them, a little overshoot, and
        looks round at them, bewildered, then a small amazed half-smile; the shrimp on his left shoulder peeks out
        and stares. Camera low in front of him (east, toward his feet), the moths big in the foreground; a slow
        push-in on 1s; characters on 2s.
    S19bot "Option B: leave at sunrise, like they said."  The bottom panel of the split (rows 486-1280 rendered, as
        Ep 2's S20bot; helper 8 crops it under the jagged divider). Dawn: the low sun just up in the east, long
        shadows, a pink-gold sky. Kai walks away from us up the dirt track out of the bell-keepers' village (helper 9's
        Ep 2 village on the south shore), between the last huts toward the meadow, the shrimp riding on his left
        shoulder. On "like they said" he stops and looks back over his right shoulder at the village once (the shrimp
        turns round on his left shoulder to look too), then faces front and walks on. A slow push after him on 1s; characters on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S19bot OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Euler, Matrix, Vector

from channels.monsters.diorama_ep02 import helper9 as H9              # village_and_lake, VILLAGE, _shore
from channels.monsters.diorama_ep02 import xprl as X                  # SCALE, _world, Kai
from channels.monsters.ep01v2 import bgqrs as s3d                     # _fix_pivots
from channels.monsters.ep01v2 import xprl as x3                       # Pose, _walk, _arms_down
from channels.monsters.mk import acting, anim, diorama, hero, look, puffshrimp

BLUR = 5.0
try:                            # the puff-shrimp on his shoulder: helper 4's size and perch (S01's hop lands it there)
    from channels.monsters.diorama_ep02.helper4 import SHRIMP_IN_HAND as SHRIMP_SHOULDER
except ImportError:
    SHRIMP_SHOULDER = 0.6
LAST = {}


def _frames(shot, fallback):
    from channels.monsters.diorama_ep03.shots import ep03_frames       # lazy: shots.py imports this module
    try:
        return ep03_frames(shot)
    except (OSError, KeyError, ValueError):                              # timing.json not in yet
        return fallback


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _cam(name, f0, f1, a, b, lens, blur=BLUR, haze=(2.5, 2.0), shift_y=0.0):
    """A camera move on 1s from pose a to pose b (each (target, dist, tilt, yaw)), eased; tilt-shift and haze re-solved
    every frame (diorama.camera's conventions: yaw 0 looks north, the camera sits behind the target)."""
    sc = bpy.context.scene
    cam = diorama.camera(name, a[0], dist=a[1], tilt=a[2], yaw=a[3], lens=lens, blur=blur, frame=f0)
    cam.data.clip_start = 0.1
    cam.data.shift_y = shift_y
    for f in range(f0, f1 + 1):
        u = _ease((f - f0) / max(1, f1 - f0))
        t = Vector(a[0]).lerp(Vector(b[0]), u)
        d = a[1] + (b[1] - a[1]) * u
        el, az = math.radians(a[2] + (b[2] - a[2]) * u), math.radians(a[3] + (b[3] - a[3]) * u)
        back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        cam.location = t + back * d
        cam.rotation_euler = (math.pi / 2 - el, 0, -az)
        cam.data.dof.focus_distance = d
        cam.data.dof.aperture_fstop = diorama.fstop_for(d, lens, blur)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        ms = sc.world.mist_settings
        ms.start, ms.depth = d * haze[0], d * haze[1]
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return cam


# ------------------------------------------------------------------------------------------------- the shrimp
def shrimp_on_shoulder(k, side="L", yaw=0.0, name="ep03_shrimp"):
    """The puff-shrimp sitting on top of Kai's shoulder (bone-parented to shoulder.<side>, so it rides every move),
    facing his front turned by `yaw` degrees (+ = toward his left). Returns the rig."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    s3d._fix_pivots(sh)
    arm = k["arm"]
    sc = bpy.context.scene
    sc.frame_set(1)
    bpy.context.view_layer.update()
    b = arm.data.bones[f"shoulder.{side}"]
    fwd = arm.matrix_world.to_3x3().normalized() @ Vector((0, -1, 0))
    perch = arm.matrix_world @ arm.pose.bones[f"upper_arm.{side}"].head + Vector((0, 0, 0.75)) - fwd * 0.1
    root = sh["root"]
    root.scale = (SHRIMP_SHOULDER,) * 3
    yaw_w = arm.matrix_world.to_euler().z + math.radians(yaw)
    root.rotation_euler = (0, 0, yaw_w)
    root.location = perch                                                # helper 4's S01 perch
    bpy.context.view_layer.update()
    mw = root.matrix_world.copy()
    root.parent = arm
    root.parent_type = "BONE"
    root.parent_bone = b.name
    bpy.context.view_layer.update()
    root.matrix_world = mw
    for e in sh["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
    return sh


def _shrimp_parts(sh):
    return [sh["root"], sh["body"], sh["shoulder"], sh["hinge"]] + list(sh["eyes"]) + list(sh.get("lids", []))


def _word(lid, w, shot="S19"):
    """The shot frame (1-based) where word `w` of line `lid` starts (ep03/timing.json)."""
    import json
    from channels.monsters.diorama_ep03 import shots as S
    with open(S._T) as fh:
        d = json.load(fh)
    start = next(s["start"] for s in d["shots"] if s["shot"] == shot)
    line = next(ln for ln in d["lines"] if ln["id"] == lid)
    t = next(x["start"] for x in line["words"] if x["w"].strip(".,:!?").lower() == w.lower())
    return int(round((t - start) * d.get("fps", 24))) + 1


def _path_strip(name, pts, width=2.6, z=0.05):
    """A dirt path (helper 9's track colour) along the polyline `pts`."""
    import bmesh
    bm = bmesh.new()
    prev = None
    for a, b in zip(pts[:-1], pts[1:]):
        dv = (b - a)
        nv = Vector((-dv.y, dv.x, 0)).normalized() * width
        l0, r0 = prev if prev else (bm.verts.new(a + nv + Vector((0, 0, z))), bm.verts.new(a - nv + Vector((0, 0, z))))
        l1, r1 = bm.verts.new(b + nv + Vector((0, 0, z))), bm.verts.new(b - nv + Vector((0, 0, z)))
        bm.faces.new((l0, r0, r1, l1))
        prev = (l1, r1)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(bpy.data.materials.get("h9_dirt") or look.toon("h5_dirt", look.hexc("#c9a873")))
    return o


# ------------------------------------------------------------------------------------------------------ S15
S15_MOTH_SCALE = 0.42                                                    # bGqrs's S13 swarm size


def _s15_landings(B, wrist, hips, hd, n_moths=34, seed=15):
    """Where the moths lie: helper 10's S14 landing spots if they are in (build/monsters/diorama_ep03/
    S14_landings.json), else a rough ring round Kai within ~1.5-9 units of his wrist and body, with a few big ones
    toward the camera (east, past his feet). Returns [(x, y, yaw, scale)]."""
    import json
    import os
    import random
    pth = os.path.join(B.BUILD, "S14_landings.json")
    if os.path.exists(pth):
        with open(pth) as fh:
            d = json.load(fh)
        pts = d.get("landings", d) if isinstance(d, dict) else d
        out = []
        for q in pts:
            if isinstance(q, dict):
                out.append((q["x"], q["y"], q.get("yaw", 0.0), q.get("scale", S15_MOTH_SCALE)))
            else:
                out.append((q[0], q[1], q[2] if len(q) > 2 else 0.0, q[3] if len(q) > 3 else S15_MOTH_SCALE))
        return out
    rnd = random.Random(seed)
    feet = hips - hd * 4.5                                               # his feet: east of the hips
    out = []
    tries = 0
    while len(out) < n_moths and tries < 5000:
        tries += 1
        c = rnd.choice((wrist, wrist, hips, feet))
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(1.6, 7.5)
        p = c + Vector((math.cos(a) * r, math.sin(a) * r, 0))
        if (p - hips).length < 2.2 or (p - (hips + hd * 2.8)).length < 1.8:  # not on his body or head
            continue
        if any((p - Vector((q[0], q[1], 0))).length < 1.7 for q in out):
            continue
        out.append((p.x, p.y, rnd.uniform(-math.pi, math.pi), S15_MOTH_SCALE * rnd.uniform(0.85, 1.12)))
    return out


def s15():
    from channels.monsters.diorama_ep03 import bgqrs as B
    from channels.monsters.ep01v2 import helper10 as s15p
    from channels.monsters.mk import fluffmoth
    n = _frames("S15", 106)
    f_up = _word("l15", "landed", shot="S15") - 3                        # he sits up on "landed"
    X._world(n)
    B._night()
    sc = bpy.context.scene
    try:
        H9.village_and_lake()
    except Exception as e:                                               # the set is optional for a test still
        print("S15: no village", e)
    hd = B._head_dir()
    yaw = math.pi + math.radians(B.S13_HEAD)
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    rot_lie = (math.radians(90.0), 0, yaw)
    s15p._pose(k, B._with_arm(B.LIE, 1.0), (0, 0, 0), rot_lie)
    twist = B._twist_for_palm_up(k)[0]
    UP = [(nm, d) for nm, d in B.SIT if not nm.startswith("left_upper_arm") and not nm.startswith("left_lower_arm")
          and nm != "left_hand"] + [("left_upper_arm", (-0.45, 0.55, -0.35)), ("left_lower_arm", (-0.2, 0.9, 0.1)),
                                    ("left_hand", (-0.1, 0.9, 0.2))]   # sitting up, the left hand on his knee
    lie = B._with_arm(B.LIE, 1.0)
    # (frame, spec, theta (90 = flat on his back), arm-out amount)
    keys = [(1, lie, 90.0, 1.0), (f_up, lie, 90.0, 1.0), (f_up + 6, B._blend(lie, UP, 0.7), 40.0, 0.4),
            (f_up + 10, UP, 2.0, 0.0), (f_up + 14, UP, 10.0, 0.0), (n, UP, 10.0, 0.0)]
    back = 3.0                                                           # the hips stay where S13 laid them
    for f in range(1, n + 1, 2):
        i = max(j for j in range(len(keys)) if keys[j][0] <= f)
        if i + 1 < len(keys):
            a, b = keys[i], keys[i + 1]
            u = _ease((f - a[0]) / max(1, b[0] - a[0]))
        else:
            a = b = keys[-1]
            u = 1.0
        spec = B._blend(a[1], b[1], u)
        theta = a[2] + (b[2] - a[2]) * u
        v = a[3] + (b[3] - a[3]) * u
        look = 0.0
        if f > f_up + 14:                                               # looking round: left, right, then front
            t = f - (f_up + 14)
            look = 0.55 * math.sin(min(1.0, t / 40.0) * 2 * math.pi) * (1 - _ease((t - 40) / 12))
        r = Euler((math.radians(theta), 0, yaw)).to_matrix()
        s15p._pose(k, [x for x in spec if x[0] != "left_hand"], (0, 0, 0), (math.radians(theta), 0, yaw))
        if v > 0:
            B._twist(k, "left_lower_arm", twist * v)
        s15p._aim(k, "left_hand", r @ Vector(dict(spec)["left_hand"]))
        if look:
            hb = k["arm"].pose.bones.get("head 1") or s15p._bone(k, "head")
            if hb is not None:
                hb.matrix = hb.matrix @ Matrix.Rotation(look, 4, "Y")
                bpy.context.view_layer.update()
        hip = s15p._world(k, "hips")
        target = B.S13_AT + hd * back
        k["arm"].location += Vector((target.x - hip.x, target.y - hip.y, 0))
        s15p._ground(k)
        bpy.context.view_layer.update()
        s15p._key_pose(k, f)
    s15p._flush_keys(k)

    # the shrimp on his left shoulder: flat and squeezed as S13 left it, it peeks out once he is up, and stares
    sh = puffshrimp.build((0, 0, 0), name="ep03_shrimp_s15")
    s3d._fix_pivots(sh)
    base = SHRIMP_SHOULDER
    f_peek = f_up + 16
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        side = (k["arm"].matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized()
        up = _ease((f - f_up) / 12.0)
        sq = 0.62 if f < f_peek else 1.0
        pt = B._bone_world(k, "upper_arm.L") + Vector((0, 0, 0.55 * sq)) + side * 0.25
        sh["root"].location = pt
        sh["root"].keyframe_insert("location", frame=f)
        sh["root"].rotation_euler = (-0.55 * (1 - up), 0, yaw + math.pi + (0.5 if f >= f_peek + 20 else 0.0))
        sh["root"].keyframe_insert("rotation_euler", frame=f)
        sh["root"].scale = (base * (1.18 if sq < 1 else 1.0), base * (1.18 if sq < 1 else 1.0), base * sq)
        sh["root"].keyframe_insert("scale", frame=f)
    sc.frame_set(1)
    for fc in anim.all_fcurves(sh["root"].animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.55, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.15, 0.0, 0.0), "CONSTANT")
    for e in sh["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 0.08), "CONSTANT")              # still squeezed shut from S13's duck
        anim.key(e, "scale", f_peek, (1.15, 1.15, 1.15), "CONSTANT")   # eyes wide at the field of moths
        anim.key(e, "scale", f_peek + 10, (1, 1, 1), "CONSTANT")
    anim.blink(sh, f_peek + 30)

    # the mark: the coral key at his wrist, as S13 left it (dimmer once he sits up and it's off the grass)
    key = bpy.data.lights.new("s15_mark_key", "POINT")
    key.color = H9.CORAL
    key.shadow_soft_size = 0.2
    lk = bpy.data.objects.new("s15_mark_key", key)
    sc.collection.objects.link(lk)
    und = bpy.data.lights.new("s15_mark_fill", "POINT")                  # the glow over the field of moths
    und.color = H9.CORAL
    und.shadow_soft_size = 3.0
    und.use_shadow = False
    lu = bpy.data.objects.new("s15_mark_fill", und)
    sc.collection.objects.link(lu)
    for f in range(1, n + 1):
        sc.frame_set(f)
        m = H9._forearm(k, H9.MARK_U)
        lk.location = m + Vector((0, 0, 0.5))
        lk.keyframe_insert("location", frame=f)
        key.energy = B.S13_LIGHT * (1.1 + 0.05 * math.sin(f / 5.0))
        key.keyframe_insert("energy", frame=f)
        lu.location = m + Vector((0, 0, 3.0))
        lu.keyframe_insert("location", frame=f)
        und.energy = B.S13_UNDER * 0.7
        und.keyframe_insert("energy", frame=f)
    sc.frame_set(1)
    wrist = H9._forearm(k, 1.0)
    hips = s15p._world(k, "hips")
    hips = Vector((hips.x, hips.y, 0.0))
    wrist = Vector((wrist.x, wrist.y, 0.0))
    B._grass_at(wrist)
    acting.grass_round(hips, hd)

    # the field of moths on their backs (one built, linked copies), legs waving
    spots = _s15_landings(B, wrist, hips, hd)
    rigs = fluffmoth.swarm(len(spots), lambda i, rnd: (Vector((spots[i][0], spots[i][1], 1.0)), spots[i][3]),
                           name="m15_", seed=15, far=lambda i, loc, scl: False)
    for i, (rig, q) in enumerate(zip(rigs, spots)):
        for w in rig["wings"]:                                           # no flight beat: they lie still
            w.animation_data_clear()
        rig["root"].rotation_euler = (0, 0, q[2])
        fluffmoth.upside_down(rig, 1, n, land_at=(q[0], q[1], 0.0), seed=100 + i)

    # Kai's face: dazed, then bewildered as he looks round, then a small amazed half-smile; eyes on the moths
    acting.face_keys(k, 1, eye_brow_down=0.5, face_angry=0.15)
    acting.face_keys(k, f_up + 8, eye_brow_down=0.0, face_angry=0.0, face_surprise=0.7)
    acting.face_keys(k, f_up + 40, face_surprise=0.35, face_happy=0.35)
    acting.blink(k, 1, n, every=(40, 70), seed=8, at=(f_up + 12,))

    # camera: in front of him (east, toward his feet), low, the moths big in the foreground; a slow push-in on 1s
    mid = hips - hd * 1.2
    cy = math.degrees(math.atan2(hd.x, hd.y))                            # looking west, along his head direction
    _cam("cam_s15", 1, n, (mid + Vector((0, 0, 3.8)), 30.0, 22.0, cy + 18.0),
         (mid + Vector((0, 0, 4.2)), 25.0, 20.0, cy + 14.0), lens=40.0, blur=4.5, shift_y=-0.04)
    LAST.update(k=k, sh=sh, moths=rigs)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + list(k.get("cap", [])))


# ----------------------------------------------------------------------------------------------------- dawn
DAWN_SUN = "#ffb487"            # a low peach-gold sun
DAWN_SKY = ("#8fb6e6", "#ffd2b0", "#ffd9c4")   # zenith, horizon, fill


def dawn():
    """Turn the day island into the first minutes after sunrise: the sun low in the east (long shadows across the
    track), a pink-gold horizon, a cooler blue zenith, the haze warmed."""
    sc = bpy.context.scene
    for o in list(sc.objects):
        if o.type == "LIGHT" and o.data.type == "SUN":
            bpy.data.objects.remove(o, do_unlink=True)
    look.world(sky=DAWN_SKY[0], horizon=DAWN_SKY[1], fill=DAWN_SKY[2], fill_strength=0.55)
    s = look.sun(elev=9, azim=75, energy=3.6, color=DAWN_SUN)
    s.data.angle = math.radians(4)
    nt = sc.node_tree
    for n in nt.nodes:                                                   # the haze colour: peach instead of sky blue
        if n.bl_idname == "CompositorNodeMixRGB" and n.blend_type == "MIX":
            n.inputs[2].default_value = look.hexc("#f6d9c8")
    from channels.monsters.mk import grade
    grade._grade(sc, dict(lift=(1.0, 0.985, 1.04), gamma=(1.0, 0.99, 0.97), gain=(1.12, 1.0, 0.86), sat=0.86,
                          vignette=0.28))                                # warm highlights, cool shadows, less green
    return s


# ------------------------------------------------------------------------------------------------------ S19B
def s19bot():
    n = _frames("S19", 177)                                          # the whole S19 (both panels)
    X._world(n)
    dawn()
    H9.village_and_lake()
    sc = bpy.context.scene
    # the way out of the village: from the square north through the gap between the last two huts (helper 9's huts
    # 3 and 4 stand at (19.6, -153.4) and (2.5, -152.3)), up toward the meadow; a worn dirt path under his feet
    p0, p1 = Vector((11.0, -160.0, 0.0)), Vector((6.5, -126.0, 0.0))
    _path_strip("h5_s19_path", [p0 + (p0 - p1).normalized() * 6.0, p0, p1, p1 + (p1 - p0).normalized() * 40.0])
    d = (p1 - p0).normalized()
    yaw = math.degrees(math.atan2(d.x, -d.y))                            # rot_z so the model's -Y points along d
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    arm = k["arm"]
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (0, 0, math.radians(yaw))
    arm.location = p0
    bpy.context.view_layer.update()
    P = x3.Pose(k)
    L = 0.86 * (p1 - p0).length / X.SCALE                                # armature units along -Y
    f_look0, f_look1 = _word("l19", "like") - 4, _word("l19", "Comment") + 4   # the look back ("like they said")

    def look_back(f):
        """0..1: the look back over his right shoulder (a quick turn, a held look, a slower turn front)."""
        return _ease((f - f_look0) / 8.0) * (1 - _ease((f - (f_look1 - 10)) / 12.0))

    def upper_at(f0, f1):
        def upper(P, t):
            f = f0 + (f1 - f0) * t
            lb = look_back(f)
            x3._arms_down(P, 9)
            P.rot("spine", (3, 0, -12 * lb))                             # the turn over his RIGHT shoulder, so the
            P.rot("chest", (-2 * lb, 0, -26 * lb))                       # shrimp on his left doesn't hide his face
            P.rot("neck", (0, 0, -32 * lb))
            P.rot("head 1", (-8 * lb, -4 * lb, -48 * lb))                # face in profile, chin up a touch
            sw = math.sin(f / 9.5 * math.pi) * (1 - lb)                  # arm swing with the steps
            P.rot("upper_arm.R", (14 * sw, 0, 0))
            P.rot("upper_arm.L", (-8 * sw, 0, 0))
        return upper

    # walk, stop and look back, walk on (armature space: -Y is forward)
    a = 0.56 * L
    feet = x3._walk(P, k, ((0, 0, 0), (0, -a, 0)), 1, f_look0 + 2, step_len=0.55, start_foot="R",
                    upper=upper_at(1, f_look0 + 2), every=2)
    x3._squat(P, feet, f_look0 + 2, f_look1 - 2, 0.0, 0.0, upper_at(f_look0 + 2, f_look1 - 2), every=2)
    x3._walk(P, k, ((0, -a, 0), (0, -L, 0)), f_look1, n, step_len=0.55, start_foot="R",
             upper=upper_at(f_look1, n), every=2)
    sh = shrimp_on_shoulder(k, "L", yaw=0.0)
    body = sh["body"]
    anim.key(body, "rotation_euler", 1, (0, 0, 0))
    anim.key(body, "rotation_euler", f_look0 + 4, (0, 0, 0))
    anim.key(body, "rotation_euler", f_look0 + 12, (0, 0, math.radians(150)))   # it turns to look back too
    anim.key(body, "rotation_euler", f_look1 + 2, (0, 0, math.radians(150)))
    anim.key(body, "rotation_euler", f_look1 + 12, (0, 0, 0))
    for f in range(1, n + 1, 12):                                        # bobbing with his steps
        anim.squash(body, f, 0.0)
        anim.squash(body, f + 6, -0.04)
    anim.blink(sh, f_look0 + 14)
    anim.on_twos(_shrimp_parts(sh), step=2)
    acting.blink(k, 1, n, at=(f_look0 + 6, f_look1 + 20))
    # render only the bottom band (helper 8's split, as Ep 2's S20bot): rows 486-1280
    sc.render.use_border = True
    sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
    sc.render.border_min_y, sc.render.border_max_y = 0.0, 0.62
    # the camera: low in the square behind him, looking up the track; it follows him, slowly gaining
    mid0 = p0 + Vector((0, 0, 5.0))
    mid1 = p0.lerp(p1, 0.55) + Vector((0, 0, 5.0))
    cy = math.degrees(math.atan2(d.x, d.y))
    _cam("cam_s19bot", 1, n, (mid0, 17.0, 8.0, cy), (mid1, 24.0, 7.0, cy + 2.0), lens=40.0, blur=4.0,
         shift_y=0.19)                                                   # him in the middle of the bottom band
    LAST.update(k=k, sh=sh)
    return dict(frames=n, step=2, ones=(1, n), subject=[arm, sh["root"]])


SHOTS = {"S15": s15, "S19bot": s19bot}
