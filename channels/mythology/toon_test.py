#!/usr/bin/env python3
"""Test clip for the code-drawn talking Krishna (toon_rig + toon_krishna), Nov 2026: ~11 s, two Hindi takes.

  python -I -X utf8 channels/mythology/toon_test.py                    # -> myth_out/tests/toon_krishna_test.mp4
  python -I -X utf8 channels/mythology/toon_test.py --still 2.0        # one frame (png in myth_out/tests)
  python -I -X utf8 channels/mythology/toon_test.py --sheet            # 6x2 contact sheet
  python -I -X utf8 channels/mythology/toon_test.py --poses            # every arm pose side by side (rig check)

Performance: gestures change at the start of each spoken phrase (found from the audio), the face follows a small
expression script, and the procedural layer adds blinks, eye darts, brow raises and nods on stressed syllables,
idle breathing and sway, hair/earring/feather follow-through, a slow camera push and background parallax.
"""
import argparse
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE]

import cairo  # noqa: E402

import toon_krishna as K  # noqa: E402
import toon_rig as R  # noqa: E402

FPS = 30
TTS = os.path.join(ROOT, "build", "mythology", "tts")
CLIPS = [(os.path.join(TTS, "2eeeefbfb66c5b2d.wav"), 0.10),   # सोचो, जिस लक्ष्मण रेखा की मिसाल ... है ही नहीं।
         (os.path.join(TTS, "7d8a23c0c9a78ecc.wav"), 5.92)]   # ये कोई अफ़वाह नहीं है। वाल्मीकि रामायण का अरण्य कांड ...
TOTAL = 11.0
OUT_DIR = os.path.join(os.path.dirname(ROOT), "myth_out", "tests")
BUILD = os.path.join(ROOT, "build", "mythology", "toon_test")


