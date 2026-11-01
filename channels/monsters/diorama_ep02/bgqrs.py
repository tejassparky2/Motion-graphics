"""Episode 2 (2.5D diorama), bGqrs's shots (channels/monsters/DIORAMA_EP02.md):

    S01  "You said save it. So I ran at the butcher bird."   THE HOOK FRAME: a low, medium-close side shot. Kai sprints
         across the frame from camera-left toward the pond, his near (right) hand thrown out ahead of him; behind him,
         deeper in the frame, the butcher bird is already plunging from the thorn tree at the shrimp drinking on the
         pond's shore, its giant shadow racing over the grass. Moving from frame 0; the camera tracks with him on 1s.
    S03  "I got there half a second sooner."                 Kai slides in on his knees and scoops the shrimp up in cupped
         hands, with a splash.

The world is Episode 1 v3's after-the-snap island (diorama_v3/xprl._set: seed 31, the grove cut to stumps), the puff-
shrimp drinking on the pond's north-east shore (MAP["shrimp_drink"], its back to the thorn tree), and the butcher bird
in XprL's dark predator form (xprl.dark_form + helper 5's rage light) diving from the thorn tree's perch. Kai is the hero
(hero.load at KAI_SCALE) posed with XprL's FK/IK Pose; his face and eyes are mk/acting.py. Characters are keyed on 2s,
the camera on 1s.
"""
import math
import os

import bpy
from mathutils import Vector

import random

from channels.monsters.diorama import helper1 as d1                # _tilt_cap
from channels.monsters.diorama import xprl as xv2                  # _soft_shadow
from channels.monsters.diorama_v3 import bgqrs as b3              # _keycam, _subject, anchors
from channels.monsters.diorama_v3 import xprl as xv3              # the v3 set, the drinking shrimp, the dark form
from channels.monsters.ep01v2 import helper5 as h5                # the rage light
from channels.monsters.ep01v2 import xprl as x3                   # Pose (FK + leg IK), _hero
from channels.monsters.diorama_ep02 import helper4 as h4            # SHRIMP_IN_HAND (shared from S01 on)
from channels.monsters.mk import acting, anim, butcherbird, diorama, hero, look, tuftwing

KAI_SCALE = x3.SCALE                                              # 5.8: the 1.75 m hero in creature units
SHRIMP = Vector(xv3.SHRIMP)                                       # (4.2, -0.1, 0): drinking, facing south
BLUR = b3.BLUR
FALLBACK = {"S01": 66, "S03": 50}                                 # the counts before ep02/timing.json lands
ANCHORS = os.path.join(b3.ROOT, "build", "monsters", "diorama_ep02")   # per-frame screen anchors for the 2D pass


def _anchors(shot, n, cam, rig, sh=None, extra=None):
    """b3._anchors, written to the Episode 2 build folder."""
    os.makedirs(ANCHORS, exist_ok=True)
    keep = b3.ANCHORS
    b3.ANCHORS = ANCHORS
    try:
        b3._anchors(shot, n, cam, rig, sh, extra)
    finally:
        b3.ANCHORS = keep


def _frames(shot):
    from channels.monsters.diorama_ep02.shots import ep02_frames  # (lazy: shots.py imports this module)
    try:
        return ep02_frames(shot)
    except (OSError, KeyError, ValueError):
        return FALLBACK[shot]


def _shrimp(n):
    """The puff-shrimp drinking on the pond's north-east shore (xv3._shrimp) at helper 4's SHRIMP_IN_HAND scale, the
    size it has in his hands from S05 on, so it never changes size across the cut."""
    sh = xv3._shrimp(n)
    sh["root"].scale = (h4.SHRIMP_IN_HAND,) * 3
    bpy.context.view_layer.update()
    return sh


def _bird_shadow_look(rig):
    """The giant shadow as a clear, dark, soft-edged bird shape on the grass (XprL's S24 look)."""
    xv2._soft_shadow(rig, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1, 2, tone="#1d2440", opacity=0.8, soften=1.0,
                     shrink=0.6)


def _facing(d):
    """The armature's rot_z (degrees) that faces Kai along ground direction d (he faces his own -Y)."""
    return math.degrees(math.atan2(d.x, -d.y))


