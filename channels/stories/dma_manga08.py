"""DEAD MAN'S ALGORITHM, the manga, Episode 8 (9:16): Chapter 3 "The Charity", pages 7-12. The loophole: zero tokens
and you're not a player, "One player is always the poorest!", rule two again ("Anyone in this room. Not any player.
Anyone."), give Momo everything, the giving, one player left (Riku), "Then you're the only player", Riku's smile, ten
seconds, and Riku walking across the room to Saki.

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter03, approved canon v5).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga08   -> out/stories/dma_manga08.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(3)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="u", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="u", **kw)


BEATS = [
    s(1, 7, 1, "ren", "Zero tokens, and you're not a player. If nobody is a player, nobody is the poorest."),
    s(2, 7, 2, "aoi", "But the tokens have to go somewhere. Whoever holds them is a player.", gap=0.4),
    s(3, 7, 3, "haruto", "Then give them all to one person.", gap=0.4),
    s(4, 7, 4, "momo", "One player is always the poorest!", gap=0.4),
    s(5, 8, 1, "ren", "Then I read rule two again. Anyone in this room."),
    s(6, 8, 2, "ren", "Not any player. Anyone.", gap=0.45),
    s(7, 8, 3, "ren", "And Momo was in this room.", gap=0.45),
    s(8, 8, 4, "momo", "[For Momo?! How generous!|For Momo? How generous!]", gap=0.4, sfx="chime"),   # was heard "for mama"
    s(9, 9, 1, "ren", "Momo isn't a player. Give Momo everything, and there are no players. And nobody dies."),
    s(10, 9, 2, "mio", "And walk into game three with nothing?", gap=0.4),
    s(11, 9, 3, "haruto", "Tokens or our lives? That's easy.", gap=0.4),
    s(12, 10, 1, "ren", "One by one, we gave Momo everything."),
    s(13, 10, 2, "saki", "It's okay. I never wanted them.", gap=0.45),
    s(14, 10, 3, "ren", "One player was left. Riku.", gap=0.45),
    s(15, 11, 1, "riku", "I'm not walking into game three with nothing."),
    s(16, 11, 2, "ren", "Then you're the only player. And the only player is always the poorest.", gap=0.4),
    s(17, 11, 3, "ren", "Riku just smiled.", gap=0.5),
    s(18, 12, 1, "ren", "Riku was the only player left. Ten seconds. And he was smiling.", sfx="ding"),
    s(19, 12, 2, "ren", "He walked across the room. To Saki.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Give Everything to the Host and Nobody Dies? | Dead Man's Algorithm Manga Ep 8 🪙",
    alt_titles=["The Loophole Was in Rule Two 🪙", "Dead Man's Algorithm: The Manga, Episode 8 🪙"],
    description="""The poorest player dies. Zero tokens, and you're not a player. "One player is always the poorest!"
Then Ren reads rule two again: give tokens to anyone in this room. Not any player. Anyone. And Momo is in this room.
One by one, they give Momo everything. One player is left: Riku. Ten seconds. And he's smiling.

Dead Man's Algorithm, the manga, Chapter 3 "The Charity", pages 7 to 12.
Episode 9 is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "charity", "loophole", "episode 8"],
    pinned_comment="Riku is the only player left, with ten seconds on the clock, and he's smiling. What is he about "
                   "to do? 👇",
)

KEY = {"zero", "player", "nobody", "poorest", "somewhere", "holds", "one", "rule", "anyone", "room", "momo",
       "generous", "everything", "dies", "nothing", "lives", "easy", "wanted", "left", "riku", "only", "smiled",
       "seconds", "smiling", "saki"}


def cues(t, tl):
    """This episode's sound cues (shared with a Chapter 3 long video)."""
    B = tl.by_id
    cue("riser", t, B["u5"].start, B["u7"].end - B["u5"].start)
    cue("hush", t, B["u7"].end, B["u8"].start - B["u7"].end + 0.1)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 8, [("GIVE IT ALL", False), ("TO MOMO?", True)], "u19", "THE GIFT", KEY)
    cues(t, tl)
