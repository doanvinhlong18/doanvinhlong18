"""Render a compact Metrics-inspired profile from a checked-in public snapshot."""

from collections import Counter
from datetime import date, timedelta
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BG = "#0D1117"
SURFACE = "#101722"
BORDER = "#28364A"
FG = "#E6EDF3"
MUTED = "#9BAEC4"
BLUE = "#79B8FF"
PURPLE = "#B4A2FF"
CYAN = "#56D4DD"
LANGUAGE_COLORS = {"Java": "#F2A766", "Python": "#78B7E6", "JavaScript": "#EBD76C",
                   "TypeScript": "#8CA7FF", "PowerShell": "#B4A2FF", "Shell": "#89D5A4",
                   "SQL": "#68CBC1", "PLpgSQL": "#68CBC1", "C++": "#E8A1C1", "C": "#ABB5C7"}
# Match the optional native Metrics workflow; notebook/markup bytes are not code proficiency.
IGNORED = {"Jupyter Notebook", "HTML", "CSS", "SCSS", "Less", "Jinja", "Dockerfile", "Batchfile", "Handlebars"}


def t(x, y, value, size=15, fill=FG, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def rule(y, x=26, width=428):
    return f'<path d="M{x} {y}h{width}" stroke="{BORDER}"/>'


def svg(width, height, title, description, body, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>{defs}</defs><g font-family="Segoe UI, Arial, sans-serif">{body}</g></svg>
'''


def panel(height=866):
    return f'<rect x="0.5" y="0.5" width="479" height="{height-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>'


def icon(x, y, kind, color=BLUE, scale=1):
    paths = {
        "repo": '<rect x="4" y="2" width="15" height="20" rx="2"/><path d="M4 17h15M8 6h7m-7 4h4"/>',
        "calendar": '<rect x="3" y="5" width="18" height="17" rx="2"/><path d="M7 2v6m10-6v6M3 11h18m-13 5h2m4 0h2"/>',
        "code": '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-2-15-4 18"/>',
        "backend": '<rect x="3" y="2" width="18" height="8" rx="2"/><rect x="3" y="14" width="18" height="8" rx="2"/><path d="M7 6h6m-6 12h6m4-12h1m-1 12h1"/>',
        "network": '<rect x="8" y="1" width="8" height="7" rx="1"/><rect x="1" y="16" width="8" height="7" rx="1"/><rect x="15" y="16" width="8" height="7" rx="1"/><path d="M12 8v4m-7 4v-4h14v4"/>',
        "data": '<ellipse cx="12" cy="5" rx="9" ry="4"/><path d="M3 5v14c0 5 18 5 18 0V5M3 12c0 5 18 5 18 0"/>',
        "ai": '<path d="m12 1 10 6v10l-10 6-10-6V7Zm0 0v22M2 7l20 10m0-10L2 17"/>',
    }
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'


def header(mobile=False):
    w,h = (480,206) if mobile else (960,168)
    out=[f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>',
         t(26,32,"doanvinhlong18 / engineering profile",12,MUTED,400,'font-family="Consolas, monospace"'),
         t(26,86,"Doan Vinh Long",36 if mobile else 44,FG,650,'letter-spacing="-1"'),
         t(27,120,"Java Backend Developer",18,BLUE,500)]
    if mobile:
        out += [rule(145,26,428),t(26,177,"RELIABLE SYSTEMS",11,MUTED,500,'letter-spacing="2"'),
                t(26,194,"DISTRIBUTED THINKING · INTELLIGENT SOFTWARE",9,PURPLE,500,'letter-spacing="0.8"')]
    else:
        out += [t(27,146,"Reliable systems. Distributed thinking. Intelligent software.",13,MUTED)]
        # Restrained isometric mark; the contribution calendar carries the main 3D visual.
        out += ['<g transform="translate(821 39)" fill="none" stroke-width="1.3">',
                f'<path d="m0 24 42-24 42 24v48L42 96 0 72Z" stroke="{PURPLE}" opacity="0.6"/>',
                f'<path d="m0 24 42 24 42-24M42 48v48" stroke="{BLUE}" opacity="0.65"/>',
                f'<path d="m20 36 22-12 22 12v25L42 74 20 61Z" stroke="{CYAN}"/>',
                f'<path d="m20 36 22 13 22-13M42 49v25" stroke="{CYAN}" opacity="0.65"/>','</g>']
    return svg(w,h,"Doan Vinh Long — Java Backend Developer",
               "Reliable systems. Distributed thinking. Intelligent software.","".join(out))


def calendar(data):
    """Isometric columns based on the Metrics plugin's projection; actual counts only.

    Reference: lowlighter/metrics source/plugins/isocalendar/index.mjs (MIT).
    This is an independent SVG renderer, not the native Metrics engine.
    """
    days = data["calendar"]["days"]
    start = date.fromisoformat(days[0]["date"])
    maximum = max(d["count"] for d in days)
    colors = ["#1A2638", "#3C4687", "#6664BC", "#9290E3", "#B8B2FF"]
    dx,dy = 10.7,5.35
    blocks=[]
    for day in days:
        offset=(date.fromisoformat(day["date"])-start).days
        week,weekday=divmod(offset,7)
        x=104+(week-weekday)*11.2
        base=272+(week+weekday)*5.6
        height=1.5+54*(day["count"]/maximum if maximum else 0)
        y=base-height
        color=colors[day["level"]]
        def poly(coords,factor=1):
            points=" ".join(f"{a:.2f},{b:.2f}" for a,b in coords)
            shaded="#"+"".join(f"{round(int(color[i:i+2],16)*factor):02x}" for i in [1,3,5])
            return f'<polygon points="{points}" fill="{shaded}" stroke="{BG}" stroke-width="0.6"/>'
        shape=(f'<g><title>{day["date"]}: {day["count"]} contributions</title>'+
               poly([(x-dx,y),(x,y+dy),(x,base+dy),(x-dx,base)],0.65)+
               poly([(x,y+dy),(x+dx,y),(x+dx,base),(x,base+dy)],0.4)+
               poly([(x,y-dy),(x+dx,y),(x,y+dy),(x-dx,y)])+'</g>')
        blocks.append((week+weekday,week,shape))
    return ''.join(shape for _,__,shape in sorted(blocks))


def languages(data):
    totals=Counter()
    for repo in data["repositories"]:
        if not repo["fork"]:
            totals.update({k:v for k,v in repo["languages"].items() if k not in IGNORED})
    return totals


def overview(data):
    totals=languages(data)
    ranked=totals.most_common(5)
    remainder=sum(totals.values())-sum(count for _,count in ranked)
    if remainder:
        ranked.append(("Other",remainder))
    total=sum(totals.values())
    through=data["calendar"]["through"]
    contribution_total=sum(d["count"] for d in data["calendar"]["days"])
    out=[panel(),icon(26,22,"repo"),t(60,41,"GitHub overview",20,BLUE,600),
         t(26,69,"@doanvinhlong18",13,MUTED),
         t(26,122,len(data["repositories"]),34,FG,650),t(26,147,"public repositories",13,MUTED),
         t(258,122,len(totals),34,FG,650),t(258,147,"code languages",13,MUTED),rule(171),
         icon(26,193,"calendar",PURPLE),t(60,212,"Contribution landscape",19,PURPLE,600),
         t(26,240,"26 WEEKS · ISOMETRIC VIEW",10,MUTED,500,'letter-spacing="1.5"'),calendar(data),
         t(26,467,f"{contribution_total:,} contributions in the displayed period",13,FG),
         t(26,490,f"{data['calendar']['from']}  —  {through}",11,MUTED),rule(513),
         icon(26,535,"code",CYAN),t(60,554,"Languages in public code",19,CYAN,600)]
    x=26
    for name,count in ranked:
        size=428*count/total if total else 0
        color=LANGUAGE_COLORS.get(name,"#9AAAC4")
        out.append(f'<rect x="{x:.3f}" y="577" width="{size:.3f}" height="9" fill="{color}"/>')
        x+=size
    for i,(name,count) in enumerate(ranked):
        y=617+i*28
        color=LANGUAGE_COLORS.get(name,"#9AAAC4")
        out += [f'<circle cx="32" cy="{y-5}" r="4" fill="{color}"/>',t(45,y,name,14),
                t(454,y,f"{count/total:.1%}" if total else "0.0%",13,MUTED,400,'text-anchor="end"')]
    out += [rule(798),t(26,824,"Repository bytes · excludes notebooks and markup",10,MUTED),
            t(26,845,f"Public snapshot · {through}",10,MUTED)]
    description=(f"Public GitHub snapshot through {through}: {len(data['repositories'])} repositories, "
                 f"{contribution_total} contributions in the displayed 26-week period. "
                 "Language shares are repository bytes excluding notebook and markup files, not proficiency.")
    return svg(480,866,"GitHub overview, isometric contributions, and code languages",description,"".join(out))


def engineering():
    out=[panel(),t(26,36,"ENGINEERING / FIELD NOTES",10,MUTED,500,'letter-spacing="1.7"'),
         t(26,78,"Backend, with intent.",29,FG,600,'letter-spacing="-0.5"'),
         t(26,108,"Java developer · 2+ years",17,BLUE,500),
         t(26,137,"Enterprise applications, careful boundaries,",13,MUTED),
         t(26,158,"and an interest in intelligent systems.",13,MUTED),rule(182)]
    rows=[("backend","Backend engineering","Java · Spring Boot · REST · SQL","Transaction boundaries and application design."),
          ("network","Distributed systems","Kafka · messaging · concurrency","Project work and continuing systems study."),
          ("data","Data & search","PostgreSQL · SQL Server · BM25 · FAISS","Relational modeling and hybrid retrieval."),
          ("ai","Applied AI","Embeddings · reranking · RAG","Experiments in intelligent data processing.")]
    for i,(kind,title,stack,desc) in enumerate(rows):
        y=209+i*94
        color=BLUE if i%2==0 else PURPLE
        out += [icon(26,y,kind,color),t(62,y+18,title,17,color,600),
                t(62,y+45,stack,14,FG),t(62,y+66,desc,12,MUTED)]
    out += [rule(591),t(26,623,"CURRENTLY EXPLORING",10,CYAN,600,'letter-spacing="1.8"')]
    for y,value in [(653,"Service contracts · gRPC · Redis"),(678,"RabbitMQ integration · performance"),(703,"Elasticsearch · entity matching")]:
        out += [f'<circle cx="30" cy="{y-5}" r="2" fill="{CYAN}"/>',t(43,y,value,14,FG)]
    out += [rule(727),t(26,757,"A FEW ENGINEERING DEFAULTS",10,MUTED,500,'letter-spacing="1.5"'),
            t(26,786,"Correctness first. Measure before scaling.",14,FG),
            t(26,810,"Make failures visible. Keep the design simple.",13,MUTED),
            t(26,845,"Core practice · public projects · ongoing study",10,MUTED)]
    return svg(480,866,"Engineering focus and working toolkit",
               "Java backend developer with 2+ years of self-reported professional experience in enterprise applications. "
               "Project and research topics include distributed systems, data and search, and applied AI. "
               "Learning areas: gRPC, Redis, RabbitMQ, performance, Elasticsearch, and entity matching.","".join(out))


def outputs(data):
    return {"profile-header.svg":header(),"profile-header-mobile.svg":header(mobile=True),
            "metrics/github.svg":overview(data),"metrics/engineering.svg":engineering(),
            "spacer.svg":svg(1,1,"Layout spacer","Decorative line break between floated infographic columns.",'<path d="M0 0" fill="none"/>')}


def write_outputs(rendered):
    # Build all strings first. Write sibling temporary files, then replace final outputs.
    for name,content in rendered.items():
        target=ASSETS/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.with_suffix(target.suffix+".tmp").write_text(content,encoding="utf-8",newline="\n")
    for name in rendered:
        target=ASSETS/name
        target.with_suffix(target.suffix+".tmp").replace(target)


def main():
    data=json.loads((ASSETS/"metrics-data.json").read_text(encoding="utf-8"))
    write_outputs(outputs(data))
    print("Built 5 Metrics-inspired profile assets from the saved public snapshot.")


if __name__=="__main__":
    main()
