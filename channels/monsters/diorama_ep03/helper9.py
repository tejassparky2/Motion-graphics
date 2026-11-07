"""Helper 9's Episode 3 (DIORAMA_EP03.md): the shared night (mk/night.py) entry points, and the shots S04 (the sun
goes down), S05 (the dark island, one coral dot) and S18 (Wren whispers and points; the lighthouse).

For everyone's night shots:

    from channels.monsters.diorama_ep03 import helper9 as N9
    N9.night(n)                  # after X._world(n): the night grade (moon, sky, haze, the mark's warm light)
    N9.dusk(n)                   # the dusk version (S04's end state)
    lt = N9.mark(k)              # Kai's wrist mark: the coral key light, on his left forearm bone (follows every pose)
    lh = N9.lighthouse()         # the ruined lighthouse across the lake (once per scene)

night() can come before the characters are built: materials are tagged for the mark's light again when the render
starts.
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector

from channels.monsters.mk import night as NG

MARK_W = 6000.0                      # the mark light at night (no shadows; its light comes back through the grade)


def night(n=None, azim=None):
    """The night grade on the current scene (call after X._world / diorama.setup)."""
    return NG.apply("night", azim=azim)


def dusk(n=None, azim=None):
    return NG.apply("dusk", azim=azim)


def mark(k, energy=MARK_W, key=None, u=0.3):
    """Kai's mark as the coral key light: `key` = [(frame, energy)] for a flare or a dim."""
    return NG.mark_light(k, energy=energy, key=key, u=u)


def lighthouse(**kw):
    return NG.lighthouse(**kw)



# ======================================================================================================== the shots
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")


def _timing():
    with open(TIMING) as fh:
        return json.load(fh)


def frames(shot):
    return next(s for s in _timing()["shots"] if s["shot"] == shot)["render_frames"]


def words(shot):
    t = _timing()
    s = next(x for x in t["shots"] if x["shot"] == shot)
    return [(w["w"].strip(".,!?:").lower(), round((w["start"] - s["start"]) * 24) + 1)
            for ln in t["lines"] if ln.get("scene") == shot for w in ln["words"]]


def at(shot, word, k=0):
    return [f for w, f in words(shot) if w == word][k]


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _anchors(shot, fn, meta=None):
    """{"meta", "frames": {f: fn(f, camera)}} for the 2D pass (build/monsters/diorama_ep03/<shot>_anchors.json)."""
    if "--still" in sys.argv or os.environ.get("H9_NO_ANCHORS"):
        return {}
    from channels.monsters.diorama_ep02 import helper9 as H2
    sc = bpy.context.scene
    out = {}
    for f in range(1, frames(shot) + 1):
        sc.frame_set(f)
        out[f] = fn(f, H2._active_cam(f))
    sc.frame_set(1)
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(dict(meta=meta or {}, frames=out), fh)
    return out


def _disc(name, pos, r, col, strength, halo=3.0, halo_col=None, halo_s=1.4):
    """A glowing disc in the sky (a sphere far off) with a soft halo: the setting sun."""
    import bmesh
    out = []
    for nm, rad, mat in ((name, r, NG.look.flat(f"{name}_mat", col, strength=strength)),
                         (f"{name}_halo", r * halo, NG._halo_mat(f"{name}_halo", halo_col or col, halo_s))):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=rad)
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        for p_ in me.polygons:
            p_.use_smooth = True
        o = bpy.data.objects.new(nm, me)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(mat)
        o.location = pos
        o.visible_shadow = False
        out.append(o)
    return out


def _dir(az, el):
    a, e = math.radians(az), math.radians(el)
    return Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))


