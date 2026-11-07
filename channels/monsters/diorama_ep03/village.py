"""Episode 3's shared village at night (channels/monsters/DIORAMA_EP03.md, "Villagers at night", helper 1).

The lane: the dirt track into helper 9's Ep 2 bell-keepers' village (diorama_ep02/helper9.village_and_lake), here
lined with huts at character scale (Kai is 8.7 units, a villager ~9): the same cream round walls and rust / brown
cone roofs, each with a hinged door, a window with two hinged shutters, a little porch with a bell on a bracket.
Night has no lanterns: Kai's mark is the only light (helper 9's mark light and night grade).

    from channels.monsters.diorama_ep03 import village as V
    huts = V.lane()                          # idempotent; huts[i]: root, door, shutters (2), bell, face, porch
    V.slam_door(huts[0], f)                  # open -> shut with an overshoot and a rattle, on 2s
    V.bang_shutters(huts[1], f)              # both shutters swing shut, a beat apart
    V.ring_bell(huts[2], f0, f1)             # the porch bell swings (ring lines are 2D, at assembly or in a post pass)
    v = V.villager(i, seed, net=True)        # Ep 2's villagers (helper 1, diorama_ep02/helper1.villager)
    V.back_off(v, p0, p1, f0, f1, look_at)   # stepping backwards on 2s, leaning away, the net held out like a ward
    V.scratcher(v, f0, f1)                   # one villager scratching a red itchy blotch on the forearm (comic)
    V.slip_inside(v, hut, f)                 # gone through its door at f (the door slams right after)

Positions are world units on helper 9's island; LANE_AT is the middle of the lane (Kai's spot in S03 and S09).
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import helper1 as e2
from channels.monsters.mk import anim, look

VILLAGE = Vector((6.0, -170.0, 0.0))        # helper 9's Ep 2 village square (diorama_ep02/helper9.VILLAGE)
LANE_AT = Vector((4.6, -131.0, 0.0))        # the middle of the lane: the track (0,-118) -> (5,-152) into the square
LANE_DIR = Vector((0.18, -1.0, 0.0)).normalized()      # down the lane, toward the square and the lake
LANE_HALF = 10.5                            # the lane's half width at the porches' edge (hut centres a bit further)
# (side: +1 = east of the lane, along: units down the lane from LANE_AT, radius, wall height, roof, door, shutters)
HUTS = [(+1, -15.0, 5.2, 9.8, 0, "#3f7f7a", "#3f7f7a"), (-1, -12.0, 5.5, 10.2, 1, "#a8452f", "#c98a3c"),
        (+1, 1.5, 5.6, 10.4, 1, "#5a6fa3", "#5a6fa3"), (-1, 4.5, 5.3, 9.9, 0, "#6f8f4a", "#a8452f"),
        (+1, 18.0, 5.4, 10.0, 0, "#c98a3c", "#3f7f7a"), (-1, 20.5, 5.6, 10.3, 1, "#3f7f7a", "#5a6fa3")]
DOOR_W, DOOR_H = 3.2, 7.2
OPEN_DOOR = 105.0                          # degrees, swung out against the wall
OPEN_SHUTTER = 115.0
BRASS = "#d9a93c"


def _side(s):
    return Vector((-LANE_DIR.y, LANE_DIR.x, 0.0)) * s          # +1: east of the lane (LANE_DIR is ~ -Y)


def _mat(name, hexc, **kw):
    return look.toon(name, look.hexc(hexc), **kw)


def _pivot(name, parent, loc, rot=(0.0, 0.0, 0.0)):
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.parent = parent
    e.location = loc
    e.rotation_euler = rot
    return e


def hut(i, at, face, r, h, roof, door_hex, shutter_hex):
    """One round hut at `at` (ground), its door facing `face` (unit, toward the lane). Local frame: the root's -Y is
    the facing (like the characters), so the door is at (0, -r) and the porch in front of it."""
    P = e2._prim
    root = bpy.data.objects.new(f"vhut{i}", None)
    bpy.context.scene.collection.objects.link(root)
    root.location = at
    root.rotation_euler = (0.0, 0.0, math.atan2(face.x, -face.y))
    wall = _mat("h9_hut_wall", "#efe0bf")
    rf = _mat(("h9_roof_rust", "h9_roof_brown")[roof % 2], ("#b4462e", "#8a5634")[roof % 2])
    wood = _mat("vhut_wood", "#7a4e2c")
    dark = look.flat("vhut_dark", look.hexc("#1b1520"))
    doorm = _mat(f"vhut_door{i}", door_hex)
    shm = _mat(f"vhut_shutter{i}", shutter_hex)
    brass = look.toon("vil_brass", look.hexc(BRASS), gloss=True)
    P("cylinder", f"vhut{i}_wall", wall, (0, 0, h / 2), parent=root, line=0.05, radius=r, depth=h, vertices=40)
    rh = r * 1.15
    P("cone", f"vhut{i}_roof", rf, (0, 0, h + rh / 2 - 0.3), parent=root, line=0.05, radius1=r * 1.35,
      radius2=0.15, depth=rh, vertices=32)
    # the doorway (dark, a frame round it) and the door on a hinge at its left edge (seen from the lane)
    y = -r - 0.05
    P("cube", f"vhut{i}_doorway", dark, (0, y + 0.2, DOOR_H / 2 + 0.05), (DOOR_W / 2, 0.3, DOOR_H / 2), parent=root,
      line=0.0, size=1.0)
    for sx in (-1, 1):
        P("cube", f"vhut{i}_jamb{sx}", wood, (sx * (DOOR_W / 2 + 0.2), y - 0.08, DOOR_H / 2 + 0.1),
          (0.2, 0.2, DOOR_H / 2 + 0.1), parent=root, size=1.0)
    P("cube", f"vhut{i}_lintel", wood, (0, y - 0.08, DOOR_H + 0.35), (DOOR_W / 2 + 0.4, 0.22, 0.22), parent=root,
      size=1.0)
    hinge = _pivot(f"vhut{i}_hinge", root, (-DOOR_W / 2, y - 0.22, 0.05))
    door = P("cube", f"vhut{i}_door", doorm, (DOOR_W / 2, 0, DOOR_H / 2), (DOOR_W / 2 - 0.05, 0.14, DOOR_H / 2),
             parent=hinge, size=1.0)
    for z in (0.28, 0.72):                                           # two dark iron straps
        P("cube", f"vhut{i}_strap{z}", dark, (DOOR_W / 2, -0.16, DOOR_H * z), (DOOR_W / 2 - 0.25, 0.03, 0.12),
          parent=hinge, line=0.0, size=1.0)
    P("uv_sphere", f"vhut{i}_knob", brass, (DOOR_W - 0.5, -0.25, DOOR_H * 0.5), parent=hinge, line=0.0,
      radius=0.16, segments=10, ring_count=6)
    # a window beside the door (on the wall, 40 degrees round), two shutters hinged at its outer edges
    a = math.radians(40.0 if i % 2 else -40.0)
    wc = Vector((math.sin(a) * (r + 0.05), -math.cos(a) * (r + 0.05), h * 0.6))
    win = _pivot(f"vhut{i}_win", root, wc, (0, 0, a))
    W = 1.9
    P("cube", f"vhut{i}_pane", dark, (0, 0.12, 0), (W / 2, 0.2, W / 2), parent=win, line=0.0, size=1.0)
    P("cube", f"vhut{i}_sill", wood, (0, -0.15, -W / 2 - 0.15), (W / 2 + 0.35, 0.25, 0.14), parent=win, size=1.0)
    shutters = []
    for sx in (-1, 1):
        sp = _pivot(f"vhut{i}_shpiv{sx}", win, (sx * W / 2, -0.12, 0))
        P("cube", f"vhut{i}_shutter{sx}", shm, (-sx * W / 4, 0, 0), (W / 4 - 0.03, 0.1, W / 2), parent=sp,
          size=1.0)
        for z in (-0.45, 0.0, 0.45):                                   # slats
            P("cube", f"vhut{i}_slat{sx}{z}", dark, (-sx * W / 4, -0.11, z * W / 2 * 1.3),
              (W / 4 - 0.15, 0.02, 0.05), parent=sp, line=0.0, size=1.0)
        shutters.append((sx, sp))
    # the porch: a plank deck in front of the door, two posts, a sloping plank awning, the bell on a bracket
    D = 3.0
    P("cube", f"vhut{i}_deck", wood, (0, -r - D / 2 + 0.3, 0.25), (DOOR_W / 2 + 1.7, D / 2, 0.25), parent=root,
      size=1.0)
    for sx in (-1, 1):
        P("cylinder", f"vhut{i}_post{sx}", wood, (sx * (DOOR_W / 2 + 1.4), -r - D + 0.5, 4.3), parent=root,
          radius=0.2, depth=8.6, vertices=8)
    P("cube", f"vhut{i}_awning", rf, (0, -r - D / 2 + 0.2, 8.9), (DOOR_W / 2 + 2.0, D / 2 + 0.5, 0.14),
      rot=(math.radians(-12), 0, 0), parent=root, size=1.0)
    bx = DOOR_W / 2 + 1.4
    P("cube", f"vhut{i}_bracket", wood, (bx, -r - D - 0.2, 8.1), (0.12, 0.75, 0.12), parent=root, size=1.0)
    bell = _pivot(f"vhut{i}_bellpiv", root, (bx, -r - D - 0.8, 8.0))
    P("cylinder", f"vhut{i}_bellcord", wood, (0, 0, -0.3), parent=bell, line=0.0, radius=0.05, depth=0.6,
      vertices=6)
    P("cone", f"vhut{i}_bell", brass, (0, 0, -1.15), parent=bell, line=0.03, radius1=0.85, radius2=0.28, depth=1.15,
      vertices=20)
    P("uv_sphere", f"vhut{i}_clapper", dark, (0, 0, -1.8), parent=bell, line=0.0, radius=0.14, segments=8,
      ring_count=6)
    return dict(root=root, door=hinge, shutters=shutters, bell=bell, face=face, r=r, h=h,
                porch=at + face * (r + D * 0.6), doorstep=at + face * (r + 0.6), window=root.matrix_world @ wc)


def lane():
    """The lane's six huts (idempotent: built once, then returned). Doors and shutters start open, bells still."""
    sc = bpy.context.scene
    if "_ep03_lane" in sc:
        return [_find(i) for i in range(len(HUTS))]
    huts = []
    for i, (s, along, r, h, roof, dh, sh) in enumerate(HUTS):
        at = LANE_AT + LANE_DIR * along + _side(s) * (LANE_HALF + r)
        huts.append(hut(i, at, -_side(s), r, h, roof, dh, sh))
        set_door(huts[-1], 1, 1.0)
        set_shutters(huts[-1], 1, 1.0)
    sc["_ep03_lane"] = 1
    bpy.context.view_layer.update()
    return huts


