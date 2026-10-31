"""The 2D shot compositor for "Cute Things Kill Here": Blender frames in, finished numbered PNGs out (the episode
timeline muxes them with ffmpeg).

    from channels.monsters import comp, fx2d, fx2d_extra
    snap = comp.Source("build/monsters/S08")                   # S08/0001.png ... and S08/subject/0001.png
    shots = [
        comp.Shot(comp.Source("build/monsters/S01"), 2.11, [(fx2d.hook_text, dict(start=0, end=1.9))]),
        comp.glitch_rewind(comp.Source("build/monsters/S01"), 1.66),
        comp.Shot(snap.hold(0.08, 0.6, insert=True), 0.9, [
            (comp.impact, dict(start=0.0, frames=2)),
            (comp.backdrop, dict(start=0.083, end=0.6, fn=fx2d_extra.burst_bg, args=dict(style="red")))],
            trans=comp.Wipe("blob", 0.45)),
    ]
    report = comp.render(shots, "build/monsters/ep01_frames",
                         overlays=[(fx2d.status_bar, dict(start=0.0, hits=[(30.1, 0.15)]))])
    # ffmpeg -framerate 24 -i build/monsters/ep01_frames/%05d.png ...

Sources: a folder of PNGs (any names, sorted), with an optional `subject/` folder of RGBA frames (the character
alone, look.subject_only). Operations return a new Source and work in source-local seconds: seq (trim), reverse,
hold (freeze one frame, replacing or inserting time), retime (slow motion by repeating frames: no blending, so the
on-3s look survives) and fit (resample to an exact length). A shot longer than its source holds the last frame.
Frames of another size (e.g. 360x640 test renders) are scaled to the canvas.

Overlays are (fn, kwargs) or (fn, kwargs, layer) and are called fn(cr, t, **kwargs): shot overlays get shot-local
t, global overlays (render(overlays=...)) get episode t. A function with a `ctx` parameter also gets the frame's
FrameCtx (its background and subject surfaces): impact and backdrop below use it. Layers:
- "fx" draws on the picture in order (full-frame effects allowed; impact and glitch read the pixels drawn so far);
- "hud" draws on a separate transparent layer composited on top; the layout check reads this layer;
- "caption" draws last, unchecked (captions belong in the caption band).
The default is "hud" for fx2d's HUD functions (HUD_FNS) and "fx" for everything else.

Transitions: a hard cut by default; Wipe(shape, dur) plays fx2d_extra.wipe over the first `dur` seconds of the
incoming shot while the outgoing shot holds its last finished frame.

Layout check (Shorts): HUD pixels must stay out of the right rail (x > 620, y 640-1180) and the caption band
(y 845-930). render() reports every shot and region that breaks it.

Sound: overlays cue m_* sounds through motion.engine.cue with episode times; render() returns the cues it
collected for motion.audio.build_soundtrack.

Run with FPS=24 in the environment (fx2d reads motion.engine.FPS at import); this module sets it if unset.
"""
import copy
import glob
import inspect
import math
import os
import time
from functools import lru_cache

os.environ.setdefault("FPS", "24")

import cv2  # noqa: E402
import numpy as np  # noqa: E402

from motion import engine  # noqa: E402
from motion.engine import H, W, cairo, cue  # noqa: E402
from channels.monsters import fx2d, fx2d_extra  # noqa: E402
from channels.monsters import sfx as _sfx  # noqa: E402,F401  (registers the m_* sounds, m_glitch included)

FPS = 24
CAPTION_BAND = (845, 930)
RAIL_X, RAIL_Y = 620, (640, 1180)
HUD_FNS = {"status_bar", "creature_tag", "choice_menu", "bond_popup", "rule_chip", "fact_card", "hud_boot",
           "hook_text"}
INK = (0.07, 0.06, 0.12)

if engine.FPS != FPS:
    print(f"comp: warning, motion.engine.FPS is {engine.FPS}; set FPS=24 before importing anything from motion")


