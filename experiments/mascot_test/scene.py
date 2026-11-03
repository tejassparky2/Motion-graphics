"""Render the quality test: a 4 s clip of the mascot on the photo floor, an expression sheet, a comparison image."""
import math
import subprocess
import sys

import cairo

sys.path.insert(0, "/home/user/Motion-graphics")
sys.path.insert(0, "/tmp/claude-0/-home-user-Motion-graphics/f748781f-9eab-54dc-8b55-eb2264278477/scratchpad/mascot")
import imageio_ffmpeg  # noqa: E402
from motion.engine import seg  # noqa: E402
from motion.polish import appear, bold_text, lin  # noqa: E402
from zib import reply, zib  # noqa: E402

D = "/tmp/claude-0/-home-user-Motion-graphics/f748781f-9eab-54dc-8b55-eb2264278477/scratchpad/mascot/"
W, H, FPS = 720, 1280, 30
bg = cairo.ImageSurface.create_from_png(D + "bg_25.2.png")


def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cr = cairo.Context(s)
    cr.save()
    cr.scale(W / bg.get_width(), H / bg.get_height())
    cr.set_source_surface(bg, 0, 0)
    cr.paint()
    cr.restore()
    # hop in at 0.4 s, land with a squash at 0.9 s, wave, blink at 2.2 s, look up at the reply
    hop = seg(t, 0.4, 0.9)
    yoff = -110 * math.sin(hop * math.pi) if 0 < hop < 1 else 0
    squash = (-0.6 * math.sin(hop * math.pi) if 0 < hop < 1 else 0) + 0.8 * math.exp(-12 * max(0, t - 0.9)) * (t > 0.9)
    land = t - 0.9
    ant = 0.9 * math.exp(-4 * land) * math.sin(14 * land) if land > 0 else 0.2 * math.sin(t * 3)
    blink = max(0.0, 1 - abs(t - 2.2) / 0.07) if abs(t - 2.2) < 0.07 else 0.0
    breathe = 0.04 * math.sin(t * 3.2)
    arms = ("wave", "down") if 1.2 < t < 2.6 else ("down", "down")
    zib(cr, t, 340, 1060 + yoff, 0.72, look=(0.25, -0.5 if t > 2.6 else 0.1), blink=blink,
        squash=squash + breathe, arms=arms, mouth="grin" if 1.2 < t < 2.6 else "smile", ant_lag=(ant, ant * 0.8),
        light=(0.6, -0.7))
    if t > 2.7:
        k = appear(t, 2.7, 0.3)
        cr.save()
        cr.translate(340, 720)
        cr.scale(k, k)
        reply(cr, 0, 0, "hi! i'm Zib", 46)
        cr.restore()
    if 0.15 < t < 2.6:
        bold_text(cr, "meet our own mascot", W / 2, 1150, 46, (1, 1, 1, 1), font="Kalam", ow=8, shadow=0.0)
    return s


def write_clip():
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-map_metadata", "-1", "-fflags", "+bitexact", D + "zib_test.mp4"], stdin=subprocess.PIPE)
    for f in range(int(4.0 * FPS)):
        p.stdin.write(bytes(frame(f / FPS).get_data()))
    p.stdin.close()
    p.wait()
    frame(3.2).write_to_png(D + "zib_still.png")


def sheet():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, 1440, 520)
    cr = cairo.Context(s)
    cr.rectangle(0, 0, 1440, 520)
    cr.set_source(lin(0, 0, 0, 520, [(0, (0.96, 0.94, 0.9, 1)), (1, (0.86, 0.82, 0.76, 1))]))
    cr.fill()
    looks = [("happy", "grin", ("up", "up"), "yay!"), ("open", "o", ("down", "down"), "wait what"),
             ("cry", "sad", ("down", "down"), "sorry..."), ("angry", "smile", ("hip", "hip"), "hmph")]
    for k, (mood, mouth, arms, txt) in enumerate(looks):
        x = 180 + k * 360
        zib(cr, 0.3, x, 470, 0.95, mood=mood, mouth=mouth, arms=arms, look=(0, 0.2))
        reply(cr, x, 70, txt, 38)
    s.write_to_png(D + "zib_expressions.png")


write_clip()
sheet()
print("ok")
