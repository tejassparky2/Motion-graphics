"""Reel 04 (Yours3D): "My sister's baby turned one" -- the owner's first-birthday figurine of their niece Manya:
her birthday photo, detail zooms (dress, bow, handbag), the 3D design, the colour print, the name plate, the reveal
and a photo-vs-figurine split that matches the details, then WhatsApp + the "from ₹3,599" end card.
The owner's sister agreed to Manya's photo and name being shown (19 Oct 2026); the photo itself is not committed.

  python tools/voiceover.py projects3d/reel04/script.txt reel04 --engine turbo --flow --gap 0.9 --polish
  python projects3d/reel04/build.py MEDIA_DIR          # -> out/3d/reel04.mp4
"""
import importlib.util
import os
import subprocess
import sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r2 = _load("reel02_build", os.path.join(HERE, "..", "reel02", "build.py"))
r3 = _load("reel03_build", os.path.join(HERE, "..", "reel03", "build.py"))
v1, v2 = r2.v1, r2.v2
W, H, FPS, ROOT, CLEAN = r2.W, r2.H, r2.FPS, r2.ROOT, r2.CLEAN
GOLD, GOLD_LIGHT, INK, WHITE, GREEN = r2.GOLD, r2.GOLD_LIGHT, r2.INK, r2.WHITE, r2.GREEN
font = r2.font

NAME = "reel04"
HALF = H // 2
SPLIT_CAP = HALF                         # captions sit on the gold divider in the split-screen scenes

# Points of interest (original pixels). Birthday photo 2766x1856; figurine still (20261019_183012) 3000x4000.
PHOTO = {"full": (1370, 928, 1856), "face": (1330, 640, 1000), "dress": (1340, 1180, 760), "bow": (1380, 340, 820),
         "bag": (1280, 870, 560), "mini": (1330, 700, 1000)}
FIG = {"full": (2050, 2100, 3100), "face": (2120, 1480, 1500), "dress": (1830, 2150, 1100), "bow": (2450, 1150, 1300),
       "bag": (1740, 2350, 760), "mini": (2050, 2100, 3100)}


def _box(im, poi, size):
    cx, cy, ch = poi
    cw = ch * size[0] / size[1]
    if cw > im.width:
        cw, ch = im.width, im.width * size[1] / size[0]
    ch = min(ch, im.height)
    cx = np.clip(cx, cw / 2, im.width - cw / 2)
    cy = np.clip(cy, ch / 2, im.height - ch / 2)
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)


RING = {"bow": (1470, 255)}           # the bow sits at the photo's top edge: ring it where it is
RING_FIG = {"bow": (2530, 1000)}


def view(im, poi, size=(W, H)):
    """Crop of `im` centred on poi = (cx, cy, crop height), at the output aspect, resized to `size`."""
    return im.resize(size, Image.BILINEAR, box=_box(im, poi, size))


def spot(im, poi, size, pt):
    """Where image point pt lands in view(im, poi, size) (the crop is clamped at the image edges)."""
    b = _box(im, poi, size)
    return ((pt[0] - b[0]) * size[0] / (b[2] - b[0]), (pt[1] - b[1]) * size[1] / (b[3] - b[1]))


def glide(a, b, x):
    """Point of interest between a and b at eased fraction x."""
    e = v2.ease(x)
    return tuple(a[i] + (b[i] - a[i]) * e for i in range(3))


def ring(frame, cx, cy, r, age, box=None):
    """Gold ring that draws itself around a detail."""
    if age <= 0:
        return
    a = v2.ease(age / 0.4)
    d = ImageDraw.Draw(frame)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * a, fill=GOLD_LIGHT, width=8)


def groups(ws):
    """[(sentence start, words)] for one caption cue."""
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if w[0][-1] in ".?!":
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [(g[0][1], g) for g in out]


def which(starts, t):
    k = 0
    for i, s in enumerate(starts):
        if t >= s - 0.05:
            k = i
    return k


