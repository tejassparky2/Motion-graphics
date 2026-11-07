"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md): helper 10's S12 (the orbit) and S14 (the flip).

The physics both shots show: a fluffmoth flies with its BACK (the top of its body, the wings' upper side) turned
toward the brightest light. With the light above, the back tilts in toward it, so the moth banks and curves round
and round it (S12). With the light below (Kai on his back, his wrist mark glowing up through the grass, bGqrs's S13),
the only way to keep its back to the light is to roll upside down; a moth flying upside down stalls and tumbles into
the grass (S14).

Staging (S14): bGqrs's S13 spot (diorama_ep03/bgqrs.py): the grass on the village's north edge, Kai flat on his
back, head west, the left arm laid out palm up. Moths: helper 6's API (mk/fluffmoth.py: flight_mode, back_to, swarm, upside_down).

    S12 "So when the light is above them, they circle it." (67 + 12): the explainer's second half, on helper 4's S11
        stage (the dark night ground, the coral glow): the light ABOVE, one fluffmoth flying round and round under
        it, side-on, banked so its back always faces the glow (2D: the glow line from the light to its back, a dotted
        trail tracing the ring). Push-in on 1s.
    S14 (no words; TWIST, the music drops; 72 + 12): S13's end: Kai on his back, the wrist on the grass glowing up,
        the swarm circling above. A held beat (1-12), then the moths roll upside down to keep their backs to the light
        below (a wave, 12-40), stall, and tumble into the grass round him: plop (32), plop (38), plop (44), then the
        rest (46-66), each landing on its back, legs waving. The 2D pass adds the dust puffs (on 2s) from
        build/monsters/diorama_ep03/S14_landings.json. The camera starts on S13's end and eases down to the grass.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S12 OUT [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import random
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
LANDINGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "S14_landings.json")   # committed (S15, sound)
try:
    import bpy
    from mathutils import Euler, Matrix, Vector

    from channels.monsters.diorama_ep02 import helper9 as H9      # _forearm, MARK_U, _mark_geo, _px, village_and_lake
    from channels.monsters.diorama_ep02 import xprl as X          # _world (the island as Ep 1 left it)
    from channels.monsters.diorama_ep03 import bgqrs as B         # S13's staging (spot, lying pose, light, swarm)
    from channels.monsters.ep01v2 import helper10 as s15          # Kai's pose helpers (_pose, _ground, _world)
    from channels.monsters.mk import acting, anim, fluffmoth, hero
except ImportError:                                               # the 2D pass runs outside Blender
    bpy = None

FPS = 24
MOTH_S = 0.42                       # the swarm's moth size (bGqrs's SWARM_SCALE): one size everywhere

def _frames(shot, fallback):
    from channels.monsters.diorama_ep03.shots import ep03_frames
    try:
        return ep03_frames(shot)
    except (OSError, KeyError):
        return fallback


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _still():
    return "--still" in sys.argv


# ---------------------------------------------------------------- the set (S13's)
def _set(n):
    X._world(n)
    B._night()                                                    # helper 9's night grade once it lands
    try:
        H9.village_and_lake()
    except Exception as e:                                        # optional for a test still
        print("helper10: no village", e)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n


def _lamp(name, energy, soft, shadow=True):
    d = bpy.data.lights.new(name, "POINT")
    d.color, d.shadow_soft_size, d.energy, d.use_shadow = H9.CORAL, soft, energy, shadow
    o = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(o)
    return o


def _mark_json(shot, k, cam, n, level):
    """The mark on screen per frame for the 2D pass (bGqrs's S13_mark.json format: H9._mark_geo + level + wrist)."""
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        out[f] = dict(H9._mark_geo(k, cam), level=round(level(f), 3), wrist=H9._px(cam, H9._forearm(k, 1.0)))
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, f"{shot}_mark.json"), "w") as fh:
        json.dump(dict(frames=out), fh)
    sc.frame_set(1)


