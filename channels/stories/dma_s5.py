"""DEAD MAN'S ALGORITHM, Part 5: "Nobody" (9:16). Ren's two-step loophole (approved script, owner 28 Oct 2026:
channels/stories/dma_arc_games_1_2.md v4): zero tokens means not a player, so if nobody is a player nobody is the
poorest; the tokens must go somewhere, and rule two says ANYONE in this room. Momo is in the room and isn't a player.
Everyone gives Momo everything. Riku refuses, and smiles.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s5   -> out/stories/dma_s5.mp4
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
TWIST = "n7"

SCRIPT = [
    dict(id="n1", scene="hook", text="Zero tokens, and you're not a player. If nobody is a player, nobody is the "
                                     "poorest."),
    dict(id="n2", scene="aoi", text="But the tokens have to go somewhere. Whoever holds them is a player.",
         speaker="aoi", gap=0.5),
    dict(id="n3", scene="haruto", text="Then give them all to one person.", speaker="haruto", gap=0.4),
    dict(id="n4", scene="momo", text="One player is always the poorest!", speaker="momo", gap=0.4),
    dict(id="n5", scene="r2", text="Then I read rule two again. Anyone in this room.", gap=0.6),
    dict(id="n6", scene="ren", text="Not any player. Anyone.", gap=0.4),
    dict(id="n7", scene="turn", text="And Momo was in this room.", gap=0.5),
    dict(id="n8", scene="momo2", text="For Momo? How generous!", speaker="momo", gap=0.5),
    dict(id="n9", scene="proof", text="Momo isn't a player. Give Momo everything, and there are no players. "
                                      "And nobody dies.", speaker="ren", gap=0.5),
    dict(id="n10", scene="mio", text="And walk into game three with nothing?", speaker="mio", gap=0.5),
    dict(id="n11", scene="haruto2", text="Tokens or our lives? That's easy.", speaker="haruto", gap=0.4),
    dict(id="n12", scene="give", text="One by one, we gave Momo everything.", gap=0.5),
    dict(id="n13", scene="saki", text="It's okay. I never wanted them.", speaker="saki", gap=0.5),
    dict(id="n14", scene="one", text="One player was left. Riku.", gap=0.6),
    dict(id="n15", scene="riku", text="I'm not walking into game three with nothing.", speaker="riku", gap=0.4),
    dict(id="n16", scene="warn", text="Then you're the only player. And the only player is always the poorest.",
         speaker="ren", gap=0.4),
    dict(id="n17", scene="end", text="Riku just smiled.", gap=0.6),
]

METADATA = dict(
    title="Nobody Can Be the Poorest If Nobody Is a Player 🧠",
    alt_titles=["The Loophole Was Sitting in the Middle of the Room 🧠",
                "Dead Man's Algorithm, Part 5: Nobody 🧠"],
    description="""Zero tokens, and you're not a player. So if nobody is a player, nobody is the poorest.
But the tokens have to go somewhere... and rule two says you may give them to ANYONE in this room.

Not any player. Anyone. And Momo was in the room.

Dead Man's Algorithm, Part 5: Nobody. Part 6 is next.

(Original story. Anime-style animation.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "game theory", "death game", "psychological thriller", "puzzle",
          "anime story", "loophole", "riddle", "part 5"],
    pinned_comment="Everyone gave Momo everything. Everyone except Riku. Why would the only player left be "
                   "smiling? 👇",
)

KEY = {"zero", "player", "nobody", "poorest", "somewhere", "one", "always", "anyone", "room", "momo", "generous",
       "everything", "nothing", "easy", "wanted", "riku", "only", "smiled"}


# ------------------------------------------------------------------ the film
RULE2 = "You may give tokens to anyone in this room. Gifts are final."
PLAN = [("n1", "hook"), ("n2", "aoi"), ("n3", "haruto"), ("n4", "momo"), ("n5", "r2"), ("n6", "ren"), ("n7", "turn"),
        ("n8", "momo2"), ("n9", "proof"), ("n10", "mio"), ("n11", "haruto2"), ("n12", "give"), ("n13", "saki"),
        ("n14", "one"), ("n15", "riku"), ("n16", "warn"), ("n17", "end")]
_sh = {}


def left(t, tl):
    """6:20 at the start (where Part 4 left the clock), about 0:12 as Riku smiles."""
    return 380 - 368 * clamp01(t / max(1.0, tl.by_id["n17"].end))


def players(t, tl):
    """20 until the class starts giving; down to 2 (Saki and Riku) during n12; 1 once Saki has given hers."""
    B = tl.by_id
    a, b = B["n12"].start + 0.4, B["n12"].end
    if t < a:
        return 20
    if t < b:
        return int(round(20 - 18 * clamp01((t - a) / (b - a))))
    return 2 if t < B["n13"].end + 0.2 else 1


def pile(t, tl):
    B = tl.by_id
    return 0.08 + 0.92 * clamp01((t - B["n11"].end) / (B["n13"].end + 0.2 - B["n11"].end))


