"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md), XprL: Wren's shots.

    S08 (Wren) "Ring the bells! Bells will drive them off!"
        Night. Wren on a hut's porch rings her bell hard with both hands (wren.ring_hard, the clapper on 2s), shouting
        (lip-sync from the word times, face 'shout'); the other porch bells swing behind her. Kai's mark is the key
        light from off-screen down the lane (coral), a cool moon fill. A slow push-in from a low 3/4.
    S16 "Wren lowered her bell."
        Close on Wren in the lane, a few steps from Kai (off-screen, his mark lighting her from the front-left): the
        bell comes down slowly (wren.lower_bell) over the line, and her stern face cracks (stern -> softening, eyes
        wide) on "bell". Upside-down moths at her feet. Slow push-in.
    S17 (Wren) "The village wants you gone by sunrise."
        She steps in and kneels beside Kai (who sits up among the dazed moths, the shrimp on his left shoulder, the
        mark glowing on his left wrist), worried; on "village" she glances back over her shoulder at the shuttered
        huts (eyes in the window cracks), then back to him on "gone". Two-shot, slow push-in.

Staging: Kai sits where S15 leaves him (bGqrs's S13 spot, when bgqrs.py exposes it; a stand-in on the track into the
village until then), facing west, his left (mark) side toward the village (south). Wren comes from the village and
kneels at his left. Night: helper 9's ep03 night grade + mark light when they land, a stand-in until then.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S16 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import importlib
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import helper9 as H9
from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, fluffmoth, hero, look, puffshrimp, wren

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")
FPS = 24
SCALE = X.SCALE
CORAL = (1.0, 0.48, 0.36)
MOON = (0.62, 0.72, 1.0)
SHRIMP_K = 0.6                      # the puff-shrimp on his shoulder (helper 4's S01 / bGqrs's S13)
MARK_W = 220.0                      # the mark light at night (bGqrs's S13_LIGHT)
CRACK = 0.07                        # shutters closed to a crack (S17: eyes peeking through)
MOTH_K = 0.42                       # the dazed upside-down moths left from S14/S15 (bGqrs's size)

# --- staging: bGqrs's S13 spot (diorama_ep03/bgqrs.py S13_AT / S13_HEAD): Kai fell back to the west, so he lies with
# his head west; S15 sits him up facing EAST, his left (the mark) side north, the village (helper 9's Ep 2 village;
# helper 1's lane when it lands) to the south, on his right. Wren comes up from the village and kneels on that side.
try:
    from channels.monsters.diorama_ep03.bgqrs import S13_AT as _AT
except ImportError:                                  # pragma: no cover (bgqrs.py is in the repo)
    _AT = Vector((12.0, -140.0, 0.0))
KAI_SIT = Vector(_AT) + Vector((-2.42, 0.0, 0.0))    # armature origin sitting: hips (0.58 west of it) at (9.0, -140), helper 5's S15
KAI_YAW3 = 90.0                                      # facing east; his left (+X local) points north
TO_VILLAGE = Vector((0.0, -1.0, 0.0))
WREN_KNEEL = KAI_SIT + Vector((2.0, -2.8, 0.0))      # at his front-right (the village side), turned to him
WREN_S16 = KAI_SIT + Vector((1.6, -7.0, 0.0))        # S16: standing a few steps off on the village side, facing him


def _yaw_to(src, dst):
    """rot_z (degrees) that turns a character's front (-Y) from src toward dst."""
    d = Vector(dst) - Vector(src)
    return math.degrees(math.atan2(d.x, -d.y))


WREN_YAW3 = _yaw_to(WREN_KNEEL, KAI_SIT)


# ------------------------------------------------------------------------------------------------------------ timing
def _shot(shot):
    with open(TIMING) as fh:
        t = json.load(fh)
    s = next(x for x in t["shots"] if x["shot"] == shot)
    return s, t


def frames(shot):
    return _shot(shot)[0]["render_frames"]


