"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 5: S19, S20, S21, the chest scene's end, on
the "after" island where the blast threw Kai (the same set, Kai and shrimp as bGqrs's S16 in diorama/bgqrs.py).

Every story beat lands on the same frame as in the 3D shot (ep01v2/bgqrs.py s19-s21), because the SFX are synced to
them. The 3D shots' 2D effects (bgqrs_post) are 3D here: the "pff" of dust on the futile snap, the stomp puffs, the
ripple when the claw dips. Characters on 2s; the cameras are locked, so only even frames render (step 2).

    S19 "So I didn't move. I let the sun dry it." (105 render frames): near top-down on his set face and the claw
        over it; the last drop on the claw tip shrinks away (gone by f90). The shrimp blinks at f36, he blinks at f60.
    S20 "It tried anyway." (103): over the shrimp on his chest. Wind-up f20, the snap at his nose f24, only a tiny
        "pff" of dust; it turns to stare at its claw and tilts its head (f34-40). Cut at f44 to his deadpan face, held.
    S21 "Then it stomped back to the puddle." (64): a higher diorama view, Kai lying in the foreground, the pond above
        him. The shrimp turns its back in a huff (f4-8), stomps off in three hops (landings f14, f22, f30, a dust puff
        on each) to the pond's edge and dips its claw in the water at f42 (a ripple: the "plip").

    blender -b -y -P channels/monsters/render_shot.py -- diorama S19 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import bgqrs as d16                 # the island, Kai on his back, the shrimp
from channels.monsters.ep01v2 import bgqrs as s3d                  # Kai's face keys, the claw poses, the drop
from channels.monsters.mk import anim, diorama, look

FRAMES = {"S19": 105, "S20": 103, "S21": 64}                       # = ep01v2/bgqrs.py FRAMES (cut + 12-frame handle)
TILT, BLUR = 78.0, 12.0
LAST = {}                                                          # the last built rig and shrimp (for framing checks)


def _base(n, breathe=True):
    """bGqrs's "after" world (diorama/bgqrs.py _world): the island with the smoking stumps, Kai on his back at
    MAP["kai_down"], the shrimp on his chest with its claw cocked beside his face, the shared sunbeam on him (S15-S21)
    and the settling dust (on 2s here, like the characters, since these locked shots render on 2s). breathe=False
    drops the shrimp's idle breathing, for shots that key its body themselves."""
    diorama.setup()
    d16._set(n)
    rig = d16._kai()
    sh = d16._shrimp(rig, n)
    if not breathe:
        for fc in anim.all_fcurves(sh["body"].animation_data.action):
            if fc.data_path == "scale":
                fc.keyframe_points.clear()
        anim.squash(sh["body"], 1, 0.0)
    diorama.sunbeam(s3d.kai_point(rig, "chest"), radius=7.0)
    d16._dust(rig, n)
    anim.on_twos([o for o in bpy.data.objects if o.name.startswith("d16_dust")], step=2)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    LAST.update(rig=rig, sh=sh)
    return rig, sh


def _axes():
    """Kai's frame on the ground: `up` toward his head (and the pond), `east` the shrimp's right as it faces him."""
    up = Vector((-math.sin(math.radians(d16.HEAD_DIR)), math.cos(math.radians(d16.HEAD_DIR)), 0))
    return up, Vector((up.y, -up.x, 0))


def _cam(name, target, height, dist, tilt=TILT, yaw=0.0, frame=1, shift=(0.0, 0.0)):
    """A locked diorama camera framing `height` units at the target (the lens follows from the distance)."""
    c = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=36.0 * dist / height, blur=BLUR,
                       frame=frame)
    c.data.shift_x, c.data.shift_y = shift
    return c


