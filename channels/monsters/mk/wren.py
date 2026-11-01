"""Wren, the village bell-keeper (Episode 2): a girl about Kai's age, built from the same Seed-san base as Kai (the
VRM Public License 1.0 allows changes; the credit line is in assets/monsters/hero/CREDIT.md) so she shares his toon
shading and coloured outlines, but reads as her own person at phone size:
  - a rust-red HOODED SHORT CAPE (hood up, a little pointed tip at the back) with a brass clasp;
  - plum-black hair with TWO BRAIDS falling from under the hood over her shoulders, ochre ties;
  - a cream tunic with ochre trim, an olive under-flap, dark-brown leggings, leather wrist cuffs and brown boots
    (textures: assets/monsters/wren/, made by channels/monsters/wren_recolor.py);
  - a leather SATCHEL on her left hip, strap across her chest;
  - a brass HAND BELL with a wooden handle in her right hand, its cord looped round her wrist; a swinging clapper.
Kai wears teal and a white cap; Wren is warm (rust, cream, brass) with a hood and braids.

    from channels.monsters.mk import wren
    w = wren.load(loc, scale=5.8, rot_z=0.0, line=0.004)     # same scales as hero.load (5.8 in the creature world)
    w["arm"], w["bone"](name)                                # as hero.load: Rigify bones, VRM names via bone()
    w["head"]                                                # HER head mesh (faces must go here, not to "head")
    wren.face(w, "stern", f) / wren.face(w, "neutral", f)   # faces on her own head (hero.face would drive Kai's)
    wren.blink(w, f0, f1)                                    # blinks every 2-4 s
    wren.talk(w, f0, f1, text="Step away from the snapper.")  # mouth flaps on 2s from the text's vowels
    wren.ring(w, f0, f1)                                     # the bell: a wrist shake on 2s, the clapper swinging
    wren.arms_down(P), wren.hold_bell(P, raise_=0..1)        # upper-body poses for an ep01v2.xprl.Pose (P)
    wren.march(w, path, f0, f1)                              # a brisk walk along path (armature space) to a stop

Load Wren and Kai in any order: her objects, materials and head are all named "wren_*", so Kai keeps "head", "hair"
and his materials. Faces snap (CONSTANT), acting on 2s, like Kai.
"""
import math
import os
import random

import bpy
import numpy as np
from mathutils import Matrix, Vector

from . import hero, look, sdf

A = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "monsters", "wren"))
CAPE, CAPE_LIN, CLASP = "#b4462e", "#e9d9b5", "#d9a53e"
HAIR, TIE = "#2a2036", "#d9a53e"
BAG, BAG_DK, BUCKLE = "#8a5634", "#6a3f24", "#d9a53e"
BELL, BELL_DK, HANDLE, CORD = "#d6a23c", "#a8781f", "#7a4e2c", "#b4462e"
BOOT, BOOT_TOE, SOLE = "#6e4630", "#8a5a3a", "#2e2622"


# ------------------------------------------------------------------------------------------------------ materials
def _toon(name, hexcol):
    return look.toon(name, look.hexc(hexcol))


def _line_for(mat):
    name = f"line_{mat.name}"
    lm = bpy.data.materials.get(name) or look.flat(name, look.line_color(look._base_color(mat)))
    lm.use_backface_culling = True
    lm.use_backface_culling_shadow = True
    return lm


def _retex(mat, img_path, base_hex):
    """A copy of a textured hero material with its image swapped (Kai's stays untouched)."""
    m = mat.copy()
    img = bpy.data.images.load(img_path, check_existing=True)
    for n in m.node_tree.nodes:
        if n.type == "TEX_IMAGE" and n.image is not None:
            n.image = img
    m["base"] = look.hexc(base_hex)
    return m


def _swap_slots(o, mapping):
    """Replace base materials (and their outline twins, if the inverted-hull shell uses material_offset)."""
    mats = list(o.data.materials)
    n = len(mats)
    off = o.modifiers["outline"].material_offset if "outline" in o.modifiers else None
    for i, m in enumerate(mats):
        if m is None:
            continue
        new = mapping.get(m.name.split(".")[0])
        if new is None:
            continue
        o.data.materials[i] = new
        if off is not None and i + off < n and (off == 0 or i < off):
            o.data.materials[i + off] = _line_for(new)


