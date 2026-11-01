"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md): helper 5's shots, Kai and the shrimp in his hands,
and the fluffed bird.

    S07 "So I turned it around."  Close on his cupped hands under his face: the shrimp faces him; his fingers pinch it
        and turn it, slowly, like a bomb tech (sweat, breath held), to face outward; it lets him, eyes darting,
        confused. Slow push-in on 1s; characters on 2s.
    S11 "Alive. Just very, very fluffed."  The bird hangs upside down in the thorn tree, wriggles, drops out, lands,
        shakes itself hard and POOFS into a round puffball (feathers sticking out), glares at the lens, then turns and
        stomps off, offended (a stiff little march). ~2 s of the march after the line for the laugh.
    S12 "Then the shrimp looked at me."  In his palm it turns round to face him (little steps) and raises the claw at
        his face: the frame-0 threat again (cocked, pincer open). Kai's pin-prick terror eyes. A held beat.
    S13 "And tapped my nose."  The claw reaches in and taps his nose, once (tiny), and sits back; Kai's stunned dot
        eyes (2D pass, post_helper5.py), held.

Staging: Kai stands where XprL's S17 puts him (xprl.KAI_AT, facing the path from the south, xprl.KAI_YAW), the shrimp
in his cupped hands (xprl._cup) at SHRIMP_S of its Episode 1 size. The bird is the tuftwing at the thorn tree
(diorama.MAP["thorn"]), at Episode 1 v3's BIRD_SCALE.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S07 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper5 as v2h5                 # _center, _puff
from channels.monsters.diorama_ep02 import xprl as X                  # the shared staging (KAI_AT, _world, _kai, _cup)
from channels.monsters.ep01v2 import bgqrs as s3d                     # kai_point, claw_tip, raise_claw, lock_on, cock
from channels.monsters.ep01v2 import xprl as x3                       # Pose
from channels.monsters.mk import acting, anim, diorama, puffshrimp, tuftwing

BLUR = 6.0
SHRIMP_S = 0.55                                                       # the shrimp's size in his hands
FWD = Vector((math.sin(math.radians(X.KAI_YAW)), -math.cos(math.radians(X.KAI_YAW)), 0.0))   # where Kai faces
LEFT = Vector((-FWD.y, FWD.x, 0.0))                                   # Kai's left (screen right from the front)
LAST = {}


def _frames(shot, fallback):
    return X._frames(shot, fallback)


def _cam(name, target, f0, f1, tilt, dist0, dist1, lens, yaw, shift=(0.0, 0.0), follow=None):
    """A diorama camera on `target` pushing in from dist0 to dist1 between f0 and f1 (eased, keyed on 1s), the
    tilt-shift and the haze re-solved every frame."""
    sc = bpy.context.scene
    cam = diorama.camera(name, target, dist=dist0, tilt=tilt, yaw=yaw, lens=lens, blur=BLUR, frame=f0)
    cam.data.shift_x, cam.data.shift_y = shift
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
        ms.start, ms.depth = d * 2.5, d * 2.0
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return cam


def _yaw_toward(v):
    """Camera yaw that looks along v (yaw 0 looks north, +Y)."""
    return math.degrees(math.atan2(v.x, v.y))


# ---------------------------------------------------------------------------------------------------- Kai + shrimp
def _kai_cupping(n, raise_hands=0.0, lean=4.0):
    """Kai at KAI_AT, both hands cupped in front of his chest (raised by `raise_hands` degrees: closer to his face),
    a slow breath on 2s. Returns (rig, Pose)."""
    k = X._kai()
    P = x3.Pose(k)
    for f in range(1, n + 1, 2):
        P.reset()
        X._cup(P)
        for sx, s in (("L", 1), ("R", -1)):
            P.rot(f"upper_arm.{sx}", (-raise_hands, 0, 0))
        P.rot("chest", (lean + 1.5 * math.sin(f / 16.0), 0, 0))
        P.rot("neck", (10, 0, 0))
        P.rot("head 1", (14, 0, 0))                                     # looking down into his hands
        P.key(f)
    bpy.context.scene.frame_set(1)
    return k, P


def _palm(k):
    """World point in the bowl of his cupped hands (between the two hand bones, a little above)."""
    arm = k["arm"]
    bpy.context.view_layer.update()
    pts = []
    for sx in ("L", "R"):
        pb = arm.pose.bones[f"hand.{sx}"]
        pts.append(arm.matrix_world @ ((pb.head + pb.tail) / 2))
    return (pts[0] + pts[1]) / 2 + Vector((0, 0, 0.08))


