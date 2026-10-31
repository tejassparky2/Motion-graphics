"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 1's shots:

    S08a  "And I was standing in it."  The night lab, close and low from the open (east) side: Kai has swivelled his
          chair toward the cracked tank, sneakers flat on the tiles. The spill from S08 slides in from the tank side
          and runs under his sneakers (ripples ring out from each shoe as it arrives); he glances down, a small lift
          first, then his head drops to his feet, and his face drops with it (fear). The camera rises on 1s from his
          sneakers to his face.
    S24bot  (B) "Option B: run while I can." (the bottom panel all through the 3-sentence S24 line): Kai stands west
          of the pond, frozen, eyes up at the butcher bird on the thorn tree; a crouch (anticipation), a snap turn,
          and he runs west, arms pumping, looking back over his shoulder in fear. The bird dives (its giant shadow
          sweeps over him on the way) and mantles over the shrimp, which keeps drinking until the last moment. The
          action stays in a horizontal band in the plate's lower half (in-place split); the camera pans with him on
          1s. The assembler adds the big B.

Frame counts come from ep01v3/timing.json (render_frames = frames + 12).
    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08a OUT [--frames A-B] [--still N --scale 0.5]
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper1 as d1
from channels.monsters.diorama import xprl as xv2
from channels.monsters.ep01v2 import helper1 as h3d
from channels.monsters.ep01v2 import helper5 as h5
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import acting, anim, diorama, diorama_lab, hero, lab, look, tuftwing
from channels.monsters.mk import shared_water as sw

BLUR = 10.0
GUESS = {"S08a": 54, "S24": 162}          # until ep01v3/timing.json lands


def _frames(shot):
    try:
        from channels.monsters.diorama_v3.shots import v3_frames
        return v3_frames(shot)
    except (OSError, KeyError):
        return GUESS[shot]


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _move(cam, f0, f1, path, n, extend=None):
    """Key `cam` on every frame 1..n along `path(u)` -> (target, dist, tilt, yaw), u eased from f0 to f1: the slow
    1s move (DOF focus and the miniature f-stop follow the distance). extend=(fa, fb, du): after the move, u keeps
    going linearly from 1 to 1 + du over fa..fb (a slow drift to the end)."""
    for f in range(1, n + 1):
        u = _ease((f - f0) / max(1, f1 - f0))
        if extend and f > extend[0]:
            u = 1.0 + extend[2] * min(1.0, (f - extend[0]) / max(1, extend[1] - extend[0]))
        t, dist, tilt, yaw = path(u)
        t = Vector(t)
        el, az = math.radians(tilt), math.radians(yaw)
        cam.location = t + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.dof.focus_distance = dist
        cam.data.dof.aperture_fstop = diorama.fstop_for(dist, cam.data.lens, BLUR)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)


def _bone_world(rig, name, tail=False):
    pb = rig["bone"](name)
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _disc(name, center, rad, mat, z, rnd, verts=22):
    vs = [(math.cos(k / verts * 2 * math.pi) * rad * rnd.uniform(0.84, 1.1),
           math.sin(k / verts * 2 * math.pi) * rad * rnd.uniform(0.84, 1.1), 0) for k in range(verts)]
    return lab._mesh(name, vs, [tuple(range(verts))], mat, (center[0], center[1], z))


def _spill_front(a, b, f0, f1, width=0.9, seed=8):
    """The water's front sliding from `a` to `b` (floor points) between f0 and f1: overlapping discs that swell into
    place one after another, each with a pale rim a touch larger under it (the meniscus catching the tank light)."""
    water = lab._water_floor()
    rnd = random.Random(seed)
    a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0))
    side = Vector((-(b - a).y, (b - a).x, 0)).normalized()
    k = 16
    for i in range(k):
        u = i / (k - 1)
        p = a.lerp(b, u) + side * 0.35 * math.sin(u * 5.0) * width
        rad = width * (0.75 + 0.35 * math.sin(u * math.pi)) * rnd.uniform(0.9, 1.1)
        ts = f0 + (f1 - f0) * u
        for nm, mat, r, z in (("w", water, rad, 0.032),):                 # (rims: shared_water.adopt)
            d = _disc(f"s08a_{nm}{i}", p, r, mat, z + i * 0.0001, random.Random(seed * 100 + i))
            d.visible_shadow = False
            anim.key(d, "scale", ts - 1, (0.001, 0.001, 1), "CONSTANT")
            anim.key(d, "scale", ts + 2, (1.12, 1.12, 1))                  # overshoot as it lands...
            anim.key(d, "scale", ts + 5, (1.0, 1.0, 1))                    # ...and settles


