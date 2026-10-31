"""D16, the diorama style test's S16 window (channels/monsters/DIORAMA_TEST.md, beat D6, test frames 116-179 + a
12-frame handle): "When I opened my eyes, it was on my chest."

Near top-down over Kai on his back by the pond, the island in its "after" state (the fan's trees gone, glowing stumps
off to the north). One continuous camera move on 1s keeps S16's idea (an eye close-up, then S01's two-shot): it
starts big on his closed eyes, they open on "opened", and on "it was on my chest" the camera pulls up and out to
show the puff-shrimp sitting on his chest, its claw raised over his face. Smoke wisps drift over the clearing and
dust settles through the light. Characters on 2s, the camera and the VFX on 1s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama D16 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.ep01v2 import bgqrs as s16                 # Kai's face keys, the shrimp's lock-on, its claw
from channels.monsters.mk import anim, diorama, hero, look, meadow

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ANCHORS = os.path.join(ROOT, "build", "monsters", "diorama")
N = 76                                # 64 frames (test 116-179) + the 12-frame handle; f1 = episode frame 917
ORIGIN = (-0.909, 0.717)              # the snap's blast origin: the claw at the strike (helper10.py), 13 trees in the fan
HIPS = (1.0, -11.5)                   # where D4 lands him (helper10.py LAND_HIPS): on his back, head toward the pond
HEAD_DIR = 12.0                       # degrees: his head points at (-sin, cos), toward the pond at (0.1, -2.6)
TILT, YAW, BLUR = 78.0, 0.0, 12.0
# the move: (frame, frame height in units at the subject, distance); lens follows from height and distance
MOVE = ((1, 6.0, 70.0), (30, 5.5, 72.0), (54, 9.2, 86.0), (76, 8.6, 88.0))
LEAN = 40.0                           # the shrimp leans back on his chest, so its face tips up toward the camera
SHIFT = (0.11, -0.03)                 # lens shift: the two-shot sits left of the Shorts rail (x < 560) and high
EASE = ((1, 30, "push"), (30, 54, "reveal"), (54, 76, "push"))


def _set():
    """The island after the snap: seed 31, the fan's trees gone, hot-cut stumps where they stood."""
    isl = diorama.island(seed=31)
    fan = set(diorama.blast_spots(isl["spots"], ORIGIN))
    gone = {c.name for i in fan for o in isl["trees"][i] for c in [o] + list(o.children_recursive)}
    for name in gone:
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    stumps = diorama.stumps([isl["spots"][i] for i in sorted(fan)], ORIGIN)
    for name, strength in (("stump_hot", 2.2), ("stump_core", 3.0)):   # the cuts glow (bloom)
        m = bpy.data.materials.get(name)
        em = next((n for n in m.node_tree.nodes if n.type == "EMISSION"), None) if m and m.use_nodes else None
        if em is not None:
            em.inputs["Strength"].default_value = strength
    return isl, stumps


def _kai():
    """Kai on his back, face up, arms out loose (knocked flat), head toward the pond."""
    rig = hero.load((0, 0, 0), scale=s16.KAI_SCALE, outfit="world")
    for side, a in (("left", -48), ("right", 48)):
        b = rig["bone"](f"{side}_upper_arm")
        b.rotation_mode = "XYZ"
        b.rotation_euler = (0, 0, math.radians(a))
    hb = rig["bone"]("head")
    hb.rotation_mode = "XYZ"
    hb.rotation_euler = (math.radians(-4), math.radians(-12), 0)     # face up, rolled a touch toward the camera
    d = Vector((-math.sin(math.radians(HEAD_DIR)), math.cos(math.radians(HEAD_DIR)), 0))
    feet = Vector((HIPS[0], HIPS[1], 0)) - d * 0.5 * 8.7
    arm = rig["arm"]
    arm.location = (feet.x, feet.y, 0.55)
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (math.radians(-90), 0, math.radians(HEAD_DIR))  # head toward +Y, turned to the pond
    bpy.context.view_layer.update()
    return rig


