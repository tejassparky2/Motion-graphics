"""The 2.5D game-diorama look (owner, 31 Oct 2026: "Go for 2.5d", then chose "Diorama 2.5D (game look)" and "Style test
first"). A tilted top-down "toy world": a long lens far away, tilt-shift depth of field (a sharp band through the
subject, the near and far ground melting into blur), warm low sun with long soft shadows, haze toward the far edge,
bloom on the glows. The reference is the owner's top-down low-poly forest Short (reports/Monster tamer anime pipeline
and hooks.md, "living diorama"); its HUD is NOT copied (no HUD in this series).

    setup()                          render settings, world, sun, mist pass + compositor (haze, bloom)
    camera(name, target, ...)        a tilted diorama camera with tilt-shift DOF focused on `target`
    island(seed)                     a forest island: a clearing with the puddle at the origin, a ring of painted trees
    stumps(spots, origin)            the trees as hot-cut stumps (the "after" state), slanted toward `origin`
    blast_spots(spots, origin, ...)  which spots the snap erases: a fan from `origin` toward +Y

Units as everywhere in this series: 1 unit = 20 cm, Kai ~8.7 units, the shrimp 2 units, trees 25-35 units tall. The
creature stands near the origin facing -Y; the diorama camera sits south (-Y) and above, looking north and down.
"""
import math
import random

import bpy
from mathutils import Vector

from . import look, meadow, paintbg

TREE = meadow.TREE
HAZE = "#d9ecf6"          # far-edge haze colour (pale sky blue, a little warm in the grade)
SUN_WARM = "#ffdcae"      # low golden sun


def setup(samples=24, sun_elev=34, sun_azim=-50, haze=0.55, bloom=0.6):
    """EEVEE scene for the diorama: Standard view (painted colours stay true), warm low sun with soft shadows, a pale
    sky fill so shadows stay blue, mist pass -> haze toward the far edge, bloom on glows (stump cuts, the flash)."""
    sc0 = bpy.context.scene
    w, h = sc0.render.resolution_x, sc0.render.resolution_y     # keep render_shot.py's --scale
    sc = look.render_setup(w if w > 8 else 720, h if h > 8 else 1280,
                           samples=max(samples, getattr(sc0.eevee, "taa_render_samples", 0)))
    look.world(sky="#7cc3f0", horizon="#e4f3fb", fill="#c4e2ff", fill_strength=0.65)
    s = look.sun(elev=sun_elev, azim=sun_azim, energy=4.2, color=SUN_WARM)
    s.data.angle = math.radians(5)                              # soft, long shadows: the toy-table look
    ee = sc.eevee
    for attr, val in (("use_gtao", True), ("gtao_distance", 6.0), ("use_soft_shadows", True),
                      ("bokeh_max_size", 60.0), ("use_shadow_jitter_viewport", False)):
        if hasattr(ee, attr):
            setattr(ee, attr, val)
    vl = sc.view_layers[0]
    vl.use_pass_mist = True
    sc.world.mist_settings.start = 0.0
    sc.world.mist_settings.depth = 1.0                         # set per camera in camera() (the far edge of the island)
    sc.world.mist_settings.falloff = "QUADRATIC"
    _compositor(sc, haze, bloom)
    return sc


def _compositor(sc, haze, bloom):
    sc.use_nodes = True
    nt = sc.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers")
    ramp = nt.nodes.new("CompositorNodeValToRGB")              # mist -> haze amount (none in the sharp band)
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (haze, haze, haze, 1)
    mix = nt.nodes.new("CompositorNodeMixRGB")
    mix.blend_type = "MIX"
    mix.inputs[2].default_value = look.hexc(HAZE)
    nt.links.new(rl.outputs["Mist"], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], mix.inputs[0])
    nt.links.new(rl.outputs["Image"], mix.inputs[1])
    out = mix.outputs[0]
    if bloom > 0:
        g = nt.nodes.new("CompositorNodeGlare")
        g.glare_type = "BLOOM" if "BLOOM" in [i.identifier for i in g.bl_rna.properties["glare_type"].enum_items] \
            else "FOG_GLOW"
        g.quality = "MEDIUM"
        if hasattr(g, "threshold"):
            g.threshold = 0.9
        g.mix = -1 + bloom                                     # -1 = image only, 0 = even mix
        if hasattr(g, "size"):
            g.size = 7
        nt.links.new(out, g.inputs[0])
        out = g.outputs[0]
    comp = nt.nodes.new("CompositorNodeComposite")
    nt.links.new(out, comp.inputs[0])


