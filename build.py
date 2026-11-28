#!/usr/bin/env python3
"""We Are Sales Force – statik site üreticisi (TR/EN)."""
import re, json, shutil, datetime, html
from pathlib import Path
import markdown, yaml

ROOT = Path(__file__).parent
C = ROOT / 'content'
OUT = ROOT / 'dist'
DOMAIN = 'https://www.wearesalesforce.com'
TODAY = datetime.date.today().isoformat()

SEC = {  # section -> url folder per language
    'guide':    {'tr': 'rehber',  'en': 'en/guide'},
    'tools':    {'tr': 'araclar', 'en': 'en/tools'},
    'articles': {'tr': 'yazilar', 'en': 'en/articles'},
}
PAGES = {  # single pages
    'home':     {'tr': '',        'en': 'en'},
    'guide':    {'tr': 'rehber',  'en': 'en/guide'},
    'tools':    {'tr': 'araclar', 'en': 'en/tools'},
    'articles': {'tr': 'yazilar', 'en': 'en/articles'},
    'glossary': {'tr': 'sozluk',  'en': 'en/glossary'},
    'about':    {'tr': 'hakkinda','en': 'en/about'},
}
T = {
 'tr': dict(guide='Rehber', tools='Araçlar', articles='Yazılar', glossary='Sözlük', about='Hakkında',
            search='Ara', search_ph='Rehberde, araçlarda ve sözlükte ara…', min='dk okuma', module='Modül',
            prev='Önceki modül', next='Sonraki modül', on_page='Bu sayfada', updated='Güncelleme',
            related='İlgili araçlar', tagline='Satış gücü yönetimi için açık başvuru kaynağı',
            footer='Satış gücü ekipleri ve yöneticileri için özgün, uygulanabilir rehberler, araçlar ve şablonlar.',
            by='Hazırlayan', lang_other='EN', all_modules='Tüm modüller', read='Oku', open='Aç',
            no_result='Sonuç bulunamadı', print='Yazdır', newest='En yeni yazılar', back='Tüm yazılar'),
 'en': dict(guide='Guide', tools='Tools', articles='Articles', glossary='Glossary', about='About',
            search='Search', search_ph='Search the guide, tools and glossary…', min='min read', module='Module',
            prev='Previous module', next='Next module', on_page='On this page', updated='Updated',
            related='Related tools', tagline='An open reference for sales force management',
            footer='Original, practical guides, tools and templates for sales force teams and their managers.',
            by='Created by', lang_other='TR', all_modules='All modules', read='Read', open='Open',
            no_result='No results', print='Print', newest='Latest articles', back='All articles'),
}

def slugify(s):
    tr = str.maketrans('çğıöşüÇĞİÖŞÜ', 'cgiosuCGIOSU')
    s = s.translate(tr).lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def load(lang, sec):
    items = []
    d = C / lang / sec
    if not d.exists(): return items
    for f in sorted(d.glob('*.md')):
        raw = f.read_text()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
        meta = yaml.safe_load(m.group(1)); body = m.group(2)
        meta.setdefault('slug', f.stem.split('_', 1)[-1])
        meta['body'] = body; meta['sec'] = sec; meta['lang'] = lang
        items.append(meta)
    items.sort(key=lambda x: (x.get('order', 99), x.get('date', '')), reverse=(sec == 'articles'))
    return items

def url(lang, sec=None, slug=None, page=None):
    if page is not None:
        p = PAGES[page][lang]
    else:
        p = f"{SEC[sec][lang]}/{slug}"
    return (p + '/') if p else ''

def rel(from_url, to_url):
    depth = from_url.count('/')
    return ('../' * depth) + to_url if (('../' * depth) + to_url) else './'

MD = lambda: markdown.Markdown(extensions=['extra', 'toc', 'sane_lists', 'md_in_html'],
                                extension_configs={'toc': {'slugify': lambda v, s: slugify(v), 'toc_depth': '2-2'}})

def render_md(text):
    md = MD()
    h = md.convert(text)
    return h, md.toc_tokens

