#!/usr/bin/env python3
"""Render "The Pumpkin Trick" to MP4.

  python render.py                      # full video -> out/pumpkin_trick.mp4
  python render.py --still 12.5         # single frame PNG at t=12.5s (for checking layouts)
  python render.py --sheet 1            # contact sheet, one thumbnail per second
  python render.py --no-audio           # skip the synthesized soundtrack
  python render.py --no-voice           # music + sound effects only, no narration
"""
import argparse
import os
import subprocess
import sys

from motion import engine
from motion.engine import FPS, H, W, cairo
from motion.scenes import SCRIPT, draw as draw_scene
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


def timeline():
    """Synthesize (or load cached) narration and lay out the whole video around it."""
    if not _tl:
        _tl.append(Timeline(SCRIPT))
        _tl[0].report()
    return _tl[0]


def total_duration():
    return timeline().total


def draw(surface, frame):
    t = frame / FPS
    engine.set_frame(frame)
    cr = cairo.Context(surface)
    draw_scene(cr, t, timeline())
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
        lufs = build_soundtrack(engine.EVENTS, n / FPS, wav, timeline().clips() if voice else None)
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
    ap.add_argument("--out", default=os.path.join(ROOT, "out", "pumpkin_trick.mp4"))
    ap.add_argument("--still", type=float)
    ap.add_argument("--sheet", type=float)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--no-voice", action="store_true")
    a = ap.parse_args()
    if a.still is not None:
        render_still(a.still, a.out if a.out.endswith(".png") else os.path.join(ROOT, "build", f"still_{a.still}.png"))
    elif a.sheet:
        render_sheet(a.sheet, a.out if a.out.endswith(".png") else os.path.join(ROOT, "build", "sheet.png"))
    else:
        render_video(a.out, audio=not a.no_audio, voice=not a.no_voice)
