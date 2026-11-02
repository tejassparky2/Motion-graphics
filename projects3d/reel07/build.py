"""Reel 07 (Yours3D): "How to make your own custom mini you" -- the first learning reel. Manya's figurine (reel 04)
from photo to print in 4 steps: ChatGPT (with the owner's real edits), the 3D model, colour painting in the slicer
(Snapmaker Orca), the Snapmaker U1 print with the slicer's real numbers, supports off, the reveal, WhatsApp, and
"Comment 3D" for the full prompt and guide. Frame 1 already reads as a tutorial (owner, 30 Oct 2026).
The owner's sister agreed to Manya's photo and name being shown (19 Oct 2026); Sowmya appears holding the figurine.

  python tools/voiceover.py projects3d/reel07/script.txt reel07 --engine turbo --flow --gap 0.9 --polish
  python projects3d/reel07/build.py "out/3d/reel07/raw2/Photo to 3d" "out/3d/reel04/raw/Raw videos"
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


r4 = _load("reel04_build", os.path.join(HERE, "..", "reel04", "build.py"))
T = _load("testimonial", os.path.join(HERE, "..", "testimonial.py"))
r2, r3, v1, v2 = r4.r2, r4.r3, r4.v1, r4.v2
W, H, FPS, ROOT, CLEAN = r2.W, r2.H, r2.FPS, r2.ROOT, r2.CLEAN
GOLD, GOLD_LIGHT, INK, WHITE, GREEN = r2.GOLD, r2.GOLD_LIGHT, r2.INK, r2.WHITE, r2.GREEN
font, view, glide, ring, spot, split = r2.font, r4.view, r4.glide, r4.ring, r4.spot, r4.split
HALF = r4.HALF

NAME = "reel07"
CAP = 1440                  # caption centre in the phone / screen scenes (below the card, above the Reels UI)
REVEAL_HOLD = 1.0           # extra beat after "And here's the result."
END_HOLD = 3.6
r2.PHONE_TOP, r2.PHONE_H = 340, 1000

# the voice says these the way they should sound; the caption shows the written form
SHOWN = {("Chat", "G", "P", "T,"): "ChatGPT,", ("U", "one"): "U1", ("Eleven", "hours."): "11 hours.",
         ("Nine", "hundred", "and", "fifty", "colour", "changes."): "950 colour changes."}

# points of interest in the final design (1280x1280): (cx, cy, crop height)
DESIGN = {"face": (640, 470, 560), "dress": (630, 900, 600), "bow": (767, 190, 420), "full": (640, 640, 1280)}
RING_DESIGN = {"bow": (767, 175)}
STEPS = ["ChatGPT", "Tripo 3D", "Slicer", "Print + finish"]
LABELS = {3: "TIP: ASK FOR CHANGES", 5: "TRIPO 3D · 3D MODEL", 6: "SLICER · PAINT COLOURS", 7: "PRINT + FINISH"}


def display_words(ws):
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


# ---------- frames ----------

def _reader(path, n, start, speed, vf_tail, size):
    vf = f"setpts=(PTS-STARTPTS)/{speed},fps={FPS}," + vf_tail
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-i", path, "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(size[0] * size[1] * 3)
        if len(buf) == size[0] * size[1] * 3:
            last = Image.frombytes("RGB", size, buf)
        yield last
    p.stdout.close()
    p.wait()


_bg = None


def backdrop():
    """Brand background with a soft gold glow, behind the phone and screen cards."""
    global _bg
    if _bg is None:
        bg = Image.new("RGB", (W, H), INK)
        d = ImageDraw.Draw(bg)
        for r, a in ((640, 26), (430, 40)):
            d.ellipse((W / 2 - r, 840 - r, W / 2 + r, 840 + r),
                      fill=tuple(int(INK[i] + (GOLD[i] - INK[i]) * a / 255) for i in range(3)))
        _bg = bg.filter(ImageFilter.GaussianBlur(90))
    return _bg


def screen_card(path, n, start, end, box, top=340, maxw=1000, maxh=1000):
    """A crop of a PC screen recording (no taskbar, no file lists) as a rounded card on the brand background."""
    cw, ch = box[2] - box[0], box[3] - box[1]
    s = min(maxw / cw, maxh / ch)
    sw, sh = int(cw * s) // 2 * 2, int(ch * s) // 2 * 2
    x0 = (W - sw) // 2
    bg = backdrop().copy()
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((x0 - 10, top - 10, x0 + sw + 10, top + sh + 10), radius=34, fill=(38, 38, 42), outline=GOLD,
                        width=3)
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=26, fill=255)
    speed = (end - start) / (n / FPS)
    for fr in _reader(path, n, start, speed, f"crop={cw}:{ch}:{box[0]}:{box[1]},scale={sw}:{sh}", (sw, sh)):
        out = bg.copy()
        if fr is not None:
            out.paste(fr, (x0, top), mask)
        yield out


def phone_parts(path, parts):
    """Several windows of a phone screen recording, back to back: parts = [(start, end, frames)]."""
    for s, e, k in parts:
        if k > 0:
            yield from r2.phone_frames(path, k, s, e)


def still_frame(path, at):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(at), "-i", path, "-frames:v", "1", "-f",
                                   "image2pipe", "-vcodec", "png", "-"])
    import io
    return Image.open(io.BytesIO(raw)).convert("RGB")


def dimmed(frames, blur=12, k=0.55):
    for fr in frames:
        yield Image.blend(fr.filter(ImageFilter.GaussianBlur(blur)), Image.new("RGB", (W, H), INK), k)


# ---------- graphics ----------

def shade(fr, y0, y1, top=True, alpha=200):
    g = Image.linear_gradient("L").resize((1, y1 - y0)).point(lambda v: int(alpha * (255 - v) / 255 if top
                                                                            else alpha * v / 255))
    fr.paste(Image.new("RGB", (W, y1 - y0), INK), (0, y0), g.resize((W, y1 - y0)))


def pill_at(d, x, y, text, fnt, fill, color=INK, right=False):
    tw = d.textlength(text, font=fnt)
    hh = fnt.size * 0.78
    x0 = x - tw - 72 if right else x
    d.rounded_rectangle((x0, y - hh, x0 + tw + 72, y + hh), radius=hh, fill=fill)
    d.text((x0 + 36 + tw / 2, y), text, font=fnt, fill=color, anchor="mm")


def bookmark(d, x, y, s, fill):
    d.polygon([(x, y), (x + s, y), (x + s, y + 1.3 * s), (x + s / 2, y + 0.95 * s), (x, y + 1.3 * s)], fill=fill)


def chips(fr, y0, ages, lit=None):
    """The 4 steps as numbered chips, 2 x 2, clear of the Reels buttons on the right."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, nm in enumerate(STEPS):
        a = v2.back(ages[i] / 0.35) if ages[i] > 0 else 0
        if a <= 0:
            continue
        cx, cy = 70 + (i % 2) * 450, y0 + (i // 2) * 112 + 30 * (1 - min(1, a))
        hot = lit == i
        d.rounded_rectangle((cx, cy - 46, cx + 430, cy + 46), radius=46, fill=(GOLD if hot else INK) + (235,),
                            outline=GOLD + (255,), width=3)
        d.ellipse((cx + 8, cy - 38, cx + 84, cy + 38), fill=(INK if hot else GOLD) + (255,))
        d.text((cx + 46, cy), str(i + 1), font=font(48), fill=(GOLD if hot else INK) + (255,), anchor="mm")
        d.text((cx + 104, cy), nm, font=font(44), fill=(INK if hot else WHITE) + (255,), anchor="lm")
    fr.paste(layer, (0, 0), layer)


def step_head(fr, step, age, label=None):
    """Progress bar of the 4 steps, 'STEP n OF 4' and the tool's name (or `label`)."""
    d = ImageDraw.Draw(fr)
    x0, x1, y, gap = 70, W - 70, 150, 14
    seg = (x1 - x0 - gap * 3) / 4
    for i in range(4):
        a = x0 + i * (seg + gap)
        d.rounded_rectangle((a, y - 7, a + seg, y + 7), radius=7, fill=(80, 76, 70))
        fill = 1.0 if i < step else (v2.ease(age / 0.5) if i == step else 0)
        if fill > 0:
            d.rounded_rectangle((a, y - 7, a + seg * fill, y + 7), radius=7, fill=GOLD)
    d.text((W / 2, 196), f"STEP {step + 1} OF 4", font=ImageFont.truetype(r2.SERIF_REG, 32), fill=GOLD_LIGHT,
           anchor="mm")
    v2.pill(fr, label or STEPS[step].upper(), 266, age - 0.1, color=GOLD, size=44, dark_text=True, slide=20)


def hook_overlay(fr, photo_inset):
    """Frame 1: everything is on screen at 0 s, so it reads as a tutorial before a word is heard."""
    shade(fr, 0, 760, top=True, alpha=225)
    shade(fr, 1120, H, top=False, alpha=230)
    d = ImageDraw.Draw(fr)
    px, py, pw, ph = 60, 700, 330, 560
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=44, fill=(10, 10, 12), outline=(70, 70, 74), width=4)
    fr.paste(photo_inset, (px + 14, py + 14))
    d = ImageDraw.Draw(fr)
    d.ellipse((px + pw + 16, py + ph / 2 - 44, px + pw + 104, py + ph / 2 + 44), fill=GOLD)
    d.text((px + pw + 60, py + ph / 2 - 4), "→", font=font(70), fill=INK, anchor="mm")
    pill_at(d, 70, 300, "HOW TO", font(50), GOLD)
    bookmark(d, W - 270, 272, 34, WHITE)
    d.text((W - 70, 300), "SAVE IT", font=font(40), fill=WHITE, anchor="rm")
    d.text((W / 2, 430), "MAKE YOUR MINI YOU", font=font(88), fill=WHITE, anchor="mm", stroke_width=6,
           stroke_fill=INK)
    d.text((W / 2, 532), "photo → 3D figurine · 4 steps", font=font(54), fill=GOLD_LIGHT, anchor="mm",
           stroke_width=5, stroke_fill=INK)


