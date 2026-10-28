"""DEAD MAN'S ALGORITHM, Part 6: "The Gift" (9:16). Riku's counter-loophole (approved script, owner 28 Oct 2026:
channels/stories/dma_arc_games_1_2.md v4): with three seconds left he gives Saki one token, which makes her a player
again, and the poorest. To live she would have to pass it on, and that kills Riku. She can't; he knew she couldn't.
Saki is executed (lights out, no gore). Nineteen survivors.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s6   -> out/stories/dma_s6.mp4
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
TWIST = "f3"

SCRIPT = [
    dict(id="f1", scene="hook", text="Riku was the only player left. Ten seconds. And he was smiling."),
    dict(id="f2", scene="walk", text="He walked across the room. To Saki.", gap=0.5),
    dict(id="f3", scene="palm", text="Three seconds left. He put one token in her hand.", gap=0.5),
    dict(id="f4", scene="momo", text="A gift! Gifts are final!", speaker="momo", gap=0.4),
    dict(id="f5", scene="screen2", text="The screen changed. Players, two.", gap=0.4),
    dict(id="f6", scene="saki", text="One token made her a player again. The poorest one.", gap=0.4),
    dict(id="f7", scene="ren", text="None of us had a single token left to stop it.", gap=0.4),
    dict(id="f8", scene="logic", text="If she gave it to Momo, Riku would be alone again. And he would die.",
         gap=0.4),
    dict(id="f9", scene="shout", text="Saki! Give it to Momo!", speaker="ren", gap=0.4),
    dict(id="f10", scene="ren2", text="I was telling her to kill him. I didn't care.", gap=0.4),
    dict(id="f11", scene="saki2", text="Saki looked at Riku. She couldn't do it.", gap=0.5),
    dict(id="f12", scene="riku", text="Riku knew she couldn't. He'd heard her say it.", gap=0.4),
    dict(id="f13", scene="flash", text="He's still one of us.", speaker="saki", gap=0.4),
    dict(id="f14", scene="ledger", text="Time's up! Kanzaki Riku, sixty-nine. Nishida Saki, one!", speaker="momo",
         gap=0.6),
    dict(id="f15", scene="out", text="The lights went out.", gap=0.6),
    dict(id="f16", scene="floor", text="When they came back, Saki was gone. Her token lay on the floor.", gap=1.0),
    dict(id="f17", scene="nineteen", text="The screen said nineteen survivors.", gap=0.5),
    dict(id="f18", scene="riku2", text="She was the only one I trusted.", speaker="riku", gap=0.6),
    dict(id="f19", scene="end", text="I found the loophole. Riku found the loophole in my loophole.", gap=0.6),
]

METADATA = dict(
    title="He Gave Her ONE Token. That Was Enough to Kill Her. 🪙",
    alt_titles=["The Box Didn't Matter. One Gift Did. 🪙", "Dead Man's Algorithm, Part 6: The Gift 🪙"],
    description="""Riku was the only player left, and the only player is always the poorest.
With three seconds left, he put one token in Saki's hand. Gifts are final.
One token made her a player again. The poorest one.

She could pass it on, and he would die. She couldn't do it. He knew she couldn't.

Dead Man's Algorithm, Part 6: The Gift.
I found the loophole. Riku found the loophole in my loophole.

(Original story. Anime-style animation. No real people.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "game theory", "death game", "psychological thriller", "betrayal",
          "anime story", "loophole", "twist", "part 6"],
    pinned_comment="Saki could have saved herself by handing the token to Momo, and Riku would have died. "
                   "Was refusing kindness, or a mistake? 👇",
)

KEY = {"only", "smiling", "saki", "three", "token", "gift", "final", "two", "poorest", "stop", "momo", "alone",
       "die", "kill", "care", "couldn't", "knew", "us", "sixty-nine", "one", "out", "gone", "floor", "nineteen",
       "trusted", "loophole"}