class Director:
    """state(t) for toon_krishna.draw: a pure function of t (safe in worker processes)."""

    def __init__(self):
        self.voice = v = R.Voice(CLIPS, TOTAL, FPS)
        ph = v.phrases                      # [सोचो] [जिस ... देते हैं] [वो ... है ही नहीं] [ये ... है] [वाल्मीकि ...] [ख़ुद ...]
        s = [a for a, _ in ph]
        self.ph = ph
        self.no_t = ph[2][1] - 0.78         # "है ही नहीं": the last ~0.8 s of phrase 3
        end = ph[-1][1]
        self.end = end
        pk = lambda t: min(v.peaks, key=lambda p: abs(p - t)) - 0.15      # land a gesture on a stressed syllable
        self.arm_r = R.Track(K.ARM_POSES, [
            (0.0, "rest", 0.4), (0.0, "point_up", 0.42),           # moving from frame 0: point on "सोचो"
            (s[1] - 0.22, "explain", 0.5),
            (pk((s[1] + ph[1][1]) / 2), "explain2", 0.45),          # long phrases get a second beat gesture
            (s[2] - 0.15, "explain", 0.45),
            (self.no_t - 0.3, "raise", 0.38),                       # raised hand on "है ही नहीं"
            (ph[2][1] + 0.25, "rest", 0.6),
            (s[3] - 0.2, "point_up", 0.42),                         # "ये कोई अफ़वाह नहीं है।"
            (s[4] - 0.2, "explain", 0.5),
            (pk((s[4] + ph[4][1]) / 2 + 0.2), "explain2", 0.45),
            (s[5] - 0.22, "offer", 0.45),                           # "ख़ुद पढ़कर देखो"
            (end - 0.05, "heart", 0.6),                             # knowing smile, nod, hand on heart
        ], delays={"ha": 0.05, "tw": 0.06, "tip": 0.06, "ci": 0.08, "cm": 0.08, "cr": 0.09, "cp": 0.1, "sp": 0.08,
                   "to": 0.07, "tf": 0.07, "tc": 0.08, "el": 0.025})
        self.arm_l = R.Track(K.ARM_POSES, [
            (0.0, "rest_l", 0.5), (s[1] + 0.2, "low_l", 0.6), (ph[1][1] - 0.1, "rest_l", 0.7),
            (s[4] + 0.1, "low_l", 0.6), (ph[4][1], "rest_l", 0.7),
        ], delays={"ha": 0.05, "tw": 0.06, "ci": 0.08, "cm": 0.08, "cr": 0.09, "cp": 0.1})
        self.face = R.Track(K.EXPRESSIONS, [
            (0.0, "intrigue", 0.3), (s[1] - 0.05, "explain", 0.4), (s[2] - 0.05, "serious", 0.4),
            (self.no_t - 0.15, "firm", 0.3), (ph[2][1] + 0.3, "neutral", 0.5), (s[3] - 0.1, "serious", 0.35),
            (s[4] - 0.1, "explain", 0.4), (s[5] - 0.1, "intrigue", 0.35), (end - 0.05, "knowing", 0.5),
        ], ease=R.smoother)
        self.turn_t = (s[4] + 0.1, ph[4][1] - 0.1)          # looks aside while naming the source
        self.blinks = R.Blinks(TOTAL, seed=5, extra=(self.turn_t[0] - 0.05, self.turn_t[1] - 0.02, end - 0.12))
        self.gaze = R.Gaze(TOTAL, seed=9)

    # -- head: authored moves + speech rhythm + idle drift
    def head_pose(self, t):
        v = self.voice
        act = v.activity(t)
        roll = 0.025 + 0.028 * R.fbm(t, 1, 0.32) + act * 0.022 * R.fbm(t, 4, 1.1)    # base: a slight 3/4 look
        yaw = -0.09 + 0.045 * R.fbm(t, 2, 0.22) + act * 0.025 * R.fbm(t, 5, 0.9)
        pitch = 0.018 * R.fbm(t, 3, 0.4)
        for p in v.peaks:                                     # small nods on stressed syllables
            pitch += 0.045 * R.bump(t, p - 0.08, 0.34)
            roll += 0.012 * R.bump(t, p - 0.06, 0.4)
        # "सोचो": a curious tilt; "है ही नहीं": a firm shake; aside glance; end: a knowing nod + tilt
        roll -= 0.07 * R.bump(t, -0.2, 1.2)
        sh = R.bump(t, self.no_t - 0.05, 0.85) ** 0.5
        yaw += 0.13 * sh * math.sin(2 * math.pi * 3.0 * (t - self.no_t + 0.05))
        a, b = self.turn_t
        aside = R.smoother((t - a) / 0.45) - R.smoother((t - b + 0.2) / 0.5)
        yaw += 0.33 * aside
        roll += 0.03 * aside
        pitch -= 0.03 * aside
        yaw -= 0.08 * R.bump(t, self.ph[3][0] - 0.1, 1.2)
        nod = R.bump(t, self.end + 0.08, 0.6)
        pitch += 0.14 * nod
        roll += 0.07 * R.smoother((t - self.end) / 0.6)
        return roll, yaw, pitch, aside

    def state(self, t):
        S = dict(K.STATE)
        S["t"] = t
        v = self.voice
        roll, yaw, pitch, aside = self.head_pose(t)
        r1, y1, p1, _ = self.head_pose(t - 0.12)
        r2, y2, p2, _ = self.head_pose(t - 0.2)
        S.update(roll=roll, yaw=yaw, pitch=pitch, roll_lag=r1, yaw_lag=y1, pitch_lag=p1)
        S["hy"] = 3.0 * math.sin(2 * math.pi * t / 3.8 + 0.6)
        S["ear_swing"] = 2.4 * (r2 - roll) + 0.9 * (y2 - yaw) + 0.04 * math.sin(2 * math.pi * 0.8 * t)
        S["feather_swing"] = 0.9 * (r2 - roll) + 0.02 * math.sin(2 * math.pi * 0.6 * t + 1)
        S["breath"] = math.sin(2 * math.pi * t / 3.8)
        S["bx"] = 7 * R.fbm(t, 6, 0.18)
        S["by"] = -2.5 * (S["breath"] + 1)
        S["brot"] = 0.007 * R.fbm(t, 7, 0.2) + 0.15 * roll * 0.2
        S["cam_s"] = 1.0 + 0.075 * R.smoother(t / TOTAL)
        S["cam_x"] = 10 * math.sin(0.35 * t)
        # face
        S.update(self.face.at(t))
        for p in v.peaks:
            S["b_raise"] += 0.32 * R.pulse(t, p, 0.08, 0.3) * (1 - 0.7 * S["b_frown"])
        m = v.mouth(t)
        S.update(m_open=m["open"], m_wide=m["wide"], m_round=m["round"], m_teeth=m["teeth"])
        S["blink"] = self.blinks(t)
        gx, gy = self.gaze(t)
        S["gx"] = gx * (1 - aside) - yaw * 1.6 * (1 - aside) + 0.75 * aside
        S["gy"] = gy * (1 - aside) - 0.25 * aside
        # arms (with beats on stresses and a wag of the raised hand on "नहीं")
        ar, al = self.arm_r.at(t), self.arm_l.at(t)
        beat = sum(R.pulse(t, p, 0.07, 0.22) for p in v.peaks)
        ar["el"] += -6 * beat
        wag = R.bump(t, self.no_t - 0.05, 0.85) ** 0.5
        ar["ha"] += 11 * wag * math.sin(2 * math.pi * 3.0 * (t - self.no_t))
        wag2 = R.bump(t, self.ph[3][0] + 0.15, 0.9) ** 0.5
        ar["ha"] += 9 * wag2 * math.sin(2 * math.pi * 3.2 * (t - self.ph[3][0]))
        for a, k in ((ar, 1), (al, 2)):
            a["sh"] += 1.2 * R.fbm(t, 20 + k, 0.4) + 0.6 * S["breath"]
            a["el"] += 2.0 * R.fbm(t, 30 + k, 0.5)
        S["arm_r"], S["arm_l"] = ar, al
        return S


_dir = None


def _init():
    global _dir
    _dir = Director()


def frame(surface, t):
    cr = cairo.Context(surface)
    K.draw(cr, _dir.state(t))
    surface.flush()


