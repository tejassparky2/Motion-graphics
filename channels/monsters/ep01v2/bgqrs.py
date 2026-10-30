"""Episode 1 v2, the chest scene (S01 frame 0, S16-S21): Kai lies on his back in the sliced meadow ("after" state),
the puff-shrimp sitting on his chest with its claw cocked at his nose. Rules: EP01V2_SHOTS.md and
reports/Pokémon episodes story and animation.md (SG, IM, SU, LC, TP).

Geography (creature units, 1 unit = 20 cm): the crater is at the origin, the stumps fan out behind it (+Y). Kai lies
on his back across the near side of the crater (along X, head to camera-left), so a camera from the -Y side sees him
lying in profile with the sliced trees and smoke beyond (shock in front, its cause behind: SG9). The shrimp (2 units
tall) sits on his chest facing the camera, so its claw (on its right) reaches toward his face.

Each SHOTS[name]() builds the scene and returns dict(frames, step, subject) for render_shot.py; it also writes the
2D anchors (eye and temple positions on screen per frame) to build/monsters/ep01v2/<shot>_anchors.json for the
comic-face pass (channels/monsters/ep01v2/bgqrs_post.py, run outside Blender).
"""
import json
import math
import os

import bpy
from mathutils import Euler, Vector

from channels.monsters.mk import anim, look, meadow, puffshrimp

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ANCHORS = os.path.join(ROOT, "build", "monsters", "ep01v2")
HANDLE = 12                                  # tail handle frames on every shot (the edit trims to the voice)
KAI_SCALE = 5.8                              # Seed-san (1.5 m) -> 1.75 m hero in creature units
FEET = (4.6, -4.6, 0.0)                      # Kai's feet; he lies along -X (head to camera-left)
STANDIN = os.environ.get("KAI_STANDIN") == "1"
HEAD_POSE = (math.radians(-6), math.radians(-60), 0)   # head bone: face turned away from the claw, toward camera
ARM_POSE = {"left": (0, 0, math.radians(-62)), "right": (0, 0, math.radians(62))}


# ---------------------------------------------------------------- the hero, lying down

def _kai_standin():
    """A stand-in body until the add-on-free hero.blend arrives: capsule torso, head, limbs in the hero's colours."""
    skin, hair = look.toon("st_skin", look.hexc("#f6d2b8")), look.toon("st_hair", look.hexc("#4a3328"))
    tunic, trousers = look.toon("st_tunic", look.hexc("#7fae8a")), look.toon("st_trousers", look.hexc("#2e3550"))
    root = bpy.data.objects.new("kai_root", None)
    bpy.context.scene.collection.objects.link(root)

    def part(kind, loc, scale, mat, rot=(0, 0, 0)):
        if kind == "s":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
        else:
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, location=loc)
        o = bpy.context.object
        o.scale, o.rotation_euler = scale, rot
        o.data.materials.append(mat)
        for p in o.data.polygons:
            p.use_smooth = True
        o.parent = root
        look.outline(o, 0.03)
        return o

    # built standing (feet at 0, facing -Y, 8.75 tall) then laid down by the root
    part("s", (0, 0, 7.6), (0.62, 0.7, 0.78), skin)                   # head
    part("s", (0, 0.1, 8.05), (0.68, 0.72, 0.52), hair)
    part("s", (0, 0, 5.35), (1.05, 0.62, 1.5), tunic)                 # torso
    for sx in (-1, 1):
        part("c", (sx * 0.42, 0, 2.0), (0.32, 0.32, 2.0), trousers)
        part("c", (sx * 1.25, 0, 5.2), (0.24, 0.24, 1.5), tunic, (0, sx * 0.12, 0))
        part("s", (sx * 0.24, -0.6, 7.65), (0.13, 0.05, 0.19), look.flat("st_eye", look.hexc("#1b1830")))
    head = [o for o in root.children if o.location.z == 7.6][0]
    return dict(arm=root, head=head, standin=True)


