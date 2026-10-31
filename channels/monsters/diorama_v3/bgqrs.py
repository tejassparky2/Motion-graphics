"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), bGqrs's shots: S15b (new), S01 and S16-S18
re-done with Kai's LYING_V3 pose and the acting library (mk/acting.py).

The after-the-snap world, the shrimp and the cameras come from the v2 builder (channels/monsters/diorama/bgqrs.py);
what changes: v3's frame counts (ep01v3/timing.json), every beat keyed on its word in v3's timing, Kai lying in
LYING_V3 (a knee up, an arm flung over his head, grass round him), his eyes alive (blinks every 2-4 s, looks with
darts), faces that match the line, and the sapling the snap cut an inch from his head (S15b on).

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S15b OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import json
import math
import os
import re

import bpy
from mathutils import Vector

from channels.monsters.diorama import bgqrs as v2                # the world, the shrimp, the camera moves
from channels.monsters.ep01v2 import bgqrs as s3d                 # Kai's face keys, the shrimp's lock-on and claw
from channels.monsters.mk import acting, anim, diorama, hero, look, meadow

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ANCHORS = os.path.join(ROOT, "build", "monsters", "diorama_v3")
TIMING = os.path.join(ROOT, "channels", "monsters", "ep01v3", "timing.json")
HIPS, HEAD_DIR, UP, EAST = v2.HIPS, v2.HEAD_DIR, v2.UP, v2.EAST
BLUR = v2.BLUR


# ---------------------------------------------------------------- v3 timing

def _timing():
    with open(TIMING) as fh:
        return json.load(fh)


def frames(shot):
    """render_frames (frames + the 12-frame handle) of a v3 shot."""
    return {s["shot"]: s["render_frames"] for s in _timing()["shots"]}[shot]


def words(shot):
    """[(word, first frame, last frame)] of the shot's line(s), frames 1-based within the shot (v3 timing)."""
    t = _timing()
    start = {s["shot"]: s["start"] for s in t["shots"]}[shot]
    out = []
    for ln in t["lines"]:
        if ln["scene"] != shot:
            continue
        for w in ln["words"]:
            out.append((re.sub(r"[^a-z']", "", w["w"].lower()), 1 + round((w["start"] - start) * 24),
                        1 + round((w["end"] - start) * 24)))
    return out


def at(shot, word, n=0, end=False):
    """The frame where `word` starts (or ends) in the shot's line, the n-th time it is said."""
    hits = [w for w in words(shot) if w[0] == word]
    return hits[n][2 if end else 1]


# ---------------------------------------------------------------- the world after the snap, v3

def _sapling(rig, n):
    """The young tree the snap cut beside his head (helper 10's sapling_spot(), on the blast line west of his head):
    the shared splintered stump (diorama.splinter_stump) once it lands, with a thin smoke wisp that drifts AWAY from
    his head (west and north), so no puff ever crosses his face or cap. Stays in every later shot."""
    head = s3d.kai_point(rig, "head")
    if hasattr(diorama, "sapling_spot"):
        x, y = diorama.sapling_spot()[:2]
        p = Vector((x, y, 0.0))
    else:
        p = head - EAST * 1.3 + UP * 0.2
    blast = diorama.MAP.get("blast", diorama.MAP["shrimp"])
    if hasattr(diorama, "splinter_stump"):
        stump = diorama.splinter_stump((p.x, p.y, 0.0), 0.3, 1.2, blast_from=blast, seed=1, smoke=None)
    else:
        bark = bpy.data.materials.get("stump_bark") or diorama.lit_paint("stump_bark", "#3c261c", "#5e3e2c",
                                                                         "#80604a")
        ring = bpy.data.materials.get("stump_hot") or look.flat("stump_hot", look.hexc("#ff7a3d"), 2.2)
        core = bpy.data.materials.get("stump_core") or look.flat("stump_core", look.hexc("#ffe08a"), 3.0)
        to_blast = Vector(blast) - Vector((p.x, p.y))
        stump = meadow._slice((p.x, p.y, 0.0), 0.32, 1.25, math.radians(34),
                              math.atan2(to_blast.y, to_blast.x) - math.pi / 2, bark, ring, core)
    stump.name = "sapling_stump"
    _wisp(p + Vector((0, 0, 1.3)), -EAST * 1.6 + UP * 0.8, n)
    return stump


