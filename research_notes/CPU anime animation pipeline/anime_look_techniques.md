# Anime look techniques: what makes 2D footage read as Japanese TV anime, and how to do each in code

Reliability tags used below: **[fetched]** = page read in full by me; **[snippet]** = only a search-engine snippet or
summary was available (page blocked or not fetched), so treat as second-hand. "Own measurement" = a CPU benchmark I ran
in this container (4 cores, OpenCV 4.10 headless, numpy, 1080x1920 frames); it is not a web source. Everything under
"Inferences" is my own reasoning or estimate unless it carries a link. Researched 27 Oct 2026.

Context from the repo (local code, not a web source): the current "anime-style" cast (`channels/stories/dma_art.py`)
is drawn with `channels/horror/toon2d.py:toon()`, which fills a part, paints the shadow wherever the part shifted
toward the light no longer covers it (so every part gets the same crescent-shaped shadow), adds an offset rim, then
strokes one uniform near-black outline (`INK = (0.09, 0.07, 0.11)`, `lw` 3-5.5 px on a 1080 px-wide frame). Sets such
as `classroom()` are also drawn with ink outlines. Motion is evaluated on continuous `t` (smooth every frame).

## 1. Line art: weight, colour-trace lines, taper, and how digital anime lines are made

### Takeaway
Anime character lines are thin, even, closed contour lines (animation needs them consistent from drawing to drawing),
with tapering only at stroke ends; colour is carried by fills, and shadow/highlight boundaries are marked by
coloured guide lines that disappear (or are recoloured) in finishing, so shadow edges carry no black ink. Digital
pipelines keep lines aliased/binary for fill and smooth them in compositing.

