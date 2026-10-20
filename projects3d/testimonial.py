"""Testimonial reels (Yours3D): a customer talks to camera in her own voice; the takes are trimmed tight, joined with
gentle alternating punch-ins (no voice-over), the owner's footage is cut in over her voice, and English captions
follow her words. Used by reel05 and reel06.

A reel is a list of Seg(clip, start, end, caption, broll=[(from, to, factory)], tags=[(text, y, at, colour)]):
  clip/start/end   her take and the part to keep (seconds in that take)
  caption          what she says, as the caption shows it (spelling fixed: "Yours 3D India", "Manya", "figurine")
  broll            cutaways over her voice: seconds into the segment, and a frames factory n -> frames
  hold             extra seconds after the words (picture keeps running, no caption) e.g. a reveal
"""
import importlib.util
import os
import subprocess
from dataclasses import dataclass, field

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r2 = _load("reel02_build", os.path.join(HERE, "reel02", "build.py"))
r3 = _load("reel03_build", os.path.join(HERE, "reel03", "build.py"))
v1, v2 = r2.v1, r2.v2
W, H, FPS, ROOT, CLEAN = r2.W, r2.H, r2.FPS, r2.ROOT, r2.CLEAN
GOLD, GOLD_LIGHT, INK, WHITE, GREEN = r2.GOLD, r2.GOLD_LIGHT, r2.INK, r2.WHITE, r2.GREEN
font = r2.font
SR = 48000
CAP_Y = 1420            # below the figurine she holds at chest height, above the Reels buttons
END_HOLD = 5.5         # logo builds (~2 s), then the price and WhatsApp labels stay ~3 s
VOICE_FX = ("highpass=f=80,afftdn=nf=-28,equalizer=f=200:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1.2:g=2.5,"
            "deesser=i=0.3,acompressor=threshold=0.12:ratio=2.5:attack=10:release=150:makeup=1.4")


@dataclass
class Seg:
    clip: str
    start: float
    end: float
    caption: str
    broll: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    hold: float = 0.0
    hold_frames: object = None      # factory for the hold (defaults to the take continuing)


def words_for(path, start, end, caption, model):
    """Caption words timed to her speech: Whisper word times when the counts match, else spread by length."""
    segs, _ = model.transcribe(path, language="en", word_timestamps=True, clip_timestamps=[start, end])
    got = [(w.start - start, w.end - start) for s in segs for w in s.words if start - 0.1 <= w.start <= end]
    ws = caption.split()
    if len(got) == len(ws):
        return [(w, a, b) for w, (a, b) in zip(ws, got)]
    a0, a1 = (got[0][0], got[-1][1]) if got else (0.05, end - start - 0.1)
    lens = np.cumsum([0] + [len(w) + 1 for w in ws])
    tt = a0 + (a1 - a0) * lens / lens[-1]
    return [(w, tt[i], tt[i + 1]) for i, w in enumerate(ws)]


# iPhone takes are HDR (HLG, BT.2020): read straight they look flat and washed out, and the phone-clip grade then
# pushes them further off. Convert them to standard video (npl 350 keeps her face natural without blowing out the white
# wall) and give only a light finish.
HLG_TO_SDR = "zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=bt709:m=bt709:p=bt709:npl=350"


def is_hdr(path):
    tr = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                  "stream=color_transfer", "-of", "csv=p=0", path]).decode()
    return "arib-std-b67" in tr or "smpte2084" in tr


def soft_finish(fr):
    """Gentle S-curve, a little colour, a touch warmer."""
    a = np.asarray(fr).astype(np.float32) / 255
    a = a + 0.12 * (a * a * (3 - 2 * a) - a)
    g = a.mean(axis=2, keepdims=True)
    a = (g + (a - g) * 1.04) * np.array([1.01, 1.0, 0.985])
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def take_frames(path, n, start):
    if is_hdr(path):
        return (soft_finish(f) for f in v1.video_frames(path, n, start=start, speed=1.0, post=HLG_TO_SDR))
    return r2.clip(path, n, start, speed=1.0)


