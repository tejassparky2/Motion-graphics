#!/usr/bin/env python3
"""Render a video from videos/<name>.py to MP4 (+ a phone preview and a title/description/tags sheet).

  python render.py --video lucky_charm  # -> out/lucky_charm.mp4, out/lucky_charm_preview.mp4, out/lucky_charm_metadata.md
  python render.py                      # default video: pumpkin_trick
  python render.py --still 12.5         # single frame PNG at t=12.5s (for checking layouts)
  python render.py --sheet 1            # contact sheet, one thumbnail per second
  python render.py --no-audio           # skip the synthesized soundtrack
  python render.py --no-voice           # music + sound effects only, no narration
"""
import argparse
import importlib
import os
import subprocess
import sys

from motion import engine, voice as narrator
from motion.engine import FPS, H, W, cairo
from motion.timeline import Timeline

ROOT = os.path.dirname(os.path.abspath(__file__))

# Output hygiene: no container metadata, no encoder/version tags, and no x264 settings SEI in the video stream.
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name="]


def ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


_tl = []
VIDEO = {}


def load(name):
    mod = importlib.import_module(f"videos.{name}")
    VIDEO.update(name=name, mod=mod)
    narrator.configure(**getattr(mod, "NARRATOR", {}))
    media = external_narration(name)
    if media:
        from motion.timeline import Beat, parse
        lines = []
        for spec in mod.SCRIPT:
            b = Beat(**spec)
            b.units = parse(b.text)
            lines.append(b.spoken_text)
        narrator.use_external(media, lines)
        VIDEO["narration"] = media
        print(f"narration: {media}", file=sys.stderr)
    return mod


NARRATION_EXT = ("wav", "m4a", "mp3", "aac", "mp4", "mov", "webm")


def external_narration(name):
    """Narration recorded elsewhere (the owner's own voice), uploaded as assets/narration/<name>.<ext>,
    or in parts as <name>_1.<ext>, <name>_2.<ext>, ... which are joined in order. None if there isn't any."""
    d = os.path.join(ROOT, "assets", "narration")
    def find(stem):
        return next((os.path.join(d, f"{stem}.{e}") for e in NARRATION_EXT if os.path.exists(os.path.join(d, f"{stem}.{e}"))), None)
    whole = find(name)
    if whole:
        return whole
    parts = []
    while find(f"{name}_{len(parts) + 1}"):
        parts.append(find(f"{name}_{len(parts) + 1}"))
    if not parts:
        return None
    joined = os.path.join(ROOT, "build", f"{name}_narration_joined.wav")
    os.makedirs(os.path.dirname(joined), exist_ok=True)
    ins = [x for p in parts for x in ("-i", p)]
    chain = "".join(f"[{i}:a]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[a]"
    subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", *ins, "-filter_complex", chain, "-map", "[a]",
                           "-ac", "1", "-ar", "44100", joined])
    return joined


def timeline():
    """Synthesize (or load cached) narration and lay out the whole video around it."""
    if not _tl:
        _tl.append(Timeline(VIDEO["mod"].SCRIPT, tail=getattr(VIDEO["mod"], "TAIL", 0.35)))
        _tl[0].report()
    return _tl[0]


def write_metadata(path):
    """Title, description, hashtags and tags for the upload, next to the video."""
    m = getattr(VIDEO["mod"], "METADATA", None)
    if not m:
        return
    tl = timeline()
    with open(path, "w") as f:
        f.write(f"# Upload sheet: {VIDEO['name']}\n\n")
        f.write(f"**Title** ({len(m['title'])} characters)\n```\n{m['title']}\n```\n\n")
        if m.get("alt_titles"):
            f.write("**Alternative titles to test**\n" + "".join(f"- `{x}`\n" for x in m["alt_titles"]) + "\n")
        f.write("**Description**\n```\n" + m["description"].strip() + "\n\n" + " ".join(m["hashtags"]) + "\n```\n\n")
        f.write("**Tags** (paste into YouTube Studio > Tags)\n```\n" + ", ".join(m["tags"]) + "\n```\n\n")
        if m.get("pinned_comment"):
            f.write(f"**Pinned comment**\n```\n{m['pinned_comment']}\n```\n\n")
        words = sum(len(u.spoken) for b in tl.beats for u in b.units)
        voiced = (f"narrated by the channel owner (`{os.path.basename(VIDEO['narration'])}`)" if VIDEO.get("narration")
                  else f"voice `{narrator.VOICE}` at speed {narrator.SPEED}")
        f.write(f"**Video facts:** {tl.total:.1f} s, {words} words of narration, {voiced}. Made for kids: **No**.\n")
    print(f"wrote {path}", file=sys.stderr)


