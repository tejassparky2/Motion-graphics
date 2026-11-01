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
def s17():
    n = _frames("S17", 84)
    _world(n)
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
    f_stop = max(30, n - 26)
    ring_until = 20

    def upper(P, t):
        f = 1 + t * (f_stop - 1)
        swing = math.sin(f / 3.0) * 6
        wren.hold_bell(P, 0.25, shake=(18 * math.sin(f * 1.6)) if f < ring_until else swing)
        P.rot("chest", (-4, 0, 0))
        P.rot("head 1", (-6, 0, 0))                                   # chin up
    feet = wren.march(w, PW, ((0, 0, 0), (0, -dist, 0)), 1, f_stop, step_len=0.31, upper=upper, every=2)
    mid = (feet["L"] + feet["R"]) / 2
    for f, lean, chin in ((f_stop + 2, 7, -8), (f_stop + 6, -3, -10), (f_stop + 10, 0, -8), (n, 0, -8)):
        PW.reset()                                                   # planted: overshoot forward, settle back
        PW.hips(Vector((mid.x, mid.y, 0)))
        for side in ("L", "R"):
            PW.leg(side, feet[side] + Vector((0, 0, PW.ankle_h)))
        wren.hold_bell(PW, 0.3)
        PW.rot("chest", (lean, 0, 0))
        PW.rot("head 1", (chin, 0, 0))
        PW.key(f)
    wren.grip(w, 1)
    wren.ring(w, 1, ring_until)
    wren.face(w, "stern", 1)
    wren.face(w, "stern", f_stop + 2, value=1.0)
    wren.blink(w, 1, n, at=(f_stop + 12,))
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