def _kai():
    """Kai lying on his back along -X (head to camera-left), arms loose at his sides, head turned a little toward
    the camera. Returns the hero rig (or the stand-in)."""
    if STANDIN:
        rig = _kai_standin()
    else:
        from channels.monsters.mk import hero
        rig = hero.load((0, 0, 0), scale=KAI_SCALE, outfit="world")
        for side, s in (("left", 1), ("right", -1)):
            b = rig["bone"](f"{side}_upper_arm")
            b.rotation_mode = "XYZ"
            b.rotation_euler = ARM_POSE[side]
        hb = rig["bone"]("head")
        hb.rotation_mode = "XYZ"
        hb.rotation_euler = HEAD_POSE                                    # flinching: face turned to camera
    arm = rig["arm"]
    arm.location = (FEET[0], FEET[1], 0.55)
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (math.radians(-90), 0, math.radians(90))     # on his back, head toward -X
    bpy.context.view_layer.update()
    return rig


def kai_point(rig, name):
    """World position of a hero landmark: 'head', 'eyes', 'nose', 'chest', 'temple'."""
    if rig.get("standin"):
        h = rig["head"].matrix_world.translation
        off = dict(head=(0, 0, 0), eyes=(0, 0.05, 0.62), nose=(0, -0.35, 0.72), chest=(0, -2.25, 0.8),
                   temple=(-0.62, 0.25, 0.4))[name]
        return h + Vector(off)
    arm = rig["arm"]
    pb = rig["bone"]("head")
    m = arm.matrix_world @ pb.matrix
    hd = m.translation
    up = (m.to_3x3() @ Vector((0, 1, 0))).normalized()                  # along the neck to the top of his head
    fwd = (m.to_3x3() @ Vector((0, 0, 1))).normalized()                 # where his face points
    side = up.cross(fwd).normalized()
    s = KAI_SCALE
    return dict(head=hd + up * 0.08 * s, eyes=hd + up * 0.07 * s + fwd * 0.09 * s,
                nose=hd + up * 0.03 * s + fwd * 0.12 * s, chest=hd - up * 0.33 * s + fwd * 0.1 * s,
                temple=hd + up * 0.09 * s + side * 0.075 * s + fwd * 0.03 * s)[name]


# ---------------------------------------------------------------- the shrimp on his chest

def _shrimp(rig, yaw=-160, chest_offset=(0.0, 0.0, 0.0)):
    """The puff-shrimp sitting on Kai's chest. yaw turns it (0 = facing -Y, the camera side); facing back toward his
    face is about 180. Its claw is on its right (-X local)."""
    c = kai_point(rig, "chest") + Vector(chest_offset)
    sh = puffshrimp.build((0, 0, 0))
    sh["root"].location = c
    sh["root"].rotation_euler = (0, 0, math.radians(yaw))
    bpy.context.view_layer.update()
    return sh


def claw_tip(sh):
    """World position of the claw's fixed finger tip (where the drops form)."""
    return sh["shoulder"].matrix_world @ (Vector((-1.25, -0.45, 3.3)) - Vector((-0.82, -0.1, 1.05)))


def cock(sh, f=None):
    """The S01 threat pose: the claw raised over Kai's face, just behind it (so his face stays clear and the pincer
    reads as a silhouette), finger cocked open. Probing showed a tip 2-3 cm from his nose means the claw lies across
    his face from every camera that sees both faces, so it hovers ~30 cm above instead."""
    vals = ((sh["shoulder"], (-0.5, -1.42, 0.0)), (sh["hinge"], (0.5, 0.0, 0.0)))
    for o, v in vals:
        o.rotation_euler = v
        if f is not None:
            anim.key(o, "rotation_euler", f, v, "CONSTANT")


# ---------------------------------------------------------------- the hero's face

def kai_face(rig, f, **keys):
    """Key Kai's face at frame f from raw shape keys on hero.blend's head mesh (e.g. eye_black_small=1, lip_a=0.4),
    zeroing every other face key, so eyes, brows and lips can be layered (hero.face sets one recipe at a time).
    Anime faces snap: CONSTANT keys."""
    if rig.get("standin"):
        return
    from channels.monsters.mk import hero
    kb = bpy.data.objects["head"].data.shape_keys.key_blocks
    names = set(k for r in hero.FACES.values() for k in r) | set(keys)
    for k in names:
        if k in kb:
            kb[k].value = keys.get(k, 0.0)
            kb[k].keyframe_insert("value", frame=f)
    ad = bpy.data.objects["head"].data.shape_keys.animation_data
    for fc in anim.all_fcurves(ad.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - f) < 0.01:
                kp.interpolation = "CONSTANT"


