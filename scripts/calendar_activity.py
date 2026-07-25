"""Refresh the Activity block in README.md from Google Calendar secret iCal feed(s).

Reads one or more comma-separated iCal URLs from the CAL_ICS_URL env var,
expands today's events (Sydney time), and writes a timeline between the
<!--START_SECTION:calendar--> markers. Only event titles + times are shown —
locations, descriptions and attendees are never read, so nothing private leaks.
"""
import datetime, os, pathlib, re
from zoneinfo import ZoneInfo

import requests
import icalendar
import recurring_ical_events

TZ = ZoneInfo("Australia/Sydney")

# First keyword match wins; default is 📌. Tweak freely.
EMOJI = [
    (("work", "shift", "socialbooth", "booth"), "💼"),
    (("uni", "lecture", "tutorial", "class", "lab", "exam", "assignment", "study", "comp"), "🎓"),
    (("boulder", "climb"), "🧗"),
    (("volley",), "🏐"),
    (("stream", "twitch"), "🟣"),
    (("osrs", "runescape"), "🧢"),
    (("gym", "workout", "run", "lift"), "🏋️"),
]


def emoji_for(title: str) -> str:
    t = title.lower()
    for keys, e in EMOJI:
        if any(k in t for k in keys):
            return e
    return "📌"


def as_sydney(value) -> datetime.datetime:
    """Normalise a date/datetime to a Sydney-aware datetime."""
    if isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=TZ)
        return value.astimezone(TZ)
    return datetime.datetime(value.year, value.month, value.day, tzinfo=TZ)


def t12(dt: datetime.datetime) -> str:
    """12-hour time, no leading zero, lowercase am/pm — e.g. 12:30pm."""
    return dt.strftime("%-I:%M%p").lower()


def collect_events(day_start, day_end):
    urls = [u.strip() for u in os.environ.get("CAL_ICS_URL", "").split(",") if u.strip()]
    events = []
    for url in urls:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        cal = icalendar.Calendar.from_ical(resp.text)
        events.extend(recurring_ical_events.of(cal).between(day_start, day_end))
    return urls, events


def render(events, now) -> str:
    rows = []
    for ev in events:
        start_raw = ev["DTSTART"].dt
        title = str(ev.get("SUMMARY", "Busy")).strip()
        all_day = not isinstance(start_raw, datetime.datetime)
        start = as_sydney(start_raw)

        if "DTEND" in ev:
            end = as_sydney(ev["DTEND"].dt)
        elif "DURATION" in ev:
            end = start + ev["DURATION"].dt
        else:
            end = None

        if all_day:
            rows.append((start, f"- **All day** · {emoji_for(title)} **{title}**"))
            continue

        is_now = start <= now < (end or start + datetime.timedelta(hours=1))
        when = t12(start) + (f"–{t12(end)}" if end else "")
        icon = "🟢" if is_now else emoji_for(title)
        tail = "  ← now" if is_now else ""
        rows.append((start, f"- {when} · {icon} **{title}**{tail}"))

    rows.sort(key=lambda r: r[0])
    heading = f"### 📅 Today · {now:%A %-d %B} (Sydney)"
    if rows:
        body = "\n".join(line for _, line in rows)
    else:
        body = "_Nothing scheduled — probably grinding OSRS_ 🧢"
    stamp = f"<sub>🔄 Updated {now:%I:%M %p} Sydney · via Google Calendar</sub>"
    return f"{heading}\n\n{body}\n\n{stamp}"


def main():
    now = datetime.datetime.now(TZ)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + datetime.timedelta(days=1)

    urls, events = collect_events(day_start, day_end)
    if not urls:
        print("CAL_ICS_URL not set — leaving README unchanged.")
        return

    content = render(events, now)
    readme = pathlib.Path("README.md")
    text = readme.read_text(encoding="utf-8")
    text = re.sub(
        r"(<!--START_SECTION:calendar-->).*?(<!--END_SECTION:calendar-->)",
        lambda m: m.group(1) + "\n" + content + "\n" + m.group(2),
        text,
        flags=re.S,
    )
    readme.write_text(text, encoding="utf-8")
    print(f"updated: {len(events)} event(s)")


if __name__ == "__main__":
    main()
