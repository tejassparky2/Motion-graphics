"""3D business reel 01: photo -> cartoon render -> 3D-printed figurine (Instagram Reels, 1080x1920).

  NARRATOR_ENGINE=clone python tools/voiceover.py projects3d/reel01/script.txt reel01      # owner's cloned voice
  python projects3d/reel01/build.py MEDIA_DIR                                             # -> out/3d/reel01.mp4

MEDIA_DIR holds the owner's uploads (not committed). Every scene is timed from the voice-over's cues, so the
picture always fits the voice. Music is synthesized (motion/audio.py) and ducked under the voice.
"""
import os
import re
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from motion import audio as synth   # noqa: E402

W, H, FPS = 1080, 1920, 30
NAME = "reel01"
FONT = os.path.join(ROOT, "assets", "fonts", "Fredoka-Bold.ttf")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name="]
PRINTER_GAP = 4.0      # seconds of printer footage with no voice
PRINTER_SPEED = 1.5
END_HOLD = 1.2
CAP_Y = 1400           # caption centre: above the Reels caption/buttons zone (bottom ~380 px)
CALLOUT_Y = 300        # callouts below the top bar


def media(d, key):
    hits = [f for f in os.listdir(d) if key in f]
    assert len(hits) == 1, (key, hits)
    return os.path.join(d, hits[0])


def font(size):
    return ImageFont.truetype(FONT, size)


# ---------- image prep ----------

def fix_comparison(path):
    """The 3-step image: replace the 'PIXAR STYLE RENDER' labels (trademark) with '3D CARTOON RENDER'."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    d = ImageDraw.Draw(im)
    pill = im.getpixel((600, 46))
    d.rounded_rectangle((567, 19, 975, 74), radius=27, fill=pill)
    f = font(36)
    t1, t2 = "2. ", "3D CARTOON RENDER"
    w1, w2 = d.textlength(t1, font=f), d.textlength(t2, font=f)
    x = 771 - (w1 + w2) / 2
    d.text((x, 47), t1, font=f, fill=(245, 166, 35), anchor="lm")
    d.text((x + w1, 47), t2, font=f, fill="white", anchor="lm")
    bg = im.getpixel((770, 942))
    d.rectangle((552, 928, 762, 958), fill=bg)
    d.text((554, 943), "3D CARTOON RENDER", font=font(20), fill=(40, 30, 25), anchor="lm")
    return im


def fix_slicer(path):
    """Slicer screenshot: hide the 'Cost' line and crop away the taskbar and the other screenshots."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle((566, 728, 700, 748), fill=im.getpixel((720, 734)))
    return im.crop((270, 380, 990, 1100))


# ---------- scene frame sources ----------

def cover(im, w=W, h=H):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def image_frames(im, n, mode="cover", zoom=(1.0, 1.07), top=None, bg=None):
    """Slow push-in on a still. mode 'cover' fills the frame; 'contain' fits the width over a blurred/solid backdrop."""
    if mode == "cover":
        base = cover(im, int(W * zoom[1]), int(H * zoom[1]))
    else:
        back = Image.new("RGB", (W, H), bg) if bg else cover(im).filter(ImageFilter.GaussianBlur(40)).point(
            lambda v: int(v * 0.55))
        fg = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        y = (H - fg.height) // 2 if top is None else top
        back.paste(fg, (0, y))
        base = back.resize((int(W * zoom[1]), int(H * zoom[1])), Image.LANCZOS)
    for k in range(n):
        z = zoom[0] + (zoom[1] - zoom[0]) * k / max(1, n - 1)
        cw, ch = base.width * zoom[0] / z, base.height * zoom[0] / z
        x, y = (base.width - cw) / 2, (base.height - ch) / 2
        yield base.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def video_frames(path, n, start=0.0, speed=1.0, fit=None):
    """n output frames from a clip, played at `speed` (or slowed/sped to fill exactly n frames when fit=True)."""
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", path]).decode())
    if fit:
        speed = (dur - start - 0.05) / (n / FPS)
    vf = (f"setpts=(PTS-STARTPTS)/{speed},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H},setsar=1")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-i", path, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            last = Image.frombytes("RGB", (W, H), buf)
        yield last
    p.stdout.close()
    p.wait()


# ---------- text ----------

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def caption(frame, text, age):
    """Clean caption: white bold text with a dark outline; pops in over 0.12 s."""
    d = ImageDraw.Draw(frame)
    size = 70 if age > 0.12 else int(70 * (0.85 + 0.15 * age / 0.12))
    f = font(size)
    lines = wrap(d, text, f, 900)
    lh = size * 1.18
    y0 = CAP_Y - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * lh), ln, font=f, fill="white", anchor="mm", stroke_width=7,
               stroke_fill=(20, 16, 14))


def callout(frame, text, y, age, color=(245, 166, 35), size=62):
    """Rounded label that slides down into place."""
    a = min(1.0, age / 0.2)
    d = ImageDraw.Draw(frame)
    f = font(size)
    tw = d.textlength(text, font=f)
    yy = y - 30 * (1 - a)
    pad = 34
    box = (W / 2 - tw / 2 - pad, yy - size * 0.75, W / 2 + tw / 2 + pad, yy + size * 0.75)
    d.rounded_rectangle(box, radius=size * 0.75, fill=color)
    d.text((W / 2, yy), text, font=f, fill=(25, 18, 14), anchor="mm")


# ---------- build ----------

