#!/usr/bin/env python3
"""Render a mythology video from channels/mythology/videos/<name>.py in one language (copied from
channels/hinglish/render_hi.py; the language switch is new).

  python -I -X utf8 channels/mythology/render_myth.py --video kakudmi --lang hi           # -> myth_out/kakudmi_hi.mp4
  python -I -X utf8 channels/mythology/render_myth.py --video kakudmi --lang kn --still 2 # one frame
  python -I -X utf8 channels/mythology/render_myth.py --video kakudmi --lang kn --sheet 1 # one frame per second
  python -I -X utf8 channels/mythology/render_myth.py --video kakudmi --lang kn --check   # Whisper medium, every line
  python -I -X utf8 channels/mythology/render_myth.py --video kakudmi --lang both          # both languages

A video module holds SCRIPTS = {"hi": [...], "kn": [...]} (same line ids in both), METADATA = {"hi": {...},
"kn": {...}}, SHOTS, draw(cr, t, tl) and sfx(tl). Cue words may be {"hi": word, "kn": word}: the timeline carries
its language (tl.lang). Outputs go outside the repo (videos are never committed; the repo is public).
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
import narrate  # noqa: E402
from channel import LANGS, NARRATORS, OUT_ROOT, WHISPER_LANG  # noqa: E402
from poster import FPS, H, W  # noqa: E402

OUT = OUT_ROOT
BUILD = os.path.join(ROOT, "build", "mythology")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name="]

_mod, _tl = None, None


def load_module(name):
    spec = importlib.util.spec_from_file_location(f"mvideo_{name}", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def narrator(mod, lang):
    return getattr(mod, "NARRATORS", NARRATORS)[lang]


def _tl_path(name, lang):
    return os.path.join(BUILD, f"{name}_{lang}_timeline.json")


def build_timeline(name, lang):
    mod = load_module(name)
    tl = narrate.Timeline(mod.SCRIPTS[lang], narrator(mod, lang), tail=getattr(mod, "TAIL", narrate.TAIL))
    tl.lang = lang
    os.makedirs(BUILD, exist_ok=True)
    json.dump(tl.to_json(), open(_tl_path(name, lang), "w", encoding="utf-8"), ensure_ascii=False)
    for b in tl.beats:
        print(f"  {b.id:>4} {b.start:6.2f}-{b.end:6.2f}  {b.text[:60]}", file=sys.stderr)
    print(f"total {tl.total:.1f} s ({lang})", file=sys.stderr)
    return mod, tl


def _init(name, lang):
    global _mod, _tl
    _mod = load_module(name)
    _tl = narrate.Timeline.from_json(json.load(open(_tl_path(name, lang), encoding="utf-8")))
    _tl.lang = lang


def draw(surface, frame):
    cr = cairo.Context(surface)
    _mod.draw(cr, frame / FPS, _tl)
    surface.flush()


def _part(args):
    name, lang, first, last, path = args
    if _mod is None:
        _init(name, lang)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-threads", "1", path]
    # owner, 29 Oct 2026: "i want best qaulity possible no limits" - near-lossless master; phone copies are separate
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(first, last):
        draw(surface, i)
        proc.stdin.write(bytes(surface.get_data()))
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg failed")
    return path


def render(name, lang, audio=True):
    mod, tl = build_timeline(name, lang)
    os.makedirs(OUT, exist_ok=True)
    n = int(round(tl.total * FPS))
    workers = max(1, min(int(os.environ.get("RENDER_WORKERS", (os.cpu_count() or 2) - 2)), 12))
    chunk = max(FPS * 2, n // (workers * 3))
    stem = f"{name}_{lang}"
    jobs = [(name, lang, a, min(n, a + chunk), os.path.join(BUILD, f"{stem}_part{k:03d}.mp4"))
            for k, a in enumerate(range(0, n, chunk))]
    with mp.get_context("spawn").Pool(workers, initializer=_init, initargs=(name, lang)) as pool:
        for k, _ in enumerate(pool.imap(_part, jobs)):
            print(f"\rparts {k + 1}/{len(jobs)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    listing = os.path.join(BUILD, f"{stem}_parts.txt")
    with open(listing, "w") as f:
        f.writelines(f"file '{j[4].replace(os.sep, '/')}'\n" for j in jobs)
    silent = os.path.join(BUILD, f"{stem}_silent.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy",
                           silent])
    for j in jobs:
        os.remove(j[4])
    out = os.path.join(OUT, f"{stem}.mp4")
    if audio:
        mux_audio(stem, mod, tl, n / FPS, silent, out)
    else:
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-c", "copy", *CLEAN, out])
    print(f"wrote {out}", file=sys.stderr)
    write_sheet(mod, tl, os.path.join(OUT, f"{stem}_upload_sheet.md"), lang)
    return out


def mux_audio(stem, mod, tl, total, silent, out):
    """Voice + music bed + sound effects at -14 LUFS, muxed onto the silent picture track (video stream copied)."""
    from motion.audio import build_soundtrack
    wav = os.path.join(BUILD, f"{stem}_soundtrack.wav")
    events = mod.sfx(tl) if hasattr(mod, "sfx") else []
    lufs = build_soundtrack(events, total, wav, tl.clips(), seed=stem, bed=getattr(mod, "MUSIC", "pad"))
    print(f"soundtrack {lufs:.1f} LUFS", file=sys.stderr)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac",
                           "-b:a", "256k", "-shortest", *CLEAN, "-movflags", "+faststart", out])


def remix(name, lang):
    """Only the soundtrack changed (music, effects): rebuild it and remux onto the last render's picture track."""
    mod, tl = build_timeline(name, lang)
    stem = f"{name}_{lang}"
    silent = os.path.join(BUILD, f"{stem}_silent.mp4")
    out = os.path.join(OUT, f"{stem}.mp4")
    mux_audio(stem, mod, tl, int(round(tl.total * FPS)) / FPS, silent, out)
    print(f"wrote {out}", file=sys.stderr)


