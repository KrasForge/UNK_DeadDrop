#!/usr/bin/env python3
"""Package only finished articles, original figures and linked supporting PDFs."""
from pathlib import Path
import hashlib
import re
import zipfile
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
posts=sorted(BASE.glob('[0-9][0-9]-*.md'))
assert len(posts)==12
references=[BASE/'historical-indicators.md',BASE/'artifact-reference.md']
files=set(posts+references+[BASE/'README.md',BASE/'VALIDATION.md',BASE/'build_diagrams.py',BASE/'assets/diagrams.json',BASE/'assets/DIAGRAMS.md'])
files.update((BASE/'assets').glob('*.svg'))
for p in posts+references:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if target.startswith('https://'): continue
        dest=(p.parent/target).resolve()
        assert dest.is_file(),dest
        dest.relative_to(ROOT)
        if dest.suffix in {'.png', '.svg', '.pdf', '.py', '.yar', '.yml'} or dest.name in {'requirements-dev.txt', 'LICENSE'}: files.add(dest)
checks=[]
output=BASE/'UNK_DeadDrop-Blog-Series.zip'
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):
        relative=p.relative_to(ROOT).as_posix()
        data=p.read_bytes()
        if p==BASE/'README.md':
            text=data.decode()
            text=re.sub(r'\[Download the series and linked supporting PDFs\]\(UNK_DeadDrop-Blog-Series.zip\)\.\nThe archive preserves the relative links between articles, images and evidence\.\n', 'This extracted collection preserves relative links between articles, images and evidence.\n', text)
            for edition in ('2026-10-25', '2026-10-26'):
                text=text.replace(f'[`rendered/{edition}/`](rendered/{edition}/index.html)', f'`rendered/{edition}/` (workspace previews are not included in this source archive)')
            data=text.encode()
        z.writestr(relative,data)
        checks.append(hashlib.sha256(data).hexdigest()+'  '+relative)
    z.writestr('SHA256SUMS','\n'.join(checks)+'\n')
    z.writestr('README.md','# UNK_DeadDrop technical blog series\n\nStart with [the series index](blog-series/README.md).\n\nTwelve articles with their diagrams and supporting PDFs. The hosted edition is at https://krasforge.github.io/UNK_DeadDrop/.\n')
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
    for line in z.read('SHA256SUMS').decode().splitlines():
        wanted,name=line.split('  ',1)
        assert hashlib.sha256(z.read(name)).hexdigest()==wanted,name
print(f'Packaged {len(posts)} posts and {len(files)-len(posts)} supporting files: {output}')
