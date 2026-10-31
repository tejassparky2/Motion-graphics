"""Acting library for Episode 1 v3 (DIORAMA_EP01_V3.md, quality pass Q1): small, reusable performance pieces so every
shot gets clear key poses, anticipation and overshoot on 2s, blinking and living eyes, and faces that match the line.

Kai (the hero rig from hero.load; face keys on the "head" mesh):
    lie(rig, hips, head_dir)                 LYING_V3: on his back, a knee bent, an arm flung over his head, grass
                                             tufts and a contact shadow (from above he never reads as standing);
                                             LYING_V3_L is its mirror (the left arm flung), mirror(spec) any other
    expression(rig, name, f0, f1=None)       surprised / fear / angry / joy / neutral / terror / deadpan / dazed /
                                             thinking / realise / realised (snaps on)
    face_keys(rig, f, **keys)                single face keys, layered
    lips(rig, f0, f1)                        whispered lips on 3s, layered
    blink(rig, f0, f1)                       a blink every 2-4 s, layered over any expression
    look_at(rig, target, f0, f1)             eyes on a world point, with small darts
Easing and moves:
    ease(u, kind)                            "inout", "out", "in", "anticipate", "overshoot", "back"
    move(obj, path, f0, f1, a, b)            anticipation before, overshoot after, keyed on 2s
The puff-shrimp (puffshrimp.build rig):
    glare(sh, target, f)                     eyes locked on, lids dropped and slanted (the narrowed glare)
    hop(sh, f, height)                       a startled hop: crouch, jump, stretch, land, settle
    strut(sh, path, f0, f1)                  a smug strut: bouncing steps, chest up, a sway, on 2s
The bird (tuftwing / butcherbird rig):
    tilt(rig, f, angle)                      a curious head tilt with overshoot
    lock_on(rig, target, f)                  head turns to the prey, eyes narrow, crest up

Faces snap between drawings (CONSTANT keys). Call expression()/kai_face() first in a shot, then blink() and look_at():
those read the face already keyed and layer on top of it.
"""
import math
import random

import bpy
from mathutils import Vector

from . import anim, look

# ---------------------------------------------------------------- easing

def ease(u, kind="inout", amount=0.12):
    """0..1 -> 0..1 (overshooting curves leave the range). "anticipate" dips back by `amount` first; "overshoot"
    goes past by `amount` and settles; "back" does both (the anime move: wind up, go, overshoot, settle)."""
    u = max(0.0, min(1.0, u))
    if kind == "in":
        return u * u
    if kind == "out":
        return 1 - (1 - u) ** 2
    if kind == "anticipate":
        return u * u * ((1 + amount * 10) * u - amount * 10)
    if kind == "overshoot":
        v = u - 1
        return 1 + v * v * ((1 + amount * 10) * v + amount * 10)
    if kind == "back":
        return 0.5 * ease(u * 2, "anticipate", amount) if u < 0.5 else 0.5 + 0.5 * ease(u * 2 - 1, "overshoot", amount)
    return u * u * (3 - 2 * u)


def move(obj, path, f0, f1, a, b, kind="back", amount=0.12, step=2):
    """Key obj.<path> from a to b over f0..f1 on `step`s along ease(kind): anticipation before the move and an
    overshoot that settles after it (CONSTANT keys: the drawing holds between steps)."""
    a, b = Vector(a), Vector(b)
    f = f0
    while True:
        u = (f - f0) / max(1, f1 - f0)
        anim.key(obj, path, f, tuple(a + (b - a) * ease(u, kind, amount)), "CONSTANT")
        if f >= f1:
            break
        f = min(f + step, f1)


# ---------------------------------------------------------------- Kai's face

EXPR = {                                      # the line's face, from hero.blend's shape keys
    "neutral": {},
    "surprised": {"face_surprise": 1.0, "eye_brow_up": 0.6},
    "fear": {"eye_black_small": 1.0, "eye_brow_up": 1.0, "mouth_wide": 0.35},
    "terror": {"eye_open": 1.0, "eye_small": 1.0, "eye_no_hilight": 1.0, "eye_brow_up": 1.0},   # the S01 pin-pricks
    "angry": {"face_angry": 1.0, "eye_brow_down": 0.6},
    "joy": {"face_happy": 1.0},
    "deadpan": {"eye_zitome": 0.7},
    "dazed": {"eye_zitome": 0.4, "eye_brow_up": 0.3, "mouse_open": 0.2},
    "thinking": {"eye_open": 0.4, "eye_brow_up": 0.4},
    "realise": {"eye_zitome": 0.5, "eye_brow_down": 0.3},
    "realised": {"eye_zitome": 0.85, "eye_brow_down": 0.6},
}
_LIPS = ("lip_a", "lip_o", "lip_u", "mouth_short")
_LAYERED = ("eye_close", "look_up", "look_down", "look_left", "look_right")   # blink() and look_at() own these


