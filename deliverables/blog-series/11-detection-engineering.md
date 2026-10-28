---
title: "Building and Testing Detections for UNK_DeadDrop"
description: "Thirty-three YARA rules replayed against retained artifacts, followed by a separate noise review and static scanner evaluation."
date: "2026-10-27"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/11-detection-engineering/"
kicker: "UNK_DeadDrop · Part 11"
tags:
  - "UNK_DeadDrop"
  - "YARA"
  - "detection engineering"
og_image_alt: "YARA matching conditions and results from case-artifact and software-baseline scans"
---


The published companion snapshot contains 33 named YARA rules in 28 files. Every rule matched at least one object in the saved investigation material, and none matched the small local software baseline. A later, separate local review narrowed seven source rules after selected controls produced collisions. The revisions preserved all earlier artifact matches, but are not part of the published snapshot. The wallet-agent rule initially matched marker-rich research prose; requiring ELF magic at byte zero makes that text fixture negative, though it does not validate the file's code or prove execution.

The [companion repository](https://github.com/KrasForge/unk-deaddrop-companion) contains file-content rules and a parse-only JavaScript scanner. It no longer includes the event rules or workspace-configuration rules: authentic endpoint logs and the original `.vscode` task and settings files were not available for replay. Synthetic event records and invented configuration files would show how a rule behaves, not whether it matches the collected targets.

## A content match is not an execution finding

The wallet-agent rule is a useful example. It now requires ELF magic at byte zero, a file smaller than 64 MiB, an Overlord module path, a server-environment marker and at least two wallet-collection strings. The combination matched the held Go agent. Removing the header or one required marker category gives a negative result in the inert boundary tests.

The earlier rule version matched a harmless fixture with the complete marker set in research prose. Requiring the ELF header at offset zero prevents that ordinary text collision, but YARA does not validate the rest of the executable or determine whether the strings are reachable code. A marker-rich ELF can still match. A file signature can help identify an artifact for review, but it cannot establish that the file ran, that data left the host or that the activity belongs to a particular operator.

![YARA conditions and validation results](assets/11-detection-logic.svg)

*Figure 1. Every wallet-agent condition is required. The retained rules matched case artifacts, while the local software baseline and marker-rich prose fixture had no hits.*

## Replay against retained files

The read-only replay covered 192 selected files: the 15 directories marked `DO-NOT-RUN`, compressed lure bundles, related web assets, extracted VSIX components and agent archives, source files, and six retained lure messages. The helper read ZIP, VSIX, TAR, gzip and nested ZIP content in memory without writing extracted files. It evaluated 395 raw or archive-member views totaling about 234 MB; all 33 named rules in 28 files matched at least once. At least one rule matched 90 input files, while 102 had no hits. Counts include copied variants and nested archive views, so they are not independent samples or incidents. [Exhibit E15](../preprint/evidence/E15.pdf) records the companion snapshot and validation scope. No file was executed.

Four ECHOES RAR archives require a password, so their members were not inspected; the separate sealed environment archive was scanned only as raw bytes. Exact hashes identify the four ECHOES containers without making claims about their contents. A separate exact-hash rule identifies the retained Surge Group message; the rule does not claim it shares control with UNK_DeadDrop. Other hash rules identify exact retained packages, launchers and messages; any modification or repackaging evades them. Most unmatched inputs were generic dashboard modules, web assets or research context without a distinctive file-content signature. They were reviewed in the coverage accounting, but weak rules that merely identify those records would not be useful detections.

Workspace-file signatures remain absent because neither the original `.vscode/tasks.json` nor `.vscode/settings.json` appears in the saved repository archive or its commit history. Event rules were removed because there are no authentic Windows process, Linux audit or comparable endpoint logs in the retained set. The companion therefore has no Sigma rules. The two SQLite databases containing target addresses were also excluded from scanning.

The companion's [artifact-validation report](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/docs/actual-artifact-validation.md) lists per-rule match counts and corpus limits. Its [detection notes](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/docs/detection-notes.md) document what each condition does and does not establish.

## A limited software baseline

The second scan covered 1,914 files and about 59.2 MB across 2,379 raw and nested object views from the local CPython standard library, installed Python packages, global npm packages and Acorn. No retained rule matched. The 19 Markdown articles and companion notes also produced no hits after source-oriented conditions were narrowed to avoid prose collisions. This is a small local baseline, not a representative or independently curated clean endpoint corpus, so it does not provide a fleet false-positive rate or a production precision estimate.

The prose fixture remains important alongside that zero-hit result. It records a false-positive case from the rule's earlier form and confirms the current ELF-header check rejects plain text. Analysts should still review file type, acquisition context and matched bytes before treating a hit as suspicious. For process and persistence behavior, collect authentic endpoint logs first; this repository does not publish event rules without them.

A later local review covered 177 case inputs, 380 views and 344 distinct objects. Seven source rules were narrowed after collisions in selected research, dual-use tooling, ordinary software, installed software and upstream-fork controls. Every previous case-artifact match was preserved, and the seven revised forms had no hits in the external controls scanned. This bounded control set does not estimate a production false-positive rate; the revisions remain separate from the public companion snapshot.

The [preprint on Zenodo](https://doi.org/10.5281/zenodo.23696198) also evaluates a separate local `unk-scanner` 0.1.0 package. It parsed 31 selected JavaScript inputs from the case material, producing 27 syntax-based findings and four identity-only records covering three distinct hashes. Of 500 local JavaScript baseline files, all parsed; one legitimate clipboard operation produced a syntax finding, and none matched an identity record. These 31 inputs were accounted for, not all identified as malicious. The package and evaluation were not part of the public companion commit.

The repository includes inert [YARA boundary tests](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/tests/test_detections.py), a [prose false-positive test](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/tests/test_blog_boundaries.py), and the [test requirements](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/requirements-dev.txt). Run the checks using the instructions in its README. These tests are repeatable checks of rule behavior, not malware execution or production validation.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