# ------------------------------------------------------------------------------------------------------------ S04
def s04():
    """"Then the sun went down." Kai alone in the lane (S03's end), side-on; behind him the sun sinks behind the
    western treeline, the sky goes from gold to orange to deep blue, the island darkens; on "down" he lifts his left
    wrist and the mark brightens into the only light."""
    from channels.monsters.diorama_ep02 import helper9 as H2
    from channels.monsters.diorama_ep02 import xprl as X
    from channels.monsters.diorama_ep03 import helper1 as E1
    from channels.monsters.diorama_ep03 import village as V
    from channels.monsters.ep01v2 import xprl as x3
    from channels.monsters.mk import anim, hero
    n = frames("S04")
    sc = bpy.context.scene
    E1._world(n)
    f_sun, f_down = at("S04", "sun"), at("S04", "down")
    f_dusk, f_night = f_down - 2, n - 6
    face = -V.LANE_DIR                                                     # as S03: facing up the lane
    k = E1._kai(V.LANE_AT, face)
    hero.line_width(k, 0.0028)
    P = x3.Pose(k)
    for f in range(1, n + 1, 2):                                           # slumped (S03's end), then the wrist up
        up = _smooth((f - f_down) / 12)
        E1._pose_kai(P, k, f, face, arm_up=0.75 * up, look=0.25 * up, slump=1.0 - 0.8 * up)
    X.v2._twos([k["arm"]])
    E1._kai_face({"face_sad": 0.6, "eye_brow_up": 0.9, "look_down": 0.4}, 1)
    E1._kai_face({"face_surprise": 0.3, "eye_brow_up": 0.7, "look_down": 0.6}, f_down + 6)   # it's getting brighter
    sh = E1._shoulder_shrimp(k, n, face, name="ep03_shrimp_h9")
    anim.key(sh["body"], "rotation_euler", 1, (0.25, 0, 0), "CONSTANT")
    anim.key(sh["body"], "rotation_euler", f_down + 4, (0.35, 0, 0.5), "CONSTANT")    # it turns to the glow
    anim.on_twos(H2._shrimp_parts(sh), step=2)
    # the sky: day (S03) -> dusk on "down" -> night by the end; the sun disc sinks behind the trees to the west
    NG.transition(1, f_dusk, "day", "dusk", "night", f_night, azim=-15.0)   # light from the sunset, behind him
    SUN_AZ = 172.0                                                         # over the far hills across the lake
    sd, halo = _disc("h9_setting_sun", _dir(SUN_AZ, 5.0) * 2400.0, 70.0, (1.0, 0.55, 0.22, 1), 3.0, halo=3.4,
                     halo_col=(1.0, 0.45, 0.18, 1), halo_s=1.6)
    for f in range(1, n + 1):
        el = 9.0 - 13.0 * _smooth((f - 1) / (f_down + 4 - 1))              # gone below the hills after "down"
        p = Vector(V.LANE_AT) + _dir(SUN_AZ, el) * 2400.0
        for o in (sd, halo):
            o.location = p
            o.keyframe_insert("location", frame=f)
    H2._hide_from(f_night, [sd, halo])
    # the mark: dim in daylight, brightening as the light goes (the key at night)
    mark(k, energy=MARK_W, key=[(1, 400.0), (f_down, 1200.0), (f_down + 10, 4200.0), (n, MARK_W)])
    # camera: low, from up the lane (north), looking south down it: Kai facing us, the square, the lake and the far
    # hills behind him with the sun sinking behind them; a slow push-in
    cam = H2._new_cam("S04cam", 1)
    tgt = Vector(V.LANE_AT) + Vector(V.LANE_DIR) * 8.0 + Vector((-0.6, 0, 6.6))
    for f in range(1, n + 1):
        u = _smooth((f - 1) / (n - 1))
        loc, rot = H2._orbit(tgt, 23.0 - 2.5 * u, 4.0, 170.0)             # from the north, on the lane's middle
        H2._key_cam(cam, f, loc, rot, 32.0, (Vector(V.LANE_AT) + Vector((0, 0, 5)) - loc).length,
                    shift_y=-0.06, blur=2.0, haze=(4.0, 10.0))
    H2._linear(cam, cam.data)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------------------ S05
S05_TINT = (0.11, 0.10, 0.27)        # darker than the shared night: the dark island, the one coral dot


