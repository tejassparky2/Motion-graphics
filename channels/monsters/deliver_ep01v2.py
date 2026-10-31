"""Episode 1 v2: the final cut. Joins the picture (helper 8's assemble_ep01v2.py -> out/monsters/ep01v2/picture.mp4)
with the sound (helper 7's ep01v2_sound.py -> out/monsters/ep01v2/mix.wav), then checks it the way the channel rules
ask before anything goes to the owner:

    /home/user/.venv-main/bin/python channels/monsters/deliver_ep01v2.py [--version diorama|diorama_v3] [--no-whisper]

writes out/monsters/ep01v2.mp4, ep01v2_preview.mp4 (small, for a phone), ep01v2_cover.jpg (frame 0, the hook
frame), ep01v2_metadata.md (the upload sheet) and ep01v2_check.md (the QA report):
- lengths: picture 1500 frames, sound 62.48 s (timing.json); the cut lands at most ~0.5 s after the last word;
- every line heard with Whisper medium.en against the script (>= 90% word match, as channels/horror/check.py);
- no encoder or metadata tags in the files (render.CLEAN);
- frame 0 has the hook text and no black frame; no Pokémon terms in the title, tags or description (report TP16).

--version diorama (owner, 31 Oct 2026: "Make episode 1 with 2.5 d so i can compare correctly") does the same for the
diorama 2.5D cut: picture out/monsters/diorama/picture.mp4, the same mix (or diorama/mix.wav if helper 7 made a
diorama-only cue fix), cover diorama/cover.jpg, and writes out/monsters/ep01v2_diorama*.  It also builds
out/monsters/ep01v2_compare.mp4: the 3D cut and the diorama cut side by side with the 3D cut's sound."""
import difflib
import importlib.util
import json
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import imageio_ffmpeg   # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-flags:a", "+bitexact", "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name=",
         "-metadata:s:a", "handler_name="]                       # the same hygiene as render.py
VERSION = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "ep01v2"
DIORAMA = VERSION == "diorama"
V3 = VERSION == "diorama_v3"             # Episode 1 v3, 2.5D (DIORAMA_EP01_V3.md): its own script, timing and mix
EPDIR = "ep01v3" if V3 else "ep01v2"
D = os.path.join(ROOT, "out", "monsters", "ep01v2")
OUT = os.path.join(ROOT, "out", "monsters", "ep01v2.mp4")
picture, mix = os.path.join(D, "picture.mp4"), os.path.join(D, "mix.wav")
cover_src = None                         # the 3D cover is written straight to ep01v2_cover.jpg by ep01v2_cover.py
if DIORAMA:
    DD = os.path.join(ROOT, "out", "monsters", "diorama")
    OUT = os.path.join(ROOT, "out", "monsters", "ep01v2_diorama.mp4")
    picture, cover_src = os.path.join(DD, "picture.mp4"), os.path.join(DD, "cover.jpg")
    if os.path.exists(os.path.join(DD, "mix.wav")):
        mix = os.path.join(DD, "mix.wav")
if V3:
    DD = os.path.join(ROOT, "out", "monsters", "diorama_v3")
    OUT = os.path.join(ROOT, "out", "monsters", "ep01v3_diorama.mp4")
    picture, cover_src = os.path.join(DD, "picture.mp4"), os.path.join(DD, "cover.jpg")
    mix = os.path.join(ROOT, "out", "monsters", "ep01v3", "mix.wav")
timing = json.load(open(os.path.join(ROOT, "channels", "monsters", EPDIR, "timing.json")))
spec = importlib.util.spec_from_file_location("ep01_episode", os.path.join(ROOT, "channels", "monsters", EPDIR,
                                                                           "episode.py"))
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)
report = [("# Episode 1 v3 (2.5D)" if V3 else "# Episode 1 v2" + (" (diorama 2.5D)" if DIORAMA else ""))
          + ": delivery check", ""]


def say(line):
    print(line)
    report.append(line)


