# Open-source / free (non-AI) pipelines for anime character and creature animation on a CPU container + RTX 3050 laptop

Scope note. This extends two earlier local reports and does not repeat them: `reports/CPU anime animation pipeline.md` (pycairo/OpenCV puppet warps measured at 25-60 ms/frame, THA3, Inochi2D/Live2D as GUI-only, Synfig/OpenToonz/Krita CLIs, EEVEE-on-llvmpipe timings) and `reports/3D horror Shorts animation and hooks.md` (three.js llvmpipe vs SwiftShader, Quaternius UAL2 bodies, Rhubarb timing, Godot `--headless` disabling rendering). Where a number below comes from those reports it is labelled "earlier report, measured here". Research date: 30 Oct 2026. Labels: **[official]** = vendor docs, **[measured]** = timed by someone (source given), **[report]** = forum/press anecdote, **[estimate]** = my arithmetic or judgement.

## 1. Rigged cut-out / mesh-deform 2D tools: rig quality, programmability, headless rendering, licences

### Takeaway
No free 2D rigging tool both (a) gives Spine/Live2D-grade mesh deformation and (b) renders headless on a GPU-less Linux box from files Claude can write. Godot's Skeleton2D + Polygon2D is the only free, scriptable, text-file-based mesh-deform rig with an offline frame recorder (Movie Maker), but users call it cumbersome and the CPU-only render path is untested; Spine Professional (one-time ~US$369-379 sale price) is the strongest commercial cut-out tool; Rive, Live2D FREE and Inochi2D are GUI-authored and either paywall export (Rive) or lack a headless renderer (Inochi2D).

