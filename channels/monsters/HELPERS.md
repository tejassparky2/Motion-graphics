# Helper brief: monster series ("Cute Things Kill Here"), Episode 1 assets

You are one of several cloud sessions building pieces of a Pokémon-ANIME-style 3D series in Blender, coordinated by
session_0153qDV4AufFgT2PhEBEfS8n ("Interactive 3D horror stories"). Reply to it with send_message when you finish or
get blocked.

## Setup (once)
1. Get the repo: tejassparky2/Motion-graphics, branch `ccr-56282fe5-evehq4-horror`. If it isn't in your session, call
   add_repo(owner="tejassparky2", repo="Motion-graphics", access="push") and clone it to /home/user/Motion-graphics.
2. Blender 4.5.15 LTS (no GUI, CPU only):
   ```
   mkdir -p /home/user/tools && cd /home/user/tools
   curl -sSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.15-linux-x64.tar.xz && tar -xf b.tar.xz && rm b.tar.xz
   B=/home/user/tools/blender-4.5.15-linux-x64; $B/4.5/python/bin/python3.11 -m ensurepip; $B/4.5/python/bin/python3.11 -m pip install scikit-image scipy
   ```
   EEVEE renders headless through Mesa llvmpipe/EGL (needs libegl1 + libegl-mesa0; `apt-get install -y libegl1 libegl-mesa0` if missing).
   Ignore "EGL_BAD_MATCH" warnings.
3. Read, in this order:
   - `channels/monsters/NOTES.md`
   - `channels/monsters/mk/look.py` (the anime look)
   - `channels/monsters/mk/sdf.py` (sculpting smooth bodies)
   - `channels/monsters/mk/puffshrimp.py` (an example creature rig)
   - `channels/monsters/mk/anim.py` (keyframes, on-2s timing, VFX)
   - `channels/monsters/mk/sets.py`
   - `channels/monsters/test_puff.py` (an example test)
   - Look at `out/monsters/style_frame_toon_v1.png`.

## The style: Pokémon anime (TV cel look), studied from Pokémon Horizons episodes 1385-1386 (Sept 2026)
- **Characters and creatures:**
  - Flat base colour plus ONE hard, slightly cool shadow tone: `look.toon(...)` with `look.STYLE = "anime"`.
  - Thin dark outlines: `look.outline(obj, width)`.
  - Big glossy eyes with two white highlights.
- **Backgrounds and set pieces:**
  - NO outlines.
  - Painted, soft light with gentle noise: `look.paint(...)`.
  - Gradient sky with big cumulus clouds: `look.world()`.
  - Distant things paler and bluer.
- **Timing:** characters animate on 2s (`anim.on_twos(objs)`); the camera stays smooth.
- **Effects:** 4-point sparkle stars, glows, speed lines, impact frames (2D overlays are a separate job).
- **Format:** vertical 720x1280 (9:16), 24 fps, EEVEE, 16 samples (`look.render_setup()`).

## Frame-by-frame targets (from studying 140 Horizons screenshots; match these, don't copy designs)
- **Characters and creatures:**
  - Clean dark-navy lines ~2-3 px at 720 px wide (`look.LINE_SCALE = 1.5`, the default).
  - One flat base colour plus one hard, cool shadow tone.
  - A colour boundary on a character (belly patch, markings) must be ONE clean curve. Build markings as their own
    smooth shapes pressed into the body, not per-face materials from sdf.py, which come out jagged.
- **Trees:** "cauliflower" masses of merged leaf clumps, painted in three greens (dark inside and underneath, mid,
  yellow-green where lit), with no lines: `mk/paintbg.py` `tree()`, `paint3()`, `greens()`. Mostly natural greens;
  candy colours only as rare accents.
- **Grass:** painted brush strokes stretched sideways (`paintbg.grass_material()`).
- **Sky:** gradient with thin, flat-bottomed, wispy clouds with lavender shadows (`paintbg.sky()`).
- **Depth:** the background is strongly soft behind characters. Use camera DOF with an exaggerated aperture,
  `aperture_fstop ≈ 0.15` (a real f-stop gives <1 px of blur at these distances). Things far away get paler and bluer
  (`far=` in paintbg).
