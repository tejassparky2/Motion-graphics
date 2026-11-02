# Helper 4 status (Ep 2)

## NEW: S20bot v2, the owner's new ending ("Option B: show her the glowing mark"): OK stills, waiting for your OK
- **Stills:** `okstills/S20bot_v2_f060.png` and `okstills/S20bot_v2_f108.png` (half-scale render, upscaled; the 2D
  pass included; bottom 62% only, as before).
- **Builder:** `helper4.py` `s20bot()` (same name), 160 render frames from the new timing (78c1cad).
- **Beats** (shot frames, 1-based): "Option B" f60, "show" f84, "glowing" f95, "mark" ends f108, "Comment" f117.
  - **f1-59:** Kai tense, the shrimp cupped; Wren stern, her bell low.
  - **f62-70:** the shrimp moves into his right hand.
  - **f68-92:** his left forearm rises slowly toward her, to chest height.
  - **From f84:** the mark is faint. **f95-99:** it flares (helper 9's S14 zigzag via `post_helper9.mark`, drawn
    bolder, with a burst and sparkles, plus a real coral point light on his arm). **From f108:** a soft pulsing glow
    with a few sparkles, to the end.
  - **From f101:** Wren's eyes go wide. These are 2D terror eyes with the blue shock lines (S05's look), because her 3D
    eye keys don't read at this size.
  - **f101-109:** she steps half a step back, leaning away.
  - **f103-109:** the bell comes up in front of her like a ward, with a small tremble; she holds the standoff to the
    end. The shrimp turns to look at the mark.
- **Camera:** behind Kai's right shoulder, so Wren's face turns to us; at the earlier side angles her hood hid it.
  - Kai is at frame left with his back three-quarters to us; Wren is at frame right.
  - A slow push-in on 1s, the characters on 2s.
  - Faces and the bell stay clear of the B card.
- **Weak spot:** the mark sits where S14 puts it (MARK_U 0.3, nearer the elbow), so on his raised forearm it's
  small, close to his body, in front of the shrimp's crest. It reads as a coral flare more than a crisp zigzag.
  If you want it to read bigger I can scale the 2D mark up (the shape stays the same) or move it toward the wrist.
- **Render:** about 150 s/frame at full size here (a guess from v1). Once you OK it, split the 160 frames like last
  time. The steps below still apply with the new range: 160 frames, `--frames A-B`, parts `S20bot_fAAA-BBB.mp4`.
  - **The 2D pass needs `build/.../S20bot_mark.json`.** The builder writes it on every render, so I regenerate it
    here before the join.
  - Then `post_helper4.py S20bot` (no longer join_parts.py: S20bot has a 2D pass now) gives the final.


Updated 2 Nov 2026.

| Shot | State | File |
|---|---|---|
| S05 | **Final, pushed.** 99 frames, 720x1280, crf 10, no tags. Approved look (hands f34, terror face f72). Hands with the dripping claw, one drop falls; cut at f50 up to his face, with 2D terror eyes and a sweat drop on "In my". | shots/S05.mp4 + S05_sheet.jpg |
| S06 | **Final, pushed.** 98 frames. The claw in profile on the light cyc; on "Straight" (f67) a tapered white arrow-jet with an ink outline shoots straight right and stops inside the frame. The floating-finger bug is fixed. | shots/S06.mp4 + S06_sheet.jpg |
| S20bot | **Final, pushed.** All six parts were joined with join_parts.py at **156 frames**, the same plate length as XprL's S20top. 720x1280, crf 10, 0 tags. The approved look: on "Option B" Wren turns away (on 2s, from f56) and rings her bell. On "hide it" Kai's hands go to his collar, the shrimp slips inside (the claw tip peeks out of the collar), and the teal bulge pops on his chest. On "Comment" Wren glances back (about f124) and Kai keeps his hands behind his back with a rigid smile. **Seams between the parts are invisible:** mean frame change across f26/27, 52/53, 78/79, 104/105 and 130/131 is 0.32-0.46, the same as the frames on either side. | shots/S20bot.mp4 + S20bot_sheet.jpg (the sheet shows every 6th frame up to f84) |
| S15 f031-040 (for helper 9) | **Done, pushed.** A raw part from helper 9's builder (`render_shot.py -- diorama_ep02 S15 DIR --frames 31-40`), no 2D pass. libx264 crf 10, yuv420p, CLEAN flags plus a stream-copy remux, start_number 31. 10 frames, 720x1280, 0 tags, about 33 s/frame. The plate is the sky and a treetop; helper 9's pass adds the rift. | parts/S15_f031-040.mp4 |
| S19 f110-124 | **Cancelled** (coordinator, 15:18 UTC: helper 10 pushed the whole f063-124). Stopped; nothing rendered for it was kept or pushed. | none |
| S19 f033-048 v2 (for helper 9) | **Done, pushed.** A raw part from the fixed helper9.py (af9cbaf: c26f273 crane/haze + bbd52b1 clash fix). libx264 crf 10, yuv420p, CLEAN flags plus a stream-copy remux, -start_number 33. 16 frames, 720x1280, 0 tags, about 145 s/frame. The crane rises over the village to the deep-blue lake, and the village reads through the haze. | parts/S19_f033-048_v2.mp4 |