def camera(name, target, dist=200.0, tilt=48.0, yaw=0.0, lens=85.0, blur=14.0, frame=1, haze=(0.97, 0.55)):
    """A diorama camera `dist` units from `target`, `tilt` degrees above the ground plane, `yaw` degrees around Z
    (0 = from the south, looking north). Tilt-shift: DOF focused exactly on `target`, with the f-stop solved so that
    ground 25 % farther than the subject blurs by `blur` pixels at full res (the scene is in metres to Blender, so a
    "miniature" needs a tiny f-stop: ~0.02 at 200 units). Haze starts at haze[0] x the subject distance and is full
    by (haze[0] + haze[1]) x, so the subject stays clear and the far forest melts. A timeline marker binds the camera
    to `frame`."""
    sc = bpy.context.scene
    t = Vector(target)
    el, az = math.radians(tilt), math.radians(yaw)
    pos = t + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam_data = bpy.data.cameras.new(name)
    c = bpy.data.objects.new(name, cam_data)
    sc.collection.objects.link(c)
    c.location = pos
    c.rotation_euler = (t - pos).to_track_quat("-Z", "Y").to_euler()
    cam_data.lens = lens
    cam_data.sensor_fit = "AUTO"
    cam_data.clip_start = 1.0
    cam_data.clip_end = dist * 6
    cam_data.dof.use_dof = True
    cam_data.dof.focus_distance = dist
    cam_data.dof.aperture_fstop = fstop_for(dist, lens, blur)      # blur is in full-res (1280) pixels
    sc.world.mist_settings.start = dist * haze[0]
    sc.world.mist_settings.depth = dist * haze[1]
    sc.world.mist_settings.falloff = "LINEAR"
    mk = sc.timeline_markers.new(name, frame=frame)
    mk.camera = c
    if frame <= sc.frame_start or sc.camera is None:
        sc.camera = c
    return c


def fstop_for(dist, lens=85.0, blur=14.0, height_px=1280):
    """The f-stop that blurs ground at 1.25 x `dist` by `blur` pixels (thin lens; the 36 mm sensor fits the 9:16
    frame's height). Call again after changing a camera's distance to keep the miniature look constant."""
    f = lens / 1000.0
    coc = blur * 0.036 / height_px
    return max(0.001, f * f / (5.0 * dist * coc))


def island(seed=31, clear_r=26.0, forest_r=105.0, puddle=True, flowers=True):
    """A forest island in a sea of grass: a round clearing (radius `clear_r`) with the puddle by the origin and a ring
    of painted trees out to `forest_r`. Deterministic for a seed, so every shot of the test shares the same trees.
    Returns dict(trees=[(trunk, canopy)], spots=[(x, y, h, r, variant)], puddle=obj or None)."""
    _ground(clear_r)
    rnd = random.Random(seed)
    spots = []
    tries = 0
    while tries < 4000:
        tries += 1
        a = rnd.uniform(0, 2 * math.pi)
        d = math.sqrt(rnd.uniform(clear_r ** 2, forest_r ** 2))
        x, y = math.cos(a) * d, math.sin(a) * d
        r = rnd.uniform(2.1, 2.9) * TREE
        if any(math.hypot(x - sx, y - sy) < (r + sr) * 0.78 for sx, sy, _, sr, _ in spots):
            continue
        spots.append((x, y, rnd.uniform(5.2, 7.6) * TREE, r, len(spots) % 4))
    out = dict(trees=[], spots=spots, puddle=None)
    for i, (x, y, h, r, v) in enumerate(spots):
        out["trees"].append(paintbg.tree((x, y, 0), height=h, radius=r, seed=500 + i, variant=v))
    if puddle:
        out["puddle"] = pond()
    if flowers:
        meadow._flowers(2.6, seed=seed, n=60)
    return out


def pond(center=(0.1, -2.6), size=(4.2, 2.3), seed=3):
    """The puddle at diorama scale (the plot device: the claw only works wet), bigger than the meadow's so it reads
    from above, with a ring of pebbles and two white glints. Returns the water object."""
    water = meadow._puddle(center=center, size=size, z=0.015, pebbles=False)
    rock = paintbg.paint3("pebble", look.hexc("#7f7a92"), look.hexc("#aaa6bd"), look.hexc("#d6d3e3"), noise=0.1)
    rnd = random.Random(seed)
    for i in range(16):
        a = i / 16 * 2 * math.pi + rnd.uniform(-0.15, 0.15)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, location=(
            center[0] + math.cos(a) * size[0] * 1.08, center[1] + math.sin(a) * size[1] * 1.12, 0.08))
        o = bpy.context.object
        sz = rnd.uniform(0.18, 0.34)
        o.scale = (sz * 1.3, sz, sz * 0.7)
        o.data.materials.append(rock)
    return water


def _ground(clear_r=26.0):
    bpy.ops.mesh.primitive_plane_add(size=3000)
    g = bpy.context.object
    g.name = "diorama_ground"
    g.data.materials.append(grass_lit(clear_r=clear_r))
    return g


