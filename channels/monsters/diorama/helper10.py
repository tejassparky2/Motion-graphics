"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 10: S15, THE SNAP: 115 frames + a 12-frame
handle, the same beats on the same frames as the 3D S15 (the SFX are synced to them), staged for the tilted toy-world
camera (mk/diorama.py, island seed 31, the world MAP). Its five beats (D1-D5 from the earlier test):

    D1  1-18   wide of the clearing, slow push-in: Kai kneels at the pond reaching toward the shrimp; it blinks, looks
               up (13)
    D1b 19-41  close and steep on the shrimp: its eyes narrow (19-21), then its claw rises out of the pond past Kai's
               hand on 2s and is held, dripping (22-41, silence)
    D2  42-49  closer, locked on the shrimp: the strike (42); flash 44-45 and impact frames 46-49 are 2D (composite)
    D3  50-79  the money shot: the fan blast toward +Y, the white ring, the trees in the fan pop into dust in order of
               distance, leaving glowing stumps; the camera pulls up and back (dist 160 -> 290) to reveal
               it, shaken on 2s
    D4  80-93  Kai blown back toward the camera (-Y), tumbling, landing on his back short of the pond (on 2s); the
               camera follows
    D5  94-115 closer and steeper over him on his back, dazed; the knocked-out stars (composite); eyes close 111-113

    blender -b -y -P channels/monsters/render_shot.py -- diorama S15 OUT [--frames A-B] [--still N --scale 0.5]
    blender -b -y -P channels/monsters/render_shot.py -- diorama S15 OUT_SUB --frames 46-49 --subject
    python channels/monsters/diorama/helper10.py OUT OUT_SUB out/monsters/diorama/shots   (flash, impact, stars)

Characters on 2s/3s; every camera move and the 1s effects sit inside ones=(1, 95); D5 renders on 2s."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
try:
    import bpy
    from mathutils import Matrix, Vector
except ImportError:                                            # composite() runs outside Blender
    bpy = None

from channels.monsters.ep01v2 import helper10 as s15  # noqa: E402  (S15's poses, effects and 2D pass)

A, B, C, D, E, F, G, END, HANDLE = s15.A, s15.B, s15.C, s15.D, s15.E, s15.F, s15.G, s15.END, s15.HANDLE
LENS, BLUR = 100.0, 12.0
HAZE = (0.97, 0.55)                                            # diorama.camera's default haze band
STAR_PX, CAP_BOX = 32, (280, 495, 420, 580)                     # the D5 stars and where his cap is in D5
LAND_YAW = 0.21                                                 # where he lands (MAP["kai_down"], his hips) his head
                                                                # points ~12 deg west of +Y, toward the pond


def _pos(target, dist, tilt, yaw=0.0):
    el, az = math.radians(tilt), math.radians(yaw)
    return Vector(target) + dist * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))


