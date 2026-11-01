"""Video 6 (tech): "AI bas agla shabd guess karta hai" - how ChatGPT-style AI works. Script approved by the owner
1 Nov 2026 ("Approve"; scripts_batch4.md); narration below is that script word for word, in Devanagari for the
voice, with numbers and English words written for the voice (AI = "ए-आई").
Hook v2 (owner, 1 Nov 2026: "The hook is not good change it and auto approved"): b1 now says the model holds no
written answers, no book, no search, only numbers (true of the model itself: its weights); b2 is the next-word game
and the phone keyboard."""
import math
import os
import random

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MONO_FONT, RED, W, calendar, card, counter, cross, draw_text,
                    footnote, gauge, headline, path, person, prog, stamp, text_size, tick)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, जो ए-आई डॉक्टर्स वाले एग्ज़ाम के सवाल हल कर लेता है... उसके अंदर एक भी जवाब लिखा हुआ नहीं है। "
                       "ना कोई किताब, ना गूगल। सिर्फ़ नंबर्स।"),
    dict(id="b2", text="और वो बस एक ही काम करता है: अगला शब्द गेस करना। वही जो तुम्हारे फ़ोन का कीबोर्ड करता है... "
                       "बस बहुत, बहुत बड़ा।"),
    dict(id="b3", text="ये कोई जादू नहीं है। ये गणित है।", gap=REVEAL_GAP),
    dict(id="b4", text="पहले इसे पढ़ाया जाता है: इंटरनेट की किताबें, आर्टिकल्स, कोड... खरबों शब्द।"),
    dict(id="b5", text="मेटा के ए-आई, लामा थ्री, ने जितना पढ़ा... उतना पढ़ने में एक इंसान को, रोज़ आठ घंटे पढ़कर भी, "
                       "दो लाख साल से ज़्यादा लगेंगे।"),
    dict(id="b6", text="पर ये पढ़ता कैसे है? एक खेल खेलकर। वाक्य का आख़िरी शब्द छिपा दो... और ए-आई से कहो: गेस करो।"),
    dict(id="b7", text="जैसे: चाय में चीनी नहीं डाली, तो चाय होगी... ए-आई कहता है: मीठी? ग़लत। सही जवाब: फीकी।"),
    dict(id="b8", text="हर ग़लती पर, उसके अंदर के अरबों छोटे-छोटे नॉब्स थोड़े से घुमाए जाते हैं, जैसे पंखे का रेगुलेटर... "
                       "ताकि अगली बार गेस थोड़ा बेहतर हो।"),
    dict(id="b9", text="जी-पी-टी थ्री में ऐसे एक सौ पचहत्तर अरब नॉब्स थे।"),
    dict(id="b10", text="और ये खेल खरबों बार खेला जाता है। हफ़्तों-महीनों तक, हज़ारों कंप्यूटर्स पर।"),
    dict(id="b11", text="पर रुको... अगर ये बस शब्द गेस करता है, तो इतने समझदार जवाब कैसे देता है?"),
    dict(id="b12", text="क्योंकि अगला शब्द सही गेस करने के लिए, उसे सीखना पड़ता है कि दुनिया कैसे चलती है: ग्रामर, फ़ैक्ट्स, "
                        "यहाँ तक कि लॉजिक भी।"),
    dict(id="b13", text="जब तुम सवाल पूछते हो, वो एक शब्द चुनता है... फिर उसे जोड़कर अगला... फिर अगला। "
                        "जब तक जवाब पूरा न हो जाए।"),
    dict(id="b14", text="इसीलिए जवाब ऐसे टाइप होता हुआ दिखता है। वो सच में एक-एक करके बन रहा होता है।"),
    dict(id="b15", text="और हर बार थोड़ी सी किस्मत भी। इसलिए एक ही सवाल दो बार पूछो, तो जवाब थोड़ा अलग आता है।"),
    dict(id="b16", text="पर इसकी एक कमज़ोरी भी है। ये सच नहीं, सबसे सही लगने वाला शब्द चुनता है।"),
    dict(id="b17", text="इसलिए कभी-कभी ये पूरे भरोसे से ग़लत बात बोल देता है। इसे कहते हैं: हैलुसिनेशन।",
         gap=REVEAL_GAP),
    dict(id="b18", text="सोचो, एक मशीन जो बस अगला शब्द गेस करती है... और फिर भी कविता लिखती है, कोड बनाती है, "
                        "एग्ज़ाम के सवाल हल करती है।"),
    dict(id="b19", text="तो क्या ए-आई सच में समझता है... या बस बहुत अच्छा गेस करता है? कमेंट में बताओ।"),
]

