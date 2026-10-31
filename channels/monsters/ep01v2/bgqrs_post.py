"""2D pass for the chest scene (S01, S16-S21): the shot effects (comic faces from fx2d_anime, TP7) composited with
comp.py over the Blender frames, then the mp4 and contact sheet for out/monsters/ep01v2/shots/.

    FPS=24 python channels/monsters/ep01v2/bgqrs_post.py S19 [S20 ...]
    DIORAMA=1 FPS=24 python channels/monsters/ep01v2/bgqrs_post.py S17     (the diorama cut, DIORAMA_EP01.md)

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

DIORAMA = os.environ.get("DIORAMA") in ("1", "v3")             # "v3": Episode 1 v3 (DIORAMA_EP01_V3.md)
SET = {"1": "diorama", "v3": "diorama_v3"}.get(os.environ.get("DIORAMA"), "ep01v2")
BUILD = os.path.join(ROOT, "build", "monsters", SET)
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", SET, "shots")
CRF = "10" if SET == "diorama_v3" else "12"
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

def drop_glint(cr, t, a, f0, f1, size=22):
    """A sparkle riding the falling drop (anchor "drop") from frame f0 to f1, so the drop reads at phone size."""
    f = int(round(t * FPS)) + 1
    if f0 <= f <= f1:
        x, y = a[f]["drop"]
        u = (f - f0 + 0.5) / (f1 - f0 + 1)
        fx2d_extra._sparkle(cr, x + 6, y - 8, size * (0.6 + 0.4 * math.sin(math.pi * u)), (1, 1, 1), 1.0, rot=0.3)


def brim_safe_mask(frame_png, eyes, rx, ry):
    """An A8 mask for painting over Kai's eyes in the diorama close-up: soft ellipses (rx, ry) on the eyes, as
    fx2d_anime._cover_eye draws them, minus the cap's teal brim, which there sits on his eyes and must stay, and the
    hair strands beside them."""
    import numpy as np
    from scipy.ndimage import gaussian_filter
    im = np.asarray(Image.open(frame_png).convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    brim = (g - r > 40) & (b - r > 40)
    hair = (r - b > 18) & (r + g + b < 420)                       # brown hair (the iris is only spared off the eye)
    yy, xx = np.mgrid[0:im.shape[0], 0:im.shape[1]]
    m = np.zeros(im.shape[:2])
    core = np.zeros(im.shape[:2], bool)
    for ex, ey in eyes:
        d = np.sqrt(((xx - ex) / rx) ** 2 + ((yy - ey) / ry) ** 2)
        m = np.maximum(m, np.clip((1.0 - d) / 0.18, 0.0, 1.0))
        core |= (np.abs(xx - ex) <= rx * 0.72) & (d < 1.0)
    m *= 1.0 - gaussian_filter((brim | (hair & ~core)).astype(float), 1.2)
    surf = cairo.ImageSurface(cairo.FORMAT_A8, im.shape[1], im.shape[0])
    stride = surf.get_stride()
    buf = np.zeros((im.shape[0], stride), np.uint8)
    buf[:, :im.shape[1]] = np.round(np.clip(m, 0, 1) * 255).astype(np.uint8)
    surf.get_data()[:] = buf.tobytes()
    surf.mark_dirty()
    return surf


def masked_dot_eyes(cr, t, start, eyes, r, skin, mask, end=None):
    """fx2d_anime.dot_eyes (same 1.5 s window) with the skin painted through `mask` (brim_safe_mask)."""
    if not fx2d_anime._on(t, start, end, 1.5):
        return
    cr.set_source_rgba(*skin[:3], 1.0)
    cr.mask_surface(mask, 0, 0)
    for ex, ey in eyes:
        cr.arc(ex, ey, r, 0, 2 * math.pi)
        cr.set_source_rgba(*fx2d.INK)
        cr.fill()


def diorama_s20():
    """S20's deadpan in the diorama: the dot eyes on his eyes as rendered (the bone anchors sit ~25 px inside them in
    this close-up) and a cover that spares the brim, then the sweat drop, as in 3D; the "pff" is in the plate."""
    a = anchors("S20")
    _, _, tilt, eyes = face_geom(a, 50 / FPS)
    plate = os.path.join(BUILD, "S20", "0050.png")
    eyes = plate_eyes(plate, eyes, math.dist(*eyes) * 0.23)
    d = math.dist(*eyes)
    (lx, ly), (rx, ry) = eyes
    cx, cy, size, er = (lx + rx) / 2, (ly + ry) / 2, d * 2.6, d * 0.23
    skin = skin_near_eyes(os.path.join(BUILD, "S20", "0070.png"), eyes, er)
    mask = brim_safe_mask(plate, eyes, d * 0.35, d * 0.19)     # solid to the hair, which the mask spares
    return [(masked_dot_eyes, dict(start=43 / FPS, eyes=eyes, r=er * 0.24, skin=skin, mask=mask)),
            (fx2d_anime.sweat_drop, dict(start=52 / FPS, end=99, x=cx, y=cy, size=size, tilt=tilt))]


def tracked_terror(cr, t, a, start, size0, corr):
    """fx2d_anime.terror_eyes + sweat_drop following the face anchors every frame (a moving camera), with the eye
    correction measured on the plate (plate_eyes) scaled as the face grows."""
    (cx, cy), size, tilt, eyes = face_geom(a, t)
    k = size / size0
    eyes = tuple((ex + dx * k, ey + dy * k) for (ex, ey), (dx, dy) in zip(eyes, corr))
    cx, cy = (eyes[0][0] + eyes[1][0]) / 2, (eyes[0][1] + eyes[1][1]) / 2
    size = math.hypot(eyes[1][0] - eyes[0][0], eyes[1][1] - eyes[0][1]) * 2.6
    fx2d_anime.sweat_drop(cr, t, start - 0.2, end=99, x=cx, y=cy, size=size, tilt=tilt)
    fx2d_anime.terror_eyes(cr, t, start, end=99, x=cx, y=cy, size=size, eyes=eyes, er=size / 2.6 * 0.26 * 1.08,
                           tilt=tilt)


def _terror_on_plate(shot, a, t0):
    """(face size at t0, per-eye correction): measured on the rendered frame at t0 when the whites of his eyes show
    there, else the anchors' eyes spread 1.32x about their midpoint (the bone-based eye offsets are that much too
    narrow on this hero: 59 vs 78 px in the 3D S01, 26 vs ~35 px in the diorama S16)."""
    (cx, cy), size, tilt, eyes = face_geom(a, t0)
    png = os.path.join(BUILD, shot, f"{int(round(t0 * FPS)) + 1:04d}.png")
    fixed = plate_eyes(png, eyes, size / 2.6 * 0.26 * 1.08) if os.path.exists(png) else eyes
    if fixed == eyes:
        fixed = tuple((cx + (ex - cx) * 1.32, cy + (ey - cy) * 1.32) for ex, ey in eyes)
    return size, tuple((fx - ex, fy - ey) for (fx, fy), (ex, ey) in zip(fixed, eyes))


def ko_stars(cr, t, a, f0, f1, size=None):
    """Knocked-out stars: 3 small yellow cel stars with navy lines circling over his head on 2s (one orbit per 16
    frames, a tilted ellipse), following the head anchor; they fade out over the last 4 frames before f1."""
    f = int(round(t * FPS)) + 1
    if not f0 <= f <= f1:
        return
    (cx, cy), fsize, tilt, _ = face_geom(a, t)
    star = size or max(18.0, fsize * 0.45)
    rx = fsize * 0.62
    cx, cy = at(a, t, "crown")                                     # just past the top of his head
    cx = min(cx, 560 - rx - star * 0.6)                            # clear of the Shorts right rail
    fade = 1.0 if f < f1 - 4 else (f1 - f) / 4
    ph = 2 * math.pi * ((f - f0) // 2 * 2) / 16
    stars = []
    for i in range(3):
        ang = ph + i * 2 * math.pi / 3
        ex, ey = math.cos(ang) * rx, math.sin(ang) * rx * 0.24
        x = cx + ex * math.cos(tilt) - ey * math.sin(tilt)
        y = cy + ex * math.sin(tilt) + ey * math.cos(tilt)
        stars.append((math.sin(ang), x, y, star * (1 + 0.18 * (math.sin(ang) + 1) / 2)))
    for _, x, y, r in sorted(stars):                               # back to front
        cr.new_path()
        for j in range(10):
            rr = r / 2 if j % 2 == 0 else r / 2 * 0.45
            aa = -math.pi / 2 + j * math.pi / 5 + ph * 0.5
            cr.line_to(x + rr * math.cos(aa), y + rr * math.sin(aa))
        cr.close_path()
        cr.set_source_rgba(1.0, 0.85, 0.25, fade)
        cr.fill_preserve()
        cr.set_source_rgba(0.11, 0.1, 0.2, fade)
        cr.set_line_width(max(2.0, star * 0.12))
        cr.set_line_join(1)
        cr.stroke()


def diorama_overlays(shot):
    """The diorama cut's 2D (coordinator, 31 Oct): the slow push-ins of the locked shots (TP13), S17's drop glint and
    S18's realisation background with the 18% snap-zoom, as in 3D. S16's push is in 3D. S19 and S20 get the 3D cut's
    comic marks (coordinator, 31 Oct); S20's "pff" is already in the diorama plate (3D puffs)."""
    if shot == "S19":
        return cut_overlays(shot)
    if shot == "S20":
        return diorama_s20()
    a = anchors(shot)
    n = max(a)
    ex, ey = at(a, 0.0, "eyes")
    if shot == "S15b":                                            # dazed: the stars circle until near the end
        return [(ko_stars, dict(a=a, f0=1, f1=n - 8))]
    if shot in ("S01", "S16"):                                    # the pin-prick terror rhyme, as in 3D
        t0 = 0.0 if shot == "S01" else 41 / FPS
        size0, corr = _terror_on_plate(shot, a, t0 if shot == "S16" else 11 / FPS)
        out = [(tracked_terror, dict(a=a, start=t0, size0=size0, corr=corr))]
        if shot == "S01":
            out.append((push, dict(start=0.0, end=n / FPS, cx=ex, cy=ey, amount=0.06)))
        return out
    if shot == "S17":
        dx, dy = at(a, 20 / FPS, "drop")
        return [(drop_glint, dict(a=a, f0=17, f1=23)),
                (push, dict(start=0.0, end=n / FPS, cx=dx, cy=dy, amount=0.10))]
    if shot == "S18":
        ex, ey = at(a, 32 / FPS, "eyes")
        return [(comp.backdrop, dict(start=29 / FPS, end=99, fn=fx2d_anime.emotion_bg,
                                     args=dict(mood="realisation", cx=ex, cy=ey))),
                (glint, dict(start=32 / FPS, x=ex + 30, y=ey - 18, size=18)),
                (snap_zoom, dict(start=29 / FPS, cx=ex, cy=ey)),
                (push, dict(start=0.0, end=n / FPS, cx=ex, cy=ey, amount=0.06))]
    return []


def overlays(shot):
    """Shot-local overlays [(fn, kwargs)] for each shot."""
    return diorama_overlays(shot) if DIORAMA else cut_overlays(shot)


def cut_overlays(shot):
    """The 3D cut's overlays."""
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
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", CRF, "-preset", "slow",
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