# ------------------------------------------------------------------ the film
PLAN = [("f1", "hook"), ("f2", "walk"), ("f3", "palm"), ("f4", "momo"), ("f5", "screen2"), ("f6", "saki"),
        ("f7", "ren"), ("f8", "logic"), ("f9", "shout"), ("f10", "ren2"), ("f11", "saki2"), ("f12", "riku"),
        ("f13", "flash"), ("f14", "ledger"), ("f15", "out"), ("f16", "floor"), ("f17", "nineteen"), ("f18", "riku2"),
        ("f19", "end")]
_sh = {}


def left(t, tl):
    """0:10 as it opens, 0:03 when the token lands; then the last seconds stretch until Momo calls time."""
    B = tl.by_id
    a, b, c = B["f1"].start, B["f3"].start, B["f14"].start
    if t < b:
        return 10 - 7 * clamp01((t - a) / (b - a))
    return max(0.0, 3 - 3 * clamp01((t - b) / (c - b)))


def landed(tl):
    return tl.at("f3", "hand", end=True)


def players(t, tl):
    return 1 if t < landed(tl) else 2


def bust(cr, t, s0, s1, bg, who, expr, talk=0.0, z=(1.02, 1.1), scale=1.2, sigma=9, **kw):
    K.camera(cr, t, s0, s1, *z, cy=700)
    hud2d.blurred(cr, bg, sigma=sigma)
    A.student_bust(cr, W / 2, K.BY, scale, t, who, expr, talk=talk, **kw)


