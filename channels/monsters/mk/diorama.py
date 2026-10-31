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
    shrimp_drink=(4.2, -0.1),  # v3, S21's end to S24: drinking on the pond's north-east shore, facing SHRIMP_DRINK_YAW
    kai_down=(1.5, -9.0),      # where the blast throws Kai on his back (S15 D4 -> S16-S21)
    thorn=(19.0, 9.0),         # the thorn tree at the clearing's north-east edge (S22-S24)
    path=((0.0, -24.0), (-6.0, -60.0), (4.0, -95.0), (0.0, -118.0)),   # clearing -> meadow (a gap in the trees)
    wake=(8.0, -140.0),        # S09: Kai wakes in the flower meadow
    snail=(-16.0, -132.0),     # S10a/S11a: the jelly-snail and its burnt-hole trail
    moth=(20.0, -128.0),       # S10b/S11b: the fluffmoth
    kai_kneel=(1.0, -6.4),     # v3 S15a-S15: Kai on his knees at the pond's south edge (his hips), facing the shrimp
    blast=(-0.72, -0.71),      # v3 S15: the claw's muzzle at the snap (helper 10, measured); the shot passes his left ear
)
SHRIMP_DRINK_YAW = 0.0     # degrees (root rotation z): facing south (-Y), its back to the thorn tree, so the bird's
                           # view from the perch sees its back; its dipped claw (the drinking pose of ep01v2/xprl.
                           # _shrimp_wet) reaches 1.7 west and 2.5 south of the root, into the water at ~(2.5, -2.6)


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


def sunbeam(target, radius=7.0, dist=30.0, elev=60.0, strength=1.0):
    """A warm pool of sunlight through a gap in the canopy onto `target` (the forest's long shadows cover the south of
    the clearing in the low sun, where Kai lies after the snap): a soft spot from the scene sun's azimuth, so its
    shadows fall the same way, but steeper (`elev`) so it shines from above the clearing instead of through the tree
    ring. `radius` is the pool's radius at the target (soft edge). Every shot of Kai at MAP["kai_down"] (S15's D5 to
    S21) calls it on his chest, so the light on him matches across the cuts."""
    sun = next((o for o in bpy.context.scene.objects if o.type == "LIGHT" and o.data.type == "SUN"), None)
    if sun is not None:
        bpy.context.view_layer.update()
        d = sun.matrix_world.to_3x3() @ Vector((0, 0, -1))
    else:
        d = Vector((0.635, 0.533, -0.559))                     # setup()'s default sun (elev 34, azim -50)
    h = Vector((d.x, d.y, 0)).normalized()
    d = (h * math.cos(math.radians(elev)) - Vector((0, 0, math.sin(math.radians(elev))))).normalized()
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
           skip=(), dressing=2, grove=False):
    """THE other-world set (every diorama shot, seed 31): a round clearing (radius `clear_r`) with the pond by the
    origin, a ring of painted trees out to `forest_r`, a dirt path south through the trees to an open flower meadow
    (MAP), rocks and bushes, the thorn tree at MAP["thorn"]. `skip`: spot indexes to leave out (e.g. the trees the snap
    erased, for the "after" state). `dressing=2` (the default since v3; 1 = the v2 island) adds the toy-table detail
    of dressing2(): mushrooms, clover, pebble-edged paths, flower clusters, logs, a stump, pond reeds, clear of every
    MAP spot and of the snap's fan. Deterministic for a seed. Returns dict(trees=[(trunk, canopy) or None per spot],
    spots=[(x, y, h, r, variant)], puddle=obj or None, thorn=thornbush dict or None, dressing=objects by kind).
    grove (v3, helper 10): True plants the young blast grove (grove_spots(), appended to spots/trees) and the sapling
    (sapling_spot(), out["sapling"]) that stand before the snap; "cut" is the after state: neither is planted (put
    stumps(grove_spots(), MAP["blast"]) and the sapling's stump in their place)."""
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
    if grove is True:
        for j, (x, y, h, r, v) in enumerate(grove_spots()):
            spots.append((x, y, h, r, v))
            out["trees"].append(paintbg.tree((x, y, 0), height=h, radius=r, seed=900 + j, variant=v))
        x, y, h, r, v = sapling_spot()
        out["sapling"] = paintbg.tree((x, y, 0), height=h, radius=r, seed=950, variant=v)
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
    if dressing >= 2:
        out["dressing"] = dressing2(seed, clear_r)
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