# ------------------------------------------------------------------------------------------------------ extras
def _attach(o, arm, bone_name, line):
    look.outline(o, line)
    c = o.constraints.new("CHILD_OF")
    c.target = arm
    c.subtarget = bone_name
    pb = arm.pose.bones[bone_name]
    c.inverse_matrix = (arm.matrix_world @ pb.matrix).inverted()
    return o


def _shell(outer, inner, cut=None):
    """outer minus inner (a hollow shell), minus `cut` if given; bounded by outer."""
    def f(p):
        d = np.maximum(outer(p), -inner(p))
        if cut is not None:
            d = np.maximum(d, -cut(p))
        return d
    f.bounds = outer.bounds
    return f


def _scaled(f, c, s):
    """f evaluated in a space squashed by s about c (an elliptical version of a round primitive)."""
    c, s = np.asarray(c, float), np.asarray(s, float)

    def g(p):
        return f(c + (p - c) / s) * float(np.min(s))
    lo, hi = f.bounds
    g.bounds = (c + (lo - c) * s, c + (hi - c) * s)
    return g


def _halfspace(axis, value, keep_above):
    def f(p):
        return (value - p[..., axis]) if keep_above else (p[..., axis] - value)
    return f


def _cap_by(f, cutter):
    def g(p):
        return np.maximum(f(p), cutter(p))
    g.bounds = f.bounds
    return g


def _hood_and_cape(J, line):
    """The hood (around the head, open at the face, a small point at the back) and the short cape (shoulders to
    upper chest), as two meshes: the hood follows the head, the cape the chest."""
    hc = J["head_c"]
    cape_m, lin_m, clasp_m = _toon("wren_cape", CAPE), _toon("wren_cape_lining", CAPE_LIN), _toon("wren_clasp", CLASP)
    outer = sdf.E(hc + Vector((0, 0.022, 0.012)), (0.133, 0.148, 0.147))
    inner = sdf.E(hc + Vector((0, 0.022, 0.01)), (0.121, 0.136, 0.135))
    face = sdf.E(hc + Vector((0, -0.14, -0.03)), (0.094, 0.1, 0.116))
    hood = _shell(outer, inner, face)

    def lining(p):                                              # the hood's edge round the face, in cream
        return np.maximum(hood(p), face(p) - 0.016)
    lining.bounds = hood.bounds
    tip = sdf.C(hc + Vector((0, 0.12, 0.09)), hc + Vector((0, 0.21, -0.01)), 0.045, 0.011)
    o_hood = sdf.build("wren_hood", [(lining, lin_m.name, None), (hood, cape_m.name, 0.0), (tip, cape_m.name, 0.03)],
                       k=0.02, res=0.006, pad=0.03, smooth_iter=6)
    # the short cape: a rounded dome over the shoulders, hollow, flaring a little to a hem below the shoulders
    nk = J["neck"]
    dc = Vector((0, nk.y - 0.004, nk.z - 0.12))
    outer_c = sdf.E(dc, (0.212, 0.145, 0.14))
    inner_c = sdf.E(dc + Vector((0, 0, -0.012)), (0.198, 0.131, 0.13))
    hem = J["chest"].z + 0.035

    def shell(p):
        d = np.maximum(outer_c(p), -inner_c(p))
        return np.maximum(d, hem - p[..., 2])
    shell.bounds = outer_c.bounds
    collar = sdf.C(Vector((0, nk.y, nk.z + 0.03)), Vector((0, nk.y, nk.z - 0.02)), 0.062, 0.07)

    def collar_shell(p):
        return np.maximum(collar(p), -sdf.C(Vector((0, nk.y, nk.z + 0.05)),
                                             Vector((0, nk.y, nk.z - 0.04)), 0.052, 0.06)(p))
    collar_shell.bounds = collar.bounds
    clasp = sdf.E(Vector((0, nk.y - 0.07, nk.z - 0.02)), (0.02, 0.011, 0.02))
    o_cape = sdf.build("wren_cape", [(shell, cape_m.name, None), (collar_shell, cape_m.name, 0.02),
                                      (clasp, clasp_m.name, 0.0)],
                       k=0.01, res=0.006, pad=0.03, smooth_iter=6)
    return o_hood, o_cape


