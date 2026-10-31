"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), bGqrs's shots: S01, S16, S17, S18. The same frame
counts and the same beats on the same frames as the 3D chest scene (channels/monsters/ep01v2/bgqrs.py), restaged
for the high toy camera (lens 70-120, tilt 40-80, the faces turned up to the lens).

The world after the snap: island(seed=31) with the fan's trees gone and hot-cut stumps (smoking) in their place; Kai
on his back at MAP["kai_down"], head toward the pond, face up; the puff-shrimp on his chest, leaning back so its own
face tips up to the camera, its claw cocked BESIDE his face (from above, a claw over his face would hide it).

    blender -b -y -P channels/monsters/render_shot.py -- diorama S01 OUT_DIR [--frames A-B] [--still N --scale 0.5]

Characters on 2s (faces snap on CONSTANT keys), every camera move on 1s (`ones`), the VFX (smoke, dust, drops) on 1s.
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.ep01v2 import bgqrs as s3d                 # Kai's face keys, the shrimp's lock-on and claw
from channels.monsters.mk import anim, diorama, hero, look, meadow

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ANCHORS = os.path.join(ROOT, "build", "monsters", "diorama")
FRAMES = {k: s3d.FRAMES[k] for k in ("S01", "S16", "S17", "S18")}   # cut + 12-frame handle, as in 3D
ORIGIN = (-0.809, 0.717)              # the snap's blast origin: the claw at the strike (helper10.py, MAP["shrimp"] based)
HIPS = diorama.MAP["kai_down"]        # where the blast throws him, on his back
_P = diorama.MAP["pond"]
HEAD_DIR = math.degrees(math.atan2(-(_P[0] - HIPS[0]), _P[1] - HIPS[1]))   # his head points at the pond (~12 deg)
UP = Vector((-math.sin(math.radians(HEAD_DIR)), math.cos(math.radians(HEAD_DIR)), 0))   # along him, toward his head
EAST = Vector((UP.y, -UP.x, 0))       # his left side (screen right from the south), where the shrimp's claw is
LEAN = 40.0                           # the shrimp leans back on his chest, so its face tips up toward the camera
BLUR = 12.0
# S01 (the hook: the shrimp's big eyes against the cocked claw must read). The puff-shrimp's face sits under its
# cream ruff, so it shows from above only when the shrimp faces his face and leans back (as in S16); his face shows
# only from his chin side (lying face up, his cap's brim points at the sky). So: from the south, steep (tilt 70), the
# shrimp leaning back 50. tilt, dist, lens, yaw, aim offsets toward his head and away from the camera (units); the
# shrimp's lean back (deg).
S01_CAM = (70.0, 62.0, 110.0, 0.0, 1.5, 0.0)
S01_LEAN = 50.0


# ---------------------------------------------------------------- the world after the snap

def _set(n):
    """The island after the snap: seed 31, the fan's trees gone, hot-cut stumps where they stood, glowing (bloom)
    and smoking. Returns the stumps' (x, y) spots, nearest the blast first."""
    isl = diorama.island(seed=31)
    fan = sorted(diorama.blast_spots(isl["spots"], ORIGIN))
    gone = {c.name for i in fan if isl["trees"][i] for o in isl["trees"][i] for c in [o] + list(o.children_recursive)}
    for name in gone:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    spots = [isl["spots"][i] for i in fan]
    diorama.stumps(spots, ORIGIN)
    for name, strength in (("stump_hot", 2.2), ("stump_core", 3.0)):
        m = bpy.data.materials.get(name)
        em = next((nd for nd in m.node_tree.nodes if nd.type == "EMISSION"), None) if m and m.use_nodes else None
        if em is not None:
            em.inputs["Strength"].default_value = strength
    near = sorted(spots, key=lambda s: math.hypot(s[0] - ORIGIN[0], s[1] - ORIGIN[1]))
    meadow.smoke([(x, y, diorama.TREE * 0.55) for x, y, *_ in near[:7]], -50, n + 10, every=16, rise=11.0,
                 size=diorama.TREE * 0.5)
    return [(x, y) for x, y, *_ in near]


