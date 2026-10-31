# Sentence-rhythm pass, 31 October 2026

Varied sentence length in the body text without changing word choice: adjacent sentences
were joined or split using punctuation and a fixed list of connectives only. A checker
confirmed that the sequence of content words is unchanged and that headings, code, tables,
figures, captions, lists, links and the References section are byte-identical; no em
dashes. The coefficient of variation of sentence length rose from 0.521 to 0.682. Joins flagged as
uncertain were reviewed by hand for claim, citation and qualification attachment.

This PDF is published on the project site but differs in wording, not content, from the
Zenodo deposit (version DOI 10.5281/zenodo.23823716, SHA-256 `5c1dbf32898275bc48e7191f8a2d49501539c6a1b049aca574838c9aec7a4553`), which is unchanged.

PDF: 17 A4 pages, 147,395 bytes, SHA-256 `372f4efa2ce86335cde24bc007a51c0040f0ab861cdd68308ca73f1148e77efc`.

# Stop Slop editorial pass: 30 October 2026

Replaced document-centered framing in the introduction and design overview with the research question, analysis path and baseline-versus-revision distinction. Evaluation numbers and caveats remain unchanged. Rebuilt with ReportLab 5.0.1: 17 A4 pages, 146,451 bytes. SHA-256: `e0d2555ad8ed55de7c45ca796ae88960c1940ab3d35f2637411646a7c19c8dcb`.

# Decoder-coverage revision: 30 October 2026

Section 5.7 now reports a revised engine (source hash prefix `ba4d1468`) that closes the two
decoder-recognition gaps the experiment found. One is the self-replacing decoder of
javascript-obfuscator 4.x and earlier; the other is wrappers that declare offset locals before
returning. Added to Section 5.7:
- results for the revised engine on the 7,200 samples;
- a held-out set generated after the fixes were written: 20 new inputs, 72 configurations,
  releases 5.9.0, 5.0.0, 4.2.2, 4.1.1 and 3.2.7, for 7,200 samples;
- a rerun of every corpus, compared with the hardened engine;
- a review of the newly decoded Tier 2 strings.
The alignment reference gained class field names after the held-out set exposed the gap; all
engines were rerun with it. The abstract, §3 introduction, §4 (69 tests), related work and
conclusion are updated. Engine change, experiment and corpus records are in companion PR #11.
All runs were on the netcup server; nothing was executed and no remote resource was fetched
during the package reviews.

Validation: 17 A4 pages; final build with no drafting markers or em dashes; §5.7 pages
rasterised and inspected.

PDF SHA-256: `8951f63cc5b0d288f629dd8a7fcb0f0de85c208204191f1cdb8f7bed71616877`.
PDF size: 147,867 bytes.

# Expansion: 30 October 2026

The paper adds a controlled string-array recovery experiment (Section 5.7) and expands the
design, implementation and case study.

- **§3 introduction:** opens with Figure 1, a pipeline diagram with the isolation boundary,
  drawn by `build.py`, and states that §3 describes the evaluated engine.
- **§3.3:** gains Algorithm 1, the conditions under which it reproduces the obfuscated
  program's rotation, its cost, and a worked example. The example is a three-line program
  obfuscated by javascript-obfuscator 5.9.0, seed 19. Its rotation (10) was confirmed by the
  scanner and by an independent Python reimplementation of the checksum; every other rotation
  yields NaN.
- **§4:** gains the module and rule structure, the iterative walks, the memory figure,
  the report contents and the test matrix.
- **§6:** gains a table of the 14 retained artifacts.

Section 5.7 setup, all run on the netcup server:
- 50 benign calibration files, obfuscated under 72 string-array configurations by
  javascript-obfuscator 5.9.0 and 4.1.1, giving 7,200 samples.
- Both scanner engines scored on all samples. webcrack 2.16.0, synchrony 2.4.6 and
  obfuscator-io-deobfuscator 1.0.6 scored on a stratified subset of 1,440 samples.
- Scoring is uniform across tools, with a site-order check for the scanner. That check was
  validated against simulated rotation errors: 0 of 5,402 correct sites flagged, 4,240 of
  4,903 shifted sites flagged.
- During development, the harness was corrected twice before the final run, because its
  ground truth missed ordinary string arrays and then template text and method names. Both
  times, apparent scanner errors were scoring artifacts. No scanner code was changed for
  this experiment.
- Records are in `../unk-scanner/benchmark/rotation/`.

Abstract, introduction, §5 introduction, related work, conclusion and artifact availability
cross-reference the experiment.

Validation: 16 A4 pages; final build with no drafting markers; no em dashes; pages with
Figure 1, Algorithm 1, the worked example, §5.7 and the artifact table were rasterised and
inspected.

PDF SHA-256: `e14ccca1802f54d9a764d14f3d2fae16f27cf774d76f6dd0d5bfb0799f768257`.
PDF size: 144,758 bytes.

# Hardening revision: 29 October 2026