def _shrimp(rig):
    """Low on his chest, facing his face and leaning back so its own face (and locked-on eyes) tips up toward the
    camera; its claw raised BESIDE his face and pointing at it (from above, a claw over his face would hide it)."""
    up = Vector((-math.sin(math.radians(HEAD_DIR)), math.cos(math.radians(HEAD_DIR)), 0))   # toward his head
    east = Vector((up.y, -up.x, 0))                                # the shrimp's right, where its claw is
    sh = s16._shrimp(rig, yaw=180 + HEAD_DIR, chest_offset=tuple(-up * 0.55 + Vector((0, 0, 0.15))))
    sh["root"].rotation_euler = (math.radians(-LEAN), 0, math.radians(180 + HEAD_DIR))
    bpy.context.view_layer.update()
    nose = s16.kai_point(rig, "nose")
    sh["cock"] = s16.raise_claw(sh, nose + east * 1.3 - up * 0.4 + Vector((0, 0, 1.6)), nose)
    s16.cock(sh, 1)
    for f in range(1, N + 1, 24):                                  # breathing, on 2s
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.035)
    return sh


def _face(rig, sh):
    """S16's timing (timing.json, l16; f1 = 38.224 s): eyes shut, a flutter on "opened" (f14), open and dazed on
    "eyes" (f24), wide on "it was" (f34), pin-prick terror on "chest" (f46). The shrimp blinks once, then locks on."""
    k = s16.kai_face
    k(rig, 1, eye_close=1.0)
    k(rig, 14, eye_close=0.55)
    k(rig, 16, eye_close=1.0)
    k(rig, 20, eye_close=0.3)
    k(rig, 24, eye_close=0.0)
    k(rig, 34, eye_open=0.6)
    k(rig, 46, **s16.TERROR)
    eyes = s16.kai_point(rig, "eyes")
    s16.lock_on(sh, eyes, 1)
    anim.lids(sh, 60, 1.0)
    s16.lock_on(sh, eyes, 64)


def _ease(u, kind):
    u = max(0.0, min(1.0, u))
    if kind == "reveal":
        return u * u * (3 - 2 * u)                                 # ease in and out
    return u                                                       # the slow drifts are linear


def _move(f):
    """(frame height, distance) at frame f along MOVE."""
    for (fa, ha, da), (fb, hb, db), (_, _, kind) in zip(MOVE, MOVE[1:], EASE):
        if fa <= f <= fb:
            e = _ease((f - fa) / (fb - fa), kind)
            return ha + (hb - ha) * e, da + (db - da) * e
    return MOVE[-1][1], MOVE[-1][2]


