"""Episode 1 v2 shots by helper 5 (EP01V2_SHOTS.md, exact lengths from ep01v2/TIMING.md): the thorn bush and the
butcher bird (the tuftwing, whose shadow is far too big) in the meadow after the snap. Every shot renders its cut
length plus the 12-frame tail handle.

    S22 "That's when I saw the thorn tree." (45 frames, line at 0.30-1.52 s): reveal by scale (SU2). Close on the
        larder, tiny shells skewered on thorns, then the camera cranes up and back (a vertical move, SG5) to the whole
        thorn bush towering beside the puddle, taller than Kai, its big empty thorn near the top. Camera and smoke on
        1s.
    S23 "A butcher bird hangs its food on thorns." (70 frames, line at 0.30-2.16 s): from the ground beside the
        puddle (the shrimp's eye level), looking up: the bird flaps down onto the top of the bush, settles, then lowers
        its head and glares down at us (SU4), and at frame 32 the light turns: a hard top shadow and amber eye glints
        (SU5, TP11, LC4: cute to deadly on the same model). Frame 56 cuts to the insert (SG10): the one empty thorn,
        shrimp-sized, a glint on its tip, and far below it the bird's giant winged shadow, dark on the open grass in
        front of the bush. Locked cameras, the bird on 2s, so only even frames render (TP13).

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S22 OUTDIR
"""
import math

import bpy
import numpy as np
from mathutils import Vector

from channels.monsters.mk import anim, butcherbird, look, meadow, thornbush, tuftwing

TAIL = 12
BIRD_SCALE = 1.3                     # the tuftwing a little bigger than the 2-unit shrimp it hunts
CUT = {"S22": 45, "S23": 70}         # ep01v2/TIMING.md
INSERT_AT = 56                       # S23: the last ~0.6 s of the cut is the empty-thorn insert
SHADOW_SHIFT = (0.6, -4.6, 0.0)      # S23: the giant shadow lies out on the open grass in front of the bush


def _target(name, loc):
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.location = loc
    return e


def _cam(name, loc, target, lens, fstop=1.0):
    """A camera that tracks an empty (so its aim can be keyed) and focuses on it."""
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.data.lens = lens
    c.data.clip_end = 2000                                     # the true-scale meadow (HELPERS.md v6)
    t = _target(f"{name}_aim", target)
    con = c.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = t, "TRACK_NEGATIVE_Z", "UP_Y"
    c.data.dof.use_dof = True
    c.data.dof.focus_object = t
    c.data.dof.aperture_fstop = fstop
    return c, t


def _smooth(t):
    return t * t * (3 - 2 * t)


def _move(obj, f0, f1, a, b):
    """Key obj.location from a to b over f0..f1 with an ease in and out, one key a frame (camera moves on 1s)."""
    for f in range(f0, f1 + 1):
        k = _smooth((f - f0) / (f1 - f0))
        anim.key(obj, "location", f, tuple(a[i] + (b[i] - a[i]) * k for i in range(3)), "LINEAR")


