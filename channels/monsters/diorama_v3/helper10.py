"""Episode 1 v3, 2.5D diorama (channels/monsters/DIORAMA_EP01_V3.md): helper 10's S15a and S15.

    S15a "Then it looked right at me." (36 frames + 12): close and low over the shrimp's claw shoulder, Kai kneeling
        at the near bank behind it. The shrimp lifts its head (anticipation, overshoot), its eyes narrow on him, then
        the dripping claw rises out of the pond and swings round to AIM at his face, big in the foreground; Kai
        flinches back, his hand drawn in, eyes on the claw. Slow push-in on 1s; the characters on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S15a OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math
import os
import sys

try:
    import bpy
    from mathutils import Vector

    from channels.monsters.diorama import helper10 as dv2       # v2 diorama S15: cameras, LYING_RELAXED, burn
    from channels.monsters.ep01v2 import helper10 as s15         # Kai's kneel / blown poses and pose helpers
    from channels.monsters.mk import acting, anim, diorama, erase, hero, look, meadow, puffshrimp
except ImportError:                                             # composite() runs outside Blender
    bpy = None

SHRIMP = (*diorama.MAP["shrimp"], 0.0) if bpy else None   # the north bank of the pond, facing -Y (Kai)
DIP = (1.8, 0.0, 0.3)                        # the claw in the water (S13-S14)
UP = (0.35, 0.75, 0.0)                       # the claw lifted out of it (v2 D1b)
CAM_DIST, CAM_TILT, CAM_YAW, CAM_LENS = float(os.environ.get("H10_DIST", 15)), float(os.environ.get("H10_TILT", 0)), \
    float(os.environ.get("H10_YAW", 124)), float(os.environ.get("H10_LENS", 50))
CUT = 18                                     # S15a: face close-up -> the aim


def _frames(shot, fallback):
    from channels.monsters.diorama_v3.shots import v3_frames           # (lazy: shots.py imports this module)
    try:
        return v3_frames(shot)
    except (OSError, KeyError):
        return fallback


# ---------------------------------------------------------------- the claw's aim

def _muzzle(rig):
    """Two empties on the claw (parented to the shoulder, made before any keys): the palm and the fingertips. The
    snap's jet leaves the fingertips along palm -> tip."""
    loc = Vector(SHRIMP)
    out = []
    for name, off in (("puff_palm", (-1.7, -0.4, 2.2)), ("puff_muzzle", (-1.62, -0.44, 3.4))):
        e = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(e)
        e.location = loc + Vector(off)
        bpy.context.view_layer.update()
        e.parent = rig["shoulder"]
        e.matrix_parent_inverse = rig["shoulder"].matrix_world.inverted()
        out.append(e)
    return out


