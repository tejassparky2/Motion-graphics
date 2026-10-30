"""Episode 1 (v2), helper 10: S15, THE SNAP (no words, 115 frames + a 12-frame handle; channels/monsters/ep01v2/
TIMING.md), the episode's biggest moment, staged with the report's nine-step hit (IM1-IM5, SS2, SG6, SG8, SG9) on the
meadow "before" set. The strike (the snap sound) is on frame 42; frames 19-41 are the ~1 s of near-silence (SS2).

    1. A   POV: Kai's hand reaches toward the puff-shrimp drinking at the puddle (the observation; Kai acts on 3s)
    2. B   the shrimp's eyes, 3 frames: they narrow (SG6)
    3. C   the claw rises out of the puddle (on 2s) and is held, dripping; only the drops move (IM2; silence, SS2)
    4. D   strike: the claw snaps shut (2 frames)
    5.     flash: 2 white frames                                    (2D, composite())
    6.     impact frames on 2s from the subject pass (comp.impact)  (2D, composite())
    7. E   from behind Kai, small under the towering forest (SG8, SG9): the white ring, the forest wall sliced and
           popped into dust (mk/erase.py), the result held, camera locked
    8. F   Kai blown backwards (on 2s)
    9. G   Kai on his back, shocked, the observer shake on 2s decaying from ~30% to ~1% of the frame width (IM5);
           his eyes close (into S16, "When I opened my eyes...")

Blender (render_shot.py builds SHOTS["S15"]), then the 2D pass and delivery, outside Blender:
    BLENDER_USER_SCRIPTS=/home/user/tools/blender_scripts blender -b -y -P channels/monsters/render_shot.py -- \\
        ep01v2 S15 build/monsters/S15
    blender ... render_shot.py -- ep01v2 S15 build/monsters/S15_sub --frames 46-49 --subject
    python channels/monsters/ep01v2/helper10.py build/monsters/S15 build/monsters/S15_sub out/monsters/ep01v2/shots

Units: 1 unit = 20 cm; the shrimp is 2 units tall, Kai hero.load(scale=5.8) (~8.7 units), the meadow trees 25-35
units. The erased trees' stumps are the meadow "after" stumps (sliced, glowing cuts), so the later chest shots
match."""
import math
import os
import random
import sys

try:
    import bpy
    from mathutils import Euler, Matrix, Vector
except ImportError:                                            # composite() runs outside Blender
    bpy = None

FPS = 24
A, B, C, D = 1, 19, 22, 42                                     # the cuts (Blender frames); D = the strike
FLASH, IMPACT = 44, 46                                         # 2D: 2 white frames, then 4 impact frames on 2s
E, F, G, END = 50, 80, 94, 115
HANDLE = 12                                                    # tail handle for the edit
KAI_SCALE = 5.8
FWD = (0.0, 1.0, 0.0)                                          # Kai faces +Y (toward the shrimp)


# ---------------------------------------------------------------- Kai: poses by aiming bones

def _bone(k, name):
    try:
        return k["bone"](name)
    except (AttributeError, KeyError):
        return None


def _reset(k):
    for pb in k["arm"].pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)


def _aim(k, name, d):
    """Turn a bone about its head so it points along world direction d."""
    pb = _bone(k, name)
    if pb is None:
        return
    arm = k["arm"]
    bpy.context.view_layer.update()
    m = pb.matrix.copy()
    cur = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    want = (arm.matrix_world.to_3x3().inverted() @ Vector(d)).normalized()
    q = cur.rotation_difference(want).to_matrix().to_4x4()
    h = m.to_translation()
    pb.matrix = Matrix.Translation(h) @ q @ Matrix.Translation(-h) @ m


def _world(k, name, tail=False):
    bpy.context.view_layer.update()
    pb = _bone(k, name)
    return k["arm"].matrix_world @ (pb.tail if tail else pb.head)


def _pose(k, spec, loc, rot=(0, 0, 0)):
    """Place the armature and pose it. spec: [(bone, direction in Kai's own frame: +Y forward, +Z up, +X his
    right)], applied in order (parents first). The model itself faces -Y, so it gets a half turn on top (the VRM
    import leaves the armature in quaternion mode, where rotation_euler does nothing: switch it to XYZ)."""
    arm = k["arm"]
    r = Euler(rot).to_matrix()
    arm.rotation_mode = "XYZ"
    arm.location = loc
    arm.rotation_euler = (r @ Matrix.Rotation(math.pi, 3, "Z")).to_euler()
    _reset(k)
    for name, d in spec:
        _aim(k, name, r @ Vector(d))


