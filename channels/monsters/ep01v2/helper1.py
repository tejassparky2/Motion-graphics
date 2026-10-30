"""Episode 1 (v2) shots by helper 1, in the lab (mk/lab.py): S03a, S03b, S05b. See channels/monsters/EP01V2_SHOTS.md and
the rules in reports/Pokémon episodes story and animation.md.

    S03a  "Wildlife biology student. Night shift at the lab." (first half): Kai at the desk beside the glowing hero
          tank, back three-quarter, cold blue (LC1); a locked camera (SG4), rain and bubbles alive on 1s (LC10), Kai's
          lean toward the tank acted on 3s (IM2).
    S03b  (second half): close on Kai's face, lit cyan by the tank, looking at the shrimp; ONE face change, neutral to a
          small fond smile (SG2). Locked, nothing on 1s in frame, so step 3 (TP13).
    S05b  "But only in water." (second half): Kai's face as the bubble's flash fades on it (light on 1s); then he taps
          the glass once with one finger, the bond gesture to repeat later (BD2). Acting on 3s, the tap on 2s.

Kai is mk/hero.py's hero.blend in his "earth" outfit (scale 1.1), seated at the lab desk facing the window; the tank
is on his right. Lengths are TIMING.md's (v7), each with a 12-frame tail handle. Kai narrates over these shots, so
his mouth stays closed.
"""
import math
import os

import bpy
from mathutils import Matrix, Vector

from channels.monsters.mk import anim, hero, lab

TAIL = 12
LEN = dict(S03a=41, S03b=39, S05b=39)          # frames in the cut (ep01v2/TIMING.md, v7); rendered with +TAIL
H = 1.1                                        # hero.load scale for metre scenes (HELPERS.md v6)
SEAT_Y = 1.42                                  # the chair pulled in to the desk (front edge at y = 1.78)


# ------------------------------------------------------------------------------------------------ Kai at the desk
def _kai(lab_h):
    """Load Kai (earth outfit), turn him to face the desk (+Y) and pull his chair in. Returns the rig."""
    if "wear_earth" not in bpy.data.images:          # hero.blend may not carry the earth shirt yet
        bpy.data.images.load(os.path.join(hero.A, "wear_earth.png")).name = "wear_earth"
    chair = lab_h["chair"]
    chair.location.y = SEAT_Y
    bpy.context.view_layer.update()
    seat = lab_h["seat"].matrix_world.translation
    rig = hero.load((seat.x, seat.y + 0.05, seat.z + 0.06 - 0.796 * H), scale=H, outfit="earth")
    rig["arm"].rotation_mode = "XYZ"                 # the armature comes in quaternion mode: rot_z alone is ignored
    rig["arm"].rotation_euler = (0, 0, math.pi)      # face the desk (+Y)
    bpy.context.view_layer.update()
    return rig


def _aim(rig, name, direction, twist=0.0):
    """Point a bone along a direction given in the CHARACTER's frame (x = his left, y = his back, z = up: the
    armature's own space), with an optional twist about the bone (radians). Pose parents before children."""
    arm = rig["arm"]
    pb = rig["bone"](name) if not isinstance(name, bpy.types.PoseBone) else name
    bpy.context.view_layer.update()
    m = pb.matrix.copy()
    cur = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    q = cur.rotation_difference(Vector(direction).normalized())
    rot = q.to_matrix() @ m.to_3x3()
    if twist:
        rot = Matrix.Rotation(twist, 3, rot @ Vector((0, 1, 0))) @ rot
    pb.matrix = Matrix.Translation(m.translation) @ rot.to_4x4()
    bpy.context.view_layer.update()
    del arm


def _key_pose(rig, frame, names, interp="CONSTANT"):
    """Key the rotations of the given bones at `frame` (anime poses snap between drawings)."""
    arm = rig["arm"]
    for n in names:
        pb = rig["bone"](n) if isinstance(n, str) else n
        pb.keyframe_insert("rotation_quaternion", frame=frame)
    for fc in anim.all_fcurves(arm.animation_data.action):
        for kp in fc.keyframe_points:
            if abs(kp.co.x - frame) < 0.01:
                kp.interpolation = interp