### Cited Findings
**Godot 2D skeletons + Movie Maker**
- Godot 4.7 stable docs: 2D characters are built from Polygon2D parts sharing one texture, a Skeleton2D with Bone2D chain, per-bone weight painting ("white means full influence"); you "animate the bones, not the polygons". Known limit: default triangulation "can bend unexpectedly", fixed by adding internal vertices. The page is flagged "Work in progress ... not yet updated for Godot 4.7" and does not mention 2D IK — [Godot docs: 2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html) [official, fetched Oct 2026]
- User experience 2024-2026: Skeleton2D "seems you have to do a lot of extra work but you can get the job done" (Jun 2024); "pretty cumbersome" (May 2025); "The skeletal system looks very cool in demos, but is very frustrating in practice" (Dec 2025); a free human Skeleton2D rig with example animations was shared in Jun 2026 via the Scalable Vector Shapes 2D add-on, "not perfect yet" — [Godot forum thread](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]
- Same thread: Spine's Godot runtime requires a custom Godot build, and one user reported editor crashes on exit and animations not previewable; DragonBones "seems discontinued"; Spriter Pro 2 was promised for ~5 years and reviewers said the app "stopped working altogether" — [Godot forum thread](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]
- Godot 4.6 brought IK back only as `IKModifier3D` (3D); 2D IK still needs a `SkeletonModifier2D` with your own solver — [TabNews (pt-BR) on Godot 4.6](https://www.tabnews.com.br/zivaengine/godot-4-6-trouxe-o-ik-de-volta-pra-quem-faz-jogo-3d-isso-importa-mais-que-o-jolt) [report, single secondary source]
- Movie Maker (Godot 4.7 docs): `--write-movie out.avi`, `--fixed-fps 30`, `--resolution WxH`, `--quit-after N`; works in exported projects. Formats: OGV (Theora/Vorbis, recording only in editor builds), AVI (MJPEG, 4 GB limit), PNG sequence + WAV (supports transparency with `transparent_bg`), or custom via GDExtension. "The output video will always have perfect frame pacing"; "Faster hardware will allow you to render ... in less time, but the visual output remains identical". Audio mix rate must be divisible by FPS. The page does not mention `--headless` — [Godot docs: Creating movies](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) [official]
- `--headless` "disables all rendering code" — [godot-proposals #5790](https://github.com/godotengine/godot-proposals/issues/5790) (via earlier report) [official]; a 2020 issue says Godot under `xvfb-run` needs a software renderer, and SwiftShader worked but was "glitchy" and "quite slow" — [godot #38428](https://github.com/godotengine/godot/issues/38428) [report, 2020, may be outdated]

**Spine (Esoteric Software) — commercial reference point**
- Prices: Essential US$99 list / $69 sale; Professional $439 list / $369 sale on the official purchase page — [Spine purchase](https://esotericsoftware.com/spine-purchase) [official]; an aggregator dated 21 Sep 2026 shows Professional $449 list / $379 — [GeekChamp](https://geekchamp.com/products/spine/) [report; conflicts slightly with the official page snapshot]
- Essential/Professional are perpetual, per named person, up to 2 computers; Enterprise (yearly) required at ≥US$500,000 annual revenue — [Spine forum (staff)](https://esotericsoftware.com/forum/d/29824-spine-43--2d-animation-buy-form) [official staff reply]
- IK constraints "are not available in Spine Essential" — [Spine IK constraints](https://eu.esotericsoftware.com/spine-ik-constraints) [official]; weighted meshes are "reserved for Spine Professional" — [Spine forum](https://fr.esotericsoftware.com/forum/d/17284-can-i-get-weighted-meshes) [official staff reply]. So the mesh-deform/parallax head turns that make Spine look good need Professional.

**DragonBones / Spriter**
- No official discontinuation notice found; AlternativeTo still lists DragonBones as free and open source; users describe it as "seems discontinued"; COA Tools for Blender can export to DragonBones format — [AlternativeTo](https://alternativeto.net/software/dragonbones); [Godot forum](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]

**Rive**
- Plans (fetched Oct 2026): Free $0 ("Build and ship with a Rive splash screen"; "3 collaborative files"; "Export .riv files with a splash screen"); Cadet $9/seat/mo ("Ship apps and games without the splash screen"); Voyager $32; Enterprise $120 for $10M+ revenue. "No revenue share, no runtime fees, no royalties, and MIT open-source runtimes" — [Rive pricing](https://rive.app/pricing) [official]
- Editor video/image export formats: H.264, GIF, PNG sequence, SVG sequence, WebM; "Exporting video and images is available on paid plans"; rendering runs on Rive's "Cloud Renderer" — [Rive docs: exporting for video](https://rive.app/docs/editor/exporting/exporting-for-video-and-static-design.md) [official]
- Rive CLI runs on "Linux x86_64", creates/previews projects and builds `.riv` locally "signed out and offline"; links to examples for "rendering without a window, and CI"; `--publish` "may add a watermark" unless the project is bound to an account file in a Cadet-or-higher workspace — [Rive CLI](https://rive.app/cli) [official]
- Exported files "don't phone home" and keep working regardless of plan — [Rive docs: exporting for runtime](https://rive.app/docs/editor/exporting/exporting-for-runtime) [official, via search snippet]

**Inochi2D**
- Inochi Creator: BSD-2-Clause, not archived, default branch `v0_8`, 132 open issues; stable builds on itch.io, Steam listed as wishlist/early access; Windows and Linux build instructions — [GitHub inochi-creator](https://github.com/Inochi2D/inochi-creator) [official]
- Inochi Creator can export animations as video via FFmpeg integration and PNG/JPEG/TGA images — [issoh.co.jp (ja)](https://www.issoh.co.jp/tech/details/10294/); [LinuxLinks](https://linuxlinks.com/inochi-creator-create-edit-inochi2d-puppets); Steam page: "usable for rigging models, adding physics, exporting video, creating animations", early access — [Steam](https://store.steampowered.com/app/2108550) [official/report]
- NLnet funds a planned 0.9 update aimed at game-engine support, no date — [NLnet](https://nlnet.nl/project/Inochi2D/) [official]
- Earlier report: no Python binding, no headless renderer, runtimes "prototype"; a VTuber reported model-file corruption — `reports/CPU anime animation pipeline.md` (citing [Inochi2D](https://github.com/Inochi2D/inochi2d), [Inox2D](https://github.com/Inochi2D/inox2d))

**Live2D Cubism**
- FREE edition may be used commercially only by "General Users and Small-Scale Enterprises (annual sales less than 10 million yen)"; ≥¥10M needs PRO; FREE has feature restrictions and "If you exceed the limit of the FREE version, you will not be able to save the file"; the trial is "demonstration, evaluation and training" only — [Live2D comparison](https://www.live2d.com/en/comparison/); [Live2D help](https://help.live2d.com/en/other/other_14/) [official]

**OpenToonz**
- Manual has a full Plastic-tool chapter (mesh building, skeletons, rigidity, parenting, cut-out animation) — [OpenToonz manual](https://opentoonz.readthedocs.io/) [official]
- v1.6 added "Rhubarb integration for automatic lip-syncing (Tahoma2D port)" — [OpenToonz What's New](https://opentoonz.readthedocs.io/ja/latest/whats_new.html) [official]
- `tcomposer` CLI renders artist-made scenes but always creates a Qt application; untested headless — earlier report citing [tcomposer source](https://raw.githubusercontent.com/opentoonz/opentoonz/master/toonz/sources/tcomposer/tcomposer.cpp)

### Inferences
- **Programmability ranking [estimate; file-format facts not re-fetched this session]:** Godot `.tscn` scenes and `.tres` animations are plain text and GDScript can build Polygon2D/Bone2D rigs at runtime, so Claude can generate and drive a rig entirely in code — the only free mesh-deform option where that is realistic. Spine's JSON skeleton format is documented and writable by code, but meshes/weights need Professional to author and the free runtimes are licence-tied to Spine owners. Synfig `.sif` and OpenToonz `.tnz` are XML but their rig semantics are awkward to synthesize. Rive `.riv` and Live2D `.moc3` are binary and editor-authored; Inochi2D's `.inp` is a container that Creator writes — all three require a human in the GUI.
- **Rive verdict:** usable only on the paid Cadet plan ($9/mo) for clean `.riv` or video export; the free plan adds a splash screen/watermark. Offline rendering is plausible via the MIT runtimes (e.g., stepping the web runtime frame by frame in headless Chrome, or the CLI's "rendering without a window" examples), but nothing found documents a frame-exact video render path, so it is an engineering gamble. Rive's strength (state machines for apps/games) is not what a narrative series needs.
- **Spine verdict:** the best pure-2D cut-out rig if the owner pays ~$369-379 once for Professional; render via the editor's own export on the laptop (Spine editor runs on Windows/Linux/macOS — background knowledge) rather than a custom renderer. Still a "puppet" look unless animators use meshes for perspective turns and frame-swapped drawings for big actions.
- **Godot 2D verdict:** free, code-first and has Movie Maker, but its 2D rig tooling is the weakest of the group and 2D IK must be written by hand. It is worth it mainly if Godot is also used for creatures/VFX (section 2-3), so one engine covers everything.
- **Live2D/Inochi2D verdict:** both remain talking-head/VTuber tools; their natural motion range (head ±30°, body sway) suits dialogue close-ups but not running quadrupeds or battles. Live2D FREE is commercially allowed for this channel's size (well under ¥10M sales) but save limits may block a full rig.
- Mesh deformation alone does not fix the "paper-doll" complaint; it is the absence of drawn key poses, smears and timing (section 3) that reads as puppet. Any cut-out tool needs swap-drawings for hands, mouths, and action poses.

### Gaps
- No CPU/headless render benchmark exists for Godot 2D Movie Maker under Xvfb + Mesa llvmpipe (Compatibility/OpenGL renderer). Needs a local test (Godot binary is not installed in the container now).
- Rive's "rendering without a window" CLI examples were not readable; whether they produce frame-exact video offline is unknown.
- Pencil2D was not researched (no sources fetched); background knowledge: frame-by-frame raster/vector drawing with no bones — not a fit for automated pipelines.
- Live2D FREE's exact feature caps (parameters, art meshes, deformers) were not retrieved.
- Inochi Creator's video export could not be verified as scriptable/CLI; Inochi Session's offline render ability is unconfirmed.
- DragonBones' official status (last release date) not confirmed from its repository.

## 2. 3D toon / 2.5D: Blender (EEVEE/Cycles/Workbench, Grease Pencil 3), toon looks, free creature assets, rigging, procedural creature motion, Godot 3D

### Takeaway
Blender is the most proven free route to "anime in 3D" (Khara/Evangelion adopted it; indie shorts use it with the Goo Engine fork), and Grease Pencil 3 (Blender 4.3+) adds hand-drawn lines, effects and geometry-node control inside the 3D scene; but EEVEE needs a GPU (the container only manages it through llvmpipe at ~8-15 s/frame) and 4 GB VRAM is tight. For a monster tamer, the cheapest high-quality creature path is CC0 animated monsters (Quaternius: 50 fully animated monsters) + Rigify quadruped/shark metarigs + procedural IK, rendered toon-shaded on the laptop.

### Cited Findings
**Blender rendering on the two machines**
- EEVEE "only uses the power of the GPU", with "no plan to support CPU (software) rendering" — [Blender manual: EEVEE limitations](https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html) (via earlier report) [official]
- Despite that, EEVEE rendered on this GPU-less container through Mesa llvmpipe over EGL after installing `libegl1`/`libegl-mesa0`: ~8 s/frame at 720x1280 with 4 samples, ~15 s at 1080x1920, 37-55 s at 16 samples; Workbench ~2 s/frame; Cycles ignored the inverted-hull backface culling; scripted Freestyle produced no strokes — `reports/CPU anime animation pipeline.md` [earlier report, measured here, contended 1.3-3.4 of 4 cores busy]
- OIDN denoising alone ~1.2 s/frame on Junkshop on an i9-13900K — [Blender 4.1 Cycles notes](https://developer.blender.org/docs/release_notes/4.1/cycles/) [official]
- Third-party requirement summaries (2026): minimum 2 GB VRAM, OpenGL 4.3; Blender 5.0 added Vulkan 1.3 alongside OpenGL 4.3; recommended 8 GB VRAM — [Renderahouse](https://www.renderahouse.com/blog/blender-system-requirements); [MyArchitectAI](https://www.myarchitectai.com/blog/blender-system-requirements) [report; official requirements page not fetched]
- 4 GB cards: one user found EEVEE crashed on selection with heavy textures while Cycles worked (<1 min/frame) — [GameDev.tv forum](https://community.gamedev.tv/t/blender-is-out-of-memory-i-think-any-solution/256347); a bug report showed a ~1.2 GiB single render-buffer allocation failing on a 4 GB card at a very large output size — [developer.blender.org T64900](https://developer.blender.org/T64900); Blender used ~900 MiB VRAM right after loading factory defaults — [projects.blender.org #92139](https://projects.blender.org/blender/blender/issues/92139) [report]

**Grease Pencil 3 (2D inside 3D)**
- Blender 4.3 rewrote Grease Pencil: "uses multiple threads whenever possible"; Geometry Nodes support; layer groups; files 2.5-3.4x smaller (Pirate 158.8→64.4 MB; Picknick 147.3→42.8 MB); 4.3 files don't load in 4.2; Screen-Space thickness removed; Python API rewritten so add-ons need migration — [Blender 4.3 GP release notes](https://developer.blender.org/docs/release_notes/4.3/grease_pencil/) [official; no speed numbers given]
- Studio Khara (Evangelion) announced in 2019 a move to Blender for future 3DCG, citing Grease Pencil ("a 3D tool that works like paper and pencil"); Unity covers what Blender cannot; full-switch completion not confirmed in sources — [blender.org](https://www.blender.org/?p=64752); [Anime News Network](https://m.animenewsnetwork.com/news/2019-08-18/khara-to-completely-switch-to-blender-open-source-3d-software-after-evangelion-3.0-1.0/.150173) [official/press, 2019]
- Blender Studio's "Hero" (2018) was the Grease Pencil 2.0 showcase short — [BlenderNation](https://www.blendernation.com/2018/04/16/hero-blender-grease-pencil-showcase/); [Blender Studio](https://studio.blender.org/blog/hero-teaser-trailer/) [official]
- A Grease Pencil production ("Hellskate") followed a traditional pipeline: rough keys → full rough animation at 12 fps → clean-up — [BlenderNation 2017](https://www.blendernation.com/2017/10/24/hellskate-grease-pencil-production/) [report]
- "Project Acheron" documents a Spider-Verse-inspired Blender workflow (2025) — [BlenderNation](https://www.blendernation.com/2025/06/20/project-acheron-spider-verse-inspired-workflow/) [report; details not fetched]

**Anime toon look: Goo Engine and NPR**
- Goo Engine is DillonGoo Studios' anime-focused Blender fork; source under GPL (buildable free), compiled binaries via Patreon (£4.50/mo in 2023) — [CG Channel 2023](https://www.cgchannel.com/2023/07/check-out-goo-engine-blender-for-anime); [GameFromScratch](https://gamefromscratch.com/goo-engine-blender-for-anime/) [report, price may be outdated]
- Dec 2024: Blender published an experimental NPR build; DillonGoo will keep developing Goo Engine in parallel and its lead developer works with EEVEE developer Miguel Pozo — [CG Channel Dec 2024](https://www.cgchannel.com/2024/12/check-out-blenders-experimental-non-photorealistic-rendering-build/) [press]
- "Samurai Blue: Afterimage" (Sept 2024), an anime short "Created by Winterstellar Studios in Blender and Goo Engine" — [BlenderNation](https://www.blendernation.com/2024/09/16/anime-short-film-samurai-blue-afterimage/) [report]

**Free creature/character assets and licences**
- Quaternius "Ultimate Monsters": "50 fully animated monsters", CC0, FBX/OBJ/Blend/glTF, free ("free to use in personal and commercial projects") — [quaternius.com](https://quaternius.com/packs/ultimatemonsters.html) [official]; Sketchfab listing describes attack, death, running and walking animations — [Sketchfab](https://sketchfab.com/3d-models/ultimate-monsters-pack-fd72e114d119488da71fe3a16f216c4f) [report]
- Quaternius "LowPoly Animated Monsters" (CC0; punch, attack, jump, flying, walk) and "Animated Easy Enemies" (CC0; movement, attack, jump, death) — [itch.io](https://quaternius.itch.io/lowpoly-animated-monsters); [itch.io](https://quaternius.itch.io/animated-easy-enemies) [official]
- Quaternius Asset License v1.0 (28 Aug 2026) still lets renders/videos be published and monetized with no attribution; bans redistributing raw assets; not retroactive — [Quaternius licence](https://quaternius.com/license.html) (via earlier report) [official]
- Mixamo: characters and animations usable "royalty free for personal, commercial, and non-profit projects"; raw-file redistribution not allowed — [Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) [official]; a July 2026 guide calls Mixamo "unmaintained" — [Cinevva](https://app.cinevva.com/guides/free-character-animations-rigging) [report, vendor]
- AccuRIG 2.0 (Jul 2025): free; exports FBX/USD; needs a free ActorCore account to export; ActorCore motions usable only inside AccuRIG, 32 free at the time — [CG Channel](https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/); Reallusion admin: software usable commercially but the rigged character keeps its own licence — [Reallusion forum](https://forum.reallusion.com/551972/reallusion-Accu-Rig-Free) [official staff reply, ~2 years old]
- Rigify ships meta-rig samples: Basic Quadruped, Human, Cat, Wolf, Horse, Shark (Basic Human lacks face/fingers); assumes 1 unit = 1 m — [Blender manual source: Rigify basics](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/addons/rigify/basics.rst) [official; a bird sample is not confirmed]

**Procedural creature locomotion**
- Godot 4.5 spider (2025): Marker3D foot targets chased by SkeletonIK3D; a step arc triggers when a foot strays past a threshold; legs move in diagonal pairs; body height = average of feet; body aligned to surface normal — [80.lv](https://80.lv/articles/ik-driven-procedural-spider-locomotion-in-godot-4-5) [report]
- University of Tartu 2025 course project: 2D spider whose legs raycast for surfaces to choose steps, with repo and playable build — [UT course page](https://courses.cs.ut.ee/2025/cg/fall/Main/Project-ProceduralAnimation) [report]
- A Godot user asking for a 2D procedural dog walk found "no up to date tutorials" — [Godot forum](https://forum.godotengine.org/t/help-making-a-2d-procedural-walk-cycle-for-a-dog/107320) [report]
- Godot 4.6 reintroduced 3D IK as `IKModifier3D`; `SkeletonIK3D` is deprecated but usable — [TabNews](https://www.tabnews.com.br/zivaengine/godot-4-6-trouxe-o-ik-de-volta-pra-quem-faz-jogo-3d-isso-importa-mais-que-o-jolt) [report]

**Monster-tamer precedent made with free tools**
- Cassette Beasts (2023, 120 monsters, >14,000 fusions, every fusion animated on screen) was built in Godot by a two-person core team (Bytten Studio); co-founder: they "could not have developed the game by themselves" without Godot; native Linux — [Wikipedia](https://en.wikipedia.org/wiki/Cassette_Beasts); [Wireframe](https://wireframe.raspberrypi.com/articles/creature-collecting-gets-an-analogue-upgrade-in-cassette-beasts); [GamingOnLinux](https://gamingonlinux.com/2023/04/charming-monster-collector-cassette-beasts-is-out-now) [press]

### Inferences
- **Laptop = Blender EEVEE render box; container = layout, scripting, light renders.** On the RTX 3050 4 GB, EEVEE should work for toon scenes at 1080x1920/1920x1080 if textures stay ≤2K, shadows are modest and other GPU apps are closed (inferred from the 4 GB crash reports above). On the container, EEVEE via llvmpipe at ~15 s/frame for 1080x1920 means a 40 s Short at 24 fps (960 frames) ≈ 4 h; rendering characters on 2s (480 unique frames) halves that to ≈ 2 h [estimate].
- **Look:** the anime 3D look comes from (1) toon ramp shading (Shader-to-RGB in EEVEE, measured working on llvmpipe in the earlier report), (2) inverted-hull or Grease Pencil Line Art outlines, (3) stepped timing on 2s/3s (section 3), and (4) per-shot pose sculpting/face-normal tweaks as in Guilty Gear Xrd. Goo Engine adds anime-specific shading controls but costs a Patreon subscription for binaries or a self-build; vanilla Blender 4.3+/5.x is enough to start.
- **Creatures:** Quaternius Ultimate Monsters (50 animated, CC0) gives a monster roster with walk/run/attack/death clips immediately; their low-poly toy look must be restyled (toon ramp, outlines, custom textures/eyes) to avoid a "game asset" read. Signature monsters should be custom-modelled and rigged with Rigify Wolf/Horse/Cat/Shark templates (quadruped, serpent/fish-like via shark spine), plus procedural IK for feet and spline-IK tails. Blob creatures need no skeleton: shape keys / lattice + squash-and-stretch driven by code.
- **Rigging route:** AccuRIG/Mixamo are humanoid-only; Mixamo's licence is the clearer of the two for monetized renders; AccuRIG is fine commercially for the software but requires an account and the ActorCore motion library is mostly paid.
- **Programmability:** Blender is fully scriptable (`bpy`), including the rewritten GP3 Python API, so Claude can build scenes, cameras, stepped keys and render jobs as Python files that the owner runs on the laptop with `blender -b file.blend -P script.py -a`.
- Godot 3D toon (StandardMaterial3D toon diffuse/specular modes, custom shaders) + Movie Maker is a second viable 3D route (background knowledge, not fetched); it is strongest for procedural creatures/particles but its anime-shading ecosystem is thinner than Blender's.

### Gaps
- No measured EEVEE (or EEVEE Next/Blender 5.x) toon render times on an RTX 3050 Laptop 4 GB were found — needs a laptop benchmark (one 1080x1920 toon frame, 16 samples).
- No CPU render timing for Grease Pencil-only scenes (GP renders through EEVEE/Workbench) was found; likely much cheaper than full EEVEE but unmeasured. Blender is not installed in the container right now.
- Whether EEVEE in Blender 5.x still runs on llvmpipe (Vulkan/OpenGL extension changes in 5.0) is unverified; the earlier measurement may have been on 4.x.
- Free MToon/VRM-for-Blender shader licence and performance not researched this session.
- Godot 3D toon + Movie Maker on llvmpipe speed: no source.
- The Studio Khara full-switch outcome and the specific Blender features used in later productions were not confirmed.
- The Amazing Digital Circus is commonly assumed to be Blender; the best source says its pipeline used Maya and Unreal Engine — [80.lv](https://80.lv/articles/glitch-on-character-animations-in-the-amazing-digital-circus); Glitch job ads list Maya, Houdini, Unreal, Toon Boom Harmony — [Working Nomads](https://www.workingnomads.com/jobs/3d-vfx-artist-glitch-productions) — so it is not a free-tool example.

## 3. Battle VFX and anime camera language: impact frames, speed lines, smears, hit-stop, shake, particles, sakuga timing

### Takeaway
The techniques that make anime battles read as "animated" rather than "puppeted" are timing techniques (limited animation on 2s/3s with stepped/held keys, hit-stop, anticipation) plus 2D overlays (impact frames, speed lines, flashes). These are cheap to implement procedurally on either machine; Effekseer (MIT runtime, Windows/macOS editor with PNG/sprite-sheet export) and a few CC0 Godot shaders/sprite packs cover particle VFX, though most free sprite VFX are pixel-art and would clash with an anime look.

### Cited Findings
**Limited animation in 3D (Guilty Gear Xrd as the model)**
- Arc System Works used "limited animation" for clarity of poses over smoothness; animators avoided automatic interpolation using "stepped keys" and "held keys" so each pose is distinct — [Kotaku breakdown](https://kotaku.com/breaking-down-the-animation-of-guilty-gear-and-dragonba-1836849279); [New Frame Plus transcript (Amara)](https://amara.org/videos/bDmpkclvfB5I/info/the-animation-of-guilty-gear-xrd-dragon-ball-fighterz) [report]
- Source talk: Junya Motomura, "GuiltyGearXrd's Art Style: The X Factor Between 2D and 3D" (GDC 2015) — [slides PDF](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf) [official; contents not retrieved this session]; CEDEC 2015 talk on "real-time limited animation" focused on removing 3D-looking qualities and drawing 2D-style poses in 3D — [Famitsu (ja)](https://www.famitsu.com/news/201508/27087024.html) [press]
- Limited animation holds each drawing for two or three frames to make up 24 fps — [Tsukuba IWAIT paper](https://www.cgg.cs.tsukuba.ac.jp/projects/2013/motion_frame_omission/data/IWAIT.pdf) [study]

**Hit-stop and shake**
- A 2024 study tested hit-stop durations from 0 to 0.7 s in an action game and measured player response — [SciTePress 2024](https://www.scitepress.org/Papers/2024/124614/124614.pdf) [study; numeric results not retrieved]
- Game-feel guidance: hit-stop (freeze frames), screen shake, particles and tweening are core "juice"; use sparingly; trigger hit-stop once per impact — [Wayline lesson](https://www.wayline.io/learn/game-feel/1) [report]

**Effekseer (particle VFX editor)**
- Runtime licence MIT; tool under a separate LICENSE_TOOL; sample texture/effect data CC-0; editor runs on Windows 10+ (DirectX 11) or macOS 10.12+; Linux editor not listed; runtimes for DX9-12, Metal, Vulkan, OpenGL, WebGL — [Effekseer overview](https://effekseer.github.io/Help_Tool/en/overview.html) [official]
- Recorder exports "a single image" (sprite sheet, frames upper-left to lower-right, X Count per row), "images" (PNG sequence), GIF, or uncompressed AVI; "Make transparent" option for non-GIF output — [Effekseer Recorder](https://effekseer.github.io/Help_Tool/en/ToolReference/record.html) [official]

**Free shaders and sprite VFX (licences vary)**
- "Actionlines Comic – Anime" Godot shader: code CC0 (images/videos on the page excluded); derived from a Shadertoy shader whose terms may also apply — [godotshaders.com](https://godotshaders.com/shader/actionlines-comic-anime/) [official page]
- "Screen-Sampled Black-and-White Manga Hit Impact" post-process (Godot 4, CanvasItem): radial speed lines + burst driven by an `impact` parameter animated 1.0→0.0 for hits/cut-ins; licence not shown in results — [godotshaders.com](https://godotshaders.com/shader/screen-sampled-black-and-white-manga-hit-impact-post-process-shader/); "Anime Style Speedlines" (planar or radial), licence not shown — [godotshaders.com](https://godotshaders.com/?p=16778) [report]
- CC0 sprite VFX: PVFX Foundry (combat, elemental, portal etc.; pixel art; page discloses "AI Assisted") — [itch.io](https://nerijs.itch.io/pvfx-foundry); PVFX Foundry Thirteen (CC0, 96×96, 20 fps, transparent) — [itch.io](https://nerijs.itch.io/pvfx-foundry-thirteen); Explosion Spriteanim minipack (CC0 per a comment) — [itch.io](https://reactorcore.itch.io/explosion-spriteanim-sheet-minipack); paid slash packs with unstated licence — [kiddolink](https://kiddolink.itch.io/vfx-slash-vol-2-pixel-art-effects) [report]

### Inferences
- **Timing is the biggest quality lever and costs nothing [estimate]:** set all character/creature F-curves to constant (stepped) interpolation, or post-quantize poses to 2s (dialogue, walks) and 3s (idles), but keep camera moves and VFX on 1s — the standard anime mix. Hold key poses 4-8 frames before an attack (anticipation), then 1-2 frames of smear, then the impact. In Blender, the "Stepped Interpolation" F-modifier does this per channel; in Godot, AnimationPlayer tracks support discrete/nearest updates; in pycairo the frame index is simply floored to the step.
- **Rendering on 2s also cuts render cost:** character passes rendered only on unique frames and composited over a per-frame camera pan/background, so EEVEE-on-CPU or laptop time roughly halves [estimate].
- **Impact frame recipe (procedural, any engine):** 1-3 frames of inverted/2-tone (black-white or red-black) image, radial speed lines centered on the contact point, a white flash, then hit-stop of ~3-6 frames at 24 fps on both characters while particles keep moving, then a decaying camera shake (offset noise with exponential falloff over ~8-12 frames). All of this is a screen-space post-process that pycairo/NumPy or a Godot shader can do at negligible cost.
- **Smears:** for 3D, a per-frame shape-key or geometry-nodes stretch along velocity on the 1-2 frames of fastest motion; for 2D, a motion-trail polygon or multiple ghosted copies drawn in cairo. No ready free smear tool was found.
- **Particle VFX:** Effekseer's editor runs on the owner's Windows laptop and exports transparent PNG sequences/sprite sheets that the CPU pipeline can composite; MIT runtime means effects can also be played in Godot. Pixel-art CC0 packs (PVFX) suit a retro look but not HD anime; HD anime slashes/explosions likely have to be drawn procedurally (cairo/Grease Pencil) or made in Effekseer.
- **Camera language:** anime battles rely on held frames + camera moves on 1s (pans across held cels, fast zoom-ins, Dutch angles, cut-ins/split panels). These are cheap 2D transforms on rendered layers; the existing `motion/kit.whip` push-in can be extended with snap-zooms and shake.

### Gaps
- The SciTePress hit-stop study's actual preferred durations were not retrieved.
- No free, commercially licensed, HD (non-pixel) anime VFX sprite library was found.
- Effekseer tool licence text (LICENSE_TOOL) not read; whether exported renders carry any restriction is not stated (runtime is MIT, data CC0).
- Godot GPUParticles vs CPUParticles cost on llvmpipe: no source.
- Blender geometry-nodes VFX recipes for anime (e.g., stylized fire/slash) not researched.

## 4. Lip sync, facial animation, blink/breath automation

### Takeaway
Rhubarb Lip Sync (MIT) is the common denominator: it outputs mouth-shape timings that OpenToonz (built-in since v1.6), Moho, Blender (Rhubarb Lipsync NG add-on, MIT per its store page) and any custom pipeline can consume; LipKit (GPL) adds Grease Pencil-layer support. Blinks and breathing are best generated procedurally (seeded timers and sine/spring drivers), which every candidate tool can do in script.

### Cited Findings
- Rhubarb 1.14.0: MIT, output "belongs to you alone", accepts the script text via `-d`, 9 mouth shapes (A-H + X) as JSON; can write `.dat` switch data read by Moho and OpenToonz — [Rhubarb README](https://github.com/DanielSWolf/rhubarb-lip-sync) [official]
- On this container an 8.57 s narration took 14.4 s in PocketSphinx mode (~1.7x real time, one core) and 1.5 s in phonetic mode — `reports/3D horror Shorts animation and hooks.md` [earlier report, measured here]
- OpenToonz v1.6 added Rhubarb integration for automatic lip-sync — [OpenToonz What's New](https://opentoonz.readthedocs.io/ja/latest/whats_new.html) [official]
- Rhubarb Lipsync NG (Blender, by Premysl Srubar): MIT per the store listing; maps cues to shape keys, armature bones or action sheets; supports Blender 3.3-4.2 per the listing — [Blender Market](https://blendermarket.com/products/rhubarb-lipsync-ng); repo — [GitHub Premik](https://github.com/Premik/blender_rhubarb_lipsync_ng) [official listing]
- LipKit (Blender add-on, GPL) works with Grease Pencil layers and shape keys — [Superhive](https://superhivemarket.com/products/lipkit) [official listing]
- Papagayo-NG has community discussion of a Grease Pencil importer and phoneme holding — [papagayo-ng #49](https://github.com/morevnaproject-org/papagayo-ng/issues/49) [report]
- Procedural idle stack reference (eye contact, head movement, blink, mood breathing): MIT TalkingHead — [TalkingHead](https://github.com/met4citizen/TalkingHead) (via earlier report) [official]

### Inferences
- **Anime mouths are sparse:** anime typically uses 3 mouth states (closed/mid/open) held on 2s-3s, so collapse Rhubarb's 9 shapes into 3-4 drawings and hold each ≥2 frames; this looks more "anime" than western-style full visemes [estimate based on genre convention].
- For Blender 3D characters: shape keys (or GP mouth layers on the face) driven by the Rhubarb JSON through a small `bpy` script; no add-on is strictly required. Rhubarb Lipsync NG's listed Blender support stops at 4.2 — check before relying on it with 4.3+/5.x (GP3 API changed).
- For Godot: an AnimationPlayer track generated from the Rhubarb JSON (frame-swap of mouth textures or blendshape values) — straightforward code generation.
- Blink: seeded random interval 2-6 s, 3-frame close/open, suppressed during stares/shock; breath: 0.2-0.3 Hz chest/shoulder scale; for creatures, add ear/tail secondary motion via damped springs.

### Gaps
- Rhubarb Lipsync NG compatibility with Blender 4.3+/5.x not confirmed; Papagayo-NG licence not retrieved.
- Whether Rhubarb's OpenToonz integration can drive Plastic mesh deformation (vs swapping drawn mouth cells) was not confirmed.
- Inochi2D/Live2D audio-driven lip sync for offline renders was not researched.

## 5. Realistic render speed on the CPU container vs the laptop

### Takeaway
Only a handful of numbers are measured; most per-tool speeds are unknown and must be benchmarked. Measured on the container: pycairo/OpenCV puppet compositing 25-60 ms/frame, Blender Workbench ~2 s/frame, EEVEE via llvmpipe ~8 s (720p-vertical) to ~15 s (1080x1920) per frame, three.js on SwiftShader ~1 fps (llvmpipe reported 2-4x faster elsewhere). No measured laptop (RTX 3050 4 GB) numbers for EEVEE, Godot Movie Maker or Grease Pencil were found.

### Cited Findings
- Container, pycairo/NumPy/OpenCV puppet ops: precomputed `cv2.remap` 2.1 ms; composite of 8 cropped parts 23.5 ms; total character shot ~25-60 ms/frame — `reports/CPU anime animation pipeline.md` [earlier report, measured here (components) / estimate (total)]
- Container, Blender: Workbench ~2 s/frame; EEVEE (llvmpipe/EGL) ~8 s at 720x1280 4 samples, ~15 s at 1080x1920, 37-55 s at 16 samples — `reports/CPU anime animation pipeline.md` [earlier report, measured here, contended]
- Container, three.js: ~1 fps on SwiftShader (80 s episode ≈ 40 min) — `reports/3D horror Shorts animation and hooks.md` [measured here]; Microlink measured a three.js skinning example at ~24 s on SwiftShader vs ~6 s on llvmpipe (8-core nodes) — [Microlink](https://microlink.io/blog/webgl-without-a-gpu) [measured, other hardware]
- Container, Rhubarb: 1.7x real time single core (PocketSphinx) — earlier report [measured here]
- Cycles OIDN denoise ~1.2 s/frame on an i9-13900K (Junkshop) — [Blender 4.1 notes](https://developer.blender.org/docs/release_notes/4.1/cycles/) [official, other hardware]
- Godot Movie Maker: "Faster hardware will allow you to render ... in less time"; setting everything to maximum "can still slow down movie saving speed, especially when recording at higher resolutions" — [Godot docs](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) [official, no numbers]
- Godot under Xvfb with a software renderer: "glitchy", "quite slow" — [godot #38428](https://github.com/godotengine/godot/issues/38428) [report, 2020]

### Inferences
- **Per-40-second Short (960 frames at 24 fps) [estimate, arithmetic on the measured per-frame figures]:**

| Pipeline | Container (4 CPU cores) | Laptop (RTX 3050 4 GB) |
|---|---|---|
| pycairo puppet + procedural VFX | ~0.5-1 min of compute + encode | similar (CPU-bound) |
| three.js toon (current) | ~16 min SwiftShader; ~4-8 min if llvmpipe gains hold | real-time-ish in a GPU browser [unmeasured] |
| Blender Workbench (no toon) | ~32 min | seconds-minutes [unmeasured] |
| Blender EEVEE toon 1080x1920 | ~4 h (every frame) / ~2 h (characters on 2s) | likely ≤1 s/frame → ≤15 min [unmeasured estimate] |
| Godot 2D/3D Movie Maker | unknown; software GL reported slow | likely faster than real time for simple 2D/toon scenes [unmeasured] |
| Spine / Rive / Live2D export | editor GUI only (Spine editor could run on Linux but needs a display) | editor export, minutes [unmeasured] |

- A 12-15 min long episode (16:9) multiplies these by ~20x; EEVEE on the container (≈40-80 h) is impractical, so long episodes need the laptop or a 2D/cairo-heavy look.
- Splitting the job: the container builds scenes (bpy/GDScript/JSON), renders previews in Workbench/low-res, and does all compositing, VFX overlays, captions and encoding; the laptop does final EEVEE/Godot renders overnight.

### Gaps
- Measured EEVEE/Godot/GP render times on the RTX 3050 Laptop 4 GB.
- Godot Compatibility renderer on Mesa llvmpipe under Xvfb in this container (frames/s for a 2D skeleton scene and a toon 3D scene).
- Synfig CLI render speed (no published figures; earlier report also found none).
- Blender 5.x EEVEE on llvmpipe (re-test needed; Blender not installed now).
- Effekseer playback/render cost in Godot on CPU.

## 6. What indie animators actually use, real examples, and which combination fits this channel

### Takeaway
Free-tool anime examples exist mostly in Blender (Khara's Evangelion work with Grease Pencil, Goo Engine shorts like "Samurai Blue: Afterimage", Blender Studio's "Hero") and Godot (Cassette Beasts, a two-person monster tamer with 120 animated monsters). High-profile web series often assumed to be Blender (The Amazing Digital Circus) actually used Maya/Unreal. For this channel, the most credible upgrade over paper-doll puppets is a hybrid: Blender toon 3D (or Godot) for characters and creatures, animated on 2s/3s with drawn-style poses, plus procedural 2D impact/speed-line/shake overlays composited in the existing CPU pipeline.

### Cited Findings
- Khara (Evangelion) moved its 3DCG to Blender, with Grease Pencil central — [blender.org](https://www.blender.org/?p=64752) [official, 2019]
- "Samurai Blue: Afterimage" anime short made in Blender + Goo Engine by Winterstellar Studios — [BlenderNation](https://www.blendernation.com/2024/09/16/anime-short-film-samurai-blue-afterimage/) [report, 2024]
- "Hero" Grease Pencil showcase (Blender Studio, 2018) — [BlenderNation](https://www.blendernation.com/2018/04/16/hero-blender-grease-pencil-showcase/) [official]
- Cassette Beasts (Godot, two full-time staff, 120 monsters, every fusion animated) — [Wikipedia](https://en.wikipedia.org/wiki/Cassette_Beasts); [Wireframe](https://wireframe.raspberrypi.com/articles/creature-collecting-gets-an-analogue-upgrade-in-cassette-beasts) [press]
- Guilty Gear Xrd: 3D that won a CEDEC visual-arts award for looking like 2D animation, via limited animation — [Inside Games (ja)](https://www.inside-games.jp/article/2017/04/28/106868_4.html); [Kotaku](https://kotaku.com/breaking-down-the-animation-of-guilty-gear-and-dragonba-1836849279) [press]
- The Amazing Digital Circus character pipeline used Maya and Unreal Engine — [80.lv](https://80.lv/articles/glitch-on-character-animations-in-the-amazing-digital-circus) [press]
- Spine runtime friction in Godot and Skeleton2D frustration (indie dev reports) — [Godot forum](https://forum.godotengine.org/t/state-of-skeleton2d-in-godot-bone-2d-rigging-cutout-animations/65393) [report]
- The owner rejected the SD1.5-painted puppet look ("Worst animation"); cairo toon and voiced-manga slideshow did not perform — assignment brief (Local)

### Inferences
**Pipeline comparison [estimate; ratings are judgement grounded in sections 1-5]**

| Pipeline | Motion quality ceiling | Creatures (quadruped / flying / serpent / blob) | Battle VFX | Claude can author in code? | Container render | Laptop render | Cost / licence | Main risk |
|---|---|---|---|---|---|---|---|---|
| **A. Blender toon 3D + GP3 lines/FX, stepped 2s/3s** | High (Xrd/Khara-style) | Yes: Quaternius CC0 monsters, Rigify Wolf/Horse/Cat/Shark, shape-key blobs, spline-IK serpents | GP strokes, geometry nodes, composited 2D overlays | Yes (`bpy`, GP3 Python API) | EEVEE ~15 s/frame (preview/short shots only) | Primary renderer; 4 GB VRAM limits textures/res | Free, GPL; assets CC0/Quaternius licence | Modelling original cast takes weeks; toy-asset look if not restyled; 4 GB VRAM crashes |
| **B. Godot 2D/3D scenes + Movie Maker** | Medium-high (3D toon + procedural creatures); 2D rigs medium | Strong procedural IK examples (spider), particles | GPUParticles + CC0 shaders + Effekseer (MIT) | Yes (`.tscn` text + GDScript) | Untested (Xvfb + llvmpipe) | Good (untested numbers) | Free, MIT | 2D skeleton tooling weak; CPU path unproven |
| **C. Spine Professional cut-out + mesh** | Medium-high 2D (perspective turns via meshes) | Good for 2D creatures with meshes + IK (Pro) | Sprite/particle overlays | Partly (JSON writable, editor needed for meshes) | Editor needs display | Editor export | US$369-379 one-time (sale), per person | Still "puppet" unless drawn swaps + smears; paid |
| **D. Current pycairo puppet + timing/VFX upgrade** | Medium | Weak for quadrupeds; OK for blobs/serpents (procedural curves) | Procedural impact frames, speed lines, shake: cheap | Yes | 25-60 ms/frame | n/a | Free | Already rejected look; upgrade may not overcome it |
| **E. Live2D FREE / Inochi2D for dialogue close-ups** | High for talking heads only | No | No | No (GUI rigging) | No headless | GUI export | Live2D FREE OK under ¥10M sales; Inochi2D BSD-2 | Narrow motion range; hours of manual rigging |
| **F. Rive** | Medium-high 2D (meshes, state machines) | 2D only | Limited | No (binary, editor) | Unclear | Cloud export (paid) | Cadet $9/mo to remove splash/watermark | Paid export; no proven offline video path |

- **Recommended combination [estimate]:** A as the main pipeline (laptop renders; container authors scenes and does all 2D compositing/VFX/captions), B as a test candidate for creature-heavy battle scenes if a llvmpipe Movie Maker benchmark proves usable, and E only if close-up dialogue needs more face acting than 3D shape keys provide. Spend first on timing (stepped 2s/3s, anticipation, hit-stop, impact frames) since it is free and is the documented difference between "anime 3D" and "game cutscene 3D" (Xrd).
- **Format fit:** Shorts (9:16) favour close/medium shots with 1-2 characters and one battle beat — feasible even on the container at ~2 h/Short with characters on 2s; long 16:9 episodes realistically need laptop renders or heavy reuse (held cels, pans, cut-ins).
- **First benchmarks to run before committing [estimate]:** (1) laptop: one Quaternius monster, toon material + outline, 1080x1920, 48 frames, EEVEE timing and VRAM peak; (2) container: same `.blend` via llvmpipe on Blender 5.x; (3) container: Godot 4.7 Compatibility renderer + Movie Maker under Xvfb/llvmpipe with a Skeleton2D creature and a CC0 speed-line shader.

### Gaps
- No verified list of YouTube anime series (frequent uploads) made with Blender/Grease Pencil and their per-episode turnaround; Lightning Boy Studio's anime workflow was not found (only a Ghibli-tree tutorial — [Digital Production](https://www.digitalproduction.com/2020/09/04/ghibli-style-in-3d-blender/)).
- No public render-time devlogs for indie anime made in Godot or Blender on 4 GB laptop GPUs.
- Cassette Beasts' monster-animation technique (sprite frames vs skeletal) was not documented in the sources found.
