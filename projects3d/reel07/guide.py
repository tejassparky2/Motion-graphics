"""The "Comment 3D" guide for reel 07 viewers: "Make your mini you", photo to 3D figurine in 4 steps, as a phone-shaped
PDF (9:16 pages, big type), with the owner's real screens (ChatGPT, Tripo, Snapmaker Orca) and real numbers.

  python3 projects3d/reel07/guide.py "out/3d/reel07/raw2/Photo to 3d" "out/3d/reel04/raw/Raw videos"
  -> out/3d/reel07/guide/Yours3D_mini_you_guide.pdf  (out/3d is not in git: it has Manya's photo)

Manya's photo and name are shown with her mother's consent (19 Oct 2026). Tripo settings: the owner's (2 Nov 2026: "pbr off and remove lighting on"). PROMPT below: the first lines are the
owner's (read off the 2 Nov screen recording); the rest is a draft until the owner sends the exact text.
"""
import io
import os
import subprocess
import sys

from PIL import Image, ImageOps
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "out", "3d", "reel07", "guide")
PW, PH = 450, 800                       # points; 9:16 so it reads like a phone screen
M = 30                                  # side margin

GOLD, GOLD_LIGHT = Color(201 / 255, 168 / 255, 108 / 255), Color(230 / 255, 205 / 255, 150 / 255)
INK, CARD = Color(17 / 255, 18 / 255, 20 / 255), Color(32 / 255, 32 / 255, 36 / 255)
WHITE, GREY, GREEN = Color(1, 1, 1), Color(0.72, 0.72, 0.74), Color(37 / 255, 211 / 255, 102 / 255)