### Cited Findings
- "Generally, lines in animation are drawn to be consistent between cels"; the Pen tool is preferred over the Pencil
  "due to its uniform density"; stroke starts/ends taper, called *irinuki* (入り抜き); line width can be fixed later
  with "Correct line width" — [CLIP STUDIO TIPS: Tips when drawing line art for animation](https://tips.clip-studio.com/en-us/articles/957) [fetched]
- Anime-style colouring workflow: line art on a vector layer; the G-Pen gives "a sharp, anime-like line"; fills use
  "Refer other layers" and "Fill up to vector path" to avoid white gaps — [Clip Studio: Simple Anime-style Coloring Techniques](https://www.clipstudio.net/how-to-draw/archives/162911) [fetched]
- Varied line weight (thickness, rhythm, direction) reads more three-dimensional than uniform lines — [O'Reilly-hosted book on designing anime/manga characters, chapter "The basics of line"](https://oreilly.com/library/view/design-your-own/9780760371381/xhtml/05_Chapter01.xhtml) [snippet]
- In 2D animation "it is very common to use colored lines in order to indicate the specific color tones which must be
  used by the colorists"; TVPaint's Line Colorize Enhanced maps line colours to 3-5 tones — [TVPaint docs: Line Colorize Enhanced](https://doc.tvpaint.com/docs/effect-categories/color/line-colorize-enhanced) [snippet]
- In OLM's digital pipeline for *Pokémon XY&Z*, colour-trace lines (色トレス線) are normally painted over in finishing so
  they disappear; keeping line and paint on separate layers lets them be hidden by toggling visibility — [CGWORLD: OLM digital animation project](https://cgworld.jp/feature/cgw209t1-olm-4.html) [snippet]
- Colour-tracing (色トレス) the line art is done with the line layer set to Multiply; the layer property "border
  effect" (境界効果) adds a thin coloured line where base meets shadow (the author used thin orange to suggest
  sunlight) — [Clip Studio (JP): anime-style shading](https://www.clipstudio.net/oekaki/archives/152709) [fetched]
- Digital cel material is handled as non-antialiased / binarised line art (二値化された線画); PSOFT's After Effects
  anti-aliasing plugin "reduces jaggies" at the compositing stage, and CelMX is "optimised for workflows that handle
  non-antialiased images" — [CGWORLD: PSOFT plugins for Adobe CC 2014](https://cgworld.jp/news/tool/1408-adobe-cc-2014psoft.html) [fetched]
- A series' palette is set by the colour designer; each episode has its own colour coordinator — [Sakuga Blog glossary](https://blog.sakugabooru.com/glossary/) [fetched]

### Inferences
- The current renderer's 3-5.5 px near-black uniform outline on a 1080 px frame reads as Western "cartoon" ink.
  Estimate (no source gave pixel values): at 1080 px wide, close-up busts look anime-like with interior lines
  ~1.5-2.5 px and the outer silhouette ~2.5-3.5 px; mid shots thinner still.
- Line colour: render the line in a dark shade of the adjacent fill rather than one global ink (e.g. hair lines =
  hair shadow colour darkened ~50-60 %, skin lines = dark red-brown). This is the visual effect of colour-traced
  lines; exact studio conventions are unverified (see Gaps).
- **No ink on shadow boundaries.** Shadow and highlight shapes should meet the base colour with a hard edge and no
  black line (the colour-trace lines vanish in finishing). Optionally emulate the "border effect" with a 1 px line in
  a saturated warm colour on sunlit scenes only.
- pycairo implementation (cheap, all vector):
  - Silhouette thicker than interior: stroke the whole outer contour at 2x the target width *before* the fill (the
    fill covers the inner half), then draw interior lines (eyelid creases, hair strands, collar folds) at 1x on top.
  - Taper (irinuki): build each open interior line as a filled polygon from its centre-line with width profile
    `w(s) = w0 * sin(pi*s)**0.6` (s in 0..1), instead of `cr.stroke()` with round caps. Costs one polygon per line.
  - Optional "comp smoothing": a 0.5-0.7 px blur on the line layer only (scipy/OpenCV), which mimics the
    binary-line-then-antialias pipeline; low value because cairo antialiasing already does most of this.

### Gaps
- No source found with numeric line widths for TV anime relative to frame size, or confirming an "outer thick /
  inner thin" studio rule (it is common illustration advice, not verified for anime production).
- The colour code of colour-trace lines in douga (commonly said to be red for shadow boundary, blue for highlight,
  green for a second shadow) could not be verified: the Production I.G "about douga" PDF
  (https://production-ig.co.jp/retail/notice-douga/docs/about-douga.pdf) did not extract to readable text.
- Specific software workflows (RETAS STUDIO / CLIP STUDIO PAINT EX / OpenToonz in studio douga & shiage) were not
  confirmed by a fetched source in this pass.

## 2. Colour and shading: cel tones, shadow colour choice, rim light, hair highlights, blush

### Takeaway
The backbone is flat base + one hard-edged shadow (sometimes a second, darker shadow) + a small highlight, with the
shadow colour made by lowering value a little, raising saturation a little and shifting hue (toward blue in cool
light), never by mixing in grey or black. Shadow areas are kept small and designed (under-hair, under-chin, nose),
and extra light (backlight, sunlight bands, gradations) is added in compositing.

### Cited Findings
- Shadow colour (影色): pick the base, "slightly lower brightness (V) and slightly raise saturation (S) so the colour
  doesn't get muddy", then slide hue (the author shifted it toward blue for a cool picture); "keep the shadow area to
  a minimum"; put a slightly darker, slightly bluer colour in the deepest recesses; white cloth = pale grey with a
  little saturation, hue-shifted to the palette (pale blue/green) — [Clip Studio (JP): anime-style shading](https://www.clipstudio.net/oekaki/archives/152709) [fetched]
- Anime colouring commonly uses one shadow slightly darker than base and one highlight slightly lighter; some
  examples add a second, darker shadow (2影); highlights are added on a clipped layer in Screen mode — [MediBang Paint: how to color like anime style](https://medibangpaint.com/en/use/2021/07/how-to-color-like-anime-style) [snippet]
- Clip Studio's Shading Assist has a Hue parameter ("amount of hue change relative to the base color") and a "Cel
  shading" option that gives hard edges between tones — [CLIP STUDIO TIPS: Shading Assist](https://tips.clip-studio.com/en-us/articles/7624) [snippet]
- Anime skin: base brighter than the final skin tone; two shadow tones; shadows around the eyes, under the nose,
  middle of the lips, inside the ears; the shadow under the hair is painted hard then its lower edge softened;
  blush = light reddish tones blended from the edges; highlights on nose, cheeks, lips, neck; a reflected-light
  colour (blue for a cold palette) in the darkest shadows such as the neck — [Clip Studio: Anime-Style Skin Coloring Tutorial](https://www.clipstudio.net/how-to-draw/archives/161037) [fetched]
- Highlight/shadow workflow in a general anime tutorial: separate shadow and highlight layers painted with an opaque
  pen; pink airbrushed lightly on the cheeks — [Clip Studio: Simple Anime-style Coloring Techniques](https://www.clipstudio.net/how-to-draw/archives/162911) [fetched]
- The "angel ring" (天使の輪) hair highlight is the toon convention for hair shine; in Unity's Toon Shader it "always
  appears in a fixed position as seen from the camera" — [Unity Toon Shader docs: Angel Ring](https://docs.unity3d.com/Packages/com.unity.toonshader@0.13/manual/AngelRing.html) [snippet]
- Lighting moods are requested from the photography (compositing) department: "backlighting", "a band of light from
  incident sunlight", and "black shadows and gradations in front of the characters" for intimate scenes; lens flare
  and spotlights are also photography's job — [Gundam THE ORIGIN interview with DoP Takeshi Katsurayama](https://www.gundam-the-origin.net/en/special/interview21.html) [fetched]
- Asahi Production's photography workflow on *Prisma Illya* used a "cel processing" (セル処理) script that
  automatically builds metal looks and gradation processing, and can tint shadows by distance from camera — [CGWORLD: Prisma Illya photography workflow](https://cgworld.jp/feature/201512-prisma-illya-cgw208t2-2.html) [snippet]

### Inferences
- Shadow colour formula for code (my estimate, consistent with the Clip Studio rule): in HSV,
  `V_shadow = V_base * 0.78-0.88`, `S_shadow = S_base + 0.06-0.15`, hue shifted 5-15 degrees toward the scene's
  ambient (blue/violet ~230-270 deg for daylight/cool interiors; toward red/magenta for sunset). Skin shadows end up
  pink-salmon rather than brown. Second shadow (2影): apply the formula again, used only in deep crevices.
  Highlight: `V * 1.08-1.15`, `S - 0.05`, hue toward the key-light colour. Generate all three from one base so
  palettes stay coherent (this replaces the current hand-picked `mix(skin, "#8a5a48", 0.35)` brownish shades).
- Shadow *shapes* matter more than colour: replace the offset-silhouette crescent in `toon()` with authored shadow
  polygons per part in local coordinates: forehead shadow cut by the bang tips (zig-zag), a wedge under the chin on
  the neck, a small triangle beside the nose, a band under the upper eyelid on the eye white, cloth folds as sharp
  triangles. Clip each to its part (`cr.clip()`), fill hard-edged. Light direction then only selects which pre-drawn
  shadow variant to use (left/right/top/back-lit), which is how TV anime colour models work in practice (estimate).
- Rim light: keep the existing offset trick but make it thin (1-3 px), very light and tinted by the environment (sky
  blue, window white, sunset orange), and only on the backlit side; this is typically added as a compositing pass
  rather than painted (inferred from the Gundam DoP's "backlighting" request).
- Hair: one angel ring per head: a band of zig-zag or rounded lozenges following the skull curve near the crown,
  1.15-1.3x base value and lower saturation, clipped to the hair, plus small streak highlights on bangs. Static
  relative to the head drawing (matches the "fixed as seen from the camera" convention).
- Blush: soft pink ellipse (Gaussian-blurred sprite, cached) at 30-50 % alpha; diagonal hatching lines (3-5 short
  parallel strokes) on top for embarrassment beats. Hatching is a widely seen anime convention but not sourced here.
- Cost: all vector fills, negligible CPU; blurred blush is a cached sprite (the repo already has `polish.sprite`).

### Gaps
- No source gave numeric HSV offsets used by studios; the numbers above are estimates.
- Blush hatching (斜線) as an anime convention: not confirmed by a fetched source.
- No primary source on studio colour-model sheets (色指定表) with shadow-colour derivations.

## 3. Face and eye construction, mouth shapes for lip flap, blink timing

### Takeaway
The "anime face" is carried by the eyes: a heavy upper lash mass, an iris with a dark top band and lighter lower
gradient, a pupil, a limbus ring and several white/coloured highlights; nose and mouth are reduced to ticks and simple
shapes. Talking is done with about three mouth drawings (closed/half/open) and blinks are sparse, irregular and short.

### Cited Findings
- Anime eye layer stack (Clip Studio official tip): sclera; shadow cast by the upper lashes on the white; iris base;
  limbus ring a few px wide (outline of the iris selection); centred elliptical pupil; collarette ring; upper iris
  shadow on a **Multiply** layer; "a color gradient in **overlay** mode" for the lit part of the iris; small light dots;
  a shine of a different colour on the side opposite the light; a bluish ambient reflection "to represent the sky";
  colour clipped onto the lash/lid lines; finally "several pure white dots" — [CLIP STUDIO TIPS: How to draw anime eyes](https://tips.clip-studio.com/en-us/articles/2674) [fetched]
- "Anime features scenes of mouth moving with occasional eye blinks"; anime limited animation also uses "long shots
  of detailed backgrounds" and reused drawings — [Wikipedia: Limited animation](https://en.wikipedia.org/wiki/Limited_animation) [fetched]
- Three mouths are the basic lip flap: "open", "half-open", "closed"; showing them purely at random "just makes the
  mouth flutter and feels off"; a better loop at 15 fps is open 3 frames + middle 3 + open 2 + closed 2, run only
  while the line is spoken; held vowels: あ/お hold open, い/う/え hold half-open, ん stops on closed; Japanese is
  covered by five vowels + ん; key lines and shouts should get properly drawn mouths — [Mynavi: 創作番長クリエイタ #22](https://news.mynavi.jp/techplus/article/kurieita-22/) [fetched]
- Blink example at 15 fps: one closed-eye frame every 2 s, with the next blink 3 s later to avoid a mechanical rhythm;
  in-between lids lower the pupil slightly; the closed eye is drawn at the lower lid line — [Mynavi: 創作番長クリエイタ #21](https://news.mynavi.jp/techplus/article/kurieita-21/) [snippet]
- A personal production note says cel-era blinks were often just two drawings (open, closed), with half-closed
  intermediates becoming more common with 3DCG/Live2D — [Scrapbox note (low reliability)](https://scrapbox.io/frog96/%E5%8D%8A%E7%9B%AEbot%E3%81%A8%E5%86%99%E7%9C%9F%E3%81%AE%E5%86%8D%E7%99%BA%E6%98%8E) [snippet]
- *Mononoke* used seven mouth drawings, described as more convincing than "the typical two to three frames" of an
  anime mouth flap — [Awesome Engine: Mononoke's Mouths](https://awesome-engine.com/mononokes-mouths/) [snippet]
- A lip-sync generator described in an IPA-archived report uses user-supplied open/middle/closed (開口・中口・閉口)
  mouth images — [IPA archive PDF](https://www.ipa.go.jp/archive/files/000059116.pdf) [snippet]
- General lip-sync timing: one mouth key about every three frames looks more like speech than denser keys, and the
  same method applies to blinks — [Dartmouth: Lip syncing in After Effects (PDF)](https://film-media.dartmouth.edu/sites/department_film.prod/files/department_film/wysiwyg/lip_syncing_in_after_effects.pdf) [snippet]; two frames is a rule of thumb for fast speech — [AnimSchool blog](https://blog.animschool.edu/?p=8) [snippet]

### Inferences
- Eye recipe for pycairo (draw order; sizes are my estimates for a bust whose face is ~360 px wide):
  1. Eye white as a soft-cornered almond, slightly off-white/blue-grey, with a hard lash-shadow band (sclera shadow
     colour, ~25 % of eye height) under the upper lid.
  2. Iris: tall ellipse (~0.85x eye height, clipped by lids), linear gradient dark at top to lighter base colour at
     ~70 % height, then a brighter, more saturated crescent at the bottom (the "overlay" lit gradient).
  3. Upper iris shadow: Multiply band (~35 % of iris height) under the lid. Limbus: 1.5-2 px darker ring.
  4. Pupil: darker vertical ellipse ~40 % of iris width (can be same hue as iris, darker), not pure black on
     softer characters.
  5. Highlights: one large white oval or rounded rectangle at upper-left/upper-right (fixed per shot), one small
     white dot lower-opposite, optional tinted sparkle; drawn above the lash line clip so they never get covered.
  6. Upper lash mass: a filled tapered wedge (3-6x line width at the thickest point) with a flick at the outer corner;
     lower lash a short thin taper or two dots; eyebrow thin and often partly hidden by bangs.
- Nose: a tiny tick or a small shadow triangle (no outline); mouth: one short line when closed (with a lighter
  inner-lip colour for open shapes), open mouth = simple shape with dark red interior, optional tongue/teeth band.
- Lip flap in code: drive three mouth drawings from the voice track's RMS envelope (or Whisper word/phoneme timings,
  which the pipeline already produces) with hysteresis; quantise changes to 2-3 frames at 24 fps (never change mouth
  every frame); force *closed* at silences and on ん/m/b/p; choose open for a/o-heavy syllables, half for i/u/e.
  Add the Mynavi anti-chatter rule: vary hold lengths (3,3,2,2 pattern) instead of random switching.
- Blinks: open → half → closed (1-2 frames) → half → open, total ~4-6 frames at 24 fps, at irregular intervals of
  ~2-5 s (estimate); during a blink drop the iris by a few px. Skip half-frames for a more "cel-era" snap.
- Cost: negligible (vector).

### Gaps
- No studio-standard blink frame count or interval found; the numbers above are estimates built on the 15 fps example.
- No source on standard anime facial proportions (eye height vs face) for TV character sheets.

## 4. Backgrounds: painted BGs, skies, perspective sets, separating cels from BG

### Takeaway
Anime puts outlined, flat-shaded characters on top of line-less, painted, detailed backgrounds made by a separate art
department (formerly gouache/poster colour, now mostly digital paint), often assembled from reusable parts; the BG
is static and the camera moves over it while layers are shifted to fake depth.

### Cited Findings
- The art director (bijutsu kantoku) is "the person in charge of the background art for the series"; approved
  artboards serve as reference and they coordinate with colour designers — [Sakuga Blog glossary](https://blog.sakugabooru.com/glossary/) [fetched]
- In Japanese animation the credited art director is often the only BG artist on smaller productions, or oversees
  BG creation on larger ones — [Wikipedia: Background artist](https://en.wikipedia.org/wiki/Background_artist) [snippet]
- Traditional anime BGs were hand-painted in gouache on paper with layered foreground elements on cels (Hiromasa
  Ogura's work) — [Japan Foundation Sydney: Hiromasa Ogura in conversation](https://sydney.jpf.go.jp/events/hiromasa-ogura-in-conversation-with-philip-brophy) [snippet, second-hand summary]
- Studio Pablo says BG creation is now mostly digital, though the studio itself mainly paints by hand — [Otakumode: Studio Pablo interview vol. 2](https://otakumode.com/news/51b7624f11f602847501e06a) [snippet]; hand-painted BGs must be scanned before use, digital ones skip this — [Gundam THE ORIGIN: Art Director x Art Setting](https://www.gundam-the-origin.net/en/special/interview33.html) [snippet]
- TV anime BG artists can be asked to paint 10+ backgrounds a day, so they assemble scenes from part materials such as
  clouds and trees — [Maruzen Junkudo listing for an anime-background technique book (2021)](https://www.maruzenjunkudo.co.jp/products/9784046053619) [snippet]
- Published BG technique books cover sky/cloud painting including evening and night variants and cloud depth — [gihyo.jp book pickup](https://gihyo.jp/book/pickup/2014/0070?summary) [snippet]; art director Hiroshi Kato's *プロが教える アニメ背景画の描き方* covers digital BG workflow — [CGWORLD](https://cgworld.jp/news/book/1410-sotechsha-book-proga.html) [snippet]
- Foreground and background art are separated into layers that are moved in software to create camera and art motion;
  cels, BGs and CG are combined by the photography department in After Effects — [Gundam THE ORIGIN DoP interview](https://www.gundam-the-origin.net/en/special/interview21.html) [fetched]
- A Kuwahara filter is used to turn renders into "soft, painterly visuals" for an anime-style look — [80.lv: Kuwahara filter for anime-style look in Blender](https://80.lv/articles/using-kuwahara-filter-for-anime-style-look-in-blender) [snippet]

### Inferences
- The strongest BG signal is **no ink lines in the BG** plus soft painted gradients and texture, against lined, flat
  characters. The current `classroom()` uses outlines (`lw=3`), which makes BG and characters look like the same
  layer. Remove BG outlines; separate shapes by value/colour; add soft edges on far objects.
- BG plate in code (rendered once per shot, cached as a numpy array, larger than the frame for pans):
  - Sky: vertical gradient (deep saturated blue at top to pale cyan/near-white at horizon); cumulus as stacked soft
    ellipses with a flat, near-white lit top and blue-grey/lavender undersides, edges blurred 2-6 px; a few thin
    cirrus streaks.
  - Interiors (classroom): 1- or 2-point perspective drawn from a vanishing point (desks rows, window frames,
    blackboard); window light as bright, slightly overexposed shapes with light falling on desks as hard-edged
    parallelograms; colour temperature split (warm light, cool shadow).
  - Painterly texture: multiply a low-contrast paper/brush noise (1-3 %), and optionally an edge-preserving or
    Kuwahara-type filter on the plate. These are expensive (own measurement at 1080x1920: `cv2.stylization`
    ~3.2 s, `cv2.edgePreservingFilter` ~1.0 s, `cv2.bilateralFilter(d=9)` ~0.53 s), so only once per shot, never
    per frame.
  - Foreground "book" layers (desk edge, window frame, plants) on separate plates for parallax during pans
    (term "BOOK" from production practice; not verified by a fetched source here).
- Camera over BG: pans/slides/track-ins are just crops/affine warps of the cached plate (cheap); depth-of-field is a
  one-time blur of the BG plate per shot (own measurement: σ=6 blur via half-res ~14 ms; full-res ~69 ms).

### Gaps
- No fetched primary source with concrete BG painting parameters (gradient stops, texture amount).
- Sakuga Blog articles on background art were not located by search in this pass.

## 5. Compositing (satsuei / 撮影): glow, rays, flare, DoF, chromatic aberration, grain, gradients, vignette

### Takeaway
Satsuei is the final stage that combines cels, BGs and CG in After Effects and adds the light and atmosphere: glow
("transmitted light"/T光), lens flare, spotlights, backlight, sunlight bands, gradations over characters, blur and
(more recently) chromatic aberration. It is a large part of why modern anime frames look "anime" rather than
"cartoon", and almost all of it is cheap image processing.

### Cited Findings
- The director of photography's job is "creating effects and moods and visual atmosphere"; cels and BG were
  "literally 'photographed'" on an animation stand, now "we use software like the one called After Effects, and
  combining elements becomes one of the jobs of photography"; "lighting effects in a scene can cause lens flare and
  add spot lights"; requests include backlighting, a band of incident sunlight, and "black shadows and gradations in
  front of the characters"; *THE ORIGIN* deliberately kept photographic effects restrained — [Gundam THE ORIGIN DoP interview](https://www.gundam-the-origin.net/en/special/interview21.html) [fetched]
- The term survives from the film era when frames were photographed one by one; some studios now call the department
  "composition"; the department is loosely split between people handling line drawings and those handling BGs — [Otakumode: Koji Tanaka (Gargantia DoP) interview](https://otakumode.com/news/51c7bbc5a5fce80e5104cb8a/Interview-with-Koji-Tanaka-Director-of-Photography-of-ldquo-Gargantia-on-the-Verdurous-Planet-rdquo-1-4) [snippet; page returned 403]
- Digital compositing's biggest change: "it's now possible to do as many retakes as you like" — [ANN: SAO Alicization DoP Kentaro Waki](https://www.animenewsnetwork.com/interview/2019-01-09/sword-art-online-alicization-director-of-photography-kentaro-waki/.140449) [snippet; 403]
- Cel-era special photography included 透過光 (transmitted light), present since early anime and often used for
  explosions; the *Pokémon* episode 38 incident was attributed to a 透過光 effect; cel photography techniques are
  classed as camera work, cel work, photography effects and scene transitions — [MIC (総務省) white paper ch. 2](https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/h11/press/japanese/housou/0626j14.htm) [snippet]
- Production shorthand: 透過光/T光 = glow; WXP (ダブラシ) = double exposure at 1/2 + 1/2 to make thin cloth, water, fire
  or glass see-through; TU/TB = track up/back (zoom in/out), SL = slide, フェアリング = easing a pan in/out — [Scrapbox anime technique notes](https://scrapbox.io/maxcaffydotwork/%F0%9F%91%A9%E2%80%8D%F0%9F%8E%A4Anime:_%E3%82%A2%E3%83%8B%E3%83%A1%E9%96%A2%E9%80%A3_%2F_%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF) [fetched; personal notes, medium reliability]
- Anime compositing plugins: PSOFT CelMX offers "a special blur based on cel colour thresholds", "path-based blur,
  glow, chromatic aberration"; CelFX does cel colour selection/replacement, blur and debanding — [CGWORLD: PSOFT plugins](https://cgworld.jp/news/tool/1408-adobe-cc-2014psoft.html) [fetched]
- Illustration-level "anime diffusion": merge visible, duplicate, Gaussian-blur the top copy and lower its opacity by
  about 20-40 %; a second copy in **Screen** with the tone curve pulled down, blurred, at 20-40 %; finally a Screen
  layer with a light colour airbrushed around the canvas edges — [Clip Studio: Simple Anime-style Coloring Techniques](https://www.clipstudio.net/how-to-draw/archives/162911) [fetched]
- Anime compositing recipes (Blender, but generic): letterbox speed lines (gradient mask + stretched cloud noise,
  Multiply for black lines, Add for white); "soft gradient": a Multiply ramp over the image but not over the focus
  character, an Overlay ramp with black set to mid-grey (0.5) to brighten only the focus area, and a smaller Add ramp
  for off-screen glare; soft glow from a blurred object mask added over the image; Alpha Over at 0.3-0.5 for soft
  glow to avoid blow-out — [CGTrader: For Anime - Common Compositing](https://www.cgtrader.com/tutorials/6301-for-anime-common-compositing) [fetched]
- On glow quality: "Standard digital glows usually rely on a simple Gaussian blur, which is uniform", whereas real
  light "stays hot and dense for a long time before falling off"; stacking Gaussian blurs of several sizes reproduces
  the colour shift from the centre outward; film looks add halation (red/orange halo), bloom (cyan haze) and grain;
  "the look is the sum of multiple, subtle parts" (article is about analog/Western light, not anime-specific) — [Animation Obsessive: Dangerous Light](https://animationobsessive.substack.com/p/dangerous-light) [fetched]
- Ufotable's satsuei is credited with enhancing motion rather than disrupting it — [Emory film blog on *Demon Slayer: Infinity Castle*](https://scholarblogs.emory.edu/introtofilm2025/?p=1340) [snippet; low authority]
- Satsuei is taught as its own craft in Japan (e.g. an online lecture by the DoP of *Kimi no Iro* on "expression and
  direction in animation photography processing") — [Natalie](https://natalie.mu/comic/news/624561) [snippet]

### Inferences
Suggested satsuei stack for the renderer, in order, with starting values (all estimates unless marked) and measured
CPU cost per 1080x1920 frame (own measurement, OpenCV 4.10 headless, 4 cores, uint8 paths):
1. **Character/BG separation**: render BG plate and character layer separately (premultiplied ARGB), so passes can
   treat them differently. Cost: memory only.
2. **BG depth of field**: blur BG plate σ 2-8 px for close-ups (more for intimate shots), 0 for wide shots; rack focus
   = animate σ between FG and BG over 8-12 frames. ~14 ms via half-res (cache per shot when static).
3. **Para / gradation (the "gradations in front of the characters")**: full-frame linear or radial gradient,
   Multiply 10-30 % from the shadow side (tinted blue/violet or deep red at night), plus an Add/Screen warm gradient
   from the light source at 5-20 %. Existing `toon2d.grade()` already does a vertical Multiply; extend it to angled
   and radial ramps and apply it *after* the character layer. Cost ~2-5 ms (cached ramp).
4. **Light rays / sunlight band**: from windows or the sun, radial streaks Add 5-15 %, or a radial zoom-blur of the
   bright pass (8 taps at quarter res ~35 ms). The repo has `polish.light_rays()` already.
5. **Diffusion (the key "anime glow")**: bright-pass (threshold ~0.6-0.75 of white), blur at quarter resolution with
   σ ≈ 1.5-3 % of frame height (stack two sizes, e.g. 1 % and 4 %, for the non-uniform falloff Animation Obsessive
   describes), combine with **Screen** at 20-40 % (the Clip Studio value). Measured ~100 ms (unoptimised uint8;
   full-res Gaussian σ=20 alone is ~450-590 ms, so always blur at reduced resolution: quarter-res σ=60-equivalent
   blur + upscale ~27 ms).
6. **Edge glow on lit objects / T光 for screens, magic, lamps**: blurred mask Added over the image (CGTrader method).
   Cost similar to 5, or cached sprites.
7. **Lens flare**: only on real light sources in frame; 3-6 ghost discs/hexagons along the line from the light
   through frame centre, Add 5-15 %, plus a soft streak. Cheap if drawn with cairo radial gradients.
8. **Chromatic aberration**: scale the red channel by ~+0.2-0.3 % (and blue by the opposite) around frame centre so
   only edges fringe; keep subtle. ~15 ms.
9. **Vignette**: 10-25 % edge darkening, cached mask. ~2 ms.
10. **Grain**: ±4-8 /255 luminance noise, regenerated every 2 frames (pre-bake 8 plates and cycle). ~28 ms.
- Whole stack measured/estimated ~180-220 ms per frame on this container → about 3.5-4 extra minutes for a 45 s
  video at 24 fps (1,080 frames). OpenCV is not currently a project dependency (the repo uses scipy's
  `gaussian_filter`, which for full-res large σ is slower; use downsample-blur-upsample either way).
- Do *not* apply diffusion/grain to captions and hook text: composite text after the satsuei stack.

### Gaps
- No studio-published numeric settings (opacity, blur radius) for diffusion, para or CA were found; only the Clip
  Studio 20-40 % opacity value is sourced. ANN and Otakumode DoP interviews were blocked (403), so only snippets used.
- No Sakuga Blog article dedicated to satsuei was found by search (its search page lists production-notes posts but
  none surfaced compositing specifics).
- The meaning of the satsuei term "パラ" (gradient overlay; often said to derive from paraffin paper) is not confirmed by
  a fetched source; a CEDEC 2020 *BLUE PROTOCOL* talk mentions a "パラ表現" post-effect in a game context — [CGWORLD](https://cgworld.jp/feature/202011-cedec2020-bluep-2.html) [snippet].

## 6. Timing: 24 fps, 2s and 3s, holds, limited-animation tricks, smears, speed/focus lines, impact frames, shake, rack focus

### Takeaway
Anime plays at 24 fps but most character drawings are held for 2 or 3 frames (threes became the TV standard), with
ones reserved for fast action and effects; long holds where only the mouth and eyes move, camera moves over still art,
and graphic devices (focus lines, BG speed lines, impact frames) carry the energy.

### Cited Findings
- At 24 fps: on ones = 24 drawings/s, on twos = 12, on threes = 8 — [iD Tech: animating on ones, twos and threes](https://www.idtech.com/blog/what-does-animating-on-ones-twos-and-threes-mean) [snippet]
- Limited animation "holds each drawing for two or three successive frames to make up 24 frames per second"; it
  "exaggerates motion speeds by omitting inbetweens" and "does not show subtle motion because it omits almost-static
  inbetween frames"; an automatic method deletes frames during fast motion (中無し) and does not update during small
  motion (コマ撮り-like holds) — [Tsukuba CGG: Motion Frame Omission for Cartoon-like Effects (IWAIT 2014)](https://cgg.cs.tsukuba.ac.jp/projects/2013/motion_frame_omission/index.html) [fetched]
- Limited animation = using the same picture for 2 or 3 consecutive frames to build 24 fps — [IPSJ paper CG-153](https://ipsj.ixsq.nii.ac.jp/record/96173/files/IPSJ-CG13153024.pdf) [snippet]
- TV production pushed anime to threes as the standard, while Western TV used reuse/cut-outs/holds instead; "shot on
  threes" is an average, with action on twos or ones; "framerate modulation" = changing drawing rate within a cut — [Wave Motion Cannon: An Introduction to Framerate Modulation](https://wavemotioncannon.com/2016/12/31/an-introduction-to-framerate-modulation/) [snippet]
- In-betweens are spaced unevenly (タメ・ツメ, hold and compress) rather than evenly — [IPSJ EC2019](https://ipsj.ixsq.nii.ac.jp/record/199401/files/IPSJ-EC2019008.pdf) [snippet]
- Impact frames: "usually monochromatic or otherwise chromatically stylized drawings hidden within sequences", some
  held longer for effect — [Sakuga Blog glossary](https://blog.sakugabooru.com/glossary/) [fetched]
- Focus lines (集中線, shuuchuu-sen) are drawn from the screen edges toward the centre or a focal point; Japanese
  convention speed-lines the *background* and leaves the character in focus (Western comics put lines on the
  character) — [Japanese with Anime: line effects](https://www.japanesewithanime.com/2020/03/line-effects.html) and [motion lines](https://www.japanesewithanime.com/2020/03/motion-lines.html) [snippets]
- Letterbox speed lines (animated stretched noise in a frame-edge mask) are "very common in anime, especially for
  emphasis and speed" — [CGTrader: For Anime - Common Compositing](https://www.cgtrader.com/tutorials/6301-for-anime-common-compositing) [fetched]
- Anime limited animation: mouth moving with occasional blinks, reused drawings, long shots of detailed BGs — [Wikipedia: Limited animation](https://en.wikipedia.org/wiki/Limited_animation) [fetched]
- Camera language in satsuei: pan, tilt, TU/TB (track up/back), slide, fairing (ease in/out) — [Scrapbox notes](https://scrapbox.io/maxcaffydotwork/%F0%9F%91%A9%E2%80%8D%F0%9F%8E%A4Anime:_%E3%82%A2%E3%83%8B%E3%83%A1%E9%96%A2%E9%80%A3_%2F_%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF) [fetched]; camera moves follow director "guides ... like blueprints" — [Gundam THE ORIGIN DoP interview](https://www.gundam-the-origin.net/en/special/interview21.html) [fetched]

### Inferences
- **Biggest single timing fix**: render at 24 fps (Shorts accept it) and quantise *character drawing time* while
  leaving *camera* (slides, TU, shake) on ones: `t_draw = floor(t*24 / k) * k / 24` with k = 3 for idle/subtle motion
  (breathing, sway), k = 2 for gestures, k = 1 only for fast action/FX. Mouths and blinks also change on 2s/3s.
  The current smooth-every-frame `t` makes cairo puppets read as Flash/After-Effects rigs. (Smooth camera over
  stepped drawings is how digital satsuei behaves since camera moves are computed per frame; inference.)
- Prefer true holds: a still drawing with only mouth/blink plus a slow TU (the repo's `kit.whip` push-in) instead of
  continuous sine-wave idle sway. Use pose-to-pose: key poses held, 1-2 fast in-betweens with ease (タメ・ツメ).
- Smears: for 1-2 frames of a fast move, draw the limb/head stretched along the motion path or as 2-3 overlapping
  copies; cheap vector.
- Focus lines: 60-120 thin wedges from outside the frame toward a focal point, random angle jitter and lengths,
  leaving a clear ellipse (~40-60 % frame width) around the face; regenerate every 2 frames; black at 60-80 % for
  shock, white for elation. Cairo vector, ~1-3 ms (estimate).
- BG speed lines: horizontal (or motion-direction) streaks replacing or overlaid on a blurred BG, character static
  and sharp; regenerate every 2 frames.
- Impact frame (2-4 frames at the hit/twist): take the composite luminance, threshold to 2-3 levels, map to
  black/white (or black/red), optionally invert, add focus lines + 6-12 px shake; ~5-10 ms with numpy LUT.
- Camera shake: random offsets 4-12 px decaying over 6-10 frames, new offset every 2 frames (shake on twos reads
  more "anime" than smooth noise; estimate).
- Bank shots: reuse a rendered sequence (e.g. a signature reaction or transformation) across videos/episodes; the
  renderer can cache and replay.
- Rack focus: see section 5 (animate BG/FG blur σ).

### Gaps
- No authoritative source found for "bank" usage frequencies, typical hold lengths, or shake amplitudes; ANN's lexicon
  entry on "shot on threes" (https://animenewsnetwork.com/encyclopedia/lexicon.php?id=61) was blocked (403).
- Smear frame conventions in anime were not covered by a fetched source.

## 7. Which changes give the biggest perceived "anime" gain per unit of engineering effort

### Takeaway
Ranked by my judgement (not by a source): (1) time-stepping characters on 2s/3s at 24 fps, (2) thinner, coloured,
tapered line art with no ink on shadow edges, (3) authored hard shadow shapes with hue-shifted shadow colours and hair
angel rings, (4) a proper anime eye and 3-mouth/blink system, (5) line-less painted BG plates, (6) a satsuei pass
(diffusion + gradation + vignette + grain), then (7) effects vocabulary (focus lines, impact frames, shake). The first
two are nearly free in CPU and touch shared helpers (`toon()`, the frame clock), so they lift every existing shot.

### Cited Findings
- Anime limited animation is defined by drawings held for 2-3 frames and omitted in-betweens — [Tsukuba CGG](https://cgg.cs.tsukuba.ac.jp/projects/2013/motion_frame_omission/index.html) [fetched]
- Lines in animation are uniform and consistent between drawings, tapered at stroke ends — [CLIP STUDIO TIPS 957](https://tips.clip-studio.com/en-us/articles/957) [fetched]
- Shadow colours are hue/saturation-shifted, shadow areas kept minimal — [Clip Studio (JP) 152709](https://www.clipstudio.net/oekaki/archives/152709) [fetched]
- Detailed, eye-led face construction — [CLIP STUDIO TIPS 2674](https://tips.clip-studio.com/en-us/articles/2674) [fetched]
- Atmosphere, glow, flare and gradations come from the photography stage — [Gundam THE ORIGIN DoP](https://www.gundam-the-origin.net/en/special/interview21.html) [fetched]; the "look is the sum of multiple, subtle parts" — [Animation Obsessive](https://animationobsessive.substack.com/p/dangerous-light) [fetched]

### Inferences
| Rank | Change | Perceived gain (estimate) | Engineering effort (estimate) | CPU per frame (own measurement / estimate) |
|---|---|---|---|---|
| 1 | 24 fps; characters, mouths, blinks on 2s/3s; camera on 1s; real holds | High | Very low (one clock function, per-element k) | 0 (fewer unique drawings; can even cache) |
| 2 | Line art: 1.5-2.5 px interior, thicker silhouette, colour-tinted lines, irinuki taper, no ink on shadow edges | High | Low-medium (change `toon()` + a tapered-stroke helper) | ~0 |
| 3 | Authored hard shadow shapes, HSV shadow/highlight formula, thin tinted rim, angel ring | High | Medium (per-part shadow polygons for each cast member) | ~0 |
| 4 | Anime eye stack + 3 mouth drawings driven by audio, irregular blinks | High for close-ups | Medium | ~0 |
| 5 | Line-less painted BG plates (gradient sky, soft clouds, perspective rooms, texture), BG DoF | Medium-high | Medium-high (new set painter) | One-time per shot: 0.1-3 s; per frame ~0 (crop) |
| 6 | Satsuei: diffusion (Screen 20-40 %), para gradients, light rays, vignette, grain | Medium-high (instantly "TV anime" sheen) | Low (one post module) | ~180-220 ms total (diffusion ~100, rays ~35, grain ~28, CA ~15, vignette ~2) |
| 7 | Focus lines, BG speed lines, impact frames, shake on 2s | Medium (for hooks/twists) | Low | 1-10 ms |
| 8 | Chromatic aberration, lens flares, Kuwahara/painterly filters | Low; easy to overdo | Low | CA ~15 ms; painterly 0.5-3 s (BG plates only) |

- Suggested order of work: 1 → 2 → 6 (fast visible wins) → 3/4 (character redesign) → 5 → 7. Re-test the owner's
  "looks anime?" judgement after 1+2+6 before investing in 3-5.
- Risks: over-strong diffusion washes out faces (keep bright-pass threshold high and apply BG and character diffusion
  at different strengths); grain and CA can create compression artefacts on YouTube Shorts at low bitrates (keep
  grain ≤ 6/255 and regenerate on 2s rather than every frame). Captions must be composited after the post stack.
- Benchmark caveat: measured in this container with synthetic frames; real frames with large flat areas behave the
  same for blurs (cost depends on size and σ, not content). Full-resolution large-σ Gaussian blurs (450-1,800 ms) must
  be avoided; downsample first.

### Gaps
- No viewer-perception study ranks these cues; the ranking is my judgement from the cited conventions and the code's
  current state, and should be validated with the owner using side-by-side style frames.
- I found no source quantifying how much 2s/3s timing alone changes "anime-ness" ratings (the Tsukuba page reports no
  user study).
