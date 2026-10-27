"""DEAD MAN'S ALGORITHM, Short 1: "12:17" (9:16). The owner's story (channels/stories/dead_mans_algorithm_bible.md);
script channels/stories/dma_s1_script.md, auto-approved by the owner on 27 Oct 2026 ("Both auto approved").

Chapter 1 beats 1-10 in canon order, told by Ren: a cold open at the impact, then one minute earlier (a clock ticks
12:16:00 -> 12:17:00 on screen), the cast with name cards, the meteor and the eye, waking underground, the screen,
EVENT 00, Momo. Ends with Momo asking the viewer who breaks first.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_s1   -> out/stories/dma_s1.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the effects)
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import dma_art as A

NARRATOR = dict(turbo=True, turbo_ref="am_echo")       # Ren tells it
TAIL = 2.0
MUSIC = "horror"
TWIST = "d12"
voice.SPEAKERS.update({
    "haruto": dict(voice="am_puck", turbo_ref="am_puck"),
    "yui": dict(voice="af_heart", turbo_ref="af_heart"),
    "riku": dict(voice="am_fenrir", turbo_ref="am_fenrir"),
    "go": dict(voice="am_onyx", turbo_ref="am_onyx-1"),
    "aoi": dict(voice="af_kore", turbo_ref="af_kore"),
    "mio": dict(voice="af_bella", turbo_ref="af_bella"),
    "momo": dict(voice="af_sky", turbo_ref="af_sky+5"),
})
audio.GAINS.update(thunder=0.5, sting=0.6, chime=0.7, static=0.35, drip=0.4)

SCRIPT = [
    dict(id="d1", scene="cold", text="At [twelve seventeen,|12:17,] a meteor hit my school."),
    dict(id="d2", scene="cold", text="Twenty of us woke up underground. And I saw something inside it."),
    dict(id="d3", scene="class", text="One minute earlier. Class [three B.|3-B.] Lunch.", gap=0.6),
    dict(id="d4", scene="class", text="Ren, if the world ends today, I'm eating your lunch.", speaker="haruto"),
    dict(id="d5", scene="class", text="Haruto! Give it back.", speaker="yui"),
    dict(id="d6", scene="class", text="Escape plans again, Kota? Escape from what, loser?", speaker="riku", gap=0.5),
    dict(id="d7", scene="class", text="That's enough, Riku.", speaker="go"),
    dict(id="d8", scene="class", text="Don't get involved. It never ends well.", speaker="mio"),
    dict(id="d9", scene="class", text="That cloud is moving against the wind.", speaker="aoi"),
    dict(id="d10", scene="class", text="It's not a cloud.", speaker="aoi", gap=0.4),
    dict(id="d11", scene="class", text="It was coming straight at us."),
    dict(id="d12", scene="eye", text="And inside the fire, something looked back at me.", gap=0.3),
    dict(id="d13", scene="chamber", text="I woke up on cold concrete. All twenty of us. Our teacher was gone.",
         gap=1.4),                                        # the impact and the black land in this silence
    dict(id="d14", scene="chamber", text="No signal. Nothing.", speaker="haruto"),
    dict(id="d15", scene="chamber", text="Cameras. Four of them. All watching us.", speaker="aoi"),
    dict(id="d16", scene="chamber", text="Then the screen came on."),
    dict(id="d17", scene="chamber", text="Survivors. Someone expects us not to.", speaker="aoi", gap=0.5),
    dict(id="d18", scene="chamber", text="Event zero. Impact. Status of Earth: unknown."),
    dict(id="d19", scene="momo", text="Good afternoon, Class [three B!|3-B!] I'm Momo, your administrator!",
         speaker="momo", gap=0.6),
    dict(id="d20", scene="momo", text="Welcome to Dead Man's Algorithm!", speaker="momo"),
    dict(id="d21", scene="momo", text="And you, watching. Who do you think breaks first?", speaker="momo", gap=0.4),
]

METADATA = dict(
    title="A Meteor Hit Our School at 12:17. We Woke Up Underground. ☄️",
    alt_titles=["20 Students. 20 Survivors. For Now. ☄️", "Dead Man's Algorithm, Part 1: 12:17 ☄️"],
    description="""12:16. Lunch in Class 3-B. One minute later, a meteor hits the school, and twenty students wake up underground. ☄️

