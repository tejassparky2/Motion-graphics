"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md), helper 4's shots:

    S05 "Now I was holding a wet pistol shrimp. In my bare hands."  Close on Kai's cupped hands: the puff-shrimp sits
        in them facing him, its wet claw resting against the heel of his left palm; drops bead on the claw, one swells
        at the tip and falls into his palm (on "wet pistol shrimp"). Cut up (f50, between the sentences) to his face:
        pinprick terror eyes, brows up, a tremble on 1s; the 2D sweat drop pops in on "In my" (post pass,
        diorama_ep02/post_helper4.py). Slow push-ins on 1s; the characters on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S05 OUT_DIR [--frames A-B] [--still N --scale 0.5]

Staging is XprL's (diorama_ep02/xprl.py): Kai at KAI_AT on the pond's east shore, facing WREN_FROM (south).
"""
import json
import math
import os

import bpy
from mathutils import Vector

from channels.monsters.diorama_ep02 import xprl as X
from channels.monsters.ep01v2 import bgqrs as s3d                 # kai_point, claw_tip, _drop, lock_on, _fix_pivots
from channels.monsters.ep01v2 import xprl as x3                   # Pose
from channels.monsters.mk import anim, hero, look, puffshrimp

SHRIMP_IN_HAND = float(os.environ.get("SHRIMP_IN_HAND", "0.6"))   # root scale of the shrimp in his hands (shared)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
FPS = 24


def _frames(shot, fallback):
    return X._frames(shot, fallback)


def _words(line_id):
    """{word: local frame (1-based) of its start} for a line, relative to its shot's first frame."""
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep02", "timing.json")) as f:
        d = json.load(f)
    ln = next(x for x in d["lines"] if x["id"] == line_id)
    s0 = next(s["start"] for s in d["shots"] if s["shot"] == ln["scene"])
    return [(w["w"], 1 + round((w["start"] - s0) * FPS), 1 + round((w["end"] - s0) * FPS)) for w in ln["words"]]


# ------------------------------------------------------------------------------------------------- Kai holding it
def _hold(P, breath=0.0, tremble=0.0):
    """Both hands cupped together in front of his chest, palms up, the shrimp sitting in them; elbows in, the
    shoulders a little up (holding his breath). `tremble` (-1..1) shifts the hands a touch on 1s."""
    P.rot("chest", (4 + 2 * breath, 0, 0))
    for side, s in (("L", 1), ("R", -1)):
        P.aim(f"upper_arm.{side}", (s * 0.18, -0.28, -1.0))
        P.aim(f"forearm.{side}", (-s * 0.32, -1.0, 0.18 + 0.02 * tremble))
        P.twist(f"forearm.{side}", -s * 80)
        P.aim(f"hand.{side}", (-s * 0.38, -1.0, 0.1))
    P.rot("head 1", (14, 0, 0))                                       # looking down at it


def _fingers(rig, curl, thumb=0.25):
    """Curl both hands' fingers (cupping) by `curl` radians per joint."""
    from mathutils import Matrix
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.rotation_mode = "QUATERNION"
            c = thumb if b.name.startswith("thumb") else curl
            b.rotation_quaternion = Matrix.Rotation(c, 4, "X").to_quaternion()


def _key_fingers(rig, f):
    for b in rig["arm"].pose.bones:
        if b.name.startswith(("f_", "thumb")) and not b.name.startswith("robo"):
            b.keyframe_insert("rotation_quaternion", frame=f)


def _palms(rig):
    """World point between his two palms (where the shrimp sits) and the up direction of the cup."""
    arm = rig["arm"]
    bpy.context.view_layer.update()
    pts = []
    for side in ("L", "R"):
        pb = rig["arm"].pose.bones[f"hand.{side}"]
        pts.append(arm.matrix_world @ ((pb.head + pb.tail) / 2))
    return (pts[0] + pts[1]) / 2


def _shrimp_in_hands(rig, yaw_deg):
    """The puff-shrimp sitting in his palms, facing his face (yaw_deg: its root's world z rotation), scaled
    SHRIMP_IN_HAND; its claw (on its right) laid down along his left palm, resting."""
    sh = puffshrimp.build((0, 0, 0))
    s3d._fix_pivots(sh)
    r = sh["root"]
    r.scale = (SHRIMP_IN_HAND,) * 3
    r.location = _palms(rig) + Vector((0, 0, 0.12))
    r.rotation_euler = (0, 0, math.radians(yaw_deg))
    bpy.context.view_layer.update()
    return sh


def _wet(sh, n, seed=3):
    """Beads of water on the claw and the collar (small glossy drops, outlined), so it reads WET at a glance."""
    import random
    rnd = random.Random(seed)
    mat = look.toon("s05_bead", look.hexc("#bfe8ff"), shade=0.7, gloss=True)
    out = []
    claw = bpy.data.objects["puff_claw"]
    vs = claw.data.vertices
    picks = rnd.sample(range(len(vs)), 9)
    for i, vi in enumerate(picks):
        co = vs[vi].co + vs[vi].normal * 0.06
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.07 + 0.03 * rnd.random(),
                                             location=claw.matrix_world @ co)
        b = bpy.context.object
        b.name = f"puff_bead{i}"
        b.data.materials.append(mat)
        look.outline(b, 0.006)
        b.visible_shadow = False
        mw = b.matrix_world.copy()
        b.parent = claw
        b.matrix_parent_inverse = claw.matrix_world.inverted()
        b.matrix_world = mw
        out.append(b)
    return out


