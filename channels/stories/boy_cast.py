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
                      "hoodie", seed=11, face=(120, 140, 320, 340), eyes=(130, 190, 300, 265), mouth=(184, 284, 236, 316),
                 extra=("smile",)),
    "maya": dict(tags="1girl, teenage girl, dark skin, curly black hair, brown eyes, warm smile, navy coat, mustard "
                      "yellow scarf", seed=11, face=(160, 150, 380, 370), eyes=(165, 175, 375, 285),
                 mouth=(234, 288, 296, 324), extra=("smile", "laugh", "grief"),
                 face_tags="1girl, dark skin, curly black hair, brown eyes"),
    "arthur": dict(tags="1boy, old man, very old, wrinkled face, thin white hair, grey eyes, frail, hospital gown",
                   neg="young, muscular, beard", seed=11, face=(125, 160, 345, 380), eyes=(140, 195, 300, 268),
                   mouth=(190, 300, 262, 342), extra=("grief",),
                   face_tags="1boy, old man, very old, wrinkled face, thin white hair, grey eyes, clean-shaven",
                   clear_grey=((0, 0, 160, 500), (100, 0, 512, 40), (330, 0, 512, 420), (380, 400, 512, 492),
                               (150, 330, 215, 420))),             # a machine painted behind him
    "nurse": dict(tags="1girl, adult woman, nurse, teal scrubs, brown hair, hair bun, brown eyes, calm", seed=11,
                  face=(190, 150, 410, 370), eyes=(200, 190, 405, 270), mouth=(262, 300, 318, 336),
                  face_tags="1girl, adult woman, brown hair, hair bun, brown eyes"),
}
BGS = {
    "room_night": dict(tags="teenager's bedroom at night, desk with three computer monitors showing stock charts, "
                            "blue screen glow, dark room, city lights through the window", seed=3),
    "cafe": dict(tags="empty small cafe interior by a train station, wooden tables, big window, warm afternoon light",
                 seed=5, neg="people, person, 1girl, 1boy, train interior, seats"),
    "street": dict(tags="city street crossing at dusk, zebra crossing, traffic lights, orange sky, wet asphalt, shops",
                   seed=4),
    "hospital": dict(tags="private hospital room at night, empty hospital bed, heart monitor, large window, city "
                          "lights below, cold blue light", seed=3),
}
for _k in list(BGS):                                   # 16:9 plates for the long video, same prompts
    BGS[_k + "_wide"] = dict(BGS[_k], size=(768, 512))


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