Cameras. No signal. A screen that says 20 SURVIVORS. And a cheerful little mascot called Momo.

Dead Man's Algorithm, Part 1: 12:17. Part 2: The Glass Auction.
💬 Who do you think breaks first? Comment a name. 👇

(Original story. 2D animation.)""",
    hashtags=["#DeadMansAlgorithm", "#SurvivalGame", "#Shorts"],
    tags=["dead mans algorithm", "survival game", "psychological thriller", "anime story", "death game", "meteor",
          "class 3-b", "mystery", "2d animation", "part 1"],
    pinned_comment="My bet: Riku breaks first. People who need to control everyone crack when nobody's scared of "
                   "them. Who's yours? 👇 (Pause on Kota's notebook 👀)",
)

KEY = {"meteor", "underground", "twenty", "inside", "lunch", "world", "escape", "loser", "enough", "involved", "wind",
       "cloud", "straight", "looked", "concrete", "gone", "signal", "cameras", "watching", "screen", "survivors",
       "expects", "unknown", "momo", "administrator", "algorithm", "breaks"}
ORANGE = (1.0, 0.62, 0.3)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def bg_class(cr, t, meteor=0.0, clock=(12, 16, 0), blur=9):
    hud2d.blurred(cr, lambda c: A.classroom(c, t, meteor, clock), sigma=blur)


def notebook(cr, t, x, y, s):
    """Kota's notebook, open: hand-drawn floor plans, arrows, numbered exits (his survival plans)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(-0.06)
    A.toon(cr, lambda c: c.rectangle(-220, -150, 440, 300), A.hexa("#f4f1e8"), A.hexa("#d6d0bf"), (-3, -3), None)
    cr.set_source_rgba(0.55, 0.65, 0.85, 0.4)
    cr.set_line_width(1.5)
    for k in range(12):
        cr.move_to(-210, -130 + k * 24)
        cr.line_to(210, -130 + k * 24)
    cr.stroke()
    cr.set_source_rgba(0.15, 0.18, 0.35, 0.9)                 # a floor plan in pencil
    cr.set_line_width(3)
    cr.rectangle(-190, -110, 170, 120)
    cr.rectangle(-20, -110, 90, 60)
    cr.move_to(-190, 40)
    cr.line_to(70, 40)
    cr.stroke()
    cr.set_line_width(2.5)
    for ax, ay in ((-100, -40), (20, -80)):                    # arrows toward the exits
        cr.move_to(ax, ay)
        cr.line_to(ax + 60, ay + 10)
        cr.line_to(ax + 48, ay)
        cr.stroke()
    A.hud2d._text(cr, "EXIT 1", 90, -60, 26, (0.15, 0.18, 0.35, 1), "Kalam")
    A.hud2d._text(cr, "EXIT 2", 90, 20, 26, (0.15, 0.18, 0.35, 1), "Kalam")
    A.hud2d._text(cr, "PLAN 7", -190, 100, 34, (0.6, 0.1, 0.1, 1), "Kalam")
    cr.restore()


def phone(cr, t, x, y, s):
    """Haruto's phone, held up: NO SERVICE."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    A.toon(cr, lambda c: A.tk.tk_rrect(c, -110, -200, 220, 400, 26), A.hexa("#1a1c20"), None, (0, 0), None, lw=5)
    cr.set_source_rgba(0.06, 0.08, 0.12, 1)
    A.tk.tk_rrect(cr, -96, -184, 192, 368, 18)
    cr.fill()
    glow(cr, 0, -40, 160, (0.6, 0.75, 1), 0.2)
    A.hud2d._text(cr, "NO SERVICE", 0, -60, 30, (1, 0.35, 0.3, 1), A.hud2d.ROUND, "center")
    for k in range(4):                                         # empty signal bars
        cr.set_source_rgba(1, 1, 1, 0.25)
        cr.rectangle(-36 + k * 20, -110 - k * 10, 12, 14 + k * 10)
        cr.fill()
    A.hud2d._text(cr, "12:17", 0, 40, 44, (1, 1, 1, 0.85), "Liberation Sans", "center")
    cr.restore()


def eye_shot(cr, t, k):
    """Ren's eye, extreme close-up; in it, the reflection of the shape inside the meteor."""
    cr.set_source_rgba(*A.mix(A.CAST["ren"]["skin"], ORANGE + (1,), 0.5))
    cr.paint()
    cr.save()
    cr.translate(W / 2, H * 0.5)
    sc = (W / 100) * (1.0 + 0.1 * k)
    cr.scale(sc, sc)
    A.anime_eye(cr, 0, 0, 1, 40, 46, 1.0, (0, 0), A.CAST["ren"]["iris"], fear=0.3, tired=False)
    cr.restore()
    A.the_eye(cr, t, W / 2 + W * 0.05, H * 0.47, W * 0.11, a=clamp01(k * 1.5))
    glow(cr, W / 2, H * 0.5, W, ORANGE, 0.35)


