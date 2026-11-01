"""Episode 2, 2.5D diorama (channels/monsters/DIORAMA_EP02.md): helper 10's S08, S09 (the snap) and S10.

Staging: Kai stands at XprL's KAI_AT on the pond's east shore and aims the palm-sized puff-shrimp north-east, along
AIM, at the island's thorn tree (MAP["thorn"]). The butcher bird (the tuftwing in XprL's dark shrike form) wheels over
the thorn tree, dives back along AIM at him, and the snap blasts it straight back up the line into the tree's crown,
where it hangs upside down, dazed. It is never killed.

    S08 "They don't call it a pistol shrimp for nothing." (60 + 12): a heroic low 3/4 angle; Kai aims the shrimp in
        both hands like a pistol (a settle with overshoot on "pistol"); far behind, over the thorn tree, the bird
        wheels round for a second dive. Push-in on 1s.
    S09 (the snap, no words; 81 + 12; TWIST, the music drops):
        A   1-14  the shrimp's eye close-up: the lids drop to a glare
        B  15-36  over Kai's shoulder: the claw cocks wide and trembles (the held wind-up, ~0.8 s) as the bird dives in
                  along the line; SNAP at 34 (2D: white impact frames 34-36 and the shockwave ring at the claw)
        C  37-93  wide from the side: the bird blasted backward up the line, tumbling, into the thorn tree (62),
                  the tree shakes; the camera shakes on 2s
    S10 "The bird landed in the thorn bush." (52 + 12): close on the thorn tree's crown: the bird stuck upside down,
        feet up, swaying, dazed; little stars circle its head (2D). Push-in on 1s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S09 OUT [--frames A-B] [--still N --scale 0.5]
    python channels/monsters/diorama_ep02/helper10.py post S09 RAW_DIR SUB_DIR OUT_DIR   (the 2D pass)
"""
import json
import math
import os
import random
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ANCHORS = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
try:
    import bpy
    from mathutils import Vector

    from channels.monsters.diorama import helper10 as dv2      # diorama cameras (_camera, _key)
    from channels.monsters.diorama_v3 import helper10 as h3     # aim_euler, _key_cam, _kai_objects
    from channels.monsters.diorama_v3 import xprl as xv3        # dark_form (the shrike's mask)
    from channels.monsters.ep01v2 import helper10 as s15        # pose helpers
    from channels.monsters.ep01v2 import helper5 as h5          # BIRD_SCALE
    from channels.monsters.mk import acting, anim, butcherbird, diorama, erase, hero, meadow, puffshrimp, tuftwing
except ImportError:                                             # the 2D pass runs outside Blender
    bpy = None

SNAP_F, CUT_B, CUT_C, CRASH_F = 34, 15, 37, 62
if bpy:
    KAI_AT = Vector((5.0, -3.5, 0.0))                           # = diorama_ep02.xprl.KAI_AT
    THORN = Vector((*diorama.MAP["thorn"], 0.0))
    AIM = Vector((THORN.x - KAI_AT.x, THORN.y - KAI_AT.y, 0.0)).normalized()
    SIDE = Vector((AIM.y, -AIM.x, 0.0))                         # to Kai's right
    KAI_YAW = math.atan2(-AIM.x, AIM.y)                         # Kai's own +Y onto AIM

AIM_POSE = [("spine", (0, 0.1, 1)), ("chest", (0, 0.12, 1)), ("upper_chest", (0, 0.12, 1)), ("neck", (0, 0.18, 1)),
            ("head", (0, 0.22, 1)),
            ("left_upper_leg", (-0.3, 0.18, -1)), ("right_upper_leg", (0.32, -0.16, -1)),
            ("left_lower_leg", (-0.24, 0.02, -1)), ("right_lower_leg", (0.26, -0.04, -1)),
            ("left_foot", (-0.1, 1, -0.3)), ("right_foot", (0.15, 1, -0.3)),
            ("right_upper_arm", (-0.3, 1, 0.02)), ("right_lower_arm", (-0.12, 1, 0.1)), ("right_hand", (-0.05, 1, 0.1)),
            ("left_upper_arm", (0.3, 1, 0.02)), ("left_lower_arm", (0.12, 1, 0.1)), ("left_hand", (0.05, 1, 0.1))]
