"""DEAD MAN'S ALGORITHM: the anime cast and sets for tools/anime_assets.py (production design, not canon: the bible
describes only Momo, who stays drawn in code). Seeds are the candidates the owner's look was picked from; face, eyes
and mouth boxes are in the 512x768 source image."""
SET = "dma"
CHAR_PROMPT = ("masterpiece, best quality, anime screencap, solo, plain white background, upper body, facing viewer, "
               "looking at viewer, {tags}")
# the whole negative prompt for characters (CLIP reads only 77 tokens: the important words come first)
CHAR_NEG_FULL = ("worst quality, low quality, lowres, bad anatomy, abstract background, dutch angle, white jacket, "
                 "white coat, holding, bowl, object, smoke, splashes, gold, text, watermark, nsfw")
FACE_PROMPT = "masterpiece, best quality, anime screencap, close-up, face, {tags}"
BG_PROMPT = "masterpiece, best quality, anime background, scenery, no humans, {tags}, detailed"

GAKURAN = "black gakuran, black school uniform"
SAILOR = "sailor uniform, navy serafuku, red neckerchief"
CHARS = {
    "ren": dict(tags=f"1boy, black hair, messy hair, hair between eyes, grey eyes, tired eyes, expressionless, {GAKURAN}",
                seed=22, face=(150, 140, 350, 340), eyes=(155, 180, 340, 250), mouth=(203, 274, 262, 308),
                clean_light_below=420),
    "haruto": dict(tags=f"1boy, brown hair, spiky hair, brown eyes, smile, {GAKURAN}, open collar, white shirt",
                   seed=22, face=(140, 155, 330, 345), eyes=(158, 210, 308, 260), mouth=(205, 283, 262, 312),
                   extra=("grin",)),
    "yui": dict(tags=f"1girl, long hair, dark brown hair, hairclip, brown eyes, gentle smile, {SAILOR}",
                seed=22, face=(170, 105, 375, 310), eyes=(195, 160, 365, 222), mouth=(252, 246, 312, 280),
                extra=("smile",)),
    "riku": dict(tags=f"1boy, ash blonde hair, swept bangs, narrowed eyes, smirk, {GAKURAN}, open collar"),
    "kota": dict(tags=f"1boy, black hair, mushroom haircut, straight bangs, round glasses, nervous, {GAKURAN}"),
    "go": dict(tags=f"1boy, tall, broad shoulders, very short black hair, crew cut, thick eyebrows, serious, {GAKURAN}"),
    "aoi": dict(tags=f"1girl, bob cut, dark blue hair, hairpin, dark blue eyes, calm, expressionless, {SAILOR}"),
    "mio": dict(tags=f"1girl, wavy hair, light brown hair, earrings, brown eyes, half-closed eyes, smug, {SAILOR}"),
}
BGS = {
    "classroom": dict(tags="japanese high school classroom, rows of wooden desks, green chalkboard, large windows on the "
                           "left, afternoon sunlight, light rays, wall clock"),
    "chamber": dict(tags="huge underground concrete hall, wide empty room, bunker, no windows, dim cold fluorescent "
                         "light, a giant black screen on the far wall, security cameras on the ceiling, pipes, dust"),
    "sky": dict(tags="sky seen from a school window, summer clouds, city rooftops below, bright day"),
    "floor": dict(tags="concrete floor, dust, cracks, cold light from above, from above, dark corners"),
}


def PARTS(c):
    """name: (prompt, img2img strength, region) for each face patch; "x+y" edits the x face."""
    p = {"blink": ("closed eyes", 0.8, "eyes"), "half": ("parted lips, talking", 0.7, "mouth"),
         "open": ("open mouth, talking", 0.78, "mouth"), "fear": ("scared, wide eyes, frown, sweat", 0.5, "face"),
         "fear+blink": ("closed eyes, scared", 0.8, "eyes"), "fear+open": ("open mouth, scared", 0.78, "mouth")}
    for e in c.get("extra", ()):
        p[e] = {"smile": ("smile, happy", 0.5, "face"), "grin": ("grin, teeth", 0.5, "face"),
                "smirk": ("smirk, smug", 0.5, "face"), "angry": ("angry, frown, clenched teeth", 0.5, "face")}[e]
        p[e + "+open"] = ("open mouth, talking", 0.78, "mouth")
        p[e + "+blink"] = ("closed eyes", 0.8, "eyes")
    return p