pdfmetrics.registerFont(TTFont("Serif", "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"))
pdfmetrics.registerFont(TTFont("SerifReg", "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))       # has ₹ → •
pdfmetrics.registerFont(TTFont("SansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))

WHATSAPP, WA_LINK = "+91 91647 48401", "https://wa.me/919164748401"

PROMPT = """Turn the person (or people) in my photo into a photo of a semi-realistic 3D-printed collectible figurine.

LIKENESS
• Keep their face shape, skin tone, hairstyle, facial hair, glasses and outfit so they are instantly recognisable.
• Keep the same expression and the same accessories (jewellery, bags, bows).

STYLE
• Semi-realistic, not cartoon: a slightly bigger head and eyes, smooth surfaces, clean details.
• Solid matte colours a multi-colour 3D printer can print: no gradients, glitter or tiny patterns.

POSE
• Full body, standing, facing the camera, arms close to the body, feet flat and slightly apart.
• Nothing thin or floating: no loose strands of hair, spread fingers or objects sticking out.

PRINTING
• One solid piece, sturdy enough to print about 14 cm tall.

BACKGROUND
• Plain white background, soft even light, the whole figure in the frame."""

HEADINGS = {"LIKENESS", "STYLE", "POSE", "PRINTING", "BACKGROUND"}
CHANGES = ["Make her standing", "Remove the white ball in her hand", "Make the shirt black, we don't have that blue colour"]


# ---------- images ----------

def frame(path, t):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-f",
                                   "image2pipe", "-vcodec", "png", "-"])
    return Image.open(io.BytesIO(raw)).convert("RGB")


def media(d, key):
    hits = [f for f in os.listdir(d) if key in f]
    assert len(hits) == 1, (key, hits)
    return os.path.join(d, hits[0])


def still(d, key):
    return ImageOps.exif_transpose(Image.open(media(d, key))).convert("RGB")


def jpeg(im, maxw=1100):
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=84, optimize=True)
    b.seek(0)
    return ImageReader(b), im.width / im.height


def cover_crop(im, aspect):
    """Centre crop of `im` to width/height = aspect."""
    if im.width / im.height > aspect:
        w = round(im.height * aspect)
        return im.crop(((im.width - w) // 2, 0, (im.width + w) // 2, im.height))
    h = round(im.width / aspect)
    return im.crop((0, (im.height - h) // 2, im.width, (im.height + h) // 2))


# ---------- drawing ----------

def wrap(text, font, size, width):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            t = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= width or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


class Page:
    def __init__(self, c, n=None):
        self.c, self.y = c, PH - M
        c.setFillColor(INK)
        c.rect(0, 0, PW, PH, stroke=0, fill=1)
        if n is not None:
            c.setFont("SerifReg", 9)
            c.setFillColor(GREY)
            c.drawString(M, 18, "Yours3D India · @yours3dindia")
            c.drawRightString(PW - M, 18, str(n))

    def step(self, k, tool):
        c = self.c
        seg = (PW - 2 * M - 3 * 6) / 4
        for i in range(4):
            c.setFillColor(GOLD if i <= k else CARD)
            c.roundRect(M + i * (seg + 6), self.y - 5, seg, 5, 2.5, stroke=0, fill=1)
        self.y -= 26
        c.setFont("SerifReg", 11)
        c.setFillColor(GOLD_LIGHT)
        c.drawString(M, self.y, f"STEP {k + 1} OF 4")
        self.y -= 34
        c.setFont("Serif", 30)
        c.setFillColor(WHITE)
        c.drawString(M, self.y, tool)
        self.y -= 16

    def title(self, text, size=26, color=WHITE):
        for ln in wrap(text, "Serif", size, PW - 2 * M):
            self.y -= size * 1.1
            self.c.setFont("Serif", size)
            self.c.setFillColor(color)
            self.c.drawString(M, self.y, ln)
        self.y -= 8

    def text(self, text, size=12.5, color=WHITE, font="Sans", indent=0, gap=6, lead=1.38):
        for ln in wrap(text, font, size, PW - 2 * M - indent):
            self.y -= size * lead
            self.c.setFont(font, size)
            self.c.setFillColor(color)
            self.c.drawString(M + indent, self.y, ln)
        self.y -= gap

    def bullets(self, items, size=12.5, color=WHITE, mark="•"):
        for it in items:
            y0 = self.y
            self.text(it, size, color, indent=16, gap=3)
            self.c.setFont("SansBold", size)
            self.c.setFillColor(GOLD)
            self.c.drawString(M, y0 - size * 1.38, mark)
        self.y -= 4

    def numbered(self, items, size=12.5):
        for i, it in enumerate(items, 1):
            y0 = self.y
            self.text(it, size, indent=26, gap=4)
            cy = y0 - size * 1.38 + size * 0.35
            self.c.setFillColor(GOLD)
            self.c.circle(M + 9, cy, 9, stroke=0, fill=1)
            self.c.setFont("SansBold", 10)
            self.c.setFillColor(INK)
            self.c.drawCentredString(M + 9, cy - 3.5, str(i))
        self.y -= 4

    def image(self, img, h=None, w=None, radius=10, border=True):
        reader, aspect = img
        wmax = w or PW - 2 * M
        hmax = h or wmax / aspect
        w = min(wmax, hmax * aspect)            # fit inside wmax x hmax, keeping the picture's shape
        h = w / aspect
        x = (PW - w) / 2
        self.y -= h
        c = self.c
        c.saveState()
        p = c.beginPath()
        p.roundRect(x, self.y, w, h, radius)
        c.clipPath(p, stroke=0, fill=0)
        c.drawImage(reader, x, self.y, w, h)
        c.restoreState()
        if border:
            c.setStrokeColor(GOLD)
            c.setLineWidth(1)
            c.roundRect(x, self.y, w, h, radius, stroke=1, fill=0)
        self.y -= 12

    def box(self, lines, size, font="Mono", pad=12, color=WHITE, fill=CARD, title=None):
        """A card with text, for copy-paste (real text, so it can be selected and copied)."""
        c = self.c
        inner = PW - 2 * M - 2 * pad
        rows = []
        for ln in lines:
            rows += wrap(ln, font, size, inner) if ln else [""]
        h = len(rows) * size * 1.35 + 2 * pad + (18 if title else 0)
        c.setFillColor(fill)
        c.setStrokeColor(GOLD)
        c.roundRect(M, self.y - h, PW - 2 * M, h, 10, stroke=1, fill=1)
        y = self.y - pad
        if title:
            c.setFont("SansBold", 10)
            c.setFillColor(GOLD)
            c.drawString(M + pad, y - 9, title)
            y -= 18
        for r in rows:
            y -= size * 1.35
            c.setFont(font, size)
            c.setFillColor(GOLD_LIGHT if r.strip() in HEADINGS else color)
            c.drawString(M + pad, y + size * 0.3, r)
        self.y -= h + 12

    def pill(self, text, fill, color=INK, size=13, x=None):
        c = self.c
        w = pdfmetrics.stringWidth(text, "SansBold", size) + 30
        x = (PW - w) / 2 if x is None else x
        self.y -= size + 14
        c.setFillColor(fill)
        c.roundRect(x, self.y, w, size + 14, (size + 14) / 2, stroke=0, fill=1)
        c.setFont("SansBold", size)
        c.setFillColor(color)
        c.drawCentredString(x + w / 2, self.y + 8.5, text)
        self.y -= 8
        return x, self.y + 8, w, size + 14


# ---------- the guide ----------

def main():
    mdir, r4dir = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    chat, tripo = media(mdir, "141710_ChatGPT"), media(mdir, "180351")
    orca, orca2 = media(mdir, "150551"), media(mdir, "150840")

    photo = jpeg(cover_crop(still(r4dir, "808397810").crop((420, 0, 2300, 1856)), 0.75), 700)
    design = jpeg(cover_crop(still(mdir, "IMG_20261014_140855"), 0.75), 700)
    fig = jpeg(cover_crop(still(r4dir, "183012").crop((700, 600, 3000, 3900)), 0.75), 700)
    s_prompt = jpeg(frame(chat, 12.0).crop((0, 180, 1080, 1000)))
    s_change = jpeg(frame(chat, 57.5).crop((0, 140, 1080, 1250)))
    s_settings = jpeg(frame(tripo, 14.5).crop((0, 90, 900, 1025)))     # panel closed: its PBR/lighting differ
    s_model = jpeg(frame(tripo, 48.0).crop((440, 120, 1240, 1025)))
    s_paint = jpeg(frame(orca, 62.0).crop((520, 70, 1880, 1030)))
    s_table = jpeg(frame(orca2, 30.0).crop((1395, 85, 1835, 530)))
    s_support = jpeg(cover_crop(frame(media(mdir, "184635"), 6.0), 1.0))
    s_final = jpeg(cover_crop(frame(media(mdir, "182700"), 1.0), 0.8))

    path = os.path.join(OUT, "Yours3D_mini_you_guide.pdf")
    c = canvas.Canvas(path, pagesize=(PW, PH), invariant=1, pageCompression=1)
    c.setTitle("Make your mini you · Yours3D India")
    c.setAuthor("Yours3D India")
    c.setSubject("Photo to 3D figurine in 4 steps")
    c.setCreator("")
    c._doc.info.producer = ""

    # 1. cover
    p = Page(c)
    p.y -= 6
    p.pill("FREE GUIDE · YOURS3D INDIA", GOLD, size=11, x=M)
    p.y -= 6
    p.title("MAKE YOUR MINI YOU", 40)
    p.text("Turn your photo into a 3D printed figurine, in 4 steps. With the exact prompt and every setting we "
           "use.", 16, GOLD_LIGHT, font="SerifReg", gap=18)
    w3 = (PW - 2 * M - 2 * 10) / 3
    y = p.y - w3 / 0.75
    for i, (img, lab) in enumerate([(photo, "PHOTO"), (design, "DESIGN"), (fig, "FIGURINE")]):
        x = M + i * (w3 + 10)
        c.saveState()
        pa = c.beginPath()
        pa.roundRect(x, y, w3, w3 / 0.75, 8)
        c.clipPath(pa, stroke=0, fill=0)
        c.drawImage(img[0], x, y, w3, w3 / 0.75)
        c.restoreState()
        c.setStrokeColor(GOLD)
        c.roundRect(x, y, w3, w3 / 0.75, 8, stroke=1, fill=0)
        c.setFont("SansBold", 9.5)
        c.setFillColor(GOLD)
        c.drawCentredString(x + w3 / 2, y - 14, lab)
    p.y = y - 50
    p.numbered(["ChatGPT: photo to a semi-realistic 3D design", "Tripo: design to a full 3D model",
                "Slicer: paint the colours it missed", "Print, remove supports, sand by hand"], 15)
    p.y = 70
    p.text("Made by Yours3D India, a 3D printing studio. This one is Manya, 1 year old, shown with her family's OK.",
           10.5, GREY)
    c.showPage()

    # 2. what you need + the photo
    p = Page(c, 2)
    p.title("What you need")
    p.bullets(["A clear photo of the person (ask them first)", "ChatGPT (image generation)",
               "A Tripo account (tripo3d.ai; each model uses credits)",
               "A slicer: Bambu Studio, OrcaSlicer or Snapmaker Orca (all free)",
               "A multi-colour 3D printer (we use a Snapmaker U1; a Bambu Lab A1 with AMS lite works too), "
               "or one colour and paint it by hand"])
    p.y -= 4
    p.title("Pick the right photo", 22)
    p.text("Good photos give good figurines:", 12.5, GOLD_LIGHT, gap=2)
    p.bullets(["Sharp and in focus", "Face clearly visible, looking at the camera", "Bright, even light",
               "Whole body in the frame, if you want the outfit"], mark="✓")
    p.text("These usually fail:", 12.5, GOLD_LIGHT, gap=2)
    p.bullets(["Blurry or dark photos", "Side faces", "Sunglasses or hands over the face",
               "Group photos where faces are tiny"], mark="✗")
    c.showPage()

    # 3. step 1: ChatGPT
    p = Page(c, 3)
    p.step(0, "ChatGPT")
    p.numbered(["Open a new chat and tap + → Photos. Attach your photo.",
                "Paste the prompt from the next page and send.",
                "Wait about a minute. Check the face, the outfit and the colours.",
                "Not right? Just ask for changes in plain words (examples on the next page).",
                "Download the final image (full size, not a screenshot)."])
    p.image(s_prompt, h=min(250, p.y - 260))
    p.text("Then ask for changes, like we did:", 12, GOLD_LIGHT, gap=4)
    p.image(s_change, h=p.y - 45)
    c.showPage()

    # 4. the prompt
    p = Page(c, 4)
    p.title("The prompt")
    p.text("Copy it exactly. It keeps the likeness and makes a design that can actually be printed.", 12, GREY,
           gap=10)
    p.box(PROMPT.split("\n"), 9.6, title="COPY + PASTE INTO CHATGPT")
    p.title("Not right the first time?", 18, GOLD_LIGHT)
    p.text("Reply in plain words. These are the real changes we asked for:", 11.5, GREY, gap=4)
    p.bullets([f"“{x}”" for x in CHANGES], 11.5)
    c.showPage()

    # 5. step 2: Tripo
    p = Page(c, 5)
    p.step(1, "Tripo")
    p.numbered(["On tripo3d.ai, open 3D Workspace → Generate Model → HD Model.",
                "Upload the design image from ChatGPT.",
                "Open Geometry & Texture and use our settings below. Then tap Generate.",
                "When the model appears, turn it around and check the back. Then tap Export and choose 3MF (the direct 'send to slicer' button sends STL only, with no colours)."],
               12)
    p.box(["Ultra Mesh Quality ......... ON", "AI Complete ................ OFF", "Texture .................... ON",
           "Texture Quality ............ 4K", "Remove Lighting ............ ON", "PBR ........................ OFF",
           "Topology ................... Triangle", "Polycount .................. 200000"], 10.2,
          title="OUR TRIPO SETTINGS")
    half = (PW - 2 * M - 10) / 2
    y0 = p.y
    for i, img in enumerate([s_settings, s_model]):
        h = min(y0 - 40, half / img[1])
        x = M + i * (half + 10)
        c.saveState()
        pa = c.beginPath()
        pa.roundRect(x, y0 - h, half, h, 8)
        c.clipPath(pa, stroke=0, fill=0)
        c.drawImage(img[0], x, y0 - h, half, h, preserveAspectRatio=True, anchor="n")
        c.restoreState()
        c.setStrokeColor(GOLD)
        c.roundRect(x, y0 - h, half, h, 8, stroke=1, fill=0)
    c.showPage()

    # 6. step 3: slicer
    p = Page(c, 6)
    p.step(2, "The slicer")
    p.numbered(["Open the 3MF in your slicer (we use Snapmaker Orca for the U1; Bambu Studio works the same). "
                "Our Tripo 3MF opens with the colours already on it. If Bambu Studio says the file is not from "
                "Bambu Lab, that's fine: it loads the shape and the colours.",
                "Scale it to the size you want. Ours: 82 × 82 × 140 mm.",
                "Open Colour painting. Zoom in and paint what Tripo missed: eyes, eyebrows, lips, small details.",
                "Turn on supports, then slice."], 11.8)
    p.image(s_paint, h=min(230, p.y - 150))
    p.box(["Nozzle 0.4 mm · Layer 0.2 mm · First layer 0.25 mm", "4 colours of PLA · Supports on"], 10.2,
          font="Sans", title="OUR SETTINGS")
    c.showPage()

    # 7. step 4: print + finish
    p = Page(c, 7)
    p.step(3, "Print + finish")
    p.text("Our real numbers for this figurine, from the slicer:", 12, GREY, gap=8)
    stats = [("11 h", "print time"), ("950", "colour changes"), ("193 g", "filament in total")]
    w3 = (PW - 2 * M - 20) / 3
    for i, (v, u) in enumerate(stats):
        x = M + i * (w3 + 10)
        c.setFillColor(CARD)
        c.setStrokeColor(GOLD)
        c.roundRect(x, p.y - 64, w3, 64, 10, stroke=1, fill=1)
        c.setFont("Serif", 24)
        c.setFillColor(WHITE)
        c.drawCentredString(x + w3 / 2, p.y - 32, v)
        c.setFont("Sans", 9)
        c.setFillColor(GOLD_LIGHT)
        c.drawCentredString(x + w3 / 2, p.y - 50, u)
    p.y -= 78
    p.text("Of those 193 g, only 83 g is the figurine. 85 g went into the prime tower, which primes the nozzle after "
           "every colour change, and 25 g into supports. Fewer colours means less waste.", 11.5, gap=8)
    p.numbered(["When it's done, let it cool, then lift it off the plate.",
                "Remove the supports slowly, from the outside in, with flush cutters. Don't twist thin parts.",
                "Sand the marks smooth by hand."], 11.8)
    half = (PW - 2 * M - 10) / 2
    y0 = p.y
    h = min(y0 - 40, half / 0.8)
    for i, img in enumerate([s_support, s_final]):
        x = M + i * (half + 10)
        c.saveState()
        pa = c.beginPath()
        pa.roundRect(x, y0 - h, half, h, 8)
        c.clipPath(pa, stroke=0, fill=0)
        c.drawImage(img[0], x, y0 - h, half, h, preserveAspectRatio=True, anchor="c")
        c.restoreState()
        c.setStrokeColor(GOLD)
        c.roundRect(x, y0 - h, half, h, 8, stroke=1, fill=0)
    c.showPage()

    # 8. table of the slice + checklist
    p = Page(c, 8)
    p.title("Quick checklist")
    p.bullets(["Photo: sharp, face visible, good light, their OK", "ChatGPT: our prompt, then ask for changes",
               "Tripo: HD Model, 4K texture, Remove Lighting on, PBR off", "Slicer: open the 3MF, paint the eyes, supports on, slice",
               "Print, supports off slowly, sand by hand"], mark="✓")
    p.image(s_table, h=min(250, p.y - 60))
    p.text("The slicer's own summary for this print (Snapmaker Orca).", 10, GREY)
    c.showPage()

    # 9. let us make it
    p = Page(c, 9)
    p.y -= 40
    p.title("Rather not do it yourself?", 30)
    p.text("Send us one photo. We design it, print it in full colour with the name on the base, and finish it by "
           "hand.", 14, GOLD_LIGHT, font="SerifReg", gap=14)
    p.image(fig, h=250)
    x, y, w, h = p.pill(f"WhatsApp {WHATSAPP}", GREEN, size=15)
    c.linkURL(WA_LINK, (x, y, x + w, y + h), relative=0)
    p.y -= 4
    p.bullets(["2 free previews in 1–2 minutes", "Figurines from ₹3,599 (incl. taxes)",
               "Free delivery across India, within 7 days"], 13)
    p.text("Instagram @yours3dindia", 12, GREY)
    c.showPage()
    c.save()
    print(path, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    main()
