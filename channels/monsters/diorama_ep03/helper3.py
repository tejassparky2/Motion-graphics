"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), helper 3.

    S02 (Wren) "Marked. The sky cracked the night you fell."
        A  close on Wren over Kai's raised left forearm (soft in the foreground, the mark glowing on it and lighting
           her): the bell still up as a ward, afraid but steady; she speaks (wren.talk_words, on 2s) and on "sky"
           her eyes and head go up.
        B  cut on "cracked": her eyeline, the zigzag crack in the evening sky due north (helper 9's Ep 2 RIFT_EL and
           size; helper 3's rift look), a slow push.
        C  on "night": low, in front of Kai: he looks up too, his left forearm raised beside his face, the mark upright,
           the crack in the sky above him. A coral echo of the mark's zigzag rises from his wrist and lands on the
           crack (the same shape, the same tilt), then both pulse together: the match.
    The shrimp sits on his left shoulder (it climbs up in S01). Kai's left sleeve keeps Ep 2's three thin scratches.

The 2D passes (the mark, the rift, the echo) are drawn by diorama_ep03/post_helper3.py over the Blender frames from
build/monsters/diorama_ep03/<SHOT>_anchors.json, which these builders write.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S02 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import helper9 as H9
from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, hero, puffshrimp, wren

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
FPS = 24
SHRIMP_K = 0.5                       # the puff-shrimp on his shoulder
MARK_LIGHT = 55.0                    # the coral point light at the mark (watts at level 1)
# until ep03/timing.json lands: S02's frames and word starts, estimated from the script (Wren, ~3.3 s, 0.5 s gap)
FALLBACK = dict(n=94, words=dict(marked=6, the=26, sky=31, cracked=37, night=51, you=58, fell=63),
                ends=dict(fell=76))


# ------------------------------------------------------------------------------------------------------------ timing
def _timing(shot):
    """(n, {word: first frame}, [(word, f0, f1)]) from ep03/timing.json, or the estimate if it hasn't landed yet."""
    try:
        with open(TIMING) as fh:
            t = json.load(fh)
        s = next(x for x in t["shots"] if x["shot"] == shot)
        out, seq = {}, []
        for ln in t["lines"]:
            if ln.get("scene") == shot or ln.get("shot") == shot:
                for w in ln["words"]:
                    key = w["w"].strip(".,!?:;").lower()
                    a = round((w["start"] - s["start"]) * FPS) + 1
                    b = round((w["end"] - s["start"]) * FPS) + 1
                    out.setdefault(key, a)
                    seq.append((key, a, b))
        return s["render_frames"], out, seq, s["start"]
    except (OSError, StopIteration, KeyError, ValueError):
        fb = FALLBACK
        ws = sorted(fb["words"].items(), key=lambda kv: kv[1])
        seq = [(w, a, (ws[i + 1][1] - 1 if i + 1 < len(ws) else fb["ends"]["fell"])) for i, (w, a) in enumerate(ws)]
        return fb["n"], dict(fb["words"]), seq, None


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _bone_world(rig, name, tail=False):
    pb = rig["arm"].pose.bones[name]
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _kai_face(keys, f):
    """A whole Kai face at frame f (every expression key in hero.FACES and `keys`), CONSTANT."""
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


def _write_anchors(shot, n, fn, meta):
    """{"meta", "frames": {f: fn(f, the active camera)}} -> build/monsters/diorama_ep03/<shot>_anchors.json (not for
    --still checks, except the one frame asked for)."""
    sc = bpy.context.scene
    still = int(sys.argv[sys.argv.index("--still") + 1]) if "--still" in sys.argv else None
    out = {}
    for f in ([still] if still else range(1, n + 1)):
        sc.frame_set(f)
        out[f] = fn(f, H9._active_cam(f))
    sc.frame_set(1)
    os.makedirs(BUILD, exist_ok=True)
    name = f"{shot}_anchors_still.json" if still else f"{shot}_anchors.json"
    with open(os.path.join(BUILD, name), "w") as fh:
        json.dump(dict(meta=meta, frames=out), fh)


def _shoulder_shrimp(k, n, name="ep03_shrimp_s02", facing=None, yaw=None):
    """The puff-shrimp riding on Kai's left shoulder, facing where he faces, breathing, blinking."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    sh["root"].scale = (SHRIMP_K,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW if yaw is None else yaw))
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        fwd = facing if facing is not None else (X.WREN_STOP - X.KAI_AT).normalized()
        p = _bone_world(k, "upper_arm.L") + Vector((0, 0, 0.34)) + Vector((fwd.x, fwd.y, 0)).normalized() * 0.1 \
            + X._side_vec(k) * 0.5                                # on the outer edge of the shoulder: beside his face
        sh["root"].location = p
        sh["root"].keyframe_insert("location", frame=f)
    sc.frame_set(1)
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 20)
    sh["name"] = name
    return sh


# ------------------------------------------------------------------------------------------------------- the sky
# The evening sky is painted in 2D behind the render (the compositor's haze turns the 3D sky into one flat colour):
# a gradient by elevation and wispy clouds at fixed places in the sky, both from these per-frame screen anchors.
CLOUDS = ((-38, 20, 0.22), (-14, 29, 0.17), (12, 17, 0.24), (31, 33, 0.15), (-27, 43, 0.13), (9, 47, 0.13),
          (42, 13, 0.21), (-48, 11, 0.19), (22, 52, 0.11), (-5, 9, 0.2))    # (deg east of north, deg up, width rad)


def _sky_geo(cam):
    """Screen y (720x1280) of elevations 0-90 deg along the camera's own heading, and the clouds: [x, y, width px]."""
    o = cam.matrix_world.translation
    fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
    h = Vector((fwd.x, fwd.y, 0))
    h = h.normalized() if h.length > 1e-4 else Vector((0, 1, 0))
    els = []
    for e in range(0, 91, 10):
        r = math.radians(e)
        p = H9._px(cam, o + (h * math.cos(r) + Vector((0, 0, math.sin(r)))) * 4000)
        els.append(p[1] if p[2] > 0 else None)
    cl = []
    for az, el, wd in CLOUDS:
        a, e = math.radians(az), math.radians(el)
        d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
        d2 = Vector((math.sin(a + wd) * math.cos(e), math.cos(a + wd) * math.cos(e), math.sin(e)))
        p, q = H9._px(cam, o + d * 4000), H9._px(cam, o + d2 * 4000)
        if p[2] > 0 and q[2] > 0:
            cl.append([p[0], p[1], round(math.hypot(q[0] - p[0], q[1] - p[1]), 1)])
    return dict(el=els, clouds=cl)


# ------------------------------------------------------------------------------------------------------------ S02
def s02():
    n, W, seq, t0 = _timing("S02")
    f_marked, f_sky, f_crk = W.get("marked", 6), W.get("sky", 31), W.get("cracked", 37)
    f_night = W.get("night", 51)
    fb = max(f_sky + 4, f_crk - 1)                     # cut A -> B (the sky), just before "cracked"
    fc = max(fb + 10, f_night - 1)                     # cut B -> C (Kai looks up)
    f_echo = fc + 6                                    # the mark's zigzag rises to the crack
    X._world(n)
    sc = bpy.context.scene
    k = X._kai()
    w = X._wren(X.WREN_STOP, X.WREN_YAW)
    PK, PW = x3.Pose(k), x3.Pose(w)
    up = Vector((0, 0, 1))
    d = (X.WREN_STOP - X.KAI_AT).normalized()
    fwd = Vector((d.x, d.y, 0)).normalized()                       # Kai's facing (toward Wren)
    left = X._side_vec(k)                                          # Kai's left
    feet = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}
    back = fwd * 0.75                                              # where S01 leaves her: half a step back

    for f in range(1, n + 1, 2):
        # Wren: the bell up as a ward (Ep 2's end), easing a little lower as she speaks; head up on "sky"
        PW.reset()
        for sd in ("L", "R"):
            PW.leg(sd, feet[sd] + Vector((0, 0, PW.ankle_h)))
        r = 1.0 - 0.35 * _smooth((f - f_marked) / 18)
        wren.hold_bell(PW, 0.9, shake=1.6 * math.sin(f * 1.3) * (1 - 0.6 * _smooth((f - f_marked) / 20)))
        PW.aim("upper_arm.R", (-0.10, -0.55 - 0.25 * r, -1 + 1.25 * r))
        PW.aim("forearm.R", (-0.04, -0.85 - 0.2 * r, -0.2 + 0.8 * r))
        PW.aim("hand.R", (-0.04, -0.3, -1))
        look_up = _smooth((f - (f_sky - 4)) / 6)                   # anticipation dip, then up (overshoot, settle)
        dip = 3.0 if f_sky - 6 <= f < f_sky - 3 else 0.0
        over = 4.0 * math.sin(math.pi * min(1.0, max(0.0, (f - f_sky - 2) / 8))) if f > f_sky + 2 else 0.0
        PW.rot("chest", (-8 + 1.0 * math.sin(f / 20.0) - 6 * look_up, 0, 0))
        PW.rot("head 1", (-10 + dip - 26 * look_up - over, 0, 0))
        PW.key(f)
        w["arm"].location = X.WREN_STOP + back
        w["arm"].keyframe_insert("location", frame=f)

        # Kai: the left forearm raised toward her, the inner wrist turned out (Ep 2's end); in C he lifts it higher
        # beside his face and looks up (anticipation dip, overshoot)
        PK.reset()
        for sd in ("L", "R"):
            PK.leg(sd, feet[sd] + Vector((0, 0, PK.ankle_h)))
        PK.rot("chest", (1.5 * math.sin(f / 20.0), 0, 0))
        bpy.context.view_layer.update()
        u = _smooth((f - fc) / 8)
        shoulder = _bone_world(k, "upper_arm.L")
        toward = shoulder + fwd * 2.4 + up * 0.9 - left * 0.25     # up toward her, face height
        skyward = shoulder + fwd * 1.0 + up * 2.6 + left * 0.35    # up beside his face, the mark to the front
        X._reach(PK, k, "L", toward.lerp(skyward, u), bend=(0, 0, 0.0))
        PK.twist("forearm.L", -80.0)
        rest = _bone_world(k, "chest") + fwd * 0.75 - up * 2.1 - left * 0.75
        X._reach(PK, k, "R", rest)                                 # the right hand down at his side
        dipk = 3.0 if fc - 2 <= f < fc else 0.0
        overk = 4.0 * math.sin(math.pi * min(1.0, max(0.0, (f - fc - 4) / 8))) if f > fc + 4 else 0.0
        PK.rot("head 1", (-4.0 + dipk - 30.0 * u - overk, 0, 0))   # chin up: he looks at the sky
        PK.rot("chest", (-6.0 * u, 0, 0))
        PK.key(f)

    # faces
    wren.face(w, "shocked", 1, value=0.85)                         # where S01 leaves her (XprL's Ep 3 faces)
    wren.face(w, "stern", f_marked - 2)                            # afraid but steady
    wren.face(w, "shocked", f_sky + 2, value=0.6)                  # she looks up at it
    wren.grip(w, 1)
    wren.blink(w, 1, f_sky - 6, at=(f_marked + 10,))
    words = [dict(w=wd, start=(a - 1) / FPS, end=(b - 1) / FPS) for wd, a, b in seq]
    wren.talk_words(w, words, 0.0)
    _kai_face({"eye_brow_down": 0.7, "face_angry": 0.25}, 1)        # steady: this is mine (Ep 2's end)
    _kai_face({"face_surprise": 0.55, "eye_brow_up": 0.7}, fc)     # he looks up: the same shape
    _kai_face({"face_surprise": 0.35, "eye_brow_up": 0.5, "look_up": 0.6}, fc + 6)

    sh = _shoulder_shrimp(k, n)
    anim.key(sh["body"], "rotation_euler", 1, (0, 0, 0), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", fc + 4, (-0.35, 0, 0), "CONSTANT")   # it looks up too
    anim.on_twos(H9._shrimp_parts(sh), step=2)
    X.v2._twos([k["arm"], w["arm"]])

    # the cameras
    sc.frame_set(1)
    bpy.context.view_layer.update()
    w_face = _bone_world(w, "head 1") + up * 0.55
    k_face = _bone_world(k, "head 1") + up * 0.55
    # A: over his left shoulder, his raised forearm soft in the foreground at frame left, her face 3/4
    camA = H9._new_cam("S02a", 1)
    pa = k_face - fwd * 3.0 + left * 3.3 + up * 0.9                 # high and wide of his shoulder (and the shrimp)
    for f in range(1, fb):
        e = _smooth((f - 1) / max(1, fb - 2))
        loc = pa.lerp(w_face, 0.10 * e)                             # a slow push in on her
        H9._key_cam(camA, f, loc, H9._look(w_face - loc), 62.0, (w_face - loc).length, shift_y=-0.06, blur=10.0,
                    haze=(4.0, 4.0))
    # B: her eyeline to the crack: the sky due north, RIFT_EL up; a slow push
    camB = H9._new_cam("S02b", fb)
    fwd_r, _ = H9._rift_dir()
    eye = w_face + fwd_r * 1.8                                     # just out in front of her face
    for f in range(fb, fc):
        e = _smooth((f - fb) / max(1, fc - fb - 1))
        p_ = math.radians(35.0 + 6.0 * e)                           # low enough for the treetops; a tilt up into it
        aim = Vector((0, math.cos(p_), math.sin(p_)))
        H9._key_cam(camB, f, eye, H9._look(aim), 30.0 * (1 + 0.04 * e), 60.0, blur=3.0, haze=(0.8, 2.0))
    # C: due south of Kai (her side; she's hidden for it), low, looking due north and up with a wide lens: his face
    # above the captions, the raised forearm (mark upright) beside it, the crack upright in the sky above him
    camC = H9._new_cam("S02c", fc)
    pc = k_face + Vector((0, -7.0, -3.0)) + left * 1.1                # toward his left: the shrimp beside his face
    el_face = math.degrees(math.atan2(k_face.z - pc.z, (k_face - pc).xy.length))
    for f in range(fc, n + 1):
        e = _smooth((f - fc) / max(1, n - fc))
        p_ = math.radians(el_face + 15.0 + 3.0 * e)                  # tilting up a touch as the echo lands
        loc = pc + Vector((0, 0.35 * e, 0))                         # and a slow push
        H9._key_cam(camC, f, loc, H9._look(Vector((0, math.cos(p_), math.sin(p_)))), 18.0, (k_face - loc).length,
                    blur=5.0, haze=(3.0, 4.0))
    H9._hide_from(fc, [o for o in w["arm"].users_collection[0].objects if not o.hide_render])   # (not her hidden cap)
    H9._linear(camA, camA.data, camB, camB.data, camC, camC.data, sc.world)

    # the mark's light: a coral point light just off his forearm on the camera's side
    ld = bpy.data.lights.new("s02_mark_light", "POINT")
    ld.color = H9.CORAL
    ld.shadow_soft_size = 0.15
    lt = bpy.data.objects.new("s02_mark_light", ld)
    sc.collection.objects.link(lt)

    def level(f):
        return 1.0 + 0.06 * math.sin(f / 5.0) + (0.35 * max(0.0, 1 - abs(f - f_echo - 8) / 6))

    for f in range(1, n + 1):
        sc.frame_set(f)
        m = H9._forearm(k, H9.MARK_U)
        cam = H9._active_cam(f)
        lt.location = m + (cam.matrix_world.translation - m).normalized() * 0.45
        lt.keyframe_insert("location", frame=f)
        ld.energy = MARK_LIGHT * level(f)
        ld.keyframe_insert("energy", frame=f)
    sc.frame_set(1)
    if f_crk:                                                       # the shrimp's in his space: hide it in B
        pass

    def geo(f, c):
        return dict(mark=H9._mark_geo(k, c), rift=H9._rift_geo(c), level=round(level(f), 3), sky=_sky_geo(c))
    _write_anchors("S02", n, geo, dict(fb=fb, fc=fc, f_echo=f_echo, f_sky=f_sky))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------------- S19 top
def _yaw_facing(F):
    """Armature rot_z (deg) so the model's front (-Y) points along world direction F."""
    return math.degrees(math.atan2(F.x, -F.y))


def _boat(name="h3_boat"):
    """A small wooden rowing boat (boat space: +Y the bow, origin on the floor boards, ~19 long, ~6 wide): a round-
    bottomed hull, a gunwale strip, three thwarts, two oarlocks. Toon wood with outlines. Returns dict(root, ...)."""
    import bmesh
    from mathutils import Matrix
    from channels.monsters.mk import look
    wood = look.toon(f"{name}_wood", look.hexc("#8a5a34"))
    plank = look.toon(f"{name}_plank", look.hexc("#a8744a"))
    dark = look.toon(f"{name}_inside", look.hexc("#6a4226"))
    root = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(root)

    def mesh(nm, bm, mat, line=0.05):
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new(nm, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(mat)
        o.parent = root
        if line:
            mod = o.modifiers.new("line", "SOLIDIFY")
            mod.thickness = -line
            mod.use_flip_normals = True
            mod.material_offset = 1
            o.data.materials.append(look.flat(f"{nm}_line", (0.16, 0.09, 0.05, 1)))
        return o
    # the hull: the lower half of a stretched sphere, pinched to a point at the bow, a little up at both ends
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=28, v_segments=14, radius=1.0)
    for v in list(bm.verts):
        if v.co.z > 0.02:
            bm.verts.remove(v)
    for v in bm.verts:
        x, y, z = v.co
        pinch = 1.0 - 0.55 * max(0.0, y) ** 2                     # a narrower bow
        v.co = Vector((x * 3.1 * pinch, y * 9.6, 2.6 + z * 3.0 + 0.35 * y * y))   # rim 2.6 over the floor, keel -0.4
    bmesh.ops.reverse_faces(bm, faces=bm.faces)                   # its inside faces the camera from above
    hull = mesh(f"{name}_hull", bm, wood)
    bm = bmesh.new()                                              # the floor boards
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((2.9, 12.0, 0.18, 1)))
    floor = mesh(f"{name}_floor", bm, dark, line=0.0)
    floor.location = (0, 0, -0.05)
    bm = bmesh.new()                                              # the gunwale: a ring round the rim
    pts = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        y = math.sin(a)
        pinch = 1.0 - 0.55 * max(0.0, y) ** 2
        pts.append(Vector((math.cos(a) * 3.1 * pinch, y * 9.6, 2.6 + 0.35 * y * y)))
    for i in range(48):
        p0, p1 = pts[i], pts[(i + 1) % 48]
        d = (p1 - p0)
        m = Matrix.Translation((p0 + p1) / 2) @ Matrix.Rotation(math.atan2(d.y, d.x), 4, "Z") @ \
            Matrix.Diagonal((d.length + 0.08, 0.32, 0.3, 1))
        bmesh.ops.create_cube(bm, size=1.0, matrix=m)
    rim = mesh(f"{name}_rim", bm, plank, line=0.04)
    bm = bmesh.new()                                              # thwarts (seats) and the oarlocks
    for y, w_ in ((1.2, 5.2), (-6.0, 4.0), (6.4, 3.2)):
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, y, 2.45)) @ Matrix.Diagonal((w_, 1.3, 0.25, 1)))
        for sx in (-1, 1):
            bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((sx * w_ * 0.42, y, 1.3)) @
                                  Matrix.Diagonal((0.3, 0.3, 2.3, 1)))
    for sx in (-1, 1):
        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((sx * 3.05, -0.4, 2.95)) @
                              Matrix.Diagonal((0.25, 0.25, 0.7, 1)))
    seats = mesh(f"{name}_seats", bm, plank, line=0.04)
    return dict(root=root, hull=hull, rim=rim, seats=seats, kai_seat=Vector((0, 1.2, 0)), wren_seat=Vector((0, -6.0, 0)),
                locks=(Vector((3.05, -0.4, 3.2)), Vector((-3.05, -0.4, 3.2))))


