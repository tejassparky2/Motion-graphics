"""3D business reel 01, v3: v2's motion graphics with four added lines that give the graphics room.

  NARRATOR_ENGINE=clone python tools/voiceover.py projects3d/reel01/script_v3.txt reel01_v3
  python projects3d/reel01/build_v3.py MEDIA_DIR          # -> out/3d/reel01_v3.mp4

New over v2: "Now watch the magic." carries the full photo -> render scan; "Layer by layer. Each layer just 0.2
millimetres thin." is voiced over the printer with a 0.2 mm counter; "Made just for you." gets a three-figurine
montage; the website line brings in the yours3dindia.com pill. Captions show 0.2 / yours3dindia.com while the voice
script spells them out so the cloned voice reads them clearly.
"""
import os
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as v1                      # noqa: E402
import build_v2 as v2                   # noqa: E402
from build import W, H, FPS, ROOT, CLEAN, media, read_srt   # noqa: E402
from build_v2 import ORANGE, DARK, CREAM, WHITE, GREEN, HANDLE, CAP_Y, WIPE, ease, back  # noqa: E402
from motion import audio as synth       # noqa: E402

NAME = "reel01_v3"
VOICE = "reel01_v3"
SHOWN = {("zero", "point", "two"): "0.2", ("yours", "3D", "India", "dot", "com."): "yours3dindia.com."}
PRINTER_SPEED = 1.5


def display_words(ws):
    """Merge spelled-out words into what the caption shows (e.g. 'zero point two' -> '0.2')."""
    out, i = [], 0
    while i < len(ws):
        for key, shown in SHOWN.items():
            if tuple(w for w, _, _ in ws[i:i + len(key)]) == key:
                out.append((shown, ws[i][1], ws[i + len(key) - 1][2]))
                i += len(key)
                break
        else:
            out.append(ws[i])
            i += 1
    return out


def card(img, w, h, radius=36, border=8):
    """Photo card with rounded corners and a white border."""
    im = v1.cover(img, w, h)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (w + 2 * border, h + 2 * border), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w + 2 * border - 1, h + 2 * border - 1), radius=radius + border,
                                          fill=WHITE + (255,))
    out.paste(im, (border, border), mask)
    return out


def still(path, at):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(at), "-i", path, "-frames:v", "1",
                                   "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    return v2.grade(Image.frombytes("RGB", (W, H), raw))


def montage(stills, n):
    """Three figurine cards slide up one after another over a dark backdrop, then drift slowly."""
    cw, ch = 316, 560
    cards = [card(s, cw, ch) for s in stills]
    bg = v1.cover(stills[0]).filter(ImageFilter.GaussianBlur(30))
    bg = Image.blend(bg, Image.new("RGB", (W, H), DARK), 0.55)
    xs = [W / 2 - cw - 26, W / 2, W / 2 + cw + 26]
    for k in range(n):
        t = k / FPS
        fr = bg.copy()
        for i, (c, x) in enumerate(zip(cards, xs)):
            a = back((t - 0.12 * i) / 0.45)
            if t - 0.12 * i <= 0:
                continue
            y = 880 + 700 * (1 - a) - 12 * t
            tilt = (-4, 0, 4)[i] * (1 - min(1, t / 1.2)) + (-2, 0, 2)[i]
            cc = c.rotate(tilt, resample=Image.BICUBIC, expand=True)
            fr.paste(cc, (int(x - cc.width / 2), int(y - cc.height / 2)), cc)
        yield fr


