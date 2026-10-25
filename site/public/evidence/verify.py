#!/usr/bin/env python3
"""Validate evidence-package completeness, fingerprints, citations and PDF layout."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import subprocess
import pymupdf
BASE=Path(__file__).resolve().parent
manifest=json.loads((BASE/'manifest.json').read_text())
expected={f'E{i:02d}' for i in range(1,22)}
assert {r['id'] for r in manifest['reports']}==expected
assert {p.stem for p in BASE.glob('E??.pdf')}==expected
results=[]
root=BASE.parents[2]
for register in sorted((BASE/'exhibits').glob('E??.artifacts.json')):
    for entry in json.loads(register.read_text()):
        locator=entry['path']
        if ' @ git ' in locator:
            path, revision=locator.rsplit(' @ git ',1)
            data=subprocess.check_output(['git','show',f'{revision}:{path}'],cwd=root)
        else:
            data=(root/locator).read_bytes()
        assert len(data)==entry['bytes'],(register.name,entry['name'],'size')
        assert hashlib.sha256(data).hexdigest()==entry['sha256'],(register.name,entry['name'],'hash')

for r in manifest['reports']:
    for exhibit in r['exhibit_files']:
        assert hashlib.sha256((BASE/exhibit['path']).read_bytes()).hexdigest()==exhibit['sha256']
    source=(BASE/r['markdown']).read_text()
    assert hashlib.sha256(source.encode()).hexdigest()==r['markdown_sha256']
    pdf=BASE/r['pdf']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==r['pdf_sha256']
    doc=pymupdf.open(pdf)
    content='\n'.join(p.get_text() for p in doc)
    assert r['id'] in doc[0].get_text()
    assert 'Source records and fingerprints' in content
    for sid in re.findall(r'\bS(\d+)\b',source):
        assert 1<=int(sid)<=len(r['sources']),(r['id'],sid)
    for entry in r['sources']:
        assert entry['sha256'] in content.replace('\n',''),(r['id'],entry['id'])
    for forbidden in ['/home/ik','incident-echoes','incident-predicttogether','incident-d2saitrade','samples-DO-NOT-RUN','deliverables/','ghp_','api-key=']:
        assert forbidden not in content,(r['id'],forbidden)
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}',content,re.I),r['id']
    for literal in re.findall(r'`([a-f0-9]{40,})`',source):
        assert len(literal)==64,(r['id'],literal)
    for page in doc:
        assert len(page.get_text().strip())>150,(r['id'],'sparse page')
        for word in page.get_text('words'):
            assert page.rect.contains(pymupdf.Rect(word[:4])),(r['id'],page.number,word)
        for font in page.get_fonts():
            assert doc.extract_font(font[0])[3],(r['id'],'unembedded font')
    results.append({'id':r['id'],'pages':len(doc),'words':len(content.split())})
with zipfile.ZipFile(BASE/'UNK_DeadDrop-E01-E21-PDFs.zip') as z:
    assert set(z.namelist())=={f'{e}.pdf' for e in expected}|{'SHA256SUMS'}
    assert z.testzip() is None
    for r in manifest['reports']:
        assert hashlib.sha256(z.read(r['pdf'])).hexdigest()==r['pdf_sha256']
preprint=pymupdf.open(BASE.parent/'UNK_DeadDrop-Preprint.pdf')
assert '1. Introduction' not in preprint[0].get_text()
assert '1. Introduction' in preprint[1].get_text()
for page in preprint:
    for word in page.get_text('words'):
        assert page.rect.contains(pymupdf.Rect(word[:4]))
print(json.dumps({'reports':results,'total_evidence_pages':sum(r['pages'] for r in results), 'preprint_pages':len(preprint)},indent=2))