# On his back, relaxed (so it reads as LYING from above, not as a standing T-pose): helper 10's LYING_RELAXED (S15's
# end) with both arms loose at his sides, hands by his hips (the shrimp sits on his chest), head tilted toward it.
# Directions in Kai's own frame: +X his right, +Y forward (up once he lies down), +Z toward his head.
LYING = [("spine", (0, 0, 1)), ("chest", (0, 0, 1)), ("upper_chest", (0, 0, 1)), ("neck", (-0.1, 0.1, 1)),
         ("head", (-0.4, 0.2, 1)),
         ("right_upper_arm", (0.45, 0.1, -1)), ("right_lower_arm", (0.3, 0.3, -1)),
         ("left_upper_arm", (-0.45, 0.1, -1)), ("left_lower_arm", (-0.35, 0.25, -1)),
         ("left_upper_leg", (-0.12, 0.45, -1)), ("right_upper_leg", (0.15, 0.3, -1)),
         ("left_lower_leg", (-0.1, -0.2, -1)), ("right_lower_leg", (0.15, -0.12, -1)),
         ("left_foot", (-0.25, 1, -0.3)), ("right_foot", (0.3, 1, -0.3))]


def _kai(head=None):
    """Kai on his back at MAP["kai_down"], relaxed (LYING), head toward the pond; a soft contact shadow under him and
    grass tufts over his outline, so he lies IN the grass. `head`: another head direction (his own frame)."""
    from channels.monsters.ep01v2 import helper10 as s15
    rig = hero.load((0, 0, 0), scale=s3d.KAI_SCALE, outfit="world")
    rot = (math.pi / 2, 0, math.pi + math.radians(HEAD_DIR))
    spec = [(b, head if (b == "head" and head) else d) for b, d in LYING]
    s15._pose(rig, spec, (HIPS[0], HIPS[1], 0.5), rot)
    hip = s15._world(rig, "hips")
    rig["arm"].location += Vector((HIPS[0] - hip.x, HIPS[1] - hip.y, 0))
    s15._ground(rig)
    bpy.context.view_layer.update()
    hero.line_width(rig, 0.0025)
    hip = s15._world(rig, "hips")
    sh = look.blob_shadow("kai_down_shadow", (hip.x, hip.y, 0.03), (1.9, 5.2))
    sh.rotation_euler = (0, 0, math.radians(HEAD_DIR))
    _tufts(hip)
    return rig


def _tufts(hip, seed=21):
    """Grass tufts and a few flowers along his outline, overlapping it a little (lit paint, so they take the sun)."""
    rnd = random.Random(seed)
    blade = diorama.lit_paint("d16_tuft", "#2f8a36", "#4cb348", "#8fdb62")
    petals = [diorama.lit_paint(f"d16_flower{i}", *c) for i, c in enumerate((("#c9c9e0", "#ffffff", "#ffffff"),
                                                                             ("#d9a400", "#ffd23f", "#fff2a8")))]
    for along, side in ((3.6, 1.15), (2.2, -1.35), (0.6, 1.5), (-0.8, -1.25), (-2.4, 0.95), (-3.6, -0.8),
                        (-4.2, 0.7), (1.4, 1.6), (3.0, -1.0), (-1.6, 1.3)):
        c = Vector(hip) + UP * along + EAST * side * rnd.uniform(0.9, 1.1)
        for k in range(rnd.randint(4, 6)):                         # a clump of blades leaning outward
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.09, radius2=0.0, depth=rnd.uniform(0.7, 1.1),
                                            location=(c.x + rnd.uniform(-0.25, 0.25), c.y + rnd.uniform(-0.25, 0.25),
                                                      0.4))
            o = bpy.context.object
            o.rotation_euler = (rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), rnd.uniform(0, 3))
            o.data.materials.append(blade)
        if rnd.random() < 0.5:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=0.16, location=(c.x, c.y, 0.75))
            bpy.context.object.data.materials.append(rnd.choice(petals))


