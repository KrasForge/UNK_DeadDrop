# Twelve-part edition, 25 October 2026

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

## Rendered edition, 25 October 2026

Rendered all twelve Markdown sources with the public
[claude-blog](https://github.com/AgriciDaniel/claude-blog) renderer at commit
`3544423`. Each article has HTML and PDF output, a local hero, and four preview
screenshots. The repository's Gate 3 visual verification passed for all twelve
articles at mobile, tablet, desktop and dark-mode sizes. Screenshots and outputs
are under `rendered/2026-10-25/`; [the edition index](rendered/2026-10-25/index.html)
links the articles.

The full five-gate delivery contract was not run. In particular, the required
independent `blog-reviewer` agent was unavailable in this runtime, so these
renders are not marked as contract-approved for publication. Existing
example.com canonical URLs remain placeholders.

Added three full articles: investigation connections (Part 10), detection engineering
(Part 11), and the framework/collection boundary (Part 12). The series index,
previous/next links and package now cover twelve articles. Part 9 no longer claims
to end the series. New prose uses retained evidence and makes the missing historical
upstream snapshot explicit; no fresh upstream comparison is represented as completed.

Checks for this edition:

- Twelve sequentially numbered Markdown articles; 45 distinct local link targets resolve.
- Six existing figures remain linked; new articles use evidence comparison tables.
- Three existing JavaScript snippets parse, and the inert Acorn demonstration passes.
- Eight companion AST tests rerun successfully.
- Four original detection tests plus three new inert boundary tests pass (seven total).
- Boundary tests demonstrate a harmless-text YARA match, task-marker substring
  matching and case folding in the local Sigma fixture evaluator. Rules are unchanged.
- Official YARA, Sigma modifier and Go build-setting references were consulted for
  technical semantics. References are linked beside the relevant article statements.
- The ZIP includes only the articles and explicitly selected supporting files,
  including the small detection test/rule bundle with pinned requirements and MIT license.
- ZIP member hashes are checked by the package builder. The extracted detection tests
  were rerun successfully from the bundle, independently of the source workspace layout.

Historical sample scans are reported as historical; no malware execution, service
installation, scheduled-task registration or production SIEM validation was performed.
Existing HTML/PDF previews are still the historical seven-part edition and are not
updated previews of these twelve Markdown articles.

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
