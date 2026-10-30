"""Episode 1 (v2), helper 6: the fluffmoth's two shots (channels/monsters/EP01V2_SHOTS.md, line 10-11 of the script).

    S10b (23 frames + 12-frame handle; TIMING.md): "Everything here was tiny. And cute." Close, locked, low at the moth's eye level
          against the bright sky of the new world's clearing. It hovers (wings on 1s, bob and antennae on 2s) and
          snaps into its head-tilt pose a beat in (SG2: one pose change in the shot), then blinks. Its wing eye-spots
          stay SHUT, so they read as innocent curved wing markings.
    S11b (26 frames + handle): "And every one of them was wrong." The wrong detail (EP4): head-on and closer. The wings
          stop dead, spread wide, and all four eye-spots open together and stare straight into the camera, their
          irises lit (LC4/TP11: local light on the creature, never a regrade). Then everything is held still; only a
          few pollen motes drift (LC10).

Both shots: bright day (LC), the world set (mk/world.py) around the moth, anime background blur, locked cameras (SG4)
framed so the moth's face and eye-spots stay above the caption band (y < 845) and out of the right rail (x < 620).
The wings beat on 1s, so both render every frame (step 1).

deliver(shot, out_dir) renders a shot for delivery the cheap way (TP13): the camera is locked and the world is
static, so the world is rendered ONCE as a plate and only the moth and its motes (the subject pass) every frame, then
composited; it writes out_dir/<shot>.mp4 and out_dir/<shot>_sheet.jpg (every 6th frame).
    blender -b -y --python-expr "import sys; sys.path.insert(0, '/home/user/Motion-graphics');
        from channels.monsters.ep01v2 import helper6; helper6.deliver('S10b', 'out/monsters/ep01v2/shots')"
"""
import math
import os
import random
import subprocess
import time

import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

from channels.monsters.mk import anim, fluffmoth, look, paintbg, world

SPOT = (-2.6, 3.2)          # where the moth hovers, in the clearing (away from the puddle and Kai's spots)
HANDLE = 12                 # tail handle on every shot (EP01V2_SHOTS.md)


def _scene(turn):
    """Sky, sun, the world, and the moth at SPOT turned `turn` degrees (0 = facing the camera at -Y)."""
    paintbg.sky()
    look.sun(elev=55, azim=-25, energy=4.5)
    world.build(seed=7)
    rig = fluffmoth.build((SPOT[0], SPOT[1], 0.0))
    rig["root"].rotation_euler = (0, 0, math.radians(turn))
    return rig


SAFE = (0.05, 0.85, 1 - 845 / 1280 + 0.02, 0.93)     # u0, u1, v0, v1 (v up): above the captions, clear of the rail