def read_srt(path):
    cues = []
    for block in open(path, encoding="utf-8").read().strip().split("\n\n"):
        ln = block.splitlines()
        a, b = [sum(float(x) * m for x, m in zip(re.split("[:,]", s.strip())[:3], (3600, 60, 1))) +
                int(re.split("[:,]", s.strip())[3]) / 1000 for s in ln[1].split("-->")]
        cues.append([a, b, " ".join(ln[2:])])
    return cues


def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", NAME)
    voice, sr = soundfile.read(vo + ".wav")
    cues = read_srt(vo + ".srt")
    texts = [c[2] for c in cues]
    i7 = texts.index("And here it is.")

    # open a no-voice gap for the printer before "And here it is."
    cut = (cues[i7 - 1][1] + cues[i7][0]) / 2
    k = int(cut * sr)
    voice = np.concatenate([voice[:k], np.zeros(int(PRINTER_GAP * sr)), voice[k:], np.zeros(int(END_HOLD * sr))])
    for c in cues[i7:]:
        c[0] += PRINTER_GAP
        c[1] += PRINTER_GAP
    total = len(voice) / sr
    st = lambda txt: cues[texts.index(txt)][0]   # noqa: E731

    comp = fix_comparison(media(mdir, "1ce678f6"))
    scenes = [  # (start, source factory, callouts [(text, from)])
        (0.0, lambda n: video_frames(media(mdir, "170721"), n, fit=True), [("From ONE photo...", 0.0)]),
        (st("Just this one."), lambda n: image_frames(Image.open(media(mdir, "2cd4a06f")), n), []),
        (st("First, I turn it into a cartoon-style 3D design."),
         lambda n: image_frames(ImageOps.exif_transpose(Image.open(media(mdir, "659bad04"))), n, "contain",
                                bg=(255, 255, 255)), []),
        (st("Then the printer gets to work."),
         lambda n: image_frames(fix_slicer(media(mdir, "1988096a")), n, "contain", top=420, zoom=(1.0, 1.05)),
         [("11 HOURS", st("Eleven hours.")), ("1,580 COLOUR CHANGES", st("Over fifteen hundred colour changes."))]),
        (cut, lambda n: video_frames(media(mdir, "WA0007"), n, start=1.0, speed=PRINTER_SPEED),
         [("PRINTING (1.5x SPEED)", cut)]),
        (st("And here it is."), lambda n: video_frames(media(mdir, "170901"), n, speed=1.0), []),
        (st("Single figures too."), lambda n: video_frames(media(mdir, "170732"), n, fit=True), []),
        (st("Couples."), lambda n: video_frames(media(mdir, "170757"), n, fit=True), []),
        (st("Send me your photo."), lambda n: image_frames(comp, n, "contain", bg=(250, 247, 243), zoom=(1.0, 1.04)),
         [("DM YOUR PHOTO TO ORDER", st("Send me your photo."))]),
    ]

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", *CLEAN, silent], stdin=subprocess.PIPE)
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    f = 0
    for (s0, make, calls), a, b in zip(scenes, bounds, bounds[1:]):
        for frame in make(b - a):
            t = f / FPS
            frame = frame.copy()
            for txt, t0 in calls:
                if t >= t0:
                    callout(frame, txt, CALLOUT_Y + 130 * [c[0] for c in calls].index(txt) if len(calls) > 1
                            else CALLOUT_Y, t - t0)
            for c0, c1, txt in cues:
                if c0 <= t < c1 + 0.15:
                    caption(frame, txt, t - c0)
            enc.stdin.write(frame.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()

    # soundtrack: voice + ducked synth music + the printer's own sound during the gap
    n = len(voice)
    music = synth.music(total + 1, seed="3d-" + NAME)[:n]
    music = np.interp(np.arange(n) * synth.SR / sr, np.arange(len(music)), music) if synth.SR != sr else music
    music = music[:n] / max(1e-6, np.abs(music).max()) * 0.32
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same")
    duck = 1.0 - 0.7 * np.clip(env * 4, 0, 1)
    duck = np.convolve(duck, np.ones(int(0.1 * sr)) / int(0.1 * sr), "same")
    mix = voice + music * duck
    pr = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", "1.0", "-i", media(mdir, "WA0007"), "-t",
                                  str(PRINTER_GAP * PRINTER_SPEED), "-af", f"atempo={PRINTER_SPEED}", "-ac", "1",
                                  "-ar", str(sr), "-f", "f32le", "-"])
    pr = np.frombuffer(pr, np.float32).astype(float)
    pr = pr / max(1e-6, np.abs(pr).max()) * 0.25
    k = int(cut * sr)
    fade = np.minimum(1, np.minimum(np.arange(len(pr)), np.arange(len(pr))[::-1]) / (0.2 * sr))
    mix[k:k + len(pr)] += (pr * fade)[: n - k]
    end_fade = np.clip((total - np.arange(n) / sr) / 0.8, 0, 1)
    mix = mix * np.where(np.arange(n) / sr > total - 0.8, end_fade, 1.0)
    mix *= 0.89 / np.abs(mix).max()
    wav = out + ".mix.wav"
    soundfile.write(wav, mix, sr, subtype="PCM_16")

    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-movflags", "+faststart", "-shortest",
                           *CLEAN, out])
    os.remove(silent)
    os.remove(wav)
    print(f"{out}: {total:.1f} s, {nframes} frames")


if __name__ == "__main__":
    main()
