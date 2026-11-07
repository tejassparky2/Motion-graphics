"""2D pass for helper 9's Episode 3 shots (DIORAMA_EP03.md), over the Blender frames, from
build/monsters/diorama_ep03/<SHOT>_anchors.json (written by diorama_ep03/helper9.py):

    S04  none (the sunset is all in 3D).
    S05  the village's one coral dot (Kai's mark) gets a soft coral bloom with a hot core and a slow pulse: the one
         warm spot on the dark island.
    S18  after the cut, a coral bloom on the lighthouse's lamp room that swells on "lighthouse".

    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep03/post_helper9.py S05             # mp4 + sheet
    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep03/post_helper9.py S05 --still F SRC DST

Reads build/monsters/diorama_ep03/<SHOT>/0001.png ... (or H9_SRC), filling frames rendered elsewhere from the raw
parts in out/monsters/diorama_ep03/parts/<SHOT>_fAAA-BBB[_vN].mp4 (the shortest part wins); writes <SHOT>_post/,
then out/monsters/diorama_ep03/shots/<SHOT>.mp4 (crf 10, bitexact, stream-copy remux, no encoder strings) and
<SHOT>_sheet.jpg.
"""
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import cairo  # noqa: E402
from channels.monsters import fx2d  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
PARTS = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "parts")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]
CORAL = (1.0, 0.52, 0.40)
HOT = (1.0, 0.86, 0.78)


def anchors(shot):
    p = os.path.join(BUILD, f"{shot}_anchors.json")
    if not os.path.exists(p):
        return {}, {}
    with open(p) as fh:
        d = json.load(fh)
    return d.get("meta", {}), {int(k): v for k, v in d["frames"].items()}


def s04(cr, f, meta, A, k):
    return


def s05(cr, f, meta, A, k):
    a = A.get(f, {}).get("dot")
    if not a or a[2] <= 0:
        return
    x, y = a[0] * k, a[1] * k
    p = 1.0 + 0.12 * math.sin(f / 7.0)
    fx2d._glow(cr, x, y, 46 * k * p, CORAL, 0.55)
    fx2d._glow(cr, x, y, 16 * k * p, CORAL, 0.9)
    fx2d._glow(cr, x, y, 5 * k, HOT, 1.0)


def s18(cr, f, meta, A, k):
    if f < meta.get("f_cut", 10 ** 6):
        return
    a = A.get(f, {}).get("lamp")
    if not a or a[2] <= 0:
        return
    fl = meta.get("f_lh", f)
    sw = 1.0 + 0.45 * math.exp(-((f - fl - 4) / 6.0) ** 2)                 # the swell on "lighthouse"
    x, y = a[0] * k, a[1] * k
    fx2d._glow(cr, x, y, 120 * k * sw, CORAL, 0.28 * sw)
    fx2d._glow(cr, x, y, 40 * k * sw, CORAL, 0.55)
    fx2d._glow(cr, x, y, 10 * k, HOT, 0.8)


DRAW = {"S04": s04, "S05": s05, "S18": s18}


def frame(shot, f, src, dst, meta, A):
    surf = cairo.ImageSurface.create_from_png(src)
    if surf.get_format() != cairo.FORMAT_ARGB32:
        s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
        c2 = cairo.Context(s2)
        c2.set_source_surface(surf)
        c2.paint()
        surf = s2
    cr = cairo.Context(surf)
    DRAW[shot](cr, f, meta, A, surf.get_width() / 720)
    surf.flush()
    surf.write_to_png(dst)


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:04d}.png")).convert("RGB") for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 7)
    out = Image.new("RGB", (w * cols, h * (-(-len(ims) // cols))), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path, quality=88)


def _src(shot):
    return os.environ.get("H9_SRC") or os.path.join(BUILD, shot)


def _frames(shot):
    with open(os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")) as fh:
        return next(s for s in json.load(fh)["shots"] if s["shot"] == shot)["render_frames"]


def join(shot, n):
    src_dir = _src(shot)
    os.makedirs(src_dir, exist_ok=True)

    def rng(path):
        m = re.search(r"_f(\d+)-(\d+)(?:_v\d+)?\.mp4$", path)
        return int(m.group(1)), int(m.group(2))
    for part in sorted(glob.glob(os.path.join(PARTS, f"{shot}_f*.mp4")), key=lambda p: (rng(p)[1] - rng(p)[0], p)):
        a, b = rng(part)
        if all(os.path.exists(os.path.join(src_dir, f"{f:04d}.png")) for f in range(a, b + 1)):
            continue
        tmp = os.path.join(BUILD, f"{shot}_join")
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", part, "-start_number", str(a),
                        os.path.join(tmp, "%04d.png")], check=True)
        got = sorted(os.listdir(tmp))
        if len(got) != b - a + 1:
            raise SystemExit(f"{part}: {len(got)} frames, expected {b - a + 1}")
        for g in got:
            if not os.path.exists(os.path.join(src_dir, g)):
                shutil.move(os.path.join(tmp, g), os.path.join(src_dir, g))
        shutil.rmtree(tmp)
        print("joined", os.path.basename(part))
    missing = [f for f in range(1, n + 1) if not os.path.exists(os.path.join(src_dir, f"{f:04d}.png"))]
    if missing:
        raise SystemExit(f"{shot}: missing frames {missing[0]}..{missing[-1]} ({len(missing)})")


def run(shot):
    meta, A = anchors(shot)
    n = _frames(shot)
    join(shot, n)
    src_dir, out_frames = _src(shot), os.path.join(BUILD, f"{shot}_post")
    shutil.rmtree(out_frames, ignore_errors=True)
    os.makedirs(out_frames)
    for f in range(1, n + 1):
        frame(shot, f, os.path.join(src_dir, f"{f:04d}.png"), os.path.join(out_frames, f"{f:04d}.png"), meta, A)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%04d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    sheet(out_frames, n, os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    print(mp4, n, "frames")


def still(shot, f, src, dst):
    meta, A = anchors(shot)
    frame(shot, f, src, dst, meta, A)
    print(dst)


if __name__ == "__main__":
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        still(sys.argv[1], int(sys.argv[i + 1]), sys.argv[i + 2], sys.argv[i + 3])
    else:
        run(sys.argv[1])
