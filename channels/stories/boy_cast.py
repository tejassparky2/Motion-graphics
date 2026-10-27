"""THE BOY WHO INHERITED ANOTHER BODY: the anime cast and sets for tools/anime_assets.py. Looks are production design,
not canon (the bible gives names, ages and the $5,014,382.61 only). Face, eyes and mouth boxes are in the 512x768
source image."""
SET = "boy"
CHAR_PROMPT = ("masterpiece, best quality, anime screencap, {tags}, solo, upper body, facing viewer, looking at viewer, "
               "straight-on, centered, standing, plain white background, simple background")
CHAR_NEG = "dutch angle, tilted, abstract background, liquid, splashes, paint, particles, gradient background"
FACE_PROMPT = "masterpiece, best quality, anime screencap, close-up, face, {tags}"
BG_PROMPT = "masterpiece, best quality, anime background, scenery, no humans, {tags}, detailed"

CHARS = {
    "neil": dict(tags="1boy, 17 years old, teenage boy, short dark brown hair, grey eyes, calm, intelligent, slight "
                      "eyebags, grey hoodie"),
    "neil_jacket": dict(tags="1boy, 17 years old, teenage boy, short dark brown hair, grey eyes, slight smile, black "
                             "jacket over grey hoodie"),
    "maya": dict(tags="1girl, 17 years old, dark skin, brown skin, curly black hair, voluminous curly hair, brown eyes, "
                      "warm smile, navy coat, mustard yellow scarf"),
    "arthur": dict(tags="1boy, old man, elderly, 82 years old, wrinkles, thin face, white hair, sparse white hair, "
                        "grey-blue eyes, frail, hospital gown, nasal cannula", neg="young, muscular, beard"),
    "nurse": dict(tags="1girl, adult woman, nurse, teal scrubs, brown hair, hair bun, brown eyes, kind, calm"),
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
    p = {"blink": ("closed eyes", 0.55, "eyes"), "half": ("parted lips, talking", 0.5, "mouth"),
         "open": ("open mouth, talking", 0.55, "mouth"), "fear": ("scared, wide eyes, frown, sweat", 0.5, "face"),
         "fear+blink": ("closed eyes, scared", 0.55, "eyes"), "fear+open": ("open mouth, scared", 0.55, "mouth")}
    for e in c.get("extra", ()):
        p[e] = {"smile": ("smile, happy", 0.5, "face"), "laugh": ("laughing, closed eyes, smile", 0.5, "face"),
                "grief": ("sad, tears, frown", 0.5, "face")}[e]
        p[e + "+open"] = ("open mouth, talking", 0.55, "mouth")
        p[e + "+blink"] = ("closed eyes", 0.55, "eyes")
    return p