BODY = ("spine", "chest", "neck", "head", "left_upper_leg", "right_upper_leg", "left_lower_leg", "right_lower_leg",
        "left_foot", "right_foot", "left_upper_arm", "right_upper_arm", "left_lower_arm", "right_lower_arm",
        "left_hand", "right_hand")


def _fingers(rig, side, curl, index_curl=None):
    """Curl a hand's fingers (radians per joint); `index_curl` lets the index finger point while the rest curl."""
    arm = rig["arm"]
    for b in arm.pose.bones:
        n = b.name
        if not n.endswith("." + side) or n.startswith("robo") or not n.startswith(("f_", "thumb")):
            continue
        c = index_curl if (index_curl is not None and n.startswith("f_index")) else curl
        if n.startswith("thumb"):
            c *= 0.4
        b.rotation_mode = "QUATERNION"
        b.rotation_quaternion = Matrix.Rotation(c, 4, "X").to_quaternion()


def _sit(rig, lean=0.12, look=(0.0, 0.0), right_reach=None):
    """The seated pose at the desk. `look` = (yaw toward his right, pitch down) in radians; `right_reach` = a world
    point for the right index fingertip to reach (the tap), else both forearms rest on the desk."""
    # legs: thighs forward, shins down, feet flat (the character faces his own -Y)
    for s in ("left", "right"):
        _aim(rig, f"{s}_upper_leg", (0.0, -1.0, -0.08))
        _aim(rig, f"{s}_lower_leg", (0.0, 0.12, -1.0))
        _aim(rig, f"{s}_foot", (0.0, -1.0, -0.25))
    _aim(rig, "spine", (0.0, -lean, 1.0))
    _aim(rig, "chest", (0.0, -lean * 1.4, 1.0))
    yaw, pitch = look
    _aim(rig, "neck", (0.0, -0.15 - pitch * 0.4, 1.0))
    _aim(rig, "head", (0.0, -0.1 - pitch, 1.0), twist=-yaw)
    # arms: forearms on the desk, hands loose
    for s, sx in (("left", 1.0), ("right", -1.0)):
        if s == "right" and right_reach is not None:
            continue
        _aim(rig, f"{s}_upper_arm", (sx * 0.22, -0.45, -0.85))
        _aim(rig, f"{s}_lower_arm", (-sx * 0.28, -1.0, 0.08))
        _aim(rig, f"{s}_hand", (-sx * 0.2, -1.0, -0.05))
        _fingers(rig, "L" if s == "left" else "R", 0.35)
    if right_reach is not None:
        _reach(rig, "right", Vector(right_reach))
        _fingers(rig, "R", 1.1, index_curl=0.05)


def _reach(rig, side, target):
    """Two-bone reach: aim the upper arm and forearm so the hand lands on `target` (world)."""
    arm = rig["arm"]
    inv = arm.matrix_world.inverted()
    up, lo, hand = (rig["bone"](f"{side}_{n}") for n in ("upper_arm", "lower_arm", "hand"))
    bpy.context.view_layer.update()
    sh = up.head.copy()
    t = inv @ target
    a = (up.tail - up.head).length
    b = (hand.head - lo.head).length
    d = t - sh
    dist = min(d.length, (a + b) * 0.999)
    dn = d.normalized()
    # the elbow sits off the shoulder-target line, toward "down and a little out" (never up)
    out = Vector((-0.4 if side == "right" else 0.4, 0.0, -1.0))
    perp = (out - dn * out.dot(dn)).normalized()
    along = (a * a - b * b + dist * dist) / (2 * dist)
    h = math.sqrt(max(0.0, a * a - along * along))
    elbow = sh + dn * along + perp * h
    upper_dir = elbow - sh
    _aim(rig, up, upper_dir)
    bpy.context.view_layer.update()
    _aim(rig, lo, t - lo.head)
    _aim(rig, hand, t - lo.head)


