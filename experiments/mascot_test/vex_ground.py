"""Grounding test: put the flat Vex exactly where Grim stands in the reference's floor shot, with real grounding:
contact shadows under each boot, a soft occlusion pool, a flattened cast shadow from his own silhouette, a touch of
softening and the footage's grain. The reference's overlays are patched out with floor from the same rows."""
import math
import subprocess
import sys

import cairo
import numpy as np

sys.path.insert(0, "/home/user/Motion-graphics")
import imageio_ffmpeg  # noqa: E402
from motion.polish import appear, bold_text, rad  # noqa: E402

D = "/tmp/claude-0/-home-user-Motion-graphics/f748781f-9eab-54dc-8b55-eb2264278477/scratchpad/mascot/"
W, H, FPS = 720, 1280, 30


# ---- clean plate: copy floor from the same rows (same depth) over each overlay, with feathered edges
def clean_plate():
    src = cairo.ImageSurface.create_from_png(D + "floor_5.2.png")
    a = np.ndarray((H, W, 4), np.uint8, src.get_data(), strides=(src.get_stride(), 4, 1)).astype(np.float32)
    out = a.copy()
    patches = [((180, 478, 348, 740), -160), ((348, 595, 512, 748), 185), ((362, 475, 482, 555), 200),
               ((255, 780, 378, 862), 250), ((278, 912, 442, 1000), 250)]
    for (x0, y0, x1, y1), dx in patches:
        f = 18
        X0, Y0, X1, Y1 = x0 - f, y0 - f, x1 + f, y1 + f
        ys, xs = np.mgrid[Y0:Y1, X0:X1]
        m = np.minimum.reduce([(xs - X0) / f, (X1 - 1 - xs) / f, (ys - Y0) / f, (Y1 - 1 - ys) / f]).clip(0, 1)[..., None]
        out[Y0:Y1, X0:X1] = out[Y0:Y1, X0:X1] * (1 - m) + a[Y0:Y1, X0 + dx:X1 + dx] * m
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    np.ndarray((H, W, 4), np.uint8, s.get_data(), strides=(s.get_stride(), 4, 1))[:] = out.clip(0, 255).astype(np.uint8)
    s.mark_dirty()
    return s


PLATE = clean_plate()
vex = cairo.ImageSurface.create_from_png(D + "vex/vex2_front.png")
VW, VH = vex.get_width(), vex.get_height()
alpha = np.ndarray((VH, VW, 4), np.uint8, vex.get_data(), strides=(vex.get_stride(), 4, 1))[..., 3]
# each boot's sole: the opaque columns in the bottom rows, split at the gap between the boots
rows = alpha[VH - 70:VH - 8] > 40
cols = np.where(rows.any(0))[0]
gaps = np.where(np.diff(cols) > 6)[0]
BOOTS = [(cols[0], cols[gaps[0]]), (cols[gaps[0] + 1], cols[-1])] if len(gaps) else [(cols[0], cols[-1])]
SOLE = max(y for y in range(VH) if (alpha[y] > 40).any())
FOOT = ((cols[0] + cols[-1]) / 2, SOLE)
EYES = ((397, 570), (705, 590))
INK = (0.12, 0.05, 0.1, 1)