def _wisp(src, drift, n, every=9, rise=3.5, size=0.45, seed=7):
    """A thin smoke wisp from `src`: small painted puffs that bud, rise and drift along `drift` (world units over a
    puff's life) as they swell and break up (1s, VFX)."""
    import random
    rnd = random.Random(seed)
    m = meadow.smoke_mat()
    f = -40
    while f < n + 10:
        life = rnd.randint(30, 42)
        pp = bpy.data.objects.new("puff_wisp", None)
        bpy.context.scene.collection.objects.link(pp)
        for _ in range(3):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=rnd.uniform(0.4, 0.7),
                                                 location=(rnd.uniform(-0.3, 0.3), rnd.uniform(-0.2, 0.2),
                                                           rnd.uniform(-0.1, 0.3)))
            lobe = bpy.context.object
            lobe.data.materials.append(m)
            lobe.parent = pp
        sz = size * rnd.uniform(0.75, 1.2)
        anim.key(pp, "scale", f - 1, 0.001, "CONSTANT")
        anim.key(pp, "scale", f, sz * 0.3, "LINEAR")
        anim.key(pp, "location", f, tuple(src), "LINEAR")
        anim.key(pp, "scale", f + life * 0.6, sz)
        anim.key(pp, "scale", f + life, 0.001)
        anim.key(pp, "location", f + life, tuple(src + drift * rnd.uniform(0.8, 1.2) +
                                                 Vector((0, 0, rise * rnd.uniform(0.8, 1.2)))), "LINEAR")
        f += every + rnd.randint(-2, 2)


def _set(n):
    """The island after v3's snap, which fired at Kai along diorama.BLAST_LINE (helper 10): the north trees stand; the
    young grove south-east of him and the sapling by his head are cut. island(grove="cut") leaves both unplanted;
    their glowing, smoking stumps go in their place (the sapling's in _sapling). Before helper 10's API lands: the
    plain island. Returns the grove's stump spots."""
    if hasattr(diorama, "grove_spots"):
        diorama.island(seed=31, grove="cut")
        spots = list(diorama.grove_spots())
        diorama.stumps(spots, diorama.MAP.get("blast", (0.1, 0.4)))
        meadow.smoke([(x, y, diorama.TREE * 0.4) for x, y, *_ in spots[:5]], -50, n + 10, every=16, rise=9.0,
                     size=diorama.TREE * 0.4)
    else:
        diorama.island(seed=31)
        spots = []
    for name, strength in (("stump_hot", 2.2), ("stump_core", 3.0)):
        m = bpy.data.materials.get(name)
        em = next((nd for nd in m.node_tree.nodes if nd.type == "EMISSION"), None) if m and m.use_nodes else None
        if em is not None:
            em.inputs["Strength"].default_value = strength
    return spots


def _world(shot, claw="face", shrimp=True, head=None, **shrimp_kw):
    n = frames(shot)
    diorama.setup()
    stumps = _set(n)
    rig = hero.load((0, 0, 0), scale=s3d.KAI_SCALE, outfit="world")
    acting.lie(rig, HIPS, HEAD_DIR, spec=acting.LYING_V3_L, head=head)   # left arm flung: the sapling is west
    hero.line_width(rig, 0.0025)
    sh = v2._shrimp(rig, n, claw, **shrimp_kw) if shrimp else None
    diorama.sunbeam(s3d.kai_point(rig, "chest"), radius=7.0)
    v2._dust(rig, n)
    _sapling(rig, n)
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, n
    return n, rig, sh, stumps