def _puff(loc, f, n=3, size=0.35, rise=0.5, life=8, seed=0, name="pff"):
    """A little cel dust puff: `n` pale lobes that pop at frame f, swell and vanish (on 2s)."""
    rnd = random.Random(seed)
    m = look.flat("pff_dust", look.hexc("#efe6da"))
    lobes = []
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        p = Vector(loc) + Vector((math.cos(a), math.sin(a), 0)) * size * rnd.uniform(0.4, 1.0)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=size * rnd.uniform(0.5, 0.8),
                                             location=p)
        o = bpy.context.object
        o.name = name
        o.data.materials.append(m)
        for pg in o.data.polygons:
            pg.use_smooth = True
        look.outline(o, 0.01)
        anim.key(o, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(o, "scale", f, 0.6, "LINEAR")
        anim.key(o, "scale", f + life * 0.5, 1.0)
        anim.key(o, "scale", f + life, 0.001)
        anim.key(o, "location", f, p, "LINEAR")
        anim.key(o, "location", f + life, p + Vector((0, 0, rise)), "LINEAR")
        lobes.append(o)
    anim.on_twos(lobes, step=2)
    return lobes


def _ripple(loc, f, frames=12, radius=1.4):
    """The "plip": a thin white ring spreading on the pond from where the claw dips, fading."""
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.03, location=loc)
    r = bpy.context.object
    r.name = "plip"
    m = look.fade("plip_m", look.hexc("#ffffff"), 0.0)
    r.data.materials.append(m)
    mix = m.node_tree.nodes["Mix"]
    anim.key(r, "scale", f - 1, 0.001, "CONSTANT")
    anim.key(r, "scale", f, (0.2, 0.2, 0.3), "LINEAR")
    anim.key(r, "scale", f + frames, (radius, radius * 0.8, 0.3), "LINEAR")
    for fr, a in ((f - 1, 0.0), (f, 0.95), (f + frames, 0.0)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    anim.on_twos([r], step=2)
    return r


def s19():
    """S19: one quiet held shot. The last drop on the claw tip dries away in the sun; his set face, one blink."""
    n = FRAMES["S19"]
    rig, sh = _base(n)
    tip = s3d.claw_tip(sh) + Vector((0.0, 0.0, -0.08))
    d = s3d._drop(tip, 1, n + 40, n + 46, tip - Vector((0, 0, 2)), r=0.22)
    d.animation_data_clear()                                       # only the drying: no swell, no fall, no regrowth
    d.location = tip
    for f, k in ((1, 1.0), (24, 0.85), (45, 0.66), (66, 0.42), (81, 0.18), (90, 0.001)):
        anim.key(d, "scale", f, (k, k, k * 1.2), "LINEAR")
    anim.key(d, "scale", n, 0.001, "CONSTANT")                     # stays gone
    anim.on_twos([d], step=2)
    eyes = s3d.kai_point(rig, "eyes")
    s3d.lock_on(sh, eyes, 1)
    set_face = dict(eye_brow_down=0.45, mouth_short=1.0, eye_open=0.2)
    s3d.kai_face(rig, 1, **set_face)
    s3d.kai_face(rig, 60, **set_face, eye_close=1.0)               # one slow blink
    s3d.kai_face(rig, 63, **set_face)
    anim.lids(sh, 36, 1.0)                                         # the shrimp blinks once, then locks on again
    s3d.lock_on(sh, eyes, 39)
    face = s3d.kai_point(rig, "nose")
    _cam("cam_s19", face.lerp(tip, 0.5) + Vector((0, 0, 0.2)), 8.75, 70.0, shift=(0.055, -0.295))
    return dict(frames=n, step=2, subject=[rig["arm"], sh["root"]] + list(rig.get("cap", [])))


def s20():
    """S20: the futile snap (f24) and the stare at its claw, then his deadpan face from the cut at f44."""
    n = FRAMES["S20"]
    rig, sh = _base(n, breathe=False)
    up, east = _axes()
    nose = s3d.kai_point(rig, "nose")
    root = sh["root"].matrix_world.translation.copy()
    windup = s3d.raise_claw(sh, nose + east * 1.6 - up * 1.4 + Vector((0, 0, 3.0)), nose)   # pulled up and back
    jab = s3d.raise_claw(sh, nose + east * 0.5 + up * 0.1 + Vector((0, 0, 0.8)), nose)      # down at his nose
    stare = s3d.raise_claw(sh, root + up * 1.2 + east * 0.6 + Vector((0, 0, 2.6)),
                           root + Vector((0, 0, 1.4)))                                       # up before its own face
    sh["shoulder"].rotation_euler = sh["cock"]
    bpy.context.view_layer.update()
    k = s3d._key_pose
    k(sh, 1, sh["cock"], 1.4, 0.0)
    k(sh, 14, sh["cock"], 1.4, 0.0)
    k(sh, 20, windup, 1.5, -0.09)                                  # wind-up: cocked back, body squashed
    k(sh, 22, windup, 1.5, -0.09)
    k(sh, 24, jab, -0.25, 0.08, "LINEAR")                          # SNAP... nothing happens
    k(sh, 28, jab, -0.25, 0.0)
    k(sh, 32, jab, -0.25)
    k(sh, 36, stare, 0.4)                                          # brings the claw round in front of its face
    body = sh["body"]
    anim.key(body, "rotation_euler", 30, (0, 0, 0))
    anim.key(body, "rotation_euler", 34, (0, 0, math.radians(-20)))                   # turns to stare at its claw
    anim.key(body, "rotation_euler", 40, (0, math.radians(-14), math.radians(-20)))   # ...and tilts its head
    anim.key(body, "rotation_euler", n, (0, math.radians(-16), math.radians(-20)))
    eyes = s3d.kai_point(rig, "eyes")
    s3d.lock_on(sh, eyes, 1)                                       # locked on through the wind-up and the snap
    s3d.unlock(sh, 28)                                             # ...nothing happened: wide, blank eyes
    anim.lids(sh, 36, 0.3)
    anim.lids(sh, 40, 0.0)
    anim.on_twos([sh["shoulder"], sh["hinge"], body], 2)
    sc = bpy.context.scene
    sc.frame_set(24)
    _puff(s3d.claw_tip(sh) + Vector((0, 0, 0.05)), 24, n=3, size=0.28, seed=2)          # the sad "pff"
    sc.frame_set(1)
    s3d.kai_face(rig, 1, **s3d.TERROR)
    s3d.kai_face(rig, 44, eye_zitome=0.75, mouth_short=1.0)       # deadpan
    _cam("cam_s20_shrimp", root.lerp(nose, 0.35) + Vector((0, 0, 1.2)), 9.0, 72.0, tilt=70.0, yaw=-18.0,
         shift=(0.178, -0.172))
    _cam("cam_s20_kai", eyes + up * 0.15, 3.4, 70.0, frame=44, shift=(0.051, -0.204))
    sc.camera = bpy.data.objects["cam_s20_shrimp"]
    return dict(frames=n, step=2, subject=[rig["arm"], sh["root"]] + list(rig.get("cap", [])))


def s21():
    """S21: it turns its back on him in a huff and stomps off in three hops to the pond, then dips its claw."""
    n = FRAMES["S21"]
    rig, sh = _base(n, breathe=False)
    up, east = _axes()
    r, body = sh["root"], sh["body"]
    p0 = r.location.copy()
    pond = Vector((diorama.MAP["pond"][0], diorama.MAP["pond"][1], 0.0))
    head = s3d.kai_point(rig, "head")
    a = math.radians(-40)                                           # the pond's south-east shore, clear of his head
    edge = pond + Vector((4.2 * math.cos(a), 2.3 * math.sin(a), 0)) * 1.12   # (diorama.pond is 4.2 x 2.3)
    side = Vector((head.x, head.y, 0)) + east * 2.4 - up * 2.2      # off his chest on its claw side
    path = [p0, side, side.lerp(edge, 0.5), edge]
    lean0 = tuple(r.rotation_euler)

    def yaw_to(a, b):
        v = b - a
        return math.atan2(v.x, -v.y)                                # local -Y (its face) toward b

    anim.key(r, "rotation_euler", 1, lean0)
    anim.key(r, "rotation_euler", 4, lean0)
    anim.key(r, "rotation_euler", 8, (0, 0, yaw_to(path[0], path[1])))    # stands up and turns its back on him
    s3d._key_pose(sh, 1, sh["cock"], 0.5)
    s3d._key_pose(sh, 8, (0.0, 0.5, 0.0), 0.0)                     # claw up at its side
    anim.squash(body, 1, 0.0)
    anim.squash(body, 6, -0.1)                                     # a huffy puff-up... squash
    hops = [(8, 14), (16, 22), (24, 30)]                            # (take-off, landing): the 3D shot's frames
    anim.key(r, "location", 1, p0)
    anim.key(r, "location", hops[0][0], p0)
    for i, (f0, f1) in enumerate(hops):
        a, b = path[i], path[i + 1]
        anim.key(r, "rotation_euler", f0, (0, 0, yaw_to(a, b)))
        anim.squash(body, f0 - 1, -0.12)
        anim.squash(body, f0 + 1, 0.12, "LINEAR")
        top = a.lerp(b, 0.5) + Vector((0, 0, max(a.z, b.z) + (1.3 if i == 0 else 1.0)))
        anim.key(r, "location", (f0 + f1) // 2, top)
        anim.key(r, "location", f1, b, "LINEAR")
        anim.squash(body, f1, -0.2, "LINEAR")                      # STOMP
        anim.squash(body, f1 + 3, 0.0)
        anim.key(r, "location", f1 + 1, b)
        _puff(b + Vector((0, 0, 0.15)), f1, n=4, size=0.45, seed=10 + i, name="stomp")
    face_pond = yaw_to(edge, pond)
    anim.key(r, "rotation_euler", 32, (0, 0, face_pond))            # faces the water
    anim.key(r, "rotation_euler", n, (0, 0, face_pond))
    s3d._key_pose(sh, 36, (0.0, 0.5, 0.0), 0.0)
    s3d._key_pose(sh, 42, (0.85, 0.35, 0.0), 0.3)                   # dips the claw in the water
    anim.on_twos([r, body, sh["shoulder"], sh["hinge"]], 2)
    sc = bpy.context.scene
    sc.frame_set(42)
    tip = s3d.claw_tip(sh)
    _ripple((tip.x, tip.y, 0.03), 42)
    sc.frame_set(1)
    s3d.kai_face(rig, 1, eye_zitome=0.5, mouth_short=1.0)
    mid = Vector((p0.x, p0.y, 0)).lerp(edge, 0.5) + Vector((0, 0, 1.0))
    _cam("cam_s21", mid, 17.0, 70.0, tilt=58.0, yaw=20.0, shift=(0.089, -0.104))
    return dict(frames=n, step=2, subject=[rig["arm"], sh["root"]] + list(rig.get("cap", [])))


SHOTS = {"S19": s19, "S20": s20, "S21": s21}