"""Kai's two-handed pistol grip (his own frame: +Y forward, +Z up, +X his right): a wide stance, leaning in."""


def _frames(shot, fallback):
    from channels.monsters.diorama_ep02.shots import ep02_frames
    try:
        return ep02_frames(shot)
    except (OSError, KeyError):
        return fallback


# ---------------------------------------------------------------- the set and the cast
def _set():
    diorama.setup()
    isl = diorama.island(seed=31, grove="cut")                  # Ep 1's after-snap island: the stumps stay
    diorama.stumps(diorama.grove_spots(), diorama.MAP["blast"], smoke=(-50, 200))
    return isl


def _kai(lean=0.0):
    k = hero.load((0, 0, 0), scale=s15.KAI_SCALE, outfit="world")
    spec = [(b, (d[0], d[1] - (lean if b in ("spine", "chest") else 0.0), d[2])) for b, d in AIM_POSE]
    s15._pose(k, spec, tuple(KAI_AT), (0, 0, KAI_YAW))
    s15._ground(k)
    return k


def _pose_kai(k, f, lean=0.0, rise=0.0):
    spec = [(b, (d[0], d[1] - (lean if b in ("spine", "chest", "upper_chest") else 0.0), d[2] + rise *
                 (1 if "arm" in b else 0))) for b, d in AIM_POSE]
    s15._pose(k, spec, tuple(KAI_AT), (0, 0, KAI_YAW))
    s15._ground(k)
    s15._key_pose(k, f)


def _shrimp_in_hands(k, scale=None):
    """The puff-shrimp at palm size (helper4.SHRIMP_IN_HAND, shared with S05) between his hands, claw forward along AIM; muzzle empties on the claw."""
    rig = puffshrimp.build((0, 0, 0), name="puff")
    emp = []
    for nm, off in (("puff_palm", (-1.7, -0.4, 2.2)), ("puff_muzzle", (-1.62, -0.44, 3.4))):
        e = bpy.data.objects.new(nm, None)
        bpy.context.scene.collection.objects.link(e)
        e.location = off
        bpy.context.view_layer.update()
        e.parent = rig["shoulder"]
        e.matrix_parent_inverse = rig["shoulder"].matrix_world.inverted()
        emp.append(e)
    hands = (s15._world(k, "right_hand", True) + s15._world(k, "left_hand", True)) / 2
    root = rig["root"]
    if scale is None:
        from channels.monsters.diorama_ep02 import helper4
        scale = helper4.SHRIMP_IN_HAND
    root.scale = (scale,) * 3
    root.rotation_euler = (0, 0, math.atan2(AIM.x, -AIM.y))    # its -Y (front) along AIM
    root.location = hands + AIM * 0.15 - Vector((0, 0, 0.1))     # sits on his palms, face clear
    bpy.context.view_layer.update()
    return rig, emp


def _bird(at):
    rig = tuftwing.build(tuple(at), name="tuft", shadow_span=6.0)
    rig["root"].scale = (h5.BIRD_SCALE,) * 3
    xv3.dark_form(1, name="tuft")
    return rig


def _fly(rig, f0, f1, path, step=2, face=None):
    """Key the bird's root along path(u) (world) on 2s, turned along its motion (or to `face`), flapping."""
    root = rig["root"]
    prev = path(0.0)
    for f in range(f0, f1 + 1, step):
        u = (f - f0) / max(1, f1 - f0)
        p = path(u)
        v = (p - prev) if (p - prev).length > 1e-4 else Vector(AIM)
        tgt = face(u) if face else v
        root.location = p
        root.rotation_euler = (0, 0, math.atan2(tgt.x, -tgt.y))
        anim.key(root, "location", f, tuple(p), "CONSTANT")
        anim.key(root, "rotation_euler", f, tuple(root.rotation_euler), "CONSTANT")
        prev = p
    for f in range(f0, f1, 8):
        tuftwing.flutter(rig, f, flaps=2, amount=1.0)


def _far(*cams):
    """dv2._key sets clip_end to 6x the subject distance; close shots still need the island behind them."""
    for c in cams:
        c.data.clip_end = 600.0
        c.data.clip_start = 0.1


