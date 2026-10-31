"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 2: S07, "The shrimp panicked. Its
snap cracked the tank." Close in the hero tank of helper 1's dollhouse lab (mk/diorama_lab.py), as v2's S07
(channels/monsters/diorama/helper2.py: the same stage, pebbles and cyan in-tank grade), now acted out:

    "The shrimp panicked."  lightning washes the lab; on "panicked" the shrimp hops in fright (crouch, jump with the
                            claw and antennae flung, a squashed landing with overshoot), then trembles on 2s
    (before "Its")          a 4-frame cut to its wide, trembling eyes (the 9-step hit template, IM1)
    "Its snap"              the claw cocks back, held while only the glint grows (IM2); the 2-frame shut lands on
                            "snap"; flash, then 2 impact frames (comp.impact from the subject pass, at IMPACT)
    (the shut + 1)          the shock hits the front glass right at the claw: a white star, a ring flash, tiny cracks
    "cracked"               the glass breaks from that point (_glass_crack): jagged white lines with a dark hairline,
                            branches and a spider-web ring, spreading in 4 steps on 1s with glints on the newest lines
    "the tank."             a jet of water (mk/shared_water.falling_water) spits out of the impact point and arcs
                            onto the desk, where a shared-water puddle spreads

Every beat is placed on the words of line l7 in channels/monsters/ep01v3/timing.json (beats()), so the picture and
the SFX follow the voice. One main camera, pushing in slowly on 1s through the whole shot, with a small shake on the
snap. Units: 1 unit = 20 cm.
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper2 as d2
from channels.monsters.diorama_v3.shots import v3_frames
from channels.monsters.ep01v2 import helper2 as h3d
from channels.monsters.mk import anim, diorama, look
from channels.monsters.mk import shared_water as sw
from channels.monsters.mk import pistolshrimp as ps

UNITS = d2.UNITS
YAW = 20.0                     # the main camera from the south-west: the shrimp faces it, the crack is between them
_T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep01v3", "timing.json")
# word starts (s) from the shot's first frame, for when the v3 timing isn't there yet
_GUESS = dict(shrimp=0.15, panicked=0.45, its=1.45, snap=1.62, cracked=1.9, tank=2.45)


def beats():
    """Shot frames (1 = the shot's first frame) of the words that carry a beat in "The shrimp panicked. Its snap
    cracked the tank.", from the v3 timing (or _GUESS before it exists)."""
    words = dict(_GUESS)
    t0 = 0.0
    if os.path.exists(_T):
        with open(_T) as f:
            d = json.load(f)
        shot = next(s for s in d["shots"] if s["shot"] == "S07")
        line = next(ln for ln in d["lines"] if ln["scene"] == "S07")
        t0 = shot["start"]
        for w in line["words"]:
            key = w["w"].lower().strip(".,!?")
            if key in words:
                words[key] = w["start"] - t0
    return {k: 1 + round(v * 24) for k, v in words.items()}


