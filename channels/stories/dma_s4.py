"""DEAD MAN'S ALGORITHM, Part 4: "The Charity" (9:16). Game 2's four rules (approved script, owner 28 Oct 2026:
channels/stories/dma_arc_games_1_2.md v4): give tokens to anyone in this room; the poorest player dies; a tie for
poorest kills them all; zero tokens and you're not a player. Every obvious answer fails on screen. Go wants Riku to
die; Saki says he's still one of us, and Riku hears her (the clue for Part 6).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s4   -> out/stories/dma_s4.mp4
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
TWIST = "h17"

SCRIPT = [
    dict(id="h1", scene="hook", text="The exit led to a white room. And Momo was sitting in the middle of it."),
    dict(id="h2", scene="momo", text="Game two! The Charity! Sharing is caring!", speaker="momo", gap=0.5),
    dict(id="h3", scene="rule", text="Rule one. Nobody can take your tokens.", speaker="momo"),
    dict(id="h4", scene="rule", text="Rule two. You may give tokens to anyone in this room. Gifts are final.",
         speaker="momo"),
    dict(id="h5", scene="rule", text="Rule three. When time runs out, the poorest player dies. A tie for poorest? "
                                     "They all die!", speaker="momo"),
    dict(id="h6", scene="rule", text="Rule four. Zero tokens, and you're not a player anymore.", speaker="momo"),
    dict(id="h7", scene="go", text="Tokens are precious! You'll want them later! Ten minutes!", speaker="momo",
         gap=0.5),
    dict(id="h8", scene="riku70", text="Riku had seventy. Fewer than anyone.", gap=0.6),
    dict(id="h9", scene="riku", text="Somebody give me thirty-one.", speaker="riku", gap=0.4),
    dict(id="h10", scene="aoi", text="Then the giver is the poorest.", speaker="aoi", gap=0.4),
    dict(id="h11", scene="go_", text="Let him be the poorest. He lied to all of us.", speaker="go", gap=0.4),
    dict(id="h12", scene="saki_in", text="Then the quietest girl in our class spoke. Seat fourteen. Nishida Saki.",
         gap=0.6),
    dict(id="h13", scene="saki", text="He's still one of us.", speaker="saki", gap=0.4),
    dict(id="h14", scene="riku_look", text="Riku looked at her for a long time.", gap=0.5),
    dict(id="h15", scene="mio", text="Then we all hold the same. Nobody is the poorest.", speaker="mio", gap=0.5),
    dict(id="h16", scene="aoi2", text="A tie for poorest. We'd all die.", speaker="aoi", gap=0.4),
    dict(id="h17", scene="stacks", text="Tokens can't vanish. Somebody always holds the fewest.", gap=0.5),
    dict(id="h18", scene="end", text="Somebody in this room had to die. Unless nobody was a player at all.", gap=0.4),
]

METADATA = dict(
    title="The Poorest Player Dies. A Tie for Poorest? They ALL Die. 💀",
    alt_titles=["Give Your Tokens Away and YOU Become the Poorest 💀",
                "Dead Man's Algorithm, Part 4: The Charity 💀"],
    description="""Game two. Four rules.
You may give tokens to anyone in this room. When time runs out, the poorest player dies. A tie for poorest? They all
die. Zero tokens, and you're not a player.

Riku has the fewest. Half the class wants him dead. One quiet girl doesn't.

Dead Man's Algorithm, Part 4: The Charity. Part 5 is next.

(Original story. Anime-style animation.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "game theory", "death game", "psychological thriller", "puzzle",
          "anime story", "loophole", "riddle", "part 4"],
    pinned_comment="Every answer they tried kills someone. There IS a way for all twenty to live, and it's in the "
                   "rules on screen. Can you find it before Part 5? 👇",
)