def _key_pose(k, frame):
    """Remember the current pose for `frame`. The keys go in at the end (_flush_keys): once the armature has an
    action, every depsgraph update re-applies it and would overwrite the pose being built."""
    arm = k["arm"]
    k.setdefault("rec", []).append((frame, arm.location.copy(), arm.rotation_euler.copy(),
                                    {pb.name: pb.rotation_quaternion.copy() for pb in arm.pose.bones}))


def _flush_keys(k):
    """Insert every remembered pose as CONSTANT keys (Kai acts on 3s/2s: poses snap)."""
    from channels.monsters.mk import anim
    arm = k["arm"]
    for frame, loc, rot, quats in k.get("rec", []):
        arm.location, arm.rotation_euler = loc, rot
        arm.keyframe_insert("location", frame=frame)
        arm.keyframe_insert("rotation_euler", frame=frame)
        for pb in arm.pose.bones:
            pb.rotation_quaternion = quats[pb.name]
            pb.keyframe_insert("rotation_quaternion", frame=frame)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


KNEEL = [("spine", (0, 0.72, 0.7)), ("chest", (0, 0.8, 0.6)), ("upper_chest", (0, 0.8, 0.6)),
         ("neck", (0, 0.5, 0.87)), ("head", (0, 0.3, 0.95)),
         ("left_upper_leg", (-0.05, 0.12, -1)), ("right_upper_leg", (0.05, 0.12, -1)),
         ("left_lower_leg", (0, -1, -0.04)), ("right_lower_leg", (0, -1, -0.04)),
         ("left_foot", (0, -1, -0.05)), ("right_foot", (0, -1, -0.05)),
         ("left_upper_arm", (-0.2, 0.35, -1)), ("left_lower_arm", (-0.05, 0.45, -1)),
         ("left_hand", (0, 1, -0.4))]


def _apply_kneel(k, loc, s, target):
    """On his knees, leaning in, the right hand reaching toward `target` (s: 0 = hand drawn back, 1 = reached)."""
    _pose(k, KNEEL, loc)
    sh = _world(k, "right_upper_arm")
    t = Vector(target)
    d = (t - sh).normalized()
    bend = (1 - s) * 0.55
    _aim(k, "right_upper_arm", (d + Vector((0.25 * (1 - s), -0.3 * (1 - s), -bend))).normalized())
    el = _world(k, "right_lower_arm")
    _aim(k, "right_lower_arm", (t - el).normalized() + Vector((0, 0, 0.25 * (1 - s))))
    _aim(k, "right_hand", (t - el).normalized() + Vector((0, 0, -0.15)))
    low = min(_world(k, "left_lower_leg").z, _world(k, "right_lower_leg").z,
              _world(k, "left_foot", True).z, _world(k, "right_foot", True).z)
    k["arm"].location.z -= low - 0.3


BLOWN = [("spine", (0, -0.35, 1)), ("chest", (0, -0.45, 1)), ("upper_chest", (0, -0.45, 1)),
         ("neck", (0, -0.7, 1)), ("head", (0, -0.8, 1)),
         ("left_upper_arm", (-0.45, 0.75, 0.55)), ("right_upper_arm", (0.45, 0.75, 0.55)),
         ("left_lower_arm", (-0.3, 0.85, 0.5)), ("right_lower_arm", (0.3, 0.85, 0.5)),
         ("left_upper_leg", (-0.2, 0.8, -0.55)), ("right_upper_leg", (0.15, 0.75, -0.6)),
         ("left_lower_leg", (-0.1, 0.45, -0.9)), ("right_lower_leg", (0.1, 0.3, -0.95)),
         ("left_foot", (0, 1, 0.3)), ("right_foot", (0, 1, 0.3))]

LYING = [("spine", (0, 0, 1)), ("chest", (0, 0, 1)), ("upper_chest", (0, 0, 1)), ("neck", (0, 0.1, 1)),
         ("head", (0, 0.15, 1)),
         ("left_upper_arm", (-1, 0.05, 0.35)), ("right_upper_arm", (1, 0.05, 0.25)),
         ("left_lower_arm", (-0.9, 0.1, 0.6)), ("right_lower_arm", (1, 0.1, 0.45)),
         ("left_upper_leg", (-0.12, 0, -1)), ("right_upper_leg", (0.15, 0, -1)),
         ("left_lower_leg", (-0.1, 0, -1)), ("right_lower_leg", (0.2, 0, -1)),
         ("left_foot", (-0.2, 1, -0.2)), ("right_foot", (0.25, 1, -0.2))]


