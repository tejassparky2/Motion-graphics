"""Pushpa Charitable Trust, reel 01 (Dasara at the trust's elderly home), 1080x1920.

Joins the three enhanced phone clips (tools/trust_enhance.py) into one reel, keeping the original Kannada
speech in sync, and ends on a donation card with the trust's UPI QR. No captions (owner's choice), no
added voice. Soft original music plays only under the end card.

  python3 trust/reel01/build.py CLIPS_DIR OUT.mp4 --fonts FONTS_DIR
CLIPS_DIR holds WA0025_enhanced.mp4, WA0026_enhanced.mp4, WA0027_enhanced.mp4 (raw footage is not committed).
"""
import argparse
import ast
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS, SR = 1080, 1920, 30, 48000
XF = 0.3                                  # crossfade between clips, seconds
CARD = 6.0                                # end card length, seconds

# (clip, start, end): Pushpa's message (the last seconds, "cut it", are off-camera talk), the residents and
# the trust banner, then the residents' "1, 2, 3" together.
CUTS = [("WA0027", 0.0, 60.0), ("WA0026", 0.0, 19.9), ("WA0025", 0.0, 14.25)]

# Exactly as on the owner's Canara Bank QR (decoded and checked): payee PUSHPA CHARITABLE TRUST.
UPI_ID = "337331253926379@cnrb"
UPI_URI = ("upi://pay?pa=337331253926379@cnrb&pn=PUSHPA CHARITABLE TRUST&mc=8641&tr=1234567887654321&am=0&mam=0"
           "&cu=INR&refUrl=http://npci.org/upi/schema/")

CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6"]


def warm_bed(n, sr, beat_from, **kw):
    """The channel's synth bed from projects3d/reel02/build.py, loaded alone (that module pulls in the
    whole 3D pipeline on import)."""
    path = os.path.join(ROOT, "projects3d", "reel02", "build.py")
    tree = ast.parse(open(path).read())
    fn = next(f for f in tree.body if isinstance(f, ast.FunctionDef) and f.name == "warm_bed")
    ns = {"np": np}
    exec(compile(ast.Module([fn], []), path, "exec"), ns)
    return ns["warm_bed"](n, sr, beat_from, **kw)


