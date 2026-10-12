"""Reel 02 (Yours3D): "POV: Your trip memory just got a mini version" -- "Your Cute Mini"-style making-of plus the
WhatsApp ordering flow, in the Yours3D brand (gold on near-black, serif type).

  NARRATOR_ENGINE=clone python tools/voiceover.py projects3d/reel02/script.txt reel02 --engine turbo --flow --gap 0.9 --polish
  python projects3d/reel02/build.py MEDIA_DIR          # -> out/3d/reel02.mp4

MEDIA_DIR: the owner's 12 Oct 2026 clips (not committed). Prices, "two free previews in 1-2 minutes" and "free
delivery across India" are the owner's own WhatsApp bot's words (Screen_Recording_*_WhatsAppBusiness.mp4).
"""
import os
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reel01"))
import build as v1                      # noqa: E402
import build_v2 as v2                   # noqa: E402
from build import W, H, FPS, ROOT, CLEAN, media, read_srt   # noqa: E402
from motion import audio as synth       # noqa: E402

NAME = "reel02"
GOLD, GOLD_LIGHT, INK = (201, 168, 108), (230, 205, 150), (17, 18, 20)
WHITE, GREEN = (255, 255, 255), (37, 211, 102)
SERIF = "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf"
RUPEE = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"     # Caladea has no ₹
CAP_Y, CAP_TOP = 1320, 205

# brand the shared motion-graphics helpers
v2.ORANGE, v2.DARK = GOLD, INK
v2.font = lambda size: ImageFont.truetype(SERIF, size)
font = v2.font


def warm(frame):
    """The phone clips are a little dim and cool: lift mid-tones, warm them, then v2's grade + vignette."""
    a = np.asarray(frame).astype(np.float32)
    a = 255 * (a / 255) ** 0.88 * np.array([1.04, 1.0, 0.94])
    return v2.grade(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))


def clip(path, n, start=0.0, end=None, speed=None):
    """n frames from [start, end) of a clip, sped to fit exactly (or at `speed`)."""
    if speed is None:
        dur = (end if end is not None else float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))) - start
        speed = dur / (n / FPS)
    return v1.video_frames(path, n, start=start, speed=speed)


def chain(*parts):
    """Play several (factory, share) parts back to back inside one scene; shares are fractions of its frames."""
    def make(n):
        counts = [int(round(n * s)) for _, s in parts]
        counts[-1] = n - sum(counts[:-1])
        for (fac, _), c in zip(parts, counts):
            yield from fac(c)
    return make


# ---------- phone mock-up for the WhatsApp screen recordings ----------

PHONE_H, PHONE_TOP = 1010, 300
SCREEN_CROP = (0, 80, 1080, 2340)          # drop the status bar (recording icon, notifications)


def phone_frames(path, n, start, end):
    """The screen recording inside a phone frame on the brand background."""
    sw = round(PHONE_H * 1080 / (SCREEN_CROP[3] - SCREEN_CROP[1]))
    x0, b = (W - sw) // 2, 14
    bg = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(bg)
    for r, a in ((620, 26), (420, 40)):     # soft gold glow behind the phone
        d.ellipse((W / 2 - r, PHONE_TOP + PHONE_H / 2 - r, W / 2 + r, PHONE_TOP + PHONE_H / 2 + r),
                  fill=tuple(int(INK[i] + (GOLD[i] - INK[i]) * a / 255) for i in range(3)))
    from PIL import ImageFilter
    bg = bg.filter(ImageFilter.GaussianBlur(90))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((x0 - b, PHONE_TOP - b, x0 + sw + b, PHONE_TOP + PHONE_H + b), radius=54, fill=(38, 38, 42),
                        outline=GOLD, width=3)
    mask = Image.new("L", (sw, PHONE_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, PHONE_H - 1), radius=42, fill=255)
    speed = (end - start) / (n / FPS)
    vf = (f"crop={SCREEN_CROP[2] - SCREEN_CROP[0]}:{SCREEN_CROP[3] - SCREEN_CROP[1]}:{SCREEN_CROP[0]}:{SCREEN_CROP[1]},"
          f"setpts=(PTS-STARTPTS)/{speed},fps={FPS},scale={sw}:{PHONE_H}")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-i", path, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(sw * PHONE_H * 3)
        if len(buf) == sw * PHONE_H * 3:
            last = Image.frombytes("RGB", (sw, PHONE_H), buf)
        fr = bg.copy()
        if last is not None:
            fr.paste(last, (x0, PHONE_TOP), mask)
        yield fr
    p.stdout.close()
    p.wait()


# ---------- graphics ----------

def hook_text(frame, age):
    """'POV:' in gold, then the line in white serif, sliding up word group by word group."""
    if age < 0:
        return
    d = ImageDraw.Draw(frame)
    a = v2.ease(age / 0.3)
    d.text((W / 2, 250 + 20 * (1 - a)), "POV:", font=font(58), fill=GOLD, anchor="mm", stroke_width=5,
           stroke_fill=INK)
    for i, ln in enumerate(["Your trip memory just", "got a mini version"]):
        b = v2.ease((age - 0.15 - 0.15 * i) / 0.3)
        if b > 0:
            d.text((W / 2, 330 + 78 * i + 25 * (1 - b)), ln, font=font(72), fill=WHITE if i == 0 else GOLD_LIGHT,
                   anchor="mm", stroke_width=7, stroke_fill=INK)


