"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 2: S04, S05a, S07, the tank beats, looking
down into the hero tank as a toy aquarium on the lab desk.

Every keyframe is the 3D shot's (channels/monsters/ep01v2/helper2.py: the same _snap_sequence and _s07_action), so
each beat lands on the same frame and the SFX stay in sync:
    S04  eye 1-4, the claw held cocked while the glint grows 5-15, the slow shut 16-19 ("snaps"), flash 20-21, the
         bubble swells white-hot to its peak on "boils" (48)
    S05a the bubble held at its peak, shrinking and collapsing with a flash on "sun" (52-53), micro-bubbles after
    S07  eye 1-2, held wind-up 3-7, the shut 8-9 ("Snap."), flash 10, impact 11-12 (comp.impact from the subject
         pass), the crack runs across the front glass 13-17, frozen hold
The cameras are diorama.camera()s (tilt 45-70, long lens, tilt-shift), close to the tank because a shrimp is ~6 cm.

Units as everywhere in the diorama: 1 unit = 20 cm. The tank is 0.56 x 0.30 x 0.30 m (2.8 x 1.5 x 1.5 units), as in
mk/lab.py. If mk/diorama_lab.py (helper 1's dollhouse lab) is present, its room() places the tank on the desk;
otherwise a stand-in desk and tank are built here.
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.ep01v2 import helper2 as h3d
from channels.monsters.mk import anim, diorama, look, paintbg
from channels.monsters.mk import pistolshrimp as ps

UNITS = 5.0                    # set units per metre (1 unit = 20 cm)
K = 0.15                       # shrimp scale: ~0.37 units (7 cm) body, a touch big so it reads from above
TURN = math.radians(45)        # as in the 3D shots: the claw points at the front glass, near the leak
TANK = (2.8, 1.5, 1.5)         # w, d, h in units
LENS, BLUR = 95.0, 10.0


def _tank(center):
    """A toy aquarium (open top, seen from above): water-blue inner walls, sand and pebbles, a rock, plants, a water
    surface with a bright waterline, faint glass panes with dark rims. center = the middle of the gravel top.
    Returns the handles the shared keyframes use (floor, glass, leak, water)."""
    cx, cy, cz = center
    w, d, h = TANK
    hx = look.hexc
    wl = cz + h * 0.82                                          # water line
    back = ps._gradient("dio_water", "#1f6f8c", "#7fd0dc")
    side = ps._gradient("dio_waterside", "#1a5f7a", "#6cc0cf")
    objs = []

    def box(name, loc, size, mat):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.object
        o.name = name
        o.scale = size
        o.data.materials.append(mat)
        objs.append(o)
        return o

    box("dio_back", (cx, cy + d / 2 - 0.02, (cz - 0.25 + wl) / 2), (w - 0.04, 0.02, wl - cz + 0.25), back)
    for s in (-1, 1):
        box(f"dio_side{s}", (cx + s * (w / 2 - 0.02), cy, (cz - 0.25 + wl) / 2), (0.02, d - 0.04, wl - cz + 0.25), side)
    sand = look.paint("tank_sand", hx("#d9c39a"), noise=0.18, scale=9.0)
    box("dio_sand", (cx, cy, cz - 0.15), (w - 0.06, d - 0.06, 0.3), sand)
    ps.gravel_bed((cx - w / 2 + 0.06, cx + w / 2 - 0.06), (cy - d / 2 + 0.06, cy + d / 2 - 0.06), cz, random.Random(5),
                  n=1400, k=K * 1.6, clear=(cx - 0.15, cy - 0.35, 0.3, 0.18), name="dio_gravel")
    rock = paintbg.paint3("tank_rock", hx("#6f6488"), hx("#9b8fb0"), hx("#c4bad6"), noise=0.2, scale=4.0)
    objs.append(ps._sphere("dio_rock", (cx + 0.75, cy + 0.3, cz + 0.1), (0.42, 0.32, 0.26), rock, 0, 24,
                           (0.2, 0.1, 0.4)))
    objs.append(ps._sphere("dio_rock2", (cx - 0.95, cy + 0.45, cz + 0.06), (0.24, 0.2, 0.15), rock, 0, 18))
    objs.append(ps._sphere("dio_hole", (cx + 0.52, cy + 0.05, cz + 0.1), (0.13, 0.03, 0.08),
                           look.flat("tank_hole", hx("#2c2238")), 0, 16, (0, 0, 0.5)))
    leaf_m = [paintbg.paint3(f"tank_leaf{v}", *paintbg.greens(v, 0.25), noise=0.2, scale=5.0) for v in range(3)]
    rnd = random.Random(9)
    for px, py, n, hh in ((-1.1, 0.5, 7, 1.0), (1.15, 0.55, 8, 1.05), (-0.5, 0.6, 5, 0.75), (0.3, 0.62, 5, 0.85)):
        for j in range(n):
            a = j / n * 2 * math.pi + rnd.uniform(-0.3, 0.3)
            tilt = rnd.uniform(0.1, 0.35)
            top = (cx + px + math.cos(a) * tilt * hh * 0.5, cy + py + math.sin(a) * tilt * hh * 0.3,
                   cz + hh * rnd.uniform(0.6, 1.0))
            mid = (cx + px + math.cos(a) * tilt * hh * 0.15, cy + py, cz + hh * 0.45)
            objs.append(ps._tube(f"dio_blade{px}_{j}", [(cx + px, cy + py, cz), mid, top], 0.022,
                                 rnd.choice(leaf_m), 0, taper=(1.0, 0.25)))
    surf = box("dio_surface", (cx, cy, wl), (w - 0.04, d - 0.04, 0.004), look.fade("dio_surface", hx("#c9f3ff"), 0.22))
    surf.visible_shadow = False
    line = box("dio_waterline", (cx, cy - d / 2 + 0.03, wl), (w - 0.06, 0.012, 0.02),
               look.flat("dio_waterline", hx("#f2fdff"), 1.3))
    line.visible_shadow = False
    glass = box("dio_glass", (cx, cy - d / 2, (cz - 0.25 + cz + h) / 2), (w, 0.01, h + 0.25),
                look.fade("dio_glass", hx("#dff7ff"), 0.07))
    glass.visible_shadow = False
    rim = look.paint("tank_rim", hx("#26323d"), noise=0.05)
    for z, hh in ((cz + h - 0.06, 0.12), (cz - 0.3, 0.12)):
        for s in (-1, 1):
            box(f"dio_rimx{z:.1f}{s}", (cx, cy + s * d / 2, z), (w + 0.06, 0.06, hh), rim)
            box(f"dio_rimy{z:.1f}{s}", (cx + s * w / 2, cy, z), (0.06, d + 0.06, hh), rim)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"dio_post{sx}{sy}", (cx + sx * w / 2, cy + sy * d / 2, cz - 0.3 + (h + 0.3) / 2), (0.06, 0.06, h + 0.3),
                rim)
    hl = look.fade("dio_glass_hl", hx("#ffffff"), 0.16)
    for u, ww in ((0.16, 0.08), (0.22, 0.03)):
        g = box(f"dio_hl{u}", (cx - w / 2 + w * u, cy - d / 2 - 0.012, cz + h * 0.45), (ww, 0.004, h * 0.6), hl)
        g.rotation_euler = (0, math.radians(-28), 0)
        g.visible_shadow = False
    bpy.ops.object.light_add(type="AREA", location=(cx, cy, cz + h + 0.3))       # the hood light
    hood = bpy.context.object
    hood.data.energy, hood.data.color = 60.0, hx("#7fd0dc")[:3]
    hood.data.size = w * 0.9
    return dict(floor=(cx, cy, cz), glass=glass, water=[back, side], waterline=wl,
                leak=(cx - w * 0.15, cy - d / 2 - 0.01, cz - 0.15), objects=objs)