# ------------------------------------------------------------------ the film
def shots(tl):
    A_, B = tl.at, tl.by_id
    return [
        (0.0, "cold_face"), (B["d2"].start - 0.1, "cold_bodies"), (A_("d2", "And") - 0.1, "cold_face2"),
        (B["d3"].start - 0.3, "rewind"), (B["d4"].start - 0.15, "haruto_ren"), (B["d5"].start - 0.15, "yui"),
        (B["d6"].start - 0.15, "riku_kota"), (A_("d6", "Escape", nth=2) - 0.1, "notebook"),
        (B["d7"].start - 0.15, "go"), (B["d8"].start - 0.15, "mio"), (B["d9"].start - 0.15, "aoi_window"),
        (B["d10"].start - 0.15, "window"), (B["d11"].start - 0.15, "faces"), (B["d12"].start - 0.1, "eye"),
        (B["d12"].end + 0.25, "black"), (B["d13"].start - 0.2, "floor"), (A_("d13", "Our") - 0.1, "ren_wake"),
        (B["d14"].start - 0.15, "phone"), (B["d15"].start - 0.15, "cameras"), (B["d16"].start - 0.15, "screen1"),
        (B["d17"].start - 0.15, "aoi_dark"), (B["d18"].start - 0.15, "screen2"), (B["d19"].start - 0.2, "momo"),
        (B["d20"].start - 0.1, "title"), (B["d21"].start - 0.1, "momo_close"), (tl.total + 1, "end")]


_shots = {}


def clock_at(t, tl):
    """The in-world time: 12:16:00 at "One minute earlier", 12:17:00 on the flash; the cold open shows 12:16:58."""
    B = tl.by_id
    t0, t1 = B["d3"].start, B["d12"].start + 0.2
    if t < t0:
        return 12, 16, 58
    if t >= t1:
        return 12, 17, 0
    sec = int(60 * (t - t0) / (t1 - t0))
    return 12, 16, min(59, sec)


