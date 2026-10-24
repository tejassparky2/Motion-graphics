"""Rap lyric video renderer: word-synced kinetic typography over beat-cut dark-anime close-ups.

    python channels/rap/lyricvid.py SONG_MODULE AUDIO.wav WORDS.json OUT.mp4 [--preview SECONDS]

SONG_MODULE (e.g. still_breathing) sets the cut (START, BEATS), the beat grid (BPM, PHASE), the lyric lines with
style marks and the shots per line. WORDS.json is faster-whisper word timestamps for the whole song
(tools: channels/rap/words.py); the real lyrics are aligned to them so captions never show Whisper's typos.

Lyric marks: *word = big emphasis word (Anton), !word = red key word, plain words are small italic serif.
Shot variants: fill (flat colour), close (tight crop on the scene's focus), line (white line-art on black),
red (white line-art on a red flood), redline (red line-art on black).
"""
import difflib
import importlib
import json
import math
import os
import re
import subprocess
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, HERE]

from motion import engine  # noqa: E402,F401  (registers assets/fonts with fontconfig)
import cairo  # noqa: E402
import numpy as np  # noqa: E402

import scenes  # noqa: E402
from render import CLEAN, ffmpeg_bin  # noqa: E402

W, H, FPS = scenes.W, scenes.H, 30
RED = (0.93, 0.08, 0.16)
RED_BG = np.array([0.08, 0.06, 0.78])      # BGR order, the red flood behind line-art
WHITE = (0.96, 0.97, 0.97)
SAFE_TOP, SAFE_BOTTOM = 260, 1440          # keep lyrics clear of the Shorts title and buttons


def norm(w):
    return re.sub(r"ing$", "in", re.sub(r"[^a-z0-9]", "", w.lower()))   # sung "breathin'" = "breathing"


def merge_pieces(words):
    """Whisper splits sung words ("ASK", "-ing"); glue pieces that start with a hyphen onto the word before."""
    out = []
    for w in words:
        if w["w"].startswith("-") and out:
            out[-1] = dict(w=out[-1]["w"] + w["w"][1:], s=out[-1]["s"], e=w["e"])
        else:
            out.append(dict(w))
    return out


def align(lines, words, t0, t1):
    """Give every lyric word a start time from the Whisper words heard between t0 and t1."""
    heard = [w for w in merge_pieces(words) if t0 - 0.3 <= w["s"] <= t1]
    lyric = [(i, j, tok) for i, line in enumerate(lines) for j, tok in enumerate(line.split())]
    a = [norm(tok) for _, _, tok in lyric]
    b = [norm(w["w"]) for w in heard]
    times = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = heard[blk.b + k]["s"]
    # words Whisper misheard: spread evenly between the matched neighbours
    known = [k for k, t in enumerate(times) if t is not None]
    for k in range(len(times)):
        if times[k] is None:
            lo = max([q for q in known if q < k], default=None)
            hi = min([q for q in known if q > k], default=None)
            if lo is None:
                times[k] = times[hi] - 0.25 * (hi - k)
            elif hi is None:
                times[k] = times[lo] + 0.25 * (k - lo)
            else:
                times[k] = times[lo] + (times[hi] - times[lo]) * (k - lo) / (hi - lo)
    out = [[] for _ in lines]
    for (i, j, tok), t in zip(lyric, times):
        out[i].append(dict(tok=tok, t=t))
    return out


# ---------------------------------------------------------------- typography

def word_style(tok):
    if tok.startswith("!"):
        return tok[1:], ("Anton", cairo.FONT_SLANT_NORMAL, 210, RED, True)
    if tok.startswith("*"):
        return tok[1:], ("Anton", cairo.FONT_SLANT_NORMAL, 150, WHITE, True)
    return tok, ("Liberation Serif", cairo.FONT_SLANT_ITALIC, 76, WHITE, False)


