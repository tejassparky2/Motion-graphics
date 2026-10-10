# Polished animation style (ported from the Interestingly Strange channel, 10 Oct 2026)

The owner wants Body Facts to use the same high-quality look as the newest Interestingly Strange videos (the honeybee,
Last Bencher 4 and paradox videos): smooth vector shapes with gradients, soft shadows, depth-of-field bokeh,
vignettes, chunky bouncing signs, counters and stamps, and bold rounded captions. Nothing here changes this
branch's existing voice, timeline, render or caption code, so the existing Body Facts videos still render exactly as
before.

## What's new on this branch
| File | What it gives you |
|---|---|
| `motion/polish.py` | Smooth shapes (`ellipse`, `rrect`, `smooth`), gradients (`lin`, `rad`), `paint`, blurred cached `sprite`s, `bokeh`, `light_rays`, `particles`, `vignette`, camera keys (`camera`, `enter`), chunky text (`bold_text`), `sign`, `counter`, `stamp`, and `captions` (Fredoka, spoken word in yellow) |
| `motion/toons.py` | Big-headed polished characters: `person(cr, t, x, y, s, who=...)` with poses, faces, walking. Cast includes **`doctor`** (white coat, teal scrubs, stethoscope), **`doctor2`** (glasses, bun), **`patient`** (hospital gown), plus kids, teacher and others. Also `head`, `portrait` (reaction bubble), animals |
| `motion/pkit.py` | UI pieces: `card` (header + lines + ✔/✘), `buttons` (end question), `bubble` (speech), `tag`, `calendar`, `knot`, `check`, `red_x`, `sparkles`, `shake`, `studio` (soft backdrop) |
| `motion/bees.py` | Shared eye, eyelid and mouth drawing used by `toons.py` |
| `assets/fonts/Fredoka-*.ttf`, `LuckiestGuy-Regular.ttf` | Caption and sign fonts (SIL OFL) |

## How a polished video file looks
Copy the structure of any Interestingly Strange polished video (for example `videos/immortal_jellyfish.py` on branch
`ccr-56282fe5-evehq4`): one `scene_<name>(cr, t, tl)` per scene, every animation keyed to a spoken word with
`tl.at(id, "word")`, then:

```python
from motion.kit import whip
from motion.polish import captions

def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)      # polished captions at y=905
```

Layout rules that keep it clean: signs at y ≈ 120–230, faces and cards above y ≈ 860, captions at 905, nothing
cut off at the edges. Check a contact sheet (`render.py --sheet 1`) before the full render.

## Optional: character voices
On the channel branch, `voice.SPEAKERS = {"doc": dict(voice="am_michael", speed=1.0, pitch=0)}` gives each character
their own Kokoro voice (commit 2f8568e there: `motion/voice.py` + `motion/timeline.py`). This branch has its own
edits to those files, so port it by hand if the owner wants it.
