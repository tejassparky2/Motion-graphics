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
SHRIMP_K = 0.42                      # the puff-shrimp on his shoulder
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


def _shoulder_shrimp(k, n, name="ep03_shrimp_s02"):
    """The puff-shrimp riding on Kai's left shoulder, facing where he faces, breathing, blinking."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    sh["root"].scale = (SHRIMP_K,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW))
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        p = _bone_world(k, "upper_arm.L") + Vector((0, 0, 0.32))
        sh["root"].location = p
        sh["root"].keyframe_insert("location", frame=f)
    sc.frame_set(1)
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 20)
    sh["name"] = name
    return sh


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
    pa = k_face - fwd * 3.0 + left * 2.4 + up * 0.2
    for f in range(1, fb):
        e = _smooth((f - 1) / max(1, fb - 2))
        loc = pa.lerp(w_face, 0.10 * e)                             # a slow push in on her
        H9._key_cam(camA, f, loc, H9._look(w_face - loc), 62.0, (w_face - loc).length, shift_y=-0.06, blur=10.0,
                    haze=(4.0, 4.0))
    # B: her eyeline to the crack: the sky due north, RIFT_EL up; a slow push
    camB = H9._new_cam("S02b", fb)
    fwd_r, _ = H9._rift_dir()
    eye = w_face + fwd_r * 1.8                                     # just out in front of her face
    lens_b = H9.MATCH_PX / H9.RIFT_ANG * 36.0 / 1280 if hasattr(H9, "MATCH_PX") else 40.0
    for f in range(fb, fc):
        e = _smooth((f - fb) / max(1, fc - fb - 1))
        aim = (fwd_r + Vector((0, 0, -0.12 * (1 - e)))).normalized()   # a small tilt up as we hold
        H9._key_cam(camB, f, eye, H9._look(aim), lens_b * (1 + 0.05 * e), 400.0, blur=2.0, haze=(0.5, 1.5))
    # C: low in front of Kai (her side, beside her), looking up past his face and raised wrist to the crack above
    camC = H9._new_cam("S02c", fc)
    pc = X.KAI_AT + fwd * 4.6 - left * 1.6 + up * 2.6
    for f in range(fc, n + 1):
        e = _smooth((f - fc) / max(1, n - fc))
        tgt = k_face + up * (3.2 + 0.6 * e)                         # tilting up a touch as the echo lands
        loc = pc.lerp(k_face, 0.06 * e)
        H9._key_cam(camC, f, loc, H9._look(tgt - loc), 22.0, (k_face - loc).length, blur=6.0, haze=(3.0, 4.0))
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
        return dict(mark=H9._mark_geo(k, c), rift=H9._rift_geo(c), level=round(level(f), 3))
    _write_anchors("S02", n, geo, dict(fb=fb, fc=fc, f_echo=f_echo, f_sky=f_sky))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]])


SHOTS = {"S02": s02}
