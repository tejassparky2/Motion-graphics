"""Join a diorama shot rendered in pieces (HELPERS.md chunk rule) into out/monsters/diorama/shots/<SHOT>.mp4 + sheet.

Each piece is either a near-lossless part (out/monsters/diorama/parts/<SHOT>_fAAA-BBB.mp4, frames AAA..BBB) or a folder
of render_shot.py PNGs (0001.png ...) given as DIR:AAA-BBB. Every frame 1..render_frames must be covered exactly once;
the result is encoded like every shot (crf 10, no encoder tags) and checked for its frame count.

    /home/user/.venv-main/bin/python channels/monsters/diorama/join_parts.py S06 /scratch/s06:1-21 \\
        out/monsters/diorama/parts/S06_f022-041.mp4
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SHOTS = os.path.join(ROOT, "out", "monsters", "diorama", "shots")
CLEAN = ["-map_metadata", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact", "-bsf:v", "filter_units=remove_types=6"]


def main():
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    shot, pieces = sys.argv[1], sys.argv[2:]
    timing = json.load(open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")))
    n = {s["shot"]: s["render_frames"] for s in timing["shots"]}[shot]
    tmp = tempfile.mkdtemp(prefix=f"join_{shot}_")
    have = {}
    for p in pieces:
        if p.endswith(".mp4"):
            a, b = map(int, re.search(r"_f(\d+)-(\d+)\.mp4$", p).groups())
            d = os.path.join(tmp, f"part{a}")
            os.makedirs(d)
            subprocess.run([ff, "-v", "error", "-i", p, "-start_number", str(a), os.path.join(d, "%04d.png")],
                           check=True)
            src = {f: os.path.join(d, f"{f:04d}.png") for f in range(a, b + 1)}
        else:
            d, rng = p.rsplit(":", 1)
            a, b = map(int, rng.split("-"))
            src = {f: os.path.join(d, f"{f:04d}.png") for f in range(a, b + 1)}
        for f, path in src.items():
            if f in have:
                sys.exit(f"frame {f} is in two pieces")
            if not os.path.exists(path):
                sys.exit(f"frame {f} missing: {path}")
            have[f] = path
    missing = [f for f in range(1, n + 1) if f not in have]
    if missing:
        sys.exit(f"{shot}: frames missing {missing[:10]}{'...' if len(missing) > 10 else ''} of 1-{n}")
    seq = os.path.join(tmp, "seq")
    os.makedirs(seq)
    for f in range(1, n + 1):
        shutil.copy(have[f], os.path.join(seq, f"{f:04d}.png"))
    out = os.path.join(SHOTS, shot + ".mp4")
    enc = os.path.join(tmp, "enc.mp4")
    subprocess.run([ff, "-v", "error", "-framerate", "24", "-start_number", "1", "-i", os.path.join(seq, "%04d.png"),
                    "-frames:v", str(n), "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-crf", "10",
                    "-pix_fmt", "yuv420p", *CLEAN, enc], check=True)
    subprocess.run([ff, "-y", "-v", "error", "-i", enc, "-c", "copy", "-map_metadata", "-1", "-fflags", "+bitexact",
                    "-metadata:s:v", "handler_name=", "-movflags", "+faststart", out], check=True)
    subprocess.run([ff, "-y", "-v", "error", "-i", out, "-vf", "select=not(mod(n\\,6)),scale=180:320,tile=7x2",
                    "-frames:v", "1", "-q:v", "3", os.path.join(SHOTS, shot + "_sheet.jpg")], check=True)
    got = len(subprocess.run([ff, "-v", "error", "-i", out, "-vf", "scale=8:8", "-f", "rawvideo", "-pix_fmt", "gray",
                              "-"], capture_output=True, check=True).stdout) // 64
    data = open(out, "rb").read()
    tags = {t: data.count(t.encode()) for t in ("x264", "Lavf", "Lavc")}
    shutil.rmtree(tmp)
    print(f"{shot}: {got}/{n} frames, tags {tags}" + ("" if got == n and not any(tags.values()) else "  **CHECK**"))


if __name__ == "__main__":
    main()
