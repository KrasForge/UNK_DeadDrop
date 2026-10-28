#!/usr/bin/env python3
"""Build explanatory SVG and PNG figures. Requires pymupdf and pillow.

All labels and counts come from the numbered articles and cited evidence reports.
No malware, network acquisition, or sample execution is involved.
"""
from pathlib import Path
from html import escape
import json
import subprocess
import math
import pymupdf
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
INK, MUTED, GREEN, AMBER = '#202a26', '#53615a', '#17634f', '#8c5518'
PALE, WARM, EDGE = '#eaf3ee', '#fff4df', '#b9c8be'
FONT = subprocess.check_output(['fc-match', '-f', '%{file}', 'sans-serif'],text=True).strip()
records = []

def width(s, size):
    return ImageFont.truetype(FONT, size).getlength(s)

def wrap(s, max_width, size):
    result = []
    for paragraph in s.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = f'{line} {word}'.strip()
            if line and width(candidate, size) > max_width:
                result.append(line)
                line = word
            else:
                line = candidate
        result.append(line)
    return result

class Figure:
    def __init__(self, filename, part, title, subtitle, height, sources, limit):
        self.name, self.h, self.part = filename, height, part
        self.title, self.subtitle, self.sources, self.limit = title, subtitle, sources, limit
        self.items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle + " " + limit)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#17634f"/></marker></defs>',
            '<rect width="1000" height="100%" fill="#fff"/>',
            '<g transform="translate(0,-120)">']

    def text(self, x, y, s, size=21, color=INK, bold=False, anchor='start'):
        assert '\u2014' not in s
        extent = width(s, size) * (1.05 if bold else 1)
        left = x if anchor == 'start' else x - extent if anchor == 'end' else x - extent/2
        assert left >= 0 and left + extent <= 1000, (self.name, s, left, extent)
        self.items.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(s)}</text>')

    def rect(self, x, y, w, h, fill='#fff', stroke=EDGE, dash=False, rx=3):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke if not dash else "none"}" stroke-width="1.5"/>')
        if dash:
            self.line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],color=stroke,arrow=False,dash=True)

    def line(self, points, color=GREEN, arrow=True, dash=False):
        for (x1,y1),(x2,y2) in zip(points,points[1:]):
            length=math.hypot(x2-x1,y2-y1)
            if not length: continue
            dx,dy=(x2-x1)/length,(y2-y1)/length
            segments=[(0,length)] if not dash else [(d,min(d+7,length)) for d in range(0,math.ceil(length),13)]
            for start,end in segments:
                self.items.append(f'<line x1="{x1+dx*start}" y1="{y1+dy*start}" x2="{x1+dx*end}" y2="{y1+dy*end}" stroke="{color}" stroke-width="2.5"/>')
        if arrow:
            x,y=points[-1]; px,py=points[-2]
            length=math.hypot(x-px,y-py); dx,dy=(x-px)/length,(y-py)/length
            pts=[(x,y),(x-12*dx+5*dy,y-12*dy-5*dx),(x-12*dx-5*dy,y-12*dy+5*dx)]
            self.items.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+f'" fill="{color}"/>')

    def circle(self, x, y, r, fill=PALE, stroke=GREEN):
        self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def node(self, x, y, w, h, title, body='', tone='green', dashed=False):
        fill, stroke = (PALE, GREEN) if tone == 'green' else (WARM, AMBER) if tone == 'amber' else ('#f4f6f4', EDGE)
        self.rect(x,y,w,h,fill,stroke,dashed)
        yy = y+31
        for ln in wrap(title,w-32,21):
            self.text(x+16, yy, ln,21,bold=True); yy += 27
        if body:
            yy += 5
            for ln in wrap(body,w-32,19):
                self.text(x+16,yy,ln,19,color=MUTED); yy += 25
        assert yy <= y+h+8, (self.name,title,yy,y+h)

    def note(self, y, title, body):
        self.rect(36,y,928,86,WARM,AMBER)
        self.text(54,y+29,title,20,bold=True,color=AMBER)
        for i,ln in enumerate(wrap(body,890,18)):
            self.text(54,y+55+i*23,ln,18)

    def save(self):
        self.items.extend(['</g>', '</svg>'])
        svg='\n'.join(self.items)
        (OUT/f'{self.name}.svg').write_text(svg)
        doc=pymupdf.open(stream=svg.encode(),filetype='svg')
        pdf=pymupdf.open(stream=doc.convert_to_pdf(),filetype='pdf')
        pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.8,1.8),alpha=False).save(OUT/f'{self.name}.png')
        records.append(dict(part=self.part,name=self.name,title=self.title,sources=self.sources,limit=self.limit))

