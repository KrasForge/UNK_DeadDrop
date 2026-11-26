---
title: "Building and Testing Detections for UNK_DeadDrop"
description: "Thirty-three YARA rules replayed against retained artifacts, followed by a separate noise review, a static scanner evaluation and a look at what source scanning cannot see."
lastUpdated: 2026-11-26
sidebar:
  order: 11
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/11.png"
  - tag: meta
    attrs:
      property: og:image:width
      content: "1200"
  - tag: meta
    attrs:
      property: og:image:height
      content: "630"
  - tag: meta
    attrs:
      property: og:image:alt
      content: "Part 11: Building and Testing Detections for UNK_DeadDrop"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/11.png"
---



The published companion snapshot contains 33 named YARA rules in 28 files, and every rule matched at least one object in the saved investigation material, while none matched the small local software baseline. A wider noise review on the same day found that seven source rules collided with public browser-decryption research and tooling and with my own published exhibits and rendered articles, which is exactly the kind of input a rule author does not think to use as a control. I tightened the seven that day, the revisions preserved every earlier artifact match, and they are still not part of the published snapshot.

The wallet-agent rule initially matched marker-rich research prose, and requiring ELF magic at byte zero rejects that text fixture. It checks the header, not the executable's behavior.

The [companion repository](https://github.com/KrasForge/unk-scanner) contains file-content rules and a parse-only JavaScript scanner, but it no longer includes the event rules or workspace-configuration rules: authentic endpoint logs and the original `.vscode` task and settings files were not available for replay. Synthetic event records and invented configuration files would show how a rule behaves, not whether it matches the collected targets.

## The wallet-agent rule matched the held Go binary

The wallet-agent rule now requires ELF magic at byte zero, a file smaller than 64 MiB, an Overlord module path, a server-environment marker and at least two wallet-collection strings. The combination matched the held Go agent. Removing the header or one required marker category gives a negative result in the inert boundary tests.

The earlier rule version matched a harmless fixture with the complete marker set in research prose, and requiring the ELF header at offset zero prevents that ordinary text collision. YARA does not validate the rest of the executable or determine whether the strings are reachable code. So a marker-rich ELF can still match.

A file signature identifies matching content. Execution and data transfer require host evidence; operator attribution requires a separate investigation.

![YARA conditions and validation results](/UNK_DeadDrop/diagrams/11-detection-logic.svg)

*Figure 1. Every wallet-agent condition is required. The retained rules matched case artifacts, while the local software baseline and marker-rich prose fixture had no hits.*

## The replay covered 192 files and 395 views

The read-only replay on 26 October covered 192 selected files: the 15 quarantined sample directories, compressed lure bundles, web assets, extracted VSIX components and agent archives, source files, and six retained lure messages, and the helper read ZIP, VSIX, TAR, gzip and nested ZIP content in memory without writing extracted files.

It evaluated 395 raw or archive-member views totaling about 234 MB, and all 33 named rules in 28 files matched at least once (at least one rule matched 90 input files, and 102 had no hits). The totals include copied variants and nested archive views, so they are not independent samples or incidents; [Exhibit E15](../../evidence/E15.pdf) records the companion snapshot and validation scope. No file was executed.

Four ECHOES RAR archives require a password, so their members were not inspected, while the separate sealed-environment archive was scanned only as raw bytes, and exact hashes identify the four ECHOES containers without making claims about their contents.

A separate exact-hash rule identifies the retained Surge Group message. It does not claim the message shares control with UNK_DeadDrop. Other hash rules identify exact retained packages, launchers and messages. Modification or repackaging evades them.

Most unmatched inputs were generic dashboard modules, web assets or research context without a distinctive file-content signature; they were included in the coverage accounting, but weak rules that only identify those records would not be useful detections.

Workspace-file signatures remain absent because neither the original `.vscode/tasks.json` nor `.vscode/settings.json` appears in the saved repository archive or its commit history, so UNK_DeadDrop is the case in which I understood configuration-launched execution but could not turn it into a published signature. Event rules were removed because there are no authentic Windows process, Linux audit or comparable endpoint logs in the retained set, and for the same reason the companion has no Sigma rules and I have submitted none to the public Sigma repository; that waits until real target logs exist. The two SQLite databases containing target addresses were also excluded from scanning.

The companion's [artifact-validation report](https://github.com/KrasForge/unk-scanner/blob/main/docs/actual-artifact-validation.md) lists per-rule match counts and corpus limits. Its [detection notes](https://github.com/KrasForge/unk-scanner/blob/main/docs/detection-notes.md) explain each condition and its limits.

## No matches in 1,914 local software files

The second scan covered 1,914 files and about 59.2 MB across 2,379 raw and nested object views from the local CPython standard library, installed Python packages, global npm packages and Acorn. No retained rule matched. The 19 Markdown articles and companion notes also produced no hits after source-oriented conditions were narrowed to avoid prose collisions. The baseline consists of local software. Its small, uncurated sample cannot support estimates of fleet false-positive rate or production precision.

The prose fixture remains important alongside that zero-hit result, as it records a false-positive case from the rule's earlier form and confirms the current ELF-header check rejects plain text; analysts should still review file type, acquisition context and matched bytes before treating a hit as suspicious. For process and persistence behavior, collect authentic endpoint logs first; this repository does not publish event rules without them.

The later local review covered 177 case inputs, 380 views and 344 distinct objects, and after the seven source rules were narrowed they had no hits across research, dual-use tooling, ordinary software, installed software and upstream-fork controls, with every previous case-artifact match preserved and no control removed to obtain that result. This bounded control set does not estimate a production false-positive rate, and a rule name remains a label rather than a verdict: because the kit's stages share code, a marker rule describes code lineage, not a file's position in the chain.

## YARA matches byte patterns; unk-scanner parses JavaScript

The YARA replay measures whether particular bytes match the signatures, while `unk-scanner` instead parses JavaScript and follows selected expressions, string decoders and launch structures; a file can match a content signature while the scanner misses its behavior, or produce a scanner warning because it uses obfuscation that also appears in legitimate software.

The expanded scanner evaluation has its own [paper](../../downloads/UNK-Scanner-Paper.pdf), which covers popular npm packages and editor extensions, recently changed npm packages, and a separate public malware dataset. The final popular-software scan raised no errors in 188,901 files outside the initial calibration corpus, although an earlier run on those files informed one escalation-rule adjustment, and in the registry changes corpus, two of 19,976 packages raised errors; full review classified both as false positives.

Sensitivity tells a different story. The engine as first calibrated warned on only 62 of 2,122 known-malicious samples, and the revised engine, which recognizes a second decoder shape, raised that to 128, still with none at error level, so roughly nineteen in twenty public malware samples get no warning at all. Most lacked the clipboard, Electron or encrypted-loader structures that the higher-severity rules recognize, and the retained Windows Node agent also stays below warning level, yet its known collection functionality does not become benign because this rule set misses it.

There is also a blind spot that no rule change closes. The scanner reads only `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts` and `.tsx` files, so editor tasks, coding-agent hooks and rules, package scripts, build files and a payload saved under a font name are never opened, and when I checked it against the configuration launchers of 2026 it saw none of them. In November I built a separate, private method for that surface, which reports a repository only when an automatic trigger and a suspicious target occur together and which tests whether a font, image or document file actually parses as JavaScript. On 300 real folder-open task files from public repositories it flagged 78 launchers with no false positive, and it reached payloads that string recovery and multi-engine scanning had missed, because the disguise defeats file selection before any analysis begins.

[Part 13](../13-scanner-registry-benchmark/) covers corpus selection, review depth, parser coverage and throughput. [Part 14](../14-scanner-recovery-and-bypasses/) examines nineteen small variants, eighteen of which evaded a rule, lowered severity or defeated string recovery, and a hardened engine that later closed all but one of them without adding error-level findings on the same corpora. These results concern the scanner, not the 33 YARA rules or their control set.

## Rule matches depend on the bytes given to YARA

YARA can inspect only the bytes supplied to it. A rule for decrypted JavaScript needs those plaintext bytes, a rule for a VSIX member needs the member supplied to the engine, and scanning an outer compressed package alone is not equivalent to the archive-member replay above. Consult each rule's target and match conditions before choosing a sample.

On the public rule-hunting platform the two launcher rules I deployed are active, and its records for the held Windows launcher include both hits, but only when the service is queried from an authenticated account in the way it expects; an unauthenticated or mis-scoped query reads as a clean negative. Its manual file scan cannot validate account-deployed rules and runs an older engine than the one I replay with, so deployment is confirmed while engine compatibility is not. Public sample collections also hold very little of this material: on 7 November I submitted indicators to ThreatFox and on 8 November a launcher to MalwareBazaar, and when I looked up 273 case hashes on 15 November only fourteen were present in one public repository, ten of them my own submissions, and two in another. Two YARA hits on a public sample record turned out to be my own rules reflected back, which is why I check every service I both read and write by submitter before counting anything as corroboration.

The repository includes inert [YARA boundary tests](https://github.com/KrasForge/unk-scanner/blob/main/tests/test_detections.py), a [prose false-positive test](https://github.com/KrasForge/unk-scanner/blob/main/tests/test_blog_boundaries.py), and the [test requirements](https://github.com/KrasForge/unk-scanner/blob/main/requirements-dev.txt). Run the checks using the instructions in its README. These tests are repeatable checks of rule behavior, not malware execution or production validation.
