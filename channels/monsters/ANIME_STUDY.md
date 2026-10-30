# What the Pokémon TV anime does, measured frame by frame (30 Oct 2026)

Sources:
- 140 wiki screenshots from Pokémon Horizons episodes 1378-1386 (Aug-Sep 2026);
- a Sun & Moon episode (season 22, ep 14, 858x480, 21:19) that the owner supplied for study, measured with frame
  differences.

Neither is stored in the repo or used in any video; we copy the style, never designs.

| Measured | Result | Our rule |
|---|---|---|
| Shot length (Sun & Moon, 440 shots in the episode body) | median 1.65 s, mean 2.46 s; 53% under 2 s, 26% 2-4 s, 18% 4-8 s, 3% over 8 s | cut every 1.5-3 s; a long hold only for a big reveal |
| Frame steps with no change | 50% | most energy comes from camera moves over held poses |
| How long a drawing is held | 1 frame 76% (mostly camera pans), 2 frames 10%, 3 frames 11%, 5+ frames 3% | character acting on 3s (`anim.on_twos(objs, 3)`), fast action on 2s, camera and VFX on 1s |
| Lines | thin (~1.5 px at 858 wide), tapered; coloured per area (dark brown on skin, dark orange on hair, dark navy on blue); thick black upper lash line | `look.outline(..., colored=True)` gives each colour its own darker line (`line_color`, k=0.28) |
| Eyes | dark iris, lighter colour at the bottom, big round white highlight plus a small second one | creature eyes: black, a lighter coloured lower crescent, two highlights |
| Shading | mostly flat; one shadow tone only in designed places (under ears, folds, under the chin) | hard two-tone cel, threshold kept low so most surfaces stay flat |
| Backgrounds | painted, no lines; strong blur behind characters; leafy "cauliflower" trees in three greens; deep blue skies with soft white clouds | `mk/paintbg.py` |
| Composition | many low angles with characters against the sky; ambient sparkles and bubbles; big expressive mouths, sweat drops | low cameras; ambient sparkle layer (fx2d) |
| Saturation (mean HSV S of frames) | 0.34-0.61 by scene | our style frame measures 0.52, in range; make skies deeper |
