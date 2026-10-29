#!/usr/bin/env python3
"""Render a "Doc and the Organs" explainer reel from channels/doctor/videos/<name>.py: the Hinglish channel's poster
pipeline (poster.py, shots.py, the `doc` music bed, the upload sheet), copied in English on 29 Oct 2026, voiced with
our narrator (motion.voice: Chatterbox stock voice, every take checked with Whisper medium).

  python channels/doctor/render_doc.py --video amoeba            # -> out/amoeba.mp4, _preview.mp4, _upload_sheet.md
  python channels/doctor/render_doc.py --video amoeba --voice    # only generate and check the narration
  python channels/doctor/render_doc.py --video amoeba --still 2  # one frame -> build/doctor/amoeba_still_2.0.png
  python channels/doctor/render_doc.py --video amoeba --sheet 1  # contact sheet, one frame per second
  python channels/doctor/render_doc.py --video amoeba --remix    # soundtrack only, onto the last picture track
  python channels/doctor/render_doc.py --video amoeba --cover    # the cover image -> out/amoeba_cover.png
"""
import argparse
import importlib.util
import json
import multiprocessing as mp
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, ROOT]

import cairo  # noqa: E402
from motion import voice  # noqa: E402
from motion.timeline import Timeline  # noqa: E402
from poster import FPS, H, W  # noqa: E402

OUT = os.path.join(ROOT, "out")
BUILD = os.path.join(ROOT, "build", "doctor")
# Output hygiene: no container metadata, no encoder/version tags, and no x264 settings SEI in the video stream.
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name="]

_mod, _tl = None, None


class BeatView:
    """One script line as the shot functions see it: start, end, and when a word (or a fraction of the line) lands."""

    def __init__(self, tl, b):
        self._tl, self._b = tl, b
        self.id, self.text, self.start, self.end = b.id, b.text, b.start, b.end

    def at(self, cue=None, frac=None, end=False, nth=1):
        if frac is not None:
            return self.start + frac * (self.end - self.start)
        return self._tl.at(self.id, cue, end=end, nth=nth)


class TL:
    """motion.timeline.Timeline with the Hinglish pipeline's interface: tl[line id].start / .end / .at(word),
    tl.total, tl.beats, tl.clips()."""

    def __init__(self, tl):
        self.raw = tl
        self.total = tl.total
        self.beats = [BeatView(tl, b) for b in tl.beats]
        self._by = {b.id: b for b in self.beats}

    def __getitem__(self, bid):
        return self._by[bid]

    def clips(self):
        return self.raw.clips()


