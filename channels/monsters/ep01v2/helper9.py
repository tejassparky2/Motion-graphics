"""Episode 1 v2 shots by helper 9 (EP01V2_SHOTS.md): the storm in the lab (S06), the water and the power cut (S08), and
the meadow before the snap: Kai crawling to the puddle (S12), the puff-shrimp's claw in the water (S13, the clue) and
Kai's sceptical face (S14). Every shot carries the 12-frame tail handle.

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S06 OUTDIR
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.mk import anim, lab, look, meadow, puffshrimp, storm

TAIL = 12


def _frames(seconds):
    return round(seconds * 24) + TAIL


def _cam(name, loc, target, lens, fstop=None, focus=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    if fstop:
        c.data.dof.use_dof = True
        c.data.dof.aperture_fstop = fstop
        c.data.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    bpy.context.scene.camera = c
    return c


# ------------------------------------------------------------------------------------------------------------ lab
def s06():
    """S06 "Then the storm hit." (1.5 s): the lab window, locked. An anime bolt (storm.py, clipped to the window glass)
    on the lab's two-hit lightning (2-frame flashes of sky and room), then the room lights stutter on 2s."""
    h = lab.build()
    cam = h["cams"]["window"]
    bpy.context.scene.camera = cam
    bpy.data.objects["bolt"].hide_render = True          # the lab's simple bolt: storm.py draws the anime one
    win = bpy.data.objects["win_glass"]
    h["lightning"](8)
    storm.lightning(cam, 8, window=win, depth=7.5, flash=False, room_light=0, seed=3)
    h["flicker"]([16, 20, 23, 27])
    return dict(frames=_frames(1.5), step=1, subject=[])


def s08():
    """S08 "Water. Cables. Me." (2.2 s): floor level, locked. Water runs across the tiles to the power strip (0.8 s),
    a spark (0.6 s), then black (0.8 s, plus the tail). Nothing graphic: the cut to black is the whole event."""
    h = lab.build()
    cam = h["cams"]["floor"]
    bpy.context.scene.camera = cam
    h["crack_puddle"](-8, 19)                              # the leak started off-screen; it reaches the strip at 19
    h["flicker"]([24, 28])
    h["spark"](20)
    h["power_out"](34)
    storm.power_out(cam, 35, flicker=False)
    return dict(frames=_frames(2.2), step=1, subject=[])


# ------------------------------------------------------------------------------------------------------- meadow
SHRIMP_AT = (1.4, 0.4, 0.0)       # on the dry bank beside the puddle; its lowered claw lies in the water


def _dipped_shrimp(f0, f1):
    """The puff-shrimp drinking: claw lowered into the puddle, a slow bob and a little claw dip on 3s, ripples and a
    drop when the claw lifts a little."""
    rig = puffshrimp.build(SHRIMP_AT)
    sh, body = rig["shoulder"], rig["body"]
    for f, ang in ((f0, 1.76), (f0 + 18, 1.82), (f0 + 33, 1.7), (f0 + 48, 1.82), (f1, 1.76)):
        anim.key(sh, "rotation_euler", f, (ang, 0.0, 0.0))
    for f in range(f0, f1 + 1, 24):
        anim.squash(body, f, 0.0)
        anim.squash(body, f + 12, -0.04)
    anim.key(rig["hinge"], "rotation_euler", f0, (0.15, 0, 0))
    for e in rig["eyes"]:                                 # content, half-closed while it drinks
        anim.key(e, "scale", f0, (1, 1, 0.65), "CONSTANT")
    anim.blink(rig, f0 + 40)
    anim.on_twos([sh, body, rig["hinge"]] + rig["eyes"], step=3)
    return rig


def _ripples(center, f0, f1, every=12, seed=4):
    m = look.fade("ripple_m", look.hexc("#ffffff"), 0.0)
    mix = m.node_tree.nodes["Mix"]
    f = f0
    rings = []
    while f < f1:
        bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.035, location=center)
        r = bpy.context.object
        r.scale = (0.001, 0.001, 0.001)
        r.data.materials.append(m)
        anim.key(r, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(r, "scale", f, (0.5, 0.4, 0.3), "LINEAR")
        anim.key(r, "scale", f + 20, (1.25, 0.95, 0.3), "LINEAR")
        anim.key(r, "scale", f + 21, 0.001, "CONSTANT")
        rings.append(r)
        f += every
    for fr, a in ((f0 - 1, 0.0), (f0, 0.9)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    return rings


def s13():
    """S13 "Something else was already drinking." (2.5 s): insert of the clue (SG10, CH3): the puff-shrimp at the
    puddle with its big claw dipped in the water. Low, close, locked; acting on 3s, ripples on 1s."""
    meadow.build("before")
    n = _frames(2.5)
    _dipped_shrimp(1, n)
    tip = (SHRIMP_AT[0] - 1.5, SHRIMP_AT[1] - 1.7, 0.02)
    _ripples(tip, -20, n)
    _cam("cam_s13", (-2.9, -4.4, 1.9), (0.0, -0.9, 0.45), 34, fstop=2.8, focus=(-0.2, -1.3, 0.2))
    return dict(frames=n, step=1, subject=[])


SHOTS = {"S06": s06, "S08": s08, "S13": s13}
