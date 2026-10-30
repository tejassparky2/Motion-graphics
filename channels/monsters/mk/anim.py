"""Keyframing helpers for the series: game-style timing (anticipation, fast snaps, holds, overshoot), squash and
stretch that keeps volume, blinks, wobble, camera shake, and VFX (shockwave ring, flash, dust)."""
import math
import random

import bpy

from . import look


def key(o, path, frame, value, interp="BEZIER", index=-1):
    """Set `o.path = value` at `frame` and key it (interp applies to the keys just made)."""
    if path == "scale" and isinstance(value, (int, float)):
        value = (value, value, value)
    setattr(o, path, value)
    o.keyframe_insert(data_path=path, frame=frame, index=index)
    ad = o.animation_data
    if ad and ad.action:
        for fc in _fcurves(ad.action, path):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.01:
                    kp.interpolation = interp
                    if interp == "BEZIER":
                        kp.easing = "AUTO"


def _fcurves(action, path):
    if hasattr(action, "fcurves"):
        try:
            return [fc for fc in action.fcurves if fc.data_path == path]
        except Exception:
            pass
    out = []
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out += [fc for fc in bag.fcurves if fc.data_path == path]
    return out


def squash(o, frame, amount, interp="BEZIER"):
    """amount > 0 stretches up, < 0 squashes down; x and y compensate so the volume stays the same."""
    z = 1.0 + amount
    xy = 1.0 / math.sqrt(z)
    key(o, "scale", frame, (xy, xy, z), interp)


