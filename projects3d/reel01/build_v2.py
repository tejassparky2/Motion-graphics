"""3D business reel 01, v2: same approved voice-over, with motion graphics and a more polished edit.

  python projects3d/reel01/build_v2.py MEDIA_DIR          # -> out/3d/reel01_v2.mp4 (needs out/voiceover/reel01.*)

Adds to v1: kinetic hook text, a PHOTO -> DESIGN -> PRINT progress tracker, a scan transition from the photo to the
render, counting stat cards, a print progress bar, brand-colour wipe transitions with whooshes, a light sweep and
sparkles on the reveal, word-by-word highlighted captions, a light grade + vignette, and a staggered end card with
the website. Everything is drawn here with PIL; music and sound effects are synthesized (motion/audio.py).
"""
import math
import os
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as v1                      # noqa: E402  (helpers + image fixes from v1)
from build import W, H, FPS, ROOT, CLEAN, font, media, read_srt, wrap   # noqa: E402
from motion import audio as synth       # noqa: E402

NAME = "reel01_v2"
ORANGE, DARK, CREAM, WHITE = (245, 166, 35), (30, 22, 18), (250, 247, 243), (255, 255, 255)
GREEN = (37, 211, 102)
WEBSITE = "yours3dindia.com"
HANDLE = "@yours3dindia"
CAP_Y = 1320
WIPE = 6                # frames each side of a cut covered by the wipe


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def back(x):            # ease-out with a small overshoot, for pops
    x = min(1.0, max(0.0, x))
    c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------- look ----------

_vig = None


def grade(frame):
    """Slightly richer colour and contrast plus a soft vignette."""
    global _vig
    if _vig is None:
        y, x = np.mgrid[0:H, 0:W]
        r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.7)) ** 2)
        _vig = (1 - 0.32 * np.clip(r - 0.35, 0, 1) ** 1.5)[..., None]
    a = np.asarray(frame).astype(np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 1.12                      # saturation
    a = (a - 128) * 1.06 + 128                  # contrast
    return Image.fromarray(np.clip(a * _vig, 0, 255).astype(np.uint8))


def zoom_in_from(frame, age, amount=0.07, dur=0.35):
    """Incoming shot settles from a slight zoom (pairs with the wipe)."""
    if age >= dur:
        return frame
    z = 1 + amount * (1 - ease(age / dur))
    cw, ch = W / z, H / z
    return frame.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))


def wipe(frame, k):
    """Diagonal brand wipe; k = frames from the cut (-WIPE..WIPE). Fully covers the frame at the cut."""
    p = (k + WIPE) / (2 * WIPE)                    # 0..1
    d = ImageDraw.Draw(frame)
    span = W + H * 0.6
    for col, lag in ((ORANGE, 0.0), (DARK, 0.12)):
        lead = ease(min(1, (p - lag) * 2)) if p < 0.5 + lag else 1
        tail = ease(max(0, (p - 0.5 - lag) * 2))
        x0, x1 = -H * 0.6 + tail * span * 1.1, -H * 0.6 + lead * span * 1.1
        if x1 > x0:
            d.polygon([(x0, H), (x1, H), (x1 + H * 0.6, 0), (x0 + H * 0.6, 0)], fill=col)
    return frame


def light_sweep(frame, age, dur=0.9):
    if not 0 <= age < dur:
        return frame
    x = -400 + (W + 800) * ease(age / dur)
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).polygon([(x - 120, H), (x + 60, H), (x + 60 + 700, 0), (x - 120 + 700, 0)], fill=110)
    band = band.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(Image.new("RGB", (W, H), WHITE), frame, band)


def sparkles(frame, age, seed=3, dur=1.4):
    if not 0 <= age < dur:
        return frame
    r = np.random.default_rng(seed)
    d = ImageDraw.Draw(frame)
    for i in range(16):
        cx, cy = r.uniform(140, W - 140), r.uniform(420, 1250)
        t0 = r.uniform(0, 0.6)
        a = (age - t0) / 0.6
        if 0 <= a < 1:
            s = 26 * math.sin(math.pi * a) * r.uniform(0.6, 1.2)
            col = ORANGE if i % 3 == 0 else WHITE
            d.polygon([(cx, cy - s), (cx + s * 0.22, cy - s * 0.22), (cx + s, cy), (cx + s * 0.22, cy + s * 0.22),
                       (cx, cy + s), (cx - s * 0.22, cy + s * 0.22), (cx - s, cy), (cx - s * 0.22, cy - s * 0.22)],
                      fill=col)
    return frame


# ---------- graphics ----------