def _glint(loc, cam, f, size=0.28):
    """A 4-point sparkle that pops on the tip of the empty thorn (2s, held between even frames)."""
    pts, n = [], 8
    for i in range(n):
        a = i / n * 2 * math.pi
        r = 1.0 if i % 2 == 0 else 0.22
        pts.append((math.cos(a) * r, math.sin(a) * r, 0))
    me = bpy.data.meshes.new("glint")
    me.from_pydata([(0, 0, 0)] + pts, [], [(0, i + 1, (i + 1) % n + 1) for i in range(n)])
    o = bpy.data.objects.new("glint", me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(look.flat("glint_m", (1, 1, 1, 1), 1.5))
    o.location = loc
    con = o.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = cam, "TRACK_Z", "UP_Y"
    for fr, s in ((f - 2, 0.001), (f, size * 0.5), (f + 2, size), (f + 4, size * 0.7), (f + 6, 0.001)):
        anim.key(o, "scale", fr, s, "CONSTANT")
    return o


def _rage_light(rig, f, cut_z, name="tuft"):
    """Cute to deadly with light on the same model (SU5, TP11, LC4): from frame f a hard top shadow puts everything of
    the bird above world height cut_z into a dark, cool shadow tone, and its eye highlights narrow to a sharp amber
    glint with a little local glow. Nothing else in the frame changes."""
    def switch(socket, before, after):
        for fr, v in ((f - 1, before), (f, after)):
            socket.default_value = v
            socket.keyframe_insert("default_value", frame=fr)
        fc = socket.id_data.animation_data.action
        for c in anim.all_fcurves(fc):
            for kp in c.keyframe_points:
                kp.interpolation = "CONSTANT"
    mats = {m for o in [rig["root"]] + list(rig["root"].children_recursive) if o.type == "MESH"
            for m in o.data.materials if m and m.name.startswith(name) and not m.name.endswith(("_hi", "_blush"))}
    for m in mats:
        nt = m.node_tree
        em = next(n for n in nt.nodes if n.type == "EMISSION")
        if not em.inputs[0].links:
            continue
        src = em.inputs[0].links[0].from_socket
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        above = nt.nodes.new("ShaderNodeMath")
        above.operation = "GREATER_THAN"
        above.inputs[1].default_value = cut_z
        on = nt.nodes.new("ShaderNodeMath")
        on.operation = "MULTIPLY"
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
        mix.inputs[7].default_value = (0.4, 0.33, 0.58, 1)       # the deep, cool top-shadow tone
        nt.links.new(geo.outputs["Position"], sep.inputs[0])
        nt.links.new(sep.outputs["Z"], above.inputs[0])
        nt.links.new(above.outputs[0], on.inputs[0])
        nt.links.new(on.outputs[0], mix.inputs["Factor"])
        nt.links.new(src, mix.inputs[6])
        nt.links.new(mix.outputs[2], em.inputs[0])
        switch(on.inputs[1], 0.0, 1.0)
    hi = bpy.data.materials[f"{name}_hi"]
    em = next(n for n in hi.node_tree.nodes if n.type == "EMISSION")
    switch(em.inputs[0], (1, 1, 1, 1), look.hexc("#ffb21f"))
    switch(em.inputs[1], 1.0, 1.6)
    glow = look.fade("rage_glow", look.hexc("#ff9a1a"), 0.38)
    for o in list(rig["root"].children_recursive):
        if o.name.startswith((f"{name}_hi", f"{name}_hi2")) and o.type == "MESH":
            anim.key(o, "scale", f - 1, tuple(o.scale), "CONSTANT")
            anim.key(o, "scale", f, (o.scale[0] * 0.8, o.scale[1], o.scale[2] * 0.4), "CONSTANT")   # a sharp slit
            if o.name.startswith(f"{name}_hi") and not o.name.startswith(f"{name}_hi2"):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.1, location=(0, 0, 0))
                g = bpy.context.object
                g.name = f"{o.name}_glow"
                g.data.materials.append(glow)
                g.parent = o                                   # centred on the highlight
                g.visible_shadow = False
                anim.key(g, "scale", f - 1, 0.001, "CONSTANT")
                anim.key(g, "scale", f, (1.0, 0.3, 1.0), "CONSTANT")


def _deep_shadow(rig, offset):
    """The insert's giant shadow: moved out over the open grass (where a bird that high would cast it) and darker,
    more opaque, so it is the clearest thing in the frame."""
    sh = rig["shadow"]
    bpy.context.view_layer.update()
    mw = sh.matrix_world.copy()
    mw.translation += Vector(offset)
    sh.matrix_world = mw
    nt = sh.data.materials[0].node_tree
    tex = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
    mixs = next(n for n in nt.nodes if n.type == "MIX_SHADER")
    em = next(n for n in nt.nodes if n.type == "EMISSION")
    em.inputs[0].default_value = look.hexc("#120d1c")
    k = nt.nodes.new("ShaderNodeMath")
    k.operation, k.use_clamp = "MULTIPLY", True
    k.inputs[1].default_value = 1.45
    nt.links.new(tex.outputs["Alpha"], k.inputs[0])
    nt.links.new(k.outputs[0], mixs.inputs[0])