def _find(i):
    ob = bpy.data.objects
    s = HUTS[i][0]
    r, h = HUTS[i][2], HUTS[i][3]
    root = ob[f"vhut{i}"]
    face = -_side(s)
    win = ob[f"vhut{i}_win"]
    return dict(root=root, door=ob[f"vhut{i}_hinge"], shutters=[(-1, ob[f"vhut{i}_shpiv-1"]),
                                                                  (1, ob[f"vhut{i}_shpiv1"])],
                bell=ob[f"vhut{i}_bellpiv"], face=face, r=r, h=h, porch=root.location + face * (r + 1.8),
                doorstep=root.location + face * (r + 0.6), window=win.matrix_world.translation.copy())


# ------------------------------------------------------------------------------------------------ doors, shutters
def set_door(hut, f, open_, interp="CONSTANT"):
    """Key the door `open_` (1 = swung out against the wall, 0 = shut) at frame f."""
    anim.key(hut["door"], "rotation_euler", f, (0, 0, -math.radians(OPEN_DOOR) * open_), interp)


def set_shutters(hut, f, open_, interp="CONSTANT"):
    for sx, sp in hut["shutters"]:
        anim.key(sp, "rotation_euler", f, (0, 0, sx * math.radians(OPEN_SHUTTER) * open_), interp)