# ---------------------------------------------------------------- frame sources

@lru_cache(maxsize=24)
def _load(path):
    img = cairo.ImageSurface.create_from_png(path)
    if (img.get_width(), img.get_height()) == (W, H):
        return img
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(out)
    cr.scale(W / img.get_width(), H / img.get_height())
    cr.set_source_surface(img, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    return out


class Source:
    """Frames from a Blender shot folder (and its optional subject/ pass), with a frame map that the operations
    rewrite. Times are in seconds of this source's current map; fps is the canvas rate (24)."""

    def __init__(self, folder, subject="auto", fps=FPS):
        self.folder = folder
        self.frames = sorted(glob.glob(os.path.join(folder, "*.png")))
        if not self.frames:
            raise FileNotFoundError(f"no PNG frames in {folder}")
        sub = os.path.join(folder, "subject") if subject == "auto" else subject
        self.subject = sorted(glob.glob(os.path.join(sub, "*.png"))) if sub and os.path.isdir(sub) else None
        if self.subject is not None and len(self.subject) != len(self.frames):
            raise ValueError(f"{folder}: {len(self.frames)} frames but {len(self.subject)} subject frames")
        self.fps = fps
        self.map = list(range(len(self.frames)))

    def _new(self, m):
        s = copy.copy(self)
        s.map = list(m)
        return s

    def _i(self, t):
        return int(round(t * self.fps))

    @property
    def duration(self):
        return len(self.map) / self.fps

    def seq(self, t0=0.0, t1=None):
        """Trim to [t0, t1)."""
        return self._new(self.map[self._i(t0): None if t1 is None else self._i(t1)])

    def reverse(self):
        return self._new(self.map[::-1])

    def hold(self, t0, t1, at=None, insert=False):
        """Freeze one frame (the one at `at`, default t0) from t0 to t1. insert=False replaces that stretch (the
        length stays the same); insert=True pauses and then carries on from the held frame (the length grows)."""
        a, b = self._i(t0), self._i(t1)
        f = self.map[min(len(self.map) - 1, self._i(t0 if at is None else at))]
        if insert:
            return self._new(self.map[:a] + [f] * (b - a) + self.map[a:])
        return self._new(self.map[:a] + [f] * (b - a) + self.map[b:])

    def retime(self, factor, t0=0.0, t1=None):
        """Slow motion (factor > 1) or fast (factor < 1) over [t0, t1) by repeating or skipping whole frames."""
        a = self._i(t0)
        b = len(self.map) if t1 is None else self._i(t1)
        part = self.map[a:b]
        n = max(1, int(round(len(part) * factor)))
        return self._new(self.map[:a] + [part[min(len(part) - 1, int(j / factor))] for j in range(n)] + self.map[b:])

    def fit(self, dur):
        """Resample to exactly `dur` seconds (nearest frame, no blending)."""
        n = max(1, self._i(dur))
        k = len(self.map) / n
        return self._new([self.map[min(len(self.map) - 1, int(j * k))] for j in range(n)])

    def get(self, i):
        """(background, subject or None) surfaces for output frame i of this source (the last frame holds)."""
        j = self.map[min(max(i, 0), len(self.map) - 1)]
        return _load(self.frames[j]), (_load(self.subject[j]) if self.subject else None)


class FrameCtx:
    """What a ctx-aware overlay can see: the shot's raw background and subject surfaces for this frame."""

    def __init__(self, bg, subject, shot, index):
        self.bg, self.subject, self.shot, self.index = bg, subject, shot, index


class Wipe:
    """A shape wipe into the shot that carries it (fx2d_extra.wipe): over its first `dur` seconds the incoming shot
    is revealed inside the growing shape while the outgoing shot holds its last frame."""

    def __init__(self, shape="iris", dur=0.45, mode="open", cx=W / 2, cy=H * 0.45, edge=(1.0, 0.84, 0.35), seed=0):
        self.shape, self.dur, self.mode, self.cx, self.cy, self.edge, self.seed = shape, dur, mode, cx, cy, edge, seed


class Shot:
    """src: a Source, a function src(cr, t) that paints the frame, or an RGB colour. dur defaults to the source's
    length. overlays: [(fn, kwargs)] or [(fn, kwargs, layer)] with shot-local times. trans: None (hard cut) or a
    Wipe."""

    def __init__(self, src, dur=None, overlays=(), trans=None, name=""):
        if dur is None:
            if not isinstance(src, Source):
                raise ValueError("a shot without a Source needs a duration")
            dur = src.duration
        self.src, self.dur, self.trans, self.name = src, dur, trans, name
        self.overlays = [_norm_overlay(o) for o in overlays]


def _norm_overlay(o):
    fn, kw = o[0], dict(o[1]) if len(o) > 1 else {}
    layer = o[2] if len(o) > 2 else ("hud" if getattr(fn, "__name__", "") in HUD_FNS else "fx")
    try:
        wants_ctx = "ctx" in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        wants_ctx = False
    return fn, kw, layer, wants_ctx


# ---------------------------------------------------------------- subject-aware effects

def _px(surf):
    surf.flush()
    return np.ndarray((surf.get_height(), surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :surf.get_width()]


def _surface(arr):
    """(surface, array): an ARGB32 surface over a (H, W, 4) uint8 premultiplied BGRA array. Keep the array alive
    while the surface is in use."""
    arr = np.ascontiguousarray(arr)
    s = cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, arr.shape[1], arr.shape[0],
                                           arr.shape[1] * 4)
    return s, arr


def _subject_centre(sub):
    a = _px(sub)[..., 3]
    ys, xs = np.nonzero(a[::4, ::4] > 128)
    if not len(xs):
        return W / 2, H * 0.45
    return float(xs.mean() * 4), float(ys.mean() * 4)


def impact(cr, t, start, frames=2, cx=None, cy=None, clear=0.2, lines=56, ctx=None, seed=0):
    """The impact frame from the subject pass: for `frames` frames the picture becomes a clean two-tone card, the
    background flat with radial lines bursting from the subject and the subject a crisp silhouette that keeps its
    own dark lines and eyes as the opposite tone. Frame 1 is white-on-black, frame 2 black-on-white. No grass or
    sky is thresholded. Without a subject pass it falls back to fx2d.impact_frame."""
    k = int(math.floor((t - start) * FPS + 1e-6))
    if not 0 <= k < frames:
        return
    sub = ctx.subject if ctx is not None else None
    if sub is None:
        fx2d.impact_frame(cr, t, start, frames=frames, seed=seed,
                          **({"cx": cx, "cy": cy} if cx is not None else {}))
        return
    cue("m_hit", t, start)
    dark = k % 2 == 0
    bgc, fgc = (INK, (1, 1, 1)) if dark else ((1, 1, 1), INK)
    if cx is None:
        cx, cy = _subject_centre(sub)
    cr.save()
    cr.set_source_rgb(*bgc)
    cr.paint()
    rng = np.random.default_rng([seed, k])
    cr.set_source_rgb(*fgc)
    for i in range(lines):
        ang = (i + rng.uniform(-0.4, 0.4)) * 2 * math.pi / lines
        r0 = H * clear * rng.uniform(0.85, 1.6)
        w = rng.uniform(6, 24) / 2
        dx, dy = math.cos(ang), math.sin(ang)
        px, py = -dy, dx
        cr.move_to(cx + dx * r0, cy + dy * r0)
        cr.line_to(cx + dx * 1600 + px * w * 8, cy + dy * 1600 + py * w * 8)
        cr.line_to(cx + dx * 1600 - px * w * 8, cy + dy * 1600 - py * w * 8)
        cr.close_path()
    cr.fill()
    cr.restore()
    s = _px(sub).astype(np.float32)
    a = s[..., 3] / 255.0
    lum = (0.114 * s[..., 0] + 0.587 * s[..., 1] + 0.299 * s[..., 2]) / np.maximum(a, 1e-3)
    ink = cv2.GaussianBlur(((lum < 75) & (a > 0.5)).astype(np.float32), (0, 0), 0.8)   # its lines and eyes
    cov = np.clip((a - 0.35) / 0.3, 0, 1)                                              # crisp silhouette edge
    solid = cv2.dilate((a > 0.97).astype(np.uint8), np.ones((7, 7), np.uint8)).astype(np.float32)
    cov *= solid                         # drops the soft contact shadow (look.blob_shadow is parented to the rig)
    out = np.zeros((H, W, 4), np.float32)
    for c, (f, b) in enumerate(zip(fgc[::-1], bgc[::-1])):                              # BGR order
        out[..., c] = (f * (1 - ink) + b * ink) * 255 * cov
    out[..., 3] = cov * 255
    sil, keep = _surface(out.astype(np.uint8))
    cr.set_source_surface(sil, 0, 0)
    cr.paint()
    del keep


def backdrop(cr, t, start, end, fn=fx2d_extra.burst_bg, args=None, ctx=None):
    """A full-frame background behind the subject from start to end: fn(cr, t, start, end, **args) paints it (e.g.
    fx2d_extra.burst_bg style "lines"/"red"/"sparkle", or fx2d.speed_lines with bg=True), then the subject pass is
    composited on top. Pair it with Source.hold to freeze the character while the background moves."""
    if t < start or t > end:
        return
    fn(cr, t, start, end, **(args or {}))
    if ctx is not None and ctx.subject is not None:
        cr.set_source_surface(ctx.subject, 0, 0)
        cr.paint()


def glitch(cr, t, start, end, strength=1.0, seed=0, sound=True):
    """A digital rewind glitch on the pixels drawn so far: RGB split, horizontal tears (some with a dropped
    channel), a few corrupted blocks, scanlines with a brightness flicker and a bright bar rolling down. Changes
    every frame; strongest in the first and last 0.25 s."""
    if t < start or t > end:
        return
    if sound:
        cue("m_glitch", t, start, end - start)
    surf = cr.get_target()
    if not isinstance(surf, cairo.ImageSurface):
        return
    a = _px(surf)
    hh, ww = a.shape[:2]                                           # any frame size: sizes and offsets scale with
    k = ww / W                                                     # the width (k = 1 on the 720x1280 canvas)
    f = int(math.floor((t - start) * FPS + 1e-6))
    r = np.random.default_rng([seed, f, 97])
    el, dur = t - start, max(end - start, 1e-3)
    edge = max(0.0, 1 - min(el, dur - el) / 0.25)
    env = strength * (0.45 + 0.35 * edge + 0.3 * (r.random() < 0.25))
    img = a.copy()
    dx = max(1, int(r.integers(4, 15) * env * k))
    img[..., 2] = np.roll(a[..., 2], dx, axis=1)                  # red right
    img[..., 0] = np.roll(a[..., 0], -dx, axis=1)                 # blue left
    for _ in range(int(r.integers(2, 6) + 4 * env)):
        y0, h = int(r.integers(0, hh - int(8 * k))), int(int(r.integers(4, 64)) * k)
        img[y0:y0 + h] = np.roll(img[y0:y0 + h], int(r.integers(-130, 130) * env * k), axis=1)
        if r.random() < 0.3:
            img[y0:y0 + h, :, int(r.integers(0, 3))] = 0
    for _ in range(int(r.integers(0, 5) * env)):
        bx, by = int(r.integers(0, ww - int(48 * k))), int(r.integers(0, hh - int(48 * k)))
        s = int(int(r.integers(16, 48)) * k)
        img[by:by + s, bx:bx + s, :3] = img[by:by + s, bx:bx + s, :3].mean(axis=(0, 1)).astype(np.uint8)
    out = img.astype(np.float32)
    out[(np.arange(hh) // max(1, int(round(2 * k)))) % 2 == 0] *= 0.82   # scanlines
    out *= r.uniform(0.9, 1.06)                                    # flicker
    bar = int((el * 900 * k) % (hh + int(200 * k))) - int(100 * k)
    out[max(0, bar):max(0, bar + int(36 * k)), :, :3] += 28
    a[..., :3] = np.clip(out[..., :3], 0, 255).astype(np.uint8)
    a[..., 3] = 255
    surf.mark_dirty()


def glitch_rewind(src, dur=1.7, overlays=(), strength=1.0, seed=0, name="rewind", trans=None):
    """A shot that plays `src` backwards, squeezed into `dur` seconds, under the rewind glitch (S02)."""
    return Shot(src.reverse().fit(dur), dur, [(glitch, dict(start=0.0, end=dur, strength=strength, seed=seed))]
                + list(overlays), trans=trans, name=name)


# ---------------------------------------------------------------- rendering

def _blank():
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)


def _call(cr, fn, kw, wants_ctx, t, ctx):
    if wants_ctx:
        fn(cr, t, ctx=ctx, **kw)
    else:
        fn(cr, t, **kw)


def _shot_frame(shot, i):
    """(picture with fx overlays, hud layer, caption layer) for local frame i of a shot."""
    t = i / FPS
    pic = _blank()
    cr = cairo.Context(pic)
    bg = sub = None
    if isinstance(shot.src, Source):
        bg, sub = shot.src.get(i)
        cr.set_source_surface(bg, 0, 0)
        cr.paint()
    elif callable(shot.src):
        shot.src(cr, t)
    else:
        cr.set_source_rgb(*shot.src[:3])
        cr.paint()
    ctx = FrameCtx(bg, sub, shot, i)
    hud = cap = None
    for fn, kw, layer, wants_ctx in shot.overlays:
        if layer == "fx":
            _call(cr, fn, kw, wants_ctx, t, ctx)
        else:
            if layer == "hud":
                hud = hud or _blank()
                target = hud
            else:
                cap = cap or _blank()
                target = cap
            _call(cairo.Context(target), fn, kw, wants_ctx, t, ctx)
    return pic, hud, cap


def _over(dst, src):
    if src is not None:
        cr = cairo.Context(dst)
        cr.set_source_surface(src, 0, 0)
        cr.paint()


def layout_check(hud):
    """Pixels of a HUD layer inside the Shorts right rail and the caption band: {region: count}."""
    if hud is None:
        return {}
    a = _px(hud)[..., 3]
    bad = {}
    rail = int((a[RAIL_Y[0]:RAIL_Y[1], RAIL_X:] > 16).sum())
    band = int((a[CAPTION_BAND[0]:CAPTION_BAND[1]] > 16).sum())
    if rail:
        bad["right rail"] = rail
    if band:
        bad["caption band"] = band
    return bad


def render(shots, out_dir, fps=FPS, overlays=(), check=True, frames=None, write=True, verbose=True):
    """Composite the shots into out_dir/00001.png ... (ffmpeg: -framerate 24 -i out_dir/%05d.png). overlays are
    global (episode time; e.g. a status_bar that carries across shots). frames=(first, last) renders a range only
    (0-based, inclusive; for parallel jobs - sound cues are only complete in a full sequential render). Returns
    {"frames", "seconds", "ms_per_frame", "events", "layout": [(shot, region, first_frame, last_frame, max_px)]}."""
    if fps != FPS:
        raise ValueError("the compositor runs at 24 fps (the anime timing and fx2d both assume it)")
    glob_ov = [_norm_overlay(o) for o in overlays]
    lengths = [max(1, int(round(s.dur * fps))) for s in shots]
    starts = np.concatenate([[0], np.cumsum(lengths)]).astype(int)
    total = int(starts[-1])
    first, last = frames if frames else (0, total - 1)
    os.makedirs(out_dir, exist_ok=True)
    n0 = len(engine.EVENTS)
    issues = {}
    held = {}                                                       # last finished frame of each shot, for wipes
    t_start = time.time()
    for g in range(first, last + 1):
        s = int(np.searchsorted(starts, g, side="right") - 1)
        shot, i = shots[s], g - int(starts[s])
        engine._state["frame"] = g
        engine._state["offset"] = float(starts[s] / fps)
        pic, hud, cap = _shot_frame(shot, i)
        full = _blank()
        _over(full, pic)
        _over(full, hud)
        w = shot.trans
        if isinstance(w, Wipe) and s > 0 and i / fps < w.dur:
            if s - 1 not in held:                                  # a range render that starts mid-wipe
                j = lengths[s - 1] - 1
                engine._state["offset"] = float(starts[s - 1] / fps)
                p0, h0, _ = _shot_frame(shots[s - 1], j)
                held[s - 1] = _blank()
                _over(held[s - 1], p0)
                _over(held[s - 1], h0)
                engine._state["offset"] = float(starts[s] / fps)
            if i == 0:
                cue("m_whoosh", 0.0, 0.0)
            frame = _blank()
            _over(frame, held[s - 1])
            fx2d_extra.wipe(cairo.Context(frame), (i + 1) / (w.dur * fps), w.shape, nxt=full, cx=w.cx, cy=w.cy,
                            edge=w.edge, mode=w.mode, seed=w.seed)
        else:
            frame = full
        if i == lengths[s] - 1:                                    # keep a copy before the global overlays
            held[s] = _blank()
            _over(held[s], frame)
            held.pop(s - 2, None)
        engine._state["offset"] = 0.0
        T = g / fps
        ghud = gcap = None
        gctx = FrameCtx(*(shot.src.get(i) if isinstance(shot.src, Source) else (None, None)), shot, i)
        fcr = cairo.Context(frame) if glob_ov else None
        for fn, kw, layer, wants_ctx in glob_ov:
            if layer == "fx":
                _call(fcr, fn, kw, wants_ctx, T, gctx)
            elif layer == "hud":
                ghud = ghud or _blank()
                _call(cairo.Context(ghud), fn, kw, wants_ctx, T, gctx)
            else:
                gcap = gcap or _blank()
                _call(cairo.Context(gcap), fn, kw, wants_ctx, T, gctx)
        if ghud is not None or cap is not None or gcap is not None:
            if frame is full:
                frame = _blank()
                _over(frame, full)
            _over(frame, ghud)
            _over(frame, cap)
            _over(frame, gcap)
        if check:
            for name, layer in ((shot.name or f"shot {s + 1}", hud), ("global overlays", ghud)):
                for region, n in layout_check(layer).items():
                    key = (name, region)
                    f0, _, mx = issues.get(key, (g, g, 0))
                    issues[key] = (f0, g, max(mx, n))
        if write:
            px = _px(frame)
            cv2.imwrite(os.path.join(out_dir, f"{g + 1:05d}.png"), px[..., :3], [cv2.IMWRITE_PNG_COMPRESSION, 1])
        if verbose and (g - first) % 48 == 0:
            print(f"comp: frame {g + 1}/{total} ({shot.name or f'shot {s + 1}'})", flush=True)
    secs = time.time() - t_start
    n = last - first + 1
    layout = [(k[0], k[1], v[0], v[1], v[2]) for k, v in issues.items()]
    if verbose:
        print(f"comp: {n} frames in {secs:.1f} s ({1000 * secs / n:.0f} ms per frame)")
        for name, region, f0, f1, mx in layout:
            print(f"comp: LAYOUT {name}: HUD in the {region}, frames {f0 + 1}-{f1 + 1} (up to {mx} px)")
    return dict(frames=n, seconds=secs, ms_per_frame=1000 * secs / n, events=engine.EVENTS[n0:], layout=layout)
