"""Camera beats for the puppet reels (owner, 14 Nov 2026: "correct from next reel the same shot is still for many
seconds and video feels slow"; videos 25-26 held one framing for 6-11 s). Inside a shot the camera cuts to a new
framing at every new script line, and adds more cuts so no framing is held longer than MAX_HOLD seconds. Each cut is
a fast punch (0.14 s) between framings, then a slow push-in until the next one.

Use in a scene module's draw():
    z, (fx, fy) = camera_beats.camera(tl, t, t0, t1, opt)
    cr.translate(fx, fy); cr.scale(z, z); cr.translate(-fx, -fy)
A SHOTS entry may give its own framings: opt["frames"] = [(zoom, (x, y)), ...], zooming about (x, y) (the point stays
where it is on screen and everything around it grows). Without them: the shot's own zoom/focus (wide), then a
punch-in left of the focus, then one right of it, in turn.
"""
MAX_HOLD = 2.6        # seconds a framing may be held
PUNCH = 0.14          # the cut's own length (a quick punch, not a slow zoom)
DRIFT = 0.035         # slow push-in during a hold


def frames(opt):
    if opt.get("frames"):
        return opt["frames"]
    z0 = opt.get("z", (1.0, 1.03))[0]
    fx, fy = opt.get("focus", (540, 1060))
    return [(z0, (fx, fy)), (z0 * 1.2, (fx - 150, fy + 60)), (z0 * 1.16, (fx + 150, fy + 40))]


def beats(tl, t0, t1, max_hold=MAX_HOLD):
    """Cut times inside a shot: its start, every line start inside it, and extra cuts that split long holds."""
    cuts = [t0] + [b.start - 0.05 for b in tl.beats if t0 + 0.8 < b.start < t1 - 0.8]
    out = []
    for a, b in zip(cuts, cuts[1:] + [t1]):
        n = max(1, int((b - a) / max_hold + 0.999))
        out += [a + (b - a) * k / n for k in range(n)]
    return out


def camera(tl, t, t0, t1, opt):
    """(zoom, (fx, fy)) at time t of the shot running t0..t1."""
    key = (round(t0, 3), round(t1, 3))
    cache = getattr(tl, "_cam_beats", None)
    if cache is None:
        cache = tl._cam_beats = {}
    if key not in cache:
        cache[key] = beats(tl, t0, t1)
    cuts = cache[key]
    fr = frames(opt)
    i = max(k for k, c in enumerate(cuts) if c <= t) if t >= cuts[0] else 0
    z1, (x1, y1) = fr[i % len(fr)]
    z0, (x0, y0) = fr[(i - 1) % len(fr)] if i > 0 else fr[0]
    u = min(1.0, max(0.0, (t - cuts[i]) / PUNCH)) if i > 0 else 1.0
    u = u * u * (3 - 2 * u)
    nxt = cuts[i + 1] if i + 1 < len(cuts) else t1
    drift = 1 + DRIFT * min(1.0, max(0.0, (t - cuts[i]) / max(0.5, nxt - cuts[i])))
    z = (z0 + (z1 - z0) * u) * drift
    return z, (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)