# 1. The copy event substitutes a command; the visible output and install attempt diverge.
f=Figure('01-clickfix',1,'One copy action, two command effects','The selected text and the clipboard value are different artifacts.',690,['E02','E15'],'A copy event does not establish terminal execution or installation.')
f.node(36,165,410,112,'Displayed verification step','Candidate selects the page instruction.',tone='neutral')
f.node(554,165,410,112,'Copy handler','Cancels the default copy operation.')
f.line([(446,221),(554,221)])
f.node(554,325,410,127,'Clipboard replacement','R(nonce, phrase, OS) supplies the generated command.')
f.line([(759,277),(759,325)])
f.text(36,333,'The displayed text is bypassed.',20,bold=True)
f.text(36,364,'setData() writes the builder output.',19,color=MUTED)
f.line([(759,452),(759,480),(270,480),(270,518)])
f.line([(759,480),(759,518)])
f.text(500,500,'Requires the candidate to paste and run',17,anchor='middle',color=AMBER)
f.node(36,518,448,110,'Visible verification result','The command prints a VERIFY- result.')
f.node(516,518,448,110,'Installation attempt','Download and execution logic also runs.',tone='amber')
f.note(660,'Observation boundary','The source explains the command design. No victim execution record is shown.')
f.save()

# 2. A two-row execution path shows its permission gates explicitly.
f=Figure('02-vsix',2,'How the editor becomes an interpreter','Windows path reconstructed from task, extension and payload source.',670,['E03','E04','E19'],'Workspace trust, permissions and elevation outcomes were not reproduced.')
for x,t,b,tone in [(36,'Project task','folderOpen selects the extension installation.','neutral'),(360,'Trust and permissions','Execution depends on workspace and task settings.','amber'),(684,'Installed VSIX','Google Update Support activates at startup.','green')]:
    f.node(x,177,280,147,t,b,tone)
f.line([(316,250),(360,250)]);f.line([(640,250),(684,250)])
f.line([(824,324),(824,382)])
f.node(684,382,280,160,'Elevation attempt','PowerShell / COM\nConsent-prompt fallback',tone='amber')
f.node(360,382,280,160,'Signed editor runtime','ELECTRON_RUN_AS_NODE\nwith process.execPath')
f.node(36,382,280,160,'Collection components','JavaScript collection\nPython browser decryption')
f.line([(684,461),(640,461)]);f.line([(360,461),(316,461)])
f.note(600,'Different evidence is needed for each step','An installed extension, an elevated process and recovered credentials are separate outcomes.')
f.save()

# 3. Show syntax recovery and authenticated payload extraction as distinct operations.
f=Figure('03-deobfuscation',3,'From obfuscated syntax to authenticated files','The historical recovery is broader than the companion AST scanner.',700,['E04','E15'],'Parsing is not execution; the companion scanner does not implement full recovery.')
f.node(36,175,280,125,'1 / Parse with Acorn','Recover syntax, call sites, arguments and offsets.')
f.node(360,175,280,125,'2 / Resolve strings','Compare candidate table rotations at resolved calls.')
f.node(684,175,280,125,'3 / Reconstruct key','Keep the order of 16 literal and decoded fragments.')
f.line([(316,237),(360,237)]);f.line([(640,237),(684,237)])
f.circle(110,350,12);f.circle(68,401,10);f.circle(152,401,10)
f.line([(110,362),(68,391)],arrow=False);f.line([(110,362),(152,391)],arrow=False)
f.text(190,374,'Syntax tree',19,color=MUTED)
for i in range(8):
    f.rect(690+i*33,337,24,34,PALE,GREEN)
    f.rect(690+i*33,381,24,34,PALE,GREEN)
