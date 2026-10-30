"""The hero (Kai), built by restyling the VRM Consortium's Seed-san sample (owner's choice, 30 Oct 2026). Licence and
the REQUIRED credit line: assets/monsters/hero/CREDIT.md.

    rig = build(loc, scale=1.0)   ->  dict(arm, expr, bone)
    arm   : the armature (root of the character; move/turn/scale it)
    expr  : the VRM expression presets (happy, angry, sad, relaxed, surprised, neutral, aa, ih, ou, ee, oh, blink,
            blink_left, blink_right, look_up, look_down, look_left, look_right); set .preview 0..1
    bone  : bone("head") -> the pose bone for a VRM humanoid bone name (head, neck, spine, chest, upper_chest, hips,
            left_upper_arm, left_lower_arm, left_hand, right_..., left_upper_leg, left_lower_leg, left_foot, ...)

Needs the VRM add-on (channels/monsters/setup_vrm.sh) and Blender run with -y (the expressions are drivers).
Scale: the model is 1.5 m tall in metres; in the creature world (1 unit = 20 cm) use scale=5.8 for a 1.75 m hero.
"""
import os

import bpy
import numpy as np
from PIL import Image

A = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "monsters", "hero"))
CUT = {"wear_metal", "backpack_metal", "backpack_nm", "backpack_plastic", "robo_face", "glass", "green_emit",
       "anim_logo", "armgear_plastic"}


def _swap_pixels(img_name, path):
    img = bpy.data.images[img_name]
    px = np.asarray(Image.open(path).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM), np.float32) / 255
    if px.shape[:2] != (img.size[1], img.size[0]):
        raise ValueError(f"{path}: size {px.shape[:2]} != {img.size[:]}")
    img.pixels.foreach_set(px.ravel())
    img.update()


def _plain_chest(o, bm):
    import bmesh
    """The sample's hexagon chest emblem is cut into the tunic (hexagon holes over a skin-textured patch, plus dark
    hexagon faces). Turn every face at that spot into plain tunic: tunic material, texture point on a plain patch.
    Found by flooding each texture with magenta and listing the faces there."""
    names = [m.name if m else "" for m in o.data.materials]
    tunic = names.index("huku_bake")
    wear = bpy.data.images["wear"]
    W, H = wear.size
    px = np.asarray(wear.pixels[:], np.float32).reshape(H, W, 4)
    uv = bm.loops.layers.uv.active
    for f in bm.faces:
        c = o.matrix_world @ f.calc_center_median()
        if not (0.02 < c.x < 0.13 and 1.05 < c.z < 1.19 and c.y < -0.03):
            continue
        name = names[f.material_index]
        if name == "huku_bake":
            u = sum(lp[uv].uv.x for lp in f.loops) / len(f.loops)
            v = sum(lp[uv].uv.y for lp in f.loops) / len(f.loops)
            if px[min(H - 1, int(v * H)), min(W - 1, int(u * W)), :3].max() > 0.35:
                continue                                          # ordinary tunic face
        elif name not in ("body_bake", "body_nm"):
            continue
        f.material_index = tunic
        for lp in f.loops:
            lp[uv].uv = (0.41, 0.81)                              # the plain spot under the old emblem
    # the hexagon holes cut into the tunic: fill them
    edges = [e for e in bm.edges if len(e.link_faces) == 1 and e.link_faces[0].material_index == tunic
             and (lambda m: 0.02 < m.x < 0.13 and 1.05 < m.z < 1.19 and m.y < -0.03)(
                 o.matrix_world @ ((e.verts[0].co + e.verts[1].co) / 2))]
    if edges:
        new = bmesh.ops.holes_fill(bm, edges=edges, sides=12)["faces"]
        for f in new:
            f.material_index = tunic
            f.smooth = True
            for lp in f.loops:
                lp[uv].uv = (0.41, 0.81)


