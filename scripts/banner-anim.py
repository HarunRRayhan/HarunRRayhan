import re, sys
T=13.0; TYPE=0.9; SCROLL0, SCROLL1 = 10.6, 11.4
k=lambda t: f"{t/T:.4f}"
for theme in ('light','dark'):
    p=f'assets/banner-{theme}.svg'; s=open(p).read()
    s=s.replace('g{animation:none!important;opacity:1!important}','')
    start=s.index('</text>', s.index('~/ship.log'))+len('</text>\n')
    end=s.index('  <text x="790" y="272"')
    block=s[start:end]
    rows=['  <g>\n    <'+x for x in block.split('  <g>\n    <')[1:]]
    assert len(rows)==5 and ''.join(rows)==block, len(rows)
    defs, out = [], []
    for i,r in enumerate(rows):
        y=int(re.search(r'<text x="808" y="(\d+)"',r).group(1))
        st=0.6+1.8*i
        defs.append(f'''    <clipPath id="row{i}"><rect x="772" y="{y-20}" width="440" height="30">
      <animate attributeName="width" dur="{T}s" repeatCount="indefinite" values="0;0;440;440;0;0" keyTimes="0;{k(st)};{k(st+TYPE)};{k(SCROLL1)};{k(SCROLL1+0.01)};1"/>
    </rect></clipPath>''')
        out.append(r.replace('  <g>\n', f'  <g clip-path="url(#row{i})">\n',1))
    log=('  <defs>\n'+'\n'.join(defs)+'\n    <clipPath id="term"><rect x="760" y="82" width="460" height="168"/></clipPath>\n  </defs>\n'
         '  <g clip-path="url(#term)"><g>\n'
         f'    <animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" values="0 0;0 0;0 -36;0 -36" keyTimes="0;{k(SCROLL0)};{k(SCROLL1)};1"/>\n'
         f'    <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;{k(SCROLL0)};{k(SCROLL1)};1"/>\n'
         + ''.join(out) + '  </g></g>\n')
    s=s[:start]+log+s[end:]
    open(p,'w').write(s)
