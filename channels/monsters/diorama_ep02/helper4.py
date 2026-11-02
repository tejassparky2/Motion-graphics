"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md), helper 4's shots:

    S05 "Now I was holding a wet pistol shrimp. In my bare hands."  Close on Kai's cupped hands: the puff-shrimp sits
        in them facing him, its wet claw resting against the heel of his left palm; drops bead on the claw, one swells
        at the tip and falls into his palm (on "wet pistol shrimp"). Cut up (f50, between the sentences) to his face:
        pinprick terror eyes, brows up, a tremble on 1s; the 2D sweat drop pops in on "In my" (post pass,
        diorama_ep02/post_helper4.py). Slow push-ins on 1s; the characters on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S05 OUT_DIR [--frames A-B] [--still N --scale 0.5]

Staging is XprL's (diorama_ep02/xprl.py): Kai at KAI_AT on the pond's east shore, facing WREN_FROM (south).
"""
import json
import math
import os

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import bgqrs as s3d                 # kai_point, claw_tip, _drop, lock_on, _fix_pivots
from channels.monsters.ep01v2 import xprl as x3                   # Pose
from channels.monsters.mk import anim, hero, look, puffshrimp, wren

SHRIMP_IN_HAND = float(os.environ.get("SHRIMP_IN_HAND", "0.6"))   # root scale of the shrimp in his hands (shared)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
FPS = 24


def _frames(shot, fallback):
    return X._frames(shot, fallback)


def _words(line_id):
    """{word: local frame (1-based) of its start} for a line, relative to its shot's first frame."""
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep02", "timing.json")) as f:
        d = json.load(f)
    ln = next(x for x in d["lines"] if x["id"] == line_id)
    s0 = next(s["start"] for s in d["shots"] if s["shot"] == ln["scene"])
    return [(w["w"], 1 + round((w["start"] - s0) * FPS), 1 + round((w["end"] - s0) * FPS)) for w in ln["words"]]


# ------------------------------------------------------------------------------------------------- Kai holding it
def _hold(P, breath=0.0, tremble=0.0):
    """Both hands cupped together in front of his chest, palms up, the shrimp sitting in them; elbows in, the
    shoulders a little up (holding his breath). `tremble` (-1..1) shifts the hands a touch on 1s."""
    P.rot("chest", (4 + 2 * breath, 0, 0))
    for side, s in (("L", 1), ("R", -1)):
        P.aim(f"upper_arm.{side}", (s * 0.18, -0.28, -1.0))
        P.aim(f"forearm.{side}", (-s * 0.32, -1.0, 0.18 + 0.02 * tremble))
        P.twist(f"forearm.{side}", -s * 80)
        P.aim(f"hand.{side}", (-s * 0.38, -1.0, 0.1))
    P.rot("head 1", (14, 0, 0))                                       # looking down at it


def _fingers(rig, curl, thumb=0.25):
    """Curl both hands' fingers (cupping) by `curl` radians per joint."""
    from mathutils import Matrix
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.rotation_mode = "QUATERNION"
            c = thumb if b.name.startswith("thumb") else curl
            b.rotation_quaternion = Matrix.Rotation(c, 4, "X").to_quaternion()


def _key_fingers(rig, f):
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.keyframe_insert("rotation_quaternion", frame=f)


def _palms(rig):
    """World point between his two palms (where the shrimp sits) and the up direction of the cup."""
    arm = rig["arm"]
    bpy.context.view_layer.update()
    pts = []
    for side in ("L", "R"):
        pb = rig["arm"].pose.bones[f"hand.{side}"]
        pts.append(arm.matrix_world @ ((pb.head + pb.tail) / 2))
    return (pts[0] + pts[1]) / 2


def _shrimp_in_hands(rig, yaw_deg):
    """The puff-shrimp sitting in his palms, facing his face (yaw_deg: its root's world z rotation), scaled
    SHRIMP_IN_HAND; its claw (on its right) laid down along his left palm, resting."""
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    r = sh["root"]
    r.scale = (SHRIMP_IN_HAND,) * 3
    r.location = _palms(rig) + Vector((0, 0, 0.12))
    r.rotation_euler = (0, 0, math.radians(yaw_deg))
    bpy.context.view_layer.update()
    return sh


