"""DEAD MAN'S ALGORITHM, the manga, Episode 11 (9:16): Chapter 4 "Find Yourself", pages 8-13. Riku can't lose; Ren asks
Kota for a page (Kota keeps the notebook shut); Ren's five-locker drawing (start at your own locker, follow the cards,
the card that leads back to your locker is your name); Aoi's long-loop odds; "Everyone's connected": the line on the
floor is one circle, so it's one loop of nineteen, and nineteen is longer than ten.

Ren's first-person captions and off-panel lines are spoken in Ren's voice (chip REN); every character line and
caption is word for word as lettered on the manga chat's pages (tejassparky2/Manga, story/chapter04, approved canon
v6). The narrator describes the wordless panels and walks B's path on Ren's drawing (B, D, A, C, E; locker E holds B),
exactly as the panel shows it.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga11   -> out/stories/dma_manga11.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(4)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="y", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="y", **kw)


BEATS = [
    s(1, 8, 1, "ren", "Riku couldn't lose this game. Only we could."),
    s(2, 8, 2, "mio", "Then he walks out, and we flip coins.", gap=0.4),
    s(3, 8, 3, "ren", "I needed paper.", gap=0.4),
    s(4, 8, 4, "ren", "Kota. Can I have a page?", gap=0.35),
    n(5, 9, 1, "Kota held his notebook shut."),
    n(6, 9, 2, "He tore out one page. Carefully. The notebook stayed closed.", gap=0.4),
    n(7, 9, 3, "Ren knelt on the floor and drew.", gap=0.4),
    s(8, 10, 1, "ren", "[Start, at your own locker.|Start at your own locker.] The card tells you which locker to open "
                       "next."),   # "Start at" was heard "Starting"
    s(9, 10, 2, "ren", "Every card points somewhere. Follow them and you go round in a loop.", gap=0.4),
    s(10, 10, 3, "ren", "[And the card that leads back to your own locker is your name.|And the card that leads back to "
                        "your own locker... is your name.]", gap=0.4),
    n(11, 10, 3, "Say you're B. Open B, and the card says D. D says A. A says C. C says E. And E holds B.", gap=0.4),
    s(12, 11, 1, "haruto", "So we just follow the arrows?"),
    s(13, 11, 2, "aoi", "If your loop is ten or shorter, you find it. If it's longer, everyone in that loop dies "
                        "together.", gap=0.4),
    s(14, 11, 3, "aoi", "[Random lockers. About six times in ten, there's a long loop.|Random lockers... About six "
                        "times in ten, there's a long loop.]", gap=0.4),
    n(15, 11, 4, "Then he looked toward the open door.", gap=0.45),          # "Ren looked" was heard "Wren, look"
    s(16, 12, 1, "ren", "[Everyone's connected.|\"Everyone's connected.\"] I looked at the line on the floor. One "
                        "circle. No breaks."),
    s(17, 12, 2, "ren", "It's not random. It's one loop. All nineteen of us.", gap=0.45),
    s(18, 12, 3, "aoi", "[Then everyone opens ten, and nobody gets there.|Then everyone opens ten... and nobody gets "
                        "there.]", gap=0.4),
    s(19, 13, 1, "ren", "Nineteen is longer than ten."),
    s(20, 13, 2, "ren", "Every one of us would die.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Follow the Cards and You Find Your Name. Unless It's One Loop | Dead Man's Algorithm Ep 11 🔒",
    alt_titles=["The Line on the Floor Was One Circle 🔒", "Dead Man's Algorithm: The Manga, Episode 11 🔒"],
    description="""Start at your own locker. The card tells you which locker to open next. Follow the cards and you go
round in a loop, and the card that leads back to your own locker is your name.
If your loop is ten or shorter, you find it. But Momo said everyone's connected, and the line on the floor is one
circle. One loop of nineteen. Nineteen is longer than ten.

Dead Man's Algorithm, the manga, Chapter 4 "Find Yourself", pages 8 to 13.
Episode 12 is next.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "loop", "episode 11"],
    pinned_comment="It's one loop of nineteen, and each of them can open ten. Can you see a way out before Episode "
                   "12? Hint: read rule four 👇",
)

KEY = {"lose", "coins", "paper", "page", "notebook", "closed", "drew", "locker", "card", "loop", "name", "points",
       "arrows", "ten", "shorter", "longer", "dies", "together", "random", "six", "door", "connected", "circle",
       "breaks", "nineteen", "nobody", "die"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 4 long video)."""
    B = tl.by_id
    cue("riser", t, B["y15"].start, B["y17"].end - B["y15"].start)
    cue("sting", t, B["y17"].end + 0.05)
    cue("hush", t, B["y20"].start - 0.2, B["y20"].end - B["y20"].start + 0.4)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 11, [("ONE LOOP.", False), ("NINETEEN OF US.", True)], "y20", "CUT THE LOOP", KEY)
    cues(t, tl)
