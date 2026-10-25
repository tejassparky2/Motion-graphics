# CPU-only rendering options for code-driven 3D horror Shorts (late 2026)

Pipeline under study: three.js r169, rendered frame by frame in headless Chromium with SwiftShader, 4 cores, ~15 GB RAM,
720x1280 at 30 fps, ~2,400 frames per 80 s episode, ~1 frame/s with UnrealBloomPass + PCF soft shadows + ACES.
Local checks made for this note (25 Oct 2026): `channels/horror/render.mjs` launches chrome-headless-shell with
`--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`, renders one page sequentially and reads each
frame back with `canvas.toDataURL("image/png")`; it already supports `RANGE=a:b` partial renders. The container has an
Intel Xeon @ 2.10 GHz (4 logical CPUs, AVX2 + AVX-512), Mesa 25.2.8 with `swrast_dri.so` (gallium/llvmpipe), LLVM 20,
and `Xvfb`/`xvfb-run` installed. (Source for these: local files `channels/horror/render.mjs`, `/proc/cpuinfo`, `dpkg -l`.)

## Which three.js post-processing most improves a dark horror look, and what does it cost (AO, pmndrs/postprocessing, volumetrics, grain/LUT), including under SwiftShader?

### Takeaway
Everything needed for a stronger horror grade is already in the r169 package (GTAOPass, SAOPass, SSAOPass, LUTPass,
FilmPass, BokehPass, SMAAPass, GodRaysShader, VignetteShader, RGBShiftShader); N8AO and pmndrs/postprocessing add a better
AO and the ability to merge grain + vignette + chromatic aberration + LUT into one full-screen pass. No source benchmarks
any of these under SwiftShader, so cost has to be measured locally; the sources only give relative hints (half-resolution
AO 2-4x faster, quarter-resolution god-ray blur, raymarched volumetrics "expensive" and usually run at reduced resolution).