def _site(c):
    u = c.get("page_url", "")
    s = c.get("source") or ("Wikimedia Commons" if "wikimedia" in u else "Pixabay" if "pixabay" in u
                            else "Unsplash" if "unsplash" in u else "")
    via = re.match(r"openverse(?: \(via |:)(\w+)", s, re.I)       # Openverse only searches: name the real site
    return {"wikimedia": "Wikimedia Commons", "flickr": "Flickr"}.get(via[1], via[1]) if via else s


def _is_cc_by(lic):
    """CC BY in any spelling ("CC BY 4.0", "BY 4.0", "cc-by"): the licences that need the author's name."""
    return re.match(r"(cc[\s-]?)?by\b", lic.strip(), re.I) is not None and not re.search(r"sa|nc|nd", lic, re.I)


def _short_source(src):
    """A source as a name only: no URL, no title in quotes (owner, 29 Oct 2026: "Don't add links in source")."""
    return re.split(r" '|\shttps?://| \(", src)[0].rstrip(", ")


def write_sheet(mod, tl, path, lang):
    m = getattr(mod, "METADATA", {}).get(lang)
    if not m:
        return
    credits = []
    for f in getattr(mod, "CREDITS_FILES", []):
        if os.path.exists(f):
            credits += json.load(open(f, encoding="utf-8"))
    used = set(getattr(mod, "USED_ASSETS", []))
    credits = [c for c in credits if not used or os.path.basename(c["file"]) in used]
    # owner, 29 Oct 2026: picture credits in 1-2 lines saying where they came from, no links; CC BY needs the names
    sites = sorted({_site(c) for c in credits} - {""})
    by = sorted({c["author"].split(" from ")[0].split(" (")[0].rstrip(". ") for c in credits
                 if _is_cc_by(c["license"])})
    photo = (f"Art: {', '.join(sites)}." if sites else "") + (f"\nCC BY: {', '.join(by)}." if by else "")
    sources = "Sources: " + "; ".join(_short_source(x) for x in m.get("sources", []))
    tags = " ".join(m["hashtags"])
    fence = lambda body: f"```\n{body}\n```"
    lines = [f"# Upload sheet ({lang}): {m['title']}", "",
             "**Instagram caption**", fence(f"{m['caption'].strip()}\n\n{tags}"), "",
             "**Instagram second comment** (credits and sources)", fence(f"{photo}\n{sources}".strip()), "",
             "**YouTube title**", fence(m["yt_title"]), "",
             "**YouTube description**", fence(f"{m['yt_description'].strip()}\n\n{sources}\n{photo}\n\n{tags}"), "",
             "**Pinned comment**", fence(m["pinned_comment"]), "",
             f"**Video facts:** {tl.total:.1f} s. Made for kids: No."]   # no voice/AI wording (owner, 29 Oct 2026)
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {path}", file=sys.stderr)


def still(name, lang, t, out):
    build_timeline(name, lang)
    _init(name, lang)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    draw(s, int(t * FPS))
    s.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def sheet(name, lang, step, out, cols=8, thumb=180):
    _, tl = build_timeline(name, lang)
    _init(name, lang)
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


def words(s):
    """Words for the error rate: Devanagari and Kannada vowel signs are not \\w, so both blocks are listed."""
    return re.findall(r"[\wऀ-ॿಀ-೿]+", s.replace("़", "").replace("಼", ""))


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / max(1, len(ref))


def check(name, lang):
    """Whisper medium on every line; flags lines whose word error rate is above 30%. Whisper is much weaker in
    Kannada than in Hindi, so Kannada flags are a pointer for a listen, not a verdict."""
    import librosa
    from asr import whisper
    _, tl = build_timeline(name, lang)
    model = whisper()
    bad = 0
    for b in tl.beats:
        y, _ = librosa.load(b.wav, sr=16000)
        heard = " ".join(s.text for s in model.transcribe(y, language=WHISPER_LANG[lang], beam_size=5)[0])
        w = wer(words(b.text), words(heard))
        flag = w > 0.30
        bad += flag
        print(f"{'!!' if flag else 'ok'} {b.id:>4} WER {w:4.0%}  heard: {heard.strip()}")
    print(f"{bad} line(s) flagged ({lang})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--lang", default="hi", choices=[*LANGS, "both"])
    ap.add_argument("--still", type=float)
    ap.add_argument("--sheet", type=float)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--remix", action="store_true", help="rebuild only the soundtrack onto the last render")
    a = ap.parse_args()
    os.makedirs(BUILD, exist_ok=True)
    for lang in (LANGS if a.lang == "both" else [a.lang]):
        if a.check:
            check(a.video, lang)
        elif a.remix:
            remix(a.video, lang)
        elif a.still is not None:
            still(a.video, lang, a.still, os.path.join(BUILD, f"{a.video}_{lang}_still_{a.still}.png"))
        elif a.sheet:
            sheet(a.video, lang, a.sheet, os.path.join(BUILD, f"{a.video}_{lang}_sheet.png"))
        else:
            render(a.video, lang, audio=not a.no_audio)
