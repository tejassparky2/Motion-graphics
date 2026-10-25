"""Reel 06 (Yours3D): "A gift for my husband" -- Sowmya tells how she ordered the couple figurine, in her own voice;
the owner's WhatsApp screen recordings (her photo going in, the two previews coming back) and making-of clips are cut
in over her words. Plan: projects3d/reel06/plan.md.

  python projects3d/reel06/build.py MEDIA_DIR          # -> out/3d/reel06.mp4

MEDIA_DIR: the owner's 20 Oct 2026 folder (IMG_41xx/42xx.MOV takes, the 12 Oct clips, the WhatsApp recordings).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import testimonial as T                 # noqa: E402


def segments(mdir):
    take = lambda n: os.path.join(mdir, f"IMG_{n}.MOV")       # noqa: E731
    md = lambda key: T.v1.media(mdir, key)                     # noqa: E731
    rec1, rec2 = md("152901_WhatsApp"), md("153010_WhatsApp")
    ph = T.r2.phone_frames
    S = T.Seg
    segs = [
        S(take(4164), 0.0, 4.70, "I was looking for a very premium and memorable gift to be gifted for my husband."),
        S(take(4171), 0.0, 2.72, "Then I came across Yours 3D India page.", tags=[("@yours3dindia", 250, 1.0, T.GOLD)]),
        S(take(4189), 0.0, 3.40, "Then I shared me and my husband's photo to them in WhatsApp.",
          broll=[(0.5, 3.40, lambda n: ph(rec1, n, 29.0, 34.0))]),
        S(take(4192), 0.0, 2.48, "Then they gave me two options to select from.",
          broll=[(0.0, 2.48, lambda n: ph(rec2, n, 0.5, 6.5))], tags=[("2 FREE PREVIEWS  ·  1–2 MIN", 250, 0.3, T.GOLD)]),
        S(take(4193), 0.0, 1.76, "Then I selected what I like."),
        S(take(4194), 0.0, 1.36, "And here it is.", hold=1.6,
          hold_frames=lambda n: T.r2.clip(md("155918"), n, 0.0, speed=1.0)),
        S(take(4197), 0.0, 4.62, "You can see the details. It's a pure replica of me and my husband's photo.",
          broll=[(1.4, 4.62, lambda n: T.r2.clip(md("152343"), n, 0.8, speed=1.0))]),
        S(take(4199), 0.0, 2.92, "When I gifted him, he was so emotional."),
        S(take(4201), 0.0, 1.90, "Then what are you waiting for?"),
        S(take(4208), 0.0, 4.10, "Send your memorable photo to Yours 3D India WhatsApp,",
          tags=[("+91 91647 48401", 250, 1.6, T.GREEN)]),
        S(take(4210), 0.0, 3.65, "and get your customized 3D figurine today!"),
    ]
    return segs


TITLE, END_EXTRA = "THE GIFT THAT MADE HIM EMOTIONAL", "COUPLE FIGURINES FROM ₹5,999"


def main():
    T.build("reel06", segments(sys.argv[1]), TITLE, end_extra=END_EXTRA)


if __name__ == "__main__":
    main()