def _shrimp_in_hands(k, yaw):
    """The puff-shrimp (SHRIMP_S) sitting in his cupped hands, turned to `yaw` (degrees, root rotation z)."""
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    sh["root"].scale = (SHRIMP_S,) * 3
    sh["root"].location = _palm(k)
    sh["root"].rotation_euler = (0, 0, math.radians(yaw))
    bpy.context.view_layer.update()
    return sh


def _breathe(sh, n, every=24, amount=0.035):
    for f in range(1, n + 1, every):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + every // 2, -amount)


def _eye_dart(sh, f, yaw_deg, pitch_deg=0.0):
    """Both eyes glance to one side (CONSTANT keys)."""
    for piv in sh["eyes"]:
        anim.key(piv, "rotation_euler", f, (math.radians(pitch_deg), 0.0, math.radians(yaw_deg)), "CONSTANT")


def _sweat_bob(k, f0, f1):
    """A held breath: tiny head jitters on 2s (the bomb-tech concentration)."""
    pass


# ------------------------------------------------------------------------------------------------------------ S07
def s07():
    n = _frames("S07", 50)
    X._world(n)
    k, P = _kai_cupping(n, raise_hands=8.0)
    yaw_in, yaw_out = X.KAI_YAW + 180.0, X.KAI_YAW                    # facing him -> facing outward
    sh = _shrimp_in_hands(k, yaw_in)
    base = sh["root"].location.copy()
    T0, T1 = 7, 31                                                     # the careful turn, on "turned it around"
    for f in range(1, n + 1, 2):
        u = acting.ease(max(0.0, min(1.0, (f - T0) / (T1 - T0))), "inout")
        wob = math.sin(f * 0.9) * 3.0 * (1 if T0 < f < T1 else 0)      # a nervous wobble mid-turn
        lift = 0.18 * math.sin(math.pi * u) * SHRIMP_S                 # lifted a hair between his fingers
        anim.key(sh["root"], "rotation_euler", f, (0, 0, math.radians(yaw_in + (yaw_out - yaw_in) * u + wob)),
                 "CONSTANT")
        anim.key(sh["root"], "location", f, tuple(base + Vector((0, 0, lift))), "CONSTANT")
    # the shrimp lets him: looks at him, then darts left, right, up (confused), antennae droop
    for f, yv, pv in ((1, 0, 6), (11, 22, 0), (17, -22, 0), (23, 0, 18), (29, 14, -6), (37, -10, 4)):
        _eye_dart(sh, f, yv, pv)
    for f, a in ((1, 0.0), (13, -0.35), (n, -0.35)):
        for i, ant in enumerate(sh["antennae"]):
            anim.key(ant, "rotation_euler", f, (a, (-1) ** i * 0.15 * (a != 0), 0), "CONSTANT")
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.0, 0.0, 0.0), "CONSTANT")   # claw resting low
    anim.key(sh["hinge"], "rotation_euler", 1, (0.2, 0.0, 0.0), "CONSTANT")
    _breathe(sh, n)
    anim.blink(sh, 27)
    # Kai: wide-eyed concentration, a held breath; blinks; looking into his hands
    acting.expression(k, "fear", 1, value=0.6)
    acting.face_keys(k, 1, mouth_wide=0.0)
    acting.blink(k, 1, n, at=(36,))
    acting.look_at(k, sh["root"].location, 1, n, darts=False, strength=0.6)
    v2_twos = getattr(X.v2, "_twos")
    v2_twos([k["arm"], sh["root"], sh["body"]] + sh["eyes"] + sh["antennae"])
    # camera: in front of him, a little to his left, looking down past the hands at his face
    eyes = s3d.kai_point(k, "eyes")
    tgt = base.lerp(eyes, 0.42)
    yaw = _yaw_toward(-(FWD * 0.85 + LEFT * 0.35))                   # from in front, a little to his left
    _cam("cam_s07", tgt, 1, n, 14.0, 5.2, 4.6, 40.0, yaw)
    LAST.update(k=k, sh=sh)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------------------ S11
BIRD_SCALE = 1.3                                                      # Episode 1's tuftwing size (ep01v2/helper5)
BUSH = Vector((diorama.MAP["thorn"][0], diorama.MAP["thorn"][1], 0.0))


