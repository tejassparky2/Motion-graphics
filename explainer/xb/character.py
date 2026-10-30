"""Characters generated with MPFB2 (MakeHuman for Blender); all assets used are CC0."""
import bpy

from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.faceservice import FaceService
from bl_ext.user_default.mpfb.services.objectservice import ObjectService


def make_human(name="Hero", phenotype=None, skin="young_caucasian_male/young_caucasian_male.mhmat",
               hair="short02/short02.mhclo", clothes=("male_casualsuit05/male_casualsuit05.mhclo",),
               eyes_color="brown", rig="default", subdiv=1, faceunits=True):
    info = HumanService._create_default_human_info_dict()
    info["name"] = name
    if phenotype:
        info["phenotype"].update(phenotype)
    info["rig"] = rig
    info["eyes"] = "high-poly/high-poly.mhclo"
    info["eyebrows"] = "eyebrow001/eyebrow001.mhclo"
    info["eyelashes"] = "eyelashes01/eyelashes01.mhclo"
    info["teeth"] = "teeth_base/teeth_base.mhclo"
    info["tongue"] = "tongue01/tongue01.mhclo"
    info["hair"] = hair
    info["clothes"] = list(clothes)
    info["skin_mhmat"] = skin
    info["skin_material_type"] = "ENHANCED_SSS"
    info["eyes_material_type"] = "PROCEDURAL_EYES"
    settings = HumanService.get_default_deserialization_settings()
    settings["subdiv_levels"] = subdiv
    body = HumanService.deserialize_from_dict(info, settings)
    if faceunits:
        FaceService.load_targets(body, load_microsoft_visemes=False, load_arkit_faceunits=True)
        FaceService.interpolate_targets(body)
    rig_obj = ObjectService.find_object_of_type_amongst_nearest_relatives(body, "Skeleton")
    return body, rig_obj



def restyle_clothes(rig, color):
    """Give the T-shirt a plain dyed cotton (no print), keeping the jeans and MPFB's wrinkle normals.

    Faces are split by the colour of the texture under them: blue denim stays, everything else is shirt."""
    import numpy as np
    for ob in rig.children:
        if 'casualsuit' not in ob.name or not ob.material_slots:
            continue
        m = ob.material_slots[0].material
        nt = m.node_tree
        bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
        img = next(n.image for n in nt.nodes if n.type == 'TEX_IMAGE' and n.image and 'diffuse' in n.image.name)
        w, h = img.size
        px = np.asarray(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[:, :, :3]
        me = ob.data
        uv = np.zeros(len(me.loops) * 2, dtype=np.float32)
        me.uv_layers.active.data.foreach_get('uv', uv)
        uv = uv.reshape(-1, 2)
        ls = np.zeros(len(me.polygons), dtype=np.int32)
        lt = np.zeros(len(me.polygons), dtype=np.int32)
        me.polygons.foreach_get('loop_start', ls)
        me.polygons.foreach_get('loop_total', lt)
        cen = np.add.reduceat(uv, ls) / lt[:, None]
        xi = np.clip((cen[:, 0] % 1.0) * w, 0, w - 1).astype(int)
        yi = np.clip((cen[:, 1] % 1.0) * h, 0, h - 1).astype(int)
        c = px[yi, xi]
        mx, mn = c.max(1), c.min(1)
        sat = (mx - mn) / np.maximum(mx, 1e-4)
        co = np.zeros(len(me.vertices) * 3, dtype=np.float32)
        me.vertices.foreach_get('co', co)
        co = co.reshape(-1, 3)
        vi = np.zeros(len(me.loops), dtype=np.int32)
        me.loops.foreach_get('vertex_index', vi)
        zc = np.add.reduceat(co[vi][:, 2], ls) / lt
        denim_tex = (c[:, 2] > c[:, 0] * 1.15) & (sat > 0.18) & (mx < 0.85)
        denim = (zc < 0.86) | (denim_tex & (zc < 1.1))
        shirt = m.copy()
        shirt.name = 'Shirt'
        snt = shirt.node_tree
        sb = next(n for n in snt.nodes if n.type == 'BSDF_PRINCIPLED')
        for l in list(snt.links):
            if l.to_socket == sb.inputs['Base Color']:
                snt.links.remove(l)
        weave = snt.nodes.new('ShaderNodeTexNoise')
        weave.inputs['Scale'].default_value = 900.0
        mix = snt.nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.inputs[0].default_value = 0.0
        snt.links.new(weave.outputs['Fac'], mix.inputs[0])
        mix.inputs[6].default_value = (*[x * 0.85 for x in color], 1.0)
        mix.inputs[7].default_value = (*[min(1.0, x * 1.15) for x in color], 1.0)
        snt.links.new(mix.outputs[2], sb.inputs['Base Color'])
        sb.inputs['Roughness'].default_value = 0.85
        if 'Sheen Weight' in sb.inputs:
            sb.inputs['Sheen Weight'].default_value = 0.15
        me.materials.append(shirt)
        mi = np.where(denim, 0, len(me.materials) - 1).astype(np.int32)
        me.polygons.foreach_set('material_index', mi)
        print("restyle_clothes:", ob.name, int((~denim).sum()), "shirt faces,", int(denim.sum()), "denim faces")
