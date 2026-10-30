---
title: UNK_DeadDrop technical series
description: Fourteen articles tracing developer-targeted phishing from delivery artifacts through collection, infrastructure, administration tooling, and detection engineering.
template: splash
hero:
  tagline: An artifact-led investigation of developer-targeted phishing and its supporting collection infrastructure.
  actions:
    - text: Start with Part 1
      link: __BASE_PATH__/articles/01-clickfix-clipboard-manipulation/
      icon: right-arrow
    - text: Read the technical paper
      link: __BASE_PATH__/downloads/UNK_DeadDrop-Preprint.pdf
      variant: minimal
    - text: Read the scanner paper
      link: __BASE_PATH__/downloads/UNK-Scanner-Paper.pdf
      variant: minimal
    - text: Open Source Detection Rules
      link: https://github.com/KrasForge/unk-deaddrop-companion
      variant: minimal
---

The series starts with three recruitment messages received in June and July 2026. It follows the evidence through clipboard substitution, a malicious editor extension, credential and wallet collection, mutable infrastructure, targeting databases, administration software, and experimental detections.

The underlying case evidence ends on 24 July 2026. Public reporting was checked through 25 October 2026. Each article distinguishes static capability from observed execution and identifies where the retained artifacts stop.

## Read the investigation

1. [The copy button changes the command](__BASE_PATH__/articles/01-clickfix-clipboard-manipulation/)
2. [A folder-open task in the VS Code project](__BASE_PATH__/articles/02-vsix-editor-execution/)
3. [Recovering the VS Code extension's AES key without running it](__BASE_PATH__/articles/03-acorn-deobfuscation/)
4. [Browser credentials, wallet material, and private-key files](__BASE_PATH__/articles/04-credential-wallet-collection/)
5. [Screen capture in the Go agent and Windows bundle](__BASE_PATH__/articles/05-screen-capture-analysis/)
6. [GitLab's resolver changed the server list](__BASE_PATH__/articles/06-gitlab-dead-drop-infrastructure/)
7. [Two SQLite pools held 142,365 address strings](__BASE_PATH__/articles/07-developer-target-harvesting/)
8. [Seventy modules from the rms-platform frontend](__BASE_PATH__/articles/08-administration-platform/)
9. [Four ECHOES revisions, no final PowerShell payload](__BASE_PATH__/articles/09-echoes-lineage-image-provenance/)
10. [Three phishing lures and their different delivery paths](__BASE_PATH__/articles/10-investigation-connections/)
11. [Testing 33 YARA rules against the retained artifacts](__BASE_PATH__/articles/11-detection-engineering/)
12. [Overlord markers in the Linux agent's collection code](__BASE_PATH__/articles/12-framework-and-collection-boundary/)
13. [Two false alarms, low coverage of public malware](__BASE_PATH__/articles/13-scanner-registry-benchmark/)
14. [Array splicing broke string recovery](__BASE_PATH__/articles/14-scanner-recovery-and-bypasses/)

## Scope

The published material excludes raw contact databases, credentials, and a complete forensic sample set. Supporting PDFs are edited evidence reports derived from the restricted case material. The series does not claim successful compromise, financial loss, or real-world attribution where the artifacts do not establish those outcomes.
