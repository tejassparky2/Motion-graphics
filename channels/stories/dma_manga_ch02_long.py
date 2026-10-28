"""DEAD MAN'S ALGORITHM, the manga, Chapter 2 "The Bids" as one long video (16:9) for the YouTube channel's long-form
tab (owner, 28 Oct 2026: "Make chapter 2 long video too").

The two Shorts' beats in reading order (Episode 5 pages 1-6, Episode 6 pages 7-11), with the same voices and takes,
so every line has already passed Whisper medium in its Short. A short silent chapter title over the chapter's title
page opens it; the Shorts' hooks and "next episode" cards are left out; the chapter ends on "CHAPTER 3 · THE
CHARITY".

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga_ch02_long   -> out/stories/dma_manga_ch02_long.mp4
"""
from motion.engine import W, H, clamp01, cue

from channels.horror import hud, hud2d
from channels.stories import manga as M, serial
from channels.stories.dma_manga import MUSIC, NARRATOR, book, setup  # noqa: F401  (render reads both)
from channels.stories.dma_manga import SERIES as NAME     # not SERIES: the pipeline would add a second chip
from channels.stories import dma_manga05 as E5, dma_manga06 as E6

TAIL = 4.0
setup()
BOOK = book(2)
EPISODES = (E5, E6)
TITLE = dict(id="t0", page=1, panel=0, text="", hold=2.4)
BEATS = [TITLE] + [b for e in EPISODES for b in e.BEATS]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()
KEY = set().union(*(e.KEY for e in EPISODES))

METADATA = dict(
    title="Dead Man's Algorithm, Chapter 2: The Bids | Original Manga Read With Voices 🔑",
    alt_titles=["He Bid 1. Everyone Else Bid 0. Then Someone Lied | Dead Man's Algorithm Ch. 2",
                "The Highest Unique Bid Wins | Dead Man's Algorithm Manga, Chapter 2"],
    description="""The Glass Auction. 20 players, 100 tokens each, one exit key. The highest unique bid wins. A tie at
the top gets you eliminated. If nobody bids at all, everyone is executed. And every bid is spent.
Riku says he's going all in. Ren does the math and makes a plan: "I bid one. Everyone else bids zero."
"And if somebody lies?" "Then let them."

Dead Man's Algorithm, Chapter 2 "The Bids": the whole chapter, every page, with a narrator and a voice for every
character.

Chapter 3, "The Charity", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#DeathGame"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "full chapter", "survival game", "death game",
          "psychological thriller", "original manga", "glass auction", "game theory", "chapter 2"],
    pinned_comment="Ren's plan let a liar win the key and still kept all twenty alive. Would you have bid one, zero, "
                   "or lied like Riku? 👇",
)


def chapter_title(cr, t, end):
    """CHAPTER 2 · THE BIDS over the chapter's title page, before the first line."""
    if t > end + 0.4:
        return
    a = clamp01(t / 0.3) * (1 - clamp01((t - end) / 0.4))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.78)
    cr.paint()
    hud2d._text(cr, "DEAD MAN'S ALGORITHM", W / 2, H * 0.36, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "CHAPTER 2", W / 2, H * 0.53, 96, (1, 1, 1, 1), hud2d.ROUND, "center", shadow=0.6)
    hud2d._text(cr, "THE BIDS", W / 2, H * 0.66, 54, hud2d.RED, hud2d.ROUND, "center", shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    last = BEATS[-1]["id"]
    hud.finish(cr, t, flash_at=[], vig=0.3, grain=0.03)
    M.series_chip(cr, f"{NAME} · CHAPTER 2")
    chapter_title(cr, t, B["t0"].end)
    if B["t0"].end + 0.3 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=H - 34, size=40, max_w=1000)
    serial.next_card(cr, t, B[last].end + 0.6, NAME, "CHAPTER 3", "THE CHARITY")
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
    for e in EPISODES:
        e.cues(t, tl)
