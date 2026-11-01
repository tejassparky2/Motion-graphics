"""WW2 Episode 1 assembly and packaging (helper 8): the 8 package parts -> one picture, plus captions, YouTube
chapters and the upload sheet, all read from the episode clock (timing.json via timing.py).

    python channels/ww2/ep01/assemble.py               # join + verify -> out/ww2/ep01/picture.mp4, and the text files
    python channels/ww2/ep01/assemble.py --text        # only captions.srt, chapters.txt and upload_sheet.md
    python channels/ww2/ep01/assemble.py --pieces 95   # also cut picture.mp4 into <=95 MB stream-copy pieces for git
    python channels/ww2/ep01/assemble.py --stub        # test run on generated stub parts (out/ww2/ep01/stub/)

Parts: out/ww2/ep01/parts/Pn.mp4, or contiguous chunks Pn_fAAAAA-BBBBB.mp4 from `render_pkg.py Pn --frames A-B`
(frame numbers count from the package's first frame; a whole Pn.mp4 wins over chunks). Each package must hold
exactly package_span("Pn") worth of frames, so a part rendered on an older clock is refused, not stretched.

The join is a stream copy (no re-encode). It is verified frame by frame: the MD5 of every decoded frame of the
picture must equal the MD5 of the same frame in its part, in order, so a gap, an overlap, a swapped part or a
dropped frame at a seam all fail. If the parts can't be stream-copied together (different encoder settings), the
join falls back to one re-encode at crf 16 and checks the frame count instead.

No burned-in captions (a long video): captions.srt carries the written script text (numbers as digits), one cue per
spoken sentence (long ones split), timed from the sentence takes.
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)
from channels.ww2.ep01.narration import split_sentences  # noqa: E402
from channels.ww2.ep01.timing import PACKAGES, Timing, package_span  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out", "ww2", "ep01")
SCRIPT = os.path.join(os.path.dirname(HERE), "ep01_script.md")
W, H, FPS = 1920, 1080, 24
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-metadata:s:v", "handler_name=", "-metadata:s:v", "encoder=", "-movflags", "+faststart"]
CHUNK = re.compile(r"^(P\d)_f(\d{5})-(\d{5})\.mp4$")
COLD_OPEN_TITLE = "The first shot"           # C0 has no card; YouTube needs a name for the 0:00 chapter


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


# ---------------------------------------------------------------- the parts and the join
def spans(T):
    """[(name, first_frame, n_frames)] on the episode clock; exits on a gap or an overlap between packages."""
    out, prev = [], 0
    for name, _, _ in PACKAGES:
        a, b = package_span(name, T)
        fa, fb = round(a * T.fps), round(b * T.fps)
        if fa != prev:
            sys.exit(f"{name} starts at frame {fa}, the previous package ends at {prev}: "
                     f"{'gap' if fa > prev else 'overlap'} of {abs(fa - prev)} frames")
        out.append((name, fa, fb - fa))
        prev = fb
    if prev != round(T.total * T.fps):
        sys.exit(f"the packages end at frame {prev}, the episode at {round(T.total * T.fps)}")
    return out


def probe(path):
    """(codec, width, height, pix_fmt, fps, packets) of the video stream; packets = frames for these encodes."""
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_read_packets", "-of", "json",
                        path]))["streams"][0]
    num, den = map(int, s["r_frame_rate"].split("/"))
    return s["codec_name"], s["width"], s["height"], s["pix_fmt"], num / den, int(s["nb_read_packets"])


def find_parts(parts_dir, name, n):
    """The files that make package `name` (n frames), in order: Pn.mp4, or chunks covering frames 0..n-1."""
    whole = os.path.join(parts_dir, f"{name}.mp4")
    if os.path.exists(whole):
        return [(whole, 0, n - 1)]
    chunks = []
    for p in glob.glob(os.path.join(parts_dir, f"{name}_f*.mp4")):
        m = CHUNK.match(os.path.basename(p))
        if m:
            chunks.append((p, int(m.group(2)), int(m.group(3))))
    if not chunks:
        return None
    chunks.sort(key=lambda c: c[1])
    nxt, problems = 0, []
    for p, a, b in chunks:
        if a != nxt:
            problems.append(f"{'gap' if a > nxt else 'overlap'} before {os.path.basename(p)} (expected f{nxt:05d})")
        nxt = b + 1
    if nxt != n:
        problems.append(f"chunks end at f{nxt - 1:05d}, the package needs f{n - 1:05d}")
    if problems:
        raise ValueError("; ".join(problems))
    return chunks


def frame_md5s(path):
    """MD5 of every decoded frame (ffmpeg framemd5), in order."""
    out = run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0", "-f", "framemd5", "-"])
    return [ln.rsplit(",", 1)[1].strip() for ln in out.splitlines() if ln and not ln.startswith("#")]


def check_parts(T, parts_dir):
    """Check every package that has landed (chunk coverage, codec, size, fps, frame counts) without joining.
    Returns (files, problems, missing); files = [(package, path, first episode frame, frames)] in order."""
    files, problems, missing = [], [], []
    print(f"clock: {'PROVISIONAL (estimated)' if T.estimated else 'voiced'}, {T.total:.3f} s, "
          f"{round(T.total * T.fps)} frames at {T.fps} fps")
    for name, f0, n in spans(T):
        try:
            got = find_parts(parts_dir, name, n)
        except ValueError as e:
            problems.append(f"{name}: {e}")
            print(f"  {name}: PROBLEM {e}")
            continue
        if got is None:
            missing.append(name)
            print(f"  {name}: episode frames {f0:5d}-{f0 + n - 1:5d} ({n:5d}, {n / T.fps:7.2f} s)  not landed")
            continue
        bad_here = []
        for path, a, b in got:
            codec, w, h, pix, fps, frames = probe(path)
            want = b - a + 1
            bad = [x for x, ok in ((f"{codec}", codec == "h264"), (f"{w}x{h}", (w, h) == (W, H)),
                                   (pix, pix == "yuv420p"), (f"{fps:g} fps", abs(fps - FPS) < 1e-6),
                                   (f"{frames} frames, needs {want}", frames == want)) if not ok]
            if bad:
                bad_here.append(f"{os.path.basename(path)}: " + ", ".join(bad))
            files.append((name, path, f0 + a, want))
        problems += bad_here
        mb = sum(os.path.getsize(p) for p, _, _ in got) / 1e6
        print(f"  {name}: episode frames {f0:5d}-{f0 + n - 1:5d} ({n:5d}, {n / T.fps:7.2f} s)  {len(got)} file"
              f"{'s' if len(got) > 1 else ''}, {mb:.0f} MB  " + ("; ".join(bad_here) if bad_here else "ok"))
    return files, problems, missing


def join(T, parts_dir, out_mp4):
    files, problems, missing = check_parts(T, parts_dir)
    if problems or missing:
        sys.exit("refusing to join:\n  " + "\n  ".join(problems + [f"{m}: not landed" for m in missing]))

    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    lst = out_mp4 + ".txt"
    with open(lst, "w") as f:
        for _, path, _, _ in files:
            f.write(f"file '{os.path.abspath(path)}'\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-map", "0:v:0", "-c", "copy",
         *CLEAN, out_mp4])
    total = sum(n for _, _, _, n in files)

    with ThreadPoolExecutor(4) as pool:                           # decoding is the slow part: run it side by side
        want_md5 = pool.map(frame_md5s, [p for _, p, _, _ in files])
        got = pool.submit(frame_md5s, out_mp4)
        want = [h for hs in want_md5 for h in hs]
        got = got.result()
    if got == want:
        how = "stream copy, every frame identical to its part"
    else:
        k = next((i for i, (x, y) in enumerate(zip(got, want)) if x != y), min(len(got), len(want)))
        print(f"stream copy differs from the parts at episode frame {k} ({len(got)} vs {len(want)} frames): "
              "re-encoding once at crf 16")
        tmp = out_mp4 + ".enc.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-map", "0:v:0",
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-bsf:v", "filter_units=remove_types=6", *CLEAN, tmp])
        run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-c", "copy", *CLEAN, out_mp4])
        os.remove(tmp)
        n = probe(out_mp4)[5]
        if n != total:
            sys.exit(f"re-encoded picture has {n} frames, needs {total}")
        how = "re-encoded at crf 16 (the parts' encoder settings differ), frame count checked"
    os.remove(lst)
    seams = [f0 for _, _, f0, _ in files[1:]]
    tags = run(["ffprobe", "-v", "error", "-show_entries", "format_tags:stream_tags", "-of", "compact", out_mp4])
    leaked = [t for t in ("encoder", "Lavf", "Lavc", "x264") if t.lower() in tags.lower()]
    print(f"{os.path.relpath(out_mp4, ROOT)}: {total} frames, {total / FPS:.3f} s, "
          f"{os.path.getsize(out_mp4) / 1e6:.1f} MB; {how}; seams at frames {seams}"
          + (f"; WARNING tags: {leaked}" if leaked else "; no encoder tags"))
    return out_mp4


def pieces(path, max_mb):
    """Cut `path` into <= max_mb stream-copy pieces at keyframes (for git's 100 MB limit) and write the join recipe.
    Joining the pieces back (concat, -c copy) gives the same frames; the MD5 of the whole file is in the recipe."""
    # cut points from the real packet sizes: the longest run of whole GOPs that stays under the limit (2% kept back
    # for the container), so a busy stretch gets a shorter piece instead of an oversized one
    pk = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time,size,flags",
              "-of", "csv=p=0", path]).split()
    pk = sorted((float(t), int(s), "K" in f) for t, s, f in (p.split(",") for p in pk))
    limit, acc, gop, cuts, t_gop = max_mb * 1e6 * 0.98, 0, 0, [], 0.0
    for t, s, key in pk:
        if key:
            if acc + gop > limit and acc > 0:
                cuts.append(t_gop)
                acc = 0
            acc += gop
            gop, t_gop = 0, t
        gop += s
    if acc + gop > limit and acc > 0:
        cuts.append(t_gop)
    stem = os.path.splitext(path)[0]
    for old in glob.glob(stem + "_piece*.mp4"):
        os.remove(old)
    run(["ffmpeg", "-y", "-v", "error", "-i", path, "-map", "0:v:0", "-c", "copy", "-f", "segment",
         *(["-segment_times", ",".join(f"{c - 0.5 / FPS:.6f}" for c in cuts)] if cuts else ["-segment_time", "1e9"]),
         "-reset_timestamps", "1", "-map_metadata", "-1", "-fflags", "+bitexact", stem + "_piece%02d.mp4"])
    got = sorted(glob.glob(stem + "_piece*.mp4"))
    big = [p for p in got if os.path.getsize(p) > max_mb * 1e6]
    if big:
        sys.exit(f"pieces over {max_mb} MB: {big}; run again with a smaller --pieces")
    with ThreadPoolExecutor(4) as pool:                           # the pieces must hold the same frames, in order
        whole_md5 = pool.submit(frame_md5s, path)
        piece_md5 = [h for hs in pool.map(frame_md5s, got) for h in hs]
        whole_md5 = whole_md5.result()
    if piece_md5 != whole_md5:
        sys.exit(f"the pieces don't match the picture frame for frame ({len(piece_md5)} vs {len(whole_md5)} frames)")
    frames = len(whole_md5)
    whole = hashlib.md5("".join(whole_md5).encode()).hexdigest()
    recipe = stem + "_pieces.txt"
    with open(recipe, "w") as f:
        f.write(f"# {len(got)} pieces of {os.path.basename(path)} ({frames} frames). Join losslessly with:\n")
        f.write("#   ffmpeg -f concat -safe 0 -i " + os.path.basename(recipe) + " -c copy "
                + os.path.basename(path) + "\n")
        f.write(f"# MD5 of all its decoded frames, in order: {whole}\n")
        for p in got:
            f.write(f"file '{os.path.basename(p)}'\n")
    print(f"{len(got)} pieces ({', '.join(f'{os.path.getsize(p) / 1e6:.0f}' for p in got)} MB), "
          f"{frames} frames -> {os.path.relpath(recipe, ROOT)}")


# ---------------------------------------------------------------- captions
def written_sentences(ln):
    """The written text (digits, as in the script) split to match the spoken takes, or None if they don't line up."""
    k = len(ln["sentences"])
    for split in (split_sentences, lambda s: re.split(r"(?<=[.?!])\s+(?=[A-Z0-9\"'])", s.strip())):
        parts = split(ln["text"])
        if len(parts) == k:
            return parts
    return None


def wrap2(text, width=42):
    """One line, or two balanced lines of at most `width` characters (None if it needs more)."""
    if len(text) <= width:
        return [text]
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) <= width and len(b) <= width:
            score = abs(len(a) - len(b)) - (8 if a.endswith((",", ";", ":")) else 0)
            if best is None or score < best[0]:
                best = (score, [a, b])
    return best[1] if best else None


