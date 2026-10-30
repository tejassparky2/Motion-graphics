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
            lp[uv].uv = (0.2, 0.75)                               # a plain spot on the tunic front
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
                lp[uv].uv = (0.2, 0.75)


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
    _swap_pixels("wear", os.path.join(A, "wear_hero.png"))
    _swap_pixels("hair", os.path.join(A, "hair_hero.png"))
    _swap_pixels("body", os.path.join(A, "body_hero.png"))
    arm.location = loc
    arm.scale = (scale, scale, scale)
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
