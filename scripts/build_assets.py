"""Build original, self-contained profile SVGs. Python standard library only."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
INK = "#E5E7EB"
MUTED = "#A7B3C8"
INDIGO = "#6366F1"
CYAN = "#06B6D4"
LILAC = "#A78BFA"


def text(x, y, value, size=18, fill=INK, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" {extra}>{escape(value)}</text>')


def line(x1, y1, x2, y2, color="#273449", width=1, extra=""):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{color}" stroke-width="{width}" {extra}/>')


def points(coords):
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)


def polygon(coords, fill, stroke="#34415F", extra=""):
    return f'<polygon points="{points(coords)}" fill="{fill}" stroke="{stroke}" stroke-width="1" {extra}/>'


def document(width, height, title, desc, body, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(desc)}</desc>
  <defs>{defs}</defs>
  <g font-family="Segoe UI, Arial, sans-serif">{body}</g>
</svg>
'''


def save(name, source):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8", newline="\n")


DEFS = '''
<linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#101629"/><stop offset="0.55" stop-color="#080B14"/><stop offset="1" stop-color="#10182A"/>
</linearGradient>
<radialGradient id="violetHalo"><stop stop-color="#6366F1" stop-opacity="0.21"/><stop offset="1" stop-color="#6366F1" stop-opacity="0"/></radialGradient>
<radialGradient id="cyanHalo"><stop stop-color="#06B6D4" stop-opacity="0.13"/><stop offset="1" stop-color="#06B6D4" stop-opacity="0"/></radialGradient>
<linearGradient id="edge"><stop stop-color="#6366F1"/><stop offset="0.5" stop-color="#A78BFA"/><stop offset="1" stop-color="#06B6D4"/></linearGradient>
<linearGradient id="top" x2="1" y2="1"><stop stop-color="#4A5489"/><stop offset="1" stop-color="#202A49"/></linearGradient>
<linearGradient id="left" x2="1" y2="0.8"><stop stop-color="#232E50"/><stop offset="1" stop-color="#10182C"/></linearGradient>
<linearGradient id="right" x2="0.2" y2="1"><stop stop-color="#1C2541"/><stop offset="1" stop-color="#0C1222"/></linearGradient>
<linearGradient id="glass" x2="1" y2="1"><stop stop-color="#8490D9" stop-opacity="0.13"/><stop offset="1" stop-color="#111827" stop-opacity="0.48"/></linearGradient>
<linearGradient id="cylinder"><stop stop-color="#203A56"/><stop offset="0.35" stop-color="#395279"/><stop offset="0.7" stop-color="#192D49"/><stop offset="1" stop-color="#102337"/></linearGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="soft" x="-50%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="12"/></filter>
'''


def mark(x, y, scale=1):
    return f'''<g transform="translate({x} {y}) scale({scale})" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M0 8 14 0 28 8 28 24 14 32 0 24Z" stroke="#A78BFA" stroke-width="1.5"/>
      <path d="m7 12 7-4 7 4v8l-7 4-7-4Z" stroke="#06B6D4" stroke-width="1.5"/>
      <path d="M14 16V8m0 8 7 4m-7-4-7 4" stroke="#8A90D8"/>
    </g>'''


def scene(ox=900, oy=390):
    """Isometric geometry: a drawn vector scene, not a 3D rendering."""
    def project(x, y, z=0):
        return ox + 0.8660254 * (x - y), oy + 0.5 * (x + y) - z

    def cube(x, y, z, w, d, h, accent=None):
        a, b, c, e = [project(*p) for p in [(x, y, z+h), (x+w, y, z+h),
                                           (x+w, y+d, z+h), (x, y+d, z+h)]]
        a0, b0, c0, e0 = [project(*p) for p in [(x, y, z), (x+w, y, z),
                                               (x+w, y+d, z), (x, y+d, z)]]
        parts = [polygon([e, c, c0, e0], "url(#left)"),
                 polygon([b, c, c0, b0], "url(#right)"),
                 polygon([a, b, c, e], "url(#top)")]
        if accent:
            parts.append(line(*e, *c, accent, 1.6))
            parts.append(line(*b, *c, accent, 1.1, 'opacity="0.65"'))
        return "".join(parts)

    def route(coords, color=CYAN):
        coords = [project(*p) for p in coords]
        p = points(coords)
        return (f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="7" opacity="0.13" filter="url(#glow)"/>'
                f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="1.3" opacity="0.75"/>'
                f'<polyline class="data-flow" points="{p}" fill="none" stroke="#C5F7FF" stroke-width="2" stroke-dasharray="3 38" opacity="0.85"/>')

    out = [f'<ellipse cx="{ox}" cy="{oy+108}" rx="205" ry="47" fill="#00030C" opacity="0.8" filter="url(#soft)"/>']
    # Subtle construction grid.
    for i in range(-200, 201, 40):
        out.append(line(*project(i, -170, -12), *project(i, 170, -12), "#283556", 0.8, 'opacity="0.35"'))
        out.append(line(*project(-200, i, -12), *project(200, i, -12), "#283556", 0.8, 'opacity="0.35"'))
    out.append(cube(-140, -110, 0, 280, 230, 12, INDIGO))
    out.append(polygon([project(-133,-103,13),project(133,-103,13),project(133,113,13),project(-133,113,13)], "#10192D", "#39456A"))
    for x in range(-100, 121, 40):
        out.append(line(*project(x,-100,14), *project(x,110,14), "#25314C", 0.8))
    for y in range(-70, 111, 40):
        out.append(line(*project(-130,y,14), *project(130,y,14), "#25314C", 0.8))

    out.append(route([(-43,0,16),(-43,55,16),(57,55,16),(57,38,16)]))
    out.append(route([(-43,0,16),(-43,-63,16),(70,-63,16)], LILAC))
    out.append(route([(-43,55,16),(-95,55,16),(-95,88,16)], INDIGO))

    # Raised server chassis and three individually drawn rack units.
    out.append(cube(-88,-28,16,83,73,10, LILAC))
    for z in [35, 82, 129]:
        out.append(cube(-82,-22,z,70,60,40, LILAC))
        for dz in [12,19,26]:
            out.append(line(*project(-73,39,z+dz), *project(-34,39,z+dz), "#5B6C9D", 1.3))
        out.append(line(*project(-74,39,z+33), *project(-59,39,z+33), CYAN, 2))
        dot = project(-22,39,z+18)
        out.append(f'<circle cx="{dot[0]}" cy="{dot[1]}" r="2.2" fill="#6DE0E7"/>')
    out.append(cube(-82,-22,175,70,60,6, INDIGO))
    for i in range(4):
        out.append(line(*project(-67+i*9,-12,182), *project(-67+i*9,23,182), "#6974AB", 1))

    # Secondary compute node.
    out.append(cube(22,8,16,67,63,9, CYAN))
    out.append(cube(28,14,31,55,51,72, CYAN))
    for z in [45,55,65,75,85]:
        out.append(line(*project(36,66,z), *project(72,66,z), "#476387", 1.5))
    out.append(line(*project(38,66,92), *project(49,66,92), CYAN, 2))
    out.append(polygon([project(38,25,104),project(69,25,104),project(69,54,104),project(38,54,104)],"#263F5F", "#6481AA"))

    # Floating database drawn with elliptical caps and directional material shading.
    dx, dy = project(68,-82,106)
    out.append(f'<g class="floating"><ellipse cx="{dx}" cy="{dy+94}" rx="40" ry="14" fill="#06B6D4" opacity="0.12" filter="url(#soft)"/>')
    for cy in [dy+30,dy+10,dy-10]:
        out.append(f'<path d="M{dx-39} {cy}v18a39 15 0 0 0 78 0v-18" fill="url(#cylinder)" stroke="#49708D"/>')
        out.append(f'<ellipse cx="{dx}" cy="{cy}" rx="39" ry="15" fill="#28445E" stroke="#688EAD"/>')
        out.append(f'<path d="M{dx-34} {cy+21}a39 15 0 0 0 68 0" fill="none" stroke="#06B6D4" opacity="0.65"/>')
    out.append(f'<ellipse cx="{dx}" cy="{dy-10}" rx="28" ry="9" fill="#34566F" stroke="#769BB5" stroke-opacity="0.6"/></g>')
    out.append(route([(68,-82,16),(68,-82,67)], CYAN))

    # Floating glass-like microservice tile.
    out.append('<g class="floating-slow">')
    glass = [project(-115,-90,105),project(-65,-90,105),project(-65,-46,105),project(-115,-46,105)]
    out.append(polygon(glass, "url(#glass)", "#6C73B2"))
    center = project(-90,-68,106)
    out.append(f'<path d="m{center[0]-10} {center[1]-4} -6 4 6 4m20-8 6 4-6 4m-5-12-6 16" fill="none" stroke="#C3BCF9" stroke-width="1.6"/>')
    out.append('</g>')

    # Foreground service node.
    out.append(cube(-115,72,16,40,34,10, INDIGO))
    out.append(cube(-109,77,34,28,24,30, INDIGO))
    out.append(line(*project(-104,102,47), *project(-89,102,47), LILAC, 2))
    for px,py,pz in [(127,-45,25),(-136,30,22),(45,110,23)]:
        x,y=project(px,py,pz)
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#111827" stroke="#7C87B4"/><circle cx="{x}" cy="{y}" r="1.3" fill="#A78BFA"/>')
    return "".join(out)


def hero(mobile=False, animated=False):
    w,h=(640,860) if mobile else (1200,600)
    out=[f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="22" fill="url(#background)" stroke="#29314B"/>',
         f'<ellipse cx="{w*0.8}" cy="{h*0.48}" rx="{w*0.42}" ry="{h*0.65}" fill="url(#violetHalo)"/>',
         f'<ellipse cx="{w*0.88}" cy="{h*0.8}" rx="{w*0.35}" ry="{h*0.5}" fill="url(#cyanHalo)"/>',
         line(28,1,w-28,1,"url(#edge)",2), mark(40 if mobile else 58,36,0.85)]
    out.append(text(78 if mobile else 98,56,"DVL  /  ENGINEERING NOTES",12,MUTED,500,'letter-spacing="2"'))
    if not mobile:
        out.append(text(1140,55,"SYSTEMS & SOFTWARE",11,MUTED,400,'text-anchor="end" letter-spacing="2"'))
    x=40 if mobile else 64
    out.append(text(x,133 if mobile else 135,"JAVA BACKEND DEVELOPER",12,LILAC,600,'letter-spacing="3"'))
    out.append(text(x,213 if mobile else 218,"DOAN",78 if mobile else 80,INK,700,'letter-spacing="-3"'))
    out.append(text(x,296 if mobile else 302,"VINH LONG",78 if mobile else 80,INK,700,'letter-spacing="-3"'))
    out.append(text(x+2,342 if mobile else 349,"BACKEND SOFTWARE ENGINEER",17,MUTED,500,'letter-spacing="2.7"'))
    out.append(line(x,374 if mobile else 385,x+56,374 if mobile else 385,"url(#edge)",2))
    if mobile:
        for y,s in [(412,"Building reliable backend systems,"),(442,"exploring distributed architectures"),(472,"& intelligent software.")]:
            out.append(text(x,y,s,22,MUTED))
        out.append(f'<g transform="translate(-410 378) scale(0.8)">{scene()}</g>')
        out.append(line(40,804,600,804,"#2B3551"))
        out.append(text(40,833,"JAVA / SYSTEMS / INTELLIGENCE",11,MUTED,500,'letter-spacing="1.8"'))
    else:
        for y,s in [(426,"Building reliable backend systems,"),(457,"exploring distributed architectures"),(488,"& intelligent software.")]:
            out.append(text(x,y,s,21,MUTED))
        out.append(scene(907,375))
        out.append(line(64,538,1136,538,"#29334C"))
        out.append(text(64,570,"JAVA / SYSTEMS / INTELLIGENCE",11,MUTED,500,'letter-spacing="2"'))
        out.append(text(1136,570,"DOANVINHLONG18",11,MUTED,400,'text-anchor="end" letter-spacing="2"'))
    defs=DEFS+f'<clipPath id="panelClip"><rect width="{w}" height="{h}" rx="22"/></clipPath>'
    if animated:
        defs+='''<style>
@keyframes flow { to { stroke-dashoffset: -82; } }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
@keyframes tint { 0%,100% { stop-color: #A78BFA; } 50% { stop-color: #7D9FEA; } }
.data-flow { animation: flow 9s linear infinite; }
.floating { animation: float 8s ease-in-out infinite; }
.floating-slow { animation: float 11s ease-in-out infinite; }
.edge-mid { animation: tint 12s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) { .data-flow,.floating,.floating-slow,.edge-mid { animation: none; } }
</style>'''
        defs=defs.replace('<stop offset="0.5" stop-color="#A78BFA"/>', '<stop class="edge-mid" offset="0.5" stop-color="#A78BFA"/>')
    return document(w,h,"Doan Vinh Long — Backend Software Engineer",
                    "Building reliable backend systems, exploring distributed architectures & intelligent software. Original isometric vector infrastructure illustration.",'<g clip-path="url(#panelClip)">'+"".join(out)+'</g>',defs)


ICONS = {
    "backend": '<rect x="13" y="12" width="22" height="10" rx="2"/><rect x="13" y="26" width="22" height="10" rx="2"/><path d="M18 17h8m-8 14h8"/><circle cx="31" cy="17" r="0.8"/><circle cx="31" cy="31" r="0.8"/>',
    "distributed": '<path d="M24 17v8m-10 7 10-7 10 7"/><rect x="18" y="8" width="12" height="9" rx="2"/><rect x="8" y="32" width="12" height="9" rx="2"/><rect x="28" y="32" width="12" height="9" rx="2"/>',
    "data": '<ellipse cx="24" cy="14" rx="12" ry="5"/><path d="M12 14v19a12 5 0 0 0 24 0V14M12 23a12 5 0 0 0 24 0"/>',
    "intelligence": '<path d="m24 8 14 8v16l-14 8-14-8V16Zm0 0v32M10 16l28 16m0-16L10 32"/><circle cx="24" cy="24" r="4" fill="#111827"/>',
}


def icons():
    for name,paths in ICONS.items():
        body=(f'<rect x="0.5" y="0.5" width="47" height="47" rx="12" fill="#111827" stroke="#384367"/>'
              f'<g fill="none" stroke="{CYAN if name in ["data","distributed"] else LILAC}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{paths}</g>')
        save(f"icons/{name}.svg",document(48,48,name.title()+" category","Original engineering category pictogram.",body))


def principles(mobile=False):
    w,h=(640,550) if mobile else (1200,254)
    out=[f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="#080B14" stroke="#29314B"/>',
         text(32,42,"AN ENGINEERING COMPASS",11,LILAC,600,'letter-spacing="2.5"')]
    if mobile:
        labels=[("01","Correctness","before optimization."),("02","Measurement","before scaling."),("03","Resilience","by design."),("04","Observability","with purpose."),("05","Simplicity","as a default.")]
        for i,(num,title,sub) in enumerate(labels):
            y=97+i*89
            out.append(text(34,y,num,14,CYAN,500,'font-family="Consolas, monospace"'))
            out.append(text(85,y,title,25,INK,600))
            out.append(text(85,y+27,sub,20,MUTED))
            if i<4: out.append(line(85,y+44,600,y+44,"#202A40"))
    else:
        labels=[("Correctness","before optimization"),("Measurement","before scaling"),("Resilience","by design"),("Observability","with purpose"),("Simplicity","as a default")]
        for i,(title,sub) in enumerate(labels):
            x=32+i*235
            out.append(text(x,94,f"0{i+1}",13,CYAN,500,'font-family="Consolas, monospace"'))
            out.append(line(x,116,x+192,116,"#323B56"))
            out.append(text(x,160,title,22,INK,600))
            out.append(text(x,192,sub,16,MUTED))
    return document(w,h,"An engineering compass","Correctness, measurement, resilience, observability, and simplicity are engineering principles, not claims of project outcomes.","".join(out))


def main():
    save("hero.svg",hero())
    save("hero-mobile.svg",hero(mobile=True))
    save("hero-animated.svg",hero(animated=True))
    icons()
    save("principles.svg",principles())
    save("principles-mobile.svg",principles(mobile=True))
    save("section-divider.svg",document(1200,30,"Section divider","Decorative indigo to cyan hairline.",'<path d="M0 15h1200" stroke="url(#divider)"/>','<linearGradient id="divider"><stop stop-color="#6366F1" stop-opacity="0"/><stop offset="0.3" stop-color="#6366F1" stop-opacity="0.5"/><stop offset="0.7" stop-color="#06B6D4" stop-opacity="0.35"/><stop offset="1" stop-color="#06B6D4" stop-opacity="0"/></linearGradient>'))
    body=('<rect width="1200" height="106" rx="14" fill="#080B14"/>'+mark(32,36,1)+
          text(80,57,"DVL",18,INK,600,'letter-spacing="3"')+line(147,34,147,71,"#36405A")+
          text(174,57,"Thoughtful systems. Intentional engineering.",20,MUTED)+
          text(1168,57,"</>",18,LILAC,400,'text-anchor="end" font-family="Consolas, monospace"'))
    save("signature.svg",document(1200,106,"DVL signature","Thoughtful systems. Intentional engineering.",body))
    mobile_body=('<rect width="640" height="130" rx="16" fill="#080B14"/>'+mark(28,29,1)+
                 text(75,50,"DVL",20,INK,600,'letter-spacing="3"')+
                 text(28,98,"Thoughtful systems. Intentional engineering.",23,MUTED))
    save("signature-mobile.svg",document(640,130,"DVL signature","Thoughtful systems. Intentional engineering.",mobile_body))
    print("Built 12 self-contained SVG assets.")


if __name__ == "__main__":
    main()