def total_duration():
    return timeline().total


def draw(surface, frame):
    t = frame / FPS
    engine.set_frame(frame)
    cr = cairo.Context(surface)
    VIDEO["mod"].draw(cr, t, timeline())
    surface.flush()


def render_video(out, audio=True, voice=True):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = int(round(total_duration() * FPS))
    silent = out if not audio else os.path.join(ROOT, "build", "video_silent.mp4")
    os.makedirs(os.path.dirname(silent), exist_ok=True)
    cmd = [ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           *([] if audio else CLEAN), "-movflags", "+faststart", silent]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(n):
        draw(surface, i)
        proc.stdin.write(bytes(surface.get_data()))
        if i % FPS == 0:
            print(f"\rrendering {i / FPS:5.1f}s / {n / FPS:.1f}s", end="", file=sys.stderr, flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(file=sys.stderr)
    if audio:
        from motion.audio import build_soundtrack
        wav = os.path.join(ROOT, "build", "soundtrack.wav")
        lufs = build_soundtrack(engine.EVENTS, n / FPS, wav, timeline().clips() if voice else None,
                                seed=VIDEO["name"])
        print(f"soundtrack: {lufs:.1f} LUFS integrated", file=sys.stderr)
        subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy",
                               "-c:a", "aac", "-b:a", "160k", "-shortest", *CLEAN, "-movflags", "+faststart", out])
    print(f"wrote {out}", file=sys.stderr)
    # smaller copy that's easy to send to a phone
    preview = out[:-4] + "_preview.mp4"
    tmp = os.path.join(ROOT, "build", "preview_tmp.mp4")
    subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", out, "-c:v", "libx264", "-crf", "27",
                           "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", *CLEAN, tmp])
    # a stream-copy pass drops the encoder tag that re-encoding writes back
    subprocess.check_call([ffmpeg_bin(), "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN,
                           "-movflags", "+faststart", preview])
    print(f"wrote {preview}", file=sys.stderr)
    write_metadata(out[:-4] + "_metadata.md")


def render_still(t, out):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    draw(surface, int(t * FPS))
    surface.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


def render_sheet(step, out, cols=8, thumb=180):
    times = [i * step for i in range(int(total_duration() / step) + 1)]
    th = int(thumb * H / W)
    rows = (len(times) + cols - 1) // cols
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols * thumb, rows * (th + 24))
    sc = cairo.Context(sheet)
    sc.set_source_rgb(1, 1, 1)
    sc.paint()
    frame = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for k, t in enumerate(times):
        draw(frame, int(t * FPS))
        x, y = (k % cols) * thumb, (k // cols) * (th + 24)
        sc.save()
        sc.translate(x, y)
        sc.scale(thumb / W, th / H)
        sc.set_source_surface(frame)
        sc.paint()
        sc.restore()
        sc.set_source_rgb(0, 0, 0)
        sc.set_font_size(16)
        sc.move_to(x + 6, y + th + 18)
        sc.show_text(f"{t:.1f}s")
    sheet.write_to_png(out)
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default="pumpkin_trick", help="module name in videos/")
    ap.add_argument("--out")
    ap.add_argument("--still", type=float)
    ap.add_argument("--sheet", type=float)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--no-voice", action="store_true")
    a = ap.parse_args()
    load(a.video)
    if a.still is not None:
        render_still(a.still, a.out or os.path.join(ROOT, "build", f"{a.video}_still_{a.still}.png"))
    elif a.sheet:
        render_sheet(a.sheet, a.out or os.path.join(ROOT, "build", f"{a.video}_sheet.png"))
    else:
        render_video(a.out or os.path.join(ROOT, "out", f"{a.video}.mp4"), audio=not a.no_audio, voice=not a.no_voice)