TERROR = dict(eye_open=1.0, eye_small=1.0, eye_no_hilight=1.0, eye_brow_up=1.0)   # pin-prick terror: frame 0


def whisper(rig, f0, f1, base, seed=3):
    """Whispered lips on 3s over a held upper face (`base` keys): small a/o/u shapes and closed beats."""
    import random
    rnd = random.Random(seed)
    f = f0
    while f < f1:
        lip = rnd.choice(("lip_a", "lip_o", "lip_u", None))
        kai_face(rig, f, **base, **({lip: 0.45} if lip else {}))
        f += 3
    kai_face(rig, f1, **base)


# ---------------------------------------------------------------- cameras and shared scene

def _camera(name, loc, target, lens, roll=0.0, dof=None, fstop=0.15):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = name
    d = Vector(target) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.rotation_euler.rotate(Euler((0, 0, roll)))
    cam.data.lens = lens
    cam.data.clip_end = 2000
    if dof is not None:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = dof
        cam.data.dof.aperture_fstop = fstop
    return cam


def _pink_grass(rig, n=46, seed=4):
    """The new world's candy-pink grass tufts around Kai (painted, no outlines)."""
    import random
    from channels.monsters.mk import paintbg
    rnd = random.Random(seed)
    m = paintbg.paint3("pink_grass", look.hexc("#d77fae"), look.hexc("#f3a6cc"), look.hexc("#ffd6ea"), noise=0.2)
    c = kai_point(rig, "chest")
    for _ in range(n):
        x, y = c.x + rnd.uniform(-5.5, 6.5), c.y + rnd.uniform(-3.5, 2.2)
        if abs(y - c.y) < 1.1 and -3.4 < x - c.x < 6.0:          # not through his body
            continue
        r = rnd.uniform(0.18, 0.42)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r, location=(x, y, r * 0.15))
        o = bpy.context.object
        o.scale = (1.0, rnd.uniform(0.7, 1.0), 0.45)
        o.data.materials.append(m)
        for p in o.data.polygons:
            p.use_smooth = True


def _scene(n_frames, shrimp_yaw=-15, shrimp_off=(0.8, -0.2, 0.0), line=None):
    look.world()
    m = meadow.build("after")
    rig = _kai()
    if line is not None and not rig.get("standin"):
        from channels.monsters.mk import hero
        hero.line_width(rig, line)                                 # thinner hero lines in close-ups
    sh = _shrimp(rig, shrimp_yaw, shrimp_off)
    meadow.smoke(m["smoke_sources"], -40, n_frames + 10, every=14, rise=3.5, size=0.9)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n_frames
    return m, rig, sh


def _anchors(shot, cam, points, frames):
    """Screen positions (pixels at 720x1280, origin top-left) of named world points for every frame: the comic-face
    pass reads them. points: {name: fn() -> world Vector}."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, frames + 1):
        sc.frame_set(f)
        row = {}
        for k, fn in points.items():
            p = world_to_camera_view(sc, cam, fn())
            row[k] = (round(p.x * 720, 1), round((1 - p.y) * 1280, 1))
        out[f] = row
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


# ---------------------------------------------------------------- shared shot pieces

def _ecu_camera(rig, name, dist=2.8, lens=60, lift=0.0, dof=True, fstop=2.0):
    """A close-up square to Kai's face, rolled so his face is upright in the frame even though he lies down."""
    from mathutils import Matrix
    m = rig["arm"].matrix_world @ rig["bone"]("head").matrix
    up = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    fwd = (m.to_3x3() @ Vector((0, 0, 1))).normalized()
    e = kai_point(rig, "eyes") + up * lift
    bpy.ops.object.camera_add(location=e + fwd * dist)
    cam = bpy.context.object
    cam.name = name
    z = fwd
    y = (up - z * up.dot(z)).normalized()
    x = y.cross(z)
    cam.rotation_euler = Matrix((x, y, z)).transposed().to_euler()
    cam.data.lens = lens
    cam.data.clip_end = 2000
    if dof:
        foc = bpy.data.objects.new(f"{name}_focus", None)
        bpy.context.scene.collection.objects.link(foc)
        foc.location = e
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = foc
        cam.data.dof.aperture_fstop = fstop
    return cam


