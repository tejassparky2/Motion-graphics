"""DEAD MAN'S ALGORITHM, the manga, Chapter 5 "Thirty Tokens" as one long video (16:9) for the YouTube channel's
long-form tab (owner, 29 Oct 2026: "Make chapter 5 shorts and long video too").

The four Shorts' beats in reading order (Episode 13 pages 1-6, Episode 14 pages 7-11, Episode 15 pages 12-15, Episode
16 pages 16-20), with the same voices and takes, so every line has already passed Whisper medium in its Short. A short
silent chapter title over the locker ring opens it; the Shorts' hooks and "next episode" cards are left out; the
chapter ends on "CHAPTER 6 · GAME FOUR" (no title for it is approved yet).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga_ch05_long   -> out/stories/dma_manga_ch05_long.mp4
"""
from motion.engine import W, H, clamp01, cue

from channels.horror import hud, hud2d
from channels.stories import manga as M, serial
from channels.stories.dma_manga import MUSIC, NARRATOR, book, setup  # noqa: F401  (render reads both)
from channels.stories.dma_manga import SERIES as NAME     # not SERIES: the pipeline would add a second chip
from channels.stories import dma_manga13 as E13, dma_manga14 as E14, dma_manga15 as E15, dma_manga16 as E16

TAIL = 4.0
setup()
BOOK = book(5)
EPISODES = (E13, E14, E15, E16)
TITLE = dict(id="t0", page=1, panel=0, text="", hold=2.4)
BEATS = [TITLE] + [b for e in EPISODES for b in e.BEATS]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()
KEY = set().union(*(e.KEY for e in EPISODES))

METADATA = dict(
    title="Dead Man's Algorithm, Chapter 5: Thirty Tokens | Original Manga Read With Voices 🃏",
    alt_titles=["Someone Swapped Two Cards for Thirty Tokens | Dead Man's Algorithm Ch. 5",
                "He Sold His Best Friend for Thirty Tokens | Dead Man's Algorithm Manga, Chapter 5"],
    description="""Riku went in first, saw every locker and kept his word: no loop longer than ten. Then Momo started
whispering offers in the locker room. "Swap TACHIBANA and HAYASHI. Thirty tokens! Nobody will know!" Everyone said
no, and nobody could prove it. Then the board said SHIBATA GŌ: NOT FOUND. Ren works out who swapped from the board
alone, and the answer breaks him.

Dead Man's Algorithm, Chapter 5 "Thirty Tokens": the whole chapter, every page, with a narrator and a voice for every
character. The end of game three.

(Original story. Original manga, read with voices. The game's maths is the published "100 prisoners problem".)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#DeathGame"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "full chapter", "survival game", "death game",
          "psychological thriller", "original manga", "100 prisoners problem", "betrayal", "chapter 5"],
    pinned_comment="Haruto says he did it to keep Ren and Yui alive in the next game. Riku killed Saki but kept his "
                   "word. Who is worse: Riku or Haruto? 👇",
)


def chapter_title(cr, t, end):
    """CHAPTER 5 · THIRTY TOKENS over the locker ring, before the first line."""
    if t > end + 0.4:
        return
    a = clamp01(t / 0.3) * (1 - clamp01((t - end) / 0.4))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.78)
    cr.paint()
    hud2d._text(cr, "DEAD MAN'S ALGORITHM", W / 2, H * 0.36, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "CHAPTER 5", W / 2, H * 0.53, 96, (1, 1, 1, 1), hud2d.ROUND, "center", shadow=0.6)
    hud2d._text(cr, "THIRTY TOKENS", W / 2, H * 0.66, 54, hud2d.RED, hud2d.ROUND, "center", shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    last = BEATS[-1]["id"]
    hud.finish(cr, t, flash_at=[], vig=0.3, grain=0.03)
    M.series_chip(cr, f"{NAME} · CHAPTER 5")
    chapter_title(cr, t, B["t0"].end)
    if B["t0"].end + 0.3 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=H - 34, size=40, max_w=1000)
    serial.next_card(cr, t, B[last].end + 0.6, NAME, "CHAPTER 6", "GAME FOUR")
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
    for e in EPISODES:
        e.cues(t, tl)
