---
title: Research materials
description: Paper, evidence reports, detection rules, and the downloadable source edition supporting the UNK_DeadDrop series.
---

The site ships with the public materials needed to review the series without depending on the original workspace layout.

## Paper and source edition

- Scanner paper: [PDF](__BASE_PATH__/downloads/UNK-Scanner-Paper.pdf) · [Zenodo record](https://doi.org/10.5281/zenodo.23823716) · [Concept DOI](https://doi.org/10.5281/zenodo.23823715) · CC BY 4.0.
- Campaign preprint: [PDF](__BASE_PATH__/downloads/UNK_DeadDrop-Preprint.pdf) · [Current Zenodo version](https://doi.org/10.5281/zenodo.23823077) · [Concept DOI](https://doi.org/10.5281/zenodo.23652297) · CC BY 4.0.
- [Blog series source package](__BASE_PATH__/downloads/UNK_DeadDrop-Blog-Series.zip)

The scanner PDF is the file deposited at Zenodo, SHA-256 `5c1dbf32898275bc48e7191f8a2d49501539c6a1b049aca574838c9aec7a4553`. The campaign PDF also matches its current Zenodo version.

## Evidence reports

Each article links directly to the reports supporting its claims. The full list is here, so readers can open a specific exhibit without going through the evidence directory. The reports are edited summaries, not complete forensic exports.

[Download all 21 PDF reports](__BASE_PATH__/evidence/UNK_DeadDrop-E01-E21-PDFs.zip) · [Collection notes](__BASE_PATH__/evidence/README.md) · [Checksums](__BASE_PATH__/evidence/SHA256SUMS)

| Exhibit | Subject | Files |
|---|---|---|
| E01 | Master investigation report | [PDF](__BASE_PATH__/evidence/E01.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E01.md) |
| E02 | Clipboard-lure deobfuscation analysis | [PDF](__BASE_PATH__/evidence/E02.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E02.md) |
| E03 | Editor-extension package analysis | [PDF](__BASE_PATH__/evidence/E03.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E03.md) |
| E04 | Authenticated payload-decryption analysis | [PDF](__BASE_PATH__/evidence/E04.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E04.md) |
| E05 | Payload capability re-examination | [PDF](__BASE_PATH__/evidence/E05.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E05.md) |
| E06 | Administration frontend analysis | [PDF](__BASE_PATH__/evidence/E06.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E06.md) |
| E07 | Configuration and infrastructure history | [PDF](__BASE_PATH__/evidence/E07.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E07.md) |
| E08 | Target-acquisition code and database aggregates | [PDF](__BASE_PATH__/evidence/E08.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E08.md) |
| E09 | Deployment and mail-guide analysis | [PDF](__BASE_PATH__/evidence/E09.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E09.md) |
| E10 | Repository-ownership reassessment | [PDF](__BASE_PATH__/evidence/E10.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E10.md) |
| E11 | Archive lineage and configuration rotation | [PDF](__BASE_PATH__/evidence/E11.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E11.md) |
| E12 | Attribution and build-artifact assessment | [PDF](__BASE_PATH__/evidence/E12.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E12.md) |
| E13 | Development-application configuration analysis | [PDF](__BASE_PATH__/evidence/E13.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E13.md) |
| E14 | Image-provenance examination | [PDF](__BASE_PATH__/evidence/E14.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E14.md) |
| E15 | Companion tooling and validation record | [PDF](__BASE_PATH__/evidence/E15.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E15.md) |
| E16 | Retraction of an earlier campaign attribution | [PDF](__BASE_PATH__/evidence/E16.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E16.md) |
| E17 | Stage-three collection and configuration analysis | [PDF](__BASE_PATH__/evidence/E17.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E17.md) |
| E18 | Framework and sample comparison | [PDF](__BASE_PATH__/evidence/E18.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E18.md) |
| E19 | Windows elevation and Electron execution analysis | [PDF](__BASE_PATH__/evidence/E19.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E19.md) |
| E20 | Historical origin-server observations | [PDF](__BASE_PATH__/evidence/E20.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E20.md) |
| E21 | Build and hosting chronology | [PDF](__BASE_PATH__/evidence/E21.pdf) · [Readable report](__BASE_PATH__/evidence/reports/E21.md) |

The [historical indicator reference](__BASE_PATH__/indicators/) collects defanged URLs, domains, paths and IP observations, separating captured evidence from weaker leads. The [sample and repository artifact reference](__BASE_PATH__/artifacts/) adds exact hashes for selected held payloads, recovered URLScan response bodies, repository files and the ECHOES archive lineage.

## Detection companion

The [companion repository](https://github.com/KrasForge/unk-deaddrop-companion) contains the parse-only AST scanner and 33 named YARA rules across 28 files. A read-only replay matched every rule against retained case artifacts; a separate scan of 1,914 local software files produced no hits. The paper distinguishes the published rule snapshot from a later local YARA noise review. The installable scanner is now available on [npm](https://www.npmjs.com/package/unk-scanner) and [PyPI](https://pypi.org/project/unk-scanner/); its expanded registry evaluation and bypass study are described in [Part 13](__BASE_PATH__/articles/13-scanner-registry-benchmark/) and [Part 14](__BASE_PATH__/articles/14-scanner-recovery-and-bypasses/). The rules remain experimental and the small baselines do not establish fleet-wide false-positive rates. Sigma rules are omitted because authentic endpoint event logs were unavailable for replay.

## Citation boundary

The scanner experiments are dated 29 October 2026. The case evidence runs through 24 July 2026. The public-literature refresh runs through 25 October 2026. Later reporting is used to assess context and novelty, while case-specific technical claims remain tied to retained evidence.