def _ground(k):
    """Lift or lower the armature so his lowest mesh point rests on the grass."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    low = min((o.evaluated_get(dg).matrix_world @ Vector(c)).z for o in k["arm"].children
              if o.type == "MESH" for c in o.evaluated_get(dg).bound_box)
    k["arm"].location.z -= low - 0.02


# ---------------------------------------------------------------- the shot

def _cam(name, loc, tgt, lens, frame, sc):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    d = [tgt[i] - loc[i] for i in range(3)]
    c.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    c.data.lens = lens
    c.data.clip_start = 0.05
    c.data.clip_end = 2000
    c.data.dof.use_dof = True
    c.data.dof.focus_distance = math.dist(loc, tgt)
    c.data.dof.aperture_fstop = 0.15                           # anime-strength background blur
    mk = sc.timeline_markers.new(name, frame=frame)
    mk.camera = c
    if frame == 1:
        sc.camera = c
    return c


def _shake(cam, f0, frames, seed=3):
    """The observer shake on 2s (IM5): from ~30% of the frame width at the subject to ~1%, over `frames`."""
    from channels.monsters.mk import anim
    rnd = random.Random(seed)
    bpy.context.view_layer.update()
    base = cam.location.copy()
    dist = cam.data.dof.focus_distance
    width = dist * (36.0 * 9 / 16) / cam.data.lens               # 9:16 frame, the sensor fits the height
    right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    up = cam.matrix_world.to_3x3() @ Vector((0, 1, 0))
    anim.key(cam, "location", f0 - 1, base, "CONSTANT")
    sign = 1
    for i in range(0, frames, 2):
        a = 0.3 * (0.01 / 0.3) ** (i / frames) * width
        off = right * a * sign * rnd.uniform(0.7, 1.0) + up * a * rnd.uniform(-0.45, 0.45)
        anim.key(cam, "location", f0 + i, base + off, "CONSTANT")
        sign = -sign
    anim.key(cam, "location", f0 + frames, base, "CONSTANT")


def _claw_pt(lowest=True):
    bpy.context.view_layer.update()
    claw = bpy.data.objects["puff_claw"]
    dg = bpy.context.evaluated_depsgraph_get()
    ev = claw.evaluated_get(dg)
    vs = [ev.matrix_world @ v.co for v in ev.data.vertices]
    if lowest:
        return min(vs, key=lambda v: v.z)
    return sum(vs, Vector()) / len(vs)


def _puff_smoke(sources, f1, size=1.0, seed=4):
    """Painted smoke curling up off the hot stumps once their tree is gone (sources: [(x, y, z, first_frame)])."""
    from channels.monsters.mk import anim, meadow
    rnd = random.Random(seed)
    m = meadow.smoke_mat()
    for (x, y, z, f) in sources:
        f += rnd.randint(2, 8)
        while f < f1:
            life = rnd.randint(26, 36)
            p = bpy.data.objects.new("hotsmoke", None)
            bpy.context.scene.collection.objects.link(p)
            for _ in range(3):
                bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=7, radius=rnd.uniform(0.5, 0.8),
                                                     location=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.2, 0.2),
                                                               rnd.uniform(-0.1, 0.4)))
                lobe = bpy.context.object
                lobe.data.materials.append(m)
                for pg in lobe.data.polygons:
                    pg.use_smooth = True
                lobe.parent = p
            s = rnd.uniform(0.45, 0.75) * size
            anim.key(p, "scale", f - 1, 0.001, "CONSTANT")
            anim.key(p, "location", f, (x, y, z))
            anim.key(p, "scale", f, s * 0.3, "LINEAR")
            anim.key(p, "scale", f + life * 0.6, s)
            anim.key(p, "scale", f + life, 0.001)
            anim.key(p, "location", f + life, (x + rnd.uniform(-0.3, 0.3) * size, y, z + rnd.uniform(2.2, 3.2) * size))
            f += rnd.randint(9, 14)


def s15():
    from channels.monsters.mk import anim, erase, hero, meadow, puffshrimp
    sc = bpy.context.scene
    n = END + HANDLE
    m = meadow.build("before")
    # the "after" stumps (sliced, glowing cuts) at the same spots, hidden until their tree pops
    before = set(bpy.data.objects)
    stumps, hot = meadow._stumps(meadow._wall_spots())
    made = [o for o in bpy.data.objects if o not in before]
    fan = bpy.data.objects["scorched_fan"]
    under = [o for o in made if o.parent is None and o.name.startswith("stump") and o not in stumps]

    # ---- the puff-shrimp at the puddle, its claw dipped in the water
    rig = puffshrimp.build((0, 0, 0))
    root, body, sh, hg = rig["root"], rig["body"], rig["shoulder"], rig["hinge"]
    DIP, UP, STRIKE = (1.8, 0.0, 0.3), (0.35, 0.75, 0.0), (-0.45, 0.55, 0.0)   # DIP: tip in the puddle's edge
    anim.key(sh, "rotation_euler", A, DIP, "CONSTANT")
    anim.key(hg, "rotation_euler", A, (0.1, 0, 0), "CONSTANT")
    anim.key(root, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    anim.key(body, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    for f in range(A, B, 6):                                   # a gentle drinking bob on 3s
        anim.squash(body, f, -0.03, "CONSTANT")
        anim.squash(body, f + 3, 0.0, "CONSTANT")
    anim.key(root, "rotation_euler", 13, (0, 0, 0.18), "CONSTANT")   # it notices the hand: turns and looks up
    anim.key(body, "rotation_euler", 13, (-0.14, 0, 0), "CONSTANT")
    for e in rig["eyes"]:
        anim.key(e, "scale", A, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 7, (1.1, 1, 0.1), "CONSTANT")    # a blink
        anim.key(e, "scale", 8, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", B + 1, (1.12, 1, 0.55), "CONSTANT")   # the eyes narrow (B), and stay narrowed
    # C: the claw rises out of the puddle on 2s, then is held while only the drops move
    for j, f in enumerate(range(C, C + 8, 2)):
        u = (j + 1) / 4
        anim.key(sh, "rotation_euler", f, tuple(a + (b - a) * u for a, b in zip(DIP, UP)), "CONSTANT")
    anim.key(hg, "rotation_euler", C + 6, (0.5, 0, 0), "CONSTANT")    # the finger cocks wide open
    anim.squash(body, C, 0.0, "CONSTANT")
    anim.squash(body, C + 6, -0.06, "CONSTANT")
    # D: the strike, then the result is held
    anim.key(sh, "rotation_euler", D, STRIKE, "CONSTANT")
    anim.key(hg, "rotation_euler", D, (-0.25, 0, 0), "CONSTANT")
    anim.squash(body, D, 0.14, "CONSTANT")
    anim.squash(body, D + 2, -0.04, "CONSTANT")
    anim.squash(body, E + 3, 0.0, "CONSTANT")
    sc.frame_set(C + 7)
    drip = _claw_pt()
    meadow.drips((drip.x, drip.y, drip.z - 0.05), C + 3, D, every=5, fall=max(0.3, drip.z - 0.02))
    sc.frame_set(D + 1)
    blast = _claw_pt(lowest=False)
    for k in range(3):                                         # steam curling off the claw after the snap
        p0 = (blast.x + 0.1 * k, blast.y, blast.z + 0.4)
        o = erase._sphere(f"clawsteam{k}", p0, 1.0, erase._paint("erase_dust", erase.DUST), 12)
        f = E + 2 + k * 5
        anim.key(o, "scale", f - 1, 0.0, "CONSTANT")
        anim.key(o, "location", f, p0)
        anim.key(o, "scale", f, 0.12)
        anim.key(o, "scale", f + 10, 0.3)
        anim.key(o, "scale", f + 22, 0.0)
        anim.key(o, "location", f + 22, (p0[0] + 0.3, p0[1] + 0.2, p0[2] + 1.6))
        erase._twos_from(o, f)

    # ---- Kai, on his knees in front of the puddle
    k = hero.load((0, 0, 0), scale=KAI_SCALE, outfit="world")
    reach = Vector((0.25, -1.45, 2.05))
    loc = Vector((-0.45, -6.4, 0))
    for _ in range(3):                                         # slide him so the reached arm is nearly straight
        _apply_kneel(k, loc, 1.0, reach)
        d = (reach - _world(k, "right_upper_arm")).length
        loc.y += d - 2.55
    for f, s in ((A, 0.0), (A + 3, 0.2), (A + 6, 0.45), (A + 9, 0.7), (A + 12, 0.9), (A + 15, 1.0)):
        _apply_kneel(k, loc, s, reach + (1 - s) * Vector((0.3, -1.6, 1.3)))    # drawn back, then reaching
        _key_pose(k, f)
    hero.face(k, "relaxed", A, 0.6)
    arm = k["arm"]
    held = [o for o in bpy.data.objects                        # the cap, its K and the shoes follow by constraints
            if any(getattr(c, "target", None) == arm for c in o.constraints)]
    for o in set(arm.children_recursive) | set(held) | set(k.get("cap", [])):   # off screen in B-D
        if o.type == "MESH":
            o.hide_render = False
            o.keyframe_insert("hide_render", frame=A)
            o.hide_render = True
            o.keyframe_insert("hide_render", frame=B)
            o.hide_render = False
            o.keyframe_insert("hide_render", frame=E)
    # A: low, beside his reaching arm: the hand comes in from the top of frame toward the shrimp's face
    _cam("S15_A_reach", (1.7, -3.9, 1.05), (0.0, -0.4, 1.45), 30, A, sc)
    sc.frame_set(B + 1)
    bpy.context.view_layer.update()
    ec = sum((e.matrix_world.translation for e in rig["eyes"]), Vector()) / 2
    cam_b = _cam("S15_B_eyes", tuple(ec + Vector((0.0, -1.55, 0.05))), tuple(ec), 30, B, sc)
    cam_b.data.dof.aperture_fstop = 1.0
    cam_c = _cam("S15_C_claw", (-3.6, -5.6, 1.15), (-0.55, 0.0, 2.1), 32, C, sc)
    # E: low behind Kai, who kneels small in the foreground; the shrimp; the forest wall towering behind (SG8, SG9)
    cam_e = _cam("S15_E_result", (loc.x + 4.5, loc.y - 15.0, 1.1), (-0.5, 26.0, 13.0), 22, E, sc)

    # ---- E: the ring, the forest wall sliced and erased, held
    fx = erase.erase_trees(m["trees"], origin=tuple(blast), f0=E - 1, cam=cam_e, stumps=stumps)
    if fx["flash"] is not None:                                 # the 2D pass has the flash
        bpy.data.objects.remove(fx["flash"], do_unlink=True)
    spd, ox, oy = fx["speed"], blast.x, blast.y
    for o in under:                                            # the sliced undergrowth appears as the ring passes
        tp = E - 1 + max(2, round(math.hypot(o.location.x - ox, o.location.y - oy) / spd))
        anim.key(o, "scale", E - 2, 0.0, "CONSTANT")
        anim.key(o, "scale", tp, 1.0, "CONSTANT")
    # the scorched fan spreads with the ring: move its origin to the blast and grow it
    fan.data.transform(Matrix.Translation(fan.location - Vector((ox, oy, fan.location.z))) @
                       Matrix.Diagonal((*fan.scale, 1.0)).to_4x4())
    fan.location, fan.scale = (ox, oy, fan.location.z), (1, 1, 1)
    anim.key(fan, "scale", E - 2, 0.0, "CONSTANT")
    for f in range(E - 1, E + 15):
        anim.key(fan, "scale", f, min(1.0, (f - E + 2) / 15), "LINEAR")
    hot_frames = {}
    for i, st in enumerate(stumps):
        hot_frames[(round(st.location.x, 3), round(st.location.y, 3))] = fx["pop_frames"][i]
    _puff_smoke([(x, y, z, hot_frames.get((round(x, 3), round(y, 3)), E + 10)) for (x, y, z) in hot[:7]], n + 1,
                size=meadow.TREE * 0.6)

    # ---- F: Kai blown backwards (on 2s), G: on his back, shocked, the shake, his eyes close
    y0 = loc.y
    path = [(F, 0.4, 0.15), (F + 2, 1.6, 0.35), (F + 4, 3.0, 0.55), (F + 6, 4.2, 0.75), (F + 8, 5.4, 0.9),
            (F + 10, 6.6, 1.0)]
    for f, back, tilt in path:
        u = (f - F) / 10
        _pose(k, BLOWN, (loc.x, y0 - back * 1.6, 1.0 + 7.0 * u * (1 - u) * 1.6), (tilt, 0, 0))
        _key_pose(k, f)
    hero.face(k, "surprised", F)
    land = Vector((loc.x + 0.4, y0 - 12.5, 0))
    _pose(k, LYING, tuple(land), (math.pi / 2, 0, 0.12))
    _ground(k)
    _key_pose(k, G)
    hero.face(k, "surprised", G)
    hero.face(k, "blink", END - 4, 0.5)                       # his eyes fall shut (into S16's "When I opened my eyes")
    hero.face(k, "blink", END - 2)
    fly = Vector((loc.x, y0 - 4.5, 4.2))
    _cam("S15_F_blown", (fly.x + 17, fly.y + 0.5, 4.0), tuple(fly), 24, F, sc)
    face = (_world(k, "head") + _world(k, "head", True)) / 2 + Vector((0, 0, 0.35))
    cam_g = _cam("S15_G_shock", (face.x + 0.3, face.y + 1.7, face.z + 3.1), tuple(face), 42, G, sc)
    cam_g.data.dof.aperture_fstop = 1.2
    _shake(cam_g, G, 14)
    _flush_keys(k)

    cam_c.data.dof.focus_distance = math.dist(cam_c.location, (0, 0, 1.4))
    cam_e.data.dof.focus_distance = math.dist(cam_e.location, (0, 24.0, 10.0))   # the result: the forest wall
    cam_e.data.dof.aperture_fstop = 0.9
    return dict(frames=n, step=1, subject=[root])


SHOTS = {"S15": s15}


# ---------------------------------------------------------------- the 2D pass and delivery (outside Blender)

def composite(raw, sub, out_dir):
    """raw: the Blender frames; sub: a render of frames IMPACT..IMPACT+3 with --subject. Adds the 2-frame flash and
    the 4 impact frames on 2s, writes S15.mp4 and S15_sheet.jpg to out_dir."""
    import glob
    import shutil
    import subprocess
    import tempfile

    os.environ.setdefault("FPS", "24")
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    sys.path.insert(0, root)
    import cv2
    import numpy as np
    from channels.monsters import comp

    frames = sorted(glob.glob(os.path.join(raw, "[0-9]*.png")))
    work = tempfile.mkdtemp(prefix="s15_")
    os.makedirs(os.path.join(work, "subject"))
    blank = np.zeros((1280, 720, 4), np.uint8)
    for f in frames:                                           # the subject pass, blank outside the impact frames
        name = os.path.basename(f)
        shutil.copyfile(f, os.path.join(work, name))
        s = os.path.join(sub, "subject", name)
        if os.path.exists(s):
            shutil.copyfile(s, os.path.join(work, "subject", name))
        else:
            cv2.imwrite(os.path.join(work, "subject", name), blank)

    def flash(cr, t, start):
        k = int(math.floor((t - start) * FPS + 1e-6))
        if 0 <= k < 2:
            cr.set_source_rgba(1, 1, 1, (1.0, 0.7)[k])
            cr.paint()

    def impact_2s(cr, t, start, ctx=None):
        k = int(math.floor((t - start) * FPS + 1e-6))
        if 0 <= k < 4:                                         # A A B B (IM4)
            comp.impact(cr, start + (k // 2) / FPS + 1e-4, start, frames=2, ctx=ctx, seed=k // 2)

    src = comp.Source(work)
    shot = comp.Shot(src, src.duration, [(flash, dict(start=(FLASH - 1) / FPS)),
                                         (impact_2s, dict(start=(IMPACT - 1) / FPS))], name="S15")
    done = os.path.join(work, "out")
    comp.render([shot], done, check=False)
    os.makedirs(out_dir, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(done, "%05d.png"),
                    "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p",
                    os.path.join(out_dir, "S15.mp4")], check=True)
    outs = sorted(glob.glob(os.path.join(done, "*.png")))
    picks = outs[::6]
    cols = 6
    th = [cv2.resize(cv2.imread(p), (180, 320)) for p in picks]
    th += [np.zeros_like(th[0])] * (-len(th) % cols)
    rows = [np.hstack(th[i:i + cols]) for i in range(0, len(th), cols)]
    cv2.imwrite(os.path.join(out_dir, "S15_sheet.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
    return done


if __name__ == "__main__" and bpy is None:
    print(composite(sys.argv[1], sys.argv[2], sys.argv[3]))
