# Monster series: production notes

## Look
Pokémon-style toon 3D (owner, 30 Oct 2026: "Try to achieve Pokémon level of animation style and quality"). Original
creatures only (no Pokémon or Kirby look-alikes). Style test: `channels/monsters/style_test.py`. Blender 4.5 EEVEE Next,
Shader to RGB banding + rim + inverted-hull outlines + blob contact shadow. Measured here on 30 Oct: ~26-32 s per
720x1280 frame at 16 samples, on 4 CPU cores via Mesa llvmpipe/EGL.

## What the pelican-film session learned (session_01PF511aj8dYVAAn5os6fLwN, branch ccr-33aaae6e-sdrhrs, 30 Oct)
- **Setup:** Blender 4.5.15 LTS headless, Cycles CPU, 10 samples, adaptive 0.04 (min 4), OIDN (RGB+albedo+normal),
  light tree, persistent data, bounces 6 / diffuse 2 / glossy 2. AgX "Medium High Contrast".
  - Vignette and grain go in ffmpeg (a compositor blur cost ~12 s per frame).
- **Timings at 1920x1080 on 4 cores:** ~72 s per frame for wides, 105-115 s for close-ups, 65 s for the sunset.
  - 481 frames took ~11-12 h of compute.
  - EEVEE (realistic materials) took ~4 min per frame there. Our toon/emission materials are much cheaper (~30 s).
- **Building:** everything procedural (bpy + numpy + scikit-image marching cubes).
  - Creatures: SDF bodies made of smooth-unioned ellipsoids, polygonised and Taubin-smoothed.
    - Marching-cubes faces come out inside-out: flip the normals.
    - A new creature costs about 4-8 h the first time (model + rig + look-dev), then it's reusable.
  - Rig: armature with procedural skin weights from capsule distances; IK targets on empties.
  - Gotcha: Blender 4.4+ with hand-made F-curves needs `anim_data.action_slot = action.slots[0]`, or nothing animates
    (all-black renders).
- **Lighting and camera:**
  - No volumetrics (too slow on CPU); fake haze with distance fog in the materials, plus bloom.
  - One sun, re-keyed at each cut with CONSTANT keys.
  - One camera per shot, switched by timeline markers; DOF focus parented to the character.
- **Speed-ups:**
  - `emission_sampling = 'NONE'` on glow-only materials.
  - World MIS map: manual sampling resolution 256 (it rebuilt every frame otherwise, 4.4 s).
  - No point lights (+15 % cost).
  - AgX washes saturated emission toward white, so keep glow low.
- **Running renders:**
  - The container sleeps when idle, so run renders as tracked background Bash tasks in chunks under 2 h, with
    `--skip_existing --budget`, and relaunch each chunk as it completes. Keep a send_later check-in as a safety net.
  - `pkill -f` can kill your own shell.
- **Parallel renders:** split by frame range (N sessions ≈ 1/N wall time). Each session needs the same Blender and a
  deterministic, seeded build script. Write PNGs into separate folders, then concatenate and encode once.
- **Humans:** the explainer pipeline uses MPFB2 (MakeHuman for Blender) with 52 ARKit face shape keys. Full hand-off:
  `explainer/SESSION_PROMPT.md` on that branch.

## Our measurements (container, 30 Oct 2026)
| Engine and scene | Time |
|---|---|
| Godot 4.5.1 Compatibility on llvmpipe, 720x1280: 2D top-down scene | ~7.5 fps |
| Godot 4.5.1 Compatibility on llvmpipe, 720x1280: 3D low-poly diorama | ~3 fps |
| Blender 4.5.15 Cycles, 720x1280, 32 samples, simple Quaternius monster scene | 30 s per frame |
| Blender 4.5.15 EEVEE Next toon style test, 720x1280, 16 samples | 26-32 s per frame |

