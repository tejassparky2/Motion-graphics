"""Episode 1 v2, shot S24 (EP01V2_SHOTS.md): "Save the shrimp that tried to kill me, or run while I can?" Two plates for
the coordinator's top/bottom split with a jagged divider (AB13): A above, B below. Each plate is rendered full frame
(720x1280) with its action framed in the half it will fill, plus slack for the divider.

    S24top  (A, SAVE): Kai steps toward the puff-shrimp at the puddle, its claw dipped and lifted wet again, dripping;
            he crouches and holds out an open hand. Bright day.
    S24bot  (B, RUN):  Kai backs away toward the surviving trees, looking up as the butcher bird drops; its shadow
            sweeps the ground. Graded darker with local light, not a regrade of the frame (LC4, LC8: RUN is riskier).

Set: meadow.build("after") (the crater, the stumps, the small puddle). Kai: mk/hero.load (world outfit, scale 5.8:
1 unit = 20 cm). Acting on 3s (IM2), effects on 1s; locked cameras (SG4). 3.4 s (line 24 is 2.88 s, cut within
0.5 s of its end): 85 frames in the cut plus the 12-frame tail (TIMING.md).

    blender -b -y -P channels/monsters/render_shot.py -- ep01v2 S24top OUTDIR
"""
import math

import bpy
from mathutils import Matrix, Vector

from channels.monsters.mk import anim, hero, look, meadow, puffshrimp, tuftwing

TAIL = 12
CUT_FRAMES = 85                                # ep01v2/TIMING.md: line 24 at 0.30-3.02 s, the cut ~0.5 s after it
SCALE = 5.8                                    # hero.blend is 1.5 m in metres; the creature world is 20 cm per unit
PUDDLE = (-1.3, -0.4)                          # meadow.build("after")
SHRIMP_AT = (-2.95, 0.9, 0.0)                  # facing +X, its claw reaching into the puddle in front of it
LEGS = {"L": ("thigh.L", "shin.L", "foot.L"), "R": ("thigh.R", "shin.R", "foot.R")}
BODY = ["hips", "spine", "chest", "neck", "head 1", "shoulder.L", "shoulder.R", "upper_arm.L", "upper_arm.R",
        "forearm.L", "forearm.R", "hand.L", "hand.R", "thigh.L", "thigh.R", "shin.L", "shin.R", "foot.L", "foot.R"]


def _frames():
    return CUT_FRAMES + TAIL                   # 97 to render


def _hero(loc, rot_z_deg):
    """hero.load's rot_z sets rotation_euler on an armature in QUATERNION mode, so it doesn't turn him: turn him
    here."""
    k = hero.load((0, 0, 0), scale=SCALE)
    k["arm"].rotation_mode = "XYZ"
    k["arm"].rotation_euler = (0, 0, math.radians(rot_z_deg))
    k["arm"].location = loc
    bpy.context.view_layer.update()
    return k


def _cam(name, loc, target, lens, shift_y=0.0, fstop=None, focus=None):
    bpy.ops.object.camera_add(location=loc)
    c = bpy.context.object
    c.name = name
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    c.data.shift_y = shift_y
    c.data.clip_end = 2000                    # the true-scale meadow (HELPERS.md v6)
    if fstop:
        c.data.dof.use_dof = True
        c.data.dof.aperture_fstop = fstop
        c.data.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    bpy.context.scene.camera = c
    return c


