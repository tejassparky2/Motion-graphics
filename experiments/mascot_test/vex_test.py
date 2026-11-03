"""Test: the owner's ChatGPT Vex image animated as a 2D sprite on a photo floor (drop-in, squash on landing, jelly
follow-through, breathing, blinks drawn over the eyes, a red reply line)."""
import math
import subprocess
import sys

import cairo

sys.path.insert(0, "/home/user/Motion-graphics")
import imageio_ffmpeg  # noqa: E402
from motion.polish import appear, bold_text, rad  # noqa: E402

D = "/tmp/claude-0/-home-user-Motion-graphics/f748781f-9eab-54dc-8b55-eb2264278477/scratchpad/mascot/"
W, H, FPS = 720, 1280, 30
bg = cairo.ImageSurface.create_from_png(D + "bg_25.2.png")
vex = cairo.ImageSurface.create_from_png(D + "vex/vex2_front.png")   # the flat 2D version
VW, VH = vex.get_width(), vex.get_height()
FOOT = (545, 1348)                     # boots' contact point in the image
EYES = ((397, 570), (705, 590))        # eye centres in the image
INK = (0.12, 0.05, 0.1, 1)


def shadow(cr, x, y, w, k=1.0):
    for rx, ry, a in ((w * 1.2, w * 0.2, 0.25), (w * 0.85, w * 0.13, 0.32), (w * 0.5, w * 0.08, 0.45)):
        cr.save()
        cr.translate(x, y)
        cr.scale(rx * k, ry * k)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y, rx * k, [(0, (0.1, 0.07, 0.05, a)), (1, (0.1, 0.07, 0.05, 0))]))
        cr.fill()


def blink_lids(cr, k):
    """Eyelids over both eyes (image coordinates), k = 0 open .. 1 shut."""
    if k <= 0:
        return
    for ex, ey in EYES:
        cr.save()
        cr.translate(ex, ey)
        cr.scale(110, 98)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.save()
        cr.clip()
        top = ey - 102
        cr.rectangle(ex - 116, top, 232, 204 * k)
        cr.set_source_rgba(0.867, 0.796, 0.925, 1)                      # flat skin, like the drawing
        cr.fill()
        cr.restore()
        if k > 0.85:                   # the closed eye: a soft curved lash line
            cr.move_to(ex - 92, ey + 8)
            cr.curve_to(ex - 40, ey + 46, ex + 40, ey + 46, ex + 92, ey + 8)
            cr.set_source_rgba(*INK)
            cr.set_line_width(14)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()


def draw_vex(cr, t, x, y, s, squash, wobble, blink):
    """Sprite with feet at (x, y). squash > 0 = wide and short. wobble = sideways jelly offset at the top (px)."""
    # build the wobbled sprite at the image's own size (pixel-aligned slices: no seams), then scale it once
    pad = 60
    spr = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW + 2 * pad, VH)
    c = cairo.Context(spr)
    if abs(wobble) < 0.3:
        c.set_source_surface(vex, pad, 0)
        c.paint()
    else:
        for y0 in range(0, VH, 4):     # jelly follow-through: the top lags behind, the boots stay planted
            c.save()
            c.rectangle(0, y0, VW + 2 * pad, 4)
            c.clip()
            c.set_source_surface(vex, pad + round(wobble * (1 - y0 / VH) ** 1.6), 0)
            c.paint()
            c.restore()
    c.translate(pad + wobble * 0.62, 0)  # eyes sit about a third of the way down
    blink_lids(c, blink)
    cr.save()
    cr.translate(x, y)
    cr.scale(s * (1 + 0.14 * squash), s * (1 - 0.16 * squash))
    cr.translate(-FOOT[0] - pad, -FOOT[1])
    cr.set_source_surface(spr, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


def frame(t):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cr = cairo.Context(sf)
    cr.save()
    cr.scale(W / bg.get_width(), H / bg.get_height())
    cr.set_source_surface(bg, 0, 0)
    cr.paint()
    cr.restore()
    land = 0.55
    fall = min(1.0, t / land)
    yoff = -700 * (1 - fall) ** 2 if t < land else 0
    dt = t - land
    squash = (-0.5 * (1 - fall) if t < land else 0.9 * math.exp(-9 * dt) * math.cos(16 * dt))
    wobble = 26 * math.exp(-5 * dt) * math.sin(18 * dt) if dt > 0 else 0
    breathe = 0.035 * math.sin(t * 3.4) if dt > 0.4 else 0
    if 2.4 < t < 3.2:                  # a little gloating sway while it talks
        wobble += 10 * math.sin((t - 2.4) * 9)
    blink = 0.0
    for bt in (1.7, 3.45):
        if abs(t - bt) < 0.09:
            blink = 1 - abs(t - bt) / 0.09
    shadow(cr, 350, 1062, 80, 1 - 0.5 * (1 - fall) if t < land else 1 + 0.15 * max(0, squash))
    draw_vex(cr, t, 350, 1060 + yoff, 0.21, squash + breathe, wobble, min(1, blink * 1.6))
    if t > 2.3:
        k = appear(t, 2.3, 0.3)
        cr.save()
        cr.translate(350, 720)
        cr.scale(k, k)
        bold_text(cr, "i bite.", 0, 0, 52, (0.92, 0.12, 0.15, 1), font="Kalam", outline=(1, 1, 1, 1), ow=8, shadow=0)
        cr.restore()
    return sf


ff = imageio_ffmpeg.get_ffmpeg_exe()
p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r",
                      str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-map_metadata",
                      "-1", "-fflags", "+bitexact", D + "vex/vex2_test.mp4"], stdin=subprocess.PIPE)
for f in range(int(4.2 * FPS)):
    p.stdin.write(bytes(frame(f / FPS).get_data()))
p.stdin.close()
p.wait()
for name, tt in (("still", 3.0), ("blink", 1.7), ("land", 0.6)):
    frame(tt).write_to_png(D + f"vex/vex2_{name}.png")
print("ok")
