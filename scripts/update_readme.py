"""Refresh the Sydney-time block in README.md between the time markers."""
import datetime, pathlib, re
from zoneinfo import ZoneInfo

now = datetime.datetime.now(ZoneInfo("Australia/Sydney"))
stamp = now.strftime("🕒 <b>%A, %d %B %Y &nbsp;·&nbsp; %I:%M %p</b> &nbsp;<sub>Sydney time</sub>")

readme = pathlib.Path("README.md")
text = readme.read_text(encoding="utf-8")
text = re.sub(
    r"(<!--START_SECTION:time-->).*?(<!--END_SECTION:time-->)",
    r"\1\n  " + stamp + r"\n  \2",
    text,
    flags=re.S,
)
readme.write_text(text, encoding="utf-8")
print("updated:", stamp)