# ------------------------------------------------------------------------------------------------ the shots
def _lab():
    h = lab.build()
    sc = bpy.context.scene
    return h, sc


def _cam(name, loc, target, lens, focus=None, fstop=None):
    cd = bpy.data.cameras.new(name)
    cd.lens, cd.clip_start, cd.clip_end = lens, 0.02, 60
    o = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if fstop:
        cd.dof.use_dof, cd.dof.aperture_fstop = True, fstop
        cd.dof.focus_distance = (Vector(focus or target) - Vector(loc)).length
    bpy.context.scene.camera = o
    return o


TANK_CYAN = "#4fd8e8"          # the tank's light on Kai: a saturated cyan (QA, LC9), from one side only


def _face_light(name, loc, target, energy, color=TANK_CYAN, size=0.25):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy, ld.color, ld.size, ld.use_shadow = energy, lab.hx(color)[:3], size, False
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


def _head_pos(rig):
    bpy.context.view_layer.update()
    pb = rig["bone"]("head")
    return rig["arm"].matrix_world @ ((pb.head + pb.tail) / 2)


def _focus_face(cam, rig):
    """Focus a close-up on the face: the head's middle, pulled toward the camera by the face's depth."""
    bpy.context.view_layer.update()
    cam.data.dof.focus_distance = (_head_pos(rig) - cam.matrix_world.translation).length - 0.085 * H


def _tint_hero(k=0.35, cool=(0.74, 0.93, 1.0)):
    """hero.blend's toon shade turns the light grey before the two-tone ramp, so a coloured light can't tint Kai. Add
    the coloured light back on top (like the lab grade does for the room), then multiply by the lab's cool night
    colour, so the tank lights him cyan and the cap and skin don't read as white (LC1, LC9)."""
    mats = ["hair", "huku_bake", "body_bake", "body_nm"]
    mats += [m.name for m in bpy.data.materials if m.name.startswith("cap")]
    for name in mats:
        m = bpy.data.materials.get(name)
        if not m or not m.use_nodes or "lab_tint" in m.node_tree.nodes:
            continue
        nt = m.node_tree
        em = next((n for n in nt.nodes if n.type == "EMISSION"), None)
        if em is None or not em.inputs[0].links:
            continue
        src = em.inputs[0].links[0].from_socket
        s2r = next((n for n in nt.nodes if n.type == "SHADERTORGB"), None)
        if s2r is not None:
            # the light's hue (normalised) times its strength capped at 1, times k: coloured, never blown out
            nrm = nt.nodes.new("ShaderNodeVectorMath")
            nrm.operation = "NORMALIZE"
            ln = nt.nodes.new("ShaderNodeVectorMath")
            ln.operation = "LENGTH"
            cap1 = nt.nodes.new("ShaderNodeMath")
            cap1.operation, cap1.inputs[1].default_value = "MINIMUM", 1.0
            kk = nt.nodes.new("ShaderNodeMath")
            kk.operation, kk.inputs[1].default_value = "MULTIPLY", k
            sc = nt.nodes.new("ShaderNodeVectorMath")
            sc.operation = "SCALE"
            add = nt.nodes.new("ShaderNodeVectorMath")
            add.operation = "ADD"
            nt.links.new(s2r.outputs[0], nrm.inputs[0])
            nt.links.new(s2r.outputs[0], ln.inputs[0])
            nt.links.new(ln.outputs["Value"], cap1.inputs[0])
            nt.links.new(cap1.outputs[0], kk.inputs[0])
            nt.links.new(kk.outputs[0], sc.inputs["Scale"])
            nt.links.new(nrm.outputs[0], sc.inputs[0])
            nt.links.new(src, add.inputs[0])
            nt.links.new(sc.outputs[0], add.inputs[1])
            src = add.outputs[0]
        mul = nt.nodes.new("ShaderNodeVectorMath")
        mul.operation, mul.name = "MULTIPLY", "lab_tint"
        mul.inputs[1].default_value = cool
        nt.links.new(src, mul.inputs[0])
        nt.links.new(mul.outputs[0], em.inputs[0])