def _ripples(at, f0, n, rings=3):
    """Thin rings spreading from a sneaker when the water reaches it (on 2s, fading by shrinking their alpha)."""
    for j in range(rings):
        m = look.fade(f"s08a_rip_m{j}", look.hexc("#e6fbff"), 0.0)
        mix = m.node_tree.nodes["Mix"].inputs[0]
        vs, faces = [], []
        seg = 28
        for k in range(seg):
            a = k / seg * 2 * math.pi
            for r in (1.0, 1.08):
                vs.append((math.cos(a) * r, math.sin(a) * r, 0))
        for k in range(seg):
            i0, i1 = 2 * k, 2 * ((k + 1) % seg)
            faces.append((i0, i1, i1 + 1, i0 + 1))
        ring = lab._mesh(f"s08a_rip{j}", vs, faces, m, (at[0], at[1], 0.045))
        ring.visible_shadow = False
        s = f0 + j * 6
        anim.key(ring, "scale", s - 1, (0.2, 0.2, 1), "CONSTANT")
        anim.key(ring, "scale", s + 16, (1.5, 1.5, 1))
        lab._ksock(mix, s - 1, 0.0, "CONSTANT")
        lab._ksock(mix, s, 0.75, "LINEAR")
        lab._ksock(mix, s + 16, 0.0, "LINEAR")