def build(loc=(0, 0, 0), scale=1.0, rot_z=0.0):
    if "io_scene_vrm" not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module="io_scene_vrm")
    before = set(bpy.data.objects)
    bpy.ops.import_scene.vrm(filepath=os.path.join(A, "Seed-san.vrm"))
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == "ARMATURE")
    for o in new:
        if o.type == "MESH" and o.name.startswith("robo_arm"):
            bpy.data.objects.remove(o, do_unlink=True)
            continue
        if o.type == "MESH":
            import bmesh
            bm = bmesh.new()
            bm.from_mesh(o.data)
            cut = [f for f in bm.faces if o.data.materials[f.material_index]
                   and o.data.materials[f.material_index].name in CUT]
            if cut:
                bmesh.ops.delete(bm, geom=cut, context="FACES")
            if o.name == "wear":
                _plain_chest(o, bm)
            bm.to_mesh(o.data)
            bm.free()
            if o.name == "wear" and o.data.has_custom_normals:
                bpy.context.view_layer.objects.active = o
                with bpy.context.temp_override(object=o, active_object=o):
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                for p in o.data.polygons:
                    p.use_smooth = True
    _swap_pixels("wear", os.path.join(A, "wear_hero.png"))
    _swap_pixels("hair", os.path.join(A, "hair_hero.png"))
    _swap_pixels("body", os.path.join(A, "body_hero.png"))
    arm.location = loc
    arm.scale = (scale, scale, scale)
    arm.rotation_mode = "XYZ"           # the VRM import leaves it in QUATERNION mode (helper 10)
    arm.rotation_euler = (0, 0, rot_z)
    hb = arm.data.vrm_addon_extension.vrm1.humanoid.human_bones

    def bone(name):
        return arm.pose.bones[getattr(hb, name).node.bone_name]

    return dict(arm=arm, expr=arm.data.vrm_addon_extension.vrm1.expressions.preset, bone=bone)


def expression(rig, name, value, frame, interp="CONSTANT"):
    """Key an expression preset (e.g. "surprised", 1.0) at a frame. Anime faces snap between drawings, so the
    default interpolation is CONSTANT."""
    getattr(rig["expr"], name).preview = value
    path = f"vrm_addon_extension.vrm1.expressions.preset.{name}.preview"
    rig["arm"].data.keyframe_insert(data_path=path, frame=frame)
    ad = rig["arm"].data.animation_data
    if ad and ad.action:
        from . import anim
        for fc in anim.all_fcurves(ad.action):
            if fc.data_path == path:
                for kp in fc.keyframe_points:
                    if abs(kp.co.x - frame) < 0.01:
                        kp.interpolation = interp


# ---------------------------------------------------------------------------------------------------------------------
# Owner, 30 Oct 2026: "add hat to your hero with letter K". Plus TP5 from the report: convert MToon to the pipeline's
# Shader-to-RGB toon with an inverted-hull outline so the hero matches the creatures, and bake everything into
# assets/monsters/hero/hero.blend so helpers need no VRM add-on (load() below).
# ---------------------------------------------------------------------------------------------------------------------
CAP = "#f2f4f7"            # white crown (owner, 30 Oct: "change his dress... Pokémon and modern anime")
CAP_BRIM = "#1d9f94"       # teal brim and letter, matching the jacket; never a red-and-white cap
CAP_LETTER = "#1d9f94"
TOON_MATS = ("hair", "huku_bake", "body_bake", "body_nm")   # eye / eye_trans keep their (textured, alpha) shader


