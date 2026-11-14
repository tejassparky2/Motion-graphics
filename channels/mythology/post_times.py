"""When to post each finished reel: the best times from the owner's own analytics, and a running calendar that gives
every new reel the next free day (one reel per day per language channel).

The owner's numbers (14 Nov 2026, IST; "Now give me all future reels with time need to be uploaded"):
- Instagram follower active times (3-hour bars): the 6-9 PM bar is the tallest Monday to Saturday (Thursday's best
  slots 6-9 PM, 3-6 PM, 9 PM-12 AM); on Friday 12 PM-12 AM is evenly high; on Sunday the 12-3 PM bar is the tallest.
- YouTube "when your viewers are on YouTube" (last 28 days): brightest at 8-9 PM every evening (Tue-Thu strongest),
  7-8 PM on Friday and Saturday; on Sunday 12-3 PM is as bright as the evening; midnight-6 AM is empty.
So: post the Reel as the evening rise starts (6 PM) and the Short at 7:30 PM, so its first hour runs into the 8-9 PM
peak; on Sunday post both around noon.

The calendar lives in myth_out/posting_calendar.json ({lang: {"YYYY-MM-DD": video}}); POSTING_SCHEDULE.md beside it
is rewritten from it every time (and copied to Drive by finish.py).
"""
import datetime as dt
import json
import os

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
# weekday (Monday = 0) -> (Instagram Reel time, YouTube Short time), IST
BEST = {d: ("6:00 PM", "7:30 PM") for d in range(6)}
BEST[6] = ("12:00 PM", "12:30 PM")
WHY = ("Why these times: your Instagram followers are most active 6-9 PM (Sunday: 12-3 PM), and your YouTube viewers "
       "peak 8-9 PM, so a Short posted at 7:30 PM gets its first hour right before the peak. On Sunday both peak "
       "around noon.")
LONG_TIME = {d: "7:00 PM" for d in range(6)}
LONG_TIME[6] = "12:00 PM"
LANG_NAME = {"hi": "Hindi", "kn": "Kannada"}


def _path(out_root):
    return os.path.join(out_root, "posting_calendar.json")


def load(out_root):
    p = _path(out_root)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save(out_root, cal):
    json.dump(cal, open(_path(out_root), "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


def first_free(cal, lang, now=None, sunday_only=False):
    """The first day from now whose posting time hasn't passed and that has no video booked in this calendar
    (long videos: Sundays only)."""
    now = now or dt.datetime.now()
    taken = set(cal.get(lang, {}))
    day = now.date()
    for _ in range(400):
        ig = dt.datetime.strptime((LONG_TIME if sunday_only else {d: v[0] for d, v in BEST.items()})[day.weekday()],
                                  "%I:%M %p").time()
        if sunday_only and day.weekday() != 6:
            day += dt.timedelta(days=1)
            continue
        if day.isoformat() not in taken and (day > now.date() or now.time() < ig):
            return day
        day += dt.timedelta(days=1)
    raise RuntimeError("no free day found")


def book(out_root, name, lang, now=None, long=False):
    """The posting day of this video: its booked day if it has one, else the next free day (booked now). Long videos
    have their own calendar (key "<lang>-long") and go out on Sundays at noon."""
    key = f"{lang}-long" if long else lang
    cal = load(out_root)
    for d, v in cal.get(key, {}).items():
        if v == name:
            return dt.date.fromisoformat(d)
    day = first_free(cal, key, now, sunday_only=long)
    cal.setdefault(key, {})[day.isoformat()] = name
    save(out_root, cal)
    return day


def when_lines(day, long=False):
    """The 'When to post' lines of an upload sheet."""
    label = f"{DAYS[day.weekday()]}, {day.day} {day.strftime('%b %Y')}"
    if long:
        return [f"- **{label}: YouTube at {LONG_TIME[day.weekday()]} IST** (a normal long video, not a Short).",
                "- " + WHY]
    ig, yt = BEST[day.weekday()]
    return [f"- **{label}: Instagram Reel at {ig} IST, YouTube Short at {yt} IST.**",
            "- If that day is missed, post on the next free day at that day's times (Monday-Saturday 6:00 PM / "
            "7:30 PM, Sunday 12:00 PM / 12:30 PM), one reel a day.",
            "- " + WHY]


def schedule_md(out_root, titles=None, today=None):
    """Rewrite POSTING_SCHEDULE.md (upcoming reels first, then the ones whose day has passed) and return its path."""
    titles = titles or {}
    today = today or dt.date.today()
    cal = load(out_root)
    rows_up, rows_past = [], []
    for lang, days in sorted(cal.items()):
        for d, v in sorted(days.items()):
            day = dt.date.fromisoformat(d)
            long = lang.endswith("-long")
            base = lang[:-5] if long else lang
            ig, yt = ("-", LONG_TIME[day.weekday()] + " (long video)") if long else BEST[day.weekday()]
            row = (f"| {DAYS[day.weekday()][:3]} {day.day} {day.strftime('%b')} | {LANG_NAME.get(base, base)} | "
                   f"{titles.get((v, base), v)} | {ig} | {yt} |")
            (rows_up if day >= today else rows_past).append((d, row))
    head = ["| Day | Channel | Reel | Instagram Reel | YouTube Short |", "|---|---|---|---|---|"]
    lines = ["# Posting schedule (IST)", "",
             "One reel a day per channel. Monday-Saturday: Instagram 6:00 PM, YouTube 7:30 PM. "
             "Sunday: Instagram 12:00 PM, YouTube 12:30 PM.", "", WHY, "", "## Coming up", *head,
             *[r for _, r in sorted(rows_up)]]
    if rows_past:
        lines += ["", "## Day already passed (post at the next free slot if not posted yet)", *head,
                  *[r for _, r in sorted(rows_past)]]
    p = os.path.join(out_root, "POSTING_SCHEDULE.md")
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return p