def _part(args):
    first, last, path = args
    if _dir is None:
        _init()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{K.W}x{K.H}", "-r",
           str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-threads",
           "1", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, K.W, K.H)
    t0 = time.time()
    for i in range(first, last):
        frame(surface, i / FPS)
        proc.stdin.write(bytes(surface.get_data()))
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg failed")
    return path, (time.time() - t0) / max(1, last - first)


def render(out):
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = int(round(TOTAL * FPS))
    workers = max(1, min(int(os.environ.get("RENDER_WORKERS", (os.cpu_count() or 2) - 2)), 12))
    chunk = max(FPS, n // (workers * 2))
    jobs = [(a, min(n, a + chunk), os.path.join(BUILD, f"part{k:03d}.mp4")) for k, a in enumerate(range(0, n, chunk))]
    t0 = time.time()
    per = []
    with mp.get_context("spawn").Pool(workers, initializer=_init) as pool:
        for k, (_, spf) in enumerate(pool.imap(_part, jobs)):
            per.append(spf)
            print(f"\rparts {k + 1}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(f"\n{n} frames in {time.time() - t0:.1f} s wall, {sum(per) / len(per):.3f} s/frame per worker "
          f"({workers} workers)", file=sys.stderr)
    listing = os.path.join(BUILD, "parts.txt")
    with open(listing, "w") as f:
        f.writelines(f"file '{j[2].replace(os.sep, '/')}'\n" for j in jobs)
    silent = os.path.join(BUILD, "silent.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listing, "-c",
                           "copy", silent])
    for j in jobs:
        os.remove(j[2])
    wav = os.path.join(BUILD, "voice.wav")
    R.Voice(CLIPS, TOTAL, FPS).write_wav(wav)                # the same timeline the mouth was synced to
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-af",
                           "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:v", "copy", "-c:a", "aac", "-b:a",
                           "256k", "-shortest", "-map_metadata", "-1", "-movflags", "+faststart", out])
    print(f"wrote {out}", file=sys.stderr)


def still(t, out):
    _init()
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, K.W, K.H)
    t0 = time.time()
    frame(s, t)
    print(f"{t:.2f}s drawn in {time.time() - t0:.3f} s", file=sys.stderr)
    s.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def sheet(times, out, cols=6, thumb=300):
    _init()
    th = int(thumb * K.H / K.W)
    rows = (len(times) + cols - 1) // cols
    sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * thumb, rows * (th + 26))
    sc = cairo.Context(sh)
    sc.set_source_rgb(1, 1, 1)
    sc.paint()
    fr = cairo.ImageSurface(cairo.FORMAT_ARGB32, K.W, K.H)
    for k, t in enumerate(times):
        frame(fr, t)
        x, y = (k % cols) * thumb, (k // cols) * (th + 26)
        sc.save()
        sc.translate(x, y)
        sc.scale(thumb / K.W, th / K.H)
        sc.set_source_surface(fr)
        sc.get_source().set_filter(cairo.FILTER_GOOD)
        sc.paint()
        sc.restore()
        sc.set_source_rgb(0, 0, 0)
        sc.set_font_size(17)
        sc.move_to(x + 8, y + th + 19)
        sc.show_text(f"{t:.2f}s")
    sh.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def poses(out):
    """Each arm pose on its own (rig check), with the neutral face."""
    names = ["rest", "point_up", "explain", "raise", "offer"]
    cols, thumb = len(names), 360
    th = int(thumb * K.H / K.W)
    sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * thumb, th + 26)
    sc = cairo.Context(sh)
    sc.set_source_rgb(1, 1, 1)
    sc.paint()
    fr = cairo.ImageSurface(cairo.FORMAT_ARGB32, K.W, K.H)
    for k, nm in enumerate(names):
        S = dict(K.STATE)
        S["arm_r"] = dict(K.ARM_POSES[nm])
        S["arm_l"] = dict(K.ARM_POSES["low_l" if nm == "explain" else "rest_l"])
        K.draw(cairo.Context(fr), S)
        sc.save()
        sc.translate(k * thumb, 0)
        sc.scale(thumb / K.W, th / K.H)
        sc.set_source_surface(fr)
        sc.get_source().set_filter(cairo.FILTER_GOOD)
        sc.paint()
        sc.restore()
        sc.set_source_rgb(0, 0, 0)
        sc.set_font_size(18)
        sc.move_to(k * thumb + 8, th + 20)
        sc.show_text(nm)
    sh.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--poses", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "toon_krishna_test.mp4"))
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    if a.still is not None:
        for t in a.still:
            still(t, os.path.join(OUT_DIR, f"toon_krishna_still_{t:05.2f}.png"))
    elif a.sheet:
        sheet([0.3, 1.2, 2.0, 3.0, 4.0, 4.6, 5.0, 6.2, 7.0, 8.3, 9.7, 10.6], os.path.join(OUT_DIR, "toon_krishna_sheet.png"))
    elif a.poses:
        poses(os.path.join(OUT_DIR, "toon_krishna_poses.png"))
    else:
        render(a.out)