METADATA = dict(
    title="AI bas agla shabd guess karta hai",
    caption="Jo AI doctors ke exam ke sawaal hal kar leta hai, uske andar ek bhi jawab likha hua nahi hai... sirf "
            "numbers 😳\n\nAur wo bas ek kaam karta hai: agla shabd guess karna.\n\n"
            "Tumhare phone ke keyboard jaisa, bas bahut bada. Har galat guess par iske andar ke arbon \"knobs\" thode "
            "ghumaaye jaate hain. GPT-3 mein 175 arab the.\n\n"
            "Isiliye jawab ek-ek shabd karke type hota dikhta hai, aur kabhi-kabhi ye poore bharose se galat bhi bol "
            "deta hai.\n\n"
            "AI sach mein samajhta hai, ya bas bahut accha guess karta hai? Comment mein batao 👇",
    yt_title="ChatGPT Ke Andar Ek Bhi Jawab Nahi Hai? 😳 | AI",
    yt_description="ChatGPT jaisa AI asal mein kaise kaam karta hai: agla shabd guess karna, kharabon shabd padhkar "
                   "seekhna, aur har galti par arbon knobs ko thoda ghumaana. Jawab ek-ek shabd karke kyun aata hai, "
                   "ek hi sawaal ka jawab alag kyun aata hai, aur AI kabhi-kabhi galat kyun bolta hai.",
    hashtags=["#ai", "#chatgpt", "#techinhindi", "#howitworks", "#factsinhindi"],
    pinned_comment="AI sach mein samajhta hai, ya bas bahut accha guess karta hai? 🤖 Comment mein batao 👇",
    sources=["Nori et al. 2023, Capabilities of GPT-4 on Medical Challenge Problems (Microsoft, OpenAI)",
             "Brown et al. 2020, Language Models are Few-Shot Learners (OpenAI)",
             "Meta 2024, Introducing Meta Llama 3"],
)

_find = asset_finder("ai", "toxoplasma2")
P = {k: _find(k) for k in ("stethoscope", "chai", "books", "servers", "earth_globe")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("ai", "toxoplasma2")]

SCREEN, BODY, KEY = (0.97, 0.97, 0.95), (0.13, 0.13, 0.14), (0.83, 0.85, 0.88)
ME, BOT = (0.80, 0.92, 0.80), (0.91, 0.93, 0.98)          # chat bubbles: the user's question, the AI's answer
QUESTION = "How many chambers does the human heart have?"
ANSWER = "The human heart has four chambers: two atria and two ventricles."


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def phone(cr, cx, cy, h, alpha=1.0):
    """A plain phone (no brand): dark body, light screen. Returns the screen rectangle (x, y, w, h)."""
    w = h * 0.49
    x, y = cx - w / 2, cy - h / 2
    rrect(cr, x + 10, y + 16, w, h, w * 0.12)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.fill()
    rrect(cr, x, y, w, h, w * 0.12)
    cr.set_source_rgba(*BODY, alpha)
    cr.fill()
    sx, sy, sw, sh = x + w * 0.05, y + h * 0.06, w * 0.9, h * 0.89
    rrect(cr, sx, sy, sw, sh, w * 0.08)
    cr.set_source_rgba(*SCREEN, alpha)
    cr.fill()
    rrect(cr, cx - w * 0.12, y + h * 0.018, w * 0.24, h * 0.022, h * 0.011)
    cr.set_source_rgba(0.05, 0.05, 0.05, alpha)
    cr.fill()
    return sx, sy, sw, sh


def bubble(cr, x, y, w, text, n=None, fill=BOT, size=30, alpha=1.0, right=False, cursor=False, t=0.0):
    """A chat bubble showing the first n words of `text`, wrapped to width w; (x, y) is its top-left corner (top-right
    when `right`). Returns its height."""
    words = text.split()
    shown = words if n is None else words[:max(0, int(n))]
    lines, cur = [], ""
    for wd in shown:
        test = (cur + " " + wd).strip()
        if cur and text_size(test, size, MONO_FONT)[0] > w - 44:
            lines.append(cur)
            cur = wd
        else:
            cur = test
    lines.append(cur)
    lh = size * 1.4
    h = len(lines) * lh + 34
    bw = w if len(lines) > 1 else min(w, text_size(lines[0] or " ", size, MONO_FONT)[0] + 70)
    bx = x - bw if right else x
    rrect(cr, bx, y, bw, h, 26)
    cr.set_source_rgba(*fill, alpha)
    cr.fill()
    for i, ln in enumerate(lines):
        draw_text(cr, ln, bx + 22, y + 17 + i * lh, size, INK, alpha, MONO_FONT)
    if cursor and int(t * 3) % 2 == 0:                     # the blinking "typing" block
        lw = text_size(lines[-1] or " ", size, MONO_FONT)[0] if lines[-1] else 0
        cr.rectangle(bx + 28 + lw, y + 17 + (len(lines) - 1) * lh + 4, size * 0.55, size)
        cr.set_source_rgba(*INK, 0.8 * alpha)
        cr.fill()
    return h


def chat(cr, rect, t, t_type, n_words=None, answer=ANSWER, alpha=1.0, wps=3.2):
    """The question bubble, then the answer typing itself from t_type (wps words a second, or n_words if given)."""
    sx, sy, sw, sh = rect
    hq = bubble(cr, sx + sw - 24, sy + 60, sw * 0.82, QUESTION, fill=ME, right=True, alpha=alpha)
    n = n_words if n_words is not None else (t - t_type) * wps
    if n > 0:
        done = n >= len(answer.split())
        bubble(cr, sx + 24, sy + 90 + hq, sw * 0.86, answer, n=n + 1e-6, alpha=alpha, cursor=not done, t=t)