def _anchor(shot, data):
    os.makedirs(ANCHORS, exist_ok=True)
    with open(os.path.join(ANCHORS, f"{shot}_anchors.json"), "w") as fh:
        json.dump(data, fh)


def _screen(cam, p):
    from bpy_extras.object_utils import world_to_camera_view
    v = world_to_camera_view(bpy.context.scene, cam, Vector(p))
    return (round(v.x * 720, 1), round((1 - v.y) * 1280, 1))


# ---------------------------------------------------------------- S08
def s08():
    n = _frames("S08", 72)
    sc = bpy.context.scene
    isl = _set()
    k = _kai()
    for f, lean, rise in ((1, -0.08, -0.15), (4, -0.04, -0.05), (8, 0.06, 0.04), (12, 0.02, 0.0)):
        _pose_kai(k, f, lean, rise)                              # brings the "pistol" up: anticipation, overshoot
    _pose_kai(k, 12, 0.02, 0.0)
    bpy.context.view_layer.update()
    rig, emp = _shrimp_in_hands(k)
    s15._flush_keys(k)
    acting.expression(k, "angry", 1, value=0.6)
    acting.blink(k, 1, n, at=(30,))
    aim, _ = h3.aim_euler(rig, emp, KAI_AT + AIM * 30 + Vector((0, 0, 9)))
    anim.key(rig["shoulder"], "rotation_euler", 1, aim, "CONSTANT")
    acting.glare(rig, THORN + Vector((0, 0, 18)), 1)
    # the bird wheels in the sky behind him (a banking loop over the pond), lining up its second dive
    c = KAI_AT - AIM * 16.0 + SIDE * 4.0 + Vector((0, 0, 17.0))
    bird = _bird(c)
    _fly(bird, 1, n, lambda u: c + Vector((math.cos(2.2 * u * math.pi) * 6, math.sin(2.2 * u * math.pi) * 4,
                                            1.5 * math.sin(u * 5))))
    # camera: heroic, low, in front and a little to his left: he aims almost into the lens; push-in on 1s
    chest = s15._world(k, "chest")
    pos0 = KAI_AT + AIM * 12.0 - SIDE * 4.5 + Vector((0, 0, 1.0))
    cam = dv2._camera("S08_cam", 1, chest, (pos0 - chest).length, 0.0)
    cam.data.lens = 28.0
    for f in range(1, n + 1):
        u = acting.ease((f - 1) / (n - 1), "inout")
        h3._key_cam(cam, f, pos0.lerp(chest + (pos0 - chest) * 0.8, u), chest + Vector((0, 0, 1.6 + 0.3 * u)))
    _far(cam)
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], rig["root"], bird["root"]])


