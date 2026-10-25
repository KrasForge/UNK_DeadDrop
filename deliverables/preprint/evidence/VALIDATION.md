# Evidence-report validation — 24 October 2026

Created 21 edited analytical reports, E01–E21, totaling 79 PDF pages.
Each contains substantive observations, method context, interpretation limits and
source-record fingerprints. They are derived reports, not original forensic exports
or independent verification of all findings in the underlying case records.

## Checks performed

- All 21 report identifiers have Markdown and PDF documents.
- Source-citation identifiers resolve within each document.
- PDF, report and exhibit-file hashes match the manifest; source fingerprints appear in the PDFs. Every registered exhibit input was checked against its actual size and SHA-256, including historical Git blobs.
- All PDF text bounding boxes remain inside page boundaries; all fonts are embedded.
- The ZIP contains exactly 21 PDFs plus SHA256SUMS; its contents match the manifest.
- Extracted report text has no local investigation paths, email addresses, GitHub
  token prefixes or API-key URL parameters under the implemented checks.
- Page layouts were reviewed as contact sheets, with detailed inspection of
  representative pages. Long hash paragraphs use left alignment to avoid excessive
  justification spacing, and source lists remain together.
- The rebuilt preprint is 14 pages with its abstract on the opening page
  and the introduction on page 2. Appendix B describes the new report editions.

The content review carries forward corrections to the original notes: bounded
negative searches, frontend/backend distinctions, timestamp semantics, limits of
infrastructure attribution and the missing final ECHOES payload. The privacy checks
are targeted checks, not a guarantee of exhaustive sensitive-data detection.

## Work not repeated

No malware was executed, no historical infrastructure was contacted, no recovered
credential was used, and nothing was uploaded. Database aggregates were reproduced read-only on 24 October, without exporting contact rows. Eight offline AST tests also passed, as recorded in E15. Authenticated decryption, independent image-signature verification and the four detection tests were not rerun. Missing original inputs are explicitly identified in the reports.

## Recheck

Run `python deliverables/preprint/evidence/verify.py` in an environment containing
PyMuPDF. ReportLab is required for the separate build script. The verifier checks
package completeness, fingerprints, citations, text boundaries, fonts and archive
contents; it does not reproduce the underlying investigation.

## Discrepancy review

Corrected message dates, key-fragment counts, payload-comparison conclusions, author/committer collection and ingestion normalization, ECHOES revision timing, and statements about reproduced checks. Removed the unsupported encrypted-archive configuration schema and replaced the schematic header dump with measured signature and name-offset values. Distinguished embedded provenance assertions from independent signature verification, and retained panel files from unretained direct-IP scan results. The register now uses “Exhibit inputs” because some inputs are analytical records rather than primary observations. Corresponding preprint and blog statements were synchronized. Historical source notes are preserved rather than rewritten.

E21’s earlier exhibit incorrectly limited ZIP dates to June. A full member listing reproduced the July 13 and July 20 entries; the corrected exhibit reports the complete date distribution.
