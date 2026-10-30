"""Stills and checks for mk/storm.py, timed like Episode 1: S07 (rain + lightning through a stand-in lab window, the
lamp flickers), S10 (black, then white) and S11 (the white opens in a star wipe onto the pastel sky).
    blender -b -P channels/monsters/test_storm.py -- OUT_DIR [SCALE]
Writes OUT_DIR/storm_rain.png, storm_whiteout.png, storm_wipe.png, storm_sky.png (720x1280 at SCALE 1) and asserts
that the power-out frame is black and the end of the white-out is white."""
import math
import os
import sys
import time

import bpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters.mk import look, storm  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
out = args[0]
scale = float(args[1]) if len(args) > 1 else 1.0
os.makedirs(out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(round(720 * scale), round(1280 * scale), 16)
look.world(sky="#2a3350", horizon="#3f4a68", fill="#3c4566", fill_strength=0.18)
look.sun(elev=30, azim=160, energy=0.7, color="#b9c6ff")
hx, P = look.hexc, look.paint


def box(name, loc, size, mat):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = [s / 2 for s in size]
    bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat)
    return o


# a dim lab wall with one window (opening x -1.1..1.1, z 0.9..2.9), a cross mullion and a sill
wall, frame = P("wall", hx("#353a52"), noise=0.1), P("frame", hx("#20233a"))
X0, X1, Z0, Z1 = -1.1, 1.1, 0.9, 2.9
box("wall_l", (-3.55, 0, 2), (4.9, 0.2, 4), wall)
box("wall_r", (3.55, 0, 2), (4.9, 0.2, 4), wall)
box("wall_b", (0, 0, Z0 / 2), (2.2, 0.2, Z0), wall)
box("wall_t", (0, 0, (Z1 + 4) / 2), (2.2, 0.2, 4 - Z1), wall)
box("wall_top", (0, 0, 5), (12, 0.2, 2), wall)
box("mull_v", (0, -0.02, 1.9), (0.08, 0.12, Z1 - Z0), frame)
box("mull_h", (0, -0.02, 1.9), (X1 - X0, 0.12, 0.08), frame)
box("sill", (0, -0.15, Z0 - 0.04), (2.5, 0.35, 0.08), frame)
box("floor", (0, -3, -0.05), (10, 8, 0.1), P("floor", hx("#3a3d52")))
# the stormy outside: a far painted backdrop with low dark hills
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 40, 6), rotation=(math.radians(90), 0, 0))
far = bpy.context.object
far.scale = (90, 40, 1)
far.data.materials.append(P("storm_sky", hx("#1c2238"), top=hx("#33405f"), noise=0.18, scale=3.0))
box("hills", (0, 30, -1.0), (80, 1, 4.0), P("hills", hx("#1f2740"), noise=0.1))

# the window object (in the real shots: helper 1's lab window) and the room lamp
bpy.ops.mesh.primitive_plane_add(size=1, location=((X0 + X1) / 2, 0, (Z0 + Z1) / 2), rotation=(math.radians(90), 0, 0))
window = bpy.context.object
window.name = "window_glass"
window.scale = (X1 - X0, Z1 - Z0, 1)
window.hide_render = True
bpy.ops.object.light_add(type="AREA", location=(0.3, -2.6, 3.8))
lamp = bpy.context.object
lamp.data.energy, lamp.data.size = 180, 1.2
lamp.data.color = hx("#ffe6c4")[:3]

bpy.ops.object.camera_add(location=(0.35, -4.2, 1.75), rotation=(math.radians(88), 0, math.radians(4)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 30
cam.keyframe_insert("rotation_euler", frame=79)
cam.keyframe_insert("location", frame=79)
cam.rotation_euler = (math.radians(104), 0, 0)   # S11: a new shot, far beyond the set, looking into open sky
cam.location = (0, 60, 10)
cam.keyframe_insert("rotation_euler", frame=80)
cam.keyframe_insert("location", frame=80)
for fc in cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []:
    for kp in fc.keyframe_points:
        kp.interpolation = "CONSTANT"
sc.frame_set(1)

print("WINDOW_RECT", ["%.3f" % v for v in storm.window_rect(cam, window)])
# S07, frames 1-33
storm.rain(cam, 1, 33, window=window, depth=6.0)
storm.lightning(cam, 9, window=window, lights=[lamp], depth=28.0)
storm.flicker([lamp], 14, 24)
# S10, frames 34-79: (lab spark ~37), lights out and black at 40, "And so did I." on black, white 63-77
storm.power_out(cam, 40, lights=[lamp])
storm.white_out(cam, 63, 77)
# S11, frames 80-101: the white opens from the sun in a star wipe
storm.birds_and_light(cam, 80, 93)


def render(frame, name):
    sc.frame_set(frame)
    sc.render.filepath = os.path.join(out, name)
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print("RENDER %s frame %d: %.1f s" % (name, frame, time.time() - t))
    img = bpy.data.images.load(sc.render.filepath, check_existing=False)
    px = img.pixels[:]
    mean = sum(px[i] + px[i + 1] + px[i + 2] for i in range(0, len(px), 4)) / (len(px) // 4 * 3)
    bpy.data.images.remove(img)
    print("MEAN %s %.3f" % (name, mean))
    return mean


render(10, "storm_rain.png")          # bolt on, the window light in the room, flash nearly gone
render(70, "storm_whiteout.png")      # half way: white glowing out from the centre
render(86, "storm_wipe.png")          # the star wipe opening from the sun
render(100, "storm_sky.png")          # open: pastel sky, sun, rays and birds
m_black = render(50, "_check_black.png")
m_white = render(78, "_check_white.png")
for f in ("_check_black.png", "_check_white.png"):
    os.remove(os.path.join(out, f))
assert m_black < 0.01, m_black
assert m_white > 0.99, m_white
print("STORM_TEST_OK")
