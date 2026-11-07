"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), bGqrs.

    S13 "So I put the light below them."  The setup of the payoff. Night on the village edge; the swarm circles Kai's
        raised left wrist (as S10-S12 leave it). He crouches, sits back and drops flat on his back in the grass
        (LYING_V3's legs, a small bounce on landing), then lays his left arm out on the ground, palm up: the mark faces
        the sky and glows up through the grass. The swarm follows the light down and hangs above him, lit coral from
        below: the light is now clearly BELOW the moths. A determined face, eyes on the swarm; the shrimp ducks flat on
        his left shoulder, then peeks up. A slow push-in on 1s, the characters on 2s.

Night look: helper 9's night grade when it lands (diorama_ep03/helper9.py), a stand-in until then. The swarm: helper
6's mk/fluffmoth.swarm() when it lands, stand-in fluffmoths until then. The 2D pass (the coral zigzag on his wrist,
helper 9's post_helper9.mark, and its glow up through the grass) reads build/monsters/diorama_ep03/S13_mark.json.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S13 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Euler, Matrix, Vector

from channels.monsters.diorama_ep02 import helper4 as E2         # SHRIMP_IN_HAND (one shrimp size everywhere)
from channels.monsters.diorama_ep02 import helper9 as H9         # CORAL, MARK_U, _forearm, _mark_geo, _px, village
from channels.monsters.diorama_ep02 import xprl as X             # _world, _cam_move
from channels.monsters.ep01v2 import bgqrs as s3d                # _fix_pivots
from channels.monsters.ep01v2 import helper10 as s15             # _pose, _key_pose, _flush_keys, _world, _ground
from channels.monsters.mk import acting, anim, fluffmoth, hero, look, puffshrimp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
FPS = 24
SCALE = 5.8

# where: the grass on the village's north edge, east of the track (helper 9's Ep 2 village; helper 1's lane runs down
# the track). He falls backward to the west, so he lies east-west, his head west, his left side (the mark) north.
S13_AT = Vector((12.0, -140.0, 0.0))     # his feet when he stands at frame 1
S13_HEAD = 90.0                          # compass of his head once he lies (0 = +Y, 90 = -X: west)
S13_LIGHT = 220.0                        # the mark's coral point light at full, at night (the key light)
S13_UNDER = 900.0                        # the broad coral glow just above the wrist that lights the swarm's bellies
SWARM_N = 26                             # stand-in moths (helper 6's swarm replaces them)
SWARM_SCALE = 0.42


def _timing():
    with open(TIMING) as f:
        return json.load(f)


def _frames(shot, fallback):
    try:
        return next(s for s in _timing()["shots"] if s["shot"] == shot)["render_frames"]
    except (OSError, StopIteration, KeyError, ValueError):
        return fallback


def _words(shot, fallback=()):
    """[(word, first frame, last frame)] of the shot's line, 1-based within the shot."""
    try:
        d = _timing()
        s0 = next(s["start"] for s in d["shots"] if s["shot"] == shot)
        out = []
        for ln in d["lines"]:
            if ln["scene"] == shot:
                out += [(w["w"].strip(".,!?:").lower(), 1 + round((w["start"] - s0) * FPS),
                         1 + round((w["end"] - s0) * FPS)) for w in ln["words"]]
        return out or list(fallback)
    except (OSError, StopIteration, KeyError, ValueError):
        return list(fallback)


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------------------------------------------------ night
def _night():
    """Helper 9's night grade if it has landed, else a stand-in: a deep-blue painted sky, a cool low moon (a dim sun)
    and a dark-blue far haze, so the coral mark is the key light."""
    try:
        from channels.monsters.diorama_ep03 import helper9 as N9
        for name in ("night", "night_grade", "grade_night"):
            fn = getattr(N9, name, None)
            if fn:
                return fn()
    except ImportError:
        pass
    look.world(sky="#0b1430", horizon="#22336a", fill="#2c3d74", fill_strength=0.32)
    for o in bpy.data.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy = 0.55
            o.data.color = look.hexc("#9db2ff")[:3]
            o.rotation_euler = (math.radians(90 - 38), 0, math.radians(150))
    nt = bpy.context.scene.node_tree
    for nd in nt.nodes:
        if nd.type == "MIX_RGB":
            nd.inputs[2].default_value = look.hexc("#1a2552")
    return None


# ------------------------------------------------------------------------------------------------------------ Kai
# Directions in Kai's own frame (helper 10's _pose spec): +X his right, +Y forward (up once he lies), +Z toward his
# head. Parents first.
_LEGS_STAND = [("left_upper_leg", (-0.1, 0.02, -1)), ("left_lower_leg", (-0.05, -0.02, -1)),
               ("left_foot", (-0.1, 1, -0.45)),
               ("right_upper_leg", (0.1, 0.02, -1)), ("right_lower_leg", (0.05, -0.02, -1)),
               ("right_foot", (0.1, 1, -0.45))]
STAND = [("spine", (0, 0, 1)), ("chest", (0, 0.02, 1)), ("neck", (0, 0.05, 1)), ("head", (0, 0.3, 1)),
         ("left_upper_arm", (-0.45, 0.35, 0.82)), ("left_lower_arm", (-0.15, 0.3, 0.94)),   # the wrist up to the swarm
         ("left_hand", (-0.05, 0.25, 1)),
         ("right_upper_arm", (0.3, 0.05, -1)), ("right_lower_arm", (0.2, 0.3, -1)), ("right_hand", (0.15, 0.3, -1))
         ] + _LEGS_STAND
CROUCH = [("spine", (0, 0.32, 0.95)), ("chest", (0, 0.25, 1)), ("neck", (0, 0.15, 1)), ("head", (0, 0.45, 1)),
          ("left_upper_arm", (-0.4, 0.55, 0.45)), ("left_lower_arm", (-0.1, 0.6, 0.8)), ("left_hand", (0, 0.5, 1)),
          ("right_upper_arm", (0.35, 0.6, -0.5)), ("right_lower_arm", (0.15, 0.95, -0.1)),
          ("right_hand", (0.1, 1, 0)),
          ("left_upper_leg", (-0.14, 0.75, -0.66)), ("left_lower_leg", (-0.05, -0.62, -0.78)),
          ("left_foot", (-0.1, 1, -0.3)),
          ("right_upper_leg", (0.14, 0.75, -0.66)), ("right_lower_leg", (0.05, -0.62, -0.78)),
          ("right_foot", (0.1, 1, -0.3))]
SIT = [("spine", (0, 0.45, 0.9)), ("chest", (0, 0.3, 1)), ("neck", (0, 0.25, 1)), ("head", (0, 0.5, 1)),
       ("left_upper_arm", (-0.3, 0.9, 0.1)), ("left_lower_arm", (-0.05, 0.9, 0.45)), ("left_hand", (0, 0.8, 0.6)),
       ("right_upper_arm", (0.3, 0.9, 0.0)), ("right_lower_arm", (0.1, 0.95, 0.3)), ("right_hand", (0.05, 0.9, 0.4)),
       ("left_upper_leg", (-0.14, 0.98, -0.15)), ("left_lower_leg", (-0.05, -0.15, -1)),
       ("left_foot", (-0.1, 1, -0.2)),
       ("right_upper_leg", (0.14, 0.98, -0.15)), ("right_lower_leg", (0.05, -0.15, -1)),
       ("right_foot", (0.1, 1, -0.2))]
LANDED = [("spine", (0, 0.1, 1)), ("chest", (0, 0.12, 1)), ("neck", (0, 0.35, 1)), ("head", (-0.15, 0.6, 1)),
          ("left_upper_arm", (-0.45, 0.6, 0.3)), ("left_lower_arm", (0.1, 0.85, 0.4)), ("left_hand", (0.2, 0.7, 0.6)),
          ("right_upper_arm", (0.5, 0.4, -0.6)), ("right_lower_arm", (0.3, 0.3, -0.9)), ("right_hand", (0.2, 0.2, -1)),
          ("left_upper_leg", (-0.14, 0.8, -0.6)), ("left_lower_leg", (-0.05, -0.75, -0.62)),
          ("left_foot", (-0.1, 0.3, -1)),
          ("right_upper_leg", (0.18, 0.75, -0.65)), ("right_lower_leg", (0.08, -0.7, -0.7)),
          ("right_foot", (0.15, 0.4, -1))]
# on his back: LYING_V3's legs (the left knee up, the right leg out), the right arm loose by his side, the head rolled
# to his left (toward the wrist and the camera), chin up to watch the swarm; the left arm is set by _arm_out()
LIE = [("spine", (0, 0, 1)), ("chest", (0, 0.05, 1)), ("neck", (-0.08, 0.15, 1)), ("head", (-0.4, 0.45, 1)),
       ("left_upper_arm", (-0.45, 0.6, 0.3)), ("left_lower_arm", (0.1, 0.85, 0.4)), ("left_hand", (0.2, 0.7, 0.6)),
       ("right_upper_arm", (0.45, -0.12, -1)), ("right_lower_arm", (0.3, -0.08, -1)), ("right_hand", (0.25, 0, -1)),
       ("left_upper_leg", (-0.12, 0.85, -0.55)), ("left_lower_leg", (-0.05, -0.75, -0.7)),
       ("left_foot", (-0.1, 0.4, -1)),
       ("right_upper_leg", (0.2, 0.2, -1)), ("right_lower_leg", (0.12, -0.05, -1)), ("right_foot", (0.35, 1, -0.3))]
ARM_IN = [("left_upper_arm", (-0.45, 0.6, 0.3)), ("left_lower_arm", (0.1, 0.85, 0.4)), ("left_hand", (0.2, 0.7, 0.6))]
ARM_OUT = [("left_upper_arm", (-0.95, -0.2, 0.22)), ("left_lower_arm", (-0.78, -0.16, 0.6)),
           ("left_hand", (-0.62, -0.12, 0.78))]           # laid out on the grass beside his head, the hand flat


def _blend(a, b, u):
    """Normalised lerp of two specs (bone order from a, bones missing in one taken from the other)."""
    da, db = dict(a), dict(b)
    order = [n for n, _ in a] + [n for n, _ in b if n not in da]
    out = []
    for n in order:
        va, vb = Vector(da.get(n, db.get(n))).normalized(), Vector(db.get(n, da.get(n))).normalized()
        v = va.lerp(vb, u)
        out.append((n, tuple(v.normalized() if v.length > 1e-4 else vb)))
    return out


def _twist(k, name, deg):
    """Roll a bone about its own length (pose space)."""
    pb = s15._bone(k, name)
    if pb is None or abs(deg) < 1e-3:
        return
    m = pb.matrix.copy()
    pb.matrix = m @ Matrix.Rotation(math.radians(deg), 4, "Y")
    bpy.context.view_layer.update()


def _bone_world(k, name, tail=False):
    pb = k["arm"].pose.bones[name]
    return k["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _palm_up_score(k, arm_dir):
    """How well the laid-out left palm (the inner wrist, the mark) faces the sky: on the ground with the arm out, a
    palm-up hand has its thumb pointing at sky x arm (toward his head side), across the arm."""
    h = _bone_world(k, "hand.L")
    t = _bone_world(k, "thumb.02.L")
    want = Vector((0, 0, 1)).cross(arm_dir).normalized()
    return (t - h).normalized().dot(want)


def _twist_for_palm_up(k):
    """The forearm roll (degrees) that turns the laid-out left palm to the sky (searched in 15-degree steps)."""
    names = ("forearm.L", "hand.L")
    base = {nm: k["arm"].pose.bones[nm].rotation_quaternion.copy() for nm in names}
    arm_dir = _bone_world(k, "hand.L") - _bone_world(k, "forearm.L")
    arm_dir = Vector((arm_dir.x, arm_dir.y, 0)).normalized()
    best = (0, -9.0)
    for deg in range(-180, 181, 15):
        for nm, q in base.items():
            k["arm"].pose.bones[nm].rotation_quaternion = q
        bpy.context.view_layer.update()
        _twist(k, "left_lower_arm", deg)
        sc_ = _palm_up_score(k, arm_dir)
        if sc_ > best[1]:
            best = (deg, sc_)
    for nm, q in base.items():
        k["arm"].pose.bones[nm].rotation_quaternion = q
    bpy.context.view_layer.update()
    return best


def _head_dir():
    h = math.radians(S13_HEAD)
    return Vector((-math.sin(h), math.cos(h), 0.0))


def _kai_drop(k, n, beats):
    """Key Kai's drop on 2s: stand (wrist up) -> a dip -> sit back -> flat on his back (a bounce) -> the left arm laid
    out, palm up. Each keyed frame: the blended spec, the body tipped back by theta, the hips moved back along the
    head direction, then grounded on the grass (his lowest point)."""
    hd = _head_dir()
    yaw = math.pi + math.radians(S13_HEAD)
    f_d0, f_sit, f_land, f_settle, f_arm0, f_arm1 = (beats[x] for x in ("dip", "sit", "land", "settle",
                                                                         "arm0", "arm1"))
    # (frame, spec, theta deg, hips back along hd)
    keys = [(1, STAND, 0.0, 0.0), (f_d0, CROUCH, -6.0, 0.35), (f_sit, SIT, 38.0, 1.6), (f_land, LANDED, 93.0, 3.0),
            (f_settle, LIE, 89.0, 3.0), (f_settle + 4, LIE, 90.0, 3.0)]
    # the palm-up forearm roll, found once on the final pose (on his back, the arm out)
    rot_lie = (math.radians(90.0), 0, yaw)
    s15._pose(k, _with_arm(LIE, 1.0), (0, 0, 0), rot_lie)
    twist = _twist_for_palm_up(k)
    print("S13 palm-up roll", twist)
    twist = twist[0]
    for f in range(1, n + 1, 2):
        i = max(j for j in range(len(keys)) if keys[j][0] <= f)
        if i + 1 < len(keys):
            a, b = keys[i], keys[i + 1]
            u = _ease((f - a[0]) / (b[0] - a[0]))
        else:
            a = b = keys[-1]
            u = 1.0
        spec = _blend(a[1], b[1], u)
        theta = a[2] + (b[2] - a[2]) * u
        back = a[3] + (b[3] - a[3]) * u
        v = _ease((f - f_arm0) / max(1, f_arm1 - f_arm0)) if f >= f_arm0 else 0.0
        if v > 0:                                                # the left arm out to the grass, palm up
            spec = _with_arm(spec, v)
        r = Euler((math.radians(theta), 0, yaw)).to_matrix()
        s15._pose(k, [x for x in spec if x[0] != "left_hand"], (0, 0, 0), (math.radians(theta), 0, yaw))
        if v > 0:
            _twist(k, "left_lower_arm", twist * v)
        s15._aim(k, "left_hand", r @ Vector(dict(spec)["left_hand"]))
        hip = s15._world(k, "hips")
        target = S13_AT + hd * back
        k["arm"].location += Vector((target.x - hip.x, target.y - hip.y, 0))
        s15._ground(k)
        if f_land <= f < f_land + 4:                             # the landing bounce: a small lift off the grass
            k["arm"].location.z += 0.22 * math.sin(math.pi * (f - f_land) / 4)
        bpy.context.view_layer.update()
        s15._key_pose(k, f)
    s15._flush_keys(k)
    return twist


def _with_arm(spec, v):
    """spec with the left arm replaced by ARM_IN -> ARM_OUT at v (0..1)."""
    keep = [(nm, d) for nm, d in spec if nm not in dict(ARM_IN)]
    return keep + _blend(ARM_IN, ARM_OUT, v)


# ------------------------------------------------------------------------------------------------------------ shrimp
def _shoulder_shrimp(k, n, beats, name="ep03_shrimp_s13"):
    """The puff-shrimp riding his left shoulder (E2.SHRIMP_IN_HAND, the one shrimp size): it clings flat (a squash,
    eyes shut) as he drops, rides him down, then peeks up at the swarm with its eyes open."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    s3d._fix_pivots(sh)
    base = E2.SHRIMP_IN_HAND
    sh["root"].scale = (base,) * 3
    sc = bpy.context.scene
    f_duck, f_peek = beats["dip"] - 2, beats["arm1"] + 6
    lying_from = beats["land"]
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        sq = 0.62 if f_duck <= f < f_peek else 1.0
        side = (k["arm"].matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized()    # his left (the model faces -Y)
        p = _bone_world(k, "upper_arm.L") + Vector((0, 0, 0.55 * sq)) + side * 0.25
        sh["root"].location = p
        sh["root"].keyframe_insert("location", frame=f)
        lie = _ease((f - beats["sit"]) / max(1, lying_from - beats["sit"]))
        sh["root"].rotation_euler = (-0.55 * lie * (1.0 if f >= f_peek else 0.4), 0, math.radians(S13_HEAD))
        sh["root"].keyframe_insert("rotation_euler", frame=f)
        sh["root"].scale = (base * (1.18 if sq < 1 else 1.0), base * (1.18 if sq < 1 else 1.0), base * sq)
        sh["root"].keyframe_insert("scale", frame=f)
    sc.frame_set(1)
    for fc in anim.all_fcurves(sh["root"].animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.55, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.15, 0.0, 0.0), "CONSTANT")
    for e in sh["eyes"]:                                         # eyes squeezed shut while it ducks
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", f_duck, (1, 1, 0.08), "CONSTANT")
        anim.key(e, "scale", f_peek, (1, 1, 1), "CONSTANT")
    anim.blink(sh, f_peek + 22)
    return sh


# ------------------------------------------------------------------------------------------------------------ swarm
def _swarm(n, centre_at, seed=13):
    """The fluffmoths circling the light: helper 6's swarm() if it has landed, else stand-in fluffmoths in a loose
    dome round the vertical through the light, following it down (centre_at(f) -> the light's world position) and
    circling slowly; wings on 1s, the rest on 2s. Returns the moth roots."""
    rnd = random.Random(seed)
    moths = []
    sc = bpy.context.scene
    for i in range(SWARM_N):
        rig = fluffmoth.build((0, 0, 0), name=f"m13_{i}")
        s = SWARM_SCALE * rnd.uniform(0.75, 1.15)
        rig["root"].scale = (s, s, s)
        r = rnd.uniform(2.2, 7.5)
        h = rnd.uniform(4.5, 11.0)
        a0 = rnd.uniform(0, 2 * math.pi)
        w = rnd.choice((-1, 1)) * rnd.uniform(0.9, 1.6) * 2 * math.pi / (FPS * 6.0)   # a turn every ~4-7 s
        rig["shadow"].hide_render = True
        for f in range(1, n + 1, 2):
            c = centre_at(f)
            a = a0 + w * f
            bob = 0.35 * math.sin(f / 9.0 + i)
            rig["root"].location = (c.x + math.cos(a) * r, c.y + math.sin(a) * r, c.z + h + bob)
            rig["root"].keyframe_insert("location", frame=f)
            # its front along the circle, banked a little in toward the light (its back tilted to it)
            tang = Vector((-math.sin(a), math.cos(a), 0)) * (1 if w > 0 else -1)
            yaw = math.atan2(-tang.x, tang.y) + math.pi
            rig["root"].rotation_euler = (0.0, 0.32 * (1 if w > 0 else -1), yaw)
            rig["root"].keyframe_insert("rotation_euler", frame=f)
        fluffmoth.idle(rig, 1, n, seed=seed + i)
        moths.append(rig)
    for rig in moths:
        for fc in anim.all_fcurves(rig["root"].animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    sc.frame_set(1)
    return moths


# ------------------------------------------------------------------------------------------------------------ S13
def _grass_at(p, seed=5):
    """A ring of grass blades round the laid-out wrist (the glow comes up through them)."""
    from channels.monsters.mk import diorama
    rnd = random.Random(seed)
    blade = diorama.lit_paint("s13_tuft", "#2f8a36", "#4cb348", "#8fdb62")
    for j in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(0.35, 1.25)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.07, radius2=0.0, depth=rnd.uniform(0.5, 1.0),
                                        location=(p.x + math.cos(a) * r, p.y + math.sin(a) * r, 0.3))
        o = bpy.context.object
        o.name = "s13_tuft"
        o.rotation_euler = (rnd.uniform(-0.45, 0.45), rnd.uniform(-0.45, 0.45), rnd.uniform(0, 3))
        o.data.materials.append(blade)


def s13():
    n = _frames("S13", 60)
    W = _words("S13")
    fw = {}
    for w_, a_, b_ in W:
        fw.setdefault(w_, []).append((a_, b_))
    f_below = fw.get("below", [(int(n * 0.55), 0)])[0][0]         # the glow blooms on "below"
    beats = dict(dip=4, sit=10, land=15, settle=18)
    beats["arm0"] = max(beats["settle"] + 2, f_below - 12)
    beats["arm1"] = beats["arm0"] + 9
    beats["glow"] = beats["arm1"] - 1
    X._world(n)
    _night()
    sc = bpy.context.scene
    try:
        H9.village_and_lake()
    except Exception as e:                                       # the set is optional for a test still
        print("S13: no village", e)

    k = hero.load((0, 0, 0), scale=SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    _kai_drop(k, n, beats)

    # the wrist at rest (for the grass, the light and the swarm's centre)
    sc.frame_set(n)
    wrist_end = H9._forearm(k, 1.0)
    _grass_at(wrist_end)
    acting.grass_round(s15._world(k, "hips"), _head_dir())
    sc.frame_set(1)

    # the mark's light: the coral key at the wrist (lighting his arm, face and the grass), and a broad glow just above
    # it that lights the swarm's bellies from below once he lies
    def level(f):
        if f < beats["glow"]:
            return 0.55                                        # glowing as in S10-S12 (wrist up)
        if f < beats["glow"] + 4:
            return 0.55 + 0.85 * (f - beats["glow"]) / 4       # the bloom on "below"
        return 1.4 - 0.3 * _ease((f - beats["glow"] - 4) / 8) + 0.05 * math.sin(f / 5.0)

    key = bpy.data.lights.new("s13_mark_key", "POINT")
    key.color = H9.CORAL
    key.shadow_soft_size = 0.2
    lk = bpy.data.objects.new("s13_mark_key", key)
    sc.collection.objects.link(lk)
    und = bpy.data.lights.new("s13_mark_under", "POINT")
    und.color = H9.CORAL
    und.shadow_soft_size = 1.5
    und.use_shadow = False
    lu = bpy.data.objects.new("s13_mark_under", und)
    sc.collection.objects.link(lu)

    def mark_at(f):
        sc.frame_set(f)
        return H9._forearm(k, H9.MARK_U)

    for f in range(1, n + 1):
        m = mark_at(f)
        lk.location = m + Vector((0, 0, 0.5))
        lk.keyframe_insert("location", frame=f)
        key.energy = S13_LIGHT * level(f)
        key.keyframe_insert("energy", frame=f)
        lu.location = m + Vector((0, 0, 1.6))
        lu.keyframe_insert("location", frame=f)
        und.energy = S13_UNDER * level(f) * (0.35 + 0.65 * _ease((f - beats["land"]) / 10))
        und.keyframe_insert("energy", frame=f)

    centres = {f: mark_at(f) for f in range(1, n + 1)}
    moths = _swarm(n, lambda f: centres[f])
    sh = _shoulder_shrimp(k, n, beats)

    # face: tense, then determined (brows down, mouth set) from the drop on; eyes on the swarm
    acting.face_keys(k, 1, eye_brow_down=0.35, face_angry=0.1)
    acting.face_keys(k, beats["dip"], eye_brow_down=0.75, face_angry=0.3, mouth_short=0.35)
    acting.face_keys(k, beats["glow"], eye_brow_down=0.65, face_angry=0.2, mouth_short=0.2, face_happy=0.12)
    swarm_mid = centres[n] + Vector((0, 0, 7.5))
    acting.look_at(k, swarm_mid, 1, n, darts=True, seed=4)
    acting.blink(k, 1, n, every=(48, 80), seed=6, at=(beats["land"],))

    # camera: north of him, a little toward his feet, looking south over the village: he drops from a profile (facing
    # east, frame right) to lying across the frame, the light low, the swarm high; a slow push-in on 1s
    hd = _head_dir()
    left = Vector((-hd.y, hd.x, 0)) * -1.0                       # his left once lying: north
    body_mid = S13_AT + hd * 2.4
    c_dir = (left * 1.0 - hd * 0.32).normalized()
    t0 = body_mid + Vector((0, 0, 5.2))
    t1 = body_mid + hd * 0.4 + Vector((0, 0, 4.2))
    c0 = t0 + c_dir * 24.0 + Vector((0, 0, 1.2))
    c1 = t1 + c_dir * 21.0 + Vector((0, 0, 1.0))
    cam = _cam_from("S13cam", n, c0, c1, t0, t1, 30.0)
    sc.frame_set(1)

    # the 2D pass: the mark on screen per frame, its glow level, the wrist point
    if "--still" not in sys.argv:
        out = {}
        for f in range(1, n + 1):
            sc.frame_set(f)
            out[f] = dict(H9._mark_geo(k, cam), level=round(level(f), 3),
                          wrist=H9._px(cam, H9._forearm(k, 1.0)))
        os.makedirs(BUILD, exist_ok=True)
        with open(os.path.join(BUILD, "S13_mark.json"), "w") as fh:
            json.dump(dict(meta=beats, frames=out), fh)
        sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + list(k.get("cap", [])),
                beats=beats)


def _cam_from(name, n, c0, c1, t0, t1, lens):
    """X._cam_move from two camera positions and aim points (the diorama blur/haze), on 1s."""
    def pose(c, t):
        v = c - t
        dist = v.length
        tilt = math.degrees(math.asin(max(-1.0, min(1.0, v.z / dist))))
        yaw = math.degrees(math.atan2(-v.x, -v.y))
        return (tuple(t), dist, tilt, yaw, lens, 0.0)
    return X._cam_move(name, n, pose(c0, t0), pose(c1, t1))


SHOTS = {"S13": s13}