Added Section 5.6, *Hardening after the evaluation*, and one-sentence cross-references in
the abstract, Sections 3.3, 5.4 and 7, and the conclusion. Sections 5.1 to 5.5 are
unchanged and still describe the frozen engine (source SHA-256 prefix `caf3f552`).
Section 5.6 reports the hardened engine (prefix `202f56f2`), run on the same server:
bypass fixtures through the isolated CLI, the 14 retained artifacts, and the calibration,
Tier 1, Tier 2 and Tier 3 corpora in process with seven workers, diffed file by file
against the frozen results (`../unk-scanner/benchmark/mitigation/`). The throughput comparison
reran the calibration corpus with four workers and validation, as in Section 5.5. Newly
decoded Tier 2 strings were screened, and the two packages that newly revealed a
`child_process` import were read statically in a deobfuscated view; nothing was executed and
no remote resource was fetched. `build.py` gives five-column tables their own widths.

Validation: 12 A4 pages; no em dashes or drafting markers; the Section 5.6 page was
rasterised and inspected.

PDF SHA-256: `9543a8b4212e55e4771342be375e6e9b199e2975ffc32e8a67864c2cf9b6b68d`.

# Narrative structure revision: 29 October 2026

Removed the numbered research-question framework. Evaluation headings now name
the results directly, and the investigation's scope is part of its introduction.
Converted the scanner's labelled recovery bullets to connected prose. Findings,
counts and citations are unchanged. Rebuilt PDF: 11 pages. Extracted text
contains no RQ labels or em dashes. The preprint upload copy is synchronized.

PDF SHA-256: `a601d8f31fc26f145ce13ff14b4682987b6413a6b035a854c7a4b50409a6f891`.
PDF size: 124,527 bytes.

# Editorial revision: 29 October 2026

Rebuilt from revised Markdown with ReportLab 5.0.1. Rewrote the abstract,
introduction and conclusion; reduced repeated metacommentary; retained the
limitations that affect interpretation. Existing references and artifact hashes
are preserved. No new evidence acquisition, benchmark execution or online
publication was performed.

Tier 1 informed one rule adjustment, so the final scan is no longer described
as an untouched held-out estimate. Expected outputs for 14 artifacts are distinguished
from detections. Rotation recovery and throughput claims reflect the documented
bypass and single-run comparison. Benchmark counts are unchanged. Removed a
leftover drafting instruction and unsupported claims of guaranteed recovery.

Validation: 11 A4 pages; searchable text; no em dashes or unresolved drafting
markers; no text spans outside the checked page margins. Opening pages and selected
body/table pages were rasterised and inspected. Cited R identifiers resolve to
preserved bibliography entries. This was a local citation-consistency check, not a
new external link, retraction or source-archive audit.

PDF SHA-256: `68428af4216138b6a90c6fa1db848db31b732bcc6c0a2f812ef7a5ef1b895292`.
PDF size: 124,668 bytes.


## Direct-prose and worked-example revision: 30 October 2026

Revised the abstract, method explanation, evaluation and conclusions. Removed the duplicated recovery-scoring explanation while retaining the 25-sample validation and 4,240/4,903 deliberately shifted call-site result. Preserved all benchmark numbers, hashes and reference identifiers.

Restored W(), f(), and the rotation loop as readable code blocks, with the original input in a separate block. Synchronized examples/rotation-example.md. Syntax-checked the original and generated examples without executing them. An independent Python calculation found rotation 10 as the only checksum match (717,217), verified NaN at rotations 0 through 9, and checked all four application strings.

Rebuilt the 17-page PDF. Visually inspected the complete example page; code fits within the page boundaries. PDF text contains no em dashes. No benchmark or malware execution was repeated, and no online publication occurred.


## Zenodo deposit preparation: 31 October 2026

Updated the cover date to match this prepared preprint and rebuilt the 17-page PDF with ReportLab 5.0.1. The deposited file is searchable and carries no draft banner. SHA-256: `5c1dbf32898275bc48e7191f8a2d49501539c6a1b049aca574838c9aec7a4553`; MD5: `05ba6fa124c3903ab8f1fd482142b9e1`; size: 147,363 bytes. The GitHub Pages download was refreshed in deployment [41142625153](https://github.com/KrasForge/UNK_DeadDrop/actions/runs/41142625153); its file checksum now matches Zenodo.

Created `zenodo-metadata.json` and `ZENODO-RECORD.md` with a separate preprint record, CC BY 4.0, ORCID, bibliography, campaign-paper DOI and exact evaluated companion commit. At publication, software archive v2.1.0 predated that commit, so the paper record linked to the exact source commit. Companion archive [v2.2.0](https://doi.org/10.5281/zenodo.23825573) now contains the evaluated scanner source; the exact commit remains the evaluation reference. Zenodo published record [10.5281/zenodo.23823716](https://doi.org/10.5281/zenodo.23823716), concept DOI [10.5281/zenodo.23823715](https://doi.org/10.5281/zenodo.23823715). The public API reports the expected open CC BY 4.0 record and matching file checksum.
