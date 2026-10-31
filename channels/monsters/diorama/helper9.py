"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 9: S06, S08 (the lab dollhouse) and S12 (the
crawl to the pond on the island). Same frame counts and beats as the 3D shots (channels/monsters/ep01v2/helper9.py).

    S06 "Then the storm hit." (41 frames): the dollhouse lab from above, the window in the back wall over Kai at the
        desk. The bolt and the room flash land on "storm" (14); he looks up to the window (16); the room lights
        stutter off for 2 frames at 20, 23, 26, 30, 34 (on 1s,
        like the 3D shot).
    S08 "Water. Cables. Me." (85 frames): the tank's leak runs across the desk, off its edge and over the tiles to the
        power strip (-1..28, "Water."), the lights stutter (34, 38, 42, "Cables."), on "Me." (48) Kai looks down at
        the water at his feet, the spark at the strip (55), every light dies (57) and the frame is black from 58.
    S12 "I was so thirsty." (47 frames): Kai crawls on hands and knees up the trodden clearing toward the pond,
        panting, his tired face turned up to the high camera; the pond glints in the foreground ahead of him.
        Locked camera; Kai and the glint on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama S12 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper1 as d1              # the dollhouse lab with Kai seated at the desk
from channels.monsters.ep01v2 import helper1 as h1               # his seated pose
from channels.monsters.ep01v2 import helper9 as h9              # the crawl, the face mixer and the glint
from channels.monsters.mk import anim, diorama, hero, look, storm

RENDER = h9.RENDER                                               # same render frames as the 3D shots
LENS, BLUR = 100.0, 12.0


def _window_bolt(R, frame, seed=3):
    """An anime lightning bolt (white core, blue glow, a fork) drawn in the window just behind the glass (in front of
    the building silhouettes),
    on at `frame` and `frame` + 2 (off between: the lab's two hits)."""
    import random
    rnd = random.Random(seed)
    (wx, wy, wz), (ww, wh) = R["window"]["center"], R["window"]["size"]
    x, z = wx + rnd.uniform(-0.15, 0.15) * ww, wz + wh * 0.6
    pts = [(x, z)]
    while z > wz - wh * 0.45:
        z -= wh * rnd.uniform(0.1, 0.16)
        x += ww * rnd.uniform(-0.16, 0.16)
        pts.append((x, z))
    k = len(pts) // 2
    fork = [pts[k]]
    for _ in range(3):
        fork.append((fork[-1][0] + ww * rnd.uniform(0.04, 0.09), fork[-1][1] - wh * rnd.uniform(0.08, 0.12)))
    glow = look.flat("s06_bolt_glow", look.hexc("#7cc4ff"), 3.0)
    core = look.flat("s06_bolt_core", look.hexc("#ffffff"), 5.0)
    objs = []
    for name, line, y, wd, mat in (("glow", pts, 0.2, 0.42, glow), ("core", pts, 0.18, 0.15, core),
                                   ("fglow", fork, 0.2, 0.28, glow), ("fcore", fork, 0.18, 0.09, core)):
        verts, faces = [], []
        for i, (px, pz) in enumerate(line):
            verts += [(px - wd / 2, wy + y, pz), (px + wd / 2, wy + y, pz)]
            if i:
                faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
        me = bpy.data.meshes.new("s06_bolt_" + name)
        me.from_pydata(verts, [], faces)
        me.materials.append(mat)
        o = bpy.data.objects.new("s06_bolt_" + name, me)
        bpy.context.scene.collection.objects.link(o)
        o.visible_shadow = False
        for f, on in ((frame - 1, 0), (frame, 1), (frame + 1, 0), (frame + 2, 1), (frame + 3, 0)):
            o.hide_render = not on
            o.keyframe_insert("hide_render", frame=f)
        objs.append(o)
    return objs