# ------------------------------------------------------------------------------------------------------- the bird
def _shadow_under(rig, n, perch):
    """The giant shadow decal rides on the grass under the bird (in the root's frame, like its lift), growing as it
    drops."""
    S = xv3.BIRD_SCALE
    rest = perch.z / S
    sh = rig["shadow"]
    z = sh.location.z
    for f in range(1, n + 3, 2):
        bpy.context.scene.frame_set(f)
        lx, ly, lz = rig["lift"].location
        anim.key(sh, "location", f, (lx, ly, z), "CONSTANT")
        k = 0.7 + 0.5 * max(0.0, 1.0 - lz / rest)
        anim.key(sh, "scale", f, (k, k, 1.0), "CONSTANT")
    bpy.context.scene.frame_set(1)


def _bird_dive(n, f0, f_hit, perch):
    """The butcher bird plunging from the perch at the shrimp's back: a crouch, then an accelerating dive (f0 -> f_hit;
    f_hit may lie past the shot, so it is still mid-air at the cut). Dark predator form from frame 1 (the whole ball
    in the top-shadow tone against the sky, amber eye glints). Its giant shadow decal rides on the grass under it,
    growing as it drops. Keyed on 2s."""
    rig = tuftwing.build((perch.x, perch.y, 0.0), shadow_span=10.0)
    S = xv3.BIRD_SCALE
    rig["root"].scale = (S, S, S)
    to = SHRIMP - Vector((perch.x, perch.y, 0.0))
    rot = math.atan2(to.x, -to.y)
    rig["root"].rotation_euler.z = rot
    rest = (0.0, 0.0, perch.z / S)
    anim.key(rig["lift"], "location", 1, rest, "CONSTANT")
    target = x3._local(rot, (to.x, to.y, 1.6), scale=S)               # onto the shrimp's back
    butcherbird.dive(rig, f0, f_hit, target, start=rest)
    tuftwing.beat(rig, max(1, f0 - 4))
    h5._rage_light(rig, 1, SHRIMP.z + (tuftwing.CENTER[2] - 0.1) * S)  # all of it dark during the dive
    xv3.dark_form(1)
    anim.on_twos(tuftwing._animated(rig), step=2)
    return rig


# ------------------------------------------------------------------------------------------------------ the sprint
def _sprint(P, f0, f1, dist, period=14, stride=0.62, drop=0.05, upper=None, every=2, lead=0.0):
    """A real sprint (not a fast walk) along the armature's -Y over f0..f1 covering `dist` armature units: each foot
    plants ahead of the hips, the body rides over it, it pushes off behind, the heel kicks up and the knee drives
    high and forward into the next strike; both feet leave the ground between strikes (the flight phase); the hips
    dip at each strike and float in the flight. `upper(P, t, ph)` poses the upper body (ph: the stride phase in
    radians, so the arms can pump against the legs). `lead` (frames) starts the cycle mid-stride, so he is already
    running at frame 0."""
    fwd = Vector((0, -1, 0))
    side = {"L": Vector((0.075, 0, 0)), "R": Vector((-0.075, 0, 0))}
    n = f1 - f0

    def base(f):                                                    # the hips' ground point at frame f
        return fwd * dist * ((f - f0) / max(1, n))

    def foot(sd, f):
        """Ankle target (armature space) of foot sd at frame f: stance 0-0.36 of its cycle, then swing."""
        ph = ((f - f0 + lead) / period + (0.0 if sd == "L" else 0.5)) % 1.0
        c0 = f - ph * period                                        # this cycle's strike frame
        stance = 0.36
        strike = base(c0) + fwd * stride * 0.48 + side[sd]
        if ph < stance:                                             # planted
            return strike, 0.0
        s = (ph - stance) / (1 - stance)                            # the swing: kick up behind, knee drive, reach
        nxt = base(c0 + period) + fwd * stride * 0.48 + side[sd]
        e = 0.5 - 0.5 * math.cos(math.pi * s)
        p = strike.lerp(nxt, e)
        p.z += 0.32 * math.sin(math.pi * s) ** 0.8                  # the knee drives high
        p += -fwd * 0.16 * math.sin(math.pi * min(1.0, s * 1.6))    # the heel kicks up behind early in the swing
        return p, s

    for f in range(f0, f1 + 1, every):
        t = (f - f0) / max(1, n)
        P.reset()
        b = base(f)
        ph = 2 * math.pi * ((f - f0 + lead) / period)
        bob = 0.035 * math.cos(2 * ph)                              # high in the flight, low at each strike
        P.hips(Vector((b.x, b.y - 0.05, -drop + bob)))              # the pelvis a little ahead: leaning into it
        for sd in ("L", "R"):
            p, _s = foot(sd, f)
            P.leg(sd, p + Vector((0, 0, P.ankle_h)))
        if upper:
            upper(P, t, ph)
        P.key(f)


