"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 6:

    S23c "The shrimp had no idea." Dramatic irony (coordinator): the puff-shrimp keeps drinking at the pond's east
         edge (MAP["shrimp_drink"]), facing south, its claw dipped in the water, eyes shut in bliss (lids down, one
         happy flutter), little sips with sip bubbles and a sway on 2s. Behind it, soft in the background: the thorn
         tree with the dark butcher bird on top (as in S24 A). The bird's crisp spread-wing shadow (S24 A's tone and
         edge) sweeps in from the tree's side, grows a little as the bird comes and settles over the shrimp; through
         the handle it keeps S24 A's slow creep. A low camera from the pond side (west-south-west), the shrimp in
         the lower third, Kai (knocked flat to the south-west) out of the frame, pushing in slowly on 1s.

The set is the island after v3's snap exactly as S23b and S24 have it (diorama_v3/xprl._set: bgqrs v3's set with the
grove's stumps, Kai knocked flat in LYING_V3_L beyond the pond); the shrimp is placed by diorama_v3/xprl._shrimp(); the shadow is
tuftwing's, softened as in XprL's S23 insert.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S23c OUT_DIR [--still N --scale 0.5]
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as dx
from channels.monsters.diorama_v3 import xprl as v3x
from channels.monsters.diorama_v3.shots import v3_frames
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import acting, anim, diorama, look


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


SHRIMP = v3x.SHRIMP
CAM = (20.0, 26.0, 40.0, 0.27)         # dist, tilt, lens, shift_y: low, the shrimp in the lower third, the whole
                                        # spread-wing shadow, the thorn tree and the bird on top all in the frame
TURN = 12.0                             # degrees off the thorn-tree line, toward the shrimp's face (it faces south)
END_BACK = 1.5                          # where the shadow settles: its body 1.5 behind the shrimp, the head over it
HAZE = (1.15, 3.0)                      # mist start, depth (x dist): the tree and the dark bird stay readable


def _bubbles(sh, n, period=18, seed=5):
    """Little sip bubbles: as the claw dips back in after each sip, two or three tiny bubbles rise from its tip at the
    water line, swell a little and pop (on 2s)."""
    rnd = random.Random(seed)
    mat = look.toon("s23c_bubble", look.hexc("#eaf8ff"), shade=0.9, gloss=True)
    f = 2 + period - 3
    k = 0
    while f + 8 <= n:
        tip = x3._claw_tip(sh, f)
        for j in range(rnd.choice((2, 3))):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1.0)
            b = bpy.context.object
            b.name = f"s23c_bubble{k}"
            k += 1
            b.data.materials.append(mat)
            r = rnd.uniform(0.05, 0.09)
            x0 = tip + Vector((rnd.uniform(-0.15, 0.15), rnd.uniform(-0.15, 0.15), 0.02))
            g0 = f + 2 * j
            g1 = g0 + rnd.choice((6, 8))
            anim.key(b, "scale", 1, (0.001,) * 3, "CONSTANT")
            anim.key(b, "scale", g0, (r * 0.6,) * 3, "CONSTANT")
            anim.key(b, "location", g0, tuple(x0), "CONSTANT")
            for g in range(g0 + 2, g1 + 1, 2):
                u = (g - g0) / (g1 - g0)
                anim.key(b, "scale", g, (r * (0.6 + 0.5 * u),) * 3, "CONSTANT")
                anim.key(b, "location", g, tuple(x0 + Vector((0.03 * u, 0, 0.35 * u))), "CONSTANT")
            anim.key(b, "scale", g1 + 2, (0.001,) * 3, "CONSTANT")             # pop
        f += period


def _bliss(sh, n):
    """Eyes shut contentedly (the lids nearly down, highlights hidden), with one slow happy flutter mid-shot."""
    anim.lids(sh, 1, 0.9)
    anim.lids(sh, 26, 0.75)
    anim.lids(sh, 30, 0.9)
    for e in sh["eyes"]:                                       # no blink under the shut lids (x3's blink at 40)
        for f in (39, 41, 43):
            anim.key(e, "scale", f, (1, 1, 1), "CONSTANT")


def _shadow_in(bird, n, f_land=48):
    """The bird's shadow as S24 A has it (a crisp silhouette, wings spread, tone and edge the same), sweeping in from
    the thorn tree's side and settling over the shrimp, growing a little as the bird comes down: at f_land it is
    exactly S24 A's first frame (place and scale), and through the handle it keeps S24 A's slow creep and growth."""
    over = Vector((SHRIMP[0] - 0.3, SHRIMP[1] - 0.2, 0.0))   # S24 A's (c76631e): body under the shrimp at its end
    n24 = v3x._frames("S24", 162)
    perch = Vector((bird["root"].location.x, bird["root"].location.y, 0.0))
    back = (perch - over).normalized()
    dx._soft_shadow(bird, tuple(over + back * END_BACK - perch), (0.0, 0.0, 0.0), 1, 2,
                    tone="#1d2440", opacity=0.78, soften=1.0, shrink=0.8)
    sh = bird["shadow"]
    sh.animation_data_clear()
    to_local = sh.parent.matrix_world.to_3x3().inverted()
    l_end = sh.location.copy()
    l_start = l_end + to_local @ (back * 11.0)
    creep = to_local @ (-back * 4.0 / (n24 - 1))               # S24 A: 4 units over its frames
    for f in range(1, n + 1):
        if f <= f_land:
            u = (f - 1) / (f_land - 1)
            e = 1 - (1 - u) ** 3                               # sweeps in fast, settles
            loc, s = l_start.lerp(l_end, e), 0.78 + 0.22 * e
        else:
            loc, s = l_end + creep * (f - f_land), 1.0 + 0.35 * (f - f_land) / (n24 - 1)
        anim.key(sh, "location", f, tuple(loc), "LINEAR")
        anim.key(sh, "scale", f, (s, s, 1), "LINEAR")


def s23c():
    n = v3_frames("S23c")
    diorama.setup()
    isl, kai = v3x._set(n, kai_down=True)                     # v3's after-snap set, as S23b and S24 either side
    sh = v3x._shrimp(n)
    _sipping(sh, n)
    _bliss(sh, n)
    dx._twos([sh["shoulder"], sh["body"]] + sh["eyes"] + sh["lids"] + sh["hi"])
    _bubbles(sh, n)
    perch = Vector(isl["thorn"]["perch"])
    bird = v3x._bird_on_perch(perch, Vector(SHRIMP))           # dark on its thorn, as in S24 A: soft behind the shrimp
    _shadow_in(bird, n)
    # low, from the pond side (west-south-west, the line from the thorn tree through the shrimp): its blissful face,
    # the thorn tree and the dark bird soft behind it; Kai (south-south-west) stays out of the narrow frame
    face = Vector(SHRIMP) + Vector((0.0, 0.0, 1.0))
    yaw = math.degrees(math.atan2(perch.x - face.x, perch.y - face.y))
    a = (tuple(face), CAM[0], CAM[1], yaw + TURN - 1.0, CAM[2], CAM[3])
    b = (tuple(face), CAM[0] * 0.88, CAM[1], yaw + TURN + 1.0, CAM[2], CAM[3])
    dx._move("cam_s23c", 1, n, a, b, n)
    ms = bpy.context.scene.world.mist_settings                # the haze reaches the tree softly, not as a wall
    for f in range(1, n + 1):
        d = CAM[0] * (1 - 0.12 * dx._smooth((f - 1) / (n - 1)))
        ms.start, ms.depth = d * HAZE[0], d * HAZE[1]
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return dict(frames=n, step=1, subject=[sh["root"]])


SHOTS = {"S23c": s23c}
