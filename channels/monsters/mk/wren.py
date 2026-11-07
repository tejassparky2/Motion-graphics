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
    # Ep 3: the cape's front edge, gathered in her left hand when she pulls the cape over her face (cape_up()). In the
    # rest T-pose it hangs under the left forearm, so with the forearm across her face it drapes face to chest.
    cape_m = bpy.data.materials["wren_cape"]
    lin_m = bpy.data.materials["wren_cape_lining"]
    fa = pb["forearm.L"].head
    fc = Vector((fa.x + 0.07, fa.y - 0.03, fa.z - 0.1))
    drape_o = sdf.E(fc, (0.16, 0.03, 0.13))
    drape_i = sdf.E(fc + Vector((0, 0.012, 0)), (0.15, 0.026, 0.12))

    def drape(p):
        return np.maximum(np.maximum(drape_o(p), -drape_i(p)), p[..., 2] - (fa.z + 0.01))
    drape.bounds = drape_o.bounds
    hem = sdf.C(Vector((fc.x - 0.15, fc.y + 0.004, fc.z - 0.09)), Vector((fc.x + 0.15, fc.y + 0.004, fc.z - 0.09)),
                0.012, 0.012)
    o_drape = sdf.build("wren_cape_drape", [(drape, cape_m.name, None), (hem, lin_m.name, 0.006)],
                        k=0.01, res=0.006, pad=0.03, smooth_iter=5)
    _attach(o_drape, arm, "forearm.L", line)
    o_drape.hide_render = o_drape.hide_viewport = True
    for c in o_drape.users_collection:
        c.objects.unlink(o_drape)
    col.objects.link(o_drape)
    rig.update(hood=o_hood, cape=o_cape, braids=o_braids, satchel=o_bag, strap=o_strap, bell=o_bell, clapper=o_clap,
               drape=o_drape)
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
    # Ep 3
    "shocked": {"face_surprise": 1.0, "eye_black_small": 0.55, "eye_brow_up": 0.9, "lip_o": 0.55},
    "shout": {"face_angry": 0.7, "eye_brow_down": 1.0, "lip_a": 1.0, "mouth_wide": 0.35},
    "softening": {"face_surprise": 0.65, "face_sad": 0.4, "eye_brow_up": 0.6},   # the stern face cracks, eyes wide
    "worried": {"face_sad": 1.0, "lip_down": 0.6, "eye_no_hilight": 0.6, "face_surprise": 0.15, "eye_brow_up": 0.6},
    "whisper": {"face_sad": 0.25, "eye_zitome": 0.3, "eye_brow_up": 0.35, "lip_u": 0.45},
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


# ------------------------------------------------------------------------------------------------------ Ep 3 poses
# All in armature space at scale 1 (she faces -Y, her left is +X; the hips sit at z ~0.80 standing). Each pose
# function poses a reset ep01v2.xprl.Pose (P) and leaves the keying to the caller (P.key(f)); the finger and cape
# helpers key on the rig directly. Combine them: e.g. kneel(P) then whisper(P, 1) then P.key(f).
_UPPER = 0.255                                                   # upper_arm head -> forearm head
_LOWER = 0.22                                                    # forearm head -> hand head (forearm + twist)


def _ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def head_c(P):
    """Her head centre (armature space) in the current pose."""
    bpy.context.view_layer.update()
    M = P.pb["head 1"].matrix
    return M.translation + M.to_3x3() @ Vector((0, 0.07, -0.01))


def reach(P, side, target, pole=(0, -1, 0), hand=None):
    """Two-bone arm IK: put the wrist of arm `side` at `target` (armature space), the elbow bending towards `pole`
    (a direction). `hand`: the hand's direction (defaults to straight on from the forearm)."""
    bpy.context.view_layer.update()
    H = P.pb[f"upper_arm.{side}"].matrix.translation.copy()
    T = Vector(target)
    d = min((T - H).length, (_UPPER + _LOWER) * 0.999)
    u = (T - H).normalized()
    pv = Vector(pole).normalized()
    w = pv - pv.dot(u) * u
    w = w.normalized() if w.length > 1e-4 else Vector((0, 0, -1))
    cos_a = max(-1.0, min(1.0, (_UPPER ** 2 + d ** 2 - _LOWER ** 2) / (2 * _UPPER * d)))
    K = H + _UPPER * (cos_a * u + math.sqrt(1 - cos_a ** 2) * w)
    P.aim(f"upper_arm.{side}", K - H)
    P.aim(f"forearm.{side}", H + u * d - K)
    P.aim(f"hand.{side}", hand if hand is not None else (H + u * d - K))


