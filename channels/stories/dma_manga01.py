"""DEAD MAN'S ALGORITHM, the manga, Episode 1 (9:16): Chapter 1 "12:17", pages 1-7 (owner, 28 Oct 2026: a manga
video, "showing manga panel and saying what that specific character says in his voice and explaining some in
Narrator voice ... zooming in and zooming out from panel to panel").

Pages and dialogue come from the manga creation chat (tejassparky2/Manga, story/chapter01/script.yaml, copied to
assets/manga/dma/ch01/). Every character line is word for word from that script; the narrator's lines are new and
only describe what the panels show (plus the canon 12:17 impact). Ends at 12:16, just before the meteor (page 8).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga01   -> out/stories/dma_manga01.mp4
"""
import os

import yaml

from motion import audio, voice
from motion.engine import W, H, cue

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.stories import dma_kit as K, manga as M, serial

NARRATOR = dict(turbo=True, turbo_ref="bm_george")            # the storyteller; Ren speaks in his own voice
TAIL = 2.0
MUSIC = "horror"
voice.SPEAKERS.update(K.SPEAKERS)
voice.SPEAKERS.update({"teacher": dict(voice="am_liam", turbo_ref="am_liam")})
audio.GAINS.update(chime=0.6, click=0.6, sting=0.5)

FOLDER = "assets/manga/dma/ch01"
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROWS = {p["page"]: p["rows"] for p in yaml.safe_load(open(os.path.join(_ROOT, FOLDER, "script.yaml")))["pages"]}
BOOK = M.Manga(os.environ.get("MANGA_PAGES", FOLDER), ROWS)              # MANGA_PAGES: test pages


def N(i, page, panel, text, **kw):
    return dict(id=f"m{i}", page=page, panel=panel, text=text, **kw)


def S(i, page, panel, who, text, **kw):
    return dict(id=f"m{i}", page=page, panel=panel, text=text, speaker=who, **kw)


BEATS = [
    N(1, 1, 0, "Class [three B.|3-B.] An ordinary school, on an ordinary day."),
    N(2, 1, 0, "At [twelve seventeen,|12:17,] a meteor will strike. Nobody here knows it yet.", gap=0.4),
    N(3, 2, 1, "Twenty students. Talking. Studying. Bored."),
    N(4, 2, 2, "And one of them, asleep by the window.", gap=0.35),
    S(5, 2, 2, "teacher", "Kuroda.", name="TEACHER", gap=0.35),
    N(6, 2, 3, "His close friend, Sakurai Haruto, helped him wake up.", gap=0.35),
    S(7, 2, 3, "teacher", "Kuroda Ren.", name="TEACHER", gap=0.3),
    S(8, 3, 1, "ren", "[What?|...What?]"),
    S(9, 3, 2, "haruto", "You were drooling.", gap=0.35),
    S(10, 3, 3, "haruto", "Dead?", gap=0.35),
    S(11, 3, 3, "ren", "Unfortunately.", gap=0.3),
    S(12, 3, 4, "haruto", "Good. I need someone to copy homework from.", gap=0.35),
    S(13, 3, 5, "ren", "You copied mine yesterday.", gap=0.35),
    S(14, 3, 6, "haruto", "And I'm building a sustainable business model.", gap=0.35),
    N(15, 4, 1, "Then Tachibana Yui came over."),
    S(16, 4, 1, "yui", "Here.", gap=0.3, sfx="click"),
    S(17, 4, 2, "ren", "[Milk?|...Milk?]", gap=0.35),
    S(18, 4, 3, "yui", "You said your stomach hurt yesterday.", gap=0.35),
    S(19, 4, 4, "haruto", "Ohh? Personal delivery?", gap=0.35),
    S(20, 4, 5, "ren", "It's not like that.", gap=0.35),
    S(21, 4, 5, "haruto", "[I didn't say anything.|I didn't say anything~]", gap=0.25),
    N(22, 5, 1, "Ren had a notebook open. Page after page of numbers."),
    S(23, 5, 2, "yui", "Are these from your trading account?", gap=0.35),
    S(24, 5, 3, "ren", "[Just notes.|...Just notes.]", gap=0.35),
    N(25, 5, 4, "Yui knew he was hiding something. She didn't push.", gap=0.35),
    N(26, 6, 1, "Then a hand slammed down on Hayashi Kota's desk.", impact=True, sfx="hit"),
    S(27, 6, 1, "riku", "What's this?", gap=0.3),
    S(28, 6, 2, "riku", "Survival plans? Seriously?", gap=0.35),
    S(29, 6, 3, "kota", "Give it back.", gap=0.35),
    S(30, 6, 4, "riku", "Or what?", gap=0.35),
    N(31, 7, 1, "Shibata Go stood up."),                      # the caption font has no "ō"
    S(32, 7, 1, "go", "Stop.", name="GO", gap=0.3),
    S(33, 7, 2, "riku", "[Huh? You want to go?|Huh?! You want to go?]", gap=0.3, impact=True),
    S(34, 7, 3, "mio", "Don't get involved.", gap=0.35),
    N(35, 7, 4, "But Fujimoto Aoi wasn't watching the fight. Something had flashed across her glasses.", gap=0.45),
    N(36, 7, 0, "It was [twelve sixteen.|12:16.] In less than a minute, none of this would matter.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="The Last Normal Minute Before the Meteor | Dead Man's Algorithm Manga Ep 1 ☄️",
    alt_titles=["Class 3-B Had No Idea What 12:17 Would Bring ☄️",
                "Dead Man's Algorithm: The Manga, Episode 1 ☄️"],
    description="""Class 3-B. An ordinary school, on an ordinary day.
At 12:17, a meteor will strike. Nobody in this room knows it yet.

Dead Man's Algorithm, the manga, Chapter 1 "12:17", pages 1 to 7.
Episode 2 is next: the sky.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "meteor", "episode 1"],
    pinned_comment="Riku, Gō, Mio, Aoi... only one of them noticed the sky. Who do you think survives this "
                   "chapter? 👇",
)

KEY = {"ordinary", "meteor", "twelve", "seventeen", "nobody", "twenty", "asleep", "kuroda", "dead", "unfortunately",
       "homework", "yesterday", "milk", "stomach", "personal", "notebook", "numbers", "trading", "hiding", "slammed",
       "survival", "stop", "involved", "aoi", "glasses", "sixteen", "minute", "matter"}


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    hud.finish(cr, t, flash_at=[], vig=0.35, grain=0.03)
    M.series_chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 1")
    hook_end = B["m2"].end + 0.1                               # under the page: the page's own title stays clear
    hud2d.hook(cr, t, [("12:17.", False), ("THE SKY FALLS.", True)], end=hook_end, y=1095, size=78)
    if hook_end + 0.25 < t < B["m36"].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=1135)
    serial.next_card(cr, t, B["m36"].end + 0.1, "DEAD MAN'S ALGORITHM · THE MANGA", "EPISODE 2", "THE SKY")
    cue("hum", t, 0.0, tl.total)
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08)
    cue("heartbeat", t, B["m35"].start, B["m36"].end - B["m35"].start)
    cue("riser", t, B["m36"].start, B["m36"].end - B["m36"].start)
