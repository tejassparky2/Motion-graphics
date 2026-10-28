"""DEAD MAN'S ALGORITHM, Parts 3-6: one painted illustration per non-talking shot (owner, 28 Oct 2026: "Better motion
comic, free"), for tools/anime_assets.py (`bg SPEC NAME SEEDS` paints candidates, `bg SPEC NAME` finishes the chosen
one into assets/anime/dma/bg/NAME.png; `layers SPEC NAME` cuts the figures out for parallax).

Faces that must match the cast stay on the painted puppets; these shots show what a puppet can't: hands, coins,
crowds from behind, full bodies at a distance, the door, the floor. Momo, screens and numbers stay drawn in code.
"""
SET = "dma"
CHARS = {}
BG_PROMPT = "masterpiece, best quality, anime screencap, cinematic, {tags}"

REN = "1boy, black hair, messy hair, grey eyes, black gakuran"
RIKU = "1boy, ash blonde hair, swept bangs, narrowed eyes, black gakuran, open collar"
SAKI = "1girl, short black hair, hair over one eye, grey eyes, sailor uniform, navy serafuku, red neckerchief"
DARK = "dark underground concrete room, cold fluorescent light"
WHITE = "empty white room, white walls, white floor, cold white light"
NOFACE = "face, looking at viewer"

BGS = {
    # Part 3: the Glass Auction ends
    "shot_keypad": dict(tags=f"close-up, pov, hand, finger pressing a glowing button on a tablet keypad, black sleeve, "
                             f"{DARK}, cyan glow, depth of field", neg="text, numbers, face", seed=11, layers=False),
    "shot_huddle": dict(tags=f"group of students in school uniforms, from behind, standing close together, {DARK}, "
                             f"wide shot, tension", neg=NOFACE, seed=11, layers=True),
    "shot_relief": dict(tags=f"students in school uniforms sitting on the floor, exhausted, relieved, {DARK}, from "
                             f"side, wide shot", neg="looking at viewer", seed=11, layers=True),
    "shot_door": dict(tags="silhouettes of students walking toward an open door, blinding white light, dark concrete "
                           "corridor, from behind, light rays", neg=NOFACE, seed=11, layers=False),
    # Part 4: the Charity
    "shot_room": dict(tags=f"wide shot, huge {WHITE}, group of students in school uniforms standing near the wall, "
                           f"from behind, small figures, minimalist", neg=NOFACE, seed=11, layers=True),
    "shot_coins": dict(tags="close-up, hands holding a small stack of gold coins, black sleeves, trembling hands, "
                            "white room, soft light", neg="face, text", seed=11, layers=False),
    "shot_saki_alone": dict(tags=f"{SAKI}, sitting on the floor, hugging knees, alone, sad, full body, from side, "
                                 f"{WHITE}", seed=11, layers=True),
    # Part 5: Nobody
    "shot_walk": dict(tags=f"students in school uniforms walking toward the center of a {WHITE}, from behind, wide "
                           f"shot, gold coins on the floor", neg=NOFACE, seed=11, layers=True),
    "shot_drop": dict(tags="close-up, hands dropping gold coins onto a pile of gold coins, white floor, coins "
                           "falling, motion blur", neg="face, text", seed=11, layers=False),
    "shot_saki_hands": dict(tags="close-up, a girl's hands opening, gold coins falling from her hands, sailor uniform "
                                 "sleeves, white room, soft light", neg="face, text", seed=11, layers=False),
    "shot_riku_alone": dict(tags=f"{RIKU}, standing alone, hands in pockets, full body, from a distance, {WHITE}, "
                                 f"cold expression", seed=11, layers=True),
    # Part 6: the Gift
    "shot_feet": dict(tags="close-up, feet, black school shoes, walking on a white floor, low angle, cold light, "
                           "shadow", neg="face, text", seed=11, layers=False),
    "shot_give": dict(tags="close-up, a boy's hand putting one gold coin into a girl's open palm, black sleeve, white "
                           "sleeve, white background, dramatic light", neg="face, text", seed=11, layers=False),
    "shot_coin_floor": dict(tags="a single gold coin lying on a white floor, close-up, dramatic light, long shadow, "
                                 "empty white room, no humans", neg="people, person, hands", seed=11, layers=False),
    "shot_riku_walk": dict(tags=f"{RIKU}, walking, full body, from side, {WHITE}, smirk", seed=11, layers=True),
}
