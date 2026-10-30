"""Anime BACKGROUND painting in 3D, modelled on Pokémon Horizons frames (episodes 1383-1386, studied 30 Oct 2026):
- trees are "cauliflower" foliage: many small leaf clumps merged into one mass, painted in three bands (dark green
  inside and underneath, mid green, yellow-green where the light hits), edges broken up by noise, no outlines;
- grass is dense painted brush strokes in three greens, stretched sideways like a painter's strokes;
- the sky is a deep-blue-to-pale gradient with thin, flat-bottomed, wispy clouds with lavender shadows;
- nothing in the background has outlines; depth of field softens it behind the characters.
"""
import math
import random

import bpy

from . import look, sdf


def paint3(name, dark, mid, light, cuts=(0.32, 0.68), noise=0.18, scale=3.0):
    """Three painted bands driven by the light, with a noisy band edge (brush-like)."""
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
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 4.0
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "MULTIPLY_ADD"                             # light + (noise - 0.5) * noise_amount
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = 0.5
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, dark
    cr.elements[1].position, cr.elements[1].color = cuts[0], mid
    e3 = cr.elements.new(cuts[1])
    e3.color = light
    em = nt.nodes.new("ShaderNodeEmission")
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], bw.inputs[0])
    L(nz.outputs["Fac"], sub.inputs[0])
    L(sub.outputs[0], add.inputs[0])
    add.inputs[1].default_value = noise
    L(bw.outputs[0], add.inputs[2])
    L(add.outputs[0], ramp.inputs[0])
    L(ramp.outputs[0], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def greens(variant=0, far=0.0):
    """Anime foliage palettes; `far` (0-1) fades toward the sky (atmospheric perspective)."""
    sets = [("#1f6b3a", "#36a64a", "#9ee05a"), ("#2a7a3c", "#4cb84f", "#b8ec6a"), ("#1d5e46", "#2f9b62", "#8fdd8a"),
            ("#3a6f2a", "#6aae3c", "#d3ef72")]
    sky = look.hexc("#bfe3ff")
    out = []
    for h in sets[variant % len(sets)]:
        c = look.hexc(h)
        out.append(tuple(c[i] * (1 - far) + sky[i] * far for i in range(3)) + (1,))
    return out


def tree(loc, height=6.0, radius=2.6, seed=0, variant=0, far=0.0, res=None):
    """A painted anime tree: trunk with two branches and a cauliflower canopy of merged leaf clumps."""
    rnd = random.Random(seed)
    x, y, z = loc
    trunk_m = paint3(f"trunk_{round(far, 2)}", *(
        tuple(c * (1 - far) + s * far for c, s in zip(look.hexc(h)[:3], look.hexc("#bfe3ff")[:3])) + (1,)
        for h in ("#4a2f22", "#6e4a33", "#8f6a4a")), noise=0.1)
    leaf_m = paint3(f"leaf_v{variant}_{round(far, 2)}", *greens(variant, far))
    th = height * 0.55
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=radius * 0.16, radius2=radius * 0.09, depth=th,
                                    location=(x, y, z + th / 2))
    t = bpy.context.object
    t.data.materials.append(trunk_m)
    for p in t.data.polygons:
        p.use_smooth = True
    cz = z + th + radius * 0.35
    parts = [(sdf.E((x, y, cz), (radius * 0.85, radius * 0.8, radius * 0.7)), leaf_m.name, None)]
    for i in range(22):                                        # leaf clumps around the core, more on top
        a = rnd.uniform(0, 2 * math.pi)
        el = rnd.uniform(-0.35, 1.0)
        r = radius * rnd.uniform(0.75, 1.0)
        c = (x + math.cos(a) * math.cos(el) * r, y + math.sin(a) * math.cos(el) * r * 0.9,
             cz + math.sin(el) * r * 0.8)
        s = radius * rnd.uniform(0.28, 0.45)
        parts.append((sdf.E(c, (s, s, s * 0.9)), leaf_m.name, None))
    canopy = sdf.build(f"canopy_{seed}", parts, k=radius * 0.12, res=res or max(0.06, radius / 28), smooth_iter=6)
    return t, canopy


