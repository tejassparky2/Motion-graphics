"""Reel 03 (Yours3D): "How to order your custom figurine on WhatsApp" -- 7 steps on the owner's real WhatsApp bot
chat (two screen recordings), in the Yours3D brand, with a step progress bar, punch-in zooms on the key messages,
couple price cards (labelled; single figurines from ₹3,599) and the logo end card.

  NARRATOR_ENGINE=clone python tools/voiceover.py projects3d/reel03/script.txt reel03 --engine turbo --flow --gap 0.9 --polish
  python projects3d/reel03/build.py MEDIA_DIR          # -> out/3d/reel03.mp4
"""
import importlib.util
import os
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reel02_build", os.path.join(HERE, "..", "reel02", "build.py"))
r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r2)
v1, v2 = r2.v1, r2.v2
W, H, FPS, ROOT, CLEAN = r2.W, r2.H, r2.FPS, r2.ROOT, r2.CLEAN
GOLD, GOLD_LIGHT, INK, WHITE, GREEN = r2.GOLD, r2.GOLD_LIGHT, r2.INK, r2.WHITE, r2.GREEN
font = r2.font

NAME = "reel03"
r2.PHONE_TOP, r2.PHONE_H = 330, 960       # leave room for the step bar above and the step label below
CAP_TOP = 262
STEPS = ["SAY HI", "TELL US WHAT YOU WANT", "SEND ONE PHOTO", "2 FREE PREVIEWS", "PICK & ASK FOR CHANGES",
         "SIZE & NAMES", "CONFIRM"]


def pill(frame, text, y, age, color, fnt, dark=True):
    """Like v2.pill but with any font (Caladea has no ₹ sign)."""
    if age < 0:
        return
    a = v2.ease(age / 0.3)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = d.textlength(text, font=fnt)
    yy, hh = y + 40 * (1 - a), fnt.size * 0.78
    d.rounded_rectangle((W / 2 - tw / 2 - 36, yy - hh, W / 2 + tw / 2 + 36, yy + hh), radius=hh, fill=color + (255,))
    d.text((W / 2, yy), text, font=fnt, fill=INK if dark else WHITE, anchor="mm")
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(layer, (0, 0), layer)


def step_bar(frame, step, prog):
    """7 segments across the top; done ones gold, the current one filling."""
    d = ImageDraw.Draw(frame)
    x0, x1, y, gap = 90, W - 90, 130, 12
    seg = (x1 - x0 - gap * 6) / 7
    for i in range(7):
        a = x0 + i * (seg + gap)
        d.rounded_rectangle((a, y - 6, a + seg, y + 6), radius=6, fill=(70, 66, 60))
        fill = 1.0 if i < step else (prog if i == step else 0)
        if fill > 0:
            d.rounded_rectangle((a, y - 6, a + seg * fill, y + 6), radius=6, fill=GOLD)
    d.text((W / 2, y + 42), f"STEP {step + 1} OF 7", font=ImageFont.truetype(r2.SERIF_REG, 30), fill=GOLD_LIGHT,
           anchor="mm")


def punch(frame, focus_y, z):
    """Camera-style punch-in toward a point on the phone (z = 1.0 .. ~1.4)."""
    if z <= 1.001:
        return frame
    cw, ch = W / z, H / z
    cx, cy = W / 2, np.clip(focus_y, ch / 2, H - ch / 2)
    return frame.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))


def zoom_curve(p, at, hold=0.35, z=1.2):
    """0 -> z around fraction `at` of a scene, holding for `hold`, easing in and out."""
    if p < at:
        return 1 + (z - 1) * v2.ease((p - at + 0.12) / 0.12) if p > at - 0.12 else 1.0
    if p < at + hold:
        return z
    return 1 + (z - 1) * (1 - v2.ease((p - at - hold) / 0.12))


def sentence_at(ws, t):
    """The sentence of a caption cue that is being spoken at time t (captions stay at 1-2 lines)."""
    groups, cur = [], []
    for w in ws:
        cur.append(w)
        if w[0][-1] in ".?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    pick = groups[0]
    for g in groups:
        if g[0][1] <= t + 0.05:
            pick = g
    return pick


def couple_cards(frame, age):
    d = ImageDraw.Draw(frame)
    a = v2.ease(age / 0.3)
    if a > 0:
        d.text((W / 2, 1318), "COUPLE FIGURINE", font=ImageFont.truetype(r2.SERIF_REG, 30), fill=GOLD_LIGHT,
               anchor="mm")
    r2.price_cards(frame, age)


def end_card(frame, t, t0):
    r2.logo_build(frame, t - t0 - 0.1)
    d = ImageDraw.Draw(frame)
    a = v2.ease((t - t0 - 1.5) / 0.4)
    if a > 0:
        col = tuple(int(INK[i] + (GOLD[i] - INK[i]) * a) for i in range(3))
        d.text((W / 2, 790), "Yours3D", font=ImageFont.truetype(r2.SERIF_REG, 120), fill=col, anchor="mm")
        d.line((W / 2 - 60 * a, 875, W / 2 + 60 * a, 875), fill=col, width=3)
        d.text((W / 2, 925), "3 D   P R I N T I N G   S T U D I O   ·   I N D I A",
               font=ImageFont.truetype(r2.SERIF_REG, 30), fill=col, anchor="mm")
    pill(frame, "STARTING FROM ₹3,599", 1040, t - t0 - 1.9, GOLD, ImageFont.truetype(r2.RUPEE, 44))
    pill(frame, "COMMENT TO GET A DM", 1160, t - t0 - 2.1, (40, 38, 36), font(48), dark=False)
    pill(frame, "FREE PREVIEW ON WHATSAPP", 1280, t - t0 - 2.4, GREEN, font(44))
    pill(frame, "+91 91647 48401", 1385, t - t0 - 2.55, GREEN, font(44))