def pill(frame, text, y, age, color=ORANGE, size=58, dark_text=None, slide=40, x=None):
    """Rounded label that slides up and fades in."""
    if age < 0:
        return
    a = ease(age / 0.3)
    f = font(size)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=f)
    cx = W / 2 if x is None else x
    yy = y + slide * (1 - a)
    pad, hh = 36, size * 0.78
    d.rounded_rectangle((cx - tw / 2 - pad, yy - hh, cx + tw / 2 + pad, yy + hh), radius=hh, fill=color + (255,))
    light = sum(color) > 400 if dark_text is None else dark_text
    d.text((cx, yy), text, font=f, fill=DARK if light else WHITE, anchor="mm")
    if a < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(layer, (0, 0), layer)


def hook_text(frame, age):
    """'From ONE photo...' -- words pop in one by one, ONE in orange and bigger."""
    words = [("From", WHITE, 92), ("ONE", ORANGE, 128), ("photo...", WHITE, 92)]
    d = ImageDraw.Draw(frame)
    widths = [d.textlength(w, font=font(s)) for w, _, s in words]
    x = W / 2 - (sum(widths) + 30 * (len(words) - 1)) / 2
    for i, ((w, col, s), wd) in enumerate(zip(words, widths)):
        a = age - 0.12 * i
        if a > 0:
            sc = back(a / 0.28)
            f = font(max(8, int(s * sc)))
            d.text((x + wd / 2, 300), w, font=f, fill=col, anchor="mm", stroke_width=8, stroke_fill=DARK)
        x += wd + 30


def tracker(frame, step, prog, alpha=1.0):
    """PHOTO -> DESIGN -> PRINT progress tracker. step: 0..2 active node; prog: 0..1 fill of the whole line."""
    if alpha <= 0:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    labels = ["PHOTO", "DESIGN", "PRINT"]
    xs, y = [250, 540, 830], 215
    d.rounded_rectangle((120, y - 62, W - 120, y + 78), radius=40, fill=(20, 15, 12, 170))
    d.line((xs[0], y, xs[2], y), fill=(255, 255, 255, 90), width=8)
    d.line((xs[0], y, xs[0] + (xs[2] - xs[0]) * ease(prog), y), fill=ORANGE + (255,), width=8)
    for i, (x, lb) in enumerate(zip(xs, labels)):
        done, active = i < step or prog >= 0.999, i == step
        r = 24 if active else 18
        d.ellipse((x - r, y - r, x + r, y + r), fill=(ORANGE if (done or active) else (90, 80, 72)) + (255,),
                  outline=WHITE + (255,), width=4)
        if done:
            d.line((x - 9, y, x - 2, y + 8, x + 11, y - 8), fill=DARK + (255,), width=5)
        d.text((x, y + 50), lb, font=font(30), fill=(WHITE if (done or active) else (190, 180, 170)) + (255,),
               anchor="mm")
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    frame.paste(layer, (0, 0), layer)


def stat_card(frame, x, y, value, unit, age, fmt="{:,.0f}"):
    """Card with a number that counts up."""
    if age < 0:
        return
    a = ease(age / 0.3)
    n = value * ease(age / 0.8)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = y + 40 * (1 - a)
    d.rounded_rectangle((x - 215, yy - 85, x + 215, yy + 85), radius=34, fill=CREAM + (245,))
    d.rounded_rectangle((x - 215, yy - 85, x - 199, yy + 85), radius=8, fill=ORANGE + (255,))
    d.text((x + 8, yy - 18), fmt.format(n), font=font(84), fill=DARK + (255,), anchor="mm")
    d.text((x + 8, yy + 50), unit, font=font(30), fill=(120, 95, 70, 255), anchor="mm")
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(layer, (0, 0), layer)


def print_bar(frame, prog, age):
    if age < 0:
        return
    a = ease(age / 0.3)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = 420 + 40 * (1 - a)
    d.rounded_rectangle((150, y - 70, W - 150, y + 70), radius=34, fill=(20, 15, 12, 200))
    d.text((190, y - 25), "PRINTING", font=font(40), fill=WHITE + (255,), anchor="lm")
    d.text((W - 190, y - 25), f"{int(prog * 100)}%  ·  1.5x", font=font(36), fill=ORANGE + (255,), anchor="rm")
    d.rounded_rectangle((190, y + 18, W - 190, y + 42), radius=12, fill=(255, 255, 255, 60))
    d.rounded_rectangle((190, y + 18, 190 + (W - 380) * max(0.03, prog), y + 42), radius=12, fill=ORANGE + (255,))
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(layer, (0, 0), layer)


def globe(d, cx, cy, r, col):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=4)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline=col, width=3)
    d.line((cx - r, cy, cx + r, cy), fill=col, width=3)


def web_pill(frame, y, age):
    if age < 0:
        return
    pill(frame, "      " + WEBSITE, y, age, color=DARK, size=54)
    a = ease(age / 0.3)
    d = ImageDraw.Draw(frame)
    tw = d.textlength("      " + WEBSITE, font=font(54))
    globe(d, W / 2 - tw / 2 + 30, y + 40 * (1 - a), 21, ORANGE)