def keyboard(cr, x, y, w, typed, chips, pick_p=0.0, alpha=1.0):
    """A phone keyboard with a text field above it and three next-word suggestion chips; chip 0 lights up with pick_p."""
    rrect(cr, x, y, w, 120, 22)
    cr.set_source_rgba(*SCREEN, alpha)
    cr.fill()
    draw_text(cr, typed, x + 26, y + 40, 38, INK, alpha, MONO_FONT)
    ky = y + 150
    rrect(cr, x, ky, w, 470, 22)
    cr.set_source_rgba(*KEY, alpha)
    cr.fill()
    cw = (w - 40) / 3
    for i, c in enumerate(chips):
        cx = x + 20 + i * cw
        rrect(cr, cx + 6, ky + 16, cw - 12, 70, 16)
        lit = pick_p if i == 0 else 0.0
        cr.set_source_rgba(*(GOLD if lit > 0.5 else SCREEN), alpha)
        cr.fill()
        draw_text(cr, c, cx + cw / 2, ky + 51, 38, INK, alpha, MONO_FONT, "cm")
    for r, row in enumerate(("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")):
        kw = (w - 40) / 10
        off = x + 20 + (10 - len(row)) * kw / 2
        for i, ch in enumerate(row):
            kx, kyy = off + i * kw, ky + 110 + r * 115
            rrect(cr, kx + 5, kyy, kw - 10, 95, 12)
            cr.set_source_rgba(1, 1, 1, alpha)
            cr.fill()
            draw_text(cr, ch, kx + kw / 2, kyy + 47, 36, INK, alpha, MONO_FONT, "cm")


def knob(cr, x, y, r, ang, alpha=1.0, numbers=False):
    """A fan-regulator knob; ang is the pointer angle in radians from straight up."""
    if numbers:
        for i in range(5):
            a = -2.2 + 1.1 * i
            draw_text(cr, str(i + 1), x + r * 1.45 * math.sin(a), y - r * 1.45 * math.cos(a), r * 0.38, INK, alpha,
                      MONO_FONT, "cm")
    cr.arc(x + r * 0.08, y + r * 0.12, r, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, 0.2 * alpha)
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.93, 0.92, 0.88, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.5 * alpha)
    cr.set_line_width(max(1.5, r * 0.06))
    cr.stroke()
    cr.arc(x, y, r * 0.62, 0, 2 * math.pi)
    cr.set_source_rgba(0.25, 0.25, 0.27, alpha)
    cr.fill()
    cr.move_to(x, y)
    cr.line_to(x + r * 0.55 * math.sin(ang), y - r * 0.55 * math.cos(ang))
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.set_line_width(max(1.5, r * 0.12))
    cr.stroke()