def tag(frame, text, y, age, color=GOLD, size=46):
    v2.pill(frame, text, y, age, color=color, size=size, dark_text=True)


def price_cards(frame, age):
    sizes = [("13 cm", "₹5,999"), ("15 cm", "₹6,999"), ("18 cm", "₹7,999")]
    for i, (s, p) in enumerate(sizes):
        a = v2.back((age - 0.12 * i) / 0.35)
        if age - 0.12 * i <= 0:
            continue
        cx, cy = W / 2 + (i - 1) * 330, 1405 + 60 * (1 - min(1, a))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle((cx - 150, cy - 70, cx + 150, cy + 70), radius=26, fill=INK + (240,), outline=GOLD,
                            width=4)
        d.text((cx, cy - 26), s, font=font(40), fill=GOLD_LIGHT + (255,), anchor="mm")
        d.text((cx, cy + 28), p, font=ImageFont.truetype(RUPEE, 42), fill=WHITE + (255,), anchor="mm")
        frame.paste(layer, (0, 0), layer)


_logo = None


def logo_build(frame, age, top=250, width=430, dur=1.4):
    """The Y logo builds up from the bottom in print layers, with a glowing 'nozzle' line at the build edge."""
    global _logo
    if _logo is None:
        im = Image.open(os.path.join(ROOT, "assets", "brand", "y_logo.png")).convert("RGBA")
        im = im.crop(im.getbbox())
        _logo = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if age < 0:
        return
    h = _logo.height
    layers = 14
    p = min(1.0, age / dur)
    shown = int(np.ceil(p * layers)) if p < 1 else layers
    cut = h - int(h * shown / layers)
    x = (W - _logo.width) // 2
    part = _logo.crop((0, cut, _logo.width, h))
    frame.paste(part, (x, top + cut), part)
    if p < 1:
        d = ImageDraw.Draw(frame)
        y = top + cut
        d.line((x - 30, y, x + _logo.width + 30, y), fill=GOLD_LIGHT, width=4)
        d.ellipse((x + _logo.width * (0.5 + 0.45 * np.sin(age * 9)) - 8, y - 8,
                   x + _logo.width * (0.5 + 0.45 * np.sin(age * 9)) + 8, y + 8), fill=WHITE)


def end_card(frame, t, t0):
    logo_build(frame, t - t0 - 0.1)
    d = ImageDraw.Draw(frame)
    a = v2.ease((t - t0 - 1.5) / 0.4)
    if a > 0:
        col = tuple(int(INK[i] + (GOLD[i] - INK[i]) * a) for i in range(3))
        d.text((W / 2, 790), "Yours3D", font=ImageFont.truetype(SERIF_REG, 120), fill=col, anchor="mm")
        d.line((W / 2 - 60 * a, 875, W / 2 + 60 * a, 875), fill=col, width=3)
        d.text((W / 2, 925), "3 D   P R I N T I N G   S T U D I O   ·   I N D I A", font=ImageFont.truetype(
            SERIF_REG, 30), fill=col, anchor="mm")
    v2.pill(frame, "@yours3dindia", 1040, t - t0 - 1.9, color=(40, 38, 36), size=48, dark_text=False)
    v2.pill(frame, "COMMENT TO GET A DM", 1160, t - t0 - 2.1, color=GOLD, size=50, dark_text=True)
    v2.pill(frame, "FREE PREVIEW ON WHATSAPP", 1280, t - t0 - 2.4, color=GREEN, size=44, dark_text=True)
    v2.pill(frame, "+91 91647 48401", 1385, t - t0 - 2.55, color=GREEN, size=44, dark_text=True)


# ---------- build ----------