def fig_frames(path, n, start=0.0, speed=1.0, box=(W, HALF)):
    """A clip cropped to a half-height panel (middle band of the frame)."""
    for fr in r2.clip(path, n, start, speed=speed):
        fr = fr.crop((0, (H - box[1] * W // box[0]) // 2, W, (H + box[1] * W // box[0]) // 2))
        yield fr.resize(box, Image.BILINEAR)


def split(top, bottom, offset=0.0):
    """Top panel over bottom panel with a gold divider; `offset` (0..1) slides the bottom panel in from below."""
    fr = Image.new("RGB", (W, H), INK)
    fr.paste(top, (0, 0))
    if bottom is not None:
        fr.paste(bottom, (0, HALF + int(HALF * offset)))
    ImageDraw.Draw(fr).rectangle((0, HALF - 4, W, HALF + 4), fill=GOLD)
    return fr


def main():
    mdir = sys.argv[1]
    vo = os.path.join(ROOT, "out", "voiceover", NAME)
    voice, sr = soundfile.read(vo + ".wav")
    cues = v1.read_srt(vo + ".srt")
    words = v2.word_timings(vo + ".wav", cues)
    sent = [groups(ws) for ws in words]
    voice = np.concatenate([voice, np.zeros(int(3.0 * sr))])
    total = len(voice) / sr
    L = [c[0] for c in cues]
    t_end = L[10] - 0.3
    md = lambda key: v1.media(mdir, key)          # noqa: E731
    still = lambda key: ImageOps.exif_transpose(Image.open(md(key))).convert("RGB")   # noqa: E731
    photo, render, slicer, fig = still("808397810"), still("IMG_20261014_140855"), still("20261014_202953"), \
        still("20261019_183012")
    d = ImageDraw.Draw(slicer)                      # the slicer's object panel (size, triangle count): soften it
    box = (2080, 2120, 2820, 2440)
    slicer.paste(slicer.crop(box).filter(ImageFilter.GaussianBlur(18)), box[:2])
    slicer_poi = (1650, 1650, 2200)

    def hook(n):
        """Sentence 1: the birthday photo full screen. Sentence 2: it moves up, the figurine rises below."""
        s2 = sent[0][1][0] if len(sent[0]) > 1 else L[0] + 0.5 * (L[1] - L[0])
        k2 = int(round((s2 - L[0]) * FPS))
        figs = fig_frames(md("182700"), n - k2, 0.4, speed=0.8)
        for k in range(n):
            p = k / max(1, n - 1)
            if k < k2:
                yield view(photo, glide(PHOTO["full"], PHOTO["face"], p * 1.2))
            else:
                age = (k - k2) / FPS
                yield split(view(photo, PHOTO["face"], (W, HALF)), next(figs), 1 - v2.ease(age / 0.4))

    def details(n):
        """'Black dress. Little bow. And her tiny white handbag.' -- glide to each detail as it is named."""
        starts = [s for s, _ in sent[2]]
        stops = ["dress", "bow", "bag"]
        for k in range(n):
            t = L[2] + k / FPS
            i = which(starts, t)
            a = PHOTO["full"] if i == 0 else PHOTO[stops[i - 1]]
            fr = view(photo, glide(a, PHOTO[stops[i]], (t - starts[i] + 0.15) / 0.45))
            x, y = spot(photo, PHOTO[stops[i]], (W, H), RING[stops[i]]) if stops[i] == "bow" else (W / 2, H / 2)
            ring(fr, x, y, 260 if stops[i] == "bow" else 330, t - starts[i] - 0.35)
            yield fr

    def design(n):
        m = int(n * 0.55)
        yield from v2.scan(view(photo, PHOTO["full"]), render, m)
        for k in range(n - m):
            yield view(slicer, glide(slicer_poi, (1650, 1600, 1500), k / max(1, n - m - 1)))

    def compare(n):
        """'Same dress. Same bow. Same handbag. Just mini.' -- photo on top, figurine below, same detail."""
        starts = [s for s, _ in sent[7]]
        stops = ["dress", "bow", "bag", "mini"]
        for k in range(n):
            t = L[7] + k / FPS
            i = min(which(starts, t), 3)
            a = ("face" if i == 0 else stops[i - 1])
            x = (t - starts[i] + 0.15) / 0.45
            top = view(photo, glide(PHOTO[a], PHOTO[stops[i]], x), (W, HALF))
            bot = view(fig, glide(FIG[a], FIG[stops[i]], x), (W, HALF))
            fr = split(top, bot)
            if i < 3:
                x, y = spot(photo, PHOTO[stops[i]], (W, HALF), RING[stops[i]]) if i == 1 else (W / 2, HALF / 2)
                ring(fr, x, y, 160 if i == 1 else 210, t - starts[i] - 0.35)
                x, y = spot(fig, FIG[stops[i]], (W, HALF), RING_FIG[stops[i]]) if i == 1 else (W / 2, HALF / 2)
                ring(fr, x, HALF + y, 160 if i == 1 else 210, t - starts[i] - 0.45)
            yield fr

    def whatsapp(n):
        """Blurred, dimmed figurine turning behind the WhatsApp offer."""
        for fr in r2.clip(md("182700"), n, 0.0, speed=0.6):
            yield Image.blend(fr.filter(ImageFilter.GaussianBlur(10)), Image.new("RGB", (W, H), INK), 0.5)

    STEADY = r2.STEADY
    clip = r2.clip
    # (start, frames factory, wipe in?, caption y)
    scenes = [
        (0.0, hook, False, SPLIT_CAP),
        (L[1], lambda n: (view(photo, glide(PHOTO["full"], (1380, 820, 1500), k / max(1, n - 1))) for k in range(n)),
         True, r2.CAP_Y),
        (L[2], details, False, r2.CAP_Y),
        (L[3], design, True, r2.CAP_Y),
        (L[4], r2.chain((lambda n: clip(md("023303"), n, 0.0, 8.6, post=STEADY), 0.36),
                        (lambda n: clip(md("110913"), n, 6.0, 16.5, post=STEADY), 0.34),
                        (lambda n: clip(md("110932"), n, 0.0, 3.2, post=STEADY), 0.30)), True, r2.CAP_Y),
        (L[5], lambda n: clip(md("023315"), n, 0.0, 8.3, post=STEADY), True, 1450),   # clear of the name plate
        (L[6], lambda n: clip(md("182700"), n, 0.0, speed=1.0), True, r2.CAP_Y),
        (L[7], compare, True, SPLIT_CAP),
        (L[8], lambda n: clip(md("183018"), n, 0.0, speed=1.4), True, r2.CAP_Y),
        (L[9], whatsapp, True, r2.CAP_Y),
        (t_end, lambda n: (Image.new("RGB", (W, H), INK) for _ in range(n)), True, r2.CAP_Y),
    ]
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    cuts = [b for b, s in zip(bounds, scenes) if s[2]]
    s_hook2 = sent[0][1][0] if len(sent[0]) > 1 else None

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    pill, tag = r3.pill, r2.tag
    f = 0
    for si, ((s0, make, wiped, cap_y), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        for frame in make(b - a):
            t = f / FPS
            fr = frame.copy()
            fr = v2.zoom_in_from(fr, t - a / FPS) if wiped else fr
            if si == 0:
                tag(fr, "HER 1ST BIRTHDAY GIFT", 250, t - 0.15)
            if si == 1:
                tag(fr, "MANYA  ·  AGE 1", 260, t - L[1] - 0.2)
            if si == 3:
                tag(fr, "3D DESIGN", 260, t - L[3] - 0.2)
            if si == 4:
                tag(fr, "PRINTED IN FULL COLOUR", 260, t - L[4] - 0.2)
            if si == 5:
                tag(fr, "NAME ON THE BASE", 260, t - L[5] - 0.2)
            if si == 6:
                fr = v2.light_sweep(fr, t - L[6])
                fr = v2.sparkles(fr, t - L[6] - 0.1)
            if si == 7:
                tag(fr, "PHOTO", 190, t - L[7] - 0.1, size=34)
                tag(fr, "FIGURINE", HALF + 80, t - L[7] - 0.2, size=34)
            if si == 8:
                tag(fr, "A GIFT TO KEEP FOREVER", 260, t - L[8] - 0.2)
            if si == 9:
                g = sent[9]
                pill(fr, "SEND 1 PHOTO ON WHATSAPP", 620, t - g[min(1, len(g) - 1)][0], GREEN, font(46))
                pill(fr, "2 FREE PREVIEWS  ·  1–2 MIN", 760, t - g[-1][0], GOLD, font(46))
                pill(fr, "+91 91647 48401", 900, t - g[-1][0] - 0.3, GREEN, font(46))
            if si == len(scenes) - 1:
                r3.end_card(fr, t, t_end)
            if t < t_end:
                for (c0, c1, _), ws in zip(cues, words):
                    if c0 <= t < c1 + 0.15:
                        sw = r3.sentence_at(ws, t)
                        v2.karaoke(fr, sw, t, cap_y if (si != 0 or (s_hook2 and t >= s_hook2)) else r2.CAP_Y,
                                   t - sw[0][1])
            for c in cuts:
                if -v2.WIPE <= f - c < v2.WIPE:
                    fr = v2.wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()

    # soundtrack: voice + the warm bed (beat from the print) + whooshes on wipes, pops on labels, a hit on the reveal
    n = len(voice)
    music = r2.warm_bed(n, sr, beat_from=L[4]) * 0.30
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
    if s_hook2:
        add(synth.sfx("whoosh", 0.45), s_hook2 - 0.1, 0.16)
    pops = [0.15, L[1] + 0.2, L[3] + 0.2, L[4] + 0.2, L[5] + 0.2, L[8] + 0.2, t_end + 1.9]
    pops += [s + 0.35 for s, _ in sent[2]] + [s + 0.35 for s, _ in sent[7][:3]] + [s for s, _ in sent[9][1:]]
    for p in pops:
        add(synth.sfx("pop", 0.15), p, 0.15)
    add(synth.sfx("hit", 0.4), L[6], 0.15)
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
