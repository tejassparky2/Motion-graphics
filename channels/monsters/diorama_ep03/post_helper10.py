"""2D pass and encode for helper 10's Episode 3 shots (DIORAMA_EP03.md), drawn with cairo over the Blender frames.

    S12 (the orbit, on helper 4's S11 stage, in post_helper4's S11 style): the coral light's soft bloom; a soft glow
        line from the light to the moth's back all the way round (its back always faces the light); a dotted trail
        tracing the ring it flies (older dots dimmer, the far side of the ring fainter); a faint dark hill-and-grass
        silhouette across the bottom (below the caption band). No text.
    S14 (the flip): a little dust puff where each moth lands on its back (on 2s: a squashed burst of soft dust balls
        and a flat ring that spreads and fades over ~10 frames), bigger and clearer for the first three plops. The
        mark's glow is helper 9's 2D pass (post_helper9.mark) from S14_mark.json, if the coordinator wants it on top.

    FPS=24 /home/user/tools/mgvenv/bin/python channels/monsters/diorama_ep03/post_helper10.py post S12 RAW OUT
    FPS=24 /home/user/tools/mgvenv/bin/python channels/monsters/diorama_ep03/post_helper10.py encode S12 OUT
    FPS=24 /home/user/tools/mgvenv/bin/python channels/monsters/diorama_ep03/post_helper10.py still S12 F PNG OUT
"""
import glob
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)
BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
CORAL, HOT = (1.0, 0.52, 0.40), (1.0, 0.86, 0.78)
DUST = (0.86, 0.84, 0.95)                      # moonlit dust (pale, a little blue)


def _cairo():
    from motion.engine import cairo
    return cairo