def _smooth_water(n):
    """The shared spill material (lab._water_floor) restyled for a close shot: broader, softer ripples (its fine
    speckle reads as gravel this close) that shimmer on 2s (4D noise, W keyed)."""
    m = lab._water_floor()
    nz = next(x for x in m.node_tree.nodes if x.type == "TEX_NOISE")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 2.4
    nz.inputs["Detail"].default_value = 1.0
    w = nz.inputs["W"]
    for f in range(1, n + 2, 2):
        w.default_value = f * 0.035
        w.keyframe_insert("default_value", frame=f)
    for fc in anim.all_fcurves(m.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return m


def _stand_look(rig, look_yaw=0.0, lift=0.0):
    """Standing in the spill before he sees it (helper 4's standing rig conventions): legs straight, arms loose, the
    head turned `look_yaw` toward his right (the tank) and lifted by `lift` (anticipation)."""
    h4._reset(rig)
    _shoulders(rig, reset=True)
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4._aim(rig, f"{s_}_upper_leg", (sx * 0.08, -0.04, -1.0))
        h4._aim(rig, f"{s_}_lower_leg", (sx * 0.04, 0.05, -1.0))
        h4._aim(rig, f"{s_}_foot", (sx * 0.1, -1.0, -0.35))
    h4._aim(rig, "spine", (0.0, 0.02 + lift * 0.5, 1.0))
    h4._aim(rig, "chest", (0.0, 0.0 + lift, 1.0))
    h4._aim(rig, "neck", (-look_yaw * 0.4, 0.0, 1.0))
    h4._aim(rig, "head", (-look_yaw, -0.04 + lift * 0.5, 1.0))
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4._aim(rig, f"{s_}_upper_arm", (sx * 0.28, 0.02, -1.0))
        h4._aim(rig, f"{s_}_lower_arm", (sx * 0.12, -0.25, -1.0))
        h4._aim(rig, f"{s_}_hand", (sx * 0.1, -0.2, -1.0))


FEAR_FACE = {"eye_open": 1.0, "eye_black_small": 1.0, "eye_brow_up": 1.0, "eye_brow_down": 0.15, "lip_o": 0.7,
             "mouse_open": 0.25}                    # wide eyes (whites showing), tiny pupils, brows up and pinched, "o"


SHOULDERS = ("left_shoulder", "right_shoulder")


def _shoulders(rig, f=None, reset=False):
    """helper 4's BODY keys leave the shoulders out: reset and/or key them here."""
    for nm in SHOULDERS:
        pb = rig["bone"](nm)
        pb.rotation_mode = "QUATERNION"
        if reset:
            pb.rotation_quaternion = (1, 0, 0, 0)
        if f is not None:
            pb.keyframe_insert("rotation_quaternion", frame=f)
            for fc in anim.all_fcurves(rig["arm"].animation_data.action):
                if pb.name in fc.data_path:
                    for kp in fc.keyframe_points:
                        if abs(kp.co.x - f) < 0.01:
                            kp.interpolation = "CONSTANT"
    bpy.context.view_layer.update()


def fear_stand(rig, f=None, sway=0.0):
    """FEAR_STAND, S08a's last pose and S08b's first (import it from here): frozen in the water, knees bent and the
    weight back, a small hunch with the shoulders up, hands lifted to his waist, fingers spread, head only a little
    down (face to a camera above him: the eyes do the looking down). `sway` (+-0.03) is the tremble on 2s. The rig
    is lowered so the bent legs keep his soles on the floor. With `f`, keys the pose (and the rig's height) there.
    Uses helper 4's standing conventions (_aim: x = his left, y = his back, z = up)."""
    from channels.monsters.diorama_v3 import helper4 as h4_
    arm = rig["arm"]
    h4_._reset(rig)
    _shoulders(rig, reset=True)
    base = arm.get("stand_z", arm.location.z)
    arm["stand_z"] = base
    arm.location.z = base
    bpy.context.view_layer.update()
    ank0 = (arm.matrix_world @ rig["bone"]("left_foot").head).z
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4_._aim(rig, f"{s_}_upper_leg", (sx * 0.1, -0.32, -1.0))          # knees bent forward...
        h4_._aim(rig, f"{s_}_lower_leg", (sx * 0.05, 0.3, -1.0))           # ...shins back
        h4_._aim(rig, f"{s_}_foot", (sx * 0.1, -1.0, -0.35))
    h4_._aim(rig, "spine", (sway, 0.14, 1.0))                              # weight back
    h4_._aim(rig, "chest", (sway * 0.5, -0.06, 1.0))                       # a small hunch over it
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4_._aim(rig, f"{s_}_shoulder", (sx * 1.0, 0.05, 0.42))            # shoulders up
    h4_._aim(rig, "neck", (0.0, 0.02, 1.0))
    h4_._aim(rig, "head", (-sway, 0.14, 1.0))                              # face up to a camera above
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4_._aim(rig, f"{s_}_upper_arm", (sx * 0.5, -0.32, -0.8))          # elbows out and forward
        h4_._aim(rig, f"{s_}_lower_arm", (sx * 0.1, -0.95, 0.38))          # hands up to his waist...
        h4_._aim(rig, f"{s_}_hand", (sx * 0.35, -0.6, 0.72))               # ...palms out
    h4_._fingers(rig, -0.12)                                               # fingers spread stiff
    bpy.context.view_layer.update()
    arm.location.z = base + ank0 - (arm.matrix_world @ rig["bone"]("left_foot").head).z
    bpy.context.view_layer.update()
    if f is not None:
        h4_._key(rig, f)
        _shoulders(rig, f)
        arm.keyframe_insert("location", frame=f)
        for fc in anim.all_fcurves(arm.animation_data.action):
            if fc.data_path == "location":
                for kp in fc.keyframe_points:
                    if abs(kp.co.x - f) < 0.01:
                        kp.interpolation = "CONSTANT"


def _anchors(shot, cam, rig, n, extra=None):
    """Kai's eye anchors per frame (720x1280, top-left origin) for the 2D pass (bgqrs_post's format), plus `extra`
    (name -> world point)."""
    import json
    import os
    from bpy_extras.object_utils import world_to_camera_view
    from channels.monsters.ep01v2 import bgqrs as s3d
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        row = {}
        pts = {k_: s3d.kai_point(rig, k_) for k_ in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        pts.update(extra or {})
        for k_, p_ in pts.items():
            v = world_to_camera_view(sc, cam, p_)
            row[k_] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
        out[f] = row
    d = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                     "build", "monsters", "diorama_v3")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def s08a():
    from channels.monsters.diorama_v3 import helper4 as h4_
    global h4
    h4 = h4_
    n = _frames("S08a")
    diorama.setup()
    R = diorama_lab.room()
    # S08b's staging (helper 4): he has stood up and pushed the chair back; he stands in the spill's path between the
    # desk front and the power strip, facing the front of the room, turned a little toward the camera
    leak, end = Vector(R["tank"]["leak"]), Vector(R["strip"]["end"])
    pa, pb = Vector((leak.x, R["desk"]["front_y"] - 0.4, 0)), Vector((end.x + 0.2, end.y + 0.2, 0))

    def path(u):
        return pa.lerp(pb, u) + Vector((-0.6, -0.4, 0)) * math.sin(u * math.pi)

    feet = path(0.5)
    feet.z = 0.0
    chair = R["desk"]["chair"]
    chair.location.y -= 1.6
    chair.rotation_euler.z = math.radians(25)
    rig = hero.load((feet.x, feet.y, 0.0), scale=d1.KAI, outfit="earth")
    d1._tilt_cap(rig, 40.0)
    rig["arm"].rotation_mode = "XYZ"
    rig["arm"].rotation_euler = (0, 0, math.radians(18))
    bpy.context.view_layer.update()
    # the spill (S08) is on the tiles from the desk to the strip, except round his feet: there it is still arriving,
    # and slides under his sneakers from the desk side (f4-15)
    R["puddle"](-60, -12)
    for o in bpy.data.objects:
        if o.name.startswith("dl_spill") and o.name[8:].isdigit():
            d = (Vector((o.location.x, o.location.y, 0)) - feet).length
            if d < 2.2:
                ts = 5 + int(d * 4)
                o.animation_data_clear()
                anim.key(o, "scale", 1, 0.001, "CONSTANT")
                anim.key(o, "scale", ts, 0.001, "CONSTANT")
                anim.key(o, "scale", ts + 4, 1.0)
    _spill_front(path(0.3), feet + (feet - path(0.3)).normalized() * 1.2, 3, 15, width=1.0)
    toes = []
    for s_ in ("left", "right"):
        toes.append(_bone_world(rig, f"{s_}_foot", tail=True))
    for i, ft in enumerate(toes):                                  # rings as the water reaches each sneaker
        sw.ripple_rings(ft, 11 + i * 2, n=2, every=4, radius=0.45, k=2.2)
    # acting on 2s: looking back at the tank, a small lift as he hears the water (anticipation), he drops into
    # FEAR_STAND past it (overshoot: lower, hands higher), settles, then trembles (S08b opens on fear_stand(rig))
    arm = rig["arm"]
    k = h4._key
    for f, yaw, lift in ((1, 0.45, 0.0), (9, 0.4, 0.0), (14, 0.15, 0.12)):
        _stand_look(rig, look_yaw=yaw, lift=lift)
        h4._fingers(rig, 0.3)
        arm.location.z = arm.get("stand_z", arm.location.z)
        k(rig, f)
        _shoulders(rig, f)
        arm.keyframe_insert("location", frame=f)
    fear_stand(rig, None, 0.0)
    h4._aim(rig, "chest", (0.0, -0.16, 1.0))                       # overshoot: hunched a touch past it
    for s_, sx in (("left", 1.0), ("right", -1.0)):
        h4._aim(rig, f"{s_}_lower_arm", (sx * 0.1, -0.85, 0.55))
    k(rig, 20)
    _shoulders(rig, 20)
    arm.keyframe_insert("location", frame=20)
    for f, sway in ((24, 0.0), (28, 0.03), (32, 0.0), (36, -0.025), (40, 0.0), (44, 0.03), (48, 0.0), (52, -0.025),
                    (56, 0.0), (n, 0.0)):
        fear_stand(rig, f, sway)
    for fc in anim.all_fcurves(arm.animation_data.action):
        if fc.data_path == "location":
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    # face (mk/acting): a blank look back at the tank, a blink, then it drops: wide eyes, tiny pupils, brows up and
    # pinched, a small "o"; the eyes (not the head) go down to his shoes, lightly, so the lids stay open
    acting.EXPR.setdefault("fear_wide", FEAR_FACE)
    acting.expression(rig, "neutral", 1)
    acting.expression(rig, "surprised", 17, value=0.8)
    acting.expression(rig, "fear_wide", 20)
    acting.look_at(rig, R["tank"]["center"], 1, 12)
    acting.look_at(rig, tuple(feet), 15, n, strength=0.15)
    acting.blink(rig, 1, n, at=(7,), every=(40, 60))
    hero.line_width(rig, 0.0028)
    sc = bpy.context.scene
    sc.frame_set(30)
    face = Vector(__import__("channels.monsters.ep01v2.bgqrs", fromlist=["x"]).kai_point(rig, "eyes"))
    sc.frame_set(1)
    mid = feet + Vector((0, 0, 0.3))
    plug = Vector(R["strip"]["spark_at"])
    end_t = face.lerp(plug, 0.42) + Vector((0, 0, -0.6))
    # from the open front, low: the camera rises on 1s from his sneakers in the water to his face, and pulls back
    # just enough at the end to keep the cause in a lower corner: the strip, the wet cable running to his feet
    cam = R["cam"]("cam_s08a", tuple(mid), dist=27.0, tilt=42.0, yaw=-22.0, lens=100.0, blur=BLUR)

    def path_cam(u):
        # u 0..1: the rise (f3-22, so his face is in frame as it drops at f20); 1..1.1: a slow push-in to the end
        r, p_ = min(u, 1.0), max(0.0, u - 1.0)
        return (mid.lerp(end_t, 0.08 + 0.92 * r), 27.0 + 7.0 * r - 18.0 * p_, 42.0 + 2.0 * r, -22.0 - 8.0 * r - 10 * p_)

    _move(cam, 3, 22, lambda u: path_cam(u), n, extend=(22, n, 0.1))
    # the plugs fizz: a cold flicker on his legs and the water (on 1s), with 2D sparks over them in the post pass
    fl = lab._light("s08a_fizz", "POINT", tuple(plug + Vector((0.0, -0.4, 0.6))), (0, 0, 0), 0.0, "#bfe6ff", 0.3)
    rnd = random.Random(5)
    for f in range(1, n + 1):
        on = f >= 4 and rnd.random() < 0.55
        lab._kprop(fl.data, "energy", f, (rnd.uniform(120, 320) if on else 8.0), "CONSTANT")
    R["flicker"]([30, 33])                                         # the lights stutter: the plugs are fizzing
    _anchors("S08a", cam, rig, n, extra={"plug": plug, "feet": feet.copy()})
    sw.adopt(R)                                                    # helper 2's shared water look (S07-S08b)
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["arm"]] + list(rig.get("cap", [])))


