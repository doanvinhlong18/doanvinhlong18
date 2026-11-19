"""Validate a native lowlighter/metrics render, then use it as the overview image."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from verify_profile import validate_svg

ROOT=Path(__file__).resolve().parents[1]
NS="http://www.w3.org/2000/svg"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    args=parser.parse_args()
    validate_svg(args.source,allow_native=True)
    tree=ET.parse(args.source)
    root=tree.getroot()
    ET.register_namespace("",NS)
    # Metrics calls contribution counts "commits" in these labels; make the meaning precise.
    for element in root.iter():
        for attr in ["text","tail"]:
            value=getattr(element,attr)
            if value:
                value=value.replace("Commits streaks","Contribution streaks").replace("Commits per day","Contributions per day")
                setattr(element,attr,value)
    root.set("role","img")
    root.set("aria-labelledby","native-metrics-title native-metrics-desc")
    if not root.get("viewBox"):
        root.set("viewBox",f"0 0 {root.get('width')} {root.get('height')}")
    title=ET.Element(f"{{{NS}}}title",{"id":"native-metrics-title"})
    title.text="Public GitHub overview — lowlighter/metrics"
    desc=ET.Element(f"{{{NS}}}desc",{"id":"native-metrics-desc"})
    desc.text="Public repository overview, isometric contribution calendar, and programming-language bytes. Notebook and markup bytes are excluded. Participation is not a skill ranking."
    root.insert(0,title)
    root.insert(1,desc)
    destination=ROOT/"assets/metrics/github.svg"
    temporary=destination.with_suffix(".svg.tmp")
    tree.write(temporary,encoding="utf-8",xml_declaration=False)
    validate_svg(temporary,allow_native=True)
    temporary.replace(destination)
    print("Adopted the validated native Metrics render.")


if __name__=="__main__":
    main()
