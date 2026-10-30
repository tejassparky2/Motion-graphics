"""Episode 1 (v2) shots by helper 2 (the pistol shrimp in the lab's hero tank): S04, S05a, S07.
See channels/monsters/EP01V2_SHOTS.md and the 9-step hit in reports/Pokémon episodes story and animation.md (IM1).

The shrimp (mk/pistolshrimp.py) stands on the gravel of lab.build()'s hero tank at 1/40 scale (~6 cm body, real
metres), so these close-ups match helper 1's wide lab shots. S04 and S05a are one continuous slow-motion snap, cut
at SPLIT; each shot carries a 12-frame tail handle.

    S04  "Its claw snaps so fast, the water boils."  eye close-up 4f -> claw cocked and HELD while only a glint grows
         (tiny bubbles are drawn into the claw) -> a 4-frame slow-motion shut -> 2-frame flash -> the bubble swells
         white-hot for the rest of the shot (IM13's long quiet scale shot), a slow shock ring spreading.
    S05a "Almost as hot as the surface of the sun."  the bubble at its peak, shimmering -> it shrinks, brightens and collapses (2-frame
         flash) -> micro-bubbles drift up in the dark water.
    S07  "Snap."  eye close-up 2f -> claw cocked, held, glint growing -> shut in 2 frames -> 1-frame flash -> 2 impact
         frames (comp.impact from the subject pass) -> the crack runs up the glass in 5 frames; the shrimp is frozen in
         its snapped pose, the camera drifts. The crack is pistolshrimp.crack_path(), the same zigzag as the lab's
         crack_puddle and the cracked sky of S09.
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.mk import anim, lab, look
from channels.monsters.mk import pistolshrimp as ps

K = 0.025                     # shrimp scale in the metre-scale lab (~6 cm body)
TURN = math.radians(45)       # the claw points at the front glass, near the leak
TAIL = 12                     # handle frames after every shot
LEN = dict(S04=61, S05a=63, S07=24)     # frames in the cut (ep01v2/TIMING.md, v7); +TAIL when rendered
SPLIT = LEN["S04"]            # S05a starts at sequence frame SPLIT + 1 of the S04/S05a snap
FSTOP = 0.3 / K               # the anime background blur at this scale (f/0.3 at unit scale)


def _stage():
    """The lab, and the shrimp on the hero tank's gravel. The scene was already set up by render_shot.py. For these
    close-ups the tank floor gets the painted sand and pebbles of mk/pistolshrimp.py's own tank at shrimp scale (the
    lab's sand box reads as a flat white plane this close)."""
    h = lab.build()
    tank = h["hero_tank"]
    fx, fy, fz = tank["floor"]
    rig = ps.build((fx - 0.03, fy - 0.07, fz), turn=TURN, scale=K)
    gy = tank["glass"].location.y
    sand_m = look.paint("tank_sand", look.hexc("#d9c39a"), noise=0.18, scale=220.0)
    bpy.data.objects["hero_gravel"].data.materials[0] = sand_m       # its front face showed white through the glass
    bpy.ops.mesh.primitive_plane_add(size=1, location=(fx, (gy + fy + 0.15) / 2, fz + 0.0004))
    sand = bpy.context.object
    sand.name = "h2_sand"
    sand.scale = (0.52, fy + 0.15 - gy - 0.004, 1)
    sand.data.materials.append(sand_m)
    ps.gravel_bed((fx - 0.25, fx + 0.25), (gy + 0.004, fy + 0.14), fz, random.Random(5), n=1600, k=K * 1.6,
                  clear=(fx - 0.03, fy - 0.07, 0.05, 0.03), name="h2_gravel")
    return h, tank, rig


def _dim_water(tank, keys):
    """Darken the hero tank's water (fear is darkness, LC2; the glow reads against it): keys = [(frame, level)]."""
    for m in tank["water"]:
        em = m.node_tree.nodes["Emission"].inputs[1]
        base = em.default_value
        for f, lv in keys:
            em.default_value = base * lv
            em.keyframe_insert("default_value", frame=f)
        em.default_value = base


