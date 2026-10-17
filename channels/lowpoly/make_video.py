"""Low-poly style test (separate channel, not Interestingly Strange): record scene.html, add a soft music bed, encode.

    python channels/lowpoly/make_video.py      -> out/lowpoly/style_test.mp4
"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from render import CLEAN, ffmpeg_bin   # noqa: E402
from motion.audio import build_soundtrack   # noqa: E402

FPS = 30
frames = os.path.join(ROOT, "build", "lowpoly", "frames")
out = os.path.join(ROOT, "out", "lowpoly", "style_test.mp4")
os.makedirs(os.path.dirname(out), exist_ok=True)
shutil.rmtree(frames, ignore_errors=True)
subprocess.check_call(["node", os.path.join(ROOT, "channels", "lowpoly", "render.mjs"), frames, str(FPS)])
n = len(glob.glob(os.path.join(frames, "f*.png")))
wav = os.path.join(ROOT, "build", "lowpoly", "music.wav")
build_soundtrack([], n / FPS, wav, seed="lowpoly")
subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", "-framerate", str(FPS), "-i",
                       os.path.join(frames, "f%05d.png"), "-i", wav, "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", *CLEAN,
                       "-movflags", "+faststart", out])
print("wrote", out)
