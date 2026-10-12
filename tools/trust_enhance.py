"""Enhance a phone clip for Pushpa Charitable Trust: keep the original speech, clean it, even out the picture.

  python3 tools/trust_enhance.py IN.mp4 OUT.mp4 --rnnoise bd.rnnn

Picture: light denoise, upscale to 1080x1920, the shared pro_grade look (white balance, exposure, S-curve),
gentle sharpening. Sound: rumble cut, RNNoise blended 70% with the original (more cuts syllables on this
footage), a light FFT denoise, clarity lift, soft compression and -14 LUFS. No captions, no added voice.
"""
import argparse
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pro_grade import ClipGrade  # noqa: E402

W, H = 1080, 1920
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name=", "-metadata:s:v", "encoder="]


def _loudness(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def clean_audio(src, dst, rnnoise, mix=0.7, target=-14.0):
    af = (f"highpass=f=80,arnndn=m={rnnoise}:mix={mix},afftdn=nr=10:nf=-50:tn=1,"
          "equalizer=f=3000:t=q:w=1.2:g=2,equalizer=f=250:t=q:w=1:g=-2,"
          "acompressor=threshold=-22dB:ratio=2.5:attack=10:release=250")
    tmp = dst + ".pre.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "48000", "-af", af, tmp],
                   check=True)
    # stereo copy of the mono voice, measured and lifted to the target with a peak limiter
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ac", "2", "-f", "wav", tmp + ".st.wav"], check=True)
    gain = target - _loudness(tmp + ".st.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp + ".st.wav", "-af",
                    f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=5:release=60:level=disabled", dst], check=True)
    os.remove(tmp)
    os.remove(tmp + ".st.wav")


def replace_audio(video, src, rnnoise):
    """Re-clean the sound of an already enhanced clip without re-encoding its picture."""
    wav = video + ".voice.wav"
    clean_audio(src, wav, rnnoise)
    tmp = video + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    *CLEAN, tmp], check=True)
    os.replace(tmp, video)
    os.remove(wav)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--rnnoise", required=True)
    ap.add_argument("--fps", default="30")
    ap.add_argument("--audio-only", action="store_true", help="only re-clean the sound of an enhanced DST")
    a = ap.parse_args()
    if a.audio_only:
        return replace_audio(a.dst, a.src, a.rnnoise)

    wav = a.dst + ".voice.wav"
    clean_audio(a.src, wav, a.rnnoise)
    grade = ClipGrade(a.src)

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.src, "-an", "-vf",
                            f"fps={a.fps},hqdn3d=1.5:1.5:4:4,scale={W}:{H}:flags=lanczos,setsar=1",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", a.fps, "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a",
                            "-vf", "unsharp=5:5:0.45:5:5:0", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", *CLEAN, a.dst], stdin=subprocess.PIPE)
    n = W * H * 3
    from PIL import Image
    while True:
        buf = dec.stdout.read(n)
        if len(buf) < n:
            break
        frame = Image.fromarray(np.frombuffer(buf, np.uint8).reshape(H, W, 3))
        enc.stdin.write(np.asarray(grade(frame)).tobytes())
    enc.stdin.close()
    dec.wait()
    if enc.wait():
        sys.exit("encode failed")
    os.remove(wav)


if __name__ == "__main__":
    main()