def end_card(fonts, path):
    import qrcode
    bold = os.path.join(fonts, "Poppins-Bold.ttf")
    semi = os.path.join(fonts, "Poppins-SemiBold.ttf")
    kn = os.path.join(fonts, "NotoSansKannada-Bold.ttf")
    y, x = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    top, bot = np.array([255, 244, 222]), np.array([250, 200, 120])          # warm cream to marigold
    bg = top + (bot - top) * (0.6 * y + 0.4 * x)[..., None]
    im = Image.fromarray(bg.astype(np.uint8))
    d = ImageDraw.Draw(im)

    def centre(text, yy, font, fill):
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, yy), text, font=font, fill=fill)

    maroon, ink = (128, 24, 36), (60, 34, 20)
    centre("ಪುಷ್ಪ ಚಾರಿಟಬಲ್ ಟ್ರಸ್ಟ್", 190, ImageFont.truetype(kn, 78), maroon)
    centre("Pushpa Charitable Trust", 320, ImageFont.truetype(bold, 72), maroon)
    centre("Your help keeps our elders cared for", 440, ImageFont.truetype(semi, 40), ink)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
    qr.add_data(UPI_URI)
    qr.make(fit=True)
    q = qr.make_image(fill_color="black", back_color="white").get_image().convert("RGB")
    side = 600
    q = q.resize((side, side), Image.NEAREST)
    card_w, card_h = 720, 860
    cx, cy = (W - card_w) // 2, 560
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((cx + 10, cy + 16, cx + card_w + 10, cy + card_h + 16), 44, fill=90)
    im.paste((120, 70, 30), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx, cy, cx + card_w, cy + card_h), 44, fill=(255, 255, 255))
    centre("SCAN & PAY", cy + 34, ImageFont.truetype(bold, 52), ink)
    im.paste(q, ((W - side) // 2, cy + 120))
    centre("UPI ID", cy + 740, ImageFont.truetype(semi, 32), (120, 100, 90))
    centre(UPI_ID, cy + 780, ImageFont.truetype(bold, 46), ink)
    centre("Any UPI app  ·  Canara Bank", 1470, ImageFont.truetype(semi, 38), ink)
    centre("ದಯವಿಟ್ಟು ಸಹಾಯ ಮಾಡಿ", 1560, ImageFont.truetype(kn, 64), maroon)
    centre("Please donate & share", 1680, ImageFont.truetype(bold, 50), maroon)
    im.save(path)
    return path


def check_qr(path):
    import cv2
    got = cv2.QRCodeDetector().detectAndDecode(cv2.imread(path))[0]
    assert got == UPI_URI, f"end card QR decodes to {got!r}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips")
    ap.add_argument("out")
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--vbitrate", help="two-pass target video bitrate, e.g. 2100k (default: CRF 18 master)")
    a = ap.parse_args()
    work = a.out + ".work"
    os.makedirs(work, exist_ok=True)

    png = end_card(a.fonts, os.path.join(work, "card.png"))
    check_qr(png)
    # end card clip: slow push-in on the still, music bed under it
    bed = warm_bed(int(CARD * SR), SR, beat_from=99)
    bed = bed * 10 ** (-20 / 20) * np.minimum(1, (CARD * SR - np.arange(len(bed))) / (1.2 * SR))
    bed_wav = os.path.join(work, "bed.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2",
                    bed_wav], input=bed.astype(np.float32).tobytes(), check=True)
    card_mp4 = os.path.join(work, "card.mp4")
    frames = int(CARD * FPS)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", png, "-i", bed_wav, "-vf",
                    f"scale={W * 2}:{H * 2},zoompan=z='1+0.04*on/{frames}':x='iw/2-(iw/zoom/2)':"
                    f"y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},fade=t=out:st={CARD - 0.6}:d=0.6",
                    "-af", f"afade=t=out:st={CARD - 0.8}:d=0.8", "-t", str(CARD), "-c:v", "libx264", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", str(SR), "-f", "mov", card_mp4], check=True)

    inputs, parts = [], []
    for name, s, e in CUTS:
        inputs += ["-ss", f"{s}", "-to", f"{e}", "-i", os.path.join(a.clips, f"{name}_enhanced.mp4")]
        parts.append(e - s)
    inputs += ["-i", card_mp4]
    parts.append(CARD)

    # chain crossfades: video xfade + audio acrossfade, offsets from the running length
    fc, v, au, total = [], "[0:v]", "[0:a]", parts[0]
    for k in range(1, len(parts)):
        fc.append(f"[{k}:v]settb=AVTB,fps={FPS},format=yuv420p[v{k}i]")
        prev_v = f"[vx{k - 1}]" if k > 1 else "[v0i]"
        if k == 1:
            fc.append(f"{v}settb=AVTB,fps={FPS},format=yuv420p[v0i]")
        fc.append(f"{prev_v}[v{k}i]xfade=transition=fade:duration={XF}:offset={total - XF:.3f}[vx{k}]")
        fc.append(f"{au if k == 1 else f'[ax{k - 1}]'}[{k}:a]acrossfade=d={XF}:c1=tri:c2=tri[ax{k}]")
        total += parts[k] - XF
    n = len(parts) - 1
    fc.append(f"[ax{n}]aresample={SR},alimiter=limit=0.84:level=disabled[aout]")
    enc = ["-c:v", "libx264", "-preset", "slow", "-pix_fmt", "yuv420p"]
    common = ["-filter_complex", ";".join(fc), "-map", f"[vx{n}]", "-map", "[aout]"]
    if a.vbitrate:
        log = os.path.join(work, "x264pass")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, *common, *enc, "-b:v", a.vbitrate, "-pass", "1",
                        "-passlogfile", log, "-an", "-f", "mp4", os.devnull], check=True)
        rate = ["-b:v", a.vbitrate, "-pass", "2", "-passlogfile", log]
    else:
        rate = ["-crf", "18"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, *common, *enc, *rate, "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", *CLEAN, a.out + ".tmp.mp4"], check=True)
    # a stream copy drops the "Lavc libx264" encoder tag the first pass leaves on the video track
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out + ".tmp.mp4", "-c", "copy", "-movflags", "+faststart",
                    *CLEAN, "-metadata:s:v", "encoder=", "-metadata:s:v", "handler_name=", "-metadata:s:a",
                    "handler_name=", a.out], check=True)
    os.remove(a.out + ".tmp.mp4")
    print(f"{a.out}: {total:.1f}s")


if __name__ == "__main__":
    main()