def _tank_glow(side, cyan=(0.18, 0.82, 0.92), mix=0.5, rim=0.6, warm=0.9):
    """S03b v3: keep his skin skin-coloured and put the tank's cyan only where the light falls. On each of Kai's toon
    materials: the lit band (the toon ramp's white) is multiplied toward cyan by `mix`; the shadow band keeps the
    skin's own lavender shadow tone; a thin hard-edged cyan rim lights the silhouette on the side facing the tank
    (world direction `side`); `warm` keeps the lit skin's value near 0.8."""
    for name in ("hair", "huku_bake", "body_bake", "body_nm"):
        m = bpy.data.materials.get(name)
        if not m or "tank_glow" in m.node_tree.nodes:
            continue
        nt = m.node_tree
        N, L = nt.nodes.new, nt.links.new
        em = next(n for n in nt.nodes if n.type == "EMISSION")
        ramp = next(n for n in nt.nodes if n.type == "VALTORGB")
        src = em.inputs[0].links[0].from_socket
        # lit mask from the toon ramp: 1 in the lit band, 0 in the shadow band
        sep = N("ShaderNodeSeparateColor")
        L(ramp.outputs[0], sep.inputs[0])
        lit = N("ShaderNodeMapRange")
        lit.inputs["From Min"].default_value, lit.inputs["From Max"].default_value = 0.8, 1.0
        L(sep.outputs[0], lit.inputs["Value"])
        k = N("ShaderNodeMath")
        k.operation, k.inputs[1].default_value = "MULTIPLY", mix
        L(lit.outputs[0], k.inputs[0])
        tint = N("ShaderNodeMix")
        tint.data_type, tint.blend_type = "RGBA", "COLOR"            # the cyan's hue over the skin's value
        L(k.outputs[0], tint.inputs["Factor"])
        L(src, tint.inputs[6])
        tint.inputs[7].default_value = (*cyan, 1)
        # the rim: facing ramp (silhouette) x how much the surface faces the tank
        lw = N("ShaderNodeLayerWeight")
        lw.inputs["Blend"].default_value = 0.3
        edge = N("ShaderNodeMapRange")
        edge.inputs["From Min"].default_value, edge.inputs["From Max"].default_value = 0.5, 0.54
        L(lw.outputs["Facing"], edge.inputs["Value"])
        geo = N("ShaderNodeNewGeometry")
        dot = N("ShaderNodeVectorMath")
        dot.operation = "DOT_PRODUCT"
        dot.inputs[1].default_value = tuple(side.normalized())
        L(geo.outputs["Normal"], dot.inputs[0])
        facing = N("ShaderNodeMapRange")
        facing.inputs["From Min"].default_value, facing.inputs["From Max"].default_value = 0.25, 0.35
        L(dot.outputs["Value"], facing.inputs["Value"])
        rk = N("ShaderNodeMath")
        rk.operation = "MULTIPLY"
        L(edge.outputs[0], rk.inputs[0])
        L(facing.outputs[0], rk.inputs[1])
        rk2 = N("ShaderNodeMath")
        rk2.operation, rk2.inputs[1].default_value = "MULTIPLY", rim
        L(rk.outputs[0], rk2.inputs[0])
        rimc = N("ShaderNodeMix")
        rimc.data_type, rimc.blend_type = "RGBA", "MIX"
        L(rk2.outputs[0], rimc.inputs["Factor"])
        L(tint.outputs[2], rimc.inputs[6])
        rimc.inputs[7].default_value = (0.55, 0.95, 1.0, 1)
        val = N("ShaderNodeVectorMath")
        val.operation, val.name = "SCALE", "tank_glow"
        val.inputs["Scale"].default_value = warm
        L(rimc.outputs[2], val.inputs[0])
        L(val.outputs[0], em.inputs[0])