def talk_frames(path, n, start, zoom):
    """Her take, with a fixed punch-in toward her face (upper part of the frame)."""
    for fr in take_frames(path, n, start):
        if zoom > 1.001:
            cw, ch = W / zoom, H / zoom
            cx, cy = W / 2, max(ch / 2, min(H / 2, 820))      # toward her face, never past the top edge
            fr = fr.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        yield fr


def still_frames(im, n, zoom=(1.0, 1.08), mode="cover"):
    yield from v1.image_frames(im, n, mode=mode, zoom=zoom, bg=WHITE if mode == "contain" else None)


def phone_still(photo, n, title="Yours3D India", appear=0.25):
    """A WhatsApp-style chat in a phone frame: the photo arrives as a sent message."""
    ph_h, top = 1010, 300
    sw = round(ph_h * 1080 / 2260)
    x0 = (W - sw) // 2
    bg = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(bg)
    for r, a in ((620, 26), (420, 40)):
        d.ellipse((W / 2 - r, top + ph_h / 2 - r, W / 2 + r, top + ph_h / 2 + r),
                  fill=tuple(int(INK[i] + (GOLD[i] - INK[i]) * a / 255) for i in range(3)))
    bg = bg.filter(ImageFilter.GaussianBlur(90))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((x0 - 14, top - 14, x0 + sw + 14, top + ph_h + 14), radius=54, fill=(38, 38, 42), outline=GOLD,
                        width=3)
    screen = Image.new("RGB", (sw, ph_h), (236, 229, 221))
    ds = ImageDraw.Draw(screen)
    ds.rectangle((0, 0, sw, 110), fill=(7, 94, 84))
    ds.ellipse((22, 30, 72, 80), fill=GOLD)
    ds.text((47, 55), "Y", font=font(34), fill=INK, anchor="mm")
    ds.text((90, 55), title, font=font(34), fill=WHITE, anchor="lm")
    mask = Image.new("L", (sw, ph_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, ph_h - 1), radius=42, fill=255)
    pw = int(sw * 0.8)
    thumb = ImageOps.fit(photo, (pw, int(pw * 1.25)), Image.LANCZOS)
    for k in range(n):
        t = k / FPS
        scr = screen.copy()
        a = v2.ease((t - appear) / 0.35)
        if a > 0:
            bx1, by1 = sw - 20, ph_h - 90 - 60 * (1 - a)
            bx0, by0 = bx1 - pw - 16, by1 - thumb.height - 16
            ImageDraw.Draw(scr).rounded_rectangle((bx0, by0, bx1, by1), radius=16, fill=(220, 248, 198))
            scr.paste(thumb, (int(bx0 + 8), int(by0 + 8)))
            ImageDraw.Draw(scr).text((bx1 - 14, by1 - 16), "✓✓", font=ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22), fill=(52, 183, 241), anchor="rs")
        fr = bg.copy()
        fr.paste(scr, (x0, top), mask)
        yield fr


def end_card(frame, t, t0, extra=None):
    r3.end_card(frame, t, t0)
    if extra:
        r3.pill(frame, extra, 1490, t - t0 - 2.7, GOLD_LIGHT, ImageFont.truetype(r2.RUPEE, 36))


