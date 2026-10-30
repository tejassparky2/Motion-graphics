# Open-source / free (non-AI) pipelines for a game-style monster-taming series on a CPU container + RTX 3050 laptop

Scope and re-weighting. The owner's target changed during this research: **not anime, but "animation like a game"** (top-down RPG / monster-tamer look, a stylized top-down "living diorama", game HUD and turn-based battle UI); 2D, 2.5D or 3D are all fine; **8-10 h of machine time per 60-90 s episode is acceptable and quality comes first**. Sections 1-7 cover the game-style pipelines; section 8 keeps the anime-specific rig tools (now lower priority); section 9 gives render budgets and the ranked recommendation. This builds on, and does not repeat, `reports/CPU anime animation pipeline.md` and `reports/3D horror Shorts animation and hooks.md`.

Reference Short to beat (owner): 92 s, 720x1280, 30 fps (2,760 frames); top-down low-poly autumn forest, tilt-shift-like depth of field, drifting fog/clouds, river, tiny character chopping trees, log cabin built in stages, day-to-night cycle (sunset, campfire, fireflies, glowing red eyes), a dragon flyover with its shadow; game HUD (Day 1, clock 6:19 AM → 6:28 AM next day, villager/house/wood counters, rule chips, "100 days" countdown) and big centred captions.

Labels: **[official]** vendor docs; **[measured here]** timed on our container (source given); **[measured]** timed elsewhere; **[report]** forum/press; **[estimate]** my arithmetic/judgement. Research date 30 Oct 2026.

## 1. Which toolchain best produces the reference "living diorama" (day/night, staged construction, creature flyover) on our machines?

### Takeaway
A real-time 3D engine scene with a long-lens top-down camera is the natural fit, and two engines can do it here: **Godot 4** (measured on our container at ~3 fps for a 600-tree low-poly 3D scene in the Compatibility renderer, ~7.5 fps in 2D) and **Blender** (EEVEE on the laptop for the best lighting; EEVEE on the container via llvmpipe at ~8 s/frame). Godot's container renderer lacks depth of field and volumetric fog, so the tilt-shift look there must be faked in post or rendered on the laptop (Godot Forward+ or Blender EEVEE). three.js works but is ~1 fps under SwiftShader and has no authoring tools; a Canvas2D/Phaser path is the fastest (tens of ms per frame) but only for a 2D version of the look.

