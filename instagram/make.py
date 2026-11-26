#!/usr/bin/env python3
"""We Are Sales Force – Instagram görsel üreticisi.
Kullanım: python3 instagram/make.py instagram/posts/2026-W49.yaml  → instagram/out/<hafta>/*.png
Her gönderi: type: card | carousel ; slides: [...]. 1080x1350 (4:5) PNG.
"""
import sys, yaml, asyncio, html
from pathlib import Path
from playwright.async_api import async_playwright

CSS = '''
*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;font-family:Inter,"Helvetica Neue",Arial,sans-serif;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:96px 88px;display:flex;flex-direction:column}
.dark{background:#041E41;color:#fff}.light{background:#FBFAF7;color:#041E41}.acc{background:#E5484D;color:#fff}.teal{background:#2F7DC0;color:#fff}
.brand{position:absolute;left:88px;bottom:58px;display:flex;align-items:center;gap:14px;font-size:24px;font-weight:600}
.brand svg{height:72px;width:auto}.brand span{font-size:24px;font-weight:600;opacity:.8;letter-spacing:.02em}
.pg{position:absolute;right:88px;bottom:68px;font-size:24px;font-weight:700;opacity:.7}
.tag{display:inline-block;align-self:flex-start;font-size:26px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:10px 22px;border-radius:40px;margin-bottom:44px}
.dark .tag{background:#0E2B55;color:#F3BF5C}.light .tag{background:#FDE8E8;color:#E5484D}.acc .tag,.teal .tag{background:rgba(255,255,255,.18);color:#fff}
h1{font-size:92px;line-height:1.02;letter-spacing:-.025em;font-weight:800}
h2{font-size:80px;line-height:1.06;letter-spacing:-.02em;font-weight:800}
h1 em,h2 em{font-style:normal;color:#F3BF5C}.light h1 em,.light h2 em{color:#E5484D}
p.lead{font-size:42px;line-height:1.38;margin-top:36px;opacity:.88}
.big{font-size:240px;font-weight:800;line-height:.9;letter-spacing:-.04em;color:#F3BF5C}
.light .big{color:#E5484D}
ul.l{list-style:none;padding:0;margin-top:44px;display:flex;flex-direction:column;gap:26px}
ul.l li{font-size:38px;line-height:1.3;padding-left:62px;position:relative}
ul.l li:before{content:"";position:absolute;left:0;top:10px;width:34px;height:34px;border-radius:9px;background:#E5484D}
.dark ul.l li:before{background:#F3BF5C}
ol.n{list-style:none;padding:0;margin-top:40px;display:flex;flex-direction:column;gap:20px;counter-reset:n}
ol.n li{counter-increment:n;font-size:36px;line-height:1.28;background:rgba(255,255,255,.07);border-radius:22px;padding:24px 28px 24px 110px;position:relative}
.light ol.n li{background:#fff;border:2px solid #E4E0D8}
ol.n li:before{content:counter(n);position:absolute;left:26px;top:20px;width:60px;height:60px;border-radius:16px;background:#E5484D;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:32px}
ol.n b{display:block}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:50px}
.cmp div{border-radius:28px;padding:38px}.cmp .a{background:#0E2B55}.cmp .b{background:#E5484D}
.cmp small{display:block;font-size:26px;opacity:.8;font-weight:600}.cmp strong{display:block;font-size:96px;font-weight:800;margin:12px 0}
.cmp span{font-size:28px;line-height:1.3;display:block}
.quote{font-size:64px;line-height:1.15;font-weight:800;letter-spacing:-.015em}
.foot{margin-top:auto;margin-bottom:70px;font-size:32px;line-height:1.35;opacity:.85}
.cta{margin-top:auto;margin-bottom:80px;font-size:34px;font-weight:700;background:#fff;color:#041E41;border-radius:22px;padding:28px 34px;align-self:flex-start}
.ghost{position:absolute;right:70px;bottom:250px;font-size:520px;font-weight:800;line-height:.8;letter-spacing:-.05em;color:rgba(4,30,65,.07)}.dark .ghost,.acc .ghost{color:rgba(255,255,255,.07)}
.swipe{position:absolute;right:88px;top:100px;font-size:26px;font-weight:700;opacity:.75}
'''
LOGO = '<svg viewBox="0 0 40 40"><rect width="40" height="40" rx="10" fill="#E5484D"/><rect x="9" y="22" width="5" height="9" rx="1.2" fill="#fff"/><rect x="17.5" y="16" width="5" height="15" rx="1.2" fill="#fff"/><rect x="26" y="9" width="5" height="22" rx="1.2" fill="#041E41"/></svg>'
LOGO_D = LOGO.replace('fill="#041E41"', 'fill="#F3BF5C"')

MARK_T = (Path(__file__).parent.parent / 'brand' / 'wasf-mark-transparent.svg').read_text()
MARK_C = (Path(__file__).parent.parent / 'brand' / 'wasf-mark.svg').read_text()

def slide(sd, i, n):
    th = sd.get('theme', 'dark')
    body = sd['html']
    pg = f'<div class="pg">{i}/{n}</div>' if n > 1 else ''
    sw = '<div class="swipe">Kaydır →</div>' if (n > 1 and i == 1) else ''
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s {th}">{sw}{body}<div class="brand">{MARK_T if th=="dark" else MARK_C}<span>@wearesalesforce</span></div>{pg}</div></body></html>'

async def render(spec):
    data = yaml.safe_load(Path(spec).read_text())
    out = Path(spec).parent.parent / 'out' / Path(spec).stem
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for post in data['posts']:
            sl = post['slides']
            for i, sd in enumerate(sl, 1):
                await pg.set_content(slide(sd, i, len(sl))); await pg.wait_for_timeout(150)
                f = out / f"{post['id']}_{i:02d}.png"
                await pg.screenshot(path=str(f)); print(f)
            (out / f"{post['id']}_caption.txt").write_text(post['caption'].strip() + '\n\n' + post['hashtags'].strip() + '\n')
        await b.close()

if __name__ == '__main__':
    asyncio.run(render(sys.argv[1]))