def build(name, segs, title, end_extra=None):
    from faster_whisper import WhisperModel
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    # timeline
    plan, t = [], 0.0
    for i, s in enumerate(segs):
        dur = s.end - s.start
        plan.append((t, dur, s, words_for(s.clip, s.start, s.end, s.caption, model)))
        t += dur + s.hold
    t_end = t
    total = t_end + END_HOLD
    nframes = int(round(total * FPS))

    # audio: her takes back to back (cleaned), music under, sounds on cuts and labels
    voice = np.zeros(int(total * SR) + SR)
    tmp = os.path.join(ROOT, "build", "testimonial")
    os.makedirs(tmp, exist_ok=True)
    for k, (t0, dur, s, _) in enumerate(plan):
        wav = os.path.join(tmp, f"{name}_{k}.wav")
        subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-ss", f"{s.start:.3f}", "-t", f"{dur:.3f}", "-i", s.clip,
                               "-vn", "-ac", "1", "-ar", str(SR), "-af", VOICE_FX, wav])
        a, _ = soundfile.read(wav)
        f = int(0.012 * SR)
        a[:f] *= np.linspace(0, 1, f)
        a[-f:] *= np.linspace(1, 0, f)
        i0 = int(t0 * SR)
        voice[i0:i0 + len(a)] += a
    voice = voice[:int(total * SR)]
    voice *= 0.8 / max(1e-6, np.abs(voice).max())

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", name + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                            "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    cuts, pops = [], []
    f = 0
    for k, (t0, dur, s, ws) in enumerate(plan):
        n_talk = int(round((t0 + dur) * FPS)) - int(round(t0 * FPS))
        n_hold = int(round((t0 + dur + s.hold) * FPS)) - int(round((t0 + dur) * FPS))
        zoom = 1.0 if k % 2 == 0 else 1.09
        talk = talk_frames(s.clip, n_talk + (n_hold if s.hold_frames is None else 0), s.start, zoom)
        hold = s.hold_frames(n_hold) if s.hold_frames is not None else None
        brolls = [(int(round(a * FPS)), int(round(b * FPS)), fac) for a, b, fac in s.broll]
        active = None
        for j in range(n_talk + n_hold):
            tt = f / FPS
            local = j / FPS
            base = next(talk) if (j < n_talk or hold is None) else next(hold)
            for bi, (a, b, fac) in enumerate(brolls):
                if a <= j < b:
                    if active is None or active[0] != bi:
                        active = (bi, fac(b - a))
                        cuts.append(f)
                    base = next(active[1])
                    break
            else:
                if active is not None:
                    cuts.append(f)
                active = None
            fr = base.copy()
            if j == 0 and k > 0:
                cuts.append(f)
            fr = v2.zoom_in_from(fr, local, amount=0.04, dur=0.25)
            if k == 0:
                r2.tag(fr, title, 250, tt - 0.15)
            for text, y, at, col in s.tags:
                r3.pill(fr, text, y, local - at, col, ImageFont.truetype(r2.RUPEE, 40) if "₹" in text else font(44))
                if abs(local - at) < 0.5 / FPS:
                    pops.append(tt)
            if j < n_talk + 4:
                sw_ = r3.sentence_at(ws, local)
                v2.karaoke(fr, sw_, local, CAP_Y, local - sw_[0][1])
            enc.stdin.write(fr.tobytes())
            f += 1
    # end card
    t_card = f / FPS
    pops.append(t_card + 1.9)
    while f < nframes:
        fr = Image.new("RGB", (W, H), INK)
        end_card(fr, f / FPS, t_card, end_extra)
        if f - int(t_card * FPS) < v2.WIPE:
            fr = v2.wipe(fr, f - int(t_card * FPS))
        enc.stdin.write(fr.tobytes())
        f += 1
    enc.stdin.close()
    enc.wait()

    n = len(voice)
    music = r2.warm_bed(n, SR, beat_from=plan[1][0]) * 0.20
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    duck = np.convolve(1.0 - 0.65 * np.clip(env * 4, 0, 1), np.ones(int(0.1 * SR)) / int(0.1 * SR), "same")
    mix = voice + music * duck
    synth = r2.synth

    def add(sig, at, gain):
        sig = np.interp(np.arange(int(len(sig) * SR / synth.SR)) * synth.SR / SR, np.arange(len(sig)), sig)
        i = int(at * SR)
        if 0 <= i < n:
            mix[i:i + len(sig)] += (sig * gain)[: n - i]

    for c in sorted(set(cuts)):
        add(synth.sfx("whoosh", 0.35), c / FPS - 0.15, 0.08)
    add(synth.sfx("whoosh", 0.45), t_card - 0.2, 0.18)
    for p in pops:
        add(synth.sfx("pop", 0.15), p, 0.12)
    tt = np.arange(n) / SR
    mix *= np.where(tt > total - 0.8, np.clip((total - tt) / 0.8, 0, 1), 1.0)
    mix *= 0.89 / np.abs(mix).max()
    wav = out + ".mix.wav"
    soundfile.write(wav, mix, SR, subtype="PCM_16")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.75:level=false",
                           "-movflags", "+faststart", "-shortest", *CLEAN, out])
    os.remove(silent)
    os.remove(wav)
    print(f"{out}: {total:.1f} s, {nframes} frames")