def karaoke(frame, words, t, y=CAP_Y, age=1.0):
    """Caption with the word being spoken in orange. words: [(word, start, end)]."""
    d = ImageDraw.Draw(frame)
    size = 70 if age > 0.12 else int(70 * (0.85 + 0.15 * age / 0.12))
    f = font(size)
    text = " ".join(w for w, _, _ in words)
    lines = wrap(d, text, f, 900)
    lh = size * 1.18
    y0 = y - lh * (len(lines) - 1) / 2
    k = 0
    for i, ln in enumerate(lines):
        n = len(ln.split())
        lw = d.textlength(ln, font=f)
        x = W / 2 - lw / 2
        for w, s, e in words[k:k + n]:
            on = s <= t < e + 0.08
            d.text((x, y0 + i * lh), w, font=f, fill=ORANGE if on else WHITE, anchor="lm", stroke_width=7,
                   stroke_fill=(20, 16, 14))
            x += d.textlength(w + " ", font=f)
        k += n


def scan(photo, render, n, dur=0.9):
    """The photo turns into the render under a glowing scan line, then a slow push-in on the render."""
    still = list(v1.image_frames(render, n, "contain", bg=WHITE))
    ph = v1.cover(photo)
    for k in range(n):
        t = k / FPS
        fr = still[k]
        if t < dur:
            y = int(H * ease(t / dur))
            fr = fr.copy()
            fr.paste(ph.crop((0, y, W, H)), (0, y))
            glow = Image.new("L", (W, H), 0)
            ImageDraw.Draw(glow).rectangle((0, y - 6, W, y + 6), fill=255)
            glow = glow.filter(ImageFilter.GaussianBlur(14))
            fr = Image.composite(Image.new("RGB", (W, H), ORANGE), fr, glow)
            ImageDraw.Draw(fr).line((0, y, W, y), fill=WHITE, width=4)
        yield fr


# ---------- word timings ----------

def word_timings(wav, cues):
    """Per cue: [(word, start, end)] from Whisper word timestamps, falling back to spreading by length."""
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="en", word_timestamps=True)
    heard = [(w.start, w.end) for s in segs for w in s.words]
    out = []
    for c0, c1, txt in cues:
        ws = txt.split()
        got = [h for h in heard if h[0] >= c0 - 0.15 and h[1] <= c1 + 0.25]
        if len(got) == len(ws):
            out.append([(w, s, e) for w, (s, e) in zip(ws, got)])
        else:
            lens = np.cumsum([0] + [len(w) + 1 for w in ws])
            tt = c0 + (c1 - c0) * lens / lens[-1]
            out.append([(w, tt[i], tt[i + 1]) for i, w in enumerate(ws)])
    return out


# ---------- build ----------