# --- v3: the snap fires SOUTH at Kai (helper 10, S15). The shot leaves the claw (MAP["blast"]), passes his left ear
# as he kneels (MAP["kai_kneel"]) and erases the young grove behind him along the line; its blast fan cuts the sapling
# that later stands an inch from his head (S15b on); MAP["kai_down"] is where it throws him.
BLAST_LINE = (0.51, -0.86)            # the shot's ground direction: ~31 deg east of south


def sapling_spot():
    """(x, y, h, r, variant): the young tree the snap cuts, ~1.6 units west of his head once he lies at kai_down (clear
    of him while he kneels at kai_kneel)."""
    return (-0.9, -5.5, 2.0 * TREE, 0.34 * TREE, 1)


def grove_spots():
    """[(x, y, h, r, variant)]: the young grove behind where he knelt, in a fan along BLAST_LINE (all erased by the
    snap). Smaller than the rim forest, so it reads as a stand of young trees inside the clearing."""
    dx, dy = BLAST_LINE
    px, py = -dy, dx                                            # perpendicular (east-north-east)
    x0, y0 = 2.3, -6.4                                          # the line where it passes his kneeling hips
    out = []
    for j, (s, o, h, r) in enumerate(((5.5, 2.4, 3.3, 1.05), (8.0, -2.6, 3.8, 1.15), (10.5, 2.2, 3.5, 1.1),
                                      (13.0, -1.2, 4.0, 1.2), (15.5, 3.4, 3.6, 1.1), (18.5, -2.4, 4.1, 1.25),
                                      (21.0, 1.6, 3.9, 1.2))):
        out.append((x0 + dx * s + px * o, y0 + dy * s + py * o, h * TREE, r * TREE, j % 4))
    return out


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