def s22():
    """S22: close on the shells, hold a beat, then crane up and back to the whole bush (frames 8-36), hold."""
    m = meadow.build("after")
    h = thornbush.build()
    n = CUT["S22"] + TAIL
    meadow.smoke(m["smoke_sources"], -40, n + 10, every=14, rise=3.5, size=0.9)
    bx, by, _ = thornbush.BUSH_AT
    shells = np.array(h["shell_spots"])
    near = shells[np.argsort(np.abs(shells[:, 2] - 2.4))[:4]].mean(axis=0)   # the cluster at the shrimp's height
    cam, aim = _cam("cam_s22", (near[0] + 0.3, near[1] - 2.5, near[2] - 0.2), tuple(near), 40, fstop=1.0)
    _move(cam, 8, 36, tuple(cam.location), (bx + 1.4, by - 13.5, 3.2))
    _move(aim, 8, 36, tuple(near), (bx, by, 5.6))
    bpy.context.scene.camera = cam
    return dict(frames=n, step=1, subject=[])


def s23():
    """S23: the bird lands on the top of the bush (from below) and glares down at us; cut on INSERT_AT to the empty
    thorn with the giant shadow on the ground below it."""
    meadow.build("after")
    h = thornbush.build(bird_scale=BIRD_SCALE)
    n = CUT["S23"] + TAIL
    perch = Vector(h["perch"])
    eye = Vector((perch.x + 7.0, perch.y - 7.0, 2.0))           # past the puddle, low, looking up
    rig = tuftwing.build((perch.x, perch.y, 0.0), shadow_span=10.0)   # root and shadow on the ground below
    rig["root"].scale = (BIRD_SCALE,) * 3
    to_cam = eye - perch
    rig["root"].rotation_euler = (0, 0, math.atan2(to_cam.x, -to_cam.y))   # it faces us
    rest = (0.0, 0.0, perch.z / BIRD_SCALE)
    butcherbird.land(rig, 20, drop=(0.6, 1.8, 3.2), rest=rest)
    tuftwing.beat(rig, 22)                                       # its shadow answers the landing, slow and heavy
    butcherbird.stare(rig, 32, down=0.5, hold=n - 32)
    _rage_light(rig, 32, perch.z + (tuftwing.CENTER[2] - 0.1) * BIRD_SCALE)
    _deep_shadow(rig, SHADOW_SHIFT)
    anim.blink(rig, 29)                                          # shut on frame 30, a held frame on 2s
    anim.on_twos(tuftwing._animated(rig), step=2)
    sc = bpy.context.scene
    up, _ = _cam("cam_s23_below", tuple(eye), tuple(perch + Vector((0, 0, 1.2))), 55, fstop=1.6)
    base, tip = (Vector(p) for p in h["empty_thorn"])
    mid = (base + tip) / 2
    d = (tip - base).normalized()
    ground = Vector((perch.x + SHADOW_SHIFT[0] - 0.6, perch.y + SHADOW_SHIFT[1] + 0.8, 0.0))
    ins, _ = _cam("cam_s23_thorn", tuple(mid + Vector((-0.4, -2.2, 3.0))),
                  tuple(mid * 0.58 + ground * 0.42 + Vector((-0.9, 0, 0))), 18, fstop=6.0)
    ins.data.dof.focus_object = None
    ins.data.dof.focus_distance = (mid - ins.location).length
    _glint(tuple(tip + d * 0.03), ins, INSERT_AT + 6)
    for f, c in ((1, up), (INSERT_AT, ins)):
        mk = sc.timeline_markers.new(c.name, frame=f)
        mk.camera = c
    sc.camera = up
    return dict(frames=n, step=2, subject=[rig["root"]])


SHOTS = {"S22": s22, "S23": s23}
