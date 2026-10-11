"""Cut-out masks for a clip (figurine + base) with BiRefNet, on every Nth frame at 30 fps.

  python tools/bgswap_masks.py clip.mp4 OUT_DIR [--every 2] [--start 0] [--dur 0]

Writes OUT_DIR/frame_00000.png (the 1080x1920 frame) for every frame and OUT_DIR/mask_00000.png for every Nth one.
tools/bgswap.py fills the in-between masks by optical flow and composites the new background.
"""
import argparse
import os
import subprocess

from PIL import Image
from rembg import new_session, remove

W, H, FPS = 1080, 1920, 30

ap = argparse.ArgumentParser()
ap.add_argument("clip")
ap.add_argument("out")
ap.add_argument("--every", type=int, default=2)
ap.add_argument("--start", type=float, default=0)
ap.add_argument("--dur", type=float, default=0)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
cmd = ["ffmpeg", "-v", "error", "-ss", str(a.start), "-i", a.clip]
if a.dur:
    cmd += ["-t", str(a.dur)]
p = subprocess.Popen(cmd + ["-vf", f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
frames = []
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    frames.append(Image.frombytes("RGB", (W, H), buf))
for i, f in enumerate(frames):
    f.save(os.path.join(a.out, f"frame_{i:05d}.png"))
keys = list(range(0, len(frames), a.every))
if keys[-1] != len(frames) - 1:
    keys.append(len(frames) - 1)
s = new_session("birefnet-general-lite")
for n, i in enumerate(keys):
    path = os.path.join(a.out, f"mask_{i:05d}.png")
    if not os.path.exists(path):
        remove(frames[i], session=s, only_mask=True).save(path)
    print(f"mask {n + 1}/{len(keys)}", flush=True)
