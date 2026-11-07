"""Episode 3, 2.5D diorama (channels/monsters/DIORAMA_EP03.md): helper 5's shots (comedy and acting).

    S07 "Their wing dust stings like nettles."  Night in helper 1's lane: a medium two-shot of one hut's porch, Wren
        and a villager sheltering on it side by side, lit coral by Kai's mark (off screen in the lane). Glittering
        wing dust drifts down in front of them from a few fluffmoths fluttering over the awning. Wren looks up, then
        throws her cape over her face (wren.shield + cape_up), shocked; the villager looks up too, and on "stings"
        starts scratching a red blotch on the forearm (V.scratcher: eyes squeezed, comic, not gross). Slow push-in on 1s;
        characters on 2s; the dust on 1s.
    S15 "Every single moth landed on its back."  The laugh hold, straight on from S14's end: the grass round Kai
        is a field of fluffmoths on their backs (helper 6's upside_down: legs waving on 2s, eye-spots dazed and
        blinking out of step, a wriggle now and then). Kai lies as bGqrs's S13 left him (on his back, head west, the
        left wrist laid out palm up, the mark glowing), then on "landed" sits up among them, a little overshoot, and
        looks round at them, bewildered, then a small amazed half-smile; the shrimp on his left shoulder peeks out
        and stares. Camera low in front of him (east, toward his feet), the moths big in the foreground; a slow
        push-in on 1s; characters on 2s.
    S19bot "Option B: leave at sunrise, like they said."  The bottom panel of the split (rows 486-1280 rendered, as
        Ep 2's S20bot; helper 8 crops it under the jagged divider). Dawn: the low sun just up in the east, long
        shadows, a pink-gold sky. Kai walks away from us up the dirt track out of the bell-keepers' village (helper 9's
        Ep 2 village on the south shore), between the last huts toward the meadow, the shrimp riding on his left
        shoulder. (Coordinator's notes: the whole of him at y ~700-1000, the road ahead, the sun low at the end of
        it.) He walks east along the beach road out of the village, past the last hut, toward the sun coming up over
        the lake; long soft shadows fall back toward us. On "like they said" he stops and looks back over his right shoulder at the village once (the shrimp
        turns round on his left shoulder to look too), then faces front and walks on. A slow push after him on 1s; characters on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep03 S19bot OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy
from mathutils import Euler, Matrix, Vector

from channels.monsters.diorama_ep02 import helper9 as H9              # village_and_lake, VILLAGE, _shore
from channels.monsters.diorama_ep02 import xprl as X                  # SCALE, _world, Kai
from channels.monsters.ep01v2 import bgqrs as s3d                     # _fix_pivots
from channels.monsters.ep01v2 import xprl as x3                       # Pose, _walk, _arms_down
from channels.monsters.mk import acting, anim, diorama, hero, look, puffshrimp

BLUR = 5.0
try:                            # the puff-shrimp on his shoulder: helper 4's size and perch (S01's hop lands it there)
    from channels.monsters.diorama_ep02.helper4 import SHRIMP_IN_HAND as SHRIMP_SHOULDER
except ImportError:
    SHRIMP_SHOULDER = 0.6
LAST = {}


def _frames(shot, fallback):
    from channels.monsters.diorama_ep03.shots import ep03_frames       # lazy: shots.py imports this module
    try:
        return ep03_frames(shot)
    except (OSError, KeyError, ValueError):                              # timing.json not in yet
        return fallback


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _cam(name, f0, f1, a, b, lens, blur=BLUR, haze=(2.5, 2.0), shift_y=0.0):
    """A camera move on 1s from pose a to pose b (each (target, dist, tilt, yaw)), eased; tilt-shift and haze re-solved
    every frame (diorama.camera's conventions: yaw 0 looks north, the camera sits behind the target)."""
    sc = bpy.context.scene
    cam = diorama.camera(name, a[0], dist=a[1], tilt=a[2], yaw=a[3], lens=lens, blur=blur, frame=f0)
    cam.data.clip_start = 0.1
    cam.data.shift_y = shift_y
    for f in range(f0, f1 + 1):
        u = _ease((f - f0) / max(1, f1 - f0))
        t = Vector(a[0]).lerp(Vector(b[0]), u)
        d = a[1] + (b[1] - a[1]) * u
        el, az = math.radians(a[2] + (b[2] - a[2]) * u), math.radians(a[3] + (b[3] - a[3]) * u)
        back = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
        cam.location = t + back * d
        cam.rotation_euler = (math.pi / 2 - el, 0, -az)
        cam.data.dof.focus_distance = d
        cam.data.dof.aperture_fstop = diorama.fstop_for(d, lens, blur)
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cam.data.dof.keyframe_insert("focus_distance", frame=f)
        cam.data.dof.keyframe_insert("aperture_fstop", frame=f)
        ms = sc.world.mist_settings
        ms.start, ms.depth = d * haze[0], d * haze[1]
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return cam


# ------------------------------------------------------------------------------------------------- the shrimp
def shrimp_on_shoulder(k, side="L", yaw=0.0, name="ep03_shrimp"):
    """The puff-shrimp sitting on top of Kai's shoulder (bone-parented to shoulder.<side>, so it rides every move),
    facing his front turned by `yaw` degrees (+ = toward his left). Returns the rig."""
    sh = puffshrimp.build((0, 0, 0), name=name)
    s3d._fix_pivots(sh)
    arm = k["arm"]
    sc = bpy.context.scene
    sc.frame_set(1)
    bpy.context.view_layer.update()
    b = arm.data.bones[f"shoulder.{side}"]
    fwd = arm.matrix_world.to_3x3().normalized() @ Vector((0, -1, 0))
    perch = arm.matrix_world @ arm.pose.bones[f"upper_arm.{side}"].head + Vector((0, 0, 0.75)) - fwd * 0.1
    root = sh["root"]
    root.scale = (SHRIMP_SHOULDER,) * 3
    yaw_w = arm.matrix_world.to_euler().z + math.radians(yaw)
    root.rotation_euler = (0, 0, yaw_w)
    root.location = perch                                                # helper 4's S01 perch
    bpy.context.view_layer.update()
    mw = root.matrix_world.copy()
    root.parent = arm
    root.parent_type = "BONE"
    root.parent_bone = b.name
    bpy.context.view_layer.update()
    root.matrix_world = mw
    for e in sh["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 1), "CONSTANT")
    return sh


def _shrimp_parts(sh):
    return [sh["root"], sh["body"], sh["shoulder"], sh["hinge"]] + list(sh["eyes"]) + list(sh.get("lids", []))


def _word(lid, w, shot="S19"):
    """The shot frame (1-based) where word `w` of line `lid` starts (ep03/timing.json)."""
    import json
    from channels.monsters.diorama_ep03 import shots as S
    with open(S._T) as fh:
        d = json.load(fh)
    start = next(s["start"] for s in d["shots"] if s["shot"] == shot)
    line = next(ln for ln in d["lines"] if ln["id"] == lid)
    t = next(x["start"] for x in line["words"] if x["w"].strip(".,:!?").lower() == w.lower())
    return int(round((t - start) * d.get("fps", 24))) + 1


def _drop_huts(centres, r=7.5):
    """Remove helper 9's village huts (walls and roofs, merged meshes) standing at `centres` (x, y): the ones that
    would sit right in front of a low camera inside the village."""
    import bmesh
    for o in list(bpy.data.objects):
        if not (o.name.startswith("h9_hut_walls") or o.name.startswith("h9_roofs")) or o.type != "MESH":
            continue
        bm = bmesh.new()
        bm.from_mesh(o.data)
        kill = [v for v in bm.verts if any(math.hypot((o.matrix_world @ v.co).x - cx, (o.matrix_world @ v.co).y - cy) < r
                                           for cx, cy in centres)]
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        bm.to_mesh(o.data)
        bm.free()


def _path_strip(name, pts, width=2.6, z=0.05):
    """A dirt path (helper 9's track colour) along the polyline `pts`."""
    import bmesh
    bm = bmesh.new()
    prev = None
    for a, b in zip(pts[:-1], pts[1:]):
        dv = (b - a)
        nv = Vector((-dv.y, dv.x, 0)).normalized() * width
        l0, r0 = prev if prev else (bm.verts.new(a + nv + Vector((0, 0, z))), bm.verts.new(a - nv + Vector((0, 0, z))))
        l1, r1 = bm.verts.new(b + nv + Vector((0, 0, z))), bm.verts.new(b - nv + Vector((0, 0, z)))
        bm.faces.new((l0, r0, r1, l1))
        prev = (l1, r1)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(bpy.data.materials.get("h9_dirt") or look.toon("h5_dirt", look.hexc("#c9a873")))
    return o


# ------------------------------------------------------------------------------------------------------ S07
S07_HUT = 3                                 # helper 1's lane hut whose porch they share (west side of the lane)
S07_SPREAD = 1.45                           # Wren and the villager this far either side of the porch's middle


def _dust(n, box_lo, box_hi, count=220, seed=7, light=None):
    """Glittering wing dust: tiny bright flakes (gold, pink, white) drifting down through the box on 1s, each swaying
    and twinkling on 2s (scale flicker). One shared emissive material per colour."""
    import random
    rnd = random.Random(seed)
    cols = [("#ffe6a0", 7.0), ("#ffc2d6", 6.0), ("#ffffff", 8.0), ("#bff2ff", 6.0)]
    mats = []
    for j, (hx, st) in enumerate(cols):
        m = bpy.data.materials.new(f"h5_dust{j}")
        m.use_nodes = True
        nt = m.node_tree
        for nd in list(nt.nodes):
            nt.nodes.remove(nd)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = look.hexc(hx)
        em.inputs["Strength"].default_value = st
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        mats.append(m)
    me = bpy.data.meshes.new("h5_flake")
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    bm.to_mesh(me)
    me.materials.append(mats[0])
    flakes = []
    lo, hi = Vector(box_lo), Vector(box_hi)
    for i in range(count):
        o = bpy.data.objects.new(f"h5_flake{i}", me)                     # one shared mesh, the colour per object
        bpy.context.scene.collection.objects.link(o)
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = mats[i % len(mats)]
        flakes.append(o)
    for i, o in enumerate(flakes):
        o.visible_shadow = False
        x, y = rnd.uniform(lo.x, hi.x), rnd.uniform(lo.y, hi.y)
        z0 = rnd.uniform(lo.z, hi.z) + rnd.uniform(0, hi.z - lo.z) * 0.6
        fall = rnd.uniform(0.07, 0.16)                                   # units a frame: a slow drift down
        sway, ph, per = rnd.uniform(0.15, 0.5), rnd.uniform(0, 6.3), rnd.uniform(18, 34)
        size = rnd.uniform(0.022, 0.055)
        for f in range(1, n + 1):
            z = z0 - fall * f
            while z < lo.z:
                z += hi.z - lo.z
            o.location = (x + sway * math.sin(f / per * 6.283 + ph), y + 0.5 * sway * math.cos(f / per * 4.0 + ph), z)
            o.keyframe_insert("location", frame=f)
            if f % 2 == 1:
                tw = 1.0 if rnd.random() > 0.25 else rnd.choice((0.35, 1.8))
                o.scale = (size * tw,) * 3
                o.keyframe_insert("scale", frame=f)
        for fc in anim.all_fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    return flakes


def s07():
    from channels.monsters.diorama_ep03 import bgqrs as B
    from channels.monsters.diorama_ep03 import village as V
    from channels.monsters.mk import fluffmoth, wren
    n = _frames("S07", 60)
    f_sting = _word("l7", "stings", shot="S07")
    X._world(n)
    B._night()                                                           # helper 9's FINAL night (N9.night)
    sc = bpy.context.scene
    try:
        H9.village_and_lake()
    except Exception as e:
        print("S07: no village", e)
    huts = V.lane()
    hut = huts[S07_HUT]
    porch, face = hut["porch"], hut["face"]
    along = Vector((-face.y, face.x, 0.0))                               # across the porch (left to right from the lane)
    kai_at = V.LANE_AT                                                   # Kai, off screen (his mark lights them)
    # the mark: as helper 9's mark light (6000 W coral, no shadow) at his raised wrist, off screen in the lane
    key = bpy.data.lights.new("s07_mark", "POINT")
    key.color = H9.CORAL
    key.energy = 6000.0
    key.shadow_soft_size = 0.25
    key.use_shadow = False
    if hasattr(key, "use_soft_falloff"):
        key.use_soft_falloff = True
    lk = bpy.data.objects.new("s07_mark", key)
    sc.collection.objects.link(lk)
    lk.location = kai_at + Vector((0, 0, 9.0))

    def facing(p):
        d = kai_at - p
        return math.atan2(d.x, -d.y)

    # Wren on the porch (its left end from the lane), facing the light: the bell low, looking up at the glitter;
    # then the cape over her face
    wp = porch + along * S07_SPREAD + Vector((0, 0, 0.5))
    w = X._wren(Vector((0, 0, 0)), 0.0)
    w["arm"].location = wp
    w["arm"].rotation_euler = (0, 0, facing(wp) + math.radians(12))
    P = x3.Pose(w)
    f_c0, f_c1 = 6, 15
    for f in range(1, n + 1, 2):
        P.reset()
        t = _ease((f - f_c0) / (f_c1 - f_c0))
        if t <= 0:
            wren.hold_bell(P, 0.15)
            P.rot("head 1", (-12 * _ease(f / 6.0), 0, 0))                 # looking up at the glitter
        else:
            wren.shield(P, min(1.0, t * 1.08) if f < f_c1 + 2 else 1.0)
        if f >= f_c1:                                                    # a little cringe under the cape
            P.rot("chest", (2 * math.sin((f - f_c1) / 3.0), 0, 0))
        P.key(f)
    wren.cape_up(w, 1, False)
    wren.cape_up(w, f_c0 + 6, True)
    wren.grip(w, 1)
    wren.face(w, "stern", 1)
    wren.face(w, "shocked", f_c0)
    wren.blink(w, 1, n, at=(4,))

    # the villager beside her (the porch's right end): looks up at the glitter, then the itch hits on "stings"
    vp = porch - along * S07_SPREAD + Vector((0, 0, 0.5))
    v = V.villager(7, 71, net=False)
    v["root"].location = vp
    v["root"].rotation_euler = (0, 0, facing(vp) - math.radians(12))
    anim.key(v["body"], "rotation_euler", 1, (math.radians(-6), 0, 0), "CONSTANT")
    anim.key(v["body"], "rotation_euler", f_sting - 8, (math.radians(-16), 0, 0), "CONSTANT")   # head back: looking up
    scr = V.scratcher(v, f_sting, n)

    # a few moths fluttering just over the awning, shedding the dust
    top = porch + Vector((0, 0, 0))
    rigs = fluffmoth.swarm(5, lambda i, rnd: (top + along * rnd.uniform(-6, 6) + face * rnd.uniform(-1, 5)
                                              + Vector((0, 0, rnd.uniform(11.5, 15.0))),
                                              0.42 * rnd.uniform(0.85, 1.1)), name="m07_", seed=7)
    import random
    rnd = random.Random(70)
    for i, r in enumerate(rigs):
        p0 = r["root"].location.copy()
        drift = (along * rnd.uniform(-1, 1) + face * rnd.uniform(-0.4, 0.4)).normalized() * rnd.uniform(3, 6)
        for f in range(1, n + 1, 2):
            r["root"].location = p0 + drift * (f / n) + Vector((0, 0, 0.5 * math.sin(f / 5.0 + i)))
            r["root"].keyframe_insert("location", frame=f)
        fluffmoth.face(r, 1, drift)

    # the dust: drifting down in front of and round the two of them, thickest just in front of the porch
    c = porch + face * 3.0
    lo = c - along * 7.5 - face * 4.0
    hi = c + along * 7.5 + face * 4.5
    _dust(n, (min(lo.x, hi.x), min(lo.y, hi.y), 0.4), (max(lo.x, hi.x), max(lo.y, hi.y), 14.5), count=340)

    # camera: from the lane, a little toward Kai's side (so the light comes from behind the lens, left), low; a slow
    # push-in on 1s. Both of them waist-up-ish, their faces above the caption band.
    tgt = porch + Vector((0, 0, 6.2))
    look_dir = (-face).lerp((porch - kai_at).normalized(), 0.15).normalized()
    cy = math.degrees(math.atan2(look_dir.x, look_dir.y))
    _cam("cam_s07", 1, n, (tgt, 15.0, 6.0, cy), (tgt, 12.5, 5.0, cy), lens=32.0, blur=4.0, shift_y=-0.06)
    _px_anchors("S07", n, dict(blotch=scr["blotch"]))                   # helper 1's itch squiggles (post_helper5)
    LAST.update(w=w, v=v)
    return dict(frames=n, step=2, ones=(1, n), subject=[w["arm"], v["root"]])


# ------------------------------------------------------------------------------------------------------ S15
S15_MOTH_SCALE = 0.42                                                    # bGqrs's S13 swarm size
# sitting on the grass (XprL's S16/S17 pose, so the cut matches): the left knee up with the left forearm resting on it
# (palm up: the mark faces the sky), the right leg out along the grass, the right hand propped behind him; head up.
# Directions in Kai's own frame (helper 10's _pose spec): +X his right, +Y forward, +Z toward his head.
S15_SIT = [("spine", (0, 0.12, 1)), ("chest", (0, 0.06, 1)), ("neck", (0, 0.0, 1)), ("head", (0, -0.08, 1)),
           ("left_upper_arm", (-0.28, 0.55, -0.78)), ("left_lower_arm", (-0.05, 1.0, 0.12)),
           ("left_hand", (0.0, 1.0, 0.05)),
           ("right_upper_arm", (0.35, -0.55, -0.75)), ("right_lower_arm", (0.22, -0.45, -0.86)),
           ("right_hand", (0.12, -0.5, -0.86)),
           ("left_upper_leg", (-0.12, 0.72, 0.6)), ("left_lower_leg", (-0.04, 0.32, -0.95)),
           ("left_foot", (-0.08, 1, -0.25)),
           ("right_upper_leg", (0.2, 1.0, -0.04)), ("right_lower_leg", (0.12, 1.0, -0.06)),
           ("right_foot", (0.12, 0.35, 1))]


def _s15_landings(B, wrist, hips, hd, n_moths=34, seed=15):
    """Where the moths lie: helper 10's S14 landing spots if they are in (build/monsters/diorama_ep03/
    S14_landings.json), else a rough ring round Kai within ~1.5-9 units of his wrist and body, with a few big ones
    toward the camera (east, past his feet). Returns [(x, y, yaw, scale)]."""
    import json
    import os
    import random
    pth = os.path.join(os.path.dirname(os.path.abspath(__file__)), "S14_landings.json")
    if not os.path.exists(pth):
        pth = os.path.join(B.BUILD, "S14_landings.json")
    if os.path.exists(pth):
        with open(pth) as fh:
            d = json.load(fh)
        pts = d.get("landings", d) if isinstance(d, dict) else d
        out = []
        for q in pts:
            if isinstance(q, dict) and "at" in q:                       # helper 10's format
                out.append((q["at"][0], q["at"][1], q.get("yaw", 0.0), q.get("scale", S15_MOTH_SCALE)))
            elif isinstance(q, dict):
                out.append((q["x"], q["y"], q.get("yaw", 0.0), q.get("scale", S15_MOTH_SCALE)))
            else:
                out.append((q[0], q[1], q[2] if len(q) > 2 else 0.0, q[3] if len(q) > 3 else S15_MOTH_SCALE))
        return out
    rnd = random.Random(seed)
    feet = hips - hd * 4.5                                               # his feet: east of the hips
    out = []
    tries = 0
    while len(out) < n_moths and tries < 5000:
        tries += 1
        c = rnd.choice((wrist, wrist, hips, feet))
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(1.6, 7.5)
        p = c + Vector((math.cos(a) * r, math.sin(a) * r, 0))
        if (p - hips).length < 2.2 or (p - (hips + hd * 2.8)).length < 1.8:  # not on his body or head
            continue
        if any((p - Vector((q[0], q[1], 0))).length < 1.7 for q in out):
            continue
        out.append((p.x, p.y, rnd.uniform(-math.pi, math.pi), S15_MOTH_SCALE * rnd.uniform(0.85, 1.12)))
    return out


S15_HEROES = [(120, 830), (640, 800), (190, 1010), (560, 1030)]  # where the hero moths lie on the 720x1280 frame (f60)


def _ground_at_px(cam, x, y, W=720, H=1280):
    """The ground point (z 0) seen at pixel (x, y) of the frame, at the current frame."""
    sc = bpy.context.scene
    fr = cam.data.view_frame(scene=sc)                                   # tr, br, bl, tl in camera space
    u, v = x / W, y / H
    top = fr[3].lerp(fr[0], u)
    bot = fr[2].lerp(fr[1], u)
    p = cam.matrix_world @ top.lerp(bot, v)
    o = cam.matrix_world.translation
    d = p - o
    t = -o.z / d.z if abs(d.z) > 1e-6 else 0.0
    return o + d * t


def _px_anchors(shot, n, objs):
    """build/monsters/diorama_ep03/<shot>_anchors.json: per frame, each named object's position on the 720x1280 frame
    as [x, y, depth] (helper 1's post_helper1.itch reads this layout)."""
    import json
    import os
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        row = {}
        for nm, o in objs.items():
            v = world_to_camera_view(sc, sc.camera, o.matrix_world.translation)
            row[nm] = [round(v.x * 720, 1), round((1 - v.y) * 1280, 1), round(v.z, 2)]
        out[f] = row
    sc.frame_set(1)
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    d = os.path.join(root, "build", "monsters", "diorama_ep03")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{shot}_anchors.json"), "w") as fh:
        json.dump(out, fh)


def _hero_anchors(shot, n, rigs):
    """build/monsters/diorama_ep03/<shot>_heroes.json: per frame, each hero moth's body centre, its two wing eye-spots
    and a size (px per moth unit) on the 720x1280 frame, for the 2D dizzy stars and spirals (post_helper5.py)."""
    import json
    import os
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    cam = sc.camera
    W, H = 720, 1280

    def px(p):
        v = world_to_camera_view(sc, cam, p)
        return [round(v.x * W, 1), round((1 - v.y) * H, 1), round(v.z, 2)]
    out = {}
    for f in range(1, n + 1):
        sc.frame_set(f)
        rows = []
        for r in rigs:
            c = r["body"].matrix_world.translation
            right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
            s_ = r["root"].matrix_world.to_scale().x
            a, b = px(c), px(c + right * s_ * 2.0)
            rows.append(dict(c=a, size=round(abs(b[0] - a[0]) / 2.0, 1),
                             spots=[px(sp.matrix_world.translation) for sp in r["spots"][:2]]))
        out[f] = rows
    sc.frame_set(1)
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
    d = os.path.join(root, "build", "monsters", "diorama_ep03")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{shot}_heroes.json"), "w") as fh:
        json.dump(out, fh)


def _s15_extra(spots, hips, hd, n_moths=12, seed=16):
    """Moths that came down just outside S14's view: on the camera side (south-east of him, toward his feet and his
    right), so the foreground is a field of legs in the air too."""
    import random
    rnd = random.Random(seed)
    right = Vector((-hd.y, hd.x, 0))                                     # his right once he sits up (the south)
    feet = hips - hd * 4.0
    out = []
    tries = 0
    while len(out) < n_moths and tries < 4000:
        tries += 1
        p = feet + right * rnd.uniform(-1.0, 9.0) - hd * rnd.uniform(-2.0, 8.0)
        if (p - hips).length < 3.0:
            continue
        if any((p - Vector((q[0], q[1], 0))).length < 1.8 for q in spots + out):
            continue
        out.append((p.x, p.y, rnd.uniform(-math.pi, math.pi), S15_MOTH_SCALE * rnd.uniform(0.85, 1.05)))
    return out


def s15():
    from channels.monsters.diorama_ep03 import bgqrs as B
    from channels.monsters.ep01v2 import helper10 as s15p
    from channels.monsters.mk import fluffmoth
    from channels.monsters.diorama_ep03 import helper9 as N9
    n = _frames("S15", 106)
    f_up = _word("l15", "landed", shot="S15") - 3                        # he sits up on "landed"
    X._world(n)
    N9.night(n)
    sc = bpy.context.scene
    try:
        H9.village_and_lake()
        _drop_huts([(19.6, -153.4)])                                     # its roof sits in the lens at the start
    except Exception as e:                                               # the set is optional for a test still
        print("S15: no village", e)
    hd = B._head_dir()
    yaw = math.pi + math.radians(B.S13_HEAD)
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    k["arm"].rotation_mode = "XYZ"
    rot_lie = (math.radians(90.0), 0, yaw)
    s15p._pose(k, B._with_arm(B.LIE, 1.0), (0, 0, 0), rot_lie)
    twist = B._twist_for_palm_up(k)[0]
    s15p._pose(k, [x for x in S15_SIT if x[0] != "left_hand"], (0, 0, 0), (math.radians(10.0), 0, yaw))
    sit_roll = B._twist_for_palm_up(k)                                   # the palm (the mark) up on his knee
    print("S15 sit palm-up roll", sit_roll)
    sit_roll = sit_roll[0]
    UP = S15_SIT
    lie = B._with_arm(B.LIE, 1.0)
    # (frame, spec, theta (90 = flat on his back), arm-out amount)
    keys = [(1, lie, 90.0, 1.0), (f_up, lie, 90.0, 1.0), (f_up + 6, B._blend(lie, UP, 0.7), 40.0, 0.4),
            (f_up + 10, UP, 2.0, 0.0), (f_up + 14, UP, 10.0, 0.0), (n, UP, 10.0, 0.0)]
    back = 3.0                                                           # the hips stay where S13 laid them
    for f in range(1, n + 1, 2):
        i = max(j for j in range(len(keys)) if keys[j][0] <= f)
        if i + 1 < len(keys):
            a, b = keys[i], keys[i + 1]
            u = _ease((f - a[0]) / max(1, b[0] - a[0]))
        else:
            a = b = keys[-1]
            u = 1.0
        spec = B._blend(a[1], b[1], u)
        theta = a[2] + (b[2] - a[2]) * u
        v = a[3] + (b[3] - a[3]) * u
        look = 0.0
        if f > f_up + 12:                                               # looks round: left, right, then to us
            t = f - (f_up + 12)
            look = 0.55 * math.sin(min(1.0, t / 30.0) * 2 * math.pi) * (1 - _ease((t - 28) / 6))
            look += -0.6 * _ease((t - 30) / 8)                           # ends facing the lens (for the grin)
        r = Euler((math.radians(theta), 0, yaw)).to_matrix()
        s15p._pose(k, [x for x in spec if x[0] != "left_hand"], (0, 0, 0), (math.radians(theta), 0, yaw))
        B._twist(k, "left_lower_arm", twist * v + sit_roll * (1 - v))   # palm (the mark) up, lying or sitting
        s15p._aim(k, "left_hand", r @ Vector(dict(spec)["left_hand"]))
        if look:
            hb = k["arm"].pose.bones.get("head 1") or s15p._bone(k, "head")
            if hb is not None:
                hb.matrix = hb.matrix @ Matrix.Rotation(look, 4, "Y")
                bpy.context.view_layer.update()
        hip = s15p._world(k, "hips")
        target = B.S13_AT + hd * back
        k["arm"].location += Vector((target.x - hip.x, target.y - hip.y, 0))
        s15p._ground(k)
        bpy.context.view_layer.update()
        s15p._key_pose(k, f)
    s15p._flush_keys(k)

    # the shrimp on his left shoulder: flat and squeezed as S13 left it, it peeks out once he is up, and stares
    sh = puffshrimp.build((0, 0, 0), name="ep03_shrimp_s15")
    s3d._fix_pivots(sh)
    base = SHRIMP_SHOULDER
    f_peek = f_up + 16
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        side = (k["arm"].matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized()
        up = _ease((f - f_up) / 12.0)
        sq = 0.62 if f < f_peek else 1.0
        pt = B._bone_world(k, "upper_arm.L") + Vector((0, 0, 0.55 * sq)) + side * 0.25
        sh["root"].location = pt
        sh["root"].keyframe_insert("location", frame=f)
        look = 0.0                                                       # it looks round at the moths: left, right
        if f >= f_peek + 8:
            look = (0.7, 0.7, -0.6, -0.6, 0.15)[min(4, (f - f_peek - 8) // 12)]
        sh["root"].rotation_euler = (-0.55 * (1 - up), 0, yaw + math.pi + look)
        sh["root"].keyframe_insert("rotation_euler", frame=f)
        sh["root"].scale = (base * (1.18 if sq < 1 else 1.0), base * (1.18 if sq < 1 else 1.0), base * sq)
        sh["root"].keyframe_insert("scale", frame=f)
    sc.frame_set(1)
    for fc in anim.all_fcurves(sh["root"].animation_data.action):
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"
    anim.key(sh["shoulder"], "rotation_euler", 1, (0.55, 0.0, 0.0), "CONSTANT")
    anim.key(sh["hinge"], "rotation_euler", 1, (0.15, 0.0, 0.0), "CONSTANT")
    for e in sh["eyes"]:
        anim.key(e, "scale", 1, (1, 1, 0.08), "CONSTANT")              # still squeezed shut from S13's duck
        anim.key(e, "scale", f_peek, (1.15, 1.15, 1.15), "CONSTANT")   # eyes wide at the field of moths
        anim.key(e, "scale", f_peek + 10, (1, 1, 1), "CONSTANT")
    anim.blink(sh, f_peek + 30)

    # the mark: helper 9's coral key on his left forearm at its default (as S13/S14 end), nothing else: a coral pool
    # round his wrist that falls off to dark
    lt = N9.mark(k, key=[(1, N9.MARK_W), (f_up, N9.MARK_W), (f_up + 10, N9.MARK_W * 0.22)])
    up = bpy.data.lights.new("s15_mark_up", "SPOT")                      # sitting, the palm-up mark shines UP:
    up.color = H9.CORAL                                                  # it lights him and the air, not the field
    up.spot_size = math.radians(80)
    up.spot_blend = 0.6
    up.use_shadow = False
    lu = bpy.data.objects.new("s15_mark_up", up)
    sc.collection.objects.link(lu)
    lu.rotation_euler = (math.pi, 0, 0)                                  # pointing straight up
    for f in range(1, n + 1, 2):
        sc.frame_set(f)
        lu.location = lt.matrix_world.translation
        lu.keyframe_insert("location", frame=f)
        up.energy = 9000.0 * _ease((f - f_up) / 10.0)
        up.keyframe_insert("energy", frame=f)
    sc.frame_set(1)
    wrist = H9._forearm(k, 1.0)
    hips = s15p._world(k, "hips")
    hips = Vector((hips.x, hips.y, 0.0))
    wrist = Vector((wrist.x, wrist.y, 0.0))
    B._grass_at(wrist)
    acting.grass_round(hips, hd)

    # the field of moths on their backs (one built, linked copies), legs waving
    spots = _s15_landings(B, wrist, hips, hd)
    spots += _s15_extra(spots, hips, hd)                                 # more on the camera side: a whole field
    # camera: low 3/4 from his right-front, the moths big in the foreground; a slow push-in on 1s
    mid = hips - hd * 1.2
    cy = math.degrees(math.atan2(hd.x, hd.y))                            # looking west, along his head direction
    _cam("cam_s15", 1, n, (mid + Vector((0, 0, 3.4)), 18.0, 13.0, cy + 40.0),
         (mid + Vector((0, 0, 3.8)), 14.5, 11.0, cy + 36.0), lens=35.0, blur=5.0, shift_y=-0.03)
    # four hero moths in the foreground round him, placed by where they land on screen at the hold (f60): big, legs
    # waving hard (+ 2D dizzy stars and spirals, post_helper5.py)
    sc.frame_set(60)
    heroes = [_ground_at_px(sc.camera, x, y) for x, y in S15_HEROES]
    sc.frame_set(1)
    to_cam = (sc.camera.matrix_world.translation - mid)
    to_cam.z = 0
    to_cam.normalize()
    spots = [q for q in spots if all((Vector((q[0], q[1], 0)) - Vector((h.x, h.y, 0))).length > 2.0 for h in heroes)]
    n_field = len(spots)
    spots += [(h.x, h.y, math.atan2(-to_cam.x, to_cam.y) + 0.5 * (i % 2 * 2 - 1), 0.52) for i, h in enumerate(heroes)]
    cam_side = hips - hd * 12.0                                          # roughly where the camera looks from
    rigs = fluffmoth.swarm(len(spots), lambda i, rnd: (Vector((spots[i][0], spots[i][1], 1.0)), spots[i][3]),
                           name="m15_", seed=15,
                           far=lambda i, loc, scl: (Vector((loc.x, loc.y, 0)) - cam_side).length > 15.0)
    for i, (rig, q) in enumerate(zip(rigs, spots)):
        for w in rig["wings"]:                                           # no flight beat: they lie still
            w.animation_data_clear()
        rig["root"].rotation_euler = (0, 0, q[2])
        fluffmoth.upside_down(rig, 1, n, land_at=(q[0], q[1], 0.0), seed=100 + i)
        anim.key(rig["root"], "location", 1, (q[0], q[1], fluffmoth.BACK_REST * q[3]), "CONSTANT")   # on the grass
        #                                                                (helper 10's fix: BACK_REST is unscaled)
        if i >= n_field:                                                 # a hero: the legs wave big and fast
            import random as _r
            rr = _r.Random(500 + i)
            for j, lp in enumerate(rig.get("legs", [])):
                sx = -1 if j % 2 == 0 else 1
                ph, sp = rr.uniform(0, 6.3), rr.uniform(0.9, 1.2)
                for f in range(1, n + 1, 2):
                    a, b = math.sin(f * sp + ph), math.sin(f * sp * 0.7 + ph * 1.3)
                    anim.key(lp, "rotation_euler", f, (0.75 * a, -sx * fluffmoth.LEG_SPLAY - sx * 0.45 * b, 0.0),
                             "CONSTANT")
    hero_rigs = rigs[n_field:]

    # Kai's face: set and tense on his back; wide surprised eyes as he sits up; then, by the hold, a slow, slightly
    # smug grin (he pulled it off): the grin creeps in over ~20 frames on 2s, the lids drop half way
    acting.face_keys(k, 1, eye_brow_down=0.55, face_angry=0.2, face_surprise=0.0, face_happy=0.0, eye_zitome=0.0,
                     eye_brow_up=0.0, eye_open=0.0)
    acting.face_keys(k, f_up + 4, eye_brow_down=0.0, face_angry=0.0, face_surprise=1.0, eye_brow_up=0.8, eye_open=0.6)
    g0 = f_up + 44
    for j, f in enumerate(range(g0, g0 + 22, 2)):
        u = (j + 1) / 11.0
        acting.face_keys(k, f, face_surprise=1.0 - u, eye_brow_up=0.8 * (1 - u), eye_open=0.6 * (1 - u),
                         face_happy=0.75 * u, eye_zitome=0.45 * u, eye_brow_down=0.2 * u)
    acting.blink(k, 1, n, every=(40, 70), seed=8, at=(f_up + 26,))

    # camera: in front of him (east, toward his feet), low, the moths big in the foreground; a slow push-in on 1s
    _hero_anchors("S15", n, hero_rigs)
    LAST.update(k=k, sh=sh, moths=rigs)
    return dict(frames=n, step=2, ones=(1, n), subject=[k["arm"], sh["root"]] + list(k.get("cap", [])))


# ----------------------------------------------------------------------------------------------------- dawn
DAWN_SUN = "#ffb487"            # a low peach-gold sun
DAWN_SKY = ("#8fb6e6", "#ffd2b0", "#ffd9c4")   # zenith, horizon, fill


def dawn(azim=75.0, elev=9.0):
    """Turn the day island into the first minutes after sunrise: the sun low in the east (long shadows across the
    track), a pink-gold horizon, a cooler blue zenith, the haze warmed."""
    sc = bpy.context.scene
    for o in list(sc.objects):
        if o.type == "LIGHT" and o.data.type == "SUN":
            bpy.data.objects.remove(o, do_unlink=True)
    look.world(sky=DAWN_SKY[0], horizon=DAWN_SKY[1], fill=DAWN_SKY[2], fill_strength=0.55)
    s = look.sun(elev=elev, azim=azim, energy=3.6, color=DAWN_SUN)
    s.data.angle = math.radians(4)
    nt = sc.node_tree
    for n in nt.nodes:                                                   # the haze colour: peach instead of sky blue
        if n.bl_idname == "CompositorNodeMixRGB" and n.blend_type == "MIX":
            n.inputs[2].default_value = look.hexc("#f6d9c8")
    from channels.monsters.mk import grade
    grade._grade(sc, dict(lift=(1.0, 0.985, 1.04), gamma=(1.0, 0.99, 0.97), gain=(1.12, 1.0, 0.86), sat=0.86,
                          vignette=0.28))                                # warm highlights, cool shadows, less green
    return s


# ------------------------------------------------------------------------------------------------------ S19B
def s19bot():
    n = _frames("S19", 177)                                          # the whole S19 (both panels)
    X._world(n)
    dawn(azim=82.0, elev=6.0)                                            # the sun ahead of him, low in the east
    H9.village_and_lake()
    _drop_huts([(-23.1, -173.4), (-17.7, -185.9)])                       # the two west huts behind him (in the lens)
    for nm in ("h9_tower", "h9_bell"):                                   # its posts and cut-off bell read as a second sun
        if nm in bpy.data.objects:
            bpy.data.objects[nm].hide_render = True
    sc = bpy.context.scene
    # the road out of the village: east along the beach above the waterline (helper 9's south shore), past the last
    # hut (helper 9's hut at (32.2, -177)), toward the sun coming up over the lake at the end of the road
    p0, p1 = Vector((2.0, -180.5, 0.0)), Vector((28.0, -182.0, 0.0))
    far = p1 + (p1 - p0).normalized() * 120.0
    far.y = H9._shore(far.x) + 5.0
    _path_strip("h5_s19_path", [p0 + (p0 - p1).normalized() * 50.0, p0, p1, (p1 + far) / 2, far], width=2.2)
    d = (p1 - p0).normalized()
    yaw = math.degrees(math.atan2(d.x, -d.y))                            # rot_z so the model's -Y points along d
    k = hero.load((0, 0, 0), scale=X.SCALE, outfit="world")
    arm = k["arm"]
    arm.rotation_mode = "XYZ"
    arm.rotation_euler = (0, 0, math.radians(yaw))
    arm.location = p0
    bpy.context.view_layer.update()
    P = x3.Pose(k)
    L = 0.86 * (p1 - p0).length / X.SCALE                                # armature units along -Y
    f_look0, f_look1 = _word("l19", "like") - 4, _word("l19", "Comment") + 4   # the look back ("like they said")

    def look_back(f):
        """0..1: the look back over his right shoulder (a quick turn, a held look, a slower turn front)."""
        return _ease((f - f_look0) / 8.0) * (1 - _ease((f - (f_look1 - 10)) / 12.0))

    def upper_at(f0, f1):
        def upper(P, t):
            f = f0 + (f1 - f0) * t
            lb = look_back(f)
            x3._arms_down(P, 9)
            P.rot("spine", (3, 0, -12 * lb))                             # the turn over his RIGHT shoulder, so the
            P.rot("chest", (-2 * lb, 0, -26 * lb))                       # shrimp on his left doesn't hide his face
            P.rot("neck", (0, 0, -32 * lb))
            P.rot("head 1", (-8 * lb, -4 * lb, -48 * lb))                # face in profile, chin up a touch
            sw = math.sin(f / 9.5 * math.pi) * (1 - lb)                  # arm swing with the steps
            P.rot("upper_arm.R", (14 * sw, 0, 0))
            P.rot("upper_arm.L", (-8 * sw, 0, 0))
        return upper

    # walk, stop and look back, walk on (armature space: -Y is forward)
    a = 0.56 * L
    feet = x3._walk(P, k, ((0, 0, 0), (0, -a, 0)), 1, f_look0 + 2, step_len=0.55, start_foot="R",
                    upper=upper_at(1, f_look0 + 2), every=2)
    x3._squat(P, feet, f_look0 + 2, f_look1 - 2, 0.0, 0.0, upper_at(f_look0 + 2, f_look1 - 2), every=2)
    x3._walk(P, k, ((0, -a, 0), (0, -L, 0)), f_look1, n, step_len=0.55, start_foot="R",
             upper=upper_at(f_look1, n), every=2)
    sh = shrimp_on_shoulder(k, "L", yaw=0.0)
    body = sh["body"]
    anim.key(body, "rotation_euler", 1, (0, 0, 0))
    anim.key(body, "rotation_euler", f_look0 + 4, (0, 0, 0))
    anim.key(body, "rotation_euler", f_look0 + 12, (0, 0, math.radians(150)))   # it turns to look back too
    anim.key(body, "rotation_euler", f_look1 + 2, (0, 0, math.radians(150)))
    anim.key(body, "rotation_euler", f_look1 + 12, (0, 0, 0))
    for f in range(1, n + 1, 12):                                        # bobbing with his steps
        anim.squash(body, f, 0.0)
        anim.squash(body, f + 6, -0.04)
    anim.blink(sh, f_look0 + 14)
    anim.on_twos(_shrimp_parts(sh), step=2)
    acting.blink(k, 1, n, at=(f_look0 + 6, f_look1 + 20))
    # render only the bottom band (helper 8's split, as Ep 2's S20bot): rows 486-1280
    sc.render.use_border = True
    sc.render.use_crop_to_border = False
    sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
    sc.render.border_min_y, sc.render.border_max_y = 0.0, 0.62
    # the camera: low on the beach behind him (west), looking east down the road; it follows him, slowly losing
    # ground so the road opens up ahead. His whole body sits at y ~700-1000 of the 1280 frame.
    mid0 = p0 + Vector((0, 0, 4.3))
    mid1 = p0.lerp(p1, 0.5) + Vector((0, 0, 4.3))
    cy = math.degrees(math.atan2(d.x, d.y))
    _cam("cam_s19bot", 1, n, (mid0, 42.0, 5.0, cy), (mid1, 48.0, 5.0, cy + 1.0), lens=40.0, blur=3.0,
         haze=(6.0, 6.0), shift_y=0.16)
    # the sun on the horizon at the end of the road (a little right, over the water): a bright disc the bloom haloes
    cam = sc.camera
    sc.frame_set(1)
    ce = cam.matrix_world.translation.copy()
    hdg = math.radians(cy + 8.0)
    SUN_D = 0.8 * cam.data.clip_end                                      # inside the far clip
    sun_at = ce + Vector((math.sin(hdg), math.cos(hdg), 0)) * SUN_D
    sun_at.z = ce.z + SUN_D * math.tan(math.radians(3.0))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=SUN_D * 0.026, segments=32, ring_count=16, location=sun_at)
    disc = bpy.context.object
    disc.name = "h5_dawn_sun"
    m = bpy.data.materials.new("h5_dawn_sun")
    m.use_nodes = True
    nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = look.hexc("#fff1c9")
    em.inputs["Strength"].default_value = 9.0
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    disc.data.materials.append(m)
    disc.visible_shadow = False
    for i, (r, st) in enumerate(((SUN_D * 0.058, 1.6), (SUN_D * 0.1, 0.7))):   # a soft glow round it
        bpy.ops.mesh.primitive_circle_add(vertices=48, radius=r, fill_type="TRIFAN", location=sun_at)
        g = bpy.context.object
        g.name = f"h5_dawn_glow{i}"
        g.rotation_euler = (math.pi / 2, 0, -hdg)
        g.location = sun_at + Vector((math.sin(hdg), math.cos(hdg), 0)) * (6.0 + i * 4)
        gm = bpy.data.materials.new(f"h5_dawn_glow{i}")
        gm.use_nodes = True
        gt = gm.node_tree
        for nd in list(gt.nodes):
            gt.nodes.remove(nd)
        tc = gt.nodes.new("ShaderNodeTexCoord")
        gr = gt.nodes.new("ShaderNodeTexGradient")
        gr.gradient_type = "SPHERICAL"
        mp = gt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1.0 / r, 1.0 / r, 1.0 / r)
        gt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        gt.links.new(mp.outputs[0], gr.inputs["Vector"])
        e2 = gt.nodes.new("ShaderNodeEmission")
        e2.inputs["Color"].default_value = look.hexc("#ffd59a")
        e2.inputs["Strength"].default_value = st
        tr = gt.nodes.new("ShaderNodeBsdfTransparent")
        mx = gt.nodes.new("ShaderNodeMixShader")
        gt.links.new(gr.outputs["Fac"], mx.inputs[0])
        gt.links.new(tr.outputs[0], mx.inputs[1])
        gt.links.new(e2.outputs[0], mx.inputs[2])
        o2 = gt.nodes.new("ShaderNodeOutputMaterial")
        gt.links.new(mx.outputs[0], o2.inputs["Surface"])
        gm.blend_method = "BLEND" if hasattr(gm, "blend_method") else None
        if hasattr(gm, "surface_render_method"):
            gm.surface_render_method = "BLENDED"
        g.data.materials.append(gm)
        g.visible_shadow = False
    LAST.update(k=k, sh=sh)
    return dict(frames=n, step=2, ones=(1, n), subject=[arm, sh["root"]])


SHOTS = {"S07": s07, "S15": s15, "S19bot": s19bot}