def silhouette(scale):
    """Vex's own shape in black, small, for a blurred cast shadow."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(VW * scale) + 2, int(VH * scale) + 2)
    c = cairo.Context(s)
    c.scale(scale, scale)
    c.set_source_rgba(0, 0, 0, 1)
    c.mask_surface(vex, 0, 0)
    return s


SIL = silhouette(1 / 10)


def blink_lids(cr, k):
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
        cr.rectangle(ex - 116, ey - 102, 232, 204 * k)
        cr.set_source_rgba(0.867, 0.796, 0.925, 1)
        cr.fill()
        cr.restore()
        if k > 0.85:
            cr.move_to(ex - 88, ey + 8)
            cr.curve_to(ex - 40, ey + 44, ex + 40, ey + 44, ex + 88, ey + 8)
            cr.set_source_rgba(*INK)
            cr.set_line_width(14)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()


def ground(cr, x, y, s, lift=0.0):
    """Shadows on the floor for a sprite whose feet are at (x, y); `lift` = height above the floor in px."""
    fade = 1 / (1 + lift / 60)
    # 1) cast shadow: his silhouette squashed flat onto the floor, leaning back-left (light from front-right)
    cr.save()
    cr.translate(x, y)
    cr.transform(cairo.Matrix(1, 0, 0.12, 0.2, 0, 0))       # flattened onto the floor, falling back and a little left
    cr.scale(s * 10, s * 10)
    cr.translate(-FOOT[0] / 10, -FOOT[1] / 10)
    cr.set_source_surface(SIL, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(0.16 * fade)
    cr.restore()
    # 2) occlusion pool under him
    w = (cols[-1] - cols[0]) * s
    for rx, ry, a in ((w * 0.75, w * 0.13, 0.22), (w * 0.5, w * 0.08, 0.3)):
        cr.save()
        cr.translate(x, y - 2)
        cr.scale(rx * (1 + lift / 200), ry * (1 + lift / 200))
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.set_source(rad(x, y - 2, rx, [(0, (0.08, 0.06, 0.05, a * fade)), (1, (0.08, 0.06, 0.05, 0))]))
        cr.fill()
    # 3) tight contact shadow under each boot sole
    if lift < 4:
        for b0, b1 in BOOTS:
            bx = x + ((b0 + b1) / 2 - FOOT[0]) * s
            bw = (b1 - b0) * s * 0.55
            cr.save()
            cr.translate(bx, y - 1)
            cr.scale(bw, bw * 0.22)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.set_source(rad(bx, y - 1, bw, [(0, (0.05, 0.03, 0.03, 0.55)), (1, (0.05, 0.03, 0.03, 0))]))
            cr.fill()


def sprite(cr, x, y, s, squash=0.0, blink=0.0):
    spr = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW, VH)
    c = cairo.Context(spr)
    c.set_source_surface(vex, 0, 0)
    c.paint()
    blink_lids(c, blink)
    c.set_operator(cairo.OPERATOR_ATOP)                      # a faint wash of the room's grey: same light as the floor
    c.set_source_rgba(0.55, 0.55, 0.56, 0.07)
    c.paint()
    soft = cairo.ImageSurface(cairo.FORMAT_ARGB32, VW + 8, VH + 8)   # ~0.6 px soft focus, like the phone footage
    c = cairo.Context(soft)
    c.set_operator(cairo.OPERATOR_ADD)
    for ox, oy in ((-3.5, 0), (3.5, 0), (0, -3.5), (0, 3.5)):
        c.set_source_surface(spr, 4 + ox, 4 + oy)
        c.paint_with_alpha(0.25)
    cr.save()
    cr.translate(x, y)
    cr.scale(s * (1 + 0.14 * squash), s * (1 - 0.16 * squash))
    cr.translate(-FOOT[0] - 4, -FOOT[1] - 4)
    cr.set_source_surface(soft, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


rng = np.random.default_rng(7)


def grain(sf):
    a = np.ndarray((H, W, 4), np.uint8, sf.get_data(), strides=(sf.get_stride(), 4, 1))
    n = rng.normal(0, 2.6, (H, W, 1)).astype(np.float32)
    a[..., :3] = (a[..., :3].astype(np.float32) + n).clip(0, 255).astype(np.uint8)
    sf.mark_dirty()


X, Y, S = 248, 706, 0.165        # Grim's spot and size in the reference shot


def frame(t, with_text=True):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cr = cairo.Context(sf)
    cr.set_source_surface(PLATE, 0, 0)
    cr.paint()
    land = 0.5
    fall = min(1.0, t / land)
    lift = 520 * (1 - fall) ** 2 if t < land else 0.0
    dt = t - land
    squash = -0.4 * (1 - fall) if t < land else 0.85 * math.exp(-9 * dt) * math.cos(16 * dt)
    breathe = 0.03 * math.sin(t * 3.4) if dt > 0.4 else 0
    blink = 0.0
    for bt in (1.6, 3.2):
        if abs(t - bt) < 0.09:
            blink = min(1.0, (1 - abs(t - bt) / 0.09) * 1.6)
    ground(cr, X, Y, S, lift)
    sprite(cr, X, Y - lift, S, squash + breathe, blink)
    if with_text and t > 2.0:
        k = appear(t, 2.0, 0.3)
        cr.save()
        cr.translate(X, 450)
        cr.scale(k, k)
        bold_text(cr, "i bite.", 0, 0, 44, (0.92, 0.12, 0.15, 1), font="Kalam", outline=(1, 1, 1, 1), ow=7, shadow=0)
        cr.restore()
    grain(sf)
    return sf


if __name__ == "__main__":
    frame(3.0, with_text=False).write_to_png(D + "vex/vex_ground_still.png")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-map_metadata", "-1", "-fflags", "+bitexact", D + "vex/vex_ground.mp4"], stdin=subprocess.PIPE)
    for f in range(int(3.8 * FPS)):
        p.stdin.write(bytes(frame(f / FPS).get_data()))
    p.stdin.close()
    p.wait()
    print("boots", BOOTS, "sole", SOLE, "foot", FOOT)