def _wet(sh, n, seed=3):
    """Beads of water on the claw and the collar (small glossy drops, outlined), so it reads WET at a glance."""
    import random
    rnd = random.Random(seed)
    mat = look.toon("s05_bead", look.hexc("#bfe8ff"), shade=0.7, gloss=True)
    out = []
    claw = bpy.data.objects["puff_claw"]
    vs = claw.data.vertices
    picks = rnd.sample(range(len(vs)), 9)
    for i, vi in enumerate(picks):
        co = vs[vi].co + vs[vi].normal * 0.06
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.07 + 0.03 * rnd.random(),
                                             location=claw.matrix_world @ co)
        b = bpy.context.object
        b.name = f"puff_bead{i}"
        b.data.materials.append(mat)
        look.outline(b, 0.006)
        b.visible_shadow = False
        mw = b.matrix_world.copy()
        b.parent = claw
        b.matrix_parent_inverse = claw.matrix_world.inverted()
        b.matrix_world = mw
        out.append(b)
    return out


def _face(keys, f):
    """Key a whole face at frame f: every expression key touched by hero.FACES (and `keys`) is set, to its value in
    `keys` or 0 (hero.face keys one recipe and zeroes the rest, so recipes can't be stacked). CONSTANT, anime snaps."""
    head = bpy.data.objects["head"]
    kb = head.data.shape_keys.key_blocks
    touched = set(keys)
    for rv in hero.FACES.values():
        touched.update(rv.keys())
    for nm in touched:
        if nm in kb:
            kb[nm].value = keys.get(nm, 0.0)
            kb[nm].keyframe_insert("value", frame=f)
    for fc in anim.all_fcurves(head.data.shape_keys.animation_data.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - f) < 0.01:
                kp.interpolation = "CONSTANT"


# ------------------------------------------------------------------------------------------------- the cameras
def _shot_cam(name, frame, target, dist, tilt, yaw, lens, blur, push=0.06, f1=None, shift_y=0.0):
    """A diorama camera bound at `frame` (timeline marker), pushing in `push` of its distance by f1 on 1s, its focus
    and haze following."""
    from channels.monsters.mk import diorama
    c = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=lens, blur=blur, frame=frame,
                       haze=(2.5, 2.0))
    c.data.shift_y = shift_y
    t = Vector(target)
    p0 = c.location.copy()
    sc = bpy.context.scene
    for f in range(frame, (f1 or frame) + 1):
        u = (f - frame) / max(1, (f1 or frame) - frame)
        e = u * u * (3 - 2 * u)
        c.location = p0.lerp(t, push * e)
        c.keyframe_insert("location", frame=f)
        c.data.dof.focus_distance = (c.location - t).length
        c.data.dof.keyframe_insert("focus_distance", frame=f)
    del sc
    return c


