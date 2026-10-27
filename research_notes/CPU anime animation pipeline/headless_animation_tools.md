# Headless, scriptable open-source animation tools for anime-style footage on a CPU-only Linux server

Scope: tools that can be driven entirely by scripts (no GUI) on this machine (4 vCPU, ~15 GB RAM, ~4-8 GB free disk that
fluctuates as other jobs write, no GPU, Ubuntu 24.04.5, Mesa 25.2.8 llvmpipe present), compared with the current approach
(Python + pycairo vector drawing, 720x1280 / 1280x720, 30 fps).

How to read this file:
- **[web]** = claim taken from the linked page.
- **[local test]** = measured by me in this container on 27 Oct 2026 (Blender 5.2.0 LTS, test scripts and output images in
  `/tmp/claude-0/-home-user-Motion-graphics/ce9fa840-85fb-5cb2-9994-edff6b8c5245/scratchpad/bltest/`: `scene.py`, `anim2.py`, `anim3.py`, `compare.png`,
  `compare2.png`, `aa_compare.png`, final frames `b_*_0004.png`, `c_*_0004.png`). **All local timings were taken while other
  agents' benchmarks and a TTS job were using 1.3-3.4 of the 4 cores (load average 4-10)**, so they are pessimistic upper
  bounds, not clean numbers. Re-time on an idle machine before planning a schedule.
- **[estimate]** = my own arithmetic or judgement, not measured and not sourced.

Context for the coordinator: during the test I installed two small system packages, `libegl1` and `libegl-mesa0`
(Mesa 25.2.8), with apt, because Blender's headless GL path needs `libEGL.so.1`. The Blender download (1.2 GB extracted)
was deleted afterwards. Free disk at the end was 7.4 GB.

---

## 1. Blender: headless rendering, CPU-usable engines, toon/anime look, Grease Pencil v3, Line Art, Freestyle, speed, size

### Takeaway
Blender is fully scriptable headless (`blender -b --factory-startup -P script.py -- args`), and **EEVEE does render on a
GPU-less Linux box through Mesa llvmpipe over EGL**. I verified this with Blender 5.2.0 LTS here once `libegl1` + `libegl-mesa0`
were installed. It gives the cleanest anime cel look (Shader to RGB, colour ramp set to Constant, inverted-hull or Grease
Pencil Line Art outlines), but it is slow on 4 CPU cores. Under contention a simple character frame took **about 8 s at 720x1280 with 4 AA
samples, about 15 s at 1080x1920 with 4 samples, and 37-55 s at 1080x1920 with 16 samples**. Workbench is about 2 s per frame but can't do proper
toon materials. Cycles CPU runs without any GL at all, but Shader to RGB is EEVEE-only, so its toon look is weaker and the outline tricks need extra work.

### Cited Findings