AWAY = Vector((-0.85, -0.53, 0.0))   # away from the thorn tree (its bearing from the pond is ~58 deg): south-west
RUN_TO = 8.0                         # how far he gets (units): to the frame's left edge
STEP = 0.09                          # run step (armature units): quick short steps, a scamper at toy scale


def _facing(d):
    """hero rot_z (degrees) that faces Kai along the ground direction d (he faces his own -Y)."""
    return math.degrees(math.atan2(d.x, -d.y))


def s24bot():
    from channels.monsters.diorama_v3 import xprl as xv3            # (lazy: shots.py imports both modules)
    n = _frames("S24")
    diorama.setup()
    isl, _ = xv2._set(n, kai_down=False)
    sh = xv3._shrimp(n)                                             # drinking on the north-east shore
    shrimp = Vector(xv3.SHRIMP)
    perch = Vector(isl["thorn"]["perch"])
    pond = Vector((*diorama.MAP["pond"], 0.0))
    start = pond + AWAY * 4.3                                       # at the pond's south-west edge
    # the bird: dark from frame 1 (as in A), then the dive onto the shrimp from the north-east (screen right), its
    # giant shadow sweeping in ahead of it
    f_dive, f_hit = 58, 84
    bird = x3._bird_drop(isl["thorn"], f_dive, f_hit, n, kai_at=tuple(shrimp - AWAY * 12.0))
    # the plunge itself starts just off screen right (the perch is far out of the panel), so the whole swoop reads
    lift = bird["lift"]
    p0 = Vector(lift.location)
    bpy.context.scene.frame_set(f_hit)
    p1 = Vector(lift.location)
    bpy.context.scene.frame_set(1)
    for fc in anim.all_fcurves(lift.animation_data.action):
        if fc.data_path == "location":
            for i in reversed([i for i, kp in enumerate(fc.keyframe_points) if f_dive <= kp.co.x <= f_hit]):
                fc.keyframe_points.remove(fc.keyframe_points[i])
    near = p0.lerp(p1, 0.62)
    for t in range(f_hit - f_dive + 1):
        u = t / (f_hit - f_dive)
        anim.key(lift, "location", f_dive + t, tuple(near.lerp(p1, u * u * (3 - 2 * u))), "LINEAR")
    anim.key(lift, "location", f_dive - 1, tuple(p0), "CONSTANT")
    x3._mantle(bird, f_hit - 2, f_hit + 4)
    h5._rage_light(bird, 1, perch.z + (tuftwing.CENTER[2] - 0.1) * h5.BIRD_SCALE)
    for e in sh["eyes"]:                                            # it only notices as the claws close
        anim.key(e, "scale", f_hit - 1, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", f_hit + 1, (0.78, 1, 0.78), "CONSTANT")
    for h in sh["hi"]:
        anim.key(h, "scale", f_hit - 1, (1, 1, 1), "CONSTANT")
        anim.key(h, "scale", f_hit + 1, (1.35, 1.35, 1.35), "CONSTANT")
    xv2._twos(tuftwing._animated(bird) + sh["eyes"] + sh["hi"])
    # Kai: frozen facing the thorn tree (the bird), a crouch, the snap turn, then the run away from the pond
    face_tree, face_away = _facing(-AWAY), _facing(AWAY)
    k = x3._hero(tuple(start), face_tree)
    d1._tilt_cap(k, 30.0)
    hero.line_width(k, 0.0026)
    arm = k["arm"]
    P = x3.Pose(k)
    f_crouch, f_turn, f_run = 26, 34, 38

    def frozen(P, t):
        P.rot("spine", (-6, 0, 0))                                  # leaning back from it
        P.rot("neck", (-12, 0, 0))
        P.rot("head 1", (-26, 0, 0))                                # eyes up at the bird on the tree
        x3._arms_down(P, 14)
        P.aim("upper_arm.R", (-0.35, -0.55, -0.6))                  # hands up by his chest
        P.aim("forearm.R", (0.1, -0.45, 0.9))
        P.aim("upper_arm.L", (0.35, -0.55, -0.6))
        P.aim("forearm.L", (-0.1, -0.45, 0.9))

    x3._walk(P, k, (Vector((0, 0, 0)), Vector((0, 0.001, 0))), 1, f_turn, 0.2, "R", crouch=(0.0, 0.1), upper=frozen,
             every=2)
    steps = RUN_TO / x3.SCALE / STEP

    def run_upper(P, t):
        ph = math.sin(t * steps * math.pi)
        P.rot("spine", (8, 0, 0))                                   # leaning into the run
        P.rot("chest", (2, 0, 10))
        P.rot("neck", (-14, 0, 28))
        P.rot("head 1", (-40, 0, 42))                               # his face turned to us (the camera is on his left)
        P.aim("upper_arm.R", (-0.2, 0.55 * ph, -0.8))               # arms pumping, opposite to the legs
        P.aim("forearm.R", (-0.05, -0.85, 0.45 + 0.2 * ph))
        P.aim("upper_arm.L", (0.2, -0.55 * ph, -0.8))
        P.aim("forearm.L", (0.05, -0.85, 0.45 - 0.2 * ph))

    x3._walk(P, k, (Vector((0, 0, 0)), Vector((0, -RUN_TO / x3.SCALE, 0))), f_run, n, STEP, "L", crouch=(0.05, 0.05),
             upper=run_upper, every=2)
    for f, z in ((1, face_tree), (f_crouch, face_tree), (f_turn, face_tree), (f_turn + 2, face_away - 14.0),
                 (f_run, face_away)):                               # the snap turn, overshoot, settle
        arm.rotation_euler.z = math.radians(z)
        arm.keyframe_insert("rotation_euler", index=2, frame=f)
    acting.expression(k, "fear", 1, value=0.8)
    acting.expression(k, "surprised", f_turn)
    acting.expression(k, "terror", f_run + 4, value=0.9)
    acting.look_at(k, tuple(perch + Vector((0, 0, 3.0))), 1, f_turn - 2)
    acting.look_at(k, tuple(shrimp + Vector((0, 0, 2.0))), f_run, n)  # glancing back at it as he runs
    acting.blink(k, 1, n, seed=11, at=(14,))
    xv2._twos([arm])
    # side-on from the south-east (the tree is screen-right, he runs screen-left), high enough to fold everyone into
    # the panel's band; a slow pan with him on 1s
    side = Vector((-AWAY.y, AWAY.x, 0))                              # unused helper direction (screen depth)
    mid = start.lerp(shrimp, 0.5)
    a = (tuple(mid + Vector((0, 0, 1.0))), 84.0, 58.0, -32.0, 80.0, 0.2)
    b = (tuple(mid + AWAY * 2.0 + Vector((0, 0, 1.0))), 81.0, 58.0, -34.0, 80.0, 0.2)
    del side
    xv2._move("cam_s24bot_v3", 1, n, a, b, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[arm])


SHOTS = {"S08a": s08a, "S24bot": s24bot}