def _tex_toon(mat, tex_img, base_rgb):
    """Rebuild `mat` as: image texture x two-tone cel shade (one hard, cool shadow), through Emission, like look.toon."""
    from . import look
    nt = mat.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = tex_img
    tex.interpolation = "Closest" if tex_img.size[0] <= 512 else "Linear"
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, (*look.SHADOW_TINT, 1)
    cr.elements[1].position, cr.elements[1].color = 0.42, (1, 1, 1, 1)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], bw.inputs[0])
    L(bw.outputs[0], ramp.inputs[0])
    L(tex.outputs["Color"], mul.inputs[6])
    L(ramp.outputs[0], mul.inputs[7])
    L(mul.outputs[2], em.inputs[0])
    L(tex.outputs["Alpha"], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    mat.blend_method = "HASHED"
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    mat.use_backface_culling = False
    mat["base"] = base_rgb                                     # look.outline reads this for the line colour


def _mean_rgb(path):
    px = np.asarray(Image.open(path).convert("RGBA"), np.float32) / 255
    w = px[..., 3:4]
    m = (px[..., :3] * w).sum((0, 1)) / max(w.sum(), 1)
    return (float(m[0]), float(m[1]), float(m[2]), 1.0)


def toonify(rig, line=0.004):
    """TP5: swap the MToon shaders for our textured cel shade and add inverted-hull outlines (coloured lines,
    look.outline). The MToon outline geometry-node modifiers are removed. `line` is in model metres; change it per
    shot with line_width()."""
    from . import look
    tex_for = {"hair": ("hair", os.path.join(A, "hair_hero.png")),
               "huku_bake": ("wear", os.path.join(A, "wear_hero.png")),
               "body_bake": ("body", os.path.join(A, "body_hero.png")),
               "body_nm": ("body", os.path.join(A, "body_hero.png"))}
    for name, (img, path) in tex_for.items():
        m = bpy.data.materials.get(name)
        if m:
            _tex_toon(m, bpy.data.images[img], _mean_rgb(path))
    for o in bpy.data.objects:
        if o.type != "MESH" or o.parent != rig["arm"]:
            continue
        for md in list(o.modifiers):
            if md.type == "NODES":
                o.modifiers.remove(md)
        look.outline(o, line)
        o.modifiers["outline"].use_rim = False
        # the outline shell must deform with the armature: keep Armature first, Solidify after it
        while o.modifiers.find("outline") < o.modifiers.find("Armature"):
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.modifier_move_down(modifier="Armature")


def line_width(rig, line):
    """Outline thickness in model metres (≈ 2-3 px at the shot's framing: ~0.004 full body, ~0.0015 face close-up)."""
    from . import look
    for o in bpy.data.objects:
        if o.type == "MESH" and o.parent == rig["arm"] and "outline" in o.modifiers:
            o.modifiers["outline"].thickness = -line * look.LINE_SCALE


def cap(rig, letter="K"):
    """A navy cap with a cream letter on the front, fixed to the head bone. Hair under the dome is removed so the
    cowlick can't poke through; the fringe and sides stay."""
    from . import look
    import bmesh
    arm = rig["arm"]
    hb = rig["bone"]("head")
    top = arm.matrix_world @ hb.tail
    cx, cy = 0.0, 0.012
    rim_z, dome_r = 1.452, 0.136
    cap_m = look.toon("cap_crown", look.hexc(CAP))
    brim_m = look.toon("cap_brim", look.hexc(CAP_BRIM))
    k_m = look.flat("cap_letter", look.hexc(CAP_LETTER))
    # dome: the upper part of a sphere, squashed a little front-to-back
    me = bpy.data.meshes.new("cap_dome")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.12], context="VERTS")
    for v in bm.verts:
        v.co.x, v.co.y, v.co.z = v.co.x * dome_r, v.co.y * dome_r * 1.08, v.co.z * dome_r * 0.78
    bm.to_mesh(me)
    bm.free()
    dome = bpy.data.objects.new("cap", me)
    bpy.context.scene.collection.objects.link(dome)
    dome.location = (cx, cy, rim_z + 0.02)
    dome.data.materials.append(cap_m)
    for p in dome.data.polygons:
        p.use_smooth = True
    look.outline(dome, 0.004)
    dome.modifiers["outline"].use_rim = True
    dome.modifiers["outline"].material_offset_rim = dome.modifiers["outline"].material_offset
    # brim: a flat crescent in front
    me = bpy.data.meshes.new("cap_brim")
    bm = bmesh.new()
    verts = []
    import math
    for i in range(13):
        a = math.radians(-78 + i * 156 / 12)
        inner = bm.verts.new((math.sin(a) * dome_r * 0.98, -math.cos(a) * dome_r * 1.0, 0))
        f = math.cos(a) ** 1.5
        outer = bm.verts.new((math.sin(a) * dome_r * (1.0 + 0.15 * f), -math.cos(a) * dome_r * (1.0 + 0.85 * f),
                              -0.03 * f))
        verts.append((inner, outer))
    for (i1, o1), (i2, o2) in zip(verts[:-1], verts[1:]):
        bm.faces.new((i1, i2, o2, o1))
    bm.to_mesh(me)
    bm.free()
    brim = bpy.data.objects.new("cap_brim", me)
    bpy.context.scene.collection.objects.link(brim)
    brim.location = (cx, cy, rim_z - 0.004)
    brim.data.materials.append(brim_m)
    s = brim.modifiers.new("thick", "SOLIDIFY")
    s.thickness = 0.008
    s.offset = 0
    look.outline(brim, 0.004)
    brim.modifiers["outline"].use_rim = True
    brim.modifiers["outline"].material_offset_rim = brim.modifiers["outline"].material_offset
    # the letter: a text object on the front of the dome, converted to a thin mesh
    bpy.ops.object.text_add(location=(cx, cy - dome_r * 1.06, rim_z + 0.05))
    t = bpy.context.object
    t.data.body = letter
    t.data.align_x = "CENTER"
    t.data.align_y = "CENTER"
    t.data.size = 0.075
    t.data.extrude = 0.003
    t.rotation_euler = (math.radians(80), 0, 0)
    bpy.context.view_layer.objects.active = t
    t.select_set(True)
    bpy.ops.object.convert(target="MESH")
    t = bpy.context.object
    t.name = "cap_letter"
    t.data.materials.append(k_m)
    # shrink-wrap the letter onto the dome so it hugs the curve
    sw = t.modifiers.new("hug", "SHRINKWRAP")
    sw.target = dome
    sw.offset = 0.004
    sw.wrap_method = "NEAREST_SURFACEPOINT"
    # hide the hair under the dome: faces whose centre lies inside the dome volume
    hair = bpy.data.objects.get("hair")
    if hair:
        bm = bmesh.new()
        bm.from_mesh(hair.data)
        gone = []
        for f in bm.faces:
            c = hair.matrix_world @ f.calc_center_median()
            dx, dy, dz = (c.x - cx) / dome_r, (c.y - cy) / (dome_r * 1.08), (c.z - (rim_z + 0.02)) / (dome_r * 0.92)
            if dz > 0.05 and dx * dx + dy * dy + dz * dz < 0.98 and (c.y - cy) > -dome_r * 0.55:
                gone.append(f)
        bmesh.ops.delete(bm, geom=gone, context="FACES")
        bm.to_mesh(hair.data)
        bm.free()
    # fix all three to the head bone
    for o in (dome, brim, t):
        c = o.constraints.new("CHILD_OF")
        c.target = arm
        c.subtarget = hb.name
        c.inverse_matrix = (arm.matrix_world @ hb.matrix).inverted()
    rig["cap"] = [dome, brim, t]
    return rig["cap"]