def split_long(text, width=42):
    """Text in chunks that each fit two caption lines, breaking after punctuation where it can."""
    if wrap2(text, width):
        return [text]
    words, best = text.split(), None
    target = len(text) / math.ceil(len(text) / (2 * width - 4))  # even cues: 85-164 chars -> two halves, ...
    for i in range(1, len(words)):                               # every head that fits two lines, scored: close to
        head, tail = " ".join(words[:i]), " ".join(words[i:])     # the even length, a break after punctuation, never
        if not wrap2(head, width):                                # ending on a small word or leaving a stub
            continue
        score = -abs(len(head) - target)
        score += 30 if head.endswith((",", ";", ":")) and len(head) >= 0.25 * len(text) else 0
        score -= 50 if words[i - 1].lower().strip(",") in SMALL_WORDS or words[i - 1].endswith(("'s", "s'")) else 0
        score += 20 if words[i].lower() in BREAK_BEFORE else 0
        score -= 60 if len(tail) < 15 else 0
        if best is None or score > best[0]:
            best = (score, head, tail)
    return [best[1]] + split_long(best[2], width) if best else [text]


BREAK_BEFORE = {"are", "is", "was", "were", "will", "where", "when", "who", "which", "that", "while",
                "because", "but", "then", "until", "as", "on", "at", "in"}   # subtitle rule: break before a verb or link
