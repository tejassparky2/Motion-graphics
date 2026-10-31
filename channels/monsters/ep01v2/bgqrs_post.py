"""2D pass for the chest scene (S01, S16-S21): the shot effects (comic faces from fx2d_anime, TP7) composited with
comp.py over the Blender frames, then the mp4 and contact sheet for out/monsters/ep01v2/shots/.

    FPS=24 python channels/monsters/ep01v2/bgqrs_post.py S19 [S20 ...]

Needs a venv with pycairo, numpy, scipy, opencv-python-headless and pillow, plus ffmpeg (helpers 5 and 6: fx2d
imports scipy). Reads build/monsters/ep01v2/<SHOT>/0001.png ... (render_shot.py output; subject/ when rendered with --subject) and
the screen anchors the builder wrote (build/monsters/ep01v2/<SHOT>_anchors.json). No text and no HUD (owner's rule).
"""
import json
import math
import os
import subprocess
import sys

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import H, W, cairo, clamp01, ease_out  # noqa: E402
from channels.monsters import comp, fx2d, fx2d_anime, fx2d_extra  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "ep01v2")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "ep01v2", "shots")
FPS = 24
# render.py's output hygiene: no container metadata, no encoder tags, no x264 settings SEI
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def face_geom(a, t):
    """(between-the-eyes point, face width px, tilt) from the eye anchors, for fx2d_anime's comic faces."""
    (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
    d = math.hypot(rx - lx, ry - ly)
    tilt = math.atan2(ry - ly, rx - lx)
    if abs(tilt) > math.pi / 2:                                   # keep the face's "up" upward on screen
        tilt -= math.copysign(math.pi, tilt)
    return ((lx + rx) / 2, (ly + ry) / 2), d * 2.6, tilt, ((lx, ly), (rx, ry))


def skin_near_eyes(frame_png, eyes, er):
    """Kai's rendered skin colour on the cheeks just below each eye (median), so the comic dot-eye patches match
    his own skin in that light rather than a fixed cream."""
    from PIL import Image
    im = Image.open(frame_png).convert("RGB")
    px = []
    for ex, ey in eyes:
        for dx in (-0.6, 0.0, 0.6):
            for dy in (1.7, 2.1):
                px.append(im.getpixel((int(ex + dx * er), int(ey + dy * er))))
    px.sort(key=sum)
    r, g, b = px[len(px) // 2]
    return (r / 255, g / 255, b / 255, 1.0)


def plate_eyes(frame_png, eyes, er):
    """Kai's eyes where the render actually drew them: the centre of the pale sclera pixels near each anchor eye
    (the bone-based anchors can be ~10 px off at close range), each searched on its own side of the midpoint.
    Keeps the anchor for an eye with too few sclera pixels or one that would move more than er."""
    import numpy as np
    im = np.asarray(Image.open(frame_png).convert("RGB")).astype(int)
    pale = (im[..., 2] > im[..., 0] + 4) & (im.sum(axis=2) > 540)
    (lx, ly), (rx, ry) = eyes
    mx, my = (lx + rx) / 2, (ly + ry) / 2
    out = []
    for ex, ey in eyes:
        r = int(2.2 * er)
        x0, y0 = max(0, int(ex) - r), max(0, int(ey) - r)
        ys, xs = np.nonzero(pale[y0:int(ey) + r, x0:int(ex) + r])
        xs, ys = xs + x0, ys + y0
        own = (xs - mx) * (ex - mx) + (ys - my) * (ey - my) > 0     # this eye's half of the face
        xs, ys = xs[own], ys[own]
        if len(xs) < 40:
            out.append((ex, ey))
            continue
        px, py = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
        out.append((px, py) if math.hypot(px - ex, py - ey) <= er else (ex, ey))
    return tuple(out)


def at(a, t, name):
    """Anchor `name` at shot time t (frame-accurate, held past the last frame)."""
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


# ---------------------------------------------------------------- shot effects (comic faces: fx2d_anime, TP7)

def sun_glare(cr, t, start, x=610, y=70, strength=1.0):
    """Hot sun glare from the top corner: a warm bloom, slowly turning soft rays and three flare discs on a line
    toward the frame centre (on 1s, very slow)."""
    if t < start:
        return
    a = strength * clamp01((t - start) / 0.3)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    fx2d_extra._glow(cr, x, y, 420, (1.0, 0.82, 0.5), 0.55 * a)
    fx2d_extra._glow(cr, x, y, 150, (1.0, 0.97, 0.85), 0.8 * a)
    for k in range(9):
        ang = t * 0.05 + k * 2 * math.pi / 9
        cr.move_to(x, y)
        cr.arc(x, y, 900, ang, ang + 0.06)
        cr.close_path()
    g = cairo.RadialGradient(x, y, 0, x, y, 900)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.22 * a)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    cr.set_source(g)
    cr.fill()
    cx, cy = W / 2, H * 0.42
    for k, (u, r, col) in enumerate(((0.45, 38, (1.0, 0.7, 0.5)), (0.7, 22, (0.6, 0.85, 1.0)),
                                     (1.25, 60, (1.0, 0.85, 0.6)))):
        px, py = x + (cx - x) * u, y + (cy - y) * u
        cr.new_path()
        for j in range(6):
            ang = j * math.pi / 3 + 0.3
            (cr.move_to if j == 0 else cr.line_to)(px + r * math.cos(ang), py + r * math.sin(ang))
        cr.close_path()
        cr.set_source_rgba(*col, 0.12 * a)
        cr.fill()
    cr.restore()


def glint(cr, t, start, x, y, size=26, life=0.3):
    """A sparkle on the eye as the thought lands."""
    u = (t - start) / life
    if 0 <= u < 1:
        fx2d_extra._sparkle(cr, x, y, size * math.sin(math.pi * u), (1, 1, 1), 1.0, rot=0.3)


def push(cr, t, start, end, cx=W / 2, cy=H / 2, amount=0.08):
    """A slow 2D push-in on the plate (TP13: <=10% push-ins are done in 2D)."""
    k = 1 + amount * ease_out(clamp01((t - start) / max(end - start, 1e-3)) ** 0.9)
    surf = cr.get_target()
    snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c2 = cairo.Context(snap)
    c2.set_source_surface(surf, 0, 0)
    c2.paint()
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    cr.translate(-cx, -cy)
    cr.set_source_surface(snap, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


def snap_zoom(cr, t, start, cx, cy, amount=0.18, frames=3):
    """An anime snap-zoom into the eyes: the picture scales 1 -> 1 + amount about (cx, cy) over `frames` frames
    from `start` (on 1s), then holds; edges are filled by stretching the border pixels, as fx2d_anime.shake does."""
    if t < start - 1e-6:
        return
    k = 1 + amount * min(1.0, (int(round((t - start) * FPS)) + 1) / frames)
    surf = cr.get_target()
    surf.flush()
    copy = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
    c = cairo.Context(copy)
    c.set_source_surface(surf, 0, 0)
    c.paint()
    pat = cairo.SurfacePattern(copy)
    pat.set_extend(cairo.EXTEND_PAD)
    pat.set_filter(cairo.FILTER_GOOD)
    pat.set_matrix(cairo.Matrix(1 / k, 0, 0, 1 / k, cx * (1 - 1 / k), cy * (1 - 1 / k)))
    cr.save()
    cr.identity_matrix()
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source(pat)
    cr.paint()
    cr.restore()


def puff(cr, t, start, x, y, size=1.0, seed=0):
    """A tiny, sad "pff" of dust: three small cel puffs (no text)."""
    fx2d.dust_puffs(cr, t, start, x, y, n=3, spread=int(30 * size), size=int(15 * size), dur=0.5, seed=seed)


# ---------------------------------------------------------------- the shots' 2D

def overlays(shot):
    """Shot-local overlays [(fn, kwargs)] for each shot."""
    if shot in ("S01", "S16"):                                    # frame 0 (and its rhyme): pin-prick terror + sweat
        a = anchors(shot)
        t0 = 0.0 if shot == "S01" else 41 / FPS                   # S16: from his terror on the wide (frame 42)
        (cx, cy), size, tilt, eyes = face_geom(a, t0)
        er = size / 2.6 * 0.26 * 1.08                             # 8% over the 3D eye, so none of it peeks out
        if shot in ("S01", "S16"):                                # on the eyes as rendered (QA: a sliver showed)
            eyes = plate_eyes(os.path.join(BUILD, shot, "0012.png" if shot == "S01" else "0042.png"), eyes, er)
        return [(fx2d_anime.terror_eyes, dict(start=t0, end=99, x=cx, y=cy, size=size, eyes=eyes, er=er, tilt=tilt)),
                (fx2d_anime.sweat_drop, dict(start=t0 - 0.2, end=99, x=cx, y=cy, size=size, tilt=tilt))]
    if shot == "S18":                                             # the realisation lands on "wet" (frame 30)
        a = anchors("S18")
        ex, ey = at(a, 32 / FPS, "eyes")
        return [(comp.backdrop, dict(start=29 / FPS, end=99, fn=fx2d_anime.emotion_bg,
                                     args=dict(mood="realisation", cx=ex, cy=ey))),
                (glint, dict(start=32 / FPS, x=ex + 70, y=ey - 40)),
                (snap_zoom, dict(start=29 / FPS, cx=ex, cy=ey))]    # last, so the glint stays on the eye
    if shot == "S19":
        a = anchors("S19")
        n = max(a)
        (cx, cy), size, tilt, _ = face_geom(a, 0.4)
        return [(fx2d_anime.sweat_drop, dict(start=0.4, x=cx, y=cy, size=size, bead=True, tilt=tilt)),
                (push, dict(start=0.0, end=n / FPS, cx=cx, cy=cy, amount=0.08)),
                (sun_glare, dict(start=0.0)),
                (fx2d_extra.ambient, dict(start=0.0, strength=0.8, keep_clear=(cx, cy, 170)))]
    if shot == "S20":                                             # snap at 24, deadpan from the cut at 44
        a = anchors("S20")
        px, py = at(a, 23 / FPS, "tip")
        (cx, cy), size, tilt, eyes = face_geom(a, 50 / FPS)
        er = size / 2.6 * 0.23
        f70 = os.path.join(BUILD, "S20", "0070.png")
        if not os.path.exists(f70):
            f70 = os.path.join(BUILD, "bg", "review", "S20", "still_70.png")
        skin = skin_near_eyes(f70, eyes, er) if os.path.exists(f70) else fx2d_anime.SKIN
        return [(puff, dict(start=23 / FPS, x=px, y=py, size=1.0)),
                (fx2d_anime.dot_eyes, dict(start=43 / FPS, x=cx, y=cy, size=size, eyes=eyes, tilt=tilt, er=er,
                                           skin=skin)),
                (fx2d_anime.sweat_drop, dict(start=52 / FPS, end=99, x=cx, y=cy, size=size, tilt=tilt))]
    if shot == "S21":
        a = anchors("S21")
        with open(os.path.join(BUILD, "S21_lands.json")) as fh:
            lands = json.load(fh)
        return [(puff, dict(start=(f - 1) / FPS, x=at(a, (f - 1) / FPS, "feet")[0],
                            y=at(a, (f - 1) / FPS, "feet")[1], size=1.3, seed=k)) for k, f in enumerate(lands)]
    return []


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:05d}.png")).convert("RGB") for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 6)
    rows = -(-len(ims) // cols)
    out = Image.new("RGB", (w * cols, h * rows), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path, quality=88)


def run(shot):
    src = comp.Source(os.path.join(BUILD, shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4 = os.path.join(SHOTS_OUT, f"{shot}.mp4")
    tmp = os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    # a stream-copy remux drops the encoder name the first pass leaves in the track header (as render.py does)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    tags = {s: data.count(s.encode()) for s in ("x264 - core", "Lavf", "Lavc", "libx264", "encoder")}
    print(f"{shot}: {rep['frames']} frames, 2D {rep['ms_per_frame']:.0f} ms/frame, {mp4} "
          f"({os.path.getsize(mp4) / 1e6:.1f} MB), tags {tags}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
