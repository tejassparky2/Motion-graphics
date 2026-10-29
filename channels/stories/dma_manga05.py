"""DEAD MAN'S ALGORITHM, the manga, Episode 5 (9:16): Chapter 2 "The Bids", pages 1-6. The auction's dilemma (Riku's
"Nobody beats a hundred", Aoi's tie, Haruto's zero, Kota's rule five, Mio's "everyone will remember who"), Ren doing
the math with the clock at 9:12, and his plan: "I bid one. Everyone else bids zero."

Chapter 2 is lettered with Ren's first-person captions; they're spoken in Ren's own voice (chip REN). Every character
line and caption is word for word as lettered on the manga chat's pages; the narrator (bm_george) only opens the
chapter and closes the episode.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga05   -> out/stories/dma_manga05.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(2)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="j", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="j", **kw)


BEATS = [
    n(1, 1, 0, "[Chapter two.|Chapter 2:] The Bids."),
    n(2, 1, 0, "Ten minutes. One key. And nobody wanted to bid first.", gap=0.4),
    s(3, 2, 1, "riku", "Easy. I'm going all in. Nobody beats a hundred."),
    s(4, 2, 2, "aoi", "Unless someone else bids a hundred. Then you're both eliminated.", gap=0.4),
    s(5, 2, 3, "haruto", "So we all bid zero and go home?", gap=0.4),
    s(6, 2, 4, "kota", "Then rule five executes all of us.", gap=0.4),
    s(7, 3, 1, "mio", "So somebody has to bid. And everyone will remember who."),
    s(8, 3, 2, "ren", "Everyone was doing the same math.", gap=0.45),
    s(9, 3, 3, "ren", "Bid too high, and you might tie. Bid too low, and someone beats you.", gap=0.4),
    s(10, 4, 1, "ren", "The countdown said [nine twelve.|9:12.]", sfx="ding"),
    s(11, 4, 2, "ren", "And I realised a hundred might be the most dangerous number in this room.", gap=0.4),
    s(12, 4, 3, "momo", "Tick tock, Class [three B!|3-B!]", gap=0.4, sfx="chime"),
    s(13, 4, 4, "ren", "I already knew my number.", gap=0.45),
    s(14, 5, 1, "ren", "My number was one."),
    s(15, 5, 2, "ren", "Somebody had to spend. Or rule five killed us all.", gap=0.45),
    s(16, 5, 3, "ren", "But two bids at the top would tie. And a tie gets you eliminated. Nobody knew what that "
                       "meant.", gap=0.4),
    s(17, 6, 1, "ren", "So only one person could bid. And spent tokens are gone permanently. So it had to be tiny."),
    s(18, 6, 2, "ren", "Mio was right. Everyone would remember who. So it had to be me.", gap=0.4),
    s(19, 6, 3, "ren", "I bid one. Everyone else bids zero.", gap=0.5),
    n(20, 6, 0, "One plan. Twenty people. And any one of them could lie.", gap=0.6),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="He Bid 1 Token. Everyone Else Bid 0. | Dead Man's Algorithm Manga Ep 5 🔑",
    alt_titles=["Bid Too High and You Tie. Bid Too Low and You Lose 🔑",
                "Dead Man's Algorithm: The Manga, Episode 5 🔑"],
    description="""The Glass Auction. The highest unique bid wins the key. A tie at the top gets you eliminated.
If nobody bids, everyone is executed. And every bid is spent.
Riku says he's going all in. Ren does the math, and decides a hundred is the most dangerous number in the room.
His plan: "I bid one. Everyone else bids zero."

Dead Man's Algorithm, the manga, Chapter 2 "The Bids", pages 1 to 6.
Episode 6 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "glass auction", "game theory", "episode 5"],
    pinned_comment="Ren bids one and asks everyone else to bid zero. Would you trust that plan, or bid something "
                   "else? 👇",
)

KEY = {"bids", "minutes", "key", "hundred", "eliminated", "zero", "five", "executes", "remember", "math", "tie",
       "beats", "countdown", "dangerous", "tick", "number", "one", "spend", "killed", "tiny", "permanently", "me",
       "plan", "lie"}


def cues(t, tl):
    """This episode's sound cues (shared with a Chapter 2 long video)."""
    B = tl.by_id
    cue("hush", t, B["j19"].end, B["j20"].start - B["j19"].end + 0.1)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 5, [("100 TOKENS.", False), ("WHAT DO YOU BID?", True)], "j20", "THE LIAR", KEY)
    cues(t, tl)
