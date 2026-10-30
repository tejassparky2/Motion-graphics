# Claude Code skills, MCP servers, plugins and agent tooling for animated video (as of 30 Oct 2026)

Method note: GitHub search and API calls are blocked from this cloud container ("sessions are bound to their configured repositories"). Repo statistics therefore come from the ecosyste.ms mirror of GitHub (`https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/<owner>%2F<repo>`), queried on 30 Oct 2026. The mirror's sync dates ranged from 8 to 30 Oct 2026, so a few counts may lag by days. "Pushed" means the last commit date in that mirror. Most repos listed have no GitHub Releases, so "last push" is the best maturity signal available. Labels: **Documented** = the project's own docs or README; **Claim** = a vendor or author claim with no independent check; **Secondary** = blog, listicle or search summary; **Inference** = my reasoning. Context the earlier reports already settled, not repeated here: Remotion and HyperFrames seek frames in headless Chrome, so without a GPU they use the same SwiftShader path as our three.js renderer. Godot's `--headless` disables rendering. Theatre.js development stalled. Blender EEVEE rendered on this server through Mesa llvmpipe/EGL in an earlier test (see `reports/CPU anime animation pipeline.md` and `reports/3D horror Shorts animation and hooks.md`).

Caution on popularity: several 2026 repositories gained stars at a rate that is unusual for developer tools. OpenMontage has ~72.9k stars 7 months after creation, HyperFrames ~73.6k after 7.5 months, and obra/superpowers ~304k. Treat star counts as a measure of attention, not of output quality (Inference).

## 1. Blender MCP servers: capabilities, GUI vs background mode, Linux headless use, reported quality