KEY = {"white", "momo", "charity", "take", "anyone", "final", "poorest", "die", "zero", "player", "precious",
       "seventy", "fewer", "thirty-one", "lied", "fourteen", "saki", "us", "long", "same", "vanish", "fewest",
       "nobody"}


# ------------------------------------------------------------------ the film
RULES = ["Nobody can take your tokens.",
         "You may give tokens to anyone in this room. Gifts are final.",
         "When time runs out, the poorest player dies. If several tie for poorest, they all die.",
         "Zero tokens, and you're not a player."]
HOT = [("take",), ("final",), ("poorest", "all die"), ("zero tokens",)]
PLAN = [("h1", "hook"), ("h2", "momo"), ("h3", "rules"), ("h7", "go"), ("h8", "riku70"), ("h9", "riku"),
        ("h10", "aoi"), ("h11", "go_"), ("h12", "saki_in"), ("h13", "saki"), ("h14", "riku_look"), ("h15", "mio"),
        ("h16", "aoi2"), ("h17", "stacks"), ("h18", "end")]
_sh = {}
MOMO_AT = (W * 0.5, H * 0.74, 0.62)                            # Momo on the floor of the shot_room painting
# the twenty after Game 1 (Ren bid 1, Riku 30, everyone else 0): in the grid, Riku is cell 6 and Ren cell 13
START = [100] * 20
START[6], START[13] = 70, 99


def left(t, tl):
    t0 = tl.at("h7", "minutes!", end=True)
    return 600.0 if t < t0 else max(0.0, 600 - (t - t0) * 6)


def bust(cr, t, s0, s1, bg, who, expr, talk=0.0, z=(1.02, 1.1), scale=1.2, sigma=9, **kw):
    K.camera(cr, t, s0, s1, *z, cy=700)
    hud2d.blurred(cr, bg, sigma=sigma)
    A.student_bust(cr, W / 2, K.BY, scale, t, who, expr, talk=talk, **kw)


