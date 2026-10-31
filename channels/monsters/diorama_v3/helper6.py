"""Episode 1 v3 in diorama 2.5D (channels/monsters/DIORAMA_EP01_V3.md), helper 6:

    S23c "The shrimp had no idea." Dramatic irony (coordinator): the puff-shrimp keeps drinking at the pond's east
         edge (MAP["shrimp_drink"]), facing south, its claw dipped in the water, eyes shut in bliss (lids down, one
         happy flutter), little sips with sip bubbles and a sway on 2s. Behind it, soft in the background: the thorn
         tree with the dark butcher bird on top (as in S24 A). The bird's crisp spread-wing shadow (S24 A's tone and
         edge) sweeps in from the tree's side, grows a little as the bird comes and settles over the shrimp; through
         the handle it keeps S24 A's slow creep. A low camera from the pond side (west-south-west), the shrimp in
         the lower third, Kai (knocked flat to the south-west) out of the frame, pushing in slowly on 1s.

The set is the island after v3's snap exactly as S23b and S24 have it (diorama_v3/xprl._set: bgqrs v3's set with the
grove's stumps, Kai knocked flat in LYING_V3_L beyond the pond); the shrimp is placed by diorama_v3/xprl._shrimp(); the shadow is
tuftwing's, softened as in XprL's S23 insert.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S23c OUT_DIR [--still N --scale 0.5]
"""
import math
import random

import bpy
from mathutils import Vector

from channels.monsters.diorama import xprl as dx
from channels.monsters.diorama_v3 import xprl as v3x
from channels.monsters.diorama_v3.shots import v3_frames
from channels.monsters.ep01v2 import xprl as x3
from channels.monsters.mk import acting, anim, diorama, look


