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
