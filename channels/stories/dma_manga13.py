"""DEAD MAN'S ALGORITHM, the manga, Episode 13 (9:16): Chapter 5 "Thirty Tokens", pages 1-6 (Part 10, "The Offer").
Riku comes out first (nineteen opened, found); Ren's turn: his own name in nine, so there's no room left for a loop
longer than ten ("He kept his word."); Momo's whispered offer (swap TACHIBANA and HAYASHI for thirty tokens); Ren
touches nothing and understands Momo wasn't only asking him; Riku turned down fifty ("Dead people don't owe me
anything."); seventeen people still waiting to be offered a price, and Ren can't say a word.

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter05, approved canon v6). The narrator opens the
chapter, reads the two board results and the cards Ren turns over.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga13   -> out/stories/dma_manga13.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(5)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="r", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="r", **kw)


BEATS = [
    n(1, 1, 0, "[Chapter five.|Chapter 5:] Thirty Tokens."),
    n(2, 1, 1, "Riku went in first. He opened all nineteen. Found.", gap=0.4),
    s(3, 1, 2, "ren", "My turn.", gap=0.4),
    s(4, 2, 1, "ren", "My locker. A card."),
    s(5, 2, 2, "ren", "A name.", gap=0.3),
    s(6, 2, 3, "ren", "The next locker. Another name.", gap=0.3),
    s(7, 2, 4, "ren", "Seven. Eight. Nine. [Kuroda Ren.|KURODA REN.]", gap=0.35),
    s(8, 3, 1, "ren", "Nine. A loop of nine leaves ten lockers. There's no room left for a loop longer than ten."),
    s(9, 3, 2, "ren", "He kept his word.", gap=0.45),
    s(10, 3, 3, "momo", "[Psst! Swap Tachibana and Hayashi.|Psst! Swap TACHIBANA and HAYASHI.]", gap=0.45,
      sfx="click"),
    s(11, 3, 3, "momo", "[Thirty tokens. Nobody will know!|Thirty tokens! Nobody will know!]", gap=0.3),   # "tokens!" was heard "token"
    s(12, 4, 1, "ren", "I didn't touch anything."),
    s(13, 4, 2, "ren", "Then I understood. Momo wasn't only asking me.", gap=0.45),
    s(14, 4, 3, "riku", "Disappointed?", gap=0.5),
    s(15, 5, 1, "ren", "It offered you something."),
    s(16, 5, 2, "riku", "[Fifty. To leave the loop... whole.|Fifty. To leave the loop whole.]", gap=0.4),   # was heard "lead the loophole"
    s(17, 5, 3, "ren", "Why didn't you take it?", gap=0.4),
    s(18, 5, 4, "riku", "Dead people don't owe me anything.", gap=0.45),
    n(19, 6, 1, "Ren. Nine. Found."),
    s(20, 6, 2, "ren", "Seventeen people were waiting to be offered a price for someone's life.", gap=0.4),
    s(21, 6, 3, "ren", "And I couldn't say a word.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Swap Two Names. Thirty Tokens. Nobody Will Know | Dead Man's Algorithm Ep 13 🃏",
    alt_titles=["The Host Whispered an Offer in the Locker Room 🃏", "Dead Man's Algorithm: The Manga, Episode 13 🃏"],
    description="""Riku went in first and opened all nineteen lockers. Then it was Ren's turn: his own name in nine, so
there's no room left for a loop longer than ten. Riku kept his word.
Then a small screen lit up. "Psst! Swap TACHIBANA and HAYASHI. Thirty tokens! Nobody will know!"
Momo wasn't only asking Ren. Seventeen people were still waiting to be offered a price for someone's life.

Dead Man's Algorithm, the manga, Chapter 5 "Thirty Tokens", pages 1 to 6.
Episode 14 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "thirty tokens", "betrayal", "episode 13"],
    pinned_comment="Momo offers thirty tokens for one secret swap, and nobody will know. Seventeen people still have "
                   "to go in. Does anyone take it? 👇",
)

KEY = {"turn", "locker", "card", "name", "nine", "loop", "ten", "room", "longer", "word", "swap", "thirty",
       "tokens", "nobody", "know", "touch", "anything", "understood", "asking", "disappointed", "offered", "fifty",
       "whole", "take", "dead", "owe", "found", "seventeen", "price", "life", "say", "nineteen", "first"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 5 long video)."""
    B = tl.by_id
    cue("hush", t, B["r10"].start - 0.2, B["r11"].end - B["r10"].start + 0.3)   # the whispered offer


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 13, [("SWAP TWO NAMES", False), ("FOR 30 TOKENS?", True)], "r21", "NOT FOUND", KEY)
    cues(t, tl)
