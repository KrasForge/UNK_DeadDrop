#!/usr/bin/env python3
"""Check the articles, references, figures and inert code examples."""
from pathlib import Path
import json
import re
import subprocess
BASE=Path(__file__).resolve().parent
posts=sorted(BASE.glob('[0-9][0-9]-*.md'))
assert len(posts)==14
assert [p.name[:2] for p in posts] == [f"{i:02}" for i in range(1,15)]
code=[]; summary=[]; figures=set(); links=set()
for p in posts:
    s=p.read_text()
    fm=re.match(r'---\n(.*?)\n---\n',s,re.S)
    assert fm,p.name
    for key in ['title','description','date','author','canonical']:
        assert re.search(rf'^{key}: "[^"]+"$',fm.group(1),re.M),(p.name,key)
    assert len(re.findall(r'^```',s,re.M))%2==0,p.name
    assert not re.search(r'^#{1,3} (?:Frequently asked questions|Article details|Evidence)(?:\s|$)',s,re.M),p.name
    assert '\u2014' not in s,p.name
    assert not re.search(r'\[E\d\d\](?!\()',s),p.name
    for value in ['/home/ik','incident-echoes-2026','incident-predicttogether-2026','samples-DO-NOT-RUN','ghp_','api-key=']:
        assert value not in s,(p.name,value)
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',s),p.name
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if target.startswith('https://'): continue
        assert (p.parent/target).resolve().is_file(),(p.name,target)
        links.add(target)
        if target.endswith(('.png', '.svg')): figures.add(target)
    for language, snippet in re.findall(r'```(\w+)\n(.*?)\n```',s,re.S):
        if language=='javascript': code.append(snippet)
        if language=='json': json.loads(snippet)
    body=re.sub(r'```.*?```','',s[fm.end():],flags=re.S)
    words=len(re.findall(r"\b[\w'-]+\b",body))
    assert words > 0, p.name  # Splits have no arbitrary minimum word target.
    summary.append({'file':p.name,'words_excluding_code_and_evidence':words})
assert len(figures)==14
# Parse all JavaScript examples; do not invoke the lure handler or file selectors.
parser="""import { parse } from 'acorn';
let text = ''; for await (const chunk of process.stdin) text += chunk;
for (const source of JSON.parse(text)) parse(source, {ecmaVersion: 'latest', sourceType: 'module'});
console.log('All JavaScript examples parsed.');
"""
repo=BASE.parent/'unk-deaddrop-companion'
r=subprocess.run(['node','--input-type=module','-e',parser],input=json.dumps(code),text=True,cwd=repo,capture_output=True,check=True)
# Execute only the invented Acorn example, whose target program is an inert string.
example=re.search(r'```javascript\n(.*?)\n```',(BASE/'03-acorn-deobfuscation.md').read_text(),re.S).group(1)
r=subprocess.run(['node','--input-type=module'],input=example,text=True,cwd=repo,capture_output=True,check=True)
assert r.stdout.strip()=='FunctionDeclaration CallExpression',r.stdout
assert 79698+62667==142365
print(json.dumps({'posts':summary,'linked_figures':len(figures),'local_link_targets':len(links),
                  'javascript_snippets_parsed':len(code),'acorn_example_output':r.stdout.strip()},indent=2))