def _shrimp(rig, n, claw="face", yaw=None, lean=LEAN, side=1):
    """Low on his chest, facing his face, leaning back. claw="face": cocked beside his face, pointing at it (S01's
    threat); "jacket": held out over his chest so its drops land on the jacket (S17). Breathes on 2s."""
    yaw = 180 + HEAD_DIR if yaw is None else yaw
    sh = s3d._shrimp(rig, yaw=yaw, chest_offset=tuple(-UP * 0.55 + Vector((0, 0, 0.15))))
    sh["root"].rotation_euler = (math.radians(-lean), 0, math.radians(yaw))
    bpy.context.view_layer.update()
    nose = s3d.kai_point(rig, "nose")
    if claw == "face":
        sh["cock"] = s3d.raise_claw(sh, nose + EAST * 1.3 * side - UP * 0.4 + Vector((0, 0, 1.6)), nose)
        s3d.cock(sh, 1)
    else:
        sh["cock"] = _over_jacket(sh, rig)
        anim.key(sh["shoulder"], "rotation_euler", 1, sh["cock"], "CONSTANT")
        anim.key(sh["hinge"], "rotation_euler", 1, (0.5, 0.0, 0.0), "CONSTANT")
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.035)
    anim.on_twos([sh["body"]], step=2)
    s3d.lock_on(sh, s3d.kai_point(rig, "eyes"), 1)
    return sh


def _hit(p):
    """(location, normal, material name) of the first surface straight below p that isn't the shrimp or a drop."""
    dg = bpy.context.evaluated_depsgraph_get()
    o = Vector(p) - Vector((0, 0, 0.02))
    for _ in range(12):
        hit, loc, nrm, idx, ob, _m = bpy.context.scene.ray_cast(dg, o, Vector((0, 0, -1)))
        if not hit:
            return None
        if not ob.name.startswith(("puff", "drop", "d16_")):
            ev = ob.evaluated_get(dg)
            mi = ev.data.polygons[idx].material_index if ob.type == "MESH" else 0
            mats = ev.data.materials if ob.type == "MESH" else []
            return loc, nrm, (mats[mi].name if 0 <= mi < len(mats) and mats[mi] else "")
        o = loc - Vector((0, 0, 0.01))
    return None


def _over_jacket(sh, rig):
    """Raise the claw so it reaches down over his jacket BESIDE the shrimp (his left chest and arm), well clear of his
    face: try cloth spots there, nearest the shrimp first, and keep the first whose claw tip hangs over cloth at least
    2 units from his eyes. Returns the shoulder pose."""
    chest = s3d.kai_point(rig, "chest")
    eyes = s3d.kai_point(rig, "eyes")
    pose = None
    for k in (1.0, 1.3, 0.7, 1.6):
        for u in (-0.3, -0.7, 0.0, -1.1):                          # level with the shrimp or toward his belly
            spot = _hit(chest + EAST * k + UP * u + Vector((0, 0, 3)))
            if not spot or "huku" not in spot[2]:
                continue
            pose = s3d.raise_claw(sh, spot[0] + Vector((0, 0, 1.4)), spot[0])
            tip = s3d.claw_tip(sh)
            h = _hit(tip)
            if h and "huku" in h[2] and (tip - eyes).length > 2.0:
                return pose
    return pose


def _dust(rig, n, count=46, seed=8):
    """Settling dust: small pale motes sinking slowly through the light, shrinking near the ground (1s)."""
    rnd = random.Random(seed)
    m = look.flat("d16_dust", look.hexc("#f3e6c8"))
    c = s3d.kai_point(rig, "chest")
    for _ in range(count):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(0.05, 0.1), location=(0, 0, 0))
        o = bpy.context.object
        o.name = "d16_dust"
        o.data.materials.append(m)
        x, y, z = c.x + rnd.uniform(-6, 6), c.y + rnd.uniform(-7, 9), rnd.uniform(1.5, 9.0)
        f0, f1 = rnd.randint(-20, 30), n + rnd.randint(0, 40)
        drift = Vector((rnd.uniform(-0.6, 0.6), rnd.uniform(-1.2, 0.2), -rnd.uniform(1.0, 2.2)))
        anim.key(o, "location", f0, (x, y, z), "LINEAR")
        anim.key(o, "location", f1, Vector((x, y, z)) + drift, "LINEAR")
        anim.key(o, "scale", f0, 1.0, "LINEAR")
        anim.key(o, "scale", f1, 0.2, "LINEAR")