def _key(c, frame, target, dist, tilt, offset=(0, 0, 0), yaw=0.0):
    """Key a diorama camera (place, aim, tilt-shift f-stop and the world's haze band) at one frame, CONSTANT: moves
    are keyed on every frame, so each frame is exact and the haze switches cleanly at the cuts."""
    from channels.monsters.mk import anim, diorama
    sc = bpy.context.scene
    p = _pos(target, dist, tilt, yaw)
    c.location = p + Vector(offset)
    c.rotation_euler = (Vector(target) - p).to_track_quat("-Z", "Y").to_euler()
    c.data.dof.focus_distance = dist
    c.data.dof.aperture_fstop = diorama.fstop_for(dist, c.data.lens, BLUR)
    c.data.clip_end = dist * 6
    c.keyframe_insert("location", frame=frame)
    c.keyframe_insert("rotation_euler", frame=frame)
    c.data.dof.keyframe_insert("focus_distance", frame=frame)
    c.data.dof.keyframe_insert("aperture_fstop", frame=frame)
    ms = sc.world.mist_settings
    ms.start, ms.depth = dist * HAZE[0], dist * HAZE[1]
    ms.keyframe_insert("start", frame=frame)
    ms.keyframe_insert("depth", frame=frame)
    for idb in (c, c.data, sc.world):
        ad = idb.animation_data
        if ad and ad.action:
            for fc in anim.all_fcurves(ad.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def _camera(name, frame, target, dist, tilt, yaw=0.0):
    from channels.monsters.mk import diorama
    c = diorama.camera(name, target, dist=dist, tilt=tilt, yaw=yaw, lens=LENS, blur=BLUR, frame=frame)
    _key(c, frame, target, dist, tilt, yaw=yaw)
    return c


LYING_RELAXED = [("spine", (0, 0, 1)), ("chest", (0, 0, 1)), ("upper_chest", (0, 0, 1)), ("neck", (0.1, 0.1, 1)),
                 ("head", (0.45, 0.15, 1)),                    # head tilted to one side
                 ("right_upper_arm", (0.35, 0.65, -0.7)), ("right_lower_arm", (-1, 0.45, 0.25)),   # over his chest
                 ("left_upper_arm", (-0.45, 0.1, -1)), ("left_lower_arm", (-0.35, 0.25, -1)),      # loose at his side
                 ("left_upper_leg", (-0.12, 0.45, -1)), ("right_upper_leg", (0.15, 0.3, -1)),      # knees a little bent
                 ("left_lower_leg", (-0.1, -0.2, -1)), ("right_lower_leg", (0.15, -0.12, -1)),
                 ("left_foot", (-0.25, 1, -0.3)), ("right_foot", (0.3, 1, -0.3))]
"""On his back, in Kai's own frame (+Y forward = up once he lies down, +Z toward his head): relaxed, so it reads as
lying from above, not as a standing T-pose."""


def _burn(origin, reach, f0, frames=15, seed=5):
    """The erased swath on the grass: a soft, irregular burn (~35% darker, a little warm, noisy edge) growing out from
    the blast with the ring, with ash and leaf bits scattered between the stumps."""
    from channels.monsters.mk import anim, look
    ox, oy = origin
    m = bpy.data.materials.new("diorama_burn")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    L, N = nt.links.new, nt.nodes.new
    out, tc, ln = N("ShaderNodeOutputMaterial"), N("ShaderNodeTexCoord"), N("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    nz = N("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 3.5
    nz.inputs["Detail"].default_value = 4.0
    add = N("ShaderNodeMath")
    add.operation = "MULTIPLY_ADD"                             # radius + (noise - 0.5) * 0.7: a ragged edge
    sub = N("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = 0.5
    add.inputs[1].default_value = 0.7
    edge = N("ShaderNodeMapRange")
    edge.inputs["From Min"].default_value, edge.inputs["From Max"].default_value = 0.55, 1.0
    edge.inputs["To Min"].default_value, edge.inputs["To Max"].default_value = 0.42, 0.0
    em, tr, mix = N("ShaderNodeEmission"), N("ShaderNodeBsdfTransparent"), N("ShaderNodeMixShader")
    em.inputs[0].default_value = look.hexc("#3b2a1c")
    L(tc.outputs["Object"], ln.inputs[0])
    L(tc.outputs["Object"], nz.inputs[0])
    L(nz.outputs["Fac"], sub.inputs[0])
    L(sub.outputs[0], add.inputs[0])
    L(ln.outputs["Value"], add.inputs[2])
    L(add.outputs[0], edge.inputs["Value"])
    L(edge.outputs["Result"], mix.inputs[0])
    L(tr.outputs[0], mix.inputs[1])
    L(em.outputs[0], mix.inputs[2])
    L(mix.outputs[0], out.inputs[0])
    m.surface_render_method = "BLENDED"
    bpy.ops.mesh.primitive_circle_add(vertices=64, radius=1.0, fill_type="NGON", location=(0, 0, 0))
    o = bpy.context.object
    o.name = "diorama_burn"
    o.data.materials.append(m)
    o.data.transform(Matrix.Translation((0, 0.55, 0)))           # the disc's near edge sits at the blast
    o.location = (ox, oy, 0.025)
    sx, sy = reach * 0.5, reach * 0.62
    anim.key(o, "scale", f0 - 1, 0.0, "CONSTANT")
    for f in range(f0, f0 + frames + 1):
        u = min(1.0, (f - f0 + 1) / frames)
        anim.key(o, "scale", f, (sx * u, sy * u, 1), "CONSTANT")
    ash = look.flat("diorama_ash", look.hexc("#2e2622"))
    rnd = random.Random(seed)
    for i in range(70):                                        # ash and charred leaf bits, there as the ring passes
        a = math.radians(rnd.uniform(-30, 30))
        d = rnd.uniform(6, reach * 0.95)
        x, y = ox + math.sin(a) * d, oy + math.cos(a) * d
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(0.18, 0.45), location=(x, y, 0.05))
        b = bpy.context.object
        flat = (1, rnd.uniform(0.4, 0.8), 0.25)
        b.rotation_euler = (0, 0, rnd.uniform(0, math.pi))
        b.data.materials.append(ash)
        anim.key(b, "scale", f0 - 1, 0.0, "CONSTANT")
        anim.key(b, "scale", f0 + max(1, int(d / reach * frames)), flat, "CONSTANT")
    return o


def _ease(u):
    return u * u * (3 - 2 * u)


def s15_diorama():
    from channels.monsters.mk import anim, diorama, erase, hero, look, meadow, puffshrimp
    sc = bpy.context.scene
    diorama.setup()
    isl = diorama.island(seed=31)
    SHRIMP = (*diorama.MAP["shrimp"], 0.0)
    LAND_HIPS = diorama.MAP["kai_down"]

    # ---- the shrimp behind the pond, its claw dipped in the water (S15's keys)
    rig = puffshrimp.build(SHRIMP)
    root, body, sh, hg = rig["root"], rig["body"], rig["shoulder"], rig["hinge"]
    DIP, UP, STRIKE = (1.8, 0.0, 0.3), (0.35, 0.75, 0.0), (-0.45, 0.55, 0.0)
    anim.key(sh, "rotation_euler", A, DIP, "CONSTANT")
    anim.key(hg, "rotation_euler", A, (0.1, 0, 0), "CONSTANT")
    anim.key(root, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    anim.key(body, "rotation_euler", A, (0, 0, 0), "CONSTANT")
    for f in range(A, 19, 6):
        anim.squash(body, f, -0.03, "CONSTANT")
        anim.squash(body, f + 3, 0.0, "CONSTANT")
    anim.key(root, "rotation_euler", 13, (0, 0, 0.18), "CONSTANT")   # notices the hand: turns and looks up
    anim.key(body, "rotation_euler", 13, (-0.14, 0, 0), "CONSTANT")
    for e in rig["eyes"]:
        anim.key(e, "scale", A, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 7, (1.1, 1, 0.1), "CONSTANT")
        anim.key(e, "scale", 8, (1, 1, 1), "CONSTANT")
        anim.key(e, "scale", 20, (1.12, 1, 0.55), "CONSTANT")
    for j, f in enumerate(range(C, C + 8, 2)):
        u = (j + 1) / 4
        anim.key(sh, "rotation_euler", f, tuple(a + (b - a) * u for a, b in zip(DIP, UP)), "CONSTANT")
    anim.key(hg, "rotation_euler", C + 6, (0.5, 0, 0), "CONSTANT")
    anim.squash(body, C, 0.0, "CONSTANT")
    anim.squash(body, C + 6, -0.06, "CONSTANT")
    anim.key(sh, "rotation_euler", D, STRIKE, "CONSTANT")
    anim.key(hg, "rotation_euler", D, (-0.25, 0, 0), "CONSTANT")
    anim.squash(body, D, 0.14, "CONSTANT")
    anim.squash(body, D + 2, -0.04, "CONSTANT")
    anim.squash(body, E + 3, 0.0, "CONSTANT")
    sc.frame_set(C + 7)
    drip = s15._claw_pt()
    meadow.drips((drip.x, drip.y, drip.z - 0.05), C + 3, D, every=5, fall=max(0.3, drip.z - 0.02))
    sc.frame_set(D + 1)
    blast = s15._claw_pt(lowest=False)

    # ---- Kai on his knees at the pond's south edge, reaching across toward the shrimp
    k = hero.load((0, 0, 0), scale=s15.KAI_SCALE, outfit="world")
    reach = Vector((SHRIMP[0] + 0.25, SHRIMP[1] - 1.45, 2.05))
    loc = Vector((SHRIMP[0] - 0.45, SHRIMP[1] - 6.4, 0))
    for _ in range(3):
        s15._apply_kneel(k, loc, 1.0, reach)
        loc.y += (reach - s15._world(k, "right_upper_arm")).length - 2.55
    for f, s in ((A, 0.0), (A + 3, 0.2), (A + 6, 0.45), (A + 9, 0.7), (A + 12, 0.9), (A + 15, 1.0)):
        s15._apply_kneel(k, loc, s, reach + (1 - s) * Vector((0.3, -1.6, 1.3)))
        s15._key_pose(k, f)
    hero.face(k, "relaxed", A, 0.6)
    y0 = loc.y
    flight = []
    for f, back, tilt, spin in ((F, 0.3, 0.15, 0.0), (F + 2, 1.0, 0.35, 0.3), (F + 4, 1.8, 0.6, 1.0),
                                (F + 6, 2.6, 0.9, 1.8), (F + 8, 3.2, 1.2, 2.6), (F + 10, 3.6, 1.4, 3.1)):
        u = (f - F) / 10                                      # blown back, tumbling with a half twist
        s15._pose(k, s15.BLOWN, (loc.x + 0.1 * back, y0 - back * 1.6, 1.0 + 7.0 * u * (1 - u) * 2.6), (tilt, 0, spin))
        s15._key_pose(k, f)
        flight.append((f, s15._world(k, "hips")))
    hero.face(k, "surprised", F)
    shadow = look.blob_shadow("kai_flight_shadow", (0, 0, 0.03), (2.6, 1.4))
    anim.key(shadow, "scale", A, 0.0, "CONSTANT")
    for f, p in flight:
        anim.key(shadow, "location", f, (p.x, p.y, 0.03), "CONSTANT")
        anim.key(shadow, "scale", f, (2.6 - 0.12 * p.z, 1.4 - 0.06 * p.z, 1), "CONSTANT")
    anim.key(shadow, "scale", G, 0.0, "CONSTANT")
    land = Vector((0, 0, 0))                                   # on his back, head toward the pond (D6 continues)
    for _ in range(2):
        s15._pose(k, LYING_RELAXED, tuple(land), (math.pi / 2, 0, math.pi + LAND_YAW))
        s15._ground(k)
        hip = s15._world(k, "hips")
        land += Vector((LAND_HIPS[0] - hip.x, LAND_HIPS[1] - hip.y, 0))
    s15._pose(k, LYING_RELAXED, tuple(land), (math.pi / 2, 0, math.pi + LAND_YAW))
    s15._ground(k)
    hip = s15._world(k, "hips")
    beam = diorama.sunbeam(s15._world(k, "chest"), radius=7.0)    # the shared light on him at kai_down (S15 D5-S21)
    beam.hide_render = True
    beam.keyframe_insert("hide_render", frame=A)
    beam.hide_render = False
    beam.keyframe_insert("hide_render", frame=G)
    body = look.blob_shadow("kai_down_shadow", (hip.x, hip.y, 0.03), (1.9, 5.2))   # a contact shadow, his length
    body.rotation_euler = (0, 0, LAND_YAW)
    anim.key(body, "scale", A, 0.0, "CONSTANT")
    anim.key(body, "scale", G, (1.9, 5.2, 1), "CONSTANT")
    from channels.monsters.mk import paintbg                   # dust settling around him (grey: not the cap's white)
    dm = paintbg.paint3("landing_dust", look.hexc("#a99f97"), look.hexc("#c6bdb4"), look.hexc("#ddd5cc"), noise=0.1)
    rnd = random.Random(12)
    for i in range(4):
        a = rnd.uniform(0, 2 * math.pi)
        p0 = (hip.x + math.cos(a) * rnd.uniform(2.5, 4.5), hip.y + math.sin(a) * rnd.uniform(3.0, 5.5), 0.6)
        d = erase._sphere(f"landdust{i}", p0, 1.0, dm, 12)
        r = rnd.uniform(0.3, 0.5)
        anim.key(d, "scale", G - 1, 0.0, "CONSTANT")
        anim.key(d, "location", G, p0)
        anim.key(d, "scale", G, r)
        anim.key(d, "scale", G + 16, r * 0.6)
        anim.key(d, "scale", G + 24, 0.0)
        anim.key(d, "location", G + 24, (p0[0], p0[1], 0.15))
        erase._twos_from(d, G)
    s15._key_pose(k, G)
    flight.append((G, s15._world(k, "hips")))
    face = (s15._world(k, "head") + s15._world(k, "head", True)) / 2
    hero.face(k, "surprised", G)
    hero.face(k, "blink", END - 4, 0.5)
    hero.face(k, "blink", END - 2)
    s15._flush_keys(k)

    # ---- cameras (every move keyed on every frame, inside ones)
    t1a, t1b = Vector((0.0, -3.4, 2.0)), Vector((0.0, -2.6, 2.2))
    c1 = _camera("D1_wide", A, t1a, 150.0, 58.0, 40.0)        # from the south-west: Kai and the shrimp side by side
    for f in range(A, B):                                       # slow push-in
        u = _ease((f - A) / (B - 1 - A))
        _key(c1, f, t1a.lerp(t1b, u), 150.0 - 10.0 * u, 58.0, yaw=40.0)
    # 19-41: close and steep on the shrimp, its face up to the lens: the eyes narrow (19-21, SG6), then the claw rises
    # past Kai's hand, dripping (IM2)
    sc.frame_set(B + 1)
    bpy.context.view_layer.update()
    ec = sum((e.matrix_world.translation for e in rig["eyes"]), Vector()) / 2
    _camera("D1b_shrimp", B, ec + Vector((-0.45, 0.1, 0.75)), 30.0, 55.0, 30.0)
    t2 = Vector((SHRIMP[0] - 0.6, SHRIMP[1] - 0.6, 2.0))
    _camera("D2_strike", D, t2, 80.0, 48.0, 40.0)
    t3a, t3b = Vector((0.0, -1.5, 2.0)), Vector((0.0, 14.0, 0.0))
    c3 = _camera("D3_reveal", E, t3a, 160.0, 64.0, 15.0)
    rnd = random.Random(8)
    sign = 1
    for f in range(E, F):                                       # pull up and back to reveal the swath, shaken on 2s
        u = _ease(min(1.0, (f - E) / 22))
        dist, tilt = 160.0 + 130.0 * u, 64.0 + 6.0 * u
        i = f - E
        off = (0, 0, 0)
        if i < 16:
            width = dist * (36.0 * 9 / 16) / LENS
            amp = 0.07 * (0.005 / 0.07) ** ((i // 2 * 2) / 16) * width
            if i % 2 == 0:
                sign = -sign
                jit = (rnd.uniform(0.7, 1.0), rnd.uniform(-0.4, 0.4))
            off = (amp * sign * jit[0], 0, amp * jit[1])
        _key(c3, f, t3a.lerp(t3b, u), dist, tilt, off, yaw=15.0)
    c4 = _camera("D4_blown", F, flight[0][1], 120.0, 42.0, 80.0)  # from the side and low: his arc and height read
    pts = [(f, Vector((p.x, p.y, min(p.z, 4.0)))) for f, p in flight]
    for f in range(F, G):                                      # follow him (smooth, on 1s)
        j = max(i for i in range(len(pts)) if pts[i][0] <= f)
        fa, pa = pts[j]
        fb, pb = pts[min(j + 1, len(pts) - 1)]
        u = 0 if fb == fa else (f - fa) / (fb - fa)
        _key(c4, f, pa.lerp(pb, u), 120.0, 42.0, yaw=80.0)
    _camera("D5_dazed", G, face + Vector((0, -1.8, 0)), 80.0, 74.0)

    # ---- D3: the fan blast toward +Y: ring, streak, the trees in the fan erased, glowing stumps
    origin = (blast.x, blast.y)
    fan = diorama.blast_spots(isl["spots"], origin)
    spots = [isl["spots"][i] for i in fan]
    sts = diorama.stumps(spots, origin)
    fx = erase.erase_trees([isl["trees"][i] for i in fan], origin=tuple(blast), f0=E - 1, cam=c3, stumps=sts,
                           direction=(0.0, 1.0))
    if fx["flash"] is not None:                                 # the 2D pass has the flash
        bpy.data.objects.remove(fx["flash"], do_unlink=True)
    _burn(origin, max(math.hypot(x - origin[0], y - origin[1]) for x, y, *_ in spots) + 10, E - 1)
    hot = sorted(zip(spots, fx["pop_frames"]), key=lambda s: math.hypot(s[0][0], s[0][1]))[:9]
    s15._puff_smoke([(x, y, diorama.TREE * 0.7, tp) for (x, y, *_), tp in hot], END + 1, size=diorama.TREE * 0.6)
    print("S15 BLAST_ORIGIN", tuple(round(v, 3) for v in blast), "KAI_LYING", tuple(round(v, 3) for v in land),
          "FACE", tuple(round(v, 3) for v in face), "FAN", len(fan), flush=True)
    return dict(frames=END + HANDLE, step=2, ones=(A, G + 1), subject=[root])


SHOTS = {"S15": s15_diorama}


def composite(raw, sub, out_dir):
    """The 2D pass (S15's): flash 44-45, impact frames 46-49 on 2s from the subject pass, knocked-out stars in D5."""
    return s15.composite(raw, sub, out_dir, name="S15", star_px=STAR_PX, cap_box=CAP_BOX, cap_white=200)


if __name__ == "__main__" and bpy is None:
    print(composite(sys.argv[1], sys.argv[2], sys.argv[3]))