def cape_up(rig, f, on=True):
    """Show (or hide) the cape edge gathered in her left hand, keyed at f (a snap, like a drawing change)."""
    o = rig["drape"]
    o.hide_render = o.hide_viewport = not on
    o.keyframe_insert("hide_render", frame=f)
    o.keyframe_insert("hide_viewport", frame=f)


def shield(P, t=1.0):
    """S07: she pulls the cape over her face: left forearm across her face (pair with cape_up), head ducked and
    turned to her right, shoulders hunched; the bell hand stays down. t 0..1 blends from standing."""
    e = _ease(t)
    P.aim("upper_arm.R", (-0.17, 0.06, -1))
    P.aim("forearm.R", (-0.06, -0.12, -1))
    P.aim("hand.R", (-0.04, -0.15, -1))
    P.rot("chest", (8 * e, 0, -10 * e))
    P.rot("neck", (10 * e, 0, -8 * e))
    P.rot("head 1", (14 * e, 4 * e, -16 * e))
    hc = head_c(P)
    rest = Vector((0.2, -0.05, 0.9))
    tgt = rest.lerp(hc + Vector((-0.07, -0.13, -0.03)), e)
    reach(P, "L", tgt, pole=(1, 0.2, -0.6), hand=(-1, -0.15, 0.25))


def ring_hard(P, shake=0, lift=1.0):
    """S08: both hands round the bell handle, held up in front of her face, shaken hard: shake = -1 / 0 / +1 (the
    swing phase; alternate it on 2s), lift 0..1 from chest to above-head height. Pair with ring(rig, ..., swing=40,
    beat=4) for the clapper, face 'shout'."""
    P.rot("chest", (-6, 5 * shake, 0))
    P.rot("head 1", (-6, 0, 0))
    z = 1.1 + 0.12 * lift + 0.035 * abs(shake)
    c = Vector((-0.22 + 0.02 * shake, -0.26, z))                 # up at her right shoulder: her face stays clear
    reach(P, "R", c + Vector((-0.04 + 0.05 * shake, 0, 0.01)), pole=(-1, 0.3, -0.6), hand=(0.15 * shake, -0.15, -1))
    reach(P, "L", c + Vector((0.035 + 0.05 * shake, 0.0, 0.055)), pole=(1, 0.3, -0.6), hand=(-0.9, -0.2, -0.2))


def lower_bell(P, t):
    """S16: the bell comes down slowly from held up (t 0) to hanging at her side (t 1), her shoulders easing and
    head dropping a little."""
    e = _ease(t)
    hold_bell(P, 1.0 - e)
    P.rot("chest", (5 * e, 0, 0))
    P.rot("head 1", (6 * e, 0, 0))


def kneel(P, front="L", depth=1.0, ankle_h=None):
    """S17/S18: down on one knee (the `front` foot planted ahead, the other knee on the ground, toes behind), torso
    upright. depth 0..1 blends from standing (crouch on the way down). Feet in armature space at ground z 0."""
    e = _ease(depth)
    ah = P.ankle_h if ankle_h is None else ankle_h
    back = "R" if front == "L" else "L"
    sx = {"L": 1, "R": -1}
    P.hips((0, 0.04 * e, -0.39 * e))
    P.leg(front, (sx[front] * 0.11, -0.26 * e, ah))
    P.leg(back, (sx[back] * 0.1, 0.30 * e, ah + (0.04 - ah) * e * 0.4))
    if e > 0.5:
        P.aim(f"foot.{back}", (0, 0.55, -0.85))                  # toes tucked behind
    P.rot("spine", (4 * e, 0, 0))
    kneel_arms(P, front, e)