def s06():
    R, rig = d1._stage()
    n = RENDER["S06"]
    h1._sit(rig, lean=0.1, look=(0.1, 0.1))
    h1._key_pose(rig, 1, h1.BODY)
    h1._sit(rig, lean=-0.05, look=(0.0, -0.45))                  # the flash: he looks up to the window
    h1._key_pose(rig, 16, h1.BODY)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "surprised", 16, 0.6)
    w = R["window"]["center"]
    head = h1._head_pos(rig)
    cam = R["cam"]("cam_s06", tuple(head.lerp(w, 0.55)), dist=70.0, tilt=44.0, yaw=-24.0, lens=95.0, blur=10.0)
    R["lightning"](14)                                            # on "storm": the sky and the room flash
    _window_bolt(R, 14)                                           # the anime bolt in the window, as in the 3D shot
    R["flicker"]([20, 23, 26, 30, 34])
    return dict(frames=n, step=1, subject=[rig["arm"]] + list(rig.get("cap", [])))


def s08():
    R, rig = d1._stage()
    n = RENDER["S08"]
    h1._sit(rig, lean=0.15, look=(0.3, 0.2))
    h1._key_pose(rig, 1, h1.BODY)
    h1._sit(rig, lean=0.3, look=(-0.2, 0.9))                     # "Me.": he looks down at the water by his chair
    h1._key_pose(rig, 48, h1.BODY)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "blink", 21)
    hero.face(rig, "neutral", 24)
    hero.face(rig, "surprised", 48, 0.8)
    st = R["strip"]
    end, leak = Vector(st["end"]), Vector(R["tank"]["leak"])
    cam = R["cam"]("cam_s08", tuple(Vector((end.x, end.y, 0)).lerp(leak, 0.4)), dist=70.0, tilt=50.0, yaw=-30.0,
                   lens=90.0, blur=10.0)
    R["puddle"](-1, 28)                                           # "Water."
    R["flicker"]([34, 38, 42])                                    # "Cables."
    R["spark"](55)                                                # after "Me."
    R["power_out"](57)
    storm.power_out(cam, 58, flicker=False)                       # black from 58 to the end
    dof = cam.data.dof                                            # no tilt-shift blur on the black plane
    dof.keyframe_insert("aperture_fstop", frame=57)
    dof.aperture_fstop = 64.0
    dof.keyframe_insert("aperture_fstop", frame=58)
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return dict(frames=n, step=2, ones=(52, 60), subject=[rig["arm"]] + list(rig.get("cap", [])))


def _cut_front(isl, cam, target, keep=0.8):
    """The dollhouse cutaway: hide the island trees standing between a low camera and its subject (closer to the
    camera, horizontally, than `keep` x the subject), so no canopy fills the foreground. Out of frame otherwise."""
    cx, cy = cam.location.x, cam.location.y
    reach = keep * math.hypot(target[0] - cx, target[1] - cy)
    for (x, y, *_), objs in zip(isl["spots"], isl["trees"]):
        if objs and math.hypot(x - cx, y - cy) < reach:
            for o in objs:
                o.hide_render = True


def s12():
    diorama.setup()
    isl = diorama.island(seed=31)
    n = RENDER["S12"]
    px, py = diorama.MAP["pond"]
    # up the clearing from the path (south) toward the pond: heading pi = facing +Y (north); look_up 3 tips his
    # face back toward the high camera so it reads under the cap's visor
    rig = h9._crawling_kai((px + 0.5, -12.0, 0.0), math.pi, 1, n, 3.0, period=16, look_up=3.0, step=2)
    hero.line_width(rig, 0.0025)
    for f in range(1, n + 3, 2):                                 # panting on 2s: open / half-open
        wide = (f // 2) % 2 == 0
        h9._face_mix(rig, {"face_sad": 0.7, "eye_zitome": 0.75, "mouse_open": 1.0 if wide else 0.5,
                           "lip_a": 0.6 if wide else 0.3}, f)
    # from the north, high and a little to the side: he crawls toward the lens, the pond between him and us
    cam = diorama.camera("cam_s12", (px + 0.5, -8.0, 2.5), dist=55.0, tilt=40.0, yaw=165.0, lens=LENS, blur=BLUR)
    cam.data.shift_x, cam.data.shift_y = 0.06, -0.08             # left of the Shorts rail (x < 560), above y 960
    _cut_front(isl, cam, (px + 0.5, -8.0))
    h9._glint((px + 1.2, py - 1.4, 0.12), cam, 2, n, size=0.6, every=10, hold=2)
    return dict(frames=n, step=2, subject=[rig["arm"]] + list(rig.get("cap", [])))


SHOTS = {"S06": s06, "S08": s08, "S12": s12}