def _glow(cr, x, y, r, col, a=1.0):
    cairo = _cairo()
    if r <= 0 or a <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col[:3], a)
    g.add_color_stop_rgba(0.35, *col[:3], a * 0.35)
    g.add_color_stop_rgba(1, *col[:3], 0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def _scale(img):
    """Frames may be half-scale stills: draw in 720x1280 coordinates either way."""
    return img.get_width() / 720.0


# ---------------------------------------------------------------- S12
def _ground(cr):
    """post_helper4's S11 hill-and-grass silhouette across the bottom (from y ~985, clear of the caption band)."""
    top = 985.0
    cr.save()
    cr.new_path()
    cr.move_to(-10, 1290)
    for x in range(-10, 740, 10):
        cr.line_to(x, top + 22 * math.sin(x / 140.0) + 10 * math.sin(x / 47.0 + 1.3))
    cr.line_to(740, 1290)
    cr.close_path()
    cr.set_source_rgba(0.035, 0.05, 0.11, 1.0)
    cr.fill()
    rnd = random.Random(7)
    for _ in range(70):
        x = rnd.uniform(-5, 725)
        y = top + 22 * math.sin(x / 140.0) + 10 * math.sin(x / 47.0 + 1.3) + 3
        h, lean = rnd.uniform(10, 30), rnd.uniform(-7, 7)
        cr.new_path()
        cr.move_to(x - 2.5, y)
        cr.line_to(x + lean, y - h)
        cr.line_to(x + 2.5, y)
        cr.close_path()
        cr.fill()
    cr.restore()


def _s12(cr, f, A):
    cairo = _cairo()
    g = A[f]
    _ground(cr)
    # the trail: its flight so far as soft dots (the last lap and a bit), older dimmer; dots on the far side of the
    # ring (higher on screen than the ring's centre line, behind the light's vertical) a little fainter
    ys = [A[k]["body"][1] for k in A]
    mid = (min(ys) + max(ys)) / 2
    for j in range(f - 1, 3, -3):
        if j > 52:
            continue
        g0 = A.get(f - j)
        if g0 is None:
            continue
        x, y = g0["body"][:2]
        a = (0.16 + 0.34 * (1 - j / 52.0)) * (0.65 if y < mid else 1.0)
        _glow(cr, x, y, 12.0, (0.85, 0.88, 1.0), a)
        cr.new_path()
        cr.arc(x, y, 4.0, 0, 2 * math.pi)
        cr.set_source_rgba(0.9, 0.92, 1.0, min(1.0, a * 1.8))
        cr.fill()
    lx, ly = g["light"][:2]
    rr = abs(g["r_orb"][1] - ly) or 12.0
    _glow(cr, lx, ly, rr * 7.0, CORAL, 0.45)                      # the light's bloom
    _glow(cr, lx, ly, rr * 2.6, HOT, 0.6)
    # the glow line from the light to its back (S11's, on from frame 1: S12 continues it)
    bx, by = g["back"][:2]
    L = math.hypot(bx - lx, by - ly)
    if L > rr * 2:
        ang = math.atan2(by - ly, bx - lx)
        r0, r1 = rr * 1.4, max(rr * 1.4 + 1, L - 6 - 22 * min(1.0, L / 300.0))
        breathe = 0.85 + 0.15 * math.sin(f / 3.0)
        cr.save()
        cr.translate(lx, ly)
        cr.rotate(ang)
        for wdt, a in ((22.0, 0.10), (12.0, 0.22), (5.0, 0.75)):
            grad = cairo.LinearGradient(r0, 0, r1, 0)
            grad.add_color_stop_rgba(0.0, *CORAL, a * breathe)
            grad.add_color_stop_rgba(0.75, *CORAL, a * breathe)
            grad.add_color_stop_rgba(1.0, *CORAL, 0.0)
            cr.new_path()
            cr.move_to(r0, -wdt * 0.25)
            cr.line_to(r1, -wdt * 0.5)
            cr.line_to(r1, wdt * 0.5)
            cr.line_to(r0, wdt * 0.25)
            cr.close_path()
            cr.set_source(grad)
            cr.fill()
        cr.restore()
        _glow(cr, bx, by, 34.0, CORAL, 0.45 * breathe)            # its back, lit
        _glow(cr, bx, by, 14.0, HOT, 0.35 * breathe)


# ---------------------------------------------------------------- S14
def _puff(cr, x, y, age, size, seed):
    """One landing's dust puff at screen (x, y), `age` frames after the landing (drawn on 2s by the caller): a flat
    ring spreading on the grass and a few soft dust balls bursting up and out, fading by ~11 frames."""
    if age < 0 or age > 11:
        return
    u = age / 11.0
    fade = (1 - u) ** 1.4
    rnd = random.Random(seed)
    cr.save()
    cr.translate(x, y)
    cr.scale(1.0, 0.42)                                           # the ring lies on the grass
    cr.new_path()
    cr.arc(0, 0, size * (0.5 + 1.1 * u), 0, 2 * math.pi)
    cr.set_line_width(size * 0.16 * (1 - u) + 1)
    cr.set_source_rgba(*DUST, 0.55 * fade)
    cr.stroke()
    cr.restore()
    for k in range(7):
        a = math.pi * (0.08 + 0.84 * k / 6) + rnd.uniform(-0.15, 0.15)   # up and out (a fan over the grass)
        d = size * (0.35 + 0.9 * u) * rnd.uniform(0.8, 1.2)
        bx = x + math.cos(a) * d * 1.3
        by = y - math.sin(a) * d * 0.75 - size * 0.25 * u
        r = size * (0.18 + 0.16 * u) * rnd.uniform(0.75, 1.25)
        cr.new_path()
        cr.arc(bx, by, r, 0, 2 * math.pi)
        cr.set_source_rgba(*DUST, 0.5 * fade)
        cr.fill()
        _glow(cr, bx, by, r * 1.8, DUST, 0.18 * fade)


def _s14(cr, f, land, plops):
    for d in land:
        age = f - d["frame"]
        age -= age % 2                                            # on 2s
        x, y, z = d["px"]
        if z <= 0:
            continue
        size = 34.0 * d["scale"] / 0.42 * (1.35 if d["frame"] in plops else 1.0) * min(2.0, max(0.5, 20.0 / z))
        _puff(cr, x, y, age, size, seed=d["moth"])


# ---------------------------------------------------------------- driver
def _drawer(shot):
    if shot == "S12":
        with open(os.path.join(BUILD, "S12_anchors.json")) as fh:
            A = {int(k): v for k, v in json.load(fh)["frames"].items()}
        return lambda cr, f: _s12(cr, min(max(1, f), max(A)), A)
    if shot == "S14":
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "S14_landings.json")) as fh:
            d = json.load(fh)
        return lambda cr, f: _s14(cr, f, d["landings"], set(d["plops"]))
    return None