FLOOR0 = Vector((0.10, 2.23, 0.785))   # the hero tank floor the camera positions below were set against


def _at(tank, p):
    """A position set against FLOOR0, moved with the hero tank (lab.py may move the tank)."""
    return Vector(p) + (Vector(tank["floor"]) - FLOOR0)


def _cam(name, loc, target, lens, focus=None, fstop=FSTOP):
    cam = ps._camera(name, loc, target, lens, focus, fstop)
    cam.data.clip_start, cam.data.clip_end = 0.002, 40.0
    return cam


def _bind(cams):
    """Cut between cameras inside a shot with timeline markers: cams = [(frame, camera), ...]."""
    sc = bpy.context.scene
    for f, cam in cams:
        m = sc.timeline_markers.new(f"cam_{f}", frame=f)
        m.camera = cam
    sc.camera = cams[0][1]


def _eye_cam(rig, name):
    """A tight eye close-up from the camera side of the head."""
    eye = rig["eyes"][0].matrix_world.translation.copy()
    face = (rig["root"].matrix_world.to_quaternion() @ Vector((0.25, -1.0, 0.12))).normalized()
    return _cam(name, eye + face * 0.07, eye, 95, rig["eyes"][0], FSTOP * 2.5)


def _flash(cam, keys):
    """A white plane just in front of the camera; keys = [(frame, alpha), ...] (CONSTANT: anime flashes pop)."""
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    p = bpy.context.object
    p.name = f"flash_{cam.name}"
    p.parent = cam
    p.location = (0, 0, -0.01)
    p.scale = (0.05, 0.05, 1)
    m = look.fade(f"flash_m_{cam.name}", look.hexc("#f6fdff"), 0.0)
    p.data.materials.append(m)
    p.visible_shadow = False
    mix = m.node_tree.nodes["Mix"]
    for f, a in keys:
        mix.inputs[0].default_value = a
        mix.inputs[0].keyframe_insert("default_value", frame=f)
    for fc in anim.all_fcurves(m.node_tree.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    return p


def _charge(rig, f0, f1, seed=4):
    """The wind-up's only motion (IM2): a cold glint swelling at the claw tip and tiny bubbles drawn into the claw."""
    k = rig["k"]
    tip, d = ps._jet(rig, f0)
    pos = tip + d * 0.1 * k
    m1 = ps._glow("charge_core", look.hexc("#f4fdff"), 0.9)
    m2 = ps._glow("charge_halo", look.hexc("#8fd8ff"), 0.35)
    for name, m, r in (("charge_core", m1, 1.0), ("charge_halo", m2, 2.4)):
        o = ps._sphere(name, pos, (1, 1, 1), m, 0, 20)
        o.visible_shadow = False
        anim.key(o, "scale", f0 - 1, 0.0001, "CONSTANT")
        anim.key(o, "scale", f0, 0.02 * k * r, "LINEAR")
        n = f0
        while n < f1:                                  # grows with a nervous flicker on 1s
            g = 0.03 + 0.13 * (n - f0) / max(1, f1 - f0)
            anim.key(o, "scale", n, g * k * r * (1.0 if (n - f0) % 2 == 0 else 0.86), "LINEAR")
            n += 1
        anim.key(o, "scale", f1, 0.17 * k * r, "LINEAR")
        anim.key(o, "scale", f1 + 1, 0.0001, "CONSTANT")
    rnd = random.Random(seed)
    bm = look.fade("charge_bub", look.hexc("#f2fdff"), 0.65)
    for i in range(8):
        a, b = rnd.uniform(0, 2 * math.pi), rnd.uniform(-0.6, 0.6)
        far = pos + Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))) * rnd.uniform(0.6, 1.0) * k
        o = ps._sphere(f"charge_bub{i}", far, (1, 1, 1), bm, 0, 10)
        o.visible_shadow = False
        s = rnd.uniform(0.02, 0.035) * k
        start = f0 + int((f1 - f0 - 6) * i / 8)
        anim.key(o, "scale", f0 - 1, 0.0001, "CONSTANT")
        anim.key(o, "scale", start, s, "CONSTANT")
        anim.key(o, "location", start, far, "LINEAR")
        anim.key(o, "location", start + 7, pos, "CONSTANT")
        anim.key(o, "scale", start + 7, 0.0001, "CONSTANT")


