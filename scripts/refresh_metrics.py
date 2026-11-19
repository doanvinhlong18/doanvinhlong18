"""Fetch public GitHub data and refresh the cached profile. No token required."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen

from render_profile import outputs, write_outputs

ROOT=Path(__file__).resolve().parents[1]
LOGIN="doanvinhlong18"
CALENDAR=f"https://github.com/users/{LOGIN}/contributions"


def fetch(url, as_json=True):
    request=Request(url,headers={"User-Agent":"doanvinhlong18-profile/2.0","Accept-Language":"en-US"})
    with urlopen(request,timeout=30) as response:
        if response.status!=200:
            raise ValueError(f"Unexpected HTTP {response.status} fetching public GitHub data")
        data=response.read().decode("utf-8")
    return json.loads(data) if as_json else data


class Contributions(HTMLParser):
    """Join GitHub calendar cells to their count tooltips; never invent counts."""
    def __init__(self):
        super().__init__()
        self.cells={}
        self.labels={}
        self.current=None

    def handle_starttag(self,tag,attributes):
        a=dict(attributes)
        if tag=="td" and all(k in a for k in ["data-date","data-level","id"]):
            day=date.fromisoformat(a["data-date"])
            level=int(a["data-level"])
            if level not in range(5) or a["id"] in self.cells:
                raise ValueError("Invalid or duplicate calendar cell")
            self.cells[a["id"]]={"date":day.isoformat(),"level":level}
        if tag=="tool-tip" and "for" in a:
            self.current=a["for"]
            self.labels[self.current]=""

    def handle_data(self,text):
        if self.current is not None:
            self.labels[self.current]+=text

    def handle_endtag(self,tag):
        if tag=="tool-tip":
            self.current=None

    def snapshot(self,as_of):
        parsed={}
        for key,cell in self.cells.items():
            label=self.labels.get(key,"").strip()
            match=re.match(r"([\d,]+) contributions?\b",label)
            if match:
                count=int(match[1].replace(",",""))
            elif re.match(r"No contributions\b",label):
                count=0
            else:
                raise ValueError("Contribution count missing from source tooltip")
            if bool(count)!=bool(cell["level"]):
                raise ValueError("Source contribution count and intensity disagree")
            day=date.fromisoformat(cell["date"])
            if day<=as_of:
                if day in parsed:
                    raise ValueError("Duplicate contribution date")
                parsed[day]={**cell,"count":count}
        if not parsed:
            raise ValueError("No contribution dates found")
        end=max(parsed)
        if as_of-end>timedelta(days=2):
            raise ValueError("Stale contribution source")
        start=end-timedelta(days=(end.weekday()+1)%7,weeks=25)
        dates=[start+timedelta(days=i) for i in range((end-start).days+1)]
        if any(d not in parsed for d in dates):
            raise ValueError("Incomplete contribution source")
        return {"source":CALENDAR,"from":start.isoformat(),"through":end.isoformat(),
                "days":[parsed[d] for d in dates]}


def snapshot(as_of):
    repos=[]
    page=1
    while True:
        batch=fetch(f"https://api.github.com/users/{LOGIN}/repos?per_page=100&sort=full_name&page={page}")
        if not isinstance(batch,list):
            raise ValueError("Unexpected repository list")
        repos.extend(batch)
        if len(batch)<100:
            break
        page+=1

    def load_languages(repo):
        if repo["private"]:
            raise ValueError("Public source unexpectedly contained a private repository")
        values=fetch(repo["languages_url"])
        if not isinstance(values,dict) or any(type(v) is not int or v<0 for v in values.values()):
            raise ValueError("Invalid repository language data")
        return {"name":repo["name"],"url":repo["html_url"],"fork":repo["fork"],"languages":values}

    with ThreadPoolExecutor(max_workers=4) as pool:
        languages=list(pool.map(load_languages,repos))
    parser=Contributions()
    parser.feed(fetch(CALENDAR,as_json=False))
    return {"login":LOGIN,"fetched_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources":[f"https://api.github.com/users/{LOGIN}/repos",CALENDAR],
            "repositories":languages,"calendar":parser.snapshot(as_of)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date",type=date.fromisoformat,default=datetime.now(timezone.utc).date())
    args=parser.parse_args()
    try:
        data=snapshot(args.date)
        rendered=outputs(data)
        rendered["metrics-data.json"]=json.dumps(data,indent=2)+"\n"
        # No writes happen until the entire fetch, source validation, and render succeed.
        write_outputs(rendered)
        print(f"Refreshed {len(data['repositories'])} public repositories and a real 26-week contribution calendar.")
    except (OSError,ValueError,KeyError) as error:
        print(f"Refresh failed; previous snapshot retained: {error}",file=sys.stderr)
        return 1
    return 0


if __name__=="__main__":
    sys.exit(main())