def post(shot, raw, out):
    cairo = _cairo()
    draw = _drawer(shot)
    os.makedirs(out, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(raw, "[0-9]*.png"))):
        name = os.path.basename(path)
        f = int(name[:4])
        dst = os.path.join(out, name)
        if draw is None:
            shutil.copyfile(path, dst)
            continue
        img = cairo.ImageSurface.create_from_png(path)
        cr = cairo.Context(img)
        s = _scale(img)
        cr.scale(s, s)
        draw(cr, f)
        img.write_to_png(dst)
    return out


def still(shot, f, png, out):
    cairo = _cairo()
    img = cairo.ImageSurface.create_from_png(png)
    cr = cairo.Context(img)
    s = _scale(img)
    cr.scale(s, s)
    _drawer(shot)(cr, int(f))
    img.write_to_png(out)
    return out


def encode(shot, frames_dir):
    """Finished frames -> out/monsters/diorama_ep03/shots/<SHOT>.mp4 + <SHOT>_sheet.jpg: crf 10, bitexact, a
    stream-copy remux, no encoder tags; checks the frame count against timing.json's render_frames."""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    with open(os.path.join(ROOT, "channels", "monsters", "ep03", "timing.json")) as fh:
        n = {s["shot"]: s["render_frames"] for s in json.load(fh)["shots"]}[shot]
    os.makedirs(SHOTS_OUT, exist_ok=True)
    out = os.path.join(SHOTS_OUT, shot + ".mp4")
    clean = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
             "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]
    tmp = tempfile.mkdtemp()
    enc = os.path.join(tmp, "enc.mp4")
    subprocess.run([ff, "-v", "error", "-framerate", "24", "-start_number", "1", "-i",
                    os.path.join(frames_dir, "%04d.png"), "-frames:v", str(n), "-vf", "scale=720:1280:flags=lanczos",
                    "-c:v", "libx264", "-crf", "10", "-preset", "slow", "-pix_fmt", "yuv420p", *clean, enc],
                   check=True)
    subprocess.run([ff, "-y", "-v", "error", "-i", enc, "-c", "copy", *clean, "-movflags", "+faststart", out],
                   check=True)
    subprocess.run([ff, "-y", "-v", "error", "-i", out, "-vf", "select=not(mod(n\\,6)),scale=180:320,tile=7x2",
                    "-frames:v", "1", "-q:v", "3", os.path.join(SHOTS_OUT, shot + "_sheet.jpg")], check=True)
    got = len(subprocess.run([ff, "-v", "error", "-i", out, "-vf", "scale=8:8", "-f", "rawvideo", "-pix_fmt", "gray",
                              "-"], capture_output=True, check=True).stdout) // 64
    data = open(out, "rb").read()
    tags = {t: data.count(t.encode()) for t in ("x264", "Lavf", "Lavc")}
    shutil.rmtree(tmp)
    print(f"{shot}: {got}/{n} frames, tags {tags}" + ("" if got == n and not any(tags.values()) else "  **CHECK**"))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "post":
        print(post(*sys.argv[2:5]))
    elif cmd == "still":
        print(still(*sys.argv[2:6]))
    elif cmd == "encode":
        encode(*sys.argv[2:4])
