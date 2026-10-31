"""S08b's 2D pass (DIORAMA_EP01_V3.md: effects done properly in 2D, from the Q5 fx2d library): over the Blender frames,
fx2d.electric_arcs runs the current from the power strip through the water to Kai's feet (travel), then crackles
over his body along his joints; fx2d.xray_flash strobes his skeleton on "died."; then the frame is black (in the
render). The builder (diorama_v3/helper4.py) exports the per-frame joints and the water path to build/monsters/
diorama_v3/. The sound is helper 7's mix, so every effect here runs with sound=False.

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08b FRAMES
    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08b XR --subject --frames 14-23
    python channels/monsters/diorama_v3/helper4_comp.py FRAMES --sub XR/subject --encode
        -> out/monsters/diorama_v3/shots/S08b.mp4 + S08b_sheet.jpg  (--only 12,18 writes test PNGs instead)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)
from channels.monsters import comp, fx2d  # noqa: E402
from channels.monsters.diorama_v3.helper4 import BUILD, _beats  # noqa: E402
from channels.monsters.mk import joints as mkj  # noqa: E402

FPS = 24
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]
CHAINS = [("l_foot", "l_knee", "l_hip", "chest"), ("r_foot", "r_knee", "r_hip", "neck"),
          ("chest", "l_shoulder", "l_elbow", "l_hand"), ("chest", "r_shoulder", "r_elbow", "r_hand"),
          ("neck", "head")]


def T(frame):
    """Shot time of a 1-based frame."""
    return (frame - 1) / FPS


def _frame(t):
    return int(round(t * FPS)) + 1


def water_arcs(cr, t, water, start, end, travel, bright_until):
    if t >= end:                                                     # nothing over the black (fx2d fades past `end`)
        return
    path = water.get(_frame(t)) or water[max(water)]
    k = 1.0 if t < bright_until else 0.55
    fx2d.electric_arcs(cr, t, start, end, path=path, n=3, width=5.0 * k, branches=3, travel=travel, flicker=0.2,
                       sound=False, seed=3)


def body_arcs(cr, t, jfn, start, end, dim_from):
    if t >= end:
        return
    j = jfn(t)
    chains = CHAINS if t < dim_from else CHAINS[:2]                  # after the lights die: only the legs crackle
    for i, ch in enumerate(chains):
        fx2d.electric_arcs(cr, t, start, end, path=[j[k] for k in ch], n=2, width=4.0 if t < dim_from else 3.0,
                           branches=2, rough=0.3, flicker=0.2, sound=False, seed=11 + i)


def xray(cr, t, jfn, start, frames, sub):
    mask = None
    p = os.path.join(sub, f"{_frame(t):04d}.png") if sub else None
    if p and os.path.exists(p):
        mask = comp._load(p)
    fx2d.xray_flash(cr, t, start, frames=frames, beat=2, joints=jfn, mask=mask, sound=False)


def shot(frames_dir, sub, n):
    B = _beats(n)
    jfn = mkj.at(mkj.load(os.path.join(BUILD, "S08b_joints.json")), 1)
    with open(os.path.join(BUILD, "S08b_water.json")) as fh:
        water = {int(k): [tuple(p) for p in v] for k, v in json.load(fh).items()}
    r0, r1 = B["run"]
    ov = [
        (water_arcs, dict(water=water, start=T(r0), end=T(B["black"]), travel=T(r1) - T(r0),
                          bright_until=T(B["out"]))),
        (body_arcs, dict(jfn=jfn, start=T(B["hit"]), end=T(B["black"]), dim_from=T(B["out"]))),
        (xray, dict(jfn=jfn, start=T(B["xray"][0]), frames=B["xray"][-1] - B["xray"][0] + 1, sub=sub)),
    ]
    return comp.Shot(comp.Source(frames_dir, subject=None), n / FPS, ov, name="S08b")


def sheet(frames, path, every=6):
    from PIL import Image
    ims = [Image.open(f) for f in frames[::every]]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 6)
    sh = Image.new("RGB", (w * cols, h * -(-len(ims) // cols)), "white")
    for i, im in enumerate(ims):
        sh.paste(im.convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sh.save(path, quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames_dir")
    ap.add_argument("--sub", default=None, help="the subject pass (RGBA) for the x-ray frames")
    ap.add_argument("--out", default=None, help="where the composited PNGs go (default: a temp dir)")
    ap.add_argument("--only", default=None, help="comma-separated 1-based frames: write just these, for checks")
    ap.add_argument("--encode", action="store_true", help="encode out/monsters/diorama_v3/shots/S08b.mp4 + sheet")
    a = ap.parse_args()
    n = len([f for f in os.listdir(a.frames_dir) if f.endswith(".png") and f[:4].isdigit()])
    sh = shot(a.frames_dir, a.sub, n)
    out = a.out or tempfile.mkdtemp(prefix="s08b_comp_")
    if a.only:
        for f in (int(v) for v in a.only.split(",")):
            comp.render([sh], out, frames=(f - 1, f - 1), check=False, verbose=False)
        print("wrote", sorted(os.listdir(out)))
        return
    rep = comp.render([sh], out, check=False)
    print(f"S08b comp: {rep['frames']} frames, {rep['ms_per_frame']:.0f} ms/frame")
    if a.encode:
        od = os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots")
        os.makedirs(od, exist_ok=True)
        tmp = os.path.join(od, "_S08b_tmp.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(out, "%05d.png"),
                        "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p", *CLEAN, tmp],
                       check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN,
                        os.path.join(od, "S08b.mp4")], check=True)
        os.remove(tmp)
        sheet(sorted(os.path.join(out, f) for f in os.listdir(out) if f.endswith(".png")),
              os.path.join(od, "S08b_sheet.jpg"))
        print("encoded", os.path.join(od, "S08b.mp4"))
        if not a.out:
            shutil.rmtree(out)


if __name__ == "__main__":
    main()