def _braids(J, line):
    hair_m, tie_m = _toon("wren_braid", HAIR), _toon("wren_tie", TIE)
    hc = J["head_c"]
    parts = []
    for s in (1, -1):
        a = hc + Vector((s * 0.088, -0.05, -0.075))
        pts = [a + Vector((s * (0.01 + 0.012 * i), -0.02 - 0.012 * i, -0.045 * i)) for i in range(7)]
        for i, p in enumerate(pts):
            r = 0.026 - 0.0018 * i
            parts.append((sdf.E(p, (r, r * 0.9, r * 1.25)), hair_m.name, 0.012))
        end = pts[-1]
        parts.append((sdf.E(end + Vector((0, 0, -0.012)), (0.02, 0.018, 0.012)), tie_m.name, 0.004))
        parts.append((sdf.C(end + Vector((0, 0, -0.02)), end + Vector((s * 0.006, -0.004, -0.065)), 0.018, 0.006),
                      hair_m.name, 0.006))
    return sdf.build("wren_braids", parts, k=0.012, res=0.005, pad=0.03, smooth_iter=5)


def _satchel(J, line, surf):
    bag_m, dk_m, buck_m = _toon("wren_satchel", BAG), _toon("wren_satchel_dk", BAG_DK), _toon("wren_buckle", BUCKLE)
    hip = J["hips"]
    bag_c = Vector((0.17, surf(0.17, hip.z - 0.02) - 0.02, hip.z - 0.05))
    bag = sdf.E(bag_c, (0.075, 0.035, 0.065))
    flap = sdf.E(bag_c + Vector((0, -0.018, 0.022)), (0.077, 0.022, 0.048))
    buckle = sdf.E(bag_c + Vector((0, -0.04, -0.005)), (0.014, 0.006, 0.012))
    o_bag = sdf.build("wren_satchel", [(bag, bag_m.name, None), (flap, dk_m.name, 0.004),
                                        (buckle, buck_m.name, 0.0)], k=0.01, res=0.005, pad=0.03, smooth_iter=5)
    # the strap: from behind the right shoulder, across the chest (over the tunic, under the cape hem), to the bag
    zs = np.linspace(J["chest"].z + 0.04, hip.z + 0.01, 9)
    xs = np.linspace(-0.12, 0.15, 9)
    parts = []
    prev = None
    for x, z in zip(xs, zs):
        p = Vector((x, surf(x, z) - 0.008, z))
        if prev is not None:
            parts.append((sdf.C(prev, p, 0.011, 0.011), dk_m.name, 0.004))
        prev = p
    o_strap = sdf.build("wren_strap", parts, k=0.004, res=0.004, pad=0.02, smooth_iter=3)
    return o_bag, o_strap


