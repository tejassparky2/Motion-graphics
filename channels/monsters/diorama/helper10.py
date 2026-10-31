"""Diorama style test (channels/monsters/DIORAMA_TEST.md), helper 10: D1-D5, test frames 1-115. Same window and beats as
S15 (the same audio), staged for the tilted toy-world camera (mk/diorama.py, island seed 31):

    D1  1-41   wide of the clearing, slow push-in: Kai kneels at the pond reaching toward the shrimp; it blinks, looks
               up (13), then its claw rises out of the pond on 2s and is held, dripping (22-41, silence)
    D2  42-49  closer, locked on the shrimp: the strike (42); flash 44-45 and impact frames 46-49 are 2D (composite)
    D3  50-79  the money shot: the fan blast toward +Y, the white ring, the trees in the fan pop into dust in order of
               distance, glowing stumps on a scorched swath; the camera pulls up and back (dist 160 -> 290) to reveal
               it, shaken on 2s
    D4  80-93  Kai blown back toward the camera (-Y), tumbling, landing on his back short of the pond (on 2s); the
               camera follows
    D5  94-115 closer and steeper over him on his back, dazed; the knocked-out stars (composite); eyes close 111-113

    blender -b -y -P channels/monsters/render_shot.py -- diorama D15 OUT [--frames A-B] [--still N --scale 0.5]
    blender -b -y -P channels/monsters/render_shot.py -- diorama D15 OUT_SUB --frames 46-49 --subject
    python channels/monsters/diorama/helper10.py OUT OUT_SUB out/monsters/diorama   (flash, impact, stars -> D15.mp4)

Characters on 2s/3s; every camera move and the 1s effects sit inside ones=(1, 95); D5 renders on 2s."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
try:
    import bpy
    from mathutils import Vector
except ImportError:                                            # composite() runs outside Blender
    bpy = None

from channels.monsters.ep01v2 import helper10 as s15  # noqa: E402  (S15's poses, effects and 2D pass)

A, C, D, E, F, G, END = s15.A, s15.C, s15.D, s15.E, s15.F, s15.G, s15.END
SHRIMP = (0.0, 0.4, 0.0)                                       # behind the pond (diorama.pond at (0.1, -2.6))
LENS, BLUR = 100.0, 12.0
HAZE = (0.97, 0.55)                                            # diorama.camera's default haze band
STAR_PX, CAP_BOX = 30, (60, 120, 600, 900)                     # the D5 stars and where to find the cap in D5
LAND_HIPS, LAND_YAW = (1.0, -11.5), 0.21                        # Kai's hips where he lands; his head points ~12 deg
                                                                # west of +Y, toward the pond


def _pos(target, dist, tilt, yaw=0.0):
    el, az = math.radians(tilt), math.radians(yaw)
    return Vector(target) + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))


def _key(c, frame, target, dist, tilt, offset=(0, 0, 0), yaw=0.0):
    """Key a diorama camera (place, aim, tilt-shift f-stop and the world's haze band) at one frame, CONSTANT: moves
    are keyed on every frame, so each frame is exact and the haze switches cleanly at the cuts."""
    from channels.monsters.mk import anim, diorama
    sc = bpy.context.scene
    p = _pos(target, dist, tilt, yaw)
    c.location = p + Vector(offset)
    c.rotation_euler = (Vector(target) - p).to_track_quat("-Z", "Y").to_euler()
    c.data.dof.focus_distance = dist
    c.data.dof.aperture_fstop = diorama.fstop_for(dist, c.data.lens, BLUR)
    c.data.clip_end = dist * 6
    c.keyframe_insert("location", frame=frame)
    c.keyframe_insert("rotation_euler", frame=frame)
    c.data.dof.keyframe_insert("focus_distance", frame=frame)
    c.data.dof.keyframe_insert("aperture_fstop", frame=frame)
    ms = sc.world.mist_settings
    ms.start, ms.depth = dist * HAZE[0], dist * HAZE[1]
    ms.keyframe_insert("start", frame=frame)
    ms.keyframe_insert("depth", frame=frame)
    for idb in (c, c.data, sc.world):
        ad = idb.animation_data
        if ad and ad.action:
            for fc in anim.all_fcurves(ad.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def _camera(name, frame, target, dist, tilt, yaw=0.0):
    from channels.monsters.mk import diorama
    c = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=LENS, blur=BLUR, frame=frame)
    _key(c, frame, target, dist, tilt, yaw=yaw)
    return c


def _ease(u):
    return u * u * (3 - 2 * u)


def _swath(origin, reach, half_angle, f0, frames=15):
    """The scorched fan on the ground, growing out from the blast origin with the ring (scaled from its tip)."""
    from channels.monsters.mk import anim, look, paintbg
    ox, oy = origin
    verts, n = [(0, 0, 0)], 24
    for i in range(n + 1):
        a = math.radians(-half_angle + 2 * half_angle * i / n)
        verts.append((math.sin(a) * reach, math.cos(a) * reach, 0))
    me = bpy.data.meshes.new("scorched_swath")
    me.from_pydata(verts, [], [(0, i, i + 1) for i in range(1, n + 1)])
    o = bpy.data.objects.new("scorched_swath", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = (ox, oy, 0.02)
    o.data.materials.append(paintbg.paint3("diorama_scorch", look.hexc("#6b5244"), look.hexc("#86684f"),
                                           look.hexc("#a3836a"), noise=0.3, scale=0.8))
    anim.key(o, "scale", f0 - 1, 0.0, "CONSTANT")
    for f in range(f0, f0 + frames + 1):
        anim.key(o, "scale", f, min(1.0, (f - f0 + 1) / frames), "CONSTANT")
    return o


def d15():
    from channels.monsters.mk import anim, diorama, erase, hero, meadow, puffshrimp
    sc = bpy.context.scene
    diorama.setup()
    isl = diorama.island(seed=31)

    # ---- the shrimp behind the pond, its claw dipped in the water (S15's keys)
    rig = puffshrimp.build(SHRIMP)
    root, body, sh, hg = rig["root"], rig["body"], rig["shoulder"], rig["hinge"]
    DIP, UP, STRIKE = (1.8, 0.0, 0.3), (0.35, 0.75, 0.0), (-0.45, 0.55, 0.0)
    anim.key(sh, "rotation_euler", A, DIP, "CONSTANT")
    anim.key(hg, "rotation_euler", A, (0.1, 0, 0), "CONSTANT")
    anim.key(root, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    anim.key(body, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    for f in range(A, 19, 6):
        anim.squash(body, f, -0.03, "CONSTANT")
        anim.squash(body, f + 3, 0.0, "CONSTANT")
    anim.key(root, "rotation_euler", 13, (0, 0, 0.18), "CONSTANT")   # notices the hand: turns and looks up
    anim.key(body, "rotation_euler", 13, (-0.14, 0, 0), "CONSTANT")
    for e in rig["eyes"]:
        anim.key(e, "scale", A, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 7, (1.1, 1, 0.1), "CONSTANT")
        anim.key(e, "scale", 8, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 20, (1.12, 1, 0.55), "CONSTANT")
    for j, f in enumerate(range(C, C + 8, 2)):
        u = (j + 1) / 4
        anim.key(sh, "rotation_euler", f, tuple(a + (b - a) * u for a, b in zip(DIP, UP)), "CONSTANT")
    anim.key(hg, "rotation_euler", C + 6, (0.5, 0, 0), "CONSTANT")
    anim.squash(body, C, 0.0, "CONSTANT")
    anim.squash(body, C + 6, -0.06, "CONSTANT")
    anim.key(sh, "rotation_euler", D, STRIKE, "CONSTANT")
    anim.key(hg, "rotation_euler", D, (-0.25, 0, 0), "CONSTANT")
    anim.squash(body, D, 0.14, "CONSTANT")
    anim.squash(body, D + 2, -0.04, "CONSTANT")
    anim.squash(body, E + 3, 0.0, "CONSTANT")
    sc.frame_set(C + 7)
    drip = s15._claw_pt()
    meadow.drips((drip.x, drip.y, drip.z - 0.05), C + 3, D, every=5, fall=max(0.3, drip.z - 0.02))
    sc.frame_set(D + 1)
    blast = s15._claw_pt(lowest=False)

    # ---- Kai on his knees at the pond's south edge, reaching across toward the shrimp
    k = hero.load((0, 0, 0), scale=s15.KAI_SCALE, outfit="world")
    reach = Vector((SHRIMP[0] + 0.25, SHRIMP[1] - 1.45, 2.05))
    loc = Vector((SHRIMP[0] - 0.45, SHRIMP[1] - 6.4, 0))
    for _ in range(3):
        s15._apply_kneel(k, loc, 1.0, reach)
        loc.y += (reach - s15._world(k, "right_upper_arm")).length - 2.55
    for f, s in ((A, 0.0), (A + 3, 0.2), (A + 6, 0.45), (A + 9, 0.7), (A + 12, 0.9), (A + 15, 1.0)):
        s15._apply_kneel(k, loc, s, reach + (1 - s) * Vector((0.3, -1.6, 1.3)))
        s15._key_pose(k, f)
    hero.face(k, "relaxed", A, 0.6)
    y0 = loc.y
    flight = []
    for f, back, tilt, spin in ((F, 0.4, 0.15, 0.0), (F + 2, 1.6, 0.35, 0.3), (F + 4, 3.0, 0.6, 1.0),
                                (F + 6, 4.2, 0.9, 1.8), (F + 8, 5.0, 1.2, 2.6), (F + 10, 5.6, 1.4, 3.1)):
        u = (f - F) / 10                                      # blown back, tumbling with a half twist
        s15._pose(k, s15.BLOWN, (loc.x + 0.1 * back, y0 - back * 1.6, 1.0 + 7.0 * u * (1 - u) * 1.6), (tilt, 0, spin))
        s15._key_pose(k, f)
        flight.append((f, s15._world(k, "hips")))
    hero.face(k, "surprised", F)
    land = Vector((0, 0, 0))                                   # on his back, head toward the pond (D6 continues)
    for _ in range(2):
        s15._pose(k, s15.LYING, tuple(land), (math.pi / 2, 0, math.pi + LAND_YAW))
        s15._ground(k)
        hip = s15._world(k, "hips")
        land += Vector((LAND_HIPS[0] - hip.x, LAND_HIPS[1] - hip.y, 0))
    s15._pose(k, s15.LYING, tuple(land), (math.pi / 2, 0, math.pi + LAND_YAW))
    s15._ground(k)
    s15._key_pose(k, G)
    flight.append((G, s15._world(k, "hips")))
    face = (s15._world(k, "head") + s15._world(k, "head", True)) / 2
    hero.face(k, "surprised", G)
    hero.face(k, "blink", END - 4, 0.5)
    hero.face(k, "blink", END - 2)
    s15._flush_keys(k)

    # ---- cameras (every move keyed on every frame, inside ones)
    t1a, t1b = Vector((0.0, -3.4, 2.0)), Vector((0.0, -2.6, 2.2))
    c1 = _camera("D1_wide", A, t1a, 150.0, 58.0, 40.0)        # from the south-west: Kai and the shrimp side by side
    for f in range(A, D):                                       # slow push-in
        u = _ease((f - A) / (D - 1 - A))
        _key(c1, f, t1a.lerp(t1b, u), 150.0 - 18.0 * u, 58.0, yaw=40.0)
    t2 = Vector((SHRIMP[0] - 0.6, SHRIMP[1] - 0.6, 2.0))
    _camera("D2_strike", D, t2, 80.0, 48.0, 40.0)
    t3a, t3b = Vector((0.0, -1.5, 2.0)), Vector((0.0, 14.0, 0.0))
    c3 = _camera("D3_reveal", E, t3a, 160.0, 64.0, 15.0)
    rnd = random.Random(8)
    sign = 1
    for f in range(E, F):                                       # pull up and back to reveal the swath, shaken on 2s
        u = _ease(min(1.0, (f - E) / 22))
        dist, tilt = 160.0 + 130.0 * u, 64.0 + 6.0 * u
        i = f - E
        off = (0, 0, 0)
        if i < 16:
            width = dist * (36.0 * 9 / 16) / LENS
            amp = 0.07 * (0.005 / 0.07) ** ((i // 2 * 2) / 16) * width
            if i % 2 == 0:
                sign = -sign
                jit = (rnd.uniform(0.7, 1.0), rnd.uniform(-0.4, 0.4))
            off = (amp * sign * jit[0], 0, amp * jit[1])
        _key(c3, f, t3a.lerp(t3b, u), dist, tilt, off, yaw=15.0)
    c4 = _camera("D4_blown", F, flight[0][1], 140.0, 70.0)
    pts = [(f, Vector((p.x, p.y, min(p.z, 4.0)))) for f, p in flight]
    for f in range(F, G):                                      # follow him (smooth, on 1s)
        j = max(i for i in range(len(pts)) if pts[i][0] <= f)
        fa, pa = pts[j]
        fb, pb = pts[min(j + 1, len(pts) - 1)]
        u = 0 if fb == fa else (f - fa) / (fb - fa)
        _key(c4, f, pa.lerp(pb, u), 140.0, 70.0)
    _camera("D5_dazed", G, face + Vector((0, -1.8, 0)), 80.0, 74.0)

    # ---- D3: the fan blast toward +Y: ring, streak, the trees in the fan erased, glowing stumps, scorched swath
    origin = (blast.x, blast.y)
    fan = diorama.blast_spots(isl["spots"], origin)
    spots = [isl["spots"][i] for i in fan]
    sts = diorama.stumps(spots, origin)
    fx = erase.erase_trees([isl["trees"][i] for i in fan], origin=tuple(blast), f0=E - 1, cam=c3, stumps=sts,
                           direction=(0.0, 1.0))
    if fx["flash"] is not None:                                 # the 2D pass has the flash
        bpy.data.objects.remove(fx["flash"], do_unlink=True)
    reach_r = max(math.hypot(x - origin[0], y - origin[1]) for x, y, *_ in spots) + 12
    _swath(origin, reach_r, 30.0, E - 1)
    hot = sorted(zip(spots, fx["pop_frames"]), key=lambda s: math.hypot(s[0][0], s[0][1]))[:9]
    s15._puff_smoke([(x, y, diorama.TREE * 0.7, tp) for (x, y, *_), tp in hot], END + 1, size=diorama.TREE * 0.6)
    print("D15 BLAST_ORIGIN", tuple(round(v, 3) for v in blast), "KAI_LYING", tuple(round(v, 3) for v in land),
          "FACE", tuple(round(v, 3) for v in face), "FAN", len(fan), flush=True)
    return dict(frames=END, step=2, ones=(A, G + 1), subject=[root])


SHOTS = {"D15": d15}


def composite(raw, sub, out_dir):
    """The 2D pass (S15's): flash 44-45, impact frames 46-49 on 2s from the subject pass, knocked-out stars in D5."""
    return s15.composite(raw, sub, out_dir, name="D15", star_px=STAR_PX, cap_box=CAP_BOX)


if __name__ == "__main__" and bpy is None:
    print(composite(sys.argv[1], sys.argv[2], sys.argv[3]))