# ------------------------------------------------------------------------------------------------- posing the hero
class Pose:
    """FK posing for the hero's armature in its own space (forward -Y, his left +X), with analytic two-bone leg IK so
    planted feet stay put while the body moves."""

    def __init__(self, rig):
        self.arm = rig["arm"]
        self.pb = self.arm.pose.bones
        b = self.arm.data.bones
        self.l1 = (b["thigh.L"].tail_local - b["thigh.L"].head_local).length
        self.l2 = (b["shin.L"].tail_local - b["shin.L"].head_local).length
        self.ankle_h = b["foot.L"].head_local.z         # ankle height above the sole in armature units

    def reset(self):
        for p in self.pb:
            p.rotation_mode = "QUATERNION"
            p.rotation_quaternion = (1, 0, 0, 0)
            p.location = (0, 0, 0)
        bpy.context.view_layer.update()

    def _set(self, name, M):
        self.pb[name].matrix = M
        bpy.context.view_layer.update()

    def rot(self, name, deg):
        """Turn a bone about the character axes (x: bend forward, y: tilt, z: turn to his left), on top of its pose."""
        p = self.pb[name]
        bpy.context.view_layer.update()
        M = p.matrix.copy()
        h = M.translation.copy()
        R = Matrix.Rotation(math.radians(deg[2]), 4, "Z") @ Matrix.Rotation(math.radians(deg[1]), 4, "Y") @ \
            Matrix.Rotation(math.radians(deg[0]), 4, "X")
        self._set(name, Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M)

    def aim(self, name, direction):
        """Point a bone along `direction` (armature space), turning it by the smallest rotation."""
        p = self.pb[name]
        bpy.context.view_layer.update()
        M = p.matrix.copy()
        h = M.translation.copy()
        cur = (M.to_3x3() @ Vector((0, 1, 0))).normalized()
        R = cur.rotation_difference(Vector(direction).normalized()).to_matrix().to_4x4()
        self._set(name, Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M)

    def hips(self, offset):
        """Move the hips (the whole upper body and the leg roots) by `offset` in armature space."""
        p = self.pb["hips"]
        bpy.context.view_layer.update()
        M = p.matrix.copy()
        M.translation = M.translation + Vector(offset)
        self._set("hips", M)

    def leg(self, side, ankle):
        """Two-bone IK: put the ankle of leg `side` at `ankle` (armature space), knee bending forward (-Y)."""
        th, sh, ft = LEGS[side]
        bpy.context.view_layer.update()
        H = self.pb[th].matrix.translation.copy()
        T = Vector(ankle)
        d = min((T - H).length, (self.l1 + self.l2) * 0.999)
        u = (T - H).normalized()
        fwd = Vector((0, -1, 0))
        w = (fwd - fwd.dot(u) * u).normalized()
        cos_a = max(-1.0, min(1.0, (self.l1 ** 2 + d ** 2 - self.l2 ** 2) / (2 * self.l1 * d)))
        K = H + self.l1 * (cos_a * u + math.sqrt(1 - cos_a ** 2) * w)
        self.aim(th, K - H)
        self.aim(sh, H + u * d - K)
        self.aim(ft, (0, -0.93, -0.38))           # foot back to its rest direction: flat on the ground

    def key(self, f):
        for name in BODY:
            p = self.pb[name]
            p.keyframe_insert("rotation_quaternion", frame=f, group=name)
            p.keyframe_insert("location", frame=f, group=name)


def _arms_down(P, spread=12):
    for sx, s in (("L", 1), ("R", -1)):
        P.aim(f"upper_arm.{sx}", (s * math.sin(math.radians(spread)), 0.05, -1))
        P.aim(f"forearm.{sx}", (s * 0.08, -0.15, -1))


def _walk(P, rig, path, f0, f1, step_len, start_foot="R", crouch=(0.0, 0.0), back=False, upper=None, every=3):
    """Walk the hero along `path` (armature space, two points) between frames f0 and f1, in steps of `step_len`
    (armature units), planting each foot (IK) while the other swings. `crouch`: hip drop at the start and the end.
    `upper(P, t)` poses the upper body for progress t in 0..1 on top of the walk. Keys every `every` frames."""
    a, b = Vector(path[0]), Vector(path[1])
    dist = (b - a).length
    n_steps = max(1, round(dist / step_len))
    side_off = {"L": Vector((0.09, 0, 0)), "R": Vector((-0.09, 0, 0))}
    # footholds: each foot's planted positions along the path
    holds = {"L": [a + side_off["L"]], "R": [a + side_off["R"]]}
    order = [start_foot, "L" if start_foot == "R" else "R"]
    for i in range(n_steps):
        foot = order[i % 2]
        t = (i + 1) / n_steps
        holds[foot].append(a + (b - a) * t + side_off[foot])
    other = order[1]
    holds[other].append(b + side_off[other])          # the trailing foot closes up at the end
    seq = []                                          # (foot, from, to) per step, one step at a time
    idx = {"L": 0, "R": 0}
    for i in range(n_steps + 1):
        foot = order[i % 2] if i < n_steps else other
        if idx[foot] + 1 >= len(holds[foot]):
            continue
        seq.append((foot, holds[foot][idx[foot]], holds[foot][idx[foot] + 1]))
        idx[foot] += 1
    span = (f1 - f0) / max(1, len(seq))
    for f in range(f0, f1 + 1, every):
        t = (f - f0) / max(1, f1 - f0)
        k = min(len(seq) - 1, int((f - f0) / span))
        s = ((f - f0) - k * span) / span                # progress through the current step
        feet = {}
        for foot in ("L", "R"):
            done = [st for st in seq[:k] if st[0] == foot]
            feet[foot] = done[-1][2] if done else holds[foot][0]
        foot, p0, p1 = seq[k]
        ease = 0.5 - 0.5 * math.cos(math.pi * min(1.0, s))
        swing = p0 + (p1 - p0) * ease
        swing.z += math.sin(math.pi * min(1.0, s)) * 0.06
        feet[foot] = swing
        P.reset()
        mid = (feet["L"] + feet["R"]) / 2
        drop = crouch[0] + (crouch[1] - crouch[0]) * t
        bob = -0.015 * math.sin(math.pi * min(1.0, s))
        P.hips(Vector((mid.x, mid.y, -drop + bob)))     # the pelvis rides above the midpoint of the feet
        for side in ("L", "R"):
            ank = feet[side] + Vector((0, 0, P.ankle_h))
            P.leg(side, ank)
        if upper:
            upper(P, t)
        P.key(f)


