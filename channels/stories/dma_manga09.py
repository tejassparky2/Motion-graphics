"""DEAD MAN'S ALGORITHM, the manga, Episode 9 (9:16): Chapter 3 "The Charity", pages 13-19, the end of Chapter 3.
Three seconds: Riku puts one token in Saki's hand ("A gift! Gifts are final!"), players two, the poorest is Saki,
nobody has a token left to stop it, "Saki! Give it to Momo!", she can't ("He's still one of us"), time's up, the
lights go out, nineteen survivors, "She was the only one I trusted.", "Riku found the loophole in my loophole." No
gore: the lights go out and her token lies on the floor.

Ren's first-person captions are spoken in Ren's voice (chip REN); every character line and caption is word for word as
lettered on the manga chat's pages (tejassparky2/Manga, story/chapter03, approved canon v5). The narrator only reads
the timer at zero.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga09   -> out/stories/dma_manga09.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(3)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="w", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="w", **kw)


BEATS = [
    s(1, 13, 1, "ren", "Three seconds left.", sfx="ding"),
    s(2, 13, 2, "ren", "He put one token in her hand.", gap=0.45),
    s(3, 13, 3, "momo", "A gift! Gifts are final!", gap=0.4, sfx="chime"),
    s(4, 13, 4, "ren", "The screen changed. Players, two.", gap=0.4),
    s(5, 14, 1, "ren", "One token made her a player again. The poorest one."),
    s(6, 14, 2, "ren", "None of us had a single token left to stop it.", gap=0.45),
    s(7, 14, 3, "ren", "If she gave it to Momo, Riku would be alone again. And he would die.", gap=0.45),
    s(8, 15, 1, "ren", "Saki! Give it to Momo!", impact=True),
    s(9, 15, 2, "ren", "I was telling her to kill him. I didn't care.", gap=0.45),
    s(10, 15, 3, "ren", "Saki looked at Riku. She couldn't do it.", gap=0.45),
    s(11, 16, 1, "ren", "Riku knew she couldn't. He'd heard her say it."),
    s(12, 16, 2, "saki", "He's still one of us.", gap=0.5),
    n(13, 16, 3, "[Zero.|00:00.]", gap=0.5, sfx="ding", impact=True),
    s(14, 17, 1, "momo", "Time's up! Kanzaki Riku, sixty-nine. Nishida Saki, one!"),
    s(15, 17, 2, "ren", "The lights went out.", gap=0.6),
    s(16, 18, 1, "ren", "When they came back, Saki was gone. Her token lay on the floor.", gap=1.0),
    s(17, 18, 2, "ren", "The screen said nineteen survivors.", gap=0.5),
    s(18, 19, 1, "riku", "She was the only one I trusted."),
    s(19, 19, 2, "ren", "I found the loophole. Riku found the loophole in my loophole.", gap=0.6),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="He Gave Her One Token. Then the Lights Went Out. | Dead Man's Algorithm Manga Ep 9 🪙",
    alt_titles=["Riku Found the Loophole in My Loophole 🪙", "Dead Man's Algorithm: The Manga, Episode 9 🪙"],
    description="""Three seconds left. Riku puts one token in Saki's hand. "A gift! Gifts are final!"
Now there are two players, and Saki is the poorest. Nobody has a token left to stop it. "Saki! Give it to Momo!"
She can't. The lights go out. Nineteen survivors.
"I found the loophole. Riku found the loophole in my loophole."

Dead Man's Algorithm, the manga, Chapter 3 "The Charity", pages 13 to 19: the end of Chapter 3.
Chapter 4, "Find Yourself", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "charity", "loophole", "plot twist", "episode 9"],
    pinned_comment="Should Saki have given the token to Momo? Riku would have died, and she would have lived. What "
                   "would you have done? 👇",
)

KEY = {"three", "seconds", "token", "hand", "gift", "final", "two", "poorest", "single", "stop", "alone", "die",
       "saki", "momo", "kill", "care", "couldn't", "us", "zero", "sixty", "one", "lights", "gone", "floor",
       "nineteen", "survivors", "trusted", "loophole"}


def cues(t, tl):
    """This episode's sound cues (shared with a Chapter 3 long video)."""
    B = tl.by_id
    cue("hush", t, B["w15"].start - 0.2, B["w16"].start - B["w15"].start + 0.2)   # the lights go out


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 9, [("ONE TOKEN.", False), ("THREE SECONDS.", True)], "w19", "FIND YOURSELF", KEY)
    cues(t, tl)
