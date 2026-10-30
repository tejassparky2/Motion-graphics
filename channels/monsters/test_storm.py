"""Stills and checks for mk/storm.py: rain + lightning through a simple window, the power cut, the white-out and the
pastel sky reveal.
    blender -b -P channels/monsters/test_storm.py -- OUT_DIR [SCALE]
Writes OUT_DIR/storm_rain.png, storm_whiteout.png, storm_sky.png (720x1280 at SCALE 1) and asserts that the power-out
frame is black and the end of the white-out is white."""
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

bpy.ops.object.camera_add(location=(0.35, -4.2, 1.75), rotation=(math.radians(88), 0, math.radians(4)))
cam = bpy.context.object
sc.camera = cam
cam.data.lens = 30

win = storm.screen_rect(cam, [(X0, 0, Z0), (X1, 0, Z0), (X0, 0, Z1), (X1, 0, Z1)])
print("WINDOW_RECT", ["%.3f" % v for v in win])
storm.rain(cam, 1, 60, area=win, depth=6.0)
storm.lightning(cam, 20, area=win, depth=28.0)
storm.power_out(cam, 64)
storm.white_out(cam, 72, 120)
storm.birds_and_light(cam, 124, 160)


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


render(21, "storm_rain.png")          # bolt on, flash nearly gone: rain and lightning through the window
render(100, "storm_whiteout.png")     # half way: white glowing out from the centre
render(150, "storm_sky.png")          # the veil is gone: pastel sky, rays and birds
m_black = render(66, "_check_black.png")
m_white = render(121, "_check_white.png")
for f in ("_check_black.png", "_check_white.png"):
    os.remove(os.path.join(out, f))
assert m_black < 0.01, m_black
assert m_white > 0.99, m_white
print("STORM_TEST_OK")
