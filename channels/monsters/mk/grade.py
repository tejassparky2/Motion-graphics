"""Q3, the v3 light and grade pass for the diorama (channels/monsters/DIORAMA_EP01_V3.md): run once after a shot
builder (render_shot.py calls finish() for diorama_v3, or for any episode with DIORAMA_LOOK=v2; DIORAMA_LOOK=v1 turns
it off for a before/after). Nothing in the builders changes.

    finish(info)   info = the builder's dict; its `subject` roots tell us which objects are characters

What it adds on top of diorama.setup() and the sets' own lights:
- The view: Standard by default (tested 31 Oct: AgX, even Punchy with +0.6 exposure and extra saturation, greys the
  painted whites and muddies the pinks and greens); DIORAMA_AGX=1 switches to AgX Punchy for comparison.
- Screen-space AO and bounce (EEVEE horizon scan): contact darkening where things meet the ground or each other.
- Island: a cool, shadowless fill sun opposite the warm key sun, so the shadow side reads blue, not grey.
- A character-only rim light (light linking): a sun from behind the characters, relative to the camera, warm on the
  island, cyan in the lab (the tank's colour), so Kai, the shrimp and the bird separate from the ground.
- The per-scene grade (compositor, after the haze and bloom): lift/gamma/gain split-toning (night lab: teal shadows,
  cool highlights; day island: cool shadows, warm highlights), a little saturation, a soft vignette.
"""
import math
import os

import bpy
from mathutils import Vector

from channels.monsters.mk import look

LOOKS = {
    "lab": dict(lift=(0.99, 1.0, 1.015), gamma=(1.0, 1.0, 1.0), gain=(1.03, 1.01, 1.0), sat=1.04, vignette=0.2,
                rim="#a8f0ff", rim_energy=2.2, exposure=0.3),
    "island": dict(lift=(0.98, 0.99, 1.045), gamma=(1.0, 1.0, 0.99), gain=(1.05, 1.01, 0.95), sat=1.05,
                   vignette=0.26, rim="#fff0cf", rim_energy=2.6, exposure=0.15, fill="#a9c8ff", fill_energy=0.9),
}


ON_BY_DEFAULT = True           # approved for diorama_v3 (coordinator, 31 Oct 13:20 UTC): lab only, see ISLAND below
# The island before/after (S18 f31) came out greyer and hazier, with a pale ghost over Kai's face and a blob at the pond
# edge, while v1's island already reads clean and bright, so island scenes keep the v1 look unless DIORAMA_ISLAND_Q3=1.
ISLAND = os.environ.get("DIORAMA_ISLAND_Q3") == "1"


def enabled(ep):
    v = os.environ.get("DIORAMA_LOOK", "")
    return v == "v2" or (ON_BY_DEFAULT and ep.startswith("diorama_v3") and v != "v1")


def scene_kind():
    return "lab" if "dl_floor" in bpy.data.objects else "island"


def _characters(info):
    objs = set()
    for r in info.get("subject") or []:
        if r is None:
            continue
        objs.add(r)
        objs.update(r.children_recursive)
    return [o for o in objs if o.type in {"MESH", "CURVE", "SURFACE", "META", "FONT", "GPENCIL"}]


def _sun(name, travel, energy, color, shadow):
    """A sun whose light travels along `travel`."""
    ld = bpy.data.lights.new(name, "SUN")
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = (-Vector(travel)).to_track_quat("Z", "Y").to_euler()
    ld.energy, ld.color, ld.use_shadow = energy, look.hexc(color)[:3], shadow
    ld.angle = math.radians(8)
    if hasattr(ld, "specular_factor"):
        ld.specular_factor = 0.0                                # no sun disc on glossy props (the tank hood)
    return o


def _view(sc, exposure):
    vs = sc.view_settings
    if os.environ.get("DIORAMA_AGX") != "1":
        return
    try:
        vs.view_transform = "AgX"
        vs.look = "AgX - Punchy"
    except TypeError:
        return
    vs.exposure = exposure


