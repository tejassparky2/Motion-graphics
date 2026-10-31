"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 6:

    S23c "The shrimp had no idea." The puff-shrimp keeps drinking at the pond's east edge (MAP["shrimp_drink"]),
         facing south, its claw dipped west into the water, its back to the thorn tree: little sips
         (the claw lifts and dips), a sway, a blink. The butcher bird's giant winged shadow comes from the thorn
         tree's side (upper left), slides across the grass, over the oblivious shrimp and out across the pond.
         The bird itself is overhead, out of shot. A close, high diorama camera west-north-west of it (the pond on the
         right), pushing in slowly on 1s.

The set is the island after v3's snap exactly as S23b and S24 have it (diorama_v3/xprl._set: bgqrs v3's set with the
grove's stumps, Kai knocked flat in LYING_V3_L beyond the pond); the shrimp is placed by diorama_v3/xprl._shrimp(); the shadow is
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
    isl, kai = v3x._set(n, kai_down=True)                     # v3's after-snap set, as S23b and S24 either side
    sh = v3x._shrimp(n)
    _sipping(sh, n)
    dx._twos([sh["shoulder"], sh["body"]])                     # the sip and sway keys on 2s too
    shrimp = Vector((diorama.MAP["shrimp_drink"][0], diorama.MAP["shrimp_drink"][1], 0.0))
    thorn = Vector((diorama.MAP["thorn"][0], diorama.MAP["thorn"][1], 0.0))
    away = (shrimp - thorn).normalized()                       # the shadow travels from the thorn tree past the shrimp
    start = shrimp - away * 7.0                                # behind the camera; it reaches the shrimp ~f30
    bird = tuftwing.build((start.x, start.y, 0.0), shadow_span=10.0)
    bird["root"].scale = (h5.BIRD_SCALE,) * 3
    bird["root"].rotation_euler = (0, 0, math.atan2(away.x, -away.y))    # it heads (-Y local) toward the shrimp
    for o in bird["root"].children_recursive:                  # the bird is overhead, out of shot: only its shadow
        if o is not bird["shadow"]:
            o.hide_render = True
    dx._soft_shadow(bird, (0.0, 0.0, 0.0), tuple(away * 14.0), 1, n, opacity=0.7)
    target = shrimp + Vector((-0.6, -0.4, 1.0))
    # yaw 120: west-north-west of it, looking east-south-east and well down: Kai (south-south-west) is out of shot,
    # we see it side-on with the claw dipped in the pond, and the shadow slides in from the thorn tree's side (upper
    # left), over the shrimp and out across the water (right)
    dx._move("cam_s23c", 1, n, (tuple(target), 30.0, 46.0, 120.0, 100.0, 0.0),
             (tuple(target), 25.0, 44.0, 124.0, 100.0, 0.0), n)
    return dict(frames=n, step=1, subject=[sh["root"]])


SHOTS = {"S23c": s23c}