def _ember_mat(phase=0):
    """The stump's cut face: charred black with thin orange ember cracks (a Voronoi crack net, broken up by noise)
    that flicker on 2s (frames -60..400; three phases so neighbouring stumps don't pulse together)."""
    name = f"stump_ember{phase}"
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    tc, vor, nz = N("ShaderNodeTexCoord"), N("ShaderNodeTexVoronoi"), N("ShaderNodeTexNoise")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 3.2
    nz.inputs["Scale"].default_value = 2.5
    crack = N("ShaderNodeMapRange")                            # distance to a cell edge < 0.05: a crack
    crack.inputs["From Min"].default_value, crack.inputs["From Max"].default_value = 0.0, 0.035
    crack.inputs["To Min"].default_value, crack.inputs["To Max"].default_value = 1.0, 0.0
    gate = N("ShaderNodeMapRange")                             # only some cracks are lit
    gate.inputs["From Min"].default_value, gate.inputs["From Max"].default_value = 0.47, 0.58
    mul = N("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    char, ember, mix, out = N("ShaderNodeEmission"), N("ShaderNodeEmission"), N("ShaderNodeMixShader"), \
        N("ShaderNodeOutputMaterial")
    char.inputs["Color"].default_value = look.hexc("#1b1411")
    char.inputs["Strength"].default_value = 1.0
    ember.inputs["Color"].default_value = look.hexc("#ff7426")
    L(tc.outputs["Object"], vor.inputs["Vector"])
    L(tc.outputs["Object"], nz.inputs["Vector"])
    L(vor.outputs["Distance"], crack.inputs["Value"])
    L(nz.outputs["Fac"], gate.inputs["Value"])
    L(crack.outputs["Result"], mul.inputs[0])
    L(gate.outputs["Result"], mul.inputs[1])
    L(mul.outputs[0], mix.inputs["Fac"])
    L(char.outputs[0], mix.inputs[1])
    L(ember.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs["Surface"])
    rnd = random.Random(400 + phase)
    st = ember.inputs["Strength"]
    for f in range(-60, 401, 2):                               # the glow breathes on 2s
        st.default_value = rnd.uniform(2.2, 4.6)
        st.keyframe_insert("default_value", frame=f)
    for fc in nt.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return m


def splinter_stump(loc, radius, height, blast_from=(0.0, 0.0), seed=0, smoke=None):
    """ONE shared stump for every tree the snap cut (grove, sapling; S15 on): bark below a charred band, a jagged
    splintered top (5-7 uneven spikes, bent away from `blast_from`), a sunken cut face of char with flickering ember
    cracks; smoke=(f0, f1) adds a thin smoke wisp (its first puff no earlier than f0). Returns the stump object."""
    import bmesh
    rnd = random.Random(1000 + seed)
    x, y, z = loc
    ax, ay = x - blast_from[0], y - blast_from[1]
    al = math.hypot(ax, ay) or 1.0
    ax, ay = ax / al, ay / al                                  # away from the blast
    seg, h, r = 20, height, radius
    spikes = [(rnd.uniform(0, 2 * math.pi), rnd.uniform(0.22, 0.75) * h, rnd.uniform(0.35, 0.7))
              for _ in range(rnd.randint(5, 7))]
    bm = bmesh.new()
    rings = []
    for zr, rr in ((0.0, 1.14), (0.3, 1.04), (0.5, 1.0), (0.7, 0.98)):
        rings.append([bm.verts.new((math.cos(2 * math.pi * i / seg) * r * rr * rnd.uniform(0.97, 1.03),
                                    math.sin(2 * math.pi * i / seg) * r * rr * rnd.uniform(0.97, 1.03), zr * h))
                      for i in range(seg)])
    top = []
    for i in range(seg):
        th = 2 * math.pi * i / seg
        up = 0.0
        for a, amp, w in spikes:
            d = abs((th - a + math.pi) % (2 * math.pi) - math.pi)
            up = max(up, amp * max(0.0, 1 - d / w) ** 1.6)
        zt = h * 0.78 + up + rnd.uniform(-0.04, 0.04) * h
        rr = r * rnd.uniform(0.84, 0.98)
        bend = 0.55 * up * rnd.uniform(0.4, 1.0)              # tall splinters lean away from the blast
        top.append(bm.verts.new((math.cos(th) * rr + ax * bend, math.sin(th) * rr + ay * bend, zt)))
    rings.append(top)
    inner = [bm.verts.new((math.cos(2 * math.pi * (i + 0.5) / seg) * r * 0.55 * rnd.uniform(0.8, 1.1),
                           math.sin(2 * math.pi * (i + 0.5) / seg) * r * 0.55 * rnd.uniform(0.8, 1.1),
                           h * rnd.uniform(0.74, 0.8))) for i in range(seg)]
    centre = bm.verts.new((0, 0, h * 0.72))
    faces = []
    for k, (lo, hi) in enumerate(zip(rings, rings[1:])):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((bm.faces.new((lo[i], lo[j], hi[j], hi[i])), k))
    for i in range(seg):                                       # the cut face: rim -> inner ring -> centre
        j = (i + 1) % seg
        faces.append((bm.faces.new((top[i], top[j], inner[i])), 4))
        faces.append((bm.faces.new((inner[i], top[j], inner[j])), 4))
        faces.append((bm.faces.new((inner[i], inner[j], centre)), 4))
    for f, mi in faces:                                        # bark, scorched bark, charred band, char, cut face
        f.material_index = mi
        f.smooth = mi < 3
    bm.normal_update()
    me = bpy.data.meshes.new(f"splinter_stump{seed}")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(f"splinter_stump{seed}", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = (x, y, z)
    bark = bpy.data.materials.get("stump_bark") or paintbg.paint3(
        "stump_bark", look.hexc("#3c261c"), look.hexc("#5e3e2c"), look.hexc("#80604a"), noise=0.12)
    scorch = bpy.data.materials.get("stump_scorch") or lit_paint("stump_scorch", "#2c1c14", "#45301f", "#5e4430")
    band = bpy.data.materials.get("stump_charband") or lit_paint("stump_charband", "#1c120d", "#2e1f16", "#45301f")
    char = bpy.data.materials.get("stump_char") or lit_paint("stump_char", "#0b0807", "#16100d", "#241a14")
    for m in (bark, scorch, band, char, _ember_mat(seed % 3)):
        me.materials.append(m)
    look.outline(o, 0.02)
    if smoke:
        f0, f1 = smoke
        meadow.smoke([(x, y, z + h * 0.85)], f0 + 27, f1, every=9, rise=max(3.0, h * 2.5),
                     size=max(0.25, r * 0.45), seed=seed + 3)  # (smoke() buds up to 3 x every before its f0)
    return o


def stumps(spots, origin=(0.0, 0.0), smoke=None):
    """Splintered, smouldering stumps where `spots` stood (the "after" state): splinter_stump() per spot, its
    splinters bent away from the blast `origin`. smoke=(f0, f1) gives each a smoke wisp."""
    rnd = random.Random(77)
    out = []
    for i, (x, y, h, r, v) in enumerate(spots):
        sh = rnd.uniform(0.6, 1.5) * TREE * 0.6
        out.append(splinter_stump((x, y, 0), r * 0.17, sh, blast_from=origin, seed=i, smoke=smoke))
    return out


# --- v3 set dressing (dressing=2; helper 6, Episode 1 v3 Q2): procedural, merged into one mesh per material -----------
class _Batch:
    """Many small primitives merged into one object (one material, one draw): sphere / box / cone, then done()."""

    def __init__(self, name, mat, smooth=True):
        import bmesh
        self.name, self.mat, self.smooth, self.bm = name, mat, smooth, bmesh.new()

    def _m(self, loc, scale, rot):
        from mathutils import Euler, Matrix
        return Matrix.LocRotScale(Vector(loc), Euler(rot), Vector(scale))

    def sphere(self, loc, scale, rot=(0, 0, 0), seg=10):
        import bmesh
        bmesh.ops.create_uvsphere(self.bm, u_segments=seg, v_segments=max(4, seg // 2), radius=1.0,
                                  matrix=self._m(loc, scale, rot))

    def box(self, loc, size, rot=(0, 0, 0)):
        import bmesh
        bmesh.ops.create_cube(self.bm, size=1.0, matrix=self._m(loc, size, rot))

    def cone(self, loc, r1, r2, depth, rot=(0, 0, 0), seg=8):
        import bmesh
        bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2,
                              depth=depth, matrix=self._m(loc, (1, 1, 1), rot))

    def done(self):
        if not self.bm.verts:
            self.bm.free()
            return None
        me = bpy.data.meshes.new(self.name)
        self.bm.to_mesh(me)
        self.bm.free()
        o = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(self.mat)
        if self.smooth:
            o.data.polygons.foreach_set("use_smooth", [True] * len(o.data.polygons))
        return o


def _keep_clear(x, y, clear_r, fan=40.0):
    """True where dressing must NOT go: the pond, the path, the story spots (MAP), and the snap's fan toward +Y (its
    trees become stumps in the "after" state, so nothing there may survive the blast)."""
    if _near_path(x, y, 3.4):
        return True
    for key, r in (("pond", 7.5), ("shrimp", 4.0), ("shrimp_drink", 4.0), ("kai_down", 8.0), ("thorn", 9.0),
                   ("wake", 7.0), ("snail", 13.0), ("moth", 6.0)):
        if key in MAP and math.hypot(x - MAP[key][0], y - MAP[key][1]) < r:
            return True
    if _near_grove(x, y):
        return True
    d = math.hypot(x, y)
    return d > 4.0 and abs(math.degrees(math.atan2(x, y))) < fan and d < 112.0


def _near_grove(x, y, margin=3.5):
    """True near helper 10's v3 blast grove (grove_spots(): young trees south of the kneel spot, flanking the path's
    mouth) or the sapling by Kai's head (sapling_spot()), whenever those are defined in this module."""
    spots = list(globals()["grove_spots"]()) if "grove_spots" in globals() else []
    if "sapling_spot" in globals():
        spots.append(globals()["sapling_spot"]())
    for sp in spots:
        r = (sp[3] if len(sp) > 3 else 1.5) + margin               # (x, y[, h, r, ...]) like island()'s spots
        if math.hypot(x - sp[0], y - sp[1]) < r:
            return True
    return False


def dressing2(seed=31, clear_r=26.0):
    """The v3 toy-table detail for the island (procedural): mushroom clusters, clover patches, pebbles lining the dirt
    path, flower clusters in the clearing and the meadow, two mossy logs, an old stump, reeds at the pond. Returns the
    merged objects by kind."""
    rnd = random.Random(seed + 301)
    P = lit_paint
    m = dict(
        stem=P("d2_stem", "#c9b79a", "#efe2c8", "#fff7e6"),
        cap_red=P("d2_cap_red", "#a8382f", "#d9584a", "#f08a74"), cap_tan=P("d2_cap_tan", "#a8865c", "#d4b083",
                                                                             "#f0d6ac"),
        cap_lilac=P("d2_cap_lilac", "#7c5ea8", "#b48cd8", "#dcc4f4"),
        spot=P("d2_spot", "#d8d2c8", "#ffffff", "#ffffff"),
        clover=P("d2_clover", "#1d5a26", "#2f7d34", "#55a84a"), clover2=P("d2_clover2", "#25652a", "#3a8a3a",
                                                                           "#64b450"),
        pebble=P("d2_pebble", "#7d7768", "#a9a291", "#d6cfbd"), pebble2=P("d2_pebble2", "#6c6f80", "#9a9cb0",
                                                                           "#c8c9da"),
        pink=P("d2_pink", "#d05a8a", "#ff8fb8", "#ffd0e2"), white=P("d2_white", "#c9c9e0", "#ffffff", "#ffffff"),
        yellow=P("d2_yellow", "#d9a400", "#ffd23f", "#fff2a8"), blue=P("d2_blue", "#4f6fc0", "#7d9cf0", "#bcd0ff"),
        bark=P("d2_bark", "#4a3424", "#6e4e36", "#8f6b4c"), cut=P("d2_cut", "#a8865c", "#d4b083", "#f0d6ac"),
        moss=P("d2_moss", "#3d7a2c", "#5ea540", "#8fd062"), reed=P("d2_reed", "#4a7a3a", "#6aa24e", "#9ccb72"),
        cattail=P("d2_cattail", "#4a3020", "#6b4630", "#8c6244"))
    B = {k: _Batch(f"d2_{k}", v) for k, v in m.items()}

    def spot(rmin, rmax, tries=60):
        for _ in range(tries):
            a = rnd.uniform(0, 2 * math.pi)
            d = rnd.uniform(rmin, rmax)
            x, y = math.cos(a) * d, math.sin(a) * d
            if not _keep_clear(x, y, clear_r):
                return x, y
        return None

    def meadow_spot(tries=60):
        for _ in range(tries):
            x, y = rnd.uniform(-55, 55), rnd.uniform(-172, -110)
            if not _keep_clear(x, y, clear_r):
                return x, y
        return None

    def path_side(tries=60):
        for _ in range(tries):
            y = rnd.uniform(-116, -26)
            x = _path_x(y) + rnd.choice((-1, 1)) * rnd.uniform(4.2, 9.0)
            if not _keep_clear(x, y, clear_r):
                return x, y
        return None

    # mushrooms: clusters of 2-5 toy mushrooms, mostly red-and-white or tan, a rare lilac
    where = [spot(clear_r * 0.72, clear_r * 1.02) for _ in range(14)] + [path_side() for _ in range(10)] + \
        [meadow_spot() for _ in range(8)]
    for c in [w for w in where if w]:
        cap = rnd.choices(("cap_red", "cap_tan", "cap_lilac"), weights=(5, 4, 1))[0]
        for _ in range(rnd.randint(2, 5)):
            x, y = c[0] + rnd.uniform(-1.4, 1.4), c[1] + rnd.uniform(-1.4, 1.4)
            h, r = rnd.uniform(0.6, 1.6), rnd.uniform(0.45, 1.0)
            B["stem"].cone((x, y, h / 2), r * 0.32, r * 0.24, h)
            B[cap].sphere((x, y, h), (r, r, r * 0.62), seg=14)
            if cap == "cap_red":
                for k in range(4):
                    a = rnd.uniform(0, 2 * math.pi)
                    B["spot"].sphere((x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55, h + r * 0.42),
                                     (r * 0.16, r * 0.16, r * 0.06), seg=8)
    # clover patches: trefoils (three round leaves) in tight clumps
    for _ in range(46):
        c = spot(5.0, clear_r * 0.95) if rnd.random() < 0.55 else meadow_spot()
        if not c:
            continue
        mat = rnd.choice(("clover", "clover2"))
        for _ in range(rnd.randint(6, 12)):
            x, y = c[0] + rnd.uniform(-1.3, 1.3), c[1] + rnd.uniform(-1.0, 1.0)
            r, a0 = rnd.uniform(0.17, 0.26), rnd.uniform(0, 2 * math.pi)
            for k in range(3):
                a = a0 + k * 2 * math.pi / 3
                B[mat].sphere((x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9, 0.06), (r, r, r * 0.3), seg=8)
    # pebbles lining both edges of the dirt path
    y = MAP["path"][0][1] + 1.0
    while y > MAP["path"][-1][1] - 7.0:
        for side in (-1, 1):
            x = _path_x(y) + side * rnd.uniform(2.9, 3.6)
            s = rnd.uniform(0.28, 0.55)
            if _near_grove(x, y, 1.0):
                continue
            B[rnd.choice(("pebble", "pebble2"))].sphere((x, y + rnd.uniform(-0.3, 0.3), s * 0.25),
                                                        (s * 1.25, s, s * 0.5), (0, 0, rnd.uniform(0, 3)), seg=8)
        y -= rnd.uniform(1.1, 1.9)
    # flower clusters: 5-9 five-petal flowers with yellow eyes
    for _ in range(40):
        c = spot(6.0, clear_r * 1.0) if rnd.random() < 0.45 else meadow_spot()
        if not c:
            continue
        col = rnd.choices(("pink", "white", "blue"), weights=(4, 4, 1))[0]
        for _ in range(rnd.randint(5, 9)):
            x, y = c[0] + rnd.uniform(-1.5, 1.5), c[1] + rnd.uniform(-1.2, 1.2)
            r = rnd.uniform(0.16, 0.26)
            a0 = rnd.uniform(0, 1)
            for k in range(5):
                a = a0 + k * 2 * math.pi / 5
                B[col].sphere((x + math.cos(a) * r, y + math.sin(a) * r, 0.1), (r * 0.8, r * 0.8, r * 0.28), seg=8)
            B["yellow"].sphere((x, y, 0.14), (r * 0.5, r * 0.5, r * 0.3), seg=8)
    # two mossy fallen logs and an old stump at the clearing's rim, outside the fan
    for ang, length in ((math.radians(205), 7.5), (math.radians(318), 6.0)):
        cx, cy = math.cos(ang) * clear_r * 0.92, math.sin(ang) * clear_r * 0.92
        if _keep_clear(cx, cy, clear_r):
            continue
        rot = (0, math.radians(90), ang + math.radians(70))
        B["bark"].cone((cx, cy, 0.85), 0.95, 0.85, length, rot, seg=14)
        for e in (-1, 1):
            axis = ang + math.radians(70)
            dx, dy = math.cos(axis) * e * length / 2, math.sin(axis) * e * length / 2
            B["cut"].sphere((cx + dx, cy + dy, 0.85), (0.86, 0.86, 0.86), seg=12)
        for _ in range(6):
            t = rnd.uniform(-0.4, 0.4) * length
            B["moss"].sphere((cx + math.cos(ang + math.radians(70)) * t, cy + math.sin(ang + math.radians(70)) * t,
                              1.55), (rnd.uniform(0.6, 1.0), rnd.uniform(0.5, 0.8), 0.35), seg=10)
    sx, sy = _path_x(-30.0) + 6.5, -30.0
    if not _keep_clear(sx, sy, clear_r):
        B["bark"].cone((sx, sy, 0.9), 1.5, 1.3, 1.8, seg=16)
        B["cut"].cone((sx, sy, 1.82), 1.3, 1.3, 0.06, seg=16)
        B["moss"].sphere((sx + 0.8, sy - 0.6, 1.9), (0.7, 0.6, 0.3), seg=10)
    # reeds and cattails on the pond's west bank (the shrimp drinks at its east edge, MAP["shrimp_drink"])
    px, py = MAP["pond"]
    for side in (-1,):
        for _ in range(14):
            x, y = px + side * rnd.uniform(4.6, 5.8), py + rnd.uniform(-1.6, 1.4)
            h = rnd.uniform(1.6, 2.8)
            tilt = (rnd.uniform(-0.15, 0.15), side * rnd.uniform(0.0, 0.2), 0)
            B["reed"].cone((x, y, h / 2), 0.07, 0.02, h, tilt, seg=6)
            if rnd.random() < 0.45:
                B["cattail"].sphere((x + side * h * 0.08, y, h * 0.92), (0.12, 0.12, 0.34), seg=8)
    return {k: b.done() for k, b in B.items()}