def _shrimp(k, n, duck=None):
    """The puff-shrimp on his left shoulder (bGqrs's rig and placement); `duck` = (f0, f1): it squashes flat with its
    eyes shut, then peeks again. Big beat numbers keep the other beats out of the shot."""
    far = 10 ** 6
    if duck:
        beats = dict(dip=duck[0] + 2, arm1=duck[1] - 6, sit=far, land=far + 1)
    else:
        beats = dict(dip=far, arm1=-100, sit=-20, land=-10)
    return B._shoulder_shrimp(k, n, beats, name="ep03_shrimp_h10")


def _wing_keys(rig, f0, f1, amp=1.0, phase=0, fold=0.0):
    """Wing beats on 1s keyed frame by frame (no CYCLES modifier: S14 changes the wings mid-shot)."""
    for f in range(f0, f1 + 1):
        ph = (f - f0 + phase) % 4
        fluffmoth.wing_pose(rig, f, amp * fluffmoth.WING_BEAT[ph], amp * fluffmoth.WING_BEAT[(ph - 1) % 4] * 0.8,
                            fold + 0.12 * amp * (ph == 2))


def _clear_wings(rig):
    for w in rig["wings"]:
        w.animation_data_clear()


# ---------------------------------------------------------------- S12
S12_PERIOD = 40                     # frames per lap (~1.7 s): about 1.7 laps in the shot, "round and round"
S12_SCALE = 1.9                     # one big moth (S11's explainer moth, the camera a little wider)
S12_R, S12_DROP = 5.2, 5.6          # the ring's radius and how far below the light it flies: a ~42 degree bank
S12_EL = 16.0                       # the camera's elevation over the ring: side-on, the ring an ellipse


def build_s12():
    """S12, the explainer's second half (helper 4's S11 stage: the dark night ground, the coral glow; its 2D pass
    style): the light ABOVE, one fluffmoth flying round and round under it, banked so its back always faces the
    glow. The 2D pass (diorama_ep03/post_helper10.py) adds the glow line from the light to its back, the light's
    bloom, a dotted trail tracing the ring, and the dark hill silhouette, from S12_anchors.json."""
    from channels.monsters.diorama_ep02.helper4 import _backdrop
    from channels.monsters.diorama_ep03.helper4 import S11_BG, S11_ORB
    from channels.monsters.mk import diorama, look
    n = _frames("S12", 79)
    diorama.setup()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    sc.world.mist_settings.start, sc.world.mist_settings.depth = 500.0, 100.0
    for o in list(sc.objects):                                    # night: the sun down to a faint cool fill
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy *= 0.12
            o.data.color = (0.6, 0.7, 1.0)
    origin = Vector((0.0, -20.0, 0.0))
    _backdrop(S11_BG).location = origin + Vector((0, 0, -6.0))
    light = origin + Vector((0, 0, 4.0 + S12_DROP))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=light, segments=32, ring_count=16)
    orb = bpy.context.object
    orb.name = "s12_orb"
    orb.data.materials.append(look.flat("s12_orb", look.hexc("#ffe3d8"), 4.0))
    ld = bpy.data.lights.new("s12_orb_light", "POINT")
    ld.color, ld.energy, ld.shadow_soft_size = look.hexc(S11_ORB)[:3], 1400.0, 0.4
    lo = bpy.data.objects.new("s12_orb_light", ld)
    sc.collection.objects.link(lo)
    lo.location = light

    m = fluffmoth.build((0, 0, 0), name="s12moth")
    fluffmoth.flight_mode(m)
    m["root"].scale = (S12_SCALE,) * 3
    fluffmoth.flap(m, phase=1)
    # the camera looks along +X (from -X): start the moth at the front of the ring (nearest the camera), going
    # screen right, so it opens big and sweeps round behind
    c = light - Vector((0, 0, S12_DROP))
    prev = None
    track = {}
    for f in range(1, n + 1):
        a = math.pi + 2 * math.pi * (f - 1) / S12_PERIOD
        p = c + Vector((S12_R * math.cos(a), S12_R * math.sin(a), 0.12 * math.sin(f * 0.5)))
        track[f] = (p, Vector((-math.sin(a), math.cos(a), 0.0)))
    for f in range(1, n + 1, 2):
        p, h = track[f]
        m["root"].location = p
        anim.key(m["root"], "location", f, tuple(p), "CONSTANT")
        prev = fluffmoth.back_to(m, f, light, h, 1.0, "CONSTANT", prev)
    fluffmoth.spot_blink(m, 34)

    # the camera: side-on from -X, a little above the ring, a long lens, a slow push-in on 1s
    tgt = c + Vector((0, 0, 2.4))
    el = math.radians(S12_EL)
    cam_d = bpy.data.cameras.new("S12cam")
    cam = bpy.data.objects.new("S12cam", cam_d)
    sc.collection.objects.link(cam)
    c0 = tgt + 54.0 * Vector((-math.cos(el), 0.0, math.sin(el)))
    cam.location = c0
    cam.rotation_euler = (tgt - c0).to_track_quat("-Z", "Y").to_euler()
    cam_d.lens, cam_d.clip_end = 52.0, 400.0
    sc.camera = cam
    for f in range(1, n + 1):
        cam.location = c0.lerp(tgt, 0.07 * _ease((f - 1) / max(1, n - 1)))
        cam.keyframe_insert("location", frame=f)

    # the 2D pass's anchors: the light, the moth's body and its back (a point on the top of its body)
    anchors = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        bpy.context.view_layer.update()
        R = m["root"].matrix_world
        anchors[f] = dict(light=H9._px(cam, light), body=H9._px(cam, R.translation),
                          back=H9._px(cam, R @ Vector((0, 0, 0.55))), r_orb=H9._px(cam, light + Vector((0, 0, 0.42))))
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "S12_anchors.json"), "w") as fh:
        json.dump(dict(meta=dict(period=S12_PERIOD), frames=anchors), fh)
    sc.frame_set(1)
    return dict(frames=n, step=1, subject=[m["root"]])


