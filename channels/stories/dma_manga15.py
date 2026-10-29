"""DEAD MAN'S ALGORITHM, the manga, Episode 15 (9:16): Chapter 5 "Thirty Tokens", pages 12-15 (Part 12, first half).
Eighteen found, one not found; everyone back in the ring, two lockers dark now; Mio: "You left a long loop."; Ren's
proof (his nine leaves no room for a long loop, everyone up to the ninth found theirs in nine or ten, Gō went in tenth
and didn't, only one person went in between them); every head turns to Haruto; "Haruto. Turn out your pockets." Thirty
coins spill onto the floor.

Ren's lines are spoken in Ren's voice (chip REN); every character line is word for word as lettered on the manga
chat's pages (tejassparky2/Manga, story/chapter05, approved canon v6). The narrator reads the final board and
describes the wordless panels (the dark lockers, the turning heads, the thirty coins: the approved script's own stage
directions).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga15   -> out/stories/dma_manga15.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(5)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="v", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="v", **kw)


BEATS = [
    n(1, 12, 1, "Eighteen found. One not found."),
    n(2, 12, 2, "Everyone stood in the ring of lockers again.", gap=0.4),
    n(3, 12, 3, "Two lockers were dark now. Saki's.", gap=0.4),
    n(4, 12, 4, "[And Go's.|And Gō's.]", gap=0.3),
    s(5, 13, 1, "mio", "You left a long loop.", impact=True),
    s(6, 13, 2, "ren", "No. He didn't.", gap=0.45),
    s(7, 13, 3, "ren", "I found mine in nine. A loop of nine leaves ten lockers. No room for a loop longer than ten.",
      gap=0.4),
    s(8, 13, 4, "ren", "Everyone up to the ninth person found theirs in nine or ten. Still no long loop.", gap=0.4),
    s(9, 14, 1, "ren", "[Go went in tenth.|Gō went in tenth.] He didn't find his in ten. Now there was a long loop."),
    s(10, 14, 2, "ren", "Only one person went in between them.", gap=0.5),
    n(11, 14, 3, "Every head turned to Haruto.", gap=0.45),
    s(12, 15, 1, "ren", "Haruto. Turn out your pockets.", impact=True),
    n(13, 15, 2, "Thirty coins spilled onto the floor.", gap=0.5, sfx="hit"),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Only One Person Went In Between Them | Dead Man's Algorithm Ep 15 🃏",
    alt_titles=["He Solved Who Swapped the Cards From the Board Alone 🃏",
                "Dead Man's Algorithm: The Manga, Episode 15 🃏"],
    description="""Eighteen found. One not found. "You left a long loop."
"No. He didn't." Ren found his name in nine, and a loop of nine leaves no room for a loop longer than ten. Everyone up
to the ninth person found theirs in nine or ten. Gō went in tenth and didn't find his. So the long loop appeared
between them. Only one person went in between them.
"Haruto. Turn out your pockets."

Dead Man's Algorithm, the manga, Chapter 5 "Thirty Tokens", pages 12 to 15.
Episode 16 is next.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "plot twist", "episode 15"],
    pinned_comment="Did you work it out before Ren did? The board alone was enough. When did you know? 👇",
)

KEY = {"eighteen", "found", "not", "ring", "lockers", "dark", "saki's", "long", "loop", "didn't", "nine", "ten",
       "room", "longer", "ninth", "tenth", "one", "person", "between", "head", "haruto", "pockets", "thirty", "coins",
       "floor"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 5 long video)."""
    B = tl.by_id
    cue("hush", t, B["v10"].start - 0.2, B["v12"].start - B["v10"].start + 0.1)     # who went in between


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 15, [("WHO SWAPPED", False), ("THE CARDS?", True)], "v13", "IT WAS HERS", KEY)
    cues(t, tl)