Render cost on this container (CPU EEVEE): S05 about 145 s/frame, S06 about 40 s/frame.

## S20bot parts: steps for helpers 2, 5, 3, bGqrs and 6 (f027-052, f053-078, f079-104, f105-130, f131-156)
My pipeline takes raw parts as they are. S20bot has **no 2D pass** (post_helper4 adds nothing to it), so the join *is*
the final encode.
- **Any start frame is safe.** S20bot is `step=2, ones=(1,156)`: the camera moves on 1s, so render_shot.py renders
  every frame, and the characters hold on 2s through STEPPED modifiers, which depend only on the frame number.
  Start exactly on your first frame.
- **Render** (repo root, about 140 s/frame on CPU EEVEE, so 26 frames is about 1 h, one task):
  ```
  /home/user/tools/blender-4.5.15-linux-x64/blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S20bot OUT --frames 27-52
  ```
  Frames land as OUT/0027.png ... Leave the env var SHRIMP_IN_HAND unset (it defaults to 0.6).
- **The frame is meant to look odd:** the render border covers only the bottom 62% (rows 486-1280). The top is empty on
  purpose, because helper 8 crops the bottom panel. Don't "fix" it.
- **Encode the part** (near-lossless, no tags; 26 frames each):
  ```
  ffmpeg -framerate 24 -start_number 27 -i OUT/%04d.png -frames:v 26 -c:v libx264 -crf 6 -pix_fmt yuv444p \
     -map_metadata -1 -fflags +bitexact -flags:v +bitexact -bsf:v filter_units=remove_types=6 \
     /tmp/part.mp4
  ffmpeg -i /tmp/part.mp4 -c copy -map_metadata -1 -map_chapters -1 -fflags +bitexact -flags:v +bitexact \
     -metadata:s:v handler_name= out/monsters/diorama_ep02/parts/S20bot_f027-052.mp4
  ```
  The second (stream-copy) pass is needed: without it the mp4 header keeps "Lavc libx264" as the compressor name.
  Check with `grep -a -c -E "Lavf|Lavc|x264"` (it must print 0). Change `-start_number` and the name to your range (`S20bot_f053-078.mp4`, `_f079-104`, `_f105-130`, `_f131-156`),
  push, and note it in your status file.
- **The join** (mine, once all five parts are in):
  ```
  python channels/monsters/diorama/join_parts.py --ep02 S20bot out/monsters/diorama_ep02/parts/S20bot_f001-026.mp4 \
     out/monsters/diorama_ep02/parts/S20bot_f027-052.mp4 ... out/monsters/diorama_ep02/parts/S20bot_f131-156.mp4
  ```
  This gives shots/S20bot.mp4 + sheet at crf 10 with no tags, checked at 156 frames.
- **What each part should show:**
  - On "Option B" (about f66) Wren turns away and rings her bell.
  - On "hide it" (about f84) Kai's hands go to his collar; the shrimp is inside by about f97, then the teal bulge pops
    on his chest.
  - On "Comment" (about f114) Wren glances back; Kai smiles rigidly with his hands behind his back.

## Timing change at 13:06 (0a7b842, l2 re-voiced): shots are now up to 1 frame off `render_frames` (for helper 8)
- Every cut from S03 on moved 0.018 s (less than 1 frame) earlier, and some shots' `render_frames` changed by 1.
- **S20 is now 157 render frames (145 + 12).** S20top and S20bot are both 156: they cover all 145 frames plus 11 of
  the 12 spare frames at the end, so nothing visible is missing. I joined S20bot at 156 to match S20top, on the
  coordinator's instruction. (`join_parts.py` itself now demands 157, so I ran it with S20's length set to 156.)
- **Shots that no longer match** the new `render_frames` (checked at 14:15 UTC). Each still covers its full `frames`,
  with at least 11 of the 12 spare frames, so none need re-rendering:

  | Shot | New render_frames | Has |
  |---|---|---|
  | S02 | 44 | 45 |
  | S03 | 63 | 62 |
  | S07 | 49 | 50 |
  | S09 | 94 | 93 |
  | S10 | 63 | 64 |
  | S12 | 75 | 74 |
  | S17 | 74 | 75 |
  | S18 | 87 | 86 |
  | S19 | 123 (was 124) | not in yet |
  | S20top, S20bot | 157 | 156 |

  The assembler should take `frames` from each shot's start and not insist on `render_frames`.

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
| S02 | helper 1 | **The shrimp is not rendered at all** (details and fix below). The shadow grows over empty grass by the pond. Dive, speed lines and the growing shadow are fine. |
| S12 | helper 5 | The brief: "raises its claw at his face: the frame-0 threat again". The claw rises high, but its tip points right, away from Kai and out toward the frame edge, so the "aimed at his face" threat reads weakly. The turn in his palm, the sweat drop and his wary eyes are fine. |
| S18 | XprL | The brief: "a villager's net is held ready behind her". Only the pole shows; the net head is cut off above the top of the frame. Wren's mouth flaps and stern face are fine. Minor. |

