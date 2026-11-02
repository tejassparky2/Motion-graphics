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
DIVE = (0.74, 0.95)         # how far down bGqrs's dive line (thorn perch -> the shrimp's back) the bird is at the
                            # first and last frame: S01 ends at 0.74; S03 shows only its shadow; S04 has it on top
S02_CAM = dict(toward=0.45, lift=0.6, dist=12.0, push=1.5, tilt=9.0, lens=35.0, shift=-0.04)
F_FOLD = 7                  # the wings snap shut into a dart (spread and flared just before: the anticipation)


def _fold(rig, n):
    """Re-key the wings over butcherbird.dive's: spread wide at the start, flared once more, then folded tight along
    the body (a dart), held; the body stretches as they close. On 2s."""
    for w in rig["wings"]:
        w.animation_data_clear()
    for sx, w in zip((-1, 1), rig["wings"]):
        anim.key(w, "rotation_euler", 1, (0, -sx * 1.25, 0))
        anim.key(w, "scale", 1, (1.45, 1.45, 1.45))
        anim.key(w, "rotation_euler", F_FOLD - 4, (0, -sx * 1.5, 0))         # flared: the last brake
        anim.key(w, "scale", F_FOLD - 4, (1.6, 1.6, 1.6))
        anim.key(w, "rotation_euler", F_FOLD, (0, -sx * 0.18, 0))            # SNAP shut
        anim.key(w, "scale", F_FOLD, (0.9, 0.9, 0.9))
        anim.key(w, "rotation_euler", n, (0, -sx * 0.14, 0))
    anim.squash(rig["body"], F_FOLD - 4, -0.08)
    anim.squash(rig["body"], F_FOLD, 0.3)                                     # stretched into a dart
    anim.squash(rig["body"], F_FOLD + 4, 0.24)
    anim.on_twos(rig["wings"] + [rig["body"]], step=2)


def _plunge(rig, n, perch):
    """Bend the last stretch of bGqrs's dive line into a drop: from where S01 leaves the bird (DIVE[0] down the line)
    it holds its height a moment while the wings snap shut, then falls steeply onto the shrimp's back (DIVE[1]),
    accelerating (a quadratic curve whose control point keeps the start height above the end point; keyed on 1s)."""
    from channels.monsters.diorama_ep02 import bgqrs as bq
    from channels.monsters.ep01v2 import xprl as x3
    lift = rig["lift"]
    for fc in list(anim.all_fcurves(lift.animation_data.action)):
        if fc.data_path == "location":
            while fc.keyframe_points:
                fc.keyframe_points.remove(fc.keyframe_points[0])
    S = __import__("channels.monsters.diorama_v3.xprl", fromlist=["x"]).BIRD_SCALE
    rot = rig["root"].rotation_euler.z
    to = bq.SHRIMP - Vector((perch.x, perch.y, 0.0))
    top = Vector((0.0, 0.0, perch.z / S))
    end = x3._local(rot, (to.x, to.y, 1.6), scale=S)
    p0, p1 = top.lerp(end, DIVE[0]), top.lerp(end, DIVE[1])
    ctl = Vector((p1.x, p1.y, p0.z + 0.2))                          # (QA: the drop starts sooner)
    for f in range(1, n + 3):
        u = min(1.0, (f - 1) / max(1, n - 1)) ** 1.15
        q = (1 - u) ** 2 * p0 + 2 * u * (1 - u) * ctl + u * u * p1
        anim.key(lift, "location", f, tuple(q), "LINEAR")


