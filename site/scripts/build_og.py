#!/usr/bin/env python3
"""Draw the link-preview thumbnails: one per article, one for the home page, and the
GitHub social preview for unk-scanner.

Cards use the palette of the article diagrams (public/diagrams/*.svg) and show each
article's own diagram, so a shared link previews the article's central figure.
Output: public/og/home.png and public/og/NN.png (1200x630), and
public/og/github-unk-scanner.png (1280x640, uploaded by hand in the repository settings).

Usage: python3 scripts/build_og.py   (scripts/sync-content.mjs adds the og:image tags at build time)
"""
import base64
import re
import subprocess
from html import escape
from pathlib import Path

from PIL import ImageFont

SITE = Path(__file__).resolve().parents[1]
DOCS = SITE / 'src/content/docs'
OUT = SITE / 'public/og'
BG, PANEL, LINE = '#ffffff', '#f4f6f4', '#b9c8be'
TEXT, MUTED, GREEN = '#202a26', '#53615a', '#17634f'
FONTS = '/usr/share/fonts/liberation-sans-fonts/LiberationSans-{}.ttf'
# Each article's own figure; Parts 6, 11, 13 and 14 reference theirs from public/diagrams.
DIAGRAMS = {'01': '01-clickfix', '02': '02-vsix', '03': '03-deobfuscation', '04': '04-collection',
            '05': '05-screen-capture', '06': '05-resolver', '07': '07-targeting', '08': '06-administration',
            '09': '07-echoes', '10': '10-evidence-map', '11': '11-detection-logic', '12': '12-framework-boundary',
            '13': '13-benchmark-results', '14': '14-rotation-failure'}


def wrap(s, size, width, bold=True):
    font = ImageFont.truetype(FONTS.format('Bold' if bold else 'Regular'), size)
    lines, line = [], ''
    for word in s.split():
        trial = f'{line} {word}'.strip()
        if font.getlength(trial) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def text(x, y, s, size, fill=TEXT, weight=400):
    return (f'<text x="{x}" y="{y}" font-family="Liberation Sans" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" xml:space="preserve">{escape(s)}</text>')


def image(path, x, y, w, h):
    """Panel sized to the diagram's aspect ratio, centred vertically in the space given."""
    iw, ih = map(int, subprocess.run(['magick', 'identify', '-format', '%w %h', str(path)],
                                     capture_output=True, text=True, check=True).stdout.split())
    fitted = min(h, round((w - 24) * ih / iw) + 24)
    y, h = y + (h - fitted) // 2, fitted
    data = base64.b64encode(path.read_bytes()).decode()
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<image x="{x + 12}" y="{y + 12}" width="{w - 24}" height="{h - 24}" preserveAspectRatio="xMidYMid meet" '
            f'href="data:image/png;base64,{data}"/>')


def card(width, height, label, title, tagline, footer, diagram, split=530):
    """Text column on the left, the article's diagram on the right."""
    b = f'<rect width="{width}" height="{height}" fill="{BG}"/><rect width="{width}" height="10" fill="{GREEN}"/>'
    b += text(60, 92, label, 26, GREEN, 700)
    size = 50
    lines = wrap(title, size, split - 110)
    while len(lines) > 4:
        size -= 4
        lines = wrap(title, size, split - 110)
    y = 170
    for line in lines:
        b += text(60, y, line, size, TEXT, 700)
        y += int(size * 1.18)
    for line in wrap(tagline, 24, split - 110, bold=False)[:4]:
        b += text(60, y + 18, line, 24, MUTED)
        y += 32
    b += f'<rect x="60" y="{height - 98}" width="{split - 90}" height="1.5" fill="{LINE}"/>'
    b += text(60, height - 54, footer, 22, MUTED)
    b += image(diagram, split, 60, width - split - 50, height - 120)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{b}</svg>'


def render(svg, png):
    tmp = png.with_suffix('.svg')
    tmp.write_text(svg)
    subprocess.run(['magick', '-density', '96', '-background', BG, f'RSVG:{tmp}', '-flatten', '-strip', str(png)], check=True)
    tmp.unlink()
    print(png.relative_to(SITE))


def front_matter(path):
    head = re.match(r'---\n(.*?)\n---\n', path.read_text(), re.S).group(1)
    get = lambda key: re.search(rf'^{key}:\s*"?(.*?)"?\s*$', head, re.M).group(1)
    return get('title'), get('description')


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    footer = 'krasforge.github.io/UNK_DeadDrop'
    for path in sorted((DOCS / 'articles').glob('[0-9][0-9]-*.md')):
        part = path.stem[:2]
        title, description = front_matter(path)
        render(card(1200, 630, f'UNK_DeadDrop · Part {int(part)} of 14', title, '', footer,
                    SITE / f'public/diagrams/{DIAGRAMS[part]}.png'), OUT / f'{part}.png')
    render(card(1200, 630, 'Fourteen-part technical series', 'UNK_DeadDrop',
                'Fake job interviews that reach developer machines, reconstructed from the artifacts without running a sample.',
                footer, SITE / 'public/diagrams/10-evidence-map.png'), OUT / 'home.png')
    render(card(1280, 640, 'Open-source static scanner', 'unk-scanner',
                'Parse-only triage of malicious JavaScript and VS Code extensions. Recovers obfuscated strings without running them.',
                'github.com/KrasForge/unk-scanner', SITE / 'public/diagrams/14-rotation-failure.png', split=560),
           OUT / 'github-unk-scanner.png')
