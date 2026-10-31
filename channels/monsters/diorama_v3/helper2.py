"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 2: S07, "The shrimp panicked. Its
snap cracked the tank." Close in the hero tank of helper 1's dollhouse lab (mk/diorama_lab.py), as v2's S07
(channels/monsters/diorama/helper2.py: the same stage, pebbles and cyan in-tank grade), now acted out:

    "The shrimp panicked."  lightning washes the lab; on "panicked" the shrimp hops in fright (crouch, jump with the
                            claw and antennae flung, a squashed landing with overshoot), then trembles on 2s
    (before "Its")          a 4-frame cut to its wide, trembling eyes (the 9-step hit template, IM1)
    "Its snap"              the claw cocks back, held while only the glint grows (IM2); the 2-frame shut lands on
                            "snap"; flash, then 2 impact frames (comp.impact from the subject pass, at IMPACT)
    "cracked"               the crack zigzags across the front glass from a starburst
    "the tank."             a jet of water spits out of the crack, arcs over the desk and splashes on it

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
    fall = sw.falling_water(pts, f, end, radius=0.0032 * k, grow=3, k=0.22, name="jet", taper=(1.5, 0.8))
    arcs = [fall["body"], fall["core"]]
    # the burst at the crack: a little star of spray, then it keeps fizzing
    burst = ps._sphere("jet_burst", o, (1, 1, 1), ps._glow("jet_burst_m", look.hexc("#e6fbff"), 0.8), 0, 16)
    burst.visible_shadow = False
    for fr, sc_ in ((f - 1, 0.0001), (f, 0.028 * k), (f + 1, 0.018 * k), (f + 3, 0.011 * k)):
        anim.key(burst, "scale", fr, sc_, "CONSTANT")
    for n in range(f + 3, end + 1, 2):
        anim.key(burst, "scale", n, (0.009 if (n - f) % 4 == 1 else 0.012) * k, "CONSTANT")
    # droplets thrown off the stream, on 1s
    dm = look.flat("jet_drop", look.hexc("#e9fcff"), 1.6)
    for i in range(9):
        d = ps._sphere(f"jet_drop{i}", o, (1, 1, 1), dm, 0, 10)
        d.visible_shadow = False
        r = rnd.uniform(0.0035, 0.007) * k
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
    lx, ly, lz = tank["leak"]
    gy = tank["glass"].location.y - 0.006 * UNITS
    path = [(x * UNITS, z * UNITS) for x, z in ps.crack_path()]
    gc = ps.glass_crack((lx, gy, lz - 0.005 * UNITS), path, k=UNITS)
    ps.crack(gc, crack, frames=5)
    h3d._dim_water(tank, [(wind, 1.0), (snap, 0.6)])
    j = min(3, len(path) - 1)                           # the jet bursts from low on the crack, under the waterline
    desk = room["desk"]["top"] if room is not None else tank["floor"][2] - 0.3
    _jet((lx + path[j][0], gy - 0.004 * UNITS, lz - 0.005 * UNITS + path[j][1]), jet, n, desk)
    fx, fy, fz = tank["floor"]
    # the claw tip and the crack a third in from the left, the body to the right of them, all left of x 560
    target = Vector((fx - 0.28, fy - 0.5, fz + 0.22))
    cam = diorama.camera("dio_cam_s07", target, dist=3.1, tilt=42, yaw=YAW, lens=d2.LENS, blur=d2.BLUR, frame=1)
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


SHOTS = {"S07": s07}
