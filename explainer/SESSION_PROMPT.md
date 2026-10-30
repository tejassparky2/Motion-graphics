You are making a vertical 3D explainer short (1080×1920, 24 fps, 15–60 s) in the style of popular
"what happens when you…" shorts: a semi-realistic character in a cosy room, an x-ray view, a medical or
mechanical cutaway, bold pop-in captions, a narrator and punchy sound design. Use only free/open-source
software and CC0/open-licensed assets, driven entirely from Python. Work headless on Linux (no GPU needed).

REUSE THE EXISTING PIPELINE FIRST
- Repo: https://github.com/tejassparky2/motion-graphics, branch `ccr-33aaae6e-sdrhrs`.
  - `explainer/xb/` = reusable toolkit: character.py (MPFB2 human + plain-dye clothes), posing.py (arm IK, hand
    shapes, fist-in-palm solver, eye tracking), anim.py (keying hands/bones/face units/blinks, camera wiggle),
    room.py (procedural living room + lights), xray.py (x-ray skin shader group, procedural hand bones bound
    to the rig, glowing joints, camera-locked backdrop), render.py (Cycles settings), captions.py, post.py.
  - `explainer/knuckles/` = the finished example: shots.py (timing), voice.py (Kokoro TTS), build.py,
    perform.py (performance + cameras), joint.py (knuckle cutaway), sound.py (SFX + music + mix).
  - `pelican/pb/` (util.py mesh builders, nodes.py shader DSL) and `pelican/tools/render_frames.py`
    (frame renderer with --range/--frames/--pct/--engine WORKBENCH/--skip_existing/--budget).
  - Read explainer/README.md first. New topics = copy `explainer/knuckles/` to a new folder and change it.

SOFTWARE (all free)
- Blender 4.5 LTS (Linux tarball from download.blender.org/release/Blender4.5/). Cycles CPU for finals,
  Workbench for fast previews. EEVEE is unusably slow without a GPU (software GL ≈ 4 min/frame) — don't use it.
- MPFB2 (MakeHuman for Blender, GPL add-on) from extensions.blender.org/add-ons/mpfb/
  install: `blender -b --command extension install-file -r user_default -e add-on-mpfb-v2.0.18.zip`
- MakeHuman CC0 asset packs from static.makehumancommunity.org/assets/assetpacks.html (files.makehumancommunity.org):
  makehuman_system_assets_cc0.zip (clothes, hair, eyes, brows, lashes, teeth), skins01_cc0.zip,
  faceunits01.zip (52 ARKit face-unit targets, CC0). Unzip ALL into
  `~/.config/blender/4.5/extensions/.user/user_default/mpfb/data/`  (that is MPFB's user-data dir;
  check with bpy.utils.extension_path_user('bl_ext.user_default.mpfb')).
