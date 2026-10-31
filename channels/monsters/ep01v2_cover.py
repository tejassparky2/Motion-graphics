"""Episode 1 v2 cover (Shorts thumbnail): one frame of the episode plus 2-4 big words -> 1080x1920 JPEG.

    python channels/monsters/ep01v2_cover.py                      # the three candidates + a phone-grid preview
    python channels/monsters/ep01v2_cover.py S15 35 "ONE SNAP." "GONE."    # one cover: shot, frame in the shot, lines
    python channels/monsters/ep01v2_cover.py --diorama    # the same from out/monsters/diorama/ -> diorama/cover.jpg

The frame comes from the clean shot render out/monsters/ep01v2/shots/<SHOT>.mp4 when it exists (no captions or hook
text burned in), else from out/monsters/ep01v2/picture.mp4 at the shot's first frame + `frame` (timing.json).
Rules (reports/Pokémon episodes story and animation.md TP16; CLAUDE.md): 3-4 words at most, readable at 160 px wide,
never the title repeated, no Pokémon terms, no fake play button, no HUD, no metadata in the file.
Writes out/monsters/ep01v2_cover.jpg (the pick), out/monsters/ep01v2/covers/cover_<name>.jpg (the candidates) and
out/monsters/ep01v2/covers/phone_grid.jpg (the candidates at 160 px wide, as in a Shorts grid).
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EP = os.path.join(ROOT, "out", "monsters", "ep01v2")
PICK_PATH = os.path.join(ROOT, "out", "monsters", "ep01v2_cover.jpg")
W, H = 1080, 1920
FONT = os.path.join(ROOT, "assets", "fonts", "LuckiestGuy-Regular.ttf")
INK = (14, 18, 40)                                               # dark navy, as the anime line colour
WHITE, HOT = (255, 255, 255), (255, 92, 60)                      # HOT marks the one word that carries the threat

# name: (shot, frame in the shot, [(line, colour), ...]); the first is the default pick
CANDIDATES = {
    "hook": ("S01", 30, [("IT ERASED", WHITE), ("A FOREST", HOT)]),
    "snap": ("S15", 65, [("ONE SNAP.", WHITE), ("GONE.", HOT)]),
    "deadpan": ("S20", 70, [("IT TRIED", WHITE), ("AGAIN.", HOT)]),
}
PICK = "hook"


def frame(shot, f):
    """One RGB frame (numpy, H x W x 3) of `shot` at frame `f` of the shot."""
    clean = os.path.join(EP, "shots", f"{shot}.mp4")
    if os.path.exists(clean):
        src, t = clean, f / 24
    else:
        with open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json")) as fh:
            s = {x["shot"]: x for x in json.load(fh)["shots"]}[shot]
        src, t = os.path.join(EP, "picture.mp4"), (s["first_frame"] + min(f, s["frames"] - 1)) / 24
        print(f"warning: no shots/{shot}.mp4 yet; using picture.mp4, which has the captions (and in S01 the hook "
              "text) burned in. Re-run once the clean shot lands.")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", src, "-frames:v", "1", "-vf",
                          f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    if len(raw) < W * H * 3:
        raise SystemExit(f"no frame at {shot} {f} in {src}")
    return np.frombuffer(raw[: W * H * 3], np.uint8).reshape(H, W, 3), src


def _fit(draw, text, max_w, size):
    while size > 60:
        font = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 6
    return ImageFont.truetype(FONT, size)


def cover(shot, f, lines, path):
    arr, src = frame(shot, f)
    img = Image.fromarray(arr).convert("RGB")
    # a soft dark band behind the words (top third, clear of the Shorts UI at the bottom and of faces mid-frame)
    y = np.arange(H)[:, None]
    shade = np.clip(1 - np.abs(y - 420) / 520, 0, 1) ** 1.5 * 0.55
    img = Image.fromarray((np.asarray(img, np.float32) * (1 - shade[..., None] * np.ones(3))).astype(np.uint8))
    draw = ImageDraw.Draw(img)
    top = 190
    for text, colour in lines:
        font = _fit(draw, text, W - 110, 230)
        box = draw.textbbox((0, 0), text, font=font, stroke_width=16)
        x = (W - (box[2] - box[0])) // 2 - box[0]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))           # drop shadow, then the stroked word
        ImageDraw.Draw(layer).text((x + 10, top + 14), text, font=font, fill=(0, 0, 0, 170), stroke_width=16,
                                   stroke_fill=(0, 0, 0, 170))
        img.paste(layer.filter(ImageFilter.GaussianBlur(8)), (0, 0), layer.filter(ImageFilter.GaussianBlur(8)))
        draw = ImageDraw.Draw(img)
        draw.text((x, top), text, font=font, fill=colour, stroke_width=16, stroke_fill=INK)
        top += (box[3] - box[1]) + 20
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=92, optimize=True)            # Pillow writes no EXIF/XMP unless given
    return path, src


def phone_grid(paths, out, w=160):
    """The candidates side by side at Shorts-grid size, labelled, to judge readability."""
    h = w * H // W
    sheet = Image.new("RGB", (len(paths) * (w + 16) + 16, h + 48), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for k, (name, p) in enumerate(paths):
        sheet.paste(Image.open(p).resize((w, h), Image.LANCZOS), (16 + k * (w + 16), 16))
        d.text((16 + k * (w + 16), h + 24), name, fill=(220, 220, 220))
    sheet.save(out, "JPEG", quality=92)


def main(argv):
    global EP, PICK_PATH
    if "--diorama" in argv:                                      # the 2.5D version: same shots, same frames
        argv = [a for a in argv if a != "--diorama"]
        EP = os.path.join(ROOT, "out", "monsters", "diorama")
        PICK_PATH = os.path.join(EP, "cover.jpg")
    if len(argv) >= 3:
        shot, f, words = argv[0], int(argv[1]), argv[2:]
        lines = [(w, HOT if k == len(words) - 1 else WHITE) for k, w in enumerate(words)]
        p, src = cover(shot, f, lines, PICK_PATH)
        print(p, "from", os.path.relpath(src, ROOT))
        return
    if EP.endswith("diorama"):                                   # only the pick ("hook") for the diorama version
        shot, f, lines = CANDIDATES[PICK]
        p, src = cover(shot, f, lines, PICK_PATH)
        print(f"{PICK} {shot} f{f} from {os.path.relpath(src, ROOT)} -> {os.path.relpath(p, ROOT)}")
        return
    made = []
    for name, (shot, f, lines) in CANDIDATES.items():
        p, src = cover(shot, f, lines, os.path.join(EP, "covers", f"cover_{name}.jpg"))
        print(f"{name:8} {shot} f{f} from {os.path.relpath(src, ROOT)} -> {os.path.relpath(p, ROOT)}")
        made.append((name, p))
    phone_grid(made, os.path.join(EP, "covers", "phone_grid.jpg"))
    shot, f, lines = CANDIDATES[PICK]
    cover(shot, f, lines, PICK_PATH)
    print("pick:", PICK, "->", os.path.relpath(PICK_PATH, ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
