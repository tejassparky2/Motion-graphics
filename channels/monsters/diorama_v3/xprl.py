"""Episode 1 v3, 2.5D diorama (channels/monsters/DIORAMA_EP01_V3.md): XprL's S23b and S24top (A).

    S23b "And it was looking at the shrimp." Close on the butcher bird on top of the thorn tree, already dark from S23
        (the top shadow and amber eye glints): its head tilts, then locks on (a snap toward the shrimp, the eyes
        narrow). Cut (CUT_POV) to its view from the perch: far below, the tiny shrimp at the pond, its back turned,
        drinking. Slow push-ins on 1s in both halves (the POV one tightens like a predator focusing).
    S24top (A) "Option A: save the shrimp that tried to kill me." (the top panel all through the 3-sentence line):
        the bird's giant shadow already lies over the shrimp at the pond, which keeps drinking; Kai runs in from the
        south-east, skids into a crouch beside it (anticipation, overshoot) and reaches an open hand over it, his face
        set (determined), glancing up at the sky between beats. The action stays in the top half (y 80-600) for the
        in-place split; the assembler adds the big A. Camera push-in on 1s.

The shrimp from S21's end on (coordinator's call, see SHRIMP): drinking at the pond's east edge, facing south (its
back to the thorn tree), its claw (right side) dipped west into the water.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S23b OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as v2
from channels.monsters.ep01v2 import helper5 as h5
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import acting, anim, diorama, hero, tuftwing

SHRIMP = (*diorama.MAP["shrimp_drink"], 0.0)  # the pond's east edge, its back to the thorn tree (coordinator, v3)
SHRIMP_YAW = diorama.SHRIMP_DRINK_YAW
BIRD_SCALE = h5.BIRD_SCALE


def _frames(shot, fallback):
    from channels.monsters.diorama_v3.shots import v3_frames           # (lazy: shots.py imports this module)
    try:
        return v3_frames(shot)
    except (OSError, KeyError):                                            # timing.json not in yet
        return fallback


def _shrimp(n, f_lift=None):
    """The puff-shrimp drinking at the pond's east edge, back to the thorn tree (x3._shrimp_wet, re-placed)."""
    x3.SHRIMP_AT = SHRIMP
    sh = x3._shrimp_wet(f_lift, n)
    sh["root"].rotation_euler = (0, 0, math.radians(SHRIMP_YAW))
    v2._twos([sh["shoulder"], sh["body"], sh["hinge"]] + sh["eyes"])
    bpy.context.view_layer.update()
    return sh


def _bird_on_perch(perch, face_to):
    """The butcher bird sitting on the top thorn, already dark (S23's rage light from frame 1), facing `face_to`."""
    rig = tuftwing.build((perch.x, perch.y, 0.0), shadow_span=10.0)
    rig["root"].scale = (BIRD_SCALE,) * 3
    d = Vector(face_to) - perch
    rig["root"].rotation_euler = (0, 0, math.atan2(d.x, -d.y))
    anim.key(rig["lift"], "location", 1, (0.0, 0.0, perch.z / BIRD_SCALE), "CONSTANT")
    h5._rage_light(rig, 1, perch.z + (tuftwing.CENTER[2] - 0.1) * BIRD_SCALE)
    return rig


# ------------------------------------------------------------------------------------------------------------ S23b
CUT_POV = 30                        # the cut to the bird's view (about where "looking" lands)


def s23b():
    n = _frames("S23b", 60)
    diorama.setup()
    isl, _ = v2._set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    prey = Vector(SHRIMP) + Vector((0, 0, 1.0))
    # the close: from the clearing side (the forest is behind the tree), 25 deg off the line to the shrimp, so when it
    # locks on its face turns three-quarter to the lens; before that it looks off to the side
    to_prey = prey - perch
    def turned(v, deg):
        c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return Vector((v.x * c - v.y * s_, v.x * s_ + v.y * c, 0)).normalized()
    side = turned(to_prey.xy.to_3d(), 25)
    bird = _bird_on_perch(perch, perch + turned(to_prey.xy.to_3d(), -70) * 10 - Vector((0, 0, 3)))
    acting.tilt(bird, 8, angle=0.42, hold=8)                                 # a curious tilt: one eye to the ground
    acting.lock_on(bird, prey, 20)                                          # snap onto the shrimp: glare, crest up
    anim.blink(bird, 4)
    anim.squash(bird["body"], 18, -0.06)                                    # a hunch into the lock
    anim.squash(bird["body"], 22, 0.03)
    anim.squash(bird["body"], 26, 0.0)
    v2._twos(tuftwing._animated(bird))
    eye_w = perch + Vector((0, 0, (tuftwing.CENTER[2] + 0.12) * BIRD_SCALE))
    yaw_close = math.degrees(math.atan2(side.x, side.y)) + 180              # camera on the `side` of the bird
    close = None
    for f in range(1, CUT_POV):
        k = (f - 1) / (CUT_POV - 2)
        close = v2._cam("cam_s23b_eye", f, tuple(eye_w), 13.0 - 3.0 * k, 34.0, yaw_close, 100.0, cam=close)
    # the bird's view: from just behind and above its head, down the line to the shrimp, a long lens tightening
    eye_pos = perch + Vector((0, 0, 1.6 * BIRD_SCALE)) - to_prey.normalized() * 1.2
    dist0 = (prey - eye_pos).length
    pov = None
    for f in range(CUT_POV, n + 1):
        k = (f - CUT_POV) / max(1, n - CUT_POV)
        d = dist0
        el = math.degrees(math.asin((eye_pos.z - prey.z) / d))
        yw = math.degrees(math.atan2((prey - eye_pos).x, (prey - eye_pos).y))   # the lens sits at the bird's eye
        pov = v2._cam("cam_s23b_pov", f, tuple(prey), d, el, yw, 30.0 + 10.0 * k, cam=pov)   # wide: it's tiny
    sc = bpy.context.scene
    for m in list(sc.timeline_markers):
        sc.timeline_markers.remove(m)
    for f, c in ((1, close), (CUT_POV, pov)):
        sc.timeline_markers.new(c.name, frame=f).camera = c
    sc.camera = close
    return dict(frames=n, step=2, ones=(1, n), subject=[bird["root"], sh["root"]])


