"""Finish a rendered mythology video in one language: cover, phone copy (< 29 MB), upload pack, Drive copy.

  python -I -X utf8 channels/mythology/finish.py <video> <lang> <number> [--cover-at 2.6] [--no-drive] [--pack-only]

Inputs: myth_out/<video>_<lang>.mp4 (the master from render_myth.py). Outputs in myth_out/upload_<video>_<lang>/:
the master, <video>_<lang>_phone.mp4, cover.jpg, UPLOAD_VIDEO<N>_<NAME>_<LANG>.md. The pack follows the owner's
rules: no links in sources or credits, no AI wording, the hook as caption line 1 (under 125 characters), 5 hashtags."""
import importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(os.path.dirname(HERE))]
from channel import OUT_ROOT, ROOT  # noqa: E402

PY = sys.executable
PHONE = os.path.join(ROOT, "channel_tools", "phone_copy.py")
DRIVE = r"H:\My Drive"
CHANNEL_DIR = "Mythology reels"          # renamed once the owner picks the channel names
LANG_NAME = {"hi": "Hindi", "kn": "Kannada"}


def load(name):
    spec = importlib.util.spec_from_file_location(f"v_{name}", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def facts(mod):
    doc = mod.__doc__ or ""
    m = re.search(r"Facts[^:]*:(.*)", doc, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", path]))


def cover(name, lang, t, out_jpg):
    env = dict(os.environ)
    env.pop("MYTH_DRY", None)
    subprocess.run([PY, "-I", "-X", "utf8", os.path.join(HERE, "render_myth.py"), "--video", name, "--lang", lang,
                    "--still", str(t)], check=True, env=env, capture_output=True)
    png = os.path.join(os.path.dirname(os.path.dirname(HERE)), "build", "mythology", f"{name}_{lang}_still_{t}.png")
    from PIL import Image
    Image.open(png).convert("RGB").save(out_jpg, quality=95)


def pack(mod, name, lang, n, folder, dur, files):
    m = mod.METADATA[lang]
    sheet = os.path.join(OUT_ROOT, f"{name}_{lang}_upload_sheet.md")
    credit_block = ""
    if os.path.exists(sheet):                        # the credits/sources comment written by render_myth
        s = open(sheet, encoding="utf-8").read()
        mm = re.search(r"\*\*Instagram second comment\*\* \(credits and sources\)\n```\n(.*?)\n```", s, re.S)
        credit_block = mm.group(1) if mm else ""
    sources = "Sources: " + "; ".join(m["sources"])
    second = credit_block or sources
    cap = m["caption"].strip()
    first = cap.splitlines()[0]
    tags = " ".join(m["hashtags"])
    yt_tags = ", ".join(t.lstrip("#") for t in m["hashtags"]) + (", kannada story, kannada" if lang == "kn" else
                                                                   ", hindi kahani, pauranik kahani")
    lines = [
        f"# Upload pack: video {n}, {LANG_NAME[lang]}: {m['title']}", "",
        "## Files",
        *[f"- `{f}`" for f in files],
        f"- Length: {dur:.0f} s (1080x1920, 30 fps). The master is the file to upload; the phone copy is only for "
        f"checking on the phone.", "",
        "## When to post",
        "- Instagram Reel first, around 6 PM IST; YouTube Short the same evening.",
        "- Cover: `cover.jpg` (the important part sits inside Instagram's 3:4 grid crop).", "",
        "## The facts it rests on",
        facts(mod), "",
        "## Instagram",
        f"Caption (line 1 is the hook, {len(first)} characters):",
        "```", f"{cap}\n\n{tags}", "```",
        "Pinned comment:", "```", m["pinned_comment"], "```",
        "Second comment (credits and sources):", "```", second, "```", "",
        "## YouTube",
        "Title:", "```", m["yt_title"], "```",
        "Description:", "```", f"{m['yt_description'].strip()}\n\n{second}\n\n{tags}", "```",
        "Tags:", "```", yt_tags, "```",
        "Settings: Made for kids: No. Category: Entertainment. Altered or synthetic content: No (this is clearly "
        "animated, so YouTube does not ask for it).", "",
        "## First hour",
        "- Reply to the first comments with a question back (" + ("\"Nimge yaava bhaaga tumba shock anistu?\"" if lang == "kn"
                                                                 else "\"Tumhe kaunsa part sabse ajeeb laga?\"") + ").",
        "- Pin the comment above as soon as the reel is live.",
        "- Share it to your story with a poll sticker: YES / NO.",
    ]
    path = os.path.join(folder, f"UPLOAD_VIDEO{n}_{name.upper()}_{lang.upper()}.md")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return path


def main():
    name, lang, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    cover_at = float(sys.argv[sys.argv.index("--cover-at") + 1]) if "--cover-at" in sys.argv else 2.6
    mod = load(name)
    master = os.path.join(OUT_ROOT, f"{name}_{lang}.mp4")
    folder = os.path.join(OUT_ROOT, f"upload_{name}_{lang}")
    os.makedirs(folder, exist_ok=True)
    phone = os.path.join(folder, f"{name}_{lang}_phone.mp4")
    pack_only = "--pack-only" in sys.argv          # rewrite only the upload sheet (captions/titles changed)
    if not pack_only:
        shutil.copy2(master, os.path.join(folder, os.path.basename(master)))
        subprocess.run([PY, "-I", "-X", "utf8", PHONE, master, phone], check=True)
        cover(name, lang, cover_at, os.path.join(folder, "cover.jpg"))
    files = [os.path.basename(master), os.path.basename(phone), "cover.jpg"]
    p = pack(mod, name, lang, n, folder, duration(master), files)
    print("pack:", p, flush=True)
    if "--no-drive" not in sys.argv and os.path.isdir(DRIVE):
        dst = os.path.join(DRIVE, CHANNEL_DIR, f"Video {n} {name.replace('_', ' ').title()} {LANG_NAME[lang]}")
        os.makedirs(dst, exist_ok=True)
        for f in [os.path.basename(p)] if pack_only else os.listdir(folder):
            shutil.copy2(os.path.join(folder, f), os.path.join(dst, f))
        print("drive:", dst, flush=True)


if __name__ == "__main__":
    main()
