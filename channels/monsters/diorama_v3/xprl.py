"""Episode 1 v3, 2.5D diorama (channels/monsters/DIORAMA_EP01_V3.md): XprL's S23b and S24top (A).

    S23b "And it was looking at the shrimp." Close on the butcher bird on top of the thorn tree, already dark from S23
        (the top shadow and amber eye glints): its head tilts, then locks on (a snap toward the shrimp, the eyes
        narrow). Cut (CUT_POV) to its view from the perch: far below, the tiny shrimp at the pond, its back turned,
        drinking. Slow push-ins on 1s in both halves (the POV one tightens like a predator focusing).
    S24top (A) "Option A: save the shrimp that tried to kill me." (the top panel all through the 3-sentence line):
        the bird's giant shadow already lies over the shrimp at the pond, which keeps drinking; Kai runs in from the
        south-east, skids into a crouch beside it (anticipation, overshoot) and reaches an open hand over it, his face
        set (determined), glancing up at the sky between beats. The action stays in the top half (y 80-600) for the
        in-place split; the assembler adds the big A. Camera push-in on 1s.

The shrimp from S21's end on (coordinator's call, see SHRIMP): drinking at the pond's east edge, facing south (its
back to the thorn tree), its claw (right side) dipped west into the water.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S23b OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Matrix, Vector

from channels.monsters.diorama import xprl as v2
from channels.monsters.diorama_v3 import bgqrs as b3
from channels.monsters.ep01v2 import helper5 as h5
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import acting, anim, butcherbird, diorama, hero, look, tuftwing

SHRIMP = (*diorama.MAP["shrimp_drink"], 0.0)  # the pond's east edge, its back to the thorn tree (coordinator, v3)
SHRIMP_YAW = diorama.SHRIMP_DRINK_YAW
BIRD_SCALE = h5.BIRD_SCALE


def _frames(shot, fallback):
    from channels.monsters.diorama_v3.shots import v3_frames           # (lazy: shots.py imports this module)
    try:
        return v3_frames(shot)
    except (OSError, KeyError):                                            # timing.json not in yet
        return fallback


def _set(n, kai_down=True):
    """The island after v3's snap exactly as bgqrs's v3 shots build it (diorama_v3/bgqrs._set: the grove's stumps
    once helper 10's grove_spots() lands), keeping the island dict for the thorn tree; with `kai_down`, Kai knocked
    flat in LYING_V3_L at his landing spot with the cut sapling smoking by his head (bgqrs v3's S15b-S18)."""
    got, real = {}, diorama.island

    def keep(*a, **kw):
        got["isl"] = real(*a, **kw)
        return got["isl"]
    diorama.island = keep
    try:
        b3._set(n)
    finally:
        diorama.island = real
    rig = None
    if kai_down:
        rig = hero.load((0, 0, 0), scale=b3.s3d.KAI_SCALE, outfit="world")
        acting.lie(rig, b3.HIPS, b3.HEAD_DIR, spec=acting.LYING_V3_L)
        hero.line_width(rig, 0.0025)
        b3._sapling(rig, n)
    return got["isl"], rig


def _shrimp(n, f_lift=None):
    """The puff-shrimp drinking at the pond's east edge, back to the thorn tree (x3._shrimp_wet, re-placed)."""
    x3.SHRIMP_AT = SHRIMP
    sh = x3._shrimp_wet(f_lift, n)
    sh["root"].rotation_euler = (0, 0, math.radians(SHRIMP_YAW))
    v2._twos([sh["shoulder"], sh["body"], sh["hinge"]] + sh["eyes"])
    bpy.context.view_layer.update()
    return sh


def _bird_on_perch(perch, face_to, cut=0.1, fold=False):
    """The butcher bird sitting on the top thorn, already dark (S23's rage light from frame 1: everything above `cut`
    below the ball's centre in the deep top-shadow tone, amber eye glints), facing `face_to`. `fold`: the little
    wings tucked away (hidden), so they never cross its face in a close shot (the head turns, the wings don't)."""
    rig = tuftwing.build((perch.x, perch.y, 0.0), shadow_span=10.0)
    rig["root"].scale = (BIRD_SCALE,) * 3
    d = Vector(face_to) - perch
    rig["root"].rotation_euler = (0, 0, math.atan2(d.x, -d.y))
    anim.key(rig["lift"], "location", 1, (0.0, 0.0, perch.z / BIRD_SCALE), "CONSTANT")
    h5._rage_light(rig, 1, perch.z + (tuftwing.CENTER[2] - cut) * BIRD_SCALE)
    if fold:
        for sx, w in zip((-1, 1), rig["wings"]):
            anim.key(w, "scale", 1, (0.001, 0.001, 0.001), "CONSTANT")   # tucked away: never across its face
    return rig


# ------------------------------------------------------------------------------------------------------- dark form
def _show(o, f, on):
    """Pop an object in (on=True) or out at frame f (scale keys, CONSTANT), keeping its scale otherwise."""
    s = tuple(o.scale)
    hide = tuple(v * 0.001 for v in s)
    before, after = (hide, s) if on else (s, hide)
    if f > 0:
        anim.key(o, "scale", f - 1, before, "CONSTANT")
    anim.key(o, "scale", f, after, "CONSTANT")


def _head_child(name, mesh, mat, head):
    """A mesh in the bird's rest coordinates, parented to its head the way tuftwing parents its parts."""
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    mesh.materials.append(mat)
    o.parent = head
    o.matrix_parent_inverse = Matrix.Translation(-Vector(tuftwing.CENTER))
    o.visible_shadow = False
    return o


def dark_form(f, name="tuft", lids_down=None):
    """The butcher bird's villain face from frame f (the end of S23, S23b, the dive in S24 B): the shrike's black mask
    through both eyes to the beak, amber eyes, hard angular lids slanting down to the beak and cutting the top of each
    eye (dropped to leave only an amber slit at `lids_down`, the lock-on), no blush, the belly a dull cream, and a
    small dark hooked beak. Works on any tuftwing rig by its object names (`name` as given to tuftwing.build)."""
    head = bpy.data.objects[f"{name}_head"]
    c = Vector(tuftwing.CENTER)
    rx, ry, rz = tuftwing.BALL
    ink = look.flat(f"{name}_mask", look.hexc("#17121a"))
    amber = look.flat(f"{name}_amber", look.hexc("#ffae1a"), 1.25)

    def surf(a, e, k=1.02):                                   # a point on the ball: azimuth a (0 = front), elevation e
        a, e = math.radians(a), math.radians(e)
        return c + Vector((rx * math.sin(a) * math.cos(e), -ry * math.cos(a) * math.cos(e), rz * math.sin(e))) * k

    # 1. the mask: a band through both eyes, dipping to the beak at the front, tapering off round the sides
    verts, faces, cols = [], [], 0
    for i, a in enumerate(range(-78, 79, 3)):
        t = min(1.0, abs(a) / 24.0)
        mid = 3.0 + 8.0 * t
        hh = (4.0 + 7.0 * t) * (1.0 if abs(a) <= 40 else max(0.1, 1 - (abs(a) - 40) / 38.0))
        verts += [tuple(surf(a, mid - hh)), tuple(surf(a, mid + hh))]
        if i:
            faces.append((2 * i - 2, 2 * i, 2 * i + 1, 2 * i - 1))
    me = bpy.data.meshes.new(f"{name}_mask")
    me.from_pydata(verts, [], faces)
    for p in me.polygons:
        p.use_smooth = True
    mask = _head_child(f"{name}_mask", me, ink, head)
    _show(mask, f, True)
    # 2. amber eyes (the ink eyes swapped for amber copies), the white glints kept small; no blush
    for sx in (-1, 1):
        eye = bpy.data.objects[f"{name}_eye{sx}"]
        am = eye.copy()
        am.data = eye.data.copy()
        am.data.materials.clear()
        am.data.materials.append(amber)
        am.name = f"{name}_eye_amber{sx}"
        bpy.context.scene.collection.objects.link(am)
        _show(am, f, True)
        _show(eye, f, False)
        for o in (bpy.data.objects.get(f"{name}_blush{sx}"),):
            if o:
                _show(o, f, False)
    # 3. the lids: angular dark slabs in front of each eye, slanting down toward the beak; half down, then a slit
    for sx in (-1, 1):
        ec = Vector((sx * 0.25, -0.515, 0.86))
        n = (ec - c).normalized()
        up = (Vector((0, 0, 1)) - n * n.z).normalized()
        right = up.cross(n).normalized()
        roll = math.radians(28) * (1 if right.x * sx > 0 else -1)          # the inner end (toward the beak) lower
        r2 = right * math.cos(roll) + up * math.sin(roll)
        u2 = up * math.cos(roll) - right * math.sin(roll)
        w, h, d = 0.17, 0.055, 0.012
        base = ec + n * 0.075
        lm = bpy.data.meshes.new(f"{name}_lid{sx}")
        corners = [(-w, -h, -d), (w, -h, -d), (w, h, -d), (-w, h, -d), (-w, -h, d), (w, -h, d), (w, h, d), (-w, h, d)]
        lm.from_pydata([tuple(r2 * x + u2 * y + n * z) for x, y, z in corners], [],
                       [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
        lid = _head_child(f"{name}_lid{sx}", lm, ink, head)
        half, slit = base + u2 * (h + 0.06), base + u2 * (h - 0.05)    # lower edge cuts the eye's top / leaves a slit
        for fr, p in ((f, half),) + (((lids_down, slit),) if lids_down else ()):
            anim.key(lid, "location", fr, tuple(p - Vector((0, 0, 0))), "CONSTANT")
        _show(lid, f, True)
    # 4. a small dark hooked beak
    beak = bpy.data.objects[f"{name}_beak"]
    hook = beak.copy()
    hook.data = beak.data.copy()
    hook.data.materials.clear()
    hook.data.materials.append(look.flat(f"{name}_beak_dark", look.hexc("#2b1f1c")))
    hook.name = f"{name}_beak_hook"
    bpy.context.scene.collection.objects.link(hook)
    hook.scale = (1.15, 1.15, 1.5)
    hook.rotation_euler = (math.radians(118), 0, 0)
    _show(hook, f, True)
    _show(beak, f, False)
    # the belly a dull cream: desaturate the butter and cream from f
    for mname in (f"{name}_butter", f"{name}_cream"):
        m = bpy.data.materials.get(mname)
        em = next((nd for nd in m.node_tree.nodes if nd.type == "EMISSION"), None) if m and m.use_nodes else None
        if em is None or not em.inputs[0].links:
            continue
        src = em.inputs[0].links[0].from_socket
        hsv = m.node_tree.nodes.new("ShaderNodeHueSaturation")
        m.node_tree.links.new(src, hsv.inputs["Color"])
        m.node_tree.links.new(hsv.outputs[0], em.inputs[0])
        for fr, sat, val in ((f - 1, 1.0, 1.0), (f, 0.3, 0.88)):
            hsv.inputs["Saturation"].default_value = sat
            hsv.inputs["Value"].default_value = val
            hsv.inputs["Saturation"].keyframe_insert("default_value", frame=fr)
            hsv.inputs["Value"].keyframe_insert("default_value", frame=fr)
        for fc in anim.all_fcurves(m.node_tree.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


# -------------------------------------------------------------------------------------------------------- S22, S23
def _to_s23_lens():
    """The way S23's bird faces at its end (it turns to S23's camera, which looks at the tree from the clearing)."""
    az = math.radians(v2.YAW_THORN)
    return Vector((-math.sin(az), -math.cos(az), 0.0))


def _v2_on_v3(builder, shot):
    """Run a v2 diorama builder (diorama/xprl.py) on v3's set, the v3 shrimp spot and the v3 frame count."""
    patches = {"_set": lambda n, kai_down=True: _set(n, kai_down), "_drinking": lambda n: _shrimp(n)}
    saved = {k: getattr(v2, k) for k in patches}
    cut = dict(v2.CUT)
    try:
        for k, f in patches.items():
            setattr(v2, k, f)
        v2.CUT[shot] = _frames(shot, cut[shot] + v2.TAIL) - v2.TAIL
        return builder()
    finally:
        for k, f in saved.items():
            setattr(v2, k, f)
        v2.CUT.clear()
        v2.CUT.update(cut)


def s22():
    """S22 as in v2 (the larder close-up craning back to the tree, the pond and Kai flat), on v3's world."""
    return _v2_on_v3(v2.s22, "S22")


def s23():
    """S23 as in v2 (the bird lands, glares at the lens, the empty-thorn insert), on v3's world. Its bird at the end
    is S23b's opening bird: same facing (to this camera), the same rage light and glare."""
    info = _v2_on_v3(v2.s23, "S23")
    dark_form(32, lids_down=None)                                           # it turns dark on the rage light (f32)
    return info


# ------------------------------------------------------------------------------------------------------------ S23b
def _twig(cam):
    """A thorny twig of the tree right in front of the bird's-view lens, across its top-left corner, so the POV reads
    "seen from the thorn tree" (the tilt-shift blurs it soft). Parented to the camera so it stays put as it moves."""
    bark = bpy.data.materials.get("thorn_bark")
    thorn = bpy.data.materials.get("thorn")
    pts = [Vector((-1.9, 2.1, -3.2)), Vector((-0.6, 1.25, -3.0)), Vector((0.4, 0.9, -2.9))]   # camera space
    objs = []
    for a, b, r in ((pts[0], pts[1], 0.07), (pts[1], pts[2], 0.05)):
        d = b - a
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=r, depth=d.length, location=(a + b) / 2)
        o = bpy.context.object
        o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        objs.append((o, bark))
    for i, t in enumerate((0.2, 0.45, 0.7, 0.9, 1.25, 1.6)):
        p = pts[0].lerp(pts[1], t) if t <= 1 else pts[1].lerp(pts[2], t - 1)
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.035, depth=0.32, location=p)
        o = bpy.context.object
        o.rotation_euler = (1.2 * (1 if i % 2 else -1), 0.4, 0.3 * i)
        objs.append((o, thorn))
    for o, m in objs:
        if m:
            o.data.materials.append(m)
        o.parent = cam
        o.visible_shadow = False


CUT_POV = 30                        # the cut to the bird's view (about where "looking" lands)
LOCK = 20                           # the lock-on, on "looking" (and the sting): the 2D snap-zoom of ~12 % lands here


def s23b():
    n = _frames("S23b", 60)
    diorama.setup()
    isl, _ = _set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    prey = Vector(SHRIMP) + Vector((0, 0, 1.0))
    # the close: from the clearing side (the forest is behind the tree), 25 deg off the line to the shrimp and a little
    # BELOW its eye (the prey's side of the look: it glares down, so only a low lens sees the face); when it locks on its
    # face turns three-quarter to the lens; before that it looks off to the side
    to_prey = prey - perch
    def turned(v, deg):
        c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return Vector((v.x * c - v.y * s_, v.x * s_ + v.y * c, 0)).normalized()
    side = turned(to_prey.xy.to_3d(), 25)
    bird = _bird_on_perch(perch, perch + _to_s23_lens() * 10, cut=0.1, fold=True)   # S23's last frame: same
    butcherbird.stare(bird, -8, down=-0.25)                                 # facing, dark, the glare, head up
    dark_form(1, lids_down=LOCK)                                            # the shrike's mask, lids, hooked beak
    acting.tilt(bird, 8, angle=0.42, hold=8)                                 # a curious tilt: one eye to the ground
    acting.lock_on(bird, prey, LOCK)                                        # snap onto the shrimp, head down at it
    # ... and make it predatory (overriding lock_on's cute stare): a half-lid squint, the pupil shrunk to a hard dot
    # with the amber glint, the crest flattened BACK, a slow forward lean
    for f in (LOCK, LOCK + 2, LOCK + 6, LOCK + 9):
        for sx, e in zip((-1, 1), bird["eyes"]):
            anim.key(e, "scale", f, (0.85, 1, 0.62), "CONSTANT")
            anim.key(e, "rotation_euler", f, (0, sx * 0.42, 0), "CONSTANT")
        anim.key(bird["crest"], "rotation_euler", f, (-1.0, 0, 0), "CONSTANT")
    anim.key(bird["body"], "rotation_euler", LOCK, (0, 0, 0), "BEZIER")
    anim.key(bird["body"], "rotation_euler", n, (0.24, 0, 0), "BEZIER")   # leaning in, slowly
    anim.blink(bird, 4)
    anim.squash(bird["body"], LOCK - 2, -0.06)                              # a hunch into the lock
    anim.squash(bird["body"], LOCK + 2, 0.03)
    anim.squash(bird["body"], LOCK + 6, 0.0)
    v2._twos(tuftwing._animated(bird))
    eye_w = perch + Vector((0, 0, (tuftwing.CENTER[2] + 0.12) * BIRD_SCALE))
    yaw_close = math.degrees(math.atan2(side.x, side.y)) + 180              # camera on the `side` of the bird
    close = None
    for f in range(1, CUT_POV):
        k = (f - 1) / (CUT_POV - 2)
        snap = 1.0 if f < LOCK else {LOCK: 1.0, LOCK + 1: 1.08, LOCK + 2: 1.16, LOCK + 3: 1.13}.get(f, 1.12)
        close = v2._cam("cam_s23b_eye", f, tuple(eye_w), 10.0 - 2.5 * k, -14.0, yaw_close, 85.0 * snap, cam=close)
    # the bird's view: from its eye, down the line to the shrimp, a wide lens tightening a little (the predator focusing)
    eye_pos = perch + Vector((0, 0, 1.3 * BIRD_SCALE)) + to_prey.normalized() * 1.4   # at its eye, past its beak
    dist0 = (prey - eye_pos).length
    pov = None
    for f in range(CUT_POV, n + 1):
        k = (f - CUT_POV) / max(1, n - CUT_POV)
        d = dist0
        el = math.degrees(math.asin((eye_pos.z - prey.z) / d))
        yw = math.degrees(math.atan2((prey - eye_pos).x, (prey - eye_pos).y))   # the lens sits at the bird's eye
        pov = v2._cam("cam_s23b_pov", f, tuple(prey), d, el, yw, 30.0 + 10.0 * k, cam=pov)   # wide: it's tiny
    _twig(pov)
    sc = bpy.context.scene
    for m in list(sc.timeline_markers):
        sc.timeline_markers.remove(m)
    for f, c in ((1, close), (CUT_POV, pov)):
        sc.timeline_markers.new(c.name, frame=f).camera = c
    sc.camera = close
    return dict(frames=n, step=2, ones=(1, n), subject=[bird["root"], sh["root"]])


# ----------------------------------------------------------------------------------------------------------- S24top
def s24top():
    n = _frames("S24", 162)
    diorama.setup()
    isl, _ = _set(n, kai_down=False)
    sh = _shrimp(n)
    perch = Vector(isl["thorn"]["perch"])
    bird = _bird_on_perch(perch, Vector(SHRIMP))
    # its giant shadow on the ground: a clear bird silhouette (sharp edge, wings spread) sliding in from the tree's side
    # over the shrimp and Kai, and growing as the bird comes (the dive itself is in panel B)
    over = Vector((SHRIMP[0] - 0.3, SHRIMP[1] - 0.2, 0.0))                  # body under the shrimp, wings across
    back = (Vector((perch.x, perch.y, 0)) - over).normalized() * 4.0
    v2._soft_shadow(bird, tuple(over + back - Vector((perch.x, perch.y, 0))), tuple(-back), 1, n,
                    tone="#1d2440", opacity=0.78, soften=1.0, shrink=0.57)   # wingspan ~6.5 -> ~8.8 units
    for f, sc_ in ((1, 1.0), (n, 1.35)):
        anim.key(bird["shadow"], "scale", f, (sc_, sc_, 1), "BEZIER")
    # Kai runs in from the east, skids, crouches at its side and reaches over it (facing west, three-quarter to us)
    reach_at = Vector((SHRIMP[0] + 3.6, SHRIMP[1] + 0.2, 0))
    facing = (Vector(SHRIMP) - reach_at).normalized()
    yaw = math.degrees(math.atan2(facing.x, -facing.y))
    start = reach_at - facing * 8.5
    k = x3._hero(tuple(start), yaw)
    hero.line_width(k, 0.0025)
    P = x3.Pose(k)
    path = (Vector((0, 0, 0)), Vector((0, -8.5 / 5.8, 0)))

    def run_upper(P, t):
        P.rot("spine", (18, 0, 0))
        P.rot("chest", (6, 0, 0))
        P.rot("head 1", (-22, 0, 0))                                        # face up to the lens: worried
        x3._arms_down(P, 25)
        P.aim("upper_arm.R", (-0.2, -0.5, -0.8))
        P.aim("forearm.R", (-0.1, -0.9, 0.1))
        P.aim("upper_arm.L", (0.2, 0.45, -0.8))
        P.aim("forearm.L", (0.1, -0.6, 0.4))

    def reach_upper(P, t):
        P.rot("spine", (14 + 4 * t, 0, 0))
        P.rot("chest", (4 + 2 * t, 0, 0))
        P.rot("neck", (-24 * t, 0, 0))
        P.rot("head 1", (-52 * t, 0, 0))                                    # chin up: his face to the lens (and sky)
        x3._arms_down(P, 12)
        P.aim("upper_arm.R", (-0.1, -0.85 - 0.1 * t, -0.35))                # reaching out over the shrimp
        P.aim("forearm.R", (-0.03, -0.98, -0.1))
        P.aim("hand.R", (0, -1, -0.15))
        P.twist("upper_arm.R", -90 * t)                                     # palm down, a cover over it
        P.aim("upper_arm.L", (0.35, -0.3, -0.85))                           # the other hand braced on his knee
        P.aim("forearm.L", (0.05, -0.75, -0.6))

    f_run = 34
    feet = x3._walk(P, k, path, 1, f_run, 0.48, "R", crouch=(0.04, 0.14), upper=run_upper, every=2)
    x3._squat(P, feet, f_run + 2, f_run + 18, 0.14, 0.42, reach_upper, every=2, hold_to=n)
    acting.EXPR.setdefault("determined", {"face_angry": 0.45, "eye_brow_down": 0.5, "mouth_wide": 0.25})
    acting.expression(k, "surprised", 1, value=0.7)
    acting.expression(k, "determined", f_run + 6)
    prey = Vector(SHRIMP) + Vector((0, 0, 1.0))
    sky = Vector((perch.x, perch.y, perch.z + 6.0))                         # where the bird is
    acting.look_at(k, prey, 1, n)
    for f in (f_run + 30, f_run + 76):                                      # quick glances up at the bird
        acting.look_at(k, sky, f, f + 10, darts=False)
        acting.look_at(k, prey, f + 12, f + 12, darts=False)
    acting.blink(k, 1, n, seed=7)
    v2._twos([k["arm"]])
    mid = Vector((SHRIMP[0] + 1.8, SHRIMP[1], 2.4))
    a = (tuple(mid + Vector((0.6, 0, 0.3))), 52.0, 42.0, 72.0, 85.0, -0.25)   # low and close, from the west-south-
    b = (tuple(mid), 43.0, 42.0, 72.0, 85.0, -0.25)                           # west: his face, the shrimp in front
    v2._move("cam_s24top_v3", 1, n, a, b, n)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"]])


SHOTS = {"S22": s22, "S23": s23, "S23b": s23b, "S24top": s24top}