def aim_euler(rig, emp, target, body_rot=(0, 0, 0), iters=16):
    """The shoulder rotation that points the claw (palm -> fingertips) at `target` (world), with the body pivot at
    body_rot. Call it before the shoulder and body have keys (a keyed action would re-apply over these trial values);
    restores both to rest."""
    sh, body = rig["shoulder"], rig["body"]
    body.rotation_euler = body_rot
    sh.rotation_euler = (0, 0, 0)
    for i in range(iters):
        bpy.context.view_layer.update()
        palm, tip = (e.matrix_world.translation for e in emp)
        want = Vector(target) - (palm if i < iters // 2 else tip)     # coarse from the palm, then exact from the tip
        delta = (tip - palm).rotation_difference(want).to_matrix()
        world = sh.matrix_world.to_3x3().normalized()
        par = (sh.parent.matrix_world @ sh.matrix_parent_inverse).to_3x3().normalized()
        sh.rotation_euler = (par.inverted() @ delta @ world).to_euler("XYZ", sh.rotation_euler)
    bpy.context.view_layer.update()
    palm, tip = (e.matrix_world.translation for e in emp)
    err = math.degrees((tip - palm).angle(Vector(target) - tip))
    e = tuple(sh.rotation_euler)
    sh.rotation_euler = (0, 0, 0)
    body.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    return e, err


def _lerp3(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ---------------------------------------------------------------- Kai kneeling at the near bank

def _kneeling_kai():
    """Kai on his knees at the pond's south edge (MAP["kai_kneel"]; his reach toward the shrimp fixes loc.y)."""
    k = hero.load((0, 0, 0), scale=s15.KAI_SCALE, outfit="world")
    reach = Vector((SHRIMP[0] + 0.45, SHRIMP[1] - 1.45, 2.05))
    loc = Vector((diorama.MAP["kai_kneel"][0], SHRIMP[1] - 6.4, 0))      # v3: 1.35 east of v2, clear of the sapling
    for _ in range(3):
        s15._apply_kneel(k, loc, 1.0, reach)
        loc.y += (reach - s15._world(k, "right_upper_arm")).length - 2.55
    return k, loc, reach


def face_point(k):
    """Between his eyes: 55% up the head bone, nudged forward (toward -Y... his facing) by a little."""
    bpy.context.view_layer.update()
    pb = k["bone"]("head")
    arm = k["arm"]
    h, t = arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail
    return h + (t - h) * 0.55


# ---------------------------------------------------------------- S15a

def s15a():
    n = _frames("S15a", 48)
    sc = bpy.context.scene
    diorama.setup()
    diorama.island(seed=31, dressing=1 if os.environ.get("H10_FAST") else 2, grove=True)

    rig = puffshrimp.build(SHRIMP)
    root, body, sh, hg = rig["root"], rig["body"], rig["shoulder"], rig["hinge"]
    emp = _muzzle(rig)

    # Kai: hand half out toward it (the end of S14), then flinches back on "right at me"
    k, loc, reach = _kneeling_kai()
    FLINCH = 22
    BACK = Vector((0, -0.35, 0))                             # the flinch rocks him back a little

    def snatch(amt=1.0):
        """His right hand snatched back to his chest (Kai faces +Y, his right is +X)."""
        s15._aim(k, "right_upper_arm", Vector((0.3, -0.25 * amt, -1)))
        s15._aim(k, "right_lower_arm", Vector((-0.7 * amt, 0.55, 0.65 * amt)))
        s15._aim(k, "right_hand", Vector((-0.8, 0.35, 0.45)))

    def flinched(s=0.0):
        s15._apply_kneel(k, loc + BACK, s, HAND_IN)
        snatch()
        s15._aim(k, "neck", Vector((0, -0.05, 1)))           # head up, out from under the cap brim: his face shows
        s15._aim(k, "head", Vector((0, -0.12, 1)))
    HAND_IN = Vector((loc.x + 0.4, loc.y + 3.0, 3.4))          # the reaching hand snatched back to his chest
    flinched()
    face = face_point(k)                                     # where the claw aims: his face once he has flinched
    LIFT = (-0.2, 0, 0)                                      # head up (body pivot pitched back)
    aim, err = aim_euler(rig, emp, face, LIFT)
    print("S15A AIM", tuple(round(v, 3) for v in aim), "ERR_DEG", round(err, 2), "FACE", tuple(round(v, 2) for v in face))

    for f in (1, FLINCH - 2):
        s15._apply_kneel(k, loc, 0.55, reach + 0.45 * Vector((0.3, -1.6, 1.3)))
        s15._key_pose(k, f)
    s15._apply_kneel(k, loc + BACK * 1.4, 0.0, HAND_IN + Vector((0, -0.3, 0.3)))   # overshoot back
    snatch(1.2)
    s15._aim(k, "neck", Vector((0, -0.15, 1)))
    s15._aim(k, "head", Vector((0, -0.25, 1)))
    s15._key_pose(k, FLINCH)
    flinched()
    s15._key_pose(k, FLINCH + 2)
    s15._flush_keys(k)
    acting.expression(k, "neutral", 1)
    acting.expression(k, "surprised", FLINCH)
    acting.expression(k, "fear", FLINCH + 10)
    acting.blink(k, 1, n, at=(6,))
    acting.look_at(k, Vector(SHRIMP) + Vector((0, 0, 1.3)), 1, FLINCH - 1, darts=False)
    sc.frame_set(FLINCH + 6)
    claw = s15._claw_pt(lowest=False)
    acting.look_at(k, claw, FLINCH, n, darts=False)

    # the shrimp: head lifts 4-10 (squash, lift, overshoot, settle), eyes narrow at 12, the claw rises 16-24 and
    # swings to the aim 26-32 (overshoot 30, settle 32), held, dripping, with a tiny tremble
    for o, v in ((root, (0, 0, 0)), (body, (0, 0, 0))):
        anim.key(o, "rotation_euler", 1, v, "CONSTANT")
    anim.key(sh, "rotation_euler", 1, DIP, "CONSTANT")
    anim.key(hg, "rotation_euler", 1, (0.1, 0, 0), "CONSTANT")
    anim.squash(body, 1, 0.0, "CONSTANT")
    anim.squash(body, 4, -0.08, "CONSTANT")                  # anticipation: a little crouch
    for f, p in ((6, -0.28), (8, -0.17), (10, -0.2)):         # head up past the mark, back, settle
        anim.key(body, "rotation_euler", f, (p, 0, 0), "CONSTANT")
    anim.squash(body, 6, 0.08, "CONSTANT")
    anim.squash(body, 10, 0.0, "CONSTANT")
    acting.glare(rig, face, 12)
    for e in rig["eyes"]:                                    # the eyes narrow (squashed shut a little, as v2 D1b)
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 12, (1.12, 1, 0.5), "CONSTANT")
        anim.key(e, "scale", 14, (1.1, 1, 0.58), "CONSTANT")
    for f, v in ((14, (2.0, 0.0, 0.35)),                     # anticipation: dips deeper before it pulls out
                 (16, _lerp3(DIP, UP, 0.3)), (18, _lerp3(DIP, UP, 0.65)), (20, UP), (22, UP),
                 (24, _lerp3(UP, aim, 0.4)), (26, _lerp3(UP, aim, 0.85)),
                 (28, _lerp3(UP, aim, 1.12)), (30, _lerp3(UP, aim, 1.05)), (32, aim)):
        anim.key(sh, "rotation_euler", f, v, "CONSTANT")
    anim.key(hg, "rotation_euler", 26, (0.45, 0, 0), "CONSTANT")   # the snapping finger cocked open
    for f in range(34, n + 1, 4):                            # held on the aim: a two-frame tremble
        anim.key(sh, "rotation_euler", f, tuple(a + 0.012 for a in aim), "CONSTANT")
        anim.key(sh, "rotation_euler", f + 2, aim, "CONSTANT")
    sc.frame_set(20)
    drip = s15._claw_pt()
    meadow.drips((drip.x, drip.y, drip.z - 0.05), 16, n, every=5, fall=max(0.3, drip.z - 0.02))

    # cameras (a cut at CUT, slow push-ins on 1s in both): A, low and close in front of the shrimp (from Kai's side,
    # off his shoulder), its head lifting and the eyes narrowing; B, low from the claw side (west), the claw big in
    # the foreground and pointing across the frame at Kai's face
    eyes = Vector(SHRIMP) + Vector((0, -0.9, 1.2))
    ca = dv2._camera("S15a_A", 1, eyes, 7.0, 6.0, yaw=24.0)
    ca.data.lens = 70.0
    for f in range(1, CUT):
        u = acting.ease((f - 1) / (CUT - 2), "inout")
        dv2._key(ca, f, eyes + Vector((0, 0, 0.1 * u)), 7.0 - 1.2 * u, 6.0 + 1.0 * u, yaw=24.0 - 4.0 * u)
    sc.frame_set(32)
    tip = emp[1].matrix_world.translation.copy()
    mid = tip.lerp(face, 0.45)
    cb = dv2._camera("S15a_B", CUT, mid, CAM_DIST, CAM_TILT, yaw=CAM_YAW)
    cb.data.lens = CAM_LENS
    for f in range(CUT, n + 1):
        u = acting.ease((f - CUT) / (n - CUT), "out")
        dv2._key(cb, f, mid, CAM_DIST * (1 - 0.15 * u), CAM_TILT + 1.5 * u, yaw=CAM_YAW + 4.0 * u)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[root])


