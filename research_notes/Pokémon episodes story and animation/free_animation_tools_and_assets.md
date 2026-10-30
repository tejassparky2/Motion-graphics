# Free and open tools, assets and models for TV-anime character animation (as of 30 Oct 2026)

Scope: what to add to the current Blender 4.5 LTS headless, CPU-only pipeline (toon Shader-to-RGB materials, inverted-hull outlines, painted backgrounds, SDF creatures, Python keyframing) so that the HUMAN hero (a 19-year-old anime boy) and character ACTING (faces, hands, running, falling, emotion) approach a Pokémon-TV-anime look. This builds on, and does not repeat, `reports/CPU anime animation pipeline.md` (27 Oct; AI stills + 2.5D puppets, satsuei, anime timing, AI-video timings) and `reports/Monster tamer anime pipeline and hooks.md` (30 Oct; Cycles farm, CC0 kits, MCP survey). Where a fact from those reports is reused, it is cited to the original source they cite.

Evidence labels: **[measured here]** = checked in this session on the cloud container on 30 Oct 2026. **[earlier report]** = measured or sourced in the two reports above. **[estimate]** = this researcher's inference. **UNVERIFIED** = a version, price or licence that could not be confirmed from a primary source in this pass.

Session facts **[measured here]**: the root disk had **2.4 GB free** (`df -h /`), and **no `blender` binary was found** on PATH or within four directory levels of `/`, so nothing below was render-tested in this session. Adobe's helpx pages returned HTTP 403 to both WebFetch and curl, so the Mixamo FAQ is cited through search-engine extracts and the earlier notes.

## 1. Anime human characters: VRoid Studio + VRM Add-on, and the alternatives

### Takeaway
VRoid Studio is the strongest free route to an anime human: a model you build there may be used in monetized videos, its VRM export carries the standard anime expression set (5 emotions, 5 visemes, blinks, look), and the VRM Add-on for Blender (MIT or GPL-3, scriptable via `bpy.ops.import_scene.vrm`) officially supports Blender 4.2 LTS up to (not including) 5.3. VRoid Studio itself runs only on Windows/macOS/iPad, so the hero is authored on the owner's laptop and the exported `.vrm` is animated and rendered headless on the container (the headless import itself is UNVERIFIED, not yet tested here). MPFB2 (CC0 assets) and AccuRIG are fallbacks; free "anime base meshes" are mostly not licence-clean.

