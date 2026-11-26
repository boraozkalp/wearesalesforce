#!/usr/bin/env python3
"""WASF logosunun vektör (SVG) çizimi. Kaynak: Bora'nın wasf_logo (JPG). Renkler logodan örneklendi."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = Path(__file__).parent
FONTS = '/usr/share/fonts/truetype/google-fonts/'
Y, O, B, R, N = '#F3BF5C', '#F2862A', '#4697D8', '#F25657', '#041E41'

def text_path(font, text, x, y, size, center=False):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); s = size / font['head'].unitsPerEm; hm = font['hmtx']
    if center: x -= sum(hm[cmap[ord(c)]][0] for c in text) * s / 2
    d = ''
    for c in text:
        g = cmap[ord(c)]; pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y))); d += pen.getCommands(); x += hm[g][0] * s
    return d

bold = TTFont(FONTS + 'Poppins-Bold.ttf'); med = TTFont(FONTS + 'Poppins-Medium.ttf')
gs = bold.getGlyphSet(); g = bold.getBestCmap()[ord('S')]
bp = BoundsPen(gs); gs[g].draw(bp); x0, y0, x1, y1 = bp.bounds
sx = 360 / (x1 - x0); sy = 610 / (y1 - y0)
pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (sx, 0, 0, -sy, 1080 - x0 * sx, 605 + y0 * sy))); S = pen.getCommands()

MARK = f'''<g fill="{R}"><rect x="1300" y="0" width="160" height="600"/><path d="M1300 0H1700a40 40 0 0 1 40 40v60a40 40 0 0 1-40 40H1300z"/><path d="M1300 250H1640a40 40 0 0 1 40 40v60a40 40 0 0 1-40 40H1300z"/></g><path d="{S}" fill="{B}"/><path d="M745 600V245A165 165 0 0 1 1075 245V600" fill="none" stroke="{O}" stroke-width="150"/><rect x="745" y="320" width="330" height="95" fill="{O}"/><g fill="none" stroke="{Y}" stroke-width="150"><path d="M75 0V385A155 140 0 0 0 385 385V0"/><path d="M385 0V385A155 140 0 0 0 695 385V0"/></g>'''
TAG = text_path(med, '“we are sales force”', 790, 815, 118, center=True)

files = {
 'wasf-logo.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-160 -170 2060 1180"><rect x="-160" y="-170" width="2060" height="1180" fill="{N}"/>{MARK}<path d="{TAG}" fill="#fff"/></svg>',
 'wasf-logo-transparent.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1740 880">{MARK}<path d="{TAG}" fill="#fff"/></svg>',
 'wasf-mark-transparent.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1740 600">{MARK}</svg>',
 'wasf-mark.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-120 -120 1980 840"><rect x="-120" y="-120" width="1980" height="840" rx="150" fill="{N}"/>{MARK}</svg>',
 'wasf-icon.svg': f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-130 -700 2000 2000"><rect x="-130" y="-700" width="2000" height="2000" rx="360" fill="{N}"/>{MARK}</svg>',
}
for k, v in files.items(): (OUT / k).write_text(v)
print('ok', list(files))