def _anchors(shot, n, cam, rig, sh=None, extra=None):
    """Screen positions (720x1280, top-left origin) per frame of his eyes, the top of his head, the claw tip and
    `extra` points, for the 2D pass (build/monsters/diorama_v3/<shot>_anchors.json)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        pts = {k: s3d.kai_point(rig, k) for k in ("eyes", "eye_l", "eye_r", "nose", "temple", "head")}
        pts["crown"] = _crown(rig)
        if sh is not None:
            pts["tip"] = s3d.claw_tip(sh)
        for k, fn in (extra or {}).items():
            pts[k] = fn()
        row = {}
        for k, p in pts.items():
            v = world_to_camera_view(sc, cam, p)
            row[k] = (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))
        out[f] = row
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)
    sc.frame_set(1)


def _crown(rig):
    """Just above the top of his head (past the cap), along the head bone: where knocked-out stars circle."""
    m = rig["arm"].matrix_world @ rig["bone"]("head").matrix
    return m.translation + (m.to_3x3() @ Vector((0, 1, 0))).normalized() * 0.3 * s3d.KAI_SCALE


def _subject(rig, sh=None):
    return [rig["arm"]] + ([sh["root"]] if sh else []) + list(rig.get("cap", []))


# ---------------------------------------------------------------- the shots

def s15b():
    """It missed me by an inch. Close and low over him (tilt 50, from his feet so his face shows under the cap's
    brim), a slow push-in on 1s: Kai flat on his back in LYING_V3, dazed (knocked-out stars in 2D), the cut sapling
    smoking right beside his head. His eyes slide to the stump on "inch"; slow dazed blinks."""
    n, rig, sh, _ = _world("S15b", shrimp=False)
    eyes = s3d.kai_point(rig, "eyes")
    stump = bpy.data.objects["sapling_stump"]
    sp = stump.matrix_world.translation + Vector((0, 0, 1.0))
    tgt = eyes.lerp(sp, 0.45) - UP * 0.4
    cam = diorama.camera("cam_s15b", tgt, dist=32.0, tilt=50.0, lens=110.0, blur=BLUR)
    v2._move(cam, n, [(1, 50.0, 32.0, 110.0), (n, 50.0, 28.0, 110.0)], lambda f: tgt)
    inch = at("S15b", "inch")
    acting.expression(rig, "dazed", 1)
    acting.look_at(rig, eyes + UP * 8 + Vector((0, 0, 6)), 1, inch - 6, darts=True, seed=4)   # unfocused, upward
    acting.look_at(rig, sp, inch - 4, n, darts=True, seed=5)       # ... then the stump an inch away
    acting.blink(rig, 1, n, every=(30, 44), seed=6)                # dazed: slow, heavy blinks
    _anchors("S15b", n, cam, rig, extra={"stump": lambda: sp})
    return dict(frames=n, step=2, ones=(1, n), subject=_subject(rig))


def s01():
    """FRAME 0, the hook (v2's approved staging and camera, S01_CAM): Kai in LYING_V3 under the shrimp, its big
    locked-on eyes and the claw cocked by his cheek; terror face, whispered lips on the v3 words, his eyes darting
    to the claw. Smoke and embers over the top third. Locked (2s); the push-in is 2D."""
    n, rig, sh, _ = _world("S01", lean=v2.S01_LEAN)
    t, d, lens, yaw, up, far = v2.S01_CAM
    fwd = Vector((math.sin(math.radians(yaw)), math.cos(math.radians(yaw)), 0))
    pair = s3d.kai_point(rig, "eyes").lerp(sh["root"].matrix_world.translation, 0.5)
    aim = pair + UP * up + fwd * far
    cam = diorama.camera("cam_s01", aim, dist=d, tilt=t, yaw=yaw, lens=lens, blur=BLUR)
    v2._move(cam, n, [(1, t, d, lens), (n, t, d, lens)], lambda f: aim, yaw=yaw)
    crown = _crown(rig)                                            # the top third, kept well past his cap: a puff
    v2._drift(n, ((crown.x - 6, crown.x + 6), (crown.y + 6.5, crown.y + 16), (2.0, 6.0)))   # drifts 4 units south
    acting.expression(rig, "terror", 1)
    w = words("S01")
    if w:                                                          # whispered lips over the held terror face
        split = next((i for i, x in enumerate(w) if i and x[1] - w[i - 1][2] > 6), len(w))
        for seg in (w[:split], w[split:]):
            if seg:
                acting.lips(rig, seg[0][1], seg[-1][2], seed=seg[0][1])
    acting.look_at(rig, s3d.claw_tip(sh), 1, n, darts=True, seed=8)
    _anchors("S01", n, cam, rig, sh)
    return dict(frames=n, step=2, subject=_subject(rig, sh))


def _keycam(cam, f, aim, tilt, dist, lens, yaw=0.0):
    """Key the diorama camera at frame f: `dist` from `aim` at `tilt`/`yaw`, the lens, the tilt-shift focus and
    f-stop, and the haze (1s)."""
    el, az = math.radians(tilt), math.radians(yaw)
    back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.location = Vector(aim) + back * dist
    cam.rotation_euler = (-back).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = lens
    cam.data.dof.focus_distance = dist
    cam.data.dof.aperture_fstop = diorama.fstop_for(dist, lens, BLUR)
    for path in ("location", "rotation_euler"):
        cam.keyframe_insert(path, frame=f)
    cam.data.keyframe_insert("lens", frame=f)
    cam.data.dof.keyframe_insert("focus_distance", frame=f)
    cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
    ms = bpy.context.scene.world.mist_settings
    ms.start, ms.depth = dist * 0.97, dist * 0.55
    ms.keyframe_insert("start", frame=f)
    ms.keyframe_insert("depth", frame=f)


def _beats(shot, **beats):
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, f"{shot}_beats.json"), "w") as fh:
        json.dump(beats, fh)


S16_CLOSE = (72.0, 11.0, 120.0, 0.0)   # tilt, dist, lens, yaw: close on his face from his feet side (under the cap's
#                                        brim), tight enough that the shrimp on his chest and its claw stay out of
#                                        frame (projection-checked: no shrimp pixel until the pull back on "chest")


def s16():
    """When I opened my eyes, it was on my chest. A reveal (coordinator): close on his face, eyes shut, a slow push;
    the eyes flutter open on "opened" and go to pin-prick terror on "eyes" (the 2D terror marks from there), his look
    dropping to his chest; on "chest" the camera eases back and tilts (on 1s, overshoot and settle) to show the
    shrimp sitting on his chest, ending on S01's framing. The shrimp blinks once near the end and locks on again."""
    n, rig, sh, _ = _world("S16")
    eyes = s3d.kai_point(rig, "eyes")
    pair = eyes.lerp(sh["root"].matrix_world.translation, 0.5)
    t1, d1, lens, yaw1 = S16_CLOSE
    t2, d2, lens2, yaw, up, far = v2.S01_CAM
    fwd = Vector((math.sin(math.radians(yaw)), math.cos(math.radians(yaw)), 0))
    a1, a2 = eyes - UP * 0.2 - EAST * 0.2, pair + UP * up + fwd * far   # his face big in the upper half; S01's aim
    f_open, f_eyes, f_it, f_chest = at("S16", "opened"), at("S16", "eyes"), at("S16", "it"), at("S16", "chest")
    b0, b1 = f_chest - 2, f_chest + 12                             # the pull back
    cam = diorama.camera("cam_s16", a1, dist=d1, tilt=t1, yaw=yaw1, lens=lens, blur=BLUR)
    for f in range(1, n + 1):
        if f < b0:                                                 # a slow push on his face
            u = (f - 1) / max(1, b0 - 1)
            _keycam(cam, f, a1, t1, d1 - 1.5 * u, lens, yaw1)
        elif f <= b1:                                              # back and tilt to the two of them
            e = acting.ease((f - b0) / (b1 - b0), "overshoot", 0.08)
            _keycam(cam, f, a1.lerp(a2, e), t1 + (t2 - t1) * e, (d1 - 1.5) + (d2 - d1 + 1.5) * e,
                    lens + (lens2 - lens) * e, yaw1 + (yaw - yaw1) * e)   # rolls upright as it pulls back
        else:                                                      # settle, a slight drift
            u = (f - b1) / max(1, n - b1)
            _keycam(cam, f, a2, t2, d2 - 0.8 * u, lens2, yaw)
    bpy.context.scene.camera = cam
    k = acting.face_keys
    k(rig, 1, eye_close=1.0, eye_open=0.0)
    k(rig, f_open, eye_close=0.55)                                 # the flutter on "opened"
    k(rig, f_open + 2, eye_close=1.0)
    k(rig, f_open + 4, eye_close=0.25)
    k(rig, f_open + 6, eye_close=0.0)
    acting.look_at(rig, eyes + UP * 6 + Vector((0, 0, 8)), f_open + 6, f_eyes - 1, darts=True, seed=9)   # blank
    acting.expression(rig, "terror", f_eyes)                       # he sees it: terror on "eyes"
    acting.look_at(rig, sh["root"].matrix_world.translation + Vector((0, 0, 1.2)), f_eyes, n, darts=True, seed=10)
    anim.lids(sh, n - 16, 1.0)
    s3d.lock_on(sh, eyes, n - 12)
    _beats("S16", terror=f_eyes, reveal=b0)
    _anchors("S16", n, cam, rig, sh)
    return dict(frames=n, step=2, ones=(1, n), subject=_subject(rig, sh))


def s17():
    """Then I saw the drops. The close-up of the drop (v2: dist 26, tilt 66, locked; the push-in is 2D): the claw over
    his jacket beside the shrimp, a drop swells at its tip, lands on "drops" and leaves a dark wet splat; the next
    one swells. His eyes follow the drop down."""
    n, rig, sh, _ = _world("S17", claw="jacket", lean=v2.S01_LEAN)
    land_f = at("S17", "drops")
    r = 0.28
    tip = s3d.claw_tip(sh) + Vector((0, -0.2, -r * 0.9))
    land, nrm, _m = v2._hit(tip)
    drop_m = look.flat("drip", look.hexc("#9fd8ff"))
    d1 = s3d._drop(tip, 1, land_f - 6, land_f, land + nrm * r * 0.6, r=r, mat=drop_m)
    s3d._drop(tip, land_f + 11, n + 20, n + 26, land, r=r, mat=drop_m)
    bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.0, fill_type="NGON", location=land + nrm * 0.02)
    spot = bpy.context.object
    for v in spot.data.vertices:
        a = math.atan2(v.co.y, v.co.x)
        v.co *= 1 + 0.16 * math.sin(3 * a + 1.0) + 0.07 * math.sin(7 * a + 2.0)
    spot.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler()
    spot.data.materials.append(look.flat("wet_tunic", look.hexc("#0f5d60")))
    for df, s in ((-1, 0.001), (0, 0.22), (2, 0.38), (6, 0.5), (12, 0.56)):
        anim.key(spot, "scale", land_f + df, (s, s * 0.8, 1), "LINEAR" if df > 0 else "CONSTANT")
    tgt = tip.lerp(land, 0.4) - EAST * 0.7 + UP * 0.3              # his whole face in at the top left
    cam = diorama.camera("cam_s17", tgt, dist=v2.S17_DIST, tilt=66.0, lens=120.0, blur=BLUR)
    v2._move(cam, n, [(1, 66.0, v2.S17_DIST, 120.0), (n, 66.0, v2.S17_DIST, 120.0)], lambda f: tgt)
    acting.expression(rig, "fear", 1)
    acting.look_at(rig, tip, 1, land_f - 7, darts=True, seed=11)   # on the swelling drop ...
    acting.look_at(rig, land, land_f - 4, n, darts=False)          # ... and down to where it lands
    acting.blink(rig, 1, land_f - 8, every=(40, 60), seed=12)
    _anchors("S17", n, cam, rig, sh, extra={"drop": lambda: d1.matrix_world.translation.copy()})
    return dict(frames=n, step=2, subject=[sh["root"]])