def _cut(cams):
    """Camera cuts inside one shot: [(frame, camera), ...] as timeline markers."""
    sc = bpy.context.scene
    for f, cam in cams:
        mk = sc.timeline_markers.new(f"cut_{f}", frame=f)
        mk.camera = cam
    sc.camera = cams[0][1]


def _s01_camera(rig, sh, name="cam_s01"):
    face = kai_point(rig, "nose")
    tgt = face + Vector((1.55, 0.2, 0.85))
    return _camera(name, tgt + Vector((0.4, -6.3, 4.4)), tgt, 28, dof=sh["body"])


def _drop(loc, f_grow, f_fall, f_hit, land, r=0.075, mat=None):
    """A water drop: swells at loc from f_grow, lets go at f_fall, falls (accelerating) to `land` at f_hit and bursts
    flat. Returns the drop object."""
    mat = mat or look.flat("drip", look.hexc("#9fd8ff"))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r, location=loc)
    d = bpy.context.object
    d.name = "drop"
    d.data.materials.append(mat)
    look.outline(d, 0.008)
    anim.key(d, "scale", f_grow - 1, 0.001, "CONSTANT")
    anim.key(d, "scale", f_grow, 0.35, "LINEAR")
    anim.key(d, "scale", f_fall - 1, (1.0, 1.0, 1.25), "LINEAR")
    anim.key(d, "location", f_fall - 1, loc, "LINEAR")
    mid = Vector(loc).lerp(Vector(land), 0.3)
    anim.key(d, "location", (f_fall + f_hit) // 2, mid, "LINEAR")
    anim.key(d, "scale", f_hit - 1, (0.8, 0.8, 1.5), "LINEAR")
    anim.key(d, "location", f_hit, land, "CONSTANT")
    anim.key(d, "scale", f_hit, (1.9, 1.9, 0.25), "CONSTANT")
    anim.key(d, "scale", f_hit + 2, 0.001, "CONSTANT")
    return d


def _surface_below(p):
    """The first surface straight below p (hit point, normal)."""
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, nrm, _, _, _ = bpy.context.scene.ray_cast(dg, p - Vector((0, 0, 0.02)), Vector((0, 0, -1)))
    return (loc, nrm) if hit else (Vector((p.x, p.y, 0.0)), Vector((0, 0, 1)))


def _key_pose(sh, f, shoulder=None, hinge=None, squash=None, interp="BEZIER"):
    if shoulder is not None:
        anim.key(sh["shoulder"], "rotation_euler", f, shoulder, interp)
    if hinge is not None:
        anim.key(sh["hinge"], "rotation_euler", f, (hinge, 0.0, 0.0), interp)
    if squash is not None:
        anim.squash(sh["body"], f, squash, interp)


COCK = (-0.5, -1.42, 0.0)


# ---------------------------------------------------------------- shots

def s01():
    """FRAME 0. Close, from above: Kai on his back, eyes wide; the shrimp on his chest, claw cocked over his face;
    sliced trees with glowing cuts and smoke at the top of the frame. Kai whispers (lips on 3s). Locked; step 1
    because the smoke moves on 1s."""
    n = int(round(2.7 * 24)) + HANDLE
    m, rig, sh = _scene(n)
    cock(sh)
    cam = _s01_camera(rig, sh)
    bpy.context.scene.camera = cam
    anim.lids(sh, 1, 0.0)
    kai_face(rig, 1, **TERROR)
    whisper(rig, 4, int(2.5 * 24), TERROR)
    _anchors("S01", cam, {k: (lambda k=k: kai_point(rig, k)) for k in ("eyes", "temple", "nose")}, n)
    return dict(frames=n, step=1, subject=[sh["root"]], cam=cam, rig=rig, sh=sh)


def s16():
    """When I opened my eyes, it was on my chest. An eye close-up as his eyes open (on 3s), then a cut to S01's exact
    framing (SU9: the frame-0 picture returns), his eyes going to pin-pricks; the shrimp blinks once. Step 3."""
    n = int(round(2.8 * 24)) + HANDLE
    m, rig, sh = _scene(n, line=0.0025)
    cock(sh)
    ecu = _ecu_camera(rig, "cam_s16_eyes", dist=2.8, lens=60)
    wide = _s01_camera(rig, sh, "cam_s16_wide")
    cut = 27
    _cut([(1, ecu), (cut, wide)])
    anim.lids(sh, 1, 0.0)
    kai_face(rig, 1, eye_close=1.0)
    kai_face(rig, 12, eye_close=0.55)                             # a flutter
    kai_face(rig, 15, eye_close=1.0)
    kai_face(rig, 18, eye_close=0.3)
    kai_face(rig, 21, eye_close=0.0)                              # open, still dazed
    kai_face(rig, cut, eye_open=0.6)
    kai_face(rig, cut + 9, **TERROR)                              # he sees it
    for f in (cut + 30,):                                         # the shrimp's slow blank blink (on 3s)
        anim.lids(sh, f, 0.6)
        anim.lids(sh, f + 3, 1.0)
        anim.lids(sh, f + 6, 0.0)
    return dict(frames=n, step=3, subject=[sh["root"]])


def s17():
    """Then I saw the drops. Insert (CH3, the clue a second time): a drop swells at the claw tip, falls and darkens a
    spot on his tunic; the next drop starts to swell. Drops on 2s (step 2)."""
    n = int(round(1.6 * 24)) + HANDLE
    m, rig, sh = _scene(n)
    sh["shoulder"].rotation_euler = (-0.25, -0.95, 0.0)           # claw tip over his collar for the insert
    sh["hinge"].rotation_euler = (0.5, 0, 0)
    bpy.context.view_layer.update()
    tip = claw_tip(sh) + Vector((0.0, -0.05, -0.08))
    land, nrm = _surface_below(tip)
    _drop(tip, 1, 13, 19, land + nrm * 0.02)
    _drop(tip, 30, n + 20, n + 26, land)                          # the next one swelling at the end
    wet = look.flat("wet_tunic", look.hexc("#56806a"))
    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.0, fill_type="NGON", location=land + nrm * 0.012)
    spot = bpy.context.object
    spot.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler()
    spot.data.materials.append(wet)
    for f, r in ((18, 0.001), (19, 0.07), (21, 0.12), (25, 0.16), (31, 0.18)):
        anim.key(spot, "scale", f, (r, r * 0.8, 1), "LINEAR" if f > 19 else "CONSTANT")
    tgt = tip.lerp(land, 0.55)
    cam = _camera("cam_s17", tgt + Vector((0.35, -2.6, 0.55)), tgt, 65)
    foc = bpy.data.objects.new("s17_focus", None)
    bpy.context.scene.collection.objects.link(foc)
    foc.location = tgt
    cam.data.dof.use_dof, cam.data.dof.focus_object, cam.data.dof.aperture_fstop = True, foc, 0.5
    bpy.context.scene.camera = cam
    kai_face(rig, 1, **TERROR)
    return dict(frames=n, step=2, subject=[sh["root"]])