def _render(sc):
    ee = sc.eevee
    # AO only: screen-space ray tracing / fast GI mirror bright screens into glossy props (a ghost disc on the tank
    # hood) and cost ~20 %, for little visible gain in a painted look
    for attr, val in (("use_raytracing", False), ("use_fast_gi", False), ("use_gtao", True), ("gtao_distance", 2.5)):
        if hasattr(ee, attr):
            try:
                setattr(ee, attr, val)
            except TypeError:
                pass


def _rim(sc, chars, color, energy):
    cam = sc.camera
    if cam is None or not chars:
        return None
    fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
    h = Vector((fwd.x, fwd.y, 0))
    h = h.normalized() if h.length > 1e-4 else Vector((0, 1, 0))
    e = math.radians(12)                                                # grazing, so it shows on top-down shots too
    travel = -h * math.cos(e) + Vector((0, 0, -math.sin(e)))            # from behind the subject toward the lens
    side = h.cross(Vector((0, 0, 1))).normalized()
    rim = _sun("q3_rim", travel + side * 0.35, energy, color, False)
    coll = bpy.data.collections.new("q3_rim_receivers")
    for o in chars:
        coll.objects.link(o)
    rim.light_linking.receiver_collection = coll
    return rim


def _grade(sc, g):
    nt = sc.node_tree
    comp = next((n for n in nt.nodes if n.bl_idname == "CompositorNodeComposite"), None)
    if comp is None or not comp.inputs[0].links:
        return
    src = comp.inputs[0].links[0].from_socket
    cb = nt.nodes.new("CompositorNodeColorBalance")
    cb.correction_method = "LIFT_GAMMA_GAIN"
    cb.lift, cb.gamma, cb.gain = g["lift"], g["gamma"], g["gain"]
    nt.links.new(src, cb.inputs[1])
    hs = nt.nodes.new("CompositorNodeHueSat")
    nt.links.new(cb.outputs[0], hs.inputs["Image"])
    for name in ("Saturation",):
        if name in hs.inputs:
            hs.inputs[name].default_value = g["sat"]
    if hasattr(hs, "color_saturation"):
        hs.color_saturation = g["sat"]
    out = hs.outputs[0]
    if g["vignette"] > 0:                                                # a soft elliptical vignette
        el = nt.nodes.new("CompositorNodeEllipseMask")
        for a, v in (("width", 0.95), ("height", 0.85)):
            if hasattr(el, a):
                setattr(el, a, v)
            elif a.capitalize() in el.inputs:
                el.inputs[a.capitalize()].default_value = v
        bl = nt.nodes.new("CompositorNodeBlur")
        bl.filter_type = "GAUSS"
        if hasattr(bl, "use_relative"):
            bl.use_relative = True
            bl.factor_x = bl.factor_y = 30.0
        else:
            bl.size_x = bl.size_y = int(0.3 * sc.render.resolution_x)
        nt.links.new(el.outputs[0], bl.inputs[0])
        inv = nt.nodes.new("CompositorNodeMath")
        inv.operation = "MULTIPLY_ADD"
        inv.inputs[1].default_value = g["vignette"]
        inv.inputs[2].default_value = 1.0 - g["vignette"]
        nt.links.new(bl.outputs[0], inv.inputs[0])
        mul = nt.nodes.new("CompositorNodeMixRGB")
        mul.blend_type = "MULTIPLY"
        mul.inputs[0].default_value = 1.0
        nt.links.new(out, mul.inputs[1])
        nt.links.new(inv.outputs[0], mul.inputs[2])
        out = mul.outputs[0]
    nt.links.new(out, comp.inputs[0])


def finish(info):
    sc = bpy.context.scene
    kind = scene_kind()
    if kind == "island" and not ISLAND and os.environ.get("DIORAMA_LOOK") != "v2":
        return "island (v1 look kept)"
    g = LOOKS[kind]
    _view(sc, g["exposure"])
    _render(sc)
    if kind == "island":
        key = next((o for o in sc.objects if o.type == "LIGHT" and o.data.type == "SUN"), None)
        if key is not None:
            d = key.matrix_world.to_3x3() @ Vector((0, 0, -1))
            _sun("q3_fill", (-d.x, -d.y, d.z * 0.6), g["fill_energy"], g["fill"], False)
    _rim(sc, _characters(info), g["rim"], g["rim_energy"])
    if sc.use_nodes and sc.node_tree:
        _grade(sc, g)
    return kind