def grass_lit(name="diorama_grass", clear_r=26.0):
    """Painted grass that TAKES LIGHT: the three brush-stroke greens of paintbg.grass_material, multiplied by a two-tone
    light ramp (cool blue-green in shadow, warm in sun) so the trees cast long soft shadows on the ground (the toy-table
    read). Near the origin the grass thins to a trodden, sandy-green clearing with a soft noisy edge."""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    N = nt.nodes.new
    out = N("ShaderNodeOutputMaterial")
    tc = N("ShaderNodeTexCoord")
    mp = N("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.35, 3.0, 1.0)
    nz = N("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 4.0
    nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.65
    grass = N("ShaderNodeValToRGB")
    cr = grass.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, look.hexc("#2f9a3a")
    cr.elements[1].position, cr.elements[1].color = 0.44, look.hexc("#4cc24a")
    e3 = cr.elements.new(0.6)
    e3.color = look.hexc("#86de5c")
    L(tc.outputs["Object"], mp.inputs[0])
    L(mp.outputs[0], nz.inputs[0])
    L(nz.outputs["Fac"], grass.inputs[0])
    # the clearing: distance from the origin (object space = world here), broken by a big soft noise
    ln = N("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    L(tc.outputs["Object"], ln.inputs[0])
    nz2 = N("ShaderNodeTexNoise")
    nz2.inputs["Scale"].default_value = 0.06
    nz2.inputs["Detail"].default_value = 3.0
    madd = N("ShaderNodeMath")
    madd.operation = "MULTIPLY_ADD"                            # length + noise * clear_r * 0.6
    madd.inputs[1].default_value = clear_r * 0.6
    L(nz2.outputs["Fac"], madd.inputs[0])
    L(ln.outputs["Value"], madd.inputs[2])
    edge = N("ShaderNodeMapRange")
    edge.inputs["From Min"].default_value = clear_r * 0.55
    edge.inputs["From Max"].default_value = clear_r * 0.95
    L(madd.outputs[0], edge.inputs["Value"])
    trod = N("ShaderNodeMixRGB")
    trod.inputs[1].default_value = look.hexc("#b9c97a")         # sandy, trodden green
    L(edge.outputs["Result"], trod.inputs[0])
    L(grass.outputs[0], trod.inputs[2])
    # light: diffuse -> Shader to RGB -> two tones with a soft edge
    dif = N("ShaderNodeBsdfDiffuse")
    s2r = N("ShaderNodeShaderToRGB")
    bw = N("ShaderNodeRGBToBW")
    tone = N("ShaderNodeValToRGB")
    t = tone.color_ramp
    t.interpolation = "EASE"
    t.elements[0].position, t.elements[0].color = 0.55, (0.50, 0.62, 0.78, 1)
    t.elements[1].position, t.elements[1].color = 0.85, (1.08, 1.02, 0.92, 1)
    L(dif.outputs[0], s2r.inputs[0])
    L(s2r.outputs[0], bw.inputs[0])
    L(bw.outputs[0], tone.inputs[0])
    mul = N("ShaderNodeMixRGB")
    mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    L(trod.outputs[0], mul.inputs[1])
    L(tone.outputs[0], mul.inputs[2])
    em = N("ShaderNodeEmission")
    L(mul.outputs[0], em.inputs[0])
    L(em.outputs[0], out.inputs[0])
    return m


def blast_spots(spots, origin=(0.0, 0.0), half_angle=34.0, reach=None):
    """The snap's fan: the spots within `half_angle` degrees of +Y from `origin` (and within `reach`, if given). The
    shrimp faces -Y in the meadow shots, but its claw fires toward +Y (the forest behind it), as in S15."""
    ox, oy = origin
    out = []
    for i, (x, y, h, r, v) in enumerate(spots):
        ang = math.degrees(math.atan2(x - ox, y - oy))         # 0 = straight +Y
        if abs(ang) <= half_angle and (reach is None or math.hypot(x - ox, y - oy) <= reach):
            out.append(i)
    return out


def stumps(spots, origin=(0.0, 0.0)):
    """Hot-cut stumps where `spots` stood (the "after" state): the slanted cut faces the blast origin and glows."""
    bark = paintbg.paint3("stump_bark", look.hexc("#3c261c"), look.hexc("#5e3e2c"), look.hexc("#80604a"), noise=0.12)
    ring = look.flat("stump_hot", look.hexc("#ff7a3d"))
    core = look.flat("stump_core", look.hexc("#ffe08a"))
    rnd = random.Random(77)
    out = []
    for (x, y, h, r, v) in spots:
        sh = rnd.uniform(0.6, 1.5) * TREE * 0.6
        yaw = math.atan2(y - origin[1], x - origin[0]) - math.pi / 2
        out.append(meadow._slice((x, y, 0), r * 0.17, sh, math.radians(rnd.uniform(28, 40)), yaw, bark, ring, core))
    return out