def _freeze_pose(rig, f, hinge):
    """Hold everything at f (the body is frozen through the wind-up: only the effect moves, IM2)."""
    anim.key(rig["hinge"], "rotation_euler", f, (0, hinge, 0))
    anim.key(rig["shoulder"], "rotation_euler", f, (0, -0.08, 0.1))
    anim.key(rig["tail"], "rotation_euler", f, (0, 0.0, 0))
    anim.squash(rig["body"], f, -0.03)
    for i, a in enumerate(rig["antennae"]):
        anim.key(a, "rotation_euler", f, (0.2 * (-1) ** i, -0.2, 0.08 * (-1) ** i))


def _pulse(objs, f0, f1, amount=0.18):
    """The peak bubble's shimmer: its glow shells breathe in alpha on 2s."""
    for o in objs:
        m = o.data.materials[0]
        mix = m.node_tree.nodes.get("Mix")
        if mix is None:
            continue
        a = mix.inputs[0].default_value
        base = sorted((kp.co.x, kp.co.y) for fc in anim.all_fcurves(m.node_tree.animation_data.action)
                      for kp in fc.keyframe_points)
        a = next((v for _, v in base if v > 0), a)                # the alpha it was born with
        for n in range(f0, f1, 2):
            mix.inputs[0].default_value = min(1.0, a * (1 + amount if (n - f0) % 4 == 0 else 1 - amount * 0.5))
            mix.inputs[0].keyframe_insert("default_value", frame=n)


def _snap_sequence(offset):
    """The S04 + S05a slow-motion snap as one continuous action; `offset` shifts it so S05a can start at frame 1
    (sequence frame s renders at frame s - offset)."""
    def F(s):
        return s - offset

    h, tank, rig = _stage()
    _freeze_pose(rig, F(1), ps.OPEN)
    # S04's words, in shot frames: "snaps" 15-21 (the strike), "boils" 44-50 (the bubble reaches its peak)
    _freeze_pose(rig, F(15), ps.OPEN)
    _charge(rig, F(5), F(15))
    anim.key(rig["hinge"], "rotation_euler", F(15), (0, ps.OPEN, 0), "LINEAR")
    anim.key(rig["hinge"], "rotation_euler", F(19), (0, 0.0, 0), "CONSTANT")      # 4-frame slow-motion strike
    anim.key(rig["shoulder"], "rotation_euler", F(19), (0, 0.05, -0.06))
    anim.key(rig["body"], "location", F(19), (0, 0, 0))
    anim.key(rig["body"], "location", F(35), (0.08, 0, 0.01))                    # a slow recoil
    anim.key(rig["tail"], "rotation_euler", F(19), (0, 0.0, 0))
    anim.key(rig["tail"], "rotation_euler", F(33), (0, 0.35, 0))
    anim.on_twos([rig["body"], rig["tail"], rig["shoulder"], *rig["antennae"]], step=2)
    # the bubble: born at the shut, swells to 3x through S04, held shimmering, then collapses in S05a
    # born on the flash (20), peak on "boils" (48); held through S05a, collapsing on "sun" (S05a frame 52)
    b = ps.bubble(rig, F(20), t=(0, 28, 88, 93, 94, 100, 110), peak_scale=1.6)
    layers = [o for o in b.children if "_core" in o.name or "_glow" in o.name]
    for o in layers:                                   # hold the peak until sequence frame 84
        fc = [c for c in anim.all_fcurves(o.animation_data.action) if c.data_path == "scale"]
        peak = max(kp.co.y for kp in fc[0].keyframe_points)
        anim.key(o, "scale", F(105), peak)
    _pulse(layers, F(28), F(107))
    ps.shock(rig, F(19), slow=4, radius=1.8)
    _dim_water(tank, [(F(4), 1.0), (F(15), 0.45)])
    ps.bubbles(Vector(tank["floor"]) + Vector((-0.06, -0.02, 0.0)), F(1), F(140), n=6, seed=8, rise=0.3, spread=0.04, size=K)
    cams = dict(
        eye=_eye_cam(rig, "cam_eye"),
        side=_cam("cam_claw", _at(tank, (0.175, 1.998, 0.805)), _at(tank, (0.035, 2.125, 0.80)), 50, rig["hinge"]),
        front=_cam("cam_front", _at(tank, (0.075, 1.90, 0.812)), _at(tank, (0.03, 2.105, 0.80)), 55, rig["tip"]))
    return h, tank, rig, cams, F


