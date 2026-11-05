"""Video 10 (science): "Socho, ek awaaz... jisne poori dharti ka chakkar laga diya" - Krakatoa 1883, the loudest sound
in recorded history, whose pressure wave went round the Earth more than three times. Owner, 5 Nov 2026: "Next video",
then "Approved" on the script. Narration in Devanagari for the voice, numbers written as words.
Facts: Krakatoa, a volcanic island in the Sunda Strait (then the Dutch East Indies), blew up on 27 August 1883; the
largest explosion was at 10:02 a.m. local time. Over 70% of the island was destroyed; at least 36,417 deaths (the
official figure), mostly from the tsunamis. RMS Norham Castle, about 64 km (40 mi) away: the captain wrote "the
ear-drums of over half my crew have been shattered". A pressure gauge at the Batavia gasworks, about 160 km (100 mi)
away, spiked by over 2.5 inches of mercury, about 172 dB. Heard in the Andaman and Nicobar Islands (~1,300 mi,
~2,100 km) "as of guns firing", and on Rodrigues near Mauritius (~4,800 km, ~3,000 mi) nearly four hours later,
thought to be cannon fire from a ship. Beyond that the wave was too faint for ears but barometers caught it: Calcutta
6 h 47 min after the blast, New York, Washington and Toronto within 18 hours; at some 50 stations the spike came back
about every 34 hours (one lap of ~40,000 km at the speed of sound) for up to 5 days: 7 passes, about 3.5 trips round
the globe (Royal Society 1888 report; Nautilus 2014; Wikipedia). Delhi to Singapore is ~4,150 km, under 4,800 km."""
import math
import os

