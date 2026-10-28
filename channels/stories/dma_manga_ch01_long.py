"""DEAD MAN'S ALGORITHM, the manga, Chapter 1 "12:17" as one long video (16:9) for the YouTube channel's long-form tab
(owner, 28 Oct 2026: "after chapter 1 in shorts make chapter 1 long video for youtube in long videos format").

The four Shorts' beats in reading order (Episode 1 pages 1-7, Episode 2 pages 8-14, Episode 3 pages 15-21, Episode 4
pages 22-26), with the same voices and takes, so every line has already passed Whisper medium in its Short. A silent
chapter title over page 1 opens it; the Shorts' hooks and "next episode" cards are left out; the chapter ends on
"CHAPTER 2 · THE BIDS".

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga_ch01_long   -> out/stories/dma_manga_ch01_long.mp4
"""
from motion.engine import W, H, clamp01, cue

from channels.horror import hud, hud2d
from channels.stories import manga as M, serial
from channels.stories.dma_manga import MUSIC, NARRATOR, SERIES, book, setup  # noqa: F401  (render reads both)
from channels.stories import dma_manga01 as E1, dma_manga02 as E2, dma_manga03 as E3, dma_manga04 as E4

TAIL = 4.0
setup()
BOOK = book(1)
EPISODES = (E1, E2, E3, E4)
TITLE = dict(id="t0", page=1, panel=0, text="", hold=3.4)
BEATS = [TITLE] + [b for e in EPISODES for b in e.BEATS]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()
KEY = set().union(*(e.KEY for e in EPISODES))

METADATA = dict(
    title="Dead Man's Algorithm, Chapter 1: 12:17 | Original Manga Read With Voices ☄️",
    alt_titles=["A Meteor Hit Our Class. Then a Mouse Started a Death Game | Dead Man's Algorithm Ch. 1",
                "20 Students, 1 Key, 10 Minutes | Dead Man's Algorithm Manga, Chapter 1"],
    description="""Class 3-B. An ordinary school, on an ordinary day. At 12:17, a meteor strikes.
They wake up in a sealed concrete chamber. No teacher. No signal. No clock. A screen reads 20 SURVIVORS and STATUS OF
EARTH: UNKNOWN. Then a small white mouse called Momo introduces itself as the administrator of Dead Man's Algorithm,
and starts the first game: the Glass Auction. 20 players, 100 tokens each, one exit key.

Dead Man's Algorithm, Chapter 1 "12:17": the whole chapter, every page, with a narrator and a voice for every
character.

Chapter 2, "The Bids", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#DeathGame"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "full chapter", "survival game", "death game",
          "psychological thriller", "original manga", "glass auction", "chapter 1"],
    pinned_comment="You have 100 tokens and ten minutes. The highest UNIQUE bid wins the key, and a tie at the top "
                   "gets you eliminated. What do you bid, and why? 👇",
)


def chapter_title(cr, t, end):
    """CHAPTER 1 · "12:17" over the first page, before the first line."""
    if t > end + 0.4:
        return
    a = clamp01(t / 0.3) * (1 - clamp01((t - end) / 0.4))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.78)
    cr.paint()
    hud2d._text(cr, "DEAD MAN'S ALGORITHM", W / 2, H * 0.36, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "CHAPTER 1", W / 2, H * 0.53, 96, (1, 1, 1, 1), hud2d.ROUND, "center", shadow=0.6)
    hud2d._text(cr, "12:17", W / 2, H * 0.66, 54, hud2d.RED, hud2d.ROUND, "center", shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    last = BEATS[-1]["id"]
    hud.finish(cr, t, flash_at=[], vig=0.3, grain=0.03)
    M.series_chip(cr, f"{SERIES} · CHAPTER 1")
    chapter_title(cr, t, B["t0"].end)
    if B["t0"].end + 0.3 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=H - 34, size=40, max_w=1000)
    serial.next_card(cr, t, B[last].end + 0.6, SERIES, "CHAPTER 2", "THE BIDS")
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
    for e in EPISODES:
        e.cues(t, tl)