def _catchlights(rig, cam, until, color="#9ff2ff", r=0.0035):
    """Tiny cyan glints in his eyes (the tank reflected), visible until frame `until` (when the eyes close). The
    posed head mesh's "eye" faces are split into the two eyes by their position across the camera's view; each glint
    sits just in front of its eye's centre, toward the camera."""
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    sc = bpy.context.scene
    head = bpy.data.objects["head"]
    eye_idx = {i for i, m in enumerate(head.data.materials) if m and m.name == "eye"}
    dg = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(dg)
    me = ev.to_mesh()
    camp = cam.matrix_world.translation
    pts = [head.matrix_world @ poly.center for poly in me.polygons if poly.material_index in eye_idx]
    ev.to_mesh_clear()
    if not pts:
        return
    sx = sorted((world_to_camera_view(sc, cam, p).x, i) for i, p in enumerate(pts))
    split = max(range(1, len(sx)), key=lambda k: sx[k][0] - sx[k - 1][0])      # the widest gap: between the eyes
    eyes = {"A": [pts[i] for _, i in sx[:split]], "B": [pts[i] for _, i in sx[split:]]}
    m = lab.look.flat("catchlight", lab.hx(color), 2.0)
    for side, ps in eyes.items():
        # the eye's on-screen middle (its bounding box, not the face average, which leans to the inner corner)
        v = [world_to_camera_view(sc, cam, p) for p in ps]
        mx, my = (min(q.x for q in v) + max(q.x for q in v)) / 2, (min(q.y for q in v) + max(q.y for q in v)) / 2
        c = min(ps, key=lambda p: (lambda q: (q.x - mx) ** 2 + (q.y - my) ** 2)(world_to_camera_view(sc, cam, p)))
        p = c + (camp - c).normalized() * 0.01 + Vector((0, 0, 0.004))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=4, radius=r, location=p)
        o = bpy.context.object
        o.name = f"catchlight_{side}"
        o.data.materials.append(m)
        o.visible_shadow = False
        o.hide_render = False
        o.keyframe_insert("hide_render", frame=1)
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=until)


def s03a():
    """Back three-quarter at the desk: the camera behind his right shoulder, his face turned to the tank."""
    h, sc = _lab()
    rig = _kai(h)
    n = LEN["S03a"] + TAIL
    tank = Vector(h["hero_tank"]["floor"])
    _sit(rig, lean=0.1, look=(0.35, 0.15))
    _key_pose(rig, 1, BODY)
    _sit(rig, lean=0.2, look=(0.55, 0.22))         # he leans in toward the tank (on 3s: a held pose change)
    _key_pose(rig, 22, BODY)
    head = _head_pos(rig)
    _cam("cam_s03a", (-0.5, 0.62, 1.42), (-0.98, 2.05, 1.06), 30, focus=head, fstop=1.6)
    _face_light("s03a_tank_on_face", tuple(tank + Vector((-0.2, -0.3, 0.25))), tuple(head), 1.6, size=0.15)
    _tint_hero(0.12)
    hero.face(rig, "neutral", 1)
    hero.face(rig, "blink", 31)
    hero.face(rig, "neutral", 34)
    return dict(frames=n, step=1, subject=[rig["arm"]])


