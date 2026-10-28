"""DEAD MAN'S ALGORITHM, the manga, Episode 2 (9:16): Chapter 1 "12:17", pages 8-14. The clock at 12:16:44, Aoi at the
window, the streak in the sky, the meteor at 12:17:03, Ren frozen in its glare, the impact at 12:17:05, darkness and
silence, then waking on cold concrete: Yui, Haruto's "...Where are we?", and someone missing (the teacher, page 15).

Every character line is word for word as lettered on the manga chat's pages (unnamed classmates are its placeholders
STUDENT A/B/C, shown as CLASSMATE); the narrator only describes what the panels show. The glare's shape stays
ambiguous (rings, cracks or an eye), as the manga script asks.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga02   -> out/stories/dma_manga02.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(1)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="e", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="e", **kw)


BEATS = [
    n(1, 8, 1, "[Twelve sixteen and forty-four seconds.|12:16:44.]"),
    n(2, 8, 2, "Ren checked his phone. Connection lost.", gap=0.4),
    n(3, 8, 3, "Aoi was already at the window.", gap=0.4),          # "Fujimoto" was heard as "The Yumoto"
    s(4, 8, 3, "aoi", "[What is that?|...What is that?]", gap=0.3),
    n(5, 8, 4, "One streak of light. Moving far too fast.", gap=0.4),
    s(6, 9, 1, "student_a", "A plane?"),
    s(7, 9, 1, "student_b", "[It's way too fast!|It's way too fast—]", gap=0.25),
    n(8, 9, 2, "Closer now. Trailing fire.", gap=0.35),
    s(9, 9, 3, "haruto", "[Hey. It's getting bigger.|Hey... it's getting bigger.]", gap=0.35),
    s(10, 9, 4, "student_c", "[It's a meteor!|It's a meteor!!]", gap=0.35, impact=True),
    n(11, 10, 1, "[Twelve seventeen and three seconds.|12:17:03.]", impact=True, sfx="thunder"),
    n(12, 10, 1, "It filled the sky. Then the roar arrived.", gap=0.3),
    n(13, 10, 2, "Desks went over. Everyone ran.", gap=0.35),
    s(14, 10, 2, "riku", "[Move!|MOVE!]", gap=0.2, impact=True),
    n(15, 11, 1, "Everyone except Ren."),
    n(16, 11, 2, "Inside the glare, there was a shape. Rings of light. Or cracks. Or an eye.", gap=0.4),
    n(17, 11, 3, "He couldn't look away.", gap=0.4),                # "Ren" was heard as "Ben"
    n(18, 12, 1, "[Twelve seventeen and five seconds.|12:17:05.]", impact=True, sfx="sting"),
    n(19, 12, 2, "Then darkness.", gap=0.6),
    n(20, 12, 3, "Then silence.", gap=0.5),
    n(21, 13, 1, "Ren opened his eyes.", gap=0.9),
    n(22, 13, 2, "Cold concrete. This wasn't his classroom.", gap=0.4),
    n(23, 13, 3, "His forehead was bleeding.", gap=0.4),
    n(24, 13, 4, "All around him, his classmates were waking up.", gap=0.4),
    n(25, 14, 1, "He went looking for someone."),
    s(26, 14, 2, "yui", "[You're bleeding!|You're bleeding—]", gap=0.35),
    s(27, 14, 2, "ren", "I'm fine.", gap=0.3),
    s(28, 14, 3, "yui", "[You're alive.|...You're alive.]", gap=0.4),
    n(29, 14, 4, "Even Haruto wasn't joking anymore.", gap=0.4),
    s(30, 14, 4, "haruto", "[Where are we?|...Where are we?]", gap=0.3),
    n(31, 14, 0, "Nobody answered. And someone was missing.", gap=0.6),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="12:17:05. The Meteor Hit. Then They Woke Up Somewhere Else | Dead Man's Algorithm Manga Ep 2 ☄️",
    alt_titles=["21 Seconds Before the Meteor Hit Class 3-B ☄️",
                "Dead Man's Algorithm: The Manga, Episode 2 ☄️"],
    description="""12:16:44. A streak of light over the town, moving far too fast.
12:17:03. The meteor fills the sky. 12:17:05. Impact.
Then darkness. Then silence. Then cold concrete, and someone missing.

Dead Man's Algorithm, the manga, Chapter 1 "12:17", pages 8 to 14.
Episode 3 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "meteor", "episode 2"],
    pinned_comment="Rings of light, cracks, or an eye: what do you think Ren saw inside the meteor's glare? 👇",
)

KEY = {"twelve", "sixteen", "seventeen", "connection", "lost", "window", "streak", "fast", "plane", "fire", "bigger",
       "meteor", "roar", "ran", "move", "except", "glare", "eye", "darkness", "silence", "eyes", "concrete",
       "bleeding", "alive", "joking", "where", "missing", "fine"}


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 2, [("12:16:44.", False), ("21 SECONDS LEFT.", True)], "e31", "THE CHAMBER", KEY)
    cue("heartbeat", t, B["e3"].start, B["e10"].end - B["e3"].start)
    cue("riser", t, B["e8"].start, B["e11"].start - B["e8"].start)
    cue("riser", t, B["e15"].start, B["e18"].start - B["e15"].start)
    cue("thud", t, B["e18"].start + 0.02)
    cue("hush", t, B["e19"].start - 0.2, B["e21"].start - B["e19"].start + 0.1)   # darkness, then silence
    cue("heartbeat", t, B["e29"].start, B["e31"].end - B["e29"].start)