def row_box(fr, y, age, x0, x1):
    if age < 0:
        return
    a = v2.ease(age / 0.3)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((x0 - 10 * (1 - a), y - 26, x0 + (x1 - x0) * a, y + 26), radius=12, outline=GOLD_LIGHT,
                        width=5)


def end_card(fr, t, t0):
    r2.logo_build(fr, t - t0 - 0.1)
    d = ImageDraw.Draw(fr)
    a = v2.ease((t - t0 - 1.5) / 0.4)
    if a > 0:
        col = tuple(int(INK[i] + (GOLD[i] - INK[i]) * a) for i in range(3))
        d.text((W / 2, 790), "Yours3D", font=ImageFont.truetype(r2.SERIF_REG, 120), fill=col, anchor="mm")
        d.line((W / 2 - 60 * a, 875, W / 2 + 60 * a, 875), fill=col, width=3)
        d.text((W / 2, 925), "3 D   P R I N T I N G   S T U D I O   ·   I N D I A",
               font=ImageFont.truetype(r2.SERIF_REG, 30), fill=col, anchor="mm")
    rupee = ImageFont.truetype(r2.RUPEE, 44)
    r3.pill(fr, "COMMENT 3D · PROMPT + GUIDE", 1040, t - t0 - 1.9, (40, 38, 36), font(46), dark=False)
    r3.pill(fr, "FIGURINES FROM ₹3,599", 1160, t - t0 - 2.1, GOLD, rupee)
    r3.pill(fr, "FREE PREVIEW ON WHATSAPP", 1280, t - t0 - 2.4, GREEN, font(44))
    r3.pill(fr, "+91 91647 48401", 1385, t - t0 - 2.55, GREEN, font(44))