def grass_material(name="anime_grass"):
    """Painted grass: brush strokes stretched sideways, three greens, slightly brighter where lit."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.35, 3.0, 1.0)        # strokes run left-right as seen by the camera
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 4.0
    nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.65
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, look.hexc("#2c8f36")
    cr.elements[1].position, cr.elements[1].color = 0.44, look.hexc("#46c046")
    e3 = cr.elements.new(0.6)
    e3.color = look.hexc("#7fdc58")
    em = nt.nodes.new("ShaderNodeEmission")
    L(tc.outputs["Object"], mp.inputs[0])
    L(mp.outputs[0], nz.inputs[0])
    L(nz.outputs["Fac"], ramp.inputs[0])
    L(ramp.outputs[0], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def sky(top="#2f86d8", mid="#6fb6ee", horizon="#d8eeff", clouds=True, fill="#bfe6ff", fill_strength=0.45):
    """Gradient sky with painted wispy clouds (camera rays only; lighting gets a dim fill)."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new("anime_sky")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    L = nt.links.new
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = look.hexc(fill)
    bg.inputs[1].default_value = fill_strength
    camsky = nt.nodes.new("ShaderNodeBackground")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    grad = nt.nodes.new("ShaderNodeValToRGB")
    g = grad.color_ramp
    g.interpolation = "EASE"
    g.elements[0].position, g.elements[0].color = 0.0, look.hexc(horizon)
    g.elements[1].position, g.elements[1].color = 0.55, look.hexc(top)
    e = g.elements.new(0.18)
    e.color = look.hexc(mid)
    L(tc.outputs["Generated"], sep.inputs[0])
    L(sep.outputs["Z"], grad.inputs[0])
    col = grad.outputs[0]
    if clouds:
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1.0, 1.0, 5.0)     # flattened: wispy, flat-bottomed layers
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 2.2
        nz.inputs["Detail"].default_value = 5.0
        nz.inputs["Roughness"].default_value = 0.6
        mask = nt.nodes.new("ShaderNodeValToRGB")
        mask.color_ramp.elements[0].position, mask.color_ramp.elements[0].color = 0.56, (0, 0, 0, 1)
        mask.color_ramp.elements[1].position, mask.color_ramp.elements[1].color = 0.66, (1, 1, 1, 1)
        band = nt.nodes.new("ShaderNodeValToRGB")              # clouds only between the horizon and mid-sky
        band.color_ramp.elements[0].position, band.color_ramp.elements[0].color = 0.02, (0, 0, 0, 1)
        band.color_ramp.elements[1].position, band.color_ramp.elements[1].color = 0.12, (1, 1, 1, 1)
        top_fade = band.color_ramp.elements.new(0.42)
        top_fade.color = (1, 1, 1, 1)
        fade_end = band.color_ramp.elements.new(0.6)
        fade_end.color = (0, 0, 0, 1)
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        shade_nz = nt.nodes.new("ShaderNodeTexNoise")
        shade_nz.inputs["Scale"].default_value = 2.2
        shade_nz.inputs["Detail"].default_value = 5.0
        shade_nz.inputs["Roughness"].default_value = 0.6
        off = nt.nodes.new("ShaderNodeVectorMath")
        off.operation = "ADD"
        off.inputs[1].default_value = (0.0, 0.0, -0.02)
        shade = nt.nodes.new("ShaderNodeValToRGB")
        shade.color_ramp.elements[0].position, shade.color_ramp.elements[0].color = 0.55, look.hexc("#ffffff")
        shade.color_ramp.elements[1].position, shade.color_ramp.elements[1].color = 0.7, look.hexc("#c9c8ea")
        cmix = nt.nodes.new("ShaderNodeMix")
        cmix.data_type = "RGBA"
        L(tc.outputs["Generated"], mp.inputs[0])
        L(mp.outputs[0], nz.inputs[0])
        L(nz.outputs["Fac"], mask.inputs[0])
        L(sep.outputs["Z"], band.inputs[0])
        L(mask.outputs[0], mul.inputs[0])
        L(band.outputs[0], mul.inputs[1])
        L(mp.outputs[0], off.inputs[0])
        L(off.outputs[0], shade_nz.inputs[0])
        L(shade_nz.outputs["Fac"], shade.inputs[0])
        L(mul.outputs[0], cmix.inputs["Factor"])
        L(col, cmix.inputs[6])
        L(shade.outputs[0], cmix.inputs[7])
        col = cmix.outputs[2]
    L(col, camsky.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(lp.outputs["Is Camera Ray"], mix.inputs[0])
    L(bg.outputs[0], mix.inputs[1])
    L(camsky.outputs[0], mix.inputs[2])
    L(mix.outputs[0], nt.nodes["World Output"].inputs[0])
    return w


def grass_tufts(center, radius, n=120, seed=7, avoid=None):
    """Clumps of painted grass blades near the camera (thin cones in three greens), skipping an `avoid(x, y)` area."""
    rnd = random.Random(seed)
    mats = [paint3(f"tuft{i}", *greens(i)) for i in range(3)]
    for i in range(n):
        x = center[0] + rnd.uniform(-radius, radius)
        y = center[1] + rnd.uniform(-radius, radius)
        if avoid and avoid(x, y):
            continue
        for j in range(3):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.05, depth=rnd.uniform(0.25, 0.5),
                                            location=(x + rnd.uniform(-0.08, 0.08), y, 0.15),
                                            rotation=(rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), 0))
            bpy.context.object.data.materials.append(rnd.choice(mats))
