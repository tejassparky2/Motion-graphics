"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), helper 6: the fluffmoth shots.

    S06 "That's when the fluffmoths came down the hill."  Night. Low by Kai's spot, looking south up the dark rise
        (helper 1's Ep 2 hill): a cloud of fluffmoths pours over the crest and down the slope toward us, near ones big,
        far ones small, all heading for the only light (Kai's mark, behind the camera; its coral catches their fronts
        as they come). Cut (on "hill") to close on one: hovering in front of us, its wing eye-spots shut, then they
        blink OPEN and glow (the creepy tell), the swarm streaming past behind it.
    S10 "They were circling my wrist. Round and round."  Top view: Kai below, his left wrist raised, the mark the
        light at the centre; a spiral of moths circling it (inner rings faster), each leaning its BACK (the body top)
        in toward the light: the physics payoff's first beat. The shrimp on his left shoulder ducks when a moth
        swings past.

Moths: mk/fluffmoth.py (swarm, flight_mode, back_to, flap). Until helper 9's night grade lands, a stand-in night
(_night): navy world, a cool moon, the mark as a coral point light.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S06 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as v2
from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.mk import acting, anim, diorama, look
from channels.monsters.mk import fluffmoth as fm

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
FPS = 24
CORAL = "#ff8466"
MOTH_K = 0.42                      # a moth's size next to Kai (~a head across, wings spread)
MARK_U = 0.3                       # helper 9's mark spot on the forearm (elbow -> wrist)
S10_K = 0.5                        # S10's moths, a little bigger (close to the camera)
S10_TILT = 0.5                     # how far each back leans in to the light (0 level .. 1 square to it)
S10_MARK_W = 9000.0                # the mark light in S10 (helper 9's night default 6000): his wrist is high over
                                   # his head here, and its light has to reach the ring and the grass round him
HERO_GLOW = 3.6                    # S06's close moth: its open eye-spots light up this bright (the material's 1.8)


# ------------------------------------------------------------------------------------------------------- shared
def _frames(shot, fallback):
    try:
        with open(TIMING) as f:
            return {s["shot"]: s["render_frames"] for s in json.load(f)["shots"]}[shot]
    except (OSError, KeyError, ValueError):
        return fallback


def _words(line_id, fallback):
    """[(word, f_in, f_out)] of a line in its shot's frames (frame 1 = the shot's start), from timing.json; the
    fallback until it lands."""
    try:
        with open(TIMING) as f:
            T = json.load(f)
        ln = next(x for x in T["lines"] if x.get("id") == line_id)
        t0 = next(s["start"] for s in T["shots"] if s["shot"] == ln["scene"])
        return [(w["w"].strip(".,!?").lower(), round((w["start"] - t0) * FPS) + 1, round((w["end"] - t0) * FPS) + 1)
                for w in ln["words"]]
    except (OSError, KeyError, ValueError, StopIteration):
        return fallback


def _at(W, word, default):
    for w, a, _ in W:
        if w == word:
            return a
    return default


def _night():
    """Stand-in night until helper 9's grade lands: diorama.setup()'s day turned into a navy night with a cool moon
    from the south-east; returns the moon."""
    hx = look.hexc
    sc = bpy.context.scene
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    bg.inputs[0].default_value = hx("#22305a")
    bg.inputs[1].default_value = 0.55
    for n in nt.nodes:
        if n.type == "VALTORGB":
            n.color_ramp.elements[0].color = hx("#0d1426")
            n.color_ramp.elements[1].color = hx("#1c2950")
    moon = None
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy, o.data.color = 0.7, hx("#a9bcff")[:3]
            o.rotation_euler = (math.radians(55), 0, math.radians(150))
            moon = o
    if sc.node_tree:
        nt = sc.node_tree
        for n in nt.nodes:
            if n.type == "MIX_RGB":
                n.inputs[2].default_value = hx("#16203a")
        comp = next((n for n in nt.nodes if n.type == "COMPOSITE"), None)
        if comp is not None and comp.inputs[0].links:                   # a navy night multiply over everything
            src = comp.inputs[0].links[0].from_socket
            mul = nt.nodes.new("CompositorNodeMixRGB")
            mul.blend_type = "MULTIPLY"
            mul.inputs[0].default_value = 1.0
            mul.inputs[2].default_value = hx("#5b6aa6")
            nt.links.new(src, mul.inputs[1])
            nt.links.new(mul.outputs[0], comp.inputs[0])
    return moon


def _night_look():
    """helper 9's night grade if it has landed (diorama_ep03/helper9.night()), else the stand-in."""
    try:
        from channels.monsters.diorama_ep03 import helper9 as H9
        if hasattr(H9, "night"):
            return H9.night()
    except ImportError:
        pass
    return _night()


def _mark_light(at, energy=6000.0, name="h6_mark_light"):
    """Kai's mark as a coral point light at a world point, for shots without his rig (S06: he is behind the camera):
    helper 9's mark light settings (mk/night.mark_light: its CORAL, no shadows, soft falloff), so the night grade
    brings its light back warm."""
    try:
        from channels.monsters.mk import night as NG
        col = NG.CORAL
    except ImportError:
        col = look.hexc(CORAL)[:3]
    ld = bpy.data.lights.new(name, "POINT")
    ld.color, ld.energy, ld.shadow_soft_size = col, energy, 0.25
    if hasattr(ld, "use_soft_falloff"):
        ld.use_soft_falloff = True
    ld.use_shadow = False                      # (a point light's shadow cube over a whole swarm costs minutes a frame)
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.location = at
    return o


def _glow(at, r=0.34, name="h6_mark_glow"):
    """A small coral-white core at the mark (it blooms in the compositor): the light the moths circle, readable."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r, location=at)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(look.flat(name, look.hexc("#ffd9c9"), 6.0))
    return o


def _cam_cut(name, n, f_cut, A, B):
    """One camera on 1s: move A (pose a0 -> a1) up to f_cut - 1, then a cut to move B (b0 -> b1). Poses are diorama
    camera poses (target, dist, tilt, yaw, lens, shift_y)."""
    cam = None
    for f in range(1, n + 1):
        (a, b), f0, f1 = (A, 1, f_cut - 1) if f < f_cut else (B, f_cut, n)
        k = v2._smooth((f - f0) / max(1, f1 - f0))
        t = tuple(a[0][i] + (b[0][i] - a[0][i]) * k for i in range(3))
        d, tl, yw, ln, sy = (a[i] + (b[i] - a[i]) * k for i in range(1, 6))
        cam = v2._cam(name, f, t, d, tl, yw, ln, (0.0, sy), cam)
    for c in anim.all_fcurves(cam.animation_data.action):
        for kp in c.keyframe_points:
            kp.interpolation = "LINEAR"
    bpy.context.scene.camera = cam
    return cam


def _haze(n, start, depth):
    ms = bpy.context.scene.world.mist_settings
    for f in range(1, n + 1):
        ms.start, ms.depth = start, depth
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)


# --------------------------------------------------------------------------------------------------------- S06
S06_NEAR = Vector((-3.2, -14.5, 2.3))      # the close one: west of Wren's path, clear of the grove's stumps (x > 4)


def _hill():
    from channels.monsters.diorama_ep02 import helper1 as h1
    h1.hill()
    return h1


def _pour(rigs, n, h1, seed=21):
    """The swarm pouring over the crest and down the slope toward the light (north): each moth on its own lane, a
    little wobble, hugging the ground (a few units over the grass), faster as they come down; banking a touch."""
    rnd = random.Random(seed)
    c = Vector((*h1.HILL["center"], 0.0))
    goal = Vector((X.KAI_AT.x, X.KAI_AT.y + 2.0, 0.0))
    for i, r in enumerate(rigs):
        lane = rnd.uniform(-9.0, 9.0)
        y0 = c.y - h1.HILL["ry"] - rnd.uniform(2.0, 16.0)             # behind the crest
        x0 = c.x + lane
        start = Vector((x0, y0, 0.0))
        end = goal + Vector((lane * 0.35 + rnd.uniform(-3, 3), rnd.uniform(-4, 6), 0.0))
        lift = rnd.uniform(2.0, 6.0)
        t0 = rnd.uniform(-0.15, 0.45)                                   # a stream: many already over the crest
        dur = rnd.uniform(2.2, 3.0) * FPS
        ph, sp = rnd.uniform(0, 6.3), rnd.uniform(0.15, 0.3)
        prev = None
        last = None
        for f in range(1, n + 1, 2):
            u = t0 + (f - 1) / dur
            uu = max(0.0, min(1.25, u))
            ease = uu * uu * (0.6 + 0.4 * uu)                           # gathering speed down the slope
            p = start.lerp(end, min(ease, 1.2))
            p.x += 1.2 * math.sin(f * sp + ph)
            p.z = h1.hill_height(p.x, p.y) + lift + 0.8 * math.sin(f * sp * 1.3 + ph)
            r["root"].location = p
            r["root"].keyframe_insert("location", frame=f)
            if last is not None:
                head = p - last
                head.z *= 0.3
                prev = fm.face(r, f, head if head.length > 1e-3 else Vector((0, 1, 0)),
                               bank=0.15 * math.sin(f * sp + ph), prev=prev)
            last = p.copy()
        if prev is None:
            fm.face(r, 1, (0, 1, 0))


def s06():
    n = _frames("S06", 96)
    W = _words("l6", [("that's", 4, 10), ("when", 10, 15), ("the", 15, 18), ("fluffmoths", 18, 34),
                      ("came", 34, 40), ("down", 40, 46), ("the", 46, 49), ("hill", 49, 62)])
    f_cut = _at(W, "down", int(n * 0.55))                               # cut to the close one on "down"
    f_open = f_cut + 5                                                  # its eye-spots blink open on "the hill"
    X._world(n)
    h1 = _hill()
    _night_look()
    _mark_light(X.KAI_AT + Vector((0.0, 1.5, 6.8)))                   # Kai's raised wrist, behind the camera
    c = Vector((*h1.HILL["center"], 0.0))
    crest = Vector((diorama._path_x(c.y), c.y, h1.HILL["h"]))

    def place(i, rnd):
        return Vector((0, 0, -50)), MOTH_K * rnd.uniform(0.8, 1.15)
    rigs = fm.swarm(int(os.environ.get("S06_MOTHS", "56")), place, name="s06sw",
                    far=lambda i, loc, s: i % 3 != 0)                   # 1 in 3 keeps every detail
    _pour(rigs, n, h1)
    # the close one: in front of the lens from the cut, facing us (the light is behind us), spots shut then open
    hero = fm.build((0, 0, 0), name="s06hero")
    fm.flight_mode(hero)
    hero["root"].scale = (MOTH_K,) * 3
    near = S06_NEAR
    for f in range(1, n + 1, 2):
        p = near + Vector((0.12 * math.sin(f * 0.21), 0.0, 0.16 * math.sin(f * 0.27)))
        if f < f_cut:
            p = p + Vector((0, -60, 0))                                 # out of shot until the cut
        anim.key(hero["root"], "location", f, tuple(p), "CONSTANT")
    fm.face(hero, 1, (0, 1, 0))                                          # faces north: toward the camera and light
    fm.flap(hero, amp=0.7)
    fm.spot_lid(hero, 1, 1.0, interp="CONSTANT")
    fm.spot_lid(hero, 1, 0.0, prop="glow", interp="CONSTANT")
    for s, d in zip(hero["spots"], (0, 2, 1, 3)):                        # they blink OPEN, out of step, and glow
        fm.spot_lid(hero, f_open + d, 1.0, [s])
        fm.spot_lid(hero, f_open + d + 5, 0.0, [s])
        fm.spot_lid(hero, f_open + d - 1, 0.0, [s], prop="glow")
        fm.spot_lid(hero, f_open + d + 6, 1.0, [s], prop="glow")
    anim.on_twos(hero["spots"] + hero["eyes"], 2)
    for m in {s_.data.materials[0] for s_ in hero["spots"]}:            # the creepy beat: a brighter iris glow
        for nd in m.node_tree.nodes:
            if nd.type == "MIX" and nd.blend_type == "MULTIPLY" and tuple(nd.inputs[7].default_value)[:3] == (1.8, 1.8, 1.8):
                nd.inputs[7].default_value = (HERO_GLOW, HERO_GLOW, HERO_GLOW, 1)
    anim.blink(hero, min(n - 4, f_open + 24))
    # camera: A low by Kai's spot looking up the rise at the crest (a slow push-in); B close on the hero moth
    tA = crest + Vector((0.0, 6.0, -2.5))
    A = ((tuple(tA), 30.0, 6.0, 180.0 - 4.0, 30.0, 0.12), (tuple(tA), 25.0, 6.0, 180.0 - 2.0, 30.0, 0.12))
    tB = near - Vector((0, 0, 0.95))                                    # aimed below it: the moth sits high, clear of
                                                                        # the caption band (845-930)
    B = ((tuple(tB), 5.2, 4.0, 180.0, 50.0, 0.05), (tuple(tB), 4.4, 4.0, 180.0, 50.0, 0.05))
    cam = _cam_cut("S06cam", n, f_cut, A, B)
    fc = next(c for c in anim.all_fcurves(cam.data.animation_data.action) if c.data_path == "dof.aperture_fstop")
    for kp in fc.keyframe_points:                                       # less blur: the swarm behind still reads
        kp.co.y *= 2.0
    _haze(n, 40.0, 70.0)
    return dict(frames=n, step=2, ones=(1, n), subject=[hero["root"]])


# --------------------------------------------------------------------------------------------------------- S10
def s10():
    from channels.monsters.diorama_ep02 import helper4 as E2
    from channels.monsters.diorama_ep02 import helper9 as H9e2
    from channels.monsters.diorama_ep03 import helper3 as h3
    from channels.monsters.diorama_ep03 import helper4 as h4
    from channels.monsters.ep01v2 import xprl as x3
    n = _frames("S10", 84)
    X._world(n)
    _night_look()
    k = X._kai()
    d = (X.WREN_STOP - X.KAI_AT).normalized()
    fwd = Vector((d.x, d.y, 0)).normalized()
    up = Vector((0, 0, 1))
    PK = x3.Pose(k)
    PK.reset()
    h4._raised_arm(PK, k, fwd, up, u=1.0)                              # (the right hand down at his side)
    bpy.context.view_layer.update()
    side = X._side_vec(k)                                               # then the left wrist straight up over his
    sh_w = E2._bone_world(k, "upper_arm.L")                             # head: the axis the spiral turns on
    X._reach(PK, k, "L", sh_w + up * 3.4 + fwd * 0.5 - side * 0.35, bend=(0, 0, 0.0))
    PK.twist("forearm.L", -80.0)
    PK.key(1)
    bpy.context.view_layer.update()
    mark = H9e2._forearm(k, MARK_U)
    try:
        from channels.monsters.diorama_ep03 import helper9 as N9
        N9.mark(k, energy=S10_MARK_W)                                  # helper 9's mark light, on his forearm bone
    except (ImportError, AttributeError):
        _mark_light(mark + Vector((0, 0, 0.3)), energy=S10_MARK_W)
    _glow(mark)
    sh = h3._shoulder_shrimp(k, n, name="ep03_shrimp_s10")
    # the spiral: rings round the wrist, a little below it so every back leans up and in to the light
    rnd = random.Random(31)

    def place(i, rnd_):
        return Vector((0, 0, -50)), S10_K * rnd_.uniform(0.85, 1.1)
    N = int(os.environ.get("S10_MOTHS", "42"))
    rigs = fm.swarm(N, place, name="s10sw", far=lambda i, loc, s: i % 2 == 1)
    close = []                                                          # (frame) a moth swings past the shrimp
    shoulder = E2._bone_world(k, "upper_arm.L")
    for i, r in enumerate(rigs):
        ring = i % 4
        rad = 3.4 + ring * 1.2 + rnd.uniform(-0.3, 0.3)
        z = mark.z - 1.6 - ring * 0.45 + rnd.uniform(-0.3, 0.3)
        w = (1.25 / rad) * 2.2 * (1 if ring % 2 == 0 else 1)          # all one way round; inner rings faster
        th0 = rnd.uniform(0, 2 * math.pi)
        drift = rnd.uniform(-0.15, 0.15)
        prev = None
        for f in range(1, n + 1, 2):
            th = th0 + w * (f - 1) / FPS
            rr = rad * (1.0 + drift * math.sin(f * 0.05 + i))
            p = Vector((mark.x + rr * math.cos(th), mark.y + rr * math.sin(th), z + 0.25 * math.sin(f * 0.17 + i)))
            r["root"].location = p
            r["root"].keyframe_insert("location", frame=f)
            head = Vector((-math.sin(th), math.cos(th), 0.0))
            prev = fm.back_to(r, f, mark, head, amount=S10_TILT, prev=prev)
            if (p - shoulder).length < 2.2:
                close.append(f)
    # the shrimp ducks (squashes down into its collar) whenever a moth swings close, on 2s
    ducks = sorted(set(f - f % 8 for f in close))
    for f in ducks:
        anim.squash(sh["body"], max(1, f - 2), 0.0, "CONSTANT")
        anim.squash(sh["body"], f, -0.22, "CONSTANT")
        anim.squash(sh["body"], f + 6, -0.22, "CONSTANT")
        anim.squash(sh["body"], f + 10, 0.0, "CONSTANT")
    acting.blink(k, 1, n, seed=4)
    # the top view: high over his left shoulder (behind him: he faces Wren), the wrist and its ring in the middle, a
    # slow push-in and a small turn
    yaw = math.degrees(math.atan2(-fwd.x, -fwd.y)) + 180.0 - 20.0
    t = (mark.x, mark.y, mark.z - 1.5)
    v2._move("S10cam", 1, n, (t, 26.0, 68.0, yaw, 45.0, 0.0), (t, 22.0, 70.0, yaw + 8.0, 45.0, 0.0), n)
    _haze(n, 60.0, 80.0)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


SHOTS = {"S06": s06, "S10": s10}
