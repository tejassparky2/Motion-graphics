"""DEAD MAN'S ALGORITHM, the manga, Episode 6 (9:16): Chapter 2 "The Bids", pages 7-11. "And if somebody lies?"
Ren's answer ("Then let them... Unless two liars pick the same number."), Riku agreeing too fast, the timer at
00:00, Momo: "Highest unique bid: thirty! Kanzaki Riku!", "You trusted a plan. I trusted a number.", "My plan was
built for a liar.", twenty survivors, and the exit opening onto game two.

Ren's first-person captions are spoken in Ren's voice; every character line and caption is word for word as lettered
on the manga chat's pages. The narrator adds two plain lines for clarity, both from canon: why Ren's plan still
worked (it needed one winner and no tie, not Ren winning), and what Riku has left (100 - 30 = 70 tokens, the fewest).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga06   -> out/stories/dma_manga06.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(2)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="k", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="k", **kw)


BEATS = [
    s(1, 7, 1, "mio", "And if somebody lies?"),
    s(2, 7, 2, "ren", "Then let them. Bid more than one, and you win the key. Unless two liars pick the same number.",
      gap=0.4),
    s(3, 7, 3, "ren", "Just never bid a hundred. Riku already called it.", gap=0.4),
    s(4, 7, 4, "riku", "[Fine. Ren, bids one.|Fine. Ren bids one.]", gap=0.4),   # "Ren bids" merged
    s(5, 8, 1, "ren", "Riku agreed too fast."),
    n(6, 8, 2, "Then time ran out.", gap=0.6, sfx="ding", impact=True),   # "hit zero" was heard "hits zero"
    s(7, 8, 3, "momo", "[Time's up! Highest unique bid. Thirty! Kanzaki Riku!|Time's up! Highest unique bid: thirty! "
                       "Kanzaki Riku!]", gap=0.4),
    s(8, 9, 1, "ren", "Riku never meant a hundred. He said it so nobody would dare bid high."),
    s(9, 9, 2, "riku", "You trusted a plan. I trusted a number.", gap=0.4),
    s(10, 9, 3, "ren", "He thought he beat my plan. My plan was built for a liar.", gap=0.45),
    n(11, 9, 0, "It never needed Ren to win. It needed one winner, and no tie.", gap=0.5),
    s(12, 10, 1, "ren", "No tie. Nobody eliminated. Twenty survivors."),
    s(13, 10, 2, "momo", "Everybody lives! How boring!", gap=0.4),
    s(14, 11, 1, "ren", "The exit key opened the exit. Into game two.", sfx="thud"),
    s(15, 11, 2, "ren", "And Riku had just spent thirty tokens. Fewer than anyone.", gap=0.45),
    n(16, 11, 2, "Seventy tokens left. The fewest in the room.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="You Trusted a Plan. I Trusted a Number. | Dead Man's Algorithm Manga Ep 6 🔑",
    alt_titles=["He Lied About His Bid. The Plan Still Worked 🔑",
                "Dead Man's Algorithm: The Manga, Episode 6 🔑"],
    description="""Ren's plan: he bids one, everyone else bids zero. "And if somebody lies?" "Then let them."
Time's up. Highest unique bid: thirty. Kanzaki Riku.
Riku thinks he beat the plan. But the plan was built for a liar: it only needed one winner, and no tie.
Twenty survivors. The exit opens. Into game two.

Dead Man's Algorithm, the manga, Chapter 2 "The Bids", pages 7 to 11.
Chapter 3, "The Charity", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "glass auction", "game theory", "episode 6"],
    pinned_comment="Riku won the key with thirty and walked out with the fewest tokens. Smart move, or a mistake "
                   "he'll pay for in game two? 👇",
)

KEY = {"lies", "liars", "same", "hundred", "called", "fast", "zero", "thirty", "kanzaki", "riku", "dare", "plan",
       "number", "liar", "win", "winner", "tie", "survivors", "boring", "exit", "two", "seventy", "fewest"}


def cues(t, tl):
    """This episode's sound cues (shared with a Chapter 2 long video)."""
    B = tl.by_id
    cue("sting", t, B["k7"].start + 0.4)
    cue("hush", t, B["k12"].start - 0.2, 0.6)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 6, [("AND IF", False), ("SOMEBODY LIES?", True)], "k16", "THE CHARITY", KEY)
    cues(t, tl)