# ------------------------------------------------------------------------------------------------------- the shrimp
def _shrimp_wet(f_lift, n):
    """The puff-shrimp at the puddle, facing Kai (+X): its claw dipped, then lifted out wet at f_lift, dripping, held
    up at the ready; a wary lean back and a blink. Acting on 3s; the drops fall on 1s."""
    rig = puffshrimp.build(SHRIMP_AT)
    rig["root"].rotation_euler = (0, 0, math.radians(90))
    sh, body, hinge = rig["shoulder"], rig["body"], rig["hinge"]
    anim.key(sh, "rotation_euler", 1, (1.76, 0, 0))
    anim.key(hinge, "rotation_euler", 1, (0.15, 0, 0))
    anim.squash(body, 1, 0.0)
    for e in rig["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
    if f_lift is None:                                                # still drinking: a slow bob, a blink
        for f in range(1, n + 1, 24):
            anim.squash(body, f, 0.0)
            anim.squash(body, f + 12, -0.03)
        anim.blink(rig, 40)
    else:
        anim.key(sh, "rotation_euler", f_lift, (1.76, 0, 0))
        anim.key(sh, "rotation_euler", f_lift + 9, (0.25, 0, 0))      # out of the water, raised, cocked
        anim.key(sh, "rotation_euler", n, (0.3, 0, 0))
        anim.key(hinge, "rotation_euler", f_lift + 9, (0.45, 0, 0))   # the finger open: armed
        anim.squash(body, f_lift + 6, -0.05)
        anim.squash(body, f_lift + 15, 0.02)
        anim.squash(body, n, 0.0)
        anim.blink(rig, f_lift + 30)
    anim.on_twos([sh, body, hinge] + rig["eyes"], step=3)
    bpy.context.view_layer.update()
    return rig


def _claw_tip(rig, frame):
    """The claw's lowest point at `frame` (where drops fall from), in world space."""
    finger = bpy.data.objects.get("puff_dactyl")
    sc = bpy.context.scene
    sc.frame_set(frame)
    vs = [finger.matrix_world @ v.co for v in finger.data.vertices] if finger else [Vector(SHRIMP_AT)]
    low = min(vs, key=lambda v: v.z)
    sc.frame_set(1)
    return low


# ------------------------------------------------------------------------------------------------------- plates
def s24top():
    """A, SAVE: Kai steps toward the shrimp, crouching, an open hand held out low; the shrimp lifts its claw out of the
    puddle, wet again and dripping, and watches him."""
    n = _frames()
    meadow.build("after")
    shrimp = _shrimp_wet(16, n)
    tip = _claw_tip(shrimp, 28)
    meadow.drips((tip.x, tip.y, tip.z - 0.05), 27, n, every=10, fall=max(0.5, tip.z - 0.05))
    k = _hero((7.5, 0.1, 0), -90)                                        # facing -X, toward the shrimp
    P = Pose(k)
    # armature space: he walks forward (-Y); turned -90 deg, armature -Y is world -X, and 1 armature unit = 5.8
    start, end = Vector((0, 0, 0)), Vector((0, -0.81, 0))                # world x 7.5 -> 2.8, ~60 cm from the claw

    def upper(P, t):
        P.rot("spine", (10 + 14 * t, 0, 0))
        P.rot("chest", (4 + 8 * t, 0, 0))
        P.rot("head 1", (8 + 10 * t, 0, 0))                               # eyes on the shrimp, down low
        _arms_down(P, 10)
        reach = min(1.0, t * 1.3)                                         # an open hand held out, low and slow
        P.aim("upper_arm.R", (-0.15, -0.3 - 0.45 * reach, -1 + 0.45 * reach))
        P.aim("forearm.R", (-0.05, -0.45 - 0.4 * reach, -0.85 + 0.25 * reach))
        P.aim("upper_arm.L", (0.25, 0.1, -1))

    _walk(P, k, (start, end), 1, n - 24, 0.3, "R", crouch=(0.0, 0.12), upper=upper)
    hero.face(k, "neutral", 1)
    hero.face(k, "happy", 52, 0.35)                                       # a small, steady smile as he crouches
    anim.on_twos([k["arm"]], step=3)
    _cam("cam_s24top", (-6.0, -15.5, 1.5), (0.6, 0.6, 3.4), 30, shift_y=-0.22, fstop=1.2, focus=(0.0, 0.0, 2.0))
    return dict(frames=n, step=3, subject=[k["arm"]])


def _bird_drop(f0, f1, n, at):
    """The butcher bird (tuftwing) plunges from above the frame toward the shrimp: wings up, on 2s (fast action), its
    giant shadow sweeping in and swelling on the ground as it comes down."""
    b = tuftwing.build(at)
    b["root"].scale = (0.85, 0.85, 0.85)
    lift, shadow = b["lift"], b["shadow"]
    for f, z in ((1, 16.0), (f0, 16.0), (f0 + 10, 11.0), (f0 + 20, 6.5), (f1, 2.6), (n, 2.2)):
        anim.key(lift, "location", f, (0, 0, z), "LINEAR")
    for f, sc in ((1, 0.35), (f0, 0.35), (f1, 1.0), (n, 1.05)):
        anim.key(shadow, "scale", f, (sc, sc, 1), "LINEAR")
    for i, w in enumerate(b["wings"]):
        side = -1 if i == 0 else 1
        for f, ang in ((1, 1.1), (f0, 1.1), (f0 + 4, 0.5), (f0 + 8, 1.2), (f0 + 12, 0.5), (f1, 1.3)):
            anim.key(w, "rotation_euler", f, (0, -side * ang, 0))
    for e in b["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
    anim.on_twos([lift, shadow] + b["wings"], step=2)
    return b


def s24bot():
    """B, RUN: Kai backs away toward the trees, looking up as the butcher bird drops toward the shrimp, its giant
    shadow sweeping the ground; the sun goes behind cloud (darker, cooler: RUN is the riskier choice, LC8)."""
    n = _frames()
    meadow.build("after")
    _shrimp_wet(None, n)                                                  # still drinking: it hasn't seen the bird
    for o in bpy.data.objects:                                            # the sun goes behind cloud: dimmer, cooler
        if o.type == "LIGHT":
            o.data.energy *= 0.42
            o.data.color = (0.8, 0.86, 1.0)
    w = bpy.context.scene.world
    if w and w.use_nodes:
        for nd in w.node_tree.nodes:
            if nd.type == "BACKGROUND":
                nd.inputs[1].default_value *= 0.6
    _bird_drop(14, 60, n, (SHRIMP_AT[0] + 1.2, SHRIMP_AT[1] - 0.6, 0.0))
    k = _hero((3.6, 0.1, 0), -90)
    P = Pose(k)
    start, end = Vector((0, 0, 0)), Vector((-0.35, 0.45, 0))              # back and to his right: toward the trees

    def upper(P, t):
        P.rot("spine", (-6 - 6 * t, 0, 0))
        P.rot("chest", (-4, 0, 0))
        P.rot("head 1", (-26 - 8 * t, 0, -8))                             # looking up at the bird
        _arms_down(P, 14)
        P.aim("upper_arm.R", (-0.5, -0.45, 0.35 + 0.2 * t))               # an arm up, shielding
        P.aim("forearm.R", (0.3, -0.35, 0.85))
        P.aim("upper_arm.L", (0.55, 0.1, -0.6))

    _walk(P, k, (start, end), 1, n - 24, 0.22, "L", crouch=(0.02, 0.06), upper=upper)
    hero.face(k, "surprised", 1)
    hero.face(k, "shock", 12)
    anim.on_twos([k["arm"]], step=3)
    _cam("cam_s24bot", (-6.5, -17.0, 1.3), (0.4, 0.6, 3.6), 30, shift_y=0.3, fstop=1.2, focus=(1.5, 0.0, 2.5))
    return dict(frames=n, step=2, subject=[k["arm"]])


SHOTS = {"S24top": s24top, "S24bot": s24bot}