f.text(500,360,'Resolve, then preserve order',19,anchor='middle',color=MUTED)
f.node(36,472,280,155,'Encrypted blob','Use the retained blob layout and recovered key.',tone='neutral')
f.node(360,472,280,155,'4 / AES-GCM check','Authentication must validate the recovered plaintext.')
f.node(684,472,280,155,'Three plaintext files','Authenticated files can be inspected without running them.')
f.line([(824,415),(824,444),(176,444),(176,472)])
f.line([(316,534),(360,534)]);f.line([(640,534),(684,534)])
f.note(663,'Tool boundary','The companion AST scanner locates supported syntax patterns; full recovery was a separate analysis.')
f.save()

# 4. Two collection paths, with permissions and encryption retained as gates.
f=Figure('04-collection',4,'A selected file is only the first step','Browser collection and the phase-three file sweep follow different paths.',745,['E04','E17','E18'],'Collection, decryption and completed upload are different claims.')
f.text(36,178,'Browser collection',22,bold=True)
f.node(36,200,280,132,'Browser stores','Copied databases and associated encryption material.',tone='neutral')
f.node(360,200,280,132,'Recovery attempts','Python component, DPAPI and browser elevation services.',tone='amber')
f.node(684,200,280,132,'Usable credentials?','No victim-side decryption result was retained.',tone='amber',dashed=True)
f.line([(316,266),(360,266)]);f.line([(640,266),(684,266)],dash=True)
f.text(36,384,'Phase-three file sweep',22,bold=True)
f.node(36,408,280,133,'Name / extension match','Wallets, keys, configuration, backups and .kdbx files.',tone='neutral')
f.node(360,408,280,133,'Access and budgets','Readable locations only; traversal limits apply.',tone='amber')
f.node(684,408,280,133,'Upload attempts','Chunked transfer and retry routines; delivery unverified.')
f.line([(316,474),(360,474)]);f.line([(640,474),(684,474)])
f.rect(36,580,928,112,'#f4f6f4',EDGE)
f.text(54,611,'Recorded default search limits',20,bold=True)
f.text(54,644,'8 min total   /   2 min per root   /   15 s per directory read',20)
f.text(54,674,'2,500 directories   /   depth 6   /   500 candidate files',20)
f.note(738,'Encryption remains a separate boundary','Selecting an encrypted KeePass database does not establish an unlock or master-password recovery.')
f.save()

# 5. Illustrative frames explain block comparison without inventing observed frames or rates.
f=Figure('05-screen-capture',5,'Why these symbols suggest repeated capture','Illustrative blocks explain the design; they are not recovered display frames.',700,['E05','E17'],'No victim session, achieved frame rate or bandwidth was measured.')
for x,label,current in [(36,'Previous frame',False),(362,'Current frame',True)]:
    f.text(x,185,label,22,bold=True)
    for row in range(3):
        for col in range(4):
            changed=(row,col) in {(0,2),(1,2),(2,3)}
            fill=WARM if changed and current else PALE
            f.rect(x+col*68,209+row*60,60,52,fill,AMBER if changed and current else EDGE)
f.line([(308,293),(350,293)])
f.node(688,209,276,172,'Compare blocks','copyPrev\nblockChanged\nencodeBlocks')
f.line([(634,293),(688,293)])
f.text(36,425,'Amber cells illustrate changed regions. Grid size is schematic.',19,color=MUTED)
f.node(36,472,280,132,'Capture repeatedly','CaptureDisplay\nCaptureAndSend\nLoop / frameFPS')
f.node(360,472,280,132,'Encode','encodeJPEG\nChanged-block encoding')
f.node(684,472,280,132,'Windows bundle','node-screenshots\njpeg-js / MessagePack / ws',tone='neutral')
f.line([(316,538),(360,538)])
f.text(684,641,'Independent component evidence',17,color=MUTED)
f.note(688,'What remains unmeasured','Display access, permissions, successful capture and transport require execution evidence.')
f.save()

# 6. Show the referenced config.json history and the separate, unreferenced file.
f=Figure('05-resolver',6,'Referenced resolver file and separate config history','The payload references config.json. Dates describe file history, not observed client connections.',630,['E07','E20','E21'],'No retained payload references config-alt.json; endpoint records do not confirm a fetch of config.json.')
f.text(36,185,'REFERENCED CLIENT FILE: CONFIG.JSON',19,bold=True,color=GREEN)
f.line([(60,226),(940,226)],arrow=False)
f.circle(95,226,9);f.circle(850,226,9)
f.node(36,266,430,154,'26 May 2026','Final listed set:\napi.domatisc[.]ink\napi.coslyintra[.]online')
f.node(534,266,430,154,'13 July 2026','Changed set:\napi.cklomino[.]ink\napi.dsfmot[.]xyz')
f.text(36,476,'SEPARATE FILE: CONFIG-ALT.JSON',19,bold=True,color=GREEN)
f.line([(60,511),(940,511)],arrow=False)
f.circle(410,511,9)
f.node(200,546,600,110,'1 June 2026','api.onoplainai[.]ink   /   api.migadyn[.]info')
f.text(36,708,'No retained payload references config-alt.json.',19,color=MUTED)
f.save()