def _open_hand(arm, side, f, spread=1.0):
    """Fingers straight and spread (a hand thrown out to grab), keyed CONSTANT at f."""
    pb = arm.pose.bones
    for i, fing in enumerate(("f_index", "f_middle", "f_ring", "f_pinky")):
        for j in (1, 2, 3):
            b = pb.get(f"{fing}.0{j}.{side}")
            if b is None:
                continue
            b.rotation_mode = "XYZ"
            b.rotation_euler = (0.0, 0.0, math.radians((i - 1.5) * 7 * spread) if j == 1 else 0.0)
            b.keyframe_insert("rotation_euler", frame=f)


# ----------------------------------------------------------------------------------------------------------- S01
# The race, on a long lens from beyond the shrimp (south-west of it, looking north-east up the bird's dive line): the
# shrimp small in the foreground at the pond's edge, Kai sprinting at the lens from the north-north-east on the left,
# his hand thrown out ahead at it, and the bird plunging from the thorn tree on the right behind him. The telephoto
# stacks all three in the portrait frame, so the shrimp, his face and the bird read together at phone size.
# (a projection search over his approach, yaw, tilt, distance and lens, frames 1 / mid / end: Kai in the left two
# thirds, head below y 90 and feet above 960; the shrimp at x 360-690, y 600-845, just above the caption band; the
# bird at x 300-690, y 80-760; his run 40 deg off the lens axis so the lean and the reach read; the biggest Kai that
# fits all of it, ~600 px of the 1280)
S01_BEARING = 20.0                     # where he comes from, seen from the shrimp (degrees from north)
S01_FROM, S01_TO = 12.0, 5.0           # his distance from the shrimp at the first and last frame (S03 brings him in)
S01_CAM = dict(yaw=60.0, tilt=7.0, dist=50.0, lens=105.0, toward=0.55, lift=2.1, push=2.5)
S01_DIVE = (0.28, 0.74)                # how far down its dive line the bird is at the first and last frame


def _s01_line():
    u = Vector((math.sin(math.radians(S01_BEARING)), math.cos(math.radians(S01_BEARING)), 0.0))
    return -u, SHRIMP + u * S01_FROM, SHRIMP + u * S01_TO


def _dive_line(rig, n, perch, frac, f_hit_pose=None):
    """Override the lift's location: the bird already mid-plunge at frame 1, accelerating down its line from the perch
    to the shrimp's back, frac[0] -> frac[1] of the way by frame n (keyed on 1s; on_twos holds it on 2s)."""
    lift = rig["lift"]
    act = lift.animation_data.action
    for fc in list(anim.all_fcurves(act)):
        if fc.data_path == "location":
            while fc.keyframe_points:
                fc.keyframe_points.remove(fc.keyframe_points[0])
    S = xv3.BIRD_SCALE
    rot = rig["root"].rotation_euler.z
    to = SHRIMP - Vector((perch.x, perch.y, 0.0))
    p0 = Vector((0.0, 0.0, perch.z / S))
    p1 = x3._local(rot, (to.x, to.y, 1.6), scale=S)
    for f in range(1, n + 3):
        u = (f - 1) / max(1, n - 1)
        k = frac[0] + (frac[1] - frac[0]) * u ** 1.25
        anim.key(lift, "location", f, tuple(p0.lerp(p1, k)), "LINEAR")


