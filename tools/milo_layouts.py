"""Rough layout sketches for the Milo thriller shots (PIL). The image model paints over them (tools/shots.py
"layout"), so each scary detail lands where the shot needs it: a silhouette, a glow, a gap under a door.

  python tools/milo_layouts.py OUT_DIR      -> one PNG per sketch below
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H = 512, 896


def base(top=(8, 12, 20), bot=(4, 6, 10)):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        f = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * f) for a, b in zip(top, bot)))
    return im, d


def stairs(d, x0, x1, top_y, inset, color=(30, 22, 16), edge=(60, 45, 30)):
    d.polygon([(x0, H), (x1, H), (x1 - inset, top_y), (x0 + inset, top_y)], fill=color)
    n = 10
    for k in range(n):
        y = H - k * (H - top_y) / n
        f = k / n
        d.line([(x0 + inset * f, y), (x1 - inset * f, y)], fill=edge, width=3)


def person(d, cx, top, h, col=(10, 8, 8)):
    r = h * 0.07
    d.ellipse([cx - r, top, cx + r, top + 2.2 * r], fill=col)
    d.polygon([(cx - h * 0.09, top + 2.3 * r), (cx + h * 0.09, top + 2.3 * r), (cx + h * 0.12, top + h),
               (cx - h * 0.12, top + h)], fill=col)


def sketches():
    out = {}
    # Video 1: "Mom never calls me sweetie"
    im, d = base()
    stairs(d, 40, 472, 380, 130)
    d.rectangle([180, 140, 332, 380], fill=(255, 190, 110))
    im = im.filter(ImageFilter.GaussianBlur(3))
    d = ImageDraw.Draw(im)
    d.polygon([(300, 160), (330, 150), (332, 380), (296, 380)], fill=(120, 70, 40))   # a shadow on the kitchen wall
    out["v1_kitchen"] = im
    im, d = base((6, 8, 14), (3, 4, 8))
    d.ellipse([150, 260, 362, 560], fill=(70, 110, 170))                              # face lit blue from below
    d.rectangle([200, 700, 312, 896], fill=(170, 210, 255))                            # phone
    out["v1_phone"] = im.filter(ImageFilter.GaussianBlur(25))
    im, d = base((6, 8, 14), (10, 10, 14))
    d.rectangle([0, 0, W, 420], fill=(5, 5, 8))
    d.polygon([(0, 420), (W, 420), (W, H), (0, H)], fill=(26, 22, 20))
    d.rectangle([300, 520, 400, 560], fill=(120, 170, 255))
    im = im.filter(ImageFilter.GaussianBlur(6))
    ImageDraw.Draw(im).rectangle([318, 528, 382, 552], fill=(200, 225, 255))
    out["v1_underbed"] = im
    im, d = base((10, 10, 14), (6, 6, 9))
    d.rectangle([90, 60, 422, 820], fill=(24, 20, 18))                                  # door
    d.rectangle([90, 820, 422, 840], fill=(255, 200, 140))                              # light under it
    d.rectangle([190, 818, 240, 842], fill=(8, 6, 6))                                   # two feet shadows
    d.rectangle([272, 818, 322, 842], fill=(8, 6, 6))
    out["v1_feet"] = im.filter(ImageFilter.GaussianBlur(2))
    im, d = base((10, 14, 24), (6, 7, 10))
    d.rectangle([300, 140, 480, 520], fill=(70, 100, 150))                              # moonlit window
    d.rectangle([20, 120, 150, 860], fill=(22, 18, 16))                                 # door
    person(d, 230, 330, 520, (120, 22, 24))                                             # Milo, red hoodie
    out["v1_choice"] = im.filter(ImageFilter.GaussianBlur(4))
    # Video 2: "He pointed behind me"
    im, d = base((6, 8, 14), (4, 5, 8))
    d.rectangle([40, 120, 472, 760], fill=(14, 20, 32))                                 # our window, night street
    d.rectangle([150, 330, 360, 640], fill=(40, 34, 30))                                # house across the street
    d.rectangle([215, 380, 295, 480], fill=(255, 200, 120))                             # its lit window
    person(d, 255, 392, 95)
    d.rectangle([40, 120, 472, 760], outline=(30, 26, 24), width=18)
    out["v2_window"] = im
    im, d = base((14, 18, 26), (6, 6, 10))
    d.rectangle([60, 80, 452, 900], fill=(255, 205, 140))                                # lit window up close
    person(d, 256, 220, 700, (60, 45, 40))
    d.polygon([(330, 420), (470, 330), (480, 350), (340, 450)], fill=(60, 45, 40))      # arm pointing
    out["v2_point"] = im.filter(ImageFilter.GaussianBlur(3))
    im, d = base((8, 10, 16), (5, 5, 8))
    d.rectangle([120, 80, 392, 860], fill=(36, 30, 26))                                 # closet doors
    d.rectangle([250, 80, 266, 860], fill=(0, 0, 0))                                    # the black gap
    out["v2_closet"] = im.filter(ImageFilter.GaussianBlur(2))
    im, d = base((14, 18, 26), (6, 6, 10))
    d.rectangle([60, 80, 452, 900], fill=(255, 205, 140))
    person(d, 256, 260, 640, (60, 45, 40))
    d.rectangle([150, 380, 362, 560], fill=(240, 236, 220))                             # paper pressed to the glass
    out["v2_note"] = im.filter(ImageFilter.GaussianBlur(3))
    im, d = base((6, 6, 10), (4, 4, 7))
    d.rectangle([150, 0, 362, 180], fill=(40, 36, 32))                                  # attic hatch, open, black
    d.rectangle([170, 20, 342, 160], fill=(0, 0, 0))
    d.rectangle([60, 180, 452, 896], fill=(30, 26, 22))                                 # closet below
    out["v2_hatch"] = im.filter(ImageFilter.GaussianBlur(2))
    # Video 3: "Never open the basement door"
    im, d = base((10, 10, 14), (6, 6, 8))
    d.rectangle([120, 100, 392, 860], fill=(46, 36, 28))
    d.rectangle([120, 860, 392, 872], fill=(255, 190, 120))                             # light under the door
    d.rectangle([228, 840, 262, 866], fill=(5, 4, 4))                                   # small fingers in the gap
    out["v3_gap"] = im.filter(ImageFilter.GaussianBlur(2))
    im, d = base((12, 12, 16), (8, 8, 10))
    d.polygon([(0, 0), (W, 0), (W, 300), (0, 520)], fill=(30, 30, 34))                  # ceiling corner
    d.ellipse([350, 120, 420, 180], fill=(30, 30, 30))
    d.ellipse([378, 140, 392, 154], fill=(255, 20, 20))                                 # red light
    out["v3_camera"] = im.filter(ImageFilter.GaussianBlur(2))
    return out


if __name__ == "__main__":
    os.makedirs(sys.argv[1], exist_ok=True)
    for k, im in sketches().items():
        im.save(os.path.join(sys.argv[1], f"{k}.png"))
    print("layouts:", ", ".join(sketches()))