def bust(cr, t, s0, s1, bg, who, expr, talk=0.0, z=(1.02, 1.1), scale=1.2, sigma=9, **kw):
    K.camera(cr, t, s0, s1, *z, cy=700)
    hud2d.blurred(cr, bg, sigma=sigma)
    A.student_bust(cr, W / 2, K.BY, scale, t, who, expr, talk=talk, **kw)


def draw(cr, t, tl):
    B = tl.by_id
    if id(tl) not in _sh:                                      # + two cut-ins inside beats
        _sh[id(tl)] = K.shot_index(tl, PLAN + [((B["n12"].start + B["n12"].end) / 2, "drop"),
                                               (B["n13"].end - 0.25, "saki_hands")])
    s0, name, s1 = K.current(_sh[id(tl)], t)
    tleft, n, pk = left(t, tl), players(t, tl), pile(t, tl)
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    room = lambda c: K.white_room(c, t, K.players(n), pile=pk, side=True)

    cr.save()
    if name == "hook":
        bust(cr, t, s0, s1, room, "ren", "focus", z=(1.02, 1.12), scale=1.25, sigma=10, rim=(0.5, 1, 0.9, 0.6),
             rim_from=(10, -6))
    elif name == "aoi":
        bust(cr, t, s0, s1, room, "aoi", "focus", talk("aoi"))
    elif name in ("haruto", "haruto2"):
        bust(cr, t, s0, s1, room, "haruto", "grin" if name == "haruto2" else "calm", talk("haruto"))
        if name == "haruto2":
            K.flying_tokens(cr, t, B["n11"].end - 0.6, B["n11"].end + 0.4, W / 2, 1100, W + 80, 700, n=5)
    elif name in ("momo", "momo2"):
        K.camera(cr, t, s0, s1, 1.0, 1.14, cy=900)
        hud2d.blurred(cr, lambda c: K.white_room(c, t, K.players(n), momo=False), sigma=9)
        A.momo(cr, W / 2, 1180, 3.4 + 0.4 * seg(t, s0, s0 + 0.8), t, mood="wink" if name == "momo" else "sly",
               lean=(0.1 if name == "momo" else -0.1) * seg(t, s0, s0 + 0.8))
    elif name == "r2":
        K.camera(cr, t, s0, s1, 1.0, 1.05, cy=900)
        if K.has_shot("shot_room"):
            K.still(cr, t, s0, s1, "shot_room", z=(1.06, 1.1), blur=6)
        else:
            hud2d.blurred(cr, room, sigma=11)
        K.dark(cr, 0.25)
    elif name == "ren":
        bust(cr, t, s0, s1, room, "ren", "focus", z=(1.06, 1.18), scale=1.4, sigma=12, rim=(0.5, 1, 0.9, 0.6),
             rim_from=(10, -6))
        K.speed_lines(cr, t, clamp01((t - tl.at("n6", "anyone.")) / 0.2), n=80)
    elif name == "turn":                                       # from Ren's shoulder, across the room, to Momo
        k = seg(t, s0, s1)
        e = k * k * (3 - 2 * k)
        cr.translate(W / 2, H * 0.62)
        cr.scale(1.0 + 0.9 * e, 1.0 + 0.9 * e)
        cr.translate(-W / 2 + 160 * (1 - e), -H * 0.62 - 120 * e)
        K.white_room(cr, t, K.players(n))
        A.student_bust(cr, 40 + 120 * e, 1300, 0.9, t, "ren", "focus", alpha=1 - e)
    elif name == "proof":
        K.camera(cr, t, s0, s1, 1.0, 1.04, cy=900)
        hud2d.blurred(cr, room, sigma=12)
        A.student_bust(cr, W / 2, 1230, 0.9, t, "ren", "focus", talk=talk("ren"))
    elif name == "mio":
        bust(cr, t, s0, s1, room, "mio", "fear", talk("mio"))
    elif name == "give":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.08, cy=900)
            K.white_room(c, t, K.players(n), pile=pk, flash=0.0)
            for j, (x0, y0) in enumerate(((-60, 1150), (W + 60, 1080), (-60, 900), (W + 60, 1250))):
                K.flying_tokens(c, t, B["n12"].start + 0.2 + 0.25 * j, B["n12"].end + 0.3, x0, y0, W * 0.5 + 150,
                                H * 0.72, n=4)
        K.still(cr, t, s0, s1, "shot_walk", z=(1.0, 1.1), drift=(0.0, -0.03), fallback=old)
    elif name == "drop":
        K.still(cr, t, s0, s1, "shot_drop", z=(1.04, 1.14), a=(0.5, 0.6),
                fallback=lambda c: K.white_room(c, t, K.players(n), pile=pk))
        for j in range(3):
            K.flying_tokens(cr, t, s0, s1 + 0.2, W * (0.3 + 0.2 * j), -60, W * (0.35 + 0.15 * j), H * 0.75, n=3)
    elif name == "saki":
        bust(cr, t, s0, s1, room, "saki", "smile", talk("saki"), z=(1.04, 1.12), scale=1.3, sigma=11)
    elif name == "saki_hands":
        K.still(cr, t, s0, s1, "shot_saki_hands", z=(1.0, 1.1), a=(0.5, 0.5),
                fallback=lambda c: bust(c, t, s0, s1, room, "saki", "smile", z=(1.04, 1.12), scale=1.3, sigma=11))
        K.dust(cr, t, 0.6)
    elif name == "one":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.1, cy=500)
            K.white_room(c, t, K.players(1), pile=pk, flash=1 - clamp01((t - s0) / 0.5), red=True)
            A.student_bust(c, W - 150, 1290, 0.75, t, "riku", "calm")
        K.still(cr, t, s0, s1, "shot_riku_alone", z=(1.0, 1.14), fallback=old)
    elif name == "riku":
        bust(cr, t, s0, s1, room, "riku", "calm", talk("riku"), scale=1.25)
    elif name == "warn":
        bust(cr, t, s0, s1, room, "ren", "fear", talk("ren"), z=(1.02, 1.1), scale=1.25)
    elif name == "end":
        bust(cr, t, s0, s1, room, "riku", "smirk", z=(1.06, 1.24), scale=1.35, sigma=12)
        K.dark(cr, 0.2 * seg(t, s0, s1))
        K.speed_lines(cr, t, 0.7 * seg(t, s0, s0 + 0.6), col=(0, 0, 0), n=80)
    cr.restore()

    if A is dma_anime:                                          # satsuei: the room's cold white light
        satsuei.apply(cr, t, glow=0.22, light=((0.5, 0.0), (0.92, 0.96, 1.0), 0.12),
                      shade=((0.5, 0.3), (0.45, 0.5, 0.62), 0.2), ca=1.0, grain=0.03)
        hud.finish(cr, t, flash_at=[], vig=0.4, grain=0.0)
    else:
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.06)

    K.impact(cr, t, tl.at("n7", "momo"), 0.25)
    if name in ("give", "drop", "saki_hands", "one", "r2"):
        K.chip_players(cr, t, n, red=n <= 2)
    if name == "one" and K.has_shot("shot_riku_alone"):
        K.slam(cr, t, B["n14"].start + 0.2, B["n14"].end + 0.4, [("PLAYERS: 1", True)], y=H * 0.2, size=84)
    K.card(cr, t, B["n5"].start + 0.05, B["n5"].end + 0.4, "RULE 2", RULE2, hot=("anyone in this room",))
    K.slam(cr, t, B["n4"].start + 0.1, B["n4"].end + 0.3, [("1 PLAYER =", False), ("THE POOREST", True)],
           y=H * 0.2, size=72)
    K.slam(cr, t, B["n6"].start + 0.05, B["n6"].end + 0.3, [("NOT ANY PLAYER.", False), ("ANYONE.", True)],
           y=H * 0.2, size=74)
    K.proof(cr, t, B["n9"].start, B["n9"].end + 0.6,
            [("0 TOKENS = NOT A PLAYER", B["n9"].start + 0.1, False),
             ("GIVE MOMO EVERYTHING", tl.at("n9", "give"), False),
             ("0 PLAYERS", tl.at("n9", "there"), False),
             ("NOBODY IS THE POOREST", tl.at("n9", "nobody"), True)], y0=H * 0.16, gap=H * 0.12)
    K.slam(cr, t, B["n16"].start + 1.4, B["n16"].end + 0.3, [("ONLY PLAYER =", False), ("THE POOREST", True)],
           y=H * 0.2, size=72)
    K.rules_strip(cr, t, 4, 4 if t < B["n5"].start else 2 if t < B["n10"].start else None, n=4)
    A.status_bar(cr, t, "GAME 02 · THE CHARITY", K.fmt(tleft), alert=True)
    hud2d.hook(cr, t, [("ZERO TOKENS =", False), ("NOT A PLAYER.", True)], end=B["n1"].end + 0.2, y=250, size=80)
    for who, gid in (("aoi", "n2"), ("haruto", "n3"), ("mio", "n10"), ("saki", "n13"), ("riku", "n15")):
        A.name_card(cr, t, B[gid].start, B[gid].end, who, y=1150)
    busy = [(B["n5"].start - 0.05, B["n5"].end + 0.45), (B["n9"].start - 0.05, B["n9"].end + 0.65)]
    if t < B["n17"].end + 0.1 and not any(a <= t <= b for a, b in busy):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, B["n17"].end + 0.1, "DEAD MAN'S ALGORITHM", "PART 6", "THE GIFT")
    cue("hum", t, 0.0, tl.total)
    cue("chime", t, B["n4"].start - 0.4)
    cue("click", t, B["n5"].start - 0.12)
    cue("riser", t, B["n6"].start, B["n7"].start - B["n6"].start + 0.2)
    cue("sting", t, B["n7"].start + 0.2)
    cue("chime", t, B["n8"].start - 0.4)
    for g in ("n9",):
        for w in ("give", "there", "nobody"):
            cue("pop", t, tl.at(g, w) - 0.05)
    cue("kaching", t, B["n12"].start + 0.3)
    cue("kaching", t, B["n13"].end + 0.1)
    cue("heartbeat", t, B["n15"].start, B["n17"].end - B["n15"].start)