def probe(path):
    out = subprocess.run([FF, "-i", path], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    return int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 0.0


say(f"- picture {os.path.relpath(picture, ROOT)}, sound {os.path.relpath(mix, ROOT)}")
for p in (picture, mix):
    if not os.path.exists(p):
        sys.exit(f"missing {p}: run the assembler / the sound mix first")

# 1. the files line up
n = len(subprocess.run([FF, "-v", "error", "-i", picture, "-map", "0:v:0", "-vf", "scale=8:8", "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout) // 64
say(f"- picture: {n} frames (timing.json: {timing['total_frames']})" + ("" if n == timing["total_frames"] else
                                                                         "  **MISMATCH**"))
ms = probe(mix)
say(f"- sound: {ms:.2f} s (timing.json: {timing['total']:.2f} s)" + ("" if abs(ms - timing["total"]) < 0.05 else
                                                                     "  **MISMATCH**"))
last_word = timing["lines"][-1]["words"][-1]["end"]
say(f"- the cut lands {timing['total'] - last_word:.2f} s after the last word (rule: about 0.5 s or less)")

# 2. mux, then a stream-copy pass so no encoder tag is written back
tmp = os.path.join(D, "_mux.mp4")
subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", picture, "-i", mix, "-map", "0:v:0", "-map", "1:a:0",
                       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", *CLEAN, tmp])   # no -shortest: it cut 3 frames
subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                       OUT])
prev = OUT[:-4] + "_preview.mp4"
subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", OUT, "-c:v", "libx264", "-crf", "27", "-preset", "slow",
                       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", *CLEAN, tmp])
subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                       prev])
os.remove(tmp)
for f in (OUT, prev):                    # the delivered files keep every frame of the picture
    nf = len(subprocess.run([FF, "-v", "error", "-i", f, "-map", "0:v:0", "-vf", "scale=8:8", "-f", "rawvideo",
                             "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout) // 64
    say(f"- {os.path.relpath(f, ROOT)}: {nf} frames" + ("" if nf == timing["total_frames"] else "  **FRAMES LOST**"))
cover = OUT[:-4] + "_cover.jpg"
if cover_src and os.path.exists(cover_src):
    subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", cover_src, "-q:v", "2", *CLEAN[:4], cover])
if not os.path.exists(cover):           # helper 7's ep01v2_cover.py writes the designed cover here; keep it if present
    subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", OUT, "-frames:v", "1", "-q:v", "2", *CLEAN[:4], cover])
say(f"- wrote {os.path.relpath(OUT, ROOT)} ({os.path.getsize(OUT) / 1e6:.1f} MB), the preview and the cover")

# 3. frame 0 is not black and the file carries no tags
f0 = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", OUT, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt",
                                   "gray", "-"], capture_output=True).stdout, np.uint8)
say(f"- frame 0 mean brightness {f0.mean():.0f}/255" + ("  **TOO DARK**" if f0.mean() < 40 else ""))
data = open(OUT, "rb").read() + open(prev, "rb").read()
tags = {s: data.count(s.encode()) for s in ["x264", "Lavf", "Lavc", "encoder", "c2pa", "jumb"]}
say(f"- tags in the files: {tags}" + ("" if not any(tags.values()) else "  **CLEAN THESE**"))

# 4. no Pokémon terms in the packaging (TP16)
m = ep.METADATA
blob = " ".join([m["title"], *m["alt_titles"], m["description"], *m["tags"], *m["hashtags"],
                 m["pinned_comment"]]).lower()
hits = [w for w in ("pokemon", "pokémon", "pikachu", "ash ketchum", "nintendo", "game freak", "-mon ") if w in blob]
say(f"- trademark terms in the upload sheet: {hits or 'none'}")

# 5. the upload sheet
with open(OUT[:-4] + "_metadata.md", "w") as f:
    f.write("# Upload sheet: Cute Things Kill Here, Episode 1\n\n")
    f.write(f"**Title** ({len(m['title'])} characters)\n```\n{m['title']}\n```\n\n")
    f.write("**Alternative titles to test**\n" + "".join(f"- `{x}`\n" for x in m["alt_titles"]) + "\n")
    f.write("**Description**\n```\n" + m["description"].strip() + "\n\n" + " ".join(m["hashtags"]) + "\n```\n\n")
    f.write("**Tags** (paste into YouTube Studio > Tags)\n```\n" + ", ".join(m["tags"]) + "\n```\n\n")
    f.write(f"**Pinned comment**\n```\n{m['pinned_comment']}\n```\n\n")
    f.write(f"**Video facts:** {timing['total']:.1f} s. Narrated with Chatterbox Turbo (synthetic voice; nobody real "
            "is cloned). Music and sound effects are original. Made for kids: **No** (comments stay on for the vote). "
            "Altered or synthetic content: **No** (fully animated fantasy). "
            f"Cover: {os.path.basename(cover)} (S01 with \"IT ERASED A FOREST\"); where the app can't take a custom "
            "Shorts cover, pick frame 0, the hook frame.\n")