def s18():
    """Its claw only works wet. Extreme close-up of his eyes: wide, then they narrow in two steps (the realisation,
    SG2), with the real background swapped for a realisation background in 2D (IM6/SU16, bgqrs_post via the subject
    pass). Step 3."""
    n = int(round(1.8 * 24)) + HANDLE
    m, rig, sh = _scene(n, line=0.0015)
    cock(sh)
    cam = _ecu_camera(rig, "cam_s18", dist=2.5, lens=60, lift=0.02)
    bpy.context.scene.camera = cam
    kai_face(rig, 1, **TERROR)
    kai_face(rig, 9, eye_open=0.3, eye_brow_up=0.3)              # the thought lands
    kai_face(rig, 12, eye_zitome=0.5, eye_brow_down=0.3)
    kai_face(rig, 15, eye_zitome=0.85, eye_brow_down=0.6)         # narrowed: he gets it
    _anchors("S18", cam, {"eyes": lambda: kai_point(rig, "eyes")}, n)
    return dict(frames=n, step=3, subject=[rig["arm"]])


def s19():
    """So I didn't move. I let the sun dry it. One quiet held shot (SG14): his face set and still, a blink as the
    one face change (SG2), the last drop on the claw tip shrinking away; sun glare, a sweat bead and a <=10% push
    are 2D (bgqrs_post). Step 3."""
    n = int(round(4.1 * 24)) + HANDLE
    m, rig, sh = _scene(n)
    cock(sh)
    tip = claw_tip(sh) + Vector((0.0, -0.06, -0.1))
    d = _drop(tip, 1, n + 40, n + 46, tip - Vector((0, 0, 2)), r=0.09)
    for f, sc_ in ((3, 1.0), (24, 0.85), (48, 0.62), (72, 0.38), (90, 0.18), (99, 0.001)):
        anim.key(d, "scale", f, (sc_, sc_, sc_ * 1.2), "LINEAR")
    face = kai_point(rig, "nose")
    tgt = face.lerp(tip, 0.45) + Vector((0.15, 0, 0.1))
    cam = _camera("cam_s19", tgt + Vector((0.3, -4.2, 2.6)), tgt, 38, dof=None)
    foc = bpy.data.objects.new("s19_focus", None)
    bpy.context.scene.collection.objects.link(foc)
    foc.location = tgt
    cam.data.dof.use_dof, cam.data.dof.focus_object, cam.data.dof.aperture_fstop = True, foc, 0.3
    bpy.context.scene.camera = cam
    anim.lids(sh, 1, 0.0)
    set_face = dict(eye_brow_down=0.45, mouth_short=1.0, eye_open=0.2)
    kai_face(rig, 1, **set_face)
    kai_face(rig, 60, **set_face, eye_close=1.0)                  # one slow blink
    kai_face(rig, 63, **set_face)
    for f in (36,):
        anim.lids(sh, f, 1.0)
        anim.lids(sh, f + 3, 0.0)
    _anchors("S19", cam, {"temple": lambda: kai_point(rig, "temple"), "tip": lambda: tip,
                          "eyes": lambda: kai_point(rig, "eyes")}, n)
    return dict(frames=n, step=3, subject=[sh["root"]])


