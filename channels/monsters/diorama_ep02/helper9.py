"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md), helper 9: the wrist mark, the sky crack, the lake.

    S14 "Something on my wrist started to glow." Over his left shoulder, looking down at his hands: the shrimp sits on
        his gloved fists, his bare left forearm below it. On "wrist" a thin coral zigzag flickers on along the inside of
        the forearm, just above the bracelet (the same zigzag as the sky crack); on "glow" it is lit: a white-hot core,
        a soft coral glow that also lights his arm and the shrimp (a real coral point light), and sparkles. The shrimp
        leans in to look at it; his hands give a small startled twitch. Slow push-in on 1s; characters on 2s.
    S15 "The same shape as the crack in the sky." An insert on the glowing mark, rolled so it stands upright, pushing
        in; a match cut just before "the crack" to the sky north of the pond, the rift in the same screen spot at the
        same size (the Ep 1 crack, helper 3's 2D look, opened); then a tilt up as the treetops fall away.
    S19 "The lake. Deep water. Where a pistol shrimp never runs dry." A crane out from behind Kai's head (Wren in
        front of him) up into a high tilt-shift view south over the island: the forest ring, the meadow, a small
        village of round huts with a bell tower on the island's south shore, and past it a huge deep-blue lake to the
        horizon. Just before "Where", a cut to the shrimp's claw in his hands, dripping (drops on 1s, glints in 2D).

Geography (new, used by nobody else yet): the island's south shore runs east-west at y ~ SHORE_Y, south of the
flower meadow; the village sits on it (VILLAGE), the lake fills everything south of it to the horizon. The sky crack
hangs due north, RIFT_EL degrees up (higher than Ep 1's 36 deg so it clears the clearing's north treetops).

The 2D passes (the mark, the rift, sparkles, glints) are drawn by diorama_ep02/post_helper9.py over the Blender frames
from build/monsters/diorama_ep02/<SHOT>_anchors.json, which these builders write.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S14 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector

from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import anim, diorama, look, puffshrimp, wren

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep02", "timing.json")
SHRIMP_K = 0.42                      # the puff-shrimp sitting on his fists
MARK_U = 0.6                         # the mark's centre: this far from his left elbow to his wrist (above the bracelet)
MARK_H = 0.45                        # the mark's length along the forearm (world units; the crack's 1-unit height)
CORAL = (1.0, 0.48, 0.36)
RIFT_EL = 58.0                       # the sky crack: due north, this many degrees up
RIFT_ANG = 0.144 * 2.0               # its angular height (helper 3's RIFT_H x POV_SIZE: the opened rift)
MATCH_Y, MATCH_PX = 430.0, 420.0     # S15's match cut: the mark / the crack centred at y 430 on 720x1280, 420 px tall
EYE = 8.2                            # Kai's eye height
VILLAGE = Vector((6.0, -170.0, 0.0))
SHORE_Y = -190.0
BLUR = 6.0
LAST = {}


def _timing():
    with open(TIMING) as f:
        return json.load(f)


def frames(shot):
    return next(s for s in _timing()["shots"] if s["shot"] == shot)["render_frames"]


def words(shot):
    """[(word, first frame)] of the shot's line, frame 1 = the shot's first frame."""
    t = _timing()
    s = next(x for x in t["shots"] if x["shot"] == shot)
    out = []
    for ln in t["lines"]:
        if ln.get("scene") == shot or ln.get("shot") == shot:
            out += [(w["w"].strip(".,!?:").lower(), round((w["start"] - s["start"]) * 24) + 1) for w in ln["words"]]
    return out


def at(shot, word, k=0):
    return [f for w, f in words(shot) if w == word][k]


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _az(front, left):
    """diorama.camera yaw for a camera placed `front` x his facing + `left` x his left (from Kai at X.KAI_AT)."""
    f = X._d
    d = (f * front + Vector((-f.y, f.x, 0)) * left).normalized()
    return math.degrees(math.atan2(-d.x, -d.y))


def _forearm(k, u, side="L"):
    """A point u of the way from his elbow (the forearm bone's head) to his wrist (the hand bone's head), in world
    space at the current frame: the forearm bone's own tail stops short of the wrist on this skeleton."""
    M = k["arm"].matrix_world
    return M @ k["bone"](f"forearm.{side}").head.lerp(k["bone"](f"hand.{side}").head, u)