def _kb():
    return bpy.data.objects["head"].data.shape_keys.key_blocks


def _value_at(name, f):
    """The value a face key holds at frame f (its F-curve), or its current value if it isn't animated."""
    sk = bpy.data.objects["head"].data.shape_keys
    ad = sk.animation_data
    if ad and ad.action:
        for fc in anim.all_fcurves(ad.action):
            if fc.data_path == f'key_blocks["{name}"].value':
                return fc.evaluate(f)
    return _kb()[name].value if name in _kb() else 0.0


def _key(name, f, v):
    kb = _kb()
    if name not in kb:
        return
    kb[name].value = v
    kb[name].keyframe_insert("value", frame=f)
    ad = bpy.data.objects["head"].data.shape_keys.animation_data
    for fc in anim.all_fcurves(ad.action):
        if fc.data_path == f'key_blocks["{name}"].value':
            for kp in fc.keyframe_points:
                if abs(kp.co.x - f) < 0.01:
                    kp.interpolation = "CONSTANT"


def expression(rig, name, f0, f1=None, value=1.0):
    """Snap Kai's face to EXPR[name] at f0 (and back to neutral at f1): sets every expression key, leaving the eye
    keys that blink()/look_at() own."""
    if rig.get("standin"):
        return
    keys = {k for e in EXPR.values() for k in e}
    for k in keys:
        _key(k, f0, EXPR[name].get(k, 0.0) * value)
    if f1 is not None:
        for k in keys:
            _key(k, f1, 0.0)


def face_keys(rig, f, **keys):
    """Key just these face keys at frame f (CONSTANT), leaving every other key as it is (layered, unlike
    kai_face/hero.face which reset the whole face)."""
    if rig.get("standin"):
        return
    for k, v in keys.items():
        _key(k, f, v)


def lips(rig, f0, f1, seed=3, amount=0.45):
    """Whispered lips on 3s from f0 to f1 (small a/o/u shapes and closed beats), keying only the lip keys, so the
    expression, blinks and looks underneath stay."""
    if rig.get("standin"):
        return
    rnd = random.Random(seed)
    f = f0
    while f < f1:
        lip = rnd.choice(("lip_a", "lip_o", "lip_u", None))
        for k in _LIPS:
            _key(k, f, (amount if k == lip else 0.0) if lip else (1.0 if k == "mouth_short" else 0.0))
        f += 3
    for k in _LIPS:
        _key(k, f1, 1.0 if k == "mouth_short" else 0.0)


def blink(rig, f0, f1, every=(48, 96), seed=1, at=()):
    """Blinks from f0 to f1, one every 2-4 s (random in `every` frames) plus any frames in `at`: shut for 2 frames
    on top of whatever face is keyed (an open-eye key is lifted for the blink and put back)."""
    if rig.get("standin"):
        return
    rnd = random.Random(seed)
    frames = sorted(set(list(at) + _blink_frames(f0, f1, every, rnd)))
    for f in frames:
        before = {k: _value_at(k, f - 1) for k in ("eye_close", "eye_open")}
        was = {k: _value_at(k, f + 2) for k in ("eye_close", "eye_open")}
        if was["eye_close"] > 0.5:                                  # already shut there
            continue
        for k, v in before.items():                                 # hold the face up to the blink (a first key
            _key(k, f - 1, v)                                       # would otherwise extend back to frame 1)
        _key("eye_close", f, 1.0)
        _key("eye_open", f, 0.0)
        _key("eye_close", f + 2, was["eye_close"])
        _key("eye_open", f + 2, was["eye_open"])


def _blink_frames(f0, f1, every, rnd):
    out, f = [], f0 + rnd.randint(8, every[0])
    while f < f1 - 3:
        out.append(f)
        f += rnd.randint(*every)
    return out


def look_at(rig, target, f0, f1=None, darts=True, seed=2, strength=0.8):
    """Turn Kai's eyes (the look_* keys) toward a world point from f0, with small darts every 8-14 frames until f1
    (the eyes stay alive). Uses the head bone's frame: up the neck, forward out of the face, side to his left."""
    if rig.get("standin"):
        return
    rnd = random.Random(seed)
    f, end = f0, (f0 if f1 is None else f1)
    while True:
        bpy.context.scene.frame_set(f)
        m = rig["arm"].matrix_world @ rig["bone"]("head").matrix
        up = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
        fwd = (m.to_3x3() @ Vector((0, 0, 1))).normalized()
        side = up.cross(fwd).normalized()                          # toward his left eye
        d = (Vector(target) - m.translation).normalized()
        x, y = d.dot(side), d.dot(up)
        if darts and f > f0:
            x += rnd.uniform(-0.12, 0.12)
            y += rnd.uniform(-0.08, 0.08)
        _key("look_left", f, max(0.0, x) * strength * 1.6)
        _key("look_right", f, max(0.0, -x) * strength * 1.6)
        _key("look_up", f, max(0.0, y) * strength * 1.6)
        _key("look_down", f, max(0.0, -y) * strength * 1.6)
        if not darts or f >= end:
            break
        f = min(end, f + rnd.randint(8, 14))
    bpy.context.scene.frame_set(1)


