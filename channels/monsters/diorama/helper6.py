"""Diorama Episode 1 (channels/monsters/DIORAMA_EP01.md), helper 6: the fluffmoth in the flower meadow at MAP["moth"],
on the island (seed 31), seen by a close, steep diorama camera (tilt 70). Its body is tipped back so its face and
spread wings look up into the lens. Same beats on the same frames as the 3D shots (ep01v2/helper6.py):

    S10b (35 render frames): "And cute." It hovers, wings fluttering on 2s, eye-spots SHUT (they read as wing
          markings); the head tilt snaps in on frame 16 and holds; a blink at 30-34.
    S11b (38 render frames): "...was wrong." The wings stop dead, spread, on frame 4; the four eye-spots open over
          frames 5-11 and stare up into the lens, irises lit; then everything holds.

Characters on 2s and a locked camera, so both render on 2s (step 2). The moth stays in the readable window (above
y 960, left of x 560); its real sun shadow falls on the meadow (the blob shadow is off).

    blender -b -y -P channels/monsters/render_shot.py -- diorama S10b OUT_DIR [--still N --scale 0.5]
"""
import math
import random

import bpy
from bpy_extras.object_utils import world_to_camera_view

from channels.monsters.mk import anim, diorama, fluffmoth

TILT, LENS, BLUR = 70.0, 110.0, 12.0
FACE_UP = 66.0                     # degrees the body tips back, so the face looks up toward the lens
UP, DOWN = 0.5, -0.4               # the wing flutter: two poses, two frames each (a 4-frame beat on 2s)
WINDOW = (0.06, 0.76, 0.36, 0.86)  # u0, u1, v0, v1 (v up): left of x 560, above y 960 (and not jammed at the top)


def _dressing(center, seed=61):
    """Toy-table texture on the meadow around the moth: flowers (petals with a yellow eye), clover patches and a few
    grass clumps, all lit paint (no lines)."""
    rnd = random.Random(seed)
    P = diorama.lit_paint
    petals = [P("h6_pink", "#d05a8a", "#ff8fb8", "#ffd0e2"), P("h6_white", "#c9c9e0", "#ffffff", "#ffffff"),
              P("h6_lilac", "#9a7cc8", "#c7a8ff", "#e6d8ff")]
    eye = P("h6_eye", "#d9a400", "#ffd23f", "#fff2a8")
    clover = [P("h6_clover0", "#2f7d3a", "#4fae4f", "#86d36e"), P("h6_clover1", "#3a8a3a", "#62bd57", "#9be07c")]
    blade = [P("h6_blade0", "#2e7a33", "#4ea845", "#8fd66a"), P("h6_blade1", "#3d8c3b", "#69c255", "#a8e57f")]
    cx, cy = center

    def disc(loc, r, mat, z=0.04):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(loc[0], loc[1], z))
        o = bpy.context.object
        o.scale = (r, r, r * 0.35)
        o.data.materials.append(mat)
        for pg in o.data.polygons:
            pg.use_smooth = True

    for _ in range(34):                                          # flowers
        x, y = cx + rnd.uniform(-6.5, 6.5), cy + rnd.uniform(-8.0, 10.0)
        m = rnd.choice(petals)
        r = rnd.uniform(0.16, 0.24)
        for k in range(5):
            a = k / 5 * 2 * math.pi + rnd.uniform(0, 1)
            disc((x + math.cos(a) * r, y + math.sin(a) * r), r * 0.8, m, 0.08)
        disc((x, y), r * 0.55, eye, 0.12)
    for _ in range(7):                                           # clover patches
        x, y = cx + rnd.uniform(-6.0, 6.0), cy + rnd.uniform(-7.0, 9.0)
        m = rnd.choice(clover)
        for _ in range(rnd.randint(6, 10)):
            disc((x + rnd.uniform(-0.8, 0.8), y + rnd.uniform(-0.6, 0.6)), rnd.uniform(0.22, 0.34), m, 0.05)
    for _ in range(4):                                           # grass clumps
        x, y = cx + rnd.uniform(-6.0, 6.0), cy + rnd.uniform(-7.0, 9.0)
        for _ in range(9):
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.09, depth=rnd.uniform(0.7, 1.2),
                                            location=(x + rnd.uniform(-0.35, 0.35), y + rnd.uniform(-0.25, 0.25), 0.4),
                                            rotation=(rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), 0))
            bpy.context.object.data.materials.append(rnd.choice(blade))


def _scene(turn):
    diorama.setup()
    diorama.island(seed=31)
    x, y = diorama.MAP["moth"]
    _dressing((x, y))
    rig = fluffmoth.build((x, y, 0.0))
    rig["root"].rotation_euler = (0, 0, math.radians(turn))
    rig["hover"].rotation_euler = (math.radians(-FACE_UP), 0, 0)
    rig["shadow"].hide_render = True                           # the low sun casts the real shadow here
    return rig


