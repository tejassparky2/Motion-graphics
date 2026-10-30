"""Build the knuckle-cracking explainer scene and save it as a .blend.

blender -b -P explainer/knuckles/build.py -- --out knuckles.blend
"""
import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))                                  # explainer/ (xb)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'pelican'))  # pelican/ (pb)
sys.path.insert(0, HERE)

import bpy  # noqa: E402

from pb import util  # noqa: E402
from xb import character, posing, render, room, xray  # noqa: E402
import joint  # noqa: E402
import perform  # noqa: E402
import shots  # noqa: E402
from xb import anim  # noqa: E402

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--out', default='/tmp/knuckles.blend')
ap.add_argument('--samples', type=int, default=8)
args = ap.parse_args(argv)

t0 = time.time()
util.clear_scene()
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = round(shots.DURATION * shots.FPS)

set_coll = util.collection("Room")
lights = room.build(set_coll)
hero_coll = util.collection("Hero")
body, rig = character.make_human(
    phenotype=dict(gender=1.0, age=0.5, muscle=0.6, weight=0.48, height=0.55,
                   race=dict(caucasian=0.8, asian=0.1, african=0.1)),
    clothes=("male_casualsuit06/male_casualsuit06.mhclo",))
for ob in [rig] + list(rig.children):
    for c in ob.users_collection:
        c.objects.unlink(ob)
    hero_coll.objects.link(ob)
character.restyle_clothes(rig, (0.035, 0.09, 0.26))
print(f"set + character {time.time() - t0:.1f}s")

# ---- x-ray hand (built in the rest pose so the bones bind to the rig) ----
xray_coll = util.collection("Xray")
bones, glow_mat = xray.build_hand_bones(rig, xray_coll, 'R')
for slot in body.material_slots:
    xray.apply_to_material(slot.material)

# ---- rig controls and performance ----
tR, pR = posing.setup_arm_ik(rig, 'R', hero_coll)
tL, pL = posing.setup_arm_ik(rig, 'L', hero_coll)
pR.location = (-0.7, 0.25, 0.9)
pL.location = (0.7, 0.25, 0.9)
look = posing.add_eye_tracking(rig, hero_coll, (0, -1.0, 1.6))
cam_coll = util.collection("Cameras")
cams = perform.cameras(cam_coll, scene)
JT = dict(start=shots.SHOTS[2][1], end=shots.SHOTS[2][2], pull=shots.PULL_T, pressure=shots.PRESSURE_T,
          bubble=shots.BUBBLE_T)
joint_coll = util.collection("Joint")
joint.build(joint_coll, JT)
cams['joint'] = joint.camera(cam_coll, JT)
perform.hands(rig, tR, tL)
perform.body(rig, look, cams)
face = anim.Face(body, [body] + list(rig.children))
perform.face(face)
perform.focus(cams, rig)
for name, t0_, t1_ in shots.SHOTS:
    if name in cams:
        m = scene.timeline_markers.new(name, frame=shots.frame(t0_))
        m.camera = cams[name]
scene.camera = cams['crack']

f = shots.frame
x0, x1 = shots.XRAY_T
xray.key_amount([(f(x0), 0.0), (f(x1), 1.0), (f(5.75) - 1, 1.0), (f(5.75), 0.0)])
xray.key_visibility(bones, f(x0))
for ob in bones:
    ob.hide_render = True
    ob.keyframe_insert('hide_render', frame=f(5.75))
glow = glow_mat.node_tree.nodes['Glow'].outputs[0]
for t, v in ((0.0, 0.0), (shots.FLUID_T - 0.1, 0.0), (shots.FLUID_T + 0.25, 1.0), (5.75, 0.75)):
    glow.default_value = v
    glow.keyframe_insert('default_value', frame=f(t))
bd, bd_amt = xray.backdrop(cams['xray'], xray_coll)
for t, hide in ((0.0, True), (shots.XRAY_T[0], False), (5.75, True)):
    bd.hide_render = hide
    bd.keyframe_insert('hide_render', frame=f(t))
for t, v in ((0.0, 0.0), (x0 + 0.1, 0.0), (x1, 1.0)):
    bd_amt.outputs[0].default_value = v
    bd_amt.outputs[0].keyframe_insert('default_value', frame=f(t))
print(f"performance {time.time() - t0:.1f}s")

# screen position of the index knuckle at the end of the x-ray shot (for the zoom transition in post)
import json  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
scene.frame_set(shots.frame(shots.SHOTS[1][2]) - 1)
dg = bpy.context.evaluated_depsgraph_get()
rig_e = rig.evaluated_get(dg)
pb = rig_e.pose.bones['finger2-1.R']
p = world_to_camera_view(scene, cams['xray'].evaluated_get(dg), rig_e.matrix_world @ pb.head)
json.dump({'zoom_center': [p.x, 1.0 - p.y]},
          open(os.path.abspath(args.out).replace('.blend', '_post.json'), 'w'))
scene.frame_set(1)

render.setup(scene, samples=args.samples)
render.world(scene)
render.cheap_emitters()
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.out), compress=True)
print("SAVED", args.out)
