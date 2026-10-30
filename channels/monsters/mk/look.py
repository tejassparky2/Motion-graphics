"""The series' toon look in Blender EEVEE: banded cel shading with a soft rim, inverted-hull outlines, glossy eyes,
blob contact shadows, and the bright-sky / dim-fill world. Shared by every creature, set and shot."""
import math

import bpy

OUTLINE_RGB = "#2a1f2e"
_outline = None


def hexc(h, a=1.0):
    """sRGB hex to linear RGBA."""
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb], a)


def toon(name, base, shade=0.62, rim=0.35, gloss=False):
    """Three soft bands (shadow / mid / light) + a rim; `gloss` adds a hard specular dot (eyes, wet claws)."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "EASE"
    cr.elements[0].position, cr.elements[0].color = 0.36, (shade, shade * 0.97, shade * 1.08, 1)
    cr.elements[1].position, cr.elements[1].color = 0.42, (0.9, 0.9, 0.92, 1)
    e3 = cr.elements.new(0.8)
    e3.color = (1.06, 1.05, 1.0, 1)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs[7].default_value = base
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.25
    rr = nt.nodes.new("ShaderNodeValToRGB")
    rr.color_ramp.interpolation = "EASE"
    rr.color_ramp.elements[0].position, rr.color_ramp.elements[0].color = 0.55, (0, 0, 0, 1)
    rr.color_ramp.elements[1].position, rr.color_ramp.elements[1].color = 0.85, (rim, rim, rim, 1)
    add = nt.nodes.new("ShaderNodeMix")
    add.data_type, add.blend_type = "RGBA", "ADD"
    add.inputs["Factor"].default_value = 1.0
    em = nt.nodes.new("ShaderNodeEmission")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], mul.inputs[6])
    L(mul.outputs[2], add.inputs[6])
    L(lw.outputs["Facing"], rr.inputs[0])
    L(rr.outputs[0], add.inputs[7])
    col = add.outputs[2]
    if gloss:
        gl = nt.nodes.new("ShaderNodeBsdfGlossy")
        gl.inputs["Roughness"].default_value = 0.15
        s2 = nt.nodes.new("ShaderNodeShaderToRGB")
        r2 = nt.nodes.new("ShaderNodeValToRGB")
        r2.color_ramp.interpolation = "CONSTANT"
        r2.color_ramp.elements[1].position = 0.6
        a2 = nt.nodes.new("ShaderNodeMix")
        a2.data_type, a2.blend_type = "RGBA", "ADD"
        a2.inputs["Factor"].default_value = 1.0
        L(gl.outputs[0], s2.inputs[0])
        L(s2.outputs[0], r2.inputs[0])
        L(col, a2.inputs[6])
        L(r2.outputs[0], a2.inputs[7])
        col = a2.outputs[2]
    L(col, em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def flat(name, rgba, strength=1.0):
    """Unlit colour (glows, highlights, VFX)."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = rgba
    e.inputs[1].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


def fade(name, rgba, alpha):
    """Unlit, see-through (smoke, shockwave rings); its alpha can be keyframed through node 'Mix'."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.name = "Mix"
    mix.inputs[0].default_value = alpha
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = rgba
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(e.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], o.inputs[0])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    return m


def outline_mat():
    global _outline
    if _outline is None or _outline.name not in bpy.data.materials:
        _outline = flat("outline", hexc(OUTLINE_RGB))
        _outline.use_backface_culling = True
    return _outline


def outline(o, width=0.025):
    """Inverted-hull outline: a flipped, slightly fattened shell that only shows its back faces."""
    if not width:
        return o
    if outline_mat().name not in [m.name for m in o.data.materials if m]:
        o.data.materials.append(outline_mat())
    s = o.modifiers.new("outline", "SOLIDIFY")
    s.thickness = -width
    s.use_flip_normals = True
    s.material_offset = len(o.data.materials) - 1
    s.use_rim = False
    return o


def blob_shadow(name, loc, size, parent=None):
    """A soft dark ellipse under a character (game-style contact shadow)."""
    m = bpy.data.materials.get("blobshadow")
    if m is None:
        m = bpy.data.materials.new("blobshadow")
        m.use_nodes = True
        nt = m.node_tree
        nt.nodes.clear()
        L = nt.links.new
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        mix = nt.nodes.new("ShaderNodeMixShader")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        e = nt.nodes.new("ShaderNodeEmission")
        e.inputs[0].default_value = hexc("#2f2433")
        g = nt.nodes.new("ShaderNodeTexGradient")
        g.gradient_type = "SPHERICAL"
        tc = nt.nodes.new("ShaderNodeTexCoord")
        r = nt.nodes.new("ShaderNodeValToRGB")
        r.color_ramp.elements[1].position = 0.6
        r.color_ramp.elements[1].color = (0.55, 0.55, 0.55, 1)
        L(tc.outputs["Object"], g.inputs[0])
        L(g.outputs[0], r.inputs[0])
        L(r.outputs[0], mix.inputs[0])
        L(tr.outputs[0], mix.inputs[1])
        L(e.outputs[0], mix.inputs[2])
        L(mix.outputs[0], o.inputs[0])
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
    bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1.0, fill_type="NGON", location=loc)
    sh = bpy.context.object
    sh.name = name
    sh.scale = (size[0], size[1], 1)
    sh.data.materials.append(m)
    if parent:
        sh.parent = parent
        sh.matrix_parent_inverse = parent.matrix_world.inverted()
    return sh


def world(sky="#8fd3ff", fill="#bfe6ff", fill_strength=0.45):
    """The camera sees a bright sky; the lighting gets a dimmer fill so cel shadows read."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new("world")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = hexc(fill)
    bg.inputs[1].default_value = fill_strength
    sk = nt.nodes.new("ShaderNodeBackground")
    sk.inputs[0].default_value = hexc(sky)
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(bg.outputs[0], mix.inputs[1])
    nt.links.new(sk.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])
    return w


def sun(elev=40, azim=-35, energy=4.5, color="#fff4e0"):
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(90 - elev), 0, math.radians(azim)))
    s = bpy.context.object
    s.data.energy = energy
    s.data.angle = math.radians(3)
    s.data.color = hexc(color)[:3]
    s.data.use_shadow = True
    return s


def render_setup(w=720, h=1280, samples=16, fps=24):
    sc = bpy.context.scene
    r = sc.render
    r.resolution_x, r.resolution_y = w, h
    r.fps = fps
    engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    r.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = samples
    if hasattr(sc.eevee, "use_shadows"):
        sc.eevee.use_shadows = True
    sc.view_settings.view_transform = "Standard"
    r.image_settings.file_format = "PNG"
    return sc
