"""Render one WW2 Episode 1 package to a clip, or a still / contact sheet for review.

    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P3                 # P3_f00000-00599.mp4, P3_f00600-...
    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P3 --frames 0-599  # one range only (re-renders, splits)
    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P3 --still 230.5   # one PNG at episode time 230.5 s
    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P3 --sheet         # 1 frame per 2 s -> P3_sheet.jpg

A package module channels/ww2/ep01/p3.py exposes draw(cr, t) with t in EPISODE seconds (inside package_span("P3"))
and cues(T) -> [(episode_time, sfx_name, gain_db, pan)] for the mix. Frame numbers in --frames count from the
package's first frame. Picture only; sound is mixed later from cues() and narration.wav.
"""
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)
from channels.ww2.ep01.timing import Timing, package_span  # noqa: E402
from channels.ww2.kit import core  # noqa: E402

OUT = os.path.join(ROOT, "out", "ww2", "ep01", "parts")
CHUNK = 600       # frames per piece (25 s): keeps every file under GitHub's 100 MB limit at crf 18
CRF = 18          # visually clean on the poster look; YouTube re-encodes anyway


def main():
    name = sys.argv[1].upper()
    T = Timing()
    a, b = package_span(name, T)
    mod = importlib.import_module(f"channels.ww2.ep01.{name.lower()}")
    os.makedirs(OUT, exist_ok=True)
    if "--still" in sys.argv:
        t = float(sys.argv[sys.argv.index("--still") + 1])
        out = os.path.join(OUT, f"{name}_t{t:07.2f}.png")
        core.render_clip(mod.draw, 0, out, still=t)
        print(out)
        return
    if "--sheet" in sys.argv:
        import cairo
        times = [a + 0.5 + 2 * k for k in range(int((b - a - 0.5) // 2) + 1)]
        cols, tw = 8, 480
        th = tw * core.H // core.W
        rows = (len(times) + cols - 1) // cols
        sheet = cairo.ImageSurface(cairo.FORMAT_RGB24, cols * tw, rows * th)
        sc = cairo.Context(sheet)
        frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, core.W, core.H)
        for k, t in enumerate(times):
            cr = cairo.Context(frame)
            mod.draw(cr, t)
            sc.save()
            sc.translate((k % cols) * tw, (k // cols) * th)
            sc.scale(tw / core.W, th / core.H)
            sc.set_source_surface(frame, 0, 0)
            sc.paint()
            sc.restore()
            core.text(sc, f"{t:.1f}", (k % cols) * tw + 8, (k // cols) * th + 26, 22, color="alert", align="left")
        png = os.path.join(OUT, f"{name}_sheet.png")
        sheet.write_to_png(png)
        print(png)
        return
    n = round((b - a) * T.fps)

    def draw(cr, t_local):
        mod.draw(cr, a + t_local)

    if "--frames" in sys.argv:
        f0, f1 = map(int, sys.argv[sys.argv.index("--frames") + 1].split("-"))
        ranges = [(f0, min(f1, n - 1))]
    else:                                    # default: CHUNK-frame pieces, each well under GitHub's 100 MB limit
        ranges = [(k, min(k + CHUNK - 1, n - 1)) for k in range(0, n, CHUNK)]
    for f0, f1 in ranges:
        out = os.path.join(OUT, f"{name}_f{f0:05d}-{f1:05d}.mp4")
        core.render_clip(draw, (b - a), out, frames=(f0, f1), crf=CRF)
        mb = os.path.getsize(out) / 1e6
        print(out, f"{f1 - f0 + 1} frames, {mb:.1f} MB")
        if mb > 95:
            print(f"  WARNING: {mb:.0f} MB > 95 MB; re-render this range in two halves with --frames")


if __name__ == "__main__":
    main()