def shoes(rig):
    """White sneakers with a yellow toe cap and a dark sole, built as smooth SDF shapes around each foot and fixed to
    the foot bones. The sample is barefoot; the bare-foot skin under them is removed."""
    from . import look, sdf
    import bmesh
    arm = rig["arm"]
    white = look.toon("shoe_white", look.hexc("#f4f6f9"))
    accent = look.toon("shoe_accent", look.hexc("#ffc23a"))
    sole = look.toon("shoe_sole", look.hexc("#3a3d46"))
    out = []
    for side in ("L", "R"):
        foot = arm.pose.bones[f"foot.{side}"]
        toe = arm.pose.bones[f"toe.{side}"]
        ankle = arm.matrix_world @ foot.head
        tip = arm.matrix_world @ toe.tail
        heel = (ankle.x, ankle.y + 0.035, 0.045)
        front = (tip.x, tip.y + 0.012, 0.038)
        mid = ((heel[0] + front[0]) / 2, (heel[1] + front[1]) / 2, 0.012)
        length = abs(front[1] - heel[1]) + 0.1
        parts = [
            (sdf.C(heel, front, 0.05, 0.042), white.name, None),
            (sdf.E(heel, (0.046, 0.055, 0.048)), white.name, 0.03),
            (sdf.C((ankle.x, ankle.y + 0.012, 0.06), (ankle.x, ankle.y + 0.012, 0.1), 0.047, 0.044), white.name, 0.03),
            (sdf.E((front[0], front[1] - 0.006, front[2]), (0.046, 0.05, 0.036)), accent.name, 0.015),
            (sdf.E(mid, (0.056, length / 2, 0.015)), sole.name, 0.01),
        ]
        o = sdf.build(f"shoe.{side}", parts, k=0.02, res=0.005, pad=0.03, smooth_iter=6)
        look.outline(o, 0.003)
        c = o.constraints.new("CHILD_OF")
        c.target = arm
        c.subtarget = foot.name
        c.inverse_matrix = (arm.matrix_world @ foot.matrix).inverted()
        out.append(o)
    wear = bpy.data.objects.get("wear")
    if wear:
        bm = bmesh.new()
        bm.from_mesh(wear.data)
        names = [m.name if m else "" for m in wear.data.materials]
        gone = [f for f in bm.faces if names[f.material_index] in ("body_bake", "body_nm")
                and (wear.matrix_world @ f.calc_center_median()).z < 0.085]
        bmesh.ops.delete(bm, geom=gone, context="FACES")
        bm.to_mesh(wear.data)
        bm.free()
    rig["shoes"] = out
    return out


