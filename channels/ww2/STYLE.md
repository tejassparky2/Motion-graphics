# WW2 Episode 1: style guide, "Animated 1940s posters" (owner's choice, 31 Oct 2026)

The owner said "many done stick man, can we do something unique but with good quality" and picked the animated 1940s posters. Every frame should look like a wartime poster or a printed war map come to life: bold flat shapes, strong silhouettes, halftone dots, few colours, period lettering, on aged paper.

Kit: `channels/ww2/kit/core.py`, imported as `from channels.ww2.kit.core import *`. Venv: `/home/user/.venv-main/bin/python`.
Canvas: 1920x1080, 24 fps, pycairo. Render with `render_clip(draw, dur, out)`; `still=t` writes one PNG. Every frame ends with `print_finish(cr, t)` (grain, specks, press wear).

## Look
- **Poster composition.**
  - Low or heroic angles, big diagonals and silhouettes against plain or rayed backgrounds.
  - Strong foreground/background separation.
  - Text is part of the design: slab headlines, stencil labels.
- **Inks.** Flat fills only. Shading is done by:
  1. a hard-edged shadow shape in a darker tone, or
  2. halftone dots: `halftone(cr, path, color, density 1-5)`.

  No smooth gradients except the paper's vignette.
- **Few colours per scene:** paper plus 3-4 inks from `PAL`. Key lines in `ink` (#1c1917), 6-8 px for main figures and 3-4 px for detail. A slight misregistration (a fill offset 2-4 px from its key line) is welcome on big shapes.
- **Background tools:**
  - `rays(cr, t, cx, cy, color=...)`, a slow sunburst;
  - `paper(cr)`, the aged print paper.
  - **Never red rays from a red or white disc.** That is Japan's Rising Sun flag, which is offensive in Korea and China. Rays are ink, gold, blue or khaki only, and never centred on a red circle.

## Sides are colours, never symbols
| Side | Palette name | Colour |
|---|---|---|
| Germany | `axis` | charcoal #45434a |
| Italy | `axis_it` | #6a6770 |
| Japan | `axis_jp` | #34323a |
| Western Allies | `allies` | navy-blue #2f5f8f |
| Soviet Union | `soviet` | poster red #b5322a |
| China | `china` | mustard #d39b2c |
| Neutral | `land` | #e3d3ad |
| Sea | `sea` | grey-green #9db3ad |

- **No Nazi symbols at all:** no swastika, no SS runes, no Nazi eagle, no Nazi or Imperial Japanese flags, and no real propaganda slogans.
- Generic marks only: a plain roundel, a plain white star (US) or a plain red star (Soviet). German vehicles and uniforms stay plain charcoal.
- **No graphic violence.** No blood, no bodies, no visible deaths. Battles are flashes, smoke, flat star-burst explosions, arrows and ducking figures. Losses are numbers, or figures fading out on a map.

## Type
| Font | Use |
|---|---|
| `SLAB` = Alfa Slab One | Poster headlines, chapter titles, word cards |
| `STENCIL` = Big Shoulders Stencil (bold) | Military and map unit labels, stamps, "CHAPTER 2" |
| `TITLE` = Anton | Big numbers, the corner date tag |
| `LABEL` = Oswald (bold) | Map labels, name tags, notes |
| `UI` = Inter | Small print only |

Labels over maps get a paper-coloured outline (`text(..., outline="paper")`).

## Characters (stick.py, now poster figures)
- **Not stick figures.** These are poster people:
  - simplified, geometric, Art Deco-ish bodies built on the same joint skeleton;
  - limbs are tapered filled shapes with an ink key line;
  - a uniform in the side colour, a hard shadow side (darker tone or halftone);
  - big readable silhouettes.
- **Faces:**
  - strong simple features, profile or 3/4: jaw, nose, brow;
  - eyes as small dark shapes that blink;
  - expressions through brow and mouth shapes;
  - light side `cream`, shadow side halftone.
- **Standard figure** is ~420 px tall at zoom 1 for a hero shot, and the same rig at 0.3-0.6 scale for crowds and soldiers. Crowds are silhouettes in one tone with a few highlights.
- **Headgear and uniforms by nation** (silhouette first):

  | Nation | Headgear |
  |---|---|
  | German | flared helmet |
  | British | flat dish helmet |
  | US | round M1 helmet |
  | Soviet | rounded helmet or side cap |
  | French | crested helmet |
  | Japanese | peaked cap with neck flaps |
  | Italian | helmet with a feather plume |

  Civilians get flat caps, fedoras, headscarves and coats in khaki or olive.
- **Leaders** are poster portraits, with likeness through ONE trademark plus silhouette. Respectful, no grotesque caricature:

  | Leader | Trademark |
  |---|---|
  | Hitler | toothbrush moustache, side-swept hair |
  | Stalin | thick moustache, pipe, swept-back hair |
  | Churchill | bowler hat, cigar, round build |
  | Roosevelt | pince-nez glasses, cigarette holder |
  | Mussolini | bald head, square jaw |
  | Hirohito | round glasses, small moustache |
  | Chamberlain | moustache, umbrella, homburg hat |

- **Motion.** Poster figures move like cut-out animation done well:
  - eased pose blends with anticipation and overshoot;
  - an idle breath and weight shift; nothing ever freezes;
  - walk, run, march, point, shrug, salute, handshake, cheer, crouch, dive, wave a paper, aim and fire (muzzle flash only).

## Vehicles and props (props.py)
- Poster silhouettes: strong side or 3/4 shapes, flat side colour, a key line, a hard shadow or halftone underside.
- Tank, fighter, bomber, dive bomber, battleship, carrier, destroyer, small boats, submarine and periscope, artillery, radar tower, searchlight, sandbags, train.
- Everything animates: tracks roll, propellers blur, ships bob and leave flat wakes, smoke is layered flat puffs, and explosions are flat star bursts with halftone smoke.

## Maps (maps.py): printed war maps
- Data: Natural Earth only (public domain). Historical borders are built from admin-1 provinces.
- Europe uses a Lambert azimuthal equal-area projection at ~15°E 52°N; the Pacific view is centred at ~160°E; the world uses Equal Earth.
- How it looks:
  - land in `land`, the sea in `sea` with fine parallel hatching near coasts;
  - ink coastlines, dashed borders, a light lat/long grid, a compass rose;
  - sides filled in their colours, with halftone on occupied territory;
  - labels in Oswald or stencil.
- How it moves:
  - colour floods outward from a point;
  - front lines are thick wobbly lines that move;
  - arrows are fat poster arrows in the side colour with an ink outline, growing along a curved path;
  - city dots pulse when named;
  - the camera pans and zooms smoothly.

## Every shot
- A slow push-in (`push_in`).
- A visual change every 1-2 seconds.
- The corner date tag (`date_stamp`).
- `print_finish(cr, t)` last.
- Sound cues listed in the scene docstring.
- Clean outputs, with no metadata or encoder tags (`render_clip` strips them).
