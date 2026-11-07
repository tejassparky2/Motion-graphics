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
S12_SCALE = 1.5                     # one big moth (S11's explainer moth, the camera a little wider)
S12_R, S12_DROP = 5.0, 5.5          # the ring's radius and how far below the light it flies: a ~42 degree bank
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
    c0 = tgt + 50.0 * Vector((-math.cos(el), 0.0, math.sin(el)))
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
S14_STALL = 3                        # hanging upside down, wings fluttering, before the drop
S14_PLOPS = (32, 38, 44)             # the first three clear landings (sound: plop, plop, plop)
S13_CUT = 45                         # S13's length (its frames, without the tail): the swarm's circling continues


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


def _swarm_layout(n_moths, seed=13):
    """bGqrs's S13 swarm, member by member (the same random sequence: scale, radius, height, start angle, turn rate),
    so S14 continues S13's circling."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n_moths):
        s = MOTH_S * rnd.uniform(0.75, 1.15)
        r = rnd.uniform(2.2, 7.5)
        h = rnd.uniform(4.5, 11.0)
        a0 = rnd.uniform(0, 2 * math.pi)
        w = rnd.choice((-1, 1)) * rnd.uniform(0.9, 1.6) * 2 * math.pi / (FPS * 6.0)
        out.append(dict(s=s, r=r, h=h, a0=a0, w=w))
    return out


def _landing_spots(n_moths, wrist, hips, hd, seed=14):
    """Where each moth lands on its back: a loose ring round the glowing wrist (1.5-5.5 units), none on Kai's body
    (the strip from his feet to past his head) and not too close to each other."""
    rnd = random.Random(seed)
    feet, crown = hips - hd * 4.2, hips + hd * 4.4
    spots = []
    tries = 0
    while len(spots) < n_moths and tries < 20000:
        tries += 1
        a = rnd.uniform(0, 2 * math.pi)
        r = 1.5 + 4.0 * math.sqrt(rnd.random())
        p = Vector((wrist.x + r * math.cos(a), wrist.y + r * math.sin(a), 0.0))
        ab = crown - feet
        t = max(0.0, min(1.0, (p - feet).dot(ab) / ab.length_squared))
        if (p - (feet + ab * t)).length < 1.5:                   # on his body
            continue
        if any((p - q).length < 0.85 for q in spots):
            continue
        spots.append(p)
    return spots


def build_s14():
    n = _frames("S14", 84)
    _set(n)
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

    # the light below: the coral key at the mark and the broad glow above the wrist (S13's end levels)
    key = _lamp("h10_s14_key", B.S13_LIGHT * 1.1, 0.2)
    key.location = mark + Vector((0, 0, 0.5))
    und = _lamp("h10_s14_under", B.S13_UNDER * 1.1, 1.5, shadow=False)
    und.location = mark + Vector((0, 0, 1.6))
    light = mark + Vector((0, 0, 0.3))                            # what the moths keep their backs to

    lay = _swarm_layout(B.SWARM_N)
    spots = _landing_spots(len(lay), wrist, hips, hd)
    rigs = fluffmoth.swarm(len(lay), lambda i, rnd: (Vector(light) + Vector((0, 0, lay[i]["h"])), lay[i]["s"]),
                           name="m14", seed=14, far=lambda i, loc, s: s < MOTH_S * 0.85)

    # who lands when: the three lowest moths give the clear plop-plop-plop, the rest follow by height
    order = sorted(range(len(lay)), key=lambda i: lay[i]["h"])
    t_land = {}
    for j, i in enumerate(order):
        if j < len(S14_PLOPS):
            t_land[i] = S14_PLOPS[j]
        else:
            t_land[i] = int(46 + (j - 3) * 20 / max(1, len(order) - 4)) + random.Random(i).randint(-1, 1)
    landings = []
    rnd = random.Random(15)
    for i, rig in enumerate(rigs):
        L = lay[i]
        s, h = L["s"], L["h"]
        fall = int(round(8 + 0.7 * h))
        f_land = t_land[i]
        f_drop = f_land - fall
        f_stall = f_drop - S14_STALL
        f_roll = max(S14_HOLD, f_stall - S14_ROLL)
        spot = spots[i % len(spots)]
        root = rig["root"]
        _clear_wings(rig)
        prev = None
        drop_from = None
        heading = Vector((0, 1, 0))
        spin_axis = rnd.choice((1, -1))
        for f in range(1, f_land, 2):
            a = L["a0"] + L["w"] * (S13_CUT + f)
            if f > f_stall:                                        # the stall: the circling dies away
                slow = 1.0 - 0.8 * _ease((f - f_stall) / max(1, f_drop - f_stall))
                a = L["a0"] + L["w"] * (S13_CUT + f_stall + (f - f_stall) * slow)
            circ = Vector((light.x + L["r"] * math.cos(a), light.y + L["r"] * math.sin(a), light.z + h))
            circ.z += 0.3 * math.sin(f / 9.0 + i)
            heading = Vector((-math.sin(a), math.cos(a), 0.0)) * (1 if L["w"] > 0 else -1)
            if f < f_drop:
                p = circ
                if f >= f_stall:                                   # hangs, sinking a little
                    p = p - Vector((0, 0, 0.25 * (f - f_stall) / max(1, S14_STALL)))
                drop_from = p.copy()
                root.location = p
                amt = 0.12 + 0.88 * _ease((f - f_roll) / S14_ROLL) if f >= f_roll else 0.12
                prev = fluffmoth.back_to(rig, f, light, heading, amt, "CONSTANT", prev)
            else:                                                  # the tumble: gravity, a flip, drifting to its spot
                u = (f - f_drop) / max(1, fall)
                q = drop_from.lerp(Vector((spot.x, spot.y, drop_from.z)), _ease(u))
                q.z = drop_from.z + (fluffmoth.BACK_REST * s - drop_from.z) * u * u
                root.location = q
                base = fluffmoth._basis(Vector((0, 0, -1)), heading)              # upside down
                m = base @ Matrix.Rotation(spin_axis * 2 * math.pi * (1 - u), 3, "X")
                e = m.to_euler("XYZ", prev) if prev is not None else m.to_euler("XYZ")
                anim.key(root, "rotation_euler", f, tuple(e), "CONSTANT")
                prev = e
            anim.key(root, "location", f, tuple(root.location), "CONSTANT")
        # the wings: steady beats while circling, frantic in the stall, flailing in the fall
        _wing_keys(rig, 1, f_stall - 1, phase=i % 4)
        _wing_keys(rig, f_stall, f_drop - 1, amp=1.35, phase=i % 4)
        _wing_keys(rig, f_drop, f_land - 1, amp=0.7, phase=i % 4, fold=0.2)
        # the landing: on its back, legs waving (helper 6's pose; its rest height scaled to this moth); the plop squash
        root.rotation_euler = Euler((0.0, math.pi, math.atan2(heading.x, -heading.y)))
        fluffmoth.upside_down(rig, f_land, n, land_at=(spot.x, spot.y, 0.0), seed=30 + i)
        anim.key(root, "location", f_land, (spot.x, spot.y, fluffmoth.BACK_REST * s), "CONSTANT")
        anim.squash(rig["body"], f_land, -0.3, "CONSTANT")
        anim.squash(rig["body"], f_land + 2, 0.08, "CONSTANT")
        anim.squash(rig["body"], f_land + 4, 0.0, "CONSTANT")
        landings.append(dict(moth=i, frame=f_land, at=[round(spot.x, 3), round(spot.y, 3), 0.0], scale=round(s, 3)))

    # Kai: determined (S13's end), eyes on the swarm, then following them down; on the plops, a grin starts
    acting.face_keys(k, 1, eye_brow_down=0.65, face_angry=0.2, mouth_short=0.2, face_happy=0.12)
    acting.face_keys(k, S14_PLOPS[1], eye_brow_down=0.2, face_happy=0.45, mouth_short=0.0, face_angry=0.0)
    acting.look_at(k, light + Vector((0, 0, 7.0)), 1, S14_PLOPS[0] - 6, darts=True, seed=14)
    acting.look_at(k, light + Vector((0, 0, 2.0)), S14_PLOPS[0] - 6, n, darts=True, seed=15)
    acting.blink(k, 1, n, every=(40, 64), seed=14, at=(S14_PLOPS[0] + 2,))

    # camera: S13's end framing (north of him, toward his feet, looking south over the village; the light low, the
    # swarm high), easing down and in to the grass as the moths fall; on 1s
    body_mid = B.S13_AT + hd * 2.4
    left = Vector((-hd.y, hd.x, 0)) * -1.0
    c_dir = (left * 1.0 - hd * 0.32).normalized()
    t0 = body_mid + hd * 0.4 + Vector((0, 0, 4.2))               # = S13's last frame (bGqrs's t1 / c1)
    t1 = body_mid + hd * 0.6 + Vector((0, 0, 1.2))
    c0 = t0 + c_dir * 21.0 + Vector((0, 0, 1.0))
    c1 = t1 + c_dir * 19.0 + Vector((0, 0, 4.6))
    cam = B._cam_from("S14cam", n, c0, c1, t0, t1, 30.0)
    cam.data.clip_end = 600.0

    # for the 2D pass (dust puffs at each landing, on its frame), S15 (the landing spots) and the sound (plops)
    os.makedirs(BUILD, exist_ok=True)
    for d in landings:
        sc.frame_set(d["frame"])
        d["px"] = H9._px(cam, Vector(d["at"]))
    sc.frame_set(1)
    with open(os.path.join(BUILD, "S14_landings.json"), "w") as fh:
        json.dump(dict(plops=list(S14_PLOPS), hold=S14_HOLD, landings=sorted(landings, key=lambda d: d["frame"])),
                  fh, indent=1)
    if not _still():
        _mark_json("S14", k, cam, n, lambda f: 1.1 + 0.05 * math.sin(f / 5.0))
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n),
                subject=[k["arm"], sh["root"]] + [r["root"] for r in rigs] + list(k.get("cap", [])))


SHOTS = {"S12": build_s12, "S14": build_s14}