# ---------- build ----------

def main():
    mdir, r4dir = sys.argv[1], sys.argv[2]
    md = lambda key: v1.media(mdir, key)          # noqa: E731
    still = lambda d, key: ImageOps.exif_transpose(Image.open(v1.media(d, key))).convert("RGB")   # noqa: E731
    photo, design, fig = still(r4dir, "808397810"), still(mdir, "IMG_20261014_140855"), still(r4dir, "183012")
    chat, orca, orca2 = md("141710_ChatGPT"), md("150551"), md("150840")

    vo = os.path.join(ROOT, "out", "voiceover", NAME)
    voice, sr = soundfile.read(vo + ".wav")
    cues = v1.read_srt(vo + ".srt")
    words = v2.word_timings(vo + ".wav", cues)
    assert len(cues) == 12, len(cues)
    # hold the reveal: a beat of silence after "And here's the result."
    cut = (cues[9][1] + cues[10][0]) / 2
    k = int(cut * sr)
    voice = np.concatenate([voice[:k], np.zeros(int(REVEAL_HOLD * sr)), voice[k:], np.zeros(int(END_HOLD * sr))])
    shift = lambda x: x + REVEAL_HOLD if x > cut else x     # noqa: E731
    cues = [(shift(a), shift(b), s) for a, b, s in cues]
    words = [[(w, shift(a), shift(b)) for w, a, b in ws] for ws in words]
    words = [display_words(ws) for ws in words]
    sent = [r4.groups(ws) for ws in words]
    total = len(voice) / sr
    L = [c[0] for c in cues]
    E = [c[1] for c in cues]
    t_end = E[11] + 0.45

    def at(i, j, default=None):
        """Start of sentence j of cue i."""
        return sent[i][j][0] if len(sent[i]) > j else default

    photo_inset = view(photo, (1330, 700, 1250), (302, 532))

    def hook(n):
        for fr in r2.clip(md("183018"), n, 0.0, speed=0.8):
            fr = fr.copy()
            hook_overlay(fr, photo_inset)
            yield fr

    def started(n):
        """'This figurine started as one phone photo.' -- the photo; 'Here's exactly how...' -- the figurine."""
        k2 = int(round((at(1, 1, L[1] + 1.8) - L[1]) * FPS))
        for k in range(k2):
            yield view(photo, glide(r4.PHOTO["full"], r4.PHOTO["face"], k / max(1, k2 - 1)))
        yield from r2.clip(md("182700"), n - k2, 0.0, speed=0.9)

    def step1(n):
        return phone_parts(chat, [(11.0, 15.0, int(n * 0.30)), (20.0, 43.5, int(n * 0.30)),
                                  (44.0, 50.0, n - 2 * int(n * 0.30))])

    def tip(n):
        """The owner's real edits, each shown as it is said."""
        s2, s3 = at(3, 2, L[3] + 2.2), at(3, 3, L[3] + 4.0)
        a, b = int(round((s2 - L[3]) * FPS)), int(round((s3 - L[3]) * FPS))
        c = n - b
        a, b = max(1, min(a, n - 3)), max(2, min(b, n - 2))
        c = n - b
        return phone_parts(chat, [(46.0, 52.0, a), (55.0, 60.5, (b - a) // 2), (85.0, 89.0, b - a - (b - a) // 2),
                                  (91.0, 96.0, c // 2), (103.8, 108.5, c - c // 2)])

    def compare(n):
        """'Same face. Same dress. Same little bow. Just cuter.' -- photo on top, design below."""
        starts = [s for s, _ in sent[4]]
        stops = ["face", "dress", "bow", "full"]
        for k in range(n):
            t = L[4] + k / FPS
            i = min(r4.which(starts, t), 3)
            a = "full" if i == 0 else stops[i - 1]
            x = (t - starts[i] + 0.15) / 0.45
            top = view(photo, glide(r4.PHOTO[a], r4.PHOTO[stops[i]], x), (W, HALF))
            bot = view(design, glide(DESIGN[a], DESIGN[stops[i]], x), (W, HALF))
            fr = split(top, bot)
            if i < 3:
                p = spot(photo, r4.PHOTO[stops[i]], (W, HALF), r4.RING["bow"]) if i == 2 else (W / 2, HALF / 2)
                ring(fr, p[0], p[1], 160 if i == 2 else 210, t - starts[i] - 0.35)
                q = spot(design, DESIGN[stops[i]], (W, HALF), RING_DESIGN["bow"]) if i == 2 else (W / 2, HALF / 2)
                ring(fr, q[0], HALF + q[1], 160 if i == 2 else 210, t - starts[i] - 0.45)
            yield fr

    def model(n):
        return screen_card(orca2, n, 2.5, 9.0, (700, 60, 1500, 1030))

    def paint(n):
        return screen_card(orca, n, 34.0, 80.0, (520, 70, 1460, 1030))

    table = still_frame(orca2, 30.0).crop((1395, 85, 1835, 530))
    TS = 1.8
    table = table.resize((int(table.width * TS), int(table.height * TS)), Image.LANCZOS)
    tmask = Image.new("L", table.size, 0)
    ImageDraw.Draw(tmask).rounded_rectangle((0, 0, table.width - 1, table.height - 1), radius=24, fill=255)
    TX, TY = (W - table.width) // 2, 330

    def printing(n):
        """Step four on the U1, then the slicer's own numbers: 11 hours, 950 colour changes."""
        s2 = at(7, 2, L[7] + 3.0)
        k2 = int(round((s2 - L[7]) * FPS))
        yield from r2.clip(md("013746"), k2, 0.0, speed=1.0)
        for fr in dimmed(r2.clip(md("013732"), n - k2, 0.0, speed=1.0)):
            fr = fr.copy()
            d = ImageDraw.Draw(fr)
            d.rounded_rectangle((TX - 8, TY - 8, TX + table.width + 8, TY + table.height + 8), radius=30,
                                outline=GOLD, width=3)
            fr.paste(table, (TX, TY), tmask)
            yield fr

    def supports(n):
        """'Then the supports come off, and we sand it by hand.' -- the print in its supports, then clean."""
        ws = words[8]
        k_and = next((i for i, w in enumerate(ws) if w[0].startswith("and") and i > 2), len(ws) // 2)
        k2 = int(round((ws[k_and][1] - L[8]) * FPS))
        yield from r2.clip(md("184635"), k2, 2.0, speed=1.0)
        yield from v1.image_frames(fig, n - k2, zoom=(1.0, 1.06))

    def reveal(n):
        k2 = int(n * 0.6)
        yield from r2.clip(md("182700"), k2, 0.0, speed=1.0)
        yield from T.take_frames(md("IMG_4135"), n - k2, 4.2, speed=1.0)

    def whatsapp(n):
        return dimmed(r2.clip(md("182700"), n, 0.0, speed=0.6), blur=10, k=0.5)

    blur_design = Image.blend(v1.cover(design).filter(ImageFilter.GaussianBlur(14)), Image.new("RGB", (W, H), INK),
                              0.62)

    def comment(n):
        return (blur_design for _ in range(n))

    # (start, frames factory, wipe in?, caption y, step for the progress bar or None)
    scenes = [
        (0.0, hook, False, None, None),
        (L[1], started, True, r2.CAP_Y, None),
        (L[2], step1, True, CAP, 0),
        (L[3], tip, False, CAP, 0),
        (L[4], compare, True, HALF, None),
        (L[5], model, True, CAP, 1),
        (L[6], paint, True, CAP, 2),
        (L[7], printing, True, CAP, 3),
        (L[8], supports, True, r2.CAP_Y, None),
        (L[9], reveal, True, r2.CAP_Y, None),
        (L[10], whatsapp, True, r2.CAP_Y, None),
        (L[11], comment, True, r2.CAP_Y, None),
        (t_end, lambda n: (Image.new("RGB", (W, H), INK) for _ in range(n)), True, None, None),
    ]
    nframes = int(round(total * FPS))
    bounds = [round(s[0] * FPS) for s in scenes] + [nframes]
    cuts = [b for b, s in zip(bounds, scenes) if s[2]]

    os.makedirs(os.path.join(ROOT, "out", "3d"), exist_ok=True)
    out = os.path.join(ROOT, "out", "3d", NAME + ".mp4")
    silent = out + ".video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                            "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", *CLEAN, silent],
                           stdin=subprocess.PIPE)
    tag, rupee = r2.tag, ImageFont.truetype(r2.RUPEE, 46)
    s_four = at(1, 1, L[1] + 1.8)
    f = 0
    for si, ((s0, make, wiped, cap_y, step), a, b) in enumerate(zip(scenes, bounds, bounds[1:])):
        for frame in make(b - a):
            t = f / FPS
            fr = frame.copy()
            fr = v2.zoom_in_from(fr, t - a / FPS) if wiped else fr
            if si == 0:
                chips(fr, 1330, [1.0] * 4, lit=int(t / 0.45) % 4 if t < 1.8 else None)
            if si == 1:
                if t < s_four:
                    tag(fr, "ONE PHONE PHOTO", 260, t - L[1] - 0.2)
                else:
                    tag(fr, "4 STEPS", 260, t - s_four - 0.1)
                    chips(fr, 1000, [t - s_four - 0.25 - 0.18 * i for i in range(4)])
            if step is not None:
                step_head(fr, step, t - s0, LABELS.get(si))
            if si == 4:
                tag(fr, "PHOTO", 190, t - L[4] - 0.1, size=34)
                tag(fr, "3D DESIGN", HALF + 80, t - L[4] - 0.2, size=34)
            if si == 7:
                s2, s3 = at(7, 2, L[7] + 3.0), at(7, 3, L[7] + 4.2)
                if t < s2:
                    tag(fr, "SNAPMAKER U1", 1300, t - at(7, 1, L[7] + 0.8) - 0.1, size=40)
                else:
                    row_box(fr, TY + int(405 * TS), t - s2 - 0.1, TX + 20, TX + table.width - 20)
                    v2.stat_card(fr, 290, 1250, 11, "HOURS", t - s2)
                    if t >= s3:
                        row_box(fr, TY + int(305 * TS), t - s3 - 0.1, TX + 20, TX + table.width - 20)
                        v2.stat_card(fr, 750, 1250, 950, "COLOUR CHANGES", t - s3)
            if si == 8:
                ws = words[8]
                k_and = next((i for i, w in enumerate(ws) if w[0].startswith("and") and i > 2), len(ws) // 2)
                if t < ws[k_and][1]:
                    tag(fr, "SUPPORTS COME OFF", 260, t - L[8] - 0.2)
                else:
                    tag(fr, "SANDED BY HAND", 260, t - ws[k_and][1] - 0.1)
            if si == 9:
                fr = v2.light_sweep(fr, t - L[9])
                fr = v2.sparkles(fr, t - L[9] - 0.1)
            if si == 10:
                g = sent[10]
                tag(fr, "YOUR OWN MINI YOU", 430, t - L[10] - 0.2)
                s1 = g[1][0] if len(g) > 1 else L[10] + 2.0
                r3.pill(fr, "SEND 1 PHOTO ON WHATSAPP", 620, t - s1, GREEN, font(46))
                r3.pill(fr, "FREE PREVIEWS IN 1–2 MIN", 760, t - s1 - 0.5, GOLD, font(46))
                r3.pill(fr, "+91 91647 48401", 900, t - s1 - 0.8, GREEN, font(46))
                r3.pill(fr, "FIGURINES FROM ₹3,599", 1040, t - s1 - 1.1, GOLD, rupee)
            if si == 11:
                g = sent[11]
                s1 = g[1][0] if len(g) > 1 else L[11] + 1.2
                tag(fr, "OR MAKE IT YOURSELF", 430, t - L[11] - 0.2)
                if t >= s1:
                    d = ImageDraw.Draw(fr)
                    a1 = v2.back((t - s1) / 0.35)
                    d.text((W / 2, 640), "COMMENT", font=font(84), fill=WHITE, anchor="mm", stroke_width=6,
                           stroke_fill=INK)
                    d.text((W / 2, 850), "3D", font=font(int(120 + 110 * min(1.1, max(0.0, a1)))), fill=GOLD,
                           anchor="mm", stroke_width=8, stroke_fill=INK)
                    r3.pill(fr, "FULL PROMPT + GUIDE IN DM", 1080, t - s1 - 0.4, GOLD, font(46))
            if si == len(scenes) - 1:
                end_card(fr, t, t_end)
            if 0 < si < len(scenes) - 1:
                for (c0, c1, _), ws in zip(cues, words):
                    if c0 <= t < c1 + 0.15:
                        sw = r3.sentence_at(ws, t)
                        v2.karaoke(fr, sw, t, cap_y, t - sw[0][1])
            for c in cuts:
                if -v2.WIPE <= f - c < v2.WIPE:
                    fr = v2.wipe(fr, f - c)
            enc.stdin.write(fr.tobytes())
            f += 1
    enc.stdin.close()
    enc.wait()

    # soundtrack: voice + the warm bed (beat from the print) + whooshes on wipes, pops on labels, a hit on the reveal
    n = len(voice)
    music = r2.warm_bed(n, sr, beat_from=L[7]) * 0.30
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same")
    duck = np.convolve(1.0 - 0.7 * np.clip(env * 4, 0, 1), np.ones(int(0.1 * sr)) / int(0.1 * sr), "same")
    mix = voice + music * duck
    synth = r2.synth

    def add(sig, at_, gain):
        sig = np.interp(np.arange(int(len(sig) * sr / synth.SR)) * synth.SR / sr, np.arange(len(sig)), sig)
        s = int(at_ * sr)
        if 0 <= s < n:
            mix[s:s + len(sig)] += (sig * gain)[: n - s]

    for c in cuts:
        add(synth.sfx("whoosh", 0.45), c / FPS - 0.22, 0.2)
    pops = [L[1] + 0.2, s_four + 0.25, L[2] + 0.1, L[3] + 0.2, L[5] + 0.1, L[6] + 0.1, L[7] + 0.1, t_end + 1.9]
    pops += [s + 0.35 for s, _ in sent[4][:3]] + [s for s, _ in sent[7][2:]] + [s for s, _ in sent[10][1:]]
    pops += [s for s, _ in sent[11][1:]]
    for p in pops:
        add(synth.sfx("pop", 0.15), p, 0.15)
    add(synth.sfx("hit", 0.4), L[9], 0.15)
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
