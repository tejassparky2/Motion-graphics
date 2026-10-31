"""The Earth lab as a DIORAMA dollhouse (DIORAMA_EP01.md): a cutaway room seen from above at an angle with the
diorama look (mk/diorama.py: tilt-shift, haze, bloom). Floor plus two walls (back wall with the rain window, left wall
with a tank shelf), the desk with laptop, lamp and the hero tank, Kai's chair, a power strip with cables on the tiles.
Night: cold blue, the tank's cyan glow and the desk lamp's warm pool. Diorama units: 1 unit = 20 cm (Kai ~8.7 units,
hero.load(scale=5.8)).

    diorama.setup(); R = diorama_lab.room()
    R["tank"]    : center (gravel top), glass (front pane object), glass_y, size, leak (where the water starts), water
    R["desk"]    : top (z), center, front_y, laptop, seat (Kai's hips, seated, facing +Y), chair (its root)
    R["window"]  : center, size, glass (object), sky (material, node "Flash")
    R["strip"]   : the power strip object, end (where the water arrives), spark_at
    R["floor"]   : z (0), x and y extent
    R["lights"]  : room (the overhead fluorescent wash), lamp, tank, moon, strike (lightning)
    R["lightning"](frame)       two quick hits: the sky flashes white-blue, the room flashes
    R["flicker"]([frames])      the room light and the lamp stutter off for 2 frames at each frame listed
    R["power_out"](frame)       every lab light dies; only the storm outside remains
    R["puddle"](f0, f1)         water runs from the tank's leak across the desk, off its front edge, to the strip by f1
    R["spark"](frame)           a bright spark at the strip
    R["cam"](name, target, ...) diorama.camera() with the lab's defaults (night haze), see LAB_CAM

The room sits with the desk against the back wall (+Y); the default camera is south-east of the room, above, looking
north-west into the cutaway (yaw -30). Everything is procedural and seeded.
"""
import math
import random

import bpy
from mathutils import Vector

from . import anim, diorama, lab, look

hx = look.hexc
X0, X1, Y0, Y1, H = -11.0, 11.0, -6.0, 10.0, 13.5        # the room (units); walls on the back (+Y) and left (-X)
TOP = 3.75                                                  # desk top
NIGHT_HAZE = "#1b2740"
LAB_CAM = dict(dist=96.0, tilt=56.0, yaw=-30.0, lens=90.0, blur=10.0)   # the establishing dollhouse view


def _p(name, dark, mid, light):
    return diorama.lit_paint("dl_" + name, dark, mid, light)


def _night():
    """Turn diorama.setup()'s warm day into the lab's night: navy world fill, the sun as a cool moon, night haze."""
    sc = bpy.context.scene
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = hx("#2a3a66")
    bg.inputs[1].default_value = 0.5
    for n in nt.nodes:                               # the camera sees a dark night void around the dollhouse
        if n.type == "VALTORGB":
            n.color_ramp.elements[0].color = hx("#0c1120")
            n.color_ramp.elements[1].color = hx("#141c33")
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy, o.data.color = 0.9, hx("#9fb4ff")[:3]
            o.rotation_euler = (math.radians(50), 0, math.radians(200))   # from behind the window, down into the room
            moon = o
    if sc.node_tree:
        for n in sc.node_tree.nodes:
            if n.type == "MIX_RGB":
                n.inputs[2].default_value = hx(NIGHT_HAZE)
    return moon


