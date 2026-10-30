"""Animated burned-in captions for vertical shorts (rendered as transparent PNG overlays with Pillow).

python3 explainer/xb/captions.py words.json OUT_DIR --frames 384 [--timer 13.95]
"""
import argparse
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 24
FONT = os.path.expanduser('~/fonts/Montserrat.ttf')
KEYWORDS = {'pop', 'crack', 'knuckles', 'fluid', 'gas', 'bubble', 'twenty', 'minutes', 'pressure'}
YELLOW = (255, 214, 10, 255)
WHITE = (255, 255, 255, 255)


def font(size, weight='Black'):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


def chunk_words(words, max_words=3, max_chars=15, gap=0.2):
    chunks, cur = [], []
    for w, s, e in words:
        n = sum(len(x[0]) + 1 for x in cur) + len(w)
        if cur and (len(cur) >= max_words or n > max_chars or s - cur[-1][2] > gap):
            chunks.append(cur)
            cur = []
        cur.append((w, s, e))
    if cur:
        chunks.append(cur)
    return chunks


def render_chunk(chunk, size=104):
    """Pre-render one caption (uppercase, black outline, soft shadow); returns an RGBA image."""
    f = font(size)
    words = [w.upper() for w, _, _ in chunk]
    space = f.getlength(' ')
    widths = [f.getlength(w) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    pad = 40
    img = Image.new('RGBA', (int(total) + 2 * pad, size + 2 * pad + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for (w, _, _), word, wd in zip(chunk, words, widths):
        key = w.lower().strip(".,!?'") in KEYWORDS
        d.text((x, pad), word, font=f, fill=YELLOW if key else WHITE, stroke_width=11, stroke_fill=(0, 0, 0, 255))
        x += wd + space
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    a = img.split()[3].filter(ImageFilter.GaussianBlur(10))
    shadow.putalpha(a.point(lambda v: int(v * 0.55)))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.alpha_composite(shadow, (0, 10))
    out.alpha_composite(img)
    return out


def timer_badge(progress):
    """Stopwatch badge: '20 MIN' with a sweeping hand (progress 0..1)."""
    f = font(70)
    img = Image.new('RGBA', (470, 170), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((10, 10, 460, 160), radius=70, fill=(255, 255, 255, 240), outline=(0, 0, 0, 255), width=8)
    cx, cy, r = 92, 88, 46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 214, 10, 255), outline=(0, 0, 0, 255), width=7)
    d.rectangle((cx - 9, cy - r - 16, cx + 9, cy - r - 4), fill=(0, 0, 0, 255))
    a = -math.pi / 2 + progress * 2 * math.pi
    d.line((cx, cy, cx + 34 * math.cos(a), cy + 34 * math.sin(a)), fill=(0, 0, 0, 255), width=7)
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=(0, 0, 0, 255))
    d.text((160, 44), '20 MIN', font=f, fill=(0, 0, 0, 255))
    return img


def pop_scale(dt):
    """Overshoot pop-in over ~5 frames."""
    if dt < 0:
        return 0.0
    k = dt * FPS
    if k >= 5:
        return 1.0
    return [0.72, 0.95, 1.08, 1.04, 1.0][int(k)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('words')
    ap.add_argument('out')
    ap.add_argument('--frames', type=int, default=384)
    ap.add_argument('--timer', type=float, default=None)
    ap.add_argument('--y', type=float, default=0.70)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    words = json.load(open(args.words))
    chunks = chunk_words(words)
    spans = []
    for i, c in enumerate(chunks):
        t0 = c[0][1] - 0.04
        t1 = c[-1][2] + 0.3
        if i + 1 < len(chunks):
            t1 = min(t1, chunks[i + 1][0][1] - 0.04)
        spans.append((t0, t1, render_chunk(c)))
    for fi in range(args.frames):
        t = fi / FPS
        canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for t0, t1, img in spans:
            if t0 <= t < t1:
                s = pop_scale(t - t0)
                im = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
                if im.width > W - 40:
                    k = (W - 40) / im.width
                    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
                canvas.alpha_composite(im, (W // 2 - im.width // 2, int(H * args.y) - im.height // 2))
        if args.timer is not None and t >= args.timer:
            s = pop_scale(t - args.timer)
            badge = timer_badge(min(1.0, (t - args.timer) / 2.0))
            im = badge.resize((max(1, int(badge.width * s)), max(1, int(badge.height * s))), Image.LANCZOS)
            canvas.alpha_composite(im, (W // 2 - im.width // 2, int(H * 0.16) - im.height // 2))
        canvas.save(os.path.join(args.out, f'c_{fi + 1:04d}.png'))
    print('captions:', len(chunks), 'chunks;', ' | '.join(' '.join(w for w, _, _ in c) for c in chunks))


if __name__ == '__main__':
    main()