def _sipping(sh, n, period=18, sway=0.05):
    """Small idle life while it drinks (mk/acting.py easing, on 2s): every `period` frames the claw lifts a little out
    of the water and dips back (a sip, with anticipation and overshoot), and the body sways side to side on a
    different rhythm, so it never freezes while the shadow slides over."""
    shoulder, body = sh["shoulder"], sh["body"]
    down, up = (1.76, 0.0, 0.0), (1.6, 0.0, 0.0)
    f = 2
    while f + period <= n:
        acting.move(shoulder, "rotation_euler", f, f + period // 2, down, up, kind="back", amount=0.08)
        acting.move(shoulder, "rotation_euler", f + period // 2, f + period, up, down, kind="back", amount=0.1)
        f += period
    f, side = 1, 1
    while f + 22 <= n + 22:
        acting.move(body, "rotation_euler", f, f + 22, (0, 0, -side * sway), (0, 0, side * sway), kind="inout")
        f, side = f + 22, -side


SHRIMP = v3x.SHRIMP
CAM = (8.2, 12.0, 45.0, 0.31)           # dist, tilt, lens, shift_y: low, the shrimp in the lower third, the whole
                                        # spread-wing shadow, the thorn tree and the bird on top all in the frame
TURN = -6.0                             # degrees off the thorn-tree line, toward the shrimp's face (it faces south)
END_BACK = 0.5                          # where the shadow settles: its body just behind the shrimp, over it
HAZE = (14.0, 40.0)                     # mist start (dist + this), depth: the tree and the dark bird stay readable
FSTOP = 2.5                             # x the diorama's tilt-shift f-stop (the far tree softer, not mush)
CASTER_Z = 0.0                          # a real-shadow caster's height (0: off; the painted decal + _shade_sweep)
TURN_SHRIMP = -35.0                     # it turns a little toward the lens (its claw swings aside, still in the water)


def _bubbles(sh, n, period=18, seed=5):
    """Little sip bubbles: as the claw dips back in after each sip, two or three tiny bubbles rise from its tip at the
    water line, swell a little and pop (on 2s)."""
    rnd = random.Random(seed)
    mat = look.toon("s23c_bubble", look.hexc("#eaf8ff"), shade=0.9, gloss=True)
    f = 2 + period - 3
    k = 0
    while f + 8 <= n:
        tip = x3._claw_tip(sh, f)
        for j in range(rnd.choice((2, 3))):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1.0)
            b = bpy.context.object
            b.name = f"s23c_bubble{k}"
            k += 1
            b.data.materials.append(mat)
            r = rnd.uniform(0.05, 0.09)
            x0 = tip + Vector((rnd.uniform(-0.15, 0.15), rnd.uniform(-0.15, 0.15), 0.02))
            g0 = f + 2 * j
            g1 = g0 + rnd.choice((6, 8))
            anim.key(b, "scale", 1, (0.001,) * 3, "CONSTANT")
            anim.key(b, "scale", g0, (r * 0.6,) * 3, "CONSTANT")
            anim.key(b, "location", g0, tuple(x0), "CONSTANT")
            for g in range(g0 + 2, g1 + 1, 2):
                u = (g - g0) / (g1 - g0)
                anim.key(b, "scale", g, (r * (0.6 + 0.5 * u),) * 3, "CONSTANT")
                anim.key(b, "location", g, tuple(x0 + Vector((0.03 * u, 0, 0.35 * u))), "CONSTANT")
            anim.key(b, "scale", g1 + 2, (0.001,) * 3, "CONSTANT")             # pop
        f += period


def _bliss(sh, n):
    """Eyes shut in bliss: each eye squeezed to a thin dark line (the blink's shut drawing, held), with one slow happy
    flutter mid-shot (they half-open a moment, then shut again). No lids, no highlights."""
    shut, half = (1.12, 1.0, 0.09), (1.05, 1.0, 0.3)
    for e in sh["eyes"]:
        for f, v in ((1, shut), (39, shut), (41, shut), (43, shut), (24, shut), (26, half), (30, shut)):
            anim.key(e, "scale", f, v, "CONSTANT")
    anim.lids(sh, 1, 0.0)
    for h in sh.get("hi", []):
        anim.key(h, "scale", 1, 0.001, "CONSTANT")


def _to_sun():
    sun = next((o for o in bpy.context.scene.objects if o.type == "LIGHT" and o.data.type == "SUN"), None)
    return -(sun.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()


def _caster(decal):
    """An invisible copy of the shadow's silhouette lifted toward the sun: the scene's sun casts it as a REAL shadow,
    so it falls over the shrimp too (and its sip bubbles), not only on the grass. Seen by shadows only."""
    me = decal.data.copy()
    img = next(nd for nd in decal.data.materials[0].node_tree.nodes if nd.type == "TEX_IMAGE").image
    m = bpy.data.materials.new("s23c_caster")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    cut = nt.nodes.new("ShaderNodeMath")
    cut.operation = "GREATER_THAN"
    cut.inputs[1].default_value = 0.3
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    df = nt.nodes.new("ShaderNodeBsdfDiffuse")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Alpha"], cut.inputs[0])
    nt.links.new(cut.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(df.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    for attr, v in (("surface_render_method", "DITHERED"), ("use_transparent_shadow", True), ("blend_method", "HASHED")):
        if hasattr(m, attr):
            setattr(m, attr, v)
    me.materials.clear()
    me.materials.append(m)
    c = bpy.data.objects.new("s23c_shadow_caster", me)
    bpy.context.scene.collection.objects.link(c)
    c.parent = decal.parent
    c.matrix_parent_inverse = decal.matrix_parent_inverse.copy()
    c.rotation_euler = decal.rotation_euler.copy()
    c.visible_camera = False
    for attr in ("visible_diffuse", "visible_glossy", "visible_transmission", "visible_volume_scatter"):
        setattr(c, attr, False)
    return c


def _shade_sweep(objs, d, front, tone="#1d2440", amount=0.55):
    """The shadow falling over the shrimp itself: every material on `objs` mixes toward the shadow tone where the
    world point lies behind the shadow's leading edge, measured along `d` (the way the shadow travels); `front` is
    [(frame, edge)] with edge in world units along d. The edge sweeps across it, so it reads as the bird's shadow
    passing onto it, not a light dimming."""
    mats = {m for o in objs if o.type == "MESH" for m in o.data.materials if m}
    val = None
    for m in mats:
        nt = m.node_tree
        out = next((nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL" and nd.is_active_output), None)
        if out is None or not out.inputs[0].links:
            continue
        src = out.inputs[0].links[0].from_socket
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        dv = nt.nodes.new("ShaderNodeCombineXYZ")
        for i in range(3):
            dv.inputs[i].default_value = d[i]
        dot = nt.nodes.new("ShaderNodeVectorMath")
        dot.operation = "DOT_PRODUCT"
        edge = nt.nodes.new("ShaderNodeValue")
        edge.name = "s23c_edge"
        lt = nt.nodes.new("ShaderNodeMath")
        lt.operation = "LESS_THAN"
        k = nt.nodes.new("ShaderNodeMath")
        k.operation = "MULTIPLY"
        k.inputs[1].default_value = amount
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs[0].default_value = look.hexc(tone)
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(geo.outputs["Position"], dot.inputs[0])
        nt.links.new(dv.outputs[0], dot.inputs[1])
        nt.links.new(dot.outputs["Value"], lt.inputs[0])
        nt.links.new(edge.outputs[0], lt.inputs[1])
        nt.links.new(lt.outputs[0], k.inputs[0])
        nt.links.new(k.outputs[0], mix.inputs[0])
        nt.links.new(src, mix.inputs[1])
        nt.links.new(em.outputs[0], mix.inputs[2])
        nt.links.new(mix.outputs[0], out.inputs[0])
        for f, v in front:
            edge.outputs[0].default_value = v
            edge.outputs[0].keyframe_insert("default_value", frame=f)
        val = edge
    return val


def _shadow_in(bird, n, f_land=48):
    """The bird's shadow as S24 A has it (a crisp silhouette, wings spread, tone and edge the same), sweeping in from
    the thorn tree's side and settling over the shrimp, growing a little as the bird comes down: at f_land it is
    exactly S24 A's first frame (place and scale), and through the handle it keeps S24 A's slow creep and growth."""
    over = Vector((SHRIMP[0] - 0.3, SHRIMP[1] - 0.2, 0.0))   # S24 A's (c76631e): body under the shrimp at its end
    n24 = v3x._frames("S24", 162)
    perch = Vector((bird["root"].location.x, bird["root"].location.y, 0.0))
    back = (perch - over).normalized()
    dx._soft_shadow(bird, tuple(over + back * END_BACK - perch), (0.0, 0.0, 0.0), 1, 2,
                    tone="#1d2440", opacity=0.78, soften=1.0, shrink=0.8)
    sh = bird["shadow"]
    sh.animation_data_clear()
    to_local = sh.parent.matrix_world.to_3x3().inverted()
    l_end = sh.location.copy()
    l_start = l_end + to_local @ (back * 11.0)
    creep = to_local @ (-back * 4.0 / (n24 - 1))               # S24 A: 4 units over its frames
    caster, up = (_caster(sh), to_local @ (_to_sun() * (CASTER_Z / _to_sun().z))) if CASTER_Z else (None, None)
    for f in range(1, n + 1):
        if f <= f_land:
            u = (f - 1) / (f_land - 1)
            e = 1 - (1 - u) ** 3                               # sweeps in fast, settles
            loc, s = l_start.lerp(l_end, e), 0.78 + 0.22 * e
        else:
            loc, s = l_end + creep * (f - f_land), 1.0 + 0.35 * (f - f_land) / (n24 - 1)
        anim.key(sh, "location", f, tuple(loc), "LINEAR")
        anim.key(sh, "scale", f, (s, s, 1), "LINEAR")
        if caster is not None:
            anim.key(caster, "location", f, tuple(loc + up), "LINEAR")
            anim.key(caster, "scale", f, (s, s, 1), "LINEAR")
    if caster is not None:
        sh.hide_render = True                                  # the caster's real shadow replaces the painted decal
    # where its leading edge (the head, ~0.35 of the span ahead of the centre) is along the travel direction
    d = -back
    span = 11.0
    front = []
    for f in range(1, n + 1, 2):
        if f <= f_land:
            e = 1 - (1 - (f - 1) / (f_land - 1)) ** 3
            c, sc_ = -END_BACK - 11.0 * (1 - e), 0.78 + 0.22 * e
        else:
            c, sc_ = -END_BACK + 4.0 * (f - f_land) / (n24 - 1), 1.0
        front.append((f, Vector(SHRIMP).dot(d) + c + 0.35 * span * sc_))
    return d, front


def s23c():
    n = v3_frames("S23c")
    diorama.setup()
    isl, kai = v3x._set(n, kai_down=True)                     # v3's after-snap set, as S23b and S24 either side
    sh = v3x._shrimp(n)
    sh["root"].rotation_euler.z += math.radians(TURN_SHRIMP)
    bpy.context.view_layer.update()
    _sipping(sh, n)
    _bliss(sh, n)
    dx._twos([sh["shoulder"], sh["body"]] + sh["eyes"] + sh["lids"] + sh["hi"])
    _bubbles(sh, n)
    perch = Vector(isl["thorn"]["perch"])
    bird = v3x._bird_on_perch(perch, Vector(SHRIMP))           # on its thorn, soft behind the shrimp
    v3x.dark_form(1, lids_down=1)                              # XprL's predator form (S23/S23b): mask, amber slits
    d, front = _shadow_in(bird, n)
    objs = [sh["root"]] + list(sh["root"].children_recursive) + [o for o in bpy.data.objects if o.name.startswith("s23c_bubble")]
    _shade_sweep(objs, d, front)
    # low, from the pond side (west-south-west, the line from the thorn tree through the shrimp): its blissful face,
    # the thorn tree and the dark bird soft behind it; Kai (south-south-west) stays out of the narrow frame
    face = Vector(SHRIMP) + Vector((0.0, 0.0, 1.2))
    yaw = math.degrees(math.atan2(perch.x - face.x, perch.y - face.y))
    a = (tuple(face), CAM[0], CAM[1], yaw + TURN - 1.0, CAM[2], CAM[3])
    b = (tuple(face), CAM[0] * 0.88, CAM[1], yaw + TURN + 1.0, CAM[2], CAM[3])
    cam = dx._move("cam_s23c", 1, n, a, b, n)
    fc = next(c for c in anim.all_fcurves(cam.data.animation_data.action) if c.data_path == "dof.aperture_fstop")
    for kp in fc.keyframe_points:                              # less blur: the dark bird's mask must read
        kp.co.y *= FSTOP
    ms = bpy.context.scene.world.mist_settings                # the haze reaches the tree softly, not as a wall
    for f in range(1, n + 1):
        d = CAM[0] * (1 - 0.12 * dx._smooth((f - 1) / (n - 1)))
        ms.start, ms.depth = d + HAZE[0], HAZE[1]
        ms.keyframe_insert("start", frame=f)
        ms.keyframe_insert("depth", frame=f)
    return dict(frames=n, step=1, subject=[sh["root"]])


SHOTS = {"S23c": s23c}
