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
WREN_KNEEL = KAI_SIT + Vector((0.6, -3.1, 0.0))      # at his right side (the village side), facing him (north)
WREN_YAW3 = 180.0
WREN_S16 = KAI_SIT + Vector((0.8, -6.5, 0.0))        # S16: standing a few steps off on the village side, facing him


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


def _village_backdrop():
    """Helper 1's night lane when diorama_ep03/village.py lands; until then helper 9's Ep 2 village and lake."""
    V = _optional("village")
    if V is None:
        H9.village_and_lake()
    return V


def _mark_light(k, n, toward, energy=MARK_W, seed=5):
    """The coral point light at Kai's left wrist (the key light at night), a slow uneven pulse."""
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


def _offscreen_mark(pos, n, energy=MARK_W * 1.6):
    """Kai's mark lighting a shot he isn't in (S08, S16): a coral point light at his wrist's spot, pulsing."""
    d = bpy.data.lights.new("x3_mark_off", "POINT")
    d.color = CORAL
    d.shadow_soft_size = 0.3
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


def _cam(name, n, a, b):
    """A slow camera move on 1s (X._cam_move: target, dist, tilt, yaw, lens, shift_y)."""
    return X._cam_move(name, n, a, b)


# ------------------------------------------------------------------------------------------------------------ S16
def s16():
    n = frames("S16")
    _night(n)
    _village_backdrop()
    w = _wren_at(WREN_S16, WREN_YAW3)
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
    _offscreen_mark(KAI_SIT + Vector((1.2, 0.6, 2.6)), n)
    _dazed_moths(n, [(WREN_S16.x - 2.2, WREN_S16.y + 2.0), (WREN_S16.x + 2.6, WREN_S16.y + 1.2),
                     (WREN_S16.x + 0.8, WREN_S16.y + 3.4)])
    # close (chest-up), from Kai's side (north-west of her), a slow push-in
    tgt = WREN_S16 + Vector((-0.4, 0, 6.3))
    yaw = 176.0
    _cam("S16cam", n, (tgt, 9.2, 3, yaw, 44, 0.0), (tgt, 8.2, 3, yaw, 44, 0.0))
    return dict(frames=n, step=2, ones=(1, n), subject=[w["arm"]])


# ------------------------------------------------------------------------------------------------------------ S17
def s17():
    n = frames("S17")
    _night(n)
    _village_backdrop()
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
            P.rot("chest", (0, 0, -18 * g))
            P.rot("neck", (0, 0, -25 * g))
            P.rot("head 1", (0, 0, -30 * g))
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
    mid = KAI_SIT.lerp(WREN_KNEEL, 0.68) + Vector((0, 0, 4.2))
    yaw = 171.0
    _cam("S17cam", n, (mid, 14.5, 7, yaw, 40, 0.0), (mid, 13.0, 7, yaw, 40, 0.0))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"]])


SHOTS = {"S16": s16, "S17": s17}
