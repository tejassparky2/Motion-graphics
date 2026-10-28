"""DEAD MAN'S ALGORITHM, Part 3: "The Bids" (9:16). Game 1 resolved (approved script, owner 28 Oct 2026:
channels/stories/dma_arc_games_1_2.md v4). Ren's number is one: one bid of one token, everyone else zero, and a plan
built so a liar wins the key without killing anyone. Riku's "nobody beats a hundred" was a bluff; he wins with thirty.
Twenty survive; Riku now has the fewest tokens.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s3   -> out/stories/dma_s3.mp4
"""
import math
import os

from motion import audio, satsuei, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import glow, noise
from channels.stories import dma_anime, dma_art, dma_kit as K, serial

A = dma_art if os.environ.get("ANIME") == "0" else dma_anime     # ANIME=0: the old vector look (for comparisons)
K.use(A)

NARRATOR = dict(turbo=True, turbo_ref="am_echo")                # Ren tells it
TAIL = 2.0
MUSIC = "horror"
voice.SPEAKERS.update(K.SPEAKERS)
audio.GAINS.update(chime=0.7, click=0.6, sting=0.55)
TWIST = "t12"

SCRIPT = [
    dict(id="t1", scene="hook", text="My number was one."),
    dict(id="t2", scene="r5", text="Somebody had to spend. Or rule five killed us all."),
    dict(id="t3", scene="r3", text="But two bids at the top would tie. And a tie at the top kills."),
    dict(id="t4", scene="r2", text="So only one person could bid. And spent tokens are gone permanently. "
                                   "So it had to be tiny."),
    dict(id="t5", scene="ren", text="Mio was right. Everyone would remember who. So it had to be me."),
    dict(id="t6", scene="plan", text="I bid one. Everyone else bids zero.", speaker="ren", gap=0.5),
    dict(id="t7", scene="mio", text="And if somebody lies?", speaker="mio", gap=0.4),
    dict(id="t8", scene="liar", text="Then let them. Bid more than one, and you win the key. And nobody dies.",
         speaker="ren", gap=0.4),
    dict(id="t9", scene="liar", text="Just never bid a hundred. Riku already called it.", speaker="ren"),
    dict(id="t10", scene="riku", text="Fine. Ren bids one.", speaker="riku", gap=0.5),
    dict(id="t11", scene="eyes", text="Riku agreed too fast.", gap=0.4),
    dict(id="t12", scene="result", text="Time's up! Highest unique bid: thirty! Kanzaki Riku!", speaker="momo",
         gap=0.7),
    dict(id="t13", scene="bluff", text="Riku never meant a hundred. He said it so nobody would dare bid high."),
    dict(id="t14", scene="key", text="You trusted a plan. I trusted a number.", speaker="riku", gap=0.4),
    dict(id="t15", scene="ren2", text="He thought he beat my plan. My plan was built for a liar.", gap=0.4),
    dict(id="t16", scene="survivors", text="No tie. Nobody died. Twenty survivors."),
    dict(id="t17", scene="momo", text="Everybody lives! How boring!", speaker="momo", gap=0.4),
    dict(id="t18", scene="door", text="The exit key opened the exit. Into game two.", gap=0.5),
    dict(id="t19", scene="end", text="And Riku had just spent thirty tokens. Fewer than anyone.", gap=0.4),
]