- Kokoro-82M TTS (Apache-2.0) in a Python 3.12 venv:
  `uv venv -p python3.12 ~/tts && uv pip install torch kokoro soundfile` plus spaCy's model wheel
  `https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl`
  (misaki can't pip-install it inside a uv venv). Voice `af_heart` (best quality), speed ~1.1.
  Use KPipeline result tokens' start_ts/end_ts for word timings; trim Kokoro's silence around each phrase.
- numpy + scipy in Blender's bundled Python (for sound synthesis), Pillow (captions/post), ffmpeg (encode).
- Font: Montserrat (SIL OFL) from raw.githubusercontent.com/google/fonts/main/ofl/montserrat/Montserrat[wght].ttf,
  weight "Black".
- Optional, if needed: CMU motion-capture BVH (free, credit CMU), Mixamo (needs the user's Adobe login),
  Rhubarb Lip Sync (open source) for on-camera talking.

METHOD
1. Script: 40–55 words for 15 s, hook question first, one fact per shot, a payoff line. Fact-check it.
   Generate the voice → voice.wav + words.json; set shot times from the word timings (shots.py).
2. Character (xb/character.py): HumanService.deserialize_from_dict with rig "default" (has fingers, eye bones,
   jaw), high-poly eyes, eyebrow001, eyelashes01, teeth, tongue, hair short02, clothes male_casualsuit06,
   skin young_caucasian_male (ENHANCED_SSS), PROCEDURAL_EYES. Then FaceService.load_targets(...,
   load_arkit_faceunits=True) + FaceService.interpolate_targets. Replace the MakeHuman logo T-shirt with a
   plain dye (restyle_clothes). Don't run Blender with --factory-startup (it disables the extension).
3. Posing (xb/posing.py): IK on lowerarm02.L/R, chain_count 4, use_tail=True, pole empties behind the elbows;
   wrist COPY_ROTATION from the target empty; place hands by (wrist position, finger direction, palm normal).
   Fingers flex with +X local rotation. MPFB names: finger1 = thumb … finger5 = pinky; metacarpal1 = index.
   Eyes: DAMPED_TRACK (TRACK_Y) to a LookAt empty that you keyframe.
4. Performance (anim.py): key IK targets, finger shapes, head/neck/spine/clavicles, gaze, ARKit face units
   (shape keys have bare names like mouthSmileLeft and exist on the body AND brows/lashes/hair — key them on
   every mesh), blinks every 2–4 s. Cameras: one per shot, vertical sensor (24 mm), DOF on a bone-parented
   focus empty, slow push-ins, small noise-modifier handheld wiggle; switch with timeline markers.
5. Room (xb/room.py): walls with a window (emissive sky plane + area light), curtains, bookshelf with books,
   poster, floor lamp, plant; key/fill/rim area lights; AgX "Medium High Contrast".
6. X-ray (xb/xray.py): route skin through a shared XrayMix node group (transparent + blue fresnel emission,
   keyframed Amount), procedural bones bone-parented to the rig in rest pose, glowing joint capsules,
   camera-locked dark-blue backdrop that fades in; hide x-ray objects outside the shot.
7. Cutaway (knuckles/joint.py): solids of revolution sliced at y=0 with bmesh bisect + triangle_fill so the
   camera sees cut faces (cortical shell, spongy-bone voronoi core drawn 0.6 mm in front, cartilage,
   capsule, fluid just behind); shape keys stretch soft tissue; elastic-overshoot keys for pops; dark
   gradient backdrop sphere; build it far from the room (60 m) so room lights don't reach.
8. Captions (xb/captions.py): 1–3 uppercase words per chunk from the word timings, white with black
   stroke + soft shadow, keywords yellow, 5-frame overshoot pop-in, ~70 % down the frame; badges for numbers.
9. Sound (knuckles/sound.py): synthesize SFX (cracks, whooshes, shimmer, pops, ticks) and a plucked
   Karplus-Strong music bed with numpy/scipy, duck the music under the voice, soft-limit, 48 kHz stereo.
10. Post + encode (xb/post.py): punch-in zoom transitions/flashes, composite caption PNGs, then
    `ffmpeg -framerate 24 -i final/f_%04d.png -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest out.mp4`.

QUALITY / SPEED RULES
- Preview every change: Workbench animation at 25 % (every 2nd frame) for motion; Cycles stills at 50 % for
  look; look at the images before moving on.
- Cycles: 12 samples, adaptive threshold 0.04, OIDN (albedo+normal), persistent data, light tree,
  transparent bounces 8, motion blur on. Set material.cycles.emission_sampling = 'NONE' on glow-only
  materials (x-ray skin, backdrops, fluid, motes) — big speed-up. Avoid Principled subsurface except on skin.
- AgX washes bright saturated emission toward white: keep glow strengths low (0.3–1.5).
- Blender 4.4+: if you create F-curves manually, assign `anim_data.action_slot`; keyframe_insert does it for you.
- Long renders in a cloud container: run render_frames.py as tracked background tasks in chunks under
  2 hours (`--skip_existing --budget 6000`), restart the next chunk when one finishes, and keep a
  send_later check-in as a safety net — an idle session lets the container sleep and kills renders.
- Licences to credit in the description: MPFB2/MakeHuman assets (CC0), Kokoro (Apache-2.0),
  Montserrat (OFL). Never copy another channel's characters, branding or scripts — make original videos.