SMALL_WORDS = {"a", "an", "the", "of", "to", "in", "on", "at", "for", "and", "or", "but", "with", "by", "from",
               "into", "as", "that", "his", "her", "its", "their", "this", "these", "those", "who", "which", "was",
               "were", "is", "are", "be", "so", "than", "more", "most", "just", "very", "had", "has", "have", "will",
               "would", "can", "could", "don't", "still", "every", "all", "two", "one", "after", "before"}


def caption_cues(T):
    d = json.load(open(os.path.join(HERE, "timing.json")))
    cues = []
    for ln in d["lines"]:
        written = written_sentences(ln)
        pieces_ = ([(s["start"], s["end"], w) for s, w in zip(ln["sentences"], written)] if written
                   else [(ln["start"], ln["end"], ln["text"])])
        for a, b, text in pieces_:
            chunks = split_long(" ".join(text.split()))
            total = sum(len(c) for c in chunks)
            t = a
            for c in chunks:
                e = t + (b - a) * len(c) / total
                cues.append([t, e, wrap2(c)])
                t = e
    for i, c in enumerate(cues):                                  # hold a beat, at least 1 s, never into the next cue
        nxt = cues[i + 1][0] - 0.05 if i + 1 < len(cues) else T.total
        c[1] = min(max(c[1] + 0.25, c[0] + 1.0), nxt)
    return cues