def _world(shot, claw="face", head=None, **shrimp):
    n = FRAMES[shot]
    diorama.setup()
    stumps = _set(n)
    rig = _kai(head)
    sh = _shrimp(rig, n, claw, **shrimp)
    diorama.sunbeam(s3d.kai_point(rig, "chest"), radius=7.0)     # shared: the same light on him S15-S21
    _dust(rig, n)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    return n, rig, sh, stumps


# ---------------------------------------------------------------- the camera

def _move(cam, n, keys, look_at, yaw=0.0):
    """Animate the diorama camera on 1s through keys [(frame, tilt, dist, lens)] (smoothstep between keys), aimed at
    look_at(f) (a world point), the tilt-shift f-stop and the haze re-solved every frame."""
    sc = bpy.context.scene

    def at(f):
        for (fa, *a), (fb, *b) in zip(keys, keys[1:]):
            if fa <= f <= fb:
                u = (f - fa) / (fb - fa)
                u = u * u * (3 - 2 * u)
                return [x + (y - x) * u for x, y in zip(a, b)]
        return list(keys[-1][1:] if f > keys[-1][0] else keys[0][1:])

    for f in range(1, n + 1):
        tilt, d, lens = at(f)
        el, az = math.radians(tilt), math.radians(yaw)
        back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        cam.location = look_at(f) + back * d
        cam.rotation_euler = (-back).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = lens
        cam.data.dof.focus_distance = d
        cam.data.dof.aperture_fstop = diorama.fstop_for(d, lens, BLUR)
        for path in ("location", "rotation_euler"):
            cam.keyframe_insert(path, frame=f)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        ms = sc.world.mist_settings
        ms.start, ms.depth = d * 0.97, d * 0.55
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    sc.camera = cam
    return cam


def _anchors(shot, cam, rig, sh=None, extra=None):
    """Screen positions (720x1280, top-left origin) of his eyes and the claw tip per frame (plus `extra`: name ->
    fn() -> world point), for the 2D pass."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, FRAMES[shot] + 1):
        sc.frame_set(f)
        pts = {k: s3d.kai_point(rig, k) for k in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        if sh is not None:
            pts["tip"] = s3d.claw_tip(sh)
        for k, fn in (extra or {}).items():
            pts[k] = fn()
        row = {}
        for k, p in pts.items():
            v = world_to_camera_view(sc, cam, p)
            row[k] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
        out[f] = row
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def _ret(n, subject, moving=True):
    """Characters on 2s; a moving 3D camera renders on 1s. Locked shots get their slow push-in in 2D (TP13: <=10%)."""
    return dict(frames=n, step=2, ones=(1, n), subject=subject) if moving else dict(frames=n, step=2, subject=subject)


def _drift(n, box, seed=13):
    """Smoke wisps and glowing embers drifting through `box` ((x0, x1), (y0, y1), (z0, z1)) from the north (from the
    stumps beyond the frame), on 2s: S01's top third, under the hook text."""
    rnd = random.Random(seed)
    (x0, x1), (y0, y1), (z0, z1) = box
    m = meadow.smoke_mat()
    ember = look.flat("d16_ember", look.hexc("#ff9a4a"), strength=4.0)
    objs = []
    for i in range(8):
        p = bpy.data.objects.new("puff_drift", None)
        bpy.context.scene.collection.objects.link(p)
        for k in range(5):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=rnd.uniform(0.5, 0.95),
                                                 location=(rnd.uniform(-1.4, 1.4), rnd.uniform(-0.5, 0.5),
                                                           rnd.uniform(-0.2, 0.3)))
            lobe = bpy.context.object
            lobe.data.materials.append(m)
            lobe.parent = p
        x, y, z = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(z0, z1)
        f0 = rnd.randint(-70, n - 40)                              # pre-rolled: some are mid-drift on frame 1
        s = rnd.uniform(0.8, 1.3)
        anim.key(p, "location", f0, (x, y + 4, z), "LINEAR")
        anim.key(p, "location", f0 + 90, (x + rnd.uniform(1, 3), y - 4, z + 1), "LINEAR")
        anim.key(p, "scale", f0 - 1, 0.001, "CONSTANT")
        anim.key(p, "scale", f0, s * 0.5)
        anim.key(p, "scale", f0 + 45, s)
        anim.key(p, "scale", f0 + 90, 0.001)
        objs.append(p)
    for i in range(22):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(0.12, 0.2), location=(0, 0, 0))
        o = bpy.context.object
        o.name = "d16_ember"
        o.data.materials.append(ember)
        x, y, z = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(z0, z1)
        f0 = rnd.randint(-60, n - 10)
        anim.key(o, "location", f0, (x, y + 4, z), "LINEAR")
        anim.key(o, "location", f0 + 70, (x + rnd.uniform(0.5, 2.5), y - 5, z + rnd.uniform(-1, 1.5)), "LINEAR")
        for f in range(f0, f0 + 71, 6):                            # a slow flicker
            anim.key(o, "scale", f, rnd.uniform(0.6, 1.2), "LINEAR")
        objs.append(o)
    anim.on_twos(objs, step=2)
    return objs