def s03b():
    """Close on his face from the tank side, lit cyan; neutral -> a small fond smile."""
    h, sc = _lab()
    rig = _kai(h)
    n = LEN["S03b"] + TAIL
    _sit(rig, lean=0.22, look=(0.6, 0.02))          # head level, so the cap's brim leaves his eyes clear
    _key_pose(rig, 1, BODY)
    head = _head_pos(rig)
    tank = Vector(h["hero_tank"]["floor"])
    # from the tank, a little below his eyes (the cap's brim must not hide them), looking slightly up at his face
    glass_y = h["hero_tank"]["glass"].location.y
    cam_loc = Vector((tank.x - 0.05, glass_y - 0.06, head.z - 0.035))     # just in front of the glass
    cam = _cam("cam_s03b", tuple(cam_loc), tuple(head + Vector((0, 0, -0.035))), 40, fstop=1.4)
    _focus_face(cam, rig)
    # from the tank on his right only, so his left cheek falls into the cool shadow tone
    _face_light("s03b_tank_on_face", tuple(Vector((head.x + 0.35, head.y + 0.2, head.z - 0.02))), tuple(head), 0.9,
                size=0.12)
    # v3 (coordinator): warm skin, not green. The tank's cyan only as coloured light over the lit side (~1/3 mix), the
    # shadow side in the skin's own lavender shadow tone, a thin cyan rim on the jaw nearest the tank, catchlights.
    _tank_glow(side=Vector((1.0, 0.0, 0.0)))
    _catchlights(rig, cam, until=22)
    hero.line_width(rig, 0.0015)                     # face close-up: ~2-3 px lines
    hero.face(rig, "neutral", 1)
    hero.face(rig, "look_right", 1, 0.4)
    hero.face(rig, "relaxed", 19, 0.7)               # the fond smile in two steps (SG2): the eyes soften...
    hero.face(rig, "happy", 22, 1.0)                 # ...then the smile ("...and the pistol shrimp")
    return dict(frames=n, step=3, subject=[rig["arm"]])


def s05b():
    """The flash fades on his face; then one finger taps the glass."""
    h, sc = _lab()
    rig = _kai(h)
    n = LEN["S05b"] + TAIL
    tank = h["hero_tank"]
    glass_y = tank["glass"].location.y
    fx, fy, fz = tank["floor"]
    tap = Vector((fx - 0.17, glass_y - 0.01, fz + 0.1))
    _sit(rig, lean=0.24, look=(0.6, 0.2))
    _key_pose(rig, 1, BODY)
    _key_pose(rig, 18, BODY)
    _sit(rig, lean=0.26, look=(0.62, 0.22), right_reach=tap + Vector((0.02, -0.07, 0.03)))   # the finger rises
    _key_pose(rig, 24, BODY)
    _sit(rig, lean=0.27, look=(0.62, 0.22), right_reach=tap)                                 # tap
    _key_pose(rig, 30, BODY)
    _sit(rig, lean=0.26, look=(0.62, 0.22), right_reach=tap + Vector((0.0, -0.03, 0.0)))      # off the glass
    _key_pose(rig, 32, BODY)
    _sit(rig, lean=0.27, look=(0.62, 0.22), right_reach=tap)                                 # and a second soft tap
    _key_pose(rig, 34, BODY)
    head = _head_pos(rig)
    # from his right, a little in front: his face on the left, his finger on the glowing tank glass on the right
    cam = _cam("cam_s05b", (-0.3, 1.32, 1.12), tuple(head.lerp(tap, 0.5) + Vector((0, 0, 0.02))), 28, fstop=1.6)
    _focus_face(cam, rig)
    # the bubble's flash on his face, fading on 1s (from S05a's collapse), then the tank's steady cyan
    fl = _face_light("s05b_flash", (fx - 0.12, glass_y - 0.05, fz + 0.12), tuple(head), 0, "#e8fbff", 0.15)
    for f, e in ((1, 8), (2, 6), (4, 4), (7, 2), (11, 1), (16, 0.3), (20, 0)):
        fl.data.energy = e
        fl.data.keyframe_insert("energy", frame=f)
    _face_light("s05b_tank_on_face", (head.x + 0.35, head.y + 0.2, head.z - 0.02), tuple(head), 0.9, size=0.12)
    _tint_hero(0.1)
    hero.line_width(rig, 0.002)
    hero.face(rig, "surprised", 1, 0.7)               # eyes still wide from the flash
    hero.face(rig, "neutral", 13)
    hero.face(rig, "relaxed", 25, 0.5)
    hero.face(rig, "happy", 31, 0.7)                  # the tap lands: a small smile
    return dict(frames=n, step=1, subject=[rig["arm"]])


SHOTS = {"S03a": s03a, "S03b": s03b, "S05b": s05b}
