#!/usr/bin/env python3
"""Typeset the scanner paper from Markdown, in the style of ../preprint/build.py.

Unlike the threat-intelligence paper, this draft uses bullet and numbered lists,
bold and italic emphasis and one table, so the Markdown subset handled here is wider.
"""
import argparse
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle, ListFlowable, ListItem

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--final', action='store_true', help='Refuse to build while PENDING or verify markers remain')
parser.add_argument('--font-dir', type=Path, default=Path('/usr/share/fonts/liberation-serif-fonts'))
parser.add_argument('--mono-font', type=Path, default=Path('/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf'))
parser.add_argument('--output', type=Path, default=BASE / 'UNK-Scanner-Paper-DRAFT.pdf')
args = parser.parse_args()
meta = json.loads((BASE / 'metadata.json').read_text())
source = (BASE / 'paper.md').read_text()
markers = len(re.findall(r'\[PENDING|\[verify', source))
if args.final and markers:
    parser.error(f'{markers} [PENDING]/[verify] markers remain; resolve them before a final build.')
draft = bool(markers)
for name, filename in [('Serif', 'LiberationSerif-Regular.ttf'), ('SerifBold', 'LiberationSerif-Bold.ttf'), ('SerifItalic', 'LiberationSerif-Italic.ttf'), ('SerifBoldItalic', 'LiberationSerif-BoldItalic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(args.font_dir / filename)))
pdfmetrics.registerFont(TTFont('Code', str(args.mono_font)))
pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBoldItalic')


def markup(text):
    text = escape(text)
    code = []
    # Protect inline code from emphasis rules.
    text = re.sub(r'`([^`]+)`', lambda m: code.append(m.group(1)) or f'\0{len(code) - 1}\0', text)
    text = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<link href="\2" color="#000000">\1</link>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', text)
    # Open items stand out in the draft.
    text = re.sub(r'\[(PENDING[^\]]*|verify[^\]]*)\]', r'<font color="#b00000">[\1]</font>', text)
    text = re.sub(r'\bR(\d+)\b', r'\1', text)
    text = re.sub(r'(https://[^\s<"]+)(?![^<]*</link>)(?![^<]*">)', r'<link href="\1" color="#000000">\1</link>', text)
    return re.sub(r'\0(\d+)\0', lambda m: f'<font name="Code" size="8.6">{code[int(m.group(1))]}</font>', text)


class Paper(SimpleDocTemplate):
    def afterFlowable(self, item):
        if hasattr(item, 'heading'):
            key = f'h{self.seq.nextf("heading")}'
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(item.heading, key, item.level)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Serif', 10)
    canvas.drawCentredString(A4[0] / 2, 34, str(doc.page))
    if draft:
        canvas.setFont('SerifItalic', 8.5)
        canvas.setFillColor(colors.HexColor('#b00000'))
        canvas.drawCentredString(A4[0] / 2, A4[1] - 34, f'Draft {meta["date"]}: results pending, not for citation')
    canvas.restoreState()


body = dict(fontName='Serif', fontSize=11, leading=13.5, alignment=TA_JUSTIFY, allowWidows=0, allowOrphans=0)
styles = {
    'body': ParagraphStyle('body', firstLineIndent=14, spaceAfter=2, **body),
    'first': ParagraphStyle('first', spaceAfter=2, **body),
    'item': ParagraphStyle('item', spaceAfter=1.5, **body),
    'title': ParagraphStyle('title', fontName='SerifBold', fontSize=18, leading=21, alignment=TA_CENTER, spaceAfter=18),
    'author': ParagraphStyle('author', fontName='Serif', fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=3),
    'affiliation': ParagraphStyle('affiliation', fontName='Serif', fontSize=10, leading=13, alignment=TA_CENTER, spaceAfter=3),
    'date': ParagraphStyle('date', fontName='Serif', fontSize=10, leading=13, alignment=TA_CENTER, spaceBefore=8, spaceAfter=17),
    'note': ParagraphStyle('note', fontName='SerifItalic', fontSize=9.5, leading=12, alignment=TA_CENTER, leftIndent=30, rightIndent=30, spaceAfter=14, textColor=colors.HexColor('#b00000')),
    'abstract_title': ParagraphStyle('abstract_title', fontName='SerifBold', fontSize=10.5, leading=13, alignment=TA_CENTER, spaceAfter=5),
    'abstract': ParagraphStyle('abstract', fontName='Serif', fontSize=10, leading=12.4, leftIndent=22, rightIndent=22, alignment=TA_JUSTIFY, spaceAfter=9),
    'keywords': ParagraphStyle('keywords', fontName='Serif', fontSize=9, leading=11.5, leftIndent=22, rightIndent=22, spaceAfter=13),
    'section': ParagraphStyle('section', fontName='SerifBold', fontSize=12.5, leading=15, spaceBefore=15, spaceAfter=7, keepWithNext=True),
    'subsection': ParagraphStyle('subsection', fontName='SerifBold', fontSize=11, leading=14, spaceBefore=11, spaceAfter=5, keepWithNext=True),
    'reference': ParagraphStyle('reference', fontName='Serif', fontSize=9.5, leading=12, leftIndent=20, firstLineIndent=-20, spaceAfter=7),
    'cell': ParagraphStyle('cell', fontName='Serif', fontSize=9, leading=11, alignment=TA_LEFT),
    'head': ParagraphStyle('head', fontName='SerifBold', fontSize=9, leading=11, alignment=TA_LEFT),
}

lines = source.splitlines()
title = lines[0].lstrip('# ').strip()
abstract = source.split('## Abstract', 1)[1].split('\n## ', 1)[0].strip()
note = source.split('\n\n', 2)[1].strip() if source.split('\n\n', 2)[1].startswith('Draft') else None

flow = [Paragraph(markup(title), styles['title'])]
for author in meta['authors']:
    flow.append(Paragraph(escape(author['name']), styles['author']))
    if author.get('affiliation'):
        flow.append(Paragraph(escape(author['affiliation']), styles['affiliation']))
    if author.get('orcid'):
        orcid = escape(author['orcid'])
        flow.append(Paragraph(f'<link href="https://orcid.org/{orcid}">ORCID: {orcid}</link>', styles['affiliation']))
flow.append(Paragraph(escape(meta['date']) + (' · Draft' if draft else ' · Preprint'), styles['date']))
if draft and note:
    flow.append(Paragraph(markup(note), styles['note']))
flow.append(Paragraph('Abstract', styles['abstract_title']))
flow.append(Paragraph(markup(' '.join(abstract.splitlines())), styles['abstract']))
flow.append(Paragraph('<b>Keywords:</b> ' + escape('; '.join(meta['keywords'])), styles['keywords']))
flow.append(PageBreak())


def bullets(items, ordered):
    return ListFlowable([ListItem(Paragraph(markup(t), styles['item']), leftIndent=16) for t in items],
                        bulletType='1' if ordered else 'bullet', start='1' if ordered else '•', bulletFormat='%s.' if ordered else None,
                        bulletFontName='Serif', bulletFontSize=10 if ordered else 9, leftIndent=16, spaceAfter=4)


def table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows if not re.match(r'^\|\s*-', r)]
    data = [[Paragraph(markup(c), styles['head' if i == 0 else 'cell']) for c in row] for i, row in enumerate(cells)]
    n = len(cells[0])
    # The corpus table has a wide description column; numeric tables get a wide first column.
    widths = [62, 230, 159] if n == 3 else [151] + [300 / (n - 1)] * (n - 1)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEABOVE', (0, 0), (-1, 0), 0.8, colors.black),
                           ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black), ('LINEBELOW', (0, -1), (-1, -1), 0.8, colors.black),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    t.spaceBefore, t.spaceAfter = 6, 8
    return t


