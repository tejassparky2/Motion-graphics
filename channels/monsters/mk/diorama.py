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

# The one other-world map (units; +Y is north, away from the default camera). Every diorama shot uses these spots so the
# world stays the same place from shot to shot. The clearing is ringed by forest; a dirt path leaves it to the south,
# through the trees, into the open flower meadow where Kai wakes (S09) and meets the jelly-snail and the fluffmoth.
MAP = dict(
    pond=(0.1, -2.6),          # the puddle at diorama scale (diorama.pond)
    shrimp=(0.1, 0.4),         # where the puff-shrimp drinks (north edge of the pond)
    kai_down=(1.5, -9.0),      # where the blast throws Kai on his back (S15 D4 -> S16-S21)
    thorn=(19.0, 9.0),         # the thorn tree at the clearing's north-east edge (S22-S24)
    path=((0.0, -24.0), (-6.0, -60.0), (4.0, -95.0), (0.0, -118.0)),   # clearing -> meadow (a gap in the trees)
    wake=(8.0, -140.0),        # S09: Kai wakes in the flower meadow
    snail=(-16.0, -132.0),     # S10a/S11a: the jelly-snail and its burnt-hole trail
    moth=(20.0, -128.0),       # S10b/S11b: the fluffmoth
)


def setup(samples=24, sun_elev=34, sun_azim=-50, haze=0.55, bloom=0.6):
    """EEVEE scene for the diorama: Standard view (painted colours stay true), warm low sun with soft shadows, a pale
    sky fill so shadows stay blue, mist pass -> haze toward the far edge, bloom on glows (stump cuts, the flash)."""
    sc0 = bpy.context.scene
    w, h = sc0.render.resolution_x, sc0.render.resolution_y     # keep render_shot.py's --scale
    if (w, h) == (1920, 1080) or w < 8:                           # factory default: the Shorts frame
        w, h = 720, 1280
    sc = look.render_setup(w, h,
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


def sunbeam(target, radius=7.0, dist=40.0, strength=1.0):
    """A warm pool of sunlight through a gap in the canopy onto `target` (the forest's long shadows cover the south of
    the clearing in the low sun, where Kai lies after the snap): a soft spot placed along the scene sun's own direction,
    so its shadows agree with the sun's. `radius` is the pool's radius at the target (soft edge). Every shot of Kai at
    MAP["kai_down"] (S15's D5 to S21) calls it on his chest, so the light on him matches across the cuts."""
    sun = next((o for o in bpy.context.scene.objects if o.type == "LIGHT" and o.data.type == "SUN"), None)
    if sun is not None:
        bpy.context.view_layer.update()
        d = (sun.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()
    else:
        d = Vector((0.635, 0.533, -0.559))                     # setup()'s default sun (elev 34, azim -50)
    t = Vector(target)
    bpy.ops.object.light_add(type="SPOT", location=t - d * dist)
    sp = bpy.context.object
    sp.name = "sunbeam"
    sp.data.energy = 26000.0 * strength * (dist / 34.6) ** 2   # the same light on the target at any distance
    sp.data.color = look.hexc(SUN_WARM)[:3]
    sp.data.spot_size = 2 * math.atan(radius / dist)
    sp.data.spot_blend = 0.6
    sp.data.shadow_soft_size = 1.5
    sp.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return sp


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


def island(seed=31, clear_r=26.0, forest_r=105.0, puddle=True, flowers=True, thorn=True, meadow_flowers=True,
           skip=()):
    """THE other-world set (every diorama shot, seed 31): a round clearing (radius `clear_r`) with the pond by the
    origin, a ring of painted trees out to `forest_r`, a dirt path south through the trees to an open flower meadow
    (MAP), rocks and bushes, the thorn tree at MAP["thorn"]. `skip`: spot indexes to leave out (e.g. the trees the snap
    erased, for the "after" state). Deterministic for a seed. Returns dict(trees=[(trunk, canopy) or None per spot],
    spots=[(x, y, h, r, variant)], puddle=obj or None, thorn=thornbush dict or None)."""
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
        if _near_path(x, y, r * 0.9 + 7.0) or math.hypot(x - MAP["thorn"][0], y - MAP["thorn"][1]) < r + 6:
            continue
        if any(math.hypot(x - sx, y - sy) < (r + sr) * 0.78 for sx, sy, _, sr, _ in spots):
            continue
        spots.append((x, y, rnd.uniform(5.2, 7.6) * TREE, r, len(spots) % 4))
    out = dict(trees=[], spots=spots, puddle=None, thorn=None)
    for i, (x, y, h, r, v) in enumerate(spots):
        out["trees"].append(None if i in skip else paintbg.tree((x, y, 0), height=h, radius=r, seed=500 + i,
                                                                 variant=v))
    path_strip()
    _dressing(seed, clear_r)
    if puddle:
        out["puddle"] = pond(center=MAP["pond"])
    if flowers:
        meadow._flowers(2.6, seed=seed, n=60)
    if meadow_flowers:
        _meadow_flowers(seed)
    if thorn:
        from . import thornbush
        out["thorn"] = thornbush.build(loc=(MAP["thorn"][0], MAP["thorn"][1], 0.0))
    return out


def _path_x(y):
    """The path's centre line: x at a given y (piecewise linear through MAP["path"])."""
    pts = MAP["path"]
    if y >= pts[0][1]:
        return pts[0][0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y1 <= y <= y0:
            t = (y0 - y) / (y0 - y1)
            return x0 + (x1 - x0) * t
    return pts[-1][0]


def _near_path(x, y, w):
    return MAP["path"][-1][1] - 10 <= y <= MAP["path"][0][1] + 4 and abs(x - _path_x(y)) < w


def path_strip(width=5.5):
    """The dirt path as a flat ribbon just above the grass (lit, so tree shadows fall across it)."""
    import bmesh
    dirt = lit_paint("path_dirt", "#8a6a48", "#b48c5e", "#d9b583")
    me = bpy.data.meshes.new("path")
    bm = bmesh.new()
    y0, y1 = MAP["path"][0][1] + 2, MAP["path"][-1][1] - 8
    n = 60
    rows = []
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        w = width * (1.0 + 0.25 * math.sin(i * 0.9))
        x = _path_x(y)
        rows.append((bm.verts.new((x - w / 2, y, 0.02)), bm.verts.new((x + w / 2, y, 0.02))))
    for (a, b), (c, d) in zip(rows, rows[1:]):
        bm.faces.new((a, b, d, c))
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("path", me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(dirt)
    return o


def lit_paint(name, dark, mid, light):
    """paintbg.paint3 (three painted bands driven by the light, so it takes shadows) from hex colours."""
    return paintbg.paint3(name, look.hexc(dark), look.hexc(mid), look.hexc(light), noise=0.2, scale=1.2)


def _dressing(seed, clear_r):
    """Rocks and round bushes around the clearing's rim and along the path: the toy-table detail."""
    rnd = random.Random(seed + 5)
    rock = lit_paint("dio_rock", "#6f6a82", "#9c98b0", "#cfcbe0")
    bush = paintbg.paint3("dio_bush", *paintbg.greens(2), noise=0.15)
    spots = [(math.cos(a) * clear_r * rnd.uniform(0.85, 1.05), math.sin(a) * clear_r * rnd.uniform(0.85, 1.05))
             for a in [rnd.uniform(0, 2 * math.pi) for _ in range(16)]]
    spots += [(_path_x(y) + rnd.choice((-1, 1)) * rnd.uniform(4.0, 6.5), y) for y in
              [rnd.uniform(-115, -30) for _ in range(12)]]
    for i, (x, y) in enumerate(spots):
        if _near_path(x, y, 3.2) or math.hypot(x - MAP["pond"][0], y - MAP["pond"][1]) < 9:
            continue
        if i % 3 == 0:
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(x, y, 0.4))
            o = bpy.context.object
            s = rnd.uniform(0.8, 1.6)
            o.scale = (s * 1.3, s, s * 0.7)
            o.rotation_euler = (0, 0, rnd.uniform(0, 3))
            o.data.materials.append(rock)
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=(x, y, 0.9))
            o = bpy.context.object
            s = rnd.uniform(1.3, 2.4)
            o.scale = (s * 1.25, s, s * 0.8)
            o.data.materials.append(bush)
            for p in o.data.polygons:
                p.use_smooth = True


def _meadow_flowers(seed, n=320):
    """The open flower meadow south of the forest (S09: Kai wakes in pink grass): pink, white and yellow dots."""
    rnd = random.Random(seed + 9)
    cols = [paintbg.paint3(f"mflower{j}", *(look.hexc(c) for c in cs), noise=0.05) for j, cs in enumerate((
        ("#d05a8a", "#ff8fb8", "#ffd0e2"), ("#d05a8a", "#ff8fb8", "#ffd0e2"), ("#c9c9e0", "#ffffff", "#ffffff"),
        ("#d9a400", "#ffd23f", "#fff2a8")))]
    for _ in range(n):
        x, y = rnd.uniform(-60, 60), rnd.uniform(-175, -108)
        if _near_path(x, y, 3.5):
            continue
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, location=(x, y, 0.12))
        o = bpy.context.object
        s = rnd.uniform(0.22, 0.4)
        o.scale = (s, s, s * 0.6)
        o.data.materials.append(rnd.choice(cols))


def pond(center=MAP["pond"], size=(4.2, 2.3), seed=3):
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