def _key_points(rig):
    """The face's extent and the rims of the four eye-spots: what must stay inside the safe window."""
    bpy.context.view_layer.update()
    bw = rig["body"].matrix_world
    pts = [bw @ Vector(p) for p in ((-0.95, -0.4, 0.1), (0.95, -0.4, 0.1), (0, -0.6, 0.95), (0, -0.6, -0.75))]
    for s in rig["spots"]:
        mw = s.matrix_world
        pts += [mw @ Vector((math.cos(a), 0, math.sin(a))) for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    return pts


def _camera(rig, view, lens=36, fstop=0.4, window=SAFE):
    """A locked camera looking along `view` (moth space), as close as it can be with the face and every eye-spot
    inside `window`, centred there with lens shift. Focus on the face; the open aperture still melts the world."""
    sc = bpy.context.scene
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    sc.camera = cam
    cam.data.lens = lens
    pts = _key_points(rig)
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    mid = (lo + hi) / 2
    d = -(rig["root"].matrix_world.to_3x3() @ Vector(view)).normalized()
    W, H = sc.render.resolution_x, sc.render.resolution_y
    tu, tv = (window[0] + window[1]) / 2, (window[2] + window[3]) / 2
    for dist in np.arange(2.0, 16.0, 0.05):
        cam.data.shift_x = cam.data.shift_y = 0.0
        cam.location = mid + d * dist
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        bpy.context.view_layer.update()
        for _ in range(3):
            uv = [world_to_camera_view(sc, cam, p) for p in pts]
            cam.data.shift_x += ((min(c.x for c in uv) + max(c.x for c in uv)) / 2 - tu) * W / H
            cam.data.shift_y += (min(c.y for c in uv) + max(c.y for c in uv)) / 2 - tv
            bpy.context.view_layer.update()
        uv = [world_to_camera_view(sc, cam, p) for p in pts]
        if all(window[0] < c.x < window[1] and window[2] < c.y < window[3] for c in uv):
            break
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (cam.location - rig["eyes"][0].matrix_world.translation).length
    cam.data.dof.aperture_fstop = fstop
    world.aim_sparkles(cam)
    return cam


def _drop_keys_after(o, frame, path=None):
    for fc in anim.all_fcurves(o.animation_data.action):
        if path and fc.data_path != path:
            continue
        for i in reversed(range(len(fc.keyframe_points))):
            if fc.keyframe_points[i].co.x > frame:
                fc.keyframe_points.remove(fc.keyframe_points[i])


def _motes(center, f0, f1, n=9, seed=4):
    """Pollen motes drifting slowly up through the frame around the moth (calm shots stay alive, LC10), on 1s."""
    rnd = random.Random(seed)
    m = look.flat("h6_mote", look.hexc("#fff4d6"), 1.2)
    out = []
    for i in range(n):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=rnd.uniform(0.018, 0.032))
        o = bpy.context.object
        o.name = f"h6_mote{i}"
        o.data.materials.append(m)
        p = Vector(center) + Vector((rnd.uniform(-1.8, 1.8), rnd.uniform(-1.4, 0.8), rnd.uniform(-1.3, 1.3)))
        v = Vector((rnd.uniform(-0.15, 0.15), 0, rnd.uniform(0.12, 0.3))) / 24
        ph = rnd.uniform(0, 2 * math.pi)
        for f in range(f0, f1 + 1, 4):
            t = f - f0
            anim.key(o, "location", f, p + v * t + Vector((0.04 * math.sin(ph + t / 9), 0, 0)), "LINEAR")
        out.append(o)
    return out


def s10b():
    frames = 34 + HANDLE
    rig = _scene(-24)
    sp = rig["spots"]
    fluffmoth.spot_lid(rig, 1, 1.0, sp, "CONSTANT")              # shut: they read as wing markings
    fluffmoth.idle(rig, 1, frames, bob=0.09, period=20, seed=5)
    for s in sp:                                                 # idle() schedules no spot blink this short, but
        s.animation_data_clear()                                 # its opening key would open them: keep them shut
        fluffmoth.spot_lid(rig, 1, 1.0, [s], "CONSTANT")
    # the pose change: a beat in, it tilts its head and perks its antennae, then blinks (on 2s, like idle)
    body = rig["body"]
    anim.key(body, "rotation_euler", 14, (0.04, -0.05, 0.0), "CONSTANT")
    fluffmoth.cute_pose(rig, 16)
    for a in rig["antennae"]:                                    # idle's antenna wave would undo the perk: hold it
        _drop_keys_after(a, 16.5)
    _drop_keys_after(body, 16.5, "rotation_euler")               # likewise the sway after the tilt
    for e in rig["eyes"]:                                        # idle's own blinks are replaced by one after the tilt
        e.animation_data_clear()
    anim.blink(rig, 30)
    anim.on_twos([*rig["eyes"]], 2)
    bpy.context.scene.frame_set(24)
    cam = _camera(rig, (0.2, 1.0, 0.12))                         # a touch from its right and below, against the sky
    motes = _motes(rig["body"].matrix_world.translation, 1, frames)
    return dict(frames=frames, step=1, subject=[rig["root"], *motes], camera=cam)


