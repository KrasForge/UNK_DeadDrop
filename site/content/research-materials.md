---
title: Research materials
description: Paper, evidence reports, detection rules, and the downloadable source edition supporting the UNK_DeadDrop series.
---

The site ships with the public materials needed to review the series without depending on the original workspace layout.

## Paper and source edition

- [Technical paper (PDF)](__BASE_PATH__/downloads/UNK_DeadDrop-Preprint.pdf)
- [Zenodo preprint, version 1.2](https://doi.org/10.5281/zenodo.23696198) · [Concept DOI for the latest version](https://doi.org/10.5281/zenodo.23652297) · CC BY 4.0.
- [Blog series source package](__BASE_PATH__/downloads/UNK_DeadDrop-Blog-Series.zip)

## Evidence reports

Each article links directly to the reports supporting its claims. The complete public set is available in the [evidence directory](__BASE_PATH__/evidence/E01.pdf), beginning with the case overview.

## Detection companion

The [companion repository](https://github.com/KrasForge/unk-deaddrop-companion) contains the parse-only AST scanner and 33 named YARA rules across 28 files. A read-only replay matched every rule against retained case artifacts; a separate scan of 1,914 local software files produced no hits. The version 1.2 paper distinguishes that public snapshot from later local YARA noise review and scanner evaluation. The rules remain experimental and the small baselines do not establish fleet-wide false-positive rates. Sigma rules are omitted because authentic endpoint event logs were unavailable for replay.

## Citation boundary

The case evidence runs through 24 July 2026. The public-literature refresh runs through 25 October 2026. Later reporting is used to assess context and novelty, while case-specific technical claims remain tied to retained evidence.