def _bell(line):
    """The hand bell in its own space: the grip at the origin, the handle up +Z, the bell hanging below, its mouth
    at -Z; plus the cord loop round the wrist (+Z side) and a separate clapper."""
    bell_m, dk_m, h_m, cord_m = _toon("wren_bell", BELL), _toon("wren_bell_dk", BELL_DK), _toon("wren_handle", HANDLE), \
        _toon("wren_cord", CORD)
    body_o = sdf.C(Vector((0, 0, -0.035)), Vector((0, 0, -0.1)), 0.026, 0.052)
    body_i = sdf.C(Vector((0, 0, -0.045)), Vector((0, 0, -0.125)), 0.018, 0.045)
    body = _cap_by(_shell(body_o, body_i), lambda p: -0.115 - p[..., 2])
    lip = _cap_by(sdf.C(Vector((0, 0, -0.105)), Vector((0, 0, -0.112)), 0.06, 0.061),
                  lambda p: np.maximum(-0.115 - p[..., 2], -(np.hypot(p[..., 0], p[..., 1]) - 0.045)))
    knob = sdf.E(Vector((0, 0, -0.03)), (0.02, 0.02, 0.014))
    handle = sdf.C(Vector((0, 0, -0.03)), Vector((0, 0, 0.055)), 0.012, 0.015)
    cap = sdf.E(Vector((0, 0, 0.06)), (0.018, 0.018, 0.012))
    parts = [(body, bell_m.name, None), (lip, dk_m.name, 0.0), (knob, dk_m.name, 0.004), (handle, h_m.name, 0.004),
             (cap, h_m.name, 0.004)]
    for i in range(10):                                         # the cord: from the cap to a loop round the wrist
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10
        c = Vector((0, 0.0, 0.12))
        p0 = c + Vector((0.035 * math.cos(a0), 0.035 * math.sin(a0), 0))
        p1 = c + Vector((0.035 * math.cos(a1), 0.035 * math.sin(a1), 0))
        parts.append((sdf.C(p0, p1, 0.004, 0.004), cord_m.name, 0.002))
    parts.append((sdf.C(Vector((0, 0, 0.066)), Vector((0.03, 0.0, 0.12)), 0.004, 0.004), cord_m.name, 0.002))
    o = sdf.build("wren_bell", parts, k=0.006, res=0.0035, pad=0.02, smooth_iter=4)
    cl = sdf.build("wren_clapper", [(sdf.C(Vector((0, 0, -0.04)), Vector((0, 0, -0.1)), 0.004, 0.004), dk_m.name, None),
                                    (sdf.E(Vector((0, 0, -0.103)), (0.012, 0.012, 0.012)), dk_m.name, 0.004)],
                   k=0.004, res=0.003, pad=0.02, smooth_iter=3)
    return o, cl


def _boots(rig):
    """Kai's sneaker meshes on her rig, recoloured as brown boots."""
    boot, toe, sole = _toon("wren_boot", BOOT), _toon("wren_boot_toe", BOOT_TOE), _toon("wren_sole", SOLE)
    for o in rig["objects"]:
        if o.type == "MESH" and "shoe" in o.name:
            _swap_slots(o, {"shoe_white": boot, "shoe_accent": toe, "shoe_sole": sole})