# 7. Address totals are measured; the repository overlap illustration is explicitly qualitative.
f=Figure('07-targeting',7,'Two pools, two different counting problems','Recorded aggregate queries across the safe and antispam SQLite pools.',780,['E08','E09'],'Rows count stored address strings, not people, delivered mail or infections.')
f.text(36,183,'Stored address strings: exact overlap = 0',23,bold=True)
f.node(36,210,400,124,'Safe pool','79,698 rows')
f.text(500,285,'+',35,anchor='middle',color=GREEN)
f.node(564,210,400,124,'Antispam pool','62,667 rows')
f.line([(236,334),(236,368),(500,368),(500,390)])
f.line([(764,334),(764,368),(500,368)],arrow=False)
f.node(226,390,548,94,'UNION: 142,365 address strings','No additional person-level identity resolution.')
f.text(36,540,'Repository values: sets overlap',23,bold=True)
f.text(56,603,'Safe-pool count: 20,880',20)
f.text(56,637,'Combined UNION: 27,698',22,bold=True,color=GREEN)
f.text(56,678,'Adding per-pool counts overcounts.',19)
f.circle(714,631,76,fill='none')
f.circle(818,631,76,fill='none')
f.text(683,638,'safe',18,anchor='middle')
f.text(842,638,'antispam',18,anchor='middle')
f.text(767,738,'Schematic overlap; areas are not scaled.',16,anchor='middle',color=MUTED)
f.note(785,'Impact boundary','Stored target data establishes neither delivered-message volume nor successful compromise.')
f.save()

# 8. Client recovery is visibly separated from unobserved service behavior.
f=Figure('06-administration',8,'What the recovered client makes visible','Seventy frontend modules expose interface intent and API references.',700,['E06','E08','E09'],'The backend, authenticated records and completed wallet transfers were not recovered.')
f.rect(36,172,588,470,PALE,GREEN)
f.text(56,211,'Recovered rms-platform frontend',24,bold=True)
for yy,t,b in [(238,'Mail and task views','Metrics, templates, auto-reply, task board'),(363,'Repository availability','clone_url and refresh controls'),(488,'Wallet interfaces','Import, preview, refresh and claim actions')]:
    f.node(58,yy,544,105,t,b,tone='neutral')
f.line([(656,172),(656,642)],color=AMBER,arrow=False,dash=True)
f.text(680,206,'Recovery boundary',20,bold=True,color=AMBER)
f.node(690,255,274,147,'Backend API','Implementation and populated records unobserved.',tone='amber',dashed=True)
f.node(690,458,274,147,'Execution outcomes','No demonstrated server authorization or wallet transfer.',tone='amber',dashed=True)
f.line([(624,541),(690,541)],dash=True)
f.note(691,'A client action is a request design','Route names and buttons show intended operations. Service-side records are needed to establish outcomes.')
f.save()

# 9. Vertical time order leaves room for hashes and actual changes.
f=Figure('07-echoes',9,'Four retained ECHOES archive revisions','March 2026 repository history, ordered by the recorded UTC timestamps.',730,['E11','E14','E16'],'Final PowerShell payloads were unavailable; the retained history establishes staging lineage.')
f.line([(265,184),(265,668)],arrow=False)
events=[('5 March','06:17 UTC','03f1795d','Earliest retained retrieval configuration; DDD task tag.'),('17 March','05:14 UTC','ded13153','Different account / repository destination; DDD retained.'),('25 March','03:54 UTC','b209f365','Another destination; task tag changes to WORD.'),('25 March','13:29 UTC','4b6ea6b2','Further destination change; VBS persistence layer added.')]
for i,(date,time,rev,body) in enumerate(events):
    yy=177+i*134
    f.text(36,yy+32,date,23,bold=True);f.text(36,yy+62,time,19,color=MUTED)
    f.circle(265,yy+40,10)
    f.node(310,yy,654,110,rev,body)