def s01():
    n = _frames("S01")
    diorama.setup()
    isl, _ = xv3._set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    bird = _bird_dive(n, 1, n + 30, perch)
    _dive_line(bird, n, perch, S01_DIVE)
    _bird_shadow_look(bird)
    _shadow_under(bird, n, perch)
    d, start, end = _s01_line()
    k = x3._hero(tuple(start), _facing(d))
    hero.line_width(k, 0.0028)
    d1._tilt_cap(k, 24.0)                                            # brim up: his eyes read from the low lens
    arm = k["arm"]
    P = x3.Pose(k)

    def upper(P, t, ph):
        s = math.sin(ph)
        P.rot("spine", (34, 0, 6 * s))                              # leaning hard into the sprint
        P.rot("chest", (8, 0, -8 * s))
        P.rot("neck", (-22, 0, 0))
        P.rot("head 1", (-20, 0, 0))                                # chin up: his eyes on the shrimp ahead
        # his right arm thrown out ahead, open hand reaching for the shrimp; it bobs with the stride
        P.aim("upper_arm.R", (-0.15, -0.95, 0.12 + 0.05 * s))
        P.aim("forearm.R", (-0.05, -0.99, 0.05 + 0.04 * s))
        P.aim("hand.R", (-0.02, -0.98, -0.02))
        # the left arm pumping hard against the legs
        P.aim("upper_arm.L", (0.26, -0.75 * s, -0.62))              # a big pump, kept low (never across his face)
        P.aim("forearm.L", (0.06, -0.85, 0.35 * max(0.0, s) - 0.3 * max(0.0, -s) - 0.05))

    _sprint(P, 1, n, (S01_FROM - S01_TO) / KAI_SCALE, upper=upper, lead=5)
    _open_hand(arm, "R", 1)
    acting.expression(k, "angry", 1, value=0.75)                     # set jaw, brows down: going for it
    acting.face_keys(k, 1, lip_a=0.55)                               # mouth open, breathing hard
    acting.look_at(k, tuple(SHRIMP + Vector((0, 0, 1.0))), 1, n, darts=False)
    acting.blink(k, 1, n, every=(40, 60), seed=5)
    anim.on_twos([arm], step=2)
    c = S01_CAM                                                      # the long lens tracks him on 1s
    cam = None
    for f in range(1, n + 1):
        u = (f - 1) / max(1, n - 1)
        hip = start.lerp(end, u)
        aim = hip.lerp(SHRIMP, c["toward"]) + Vector((0, 0, c["lift"]))
        if cam is None:
            cam = diorama.camera("cam_s01", tuple(aim), dist=c["dist"], tilt=c["tilt"], yaw=c["yaw"], lens=c["lens"],
                                 blur=BLUR)
        b3._keycam(cam, f, aim, c["tilt"], c["dist"] - c["push"] * u, c["lens"], c["yaw"])
        cam.data.dof.focus_distance = (cam.location - (hip + Vector((0, 0, 4.0)))).length   # focus on Kai
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    bpy.context.scene.camera = cam
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {arm, *arm.children_recursive, bird["root"], *bird["root"].children_recursive, sh["root"],
            *sh["root"].children_recursive}
    _clear_view(cam, [1, n // 2, n], start.lerp(SHRIMP, 0.5), keep)
    _anchors("S01", n, cam, k, sh)
    return dict(frames=n, step=2, ones=(1, n), subject=b3._subject(k, sh))


# ----------------------------------------------------------------------------------------------------------- S03
# "I got there half a second sooner." The same approach as S01 (from the north-north-east, heading down at the shrimp)
# and the same screen direction (he moves left to right): seen low from the west, over the pond's edge, so the scoop
# and the splash are in front and his face reads in three-quarter. His last stride drops him onto his knees; he slides
# in, both hands reaching down; they scoop the shrimp out of the shallows with a splash and bring it up to his chest
# in a cup, and he hunches over it. Then the bird's shadow sweeps over him from behind (S04: the talons).
S03_CAM = dict(yaw=100.0, tilt=14.0, dist=30.0, lens=85.0, lift=2.6)
S03_BEATS = dict(kneel=6, slide=10, scoop=22, lift=28, hold=36, shadow=44)
S03_SLIDE = (4.6, 1.15)                # his knees' distance from the shrimp: where the slide starts, where it stops


def _kneel_legs(P, hip_ground, drop):
    """Both knees down, shins flat behind, the tops of the feet on the ground (armature space)."""
    for sd, x in (("L", 0.085), ("R", -0.085)):
        ank = hip_ground + Vector((x, 0.30, P.ankle_h * 0.55))
        P.leg(sd, ank)
        P.aim(f"foot.{sd}", (0.0, 0.92, -0.38))                    # toes back, sole up


def _cup_hands(arm, f, curl=1.0):
    """Fingers curled into a cup (CONSTANT keys at f)."""
    pb = arm.pose.bones
    for sd in ("L", "R"):
        for fing in ("f_index", "f_middle", "f_ring", "f_pinky"):
            for j, a in ((1, 22), (2, 30), (3, 24)):
                b = pb.get(f"{fing}.0{j}.{sd}")
                if b is not None:
                    b.rotation_mode = "XYZ"
                    b.rotation_euler = (math.radians(a * curl), 0.0, 0.0)
                    b.keyframe_insert("rotation_euler", frame=f)
        for j in (1, 2, 3):
            b = pb.get(f"thumb.0{j}.{sd}")
            if b is not None:
                b.rotation_mode = "XYZ"
                b.rotation_euler = (math.radians(12 * curl), 0.0, 0.0)
                b.keyframe_insert("rotation_euler", frame=f)


def _splash(at, f, n=26, seed=5, up=2.6, out=2.2, life=14):
    """A splash: water drops thrown up and out from `at` in parabolas (on 1s), shrinking as they fall back, plus a
    flat ring on the water that spreads and fades."""
    rnd = random.Random(seed)
    m = bpy.data.materials.get("drip") or look.flat("drip", look.hexc("#9fd8ff"))
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        v = Vector((math.cos(a) * out * rnd.uniform(0.4, 1.0), math.sin(a) * out * rnd.uniform(0.4, 1.0),
                    up * rnd.uniform(0.6, 1.2)))
        r = rnd.uniform(0.09, 0.2)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=r, location=at)
        d = bpy.context.object
        d.name = f"splash_{i}"
        d.data.materials.append(m)
        for pg in d.data.polygons:
            pg.use_smooth = True
        L = int(life * rnd.uniform(0.7, 1.1))
        anim.key(d, "scale", f - 1, (0.001,) * 3, "CONSTANT")
        for k in range(0, L + 1):
            u = k / L
            p = Vector(at) + Vector((v.x * u, v.y * u, v.z * (u - u * u) * 4 * 0.5))
            anim.key(d, "location", f + k, tuple(p), "LINEAR")
            sc = 1.0 if u < 0.6 else max(0.001, 1 - (u - 0.6) / 0.4)
            anim.key(d, "scale", f + k, (sc, sc, sc * (1.3 if u < 0.3 else 1.0)), "LINEAR")
    bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1.0, fill_type="NOTHING", location=(at[0], at[1], 0.05))
    ring = bpy.context.object
    ring.name = "splash_ring"
    ring.data.materials.append(m)
    mod = ring.modifiers.new("w", "WIREFRAME")
    mod.thickness = 0.08
    for k, (sc_, a) in enumerate(((0.2, 1), (1.6, 1), (2.8, 0))):
        anim.key(ring, "scale", f + k * 7, (sc_, sc_, 1.0), "LINEAR")
    anim.key(ring, "scale", f - 1, (0.001,) * 3, "CONSTANT")
    anim.key(ring, "scale", f + 16, (0.001,) * 3, "CONSTANT")