def draw(cr, t, tl):
    B = tl.by_id
    if id(tl) not in _sh:                                      # + a cut-in inside the walk
        _sh[id(tl)] = K.shot_index(tl, PLAN + [((B["f2"].start + B["f2"].end) / 2 + 0.2, "feet")])
    s0, name, s1 = K.current(_sh[id(tl)], t)
    tleft, n = left(t, tl), players(t, tl)
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    after = t >= B["f15"].start                                 # Saki is gone
    room = lambda c: K.white_room(c, t, ["SURVIVORS", "19"] if t >= B["f17"].start - 0.2 else K.players(n),
                                  pile=1.0, red=n == 2 and not after, side=True)

    cr.save()
    if name == "hook":
        bust(cr, t, s0, s1, room, "riku", "smirk", z=(1.02, 1.12), scale=1.25)
    elif name == "walk":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.06, cy=900)
            hud2d.blurred(c, room, sigma=6)
            k = seg(t, s0, s1)
            A.student_bust(c, W * 0.7, 1210, 0.85, t, "saki", "fear")
            A.student_bust(c, -120 + (W * 0.32 + 120) * k, 1230, 0.9, t, "riku", "calm",
                           tilt=0.02 * math.sin(t * 9))
        K.still(cr, t, s0, s1, "shot_riku_walk", z=(1.04, 1.1), drift=(-0.06, 0.0), par=0.08, fallback=old)
    elif name == "feet":
        K.still(cr, t, s0, s1, "shot_feet", z=(1.0, 1.08), drift=(0.08, 0.0),
                fallback=lambda c: K.white_room(c, t, K.players(n), pile=1.0))
    elif name == "palm":
        def old(c):
            K.camera(c, t, s0, s1, 1.0, 1.1, cy=800)
            hud2d.blurred(c, room, sigma=14)
            K.dark(c, 0.15)
            drop = tl.at("f3", "token")
            K.palm(c, t, W / 2, H * 0.66, 1.5, has_token=clamp01((t - drop) / max(0.2, landed(tl) - drop)), close=0.0)
        K.still(cr, t, s0, s1, "shot_give", z=(1.0, 1.16), a=(0.5, 0.5), fallback=old)
        K.speed_lines(cr, t, clamp01((t - landed(tl)) / 0.15), col=(0, 0, 0), n=70, r0=W * 0.4)
    elif name == "momo":
        K.camera(cr, t, s0, s1, 1.0, 1.14, cy=900)
        hud2d.blurred(cr, lambda c: K.white_room(c, t, K.players(n), momo=False, pile=1.0, red=True), sigma=9)
        A.momo(cr, W / 2, 1180, 3.4 + 0.4 * seg(t, s0, s0 + 0.8), t, mood="happy", wave=clamp01((t - s0) / 0.4))
    elif name == "screen2":
        K.camera(cr, t, s0, s1, 1.0, 1.2, cx=W * 0.39, cy=H * 0.2, shake=1.6)
        K.white_room(cr, t, K.players(2), flash=1 - clamp01((t - s0) / 0.4), red=True, pile=1.0)
    elif name in ("saki", "saki2"):
        bust(cr, t, s0, s1, room, "saki", "fear", z=(1.04, 1.14) if name == "saki" else (1.1, 1.32),
             scale=1.3 if name == "saki" else 1.45, sigma=12, tremble=0.4)
    elif name in ("ren", "ren2"):
        bust(cr, t, s0, s1, room, "ren", "fear", z=(1.02, 1.1), scale=1.25, sigma=11)
        if name == "ren2":
            K.dark(cr, 0.3)
            cr.set_source_rgba(0.4, 0, 0, 0.12)
            cr.paint()
    elif name == "logic":
        K.camera(cr, t, s0, s1, 1.0, 1.04, cy=900)
        hud2d.blurred(cr, room, sigma=12)
    elif name == "shout":
        K.camera(cr, t, s0, s1, 1.0, 1.12, cy=700, shake=3.0)
        hud2d.blurred(cr, room, sigma=9)
        A.student_bust(cr, W / 2, K.BY, 1.3, t, "ren", "fear", talk=talk("ren"), tremble=1.0)
        K.speed_lines(cr, t, 0.9, n=90)
    elif name == "riku":
        bust(cr, t, s0, s1, room, "riku", "calm", z=(1.04, 1.16), scale=1.3, sigma=11)
    elif name == "flash":
        bust(cr, t, s0, s1, lambda c: K.white_room(c, t, K.players(20), side=True), "saki", "calm", talk("saki"),
             z=(1.0, 1.06), scale=1.25, sigma=10)
        K.flashback(cr, 1.0)
    elif name == "ledger":
        K.camera(cr, t, s0, s1, 1.0, 1.05, cy=900)
        hud2d.blurred(cr, room, sigma=12)
        K.dark(cr, 0.4)
        A.momo(cr, W / 2, 1240, 2.2, t, mood="sly")
    elif name == "out":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    elif name == "floor" and K.has_shot("shot_coin_floor"):
        K.still(cr, t, s0, s1, "shot_coin_floor", z=(1.12, 1.0), a=(0.5, 0.55))
        K.dark(cr, 1 - clamp01((t - s0 - 0.4) / 0.8))           # the lights coming back
    elif name == "floor":
        k = clamp01((t - s0 - 0.4) / 0.8)                       # the lights coming back
        K.camera(cr, t, s0, s1, 1.04, 1.16, cy=1000)
        hud2d.blurred(cr, lambda c: K.white_room(c, t, None, momo=False, pile=1.0), sigma=8)
        cr.save()
        cr.translate(W * 0.5, H * 0.8)
        cr.set_source_rgba(0, 0, 0, 0.25)
        cr.save()
        cr.scale(1, 0.3)
        cr.arc(0, 30, 70, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
        cr.scale(1, 0.45)
        K.token(cr, 0, 0, 62)
        cr.restore()
        K.dark(cr, 1 - k)
    elif name == "nineteen":
        K.camera(cr, t, s0, s1, 1.0, 1.15, cx=W * 0.39, cy=H * 0.2)
        K.white_room(cr, t, ["SURVIVORS", "19"], pile=1.0)
    elif name == "riku2":
        bust(cr, t, s0, s1, room, "riku", "calm", talk("riku"), z=(1.04, 1.12), scale=1.3, sigma=11)
    elif name == "end":
        bust(cr, t, s0, s1, room, "ren", "focus", z=(1.06, 1.22), scale=1.35, sigma=12, rim=(1, 0.3, 0.3, 0.5),
             rim_from=(10, -6))
        K.dark(cr, 0.25)
        K.speed_lines(cr, t, clamp01((t - tl.at("f19", "riku")) / 0.3), col=(0, 0, 0), n=80)
    cr.restore()

    if A is dma_anime and name != "out":                        # satsuei: the room's cold white light
        satsuei.apply(cr, t, glow=0.22, light=((0.5, 0.0), (0.92, 0.96, 1.0), 0.12),
                      shade=((0.5, 0.3), (0.45, 0.5, 0.62), 0.22), ca=1.0 if name != "shout" else 2.0, grain=0.03)
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.0)
    elif name != "out":
        hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.06)

    K.impact(cr, t, landed(tl), 0.25)
    K.impact(cr, t, B["f5"].start, 0.17, red=False)
    K.impact(cr, t, B["f14"].start + 0.5 + 0.9 * 2, 0.25)                 # the ledger marks the poorest
    if name in ("walk", "feet", "palm", "floor"):
        K.chip_players(cr, t, 19 if after else n, red=n == 2 and not after)
    K.proof(cr, t, B["f8"].start, B["f8"].end + 0.4,
            [("SAKI GIVES IT TO MOMO", tl.at("f8", "gave"), False),
             ("RIKU IS ALONE AGAIN", tl.at("f8", "alone"), False),
             ("ALONE = POOREST: RIKU DIES", tl.at("f8", "die."), True)], y0=H * 0.2, gap=H * 0.14)
    K.ledger(cr, t, B["f14"].start, B["f14"].end + 0.5, [("KANZAKI RIKU", 69), ("NISHIDA SAKI", 1)], y=H * 0.2)
    K.slam(cr, t, landed(tl), B["f3"].end + 0.3, [("PLAYERS: 2", True)], y=H * 0.2, size=84)
    if name != "out":
        A.status_bar(cr, t, "GAME 02 · THE CHARITY",
                     "0:00" if t >= B["f14"].start else f"0:{int(math.ceil(tleft)):02d}", alert=True)
    hud2d.hook(cr, t, [("ONE PLAYER LEFT.", False), ("10 SECONDS.", True)], end=B["f1"].end + 0.2, y=250, size=80)
    if t < B["f2"].start:
        hud2d._text(cr, f"0:{int(math.ceil(tleft)):02d}", W / 2, 470, 70, K.RED, "Liberation Mono", "center",
                    outline=(0, 0, 0, 1), ow=6)
    if B["f3"].start <= t < landed(tl) + 0.4:
        hud2d._text(cr, "0:03", W / 2, 300, 96, K.RED, "Liberation Mono", "center", outline=(0, 0, 0, 1), ow=8)
    busy = [(B["f8"].start - 0.05, B["f8"].end + 0.45), (B["f14"].start - 0.05, B["f14"].end + 0.55)]
    if t < B["f19"].end + 0.1 and not any(a <= t <= b for a, b in busy):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, B["f19"].end + 0.1, "DEAD MAN'S ALGORITHM", "PART 7", "GAME THREE")
    cue("hum", t, 0.0, B["f15"].start)
    cue("heartbeat", t, 0.0, B["f3"].start)
    cue("step", t, B["f2"].start + 0.3)
    cue("step", t, B["f2"].start + 0.9)
    cue("ding", t, landed(tl) - 0.05)
    cue("sting", t, landed(tl) + 0.1)
    cue("chime", t, B["f4"].start - 0.4)
    for w in ("gave", "alone", "die."):
        cue("pop", t, tl.at("f8", w) - 0.05)
    cue("heartbeat", t, B["f9"].start, B["f13"].end - B["f9"].start)
    cue("riser", t, B["f13"].start, B["f14"].start - B["f13"].start)
    cue("chime", t, B["f14"].start - 0.4)
    cue("thud", t, B["f15"].start + 0.05)
    cue("hum", t, B["f16"].start + 0.4, tl.total - B["f16"].start)
