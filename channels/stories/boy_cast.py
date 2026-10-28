"""THE BOY WHO INHERITED ANOTHER BODY: the anime cast and sets for tools/anime_assets.py. Looks are production design,
not canon (the bible gives names, ages and the $5,014,382.61 only). Face, eyes and mouth boxes are in the 512x768
source image."""
SET = "boy"
CHAR_PROMPT = ("masterpiece, best quality, anime screencap, solo, plain white background, upper body, facing viewer, "
               "looking at viewer, {tags}")
# the whole negative prompt for characters (CLIP reads only 77 tokens: the important words come first)
CHAR_NEG_FULL = ("worst quality, low quality, lowres, bad anatomy, abstract background, dutch angle, holding, object, "
                 "smoke, splashes, text, watermark, nsfw")
FACE_PROMPT = "masterpiece, best quality, anime screencap, close-up, face, {tags}"
BG_PROMPT = "masterpiece, best quality, anime background, scenery, no humans, {tags}, detailed"

CHARS = {   # one look per character for every scene (consistency first)
    "neil": dict(tags="1boy, teenage boy, short dark brown hair, grey eyes, calm, slight eyebags, black jacket over grey "
                      "hoodie", seed=11, face=(120, 140, 320, 340), eyes=(130, 190, 300, 265), mouth=(184, 284, 236, 316)),
    "maya": dict(tags="1girl, teenage girl, dark skin, curly black hair, brown eyes, warm smile, navy coat, mustard "
                      "yellow scarf", seed=11, face=(160, 150, 380, 370), eyes=(165, 175, 375, 285),
                 mouth=(234, 288, 296, 324), extra=("smile", "laugh")),
    "arthur": dict(tags="1boy, old man, very old, wrinkled face, thin white hair, grey eyes, frail, hospital gown",
                   neg="young, muscular, beard", seed=11, face=(125, 160, 345, 380), eyes=(140, 195, 300, 268),
                   mouth=(190, 300, 262, 342), extra=("grief",)),
    "nurse": dict(tags="1girl, adult woman, nurse, teal scrubs, brown hair, hair bun, brown eyes, calm", seed=11,
                  face=(190, 150, 410, 370), eyes=(200, 190, 405, 270), mouth=(262, 300, 318, 336)),
}
BGS = {
    "room_night": dict(tags="teenager's bedroom at night, desk with three computer monitors showing stock charts, "
                            "blue screen glow, dark room, city lights through the window"),
    "cafe": dict(tags="small cafe by a train station, window seat, two cups of hot chocolate, warm afternoon light"),
    "street": dict(tags="city street crossing at dusk, zebra crossing, traffic lights, orange sky, wet asphalt, shops"),
    "hospital": dict(tags="private hospital room at night, empty hospital bed, heart monitor, large window, city "
                          "lights below, cold blue light"),
}


def PARTS(c):
    """name: (prompt, img2img strength, region) for each face patch; "x+y" edits the x face."""
    p = {"blink": ("closed eyes", 0.8, "eyes"), "half": ("parted lips, talking", 0.7, "mouth"),
         "open": ("open mouth, talking", 0.78, "mouth"), "fear": ("scared, wide eyes, frown, sweat", 0.5, "face"),
         "fear+blink": ("closed eyes, scared", 0.8, "eyes"), "fear+open": ("open mouth, scared", 0.78, "mouth")}
    for e in c.get("extra", ()):
        p[e] = {"smile": ("smile, happy", 0.5, "face"), "laugh": ("laughing, closed eyes, smile", 0.5, "face"),
                "grief": ("sad, tears, frown", 0.5, "face")}[e]
        p[e + "+open"] = ("open mouth, talking", 0.78, "mouth")
        p[e + "+blink"] = ("closed eyes", 0.8, "eyes")
    return p
