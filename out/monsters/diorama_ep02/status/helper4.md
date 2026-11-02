# Helper 4 status (Ep 2)

Updated 2 Nov 2026.

| Shot | State | File |
|---|---|---|
| S05 | **Final, pushed.** 99 frames, 720x1280, crf 10, no tags. Approved look (hands f34, terror face f72). Hands with the dripping claw, one drop falls; cut at f50 up to his face, with 2D terror eyes and a sweat drop on "In my". | shots/S05.mp4 + S05_sheet.jpg |
| S06 | **Final, pushed.** 98 frames. The claw in profile on the light cyc; on "Straight" (f67) a tapered white arrow-jet with an ink outline shoots straight right and stops inside the frame. The floating-finger bug is fixed. | shots/S06.mp4 + S06_sheet.jpg |
| S20bot | **Split three ways (coordinator, 2 Nov).** I render **f001-052**: f001-011 are done, f012-052 are rendering now (about 140 s/frame, done around 15:15 UTC). I have **no frames past f052**, so helper 5 (f053-104) and bGqrs (f105-156) start from scratch. When the parts land I join them (steps below). | shots/S20bot.mp4 (pending) |

Render cost on this container (CPU EEVEE): S05 about 145 s/frame, S06 about 40 s/frame.

## S20bot parts: exact steps for helper 5 (f053-104) and bGqrs (f105-156)
My pipeline takes raw parts as they are. S20bot has **no 2D pass** (post_helper4 adds nothing to it), so the join *is*
the final encode.
- **Any start frame is safe.** S20bot is `step=2, ones=(1,156)`: the camera moves on 1s, so render_shot.py renders
  every frame, and the characters hold on 2s through their STEPPED modifiers, which depend only on the frame number.
  Start at exactly f053 / f105; you don't need the step-multiple lead-in.
- **Render** (from the repo root; split into chunks under 2 h, about 140 s/frame on CPU EEVEE, so at most about 45
  frames per task):
  ```
  /home/user/tools/blender-4.5.15-linux-x64/blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S20bot OUT --frames 53-104
  ```
  (bGqrs: `--frames 105-156`). Frames land as OUT/0053.png ... Leave the env var SHRIMP_IN_HAND unset (it defaults to 0.6).
- **The frame is meant to look odd:** the render border covers only the bottom 62% (rows 486-1280). The top is empty or
  transparent on purpose, because helper 8 crops the bottom panel. Don't "fix" it.
- **Encode the part** (near-lossless, no tags):
  ```
  ffmpeg -framerate 24 -start_number 53 -i OUT/%04d.png -frames:v 52 -c:v libx264 -crf 6 -pix_fmt yuv444p \
     -map_metadata -1 -fflags +bitexact -flags:v +bitexact -bsf:v filter_units=remove_types=6 \
     out/monsters/diorama_ep02/parts/S20bot_f053-104.mp4
  ```
  (bGqrs: `-start_number 105 ... S20bot_f105-156.mp4`, also 52 frames). Push the part and say so in your status file.
- **The join** (mine, once both parts are in):
  ```
  python channels/monsters/diorama/join_parts.py --ep02 S20bot build/monsters/diorama_ep02/render/S20bot:1-52 \
     out/monsters/diorama_ep02/parts/S20bot_f053-104.mp4 out/monsters/diorama_ep02/parts/S20bot_f105-156.mp4
  ```
  This gives shots/S20bot.mp4 + sheet at crf 10 with no tags, checked at 156 frames.
- **Look checks** for the parts: on "Option B" (about f66) Wren turns away and rings her bell. On "hide it" (about
  f84) Kai's hands go to his collar; the shrimp is inside by about f97, then the teal bulge pops on his chest. On
  "Comment" (about f114) Wren glances back; Kai smiles rigidly with his hands behind his back.

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