def s04():
    h, tank, rig, cams, F = _snap_sequence(0)
    _bind([(1, cams["eye"]), (5, cams["side"])])
    _flash(cams["side"], [(19, 0.0), (20, 0.9), (21, 0.55), (22, 0.0)])
    return dict(frames=LEN["S04"] + TAIL, step=1, subject=[rig["root"]])


def s05a():
    h, tank, rig, cams, F = _snap_sequence(SPLIT)
    _bind([(1, cams["front"])])
    _flash(cams["front"], [(F(112), 0.0), (F(113), 0.85), (F(114), 0.4), (F(115), 0.0)])   # the collapse's light
    return dict(frames=LEN["S05a"] + TAIL, step=1, subject=[rig["root"]])


# frames inside S07 (1-based): eye insert, wind-up, strike, flash, impact (composited), crack
# "Snap." is at frames 8-13: the shut lands on it, then flash, the 2 impact frames and the 5-frame crack
S07_EYE, S07_WIND, S07_SHUT, S07_FLASH, S07_IMPACT, S07_CRACK = 1, 3, 8, 10, 11, 13


def s07():
    h, tank, rig = _stage()
    ps.reaction(rig, 1, hold=S07_SHUT - 2)             # cocked wide and HELD: only the glint moves
    anim.key(rig["hinge"], "rotation_euler", S07_SHUT - 1, (0, ps.OPEN, 0), "LINEAR")
    anim.key(rig["hinge"], "rotation_euler", S07_SHUT + 1, (0, 0.0, 0), "CONSTANT")
    anim.key(rig["shoulder"], "rotation_euler", S07_SHUT + 1, (0, 0.06, -0.08), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", S07_SHUT + 1, (0, 0.55, 0), "CONSTANT")    # then frozen (IM12)
    _charge(rig, S07_WIND, S07_SHUT - 1)
    ps.bubble(rig, S07_SHUT + 1)
    ps.shock(rig, S07_SHUT + 1, radius=2.2)
    lx, ly, lz = tank["leak"]
    gy = tank["glass"].location.y - 0.006
    gc = ps.glass_crack((lx, gy, lz - 0.005))
    ps.crack(gc, S07_CRACK, frames=5)
    eye = _eye_cam(rig, "cam_eye")
    _dim_water(tank, [(S07_WIND, 1.0), (S07_SHUT, 0.6)])
    cam = _cam("cam_tank", _at(tank, (0.07, 1.90, 0.815)), _at(tank, (0.045, 2.08, 0.86)), 28, None)
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector((lx, gy, lz + 0.12)) - cam.location).length
    cam.data.dof.aperture_fstop = 2.8
    anim.key(cam, "location", S07_CRACK, cam.location.copy(), "LINEAR")          # the final hit drifts (IM5)
    anim.key(cam, "location", LEN["S07"] + TAIL, cam.location + Vector((0.0, 0.012, 0.004)), "LINEAR")
    _bind([(S07_EYE, eye), (S07_WIND, cam)])
    _flash(cam, [(S07_FLASH - 1, 0.0), (S07_FLASH, 0.9), (S07_FLASH + 1, 0.0)])
    return dict(frames=LEN["S07"] + TAIL, step=1, subject=[rig["root"]])


SHOTS = {"S04": s04, "S05a": s05a, "S07": s07}