# ------------------------------------------------------------------------------------------------------ load
def load(loc=(0, 0, 0), scale=1.0, rot_z=0.0, line=0.004):
    """Wren, posed in the base T-pose at loc/scale/rot_z (turn her with rig["arm"].rotation_euler.z afterwards,
    like Kai). Returns the hero-style rig dict plus head, hood, cape, braids, satchel, strap, bell, clapper."""
    rig = hero.load((0, 0, 0), scale=1.0, line=line)
    arm = rig["arm"]
    col = arm.users_collection[0]
    col.name = "wren"
    objs = list(col.objects)
    by_base = {}
    for o in objs:                                              # her own names: Kai keeps "head", "hair", ...
        base = (o.name[5:] if o.name.startswith("hero_") else o.name).split(".")[0]
        by_base[base] = o
        o.name = "wren_" + base
    for o in objs:
        if "cap" in o.name:
            o.hide_render = o.hide_viewport = True
    rig["objects"] = objs
    rig["cap"] = []
    head, hair, wear = by_base["head"], by_base["hair"], by_base["wear"]
    rig["head"] = head
    # materials: her own copies; the tunic and hair textures recoloured
    tunic = _retex(bpy.data.materials[wear.data.materials[[m.name.split(".")[0] if m else "" for m in
                                                           wear.data.materials].index("huku_bake")].name],
                   os.path.join(A, "wear_wren.png"), "#d8c7a2")
    tunic.name = "wren_huku_bake"
    hair_src = next(m for m in hair.data.materials if m and m.name.split(".")[0] == "hair")
    hairm = _retex(hair_src, os.path.join(A, "hair_wren.png"), HAIR)
    hairm.name = "wren_hair"
    for o in (wear, hair, head):
        _swap_slots(o, {"huku_bake": tunic, "hair": hairm})
    _boots(rig)
    # rest-pose joints (model metres; she faces -Y)
    bpy.context.view_layer.update()
    pb = arm.pose.bones
    hb = pb["head 1"]
    dg0 = bpy.context.evaluated_depsgraph_get()
    he = head.evaluated_get(dg0)
    hv = np.array([v.co[:] for v in he.to_mesh().vertices])
    he.to_mesh_clear()
    lo_, hi_ = hv.min(0), hv.max(0)                           # the head mesh's box (skull + face), rest pose
    J = dict(head_c=Vector((0.0, (lo_[1] + hi_[1]) / 2, (lo_[2] + hi_[2]) / 2)), neck=pb["neck"].head.copy(),
             chest=pb["chest"].head.copy(), hips=pb["hips"].head.copy())
    del hb
    # the front surface of the body (for the strap), by ray casts on the evaluated wear mesh
    from mathutils.bvhtree import BVHTree
    dg = bpy.context.evaluated_depsgraph_get()
    bvh = BVHTree.FromObject(wear, dg)

    def surf(x, z):
        hit = bvh.ray_cast(Vector((x, -1.0, z)), Vector((0, 1, 0)))
        return hit[0].y if hit[0] is not None else -0.09
    o_hood, o_cape = _hood_and_cape(J, line)
    o_braids = _braids(J, line)
    o_bag, o_strap = _satchel(J, line, surf)
    _attach(o_hood, arm, "head 1", line)
    _attach(o_braids, arm, "head 1", line)
    _attach(o_cape, arm, "chest", line)
    _attach(o_strap, arm, "chest", line)
    _attach(o_bag, arm, "hips", line)
    # the bell in the right fist: its +Z (handle up) along the hand bone's -Y, so with the arm down it hangs upright
    o_bell, o_clap = _bell(line)
    hr = pb["hand.R"]
    Mh = hr.matrix.copy()
    y = (Mh.to_3x3() @ Vector((0, 1, 0))).normalized()
    zl = -y
    xl = (Mh.to_3x3() @ Vector((0, 0, 1))).normalized()
    yl = zl.cross(xl).normalized()
    xl = yl.cross(zl).normalized()
    R = Matrix((xl, yl, zl)).transposed().to_4x4()
    grip = Mh.translation + y * 0.075 + (Mh.to_3x3() @ Vector((0, 0, 1))).normalized() * 0.0
    o_bell.matrix_world = Matrix.Translation(grip) @ R
    o_clap.data.transform(Matrix.Translation((0, 0, 0.038)))      # pivot at the bell's crown, not the grip
    o_clap.location = (0, 0, -0.038)
    o_clap.parent = o_bell
    look.outline(o_clap, line * 0.6)
    _attach(o_bell, arm, "hand.R", line)
    for o in (o_hood, o_cape, o_braids, o_bag, o_strap, o_bell, o_clap):
        for c in o.users_collection:
            c.objects.unlink(o)
        col.objects.link(o)
    rig.update(hood=o_hood, cape=o_cape, braids=o_braids, satchel=o_bag, strap=o_strap, bell=o_bell, clapper=o_clap)
    arm.rotation_mode = "XYZ"
    arm.location = loc
    arm.scale = (scale, scale, scale)
    arm.rotation_euler = (0, 0, rot_z)
    bpy.context.view_layer.update()
    return rig


# ------------------------------------------------------------------------------------------------------ face
FACES = dict(hero.FACES)
FACES.update({
    "stern": {"face_angry": 0.85, "eye_zitome": 0.45, "eye_brow_down": 1.0},
    "stern_open": {"face_angry": 0.85, "eye_zitome": 0.4, "eye_brow_down": 1.0, "lip_a": 0.5},
    "softer": {"face_relax": 0.35, "eye_brow_up": 0.2},
})
_LIPS = ("lip_a", "lip_o", "lip_u", "lip_i", "lip_e", "mouth_short")


def _key(head, k, f, v):
    kb = head.data.shape_keys.key_blocks
    if k not in kb:
        return
    kb[k].value = v
    kb[k].keyframe_insert("value", frame=f)
    from . import anim
    ad = head.data.shape_keys.animation_data
    for fc in anim.all_fcurves(ad.action):
        if fc.data_path == f'key_blocks["{k}"].value':
            for kp in fc.keyframe_points:
                if abs(kp.co.x - f) < 0.01:
                    kp.interpolation = "CONSTANT"