### Cited Findings
**VRoid Studio licence (official guidelines, edited 21 Dec 2023)**
- "The copyright and other rights for textures and hair meshes you created from scratch on VRoid Studio or other tools belong to you, the creator." Preset meshes and items stay pixiv's and "is not CC0", but pixiv licenses them "for as wide a range of purposes as possible" — [VRoid Studio Guidelines](https://vroid.com/en/studio/guidelines)
- "Any individual or corporation may sell or use for commercial purposes any mesh, texture, or preset item provided by VRoid Studio … provided that no special clauses are indicated in the license", including "You can use images and videos of models created with VRoid Studio and generate profit from videos" and "for-profit appearances in shows" — [VRoid Studio Guidelines](https://vroid.com/en/studio/guidelines)
- Restrictions: items with "special licensing terms" and sample models have their own conditions; you may not build an application that generates/outputs models from VRoid meshes without a separate licence (personal-only tools excepted); do not produce videos that imply collaboration with or backing by pixiv/VRoid; no reverse engineering — [VRoid Studio Guidelines](https://vroid.com/en/studio/guidelines)
- Models made by OTHER people on VRoid Hub carry per-model licence fields (separate corporate and personal commercial-use settings), so third-party VRoid models must be checked one by one — [VRoid developer: conditions of use](https://developer.vroid.com/en/guidelines/conditions_of_use.html) (via search extract)

**VRoid Studio platform**
- Official downloads: Steam, Windows and macOS installers, iPad (App Store). Windows requirement: Windows 8.1/10/11, Core i5 6th gen / Ryzen 5 3rd gen, 8 GB RAM, Intel Iris 540 or better; 10 GB storage — [vroid.com/en/studio](https://vroid.com/en/studio). No Linux build is listed.
- A community MCP project reports VRoid Studio 2.14.0 running under Steam/Proton on Arch Linux + Hyprland (Wayland) — [mcp-vroid README](https://github.com/nhodges/mcp-vroid); a third-party Steam aggregator says it is "not playable on Linux" — [wasdland](https://www.wasdland.com/game/vroid-studio-1486350/). Conflicting, non-official; ProtonDB not checked (UNVERIFIED).
- The owner's laptop (i7-11600H, 16 GB, RTX 3050) exceeds the stated Windows requirements — [vroid.com/en/studio](https://vroid.com/en/studio) [comparison: estimate]

**VRM format: expressions, hands, licence metadata**
- VRM 1.0 preset expressions: emotions `happy`, `angry`, `sad`, `relaxed`, `surprised`; visemes `aa`, `ih`, `ou`, `ee`, `oh`; `blink`, `blinkLeft`, `blinkRight`; `lookUp`/`lookDown`/`lookLeft`/`lookRight`; plus `neutral` for backward compatibility. Expressions can bind morph targets (`MorphTargetBind`), material colours (`MaterialColorBind`) and texture transforms (`TextureTransformBind`) — [VRM 1.0 expressions spec](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md)
- VRM files carry licence metadata (e.g. `commercial_usage` = personalNonProfit / personalProfit / corporation, `credit_notation`, `allow_redistribution`, `modification`) that the add-on exposes to Python — [VRM Add-on scripting API](https://vrm-addon-for-blender.info/en-us/scripting-api/)

**VRM Add-on for Blender (saturday06)**
- Dual-licensed MIT or GPL-3.0; "VRM Importer, Exporter and Utilities for Blender 2.93 to 5.2"; adds VRM import, export, VRM Humanoid, MToon shader configuration, and "an API for automation via Python scripts" (PyPI package `bpy-vrm-format`) — [GitHub](https://github.com/saturday06/VRM-Addon-for-Blender)
- On the official Extensions platform: version **4.10.3**, updated the day before this check, 326,089 downloads, 1.6 MB, compatibility "Blender 4.2 LTS", "Unsupported 5.3 and above" — [extensions.blender.org/add-ons/vrm](https://extensions.blender.org/add-ons/vrm/) [read here 30 Oct 2026]
- Scripted import/export: `bpy.ops.import_scene.vrm(filepath=...)` and `bpy.ops.export_scene.vrm(...)` return `{"FINISHED"}` on success — [scripting API](https://vrm-addon-for-blender.info/en-us/scripting-api/)
- VRM Animation (`.vrma`) export needs a VRM 1.0 armature and carries humanoid bone rotations, hips translation and expression preview values (Look At not yet exported) — [VRM Animation docs (JA)](https://vrm-addon-for-blender.info/en-us/animation/)
- MToon ("anime-style material") is set per material ("Enable VRM MToon Material"); the tutorial tells users to set View Transform to **Standard**, otherwise colours render darker — [MToon tutorial](https://vrm-addon-for-blender.info/en-us/material-mtoon/). The repo's own CI/dev scripts pin `blender_version=4.5` — [README](https://github.com/saturday06/VRM-Addon-for-Blender)
- Spring-bone (hair/cloth jiggle) simulation inside Blender is not described on the pages read — UNVERIFIED.

**Alternatives**
- **MPFB2** (MakeHuman for Blender): "a free and open source human generator for Blender", requires Blender ≥ 4.2; code GPL-3, **assets CC0 1.0** — [GitHub](https://github.com/makehumancommunity/mpfb2); [LICENSE.ASSETS.md](https://github.com/makehumancommunity/mpfb2/blob/master/LICENSE.ASSETS.md); on the Extensions platform with ~243K downloads — [extensions search](https://extensions.blender.org/search/?q=mpfb). Rig types and face-expression support were not confirmed on the pages read (UNVERIFIED). No anime style option was found.
- **Reallusion AccuRIG 2.0** (Jul 2025): free, Windows 8+, exports rigged characters (full body + fingers) to FBX/USD; a free ActorCore account is required even for local export; ActorCore motions can be used only inside AccuRIG (32 free of 4,500+) — [CG Channel](https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/); rigs are usable commercially and characters keep their own licence — [Reallusion forum](https://forum.reallusion.com/551972/reallusion-Accu-Rig-Free) (staff answer, cited in earlier notes)
- **Rigify** (bundled): meta-rigs include Human, Basic Human (no face/fingers), Basic Quadruped, Cat, Wolf, Horse, Shark — [Blender manual source](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/addons/rigify/basics.rst)
- **Blender Studio Human Base Meshes**: free under **CC0**, stylised and realistic male/female bodies and parts, as a .blend — [CG Channel](https://www.cgchannel.com/2023/06/download-blender-studios-free-human-base-meshes)
- Free "anime" base meshes found were not CC0: a free Genshin-style female base is CC BY (credit required) — [Gumroad listing](https://downloadforfree.gumroad.com/l/free-genshin-style-anime-female-base-mesh-for-blender-3d-model); a free Superhive "Basemesh Pack – Free Edition" is personal / non-commercial only — [Superhive docs](https://superhivemarket.com/products/basemesh-pack-free-edition-character-related-models/docs) (both via search extract)
- **UniRig** (AI auto-rigging: skeleton + skinning prediction): MIT; current checkpoint trained on Articulation-XL2.0; the full model trained on Rig-XL/VRoid is still "⏳" pending; install needs CUDA builds of spconv and torch_scatter/cluster — [GitHub README + LICENSE](https://github.com/VAST-AI-Research/UniRig). GPU-only in practice [estimate].

### Inferences
- **Laptop → container hand-off works on paper [estimate]:** the owner designs the hero in VRoid Studio on Windows (sliders + hair-guide drawing; 1-3 evenings for a first version, estimate), exports `.vrm`, commits it (VRoid exports are typically tens of MB; size not measured) and the container imports it with `blender -b -P import.py` using the add-on's documented operator. Expressions come in as shape keys/expression slots, so the existing Python keyframer can drive `happy`/`surprised`/`aa..oh`/`blink` directly. First test to run: `blender -b --python-expr` import of one VRoid sample-free `.vrm`, then one EEVEE frame.
- **Blender version pinning:** stay on 4.5 LTS for VRM work; the add-on's own metadata marks 5.3+ unsupported today.
- **MToon → our toon [estimate]:** keep VRoid's base-colour and shade textures and MToon's shade colour, but rebuild each material as the pipeline's Shader-to-RGB ramp (hard 1-2 step terminator, HSV-derived shadow colour, no ink on shadow edges, per the earlier report's anime rules) so the hero matches the creatures and backgrounds. Keep MToon only for quick previews.
- **Quality ceiling:** VRoid gives a convincing anime face, hair and proportions out of the box, which is exactly the current weak point; the risk is a recognisable "default VRoid" face. Mitigate with custom eye/hair textures and the owner's own hair guides (textures and hair meshes made from scratch belong to the owner per the guidelines).
- **Licence hygiene:** set the VRM metadata on export (author = owner, commercialUsage = personalProfit or corporation), avoid VRoid items flagged with special clauses, and never use other people's VRoid Hub models unless their per-model licence allows profit use.
- MPFB2/Blender Studio bases are licence-cleanest (CC0) but would need sculpting into an anime face; AccuRIG is a Windows-side rigging fallback only. For this project VRoid wins on time-to-anime-look.

### Gaps
- Not tested here: headless (`-b`) VRM import in Blender 4.5.15, render cost of a VRoid character (hair cards + transparency) in EEVEE/llvmpipe, and whether spring bones can be baked headless.
- The pixiv Terms of Use Article 11 (referenced by the guidelines) was not read directly.
- MPFB2 rig/expression features and AccuRIG's current EULA text not read from primary pages.
- VRoid on Linux: no official statement; ProtonDB rating not checked.

## 2. Motion sources and retargeting

### Takeaway
For a monetized channel the licence-clean motion sources are **Mixamo** (free with an Adobe ID, royalty-free commercial use, no raw-file redistribution), **CMU mocap** ("free for all uses") and **video mocap of the owner himself** with MediaPipe/FreeMoCap. Most AI text-to-motion models have permissive code licences (MIT/Apache) but were trained on AMASS/HumanML3D, whose licence forbids "production of other artefacts for commercial purposes", and the SMPL body model is non-commercial; treat their outputs as a legal grey zone. Several popular BVH sets (Bandai Namco, Ubisoft LAFAN1) are non-commercial. Retargeting onto a VRM rig can be done with Rokoko's free LGPL plugin or Keemap (GPL-3); MoMask's authors report Rokoko gives large foot error.

### Cited Findings
**Mixamo**
- Adobe's FAQ (as extracted by the search engine; direct fetch blocked with HTTP 403 here): Mixamo is "available free for anyone with an Adobe ID and does not require a subscription to Creative Cloud"; access is blocked for Enterprise and Federated IDs and for China country codes — [Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (via search extract)
- Characters and animations are "royalty free for personal, commercial, and non-profit projects"; raw files may not be redistributed — [Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (cited in earlier notes)
- A vendor guide (Sept 2026) says the FAQ was last updated 14 Sep 2021 and describes Mixamo as unmaintained since Adobe's 2015 purchase — [Cinevva](https://app.cinevva.com/guides/free-character-animations-rigging) (vendor with a stake in alternatives)

**Mocap libraries**
- CMU Graphics Lab: "This dataset of motions is free for all uses"; BVH conversions (3ds Max / MotionBuilder) hosted at cgspeed — [CMU mocap home](http://mocap.cs.cmu.edu/); "The motion capture data may be copied, modified, or redistributed without permission" — [CMU FAQ](http://mocap.cs.cmu.edu/faqs.php)
- Bandai Namco Research Motion datasets 1 and 2 (stylized BVH: 15 + 7 styles such as active, tired, happy; daily activities, fighting, dancing): **CC BY-NC 4.0** (non-commercial); only the Blender visualisation script is MIT — [GitHub README](https://github.com/BandaiNamcoResearchInc/Bandai-Namco-Research-Motiondataset)
- Ubisoft LAFAN1 (BVH): **CC BY-NC-ND 4.0** — [GitHub README](https://github.com/ubisoft/ubisoft-laforge-animation-dataset)

**AI text-to-motion**
- MoMask: code MIT; "depends on other libraries, including SMPL, SMPL-X, PyTorch3D, and uses datasets which each have their own respective licenses that must also be followed"; outputs joints `.npy`, MP4 stick figures and **BVH** (foot-IK version "sometimes will fail"); its WebUI demo runs on CPU ("No GPU is required to use MoMask", Aug 2024 news); recommends the keemap retargeting add-on with a bundled `mapping.json` and says Rokoko "usually leads to large error on foot" — [momask-codes](https://github.com/EricGuo5513/momask-codes)
- MDM: MIT — [motion-diffusion-model LICENSE](https://github.com/GuyTevet/motion-diffusion-model); T2M-GPT: Apache-2.0 — [T2M-GPT LICENSE](https://github.com/Mael-zys/T2M-GPT); MotionGPT: MIT — [MotionGPT LICENSE](https://github.com/OpenMotionLab/MotionGPT) [licence files read here]
- AMASS dataset licence: use only "for the sole purpose of performing non-commercial scientific research, non-commercial education, or non-commercial artistic projects"; "Any other use, in particular any use for commercial purposes, is prohibited. This includes … production of other artefacts for commercial purposes" — [AMASS licence](https://amass.is.tue.mpg.de/license.html)
- SMPL model licence: same non-commercial grant; commercial licensing via Meshcapade — [SMPL model licence](https://smpl.is.tue.mpg.de/modellicense.html)
- HY-Motion 1.0 (Tencent, released 30 Dec 2025): Tencent HY-Motion community licence "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"; licensees above 1 million MAU must request a licence; "Outputs by themselves are not deemed Model Derivatives" — [License.txt](https://github.com/Tencent-Hunyuan/HY-Motion-1.0/blob/master/License.txt); minimum VRAM 26 GB (1.0B) / 24 GB (0.46B Lite) per the model card — [HF model card](https://huggingface.co/tencent/HY-Motion-1.0) (via search extract); CGWORLD describes free commercial use — [CGWORLD](https://cgworld.jp/flashnews/01-202601-HY-Motion.html)

**Video-to-mocap**
- FreeMoCap: AGPL-3.0; installs "skellytracker with NVIDIA GPU acceleration on Windows/Linux, or CPU-only on macOS", with a CPU-only build for machines without a supported GPU — [freemocap](https://github.com/freemocap/freemocap)
- BlendArMocap: GPL-3, runs Google MediaPipe hand/face/pose detection inside Blender and transfers results to a generated Rigify rig (new Rigify face not supported); the author says he can no longer actively maintain it — [BlendArMocap LICENSE](https://github.com/cgtinker/BlendArMocap); [BlenderNation](https://www.blendernation.com/2022/06/08/blendarmocap-free-motion-capture-add-on-release-version/) (via search extract); MediaPipe itself is Apache-2.0 — [mediapipe LICENSE](https://github.com/google-ai-edge/mediapipe)
- 4D-Humans: code MIT (UC Regents) — [LICENSE.md](https://github.com/shubham-goel/4D-Humans), but it is built on SMPL (non-commercial, see above)
- GVHMR: "educational, research and non-profit purposes only … prohibited for commercial use" — [GVHMR LICENSE](https://github.com/zju3dv/GVHMR)

**Retargeting in Blender**
- Rokoko Studio Live for Blender: **LGPL-3.0** — [repo LICENSE](https://github.com/Rokoko/rokoko-studio-live-blender); Rokoko says retargeting "is not a paid feature" and needs no premium account — [Rokoko support](https://support.rokoko.com/hc/en-us/articles/4410463481489-Retarget-an-animation-in-Blender); a free Rokoko login is required to use the add-on — [BlenderNation guide](https://www.blendernation.com/2021/12/23/retargeting-using-rokoko-complete-guide/) (via search extract). Not on the Blender Extensions platform (0 results) [read here].
- Keemap rig retargeting add-on: GPL-3.0 — [repo LICENSE](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon)
- Expy Kit: GPL-3 (licence block in `__init__.py`), version 0.6.1, minimum Blender 2.90; converts Rigify to a single game hierarchy, restores Rigify naming after Unreal, renames bones to export to Mixamo, and constrains bones to another armature — [Expy-Kit](https://github.com/pKrime/Expy-Kit). Its compatibility with Blender 4.5 was not confirmed (has a `version_compatibility.py`; UNVERIFIED).
- "Retarget" (KBS-DEV) extension: GPL-3, v5.2.0, **Blender 5.0 and newer only** — [extensions.blender.org](https://extensions.blender.org/add-ons/retarget/); "Rig Bridge / Humanoid Remap Studio": GPL, v0.1.66 (Jul 2026), preset-first humanoid retargeting with topology fallback; its text says "Blender 5.1 or newer" while the page lists 4.2 LTS compatibility (conflict) — [extensions.blender.org](https://extensions.blender.org/add-ons/humanoid-remap-studio/)
- The VRM add-on can import `.vrma` VRM Animation onto a VRM 1.0 humanoid — [VRM Animation docs](https://vrm-addon-for-blender.info/en-us/animation/)

### Inferences
- **Motion stack for the hero [estimate]:** Mixamo for locomotion and stock acting (run cycles, stumbles, falls, hit reactions, idles, gestures) + CMU for extra athletic clips → retarget once to the VRM humanoid with Rokoko (fast, LGPL) or Keemap (scriptable bone map, better feet per MoMask) → store as Blender Actions in a library `.blend` → the Python keyframer layers them (NLA strips) and adds anime timing (hold key poses on 2s/3s, smear/impact frames). Everything after the Mixamo download is CPU-trivial and headless-friendly.
- **Bespoke acting [estimate]:** for beats no library has (e.g. "kneels, grabs his partner, looks up"), the owner films himself on the laptop webcam and runs a MediaPipe-based capture (FreeMoCap CPU build, or BlendArMocap); the motion is his own, and AGPL/GPL govern the software, not his recordings. Expect jitter; clean by keeping only key poses and re-timing on 2s/3s, which is how anime acting is timed anyway.
- **AI text-to-motion: avoid for monetized output for now.** Code licences are permissive, but the AMASS licence explicitly bars commercial artefacts and nobody has tested whether model outputs inherit that; HY-Motion (own licence) needs 24-26 GB VRAM, so neither the laptop (4 GB) nor the container can run it. MoMask on CPU is fine for previs only.
- Do not use Bandai Namco, LAFAN1, GVHMR or SMPL-based video mocap (4D-Humans etc.) in published videos.

### Gaps
- Mixamo FAQ full text could not be fetched (Adobe 403); the "no raw-file redistribution" and any AI/ML clauses rely on earlier notes and search extracts.
- FreeMoCap single-webcam quality and CPU speed were not measured; BlendArMocap compatibility with Blender 4.5 not confirmed.
- No legal opinion found on whether AMASS-trained model outputs are "artefacts" under its licence.
- Rokoko Vision (free web single-camera mocap) terms were not researched.

## 3. Anime-specific NPR in Blender

### Takeaway
No paid shader is needed. Goo Engine is a GPL Blender fork distributed through DillonGoo's Patreon and was still on Blender 4.1 in Dec 2024 (current status UNVERIFIED); Lightning Boy Shader ($30+) targets Blender 3.4 and is not usable on 4.5. Official Blender is absorbing NPR features piece by piece: Shader-to-RGB fixes (5.1, 5.2), a Raycast node (5.1) and, in **Blender 5.3 (beta until 4 Nov 2026)**, Material Lighting nodes explicitly meant for toon shading. On 4.5 LTS, the anime face is made with free techniques: custom normals transferred from a proxy, an SDF face-shadow texture, and expression/texture swaps for eyes and mouths. Grease Pencil Line Art runs from the camera in any engine but recomputes occlusion per modifier.

### Cited Findings
**Goo Engine and the NPR branch**
- DillonGoo Studios released Goo Engine in 2022 as "a custom build of Blender designed specifically for use in 3D anime production"; in Nov 2023 it launched "Emily", an anime-style 3D rig — [Wikipedia: DillonGoo](https://en.wikipedia.org/wiki/DillonGoo)
- 2023: GPL fork; compiled Windows/macOS binaries via Patreon at £4.50/month — [CG Channel 2023](https://www.cgchannel.com/2023/07/check-out-goo-engine-blender-for-anime) (price as of 2023; current price UNVERIFIED)
- Dec 2024: Goo Engine was based on Blender 4.1 (last legacy-EEVEE release); a 4.2 base was "difficult to get working"; DillonGoo works with Blender on an official NPR branch (free experimental builds for Windows, Linux, macOS) and estimated integration into master "could be two years" — [CG Channel Dec 2024](https://www.cgchannel.com/2024/12/check-out-blenders-experimental-non-photorealistic-rendering-build/)
- A community port of Goo Engine nodes and the NPR prototype (NPR Tree, Filter Materials, Render Textures) to Blender 5.1 exists; its author says it "was developed with AI and may contain unknown bugs or stability issues"; licence and Linux builds not stated (thread Mar-Jun 2026) — [BlenderArtists](https://blenderartists.org/t/porting-goo-engine-and-npr-prototype-to-blender-5-1/1635806)

**Official Blender 5.x**
- 5.1: new Raycast shader node "allows for a wide variety of effects, including NPR stylization", screen-space only in EEVEE; "Added transparency evaluation for Shader To RGB node"; max AOVs raised to 128 — [5.1 EEVEE notes](https://developer.blender.org/docs/release_notes/5.1/eevee/)
- 5.2: Light Probe Planes now compatible with Blended mode and Shader to RGB — [5.2 EEVEE notes](https://developer.blender.org/docs/release_notes/5.2/eevee/)
- 5.3 (in Beta "until November 4, 2026"): **Material Lighting nodes** "can, for example, be used for toon and stylized shading": Light Accumulation, Light Info, Light Evaluation, Shadow Raycast, Attribute (Light Mode), Vector Transform (Light Space); Vulkan becomes the default backend on Windows and Linux — [5.3 EEVEE notes](https://developer.blender.org/docs/release_notes/5.3/eevee/); [5.3 status](https://developer.blender.org/docs/release_notes/5.3/)
- Grease Pencil v3 (4.3): multithreaded, Geometry Nodes support, rewritten Python API — [4.3 GP notes](https://developer.blender.org/docs/release_notes/4.3/grease_pencil/); 5.0 adds GP **motion blur rendering** and Sharp/Flat stroke corners — [5.0 GP notes](https://developer.blender.org/docs/release_notes/5.0/grease_pencil/); 5.3 adds selection/editing in Draw Mode, a Carver tool and multi-region fill — [5.3 GP notes](https://developer.blender.org/docs/release_notes/5.3/grease_pencil/)

**Line tools**
- Line Art modifier: "generates stylized Line Art from a scene, collection, or object"; needs an active camera; "each Line Art modifier will run the entire occlusion calculation for itself", so several modifiers are much slower (a cache option exists for stacked modifiers) — [Blender 4.5 manual](https://docs.blender.org/manual/en/4.5/grease_pencil/modifiers/generate/line_art.html)
- In the 27 Oct test on this container, Cycles ignored the inverted-hull outline and scripted Freestyle produced no strokes; EEVEE + Shader-to-RGB + inverted hull worked with View Transform Standard — [earlier report](../../reports/CPU%20anime%20animation%20pipeline.md) [earlier report, measured]

**Paid shader**
- Lightning Boy Shader 2.1: $30+ on Gumroad, "Blender 3.4 / EEVEE"; listing says the current build is not compatible with Blender 3.5 and up — [Gumroad](https://lightningboystudio.gumroad.com/l/aYbiH) (title read directly; incompatibility via search extract)

**Anime face techniques**
- Custom normals for clean face shadows: a free video "PERFECT Anime/Toon Shading in Blender 4.0!" uses Data Transfer modifiers to define shadow zones — [BlenderNation Bazaar](https://bazaar.blendernation.com/listing/perfect-anime-toon-shading-in-blender-4-0/); a "Customizing Normals" series moves from Data Transfer to Geometry and Shader Nodes for stylized faces — [BlenderArtists](https://blenderartists.org/t/customizing-normals-tutorial-series/1369038); one Stack Exchange answer reports glitches with Data Transfer and suggests transferring from an edited mesh copy or the TiNA add-on — [Blender SE answer 251667](https://blender.stackexchange.com/a/251667) (read via mirror); Polycount practitioners note normal baking alone "falls flat" on faces — [Polycount](https://polycount.com/discussion/comment/2666647) (all via search extract)
- Paid option: Fondant Tools "Easy Custom Normals" (Blender 4.3-4.5) with an "Anime Face Proxy" curve rig driving Geometry-Nodes normals — [Gumroad](https://fondanttools.gumroad.com/) (via search extract; price UNVERIFIED)
- SDF face shadow maps: hand-paint shadow thresholds over the face UVs, bake/merge into one SDF texture, then threshold it by light angle — [Notion workflow guide](https://erichu33.notion.site/Face-Shadow-Map-Creation-Baking-Workflow-d3b8769021e04683a2f2ae4cf16ac810); a Japanese lilToon write-up builds one with an SDF tool and Blender — [scrapbox](https://scrapbox.io/onigiri-tiken/%E3%80%90Unity%E3%80%91%E3%82%B7%E3%82%A7%E3%83%BC%E3%83%80%E3%83%BC%EF%BC%9AlilToon%E3%81%A7SDF%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E9%A1%94%E5%BD%B1); a paid BOOTH "Face Shadow SDF Generator" bakes from FBX — [BOOTH](https://milktank-booth.booth.pm/items/8245542) (via search extract). No Blender-native free tutorial was found.
- Eye/mouth swaps: VRM expressions can drive texture transforms and material colours as well as shape keys — [VRM 1.0 expressions spec](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md); Rhubarb Lip Sync (MIT) outputs mouth-shape JSON — [Rhubarb](https://github.com/DanielSWolf/rhubarb-lip-sync)

### Inferences
- **Stay on 4.5 LTS for production; trial 5.3 later [estimate].** Everything the hero needs (Shader-to-RGB ramp, SDF face shadow via a light-direction driver, custom normals, inverted hull) works on 4.5. 5.3's Material Lighting nodes would make per-light toon terminators and light-space SDF lookups native, but it is a beta, the VRM add-on marks 5.3 unsupported, and 5.3's Vulkan-default on Linux may need `--gpu-backend opengl` on this Vulkan-less container (UNVERIFIED).
- **Face recipe (CPU-free at render time) [estimate]:** (1) transfer normals from a sphere/ellipsoid proxy onto the face so the terminator moves as one clean shape; (2) an SDF shadow texture sampled in the face material, thresholded by the dot of head-forward and light direction (driver from the key light), for the classic "nose-shadow triangle" anime look; (3) eyes as separate textured planes or texture-swapped materials (iris + highlight layers; the earlier report's eye stack), mouth as 3-5 texture or shape-key states driven by Rhubarb mapped to VRM `aa/ih/ou/ee/oh`; (4) brows/blush as overlay textures keyed by emotion.
- **Lines:** keep the inverted hull for silhouettes (cheap, works in EEVEE). Use Line Art only for close-ups that need interior creases (nose, jaw, hair clumps), with one Line Art modifier per shot to avoid repeated occlusion passes. Its CPU cost on this container is unmeasured.
- Goo Engine and the AI-written 5.1 port are not worth the risk for a headless Linux farm: no current Linux binary confirmed, stability disclaimers, and the official path is catching up.

### Gaps
- Goo Engine's 2025-2026 releases, current base version and Patreon price: no primary source found.
- Line Art and Freestyle render times on llvmpipe; SDF face shadow quality on a VRoid face: not measured.
- Lightning Boy's current licence terms for commercial output were not readable on the page.
- No free, maintained "anime toon shader" add-on for Blender 4.5 was verified beyond MToon (VRM add-on).

## 4. 2D and hybrid tools and effects

### Takeaway
Anime studios add their energy in 2D: smear frames, impact frames, speed lines and stepped key poses. In this pipeline those are best drawn as Grease Pencil layers over the 3D render (or composited in pycairo as the earlier report proposed) rather than moving to a full 2D package. OpenToonz, Krita and Synfig are free but GUI-authored; none replaces the scripted pipeline.

### Cited Findings
- Smear frames stretch or distort a moving object along its path to show speed and direction; impact frames capture the instant of collision — [CG Wire](https://blog.cg-wire.com/smear-frames/) (via search extract); impact frames are "drawn by animators that appear for a split second", popularised in 2023 by One Piece — [Know Your Meme](https://knowyourmeme.com/memes/cultures/impact-frames) (via search extract); impact frames are "usually monochromatic or otherwise chromatically stylized drawings hidden within sequences" — [Sakuga Blog glossary](https://blog.sakugabooru.com/glossary/) (cited in earlier report)
- Guilty Gear Xrd made 3D characters read as hand-animated by holding stepped key poses — [GDC slides](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf) (cited in earlier report)
- Grease Pencil v3 + 5.0 motion blur + 5.3 Draw-mode editing (see section 3); Khara moved its 3DCG to Blender citing Grease Pencil — [blender.org](https://www.blender.org/?p=64752) (cited in earlier notes)
- OpenToonz: Plastic-tool mesh rigging; Rhubarb lip-sync import since v1.6 — [OpenToonz manual](https://opentoonz.readthedocs.io/); repo licence file is copyright DWANGO Co., Ltd. and contributors 2016-2026 — [LICENSE.txt](https://github.com/opentoonz/opentoonz/blob/master/LICENSE.txt) (the exact licence type, usually described as BSD-3-Clause, was not re-read: UNVERIFIED)
- Earlier container findings: Synfig has a CLI renderer and bones but yields a cut-out look; OpenToonz `tcomposer` always creates a Qt application and is untested headless; Krita's `--export-sequence` only exports an existing animated file — [Synfig man page](https://manpages.ubuntu.com/manpages/lunar/man1/synfig.1.html); [tcomposer source](https://raw.githubusercontent.com/opentoonz/opentoonz/master/toonz/sources/tcomposer/tcomposer.cpp); [Krita manual](https://docs.krita.org/en/reference_manual/linux_command_line.html) (earlier report)

### Inferences
- **Hybrid recipe [estimate]:** render the 3D hero on 1s for camera moves but evaluate character poses on 2s/3s (stepped interpolation in the Actions), then add per-shot GP or pycairo layers: (a) a 1-2 frame smear (stretched silhouette or multiple limbs) on fast arm swings and turns; (b) a 2-4 frame monochrome impact frame on hits and falls; (c) background speed lines while the character stays sharp; (d) sweat drops, anger marks and shock lines as reusable GP assets. These are pure 2D overlays, so they cost milliseconds in pycairo or one GP layer in EEVEE.
- Krita/OpenToonz are useful on the laptop only for hand-drawing reusable effect sprites (impact bursts, smoke puffs) that the pipeline then composites.

### Gaps
- No primary source from a Japanese studio quantifying which effects are 2D in 3DCG anime was found in this pass.
- Krita and Synfig licences (both widely known as GPL) were not re-verified here.

## 5. AI video and interpolation

### Takeaway
Nothing in this class runs usefully on 4 CPU cores, and only the smallest variants fit a 4 GB RTX 3050 with heavy compromises (earlier reports: Wan/AnimateDiff minutes per step on the CPU; 30 min to 6 h per clip and morphing on 4 GB GPUs). ToonCrafter, the one anime-specific in-betweener, needs about 10 GB even after community optimisation. Licences are mostly fine for a small Indian channel (Apache-2.0 code for ToonCrafter, AnimateDiff, Wan 2.2, LTX-Video; LTX-2.x free under US$10M revenue; HunyuanVideo 1.5 excluded in the EU/UK/South Korea). RIFE and GMFSS are MIT but interpolating held anime drawings destroys the look. Keep AI video out of character shots.

### Cited Findings
- ToonCrafter: code Apache-2.0 (LICENSE read here); model weights' licence not stated; "This is an open-source research exploration, instead of commercial products"; 512x320, up to 16 frames; ~24 GB on an A100, community reduced it to ~10 GB, fp16 version 12 GB; supports sparse-sketch guidance and reference-based sketch colourisation — [ToonCrafter](https://github.com/Doubiiu/ToonCrafter)
- In ComfyUI the ToonCrafter node runs 512x320 under 10 GB; routing it through the older DynamiCrafter I2V node roughly halves memory to under 8 GB with a large quality loss; fp8 saves 1-2 GB — [RunComfy: DynamiCrafterWrapper](https://www.runcomfy.com/comfyui-nodes/ComfyUI-DynamiCrafterWrapper) (via search extract). No 4 GB report found.
- AnimateDiff: Apache-2.0 — [LICENSE.txt](https://github.com/guoyww/AnimateDiff); Wan 2.2: Apache-2.0 — [LICENSE.txt](https://github.com/Wan-Video/Wan2.2); LTX-Video (repo): Apache-2.0 — [LICENSE](https://github.com/Lightricks/LTX-Video) [licence files read here]
- LTX-2.x Community License (dated 11 Aug 2026): use for any purpose subject to restrictions, but entities "with annual revenues of at least $10,000,000" need a paid licence — [LTX-2 LICENSE-2_x](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x)
- HunyuanVideo 1.5 (21 Nov 2025): Tencent Hunyuan Community License; "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA" — [LICENSE](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE)
- Practical-RIFE: MIT — [LICENSE](https://github.com/hzwer/Practical-RIFE); GMFSS_Fortuna (anime-oriented interpolation): MIT — [LICENSE](https://github.com/98mxr/GMFSS_Fortuna)
- Earlier measurements and sources: AnimateDiff ~42 s per denoising step and Wan 2.1 1.3B ~134 s per step on this container's CPU; RIFE-ncnn 2.16 s per 720x1280 in-between; anime "use 1 image for 2~3 frames", which breaks naive interpolation — [Practical-RIFE PR #23](https://github.com/hzwer/Practical-RIFE/pull/23); RTX 3050 4 GB users report ~30 min per 5 s Wan clip and "hands still render as indistinct blurry blobs" — [r/StableDiffusion 1p9gjj7](https://www.reddit.com/r/StableDiffusion/comments/1p9gjj7/); [1w9zhbx](https://www.reddit.com/r/StableDiffusion/comments/1w9zhbx/) (earlier report)
- YouTube: "Creators don't need to disclose non-realistic content that's made with AI", e.g. an AI-altered animation in a fully animated video; disclosure alone does not limit reach or monetization — [YouTube Help 14328491](https://support.google.com/youtube/answer/14328491); the inauthentic-content policy targets "AI-generated content made with generic or unoriginal templates" — [YouTube Help 1311392](https://support.google.com/youtube/answer/1311392)

### Inferences
- **Style drift is the real risk, not disclosure [estimate]:** a VRoid/Blender hero is pixel-consistent across shots; any diffusion pass (restyle, ToonCrafter in-between, AI video) reintroduces face and hand drift, the exact failure the earlier reports documented. The only AI step worth testing is ToonCrafter-style sketch-guided in-betweening for a 2D effect sprite (e.g. an explosion), and only on a rented or larger GPU, not the 3050.
- Use RIFE/GMFSS never on characters; at most on camera-only plates where nothing is held.

### Gaps
- No measured ToonCrafter, AnimateDiff or LTX run on a 4 GB card in this pass; no ToonCrafter weight licence found.
- HunyuanVideo 1.5 and LTX-2.x VRAM needs on 4 GB were not researched here (earlier report: LTX-2 32-44 GB system RAM reported).

## 6. Claude skills and MCP servers

### Takeaway
No public skill or MCP server materially improves anime character animation. The useful new find is **mcp-vroid** (MIT, 2026), which drives VRoid Studio's GUI through screenshots, OCR and synthetic input on Linux/Wayland; it could let Claude tweak sliders and export a `.vrm` on a desktop machine, but not on the headless container. The Blender MCPs (covered in the 30 Oct notes) add nothing over `blender -b -P` here. Public skill registries carry measurable malware risk; write project-local skills instead.

### Cited Findings
- mcp-vroid: "Drive VRoid Studio from any MCP client, on Linux/Wayland"; VRoid "has no scripting API, no CLI, no plugin surface", so the server screenshots the window with `grim`, locates widgets with tesseract/OpenCV and injects pointer and keyboard events; tools include `vroid_set_slider`, hair-guide editing and `vroid_export_vrm` (walks Wine's save dialog); tested on Arch Linux + Hyprland with VRoid Studio 2.14.0 under Steam/Proton; MIT (2026) — [mcp-vroid](https://github.com/nhodges/mcp-vroid); listing — [Glama](https://glama.ai/mcp/servers/nhodges/mcp-vroid)
- claude-plugins.dev (queried 30 Oct 2026): `blender-animation` and `blender-addon-dev` (TerminalSkills, 20★, 31 and 36 installs); `vrm-springbone-physics` targets three-vrm (web) debugging; no Mixamo skill; "anime"/"animation" queries return web-UI and GSAP skills — [API: blender](https://claude-plugins.dev/api/skills?q=blender); [API: vrm](https://claude-plugins.dev/api/skills?q=vrm); [API: animation](https://claude-plugins.dev/api/skills?q=animation) [read here]
- Blender MCP landscape, headless servers, BlenderGym evidence and the official Blender Lab MCP warning that it "will execute LLM generated code in Blender without any guards" — [Blender Lab](https://www.blender.org/lab/mcp-server/); [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) (see `research_notes/Monster tamer anime pipeline and hooks/claude_skills_mcp_tooling.md`)
- Snyk "ToxicSkills" (Feb 2026): of 3,984 skills from ClawHub and skills.sh, 534 (13.4%) had at least one critical issue and 76 had confirmed malicious payloads; publishing needs only a SKILL.md and a week-old GitHub account — [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub) (vendor, via search extract)
- An academic study verified 157 malicious skills among 98,380 from two community registries and notes the skill format is supported by Claude Code — [arXiv 2602.06547](https://arxiv.org/pdf/2602.06547v2) (via search extract)

### Inferences
- **Security rules [estimate]:** never install a registry skill or MCP on the container without reading every file; prefer skills written in-repo with the skill-creator; run GUI MCPs (mcp-vroid, Blender Lab MCP) only on the laptop or in a VM, never with credentials in reach.
- The most valuable "skill" is project-local: a `hero-vrm` skill documenting the VRoid export settings, the VRM import + material-conversion script, the expression/viseme map, the Mixamo/CMU action library and the timing rules (2s/3s holds, smear/impact overlays).

### Gaps
- mcp-vroid on Windows (the owner's laptop) is untested; it is Wayland/Linux-oriented.
- Download counts and maintenance of the TerminalSkills Blender skills were not inspected.

## 7. Ranked shortlist: the five changes that most improve character animation

### Takeaway
Ranked by expected quality gain per hour for the human hero and his acting, all licence-clean for monetized YouTube: (1) VRoid hero → VRM → headless Blender; (2) a retargeted Mixamo + CMU action library; (3) an anime face kit (normals, SDF shadow, expression and viseme swaps); (4) anime timing plus 2D effect overlays on the 3D render; (5) owner-acted webcam mocap for bespoke beats. AI video, text-to-motion and paid shaders stay out.

### Cited Findings
- VRoid output may be used in monetized videos — [VRoid Studio Guidelines](https://vroid.com/en/studio/guidelines); VRM Add-on 4.10.3 supports Blender 4.2 LTS to below 5.3, scriptable import — [Extensions](https://extensions.blender.org/add-ons/vrm/); [scripting API](https://vrm-addon-for-blender.info/en-us/scripting-api/)
- Mixamo royalty-free with a free Adobe ID — [Adobe FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (via extract); CMU free for all uses — [CMU](http://mocap.cs.cmu.edu/); Rokoko plugin LGPL-3 — [repo](https://github.com/Rokoko/rokoko-studio-live-blender)
- VRM expression presets (emotions, visemes, blinks) — [VRM spec](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md); custom-normal and SDF techniques — [BlenderNation Bazaar](https://bazaar.blendernation.com/listing/perfect-anime-toon-shading-in-blender-4-0/); [Notion SDF guide](https://erichu33.notion.site/Face-Shadow-Map-Creation-Baking-Workflow-d3b8769021e04683a2f2ae4cf16ac810)
- Held 2s/3s timing is the anime standard — [Wave Motion Cannon](https://wavemotioncannon.com/2016/12/31/an-introduction-to-framerate-modulation/) (earlier report); stepped key poses in 3D — [GGXrd GDC](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf)
- FreeMoCap (AGPL-3.0, CPU-only builds) — [freemocap](https://github.com/freemocap/freemocap); MediaPipe Apache-2.0 — [mediapipe](https://github.com/google-ai-edge/mediapipe)
- Current EEVEE cost on this container class: ~8 s per 720x1280 frame at 4 samples, 37-55 s at 16 samples [earlier report, contended]; the brief states 30-45 s per 720x1280 frame today.

### Inferences
| Rank | Change | Runs on | Time to set up [estimate] | CPU / render cost [estimate] | Licence |
|---|---|---|---|---|---|
| 1 | **Hero from VRoid Studio** (owner sculpts face/hair/outfit; export VRM 1.0 with owner metadata) → VRM Add-on import in `blender -b` → convert MToon to the pipeline's Shader-to-RGB toon + inverted hull | Laptop (authoring, Windows) + container (import, animate, render) | Owner 1-3 evenings for the model; 1-2 days of scripting (import, material conversion, test render) | Import seconds; render cost similar to today's characters, maybe higher from transparent hair cards (unmeasured). Add-on 1.6 MB; Blender itself must fit in the ~2.4 GB free disk | VRoid guidelines allow monetized video; avoid items with special clauses; add-on MIT/GPL |
| 2 | **Action library**: 30-60 Mixamo clips (runs, stumbles, falls, hit reactions, idles, gestures) + selected CMU BVH, retargeted once to the VRM rig (Rokoko or Keemap), stored as Actions; Python layers them with NLA | Laptop browser (Mixamo download) + container | 1-2 days (bone map, foot fixes, naming) | Negligible CPU | Mixamo royalty-free, no raw redistribution (keep FBX out of public repos); CMU free; Rokoko LGPL-3, Keemap GPL-3 (tools only) |
| 3 | **Anime face kit**: proxy-transferred custom normals, SDF face-shadow texture driven by key-light angle, VRM expressions keyed by emotion, Rhubarb → `aa/ih/ou/ee/oh` visemes, blinks, eye-highlight and brow/blush texture swaps | Container (one-off SDF painting can be on laptop in Krita) | 2-3 days | ~0 extra per frame (texture lookups) | All free techniques; Rhubarb MIT |
| 4 | **Anime timing + 2D effects over 3D**: character Actions evaluated on 2s/3s (camera on 1s), anticipation/hold key poses, GP or pycairo smear frames, impact frames, speed lines, emotes; optional Line Art only on close-ups | Container | 1-2 days | Overlays ms per frame; Line Art unmeasured (one modifier per shot) | Built-in / own code |
| 5 | **Owner-acted webcam mocap** for bespoke beats (FreeMoCap CPU build or MediaPipe/BlendArMocap), reduced to key poses and re-timed | Laptop (capture) + container (cleanup) | 1 day setup; ~30-60 min per beat | Capture on laptop CPU; cleanup trivial | Software AGPL/GPL/Apache; the motion is the owner's own |

- **Not recommended now:** AI text-to-motion for published shots (AMASS/SMPL non-commercial lineage; HY-Motion needs 24-26 GB VRAM); SMPL-based or non-commercial video mocap (4D-Humans, GVHMR); Bandai Namco and LAFAN1 BVH (NC); Goo Engine or the AI-written 5.1 NPR port (no confirmed Linux build, stability); Lightning Boy (Blender 3.4 only); AI video and RIFE/GMFSS on characters (drift, 4 GB limits, destroys held timing).
- **Watch list:** Blender 5.3 Material Lighting nodes once 5.3 is final and the VRM add-on supports it; UniRig if a Rig-XL/VRoid checkpoint ships (laptop GPU only).
- **Highest-value first test (half a day) [estimate]:** install Blender 4.5 LTS + VRM add-on on the container, import one owner-made `.vrm`, apply one Mixamo run and one fall retargeted with Rokoko, render 48 EEVEE frames at 720x1280 with stepped timing, and log seconds per frame and disk use.

### Gaps
- None of the five changes has been render-tested on the container in this session (no Blender binary found; 2.4 GB free disk).
- Setup-time figures are the researcher's estimates, not measurements.
- How a VRoid hero looks next to the existing SDF creatures and painted backgrounds is a style-frame question only the owner can judge.
