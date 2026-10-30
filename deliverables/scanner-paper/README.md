# Scanner paper

Title: *Static AST-Based Triage of Socially-Engineered Developer Lures: Proving Obfuscator Rotations Without Execution* (renamed 29 October 2026 from *Static AST-Based Detection of Socially-Engineered Developer Malware: Overcoming Client-Side Obfuscation at Registry Scale*, which overclaimed after Tier 3).

Split from the UNK_DeadDrop preprint on 29 October 2026; that paper is now threat-intelligence only and cites this one as [R18]. `paper.md` is the draft. The three-tier evaluation and the bypass experiment are complete (all runs on the netcup server with the frozen engine; results, ledgers and summaries in `../unk-scanner/benchmark/`, `tiers/` and `bypass/`). Related-work citations were checked against primary sources on 29 October 2026. `build.py --final --output UNK-Scanner-Paper.pdf` typesets the paper; without `--final` it writes `UNK-Scanner-Paper-DRAFT.pdf` (ReportLab 5.0.1, as `../preprint/requirements.txt`): while [PENDING]/[verify] markers remain it prints a red draft header and highlights them; `build.py --final` refuses to build until none remain.

Editorial revision on 29 October: `UNK-Scanner-Paper.pdf` is rebuilt from revised source. See `VALIDATION.md` for writing changes, evaluation qualifications and PDF checks.

Decoder-coverage revision on 30 October: Section 5.7 adds a revised engine (`ba4d1468…`) that recognises two further decoder shapes, a held-out set of five obfuscator releases, and a rerun of every corpus (companion PR #11).

Expansion on 30 October: Figure 1, Algorithm 1 with a worked example, an expanded implementation section, an artifact table, and Section 5.7, a controlled string-array recovery experiment against three deobfuscators (data in `../unk-scanner/benchmark/rotation/`). See `VALIDATION.md`.

Hardening revision on 29 October: Sections 5.1 to 5.5 still report the frozen engine (source SHA-256 `caf3f552…`). The new Section 5.6 reports the hardened engine (`202f56f2…`), rescanned on the netcup server against the bypass fixtures, the 14 artifacts and all four corpora; data in `../unk-scanner/benchmark/mitigation/`.
