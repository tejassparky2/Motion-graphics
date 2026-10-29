"""DEAD MAN'S ALGORITHM, the manga, Episode 7 (9:16): Chapter 3 "The Charity", pages 1-6. Game two: Momo's four rules
(nobody can take your tokens; give tokens to anyone in this room; the poorest player dies, a tie for poorest kills
them all; zero tokens and you're not a player), Riku with seventy asking for thirty-one, Go's "Let him be the
poorest", Saki's "He's still one of us", and Ren's thought: unless nobody was a player at all.

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter03, approved canon v5). The narrator opens the
chapter, reads the screen's player count (the clue: Momo isn't counted) and adds one line of arithmetic (70 + 31 =
101) so Aoi's answer is clear.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga07   -> out/stories/dma_manga07.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(3)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="q", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="q", **kw)


BEATS = [
    n(1, 1, 0, "[Chapter three.|Chapter 3:] The Charity."),
    s(2, 1, 1, "ren", "The exit led to a white room. And Momo was sitting in the middle of it.", gap=0.4),
    s(3, 2, 1, "momo", "Game two! The Charity! Twenty players! Momo just watches!"),
    n(4, 2, 2, "The screen counted the players. [Twenty.|20.]", gap=0.4),
    s(5, 2, 3, "momo", "Rule one. Nobody can take your tokens.", gap=0.4),
    s(6, 3, 1, "momo", "Rule two. You may give tokens to anyone in this room. Gifts are final."),
    s(7, 3, 2, "momo", "Rule three. When time runs out, the poorest player dies. A tie for poorest? They all die!",
      gap=0.4),
    s(8, 3, 3, "momo", "Rule four. Zero tokens, and you're not a player anymore.", gap=0.4),
    s(9, 3, 4, "momo", "Tokens are precious! You'll want them later! Ten minutes!", gap=0.4, sfx="chime"),
    s(10, 4, 1, "ren", "Riku had seventy. Fewer than anyone."),
    s(11, 4, 2, "riku", "Somebody give me thirty-one.", gap=0.4),
    n(12, 4, 2, "With thirty-one more, he'd have a hundred and one.", gap=0.3),
    s(13, 4, 3, "aoi", "Then the giver is the poorest.", gap=0.4),
    s(14, 4, 4, "go", "Let him be the poorest. He lied to all of us.", name="GO", gap=0.4),
    s(15, 5, 1, "ren", "Then the quietest girl in our class spoke. Seat fourteen. Nishida Saki."),
    s(16, 5, 2, "saki", "He's still one of us.", gap=0.5),
    s(17, 5, 3, "ren", "Riku looked at her for a long time.", gap=0.6),
    s(18, 6, 1, "mio", "Then we all hold the same. Nobody is the poorest."),
    s(19, 6, 2, "aoi", "A tie for poorest. We'd all die.", gap=0.4),
    s(20, 6, 3, "ren", "Tokens can't vanish. Somebody always holds the fewest.", gap=0.45),
    s(21, 6, 4, "ren", "Somebody in this room had to die. Unless nobody was a player at all.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="The Poorest Player Dies. A Tie Kills Everyone. | Dead Man's Algorithm Manga Ep 7 🪙",
    alt_titles=["Give Tokens to Anyone. The Poorest Player Dies 🪙", "Dead Man's Algorithm: The Manga, Episode 7 🪙"],
    description="""Game two: the Charity. Nobody can take your tokens. You may give tokens to anyone in this room.
When time runs out, the poorest player dies, and a tie for poorest kills them all. Zero tokens, and you're not a player.
Riku has the fewest. "Somebody give me thirty-one." Then the quietest girl in class speaks: "He's still one of us."

Dead Man's Algorithm, the manga, Chapter 3 "The Charity", pages 1 to 6.
Episode 8 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "charity", "game theory", "episode 7"],
    pinned_comment="Somebody always holds the fewest tokens. Can you see a way for nobody to die before Episode 8? 👇",
)

KEY = {"charity", "twenty", "rule", "take", "anyone", "room", "final", "poorest", "tie", "dies", "die", "zero",
       "player", "precious", "seventy", "fewer", "thirty", "hundred", "giver", "lied", "fourteen", "saki", "us",
       "same", "vanish", "fewest", "nobody"}


def cues(t, tl):
    """This episode's sound cues (shared with a Chapter 3 long video)."""
    B = tl.by_id
    cue("hush", t, B["q16"].end, B["q17"].end - B["q16"].end + 0.3)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 7, [("THE POOREST", False), ("PLAYER DIES.", True)], "q21", "THE LOOPHOLE", KEY)
    cues(t, tl)