main = source[source.index('## 1.'):]
references = False
first = True
for block in re.split(r'\n\s*\n', main.strip()):
    block_lines = block.splitlines()
    if block.startswith('## '):
        heading = block[3:].strip()
        references = heading == 'References'
        p = Paragraph(markup(heading), styles['section'])
        p.heading, p.level = heading, 0
        flow.append(p)
        first = True
    elif block.startswith('### '):
        heading = block[4:].strip()
        p = Paragraph(markup(heading), styles['subsection'])
        p.heading, p.level = heading, 1
        flow.append(p)
        first = True
    elif block.startswith('|'):
        flow.append(table(block_lines))
    elif re.match(r'^(- |\d+\. )', block):
        ordered = bool(re.match(r'^\d+\. ', block))
        items = []
        for line in block_lines:
            if re.match(r'^(- |\d+\. )', line):
                items.append(re.sub(r'^(- |\d+\. )', '', line))
            else:
                items[-1] += ' ' + line.strip()
        flow.append(bullets(items, ordered))
        first = True
    else:
        text = ' '.join(block_lines)
        style = 'reference' if references and re.match(r'^\[R\d+\]', text) else 'first' if first else 'body'
        flow.append(Paragraph(markup(text), styles[style]))
        first = False

doc = Paper(str(args.output), pagesize=A4, leftMargin=72, rightMargin=72, topMargin=60, bottomMargin=60, title=title,
            author='; '.join(a['name'] for a in meta['authors']), subject='Static analysis of developer-targeting JavaScript; companion to the UNK_DeadDrop preprint', initialFontName='Serif')
doc.build(flow, onFirstPage=footer, onLaterPages=footer)
print(args.output, f'({markers} open markers)' if draft else '')