### Cited Findings
**What r169 ships (built in)**
- r169's `examples/jsm/postprocessing` contains AfterimagePass, BloomPass, BokehPass, FilmPass, GTAOPass, GlitchPass,
  LUTPass, OutlinePass, OutputPass, SAOPass, SMAAPass, SSAARenderPass, SSAOPass, SSRPass, TAARenderPass, UnrealBloomPass and
  others; `examples/jsm/shaders` contains FilmShader, GodRaysShader, VignetteShader, RGBShiftShader, ColorCorrectionShader,
  PoissonDenoiseShader, GTAOShader, SAOShader, SSAOShader, FXAAShader, SMAAShader — [three.js r169 tree](https://github.com/mrdoob/three.js/tree/r169/examples/jsm/postprocessing) (confirmed by listing the installed `three@0.169.0` package in `build/is3d/node_modules/three`).
- r169 also ships `misc/ProgressiveLightMap.js`, `lights/LightProbeGenerator.js`, `lights/RectAreaLightUniformsLib.js` — [three.js r169 tree](https://github.com/mrdoob/three.js/tree/r169/examples/jsm) (confirmed in the local package).
- GTAOPass docs describe the constructor and output modes, including a Denoise output; no timings are given — [three.js GTAOPass docs](https://threejs.org/docs/pages/GTAOPass.html).
- No source found that times GTAOPass against SAOPass/SSAOPass; a third-party engine port runs three.js's GTAO steps at half resolution to save cost — [null3d PR #288](https://github.com/null3d-engine/null3d/pull/288).

**N8AO**
- N8AO is CC0-1.0, needs WebGL 2 ("WebGL 1 is not supported"), recommends three.js r161 or later; use `N8AOPass` in place of RenderPass with three.js EffectComposer, or `N8AOPostPass` after a RenderPass with pmndrs/postprocessing — [N8AO README](https://github.com/N8python/n8ao).
- Quality presets: Performance = 8 AO samples / 4 denoise samples; Low = 16/4; Medium (default) = 16/8; High = 64/8; Ultra = 64/16; plus Neural-Low/Medium/High modes (neural denoise, always full resolution) — [N8AO README](https://github.com/N8python/n8ao).
- `halfRes = true` computes AO at half resolution: README claims 2x-4x speedup with some loss of detail; depth-aware upscaling costs ~1 ms (GPU, hardware unspecified); half-res Ultra is "slightly slower than full-res Performance but looks significantly better" — [N8AO README](https://github.com/N8python/n8ao).
- `accumulate = true` averages samples across frames while the camera is still (moving objects blur since no motion vectors); hardware MSAA does not work with AO, so the README recommends SMAA (Ultra preset) afterwards — [N8AO README](https://github.com/N8python/n8ao).
- No benchmark of N8AO under SwiftShader was found — [three.js forum HBAO vs N8AO thread](https://discourse.threejs.org/t/new-ambient-occlusion-example-hbao-vs-n8ao/58847) (thread exists; no software-renderer numbers surfaced).

**pmndrs/postprocessing**
- Effects: antialiasing (SMAA), Bloom, Blur, Color Depth, Color Grading (Brightness/Contrast, Hue/Saturation, Sepia, LUT), Depth of Field, Vignette, Glitch (Chromatic Aberration, Noise), God Rays, Scanline/Dot-screen/Grid, Pixelation, Outline, Shock Wave, SSAO, Texture, Tone Mapping — [pmndrs/postprocessing README](https://github.com/pmndrs/postprocessing).
- `EffectPass` "automatically organizes and merges any given combination of effects", reducing render operations compared with chaining separate passes; Zlib licence — [pmndrs/postprocessing README](https://github.com/pmndrs/postprocessing).
- postprocessing 6.38+ changed the default `Pass` camera to an OrthographicCamera (a break third-party passes had to fix) — [Casey Primozic, 1 Jan 2026](https://cprimozic.net/notes/posts/updating-three-good-godrays-for-threejs-182/).

**God rays and volumetric light / fog**
- r169's `webgl_postprocessing_godrays` example: renders the scene twice (colour + `MeshDepthMaterial` depth), builds an occlusion mask, then 3 radial-blur passes of 6 taps each into quarter-resolution ping-pong targets, then a combine pass; the source notes quarter-size depth caused flicker, so depth/colour/mask targets stay full size (half-float) — [three.js r169 godrays example](https://github.com/mrdoob/three.js/blob/r169/examples/webgl_postprocessing_godrays.html).
- three-good-godrays: screen-space raymarched god rays (from shadow maps) for pmndrs/postprocessing; updated 1 Jan 2026 to work with three.js 0.182 (new shadow-map depth packing, point-light cubemap shadows); the post does not say whether r169 works with the current release — [Casey Primozic notes](https://cprimozic.net/notes/posts/updating-three-good-godrays-for-threejs-182/); [three-good-godrays repo](https://github.com/Ameobea/three-good-godrays).
- three-volumetric-pass: raymarched screen-space volumetrics (fog, clouds) compatible with pmndrs/postprocessing, with a half-resolution option — [three-volumetric-pass repo](https://github.com/Ameobea/three-volumetric-pass).
- The official three.js "Volumetric Lighting" example is WebGPU/TSL-based, works with native lights and shadows, and exposes step count, resolution, denoise and fog amount — [three.js webgpu_volume_lighting](https://threejs.org/examples/webgpu_volume_lighting.html).
- Forum discussion: raymarching is per-pixel expensive, so reduced-resolution rendering is common; lower resolution causes edge aliasing around fog silhouettes — [three.js forum, volumetric lighting in WebGPU](https://discourse.threejs.org/t/volumetric-lighting-in-webgpu/87959).
- A write-up on volumetric light for the web covers depth-based ray stopping, SDF light shaping, shadow-mapped light volumes and Henyey-Greenstein phase functions (useful for a raymarched spotlight cone) — [daily.dev summary of "On Shaping Light"](https://daily.dev/posts/on-shaping-light-real-time-volumetric-lighting-with-post-processing-and-raymarching-for-the-web-usjkj4qeq).

**Bloom / float targets (relevant to software WebGL)**
- HDR bloom needs HalfFloat render targets; 8-bit (UnsignedByte) targets clamp to [0,1] and lose the bloom signal — [Sangil Lee, post-processing notes (2025)](https://sangillee.com/2025-01-15-post-processing/).
- Reported three.js bloom artefacts (black flashing blocks with transparent objects) were filed against desktop Chrome, not SwiftShader — [three.js issue #27878](https://github.com/mrdoob/three.js/issues/27878).

**SwiftShader status**
- Chromium deprecated automatic fallback to SwiftShader WebGL (starting around Chromium 135); context creation fails unless `--enable-unsafe-swiftshader` is passed — [three.js forum, Jan 2025](https://discourse.threejs.org/t/swiftshader-is-going-away-what-to-do/76140). Our render scripts already pass that flag (local `channels/horror/render.mjs`).

### Inferences
- On a CPU rasterizer, cost scales with full-screen passes x pixels (921,600 px at 720x1280) x texture taps. Merging grain,
  vignette, chromatic aberration, LUT and tone mapping into one pmndrs `EffectPass` should be cheaper than separate
  three.js ShaderPasses (based on the README's merging claim; not measured under SwiftShader).
- For a dark horror look the highest value per CPU cost is likely: (1) a LUT/colour grade + grain + vignette (single
  cheap pass), (2) half-res AO (N8AO Performance/Low halfRes, or GTAOPass) to ground objects in contact shadow,
  (3) quarter-res god rays only on the shots that have a visible light source (elevator emergency light, lightning).
  Raymarched volumetrics are the most expensive item and should be tried at half or quarter resolution with few steps.
- Because frames are rendered offline and the camera is deterministic, N8AO's `accumulate` (designed for a still camera)
  is not a natural fit for moving shots; rendering several jittered sub-frames per output frame (SSAARenderPass /
  TAARenderPass are in r169) is the offline equivalent but multiplies cost by the sample count.
- Built-in `scene.fog` / `FogExp2` ([three.js docs](https://threejs.org/docs/#api/en/scenes/FogExp2)) costs almost
  nothing per pixel and is the cheapest atmosphere layer; it does not give light shafts.
- A "fake" volumetric spotlight (additive cone mesh with a view-angle/depth fade shader) is a common cheap alternative to
  raymarching — UNVERIFIED (no source fetched in this session).

### Gaps
- No source reports per-pass timings for GTAOPass, SAOPass, SSAOPass, N8AO, pmndrs effects, god rays or volumetric passes
  under SwiftShader or llvmpipe; they must be benchmarked on our container (render a 10-frame test per pass).
- Whether SwiftShader exposes `EXT_color_buffer_float` / half-float render targets for bloom/AO was not confirmed by any
  source (our current UnrealBloomPass works, which suggests half-float targets function, but that is an inference).
- Compatibility of three-good-godrays / three-volumetric-pass current releases with three.js r169 not stated.

## Shadow quality (VSM, PCSS) and realistic soft-lighting tricks (baked lightmaps, light probes, RectAreaLight) in three.js

### Takeaway
r169 offers PCF, PCFSoft and VSM shadow maps; true contact-hardening PCSS is only an example that patches the shadow
shader chunk (~51 shadow-map reads per shadowed pixel worst case). RectAreaLight gives soft panel-light shading but casts
no shadows. For static horror sets, baked lighting (lightmaps / ProgressiveLightMap / baked probes) is the documented
route to soft, realistic light without per-frame cost.

### Cited Findings
- r169 `webgl_shadowmap_pcss` example: replaces `THREE.ShaderChunk.shadowmap_pars_fragment` globally; 17-sample blocker
  search plus 34 PCF reads (17 + 17 mirrored), i.e. up to ~51 shadow-map fetches per shadowed fragment, with per-fragment
  Poisson pattern generation; no benchmark given — [three.js r169 PCSS example](https://github.com/mrdoob/three.js/blob/r169/examples/webgl_shadowmap_pcss.html).
- Sources disagree on naming: one tutorial says `PCFSoftShadowMap` uses PCSS; three.js reference text describes it as PCF
  "with better soft shadows especially when using low-resolution shadow maps" — [sbcode soft shadows](https://sbcode.net/threejs/soft-shadows/); [three.js renderer constants mirror](https://neofixer.arizona.edu/css/CSSOrbit/asteroidJS/three/docs/api/en/constants/Renderer.html). The r169 PCSS example's need to patch the shader chunk shows PCSS is not the built-in PCFSoft type.
- VSM: softness controlled by `shadow.radius` and `blurSamples`; prone to light bleeding (bright halos where casters
  overlap); with VSMShadowMap all shadow receivers also cast shadows — [sbcode soft shadows](https://sbcode.net/threejs/soft-shadows/); [ramijames shadow types](https://www.ramijames.com/learn-threejs/lighting/types-of-shadows); [mysimulator shadows tutorial](https://www.mysimulator.uk/content/tutorials/threejs-shadows.html).
- RectAreaLight: "There is no shadow support"; "Only PBR materials are supported"; requires `RectAreaLightUniformsLib.init()` for WebGLRenderer — [three.js RectAreaLight docs](https://threejs.org/docs/pages/RectAreaLight.html).
- LightProbe can be filled from a cube texture (`LightProbeGenerator.fromCubeTexture`) or a CubeCamera render target; a forum reply says baking probes offline is much cheaper than a live CubeCamera; a "LightProbeVolume" baked-probe PR (#18371) did not port cleanly — [three.js forum, photorealism thread](https://discourse.threejs.org/t/how-to-get-photorrealism-light-shadows-in-three-js/28874).
- The photoreal look discussed in that thread is attributed to lightmaps — [three.js forum, photorealism thread](https://discourse.threejs.org/t/how-to-get-photorrealism-light-shadows-in-three-js/28874).
- `webgl_shadowmap_progressive` (ProgressiveLightMap) is the closest built-in example for baking soft shadows onto surfaces — [three.js forum, baking shadow onto plane](https://discourse.threejs.org/t/how-can-i-bake-a-shadow-onto-a-planegeometry/40887).

### Inferences
- In offline rendering, soft area-light shadows can be approximated by averaging several renders with the light jittered
  over its area (the idea behind ProgressiveLightMap), trading N renders per frame for physically plausible penumbrae.
  For mostly static sets (elevator box, bus interior, tower room), baking once and reusing for all 2,400 frames costs
  nothing per frame, while moving characters keep a single real-time shadow.
- For the elevator's red emergency light, a RectAreaLight (no shadows) for the soft panel glow plus one shadow-casting
  SpotLight is a plausible combination; PCSS's ~51 taps per shadowed pixel is likely costly on a CPU rasterizer.
- Baking lighting in Blender Cycles (CPU) and loading lightmaps into three.js is a common workflow — UNVERIFIED in this
  session (no source fetched).

### Gaps
- No timings found for VSM vs PCF vs PCSS on software WebGL.
- No three.js-specific lightmap-baking example for r169 was confirmed beyond ProgressiveLightMap.

## Blender headless (bpy): EEVEE/EEVEE Next without GPU, Cycles CPU per-frame times with OIDN, Workbench, Grease Pencil, farm/speed tips

### Takeaway
EEVEE is officially GPU-only (no CPU/software rendering planned); in a GPU-less Docker container EEVEE Next (4.2) failed
with a shader storage-block limit error, while legacy EEVEE (4.1) silently fell back to CPU. Cycles runs headless on CPU
with no OpenGL. No source gives clean seconds-per-frame for a simple 720x1280 Cycles CPU frame with OIDN; the only firm
number found is CPU denoise time (~1 s for the Junkshop scene on a desktop CPU), so render cost must be measured locally.

### Cited Findings
- EEVEE manual: "Being a rasterization engine, EEVEE only uses the power of the GPU to render." "There is no plan to support CPU (software) rendering as it would be very inefficient." "Headless rendering is not supported on headless Windows systems." — [Blender manual, EEVEE Limitations (latest)](https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html).
- A course guide states EEVEE headless rendering is supported only on Linux (since Blender 3.4, via EGL) — [SURF Blender course, GPU rendering](https://surf-visualization.github.io/blender-course/basics/rendering_lighting_materials/gpu_rendering/).
- Blender 4.2.1 EEVEE in Docker (A100 host, Oct 2024 - Jul 2025): without the NVIDIA `graphics` capability, EEVEE failed with `EGL_BAD_MATCH`, then (after Xvfb) "Unsupported platform as it supports max 8 SSBO binding locations" and "Too many vertex shader storage blocks (9/8)", even though `glxinfo` reported OpenGL 4.5; Blender 4.1.1 instead fell back to CPU with no error; fix was `NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics` — [Blender Artists thread](https://blenderartists.org/t/belender-4-2-1-eevee-does-not-work-inside-docker/1551491).
- A Docker image for headless EEVEE + Cycles via EGL (GPU required) exists — [HaiyiMei/blender-docker-headless](https://github.com/HaiyiMei/blender-docker-headless).
- EEVEE always uses OpenGL; Cycles can render without OpenGL/X in background (`-b`) mode — [devtalk, "Unable to open a display" (2.8 era)](https://devtalk.blender.org/t/blender-2-8-unable-to-open-a-display-by-the-rendering-on-the-background-eevee/1436?page=2).
- A user whose OpenGL renderer was llvmpipe was told by Blender developers the GPU was not used and "there is not much to be done" about lag under software rendering — [Blender bug T90225](https://developer.blender.org/T90225).
- EEVEE Next shader compile times are a known issue (separate tracker task) — [Blender issue #120100](https://projects.blender.org/blender/blender/issues/120100).
- Grease Pencil "is drawn using OpenGL", so a no-GPU farm needs GPU+driver or software emulation; a Mesa opengl32.dll workaround rendered GP successfully (Windows, 2019); even hidden GP objects made renders fail; geometry-only Cycles scenes rendered fine on the farm — [devtalk, Grease Pencil on headless no-GPU farm](https://devtalk.blender.org/t/rendering-grease-pencil-objects-on-headless-no-gpu-render-farm-machines-in-blender-2-8/10194).
- GPU-enabled compositor nodes (Defocus) were reported very slow in headless container mode — [Blender issue #126887](https://projects.blender.org/blender/blender/issues/126887).
- OIDN CPU denoise time for the Junkshop scene: ~1.22 s on Intel i9-13900K, ~1.04 s on Apple M2 Ultra CPU (vs ~0.08 s on RTX 3090); path-tracing time excluded — [Blender 4.1 Cycles release notes](https://developer.blender.org/docs/release_notes/4.1/cycles/).
- Non-Blender reference: OIDN on a 16-core Ryzen 9 took ~581 ms per 1080p frame (463 ms after keeping the filter alive between frames) — [blendity PR #85](https://github.com/EmilianoManaloIV/blendity/pull/85).
- Old data point: Blender demo scene at 100 samples took 25 s on a Ryzen 7 @ 3.4 GHz (2020-era Blender, not 720x1280) — [AnandTech forum](https://forums.anandtech.com/threads/post-your-ryzen-blender-demo-scores-amd-clarifies-blender-benchmark-confusion-run-150-samples.2494600/post-38629820).
- Render-farm guides give only broad ranges ("a single Cycles frame might take 2 to 30 minutes depending on complexity") and suggest 256-512 samples + adaptive sampling 0.01 + OIDN — [SuperRendersFarm settings guide (2026)](https://superrendersfarm.com/article/blender-render-settings-optimization-guide); a low-end guide suggests 50-100 samples with denoising — [iRender dev.to (2025)](https://dev.to/irender_gpu_cloud/blender-cycles-optimization-tips-for-low-end-pc-2025-1odd).
- Blender Open Data publishes per-device "samples per minute" for scenes like Junkshop/Classroom (e.g. one Ryzen 5 5600 submission 924 spm, device type not visible) — [Blender Open Data sample entry](https://opendata.blender.org/benchmarks/2f62317e-e064-4b77-918b-698557ff022e).

### Inferences
- EEVEE Next on Mesa llvmpipe in our container is unlikely to work out of the box: the Docker failure (OpenGL 4.5 reported,
  8 vertex SSBO bindings, EEVEE Next needs 9) matches what a software GL stack would report — but the thread never
  names llvmpipe, so this is an inference. Legacy EEVEE (Blender <= 4.1) did render via CPU fallback in that thread,
  speed unknown.
- Cycles CPU is the only Blender engine guaranteed to work here. At 2,400 frames per episode, every 1 s/frame adds 40 min
  of render time; a dark interior with volumetrics, lightning and OIDN on 4 cores will very likely exceed our current
  ~1 s/frame by a large factor (arithmetic + the ranges above; no measured number for our case).
- Dark horror scenes are the worst case for path tracing (low light = more noise = more samples), which raises Cycles
  cost relative to the rasterized three.js path.

### Gaps
- No source gives Cycles CPU seconds-per-frame for a simple 720x1280 scene with OIDN on a 4-core CPU; a local test render
  is the only reliable number.
- No source confirms whether Workbench renders under Mesa llvmpipe in Blender 4.x/5.x (it is OpenGL-based like EEVEE,
  but not confirmed).
- No current (4.3+ Grease Pencil v3) report on GP rendering without a GPU.
- Render-farm options (Flamenco, SheepIt, commercial farms) and Persistent Data speed tips were not researched with sources.

## Godot 4 Movie Maker mode without a GPU

### Takeaway
`--headless` swaps in a dummy rendering driver, so Movie Maker cannot record in headless mode; on a GPU-less machine Godot
would need a software GL/Vulkan stack (llvmpipe/Lavapipe/SwiftShader) plus a (virtual) display, and developers describe
that as "extremely slow". Off-screen rendering is still an open proposal (Oct 2026).

### Cited Findings
- `--headless` "disables all rendering code" (2022) and "swaps in a dummy driver that disables rendering outright" (Aug 2026 comment); off-screen rendering would still not lift the GPU requirement "unless you use Lavapipe or SwiftShader ... to provide a software Vulkan implementation"; the proposal is open, with an open draft PR godotengine/godot#94530 (Feb 2026) — [godot-proposals #5790](https://github.com/godotengine/godot-proposals/issues/5790).
- Headless mode lets the engine run "without a GPU or display server" (for servers/exports) — [Godot docs, exporting for dedicated servers](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html).
- Movie Maker outputs: OGV (Theora/Vorbis, editor builds only), AVI (MJPEG, 4 GB limit), PNG sequence + WAV (lossless, transparency possible); `--write-movie` and `--fixed-fps` work in exported projects; output is identical regardless of hardware speed ("Faster hardware will allow you to render a given animation in less time, but the visual output remains identical"); recommended quality 0.75-0.9 — [Godot docs, Creating movies](https://docs.godotengine.org/en/latest/tutorials/animation/creating_movies.html).
- A developer report (Godot 4.7.1, macOS) says Movie Maker does not work with `--headless` but works with the real renderer and an off-screen window — [dev.to, Godot Movie Maker on macOS](https://dev.to/nefayran/godot-movie-maker-and-screenshots-on-macos-without-headless-26pi).
- Godot 4.2's Compatibility (OpenGL/GLES3) renderer ran on llvmpipe while Forward+ and Mobile failed on that setup — [godot issue #87088](https://github.com/godotengine/godot/issues/87088).
- A forum answer: llvmpipe or Lavapipe can be used, "but these are extremely slow solutions compared to a purpose-built software renderer" — [Godot forum, render to framebuffer without X](https://forum.godotengine.org/t/can-godot-render-directly-to-frame-buffer-without-x-on-linux/55812).
- Godot on llvmpipe instead of hardware Vulkan shows very poor performance — [godot issue #83225](https://github.com/godotengine/godot/issues/83225); running Godot 4 with Vulkan on the llvmpipe CPU driver in WSL2 is discussed in [godot-proposals discussion #4335](https://github.com/godotengine/godot-proposals/discussions/4335).
- RenderingDevice is not available in headless mode or with the Compatibility renderer — [Godot RenderingDevice docs (4.4)](https://docs.godotengine.org/en/4.4/classes/class_renderingdevice.html).

### Inferences
- Realistic GPU-less Godot route: Compatibility renderer + Xvfb + Mesa llvmpipe + `--write-movie frames.png --fixed-fps 30`
  (not `--headless`). The Compatibility renderer lacks Forward+ features (SDFGI, volumetric fog) per Godot's renderer
  split, so the main reason to switch (Godot's volumetric fog) would be lost on CPU — the feature split itself is
  UNVERIFIED in this session.
- Switching to Godot means rewriting all scenes from three.js/JS to Godot scenes/GDScript for an uncertain speed/quality gain.

### Gaps
- No source reports Movie Maker frame times on llvmpipe/Lavapipe; no confirmation that Forward+ with volumetric fog runs
  on Lavapipe in a container.

## Remotion + @remotion/three: how it renders 3D, GL flags, licence, CPU speed

### Takeaway
Remotion renders by driving headless Chrome frame by frame, i.e. the same mechanism as our script; on a machine with no
GPU its recommended `--gl=swangle` is SwiftShader via ANGLE, the same software path we already use, and its docs warn it
"might be slow". It adds React tooling, parallel tabs and a studio, not better 3D quality. Free only for individuals and
companies of up to 3 people; companies of 4+ need a paid licence.

### Cited Findings
- `--gl` options: `angle` is the default in Remotion 5.0 (GPU if available, else SwiftShader fallback; known memory-leak problem, split long renders); `null` was the 4.0 local default; `swangle` is the default on Lambda/Cloud Run and is recommended for WebGL/WebGPU/Three.js on machines without a GPU — "Rendering might be slow"; `angle-egl` for Linux cloud GPUs; also `egl`, `swiftshader`, `vulkan` — [Remotion --gl docs](https://www.remotion.dev/docs/gl-options).
- @remotion/three docs say Three.js does not render with the default OpenGL renderer and recommend `angle` — [@remotion/three docs](https://www.remotion.dev/docs/three); [WebGL during renders](https://www.remotion.dev/docs/webgl).
- Performance docs: WebGL (Three.js, Skia), canvas and CSS shadows/gradients/blur are GPU-dependent; "Compute instances in the cloud do not have a GPU and may take a long time to render these effects"; use `npx remotion benchmark` to find the best `--concurrency` — [Remotion performance tips](https://www.remotion.dev/docs/performance).
- Concurrency (parallel Chromium tabs/instances): increased concurrency "does not consistently improve performance and can sometimes make rendering slower" on large VPSs — [remotion issue #4949](https://github.com/remotion-dev/remotion/issues/4949); default concurrency reported as 50% of logical cores (third-party summary; not stated on the performance page I read) — [rendercomp blog](https://rendercomp.com/blog/remotion-render-time-benchmarks/).
- A reported progressive slowdown on long renders (asset rebuild per frame, O(n^2)) — [remotion issue #11911](https://github.com/remotion-dev/remotion/issues/11911).
- Licence: free for "individuals and companies up to three people", including commercial use; a Company License is needed for companies of 4+ and collaborations; Remotion for Automators $0.01/render with $100/month minimum; Remotion for Creators $25/month per seat; Enterprise from $500/month — [Remotion licensing page](https://www.remotion.pro/license). A third-party note says contractors count toward team size and Remotion 5.0 binds the licence to new terms (not confirmed on the official page) — [snapcn Remotion licence summary](https://snapcn.dev/remotion-license-pricing).
- Example three.js Remotion project exists — [uxfreak/walking-characters-remotion](https://github.com/uxfreak/walking-characters-remotion).

### Inferences
- Moving to Remotion would not improve image quality or software-render speed (same Chrome + SwiftShader path); its value
  is tooling (React, Studio preview, built-in concurrency). Our script already gets the core benefit (deterministic
  `renderAt(t)` seeking).
- Licence: whether the owner's business counts as "up to three people" (incl. contractors) decides free vs paid; check
  before adopting.

### Gaps
- No published CPU-only fps numbers for @remotion/three scenes with `swangle`.

## Theatre.js for keyframing three.js cameras/objects: licence and 2025-2026 status

### Takeaway
Theatre.js core is Apache-2.0 and the studio is AGPL-3.0; public development has been paused since the team moved work to
a private repo for a 1.0 rewrite, with no official public update through at least March 2026. Usable, but a maintenance risk.

### Cited Findings
- `@theatre/core` is Apache-licensed; `@theatre/studio` is AGPL 3.0; only core's Apache terms apply to the final bundle; the repo banner says development was "_temporarily_ moved ... to a private repo" for Theatre.js 1.0 and "Terms and license will remain OSS" — [theatre-js/theatre GitHub](https://github.com/theatre-js/theatre).
- Issue "This wonderful project will not continue?" (14 May 2025) is open with no maintainer reply; a secondhand Discord screenshot (posted 20 Jul 2025) quotes a team member: "Just a 1.0 rewrite that's taking (way) longer than planned. Almost there."; users asked again Oct 2025 and Mar 2026 with no answer — [theatre issue #504](https://github.com/theatre-js/theatre/issues/504).
- New issues were still being filed in Dec 2025 — [theatre issues](https://github.com/theatre-js/theatre/issues).
- The project's X account's latest surfaced post announced v0.7 (Aug 2023) — [Theatre.js on X](https://x.com/theatre_js?lang=en).

### Inferences
- For a code-only pipeline, the studio UI (AGPL) is only needed while authoring; exported JSON state played back by core
  (Apache) keeps the shipped renderer free of AGPL code — based on the README's statement that only core's terms apply
  to the final bundle.
- Given the stalled public repo, keyframes in our own JSON/timing format (as `make_horror.py` already does with
  timing.json) remain the lower-risk option.

### Gaps
- Latest npm version and its date were not confirmed from a primary source (believed 0.7.x — UNVERIFIED).

## HeyGen HyperFrames: what it is, licence, how it renders, anything for 3D

### Takeaway
HyperFrames is an Apache-2.0, agent-oriented HTML-to-MP4 framework that seeks each frame in headless Chrome via Puppeteer
and encodes with FFmpeg; three.js is a supported runtime, but it uses the same browser rendering path as ours, so it adds
authoring/agent tooling, not 3D quality or CPU speed.

### Cited Findings
- "an open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos"; Apache 2.0 with "no per-render fees or commercial-use thresholds"; renderer "seeks each frame in headless Chrome and encodes the result with FFmpeg"; engine package is a "Seekable page-to-video capture engine using Puppeteer and FFmpeg"; Three.js listed among supported runtimes with GSAP, Lottie, Anime.js; `@hyperframes/shader-transitions` provides WebGL transitions; AWS Lambda distributed rendering; needs Node.js 22+ and FFmpeg; ~71.6k stars — [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes).
- Site headline "The video editor built for agents"; install via `npx skills add heygen-com/hyperframes`; no render-speed claims — [hyperframes.heygen.com](https://hyperframes.heygen.com/).
- Example compositions behind HeyGen's launch videos are public — [hyperframes-launches](https://github.com/heygen-com/hyperframes-launches); [hyperframes-launch-video](https://github.com/heygen-com/hyperframes-launch-video).

### Inferences
- Without a GPU, HyperFrames' three.js frames go through Chrome's software WebGL just like ours; its possible gains are
  ready-made 2D overlay/caption/transition tooling and Lambda fan-out, not local 3D speed.

### Gaps
- The README does not document GPU/GL flags or local parallel workers; no CPU-only 3D benchmarks found.

## Parallelising frame rendering on a 4-core CPU (multiple headless browsers) and faster software WebGL

### Takeaway
The biggest documented CPU-only speed lever is not parallel browsers but switching Chrome's software backend from
SwiftShader to Mesa llvmpipe (`--use-angle=gl` + Xvfb + `LIBGL_ALWAYS_SOFTWARE=1`): ~4x faster on a three.js page in one
production report. Parallel browser instances give sub-linear gains because the software rasterizers are already
multi-threaded and compete for the same cores.

### Cited Findings
- Microlink (GPU-less Linux nodes: 8-core Intel @ 2.1 GHz, ~16 GB RAM, Chrome 150, Mesa 26.1.3, LLVM 19, AVX2) rendering
  the three.js `webgl_animation_skinning_blending` example: SwiftShader ~24 s (24-31 s in benchmark runs) vs llvmpipe ~6 s
  isolated (~4x), 7-14 s under load (~2x); flags: remove `--use-angle=swiftshader`, add `--use-angle=gl`; do not use
  `--disable-gpu` (forces SwiftShader) or `--in-process-gpu`; set `LIBGL_ALWAYS_SOFTWARE=1`; Xvfb must start before Chrome
  because `--use-angle=gl` needs an X display even headless; without X, WebGL silently fell back to flat 2D; llvmpipe JITs
  shaders via LLVM and is "tiled and multi-threaded"; cold JIT and shared cores made single runs unreliable — [Microlink blog, "WebGL without a GPU"](https://microlink.io/blog/webgl-without-a-gpu).
- Mesa: `LIBGL_ALWAYS_SOFTWARE=true` forces software rendering; `GALLIUM_DRIVER` selects softpipe or llvmpipe — [Mesa environment variables](https://docs.mesa3d.org/envvars.html). (Mesa also documents `LP_NUM_THREADS` to set llvmpipe's thread count — UNVERIFIED in this session.)
- Remotion: concurrency gains flatten; on Google Cloud VMs ~8.8-16.2 fps "nowhere near proportional to the compute
  resources" (video compositions, not WebGL) — [remotion issue #4949](https://github.com/remotion-dev/remotion/issues/4949); `npx remotion benchmark --concurrency=...` recommended — [Remotion performance tips](https://www.remotion.dev/docs/performance).
- Going above core count competes with the OS scheduler and typically doesn't help — [GenMotion answer on slow Remotion renders](https://genmotion.dev/answers/remotion-render-is-slow).
- Chromium's SwiftShader WebGL now requires `--enable-unsafe-swiftshader` (from ~Chromium 135) — [three.js forum](https://discourse.threejs.org/t/swiftshader-is-going-away-what-to-do/76140).

### Inferences
- Our container already has the ingredients Microlink used (Mesa 25.2.8 llvmpipe, Xvfb, LLVM 20, AVX-512), so a
  `--use-angle=gl` + `xvfb-run` + `LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe` trial is cheap; any speed-up can be
  spent on AO/god rays/grain. It must be verified per frame that WebGL did not silently fall back (e.g. compare a test
  frame pixel-for-pixel with the SwiftShader render, or log `WEBGL_debug_renderer_info`).
- Parallelism: split the 2,400 frames into 2 contiguous `RANGE` chunks (one browser each) and benchmark 1 vs 2 vs 4
  processes; with multi-threaded rasterizers on 4 cores, expect sub-linear gains (per the Microlink "under load" and
  Remotion results). RAM (15 GB) is unlikely to be the limit at 720x1280 but should be watched.
- Per-frame overhead outside WebGL also matters on CPU: `canvas.toDataURL("image/png")` PNG-encodes and base64-encodes
  every frame inside the page; reading raw pixels or a faster lossless/JPEG path may cut seconds per batch (inference,
  not measured).

### Gaps
- No source measured SwiftShader vs llvmpipe for post-processing-heavy three.js scenes (bloom, AO, shadows) or on a
  4-core machine; the 4x figure is one 8-core report on one example scene.
- No published numbers for multiple headless Chromium instances doing WebGL on 4 cores.