# ---------------------------------------------------------------- Kai lying down (LYING_V3)

# On his back, so that from above he can never read as standing: the right arm flung up over his head, the left loose
# by his hip, the left knee up (the foot planted by his other knee), the right leg out, the head rolled to one side.
# Directions in Kai's own frame (helper 10's _pose spec): +X his right, +Y forward (up once he lies down), +Z toward
# his head. Parents first.
LYING_V3 = [("spine", (0, 0, 1)), ("chest", (0, 0.05, 1)), ("upper_chest", (0, 0.05, 1)), ("neck", (-0.1, 0.1, 1)),
            ("head", (-0.35, 0.25, 1)),
            ("right_upper_arm", (0.8, 0.15, 0.65)), ("right_lower_arm", (-0.85, 0.25, 0.5)),  # flung over his head
            ("left_upper_arm", (-0.45, 0.1, -1)), ("left_lower_arm", (-0.3, 0.3, -1)),      # loose by his hip
            ("left_upper_leg", (-0.12, 0.85, -0.55)), ("left_lower_leg", (-0.05, -0.75, -0.7)),   # knee up
            ("right_upper_leg", (0.2, 0.2, -1)), ("right_lower_leg", (0.12, -0.05, -1)),
            ("left_foot", (-0.1, 0.4, -1)), ("right_foot", (0.35, 1, -0.3))]


def mirror(spec):
    """The same pose mirrored left to right (swap the left_/right_ bones, flip X)."""
    swap = {"left_": "right_", "right_": "left_"}
    out = []
    for b, (x, y, z) in spec:
        for a, c in swap.items():
            if b.startswith(a):
                b = c + b[len(a):]
                break
        out.append((b, (-x, y, z)))
    return out


LYING_V3_L = mirror(LYING_V3)     # the LEFT arm flung over his head (east side, clear of v3's sapling to his west)


def lie(rig, hips, head_dir, spec=LYING_V3, tufts=True, shadow=True, head=None):
    """Lay Kai on his back with his hips at `hips` (x, y), his head pointing at compass `head_dir` degrees (0 = +Y,
    positive toward -X), in `spec` (LYING_V3); `head` replaces the head direction. Grounds him on the grass and adds
    a soft contact shadow and grass tufts over his outline. Returns the hips' world position."""
    from channels.monsters.ep01v2 import helper10 as s15
    if head is not None:
        spec = [(b, head if b == "head" else d) for b, d in spec]
    rot = (math.pi / 2, 0, math.pi + math.radians(head_dir))
    s15._pose(rig, spec, (hips[0], hips[1], 0.5), rot)
    hip = s15._world(rig, "hips")
    rig["arm"].location += Vector((hips[0] - hip.x, hips[1] - hip.y, 0))
    s15._ground(rig)
    bpy.context.view_layer.update()
    hip = s15._world(rig, "hips")
    up = Vector((-math.sin(math.radians(head_dir)), math.cos(math.radians(head_dir)), 0))
    if shadow:
        sh = look.blob_shadow("kai_down_shadow", (hip.x, hip.y, 0.03), (2.2, 5.4))
        sh.rotation_euler = (0, 0, math.radians(head_dir))
    if tufts:
        grass_round(hip, up)
    return hip


def grass_round(hip, up, seed=21):
    """Grass tufts and a few flowers along a lying body's outline, overlapping it a little (lit paint)."""
    from . import diorama
    rnd = random.Random(seed)
    side = Vector((up.y, -up.x, 0))
    blade = diorama.lit_paint("act_tuft", "#2f8a36", "#4cb348", "#8fdb62")
    petals = [diorama.lit_paint(f"act_flower{i}", *c) for i, c in enumerate((("#c9c9e0", "#ffffff", "#ffffff"),
                                                                             ("#d9a400", "#ffd23f", "#fff2a8")))]
    for along, s in ((3.6, 1.15), (2.2, -1.35), (0.6, 1.5), (-0.8, -1.25), (-2.4, 0.95), (-3.6, -0.8),
                     (-4.2, 0.7), (1.4, 1.6), (3.0, -1.0), (-1.6, 1.3), (4.6, 0.4), (-4.8, -0.3)):
        c = Vector(hip) + up * along + side * s * rnd.uniform(0.9, 1.1)
        for _ in range(rnd.randint(4, 6)):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.09, radius2=0.0, depth=rnd.uniform(0.7, 1.1),
                                            location=(c.x + rnd.uniform(-0.25, 0.25), c.y + rnd.uniform(-0.25, 0.25),
                                                      0.4))
            o = bpy.context.object
            o.name = "act_tuft"
            o.rotation_euler = (rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), rnd.uniform(0, 3))
            o.data.materials.append(blade)
        if rnd.random() < 0.5:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=0.16, location=(c.x, c.y, 0.75))
            bpy.context.object.name = "act_flower"
            bpy.context.object.data.materials.append(rnd.choice(petals))


