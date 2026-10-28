"""DEAD MAN'S ALGORITHM, Chapter 1: "12:17" (the long video, 16:9). The owner's story bible:
channels/stories/dead_mans_algorithm_bible.md. Auto-approved by the owner, 27 Oct 2026.

All twelve Chapter 1 beats in order: lunch at 12:16 (Ren, Haruto, Yui), Riku bullying Kota and Go stepping in, Aoi and
Mio, the meteor, the impact and the eye, waking underground (twenty students, the teacher missing), the cameras, the
screen (20 SURVIVORS), EVENT 00, Momo, the Glass Auction with its five rules read word for word, and the class facing
the countdown, ending on the hook into Chapter 2 (Ren already knows his number). Nothing beyond the bible is made
canon: the teacher has no name, the twelve other students stay unnamed, the auction is not resolved.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_long   -> out/stories/dma_long.mp4 (1280x720)
"""
import os

from motion import audio, satsuei, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import dma_anime, dma_art, serial
from channels.stories import dma_s1 as S1      # notebook, phone, the eye close-up
from channels.stories import dma_s2 as S2      # the room, rule cards, countdown format

A = dma_art if os.environ.get("ANIME") == "0" else dma_anime     # ANIME=0: the old vector look (for comparisons)

NARRATOR = dict(turbo=True, turbo_ref="am_echo")
TAIL = 2.5
MUSIC = "horror"
TWIST = "c26"
voice.SPEAKERS.update({
    "haruto": dict(voice="am_puck", turbo_ref="am_puck"),
    "yui": dict(voice="af_heart", turbo_ref="af_heart"),
    "riku": dict(voice="am_fenrir", turbo_ref="am_fenrir"),
    "kota": dict(voice="am_eric", turbo_ref="am_eric+1"),
    "go": dict(voice="am_onyx", turbo_ref="am_onyx-1"),
    "aoi": dict(voice="af_kore", turbo_ref="af_kore"),
    "mio": dict(voice="af_bella", turbo_ref="af_bella"),
    "momo": dict(voice="af_sky", turbo_ref="af_sky+5"),
})
audio.GAINS.update(thunder=0.5, sting=0.6, chime=0.7, static=0.35, drip=0.4, click=0.6)