# ---------------------------------------------------------------- S15: the snap, fired at Kai

COCK, SNAP, CUT2, LAND, CUT3 = 10, 30, 36, 48, 78
"""S15 beats (1-based; helper 7's mix has them): the claw cocks (10-29, the snapping finger opens wide, the claw
draws back, straining), the SNAP (30; the 2D pass has the flash 30-31 and impact frames 32-35), the cut to the blast
line (36), Kai thrown back 31-47 and landing (48), the aftermath (78)."""


def _key_cam(c, f, pos, target, blur=None):
    """Key a camera from a position and a target (dv2._key works in dist/tilt/yaw)."""
    v = Vector(pos) - Vector(target)
    dist = v.length
    tilt = math.degrees(math.asin(v.z / dist))
    yaw = math.degrees(math.atan2(-v.x, -v.y))
    dv2._key(c, f, Vector(target), dist, tilt, yaw=yaw)


def _hide_occluders(cam, f0, f1, keep, near=0.85, pairs=None):
    """Hide (hide_render, keyed) the set pieces that would sit between `cam` and its subject over f0..f1 (a blurred
    canopy or bush across the frame from a high diorama camera): any mesh smaller than 40 units and taller than 1,
    in frame and nearer than `near` x the focus distance, except `keep` (objects and their children: the characters,
    the grove, the stumps). The other cameras never see them, so they come back after f1. Returns their names."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    skip = set()
    for o in keep:
        skip |= {o.name} | {c.name for c in o.children_recursive}
    cands = [o for o in sc.objects if o.type == "MESH" and o.name not in skip
             and (o.parent is None or o.parent.name not in skip)]
    hide = []
    for f in (f0, (f0 + f1) // 2, f1):
        sc.frame_set(f)
        focus = cam.data.dof.focus_distance
        for o in cands:
            if o in hide:
                continue
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            size = max((max(p[i] for p in bb) - min(p[i] for p in bb)) for i in range(3))
            if size > 40 or max(p.z for p in bb) < 1.0:
                continue
            for c in bb + [sum(bb, Vector()) / 8]:
                v = world_to_camera_view(sc, cam, c)
                if 0 < v.z < near * focus and -0.1 < v.x < 1.1 and -0.1 < v.y < 1.1:
                    hide.append(o)
                    break
    for o in list(hide):                                       # a tree goes whole (pairs: canopy name -> trunk)
        t = (pairs or {}).get(o.name)
        if t is not None and t not in hide:
            hide.append(t)
    for o in hide:
        for c in [o] + list(o.children_recursive):
            for fr, v in ((1, False), (f0, True), (f1 + 1, False)):
                c.hide_render = v
                c.keyframe_insert("hide_render", frame=fr)
            c.hide_render = False
    return [o.name for o in hide]


def s15_snap():
    from channels.monsters.diorama import bgqrs as b2                  # HIPS (kai_down) and HEAD_DIR, S15b's lie
    n = _frames("S15", 118)
    sc = bpy.context.scene
    diorama.setup()
    isl = diorama.island(seed=31, dressing=1 if os.environ.get("H10_FAST") else 2, grove=True)

    rig = puffshrimp.build(SHRIMP)
    root, body, sh, hg = rig["root"], rig["body"], rig["shoulder"], rig["hinge"]
    emp = _muzzle(rig)
    k, loc, reach = _kneeling_kai()
    BACK = Vector((0, -0.35, 0))
    HAND_IN = Vector((loc.x + 0.4, loc.y + 3.0, 3.4))

    def flinched(lean=0.0):                                   # S15a's last pose (frozen, hand at his chest)
        s15._apply_kneel(k, loc + BACK * (1 + lean), 0.0, HAND_IN)
        s15._aim(k, "right_upper_arm", Vector((0.3, -0.25, -1)))
        s15._aim(k, "right_lower_arm", Vector((-0.7, 0.55, 0.65)))
        s15._aim(k, "right_hand", Vector((-0.8, 0.35, 0.45)))
        s15._aim(k, "neck", Vector((0, -0.05 - 0.1 * lean, 1)))
        s15._aim(k, "head", Vector((0, -0.12 - 0.15 * lean, 1)))
    flinched()
    face = face_point(k)
    s15._aim(k, "head", Vector((0, -0.12, 1)))
    LIFT = (-0.2, 0, 0)
    aim, _ = aim_euler(rig, emp, face, LIFT)                   # S15a's aim, held
    ear = face + Vector((-0.75, -0.2, 0.25))                   # the shot: past his LEFT ear (west), by an inch
    fire, err = aim_euler(rig, emp, ear, LIFT)
    cock = tuple(a + d for a, d in zip(aim, (-0.12, 0.0, 0.05)))   # drawn back a little: the wind-up

    # ---- the shrimp: held on the aim, cocks (finger wide open, claw back), SNAPS (18), recoils, glares
    anim.key(root, "rotation_euler", 1, (0, 0, 0), "CONSTANT")
    anim.key(body, "rotation_euler", 1, LIFT, "CONSTANT")
    acting.glare(rig, face, 1)
    for e in rig["eyes"]:
        anim.key(e, "scale", 1, (1.1, 1, 0.58), "CONSTANT")
        anim.key(e, "scale", SNAP, (1.15, 1, 0.3), "CONSTANT")         # squeezes its eyes on the snap
        anim.key(e, "scale", SNAP + 6, (1.1, 1, 0.58), "CONSTANT")
    anim.key(sh, "rotation_euler", 1, aim, "CONSTANT")
    anim.key(hg, "rotation_euler", 1, (0.45, 0, 0), "CONSTANT")
    for f, u in ((COCK, 0.35), (COCK + 2, 0.7), (COCK + 4, 1.0)):
        anim.key(sh, "rotation_euler", f, _lerp3(aim, cock, u), "CONSTANT")
        anim.key(hg, "rotation_euler", f, (0.45 + 0.4 * u, 0, 0), "CONSTANT")     # the finger cocks wide open
        anim.squash(body, f, -0.06 * u, "CONSTANT")
    for f in range(COCK + 6, SNAP, 2):                         # held, trembling with the strain
        anim.key(sh, "rotation_euler", f, tuple(c + (0.01 if (f // 2) % 2 else -0.01) for c in cock), "CONSTANT")
    anim.key(sh, "rotation_euler", SNAP, fire, "CONSTANT")
    anim.key(hg, "rotation_euler", SNAP, (-0.3, 0, 0), "CONSTANT")              # SNAP: slammed shut
    anim.squash(body, SNAP, 0.16, "CONSTANT")
    for f, d in ((SNAP + 2, (-0.18, 0.0, 0.0)), (SNAP + 4, (-0.08, 0.0, 0.0)), (SNAP + 8, (0.0, 0.0, 0.0))):
        anim.key(sh, "rotation_euler", f, tuple(a + b for a, b in zip(fire, d)), "CONSTANT")   # recoil, settle
    anim.squash(body, SNAP + 2, -0.08, "CONSTANT")
    anim.squash(body, SNAP + 6, 0.0, "CONSTANT")
    anim.key(hg, "rotation_euler", SNAP + 10, (0.1, 0, 0), "CONSTANT")
    sc.frame_set(1)
    drip = s15._claw_pt()
    meadow.drips((drip.x, drip.y, drip.z - 0.05), 1, SNAP, every=5, fall=max(0.3, drip.z - 0.02))
    sc.frame_set(SNAP)
    bpy.context.view_layer.update()
    muzzle = emp[1].matrix_world.translation.copy()
    shot_dir = (ear - muzzle).normalized()

    # ---- Kai: frozen (fear, terror as it cocks), thrown back flipping on the snap, lands on his back at kai_down
    for f, lean in ((1, 0.0), (COCK + 2, 0.4), (SNAP, 0.4)):
        flinched(lean)
        s15._key_pose(k, f)
    y0 = loc.y + BACK.y
    for i in range(1, 9):                                      # 19-35 on 2s: up and back, twisting round first,
        u = i / 8                                              # then laid flat on his back (head to the pond)
        e = acting.ease(u, "out")
        z = 1.0 + 4.2 * math.sin(math.pi * u) ** 1.2
        spin = (math.pi + math.radians(b2.HEAD_DIR)) * acting.ease(min(1.0, u / 0.55), "inout")
        tilt = 1.45 * acting.ease(max(0.0, (u - 0.3) / 0.7), "in")
        s15._pose(k, s15.BLOWN, (loc.x + 0.5 * e, y0 - 2.2 * e, z), (tilt, 0, spin))
        s15._key_pose(k, SNAP + 1 + 2 * (i - 1))
    hip = acting.lie(k, b2.HIPS, b2.HEAD_DIR, spec=acting.LYING_V3_L)
    s15._key_pose(k, LAND)
    rest = k["arm"].location.copy()
    for f, dz in ((LAND + 2, 0.55), (LAND + 4, 0.0), (LAND + 6, 0.12), (LAND + 8, 0.0)):   # the bounce
        k["arm"].location = rest + Vector((0, 0, dz))
        s15._key_pose(k, f)
    k["arm"].location = rest
    s15._flush_keys(k)
    shadow = bpy.data.objects.get("kai_down_shadow")
    if shadow is not None:                                     # lie()'s contact shadow: only once he is down
        full = tuple(shadow.scale)
        anim.key(shadow, "scale", 1, (0, 0, 0), "CONSTANT")
        anim.key(shadow, "scale", LAND, full, "CONSTANT")
    acting.expression(k, "fear", 1)
    acting.expression(k, "terror", COCK + 2)
    acting.expression(k, "surprised", SNAP + 1)
    acting.expression(k, "dazed", LAND)
    acting.blink(k, 1, SNAP - 1, at=(4,))
    acting.look_at(k, muzzle, 1, SNAP, darts=False)
    for f, v in ((LAND, 1.0), (LAND + 30, 1.0), (LAND + 34, 0.6), (LAND + 46, 0.6), (LAND + 50, 1.0),
                 (LAND + 58, 1.0), (LAND + 62, 0.55)):         # out cold, then dazed half-blinks (S15b goes on)
        hero.face(k, "blink", f, v)

    # ---- the blast: the streak along the shot, the ring, the sapling and the grove pop in order, glowing stumps
    grove = isl["trees"][-len(diorama.grove_spots()):]
    trees = [isl["sapling"]] + list(grove)
    sx, sy = diorama.sapling_spot()[:2]
    sts = [diorama.splinter_stump((sx, sy, 0.0), 0.3, 1.2, blast_from=diorama.MAP["blast"], seed=1,
                                  smoke=(SNAP + 4, n + 10))]          # as bGqrs places it in S15b on
    sts += diorama.stumps(diorama.grove_spots(), diorama.MAP["blast"], smoke=(SNAP + 10, n + 10))
    d = Vector((diorama.BLAST_LINE[0], diorama.BLAST_LINE[1], 0))
    t2 = Vector((loc.x, loc.y, 2.0)) + d * 6.0
    yaw2 = math.degrees(math.atan2(d.x, d.y))                  # the camera behind the line, looking down it
    c2 = dv2._camera("S15_line", CUT2, t2, 95.0, 46.0, yaw=yaw2)   # (the streak turns to face this camera)
    fx = erase.erase_trees(trees, origin=tuple(muzzle), f0=SNAP, cam=c2, stumps=sts,
                           direction=(shot_dir.x, shot_dir.y), speed=2.0)
    if fx["flash"] is not None:                                # the 2D pass has the flash
        bpy.data.objects.remove(fx["flash"], do_unlink=True)
    pitch = math.atan2(shot_dir.z, math.hypot(shot_dir.x, shot_dir.y))
    for o in fx["streak"]:                                     # the streak climbs with the shot (past his ear)
        o.rotation_euler = (o.rotation_euler.x, -pitch, o.rotation_euler.z)
    print("S15 MUZZLE", tuple(round(v, 3) for v in muzzle), "SHOT_DIR", tuple(round(v, 3) for v in shot_dir),
          "AIM_ERR", round(err, 2), "POPS", fx["pop_frames"], "HIP", tuple(round(v, 2) for v in hip), flush=True)

    # ---- cameras, every move on 1s
    # C1 1-23: down the barrel, low behind the claw, Kai's face sharp; a slow push-in
    hd = Vector((shot_dir.x, shot_dir.y, 0)).normalized()
    side = Vector((-hd.y, hd.x, 0))                            # to the line's left (east of it, the claw's far side)
    behind = muzzle - hd * 9.0 - side * 1.2 + Vector((0, 0, 0.6))
    c1 = dv2._camera("S15_barrel", 1, face, (behind - face).length, 10.0)
    c1.data.lens = 45.0
    for f in range(1, CUT2):
        u = acting.ease((f - 1) / (CUT2 - 2), "inout")
        _key_cam(c1, f, behind.lerp(muzzle - hd * 6.5 - side * 0.9 + Vector((0, 0, 0.5)), u), face)
    # C2 24-69: along the line from behind the shrimp, high: the shot runs away from us past Kai into the grove,
    # he flips back and lands, the trees pop in order; shaken on 2s
    import random
    rnd = random.Random(8)
    sign, jit = 1, (1.0, 0.0)
    for f in range(CUT2, CUT3):
        u = acting.ease((f - CUT2) / (CUT3 - 1 - CUT2), "out")
        dist = 95.0 - 18.0 * u
        i = f - CUT2
        off = (0, 0, 0)
        if i < 16:
            width = dist * (36.0 * 9 / 16) / dv2.LENS
            amp = 0.05 * (0.005 / 0.05) ** ((i // 2 * 2) / 16) * width
            if i % 2 == 0:
                sign = -sign
                jit = (rnd.uniform(0.7, 1.0), rnd.uniform(-0.4, 0.4))
            off = (amp * sign * jit[0], 0, amp * jit[1])
        dv2._key(c2, f, t2.lerp(Vector((hip.x, hip.y, 1.0)) + d * 4.0, u), dist, 46.0 + 4.0 * u, off, yaw=yaw2)
    # C3 70-end: from his feet (south-east), high: the smoking stumps in front, Kai on his back beyond them, the
    # sapling's stump by his head; a slow push-in toward him (S15b continues close and low from his feet)
    t3a = Vector((hip.x, hip.y, 0.5)) + d * 3.0
    t3b = Vector((hip.x, hip.y + 1.5, 0.8))
    c3 = dv2._camera("S15_after", CUT3, t3a, 70.0, 50.0, yaw=-28.0)
    for f in range(CUT3, n + 1):
        u = acting.ease((f - CUT3) / (n - CUT3), "inout")
        dv2._key(c3, f, t3a.lerp(t3b, u), 70.0 - 22.0 * u, 50.0, yaw=-28.0 + 6.0 * u)
    keep = [k["arm"], root] + sts + [o for t in trees for o in (t if isinstance(t, (tuple, list)) else [t])]
    keep += [o for o in sc.objects if o.name.startswith(("puff", "erase", "splinter", "kai_down", "grass", "wisp", "stump", "landdust"))
             or any(getattr(c, "target", None) == k["arm"] for c in o.constraints)]   # (his cap and shoes)
    pairs = {c.name: t for t, c in (tr for tr in isl["trees"] if tr)}
    hid = _hide_occluders(c2, CUT2, CUT3 - 1, keep, pairs=pairs) + _hide_occluders(c3, CUT3, n, keep, pairs=pairs)
    print("S15 HIDDEN_OCCLUDERS", hid, flush=True)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], root] + list(k.get("cap", [])))


SHOTS = {"S15a": s15a, "S15": s15_snap}


# ---------------------------------------------------------------- S15's 2D pass (outside Blender)

def composite(raw, sub, out, face_px=(360, 520)):
    """S15's 2D pass on the rendered PNGs: the white flash on the snap (SNAP, SNAP+1: 1.0, 0.7) and helper 7's
    fx2d.impact_frame_v3 on SNAP+2..SNAP+5 (1s), bursting from his face (face_px, full-res pixels), the subject pass
    (render_shot --subject for those frames, in sub/subject/) keeping Kai and the claw clean silhouettes. Every other
    frame is copied. Writes out/0001.png...; join with diorama/join_parts.py --v3 S15 out:1-N."""
    import glob
    import shutil
    os.environ.setdefault("FPS", "24")
    sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    from channels.monsters import fx2d
    from motion.engine import FPS, cairo
    os.makedirs(out, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(raw, "[0-9]*.png"))):
        name = os.path.basename(path)
        f = int(name[:4])
        dst = os.path.join(out, name)
        if not SNAP <= f <= SNAP + 5:
            shutil.copyfile(path, dst)
            continue
        img = cairo.ImageSurface.create_from_png(path)
        cr = cairo.Context(img)
        if f < SNAP + 2:
            cr.set_source_rgba(1, 1, 1, (1.0, 0.7)[f - SNAP])
            cr.paint()
        else:
            sp = os.path.join(sub, "subject", name)
            subject = cairo.ImageSurface.create_from_png(sp) if os.path.exists(sp) else None
            start = (SNAP + 2 - 1) / FPS
            fx2d.impact_frame_v3(cr, (f - 1) / FPS + 1e-4, start, cx=face_px[0], cy=face_px[1], frames=4,
                                 subject=subject, seed=15)
        img.write_to_png(dst)
    return out


if __name__ == "__main__" and bpy is None:
    print(composite(*sys.argv[1:4]))
