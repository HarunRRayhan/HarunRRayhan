import sys
out = sys.argv[1]
themes = {
 "light": dict(bg="#f6f1e7", ink="#1c1917", mute="#6b625a", rule="#ddd2bf", accent="#b8541f", panel="#fffaf2", ok="#3f7d4e"),
 "dark":  dict(bg="#13110f", ink="#f4ede2", mute="#a39887", rule="#332d28", accent="#e0793f", panel="#1b1815", ok="#7cc28e"),
}
W, H = 1280, 560
CX0, CX1, CY0, CY1 = 450, 830, 190, 370
NW, NH = 320, 100
rows = [110, 280, 450]
left = [("01", "Cloud Engineering", "multi-cloud · serverless"),
        ("02", "AWS", "ECS · Lambda · RDS · IAM"),
        ("03", "DevOps", "Terraform · CI/CD · Kubernetes")]
right = [("04", "AI / ML", "agents · MCP · MLOps · LLMs"),
         ("05", "Backend", "Rails · Rust · APIs"),
         ("06", "Databases", "Postgres · Redis · modeling")]
exits = [250, 280, 310]

def route(sx, sy, bx, ex, ey, r=12):
    # horizontal from (sx,sy) to bend x, vertical to ey, horizontal to ex; rounded corners
    if sy == ey:
        return f"M{sx} {sy} H{ex}"
    d1 = -1 if bx < sx else 1
    dv = -1 if ey < sy else 1
    d2 = -1 if ex < bx else 1
    return (f"M{sx} {sy} H{bx - d1*r} Q{bx} {sy} {bx} {sy + dv*r} "
            f"V{ey - dv*r} Q{bx} {ey} {bx + d2*r} {ey} H{ex}")

def node(x, y, num, title, sub, c):
    return f'''
  <g>
    <rect x="{x}" y="{y-NH/2}" width="{NW}" height="{NH}" rx="10" fill="{c['panel']}" stroke="{c['rule']}"/>
    <text x="{x+20}" y="{y-20}" class="m" font-size="13" letter-spacing="1.5" fill="{c['accent']}">{num}</text>
    <text x="{x+20}" y="{y+10}" class="s" font-size="26" fill="{c['ink']}">{title}</text>
    <text x="{x+20}" y="{y+34}" class="m" font-size="15" fill="{c['mute']}">{sub}</text>
  </g>'''

for name, c in themes.items():
    paths, nodes = [], []
    for i, (yc, n) in enumerate(zip(rows, left)):
        paths.append(route(CX0, exits[i], 415, 60+NW, yc))
        nodes.append(node(60, yc, *n, c))
    for i, (yc, n) in enumerate(zip(rows, right)):
        paths.append(route(CX1, exits[i], 865, W-60-NW, yc))
        nodes.append(node(W-60-NW, yc, *n, c))
    wires = ""
    for i, d in enumerate(paths):
        wires += f'''
  <path d="{d}" fill="none" stroke="{c['rule']}" stroke-width="2"/>
  <path class="flow" d="{d}" fill="none" stroke="{c['accent']}" stroke-width="2" stroke-dasharray="4 14" opacity=".55"/>
  <circle class="pkt" r="4.5" fill="{c['accent']}"><animateMotion dur="2.8s" begin="-{i*0.45:.2f}s" repeatCount="indefinite" path="{d}"/></circle>'''
    ports = "".join(f'<circle cx="{60+NW}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/><circle cx="{W-60-NW}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>' for y in rows)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Solution architecture at the center, connected to cloud engineering, AWS, DevOps, AI/ML, backend and databases">
  <style>
    .s{{font-family:Georgia,'Iowan Old Style','Times New Roman',serif}}
    .m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
    .flow{{animation:flow 1.2s linear infinite}}
    .halo{{animation:halo 3s ease-in-out infinite;transform-origin:640px 280px}}
    @keyframes flow{{to{{stroke-dashoffset:-18}}}}
    @keyframes halo{{0%,100%{{opacity:.15;transform:scale(1)}}50%{{opacity:.45;transform:scale(1.035)}}}}
    @media (prefers-reduced-motion:reduce){{.flow,.halo{{animation:none}}.pkt{{display:none}}}}
  </style>
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{c['rule']}"/></pattern></defs>
  <rect width="{W}" height="{H}" fill="url(#g)" opacity=".7"/>{wires}
  {ports}{''.join(nodes)}
  <rect class="halo" x="{CX0-10}" y="{CY0-10}" width="{CX1-CX0+20}" height="{CY1-CY0+20}" rx="18" fill="none" stroke="{c['accent']}" stroke-width="1.5"/>
  <rect x="{CX0}" y="{CY0}" width="{CX1-CX0}" height="{CY1-CY0}" rx="14" fill="{c['ink']}"/>
  <text x="640" y="{CY0+42}" text-anchor="middle" class="m" font-size="15" letter-spacing="3" fill="{c['accent']}">SOFTWARE ARCHITECT</text>
  <text x="640" y="{CY0+90}" text-anchor="middle" class="s" font-size="36" fill="{c['bg']}">Solution Architecture</text>
  <text x="640" y="{CY0+126}" text-anchor="middle" class="m" font-size="15" fill="{c['rule'] if name=='light' else '#6b625a'}">system design · technical strategy</text>
  <text x="640" y="{CY0+150}" text-anchor="middle" class="m" font-size="15" fill="{c['rule'] if name=='light' else '#6b625a'}">business needs → software</text>
</svg>
'''
    open(f"{out}/architect-{name}.svg", "w").write(svg)