def _stand_in_desk(top):
    """A painted desk top and a dark floor when helper 1's dollhouse lab isn't available."""
    hx = look.hexc
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, top - 0.1))
    d = bpy.context.object
    d.name = "dio_desk"
    d.scale = (12, 6, 0.2)
    d.data.materials.append(paintbg.paint3("dio_desk", hx("#4a3d50"), hx("#5b4a5e"), hx("#76627a"), noise=0.12))
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, top - 3.75))
    bpy.context.object.data.materials.append(look.paint("dio_floor", hx("#2f3a4a"), noise=0.08))


def _dress(tank):
    """Close-up detail inside the dollhouse lab's hero tank: painted pebbles at shrimp scale (its sand box reads as
    a flat plane this close), and the water-blue inner walls stay helper 1's."""
    cx, cy, cz = tank["floor"]
    w, d, _ = tank["size"]
    ps.gravel_bed((cx - w / 2 + 0.1, cx + w / 2 - 0.1), (cy - d / 2 + 0.1, cy + d / 2 - 0.1), cz, random.Random(5),
                  n=1600, k=K * 1.6, clear=(cx - 0.15, cy - 0.35, 0.3, 0.18), name="dio_gravel")


def _stage():
    """The diorama set and the shrimp (room, tank, rig): helper 1's dollhouse lab (mk/diorama_lab.py) with my
    pebbles in its hero tank; a stand-in desk and tank if that module is missing."""
    diorama.setup()
    try:
        from channels.monsters.mk import diorama_lab
    except ImportError:
        diorama_lab = None
    if diorama_lab is not None:
        room = diorama_lab.room()
        t = room["tank"]
        tank = dict(floor=t["center"], glass=t["glass"], leak=t["leak"], size=t["size"],
                    water=[t["water"]] if not isinstance(t["water"], list) else t["water"])
        _dress(tank)
    else:
        room = None
        _stand_in_desk(3.75)
        tank = _tank(Vector((0.0, 0.0, 3.75 + 0.3)))
    fx, fy, fz = tank["floor"]
    rig = ps.build((fx - 0.15, fy - 0.35, fz), turn=TURN, scale=K)
    return room, tank, rig