def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", NAME)
    voice, sr = soundfile.read(vo + ".wav")
    cues = v1.read_srt(vo + ".srt")
    words = v2.word_timings(vo + ".wav", cues)
    voice = np.concatenate([voice, np.zeros(int(3.0 * sr))])
    total = len(voice) / sr
    L = [c[0] for c in cues]
    t_end = L[9] - 0.3
    rec1, rec2 = v1.media(mdir, "152901_WhatsApp"), v1.media(mdir, "153010_WhatsApp")
    ph = r2.phone_frames
    # (start, frames factory, step index or None, punch-in (at, focus_y) or None)
    scenes = [
        (0.0, lambda n: r2.clip(v1.media(mdir, "155918"), n, 0.0, speed=1.0), None, None),
        (L[1], lambda n: ph(rec1, n, 0.0, 4.5), 0, (0.45, 520)),
        (L[2], lambda n: ph(rec1, n, 9.0, 25.0), 1, (0.55, 720)),
        (L[3], lambda n: ph(rec1, n, 27.6, 33.6), 2, None),
        (L[4], r2.chain((lambda n: ph(rec1, n, 38.2, 40.2), 0.3), (lambda n: ph(rec2, n, 0.5, 7.5), 0.7)), 3,
         (0.05, 620)),
        (L[5], lambda n: ph(rec2, n, 7.5, 17.5), 4, (0.3, 700)),
        (L[6], r2.chain((lambda n: ph(rec2, n, 18.0, 22.0), 0.5), (lambda n: ph(rec2, n, 32.0, 50.0), 0.5)), 5,
         (0.08, 640)),
        (L[7], lambda n: ph(rec2, n, 50.0, 56.0), 6, (0.4, 640)),
        (L[8], lambda n: ph(rec2, n, 56.0, 61.9), 6, (0.1, 760)),
        (t_end, lambda n: (Image.new("RGB", (W, H), INK) for _ in range(n)), None, None),
    ]
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    cuts = [bounds[i] for i in (1, len(scenes) - 1)]       # wipe into the chat and into the end card

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    f = 0
    for si, ((s0, make, step, zp), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        n = b - a
        for k, frame in enumerate(make(n)):
            t = f / FPS
            p = k / max(1, n - 1)
            fr = frame.copy()
            if zp:
                fr = punch(fr, zp[1], zoom_curve(p, zp[0]))
            if si == 0:
                d = ImageDraw.Draw(fr)
                aa = v2.ease((t - 0.2) / 0.35)
                if aa > 0:
                    d.text((W / 2, 260 + 25 * (1 - aa)), "HOW TO ORDER", font=font(96), fill=WHITE, anchor="mm",
                           stroke_width=8, stroke_fill=INK)
                    d.text((W / 2, 370 + 25 * (1 - aa)), "on WhatsApp", font=font(80), fill=GOLD_LIGHT, anchor="mm",
                           stroke_width=8, stroke_fill=INK)
                pill(fr, "7 EASY STEPS", 1430, t - 0.8, GOLD, font(46))
            if step is not None:
                step_bar(fr, step, p)
                if step == 5 and p < 0.5:
                    couple_cards(fr, t - s0 - 0.2)
                    pill(fr, "SINGLE FIGURINES FROM ₹3,599", 1510, t - s0 - 0.6, (40, 38, 36),
                         ImageFont.truetype(r2.RUPEE, 32), dark=False)
                elif si == 8:
                    pill(fr, "PRINTING STARTS AFTER YOUR APPROVAL", 1420, t - s0 - 0.2, GOLD, font(40))
                elif step == 6:
                    pill(fr, "FREE DELIVERY ACROSS INDIA", 1420, t - s0 - 0.3, GOLD, font(44))
                else:
                    pill(fr, STEPS[step], 1420, t - s0 - 0.2, GOLD, font(46))
            if si == len(scenes) - 1:
                end_card(fr, t, t_end)
            if t < t_end:
                for (c0, c1, _), ws in zip(cues, words):
                    if c0 <= t < c1 + 0.15:
                        sw = sentence_at(ws, t)
                        v2.karaoke(fr, sw, t, CAP_TOP if si else r2.CAP_Y, t - sw[0][1])
            for c in cuts:
                if -v2.WIPE <= f - c < v2.WIPE:
                    fr = v2.wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()

    # soundtrack: voice + the warm bed (beat from step one) + soft pops on each step + whooshes on the wipes
    n = len(voice)
    music = r2.warm_bed(n, sr, beat_from=L[1]) * 0.30
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same")
    duck = np.convolve(1.0 - 0.7 * np.clip(env * 4, 0, 1), np.ones(int(0.1 * sr)) / int(0.1 * sr), "same")
    mix = voice + music * duck
    synth = r2.synth

    def add(sig, at, gain):
        sig = np.interp(np.arange(int(len(sig) * sr / synth.SR)) * synth.SR / sr, np.arange(len(sig)), sig)
        s = int(at * sr)
        if 0 <= s < n:
            mix[s:s + len(sig)] += (sig * gain)[: n - s]

    for c in cuts:
        add(synth.sfx("whoosh", 0.45), c / FPS - 0.22, 0.2)
    for p in L[1:8] + [t_end + 1.9]:
        add(synth.sfx("pop", 0.15), p + 0.2, 0.15)
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
