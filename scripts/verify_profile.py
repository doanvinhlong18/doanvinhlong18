"""Check dashboard assets and source integrity; --online checks public links."""

import argparse
from datetime import date, timedelta
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import Request,urlopen
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS="{http://www.w3.org/2000/svg}"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets=[]

    def handle_starttag(self,tag,attributes):
        a=dict(attributes)
        if tag in {"script","style","iframe","canvas"}:
            raise ValueError(f"Unsupported README tag: {tag}")
        if tag=="img":
            if "alt" not in a:
                raise ValueError("README image missing alt text")
            self.assets.append(a["src"])
        if tag=="source":
            self.assets.append(a["srcset"])


def validate_svg(path,allow_native=False):
    root=ET.parse(path).getroot()
    if root.tag!=NS+"svg":
        raise ValueError(f"Invalid SVG root: {path}")
    if not allow_native and (not root.get("viewBox") or root.find(NS+"title") is None or root.find(NS+"desc") is None):
        raise ValueError(f"SVG missing viewport or accessible text: {path}")
    for key in ["width","height"]:
        if not 0<float(root.get(key,"0"))<15000:
            raise ValueError(f"Unexpected SVG {key}: {path}")
    if path.stat().st_size>4_000_000:
        raise ValueError(f"Oversized SVG: {path}")
    ids=[e.get("id") for e in root.iter() if e.get("id")]
    # Native Metrics repeats some per-chart mask IDs (for example languages-bar).
    # Keep stricter uniqueness checks for the SVGs authored in this repository.
    if not allow_native and len(ids)!=len(set(ids)):
        raise ValueError(f"Duplicate SVG IDs: {path}")
    forbidden={"script","iframe","object","embed","animate","animateMotion","animateTransform"}
    if not allow_native:
        forbidden|={"foreignObject","image","style"}
    for e in root.iter():
        tag=e.tag.rsplit("}",1)[-1]
        if tag in forbidden:
            raise ValueError(f"Unsupported SVG element {tag}: {path}")
        for key,value in e.attrib.items():
            if key.lower().startswith("on") or re.search(r"(?:javascript|vbscript):",value,re.I):
                raise ValueError(f"Active SVG content: {path}")
            if tag in {"image","img"} and key.rsplit("}",1)[-1] in {"href","src"}:
                if not value.startswith(("data:image/","#")):
                    raise ValueError(f"External image dependency: {path}")
        if tag=="style":
            css="".join(e.itertext())
            if "@import" in css or re.search(r"url\(\s*['\"]?https?://",css,re.I):
                raise ValueError(f"Remote CSS dependency: {path}")
    return root


def local():
    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    refs=References();refs.feed(readme)
    for name in refs.assets:
        if urlparse(name).scheme or not (ROOT/name).is_file():
            raise ValueError(f"Missing or nonlocal README image: {name}")
    paths=list((ROOT/"assets").rglob("*.svg"))
    for path in paths:
        validate_svg(path,allow_native=path==ROOT/"assets/metrics/github.svg")
    data=json.loads((ROOT/"assets/metrics-data.json").read_text(encoding="utf-8"))
    if data["login"]!="doanvinhlong18":
        raise ValueError("Wrong snapshot identity")
    days=data["calendar"]["days"]
    start,end=[date.fromisoformat(data["calendar"][key]) for key in ["from","through"]]
    expected=[(start+timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
    if [d["date"] for d in days]!=expected or not 176<=len(days)<=182 or start.weekday()!=6:
        raise ValueError("Incomplete or unaligned 26-week contribution data")
    for d in days:
        if type(d["count"]) is not int or d["count"]<0 or type(d["level"]) is not int or d["level"] not in range(5):
            raise ValueError("Invalid contribution count or level")
        if bool(d["count"])!=bool(d["level"]):
            raise ValueError("Contribution count/intensity disagreement")
    names=[r["name"] for r in data["repositories"]]
    if len(names)!=len(set(names)) or not names:
        raise ValueError("Invalid repository snapshot")
    for repo in data["repositories"]:
        if repo["url"]!=f"https://github.com/doanvinhlong18/{repo['name']}":
            raise ValueError("Unexpected repository URL")
        if any(type(v) is not int or v<0 for v in repo["languages"].values()):
            raise ValueError("Invalid language-byte count")
    print(f"PASS: {len(refs.assets)} README images, {len(paths)} SVGs, public repository bytes, and actual contribution counts.")


def online():
    urls={"https://github.com/doanvinhlong18","https://github.com/users/doanvinhlong18/contributions",
          "https://github.com/lowlighter","https://github.com/lowlighter/metrics"}
    for n in ["ShopCore","RAG-NEWS","RecommenderSystem","BigData"]:
        urls.add(f"https://github.com/doanvinhlong18/{n}")
    for url in sorted(urls):
        with urlopen(Request(url,headers={"User-Agent":"Profile-Verification"}),timeout=30) as response:
            if response.status!=200:
                raise ValueError(f"HTTP {response.status}: {url}")
        print(f"PASS: HTTP 200 {url}")


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--online",action="store_true");args=p.parse_args()
    try:
        local()
        if args.online:online()
    except (OSError,ValueError,KeyError,ET.ParseError) as error:
        print(f"FAIL: {error}",file=sys.stderr);return 1
    return 0


if __name__=="__main__":
    sys.exit(main())