# ------------------------------------------------------------------------------------------------------------ camera
def _new_cam(name, frame=1):
    sc = bpy.context.scene
    c = bpy.data.objects.new(name, bpy.data.cameras.new(name))
    sc.collection.objects.link(c)
    c.data.sensor_fit = "AUTO"
    c.data.clip_start, c.data.clip_end = 0.05, 6000
    c.data.dof.use_dof = True
    c.rotation_mode = "QUATERNION"
    mk = sc.timeline_markers.new(name, frame=frame)
    mk.camera = c
    if frame <= 1 or sc.camera is None:
        sc.camera = c
    return c


def _look(fwd, up=Vector((0, 0, 1))):
    """The camera rotation looking along `fwd` with `up` as the screen's up (as near as it can be)."""
    f = fwd.normalized()
    r = f.cross(up)
    if r.length < 1e-6:
        r = f.cross(Vector((0, 1, 0)))
    r.normalize()
    u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()


def _key_cam(cam, f, loc, rot, lens, focus, shift_y=0.0, blur=BLUR, haze=(0.97, 0.55)):
    """Place and key a camera at frame f (on 1s): pose, lens, shift, the tilt-shift focus and the haze band."""
    sc = bpy.context.scene
    cam.location = loc
    cam.rotation_quaternion = rot
    cam.data.lens = lens
    cam.data.shift_y = shift_y
    cam.data.dof.focus_distance = focus
    cam.data.dof.aperture_fstop = diorama.fstop_for(focus, lens, blur)
    ms = sc.world.mist_settings
    ms.start, ms.depth = focus * haze[0], focus * haze[1]
    for o, p in ((cam, "location"), (cam, "rotation_quaternion"), (cam.data, "lens"), (cam.data, "shift_y"),
                 (cam.data.dof, "focus_distance"), (cam.data.dof, "aperture_fstop"), (ms, "start"), (ms, "depth")):
        o.keyframe_insert(p, frame=f)


def _orbit(target, dist, tilt, yaw):
    """diorama.camera's placement: `dist` from `target`, `tilt` deg above the ground plane, `yaw` deg round Z."""
    el, az = math.radians(tilt), math.radians(yaw)
    loc = Vector(target) + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    return loc, _look(Vector(target) - loc)