SCRIPT = [
    # cold open
    dict(id="c1", scene="cold", text="At [twelve seventeen,|12:17,] a meteor hit my school."),
    dict(id="c2", scene="cold", text="Twenty of us woke up underground."),
    dict(id="c3", scene="cold", text="Our teacher didn't. And inside that meteor, I saw something I still can't "
                                     "explain.", gap=0.3),
    # 12:16
    dict(id="c4", scene="class", text="[Twelve sixteen.|12:16.] One minute before the end of the world, Class "
                                      "[three B|3-B] was arguing about lunch.", gap=2.2),   # the title card plays first
    dict(id="c5", scene="class", text="Ren. Ren. If the world ends today, I'm eating your lunch.", speaker="haruto"),
    dict(id="c6", scene="class", text="You say that every day."),
    dict(id="c7", scene="class", text="And one day I'll be right.", speaker="haruto"),
    dict(id="c8", scene="class", text="Haruto! Give it back. He hasn't even eaten.", speaker="yui"),
    dict(id="c9", scene="class", text="Yui always takes my side. I've never asked her why."),
    dict(id="c10", scene="class", text="Escape plans again, Kota?", speaker="riku", gap=0.6),
    dict(id="c11", scene="class", text="Escape from what, loser? Math class?", speaker="riku"),
    dict(id="c12", scene="class", text="Please give it back.", speaker="kota"),
    dict(id="c13", scene="class", text="Make me.", speaker="riku"),
    dict(id="c14", scene="class", text="That's enough, Riku.", speaker="go", gap=0.6),
    dict(id="c15", scene="class", text="Go doesn't talk much. He doesn't need to."),
    dict(id="c16", scene="class", text="Relax, big guy. It's a joke.", speaker="riku"),
    dict(id="c17", scene="class", text="Don't get involved, Ren. It never ends well.", speaker="mio"),
    dict(id="c18", scene="class", text="Mio always knows who's about to lose. That's why she never picks a side."),
    dict(id="c19", scene="class", text="That cloud is moving against the wind.", speaker="aoi", gap=0.5),
    dict(id="c20", scene="class", text="Clouds can do that?", speaker="haruto"),
    dict(id="c21", scene="class", text="No. It's not a cloud.", speaker="aoi", gap=0.4),
    dict(id="c22", scene="class", text="Everyone went to the windows. Phones came out."),
    dict(id="c23", scene="class", text="It wasn't moving across the sky. It was coming straight at us."),
    dict(id="c24", scene="class", text="Ren?", speaker="yui"),
    dict(id="c25", scene="class", text="[Twelve sixteen and fifty-nine seconds.|12:16 and 59 seconds.]"),
    dict(id="c26", scene="eye", text="And in the last second, inside the fire, I saw it. A shape, like an eye. "
                                     "Looking back at me.", gap=0.4),
    # underground
    dict(id="c27", scene="chamber", text="Cold. That's the first thing I remember. Concrete under my cheek.",
         gap=2.4),                                         # the impact, then black
    dict(id="c28", scene="chamber", text="Then the light, flickering, like it couldn't decide whether to let us see."),
    dict(id="c29", scene="chamber", text="Ren? Ren, are you alive?", speaker="haruto"),
    dict(id="c30", scene="chamber", text="I think so.", gap=0.4),
    dict(id="c31", scene="chamber", text="I counted. I always count. Eighteen. Nineteen. Twenty. All of Class "
                                         "[three B.|3-B.]"),
    dict(id="c32", scene="chamber", text="Where's our teacher?", speaker="yui"),
    dict(id="c33", scene="chamber", text="Our teacher had been standing at the front of the room. Now there was "
                                         "no one."),
    dict(id="c34", scene="chamber", text="No signal. Nothing.", speaker="haruto"),
    dict(id="c35", scene="chamber", text="The door's sealed.", speaker="go"),
    dict(id="c36", scene="chamber", text="Then somebody open it! Hey! We're down here!", speaker="riku"),
    dict(id="c37", scene="chamber", text="Stop shouting. Look up.", speaker="aoi", gap=0.5),
    dict(id="c38", scene="chamber", text="Cameras. Four of them. All watching us.", speaker="aoi"),
    dict(id="c39", scene="chamber", text="They turned. All four. At the same time."),
    dict(id="c40", scene="chamber", text="Then the screen came on.", gap=0.4),
    dict(id="c41", scene="screen", text="Survivors.", speaker="kota", gap=1.2),
    dict(id="c42", scene="screen", text="Someone expects us not to be.", speaker="aoi"),
    dict(id="c43", scene="screen", text="Then a second line.", gap=0.4),
    dict(id="c44", scene="screen", text="Status of Earth, unknown?", speaker="mio", gap=1.0),
    dict(id="c45", scene="screen", text="Our families...", speaker="yui", gap=0.4),
    # Momo
    dict(id="c46", scene="momo", text="Good afternoon, Class [three B!|3-B!]", speaker="momo", gap=0.8),
    dict(id="c47", scene="momo", text="I'm Momo, your administrator! Welcome to Dead Man's Algorithm!",
         speaker="momo"),
    dict(id="c48", scene="momo", text="What the hell is that? A mascot?", speaker="riku", gap=0.4),
    dict(id="c49", scene="momo", text="Rude! But don't worry. I like rude ones.", speaker="momo"),
    dict(id="c50", scene="momo", text="It's time for game one! The Glass Auction!", speaker="momo", gap=0.6),
    dict(id="c51", scene="momo", text="Twenty players. One hundred tokens each. Ten minutes. And one exit key!",
         speaker="momo", gap=0.6),
    dict(id="c52", scene="rule", text="Rule one. The highest unique bid wins the key.", speaker="momo", gap=0.4),
    dict(id="c53", scene="rule", text="Rule two. All spent tokens are permanently lost.", speaker="momo"),
    dict(id="c54", scene="rule", text="Rule three. If multiple players submit the same highest bid, every player "
                                      "tied at that amount is eliminated.", speaker="momo"),
    dict(id="c55", scene="rule", text="Rule four. If the highest bid is tied, the next highest unique bid wins.",
         speaker="momo"),
    dict(id="c56", scene="rule", text="Rule five. If everyone leaves all tokens unspent when time expires, everyone "
                                      "is executed!", speaker="momo"),
    dict(id="c57", scene="momo", text="Ten minutes! Starting now!", speaker="momo", gap=0.6),
    # the countdown
    dict(id="c58", scene="talk", text="Easy. I bid all hundred. Nobody beats a hundred.", speaker="riku", gap=0.8),
    dict(id="c59", scene="talk", text="Unless someone else bids a hundred. Then you're both eliminated.",
         speaker="aoi", gap=0.4),
    dict(id="c60", scene="talk", text="So we all bid zero and go home?", speaker="haruto", gap=0.5),
    dict(id="c61", scene="talk", text="Then rule five executes all of us.", speaker="kota", gap=0.4),
    dict(id="c62", scene="talk", text="So somebody has to bid. And everyone will remember who.", speaker="mio",
         gap=0.5),
    dict(id="c63", scene="talk", text="We do this together. All of us.", speaker="go", gap=0.5),
    dict(id="c64", scene="ren", text="Twenty people. Twenty numbers. One key."),
    dict(id="c65", scene="ren", text="Bid too high, and you might tie. Bid too low, and someone beats you."),
    dict(id="c66", scene="ren", text="I looked at Yui. At Haruto. At the countdown."),
    dict(id="c67", scene="ren", text="And I realised the safest number in this room might not be a hundred.",
         gap=0.6),
    dict(id="c68", scene="ren", text="I already knew my number.", gap=0.5),
    dict(id="c69", scene="momo", text="Tick tock, Class [three B!|3-B!]", speaker="momo", gap=0.3),
]
METADATA = dict(
    title="A Meteor Hit Our School at 12:17. Then the Game Began. | Dead Man's Algorithm, Chapter 1",
    alt_titles=["20 Students Woke Up Underground. One Key. 100 Tokens Each. | Dead Man's Algorithm Ch. 1",
                "Dead Man's Algorithm, Chapter 1: 12:17"],
    description="""12:16. Lunch in Class 3-B. One minute later, a meteor hits the school, and twenty students wake up in an underground facility. Their teacher is gone. Their phones have no signal. Four cameras are watching. And a cheerful little administrator called Momo has a game for them.

THE GLASS AUCTION
• 20 players · 100 tokens each · 10 minutes · 1 exit key
• Rule 1: The highest unique bid wins the key.
• Rule 2: All spent tokens are permanently lost.
• Rule 3: If multiple players submit the same highest bid, every player tied at that amount is eliminated.
• Rule 4: If the highest bid is tied, the next-highest unique bid wins.
• Rule 5: If everyone leaves all tokens unspent when time expires, everyone is executed.

Ren already knows his number. Chapter 2 is next.

Dead Man's Algorithm is an original story. Anime-style animation.""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Anime"],
    tags=["dead mans algorithm", "survival game", "death game", "psychological thriller", "game theory",
          "anime story", "original story", "meteor", "class 3-b", "chapter 1", "2d animation"],
    pinned_comment="Chapter 1 of Dead Man's Algorithm. I'd bid 1: everyone scared of ties goes high. What's your "
                   "number?",
)

KEY = S1.KEY | S2.KEY | {"teacher", "eye", "count", "twenty", "sealed", "families", "rude", "together"}
ORANGE = S1.ORANGE
CYAN = S2.CYAN

# what each line shows: (kind, ...) ; kinds: cold, title, class (whos), window, faces, eye, black, floor, wake (whos),
# chamber (whos), cameras, screen (lines), momo, rule n, countdown, talk (whos), ren, momo_close
SHOT = {
    "c1": ("cold",), "c2": ("floor",), "c3": ("cold",),
    "c4": ("class_wide",), "c5": ("class", [("ren", "focus"), ("haruto", "grin")]),
    "c6": ("class", [("ren", "calm"), ("haruto", "grin")]), "c7": ("class", [("haruto", "grin"), ("yui", "smile")]),
    "c8": ("class", [("yui", "smile")]), "c9": ("class", [("ren", "calm"), ("yui", "smile")]),
    "c10": ("class", [("kota", "worry"), ("riku", "smirk")]), "c11": ("notebook",),
    "c12": ("class", [("kota", "fear")]), "c13": ("class", [("riku", "smirk")]),
    "c14": ("class", [("riku", "worry"), ("go", "angry")]), "c15": ("class", [("go", "angry")]),
    "c16": ("class", [("riku", "smirk"), ("kota", "worry")]), "c17": ("class", [("ren", "calm"), ("mio", "smirk")]),
    "c18": ("class", [("mio", "calm")]), "c19": ("class_meteor", [("aoi", "focus")]),
    "c20": ("class_meteor", [("haruto", "worry"), ("aoi", "focus")]), "c21": ("window",),
    "c22": ("faces",), "c23": ("window",), "c24": ("class_meteor", [("yui", "fear")]), "c25": ("faces",),
    "c26": ("eye",),
    "c27": ("floor",), "c28": ("wake", [("ren", "worry")]), "c29": ("wake", [("haruto", "worry")]),
    "c30": ("wake", [("ren", "worry"), ("haruto", "worry")]), "c31": ("count",),
    "c32": ("chamber", [("yui", "fear")]), "c33": ("chamber", [("ren", "worry")]), "c34": ("phone",),
    "c35": ("door",), "c36": ("chamber", [("riku", "angry")]), "c37": ("chamber", [("aoi", "focus")]),
    "c38": ("cameras",), "c39": ("cameras",), "c40": ("screen", ["CLASS 3-B", "20 STUDENTS", "20 SURVIVORS"]),
    "c41": ("chamber", [("kota", "fear")]), "c42": ("chamber", [("aoi", "worry")]),
    "c43": ("screen", ["EVENT 00: IMPACT", "STATUS OF EARTH:", "UNKNOWN"]), "c44": ("chamber", [("mio", "shock")]),
    "c45": ("chamber", [("yui", "sad")]), "c46": ("momo",), "c47": ("momo",), "c48": ("chamber", [("riku", "angry")]),
    "c49": ("momo_close",), "c50": ("room",), "c51": ("room",),
    "c52": ("rule", 1, "riku"), "c53": ("rule", 2, "kota"), "c54": ("rule", 3, "aoi"), "c55": ("rule", 4, "haruto"),
    "c56": ("rule", 5, "yui"), "c57": ("countdown",),
    "c58": ("talk", [("riku", "smirk")]), "c59": ("talk", [("riku", "worry"), ("aoi", "focus")]),
    "c60": ("talk", [("haruto", "grin")]), "c61": ("talk", [("kota", "fear")]), "c62": ("talk", [("mio", "calm")]),
    "c63": ("talk", [("go", "focus"), ("yui", "worry")]), "c64": ("ren",), "c65": ("ren",),
    "c66": ("look",), "c67": ("ren",), "c68": ("ren",), "c69": ("momo_close",),
}
NAMED = {"c5": "haruto", "c6": "ren", "c8": "yui", "c10": "riku", "c12": "kota", "c14": "go", "c17": "mio",
         "c19": "aoi"}


def camera(cr, t, s0, s1, z0=1.0, z1=1.05, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def busts(cr, t, tl, whos, look_up=False, rim=None, rim_from=(9, 0), scale=None):
    """One, two or three students across the 16:9 frame, faces clear of the captions."""
    n = len(whos)
    xs = {1: [0.5], 2: [0.33, 0.67], 3: [0.22, 0.5, 0.78]}[n]
    s = scale or {1: 1.05, 2: 0.9, 3: 0.78}[n]
    neck = H * 0.94 if n == 1 else H * 0.96
    for j, (who, e) in enumerate(whos):
        lk = (0, -0.6) if look_up else ((0.5 if xs[j] < 0.5 else -0.5) if n > 1 else 0.15, 0.05)
        A.student_bust(cr, W * xs[j], neck, s, t, who, e, look=lk, talk=1.0 if tl.speaking(who, t) else 0.0,
                       rim=rim, rim_from=rim_from, sweat=0.6 if e == "fear" else 0.0)


def shots(tl):
    """One shot per line, with a few extra cuts inside the long lines."""
    out = []
    for d in SCRIPT:
        b = tl.by_id[d["id"]]
        out.append((b.start - 0.15, d["id"]))
    out.insert(3, (tl.by_id["c3"].end + 0.3, "title"))
    extra = [(tl.at("c26", "A"), "c26b"), (tl.at("c31", "Eighteen."), "c31b"), (tl.by_id["c26"].end + 0.35, "black"),
             (tl.at("c22", "Phones"), "c22b")]
    out = sorted(out + extra)
    out.append((tl.total + 1, "end"))
    return out


_shots = {}
SHOT.update({"c26b": ("eye",), "c31b": ("count",), "c22b": ("faces",), "title": ("title",), "black": ("black",)})


def draw(cr, t, tl):
    A_, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, sid, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    spec = SHOT[sid]
    kind = spec[0]
    t_flash = A_("c26", "A") + 0.05
    t_boom = B["c26"].end + 0.35
    t_c4 = B["c4"].start
    meteor = clamp01((t - B["c19"].start) / max(1.0, t_flash - B["c19"].start)) if t >= B["c19"].start else 0.0
    if t < t_c4:
        clk = (12, 16, 58)
    elif t >= t_flash:
        clk = (12, 17, 0)
    else:
        clk = (12, 16, min(59, int(60 * (t - t_c4) / (t_flash - t_c4))))
    left = S2.countdown(t, _CountdownTL(tl))

    cr.save()
    if kind == "cold":
        camera(cr, t, s0, s1, 1.02, 1.1, shake=1.5)
        hud2d.blurred(cr, lambda c: A.classroom(c, t, 0.85, (12, 16, 58)), sigma=8)
        busts(cr, t, tl, [("ren", "shock" if sid == "c1" else "fear")], look_up=False, rim=ORANGE + (0.8,),
              rim_from=(-10, -6))
        glow(cr, 0, 100, 800, ORANGE, 0.35)
    elif kind == "title":
        cr.set_source_rgba(0.02, 0.02, 0.03, 1)
        cr.paint()
        p = seg(t, s0, s0 + 0.4)
        hud2d._text(cr, "DEAD MAN'S", W / 2, H * 0.42, 92, (1, 1, 1, p), hud2d.ROUND, "center", outline=INK, ow=10)
        hud2d._text(cr, "ALGORITHM", W / 2, H * 0.56, 92, (*hud2d.RED[:3], p), hud2d.ROUND, "center", outline=INK,
                    ow=10)
        hud2d._text(cr, "CHAPTER 1 · 12:17", W / 2, H * 0.68, 32, (1, 1, 1, 0.8 * p), "Liberation Mono", "center")
        A.the_eye(cr, t, W / 2, H * 0.2, 46, a=0.5 * p)
    elif kind == "class_wide":
        camera(cr, t, s0, s1, 1.0, 1.04)
        A.classroom(cr, t, 0.0, clk)
        for j, who in enumerate(("mio", "go", "riku", "kota")):     # the room behind
            A.student_bust(cr, W * (0.58 + j * 0.11), H * 0.98, 0.42, t, who, "calm", look=(-0.3, 0))
        busts(cr, t, tl, [("haruto", "grin"), ("ren", "calm"), ("yui", "smile")], scale=0.62)
    elif kind in ("class", "class_meteor"):
        camera(cr, t, s0, s1, 1.0, 1.05, shake=1.3 if sid in ("c10", "c13", "c14") else 1.0)
        m = meteor if kind == "class_meteor" else 0.0
        hud2d.blurred(cr, lambda c: A.classroom(c, t, m, clk), sigma=9)
        busts(cr, t, tl, spec[1], rim=ORANGE + (0.6 * m,) if m else None, rim_from=(-10, -6))
    elif kind == "notebook":
        camera(cr, t, s0, s1, 1.0, 1.08)
        hud2d.blurred(cr, lambda c: A.classroom(c, t, 0.0, clk), sigma=14)
        S1.notebook(cr, t, W / 2, H * 0.48, 1.1)
    elif kind == "window":
        camera(cr, t, s0, s1, 1.0, 1.15, cx=W * 0.2, cy=H * 0.3, shake=1.5)
        A.classroom(cr, t, meteor, clk)
    elif kind == "faces":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=2.5)
        hud2d.blurred(cr, lambda c: A.classroom(c, t, meteor, clk), sigma=12)
        for who, x, s, e in (("kota", 0.1, 0.55, "fear"), ("mio", 0.9, 0.55, "shock"), ("haruto", 0.28, 0.7, "shock"),
                             ("yui", 0.72, 0.7, "fear"), ("ren", 0.5, 0.82, "shock")):
            A.student_bust(cr, W * x, H * 0.98, s, t, who, e, look=(-0.5, -0.6), rim=ORANGE + (0.9,),
                           rim_from=(-10, -8))
        glow(cr, 0, 0, 900, ORANGE, 0.45 * meteor)
    elif kind == "eye":
        camera(cr, t, s0, s1, 1.0, 1.2, shake=1.0)
        S1.eye_shot(cr, t, seg(t, A_("c26", "A"), B["c26"].end))
    elif kind == "black":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    elif kind == "floor":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=0.6)
        A.lying_students(cr, t, stir=1.0 if sid == "c27" else 0.0)
        grade(cr, (0.7, 0.75, 0.85), (0.35, 0.36, 0.42))
    elif kind in ("wake", "chamber"):
        camera(cr, t, s0, s1, 1.02, 1.08)
        hud2d.blurred(cr, lambda c: A.chamber(c, t, screen=A.screen_text(["20 SURVIVORS"])
                                              if t >= B["c40"].end else None), sigma=8)
        busts(cr, t, tl, spec[1], rim=(0.8, 0.9, 1, 0.5), rim_from=(0, -8))
    elif kind == "count":
        camera(cr, t, s0, s1, 1.0, 1.04)
        A.chamber(cr, t)
        n = 20 if sid == "c31b" else 17
        for j in range(n):                                      # all of them, row by row, as Ren counts
            row, col = divmod(j, 10)
            who = (["ren", "haruto", "yui", "riku", "kota", "go", "aoi", "mio"] + list(range(12)))[j]
            A.student_bust(cr, W * (0.06 + col * 0.098) + row * 30, H * (0.66 + row * 0.26), 0.3, t, who, "worry",
                           look=(0, -0.2))
        if sid == "c31b":
            p = seg(t, s0, B["c31"].end)
            hud2d._text(cr, f"{min(20, 18 + int(p * 3))} / 20", W * 0.86, H * 0.2, 60, hud2d.YELLOW, hud2d.ROUND,
                        "center", outline=INK, ow=8)
    elif kind == "phone":
        camera(cr, t, s0, s1, 1.0, 1.06)
        hud2d.blurred(cr, lambda c: A.chamber(c, t), sigma=10)
        A.student_bust(cr, W * 0.66, H * 0.96, 0.95, t, "haruto", "worry", look=(-0.5, 0.3),
                       talk=1.0 if tl.speaking("haruto", t) else 0.0)
        S1.phone(cr, t, W * 0.3, H * 0.5, 0.8)
    elif kind == "door":
        camera(cr, t, s0, s1, 1.0, 1.1, cx=W * 0.86, cy=H * 0.5)
        A.chamber(cr, t)
        A.student_bust(cr, W * 0.68, H * 0.98, 0.85, t, "go", "focus", look=(0.7, 0),
                       talk=1.0 if tl.speaking("go", t) else 0.0)
    elif kind == "cameras":
        camera(cr, t, s0, s1, 1.0, 1.06)
        A.chamber(cr, t)
        turn = 0.4 * seg(t, B["c39"].start, B["c39"].start + 0.6)
        for cx, cy, sx in ((W * 0.2, H * 0.24, 1), (W * 0.8, H * 0.24, -1)):
            A.camera_unit(cr, t, cx, cy, sx, 1.1, turn=turn)
        busts(cr, t, tl, [("aoi", "worry")], look_up=True, scale=0.8)
    elif kind == "screen":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=H * 0.3)
        col = (1, 0.45, 0.35, 1) if spec[1][0].startswith("EVENT") else CYAN
        A.chamber(cr, t, screen=A.screen_text(spec[1], col=col))
        for j, who in enumerate(("kota", "riku", "ren", "yui", "go", "mio", "aoi")):
            A.student_bust(cr, W * (0.08 + j * 0.14), H * 1.06, 0.48, t, who, "worry", look=(0, -0.8))
    elif kind in ("momo", "room"):
        camera(cr, t, s0, s1, 1.0, 1.05, cy=H * 0.3)
        pop = seg(t, B["c46"].start - 0.3, B["c46"].start + 0.3)
        if kind == "room":
            S2.room(cr, t, 600, ["GAME 01", "THE GLASS AUCTION"], momo_at=1.0)
        else:
            A.chamber(cr, t, screen=A.screen_text([" "], momo_at=pop, t=t))
        for j, who in enumerate(("mio", "haruto", "ren", "yui", "aoi", "riku", "go")):
            A.student_bust(cr, W * (0.08 + j * 0.14), H * 1.06, 0.48, t, who, "shock", look=(0, -0.8))
    elif kind == "momo_close":
        camera(cr, t, s0, s1, 1.0, 1.12, cy=H * 0.6)
        hud2d.blurred(cr, lambda c: A.chamber(c, t), sigma=10)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
        A.momo(cr, W / 2, H * 0.98, 2.4 + 0.3 * seg(t, s0, s0 + 0.8), t,
               mood="wink" if sid == "c69" else "sly", lean=0.08 * seg(t, s0, s0 + 0.8))
    elif kind == "rule":
        camera(cr, t, s0, s1, 1.0, 1.04)
        hud2d.blurred(cr, lambda c: S2.room(c, t, 600, ["GAME 01", "THE GLASS AUCTION"]), sigma=8)
        A.student_bust(cr, W * 0.82, H * 0.98, 0.7, t, spec[2], "worry", look=(-0.6, -0.2))
    elif kind == "countdown":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=H * 0.3, shake=0.6)
        S2.room(cr, t, left, ["TIME LEFT", S2.fmt(left)])
    elif kind == "talk":
        camera(cr, t, s0, s1, 1.02, 1.08, shake=1.2 if sid == "c58" else 1.0)
        hud2d.blurred(cr, lambda c: S2.room(c, t, left, ["TIME LEFT", S2.fmt(left)]), sigma=9)
        busts(cr, t, tl, spec[1])
    elif kind in ("ren", "look"):
        camera(cr, t, s0, s1, 1.03, 1.12, cy=H * 0.55)
        hud2d.blurred(cr, lambda c: S2.room(c, t, left, ["TIME LEFT", S2.fmt(left)]), sigma=10)
        cr.set_source_rgba(0, 0.02, 0.03, 0.35)
        cr.paint()
        if kind == "look":
            busts(cr, t, tl, [("yui", "worry"), ("ren", "focus"), ("haruto", "worry")])
        else:
            busts(cr, t, tl, [("ren", "focus")], rim=(0.5, 1, 0.9, 0.6), rim_from=(10, -6))
            S2.numbers(cr, t, 1.0 if sid != "c67" else 0.3)
    cr.restore()

    if kind not in ("black", "title"):
        if A is dma_anime:                                      # satsuei: glow, light, aberration, grain
            satsuei.apply(cr, t, glow=0.24, light=((0.1, 0.1), (1.0, 0.85, 0.7), 0.14),
                          shade=((0.5, 0.3), (0.35, 0.3, 0.45), 0.3), ca=1.0, grain=0.03)
            hud.finish(cr, t, flash_at=[], vig=0.4, grain=0.0)
        else:
            hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.05)
    A.flash(cr, t, t_flash, 0.35)
    A.flash(cr, t, t_boom, 0.25)
    if kind == "rule":
        n = spec[1]
        S2.rule_card(cr, t, B[sid].start + 0.05, B[sid].end + 0.1, n, S2.RULES[n - 1])
    for lid, who in NAMED.items():
        A.name_card(cr, t, B[lid].start, B[lid].end + 0.3, who, y=H * 0.2,
                    side=1 if SHOT[lid][1][-1][0] != who or len(SHOT[lid][1]) == 1 else -1)
    if B["c46"].start <= t <= B["c47"].end:
        A.NAMES.setdefault("momo", ("MOMO", "administrator"))
        A.name_card(cr, t, B["c46"].start + 0.4, B["c47"].end, "momo", y=H * 0.2, side=-1)
    started = t >= A_("c57", "now!", end=True)
    after = t >= t_boom
    if t >= B["c4"].start - 0.2 or t < B["c3"].end + 0.3:
        h, m, sec = clk
        A.status_bar(cr, t, ("GAME 01 · THE GLASS AUCTION" if t >= B["c50"].start else
                             f"CLASS 3-B · {h}:{m:02d}:{sec:02d}" if not after else "CLASS 3-B · ??:??:??"),
                     S2.fmt(left) if started else ("IMPACT" if t_flash <= t < B["c27"].start else
                                                   ("STATUS: UNKNOWN" if after else None)), alert=t >= t_flash)
    hud2d.hook(cr, t, [("12:17.", False), ("THE SKY FELL ON US.", True)], end=B["c3"].end + 0.1, y=H * 0.3, size=70)
    hud2d.stamp(cr, t, B["c4"].start - 0.1, A_("c4", "One") + 0.6, ["1 MINUTE EARLIER"], x=W * 0.5, y=H * 0.3,
                col=hud2d.YELLOW)
    if t < B["c69"].end + 0.1 and kind not in ("rule", "title"):
        hud2d.captions(cr, t, tl, KEY, y=H * 0.93, size=40, max_w=W * 0.7)
    serial.next_card(cr, t, B["c69"].end + 0.1, "DEAD MAN'S ALGORITHM", "CHAPTER 2", "THE BIDS")
    cue("thunder", t, 0.0, 3.5)
    cue("riser", t, B["c23"].start, t_flash - B["c23"].start)
    cue("sting", t, t_boom)
    cue("drip", t, B["c27"].start - 0.6)
    cue("hum", t, B["c27"].start, A_("c57", "now!") - B["c27"].start)
    cue("click", t, B["c39"].start - 0.2)
    cue("static", t, B["c40"].end + 0.02, 0.3)
    cue("chime", t, B["c46"].start - 0.6)
    for lid in ("c52", "c53", "c54", "c55", "c56"):
        cue("click", t, B[lid].start - 0.15)
    cue("sting", t, A_("c57", "now!", end=True) + 0.05)
    cue("heartbeat", t, B["c64"].start, B["c67"].end - B["c64"].start)


class _CountdownTL:
    """Lets dma_s2.countdown read this script's lines: "now!" is c57 here, and Ren never reads a time aloud, so the
    clock runs at 4.8x (the same in-world speed as Short 2) from c57 to the end."""
    def __init__(self, tl):
        self.tl = tl
        self.by_id = {"g16": type("b", (), {"start": tl.by_id["c67"].start})()}

    def at(self, bid, key=None, end=False, nth=1):
        return self.tl.at("c57", "now!", end=True)