def _oar(name, wood_mat):
    """An oar along its local +Y from the handle (origin) out to the blade, ~11.5 long."""
    import bmesh
    from mathutils import Matrix
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.12, radius2=0.12, depth=9.0,
                          matrix=Matrix.Translation((0, 4.5, 0)) @ Matrix.Rotation(math.radians(90), 4, "X"))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, 10.2, 0)) @ Matrix.Diagonal((0.12, 2.6, 0.75, 1)))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(wood_mat)
    o.rotation_mode = "QUATERNION"
    return o


def s19top():
    """S19 top (A): "Option A: go with Wren tonight." Night on the lake: Kai and Wren in a small rowing boat heading
    across the dark water to the old lighthouse. Kai rows (facing the stern, his face to us), the shrimp on his left
    shoulder; Wren sits in the stern with the bell in her lap (XprL's wren.sit), looking ahead past him. His mark is
    the key light (helper 9's N9.mark): a coral pool on the water round the boat and on their faces. Seen from behind
    the stern quarter, tracking with the boat, the lighthouse's coral glow ahead. Rendered in the top panel only
    (rows 0-690); the characters on 2s, the camera on 1s."""
    from channels.monsters.diorama_ep02 import helper9 as h9e2
    from channels.monsters.diorama_ep03 import helper9 as N9
    from channels.monsters.mk import acting, look
    n, W, seq, t0 = _timing("S19")
    X._world(n)
    sc = bpy.context.scene
    lake = h9e2.village_and_lake()
    night_water = look.toon("h3_lake_night", look.hexc("#0e1f4a"), shade=0.85, rim=0.15)   # until helper 9's night lake
    for key in ("lake", "shallow"):
        o = lake.get(key)
        if o is not None:
            o.data.materials.clear()
            o.data.materials.append(night_water)
    lh = N9.lighthouse()
    N9.night(n)
    from channels.monsters.mk import night as NG
    lh_top = Vector(lh["top"]) if "top" in lh else (lh["lamp"].matrix_world.translation.copy() if lh.get("lamp")
                                                     else Vector(NG.LIGHTHOUSE_AT) + Vector((0, 0, 60)))
    start = Vector((h9e2.VILLAGE.x - 4.0, h9e2.SHORE_Y - 70.0, 0.0))
    head = Vector((lh_top.x - start.x, lh_top.y - start.y, 0)).normalized()     # the heading: the lighthouse
    side = Vector((head.y, -head.x, 0))                                          # starboard
    yaw_b = math.atan2(-head.x, head.y)                                          # boat +Y along the heading
    b = _boat()
    b["root"].rotation_euler = (0, 0, yaw_b)
    WATER = 0.06
    FLOOR = WATER + 0.9                                                          # the hull draws ~1.3
    period = 40                                                                  # one stroke (frames)

    def surge(f):
        return 0.16 * f + 0.6 * math.sin(2 * math.pi * f / period - 1.2)          # glides on, a push on each drive

    def boat_at(f):
        return start + head * surge(f) + Vector((0, 0, FLOOR + 0.12 * math.sin(f / 9.0)))

    for f in range(1, n + 1):
        b["root"].location = boat_at(f)
        b["root"].rotation_euler = (math.radians(0.9 * math.sin(f / 11.0)), math.radians(1.6 * math.sin(f / 13.0)),
                                    yaw_b)
        b["root"].keyframe_insert("location", frame=f)
        b["root"].keyframe_insert("rotation_euler", frame=f)
    H9._linear(b["root"])

    def bw(p, f):                                                                # boat space -> world at frame f
        sc.frame_set(f)
        bpy.context.view_layer.update()
        return b["root"].matrix_world @ Vector(p)

    # the characters, parented to the boat so they ride it
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    w = wren.load((0, 0, 0), scale=X.SCALE)
    for rig, seat, facing in ((k, b["kai_seat"], Vector((0, -1, 0))), (w, b["wren_seat"], Vector((0, 1, 0)))):
        arm = rig["arm"]
        arm.parent = b["root"]
        arm.rotation_mode = "XYZ"
        arm.rotation_euler = (0, 0, math.radians(_yaw_facing(facing)))
        arm.location = seat - facing * 0.35 + Vector((0, 0, 0.0))                # the thwart under the hips
        arm.scale = (X.SCALE,) * 3
    bpy.context.view_layer.update()
    PK, PW = x3.Pose(k), x3.Pose(w)
    wood = bpy.data.materials.get("h3_boat_plank")
    oars = [_oar("h3_oar_L", wood), _oar("h3_oar_R", wood)]
    for o in oars:
        o.parent = b["root"]
    f_go = W.get("go", 34)
    for f in range(1, n + 1, 2):
        u = ((f - 1) % period) / period                                           # 0 catch, 0.45 finish
        if u < 0.45:
            v = _smooth(u / 0.45)
            hy, hz = -1.3 + 1.9 * v, 4.35 + 0.15 * math.sin(math.pi * v)           # the drive: blades in
            lean = 12 - 22 * v
        else:
            v = _smooth((u - 0.45) / 0.55)
            hy, hz = 0.6 - 1.9 * v, 3.85                                          # the recovery: blades out
            lean = -10 + 22 * v
        # Kai: seated, rowing (hands in boat space, then into his armature space for the IK)
        PK.reset()
        wren.sit(PK, bell_in_lap=False)
        PK.rot("spine", (lean * 0.5, 0, 0))
        PK.rot("chest", (lean * 0.5, 0, 0))
        PK.rot("head 1", (-lean * 0.6 - 4, 0, 0))
        M = k["arm"].matrix_local.inverted()                                     # boat space -> his armature space
        for sd, sx in (("L", -1), ("R", 1)):                                     # he faces -Y: his left is boat -X
            wren.reach(PK, sd, M @ Vector((sx * 0.75, hy, hz)), pole=(-sx * 1, 0.4, -0.4), hand=(0, -1, 0))
        PK.key(f)
        # the oars: from each hand through its oarlock out to the blade
        for i, (sd, sx) in enumerate((("L", -1), ("R", 1))):
            H = Vector((sx * 0.75, hy, hz))
            lock = b["locks"][0] if sx > 0 else b["locks"][1]
            d = (lock - H).normalized()
            oars[i].location = H
            oars[i].rotation_quaternion = Vector((0, 1, 0)).rotation_difference(d)
            oars[i].keyframe_insert("location", frame=f)
            oars[i].keyframe_insert("rotation_quaternion", frame=f)
        # Wren: seated in the stern, the bell in her lap, a slow breath; a small nod on "go with Wren"
        PW.reset()
        wren.sit(PW)
        nod = 6.0 * math.sin(math.pi * min(1.0, max(0.0, (f - f_go - 6) / 10)))
        PW.rot("chest", (1.2 * math.sin(f / 22.0), 0, 0))
        PW.rot("head 1", (-6 + nod, 0, 0))
        PW.key(f)
    X.v2._twos([k["arm"], w["arm"]] + oars)
    wren.grip(w, 1)
    wren.face(w, "worried", 1)
    wren.face(w, "stern", f_go + 4)
    wren.blink(w, 1, n, at=(f_go + 2,))
    _kai_face({"eye_brow_down": 0.5, "face_angry": 0.2}, 1)                         # set on it
    acting.blink(k, 1, n, seed=11)
    sh = _shoulder_shrimp(k, n, name="ep03_shrimp_s19", facing=head * -1, yaw=math.degrees(yaw_b) + 180)
    anim.on_twos(H9._shrimp_parts(sh), step=2)
    lt = N9.mark(k)                                                               # the coral key light
    # the camera: behind the stern quarter, low over the water, the boat and the lighthouse ahead; tracking
    cam = H9._new_cam("S19Acam", 1)
    for f in range(1, n + 1):
        e = _smooth((f - 1) / max(1, n - 1))
        bc = boat_at(f) + Vector((0, 0, 3.2))
        loc = bc - head * (31.0 - 3.0 * e) + side * 10.5 + Vector((0, 0, 7.5))
        tgt = bc + head * 10.0 + Vector((0, 0, 1.5))
        H9._key_cam(cam, f, loc, H9._look(tgt - loc), 27.0, (bc - loc).length, shift_y=-0.27, blur=4.0,
                    haze=(6.0, 24.0))
    H9._linear(cam, cam.data)
    sc.render.use_border = True
    sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
    sc.render.border_min_y, sc.render.border_max_y = 0.46, 1.0                # rows 0-691: the top panel
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]])


SHOTS = {"S02": s02, "S19top": s19top}