def _eye_cam(rig, name, frame, dist=0.55):
    """A high close-up on the shrimp's face (tilt 48, never eye level), focused on the camera-side eye."""
    eye = rig["eyes"][0].matrix_world.translation.copy()
    yaw = math.degrees(TURN) - 60                      # from the face side
    return diorama.camera(name, eye, dist=dist, tilt=48, yaw=yaw, lens=LENS, blur=BLUR, frame=frame)


def _flash(cam, keys):
    return h3d._flash(cam, keys)


def _near(cam):
    """Close tank cameras: the flash card sits 1 cm in front; and the haze (meant for the far edge of a room) starts
    well past the tank floor, so the water stays clear."""
    cam.data.clip_start = 0.004
    ms = bpy.context.scene.world.mist_settings
    ms.start, ms.depth = max(ms.start, cam.data.dof.focus_distance * 3.0), max(ms.depth, 6.0)


def s04():
    room, tank, rig, _, F = h3d._snap_sequence(0, stage=_stage, cameras=False)
    tip = rig["tip"].matrix_world.translation
    eye = _eye_cam(rig, "dio_cam_eye", 1)
    claw = diorama.camera("dio_cam_claw", tip + Vector((0.12, 0.05, 0.0)), dist=1.9, tilt=62, yaw=-25, lens=LENS,
                          blur=BLUR, frame=5)
    for c in (eye, claw):
        _near(c)
    _flash(claw, [(19, 0.0), (20, 0.9), (21, 0.55), (22, 0.0)])
    return dict(frames=h3d.LEN["S04"] + h3d.TAIL, step=1, subject=[rig["root"]])


def s05a():
    room, tank, rig, _, F = h3d._snap_sequence(h3d.SPLIT, stage=_stage, cameras=False)
    tip = rig["tip"].matrix_world.translation
    cam = diorama.camera("dio_cam_bubble", tip + Vector((-0.05, 0.05, 0.08)), dist=2.2, tilt=55, yaw=10, lens=LENS,
                         blur=BLUR, frame=1)
    _near(cam)
    _flash(cam, [(F(112), 0.0), (F(113), 0.85), (F(114), 0.4), (F(115), 0.0)])
    return dict(frames=h3d.LEN["S05a"] + h3d.TAIL, step=1, subject=[rig["root"]])


def s07():
    room, tank, rig = _stage()
    lx, gy, lz = h3d._s07_action(tank, rig, units=UNITS)
    eye = _eye_cam(rig, "dio_cam_eye", h3d.S07_EYE)
    fx, fy, fz = tank["floor"]
    cam = diorama.camera("dio_cam_tank", Vector((fx - 0.3, fy - 0.35, fz + 0.45)), dist=5.0, tilt=45, yaw=-8,
                         lens=LENS, blur=BLUR, frame=h3d.S07_WIND)
    for c in (eye, cam):
        _near(c)
    anim.key(cam, "location", h3d.S07_CRACK, cam.location.copy(), "LINEAR")      # the final hit drifts (IM5)
    anim.key(cam, "location", h3d.LEN["S07"] + h3d.TAIL, cam.location + Vector((0.0, 0.06, 0.03)), "LINEAR")
    _flash(cam, [(h3d.S07_FLASH - 1, 0.0), (h3d.S07_FLASH, 0.9), (h3d.S07_FLASH + 1, 0.0)])
    return dict(frames=h3d.LEN["S07"] + h3d.TAIL, step=1, subject=[rig["root"]])


SHOTS = {"S04": s04, "S05a": s05a, "S07": s07}
