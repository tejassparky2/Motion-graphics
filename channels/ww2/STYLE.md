# WW2 Episode 1: style guide (every module and chapter follows this)

Kit: `channels/ww2/kit/core.py`, imported as `from channels.ww2.kit.core import *`. Venv: `/home/user/.venv-main/bin/python`.
Canvas: 1920x1080, 24 fps, drawn with pycairo, rendered by `render_clip(draw, dur, out)`. `still=t` writes one PNG.

## Look
- **Sketchbook documentary.** Every scene sits on parchment paper (`paper(cr)`). Lines are ink (`PAL["ink"]`, #1f1c1a) with round caps and joins. Colour is flat and muted, with no gradients except soft shadows and glows.
- **Sides are coloured, never shown by symbols:**

  | Side | Palette name | Colour |
  |---|---|---|
  | Germany | `axis` | charcoal #4b4b52 |
  | Italy | `axis_it` | #6c6c72 |
  | Japan | `axis_jp` | #3a3a42 |
  | Western Allies (Britain, France, US) | `allies` | blue #3f6fb5 |
  | Soviet Union | `soviet` | red #b8382e |
  | China | `china` | gold #cf9f2a |
  | Neutral / not at war | `land` | #ddd2b6 |
  | Sea | `sea` | #b8cfd3 |

- **Attack arrows:** the attacker's side colour, with an ink outline and a white inner highlight. They grow along their path, never pop in whole.
- **No Nazi symbols at all.** No swastika, no SS runes, no Nazi eagle, no flags with symbols. Germany is charcoal plus a label. Generic insignia are fine: plain roundels on Allied planes, a plain white star on US vehicles, a plain red star on Soviet ones, a plain cross-free grey on German ones.
- **No graphic violence.** No blood, no bodies, no visible deaths. Battles are shown with flashes, smoke, shaking, arrows, and figures diving or ducking. Losses are shown as numbers or as figures fading out on a map.

## Type
| Font | Use |
|---|---|
| `TITLE` = Anton | Chapter cards, word cards, big numbers, the date tag |
| `HAND` = Kalam Bold | Map labels, notes and name tags |
| `UI` = Inter | Small print only |

Labels sit on the paper colour with a paper-coloured outline (`text(..., outline="paper")`) so they read over maps.

## Stick figures (stick.py)
- **Size:** standard figure height 300 px at zoom 1 (head 64 px across). Limbs are ink lines 7 px wide, the head is a filled paper-coloured circle with a 6 px ink outline. Crowds use the same rig at 0.4-0.6 scale.
- **Faces:**
  - expressive: dot eyes, brows that tilt for anger or worry, a mouth line or an O;
  - eyes blink every 2-5 s;
  - a little sweat drop for fear.
- **Nation is shown by headgear tinted in its side colour:**

  | Nation | Headgear |
  |---|---|
  | German | flared helmet |
  | British | flat dish helmet |
  | US | round M1 helmet |
  | Soviet | rounded helmet or side cap |
  | French | crested helmet |
  | Japanese | peaked cap with neck flaps |
  | Italian | helmet with a small feather plume (Bersaglieri) |

  Civilians get flat caps, hats and headscarves in neutral colours.
- **Leaders** are stick figures with ONE trademark each, drawn respectfully (no mockery beyond the trademark):

  | Leader | Trademark |
  |---|---|
  | Hitler | toothbrush moustache, side-swept hair |
  | Stalin | thick moustache, pipe, swept-back hair |
  | Churchill | bowler hat, cigar, round head |
  | Roosevelt | pince-nez glasses, cigarette holder |
  | Mussolini | bald head, square jaw |
  | Hirohito | round glasses, small moustache |
  | Chamberlain | moustache, umbrella, homburg hat |

- **Motion:**
  - poses blend with eased interpolation;
  - idle figures breathe (a 2 px bob) and shift weight;
  - nothing ever freezes completely;
  - figures walk, run, point, shrug, salute, shake hands, cheer, crouch, dive, wave a paper, and aim and fire (with a muzzle flash only).

## Vehicles and props (props.py)
- Same ink line weight (5-7 px at zoom 1), flat fills in the side colour.
- Tank, fighter, bomber, dive bomber, battleship, aircraft carrier, destroyer, small boats (fishing boat, yacht, ferry), submarine and periscope, artillery, radar tower, searchlight, sandbags and trench, train.
- Everything animates: tank tracks roll, propellers spin, ships leave wakes and bob, smoke drifts, and explosions are a flash, a ring and a smoke puff (no debris gore).

## Maps (maps.py)
- Data: Natural Earth only (public domain). Historical borders (1939 Poland, 1938 Germany plus Austria, and so on) are built from Natural Earth admin-1 provinces where possible.
- Europe uses a Lambert azimuthal equal-area projection centred near 15°E 52°N. The Pacific gets its own view centred on 160°E; the world uses Robinson or Equal Earth.
- Countries are filled in side colours on `land`, coastlines are ink 2.5 px, borders are `ink_soft` 1.5 px, the sea is `sea` with faint hatching near the coast, and labels are Kalam.
- Animation:
  - colours flood outward from a point (they don't just switch);
  - front lines are thick wobbly lines that move;
  - city dots pulse when named;
  - the map camera pans and zooms smoothly.

## Every shot
- A slow push-in over the shot (`push_in`).
- A visual change about every 1-2 seconds.
- The corner date tag (`date_stamp`).
- Sound cues are noted with `engine.cue(name, t, start)` for the mix, or listed in the scene's docstring.
- Clean outputs only: no metadata or encoder tags (`render_clip` already strips them).