def reading_time(text):
    return max(2, round(len(re.findall(r'\w+', text)) / 200))

ICONS = {
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 'portfolio': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 'goal': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
 'hunt': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/>',
 'visit': '<path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="10" cy="7" r="4"/><path d="M21 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'org': '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-5h14v5"/>',
 'profile': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'money': '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/>',
 'learn': '<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 'calc': '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h8"/>',
 'check': '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
 'form': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
 'book': '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5V21h16"/>',
 'pen': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 'insta': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
}
def icon(name, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, ICONS["book"])}</svg>'

LOGO = '<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#041E41"/><rect x="9" y="22" width="5" height="9" rx="1.2" fill="#F3BF5C"/><rect x="17.5" y="16" width="5" height="15" rx="1.2" fill="#F3BF5C"/><rect x="26" y="9" width="5" height="22" rx="1.2" fill="#E5484D"/></svg>'

def page(lang, cur_url, title, body, desc='', alt_url=None, active='', extra_head='', scripts=''):
    t = T[lang]; r = lambda u: rel(cur_url, u)
    nav = ''.join(f'<a href="{r(url(lang, page=k))}" class="{"on" if active == k else ""}">{t[k]}</a>' for k in ('guide', 'tools', 'articles', 'glossary', 'about'))
    other = 'en' if lang == 'tr' else 'tr'
    alt = alt_url if alt_url is not None else url(other, page='home')
    full_title = f'{title} · We Are Sales Force' if title else 'We Are Sales Force – ' + t['tagline']
    hre = f'<link rel="alternate" hreflang="{lang}" href="{DOMAIN}/{cur_url}"><link rel="alternate" hreflang="{other}" href="{DOMAIN}/{alt}">'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc or t['tagline'])}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc or t['tagline'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/{cur_url}">
<meta property="og:image" content="{DOMAIN}/assets/og.png">
<link rel="canonical" href="{DOMAIN}/{cur_url}">
{hre}
<link rel="icon" href="{r('assets/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{r('assets/style.css')}">
{extra_head}
</head>
<body data-root="{r('')}" data-lang="{lang}">
<a class="skip" href="#main">{'İçeriğe geç' if lang == 'tr' else 'Skip to content'}</a>
<header class="top">
 <div class="wrap top-in">
  <a class="brand" href="{r(url(lang, page='home'))}"><img class="logo-mark" src="{r('assets/wasf-mark.svg')}" alt="WASF"><span>We Are Sales Force</span></a>
  <nav class="nav" id="nav">{nav}</nav>
  <div class="top-act">
   <button class="sbtn" id="sbtn" aria-label="{t['search']}">{icon('search')}<span>{t['search']}</span><kbd>/</kbd></button>
   <a class="lang" href="{r(alt)}" hreflang="{other}">{t['lang_other']}</a>
   <button class="burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
 <div class="wrap foot-in">
  <div><a class="foot-logo" href="{r(url(lang, page='home'))}"><img src="{r('assets/wasf-logo-transparent.svg')}" alt="WASF – we are sales force"></a>
   <p>{t['footer']}</p>
   <p class="by">{t['by']}: <b>Bora Özkalp</b></p></div>
  <div><h4>{t['guide']}</h4>{''.join(f'<a href="{r(url(lang, "guide", g["slug"]))}">{g["num"]:02d} · {g["short"]}</a>' for g in GUIDES[lang])}</div>
  <div><h4>{t['tools']}</h4>{''.join(f'<a href="{r(url(lang, "tools", x["slug"]))}">{x["title"]}</a>' for x in TOOLS[lang])}
   <h4 style="margin-top:18px">Instagram</h4><a href="https://www.instagram.com/wearesalesforce/" rel="noopener">{icon('insta')} @wearesalesforce</a></div>
 </div>
 <div class="wrap legal">© {datetime.date.today().year} We Are Sales Force · {'Tüm içerik özgün olarak hazırlanmıştır; bağımsız bir yayındır ve herhangi bir yazılım markasıyla bağlantılı değildir.' if lang == 'tr' else 'All content is original; an independent publication not affiliated with any software brand.'}</div>
</footer>
<div class="search" id="search" hidden>
 <div class="search-box" role="dialog" aria-modal="true" aria-label="{t['search']}">
  <div class="search-in">{icon('search')}<input id="q" type="search" placeholder="{t['search_ph']}" autocomplete="off"><button id="sclose" aria-label="Kapat">Esc</button></div>
  <div id="sres" class="sres" data-empty="{t['no_result']}"></div>
 </div>
</div>
<script src="{r('assets/search-index.js')}"></script>
<script src="{r('assets/app.js')}"></script>
{scripts}
</body>
</html>'''

GUIDES, TOOLS, ARTS = {}, {}, {}
INDEX = []

def toc_html(tokens, lang):
    if not tokens: return ''
    return f'<nav class="toc"><h4>{T[lang]["on_page"]}</h4>' + ''.join(f'<a href="#{x["id"]}">{x["name"]}</a>' for x in tokens) + '</nav>'

def strip(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'assets', OUT / 'assets')
    for lang in ('tr', 'en'):
        GUIDES[lang] = load(lang, 'guide')
        ARTS[lang] = load(lang, 'articles')
    import tools as TL
    for lang in ('tr', 'en'):
        TOOLS[lang] = TL.TOOLS[lang]
    glossary = yaml.safe_load((C / 'glossary.yaml').read_text())
    sitemap = []

    def write(u, s):
        p = OUT / u / 'index.html' if u else OUT / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s); sitemap.append(u)

    for lang in ('tr', 'en'):
        t = T[lang]; other = 'en' if lang == 'tr' else 'tr'
        G = GUIDES[lang]
        # ---- guide modules
        for i, g in enumerate(G):
            u = url(lang, 'guide', g['slug'])
            og = next(x for x in GUIDES[other] if x['num'] == g['num'])
            h, toc = render_md(g['body'])
            r = lambda x: rel(u, x)
            prev = G[i - 1] if i > 0 else None; nxt = G[i + 1] if i < len(G) - 1 else None
            pn = '<div class="pn">' + (f'<a class="p" href="{r(url(lang, "guide", prev["slug"]))}"><small>← {t["prev"]}</small>{prev["title"]}</a>' if prev else '<span></span>') + (f'<a class="n" href="{r(url(lang, "guide", nxt["slug"]))}"><small>{t["next"]} →</small>{nxt["title"]}</a>' if nxt else '<span></span>') + '</div>'
            rel_tools = ''.join(f'<a class="mini-tool" href="{r(url(lang, "tools", x["slug"]))}">{icon(x["icon"])}<span>{x["title"]}</span></a>' for x in TOOLS[lang] if g['num'] in x.get('modules', []))
            side = toc_html(toc, lang) + (f'<div class="side-tools"><h4>{t["related"]}</h4>{rel_tools}</div>' if rel_tools else '')
            body = f'''<section class="phero mod"><div class="wrap">
 <div class="crumb"><a href="{r(url(lang, page='guide'))}">{t['guide']}</a> / {t['module']} {g['num']:02d}</div>
 <div class="phero-row"><div class="mod-ic">{icon(g['icon'], 'ic big')}<b>{g['num']:02d}</b></div>
 <div><h1>{g['title']}</h1><p class="lead">{g['summary']}</p>
 <div class="meta"><span>{reading_time(g['body'])} {t['min']}</span><span>{t['updated']}: {g.get('updated', TODAY)}</span><button class="linkbtn" onclick="window.print()">{t['print']}</button></div></div></div>
</div></section>
<div class="wrap doc"><aside class="side">{side}</aside><article class="prose">{h}{pn}</article></div>'''
            write(u, page(lang, u, g['title'], body, g['summary'], url(other, 'guide', og['slug']), 'guide'))
            INDEX.append(dict(l=lang, t=g['title'], s=g['summary'], u=u, k=t['guide'], x=strip(h)[:4000]))
        # ---- guide index
        u = url(lang, page='guide'); r = lambda x: rel(u, x)
        cards = ''.join(f'''<a class="mcard" href="{r(url(lang, 'guide', g['slug']))}"><div class="mcard-top">{icon(g['icon'])}<b>{g['num']:02d}</b></div><h3>{g['title']}</h3><p>{g['summary']}</p><span class="q">{g['question']}</span></a>''' for g in G)
        intro = ('Satış gücü yönetimini 11 modülde, uçtan uca bir sistem olarak ele alıyoruz. Her modül önce yönetim mantığını anlatır, ardından sahada nasıl uygulanacağını kontrol listeleri, örnekler ve şablonlarla gösterir.' if lang == 'tr' else
                 'We treat sales force management as one end-to-end system in 11 modules. Each module explains the management logic first, then shows how to apply it in the field with checklists, examples and templates.')
        body = f'<section class="phero"><div class="wrap"><h1>{t["guide"]}</h1><p class="lead">{intro}</p></div></section><div class="wrap"><div class="flow">{FLOW(lang, r)}</div><div class="mgrid">{cards}</div></div>'
        write(u, page(lang, u, t['guide'], body, intro, url(other, page='guide'), 'guide'))
        # ---- tools
        for x in TOOLS[lang]:
            u = url(lang, 'tools', x['slug']); r = lambda y: rel(u, y)
            ox = next(y for y in TOOLS[other] if y['key'] == x['key'])
            mods = ''.join(f'<a class="chip" href="{r(url(lang, "guide", g["slug"]))}">{t["module"]} {g["num"]:02d} · {g["short"]}</a>' for g in G if g['num'] in x.get('modules', []))
            body = f'''<section class="phero tool"><div class="wrap"><div class="crumb"><a href="{r(url(lang, page='tools'))}">{t['tools']}</a></div>
<div class="phero-row"><div class="mod-ic">{icon(x['icon'], 'ic big')}</div><div><h1>{x['title']}</h1><p class="lead">{x['summary']}</p><div class="chips">{mods}</div></div></div></div></section>
<div class="wrap narrow tool-body">{x['html']}</div>'''
            write(u, page(lang, u, x['title'], body, x['summary'], url(other, 'tools', ox['slug']), 'tools', scripts=f'<script src="{r("assets/tools.js")}"></script>'))
            INDEX.append(dict(l=lang, t=x['title'], s=x['summary'], u=u, k=t['tools'], x=strip(x['html'])[:1500]))
        u = url(lang, page='tools'); r = lambda y: rel(u, y)
        cards = ''.join(f'<a class="tcard" href="{r(url(lang, "tools", x["slug"]))}">{icon(x["icon"])}<div><h3>{x["title"]}</h3><p>{x["summary"]}</p><span class="tag">{x["kind"]}</span></div></a>' for x in TOOLS[lang])
        intro = ('Sahada ve yönetim toplantılarında doğrudan kullanabileceğiniz hesaplayıcılar, formlar ve kontrol listeleri. Hepsi tarayıcıda çalışır; hiçbir veri kaydedilmez.' if lang == 'tr' else
                 'Calculators, forms and checklists you can use directly in the field and in management meetings. Everything runs in your browser; no data is stored.')
        body = f'<section class="phero"><div class="wrap"><h1>{t["tools"]}</h1><p class="lead">{intro}</p></div></section><div class="wrap"><div class="tgrid">{cards}</div></div>'
        write(u, page(lang, u, t['tools'], body, intro, url(other, page='tools'), 'tools'))
        # ---- articles
        A = ARTS[lang]
        for a in A:
            u = url(lang, 'articles', a['slug']); r = lambda y: rel(u, y)
            oa = next((y for y in ARTS[other] if y['key'] == a['key']), None)
            h, _ = render_md(a['body'])
            body = f'''<section class="phero art"><div class="wrap narrow"><div class="crumb"><a href="{r(url(lang, page='articles'))}">{t['articles']}</a> · {a['cat']}</div><h1>{a['title']}</h1><p class="lead">{a['summary']}</p><div class="meta"><span>{a['date']}</span><span>{reading_time(a['body'])} {t['min']}</span><span>{t['by']}: Bora Özkalp</span></div></div></section>
<div class="wrap narrow"><article class="prose">{h}<p class="back"><a href="{r(url(lang, page='articles'))}">← {t['back']}</a></p></article></div>'''
            write(u, page(lang, u, a['title'], body, a['summary'], url(other, 'articles', oa['slug']) if oa else url(other, page='articles'), 'articles'))
            INDEX.append(dict(l=lang, t=a['title'], s=a['summary'], u=u, k=t['articles'], x=strip(h)[:3000]))
        u = url(lang, page='articles'); r = lambda y: rel(u, y)
        intro = ('Sahadan notlar, yöntem açıklamaları ve satış yöneticileri için kısa, uygulanabilir yazılar. Düzenli olarak güncellenir.' if lang == 'tr' else
                 'Field notes, method explainers and short, practical pieces for sales managers. Updated regularly.')
        body = f'<section class="phero"><div class="wrap"><h1>{t["articles"]}</h1><p class="lead">{intro}</p></div></section><div class="wrap"><div class="agrid">{"".join(ACARD(lang, a, r) for a in A)}</div></div>'
        write(u, page(lang, u, t['articles'], body, intro, url(other, page='articles'), 'articles'))
        # ---- glossary
        u = url(lang, page='glossary'); r = lambda y: rel(u, y)
        terms = sorted(glossary, key=lambda g: g[lang]['term'].lower().translate(str.maketrans('çğıöşü', 'cgiosu')))
        letters = []
        rows = []
        for g in terms:
            L = g[lang]['term'][0].upper().translate(str.maketrans('ÇĞİÖŞÜ', 'CGIOSU'))
            if L not in letters:
                letters.append(L); rows.append(f'<h2 id="l-{L}" class="gl-letter">{L}</h2>')
            o = g['en' if lang == 'tr' else 'tr']['term']
            mod = next((x for x in G if x['num'] == g.get('module')), None)
            ml = f' <a class="chip" href="{r(url(lang, "guide", mod["slug"]))}">{t["module"]} {mod["num"]:02d}</a>' if mod else ''
            rows.append(f'<div class="gl" id="{slugify(g[lang]["term"])}"><dt>{g[lang]["term"]} <span>{o}</span></dt><dd>{g[lang]["def"]}{ml}</dd></div>')
            INDEX.append(dict(l=lang, t=g[lang]['term'], s=g[lang]['def'][:160], u=u + '#' + slugify(g[lang]['term']), k=t['glossary'], x=o))
        intro = (f'Satış gücü yönetiminde sık kullanılan {len(terms)} kavram; Türkçe karşılıkları, İngilizce eşdeğerleri ve ilgili modüllerle.' if lang == 'tr' else
                 f'{len(terms)} common sales force management terms, with Turkish equivalents and related modules.')
        az = ''.join(f'<a href="#l-{L}">{L}</a>' for L in letters)
        body = f'<section class="phero"><div class="wrap"><h1>{t["glossary"]}</h1><p class="lead">{intro}</p><div class="az">{az}</div></div></section><div class="wrap narrow"><input class="gl-filter" id="glf" type="search" placeholder="{"Sözlükte filtrele…" if lang == "tr" else "Filter terms…"}"><dl class="gls" id="gls">{"".join(rows)}</dl></div>'
        write(u, page(lang, u, t['glossary'], body, intro, url(other, page='glossary'), 'glossary'))
        # ---- about
        u = url(lang, page='about')
        h, _ = render_md((C / lang / 'about.md').read_text())
        body = f'<section class="phero"><div class="wrap narrow"><h1>{t["about"]}</h1></div></section><div class="wrap narrow"><article class="prose">{h}</article></div>'
        write(u, page(lang, u, t['about'], body, '', url(other, page='about'), 'about'))
        # ---- home
        u = url(lang, page='home'); r = lambda y: rel(u, y)
        write(u, page(lang, u, '', HOME(lang, r), T[lang]['tagline'], url(other, page='home'), 'home'))

    (OUT / 'assets' / 'search-index.js').write_text('window.SEARCH=' + json.dumps(INDEX, ensure_ascii=False) + ';')
    (OUT / 'CNAME').write_text('www.wearesalesforce.com\n')
    (OUT / '.nojekyll').write_text('')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    sm = ''.join(f'<url><loc>{DOMAIN}/{x}</loc><lastmod>{TODAY}</lastmod></url>' for x in sitemap)
    (OUT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    nf = page('tr', '404.html'.replace('.html', ''), '404', f'<section class="phero"><div class="wrap narrow"><h1>404</h1><p class="lead">Aradığınız sayfa bulunamadı. / Page not found.</p><p><a class="btn" href="/">Ana sayfa / Home</a></p></div></section>')
    (OUT / '404.html').write_text(nf.replace('href="../', 'href="/').replace('src="../', 'src="/'))
    print('pages', len(sitemap), 'index', len(INDEX))

def FLOW(lang, r):
    G = GUIDES[lang]
    return ''.join(f'<a href="{r(url(lang, "guide", g["slug"]))}" title="{g["title"]}"><b>{g["num"]:02d}</b><span>{g["short"]}</span></a>' for g in G)

def ACARD(lang, a, r):
    return f'<a class="acard" href="{r(url(lang, "articles", a["slug"]))}"><span class="cat">{a["cat"]}</span><h3>{a["title"]}</h3><p>{a["summary"]}</p><span class="meta">{a["date"]} · {reading_time(a["body"])} {T[lang]["min"]}</span></a>'

def HOME(lang, r):
    t = T[lang]; G = GUIDES[lang]
    if lang == 'tr':
        h1 = 'Satış gücünüzü <em>kişisel gayretten</em> sistemli performansa taşıyın.'
        sub = 'Satış temsilcileri, satış gücü yöneticileri ve satış direktörleri için açık, özgün ve uygulanabilir bir başvuru kaynağı: 11 modüllük yönetim rehberi, sahada kullanılan araçlar, sözlük ve düzenli yazılar.'
        cta1, cta2 = 'Rehbere başla', 'Araçları keşfet'
        stats = [('11', 'yönetim modülü'), (str(len(TOOLS[lang])), 'interaktif araç'), ('2', 'dil: TR + EN'), ('Açık', 'ücretsiz erişim')]
        sys_t = 'Satış gücü bir sistemdir'
        sys_p = 'Doğru müşteriyi seçmeden hedef konmaz; hedef olmadan performans izlenmez; izlenmeyen performans koçlukla gelişmez. Rehber bu zinciri baştan sona kurar.'
        who = [('Satış temsilcisi', 'Ziyaret hazırlığı, soru sorma, itiraz ve kapanış teknikleri; günlük kontrol listeleri.', 'visit'),
               ('Satış gücü yöneticisi', 'Portföy kurma, hedef kırılımı, performans takibi ve koçluk günü planı.', 'chart'),
               ('Satış direktörü', 'Organizasyon tasarımı, yetkinlik modeli, prim sistemi ve uyum çerçevesi.', 'org')]
        who_t = 'Kimin için?'; tools_t = 'Öne çıkan araçlar'; arts_t = t['newest']
        ig = 'Kısa ipuçları, infografikler ve sahadan notlar için Instagram’da takip edin.'
    else:
        h1 = 'Move your sales force from <em>personal effort</em> to systematic performance.'
        sub = 'An open, original and practical reference for sales reps, sales force managers and sales directors: an 11-module management guide, field-ready tools, a glossary and regular articles.'
        cta1, cta2 = 'Start the guide', 'Explore the tools'
        stats = [('11', 'management modules'), (str(len(TOOLS[lang])), 'interactive tools'), ('2', 'languages: TR + EN'), ('Free', 'and open')]
        sys_t = 'A sales force is a system'
        sys_p = 'Without choosing the right customers you cannot set targets; without targets you cannot track performance; and untracked performance does not improve through coaching. The guide builds this chain end to end.'
        who = [('Sales representative', 'Visit preparation, questioning, objection handling and closing; daily checklists.', 'visit'),
               ('Sales force manager', 'Building portfolios, breaking down targets, tracking performance and planning coaching days.', 'chart'),
               ('Sales director', 'Organisation design, competency model, incentive scheme and compliance framework.', 'org')]
        who_t = 'Who is it for?'; tools_t = 'Featured tools'; arts_t = t['newest']
        ig = 'Follow us on Instagram for quick tips, infographics and field notes.'
    st = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in stats)
    mods = ''.join(f'<a class="mcard sm" href="{r(url(lang, "guide", g["slug"]))}"><div class="mcard-top">{icon(g["icon"])}<b>{g["num"]:02d}</b></div><h3>{g["title"]}</h3><span class="q">{g["question"]}</span></a>' for g in G)
    tl = ''.join(f'<a class="tcard" href="{r(url(lang, "tools", x["slug"]))}">{icon(x["icon"])}<div><h3>{x["title"]}</h3><p>{x["summary"]}</p></div></a>' for x in TOOLS[lang][:4])
    wh = ''.join(f'<div class="who">{icon(i)}<h3>{a}</h3><p>{b}</p></div>' for a, b, i in who)
    ar = ''.join(ACARD(lang, a, r) for a in ARTS[lang][:3])
    return f'''<section class="hero"><div class="wrap hero-in">
 <div class="hero-txt"><span class="eyebrow">{t['tagline']}</span><h1>{h1}</h1><p>{sub}</p>
 <div class="ctas"><a class="btn" href="{r(url(lang, page='guide'))}">{cta1} →</a><a class="btn ghost" href="{r(url(lang, page='tools'))}">{cta2}</a></div></div>
 <div class="hero-art" aria-hidden="true">{HERO_SVG}</div>
</div><div class="wrap stats">{st}</div></section>
<section class="band"><div class="wrap"><div class="sec-h"><h2>{sys_t}</h2><p>{sys_p}</p></div><div class="flow big">{FLOW(lang, r)}</div><div class="mgrid">{mods}</div></div></section>
<section class="band alt"><div class="wrap"><div class="sec-h"><h2>{who_t}</h2></div><div class="whos">{wh}</div></div></section>
<section class="band"><div class="wrap"><div class="sec-h row"><h2>{tools_t}</h2><a href="{r(url(lang, page='tools'))}">{t['tools']} →</a></div><div class="tgrid">{tl}</div></div></section>
<section class="band alt"><div class="wrap"><div class="sec-h row"><h2>{arts_t}</h2><a href="{r(url(lang, page='articles'))}">{t['articles']} →</a></div><div class="agrid">{ar}</div></div></section>
<section class="igband"><div class="wrap ig-in">{icon('insta', 'ic big')}<p>{ig}</p><a class="btn light" href="https://www.instagram.com/wearesalesforce/" rel="noopener">@wearesalesforce</a></div></section>'''

HERO_SVG = '''<svg viewBox="0 0 420 360" xmlns="http://www.w3.org/2000/svg">
<circle cx="300" cy="120" r="110" fill="#0B2A52"/><circle cx="300" cy="120" r="74" fill="none" stroke="#1E3B66"/><circle cx="300" cy="120" r="40" fill="none" stroke="#1E3B66"/><circle cx="300" cy="120" r="12" fill="#E5484D"/>
<g fill="#F3BF5C"><rect x="40" y="250" width="34" height="80" rx="6"/><rect x="92" y="215" width="34" height="115" rx="6"/><rect x="144" y="175" width="34" height="155" rx="6"/></g><rect x="196" y="125" width="34" height="205" rx="6" fill="#E5484D"/>
<path d="M40 190 C110 170 150 210 210 160 S300 110 300 120" fill="none" stroke="#4697D8" stroke-width="4" stroke-linecap="round"/>
<circle cx="300" cy="120" r="6" fill="#4697D8"/>
<g font-family="Inter,system-ui" font-size="13" font-weight="700" fill="#C9D1E0"><rect x="250" y="250" width="150" height="74" rx="12" fill="#0E2B55"/><text x="266" y="278">KPI</text><text x="266" y="304" fill="#4697D8" font-size="22">+18%</text></g>
</svg>'''

if __name__ == '__main__':
    build()
