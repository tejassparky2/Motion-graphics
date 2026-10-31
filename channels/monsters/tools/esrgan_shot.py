"""Upscale one finished shot 720x1280 -> 1080x1920 with the adopted Q4 blend (out/monsters/diorama_v3/Q4_upscale.md):
65% Real-ESRGAN realesr-animevideov3 (4x, then lanczos down) + 35% plain lanczos. Crisp lines and comic marks; the
tilt-shift bokeh keeps its softness.

    python channels/monsters/tools/esrgan_shot.py S08b                      whole shot -> shots_1080/S08b.mp4
    python channels/monsters/tools/esrgan_shot.py S08b --frames 1-32        a part -> shots_1080/parts/S08b_f001-032.mp4
    python channels/monsters/tools/esrgan_shot.py S08b --join               the parts (contiguous, 1..N) -> S08b.mp4

  --src DIR   default out/monsters/diorama_v3/shots (reads <SHOT>.mp4, 720x1280)
  --out DIR   default out/monsters/diorama_v3/shots_1080
  --threads N torch CPU threads (default: all cores).
  --force     redo a shot or part whose output already exists with the right frame count (skipped by default).
  --exact     the plain fp32 network (~7.5 s per frame on 4 cores). By default the fast path runs (channels_last, plus
              bf16 on a CPU with AMX/AVX512-BF16): ~1.9 s per frame on 4 cores, PSNR >= 54 dB against --exact
              (out/monsters/diorama_v3/Q4_speed.md). Two parts side by side with --threads 2 each beat one with 4.

Splitting: idle helpers each take a frame range of the same shot (frames are 1-based, as in render_shot.py); the
last one (or anyone) runs --join, which checks the parts cover every frame exactly once.
Needs torch (CPU is fine: pip install torch --index-url https://download.pytorch.org/whl/cpu), numpy, Pillow and
ffmpeg. Output: x264 crf 10 yuv420p, then a stream-copy remux with the bitexact flags (no encoder strings).
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import time

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)
WEIGHTS = os.path.join(ROOT, "assets", "models", "realesr-animevideov3.pth")
BLEND = 0.65                                               # the ESRGAN share (Q4, adopted 31 Oct 2026)
SRC_W, SRC_H, W, H = 720, 1280, 1080, 1920
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]


def count_frames(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames,width,height", "-of", "csv=p=0", mp4], capture_output=True,
                         text=True, check=True).stdout.strip().split(",")
    return int(out[2]), int(out[0]), int(out[1])


def frames_in(mp4, a, b, w, h):
    """Yield frames a..b (1-based) of `mp4` as HxWx3 uint8 arrays."""
    cmd = ["ffmpeg", "-loglevel", "error", "-i", mp4, "-vf", f"select=between(n\\,{a - 1}\\,{b - 1})",
           "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    size = w * h * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


def clean_remux(tmp, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, dst], check=True)


def upscale_range(shot, a, b, src, dst, threads, fast=True):
    import torch
    from channels.monsters.tools.esrgan_upscale import load, upscale
    if threads:
        torch.set_num_threads(threads)
    net = load(WEIGHTS, fast=fast)
    n, w, h = count_frames(src)
    if (w, h) != (SRC_W, SRC_H):
        print(f"{shot}: source is {w}x{h}, expected {SRC_W}x{SRC_H}; upscaling to {W}x{H} anyway", flush=True)
    b = min(b, n)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = tempfile.mktemp(suffix=".mp4", dir=os.path.dirname(dst))
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                            f"{W}x{H}", "-framerate", "24", "-i", "-", "-c:v", "libx264", "-crf", "10", "-preset",
                            "slow", "-pix_fmt", "yuv420p", *CLEAN, tmp], stdin=subprocess.PIPE)
    t0, done = time.time(), 0
    for arr in frames_in(src, a, b, w, h):
        im = Image.fromarray(arr)
        sr = upscale(net, im, (W, H))
        lz = im.resize((W, H), Image.LANCZOS)
        enc.stdin.write(np.asarray(Image.blend(lz, sr, BLEND), np.uint8).tobytes())
        done += 1
        if done % 6 == 0 or done == b - a + 1:
            el = time.time() - t0
            print(f"{shot} f{a + done - 1}: {done}/{b - a + 1}, {el / done:.1f} s/frame", flush=True)
    enc.stdin.close()
    if enc.wait() or done != b - a + 1:
        raise SystemExit(f"{shot}: encoded {done} of {b - a + 1} frames")
    clean_remux(tmp, dst)
    os.remove(tmp)
    print(f"{shot}: wrote {dst} ({done} frames, {(time.time() - t0) / 60:.1f} min)", flush=True)


def join(shot, src, out):
    """Concatenate shots_1080/parts/<SHOT>_fAAA-BBB.mp4 (they must tile 1..N exactly) into shots_1080/<SHOT>.mp4."""
    n, _, _ = count_frames(src)
    pdir = os.path.join(out, "parts")
    parts = []
    for f in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        m = re.fullmatch(rf"{re.escape(shot)}_f(\d+)-(\d+)\.mp4", f)
        if m:
            parts.append((int(m.group(1)), int(m.group(2)), os.path.join(pdir, f)))
    parts.sort()
    want = 1
    for a, b, p in parts:
        if a != want:
            raise SystemExit(f"{shot}: parts leave a gap or overlap at frame {want} (next part starts at {a})")
        if count_frames(p)[0] != b - a + 1:
            raise SystemExit(f"{shot}: {p} has the wrong frame count")
        want = b + 1
    if want != n + 1:
        raise SystemExit(f"{shot}: parts cover 1-{want - 1}, the shot has {n} frames")
    lst = tempfile.mktemp(suffix=".txt", dir=out)
    with open(lst, "w") as fh:
        fh.writelines(f"file '{os.path.abspath(p)}'\n" for _, _, p in parts)
    tmp = tempfile.mktemp(suffix=".mp4", dir=out)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    *CLEAN, tmp], check=True)
    os.remove(lst)
    dst = os.path.join(out, f"{shot}.mp4")
    clean_remux(tmp, dst)
    os.remove(tmp)
    got = count_frames(dst)[0]
    if got != n:
        raise SystemExit(f"{shot}: joined {got} frames, want {n}")
    print(f"{shot}: joined {len(parts)} parts -> {dst} ({got} frames)", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("shot")
    ap.add_argument("--frames", help="A-B, 1-based, inclusive: write a part instead of the whole shot")
    ap.add_argument("--join", action="store_true", help="join the shot's parts into the whole shot")
    ap.add_argument("--src", default=os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots"))
    ap.add_argument("--out", default=os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots_1080"))
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--exact", action="store_true", help="the plain fp32 network (slow; the quality reference)")
    ap.add_argument("--force", action="store_true", help="redo a shot or part that is already done")
    a = ap.parse_args()
    src = os.path.join(a.src, f"{a.shot}.mp4")
    if not os.path.exists(src):
        raise SystemExit(f"no {src}")
    if a.join:
        return join(a.shot, src, a.out)
    n = count_frames(src)[0]
    if a.frames:
        f0, f1 = (int(v) for v in a.frames.split("-"))
        f1 = min(f1, n)
        dst = os.path.join(a.out, "parts", f"{a.shot}_f{f0:03d}-{f1:03d}.mp4")
    else:
        f0, f1, dst = 1, n, os.path.join(a.out, f"{a.shot}.mp4")
    if not a.force and os.path.exists(dst) and count_frames(dst)[:1] == (f1 - f0 + 1,):
        print(f"{a.shot}: {dst} is already done ({f1 - f0 + 1} frames); --force to redo it", flush=True)
        return
    upscale_range(a.shot, f0, f1, src, dst, a.threads, fast=not a.exact)


if __name__ == "__main__":
    main()