def s02():
    from channels.monsters.diorama_ep02 import bgqrs as bq
    from channels.monsters.diorama_ep02.xprl import _cam_move           # (XprL's gentler blur and farther haze)
    n = _frames("S02")
    isl = _world(n)
    sh = bq._shrimp(n)                                                  # drinking: it hasn't seen it
    shrimp = Vector(bq.SHRIMP)
    perch = Vector(isl["thorn"]["perch"])
    bird = bq._bird_dive(n, 1, n + 30, perch)
    bq._dive_line(bird, n, perch, DIVE)
    _plunge(bird, n, perch)
    bq._bird_shadow_look(bird)
    bq._shadow_under(bird, n, perch)
    _fold(bird, n)
    for e in sh["eyes"]:                                                # it only feels the shadow at the end
        anim.key(e, "scale", 37, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 39, (0.8, 1, 0.8), "CONSTANT")
    # side-on to the dive (from the south-east, the pond on the left): the bird comes down a big diagonal from the
    # top right onto the tiny shrimp at the water's edge; its shadow spreads over it. A slow push-in on 1s.
    line = Vector((shrimp.x - perch.x, shrimp.y - perch.y, 0)).normalized()
    yaw = math.degrees(math.atan2(-line.x, -line.y)) - 90.0
    lift = bird["lift"]
    bpy.context.scene.frame_set(n // 2)
    mid = lift.matrix_world.translation.copy()
    bpy.context.scene.frame_set(1)
    tgt = shrimp.lerp(mid, S02_CAM["toward"]) + Vector((0, 0, S02_CAM["lift"]))   # (QA: the shrimp big and clear)
    c = S02_CAM
    a = (tuple(tgt), c["dist"], c["tilt"], yaw, c["lens"], c["shift"])
    b = (tuple(tgt + Vector((0, 0, -0.1))), c["dist"] - c["push"], c["tilt"], yaw + 2.0, c["lens"], c["shift"])
    cam = _cam_move("cam_s02", n, a, b)
    from channels.monsters.diorama_v3.helper1 import _clear_view
    keep = {bird["root"], *bird["root"].children_recursive, sh["root"], *sh["root"].children_recursive}
    _clear_view(cam, [1, n], shrimp, keep, reach=0.9)
    _clear_smoke(cam, list(range(1, n + 1, 2)), tgt)
    _anchors("S02", cam, {"bird": lambda f: lift.matrix_world.translation.copy(),
                          "shrimp": lambda f: shrimp + Vector((0, 0, 0.8))}, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[bird["root"], sh["root"]])


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
    """The stumps' smoke puffs that would drift across the lens between Kai and `target` (the dollhouse cutaway): a
    whole puff is hidden if any of its spheres comes into frame nearer than the target (or behind the lens plane
    around the camera) at any of `frames`."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    puffs = [o for o in sc.objects if o.name.startswith("puff") and o.type == "EMPTY" and o.parent is None
             and not o.name.startswith("puff_root")]                 # (puff_root is the shrimp itself)
    hide = set()
    for f in frames:
        sc.frame_set(f)
        far = (target - cam.matrix_world.translation).length
        for o in puffs:
            if o in hide:
                continue
            for c in [o] + list(o.children_recursive):
                pts = [world_to_camera_view(sc, cam, c.matrix_world @ Vector(v)) for v in
                       (c.bound_box if c.type == "MESH" else [(0, 0, 0)])]
                near = [p for p in pts if p.z < far]
                if any(p.z <= 0 for p in pts) and near or any(-0.3 < p.x < 1.3 and -0.3 < p.y < 1.3 for p in near):
                    hide.add(o)
                    break
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
    _clear_smoke(cam, list(range(1, n + 1, 2)), crest)
    pts = {name: (lambda f, o=o: o.matrix_world.translation.copy() + Vector((0, 0, -1.0)))
           for name, o in bells.items()}
    _anchors("S16", cam, pts, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"]] + [v["root"] for v in vil])


# ------------------------------------------------------------------------------------------------------------ S04
F_RAKE = 13                 # the talons cross his forearm ("Its TALONS got my arm"): the 2D slash lands here


def _s04_pose(P, B, layout, f, look=0.0, flinch=0.0, rake=0.0, curl=0.0):
    """S03's last pose (bgqrs._s03_pose: on his knees, hunched over the cupped hands at his chest, facing SSW) plus:
    look (0-1) his head up and round over his left shoulder at the wings behind him; flinch (0-1) the jolt of the hit
    (shoulders up, head snapped away); rake (0-1) his left forearm knocked out by the talons; curl (0-1) folded
    tighter over the shrimp, his left shoulder turned to the bird (shielding it)."""
    d, k0, k1, start, slide0, slide1 = layout
    B._s03_pose(P, 999, slide0, slide1)
    P.rot("spine", (12 * curl - 4 * flinch, 0, 8 * curl))
    P.rot("chest", (10 * curl, 0, 6 * curl))
    P.rot("neck", (-14 * look + 10 * curl, 0, 18 * look))
    P.rot("head 1", (-16 * look + 3 * curl + 4 * flinch, 0, 22 * look - 18 * flinch + 6 * curl))
    for nm, sx in (("shoulder.L", 1), ("shoulder.R", -1)):
        P.rot(nm, (0, sx * (9 * flinch + 5 * curl), 0))                     # shoulders up round his ears
    if rake:
        P.aim("forearm.L", (0.25 + 0.45 * rake, -0.8, -0.2 - 0.3 * rake))    # knocked out and down
        P.aim("hand.L", (0.3 + 0.4 * rake, -0.7, -0.35 * rake))
    P.key(f)


def s04():
    from channels.monsters.diorama_ep02 import bgqrs as B
    from channels.monsters.diorama_ep02.xprl import _cam_move
    from channels.monsters.diorama_v3 import xprl as xv3
    from channels.monsters.diorama import helper1 as d1
    from channels.monsters.ep01v2 import bgqrs as s3d
    from channels.monsters.ep01v2 import helper5 as h5
    from channels.monsters.ep01v2 import xprl as x3
    from channels.monsters.mk import acting, hero
    n = _frames("S04")
    _world(n)
    layout = B._s03_layout()
    d, start = layout[0], layout[3]
    k = x3._hero(tuple(start), B._facing(d))                             # exactly as bgqrs.kai_s03_end builds him
    hero.line_width(k, 0.0028)
    d1._tilt_cap(k, 32.0)
    P = x3.Pose(k)
    beats = [(1, dict()), (5, dict(look=0.5)), (9, dict(look=1.0)),           # the wings behind him: a look
             (11, dict(look=0.6, flinch=0.3)),                                    # anticipation: a duck
             (F_RAKE, dict(flinch=1.0, rake=1.0)),                                # HIT: the arm knocked out
             (F_RAKE + 2, dict(flinch=0.9, rake=0.7, curl=0.3)),
             (F_RAKE + 6, dict(flinch=0.5, rake=0.1, curl=1.15)),                 # curls round it (past)
             (F_RAKE + 10, dict(flinch=0.3, curl=1.0)),                           # settle
             (F_RAKE + 24, dict(flinch=0.15, curl=0.95))]
    for f, kw in beats:
        _s04_pose(P, B, layout, f, **kw)
    for i, f in enumerate(range(F_RAKE + 28, n + 1, 4)):                        # a tremble on 2s
        _s04_pose(P, B, layout, f, flinch=0.1 + 0.06 * (i % 2), curl=0.95)
    B._cup_hands(k["arm"], 1, 1.0)
    anim.on_twos([k["arm"]], step=2)
    acting.EXPR.setdefault("wince", {"eye_V": 1.0, "mouth_wide": 0.7, "eye_brow_down": 0.4})
    acting.expression(k, "fear", 1, value=0.8)
    acting.expression(k, "surprised", 7, value=0.8)
    acting.expression(k, "wince", F_RAKE)
    acting.expression(k, "wince", F_RAKE + 20, value=0.85)
    acting.blink(k, 1, F_RAKE - 2, at=(4,))
    # the shrimp in his cupped hands (bgqrs: 0.6 scale, its root at the midpoint of his hand tails + 0.05 z), on 2s
    shr = B._shrimp(n)
    for f in range(1, n + 1, 2):
        bpy.context.scene.frame_set(f)
        hl = k["arm"].matrix_world @ k["arm"].pose.bones["hand.L"].tail
        hr = k["arm"].matrix_world @ k["arm"].pose.bones["hand.R"].tail
        anim.key(shr["root"], "location", f, tuple((hl + hr) / 2 + Vector((0, 0, 0.05))), "CONSTANT")
        anim.key(shr["root"], "rotation_euler", f, (0, 0, math.radians(B._facing(d))), "CONSTANT")
    # the bird: right on top of them at frame 1 (behind his left shoulder, where S02's dive was taking it); it
    # strikes past his left forearm talons first, then beats up and away over his left, climbing out of frame
    face = Vector((d.x, d.y, 0)).normalized()
    left = Vector((-face.y, face.x, 0))
    bpy.context.scene.frame_set(F_RAKE)
    pb = k["arm"].pose.bones["forearm.L"]
    elbow, wrist = k["arm"].matrix_world @ pb.head, k["arm"].matrix_world @ pb.tail
    bpy.context.scene.frame_set(1)
    hit = elbow.lerp(wrist, 0.55) + left * 0.7 + Vector((0, 0, 0.5))
    p0 = hit - face * 3.2 + left * 1.2 + Vector((0, 0, 4.6))
    p2 = hit + face * 2.0 + left * 9.0 + Vector((0, 0, 12.0))
    S = xv3.BIRD_SCALE
    rig = tuftwing.build((hit.x, hit.y, 0.0), shadow_span=10.0)
    rig["root"].scale = (S,) * 3
    c = Vector(tuftwing.CENTER)
    din = hit - p0
    rot = math.atan2(din.x, -din.y)
    rig["root"].rotation_euler.z = rot
    lift = rig["lift"]
    base = Vector((hit.x, hit.y, 0))
    for f in range(1, F_RAKE + 31):
        if f <= F_RAKE:
            p = p0.lerp(hit, ((f - 1) / (F_RAKE - 1)) ** 1.5)                     # dropping onto the arm
        else:
            e = 1 - (1 - min(1.0, (f - F_RAKE) / 24.0)) ** 2                      # bursting away, slowing
            p = hit.lerp(p2, e)
        anim.key(lift, "location", f, tuple(_local(rot, p - base, S) - c), "LINEAR")
    anim.key(lift, "location", F_RAKE + 40, tuple(_local(rot, p2 + face * 25 + Vector((0, 0, 10)) - base, S) - c),
             "LINEAR")
    for sx, w in zip((-1, 1), rig["wings"]):
        anim.key(w, "rotation_euler", 1, (0, -sx * 0.25, 0))                       # tucked, still diving
        anim.key(w, "rotation_euler", F_RAKE - 3, (0, -sx * 1.45, 0))              # flared to brake...
        anim.key(w, "scale", F_RAKE - 3, (1.6, 1.6, 1.6))
    anim.key(rig["body"], "rotation_euler", F_RAKE - 3, (-0.55, 0, 0))             # ...talons thrown forward
    anim.key(rig["body"], "rotation_euler", F_RAKE + 4, (0.3, 0, 0))
    tuftwing.flutter(rig, F_RAKE + 2, flaps=6, amount=1.4)                        # beating hard to climb away
    butcherbird.stare(rig, 1, down=0.45)
    h5._rage_light(rig, 1, B.SHRIMP.z + (tuftwing.CENTER[2] - 0.1) * S)          # all dark, as in S01-S02
    xv3.dark_form(1)
    B._bird_shadow_look(rig)
    sh = rig["shadow"]                                                            # its shadow sweeps over him
    z = sh.location.z
    for f in range(1, n + 1, 2):
        bpy.context.scene.frame_set(f)
        lx, ly, _ = lift.location
        anim.key(sh, "location", f, (lx, ly, z), "CONSTANT")
    bpy.context.scene.frame_set(1)
    anim.on_twos([o for o in tuftwing._animated(rig) if o is not lift], step=2)  # the swoop path stays on 1s
    # low in front of him and a little to his left: his face under the cap, the cupped hands, the left forearm;
    # the bird drops in from the top behind his shoulder. A slow push-in on 1s.
    hips = start + face * (layout[5] * B.KAI_SCALE)
    chest = hips + Vector((0, 0, 3.6))
    cdir = (face + left * 0.5).normalized()
    yaw = math.degrees(math.atan2(-cdir.x, -cdir.y))
    a = (tuple(chest + Vector((0, 0, 1.2))), 12.5, 7.0, yaw, 35.0, -0.14)
    b = (tuple(chest + Vector((0, 0, 1.0))), 10.5, 7.0, yaw - 2.0, 35.0, -0.14)
    cam = _cam_move("cam_s04", n, a, b)
    _clear_smoke(cam, list(range(1, n + 1, 2)), chest)

    def bone(name, tail=False):
        def fn(f):
            pbn = k["arm"].pose.bones[name]
            return k["arm"].matrix_world @ (pbn.tail if tail else pbn.head)
        return fn
    pts = {"elbow": bone("forearm.L"), "wrist": bone("forearm.L", True),
           "bird": lambda f: lift.matrix_world.translation.copy(),
           "eye_l": lambda f: s3d.kai_point(k, "eye_l"), "eye_r": lambda f: s3d.kai_point(k, "eye_r")}
    _anchors("S04", cam, pts, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], rig["root"], shr["root"]])

SHOTS = {"S02": s02, "S04": s04, "S16": s16}
