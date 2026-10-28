# UNK_DeadDrop evidence reports E01–E21

Prepared 24 October 2026 from the restricted case records cited by the preprint. These are edited analytical reports with exhibits: selected artifact excerpts and clearly identified secondary records, with input fingerprints and extraction methods. Redactions and display transformations are noted in the exhibits. They are not complete forensic exports. Historical findings remain dated to the underlying observations; companion engineering checks were recorded in October 2026.

The reports omit local folder organization, raw contact rows, usable credentials and personal identity leads. They preserve corrections and limits on older claims. The underlying records and databases remain restricted. The edited reports and exhibit index are published at https://krasforge.github.io/UNK_DeadDrop/evidence/. The underlying records remain restricted.

[Download all 21 PDFs](UNK_DeadDrop-E01-E21-PDFs.zip). Editable report text is retained alongside the builder.

| Evidence | Report |
|---|---|
| E01 | [Master investigation report](E01.pdf) |
| E02 | [Clipboard-lure deobfuscation analysis](E02.pdf) |
| E03 | [Editor-extension package analysis](E03.pdf) |
| E04 | [Authenticated payload-decryption analysis](E04.pdf) |
| E05 | [Payload capability re-examination](E05.pdf) |
| E06 | [Administration frontend analysis](E06.pdf) |
| E07 | [Configuration and infrastructure history](E07.pdf) |
| E08 | [Target-acquisition code and database aggregates](E08.pdf) |
| E09 | [Deployment and mail-guide analysis](E09.pdf) |
| E10 | [Repository-ownership reassessment](E10.pdf) |
| E11 | [Archive lineage and configuration rotation](E11.pdf) |
| E12 | [Attribution and build-artifact assessment](E12.pdf) |
| E13 | [Development-application configuration analysis](E13.pdf) |
| E14 | [Image-provenance examination](E14.pdf) |
| E15 | [Companion tooling and validation record](E15.pdf) |
| E16 | [Retraction of an earlier campaign attribution](E16.pdf) |
| E17 | [Stage-three collection and configuration analysis](E17.pdf) |
| E18 | [Framework and sample comparison](E18.pdf) |
| E19 | [Windows elevation and Electron execution analysis](E19.pdf) |
| E20 | [Historical origin-server observations](E20.pdf) |
| E21 | [Build and hosting chronology](E21.pdf) |

## Verification and rebuild

Each PDF identifies its source records by descriptive title, byte count and SHA-256. Local source paths are confined to the build script and are not printed in the reports or included in the PDF bundle. Source citations refer to retained records, not publicly accessible publications.

Use the preprint’s pinned ReportLab dependency, then run `python deliverables/preprint/evidence/build.py` from the investigation workspace. The builder reads local records and hashes database bytes without querying or exporting contact rows. No samples are executed and no network access is required.

Validation results are in [VALIDATION.md](VALIDATION.md). The bundle contains only E01.pdf through E21.pdf and their SHA-256 checksums.