METADATA = dict(
    title="Twenty Students. One Bid of ONE Token. And One Liar. 🔑",
    alt_titles=["How Do 20 People Survive This Auction? 🔑", "Dead Man's Algorithm, Part 3: The Bids 🔑"],
    description="""Rule five kills everyone if nobody spends. Rule three kills a tie at the top.
So Ren's plan: one bid of one token. Everyone else bids zero.
And if someone lies? Let them. A liar wins the key, and nobody dies.

Dead Man's Algorithm, Part 3: The Bids.
Riku won with thirty. Now he has fewer tokens than anyone. Part 4 is next.

(Original story. Anime-style animation.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "game theory", "death game", "psychological thriller", "puzzle",
          "anime story", "auction", "loophole", "part 3"],
    pinned_comment="Ren's plan let a liar win without killing anyone. Riku took the key for thirty. "
                   "Smart move, or did he just put a target on himself? 👇",
)

KEY = {"one", "spend", "five", "tie", "kills", "permanently", "tiny", "me", "zero", "lies", "nobody", "hundred",
       "fast", "thirty", "bluff", "liar", "survivors", "boring", "game", "fewer", "number", "plan"}


# ------------------------------------------------------------------ the film
RULE = {2: "All spent tokens are permanently lost.",               # the bible's wording, word for word
        3: "If multiple players submit the same highest bid, every player tied at that amount is eliminated.",
        5: "If everyone leaves all tokens unspent when time expires, everyone is executed."}
PLAN = [("t1", "hook"), ("t2", "r5"), ("t3", "r3"), ("t4", "r2"), ("t5", "ren"), ("t6", "plan"), ("t7", "mio"),
        ("t8", "liar"), ("t10", "riku"), ("t11", "eyes"), ("t12", "result"), ("t13", "bluff"), ("t14", "key"),
        ("t15", "ren2"), ("t16", "survivors"), ("t17", "momo"), ("t18", "door"), ("t19", "end")]
_sh = {}


def left(t, tl):
    """In-world time left: 9:12 (where Part 2 stopped) running out exactly as Momo calls time."""
    t0, t1 = 0.0, tl.by_id["t12"].start
    return max(0.0, 552 - 552 * clamp01((t - t0) / max(1.0, t1 - t0)))


def bust(cr, t, s0, s1, bg, who, expr, talk=0.0, z=(1.02, 1.1), scale=1.2, sigma=9, **kw):
    K.camera(cr, t, s0, s1, *z, cy=700)
    hud2d.blurred(cr, bg, sigma=sigma)
    A.student_bust(cr, W / 2, K.BY, scale, t, who, expr, talk=talk, **kw)


def collide(cr, t, start, end):
    """Two bids of 100 sliding together; at contact, a red X: both eliminated."""
    if not (start <= t <= end + 0.2):
        return
    p = clamp01((t - start) / 0.9)
    y = H * 0.62
    for sx in (-1, 1):
        x = W / 2 + sx * (260 - 150 * p)
        K.token(cr, x, y, 96)
        hud2d._text(cr, "100", x, y + 26, 64, (0.3, 0.2, 0.02, 1), hud2d.ROUND, "center")
    if p >= 1:
        cr.set_source_rgba(*K.RED[:3], 0.95)
        cr.set_line_width(22)
        for a, b in ((-1, 1), (1, 1)):
            cr.move_to(W / 2 - 140 * a, y - 140)
            cr.line_to(W / 2 + 140 * a, y + 140)
        cr.stroke()


def draw(cr, t, tl):
    B = tl.by_id
    if id(tl) not in _sh:
        _sh[id(tl)] = K.shot_index(tl, PLAN)
    s0, name, s1 = K.current(_sh[id(tl)], t)
    tleft = left(t, tl)
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    room = lambda c: K.chamber(c, t, ["GAME 01", "TIME LEFT", K.fmt(tleft)])

    cr.save()
    if name == "hook":
        K.camera(cr, t, s0, s1, 1.02, 1.1, cy=720)
        hud2d.blurred(cr, room, sigma=8)
        A.student_bust(cr, W / 2, K.BY - 10, 1.15, t, "ren", "focus", rim=(0.5, 1, 0.9, 0.6), rim_from=(0, 10))
        A.terminal(cr, t, W / 2, 1090, 0.75, tokens=100, bid=1 if t > 0.35 else None)
    elif name in ("r5", "r3", "r2"):
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.06, cy=700)
            hud2d.blurred(c, room, sigma=10)
            for j, who in enumerate(("mio", "haruto", "ren", "yui", "aoi")):
                A.student_bust(c, 80 + j * 140, 1260, 0.6, t, who, "worry")
        K.still(cr, t, s0, s1, "shot_keypad" if name == "r2" else "shot_huddle", z=(1.02, 1.14),
                drift=(0.04, 0.0) if name == "r3" else (0.0, -0.03), fallback=old)
        K.dark(cr, 0.2)
    elif name in ("ren", "ren2"):
        bust(cr, t, s0, s1, room, "ren", "focus", z=(1.03, 1.12), scale=1.3, sigma=10, rim=(0.5, 1, 0.9, 0.6),
             rim_from=(10, -6))
        if name == "ren":                                       # "So it had to be me."
            K.speed_lines(cr, t, clamp01((t - tl.at("t5", "so", nth=1)) / 0.3), col=(0, 0, 0), n=70)
    elif name == "plan":
        K.camera(cr, t, s0, s1, 1.0, 1.06, cy=900)
        if K.has_shot("shot_huddle"):
            K.still(cr, t, s0, s1, "shot_huddle", z=(1.1, 1.14), blur=6)
            K.dark(cr, 0.25)
        else:
            hud2d.blurred(cr, room, sigma=9)
        for j, who in enumerate(("mio", "haruto", "yui", "aoi")):
            A.student_bust(cr, (110, 260, 460, 610)[j], 1250, 0.62, t, who, "worry", look=(0.5 - j * 0.3, 0))
        A.student_bust(cr, W / 2, 1150, 0.95, t, "ren", "focus", talk=talk("ren"))
    elif name == "mio":
        bust(cr, t, s0, s1, room, "mio", "calm", talk("mio"))
    elif name == "liar":
        bust(cr, t, s0, s1, room, "ren", "focus", talk("ren"), z=(1.02, 1.12), scale=1.25)
    elif name == "riku":
        bust(cr, t, s0, s1, room, "riku", "smirk", talk("riku"), scale=1.25)
    elif name == "eyes":
        A.eye_closeup(cr, t, seg(t, s0, s1), "ren")
        K.speed_lines(cr, t, 0.8, cy=H / 2, col=(0, 0, 0), n=90, r0=W * 0.42)
    elif name == "result":
        K.camera(cr, t, s0, s1, 1.0, 1.18, cy=420, shake=1.6)
        K.chamber(cr, t, ["HIGHEST UNIQUE BID", "30", "KANZAKI RIKU"], momo_at=clamp01((t - s0) / 0.4))
        K.speed_lines(cr, t, clamp01((t - tl.at("t12", "thirty!")) / 0.2), cy=H * 0.24)
    elif name == "bluff":
        bust(cr, t, s0, s1, room, "riku", "smirk", z=(1.08, 1.16), scale=1.3)
        K.flashback(cr, 1.0 - clamp01((t - B["t13"].end + 0.4) / 0.4))
    elif name == "key":
        bust(cr, t, s0, s1, room, "riku", "smirk", talk("riku"), scale=1.2)
        K.key(cr, W * 0.74, 760 - 40 * clamp01((t - s0) / 0.5), 1.6, rot=-0.7)
        K.speed_lines(cr, t, 0.35, cy=H * 0.45, col=(1, 0.9, 0.6), n=50)
    elif name == "survivors":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.08, cy=500)
            K.chamber(c, t, ["NO TIE", "20 SURVIVORS"], case=False)
            for j, who in enumerate(("kota", "haruto", "ren", "yui", "go")):
                A.student_bust(c, 80 + j * 140, 1260, 0.6, t, who, "calm")
        K.still(cr, t, s0, s1, "shot_relief", z=(1.0, 1.1), drift=(0.05, 0.0), fallback=old)
        K.dust(cr, t, 0.6)
    elif name == "momo":
        K.camera(cr, t, s0, s1, 1.0, 1.15, cy=700)
        hud2d.blurred(cr, lambda c: K.chamber(c, t, ["20 SURVIVORS"], case=False), sigma=10)
        K.dark(cr, 0.35)
        A.momo(cr, W / 2, 1180, 3.6 + 0.5 * seg(t, s0, s0 + 0.8), t, mood="sly", lean=-0.12 * seg(t, s0, s0 + 0.8))
    elif name == "door":
        k = seg(t, B["t18"].start + 0.3, B["t18"].end)
        if K.has_shot("shot_door"):
            K.still(cr, t, s0, s1, "shot_door", z=(1.0, 1.3), a=(0.5, 0.45))
            glow(cr, W / 2, H * 0.4, 300 + 700 * k, (1, 1, 1), 0.3 + 0.5 * k)
            K.dust(cr, t, 0.8)
            cr.set_source_rgba(1, 1, 1, 0.75 * clamp01((k - 0.7) / 0.3))
            cr.paint()
        else:
            K.camera(cr, t, s0, s1, 1.0, 1.1, cy=700)
            K.door(cr, t, k)
    elif name == "end":
        bust(cr, t, s0, s1, lambda c: K.white_room(c, t, side=True), "riku", "worry", z=(1.04, 1.14), scale=1.25,
             sigma=12, sweat=0.5)
        A.terminal(cr, t, W * 0.78, 1150, 0.5, tokens=70)
    cr.restore()

    if A is dma_anime:                                          # satsuei: glow, cold light, aberration, grain
        bright = name in ("door", "end")
        satsuei.apply(cr, t, glow=0.3 if bright else 0.24, light=((0.5, 0.0), (0.7, 0.85, 1.0), 0.14),
                      shade=((0.5, 0.3), (0.35, 0.3, 0.45), 0.2 if bright else 0.35), ca=1.2, grain=0.03)
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.0)
    else:
        hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.06)

    K.impact(cr, t, tl.at("t12", "thirty!"), 0.25)
    K.impact(cr, t, B["t13"].end - 0.45, 0.17, red=False)
    if name == "survivors":
        K.slam(cr, t, B["t16"].start + 1.2, B["t16"].end + 0.3, [("20 SURVIVORS", False)], y=H * 0.22, size=80)
    K.card(cr, t, B["t2"].start + 0.05, B["t2"].end + 0.1, "RULE 5", RULE[5], hot=("executed",))
    K.card(cr, t, B["t3"].start + 0.05, B["t3"].start + 2.0, "RULE 3", RULE[3], hot=("same highest bid",),
           y=H * 0.4)
    collide(cr, t, B["t3"].start + 0.3, B["t3"].end + 0.1)
    K.card(cr, t, B["t4"].start + 0.05, B["t4"].end + 0.1, "RULE 2", RULE[2], hot=("permanently",))
    K.slam(cr, t, B["t6"].start + 0.1, B["t6"].end + 0.2, [("REN: 1", True), ("EVERYONE ELSE: 0", False)],
           y=H * 0.24)
    K.slam(cr, t, B["t8"].start + 0.6, B["t8"].end + 0.2, [("BID MORE THAN 1?", False), ("YOU WIN.", False),
                                                         ("NOBODY DIES.", True)], y=H * 0.2, size=66)
    hud2d.stamp(cr, t, B["t9"].start + 0.2, B["t9"].end + 0.3, ["NEVER 100"], y=330)
    K.slam(cr, t, B["t13"].start + 0.1, B["t13"].end - 0.5,
           [("\u201cNOBODY BEATS", False), ("A HUNDRED.\u201d", False)], y=H * 0.2, size=64)
    hud2d.stamp(cr, t, B["t13"].end - 0.45, B["t13"].end + 0.4, ["BLUFF"], y=360)
    K.slam(cr, t, B["t15"].end - 1.4, B["t15"].end + 0.3, [("BUILT FOR A LIAR", True)], y=H * 0.22, size=70)
    A.status_bar(cr, t, "GAME 01 · THE GLASS AUCTION", K.fmt(tleft) if t < B["t12"].start else "TIME'S UP",
                 alert=True)
    hud2d.hook(cr, t, [("MY NUMBER:", False), ("ONE.", True)], end=B["t1"].end + 0.2, y=230, size=86)
    for who, gid in (("mio", "t7"), ("riku", "t10")):
        A.name_card(cr, t, B[gid].start, B[gid].end, who, y=1150)
    cards = [(B[g].start - 0.05, B[g].end + 0.15) for g in ("t2", "t4")] + [(B["t3"].start, B["t3"].start + 2.1)]
    if t < B["t19"].end + 0.1 and not any(a <= t <= b for a, b in cards):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, B["t19"].end + 0.1, "DEAD MAN'S ALGORITHM", "PART 4", "THE CHARITY")
    cue("hum", t, 0.0, tl.total)
    for g in ("t2", "t3", "t4"):
        cue("click", t, B[g].start - 0.12)
    cue("heartbeat", t, B["t10"].start, B["t11"].end - B["t10"].start)
    cue("riser", t, B["t11"].end - 0.2, B["t12"].start - B["t11"].end + 0.2)
    cue("chime", t, B["t12"].start - 0.45)
    cue("sting", t, B["t12"].start + 0.05)
    cue("hit", t, B["t13"].end - 0.45)
    cue("chime", t, B["t17"].start - 0.4)
    cue("whoosh", t, B["t18"].start + 0.3)
