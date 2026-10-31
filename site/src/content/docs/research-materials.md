---
title: Research materials
description: Paper, evidence reports, detection rules, and the downloadable source edition supporting the UNK_DeadDrop series.
---

The site ships with the public materials needed to review the series without depending on the original workspace layout.

## Paper and source edition

- Scanner paper: [PDF](/UNK_DeadDrop/downloads/UNK-Scanner-Paper.pdf) · [Zenodo record](https://doi.org/10.5281/zenodo.23826671) · [Concept DOI](https://doi.org/10.5281/zenodo.23823715) · CC BY 4.0.
- Campaign preprint: [PDF](/UNK_DeadDrop/downloads/UNK_DeadDrop-Preprint.pdf) · [Current Zenodo version](https://doi.org/10.5281/zenodo.23829170) · [Concept DOI](https://doi.org/10.5281/zenodo.23652297) · CC BY 4.0.
- [Blog series source package](/UNK_DeadDrop/downloads/UNK_DeadDrop-Blog-Series.zip)

The scanner PDF is the file deposited at Zenodo, SHA-256 `5c1dbf32898275bc48e7191f8a2d49501539c6a1b049aca574838c9aec7a4553`. The campaign PDF also matches its current Zenodo version.

## Evidence reports

Each article links directly to the reports supporting its claims. The full list is here, so readers can open a specific exhibit without going through the evidence directory. The reports are edited summaries, not complete forensic exports.

[Download all 21 PDF reports](/UNK_DeadDrop/evidence/UNK_DeadDrop-E01-E21-PDFs.zip) · [Collection notes](/UNK_DeadDrop/evidence/README.md) · [Checksums](/UNK_DeadDrop/evidence/SHA256SUMS)

| Exhibit | Subject | Files |
|---|---|---|
| E01 | Master investigation report | [PDF](/UNK_DeadDrop/evidence/E01.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E01.md) |
| E02 | Clipboard-lure deobfuscation analysis | [PDF](/UNK_DeadDrop/evidence/E02.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E02.md) |
| E03 | Editor-extension package analysis | [PDF](/UNK_DeadDrop/evidence/E03.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E03.md) |
| E04 | Authenticated payload-decryption analysis | [PDF](/UNK_DeadDrop/evidence/E04.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E04.md) |
| E05 | Payload capability re-examination | [PDF](/UNK_DeadDrop/evidence/E05.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E05.md) |
| E06 | Administration frontend analysis | [PDF](/UNK_DeadDrop/evidence/E06.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E06.md) |
| E07 | Configuration and infrastructure history | [PDF](/UNK_DeadDrop/evidence/E07.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E07.md) |
| E08 | Target-acquisition code and database aggregates | [PDF](/UNK_DeadDrop/evidence/E08.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E08.md) |
| E09 | Deployment and mail-guide analysis | [PDF](/UNK_DeadDrop/evidence/E09.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E09.md) |
| E10 | Repository-ownership reassessment | [PDF](/UNK_DeadDrop/evidence/E10.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E10.md) |
| E11 | Archive lineage and configuration rotation | [PDF](/UNK_DeadDrop/evidence/E11.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E11.md) |
| E12 | Attribution and build-artifact assessment | [PDF](/UNK_DeadDrop/evidence/E12.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E12.md) |
| E13 | Development-application configuration analysis | [PDF](/UNK_DeadDrop/evidence/E13.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E13.md) |
| E14 | Image-provenance examination | [PDF](/UNK_DeadDrop/evidence/E14.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E14.md) |
| E15 | Companion tooling and validation record | [PDF](/UNK_DeadDrop/evidence/E15.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E15.md) |
| E16 | Retraction of an earlier campaign attribution | [PDF](/UNK_DeadDrop/evidence/E16.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E16.md) |
| E17 | Stage-three collection and configuration analysis | [PDF](/UNK_DeadDrop/evidence/E17.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E17.md) |
| E18 | Framework and sample comparison | [PDF](/UNK_DeadDrop/evidence/E18.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E18.md) |
| E19 | Windows elevation and Electron execution analysis | [PDF](/UNK_DeadDrop/evidence/E19.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E19.md) |
| E20 | Historical origin-server observations | [PDF](/UNK_DeadDrop/evidence/E20.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E20.md) |
| E21 | Build and hosting chronology | [PDF](/UNK_DeadDrop/evidence/E21.pdf) · [Readable report](/UNK_DeadDrop/evidence/reports/E21.md) |

The [historical indicator reference](/UNK_DeadDrop/indicators/) collects defanged URLs, domains, paths and IP observations, separating captured evidence from weaker leads. The [sample and repository artifact reference](/UNK_DeadDrop/artifacts/) adds exact hashes for selected held payloads, recovered URLScan response bodies, repository files and the ECHOES archive lineage.

## Detection companion

The [companion repository](https://github.com/KrasForge/unk-deaddrop-companion) contains the parse-only AST scanner and 33 named YARA rules across 28 files. A read-only replay matched every rule against retained case artifacts; a separate scan of 1,914 local software files produced no hits. The paper distinguishes the published rule snapshot from a later local YARA noise review. The installable scanner is now available on [npm](https://www.npmjs.com/package/unk-scanner) and [PyPI](https://pypi.org/project/unk-scanner/); its expanded registry evaluation and bypass study are described in [Part 13](/UNK_DeadDrop/articles/13-scanner-registry-benchmark/) and [Part 14](/UNK_DeadDrop/articles/14-scanner-recovery-and-bypasses/). The rules remain experimental and the small baselines do not establish fleet-wide false-positive rates. Sigma rules are omitted because authentic endpoint event logs were unavailable for replay.

## Citation boundary

The scanner experiments are dated 29 October 2026. The case evidence runs through 24 July 2026. The public-literature refresh runs through 25 October 2026. Later reporting is used to assess context and novelty, while case-specific technical claims remain tied to retained evidence.
