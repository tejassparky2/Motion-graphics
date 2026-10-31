"""Episode 1 v3, 2.5D diorama (channels/monsters/DIORAMA_EP01_V3.md): helper 5's S19, S20, S21, the end of the chest
scene on the "after" island (bGqrs's world: the smoking stumps, the sunbeam, the dust), with Kai in the v3 lying pose
(acting.LYING_V3) and the acting library's blinks, eyes and expressions. Every shot has a slow camera move on 1s.

    S19 "So I didn't move. I let the sun dry it." Close and low over his face and the claw: the last drop on the claw
        tip shrinks away in the sun (gone a little after the line). His face is set, his eyes on the drop, blinking;
        the shrimp glares, blinks once. A slow push-in. (helper 1's 2D pass adds the sweat and the sun glare.)
    S20 "It tried to finish me anyway." The shrimp winds up at his nose and SNAPS: only a tiny "pff" of dust. It
        startles (acting.hop), then turns to stare at its dry claw and tilts its head. Cut (CUT) to Kai's deadpan face,
        held (helper 1's 2D pass: dot eyes and a sweat drop). A push-in on each camera.
    S21 "Then it stomped back to the puddle." The toy-world wide: it turns its back on him in a huff, hops off his
        chest and struts (acting.strut: chest up, bouncing steps) to the pond's east edge (MAP["shrimp_drink"]),
        turns to face south (SHRIMP_DRINK_YAW) and dips its claw west into the water (the "plip" ripple). Kai's eyes
        follow it. The camera drifts with it.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S19 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import bgqrs as d16                 # the after-island, the shrimp on his chest, dust
from channels.monsters.diorama import helper5 as v2                 # puff, ripple, framing helpers
from channels.monsters.diorama_v3.shots import v3_frames
from channels.monsters.ep01v2 import bgqrs as s3d                  # Kai's face points, the claw poses, the drop
from channels.monsters.mk import acting, anim, diorama, hero

BLUR = 12.0
LAST = {}                                                          # the last built rig and shrimp (framing checks)
UP, EAST = d16.UP, d16.EAST                                        # along Kai toward his head; his left side


def _frames(shot, fallback):
    try:
        return v3_frames(shot)
    except (OSError, KeyError):                                    # timing.json not in yet
        return fallback


def _world(n, breathe=True):
    """bGqrs's after-the-snap island and light, with Kai in LYING_V3 (head toward the pond) and the shrimp on his
    chest, its claw cocked beside his face. breathe=False clears the shrimp's idle breathing for shots that key its
    body themselves."""
    diorama.setup()
    d16._set(n)
    rig = hero.load((0, 0, 0), scale=s3d.KAI_SCALE, outfit="world")
    acting.lie(rig, d16.HIPS, d16.HEAD_DIR)
    hero.line_width(rig, 0.0025)
    sh = d16._shrimp(rig, n)
    if not breathe:
        for fc in anim.all_fcurves(sh["body"].animation_data.action):
            if fc.data_path == "scale":
                fc.keyframe_points.clear()
        anim.squash(sh["body"], 1, 0.0)
    diorama.sunbeam(s3d.kai_point(rig, "chest"), radius=7.0)
    d16._dust(rig, n)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    LAST.update(rig=rig, sh=sh)
    return rig, sh


def _push(name, target, f0, f1, tilt, dist0, dist1, lens, yaw=0.0, frame=None, follow=None):
    """A diorama camera on `target` pushing in from dist0 to dist1 between f0 and f1 (smoothstep, keyed on 1s), the
    tilt-shift f-stop and the haze re-solved every frame. Bound to its first frame by a marker when `frame` is set."""
    sc = bpy.context.scene
    cam = diorama.camera(name, target, dist=dist0, tilt=tilt, yaw=yaw, lens=lens, blur=BLUR,
                         frame=frame if frame is not None else f0)
    el, az = math.radians(tilt), math.radians(yaw)
    back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    for f in range(f0, f1 + 1):
        u = acting.ease((f - f0) / max(1, f1 - f0), "inout")
        d = dist0 + (dist1 - dist0) * u
        cam.location = (follow(u) if follow else Vector(target)) + back * d
        cam.data.dof.focus_distance = d
        cam.data.dof.aperture_fstop = diorama.fstop_for(d, lens, BLUR)
        cam.keyframe_insert("location", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        ms = sc.world.mist_settings
        ms.start, ms.depth = d * 0.97, d * 0.55
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return cam


def _anchors(shot, n, cam, rig, sh, extra=None):
    """Screen positions (720x1280, top-left origin) of his eyes, nose and temple and the claw tip (plus `extra`:
    name -> fn() -> world point) on every frame, through `cam` or each frame's marker camera (cam=None), for helper
    1's 2D pass: build/monsters/diorama_v3/<SHOT>_anchors.json (same format as diorama/bgqrs._anchors)."""
    import json
    import os
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        c = cam or sc.camera
        pts = {k: s3d.kai_point(rig, k) for k in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        pts["tip"] = s3d.claw_tip(sh)
        for k, fn in (extra or {}).items():
            pts[k] = fn()
        row = {}
        for k, p in pts.items():
            v = world_to_camera_view(sc, c, p)
            row[k] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
        out[f] = row
    folder = os.path.join(d16.ROOT, "build", "monsters", "diorama_v3")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def _subject(rig, sh):
    return [rig["arm"], sh["root"]] + list(rig.get("cap", []))


# ---------------------------------------------------------------- S19

def s19():
    """S19: the last drop on the claw tip dries away in the sun; his set face, eyes on the drop, blinking."""
    n = _frames("S19", 105)
    rig, sh = _world(n)
    tip = s3d.claw_tip(sh) + Vector((0.0, 0.0, -0.08))
    d = s3d._drop(tip, 1, n + 40, n + 46, tip - Vector((0, 0, 2)), r=0.22)
    d.animation_data_clear()                                       # only the drying: no swell, no fall
    d.location = tip
    gone = min(90, n - 12)
    for f, k in ((1, 1.0), (round(gone * .27), 0.85), (round(gone * .5), 0.66), (round(gone * .73), 0.42),
                 (round(gone * .9), 0.18), (gone, 0.001)):
        anim.key(d, "scale", f, (k, k, k * 1.2), "LINEAR")
    anim.key(d, "scale", n, 0.001, "CONSTANT")
    anim.on_twos([d], step=2)
    eyes = s3d.kai_point(rig, "eyes")
    s3d.kai_face(rig, 1, eye_brow_down=0.45, mouth_short=1.0, eye_open=0.2)   # set, holding still
    acting.blink(rig, 1, n, seed=19, at=(58,))
    acting.look_at(rig, tip, 1, n, seed=19, strength=0.6)          # eyes on the drying drop, small darts
    acting.glare(sh, eyes, 1)
    anim.lids(sh, 36, 1.0)                                         # the shrimp blinks once, then glares again
    acting.glare(sh, eyes, 39)
    face = s3d.kai_point(rig, "nose")
    tgt = face.lerp(tip, 0.5)
    cam = _push("cam_s19", tgt, 1, n, 60.0, 42.0, 37.0, 120.0)
    v2._center(cam, [eyes, tip, v2._seye(sh), sh["root"].matrix_world.translation.copy()], (0.42, 0.3))
    _anchors("S19", n, cam, rig, sh)                              # for helper 1's 2D pass (sweat, glare)
    return dict(frames=n, step=2, ones=(1, n), subject=_subject(rig, sh))


# ---------------------------------------------------------------- S20

WIND, SNAP, CUT = 20, 32, 70                                       # S20 beats: "finish" f20, "anyway" f31-36 (timing.json)


def s20():
    """S20: wind-up, the futile snap, a startled hop, the stare at its dry claw; cut to his deadpan face."""
    n = _frames("S20", 110)
    rig, sh = _world(n, breathe=False)
    nose = s3d.kai_point(rig, "nose")
    eyes = s3d.kai_point(rig, "eyes")
    root = sh["root"].matrix_world.translation.copy()
    windup = s3d.raise_claw(sh, root - UP * 1.2 + EAST * 0.4 + Vector((0, 0, 3.6)), nose)  # high over its head
    jab = s3d.raise_claw(sh, nose + EAST * 0.5 + UP * 0.1 + Vector((0, 0, 0.8)), nose)      # down at his nose
    stare = s3d.raise_claw(sh, root + UP * 1.2 + EAST * 0.6 + Vector((0, 0, 2.6)),
                           root + Vector((0, 0, 1.4)))                                       # up before its own face
    sh["shoulder"].rotation_euler = sh["cock"]
    bpy.context.view_layer.update()
    k = s3d._key_pose
    k(sh, 1, sh["cock"], 1.4, 0.0)
    k(sh, WIND - 8, sh["cock"], 1.4, 0.0)
    k(sh, WIND - 4, sh["cock"], 1.4, 0.04)                         # a breath in...
    k(sh, WIND, windup, 1.5, -0.1)                                 # wind-up: cocked back, body squashed
    k(sh, SNAP - 2, windup, 1.5, -0.12)
    k(sh, SNAP, jab, -0.25, 0.1, "LINEAR")                         # SNAP... nothing happens
    k(sh, SNAP + 4, jab, -0.25, 0.0)
    acting.hop(sh, SNAP + 6, height=0.5)                           # startled by its own dud
    k(sh, SNAP + 18, jab, -0.25)
    k(sh, SNAP + 24, stare, 0.4)                                   # brings the claw round in front of its face
    body = sh["body"]
    anim.key(body, "rotation_euler", SNAP + 18, (0, 0, 0))
    anim.key(body, "rotation_euler", SNAP + 22, (0, 0, math.radians(-22)))                 # turns to stare
    anim.key(body, "rotation_euler", SNAP + 26, (0, math.radians(-16), math.radians(-20)))  # ...and tilts its head
    anim.key(body, "rotation_euler", n, (0, math.radians(-14), math.radians(-20)))
    acting.glare(sh, eyes, 1)                                      # locked on through the wind-up and the snap
    s3d.unlock(sh, SNAP + 6)                                       # ...nothing happened: wide, blank eyes
    anim.lids(sh, SNAP + 24, 0.3)
    anim.lids(sh, SNAP + 28, 0.0)
    anim.on_twos([sh["shoulder"], sh["hinge"], body], 2)
    sc = bpy.context.scene
    sc.frame_set(SNAP)
    v2._puff(s3d.claw_tip(sh) + Vector((0, 0, 0.05)), SNAP, n=4, size=0.42, seed=2)   # the sad "pff"
    sc.frame_set(1)
    acting.expression(rig, "terror", 1)
    acting._key("eye_close", 1, 0.0)                               # (open until the squeeze)
    acting._key("eye_close", SNAP - 3, 0.0)
    acting._key("eye_close", SNAP - 2, 1.0)                        # squeezes his eyes shut for the snap...
    acting.expression(rig, "fear", SNAP + 4)                       # ...opens them: nothing
    acting._key("eye_close", SNAP + 4, 0.0)
    acting.expression(rig, "deadpan", CUT)
    acting.blink(rig, 1, SNAP - 8, seed=20)
    acting.blink(rig, CUT + 2, n, seed=20, at=(CUT + 20,))
    acting.look_at(rig, s3d.claw_tip(sh), 1, SNAP - 4, seed=20)
    acting.look_at(rig, root + Vector((0, 0, 1.5)), CUT, n, seed=21, strength=0.5)   # at the shrimp, flat
    camA = _push("cam_s20_shrimp", root.lerp(nose, 0.35) + Vector((0, 0, 1.0)), 1, CUT - 1, 58.0, 40.0, 35.0,
                 120.0, yaw=-150.0)                                  # from past his head: the shrimp's face and claw
    v2._center(camA, [eyes] + v2._track(lambda: [s3d.claw_tip(sh), v2._seye(sh),
                                                 sh["root"].matrix_world.translation.copy()],
                                        (1, WIND, SNAP, SNAP + 26)), (0.45, 0.35))
    camB = _push("cam_s20_kai", eyes + UP * 0.15, CUT, n, 55.0, 30.0, 27.0, 120.0, frame=CUT)
    v2._center(camB, [eyes], (0.42, 0.33))
    sc.camera = camA
    _anchors("S20", n, None, rig, sh)                             # through each frame's camera (the cut)
    return dict(frames=n, step=2, ones=(1, n), subject=_subject(rig, sh))


# ---------------------------------------------------------------- S21

def s21():
    """S21: it turns its back on him, hops off his chest and struts to the pond's east edge, then dips its claw."""
    n = _frames("S21", 64)
    rig, sh = _world(n, breathe=False)
    r, body = sh["root"], sh["body"]
    p0 = r.location.copy()
    lean0 = tuple(r.rotation_euler)
    drink = Vector((*diorama.MAP["shrimp_drink"], 0.0))
    pond = Vector((*diorama.MAP["pond"], 0.0))
    down = Vector((p0.x, p0.y, 0)) + EAST * 2.2 - UP * 0.4         # beside him, on its claw side
    mid = down.lerp(drink, 0.5) + EAST * 0.6                       # a swaggering curve, not a beeline
    t0, t1 = 10, n - 22                                            # off his chest at t0; the strut ends at t1

    def yaw_to(a, b):
        v = b - a
        return math.atan2(v.x, -v.y)                               # local -Y (its face) toward b

    anim.key(r, "rotation_euler", 1, lean0, "CONSTANT")
    anim.key(r, "rotation_euler", 4, lean0, "CONSTANT")
    anim.key(r, "rotation_euler", 6, (0, 0, yaw_to(p0, down)), "CONSTANT")   # stands up, turns its back on him
    s3d._key_pose(sh, 1, sh["cock"], 0.5)
    s3d._key_pose(sh, 6, (0.0, 0.5, 0.0), 0.0)                    # claw up at its side
    anim.squash(body, 1, 0.0, "CONSTANT")
    anim.squash(body, 4, 0.12, "CONSTANT")                         # a huffy puff-up...
    anim.squash(body, 6, -0.14, "CONSTANT")                        # ...crouch (anticipation)
    anim.key(r, "location", 1, p0, "CONSTANT")
    anim.key(r, "location", 6, p0, "CONSTANT")
    anim.key(r, "location", 8, p0.lerp(down, 0.5) + Vector((0, 0, 1.0)), "CONSTANT")   # hops off his chest
    anim.key(r, "location", t0, down, "CONSTANT")
    anim.squash(body, 8, 0.2, "CONSTANT")
    anim.squash(body, t0, -0.22, "CONSTANT")                       # STOMP
    acting.strut(sh, [down, mid, drink], t0 + 2, t1)
    anim.key(r, "rotation_euler", t1 + 2, (0, 0, math.radians(diorama.SHRIMP_DRINK_YAW) - 0.25), "CONSTANT")
    anim.key(r, "rotation_euler", t1 + 4, (0, 0, math.radians(diorama.SHRIMP_DRINK_YAW)), "CONSTANT")  # faces south
    anim.squash(body, t1 + 2, -0.08, "CONSTANT")
    anim.squash(body, t1 + 4, 0.0, "CONSTANT")
    anim.key(r, "location", t1 + 2, drink, "CONSTANT")
    sc = bpy.context.scene
    sc.frame_set(t1 + 4)                                           # at the shore, facing south: claw west, into the water
    west = Vector((-1, 0, 0))
    over = s3d.raise_claw(sh, drink + west * 1.6 + Vector((0, 0, 2.4)), pond)
    dip = s3d.raise_claw(sh, drink + west * 2.2 + Vector((0, 0, -0.6)), pond)
    sc.frame_set(1)
    dip_f = t1 + 12
    s3d._key_pose(sh, t1, (0.0, 0.5, 0.0), 0.0)
    s3d._key_pose(sh, t1 + 6, over, 0.0, interp="CONSTANT")       # claw up over the water...
    s3d._key_pose(sh, dip_f - 2, over, 0.0, interp="CONSTANT")
    s3d._key_pose(sh, dip_f, dip, 0.3, interp="CONSTANT")          # ...and dips it in
    anim.on_twos([sh["shoulder"], sh["hinge"]], 2)
    sc.frame_set(dip_f)
    tip = s3d.claw_tip(sh)
    v2._ripple((tip.x, tip.y, 0.03), dip_f)
    sc.frame_set(1)
    v2._puff(down + Vector((0, 0, 0.15)), t0, n=4, size=0.45, seed=10, name="stomp")   # the landing off his chest
    acting.expression(rig, "deadpan", 1)
    acting.blink(rig, 1, n, seed=22)
    acting.look_at(rig, p0 + Vector((0, 0, 1.0)), 1, t0, seed=22, strength=0.6)       # eyes follow it off...
    acting.look_at(rig, mid + Vector((0, 0, 1.0)), t0 + 2, t1 - 6, seed=23, strength=0.6)
    acting.look_at(rig, drink + Vector((0, 0, 1.0)), t1 - 4, n, seed=24, strength=0.6)  # ...to the puddle
    a = Vector((p0.x, p0.y, 0)).lerp(s3d.kai_point(rig, "eyes"), 0.4)   # him and the shrimp on his chest...
    b = drink.lerp(Vector((p0.x, p0.y, 0)), 0.3)                    # ...drifting with the strut to the puddle
    cam = _push("cam_s21", a, 1, n, 58.0, 62.0, 56.0, 120.0, yaw=20.0,
                follow=lambda u: a.lerp(b, u))
    cam.data.shift_x, cam.data.shift_y = 0.06, -0.12                 # the action up and left of the Shorts rail
    _anchors("S21", n, cam, rig, sh, extra={"shrimp": lambda: r.matrix_world.translation.copy()})
    return dict(frames=n, step=2, ones=(1, n), subject=_subject(rig, sh))


SHOTS = {"S19": s19, "S20": s20, "S21": s21}
