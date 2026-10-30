"""Episode 1 shot builders (see channels/monsters/EP01_SHOTS.md). Each builds its scene from scratch and returns
dict(frames=N, subject=[roots for the subject pass]). Render with channels/monsters/render_shot.py."""
import math

import bpy

from ..mk import anim, look, meadow, puffshrimp

FPS = 24


def _camera(loc, aim, lens=40, focus=None, fstop=0.16):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object
    d = [aim[i] - loc[i] for i in range(3)]
    cam.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    cam.data.lens = lens
    if focus is not None:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_object = focus
        cam.data.dof.aperture_fstop = fstop
    bpy.context.scene.camera = cam
    return cam


def _push(cam, f0, f1, dist):
    """The slow push-in every shot gets (camera on 1s, linear)."""
    fwd = cam.matrix_world.to_3x3() @ __import__("mathutils").Vector((0, 0, -1))
    a = cam.location.copy()
    anim.key(cam, "location", f0, a, "LINEAR")
    anim.key(cam, "location", f1, a + fwd * dist, "LINEAR")


def _claw_tip(rig):
    """World position just under the claw's fingers, for drips."""
    bpy.context.view_layer.update()
    arm = bpy.data.objects[rig["shoulder"].name.replace("shoulder", "claw")]
    coral = [i for i, m in enumerate(arm.data.materials) if m and m.name.endswith("_coral")]
    vs = {v for p in arm.data.polygons if p.material_index in coral for v in p.vertices}
    lo = min((arm.matrix_world @ arm.data.vertices[i].co for i in vs), key=lambda v: v.z)   # bottom of the claw
    print("CLAW_TIP", tuple(round(c, 2) for c in lo))
    return (lo.x, lo.y, lo.z - 0.05)


def _crater_scene(frames):
    set_ = meadow.build("after")
    rig = puffshrimp.build((0, 0, 0))
    meadow.smoke(set_["smoke_sources"], -40, frames + 10)
    meadow.smoke(set_["rim_smoke"], -40, frames + 10, every=14, rise=1.6, size=0.3, seed=4)
    return set_, rig


def s01():
    """Flash-forward hook: the puff-shrimp in the smoking crater, claw raised, eyes half-shut (smug); sliced glowing
    stumps where the forest stood. Low camera, slow push-in."""
    n = 64
    set_, rig = _crater_scene(n)
    rig["root"].rotation_euler = (0, 0, -0.4)                  # 3/4, looking off; it turns to us in S18
    rig["shoulder"].rotation_euler = (0.1, 0.55, 0.0)
    anim.lids(rig, 1, 0.5)
    anim.idle(rig, 1, n, period=30, amount=0.03, seed=3)
    anim.key(rig["hinge"], "rotation_euler", 1, (-0.25, 0, 0), "CONSTANT")     # the claw still shut from the snap
    anim.on_twos([rig["body"], *rig["eyes"], *rig["lids"], *rig["hi"], *rig["antennae"], rig["shoulder"], rig["hinge"]])
    tip = _claw_tip(rig)
    meadow.drips(tip, -6, n, every=16, fall=tip[2] - 0.04)
    cam = _camera((0.5, -7.0, 1.45), (-0.1, 2.0, 1.95), lens=34, focus=rig["body"], fstop=0.45)
    _push(cam, 1, n, 0.6)
    return dict(frames=n, subject=[rig["root"]])


SHOTS = dict(S01=s01)