def draw(cr, t, tl):
    A_, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    clk = clock_at(t, tl)
    t_flash = B["d12"].start + 0.2
    t_boom = B["d12"].end + 0.25
    meteor = clamp01((t - B["d9"].start) / max(1.0, t_flash - B["d9"].start)) if t >= B["d9"].start else 0.0
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    by = 940                                                    # neck base for single busts (captions sit below)

    cr.save()
    if name in ("cold_face", "cold_face2"):
        camera(cr, t, s0, s1, 1.02, 1.12, cy=700, shake=1.5)
        bg_class(cr, t, 0.8, (12, 16, 58))
        A.student_bust(cr, W / 2, by + 40, 1.3, t, "ren", "shock" if name == "cold_face" else "fear",
                       look=(-0.6, -0.5), rim=ORANGE + (0.8,), rim_from=(-10, -6))
        glow(cr, 0, 200, 700, ORANGE, 0.35)
        if name == "cold_face2":                               # a subliminal glimpse of the eye
            A.the_eye(cr, t, W / 2, H * 0.3, 150, a=0.85 * (abs((t - A_("d2", "something")) ) < 0.2))
    elif name == "cold_bodies":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=0.8)
        A.lying_students(cr, t)
        grade(cr, (0.7, 0.75, 0.85), (0.35, 0.36, 0.42))
    elif name == "rewind":
        camera(cr, t, s0, s1, 1.0, 1.04)
        A.classroom(cr, t, 0.0, clk)
        for j in range(5):                                     # the rewind: tape lines rolling
            yy = (t * 900 + j * 280) % H
            cr.set_source_rgba(1, 1, 1, 0.25)
            cr.rectangle(0, yy, W, 10)
            cr.fill()
        for j, (who, x) in enumerate((("haruto", 180), ("ren", 380), ("yui", 580))):
            A.student_bust(cr, x, 1180, 0.62, t, who, "smile" if who != "ren" else "calm")
    elif name == "haruto_ren":
        camera(cr, t, s0, s1, 1.0, 1.05)
        bg_class(cr, t, 0.0, clk)
        A.student_bust(cr, 230, by + 60, 0.98, t, "ren", "focus", look=(0.6, 0))
        A.student_bust(cr, 510, by + 40, 1.02, t, "haruto", "grin", look=(-0.6, 0), talk=talk("haruto"))
    elif name == "yui":
        camera(cr, t, s0, s1, 1.02, 1.08)
        bg_class(cr, t, 0.0, clk)
        A.student_bust(cr, W / 2, by, 1.25, t, "yui", "smile", look=(-0.3, 0), talk=talk("yui"))
    elif name == "riku_kota":
        camera(cr, t, s0, s1, 1.0, 1.05, shake=1.4)
        bg_class(cr, t, 0.0, clk)
        A.student_bust(cr, 220, by + 80, 0.95, t, "kota", "fear", look=(0.6, -0.2), sweat=0.7)
        A.student_bust(cr, 500, by + 20, 1.08, t, "riku", "smirk", look=(-0.7, 0.1), talk=talk("riku"))
    elif name == "notebook":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=620)
        bg_class(cr, t, 0.0, clk, blur=14)
        notebook(cr, t, W / 2, 640, 1.3)
    elif name == "go":
        camera(cr, t, s0, s1, 1.02, 1.08)
        bg_class(cr, t, 0.0, clk)
        A.student_bust(cr, 180, by + 120, 0.8, t, "riku", "worry", look=(0.7, -0.2))
        A.student_bust(cr, 470, by, 1.2, t, "go", "angry", look=(-0.5, 0), talk=talk("go"))
    elif name == "mio":
        camera(cr, t, s0, s1, 1.02, 1.08)
        bg_class(cr, t, 0.0, clk)
        A.student_bust(cr, W / 2, by, 1.25, t, "mio", "smirk", look=(0.5, 0.2), talk=talk("mio"))
    elif name == "aoi_window":
        camera(cr, t, s0, s1, 1.02, 1.1)
        bg_class(cr, t, meteor, clk, blur=5)
        A.student_bust(cr, W * 0.58, by, 1.2, t, "aoi", "focus", look=(-0.8, -0.4), talk=talk("aoi"))
    elif name == "window":
        camera(cr, t, s0, s1, 1.0, 1.15, cx=200, cy=400, shake=1.5)
        A.classroom(cr, t, meteor, clk)
    elif name == "faces":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=2.5)
        bg_class(cr, t, meteor, clk, blur=12)
        for who, x, y, s, e in (("kota", 110, 1120, 0.7, "fear"), ("mio", 610, 1120, 0.7, "shock"),
                                ("haruto", 200, 1000, 0.85, "shock"), ("yui", 520, 1000, 0.85, "fear"),
                                ("ren", W / 2, 960, 0.95, "shock")):
            A.student_bust(cr, x, y, s, t, who, e, look=(-0.5, -0.6), rim=ORANGE + (0.9,), rim_from=(-10, -8))
        glow(cr, 100, 300, 900, ORANGE, 0.45 * meteor)
    elif name == "eye":
        camera(cr, t, s0, s1, 1.0, 1.25, shake=1.0)
        eye_shot(cr, t, seg(t, B["d12"].start, B["d12"].end))
    elif name == "black":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    elif name == "floor":
        camera(cr, t, s0, s1, 1.0, 1.08, shake=0.6)
        A.lying_students(cr, t, stir=1.0)
        grade(cr, (0.7, 0.75, 0.85), (0.35, 0.36, 0.42))
    elif name == "ren_wake":
        camera(cr, t, s0, s1, 1.02, 1.1)
        hud2d.blurred(cr, lambda c: A.chamber(c, t), sigma=8)
        A.student_bust(cr, W / 2, by, 1.25, t, "ren", "worry", look=(0.4, -0.2), rim=(0.8, 0.9, 1, 0.5))
    elif name == "phone":
        camera(cr, t, s0, s1, 1.0, 1.08)
        hud2d.blurred(cr, lambda c: A.chamber(c, t), sigma=10)
        A.student_bust(cr, 470, by + 80, 1.05, t, "haruto", "worry", look=(-0.5, 0.3), talk=talk("haruto"))
        phone(cr, t, 220, 640, 1.1)
    elif name == "cameras":
        camera(cr, t, s0, s1, 1.0, 1.06)
        A.chamber(cr, t)
        turn = 0.4 * seg(t, s0, s0 + 0.8)
        for cx, cy, sx in ((W * 0.18, H * 0.2, 1), (W * 0.82, H * 0.2, -1)):
            A.camera_unit(cr, t, cx, cy, sx, 1.4, turn=turn)
        A.student_bust(cr, W / 2, by + 60, 0.95, t, "aoi", "worry", look=(0, -0.7), talk=talk("aoi"))
    elif name in ("screen1", "screen2"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=420)
        lines = (["CLASS 3-B", "20 STUDENTS", "20 SURVIVORS"] if name == "screen1"
                 else ["EVENT 00: IMPACT", "STATUS OF EARTH:", "UNKNOWN"])
        A.chamber(cr, t, screen=A.screen_text(lines, col=(0.55, 1, 0.85, 1) if name == "screen1"
                                              else (1, 0.45, 0.35, 1)))
        for j, who in enumerate(("kota", "riku", "ren", "yui", "go")):        # their backs, looking up
            A.student_bust(cr, 80 + j * 140, 1250, 0.6, t, who, "worry", look=(0, -0.8))
    elif name == "aoi_dark":
        camera(cr, t, s0, s1, 1.03, 1.12)
        hud2d.blurred(cr, lambda c: A.chamber(c, t, screen=A.screen_text(["20 SURVIVORS"])), sigma=8)
        A.student_bust(cr, W * 0.62, by, 1.15, t, "aoi", "worry", look=(-0.3, -0.2), talk=talk("aoi"))
        A.student_bust(cr, 140, by + 160, 0.7, t, "kota", "fear", look=(0.3, -0.5), tremble=1.0)
    elif name in ("momo", "title"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=420)
        pop = seg(t, B["d19"].start - 0.2, B["d19"].start + 0.3)
        A.chamber(cr, t, screen=A.screen_text([" "], momo_at=pop, t=t))
        for j, who in enumerate(("mio", "haruto", "ren", "yui", "aoi")):
            A.student_bust(cr, 80 + j * 140, 1250, 0.6, t, who, "shock", look=(0, -0.8))
        if name == "title":
            p = seg(t, B["d20"].start, B["d20"].start + 0.25)
            hud2d._text(cr, "DEAD MAN'S", W / 2, 640 - 40 * (1 - p), 76, (1, 1, 1, p), hud2d.ROUND, "center",
                        outline=INK, ow=10, shadow=0.5)
            hud2d._text(cr, "ALGORITHM", W / 2, 720 - 40 * (1 - p), 76, (*hud2d.RED[:3], p), hud2d.ROUND, "center",
                        outline=INK, ow=10, shadow=0.5)
    elif name == "momo_close":
        camera(cr, t, s0, s1, 1.0, 1.15, cy=700)
        hud2d.blurred(cr, lambda c: A.chamber(c, t), sigma=10)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
        lean = seg(t, s0, s0 + 0.8)
        A.momo(cr, W / 2, 1180, 3.6 + 0.6 * lean, t, mood="sly" if t > A_("d21", "breaks") else "happy",
               lean=0.12 * lean)
    cr.restore()

    if name != "black":
        hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.06)
    A.flash(cr, t, t_flash, 0.35)
    A.flash(cr, t, t_boom, 0.25)
    # name cards (the first time each speaks or is seen)
    for who, a, b in (("haruto", B["d4"].start, B["d4"].start + 1.6), ("ren", B["d4"].start + 1.6, B["d4"].end + 0.2),
                      ("yui", B["d5"].start, B["d5"].end + 0.3), ("riku", B["d6"].start, B["d6"].start + 1.5),
                      ("kota", B["d6"].start + 1.5, A_("d6", "Escape", nth=2)), ("go", B["d7"].start, B["d7"].end + 0.3),
                      ("mio", B["d8"].start, B["d8"].end + 0.2), ("aoi", B["d9"].start, B["d9"].end + 0.2)):
        A.name_card(cr, t, a, b, who, y=1150)
    momo_card(cr, t, B["d19"].start + 0.4, B["d19"].end + 0.3)
    after = t >= t_boom
    h, m, sec = clk
    A.status_bar(cr, t, f"CLASS 3-B · {h}:{m:02d}:{sec:02d}" if not after else "CLASS 3-B · ??:??:??",
                 "IMPACT" if t_flash <= t < B["d13"].start else ("STATUS: UNKNOWN" if after else None),
                 alert=t >= t_flash)
    hud2d.hook(cr, t, [("12:17.", False), ("THE SKY FELL ON US.", True)], end=B["d2"].end + 0.1, y=230, size=80)
    hud2d.stamp(cr, t, B["d3"].start - 0.2, B["d3"].end + 0.2, ["1 MINUTE EARLIER"], y=320, col=hud2d.YELLOW)
    if t < A_("d21", "who"):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    final_card(cr, t, A_("d21", "breaks"))
    cue("thunder", t, 0.0, 3.0)                                  # the rumble, from frame 0
    cue("riser", t, B["d10"].start, t_flash - B["d10"].start)
    cue("sting", t, t_boom)                                      # the impact, in the silence after line 12
    cue("drip", t, B["d13"].start - 0.3)
    cue("hum", t, B["d13"].start, B["d18"].end - B["d13"].start)
    cue("click", t, B["d15"].start - 0.2)
    cue("static", t, B["d16"].end + 0.02, 0.3)
    cue("chime", t, B["d19"].start - 0.5)
    cue("heartbeat", t, B["d17"].start, B["d18"].end - B["d17"].start)