def s03():
    n = _frames("S03")
    B = S03_BEATS
    diorama.setup()
    isl, _ = xv3._set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    d, _s, _e = _s01_line()                                          # the same approach line as S01 (heading SSW)
    k0, k1 = SHRIMP - d * S03_SLIDE[0], SHRIMP - d * S03_SLIDE[1]   # the knees' slide
    run_in = 0.9 * KAI_SCALE / 5.8 * 3.0                             # the last stride before he drops (units)
    start = k0 - d * run_in
    k = x3._hero(tuple(start), _facing(d))
    hero.line_width(k, 0.0028)
    d1._tilt_cap(k, 20.0)
    arm = k["arm"]
    P = x3.Pose(k)
    S = KAI_SCALE
    slide0 = run_in / S                                              # armature units along -Y
    slide1 = slide0 + (S03_SLIDE[0] - S03_SLIDE[1]) / S
    fwd = Vector((0, -1, 0))

    def arms_reach(P, t):                                           # both arms down at the ground ahead
        P.aim("upper_arm.R", (-0.14, -0.75, -0.65 + 0.2 * t))
        P.aim("forearm.R", (0.02, -0.7, -0.7 + 0.25 * t))
        P.aim("upper_arm.L", (0.14, -0.75, -0.65 + 0.2 * t))
        P.aim("forearm.L", (-0.02, -0.7, -0.7 + 0.25 * t))
        P.aim("hand.R", (0.05, -0.6, -0.8))
        P.aim("hand.L", (-0.05, -0.6, -0.8))

    def cup_up(P, t):                                               # the cup rising to his chest
        for sx, sg in (("L", 1), ("R", -1)):
            P.aim(f"upper_arm.{sx}", (sg * 0.12, -0.45 + 0.1 * t, -0.9 + 0.1 * t))
            P.aim(f"forearm.{sx}", (-sg * 0.5, -0.85, -0.25 + 0.5 * t))
            P.aim(f"hand.{sx}", (-sg * 0.5, -0.85, -0.15 + 0.1 * t))

    for f in range(1, n + 1, 2):
        P.reset()
        if f < B["kneel"]:                                          # the last stride, flying in
            u = (f - 1) / (B["kneel"] - 1)
            y = fwd * slide0 * u
            P.hips(Vector((0, y.y - 0.05, -0.05 - 0.04 * u)))
            P.leg("L", y + fwd * 0.28 + Vector((0.075, 0, P.ankle_h)))
            P.leg("R", y - fwd * 0.22 + Vector((-0.075, 0, P.ankle_h + 0.18)))
            P.rot("spine", (30, 0, 0))
            P.rot("neck", (-20, 0, 0))
            P.rot("head 1", (-18, 0, 0))
            arms_reach(P, 0.6)
        else:
            if f < B["slide"]:                                      # the drop onto the knees
                u = (f - B["kneel"]) / (B["slide"] - B["kneel"])
                y = slide0 + (slide1 - slide0) * 0.25 * u
                drop = 0.05 + 0.33 * u * u
            else:                                                   # the slide, slowing, then still
                u = min(1.0, (f - B["slide"]) / (B["scoop"] + 2 - B["slide"]))
                e = 1 - (1 - u) ** 2.2
                y = slide0 + (slide1 - slide0) * (0.25 + 0.75 * e)
                drop = 0.38
            hip_g = fwd * y
            P.hips(Vector((hip_g.x, hip_g.y, -drop)))
            _kneel_legs(P, hip_g, drop)
            if f < B["scoop"]:                                      # leaning down to it, arms reaching
                lean = 28 + 22 * min(1.0, (f - B["kneel"]) / max(1, B["scoop"] - B["kneel"]))
                P.rot("spine", (lean, 0, 0))
                P.rot("chest", (10, 0, 0))
                P.rot("neck", (-18, 0, 0))
                P.rot("head 1", (6, 0, 0))                          # eyes down on the shrimp
                arms_reach(P, 0.0)
            elif f < B["lift"]:                                     # the scoop
                u = (f - B["scoop"]) / (B["lift"] - B["scoop"])
                P.rot("spine", (50 - 22 * u, 0, 0))
                P.rot("chest", (10, 0, 0))
                P.rot("head 1", (6, 0, 0))
                cup_up(P, 0.4 * u)
            else:                                                   # up to his chest, hunched over it: protect it
                u = min(1.0, (f - B["lift"]) / max(1, B["hold"] - B["lift"]))
                br = 0.6 * math.sin(2 * math.pi * f / 30.0)
                P.rot("spine", (28 - 10 * u + br, 0, 0))
                P.rot("chest", (12 + 8 * u, 0, 0))
                P.rot("neck", (14 * u, 0, 0))
                P.rot("head 1", (14 * u, 0, 0))                     # head down over the cup
                cup_up(P, 0.4 + 0.6 * u)
        P.key(f)
    _open_hand(arm, "R", 1)
    _open_hand(arm, "L", 1)
    _cup_hands(arm, B["scoop"] - 2, 0.5)
    _cup_hands(arm, B["scoop"] + 2, 1.0)
    anim.on_twos([arm], step=2)
    # the shrimp: drinking, then scooped (it rides in his cupped hands from the scoop on, a startled squash)
    r = sh["root"]
    pal = arm.pose.bones
    sc = bpy.context.scene
    for f in range(B["scoop"], n + 1):
        sc.frame_set(f)
        mid = (arm.matrix_world @ pal["hand.L"].tail + arm.matrix_world @ pal["hand.R"].tail) / 2
        anim.key(r, "location", f, tuple(mid + Vector((0, 0, 0.05))), "CONSTANT")
    anim.key(r, "location", B["scoop"] - 1, tuple(r.location), "CONSTANT")
    sc.frame_set(1)
    anim.squash(sh["body"], B["scoop"], 0.18)                       # startled
    anim.squash(sh["body"], B["scoop"] + 4, -0.08)
    anim.squash(sh["body"], B["scoop"] + 8, 0.0)
    _splash(tuple(SHRIMP + Vector((0, 0, 0.3)) - d * 0.3), B["scoop"])
    anim.dust(tuple(k0 + Vector((0, 0, 0.3))), B["slide"], n=10, spread=2.4, seed=8, color="#b9a77f")
    # the bird: still plunging, off the top of the frame; its shadow sweeps over him from behind at the end
    bird = _bird_dive(n, 1, n + 30, perch)
    _dive_line(bird, n, perch, (0.88, 1.0))                          # S02 (helper 1) takes it 0.74 -> 0.88
    _bird_shadow_look(bird)
    _shadow_under(bird, n, perch)
    # his face: determined into the slide, then wide-eyed relief over the shrimp
    acting.expression(k, "angry", 1, value=0.7)
    acting.face_keys(k, 1, lip_a=0.5)
    acting.expression(k, "surprised", B["lift"], value=0.8)
    acting.look_at(k, tuple(SHRIMP + Vector((0, 0, 0.5))), 1, B["scoop"], darts=False)
    acting.look_at(k, tuple(k1 + Vector((0, 0, 4.2)) - d * 1.5), B["lift"], n, darts=True, seed=4)
    acting.blink(k, B["hold"], n, every=(30, 44), seed=9)
    c = S03_CAM                                                      # low from the west over the water, a push on 1s
    aim0 = SHRIMP.lerp(k0, 0.45) + Vector((0, 0, c["lift"]))
    aim1 = SHRIMP.lerp(k1, 0.6) + Vector((0, 0, c["lift"] + 0.6))
    cam = None
    for f in range(1, n + 1):
        u = (f - 1) / max(1, n - 1)
        e = u * u * (3 - 2 * u)
        aim = aim0.lerp(aim1, e)
        if cam is None:
            cam = diorama.camera("cam_s03", tuple(aim), dist=c["dist"], tilt=c["tilt"], yaw=c["yaw"], lens=c["lens"],
                                 blur=BLUR)
        b3._keycam(cam, f, aim, c["tilt"], c["dist"] - 4.0 * e, c["lens"], c["yaw"])
    bpy.context.scene.camera = cam
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {arm, *arm.children_recursive, bird["root"], *bird["root"].children_recursive, sh["root"],
            *sh["root"].children_recursive}
    _clear_view(cam, [1, n // 2, n], SHRIMP, keep)
    _anchors("S03", n, cam, k, sh)
    return dict(frames=n, step=2, ones=(1, n), subject=b3._subject(k, sh))


SHOTS = {"S01": s01, "S03": s03}