def _hop(rig, f, back=Vector((0.0, 0.0, 0.0))):
    """The fright hop at f (takeoff): a 2-frame crouch, the jump with claw, antennae and tail flung (reaction pose),
    a squashed landing at f + 6 with an overshoot, settled by f + 11. `back` = the world offset it lands at."""
    root, body = rig["root"], rig["body"]
    k = rig["k"]
    p0 = root.location.copy()
    ps.reaction(rig, f, hold=4)                        # claw thrown open, antennae up, eyes bigger, in the air
    up = 1.9 * k                                       # ~0.28 units: about its own body height
    anim.key(root, "location", f - 3, p0)
    anim.squash(body, f - 3, 0.0)
    anim.squash(body, f - 1, -0.14)                    # crouch (anticipation)
    anim.key(root, "location", f - 1, p0 + Vector((0, 0, -0.05 * k)), "LINEAR")
    anim.key(root, "location", f, p0 + back * 0.15 + Vector((0, 0, 0.5 * k)), "LINEAR")
    anim.squash(body, f, 0.16, "LINEAR")               # stretch at takeoff
    anim.key(root, "location", f + 3, p0 + back * 0.6 + Vector((0, 0, up)))
    anim.squash(body, f + 3, 0.04)
    anim.key(root, "location", f + 6, p0 + back, "LINEAR")
    sh = bpy.data.objects.get(f"{rig['name']}_shadow")
    if sh is not None:                                 # the contact shadow stays on the gravel and shrinks in the air
        z0, s0 = sh.location.z, sh.scale.copy()
        for fr, dz, sc_, it in ((f - 3, 0.0, 1.0, "BEZIER"), (f - 1, -0.05 * k, 1.0, "LINEAR"),
                                (f, 0.5 * k, 0.9, "LINEAR"), (f + 3, up, 0.6, "BEZIER"), (f + 6, 0.0, 1.0, "LINEAR")):
            anim.key(sh, "location", fr, (sh.location.x, sh.location.y, z0 - dz / k), it)
            anim.key(sh, "scale", fr, s0 * sc_, it)
    anim.squash(body, f + 6, -0.16, "LINEAR")          # landing squash
    anim.squash(body, f + 8, 0.06)                     # overshoot
    anim.squash(body, f + 11, 0.0)
    for i, a in enumerate(rig["antennae"]):            # the whips trail the jump, then whip forward on landing
        s = (-1) ** i
        anim.key(a, "rotation_euler", f - 1, (0.05 * s, 0.1, 0.0))
        anim.key(a, "rotation_euler", f + 6, (-0.25 * s, 0.25, -0.1 * s), "LINEAR")
        anim.key(a, "rotation_euler", f + 9, (0.2 * s, -0.15, 0.06 * s))
    anim.key(rig["hinge"], "rotation_euler", f + 8, (0, 0.15, 0))
    anim.key(rig["tail"], "rotation_euler", f + 8, (0, -0.1, 0))
    return p0 + back


def _tremble(rig, f0, f1, home, amount=0.022):
    """Panic: the body shivers on 2s (small twists and shifts), the antennae flutter, the eyes stay wide and pulse."""
    root, k = rig["root"], rig["k"]
    turn = root.rotation_euler.z
    rnd = random.Random(7)
    for n in range(f0, f1, 2):
        s = 1 if (n - f0) % 4 == 0 else -1
        anim.key(root, "location", n, home + Vector((s * amount * k * 6, rnd.uniform(-1, 1) * amount * k * 3, 0)),
                 "CONSTANT")
        anim.key(root, "rotation_euler", n, (0, 0, turn + s * 0.06), "CONSTANT")
        for i, a in enumerate(rig["antennae"]):
            q = (-1) ** i
            anim.key(a, "rotation_euler", n, (q * (0.12 + 0.1 * s), 0.05 * s, 0.05 * q), "CONSTANT")
        for e in rig["eyes"]:
            anim.key(e, "scale", n, (1.14 + 0.04 * s,) * 3, "CONSTANT")
    anim.key(root, "location", f1, home, "CONSTANT")
    anim.key(root, "rotation_euler", f1, (0, 0, turn), "CONSTANT")


def _strike(rig, wind, shut):
    """The wind-up and the shut, as v2 S07 (_s07_action) but timed to the words: the claw cocks back over 3 frames
    from `wind` and HOLDS while only the glint grows; the shut is 2 frames, landing on `shut`; recoil and tail flick,
    then frozen."""
    anim.key(rig["hinge"], "rotation_euler", wind, (0, 0.15, 0))
    anim.key(rig["shoulder"], "rotation_euler", wind, (0, 0, 0))
    anim.key(rig["hinge"], "rotation_euler", wind + 3, (0, ps.OPEN, 0))
    anim.key(rig["shoulder"], "rotation_euler", wind + 3, (0, -0.22, 0.18))          # cocked back and up
    anim.squash(rig["body"], wind + 3, -0.06)
    anim.key(rig["hinge"], "rotation_euler", shut - 1, (0, ps.OPEN, 0), "LINEAR")
    anim.key(rig["shoulder"], "rotation_euler", shut - 1, (0, -0.24, 0.2), "LINEAR")
    anim.key(rig["hinge"], "rotation_euler", shut, (0, ps.OPEN * 0.3, 0), "LINEAR")
    anim.key(rig["hinge"], "rotation_euler", shut + 1, (0, 0.0, 0), "CONSTANT")
    anim.key(rig["shoulder"], "rotation_euler", shut + 1, (0, 0.06, -0.08), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", shut - 1, (0, -0.05, 0), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", shut + 1, (0, 0.55, 0), "CONSTANT")
    anim.squash(rig["body"], shut + 1, 0.06, "CONSTANT")
    h3d._charge(rig, wind + 3, shut - 1)
    ps.bubble(rig, shut + 1)
    ps.shock(rig, shut + 1, radius=2.2)


