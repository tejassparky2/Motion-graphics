"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 9: S06 and S08 in the dollhouse lab.
Frame counts come from channels/monsters/ep01v3/timing.json (render_frames); the picture builds on diorama/helper9.py.

    S06 "Then the storm hit.": the dollhouse lab from above, the window over Kai at the desk, the hero tank beside
        him with the shrimp asleep on the gravel (eyes shut, antennae down, breathing). The bolt and the room flash
        land on "storm" (14): 2 near-white frames (14-15, a 2D overlay at 72 % / 60 %, then 18 % on 16) with hard
        window shadows and the bolt in the glass (14-17); the shrimp jolts awake (squash, hop with its claw and antennae flung up, overshoot,
        land, wide eyes, 2D surprise lines) and Kai looks up to the window (16); the room lights stutter at 20, 23,
        26, 30, 34. A slow push-in on 1s; characters on 2s.
    S08 "Water spilled off the desk, straight into the power cables." (98 frames): the camera follows the water on
        1s (a crane/truck move, fixed angle): the leak spreads over the desk from the cracked tank (6), runs off the
        front edge on "spilled" (15) and pours down in a little waterfall with a splash at its foot ("off the desk"),
        spreads over the tiles toward the power strip, reaches the plugs on "cables" (68), and they start to fizz:
        small electric crackles on 1s, two bright pops (70, 84) and a light stutter (72). Kai stays at the desk,
        unaware, in the background.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S06 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Vector

from channels.monsters.diorama import helper1 as d1              # the dollhouse lab with Kai seated at the desk
from channels.monsters.diorama import helper9 as v2              # the window bolt
from channels.monsters.ep01v2 import helper1 as h1               # his seated pose
from channels.monsters.mk import anim, hero, look, storm
from channels.monsters.mk import pistolshrimp as ps

V2 = {"S06": 41, "S08": 85}                                     # v2 counts: only a fallback until timing.json lands
K = 0.48                                                        # the shrimp, big enough to read in a room shot


def _n(shot):
    try:
        from channels.monsters.diorama_v3.shots import v3_frames
        return v3_frames(shot)
    except (OSError, KeyError):
        return V2[shot]