# ---------------------------------------------------------------- S14
S14_HOLD = 12                        # the held beat: still circling, the hush
S14_ROLL = 6                         # frames to roll upside down
S14_STALL = 3                        # hanging upside down, a wobble, before the drop
S14_PLOPS = (32, 38, 44)             # the first three clear landings (sound: plop, plop, plop): hero moths
S14_HEROES = (32, 38, 44, 48)        # the four hero moths' landings (big, in the foreground)
S13_CUT = 45                         # S13's length (its frames, without the tail): the swarm's circling continues
S14_MOVE = (12, 30)                  # the camera's move from S13's framing down to the low, close landing view
UNDER_W = 3200.0                     # the coral glow above the wrist that lights the swarm from below (no shadows)


def _lie(k):
    """Kai exactly as S13 leaves him: flat on his back, head west, LIE with the left arm laid out palm up (bGqrs's
    _kai_drop final pose), hips S13_AT + 3 along the head direction."""
    hd = B._head_dir()
    yaw = math.pi + math.radians(B.S13_HEAD)
    spec = B._with_arm(B.LIE, 1.0)
    rot = (math.radians(90.0), 0, yaw)
    s15._pose(k, spec, (0, 0, 0), rot)
    twist = B._twist_for_palm_up(k)[0]
    s15._pose(k, [x for x in spec if x[0] != "left_hand"], (0, 0, 0), rot)
    B._twist(k, "left_lower_arm", twist)
    s15._aim(k, "left_hand", Euler(rot).to_matrix() @ Vector(dict(spec)["left_hand"]))
    hip = s15._world(k, "hips")
    target = B.S13_AT + hd * 3.0
    k["arm"].location += Vector((target.x - hip.x, target.y - hip.y, 0))
    s15._ground(k)
    bpy.context.view_layer.update()
    return hd


def _night_set(n):
    """X._world + helper 9's shared night (N9.night) and the Ep 2 village bGqrs's S13 uses."""
    X._world(n)
    try:
        from channels.monsters.diorama_ep03 import helper9 as N9
        N9.night(n)
    except (ImportError, AttributeError) as e:
        print("helper10: no shared night yet", e)
        B._night()
    try:
        H9.village_and_lake()
    except Exception as e:
        print("helper10: no village", e)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n