def momo_card(cr, t, start, end):
    if t < start or t > end + 0.25:
        return
    A.NAMES.setdefault("momo", ("MOMO", "administrator"))
    A.name_card(cr, t, start, end, "momo", y=1150, side=-1)


def final_card(cr, t, start):
    """WHO BREAKS FIRST? The eight names, then the ask and the next part. Held over the tail."""
    if t < start:
        return
    k = clamp01((t - start) / 0.3)
    cr.set_source_rgba(0.02, 0.02, 0.04, 0.8 * k)
    cr.paint()
    hud2d._text(cr, "WHO BREAKS FIRST?", W / 2, 250, 60, (1, 1, 1, k), hud2d.ROUND, "center", shadow=0.5)
    order = ["ren", "haruto", "yui", "riku", "kota", "go", "aoi", "mio"]
    for j, who in enumerate(order):
        p = clamp01((t - start - 0.15 - 0.06 * j) / 0.2)
        if p <= 0:
            continue
        x = W / 2 + (-170 if j % 2 == 0 else 170)
        y = 380 + (j // 2) * 120
        nm = A.NAMES[who][0]
        cr.save()
        A.tk.tk_rrect(cr, x - 165, y - 40, 330, 80, 14)
        cr.set_source_rgba(0.08, 0.08, 0.1, p)
        cr.fill_preserve()
        cr.set_source_rgba(*hud2d.RED[:3], p)
        cr.set_line_width(3)
        cr.stroke()
        hud2d._text(cr, nm, x, y + 10, 26, (1, 1, 1, p), hud2d.ROUND, "center")
        cr.restore()
    p = clamp01((t - start - 0.7) / 0.25)
    if p > 0:
        A.tk.tk_rrect(cr, W / 2 - 240, 890, 480, 84, 42)
        cr.set_source_rgba(*hud2d.YELLOW[:3], p)
        cr.fill()
        hud2d._text(cr, "COMMENT A NAME BELOW", W / 2, 945, 38, (0.08, 0.06, 0.04, p), hud2d.ROUND, "center")
        hud2d._text(cr, "PART 2: THE GLASS AUCTION", W / 2, 1030, 30, (1, 1, 1, 0.9 * p), hud2d.ROUND, "center")
