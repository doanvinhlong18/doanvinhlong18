"""Validate local profile assets; optionally check public links with --online."""

import argparse
from datetime import date, timedelta
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            if "alt" not in attrs:
                raise ValueError("Image missing alt attribute")
            self.assets.append(attrs["src"])
        if tag == "source":
            self.assets.append(attrs["srcset"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if tag in {"script", "style", "iframe", "canvas"}:
            raise ValueError(f"Unsupported README element: {tag}")


def local_checks():
    readme = (ROOT/"README.md").read_text(encoding="utf-8")
    refs = References()
    refs.feed(readme)
    for asset in refs.assets:
        if urlparse(asset).scheme or not (ROOT/asset).is_file():
            raise ValueError(f"Missing or nonlocal README image: {asset}")
    headings = {re.sub(r"[^\w\- ]", "", x.lower()).replace(" ", "-")
                for x in re.findall(r"^## (.+)$", readme, re.M)}
    for anchor in refs.anchors:
        if anchor not in headings:
            raise ValueError(f"Missing navigation anchor: {anchor}")
    paths = list((ROOT/"assets").rglob("*.svg"))
    for path in paths:
        tree = ET.parse(path)
        root = tree.getroot()
        if root.tag != SVG+"svg" or "viewBox" not in root.attrib:
            raise ValueError(f"Invalid SVG root: {path}")
        width,height = (float(root.attrib[k]) for k in ["width","height"])
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid dimensions: {path}")
        if root.find(SVG+"title") is None or root.find(SVG+"desc") is None:
            raise ValueError(f"SVG missing accessible title/description: {path}")
        ids = [el.attrib["id"] for el in root.iter() if "id" in el.attrib]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate SVG ID: {path}")
        for element in root.iter():
            tag = element.tag.rsplit("}",1)[-1]
            if tag in {"script","foreignObject","image","iframe"}:
                raise ValueError(f"Unsupported SVG element {tag}: {path}")
            if path.name != "hero-animated.svg" and tag in {"animate","animateMotion","animateTransform","style"}:
                raise ValueError(f"Unexpected motion in static asset: {path}")
            for key,value in element.attrib.items():
                if key.lower().startswith("on"):
                    raise ValueError(f"SVG event handler: {path}")
                if key.endswith("href") and not value.startswith("#"):
                    raise ValueError(f"External SVG dependency: {path}")
                for target in re.findall(r"url\(#([^)]+)\)",value):
                    if target not in ids:
                        raise ValueError(f"Unresolved SVG reference {target}: {path}")
        if path.stat().st_size > 500_000:
            raise ValueError(f"Unnecessarily large SVG: {path}")
    snapshot = json.loads((ROOT/"assets/activity-data.json").read_text(encoding="utf-8"))
    start,end = date.fromisoformat(snapshot["from"]),date.fromisoformat(snapshot["through"])
    expected = [(start+timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
    if [d["date"] for d in snapshot["days"]] != expected:
        raise ValueError("Activity dates must be contiguous, sorted, and match source range")
    if any(type(d["level"]) is not int or d["level"] not in range(5) for d in snapshot["days"]):
        raise ValueError("Invalid activity intensity")
    if len(snapshot["days"]) < 176:
        raise ValueError("Insufficient source history for 26 calendar columns")
    print(f"PASS: {len(refs.assets)} local image references, {len(paths)} SVGs, navigation, and activity data.")


def online_checks():
    urls = {"https://github.com/doanvinhlong18", "https://github.com/users/doanvinhlong18/contributions"}
    for name in ["ShopCore","RAG-NEWS","RecommenderSystem","BigData"]:
        urls.add(f"https://github.com/doanvinhlong18/{name}")
    for url in sorted(urls):
        with urlopen(Request(url,headers={"User-Agent":"Profile-Verification/1.0"}),timeout=30) as response:
            if response.status != 200:
                raise ValueError(f"HTTP {response.status}: {url}")
            if urlparse(response.url).hostname != "github.com":
                raise ValueError(f"Unexpected redirect: {url}")
            print(f"PASS: HTTP 200 {url}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online",action="store_true")
    args=parser.parse_args()
    try:
        local_checks()
        if args.online:
            online_checks()
    except (OSError, ValueError, ET.ParseError, KeyError) as error:
        print(f"FAIL: {error}",file=sys.stderr)
        return 1
    return 0


if __name__=="__main__":
    sys.exit(main())
