"""DEAD MAN'S ALGORITHM, the manga, Episode 4 (9:16): Chapter 1 "12:17", pages 22-26, the end of Chapter 1. Momo starts
GAME 01, THE GLASS AUCTION: the parameters, the key behind the glass, the five rules (the camera moves rule by rule
down the rules page), Haruto's "Eliminated... What does that even mean?", Momo's silence, Ren reading, the timer at
10:00, and the closing page at 09:55: "And the game has just begun." Chapter 2 ("The Bids") is next.

Every character line is word for word as lettered on the manga chat's pages; the five rules and the parameters are
read exactly as displayed (canon). The narrator only describes the panels, plus one plain-words summary of the rules
under the rules page, which follows the approved continuation (every bid is spent; "eliminated" stays unexplained).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga04   -> out/stories/dma_manga04.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(1)
RULE = {1: (90, 214, 1510, 448), 2: (90, 488, 1510, 721), 3: (90, 762, 1510, 1184),   # each rule's lines on page 24
        4: (90, 1238, 1510, 1573), 5: (90, 1613, 1510, 2035)}


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="h", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="h", **kw)


BEATS = [
    s(1, 22, 1, "momo", "Let's not waste time!", sfx="chime"),
    n(2, 22, 2, "[Game one. The Glass Auction.|GAME 01: THE GLASS AUCTION.]", gap=0.45),
    n(3, 22, 3, "[Twenty players. A hundred tokens each. Ten minutes.|20 PLAYERS. 100 TOKENS EACH. 10 MINUTES.]",
      gap=0.4),
    n(4, 22, 3, "[Objective. Obtain the exit key.|OBJECTIVE: OBTAIN THE EXIT KEY.]", gap=0.3),
    n(5, 23, 1, "A light came on over a glass case.", sfx="thud"),
    n(6, 23, 2, "Inside it, the key.", gap=0.4),
    s(7, 23, 3, "momo", "And these are the rules.", gap=0.4),
    n(8, 24, 1, "[Rule one. The highest unique bid wins the key.|RULE 01: The highest unique bid wins the key.]",
      box=RULE[1]),
    n(9, 24, 1, "[Rule two. All spent tokens are permanently lost.|RULE 02: All spent tokens are permanently "
                "lost.]", box=RULE[2], gap=0.4),
    n(10, 24, 1, "[Rule three. If two or more players submit the same highest bid, every player tied at that amount "
                 "is eliminated.|RULE 03: If two or more players submit the same highest bid, every player tied at "
                 "that amount is eliminated.]", box=RULE[3], gap=0.4),
    n(11, 24, 1, "[Rule four. If the highest bid is not unique, the next-highest unique bid wins.|RULE 04: If the "
                 "highest bid is not unique, the next-highest unique bid wins.]", box=RULE[4], gap=0.4),
    n(12, 24, 1, "[Rule five. If all players leave all tokens unspent when time expires, everyone is executed.|"
                 "RULE 05: If all players leave all tokens unspent when time expires, everyone is executed.]",
      box=RULE[5], gap=0.4, sfx="sting"),
    n(13, 24, 0, "In plain words. The biggest bid that nobody else matches wins. Every bid is spent, win or lose.",
      gap=0.6),
    n(14, 24, 0, "Tie at the top, and you're eliminated. And if nobody bids at all, everyone dies.", gap=0.35),
    s(15, 25, 1, "haruto", "[Eliminated. What does that even mean?|\"Eliminated\"... What does that even mean?]"),
    n(16, 25, 2, "Momo just smiled. And said nothing.", gap=0.45),
    n(17, 25, 3, "Ren was still reading. Every word.", gap=0.45),
    s(18, 25, 4, "momo", "[Time starts now!|Time starts... now!]", gap=0.5),
    n(19, 25, 5, "[Ten minutes.|10:00.]", gap=0.3, sfx="ding", impact=True),
    n(20, 26, 1, "Twenty students. One key behind the glass."),
    n(21, 26, 1, "And the game has just begun.", gap=0.6),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="The Highest Unique Bid Wins. A Tie Gets You Eliminated | Dead Man's Algorithm Manga Ep 4 🔑",
    alt_titles=["20 Players. 100 Tokens Each. One Key 🔑",
                "Dead Man's Algorithm: The Manga, Episode 4 🔑"],
    description="""GAME 01: THE GLASS AUCTION.
20 players. 100 tokens each. 10 minutes. One exit key behind the glass.
The highest unique bid wins. Every bid is spent. A tie at the top gets you eliminated.
And if nobody bids at all, everyone is executed.

Dead Man's Algorithm, the manga, Chapter 1 "12:17", pages 22 to 26: the end of Chapter 1.
Chapter 2, "The Bids", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "glass auction", "episode 4"],
    pinned_comment="You have 100 tokens and ten minutes. How much do you bid, and why? 👇",
)

KEY = {"waste", "game", "glass", "auction", "twenty", "hundred", "tokens", "minutes", "objective", "key", "light",
       "rules", "rule", "highest", "unique", "spent", "lost", "tied", "eliminated", "next", "unspent", "executed",
       "plain", "matches", "bid", "lose", "tie", "dies", "mean", "smiled", "nothing", "reading", "starts", "ten",
       "begun"}


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 4, [("20 PLAYERS.", False), ("ONE KEY.", True)], "h21", "THE BIDS", KEY)
    cue("heartbeat", t, B["h10"].start, B["h13"].start - B["h10"].start)
    cue("hush", t, B["h16"].start - 0.2, B["h17"].end - B["h16"].start + 0.2)        # Momo's silence, Ren reading
    cue("riser", t, B["h17"].end, B["h19"].start - B["h17"].end)
    cue("heartbeat", t, B["h20"].start, B["h21"].end - B["h20"].start)