# ---------------------------------------------------------------- the puff-shrimp

def glare(sh, target, f, lids=0.42, slant=0.36):
    """The narrowed glare: eyes locked on `target`, lids dropped and slanted in (determined, still cute)."""
    from channels.monsters.ep01v2 import bgqrs as s3d
    s3d.lock_on(sh, target, f, lids=lids, slant=slant)


def hop(sh, f, height=0.6, frames=10):
    """A startled hop around frame f: a crouch (anticipation), the jump (stretched), the landing squash and a
    settle (overshoot), on 2s."""
    root, body = sh["root"], sh["body"]
    z0 = root.location.z
    for df, dz, sq in ((-4, 0.0, -0.18), (-2, 0.0, -0.22), (0, height * 0.6, 0.25), (2, height, 0.12),
                       (4, height * 0.7, 0.05), (6, 0.0, -0.2), (8, 0.0, 0.06), (10, 0.0, 0.0)):
        if df > frames:
            break
        anim.key(root, "location", f + df, (root.location.x, root.location.y, z0 + dz), "CONSTANT")
        anim.squash(body, f + df, sq, "CONSTANT")


def strut(sh, path, f0, f1, step_frames=6, bounce=0.18, sway=0.12):
    """A smug strut along `path` (world points) from f0 to f1: one bouncing step every `step_frames` (up on the
    stride, a squash on each footfall), chest up (leaning back), a side-to-side sway, facing where it goes. On 2s."""
    root, body = sh["root"], sh["body"]
    pts = [Vector(p) for p in path]
    segs = [(a, b, (b - a).length) for a, b in zip(pts, pts[1:])]
    total = sum(s[2] for s in segs) or 1.0

    def at(u):
        d = u * total
        for a, b, ln in segs:
            if d <= ln or (a, b, ln) == segs[-1]:
                return a.lerp(b, min(1.0, d / ln if ln else 0)), (b - a)
            d -= ln

    for f in range(f0, f1 + 1, 2):
        u = (f - f0) / max(1, f1 - f0)
        p, d = at(u)
        ph = ((f - f0) % step_frames) / step_frames
        z = bounce * math.sin(math.pi * ph)
        yaw = math.atan2(d.x, -d.y) if d.length > 1e-6 else root.rotation_euler.z
        anim.key(root, "location", f, (p.x, p.y, p.z + z), "CONSTANT")
        anim.key(root, "rotation_euler", f, (math.radians(-12), sway * math.sin(2 * math.pi * (f - f0) /
                                                                              (2 * step_frames)), yaw), "CONSTANT")
        anim.squash(body, f, -0.12 if ph < 0.2 else 0.06, "CONSTANT")


# ---------------------------------------------------------------- the bird

def tilt(rig, f, angle=0.45, hold=10):
    """A curious head tilt at f (roll `angle` radians), overshooting and settling, held `hold` frames, then back."""
    head = rig["head"]
    r0 = tuple(head.rotation_euler)
    for df, k in ((0, 0.0), (2, 1.25), (4, 0.95), (6, 1.0)):
        anim.key(head, "rotation_euler", f + df, (r0[0], angle * k, r0[2]), "CONSTANT")
    anim.key(head, "rotation_euler", f + 6 + hold, (r0[0], angle, r0[2]), "CONSTANT")
    anim.key(head, "rotation_euler", f + 8 + hold, r0, "CONSTANT")


def lock_on(rig, target, f, down=0.35):
    """The bird locks on: its head turns to the world point `target` (a small overshoot), the eyes narrow and slant
    into a glare and the crest rises (butcherbird.stare, aimed)."""
    from . import butcherbird
    bpy.context.view_layer.update()
    h = rig["head"].matrix_world.translation
    d = Vector(target) - h
    root_yaw = rig["root"].matrix_world.to_euler().z
    turn = math.atan2(d.x, -d.y) - root_yaw                        # facing d at rest -Y: z = atan2(d.x, -d.y)
    turn = (turn + math.pi) % (2 * math.pi) - math.pi
    butcherbird.stare(rig, f, down=down, turn=turn * 1.12)          # overshoot ...
    anim.key(rig["head"], "rotation_euler", f + 9, (down, 0, turn), "CONSTANT")   # ... and settle