# ---------------------------------------------------------------- the shots

def s01():
    """FRAME 0, the hook: from his feet and high above, Kai on his back, the shrimp on his chest leaning back so its big
    locked-on eyes show (on his face), its claw cocked by his cheek. The big hook text sits at the top, over smoke wisps and embers drifting across the top third from
    the stumps beyond the frame (on 2s). Kai whispers
    (lips on 3s), terror face. Locked camera (step 2); the slow push-in is added in 2D."""
    n, rig, sh, _ = _world("S01", lean=S01_LEAN)
    t, d, lens, yaw, up, far = S01_CAM
    fwd = Vector((math.sin(math.radians(yaw)), math.cos(math.radians(yaw)), 0))   # away from the camera
    pair = s3d.kai_point(rig, "eyes").lerp(sh["root"].matrix_world.translation, 0.5)
    aim = pair + UP * up + fwd * far                               # the two of them below the middle, the top free
    cam = diorama.camera("cam_s01", aim, dist=d, tilt=t, yaw=yaw, lens=lens, blur=BLUR)
    _move(cam, n, [(1, t, d, lens), (n, t, d, lens)], lambda f: aim, yaw=yaw)   # locked: the push-in is 2D
    c = pair + fwd * 8                                             # the top third: beyond them, away from the lens
    _drift(n, ((c.x - 6, c.x + 6), (c.y - 9, c.y + 9), (2.0, 6.0)))
    s3d.kai_face(rig, 1, **s3d.TERROR)
    s3d.whisper(rig, 4, 13, s3d.TERROR)                            # "Don't move." 0.12-0.52 s
    s3d.whisper(rig, 26, 51, s3d.TERROR, seed=5)                   # "That claw can boil water." 1.04-2.12 s
    _anchors("S01", cam, rig, sh)
    return _ret(n, [rig["arm"], sh["root"]] + list(rig.get("cap", [])), moving=False)


def s16():
    """When I opened my eyes, it was on my chest. Near top-down (tilt 78) over him, a slow push-in on 1s from the two
    of them toward his face. S16's timing (timing.json l16, f1 = 38.224 s): eyes shut, a flutter on "opened" (f14),
    open and dazed on "eyes" (f24), wide on "it was" (f34), pin-prick terror on "chest" (f46); the shrimp blinks once
    and locks on again."""
    n, rig, sh, _ = _world("S16")
    eyes = s3d.kai_point(rig, "eyes")
    pair = eyes.lerp(sh["root"].matrix_world.translation, 0.5)
    cam = diorama.camera("cam_s16", pair, dist=70.0, tilt=78.0, lens=110.0, blur=BLUR)
    _move(cam, n, [(1, 78.0, 70.0, 110.0), (n, 78.0, 48.0, 120.0)],
          lambda f: pair.lerp(eyes.lerp(pair, 0.35), (f - 1) / (n - 1)))
    k = s3d.kai_face
    k(rig, 1, eye_close=1.0)
    k(rig, 14, eye_close=0.55)
    k(rig, 16, eye_close=1.0)
    k(rig, 20, eye_close=0.3)
    k(rig, 24, eye_close=0.0)
    k(rig, 34, eye_open=0.6)
    k(rig, 46, **s3d.TERROR)
    anim.lids(sh, 60, 1.0)
    s3d.lock_on(sh, eyes, 64)
    _anchors("S16", cam, rig, sh)
    return _ret(n, [rig["arm"], sh["root"]] + list(rig.get("cap", [])))


