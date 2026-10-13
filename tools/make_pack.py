"""Build a download pack: python tools/make_pack.py OUT FIRST LAST [skip_name...] -> dated mp4s (e.g. 30_Oct13_930PM_name.mp4) for calendar rows FIRST..LAST, plus one combined upload sheet."""
import re
import shutil
import sys
from pathlib import Path

REPO = Path("/home/user/Motion-graphics")
OUT = Path(sys.argv[1])
FIRST, LAST = int(sys.argv[2]), int(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for line in (REPO / "out/content_calendar.md").read_text().splitlines():
    m = re.match(r"\| (\d+) \| \w+ (\w+) (\d+) \| (\d+):(\d+) (AM|PM) \| (\w+) \|", line)
    if m and FIRST <= int(m[1]) <= LAST and m[7] not in sys.argv[4:]:
        n, mon, day, hh, mm, ap, name = m.groups()
        rows.append((int(n), f"{mon}{day}_{hh}{mm if mm != '00' else ''}{ap}", line.split("|")[2].strip(),
                     f"{hh}:{mm} {ap}", name))

sheet = ["# Upload sheets, in posting order\n", "Times are IST. File numbers match the rows below.\n"]
for n, stamp, date, time, name in rows:
    fn = f"{n:02d}_{stamp}_{name}.mp4"
    shutil.copyfile(REPO / f"out/{name}.mp4", OUT / fn)
    meta = (REPO / f"out/{name}_metadata.md").read_text()
    meta = re.sub(r"^# Upload sheet: .*\n", "", meta)
    sheet.append(f"\n---\n\n## {n}. {date}, {time} IST: `{fn}`\n{meta}")
    print(fn)
(OUT / f"upload_sheets_{FIRST:02d}-{LAST:02d}.md").write_text("".join(sheet))