def s18():
    """Its claw only works wet. Close top-down on his face (v2, locked; the push and the snap-zoom are 2D): wide eyes on
    the claw, a blink, then they narrow in two steps as the thought lands on "wet" (the realisation background swaps
    in 2D from that frame)."""
    n, rig, sh, _ = _world("S18")
    tgt = s3d.kai_point(rig, "eyes") - UP * 0.6
    cam = diorama.camera("cam_s18", tgt, dist=50.0, tilt=76.0, lens=120.0, blur=BLUR)
    v2._move(cam, n, [(1, 76.0, 50.0, 120.0), (n, 76.0, 50.0, 120.0)], lambda f: tgt)
    f_claw, f_wet = at("S18", "claw"), at("S18", "wet")
    acting.expression(rig, "terror", 1)
    acting.expression(rig, "thinking", f_claw)                     # "claw only"
    acting.expression(rig, "realise", f_wet)                       # "wet": the thought lands
    acting.expression(rig, "realised", f_wet + 3)                  # narrowed: he gets it
    acting.look_at(rig, s3d.claw_tip(sh), 1, f_wet - 1, darts=True, seed=13)
    acting.blink(rig, 1, f_claw - 2, every=(60, 90), seed=14)
    _anchors("S18", n, cam, rig, sh)
    return dict(frames=n, step=2, subject=_subject(rig, sh))


SHOTS = {"S15b": s15b, "S01": s01, "S16": s16, "S17": s17, "S18": s18}
