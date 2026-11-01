"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md), helper 1's shots:

    S02 "The bird dived first."  Low from the pond's south-west side, the thorn tree far behind: the tiny shrimp drinks
        at the water's edge (it hasn't seen anything). The butcher bird (its dark predator form, as in Ep 1's dive)
        glides in high from the thorn side, gives one hitch (anticipation), folds its wings into a dart and plunges
        at it, accelerating; its giant shadow slides across the grass and spreads over the shrimp. The 2D pass adds
        streaming speed lines behind the bird. Camera: a slow push-in on 1s; characters on 2s.
    S04 "Its talons got my arm instead."  (see s04)
    S16 "Then came the bells."  (see s16)

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S02 OUT [--frames A-B] [--still N --scale 0.5]
    FPS=24 python channels/monsters/diorama_ep02/post_helper1.py S02        (the 2D pass, the mp4 and the sheet)
"""
import json
import math
import os

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as v2
from channels.monsters.mk import anim, butcherbird, diorama, look, tuftwing

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
GUESS = {"S02": 45, "S04": 66, "S16": 47}


def _frames(shot):
    from channels.monsters.diorama_ep02.shots import ep02_frames        # lazy: shots.py imports this module
    try:
        return ep02_frames(shot)
    except (OSError, KeyError, ValueError):
        return GUESS[shot]


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _local(rot, v, scale):
    """A world-space offset in a bird root's frame (turned by `rot` about Z, scaled by `scale`)."""
    c, s = math.cos(-rot), math.sin(-rot)
    return Vector(((v[0] * c - v[1] * s) / scale, (v[0] * s + v[1] * c) / scale, v[2] / scale))


def _anchors(shot, cam, pts, n):
    """Screen positions (720x1280, top-left origin) per frame of `pts` (name -> callable(frame) -> world point) for
    the 2D pass: build/monsters/diorama_ep02/<shot>_anchors.json."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        row = {}
        for k, fn in pts.items():
            v = world_to_camera_view(sc, cam, fn(f))
            row[k] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1), round(v.z, 2))
        out[f] = row
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def _world(n):
    """The island as Episode 1 left it (the cut grove's stumps, the thorn tree), no Kai lying down; returns the
    island dict (diorama_v3/xprl._set)."""
    from channels.monsters.diorama_v3 import xprl as xv3               # lazy (it pulls in the v3 registry)
    diorama.setup()
    isl, _ = xv3._set(n, kai_down=False)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    return isl


# ------------------------------------------------------------------------------------------------------------ S02
F_HITCH, F_FOLD, F_END = 7, 11, 45          # the hitch up, the wings folded into a dart, the plunge (eased in) to here
START = Vector((7.4, 5.1, 10.5))           # the bird's ball centre at frame 1 (world offset from the shrimp)
STOP = Vector((0.9, 0.6, 2.6))              # where the plunge has got to at F_END (the cut is at 33: still above it)


def _plunge(rig, rot, scale, n):
    """Glide (wings spread, a slight sink), the hitch (a small rise, wings up), the fold (wings swept back and tucked,
    body stretched to a dart, head pitched down at the prey, tail up, crest flat), then the plunge: accelerating along
    a slightly bowed line. The giant shadow slides in under it and spreads over the shrimp. Keys on 1s for the path
    (the camera reads it as smooth), the pose on 2s (anim.on_twos)."""
    lift = rig["lift"]
    c = Vector(tuftwing.CENTER)
    hitch = START + Vector((-0.6, -0.4, 0.5))
    for f in range(1, n + 1):
        if f <= F_HITCH:
            u = (f - 1) / (F_HITCH - 1)
            p = START.lerp(START + Vector((-0.6, -0.4, -0.2)), u)
        elif f <= F_FOLD:
            u = _ease((f - F_HITCH) / (F_FOLD - F_HITCH))
            p = (START + Vector((-0.6, -0.4, -0.2))).lerp(hitch, u)
        else:
            u = ((f - F_FOLD) / (F_END - F_FOLD)) ** 1.7                 # accelerating
            p = hitch.lerp(STOP, u)                                     # a straight plunge
        anim.key(lift, "location", f, tuple(_local(rot, p, scale) - c), "LINEAR")
    # the pose (on 2s)
    for sx, w in zip((-1, 1), rig["wings"]):
        anim.key(w, "rotation_euler", 1, (0, -sx * 1.25, 0))                # spread: gliding
        anim.key(w, "scale", 1, (1.6, 1.6, 1.6))
        anim.key(w, "rotation_euler", F_HITCH, (0, -sx * 1.45, 0))         # up for the hitch
        anim.key(w, "scale", F_HITCH, (1.7, 1.7, 1.7))
        anim.key(w, "rotation_euler", F_FOLD, (0, -sx * 0.5, 0))             # swept back for the plunge (as
        anim.key(w, "scale", F_FOLD, (1.15, 1.15, 1.15))                     # butcherbird.dive), then tucked in
        anim.key(w, "rotation_euler", F_FOLD + 6, (0, -sx * 0.32, 0))
        anim.key(w, "scale", F_FOLD + 6, (1.0, 1.0, 1.0))
    body, head = rig["body"], rig["head"]
    anim.squash(body, 1, 0.0)
    anim.squash(body, F_HITCH, -0.1)                                        # bunched for the hitch
    anim.squash(body, F_FOLD, 0.3)                                          # stretched into a dart
    anim.squash(body, F_FOLD + 2, 0.24)
    anim.key(body, "rotation_euler", 1, (0.2, 0, 0))
    anim.key(body, "rotation_euler", F_FOLD, (0.35, 0, 0))                  # nose down along the plunge
    anim.key(head, "rotation_euler", 1, (0.3, 0, 0))
    anim.key(head, "rotation_euler", F_HITCH, (0.15, 0, 0))
    anim.key(head, "rotation_euler", F_FOLD, (0.5, 0, 0))                   # eyes locked on the prey
    anim.key(rig["tail"], "rotation_euler", 1, (0.2, 0, 0))
    anim.key(rig["tail"], "rotation_euler", F_FOLD, (0.55, 0, 0))
    anim.key(rig["crest"], "rotation_euler", 1, (-0.2, 0, 0))
    anim.key(rig["crest"], "rotation_euler", F_FOLD, (-0.6, 0, 0))          # flattened by the wind
    butcherbird.stare(rig, 1, down=0.3)                                     # the glare (eyes narrowed, slanted)
    # the giant shadow (its tell): from under its line of flight it slides onto the shrimp and spreads over it
    sh = rig["shadow"]
    z = sh.location.z
    for f in range(1, n + 1, 2):
        u = _ease((f - 1) / (F_END - 1))
        g = Vector((START.x, START.y, 0)).lerp(Vector((0.4, 0.3, 0)), u ** 0.8)
        lo = _local(rot, g, scale)
        anim.key(sh, "location", f, (lo.x, lo.y, z), "LINEAR")
        s = 0.55 + 0.75 * u
        anim.key(sh, "scale", f, (s, s, 1), "LINEAR")
    anim.on_twos([body, head, rig["tail"], rig["crest"], sh] + rig["eyes"] + rig["wings"], step=2)


def s02():
    from channels.monsters.diorama_v3 import xprl as xv3
    n = _frames("S02")
    isl = _world(n)
    sh = xv3._shrimp(n)                                                 # drinking: it hasn't seen it
    shrimp = Vector(xv3.SHRIMP)
    scale = xv3.BIRD_SCALE
    rig = tuftwing.build((shrimp.x, shrimp.y, 0.0), shadow_span=10.0)
    rig["root"].scale = (scale,) * 3
    d = -START                                                          # it flies toward the shrimp
    rot = math.atan2(d.x, -d.y)
    rig["root"].rotation_euler.z = rot
    _plunge(rig, rot, scale, n)
    xv3.dark_form(1)                                                    # the predator form (Ep 1's dive)
    for e in sh["eyes"]:                                                # it only feels the shadow at the end
        anim.key(e, "scale", 37, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 39, (0.8, 1, 0.8), "CONSTANT")
    # low from the south-west, looking up the line the bird comes down: the shrimp low in frame, the thorn tree far
    # behind and up, the bird big against the sky as it comes; a slow push-in on 1s
    from channels.monsters.diorama_ep02.xprl import _cam_move           # (XprL's gentler blur and farther haze)
    yaw = math.degrees(math.atan2(START.x, START.y)) - 90.0             # side-on to the dive: a big diagonal
    tgt = shrimp + Vector((START.x * 0.42, START.y * 0.42, 4.6))
    a = (tuple(tgt), 21.0, 12.0, yaw, 30.0, 0.0)
    b = (tuple(tgt + Vector((-0.5, -0.35, -0.5))), 18.5, 12.0, yaw + 2.0, 30.0, 0.0)
    cam = _cam_move("cam_s02", n, a, b)
    lift = rig["lift"]
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {rig["root"], *rig["root"].children_recursive, sh["root"], *sh["root"].children_recursive}
    _clear_view(cam, [1, n], shrimp, keep, reach=0.9)

    def bird_at(f):
        return lift.matrix_world.translation.copy()
    _anchors("S02", cam, {"bird": bird_at, "shrimp": lambda f: shrimp + Vector((0, 0, 0.8))}, n)
    del isl
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["root"], sh["root"]])


# ------------------------------------------------------------------------------------------------------------ S16
HILL = dict(center=(-3.6, -48.0), rx=19.0, ry=9.0, h=7.0)   # a grassy rise across the south path (the villagers'
                                                            # side): they come up over its crest toward Kai
CLOAKS = ("#b4643c", "#7d8f5a", "#6f5a8c", "#c99a4a", "#8a5a46", "#4f7a78", "#a8834e")
HATS = ("#d8b874", "#5b4636", "#c4a060", "#3f4f5c")
SKINS = ("#f2c9a2", "#d9a77c", "#b77f58", "#f0d0b4")
BRASS = "#d9a93c"


def hill_height(x, y):
    c, rx, ry, h = HILL["center"], HILL["rx"], HILL["ry"], HILL["h"]
    q = 1.0 - ((x - c[0]) / rx) ** 2 - ((y - c[1]) / ry) ** 2
    return h * math.sqrt(q) if q > 0 else 0.0


def hill():
    """The rise on the south path, in the island's own grass (a squashed half-ellipsoid; the path's dirt ribbon is
    laid over its crest). Import it in any ep02 shot that looks south past Kai (S16-S18), so the hill stays put."""
    if "ep02_hill" in bpy.data.objects:
        return bpy.data.objects["ep02_hill"]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=24, radius=1.0,
                                         location=(*HILL["center"], 0.0))
    o = bpy.context.object
    o.name = "ep02_hill"
    o.scale = (HILL["rx"], HILL["ry"], HILL["h"])
    bpy.ops.object.shade_smooth()
    grass = bpy.data.materials.get("diorama_grass") or diorama.grass_lit()
    o.data.materials.append(grass)
    import bmesh
    me = bpy.data.meshes.new("ep02_hill_path")                     # the path's dirt over the crest
    bm = bmesh.new()
    rows = []
    for i in range(25):
        y = HILL["center"][1] - HILL["ry"] + 2 * HILL["ry"] * i / 24
        x = diorama._path_x(y)
        w = 2.6
        rows.append([bm.verts.new((x + dx, y, hill_height(x + dx, y) + 0.06)) for dx in (-w, -w / 2, 0, w / 2, w)])
    for r0, r1 in zip(rows, rows[1:]):
        for j in range(4):
            bm.faces.new((r0[j], r0[j + 1], r1[j + 1], r1[j]))
    bm.to_mesh(me)
    bm.free()
    po = bpy.data.objects.new("ep02_hill_path", me)
    bpy.context.scene.collection.objects.link(po)
    dirt = bpy.data.materials.get("path_dirt") or diorama.lit_paint("path_dirt", "#8a6a48", "#b48c5e", "#d9b583")
    po.data.materials.append(dirt)
    return o


def _prim(kind, name, mat, loc, scale=(1, 1, 1), rot=(0, 0, 0), parent=None, line=0.03, **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(location=loc, rotation=rot, **kw)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    if kind in ("uv_sphere", "cone", "cylinder", "torus"):
        bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    if parent is not None:
        o.parent = parent
    look.outline(o, line)
    return o


def villager(i, seed, net=True, bell=False):
    """A small stylised villager (about 9 units, an adult beside 8.7-unit Kai): a bell-shaped hooded cloak, a round
    face under a wide hat, and a long-handled net held up on the shoulder or a hand bell raised and ringing. Built
    from primitives round an empty `root` (origin at the feet, facing -Y); `bell_at` is the bell's empty."""
    import random
    r = random.Random(seed)
    cloak = look.toon(f"vil_cloak{i}", look.hexc(CLOAKS[i % len(CLOAKS)]))
    hatm = look.toon(f"vil_hat{i}", look.hexc(HATS[r.randrange(len(HATS))]))
    skin = look.toon(f"vil_skin{i}", look.hexc(SKINS[r.randrange(len(SKINS))]))
    pole = look.toon("vil_pole", look.hexc("#7a5636"))
    netm = look.toon("vil_net", look.hexc("#efe6cf"))
    ink = look.flat("vil_ink", look.hexc("#231a22"))
    root = bpy.data.objects.new(f"vil{i}", None)
    bpy.context.scene.collection.objects.link(root)
    body = bpy.data.objects.new(f"vil{i}_body", None)                 # bobs and sways on 2s
    bpy.context.scene.collection.objects.link(body)
    body.parent = root
    h = r.uniform(8.6, 9.6)
    _prim("cone", f"vil{i}_cloak", cloak, (0, 0, h * 0.36), (1, 1, 1), parent=body, radius1=1.55, radius2=0.7,
          depth=h * 0.72, vertices=24)
    _prim("uv_sphere", f"vil{i}_head", skin, (0, 0, h * 0.8), (1, 1, 1.05), parent=body, radius=h * 0.12,
          segments=24, ring_count=12)
    _prim("cylinder", f"vil{i}_brim", hatm, (0, 0, h * 0.86), (1, 1, 1), parent=body, radius=h * 0.22, depth=0.18,
          vertices=28)
    _prim("cone", f"vil{i}_crown", hatm, (0, 0, h * 0.93), (1, 1, 1), parent=body, radius1=h * 0.12,
          radius2=h * 0.04, depth=h * 0.13, vertices=20)
    for sx in (-1, 1):                                                 # two dot eyes, facing -Y
        _prim("uv_sphere", f"vil{i}_eye{sx}", ink, (sx * h * 0.045, -h * 0.112, h * 0.8), (1, 0.5, 1.3),
              parent=body, line=0.0, radius=h * 0.016, segments=10, ring_count=6)
    out = dict(root=root, body=body, h=h, bell=None)
    if net:                                                            # a long pole over the right shoulder, net up
        tilt = math.radians(r.uniform(14, 26))
        L = h * 1.05
        base = Vector((-1.1, -0.5, h * 0.45))
        d = Vector((-math.sin(tilt) * 0.5, math.sin(tilt) * 0.3, math.cos(tilt))).normalized()
        mid = base + d * L / 2
        _prim("cylinder", f"vil{i}_pole", pole, tuple(mid), (1, 1, 1),
              rot=d.to_track_quat("Z", "Y").to_euler(), parent=body, radius=0.09, depth=L, vertices=8)
        top = base + d * L
        _prim("torus", f"vil{i}_hoop", pole, tuple(top + d * 0.9), (1, 1, 1),
              rot=(math.radians(80), 0, math.radians(r.uniform(-30, 30))), parent=body, line=0.02,
              major_radius=1.0, minor_radius=0.07)
        _prim("cone", f"vil{i}_net", netm, tuple(top + d * 0.9 + Vector((0, 0.15, -0.9))), (1, 1, 1),
              rot=(math.radians(-10), 0, 0), parent=body, line=0.02, radius1=0.15, radius2=0.95, depth=1.7,
              vertices=16)
    if bell:                                                           # a hand bell held up on the left
        arm = cloak
        _prim("cylinder", f"vil{i}_arm", arm, (1.25, -0.35, h * 0.66), (1, 1, 1),
              rot=(math.radians(-15), math.radians(-28), 0), parent=body, radius=0.32, depth=h * 0.3, vertices=10)
        hold = bpy.data.objects.new(f"vil{i}_bellhold", None)
        bpy.context.scene.collection.objects.link(hold)
        hold.parent = body
        hold.location = (1.75, -0.5, h * 0.84)
        brass = look.toon("vil_brass", look.hexc(BRASS), gloss=True)
        _prim("uv_sphere", f"vil{i}_hand", skin, (0, 0, 0), (1, 1, 1), parent=hold, radius=0.36, segments=12,
              ring_count=8)
        _prim("cylinder", f"vil{i}_handle", pole, (0, 0, -0.45), (1, 1, 1), parent=hold, radius=0.12, depth=0.6,
              vertices=8)
        _prim("cone", f"vil{i}_bell", brass, (0, 0, -1.05), (1, 1, 1), parent=hold, radius1=0.62, radius2=0.22,
              depth=0.85, vertices=20)
        out["bell"] = hold
    return out


VILLAGERS = [   # (x offset from the path, start y behind the crest, delay in frames, net, bell)
    (-0.3, -56.0, 0, False, True), (3.4, -57.5, 3, True, False), (-3.8, -57.0, 6, True, False),
    (1.6, -59.5, 8, True, True), (-2.2, -60.5, 11, True, False), (5.8, -61.0, 13, True, False),
    (-6.2, -62.0, 15, False, True),
]


def _clear_smoke(cam, frames, target):
    """The stumps' smoke puffs that would drift across the lens between Kai and `target` (the dollhouse cutaway):
    hidden if in frame and nearer than the target at any of `frames`."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    far = None
    hide = set()
    for f in frames:
        sc.frame_set(f)
        far = (target - cam.matrix_world.translation).length
        for o in sc.objects:
            if not o.name.startswith("puff"):
                continue
            v = world_to_camera_view(sc, cam, o.matrix_world.translation)
            if -0.3 < v.x < 1.3 and -0.3 < v.y < 1.3 and 0 < v.z < far:
                hide.add(o)
    for o in hide:
        for c in [o] + list(o.children_recursive):
            c.hide_render = True
    sc.frame_set(1)


def s16():
    from channels.monsters.diorama_ep02 import xprl as xp
    n = _frames("S16")
    xp._world(n)
    hill()
    k = xp._kai()
    PK = __import__("channels.monsters.ep01v2.xprl", fromlist=["Pose"]).Pose(k)
    for f in range(1, n + 1, 2):                                       # Kai holds the shrimp, his back to us; on the
        PK.reset()                                                     # first ring his head comes up (a little start)
        xp._cup(PK)
        lift = 6 * _ease((f - 3) / 6)
        PK.rot("chest", (2 * math.sin(f / 18.0) - lift * 0.3, 0, 0))
        PK.rot("head 1", (-4 - lift, 3 * math.sin(f / 30.0), 0))
        PK.key(f)
    v2._twos([k["arm"]])
    vil, bells = [], {}
    speed = 0.3                                                        # units per frame (a brisk march)
    for i, (dx, y0, delay, net, bell) in enumerate(VILLAGERS):
        v = villager(i, 11 + i * 7, net=net, bell=bell)
        x0 = diorama._path_x(y0) + dx
        target = Vector((xp.KAI_AT.x + dx * 0.4, xp.KAI_AT.y - 6.0, 0))
        d = (target - Vector((x0, y0, 0))).normalized()
        v["root"].rotation_euler.z = math.atan2(d.x, -d.y)
        for f in range(1, n + 1, 2):                                   # on 2s: walk, bob, sway
            t = max(0, f - delay)
            p = Vector((x0, y0, 0)) + d * speed * t
            p.z = hill_height(p.x, p.y)
            anim.key(v["root"], "location", f, tuple(p), "CONSTANT")
            ph = t * 0.42 + i
            anim.key(v["body"], "location", f, (0, 0, 0.22 * abs(math.sin(ph))), "CONSTANT")
            anim.key(v["body"], "rotation_euler", f, (0, 0.06 * math.sin(ph), 0), "CONSTANT")
            if v["bell"] is not None:                                 # the bell swings hard: ring, ring
                anim.key(v["bell"], "rotation_euler", f, (0.55 * math.sin(f * 1.3 + i), 0, 0), "CONSTANT")
        vil.append(v)
        if v["bell"] is not None:
            bells[f"bell{i}"] = v["bell"]
    # over Kai's right shoulder, low (XprL's S17 eye line), looking down the path at the rise; a slow push-in on 1s
    crest = Vector((diorama._path_x(HILL["center"][1]), HILL["center"][1] + 1.5, HILL["h"] + 3.0))
    back = Vector((xp.KAI_AT.x - crest.x, xp.KAI_AT.y - crest.y, 0)).normalized()
    side = Vector((back.y, -back.x, 0))                                # his right as he faces the hill
    eye = xp.KAI_AT + back * 7.5 + side * 1.6 + Vector((0, 0, 11.0))  # behind and above his right shoulder
    v = crest - eye
    dist = v.length
    tilt = math.degrees(math.asin(-v.z / dist))
    yaw = math.degrees(math.atan2(v.x, v.y))
    cam = xp._cam_move("cam_s16", n, (tuple(crest), dist, tilt, yaw, 30.0, -0.12),
                       (tuple(crest), dist - 3.0, tilt, yaw, 30.0, -0.12))
    _clear_smoke(cam, [1, n // 2, n], crest)
    pts = {name: (lambda f, o=o: o.matrix_world.translation.copy() + Vector((0, 0, -1.0)))
           for name, o in bells.items()}
    _anchors("S16", cam, pts, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"]] + [v["root"] for v in vil])


# ------------------------------------------------------------------------------------------------------------ S04
F_RAKE = 15                 # the talons cross his forearm ("Its TALONS got my arm"): the 2D slash lands here
KNEEL_AT = Vector((4.9, -2.6, 0.0))   # on his knees just south of the shrimp's drinking spot (S03's slide ends here)
KNEEL_YAW = -40.0           # facing south-west: toward the camera, his back to the thorn tree the bird comes from


def kneel(P, look_up=0.0, curl=0.0, flinch=0.0, rake_arm=0.0):
    """On his knees, sitting back a little, the shrimp cupped in both hands at his chest. look_up (0-1): chin up to
    the bird above and behind; curl (0-1): hunched over his hands, head down, shoulders round (shielding it);
    flinch (0-1): the jolt as the talons hit (shoulders up, head away); rake_arm (0-1): the right forearm knocked
    out and down by the talons."""
    from channels.monsters.diorama_ep02 import xprl as xp
    P.reset()
    h0 = P.pb["hips"].matrix.translation.z
    hip_z = P.l1 * 0.92 + P.ankle_h * 0.5 - 0.06 * curl
    P.hips(Vector((0, 0.04 + 0.03 * curl, hip_z - h0)))
    for side, sx in (("L", 1), ("R", -1)):                               # knees forward on the grass, shins back
        P.leg(side, Vector((sx * 0.11, P.l2 * 0.92 + 0.06, P.ankle_h * 0.7)))
    xp._cup(P)
    P.rot("spine", (8 + 26 * curl - 6 * flinch, 0, 0))
    P.rot("chest", (4 + 18 * curl - 8 * look_up, 0, 4 * flinch))
    P.rot("neck", (-10 * look_up + 14 * curl, 0, 0))
    P.rot("head 1", (-26 * look_up + 22 * curl + 6 * flinch, 0, -14 * flinch))
    for nm, sx in (("shoulder.L", 1), ("shoulder.R", -1)):
        P.rot(nm, (0, sx * (8 * flinch + 6 * curl), 0))                   # shoulders up
    if rake_arm:
        P.aim("forearm.R", (-0.35 - 0.25 * rake_arm, -0.75, -0.25 * rake_arm))
        P.aim("hand.R", (-0.5, -0.7, -0.3 * rake_arm))


def s04():
    from channels.monsters.diorama_ep02 import xprl as xp
    from channels.monsters.diorama_v3 import xprl as xv3
    from channels.monsters.ep01v2.xprl import Pose
    from channels.monsters.mk import acting, hero
    n = _frames("S04")
    _world(n)
    k = hero.load((0, 0, 0), scale=xp.SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    k["arm"].rotation_euler = (0, 0, math.radians(KNEEL_YAW))
    k["arm"].location = KNEEL_AT
    bpy.context.view_layer.update()
    hero.line_width(k, 0.0028)
    P = Pose(k)
    beats = [(1, dict(look_up=0.9)), (9, dict(look_up=1.0)),                      # eyes up: it's coming
             (13, dict(look_up=0.7, flinch=0.3)),                                     # anticipation: a small duck
             (F_RAKE, dict(look_up=0.2, flinch=1.0, rake_arm=1.0)),                  # HIT: the arm knocked out
             (F_RAKE + 2, dict(look_up=0.0, flinch=0.9, rake_arm=0.8, curl=0.3)),
             (F_RAKE + 6, dict(curl=1.1, flinch=0.4, rake_arm=0.2)),                 # curls round the shrimp (past)
             (F_RAKE + 10, dict(curl=1.0, flinch=0.2)),                               # settle
             (F_RAKE + 24, dict(curl=0.95, flinch=0.1)), (n, dict(curl=0.95))]
    for f, kw in beats:
        kneel(P, **kw)
        P.key(f)
    for f in range(F_RAKE + 26, n + 1, 4):                                         # a tremble on 2s
        kneel(P, curl=0.95 + 0.03 * math.sin(f), flinch=0.08)
        P.key(f)
    v2._twos([k["arm"]])
    # the shrimp in his cupped hands (scooped in S03): it rides with them, facing out, on 2s
    shr = xv3._shrimp(n)
    shr["root"].scale = (0.62,) * 3
    for f in range(1, n + 1, 2):
        bpy.context.scene.frame_set(f)
        hl = k["arm"].matrix_world @ k["arm"].pose.bones["hand.L"].tail
        hr = k["arm"].matrix_world @ k["arm"].pose.bones["hand.R"].tail
        mid = (hl + hr) / 2 + Vector((0, 0, 0.05))
        anim.key(shr["root"], "location", f, tuple(mid), "CONSTANT")
        anim.key(shr["root"], "rotation_euler", f, (0, 0, math.radians(KNEEL_YAW)), "CONSTANT")
    bpy.context.scene.frame_set(1)
    acting.EXPR.setdefault("wince", {"eye_V": 1.0, "mouth_wide": 0.7, "eye_brow_down": 0.4})
    acting.expression(k, "fear", 1, value=0.9)
    acting.expression(k, "wince", F_RAKE)
    acting.expression(k, "wince", F_RAKE + 20, value=0.85)
    acting.blink(k, 1, F_RAKE - 2, at=(5,))
    # the bird: from high behind him (the thorn side) it swoops down past his right forearm, talons first, then
    # beats up and away over his left (screen left), climbing
    face = Vector((math.sin(math.radians(KNEEL_YAW)), -math.cos(math.radians(KNEEL_YAW)), 0))   # his front (-Y)
    right = Vector((face.y, -face.x, 0))                                             # his right (-X)
    bpy.context.scene.frame_set(F_RAKE)
    pb = k["arm"].pose.bones["forearm.R"]
    elbow = k["arm"].matrix_world @ pb.head
    wrist = k["arm"].matrix_world @ pb.tail
    bpy.context.scene.frame_set(1)
    hit = elbow.lerp(wrist, 0.55) + right * 0.6 + Vector((0, 0, 0.6))
    p0 = hit - face * 9.0 + right * 3.0 + Vector((0, 0, 9.0))                 # high behind his right shoulder
    p2 = hit + face * 6.0 - right * 9.0 + Vector((0, 0, 10.0))                # away past the camera's left, up
    scale = xv3.BIRD_SCALE
    rig = tuftwing.build((hit.x, hit.y, 0.0), shadow_span=10.0)
    rig["root"].scale = (scale,) * 3
    c = Vector(tuftwing.CENTER)
    d_in = (hit - p0)
    rot = math.atan2(d_in.x, -d_in.y)
    rig["root"].rotation_euler.z = rot
    lift = rig["lift"]
    for f in range(1, n + 1):
        if f <= F_RAKE:
            u = ((f - 1) / (F_RAKE - 1)) ** 1.6                                        # accelerating down
            p = p0.lerp(hit, u)
        else:
            u = min(1.0, (f - F_RAKE) / 22.0)
            e = 1 - (1 - u) ** 2                                                      # bursting away, slowing
            p = hit.lerp(p2, e) + Vector((0, 0, -2.5)) * math.sin(math.pi * e) * 0.5
        anim.key(lift, "location", f, tuple(_local(rot, p - Vector((hit.x, hit.y, 0)), scale) - c), "LINEAR")
        if f > F_RAKE + 26:
            break
    anim.key(lift, "location", F_RAKE + 30, tuple(_local(rot, p2 + face * 20 - Vector((hit.x, hit.y, 0)), scale) - c),
             "LINEAR")
    for sx, w in zip((-1, 1), rig["wings"]):
        anim.key(w, "rotation_euler", 1, (0, -sx * 0.5, 0))                          # swept back in the dive
        anim.key(w, "rotation_euler", F_RAKE - 3, (0, -sx * 1.4, 0))                 # flared to brake...
        anim.key(w, "scale", F_RAKE - 3, (1.6, 1.6, 1.6))
    anim.key(rig["body"], "rotation_euler", F_RAKE - 3, (-0.5, 0, 0))                # ...feet (talons) thrown forward
    anim.key(rig["body"], "rotation_euler", F_RAKE + 4, (0.3, 0, 0))
    tuftwing.flutter(rig, F_RAKE + 2, flaps=5, amount=1.4)                          # beating hard to climb away
    butcherbird.stare(rig, 1, down=0.45)
    xv3.dark_form(1)
    sh = rig["shadow"]                                                               # its shadow sweeps over him
    z = sh.location.z
    for f in range(1, n + 1, 2):
        u = min(1.0, (f - 1) / (F_RAKE + 20))
        g = (p0.lerp(hit, min(1.0, u * 1.6)) if u < 0.62 else hit.lerp(p2, (u - 0.62) / 0.38))
        lo = _local(rot, Vector((g.x - hit.x, g.y - hit.y, 0)), scale)
        anim.key(sh, "location", f, (lo.x, lo.y, z), "LINEAR")
    anim.on_twos([o for o in tuftwing._animated(rig) if o is not lift], step=2)    # the swoop path stays on 1s
    # in front of him, a little to his right and low: his face, the cupped hands and the right forearm; the bird
    # comes down out of the top of frame behind his shoulder; a slow push-in on 1s
    chest = KNEEL_AT + Vector((0, 0, 4.0))
    cam_dir = (face * 1.0 - right * 0.35).normalized()
    yaw = math.degrees(math.atan2(-cam_dir.x, -cam_dir.y))
    a = (tuple(chest + Vector((0, 0, 1.6))), 13.0, 9.0, yaw, 36.0, -0.1)
    b = (tuple(chest + Vector((0, 0, 1.4))), 11.0, 9.0, yaw - 2.0, 36.0, -0.1)
    cam = xp._cam_move("cam_s04", n, a, b)
    _clear_smoke(cam, [1, n // 2, n], chest)

    def bone(name, tail=False):
        def fn(f):
            pbn = k["arm"].pose.bones[name]
            return k["arm"].matrix_world @ (pbn.tail if tail else pbn.head)
        return fn
    from channels.monsters.ep01v2 import bgqrs as s3d
    pts = {"elbow": bone("forearm.R"), "wrist": bone("forearm.R", True),
           "bird": lambda f: lift.matrix_world.translation.copy(),
           "eye_l": lambda f: s3d.kai_point(k, "eye_l"), "eye_r": lambda f: s3d.kai_point(k, "eye_r")}
    _anchors("S04", cam, pts, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], rig["root"], shr["root"]])


SHOTS = {"S02": s02, "S04": s04, "S16": s16}