def idle(rig, f0, f1, period=28, amount=0.035, seed=1):
    """A gentle breathing bob, antenna wobble and blinks between f0 and f1."""
    rnd = random.Random(seed)
    f = f0
    while f <= f1:
        squash(rig["body"], f, amount)
        squash(rig["body"], f + period // 2, -amount)
        f += period
    for i, a in enumerate(rig["antennae"]):
        f = f0 + i * 5
        while f <= f1:
            key(a, "rotation_euler", f, (0.12, 0.0, (-1) ** i * 0.08))
            key(a, "rotation_euler", f + period // 2, (-0.08, 0.0, -(-1) ** i * 0.05))
            f += period
    f = f0 + rnd.randint(10, 30)
    while f < f1 - 4:
        blink(rig, f)
        f += rnd.randint(40, 70)


def blink(rig, f):
    for e in rig["eyes"]:
        key(e, "scale", f - 1, (1, 1, 1))
        key(e, "scale", f + 1, (1.1, 1, 0.08), "LINEAR")
        key(e, "scale", f + 3, (1, 1, 1))


def snap(rig, f, wind=8):
    """Anticipation (claw cocks back, body squashes) for `wind` frames, then the snap at frame f: the finger shuts in
    two frames, the claw jerks forward, the body stretches and settles."""
    sh, hg, body = rig["shoulder"], rig["hinge"], rig["body"]
    key(sh, "rotation_euler", f - wind, (0.0, 0.6, 0.0))
    key(sh, "rotation_euler", f - 1, (0.35, 0.75, 0.0))           # cocked back
    key(sh, "rotation_euler", f + 1, (-0.45, 0.55, 0.0), "LINEAR")  # thrown forward
    key(sh, "rotation_euler", f + 8, (-0.2, 0.6, 0.0))
    key(sh, "rotation_euler", f + 16, (0.0, 0.6, 0.0))
    key(hg, "rotation_euler", f - wind, (0.35, 0.0, 0.0))         # finger opens wide
    key(hg, "rotation_euler", f - 1, (0.5, 0.0, 0.0))
    key(hg, "rotation_euler", f + 1, (-0.25, 0.0, 0.0), "CONSTANT")  # SNAP shut
    key(hg, "rotation_euler", f + 12, (-0.25, 0.0, 0.0))
    key(hg, "rotation_euler", f + 20, (0.1, 0.0, 0.0))
    squash(body, f - wind, 0.0)
    squash(body, f - 1, -0.12)
    squash(body, f + 1, 0.14, "LINEAR")
    squash(body, f + 5, -0.05)
    squash(body, f + 10, 0.0)


def shockwave(origin, f, frames=10, radius=9.0, color="#ffffff"):
    """A white ring that races outward along the ground and fades."""
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.08, location=origin)
    ring = bpy.context.object
    ring.name = f"shock_{f}"
    m = look.fade(f"shock_m_{f}", look.hexc(color), 1.0)
    ring.data.materials.append(m)
    mix = m.node_tree.nodes["Mix"]
    key(ring, "scale", f - 1, 0.01, "CONSTANT")
    key(ring, "scale", f, 0.3, "LINEAR")
    key(ring, "scale", f + frames, radius, "LINEAR")
    for fr, a in ((f - 1, 0.0), (f, 1.0), (f + frames * 0.6, 0.8), (f + frames, 0.0)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    return ring


def flash(cam, f, frames=3, color="#ffffff"):
    """A full-screen white flash: a plane just in front of the camera whose alpha pops and decays."""
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    p = bpy.context.object
    p.name = f"flash_{f}"
    p.parent = cam
    p.location = (0, 0, -0.2)
    p.scale = (0.5, 0.5, 1)
    m = look.fade(f"flash_m_{f}", look.hexc(color), 0.0)
    p.data.materials.append(m)
    mix = m.node_tree.nodes["Mix"]
    for fr, a in ((f - 1, 0.0), (f, 0.7), (f + 1, 0.25), (f + frames, 0.0)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    return p


def dust(origin, f, n=14, spread=3.0, seed=3, color="#efe6da"):
    """Puffs that burst outward from `origin`, grow and fade."""
    rnd = random.Random(seed)
    m = look.fade(f"dust_m_{f}", look.hexc(color), 0.0)
    mix = m.node_tree.nodes["Mix"]
    for fr, a in ((f - 1, 0.0), (f, 0.45), (f + 18, 0.0)):
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=fr)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=origin)
        d = bpy.context.object
        d.data.materials.append(m)
        for pgn in d.data.polygons:
            pgn.use_smooth = True
        s = rnd.uniform(0.3, 0.6)
        key(d, "scale", f - 1, 0.01, "CONSTANT")
        key(d, "scale", f, s * 0.4)
        key(d, "scale", f + 18, s * 1.8)
        end = (origin[0] + math.cos(a) * spread * rnd.uniform(0.6, 1.0),
               origin[1] + math.sin(a) * spread * rnd.uniform(0.6, 1.0), origin[2] + rnd.uniform(0.2, 1.2))
        key(d, "location", f, origin)
        key(d, "location", f + 18, end)


def shake(cam, f, frames=10, amp=0.12, seed=5):
    """Decaying camera shake starting at frame f (keys on top of the camera's resting location)."""
    rnd = random.Random(seed)
    base = cam.location.copy()
    key(cam, "location", f - 1, base)
    for i in range(frames):
        d = amp * (1 - i / frames) ** 2
        key(cam, "location", f + i, (base.x + rnd.uniform(-d, d), base.y, base.z + rnd.uniform(-d, d)), "LINEAR")
    key(cam, "location", f + frames, base)


def all_fcurves(action):
    out = []
    try:
        out += list(action.fcurves)
    except Exception:
        pass
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out += list(bag.fcurves)
    return out


def on_twos(objects, step=3):
    """TV-anime timing: characters hold each pose for `step` frames (a Stepped modifier on every F-curve); the camera
    and VFX stay on ones."""
    for o in objects:
        ad = o.animation_data
        if not (ad and ad.action):
            continue
        for fc in all_fcurves(ad.action):
            if not any(m.type == "STEPPED" for m in fc.modifiers):
                m = fc.modifiers.new("STEPPED")
                m.frame_step = step