**Headless invocation**
- The official background-job template runs Blender in background mode with a script; arguments after `--` are ignored
  by Blender and passed to the script ("'--' causes blender to ignore all following arguments so python can use them") —
  [web] [Blender background_job.py template](https://projects.blender.org/archive/blender-archive/raw/commit/13ae75f545c5087bc6dbe44a64763e17ad65a44c/scripts/templates_py/background_job.py)
- `-b/--background` runs Blender without UI; `-P/--python <file>` runs a script; arguments execute in order, so output
  settings must come before `-f`/`-a` render flags — [web] [Blender 2.80 manual, command-line arguments](https://docs.blender.org/manual/en/2.80/advanced/command_line/arguments.html); [Blender 2.79 manual](https://docs.blender.org/manual/ja/2.79/advanced/command_line/arguments.html) (older manual versions; the same flags worked unchanged in 5.2.0 in my test).
- [local test] `blender -b --factory-startup -P scene.py -- ENGINE out.png` built a scene from nothing in Python
  (`read_factory_settings(use_empty=True)`, primitives, materials, sun, camera, world colour) and rendered it with each
  engine. Blender 5.2 prints DeprecationWarnings that `Material.use_nodes` / `World.use_nodes` "is expected to be removed in
  Blender 6.0", so scripts should avoid that property.

**Can EEVEE run without a GPU?**
- Official 2.80 notes: "Eevee only uses the power of the GPU to render. There are no plans to support CPU (software)
  rendering" and headless systems were "not supported currently" (2019, dated) — [web] [Blender 2.80 EEVEE release notes](https://developer.blender.org/docs/release_notes/2.80/eevee/)
- A teaching course says "Cycles can render both on CPU and GPU, whereas EEVEE can only render on a GPU (more specifically, it
  needs OpenGL)" and that EEVEE headless rendering is supported "only Linux since 3.4" — [web] [SURF Blender course, GPU rendering](https://surf-visualization.github.io/blender-course/basics/rendering_lighting_materials/gpu_rendering/)
- Commit 3195a381200 (Sebastian Parborg, 15 Aug 2022): "With this patch true headless OpenGL rendering is now possible on
  Linux"; "Blender will try to fall back to it if it fails to initialize other backends while in background mode"; the
  headless backend is "now always available with regular builds"; Linux-only because EGL is not used on Mac/Windows; the
  diff uses the `EGL_MESA_platform_surfaceless` extension — [web] [bf-blender-cvs commit mail](https://archive.blender.org/lists/bf-blender-cvs/2022-August/176810.html)
- Current requirements (page covers up to Blender 5.0+): Linux minimum 4 cores with SSE4.2, 8 GB RAM, GPU with 2 GB VRAM,
  OpenGL 4.3 with GL_ARB_shader_draw_parameters and GL_ARB_clip_control, Vulkan 1.3. No statement about software or
  headless rendering — [web] [blender.org requirements](https://www.blender.org/download/requirements/)
- A CI project got Blender's EEVEE renders working on a **Windows** runner with no GPU driver by copying Mesa llvmpipe
  26.2.3 GL DLLs next to blender.exe and setting `GALLIUM_DRIVER=llvmpipe` ("EEVEE needs OpenGL 4.3; the Windows runner has
  no GPU driver"). It reports CI green, with one Blender crash on a first attempt, and no render times — [web] [BuildersGate PR #85](https://github.com/Thepizzapie/BuildersGate/pull/85)
- **Contradicting claim:** a render-farm vendor article says EEVEE-Next (4.2+) "cannot be executed as an abstracted
  command-line binary on headless cloud instances" and outputs black frames. It is marketing with no method, and my local
  test below contradicts it for Linux + Mesa EGL — [web] [iRender article](https://irendering.net/eevee-next-headless-dilemma-cloud-render-farm-guide/)
- **[local test] verified:** Blender 5.2.0 LTS (build date 2026-07-14), `-b` with `BLENDER_EEVEE`:
  - Without libEGL installed it fails: `Couldn't open libEGL.so.1: libEGL.so.1: cannot open shared object file`.
  - After `apt-get install libegl1 libegl-mesa0` (Mesa 25.2.8, llvmpipe already present via `mesa-libgallium`), it rendered
    correct cel-shaded frames with no X server, Xvfb or GPU. It prints repeated harmless-looking
    `EGL Error (0x3009): EGL_BAD_MATCH` lines and then saves the image.
  - The Blender 5.2 Linux tarball ships **no bundled Mesa** (`lib/` has no `mesa` folder and there is no
    `blender-softwaregl` launcher), so the system Mesa EGL is what makes it work. Older tarballs shipped
    `blender-softwaregl` with Mesa in `lib/mesa` ([web] [Arch bug FS#52980](https://bugs.archlinux.org/task/52980);
    [2022 commit moving Mesa to lib/mesa](https://lists.blender.org/pipermail/bf-blender-cvs/2022-July/175521.html)); that
    launcher was reported to segfault on several builds ([web] [Blender T56315](https://developer.blender.org/T56315)).
- EEVEE shader compilation became much slower in 4.2/4.3 after the EEVEE rewrite ("Compiling EEVEE engine shaders is
  REALLY slow in version 4.2 and 4.3") — [web] [Blender issue #127812](https://projects.blender.org/blender/blender/issues/127812).
  On llvmpipe this cost lands on the CPU too, so the first frame of each run is slower.
- Blender 4.5 LTS made the Vulkan backend stable, but OpenGL stays the default; Vulkan on Linux needs NVIDIA 550+ or Mesa
  25.3+ for AMD — [web] (search summary of) [Phoronix, Blender 4.5 LTS](https://www.phoronix.com/news/Blender-4.5-LTS-Released) and [9to5Linux](https://9to5linux.com/blender-4-5-lts-open-source-3d-graphics-app-makes-the-vulkan-backend-stable). I did not test Vulkan (lavapipe) here.

**Engines and the toon look**
- Shader to RGB (the node behind most anime cel setups: diffuse, then Shader to RGB, then a colour ramp set to Constant) is **EEVEE only** — [web]
  [Blender manual, Shader To RGB](https://www.blender.org/manual/de/render/shader_nodes/converter/shader_to_rgb.html);
  [Blender bug T77177](https://developer.blender.org/T77177) ("only available for Eevee, not for Cycles").
- In Cycles the alternatives are the built-in Toon BSDF (forum users call it "not actually a toon shader"), light-linking
  tricks since 4.0, or paid add-ons such as Cyclotoon; a vendor FAQ says EEVEE "makes a great default for any toon rendered
  project" and Cycles toon shows "some soft shading" — [web] [GameDev.tv thread](https://community.gamedev.tv/t/shader-to-rgb-alternative-for-cycles/236416); [Cyclotoon listing](https://superhivemarket.com/products/cyclotoon); [Advanced Toon Shader FAQ](https://superhivemarket.com/products/advanced-toon-shader/faq)
- New EEVEE material-lighting nodes (Light Info, Light Evaluation, Shadow Raycast, Light Accumulation, a Light mode on the
  Attribute node) were posted for feedback on 19 Aug 2026, "targeting the next (5.3) release". They are EEVEE only; Cycles is "Maybe, but
  it's not planned for now"; they resemble the "For Each Light" zone of the NPR prototype — [web] [devtalk: Material Lighting Nodes feedback](https://devtalk.blender.org/t/material-lighting-nodes-feedback/45695)
- The Blender Foundation released an experimental NPR prototype build in Dec 2024 with DillonGoo Studios — [web] [CG Channel, Dec 2024](https://www.cgchannel.com/2024/12/check-out-blenders-experimental-non-photorealistic-rendering-build/)
- Goo Engine is DillonGoo Studios' Blender fork for anime/NPR. The source is GPL, but compiled binaries are Patreon-only;
  you can compile it free with the same requirements as Blender — [web] [CG Channel, Jul 2023](https://www.cgchannel.com/2023/07/check-out-goo-engine-blender-for-anime); [GameFromScratch](https://gamefromscratch.com/goo-engine-blender-for-anime/)
- [local test] With a cel material (Diffuse, then Shader to RGB, then a two-stop Constant ramp, then Emission) and inverted-hull outlines
  (Solidify modifier with flipped normals, black emission material with backface culling), EEVEE produced a clean, flat anime-like
  look (`compare2.png`, first panel). Two script-level gotchas showed up:
  - The default view transform (AgX) washed the flat colours out (`compare.png`, first panel); setting
    `scene.view_settings.view_transform = "Standard"` fixed it (`compare2.png`).
  - In **Cycles** the inverted hull covered the whole character in black, because backface culling is not honoured by Cycles
    (`compare.png`, third panel). A Backfacing-to-Transparent mix still left the character dark (`compare2.png`, third
    panel), probably because the hull casts shadows. Cycles needs the hull's shadow visibility turned off or a camera-ray-only
    shader. I didn't fix this.
  - Cycles Toon BSDF + Freestyle produced a soft, glossy-looking result, not flat cel shading, and my scripted Freestyle line
    set produced **no strokes** ("Error: strokes set empty"). Line-set setup from an empty factory scene needs more work
    (`compare2.png`, fourth panel).

**Grease Pencil v3 and Line Art**
- Since 4.3, Grease Pencil Python add-ons written before 4.3 "are expected to break". The object type is GREASEPENCIL, the data type
  GreasePencilv3, GP modifiers are regular modifiers, Line Art is type `LINEART`, and operators moved to
  `bpy.ops.grease_pencil.*` — [web] [4.3 Grease Pencil migration notes](https://developer.blender.org/docs/release_notes/4.3/grease_pencil_migration/); [API: GreasePencilLineartModifier (4.3)](https://docs.blender.org/api/4.3/bpy.types.GreasePencilLineartModifier.html)
- Grease Pencil is drawn with OpenGL even when the scene renders with Cycles. Blender developer Jeroen Bakker: "Yes, that is correct
  Grease Pencil is drawn using OpenGL ... OpenGL support is needed ... via GPU+driver or software emulation". A hidden GP object
  was enough to make a no-GPU farm fail — [web] [devtalk thread, Oct-Nov 2019](https://devtalk.blender.org/t/rendering-grease-pencil-objects-on-headless-no-gpu-render-farm-machines-in-blender-2-8/10194)
- Older background-mode GP bugs: some GP frames skipped in background mode ([web] [T85035](https://developer.blender.org/T85035));
  Line Art missing in renders above 2048x2048 ([web] [T94169](https://developer.blender.org/T94169)). These are 2.9x/3.x-era
  reports; I didn't check whether they are fixed.
- [local test] `bpy.ops.object.grease_pencil_add(type="LINEART_SCENE")` in background mode created a `GREASEPENCIL` object
  with a `LINEART` modifier, and EEVEE (llvmpipe) rendered the Line Art outlines at 1080x1920 (`compare2.png`, second panel).
  The default line was thin, so thickness needs tuning.

**Freestyle**
- The 2023 Line Art design plan states the end goal "to replace freestyle and the existing line art modifier with a
  node-based Line Art design" (a plan, not a shipped change) — [web] [devtalk 2023-10-30 Line Art meeting](https://devtalk.blender.org/t/2023-10-30-line-art/31809)
- Report that Freestyle lines become invisible above a certain resolution in complex scenes — [web] [issue #118310](https://projects.blender.org/blender/blender/issues/118310)

**Install size**
- [local test] `blender-5.2.0-linux-x64.tar.xz` is 384,441,228 bytes (HTTP content-length from download.blender.org); it
  downloaded in 28 s and extracted in 32 s to **1.2 GB**.
- Blender 5.0.0 / 5.0.1 Linux archives: 369.8 MiB / 356.8 MiB — [web] [NLUUG mirror, Blender5.0](https://ftp.nl.freebsd.org/ftp/graphics/blender/release/Blender5.0)
- Alpine Linux packages a `blender-headless` build — [web] [Alpine package page](https://pkgs.alpinelinux.org/package/v3.21/community/x86_64/blender-headless) (title only; contents not checked).

**[local test] Timings.** Scene: five primitive meshes (48-segment spheres and cylinder: head, hair, body, two eyes), one
sun, flat sky colour, 4-frame animation (body rotates), **1080x1920 unless noted**, Blender 5.2.0, 4 vCPU. Contention noted per run.

| Run (UTC, contention) | Engine / setup | Seconds per frame (frames 1-4) |
|---|---|---|
| 21:30-21:31, other agents' benchmarks ~340% CPU + TTS 45% | Workbench (default studio lighting, no toon) | 2.25, 2.25, 2.11, 2.12 |
| 21:31-21:32, bench ~138% + 92% + TTS 43% | Cycles CPU, 16 spp, Toon BSDF + transparent-backface hull | 21.5, 17.7, 19.0, 19.5 |
| 21:32-21:35, upscaler bench ~164% + TTS | EEVEE (llvmpipe), 16 AA samples, Shader to RGB + inverted hull | 41.6, 55.0, 45.3, 36.7 |
| 21:35-21:37, ESRGAN bench ~186% | EEVEE, 16 samples, GP Line Art outlines (no hull) | 28.5, 35.4, 33.9, 30.9 |
| 21:37-21:38, load ~6-7 | Cycles CPU, 16 spp, Toon BSDF, Freestyle on (0 strokes made), no hull | 7.9, 7.8, 7.6, 7.4 |
| 21:38-21:39, TTS ~133% | EEVEE, **720x1280, 4 samples**, hull | 7.1, 8.2, 8.3, 8.1 |
| 21:39-21:40, TTS ~192% | EEVEE, 720x1280, 16 samples, hull | 18.6, 25.8, 26.5, 29.6 |
| 21:40-21:41, TTS ~190% + bench ~122% | EEVEE, 1080x1920, 4 samples, hull | 14.0, 15.0, 14.5, 15.6 |
| 21:24-21:29 (earlier run, TTS ~1 core + other benches) | Cycles 16 spp, opaque hull (wrong look) / Workbench / EEVEE 16 samples | 6.1-7.5 / 2.1-3.0 / 33-55 |

- [local test] At 720x1280, 4 vs 16 EEVEE AA samples looked practically identical on flat cel colours and outline edges
  (`aa_compare.png`), so low sample counts are fine for this style.

### Inferences
- [estimate] One 40 s Short = 1,200 frames at 30 fps. At the contended rates measured: EEVEE 720x1280 / 4 samples ≈ 8 s/frame,
  about **2.7 h per Short**; 1080x1920 / 4 samples ≈ 15 s, about 5 h; Workbench ≈ 2 s, about 40 min. On an idle machine I'd expect
  these to drop by a noticeable but unmeasured amount (perhaps a third to a half, since 1.3-3.4 of 4 cores were busy). Animating on twos
  or threes (12 or 8 drawings per second, normal in anime) would cut render time by 2-3x with no visible loss of style.
- [estimate] Real character scenes (rigged anime mesh of 20-60k triangles, hair cards, a background) will cost more per
  frame than this 5-primitive test. Rendering the character layer in Blender and doing backgrounds and text in the 2D pipeline
  (pycairo/skia, or a pre-rendered still) keeps per-frame cost near the measured numbers.
- Workbench supports flat and matcap lighting plus an object outline option. A two-tone "toon matcap" in Workbench could give
  a cheap cel look at about 2 s/frame. This is an idea to test, with no source or measurement.
- Cycles is the only engine here that needs no GL at all. For anime cel look EEVEE is better, and it now works headless here, so
  Cycles has little advantage on this box beyond robustness.
- Grease Pencil (2D drawing inside Blender, Line Art) needs the same EGL/llvmpipe path as EEVEE, which now works here.

### Gaps
- No clean, uncontended timings (the machine was shared during every run); no timing with a real rigged anime character
  (VRM/MMD model) or with background sets; peak RAM per render not recorded.
- Freestyle line-set scripting from an empty scene failed (no strokes); I didn't find the cause.
- Vulkan backend with Mesa lavapipe (software Vulkan) not tested.
- Whether the old Grease Pencil background-mode bugs (T85035, T94169) still exist in 5.2 not checked.
- No published benchmark of EEVEE on llvmpipe was found online; the numbers above are the only ones I have.

---

## 2. Synfig Studio CLI

### Takeaway
Synfig has a real headless command-line renderer (`synfig file.sifz -t png -o out.png ...`). Its files are XML (`.sif`, or gzipped
`.sifz`) that a script can generate, and it has bones (Skeleton and Skeleton Deformation layers). The open anime-style
"Morevna" project used it with a CLI render manager. I found no performance benchmark, and its look is cut-out/vector
animation, which is close to what pycairo already does.

### Cited Findings
- Usage `synfig [DEFAULT OPTIONS] ([SIF FILE] [SPECIFIC OPTIONS])...` (man page for synfig 1.5.1) — [web] [Ubuntu manpage synfig(1)](https://manpages.ubuntu.com/manpages/lunar/man1/synfig.1.html)
- Options: `-T` threads for the multithreaded renderer, `-b` print benchmarks, `-Q` quality 0-10 (default 2), `-a`
  antialias 1-30 (parametric renderer), `-o` output file, `-w`/`-h` size, `-t` target type, `-v`/`-q` verbosity,
  `--time` single frame, `--begin-time`/`--end-time`, `--fps`, `-c` canvas ID — [web] [manpages.org synfig](https://manpages.org/synfig); [man.cx synfig(1)](https://man.cx/synfig(1)); [hexmos synfig man page](https://hexmos.com/freedevtools/man-pages/user-commands/compilers-and-assemblers/synfig/) (some of these pages are based on old builds; check `synfig --help`).
- Bones: "There are two types of layers in Synfig that are built with bones: Skeleton Layer and Skeleton Deformation
  Layer"; Skeleton Deformation is pixel-level raster deformation with settable distortion area and mesh resolution — [web] [Synfig docs: Skeleton Deformation layer](https://synfig.readthedocs.io/en/latest/layers/skeleton_deformation.html)
- 1.5.0 added a Skeleton Tool, a Python plugin system for import/export, and >3x faster Perspective layer in preview/draft — [web] [Synfig 1.5.0 release notes](https://synfig.readthedocs.io/en/latest/releases/development/1.5.0.html); [Skeleton tool docs](https://synfig.readthedocs.io/en/latest/tools/skeleton.html)
- Lottie export exists; region/outline layers are exported frame-by-frame; bone export to Lottie was "not implemented yet" (page may be dated) — [web] [Synfig: Export for Web (Lottie)](https://synfig.readthedocs.io/en/latest/export/export_for_web_lottie.html); [dev docs, lottie](https://synfig-docs-dev.readthedocs.io/en/latest/projects/lottie-export-for-web.html)
- RenderChan (Morevna Project) is an open-source CLI "smart rendering manager" that renders a file plus its dependencies
  (Blender, Synfig, Krita, Pencil2D, Inkscape, GIMP), e.g. `renderchan ~/morevna-ep3/001/001.sifz`, and re-renders only changed inputs — [web] [RenderChan page](https://morevnaproject.org/renderchan/); [RenderChan tutorial (GitHub wiki)](https://github.com/morevnaproject/RenderChan/wiki/Tutorial); [Morevna ep.4 sources](https://morevnaproject.org/2020/05/23/how-to-work-with-sources-of-morevna-episode-4/)

### Inferences
- Synfig would mainly be a different file format for the same kind of vector cut-out animation the pycairo engine already
  makes. Its gains would be bones with mesh deformation and an artist GUI for building rigs, which are then rendered headless. Generating
  `.sif` XML from Python is possible in principle but adds a format to learn with no evident quality gain for anime faces.
- RenderChan is a useful pattern (dependency-aware re-rendering) even if the tools aren't adopted.

### Gaps
- No render-speed benchmark for Synfig (with or without bones) found; the `.sif` format reference page wasn't retrieved
  (the readthedocs CLI page URL I tried returned 404).
- Not checked whether Ubuntu 24.04's synfig package is 1.4.x or 1.5.x.

---

## 3. OpenToonz / Tahoma2D command-line rendering (tcomposer)

### Takeaway
OpenToonz (and its fork Tahoma2D) ships a CLI renderer `tcomposer` that renders an existing scene file with range, step,
shrink and thread options. It always creates a Qt `QApplication`, so headless use probably needs `QT_QPA_PLATFORM=offscreen`
(untested). There's no documented way to *generate* scenes by script beyond the in-app Toonz Script console, so it suits
rendering artist-made scenes, not procedural ones.

### Cited Findings
- OpenToonz CLI tools: "tcleanup", "tcomposer", "tconverter", "tfarmcontroller", "tfarmserver"; AppImage builds expose them
  via `--appimage-exec`; only tconverter's syntax is documented there (2016 article) — [web] [Morevna: How to use OpenToonz CLI](https://morevnaproject.org/2016/11/27/use-opentoonz-cli)
- tcomposer arguments from source: source scene file, `-o dstName`, `-step n`, `-shrink n`, `-multimedia n`, `-farm`,
  `-id`, `-nthreads single|half|all|n`, `-maxtilesize none|large|medium|small|n`, a frame-range qualifier, and
  `-TOONZROOT folderpath`. It calls `QApplication app(argc, argv);` unconditionally; there's no OpenGL or X11 code in that
  file — [web] [opentoonz tcomposer.cpp (master)](https://raw.githubusercontent.com/opentoonz/opentoonz/master/toonz/sources/tcomposer/tcomposer.cpp)
- The tcomposer binary ships in standard packaging (snap) — [web] [opentoonz-morevna snapcraft.yaml](https://github.com/snapcrafters/opentoonz-morevna/blob/master/snap/snapcraft.yaml)
- OpenToonz has a "Toonz Script" page in its docs — [web] [OpenToonz docs: toonzscript (JA)](https://opentoonz.readthedocs.io/ja/latest/toonzscript.html) (search result only, not read).
- Tahoma2D documents its changes relative to OpenToonz — [web] [Tahoma2D What's New](https://Tahoma2D.readthedocs.io/en/latest/whats_new.html); no tcomposer docs found there.

### Inferences
- `QT_QPA_PLATFORM=offscreen` is the standard way to run Qt apps without a display (e.g. used for headless PhantomJS in
  [web] [OSM rails-dev, 2020](https://lists.openstreetmap.org/pipermail/rails-dev/2020-March/018227.html)), so tcomposer
  probably runs headless with it, but this is unverified.
- OpenToonz's strengths (hand-drawn raster/vector levels, xsheet timing, effects) only pay off when a human draws the
  frames; for script-generated footage it adds little.

### Gaps
- No source confirms tcomposer working without X; not tested here. No render-speed data. Tahoma2D-specific tcomposer
  differences unknown.

---

## 4. Krita scripting and `krita --export` / `--export-sequence`

### Takeaway
Krita can batch-export an existing animated `.kra` to a PNG sequence from the command line (`--export-sequence`, since 4.2),
and it has an in-app Python API. Headless use (no display) isn't documented. It's a painting tool, so it fits making
backgrounds or hand-painted assets, not generating motion automatically.

### Cited Findings
- `krita file.png --export --export-filename final.jpg`; `krita --export-sequence --export-filename file.png test.kra`
  ("Export animation to the given filename and exit", added in 4.2); `--nosplash`; `--export-pdf` was removed in 3.1. The
  page doesn't say whether a display is needed — [web] [Krita manual: Linux Command Line](https://docs.krita.org/en/reference_manual/linux_command_line.html)
- If the file has no animation, `--export-sequence` prints "This file has no animation." and does nothing; format comes from
  the extension — [web] [Krita feature request bug 364046](https://bugs.kde.org/show_bug.cgi?id=364046); [Phabricator D19706](https://phabricator.kde.org/D19706)
- The Python API has gaps, e.g. the Storyboard docker has no direct Python access — [web] [Krita Artists thread](https://krita-artists.org/t/accessing-exporting-storyboard-data/79128)

### Inferences
- [estimate] Krita is mainly useful as a hand-painting tool for backgrounds and overlays that the code pipeline then composites.
  Driving its animation timeline from Python is possible but clumsy compared with drawing directly in pycairo/skia.

### Gaps
- No source confirms `QT_QPA_PLATFORM=offscreen krita --export-sequence ...` works on a display-less server. Not tested.
  AppImage/package size not found.

---

## 5. Code-first options: manim, MoviePy, Cairo vs Skia (skia-python), OpenCV, pyrender

### Takeaway
For pure 2D, the current pycairo approach is already the lightest headless option. **skia-python** is a drop-in-style
alternative (BSD-3, pip wheels for Python 3.8-3.13) worth benchmarking for anti-aliasing quality. manim's default renderer is
Cairo on the CPU, so it brings nothing new for anime. MoviePy is slower than piping raw frames to ffmpeg. pyrender needs
EGL or OSMesa; OSMesa appears to have been dropped from recent Mesa, so use EGL with llvmpipe, as Blender does here.

### Cited Findings
- skia-python: `pip install skia-python`, binary wheels for CPython 3.8-3.13; on Linux it needs system libraries "such as
  fontconfig and Mesa GL"; License BSD-3-Clause; Skia itself is BSD — [web] [PyPI skia-python](https://pypi.org/project/skia-python/); [GitHub kyamagu/skia-python docs link via PyPI](https://pypi.org/project/skia-python/)
- Cairo's own perf suite once measured stroke as "5x slower than fill for the xlib backend and 16x slower for the image
  backend" for 1-px outlines (old Cairo, historical) — [web] [cairo perf box-outline](https://opensource.apple.com/source/X11libs/X11libs-40.3/cairo/cairo-1.8.6/perf/box-outline.c.auto.html)
- No direct skia-python vs pycairo benchmark was found (search returned none).
- manim Community: Cairo renderer is CPU-based and the default; the OpenGL renderer needs GL; line orientation differs between
  them — [web] [manim RendererType docs](https://docs.manim.community/en/stable/reference/manim.constants.RendererType.html); [manim issue #4341](https://github.com/manimcommunity/manim/issues/4341); [FlyingFrames ch.8 (OpenGL timing example)](https://flyingframes.readthedocs.io/en/stable/ch8.html)
- MoviePy works on frames as numpy arrays, which makes it slower than raw ffmpeg. A competing library's own benchmark (MoviePy 2.2.1,
  1280x720 30 fps) claims 3.1-4.5x speedups, e.g. text overlay 35.35 s vs 7.82 s (vendor-run, hardware unspecified) — [web] [MovieLite performance benchmarks](https://www.mintlify.com/francozanardi/movielite/resources/performance-benchmarks); [MoviePy GitHub](https://github.com/Zulko/moviepy)
- pyrender headless: set `PYOPENGL_PLATFORM=egl` or `osmesa` before importing; EGL is "the first (and preferred)" option,
  OSMesa is the CPU-only software fallback and needs a Mesa built with OSMesa plus a patched PyOpenGL — [web] [pyrender offscreen docs](https://pyrender.readthedocs.io/en/latest/examples/offscreen.html); [pyrender install guide](https://pyrender.readthedocs.io/en/latest/install/)
- A June 2025 Yocto patch drops the OSMesa option from mesa-demos because "support for OSMesa has been removed in the latest
  Mesa versions" — [web] [Yocto patchwork comment](https://patchwork.yoctoproject.org/comment/28371) (exact Mesa release not confirmed).
- [local test] This container has Mesa 25.2.8 (`mesa-libgallium`, `libgl1-mesa-dri`, `libglx-mesa0`) and, after my install,
  `libegl1` + `libegl-mesa0`; there's no `libOSMesa` in `/usr/lib/x86_64-linux-gnu`. pycairo is listed in
  `requirements.txt` but wasn't importable from the system Python 3.11/3.12/3.13 at the time of checking (it presumably
  lives in a project venv such as `/home/user/.venv-main`).

### Inferences
- Neither Cairo nor Skia has a native "variable-width stroke" primitive as far as I know (no source checked). Anime-style
  tapered ink lines are made by building the outline polygon of the stroke (offset curves along the normal with a width
  profile) and filling it. That works the same in pycairo and skia, so the quality question is mostly anti-aliasing and speed.
- OpenCV is useful for compositing and post effects (blur, glow, colour LUTs) on numpy frames, but adds nothing for drawing
  anime lines. No sources were gathered on it.
- For any GL-based Python renderer (pyrender, moderngl, AnimatedDrawings) on this box, use EGL with Mesa llvmpipe
  (`PYOPENGL_PLATFORM=egl`), the same stack I verified with Blender, instead of OSMesa.

### Gaps
- No measured pycairo vs skia-python speed or quality comparison on this machine; no measured per-frame cost of the current
  pycairo engine to compare with Blender's numbers.
- Colour-emoji rendering in pycairo vs skia not checked.

---

## 6. Existing open-source, script-driven anime-style projects and pipelines

### Takeaway
There is no ready-made "script in, anime episode out" open-source pipeline. The closest building blocks are Blender plus
anime-model importers (VRM add-on, mmd_tools) with EEVEE toon shading, Goo Engine (GPL fork, free if self-compiled), Meta's
AnimatedDrawings (MIT, headless Mesa view), Inochi2D (BSD-2 Live2D-style puppets, no official headless CLI), and Morevna's
Synfig + Blender + RenderChan workflow.

### Cited Findings
- VRM Add-on for Blender is listed on Blender Extensions under MIT and GPL-3.0-or-later; mmd_tools (maintained repo) is
  GPLv3 — [web] [Blender Extensions: VRM](https://extensions.blender.org/add-ons/vrm); [MMD-Blender/blender_mmd_tools](https://github.com/MMD-Blender/blender_mmd_tools)
- Goo Engine (GPL source, paid binaries) and the official NPR prototype: see section 1 — [web] [CG Channel](https://www.cgchannel.com/2023/07/check-out-goo-engine-blender-for-anime)
- AnimatedDrawings' `mesa_view.py` (Meta, "licensed under the MIT license") sets `PYOPENGL_PLATFORM=osmesa` and creates a
  "Mesa View for Headless Rendering" — [web] [mirror of animated_drawings/view/mesa_view.py](https://huggingface.co/spaces/gauravyad86/nanee-animation/blob/main/animated_drawings/view/mesa_view.py) (mirror, not upstream; upstream LICENSE not checked)
- Inochi2D: "open source, BSD 2-clause licensed toolkit and ecosystem for real-time 2D puppet animation" — [web] [NLnet project page](https://nlnet.nl/project/Inochi2D/); Live2D Cubism is under Live2D's own proprietary licence — [web] [Live2D Open Software License](https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html); a community Rust port (MPL-2.0) is early-stage — [web] [inochi2d crate](https://lib.rs/crates/inochi2d)
- python-lottie builds Lottie JSON from Python classes — [web] [PyPI lottie](https://pypi.org/project/lottie/)
- Morevna + RenderChan: see section 2.

### Inferences
- AnimatedDrawings relies on OSMesa, which recent Mesa no longer ships (section 5), so on this box it would need porting
  to EGL. I haven't verified that.
- The most practical "anime-looking automatically" Blender route is: import a free/licensed VRM (VRoid-style) character, apply an
  EEVEE Shader to RGB toon material and hull or Line Art outlines, keyframe or pose from Python, and render at 720x1280 with 4
  samples on twos. Licences of individual character models must be checked one by one.

### Gaps
- Talking-Head-Anime (single-image anime puppet nets) CPU speed and licence: nothing found.
- No GitHub project found that procedurally generates whole anime characters plus scenes headless end to end.

---

## 7. Practical blockers: headless OpenGL, fonts and emoji, containers, disk

### Takeaway
The main blocker for Blender's EEVEE and Grease Pencil on this box was a missing `libEGL.so.1`; `apt-get install libegl1
libegl-mesa0` fixed it. Disk is the next limit: Blender takes 1.2 GB extracted and free space swings between about 4 and 8 GB as other
jobs run. CPU time is the real cost: anime cel frames from EEVEE take roughly 8-15 s each on a shared 4-core box, versus about 2 s for Workbench.

### Cited Findings
- [local test] EEVEE `-b` without libEGL: `Couldn't open libEGL.so.1`; with Mesa EGL installed it renders, printing
  `EGL_BAD_MATCH` warnings. No Xvfb needed.
- Blender's headless path is EGL with Mesa surfaceless, Linux-only — [web] [commit 3195a381200](https://archive.blender.org/lists/bf-blender-cvs/2022-August/176810.html)
- llvmpipe is Mesa's software rasterizer that "uses LLVM to do runtime code generation" — [web] [Mesa llvmpipe docs](https://ldeks.pages.freedesktop.org/mesa/llvmpipe.html)
- Blender Linux minimum is 8 GB RAM and 4 cores — [web] [blender.org requirements](https://www.blender.org/download/requirements/)
- [local test] Disk: free space was 8.2 GB before the download, 4.0 GB just after extracting (other jobs were also writing), and
  7.4 GB after I deleted the Blender folder. `fonts-noto-color-emoji` is installed in this container.

### Inferences
- Keep all text, captions and emoji in the existing 2D compositing stage (pycairo with fontconfig and Noto Color Emoji). Blender
  text objects are not a good place for colour emoji (my understanding, not checked).
- In Docker/CI, the same recipe should apply: official Blender tarball + distro `libegl1 libegl-mesa0` (+ `libgl1-mesa-dri`), no
  GPU and no X server. Set `view_transform="Standard"` for flat anime colours.

### Gaps
- RAM use per EEVEE frame, and whether two Blender renders can run in parallel within 15 GB, not measured.
- Vulkan/lavapipe path, Xvfb path and `QT_QPA_PLATFORM=offscreen` for Krita/OpenToonz not tested.