def load_module(name):
    spec = importlib.util.spec_from_file_location(f"dvideo_{name}", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_timeline(name):
    """Voice every sentence (cached), re-take any that Whisper medium mishears, and lay the lines out."""
    global _mod, _tl
    if _tl is not None:
        return _mod, _tl
    mod = load_module(name)
    voice.configure(**mod.NARRATOR)
    takes = Timeline.sentences(mod.SCRIPT)
    voice.clone_prefetch([(t, w) for t, _, w in takes])
    voice.clone_check(takes)
    tl = Timeline(mod.SCRIPT, lead_in=0.10, tail=getattr(mod, "TAIL", 0.9))
    tl.report()
    for b in tl.beats:
        print(f"  {b.id:>4} {b.start:6.2f}-{b.end:6.2f}  {b.text[:70]}", file=sys.stderr)
    _mod, _tl = mod, TL(tl)
    return _mod, _tl


def draw(surface, frame):
    cr = cairo.Context(surface)
    _mod.draw(cr, frame / FPS, _tl)
    surface.flush()


def _part(args):
    first, last, path = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-threads", "1", path]
    # crf 18, not the Hinglish channel's 14: our masters are committed, and GitHub refuses files over 100 MB
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(first, last):
        draw(surface, i)
        proc.stdin.write(bytes(surface.get_data()))
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg failed")
    return path


def render(name, audio=True):
    """Frames drawn in parallel (forked workers share the timeline; every frame depends only on its time), parts
    joined without re-encoding, then the soundtrack is muxed on."""
    mod, tl = build_timeline(name)
    os.makedirs(OUT, exist_ok=True)
    n = int(round(tl.total * FPS))
    workers = max(1, min(int(os.environ.get("RENDER_WORKERS", os.cpu_count() or 2)), 12))
    chunk = max(FPS * 2, n // (workers * 3))
    jobs = [(a, min(n, a + chunk), os.path.join(BUILD, f"{name}_part{k:03d}.mp4"))
            for k, a in enumerate(range(0, n, chunk))]
    with mp.get_context("fork").Pool(workers) as pool:
        for k, _ in enumerate(pool.imap(_part, jobs)):
            print(f"\rparts {k + 1}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    listing = os.path.join(BUILD, f"{name}_parts.txt")
    with open(listing, "w") as f:
        f.writelines(f"file '{j[2]}'\n" for j in jobs)
    silent = os.path.join(BUILD, f"{name}_silent.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy",
                           silent])
    for j in jobs:
        os.remove(j[2])
    out = os.path.join(OUT, f"{name}.mp4")
    if audio:
        mux_audio(name, mod, tl, n / FPS, silent, out)
    else:
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-c", "copy", *CLEAN, out])
    print(f"wrote {out}", file=sys.stderr)
    preview(out)
    write_sheet(mod, tl, os.path.join(OUT, f"{name}_upload_sheet.md"))
    return out


def preview(out):
    """A smaller copy that's easy to send to a phone (a stream-copy pass drops the encoder tag re-encoding writes)."""
    tmp = os.path.join(BUILD, "preview_tmp.mp4")
    path = out[:-4] + "_preview.mp4"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-c:v", "libx264", "-crf", "26", "-preset",
                           "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", *CLEAN, tmp])
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags",
                           "+faststart", path])
    os.remove(tmp)
    print(f"wrote {path}", file=sys.stderr)


def mux_audio(name, mod, tl, total, silent, out):
    """Voice + music bed + sound effects at -14 LUFS, muxed onto the silent picture track (video stream copied)."""
    from motion.audio import build_soundtrack
    wav = os.path.join(BUILD, f"{name}_soundtrack.wav")
    events = mod.sfx(tl) if hasattr(mod, "sfx") else []
    lufs = build_soundtrack(events, total, wav, tl.clips(), seed=name, bed=getattr(mod, "MUSIC", "doc"))
    print(f"soundtrack {lufs:.1f} LUFS", file=sys.stderr)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac",
                           "-b:a", "256k", "-shortest", *CLEAN, "-movflags", "+faststart", out])


def remix(name):
    """Only the soundtrack changed (music, effects): rebuild it and remux onto the last render's picture track."""
    mod, tl = build_timeline(name)
    out = os.path.join(OUT, f"{name}.mp4")
    mux_audio(name, mod, tl, int(round(tl.total * FPS)) / FPS, os.path.join(BUILD, f"{name}_silent.mp4"), out)
    print(f"wrote {out}", file=sys.stderr)
    preview(out)


def _site(c):
    u = c.get("page", "")
    return c.get("site") or ("Wikimedia Commons" if "wikimedia" in u else "Pixabay" if "pixabay" in u
                             else "Unsplash" if "unsplash" in u else "NASA" if "nasa.gov" in u
                             else "Smithsonian" if "si.edu" in u else "")


def _short_source(src):
    """A research source as a name only: no URL, no paper title (Hinglish channel owner rule: no links in sources)."""
    return re.split(r" '|\shttps?://| \(", src)[0].rstrip(", ")


