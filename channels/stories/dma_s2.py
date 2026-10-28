"""DEAD MAN'S ALGORITHM, Short 2: "The Glass Auction" (9:16). Chapter 1 beats 11-12: the first game begins and the
students face its countdown. Auto-approved by the owner, 27 Oct 2026.

Momo reads the five rules exactly as the bible fixes them (20 players, 100 tokens each, 10 minutes, the exit key).
The students reason from those rules only: Riku claims 100, Aoi points out a tie at the top eliminates everyone tied
(rule 3), Kota points out all-zero executes everyone (rule 5), Mio sees that whoever bids will be watched. Ren sees that
100 may not be the safest number. Nothing is resolved (the open rule questions are the owner's to answer); it ends on
the hook into Part 3: Ren already knows his number, and Momo's "Tick tock".

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s2   -> out/stories/dma_s2.mp4
"""
import math
import os

from motion import audio, satsuei, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import dma_anime, dma_art, serial

A = dma_art if os.environ.get("ANIME") == "0" else dma_anime     # ANIME=0: the old vector look (for comparisons)

NARRATOR = dict(turbo=True, turbo_ref="am_echo")
TAIL = 2.0
MUSIC = "horror"
TWIST = "g17"
voice.SPEAKERS.update({
    "haruto": dict(voice="am_puck", turbo_ref="am_puck"),
    "riku": dict(voice="am_fenrir", turbo_ref="am_fenrir"),
    "kota": dict(voice="am_eric", turbo_ref="am_eric+1"),
    "aoi": dict(voice="af_kore", turbo_ref="af_kore"),
    "mio": dict(voice="af_bella", turbo_ref="af_bella"),
    "momo": dict(voice="af_sky", turbo_ref="af_sky+5"),
})
audio.GAINS.update(chime=0.7, click=0.6, sting=0.55)

SCRIPT = [
    dict(id="g1", scene="hook", text="Momo gave each of us a hundred tokens. And ten minutes."),
    dict(id="g2", scene="momo", text="Game one! The Glass Auction! Win the exit key!", speaker="momo", gap=0.5),
    dict(id="g3", scene="rule", text="Rule one. The highest unique bid wins the key.", speaker="momo"),
    dict(id="g4", scene="rule", text="Rule two. All spent tokens are permanently lost.", speaker="momo"),
    dict(id="g5", scene="rule", text="Rule three. If multiple players submit the same highest bid, every player "
                                     "tied at that amount is eliminated.", speaker="momo"),
    dict(id="g6", scene="rule", text="Rule four. If the highest bid is tied, the next highest unique bid wins.",
         speaker="momo"),
    dict(id="g7", scene="rule", text="Rule five. If everyone leaves all tokens unspent when time expires, "
                                     "everyone is executed!", speaker="momo"),
    dict(id="g8", scene="momo", text="Ten minutes! Starting now!", speaker="momo", gap=0.6),
    dict(id="g9", scene="talk", text="Easy. I bid all hundred. Nobody beats a hundred.", speaker="riku", gap=0.6),
    dict(id="g10", scene="talk", text="Unless someone else bids a hundred. Then you're both eliminated.",
         speaker="aoi", gap=0.4),
    dict(id="g11", scene="talk", text="So we all bid zero and go home?", speaker="haruto", gap=0.5),
    dict(id="g12", scene="talk", text="Then rule five executes all of us.", speaker="kota", gap=0.4),
    dict(id="g13", scene="talk", text="So somebody has to bid. And everyone will remember who.", speaker="mio",
         gap=0.5),
    dict(id="g14", scene="ren", text="Everyone was doing the same math."),
    dict(id="g15", scene="ren", text="Bid too high, and you might tie. Bid too low, and someone beats you."),
    dict(id="g16", scene="clock", text="The countdown said [nine twelve.|9:12.]"),
    dict(id="g17", scene="ren", text="And I realised the safest number in this room might not be a hundred.",
         gap=0.6),
    dict(id="g18", scene="ren", text="I already knew my number.", gap=0.5),
    dict(id="g19", scene="momo_close", text="Tick tock, Class [three B!|3-B!]", speaker="momo", gap=0.3),
]

