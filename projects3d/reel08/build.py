"""Reels 08 and 09 (Yours3D): Sowmya's two stories in her own voice, each in English and in Kannada (owner, 11 Nov
2026: "2 reels each in both languages, don't mix them, for hook keep which is best"; approved the same day).

  reel08     English: "A dad's gift for his son" (the baby figurine HARSHVARDHAN; the parents agreed to the name)
  reel08_kn  Kannada, same story (one take, from the father's part, not "Hi guys")
  reel09     English: the bulk order of name keychains, return gifts for a daughter's birthday
  reel09_kn  Kannada, same story (one take, cut before the "order on our website" ending: WhatsApp only)

Kannada reels: no captions (owner, 11 Nov 2026: "no caption for kannada ones just good edits"); the English lines in
those segments are only notes of what she says (Whisper's translation), not shown.
She says "7 to 10 days" for delivery: owner (11 Nov 2026) "keep".

  python projects3d/reel08/build.py "out/3d/reel08/raw/Reel2" [reel08 reel08_kn reel09 reel09_kn]
"""
import importlib.util
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("testimonial", os.path.join(HERE, "..", "testimonial.py"))
T = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T)
Seg = T.Seg

WA = ("WHATSAPP +91 91647 48401", T.GREEN)


def tag(text, at, y=250, colour=T.GOLD):
    return (text, y, at, colour)


def reel08(m):
    return [
        Seg(m("5523"), 0.0, 5.4, "This is a cute story, where the father gave the order to print a little cute son "
            "of them."),
        Seg(m("5524"), 0.0, 6.6, "I think this is the best, most preserving gift, where the father or a parent "
            "gifted to their children.", tags=[tag("A GIFT TO KEEP FOREVER", 1.0)]),
        Seg(m("5542"), 0.0, 5.95, "After sending a photo, we'll be giving two options to select from. Once you "
            "approve, we'll be starting to print.", tags=[tag("2 FREE PREVIEWS", 2.2)]),
        Seg(m("5553"), 0.0, 6.7, "We'll be shipping within 7 to 10 days, and there will be free shipping all over "
            "India.", tags=[tag("FREE SHIPPING ACROSS INDIA", 3.8)]),
        Seg(m("5531"), 0.0, 7.9, "Then what are you waiting for? You need a customized figurine like this? Then "
            "WhatsApp us, and get your customization done today.", tags=[tag(*WA[:1], 4.8, colour=WA[1])]),
    ]


def reel08_kn(m):
    k = m("5558")
    return [
        Seg(k, 11.9, 16.15, "A father gave the best gift to his son,"),
        Seg(k, 16.15, 20.4, "to keep his son's image forever. I really loved it."),
        Seg(k, 20.4, 26.0, "You should get yours customized too. So why wait?"),
        Seg(k, 26.0, 31.5, "We give you 2 options to choose from.", tags=[tag("2 FREE PREVIEWS", 0.6)]),
        Seg(k, 31.5, 35.8, "Once you approve, we start printing."),
        Seg(k, 35.8, 38.5, "It reaches your home within 7 to 10 days.", tags=[tag("FREE DELIVERY · 7–10 DAYS", 0.4)]),
        Seg(k, 38.5, 43.85, "Want a figurine like this? WhatsApp us now.", tags=[tag(*WA[:1], 1.0, colour=WA[1])]),
        Seg(k, 43.85, 45.2, "Tata!"),
    ]


def reel09(m, magnet):
    hook = (0.0, 1.3, lambda n: T.still_frames(magnet, n, zoom=(1.06, 1.0)))
    return [
        Seg(m("5565"), 0.0, 4.06, "Hi guys, one of my customers saw my video and gave the bulk order to us.",
            broll=[hook]),
        Seg(m("5567"), 0.0, 3.45, "They customized this cute little keychain for their daughter's birthday.",
            tags=[tag("RETURN GIFTS", 0.4)]),
        Seg(m("5591"), 0.0, 9.8, "They shared their photo to us on WhatsApp, then we restyled this with a base "
            "name. Also guys, if you need an anime base or a cartoon base with a name, also we can customize.",
            tags=[tag("1 PHOTO ON WHATSAPP", 1.0, colour=T.GREEN), tag("ANIME OR CARTOON + NAME", 6.4, y=345)]),
        Seg(m("5604"), 0.0, 7.3, "If you need this customized keychain, then WhatsApp your photo and get your "
            "customization done today. Thank you.", tags=[tag(*WA[:1], 2.4, colour=WA[1])]),
    ]


def reel09_kn(m, magnet):
    k = m("5564")
    hook = (0.0, 1.3, lambda n: T.still_frames(magnet, n, zoom=(1.06, 1.0)))
    return [
        Seg(k, 0.0, 4.0, "I'm so happy, I got this bulk order!", broll=[hook]),
        Seg(k, 4.0, 10.0, "One of our clients ordered return gifts for his daughter's birthday.",
            tags=[tag("RETURN GIFTS", 0.5)]),
        Seg(k, 10.0, 13.0, "A bulk order, as return gifts."),
        Seg(k, 13.0, 20.0, "They send us photos on WhatsApp. We restyle the photos and add their names.",
            tags=[tag("1 PHOTO ON WHATSAPP", 0.5, colour=T.GREEN)]),
        Seg(k, 20.0, 29.0, "We can do a god design with the name, or a cartoon photo with the name."),
        Seg(k, 29.0, 37.3, "You can use it as a fridge magnet, or as a kitchen magnet.",
            tags=[tag("FRIDGE MAGNET", 0.6)]),
        Seg(k, 37.3, 43.0, "Send your photos to our WhatsApp.", tags=[tag(*WA[:1], 0.5, colour=WA[1])]),
        Seg(k, 43.0, 47.0, "Once you approve, we start printing."),
        Seg(k, 47.0, 49.95, "You'll receive it within 7 to 10 days."),
    ]


def main():
    mdir = sys.argv[1]
    which = sys.argv[2:] or ["reel08", "reel08_kn", "reel09", "reel09_kn"]
    m = lambda key: T.v1.media(mdir, key)          # noqa: E731
    T.FLIP = True       # all 14 takes are front-camera: "HARSHVARDHAN" and the keychain names read backwards
    magnet = ImageOps.exif_transpose(Image.open(m("20261111_012927"))).convert("RGB")
    os.makedirs(os.path.join(T.ROOT, "out", "3d", "kannada"), exist_ok=True)
    jobs = {
        "reel08": lambda: T.build("reel08", reel08(m), "A DAD'S GIFT FOR HIS SON"),
        "reel08_kn": lambda: T.build(os.path.join("kannada", "reel08_kn"), reel08_kn(m), "A DAD'S GIFT FOR HIS SON",
                                     whole=True, captions=False),
        "reel09": lambda: T.build("reel09", reel09(m, magnet), "SHE SAW OUR REEL. THEN ORDERED IN BULK", price=False),
        "reel09_kn": lambda: T.build(os.path.join("kannada", "reel09_kn"), reel09_kn(m, magnet),
                                     "A BULK ORDER OF RETURN GIFTS", whole=True, price=False, captions=False),
    }
    for w in which:
        jobs[w]()


if __name__ == "__main__":
    main()