def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", VOICE)
    voice, sr = soundfile.read(vo + ".wav")
    cues = read_srt(vo + ".srt")
    words = [display_words(ws) for ws in v2.word_timings(vo + ".wav", cues)]
    texts = [c[2] for c in cues]
    voice = np.concatenate([voice, np.zeros(int(v1.END_HOLD * sr))])
    total = len(voice) / sr
    st = lambda txt: cues[texts.index(txt)][0]   # noqa: E731
    mid = lambda a, b: (cues[texts.index(a)][1] + st(b)) / 2   # noqa: E731

    photo = ImageOps.exif_transpose(Image.open(media(mdir, "2cd4a06f"))).convert("RGB")
    render = ImageOps.exif_transpose(Image.open(media(mdir, "659bad04"))).convert("RGB")
    comp = v1.fix_comparison(media(mdir, "1ce678f6"))
    t_b, t_c = st("Just this one."), st("Now watch the magic.")
    t_d = st("Then the printer gets to work.")
    t_e = mid("Over fifteen hundred colour changes.", "Layer by layer.")
    t_f, t_g, t_h = st("And here it is."), st("Single figures too."), st("Couples.")
    t_m, end = st("Made just for you."), st("Want one?")
    t_web = st("Or order at yours 3D India dot com.")
    scan_dur = st("First, I turn it into a cartoon-style 3D design.") - t_c
    stills = [still(media(mdir, "170721"), 1.5), still(media(mdir, "170732"), 1.5), still(media(mdir, "170757"), 2.0)]
    # (start, frames factory, graded?, wipe into this scene?, caption y)
    scenes = [
        (0.0, lambda n: v1.video_frames(media(mdir, "170721"), n, fit=True), True, False, CAP_Y),
        (t_b, lambda n: v1.image_frames(photo, n), True, True, CAP_Y),
        (t_c, lambda n: v2.scan(photo, render, n, dur=scan_dur), False, False, CAP_Y),
        (t_d, lambda n: v1.image_frames(v1.fix_slicer(media(mdir, "1988096a")), n, "contain", top=560,
                                        zoom=(1.0, 1.05)), False, True, 1420),
        (t_e, lambda n: v1.video_frames(media(mdir, "WA0007"), n, start=0.5, speed=PRINTER_SPEED), True, True,
         CAP_Y),
        (t_f, lambda n: v1.video_frames(media(mdir, "170901"), n), True, True, CAP_Y),
        (t_g, lambda n: v1.video_frames(media(mdir, "170732"), n, fit=True), True, True, 420),
        (t_h, lambda n: v1.video_frames(media(mdir, "170757"), n, fit=True), True, True, CAP_Y),
        (t_m, lambda n: montage(stills, n), False, True, 1420),
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
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    f = 0
    for si, ((s0, make, graded, wiped, cap_y), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        for frame in make(b - a):
            t = f / FPS
            fr = v2.grade(frame) if graded else frame.copy()
            fr = v2.zoom_in_from(fr, t - a / FPS) if wiped else fr
            if si == 0:
                v2.hook_text(fr, t - 0.1)
            if si == 5:
                fr = v2.light_sweep(fr, t - t_f)
                fr = v2.sparkles(fr, t - t_f - 0.1)
            if t_b <= t < t_f + 0.6:
                step = 0 if t < t_c else 1 if t < t_d else 2
                prog = 0 if t < t_c else 0.5 * ease((t - t_c) / scan_dur) if t < t_d else \
                    0.5 + 0.5 * ease((t - t_d) / (t_f - t_d))
                v2.tracker(fr, step, prog, alpha=min(1, (t - t_b) / 0.2, (t_f + 0.6 - t) / 0.3))
            if si == 3:
                v2.stat_card(fr, 300, 420, 11, "HOURS", t - st("Eleven hours."))
                v2.stat_card(fr, 780, 420, 1580, "COLOUR CHANGES", t - st("Over fifteen hundred colour changes."))
            if si == 4:
                v2.print_bar(fr, (t - t_e) / (t_f - t_e), t - t_e)
                v2.stat_card(fr, 540, 640, 0.2, "MM PER LAYER",
                             t - st("Each layer just zero point two millimetres thin."), fmt="{:.1f}")
            if si == 8:
                v2.pill(fr, "MADE JUST FOR YOU", 300, t - t_m, size=60)
            if si == 9:
                v2.pill(fr, HANDLE, 210, t - end, color=DARK, size=60)
                v2.pill(fr, "COMMENT TO GET A DM", 1135, t - st("Comment below to get a DM."), size=54)
                v2.pill(fr, "FREE PREVIEW ON WHATSAPP", 1240, t - st("Free previews on WhatsApp."), color=GREEN,
                        size=50, dark_text=True)
                v2.pill(fr, "+91 91647 48401", 1340, t - st("Free previews on WhatsApp.") - 0.12, color=GREEN,
                        size=50, dark_text=True)
                v2.web_pill(fr, 1445, t - t_web)
            if t < end:
                for (c0, c1, _), ws in zip(cues, words):
                    if c0 <= t < c1 + 0.15:
                        v2.karaoke(fr, ws, t, cap_y, t - c0)
            for c in cuts:
                if -WIPE <= f - c < WIPE:
                    fr = v2.wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()
    pops = [st("Eleven hours."), st("Over fifteen hundred colour changes."),
            st("Each layer just zero point two millimetres thin."), t_m, end, st("Comment below to get a DM."),
            st("Free previews on WhatsApp."), t_web]

    # soundtrack: voice + ducked music + quiet printer sound + whooshes, pops and a reveal hit
    n = len(voice)
    music = synth.music(total + 1, seed="3d-reel01")
    music = np.interp(np.arange(n) * synth.SR / sr, np.arange(len(music)), music)
    music = music / max(1e-6, np.abs(music).max()) * 0.32
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same")
    duck = np.convolve(1.0 - 0.7 * np.clip(env * 4, 0, 1), np.ones(int(0.1 * sr)) / int(0.1 * sr), "same")
    mix = voice + music * duck

    def add(sig, at, gain, rate=synth.SR):
        if rate != sr:
            sig = np.interp(np.arange(int(len(sig) * sr / rate)) * rate / sr, np.arange(len(sig)), sig)
        s = int(at * sr)
        if 0 <= s < n:
            mix[s:s + len(sig)] += (sig * gain)[: n - s]

    for c in cuts:
        add(synth.sfx("whoosh", 0.45), c / FPS - 0.22, 0.22)
    for p in pops:
        add(synth.sfx("pop", 0.15), p, 0.18)
    add(synth.sfx("hit", 0.4), t_f, 0.15)
    dur_e = t_f - t_e
    pr = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", media(mdir, "WA0007"), "-t",
                                  str(dur_e * PRINTER_SPEED), "-af", f"atempo={PRINTER_SPEED}", "-ac", "1",
                                  "-ar", str(sr), "-f", "f32le", "-"])
    pr = np.frombuffer(pr, np.float32).astype(float)
    pr = pr / max(1e-6, np.abs(pr).max()) * 0.12
    pr *= np.minimum(1, np.minimum(np.arange(len(pr)), np.arange(len(pr))[::-1]) / (0.2 * sr))
    add(pr, t_e, 1.0, rate=sr)
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