METADATA = dict(
    title="100 Tokens. 10 Minutes. One Key. How Much Would You Bid? 🔑",
    alt_titles=["The Highest UNIQUE Bid Wins. Ties Are Eliminated. 🔑", "Dead Man's Algorithm, Part 2: The Glass "
                                                                         "Auction 🔑"],
    description="""Twenty students. A hundred tokens each. Ten minutes. One exit key. 🔑

The highest UNIQUE bid wins. Tie at the top and you're eliminated. Spend nothing at all and everyone is executed.

Dead Man's Algorithm, Part 2: The Glass Auction.
Ren already knows his number. Do you? Part 3 is next.

(Original story. Anime-style animation.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "game theory", "death game", "psychological thriller", "puzzle",
          "anime story", "auction", "2d animation", "part 2"],
    pinned_comment="I'd bid 1. Everyone scared of ties goes high, and a hundred is where the ties are. Am I wrong? "
                   "What's your number? 👇",
)

KEY = {"hundred", "tokens", "ten", "minutes", "key", "unique", "lost", "forever", "tied", "eliminated", "next",
       "executed", "zero", "five", "somebody", "remember", "math", "high", "low", "tie", "beats", "safest", "bid"}
RULES = [r.upper() for r in (                              # the bible's wording, word for word
    "The highest unique bid wins the key.",
    "All spent tokens are permanently lost.",
    "If multiple players submit the same highest bid, every player tied at that amount is eliminated.",
    "If the highest bid is tied, the next-highest unique bid wins.",
    "If everyone leaves all tokens unspent when time expires, everyone is executed.")]
CYAN = (0.55, 1, 0.85, 1)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def countdown(t, tl):
    """In-world time left: 10:00 when Momo says "now", 9:12 when Ren reads it (the narration compresses time)."""
    B = tl.by_id
    t0, t1 = tl.at("g8", "now!", end=True), B["g16"].start + 0.3
    if t < t0:
        return 600.0
    return max(0.0, 600 - (t - t0) * (48.0 / max(1.0, t1 - t0)))


def fmt(sec):
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def room(cr, t, left, screen_lines=None, momo_at=None):
    """The chamber with the glass case risen in the middle and the big countdown on the screen."""
    lines = screen_lines or ["GAME 01", "THE GLASS AUCTION", fmt(left)]
    A.chamber(cr, t, screen=A.screen_text(lines, col=CYAN, momo_at=momo_at, t=t))
    A.glass_case(cr, t, W / 2, H * 0.62, 0.9)


def rule_card(cr, t, start, end, n, text):
    """RULE n, slammed on screen, one line at a time."""
    if t < start or t > end + 0.25:
        return
    p = clamp01((t - start) / 0.15)
    a = 1 - clamp01((t - end) / 0.25)
    cr.save()
    cr.push_group()
    y = H * 0.5
    s = 1.25 - 0.25 * p
    cr.translate(W / 2, y)
    cr.scale(s, s)
    w = W * 0.86
    A.tk.tk_rrect(cr, -w / 2, -150, w, 300, 18)
    cr.set_source_rgba(0.03, 0.05, 0.06, 0.93)
    cr.fill_preserve()
    cr.set_source_rgba(*CYAN[:3], 0.9)
    cr.set_line_width(4)
    cr.stroke()
    hud2d._text(cr, f"RULE {n}", 0, -82, 46, hud2d.RED, hud2d.ROUND, "center")
    words, lines, cur = text.split(), [], ""
    for wd in words:
        nxt = (cur + " " + wd).strip()
        if cur and A.text_width(cr, nxt, 34, "Liberation Mono") > w - 60:
            lines.append(cur)
            cur = wd
        else:
            cur = nxt
    lines.append(cur)
    for j, ln in enumerate(lines):
        hud2d._text(cr, ln, 0, -10 + j * 46, 34, CYAN, "Liberation Mono", "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def rules_strip(cr, t, shown, hot=None):
    """Small chips R1..R5 under the status bar once each is read; the one in play turns red."""
    x = 18
    for n in range(1, shown + 1):
        txt = f"R{n}"
        w = 64
        A.tk.tk_rrect(cr, x, 66, w, 36, 18)
        cr.set_source_rgba(*(hud2d.RED[:3] if hot == n else (0.04, 0.06, 0.07)), 0.92)
        cr.fill_preserve()
        cr.set_source_rgba(*CYAN[:3], 0.6)
        cr.set_line_width(2)
        cr.stroke()
        hud2d._text(cr, txt, x + w / 2, 91, 22, (1, 1, 1, 1), hud2d.ROUND, "center")
        x += w + 8


def numbers(cr, t, k):
    """The numbers in Ren's head: 100? 99? 50? 1?, drifting."""
    if k <= 0:
        return
    for j, (n, x, y) in enumerate((("100?", 0.2, 0.3), ("99?", 0.78, 0.26), ("50?", 0.16, 0.5), ("1?", 0.82, 0.48),
                                   ("0?", 0.5, 0.2))):
        a = k * (0.55 + 0.25 * math.sin(t * 2 + j))
        hud2d._text(cr, n, W * x, H * y + 10 * math.sin(t * 1.5 + j), 54, (*CYAN[:3], a), "Liberation Mono",
                    "center")


# ------------------------------------------------------------------ the film
def shots(tl):
    A_, B = tl.at, tl.by_id
    return [
        (0.0, "hook"), (B["g2"].start - 0.15, "momo"), (B["g3"].start - 0.1, "r1"), (B["g4"].start - 0.1, "r2"),
        (B["g5"].start - 0.1, "r3"), (B["g6"].start - 0.1, "r4"), (B["g7"].start - 0.1, "r5"),
        (B["g8"].start - 0.1, "go"), (B["g9"].start - 0.15, "riku"), (B["g10"].start - 0.15, "aoi"),
        (B["g11"].start - 0.15, "haruto"), (B["g12"].start - 0.15, "kota"), (B["g13"].start - 0.15, "mio"),
        (B["g14"].start - 0.15, "ren_math"), (B["g16"].start - 0.15, "clock"), (B["g17"].start - 0.15, "ren_eyes"),
        (B["g19"].start - 0.1, "momo_close"), (tl.total + 1, "end")]


_shots = {}
REACT = {"r1": ("riku", "smirk"), "r2": ("kota", "worry"), "r3": ("aoi", "focus"), "r4": ("haruto", "worry"),
         "r5": ("yui", "fear")}


def draw(cr, t, tl):
    A_, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    left = countdown(t, tl)
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    by = 940

    cr.save()
    if name == "hook":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=720)
        hud2d.blurred(cr, lambda c: room(c, t, 600), sigma=8)
        A.student_bust(cr, W / 2, by + (140 if A is dma_art else -10), 1.15, t, "ren", "focus", look=(0, 0.5),
                       rim=(0.5, 1, 0.9, 0.6), rim_from=(0, 10))
        A.terminal(cr, t, W / 2, 1090, 0.75, tokens=100)
        glow(cr, W / 2, 1000, 400, (0.4, 1, 0.9), 0.2)
    elif name in ("momo", "go"):
        camera(cr, t, s0, s1, 1.0, 1.06, cy=480)
        lines = (["GAME 01", "THE GLASS AUCTION"] if name == "momo" else ["TIME LEFT", fmt(left)])
        room(cr, t, left, lines, momo_at=1.0 if name == "momo" else None)
        for j, who in enumerate(("mio", "haruto", "ren", "yui", "aoi")):
            A.student_bust(cr, 80 + j * 140, 1260, 0.6, t, who, "worry", look=(0, -0.8))
    elif name in REACT:
        camera(cr, t, s0, s1, 1.02, 1.08, cy=700)
        hud2d.blurred(cr, lambda c: room(c, t, left), sigma=8)
        who, e = REACT[name]
        A.student_bust(cr, W / 2, by + 40, 1.15, t, who, e, look=(0, -0.3))
    elif name in ("riku", "aoi", "haruto", "kota", "mio"):
        camera(cr, t, s0, s1, 1.02, 1.1, cy=700, shake=1.3 if name == "riku" else 1.0)
        hud2d.blurred(cr, lambda c: room(c, t, left), sigma=9)
        e = {"riku": "smirk" if t < B["g10"].start else "worry", "aoi": "focus", "haruto": "grin", "kota": "fear",
             "mio": "calm"}[name]
        if name == "riku" or name == "aoi":                    # the two of them: Riku hears it land
            if name == "aoi":
                A.student_bust(cr, 170, by + 150, 0.75, t, "riku", "worry", look=(0.6, -0.1), sweat=0.6)
            A.student_bust(cr, W / 2 + (60 if name == "aoi" else 0), by, 1.15, t, name, e,
                           look=(-0.4, 0) if name == "aoi" else (0.2, 0), talk=talk(name))
        else:
            A.student_bust(cr, W / 2, by, 1.2, t, name, e, look=(0.3, 0.1), talk=talk(name),
                           sweat=0.8 if name == "kota" else 0.0, tremble=0.6 if name == "kota" else 0.0)
    elif name in ("ren_math", "ren_eyes"):
        camera(cr, t, s0, s1, 1.03, 1.14 if name == "ren_eyes" else 1.08, cy=700)
        hud2d.blurred(cr, lambda c: room(c, t, left), sigma=10)
        cr.set_source_rgba(0, 0.02, 0.03, 0.35)
        cr.paint()
        A.student_bust(cr, W / 2, by, 1.25 if name == "ren_math" else 1.5, t, "ren", "focus", look=(-0.3, -0.1),
                       rim=(0.5, 1, 0.9, 0.6), rim_from=(10, -6))
        numbers(cr, t, 1.0 if name == "ren_math" else 0.3)
    elif name == "clock":
        camera(cr, t, s0, s1, 1.0, 1.12, cy=420, shake=0.6)
        room(cr, t, left, ["TIME LEFT", fmt(left)])
    elif name == "momo_close":
        camera(cr, t, s0, s1, 1.0, 1.15, cy=700)
        hud2d.blurred(cr, lambda c: room(c, t, left), sigma=10)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
        A.momo(cr, W / 2, 1180, 3.6 + 0.5 * seg(t, s0, s0 + 0.8), t, mood="wink", lean=0.1 * seg(t, s0, s0 + 0.8))
    cr.restore()

    if A is dma_anime:                                          # satsuei: glow, cold light, aberration, grain
        satsuei.apply(cr, t, glow=0.24, light=((0.5, 0.0), (0.7, 0.85, 1.0), 0.14),
                      shade=((0.5, 0.3), (0.35, 0.3, 0.45), 0.35), ca=1.2, grain=0.03)
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.0)
    else:
        hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.06)
    for n, gid in enumerate(("g3", "g4", "g5", "g6", "g7"), 1):
        rule_card(cr, t, B[gid].start + 0.05, B[gid].end + 0.1, n, RULES[n - 1])
    shown = sum(t >= B[g].end for g in ("g3", "g4", "g5", "g6", "g7"))
    hot = 3 if B["g10"].start <= t <= B["g10"].end + 0.3 else 5 if B["g12"].start <= t <= B["g12"].end + 0.3 else \
        1 if B["g9"].start <= t <= B["g9"].end else None
    if t < B["g19"].start:
        rules_strip(cr, t, shown, hot)
    alert = t >= A_("g8", "now!", end=True)
    A.status_bar(cr, t, "GAME 01 · THE GLASS AUCTION" if alert else "GAME 01", fmt(left) if alert else "20 PLAYERS · 100 TOKENS",
                 alert=alert)
    hud2d.hook(cr, t, [("100 TOKENS. 10 MINUTES.", False), ("ONE KEY.", True)], end=B["g1"].end + 0.1, y=230,
               size=72)
    for who, a, b in (("riku", B["g9"].start, B["g9"].end), ("aoi", B["g10"].start, B["g10"].end),
                      ("haruto", B["g11"].start, B["g11"].end), ("kota", B["g12"].start, B["g12"].end),
                      ("mio", B["g13"].start, B["g13"].end)):
        A.name_card(cr, t, a, b, who, y=1150)
    if t < B["g19"].end + 0.1 and not any(B[g].start - 0.05 <= t <= B[g].end + 0.1 for g in ("g3", "g4", "g5", "g6",
                                                                                          "g7")):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, B["g19"].end + 0.1, "DEAD MAN'S ALGORITHM", "PART 3", "THE BIDS")
    cue("hum", t, 0.0, tl.total)
    cue("chime", t, B["g2"].start - 0.45)
    for g in ("g3", "g4", "g5", "g6", "g7"):
        cue("click", t, B[g].start - 0.12)
    cue("sting", t, A_("g8", "now!", end=True) + 0.05)
    cue("heartbeat", t, B["g14"].start, B["g17"].end - B["g14"].start)
    cue("riser", t, B["g17"].start, B["g18"].start - B["g17"].start)
