"""Episode 1 in diorama 2.5D (DIORAMA_EP01.md), helper 1's lab shots, in the dollhouse lab (mk/diorama_lab.py):

    S03a  "Night shift at the marine lab."  Kai at the desk beside the glowing tank, rain on the window; the
          dollhouse seen from above behind his right shoulder. He leans in toward the tank at f22, blinks at f32.
    S03b  "Just me and the pistol shrimp."  Close from the tank side and above, his face turned up to the lens and lit
          cyan by the tank: wide eyes, then the eyes soften (f19) and the smile lands (f22).
    S05b  "But only in water."  The bubble's flash fades on his face (f1-20, on 1s), his right index finger rises
          (f18-24) and taps the tank glass at f30 and again at f34 (the SFX "tik"s are on those frames).

Every beat sits on the same frame as the 3D shot (channels/monsters/ep01v2/helper1.py), with the same lengths
(TIMING.md + 12). Kai is on 2s; the posing and the tank-light shading come from the 3D builder.
    blender -b -y -P channels/monsters/render_shot.py -- diorama S03a OUT [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Matrix, Vector

from channels.monsters.ep01v2 import helper1 as h3d
from channels.monsters.mk import diorama, diorama_lab, hero

KAI = 5.8                                   # hero.load scale in diorama units (1 u = 20 cm): ~1.75 m
TAIL = h3d.TAIL
LEN = h3d.LEN
BLUR = 10.0


def _stage():
    """The night lab and Kai seated at the desk facing the window (+Y), the tank on his right."""
    diorama.setup()
    R = diorama_lab.room()
    sx, sy, sz = R["desk"]["seat"]
    rig = hero.load((sx, sy + 0.25, sz + 0.3 - 0.796 * KAI), scale=KAI, rot_z=math.pi, outfit="earth")
    bpy.context.view_layer.update()
    return R, rig


def _tilt_cap(rig, deg=30.0):
    """Push the cap back on his head (brim up) for the close beats: from a camera 40 deg or more above him (the
    diorama's minimum tilt) the brim would hide his eyes. The dome, brim and letter turn together about the dome's
    centre (their meshes are transformed in the cap's shared rest space, so the head-bone constraints still hold)."""
    caps = rig.get("cap") or []
    dome = next((o for o in caps if o.name.startswith("cap") and o.data and "brim" not in o.name
                 and "letter" not in o.name), None)
    if dome is None:
        return
    pivot = dome.matrix_basis.translation.copy()
    spin = Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(-deg), 4, "X") @ Matrix.Translation(-pivot)
    for o in caps:
        if o.type == "MESH":
            o.data = o.data.copy()
            o.data.transform(o.matrix_basis.inverted() @ spin @ o.matrix_basis)


def _light(name, loc, target, energy, color="#4fd8e8", size=1.2):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy, ld.color, ld.size, ld.use_shadow = energy, diorama.look.hexc(color)[:3], size, False
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


def s03a():
    R, rig = _stage()
    n = LEN["S03a"] + TAIL
    h3d._sit(rig, lean=0.1, look=(0.35, 0.15))
    h3d._key_pose(rig, 1, h3d.BODY)
    h3d._sit(rig, lean=0.2, look=(0.55, 0.22))     # he leans in toward the tank
    h3d._key_pose(rig, 22, h3d.BODY)
    head = h3d._head_pos(rig)
    tank = Vector(R["tank"]["center"])
    R["cam"]("cam_s03a", tuple(head.lerp(tank, 0.45) + Vector((0, 0, -0.6))), dist=72.0, tilt=50.0, yaw=-26.0,
             lens=95.0, blur=BLUR)
    _light("s03a_tank_on_kai", tuple(tank + Vector((-1.0, -1.8, 1.0))), tuple(head), 260, size=1.0)
    h3d._tint_hero(0.12)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "blink", 31)
    hero.face(rig, "neutral", 34)
    return dict(frames=n, step=2, subject=[rig["arm"]])


