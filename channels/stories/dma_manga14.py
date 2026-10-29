"""DEAD MAN'S ALGORITHM, the manga, Episode 14 (9:16): Chapter 5 "Thirty Tokens", pages 7-11 (Part 11, "Not Found").
Yui, Aoi and Mio all say no to the offer, and nobody can prove it; nines and tens on the board; Haruto comes in and
doesn't make a joke; Gō goes in, doesn't find his name in ten, cuts the loop (first and tenth) and the page goes black;
SHIBATA GŌ, NOT FOUND; "Riku lied!"; Kota, who Gō told to stay behind him, goes in next and finds his in nine; every
head turns to Riku ("Look at the board."); Momo: "Momo knows who swapped! Do you?"

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter05, approved canon v6). The narrator reads the
board and describes the wordless panels: Haruto's smile, Gō's three panels (staged canon: ten lockers, no name, the
cut) and Kota walking in. Gō's death is a black panel, as Saki's was: no gore.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga14   -> out/stories/dma_manga14.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(5)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="s", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="s", **kw)


BEATS = [
    n(1, 7, 1, "Then Yui. Ten. Found."),
    s(2, 7, 2, "yui", "It offered me tokens. I said no.", gap=0.4),
    n(3, 7, 3, "Aoi, nine. Mio, ten. Both found.", gap=0.4),
    s(4, 7, 4, "aoi", "Me too.", gap=0.35),
    s(5, 7, 4, "mio", "Same.", gap=0.3),
    s(6, 7, 5, "ren", "Everyone said no. Nobody could prove it.", gap=0.45),
    n(7, 8, 1, "Nines and tens. Then Haruto. Ten. Found."),
    s(8, 8, 2, "ren", "Haruto came in and sat by the wall. He didn't make a joke.", gap=0.4),
    s(9, 8, 3, "yui", "Haruto?", gap=0.4),
    n(10, 8, 4, "Haruto smiled. It didn't reach his eyes.", gap=0.45),
    n(11, 9, 1, "Then Go went in. Alone."),
    n(12, 9, 2, "He opened ten lockers. None of them had his name.", gap=0.45),
    n(13, 9, 3, "So he swapped the cards in his first and tenth lockers.", gap=0.4),
    n(14, 9, 4, "", hold=1.4, gap=0.5),
    n(15, 10, 1, "[Shibata Go. Ten.|SHIBATA GO. Ten.] Not found.", impact=True, sfx="sting"),
    s(16, 10, 2, "student_b", "Riku lied!", gap=0.35, impact=True),
    s(17, 10, 2, "student_a", "It's still one loop!", gap=0.25),
    s(18, 10, 3, "ren", "Go had told him to stay behind him. Kota was next.",
      gap=0.45),
    n(19, 10, 4, "Kota walked in alone.", gap=0.4),
    n(20, 11, 1, "Kota. Nine. Found."),
    n(21, 11, 2, "Every head turned to Riku.", gap=0.4),
    s(22, 11, 3, "riku", "Don't look at me. Look at the board.", gap=0.4),
    s(23, 11, 4, "momo", "Momo knows who swapped! Do you?", gap=0.45, sfx="chime"),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Everyone Said No. Then One Name Said NOT FOUND | Dead Man's Algorithm Ep 14 🃏",
    alt_titles=["Someone Took Momo's Offer. Nobody Can Prove Who 🃏", "Dead Man's Algorithm: The Manga, Episode 14 🃏"],
    description="""Yui said no to Momo's offer. So did Aoi. So did Mio. Nobody could prove it.
Nines and tens on the board. Haruto came in and sat by the wall, and didn't make a joke.
Then Gō went in, and the board said NOT FOUND. "Riku lied!" "It's still one loop!"
Riku: "Don't look at me. Look at the board." Momo: "Momo knows who swapped! Do you?"

Dead Man's Algorithm, the manga, Chapter 5 "Thirty Tokens", pages 7 to 11.
Episode 15 is next.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "betrayal", "episode 14"],
    pinned_comment="Riku saw every locker and kept his word. Then someone swapped two cards and Gō died. Who did "
                   "it? Name your suspect before Episode 15 👇",
)

KEY = {"tokens", "no", "found", "nobody", "prove", "nines", "tens", "wall", "joke", "smiled", "eyes", "alone",
       "ten", "lockers", "name", "swapped", "cards", "first", "tenth", "not", "lied", "loop", "behind", "next",
       "nine", "head", "riku", "board", "momo", "knows", "swapped"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 5 long video)."""
    B = tl.by_id
    cue("hush", t, B["s13"].start - 0.1, B["s15"].start - B["s13"].start + 0.1)     # the cut, then black


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 14, [("EVERYONE SAID NO.", False), ("SOMEONE LIED.", True)], "s23", "WHO SWAPPED?", KEY)
    cues(t, tl)