say(f"- wrote {os.path.relpath(OUT[:-4] + '_metadata.md', ROOT)}")

# 6. every line heard as written (Whisper medium.en)
if "--no-whisper" not in sys.argv:
    from faster_whisper import WhisperModel
    SAME = {"its": "it's", "didnt": "didn't", "dont": "don't", "thats": "that's"}

    def norm(s):
        return [SAME.get(w, w) for w in re.findall(r"[a-z0-9']+", s.lower().replace("-", " "))]

    pcm = subprocess.run([FF, "-v", "error", "-i", OUT, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    model = WhisperModel("medium.en", device="cpu", compute_type="int8")
    bad = spoken = 0
    say("")
    say("| Line | Match | Heard |")
    say("|---|---|---|")
    for b in timing["lines"]:
        if not b["text"]:
            continue
        spoken += 1
        a = audio[max(0, int((b["start"] - .3) * 16000)): int((b["end"] + .15) * 16000)]
        heard = " ".join(s.text for s in model.transcribe(a, language="en", beam_size=5)[0]).strip()
        r = difflib.SequenceMatcher(None, norm(b["text"]), norm(heard)).ratio()
        bad += r < .9
        say(f"| {b['id']} | {r:.0%}{'' if r >= .9 else ' **BAD**'} | {heard} |")
    say("")
    say(f"**{spoken - bad}/{spoken} lines heard as written (Whisper medium.en)**")
with open(OUT[:-4] + "_check.md", "w") as f:
    f.write("\n".join(report) + "\n")

# 7. the diorama cut: the side-by-side comparison the owner asked for (3D left, diorama right, the 3D cut's sound)
if DIORAMA:
    from PIL import Image, ImageDraw, ImageFont
    three_d = os.path.join(ROOT, "out", "monsters", "ep01v2.mp4")
    cmp_out = os.path.join(ROOT, "out", "monsters", "ep01v2_compare.mp4")
    band = os.path.join(D, "_compare_band.png")
    im = Image.new("RGB", (1080, 80), (16, 16, 20))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(ROOT, "assets", "fonts", "LuckiestGuy-Regular.ttf"), 44)
    for x, label in ((270, "3D"), (810, "2.5D DIORAMA")):
        dr.text((x, 44), label, font=font, fill=(255, 255, 255), anchor="mm")
    im.save(band)
    subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", three_d, "-i", OUT, "-framerate", "24", "-loop", "1",
                           "-i", band,
                           "-filter_complex", "[0:v]scale=540:960:flags=lanczos[a];[1:v]scale=540:960:flags=lanczos[b];"
                           "[a][b]hstack[ab];[2:v][ab]vstack=shortest=1,format=yuv420p[v]",
                           "-map", "[v]", "-map", "0:a:0", "-frames:v", str(timing["total_frames"]), "-c:v", "libx264",
                           "-crf", "18", "-preset", "slow", "-c:a", "aac", "-b:a", "160k", *CLEAN,
                           OUT[:-4] + "_tmp.mp4"])
    subprocess.check_call([FF, "-y", "-loglevel", "error", "-i", OUT[:-4] + "_tmp.mp4", "-c", "copy", *CLEAN,
                           "-movflags", "+faststart", cmp_out])
    os.remove(OUT[:-4] + "_tmp.mp4")
    os.remove(band)
    nf = len(subprocess.run([FF, "-v", "error", "-i", cmp_out, "-map", "0:v:0", "-vf", "scale=8:8", "-f", "rawvideo",
                             "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout) // 64
    say(f"- wrote {os.path.relpath(cmp_out, ROOT)}: {nf} frames, 1080x1040 (3D left, diorama right)"
        + ("" if nf == timing["total_frames"] else "  **FRAMES LOST**"))
    with open(OUT[:-4] + "_check.md", "w") as f:
        f.write("\n".join(report) + "\n")
