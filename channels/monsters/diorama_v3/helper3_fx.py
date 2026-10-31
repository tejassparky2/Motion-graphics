"""Episode 1 v3 S09 (helper 3), 2D pass: the soul spark's comet trail, twinkles and landing (flash, a ring lying on
the meadow, a sparkle pop), drawn on the rendered frames along the 3D ball's own screen path (out/monsters/diorama_v3/
shots/S09_spark.json, written by helper3.s09). The 3D ball stays the spark itself (depth and blur); this only adds what
doesn't read at phone size. Same look as fx2d.soul_spark (its glow, star and colour).

    /home/user/tools/postenv/bin/python channels/monsters/diorama_v3/helper3_fx.py FRAMES_DIR [SPARK_JSON]

FRAMES_DIR holds 0001.png ... (frame 1 = the shot's first frame); the frames are drawn on in place.
"""
import json
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)

from channels.monsters import fx2d  # noqa: E402
from motion.engine import cairo  # noqa: E402

SIZE = 15            # spark size on a 720-wide frame (fx2d's default is 22; the 3D ball is the core)
TRAIL = 5.0          # frames of comet trail behind it
LAND = 11            # frames of the landing (0.45 s)


def _at(path, f):
    """The ball's screen point at (fractional) frame f, held at the two ends."""
    keys = sorted(int(k) for k in path)
    f = max(keys[0], min(keys[-1], f))
    a = int(math.floor(f))
    b = min(keys[-1], a + 1)
    u = f - a
    pa, pb = path[str(a)], path[str(b)]
    return pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u


def draw(cr, f, spark, k=1.0):
    path, (f0, f1) = spark["path"], spark["fall"]
    size = SIZE * k
    col, white = fx2d.SOUL, fx2d.WHITE
    if f0 - 1 <= f <= f1:                                     # flying: trail, twinkles, a halo round the ball
        steps = 18
        for i in range(steps, 0, -1):
            ff = f - TRAIL * i / steps
            if ff < f0:
                continue
            x, y = (c * k for c in _at(path, ff))
            q = 1 - i / steps
            fx2d._glow(cr, x, y, size * (0.6 + 1.6 * q), col, 0.24 * q)
            cr.set_source_rgba(1, 1, 1, 0.55 * q * q)
            cr.arc(x, y, size * 0.32 * q, 0, 2 * math.pi)
            cr.fill()
        rnd = random.Random(101 + f // 2 * 2)                 # twinkles on 2s
        for _ in range(4):
            ff = f - rnd.uniform(0.5, TRAIL * 1.4)
            if ff < f0:
                continue
            x, y = (c * k for c in _at(path, ff))
            life = 1 - (f - ff) / (TRAIL * 1.4)
            cr.set_source_rgba(*col[:3], 0.9 * life)
            fx2d._star4(cr, x + rnd.uniform(-18, 18) * k, y + rnd.uniform(-10, 10) * k, size * 0.5 * life + 3 * k,
                        rnd.uniform(0, 0.8))
            cr.fill()
        x, y = (c * k for c in _at(path, max(f, f0)))
        fx2d._glow(cr, x, y, size * 4.0, col, 0.45)
        fx2d._glow(cr, x, y, size * 1.6, white, 0.75)
    elif f1 < f <= f1 + LAND:                                 # landing: flash, a ring on the ground, sparkle pop
        u = (f - f1) / LAND
        x, y = (c * k for c in _at(path, f1))
        fx2d._glow(cr, x, y, size * (5 + 6 * u), white, (1 - u) * 0.9)
        cr.set_source_rgba(*col[:3], 1 - u)
        cr.set_line_width((4 * (1 - u) + 1) * k)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.35)
        cr.arc(0, 0, size * (1.5 + 7 * fx2d.ease_out(u)), 0, 2 * math.pi)
        cr.restore()
        cr.stroke()
        rnd = random.Random(10)
        for i in range(6):
            ang = i * math.pi / 3 + rnd.uniform(-0.3, 0.3)
            r = size * (1.2 + 4.5 * fx2d.ease_out(u))
            cr.set_source_rgba(1, 1, 1, 1 - u)
            fx2d._star4(cr, x + math.cos(ang) * r, y + math.sin(ang) * r * 0.6, size * 0.5 * (1 - u) + 2 * k, 0.3)
            cr.fill()


def main(frames_dir, spark_json):
    with open(spark_json) as fh:
        spark = json.load(fh)
    f0, f1 = spark["fall"]
    for f in range(f0 - 1, f1 + LAND + 1):
        p = os.path.join(frames_dir, f"{f:04d}.png")
        if not os.path.exists(p):
            continue
        surf = cairo.ImageSurface.create_from_png(p)
        cr = cairo.Context(surf)
        draw(cr, f, spark, surf.get_width() / 720)
        surf.flush()
        surf.write_to_png(p)
        print("fx", f)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else
         os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots", "S09_spark.json"))