def grid(cr, t, k_give):
    """Twenty stacks; the poorest glows red. k_give 0..1: someone hands Riku 31 and becomes the poorest instead."""
    vals = list(START)
    if k_give >= 1:
        vals[6], vals[7] = 101, 69
    low = min(vals)
    for i, v in enumerate(vals):
        cx, cy = W * (0.14 + 0.24 * (i % 4)), H * (0.22 + 0.13 * (i // 4))
        red = v == low
        if red:
            glow(cr, cx, cy - 10, 110, K.RED[:3], 0.35 + 0.15 * math.sin(t * 7))
        K.stack(cr, cx, cy, v, r=30, red=red)
    if 0 < k_give < 1:                                        # 31 tokens flying from cell 7 to Riku (cell 6)
        x0, x1, y = W * 0.86, W * 0.62, H * 0.35 - 10
        for j in range(5):
            p = clamp01(k_give * 1.3 - j * 0.07)
            K.token(cr, x0 + (x1 - x0) * p, y - math.sin(p * math.pi) * 90, 20)


def draw(cr, t, tl):
    B = tl.by_id
    if id(tl) not in _sh:
        _sh[id(tl)] = K.shot_index(tl, PLAN)
    s0, name, s1 = K.current(_sh[id(tl)], t)
    tleft = left(t, tl)
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    room = lambda c: K.white_room(c, t, K.players(20), side=True)

    cr.save()
    if name == "hook":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.08, cy=1000)
            K.white_room(c, t, K.players(20))
            for x, who in ((90, "mio"), (W - 90, "haruto")):
                A.student_bust(c, x, 1330, 0.62, t, who, "worry")
        if K.has_shot("shot_room"):
            K.camera(cr, t, s0, s1, 1.0, 1.08, cy=MOMO_AT[1])
            K.still(cr, t, s0, s1, "shot_room", z=(1.0, 1.04), par=0.0)
            A.momo(cr, MOMO_AT[0], MOMO_AT[1], MOMO_AT[2], t, mood="happy")
            K.dust(cr, t, 0.5)
        else:
            old(cr)
    elif name == "momo":
        K.camera(cr, t, s0, s1, 1.0, 1.12, cy=900)
        hud2d.blurred(cr, lambda c: K.white_room(c, t, K.players(20), momo=False), sigma=8)
        A.momo(cr, W / 2, 1180, 3.4 + 0.4 * seg(t, s0, s0 + 0.8), t, mood="happy", wave=clamp01((t - s0) / 0.4))
    elif name == "rules":
        K.camera(cr, t, s0, s1, 1.0, 1.05, cy=900)
        if K.has_shot("shot_room"):
            K.still(cr, t, s0, s1, "shot_room", z=(1.06, 1.1), blur=6)
            K.dark(cr, 0.3)
        else:
            hud2d.blurred(cr, room, sigma=10)
            for j, who in enumerate(("mio", "haruto", "ren", "yui", "aoi")):
                A.student_bust(cr, 80 + j * 140, 1260, 0.6, t, who, "worry")
    elif name == "go":
        K.camera(cr, t, s0, s1, 1.0, 1.06, cy=700)
        K.white_room(cr, t, K.players(20))
        for j, who in enumerate(("kota", "go", "ren", "saki", "riku")):
            A.student_bust(cr, 80 + j * 140, 1290, 0.58, t, who, "worry")
    elif name == "riku70":
        if K.has_shot("shot_coins"):
            K.still(cr, t, s0, s1, "shot_coins", z=(1.0, 1.12), a=(0.5, 0.55))
            K.dark(cr, 0.15)
            hud2d._text(cr, "70", W / 2, H * 0.3, 190, K.RED, hud2d.ROUND, "center", outline=(0, 0, 0, 1), ow=16,
                        shadow=0.6)
            hud2d._text(cr, "EVERYONE ELSE: 100", W / 2, H * 0.3 + 80, 40, (1, 1, 1, 1), hud2d.ROUND, "center",
                        outline=(0, 0, 0, 1), ow=6)
        else:
            bust(cr, t, s0, s1, room, "riku", "fear", z=(1.02, 1.08), scale=1.15, sweat=0.6)
            K.stack(cr, W * 0.8, 1120, 70, r=40, red=True)
            K.stack(cr, W * 0.2, 1120, 100, r=40)
            hud2d._text(cr, "EVERYONE ELSE", W * 0.2, 1240, 26, (1, 1, 1, 0.9), hud2d.ROUND, "center",
                        outline=(0, 0, 0, 1), ow=4)
            hud2d._text(cr, "RIKU", W * 0.8, 1240, 26, K.RED, hud2d.ROUND, "center", outline=(0, 0, 0, 1), ow=4)
    elif name == "riku":
        bust(cr, t, s0, s1, room, "riku", "fear", talk("riku"), scale=1.25, sweat=0.8)
    elif name in ("aoi", "aoi2"):
        bust(cr, t, s0, s1, room, "aoi", "focus", talk("aoi"))
    elif name == "go_":
        bust(cr, t, s0, s1, room, "go", "angry", talk("go"), scale=1.2)
        K.speed_lines(cr, t, clamp01((t - tl.at("h11", "lied")) / 0.2), col=(0, 0, 0), n=70)
    elif name == "saki_in":
        K.still(cr, t, s0, s1, "shot_saki_alone", z=(1.0, 1.12), drift=(0.03, 0.0),
                fallback=lambda c: bust(c, t, s0, s1, room, "saki", "calm", z=(1.0, 1.12), scale=1.25, sigma=11))
        K.dust(cr, t, 0.5)
    elif name == "saki":
        bust(cr, t, s0, s1, room, "saki", "calm", talk("saki"), z=(1.06, 1.14), scale=1.3, sigma=11)
    elif name == "riku_look":
        bust(cr, t, s0, s1, room, "riku", "calm", z=(1.04, 1.2), scale=1.3, sigma=12, tilt=-0.03)
        K.dark(cr, 0.18)
    elif name == "mio":
        bust(cr, t, s0, s1, room, "mio", "calm", talk("mio"))
    elif name == "stacks":
        K.camera(cr, t, s0, s1, 1.0, 1.04, cy=700)
        hud2d.blurred(cr, room, sigma=12)
        K.dark(cr, 0.45)
        grid(cr, t, clamp01((t - B["h17"].start - 0.6) / 1.4))
    elif name == "end":
        bust(cr, t, s0, s1, room, "ren", "focus", z=(1.04, 1.16), scale=1.35, sigma=12, rim=(0.5, 1, 0.9, 0.6),
             rim_from=(10, -6))
        K.dark(cr, 0.2)
        K.speed_lines(cr, t, clamp01((t - tl.at("h18", "unless")) / 0.3), n=70)
    cr.restore()

    if A is dma_anime:                                          # satsuei: the room's cold white light
        satsuei.apply(cr, t, glow=0.22, light=((0.5, 0.0), (0.92, 0.96, 1.0), 0.12),
                      shade=((0.5, 0.3), (0.45, 0.5, 0.62), 0.2), ca=1.0, grain=0.03)
        hud.finish(cr, t, flash_at=[], vig=0.4, grain=0.0)
    else:
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.06)

    for n, gid in enumerate(("h3", "h4", "h5", "h6"), 1):
        K.card(cr, t, B[gid].start + 0.05, B[gid].end + 0.1, f"RULE {n}", RULES[n - 1], hot=HOT[n - 1])
    K.card(cr, t, B["h16"].start + 0.05, B["h16"].end + 0.2, "RULE 3", RULES[2], hot=("all die",), y=H * 0.27,
           size=30)
    shown = sum(t >= B[g].end for g in ("h3", "h4", "h5", "h6"))
    hot = 2 if B["h9"].start <= t <= B["h10"].end + 0.3 else 3 if B["h15"].start <= t <= B["h17"].end else \
        4 if B["h18"].start <= t else None
    K.rules_strip(cr, t, shown, hot, n=4)
    if name in ("hook", "rules", "riku70", "saki_in"):
        K.chip_players(cr, t, 20)
    go = t >= tl.at("h7", "minutes!", end=True)
    A.status_bar(cr, t, "GAME 02 · THE CHARITY", K.fmt(tleft) if go else "20 PLAYERS", alert=go)
    hud2d.hook(cr, t, [("GAME TWO.", False), ("THE POOREST DIES.", True)], end=B["h1"].end + 0.2, y=330, size=80)
    K.slam(cr, t, B["h18"].start + 1.9, B["h18"].end + 0.3, [("UNLESS NOBODY", False), ("IS A PLAYER?", True)],
           y=H * 0.2, size=74)
    for who, gid in (("riku", "h9"), ("aoi", "h10"), ("go", "h11"), ("saki", "h12"), ("mio", "h15")):
        A.name_card(cr, t, B[gid].start, B[gid].end, who, y=1150)
    cards = [(B[g].start - 0.05, B[g].end + 0.15) for g in ("h3", "h4", "h5", "h6")]
    if t < B["h18"].end + 0.1 and not any(a <= t <= b for a, b in cards):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, B["h18"].end + 0.1, "DEAD MAN'S ALGORITHM", "PART 5", "NOBODY")
    cue("hum", t, 0.0, tl.total)
    cue("chime", t, B["h2"].start - 0.45)
    for g in ("h3", "h4", "h5", "h6"):
        cue("click", t, B[g].start - 0.12)
    cue("sting", t, tl.at("h7", "minutes!", end=True) + 0.05)
    cue("heartbeat", t, B["h11"].start, B["h14"].end - B["h11"].start)
    cue("kaching", t, B["h17"].start + 0.6)
    cue("riser", t, B["h18"].start, B["h18"].end - B["h18"].start)