def _linear(*ids):
    for idb in ids:
        ad = getattr(idb, "animation_data", None)
        if ad and ad.action:
            for fc in anim.all_fcurves(ad.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"


def _active_cam(f):
    sc = bpy.context.scene
    cam = sc.camera
    for m in sorted(sc.timeline_markers, key=lambda m: m.frame):
        if m.camera and m.frame <= f:
            cam = m.camera
    return cam


def _px(cam, p):
    from bpy_extras.object_utils import world_to_camera_view
    v = world_to_camera_view(bpy.context.scene, cam, p)
    return [round(v.x * 720, 2), round((1 - v.y) * 1280, 2), round(v.z, 3)]


def _anchors(shot, fn, meta=None):
    """Write {"meta": meta, "frames": {frame: fn(frame, active camera)}} for the 2D pass
    (build/monsters/diorama_ep02/<shot>_anchors.json). Skipped for check stills (--still) to keep them quick."""
    if "--still" in sys.argv or os.environ.get("H9_NO_ANCHORS"):
        return {}
    sc = bpy.context.scene
    out = {}
    for f in range(sc.frame_start, sc.frame_end + 1):
        sc.frame_set(f)
        out[f] = fn(f, _active_cam(f))
    sc.frame_set(1)
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(dict(meta=meta or {}, frames=out), fh)
    return out


def _mark_geo(k, cam):
    """The mark on screen this frame (720x1280): its centre c, and ex / ey = px per crack-height unit across the arm
    and along it (toward the wrist), the zigzag drawn as if lying on the arm's camera-facing side."""
    m = _forearm(k, MARK_U)
    a = (_forearm(k, 1.0) - _forearm(k, 0.0)).normalized()
    v = (m - cam.matrix_world.translation).normalized()
    x = a.cross(v).normalized()
    p0 = _px(cam, m)
    pa = _px(cam, m + a * MARK_H * 0.05)
    pxx = _px(cam, m + x * MARK_H * 0.05)
    return dict(c=p0[:2], z=p0[2], ey=[round((pa[0] - p0[0]) / 0.05, 2), round((pa[1] - p0[1]) / 0.05, 2)],
                ex=[round((pxx[0] - p0[0]) / 0.05, 2), round((pxx[1] - p0[1]) / 0.05, 2)])


def _rift_dir():
    e = math.radians(RIFT_EL)
    return Vector((0, math.cos(e), math.sin(e))), Vector((0, -math.sin(e), math.cos(e)))   # forward, the crack's up


def _rift_geo(cam):
    """The sky crack on screen (helper3_fx's rift dict: c, ex, ey in px per crack-height unit), or None if it's
    behind the camera."""
    fwd, upv = _rift_dir()
    rt = Vector((1, 0, 0))
    o = cam.matrix_world.translation

    def px(x, y):
        d = (fwd + rt * x * RIFT_ANG + upv * y * RIFT_ANG).normalized()
        p = _px(cam, o + d * 4000)
        return None if p[2] <= 0 else p
    p0, pxx, pyy = px(0, 0), px(0.05, 0), px(0, 0.05)
    if p0 is None or pxx is None or pyy is None:
        return None
    return dict(c=p0[:2], ex=[round((pxx[0] - p0[0]) / 0.05, 2), round((pxx[1] - p0[1]) / 0.05, 2)],
                ey=[round((pyy[0] - p0[0]) / 0.05, 2), round((pyy[1] - p0[1]) / 0.05, 2)])


# ------------------------------------------------------------------------------------------------------- characters
def _kai_cupping(n, twitch=None, head=14.0, head_at=None):
    """Kai at X.KAI_AT, the shrimp on his fists (X._cup), breathing; `twitch` = a frame where his hands give a small
    startled jerk (anticipation down, up, overshoot, settle); `head` = his nod (deg, + looks down), `head_at` =
    [(frame, nod)] changes. On 2s."""
    k = X._kai()
    P = x3.Pose(k)
    nods = sorted([(1, head)] + list(head_at or []))
    for f in range(1, n + 1, 2):
        P.reset()
        X._cup(P)
        P.rot("chest", (2 * math.sin(f / 18.0), 0, 0))
        nod = [v for g, v in nods if g <= f][-1]
        P.rot("head 1", (nod, 0, 0))
        if twitch is not None and -2 <= f - twitch <= 5:
            d = f - twitch
            lift = {-2: -2.5, 0: 6.0, 2: 3.5, 4: 1.0}[d - d % 2]
            for side in ("L", "R"):
                P.rot(f"upper_arm.{side}", (lift, 0, 0))
        P.key(f)
    return k


def _shrimp_in_hands(k, name="ep02_shrimp"):
    """The puff-shrimp sitting on his fists, facing out (his front)."""
    sc = bpy.context.scene
    sc.frame_set(1)
    bpy.context.view_layer.update()
    hl = k["arm"].matrix_world @ k["bone"]("hand.L").head.lerp(k["bone"]("hand.L").tail, 0.5)
    hr = k["arm"].matrix_world @ k["bone"]("hand.R").head.lerp(k["bone"]("hand.R").tail, 0.5)
    seat = (hl + hr) / 2 + Vector((0, 0, 0.14))
    rig = puffshrimp.build((0, 0, 0), name=name)
    rig["root"].location = seat
    rig["root"].scale = (SHRIMP_K,) * 3
    rig["root"].rotation_euler = (0, 0, math.radians(X.KAI_YAW))
    for e in rig["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
    rig["name"] = name
    return rig, seat


def _shrimp_parts(rig):
    return [rig["root"], rig["body"], rig["shoulder"], rig["hinge"]] + rig["eyes"] + rig["antennae"]


def _claw_tip(rig):
    """The snapping finger's lowest point now (where the drops fall from), in world space."""
    fin = bpy.data.objects.get(f"{rig['name']}_dactyl")
    bpy.context.view_layer.update()
    vs = [fin.matrix_world @ v.co for v in fin.data.vertices]
    return min(vs, key=lambda v: v.z)


def _mark_light(k, f_on, f_full, n, toward, seed=3):
    """A small coral point light at the mark (it lights his arm and the shrimp): off, a flicker on 2s from f_on, full
    from f_full (with a small overshoot), then a slow pulse."""
    bpy.context.scene.frame_set(1)
    m = _forearm(k, MARK_U)
    d = bpy.data.lights.new("h9_mark_light", "POINT")
    d.color = CORAL
    d.shadow_soft_size = 0.15
    lt = bpy.data.objects.new("h9_mark_light", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.location = m + (Vector(toward) - m).normalized() * 0.45     # just off the skin, on the camera's side
    rnd = random.Random(seed)
    full = 60.0
    for f in range(1, n + 1):
        if f < f_on:
            e = 0.0
        elif f < f_full:
            u = (f - f_on) / max(1, f_full - f_on)
            e = full * 0.35 * u * (0.4 + 0.6 * rnd.random()) if (f // 2) % 3 else 0.0
        else:
            e = full * (1.25 - 0.25 * _smooth((f - f_full) / 6)) * (0.92 + 0.08 * math.sin((f - f_full) / 5.0))
        d.energy = e
        d.keyframe_insert("energy", frame=f)
    return lt


def _tree(o):
    return [o] + [c for ch in o.children for c in _tree(ch)]


def _hide_from(f, objs):
    for o in objs:
        for g, hide in ((1, False), (f, True)):
            o.hide_render = hide
            o.keyframe_insert("hide_render", frame=g)
        if o.animation_data and o.animation_data.action:
            for fc in anim.all_fcurves(o.animation_data.action):
                if fc.data_path == "hide_render":
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"


# ------------------------------------------------------------------------------------------------------------ S14
def _s14_cam(mark, seat):
    return mark.lerp(seat, 0.45), _az(-0.3, 0.9)          # over his left shoulder, looking down at his hands


def s14():
    n = frames("S14")
    X._world(n)
    f_wrist, f_glow = at("S14", "wrist"), at("S14", "glow")
    k = _kai_cupping(n, twitch=f_glow - 2, head=14.0, head_at=[(f_wrist + 2, 20.0)])   # he looks down at his wrist
    sh, seat = _shrimp_in_hands(k)
    body = sh["body"]
    for f, lean in ((1, 0.0), (f_wrist + 6, 0.0), (f_wrist + 10, 0.32), (f_glow, 0.32), (f_glow + 2, 0.12),
                    (f_glow + 6, 0.28)):
        anim.key(body, "rotation_euler", f, (lean, 0, 0))                # it leans over to look down at the mark
    anim.squash(body, f_glow, -0.06)                                     # startled by the glow
    anim.squash(body, f_glow + 3, 0.05)
    anim.squash(body, f_glow + 7, 0.0)
    anim.blink(sh, f_glow + 10)
    anim.on_twos(_shrimp_parts(sh), step=2)
    bpy.context.scene.frame_set(1)
    mark = _forearm(k, MARK_U)
    tgt, yaw = _s14_cam(mark, seat)
    _mark_light(k, f_wrist, f_glow, n, _orbit(tgt, 5.0, 55.0, yaw)[0])
    cam = _new_cam("S14cam")
    for f in range(1, n + 1):                                           # a slow push-in on 1s
        loc, rot = _orbit(tgt, 5.4 - 0.8 * _smooth((f - 1) / (n - 1)), 55.0, yaw)
        _key_cam(cam, f, loc, rot, 50.0, (tgt - loc).length, blur=4.0, haze=(3.0, 3.0))
    _linear(cam, cam.data, bpy.context.scene.world)
    X.v2._twos([k["arm"]])
    LAST.update(k=k, sh=sh, mark=mark, seat=seat)
    _anchors("S14", lambda f, c: dict(mark=_mark_geo(k, c)), meta=dict(f_wrist=f_wrist, f_glow=f_glow))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------------------ S15
def s15():
    n = frames("S15")
    X._world(n)
    fc = at("S15", "crack") - 4                                          # the cut: just before "the crack"
    k = _kai_cupping(n, head=20.0)
    sh, seat = _shrimp_in_hands(k)
    anim.key(sh["body"], "rotation_euler", 1, (0.28, 0, 0))              # still leaning over the mark
    anim.blink(sh, 14)
    anim.on_twos(_shrimp_parts(sh), step=2)
    sc = bpy.context.scene
    sc.frame_set(1)
    m = _forearm(k, MARK_U)
    _mark_light(k, -10, -2, n, _orbit(m, 5.0, 55.0, _s14_cam(m, seat)[1])[0])
    a = (_forearm(k, 1.0) - _forearm(k, 0.0)).normalized()               # elbow -> wrist: the crack's "up"
    tgt, yaw = _s14_cam(m, seat)
    view_from, _ = _orbit(m, 1.0, 55.0, yaw)
    nrm = view_from - m
    nrm = (nrm - a * nrm.dot(a)).normalized()                            # face the arm square-on from S14's side
    f_mm = 50.0
    d1 = MARK_H * (f_mm / 36.0 * 1280) / MATCH_PX                        # at the cut: the mark is MATCH_PX tall
    shift = (640 - MATCH_Y) / 1280                                       # its centre above the frame's centre
    ins = _new_cam("S15ins", 1)
    for f in range(1, fc):
        d = d1 * (1.18 - 0.18 * _smooth((f - 1) / max(1, fc - 2)))       # pushing in on the mark
        _key_cam(ins, f, m + nrm * d, _look(-nrm, a), f_mm, d, shift_y=shift, blur=6.0, haze=(3.0, 3.0))
    # the sky: from his eyes, the rift dead ahead at the cut (same spot, same size), then a tilt up
    sky = _new_cam("S15sky", fc)
    eye = X.KAI_AT + Vector((0, 0, EYE))
    fwd, _ = _rift_dir()
    lens = MATCH_PX / RIFT_ANG * 36.0 / 1280                             # the rift MATCH_PX tall at the cut
    for f in range(fc, n + 1):
        u = _smooth((f - fc - 4) / max(1, n - fc - 10))
        q = Quaternion(Vector((1, 0, 0)), math.radians(9.0) * u)         # pitch up about the east axis
        _key_cam(sky, f, eye, _look(q @ fwd), lens * (1 + 0.06 * u), 400.0, shift_y=shift, blur=2.0,
                 haze=(0.5, 1.5))
    _linear(ins, ins.data, sky, sky.data, sc.world)
    _hide_from(fc, list(k["arm"].users_collection[0].objects) + _tree(sh["root"]))   # the sky camera is at his eyes
    X.v2._twos([k["arm"]])
    LAST.update(k=k, sh=sh, mark=m, seat=seat, fc=fc)
    _anchors("S15", lambda f, c: dict(mark=_mark_geo(k, c)) if f < fc else dict(rift=_rift_geo(c)), meta=dict(fc=fc))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]])


# ------------------------------------------------------------------------------------------------- village and lake
def _shore(x):
    return SHORE_Y + 7.0 * math.sin(x / 23.0) + 4.0 * math.sin(x / 9.1 + 1.3)


def _mesh(name, bm, mat, line=0.0):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat)
    if line:
        look.outline(o, line)
    return o


