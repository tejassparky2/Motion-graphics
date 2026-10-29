"""DEAD MAN'S ALGORITHM, the manga, Episode 16 (9:16): Chapter 5 "Thirty Tokens", pages 16-20 (Part 12, second half),
the end of Chapter 5 and of Game 3. Mio turns on Kota's notebook: one coin, Saki's ("It was hers."); Haruto's
confession ("Momo said nobody would know."); Momo paid him with the tokens they gave it for Saki; Gō cut the loop
before he died and saved the nine behind him; Riku collects ("You all owe me."); Haruto's "sustainable business model"
on the first day, and today he sold Gō for thirty tokens; "The boy who killed Saki kept his word. My best friend broke
his."; Momo: "Eighteen players! Momo loves a smaller loop!"

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter05, approved canon v6). The narrator only
describes the two wordless panels (Kota holding the notebook, the one coin inside).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga16   -> out/stories/dma_manga16.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(5)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="o", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="o", **kw)


BEATS = [
    s(1, 16, 1, "mio", "And Kota. You always hold that notebook."),
    n(2, 16, 2, "Kota held it to his chest.", gap=0.4),
    n(3, 16, 3, "Between the pages, one coin.", gap=0.4),
    s(4, 16, 4, "kota", "It was hers.", gap=0.5),
    s(5, 17, 1, "haruto", "Momo said nobody would know."),
    s(6, 17, 2, "haruto", "[Riku had fixed everything. One swap. I thought, maybe they were in the same loop.|Riku had "
                          "fixed everything. One swap. I thought... maybe they were in the same loop.]", gap=0.4),
    s(7, 17, 3, "haruto", "Next game, I'd have something. I could've kept you and Yui alive.", gap=0.4),
    s(8, 18, 1, "ren", "Momo paid him with the tokens we gave it for Saki."),
    s(9, 18, 2, "ren", "Kota found his in nine. [Go cut the loop before he died.|Gō cut the loop before he died.]",
      gap=0.45),
    s(10, 18, 3, "ren", "[Go's last swap saved the nine people behind him.|Gō's last swap saved the nine people behind "
                        "him.]", gap=0.45),
    s(11, 19, 1, "riku", "Eighteen alive. Nine tokens. You all owe me."),
    s(12, 19, 2, "ren", "On the first day, Haruto said he was building a sustainable business model.", gap=0.45),
    s(13, 19, 3, "ren", "[Today he sold Go for thirty tokens.|Today he sold Gō for thirty tokens.]", gap=0.4),
    s(14, 20, 1, "ren", "The boy who killed Saki kept his word. My best friend broke his."),
    s(15, 20, 2, "ren", "I didn't know anyone in this room anymore.", gap=0.5),
    s(16, 20, 3, "momo", "Eighteen players! Momo loves a smaller loop!", gap=0.5, sfx="chime"),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="He Sold His Friend for Thirty Tokens | Dead Man's Algorithm Ep 16 🃏",
    alt_titles=["The Boy Who Killed Saki Kept His Word. My Best Friend Broke His 🃏",
                "Dead Man's Algorithm: The Manga, Episode 16 🃏"],
    description="""Thirty coins on the floor, and one more in Kota's notebook: Saki's. "It was hers."
Haruto: "Momo said nobody would know." He thought one swap was safe. Momo paid him with the tokens they gave it for
Saki. Gō cut the loop before he died, and saved the nine people behind him.
On the first day, Haruto said he was building a sustainable business model. Today he sold Gō for thirty tokens.
"The boy who killed Saki kept his word. My best friend broke his."

Dead Man's Algorithm, the manga, Chapter 5 "Thirty Tokens", pages 16 to 20: the end of Chapter 5 and of game three.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "betrayal", "thirty tokens", "episode 16"],
    pinned_comment="Haruto says he did it to keep Ren and Yui alive in the next game. Riku killed Saki but kept his "
                   "word. Who is worse: Riku or Haruto? 👇",
)

KEY = {"kota", "notebook", "chest", "coin", "hers", "nobody", "know", "fixed", "swap", "loop", "game", "alive",
       "paid", "tokens", "saki", "nine", "died", "saved", "behind", "eighteen", "owe", "first", "business", "sold",
       "thirty", "killed", "word", "friend", "broke", "anyone", "room", "players", "smaller"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 5 long video)."""
    B = tl.by_id
    cue("hush", t, B["o14"].start - 0.2, B["o15"].end - B["o14"].start + 0.3)     # Ren, alone


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 16, [("HE SOLD GŌ", False), ("FOR 30 TOKENS.", True)], "o16", "GAME FOUR", KEY)
    cues(t, tl)