def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", NAME)
    voice, sr = soundfile.read(vo + ".wav")
    cues = read_srt(vo + ".srt")
    words = v2.word_timings(vo + ".wav", cues)
    texts = [c[2] for c in cues]
    END_HOLD = 3.0          # let the end card breathe after the last line
    voice = np.concatenate([voice, np.zeros(int(END_HOLD * sr))])
    total = len(voice) / sr
    st = lambda txt: cues[texts.index(txt)][0]   # noqa: E731
    L = [c[0] for c in cues]
    t_end = L[8] - 0.3                            # end card starts just before "Comment below to get a DM."
    rec1 = media(mdir, "152901_WhatsApp")
    rec2 = media(mdir, "153010_WhatsApp")
    # (start, frames factory, warm grade?, wipe in?, caption y)
    scenes = [
        (0.0, lambda n: clip(media(mdir, "152343"), n, 0.2, speed=1.0), True, False, CAP_Y),
        (L[1], lambda n: clip(media(mdir, "152321"), n, 0.0, speed=1.0), True, True, CAP_Y),
        (L[2], lambda n: clip(media(mdir, "153133"), n, 1.5, speed=1.4), True, True, CAP_Y),
        (L[3], chain((lambda n: clip(media(mdir, "153348"), n, 2.0, speed=1.6), 0.28),
                     (lambda n: clip(media(mdir, "155428"), n, 0.5, speed=1.0), 0.32),
                     (lambda n: clip(media(mdir, "155838"), n, 1.0, speed=1.6), 0.40)), True, True, CAP_Y),
        (L[4], lambda n: clip(media(mdir, "155918"), n, 0.0, speed=1.0), True, True, CAP_Y),
        (L[5], lambda n: phone_frames(rec1, n, 27.6, 33.6), False, True, CAP_TOP),
        (L[6], chain((lambda n: phone_frames(rec1, n, 38.2, 40.2), 0.25),
                     (lambda n: phone_frames(rec2, n, 0.5, 7.5), 0.75)), False, False, CAP_TOP),
        (L[7], chain((lambda n: phone_frames(rec2, n, 18.6, 22.0), 0.55),
                     (lambda n: phone_frames(rec2, n, 53.0, 60.0), 0.45)), False, False, CAP_TOP),
        (t_end, lambda n: (Image.new("RGB", (W, H), INK) for _ in range(n)), False, True, CAP_Y),
    ]
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    cuts = [b for b, s in zip(bounds, scenes) if s[3]]
    t_free = L[7] + 0.55 * (L[8] - 0.3 - L[7])

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    f = 0
    for si, ((s0, make, graded, wiped, cap_y), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        for frame in make(b - a):
            t = f / FPS
            fr = warm(frame) if graded else frame.copy()
            fr = v2.zoom_in_from(fr, t - a / FPS) if wiped else fr
            if si == 0:
                hook_text(fr, t - 0.1)
            if si == 1:
                tag(fr, "IT STARTS WITH 1 PHOTO", 260, t - L[1] - 0.2)
            if si == 2:
                tag(fr, "3D DESIGN", 260, t - L[2] - 0.2)
            if si == 3:
                tag(fr, "PRINTED IN FULL COLOUR", 260, t - L[3] - 0.2)
            if si == 4:
                fr = v2.light_sweep(fr, t - L[4])
                fr = v2.sparkles(fr, t - L[4] - 0.1)
            if si == 6:
                tag(fr, "2 FREE PREVIEWS  ·  1–2 MIN", 1405, t - L[6] - 0.3)
            if si == 7:
                if t < t_free:
                    price_cards(fr, t - L[7] - 0.2)
                else:
                    tag(fr, "FREE DELIVERY ACROSS INDIA", 1405, t - t_free)
            if si == 8:
                end_card(fr, t, t_end)
            if t < t_end:
                for k, ((c0, c1, _), ws) in enumerate(zip(cues, words)):
                    if c0 <= t < c1 + 0.15 and k > 0:     # the hook line is already the POV title
                        v2.karaoke(fr, ws, t, cap_y, t - c0)
            for c in cuts:
                if -v2.WIPE <= f - c < v2.WIPE:
                    fr = v2.wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()

    # soundtrack: voice + ducked synth music + whooshes on wipes, pops on graphics, a hit on the reveal
    n = len(voice)
    music = synth.music(total + 1, seed="3d-reel02")
    music = np.interp(np.arange(n) * synth.SR / sr, np.arange(len(music)), music)
    music = music / max(1e-6, np.abs(music).max()) * 0.32
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same")
    duck = np.convolve(1.0 - 0.7 * np.clip(env * 4, 0, 1), np.ones(int(0.1 * sr)) / int(0.1 * sr), "same")
    mix = voice + music * duck

    def add(sig, at, gain):
        sig = np.interp(np.arange(int(len(sig) * sr / synth.SR)) * synth.SR / sr, np.arange(len(sig)), sig)
        s = int(at * sr)
        if 0 <= s < n:
            mix[s:s + len(sig)] += (sig * gain)[: n - s]

    for c in cuts:
        add(synth.sfx("whoosh", 0.45), c / FPS - 0.22, 0.2)
    for p in [L[1] + 0.2, L[2] + 0.2, L[3] + 0.2, L[6] + 0.3, L[7] + 0.2, t_free, t_end + 1.9, L[8]]:
        add(synth.sfx("pop", 0.15), p, 0.16)
    add(synth.sfx("hit", 0.4), L[4], 0.15)
    tt = np.arange(n) / sr
    mix *= np.where(tt > total - 0.8, np.clip((total - tt) / 0.8, 0, 1), 1.0)
    mix *= 0.89 / np.abs(mix).max()
    wav = out + ".mix.wav"
    soundfile.write(wav, mix, sr, subtype="PCM_16")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.75:level=false",
                           "-movflags", "+faststart", "-shortest", *CLEAN, out])
    os.remove(silent)
    os.remove(wav)
    print(f"{out}: {total:.1f} s, {nframes} frames")


if __name__ == "__main__":
    main()