def _jet(origin, f, end, floor_z, k=UNITS, seed=11):
    """The water spitting out of the crack at `origin` (on the front glass) from frame f: a bright arc that shoots out
    toward the camera side and falls to the desk in 3 frames, wobbling on 2s, with droplets flying along it on 1s and
    a splash where it lands. Lengths in metres x k."""
    rnd = random.Random(seed)
    o = Vector(origin)
    v = Vector((-0.3, -0.2, 0.2)) * k                  # launch velocity (units per second): out of the glass, up
    g = 1.6 * k                                        # and to the left of the yaw -22 frame, so it reads as an arc

    def at(t):
        return o + v * t + Vector((0, 0, -0.5 * g * t * t))

    t_hit = (v.z + math.sqrt(v.z * v.z + 2 * g * (o.z - floor_z))) / g
    pts = [at(t_hit * i / 10) for i in range(11)]
    fall = sw.falling_water(pts, f, end, radius=0.0024 * k, grow=3, k=0.22, name="jet", taper=(1.4, 0.8), glassy=True,
                            jitter=0.3)
    # a little spray right where it bursts out of the crack: fine droplets flung out on 2s, again and again
    sm = look.flat("jet_spray", look.hexc("#f2fdff"), 1.8)
    for i in range(10):
        dpl = ps._sphere(f"jet_spray{i}", o, (1, 1, 1), sm, 0, 8)
        dpl.visible_shadow = False
        a = rnd.uniform(0, 2 * math.pi)
        dv = Vector((math.cos(a) * 0.8, -rnd.uniform(0.3, 1.0), math.sin(a) * 0.8)).normalized() * \
            rnd.uniform(0.012, 0.03) * k
        r = rnd.uniform(0.0006, 0.0012) * k
        anim.key(dpl, "scale", f - 1, 0.0001, "CONSTANT")
        s0 = f + (i % 3) * 2
        while s0 < end:
            for t in (0, 2, 4):
                anim.key(dpl, "location", s0 + t, o + dv * (t / 4) + Vector((0, 0, -0.004 * k * (t / 4) ** 2)),
                         "CONSTANT")
                anim.key(dpl, "scale", s0 + t, r if t < 4 else 0.0001, "CONSTANT")
            s0 += 6
    arcs = [fall["body"], fall["core"]]
    # the burst at the crack: a little star of spray, then it keeps fizzing
    burst = ps._sphere("jet_burst", o, (1, 1, 1), ps._glow("jet_burst_m", look.hexc("#e6fbff"), 0.8), 0, 16)
    burst.visible_shadow = False
    for fr, sc_ in ((f - 1, 0.0001), (f, 0.006 * k), (f + 1, 0.004 * k), (f + 3, 0.0025 * k)):
        anim.key(burst, "scale", fr, sc_, "CONSTANT")
    for n in range(f + 3, end + 1, 2):
        anim.key(burst, "scale", n, (0.002 if (n - f) % 4 == 1 else 0.0028) * k, "CONSTANT")
    # droplets thrown off the stream, on 1s
    dm = look.flat("jet_drop", look.hexc("#e9fcff"), 1.6)
    for i in range(9):
        d = ps._sphere(f"jet_drop{i}", o, (1, 1, 1), dm, 0, 10)
        d.visible_shadow = False
        r = rnd.uniform(0.0009, 0.0016) * k
        off = Vector((rnd.uniform(-0.04, 0.04), rnd.uniform(-0.03, 0.02), rnd.uniform(-0.01, 0.05))) * k
        life = 7
        start = f + 1 + (i * 3) % 8
        anim.key(d, "scale", f - 1, 0.0001, "CONSTANT")
        while start + 2 < end + 1:
            for j in range(life):
                t = t_hit * 1.1 * j / (life - 1)
                anim.key(d, "location", start + j, at(t) + off * (j / (life - 1)), "CONSTANT")
                anim.key(d, "scale", start + j, r if j < life - 1 else 0.0001, "CONSTANT")
            start += life + rnd.randint(0, 2)
    # where it lands: the shared puddle (sw.spill_material, rimmed) spreading on the desk
    hit = at(t_hit)
    bpy.ops.mesh.primitive_circle_add(vertices=24, radius=1.0, fill_type="NGON", location=(hit.x, hit.y, hit.z + 0.002))
    pud = bpy.context.object
    pud.name = "jet_puddle"
    pud.data.materials.append(sw.spill_material())
    pud.visible_shadow = False
    anim.key(pud, "scale", f + 2, (0.0001,) * 3, "CONSTANT")
    anim.key(pud, "scale", f + 3, (0.02 * k, 0.014 * k, 1), "LINEAR")
    anim.key(pud, "scale", end, (0.07 * k, 0.05 * k, 1), "LINEAR")
    sw.rim(pud, width=0.08)
    return arcs