## Parallel sessions
Reuse the existing helper sessions listed in channels/horror/README.md (owner: don't create new ones).

## Pelican session follow-up (30 Oct): explainer toolkit and speed-ups (branch ccr-33aaae6e-sdrhrs, explainer/)
- **Humans:** MPFB2 (add-on GPL; generated characters + MakeHuman system assets CC0).
  - Asset packs: makehuman_system_assets_cc0.zip, skins01_cc0.zip, faceunits01.zip (52 ARKit face units).
  - Data folder: ~/.config/blender/4.5/extensions/.user/user_default/mpfb/data.
  - `--factory-startup` disables the extension.
  - Names: finger1 = thumb, metacarpal1 = index.
  - Arm IK: lowerarm02, chain 4, use_tail=True. Fingers flex with +X local rotation.
  - Replace the MakeHuman logo T-shirt with a plain dye.
- **Stylised rigs:** Blender Studio "Rain" and "Snow" rigs, CC-BY (credit line required).
- **Mocap, lip sync, voice, font:**
  - Mixamo needs the owner's Adobe ID.
  - CMU mocap was unreachable from that container.
  - Lip sync: Rhubarb Lip Sync.
  - Voice: Kokoro af_heart at speed 1.1 (word timings for captions).
  - Font: Montserrat Black (OFL).
- **Cycles speed-ups:**
  - `emission_sampling='NONE'` on glow-only materials.
  - No subsurface except skin.
  - 8 samples, adaptive 0.05, OIDN.
  - Never Add-Shader a Transparent BSDF (it doubles the transparency).
  - These took 110 s down to ~62 s per frame at 1080x1920.
- **Look at every image.** Things they only caught by looking: IK not reaching its target, gaze drifting under the eyelids, a backdrop leaking into other shots.
- **Previews:** a Workbench contact sheet every 2nd frame.

## Episode 1 work split (30 Oct 2026, owner: "Use all this dma sessions to speed up")
| Who | Piece | Module |
|---|---|---|
| DMA helper 1 (session_01PF511bDdsYwHy141n4jcnn) | Earth lab set (tanks, rain window, power strip, lightning/flicker/puddle/spark) | mk/lab.py |
| DMA helper 2 (session_01PF511Y13zuEX6TW3egNyxM) | Pistol shrimp in its tank (snap, bubble glow, glass crack) | mk/pistolshrimp.py |
| DMA helper 3 (session_01PF511b6tpL8dByjU7Qp3Tu) | The new world landscape + fall-through-clouds camera | mk/world.py |
| DMA helper 4 (session_01PF511YEojWTNPFKxSeURms) | Jelly-snail (tell: smoking holes in its trail) | mk/jellysnail.py |
| DMA helper 5 (session_01PF511ahSS4W8tEQ9ukoLwF) | Tuftwing bird (tell: a giant shadow) | mk/tuftwing.py |
| DMA helper 6 (session_01PF511Y382fBtBJa7rzyVDQ) | Fluffmoth (tell: the wing eye-spots blink) | mk/fluffmoth.py |
| ~~DMA helper 7 (session_01PF511bWPhLFvpRbgd3zffg)~~ | (Kai moved to XprL on 30 Oct: helper 7 was stuck on a permission prompt) | - |
| DMA helper 8 (session_01PF511Yk7bwbspWweS95hGA) | 2D anime FX + original game HUD (pycairo): DONE (ede50cf) | fx2d.py |
| DMA helper 9 (session_01PF511ZFaQeq2RigHZ22DrB) | Storm, power-out, white-out, sky reveal | mk/storm.py |
| DMA helper 10 (session_01PF511YTmbSi3KeLNnX6GyZ) | Forest-erase effect | mk/erase.py |
| session_01PF511bGqrs1SFn3cpk5NqS | Sound effects + music beds (numpy): DONE (562896c); beam + bokeh: DONE (ead9ac1); now the 2D compositor | sfx.py, fx2d_extra.py, comp.py |
| session_01PF511XprLcpVNCdEQUsUFF | Kai's voice (am_liam) + Episode 1 takes: DONE (56cb0bd); now Kai himself (design in HELPERS.md v3.2) | monsters_ep01_takes.tar, mk/kai.py |
| Coordinator (this session) | Puff-shrimp, crater shots, shot list and timeline, integration, final parallel render | mk/puffshrimp.py, ep01 |

## Standing rule (owner, 30 Oct 2026): "Update all helpers the same whenever we Update anything here"
Every change to the look, the kit or the rules goes into HELPERS.md under "Latest updates", and a note goes by
send_message to EVERY helper session in the work-split table (active or waiting).

## Owner direction, 30 Oct 2026 (evening): stop, study three episodes, rewrite the story, no HUD
Word for word:
- (with two more episode links, S22E22 and S20E43) "One more for you to study deep dive" / "One more deep dive"
- "I said anime then why Health bar i want you to write good engaging interesting story do deep research take
  inspiration from Pokémon episodes First study all 3 episodes i gave you do deep dive animation story take full
  inspiration then make animation after that research launch parallel angents to make deep dive on all episodes story
  everything no hallucinations"
- "I said stop and First study all 3 episodes ..." (repeated)
- "Also stop helpers too"
- "I want you to make best out of it possible use any tools skills opensouce free character animation community tools
  anything needed output best animation and best story"
- "No if it's slow take help from helpers sessions"
- "And our story should still have option a and b so we go as viewer's comment but all should be engaging brilliant
  clever entertainment interesting suspens thirrling"

What changes:
- The series is a pure anime. NO game HUD: no health bar, status bar, WILD tag, threat pips, menus, BOND pop-up or
  fact cards.
- Every episode still ends on an A/B choice decided by viewers' comments. Both options must be clever, thrilling and
  fair; a losing branch is never a dead end.
- Order:
  1. Study all three episodes (animation AND story), with parallel deep-dive agents and no unsupported claims.
  2. Research tools, assets and story craft.
  3. Rewrite the story; the owner approves the script.
  4. Then animate.
- The helpers are stopped; six of them only transcribe episode halves (Whisper medium). Episode files stay in
  scratchpads; nothing from them goes into git.
- Research notes: `research_notes/Pokémon episodes story and animation/`. Report: `reports/Pokémon episodes story and
  animation.md`.