def _anchors(shot, n, rig, extra=None):
    """Screen points (720x1280, top-left origin) of Kai's eyes and temple per frame through each frame's marker
    camera, for the 2D pass: build/monsters/diorama_ep02/<SHOT>_anchors.json."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    marks = sorted(sc.timeline_markers, key=lambda m: m.frame)
    for f in range(1, n + 1):
        sc.frame_set(f)
        cam = [m.camera for m in marks if m.frame <= f][-1] if marks else sc.camera
        pts = {k: s3d.kai_point(rig, k) for k in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        for k, fn in (extra or {}).items():
            pts[k] = fn()
        out[f] = {k: (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
                  for k, v in ((k, world_to_camera_view(sc, cam, p)) for k, p in pts.items())}
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


# ------------------------------------------------------------------------------------------------------------ S05
S05_CUT = 50                                    # the cut up to his face, between "...shrimp." and "In my bare hands."


def s05():
    n = _frames("S05", 99)
    W = _words("l5")
    f_wet = next(a for w, a, b in W if w == "wet")                  # 28
    f_in = next(a for w, a, b in W if w == "In")                    # 56
    X._world(n)
    k = X._kai()
    P = x3.Pose(k)
    # Kai: frozen, holding his breath; a tremble on 2s that gets worse after the cut
    for f in range(1, n + 1, 2):
        P.reset()
        tr = math.sin(f * 2.3) * (0.4 if f < S05_CUT else 1.0)
        _hold(P, breath=math.sin(f / 14.0), tremble=tr)
        if f >= S05_CUT:
            P.rot("head 1", (-12, 3 * tr, 0))                          # head comes up off the hands: the stare
        P.key(f)
    _fingers(k, 0.32)
    _key_fingers(k, 1)
    _face({"eye_black_small": 1.0, "eye_brow_up": 0.6, "look_down": 0.7}, 1)        # A: staring down at it
    _face({"eye_black_small": 1.0, "eye_brow_up": 1.0, "shock_plane": 1.0, "mouth_short": 0.6}, S05_CUT)  # B: terror
    _face({"eye_black_small": 1.0, "eye_brow_up": 1.0, "shock_plane": 1.0, "mouth_wide": 0.35, "lip_i": 0.4},
          S05_CUT + 8)                                              # the teeth clench on "In my bare hands"
    X.v2._twos([k["arm"]])

    # the shrimp in his hands, facing his face, its claw down along his left palm; eyes locked on his face
    bpy.context.scene.frame_set(1)
    sh = _shrimp_in_hands(k, X.KAI_YAW + 180)
    pb = k["arm"].pose.bones["hand.L"]
    palm_l = k["arm"].matrix_world @ (pb.head.lerp(pb.tail, 0.7))
    anim.key(sh["shoulder"], "rotation_euler", 1, s3d.aim_claw(sh, palm_l + Vector((0, 0, 0.12))), "CONSTANT")
    # (the claw laid down over the heel of his left palm, its tip resting on it)
    anim.key(sh["hinge"], "rotation_euler", 1, (0.12, 0.0, 0.0), "CONSTANT")
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 70)
    s3d.lock_on(sh, s3d.kai_point(k, "eyes"), 1, lids=0.15, slant=0.1)
    X.v2._twos([sh["body"], sh["shoulder"], sh["hinge"]] + sh["eyes"])
    _wet(sh, n)
    tip = s3d.claw_tip(sh)
    land = _palms(k) + Vector((0.0, 0.0, 0.05))
    s3d._drop(tip - Vector((0, 0, 0.05)), f_wet - 10, f_wet + 4, f_wet + 9, land, r=0.11)

    # cameras: A low over the hands from his front-right, the shrimp side-on in his palms (1..CUT-1);
    # B up to his face, a touch low, his eyes above the caption band (CUT..n)
    hands = _palms(k) + Vector((0, 0, 0.55))
    face = s3d.kai_point(k, "eyes")
    _shot_cam("S05a", 1, tuple(hands), 7.6, 18.0, -X.KAI_YAW - 42.0, 60.0, 3.0, push=0.07, f1=S05_CUT - 1,
              shift_y=-0.2)
    _shot_cam("S05b", S05_CUT, tuple(face - Vector((0, 0, 0.35))), 5.6, 4.0, -X.KAI_YAW + 8.0, 55.0, 2.5, push=0.1,
              f1=n, shift_y=-0.07)
    _anchors("S05", n, k, extra={"tip": lambda: s3d.claw_tip(sh)})
    return dict(frames=n, step=1, subject=[k["arm"], sh["root"]] + list(k.get("cap", [])), cut=S05_CUT,
                beats=dict(wet=f_wet, sweat=f_in))


# ------------------------------------------------------------------------------------------------------------ S06
S06_BG = "#fbefc8"                              # the graphic insert's light ground (pale butter: aqua and coral pop)


def _backdrop(color):
    """A seamless light cyc behind and under the shrimp (a plain graphic ground, no island): a floor plane curving
    up into a back wall, flat-lit (emission) so it stays one clean light tone."""
    import bmesh
    me = bpy.data.meshes.new("s06_cyc")
    bm = bmesh.new()
    rows = []
    for i in range(25):                                              # the profile: floor -> quarter circle -> wall
        u = i / 24
        if u < 0.4:
            y, z = -60 + (u / 0.4) * 60, 0.0
        else:
            a = (u - 0.4) / 0.6 * (math.pi / 2)
            y, z = 18 * math.sin(a), 18 * (1 - math.cos(a))
            if u > 0.99:
                z = 80.0
        rows.append([bm.verts.new((x, y, z)) for x in (-80.0, 80.0)])
    for r0, r1 in zip(rows[:-1], rows[1:]):
        bm.faces.new((r0[0], r0[1], r1[1], r1[0]))
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("s06_cyc", me)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (0.0, 0.0, -math.pi / 2)                     # the wall behind the shrimp on +X (the camera's -X)
    o.data.materials.append(look.flat("s06_ground", look.hexc(color), 1.0))
    o.visible_shadow = False
    return o


def s06():
    """The claw in clean side profile, aimed straight ahead (screen right), on a light graphic ground: the shrimp
    breathes and blinks; on "fires" the snapping finger cocks open (anticipation); on "Straight ahead" the 2D pass
    (post_helper4.py) fires an arrow-like jet streak straight out of the claw to the frame edge, nothing in any other
    direction. A slow push-in on 1s; the shrimp on 2s."""
    from channels.monsters.mk import diorama
    n = _frames("S06", 98)
    W = _words("l6")
    f_fires = next(a for w, a, b in W if w == "fires")              # 35
    f_str = next(a for w, a, b in W if w == "Straight")             # 67
    diorama.setup()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    sc.world.mist_settings.start, sc.world.mist_settings.depth = 500.0, 100.0   # no haze on the insert
    # the shrimp turned so its right side (the claw) faces the camera on -X, its front (-Y) to screen right
    origin = Vector((0.0, -20.0, 0.0))
    _backdrop(S06_BG).location = origin
    sh = puffshrimp.build((0, 0, 0))                                # at the origin: _fix_pivots assumes it
    s3d._fix_pivots(sh)                                             # (built elsewhere, it moved the finger's hinge
    sh["root"].location = origin                                    # 20 units off and the finger came loose)
    bpy.context.view_layer.update()
    ahead = origin + Vector((0, -40.0, 2.6))                        # straight ahead, at the claw's height
    rest = s3d.aim_claw(sh, ahead)
    anim.key(sh["shoulder"], "rotation_euler", 1, rest, "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.2, 0.0, 0.0), "CONSTANT")
    for f, v in ((f_fires - 4, 0.2), (f_fires, 1.25), (f_fires + 4, 1.05)):   # it cocks: the finger swings wide
        anim.key(sh["hinge"], "rotation_euler", f, (v, 0.0, 0.0), "BEZIER")
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.squash(sh["body"], f_str - 6, -0.06)                       # a little crouch before the streak...
    anim.squash(sh["body"], f_str, 0.03)                            # ...and the kick of the recoil
    anim.squash(sh["body"], f_str + 6, 0.0)
    anim.blink(sh, 16)
    anim.blink(sh, 84)
    s3d.lock_on(sh, ahead, 1, lids=0.3, slant=0.25)
    X.v2._twos([sh["body"], sh["shoulder"], sh["hinge"]] + sh["eyes"])
    # the camera: side-on from its right (-X), level, a long lens; the shrimp left of centre so the streak has room
    tip0 = s3d.claw_tip(sh)
    tgt = origin + Vector((0, -0.7, 1.9))
    bpy.ops.object.camera_add(location=tgt + Vector((-27.0, 0.0, 1.0)))
    cam = bpy.context.object
    cam.name = "S06cam"
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 85.0
    cam.data.shift_x = 0.07                                         # the shrimp left; the jet runs to the right
    cam.data.shift_y = -0.17                                        # and above the caption band
    cam.data.clip_end = 400
    sc.camera = cam
    p0 = cam.location.copy()
    for f in range(1, n + 1):
        u = (f - 1) / max(1, n - 1)
        cam.location = p0.lerp(tgt, 0.08 * u * u * (3 - 2 * u))
        cam.keyframe_insert("location", frame=f)
    # the 2D pass's anchors: the muzzle and a point far straight ahead of it, per frame
    from bpy_extras.object_utils import world_to_camera_view
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        t = s3d.claw_tip(sh)
        piv = sh["shoulder"].matrix_world.translation
        d = (t - piv).normalized()
        row = {}
        for nm, p in (("tip", t), ("ahead", t + d * 60.0)):
            v = world_to_camera_view(sc, cam, p)
            row[nm] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
        out[f] = row
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "S06_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)
    del tip0
    return dict(frames=n, step=1, subject=[sh["root"]], beats=dict(fires=f_fires, streak=f_str))


# ------------------------------------------------------------------------------------------------------- S20 (B)
def _shirt_mat(rig):
    """Kai's jacket material (the 'huku' toon), so the bulge is his own shirt."""
    for o in bpy.data.objects:
        if o.type == "MESH" and o.find_armature() == rig["arm"]:
            for m in o.data.materials:
                if m and "huku" in m.name.lower() and "line" not in m.name.lower():
                    return m
    return look.toon("s20b_shirt", look.hexc("#1d9f94"))


