"""Manga videos (owner, 28 Oct 2026: "Make manga like video like showing manga page and explaining take manga pages
from manga creation chat ... showing manga panel and saying what that specific character says in his voice and
explaining some in Narrator voice ... zooming in and zooming out from panel to panel").

The pages come from the manga creation chat (repo tejassparky2/Manga, story/chapterNN/script.yaml + its rendered
pages), copied into assets/manga/SET/chNN/page_NN.jpg. Panel boxes are computed exactly as that repo's
tools/manga/layout.py does (rows top to bottom, cells right to left), so the camera always lands on a real panel.

An episode is a list of beats: dict(id, page, panel, text, speaker, ...). panel = 0 shows the whole page. The camera
eases from one beat's panel to the next (zoom out to the page and back in when the page turns), the other panels dim,
the narrator explains in his own voice and every character speaks in theirs.
"""
import functools
import json
import math
import os

import cairo
import cv2
import numpy as np

from motion.engine import W, H, clamp01
from channels.horror import hud2d
from channels.horror.toon2d import glow
from channels.stories import anime2d as AN

PAGE_W, PAGE_H = 1600, 2264                                   # tejassparky2/Manga tools/manga/layout.py
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 80, 90, 100
HGAP, VGAP = 24, 32
V = H > W
EASE = 0.5                                                    # seconds for the camera to move between panels
TURN = 0.55                                                   # seconds for a page turn


def panel_rects(rows):
    """[(x0, y0, x1, y1)] in reading order for a page's rows (same arithmetic as the manga repo's layout.py)."""
    content_w = PAGE_W - 2 * MARGIN_X
    content_h = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
    total_h = sum(r[0] for r in rows)
    avail_h = content_h - VGAP * (len(rows) - 1)
    rects, y = [], MARGIN_TOP
    for height_weight, cells in rows:
        h = round(avail_h * height_weight / total_h)
        avail_w = content_w - HGAP * (len(cells) - 1)
        x_right = PAGE_W - MARGIN_X
        for w_weight in cells:
            w = round(avail_w * w_weight / sum(cells))
            rects.append((x_right - w, y, x_right, y + h))
            x_right -= w + HGAP
        y += h + VGAP
    return rects


def frame_box():
    """Where the page or panel sits on the canvas (the captions live below it on 9:16)."""
    return (24, 150, W - 24, 1010) if V else (40, 60, W - 40, H - 120)


def smooth(k):
    k = clamp01(k)
    return k * k * (3 - 2 * k)


class Manga:
    """One chapter's pages and their panel boxes."""

    def __init__(self, folder, rows_by_page):
        self.folder = folder                                  # e.g. assets/manga/dma/ch01
        self.rows = rows_by_page                              # {page: rows}
        mf = os.path.join(AN.ROOT, folder, "manifest.json")   # the manga chat's own panel boxes, when exported
        self.boxes = {int(k): [tuple(q["box"]) for q in v["panels"]]
                      for k, v in json.load(open(mf))["pages"].items()} if os.path.exists(mf) else {}

    def path(self, page):
        for ext in ("jpg", "png"):
            p = os.path.join(self.folder, f"page_{page:02d}.{ext}")
            if os.path.exists(os.path.join(AN.ROOT, p)):
                return p
        raise FileNotFoundError(f"{self.folder}/page_{page:02d}")

    def rect(self, page, panel, pad=18):
        if not panel:
            return (0, 0, PAGE_W, PAGE_H)
        x0, y0, x1, y1 = (self.boxes.get(page) or panel_rects(self.rows[page]))[panel - 1]
        return (x0 - pad, y0 - pad, x1 + pad, y1 + pad)


def cam_for(rect, push=0.0):
    """(scale, centre x, centre y) that fits a page rect into the frame box, pushed in by `push`."""
    fx0, fy0, fx1, fy1 = frame_box()
    x0, y0, x1, y1 = rect
    s = min((fx1 - fx0) / (x1 - x0), (fy1 - fy0) / (y1 - y0)) * (1 + push)
    return s, (x0 + x1) / 2, (y0 + y1) / 2