f.note(742,'The lineage stops at the retained staging','A shared relationship cannot supply the implementation or capabilities of a missing final payload.')
f.save()

# 10. Explicitly labeled relationships, not an implied compromise chain.
f=Figure('10-evidence-map',10,'Connections need named relationships','Read each row as an evidence pivot, not as an observed execution sequence.',830,['E01','E02','E03','E07','E08','E06','E11'],'Different edge labels support different claims; end-to-end execution was not established.')
rows=[('Received messages','link to','Recruitment lures'),('Lure copy handler','calls','Command builder'),('Project task / settings','configure','Extension deployment'),('Held collector','references','GitLab configuration'),('Sender configuration','names','Two targeting pools'),('Recovered frontend','defines','Mail / wallet actions'),('Archive history','preserves','ECHOES revisions')]
for i,(left,edge,right) in enumerate(rows):
    yy=173+i*91
    f.node(36,yy,324,65,left,tone='neutral')
    f.line([(369,yy+45),(626,yy+45)])
    f.text(498,yy+29,edge,18,color=GREEN,anchor='middle')
    f.node(640,yy,324,65,right)
f.note(841,'What these edges do not establish','Infection, one integrated backend, successful transfers and operator identity require additional evidence.')
f.save()

# 11. A conjunction diagram and two bounded corpus checks make the selector boundary visible.
f=Figure('11-detection-logic',11,'A YARA match requires the full conjunction','Every gate is necessary; matching bytes still need acquisition context.',835,['E15'],'The software baseline is small; an ELF header does not prove code reachability or execution.')
for i,(title,body) in enumerate([('ELF format and size','ELF magic at byte zero; under 64 MiB'),('Framework marker','overlord-client/cmd/agent'),('Environment marker','OVERLORD_SERVER_RAW'),('Wallet context','At least 2 of 3 wallet markers')]):
    yy=172+i*105
    f.node(36,yy,565,87,title,body)
    f.line([(601,yy+43),(675,yy+43),(675,367)],arrow=False)
f.circle(752,367,48)
f.text(752,375,'AND',24,bold=True,anchor='middle',color=GREEN)
f.line([(675,367),(704,367)])
f.line([(800,367),(853,367),(853,476)])
f.node(692,476,272,120,'Content match','A match is not proof of execution.',tone='amber')
f.text(36,638,'Replay results',23,bold=True)
f.node(36,665,446,143,'Retained case artifacts','33 named rules matched artifacts.\n90/192 inputs hit; 395 raw/member views.',tone='neutral')
f.node(518,665,446,143,'Local software baseline','Zero hits across 2,379 views of 1,914 files (59.2 MB).\nSmall and not independently curated.',tone='neutral')
f.note(843,'False-positive boundary','Plain prose now misses; a marker-rich ELF can still match.')
f.save()

# 12. Separate positive sample evidence from an unpinned upstream comparison.
f=Figure('12-framework-boundary',12,'Framework lineage and collection evidence','A positive observation in a held sample is stronger than an unpinned absence claim.',690,['E05','E17','E18'],'The upstream files were not preserved as a pinned baseline; authorship remains unresolved.')
f.node(36,178,446,250,'Recorded framework lineage','overlord-client module path\nWebAssembly plugin runtime\nGeneric control and transport\n\nThese markers alone do not identify the campaign.',tone='neutral')
f.node(518,178,446,250,'Positive sample evidence','SQLite-related dependencies\nBrowser-store names\nWallet-related markers\nCapture-related symbols\n\nRetained artifacts remain inspectable.')
f.line([(259,428),(259,482)],dash=True)
f.node(36,482,446,147,'Historical upstream comparison','Selected files were examined, but no pinned snapshot was retained.',tone='amber',dashed=True)
f.line([(741,428),(741,482)])
f.node(518,482,446,147,'Supported conclusion','Framework-derived agent with collection-related implementation.')
f.note(695,'Claims the comparison cannot settle','Who wrote each addition, whether every upstream variant lacks it, or whether a victim-side action succeeded.')
f.save()

(OUT/'diagrams.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'Built {len(records)} explanatory diagrams as SVG and PNG.')