def s05():
    """"And my wrist was the only light for miles." High and wide over the dark island and the lake at night; in the
    village, one tiny coral dot (Kai's mark). A slow push-in toward it. (No lighthouse here: the wrist is the only
    light; S18 reveals the lighthouse.)"""
    from channels.monsters.diorama_ep02 import helper9 as H2
    from channels.monsters.diorama_ep03 import helper1 as E1
    from channels.monsters.diorama_ep03 import village as V
    from channels.monsters.ep01v2 import xprl as x3
    from channels.monsters.mk import hero
    n = frames("S05")
    E1._world(n)
    face = -V.LANE_DIR
    k = E1._kai(V.LANE_AT, face)
    P = x3.Pose(k)
    for f in range(1, n + 1, 2):
        E1._pose_kai(P, k, f, face, arm_up=0.75, look=0.25, slump=0.2)
    night(n)
    NG.moon(az=150.0, el=30.0)                                             # behind the camera's view: its light only
    tint = bpy.context.scene.node_tree.nodes["h9n_tint"]
    tint.inputs[2].default_value = (*S05_TINT, 1)
    lt = mark(k, energy=MARK_W)
    cam = H2._new_cam("S05cam", 1)
    dot = Vector(V.LANE_AT) + Vector((0, 0, 5.5))
    tgt = Vector(V.VILLAGE) + Vector((0, 40, 0))
    for f in range(1, n + 1):
        u = _smooth((f - 1) / (n - 1))
        t = tgt.lerp(dot, 0.25 * u)
        loc, rot = H2._orbit(t, 470.0 - 90.0 * u, 36.0, 180.0)
        H2._key_cam(cam, f, loc, rot, 34.0, (t - loc).length, blur=6.0, haze=(1.4, 2.6))
    H2._linear(cam, cam.data)
    _anchors("S05", lambda f, c: dict(dot=H2._px(c, dot)), meta={})
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"]])