def _flutter(rig, f0, f1):
    """Wings up and down on 2s: keys on frame f0 and every even frame (the frames render_shot renders at step 2)."""
    frames = [f0] + [f for f in range(f0 + 1, f1 + 1) if f % 2 == 0]
    for f in frames:
        up = (f // 2) % 2 == 0
        fluffmoth.wing_pose(rig, f, UP if up else DOWN, (DOWN if up else UP) * 0.8)


def _constant(objs):
    for o in objs:
        for fc in anim.all_fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def _camera(rig, name, yaw, frame):
    """The close diorama camera: distance from the moth's size (wings across ~70 % of the width), then lens shift
    to centre it in WINDOW."""
    sc = bpy.context.scene
    sc.frame_set(frame)
    bpy.context.view_layer.update()
    wing = [w.matrix_world @ v.co for w in rig["wings"] for v in list(w.data.vertices)[::6]]
    body = rig["body"].matrix_world.translation
    span = max((p - body).length for p in wing) * 2
    dist = span * LENS / (36.0 * sc.render.resolution_x / sc.render.resolution_y * (WINDOW[1] - WINDOW[0]))
    cam = diorama.camera(name, body, dist=dist, tilt=TILT, yaw=yaw, lens=LENS, blur=BLUR)
    sc.camera = cam
    W, H = sc.render.resolution_x, sc.render.resolution_y
    for _ in range(4):                     # dolly in or out until the wings fill the window's width, then centre them
        bpy.context.view_layer.update()
        uv = [world_to_camera_view(sc, cam, p) for p in wing]
        k = (max(c.x for c in uv) - min(c.x for c in uv)) / (WINDOW[1] - WINDOW[0])
        dist *= k
        cam.location = body + (cam.location - body) * k
        cam.data.dof.focus_distance = dist
        cam.data.dof.aperture_fstop = diorama.fstop_for(dist, LENS, BLUR)
        cam.data.clip_end = dist * 6
        sc.world.mist_settings.start, sc.world.mist_settings.depth = dist * 0.97, dist * 0.55
        bpy.context.view_layer.update()
        uv = [world_to_camera_view(sc, cam, p) for p in wing]
        cam.data.shift_x += ((min(c.x for c in uv) + max(c.x for c in uv)) / 2 - (WINDOW[0] + WINDOW[1]) / 2) * W / H
        cam.data.shift_y += (min(c.y for c in uv) + max(c.y for c in uv)) / 2 - (WINDOW[2] + WINDOW[3]) / 2
    return cam


def s10b():
    frames = 35
    rig = _scene(-14)
    sp = rig["spots"]
    fluffmoth.idle(rig, 1, frames, bob=0.09, period=20, seed=5)
    for w in rig["wings"]:
        w.animation_data_clear()
    _flutter(rig, 1, frames)
    _constant(rig["wings"])
    for s in sp:                                                 # shut all shot: innocent wing markings
        s.animation_data_clear()
        fluffmoth.spot_lid(rig, 1, 1.0, [s], "CONSTANT")
    body = rig["body"]
    anim.key(body, "rotation_euler", 14, (0.04, -0.05, 0.0), "CONSTANT")
    fluffmoth.cute_pose(rig, 16)                                 # the head tilt, on the same frame as the 3D shot
    for o, path in [(a, None) for a in rig["antennae"]] + [(body, "rotation_euler")]:
        for fc in anim.all_fcurves(o.animation_data.action):
            if path and fc.data_path != path:
                continue
            for i in reversed(range(len(fc.keyframe_points))):
                if fc.keyframe_points[i].co.x > 16.5:
                    fc.keyframe_points.remove(fc.keyframe_points[i])
    for e in rig["eyes"]:
        e.animation_data_clear()
    anim.blink(rig, 31)                                          # keys 30-32-34: shut on the rendered frame 32
    anim.on_twos([*rig["eyes"]], 2)
    _camera(rig, "h6_S10b", 14.0, 24)
    return dict(frames=frames, step=2, subject=[rig["root"]])


def s11b():
    frames = 38
    rig = _scene(0)
    sp = rig["spots"]
    stop = 4                                                     # the wings stop dead; the spots open on "wrong"
    _flutter(rig, 1, stop - 1)
    fluffmoth.wing_pose(rig, stop, 0.12, 0.05)
    _constant(rig["wings"])
    hov = rig["hover"]
    anim.key(hov, "location", 1, (0, 0, fluffmoth.HOVER + 0.06), "CONSTANT")
    anim.key(hov, "location", 2, (0, 0, fluffmoth.HOVER + 0.03), "CONSTANT")
    anim.key(hov, "location", stop, (0, 0, fluffmoth.HOVER), "CONSTANT")
    fluffmoth.spot_lid(rig, 1, 1.0, sp, "CONSTANT")
    fluffmoth.spot_lid(rig, 1, 0.0, sp, "CONSTANT", prop="glow")
    for s, d in zip(sp, (0, 2, 2, 0)):                           # on 2s, the hind pair a beat behind
        fluffmoth.spot_lid(rig, stop + 1 + d, 1.0, [s])
        fluffmoth.spot_lid(rig, stop + 7 + d, 0.0, [s], "CONSTANT")
        fluffmoth.spot_lid(rig, stop + 3 + d, 0.0, [s], prop="glow")
        fluffmoth.spot_lid(rig, stop + 9 + d, 1.0, [s], "CONSTANT", prop="glow")
    anim.on_twos([hov, *sp], 2)
    _camera(rig, "h6_S11b", 0.0, stop + 10)
    return dict(frames=frames, step=2, subject=[rig["root"]])


SHOTS = {"S10b": s10b, "S11b": s11b}