- **Framing:** the character is big in the frame, camera low at its eye level (35-50 mm). Wides are for establishing
  shots only.
- **Effects:** glowing beams with white cores and streaks, 4-point sparkles, soft bokeh glows. Keep flashes short
  (1-2 frames) and dust light.
- **Reference frame:** `out/monsters/style_frame_anime_v2.png` and `channels/monsters/test_anime_bg.py`.

## Latest updates (newest first). The coordinator sends every change to every helper.
- **30 Oct, v8 (outlines on every creature; the cap gap; earth outfit). Pull 3b0fc70 or later before ANY render:**
  - `sdf.build` meshes now face outward. Until now every SDF body (puff-shrimp body and claw, pistol shrimp,
    jelly-snail, fluffmoth parts) faced INWARD: their inverted-hull outline was hidden and their toon light was
    inverted (the lit side came out dark). Now they get crisp coloured lines like Kai. If your module flips SDF
    normals itself, check it still faces outward (tuftwing's check-and-flip is fine).
  - `look.outline` uses quality normals: no long dark spikes from sliver triangles.
  - `hero.load()` closes the ~1 cm gap between the cap's dome and visor (hair and forehead showed through at eye
    level), and `outfit="earth"` works without a workaround.
  - **Any shot already rendered with a creature in it must be re-rendered** so the creatures match across the cut.
  - **The outline shells no longer shadow the bodies they wrap** (look.py, `use_backface_culling_shadow` on every
    line material; found by helper 6). After 3b0fc70 the shell wrapped each SDF body and EEVEE shadowed the whole
    creature, so bodies rendered in the shadow tone all over. **Every creature render must start from this commit or
    later** (see the commit after f62df6a).
  - **1d22a94: the puff-shrimp's pivots are fixed** (mk/puffshrimp.py `_empty`). The claw hinge and the lid pivots sat at
    twice their offset, so the snapping finger swung off the claw and blinks closed in the wrong place. Re-check any
    shoulder/hinge/lid angles you tuned against the old pivots. Start every shrimp render from 1d22a94 or later.
- **30 Oct, v7 (exact timing; rot_z fixed):**
  - **Exact shot lengths are in `channels/monsters/ep01v2/TIMING.md`** (and `timing.json`), measured from the voice
    takes. They replace the estimates in EP01V2_SHOTS.md. The episode is 62.48 s = 1500 frames.
  - Render **frames + 12** (the "Render frames" column). Longer is fine: the edit trims. Shorter is not: re-render.
  - Every shot cuts in 0.30 s (7 frames) before its line. The voice in/out columns are seconds from the shot's first
    frame, so mouth flaps (aa/oh on 3s), blinks and hits land on them. Word times are in timing.json.
  - Silences belong to the shot BEFORE the next line: S08 ends on ~0.8 s of black, S19 holds the quiet drying for
    ~1.4 s after its line, S20 holds the pff, the stare, the head tilt and Kai's 2 s deadpan after "It tried anyway."
  - **`hero.load(rot_z=...)` now works** (the VRM import left the armature in quaternion mode; thanks, helper 10).
    Pull before your next render. If you worked around it, your workaround still works.
- **30 Oct, v6 (hero ready, new outfit, meadow scale):**
  - **Kai is ready, with no add-on needed:**
    - `from channels.monsters.mk import hero`
    - `rig = hero.load(loc, scale, rot_z, outfit="world"|"earth", line=0.004)` appends `assets/monsters/hero/hero.blend`.
    - Scale: 5.8 in the creature world (1 unit = 20 cm), 1.1 in metre scenes (the lab).
    - Faces: `hero.face(rig, "surprised", frame)`. Names: neutral happy angry sad relaxed surprised blink wink squint
      star shock pinprick dot v blush aa ih ou ee oh mouth_open grit brows_up brows_down look_up look_down look_left
      look_right, or any raw shape key on the `head` mesh. Faces snap (CONSTANT).
    - Bones: `rig["bone"]("left_upper_arm")`, with Rigify names underneath: upper_arm.L, forearm.L, hand.L, thigh.L,
      shin.L, foot.L, spine, chest, neck, "head 1", hips. The rest pose is a T-pose; arms down is upper_arm
      rotation_euler z = ±(-72°) in XYZ mode.
    - Outline: `hero.line_width(rig, 0.0015)` for face close-ups.
  - **His look** (owner, 30 Oct: "change his dress... Pokémon and modern anime"): a teal zip jacket, charcoal joggers,
    bare forearms with fingerless gloves, a teal sweatband, white sneakers with yellow toes, and a white cap with a
    teal visor and a teal "K". See `out/monsters/tests/hero_v2_outfit.png`.
  - **Meadow scale:** `mk/meadow.py` trees are now real size (TREE = 4.5), so Kai is dwarfed by them and the stumps
    are big and glowing. Set cameras to `clip_end = 2000`. See `out/monsters/tests/meadow_scale_kai.png`.
  - **Credit:** every upload carries the line in `assets/monsters/hero/CREDIT.md`.