def s03b():
    R, rig = _stage()
    n = LEN["S03b"] + TAIL
    # he has swivelled his chair toward the tank (no wall on that side of the dollhouse), face lifted to the lens
    turn = 1.0
    _tilt_cap(rig)
    rig["arm"].rotation_euler.z = math.pi - turn
    R["desk"]["chair"].rotation_euler.z = -turn
    h3d._sit(rig, lean=-0.12, look=(0.25, -0.8))     # leaning back, a dreamy look up: the face reads under the cap
    h3d._key_pose(rig, 1, h3d.BODY)
    head = h3d._head_pos(rig)
    face = head + Vector((0.3, 0.15, -0.1))
    cam = R["cam"]("cam_s03b", tuple(face), dist=28.0, tilt=46.0, yaw=-100.0, lens=120.0, blur=BLUR)
    _light("s03b_tank_on_face", tuple(head + Vector((2.2, 1.2, -0.1))), tuple(head), 28, size=0.7)
    h3d._tank_glow(side=Vector((1.0, 0.0, 0.0)))
    hero.line_width(rig, 0.0025)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "look_right", 1, 0.4)
    hero.face(rig, "relaxed", 19, 0.7)              # the eyes soften...
    hero.face(rig, "happy", 22, 1.0)                # ...then the smile ("...and the pistol shrimp")
    h3d._catchlights(rig, cam, until=22, r=0.02)
    return dict(frames=n, step=2, subject=[rig["arm"]])


def s05b():
    R, rig = _stage()
    n = LEN["S05b"] + TAIL
    t = R["tank"]
    tap = Vector((t["center"][0] - 1.15, t["glass_y"] - 0.04, t["center"][2] + 0.55))
    turn = 0.4                                      # his chair angled a little toward the tank
    _tilt_cap(rig)
    rig["arm"].rotation_euler.z = math.pi - turn
    R["desk"]["chair"].rotation_euler.z = -turn
    bpy.context.view_layer.update()
    h3d._sit(rig, lean=0.24, look=(0.35, -0.55))
    h3d._key_pose(rig, 1, h3d.BODY)
    h3d._key_pose(rig, 18, h3d.BODY)
    h3d._sit(rig, lean=0.26, look=(0.35, -0.55), right_reach=tap + Vector((0.12, -0.4, 0.18)))   # the finger rises
    h3d._key_pose(rig, 24, h3d.BODY)
    h3d._sit(rig, lean=0.27, look=(0.35, -0.55), right_reach=tap)                               # tap
    h3d._key_pose(rig, 30, h3d.BODY)
    h3d._sit(rig, lean=0.26, look=(0.35, -0.55), right_reach=tap + Vector((0.0, -0.18, 0.0)))   # off the glass
    h3d._key_pose(rig, 32, h3d.BODY)
    h3d._sit(rig, lean=0.27, look=(0.35, -0.55), right_reach=tap)                               # the second tap
    h3d._key_pose(rig, 34, h3d.BODY)
    head = h3d._head_pos(rig)
    # lower, from the south-east: the finger on the front glass and his face in three-quarter
    R["cam"]("cam_s05b", tuple(head.lerp(tap, 0.5) + Vector((0, 0, -0.2))), dist=32.0, tilt=46.0, yaw=-80.0,
             lens=100.0, blur=BLUR)
    tc = Vector(t["center"])
    fl = _light("s05b_flash", tuple(tc + Vector((-1.0, -0.6, 0.6))), tuple(head), 0, "#e8fbff", 0.6)
    for f, e in ((1, 280), (2, 210), (4, 140), (7, 70), (11, 35), (16, 10), (20, 0)):       # S05a's flash fading
        fl.data.energy = e
        fl.data.keyframe_insert("energy", frame=f)
    _light("s05b_tank_on_face", tuple(head + Vector((2.2, 1.2, -0.1))), tuple(head), 28, size=0.7)
    h3d._tint_hero(0.1)
    hero.line_width(rig, 0.003)
    hero.face(rig, "surprised", 1, 0.7)             # eyes still wide from the flash
    hero.face(rig, "neutral", 13)
    hero.face(rig, "relaxed", 25, 0.5)
    hero.face(rig, "happy", 31, 0.7)                # the tap lands: a small smile
    return dict(frames=n, step=2, ones=(1, 20), subject=[rig["arm"]])


SHOTS = {"S03a": s03a, "S03b": s03b, "S05b": s05b}