def _bone_world(rig, name, tail=False):
    pb = rig["arm"].pose.bones[name]
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


S20B_LIGHT = 55.0                                # the mark's coral point light at full (S14's is 60)


def s20bot():
    """Option B, the bottom panel (helper 8 crops it under the jagged divider), owner's new ending (2 Nov): "Option
    B: show her the glowing mark." Kai and Wren face to face as S17-S20A leave them: Kai tense, the shrimp cupped;
    Wren stern with her bell. On "Option B" he shifts the shrimp into his right hand and slowly raises his left
    forearm toward her ("show her"); on "glowing mark" the coral zigzag on it (helper 9's S14 mark, drawn by
    post_helper4 from S20bot_mark.json) flares, lighting his arm (a real coral point light). Wren's eyes go wide,
    she steps back half a step and raises the bell up in front of her like a ward; the standoff holds to the end,
    the mark glowing softly. Her wide eyes are 2D (S05's terror eyes, from her eye anchors in S20bot_mark.json): her
    3D eye keys don't read at this size. Framed in the bottom band; a slow push-in on 1s, the characters on 2s."""
    from channels.monsters.diorama_ep02 import helper9 as H9
    n = _frames("S20", 160)
    W = _words("l20")
    fw = {}
    for w_, a_, b_ in W:
        fw.setdefault(w_.strip(".:").lower(), []).append((a_, b_))
    f_optB = fw["option"][1][0]                                    # 60
    f_show = fw["show"][0][0]                                      # 84
    f_glow = fw["glowing"][0][0]                                   # 95
    f_mark_end = fw["mark"][0][1]                                  # 108
    f_comment = fw["comment"][0][0]                                # 117
    X._world(n)
    k = X._kai()
    w = X._wren(X.WREN_STOP, X.WREN_YAW)
    PK, PW = x3.Pose(k), x3.Pose(w)
    feet = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}
    up = Vector((0, 0, 1))
    d = (X.WREN_STOP - X.KAI_AT).normalized()                      # Kai's facing (toward Wren)
    fwd = Vector((d.x, d.y, 0)).normalized()

    # beats
    f_shift0, f_shift1 = f_optB + 2, f_optB + 10                   # the shrimp into his right hand
    f_arm0, f_arm1 = f_optB + 8, f_show + 8                        # the left forearm rises toward her, slowly
    f_fear = f_glow + 6                                            # she sees it flare
    f_back0, f_back1 = f_fear, f_fear + 8                          # half a step back (anticipation, overshoot)
    f_ward0, f_ward1 = f_fear + 2, f_fear + 8                      # the bell up in front of her
    back = fwd * 0.75                                              # her half step (world units; Kai is 5.8x scale)

    def arm_u(f):
        return _smooth((f - f_arm0) / max(1, f_arm1 - f_arm0))

    for f in range(1, n + 1, 2):
        # Wren
        PW.reset()
        for sd in ("L", "R"):
            PW.leg(sd, feet[sd] + Vector((0, 0, PW.ankle_h)))
        ward = _smooth((f - f_ward0) / max(1, f_ward1 - f_ward0))
        if ward > 0:
            over = 1.0 + 0.08 * math.sin(math.pi * min(1.0, (f - f_ward0) / 10.0)) if f >= f_ward1 else 1.0
            r = ward * over
            wren.hold_bell(PW, 1.0, shake=2.5 * math.sin(f * 1.3) if f > f_ward1 else 0.0)
            PW.aim("upper_arm.R", (-0.10, -0.55 - 0.25 * r, -1 + 1.25 * r))      # up past chest height: a ward
            PW.aim("forearm.R", (-0.04, -0.85 - 0.2 * r, -0.2 + 0.8 * r))
            PW.aim("hand.R", (-0.04, -0.3, -1))                    # the bell still hangs upright
        else:
            wren.hold_bell(PW, 0.25)
        recoil = _smooth((f - f_back0) / max(1, f_back1 - f_back0))
        PW.rot("chest", (-3 + 1.0 * math.sin(f / 20.0) - 7.0 * recoil, 0, 0))   # leaning away
        PW.rot("head 1", (-6 - 5.0 * recoil, 0, 0))
        PW.key(f)
        hop = 0.0
        if f_back0 <= f < f_back1:
            hop = 0.12 * math.sin(math.pi * (f - f_back0) / (f_back1 - f_back0))
        w["arm"].location = X.WREN_STOP + back * (recoil * (1.04 if f >= f_back1 - 2 else 1.0)) + up * hop
        w["arm"].keyframe_insert("location", frame=f)

        # Kai
        PK.reset()
        for sd in ("L", "R"):
            PK.leg(sd, feet[sd] + Vector((0, 0, PK.ankle_h)))
        PK.rot("chest", (1.5 * math.sin(f / 20.0), 0, 0))
        bpy.context.view_layer.update()
        if f < f_shift0:
            X._cup(PK)
            if f < f_optB:
                PK.rot("head 1", (4.0, 0, 0))                      # eyes on her, tense
        else:
            sh_r = _bone_world(k, "chest") + fwd * 1.15 - up * 0.55 + X._side_vec(k) * -0.25
            X._reach(PK, k, "R", sh_r)                             # the shrimp on his right hand
            u = arm_u(f)
            shoulder = _bone_world(k, "upper_arm.L")
            low = _bone_world(k, "chest") + fwd * 1.1 - up * 0.6 + X._side_vec(k) * 0.3
            high = shoulder + fwd * 2.7 - up * 0.35 + X._side_vec(k) * -0.15    # held out toward her, chest height
            X._reach(PK, k, "L", low.lerp(high, u), bend=(0, 0, -0.15))
            PK.rot("head 1", (6.0 * u, 0, 0))                      # chin down a touch: steady
        PK.key(f)

    # faces
    _face({"face_sad": 0.6, "eye_brow_up": 0.5}, 1)                 # tense, worried
    _face({"face_sad": 0.3, "eye_brow_down": 0.5, "mouth_short": 0.4}, f_show)   # resolve
    _face({"eye_brow_down": 0.7, "face_angry": 0.25}, f_glow)       # steady: this is mine
    wren.face(w, "stern", 1)
    wren.FACES["fear"] = {"face_surprise": 1.0, "eye_black_small": 0.8, "eye_brow_up": 1.0, "lip_o": 0.5}
    wren.face(w, "fear", f_fear)
    wren.face(w, "fear", f_fear + 14, value=0.85)
    wren.grip(w, 1)
    wren.blink(w, 1, f_fear - 4, at=(40,))

    # the shrimp: cupped, then on his right hand, watching the mark
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    sh["root"].scale = (SHRIMP_IN_HAND,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW + 180))   # facing him
    sc = bpy.context.scene
    for f in range(1, n + 1):
        sc.frame_set(f)
        both = (X._world_of(k, "hand.L") + X._world_of(k, "hand.R")) / 2 + up * 0.25
        right = X._world_of(k, "hand.R") + up * 0.3
        u = _smooth((f - f_shift0) / max(1, f_shift1 - f_shift0))
        sh["root"].location = both.lerp(right, u)
        sh["root"].keyframe_insert("location", frame=f)
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.55, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.15, 0.0, 0.0), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", 1, (0, 0, 0), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", f_glow + 2, (0, 0, math.radians(-35)), "CONSTANT")   # it looks at the mark
    anim.blink(sh, 30)

    # the mark's light: a coral point light just off his forearm on the camera side, following the arm
    ld = bpy.data.lights.new("s20b_mark_light", "POINT")
    ld.color = H9.CORAL
    ld.shadow_soft_size = 0.15
    lt = bpy.data.objects.new("s20b_mark_light", ld)
    sc.collection.objects.link(lt)

    def mark_level(f):
        """0..~1.3: faint once the arm is up, the flare on "glowing mark", then a soft glow."""
        if f < f_show:
            return 0.0
        if f < f_glow:
            return 0.12 * _smooth((f - f_show) / 6)
        if f < f_glow + 4:
            return 0.12 + 1.18 * (f - f_glow) / 4
        if f < f_mark_end:
            return 1.3 - 0.15 * _smooth((f - f_glow - 4) / (f_mark_end - f_glow - 4))
        return 1.15 - 0.45 * _smooth((f - f_mark_end) / 10) + 0.06 * math.sin(f / 5.0)

    X.v2._twos([k["arm"], w["arm"], sh["body"], sh["hinge"]] + sh["eyes"])

    # camera: the same south-east 3/4 two-shot as before, nudged toward Wren so her face and the raised arm stay in
    # the bottom band; a slow push-in on 1s
    # from Kai's right side, a little behind him: Kai at frame left in profile, Wren at frame right turned 3/4 to us
    # (her face carries the beat); the raised forearm between them
    cdir = (fwd * float(os.environ.get("S20B_FWD", "-0.85")) + Vector((-fwd.y, fwd.x, 0)) * -1.0).normalized()
    yaw = math.degrees(math.atan2(-cdir.x, -cdir.y))
    mid = X.KAI_AT.lerp(X.WREN_STOP, float(os.environ.get("S20B_MID", "0.5")))
    tgt = tuple(mid + Vector((0, 0, 5.4)))
    dist0 = float(os.environ.get("S20B_DIST", "16.5"))
    yoff = float(os.environ.get("S20B_YAW", "0.0"))
    sc.render.use_border = True
    sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
    sc.render.border_min_y, sc.render.border_max_y = 0.0, 0.62   # rows 486-1280: helper 8 shows plate rows 518-1200
    cam = X._cam_move("S20Bcam", n, (tgt, dist0, 6.0, yaw + yoff, 34.0, 0.27),
                      (tgt, dist0 - 1.4, 6.0, yaw + yoff, 34.0, 0.27))
    marks = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        m = H9._forearm(k, H9.MARK_U)
        lt.location = m + (cam.matrix_world.translation - m).normalized() * 0.45
        lt.keyframe_insert("location", frame=f)
        ld.energy = S20B_LIGHT * mark_level(f)
        ld.keyframe_insert("energy", frame=f)
        marks[f] = dict(H9._mark_geo(k, cam), level=round(mark_level(f), 3),
                        w_eye_l=H9._px(cam, s3d.kai_point(w, "eye_l")), w_eye_r=H9._px(cam, s3d.kai_point(w, "eye_r")))
    os.makedirs(BUILD, exist_ok=True)                              # the 2D pass's mark (post_helper4)
    with open(os.path.join(BUILD, "S20bot_mark.json"), "w") as fh:
        json.dump(dict(meta=dict(f_show=f_show, f_glow=f_glow, f_mark_end=f_mark_end, f_fear=f_fear), frames=marks), fh)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]],
                beats=dict(optB=f_optB, show=f_show, glow=f_glow, fear=f_fear, comment=f_comment))


SHOTS = {"S05": s05, "S06": s06, "S20bot": s20bot}
