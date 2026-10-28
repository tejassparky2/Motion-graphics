"""DEAD MAN'S ALGORITHM, the manga, Chapter 4 "Find Yourself" as one long video (16:9) for the YouTube channel's
long-form tab (owner, 28 Oct 2026: "Make chapter 4 shorts and long video too").

The three Shorts' beats in reading order (Episode 10 pages 1-7, Episode 11 pages 8-13, Episode 12 pages 14-20), with
the same voices and takes, so every line has already passed Whisper medium in its Short. A short silent chapter title
over the open door opens it; the Shorts' hooks and "next episode" cards are left out; the chapter ends on "CHAPTER 5
· THIRTY TOKENS".

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga_ch04_long   -> out/stories/dma_manga_ch04_long.mp4
"""
from motion.engine import W, H, clamp01, cue

from channels.horror import hud, hud2d
from channels.stories import manga as M, serial
from channels.stories.dma_manga import MUSIC, NARRATOR, book, setup  # noqa: F401  (render reads both)
from channels.stories.dma_manga import SERIES as NAME     # not SERIES: the pipeline would add a second chip
from channels.stories import dma_manga10 as E10, dma_manga11 as E11, dma_manga12 as E12

TAIL = 4.0
setup()
BOOK = book(4)
EPISODES = (E10, E11, E12)
TITLE = dict(id="t0", page=1, panel=0, text="", hold=2.4)
BEATS = [TITLE] + [b for e in EPISODES for b in e.BEATS]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()
KEY = set().union(*(e.KEY for e in EPISODES))

METADATA = dict(
    title="Dead Man's Algorithm, Chapter 4: Find Yourself | Original Manga Read With Voices 🔒",
    alt_titles=["Find Your Name in 10 Lockers or Die | Dead Man's Algorithm Ch. 4",
                "One Loop of Nineteen. Whoever Cuts It Dies | Dead Man's Algorithm Manga, Chapter 4"],
    description="""Game three: Find Yourself. Nineteen lockers, each holding one card with one of their names. Go in
alone, open ten lockers, find your own name, and you live. Each token opens one more. You may swap two cards, once.
Follow the cards from your own locker and you go round a loop that ends at your name. But Momo set it up as one loop
of nineteen, and nineteen is longer than ten. Ren finds how to cut the loop, and who pays for it. Only Riku has the
tokens to save everyone.

Dead Man's Algorithm, Chapter 4 "Find Yourself": the whole chapter, every page, with a narrator and a voice for every
character.

Chapter 5, "Thirty Tokens", is next.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#DeathGame"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "full chapter", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "loop", "chapter 4"],
    pinned_comment="Riku goes first and sees every locker. He could save all eighteen, or leave a loop of eleven on "
                   "purpose. Do you trust him? 👇",
)


def chapter_title(cr, t, end):
    """CHAPTER 4 · FIND YOURSELF over the open door, before the first line."""
    if t > end + 0.4:
        return
    a = clamp01(t / 0.3) * (1 - clamp01((t - end) / 0.4))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.78)
    cr.paint()
    hud2d._text(cr, "DEAD MAN'S ALGORITHM", W / 2, H * 0.36, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "CHAPTER 4", W / 2, H * 0.53, 96, (1, 1, 1, 1), hud2d.ROUND, "center", shadow=0.6)
    hud2d._text(cr, "FIND YOURSELF", W / 2, H * 0.66, 54, hud2d.RED, hud2d.ROUND, "center", shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    last = BEATS[-1]["id"]
    hud.finish(cr, t, flash_at=[], vig=0.3, grain=0.03)
    M.series_chip(cr, f"{NAME} · CHAPTER 4")
    chapter_title(cr, t, B["t0"].end)
    if B["t0"].end + 0.3 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=H - 34, size=40, max_w=1000)
    serial.next_card(cr, t, B[last].end + 0.6, NAME, "CHAPTER 5", "THIRTY TOKENS")
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
    for e in EPISODES:
        e.cues(t, tl)
