"""Satsuei (撮影): the anime compositing pass, applied to a finished cairo frame with numpy + OpenCV.

Anime gets much of its look in compositing, after the cels are painted: a soft diffusion glow, light gradients laid
over the cels, a little chromatic aberration at the edges and film grain (research_notes/CPU anime animation
pipeline/anime_look_techniques.md, section 5). Blurs run at quarter resolution, so the whole pass costs ~0.1-0.2 s per
frame instead of seconds.

    satsuei.apply(cr, t, glow=0.22, light=((0.85, 0.1), (1.0, 0.85, 0.7), 0.18), ca=1.0, grain=0.035)

Call it from a scene's draw() after the picture and before captions / HUD, so text stays crisp.
"""
import functools

import cv2
import numpy as np

cv2.setNumThreads(1)          # frames are already rendered one process per core


@functools.lru_cache(maxsize=4)
def _ca_maps(w, h, px):
    """Remap grids that scale the frame about its centre by +-px pixels at the corners (red out, blue in)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = (w - 1) / 2, (h - 1) / 2
    k = px / max(cx, cy)
    out = []
    for s in (1 - k, 1 + k):                   # red sampled from inside (spreads outward), blue the other way
        out.append(((xx - cx) * s + cx, (yy - cy) * s + cy))
    return out


@functools.lru_cache(maxsize=8)
def _grain_tile(w, h, n):
    rng = np.random.default_rng(1000 + n)
    g = rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32)
    return cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)[..., None]


def _light(w, h, pos, col, amt):
    """A soft radial light gradient (screen blend), e.g. sun through a window. pos is in 0..1 frame units."""
    yy, xx = np.ogrid[0:h, 0:w]
    d = np.sqrt(((xx / w - pos[0]) * (w / h)) ** 2 + (yy / h - pos[1]) ** 2)
    m = np.clip(1 - d / 0.9, 0, 1) ** 2 * amt
    return m[..., None].astype(np.float32) * np.array(col[::-1], np.float32)     # BGR


@functools.lru_cache(maxsize=8)
def _light_cached(w, h, pos, col, amt):
    return _light(w, h, pos, col, amt)


def apply(cr, t, glow=0.22, threshold=0.55, light=None, shade=None, ca=1.0, grain=0.035):
    """Composite the frame under `cr` in place.

    glow:   strength of the diffusion (bright areas blurred and screened back over the frame)
    light:  (pos, rgb, amount) soft light gradient screened over the frame, or None
    shade:  (pos, rgb, amount) a multiply gradient (darkens away from pos), or None
    ca:     chromatic aberration in pixels at the frame corners (0 = off)
    grain:  film grain strength (0 = off); changes every 2 frames at 24 fps like anime's held cels
    """
    surf = cr.get_target()
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    buf = np.ndarray((h, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :w]
    img = buf[..., :3].astype(np.float32) * (1 / 255)
    if glow:
        small = cv2.resize(img, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
        bright = np.clip((small - threshold) / (1 - threshold), 0, 1)
        soft = cv2.GaussianBlur(bright, (0, 0), 5) + 0.6 * cv2.GaussianBlur(bright, (0, 0), 14)
        soft = cv2.resize(soft, (w, h), interpolation=cv2.INTER_LINEAR)
        img = 1 - (1 - img) * (1 - np.clip(glow * soft, 0, 1))
    if light:
        img = 1 - (1 - img) * (1 - _light_cached(w, h, *light))
    if shade:
        pos, col, amt = shade
        m = 1 - _light_cached(w, h, pos, (1.0, 1.0, 1.0), 1.0)[..., :1]          # 0 near pos, 1 far away
        img = img * (1 - amt * m * (1 - np.array(col[::-1], np.float32)))
    if ca:
        (rx, ry), (bx, by) = _ca_maps(w, h, float(ca))
        r = cv2.remap(img[..., 2], rx, ry, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        b = cv2.remap(img[..., 0], bx, by, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        img = np.dstack((b, img[..., 1], r))
    if grain:
        img = img + grain * _grain_tile(w, h, int(t * 12) % 8) * (0.35 + 0.65 * img * (1 - img) * 4)
    buf[..., :3] = np.clip(img * 255 + 0.5, 0, 255).astype(np.uint8)
    surf.mark_dirty()