def _glow_cone(at, height=3.4, r0=0.3, r1=1.5, peak=0.3, name="h10_uplight"):
    """The light below, made visible: a soft coral cone of glow rising from the palm-up wrist through the grass (an
    additive, height-faded emission shell, no shadows), and a bright glowing disc on the grass at its foot."""
    import bmesh
    from channels.monsters.mk import look
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, cap_tris=False, segments=32, radius1=r0, radius2=r1, depth=height)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = Vector(at) + Vector((0, 0, height / 2))
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    else:
        m.blend_method = "BLEND"
    m.use_backface_culling = False
    nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    add = nt.nodes.new("ShaderNodeAddShader")
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em.inputs["Color"].default_value = (*H9.CORAL, 1.0)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")                 # bright at the foot, gone at the top
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.0, (peak, peak, peak, 1)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 1.0, (0, 0, 0, 1)
    lw = nt.nodes.new("ShaderNodeLayerWeight")                # softer at the silhouette edges
    lw.inputs["Blend"].default_value = 0.35
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    nt.links.new(lw.outputs["Facing"], inv.inputs[1])
    nt.links.new(ramp.outputs[0], mul.inputs[0])
    nt.links.new(inv.outputs[0], mul.inputs[1])
    nt.links.new(mul.outputs[0], em.inputs["Strength"])
    nt.links.new(em.outputs[0], add.inputs[0])
    nt.links.new(tr.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    o.visible_shadow = False
    disc = bpy.data.objects.new(name + "_foot", bpy.data.meshes.new(name + "_foot"))
    bpy.context.scene.collection.objects.link(disc)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=32, radius=0.7)
    bm.to_mesh(disc.data)
    bm.free()
    disc.location = Vector(at) + Vector((0, 0, 0.04))
    disc.data.materials.append(look.flat(name + "_foot", (*H9.CORAL, 1.0), strength=1.0))
    disc.visible_shadow = False
    return o


def _hero_spots(wrist, cam_end, feet_dir):
    """The four hero moths land in the foreground, in front of the glowing wrist and a little along toward his feet
    (so his head and the glow stay clear behind them): a loose row ~1.7 apart, the nearest toward the lens."""
    to_cam = Vector((cam_end.x - wrist.x, cam_end.y - wrist.y, 0)).normalized()
    side = Vector((-to_cam.y, to_cam.x, 0))
    H = wrist + to_cam * 2.3 + Vector(feet_dir) * 2.6
    H.z = 0.0
    return [H + side * -1.75, H + to_cam * -0.5, H + side * 1.8 + to_cam * 0.1, H + to_cam * 1.35 + side * 0.4], H


def _ring_spots(n_spots, wrist, hips, hd, taken, cam_end, H, seed=14):
    """The rest land in a loose ring round the wrist (2-8 units): none on Kai's body, ~1.4 apart (splayed wings), and
    none in the view between the last camera and the heroes."""
    rnd = random.Random(seed)
    feet, crown = hips - hd * 4.2, hips + hd * 4.4
    ab = crown - feet
    cv = Vector((cam_end.x - H.x, cam_end.y - H.y, 0))
    spots = []
    for gap in (1.4, 1.15, 0.95):
        tries = 0
        while len(spots) < n_spots and tries < 6000:
            tries += 1
            a = rnd.uniform(0, 2 * math.pi)
            r = 2.0 + 6.0 * math.sqrt(rnd.random())
            p = Vector((wrist.x + r * math.cos(a), wrist.y + r * math.sin(a), 0.0))
            t = max(0.0, min(1.0, (p - feet).dot(ab) / ab.length_squared))
            if (p - (feet + ab * t)).length < 1.8:
                continue
            tc = max(0.0, min(1.0, (p - H).dot(cv) / cv.length_squared))
            if (p - (H + cv * tc)).length < 2.2:                 # in front of the heroes
                continue
            if any((p - q).length < gap for q in spots + taken):
                continue
            spots.append(p)
    print("S14 ring spots", len(spots), "of", n_spots)
    return spots