FACES = {                                                       # shape-key recipes on the head mesh (see hero.blend)
    "neutral": {}, "happy": {"face_happy": 1}, "angry": {"face_angry": 1}, "sad": {"face_sad": 1},
    "relaxed": {"face_relax": 1}, "surprised": {"face_surprise": 1}, "blink": {"eye_close": 1},
    "wink": {"blink_R": 1}, "squint": {"eye_zitome": 1}, "star": {"eye_star": 1}, "shock": {"shock_plane": 1},
    "pinprick": {"eye_black_small": 1}, "dot": {"eye_black_big": 1}, "v": {"eye_V": 1}, "blush": {"cheek": 1},
    "aa": {"lip_a": 1}, "ih": {"lip_i": 1}, "ou": {"lip_u": 1}, "ee": {"lip_e": 1}, "oh": {"lip_o": 1},
    "mouth_open": {"mouse_open": 1}, "grit": {"mouth_wide": 1}, "brows_up": {"eye_brow_up": 1},
    "brows_down": {"eye_brow_down": 1}, "look_up": {"look_up": 1}, "look_down": {"look_down": 1},
    "look_left": {"look_left": 1}, "look_right": {"look_right": 1},
}


def face(rig, name, frame, value=1.0, interp="CONSTANT"):
    """Key a face from FACES (or any raw shape-key name) on the head mesh at `frame`. Keys every recipe key, so the
    previous face is cleared where the recipe sets 0. Anime faces snap, so CONSTANT by default."""
    head = bpy.data.objects["head"]
    kb = head.data.shape_keys.key_blocks
    recipe = FACES.get(name, {name: 1})
    touched = set()
    for rname, rv in FACES.items():
        touched.update(rv.keys())
    for k in touched:
        if k not in kb:
            continue
        kb[k].value = recipe.get(k, 0) * value
        kb[k].keyframe_insert("value", frame=frame)
    from . import anim
    ad = head.data.shape_keys.animation_data
    if ad and ad.action:
        for fc in anim.all_fcurves(ad.action):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.01:
                    kp.interpolation = interp


def _strip_drivers():
    """The VRM expression drivers point at add-on properties; without the add-on they error. Remove them so the
    shape keys are keyed directly (face())."""
    for o in bpy.data.objects:
        if o.type == "MESH" and o.data.shape_keys and o.data.shape_keys.animation_data:
            ad = o.data.shape_keys.animation_data
            for d in list(ad.drivers):
                ad.drivers.remove(d)
    for o in bpy.data.objects:
        if o.animation_data:
            for d in list(o.animation_data.drivers):
                o.animation_data.drivers.remove(d)
        if o.data and getattr(o.data, "animation_data", None):
            for d in list(o.data.animation_data.drivers):
                o.data.animation_data.drivers.remove(d)
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data:
            for d in list(m.node_tree.animation_data.drivers):
                m.node_tree.animation_data.drivers.remove(d)