def kneel_arms(P, front="L", e=1.0):
    """Arms for the kneel: the hand on the front knee rests on it, the other (the bell hand when front is L) hangs by
    the grounded knee with the bell just off the grass. Called by kneel(); whisper()/point() then re-pose the left."""
    bpy.context.view_layer.update()
    sx = {"L": 1, "R": -1}
    back = "R" if front == "L" else "L"
    knee = P.pb[f"shin.{front}"].matrix.translation
    rest = Vector((sx[front] * 0.2, -0.05, 0.9 - 0.39 * e))
    reach(P, front, rest.lerp(knee + Vector((sx[front] * 0.02, 0.03, 0.06)), e), pole=(sx[front], 0.4, -0.2),
          hand=(0, -1, -0.5))
    reach(P, back, Vector((sx[back] * 0.24, -0.08, 0.95 - 0.55 * e)), pole=(sx[back], 0.5, 0), hand=(0, -0.15, -1))


def whisper(P, t=1.0, toward=(0, -1, 0)):
    """S18: she leans in to whisper (chest and head forward and tipped), her left hand cupped beside her mouth.
    t 0..1 blends in. `toward`: where the ear she whispers to is (a direction, armature space)."""
    e = _ease(t)
    tw = Vector(toward).normalized()
    yaw = math.degrees(math.atan2(-tw.x, -tw.y))
    P.rot("chest", (16 * e, 0, yaw * 0.4 * e))
    P.rot("neck", (6 * e, 0, yaw * 0.3 * e))
    P.rot("head 1", (6 * e, -8 * e, yaw * 0.3 * e))
    hc = head_c(P)
    rest = Vector((0.2, -0.05, 0.9))
    reach(P, "L", rest.lerp(hc + Vector((0.075, -0.1, -0.075)), e), pole=(1, 0.3, -1), hand=(-0.35, -0.5, 0.8))


def point(P, direction, t=1.0):
    """S18: her left arm points along `direction` (armature space), straight, the hand on line. t 0..1 blends from
    the arm down. Key point_fingers(rig, f) for the index finger."""
    e = _ease(t)
    d = Vector(direction).normalized()
    down = Vector((0.17, 0.04, -1)).normalized()
    a = down.lerp(d, e).normalized()
    P.aim("upper_arm.L", a)
    P.aim("forearm.L", a)
    P.aim("hand.L", a)
    P.rot("chest", (0, 0, math.degrees(math.atan2(-d.x, -d.y)) * 0.25 * e))


def point_fingers(rig, f, side="L"):
    """Index finger out, the others curled (keyed at f)."""
    pb = rig["arm"].pose.bones
    for fn, curl in (("index", 0.0), ("middle", 1.0), ("ring", 1.0), ("pinky", 1.0)):
        for j, ang in ((1, 70), (2, 80), (3, 50)):
            name = f"f_{fn}.0{j}.{side}"
            if name not in pb:
                continue
            b = pb[name]
            b.rotation_mode = "QUATERNION"
            b.rotation_quaternion = Matrix.Rotation(math.radians(ang * curl), 4, "X").to_quaternion()
            b.keyframe_insert("rotation_quaternion", frame=f, group=name)


def sit(P, seat=0.42, feet_y=-0.36, bell_in_lap=True):
    """S19 top: sitting on a boat thwart `seat` high (armature units above her soles), feet forward on the boat
    floor, back straight; the bell hand rests in her lap, the left on her knee."""
    hz = P.pb["hips"].matrix.translation.z
    P.hips((0, 0.06, seat + 0.07 - hz))
    for s, sx in (("L", 1), ("R", -1)):
        P.leg(s, (sx * 0.12, feet_y, P.ankle_h))
    P.rot("spine", (-3, 0, 0))
    bpy.context.view_layer.update()
    kL = P.pb["shin.L"].matrix.translation
    kR = P.pb["shin.R"].matrix.translation
    reach(P, "L", kL + Vector((0.0, 0.02, 0.06)), pole=(1, 0.2, -0.3), hand=(0, -1, -0.6))
    if bell_in_lap:
        reach(P, "R", Vector((kR.x * 0.4, kR.y * 0.45 + 0.02, seat + 0.2)), pole=(-1, 0.3, -0.3),
              hand=(0.1, -0.2, -1))