def _cone(bm, loc, r1, r2, h, seg=14):
    m = Matrix.Translation(Vector(loc) + Vector((0, 0, h / 2)))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=h, matrix=m)


def _box(bm, loc, size):
    m = Matrix.Translation(Vector(loc)) @ Matrix.Diagonal((*size, 1.0))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)


def _strip_shore(name, y_off, width, z, mat, x0=-1500, x1=1500, step=6.0):
    bm = bmesh.new()
    xs = [x0 + i * step for i in range(int((x1 - x0) / step) + 1)]
    top = [bm.verts.new((x, _shore(x) + y_off, z)) for x in xs]
    bot = [bm.verts.new((x, _shore(x) + y_off - width, z)) for x in xs]
    for i in range(len(xs) - 1):
        bm.faces.new((bot[i], bot[i + 1], top[i + 1], top[i]))
    return _mesh(name, bm, mat)


def village_and_lake():
    """The island's south shore (y ~ SHORE_Y): a small bell-keepers' village (round cream huts with rust and brown
    roofs, a bell tower with a brass bell, a jetty, two boats, a dirt square and a track up to the meadow) and the
    lake: deep blue to the horizon, a light shallow band and a foam line at the shore, a sandy beach, low far hills on
    the far side. Toon materials with outlines, like the rest of the island."""
    hx = look.hexc
    deep = look.toon("h9_lake_deep", hx("#1f4fae"), shade=0.85, rim=0.15)
    shallow = look.toon("h9_lake_shallow", hx("#4fa6e3"), shade=0.85, rim=0.1)
    foam = look.flat("h9_lake_foam", hx("#eef8ff"))
    sand = look.toon("h9_sand", hx("#e8d6a8"))
    wall = look.toon("h9_hut_wall", hx("#efe0bf"))
    roofs = [look.toon("h9_roof_rust", hx("#b4462e")), look.toon("h9_roof_brown", hx("#8a5634"))]
    wood = look.toon("h9_wood", hx("#7a4e2c"))
    brass = look.toon("h9_brass", hx("#d6a23c"), gloss=True)
    dirt = look.toon("h9_dirt", hx("#c9a873"))
    hills = look.toon("h9_far_hills", hx("#3f6f5a"), shade=0.9, rim=0.0)
    # the lake: one big sheet south of the shore, the shallow band and foam over it, a sandy beach strip above it
    bm = bmesh.new()
    xs = [-1500 + i * 6.0 for i in range(501)]
    top = [bm.verts.new((x, _shore(x) - 4.0, 0.06)) for x in xs]
    bot = [bm.verts.new((x, -1500.0, 0.06)) for x in xs]
    for i in range(len(xs) - 1):
        bm.faces.new((bot[i], bot[i + 1], top[i + 1], top[i]))
    out = dict(lake=_mesh("h9_lake", bm, deep))
    out["shallow"] = _strip_shore("h9_lake_shallow", -1.5, 16.0, 0.09, shallow)
    out["foam"] = _strip_shore("h9_lake_foam", 0.0, 1.6, 0.12, foam)
    out["beach"] = _strip_shore("h9_beach", 7.0, 7.2, 0.05, sand)
    # far hills on the far shore (they melt into the haze)
    bm = bmesh.new()
    rnd = random.Random(19)
    for i in range(26):
        x = -1400 + i * 112 + rnd.uniform(-30, 30)
        r = rnd.uniform(70, 150)
        m = Matrix.Translation((x, -1380 + rnd.uniform(-40, 40), 0)) @ \
            Matrix.Diagonal((r, r * 0.6, rnd.uniform(28, 60), 1.0))
        bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=8, radius=1.0, matrix=m)
    out["hills"] = _mesh("h9_far_hills", bm, hills)
    # the village: huts in a loose ring round a dirt square, the bell tower on the shore side
    sq = bmesh.new()
    bmesh.ops.create_circle(sq, cap_ends=True, segments=24, radius=17.0,
                            matrix=Matrix.Translation(VILLAGE + Vector((0, 0, 0.04))))
    out["square"] = _mesh("h9_square", sq, dirt)
    walls, rf = bmesh.new(), [bmesh.new(), bmesh.new()]
    rnd = random.Random(7)
    spots = []
    for i in range(11):
        a = -0.4 + i * (2 * math.pi - 0.8) / 10 + rnd.uniform(-0.12, 0.12)
        d = rnd.uniform(22, 30)
        x, y = VILLAGE.x + math.cos(a) * d * 1.25, VILLAGE.y + math.sin(a) * d * 0.7
        if y < _shore(x) + 9:
            continue
        spots.append((x, y))
    for i, (x, y) in enumerate(spots):
        r = rnd.uniform(3.6, 5.0)
        h = rnd.uniform(5.0, 6.5)
        _cone(walls, (x, y, 0), r, r, h)
        _cone(rf[i % 2], (x, y, h), r * 1.35, 0.15, r * 1.25)
    out["walls"] = _mesh("h9_hut_walls", walls, wall, 0.06)
    out["roofs"] = [_mesh(f"h9_roofs{j}", b, roofs[j], 0.06) for j, b in enumerate(rf)]
    # the bell tower: four posts, a deck, a peaked roof and the brass bell, by the shore
    tw, tb = bmesh.new(), bmesh.new()
    t0 = Vector((VILLAGE.x + 14.0, _shore(VILLAGE.x + 14.0) + 12.0, 0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            _box(tw, t0 + Vector((sx * 2.2, sy * 2.2, 9.0)), (0.7, 0.7, 18.0))
    _box(tw, t0 + Vector((0, 0, 18.3)), (6.2, 6.2, 0.6))
    _cone(tw, t0 + Vector((0, 0, 18.6)), 4.8, 0.1, 5.5, seg=4)
    out["tower"] = _mesh("h9_tower", tw, wood, 0.05)
    bmesh.ops.create_uvsphere(tb, u_segments=12, v_segments=8, radius=1.5,
                              matrix=Matrix.Translation(t0 + Vector((0, 0, 15.8))))
    out["bell"] = _mesh("h9_bell", tb, brass, 0.04)
    # the jetty and two boats
    jx = VILLAGE.x - 12.0
    jb = bmesh.new()
    _box(jb, (jx, _shore(jx) - 12.0, 0.9), (3.2, 26.0, 0.6))
    for j in range(5):
        for sx in (-1, 1):
            _box(jb, (jx + sx * 1.4, _shore(jx) - 2.0 - j * 5.0, 0.3), (0.5, 0.5, 2.0))
    for bx, by, yaw in ((jx + 6.0, _shore(jx) - 18.0, 0.3), (jx + 24.0, _shore(jx + 24) - 30.0, -0.5)):
        m = Matrix.Translation((bx, by, 0.45)) @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Diagonal((1.4, 4.2, 0.55, 1.0))
        bmesh.ops.create_uvsphere(jb, u_segments=12, v_segments=6, radius=1.0, matrix=m)
    out["jetty"] = _mesh("h9_jetty", jb, wood, 0.04)
    # the dirt track from the meadow down to the square
    pb = bmesh.new()
    pts = [Vector((0, -118, 0.045)), Vector((3, -138, 0.045)), Vector((5, -152, 0.045)),
           VILLAGE + Vector((0, 14, 0.045))]
    prev = None
    for p0, p1 in zip(pts[:-1], pts[1:]):
        dv = p1 - p0
        nv = Vector((-dv.y, dv.x, 0)).normalized() * 2.4
        a, b = (pb.verts.new(p0 + nv), pb.verts.new(p0 - nv)) if prev is None else prev
        c, d = pb.verts.new(p1 - nv), pb.verts.new(p1 + nv)
        pb.faces.new((a, b, c, d))
        prev = (d, c)
    out["track"] = _mesh("h9_track", pb, dirt)
    return out


def _wren_facing_kai(n):
    """Wren where XprL's S17 stops her (X.WREN_STOP), facing Kai: arms down, the bell held low, stern, blinking."""
    w = X._wren(X.WREN_STOP, X.WREN_YAW)
    P = x3.Pose(w)
    for f in range(1, n + 1, 2):
        P.reset()
        wren.hold_bell(P, 0.2)
        P.rot("chest", (1.5 * math.sin(f / 20.0), 0, 0))
        P.rot("head 1", (-8, 0, 0))
        P.key(f)
    wren.grip(w, 1)
    wren.face(w, "stern", 1)
    wren.blink(w, 1, n, at=(30,))
    return w


# ------------------------------------------------------------------------------------------------------------ S19
def s19():
    n = frames("S19")
    X._world(n)
    sc = bpy.context.scene
    lake = village_and_lake()
    fc = at("S19", "where") - 3                                          # the cut to the claw
    f_dry = at("S19", "dry")
    k = _kai_cupping(n, head=-6.0)                                       # chin up: he looks past her, far off
    w = _wren_facing_kai(n)
    sh, seat = _shrimp_in_hands(k)
    shp, hinge, body = sh["shoulder"], sh["hinge"], sh["body"]
    anim.key(shp, "rotation_euler", 1, (1.25, 0, 0))                     # the claw hanging forward and down, wet
    anim.key(hinge, "rotation_euler", 1, (0.12, 0, 0))
    for f in range(1, n + 1, 24):                                        # breathing
        anim.squash(body, f, 0.0)
        anim.squash(body, f + 12, -0.03)
    anim.key(body, "rotation_euler", 1, (0, 0, 0))
    anim.key(body, "rotation_euler", fc + 16, (0, 0, 0))
    anim.key(body, "rotation_euler", fc + 22, (0, 0, math.radians(-14)))  # it turns its eyes toward the lake
    anim.blink(sh, fc + 34)
    for e in sh["eyes"]:                                                 # "never runs dry": its eyes go big
        anim.key(e, "scale", f_dry - 1, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", f_dry, (1.18, 1.18, 1.18), "CONSTANT")
    anim.on_twos(_shrimp_parts(sh), step=2)
    X.v2._twos([k["arm"], w["arm"]])
    sc.frame_set(fc)
    bpy.context.view_layer.update()
    tip = _claw_tip(sh)
    from channels.monsters.mk import meadow
    before = set(bpy.data.objects)
    meadow.drips(tip, fc - 10, n + 2, every=15, fall=2.4, seed=4)
    drops = sorted(set(bpy.data.objects) - before, key=lambda o: o.name)
    for i, o in enumerate(drops):
        o.name = f"h9_drop{i}"
    sc.frame_set(1)
    # part A: crane out from behind his head to the high view south over the island (log distance, eased)
    crane = _new_cam("S19crane", 1)
    head = X.KAI_AT + Vector((0, 0, EYE + 0.6))
    a = (head + X._d * 6.0, 9.0, 12.0, _az(-1.0, 0.0), 40.0)
    b = (VILLAGE + Vector((0, 20.0, 0)), 330.0, 33.0, 180.0, 34.0)
    f_end = max(30, fc - 6)
    for f in range(1, fc):
        u = _smooth((f - 1) / (f_end - 1))
        t = Vector(a[0]).lerp(Vector(b[0]), u)
        d = math.exp(math.log(a[1]) + (math.log(b[1]) - math.log(a[1])) * u)
        tl = a[2] + (b[2] - a[2]) * _smooth(min(1.0, u * 1.8))           # up over the trees before it pulls back
        yw = a[3] + ((b[3] - a[3] + 180) % 360 - 180) * u
        ln = a[4] + (b[4] - a[4]) * u
        drift = 1 - 0.03 * max(0.0, (f - f_end) / 10)                    # keeps drifting in after the crane lands
        loc, rot = _orbit(t, d * drift, tl, yw)
        _key_cam(crane, f, loc, rot, ln, d * drift, blur=BLUR + 6 * u, haze=(0.97 + 0.5 * u, 0.55 + 2.2 * u))
    # part B: the claw in his hands, dripping; a slow push-in
    close = _new_cam("S19claw", fc)
    yaw = _az(0.75, -0.65)                                               # from the claw's side (its right), in front
    aim = tip.lerp(seat, 0.35) + Vector((0, 0, 0.1))                    # the claw and its face, the drops below
    for f in range(fc, n + 1):
        u = _smooth((f - fc) / (n - fc))
        loc, rot = _orbit(aim, 3.4 - 0.45 * u, 8.0, yaw)
        _key_cam(close, f, loc, rot, 70.0, (aim - loc).length, blur=14.0, haze=(3.0, 3.0))
    _linear(crane, crane.data, close, close.data, sc.world)
    LAST.update(k=k, sh=sh, w=w, fc=fc, tip=tip, lake=lake)

    def geo(f, c):
        ds = [_px(c, o.matrix_world.translation) for o in drops if o.scale.x > 0.01] if f >= fc else []
        return dict(tip=_px(c, _claw_tip(sh)), drops=ds)
    _anchors("S19", geo, meta=dict(fc=fc, f_dry=f_dry))
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], w["arm"], sh["root"]])


def _test_cam(name, front, left, tilt, dist, lens):
    def make():
        c = diorama.camera(name, LAST["mark"], dist=dist, tilt=tilt, yaw=_az(front, left), lens=lens, blur=4.0)
        c.data.clip_start = 0.05
        return c
    return make


SHOTS = {"S14": s14, "S15": s15, "S19": s19}
