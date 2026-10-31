"""2D grade-match for the reused v2 lab shots (S03a, S03b, S04, S05a, S05b), so they sit beside the v3 lab renders that
carry Q3 (channels/monsters/mk/grade.py LOOKS["lab"]) without a re-render.

The grade copies the structure of the Q3 compositor chain: lift/gamma/gain per channel, then saturation, then a soft
elliptical vignette (an ellipse 0.98 x 0.90 of the frame, Gaussian-blurred, MULTIPLY_ADD v / 1 - v). Its numbers
are fitted to helper 9's out/monsters/diorama_v3/okstills/Q3_lab_before_after.jpg (the same frame without and with
Q3): `--fit` re-fits them and prints the match; GRADE below holds the fitted values. The AO contact shadows are
lighting and can't be added in 2D.

    python channels/monsters/tools/grade_match.py --fit                 fit GRADE to the reference and report
    python channels/monsters/tools/grade_match.py S03a S03b ...         grade shots/<SHOT>.mp4 in place (+ sheet)
    python channels/monsters/tools/grade_match.py S03a --out DIR        write DIR/<SHOT>.mp4 instead

Output: x264 crf 10 yuv420p, then a stream-copy remux with the bitexact flags (no encoder strings), like the renders.
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SHOTS = os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots")
REF = os.path.join(ROOT, "out", "monsters", "diorama_v3", "okstills", "Q3_lab_before_after.jpg")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=", "-metadata:s:v", "encoder="]

# Fitted with --fit on the Q3 lab reference (31 Oct 2026). Mean colour error against Q3 (8-bit, RGB) went from
# shadows (-5.9, -4.2, -2.1) / mids (-8.1, -8.1, -7.8) / highlights (-6.2, -7.5, -8.7) to (0.4, -0.3, -0.6) /
# (0.0, 0.0, -0.3) / (0.0, 1.1, 2.3). The lift is the night lab's teal shadows (red down, blue up).
GRADE = dict(lift=(-0.0151, 0.012, 0.0226), gamma=(0.9666, 0.9375, 0.9616), gain=(1.0467, 1.0276, 1.0037),
             sat=1.0623, vignette=0.1386, blur=0.2611)


def vignette_mask(h, w, blur):
    """Blender's ellipse mask (0.98 x 0.90 of the frame, centred), Gaussian-blurred by `blur` x the width."""
    yy, xx = np.mgrid[0:h, 0:w]
    m = ((((xx + 0.5) / w - 0.5) / 0.49) ** 2 + (((yy + 0.5) / h - 0.5) / 0.45) ** 2 <= 1.0).astype(np.float32)
    return gaussian_filter(m, blur * w, mode="nearest")


def apply(img, g, mask=None):
    """img: HxWx3 float 0..1. Lift/gamma/gain per channel, saturation, then the vignette."""
    lift, gamma, gain = (np.asarray(g[k], np.float32) for k in ("lift", "gamma", "gain"))
    x = np.clip(img * gain + lift * (1 - img), 0, 1) ** (1 / gamma)
    lum = (x * np.array([0.2126, 0.7152, 0.0722], np.float32)).sum(-1, keepdims=True)
    x = lum + (x - lum) * g["sat"]
    if g["vignette"] > 0:
        if mask is None:
            mask = vignette_mask(*img.shape[:2], g["blur"])
        x = x * (mask * g["vignette"] + (1 - g["vignette"]))[..., None]
    return np.clip(x, 0, 1)


def _ref():
    im = np.asarray(Image.open(REF).convert("RGB")).astype(np.float32) / 255
    w = im.shape[1] // 2
    return im[:, :w], im[:, w:]


def report(before, after, graded):
    lum = (before * np.array([0.2126, 0.7152, 0.0722])).sum(-1)
    rows = []
    for name, m in (("shadows", lum < 0.25), ("mids", (lum >= 0.25) & (lum < 0.6)), ("highlights", lum >= 0.6)):
        d0 = np.abs(after[m] - before[m]).mean(0) * 255
        d1 = np.abs(after[m] - graded[m]).mean(0) * 255
        e0 = (after[m] - before[m]).mean(0) * 255
        e1 = (after[m] - graded[m]).mean(0) * 255
        rows.append(f"  {name:10s} |Q3 - before| {d0.round(1)}  |Q3 - graded| {d1.round(1)}   "
                    f"mean colour error before {e0.round(1)} -> graded {e1.round(1)} (8-bit levels, RGB)")
    return "\n".join(rows)


def fit():
    from scipy.optimize import least_squares
    before, after = _ref()
    sb, sa = before[::2, ::2], after[::2, ::2]

    def unpack(p):
        return dict(lift=p[0:3], gamma=p[3:6], gain=p[6:9], sat=p[9], vignette=p[10], blur=p[11])

    cache = {}

    def resid(p):
        g = unpack(p)
        key = round(float(g["blur"]), 4)
        if key not in cache:
            cache.clear()
            cache[key] = vignette_mask(*sb.shape[:2], g["blur"])
        return (apply(sb, g, cache[key]) - sa).ravel()

    p0 = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1.0, 0.2, 0.11])
    lo = [-0.1] * 3 + [0.7] * 3 + [0.8] * 3 + [0.8, 0.0, 0.02]
    hi = [0.1] * 3 + [1.4] * 3 + [1.2] * 3 + [1.3, 0.5, 0.3]
    r = least_squares(resid, p0, bounds=(lo, hi), diff_step=1e-3)
    g = unpack(r.x)
    g = {k: (tuple(round(float(v), 4) for v in g[k]) if k in ("lift", "gamma", "gain") else round(float(g[k]), 4))
         for k in g}
    graded = apply(before, g)
    print("GRADE =", g)
    print(report(before, after, graded))
    return g, graded


def grade_shot(shot, out_dir):
    src = os.path.join(SHOTS, f"{shot}.mp4")
    w, h = (int(v) for v in subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
         src], capture_output=True, text=True, check=True).stdout.strip().split(","))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    mask = vignette_mask(h, w, GRADE["blur"])
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, f"{shot}.mp4")
    tmp = dst + ".tmp.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                            "-r", "24", "-i", "-", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                            "-pix_fmt", "yuv420p", *CLEAN, tmp], stdin=subprocess.PIPE)
    sheet = []
    for i, f in enumerate(frames):
        out = (apply(f.astype(np.float32) / 255, GRADE, mask) * 255 + 0.5).astype(np.uint8)
        enc.stdin.write(out.tobytes())
        if i % max(1, len(frames) // 8) == 0 and len(sheet) < 8:
            sheet.append(Image.fromarray(out).resize((w // 4, h // 4)))
    enc.stdin.close()
    if enc.wait():
        sys.exit(f"{shot}: ffmpeg failed")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c", "copy", *CLEAN, dst], check=True)
    os.remove(tmp)
    s = Image.new("RGB", (sheet[0].width * len(sheet), sheet[0].height))
    for k, im in enumerate(sheet):
        s.paste(im, (k * im.width, 0))
    s.save(os.path.join(out_dir, f"{shot}_sheet.jpg"), quality=88)
    print(f"{shot}: {len(frames)} frames graded -> {os.path.relpath(dst, ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("shots", nargs="*")
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--out", default=SHOTS)
    a = ap.parse_args()
    if a.fit:
        fit()
    for shot in a.shots:
        grade_shot(shot, a.out)


if __name__ == "__main__":
    main()
