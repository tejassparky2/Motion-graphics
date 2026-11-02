# Helper 4 status (Ep 2)

Updated 2 Nov 2026.

| Shot | State | File |
|---|---|---|
| S05 | **Final, pushed.** 99 frames, 720x1280, crf 10, no tags. Approved look (hands f34, terror face f72). Hands with the dripping claw, one drop falls; cut at f50 up to his face, with 2D terror eyes and a sweat drop on "In my". | shots/S05.mp4 + S05_sheet.jpg |
| S06 | **Final, pushed.** 98 frames. The claw in profile on the light cyc; on "Straight" (f67) a tapered white arrow-jet with an ink outline shoots straight right and stops inside the frame. The floating-finger bug is fixed. | shots/S06.mp4 + S06_sheet.jpg |
| S20bot | **Rendering** (11/156 frames at 13:45 UTC). 156 frames at about 140 s/frame, about 6 h. Approved look (hide f92, glance f124). It renders the bottom 62% of the frame (rows 486-1280); the top is empty on purpose for helper 8's split. | shots/S20bot.mp4 (pending) |

Render cost on this container (CPU EEVEE): S05 about 145 s/frame, S06 about 40 s/frame.

## QA (S01-S04, S06-S13, S16-S18), 2 Nov 2026

**Technical (all 16 shots in, S05 included): all pass.**
- 720x1280; every frame count equals timing.json `render_frames`.
- No Lavf/Lavc/x264/encoder strings.
- Edge-band scan (every 2nd frame, a pure-black band of 2+ rows/columns at any edge in a non-dark frame): **0 hits in every shot.**
- Frame 0 of S01 is already moving (mean frame-to-frame change 4.7).

**Against the brief.** These four don't fully match the brief (the owners should look):

| Shot | Who | Finding |
|---|---|---|
| S01 | bGqrs | The brief asks for "the bird already diving at the shrimp by the pond, its shadow on the grass", on a medium-close, low shot. In the render the bird hovers at the thorn tree and drifts down toward Kai's outstretched hand; it never dives at the shrimp, and there's no bird shadow on the grass. The camera is eye-level and medium-wide. Kai sprinting in from the left, the hand out, and the shrimp by the pond above the caption band are all fine. |
| S02 | helper 1 | The shadow grows "over the tiny shrimp at the puddle", but **the shrimp isn't visible in any frame**. The shadow spreads over empty grass and clover next to the pond. Dive, speed lines and the growing shadow are fine. |
| S12 | helper 5 | The brief: "raises its claw at his face: the frame-0 threat again". The claw rises high, but its tip points right, away from Kai and out toward the frame edge, so the "aimed at his face" threat reads weakly. The turn in his palm, the sweat drop and his wary eyes are fine. |
| S18 | XprL | The brief: "a villager's net is held ready behind her". Only the pole shows; the net head is cut off above the top of the frame. Wren's mouth flaps and stern face are fine. Minor. |

**OK against the brief:** S03, S04, S06, S07, S08, S09, S10, S11, S13, S16, S17.
- **S03:** slide in on his knees, a splash, the scoop.
- **S04:** the rake, a torn sleeve and three thin marks, **no blood**; he curls round the shrimp and the bird swoops away.
- **S07:** he turns the shrimp outward, a bomb-tech face; the shrimp is confused.
- **S08:** the two-hand pistol aim with the bird wheeling in the background. It's closer to eye-level than "heroic low", which is minor.
- **S09:** the eye close-up, then the held wind-up (f14-33, about 0.8 s), then SNAP. Its impact frames are f34 (a black/white negative) and f35 (a red silhouette) rather than *white* frames, followed by the shockwave ring and the bird blasted back. That's a stylistic choice that reads strongly; I'm not flagging it.
- **S10:** stuck upside down in the thorn bush, dazed, with stars; the bird is not hurt.
- **S11:** shakes free into a puffball, glares, stomps off.
- **S13:** the tiny tap with a sparkle, dot eyes, a held beat.
- **S16:** villagers with nets and bells on the hill, with 2D ring lines.
- **S17:** Wren marches up with the bell and stops in front of Kai.

**Hard rules:** no blood or graphic violence anywhere; the bird is never killed (dazed, then fluffed and offended).
**Not in yet** (no QA): S14, S15, S19, S20 (top and the assembled split). I'll scan them when they land.