from poster import (CORAL, CREAM, FADED, GOLD, GREEN, INK, MONO_FONT, RED, W, calendar, card, counter, cross,
                    draw_text, headline, path, person, prog, ring, stamp, tick, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, एक आवाज़... जिसने पूरी धरती का चक्कर लगा दिया। एक बार नहीं, तीन बार से भी ज़्यादा।"),
    dict(id="b2", text="ये कोई कहानी नहीं है। अट्ठारह सौ तिरासी में, ये सच में हुआ था।"),
    dict(id="b3", text="इंडोनेशिया के पास, समुद्र में एक ज्वालामुखी वाला टापू था: क्राकाटोआ। सत्ताईस अगस्त की सुबह, "
                       "दस बजकर दो मिनट पर... वो फट गया।"),
    dict(id="b4", text="धमाका इतना बड़ा था कि टापू का ज़्यादातर हिस्सा गायब हो गया। और उसकी सुनामी ने, छत्तीस हज़ार से "
                       "ज़्यादा लोगों की जान ले ली।"),
    dict(id="b5", text="पर इस कहानी का सबसे अजीब हिस्सा है, उसकी आवाज़।"),
    dict(id="b6", text="चौंसठ किलोमीटर दूर, समुद्र में एक जहाज़ खड़ा था। उसके कैप्टन ने लिखा: मेरे आधे से ज़्यादा लोगों "
                       "के कान के पर्दे फट गए।"),
    dict(id="b7", text="चौंसठ किलोमीटर दूर से।", gap=REVEAL_GAP),
    dict(id="b8", text="एक सौ साठ किलोमीटर दूर, एक मशीन ने आवाज़ नापी: एक सौ बहत्तर डेसिबल। यानी जेट इंजन के पास खड़े "
                       "होने से भी कहीं ज़्यादा।"),
    dict(id="b9", text="भारत के अंडमान में, दो हज़ार किलोमीटर दूर, लोगों को लगा... कहीं पास में तोपें चल रही हैं।"),
    dict(id="b10", text="और चार हज़ार आठ सौ किलोमीटर दूर, एक छोटे से टापू पर, चार घंटे बाद लोगों ने ये आवाज़ सुनी। "
                        "उन्हें लगा, किसी जहाज़ से तोप चली है।"),
    dict(id="b11", text="सोचो, अगर ये धमाका दिल्ली में होता... तो आवाज़ सिंगापुर तक सुनाई देती।"),
    dict(id="b12", text="पर उसके बाद, आवाज़ इतनी धीमी हो गई कि कान उसे सुन नहीं सकते थे। फिर भी, वो रुकी नहीं।"),
    dict(id="b13", text="उस ज़माने में, दुनिया भर के शहरों में हवा का दबाव नापने वाली मशीनें थीं: बैरोमीटर। और धमाके के "
                        "छह घंटे सैंतालीस मिनट बाद, कोलकाता के बैरोमीटर में अचानक एक झटका आया।"),
    dict(id="b14", text="अठारह घंटे में, ये झटका न्यूयॉर्क और वॉशिंगटन तक पहुँच गया।"),
    dict(id="b15", text="पर फिर कुछ और अजीब हुआ। लगभग हर चौंतीस घंटे में, वही झटका... फिर से आने लगा। क्यों?"),
    dict(id="b16", text="क्योंकि वो आवाज़, धरती का पूरा चक्कर लगाकर, वापस आ रही थी।", gap=REVEAL_GAP),
    dict(id="b17", text="धरती का एक चक्कर, करीब चालीस हज़ार किलोमीटर। आवाज़ की स्पीड से, यही चौंतीस घंटे।"),
    dict(id="b18", text="पाँच दिन तक, बैरोमीटर्स ने उसे बार-बार पकड़ा। तीन बार से भी ज़्यादा, पूरी धरती के चक्कर।"),
    dict(id="b19", text="जिस आवाज़ को सुनने के लिए कान छोटे पड़ गए... उसे पूरी धरती की हवा ने महसूस किया।"),
    dict(id="b20", text="तुम्हें पता था कि एक आवाज़, धरती का चक्कर लगा सकती है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Ek awaaz jisne dharti ke 3 chakkar lagaye",
    caption="Socho, ek awaaz... jisne poori dharti ka chakkar laga diya. Ek baar nahi, teen baar se bhi zyada 😳\n\n"
            "1883, Krakatoa: 64 km door ek jahaaz ke aadhe logon ke kaan ke parde phat gaye. Andaman mein logon ko "
            "laga topein chal rahi hain. 4,800 km door tak awaaz suni gayi.\n\n"
            "Phir kaan sun nahi paaye, par barometers ne pakda: har 34 ghante mein wahi jhatka, 5 din tak.\n\n"
            "Tumhe pata tha ki ek awaaz dharti ka chakkar laga sakti hai? Comment mein YES ya NO likho 👇",
    yt_title="Ek Awaaz Jisne Dharti Ke 3 Chakkar Lagaye 😳 | Krakatoa 1883",
    yt_description="1883 mein Indonesia ka Krakatoa jwalamukhi phata, aur itihaas ki sabse zordaar awaaz paida hui: 64 km "
                   "door kaan ke parde phate, Andaman tak topon jaisi awaaz, 4,800 km door tak suni gayi. Uske baad "
                   "kaan sun nahi paaye, par duniya bhar ke barometers ne pakda: wo dabaav ki lehar dharti ke 3 se "
                   "zyada chakkar laga gayi.",
    hashtags=["#krakatoa", "#volcano", "#sciencefacts", "#factsinhindi", "#history"],
    pinned_comment="Tumhe pata tha ki ek awaaz dharti ka chakkar laga sakti hai? 🌍 YES ya NO? 👇",
    sources=["Royal Society 1888, The Eruption of Krakatoa, and Subsequent Phenomena",
             "Nautilus 2014, The Sound So Loud That It Circled the Earth Four Times",
             "Wikipedia, 1883 eruption of Krakatoa"],
)

_find = asset_finder("krakatoa", "toxoplasma2", "mosquito")
P = {k: _find(k) for k in ("lithograph", "maps", "barograph", "steamship", "cannon", "jet", "ear_anatomy",
                           "earth_globe", "world_map")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("krakatoa", "toxoplasma2", "mosquito")]

LAND = (0.55, 0.47, 0.38)
# Places in percent of world_map.png, measured from the grid points used in sea_internet (Singapore, Perth, Mombasa,
# Chennai, Mumbai) with ~0.28 % per degree of longitude and ~0.55 % per degree of latitude around there.
WP = dict(krakatoa=(81.5, 59.0), andaman=(77.6, 48.8), rodrigues=(67.0, 66.0), kolkata=(76.1, 42.3),
          delhi=(71.2, 38.3), singapore=(81.0, 55.0), newyork=(20.5, 31.0), washington=(19.8, 32.5))
ASIA = (-13, 1051, 1100)        # the world map zoomed on the Indian Ocean: Krakatoa lands at (640, 1150)
WORLD = (W / 2, 1080, 520)      # the whole world map
KM_PX = 4800 / 311              # km per pixel on the ASIA map (Krakatoa to Rodrigues is 311 px)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def clamp01(x):
    return max(0.0, min(1.0, x))


def glow(cr, x, y, r, color=CORAL, alpha=1.0):
    if alpha <= 0 or r <= 0:
        return
    for k, a in ((2.6, 0.12), (1.6, 0.3), (1.0, 0.95)):
        cr.arc(x, y, r * k, 0, 2 * math.pi)
        cr.set_source_rgba(*color, a * alpha)
        cr.fill()


def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def mp(p, m=WORLD, aspect=1.884):
    """A place (name or (fx, fy) percent) on world_map.png drawn at m = (cx, cy, height)."""
    fx, fy = WP[p] if isinstance(p, str) else p
    cx, cy, h = m
    return cx + (fx / 100 - 0.5) * aspect * h, cy + (fy / 100 - 0.5) * h


def world(cr, t, t0, m=WORLD, alpha=1.0):
    _pic(cr, "world_map", m[0], m[1], m[2], t, t0, tint=LAND, alpha=alpha)


def map_pin(cr, x, y, s, color=RED, alpha=1.0):
    """A map pin whose tip is at (x, y)."""
    if alpha <= 0:
        return
    cr.move_to(x, y)
    cr.curve_to(x - s * 0.9, y - s * 1.1, x - s * 0.75, y - s * 2.0, x, y - s * 2.0)
    cr.curve_to(x + s * 0.75, y - s * 2.0, x + s * 0.9, y - s * 1.1, x, y)
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.arc(x, y - s * 1.35, s * 0.32, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill()


def pin(cr, t, t_in, place, label, m=WORLD, color=RED, size=30, label_at="below", text_color=INK):
    x, y = mp(place, m)
    p = prog(t, t_in, 0.3)
    map_pin(cr, x, y, size, color, p)
    if label:
        if label_at == "below":
            draw_text(cr, label, x, y + 14, 32, text_color, p, MONO_FONT, "ct", tracking=2)
        else:
            draw_text(cr, label, x + (24 if label_at == "right" else -24), y - size, 32, text_color, p, MONO_FONT,
                      "lm" if label_at == "right" else "rm", tracking=2)
    return x, y


def rings(cr, x, y, r, t, color=CORAL, alpha=1.0, n=3, width=6):
    """The sound front: a bright circle of radius r with fainter echoes inside it, pulsing outwards."""
    if alpha <= 0 or r <= 0:
        return
    for k in range(n):
        rr = r * (1 - 0.18 * k) - 6 * ((t * 3) % 1)
        if rr <= 0:
            continue
        cr.arc(x, y, rr, 0, 2 * math.pi)
        cr.set_source_rgba(*color, alpha * (1 - 0.3 * k))
        cr.set_line_width(width - k)
        cr.stroke()


def globe_lap(cr, t, t0, cx, cy, h, period=2.4, alpha=1.0, laps_from=None):
    """The Earth with the sound running round it on a tilted orbit, a bright pulse with a fading trail.
    laps_from: the time the pulse starts; returns the number of laps completed so far."""
    rx, ry, tilt = h * 0.68, h * 0.2, -0.25
    start = t0 if laps_from is None else laps_from
    a = 2 * math.pi * max(0.0, t - start) / period - math.pi / 2

    def pt(ang):
        x, y = rx * math.cos(ang), ry * math.sin(ang)
        return cx + x * math.cos(tilt) - y * math.sin(tilt), cy + x * math.sin(tilt) + y * math.cos(tilt)

    def orbit(back):
        cr.save()
        cr.set_dash([16, 14])
        cr.set_source_rgba(*CREAM, (0.25 if back else 0.6) * alpha)
        cr.set_line_width(4)
        rng = (math.pi, 2 * math.pi) if back else (0, math.pi)
        for i in range(61):
            ang = rng[0] + (rng[1] - rng[0]) * i / 60
            (cr.move_to if i == 0 else cr.line_to)(*pt(ang))
        cr.stroke()
        cr.restore()

    orbit(True)
    _pic(cr, "earth_globe", cx, cy, h, t, t0, alpha=alpha)
    orbit(False)
    if t > start:
        for k in range(12):                                  # the trail
            x, y = pt(a - 0.09 * k)
            glow(cr, x, y, 9 * (1 - k / 14), CORAL, alpha * (1 - k / 12) * (0.4 if math.sin(a - 0.09 * k) < 0 else 1))
    return int(max(0.0, t - start) / period)


def clock(cr, x, y, r, hh, mm, alpha=1.0, label=None, label_color=INK):
    """A plain analogue clock showing hh:mm."""
    if alpha <= 0:
        return
    cr.arc(x + 6, y + 10, r, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.97, 0.95, 0.90, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(r * 0.09)
    cr.stroke()
    for k in range(12):
        a = 2 * math.pi * k / 12
        l0 = 0.78 if k % 3 else 0.68
        cr.move_to(x + r * l0 * math.sin(a), y - r * l0 * math.cos(a))
        cr.line_to(x + r * 0.86 * math.sin(a), y - r * 0.86 * math.cos(a))
        cr.set_line_width(r * (0.05 if k % 3 else 0.08))
        cr.stroke()
    for a, l, wd in ((2 * math.pi * ((hh % 12) + mm / 60) / 12, 0.48, 0.09), (2 * math.pi * mm / 60, 0.7, 0.06)):
        cr.move_to(x, y)
        cr.line_to(x + r * l * math.sin(a), y - r * l * math.cos(a))
        cr.set_line_width(r * wd)
        cr.stroke()
    cr.arc(x, y, r * 0.07, 0, 2 * math.pi)
    cr.fill()
    if label:
        draw_text(cr, label, x, y + r + 18, max(26, int(r * 0.3)), label_color, alpha, MONO_FONT, "ct", tracking=2)


def chart(cr, x, y, w, h, t, spikes, alpha=1.0, color=INK, paper=(0.95, 0.92, 0.85), xlabel=None):
    """Barograph paper: a pressure line drawn left to right; spikes = [(x fraction, time it is drawn, height)]."""
    if alpha <= 0:
        return
    cr.rectangle(x + 8, y + 12, w, h)
    cr.set_source_rgba(0, 0, 0, 0.2 * alpha)
    cr.fill()
    cr.rectangle(x, y, w, h)
    cr.set_source_rgba(*paper, alpha)
    cr.fill()
    cr.set_source_rgba(0.55, 0.65, 0.80, 0.5 * alpha)
    cr.set_line_width(2)
    for k in range(1, 8):
        cr.move_to(x + w * k / 8, y)
        cr.line_to(x + w * k / 8, y + h)
        cr.move_to(x, y + h * k / 8)
        cr.line_to(x + w, y + h * k / 8)
    cr.stroke()
    keys = [(spikes[0][1] - 0.6, 0.0)] + [(ts, f) for f, ts, _ in spikes]   # the pen reaches each spike on its cue
    reach = min(1.0, keys[-1][1] + 0.6 * max(0.0, t - keys[-1][0]))
    for (ta, fa), (tb, fb) in zip(keys, keys[1:]):
        if t < tb:
            reach = fa + (fb - fa) * clamp01((t - ta) / max(0.01, tb - ta))
            break
    n = 240
    base = y + h * 0.62
    for i in range(n + 1):
        u = i / n
        if u > reach + 0.015:
            break
        v = 0.012 * math.sin(u * 70)
        for f, _, amp in spikes:
            v += amp * (math.exp(-((u - f) / 0.008) ** 2) - 0.4 * math.exp(-((u - f - 0.018) / 0.008) ** 2))
        (cr.move_to if i == 0 else cr.line_to)(x + w * u, base - v * h)
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(5)
    cr.stroke()
    if xlabel:
        draw_text(cr, xlabel, x + w, y + h + 14, 26, color, alpha, MONO_FONT, "rt", tracking=2)


def meter(cr, x, y0, y1, t, t_rise, level, marks, alpha=1.0):
    """A vertical loudness scale from y0 (0 dB) up to y1 (180 dB); the bar rises to `level` from t_rise.
    marks = [(dB, label, time it shows)]."""
    if alpha <= 0:
        return
    yy = lambda db: y0 - (y0 - y1) * db / 180
    rrect(cr, x - 40, y1 - 20, 80, y0 - y1 + 40, 40)
    cr.set_source_rgba(0.93, 0.89, 0.80, 0.25 * alpha)
    cr.fill()
    lvl = level * prog(t, t_rise, 1.2)
    rrect(cr, x - 28, yy(lvl), 56, y0 - yy(lvl) + 8, 28)
    cr.set_source_rgba(*CORAL, alpha)
    cr.fill()
    for db, lab, ts in marks:
        p = prog(t, ts, 0.3) * alpha
        if p <= 0:
            continue
        y = yy(db)
        path(cr, [(x + 50, y), (x + 90, y)], 1.0, 4, CREAM, p)
        draw_text(cr, f"{db} dB", x + 104, y, 38, CREAM, p, MONO_FONT, "lm")
        draw_text(cr, lab, x - 60, y, 40, CREAM, p, anchor="rm")


def crew(cr, t, t_red, x, y, n=12, cols=6, size=110, alpha=1.0):
    """The ship's crew as figures; 7 of the 12 (over half) turn red from t_red."""
    for i in range(n):
        cx, cy = x + (i % cols) * size * 0.75, y + (i // cols) * size * 1.25
        red = i % 2 == 0 or i == 7
        p = prog(t, t_red + 0.05 * i, 0.2)
        col = tuple(a + (b - a) * p for a, b in zip(INK, RED)) if red else INK
        person(cr, cx, cy, size, col, alpha)


def blast(cr, x, y, s, p, t, alpha=1.0):
    """The explosion as a starburst over a dark island; p 0 -> 1 grows it."""
    if p <= 0 or alpha <= 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(1, 0.32)
    cr.arc(0, s * 1.3, s * 0.9, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(0.25, 0.22, 0.20, alpha)
    cr.fill()
    for scale, color in ((1.0, CORAL), (0.72, GOLD), (0.42, CREAM)):
        n = 18
        for k in range(2 * n + 1):
            a = math.pi * k / n + 0.05 * math.sin(t * 4 + k)
            r = s * p * scale * (1.0 if k % 2 == 0 else 0.55) * (1 + 0.08 * math.sin(t * 9 + k * 1.7))
            (cr.move_to if k == 0 else cr.line_to)(x + r * math.cos(a), y + r * math.sin(a))
        cr.close_path()
        cr.set_source_rgba(*color, alpha)
        cr.fill()


def wave_line(cr, x0, x1, y, t, amp0, decay, color=CORAL, alpha=1.0, floor=0.06):
    """A sound wave running to the right whose height dies away but never quite reaches zero."""
    if alpha <= 0:
        return
    n = 220
    for i in range(n + 1):
        u = i / n
        a = amp0 * max(floor, math.exp(-u * decay))
        x = x0 + (x1 - x0) * u
        (cr.move_to if i == 0 else cr.line_to)(x, y + a * math.sin(u * 46 - t * 9))
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(6)
    cr.stroke()


def sea_wave(cr, x0, x1, y, t, h, alpha=1.0):
    """A tsunami: a tall dark wave crest over the sea line."""
    if alpha <= 0:
        return
    cr.move_to(x0, y + h * 0.6)
    n = 80
    for i in range(n + 1):
        u = i / n
        crest = math.exp(-((u - 0.55) / 0.16) ** 2)
        cr.line_to(x0 + (x1 - x0) * u, y + h * 0.6 - h * (0.12 * math.sin(u * 20 + t * 3) + 1.0 * crest))
    cr.line_to(x1, y + h)
    cr.line_to(x0, y + h)
    cr.close_path()
    cr.set_source_rgba(0.20, 0.38, 0.50, alpha)
    cr.fill()
    for i in range(n + 1):                                   # white foam along the crest, curling forward at the top
        u = i / n
        crest = math.exp(-((u - 0.55) / 0.16) ** 2)
        (cr.move_to if i == 0 else cr.line_to)(x0 + (x1 - x0) * u,
                                               y + h * 0.6 - h * (0.12 * math.sin(u * 20 + t * 3) + 1.0 * crest))
    cr.set_source_rgba(0.95, 0.97, 0.98, alpha)
    cr.set_line_width(12)
    cr.stroke()
    for k in range(3):                                       # swell lines inside the water
        yy = y + h * (0.72 + 0.09 * k)
        cr.move_to(x0, yy)
        for i in range(1, 41):
            u = i / 40
            cr.line_to(x0 + (x1 - x0) * u, yy + 8 * math.sin(u * 14 + t * 2 + k))
        cr.set_source_rgba(0.55, 0.72, 0.82, 0.6 * alpha)
        cr.set_line_width(4)
        cr.stroke()


# ---------- shots ----------
# Rules (style bible): a new picture every ~3 s cut on the word, the literal noun on screen, red = the key word.
# The recurring picture is the sound front: a coral ring spreading over the map, and a pulse running round the globe.

GLOBE = (W / 2, 1180, 620)


def h_hook(cr, t, tl, t0):                               # b1 frame 0: "a sound... that went round the whole Earth"
    t3 = T(tl, "b1", "तीन")
    laps = globe_lap(cr, t, -1, *GLOBE, period=1.35, laps_from=0.0)
    n = "3+" if t >= t3 else str(min(laps, 3))
    if laps or t >= t3:                                      # the counter shows up with the first full lap
        draw_text(cr, "LAPS", 900, 1560, 34, CREAM, 1.0, MONO_FONT, "ct", tracking=3)
        draw_text(cr, n, 900, 1600, 110, CORAL, 1.0, MONO_FONT, "ct")     # Anton's "+" is tiny
    stamp(cr, t, "MORE THAN 3 TIMES", t3, 400, 1660, 56, color=CORAL)
    headline(cr, t, "A SOUND THAT WENT AROUND", "THE EARTH", -1, min(1.8, T(tl, "b1", "धरती")), t_ghost=-1,
             small_color=CREAM, big_color=CORAL)


def k_real(cr, t, tl, t0):                               # b2 "this is no story: in 1883 it really happened"
    _pic(cr, "lithograph", W / 2, 1130, 0, t, t0, frame=(560, 712), rot=-0.02)
    draw_text(cr, "KRAKATOA, 1883 (LITHOGRAPH)", W / 2, 1505, 26, INK, 0.75 * prog(t, t0 + 0.3, 0.3), MONO_FONT, "ct",
              tracking=2)
    stamp(cr, t, "TRUE STORY", T(tl, "b2", "सच"), 780, 1640, 60)
    headline(cr, t, "NOT A STORY. IT HAPPENED IN", "1883", t0, T(tl, "b2", "तिरासी"))


def k_where(cr, t, tl, t0):                              # b3 "near Indonesia, a volcano island in the sea: Krakatoa"
    world(cr, t, t0, ASIA)
    draw_text(cr, "INDONESIA", 800, 1240, 34, INK, prog(t, T(tl, "b3", "इंडोनेशिया"), 0.3), MONO_FONT, "lt", tracking=3)
    x, y = pin(cr, t, T(tl, "b3", "क्राकाटोआ") - 0.2, "krakatoa", None, ASIA, size=40)
    if t > T(tl, "b3", "क्राकाटोआ"):
        ring(cr, x, y, 70, 40, prog(t, T(tl, "b3", "क्राकाटोआ"), 0.4))
    headline(cr, t, "A VOLCANO ISLAND:", "KRAKATOA", t0, T(tl, "b3", "क्राकाटोआ"))


def k_blast(cr, t, tl, t0):                              # b3 "...on 27 August at 10:02 in the morning, it exploded"
    tf = T(tl, "b3", "फट")
    card(cr, t, t0, 110, 600, ["27 AUGUST 1883"], size=50)
    clock(cr, 860, 690, 120, 10, 2, prog(t, T(tl, "b3", "दस") - 0.2, 0.3), "10:02 AM")
    blast(cr, W / 2, 1300, 360, prog(t, tf - 0.1, 0.35), t)
    headline(cr, t, "27 AUGUST, 10:02 AM:", "IT EXPLODED", t0, tf)


def k_gone(cr, t, tl, t0):                               # b4 "the blast was so big most of the island vanished"
    _pic(cr, "maps", W / 2, 1060, 0, t, t0, frame=(960, 569), rot=0.0)
    q = prog(t, t0 + 0.3, 0.3)
    draw_text(cr, "BEFORE", 300, 740, 40, INK, q, MONO_FONT, "cb", tracking=3)
    draw_text(cr, "AFTER", 780, 740, 40, RED, q, MONO_FONT, "cb", tracking=3)
    ring(cr, 330, 1240, 110, 95, prog(t, T(tl, "b4", "टापू"), 0.4), color=INK)
    tg = T(tl, "b4", "गायब")
    ring(cr, 790, 1265, 110, 70, prog(t, tg, 0.4))
    card(cr, t, tg + 0.2, 300, 1450, ["OVER 70% OF THE", "ISLAND WAS GONE"], size=48)
    headline(cr, t, "MOST OF THE ISLAND", "VANISHED", t0, tg)


def k_tsunami(cr, t, tl, t0):                            # b4 "...and its tsunami killed over 36,000 people"
    sea_wave(cr, 0, W, 1260, t, 420, prog(t, T(tl, "b4", "सुनामी") - 0.2, 0.4))
    counter(cr, t, T(tl, "b4", "छत्तीस") - 0.2, W / 2, 900, "36,417", 120)
    draw_text(cr, "PEOPLE (OFFICIAL COUNT)", W / 2, 1010, 36, INK, prog(t, T(tl, "b4", "छत्तीस") + 0.3, 0.3), MONO_FONT,
              "ct", tracking=2)
    headline(cr, t, "ITS TSUNAMI KILLED OVER", "36,000", t0, T(tl, "b4", "छत्तीस"))


def k_sound(cr, t, tl, t0):                              # b5 "but the strangest part of this story is its sound" (slate)
    blast(cr, W / 2, 1180, 120, 1.0, t, prog(t, t0, 0.3))
    for k in range(4):
        f = ((t - t0) * 0.45 + k / 4) % 1
        rings(cr, W / 2, 1180, 140 + 520 * f, t, CORAL, (1 - f) * prog(t, t0 + 0.2, 0.3), n=1)
    headline(cr, t, "THE STRANGEST PART:", "ITS SOUND", t0, T(tl, "b5", "आवाज़"), small_color=CREAM,
             big_color=CORAL)


def s_ship(cr, t, tl, t0):                               # b6 "64 km away, a ship stood in the sea"
    _pic(cr, "steamship", W / 2, 1100, 0, t, t0, frame=(900, 671), rot=0.015)
    draw_text(cr, "SYMBOLIC PHOTO", W / 2, 1455, 24, INK, 0.7 * prog(t, t0, 0.3), MONO_FONT, "ct", tracking=2)
    tc = T(tl, "b6", "चौंसठ")
    path(cr, [(120, 1560), (960, 1560)], prog(t, tc, 0.5), 6, RED, arrow=True)
    draw_text(cr, "64 KM FROM THE VOLCANO", W / 2, 1590, 40, RED, prog(t, tc + 0.3, 0.3), MONO_FONT, "ct", tracking=2)
    headline(cr, t, "64 KM AWAY:", "A SHIP", t0, T(tl, "b6", "जहाज़"))


def s_log(cr, t, tl, t0):                                # b6 "...its captain wrote: over half my crew's eardrums burst"
    q = prog(t, t0, 0.3)
    if q > 0:
        rrect(cr, 98, 612, 884, 330, 14)
        cr.set_source_rgba(0, 0, 0, 0.18 * q)
        cr.fill()
        rrect(cr, 90, 600, 884, 330, 14)
        cr.set_source_rgba(0.95, 0.92, 0.84, q)
        cr.fill()
        for i, line in enumerate(("\"THE EAR-DRUMS OF OVER", "HALF MY CREW HAVE", "BEEN SHATTERED.\"")):
            n = int(len(line) * clamp01((t - t0 - 0.2 - 0.45 * i) / 0.45))       # typed in, line by line
            draw_text(cr, line[:n], 130, 640 + 78 * i, 50, INK, q, MONO_FONT, "lt")
        draw_text(cr, "CAPTAIN, NORHAM CASTLE, 1883", 130, 880, 28, FADED, q, MONO_FONT, "lt", tracking=2)
    crew(cr, t, T(tl, "b6", "आधे"), 150, 1290, size=150)
    headline(cr, t, "THE CAPTAIN WROTE:", "EARDRUMS BURST", t0, T(tl, "b6", "फट"))


def s_64(cr, t, tl, t0):                                 # b7 "from 64 km away" (slate)
    _pic(cr, "ear_anatomy", W / 2, 1080, 0, t, t0, frame=(900, 666))
    ring(cr, 570, 1150, 70, 110, prog(t, t0 + 0.2, 0.4), color=CORAL)
    draw_text(cr, "EARDRUM", 640, 1290, 40, CORAL, prog(t, t0 + 0.4, 0.3), MONO_FONT, "lt", tracking=2)
    headline(cr, t, "FROM", "64 KM AWAY", t0, t0 + 0.2, small_color=CREAM, big_color=CORAL)


def s_db(cr, t, tl, t0):                                 # b8 "160 km away a gauge measured it: 172 decibels" (slate)
    tb = T(tl, "b8", "बहत्तर")
    meter(cr, 540, 1700, 640, t, T(tl, "b8", "डेसिबल") - 1.0, 172,
          [(60, "TALKING", t0 + 0.3), (120, "ROCK CONCERT", t0 + 0.6), (150, "JET ENGINE", t0 + 0.9),
           (172, "KRAKATOA", tb)])
    headline(cr, t, "160 KM AWAY, A GAUGE READ", "172 dB", t0, tb, small_color=CREAM, big_color=CORAL)


def s_jet(cr, t, tl, t0):                                # b8 "...louder even than standing next to a jet engine"
    _pic(cr, "jet", W / 2, 1100, 0, t, t0, frame=(940, 627), rot=-0.015)
    stamp(cr, t, "EVEN LOUDER", T(tl, "b8", "ज़्यादा"), W / 2, 1560, 64)
    headline(cr, t, "LOUDER THAN STANDING BY A", "JET ENGINE", t0, T(tl, "b8", "जेट"))


def s_andaman(cr, t, tl, t0):                            # b9 "in India's Andaman, 2,000 km away, people thought guns were firing"
    world(cr, t, t0, ASIA)
    kx, ky = mp("krakatoa", ASIA)
    ta = T(tl, "b9", "अंडमान")
    rings(cr, kx, ky, 2100 / KM_PX * prog(t, t0 + 0.2, ta - t0), t)
    pin(cr, t, ta, "andaman", "ANDAMAN (INDIA)", ASIA, label_at="left")
    map_pin(cr, kx, ky, 26, INK, 1.0)
    _pic(cr, "cannon", 820, 1560, 300, t, T(tl, "b9", "तोपें") - 0.2)
    card(cr, t, T(tl, "b9", "तोपें"), 90, 1520, ["\"LIKE GUNS FIRING\""], size=44)
    headline(cr, t, "2,000 KM AWAY, IN INDIA'S", "ANDAMAN", t0, ta)


def s_rodrigues(cr, t, tl, t0):                          # b10 "and 4,800 km away, on a small island, 4 hours later..."
    world(cr, t, t0, ASIA)
    kx, ky = mp("krakatoa", ASIA)
    ti = T(tl, "b10", "टापू")
    rings(cr, kx, ky, 2100 / KM_PX + (4800 - 2100) / KM_PX * prog(t, t0, ti - t0 + 0.2), t)
    map_pin(cr, kx, ky, 26, INK, 1.0)
    pin(cr, t, ti, "rodrigues", "RODRIGUES", ASIA, label_at="left")
    th = T(tl, "b10", "घंटे")
    clock(cr, 860, 1560, 110, 2, 2, prog(t, th - 0.2, 0.3), "4 HOURS LATER")
    headline(cr, t, "4,800 KM AWAY, AFTER", "4 HOURS", t0, th)


def s_cannon(cr, t, tl, t0):                             # b10 "...they thought a ship had fired a cannon"
    _pic(cr, "cannon", 560, 1150, 620, t, t0)
    tt = T(tl, "b10", "तोप")
    blast(cr, 300, 980, 90, prog(t, tt, 0.25), t)
    headline(cr, t, "THEY THOUGHT A SHIP", "FIRED A CANNON", t0, tt)


def s_delhi(cr, t, tl, t0):                              # b11 "if this blast were in Delhi, you'd hear it in Singapore"
    world(cr, t, t0, ASIA)
    dx, dy = pin(cr, t, T(tl, "b11", "दिल्ली") - 0.2, "delhi", "DELHI", ASIA, label_at="left")
    ts = T(tl, "b11", "सिंगापुर")
    rings(cr, dx, dy, 311 * prog(t, T(tl, "b11", "दिल्ली"), ts - T(tl, "b11", "दिल्ली")), t)
    pin(cr, t, ts, "singapore", "SINGAPORE", ASIA, label_at="right", color=CORAL)
    draw_text(cr, "4,800 KM", dx + 160, dy - 250, 40, RED, prog(t, ts, 0.3), MONO_FONT, "lb", tracking=2)
    headline(cr, t, "IF IT HAPPENED IN DELHI, HEARD IN", "SINGAPORE", t0, ts)


def s_faint(cr, t, tl, t0):                              # b12 "after that ears couldn't hear it. yet it didn't stop" (slate)
    wave_line(cr, 60, 1020, 1050, t, 220, 4.0, CORAL, prog(t, t0, 0.3))
    ts = T(tl, "b12", "सुन")
    draw_text(cr, "EARS", 260, 1450, 90, CREAM, prog(t, ts - 0.3, 0.3), anchor="cm")
    cross(cr, 260, 1600, 90, prog(t, ts, 0.3), color=CORAL)
    draw_text(cr, "MACHINES", 740, 1450, 90, CREAM, prog(t, T(tl, "b12", "रुकी"), 0.3), anchor="cm")
    tick(cr, 680, 1580, 90, prog(t, T(tl, "b12", "रुकी") + 0.2, 0.3), color=GREEN)
    headline(cr, t, "TOO FAINT FOR EARS, BUT", "IT KEPT GOING", t0, T(tl, "b12", "रुकी"), small_color=CREAM,
             big_color=CORAL)


def p_baro(cr, t, tl, t0):                               # b13 "cities everywhere had air-pressure machines: barometers"
    _pic(cr, "barograph", W / 2, 1120, 560, t, t0)
    card(cr, t, T(tl, "b13", "दबाव"), 170, 1480, ["IT RECORDS AIR PRESSURE", "ON A TURNING DRUM"], size=42)
    headline(cr, t, "CITIES ALL OVER THE WORLD HAD A", "BAROMETER", t0, T(tl, "b13", "बैरोमीटर"))


def p_kolkata(cr, t, tl, t0):                            # b13 "...6 h 47 min after the blast, Kolkata's barometer jolted"
    tj = T(tl, "b13", "झटका")
    chart(cr, 90, 800, 900, 520, t, [(0.7, tj, 0.32)], prog(t, t0, 0.3), xlabel="KOLKATA, 27 AUG 1883")
    card(cr, t, T(tl, "b13", "छह"), 110, 1420, ["6 HOURS 47 MINUTES", "AFTER THE BLAST"], size=50)
    headline(cr, t, "KOLKATA'S BAROMETER:", "A JOLT", t0, tj)


def p_world(cr, t, tl, t0):                              # b14 "within 18 hours, the jolt reached New York and Washington"
    world(cr, t, t0)
    kx, ky = mp("krakatoa")
    rings(cr, kx, ky, 40 + 720 * prog(t, t0, 2.4), t)
    map_pin(cr, kx, ky, 22, INK, 1.0)
    pin(cr, t, T(tl, "b14", "न्यूयॉर्क"), "newyork", "NEW YORK", label_at="right", size=26)
    pin(cr, t, T(tl, "b14", "वॉशिंगटन"), "washington", "WASHINGTON", label_at="left", size=26, color=CORAL)
    counter(cr, t, T(tl, "b14", "अठारह") - 0.1, W / 2, 1500, "18 H", 100)
    headline(cr, t, "WITHIN 18 HOURS:", "NEW YORK", t0, T(tl, "b14", "न्यूयॉर्क"))


def p_again(cr, t, tl, t0):                              # b15 "then, about every 34 hours, the same jolt came back. why?" (slate)
    t34 = T(tl, "b15", "चौंतीस")
    spikes = [(0.08, t0 + 0.2, 0.3), (0.36, t34, 0.24), (0.64, t34 + 0.7, 0.2), (0.92, t34 + 1.4, 0.17)]
    chart(cr, 70, 760, 940, 520, t, spikes, prog(t, t0, 0.3), xlabel="HOURS AFTER THE BLAST")
    for i in range(3):
        x0, x1 = 70 + 940 * spikes[i][0], 70 + 940 * spikes[i + 1][0]
        q = prog(t, spikes[i + 1][1], 0.3)
        path(cr, [(x0, 1340), (x1, 1340)], q, 4, CREAM, arrow=True)
        draw_text(cr, "34 H", (x0 + x1) / 2, 1360, 34, CREAM, q, MONO_FONT, "ct", tracking=2)
    headline(cr, t, "EVERY ~34 HOURS, AGAIN.", "WHY?", t0, T(tl, "b15", "क्यों"), small_color=CREAM, big_color=CORAL)


def g_lap(cr, t, tl, t0):                                # b16 "because the sound was coming back after a full lap" (slate)
    globe_lap(cr, t, t0, *GLOBE, period=1.6)
    headline(cr, t, "IT WAS COMING BACK", "AROUND THE EARTH", t0, T(tl, "b16", "चक्कर"), small_color=CREAM,
             big_color=CORAL)


def g_math(cr, t, tl, t0):                               # b17 "one lap ~40,000 km; at the speed of sound, 34 hours"
    rows = (("ONE LAP OF THE EARTH", "40,000 KM", T(tl, "b17", "चालीस")),
            ("SPEED OF SOUND", "~1,200 KM/H", T(tl, "b17", "स्पीड")),
            ("SO ONE LAP TAKES", "~34 HOURS", T(tl, "b17", "चौंतीस") - 0.2))
    for i, (lab, val, ts) in enumerate(rows):
        y = 700 + 260 * i
        p = prog(t, ts - 0.1, 0.3)
        draw_text(cr, lab, 110, y, 36, INK, p, MONO_FONT, "lt", tracking=2)
        draw_text(cr, val, 110, y + 50, 96, RED if i == 2 else INK, p, MONO_FONT, "lt")
    headline(cr, t, "40,000 KM AT THE SPEED OF SOUND:", "34 HOURS", t0, T(tl, "b17", "चौंतीस"))


def g_days(cr, t, tl, t0):                               # b18 "for 5 days barometers caught it again and again: 3+ laps" (slate)
    calendar(cr, t, T(tl, "b18", "पाँच") - 0.2, 300, 1050, ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"],
             "barographs", interval=0.3, w=380, h=400)
    laps = globe_lap(cr, t, t0, 790, 1080, 360, period=1.0)
    draw_text(cr, "LAPS: " + ("3+" if t >= T(tl, "b18", "तीन") else str(min(laps, 3))), 790, 1360, 56, CORAL,
              prog(t, t0 + 0.2, 0.3), MONO_FONT, "ct")
    headline(cr, t, "FOR 5 DAYS, MORE THAN", "3 LAPS", t0, T(tl, "b18", "तीन"), small_color=CREAM, big_color=CORAL)


def z_awe(cr, t, tl, t0):                                # b19 "a sound too big for ears... felt by the whole Earth's air" (slate)
    th = T(tl, "b19", "हवा")
    glow(cr, GLOBE[0], GLOBE[1], GLOBE[2] * 0.33, (0.55, 0.85, 1.0), 0.35 * prog(t, th - 0.2, 0.5))
    globe_lap(cr, t, t0, *GLOBE, period=1.6)
    draw_text(cr, "EARS", 170, 1640, 60, CREAM, prog(t, T(tl, "b19", "कान"), 0.3), anchor="cm")
    cross(cr, 300, 1640, 70, prog(t, T(tl, "b19", "कान") + 0.2, 0.3), color=CORAL)
    headline(cr, t, "TOO BIG FOR EARS, BUT", "THE AIR FELT IT", t0, th, small_color=CREAM, big_color=CORAL)


def e_question(cr, t, tl, t0):                           # b20 "did you know a sound can go round the Earth?"
    globe_lap(cr, t, t0, W / 2, 920, 420, period=1.4)
    yes_no_card(cr, t, T(tl, "b20", "यस") - 0.2, W / 2, 1460, w=560, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DID YOU KNOW A SOUND CAN", "CIRCLE THE EARTH?", t0, T(tl, "b20", "चक्कर"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_hook, "slate"),
    ("b2", None, k_real, "paper"),
    ("b3", None, k_where, "paper"), ("b3", "सत्ताईस", k_blast, "paper"),
    ("b4", None, k_gone, "paper"), ("b4", "और", k_tsunami, "paper"),
    ("b5", None, k_sound, "slate"),
    ("b6", None, s_ship, "paper"), ("b6", "कैप्टन", s_log, "paper"),
    ("b7", None, s_64, "slate"),
    ("b8", None, s_db, "slate"), ("b8", "यानी", s_jet, "paper"),
    ("b9", None, s_andaman, "paper"),
    ("b10", None, s_rodrigues, "paper"), ("b10", "उन्हें", s_cannon, "paper"),
    ("b11", None, s_delhi, "paper"),
    ("b12", None, s_faint, "slate"),
    ("b13", None, p_baro, "paper"), ("b13", "धमाके", p_kolkata, "paper"),
    ("b14", None, p_world, "paper"),
    ("b15", None, p_again, "slate"),
    ("b16", None, g_lap, "slate"),
    ("b17", None, g_math, "paper"),
    ("b18", None, g_days, "slate"),
    ("b19", None, z_awe, "slate"),
    ("b20", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, a boom on the explosion, thuds on the eardrums and the cannon, ticks (and music dips)
    before the 64 km punch, the re-hook, the lap reveal and the closing line, typing under the lap maths."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b3", "फट"), "thud", 0.0), (T(tl, "b6", "फट"), "thud", 0.0), (T(tl, "b10", "तोप"), "thud", 0.0),
           (T(tl, "b7", None) - 0.35, "tick", 0.0), (T(tl, "b15", None) - 0.35, "tick", 0.0),
           (T(tl, "b16", None) - 0.35, "tick", 0.0), (T(tl, "b20", None) - 0.35, "tick", 0.0),
           (T(tl, "b17", "चालीस"), "typing", 1.0), (T(tl, "b20", "यस"), "typing", 1.0)]
    for bid in ("b2", "b4", "b8", "b14"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
