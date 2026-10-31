# WW2 Episode 1: production contract for the 8 packages

The owner approved the poster look, the male British narrator and the ~11-13 min length (31 Oct 2026). Branch: `ccr-56282fe5-evehq4-ww2`. Pull before every push.

## The clock
- `channels/ww2/ep01/timing.json` is the episode clock. Read it only through `from channels.ww2.ep01.timing import Timing, package_span`.
- It is **provisional** (`T.estimated == True`) until the voiced narration lands, about 1 h from 22:15 UTC. Then the real timing replaces it and every time shifts.
- So **never hard-code seconds.** Place every beat relative to `T.line(id).start/.end` or `T.sentence(id, k).start`, plus small offsets.
- Your package covers `package_span("Pn")`. It begins at the chapter card if your first line opens a chapter, otherwise halfway through the pause before your first line.
- Chapter cards (`T.chapter(c).card`) fall inside the package whose lines they introduce. Draw them with `core.chapter_card` plus the newsreel fanfare cue.

| Pkg | Lines | Animator |
|---|---|---|
| P1 | 1-16 | helper 10 |
| P2 | 17-35 | helper 9 |
| P3 | 36-53 | XprL |
| P4 | 54-69 | helper 1 |
| P5 | 70-86 | bGqrs |
| P6 | 87-101 | helper 4 |
| P7 | 102-116 | helper 5 |
| P8 | 117-131 | helper 9 (after P2) |

- Assembly, YouTube chapters and the thumbnail: helper 8.
- Final mix (score, SFX from your `cues()`, narration): helper 7.

## The module: `channels/ww2/ep01/pN.py`
```python
from channels.ww2.kit.core import *          # paper, text, rays, halftone, print_finish, date_stamp, ...
from channels.ww2.ep01.timing import Timing
T = Timing()
def draw(cr, t):            # t = EPISODE seconds; must draw a complete frame for any t in package_span("Pn")
    ...
    print_finish(cr, t)     # last
def cues(T):                # [(episode_time, sfx_name, gain_db, pan -1..1)] for helper 7's mix; names from sound.SFX
    return [...]
```
- Shots come from `channels/ww2/SHOTLIST.md`. Use the shared kit:
  - `maps.py` + `map_content.py`: views, eras, fronts, arrows, zones, pins (see `channels/ww2/MAPS.md`);
  - `stick.py`: poster figures and actions;
  - `heads.py`: faces and `portrait()`;
  - `setpieces.py`: squads, columns, crowds, radio family, snow, prisoners;
  - `props.py` / `things.py` / `fx.py` / `sets.py`: XprL's vehicles, props, effects and backgrounds.
- Style references (the quality bar): `out/ww2/style/` → `dunkirk_mid.png`, `map_1939_mid.png`, `leaders_pact_mid.png`, `heads_sheet.png`.

## Rules (STYLE.md has them all)
- **Poster look:**
  - flat inks, key lines, halftone shading, slab or stencil type;
  - a slow push-in on every shot, and a visual change every 1-2 s;
  - the corner `date_stamp` on every shot, with the right month and year.
- **No Nazi symbols, no Rising Sun, no red rays, no graphic violence.** Battles are flashes, smoke, arrows and ducking. Losses are numbers.
- **Holocaust chapter (P6):**
  - maps, rail lines, numbers and text only; no figures of victims;
  - muted map;
  - the music drops to the low tone.
- **Clean encoding:**
  - no per-frame full-screen noise (the grain is static);
  - `render_clip` defaults to crf 16;
  - outputs carry no tags.
- **Speed:** keep a frame under ~0.6 s (cache static layers to surfaces).

## Render and hand-in
- Review: `python channels/ww2/ep01/render_pkg.py Pn --sheet` (1 frame per 2 s) and `--still <t>` for spot checks.
- Final: `python channels/ww2/ep01/render_pkg.py Pn` writes **600-frame chunks** `out/ww2/ep01/parts/Pn_f00000-00599.mp4`, `Pn_f00600-01199.mp4`, … at crf 18. Each must be ≤ 95 MB (GitHub's limit is 100 MB); the tool warns if one isn't, and then you re-render that range in halves with `--frames A-B`. Split the work across helpers by range if you like. Helper 8's assemble.py joins the chunks frame-exact; never hand-join or re-encode them.
- **Don't render the final until the voiced timing lands** (`T.estimated == False`). Build and review against the provisional clock, then re-render once.
- Push `pN.py`, the sheet and the final part, then tell the coordinator (session_0153qDV4AufFgT2PhEBEfS8n). Also tell helper 8 (assembly) and helper 7 (mix).