def knob_wall(cr, t, t0, x0, y0, cols, rows, gap, r, turning=(), alpha=1.0):
    """A wall of tiny knobs fading in; the ones in `turning` turn a little back and forth."""
    rng = random.Random(4)
    for i in range(cols * rows):
        q = prog(t, t0 + 0.012 * i, 0.25) * alpha
        a = rng.uniform(-2, 2) + (0.5 * math.sin(t * 4 + i) if i in turning else 0)
        knob(cr, x0 + (i % cols) * gap, y0 + (i // cols) * gap, r, a, q)


def dice(cr, x, y, s, v, rot=0.0, alpha=1.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    rrect(cr, -s / 2 + 8, -s / 2 + 12, s, s, s * 0.18)
    cr.set_source_rgba(0, 0, 0, 0.2 * alpha)
    cr.fill()
    rrect(cr, -s / 2, -s / 2, s, s, s * 0.18)
    cr.set_source_rgba(0.98, 0.97, 0.94, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.5 * alpha)
    cr.set_line_width(3)
    cr.stroke()
    pips = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
            5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
    for px, py in pips[v]:
        cr.arc(px * s * 0.26, py * s * 0.26, s * 0.08, 0, 2 * math.pi)
        cr.set_source_rgba(*(RED if v == 1 else INK), alpha)
        cr.fill()
    cr.restore()


def balance(cr, x, y, w, tilt, left, right, alpha=1.0):
    """A drawn balance: the beam tilts by `tilt` radians (positive = left side down); a label card on each pan."""
    cr.move_to(x, y)
    cr.line_to(x - 70, y + 420)
    cr.line_to(x + 70, y + 420)
    cr.close_path()
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.fill()
    ends = []
    for s in (-1, 1):
        ex, ey = x + s * w / 2 * math.cos(tilt), y - s * w / 2 * math.sin(tilt)
        ends.append((ex, ey))
    path(cr, ends, 1.0, 12, INK, alpha)
    for (ex, ey), lab in zip(ends, (left, right)):
        path(cr, [(ex, ey), (ex - 90, ey + 170)], 1.0, 3, INK, alpha)
        path(cr, [(ex, ey), (ex + 90, ey + 170)], 1.0, 3, INK, alpha)
        cr.arc(ex, ey + 170, 110, 0, math.pi)
        cr.set_source_rgba(*GOLD, alpha)
        cr.fill()
        draw_text(cr, lab, ex, ey + 300, 50, INK, alpha, anchor="ct")      # under the pan, clear of the strings


def ai_box(cr, x, y, s, alpha=1.0, glow=0.0):
    """The model, drawn as a chip: a dark square with pins and "AI" on it."""
    for i in range(5):
        for side in (-1, 1):
            o = -s * 0.36 + i * s * 0.18
            path(cr, [(x + o, y + side * s / 2), (x + o, y + side * (s / 2 + 26))], 1.0, 8, (0.55, 0.55, 0.58), alpha)
            path(cr, [(x + side * s / 2, y + o), (x + side * (s / 2 + 26), y + o)], 1.0, 8, (0.55, 0.55, 0.58), alpha)
    rrect(cr, x - s / 2, y - s / 2, s, s, s * 0.1)
    cr.set_source_rgba(*BODY, alpha)
    cr.fill()
    if glow > 0:
        cr.arc(x, y, s * 0.75, 0, 2 * math.pi)
        cr.set_source_rgba(*GOLD, 0.25 * glow * alpha)
        cr.fill()
    draw_text(cr, "AI", x, y, s * 0.42, CREAM, alpha, anchor="cm")


def sentence(cr, t, x, y, words, size=64, alpha=1.0, blank=None):
    """Words in a row (Anton); `blank` (text, p) draws the next slot: a yellow sticky note while p < 1, the word after."""
    cx = x
    for wd in words:
        draw_text(cr, wd, cx, y, size, INK, alpha)
        cx += text_size(wd, size)[0] + size * 0.3
    if blank:
        txt, p = blank
        if p < 1:
            cr.save()
            cr.translate(cx + 90, y + size * 0.55)
            cr.rotate(-0.04)
            cr.rectangle(-90, -size * 0.7, 180, size * 1.4)
            cr.set_source_rgba(0.98, 0.86, 0.30, alpha)
            cr.fill()
            draw_text(cr, "?", 0, 0, size, INK, alpha, anchor="cm")
            cr.restore()
        else:
            draw_text(cr, txt, cx, y, size, GREEN, alpha)
    return cx


def candidates(cr, t, t0, x, y, opts, chosen_at=None, alpha=1.0):
    """Next-word candidates with probability bars; the first one is picked (green tick) at chosen_at."""
    for i, (wd, pct) in enumerate(opts):
        q = prog(t, t0 + 0.12 * i, 0.3) * alpha
        yy = y + i * 110
        draw_text(cr, wd, x, yy, 52, INK, q, MONO_FONT)
        cr.rectangle(x + 330, yy + 6, 380 * pct / 100 * prog(t, t0 + 0.2 + 0.12 * i, 0.5), 48)
        cr.set_source_rgba(*(GREEN if i == 0 else (0.55, 0.50, 0.42)), 0.85 * q)
        cr.fill()
        draw_text(cr, f"{pct}%", x + 330 + 390 * pct / 100 + 14, yy + 6, 40, INK, q, MONO_FONT)
        if i == 0 and chosen_at is not None:
            tick(cr, x - 60, yy + 28, 50, prog(t, chosen_at, 0.3))


# ---------- shots ----------
# Rules (style bible): a new picture every ~3 s cut on the word, the literal noun on screen, red = the key word,
# gold = numbers, green = right; the fan-regulator knob is the one recurring metaphor (the model's settings).

def h_phone(cr, t, tl, t0):                              # b1 frame 0: "the AI that solves doctors' exam questions..."
    rect = phone(cr, 360, 1130, 840)
    chat(cr, rect, t, -1, wps=2.6)
    _pic(cr, "stethoscope", 850, 920, 330, t, T(tl, "b1", "डॉक्टर्स") - 0.2)
    card(cr, t, T(tl, "b1", "सवाल"), 690, 1250, ["EXAM QUESTIONS"], size=38)
    tick(cr, 940, 1390, 70, prog(t, T(tl, "b1", "सवाल") + 0.4, 0.3), color=GREEN)
    headline(cr, t, "IT PASSES DOCTOR EXAMS WITH", "0 ANSWERS INSIDE", -1, min(1.8, T(tl, "b1", "जवाब")),
             t_ghost=-1)


def o_numbers(cr, t, tl, t0):                            # b1 "...no book, no Google. Only numbers."
    tb, tg, tn = T(tl, "b1", "किताब"), T(tl, "b1", "गूगल"), T(tl, "b1", "नंबर्स")
    _pic(cr, "books", 230, 820, 260, t, tb - 0.3)
    cross(cr, 230, 820, 150, prog(t, tb + 0.2, 0.3))
    q = prog(t, tg - 0.3, 0.3)                           # a plain search bar (no logo)
    rrect(cr, 560, 770, 420, 100, 50)
    cr.set_source_rgba(1, 1, 1, q)
    cr.fill()
    draw_text(cr, "search...", 610, 820, 40, (0.5, 0.5, 0.5), q, MONO_FONT, "lm")
    cross(cr, 770, 820, 150, prog(t, tg + 0.2, 0.3))
    ai_box(cr, W / 2, 1300, 420, glow=prog(t, tn, 0.4))
    p = prog(t, tn - 0.1, 0.6)                           # the inside: nothing but numbers
    if p > 0:
        rng = random.Random(int(t * 12))
        for r in range(6):
            for c in range(7):
                draw_text(cr, f"{rng.uniform(-1, 1):+.2f}"[:4], W / 2 - 170 + c * 56, 1150 + r * 56, 26, GOLD,
                          p * (0.5 + 0.5 * rng.random()), MONO_FONT, "cm")
    headline(cr, t, "NO BOOK, NO GOOGLE...", "ONLY NUMBERS", t0, tn)


def o_onejob(cr, t, tl, t0):                             # b2 "and it does one thing: guess the next word"
    tg = T(tl, "b2", "गेस")
    sentence(cr, t, 70, 1000, ["THE", "HEART", "HAS", "FOUR"], 80, blank=("CHAMBERS", prog(t, tg + 0.4, 0.2)))
    ai_box(cr, W / 2, 1400, 200, glow=prog(t, tg, 0.4))
    headline(cr, t, "ITS ONLY JOB:", "THE NEXT WORD", t0, tg)


def k_keyboard(cr, t, tl, t0):                           # b2 "the same thing your phone's keyboard does..."
    keyboard(cr, 90, 860, 900, "Good morning, how are", ("you", "u", "things"),
             prog(t, T(tl, "b2", "कीबोर्ड") + 0.4, 0.3), prog(t, t0, 0.3))
    headline(cr, t, "LIKE YOUR PHONE'S", "KEYBOARD", t0, t0 + 0.3)


def k_giant(cr, t, tl, t0):                              # b2 "...just very, very big"
    s = 1 + 1.6 * prog(t, t0 + 0.2, 1.2)
    cr.save()
    cr.translate(W / 2, 1130)
    cr.scale(s, s)
    rrect(cr, -130, -45, 260, 90, 20)
    cr.set_source_rgba(*GOLD, 1)
    cr.fill()
    draw_text(cr, "you", 0, 0, 52, INK, 1, MONO_FONT, "cm")
    cr.restore()
    headline(cr, t, "SAME TRICK, JUST", "MUCH BIGGER", t0, t0 + 0.3)


def j_maths(cr, t, tl, t0):                              # b3 "it's not magic. it's maths."
    rrect(cr, 120, 820, 840, 560, 18)
    cr.set_source_rgba(0.16, 0.27, 0.21, prog(t, t0, 0.3))
    cr.fill()
    for i, eq in enumerate(("y = w1x1 + w2x2 + b", "P(next word) = ?", "loss = -log p")):
        draw_text(cr, eq, 180, 900 + 130 * i, 54, CREAM, prog(t, t0 + 0.3 + 0.3 * i, 0.3), MONO_FONT)
    stamp(cr, t, "NOT MAGIC", t0 + 0.2, W / 2, 1480, 70)
    headline(cr, t, "NOT MAGIC:", "MATHS", t0, T(tl, "b3", "गणित"))


def r_read(cr, t, tl, t0):                               # b4 "first it is made to read: books, articles, code..."
    ai_box(cr, W / 2, 1380, 220, glow=prog(t, t0 + 1.5, 0.6))
    items = (("books", "किताबें", 230), ("articles", "आर्टिकल्स", W / 2), ("code", "कोड", 850))
    for key, cue, x in items:
        tc = T(tl, "b4", cue)
        p, f = prog(t, tc - 0.2, 0.3), prog(t, tc + 0.6, 0.8)        # appear, then fly into the box
        xx, yy, a = x + (W / 2 - x) * f, 940 + 440 * f, p * (1 - f)
        if key == "books":
            _pic(cr, "books", xx, yy, 260 * (1 - 0.6 * f), t, tc - 0.2, alpha=1 - f)
        elif key == "articles":
            rrect(cr, xx - 110, yy - 140, 220, 280, 10)
            cr.set_source_rgba(*SCREEN, a)
            cr.fill()
            for k in range(7):
                cr.rectangle(xx - 85, yy - 110 + 34 * k, 170 - 40 * (k % 3), 12)
                cr.set_source_rgba(*INK, 0.5 * a)
                cr.fill()
        else:
            rrect(cr, xx - 120, yy - 110, 240, 220, 10)
            cr.set_source_rgba(*BODY, a)
            cr.fill()
            for k, ln in enumerate(("def f(x):", "  return x+1", "print(f(2))")):
                draw_text(cr, ln, xx - 100, yy - 80 + 50 * k, 26, (0.55, 0.85, 0.55), a, MONO_FONT)
    headline(cr, t, "FIRST, IT READS:", "TRILLIONS OF WORDS", t0, T(tl, "b4", "खरबों"))


def r_llama(cr, t, tl, t0):                              # b5 "Meta's AI, Llama 3, read so much..."
    card(cr, t, t0 + 0.1, 120, 800, ["META'S AI: LLAMA 3"], size=48)
    counter(cr, t, t0 + 0.5, W / 2, 1150, "15", 200, color=GOLD)
    draw_text(cr, "TRILLION WORD-PIECES", W / 2, 1300, 60, INK, prog(t, t0 + 0.8, 0.3), anchor="ct")
    headline(cr, t, "IT READ", "SO MUCH...", t0, t0 + 0.3)


def r_years(cr, t, tl, t0):                              # b5 "...a human reading 8 hours a day would need 2 lakh+ years"
    person(cr, 260, 1350, 420, INK, prog(t, t0, 0.3))
    rrect(cr, 300, 1010, 150, 110, 8)                   # the book in its hands
    cr.set_source_rgba(*RED, prog(t, t0 + 0.2, 0.3))
    cr.fill()
    card(cr, t, T(tl, "b5", "आठ"), 520, 900, ["8 HOURS A DAY"], size=44)
    counter(cr, t, T(tl, "b5", "लाख") - 0.2, 700, 1180, "2,00,000+", 82, color=GOLD)
    draw_text(cr, "YEARS", 700, 1260, 60, INK, prog(t, T(tl, "b5", "साल"), 0.3), anchor="ct")
    headline(cr, t, "ONE HUMAN WOULD NEED", "2 LAKH+ YEARS", t0, T(tl, "b5", "लाख"))


def g_game(cr, t, tl, t0):                               # b6 "how does it read? by a game: hide the last word..."
    sentence(cr, t, 70, 1000, ["NO", "SUGAR,", "SO", "THE", "CHAI", "IS"], 70,
             blank=("", 0.0) if t >= T(tl, "b6", "छिपा") else None)
    ai_box(cr, W / 2, 1400, 180)
    q = prog(t, T(tl, "b6", "गेस"), 0.3)
    draw_text(cr, "GUESS!", W / 2, 1600, 70, RED, q, anchor="cm")
    headline(cr, t, "HOW DOES IT LEARN?", "A GAME", t0, T(tl, "b6", "खेल"))


def g_chai(cr, t, tl, t0):                               # b7 "...the AI says: sweet? Wrong."
    _pic(cr, "chai", 300, 1150, 520, t, t0)
    tm = T(tl, "b7", "मीठी")
    card(cr, t, tm, 600, 980, ["MEETHI?", "(SWEET)"], size=60)
    cross(cr, 980, 1020, 110, prog(t, tm + 0.6, 0.3))
    headline(cr, t, "AI'S GUESS:", "WRONG", t0, tm + 0.6)


def g_right(cr, t, tl, t0):                              # b7 "...right answer: pheeki"
    _pic(cr, "chai", 300, 1150, 520, t, t0 - 1)
    card(cr, t, t0 + 0.1, 600, 980, ["PHEEKI", "(NOT SWEET)"], size=60)
    tick(cr, 990, 1020, 110, prog(t, T(tl, "b7", "फीकी"), 0.3), color=GREEN)
    headline(cr, t, "RIGHT ANSWER:", "PHEEKI", t0, T(tl, "b7", "फीकी"), big_color=GREEN)


def n_knobs(cr, t, tl, t0):                              # b8 "every mistake: billions of tiny knobs turned a little"
    knob_wall(cr, t, t0, 150, 820, 7, 7, 130, 46, turning=(3, 10, 16, 24, 31, 38, 45))
    headline(cr, t, "EVERY MISTAKE:", "TURN THE KNOBS", t0, T(tl, "b8", "नॉब्स"))


def n_regulator(cr, t, tl, t0):                          # b8 "...like a fan regulator..."
    a = -2.2 + 1.1 * (1.2 + 0.8 * prog(t, t0 + 0.3, 1.2))
    knob(cr, W / 2, 1150, 230, a, numbers=True)
    headline(cr, t, "LIKE A FAN", "REGULATOR", t0, t0 + 0.3)


def n_better(cr, t, tl, t0):                             # b8 "...so the next guess is a little better"
    gauge(cr, t, t0 + 0.1, W / 2, 1250, 300, 0.35, 0.55, labels=("BAD GUESS", "GOOD GUESS"))
    headline(cr, t, "NEXT GUESS:", "A BIT BETTER", t0, t0 + 0.4, big_color=GREEN)


def n_175(cr, t, tl, t0):                                # b9 "GPT-3 had 175 billion such knobs"
    knob_wall(cr, t, t0 - 2, 150, 820, 7, 7, 130, 46, alpha=0.25)
    counter(cr, t, t0 + 0.2, W / 2, 1120, "175", 230, color=GOLD)
    draw_text(cr, "BILLION KNOBS", W / 2, 1290, 80, INK, prog(t, t0 + 0.6, 0.3), anchor="ct")
    headline(cr, t, "GPT-3 HAD", "175 BILLION", t0, T(tl, "b9", "पचहत्तर"))


def d_repeat(cr, t, tl, t0):                             # b10 "this game is played trillions of times"
    for i in range(12):
        q = prog(t, t0 + 0.1 * i, 0.25)
        x, y = 180 + (i % 4) * 240, 880 + (i // 4) * 220
        rrect(cr, x - 100, y - 60, 200, 120, 12)
        cr.set_source_rgba(*SCREEN, q)
        cr.fill()
        draw_text(cr, "? ->", x, y, 44, INK, q, MONO_FONT, "cm")
    headline(cr, t, "PLAYED", "TRILLIONS OF TIMES", t0, T(tl, "b10", "खरबों"))


def d_servers(cr, t, tl, t0):                            # b10 "...for weeks and months, on thousands of computers"
    _pic(cr, "servers", W / 2, 1010, 0, t, t0, frame=(860, 500))
    calendar(cr, t, t0 + 0.3, 800, 1470, ["WEEK 1", "WEEK 6", "MONTH 3", "MONTH 4"], "TRAINING", interval=0.35,
             w=280, h=290)
    headline(cr, t, "FOR MONTHS, ON", "1000s OF COMPUTERS", t0, t0 + 0.3)


def q_rehook(cr, t, tl, t0):                             # b11 re-hook: "if it only guesses, how is it so smart?" (slate)
    q = prog(t, t0 + 0.2, 0.3)
    draw_text(cr, "?", W / 2, 1150, 520 * (0.8 + 0.2 * q), CORAL, q, anchor="cm")
    headline(cr, t, "IF IT ONLY GUESSES...", "WHY SO SMART?", t0, T(tl, "b11", "समझदार"), small_color=CREAM,
             big_color=CORAL)


def w_world(cr, t, tl, t0):                              # b12 "to guess right, it must learn how the world works"
    _pic(cr, "earth_globe", W / 2, 1150, 560, t, t0)
    headline(cr, t, "TO GUESS WELL, IT LEARNS", "HOW THE WORLD WORKS", t0, T(tl, "b12", "दुनिया"))


def w_cards(cr, t, tl, t0):                              # b12 "...grammar, facts, even logic"
    tg = T(tl, "b12", "ग्रामर")
    for i, (lab, at) in enumerate((("GRAMMAR", tg), ("FACTS", tg + 0.7), ("LOGIC", T(tl, "b12", "लॉजिक")))):
        card(cr, t, at, 140 + 70 * i, 860 + 230 * i, [lab], size=80)
    headline(cr, t, "GRAMMAR, FACTS,", "EVEN LOGIC", t0, T(tl, "b12", "लॉजिक"))


def p_pick(cr, t, tl, t0):                               # b13 "when you ask, it picks one word..."
    tc = T(tl, "b13", "चुनता")
    sentence(cr, t, 70, 840, ["THE", "SKY", "IS"], 80, blank=("BLUE", prog(t, tc + 0.5, 0.2)))
    candidates(cr, t, t0 + 0.2, 160, 1120, (("BLUE", 72), ("CLEAR", 15), ("FALLING", 2)), chosen_at=tc)
    headline(cr, t, "IT PICKS", "ONE WORD", t0, tc)


def p_next(cr, t, tl, t0):                               # b13 "...then the next... then the next, till the answer is done"
    words = ["THE", "SKY", "IS", "BLUE", "TODAY"]
    k = 4 + int(prog(t, t0 + 1.2, 0.01))
    sentence(cr, t, 70, 840, words[:k], 80, blank=("TODAY", 0.0) if k == 4 else None)
    if k == 4:
        candidates(cr, t, t0 + 0.1, 160, 1120, (("TODAY", 41), ("AND", 22), ("BECAUSE", 9)), chosen_at=t0 + 0.8)
    else:
        draw_text(cr, "...ONE WORD AT A TIME", W / 2, 1200, 64, RED, prog(t, t0 + 1.3, 0.3), anchor="ct")
    headline(cr, t, "THEN THE NEXT...", "AND THE NEXT", t0, t0 + 0.3)


def t_typing(cr, t, tl, t0):                             # b14 "that's why the answer looks like it's being typed"
    rect = phone(cr, W / 2, 1150, 900)
    chat(cr, rect, t, t0 + 0.2, wps=3.0)
    headline(cr, t, "THAT'S WHY IT", "TYPES", t0, T(tl, "b14", "टाइप"))


def l_dice(cr, t, tl, t0):                               # b15 "and every time, a little luck"
    for i, (x, v) in enumerate(((380, 3), (700, 5))):
        p = prog(t, t0 + 0.1 * i, 0.8)
        dice(cr, x, 1150 - 260 * math.sin(math.pi * p) * (1 - p), 230, v if p >= 1 else (int(t * 12) + i) % 6 + 1,
             rot=(1 - p) * 4 + 0.15 * (i - 0.5))
    headline(cr, t, "EVERY WORD:", "A LITTLE LUCK", t0, T(tl, "b15", "किस्मत"))


def l_two(cr, t, tl, t0):                                # b15 "...same question twice, a slightly different answer"
    for i, (x, ans) in enumerate(((290, ANSWER), (790, "Your heart has 4 chambers: 2 atria on top and 2 "
                                                             "ventricles below."))):
        rect = phone(cr, x, 1150, 820, prog(t, t0 + 0.2 * i, 0.3))
        chat(cr, rect, t, t0 + 0.4 + 0.2 * i, wps=5.0, answer=ans, alpha=prog(t, t0 + 0.2 * i, 0.3))
    headline(cr, t, "SAME QUESTION,", "DIFFERENT ANSWER", t0, T(tl, "b15", "अलग"))


def s_scale(cr, t, tl, t0):                              # b16 "its weakness: it picks what sounds right, not what's true"
    tilt = 0.18 * prog(t, T(tl, "b16", "सही") - 0.3, 0.8)
    balance(cr, W / 2, 900, 640, tilt, "SOUNDS RIGHT", "IS TRUE", prog(t, t0, 0.3))
    headline(cr, t, "ITS WEAKNESS: IT PICKS", "WHAT SOUNDS RIGHT", t0, T(tl, "b16", "सही"))


def h_wrong(cr, t, tl, t0):                              # b17 "so sometimes it says wrong things with full confidence"
    rect = phone(cr, W / 2, 1150, 900)
    sx, sy, sw, sh = rect
    hq = bubble(cr, sx + sw - 24, sy + 60, sw * 0.82, "Can you see the Great Wall of China from the Moon?", fill=ME,
                right=True)
    bubble(cr, sx + 24, sy + 90 + hq, sw * 0.86, "Yes! It is the only human-made thing visible from the Moon.",
           n=(t - t0 - 0.2) * 4)
    cross(cr, W / 2 + 160, 1360, 170, prog(t, t0 + 1.8, 0.3))
    footnote(cr, "the right answer: no, it can't be seen from the Moon", prog(t, t0 + 2.0, 0.3))
    headline(cr, t, "FULL CONFIDENCE,", "WRONG ANSWER", t0, t0 + 1.8)


def h_name(cr, t, tl, t0):                               # b17 "...this is called hallucination"
    stamp(cr, t, "CONFIDENT. WRONG.", t0 + 0.5, W / 2, 1200, 80)
    headline(cr, t, "IT'S CALLED", "HALLUCINATION", t0, T(tl, "b17", "हैलुसिनेशन"))


def z_machine(cr, t, tl, t0):                            # b18 "socho: a machine that only guesses the next word..."
    ai_box(cr, W / 2, 1150, 300, glow=0.5 + 0.5 * math.sin(t * 3))
    headline(cr, t, "IT ONLY GUESSES", "THE NEXT WORD...", t0, t0 + 0.3)


def z_does(cr, t, tl, t0):                               # b18 "...and yet writes poems, code, solves exam questions"
    for i, (lab, cue) in enumerate((("POEMS", "कविता"), ("CODE", "कोड"), ("EXAM ANSWERS", "सवाल"))):
        card(cr, t, T(tl, "b18", cue), 140 + 60 * i, 860 + 230 * i, [lab], size=80)
    headline(cr, t, "...YET IT WRITES", "POEMS AND CODE", t0, T(tl, "b18", "कविता"))


def e_question(cr, t, tl, t0):                           # b19 "does AI really understand, or just guess very well?"
    for i, (lab, x) in enumerate((("UNDERSTANDS", 290), ("JUST GUESSES", 790))):
        card(cr, t, t0 + 0.3 + 0.3 * i, x - 200, 1000, [lab], size=48)
    draw_text(cr, "COMMENT BELOW", W / 2, 1300, 44, INK, prog(t, T(tl, "b19", "कमेंट"), 0.3), MONO_FONT, "ct")
    ai_box(cr, W / 2, 1520, 160)
    headline(cr, t, "DOES AI UNDERSTAND,", "OR JUST GUESS?", t0, T(tl, "b19", "समझता"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_phone, "paper"), ("b1", "कोई", o_numbers, "paper"),
    ("b2", None, o_onejob, "paper"), ("b2", "वही", k_keyboard, "paper"), ("b2", "बहुत", k_giant, "paper"),
    ("b3", None, j_maths, "paper"),
    ("b4", None, r_read, "paper"),
    ("b5", None, r_llama, "paper"), ("b5", "इंसान", r_years, "paper"),
    ("b6", None, g_game, "paper"),
    ("b7", None, g_chai, "paper"), ("b7", "सही", g_right, "paper"),
    ("b8", None, n_knobs, "paper"), ("b8", "जैसे", n_regulator, "paper"), ("b8", "ताकि", n_better, "paper"),
    ("b9", None, n_175, "paper"),
    ("b10", None, d_repeat, "paper"), ("b10", "महीनों", d_servers, "paper"),
    ("b11", None, q_rehook, "slate"),
    ("b12", None, w_world, "paper"), ("b12", "ग्रामर", w_cards, "paper"),
    ("b13", None, p_pick, "paper"), ("b13", "फिर", p_next, "paper"),
    ("b14", None, t_typing, "paper"),
    ("b15", None, l_dice, "paper"), ("b15", "इसलिए", l_two, "paper"),
    ("b16", None, s_scale, "paper"),
    ("b17", None, h_wrong, "paper"), ("b17", "इसे", h_name, "paper"),
    ("b18", None, z_machine, "paper"), ("b18", "कविता", z_does, "paper"),
    ("b19", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on the wrong guess and the stamps, ticks (and music dips) before the re-hook, the
    weakness and the closing line, typing on the chat."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b7", "मीठी") + 0.6, "thud", 0.0), (T(tl, "b3", None) + 0.2, "thud", 0.0),
           (T(tl, "b11", None) - 0.35, "tick", 0.0), (T(tl, "b16", None) - 0.35, "tick", 0.0),
           (T(tl, "b19", None) - 0.35, "tick", 0.0), (T(tl, "b1", None), "typing", 2.0),
           (T(tl, "b14", None) + 0.2, "typing", 2.0)]
    for bid in ("b4", "b9", "b12"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