def lerp_cam(a, b, k):
    k = smooth(k)
    return (math.exp(math.log(a[0]) + (math.log(b[0]) - math.log(a[0])) * k), a[1] + (b[1] - a[1]) * k,
            a[2] + (b[2] - a[2]) * k)


@functools.lru_cache(maxsize=8)
def _backdrop(path):
    """The page blurred and darkened to fill the canvas behind it."""
    a = cv2.imread(os.path.join(AN.ROOT, path))
    k = max(W / a.shape[1], H / a.shape[0]) * 1.15
    a = cv2.resize(a, (int(a.shape[1] * k), int(a.shape[0] * k)), interpolation=cv2.INTER_AREA)
    y, x = (a.shape[0] - H) // 2, (a.shape[1] - W) // 2
    a = cv2.GaussianBlur(a[y:y + H, x:x + W], (0, 0), 18)
    a = (a.astype(np.float32) * 0.32).astype(np.uint8)
    return AN._surface_from_rgba(np.dstack([a[..., ::-1], np.full(a.shape[:2], 255, np.uint8)]))


def draw_page(cr, book, page, cam, spot=None, spot_k=0.0, dx=0.0, shake=(0.0, 0.0)):
    """The page under camera `cam`; everything but `spot` (a page rect) dimmed by spot_k."""
    fx0, fy0, fx1, fy1 = frame_box()
    s, cx, cy = cam
    ox, oy = (fx0 + fx1) / 2 + dx + shake[0], (fy0 + fy1) / 2 + shake[1]
    surf = AN.image(book.path(page))
    k = surf.get_width() / PAGE_W                              # pages may be stored at another size
    cr.save()
    cr.translate(ox, oy)
    cr.scale(s, s)
    cr.translate(-cx, -cy)
    cr.set_source_rgba(0, 0, 0, 0.5)                           # a soft shadow under the paper
    cr.rectangle(10, 14, PAGE_W, PAGE_H)
    cr.fill()
    cr.save()
    cr.scale(1 / k, 1 / k)
    cr.set_source_surface(surf, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()
    if spot and spot_k > 0:                                   # dim the other panels
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.rectangle(-4000, -4000, PAGE_W + 8000, PAGE_H + 8000)
        x0, y0, x1, y1 = spot
        cr.rectangle(x0, y0, x1 - x0, y1 - y0)
        cr.set_source_rgba(0.02, 0.02, 0.04, 0.62 * spot_k)
        cr.fill()
        cr.set_fill_rule(cairo.FILL_RULE_WINDING)
        cr.set_source_rgba(1, 1, 1, 0.55 * spot_k)
        cr.set_line_width(4 / s)
        cr.rectangle(x0 + 6, y0 + 6, x1 - x0 - 12, y1 - y0 - 12)
        cr.stroke()
    cr.restore()


class Reader:
    """Turns an episode's beats into camera moves; `draw(cr, t, tl)` paints one frame."""

    def __init__(self, book, beats, push=0.05):
        self.book, self.beats, self.push = book, beats, push
        self._plan = None

    def script(self, **narrator_gaps):
        """The timeline SCRIPT: one entry per beat; a page turn gets a longer gap so the turn happens in silence."""
        out, prev = [], None
        for b in self.beats:
            d = dict(id=b["id"], scene=f"p{b['page']}", text=b["text"])
            if b.get("speaker"):
                d["speaker"] = b["speaker"]
            if b.get("hold"):                                 # a silent beat (a title card over the page)
                d["hold"] = b["hold"]
            gap = b.get("gap", 0.25)
            if prev is not None and b["page"] != prev:
                gap = max(gap, TURN + 0.45)
            d["gap"] = gap
            out.append(d)
            prev = b["page"]
        return out

    def _rect(self, b):
        """The page rect a beat looks at: its panel, or a part of it when the beat gives a page-pixel `box`."""
        return b["box"] if b.get("box") else self.book.rect(b["page"], b["panel"])

    def plan(self, tl):
        """Each beat with t0 (when the camera starts moving to it); a page turn starts as soon as the last line of
        the old page ends."""
        if self._plan is None:
            p, prev = [], None
            for b in self.beats:
                tb = tl.by_id[b["id"]]
                turn = prev is not None and b["page"] != prev
                t0 = tb.start - tb.gap if turn else tb.start - min(EASE, tb.gap) - 0.05
                p.append(dict(b, t0=t0, start=tb.start, end=tb.end, turn=turn))
                prev = b["page"]
            self._plan = p
        return self._plan

    def current(self, t, tl):
        p = self.plan(tl)
        k = max([i for i, b in enumerate(p) if b["t0"] <= t] or [0])
        return k, p

    def draw(self, cr, t, tl):
        k, p = self.current(t, tl)
        b = p[k]
        prev = p[k - 1] if k else None
        book = self.book
        rect = self._rect(b)
        nxt = p[k + 1]["t0"] if k + 1 < len(p) else tl.total + 2
        hold = clamp01((t - b["start"]) / max(0.5, nxt - b["start"]))
        target = cam_for(rect, self.push * hold)
        shake = (0.0, 0.0)
        if b.get("impact") and b["start"] - 0.05 <= t < b["start"] + 0.35:
            a = 14 * (1 - (t - b["start"]) / 0.4)
            shake = (a * math.sin(t * 91), a * math.cos(t * 77))
        cr.set_source_surface(_backdrop(book.path(b["page"])), 0, 0)
        cr.paint()
        full = cam_for(book.rect(b["page"], 0))
        if b["turn"] and t < b["t0"] + TURN:                   # the page turns (next page comes in from the left)
            e = smooth((t - b["t0"]) / TURN)
            draw_page(cr, book, prev["page"], cam_for(book.rect(prev["page"], 0)), dx=W * 1.02 * e)
            draw_page(cr, book, b["page"], full, dx=W * 1.02 * (e - 1))
            cr.set_source_rgba(0, 0, 0, 0.3 * math.sin(math.pi * e))
            cr.paint()
            return
        if b["turn"] or not prev:                             # from the whole page in to this beat's panel
            a0 = b["t0"] + TURN if b["turn"] else 0.0
            z = clamp01((t - a0) / max(0.25, b["start"] - a0))
            cam = lerp_cam(full, target, z) if b["panel"] else target
            draw_page(cr, book, b["page"], cam, rect if b["panel"] else None, smooth(z), shake=shake)
            return
        src = cam_for(self._rect(prev), self.push)
        m = clamp01((t - b["t0"]) / EASE)
        cam = lerp_cam(src, target, m)
        if b["panel"]:
            spot, sk = rect, (1.0 if prev["panel"] else smooth(m))
        else:
            spot = self._rect(prev) if prev["panel"] else None
            sk = 1 - smooth(m)
        draw_page(cr, book, b["page"], cam, spot, sk, shake=shake)

    def speaker(self, t, tl):
        """The name of whoever is talking now (None for the narrator)."""
        for b in self.plan(tl):
            tb = tl.by_id[b["id"]]
            if tb.start <= t <= tb.end + 0.15:
                return b.get("name") or (b.get("speaker") or "").upper() or None
        return None


def name_chip(cr, t, name, y=None, col=hud2d.RED):
    """A small speaker label over the captions (who is talking)."""
    if not name:
        return
    y = y if y is not None else (1062 if V else H - 96)
    w = hud2d.text_width(cr, name, 30, hud2d.ROUND) + 40
    cr.save()
    cr.translate(W / 2 - w / 2, y - 30)
    hud2d.rrect(cr, 0, 0, w, 42, 21)
    cr.set_source_rgba(*col[:3], 0.95)
    cr.fill()
    hud2d._text(cr, name, w / 2, 31, 30, (1, 1, 1, 1), hud2d.ROUND, "center")
    cr.restore()


def series_chip(cr, text):
    """The series label at the top of the frame."""
    hud2d._text(cr, text, W / 2, 60 if V else 34, 26 if V else 20, (1, 0.85, 0.4, 0.95), hud2d.ROUND, "center",
                outline=(0, 0, 0, 1), ow=4)


def glow_panel(cr, k):
    if k > 0:
        glow(cr, W / 2, H / 2, W, (1, 1, 1), 0.05 * k)