# ---------------------------------------------------------------- S09
def s09():
    n = _frames("S09", 93)
    sc = bpy.context.scene
    isl = _set()
    k = _kai()
    for f, lean in ((1, 0.0), (SNAP_F - 2, 0.04), (SNAP_F, -0.14), (SNAP_F + 2, -0.08), (SNAP_F + 6, 0.0)):
        _pose_kai(k, f, lean)                                    # braced, then the recoil rocks him back
    rig, emp = _shrimp_in_hands(k)
    s15._flush_keys(k)
    acting.expression(k, "angry", 1, value=0.8)
    acting.expression(k, "surprised", SNAP_F + 1)
    acting.blink(k, 1, SNAP_F - 2, at=(8,))
    perch = Vector(isl["thorn"]["perch"]) if isl.get("thorn") else THORN + Vector((0, 0, 9.0))
    stuck = perch + Vector((0, 0, -1.6))
    target = KAI_AT + AIM * 30 + Vector((0, 0, 9))
    aim, _ = h3.aim_euler(rig, emp, target)
    sh, hg = rig["shoulder"], rig["hinge"]
    cock = tuple(a + b for a, b in zip(aim, (-0.14, 0, 0.06)))
    anim.key(sh, "rotation_euler", 1, aim, "CONSTANT")
    anim.key(hg, "rotation_euler", 1, (0.3, 0, 0), "CONSTANT")
    acting.glare(rig, target, 6)                                 # A: the lids drop to a glare
    for f, u in ((CUT_B, 0.3), (CUT_B + 2, 0.7), (CUT_B + 4, 1.0)):
        anim.key(sh, "rotation_euler", f, tuple(a + (c - a) * u for a, c in zip(aim, cock)), "CONSTANT")
        anim.key(hg, "rotation_euler", f, (0.3 + 0.6 * u, 0, 0), "CONSTANT")
    for f in range(CUT_B + 6, SNAP_F, 2):                        # held, trembling: the wind-up
        anim.key(sh, "rotation_euler", f, tuple(c + (0.012 if (f // 2) % 2 else -0.012) for c in cock), "CONSTANT")
    anim.key(sh, "rotation_euler", SNAP_F, aim, "CONSTANT")
    anim.key(hg, "rotation_euler", SNAP_F, (-0.3, 0, 0), "CONSTANT")
    anim.squash(rig["body"], SNAP_F, 0.18, "CONSTANT")
    anim.squash(rig["body"], SNAP_F + 3, 0.0, "CONSTANT")
    sc.frame_set(SNAP_F)
    bpy.context.view_layer.update()
    muzzle = emp[1].matrix_world.translation.copy()
    # the bird: dives in along the line (12-33), is blasted back up it tumbling (34-62), lands upside down
    hi = THORN + Vector((-2.0, -3.0, 22.0))
    near = KAI_AT + AIM * 7.5 + Vector((0, 0, 6.8))
    bird = _bird(hi)
    _fly(bird, 1, 11, lambda u: hi + Vector((1.5 * math.sin(u * 3), 1.5 * math.cos(u * 3), 0)))
    _fly(bird, 12, SNAP_F - 1, lambda u: hi.lerp(near, u ** 1.8), face=lambda u: -AIM)
    butcherbird.dive(bird, 12, SNAP_F - 1, target=tuple(bird["lift"].location), start=tuple(bird["lift"].location))
    root = bird["root"]
    for f in range(SNAP_F, CRASH_F + 1, 2):                      # blasted back along the line, an arc, tumbling
        u = (f - SNAP_F) / (CRASH_F - SNAP_F)
        e = 1 - (1 - u) ** 2.2
        p = near.lerp(stuck, e) + Vector((0, 0, 6.0 * math.sin(math.pi * u) * (1 - u)))
        anim.key(root, "location", f, tuple(p), "CONSTANT")
        anim.key(root, "rotation_euler", f, (math.pi * 3.0 * e, 0.4 * math.sin(u * 9), math.atan2(-AIM.x, AIM.y)),
                 "CONSTANT")
    anim.key(root, "rotation_euler", CRASH_F + 2, (math.pi * 3.0 + 0.25, 0, math.atan2(-AIM.x, AIM.y)), "CONSTANT")
    anim.key(root, "rotation_euler", CRASH_F + 4, (math.pi * 3.0, 0, math.atan2(-AIM.x, AIM.y)), "CONSTANT")
    meadow.drips((muzzle.x, muzzle.y, muzzle.z - 0.05), 1, SNAP_F, every=6, fall=max(0.3, muzzle.z - 0.02))
    tree = isl["thorn"]["root"] if isl.get("thorn") else None
    if tree is not None:                                         # the tree shudders when the bird hits it
        for f, a in ((CRASH_F - 1, 0.0), (CRASH_F, 0.07), (CRASH_F + 2, -0.05), (CRASH_F + 4, 0.03),
                     (CRASH_F + 6, -0.015), (CRASH_F + 8, 0.0)):
            anim.key(tree, "rotation_euler", f, (a, 0, 0), "CONSTANT")
    for i in range(6):                                           # loose feathers drifting down off the bird
        r = random.Random(40 + i)
        fe = erase._sphere(f"feather{i}", tuple(stuck), 1.0, bpy.data.materials["tuft_wing"], 8)
        fe.scale = (0.0, 0.0, 0.0)
        anim.key(fe, "scale", CRASH_F - 1, (0, 0, 0), "CONSTANT")
        for j, f in enumerate(range(CRASH_F, n + 1, 4)):
            p = stuck + Vector((r.uniform(-2, 2) + 0.6 * math.sin(j + i), r.uniform(-2, 2), 1.5 - j * 0.45))
            anim.key(fe, "location", f, tuple(p), "CONSTANT")
            anim.key(fe, "scale", f, (0.28, 0.06, 0.16), "CONSTANT")
    # cameras: A eye close-up, B over his shoulder down the line, C high and wide from behind him (portrait: the
    # blast runs up the frame into the thorn tree)
    sc.frame_set(1)
    bpy.context.view_layer.update()
    eye = sum((e.matrix_world.translation for e in rig["eyes"]), Vector()) / 2
    dv2.BLUR = 10.0
    ca = dv2._camera("S09_A", 1, eye, 3.0, 0.0)
    ca.data.lens = 50.0
    for f in range(1, CUT_B):
        u = acting.ease((f - 1) / (CUT_B - 2), "inout")
        h3._key_cam(ca, f, eye + AIM * (3.6 - 0.6 * u) - SIDE * 1.0 + Vector((0, 0, -0.45)), eye + Vector((0, 0, 0.1)))
    head = s15._world(k, "head")
    focus = KAI_AT + AIM * 6.0 + Vector((0, 0, 6.3))            # between the claw and where the bird pulls up
    dv2.BLUR = 5.0
    cb = dv2._camera("S09_B", CUT_B, near, 20.0, 5.0)
    cb.data.lens = 30.0
    for f in range(CUT_B, CUT_C):
        u = acting.ease((f - CUT_B) / (CUT_C - 1 - CUT_B), "out")
        pos = head - AIM * (4.2 - 0.8 * u) + SIDE * 1.7 + Vector((0, 0, 1.6))
        h3._key_cam(cb, f, pos, focus)
    goal = KAI_AT.lerp(THORN, 0.62) + Vector((0, 0, 5.0))
    dv2.BLUR = 3.0
    cc = dv2._camera("S09_C", CUT_C, goal, 30.0, 25.0)
    cc.data.lens = 30.0
    rnd = random.Random(9)
    sign = 1
    for f in range(CUT_C, n + 1):
        u = acting.ease((f - CUT_C) / (n - CUT_C), "out")
        pos = KAI_AT - AIM * (10.0 - 2.5 * u) + SIDE * 4.0 + Vector((0, 0, 13.0 + 1.0 * u))
        i = f - CUT_C
        if i < 14 and i % 2 == 0:
            sign = -sign
        off = Vector((0, 0, 0))
        if i < 14:
            amp = 0.6 * (1 - i / 14)
            off = SIDE * amp * sign * rnd.uniform(0.6, 1.0) + Vector((0, 0, amp * 0.5 * rnd.uniform(-1, 1)))
        h3._key_cam(cc, f, pos + off, goal + off * 0.5)
    # the streak along the shot (3D), turned to camera C
    st = erase._streak(tuple(muzzle), (AIM.x, AIM.y), (stuck - muzzle).length + 4, SNAP_F, cc)
    pitch = math.atan2(near.z - muzzle.z, (near - muzzle).length)
    for o in st:
        o.rotation_euler = (o.rotation_euler.x, -pitch, o.rotation_euler.z)
    _far(ca, cb, cc)
    sc.frame_set(SNAP_F)
    _anchor("S09", dict(muzzle=_screen(cb, muzzle), bird=_screen(cb, near)))
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], rig["root"], bird["root"]])


# ---------------------------------------------------------------- S10
def s10():
    n = _frames("S10", 64)
    sc = bpy.context.scene
    isl = _set()
    perch = Vector(isl["thorn"]["perch"]) if isl.get("thorn") else THORN + Vector((0, 0, 9.0))
    stuck = perch + Vector((0, 0, -1.6))
    bird = _bird(stuck)
    root = bird["root"]
    yaw = math.atan2(-AIM.x, AIM.y)
    for f in range(1, n + 1, 2):                                 # upside down, feet up, swaying slowly
        a = 0.12 * math.sin(f / 9.0)
        anim.key(root, "rotation_euler", f, (math.pi + a, 0.08 * math.sin(f / 13.0), yaw), "CONSTANT")
        anim.key(root, "location", f, tuple(stuck + Vector((0, 0, 0.12 * math.sin(f / 7.0)))), "CONSTANT")
    for f in (10, 30, 50):                                       # a dazed, feeble flutter
        tuftwing.flutter(bird, f, flaps=1, amount=0.35)
    for e in bird.get("eyes", []):                               # eyes squeezed half-shut
        anim.key(e, "scale", 1, (1.1, 1, 0.45), "CONSTANT")
    cam_t = stuck + Vector((0, 0, 0.2))
    cam = dv2._camera("S10_cam", 1, cam_t, 14.0, 12.0, yaw=math.degrees(math.atan2(AIM.x, AIM.y)) + 180 + 25)
    cam.data.lens = 40.0
    yaw_c = math.degrees(math.atan2(AIM.x, AIM.y)) + 205
    for f in range(1, n + 1):
        u = acting.ease((f - 1) / (n - 1), "inout")
        dv2._key(cam, f, cam_t, 14.0 - 3.0 * u, 12.0 + 3 * u, yaw=yaw_c - 6 * u)
    _far(cam)
    head = stuck + Vector((0, 0, -0.9 * h5.BIRD_SCALE))          # upside down: its head hangs below the body
    rows = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        rows[f] = _screen(cam, head)
    _anchor("S10", dict(head=rows))
    sc.frame_set(1)
    return dict(frames=n, step=2, ones=(1, n), subject=[bird["root"]])


SHOTS = {"S08": s08, "S09": s09, "S10": s10}


# ---------------------------------------------------------------- the 2D pass (outside Blender)
def post(shot, raw, sub, out):
    """S09: white impact frames at SNAP_F..+2 (fx2d.impact_frame_v3 from the subject pass) and the shockwave ring at
    the claw; S10: little stars circling the bird's head. Other frames are copied."""
    import glob
    import shutil
    os.environ.setdefault("FPS", "24")
    sys.path.insert(0, ROOT)
    from channels.monsters import fx2d
    from motion.engine import FPS, cairo
    a = json.load(open(os.path.join(ANCHORS, f"{shot}_anchors.json")))
    os.makedirs(out, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(raw, "[0-9]*.png"))):
        name = os.path.basename(path)
        f = int(name[:4])
        dst = os.path.join(out, name)
        t = (f - 1) / FPS
        if shot == "S09" and SNAP_F <= f <= SNAP_F + 12:
            img = cairo.ImageSurface.create_from_png(path)
            cr = cairo.Context(img)
            mx, my = a["muzzle"]
            if f < SNAP_F + 3:
                sp = os.path.join(sub, "subject", name)
                subj = cairo.ImageSurface.create_from_png(sp) if os.path.exists(sp) else None
                fx2d.impact_frame_v3(cr, t + 1e-4, (SNAP_F - 1) / FPS, cx=mx, cy=my, frames=3, subject=subj,
                                     seed=9)
            fx2d.shockwave(cr, t, (SNAP_F - 1) / FPS, mx, my, r=420, rings=2, dur=0.5, sound=False)
            img.write_to_png(dst)
        elif shot == "S10":
            img = cairo.ImageSurface.create_from_png(path)
            cr = cairo.Context(img)
            hx, hy = a["head"][str(f)]
            _stars(cr, f, hx, hy)
            img.write_to_png(dst)
        else:
            shutil.copyfile(path, dst)
    return out


def _stars(cr, f, cx, cy, n=3, rx=70.0, size=26.0):
    """Little yellow cel stars with navy lines circling over a dazed head on 2s (one orbit per 16 frames)."""
    ph = 2 * math.pi * ((f // 2) * 2) / 16
    for i in range(n):
        a = ph + i * 2 * math.pi / n
        x, y = cx + math.cos(a) * rx, cy - size * 1.6 + math.sin(a) * rx * 0.25
        r = size * (1 + 0.18 * math.sin(a))
        cr.new_path()
        for j in range(10):
            rr = r / 2 if j % 2 == 0 else r / 2 * 0.45
            ang = -math.pi / 2 + j * math.pi / 5 + ph * 0.5
            cr.line_to(x + rr * math.cos(ang), y + rr * math.sin(ang))
        cr.close_path()
        cr.set_source_rgba(1.0, 0.85, 0.25, 1)
        cr.fill_preserve()
        cr.set_source_rgba(0.11, 0.1, 0.2, 1)
        cr.set_line_width(4)
        cr.stroke()


if __name__ == "__main__" and bpy is None:
    if sys.argv[1] == "post":
        print(post(*sys.argv[2:6]))
