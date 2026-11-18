"""Refresh a dated public activity snapshot; keep old files if fetching fails."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = "https://github.com/users/doanvinhlong18/contributions"
COLORS = ["#172237", "#343B78", "#545AC2", "#8583EA", "#B1ADF9"]


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag != "td" or "data-date" not in attrs or "data-level" not in attrs:
            return
        day = date.fromisoformat(attrs["data-date"])
        level = int(attrs["data-level"])
        if not 0 <= level <= 4:
            raise ValueError("Unexpected GitHub contribution level")
        if day in self.days:
            raise ValueError("Duplicate GitHub contribution date")
        self.days[day] = level


def svg(snapshot, mobile=False):
    width, height = (640, 330) if mobile else (1200, 290)
    weeks = 13 if mobile else 26
    end = date.fromisoformat(snapshot["through"])
    end_sunday = end - timedelta(days=(end.weekday() + 1) % 7)
    start = end_sunday - timedelta(weeks=weeks-1)
    levels = {date.fromisoformat(row["date"]): row["level"] for row in snapshot["days"]}
    step, cell = (39, 28) if mobile else (40, 28)
    x0, y0 = (86, 104) if mobile else (104, 93)
    font = 'font-family="Segoe UI, Arial, sans-serif"'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">Public GitHub activity — dated snapshot</title>',
           f'<desc id="desc">{weeks} weeks of contribution intensity through {end.isoformat()}, fetched {escape(snapshot["fetched_at"])}. Source: GitHub. Not a measure of engineering skill.</desc>',
           f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="18" fill="#080B14" stroke="#29314B"/>',
           f'<g {font}>',
           '<text x="32" y="37" fill="#A78BFA" font-size="11" font-weight="600" letter-spacing="2">PUBLIC CONTRIBUTION RHYTHM</text>']
    # Fit 7 weekday rows into a restrained panel.
    row_step, row_cell = (22,16) if mobile else (19,13)
    for weekday, label in [(1,"MON"),(3,"WED"),(5,"FRI")]:
        out.append(f'<text x="32" y="{y0+weekday*row_step+row_cell-2}" fill="#A7B3C8" font-size="10">{label}</text>')
    previous_month = None
    for week in range(weeks):
        sunday = start + timedelta(weeks=week)
        x = x0 + week*step
        if sunday.month != previous_month:
            out.append(f'<text x="{x}" y="{y0-14}" fill="#A7B3C8" font-size="11">{sunday.strftime("%b").upper()}</text>')
            previous_month = sunday.month
        for weekday in range(7):
            day = sunday + timedelta(days=weekday)
            if day > end:
                continue
            level = levels[day]
            out.append(f'<rect x="{x}" y="{y0+weekday*row_step}" width="{cell}" height="{row_cell}" rx="3" fill="{COLORS[level]}"><title>{day.isoformat()}: intensity {level}/4</title></rect>')
    footer_y = height-25
    out.append(f'<text x="32" y="{footer_y}" fill="#A7B3C8" font-size="11">THROUGH {end.isoformat()} · {weeks} WEEKS</text>')
    legend_x = width-205
    out.append(f'<text x="{legend_x-30}" y="{footer_y}" fill="#A7B3C8" font-size="10">LESS</text>')
    for i,color in enumerate(COLORS):
        out.append(f'<rect x="{legend_x+8+i*22}" y="{footer_y-10}" width="16" height="12" rx="2" fill="{color}"/>')
    out.append(f'<text x="{legend_x+125}" y="{footer_y}" fill="#A7B3C8" font-size="10">MORE</text></g></svg>\n')
    return "\n".join(out)


def fetch_snapshot(as_of):
    request = Request(SOURCE, headers={"User-Agent": "doanvinhlong18-profile-activity/1.0"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"GitHub returned HTTP {response.status}")
        html = response.read().decode("utf-8")
    parser = CalendarParser()
    parser.feed(html)
    usable = [day for day in parser.days if day <= as_of]
    if not usable:
        raise ValueError("No contribution dates found; GitHub markup may have changed")
    end = max(usable)
    if as_of - end > timedelta(days=2):
        raise ValueError("GitHub contribution calendar is stale")
    # 26 calendar columns, aligned to Sunday, including the current partial week.
    start = end - timedelta(days=(end.weekday()+1) % 7, weeks=25)
    days = [start+timedelta(days=i) for i in range((end-start).days+1)]
    if any(day not in parser.days for day in days):
        raise ValueError("Contribution calendar has missing dates; old assets retained")
    return {"source": SOURCE,
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "from": start.isoformat(), "through": end.isoformat(),
            "days": [{"date": day.isoformat(), "level": parser.days[day]} for day in days]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=datetime.now(timezone.utc).date(),
                        help="Snapshot cutoff in YYYY-MM-DD (default: current UTC date)")
    args = parser.parse_args()
    try:
        snapshot = fetch_snapshot(args.date)
        # Prepare every output before changing any existing files.
        outputs = {"activity-data.json": json.dumps(snapshot, indent=2)+"\n",
                   "activity.svg": svg(snapshot), "activity-mobile.svg": svg(snapshot, mobile=True)}
        ASSETS.mkdir(exist_ok=True)
        for name, content in outputs.items():
            (ASSETS/(name+".tmp")).write_text(content, encoding="utf-8", newline="\n")
        for name in outputs:
            (ASSETS/(name+".tmp")).replace(ASSETS/name)
        print(f"Updated public activity: {snapshot['from']} to {snapshot['through']}.")
    except (OSError, ValueError, KeyError) as error:
        print(f"Activity refresh failed; existing snapshot retained: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