# ------------------------------------------------------------------------------------------------------------ S18
def s18():
    """"But the last marked one left something at the old lighthouse." XprL's S17 staging: Kai sitting in the grass
    (the shrimp on his shoulder), Wren kneeling at his side. She leans in and whispers (her hand cupped), then on
    "left" turns and points across the dark lake; on "at" a cut to the ruined lighthouse on its rocky point, its coral
    glow the only warm thing in the frame, its reflection on the water; the glow swells on "lighthouse"."""
    from channels.monsters.diorama_ep02 import helper9 as H2
    from channels.monsters.diorama_ep03 import xprl as XP
    from channels.monsters.ep01v2 import xprl as x3
    from channels.monsters.mk import hero, wren
    n = frames("S18")
    sc = bpy.context.scene
    XP._night(n)
    XP._village_backdrop(shut=1)
    lh = lighthouse()
    f_lean0, f_lean1 = 2, 12
    f_point0 = at("S18", "left") - 3
    f_point1 = f_point0 + 10
    f_cut = at("S18", "at") - 2
    f_lh = at("S18", "lighthouse")
    k = XP._kai_sitting(n, look_at=XP.WREN_KNEEL + Vector((0, 0, 5.0)))
    XP._shoulder_shrimp(k, n)
    hero.face(k, "worried", 1) if "worried" in hero.FACES else hero.face(k, "sad", 1)
    lt = mark(k, energy=MARK_W)
    w = XP._wren_at(XP.WREN_KNEEL, XP.WREN_YAW3)
    P = x3.Pose(w)
    M_inv = w["arm"].matrix_world.inverted().to_3x3()
    to_kai = (M_inv @ ((XP.KAI_SIT + Vector((0, 0, 7.0))) - (XP.WREN_KNEEL + Vector((0, 0, 6.0))))).normalized()
    to_lh = (M_inv @ (lh["top"] - (XP.WREN_KNEEL + Vector((0, 0, 6.0))))).normalized()
    words_, t0 = XP._line_words("S18")
    for f in range(1, n + 1, 2):
        P.reset()
        wren.kneel(P, front="L", depth=1.0)
        lean = _smooth((f - f_lean0) / (f_lean1 - f_lean0)) * (1 - _smooth((f - f_point0) / 6))
        pt = _smooth((f - f_point0) / (f_point1 - f_point0))
        if pt > 0.01:
            wren.point(P, to_lh, pt)
        if lean > 0.01:
            wren.whisper(P, lean, toward=to_kai)
        P.rot("chest", (0.8 * math.sin(f / 8.0), 0, 0))
        if f_point1 <= f < f_point1 + 6:                                       # a small overshoot on the point
            P.rot("chest", (0, 0, 3.0 * math.sin(math.pi * (f - f_point1) / 6)))
        P.key(f)
    wren.grip(w, 1)
    wren.face(w, "whisper", 1)
    wren.face(w, "worried", f_point0 + 2)
    wren.point_fingers(w, f_point0 + 4)
    wren.talk_words(w, words_, t0, first=1, amount=0.6)                     # a whisper: smaller mouth shapes
    wren.blink(w, 1, n, every=(200, 201), at=(f_point0 - 2,))
    wren.contact_shadows(w)
    hero.blink(k, 1, n) if hasattr(hero, "blink") else None
    # part A: a close two-shot from the east (Kai facing us, Wren side-on, leaning to him); a slow push-in
    camA = H2._new_cam("S18a", 1)
    mid = XP.KAI_SIT.lerp(XP.WREN_KNEEL, 0.45) + Vector((0, 0, 5.4))
    for f in range(1, f_cut):
        u = _smooth((f - 1) / (f_cut - 2))
        loc, rot = H2._orbit(mid, 9.6 - 1.0 * u, 8.0, 247.5)              # from the ENE: her point to the lighthouse
                                                                            # crosses the frame (screen left), clear of him
        H2._key_cam(camA, f, loc, rot, 30.0, (mid - loc).length, blur=3.0, haze=(4.0, 9.0))
    # part B: the lighthouse from the near shore, across the dark water: the reflection runs to us; a slow push-in
    camB = H2._new_cam("S18b", f_cut)
    eye0 = lh["top"] + Vector((-55, 250, -38))
    for f in range(f_cut, n + 1):
        u = _smooth((f - f_cut) / (n - f_cut))
        eye = eye0.lerp(lh["top"] + Vector((-46, 205, -36)), u)
        d = (lh["top"] - Vector((0, 0, 24))) - eye
        H2._key_cam(camB, f, eye, H2._look(d), 58.0, d.length, blur=1.0, haze=(1.5, 3.0))
    NG.reflection(lh["top"], eye0)
    NG.moon(az=161.5, el=14.5, r=30.0, origin=eye0)                        # up and left of the lamp, small
    hl = bpy.data.lights[f"h9_lighthouse_light"]                            # the glow swells on "lighthouse"
    gm = bpy.data.materials["h9_lighthouse_glow"].node_tree.nodes["Emission"].inputs[1]
    hm = [nd for nd in bpy.data.materials["h9_lighthouse_halo"].node_tree.nodes if nd.bl_idname == "ShaderNodeEmission"][0].inputs[1]
    for f, g in ((1, 0.8), (f_lh - 2, 0.8), (f_lh + 4, 1.5), (f_lh + 16, 1.1), (n, 1.15)):
        hl.energy = 26000.0 * 2.25 * g
        hl.keyframe_insert("energy", frame=f)
        gm.default_value = 6.5 * g
        gm.keyframe_insert("default_value", frame=f)
        hm.default_value = 2.4 * g
        hm.keyframe_insert("default_value", frame=f)
    H2._linear(camA, camA.data, camB, camB.data)
    _anchors("S18", lambda f, c: dict(lamp=H2._px(c, lh["top"])), meta=dict(f_cut=f_cut, f_lh=f_lh))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"]])


SHOTS = {"S04": s04, "S05": s05, "S18": s18}