def s11b():
    frames = 26 + HANDLE
    rig = _scene(0)
    sp = rig["spots"]
    stop = 4             # the wings stop dead here, and the spots open on "wrong" (TIMING.md: "was wrong." 0.00-0.48 s)
    for f in range(1, stop):
        ph = (f - 1) % 4
        fluffmoth.wing_pose(rig, f, fluffmoth.WING_BEAT[ph], fluffmoth.WING_BEAT[(ph - 1) % 4] * 0.8)
    fluffmoth.wing_pose(rig, stop, 0.12, 0.05)                   # spread wide and frozen
    for w in rig["wings"]:
        for fc in anim.all_fcurves(w.animation_data.action):
            fc.keyframe_points[-1].interpolation = "CONSTANT"
    hov = rig["hover"]
    anim.key(hov, "location", 1, (0, 0, fluffmoth.HOVER + 0.06), "LINEAR")
    anim.key(hov, "location", stop - 1, (0, 0, fluffmoth.HOVER), "LINEAR")
    anim.key(hov, "location", stop, (0, 0, fluffmoth.HOVER), "CONSTANT")
    # the eye-spots open together (a 1-2 frame stagger), on 2s, and their irises light up; then nothing moves
    fluffmoth.spot_lid(rig, 1, 1.0, sp, "CONSTANT")
    fluffmoth.spot_lid(rig, 1, 0.0, sp, "CONSTANT", prop="glow")
    for s, d in zip(sp, (0, 1, 1, 0)):
        fluffmoth.spot_lid(rig, stop + 1 + d, 1.0, [s])
        fluffmoth.spot_lid(rig, stop + 7 + d, 0.0, [s], "CONSTANT")
        fluffmoth.spot_lid(rig, stop + 3 + d, 0.0, [s], prop="glow")
        fluffmoth.spot_lid(rig, stop + 9 + d, 0.7, [s], "CONSTANT", prop="glow")
    anim.on_twos([hov, *sp], 2)
    bpy.context.scene.frame_set(stop + 10)
    cam = _camera(rig, (0.0, 1.0, 0.06))                         # head-on: all four eye-spots face the lens
    motes = _motes(rig["body"].matrix_world.translation, 1, frames, n=7, seed=9)
    return dict(frames=frames, step=1, subject=[rig["root"], *motes], camera=cam)


SHOTS = {"S10b": s10b, "S11b": s11b}


def deliver(shot, out_dir, work=None, scale=1.0, samples=16, frames=None):
    """Build `shot`, render the static world once (plate) and the subject pass on every frame, composite them, and
    write <out_dir>/<shot>.mp4 (24 fps, x264 crf 12) and <shot>_sheet.jpg (every 6th frame). The frames go to `work`
    (keep it outside the repo: no frame sequences in git); finished frames are skipped, so a run can resume."""
    from PIL import Image
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = look.render_setup(int(720 * scale), int(1280 * scale), samples)
    info = SHOTS[shot]()
    n = info["frames"]
    sc.frame_start, sc.frame_end = 1, n
    work = work or os.path.join("/tmp", f"h6_{shot}")
    os.makedirs(work, exist_ok=True)
    keep = set()

    def walk(o):
        keep.add(o)
        for c in o.children:
            walk(c)
    for r in info["subject"]:
        walk(r)
    plate = os.path.join(work, "plate.png")                      # the world alone, once
    if not os.path.exists(plate):
        for o in keep:
            o.hide_render = True
        sc.frame_set(1)
        sc.render.filepath = plate
        t = time.time()
        bpy.ops.render.render(write_still=True)
        print(f"PLATE {time.time() - t:.1f}s", flush=True)
        for o in keep:
            o.hide_render = False
    look.subject_only(info["subject"])
    bg = Image.open(plate).convert("RGBA")
    for f in frames or range(1, n + 1):
        out = os.path.join(work, f"{f:04d}.png")
        if os.path.exists(out):
            continue
        sc.frame_set(f)
        sc.render.filepath = os.path.join(work, "subject.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        Image.alpha_composite(bg, Image.open(sc.render.filepath).convert("RGBA")).convert("RGB").save(out)
        print(f"FRAME {f} {time.time() - t:.1f}s", flush=True)
    if frames:
        return
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(work, "%04d.png"),
                    "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-map_metadata", "-1",
                    os.path.join(out_dir, f"{shot}.mp4")], check=True)
    ims = [Image.open(os.path.join(work, f"{f:04d}.png")) for f in range(1, n + 1, 6)]
    w, h = ims[0].size
    w, h = w // 3, h // 3
    cols = min(len(ims), 4)
    rows = -(-len(ims) // cols)
    sheet = Image.new("RGB", (w * cols, h * rows), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(out_dir, f"{shot}_sheet.jpg"), quality=90)