- **30 Oct, v5 (owner APPROVED Episode 1 v2: "build full with animation like Pokémon, apply all research, quality
  first, use all helpers"):**
  - **Script:** `out/monsters/story_v2.md`.
  - **Shot list, who builds what, and the rules per shot:** `channels/monsters/EP01V2_SHOTS.md`.
  - **Rules:** `reports/Pokémon episodes story and animation.md`. Read sections SG, IM, LC, SU, CH, TP before
    building. Every shot must follow them, and you compare your frames against them.
  - **No HUD and no text in the picture.** The 2D kit is used only for effects (impact frames, speed lines,
    sparkles, emotion backgrounds, comic faces).
  - **The hero:** `channels/monsters/mk/hero.py` (Seed-san restyled; credit in `assets/monsters/hero/CREDIT.md`). A
    no-add-on `hero.blend` version is coming from the coordinator; until then build your sets and creatures.
  - **The runner:** `render_shot.py` supports `step` (render only frames that change).
  - **Deliver** finished shot mp4s plus contact sheets in `out/monsters/ep01v2/shots/`.
- **30 Oct, v4 (owner): STOP and PAUSE.**
  - The game HUD is dropped: a pure anime, with no health bar, status bar, WILD tag, threat pips, menus, BOND
    pop-up or fact cards.
  - The story is being rewritten after a deep study of three Pokémon TV episodes (animation and story).
  - Helpers push what works and wait for a new brief. The v3.2 shot list (`EP01_SHOTS.md`) is on hold.
- **30 Oct, v3.2 (shot list, voice, 2D kit, subject pass, Kai's design):**
  - **Shot list:** `channels/monsters/EP01_SHOTS.md` gives every Episode 1 shot, its length, camera and overlay. Build
    your asset's motion to fit those lengths: lines over 3 s are split into two shots (e.g. the snap line 5 = 4.35 s
    becomes S05a + S05b).
  - **Voice:** Kai narrates in Turbo `am_liam`. All 19 lines are voiced and Whisper-checked
    (`assets/voice_cache/monsters_ep01_takes.tar`). Any change to a line's text or punctuation re-voices it.
  - **2D kit:**
    - `channels/monsters/fx2d.py` has the impact frame, speed lines, sparkles, glow, shockwave, dust, "!", status
      bar, WILD tag, choice menu, BOND!, rule chip, fact card, HUD boot and hook text. Demo stills are
      `out/monsters/tests/fx2d_*.png`.
    - `channels/monsters/fx2d_extra.py` has the beam (white core) and bokeh glows.
    - Don't draw your own HUD or text in Blender; leave room for these.
  - **Safe areas:**
    - Captions sit at y 845-930.
    - Nothing important below y 845, or in the Shorts right rail (x > 620, y 640-1180).
  - **Subject pass:** shots with an impact frame or a speed-line background (S08, S16) also render the character
    alone on a transparent film. `look.subject_only([rig["root"]])` switches a scene to that pass; render it into a
    `subject/` folder next to the normal frames.
  - **Kai's design (use exactly this wherever Kai appears):**
    - A 19-year-old, slim, anime-teen proportions (about 6 heads tall).
    - Messy dark-brown hair (#4a3328) with one tall front cowlick and side tufts. No cap or hat.
    - Big anime eyes: amber-brown iris (#b5652b), a lighter lower crescent, two white highlights.
    - Clothes:
      - an open sage-green zip-up jacket with a hood (#7fae8a; he throws it over the puddle in Episode 2) over a
        white T-shirt;
      - dark-navy cargo trousers (#2e3550);
      - orange-yellow sneakers (#ffb340);
      - a black digital watch on the RIGHT wrist. The left wrist stays bare: the bond ring appears there in
        Episode 2.
    - In the lab, an open white lab coat over the jacket.
    - Faces are flat anime: the eyes are separate shapes, the nose tiny, and the mouth a swappable shape (neutral,
      shocked "o", smile, gritted teeth).
- **30 Oct, v3.1 (full shot-by-shot pass over a TV episode, `ANIME_STUDY.md` "Second pass"):**
  - 78% of shots have a locked camera; pans are short (1.5-2 s).
  - A reaction shot follows almost every beat.
  - Big moments get full-frame energy, speed-line or burst backgrounds, and the character frozen while the effect moves.
  - Shape wipes mark act changes.
  - For assets: give every creature and Kai one strong held "reaction pose" (shock, delight) usable as a freeze frame.
- **30 Oct, v3 (style frame `out/monsters/style_frame_anime_v3.png`).** From measuring a full Pokémon TV episode frame
  by frame (`channels/monsters/ANIME_STUDY.md`):
  - Lines are coloured per colour: `look.outline()` now gives each material its own darker line (`line_color`,
    k=0.28). Don't force a single black outline.
  - Creature eyes are black, with a lighter coloured crescent low in the eye and two white highlights (see
    `puffshrimp.py`, `iris_m`).
  - Character acting is on 3s: `anim.on_twos(objs)` now defaults to step=3. Use step=2 for fast action; the camera
    and VFX stay on 1s.
  - Shots cut every 1.5-3 s; hold longer only for big reveals. Keep shading mostly flat, with shadows only in designed
    spots. Use low camera angles against a deep blue sky, with ambient sparkles and bubbles.
- **30 Oct, v2 (style frame `out/monsters/style_frame_anime_v2.png`):**
  - `mk/paintbg.py`: painted backgrounds, cauliflower trees, brush-stroke grass, wispy sky.
  - Lines ~2-3 px.
  - Clean colour boundaries.
  - Background blur at f≈0.15.

## Hard rules
- **Original designs only.** Nothing that looks like a Pokémon, Kirby, Digimon or any franchise character: no
  red-and-white ball, no Pokédex-style UI, no pink round puffballs. Cute round bodies; each creature has ONE odd,
  creepy "tell".
- **Reproducible code.** Everything is built in Python (bpy + numpy), deterministic with seeded RNG. Every shot must
  render identically on every session.
- **Assets:** if you use downloaded assets, only CC0 (Quaternius, Kenney, Poly Haven), and note the source in a
  docstring.
- **Files:** only add your own files:
  - `channels/monsters/mk/<yourmodule>.py`
  - `channels/monsters/test_<yourmodule>.py`
  - `out/monsters/tests/<yourmodule>_*.png` (PNG stills at 720x1280; keep each under ~2 MB, no frame sequences in
    git)
- **Don't edit shared files** (look.py, sdf.py, anim.py, sets.py, puffshrimp.py). If you need a change there, put it
  in your module or ask the coordinator.
- **Check your own output.** LOOK at every render before reporting (silhouette readable at phone size, nothing cut
  off, no black frames). Blender 4.4+: hand-made F-curves need `anim_data.action_slot = action.slots[0]`.
- **Git:**
  - `git pull --no-rebase origin ccr-56282fe5-evehq4-horror` before each push.
  - Push with `git push -u origin ccr-56282fe5-evehq4-horror`.
  - If refused: `git -c push.negotiate=false push --no-thin -u origin ccr-56282fe5-evehq4-horror`.
  - Retry on network errors (2/4/8/16 s).
  - Commit messages end with your own session's attribution lines.
- **Long renders:** run them as tracked background tasks in chunks under 2 h. The container sleeps when idle.

## Report back (send_message to session_0153qDV4AufFgT2PhEBEfS8n)
- The files you added and the commit hash.
- The render time per frame.
- What still looks weak.
