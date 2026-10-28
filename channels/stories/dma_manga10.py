"""DEAD MAN'S ALGORITHM, the manga, Episode 10 (9:16): Chapter 4 "Find Yourself", pages 1-7. A door opens in the white
room; a hand in a black sleeve takes Saki's token (nobody sees who); the locker room (twenty lockers in a ring, Saki's
sealed, a painted line all the way round); Momo's game three ("Everyone's connected!"); the board; Aoi's "on average,
nine of us die"; Riku: "Sixty-nine tokens. I open all nineteen."

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter04, approved canon v6). The narrator opens the
chapter, describes the wordless panels and reads the last rule on the screen (rule 07, which Momo doesn't say aloud).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga10   -> out/stories/dma_manga10.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(4)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="x", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="x", **kw)


BEATS = [
    n(1, 1, 0, "[Chapter four.|Chapter 4:] Find Yourself."),
    s(2, 1, 1, "ren", "A door opened in the white room. Nobody moved first.", gap=0.4),
    n(3, 2, 1, "A hand in a black sleeve picked up Saki's token."),
    n(4, 2, 2, "And slid it into a small notebook.", gap=0.35),
    s(5, 2, 3, "ren", "Nobody saw who took it.", gap=0.4),
    s(6, 3, 1, "ren", "Three rooms. In the middle one, twenty lockers stood in a ring. Every one had a name on it."),
    s(7, 3, 2, "ren", "One said [Nishida Saki.|NISHIDA SAKI.] It was sealed shut.", gap=0.4),
    s(8, 3, 3, "ren", "A line was painted on the floor. It ran past every locker, all the way around, without a "
                      "break.", gap=0.4),
    s(9, 4, 1, "momo", "Game three! Find Yourself!", sfx="chime"),
    s(10, 4, 2, "momo", "Nineteen lockers! Each one holds one card, with one of your names!", gap=0.4),
    s(11, 4, 3, "momo", "Go in alone. Open ten lockers. Find your own name, and you live! Don't, and you die!", gap=0.4),
    s(12, 5, 1, "momo", "Each token you spend opens one more! You can give tokens away before someone goes in!"),
    s(13, 5, 2, "momo", "Before you leave, you may swap the cards in two lockers. Once!", gap=0.4),
    s(14, 5, 3, "momo", "Inside, Momo might whisper you an offer!", gap=0.4),
    s(15, 5, 4, "momo", "After you go in, no talking to anyone who hasn't. No signs, no notes, nothing! Thirty "
                        "minutes!", gap=0.4),
    s(16, 6, 1, "momo", "And Momo set them up special. Everyone's connected!"),
    n(17, 6, 2, "The last rule on the screen. Anyone who hasn't gone in when thirty minutes are up dies.", gap=0.5),
    n(18, 7, 1, "The board lit up. Nineteen names. All blank."),
    s(19, 7, 2, "aoi", "Ten lockers out of nineteen. On average, nine of us die.", gap=0.4),
    s(20, 7, 3, "haruto", "Great. Half a class.", gap=0.4),
    s(21, 7, 4, "riku", "Speak for yourselves. Sixty-nine tokens. I open all nineteen.", gap=0.45),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Find Your Own Name in 10 Lockers or Die | Dead Man's Algorithm Manga Ep 10 🔒",
    alt_titles=["19 Lockers. You Can Open 10. On Average, 9 of Us Die 🔒",
                "Dead Man's Algorithm: The Manga, Episode 10 🔒"],
    description="""Game three: Find Yourself. Nineteen lockers, each holding one card with one of their names.
Go in alone, open ten lockers, find your own name, and you live. Each token opens one more. You may swap two cards,
once. And Momo says everyone's connected.
On average, nine of them die. Riku has sixty-nine tokens. He can open all nineteen.

Dead Man's Algorithm, the manga, Chapter 4 "Find Yourself", pages 1 to 7.
Episode 11 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "find yourself", "100 prisoners problem", "episode 10"],
    pinned_comment="Who took Saki's token? A hand in a black sleeve, and a small notebook. Name your suspect 👇",
)

KEY = {"door", "token", "notebook", "took", "lockers", "ring", "name", "saki", "sealed", "line", "break", "find",
       "nineteen", "card", "alone", "ten", "live", "die", "spend", "swap", "once", "offer", "nothing", "thirty",
       "connected", "rule", "board", "blank", "average", "nine", "half", "sixty", "all"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 4 long video)."""
    B = tl.by_id
    cue("heartbeat", t, B["x3"].start, B["x5"].end - B["x3"].start)
    cue("riser", t, B["x16"].start, B["x17"].end - B["x16"].start)
    cue("sting", t, B["x17"].end + 0.05)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 10, [("FIND YOUR NAME", False), ("OR DIE.", True)], "x21", "THE CHAIN", KEY)
    cues(t, tl)
