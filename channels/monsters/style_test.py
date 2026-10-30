"""Style test for the monster series: an original creature ("puff-shrimp": chubby aqua body, one huge coral claw,
antennae, tail fan, fluffy collar, big glossy eyes) in a bright toon look (EEVEE: Shader to RGB banding, rim light,
inverted-hull outlines) on a pastel meadow with a smoking crater.

    blender -b -P channels/monsters/style_test.py -- OUT.png [toon|soft] [WIDTH HEIGHT]
"""
import math
import sys
import time

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
LOOK = argv[1] if len(argv) > 1 else "toon"
W, H = (int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
OUTLINE = None


def hexc(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, a)


def toon(name, base, shade=0.62, rim=0.35, gloss=False):
    """Two-band cel material with a soft rim; `soft` look uses a plain Principled BSDF instead."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    if LOOK == "soft":
        b = nt.nodes.new("ShaderNodeBsdfPrincipled")
        b.inputs["Base Color"].default_value = base
        b.inputs["Roughness"].default_value = 0.25 if gloss else 0.6
        b.inputs["Subsurface Weight"].default_value = 0.15
        b.inputs["Subsurface Radius"].default_value = (0.3, 0.2, 0.15)
        nt.links.new(b.outputs[0], out.inputs[0])
        return m
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].position = 0.36
    ramp.color_ramp.elements[0].color = (shade, shade * 0.97, shade * 1.08, 1)
    ramp.color_ramp.elements[1].position = 0.42
    ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.92, 1)
    e3 = ramp.color_ramp.elements.new(0.8)
    e3.color = (1.06, 1.05, 1.0, 1)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs[7].default_value = base
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.25
    rr = nt.nodes.new("ShaderNodeValToRGB")
    rr.color_ramp.interpolation = "EASE"
    rr.color_ramp.elements[0].position = 0.55
    rr.color_ramp.elements[0].color = (0, 0, 0, 1)
    rr.color_ramp.elements[1].position = 0.85
    rr.color_ramp.elements[1].color = (rim, rim, rim, 1)
    add = nt.nodes.new("ShaderNodeMix")
    add.data_type = "RGBA"
    add.blend_type = "ADD"
    add.inputs["Factor"].default_value = 1.0
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(dif.outputs[0], s2r.inputs[0])
    nt.links.new(s2r.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], mul.inputs[6])
    nt.links.new(mul.outputs[2], add.inputs[6])
    nt.links.new(lw.outputs["Facing"], rr.inputs[0])
    nt.links.new(rr.outputs[0], add.inputs[7])
    out_col = add.outputs[2]
    if gloss:                                                  # a hard specular dot for eyes
        gl = nt.nodes.new("ShaderNodeBsdfGlossy")
        gl.inputs["Roughness"].default_value = 0.15
        s2 = nt.nodes.new("ShaderNodeShaderToRGB")
        r2 = nt.nodes.new("ShaderNodeValToRGB")
        r2.color_ramp.interpolation = "CONSTANT"
        r2.color_ramp.elements[1].position = 0.6
        a2 = nt.nodes.new("ShaderNodeMix")
        a2.data_type = "RGBA"
        a2.blend_type = "ADD"
        a2.inputs["Factor"].default_value = 1.0
        nt.links.new(gl.outputs[0], s2.inputs[0])
        nt.links.new(s2.outputs[0], r2.inputs[0])
        nt.links.new(add.outputs[2], a2.inputs[6])
        nt.links.new(r2.outputs[0], a2.inputs[7])
        out_col = a2.outputs[2]
    nt.links.new(out_col, em.inputs[0])
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def outline_mat():
    global OUTLINE
    if OUTLINE is None:
        OUTLINE = bpy.data.materials.new("outline")
        OUTLINE.use_nodes = True
        nt = OUTLINE.node_tree
        nt.nodes.clear()
        e = nt.nodes.new("ShaderNodeEmission")
        e.inputs[0].default_value = hexc("#2a1f2e")
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(e.outputs[0], o.inputs[0])
        OUTLINE.use_backface_culling = True
    return OUTLINE


def finish(o, mat, line=0.025):
    o.data.materials.append(mat)
    if LOOK == "toon" and line:
        o.data.materials.append(outline_mat())
        s = o.modifiers.new("outline", "SOLIDIFY")
        s.thickness = -line
        s.use_flip_normals = True
        s.material_offset = 1
        s.use_rim = False
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def blob(name, loc, scale, mat, rot=(0, 0, 0), line=0.025, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return finish(o, mat, line)


def tube(name, pts, radius, mat, line=0.015):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    o = bpy.context.object
    return finish(o, mat, line)


# ------------------------------------------------------------------ the creature (original design)
AQUA, CREAM, CORAL, BLUSH = hexc("#8fe3d6"), hexc("#fff3dc"), hexc("#ff7a5c"), hexc("#ff9fb4")
body_m, belly_m, claw_m = toon("body", AQUA), toon("belly", CREAM), toon("claw", CORAL)
eye_m, white_m, blush_m = toon("eye", hexc("#1b1830"), shade=0.8, gloss=True), toon("hi", (1, 1, 1, 1), 1, 0), \
    toon("blush", BLUSH, 0.9, 0.0)
X0 = 0.0
body = blob("body", (X0, 0, 1.0), (1.0, 0.92, 0.95), body_m)
blob("belly", (X0, -0.55, 0.85), (0.62, 0.42, 0.6), belly_m, line=0.0)
for i in range(14):                                            # fluffy collar
    a = i / 14 * 2 * math.pi
    blob(f"fluff{i}", (X0 + math.cos(a) * 0.82, math.sin(a) * 0.74, 1.55 + 0.05 * math.sin(3 * a)),
         (0.26, 0.26, 0.2), belly_m, line=0.018, seg=24)
for sx in (-1, 1):                                             # eyes + highlights + blush
    ex = X0 + sx * 0.36
    blob(f"eye{sx}", (ex, -0.78, 1.2), (0.23, 0.12, 0.31), eye_m, line=0.022)
    blob(f"hi{sx}", (ex + 0.08, -0.89, 1.33), (0.08, 0.03, 0.09), white_m, line=0.0, seg=16)
    blob(f"hi2{sx}", (ex - 0.07, -0.9, 1.1), (0.04, 0.02, 0.04), white_m, line=0.0, seg=12)
    blob(f"blush{sx}", (X0 + sx * 0.62, -0.7, 0.98), (0.14, 0.04, 0.08), blush_m, line=0.0, seg=16)
    tube(f"ant{sx}", [(X0 + sx * 0.25, -0.2, 1.85), (X0 + sx * 0.45, -0.35, 2.4), (X0 + sx * 0.85, -0.2, 2.7)],
         0.035, body_m)
    blob(f"antip{sx}", (X0 + sx * 0.85, -0.2, 2.7), (0.09, 0.09, 0.09), claw_m, line=0.015, seg=16)
blob("mouth", (X0, -0.86, 0.9), (0.11, 0.03, 0.08), eye_m, line=0.0, seg=16)
blob("tongue", (X0, -0.88, 0.86), (0.07, 0.02, 0.035), blush_m, line=0.0, seg=16)
shadow_m = bpy.data.materials.new("blobshadow")              # a soft game-style contact shadow
shadow_m.use_nodes = True
sn = shadow_m.node_tree
sn.nodes.clear()
so = sn.nodes.new("ShaderNodeOutputMaterial")
sm = sn.nodes.new("ShaderNodeMixShader")
st = sn.nodes.new("ShaderNodeBsdfTransparent")
se = sn.nodes.new("ShaderNodeEmission")
se.inputs[0].default_value = hexc("#2f2433")
sg = sn.nodes.new("ShaderNodeTexGradient")
sg.gradient_type = "SPHERICAL"
stc = sn.nodes.new("ShaderNodeTexCoord")
smap = sn.nodes.new("ShaderNodeMapping")
smap.inputs["Scale"].default_value = (1.0, 1.0, 1.0)
sr = sn.nodes.new("ShaderNodeValToRGB")
sr.color_ramp.elements[0].color = (0, 0, 0, 1)
sr.color_ramp.elements[1].position = 0.6
sr.color_ramp.elements[1].color = (0.55, 0.55, 0.55, 1)
sn.links.new(stc.outputs["Object"], smap.inputs[0])
sn.links.new(smap.outputs[0], sg.inputs[0])
sn.links.new(sg.outputs[0], sr.inputs[0])
sn.links.new(sr.outputs[0], sm.inputs[0])
sn.links.new(st.outputs[0], sm.inputs[1])
sn.links.new(se.outputs[0], sm.inputs[2])
sn.links.new(sm.outputs[0], so.inputs[0])
if hasattr(shadow_m, "surface_render_method"):
    shadow_m.surface_render_method = "BLENDED"
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1.0, fill_type="NGON", location=(X0 - 0.2, -0.05, 0.075))
sh = bpy.context.object
sh.scale = (1.35, 1.1, 1)
sh.data.materials.append(shadow_m)
for i, (lx, ly) in enumerate([(-0.5, -0.4), (0.5, -0.4), (-0.45, 0.35), (0.45, 0.35)]):
    blob(f"leg{i}", (X0 + lx, ly, 0.16), (0.17, 0.2, 0.17), body_m, line=0.018, seg=24)
for i, a in enumerate((-0.5, 0, 0.5)):                          # tail fan
    blob(f"fan{i}", (X0 + math.sin(a) * 0.5, 0.95 + math.cos(a) * 0.25, 0.75), (0.28, 0.12, 0.42), claw_m,
         rot=(0.4, 0, -a), line=0.018, seg=24)
# the one huge claw (the creature's right side), raised
tube("arm", [(X0 - 0.85, -0.1, 1.0), (X0 - 1.35, -0.25, 1.35), (X0 - 1.6, -0.35, 1.85)], 0.14, body_m)
blob("claw", (X0 - 1.7, -0.4, 2.2), (0.62, 0.5, 0.66), claw_m, rot=(0.1, 0.2, 0.1))
tube("dactyl", [(X0 - 1.95, -0.42, 2.7), (X0 - 2.05, -0.44, 3.2), (X0 - 1.8, -0.45, 3.6)], 0.2, claw_m)
tube("fixed", [(X0 - 1.35, -0.42, 2.65), (X0 - 1.15, -0.44, 3.05), (X0 - 1.25, -0.45, 3.35)], 0.15, claw_m)
blob("claw_spot", (X0 - 1.95, -0.86, 2.1), (0.17, 0.05, 0.17), belly_m, line=0.0, seg=16)
blob("claw_spot2", (X0 - 1.6, -0.88, 2.45), (0.09, 0.04, 0.09), belly_m, line=0.0, seg=16)

# ------------------------------------------------------------------ the meadow, the crater, the forest it erased
grass_m, dirt_m, rock_m = toon("grass", hexc("#7ccf6a")), toon("dirt", hexc("#a5774f")), toon("rock", hexc("#b9b2c4"))
leaf_ms = [toon("leaf0", hexc("#4fb35a")), toon("leaf1", hexc("#ffb347")), toon("leaf2", hexc("#ff8fa3")),
           toon("leaf3", hexc("#3f9e6a"))]
trunk_m = toon("trunk", hexc("#8a5a3b"))
bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0))
finish(bpy.context.object, grass_m, 0)
blob("crater", (0, 0.2, -0.02), (4.2, 3.6, 0.06), toon("scorch", hexc("#6e4a35")), line=0.0, seg=64)
bpy.ops.mesh.primitive_torus_add(major_radius=4.2, minor_radius=0.42, location=(0, 0.2, 0.0))
rim = bpy.context.object
rim.scale = (1.0, 0.86, 0.55)
bpy.ops.object.transform_apply(scale=True)
finish(rim, dirt_m, 0.02)
crack_m = toon("crack", hexc("#3b2a24"), 1.0, 0.0)
for i in range(7):                                             # scorch cracks behind the crater only
    a = 0.12 * math.pi + i / 6 * 0.76 * math.pi
    bpy.ops.mesh.primitive_cube_add(location=(math.cos(a) * 5.0, 0.2 + math.sin(a) * 4.35, 0.01),
                                    rotation=(0, 0, a))
    c = bpy.context.object
    c.scale = (0.55, 0.04, 0.01)
    bpy.ops.object.transform_apply(scale=True)
    finish(c, crack_m, 0)
import random
random.seed(4)
for i in range(18):                                            # crater rim rocks
    a = i / 18 * 2 * math.pi + random.uniform(-0.1, 0.1)
    r = random.uniform(3.9, 4.6)
    s = random.uniform(0.25, 0.55)
    blob(f"rock{i}", (math.cos(a) * r, 0.2 + math.sin(a) * r * 0.86, s * 0.3), (s, s * 0.8, s * 0.6), rock_m,
         rot=(random.random(), random.random(), random.random()), line=0.02, seg=12)
tuft_ms = [toon("tuft0", hexc("#5fbf55")), toon("tuft1", hexc("#8edc72"))]
flower_ms = [toon("fl0", hexc("#ffe066")), toon("fl1", hexc("#ff8fb1")), toon("fl2", hexc("#ffffff"))]
random.seed(9)
for i in range(160):                                           # grass tufts and flower dots outside the crater
    x, y = random.uniform(-9, 9), random.uniform(-6, 14)
    if (x / 4.9) ** 2 + ((y - 0.2) / 4.3) ** 2 < 1:
        continue
    if random.random() < 0.75:
        bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.12, depth=0.35, location=(x, y, 0.17))
        finish(bpy.context.object, random.choice(tuft_ms), 0.0)
    else:
        blob(f"fl{i}", (x, y, 0.12), (0.1, 0.1, 0.06), random.choice(flower_ms), line=0.012, seg=10)
for i in range(10):                                            # broken stumps
    a = random.uniform(0.15 * math.pi, 0.85 * math.pi)        # behind the creature only
    r = random.uniform(5.2, 8)
    bpy.ops.mesh.primitive_cylinder_add(radius=random.uniform(0.18, 0.3), depth=random.uniform(0.3, 0.8),
                                        location=(math.cos(a) * r, 2 + math.sin(a) * r, 0.2), vertices=12)
    finish(bpy.context.object, trunk_m, 0.02)
for i in range(70):                                            # the surviving forest, far behind
    x = random.uniform(-22, 22)
    y = random.uniform(13, 40)
    s = random.uniform(1.1, 2.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * s, depth=1.2 * s, location=(x, y, 0.6 * s), vertices=10)
    finish(bpy.context.object, trunk_m, 0.02)
    blob(f"tree{i}", (x, y, 1.9 * s), (1.1 * s, 1.1 * s, 1.0 * s), random.choice(leaf_ms), line=0.03, seg=16)
smoke_m = bpy.data.materials.new("smoke")
smoke_m.use_nodes = True
sb = smoke_m.node_tree.nodes["Principled BSDF"]
sb.inputs["Base Color"].default_value = hexc("#f2ece6")
sb.inputs["Alpha"].default_value = 0.4
smoke_m.surface_render_method = "BLENDED" if hasattr(smoke_m, "surface_render_method") else None
for i in range(9):                                             # puffs of smoke rising behind the creature
    a = random.uniform(0.1 * math.pi, 0.9 * math.pi)
    r = random.uniform(2.6, 4.2)
    s = random.uniform(0.35, 0.7)
    blob(f"smoke{i}", (math.cos(a) * r, 0.5 + math.sin(a) * r, 0.5 + random.uniform(0, 2.2)), (s, s, s * 0.8),
         smoke_m, line=0.0, seg=16)

# ------------------------------------------------------------------ light, sky, camera
w = bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
wn = w.node_tree
bg = wn.nodes["Background"]
bg.inputs[0].default_value = hexc("#bfe6ff")
bg.inputs[1].default_value = 0.45
sky = wn.nodes.new("ShaderNodeBackground")
sky.inputs[0].default_value = hexc("#8fd3ff")
sky.inputs[1].default_value = 1.0
lp = wn.nodes.new("ShaderNodeLightPath")
mix = wn.nodes.new("ShaderNodeMixShader")
wn.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
wn.links.new(bg.outputs[0], mix.inputs[1])
wn.links.new(sky.outputs[0], mix.inputs[2])
wn.links.new(mix.outputs[0], wn.nodes["World Output"].inputs[0])
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), 0, math.radians(-35)))
sun = bpy.context.object
sun.data.energy = 4.5
sun.data.angle = math.radians(3)
bpy.ops.object.camera_add(location=(-0.6, -10.5, 3.4), rotation=(math.radians(78), 0, math.radians(-4)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 42
cam.data.dof.use_dof = True
cam.data.dof.focus_object = body
cam.data.dof.aperture_fstop = 4.0

r = sc.render
r.resolution_x, r.resolution_y = W, H
r.filepath = OUT
sc.view_settings.view_transform = "Standard"
if LOOK == "toon":
    r.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [e.identifier for e in
                                                               bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = 16
    if hasattr(sc.eevee, "use_shadows"):
        sc.eevee.use_shadows = True
    sun.data.use_shadow = True
else:
    r.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.cycles.use_denoising = True
    sc.view_settings.view_transform = "AgX"
t = time.time()
bpy.ops.render.render(write_still=True)
print("RENDER_SECONDS %.1f engine=%s" % (time.time() - t, r.engine))