### Cited Findings
- **Godot 4.5.1, Compatibility renderer, Mesa llvmpipe via Xvfb, Movie Maker, 720x1280 @ 30 fps on our 4-core container:** 2D top-down test (~400 trees drawn once, CanvasModulate day/night, CPUParticles2D, camera zoom) rendered 300 frames in 40 s (~7.5 fps); 3D low-poly top-down test (~600 MultiMesh trees, shadowed DirectionalLight, OmniLight, fog) rendered 240 frames in 79 s (~3 fps) — coordinator's local test, Oct 2026 [measured here]
- Godot 4.7 renderer matrix: Compatibility (OpenGL) has **no depth-of-field blur, no volumetric fog, no SDFGI, no VoxelGI, no decals**, no SSR/SSIL/TAA/FSR2/compute, no particle trails or particle SDF collision; it does have glow, SSAO, depth and height fog; 8 Omni + 8 Spot lights per mesh (raisable); 2D rendering features are supported in all renderers. Forward+ and Mobile require Vulkan, Direct3D 12 or Metal; DOF is in Mobile and Forward+, volumetric fog only in Forward+ — [Godot docs: Overview of renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) [official]
- Our container has `libvulkan1` but no Vulkan ICD (`/usr/share/vulkan/icd.d` empty, so no lavapipe), plus Xvfb and `libegl-mesa0` 25.2.8 — local `dpkg -l` check, 30 Oct 2026 [measured here]. So Godot Forward+/Mobile cannot run on the container as installed.
- Movie Maker: `--write-movie`, `--fixed-fps`, `--resolution`, `--quit-after`; AVI (MJPEG), PNG+WAV (transparency supported), OGV (editor builds only); "The output video will always have perfect frame pacing"; for 3D, "Scaling 3D" above 1.0 gives supersampling without raising output resolution — [Godot docs: Creating movies](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) [official, Godot 4.7]
- Blender EEVEE on this container via llvmpipe/EGL: ~8 s/frame at 720x1280 with 4 samples, ~15 s at 1080x1920, 37-55 s at 16 samples; Workbench ~2 s/frame — `reports/CPU anime animation pipeline.md` [measured here earlier, contended]. EEVEE officially "only uses the power of the GPU" — [Blender manual](https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html) [official]
- three.js r169 in chrome-headless-shell with SwiftShader, with bloom/PCF shadows/ACES: ~1 fps (80 s episode ≈ 40 min); Mesa llvmpipe was ~4x faster than SwiftShader in isolation on another team's 8-core nodes — `reports/3D horror Shorts animation and hooks.md`; [Microlink](https://microlink.io/blog/webgl-without-a-gpu) [measured here / measured elsewhere]
- RTX 3050 4 GB Laptop GPU: Blender 3.3 Classroom (Cycles, OptiX) ~97-152 s, average ~123.5 s, median ~116 s per frame — [Notebookcheck RTX 3050 Laptop page](https://notebookcheck-ru.com/nvidia-geforce-rtx-3050-laptop-gpu.554490.0.html) [measured, aggregated; page unclear whether all entries are this exact chip]. Desktop RTX 3050 Blender benchmark median ~1,470 (Renderjuice estimate from Open Data, Mar 2026) — [Renderjuice](https://www.renderjuice.com/gpus/compare/rtx-3050-vs-rtx-5050) [report]
- 4 GB cards and EEVEE: crash reports with heavy textures while Cycles worked; a ~1.2 GiB single render-buffer allocation failing at a very large output size; ~900 MiB VRAM used by Blender at factory startup — [GameDev.tv forum](https://community.gamedev.tv/t/blender-is-out-of-memory-i-think-any-solution/256347); [T64900](https://developer.blender.org/T64900); [#92139](https://projects.blender.org/blender/blender/issues/92139) [report]

### Inferences
- **How each element of the reference maps to engine features [estimate; standard features of both engines]:**
  - *Top-down tilt-shift:* long focal length camera tilted ~60-80°, shallow DOF focused on the action. Blender: camera DOF (f-stop + focus object) in EEVEE/Cycles. Godot: CameraAttributesPractical DOF blur near/far — **Forward+/Mobile only**, so on the container it must be faked (render a depth pass, blur by depth in NumPy/OpenCV post) or done on the laptop.
  - *Drifting fog/clouds:* Godot height fog (all renderers) plus scrolling cloud-shadow texture (light cookie or decal-like plane) and billboard cloud sprites; volumetric fog only in Forward+. Blender: volume scatter (expensive on 4 GB) or alpha cloud cards.
  - *River:* scrolling-UV water shader with foam edges; trivial in both.
  - *Day/night:* animate sun rotation/colour/energy and sky/ambient colour on a timeline; campfire = flickering OmniLight + emissive mesh + glow; fireflies = GPU/CPU particles with emissive material + glow; red eyes = emissive billboards that fade in when ambient light drops.
  - *Staged construction:* modular cabin pieces (logs, walls, roof) shown in sequence with a scale-pop and dust particles (Godot AnimationPlayer or a script reading a timeline; Blender visibility/scale keys).
  - *Dragon flyover with shadow:* animated creature mesh on a path; the shadow comes free from the directional (moon) light — in Godot Compatibility that costs one shadowed directional light (already in the measured 3 fps test).
  - *HUD and captions:* render in the engine (Godot Control nodes) or composite afterwards in pycairo/Canvas2D for crisp type and easy edits (recommended, since captions change per script).
- **Container-only build of this scene in Godot Compatibility: 2,760 frames at ~3 fps ≈ 15 min** [estimate from measured rate]; even 4x supersampling (Scaling 3D = 2.0) at an assumed ~4x cost stays ≈ 1 h, well inside 10 h. The missing DOF/volumetrics are the price.
- **Laptop build in Blender EEVEE or Godot Forward+** gives real DOF, volumetric fog, better shadows and GI; both should render a 92 s diorama far inside 10 h on the RTX 3050, but no measured EEVEE/Godot numbers for that GPU exist (see section 9).
- **three.js** is a fallback only: it has every needed effect (BokehPass/DOF, fog, particles) but SwiftShader speed (~1 s/frame) plus no scene editor makes it worse than Godot on both quality-per-hour and authoring.

### Gaps
- No measured EEVEE or Godot Forward+ frame times on the RTX 3050 4 GB laptop.
- Godot Forward+ on Mesa lavapipe (software Vulkan) was not tested; it would need `mesa-vulkan-drivers` installed and its speed is unknown.
- Whether Blender 5.x EEVEE still runs on llvmpipe (Blender 5.0 added Vulkan 1.3 to its requirements per [Renderahouse](https://www.renderahouse.com/blog/blender-system-requirements)) is unverified; the earlier measurement may have been on Blender 4.x.

## 2. Godot 4 as a game-style animation pipeline: 2D (tiles, sprites, Skeleton2D creatures, lights, particles) and 3D low-poly, rendered offline

### Takeaway
Godot covers the whole game look in one MIT-licensed, text-scriptable engine: TileMap worlds, frame-by-frame sprites, cut-out Skeleton2D creatures, 2D lights with CanvasModulate day/night, particles, and 3D low-poly scenes, all rendered frame-exact by Movie Maker. Its known weak spot is 2D skeletal rigging ergonomics; a real monster tamer with 120 animated monsters (Cassette Beasts) was built in Godot by a two-person team.

### Cited Findings
- Godot 4.7 2D skeletons: Polygon2D parts on one texture, Skeleton2D + Bone2D chain, weight painting, "animate the bones, not the polygons"; default triangulation "can bend unexpectedly" (add internal vertices); page "not yet updated for Godot 4.7"; no 2D IK documented — [Godot docs: 2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html) [official]
- Users: Skeleton2D "a lot of extra work but you can get the job done" (Jun 2024); "pretty cumbersome" (May 2025); "very frustrating in practice" (Dec 2025); a free human Skeleton2D rig shared Jun 2026 via Scalable Vector Shapes 2D — [Godot forum](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]
- 2D rendering features are supported in all three renderers (so CanvasModulate/PointLight2D/2D particles work in Compatibility on the container) — [Godot renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) [official]; confirmed in practice by the coordinator's container test (CanvasModulate + CPUParticles2D at ~7.5 fps, 720x1280) [measured here]
- Godot 4.6 restored 3D IK (`IKModifier3D`); 2D IK still needs a `SkeletonModifier2D` with your own solver — [TabNews](https://www.tabnews.com.br/zivaengine/godot-4-6-trouxe-o-ik-de-volta-pra-quem-faz-jogo-3d-isso-importa-mais-que-o-jolt) [report]
- Procedural 3D spider in Godot 4.5: Marker3D foot targets chased by IK; step arc when a foot passes a distance threshold; diagonal leg pairs; body height = foot average — [80.lv](https://80.lv/articles/ik-driven-procedural-spider-locomotion-in-godot-4-5) [report]; a 2D raycasting spider (Univ. of Tartu, 2025) — [course page](https://courses.cs.ut.ee/2025/cg/fall/Main/Project-ProceduralAnimation) [report]
- Cassette Beasts (2023): Godot, two full-time developers, 120 monsters and >14,000 animated fusions, native Linux — [Wikipedia](https://en.wikipedia.org/wiki/Cassette_Beasts); [Wireframe](https://wireframe.raspberrypi.com/articles/creature-collecting-gets-an-analogue-upgrade-in-cassette-beasts) [press]
- Godot `--headless` "disables all rendering code" — [godot-proposals #5790](https://github.com/godotengine/godot-proposals/issues/5790) [official]; hence the Xvfb + llvmpipe route used in the coordinator's test.
- MIT turn-based battle cores exist in the asset library: "Turn by Turn Battle Engine" (Godot 4.1, v0.3) and LeviOS31's "Turn-based combat Addon" (Godot 4.6) — [asset 23342](https://godotengine.org/asset-library/asset/edit/23342); [asset 23058](https://www.godotengine.org/asset-library/asset/edit/23058) [report; repos not inspected]

### Inferences
- **Claude can author everything as text** [estimate; `.tscn`/`.tres`/GDScript are plain text]: scene trees, tilemaps, animation tracks generated from the script/timing JSON (the same way `make_horror.py` writes timing today), then one Movie Maker command per shot. This is the strongest "code-first" game pipeline found.
- **2D style choices in Godot:** (a) frame-by-frame sprites (AnimatedSprite2D) drawn in a pixel or HD style — most "game-like"; (b) Skeleton2D cut-out creatures — smoother, fewer drawings, but rig set-up is manual-ish; (c) 2D lights with normal-mapped sprites for dramatic night scenes. A mix (frame-by-frame characters, Skeleton2D for big monsters, particles for VFX) is how 2D games are usually built.
- **3D in Godot on the container** is limited by Compatibility (no DOF/volumetrics) but fast (3 fps at 600 trees); the same project opened on the laptop in Forward+ gains DOF, volumetric fog, SDFGI and better shadows with no asset changes — a clean "preview on container, final on laptop" split.
- For creatures, Godot's procedural tools (IK, springs, particles, shaders) let one monster rig produce many behaviours (idle breathing, hop, wing flap, tail sway) by code rather than hand-keyed clips.

### Gaps
- Skeleton2D + Polygon2D render cost under llvmpipe was not measured separately (the 2D test used trees and particles).
- The two MIT battle addons were not inspected for completeness (catching, party, stats).
- Cassette Beasts' animation method (frame sprites vs skeletal) was not documented in the sources found.

## 3. Browser engines (Phaser, PixiJS) rendering frame by frame in headless Chromium on CPU

### Takeaway
On our container the decisive factor is not the engine but the raster path: a CPU-rasterized Canvas2D game frame (720x1280, ~400 tiles, 300 trees, 150 animated sprites, 20 lights, day/night tint, HUD) costs **~15 ms to draw and ~25-50 ms including transfer to Node** [measured here], about 10x faster than the same canvas GPU-accelerated through SwiftShader (~160 ms). Phaser 4 (MIT, April 2026) still has a Canvas renderer but most of its new effects are WebGL-only, and WebGL here means SwiftShader/llvmpipe speeds. So browser engines are excellent for HUD/battle-UI layers and flat 2D scenes, not for lit 3D-looking worlds.

### Cited Findings
- **Local benchmark (30 Oct 2026, chrome-headless-shell build 1243 via playwright-core, 4-core container, load average 1.3-4 from other processes, one run each)**, scene drawn by Canvas2D `drawImage` with nearest-neighbour scaling, multiply day/night overlay, 20 additive radial-gradient lights, HUD text, two HP bars, outlined caption [measured here; script in the session scratchpad]:

  | Chrome flags | Size | draw + raster (getImageData) | + JPEG q92 to Node | + raw RGBA (base64) to Node | page.screenshot PNG | page.screenshot JPEG |
  |---|---|---|---|---|---|---|
  | `--disable-gpu --disable-accelerated-2d-canvas` (CPU Skia) | 720x1280 | **14.9 ms** | 25.0 ms | 47.8 ms | 142.7 ms | 53.2 ms |
  | same | 1080x1920 | **22.9 ms** | 47.2 ms | 102.5 ms | 196.5 ms | 84.8 ms |
  | `--use-angle=swiftshader` (accelerated canvas on SwiftShader) | 720x1280 | 161.5 ms | 173.9 ms | 189.0 ms | 284.2 ms | 171.5 ms |
  | same | 1080x1920 | 292.3 ms | 292.3 ms | 346.8 ms | 421.8 ms | 329.2 ms |

  In-page `canvas.toDataURL('image/png')` alone cost 274 ms (720x1280) and 521 ms (1080x1920) on the SwiftShader run — PNG encoding in the page is the bottleneck, so frames should leave as raw RGBA (or lossless encode in Node/ffmpeg).
- Phaser 4 first released 10 Apr 2026 (v4.2.1 on jsDelivr), MIT; Phaser uses Canvas and WebGL renderers; Phaser 4 is "built on a brand-new WebGL renderer" and per the official rendering tutorial most new features are "only available in WebGL" — [Wikipedia](https://en.wikipedia.org/wiki/Phaser_(game_framework)); [Phaser 4 rendering concepts](https://phaser.io/tutorials/phaser-4-rendering-concepts); [jsDelivr README](https://cdn.jsdelivr.net/npm/phaser@4.2.1/README.md) [official/report]
- PixiJS v8 auto-detects WebGPU/WebGL; the Canvas fallback was moved to `pixi.js-legacy` in v5, and its status in v8 is unclear — [PixiJS v8 beta post](https://pixijs.com/blog/pixi-v8-beta); [pixi.js #5694](https://www.github.com/pixijs/pixi.js/issues/5694) [official/report]
- Frame-exact capture pattern: drive the page with Puppeteer and call a `seekToFrame(n)` per frame so heavy scenes never drop frames — [html5-animation-video-renderer](https://github.com/andreybo/html5-animation-video-renderer); HyperFrames' deterministic mode drives `performance.now()` from passed frame ticks; in-page `<video>` decoding is unreliable during BeginFrame capture — [HeyGen research](https://www.heygen.com/research/html-to-video) [report]

### Inferences
- For Phaser/Pixi in this pipeline: disable the engine's own loop, step a fixed `dt` per frame from Node, force the Canvas renderer for 2D scenes on the container, and pipe raw RGBA to ffmpeg. Expect ~2-3 min of render for a 90 s episode at 720x1280 and ~3-5 min at 1080x1920 for scenes like the benchmark [estimate from measured per-frame cost].
- The same trick (CPU Canvas2D, raw readback) is a cheap way to render the HUD, battle UI, captions and 2D VFX layers on top of Godot/Blender plates, at ~25-50 ms per frame.
- WebGL-heavy Phaser 4 effects (lighting, filters) fall back to SwiftShader/llvmpipe costs comparable to three.js (~1 s/frame for heavy scenes), so they offer no advantage over Godot.

### Gaps
- Phaser 4's Canvas renderer was not itself benchmarked (only raw Canvas2D, which is what it uses); scene-graph overhead is unmeasured.
- llvmpipe-backed WebGL (`--use-angle=gl` + Xvfb) for Phaser/Pixi was not measured here.

## 4. Sprite tools and free asset packs (tiles, creatures, props, VFX): licences and caveats

### Takeaway
For 3D, Kenney, Quaternius and KayKit together cover the reference diorama (autumn forest, river props, survival/camp items, modular village/cabin pieces) and a monster roster (Quaternius Ultimate Monsters, 50 animated) under CC0 or CC0-like terms; for 2D, CC0 tiles exist but CC0 creature sprites in a consistent style are scarce (Tuxemon's 154 monsters are CC BY-SA with per-monster attribution). Pixel editors: Pixelorama (MIT), LibreSprite (GPL fork, unverified here) and Aseprite (source-available, ~US$20, compile-for-own-use allowed, outputs usable commercially).

### Cited Findings
**3D packs**
- Kenney Nature Kit: "over 330 nature themed objects including trees, rocks, stones, terrain elements, waterfalls, camping equipment, and plants", CC0 — [OpenGameArt](https://opengameart.org/content/nature-kit); Kenney Survival Kit: CC0 1.0, "attribution is not required", 70+ models, OBJ/FBX/glTF — [itch.io](https://kenney-assets.itch.io/survival-kit); Kenney Fantasy Town Kit CC0 — [OpenGameArt](https://opengameart.org/content/fantasy-town-kit) [official listings]
- Quaternius Stylized Nature MegaKit: 110+ models (40 trees, 35 plants/flowers, 27 rocks, grass, bushes), CC0, Unity/Unreal/Godot-ready — [itch.io](https://quaternius.itch.io/stylized-nature-megakit); [quaternius.com](https://quaternius.com/packs/stylizednaturemegakit.html) [official]
- Quaternius Medieval Village MegaKit: ~300 modular pieces (walls, roofs, doors, windows, props), 304 models, some animated; Standard free, Pro/Source tiers at US$9.99/$14.99+; CC0 per OpenGameArt — [quaternius.com](https://quaternius.com/packs/medievalvillagemegakit.html); [OpenGameArt](https://opengameart.org/content/medieval-village-megakit) [official/report]
- Quaternius Ultimate Monsters: "50 fully animated monsters", CC0, FBX/OBJ/Blend/glTF, free — [quaternius.com](https://quaternius.com/packs/ultimatemonsters.html); attack, death, run, walk clips per Sketchfab listing — [Sketchfab](https://sketchfab.com/3d-models/ultimate-monsters-pack-fd72e114d119488da71fe3a16f216c4f); LowPoly Animated Monsters (CC0; incl. flying) — [itch.io](https://quaternius.itch.io/lowpoly-animated-monsters) [official]
- Quaternius Asset License v1.0 (28 Aug 2026): renders/videos may be published and monetized with no attribution; raw-asset redistribution banned; not retroactive to earlier CC0 downloads — [Quaternius licence](https://quaternius.com/license.html) (via earlier report) [official]
- KayKit (Kay Lousberg): CC0; "Free for personal and commercial use, no attribution required"; Forest Nature Pack 200+ unique (1,500+ with recolours) trees/bushes/rocks/grass/terrain, mostly free, source files paid; Adventurers 5 (+3) rigged characters; Dungeon character pack 4 rigged/animated characters; author asks not to resell unmodified copies — [KayKit Forest](https://kaylousberg.itch.io/kaykit-forest); [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers); [KayKit Medieval Builder (OGA)](https://opengameart.org/content/kaykit-medieval-builder-pack-10); [KayKit character animations (OGA)](https://opengameart.org/content/kaykit-character-animations) [official listings]
- Kenney's CC0 characters are rigid/toy-rigged with few clips and no face shapes — `reports/3D horror Shorts animation and hooks.md` (local check) [measured here earlier]

**2D packs and monster sprites**
- Tuxemon: code GPL, art CC BY-SA (mix of 3.0 and 4.0); "Tuxemon Set 1": 154 monsters with front/back sprites and menu animations, attribution required per monster — [OpenGameArt Set 1](https://opengameart.org/content/tuxemon-set-1-154-monsters-front-and-back-sprites-and-menu-animations); [Tuxemon tileset (CC-BY-SA 3.0)](https://opengameart.org/content/tuxemon-tileset); [Game Bible](https://wiki.tuxemon.org/Game_Bible) [official]
- OPMon art CC BY-SA 4.0 (code GPL-3.0); Zoonami monster art is proprietary — [Tuxemon wiki: related projects](https://wiki.tuxemon.org/Zoonami) [report]
- itch.io packs set their own terms: PVFX Foundry / Foundry Thirteen are CC0 pixel VFX (96×96, 20 fps) with an "AI Assisted" disclosure — [nerijs](https://nerijs.itch.io/pvfx-foundry); [Thirteen](https://nerijs.itch.io/pvfx-foundry-thirteen); a paid Godot combat template states its game assets "are NOT mine and cannot be modified or reused" — [samhilly451](https://samhilly451.itch.io/turn-base-combat-system-template-godot); some VFX packs show no licence at all — [kiddolink](https://kiddolink.itch.io/vfx-slash-vol-2-pixel-art-effects); [combosmooth](https://combosmooth.itch.io/vfx-pack) [report]

**Sprite editors**
- Aseprite: changed from GPLv2 to a source-available EULA in 2016; you may compile and modify for your own purposes but not redistribute; FAQ: you can use your creations "in any product (personal or commercial)"; ~US$20 on Steam/itch — [Aseprite dev blog 2016](https://dev.aseprite.org/2016/09/01/new-source-code-license/); [Aseprite FAQ](https://aseprite.org/faq/); [EULA confusion thread](https://community.aseprite.org/t/eula-and-faq-confusion/9377); [MacPorts note](https://ports.macports.org/port/Aseprite/details/) [official/report]
- Pixelorama: MIT, free and open source — [AlternativeTo](https://alternativeto.net/software/pixelorama/?p=4); LibreSprite: free/open-source sprite editor — [AlternativeTo](https://www.alternativeto.net/software/libresprite/) [report]

### Inferences
- **Diorama kit [estimate]:** KayKit Forest (autumn recolours) or Quaternius Stylized Nature + Kenney Nature/Survival (camp, axe, logs, river rocks) + Quaternius Medieval Village / KayKit Medieval Builder (staged cabin and village) + Quaternius Ultimate Monsters (flying creature for the flyover; whether a dragon is among the 50 is unconfirmed). All glTF, all importable into Godot and Blender.
- **Look cohesion:** mixing packs from three artists will clash unless all materials are replaced by one shared palette/toon or flat-shaded material and one lighting rig — budget a day for a "look pass" per biome.
- **Originality/brand:** CC0 assets are used by many games and channels; the signature cast (tamer kid, 6-10 hero monsters) should be custom-modelled or heavily modified so the series is recognisable and not a "template" (also helps with YouTube's inauthentic-content rule noted in CLAUDE.md).
- **ShareAlike risk:** using CC BY-SA sprites (Tuxemon) inside a monetized video likely makes the video an adaptation subject to BY-SA terms and per-monster credit; prefer CC0 or own art for monsters [estimate, not legal advice].
- **Pixel art route:** Pixelorama (MIT) or a self-compiled Aseprite are both fine for original sprites; Aseprite's mature `--batch` CLI export (background knowledge, not verified this session) would let Claude export sprite sheets from `.aseprite` files in scripts.

### Gaps
- Whether Quaternius Ultimate Monsters includes a dragon (and its flight clip) was not confirmed; nor were the KayKit/Kenney packs checked for flying creatures.
- No consistent-style CC0 2D monster sprite set (front/back battle sprites) was found.
- LibreSprite's exact licence (believed GPL-2) and CLI capabilities were not verified; Aseprite's current official price not retrieved.
- OpenGameArt's licence menu (CC0, CC-BY, CC-BY-SA, GPL, OGA-BY) was not fetched; check each asset page.

## 5. Turn-based monster-battle presentation and battle VFX/camera (HP bars, type icons, move names, hit effects, shakes)

### Takeaway
Game battle "feel" is built from a small, well-documented kit: a hold before the move, a move-name banner, the hit with a white flash, a few frames of hit-stop, a decaying screen shake, particles, damage numbers and an HP bar that drains with a lag bar. All of it is cheap screen-space work on either machine; Effekseer (MIT runtime, Windows editor with PNG/sprite-sheet export) and a few CC0 Godot shaders supply particle/impact effects.

### Cited Findings
- Hit-stop (freeze frames), screen shake, particles and tweening are the core "juice" techniques; use sparingly; trigger hit-stop once per impact — [Wayline game-feel lesson](https://www.wayline.io/learn/game-feel/1) [report]
- A 2024 study tested hit-stop durations from 0 to 0.7 s and measured player response — [SciTePress 2024](https://www.scitepress.org/Papers/2024/124614/124614.pdf) [study; results not retrieved]
- Effekseer: runtime MIT, tool under LICENSE_TOOL, sample texture/effect data CC-0; editor on Windows 10+ (DirectX 11) or macOS; runtimes for OpenGL/WebGL/Vulkan etc. — [Effekseer overview](https://effekseer.github.io/Help_Tool/en/overview.html); Recorder exports a sprite sheet ("single image", X Count per row), a PNG image sequence, GIF or uncompressed AVI, with a "Make transparent" option — [Effekseer Recorder](https://effekseer.github.io/Help_Tool/en/ToolReference/record.html) [official]
- Godot shaders: "Actionlines Comic – Anime" code CC0 (derived from a Shadertoy shader whose terms may also apply) — [godotshaders](https://godotshaders.com/shader/actionlines-comic-anime/); a Godot 4 manga hit-impact post-process (radial lines + burst on an `impact` parameter 1.0→0.0), licence not shown — [godotshaders](https://godotshaders.com/shader/screen-sampled-black-and-white-manga-hit-impact-post-process-shader/) [official page/report]
- Fighting-game 3D that reads as 2D (Guilty Gear Xrd) used "limited animation" with stepped/held keys so each pose is distinct — [Kotaku](https://kotaku.com/breaking-down-the-animation-of-guilty-gear-and-dragonba-1836849279); GDC 2015 slides — [Motomura PDF](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf) [report/official]
- Local benchmark: two HP bars, HUD text and a large outlined caption drawn in Canvas2D add negligible cost inside a ~15 ms frame — section 3 [measured here]

### Inferences
- **Battle beat template (per move, ~2-3 s) [estimate]:** camera cut from the top-down world to a 3/4 battle angle (or a continuous dolly-in in 3D) → attacker anticipation pose (6-10 frames) → move-name banner slides in with type icon and colour → wind-up particles → contact frame: 1-2 frame white/inverted flash + radial lines → hit-stop 3-6 frames (both creatures frozen, particles keep moving) → shake (noise offset, exponential decay over ~8-12 frames) → damage number pops → HP bar: front bar snaps, a lighter "lag" bar drains over ~0.5 s, colour shifts green→yellow→red → "super effective"-style chip. Every number is a tunable constant in one battle-UI module reused across episodes.
- **Where to build it:** HUD/battle UI as a separate Canvas2D or pycairo layer (crisp text at 1080x1920, easy edits per script) composited over engine renders; particles and impacts in the engine (Godot GPU/CPUParticles, Blender particles/geometry nodes) or as Effekseer PNG sequences rendered on the laptop.
- **Timing for quality within the 10 h budget:** keep action shots on 1s (every frame unique) for smooth game motion; use held poses only for anticipation/impact emphasis, not as a cost-saver.
- **Type icons / move names:** design an original type system (icons as SVG drawn in code) — avoid any resemblance to Pokémon's type icons, HP-bar layout specifics or names (IP risk, not researched here).

### Gaps
- No free HD (non-pixel) game VFX sprite library with a clear commercial licence was found; Effekseer or procedural effects fill this gap.
- Effekseer's LICENSE_TOOL text and Linux support for the editor were not verified (editor listed for Windows/macOS only).
- Hit-stop durations preferred by viewers of video (not players) are unknown.

## 6. Creatures: rigs, clips and procedural motion (quadruped, flying, serpentine, blob)

### Takeaway
3D gives the most creature motion per hour: Quaternius' CC0 animated monsters work out of the box, Rigify ships Wolf/Horse/Cat/Shark/quadruped meta-rigs for custom monsters, and procedural IK (proven in Godot) handles feet, tails and wings. In 2D, creatures need either many drawn frames or Skeleton2D rigs, which users find laborious.

### Cited Findings
- Rigify meta-rig samples: Basic Quadruped, Human, Cat, Wolf, Horse, Shark (Basic Human lacks face/fingers); 1 unit = 1 m — [Blender manual source: Rigify basics](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/addons/rigify/basics.rst) [official; no bird sample confirmed]
- Mixamo: characters and animations "royalty free for personal, commercial, and non-profit projects"; no raw-file redistribution — [Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) [official]; described as "unmaintained" in July 2026 — [Cinevva](https://app.cinevva.com/guides/free-character-animations-rigging) [report, vendor]
- AccuRIG 2.0 (Jul 2025): free, FBX/USD export, free ActorCore account needed; ActorCore motions usable only inside AccuRIG, 32 free — [CG Channel](https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/); software usable commercially, rigged characters keep their own licence — [Reallusion forum](https://forum.reallusion.com/551972/reallusion-Accu-Rig-Free) [official staff]
- Quaternius UAL2: 65-joint skeleton, 43 clips; UBC bodies bind to the same joints — `reports/3D horror Shorts animation and hooks.md` [measured here earlier]
- Godot procedural spider/quadruped references and the lack of up-to-date 2D dog-walk tutorials — [80.lv](https://80.lv/articles/ik-driven-procedural-spider-locomotion-in-godot-4-5); [Godot forum](https://forum.godotengine.org/t/help-making-a-2d-procedural-walk-cycle-for-a-dog/107320) [report]

### Inferences
- **Per creature archetype [estimate]:** quadruped → Rigify Wolf/Horse/Cat + foot IK, procedural gait offsets; flying → wing bones with a sine flap whose amplitude follows speed, body bob, path-follow with banking, shadow from the directional light; serpentine → spline IK along a moving curve (Blender) or a chain of bones following a path with lag (Godot); blob → no skeleton: shape keys / squash-and-stretch driven by velocity, jiggle springs, eye sprites.
- Humanoid tamers: Quaternius UAL2/UBC (CC0-ish) or Mixamo clips; faces stay procedural (eye/mouth textures swapped by code) since the free bodies have no face shapes.
- A "signature" monster set of 6-10 custom models is the main asset investment; the CC0 Ultimate Monsters fill wild-encounter roles.

### Gaps
- No measured cost of Rigify-rigged creatures in Godot Compatibility on llvmpipe (the 3 fps test had no skinned meshes).
- No CC0 animated dragon was confirmed.

## 7. Lip sync, faces, blinks and breathing

### Takeaway
Rhubarb Lip Sync (MIT; ~1.7x real time on one container core) feeds every candidate engine; game-style faces need only 3-4 mouth shapes and seeded blinks, all driven by code.

### Cited Findings
- Rhubarb 1.14.0: MIT, output "belongs to you alone", script-guided (`-d`), 9 mouth shapes (A-H, X) as JSON; `.dat` switch data for Moho/OpenToonz — [Rhubarb](https://github.com/DanielSWolf/rhubarb-lip-sync) [official]; 8.57 s of speech took 14.4 s (PocketSphinx) or 1.5 s (phonetic) on one core — `reports/3D horror Shorts animation and hooks.md` [measured here earlier]
- Blender: Rhubarb Lipsync NG (MIT per listing; shape keys, bones, action sheets; listed for Blender 3.3-4.2) — [Blender Market](https://blendermarket.com/products/rhubarb-lipsync-ng); LipKit (GPL) supports Grease Pencil layers and shape keys — [Superhive](https://superhivemarket.com/products/lipkit) [official listings]
- MIT TalkingHead implements a procedural idle stack (eye contact, head movement, blinking, mood breathing) — [TalkingHead](https://github.com/met4citizen/TalkingHead) [official]

### Inferences
- Godot: generate an AnimationPlayer track (mouth texture frame or blendshape value) from Rhubarb JSON; Blender: a short `bpy` script keys shape keys/texture offsets — no add-on needed.
- Creatures "talk" through emotes rather than lip sync: ear/eye/body reactions and a short creature-voice sound, with game-style emote bubbles (!, ?, ♥, sweat drop) — cheap and very "game".

### Gaps
- Rhubarb Lipsync NG compatibility with Blender 4.3+/5.x not confirmed.

## 8. Anime-specific 2D rig and look tools (now lower priority): what they offer and why they rank lower

### Takeaway
Spine Professional, Live2D, Inochi2D, Rive, OpenToonz and Blender Grease Pencil/Goo Engine can produce excellent 2D/anime motion, but all are GUI-authored (or paywalled for export) and none renders headless from code on the container; with the owner's switch to a game look they are optional extras (e.g., Live2D/Inochi2D for dialogue portraits like visual-novel/RPG talk screens).

### Cited Findings
- Spine: Essential $99 list / $69 sale, Professional $439 / $369 (official page; an aggregator dated 21 Sep 2026 shows $449/$379); perpetual per-person licences; Enterprise at ≥US$500k revenue; IK and weighted meshes are Professional-only — [Spine purchase](https://esotericsoftware.com/spine-purchase); [GeekChamp](https://geekchamp.com/products/spine/); [Spine forum](https://esotericsoftware.com/forum/d/29824-spine-43--2d-animation-buy-form); [Spine IK](https://eu.esotericsoftware.com/spine-ik-constraints); [weighted meshes](https://fr.esotericsoftware.com/forum/d/17284-can-i-get-weighted-meshes) [official]
- Spine's Godot runtime needs a custom Godot build (crash/preview problems reported); DragonBones "seems discontinued"; Spriter Pro 2 long delayed — [Godot forum](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]
- Rive: Free plan ships "with a Rive splash screen" (3 collaborative files); Cadet $9/seat/mo removes it; runtimes MIT; editor video export (H.264, GIF, PNG/SVG sequence, WebM) "available on paid plans" via a Cloud Renderer; Linux CLI builds `.riv` offline, `--publish` "may add a watermark" below Cadet — [Rive pricing](https://rive.app/pricing); [Rive video export](https://rive.app/docs/editor/exporting/exporting-for-video-and-static-design.md); [Rive CLI](https://rive.app/cli) [official]
- Inochi Creator: BSD-2, branch `v0_8`, early access; video export via FFmpeg — [GitHub](https://github.com/Inochi2D/inochi-creator); [issoh.co.jp](https://www.issoh.co.jp/tech/details/10294/); no headless renderer/Python binding — `reports/CPU anime animation pipeline.md` [official/earlier report]
- Live2D Cubism FREE: commercial use allowed for general users and small enterprises under ¥10M annual sales; files exceeding FREE limits cannot be saved — [Live2D comparison](https://www.live2d.com/en/comparison/); [Live2D help](https://help.live2d.com/en/other/other_14/) [official]
- OpenToonz: Plastic-tool mesh rigging; Rhubarb lip-sync integration since v1.6 — [OpenToonz manual](https://opentoonz.readthedocs.io/); [What's New](https://opentoonz.readthedocs.io/ja/latest/whats_new.html) [official]
- Blender Grease Pencil 3 (4.3): multithreaded, Geometry Nodes support, layer groups, 2.5-3.4x smaller files, rewritten Python API — [release notes](https://developer.blender.org/docs/release_notes/4.3/grease_pencil/); Khara (Evangelion) moved its 3DCG to Blender in 2019 citing Grease Pencil — [blender.org](https://www.blender.org/?p=64752); Goo Engine (GPL fork, binaries via Patreon, £4.50/mo in 2023) used for "Samurai Blue: Afterimage" — [CG Channel](https://www.cgchannel.com/2023/07/check-out-goo-engine-blender-for-anime); [BlenderNation](https://www.blendernation.com/2024/09/16/anime-short-film-samurai-blue-afterimage/) [official/press]
- The Amazing Digital Circus (often assumed Blender) used Maya and Unreal — [80.lv](https://80.lv/articles/glitch-on-character-animations-in-the-amazing-digital-circus) [press]

### Inferences
- Useful niche in a game-style series: RPG-style dialogue portraits (bust shots that blink, breathe and talk) — Live2D FREE or Inochi2D on the laptop, exported once per expression as loops, then composited. Otherwise skip.
- Grease Pencil remains valuable inside Blender for hand-drawn VFX (slashes, speed lines, impact bursts) layered over 3D, even in a game look.

### Gaps
- Live2D FREE feature caps, Rive offline-render path, Inochi2D scriptable export: unverified.

## 9. Render budgets on our machines and the ranked recommendation (best quality within ~10 h per 60-90 s episode)

### Takeaway
Ranked by the best quality reachable in ~10 h of machine time per 60-90 s episode: **(1) Blender EEVEE on the RTX 3050 laptop for a stylized 3D world + close-up 3D battles, with 2D HUD/battle UI composited on the container; (2) Godot 4 3D (Forward+ on the laptop, Compatibility on the container), the best quality per production-hour and the most "game-native"; (3) Godot 4 2D HD sprites with lights, fully on the container; (4) a Canvas2D/Phaser 2D game look, fastest but flattest; (5) three.js; (6) Blender Cycles; (7) anime 2D rig tools.** The practical plan is a hybrid: build worlds and creatures once as glTF assets usable in both Godot and Blender, preview/iterate in Godot on the container, final-render hero 3D shots in Blender EEVEE on the laptop, and render all HUD/captions/battle UI as a crisp 2D layer.

### Cited Findings
- Container, measured: Godot 2D ~7.5 fps and Godot 3D ~3 fps at 720x1280 (Compatibility, llvmpipe, Xvfb) — coordinator test [measured here]; Canvas2D CPU raster 15-23 ms/frame (720x1280-1080x1920), 25-50 ms with JPEG transfer, 48-103 ms with raw RGBA — section 3 [measured here]; Blender EEVEE via llvmpipe ~8 s/frame (720x1280, 4 samples), ~15 s (1080x1920), 37-55 s (16 samples); Workbench ~2 s — `reports/CPU anime animation pipeline.md` [measured here earlier]; three.js SwiftShader ~1 fps — `reports/3D horror Shorts animation and hooks.md` [measured here earlier]; Rhubarb ~1.7x real time per core [measured here earlier]
- Laptop: Cycles OptiX Classroom ~116 s median per frame of the Classroom benchmark scene on an RTX 3050 4 GB Laptop (Blender 3.3; scene resolution and samples not stated in the source) — [Notebookcheck](https://notebookcheck-ru.com/nvidia-geforce-rtx-3050-laptop-gpu.554490.0.html) [measured, aggregated]; OIDN denoise ~1.2 s/frame on an i9-13900K — [Blender 4.1 notes](https://developer.blender.org/docs/release_notes/4.1/cycles/) [official]; Blender minimum 2 GB VRAM / OpenGL 4.3, 8 GB recommended (third-party summaries) — [MyArchitectAI](https://www.myarchitectai.com/blog/blender-system-requirements) [report]
- Godot Compatibility lacks DOF and volumetric fog; Forward+ needs Vulkan — [Godot renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) [official]
- TTS cost to reserve: Chatterbox Turbo ~40-60 s per sentence on the container CPU — `reports/3D horror Shorts animation and hooks.md` [measured here earlier]

### Gaps
- Must benchmark on the laptop before committing: (a) Blender EEVEE, the diorama scene at 1080x1920 with DOF, 32 and 64 samples, VRAM peak; (b) Godot 4.5 Forward+ Movie Maker, same scene; (c) Cycles OptiX at 64/128 samples + OIDN for one hero shot.
- Must benchmark on the container: Godot Compatibility with skinned creatures + 2x supersampling; Blender 5.x EEVEE via llvmpipe; Godot Forward+ on lavapipe after installing `mesa-vulkan-drivers` (optional).
- Laptop availability (hours per day it can render, thermals) is an owner question, not researched.

### Inferences
**Frame budgets [estimate, arithmetic].** 60 s @ 30 fps = 1,800 frames; 90 s @ 30 fps = 2,700 frames. Reserving ~1.5-2 h for TTS (~25-35 sentences × 40-60 s), Whisper-medium checks, retakes, compositing and encoding leaves ~8 h ≈ 28,800 s of render time per machine: **~10.7 s/frame for 90 s, ~16 s/frame for 60 s**, per machine. Using both machines in parallel on different shots roughly doubles it.

| Pipeline (final render location) | Per-frame cost (label) | 90 s episode render time | Fits ~10 h? | Quality ceiling for the game look |
|---|---|---|---|---|
| Blender EEVEE, laptop, 1080x1920, DOF + volumetrics, 32-64 samples | ~0.5-4 s [estimate; unmeasured on 3050] | ~0.4-3 h | Yes, with headroom for more samples, motion blur, bigger scenes | Highest: soft shadows, real tilt-shift DOF, volumetric light shafts, bloom, motion blur |
| Blender Cycles, laptop OptiX, 64-128 samples + OIDN | ~5-30 s [estimate; Classroom interior benchmark ≈116 s per frame] | ~4-22 h | Only for 60 s or for hero shots | Highest lighting realism, but a stylized game look gains little over EEVEE |
| Godot 4 Forward+, laptop | ≪1 s [estimate; real-time engine] | minutes | Yes, easily (supersample 2x, high shadow quality) | High: DOF, volumetric fog, SDFGI, glow; game-authentic |
| Godot 4 3D Compatibility, container | 0.33 s [measured here] | ~15 min (≈1 h at 2x supersample, est.) | Yes | Medium-high: no DOF/volumetrics (fake DOF in post) |
| Blender EEVEE via llvmpipe, container, 720x1280, 4 samples | ~8 s [measured here] | ~6 h | Yes for 720p; 1080x1920 (~15 s) only for ≤60 s | High look, but 4 samples = noisier DOF/shadows |
| Godot 4 2D (HD sprites, lights, particles), container | 0.13 s [measured here] | ~6 min | Yes | Medium-high if the sprite art is strong; flat compared with lit 3D |
| Canvas2D / Phaser canvas, container | 0.015-0.05 s [measured here] | ~1-3 min | Yes | Medium: no real lighting/shaders on the CPU path |
| three.js, container (SwiftShader) | ~1 s [measured here] | ~45 min | Yes | Medium-high, but weak tooling |

**Ranked recommendation (quality first, within ~10 h machine time per 60-90 s episode):**

1. **Blender EEVEE on the laptop for all 3D world and battle shots** (top-down diorama, day/night, staged building, dragon flyover with shadow, then close-up 3/4 battle shots of creatures), driven by `bpy` scripts Claude writes; container renders previews/backup shots in EEVEE-llvmpipe at 720x1280 and composites the HUD, battle UI, captions and 2D impact effects (pycairo or CPU Canvas2D at ~25-50 ms/frame). Why first: highest lighting and DOF quality that fits the budget; full scripting; assets (Quaternius/KayKit/Kenney CC0 glTF, Rigify creatures) proven. Risks: 4 GB VRAM (keep textures ≤2K, close other apps), all finals depend on the laptop, and the first scene-building scripts are a multi-day investment. Production-hours: highest setup cost, then reusable sets per biome.
2. **Godot 4 3D** (same glTF assets): final renders in Forward+ on the laptop for DOF/volumetric fog, or entirely on the container in Compatibility at the measured ~3 fps with post-process tilt-shift. Why second: slightly lower lighting ceiling than EEVEE, but the best quality per production-hour, game-authentic by construction, and the best tool for systems (day/night clock, villagers walking, construction stages, particle fireflies, procedural creature IK, turn-based battle logic) — strong for the 100-day-survival-style world shots. Could be ranked first if laptop benchmarks show EEVEE's advantage is small for this stylized look.
3. **Godot 4 2D, fully on the container** (HD or pixel sprites, Skeleton2D for big monsters, CanvasModulate + PointLight2D night, particles): ~6 min per episode measured-rate render, so all budget goes into art and frames on 1s. Quality depends on drawing original sprites (Pixelorama/Aseprite); the only top-quality route that never needs the laptop.
4. **Canvas2D / Phaser 4 canvas on the container:** best for the HUD and battle-UI layers in every pipeline, and for quick 2D episodes; flat lighting limits it as the main look.
5. **three.js (current renderer):** keep only for existing channels; Godot dominates it here on speed, tools and features.
6. **Blender Cycles:** only for a few hero shots or still plates (title cards, thumbnails) on the laptop; on the container CPU it is too slow for animation.
7. **Anime 2D rig tools (Spine, Live2D, Inochi2D, Rive, OpenToonz):** optional dialogue portraits only.

**Extending the diorama into a monster-taming world [estimate]:** open each episode on the top-down world (hook: a "wrong" thing visible in frame 0, e.g., red eyes in the trees at dusk, with the HUD clock and a rule chip), follow the tamer through the day with HUD counters, trigger an encounter (screen flash + swirl transition, or one continuous 3D camera move from top-down to a low 3/4 angle), play the turn-based battle with the section-5 beat template (move banner, type icon, hit flash, hit-stop, shake, HP lag bar, damage numbers), then pull back to the world as night falls and end on the either/or question over the frozen HUD. Close-ups give the creatures faces and acting (emotes, blinks, squash-and-stretch) that the reference's tiny figures lack — the main way to "beat it by far", together with 1080x1920 output, real DOF/volumetric light on the laptop, and a recurring original cast.