def write_sheet(mod, tl, path):
    """Upload pack in the Hinglish channel's format: Instagram caption (+ hashtags), a second comment with the photo
    credits, YouTube title and description, pinned comment. Sources and credits are names only, never links, and
    there's no AI or voice wording anywhere in it."""
    m = getattr(mod, "METADATA", None)
    if not m:
        return
    credits = []
    for f in getattr(mod, "CREDITS_FILES", []):
        if os.path.exists(f):
            credits += json.load(open(f, encoding="utf-8"))
    used = set(getattr(mod, "USED_ASSETS", []))
    credits = [c for c in credits if not used or os.path.basename(c["file"]) in used]
    sites = sorted({_site(c) for c in credits} - {""})
    by = sorted({c["author"] for c in credits if c["license"].upper().startswith("CC BY")})
    photo = (f"Photos: {', '.join(sites)}." if sites else "") + (f"\nCC BY: {', '.join(by)}." if by else "")
    sources = "Sources: " + "; ".join(_short_source(x) for x in m.get("sources", []))
    tags = " ".join(m["hashtags"])
    fence = lambda body: f"```\n{body.strip()}\n```"
    lines = [f"# Upload sheet: {m['title']}", "",
             "**Instagram caption**", fence(f"{m['caption'].strip()}\n\n{tags}"), "",
             "**Instagram second comment** (sources and photo credits)", fence(f"{photo}\n{sources}"), "",
             "**YouTube title**", fence(m["yt_title"]), "",
             "**Alternative titles**", *[f"- {a}" for a in m.get("alt_titles", [])], "",
             "**YouTube description**", fence(f"{m['yt_description'].strip()}\n\n{sources}\n{photo}\n\n{tags}"), "",
             "**YouTube tags**", fence(", ".join(m.get("tags", []))), "",
             "**Pinned comment**", fence(m["pinned_comment"]), "",
             f"**Video facts:** {tl.total:.1f} s, 1080x1920. Made for kids: No. Cover: `{os.path.basename(path).replace('_upload_sheet.md', '_cover.png')}` "
             "(text kept inside the 3:4 grid crop)."]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {path}", file=sys.stderr)


def still(name, t, out):
    build_timeline(name)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    draw(s, int(t * FPS))
    s.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def cover(name, out):
    """The cover: the video module's cover(cr) drawing (dark poster, one subject, at most three words)."""
    mod, _ = build_timeline(name)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    mod.cover(cairo.Context(s))
    s.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def sheet(name, step, out, cols=8, thumb=180):
    _, tl = build_timeline(name)
    times = [i * step for i in range(int(tl.total / step) + 1)]
    th = int(thumb * H / W)
    rows = (len(times) + cols - 1) // cols
    sh = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * thumb, rows * (th + 24))
    sc = cairo.Context(sh)
    sc.set_source_rgb(1, 1, 1)
    sc.paint()
    fr = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for k, t in enumerate(times):
        draw(fr, int(t * FPS))
        x, y = (k % cols) * thumb, (k // cols) * (th + 24)
        sc.save()
        sc.translate(x, y)
        sc.scale(thumb / W, th / H)
        sc.set_source_surface(fr)
        sc.paint()
        sc.restore()
        sc.set_source_rgb(0, 0, 0)
        sc.set_font_size(16)
        sc.move_to(x + 6, y + th + 18)
        sc.show_text(f"{t:.1f}s")
    sh.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--voice", action="store_true", help="only generate and check the narration")
    ap.add_argument("--still", type=float)
    ap.add_argument("--sheet", type=float)
    ap.add_argument("--cover", action="store_true")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--remix", action="store_true", help="rebuild only the soundtrack onto the last render")
    a = ap.parse_args()
    os.makedirs(BUILD, exist_ok=True)
    if a.voice:
        build_timeline(a.video)
    elif a.remix:
        remix(a.video)
    elif a.cover:
        cover(a.video, os.path.join(OUT, f"{a.video}_cover.png"))
    elif a.still is not None:
        still(a.video, a.still, os.path.join(BUILD, f"{a.video}_still_{a.still}.png"))
    elif a.sheet:
        sheet(a.video, a.sheet, os.path.join(BUILD, f"{a.video}_sheet.png"))
    else:
        render(a.video, audio=not a.no_audio)