### Takeaway
Blender has a mature community MCP (ahujasid's "MCP for Blender", MIT, ~32.7k stars) and, since 2026, an official Blender Lab MCP server (add-on v1.0.3, Blender 5.1+). Both drive a **running Blender GUI** through a localhost socket and execute LLM-written Python with no guards. Several small MIT servers run Blender in `--background` mode for headless Linux, but they have only 30-60 stars. The only rigorous evidence of quality, the BlenderGym benchmark (CVPR 2025), found a "substantial performance gap" between AI models and human Blender users. For our container, an MCP adds little over Claude calling `blender -b --python script.py` directly from Bash (Inference).

### Cited findings
**ahujasid/mcp-for-blender (formerly ahujasid/blender-mcp)**
- The repo describes itself as a "Community plugin to control Blender 3D with any LLM of your choice. Not affiliated with the official Blender Foundation". MIT; ~32,742 stars; created 2025-03-07; last push 2026-10-29; 57 open issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/ahujasid%2Fmcp-for-blender) (Documented)
- Tools (Documented, [README](https://github.com/ahujasid/blender-mcp)):
  - `execute_blender_code` runs Python in a live Blender session, and the AI writes Python for "modelling, layout, materials, animation, rigging and retopology".
  - `look` shows the viewport, the camera view, multi-angle sheets or animation frames, in solid, material, rendered, wireframe or x-ray mode.
  - `get_scene_info` returns a summary of the scene.
  - `generate_3d` calls Tripo, Hunyuan3D, Hyper3D Rodin or Meshy.
  - `search_assets` / `import_asset` cover Poly Haven, Sketchfab and Poly Pizza.
- Architecture: an add-on runs a socket server inside Blender (default `localhost:9876`, configurable with `BLENDER_HOST`/`BLENDER_PORT`). The README describes only the GUI workflow and says nothing about background mode. Requires Blender 3.0+, Python 3.10+ and uv — [README](https://github.com/ahujasid/blender-mcp) (Documented)
- README warnings ([README](https://github.com/ahujasid/blender-mcp), Documented):
  - Arbitrary code "can be powerful but potentially dangerous".
  - "ALWAYS save your work before using it."
  - "Complex operations might need to be broken down into smaller steps."
  - The socket server has no authentication or encryption.
  - Safe mode (`BLENDER_MCP_SAFE_MODE=1`) is off by default.
  - Poly Haven downloads freeze the UI.
  - Only one MCP server instance should run at a time.
- The project's troubleshooting notes say Claude is "sometimes erratic", particularly with the Poly Haven integration — [DEV Community summary](https://dev.to/githubopensource/blendermcp-unleash-the-power-of-ai-in-your-3d-modeling-workflow-1ooa) (Secondary)

**Official Blender Lab MCP server**
- Hosted at blender.org/lab/mcp-server. The add-on is v1.0.3 (`mcp-1.0.3.zip`) and requires Blender 5.1 or newer. The page describes "a natural language interface with Blender's Python API", aimed at documentation access and exploring complex setups — [Blender Lab](https://www.blender.org/lab/mcp-server/) (Documented)
- The official security warning reads: "The MCP server will execute LLM generated code in Blender without any guards in place … it is recommended to use a virtual machine, or a system without access to sensitive information." The page also says "The sucess of the operation will depend on the model used", and several of its use cases are still "yet to be explored" — [Blender Lab](https://www.blender.org/lab/mcp-server/) (Documented)
- v1.0.0 is dated 27 Apr 2026 and v1.0.3 is current as of Sep 2026. Sources disagree on whether the maintainer label is "Blender Lab" or "Blender Authors" — [StraySpark comparison](https://www.strayspark.studio/blog/official-blender-mcp-server-comparison-2026); [Voyager](https://voyager.so/blog/blender-mcp) (Secondary)
- A developer guide (17 Oct 2026) says the official server includes an `execute_blender_code_for_cli` tool that "executes Python code in a background Blender process". The page returned 404 when fetched, so this is unverified — [DevelopersDigest via search](https://www.developersdigest.tech/mcp-servers/blender-mcp) (Secondary, unverified)
- One source says this server is what "Anthropic's Blender connector for Claude uses". No primary source was found for that — [zenn.dev guide](https://zenn.dev/shintama/articles/blender-official-mcp-claude?locale=en) (Secondary, unverified)

**Headless/background-mode servers (small, MIT)**

| Server | Headless mechanism | Stars / dates | Source |
|---|---|---|---|
| djeada/blender-mcp-server | "headless transport" launches a separate `blender -b`; `BLENDER_MCP_HEADLESS_TIMEOUT` defaults to 3600 s; 22 tools in 6 namespaces | 30★, created 2026-02-27, last push 2026-09-23 | [repo](https://github.com/djeada/blender-mcp-server); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/djeada%2Fblender-mcp-server) |
| sandraschi/blender-mcp | "Headless by default", spawns `blender --background`; batch mesh/VSE/Grease Pencil, VRM | 60★, last push 2026-10-13 | [repo](https://github.com/sandraschi/blender-mcp); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/sandraschi%2Fblender-mcp) |
| dcc-mcp/dcc-mcp-blender | `blender --background --python …/blender_bootstrap.py`; model, UVs, rig, materials, render; recommended for CI | 50★, created 2026-04-12, last push 2026-10-25, 7 issues | [repo](https://github.com/dcc-mcp/dcc-mcp-blender); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/dcc-mcp%2Fdcc-mcp-blender) |
| nirholas/blender-mcp (official MCP registry) | "Drive a local Blender headlessly: inspect, convert, render and script 3D files" | v0.5.0 | [MCP registry API](https://registry.modelcontextprotocol.io/v0/servers?search=blender) |
| mohakmalviya/frugal-blender-mcp | 4 tools (discover, execute, inspect, capture), "338 tokens of fixed context" | 15★, created 2026-09-09 | [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/mohakmalviya%2Ffrugal-blender-mcp) |

- A query of the official MCP registry on 30 Oct 2026 also returned 9 Blender servers, including a paid "Blender-as-a-service" (willitblender) and blenderbridge. Most are early versions (0.x) — [MCP registry](https://registry.modelcontextprotocol.io/v0/servers?search=blender) (Documented listing)
- The claude-plugins.dev registry lists a `blender-animation` skill (TerminalSkills, 20★, 31 installs) — [claude-plugins.dev API](https://claude-plugins.dev/api/skills?q=blender) (Documented listing)

**Quality evidence**
- BlenderGym (CVPR 2025 highlight) asked 13 VLMs, including GPT-4o and Claude 3.5 Sonnet, to edit Blender Python so a render matches a goal image. Tasks covered object placement, lighting, procedural materials, blend shapes and procedural geometry. The authors report "a substantial performance gap between human Blender users and VLM systems", and even the best system "struggles with tasks relatively easy for human Blender users" — [arXiv 2504.01786](https://arxiv.org/pdf/2504.01786); [HF papers](https://huggingface.co/papers/2504.01786) (Study)
- The follow-up VIGA (arXiv 2601.11109) evaluates Claude-Sonnet-4 and Gemini-2.5-Pro on BlenderGym and reports gains from an interleaved render-and-look loop — [arXiv 2601.11109](https://arxiv.org/pdf/2601.11109) (Study, self-reported)
- The Reddit search found no hands-on threads from r/blender or r/ClaudeAI on output quality. Aggregator pages praise the tools but are not reviews — [search results incl. glama/mcpmarket listings](https://github.com/topics/blender-mcp) (Gap noted)

### Inferences
- In this container, Claude can already write a `bpy` script and run `blender -b file.blend --python make_shot.py -- --frames 1-48`, then read the rendered PNGs. A background-mode MCP adds structured tools but not new capability. The GUI MCPs (ahujasid, official Blender Lab) only make sense on the owner's laptop. There, `look` viewport screenshots give a fast visual feedback loop that BlenderGym/VIGA suggest matters.
- BlenderGym shows models fail at fine spatial and material edits. Blender is best used for things code does reliably: camera moves over pre-built sets, procedural backgrounds, toon-shaded plates. Asking an agent to model or rig the monsters themselves is not a good use.
- Security: every Blender MCP runs arbitrary Python. On the laptop, bind to localhost only and follow Blender Lab's own advice to use a VM or a machine without sensitive data.

### Gaps
- No independent, published per-frame CPU render time for a toon-shaded Blender shot at 1080x1920. The earlier report measured feasibility, not speed.
- I could not confirm the official server's background-mode tool or the "Anthropic connector" claim from a primary source.
- I found no Reddit or HN user reports with sample output from Blender MCP character animation (as opposed to static scenes).

## 2. Code-driven animation frameworks: Remotion (licence, skills, CPU speed), HyperFrames, Motion Canvas, Revideo, Manim CE, Theatre.js, Lottie, Rive

### Takeaway
For frame-accurate headless rendering, the live options are Remotion, HyperFrames, Revideo and Manim. Remotion is free for individuals and companies of up to 3 people ("Unlimited commercial use") and has official Claude Code skills (Jan 2026). HyperFrames (HeyGen, Apache-2.0, Mar 2026) has no per-render fees or headcount threshold and ships a Claude Code plugin. Revideo now lives at midrender/revideo, with headless rendering (v0.11.0, Jul 2026). Manim CE renders on CPU but suits diagrams, not characters. Motion Canvas is effectively dormant and Theatre.js is stalled. Lottie and Rive are playback formats: Lottie renders headlessly through rlottie or a browser, while Rive's own video export is a paid editor feature.

### Cited findings
**Remotion**
- Repo: ~67,430 stars, last push 2026-10-25, 206 open issues, licence "other" (source-available) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/remotion-dev%2Fremotion) (Documented)
- Licence (Documented, [remotion.pro/license](https://www.remotion.pro/license)):
  - "Remotion is free to use for individuals and companies up to three people." The Free License card says "Unlimited commercial use", "Must upgrade when your organization grows".
  - A Company License is "Required for collaborations and companies of 4+ people".
  - Pricing: "Remotion for Automators" costs $0.01 per render with a $100/month minimum. "Remotion for Creators" costs $25/month per seat. Enterprise starts at $500/month.
  - The page has no YouTube-specific clause.
- Official agent skills (Documented):
  - Remotion announced "Remotion now has Agent Skills - make videos just with Claude Code!" on 20 Jan 2026 — [X/Remotion](https://x.com/Remotion/status/2013626968386765291).
  - Install with `npx skills add remotion-dev/skills` or `npx remotion skills add`. Skills go to `.claude/skills` — [remotion.dev/docs/ai/skills](https://www.remotion.dev/docs/ai/skills); [remotion.dev/docs/cli/skills](https://www.remotion.dev/docs/cli/skills).
  - The remotion-dev/skills repo has ~5,617 stars, was created 2026-01-19, last push 2026-10-22, 22 issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/remotion-dev%2Fskills).
  - A third-party guide says the `remotion-best-practices` skill covers "animations, timing, audio, captions, and 3D" — [nemovideo guide](https://www.nemovideo.com/blog/remotion-agent-skills-claude-code-guide) (Secondary).
- CPU rendering: `--gl` accepts `swiftshader`, `swangle`, `angle`, `egl` and `vulkan`, and defaults to `swangle` on Lambda. Concurrency defaults to half the CPU threads. `npx remotion benchmark` compares concurrency settings. Remotion publishes no CPU-only fps figure — [remotion.dev/docs/cli/render](https://remotion.dev/docs/cli/render); [benchmark](https://www.remotion.dev/docs/cli/benchmark); [config](https://www.remotion.dev/docs/config) (Documented)
- Examples are mostly data/statistics animations and product promos, e.g. "This animated statistics video was created from a single prompt. Claude wrote the entire React/Remotion codebase" — [LinkedIn post](https://www.linkedin.com/posts/aaabulkhair_datascience-ai-claudecode-activity-7442858830163738626-smN-) (Claim)
  - video-shotcraft (Apache-2.0, ~14.5k★, created 2026-07-19) is a Claude Code/Codex skill for Remotion product promos with "124 shot recipe cards", beat sync and sound design — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Vincentwei1021%2Fvideo-shotcraft); [repo](https://github.com/Vincentwei1021/video-shotcraft) (Documented)
  - I found no Remotion-made character-animated story series.

**HyperFrames (HeyGen)**
- "an open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos". The renderer "seeks each frame in headless Chrome and encodes the result with FFmpeg". It supports GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI and custom frame adapters. Licence is Apache 2.0 with "no per-render fees or commercial-use thresholds". Requires Node 22+ and FFmpeg. Its Studio editor is "Available, evolving" — [README](https://github.com/heygen-com/hyperframes) (Documented)
- Claude Code: `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`, or `npx skills add heygen-com/hyperframes`. The core skills are `/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry` and `/media-use`, and the README cites a catalogue of ~450 blocks (transitions, captions, overlays) — [README](https://github.com/heygen-com/hyperframes) (Documented)
- Stats: ~73.6k★ (mirror) / 75.8k (page), created 2026-03-10, last push 2026-10-27, 174 issues. The README credits Remotion's Lambda as the more mature cloud renderer — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/heygen-com%2Fhyperframes); [README](https://github.com/heygen-com/hyperframes) (Documented)

**Motion Canvas / Revideo**
- Motion Canvas: MIT, ~19.4k★, last push 2026-07-02, 175 issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/motion-canvas%2Fmotion-canvas) (Documented). Secondary sources say it has had no stable release since Dec 2024, "core is effectively dormant", and it has "no built-in headless or cloud rendering" — [PkgPulse](https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026); [wireflow](https://www.wireflow.ai/blog/best-remotion-alternatives-in-2026) (Secondary)
- Revideo (a Motion Canvas fork) now lives at midrender/revideo: MIT, ~4,156★, last push 2026-07-15 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/midrender%2Frevideo) (Documented). Headless rendering is a function call (`renderVideo` uses a headless browser and FFmpeg) — [docs.re.video](https://docs.re.video/api/renderer/renderVideo) (Documented). The latest npm release is v0.11.0 (10 Jul 2026), and one article says the project has "folded into Midrender", a commercial editor — [search summary of snapcn/pkgpulse](https://snapcn.dev/remotion-vs-revideo) (Secondary, conflicting)
- A `motion-canvas` skill exists on Smithery (davila7) — [Smithery](https://smithery.ai/skills/davila7/motion-canvas) (Documented listing)

**Manim Community Edition**
- MIT, ~41.9k★, last push 2026-10-27, 390 open issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/ManimCommunity%2Fmanim) (Documented)
- Agent evidence:
  - TheoremExplainAgent (ACL 2025) makes videos of up to 10 minutes with Manim but "exhibits limitations in visual structuring, with issues such as misaligned text, overlapping shapes, and inconsistent sizes". The most frequent failure was invalid Manim code — [arXiv 2502.19400](https://arxiv.org/html/2502.19400); [ACL](https://aclanthology.org/2025.acl-long.332/) (Study)
  - Code2Video (ICML 2026, MIT, ~2.1k★) uses Planner/Coder/Critic agents and reports Element Layout rising from 0.59 to 0.91 with GPT-4o. Its repo says the best Manim code came from Claude-4-Opus — [arXiv 2510.01174](https://arxiv.org/pdf/2510.01174); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/showlab%2FCode2Video) (Study, self-reported)
- Tooling:
  - The MCP server daedalus/mcp-manimgl has 0★ — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=manim).
  - DominikPeters/manim-skill (render stills and review layout) is listed — [claude-plugins.dev](https://claude-plugins.dev/api/skills?q=manim) (Documented listing).

**Theatre.js**
- Apache-2.0, ~12.8k★, last push 2024-08-14 (no commits in over 2 years) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/theatre-js%2Ftheatre) (Documented)

**Lottie**
- lottie-web: MIT, ~32.3k★, last push 2025-09-01, 861 open issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/airbnb%2Flottie-web) (Documented)
- dotlottie-web (Rust+WASM player): MIT, ~925★, last push 2026-10-22 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/LottieFiles%2Fdotlottie-web) (Documented)
- Samsung/rlottie (C++ renderer): ~1.4k★, last push 2026-09-30, licence listed as "other". It "has no built-in video export", so frames must be piped to FFmpeg — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Samsung%2Frlottie); [repo](https://github.com/Samsung/rlottie) (Documented)
- rlottie-python: LGPL-2.1, 28★, returns Pillow images, and "rlottie is included in the wheel" — [repo](https://github.com/laggykiller/rlottie-python) (Documented)
- puppeteer-lottie (headless Chrome to MP4) was last pushed in 2020. lottie-render (MIT, 2★, 2026) does the same as an npm library or HTTP service — [puppeteer-lottie](https://github.com/mahboubii/puppeteer-lottie); [lottie-render](https://github.com/steven-panxd/lottie-render) (Documented)
- python-lottie is AGPL-3.0 on GitLab (135★) — [ecosyste.ms GitLab](https://repos.ecosyste.ms/api/v1/hosts/GitLab.com/repositories/mattbas%2Fpython-lottie) (Documented)
- The official MCP registry had **0** Lottie servers on 30 Oct 2026 — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=lottie)

**Rive**
- Runtimes are MIT (rive-runtime ~1.2k★, rive-wasm ~1.0k★, both active in Oct 2026) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/rive-app%2Frive-runtime) (Documented)
- Video export (H.264, WebM, PNG sequence) goes through the Rive editor's Cloud Renderer and "is available on paid plans". The React runtime does not render to a bitmap directly, and Rive's docs point to Revideo or Remotion for offline rendering — [Rive docs](https://rive.app/docs/editor/exporting/exporting-for-video-and-static-design); [Rive bitmap docs](https://rive.app/docs/runtimes/react/rendering-to-a-bitmap.md) (Documented)

**Anthropic's own creative skills**
- anthropics/skills (~184.8k★) includes `slack-gif-creator`, `algorithmic-art`, `canvas-design`, `theme-factory`, `frontend-design` and `web-artifacts-builder`. It has no video skill. Many skills are Apache 2.0, and the document skills are source-available — [skills folder](https://github.com/anthropics/skills/tree/main/skills); [README](https://github.com/anthropics/skills) (Documented)
- The official GSAP skill (`greensock/gsap-skills/gsap-core`) and a `threejs` skill are in the claude-plugins.dev registry — [claude-plugins.dev](https://claude-plugins.dev/api/skills?q=animation) (Documented listing)

### Inferences
- **Licence fit for a YouTube channel.** Remotion is free for the owner while the team stays at 3 people or fewer, including commercial videos. Hiring a 4th person or partnering with a company triggers the Company License. HyperFrames' Apache-2.0 has no such cliff.
- **Speed.** Remotion, HyperFrames and Revideo all screenshot headless Chrome. For DOM/canvas 2D work (layered PNG puppets, captions, overlays) they should be far faster than our WebGL-on-SwiftShader three.js path. They give no speed-up for WebGL/three.js scenes. None publishes CPU-only fps, so we would have to benchmark (`npx remotion benchmark`) on the 4-core box.
- **What they would add to our pipeline.** None of these adds "anime quality" by itself. The look comes from the art (laptop ComfyUI stills) and the compositing pass. A browser framework is worth it only for its ready-made blocks: transitions, caption styles, GSAP easing and a Studio preview. Our pycairo/NumPy compositor already does frame-accurate 2D at known cost.
- **Lottie** is useful only for vector overlays (UI chips, effect sprites). rlottie-python → NumPy → FFmpeg renders natively on CPU without a browser.
- **Rive** is not agent-friendly: authoring needs the GUI editor and its video export is paid.

### Gaps
- No measured CPU-only fps for Remotion, HyperFrames or Revideo at 1080x1920 on 4 cores.
- I couldn't confirm Revideo's governance (open-source project vs Midrender product) from a primary source.
- I found no examples of an anime-style character story series produced with Remotion or HyperFrames.

## 3. ComfyUI MCPs and automation, Godot MCPs, Krita/GIMP MCPs, open compositors (Natron, Friction, Glaxnimate) and NLE MCPs

### Takeaway
ComfyUI is the most mature target. Comfy-Org shipped a first-party local `comfy-mcp` plus a cloud MCP and a Claude Code plugin marketplace (mid-2026), but the local server must run on the same machine as ComfyUI. The community `artokun/comfyui-mcp` (MIT, ~879★) explicitly supports a remote ComfyUI URL, auth headers, a cloudflared tunnel mode, Windows, VRAM-clearing tools and WAN/LTX video packs. Godot MCPs control the editor and run projects but don't capture frames headlessly. Krita and GIMP MCPs are tiny or Windows-bridge projects. Natron, Friction and Glaxnimate have no MCP, so they would be scripted directly.

### Cited findings
**ComfyUI**
- ComfyUI core: GPL-3.0, ~142.6k★, last push 2026-10-24 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Comfy-Org%2FComfyUI) (Documented)
- **Comfy-Org/comfy-mcp** (first party):
  - Repo: ~310★, created 2026-07-01, last push 2026-10-27, 23 issues, licence "other" — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Comfy-Org%2Fcomfy-mcp).
  - Docs call it "Comfy's first-party local MCP server", with tools `run_workflow`, `wait_for_job`, `fetch_outputs`, `launch_comfyui`, `validate_workflow` and `search_models`.
  - The local server is launched over stdio on the ComfyUI machine (`claude mcp add comfy-mcp -e COMFY_BIN=… -- comfy-mcp`). The docs do not cover remote/LAN use.
  - The cloud endpoint `https://cloud.comfy.org/mcp` needs an active Comfy Cloud subscription and gives 5 free runs. Comfy MCP is described as "an early release".
  - Plugin: `/plugin marketplace add Comfy-Org/comfy-skills` — [docs.comfy.org/agent-tools/mcp](https://docs.comfy.org/agent-tools/mcp) (Documented).
  - comfy-skills is MIT, ~239★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Comfy-Org%2Fcomfy-skills).
- **artokun/comfyui-mcp**:
  - Repo: MIT, ~879★, created 2026-02-15, last push 2026-10-26, 81 issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/artokun%2Fcomfyui-mcp).
  - Remote and auth: `COMFYUI_URL` targets a remote instance, and remote mode disables local filesystem and process tools. Gateway auth uses `COMFYUI_AUTH_TOKEN`/`HEADER`/`SCHEME`. `--tunnel` runs over HTTP with a generated auth token through a cloudflared quick tunnel. "Auth is opt-in."
  - "Works on macOS, Linux, and Windows."
  - VRAM tools: `clear_vram` calls ComfyUI's `/free`, and a watchdog warns when less than 1 GB is free.
  - Video uses LTX-2.3 and WAN packs. The skill count is inconsistent: "42 AI skills" in the README vs "36" in the About text.
  - Plugin: `/plugin marketplace add artokun/comfyui-mcp` then `/plugin install comfy`.
  - The README itself says Comfy-Org's tools are "the better path" for users with no GPU — [README](https://github.com/artokun/comfyui-mcp) (Documented).
- Other ComfyUI MCPs:
  - joenorton/comfyui-mcp-server: Apache-2.0, ~411★, last push 2026-02-17 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/joenorton%2Fcomfyui-mcp-server).
  - ChristopherGoodale/comfy_mcp binds ComfyUI to the GPU box's Tailscale IP with a tailnet-only firewall rule, noting that ComfyUI has no authentication of its own — [repo](https://github.com/ChristopherGoodale/comfy_mcp) (Documented via search summary).
  - Registry entries include GermaniU/comfyui-mcp ("SDXL/Wan 2.2 … image and short-video") and MetaBrain-Labs — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=comfyui).
- Video nodes (context): kijai/ComfyUI-WanVideoWrapper (Apache-2.0, ~6.7k★, last push 2026-05-24, 1,285 open issues) and ComfyUI-AnimateDiff-Evolved (Apache-2.0, ~3.6k★, last push 2026-07-28) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/kijai%2FComfyUI-WanVideoWrapper); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Kosinkadink%2FComfyUI-AnimateDiff-Evolved) (Documented)

**Godot**
- Coding-Solo/godot-mcp: MIT, ~6.3k★, last push 2026-04-16, 75 issues. Tools: `launch_editor`, `run_project`, `get_debug_output`, `create_scene`, `add_node`, `load_sprite`, `save_scene`, `export_mesh_library` and UID tools. It has no frame or video capture — [README](https://github.com/Coding-Solo/godot-mcp); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Coding-Solo%2Fgodot-mcp) (Documented)
- ee0pdt/Godot-MCP: ~615★, last push 2025-03-19 (inactive) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/ee0pdt%2FGodot-MCP)
- AI-osho/godot-mcp-loop ("record GIFs", 0★, created 2026-10-17) and Erodenn/godot-mcp-runtime (95★) — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=godot); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Erodenn%2Fgodot-mcp-runtime)

**Krita / GIMP**
- cyyprezz/krita-codex-mcp: MIT, 10★, "Control Krita through a secure local MCP server and authenticated Windows bridge", built for OpenAI Codex. It is the only Krita entry in the official registry — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=krita); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/cyyprezz%2Fkrita-codex-mcp)
- maorcc/gimp-mcp: GPL-3.0, ~190★, last push 2026-05-29 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/maorcc%2Fgimp-mcp)

**Open compositors / After Effects alternatives (no MCPs found)**
- Natron: GPL-2.0, ~5.6k★, last push 2026-07-24, 290 issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/NatronGitHub%2FNatron). Natron has Python scripting and a command-line renderer (NatronRenderer) — [Natron docs](https://natron.readthedocs.io/en/rb-2.5/devel/natronexecution.html) (Documented; not re-fetched this session)
- Friction: GPL-3.0, ~1.8k★, last push 2026-09-17, 171 issues — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/friction2d%2Ffriction)
- Glaxnimate (KDE, GPL-3.0) has Python bindings on PyPI that run headless via `glaxnimate.environment.Headless()` and load/export Lottie and SVG. Search results did not confirm a video export path — [PyPI glaxnimate](https://pypi.org/project/glaxnimate/) (Documented, partial)

**NLE / paid-tool MCPs**
- samuelgursky/davinci-resolve-mcp: MIT, ~3.7k★, last push 2026-10-23 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/samuelgursky%2Fdavinci-resolve-mcp)
- Dakkshin/after-effects-mcp: MIT, ~647★, last push 2026-04-01 (needs a paid After Effects install) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Dakkshin%2Fafter-effects-mcp)
- OpenCut (open CapCut alternative): MIT, ~96.5k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/OpenCut-app%2FOpenCut)
- MLT framework: LGPL-2.1, active — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/mltframework%2Fmlt)

### Inferences
- **ComfyUI on the laptop is the one GPU automation target worth the effort.** Its HTTP API (`/prompt`, `/history`, `/view`, `/free`) is what every MCP wraps. Option 1: install artokun/comfyui-mcp or Comfy-Org comfy-mcp in a Claude Code session running on the laptop itself. Option 2: have the cloud agent call the HTTP API through an authenticated tunnel (Q6). artokun's VRAM tools fit a 4 GB RTX 3050.
- WAN/LTX video packs exist, but the earlier report already ruled out AI video on a 4 GB card (30 min to 6 h per clip, morphing). Use these MCPs for **stills, character sheets and inpainting**, not motion.
- **Natron** is the only mature open node compositor with a CLI renderer, but it would duplicate our NumPy satsuei pass. **Friction** and **Glaxnimate** are GUI vector animators and give an agent no advantage over code. **DaVinci Resolve** and **After Effects** MCPs need GUI desktop apps on Windows and are irrelevant to the headless server.
- **Godot** is not a fit for offline anime rendering here (headless disables rendering, and no MCP captures frames).

### Gaps
- Whether Comfy-Org's local comfy-mcp can target a non-local ComfyUI (the docs don't say).
- Friction's scripting/CLI story was not researched.
- Whether Glaxnimate's Python API can export a raster frame sequence was not confirmed.
- Natron's 2026 release state was not checked.

## 4. Skills registries and plugin marketplaces: animation, video editing, storyboarding, character sheets, sprites, lip sync, sound design

### Takeaway
General-purpose registries are large, but they hold few animation-specific skills, and those are low-adoption. Searches on 30 Oct 2026 of the official MCP registry and claude-plugins.dev returned:

| Area | What exists |
|---|---|
| Lip sync, storyboard, Lottie, Live2D | 0 MCP servers |
| Sprite | 13 entries, mostly paid SaaS pixel-art generators |
| Storyboard | A handful of skills with 0-268 stars |
| Animation / motion | Official vendor skills: GSAP, Remotion, HyperFrames, Comfy |

The most useful "skill" for our mouth animation is not a skill at all. It is the long-standing CLI Rhubarb Lip Sync.

### Cited findings
**Registries and marketplaces**
- Official MCP registry: queried via its public API on 30 Oct 2026 (Documented listings) — [registry API](https://registry.modelcontextprotocol.io/v0/servers?search=animation); repo modelcontextprotocol/registry ~7.4k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/modelcontextprotocol%2Fregistry). Results by keyword:
  - "animation" returned 4 servers, including animation-machine ("Render AI-written HTML animations to MP4/GIF with music, voiceover and captions", MIT, 0★).
  - "video" returned 15+, mostly SaaS. One, `app.filmee/anime-video`, is a closed service: "Turn a one-line story idea into a narrated anime video".
  - "sprite" returned 13, mostly paid generators: gensprite, spritecook, sprite-ai, spritefuse.
  - "spine" returned `top.lain42/spine-render` ("Render Spine 3.8 skeleton animations to PNG frames or GIF. Pay per call").
  - "lottie", "storyboard", "lip sync", "live2d" and "remotion" returned 0 each.
- claude-plugins.dev API, queried 30 Oct 2026 (Documented listings) — [animation](https://claude-plugins.dev/api/skills?q=animation); [storyboard](https://claude-plugins.dev/api/skills?q=storyboard); [sprite](https://claude-plugins.dev/api/skills?q=sprite); [lip](https://claude-plugins.dev/api/skills?q=lip):
  - "animation" returned mostly HTML slides/UI skills plus `greensock/gsap-skills/gsap-core` (official GSAP, 34 installs) and `threejs` (86 installs).
  - "storyboard" returned `storyboard-manager` (268★ repo, 86 installs) and LikeRainDay's film-storyboard, storyboard-review and "Animator Skill" (0★, 14-22 installs).
  - "sprite" returned willibrandon's pixel-art plugin (15★) and openai/skills `hatch-pet` (animated pet sprites for Codex).
  - "lip" returned only Seedance and Veo video-generation wrappers and no lip-sync skill.
- The Anthropic plugin directory `anthropics/claude-plugins-official`: Apache-2.0, ~45k★, last push 2026-10-28 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/anthropics%2Fclaude-plugins-official). Anthropic's skills repo installs via `/plugin marketplace add anthropics/skills` — [README](https://github.com/anthropics/skills) (Documented)
- Awesome lists (curation, not quality checks):
  - ComposioHQ/awesome-claude-skills ~78k★ (1,865 open issues) — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/ComposioHQ%2Fawesome-claude-skills)
  - travisvn/awesome-claude-skills ~15.6k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/travisvn%2Fawesome-claude-skills)
  - hesreallyhim/awesome-claude-code ~56.5k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/hesreallyhim%2Fawesome-claude-code)
  - punkpeye/awesome-mcp-servers ~96.9k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/punkpeye%2Fawesome-mcp-servers)
- The skills CLI `vercel-labs/skills` (`npx skills`): MIT, ~36.4k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/vercel-labs%2Fskills) (Documented)
- A third-party directory claims to grade "382" Claude video skills. It names ClaudeAnimationBase, PDoomVideo and hyperframes among the top. Its methodology is not verifiable — [agentskillshub](https://agentskillshub.top/best/claude-video-skills/) (Secondary)
- Glama's MCP directory API needs an API key, so it was not searched — [glama.ai](https://glama.ai/mcp/servers/udhkgzgr6o) (Gap)

**Lip sync and character tools**
- Rhubarb Lip Sync, "a command-line tool that automatically creates 2D mouth animation from voice recordings" (Documented, [README](https://github.com/DanielSWolf/rhubarb-lip-sync)):
  - Runs on Windows, macOS and Linux.
  - Outputs mouth shapes A-F plus G, H and X (idle). A Preston Blair mapping exports `.dat` for Moho/OpenToonz.
  - Two recognizers: PocketSphinx (English only) and a language-independent "Phonetic" one, whose results are "usually less precise".
  - Output formats are TSV, XML and JSON. It is multithreaded, one thread per core by default.
  - The README does not state the licence; the mirror lists it as "other". ~2.7k★, last push 2026-06-16 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/DanielSWolf%2Frhubarb-lip-sync).
- TalkingHead (3D, JS, real-time lip-sync for full-body avatars): MIT, ~1.6k★, last push 2026-10-11 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/met4citizen%2FTalkingHead) (Documented)
- claude-code-video-toolkit ships skills for `elevenlabs` (voice), `acestep` (music), `ltx2` (video) and SadTalker/SoulX talking heads, all on rented cloud GPUs (Q5) — [README](https://github.com/digitalsamba/claude-code-video-toolkit) (Documented)

### Inferences
- There is no registry skill that would make our anime look better. The useful vendor skills (Remotion, HyperFrames, GSAP, Comfy) teach Claude a framework's API, not art direction.
- A **project-local skill** written from our own anime-pipeline report would encode more value than anything in the registries: timing on 2s/3s, satsuei pass, the character-sheet rules, Rhubarb mouth mapping. This is what Anthropic's `skill-creator` is for.
- Rhubarb's English recognizer plus its JSON output maps directly onto our 3-mouth puppet. It replaces a loudness-envelope heuristic with phoneme-timed shapes, and closes the mouth on m/b/p ("A" shape) as our report asked. Hindi or Hinglish narration would need the less precise phonetic mode.
- **Sound design**: no dedicated skill was found. The music/SFX path stays our own code or an ElevenLabs/ACE-Step skill.

### Gaps
- Smithery and mcp.so were not searched directly (Smithery returned only one Motion Canvas skill in web search).
- No character-design-sheet or turnaround skill was found apart from paid sprite SaaS.
- Rhubarb's exact licence text was not confirmed.

## 5. Published agent workflows for AI animation pipelines (LLM orchestrating tools): results and honest limits

### Takeaway
2026 brought several large open-source "agentic video" systems built around Claude Code: OpenMontage (AGPL-3.0), claude-code-video-toolkit (MIT), video-use (MIT), FireRed-OpenStoryline (Apache-2.0) and video-shotcraft. Their published outputs are explainers, promos, documentaries and edits of real footage. The one "animated short" OpenMontage showcases used paid Kling v3 video clips. I found no published case of an LLM agent producing consistent, character-driven anime episodes from code alone. The research literature (TheoremExplainAgent, Code2Video, BlenderGym, OmniManim) consistently reports layout and spatial errors that need a render-look-fix loop and human review.

### Cited findings
**OpenMontage**
- "Turn your AI coding assistant into a full video production studio … There is no code orchestrator. Your AI coding assistant IS the orchestrator."
- Pipelines include Animated Explainer, Animation, Cinematic, Hybrid, Talking Head, Localization & Dub and others. It renders with Remotion and HyperFrames ("SVG character rigs") plus FFmpeg; TTS uses Piper (free) or ElevenLabs and others. ComfyUI is used for local WAN; Blender appears only in one showcase.
- Without a video-generation provider, "the agent produces still images and Remotion animates them".
- Examples: "THE LAST BANANA", a 60 s animated short made with Kling v3 clips for $1.33 total, and "OBJECTS IN OVERDRIVE", a 54 s Blender Eevee/Cycles showcase.
- Local LLM support is "Coming soon". Windows `npm install` can fail with `ERR_INVALID_ARG_TYPE`.
- AGPL-3.0, ~72.9k★, created 2026-03-29, last push 2026-10-28, 419 issues — [README](https://github.com/calesthio/OpenMontage); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/calesthio%2FOpenMontage) (Documented / Claim for costs)

**digitalsamba/claude-code-video-toolkit**
- "AI-native video production toolkit for Claude Code". Remotion is the main renderer, and Python/moviepy is used for 9:16 shorts.
- Skills: remotion, elevenlabs, ffmpeg, moviepy, runpod, ltx2, acestep, qwen-edit.
- AI tools run on cloud GPUs (Modal recommended, "$30/month free compute"). Listed per-use costs: SadTalker ~$0.10, LTX-2 clip ~$0.23.
- Examples include a 52 s "sky-blue-short" explainer (~$0.80) and a 3:41 vertical explainer.
- The author's own caveat: "a lofty ideal for such a subjective field, but we can try :)"
- MIT, ~2.3k★, last push 2026-10-21 — [README](https://github.com/digitalsamba/claude-code-video-toolkit); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/digitalsamba%2Fclaude-code-video-toolkit) (Documented)

**browser-use/video-use**
- Edits existing footage: "Drop raw footage in a folder, chat with Claude Code, get final.mp4 back."
- "The LLM never watches the video. It reads it", from ElevenLabs Scribe transcripts plus on-demand filmstrip and waveform images.
- Animation overlays come from HyperFrames, Remotion, Manim or PIL, one parallel sub-agent each, with up to 3 fix-and-re-render passes.
- Requires an ElevenLabs key. MIT, ~29.7k★, created 2026-04-12 — [README](https://github.com/browser-use/video-use); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/browser-use%2Fvideo-use) (Documented)

**Other workflows**
- FireRedTeam/FireRed-OpenStoryline (agentic editing): Apache-2.0, ~3.6k★, last push 2026-07-31 — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/FireRedTeam%2FFireRed-OpenStoryline)
- Agentchengfeng/chengfeng-videocut-skills ("video-editing agent built with Claude Code Skills"): Apache-2.0, ~3.2k★ — [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/Agentchengfeng%2Fchengfeng-videocut-skills) (Documented)

**Research evidence**
- TheoremExplainAgent: an agentless approach "fails to generate videos longer than 20 seconds", while agents reach 10 minutes. Problems remain: misaligned text, overlapping shapes, invalid API calls, and RAG on docs that "proved inconsistent in practice" — [arXiv 2502.19400](https://arxiv.org/html/2502.19400) (Study)
- Code2Video adds a Critic agent that looks at rendered frames and improves layout scores (self-reported) — [arXiv 2510.01174](https://arxiv.org/pdf/2510.01174) (Study)
- A 2026 paper on OmniManim lists limits in "short-horizon keyframes, richer typography, camera motion, and long-range narrative planning" and says human review is still needed — [arXiv 2605.15585 (search summary)](https://arxiv.org/pdf/2605.15585) (Study, via search summary)
- BlenderGym finds VLMs far below humans at 3D editing, and VIGA shows interleaved look-and-edit helps — [arXiv 2504.01786](https://arxiv.org/pdf/2504.01786); [arXiv 2601.11109](https://arxiv.org/pdf/2601.11109) (Study)
- Searches for HN/Reddit showcases of a Claude-agent-made animated character short returned none. One directory mentions an unnamed plugin making "animated short films where each frame is drawn in code", with no linked source — [search results](https://agentskillshub.top/best/claude-video-skills/) (Gap/Secondary)

### Inferences
- The common pattern that works is the one our pipeline already uses: a script as the source of truth, deterministic renderers, TTS, Whisper-style transcript checks, and a render → look at frames → fix loop. The new frameworks mostly package that pattern with React/HTML renderers and paid generative APIs.
- **OpenMontage's AGPL-3.0.** Using it internally to make YouTube videos is not distributing software, so the AGPL's source-sharing duties would apply only if we offered it to others as a network service. Still, copying its code into our repo would bring AGPL obligations into our code (Inference, not legal advice).
- **The quality gap for "anime" is art, not orchestration.** None of these systems solves character consistency without either reused layered art (our approach) or paid video models. Adopt individual parts (Rhubarb, HyperFrames/Remotion blocks, a Critic-style frame review) rather than a whole framework.

### Gaps
- No independent quality reviews or retention data for videos made with these frameworks.
- I did not watch the showcase videos, so their visual quality is unassessed.
- No published workflow targets anime-style monster/character series specifically.

## 6. Connecting the cloud agent to the owner's Windows GPU laptop securely (documented routes only)

### Takeaway
The documented, no-open-ports route is Claude Code's own **Remote Control** plus **cross-session messaging**. The owner runs `claude remote-control` on the laptop, which "makes outbound HTTPS requests only and never opens inbound ports". A laptop session there runs ComfyUI (or a ComfyUI MCP) locally, and this cloud session sends it jobs as messages. Files move through the git branch. Messaging works on native Windows (Claude Code v2.1.234+), but a cloud session "can't use SendMessage to answer a message from another machine". This session's folder-attach feature accepts only Mac or Linux folders, so it can't attach a native Windows folder. A direct network link (Tailscale in userspace mode, or a cloudflared tunnel with a token) is possible in principle but must pass this environment's outbound-domain policy. That route is unverified here.

### Cited findings
**Remote Control**
- "Remote Control sessions run directly on your machine and interact with your local filesystem … your computer has to stay on and the `claude` process has to keep running." It is available on Pro, Max, Team and Enterprise plans. "API keys are not supported." — [Remote Control docs](https://code.claude.com/docs/en/remote-control) (Documented)
- Security: "Your local Claude Code session makes outbound HTTPS requests only and never opens inbound ports on your machine … All traffic travels through the Anthropic API over TLS … multiple short-lived credentials." Optional Trusted Devices requires a sign-in under 18 hours old, confirmed with Windows Hello, a passkey and so on — [Remote Control docs](https://code.claude.com/docs/en/remote-control) (Documented)
- Server mode (`claude remote-control`) serves up to 32 concurrent sessions by default (`--capacity`). It can spawn each session in its own git worktree (`--spawn worktree`). After a ~10-minute network outage the process exits — [Remote Control docs](https://code.claude.com/docs/en/remote-control) (Documented)
- A Windows 11 bug report (v2.1.69, Mar 2026) said `/rc` was unavailable; it is marked resolved — [claudeissues](https://claudeissues.com/issue/30976-remote-control-rc-feature-not-available-windows-11-claude-code-v2-1-69) (Secondary)

**Cross-session messaging**
- Requirements: "Cross-session messaging requires Claude Code v2.1.224 or later on macOS and Linux, including Linux inside WSL 2. On native Windows, it requires Claude Code v2.1.234 or later." — [cross-session messaging docs](https://code.claude.com/docs/en/cross-session-messaging) (Documented)
- Routing: a message to a session "On another of your machines" goes "Through Anthropic servers, arriving over that machine's Remote Control connection", and to "In the cloud … straight to the cloud session" — [cross-session messaging docs](https://code.claude.com/docs/en/cross-session-messaging) (Documented)
- Limits — [cross-session messaging docs](https://code.claude.com/docs/en/cross-session-messaging) (Documented):
  - "A cloud session … can't use SendMessage to answer a message from another machine … Read the cloud session's response in its transcript."
  - Messages are "Plain text only".
  - "A session inside WSL 2 and a native Windows session on the same computer can't reach each other."
  - The receiving session's own permission prompts still apply, and a message "can't approve anything".
- This session's own tool documentation for attaching a computer folder (`list_computer_folders` / `request_computer_folder`) says: "A folder can be used only if it is the root of a Git repository … and is on a Mac or Linux computer." (Documented in-session tool description; no public URL.) The Claude Code docs describe a related project feature to "run a thread on your own computer" — [Remote Control docs, comparison table](https://code.claude.com/docs/en/remote-control) (Documented)

**This cloud environment's network policy**
- Outbound hosts are controlled by the environment's "Network access" setting (a broader level, or hosts added under "Allowed domains") — [cloud environments docs](https://code.claude.com/docs/en/cloud-environments#network-access) (Documented)
- This container reaches the internet through an HTTPS agent proxy. In this session, direct GitHub API calls were refused (Observed).

**Tunnels**
- Tailscale userspace networking runs "without access to create a VPN tunnel device, which is common in containers". `tailscaled` then acts as a SOCKS5/HTTP proxy that other processes use (`--tun=userspace-networking`). Tailscale says the mode is primarily for serverless environments — [Tailscale userspace networking](https://tailscale.com/docs/concepts/userspace-networking) (Documented)
- Tailscale's free-plan limits were not confirmed from a primary source. One secondary page says "1 user … 20 devices" — [wener.me notes](https://wener.me/notes/service/network/vpn/tailscale) (Secondary, possibly outdated)
- tailscale/tailscale is BSD-3 and cloudflare/cloudflared is Apache-2.0, both active in Oct 2026 — [ecosyste.ms tailscale](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/tailscale%2Ftailscale); [ecosyste.ms cloudflared](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/cloudflare%2Fcloudflared) (Documented)
- artokun/comfyui-mcp's `--tunnel` mode creates a cloudflared quick tunnel with a generated auth token (Bearer/X-API-Key). ChristopherGoodale/comfy_mcp binds ComfyUI to the Tailscale IP with a tailnet-only firewall rule because "ComfyUI itself has no authentication" — [artokun README](https://github.com/artokun/comfyui-mcp); [comfy_mcp](https://github.com/ChristopherGoodale/comfy_mcp) (Documented)

### Inferences
**Recommended setup (lowest risk, documented pieces only):**
1. On the laptop, install Claude Code and keep the owner's own git clone of this repo.
2. Run `claude remote-control` there, with ComfyUI started locally (`--listen 127.0.0.1`, never exposed).
3. This cloud session messages the laptop session a job, e.g. "generate the 6 Animagine stills in `jobs/ep01.json`, push PNGs to branch X".
4. The laptop session runs ComfyUI (through comfy-mcp, artokun/comfyui-mcp or a plain script) and pushes the results.
5. The cloud session pulls from git.

This needs no inbound ports and no new network allow-list entry. Its limits: the laptop must be on with `claude` running, replies come back through git or the transcript rather than SendMessage, and every message is plain text.

**Direct API route (not recommended first):**
- Expose ComfyUI through a cloudflared named tunnel protected by a token or service token, then add that hostname to this environment's Allowed domains.
- Alternatively, run `tailscaled --tun=userspace-networking` inside the container. Whether Tailscale's control plane and DERP relays work through the agent's HTTPS proxy is untested. ComfyUI has no auth, so a quick tunnel with no token must never be used.
- WSL 2 might let the laptop qualify as a "Linux computer" for this session's folder-attach tool. This is unverified, and the docs say WSL 2 and native Windows sessions can't message each other.

### Gaps
- Not tested from this container: whether Tailscale userspace mode or a cloudflared hostname is reachable through the agent proxy, which depends on the environment's network-access level.
- Whether this cloud session's ListAgents can see a Windows Remote Control session in practice; the docs suggest yes but I did not try it.
- The current Tailscale free-plan device limit (primary pricing page not fetched).
- Whether a folder inside WSL 2 can be attached with `request_computer_folder`.
