"""Builds assets/companies-{light,dark}.svg: a looping logo marquee (logos from harun.dev)."""
import base64, sys, os
src, out = sys.argv[1], sys.argv[2]
logos = [("SocialHP","socialhp-72.png"),("L'Oréal","loreal.svg"),("Kiehl's","kiehls.svg"),("Samsung","samsung-280.png"),
         ("Prudential","prudential-280.png"),("Lonza","lonza.svg"),("Fleetcor","fleetcor-280.png"),("NCR","ncr.svg")]
def uri(f):
    mime = "image/svg+xml" if f.endswith(".svg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(src, f), "rb").read()).decode()
W, H, CW, CH, GAP, DUR = 1280, 112, 180, 60, 16, 36
step = CW + GAP; setw = step * len(logos)
themes = {"light": dict(bg="#f6f1e7", card="#ffffff", rule="#e3d9c8"),
          "dark": dict(bg="#13110f", card="#ffffff", rule="#332d28")}
symbols = "".join(f'  <image id="logo{i}" x="20" y="{(H-CH)//2+12}" width="{CW-40}" height="{CH-24}" href="{uri(f)}" preserveAspectRatio="xMidYMid meet" filter="url(#mono)" opacity=".7"/>\n' for i, (_, f) in enumerate(logos))
for name, c in themes.items():
    cards = ""
    for rep in range(3):  # 3 copies so the strip never shows a gap at 1280px
        for i, (label, f) in enumerate(logos):
            x = rep*setw + i*step
            cards += (f'<g><title>{label}</title><rect x="{x}" y="{(H-CH)//2}" width="{CW}" height="{CH}" rx="10" fill="{c["card"]}" stroke="{c["rule"]}"/>'
                      f'<use href="#logo{i}" x="{x}"/></g>\n')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Companies: {', '.join(l for l,_ in logos)}">
<defs>
{symbols}  <filter id="mono"><feColorMatrix type="saturate" values="0"/></filter>
  <linearGradient id="edge"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/><stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
</defs>
<g mask="url(#fade)"><g>
<animateTransform attributeName="transform" type="translate" from="0 0" to="-{setw} 0" dur="{DUR}s" repeatCount="indefinite"/>
{cards}</g></g>
</svg>
'''
    open(os.path.join(out, f"companies-{name}.svg"), "w").write(svg)