# ------------------------------------------------------------------------------------------------- the cameras
def _shot_cam(name, frame, target, dist, tilt, yaw, lens, blur, push=0.06, f1=None, shift_y=0.0):
    """A diorama camera bound at `frame` (timeline marker), pushing in `push` of its distance by f1 on 1s, its focus
    and haze following."""
    from channels.monsters.mk import diorama
    c = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=lens, blur=blur, frame=frame,
                       haze=(2.5, 2.0))
    c.data.shift_y = shift_y
    t = Vector(target)
    p0 = c.location.copy()
    sc = bpy.context.scene
    for f in range(frame, (f1 or frame) + 1):
        u = (f - frame) / max(1, (f1 or frame) - frame)
        e = u * u * (3 - 2 * u)
        c.location = p0.lerp(t, push * e)
        c.keyframe_insert("location", frame=f)
        c.data.dof.focus_distance = (c.location - t).length
        c.data.dof.keyframe_insert("focus_distance", frame=f)
    del sc
    return c


def _anchors(shot, n, rig, extra=None):
    """Screen points (720x1280, top-left origin) of Kai's eyes and temple per frame through each frame's marker
    camera, for the 2D pass: build/monsters/diorama_ep02/<SHOT>_anchors.json."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    marks = sorted(sc.timeline_markers, key=lambda m: m.frame)
    for f in range(1, n + 1):
        sc.frame_set(f)
        cam = [m.camera for m in marks if m.frame <= f][-1] if marks else sc.camera
        pts = {k: s3d.kai_point(rig, k) for k in ("eyes", "eye_l", "eye_r", "nose", "temple")}
        for k, fn in (extra or {}).items():
            pts[k] = fn()
        out[f] = {k: (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
                  for k, v in ((k, world_to_camera_view(sc, cam, p)) for k, p in pts.items())}
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


# ------------------------------------------------------------------------------------------------------------ S05
S05_CUT = 50                                    # the cut up to his face, between "...shrimp." and "In my bare hands."


def s05():
    n = _frames("S05", 99)
    W = _words("l5")
    f_wet = next(a for w, a, b in W if w == "wet")                  # 28
    f_in = next(a for w, a, b in W if w == "In")                    # 56
    X._world(n)
    k = X._kai()
    rig = k
    P = x3.Pose(k)
    # Kai: frozen, holding his breath; a tremble on 2s that gets worse after the cut
    for f in range(1, n + 1, 2):
        P.reset()
        tr = math.sin(f * 2.3) * (0.4 if f < S05_CUT else 1.0)
        _hold(P, breath=math.sin(f / 14.0), tremble=tr)
        if f >= S05_CUT:
            P.rot("head 1", (-12, 3 * tr, 0))                          # head comes up off the hands: the stare
        P.key(f)
    _fingers(k, 0.32)
    _key_fingers(k, 1)
    hero.face(k, "pinprick", 1)
    hero.face(k, "brows_up", 1, value=0.6)
    hero.face(k, "look_down", 1, value=0.7)
    for f in (S05_CUT - 1,):
        hero.face(k, "look_down", f, value=0.7)
    hero.face(k, "look_down", S05_CUT, value=0.0)
    hero.face(k, "shock", S05_CUT, value=1.0)
    hero.face(k, "pinprick", S05_CUT, value=1.0)
    hero.face(k, "brows_up", S05_CUT, value=1.0)
    hero.face(k, "grit", S05_CUT + 6, value=0.45)
    X.v2._twos([k["arm"]])

    # the shrimp in his hands, facing his face, its claw down along his left palm; eyes locked on his face
    bpy.context.scene.frame_set(1)
    sh = _shrimp_in_hands(k, X.KAI_YAW + 180)
    anim.key(sh["shoulder"], "rotation_euler", 1, (1.45, 0.0, 0.15), "CONSTANT")   # the claw laid down on his palm
    anim.key(sh["hinge"], "rotation_euler", 1, (0.12, 0.0, 0.0), "CONSTANT")
    for f in range(1, n + 1, 24):
        anim.squash(sh["body"], f, 0.0)
        anim.squash(sh["body"], f + 12, -0.03)
    anim.blink(sh, 70)
    s3d.lock_on(sh, s3d.kai_point(k, "eyes"), 1, lids=0.15, slant=0.1)
    X.v2._twos([sh["body"], sh["shoulder"], sh["hinge"]] + sh["eyes"])
    _wet(sh, n)
    tip = s3d.claw_tip(sh)
    land = _palms(k) + Vector((0.0, 0.0, 0.05))
    s3d._drop(tip - Vector((0, 0, 0.05)), f_wet - 10, f_wet + 4, f_wet + 9, land, r=0.11)

    # cameras: A low over the hands from his front-right, the shrimp side-on in his palms (1..CUT-1);
    # B up to his face, a touch low, his eyes above the caption band (CUT..n)
    hands = _palms(k) + Vector((0, 0, 0.55))
    face = s3d.kai_point(k, "eyes")
    _shot_cam("S05a", 1, tuple(hands), 6.5, 16.0, -X.KAI_YAW - 55.0, 60.0, 3.0, push=0.06, f1=S05_CUT - 1,
              shift_y=0.12)
    _shot_cam("S05b", S05_CUT, tuple(face - Vector((0, 0, 0.35))), 7.5, 4.0, -X.KAI_YAW + 8.0, 55.0, 2.5, push=0.08,
              f1=n, shift_y=0.1)
    _anchors("S05", n, k, extra={"tip": lambda: s3d.claw_tip(sh)})
    return dict(frames=n, step=1, subject=[k["arm"], sh["root"]] + list(k.get("cap", [])), cut=S05_CUT,
                beats=dict(wet=f_wet, sweat=f_in))


SHOTS = {"S05": s05}
