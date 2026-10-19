"""Hindi reel 04 (Yours3D Hindi page): the English reel 04 edit (projects3d/reel04/build.py, unchanged) with the
owner's Hindi voice-over, Devanagari captions and labels, and a Hindi end card.

  python tools/hindi_voiceover.py projects3d/hindi/reel04/script.txt hindi/reel04_hi
  python projects3d/hindi/reel04/build.py MEDIA_DIR          # -> out/3d/hindi/reel04_hi.mp4

Noto Serif Devanagari has no Latin letters, so mixed text (WhatsApp, 3D, DM) is drawn in runs: Devanagari in Noto
Serif Devanagari, Latin in the brand's Caladea.
"""
import importlib.util
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reel04_build", os.path.join(HERE, "..", "..", "reel04", "build.py"))
r4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r4)
v1, v2, r2, r3 = r4.v1, r4.v2, r4.r2, r4.r3
W, H, ROOT = r4.W, r4.H, r4.ROOT
GOLD, GOLD_LIGHT, INK, WHITE, GREEN = r4.GOLD, r4.GOLD_LIGHT, r4.INK, r4.WHITE, r4.GREEN

DEV = "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf"
LAT = r2.SERIF
ENDS = ".?!।"
_fonts = {}


def fonts(size):
    if size not in _fonts:
        _fonts[size] = (ImageFont.truetype(DEV, size), ImageFont.truetype(LAT, size))
    return _fonts[size]


def runs(text, size):
    """[(piece, font)]: Latin letters in Caladea, everything else (Devanagari, digits, ₹, punctuation) in Noto."""
    dev, lat = fonts(size)
    out = []
    for piece in re.findall(r"[A-Za-z0-9][A-Za-z0-9']*|[•·]|[^A-Za-z0-9•·]+|[0-9]+", text):
        latin = re.search(r"[A-Za-z•·]", piece) is not None
        out.append((piece, lat if latin else dev))
    return out


def tlen(d, text, size):
    return sum(d.textlength(p, font=f) for p, f in runs(text, size))


def draw(d, x, y, text, size, fill, **kw):
    """Left-aligned mixed text, vertically centred on y (both scripts share one baseline)."""
    for p, f in runs(text, size):
        d.text((x, y + size * 0.34), p, font=f, fill=fill, anchor="ls", **kw)
        x += d.textlength(p, font=f)


# ---------- captions ----------

def wrap(d, words, size, maxw=900):
    lines, cur = [], []
    for w in words:
        if not cur or tlen(d, " ".join(cur + [w]), size) <= maxw:
            cur.append(w)
        else:
            lines.append(cur)
            cur = [w]
    lines.append(cur)
    if len(lines) == 2:
        flat = lines[0] + lines[1]
        k = min(range(1, len(flat)), key=lambda k: max(tlen(d, " ".join(flat[:k]), size),
                                                       tlen(d, " ".join(flat[k:]), size)))
        lines = [flat[:k], flat[k:]]
    return lines


def karaoke(frame, words, t, y=v2.CAP_Y, age=1.0):
    """v2.karaoke for Devanagari: the word being spoken in gold."""
    d = ImageDraw.Draw(frame)
    size = 66 if age > 0.12 else int(66 * (0.85 + 0.15 * age / 0.12))
    lines = wrap(d, [w for w, _, _ in words], size)
    lh = size * 1.32
    y0 = y - lh * (len(lines) - 1) / 2
    k = 0
    for i, ln in enumerate(lines):
        x = W / 2 - tlen(d, " ".join(ln), size) / 2
        for w, s, e in words[k:k + len(ln)]:
            on = s <= t < e + 0.08
            draw(d, x, y0 + i * lh, w, size, GOLD if on else WHITE, stroke_width=7, stroke_fill=(20, 16, 14))
            x += tlen(d, w + " ", size)
        k += len(ln)


CAPTION = [(("थ्री", "डी"), "3D"), (("डी", "एम"), "DM"), (("व्हाट्सऐप",), "WhatsApp")]


def caption_words(ws):
    """Spoken spellings -> written form in captions (थ्री डी -> 3D), keeping the timing span and end punctuation."""
    out, i = [], 0
    while i < len(ws):
        for src, dst in CAPTION:
            n = len(src)
            got = [w[0].rstrip(ENDS + ",") for w in ws[i:i + n]]
            if tuple(got) == src:
                tail = ws[i + n - 1][0][len(got[-1]):]
                out.append((dst + tail, ws[i][1], ws[i + n - 1][2]))
                i += n
                break
        else:
            out.append(ws[i])
            i += 1
    return out