def _tufts(rig, n=9, seed=4):
    """Feather tufts sticking out of the fluffed ball (little butter/cream cones parented to the body), hidden until
    the poof. Returns the objects."""
    import random
    from channels.monsters.mk import look
    rnd = random.Random(seed)
    mats = [look.toon("tuft_butter", look.hexc(tuftwing.BUTTER)), look.toon("tuft_cream", look.hexc(tuftwing.CREAM))]
    out = []
    c = Vector(tuftwing.CENTER)
    rx, ry, rz = tuftwing.BALL
    for i in range(n):
        az = rnd.uniform(-2.8, 2.8) if i else 0.6
        el = rnd.uniform(-0.25, 1.1)
        d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        p = c + Vector((d.x * rx, d.y * ry, d.z * rz)) * 0.96
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.09, radius2=0.0, depth=0.32, location=(0, 0, 0))
        o = bpy.context.object
        o.name = f"tuft_{i}"
        o.data.materials.append(mats[i % 2])
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
        o.location = p + d * 0.1
        look.outline(o, 0.008)
        bpy.context.view_layer.update()
        o.parent = rig["body"]
        o.matrix_parent_inverse = rig["body"].matrix_world.inverted()
        out.append(o)
    return out


def s11():
    n = _frames("S11", 113)
    X._world(n)
    rig = tuftwing.build((0, 0, 0), name="tuft", shadow_span=10.0)
    root, lift, body, head = rig["root"], rig["lift"], rig["body"], rig["head"]
    root.scale = (BIRD_SCALE,) * 3
    cam_dir = Vector((-0.55, -1.0, 0.0)).normalized()                  # the camera stands south-west of the bush
    stuck = BUSH + cam_dir * 1.1 + Vector((0, 0, 0.0))
    yaw_cam = math.atan2(cam_dir.x, -cam_dir.y)                        # root yaw that faces the lens (-Y local)
    root.location = stuck
    root.rotation_mode = "XYZ"
    STUCK_Z = 4.6 / BIRD_SCALE
    F_DROP, F_LAND, F_SHAKE, F_POOF, F_GLARE, F_TURN = 13, 21, 27, 41, 49, 67
    # 1. upside down in the thorns, wriggling (on 2s)
    for f in range(1, F_DROP + 1, 2):
        anim.key(root, "rotation_euler", f, (math.pi, 0.25 * math.sin(f * 1.3), yaw_cam), "CONSTANT")
        anim.key(lift, "location", f, (0, 0, -STUCK_Z - 1.2), "CONSTANT")   # upside down: lift points down
    # 2. drops out, flipping upright, lands with a squash
    for i, f in enumerate(range(F_DROP + 1, F_LAND + 1)):
        u = (f - F_DROP) / (F_LAND - F_DROP)
        flip = math.pi * (1 - acting.ease(u, "out"))
        anim.key(root, "rotation_euler", f, (flip, 0, yaw_cam), "LINEAR")
        z = STUCK_Z * (1 - u * u)
        anim.key(lift, "location", f, (0, 0, -z - 1.2 * (1 - u) if flip > math.pi / 2 else z), "LINEAR")
    anim.key(lift, "location", F_LAND, (0, 0, 0), "CONSTANT")
    anim.key(root, "rotation_euler", F_LAND, (0, 0, yaw_cam), "CONSTANT")
    for t, a in ((F_LAND, -0.35), (F_LAND + 2, 0.12), (F_LAND + 4, -0.06), (F_LAND + 6, 0.0)):
        anim.squash(body, t, a, "LINEAR")
    # dazed: eyes half shut, head wobble
    for f in (F_LAND, F_LAND + 2):
        for e in rig["eyes"]:
            anim.key(e, "scale", f, (1.05, 1, 0.45), "CONSTANT")
    for f, a in ((F_LAND, 0.25), (F_LAND + 2, -0.2), (F_LAND + 4, 0.15), (F_SHAKE - 1, 0.0)):
        anim.key(head, "rotation_euler", f, (0, a, 0), "CONSTANT")
    # 3. the shake: a fast wet-dog shake (alternating every frame), then POOF
    for f in range(F_SHAKE, F_POOF):
        s = 1 if (f - F_SHAKE) % 2 == 0 else -1
        anim.key(root, "rotation_euler", f, (0, 0.18 * s, yaw_cam + 0.45 * s), "CONSTANT")
        anim.key(body, "scale", f, (1.0 + 0.05 * s, 1.0, 1.0 - 0.04 * s), "CONSTANT")
        for e in rig["eyes"]:
            anim.key(e, "scale", f, (1.1, 1, 0.12), "CONSTANT")             # squeezed shut
    anim.key(root, "rotation_euler", F_POOF, (0, 0, yaw_cam), "CONSTANT")
    tufts = _tufts(rig)
    for o in tufts:
        anim.key(o, "scale", F_POOF - 1, 0.001, "CONSTANT")
        anim.key(o, "scale", F_POOF, 1.3, "CONSTANT")
        anim.key(o, "scale", F_POOF + 2, 1.0, "CONSTANT")
    for t, sc in ((F_POOF, 1.62), (F_POOF + 2, 1.38), (F_POOF + 4, 1.48), (F_POOF + 6, 1.45)):
        anim.key(body, "scale", t, (sc, sc, sc * 0.98), "CONSTANT")
    v2h5._puff(stuck + Vector((0, 0, 1.0)), F_POOF, n=6, size=1.1, rise=0.8, life=10, seed=11, name="poof")
    for e in rig["eyes"]:
        anim.key(e, "scale", F_POOF, (1.25, 1, 1.25), "CONSTANT")          # eyes popped wide in the poof
        anim.key(e, "scale", F_POOF + 4, (1, 1, 1), "CONSTANT")
    anim.key(rig["crest"], "rotation_euler", F_POOF, (-0.6, 0, 0), "CONSTANT")
    # 4. the glare at the lens: narrowed, slanted, crest up; a huff (squash) and hold through the line
    for sx, e in zip((-1, 1), rig["eyes"]):
        anim.key(e, "scale", F_GLARE, (1.05, 1, 0.55), "CONSTANT")
        anim.key(e, "rotation_euler", F_GLARE, (0, sx * 0.4, 0), "CONSTANT")
    anim.key(head, "rotation_euler", F_GLARE, (-0.12, 0, 0), "CONSTANT")
    for t, a in ((F_GLARE + 6, -0.06), (F_GLARE + 8, 0.08), (F_GLARE + 10, 0.0)):
        anim.key(body, "scale", t, (1.45 * (1 - a / 2), 1.45 * (1 - a / 2), 1.42 * (1 + a)), "CONSTANT")
    # 5. turns its back (a sharp "hmph") and stomps off south-west, stiff little hops, tail up, head high
    away = Vector((cam_dir.y, -cam_dir.x, 0.0)).normalized() * 0.85 - cam_dir * 0.3
    yaw_away = math.atan2(away.x, -away.y)
    for t, y in ((F_TURN, yaw_cam), (F_TURN + 2, yaw_away + 0.3), (F_TURN + 4, yaw_away)):
        anim.key(root, "rotation_euler", t, (0, 0, y), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", F_TURN + 2, (0.5, 0, 0), "CONSTANT")
    anim.key(head, "rotation_euler", F_TURN + 2, (-0.25, 0, 0), "CONSTANT")
    pos = stuck.copy()
    f = F_TURN + 6
    while f + 6 <= n:
        a, b = pos.copy(), pos + away.normalized() * 0.75
        for t in range(0, 7):
            u = t / 6
            p = a.lerp(b, u)
            anim.key(root, "location", f + t, tuple(p), "LINEAR")
            anim.key(lift, "location", f + t, (0, 0, 0.35 * math.sin(math.pi * u) / BIRD_SCALE), "LINEAR")
        anim.squash(body, f, 0.0)
        anim.key(body, "scale", f + 6, (1.5, 1.5, 1.32), "CONSTANT")       # a stomp
        anim.key(body, "scale", f + 8, (1.45, 1.45, 1.42), "CONSTANT")
        pos = b
        f += 8
    anim.blink(rig, 60)
    X.v2._twos(tuftwing._animated(rig))
    # camera: low, south-west of the bush, on the bird's landing spot; follows the stomp a little
    tgt = stuck + Vector((0, 0, 1.4))
    end = pos + Vector((0, 0, 1.4))
    yaw = _yaw_toward(-cam_dir)
    _cam("cam_s11", tgt, 1, n, 6.0, 12.0, 10.5, 50.0, yaw, follow=lambda u: tgt.lerp(tgt.lerp(end, 0.5), u))
    LAST.update(bird=rig)
    return dict(frames=n, step=2, ones=(1, n), subject=[root])


# ------------------------------------------------------------------------------------------------------------ S12
def _cock_at_face(sh, k):
    """Claw raised beside his face, pincer open, aimed at his nose (Episode 1's frame-0 threat, at this scale)."""
    nose = s3d.kai_point(k, "nose")
    side = LEFT * 0.35 * SHRIMP_S / 0.55
    return s3d.raise_claw(sh, nose + side + Vector((0, 0, 0.55)), nose)


def s12():
    n = _frames("S12", 74)
    X._world(n)
    k, P = _kai_cupping(n, raise_hands=18.0)
    yaw_out = X.KAI_YAW
    sh = _shrimp_in_hands(k, yaw_out)
    base = sh["root"].location.copy()
    # it turns round in his palm: three little stepping hops (on 2s), 60 degrees each
    hops = (8, 15, 22)
    cur = yaw_out
    anim.key(sh["root"], "rotation_euler", 1, (0, 0, math.radians(cur)), "CONSTANT")
    anim.key(sh["root"], "location", 1, tuple(base), "CONSTANT")
    for h in hops:
        nxt = cur + 60.0
        anim.key(sh["root"], "rotation_euler", h, (0, 0, math.radians(cur + 20)), "CONSTANT")
        anim.key(sh["root"], "location", h, tuple(base + Vector((0, 0, 0.12))), "CONSTANT")
        anim.key(sh["root"], "rotation_euler", h + 2, (0, 0, math.radians(nxt + 6)), "CONSTANT")
        anim.key(sh["root"], "location", h + 2, tuple(base), "CONSTANT")
        anim.key(sh["root"], "rotation_euler", h + 4, (0, 0, math.radians(nxt)), "CONSTANT")
        anim.squash(sh["body"], h + 2, -0.12, "CONSTANT")
        anim.squash(sh["body"], h + 4, 0.0, "CONSTANT")
        cur = nxt
    # it looks up at him ... then the claw goes up: the threat (anticipation dip, overshoot, settle)
    LOOK, RAISE = 28, 36
    s3d.lock_on(sh, s3d.kai_point(k, "eyes"), LOOK)
    rest = (0.0, 0.0, 0.0)
    anim.key(sh["shoulder"], "rotation_euler", 1, rest, "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.2, 0.0, 0.0), "CONSTANT")
    cock = _cock_at_face(sh, k)
    anim.key(sh["shoulder"], "rotation_euler", RAISE - 2, (-0.15, 0.0, 0.0), "CONSTANT")   # the dip
    over = tuple(v * 1.12 for v in cock)
    anim.key(sh["shoulder"], "rotation_euler", RAISE, over, "CONSTANT")
    anim.key(sh["shoulder"], "rotation_euler", RAISE + 2, cock, "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", RAISE, (1.5, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", RAISE + 2, (1.4, 0.0, 0.0), "CONSTANT")
    for f in range(RAISE + 4, n + 1, 4):                               # a held tremble of the raised claw
        j = 0.02 * (1 if (f // 4) % 2 else -1)
        anim.key(sh["shoulder"], "rotation_euler", f, (cock[0] + j, cock[1], cock[2]), "CONSTANT")
    _breathe(sh, n)
    # Kai: relief (a small smile) while it turns, surprise when it looks up, the pin-prick terror at the claw
    acting.expression(k, "joy", 1, value=0.35)
    acting.expression(k, "surprised", LOOK + 1, value=0.8)
    acting.expression(k, "terror", RAISE + 1)
    acting.blink(k, 1, LOOK - 2, at=(12,))
    acting.look_at(k, sh["root"].location + Vector((0, 0, 0.6)), 1, n, darts=False, strength=0.6)
    X.v2._twos([k["arm"], sh["root"], sh["body"], sh["shoulder"], sh["hinge"]] + sh["eyes"] + sh["antennae"])
    # camera: the frame-0 threat: three-quarter from his left-front, low, both faces in frame; slow push-in
    eyes = s3d.kai_point(k, "eyes")
    tgt = base.lerp(eyes, 0.55)
    yaw = _yaw_toward(-(FWD * 0.7 + LEFT * 0.7))
    _cam("cam_s12", tgt, 1, n, 4.0, 5.6, 4.8, 50.0, yaw)
    LAST.update(k=k, sh=sh)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------------------ S13
def s13():
    n = _frames("S13", 59)
    X._world(n)
    k, P = _kai_cupping(n, raise_hands=18.0)
    sh = _shrimp_in_hands(k, X.KAI_YAW + 180.0)
    base = sh["root"].location.copy()
    eyes, nose = s3d.kai_point(k, "eyes"), s3d.kai_point(k, "nose")
    s3d.lock_on(sh, eyes, 1)
    cock = _cock_at_face(sh, k)
    # the tap: the claw reaches to his nose; the shrimp leans in to reach it
    TAP = 18
    reach = s3d.raise_claw(sh, nose, nose + FWD)
    sh["shoulder"].rotation_euler = reach
    bpy.context.view_layer.update()
    gap = nose - s3d.claw_tip(sh)
    lean = base + gap * 0.98
    sh["shoulder"].rotation_euler = cock
    for f, rot, loc in ((1, cock, base), (TAP - 6, cock, base), (TAP - 2, reach, base.lerp(lean, 0.7)),
                        (TAP, reach, lean), (TAP + 2, reach, lean), (TAP + 4, reach, base.lerp(lean, 0.6)),
                        (TAP + 8, cock, base)):
        anim.key(sh["shoulder"], "rotation_euler", f, rot, "CONSTANT")
        anim.key(sh["root"], "location", f, tuple(loc), "CONSTANT")
    anim.key(sh["root"], "rotation_euler", 1, (0, 0, math.radians(X.KAI_YAW + 180.0)), "CONSTANT")
    for f, a in ((1, 1.4), (TAP - 2, 0.3), (TAP + 6, 0.6), (TAP + 14, 0.2)):   # pincer closes to a gentle "tap"
        anim.key(sh["hinge"], "rotation_euler", f, (a, 0.0, 0.0), "CONSTANT")
    # after the tap: it lowers the claw, sits back, pleased (lids up, a little bounce, a blink)
    LOW = TAP + 14
    anim.key(sh["shoulder"], "rotation_euler", LOW, (0.0, 0.0, 0.0), "CONSTANT")
    for lp, hi in zip(sh["lids"], sh["hi"]):
        anim.key(lp, "scale", LOW, 0.001, "CONSTANT")
        anim.key(hi, "scale", LOW, 1.0, "CONSTANT")
    anim.squash(sh["body"], LOW, -0.1, "CONSTANT")
    anim.squash(sh["body"], LOW + 2, 0.05, "CONSTANT")
    anim.squash(sh["body"], LOW + 4, 0.0, "CONSTANT")
    anim.blink(sh, LOW + 10)
    # Kai: terror, then the tap: eyes squeeze, then stunned and held (the 2D dot eyes go on from TAP + 1)
    acting.expression(k, "terror", 1)
    acting.face_keys(k, TAP, eye_close=0.8)
    acting.face_keys(k, TAP + 2, eye_close=0.0)
    acting.expression(k, "deadpan", TAP + 1, value=0.3)
    acting.look_at(k, sh["root"].location + Vector((0, 0, 0.6)), 1, TAP, darts=False, strength=0.6)
    X.v2._twos([k["arm"], sh["root"], sh["body"], sh["shoulder"], sh["hinge"]] + sh["eyes"] + sh["antennae"])
    # camera: closer, more in profile so the tap reads; a slow push-in
    tgt = nose.lerp(base, 0.4)
    yaw = _yaw_toward(-(FWD * 0.6 + LEFT * 0.8))
    _cam("cam_s13", tgt, 1, n, 3.0, 4.0, 3.5, 50.0, yaw)
    _anchors("S13", n, k, sh)
    LAST.update(k=k, sh=sh)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


def _anchors(shot, n, k, sh):
    """Screen positions (720x1280) of his eyes and nose and the claw tip per frame, for the 2D pass
    (build/monsters/diorama_ep02/<SHOT>_anchors.json)."""
    import json
    import os
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        pts = {kk: s3d.kai_point(k, kk) for kk in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        pts["tip"] = s3d.claw_tip(sh)
        out[f] = {kk: (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
                  for kk, v in ((kk, world_to_camera_view(sc, sc.camera, p)) for kk, p in pts.items())}
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    folder = os.path.join(root, "build", "monsters", "diorama_ep02")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


SHOTS = {"S07": s07, "S11": s11, "S12": s12, "S13": s13}
