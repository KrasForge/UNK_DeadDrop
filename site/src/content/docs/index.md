---
title: UNK_DeadDrop technical series
description: Fourteen articles tracing developer-targeted phishing from delivery artifacts through collection, infrastructure, administration tooling, and detection engineering.
template: splash
hero:
  tagline: An artifact-led investigation of developer-targeted phishing and its supporting collection infrastructure.
  actions:
    - text: Start with Part 1
      link: /UNK_DeadDrop/articles/01-clickfix-clipboard-manipulation/
      icon: right-arrow
    - text: Read the technical paper
      link: /UNK_DeadDrop/downloads/UNK_DeadDrop-Preprint.pdf
      variant: minimal
    - text: Open Source Detection Rules
      link: https://github.com/KrasForge/unk-deaddrop-companion
      variant: minimal
---

The series starts with three recruitment messages received in June and July 2026. It follows the evidence through clipboard substitution, a malicious editor extension, credential and wallet collection, mutable infrastructure, targeting databases, administration software, and experimental detections.

The underlying case evidence ends on 24 July 2026. Public reporting was checked through 25 October 2026. Each article distinguishes static capability from observed execution and identifies where the retained artifacts stop.

## Read the investigation

1. [Anatomy of a Developer Lure: ClickFix Clipboard Manipulation](/UNK_DeadDrop/articles/01-clickfix-clipboard-manipulation/)
2. [How a Malicious VSIX Uses the Signed Editor Runtime](/UNK_DeadDrop/articles/02-vsix-editor-execution/)
3. [Parsing Without Executing: JavaScript Deobfuscation with Acorn](/UNK_DeadDrop/articles/03-acorn-deobfuscation/)
4. [Inside the Collector: Browser Credentials and Wallet Files](/UNK_DeadDrop/articles/04-credential-wallet-collection/)
5. [Beyond Screenshot Strings: Reconstructing Screen Capture](/UNK_DeadDrop/articles/05-screen-capture-analysis/)
6. [Following the GitLab Dead Drop](/UNK_DeadDrop/articles/06-gitlab-dead-drop-infrastructure/)
7. [From Commit Metadata to a Developer Target List](/UNK_DeadDrop/articles/07-developer-target-harvesting/)
8. [Inside rms-platform](/UNK_DeadDrop/articles/08-administration-platform/)
9. [Tracing the ECHOES Archive](/UNK_DeadDrop/articles/09-echoes-lineage-image-provenance/)
10. [From Three Phishing Emails to a Connected Investigation](/UNK_DeadDrop/articles/10-investigation-connections/)
11. [Building and Testing Detections for UNK_DeadDrop](/UNK_DeadDrop/articles/11-detection-engineering/)
12. [Where Overlord Ends and the Collection Toolchain Begins](/UNK_DeadDrop/articles/12-framework-and-collection-boundary/)

## Scanner follow-ups

The October evaluation extends the investigation into static-analysis tooling. These articles cover a larger registry corpus, the alerts that survived review, missed malware and incorrect string recovery.

13. [What 2.8 Million Files Revealed About unk-scanner](/UNK_DeadDrop/articles/13-scanner-registry-benchmark/)
14. [When a Decoder Returns the Wrong Strings](/UNK_DeadDrop/articles/14-scanner-recovery-and-bypasses/)

[Read the scanner paper (PDF)](/UNK_DeadDrop/downloads/UNK-Scanner-Paper.pdf).

## Scope

The published material excludes raw contact databases, credentials, and a complete forensic sample set. Supporting PDFs are edited evidence reports derived from the restricted case material. The series does not claim successful compromise, financial loss, or real-world attribution where the artifacts do not establish those outcomes.