def ts(t, sep=","):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def write_srt(T, path):
    cues = caption_cues(T)
    with open(path, "w") as f:
        for i, (a, b, lines) in enumerate(cues, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n" + "\n".join(lines) + "\n\n")
    longest = max(len(x) for _, _, ls in cues for x in ls)
    print(f"{os.path.relpath(path, ROOT)}: {len(cues)} cues, longest line {longest} chars")


# ---------------------------------------------------------------- chapters
def script_chapter_titles():
    """{"C1": "The broken peace", "C2": "Lightning war, 1939-1940", ...} from the approved script's headings."""
    out = {}
    for m in re.finditer(r"^## Chapter (\d+): (.+?)(?: \(\d+:\d\d\))?\s*$", open(SCRIPT).read(), re.M):
        out[f"C{m.group(1)}"] = m.group(2).strip()
    return out


def clock(t):
    s = int(t)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def chapters(T):
    """[(seconds, title)] validated against YouTube's rules: first at 0:00, at least 3, each at least 10 s,
    ascending. Titles from timing.json (as on the chapter cards), with the script heading's years when it agrees."""
    d = json.load(open(os.path.join(HERE, "timing.json")))
    titles = script_chapter_titles()
    out = []
    for c in d["chapters"]:
        start = 0.0 if c["card"] is None and c["start"] == 0 else (c["card"] or [c["start"]])[0]
        script = titles.get(c["id"], "")                         # timing.json's title wins (the card); the script
        title = (COLD_OPEN_TITLE if c["id"] == "C0" else         # heading adds its years when it agrees
                 script if script.lower().startswith(c["title"].lower()) else c["title"])
        out.append((int(start), title))
    problems = []
    if not out or out[0][0] != 0:
        problems.append("the first chapter must start at 0:00")
    if len(out) < 3:
        problems.append(f"YouTube needs at least 3 chapters, there are {len(out)}")
    ends = [s for s, _ in out[1:]] + [int(T.total)]
    for (s, title), e in zip(out, ends):
        if e - s < 10:
            problems.append(f"'{title}' at {clock(s)} lasts {e - s} s (YouTube needs at least 10 s)")
    if any(b[0] <= a[0] for a, b in zip(out, out[1:])):
        problems.append("chapter times must increase")
    if problems:
        sys.exit("chapters: " + "; ".join(problems))
    return out


# ---------------------------------------------------------------- the upload sheet
def script_section(name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", open(SCRIPT).read(), re.M | re.S)
    return m.group(1).strip() if m else ""


def titles():
    sec = script_section("Title")
    main = re.search(r"\*\*(.+?)\*\*", sec).group(1)
    alts = [a.strip() for a in re.findall(r"^- (.+)$", sec, re.M)]
    return main, alts


def sources():
    """The script's source list, markdown stripped, one line each (the fact-check note above it is dropped)."""
    out = []
    for ln in re.findall(r"^- (.+)$", script_section("Sources for the numbers and dates"), re.M):
        ln = re.sub(r"\*\*(.+?)\*\*", r"\1", ln)
        ln = re.sub(r"\*(.+?)\*", r"\1", ln)
        ln = ln.replace("Dates and events from memory:", "Other dates and events:")       # public wording
        ln = ln.replace(" All are standard textbook facts (Britannica, IWM).", " Britannica; IWM.")
        ln = ln.replace("so the script says", "so the video says")
        out.append(ln)
    return out


TAGS = ["world war 2", "ww2", "world war ii", "second world war", "ww2 explained", "world war 2 explained",
        "world war 2 animated", "ww2 animated", "history", "history documentary", "1939", "1945", "blitzkrieg",
        "battle of britain", "pearl harbor", "midway", "stalingrad", "d-day", "holocaust", "hiroshima",
        "churchill", "stalin", "roosevelt", "animated history", "war map"]


def write_upload_sheet(T, chaps, path):
    main, alts = titles()
    minutes = round(T.total / 60)
    alts = [re.sub(r"\b\d+ Minutes", f"{minutes} Minutes", a) for a in alts]    # the script guessed ~10 min
    poster_ok = [a for a in alts if "stick" not in a.lower()]
    dropped = [a for a in alts if "stick" in a.lower()]
    tags = ", ".join(TAGS)
    assert len(tags) <= 500, "YouTube allows 500 characters of tags"
    chap_lines = "\n".join(f"{clock(s)} {t}" for s, t in chaps)
    desc = f"""September 1st, 1939. 4:45 in the morning. The first shots of the deadliest war in history.

The whole of World War 2 in {minutes} minutes, from the first shot to the last: how the broken peace after 1918 led \
to war, the lightning campaigns of 1939-1940, the war going global in 1941, the turning points, the Holocaust, the \
long road to Berlin and Tokyo, and the world the war left behind. Animated in the style of 1940s wartime posters and \
printed war maps.

Chapters
{chap_lines}

Sources
""" + "\n".join(f"- {s}" for s in sources()) + """

Maps: Natural Earth (public domain). Original animation; no archive footage.

#WW2 #WorldWar2 #History"""
    sheet = f"""# Upload sheet: WW2 Episode 1{' (PROVISIONAL clock: chapter times move when the voiced timing lands)' if T.estimated else ''}

Video: `WW2_Explained_Episode1.mp4` (1920x1080, 24 fps, {clock(T.total)}, sent directly; too big for git). Thumbnail: `out/ww2/ep01/thumbnail.png` (1280x720).
Captions: `out/ww2/ep01/captions.srt` (upload under Subtitles, English).

## Title
**{main}** ({len(main)} characters)

Alternatives:
""" + "\n".join(f"- {a}" for a in poster_ok) + (f"\n- (Not used: \"{dropped[0]}\". The final look is posters, not stick figures.)" if dropped else "") + f"""

## Description
```
{desc}
```

## Tags
```
{tags}
```
({len(tags)} characters of 500.)

## Pinned comment
```
When did Germany really lose the war? 1 = the day Hitler invaded the Soviet Union, 2 = the day America joined, 3 = the frozen streets of Stalingrad. Answer 1, 2 or 3 and give your reason.
```

## Settings
- Category: Education. Language: English. Captions: English (captions.srt).
- Made for kids: No. Age restriction: none (no graphic violence; the Holocaust chapter is maps, numbers and text).
- Altered or synthetic content: the narration is an AI voice reading an original script over original animation;
  no real person's likeness or voice is imitated. YouTube's label is aimed at realistic content, so "No" fits; the
  owner decides.
"""
    assert len(desc) <= 5000, f"the description is {len(desc)} characters (YouTube allows 5,000)"
    open(path, "w").write(sheet)
    print(f"{os.path.relpath(path, ROOT)}: title {len(main)} chars, {len(chaps)} chapters, {len(sources())} sources, "
          f"tags {len(tags)} chars")


# ---------------------------------------------------------------- the stub test
def make_stubs(T, parts_dir):
    """Stub parts with distinct frames (test pattern, a hue per package), P3 as three chunks, P6 as two."""
    os.makedirs(parts_dir, exist_ok=True)
    for old in glob.glob(os.path.join(parts_dir, "P*.mp4")):
        os.remove(old)
    chunked = {"P3": 3, "P6": 2}
    for k, (name, f0, n) in enumerate(spans(T)):
        cuts = [round(n * i / chunked.get(name, 1)) for i in range(chunked.get(name, 1) + 1)]
        for a, b in zip(cuts, cuts[1:]):
            out = os.path.join(parts_dir, f"{name}.mp4" if len(cuts) == 2 else f"{name}_f{a:05d}-{b - 1:05d}.mp4")
            run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                 f"testsrc2=s={W}x{H}:r={FPS},trim=start_frame={f0 + a}:end_frame={f0 + b},setpts=PTS-STARTPTS,"
                 f"hue=h={k * 45}", "-frames:v", str(b - a), "-c:v", "libx264", "-crf", "30", "-preset",
                 "ultrafast", "-g", "48", "-pix_fmt", "yuv420p", "-bsf:v", "filter_units=remove_types=6", *CLEAN,
                 out])
    print(f"stub parts -> {os.path.relpath(parts_dir, ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--text", action="store_true", help="only the captions, chapters and upload sheet")
    ap.add_argument("--stub", action="store_true", help="test run on stub parts in out/ww2/ep01/stub/")
    ap.add_argument("--check", action="store_true", help="only check the parts that have landed (no join)")
    ap.add_argument("--pieces", type=float, default=None, metavar="MB", help="also cut the picture into pieces")
    a = ap.parse_args()
    T = Timing()
    out_dir = os.path.join(OUT, "stub") if a.stub else OUT
    os.makedirs(out_dir, exist_ok=True)
    chaps = chapters(T)
    with open(os.path.join(out_dir, "chapters.txt"), "w") as f:
        f.write("\n".join(f"{clock(s)} {t}" for s, t in chaps) + "\n")
    print(f"chapters: {len(chaps)}, " + ", ".join(f"{clock(s)} {t}" for s, t in chaps))
    write_srt(T, os.path.join(out_dir, "captions.srt"))
    write_upload_sheet(T, chaps, os.path.join(out_dir, "upload_sheet.md"))
    if a.text:
        return
    parts_dir = os.path.join(out_dir, "parts")
    if a.check:
        _, problems, missing = check_parts(T, parts_dir)
        print(f"{8 - len(missing)}/8 landed, {len(problems)} problem(s)" + (f"; waiting on {', '.join(missing)}"
                                                                           if missing else ""))
        sys.exit(1 if problems else 0)
    if a.stub:
        make_stubs(T, parts_dir)
    pic = join(T, parts_dir, os.path.join(out_dir, "picture.mp4"))
    if a.pieces:
        pieces(pic, a.pieces)


if __name__ == "__main__":
    main()