| S04 | helper 1 | **The same bug: the shrimp is not rendered.** His cupped hands are empty from f1, while S03 ends with the shrimp in them and S05 opens on it. The rake, the torn sleeve, the three thin marks (**no blood**), the wince and the bird swooping off are fine. |

### S02 / S04: why the shrimp is missing, and the one-line fix (for helper 1)
- **What I checked:** I built S02 and S04 here with the committed code (`channels/monsters/diorama_ep02/helper1.py`)
  and inspected the scene.
  - In S02 the shrimp is at `bgqrs.SHRIMP` (4.2, -0.1, 0). It projects to about (258, 736) px at f10, and a ray from
    the camera reaches it unblocked.
  - But **every `puff_*` object has `hide_render=True`**: 46 of 46 in S04, and the same in S02. The rendered S02
    frames show empty grass at that spot; see S02 f10/f40.
- **Cause:** `_clear_smoke` (helper1.py:305) picks the smoke spheres by
  `o.name.startswith("puff") and o.type == "EMPTY"`. **The shrimp's rig empties are named `puff_root`, `puff_body`,
  ...**, so the shrimp counts as a "smoke puff". It sits nearer than the target, so the function hides it along with
  all its children.
  - S02 (line 159) and S04 (line 504) call it.
  - S16 (line 373) calls it too but has no shrimp, so it's unaffected.
- **Fix** (helper1.py:305):
  ```
  puffs = [o for o in sc.objects if o.name.startswith("puff") and not o.name.startswith("puff_") and o.type == "EMPTY"]
  ```
  The smoke spheres are `puff`, `puff.001`, ... Then re-render S02 and S04.
  - The S02 camera already frames the shrimp at (258, ~736) px, above the caption band's bottom edge (930) but inside
    the band (845-930) only if it drifts. Check it stays clear.
  - In S04, check that the shrimp shows in his cupped hands.
- Other helpers' builders don't use `_clear_smoke`, as far as I can see (grep finds it only in helper1.py).

**OK against the brief:** S03, S06, S07, S08, S09, S10, S11, S13, S16, S17.
- **S03:** slide in on his knees, a splash, the scoop.
- **S07:** he turns the shrimp outward, a bomb-tech face; the shrimp is confused.
- **S08:** the two-hand pistol aim with the bird wheeling in the background. It's closer to eye-level than "heroic low", which is minor.
- **S09:** the eye close-up, then the held wind-up (f14-33, about 0.8 s), then SNAP. Its impact frames are f34 (a black/white negative) and f35 (a red silhouette) rather than *white* frames, followed by the shockwave ring and the bird blasted back. That's a stylistic choice that reads strongly; I'm not flagging it.
- **S10:** stuck upside down in the thorn bush, dazed, with stars; the bird is not hurt.
- **S11:** shakes free into a puffball, glares, stomps off.
- **S13:** the tiny tap with a sparkle, dot eyes, a held beat.
- **S16:** villagers with nets and bells on the hill, with 2D ring lines.
- **S17:** Wren marches up with the bell and stops in front of Kai.

**Hard rules:** no blood or graphic violence anywhere; the bird is never killed (dazed, then fluffed and offended).
**S20top (XprL, d584790): OK.** 156 frames, no tags, 0 edge-scan hits. Kai lowers the shrimp into Wren's net (in the net from about f50), and the action stays in the upper half for helper 8's split.
**S20bot (mine, joined from six parts): OK.** 156 frames, no tags. The edge scan flags only the intentionally empty top band (rows 0-485, the render border); everything below the crop line is clean.
**Check-in 15:15 UTC:**
- **S02, re-rendered (1cee315): fixed.** The shrimp sits at the pond's edge in every frame. 44 frames (= the new
  render_frames), 0 tags, 0 edge hits. The shadow grows just to its right rather than right over it; that's minor and
  acceptable.
- **S04: not re-rendered yet** (still 3d28621). His cupped hands are still empty. Helper 1's new `_clear_smoke` filter
  (`... and o.parent is None`, helper1.py:307) should leave S04's shrimp alone, as long as its root is parented to Kai.
  Check it when you re-render.
- **picture.mp4** (helper 8, 04bd32c, a work in progress):
  - 1376 frames, 1080x1920, 57.33 s, 0 tags, **0 edge-scan hits**.
  - The hook text is on frame 0. The captions sit in the band, and the A/B badges and the jagged divider in the S20
    split are clear of every face (the B badge is over the tree in the bottom panel).
  - **It still carries the old S02 and S04** (no shrimp; frame 80 is S02, frame 175 is S04).
  - **S14, S15 and S19 are placeholder cards.**
  - S20 top, minor: Kai's cap touches the top edge of the frame in its last second.
- **Not in yet** (no QA): S14, S15, S19 (finals), S04 (the re-render) and the final picture. I'll scan them when they land.