def s17():
    """Then I saw the drops. Close, locked and looking down (tilt 70) on his chest: the claw reaches down over his
    jacket beside the shrimp, clear of his face; a drop swells at its tip (diorama scale, so it reads from up here),
    lets go at f17, lands on the jacket at f23 ("drops") and leaves a dark wet splat; the next drop swells from f34.
    Same frames as the 3D S17."""
    n, rig, sh, _ = _world("S17", claw="jacket", lean=S01_LEAN)       # leaning back: its eyes show, as in S01
    r = 0.3
    tip = s3d.claw_tip(sh) - Vector((0, 0, r * 0.9))
    land, nrm, mat = _hit(tip)
    drop_m = look.flat("drip", look.hexc("#9fd8ff"))
    d1 = s3d._drop(tip, 1, 17, 23, land + nrm * r * 0.6, r=r, mat=drop_m)
    s3d._drop(tip, 34, n + 20, n + 26, land, r=r, mat=drop_m)
    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.0, fill_type="NGON", location=land + nrm * 0.02)
    spot = bpy.context.object
    for v in spot.data.vertices:                                   # an uneven splat, not a perfect disc
        a = math.atan2(v.co.y, v.co.x)
        v.co *= 1 + 0.16 * math.sin(3 * a + 1.0) + 0.07 * math.sin(7 * a + 2.0)
    spot.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler()
    spot.data.materials.append(look.flat("wet_tunic", look.hexc("#0f5d60")))
    for f, s in ((22, 0.001), (23, 0.22), (25, 0.38), (29, 0.5), (35, 0.56)):
        anim.key(spot, "scale", f, (s, s * 0.8, 1), "LINEAR" if f > 23 else "CONSTANT")
    tgt = tip.lerp(land, 0.5)
    cam = diorama.camera("cam_s17", tgt, dist=50.0, tilt=70.0, lens=120.0, blur=BLUR)
    _move(cam, n, [(1, 70.0, 50.0, 120.0), (n, 70.0, 50.0, 120.0)], lambda f: tgt)   # locked: the push-in is 2D
    s3d.kai_face(rig, 1, **s3d.TERROR)
    _anchors("S17", cam, rig, sh, extra={"drop": lambda: d1.matrix_world.translation.copy()})
    print("S17 drop lands on", mat, flush=True)
    return _ret(n, [sh["root"]], moving=False)


def s18():
    """Its claw only works wet. Close on his face from above (tilt 76, the face turned up to the lens), locked (the push
    and the snap-zoom are 2D):
    wide eyes, then they narrow in two steps as the thought lands on "wet" (f15, f30, f33, as in 3D). The real
    background is swapped for the realisation background in 2D (subject pass)."""
    n, rig, sh, _ = _world("S18")
    tgt = s3d.kai_point(rig, "eyes") - UP * 0.6
    cam = diorama.camera("cam_s18", tgt, dist=50.0, tilt=76.0, lens=120.0, blur=BLUR)
    _move(cam, n, [(1, 76.0, 50.0, 120.0), (n, 76.0, 50.0, 120.0)], lambda f: tgt)   # locked: push + snap in 2D
    k = s3d.kai_face
    k(rig, 1, **s3d.TERROR)
    k(rig, 15, eye_open=0.4, eye_brow_up=0.4)                      # thinking ("claw only")
    k(rig, 30, eye_zitome=0.5, eye_brow_down=0.3)                  # "wet": the thought lands
    k(rig, 33, eye_zitome=0.85, eye_brow_down=0.6)                 # narrowed: he gets it
    _anchors("S18", cam, rig, sh)
    return _ret(n, [rig["arm"], sh["root"]] + list(rig.get("cap", [])), moving=False)


SHOTS = {"S01": s01, "S16": s16, "S17": s17, "S18": s18}
