"""Reel 05 (Yours3D): "My little princess turned one" -- Sowmya (Manya's mother) tells how she ordered Manya's
figurine, in her own voice; the owner's reel 04 footage is cut in over her words. Plan: projects3d/reel05/plan.md.

  python projects3d/reel05/build.py SOWMYA_DIR REEL04_DIR          # -> out/3d/reel05.mp4

SOWMYA_DIR: the original takes IMG_41xx.MOV (20 Oct 2026); REEL04_DIR: reel 04's photos and clips. Not committed.
"""
import importlib.util
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import testimonial as T                 # noqa: E402

_spec = importlib.util.spec_from_file_location("reel04_build", os.path.join(HERE, "..", "reel04", "build.py"))
r4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r4)


def segments(sdir, mdir):
    take = lambda n: os.path.join(sdir, f"IMG_{n}.MOV")       # noqa: E731
    md = lambda key: T.v1.media(mdir, key)                     # noqa: E731
    still = lambda key: ImageOps.exif_transpose(Image.open(md(key))).convert("RGB")   # noqa: E731
    photo, render, fig = still("808397810"), still("IMG_20261014_140855"), still("20261019_183012")
    portrait = r4.view(photo, r4.PHOTO["full"])
    printed = r4.view(fig, (2050, 2000, 3600))

    def compare(n):
        top, bot = r4.view(photo, r4.PHOTO["mini"], (T.W, r4.HALF)), r4.view(fig, r4.FIG["mini"], (T.W, r4.HALF))
        im = r4.split(top, bot)
        yield from T.still_frames(im, n, zoom=(1.0, 1.04))

    S = T.Seg
    segs = [
        S(take(4133), 0.0, 2.66, "My little cute princess was turning one."),
        S(take(4135), 0.0, 5.02, "I wanted to gift her a memorable gift which she can preserve for a long time.",
          broll=[(1.7, 5.02, lambda n: T.still_frames(portrait, n))]),
        S(take(4145), 0.0, 2.58, "I shared my daughter pic to their WhatsApp.",
          broll=[(0.8, 2.58, lambda n: T.phone_still(portrait, n))], tags=[("1 PHOTO ON WHATSAPP", 250, 0.9, T.GREEN)]),
        S(take(4147), 1.72, 4.10, "They gave me two options to preview.",
          broll=[(0.0, 2.38, lambda n: T.still_frames(render, n, mode="contain"))],
          tags=[("2 FREE PREVIEWS", 250, 0.2, T.GOLD)]),
        S(take(4152), 0.0, 1.71, "Then I selected which I love."),
        S(take(4154), 0.0, 5.82, "Then they gave me an option to write a message on the base, then I filled "
          "Cute Little Manya on it.",
          broll=[(3.3, 5.82, lambda n: T.r2.clip(md("023315"), n, 0.0, 8.3, post=T.r2.STEADY))]),
        S(take(4155), 0.0, 3.56, "Once the figurine is printed, they shared me a photo in my WhatsApp.",
          broll=[(0.0, 1.5, lambda n: T.r2.clip(md("110913"), n, 6.0, 12.0, post=T.r2.STEADY)),
                 (1.6, 3.56, lambda n: T.phone_still(printed, n, appear=0.15))]),
        S(take(4159), 0.0, 4.42, "Once I upload, they delivered this figurine to me within 7 days.",
          tags=[("FREE DELIVERY  ·  WITHIN 7 DAYS", 250, 1.4, T.GOLD)]),
        S(take(4161), 0.0, 2.16, "Just I love this detailing.", hold=1.6, hold_frames=compare),
        S(take(4162), 0.0, 3.20, "Thank you Yours 3D India for this wonderful gift."),
        S(take(4177), 0.0, 3.21, "Get the customized 3D figurine according to your need."),
    ]
    return segs


TITLE = "HER 1ST BIRTHDAY GIFT"


def main():
    T.build("reel05", segments(sys.argv[1], sys.argv[2]), TITLE)


if __name__ == "__main__":
    main()