def word_timings(wav, cues):
    """Per cue: [(word, start, end)] from Whisper (Hindi) word timestamps, else spread by length."""
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="hi", word_timestamps=True)
    heard = [(w.start, w.end) for s in segs for w in s.words]
    out = []
    for c0, c1, txt in cues:
        ws = txt.split()
        got = [h for h in heard if h[0] >= c0 - 0.15 and h[1] <= c1 + 0.25]
        if len(got) == len(ws):
            timed = [(w, s, e) for w, (s, e) in zip(ws, got)]
        else:
            lens = np.cumsum([0] + [len(w) + 1 for w in ws])
            tt = c0 + (c1 - c0) * lens / lens[-1]
            timed = [(w, tt[i], tt[i + 1]) for i, w in enumerate(ws)]
        out.append(caption_words(timed))
    return out


def groups(ws):
    out, cur = [], []
    for w in ws:
        cur.append(w)
        if w[0][-1] in ENDS:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [(g[0][1], g) for g in out]


def sentence_at(ws, t):
    pick = groups(ws)[0][1]
    for s, g in groups(ws):
        if s <= t + 0.05:
            pick = g
    return pick


# ---------- labels and end card ----------

HINDI = {
    "HER 1ST BIRTHDAY GIFT": "पहले बर्थडे का गिफ़्ट",
    "MANYA  ·  AGE 1": "मान्या  •  1 साल",
    "3D DESIGN": "3D डिज़ाइन",
    "PRINTED IN FULL COLOUR": "पूरे रंगों में प्रिंट",
    "NAME ON THE BASE": "बेस पर नाम",
    "PHOTO": "फ़ोटो",
    "FIGURINE": "फ़िगरीन",
    "A GIFT TO KEEP FOREVER": "हमेशा के लिए यादगार",
    "SEND 1 PHOTO ON WHATSAPP": "WhatsApp पर 1 फ़ोटो भेजें",
    "2 FREE PREVIEWS  ·  1–2 MIN": "2 फ़्री प्रीव्यू  •  1–2 मिनट",
}


def pill(frame, text, y, age, color, size, dark=True):
    """Rounded label sliding up, mixed-script text."""
    if age < 0:
        return
    text = HINDI.get(text, text)
    a = v2.ease(age / 0.3)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tw = tlen(d, text, size)
    yy, hh = y + 40 * (1 - a), size * 0.85
    d.rounded_rectangle((W / 2 - tw / 2 - 36, yy - hh, W / 2 + tw / 2 + 36, yy + hh), radius=hh, fill=color + (255,))
    draw(d, W / 2 - tw / 2, yy, text, size, INK if dark else WHITE)
    layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    frame.paste(layer, (0, 0), layer)


def tag(frame, text, y, age, color=GOLD, size=46):
    pill(frame, text, y, age, color, size - 4)


def r3_pill(frame, text, y, age, color, fnt, dark=True):
    pill(frame, text, y, age, color, fnt.size - 4, dark)


def end_card(frame, t, t0):
    r2.logo_build(frame, t - t0 - 0.1)
    d = ImageDraw.Draw(frame)
    a = v2.ease((t - t0 - 1.5) / 0.4)
    if a > 0:
        col = tuple(int(INK[i] + (GOLD[i] - INK[i]) * a) for i in range(3))
        d.text((W / 2, 790), "Yours3D", font=ImageFont.truetype(r2.SERIF_REG, 120), fill=col, anchor="mm")
        d.line((W / 2 - 60 * a, 875, W / 2 + 60 * a, 875), fill=col, width=3)
        w = tlen(d, "3D प्रिंटिंग स्टूडियो  •  इंडिया", 32)
        draw(d, W / 2 - w / 2, 925, "3D प्रिंटिंग स्टूडियो  •  इंडिया", 32, col)
    pill(frame, "सिर्फ़ ₹3,599 से शुरू", 1040, t - t0 - 1.9, GOLD, 42)
    pill(frame, "DM के लिए कमेंट करें", 1160, t - t0 - 2.1, (40, 38, 36), 44, dark=False)
    pill(frame, "WhatsApp पर फ़्री प्रीव्यू", 1280, t - t0 - 2.4, GREEN, 42)
    pill(frame, "+91 91647 48401", 1385, t - t0 - 2.55, GREEN, 42)


# the English edit, with the Hindi pieces swapped in
r4.NAME = os.path.join("hindi", "reel04_hi")
r4.groups = groups
v2.word_timings = word_timings
v2.karaoke = karaoke
r2.tag = tag
r3.pill = r3_pill
r3.sentence_at = sentence_at
r3.end_card = end_card

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "out", "3d", "hindi"), exist_ok=True)
    r4.main()