def face(rig, name, f, value=1.0):
    """Snap HER face to FACES[name] at frame f (every expression key reset; blinks and lips layered by their own
    functions afterwards)."""
    head = rig["head"]
    recipe = FACES.get(name, {name: 1})
    keys = set()
    for r in FACES.values():
        keys.update(r)
    keys -= {"eye_close"}
    for k in keys:
        _key(head, k, f, recipe.get(k, 0) * value)


def blink(rig, f0, f1, every=(48, 96), seed=4, at=()):
    rnd = random.Random(seed)
    fs = list(at)
    f = f0 + rnd.randint(12, every[0])
    while f < f1 - 3:
        fs.append(f)
        f += rnd.randint(*every)
    head = rig["head"]
    _key(head, "eye_close", f0, 0.0)
    for f in sorted(fs):
        _key(head, "eye_close", f, 1.0)
        _key(head, "eye_close", f + 2, 0.0)


VOWEL = {"a": "lip_a", "e": "lip_e", "i": "lip_i", "o": "lip_o", "u": "lip_u", "y": "lip_i"}


def talk(rig, f0, f1, text="", amount=0.85, seed=6):
    """Mouth flaps from f0 to f1 on 2s: one open shape per vowel group of `text`, spread over the span, closed at
    word gaps and full stops; shut at f1."""
    head = rig["head"]
    shapes = []
    for w in text.lower().replace(".", " . ").split():
        if w == ".":
            shapes += [None, None]
            continue
        groups, prev = [], False
        for ch in w:
            v = ch in VOWEL
            if v and not prev:
                groups.append(VOWEL[ch])
            prev = v
        shapes += groups or ["lip_u"]
        shapes.append(None)
    if not shapes:
        shapes = ["lip_a", None]
    n = max(1, (f1 - f0) // 2)
    for i in range(n):
        f = f0 + 2 * i
        s = shapes[min(len(shapes) - 1, int(i * len(shapes) / n))]
        for k in _LIPS:
            if s is None:
                _key(head, k, f, 1.0 if k == "mouth_short" else 0.0)
            else:
                _key(head, k, f, (amount if k == s else 0.0))
    for k in _LIPS:
        _key(head, k, f1, 1.0 if k == "mouth_short" else 0.0)


def ring(rig, f0, f1, swing=26.0, beat=4):
    """The bell rings from f0 to f1: the clapper swings side to side on 2s (beat = frames per swing). Pair it with a
    wrist shake in the pose (hold_bell(P, raise_, shake=...)). Returns the strike frames (for the ring lines and
    the sound)."""
    cl = rig["clapper"]
    cl.rotation_mode = "XYZ"
    strikes = []
    cl.rotation_euler = (0, 0, 0)
    cl.keyframe_insert("rotation_euler", frame=f0)
    s = 1
    for f in range(f0 + beat // 2, f1, beat):
        cl.rotation_euler = (0, math.radians(swing * s), 0)
        cl.keyframe_insert("rotation_euler", frame=f)
        strikes.append(f)
        s = -s
    cl.rotation_euler = (0, 0, 0)
    cl.keyframe_insert("rotation_euler", frame=f1)
    return strikes


# ------------------------------------------------------------------------------------------------------ poses
def arms_down(P, spread=10):
    """Both arms down at her sides (the ep01v2 Pose helper, in armature space)."""
    for sx, s in (("L", 1), ("R", -1)):
        P.aim(f"upper_arm.{sx}", (s * math.sin(math.radians(spread)), 0.04, -1))
        P.aim(f"forearm.{sx}", (s * 0.06, -0.12, -1))


def hold_bell(P, raise_=0.0, shake=0.0):
    """The bell hand: down at her side (raise_ 0) up to held out in front at chest height (raise_ 1), with a wrist
    shake (degrees) for the ring. The left arm stays down."""
    P.aim("upper_arm.L", (math.sin(math.radians(10)), 0.04, -1))
    P.aim("forearm.L", (0.06, -0.12, -1))
    r = max(0.0, min(1.0, raise_))
    P.aim("upper_arm.R", (-0.17 + 0.05 * r, 0.04 - 0.55 * r, -1 + 0.55 * r))
    P.aim("forearm.R", (-0.06 + 0.02 * r, -0.12 - 0.95 * r, -1 + 1.05 * r))
    P.aim("hand.R", (-0.04, -0.15 - 0.2 * r, -1))                 # the hand stays pointing down: the bell hangs upright
    if shake:
        P.rot("hand.R", (0, shake, 0))


def march(rig, P, path, f0, f1, step_len=0.30, upper=None, every=2):
    """A brisk, upright walk along `path` (armature space) from f0 to f1, ending planted (a stop). Returns the
    planted feet for a follow-up pose."""
    from channels.monsters.ep01v2 import xprl as x3

    def up(P_, t):
        if upper:
            upper(P_, t)
        else:
            arms_down(P_)
        P_.rot("chest", (-3, 0, 0))                              # chin up, shoulders back: purposeful
    return x3._walk(P, rig, path, f0, f1, step_len, "R", crouch=(0.0, 0.0), upper=up, every=every)


def grip(rig, f, side="R", curl=1.0):
    """Close the fingers round the bell handle (side R) or into a loose fist, keyed at f (fingers aren't part of the
    Pose helper's BODY keys, so this layers on top of any pose)."""
    pb = rig["arm"].pose.bones
    for fn in ("index", "middle", "ring", "pinky"):
        for j, ang in ((1, 62), (2, 70), (3, 45)):
            name = f"f_{fn}.0{j}.{side}"
            if name not in pb:
                continue
            b = pb[name]
            b.rotation_mode = "QUATERNION"
            b.rotation_quaternion = Matrix.Rotation(math.radians(ang * curl), 4, "X").to_quaternion()
            b.keyframe_insert("rotation_quaternion", frame=f, group=name)


def talk_words(rig, words, t0, fps=24, amount=0.85, first=1):
    """Lip-sync from word timings (ep02/timing.json "words": [{w, start, end}], seconds): each word opens on its
    vowel shapes between its start and end (on 2s), the mouth shuts in the gaps. t0 = the shot's start in seconds
    (frame `first`)."""
    head = rig["head"]

    def fr(s):
        return int(round((s - t0) * fps)) + first
    shut = {k: (1.0 if k == "mouth_short" else 0.0) for k in _LIPS}
    for k, v in shut.items():
        _key(head, k, first, v)
    for w in words:
        a, b = fr(w["start"]), max(fr(w["start"]) + 2, fr(w["end"]))
        groups, prev = [], False
        for ch in w["w"].lower():
            v = ch in VOWEL
            if v and not prev:
                groups.append(VOWEL[ch])
            prev = v
        groups = groups or ["lip_u"]
        span = max(2, b - a)
        for i, g in enumerate(groups):
            f = a + int(i * span / len(groups))
            for k in _LIPS:
                _key(head, k, f, amount if k == g else 0.0)
        for k, v in shut.items():
            _key(head, k, b, v)


def contact_shadows(rig, size=(0.55, 0.85)):
    """Soft blob shadows under her boots (look.blob_shadow), following each foot over the ground (x, y only), so she
    reads as standing ON the grass in diorama light. Sizes are in creature units at scale 5.8 (scaled with her)."""
    arm = rig["arm"]
    k = arm.scale.x / 5.8
    out = []
    for side in ("L", "R"):
        sh = look.blob_shadow(f"wren_foot_shadow.{side}", (0, 0, 0.03), (size[0] * k, size[1] * k))
        c = sh.constraints.new("COPY_LOCATION")
        c.target = arm
        c.subtarget = f"foot.{side}"
        c.use_z = False
        out.append(sh)
    body = look.blob_shadow("wren_body_shadow", (0, 0, 0.025), (1.2 * k, 0.9 * k))
    c = body.constraints.new("COPY_LOCATION")
    c.target = arm
    c.subtarget = "hips"
    c.use_z = False
    out.append(body)
    rig["shadows"] = out
    return out
