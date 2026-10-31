"""A slow 2D push-in on a delivered diorama shot (channels/monsters/DIORAMA_EP01.md), for locked shots whose acting is too
small to read at phone size: the frame eases from 1.0 to 1 + ZOOM toward a point (full-res pixels), on 1s, sub-pixel
(bicubic), then the same clean encode as every shot (crf 10, no encoder tags) and a new contact sheet.

    /home/user/.venv-main/bin/python channels/monsters/diorama/push2d.py S14 --at 360 631 --zoom 0.2
"""
import argparse
import os
import subprocess

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SHOTS = os.path.join(ROOT, "out", "monsters", "diorama", "shots")
W, H = 720, 1280
CLEAN = ["-map_metadata", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact", "-bsf:v", "filter_units=remove_types=6"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shot")
    ap.add_argument("--at", nargs=2, type=float, required=True, help="the point to push toward (x y, full-res px)")
    ap.add_argument("--zoom", type=float, default=0.2)
    a = ap.parse_args()
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    src = os.path.join(SHOTS, a.shot + ".mp4")
    raw = subprocess.run([ff, "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    n = len(frames)
    out = []
    for i, f in enumerate(frames):
        u = i / max(1, n - 1)
        z = 1 + a.zoom * u * u * (3 - 2 * u)                       # ease in and out
        x0 = min(max(a.at[0] - W / (2 * z), 0), W - W / z)         # the crop box stays inside the frame
        y0 = min(max(a.at[1] - H / (2 * z), 0), H - H / z)
        im = Image.fromarray(f).transform((W, H), Image.AFFINE, (1 / z, 0, x0, 0, 1 / z, y0), Image.BICUBIC)
        out.append(np.asarray(im))
    tmp = os.path.join(SHOTS, f"_{a.shot}_push.mp4")
    subprocess.run([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "24",
                    "-i", "-", "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", *CLEAN, tmp],
                   input=np.stack(out).tobytes(), check=True)
    subprocess.run([ff, "-y", "-v", "error", "-i", tmp, "-c", "copy", "-map_metadata", "-1", "-fflags", "+bitexact",
                    "-metadata:s:v", "handler_name=", "-movflags", "+faststart", src], check=True)
    os.remove(tmp)
    subprocess.run([ff, "-y", "-v", "error", "-i", src, "-vf", "select=not(mod(n\\,6)),scale=180:320,tile=7x2",
                    "-frames:v", "1", "-q:v", "3", os.path.join(SHOTS, a.shot + "_sheet.jpg")], check=True)
    print(f"{a.shot}: {n} frames pushed in {a.zoom:.0%} toward {a.at}")


if __name__ == "__main__":
    main()