def words(shot):
    """[(word, first frame, last frame)] of the shot's line (frame 1 = the shot's start)."""
    s, t = _shot(shot)
    out = []
    for ln in t["lines"]:
        if ln.get("scene") == shot:
            for w in ln["words"]:
                a = round((w["start"] - s["start"]) * FPS) + 1
                b = round((w["end"] - s["start"]) * FPS) + 1
                out.append((w["w"].strip(".,!?:;").lower(), a, b))
    return out


def at(shot, word, k=0):
    hits = [a for w, a, b in words(shot) if w == word]
    return hits[min(k, len(hits) - 1)]


def _line_words(shot):
    s, t = _shot(shot)
    for ln in t["lines"]:
        if ln.get("scene") == shot:
            return ln["words"], s["start"]
    return [], s["start"]


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _bone_world(rig, name, tail=False):
    pb = rig["arm"].pose.bones[name]
    return rig["arm"].matrix_world @ (pb.tail if tail else pb.head)


# ------------------------------------------------------------------------------------------------------------ world
def _optional(name):
    """Another helper's diorama_ep03 module if it has landed, else None (only a missing module is tolerated)."""
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{name}.py")):
        return None
    return importlib.import_module(f"channels.monsters.diorama_ep03.{name}")


def _night(n):
    """The island at night: helper 9's ep03 night grade if it has landed, else a stand-in (navy sky, the sun turned
    into a dim cool moon, the haze darkened)."""
    X._world(n)
    N9 = _optional("helper9")
    if N9 is not None and hasattr(N9, "night"):
        return N9.night(n)
    return _optional("bgqrs")._night()                 # bGqrs's stand-in (the same look as S13) until then


def _village_backdrop(shut=None):
    """Helper 9's Ep 2 village and lake, plus helper 1's night lane of huts (diorama_ep03/village.py) when it is in.
    `shut`: a frame from which every door is shut and every shutter closed to a crack (after the swarm). Returns the
    lane's huts (or [])."""
    H9.village_and_lake()
    V = _optional("village")
    if V is None:
        return []
    huts = V.lane()
    if shut is not None:
        for h in huts:
            V.set_door(h, shut, 0.0)
            if hasattr(V, "peek"):                                        # helper 1's cracked shutters (~7 degrees)
                V.bang_shutters(h, shut - 11, crack=0.06)
            else:
                V.set_shutters(h, shut, CRACK)
    return huts


def _peeking_eyes(hut, n, seed=0):
    """Two eyes in the crack between a hut's nearly shut shutters (S17: the village watching), blinking now and then
    and sliding a little to look."""
    rnd = random.Random(seed)
    win = bpy.data.objects[hut["root"].name + "_win"]
    white = look.flat("x3_eye_white", look.hexc("#f4efe2"), strength=4.0)      # glows through the night grade
    ink = look.flat("x3_eye_ink", look.hexc("#140f18"))
    out = []
    for sx in (-1, 1):
        e = bpy.data.objects.new(f"{hut['root'].name}_eye{sx}", None)
        bpy.context.scene.collection.objects.link(e)
        e.parent = win
        e.location = (sx * 0.17, -0.02, 0.12)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, segments=12, ring_count=8)
        w = bpy.context.object
        w.data.materials.append(white)
        w.parent = e
        w.location = (0, 0, 0)
        w.scale = (1.0, 0.5, 0.75)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.055, segments=10, ring_count=6)
        pu = bpy.context.object
        pu.data.materials.append(ink)
        pu.parent = e
        pu.location = (0, -0.05, 0)
        out.append(e)
    blinks = [rnd.randint(10, 30), rnd.randint(40, 60)]
    for f in range(1, n + 1, 2):
        shut_ = any(b <= f < b + 2 for b in blinks)
        for k, e in enumerate(out):
            e.scale = (1.0, 1.0, 0.12 if shut_ else 1.0)
            e.keyframe_insert("scale", frame=f)
    return out


