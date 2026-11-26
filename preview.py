"""dist -> dist_preview: dizin linklerini index.html'e çevirir (artifact önizlemesi için)."""
import re, shutil
from pathlib import Path
S=Path('dist'); D=Path('dist_preview')
if D.exists(): shutil.rmtree(D)
shutil.copytree(S, D)
def fix(m):
    h=m.group(2)
    if h.startswith(('http','#','mailto:','/')) : return m.group(0)
    path,_,frag=h.partition('#')
    if path=='' : return m.group(0)
    if path.endswith('/') or path in ('.','..'):
        path=path.rstrip('/')+'/index.html' if path not in ('./',) else 'index.html'
    return f'{m.group(1)}="{path}{"#"+frag if frag else ""}"'
for f in D.rglob('*.html'):
    s=f.read_text()
    s=re.sub(r'(href)="([^"]*)"', fix, s)
    s=s.replace('<body data-root=', '<body data-preview="1" data-root=')
    f.write_text(s)
(D/'404.html').unlink(); (D/'CNAME').unlink(); (D/'.nojekyll').unlink()
print(len(list(D.rglob('*'))))