# ----------------------------------------------------------------------------------------------------------- S24top
def s24top():
    n = _frames("S24", 162)
    diorama.setup()
    isl, _ = v2._set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    bird = _bird_on_perch(perch, Vector(SHRIMP))
    # its giant shadow on the ground over the shrimp, growing as it comes (the dive is in panel B)
    shadow = bird["shadow"]
    bpy.context.view_layer.update()
    to_local = bird["root"].matrix_world.inverted()
    for f, (w, s) in ((1, (0.55, 0.55)), (n // 2, (0.85, 0.8)), (n, (1.0, 1.0))):
        p = to_local @ (Vector(SHRIMP).lerp(Vector((perch.x, perch.y, 0)), 1.0 - w) + Vector((0, 0, 0.02)))
        anim.key(shadow, "location", f, tuple(p), "BEZIER")
        anim.key(shadow, "scale", f, (s, s, 1), "BEZIER")
    # Kai runs in from the east, skids, crouches at its side and reaches over it (facing west, three-quarter to us)
    reach_at = Vector((SHRIMP[0] + 3.6, SHRIMP[1] + 0.2, 0))
    facing = (Vector(SHRIMP) - reach_at).normalized()
    yaw = math.degrees(math.atan2(facing.x, -facing.y))
    start = reach_at - facing * 8.5
    k = x3._hero(tuple(start), yaw)
    hero.line_width(k, 0.0025)
    P = x3.Pose(k)
    path = (Vector((0, 0, 0)), Vector((0, -8.5 / 5.8, 0)))

    def run_upper(P, t):
        P.rot("spine", (18, 0, 0))
        P.rot("chest", (6, 0, 0))
        P.rot("head 1", (-22, 0, 0))                                        # face up to the lens: worried
        x3._arms_down(P, 25)
        P.aim("upper_arm.R", (-0.2, -0.5, -0.8))
        P.aim("forearm.R", (-0.1, -0.9, 0.1))
        P.aim("upper_arm.L", (0.2, 0.45, -0.8))
        P.aim("forearm.L", (0.1, -0.6, 0.4))

    def reach_upper(P, t):
        P.rot("spine", (20 + 8 * t, 0, 0))
        P.rot("chest", (6 + 2 * t, 0, 0))
        P.rot("neck", (-18 * t, 0, 0))
        P.rot("head 1", (-40 * t, 0, 0))                                    # chin up to the lens (and the sky)
        x3._arms_down(P, 12)
        P.aim("upper_arm.R", (-0.1, -0.85 - 0.1 * t, -0.35))                # reaching out over the shrimp
        P.aim("forearm.R", (-0.03, -0.98, -0.1))
        P.aim("hand.R", (0, -1, -0.15))
        P.twist("upper_arm.R", -90 * t)                                     # palm down, a cover over it
        P.aim("upper_arm.L", (0.35, -0.3, -0.85))                           # the other hand braced on his knee
        P.aim("forearm.L", (0.05, -0.75, -0.6))

    f_run = 34
    feet = x3._walk(P, k, path, 1, f_run, 0.48, "R", crouch=(0.04, 0.14), upper=run_upper, every=2)
    x3._squat(P, feet, f_run + 2, f_run + 18, 0.14, 0.42, reach_upper, every=2, hold_to=n)
    acting.EXPR.setdefault("determined", {"face_angry": 0.45, "eye_brow_down": 0.5, "mouth_wide": 0.25})
    acting.expression(k, "surprised", 1, value=0.7)
    acting.expression(k, "determined", f_run + 6)
    prey = Vector(SHRIMP) + Vector((0, 0, 1.0))
    sky = Vector((perch.x, perch.y, perch.z + 6.0))                         # where the bird is
    acting.look_at(k, prey, 1, n)
    for f in (f_run + 30, f_run + 76):                                      # quick glances up at the bird
        acting.look_at(k, sky, f, f + 10, darts=False)
        acting.look_at(k, prey, f + 12, f + 12, darts=False)
    acting.blink(k, 1, n, seed=7)
    v2._twos([k["arm"]])
    mid = Vector((SHRIMP[0] + 2.0, SHRIMP[1], 2.4))
    a = (tuple(mid + Vector((1.2, -0.4, 0.6))), 74.0, 46.0, 30.0, 80.0, -0.2)    # from the south-south-west
    b = (tuple(mid), 58.0, 46.0, 30.0, 92.0, -0.22)
    v2._move("cam_s24top_v3", 1, n, a, b, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"]])


SHOTS = {"S23b": s23b, "S24top": s24top}
