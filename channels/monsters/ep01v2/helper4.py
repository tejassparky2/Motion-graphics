"""Episode 1 (v2), helper 4: the jelly-snail's two shots (channels/monsters/EP01V2_SHOTS.md, lines 10-11 of the script).

    S10a (~1.3 s + 12-frame handle): "Everything here was tiny. And cute." Close, locked, low at the snail's eye level
          against the bright sky of the new world's clearing: the cute held pose (head tilt, stalks leaning) with one
          slow bob and one blink, on 3s. No trail in this shot: the wrong detail is saved for S11a (EP4).
    S11a (~1.0 s + handle): "And every one of them was wrong." The wrong detail (EP4): low behind the snail, looking
          along its slime trail at the holes it has burned through the grass, their ember edges glowing and smoke
          curling up on 1s; the snail sits soft in the background, rippling on 3s (LC4/TP11: the danger is lit
          locally, the ember glow, never a regrade of the frame).

Both shots: bright day (LC), the world set (mk/world.py) around the snail, anime background blur, locked cameras (SG4),
pollen motes drifting on 1s (LC10), framed so the face and the holes stay above the caption band (y < 845) and out of
the right rail (x < 620 where y > 640). Where the trail runs, the world's grass blades and flowers are removed: the
slime has burned them away.

deliver(shot, out_dir) renders a shot the cheap way (TP13): the camera is locked and the world is static, so the world
is rendered ONCE as a plate and only the snail, its trail and the motes (the subject pass) every frame, then
composited; it writes out_dir/<shot>.mp4 and out_dir/<shot>_sheet.jpg (every 6th frame).
    blender -b -y --python-expr "import sys; sys.path.insert(0, '/home/user/Motion-graphics');
        from channels.monsters.ep01v2 import helper4; helper4.deliver('S10a', 'out/monsters/ep01v2/shots')"
"""
import math
import os
import random
import subprocess
import time

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

from channels.monsters.mk import anim, jellysnail, look, paintbg, world

SPOT = (3.0, -1.2)          # where the snail sits in the clearing (away from the puddle, the moth and Kai's spots)
HANDLE = 12                 # tail handle on every shot (EP01V2_SHOTS.md)


def _scene(trail):
    """Sky, sun, the world, and the snail at SPOT (facing -Y), with or without its burned trail."""
    paintbg.sky()
    look.sun(elev=55, azim=-25, energy=4.5)
    h = world.build(seed=7)
    rig = jellysnail.build((SPOT[0], SPOT[1], float(h["ground"](*SPOT))), trail=trail)
    _clear_grass(h, rig)
    return h, rig


def _clear_grass(h, rig):
    """Delete the world's blades and flowers under the snail and along its trail (burned away), in this scene only."""
    tr = rig.get("trail")

    def burned(x, y):
        if ((x - SPOT[0]) / 0.95) ** 2 + ((y - SPOT[1] - 0.15) / 1.8) ** 2 < 1:
            return True
        if not tr:
            return False
        if any((x - hx) ** 2 + (y - hy) ** 2 < (2.2 * r) ** 2 for hx, hy, r in tr["holes"]):
            return True
        return any((x - px) ** 2 + (y - py) ** 2 < 0.55 ** 2 for px, py in tr["path"])
    for o in h["flowers"]:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        mw = o.matrix_world
        dead = [v for v in bm.verts if burned(*(mw @ v.co).xy)]
        if dead:
            bmesh.ops.delete(bm, geom=dead, context="VERTS")
            bm.to_mesh(o.data)
        bm.free()


def _camera(loc, target, lens, focus, fstop=0.15):
    """A locked camera at `loc` aimed at `target`, focused at the world point `focus`; the open aperture melts the
    world behind (anime background blur)."""
    sc = bpy.context.scene
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    cam.name = "h4_cam"
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector(focus) - Vector(loc)).length
    cam.data.dof.aperture_fstop = fstop
    sc.camera = cam
    world.aim_sparkles(cam)
    return cam


def check_safe(cam, pts, label=""):
    """Print where key points land in pixels and whether they stay out of the caption band and the right rail."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    W, H = 720, 1280
    bad = []
    for name, p in pts:
        c = world_to_camera_view(sc, cam, Vector(p))
        x, y = c.x * W, (1 - c.y) * H
        if not (0 < x < W and 0 < y < 845) or (x > 620 and 640 < y < 1180):
            bad.append(name)
        print(f"SAFE {label} {name}: x {x:.0f} y {y:.0f}", flush=True)
    print(f"SAFE {label} {'OK' if not bad else 'OUTSIDE: ' + ', '.join(bad)}", flush=True)


def _motes(center, f0, f1, spread=(1.6, 1.2, 1.1), n=9, seed=4):
    """Pollen motes drifting slowly up through the frame (calm shots stay alive, LC10), on 1s."""
    rnd = random.Random(seed)
    m = look.flat("h4_mote", look.hexc("#fff4d6"), 1.2)
    out = []
    for i in range(n):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=rnd.uniform(0.016, 0.028))
        o = bpy.context.object
        o.name = f"h4_mote{i}"
        o.data.materials.append(m)
        p = Vector(center) + Vector([rnd.uniform(-s, s) for s in spread])
        v = Vector((rnd.uniform(-0.12, 0.12), 0, rnd.uniform(0.1, 0.25))) / 24
        ph = rnd.uniform(0, 2 * math.pi)
        for f in range(f0, f1 + 1, 4):
            t = f - f0
            anim.key(o, "location", f, p + v * t + Vector((0.03 * math.sin(ph + t / 9), 0, 0)), "LINEAR")
        out.append(o)
    return out


def _ember_flicker(f0, f1, seed=6, lo=1.0, hi=1.9):
    """The holes' ember edges breathe brighter and dimmer on 1s: the one locally lit sign of danger (LC4)."""
    rnd = random.Random(seed)
    m = bpy.data.materials["jsnail_ember"]
    em = next(n for n in m.node_tree.nodes if n.type == "EMISSION")
    em.inputs[0].default_value = look.hexc("#ff8a2a")
    for f in range(f0, f1 + 1, 3):
        em.inputs["Strength"].default_value = rnd.uniform(lo, hi)
        em.inputs["Strength"].keyframe_insert("default_value", frame=f)