def _jag(rnd, p, ang, length, segs, wobble=0.45):
    """A jagged line in the glass plane (x, z) from p: `segs` kinks, each turning by up to `wobble` radians."""
    pts = [Vector(p)]
    step = length / segs
    for _ in range(segs):
        ang += rnd.uniform(-wobble, wobble)
        q = pts[-1] + Vector((math.cos(ang), 0.0, math.sin(ang))) * step * rnd.uniform(0.7, 1.3)
        pts.append(q)
    return pts


def _crack_line(name, pts, f_show, f_done, lite, dark, w=0.0026, side=1):
    """One crack line: a bright white curve with a dark hairline one pixel or two to one side (and a hair behind,
    on the glass), growing from its first point between f_show and f_done on 1s."""
    objs = []
    for nm, m, r, off in ((f"{name}_d", dark, w * 0.35, side * w * 0.75), (f"{name}_l", lite, w * 0.5, 0.0)):
        cu = bpy.data.curves.new(nm, "CURVE")
        cu.dimensions = "3D"
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for i, (a, q) in enumerate(zip(sp.points, pts)):
            nb = pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]
            perp = Vector((-nb.z, 0.0, nb.x)).normalized() if nb.length > 1e-6 else Vector((0, 0, 1))
            c = q + perp * off + Vector((0, 0.0006 if off else 0.0, 0))
            a.co = (c.x, c.y, c.z, 1.0)
            a.radius = 1.0 - 0.5 * i / max(1, len(pts) - 1)            # thinner toward the end
        cu.bevel_depth = r
        cu.bevel_resolution = 1
        o = bpy.data.objects.new(nm, cu)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(m)
        o.visible_shadow = False
        steps = max(1, f_done - f_show)
        for i in range(-1, steps + 1):
            cu.bevel_factor_end = 0.0 if i < 0 else min(1.0, 0.08 + 0.92 * i / steps)
            cu.keyframe_insert("bevel_factor_end", frame=f_show + i)
        for fc in anim.all_fcurves(cu.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
        objs.append(o)
    return objs


def _glass_crack(hit, f_hit, f0, steps=4, seed=17, size=0.42):
    """The front glass breaking from the snap. On f_hit (the frame after the shut): a small white star and a ring of
    light flash at the impact point, with a few tiny cracks. From f0 ("cracked") the crack spreads out in `steps`
    steps on 1s: 8 jagged radial lines (out to `size` units, 3 px wide at 720), short branches off them, a broken
    spider-web ring near the centre; a glint runs out along the newest lines. Lines are white with a dark hairline
    on one side, so they read on the gravel."""
    rnd = random.Random(seed)
    lite = look.flat("crack3_lite", look.hexc("#ffffff"), 2.2)
    dark = look.flat("crack3_dark", look.hexc("#0e2c38"), 1.0)
    out = []
    # the impact: tiny cracks at once, a white star and a ring flash
    for i in range(6):
        a = i / 6 * 2 * math.pi + rnd.uniform(-0.3, 0.3)
        out += _crack_line(f"crk_hit{i}", _jag(rnd, hit, a, rnd.uniform(0.018, 0.03), 2, 0.3), f_hit, f_hit, lite,
                           dark)
    star = look.flat("crack3_star", look.hexc("#ffffff"), 4.0)
    verts = [(math.cos(k / 16 * 2 * math.pi) * (1.0 if k % 2 == 0 else 0.18), 0,
              math.sin(k / 16 * 2 * math.pi) * (1.0 if k % 2 == 0 else 0.18)) for k in range(16)] + [(0, 0, 0)]
    me = bpy.data.meshes.new("crk_star")
    me.from_pydata(verts, [], [(16, k, (k + 1) % 16) for k in range(16)])
    st = bpy.data.objects.new("crk_star", me)
    bpy.context.scene.collection.objects.link(st)
    st.data.materials.append(star)
    st.location = hit + Vector((0, -0.002, 0))
    st.visible_shadow = False
    for fr, sc_ in ((f_hit - 1, 0.0001), (f_hit, 0.05), (f_hit + 1, 0.035), (f_hit + 2, 0.02), (f_hit + 4, 0.012),
                    (f0, 0.012), (f0 + 1, 0.03), (f0 + 2, 0.015), (f0 + 4, 0.008)):
        anim.key(st, "scale", fr, (sc_, sc_, sc_), "CONSTANT")
    ring = anim.shockwave(tuple(hit + Vector((0, -0.003, 0))), f_hit, frames=4, radius=0.12, color="#f0fbff")
    ring.rotation_euler = (math.radians(90), 0, 0)
    ring.visible_shadow = False
    for fc in anim.all_fcurves(ring.animation_data.action):
        if fc.data_path == "scale":
            for kp in fc.keyframe_points:
                if kp.co.x <= f_hit:
                    kp.co.y *= 0.05
                    kp.handle_left.y = kp.handle_right.y = kp.co.y
    # the spread: radial lines out in `steps` steps, branches when the line reaches them, the web ring at step 2
    mains = []
    for i in range(8):
        a = i / 8 * 2 * math.pi + rnd.uniform(-0.25, 0.25)
        ln = size * rnd.uniform(0.45, 1.0)
        pts = _jag(rnd, hit, a, ln, rnd.randint(6, 9))
        out += _crack_line(f"crk_main{i}", pts, f0, f0 + steps - 1, lite, dark, side=(-1) ** i)
        mains.append(pts)
        for j in range(2, len(pts) - 1):
            if rnd.random() < 0.55:
                u = j / (len(pts) - 1)
                fb = f0 + min(steps - 1, int(u * steps))
                ba = a + rnd.choice((-1, 1)) * rnd.uniform(0.5, 1.1)
                out += _crack_line(f"crk_br{i}_{j}", _jag(rnd, pts[j], ba, ln * rnd.uniform(0.12, 0.25), 3, 0.5),
                                   fb, min(f0 + steps, fb + 1), lite, dark, w=0.0019, side=(-1) ** j)
    for i in range(8):                                  # the web: short kinked links between neighbouring radials
        if rnd.random() < 0.7:
            a, b = mains[i], mains[(i + 1) % 8]
            ka = min(len(a) - 1, 2 + rnd.randint(0, 1))
            kb = min(len(b) - 1, 2 + rnd.randint(0, 1))
            mid = (a[ka] + b[kb]) / 2 + (a[ka] + b[kb] - 2 * hit).normalized() * 0.006
            out += _crack_line(f"crk_web{i}", [a[ka], mid, b[kb]], f0 + 1, f0 + 2, lite, dark, w=0.0019)
    # glints running out along three of the newest lines, on 1s
    gm = ps._glow("crack3_glint", look.hexc("#ffffff"), 0.9)
    for i in (0, 3, 5):
        pts = mains[i]
        g = ps._sphere(f"crk_glint{i}", hit, (1, 1, 1), gm, 0, 12)
        g.visible_shadow = False
        anim.key(g, "scale", f0 - 1, 0.0001, "CONSTANT")
        last = f0 + steps + 3
        for fr in range(f0, last + 1):
            u = min(1.0, (fr - f0 + 1) / (last - f0 + 1))
            q = pts[min(len(pts) - 1, int(u * (len(pts) - 1)))]
            anim.key(g, "location", fr, q + Vector((0, -0.002, 0)), "CONSTANT")
            anim.key(g, "scale", fr, 0.009 * (1.0 if fr < last else 0.0001), "CONSTANT")
    return out


def _push(cam, target, f0, f1, amount=0.1):
    """A slow push-in on 1s (LINEAR) from f0 to f1: `amount` of the distance, focus kept on the target."""
    t = Vector(target)
    p0 = cam.location.copy()
    p1 = p0 + (t - p0) * amount
    anim.key(cam, "location", f0, p0, "LINEAR")
    anim.key(cam, "location", f1, p1, "LINEAR")
    for f, p in ((f0, p0), (f1, p1)):
        cam.data.dof.focus_distance = (t - p).length
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def _shake(cam, f, amount=0.012):
    """A 4-frame camera jolt on the snap, on 1s, added on top of the push-in."""
    fc = {c.array_index: c for c in anim.all_fcurves(cam.animation_data.action) if c.data_path == "location"}
    fc = [fc[i] for i in range(3)]
    pos = [Vector([c.evaluate(f + n) for c in fc]) for n in range(4)]
    for n, (dx, dz) in enumerate(((1, -1), (-0.7, 0.6), (0.4, -0.3), (0, 0))):
        anim.key(cam, "location", f + n, pos[n] + Vector((dx, 0, dz)) * amount * UNITS, "LINEAR")


def s07():
    B = beats()
    n = v3_frames("S07") if os.path.exists(_T) else 84
    snap = max(B["snap"], 16)
    hop = max(5, min(B["panicked"] + 1, snap - 16))    # the takeoff lands on "panicked"
    eye0, wind = snap - 10, snap - 6                    # eye cut 4 frames, then the wind-up
    flash = snap + 2
    crack = max(B["cracked"], snap + 4)
    jet = max(B["tank"], crack + 4)
    room, tank, rig = d2._stage()
    if room is not None:                                # the storm is still on: a lightning wash as it starts
        room["lightning"](2, 0.6)
    home = _hop(rig, hop, back=Vector((0.12, 0.05, 0.0)) * rig["k"] * 2)
    _tremble(rig, hop + 11, wind, home)
    _strike(rig, wind, snap)
    fx, fy, fz = tank["floor"]
    # the claw tip and the crack a third in from the left, the body to the right of them, all left of x 560
    target = Vector((fx - 0.28, fy - 0.5, fz + 0.22))
    cam = diorama.camera("dio_cam_s07", target, dist=3.1, tilt=42, yaw=YAW, lens=d2.LENS, blur=d2.BLUR, frame=1)
    gy = tank["glass"].location.y - 0.004 * UNITS        # just in front of the front pane
    tip, _ = ps._jet(rig, snap + 1)                     # where the snap's shock hits the glass: on the pane where
    ray = tip - cam.location                            # it covers the claw tip from the camera
    hit = cam.location + ray * ((gy - cam.location.y) / ray.y) + Vector((0, 0, 0.005))
    _glass_crack(hit, snap + 1, crack, seed=17)
    h3d._dim_water(tank, [(wind, 1.0), (snap, 0.6)])
    desk = room["desk"]["top"] if room is not None else tank["floor"][2] - 0.3
    _jet(hit + Vector((0, -0.004, 0)), jet, n, desk)    # the water spits out of the impact point
    e = ps._world(rig["eyes"][0], eye0 + 1).translation          # where the eye is after the hop, mid-tremble
    eye = diorama.camera("dio_cam_s07_eye", e, dist=0.6, tilt=48, yaw=math.degrees(d2.TURN) - 60, lens=d2.LENS,
                         blur=d2.BLUR, frame=eye0)
    bpy.context.scene.timeline_markers.new("dio_cam_s07_back", frame=wind).camera = cam     # back after the eye cut
    for c in (cam, eye):
        d2._near(c)
    _push(cam, target, 1, n, 0.12)                      # one continuous push, on 1s, across the cut
    _shake(cam, snap + 1)
    d2._flash(cam, [(flash - 1, 0.0), (flash, 0.9), (flash + 1, 0.0)])
    d2._grade()
    return dict(frames=n, step=1, subject=[rig["root"]], beats=dict(B, hop=hop, eye=eye0, wind=wind, snap=snap,
                                                                     flash=flash, impact=flash + 1, crack=crack,
                                                                     jet=jet))


def _reuse(build, shot):
    """A v2 diorama tank shot in the v3 set (dressing, Q3 lighting, shared water are applied by the shared modules
    and render_shot), with its v3 frame count. S04/S05a keep v2's lines, so every beat stays on its frame."""
    def b():
        info = build()
        info["frames"] = v3_frames(shot) if os.path.exists(_T) else info["frames"]
        return info
    return b


SHOTS = {"S07": s07, "S04": _reuse(d2.s04, "S04"), "S05a": _reuse(d2.s05a, "S05a")}