def slam_door(hut, f, swing=4):
    """The door swings shut over `swing` frames, hits at f (past shut a hair: the bounce), rattles, settles. On 2s."""
    set_door(hut, f - swing, 1.0)
    set_door(hut, f - swing // 2, 0.55)
    set_door(hut, f, -0.03)
    set_door(hut, f + 2, 0.06)
    set_door(hut, f + 4, 0.0)


def bang_shutters(hut, f, gap=2):
    """Both shutters slam shut (left at f, right `gap` frames later), each bouncing once."""
    for k, (sx, sp) in enumerate(hut["shutters"]):
        g = f + k * gap
        for df, o in ((-4, 1.0), (-2, 0.5), (0, -0.04), (2, 0.08), (4, 0.0)):
            anim.key(sp, "rotation_euler", g + df, (0, 0, sx * math.radians(OPEN_SHUTTER) * o), "CONSTANT")


def ring_bell(hut, f0, f1, amp=28.0, period=6, seed=0):
    """The porch bell swings side to side (about the lane-facing axis) from f0 to f1, on 2s, then damps out."""
    rnd = random.Random(seed)
    ph = rnd.uniform(0, math.tau)
    b = hut["bell"]
    for f in range(f0, f1 + 13, 2):
        damp = 1.0 if f <= f1 else max(0.0, 1.0 - (f - f1) / 12.0)
        a = math.radians(amp) * damp * math.sin(ph + (f - f0) * math.tau / period)
        anim.key(b, "rotation_euler", f, (a, 0.0, 0.0), "CONSTANT")


# ------------------------------------------------------------------------------------------------------ villagers
def villager(i, seed, net=True, bell=False):
    return e2.villager(i, seed, net=net, bell=bell)


def _yaw_to(p, q):
    d = q - p
    return math.atan2(d.x, -d.y)                 # the characters face their own -Y


def back_off(v, p0, p1, f0, f1, look_at, lean=10.0, stride=4):
    """Stepping backwards from p0 to p1 between f0 and f1 (eased, on 2s), facing `look_at`, leaning away from it with
    a little bob per step; the net (if any) is pushed out in front like a ward."""
    root, body = v["root"], v["body"]
    for f in range(f0, f1 + 1, 2):
        u = (f - f0) / max(1, f1 - f0)
        u = u * u * (3 - 2 * u)
        p = Vector(p0).lerp(Vector(p1), u)
        anim.key(root, "location", f, tuple(p), "CONSTANT")
        anim.key(root, "rotation_euler", f, (0, 0, _yaw_to(p, Vector(look_at))), "CONSTANT")
        step = ((f - f0) // stride) % 2
        anim.key(body, "location", f, (0, 0, 0.18 * step), "CONSTANT")
        anim.key(body, "rotation_euler", f, (math.radians(-lean * (0.6 + 0.4 * step)), 0,
                                             math.radians(3 * (1 - 2 * step))), "CONSTANT")
    pole = bpy.data.objects.get(f"{root.name}_pole")
    if pole is not None:                             # the net levelled forward at the threat
        for ob in [o for o in body.children if o.name.split("_")[-1] in ("pole", "hoop", "net")]:
            ob["_ward"] = 1
        ward = bpy.data.objects.get(f"{root.name}_ward")
        if ward is None:
            ward = _pivot(f"{root.name}_ward", body, (-1.1, -0.5, v["h"] * 0.45))
            for ob in list(body.children):
                if ob.get("_ward"):
                    M = ob.matrix_world.copy()
                    ob.parent = ward
                    ob.matrix_world = M
        anim.key(ward, "rotation_euler", f0, (0, 0, 0), "CONSTANT")
        anim.key(ward, "rotation_euler", f0 + 4, (math.radians(-38), 0, math.radians(-10)), "CONSTANT")
    return v


def slip_inside(v, hut, f):
    """The villager steps through its doorway at f: from f it stands inside the hut, out of sight."""
    inside = hut["root"].location - hut["face"] * 1.0
    anim.key(v["root"], "location", f, tuple(inside), "CONSTANT")
    anim.key(v["root"], "scale", f - 1, (1, 1, 1), "CONSTANT")
    anim.key(v["root"], "scale", f, (0.001, 0.001, 0.001), "CONSTANT")


def scratcher(v, f0, f1, rate=4):
    """One villager scratching a red itchy blotch on the left forearm (raised across the chest, sleeve pushed up):
    the right hand rubs back and forth on 2s, the eyes squeezed shut, a small wince. Comic, not gross: one flat red
    blotch, no swelling, no blood."""
    body, h, i = v["body"], v["h"], v["root"].name[3:]
    P = e2._prim
    cloak = bpy.data.materials[f"vil_cloak{i}"]
    skin = bpy.data.materials[f"vil_skin{i}"]
    red = look.toon("vil_blotch", look.hexc("#e04a4a"), shade=0.8, rim=0.1)
    fore = _pivot(f"vil{i}_scr_fore", body, (0.9, -1.25, h * 0.55), (0, 0, math.radians(-8)))
    P("cylinder", f"vil{i}_scr_sleeve", cloak, (0.9, 0, 0), (1, 1, 1), rot=(0, math.radians(90), 0), parent=fore,
      radius=0.42, depth=1.1, vertices=12)
    P("cylinder", f"vil{i}_scr_arm", skin, (-0.45, 0, 0), (1, 1, 1), rot=(0, math.radians(90), 0), parent=fore,
      radius=0.33, depth=1.7, vertices=12)
    P("uv_sphere", f"vil{i}_scr_lhand", skin, (-1.45, 0, 0.05), parent=fore, radius=0.36, segments=12,
      ring_count=8)
    P("cylinder", f"vil{i}_scr_blotch", red, (0.05, -0.3, 0.05), (1.25, 1.0, 0.9), rot=(math.radians(90), 0, 0),
      parent=fore, line=0.0, radius=0.32, depth=0.06, vertices=16)
    hx, hy, hz = 0.2, -1.78, h * 0.55 + 0.12                           # the rubbing hand, beside the blotch
    hand = _pivot(f"vil{i}_scr_hand", body, (hx, hy, hz))
    P("uv_sphere", f"vil{i}_scr_rhand", skin, (0, 0, 0), (1.0, 0.8, 0.9), parent=hand, radius=0.4, segments=12,
      ring_count=8)
    P("cylinder", f"vil{i}_scr_rarm", cloak, (-0.75, 0.3, -0.3), (1, 1, 1),
      rot=(0, math.radians(-70), math.radians(20)), parent=hand, radius=0.38, depth=1.6, vertices=12)
    for f in range(f0, f1 + 1, 2):                       # scritch-scritch on 2s, a bigger rub every 3rd stroke
        k = ((f - f0) // 2) % rate
        dx = (0.0, 0.32, 0.0, -0.32)[k] * (1.4 if ((f - f0) // (2 * rate)) % 3 == 2 else 1.0)
        anim.key(hand, "location", f, (hx + dx, hy, hz + 0.06 * (k % 2)), "CONSTANT")
        anim.key(body, "rotation_euler", f, (math.radians(4), 0, math.radians(4 * (1 if k < 2 else -1))),
                 "CONSTANT")
    for sx in (-1, 1):                                    # eyes squeezed into lines: the itch face
        e = bpy.data.objects[f"vil{i}_eye{sx}"]
        anim.key(e, "scale", f0, (1.6, 0.5, 0.28), "CONSTANT")
    return dict(hand=hand, fore=fore)
