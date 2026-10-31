"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 6:

    S23c "The shrimp had no idea." The puff-shrimp keeps drinking at the pond's east edge (MAP["shrimp_drink"]),
         facing south, its claw dipped west into the water, its back to the thorn tree (and to us): little sips
         (the claw lifts and dips), a sway, a blink. The butcher bird's giant winged shadow comes from the thorn
         tree's side, from behind the camera, slides across the grass and over the oblivious shrimp toward the pond.
         The bird itself is overhead, out of shot. A close diorama camera behind it (north-north-east, the bird's
         side), pushing in slowly on 1s.

The set is the island after the snap exactly as the other v3 shots have it (diorama/xprl._set: seed 31, the fan's
trees gone, Kai knocked flat beyond the pond); the shrimp is placed by diorama_v3/xprl._shrimp(); the shadow is
tuftwing's, softened as in XprL's S23 insert.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S23c OUT_DIR [--still N --scale 0.5]
"""
import math

from mathutils import Vector

from channels.monsters.diorama import xprl as dx
from channels.monsters.diorama_v3 import xprl as v3x
from channels.monsters.diorama_v3.shots import v3_frames
from channels.monsters.ep01v2 import helper5 as h5
from channels.monsters.mk import acting, diorama, tuftwing


def _sipping(sh, n, period=18, sway=0.05):
    """Small idle life while it drinks (mk/acting.py easing, on 2s): every `period` frames the claw lifts a little out
    of the water and dips back (a sip, with anticipation and overshoot), and the body sways side to side on a
    different rhythm, so it never freezes while the shadow slides over."""
    shoulder, body = sh["shoulder"], sh["body"]
    down, up = (1.76, 0.0, 0.0), (1.6, 0.0, 0.0)
    f = 2
    while f + period <= n:
        acting.move(shoulder, "rotation_euler", f, f + period // 2, down, up, kind="back", amount=0.08)
        acting.move(shoulder, "rotation_euler", f + period // 2, f + period, up, down, kind="back", amount=0.1)
        f += period
    f, side = 1, 1
    while f + 22 <= n + 22:
        acting.move(body, "rotation_euler", f, f + 22, (0, 0, -side * sway), (0, 0, side * sway), kind="inout")
        f, side = f + 22, -side


def s23c():
    n = v3_frames("S23c")
    diorama.setup()
    isl, kai = dx._set(n)
    sh = v3x._shrimp(n)
    _sipping(sh, n)
    shrimp = Vector((diorama.MAP["shrimp_drink"][0], diorama.MAP["shrimp_drink"][1], 0.0))
    thorn = Vector((diorama.MAP["thorn"][0], diorama.MAP["thorn"][1], 0.0))
    away = (shrimp - thorn).normalized()                       # the shadow travels from the thorn tree past the shrimp
    start = shrimp - away * 9.0                                # behind the camera, on the thorn tree's side
    bird = tuftwing.build((start.x, start.y, 0.0), shadow_span=10.0)
    bird["root"].scale = (h5.BIRD_SCALE,) * 3
    bird["root"].rotation_euler = (0, 0, math.atan2(away.x, -away.y))    # it heads (-Y local) toward the shrimp
    for o in bird["root"].children_recursive:                  # the bird is overhead, out of shot: only its shadow
        if o is not bird["shadow"]:
            o.hide_render = True
    dx._soft_shadow(bird, (0.0, 0.0, 0.0), tuple(away * 14.0), 1, n, opacity=0.7)
    target = shrimp + Vector((-0.6, -0.4, 1.0))
    # yaw 205: north-north-east of it, on the bird's side: its back to us, the dipped claw and the pond beyond, and
    # the shadow sliding in from under the lens and over it
    dx._move("cam_s23c", 1, n, (tuple(target), 34.0, 46.0, 205.0, 100.0, 0.0),
             (tuple(target), 28.0, 44.0, 209.0, 100.0, 0.0), n)
    return dict(frames=n, step=1, subject=[sh["root"]])


SHOTS = {"S23c": s23c}
