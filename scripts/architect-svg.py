"""Builds assets/architect-{light,dark}.svg. Logos come from skillicons.dev (icons/ dir)."""
import re, sys, os
out, icons = sys.argv[1], sys.argv[2]

def icon(name, x, y, size):
    src = open(os.path.join(icons, f"{name}.svg")).read()
    inner = re.search(r'<g transform="translate\(0, 0\)">\s*(<svg.*</svg>)\s*</g>', src, re.S).group(1)
    inner = re.sub(r'id="([^"]+)"', rf'id="{name}-\1"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', rf'url(#{name}-\1)', inner)
    inner = re.sub(r'href="#([^"]+)"', rf'href="#{name}-\1"', inner)
    return re.sub(r'<svg[^>]*>', f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256" fill="none">', inner, count=1)

def blueprint(x, y, size, c):
    # hand-drawn "solution architecture" tile: three layered boxes
    s = size / 28
    return (f'<g transform="translate({x} {y}) scale({s})"><rect width="28" height="28" rx="6.5" fill="{c["ink"]}"/>'
            f'<rect x="6" y="6" width="16" height="4" rx="1" fill="{c["accent"]}"/>'
            f'<rect x="6" y="12" width="7" height="10" rx="1" fill="none" stroke="{c["bg"]}" stroke-width="1.5"/>'
            f'<rect x="15" y="12" width="7" height="10" rx="1" fill="none" stroke="{c["bg"]}" stroke-width="1.5"/></g>')

themes = {
 "light": dict(bg="#f6f1e7", ink="#1c1917", mute="#6b625a", rule="#ddd2bf", accent="#b8541f", panel="#fffaf2", csub="#ddd2bf"),
 "dark":  dict(bg="#13110f", ink="#f4ede2", mute="#a39887", rule="#332d28", accent="#e0793f", panel="#1b1815", csub="#6b625a"),
}
W, H = 1280, 640
CX0, CX1, CY0, CY1 = 455, 825, 230, 410
NW, NH, L, R = 340, 124, 40, 1280 - 40 - 340
rows = [90, 240, 400, 550]
exits = [275, 305, 335, 365]
bends_l = [430, 405, 405, 430]
left = [("Solution Architecture", "system design · trade-offs", ["@bp"]),
        ("Cloud Engineering", "multi-cloud · serverless", ["gcp", "azure", "cloudflare"]),
        ("AWS", "ECS · Lambda · RDS · IAM", ["aws"]),
        ("DevOps &amp; Terraform", "IaC · CI/CD · Kubernetes", ["terraform", "docker", "kubernetes", "githubactions"])]
right = [("AI / ML", "agents · MCP · MLOps · LLMs", ["py", "pytorch", "tensorflow"]),
         ("Backend", "Rails · Rust · Laravel", ["rails", "rust", "laravel"]),
         ("Databases", "Postgres · Redis · modeling", ["postgres", "redis", "mysql"]),
         ("Observability", "metrics · alerts · cron jobs", ["prometheus", "grafana"])]

def route(sx, sy, bx, ex, ey, r=12):
    if sy == ey:
        return f"M{sx} {sy} H{ex}"
    d1 = -1 if bx < sx else 1
    dv = -1 if ey < sy else 1
    d2 = -1 if ex < bx else 1
    return (f"M{sx} {sy} H{bx - d1*r} Q{bx} {sy} {bx} {sy + dv*r} "
            f"V{ey - dv*r} Q{bx} {ey} {bx + d2*r} {ey} H{ex}")

def node(x, y, title, sub, logos, c):
    tiles = "".join(blueprint(x + 20 + i*36, y - 46, 30, c) if n == "@bp" else icon(n, x + 20 + i*36, y - 46, 30)
                    for i, n in enumerate(logos))
    return f'''
  <g>
    <rect x="{x}" y="{y-NH/2}" width="{NW}" height="{NH}" rx="12" fill="{c['panel']}" stroke="{c['rule']}"/>
    {tiles}
    <text x="{x+20}" y="{y+16}" class="s" font-size="26" fill="{c['ink']}">{title}</text>
    <text x="{x+20}" y="{y+42}" class="m" font-size="15" fill="{c['mute']}">{sub}</text>
  </g>'''

for name, c in themes.items():
    paths, nodes = [], []
    for i, (yc, n) in enumerate(zip(rows, left)):
        paths.append(route(CX0, exits[i], bends_l[i], L + NW, yc))
        nodes.append(node(L, yc, *n, c))
    for i, (yc, n) in enumerate(zip(rows, right)):
        paths.append(route(CX1, exits[i], W - bends_l[i], R, yc))
        nodes.append(node(R, yc, *n, c))
    wires = ""
    for i, d in enumerate(paths):
        wires += f'''
  <path d="{d}" fill="none" stroke="{c['rule']}" stroke-width="2"/>
  <path class="flow" d="{d}" fill="none" stroke="{c['accent']}" stroke-width="2" stroke-dasharray="4 14" opacity=".55"/>
  <circle class="pkt" r="4.5" fill="{c['accent']}"><animateMotion dur="2.8s" begin="-{i*0.35:.2f}s" repeatCount="indefinite" path="{d}"/></circle>'''
    ports = "".join(f'<circle cx="{L+NW}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/><circle cx="{R}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>' for y in rows)
    cx, cy = (CX0 + CX1) // 2, (CY0 + CY1) // 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Software architect at the center, connected to solution architecture, cloud engineering, AWS, DevOps and Terraform, AI/ML, backend, databases and observability">
  <style>
    .s{{font-family:Georgia,'Iowan Old Style','Times New Roman',serif}}
    .m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
    .flow{{animation:flow 1.2s linear infinite}}
    .halo{{animation:halo 3s ease-in-out infinite;transform-origin:{cx}px {cy}px}}
    @keyframes flow{{to{{stroke-dashoffset:-18}}}}
    @keyframes halo{{0%,100%{{opacity:.15;transform:scale(1)}}50%{{opacity:.45;transform:scale(1.035)}}}}
    @media (prefers-reduced-motion:reduce){{.flow,.halo{{animation:none}}.pkt{{display:none}}}}
  </style>
  <defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{c['rule']}"/></pattern></defs>
  <rect width="{W}" height="{H}" fill="url(#g)" opacity=".7"/>{wires}
  {ports}{''.join(nodes)}
  <rect class="halo" x="{CX0-10}" y="{CY0-10}" width="{CX1-CX0+20}" height="{CY1-CY0+20}" rx="20" fill="none" stroke="{c['accent']}" stroke-width="1.5"/>
  <rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="16" fill="{c['ink']}"/>
  <text x="{cx}" y="{CY0+46}" text-anchor="middle" class="m" font-size="14" letter-spacing="3" fill="{c['accent']}">HARUN R. RAYHAN</text>
  <text x="{cx}" y="{CY0+100}" text-anchor="middle" class="s" font-size="42" fill="{c['bg']}">Software Architect</text>
  <text x="{cx}" y="{CY0+136}" text-anchor="middle" class="m" font-size="15" fill="{c['csub']}">design · build · ship · scale</text>
</svg>
'''
    open(f"{out}/architect-{name}.svg", "w").write(svg)