def _rain_material():
    """Painted rain on a see-through card: bright diagonal streaks (~0.1 u wide, ~1.2 u long, a few px wide even in the
    wide shots) falling ~0.6 u a frame, plus a few fat drips sliding slowly down the glass. Two stretched Voronoi
    layers in the card's own units (the box's scale is applied), scrolling without end, so the window shows rain
    moving on every rendered frame without anything outside the wall."""
    m = bpy.data.materials.new("dl_rain_m")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new
    tc, rot = N("ShaderNodeTexCoord"), N("ShaderNodeVectorRotate")
    rot.rotation_type, rot.inputs["Angle"].default_value = "Y_AXIS", math.radians(20)    # slanted by the wind
    L(tc.outputs["Object"], rot.inputs["Vector"])

    def layer(scale, d, speed, sparse=0.0):
        """One stretched Voronoi layer: features d (mapped units) round, falling `speed` card units a frame."""
        mp, vor = N("ShaderNodeMapping"), N("ShaderNodeTexVoronoi")
        mp.inputs["Scale"].default_value = (scale[0], 1.0, scale[1])
        vor.feature, vor.inputs["Scale"].default_value = "F1", 1.0
        L(rot.outputs[0], mp.inputs[0])
        L(mp.outputs[0], vor.inputs["Vector"])
        ramp = N("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.0, (1, 1, 1, 1)
        ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = d, (0, 0, 0, 1)
        L(vor.outputs["Distance"], ramp.inputs[0])
        mask = ramp.outputs[0]
        if sparse:                                  # keep only some cells (by the cell's random colour)
            keep, mul = N("ShaderNodeMath"), N("ShaderNodeMath")
            keep.operation, keep.inputs[1].default_value = "GREATER_THAN", sparse
            mul.operation = "MULTIPLY"
            L(vor.outputs["Color"], keep.inputs[0])
            L(mask, mul.inputs[0])
            L(keep.outputs[0], mul.inputs[1])
            mask = mul.outputs[0]
        loc = mp.inputs["Location"]
        for f in (0, 1):
            loc.default_value = (0, 0, f * speed * scale[1])
            loc.keyframe_insert("default_value", frame=f)
        return mask

    streaks = layer((4.0, 0.4), 0.22, 0.6)
    drips = layer((1.4, 0.7), 0.2, 0.05, sparse=0.6)
    both = N("ShaderNodeMath")
    both.operation = "MAXIMUM"
    L(streaks, both.inputs[0])
    L(drips, both.inputs[1])
    sc = N("ShaderNodeMath")
    sc.operation, sc.inputs[1].default_value, sc.use_clamp = "MULTIPLY", 0.9, True
    L(both.outputs[0], sc.inputs[0])
    em, tr, mix, out = N("ShaderNodeEmission"), N("ShaderNodeBsdfTransparent"), N("ShaderNodeMixShader"), \
        N("ShaderNodeOutputMaterial")
    em.inputs[0].default_value, em.inputs[1].default_value = hx("#d6e6ff"), 2.6
    L(sc.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "BLENDED"
    for fc in anim.all_fcurves(nt.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
        fc.extrapolation = "LINEAR"                  # keeps falling forever (Voronoi doesn't tile, so no cycle)
    return m


def _box(name, loc, size, mat, rot=(0, 0, 0), bevel=0.0):
    return lab._box(name, loc, size, mat, rot=rot, bevel=bevel)


def room(seed=7):
    """Build the lab dollhouse into the current scene (call diorama.setup() first). Returns the anchors."""
    rnd = random.Random(seed)
    moon = _night()
    # ---------------------------------------------------------------- shell: floor, two walls, skirting
    tile = _p("tile", "#1c2433", "#2a3548", "#3a4862")
    grout = lab._glow("dl_grout", "#0d121b", 1.0)
    _box("dl_floor", ((X0 + X1) / 2, (Y0 + Y1) / 2, -0.3), (X1 - X0 + 2, Y1 - Y0 + 2, 0.6), tile)
    for i in range(int(X1 - X0) // 2 + 1):
        _box(f"dl_gx{i}", (X0 + i * 2.0, (Y0 + Y1) / 2, 0.005), (0.06, Y1 - Y0, 0.01), grout)
    for j in range(int(Y1 - Y0) // 2 + 1):
        _box(f"dl_gy{j}", ((X0 + X1) / 2, Y0 + j * 2.0, 0.005), (X1 - X0, 0.06, 0.01), grout)
    wall = _p("wall", "#26324e", "#34446a", "#465a86")
    band = _p("band", "#1d2740", "#28344f", "#34425f")
    t = 0.6
    wx0, wx1, wz0, wz1 = -8.5, -0.5, 5.2, 11.2               # the window over the desk
    _box("dl_wall_back_l", ((X0 + wx0) / 2, Y1 + t / 2, H / 2), (wx0 - X0, t, H), wall)
    _box("dl_wall_back_r", ((wx1 + X1) / 2, Y1 + t / 2, H / 2), (X1 - wx1, t, H), wall)
    _box("dl_wall_back_b", ((wx0 + wx1) / 2, Y1 + t / 2, wz0 / 2), (wx1 - wx0, t, wz0), wall)
    _box("dl_wall_back_t", ((wx0 + wx1) / 2, Y1 + t / 2, (wz1 + H) / 2), (wx1 - wx0, t, H - wz1), wall)
    _box("dl_wall_left", (X0 - t / 2, (Y0 + Y1) / 2, H / 2), (t, Y1 - Y0 + t * 2, H), wall)
    _box("dl_band_back", ((X0 + X1) / 2, Y1 - 0.05, 2.2), (X1 - X0, 0.1, 4.4), band)
    _box("dl_band_left", (X0 + 0.05, (Y0 + Y1) / 2, 2.2), (0.1, Y1 - Y0, 4.4), band)
    rim = _p("rim", "#3b4a6e", "#566894", "#7488b8")         # the cut edge of the dollhouse walls reads as a clean top
    _box("dl_wall_cap_b", ((X0 + X1) / 2, Y1 + t / 2, H + 0.15), (X1 - X0 + t, t + 0.1, 0.3), rim)
    _box("dl_wall_cap_l", (X0 - t / 2, (Y0 + Y1) / 2, H + 0.15), (t + 0.1, Y1 - Y0 + t * 2, 0.3), rim)
    _box("dl_floor_edge", ((X0 + X1) / 2, Y0 - 0.3, -0.3), (X1 - X0 + 2, 0.6, 0.62), rim)
    _box("dl_floor_edge_r", (X1 + 1.0, (Y0 + Y1) / 2, -0.3), (0.6, Y1 - Y0 + 2, 0.62), rim)
    # ---------------------------------------------------------------- the window: frame, night sky, rain
    frame_m = _p("win_frame", "#4a5a80", "#62749e", "#8193c0")
    for nm, loc, size in (("l", (wx0 + 0.2, Y1, (wz0 + wz1) / 2), (0.4, t + 0.2, wz1 - wz0)),
                          ("r", (wx1 - 0.2, Y1, (wz0 + wz1) / 2), (0.4, t + 0.2, wz1 - wz0)),
                          ("b", ((wx0 + wx1) / 2, Y1, wz0 + 0.2), (wx1 - wx0, t + 0.2, 0.4)),
                          ("t", ((wx0 + wx1) / 2, Y1, wz1 - 0.2), (wx1 - wx0, t + 0.2, 0.4)),
                          ("m", ((wx0 + wx1) / 2, Y1, (wz0 + wz1) / 2), (0.25, t, wz1 - wz0)),
                          ("h", ((wx0 + wx1) / 2, Y1, wz0 + (wz1 - wz0) * 0.6), (wx1 - wx0, t, 0.25))):
        _box(f"dl_win_{nm}", loc, size, frame_m)
    _box("dl_sill", ((wx0 + wx1) / 2, Y1 - 0.6, wz0 - 0.1), (wx1 - wx0 + 1.0, 1.4, 0.25), frame_m)
    # everything seen through the window sits INSIDE the back wall's thickness (y Y1..Y1+t), so from above nothing
    # shows over the wall: a night-sky card, distant buildings, and painted rain scrolling down a card in front of it
    ww, wh = wx1 - wx0, wz1 - wz0
    wcx, wcz = (wx0 + wx1) / 2, (wz0 + wz1) / 2
    sky = lab._gradient("dl_sky", "#1d2c58", "#0a1030", 1.0, noise=0.3)
    _box("dl_sky", (wcx, Y1 + 0.5, wcz), (ww + 0.4, 0.04, wh + 0.4), sky)
    bld = lab._glow("dl_bldg", "#0b1022", 1.0)
    lit = lab._glow("dl_lit", "#ffcf7a", 1.4)
    for i in range(4):
        bx, bw, bh = wx0 + 0.9 + i * 2.0 + rnd.uniform(-0.3, 0.3), rnd.uniform(1.2, 1.9), rnd.uniform(1.2, 2.6)
        _box(f"dl_bldg{i}", (bx, Y1 + 0.42, wz0 + bh / 2), (bw, 0.04, bh), bld)
        for j in range(rnd.randint(1, 2)):
            _box(f"dl_bldg{i}_w{j}", (bx + rnd.uniform(-bw / 3, bw / 3), Y1 + 0.38, wz0 + rnd.uniform(0.4, bh - 0.3)),
                 (0.22, 0.02, 0.18), lit)
    glass = look.fade("dl_glass", hx("#a8c8ff"), 0.08)
    win_glass = _box("dl_win_glass", (wcx, Y1 + 0.05, wcz), (ww, 0.03, wh), glass)
    rain_m = _rain_material()
    _box("dl_rain", (wcx, Y1 + 0.3, wcz), (ww, 0.02, wh), rain_m)
    r = random.Random(11)
    bolt_m = look.fade("dl_bolt_m", hx("#f4f8ff"), 0.0)
    pts, x, z = [], wcx - 0.5, wz1 + 0.3
    while z > wz0 + 1.5:
        pts.append((x, z))
        x += r.uniform(-0.5, 0.5)
        z -= r.uniform(0.5, 0.9)
    verts, faces = [], []
    for i, ((xa, za), (xb, zb)) in enumerate(zip(pts, pts[1:])):
        k, w = len(verts), 0.1 * (1 - i / len(pts)) + 0.03
        verts += [(xa - w, 0, za), (xa + w, 0, za), (xb + w, 0, zb), (xb - w, 0, zb)]
        faces.append((k, k + 1, k + 2, k + 3))
    lab._mesh("dl_bolt", verts, faces, bolt_m, (0, Y1 + 0.46, 0))
    # ---------------------------------------------------------------- left wall: a shelf of glowing tanks + a chart
    metal = _p("shelf", "#2c3650", "#3e4a68", "#55648a")
    for z in (2.0, 5.6):
        _box(f"dl_shelf{z}", (X0 + 1.6, 0.5, z), (3.0, 9.0, 0.25), metal)
    shelf_water = []
    for i, (yc, z, col) in enumerate(((-1.6, 2.12, ("#0f4f86", "#56d6ff")), (2.6, 2.12, ("#0e5a63", "#4fe8cf")),
                                      (0.5, 5.72, ("#143a86", "#6aa8ff")))):
        wm = lab._gradient(f"dl_shelfwater{i}", col[0], col[1], 1.0)
        shelf_water.append(wm)
        _box(f"dl_shelftank{i}_w", (X0 + 1.6, yc, z + 1.0), (2.2, 3.6, 2.0), wm)
        _box(f"dl_shelftank{i}_hood", (X0 + 1.6, yc, z + 2.15), (2.4, 3.8, 0.3), _p("hood", "#141a26", "#1f2738",
                                                                                       "#2b354b"))
    _box("dl_chart", (X0 + 0.1, 7.6, 8.4), (0.1, 3.6, 3.0), _p("chart", "#8a96b4", "#a8b4d0", "#c8d2ea"))
    # ---------------------------------------------------------------- the desk, laptop, lamp, notebook, mug
    wood = _p("desk", "#3e3248", "#564662", "#6e5c7e")
    side = _p("desk_side", "#2c2638", "#3a3248", "#4a405a")
    dx0, dx1, dy0, dy1 = -10.0, 2.0, Y1 - 3.6, Y1 - 0.1
    dcx, dcy = (dx0 + dx1) / 2, (dy0 + dy1) / 2
    _box("dl_desk_top", (dcx, dcy, TOP - 0.15), (dx1 - dx0, dy1 - dy0, 0.3), wood, bevel=0.06)
    _box("dl_desk_leg_l", (dx0 + 0.25, dcy, (TOP - 0.3) / 2), (0.3, dy1 - dy0 - 0.3, TOP - 0.3), side)
    _box("dl_desk_drawers", (dx1 - 1.2, dcy, (TOP - 0.3) / 2), (2.2, dy1 - dy0 - 0.3, TOP - 0.3), side, bevel=0.05)
    shell = _p("laptop", "#8a92a8", "#a7afc4", "#c9d0e2")
    lx, ly = dx1 - 1.9 - 3.5, dcy - 0.3                    # the laptop (and Kai) just left of the tank: within reach
    _box("dl_laptop_base", (lx, ly, TOP + 0.08), (2.2, 1.5, 0.12), shell, bevel=0.03)
    screen = lab._glow("dl_screen", "#bfe0ff", 1.3)
    _box("dl_laptop_lid", (lx, ly + 0.85, TOP + 0.75), (2.2, 0.1, 1.4), shell, rot=(math.radians(-15), 0, 0))
    _box("dl_laptop_screen", (lx, ly + 0.78, TOP + 0.75), (2.0, 0.02, 1.25), screen, rot=(math.radians(-15), 0, 0))
    page = _p("page", "#c8c0aa", "#e9e2cf", "#f6f1e3")
    nx, ny = dx0 + 2.0, dcy - 0.4
    _box("dl_notebook", (nx, ny, TOP + 0.05), (2.0, 1.4, 0.08), page, rot=(0, 0, math.radians(8)))
    lab._cyl("dl_mug", (lx - 2.2, ly - 0.4, TOP + 0.3), 0.3, 0.6, _p("mug", "#b04a3c", "#d96c5a", "#f08a76"))
    lamp_m = _p("lamp", "#b8862e", "#e3b04b", "#f5cd6e")
    bx, by = dx0 + 0.8, dy1 - 0.8
    lab._cyl("dl_lamp_base", (bx, by, TOP + 0.08), 0.45, 0.16, lamp_m)
    lab._cyl("dl_lamp_arm", (bx + 0.2, by - 0.3, TOP + 1.3), 0.06, 2.5, lamp_m,
             rot=(math.radians(-15), math.radians(8), 0))
    lab._cyl("dl_lamp_shade", (bx + 0.6, by - 0.9, TOP + 2.4), 0.55, 0.7, lamp_m, r2=0.2,
             rot=(math.radians(-150), math.radians(-10), 0))
    bulb = lab._glow("dl_bulb", "#fff1c9", 3.0)
    lab._ball("dl_bulb", (bx + 0.65, by - 1.0, TOP + 2.15), (0.22, 0.22, 0.22), bulb, 10)
    pool = lab._pool("dl_lamp", (nx + 0.4, ny + 0.2, TOP + 0.01), (3.6, 2.7), "#ffb054", 0.95)
    lamp = lab._light("dl_lamp_light", "SPOT", (bx + 0.7, by - 1.1, TOP + 2.1), (math.radians(15), 0, 0), 1400,
                      "#ffd28a", 0.2, spot=math.radians(100))
    # ---------------------------------------------------------------- the hero tank on the desk's right end
    tw, td, th = 3.2, 1.8, 1.8                               # 64 x 36 x 36 cm
    tcx, tcy = dx1 - 1.9, dcy + 0.2
    tank_rim = _p("tank_rim", "#10151f", "#1a2130", "#263046")
    water = lab._gradient("dl_tankwater", "#1f6f8c", "#7fd0dc", 1.2)
    _box("dl_tank_back", (tcx, tcy + td / 2 - 0.05, TOP + th * 0.45), (tw - 0.1, 0.05, th * 0.85), water)
    for s in (-1, 1):
        _box(f"dl_tank_side{s}", (tcx + s * (tw / 2 - 0.05), tcy, TOP + th * 0.45), (0.05, td - 0.1, th * 0.85), water)
    sand = _p("tank_sand", "#b8a07a", "#d9c39a", "#efe0bf")
    _box("dl_tank_sand", (tcx, tcy, TOP + 0.18), (tw - 0.12, td - 0.12, 0.3), sand)
    for i in range(4):
        lab._cyl(f"dl_tank_plant{i}", (tcx + (-1.1 if i % 2 else 1.1) + rnd.uniform(-0.2, 0.2), tcy + 0.3,
                                       TOP + 0.75), 0.12, rnd.uniform(0.8, 1.3), _p(f"plant{i % 2}", "#246e48",
                                                                                    "#3fae6a", "#69c96e"),
                 verts=6, r2=0.01)
    lab._ball("dl_tank_rock", (tcx + 0.6, tcy + 0.2, TOP + 0.4), (0.45, 0.35, 0.3), _p("tank_rock", "#6f6588",
                                                                                         "#9b8fb0", "#bdb3d0"), 10)
    surf = look.fade("dl_tank_surface", hx("#c9f3ff"), 0.5)
    _box("dl_tank_surface", (tcx, tcy, TOP + th * 0.88), (tw - 0.1, td - 0.1, 0.03), surf)
    tglass = _box("dl_tank_glass", (tcx, tcy - td / 2, TOP + th / 2), (tw, 0.03, th),
                  look.fade("dl_tank_glass_m", hx("#bff2ff"), 0.1))
    for z in (TOP + 0.05, TOP + th):
        _box(f"dl_tank_rim{z:.1f}", (tcx, tcy, z), (tw + 0.1, td + 0.1, 0.12), tank_rim)
    _box("dl_tank_hood", (tcx, tcy, TOP + th + 0.15), (tw + 0.15, td + 0.15, 0.25), tank_rim)
    bub = lab._glow("dl_bubble", "#e6fbff", 1.6)
    for i in range(6):
        s = rnd.uniform(0.04, 0.08)
        b = lab._ball(f"dl_bub{i}", (tcx - 1.3, tcy + 0.5, TOP + 0.4), (s, s, s), bub, 8)
        b.visible_shadow = False
        P, t0 = rnd.randint(36, 56), -rnd.randint(0, 50)
        anim.key(b, "location", t0, (tcx - 1.3, tcy + 0.5, TOP + 0.4), "LINEAR")
        anim.key(b, "location", t0 + P, (tcx - 1.3 + rnd.uniform(-0.1, 0.1), tcy + 0.5, TOP + th * 0.86), "LINEAR")
        lab._cycle(b, "location")
    tank_light = lab._light("dl_tank_light", "AREA", (tcx, tcy - 1.6, TOP + 1.2), (math.radians(-80), 0, 0), 1100,
                            "#4fd8e8", 2.4, 1.2, shadow=False)
    cyan_pool = lab._pool("dl_tank", (tcx - 0.8, dy0 - 3.0, 0.02), (6.5, 4.6), "#4fd8e8", 0.6)
    desk_pool = lab._pool("dl_tank_desk", (tcx - 0.2, dy0 + 0.6, TOP + 0.02), (2.6, 1.0), "#4fd8e8", 0.45)
    # ---------------------------------------------------------------- Kai's chair (seated facing +Y, the window)
    fab = _p("chair", "#1f2740", "#2c3550", "#3e4a6e")
    blk = _p("chair_base", "#10131c", "#1b2030", "#262c40")
    sx, sy, sz = lx - 0.2, dy0 - 1.2, 2.4                  # pulled in: his right hand reaches the tank glass
    before = set(bpy.context.scene.objects)
    _box("dl_chair_seat", (sx, sy, sz - 0.15), (2.3, 2.2, 0.35), fab, bevel=0.12)
    _box("dl_chair_back", (sx, sy - 1.2, sz + 1.4), (2.1, 0.3, 2.1), fab, rot=(math.radians(-8), 0, 0), bevel=0.12)
    lab._cyl("dl_chair_pole", (sx, sy, sz / 2), 0.14, sz - 0.3, blk, verts=12)
    for i in range(5):
        a = i / 5 * 2 * math.pi + 0.3
        _box(f"dl_chair_leg{i}", (sx + math.cos(a) * 0.8, sy + math.sin(a) * 0.8, 0.3), (1.6, 0.18, 0.15), blk,
             rot=(0, 0, a))
    root = lab._link(bpy.data.objects.new("dl_chair_root", None))
    root.location = (sx, sy, 0)
    bpy.context.view_layer.update()
    for o in [o for o in bpy.context.scene.objects if o not in before and o is not root]:
        o.parent = root
        o.matrix_parent_inverse = root.matrix_world.inverted()
    # ---------------------------------------------------------------- the power strip and cables on the floor
    body_m = _p("strip", "#b8bccb", "#d7dbe4", "#eef1f6")
    px, py, rz = dx1 + 3.2, dy0 - 3.6, math.radians(-20)
    strip = _box("dl_strip", (px, py, 0.2), (2.4, 0.45, 0.32), body_m, rot=(0, 0, rz), bevel=0.06)
    ax = Vector((math.cos(rz), math.sin(rz), 0))
    plug_m = _p("plug", "#1c2029", "#2b2f3a", "#3a3f4d")
    for i in range(3):
        p = Vector((px, py, 0.5)) + ax * (-0.6 + i * 0.5)
        _box(f"dl_plug{i}", tuple(p), (0.28, 0.28, 0.28), plug_m, rot=(0, 0, rz), bevel=0.03)
    _box("dl_switch", tuple(Vector((px, py, 0.38)) + ax * 0.95), (0.22, 0.22, 0.05), lab._glow("dl_switch", "#ff5a4a",
                                                                                                 1.6), rot=(0, 0, rz))
    cable = _p("cable", "#0f1218", "#1e222b", "#2c313c")
    lab._cable("dl_cord_tank", [(px - 0.6, py, 0.4), (px - 1.4, py + 1.6, 0.08), (dx1 - 0.2, dy0 + 1.0, 0.08),
                                (dx1 - 0.3, dy1 - 0.3, 0.2), (dx1 - 0.3, dy1 - 0.3, TOP - 0.3),
                                (tcx + 1.0, tcy + 0.6, TOP + 0.1)], cable, r=0.07)
    lab._cable("dl_cord_laptop", [(px - 0.1, py, 0.4), (px - 3.0, py + 1.0, 0.08), (lx + 0.5, dy0 + 0.5, 0.08),
                                  (lx + 0.5, dy1 - 0.3, 0.2), (lx + 0.5, dy1 - 0.3, TOP - 0.2), (lx + 0.9, ly + 0.5,
                                                                                                TOP + 0.1)], cable,
               r=0.06)
    lab._cable("dl_cord_wall", [(px + 1.2, py - 0.4, 0.2), (X1 - 4.0, py - 1.0, 0.08), (X1 - 1.0, Y1 - 1.0, 0.08),
                                (X1 - 1.0, Y1 - 0.2, 1.2)], cable, r=0.07)
    end = Vector((px, py, 0.0)) - ax * 1.25
    spark_at = Vector((px, py, 0.9)) - ax * 0.6
    # ---------------------------------------------------------------- the room light (an overhead fluorescent wash)
    room_l = lab._light("dl_room_light", "AREA", ((X0 + X1) / 2, (Y0 + Y1) / 2, H + 6), (0, 0, 0), 13000, "#cfe0ff",
                        14.0, 10.0)
    strike = lab._light("dl_strike", "AREA", ((wx0 + wx1) / 2, Y1 + 3.0, 9.0), (math.radians(-70), 0, 0), 0.0,
                        "#d4e0ff", 8.0, 6.0)
    for o in bpy.context.scene.objects:
        if o.type == "MESH" and (o.name.startswith(("dl_sky", "dl_bldg", "dl_rain", "dl_bolt", "dl_bub", "dl_lit"))
                                 or any(m and getattr(m, "surface_render_method", "") == "BLENDED"
                                        for m in o.data.materials)):
            o.visible_shadow = False
    spill_m = lab._water_floor()
    base = {o.name: o.data.energy for o in (room_l, lamp, tank_light)}
    glows = [(screen, 1.3), (bulb, 3.0), (pool, 0.95), (cyan_pool, 0.6), (desk_pool, 0.45), (water, 1.2)]
    glows += [(m, 1.0) for m in shelf_water]

    def _em(m):
        return lab._em(m).inputs[1]

    def lightning(frame, strength=1.0):
        fl_sky = sky.node_tree.nodes["Flash"].inputs["Factor"]
        fl_bolt = bolt_m.node_tree.nodes["Mix"].inputs[0]
        for f, v in ((frame - 1, 0.0), (frame, 1.0), (frame + 1, 0.25), (frame + 2, 0.85), (frame + 3, 0.5),
                     (frame + 6, 0.0)):
            it = "LINEAR" if f >= frame + 3 else "CONSTANT"
            lab._ksock(fl_sky, f, v * 0.9 * strength, it)
            lab._kprop(strike.data, "energy", f, v * 30000 * strength, it)
            lab._ksock(fl_bolt, f, (1.0 if frame <= f <= frame + 2 and v > 0.5 else 0.0) * strength, "CONSTANT")

    def _set(f, on, lamps=(room_l, lamp), mats=((screen, 1.3), (bulb, 3.0), (pool, 0.95)), k_off=0.03):
        for o in lamps:
            lab._kprop(o.data, "energy", f, base[o.name] * (1.0 if on else k_off), "CONSTANT")
        for m, s in mats:
            lab._ksock(_em(m), f, s if on else s * 0.08, "CONSTANT")

    def flicker(frames):
        frames = sorted(frames)
        _set(frames[0] - 1, True, mats=((bulb, 3.0), (pool, 0.95)))
        for f in frames:
            _set(f, False, mats=((bulb, 3.0), (pool, 0.95)))
            _set(f + 2, True, mats=((bulb, 3.0), (pool, 0.95)))

    def power_out(frame):
        _set(frame - 1, True, (room_l, lamp, tank_light), glows + [(spill_m, 1.0)])
        _set(frame, False, (room_l, lamp, tank_light), glows + [(spill_m, 1.0)], 0.0)

    def puddle(f0, f1):
        lx_, ly_ = tcx - 0.6, dy0
        t_edge, t_floor = f0 + (f1 - f0) * 0.15, f0 + (f1 - f0) * 0.3
        sheet = lab._mesh("dl_spill_desk", [(-0.25, -1, 0), (0.25, -1, 0), (0.35, 0, 0), (-0.35, 0, 0)],
                          [(0, 1, 2, 3)], spill_m, (lx_, tcy - td / 2, TOP + 0.02))
        anim.key(sheet, "scale", f0 - 1, (1, 0.001, 1), "CONSTANT")
        anim.key(sheet, "scale", t_edge, (1, tcy - td / 2 - ly_, 1), "LINEAR")
        stream = lab._mesh("dl_spill_stream", [(-0.08, 0, -1), (0.08, 0, -1), (0.1, 0, 0), (-0.1, 0, 0)],
                           [(0, 1, 2, 3)], spill_m, (lx_, ly_ - 0.05, TOP))
        stream.visible_shadow = False
        anim.key(stream, "scale", t_edge - 1, (1, 1, 0.001), "CONSTANT")
        anim.key(stream, "scale", t_floor, (1, 1, TOP), "LINEAR")
        a, b = Vector((lx_, ly_ - 0.4, 0)), Vector((end.x + 0.2, end.y + 0.2, 0))
        rr = random.Random(21)
        for i in range(14):
            u = i / 13
            p = a.lerp(b, u) + Vector((-0.6, -0.4, 0)) * math.sin(u * math.pi)
            rad = 0.6 + 0.4 * math.sin(u * math.pi) + rr.uniform(-0.05, 0.1)
            vs = [(math.cos(k / 20 * 2 * math.pi) * rad * rr.uniform(0.82, 1.1),
                   math.sin(k / 20 * 2 * math.pi) * rad * rr.uniform(0.82, 1.1), 0) for k in range(20)]
            d = lab._mesh(f"dl_spill{i}", vs, [tuple(range(20))], spill_m, (p.x, p.y, 0.03 + i * 0.0001))
            ts = t_floor + (f1 - t_floor) * u
            anim.key(d, "scale", ts - 1, 0.001, "CONSTANT")
            anim.key(d, "scale", ts + 5, 1.0)

    def spark(frame):
        sl = lab._light("dl_spark_light", "POINT", tuple(spark_at + Vector((0, -0.5, 1.5))), (0, 0, 0), 0.0,
                        "#e8f3ff", 0.2)
        for f, v in ((frame - 1, 0), (frame, 1.0), (frame + 1, 0.25), (frame + 2, 0.8), (frame + 3, 0.15),
                     (frame + 5, 0)):
            lab._kprop(sl.data, "energy", f, v * 800, "CONSTANT")
        star = lab._glow("dl_spark_star", "#f4fbff", 4.0)
        verts = [(math.cos(k / 8 * 2 * math.pi) * (1.0 if k % 2 == 0 else 0.09), 0,
                  math.sin(k / 8 * 2 * math.pi) * (1.0 if k % 2 == 0 else 0.09)) for k in range(8)] + [(0, 0, 0)]
        for j in range(2):
            s = lab._mesh(f"dl_spark{frame}_{j}", verts, [(8, k, (k + 1) % 8) for k in range(8)], star,
                          tuple(spark_at))
            s.rotation_euler = (math.radians(55), math.radians(45 * j), math.radians(-30))
            s.visible_shadow = False
            for f, sc_ in zip(range(frame - 1, frame + 5), ((0.001, 1.6, 0.8, 1.9, 0.5, 0.001) if j == 0 else
                                                            (0.001, 0.7, 1.2, 0.6, 0.9, 0.001))):
                anim.key(s, "scale", f, sc_, "CONSTANT")

    def cam(name, target, frame=1, **kw):
        c = diorama.camera(name, target, frame=frame, **{**LAB_CAM, **kw})
        return c

    return dict(
        tank=dict(center=(tcx, tcy, TOP + 0.33), glass=tglass, glass_y=tcy - td / 2, size=(tw, td, th),
                  leak=(tcx - 0.6, tcy - td / 2, TOP + 0.05), water=water, surface=surf, light=tank_light),
        desk=dict(top=TOP, center=(dcx, dcy, TOP), front_y=dy0, laptop=(lx, ly, TOP), seat=(sx, sy, sz),
                  chair=root, lamp=(bx, by, TOP)),
        window=dict(center=((wx0 + wx1) / 2, Y1, (wz0 + wz1) / 2), size=(wx1 - wx0, wz1 - wz0), glass=win_glass,
                    sky=sky, bolt=bolt_m),
        strip=dict(object=strip, end=tuple(end), spark_at=tuple(spark_at)),
        floor=dict(z=0.0, x=(X0, X1), y=(Y0, Y1)),
        lights=dict(room=room_l, lamp=lamp, tank=tank_light, moon=moon, strike=strike),
        lightning=lightning, flicker=flicker, power_out=power_out, puddle=puddle, spark=spark, cam=cam,
    )