def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", "reel01")
    voice, sr = soundfile.read(vo + ".wav")
    cues = read_srt(vo + ".srt")
    words = word_timings(vo + ".wav", cues)
    texts = [c[2] for c in cues]
    i7 = texts.index("And here it is.")
    cut = (cues[i7 - 1][1] + cues[i7][0]) / 2
    k = int(cut * sr)
    voice = np.concatenate([voice[:k], np.zeros(int(v1.PRINTER_GAP * sr)), voice[k:],
                            np.zeros(int(v1.END_HOLD * sr))])
    for c, ws in zip(cues[i7:], words[i7:]):
        c[0] += v1.PRINTER_GAP
        c[1] += v1.PRINTER_GAP
        ws[:] = [(w, s + v1.PRINTER_GAP, e + v1.PRINTER_GAP) for w, s, e in ws]
    total = len(voice) / sr
    st = lambda txt: cues[texts.index(txt)][0]   # noqa: E731

    photo = ImageOps.exif_transpose(Image.open(media(mdir, "2cd4a06f"))).convert("RGB")
    render = ImageOps.exif_transpose(Image.open(media(mdir, "659bad04"))).convert("RGB")
    comp = v1.fix_comparison(media(mdir, "1ce678f6"))
    t_b, t_c, t_d = st("Just this one."), st("First, I turn it into a cartoon-style 3D design."), \
        st("Then the printer gets to work.")
    t_f, t_g, t_h, end = st("And here it is."), st("Single figures too."), st("Couples."), st("Want one?")
    # (start, frames factory, graded?, wipe into this scene?, caption y)
    scenes = [
        (0.0, lambda n: v1.video_frames(media(mdir, "170721"), n, fit=True), True, False, CAP_Y),
        (t_b, lambda n: v1.image_frames(photo, n), True, True, CAP_Y),
        (t_c, lambda n: scan(photo, render, n), False, False, CAP_Y),
        (t_d, lambda n: v1.image_frames(v1.fix_slicer(media(mdir, "1988096a")), n, "contain", top=560,
                                        zoom=(1.0, 1.05)), False, True, 1420),
        (cut, lambda n: v1.video_frames(media(mdir, "WA0007"), n, start=1.0, speed=v1.PRINTER_SPEED), True, True,
         CAP_Y),
        (t_f, lambda n: v1.video_frames(media(mdir, "170901"), n), True, True, CAP_Y),
        (t_g, lambda n: v1.video_frames(media(mdir, "170732"), n, fit=True), True, True, 420),
        (t_h, lambda n: v1.video_frames(media(mdir, "170757"), n, fit=True), True, True, CAP_Y),
        (end, lambda n: v1.image_frames(comp, n, "contain", bg=CREAM, zoom=(1.0, 1.03), top=330), False, True,
         CAP_Y),
    ]
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    cuts = [b for b, s in zip(bounds, scenes) if s[3]]

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "7M", "-bufsize", "14M",
                            "-pix_fmt", "yuv420p", *CLEAN, silent], stdin=subprocess.PIPE)
    pops = []    # times of sound-effect pops (graphics appearing)
    f = 0
    for si, ((s0, make, graded, _, cap_y), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        for frame in make(b - a):
            t = f / FPS
            fr = grade(frame) if graded else frame.copy()
            fr = zoom_in_from(fr, t - a / FPS) if scenes[si][3] else fr

            if si == 0:
                hook_text(fr, t - 0.1)
            if si == 5:
                fr = light_sweep(fr, t - t_f)
                fr = sparkles(fr, t - t_f - 0.1)
            # PHOTO -> DESIGN -> PRINT tracker from the photo until the reveal
            if t_b <= t < t_f + 0.6:
                step = 0 if t < t_c else 1 if t < t_d else 2
                prog = 0 if t < t_c else 0.5 * ease((t - t_c) / 0.6) if t < t_d else \
                    0.5 + 0.5 * ease((t - t_d) / (t_f - t_d))
                tracker(fr, step, prog, alpha=min(1, (t - t_b) / 0.2, (t_f + 0.6 - t) / 0.3))
            if si == 3:
                stat_card(fr, 300, 420, 11, "HOURS", t - st("Eleven hours."))
                stat_card(fr, 780, 420, 1580, "COLOUR CHANGES", t - st("Over fifteen hundred colour changes."))
            if si == 4:
                print_bar(fr, (t - cut) / (t_f - cut), t - cut)
            if si == 8:
                pill(fr, HANDLE, 210, t - end, color=DARK, size=60)
                pill(fr, "COMMENT TO GET A DM", 1135, t - st("Comment below to get a DM."), size=54)
                pill(fr, "FREE PREVIEW ON WHATSAPP", 1240, t - st("Free previews on WhatsApp."), color=GREEN,
                     size=50, dark_text=True)
                pill(fr, "+91 91647 48401", 1340, t - st("Free previews on WhatsApp.") - 0.12, color=GREEN, size=50,
                     dark_text=True)
                web_pill(fr, 1445, t - st("Free previews on WhatsApp.") - 0.5)
            if t < end:
                for (c0, c1, _), ws in zip(cues, words):
                    if c0 <= t < c1 + 0.15:
                        karaoke(fr, ws, t, cap_y, t - c0)
            for c in cuts:
                if -WIPE <= f - c < WIPE:
                    fr = wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()
    pops = [st("Eleven hours."), st("Over fifteen hundred colour changes."), end,
            st("Comment below to get a DM."), st("Free previews on WhatsApp."), st("Free previews on WhatsApp.") + 0.5]

    # soundtrack: voice + ducked music + printer sound + whooshes on wipes, pops on graphics, a hit on the reveal
    n = len(voice)
    music = synth.music(total + 1, seed="3d-reel01")
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
        add(synth.sfx("whoosh", 0.45), c / FPS - 0.22, 0.22)
    for p in pops:
        add(synth.sfx("pop", 0.15), p, 0.18)
    add(synth.sfx("hit", 0.4), t_f, 0.15)
    pr = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", "1.0", "-i", media(mdir, "WA0007"), "-t",
                                  str(v1.PRINTER_GAP * v1.PRINTER_SPEED), "-af", f"atempo={v1.PRINTER_SPEED}",
                                  "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    pr = np.frombuffer(pr, np.float32).astype(float)
    pr = pr / max(1e-6, np.abs(pr).max()) * 0.25
    fade = np.minimum(1, np.minimum(np.arange(len(pr)), np.arange(len(pr))[::-1]) / (0.2 * sr))
    k = int(cut * sr)
    mix[k:k + len(pr)] += (pr * fade)[: n - k]
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