def s20():
    """It tried anyway. The gag (1-2 s): wind-up, SNAP, and only a tiny puff (2D); the shrimp stares at its claw and
    tilts its head (CH14). Then a cut to Kai's deadpan face, held ~2 s (SU11), a 2D sweat drop. Action on 2s."""
    n = int(round(3.5 * 24)) + HANDLE
    m, rig, sh = _scene(n, line=0.002)
    root = sh["root"].location.copy()
    camA = _camera("cam_s20_shrimp", root + Vector((-1.4, -6.4, 3.0)), root + Vector((-1.15, 0.0, 1.75)), 42,
                   dof=sh["body"], fstop=0.3)
    cut = 41
    camB = _ecu_camera(rig, "cam_s20_kai", dist=4.6, lens=55, lift=-0.25, fstop=1.2)
    _cut([(1, camA), (cut, camB)])
    _key_pose(sh, 1, COCK, 0.5, 0.0)
    _key_pose(sh, 4, COCK, 0.5, 0.0)
    _key_pose(sh, 10, (-0.62, -1.22, 0.0), 0.7, -0.09)            # wind-up: cocked further back, body squashed
    _key_pose(sh, 12, (-0.62, -1.22, 0.0), 0.7, -0.09)
    _key_pose(sh, 14, (-0.38, -1.62, 0.0), -0.25, 0.08, "LINEAR")  # SNAP (nothing happens)
    _key_pose(sh, 18, (-0.42, -1.55, 0.0), -0.25, 0.0)
    body = sh["body"]
    anim.key(body, "rotation_euler", 20, (0, 0, 0))
    anim.key(body, "rotation_euler", 26, (0, 0, math.radians(18)))   # turns to stare at its claw
    anim.key(body, "rotation_euler", 32, (0, math.radians(-14), math.radians(18)))  # ...and tilts its head
    anim.key(body, "rotation_euler", n, (0, math.radians(-16), math.radians(18)))
    anim.lids(sh, 30, 0.3)
    anim.lids(sh, 36, 0.0)
    anim.on_twos([sh["shoulder"], sh["hinge"], body], 2)
    deadpan = dict(eye_zitome=0.75, mouth_short=1.0)
    kai_face(rig, 1, **TERROR)
    kai_face(rig, cut, **deadpan)
    tipf = lambda: claw_tip(sh)  # noqa: E731
    _anchors("S20", camA, {"tip": tipf}, cut - 1)
    with open(os.path.join(ANCHORS, "S20_anchors.json")) as fh:
        a = json.load(fh)
    _anchors("S20b", camB, {"temple": lambda: kai_point(rig, "temple"), "eyes": lambda: kai_point(rig, "eyes")}, n)
    with open(os.path.join(ANCHORS, "S20b_anchors.json")) as fh:
        b = json.load(fh)
    for k, v in b.items():
        a.setdefault(k, {}).update(v)
    with open(os.path.join(ANCHORS, "S20_anchors.json"), "w") as fh:
        json.dump(a, fh)
    bpy.context.scene.camera = camA
    return dict(frames=n, step=2, subject=[sh["root"]])