def layout_line(cr, words, align_left):
    """Flow a line's words into rows (fixed for the whole line, so new words never push old ones around)."""
    items = []
    for w in words:
        text, st = word_style(w["tok"])
        text = text.upper() if st[4] else text
        cr.select_font_face(st[0], st[1], cairo.FONT_WEIGHT_BOLD if st[0] != "Anton" else cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(st[2])
        ext = cr.text_extents(text)
        width = ext.x_advance
        if width > 940:                       # a single huge word: shrink to fit
            st = (st[0], st[1], st[2] * 940 / width, st[3], st[4])
            width = 940
        items.append(dict(text=text, st=st, w=width, t=w["t"]))
    rows, row, rw = [], [], 0
    gap = 26
    for it in items:
        if row and rw + gap + it["w"] > 940:
            rows.append(row)
            row, rw = [], 0
        row.append(it)
        rw += (gap if len(row) > 1 else 0) + it["w"]
    rows.append(row)
    y = 0
    for row in rows:
        asc = max(it["st"][2] for it in row) * 0.92
        y += asc
        total = sum(it["w"] for it in row) + gap * (len(row) - 1)
        x = 70 if align_left else (W - total) / 2
        for it in row:
            it["x"], it["y"] = x, y
            x += it["w"] + gap
        y += 18
    return items, y


def draw_text(cr, items, block_h, anchor, t):
    top = {"top": SAFE_TOP + 40, "mid": (H - block_h) / 2 - 80, "low": SAFE_BOTTOM - block_h - 40}[anchor]
    for it in items:
        age = t - it["t"]
        if age < 0:
            continue
        pop = 1 + 0.35 * math.exp(-age * 18)
        alpha = min(1.0, age / 0.05)
        font, slant, size, col, big = it["st"]
        cr.save()
        cx, cy = it["x"] + it["w"] / 2, top + it["y"] - size * 0.35
        cr.translate(cx, cy)
        cr.scale(pop, pop)
        cr.translate(-cx, -cy)
        cr.select_font_face(font, slant, cairo.FONT_WEIGHT_NORMAL if font == "Anton" else cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        cr.move_to(it["x"], top + it["y"])
        cr.text_path(it["text"])
        cr.set_source_rgba(0, 0, 0, 0.55 * alpha)
        cr.set_line_width(size * 0.10)
        cr.stroke_preserve()
        if big and age < 0.12:                 # fresh key word: split-colour glitch for a few frames
            cr.save()
            cr.translate(9, 0)
            cr.set_source_rgba(0.1, 0.9, 0.9, 0.5 * alpha)
            cr.fill_preserve()
            cr.restore()
        if big:                                # soft glow behind key words
            for wdt, a in ((size * 0.30, 0.10), (size * 0.16, 0.16)):
                cr.set_source_rgba(col[0], col[1], col[2], a * alpha)
                cr.set_line_width(wdt)
                cr.stroke_preserve()
        cr.set_source_rgba(col[0], col[1], col[2], alpha)
        cr.fill()
        cr.restore()


# ---------------------------------------------------------------- picture effects

def lineart(arr, variant):
    lum = (arr[..., 0] * 0.11 + arr[..., 1] * 0.59 + arr[..., 2] * 0.30) / 255.0
    gx = np.zeros_like(lum)
    gy = np.zeros_like(lum)
    gx[:, 1:-1] = lum[:, 2:] - lum[:, :-2]
    gy[1:-1, :] = lum[2:, :] - lum[:-2, :]
    edge = np.clip((np.sqrt(gx * gx + gy * gy) - 0.035) * 9, 0, 1)[..., None]
    shade = (0.78 + 0.35 * lum)[..., None]
    if variant == "red":
        base, ink = RED_BG * shade, np.array([0.97, 0.97, 0.97])
    elif variant == "redline":
        base, ink = np.array([0.04, 0.025, 0.02]) * shade, np.array([0.16, 0.10, 0.93])
    else:
        base, ink = np.array([0.06, 0.05, 0.04]) * shade, np.array([0.90, 0.92, 0.92])
    out = base * (1 - edge) + ink * edge
    arr[..., :3] = np.clip(out * 255, 0, 255).astype(np.uint8)


class Finish:
    """Grain, vignette and chromatic-aberration edges, applied to the finished frame."""

    def __init__(self):
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        self.vig = np.clip(1.08 - 0.42 * d ** 2, 0.35, 1.0)[..., None].astype(np.float32)
        self.ca = np.clip((d - 0.45) * 1.4, 0, 1)[..., None].astype(np.float32)
        rnd = np.random.default_rng(7)
        self.grain = [rnd.normal(0, 9, (H, W, 1)).astype(np.float32) for _ in range(6)]

    def __call__(self, arr, frame, glitch):
        f = arr[..., :3].astype(np.float32)
        s = 6 + int(14 * glitch)
        r = np.roll(f[..., 2], s, axis=1)
        b = np.roll(f[..., 0], -s, axis=1)
        m = np.clip(self.ca[..., 0] + glitch * 0.8, 0, 1)
        f[..., 2] = f[..., 2] * (1 - m) + r * m
        f[..., 0] = f[..., 0] * (1 - m) + b * m
        f = f * self.vig + self.grain[frame % 6]
        arr[..., :3] = np.clip(f, 0, 255).astype(np.uint8)
        arr[..., 3] = 255


# ---------------------------------------------------------------- timeline

class Video:
    def __init__(self, song, words):
        self.song = song
        self.beat = 60.0 / song.BPM
        self.t0 = song.PHASE + song.START_BEAT * self.beat
        self.dur = song.BEATS * self.beat
        lines = [ln for ln, _ in song.LINES]
        self.lines = align(lines, words, self.t0, self.t0 + self.dur + 0.5)
        # shots: each line starts on the beat nearest its first word, then cuts every 2 beats through its variants
        self.shots = []
        starts = [self.snap(ws[0]["t"] - 0.06) for ws in self.lines]
        starts[0] = 0.0
        ends = starts[1:] + [self.dur]
        for (ln, plan), s, e in zip(song.LINES, starts, ends):
            k = 0
            t = s
            while t < e - 1.5 * self.beat or t == s:
                scene, variant = plan[k % len(plan)]
                self.shots.append((t, scene, variant))
                t += 2 * self.beat
                k += 1
        self.line_starts = [ws[0]["t"] - self.t0 for ws in self.lines]

    def snap(self, t_song):
        rel = t_song - self.t0
        return max(0.0, round(rel / self.beat) * self.beat)

    def frames(self):
        return int(round(self.dur * FPS))


def render_range(args):
    song_name, words_path, first, last, path = args
    song = importlib.import_module(song_name)
    vid = Video(song, json.load(open(words_path)))
    fin = Finish()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    arr = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    layouts = {}
    cmd = [ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", "14M", "-bufsize", "28M", "-pix_fmt", "yuv420p",
           "-threads", "1", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(first, last):
        t = i / FPS
        k = max(j for j, s in enumerate(vid.shots) if s[0] <= t + 1e-6)
        s0, scene, variant = vid.shots[k]
        s1 = vid.shots[k + 1][0] if k + 1 < len(vid.shots) else vid.dur
        p = (t - s0) / max(s1 - s0, 1e-3)
        bt = ((t + vid.t0 - vid.song.PHASE) % vid.beat)
        beat = math.exp(-bt * 7)
        cr = cairo.Context(surf)
        cr.set_source_rgb(0, 0, 0)
        cr.paint()
        cr.save()
        fx, fy = vid.song.FOCUS.get(scene, (W / 2, H / 2))
        zoom = (1.75 if variant == "close" else 1.0) * (1 + 0.07 * p) * (1 + 0.035 * math.exp(-(t - s0) * 9))
        cx = W / 2 + (fx - W / 2) * (0.0 if variant != "close" else 1.0)
        cy = H / 2 + (fy - H / 2) * (0.0 if variant != "close" else 1.0)
        cr.translate(W / 2, H / 2)
        cr.scale(zoom, zoom)
        cr.translate(-cx, -cy)
        scenes.SCENES[scene](cr, p, beat)
        cr.restore()
        surf.flush()
        if variant in ("line", "red", "redline"):
            lineart(arr, variant)
            surf.mark_dirty()
        # lyrics: the current line builds up word by word
        li = max([j for j, s in enumerate(vid.line_starts) if s <= t + 0.08], default=0)
        if li not in layouts:
            words = [dict(tok=w["tok"], t=w["t"] - vid.t0) for w in vid.lines[li]]
            layouts[li] = layout_line(cr, words, vid.song.LINES_LEFT[li % len(vid.song.LINES_LEFT)])
        items, bh = layouts[li]
        draw_text(cr, items, bh, vid.song.ANCHORS[li % len(vid.song.ANCHORS)], t + 0.03)
        surf.flush()
        glitch = math.exp(-(t - s0) * 25) if k > 0 else 0.0
        if li >= vid.song.DIP_FROM and 0 < t - vid.line_starts[li] < 0.1 and li > 0:
            arr[..., :3] = (arr[..., :3] * 0.15).astype(np.uint8)   # dip to black as a verse line lands
        fin(arr, i, glitch)
        proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    return path


def main():
    song_name, audio, words_path, out = sys.argv[1:5]
    preview = float(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None
    song = importlib.import_module(song_name)
    vid = Video(song, json.load(open(words_path)))
    n = vid.frames() if preview is None else int(preview * FPS)
    tmp = os.path.join(ROOT, "build", "rap")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    parts = os.cpu_count() or 2
    bounds = [n * k // parts for k in range(parts + 1)]
    jobs = [(song_name, words_path, bounds[k], bounds[k + 1], os.path.join(tmp, f"part{k}.mp4"))
            for k in range(parts) if bounds[k + 1] > bounds[k]]
    with Pool(len(jobs)) as pool:
        paths = pool.map(render_range, jobs)
    lst = os.path.join(tmp, "parts.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in paths)
    dur = n / FPS
    subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-ss", f"{vid.t0:.3f}", "-t", f"{dur:.3f}", "-i", audio,
                           "-filter:a", f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.15:.3f}:d=0.15",
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-shortest", *CLEAN, out])
    print(out, f"{dur:.2f}s")


if __name__ == "__main__":
    main()
