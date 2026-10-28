"""DEAD MAN'S ALGORITHM, the manga, Episode 12 (9:16): Chapter 4 "Find Yourself", pages 14-20, the end of Chapter 4.
Rule four again: whoever opens ten and doesn't find their name swaps their first and tenth cards, cutting the loop
into nine and ten, and dies; Go volunteers ("Stay behind me."); Ren's way for nobody to die (nine tokens buy sight of
all nineteen); Riku refuses ("I go first."), names his price ("Eighteen lives for nine tokens. Every one of you owes
me."), and Ren's plan for everyone after him. Ends on Riku at the door: "Remember. You owe me."

Ren's first-person captions and off-panel lines are spoken in Ren's voice (chip REN); every character line and
caption is word for word as lettered on the manga chat's pages (tejassparky2/Manga, story/chapter04, approved canon
v6). The narrator only describes one wordless panel (Kota grabbing Go's sleeve).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga12   -> out/stories/dma_manga12.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(4)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="z", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="z", **kw)


BEATS = [
    s(1, 14, 1, "ren", "Then I read rule four again. Swap two cards."),
    s(2, 14, 2, "ren", "Whoever opens ten and doesn't find their name knows it's the long loop.", gap=0.4),
    s(3, 14, 3, "ren", "Swap the card in your first locker with the card in your tenth. The loop breaks in two.",
      gap=0.4),
    s(4, 15, 1, "ren", "One loop of nine. The other is what's left. Nineteen minus nine is ten."),
    s(5, 15, 2, "aoi", "Ten or shorter. Everyone after you finds their name.", gap=0.4),
    s(6, 15, 3, "ren", "Except the one who cuts it.", gap=0.5),
    s(7, 16, 1, "ren", "Silence."),
    s(8, 16, 2, "go", "Then I go first. If it's one loop, I'll be the one who cuts it.", name="GO", gap=0.6),
    n(9, 16, 3, "Kota grabbed his sleeve.", gap=0.45),
    s(10, 16, 4, "go", "Stay behind me.", name="GO", gap=0.45),
    s(11, 17, 1, "ren", "Ten free. Nine more makes nineteen. Whoever goes first with nine tokens sees everything."),
    s(12, 17, 2, "ren", "Nobody has to die. Riku. Give Go nine tokens.", gap=0.4),
    s(13, 17, 3, "riku", "My tokens don't leave my hands. I go first.", gap=0.4),
    s(14, 18, 1, "mio", "Then he decides who dies."),
    s(15, 18, 2, "ren", "If he sees every locker, he can cut the loop anywhere. He could leave a loop of eleven. On "
                        "purpose.", gap=0.4),
    s(16, 18, 3, "riku", "Or I save all of you.", gap=0.4),
    s(17, 18, 4, "riku", "Eighteen lives for nine tokens. Every one of you owes me.", gap=0.4),
    s(18, 19, 1, "ren", "Nine of us dead on average. One of us dead for sure. Or none of us, if he keeps his word."),
    s(19, 19, 2, "ren", "He goes first. I go second. I'll know if he lied.", gap=0.4),
    s(20, 19, 3, "riku", "You'll know.", gap=0.4),
    s(21, 20, 1, "ren", "[Everyone else. Follow the chain.|Everyone else: follow the chain.] Find your name, touch "
                        "nothing. Fail, cut first and tenth."),
    s(22, 20, 2, "ren", "[And whatever Momo offers you, say no.|And whatever Momo offers you... say no.]", gap=0.4),
    s(23, 20, 3, "riku", "Remember. You owe me.", gap=0.5),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="Eighteen Lives for Nine Tokens. Every One of You Owes Me | Dead Man's Algorithm Ep 12 🔒",
    alt_titles=["Whoever Cuts the Loop Dies. He Volunteered 🔒", "Dead Man's Algorithm: The Manga, Episode 12 🔒"],
    description="""Rule four: swap two cards, once. Whoever opens ten lockers and doesn't find their name cuts the loop:
first locker with tenth. One loop of nine, one of ten, and everyone after them lives. Except the one who cuts it.
Go volunteers. But nobody has to die: ten free opens plus nine tokens shows all nineteen lockers. Only Riku has nine.
"My tokens don't leave my hands. I go first."

Dead Man's Algorithm, the manga, Chapter 4 "Find Yourself", pages 14 to 20: the end of Chapter 4.
Chapter 5, "Thirty Tokens", is next.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "loop", "episode 12"],
    pinned_comment="Riku goes first and sees every locker. He could save all eighteen, or leave a loop of eleven on "
                   "purpose. Do you trust him? 👇",
)

KEY = {"rule", "swap", "cards", "ten", "long", "loop", "first", "tenth", "breaks", "nine", "except", "cuts",
       "silence", "behind", "nineteen", "everything", "nobody", "die", "tokens", "hands", "dies", "anywhere",
       "eleven", "purpose", "save", "eighteen", "owes", "average", "sure", "word", "second", "lied", "know", "chain",
       "nothing", "fail", "say", "remember", "owe"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 4 long video)."""
    B = tl.by_id
    cue("hush", t, B["z7"].start - 0.2, B["z8"].start - B["z7"].start + 0.1)
    cue("heartbeat", t, B["z8"].start, B["z10"].end - B["z8"].start)
    cue("riser", t, B["z15"].start, B["z17"].end - B["z15"].start)
    cue("heartbeat", t, B["z21"].start, B["z23"].end - B["z21"].start)


def draw(cr, t, tl):
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 12, [("WHO CUTS", False), ("THE LOOP?", True)], "z23", "THIRTY TOKENS", KEY)
    cues(t, tl)