def s21():
    """Then it stomped back to the puddle. Low angle, Kai lying across the foreground; the shrimp turns its back in a
    huff and stomps off in three hops to the puddle (squash on every landing, 2D dust puffs), then dips its claw.
    Action on 2s (SU12)."""
    n = int(round(2.2 * 24)) + HANDLE
    m, rig, sh = _scene(n)
    r, body = sh["root"], sh["body"]
    p0 = r.location.copy()
    pud = Vector((-1.3, -0.4, 0.0))
    path = [p0, Vector((-0.75, -3.3, 0.0)), Vector((-0.95, -2.2, 0.0)), Vector((-1.12, -1.25, 0.0))]
    face_puddle = math.degrees(math.atan2(-(pud - p0).x, (pud - p0).y)) + 180   # yaw so it faces the puddle
    anim.key(r, "rotation_euler", 1, (0, 0, math.radians(-15)))
    anim.key(r, "rotation_euler", 4, (0, 0, math.radians(-15)))
    anim.key(r, "rotation_euler", 8, (0, 0, math.radians(face_puddle)))    # turns its back on him
    _key_pose(sh, 1, COCK, 0.5)
    _key_pose(sh, 8, (0.0, 0.5, 0.0), 0.0)                                  # claw up at its side
    anim.squash(body, 1, 0.0)
    anim.squash(body, 6, -0.1)                                              # a huffy puff-up... squash
    hops = [(8, 14), (16, 22), (24, 30)]                                    # (take-off, landing)
    anim.key(r, "location", 1, p0)
    anim.key(r, "location", hops[0][0], p0)
    lands = []
    for k, (f0, f1) in enumerate(hops):
        a, b = path[k], path[k + 1]
        anim.squash(body, f0 - 1, -0.12)
        anim.squash(body, f0 + 1, 0.12, "LINEAR")
        top = a.lerp(b, 0.5) + Vector((0, 0, 1.1 if k == 0 else 0.8))
        anim.key(r, "location", (f0 + f1) // 2, top)
        anim.key(r, "location", f1, b, "LINEAR")
        anim.squash(body, f1, -0.2, "LINEAR")                               # STOMP
        anim.squash(body, f1 + 3, 0.0)
        anim.key(r, "location", f1 + 1, b)
        lands.append(f1)
    _key_pose(sh, 36, (0.0, 0.5, 0.0), 0.0)
    _key_pose(sh, 42, (0.85, 0.35, 0.0), 0.3)                               # dips the claw in the water
    anim.on_twos([r, body, sh["shoulder"], sh["hinge"]], 2)
    kai_face(rig, 1, eye_zitome=0.5, mouth_short=1.0)
    # raised (coordinator, 30 Oct): from 1.05 his lying body hid the shrimp's stomps and the puddle after frame ~20;
    # from here Kai stays the foreground at the bottom and the whole hop path and the puddle read above him
    cam_loc = Vector((-0.2, -9.6, 5.2))
    cam = _camera("cam_s21", cam_loc, Vector((-1.0, -1.3, 0.2)), 26, dof=sh["body"], fstop=0.6)
    bpy.context.scene.camera = cam
    _anchors("S21", cam, {"feet": lambda: r.matrix_world.translation.copy()}, n)
    with open(os.path.join(ANCHORS, "S21_lands.json"), "w") as fh:
        json.dump(lands, fh)
    return dict(frames=n, step=2, subject=[sh["root"]])


SHOTS = {"S01": s01, "S16": s16, "S17": s17, "S18": s18, "S19": s19, "S20": s20, "S21": s21}