def _camera(rig, sh):
    """The diorama camera at TILT/YAW, re-aimed and re-solved every frame (1s): from his eyes out to the two-shot.
    The lens follows the frame height at the subject; the f-stop is re-solved for the miniature blur each frame."""
    eyes = s16.kai_point(rig, "eyes")
    toes = (sh["root"].matrix_world.translation - eyes).normalized()
    start = eyes + toes * 0.7                                      # his eyes a little above the frame centre
    pair = eyes.lerp(sh["root"].matrix_world.translation, 0.62)    # face high, the shrimp below it, both over y 960
    cam = diorama.camera("cam_d16", start, dist=MOVE[0][2], tilt=TILT, yaw=YAW, lens=36 * MOVE[0][2] / MOVE[0][1],
                         blur=BLUR)
    cam.data.shift_x, cam.data.shift_y = SHIFT
    el, az = math.radians(TILT), math.radians(YAW)
    back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    sc = bpy.context.scene
    for f in range(1, N + 1):
        h, d = _move(f)
        w = _ease((f - MOVE[1][0]) / (MOVE[2][0] - MOVE[1][0]), "reveal")
        tgt = start.lerp(pair, w)
        lens = 36.0 * d / h
        cam.location = tgt + back * d
        cam.data.lens = lens
        cam.data.dof.focus_distance = d
        cam.data.dof.aperture_fstop = diorama.fstop_for(d, lens, BLUR)
        cam.keyframe_insert("location", frame=f)
        cam.data.keyframe_insert("lens", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        ms = sc.world.mist_settings
        ms.start, ms.depth = d * 0.97, d * 0.55
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    sc.camera = cam
    return cam


def _wisps(rig, seed=4):
    """Smoke from the cut stumps drifting low over the clearing toward the camera side (the stumps themselves are 30+
    units north, out of this close frame): painted puffs that slide through, swell and break up. On 1s (VFX)."""
    rnd = random.Random(seed)
    m = meadow.smoke_mat()
    c = s16.kai_point(rig, "chest")
    out = []
    for i in range(7):
        f0 = rnd.randint(-30, N - 20)
        life = rnd.randint(48, 70)
        x0 = c.x + rnd.uniform(-9, 7)
        y0 = c.y + rnd.uniform(4, 12)
        z = rnd.uniform(1.2, 3.2)
        p = bpy.data.objects.new("puff_wisp", None)
        bpy.context.scene.collection.objects.link(p)
        for k in range(5):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=rnd.uniform(0.5, 0.95),
                                                 location=(rnd.uniform(-1.4, 1.4), rnd.uniform(-0.5, 0.5),
                                                           rnd.uniform(-0.2, 0.3)))
            lobe = bpy.context.object
            lobe.data.materials.append(m)
            for pg in lobe.data.polygons:
                pg.use_smooth = True
            lobe.parent = p
        s = rnd.uniform(0.9, 1.4)
        anim.key(p, "location", f0, (x0, y0, z), "LINEAR")
        anim.key(p, "location", f0 + life, (x0 + rnd.uniform(-2, 2), y0 - rnd.uniform(6, 9), z + 0.8), "LINEAR")
        anim.key(p, "scale", f0 - 1, 0.001, "CONSTANT")
        anim.key(p, "scale", f0, s * 0.4)
        anim.key(p, "scale", f0 + life * 0.5, s)
        anim.key(p, "scale", f0 + life, 0.001)
        out.append(p)
    return out


def _dust(rig, n=46, seed=8):
    """Settling dust: small pale motes sinking slowly through the light around him, each shrinking away near the
    ground. On 1s (VFX)."""
    rnd = random.Random(seed)
    m = look.flat("d16_dust", look.hexc("#f3e6c8"))
    c = s16.kai_point(rig, "chest")
    for i in range(n):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(0.035, 0.075),
                                              location=(0, 0, 0))
        o = bpy.context.object
        o.name = "d16_dust"
        o.data.materials.append(m)
        x, y, z = c.x + rnd.uniform(-6, 6), c.y + rnd.uniform(-7, 8), rnd.uniform(1.5, 9.0)
        f0, f1 = rnd.randint(-20, 30), N + rnd.randint(0, 40)
        drift = Vector((rnd.uniform(-0.6, 0.6), rnd.uniform(-1.2, 0.2), -rnd.uniform(1.0, 2.2)))
        anim.key(o, "location", f0, (x, y, z), "LINEAR")
        anim.key(o, "location", f1, Vector((x, y, z)) + drift, "LINEAR")
        anim.key(o, "scale", f0, 1.0, "LINEAR")
        anim.key(o, "scale", f1, 0.2, "LINEAR")


def _anchors(cam, rig):
    """Screen positions (720x1280, top-left origin) of his eyes per frame, for any 2D pass."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, N + 1):
        sc.frame_set(f)
        row = {}
        for k in ("eyes", "eye_l", "eye_r", "nose"):
            p = world_to_camera_view(sc, cam, s16.kai_point(rig, k))
            row[k] = (round(p.x * 720, 1), round((1 - p.y) * 1280, 1))
        out[f] = row
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, "D16_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def d16():
    diorama.setup()
    _set()
    rig = _kai()
    hero.line_width(rig, 0.0025)
    sh = _shrimp(rig)
    _face(rig, sh)
    anim.on_twos([sh["body"]], step=2)
    cam = _camera(rig, sh)
    _wisps(rig)
    _dust(rig)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, N
    _anchors(cam, rig)
    return dict(frames=N, step=2, ones=(1, N), subject=[rig["arm"], sh["root"]] + list(rig.get("cap", [])))


SHOTS = {"D16": d16}