def save_blend(path=None):
    """Build the finished hero (restyle + cap + toon + no drivers) and save hero.blend with both outfit textures
    packed. Run with the VRM add-on (BLENDER_USER_SCRIPTS=... blender -b -y)."""
    path = path or os.path.join(A, "hero.blend")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    rig = build()
    tail = bpy.data.objects.get("hair_tail")
    if tail:
        bpy.data.objects.remove(tail, do_unlink=True)          # a boy with short hair: no ponytail
    toonify(rig)
    cap(rig)
    shoes(rig)
    _strip_drivers()
    # the imported images are packed copies of the SAMPLE's textures; pixel edits in memory are not what gets saved.
    # Repoint each to our PNG on disk, reload, then pack, so hero.blend carries the restyled textures.
    for name, fn in (("wear", "wear_hero.png"), ("hair", "hair_hero.png"), ("body", "body_hero.png")):
        img = bpy.data.images[name]
        if img.packed_file:
            img.unpack(method="REMOVE")
        img.filepath = img.filepath_raw = os.path.join(A, fn)
        img.source = "FILE"
        img.reload()
    earth = bpy.data.images.load(os.path.join(A, "wear_earth.png"))
    earth.name = "wear_earth"
    for img in bpy.data.images:
        if img.size[0] and not img.packed_file:
            try:
                img.pack()
            except RuntimeError:
                pass
    col = bpy.data.collections.new("hero")
    bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.collection.objects):
        bpy.context.scene.collection.objects.unlink(o)
        col.objects.link(o)
    for o in col.objects:
        o.name = "hero_" + o.name if not o.name.startswith("hero_") else o.name
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    kb = [k.name for k in bpy.data.objects["hero_head"].data.shape_keys.key_blocks]
    print("SAVED", path, "shapekeys", kb, flush=True)


def load(loc=(0, 0, 0), scale=1.0, rot_z=0.0, outfit="world", line=0.004):
    """Append the finished hero from hero.blend (no add-on needed). outfit: "world" (sage tunic) or "earth" (charcoal
    shirt, the lab). Returns the same rig dict as build(): arm, bone(name), cap, plus face() works on it."""
    path = os.path.join(A, "hero.blend")
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = ["hero"]
    col = dst.collections[0]
    bpy.context.scene.collection.children.link(col)
    for o in col.objects:                                      # drop the "hero_" prefix if nothing else uses the name
        base = o.name[5:] if o.name.startswith("hero_") else o.name
        if base not in bpy.data.objects:
            o.name = base
    arm = next(o for o in col.objects if o.type == "ARMATURE")
    arm.location = loc
    arm.scale = (scale, scale, scale)
    arm.rotation_mode = "XYZ"           # saved in QUATERNION mode by the VRM import; Euler so rot_z works
    arm.rotation_euler = (0, 0, rot_z)
    if outfit == "earth":
        wear = bpy.data.materials["huku_bake"].node_tree.nodes
        for n in wear:
            if n.type == "TEX_IMAGE" and n.image and n.image.name.startswith("wear"):
                n.image = bpy.data.images["wear_earth"]
    bones = {b.name: b for b in arm.pose.bones}
    # the VRM humanoid names -> this skeleton's (Rigify-style) bone names
    rigify = {"head": "head 1", "neck": "neck", "spine": "spine", "chest": "chest", "hips": "hips",
              "left_shoulder": "shoulder.L", "right_shoulder": "shoulder.R",
              "left_upper_arm": "upper_arm.L", "right_upper_arm": "upper_arm.R",
              "left_lower_arm": "forearm.L", "right_lower_arm": "forearm.R",
              "left_hand": "hand.L", "right_hand": "hand.R",
              "left_upper_leg": "thigh.L", "right_upper_leg": "thigh.R",
              "left_lower_leg": "shin.L", "right_lower_leg": "shin.R",
              "left_foot": "foot.L", "right_foot": "foot.R"}

    def bone(name):
        for cand in (rigify.get(name, name), name):
            if cand in bones:
                return bones[cand]
        raise KeyError(f"no bone for {name}; have {sorted(bones)}")

    rig = dict(arm=arm, bone=bone, cap=[o for o in col.objects if o.name.startswith("cap")])
    line_width(rig, line)
    return rig