def build_s14():
    n = _frames("S14", 84)
    _night_set(n)
    sc = bpy.context.scene
    k = hero.load((0, 0, 0), scale=B.SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    hd = _lie(k)
    s15._key_pose(k, 1)
    s15._flush_keys(k)
    hips = s15._world(k, "hips")
    wrist = H9._forearm(k, 1.0)
    mark = H9._forearm(k, H9.MARK_U)
    B._grass_at(wrist)
    acting.grass_round(hips, hd)
    sh = _shrimp(k, n)

    # the light below: helper 9's mark key (6000 W, on the forearm), a strong coral glow above the wrist that lights
    # the swarm from underneath (their backs once they roll), and the visible cone rising through the grass
    try:
        from channels.monsters.diorama_ep03 import helper9 as N9
        N9.mark(k)
    except (ImportError, AttributeError):
        _lamp("h10_s14_key", B.S13_LIGHT * 2.0, 0.2).location = mark + Vector((0, 0, 0.5))
    und = _lamp("h10_s14_under", UNDER_W, 1.2, shadow=False)
    und.location = wrist + Vector((0, 0, 2.6))
    _glow_cone(wrist)
    light = Vector(mark)                                          # what the moths keep their backs to (S13's centre)

    # camera: S13's last frame (bGqrs's camera_at(45)), then down and in to a low, close view of the landing spot in
    # front of the wrist (S14_MOVE); a slow drift after
    _, beats13 = B.s13_beats()
    poses = B.camera_poses(B._frames("S13", 57), beats13)
    c0, t0, lens0, _ = B.camera_at(S13_CUT, poses)
    cam_end_guess = wrist + Vector((c0.x - wrist.x, c0.y - wrist.y, 0)).normalized() * 9.5
    hero_spots, H = _hero_spots(wrist, cam_end_guess, -hd)
    to_cam = Vector((c0.x - H.x, c0.y - H.y, 0)).normalized()
    c1 = H + to_cam * 7.6 + Vector((0, 0, 2.1))
    head = s15._world(k, "head")
    t1 = H.lerp(head, 0.45) + Vector((0, 0, 0.9))
    c2 = H + to_cam * 7.0 + Vector((0, 0, 1.9))
    t2 = H.lerp(head, 0.5) + Vector((0, 0, 0.8))
    old_blur = X.v2.BLUR
    X.v2.BLUR = 3.0
    cam = None
    ms = sc.world.mist_settings
    for f in range(1, n + 1):
        if f <= S14_MOVE[1]:
            u = _ease((f - S14_MOVE[0]) / (S14_MOVE[1] - S14_MOVE[0]))
            c, t, ln = c0.lerp(c1, u), t0.lerp(t1, u), lens0 + (26.0 - lens0) * u
        else:
            u = _ease((f - S14_MOVE[1]) / max(1, n - S14_MOVE[1]))
            c, t, ln = c1.lerp(c2, u), t1.lerp(t2, u), 26.0
        v = c - t
        dist = v.length
        tilt = math.degrees(math.asin(max(-1.0, min(1.0, v.z / dist))))
        yaw = math.degrees(math.atan2(-v.x, -v.y))
        cam = X.v2._cam("S14cam", f, tuple(t), dist, tilt, yaw, ln, (0.0, 0.0), cam)
        ms.start, ms.depth = dist * 2.5, dist * 2.0
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    X.v2.BLUR = old_blur
    sc.camera = cam
    cam.data.clip_end = 600.0

    # the swarm: S13's members (bGqrs's layout), continuing their circles; the four lowest are the heroes
    lay = B.swarm_layout()
    order = sorted(range(len(lay)), key=lambda i: lay[i]["h"])
    heroes = order[:len(S14_HEROES)]
    rest = order[len(S14_HEROES):]
    ring = _ring_spots(len(rest), wrist, hips, hd, hero_spots, c2, H)
    spot_of, t_land = {}, {}
    for j, i in enumerate(heroes):
        spot_of[i], t_land[i] = hero_spots[j], S14_HEROES[j]
    for j, i in enumerate(rest):
        spot_of[i] = ring[j % len(ring)]
        t_land[i] = int(48 + j * 18 / max(1, len(rest) - 1)) + random.Random(i).randint(-1, 1)

    def place(i, rnd):
        return tuple(B.swarm_at(lay[i], S13_CUT + 1, light)), lay[i]["s"]
    rigs = fluffmoth.swarm(len(lay), place, name="m14_", seed=13, far=lambda i, loc, s: i not in heroes)
    # (no decimation: the heroes come close to the lens, and the copies share their meshes)

    landings, hero_track = [], {}
    rnd = random.Random(15)
    for i, rig in enumerate(rigs):
        L = lay[i]
        s = L["s"]
        is_hero = i in heroes
        spot = spot_of[i]
        f_land = t_land[i]
        if is_hero:                                               # low over its spot, near the lens: a short fall
            h_fall = 3.6
            fall = 8
        else:
            h_fall = None
            fall = int(round(8 + 0.6 * L["h"]))
        f_drop = f_land - fall
        f_stall = f_drop - S14_STALL
        f_roll = max(S14_HOLD, f_stall - S14_ROLL)
        root = rig["root"]
        _clear_wings(rig)
        prev, drop_from = None, None
        heading = B.swarm_heading(L, S13_CUT + 1)
        spin = rnd.choice((1, -1))
        track = {}
        for f in range(1, f_land, 2):
            ff = S13_CUT + f
            if f > f_stall:                                       # the stall: the circling dies away
                ff = S13_CUT + f_stall + (f - f_stall) * 0.25
            circ = B.swarm_at(L, ff, light)
            heading = B.swarm_heading(L, ff)
            if is_hero:                                           # drifts over to hang above its landing spot
                over = Vector((spot.x, spot.y, h_fall))
                circ = circ.lerp(over, _ease((f - 4) / max(1, f_roll - 2)))
            if f < f_drop:
                p = circ.copy()
                if f >= f_stall:
                    p.z -= 0.25 * (f - f_stall) / max(1, S14_STALL)
                drop_from = p.copy()
                root.location = p
                amt = 0.12 + 0.88 * _ease((f - f_roll) / S14_ROLL) if f >= f_roll else 0.12
                prev = fluffmoth.back_to(rig, f, light, heading, amt, "CONSTANT", prev)
                if f_stall <= f < f_drop:                         # the "!" wobble: a quick rock while it hangs
                    w = 0.35 * (1 if (f - f_stall) % 4 < 2 else -1)
                    e = Euler(prev)
                    e.rotate(Euler((0, w, 0)))
                    prev = e
                    anim.key(root, "rotation_euler", f, tuple(e), "CONSTANT")
            else:                                                 # the tumble: gravity, a flip, drifting to its spot
                u = (f - f_drop) / max(1, fall)
                q = drop_from.lerp(Vector((spot.x, spot.y, drop_from.z)), _ease(u))
                q.z = drop_from.z + (fluffmoth.BACK_REST * s - drop_from.z) * u * u
                root.location = q
                base = fluffmoth._basis(Vector((0, 0, -1)), heading)
                m = base @ Matrix.Rotation(spin * 2 * math.pi * (1 - u), 3, "X")
                e = m.to_euler("XYZ", prev) if prev is not None else m.to_euler("XYZ")
                anim.key(root, "rotation_euler", f, tuple(e), "CONSTANT")
                prev = e
            anim.key(root, "location", f, tuple(root.location), "CONSTANT")
            track[f] = root.location.copy()
        _wing_keys(rig, 1, f_stall - 1, phase=i % 4)
        _wing_keys(rig, f_stall, f_drop - 1, amp=1.35, phase=i % 4)
        _wing_keys(rig, f_drop, f_land - 1, amp=0.7, phase=i % 4, fold=0.2)
        yaw = math.atan2(heading.x, -heading.y)
        root.rotation_euler = Euler((0.0, math.pi, yaw))
        fluffmoth.upside_down(rig, f_land, n, land_at=(spot.x, spot.y, 0.0), seed=30 + i)
        anim.key(root, "location", f_land, (spot.x, spot.y, fluffmoth.BACK_REST * s), "CONSTANT")
        anim.squash(rig["body"], f_land, -0.3, "CONSTANT")
        anim.squash(rig["body"], f_land + 2, 0.08, "CONSTANT")
        anim.squash(rig["body"], f_land + 4, 0.0, "CONSTANT")
        landings.append(dict(moth=i, frame=f_land, at=[round(spot.x, 3), round(spot.y, 3), 0.0], scale=round(s, 3),
                             yaw=round(yaw, 4), hero=is_hero))
        if is_hero:
            hero_track[i] = dict(roll=f_roll, stall=f_stall, drop=f_drop, land=f_land, s=s)

    # Kai: determined (S13's end), eyes on the swarm, then following them down; on the plops, a grin starts
    acting.face_keys(k, 1, eye_brow_down=0.65, face_angry=0.2, mouth_short=0.2, face_happy=0.12)
    acting.face_keys(k, S14_PLOPS[1], eye_brow_down=0.2, face_happy=0.45, mouth_short=0.0, face_angry=0.0)
    acting.look_at(k, light + Vector((0, 0, 7.0)), 1, S14_PLOPS[0] - 6, darts=True, seed=14)
    acting.look_at(k, H + Vector((0, 0, 0.6)), S14_PLOPS[0] - 6, n, darts=True, seed=15)
    acting.blink(k, 1, n, every=(40, 64), seed=14, at=(S14_PLOPS[0] + 2,))

    # for the 2D pass (dust puffs; the heroes' roll arcs and stall wobble), S15 (the spots) and the sound (plops)
    os.makedirs(BUILD, exist_ok=True)
    for d in landings:
        sc.frame_set(d["frame"])
        d["px"] = H9._px(cam, Vector(d["at"]))
    heroes_px = {}
    for i, hdat in hero_track.items():
        rows = {}
        for f in range(1, hdat["land"] + 1):
            sc.frame_set(f)
            bpy.context.view_layer.update()
            p = rigs[i]["root"].matrix_world.translation
            c = H9._px(cam, p)
            e = H9._px(cam, p + Vector((0, 0, 0.9 * hdat["s"])))   # ~the body's radius on screen
            rows[f] = c[:2] + [round(math.hypot(e[0] - c[0], e[1] - c[1]), 1)]
        heroes_px[i] = dict(hdat, px=rows)
    sc.frame_set(1)
    data = dict(plops=list(S14_PLOPS), heroes=list(S14_HEROES), hold=S14_HOLD,
                landings=sorted(landings, key=lambda d: d["frame"]))
    for path in (os.path.join(BUILD, "S14_landings.json"), LANDINGS):
        with open(path, "w") as fh:
            json.dump(data, fh, indent=1)
    with open(os.path.join(BUILD, "S14_heroes.json"), "w") as fh:
        json.dump(heroes_px, fh)
    for d in landings:
        if d["hero"]:
            print("S14 hero lands", d["frame"], "at px", d["px"])
    sc.frame_set(n)
    print("S14 end: head px", H9._px(cam, s15._world(k, "head")), "wrist px", H9._px(cam, wrist))
    if not _still():
        _mark_json("S14", k, cam, n, lambda f: 1.1 + 0.05 * math.sin(f / 5.0))
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n),
                subject=[k["arm"], sh["root"]] + [r["root"] for r in rigs] + list(k.get("cap", [])))


def s14_landings():
    """S14's landings (for S15 and the sound), from the committed channels/monsters/diorama_ep03/S14_landings.json:
    a list of dict(moth, frame, at=[x, y, 0], scale, yaw, px), sorted by frame. No Blender needed."""
    with open(LANDINGS) as fh:
        return json.load(fh)["landings"]


SHOTS = {"S12": build_s12, "S14": build_s14}
