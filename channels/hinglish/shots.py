"""Shot machinery shared by the channel's videos (from video 1's fast-cut rebuild): cue timing, asset lookup,
photo pop-ins, the kraft checklist, the old-TV screen, and the cut list -> frame loop.

A video module lists SHOTS = [(line id, cue, draw function, "paper" | "slate"), ...]; a shot starts just before its
cue word is spoken and runs until the next one. Each draw function is fn(cr, t, tl, t0) with t0 = the shot's start.
"""
import os

from channel import ASSETS_ROOT
from poster import (CREAM, INK, MONO_FONT, _round, clamp, cross, draw_text, erase, finish, framed_photo, paper, photo,
                    photo_width, prog, push, rule, slate, tick)

CUT_LEAD = 0.12      # cut just before the word lands
MIN_SHOT = 0.5


def asset_finder(*folders):
    """find(name) -> the first file in these hinglish_assets folders whose name starts with `name` (originals
    skipped), or None if the photo search hasn't found one."""
    dirs = [os.path.join(ASSETS_ROOT, f) for f in folders]

    def find(name):
        for d in dirs:
            if os.path.isdir(d):
                for f in sorted(os.listdir(d)):
                    if f.startswith(name) and f.lower().endswith((".png", ".jpg", ".jpeg")) and "_orig" not in f:
                        return os.path.join(d, f)
        return None
    return find


def T(tl, bid, cue=None):
    """Time of a cue inside line `bid`: None = line start, str = that word, float = fraction of the line."""
    b = tl[bid]
    if cue is None:
        return b.start
    return b.at(cue) if isinstance(cue, str) else b.at(frac=cue)


def pic(cr, path_, cx, cy, h, t, t0, rot=0.0, flip=False, tint=None, alpha=1.0, frame=None):
    """Photo cut-out (or framed photo when `frame` = (w, h)) that pops up into place at t0."""
    if not path_:
        return
    p = prog(t, t0, 0.3)
    if frame:
        framed_photo(cr, path_, cx, cy + 50 * (1 - p), frame[0], frame[1], alpha=p * alpha, rot=rot)
    else:
        photo(cr, path_, cx, cy + 50 * (1 - p), h, alpha=p * alpha, rot=rot, flip=flip, tint=tint)


def tv(cr, tv_path, cx, cy, h, alpha=1.0):
    """The old CRT photo (toxoplasma2/old_tv.png, logo removed); returns its screen glass rectangle (measured on the
    photo) so a picture can be drawn into it."""
    photo(cr, tv_path, cx, cy, h, alpha=alpha)
    w = photo_width(tv_path, h)
    x0, y0 = cx - w / 2, cy - h / 2
    return x0 + 0.136 * w, y0 + 0.083 * h, 0.634 * w, 0.356 * h


def screen(cr, rect, alpha, on=1.0):
    """CRT picture area: pale glow when on; collapses to a line then a dot as `on` goes 1 -> 0."""
    sx, sy, sw_, sh_ = rect
    vy = max(0.02, clamp(on * 2 - 1)) if on < 1 else 1.0
    vx = clamp(on * 2) if on < 1 else 1.0
    cx, cy = sx + sw_ / 2, sy + sh_ / 2
    cr.set_source_rgba(0.80, 0.86, 0.82, alpha * (1 if on > 0 else 0))
    _round(cr, cx - sw_ * vx / 2, cy - sh_ * vy / 2, sw_ * vx, sh_ * vy, 30 * vy)
    cr.fill()


def checklist(cr, t, x, y, w, title, items, alpha=1.0, eraser=None):
    """Kraft card with a title and rows: (label, t_show, mark, t_mark), mark in {"tick", "cross", "erase", None}."""
    rows = len(items)
    h = 120 + 110 * rows
    p = prog(t, items[0][1] - 0.35, 0.3) * alpha
    if p <= 0:
        return
    cr.set_source_rgba(0, 0, 0, 0.2 * p)
    _round(cr, x + 8, y + 14, w, h, 16)
    cr.fill()
    cr.set_source_rgba(0.83, 0.72, 0.54, p)
    _round(cr, x, y, w, h, 16)
    cr.fill()
    draw_text(cr, title, x + 40, y + 34, 40, INK, p, MONO_FONT, tracking=4)
    for i, (label, t_show, mark, t_mark) in enumerate(items):
        ry = y + 150 + 110 * i
        q = prog(t, t_show, 0.25) * alpha
        if q <= 0:
            continue
        cr.set_source_rgba(*INK, 0.85 * q)
        cr.set_line_width(5)
        cr.rectangle(x + 40, ry - 32, 64, 64)
        cr.stroke()
        if mark == "erase":
            erase(cr, t, t_mark, label, x + 130, ry, 70, INK, dur=0.8, eraser=eraser, anchor="lm")
        else:
            draw_text(cr, label, x + 130, ry, 70, INK, q, anchor="lm")
        if mark == "tick":
            tick(cr, x + 48, ry - 4, 62, prog(t, t_mark, 0.3))
        elif mark == "cross":
            cross(cr, x + 72, ry, 56, prog(t, t_mark, 0.3))


def starts(tl, shots):
    out = []
    for k, (bid, cue, _, _) in enumerate(shots):
        if k == 0:
            out.append(0.0)
            continue
        s = T(tl, bid, cue)
        if cue is not None:
            s -= CUT_LEAD
        out.append(max(s, out[-1] + MIN_SHOT))
    return out


def shot_at(t, tl, shots):
    cached = getattr(tl, "_shot_starts", None)
    if cached is None:
        cached = tl._shot_starts = starts(tl, shots)
    k = max(i for i, s in enumerate(cached) if t >= s)
    return k, cached[k], cached[k + 1] if k + 1 < len(cached) else tl.total


def draw_frame(cr, t, tl, shots):
    """Background (paper, or dark slate for inside a body), a slow push-in, the shot, the bare rule, print texture."""
    k, t0, t1 = shot_at(t, tl, shots)
    _, _, fn, bg = shots[k]
    if bg == "slate":
        slate(cr)
    else:
        paper(cr, seed=1 + k % 3)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.04)
    fn(cr, t, tl, t0)
    cr.restore()
    rule(cr, color=CREAM if bg == "slate" else INK)
    finish(cr)
