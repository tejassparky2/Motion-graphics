"""Build a download pack in a chosen posting order (not calendar order):

  python tools/make_order_pack.py OUT LABEL name1 name2 ...

-> OUT/01_name1.mp4, OUT/02_name2.mp4, ... plus OUT/upload_sheets_LABEL.md with each video's upload sheet in that
order. Used since the 26 Oct re-cut, when the posting order stopped following the calendar row numbers."""
import re
import shutil
import sys
from pathlib import Path

REPO = Path("/home/user/Motion-graphics")
OUT, LABEL, NAMES = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
OUT.mkdir(parents=True, exist_ok=True)

sheet = ["# Upload sheets, in posting order\n",
         "Post one at 4:30 PM IST and one at 7:30 PM IST, in the order of the file numbers.\n"]
for k, name in enumerate(NAMES, 1):
    if not (REPO / f"out/{name}.mp4").exists():
        print(f"skipped {name}: not rendered yet")
        continue
    fn = f"{k:02d}_{name}.mp4"
    shutil.copyfile(REPO / f"out/{name}.mp4", OUT / fn)
    meta = re.sub(r"^# Upload sheet: .*\n", "", (REPO / f"out/{name}_metadata.md").read_text())
    sheet.append(f"\n---\n\n## {k}. `{fn}`\n{meta}")
    print(fn)
(OUT / f"upload_sheets_{LABEL}.md").write_text("".join(sheet))