def _push(cam, target, f0, f1, amount):
    """A slow push-in on 1s: the camera slides `amount` (0-1) of the way toward `target`, focus following."""
    t = Vector(target)
    p0 = cam.location.copy()
    d0 = cam.data.dof.focus_distance
    for f, u in ((f0, 0.0), (f1, amount)):
        anim.key(cam, "location", f, p0.lerp(t, u), "LINEAR")
        cam.data.dof.focus_distance = d0 * (1 - u)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    for fc in anim.all_fcurves(cam.data.animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def _surprise_lines(loc, cam, f0, f1, size=0.55, n=7):
    """2D comic surprise lines: short white strokes radiating round `loc` (an arc over the head), facing the camera,
    popping out at f0 (big), easing in, gone at f1. On 2s."""
    verts, faces = [], []
    for i in range(n):
        a = math.radians(20 + 140 * i / (n - 1))
        d = Vector((math.cos(a), math.sin(a), 0))
        s = Vector((-d.y, d.x, 0)) * 0.05
        r0, r1 = 0.62, 1.0 if i % 2 == 0 else 0.86
        b = len(verts)
        verts += [tuple(d * r0 - s * 0.5), tuple(d * r0 + s * 0.5), tuple(d * r1 + s), tuple(d * r1 - s)]
        faces.append((b, b + 1, b + 2, b + 3))
    me = bpy.data.meshes.new("s06_surprise")
    me.from_pydata(verts, [], faces)
    me.materials.append(look.flat("s06_surprise", look.hexc("#ffffff"), 3.0))
    o = bpy.data.objects.new("s06_surprise", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.visible_shadow = False
    c = o.constraints.new("TRACK_TO")
    c.target, c.track_axis, c.up_axis = cam, "TRACK_Z", "UP_Y"
    for f, sc in ((f0 - 1, 0.001), (f0, 1.25), (f0 + 2, 1.0), (f0 + 4, 0.95), (f1 - 2, 0.9), (f1, 0.001)):
        anim.key(o, "scale", f, (size * sc,) * 3, "CONSTANT")
    return o


def _tank_shrimp(R, cam_yaw):
    """The shrimp on the hero tank's gravel, three-quarter to the camera, with the close pebbles round it."""
    t = R["tank"]
    fx, fy, fz = t["center"]
    gy = t["glass_y"]
    face = math.radians(cam_yaw)                                 # head toward the camera, turned 35 deg to show the claw
    turn = math.atan2(math.cos(face), math.sin(face)) - math.radians(35)   # head dir is (-cos, -sin)
    rig = ps.build((fx + 0.1, gy + 0.55, fz), turn=turn, scale=K, name="s06_shrimp")   # just behind the front glass
    bpy.ops.object.light_add(type="POINT", location=(fx + 0.1, gy - 0.6, fz + 1.0))       # a soft key on it
    key = bpy.context.object
    key.data.energy, key.data.color, key.data.shadow_soft_size = 25.0, look.hexc("#d6fbff")[:3], 0.4
    key.data.use_shadow = False
    return rig


def _asleep(rig, f):
    """Shrimp asleep: eyes shut (flat), antennae drooped, claw resting, body low."""
    for e in rig["eyes"]:
        anim.key(e, "scale", f, (1.1, 1, 0.08), "CONSTANT")
    for i, a in enumerate(rig["antennae"]):
        anim.key(a, "rotation_euler", f, (0.0, 0.35, 0.1 * (-1) ** i), "CONSTANT")
    anim.key(rig["hinge"], "rotation_euler", f, (0, 0.04, 0), "CONSTANT")
    anim.key(rig["shoulder"], "rotation_euler", f, (0, 0.1, 0), "CONSTANT")
    anim.key(rig["tail"], "rotation_euler", f, (0, 0.0, 0), "CONSTANT")


def _jolt(rig, flash):
    """Asleep (breathing on 2s) until the flash, then: squash (flash), hop up with the startled pose (+2), overshoot at
    the top (+4), land squashed (+6), settle wide-eyed (+8); antennae twitch on 2s after."""
    root = rig["root"]
    z0 = root.location.z
    hop = 0.32
    for f in range(1, flash, 2):                                 # slow sleepy breathing
        _asleep(rig, f)
        anim.squash(rig["body"], f, -0.03 if (f // 8) % 2 else 0.0, "CONSTANT")
        anim.key(root, "location", f, (root.location.x, root.location.y, z0), "CONSTANT")
    _asleep(rig, flash)
    anim.squash(rig["body"], flash, -0.12, "CONSTANT")           # the flash hits: squash
    anim.key(root, "location", flash, (root.location.x, root.location.y, z0), "CONSTANT")
    ps.reaction(rig, flash + 2, hold=4)                          # startled pose, eyes popped
    for e in rig["eyes"]:
        anim.key(e, "scale", flash + 2, (1.35, 1.35, 1.45), "CONSTANT")
        anim.key(e, "scale", flash + 8, (1.2, 1.2, 1.3), "CONSTANT")
    for f, dz, sq in ((flash + 2, hop * 0.8, 0.14), (flash + 4, hop, 0.06), (flash + 6, 0.0, -0.1),
                      (flash + 8, 0.0, 0.03), (flash + 10, 0.0, 0.0)):
        anim.key(root, "location", f, (root.location.x, root.location.y, z0 + dz), "CONSTANT")
        anim.squash(rig["body"], f, sq, "CONSTANT")
    for f in range(flash + 10, flash + 80, 2):                   # alert: antennae twitching, claw half raised
        k = (f // 2) % 3
        for i, a in enumerate(rig["antennae"]):
            anim.key(a, "rotation_euler", f, (0.25 * (-1) ** i + 0.06 * (k - 1), -0.22, 0.1 * (-1) ** i), "CONSTANT")
    anim.key(rig["hinge"], "rotation_euler", flash + 10, (0, 0.5, 0), "CONSTANT")
    anim.key(rig["shoulder"], "rotation_euler", flash + 10, (0, -0.12, 0.1), "CONSTANT")
    for o in (rig["hinge"], rig["shoulder"], rig["tail"], rig["body"], *rig["eyes"], *rig["antennae"]):
        ad = o.animation_data
        if ad and ad.action:
            for fc in anim.all_fcurves(ad.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def s06():
    R, rig = d1._stage()
    n = _n("S06")
    h1._sit(rig, lean=0.1, look=(0.1, 0.1))
    h1._key_pose(rig, 1, h1.BODY)
    h1._sit(rig, lean=-0.05, look=(0.0, -0.45))                  # the flash: he looks up to the window
    h1._key_pose(rig, 16, h1.BODY)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "blink", 9)
    hero.face(rig, "neutral", 11)
    hero.face(rig, "surprised", 16, 0.7)
    w, tank = Vector(R["window"]["center"]), Vector(R["tank"]["center"])
    head = h1._head_pos(rig)
    yaw = -42.0                                                  # from the tank's side: Kai and the tank closer together
    target = head.lerp(tank, 0.55) + Vector((0, 0, 1.4))
    cam = R["cam"]("cam_s06", tuple(target), dist=40.0, tilt=42.0, yaw=yaw, lens=95.0, blur=10.0)
    cam.data.shift_x = 0.07                                      # the tank left of the Shorts rail (x < 560)
    _push(cam, target, 1, n, 0.1)
    strike = R["lights"]["strike"].data                          # the lightning: a small hot source behind the window,
    strike.size, strike.size_y = 1.2, 1.0                        # so the window bars throw hard shadows into the room
    R["lightning"](14, strength=1.4)                             # on "storm": the sky and the room flash
    for o in v2._window_bolt(R, 14):                             # the bolt in the glass through the whole hit (14-17)
        for f in (15, 17):
            o.hide_render = False
            o.keyframe_insert("hide_render", frame=f)
    flash = storm._overlay("s06_flash", (0.93, 0.97, 1.0, 1.0), 0.0)      # 2 near-white frames over everything
    fp = storm._screen_plane("s06_flash", cam, storm.D_WHITE, flash, storm._group(cam, "flash"))
    fp.visible_shadow = False
    for f, a in ((13, 0.0), (14, 0.72), (15, 0.6), (16, 0.18), (17, 0.0)):
        storm._key_socket(storm._alpha(flash), f, a, "CONSTANT")
    R["flicker"]([20, 23, 26, 30, 34])
    shrimp = _tank_shrimp(R, yaw)
    _jolt(shrimp, 14)
    anim.on_twos([rig["arm"]], step=2)                           # Kai on 2s
    _surprise_lines(shrimp["root"].location + Vector((0, -0.85, 0.5)), cam, 16, 24, size=0.8)
    return dict(frames=n, step=1, subject=[rig["arm"], shrimp["root"]] + list(rig.get("cap", [])))


def _sparkle(name, color, strength):
    return look.flat(name, look.hexc(color), strength)


def _zigzag(name, a, b, rnd, mat, width=0.06, kinks=4):
    """A small electric crackle: a jagged ribbon from a to b (in a plane facing up/camera-ish), one mesh."""
    a, b = Vector(a), Vector(b)
    d = b - a
    side = d.cross(Vector((0, 0, 1)))
    side = side.normalized() if side.length > 1e-6 else Vector((1, 0, 0))
    pts = [a]
    for i in range(1, kinks):
        pts.append(a + d * (i / kinks) + side * rnd.uniform(-0.18, 0.18) * d.length + Vector((0, 0, rnd.uniform(-0.05, 0.08))))
    pts.append(b)
    verts, faces = [], []
    for i, p in enumerate(pts):
        verts += [tuple(p - Vector((0, 0, width / 2))), tuple(p + Vector((0, 0, width / 2)))]
        if i:
            faces.append((2 * i - 2, 2 * i - 1, 2 * i + 1, 2 * i))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.visible_shadow = False
    return o


def _fizz(R, f0, f1, seed=8):
    """The plugs fizz: on 1s from f0, 1-3 tiny crackles jump between the plugs and the wet tiles (each lives 1-2
    frames), a cold blue point light stutters with them."""
    import random
    rnd = random.Random(seed)
    st = R["strip"]["object"]
    rz = st.rotation_euler.z
    ax = Vector((math.cos(rz), math.sin(rz), 0))
    base = Vector(st.location)
    plugs = [base + ax * (-0.6 + i * 0.5) + Vector((0, 0, 0.35)) for i in range(3)]
    core = _sparkle("s08_fizz_core", "#ffffff", 6.0)
    glow = _sparkle("s08_fizz_glow", "#8fd8ff", 3.0)
    bpy.ops.object.light_add(type="POINT", location=tuple(base + Vector((0, -0.6, 1.2))))
    lt = bpy.context.object
    lt.data.color, lt.data.shadow_soft_size, lt.data.use_shadow = look.hexc("#bfe8ff")[:3], 0.3, False
    lt.data.energy = 0.0
    lt.data.keyframe_insert("energy", frame=f0 - 1)
    k = 0
    for f in range(f0, f1 + 1):
        n = rnd.choice((1, 1, 2, 2, 3)) if f > f0 + 2 else 2
        for j in range(n):
            p = rnd.choice(plugs)
            tgt = p + Vector((rnd.uniform(-0.7, 0.7), rnd.uniform(-0.9, -0.2), -p.z + 0.04))
            life = rnd.choice((1, 1, 2))
            for mat, wd, nm in ((glow, 0.16, "g"), (core, 0.05, "c")):
                o = _zigzag(f"s08_fizz{k}{nm}", p, tgt, random.Random(k), mat, width=wd)
                for ff, on in ((f - 1, 0), (f, 1), (f + life, 0)):
                    o.hide_render = not on
                    o.keyframe_insert("hide_render", frame=ff)
            k += 1
        lt.data.energy = rnd.uniform(60, 260) * (1 + 0.4 * n)
        lt.data.keyframe_insert("energy", frame=f)
    for fc in lt.data.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def _splash(base, f0, f1, seed=5):
    """Drops jumping at the foot of the waterfall, on 2s: small bright water beads that pop up and fall."""
    import random
    rnd = random.Random(seed)
    m = _sparkle("s08_drop", "#d6f6ff", 2.2)
    for i in range(10):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, segments=10, ring_count=6, location=tuple(base))
        d = bpy.context.object
        d.name = f"s08_drop{i}"
        d.data.materials.append(m)
        d.visible_shadow = False
        a = rnd.uniform(0, 2 * math.pi)
        v = Vector((math.cos(a), math.sin(a) * 0.6 - 0.4, 0)) * rnd.uniform(0.3, 0.7)
        f = f0 + rnd.randint(0, 8) // 2 * 2
        while f < f1:
            life = 6
            for t in range(0, life + 1, 2):
                u = t / life
                pos = Vector(base) + v * u + Vector((0, 0, 0.9 * u * (1 - u) * 1.8))
                anim.key(d, "location", f + t, tuple(pos), "CONSTANT")
                anim.key(d, "scale", f + t, (1.0 if t < life else 0.001,) * 3, "CONSTANT")
            anim.key(d, "scale", f - 1, (0.001,) * 3, "CONSTANT")
            f += life + rnd.choice((2, 4))


def s08():
    R, rig = d1._stage()
    n = _n("S08")
    h1._sit(rig, lean=0.15, look=(0.3, 0.2))                     # typing, unaware
    h1._key_pose(rig, 1, h1.BODY)
    h1._sit(rig, lean=0.18, look=(0.2, 0.25))
    h1._key_pose(rig, 40, h1.BODY)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "blink", 30)
    hero.face(rig, "neutral", 32)
    hero.face(rig, "blink", 80)
    hero.face(rig, "neutral", 82)
    anim.on_twos([rig["arm"]], step=2)
    T = R["desk"]["top"]
    leak = Vector(R["tank"]["leak"])
    fy = R["desk"]["front_y"]
    end = Vector(R["strip"]["end"])
    edge = Vector((leak.x, fy, T))
    foot = Vector((leak.x, fy - 0.4, 0.0))
    mid = foot.lerp(Vector((end.x + 0.2, end.y + 0.2, 0)), 0.5) + Vector((-0.6, -0.4, 0))
    R["puddle"](6, 68)                                           # edge at 15 ("spilled"), floor at 25, strip at 68
    _splash(foot + Vector((0, -0.1, 0.05)), 25, n)
    _fizz(R, 68, n)                                              # "...power cables." and on
    R["spark"](70)
    R["spark"](84)
    R["flicker"]([72])
    # follow the water: the camera keeps its angle and slides with a target that runs ahead of the water a little
    path = [(1, leak.lerp(edge, 0.3) + Vector((0, 0, 0.3))), (15, edge + Vector((0, 0, -0.4))),
            (30, foot.lerp(edge, 0.45)), (50, mid + Vector((0, 0, 0.3))), (68, end + Vector((0.3, 0.2, 0.4))),
            (n, end + Vector((0.5, 0.4, 0.45)))]
    dist0 = 36.0
    cam = R["cam"]("cam_s08", tuple(path[0][1]), dist=dist0, tilt=50.0, yaw=-28.0, lens=90.0, blur=10.0)
    shrimp = _tank_shrimp(R, -28.0)                              # still startled in the cracked tank (S06/S07)
    ps.reaction(shrimp, 1, hold=n)
    for e in shrimp["eyes"]:
        anim.key(e, "scale", 1, (1.25, 1.25, 1.35), "CONSTANT")
    for f in range(1, n + 1, 2):
        for i, a in enumerate(shrimp["antennae"]):
            anim.key(a, "rotation_euler", f, (0.3 * (-1) ** i + 0.07 * ((f // 2) % 3 - 1), -0.25, 0.1 * (-1) ** i),
                     "CONSTANT")
    off = cam.location - path[0][1]
    for f, t in path:
        k = 1.0 - 0.14 * max(0.0, (f - 68) / max(1, n - 68))      # a slow push-in onto the fizzing plugs at the end
        anim.key(cam, "location", f, tuple(t + off * k))
        cam.data.dof.focus_distance = dist0 * k
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
    from channels.monsters.mk import shared_water as sw          # helper 2's one water look for S07-S08b
    sw.adopt(R)
    return dict(frames=n, step=2, ones=(1, n), subject=[rig["arm"], shrimp["root"]] + list(rig.get("cap", [])))


SHOTS = {"S06": s06, "S08": s08}