def _hole_glow(trail, k=2.4):
    """A soft orange glow on the grass round each hole, fading out from the rim (local light, LC4/TP11: no regrade)."""
    m = bpy.data.materials.new("h4_hole_glow")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L = nt.links.new
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = look.hexc("#ff9a3c")
    g = nt.nodes.new("ShaderNodeTexGradient")
    g.gradient_type = "SPHERICAL"
    tc = nt.nodes.new("ShaderNodeTexCoord")
    r = nt.nodes.new("ShaderNodeValToRGB")
    r.color_ramp.elements[0].position, r.color_ramp.elements[0].color = 0.0, (0, 0, 0, 1)
    r.color_ramp.elements[1].position, r.color_ramp.elements[1].color = 0.75, (0.55, 0.55, 0.55, 1)
    L(tc.outputs["Object"], g.inputs[0])
    L(g.outputs[0], r.inputs[0])
    L(r.outputs[0], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(e.outputs[0], mix.inputs[2])
    L(mix.outputs[0], o.inputs[0])
    m.surface_render_method = "BLENDED"
    out = []
    for i, (hx, hy, hr) in enumerate(trail["holes"]):
        bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.0, fill_type="NGON", location=(hx, hy, 0.01))
        c = bpy.context.object
        c.name = f"h4_glow{i}"
        c.scale = (hr * k, hr * k, 1)
        c.data.materials.append(m)
        c.visible_shadow = False
        c.parent = trail["root"]
        c.matrix_parent_inverse = trail["root"].matrix_world.inverted()
        out.append(c)
    return out


def _clear_props(h, center, radius):
    """Delete the world's small mushrooms near `center` (this scene only): nothing bright may pull the eye off the
    holes."""
    for o in h["mushrooms"]:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        mw = o.matrix_world
        dead = [v for v in bm.verts if (Vector((*(mw @ v.co).xy, 0)) - Vector((*center, 0))).length < radius
                and (mw @ v.co).z < 4.0]
        if dead:
            bmesh.ops.delete(bm, geom=dead, context="VERTS")
            bm.to_mesh(o.data)
        bm.free()


def s10a():
    frames = 44 + HANDLE                                             # TIMING.md (v7): 44 in the cut
    h, rig = _scene(trail=False)
    jellysnail.hold(rig, 1, frames, "cute", bob=0.025, period=36)    # one slow bob over the shot
    anim.blink(rig, 23)                                               # SG2: one face change (shut on a 3s frame)
    x, y, z = SPOT[0], SPOT[1], 0.0
    head = (x, y - 1.1, z + 1.1)
    cam = _camera((x - 1.75, y - 4.6, z + 1.05), (x + 0.02, y - 1.1, z + 1.0), 42, head)
    check_safe(cam, [("bulb_l", (x - 0.36, y - 0.98, 2.0)), ("bulb_r", (x + 0.36, y - 0.98, 2.0)),
                     ("mouth", (x, y - 1.17, 0.6)), ("cheek_r", (x + 0.3, y - 1.12, 0.72))], "S10a")
    motes = _motes((x, y - 1.6, 1.1), 1, frames)
    return dict(frames=frames, step=1, subject=[rig["root"], *motes], camera=cam)


def s11a():
    frames = 27 + HANDLE                                             # TIMING.md (v7): 27 in the cut
    h, rig = _scene(trail=True)
    tr = rig["trail"]
    x, y = SPOT
    _clear_props(h, (x, y + 6.0), 3.5)                               # the small red mushroom by the camera
    # the wrong detail must read in 1.1 s (EP4): darker, thicker smoke, brighter embers, a glow on the grass
    jellysnail.smoke(tr, 1, strength=1.6, color="#3a3340")
    jellysnail.idle(rig, 1, frames)
    _ember_flicker(1, frames, lo=1.8, hi=2.8)
    _hole_glow(tr)
    far, mid = tr["holes"][-1], tr["holes"][-3]
    # low and close behind the last holes, looking up the trail: the nearest holes big in the lower middle, the
    # trail leading the eye up to the snail
    cam = _camera((far[0] + 0.3, far[1] + 2.6, 1.3), (x, y + 1.8, -0.8), 32, (mid[0], mid[1], 0.02), 0.8)
    check_safe(cam, [(f"hole{k}", (hx, hy, 0.02)) for k, (hx, hy, r) in enumerate(tr["holes"])] +
               [("shell_top", (x, y + 0.32, 1.57)), ("bulb", (x, y - 0.98, 2.0))], "S11a")
    motes = _motes((mid[0], mid[1], 0.7), 1, frames, spread=(1.0, 1.4, 0.6), n=8, seed=11)
    return dict(frames=frames, step=1, subject=[rig["root"], tr["root"], *motes], camera=cam)


SHOTS = {"S10a": s10a, "S11a": s11a}


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
    work = work or os.path.join("/tmp", f"h4_{shot}")
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
    os.makedirs(out_dir, exist_ok=True)
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
