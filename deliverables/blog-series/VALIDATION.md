# Sentence-rhythm pass, 30 October 2026

Varied sentence length across all fourteen articles without changing word choice: adjacent
sentences were joined into longer ones and others split into short ones, using only
punctuation, paragraph breaks and a fixed list of connectives (and, but, which, while and
similar). A checker confirmed for every article that the sequence of content words is
unchanged, that front matter, headings, code, tables, captions and link targets are
byte-identical, and that no em dashes were introduced. The coefficient of variation of prose
sentence length rose from 0.31-0.49 to 0.65-0.76 per article. Long joins and new short
sentences were reviewed by hand; one 59-word join in Part 6 was split again.

# Stop Slop editorial pass, 30 October 2026

Reviewed all fourteen current article sources using the [Stop Slop writing checks](https://github.com/hardikpandya/stop-slop). Replaced several document-centered phrases with direct descriptions of the analysis, tightened wording in Parts 1, 3 and 6, and retained attribution, dates and limits on what artifacts establish. The descriptive article titles and revised section headings remain in place.

Packaged the 14-post archive with the updated sources and validation record. The local Astro production build completed with Node.js 22.23.4. Its downloadable preprint and scanner PDFs match the rebuilt manuscript files byte for byte. The existing non-blocking Starlight warning for the `/404` content entry remains.

# Controlled recovery test, 30 October 2026

Part 14 gains a section, *Comparing decoded strings with their originals*, summarising Section 5.7 of the rebuilt
scanner paper. It covers the 7,200-sample controlled experiment, the two decoder fixes and the
held-out check across five obfuscator releases, and the rise in Tier 3 detection from 64 to 128
samples, all at warning level. Figures come from companion PRs #10 and #11. `verify.py` passes.

## Voice revision, 30 October 2026

Reworked Parts 13 and 14 after reviewing their cadence. Replaced the mirrored
section pattern and recurring lesson summaries with a concrete account of the
reviewed false positives and the `splice` rotation defect. Added two small SVG
diagrams tied directly to those results. Revised the section headings across all
fourteen articles to name the artifacts, code paths, and results each article
examines. Restored the more descriptive main titles in the articles,
landing page, sidebar and archive index while retaining the revised section
headings. Split dense passages across Parts 1 to 4, 6 to 7, 10 to 11,
and 13 to 14 at changes in evidence or argument, and clarified the indicator
reference. Converted the repository paths and email steps in Part 2 into lists.
Updated the landing page, sidebar, and downloadable archive to match. The Astro
build and archive checks passed locally; Pages status is recorded in the
repository Actions history.

# Scanner hardening update, 29 October 2026

Part 14 now describes the hardened scanner engine in a new section, *Closing the variants,
and what that does not prove*. It replaces the paragraph that proposed untested mitigations.
Parts 3, 11 and 13 and the series index gain one cross-reference each. The figures come from
Section 5.6 of the rebuilt scanner paper and `benchmark/mitigation/` in the companion
repository (merged as PR #9): 18 of 19 variants handled, no new error-level finding on the
calibration corpus or Tiers 1 to 3, new warnings in three benign packages, unresolved Tier 2
arrays down from 1,387 to 16, artifacts 14 of 14, and throughput of 281 against 264 files/s.
The site carries the rebuilt scanner PDF.

# Fourteen-article edition, 29 October 2026

Added Part 13 on the expanded scanner evaluation and Part 14 on recovery defects
and single-change bypass fixtures. Both draw on the completed scanner manuscript
and retained evaluation results. They preserve the distinction between calibration,
Tier 1 feedback, the registry changes window and the public malware dataset.

Updated Parts 3 and 11 to remove obsolete parser and benchmark claims and separate
YARA validation from scanner results. Expanded Part 6 with certificate and registration
context and the missing raw-scan evidence. Expanded Part 9 with delivery-repository
relationships and corrected the C2PA verification qualification against E14.
No new historical collection, sample execution or external publication was performed.

Updated the series index, sidebar, research-materials page and source archive.
The site now includes the revised scanner PDF as well as the revised investigation
PDF. Added link rewriting for the scanner PDF and the indicator/artifact references.

Validation: all 14 article sources pass `verify.py`, including local source links,
frontmatter, sensitive-string checks, absence of em dashes and JavaScript syntax.
The inert Acorn example still returns its expected output. The production Astro
build passed using the installed Node.js 22.23.4 runtime; the default 22.22.2 runtime
was below Astro's required version. Checked 862 local rendered-page links with no
missing targets, canonical URLs for both new articles, and byte equality of the
paper downloads. The ZIP integrity and all packaged checksums pass. The source
archive includes both new articles and their linked scanner paper.

Build output: `site/dist/`. This update has not been deployed. Older standalone
HTML/PDF previews under `rendered/` remain historical and were not regenerated.

# Twelve-part edition, 26 October 2026

## Evidence-source expansion, 28 October 2026

Expanded the historical indicator reference with additional captured lure hosts,
mail and certificate names, administration routes, dated IP observations,
repository copies and source-labeled weak pivots. Added a separate artifact
reference with exact hashes for selected payloads, URLScan response bodies, the
ECHOES archive branch and exact repository-file variants. Added contextual
evidence-PDF links across the related articles and updated the Markdown series
archive and its hosted-download copy. The source pages and ZIP are updated; the
Astro site was not rebuilt or deployed, and the older standalone previews were
not regenerated in this step.

## Indicator reference update, 28 October 2026

Added an unnumbered historical-indicator reference covering retained lure bundles,
route strings, both resolver generations, repository URLs, dated IP associations,
passive-DNS leads and domains listed by Proofpoint. Parts 1, 2, 6, 8, 9 and 10 now point
readers to the relevant indicators. The reference defangs URLs and separates direct
sample content from scan-based or externally reported associations. Shared provider
addresses, victim forks, personal email addresses, analyst network addresses and
credentials are excluded. The late July droppers' SHA-256 values were checked against
the retained files. The Astro site was not rebuilt and the edits have not been deployed.

## Preprint alignment update, 27 October 2026

Updated Parts 3 and 11 to separate the public companion scanner and YARA
snapshot from the later local scanner package and YARA noise review. Part 11
reports the 177-input/380-view review and the 31-input scanner evaluation with
their limited scope. Added the current Zenodo DOI to the relevant pages,
series index and research-materials page. Regenerated the standalone HTML/PDF
for Parts 3 and 11, refreshed the full-edition index, and replaced its preprint
PDF with the deposited file. GitHub Pages run 40539680516 succeeded; live
Parts 3 and 11, Research Materials, and the downloadable PDF were checked. The
PDF checksum matches Zenodo. The historical artifact cutoff remains 24 July 2026.

The 12 Markdown articles now use their GitHub Pages canonical URLs and each
ends with a direct link to the companion repository. The landing page links the
Zenodo preprint record and companion repository. No technical claims changed in
this publication-metadata update.

## Prose revision, 26 October 2026

Reviewed all twelve posts for editorial metacommentary. Removed repeated takeaway
boxes, narration about correcting earlier drafts, instructions about how claims
should be presented, and repeated conclusions. Parts 5, 10 and 12 were restructured
around their technical findings. Limitations affecting interpretation remain next
to the relevant artifacts, including the missing ECHOES payload, absent runtime
and backend observations, and unavailable pinned upstream source files.

Compared all fenced code and evidence blocks with the previous sources: unchanged.
Checked all twelve source files for valid local links, canonical URLs, companion
links, balanced fences, absence of em dashes and absence of the removed FAQ and
article-details sections. All checks passed.

Rendered all twelve standalone HTML/PDF articles with the claude-blog
`blog_render.py` renderer, using WeasyPrint. Each HTML source hash matches its
rendered Markdown copy, and the PDFs were produced successfully. The current
edition includes the latest Part 2 and Part 11 scope and rule references. The
earlier rendered edition used the first deposited preprint.

The Astro production build passed with Node.js 24. All twelve generated article
bodies contain their diagrams and exclude em dashes and the removed sections.

## Detection coverage revision, 26 October 2026

Updated Parts 2 and 11 to link only to retained, artifact-tested detections.
The companion now contains 33 named YARA rules in 28 files. A read-only replay
covered 192 selected files and 395 raw or archive-member views; every rule
matched retained case material. A separate scan of 1,914 local software files
and 2,379 views had no hits. Five RAR containers were not decoded. Sigma event
rules were removed because authentic endpoint logs were unavailable, and
workspace-file rules were removed because the original `.vscode` targets were
not retained. The wallet rule's earlier prose collision was fixed by requiring
ELF magic at byte zero; the marker-rich prose boundary fixture now stays
negative. The small baseline does not establish production false-positive
rates.
No samples were executed or uploaded.
The Astro Pages build also passed with Node.js 22.23.4 after syncing the current
companion source and article Markdown.

## Current standalone render, 26 October 2026

The initial twelve-page edition was rendered with the public
[claude-blog](https://github.com/AgriciDaniel/claude-blog) renderer at commit
`3544423`. After the detection-scope revision, Parts 2 and 11 were regenerated
from current Markdown using the existing claude-blog HTML/CSS template, Python
Markdown and WeasyPrint. Their source hashes, descriptions, dates and word counts
were updated; Part 11's diagram now shows the artifact replay and local baseline.
The other ten pages are unchanged. The previously deposited Zenodo PDF and
linked public evidence reports are included; the unsubmitted local preprint draft
is excluded. The edition is under `rendered/2026-10-26/`.

The full five-gate delivery contract and new viewport screenshots were not run.
These refreshed formats are not marked as contract-approved. The 25 October
folder retains its earlier screenshots and historical render.

## Previous standalone render, 25 October 2026

Editorial update: Parts 1–12 received a series-wide prose and structure pass,
including clearer openings, shorter paragraphs, stronger section progression,
and transitions between artifacts and their evidentiary limits. The current
heading hierarchy uses four to six main sections per article, with related
technical details nested as smaller subheadings. Part 2's title now identifies
the signed editor runtime precisely.
Part 10 incorporates public reporting through 25 October and frames novelty as
case-specific technical detail rather than a first-ever claim. New sources and
their independence limits are linked in the article and index. The case evidence
cutoff remains 24 July 2026.

## Historical rendered edition, 25 October 2026

Rendered all twelve Markdown sources with the public
[claude-blog](https://github.com/AgriciDaniel/claude-blog) renderer at commit
`3544423`. Each article has HTML and PDF output, a local hero, and four preview
screenshots. The repository's Gate 3 visual verification passed for all twelve
articles at mobile, tablet, desktop and dark-mode sizes. Screenshots and outputs
are under `rendered/2026-10-25/`; [the edition index](rendered/2026-10-25/index.html)
links the articles.

The full five-gate delivery contract was not run. In particular, the required
independent `blog-reviewer` agent was unavailable in this runtime, so these
renders are not marked as contract-approved for publication. That edition's
canonical URLs used example.com placeholders; the 26 October render now uses
the GitHub Pages article URLs.

Added three full articles: investigation connections (Part 10), detection engineering
(Part 11), and the framework/collection boundary (Part 12). The series index,
previous/next links and package now cover twelve articles. Part 9 no longer claims
to end the series. New prose uses retained evidence and makes the missing historical
upstream snapshot explicit; no fresh upstream comparison is represented as completed.

Checks for this edition:

- Twelve sequentially numbered Markdown articles; 23 local link targets resolve.
- All twelve articles render with their current diagrams and selected evidence links.
- Three existing JavaScript snippets parse, and the inert Acorn demonstration passes.
- Eight companion AST scanner tests and six Python detection/boundary tests pass.
- The read-only actual-artifact replay produced hits for all 33 YARA rules. The
  small baseline scan produced no hits; neither result estimates production
  precision or recall.
- The inert boundaries reject prose collisions and partial-marker cases. No
  Sigma rules or synthetic event records are published as detections.
- Official YARA and Go build-setting references were consulted for technical
  semantics. References are linked beside the relevant article statements.
- The ZIP includes the Markdown articles, diagrams, preprint, selected
  edited evidence reports and checksums. Current detection rules live in the
  companion repository.
- ZIP member hashes are checked by the package builder.

Historical sample scans are reported as historical; no malware execution, service
installation, scheduled-task registration or production SIEM validation was performed.
Earlier render folders are superseded previews. The current HTML/PDF edition is
the twelve-part `rendered/2026-10-26/` set.

## Previous split validation

# Nine-part split, 25 October 2026

The numbered Markdown sources now contain nine articles. Former Part 4 was split
into collection and screen-capture articles; former Part 6 into targeting and
administration articles. Each has its own opening, takeaways, conclusion, FAQ,
evidence links and navigation. Existing technical claims and qualifications were
retained; no new sample execution or network investigation was performed.

The harvesting article explicitly separates normalization in the harvester from
stored-value comparisons during verification. The capture FAQ states that
keylogging was not established, rather than claiming its absence.

The current ZIP contains the nine-part Markdown edition and linked supporting
files. Historical seven-part rendered previews and their review scores remain
under `rendered/` and do not validate this new edition. They are excluded from
the ZIP. The verifier no longer imposes the old word-count floor on split posts.

Current checks passed: nine sequentially numbered posts, 33 local link targets,
six referenced figures, three parsed JavaScript examples, and the inert Acorn
demonstration. The rebuilt ZIP passed member-integrity and SHA-256 checks.

## Historical validation record (seven-part edition)

### Blog-series validation, 24 October 2026

Seven complete articles, approximately 1,550–1,850 words of prose each before code,
evidence links and method notes. Total prose under that counting method: 11,385 words.

The posts were revised with the claude-blog rewrite skill on 24 October 2026. Its
format, visual and link gates (1, 2, 3 and 5) pass for all seven rendered drafts.
Its blocking review gate (4) does not: final reviewer scores were 76–84 against a
90 threshold, with no P0 issues; the author kept long sentences and the original
titles, which the rubric marks down. Both review rounds are kept in
`rendered/<slug>/reviews/`.

## Editorial review

The five public references listed in the series index were opened and read for
structure and pacing. The articles were then rewritten around the case's own
findings: direct openings, artifact-led investigation, code/configuration details,
short technical sections and focused implications. They do not copy the external
authors' prose or import their personal experiences into this investigation.

The articles preserve distinctions between static capability and execution,
frontend design and backend operation, targeting rows and victim counts, recorded
configuration changes and client behavior, and metadata timestamps and actual
creation/compilation time. The first-person account is limited to the documented
investigation and analytical choices. No anecdote of compromise was invented.

## Checks completed

- All seven posts exist and have balanced Markdown code fences.
- All 31 distinct local article-link targets resolve; all six referenced PNGs exist.
- Three JavaScript examples parse with the locally installed Acorn dependency.
- Only the invented Acorn demonstration was executed. It printed the documented
  `FunctionDeclaration CallExpression` result while treating its example wrapper
  as an inert source string. The lure handler and file selector were not executed.
- The JSON manifest excerpt parses successfully.
- The two pool counts sum to 142,365. Database queries were not rerun.
- Targeted text checks found no local investigation paths, email addresses,
  GitHub token prefixes or API-key URL parameters in the articles.
- All six original analytical diagrams were visually reviewed. They are labeled
  as reconstructions, not victim telemetry or original interface screenshots.
- The download archive is allowlisted and its member checksums are verified.
  Raw samples, databases, credentials and private reports are not packaged.

These checks do not independently reproduce the historical decryption, image
signature validation, collection outcomes or companion detection tests. The
source reports state the status of those results. No historical infrastructure
was contacted, no recovered credential was used and no publication occurred.

## Rebuild

`python deliverables/blog-series/verify.py` checks text, local references and the
inert code examples; it uses the companion's installed Acorn package.

`python deliverables/blog-series/build_assets.py` rebuilds the diagrams using
ReportLab and PyMuPDF. `python deliverables/blog-series/package.py` rebuilds and
checks the download archive.

## Direct-prose review: 30 October 2026

Edited all fourteen current article sources. Reduced repetitive limitations and decorative transitions, varied sentence structure, and used first-person descriptions for documented analysis. Kept main titles, code snippets, hashes, citations and evidence boundaries intact. Historical rendered editions were left as archives.

verify.py passed for all fourteen posts: fourteen linked figures, 47 local link targets, three parsed JavaScript snippets and the inert Acorn demonstration. No prohibited negative-clause phrases or em dashes remain in the active article prose. The source ZIP and local Astro site were rebuilt from these sources and the current PDFs. This revision is local; it does not record a new deployment.