def _mark_light(k, n, toward, energy=MARK_W, seed=5):
    """Kai's mark, the key light at night: helper 9's N9.mark(k) (on his left forearm, calibrated for the night
    grade) once it is in; until then a coral point light at the wrist with a slow uneven pulse."""
    N9 = _optional("helper9")
    if N9 is not None and hasattr(N9, "mark"):
        return N9.mark(k)
    d = bpy.data.lights.new("x3_mark_light", "POINT")
    d.color = CORAL
    d.shadow_soft_size = 0.2
    lt = bpy.data.objects.new("x3_mark_light", d)
    bpy.context.scene.collection.objects.link(lt)
    rnd = random.Random(seed)
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        m = _bone_world(k, "forearm.twist.L").lerp(_bone_world(k, "hand.L"), 0.4)
        lt.location = m + (Vector(toward) - m).normalized() * 0.5
        lt.keyframe_insert("location", frame=f)
        d.energy = energy * (0.9 + 0.1 * math.sin(f / 6.0) + 0.04 * rnd.random())
        d.keyframe_insert("energy", frame=f)
    sc.frame_set(1)
    return lt


def _offscreen_mark(pos, n, energy=None, k=1.0):
    """Kai's mark lighting a shot he isn't in (S08, S16): a coral point light at his wrist's spot, pulsing (helper
    9's mark power and no shadows once the night grade is in: the grade warms what the coral light reaches)."""
    N9 = _optional("helper9")
    if energy is None:
        energy = getattr(N9, "MARK_W", MARK_W * 1.6) if N9 is not None else MARK_W * 1.6
    d = bpy.data.lights.new("x3_mark_off", "POINT")
    d.color = CORAL
    d.shadow_soft_size = 0.3
    d.use_shadow = N9 is None
    energy *= k
    lt = bpy.data.objects.new("x3_mark_off", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.location = pos
    for f in range(1, n + 1, 2):
        d.energy = energy * (0.92 + 0.08 * math.sin(f / 6.0))
        d.keyframe_insert("energy", frame=f)
    return lt


def _dazed_moths(n, spots, seed=21):
    """A few fluffmoths on their backs in the grass (S14 left them there), legs waving, eye-spots dazed."""
    out = []
    rnd = random.Random(seed)
    for i, (x, y) in enumerate(spots):
        m = fluffmoth.build((x, y, 0), name=f"x3_dazed{i}")
        m["root"].scale = (MOTH_K,) * 3
        m["root"].rotation_euler = (0, 0, rnd.uniform(0, 2 * math.pi))
        fluffmoth.upside_down(m, 1, n, seed=seed + i)
        out.append(m)
    return out


# ------------------------------------------------------------------------------------------------------------ people
def _wren_at(at, yaw):
    w = wren.load((0, 0, 0), scale=SCALE)
    w["arm"].rotation_euler = (0, 0, math.radians(yaw))
    w["arm"].location = at
    bpy.context.view_layer.update()
    return w


def _kai_sitting(n, look_at=None):
    """Kai sitting up in the grass where the flip left him (S15's end): legs out, leaning back on his right hand, his
    left forearm resting on his raised left knee with the mark up; breathing on 2s; he looks at `look_at`."""
    k = hero.load((0, 0, 0), scale=SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    k["arm"].rotation_euler = (0, 0, math.radians(KAI_YAW3))
    k["arm"].location = KAI_SIT
    bpy.context.view_layer.update()
    P = x3.Pose(k)
    yaw_look = 0.0
    if look_at is not None:
        loc = k["arm"].matrix_world.inverted() @ Vector(look_at)
        yaw_look = math.degrees(math.atan2(loc.x, -loc.y))
    for f in range(1, n + 1, 2):
        P.reset()
        hz = P.pb["hips"].matrix.translation.z
        P.hips((0, 0.1, 0.13 - hz))
        P.leg("L", (0.12, -0.36, P.ankle_h))                     # left knee up (the arm rests on it)
        P.leg("R", (-0.13, -0.62, P.ankle_h))                    # right leg out
        P.rot("spine", (-6, 0, 0))
        b = math.sin(f / 9.0)
        P.rot("chest", (1.5 * b, 0, yaw_look * 0.35))
        P.rot("head 1", (-4, 0, yaw_look * 0.5))
        bpy.context.view_layer.update()
        kn = P.pb["shin.L"].matrix.translation
        wren.reach(P, "L", kn + Vector((-0.04, -0.06, 0.05)), pole=(1, 0.4, 0), hand=(-0.6, -0.6, 0.2))
        P.twist("forearm.L", -70)                                # inside of the forearm (the mark) turned up
        wren.reach(P, "R", Vector((-0.2, 0.22, 0.05)), pole=(-1, 0.6, 0), hand=(0, 0.5, -1))
        P.key(f)
    return k


def _shoulder_shrimp(k, n, name="x3_shrimp"):
    """The puff-shrimp on Kai's left shoulder (helper 3's S02 way), breathing and blinking."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    sh["root"].scale = (SHRIMP_K,) * 3
    sh["root"].rotation_euler = (0, 0, math.radians(KAI_YAW3))
    sc = bpy.context.scene
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        sh["root"].location = _bone_world(k, "upper_arm.L") + Vector((0, 0, 0.32))
        sh["root"].keyframe_insert("location", frame=f)
    sc.frame_set(1)
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 20)
    return sh


def _clear_near(cam, radius):
    """Hide the lane's porch bells and brackets right in front of the lens (soft blobs across the frame)."""
    bpy.context.scene.frame_set(1)
    c = cam.matrix_world.translation
    for o in bpy.data.objects:
        if o.name.startswith("vhut") and any(k in o.name for k in ("_bell", "_bracket", "_clapper")):
            if (o.matrix_world.translation - c).length < radius:
                o.hide_render = True


def _cam(name, n, a, b):
    """A slow camera move on 1s (X._cam_move: target, dist, tilt, yaw, lens, shift_y)."""
    return X._cam_move(name, n, a, b)


# ------------------------------------------------------------------------------------------------------------ S16
def s16():
    n = frames("S16")
    _night(n)
    _village_backdrop(shut=1)
    w = _wren_at(WREN_S16, _yaw_to(WREN_S16, KAI_SIT))
    P = x3.Pose(w)
    f_low0, f_low1 = max(1, at("S16", "wren") - 2), at("S16", "bell") + 6          # the bell comes down over the line
    f_crack = at("S16", "bell") - 2                                                  # her face cracks
    for f in range(1, n + 1, 2):
        P.reset()
        t = (f - f_low0) / max(1, f_low1 - f_low0)
        wren.lower_bell(P, t)
        P.rot("chest", (0.8 * math.sin(f / 8.0), 0, 0))
        if f >= f_crack:                                                              # a small breath out, head up
            u = _ease((f - f_crack) / 8)
            P.rot("head 1", (-5 * u, 0, 3 * u))
        P.key(f)
    wren.grip(w, 1)
    wren.face(w, "stern", 1)
    wren.face(w, "softening", f_crack)
    wren.blink(w, 1, n, every=(200, 201), at=(f_crack + 10,))
    wren.contact_shadows(w)
    _offscreen_mark(KAI_SIT + Vector((1.2, 0.6, 2.6)), n, k=0.5)              # softer: she is close to it
    _dazed_moths(n, [(WREN_S16.x - 2.2, WREN_S16.y + 2.0), (WREN_S16.x + 2.6, WREN_S16.y + 1.2),
                     (WREN_S16.x + 0.8, WREN_S16.y + 3.4)])
    # close (chest-up), from Kai's side (north-west of her), a slow push-in
    tgt = WREN_S16 + Vector((1.0, 0, 6.3))                                    # her bell side (east) in frame
    yaw = 176.0
    _cam("S16cam", n, (tgt, 9.2, 3, yaw, 44, 0.0), (tgt, 8.2, 3, yaw, 44, 0.0))
    return dict(frames=n, step=2, ones=(1, n), subject=[w["arm"]])


# ------------------------------------------------------------------------------------------------------------ S17
def s17():
    n = frames("S17")
    _night(n)
    huts = _village_backdrop(shut=1)
    V = _optional("village")
    for i, h in enumerate(huts):                                   # the village peeking through its shutters
        if (h["root"].location - KAI_SIT).length < 45:
            if V is not None and hasattr(V, "peek"):
                V.peek(h, 1, n, blinks=(9 + 7 * i, 40 + 5 * i))
            else:
                _peeking_eyes(h, n, seed=i)
    k = _kai_sitting(n, look_at=WREN_KNEEL + Vector((0, 0, 5.0)))
    _shoulder_shrimp(k, n)
    hero.face(k, "worried", 1) if "worried" in hero.FACES else hero.face(k, "sad", 1)
    _mark_light(k, n, toward=KAI_SIT + Vector((-4, -2, 6)))
    # Wren: two steps in from the S16 spot, then down on one knee at his side (anticipation dip, overshoot settle)
    start = WREN_KNEEL + (WREN_S16 - WREN_KNEEL).normalized() * 1.6
    w = _wren_at(start, WREN_YAW3)
    P = x3.Pose(w)
    f_kneel0, f_kneel1 = 3, 15
    f_back, f_return = at("S17", "village") - 2, at("S17", "gone") - 1
    words_, t0 = _line_words("S17")
    for f in range(1, n + 1, 2):
        P.reset()
        u = _ease((f - 1) / (f_kneel1 - 1))
        w["arm"].location = start.lerp(WREN_KNEEL, u)
        w["arm"].keyframe_insert("location", frame=f)
        d = _ease((f - f_kneel0) / (f_kneel1 - f_kneel0))
        if f_kneel1 <= f < f_kneel1 + 6:                                          # the settle: a little dip
            P.hips((0, 0, -0.012 * math.sin(math.pi * (f - f_kneel1) / 6)))
        wren.kneel(P, front="L", depth=d)
        if f_back <= f < f_return + 4:                                            # the glance back at the village
            g = _ease((f - f_back) / 5) * (1 - _ease((f - f_return) / 4))
            P.rot("chest", (0, 0, 5 * g))                                     # over her left shoulder (south):
            P.rot("neck", (0, 0, 10 * g))                                     # a glance, her profile to us
            P.rot("head 1", (0, 0, 20 * g))
        else:
            P.rot("head 1", (8, 0, 0))                                            # looking down at him
        P.key(f)
    wren.grip(w, 1)
    wren.face(w, "worried", 1)
    wren.talk_words(w, words_, t0, first=1)
    wren.blink(w, 1, n, every=(200, 201), at=(f_back - 3, f_return + 8))
    wren.contact_shadows(w)
    _dazed_moths(n, [(KAI_SIT.x + 4.0, KAI_SIT.y + 2.0), (KAI_SIT.x - 2.6, KAI_SIT.y + 3.4),
                     (KAI_SIT.x + 5.2, KAI_SIT.y - 2.4), (KAI_SIT.x - 3.4, KAI_SIT.y - 4.2),
                     (KAI_SIT.x + 2.4, KAI_SIT.y + 5.0)])
    # over Kai's left shoulder from the north (the shrimp in the soft foreground): Wren facing us, kneeling on the
    # village side, the huts behind her; on "village" she looks back at them. A slow push-in.
    mid = KAI_SIT.lerp(WREN_KNEEL, 0.7) + Vector((0, 0, 4.2))
    yaw = 180.0                                                               # from the north: Wren clear of his head
    _cam("S17cam", n, (mid, 14.5, 7, yaw, 40, 0.0), (mid, 13.0, 7, yaw, 40, 0.0))
    _clear_near(bpy.context.scene.camera, 9.0)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"]])


# ------------------------------------------------------------------------------------------------------------ S08
PORCH_HUT = 2                       # helper 1's lane: hut 2 (east side, the porch nearest Kai's spot; helper 1)


def s08():
    n = frames("S08")
    _night(n)
    huts = _village_backdrop()
    V = _optional("village")
    if huts:
        h = huts[PORCH_HUT]
        face = Vector(h["face"])
        spot = Vector(h["doorstep"]) + face * 0.7 + Vector((0, 0, 0.5))       # on the deck, near the door
        if hasattr(V, "porch"):                                               # helper 1's porch(): deck height
            spot.z = V.porch(PORCH_HUT)[2]
        kai_at = V.LANE_AT
    else:                                                                     # no lane yet: a spot by the track
        face = Vector((1.0, 0.0, 0.0))
        spot = Vector((-6.0, -135.0, 0.0))
        kai_at = Vector((4.6, -131.0, 0.0))
    yaw = math.degrees(math.atan2(face.x, -face.y))
    w = _wren_at(spot, yaw)
    P = x3.Pose(w)
    words_, t0 = _line_words("S08")
    f_ring = max(3, at("S08", "ring") - 2)                                     # the first swing on "Ring"
    f_stop = min(n - 4, at("S08", "off") + 16)
    for f in range(1, n + 1, 2):
        P.reset()
        if f < f_ring:                                                        # the wind-up: bell drawn back, a dip
            u = _ease((f - 1) / max(1, f_ring - 1))
            P.hips((0, 0, -0.03 * math.sin(math.pi * u)))
            wren.ring_hard(P, 0, lift=0.5 * u)
        elif f <= f_stop:
            s = 1 if ((f - f_ring) // 2) % 2 == 0 else -1
            P.hips((0, 0, -0.012 * (1 if s > 0 else 0)))
            wren.ring_hard(P, s, lift=1.0)
        else:
            u = _ease((f - f_stop) / 8)
            wren.ring_hard(P, 0, lift=1.0 - 0.3 * u)
        P.key(f)
    wren.grip(w, 1)
    wren.grip(w, 1, side="L")
    wren.ring(w, f_ring, f_stop, swing=40.0, beat=4)
    wren.face(w, "stern", 1)
    wren.face(w, "shout", f_ring)
    wren.talk_words(w, words_, t0, first=1, amount=1.0)
    wren.face(w, "stern", f_stop + 2)
    wren.blink(w, 1, n, every=(200, 201), at=(f_stop + 6,))
    wren.contact_shadows(w)
    if V is not None and huts:                                                # every porch bell joins in, one by one
        for i, h in enumerate(huts):
            if i != PORCH_HUT:
                V.ring_bell(h, f_ring + 6 + 5 * i, f_stop, seed=i)
    _offscreen_mark(Vector(kai_at) + Vector((0, 0, 3.0)), n)
    # low, in front of her and a little to the lane's north (her left): she fills the frame, the porch post and bell
    # and the lane's other porches beyond; a slow push-in
    side = Vector((-face.y, face.x, 0))
    tgt = spot + Vector((0, 0, 6.6)) - side * 1.3                              # toward her bell hand (her right)
    cdir = (face * 0.9 + side * 0.44).normalized()                           # her bell side: her face stays clear
    cyaw = math.degrees(math.atan2(-cdir.x, -cdir.y))
    _cam("S08cam", n, (tgt, 12.0, -7, cyaw, 46, 0.0), (tgt, 10.8, -7, cyaw, 46, 0.0))
    _clear_near(bpy.context.scene.camera, 9.0)
    return dict(frames=n, step=2, ones=(1, n), subject=[w["arm"]])


SHOTS = {"S08": s08, "S16": s16, "S17": s17}
