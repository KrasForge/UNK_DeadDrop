---
title: UNK_DeadDrop technical series
description: Twenty-four articles tracing developer-targeted recruitment malware from delivery artifacts through collection, infrastructure, personas, attribution and the separate PolinRider operation.
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
      link: https://github.com/KrasForge/unk-scanner
      variant: minimal
---

The series starts with three recruitment messages received in June and July 2026. It follows the evidence through clipboard substitution, a malicious editor extension, credential and wallet collection, mutable infrastructure, targeting databases, administration software and experimental detections, then on to the persona farm behind the operators' credibility, the control layer after October, and PolinRider, a separate operation that the investigation ran into along the way.

Parts 1 to 14 began with evidence ending on 24 July 2026 and have been brought up to the case record of 17 November 2026; Parts 15 to 24 rest on that record. Public reporting was checked through 18 November 2026. Each article distinguishes static capability from observed execution and identifies where the retained artifacts stop.

## Read the investigation

### UNK_DeadDrop: delivery, collection and infrastructure

1. [Anatomy of a Developer Lure: ClickFix Clipboard Manipulation](__BASE_PATH__/articles/01-clickfix-clipboard-manipulation/)
2. [How a Malicious VSIX Uses the Signed Editor Runtime](__BASE_PATH__/articles/02-vsix-editor-execution/)
3. [Parsing Without Executing: JavaScript Deobfuscation with Acorn](__BASE_PATH__/articles/03-acorn-deobfuscation/)
4. [Inside the Collector: Browser Credentials and Wallet Files](__BASE_PATH__/articles/04-credential-wallet-collection/)
5. [Beyond Screenshot Strings: Reconstructing Screen Capture](__BASE_PATH__/articles/05-screen-capture-analysis/)
6. [Following the GitLab Dead Drop: Configuration Changes and C2 History](__BASE_PATH__/articles/06-gitlab-dead-drop-infrastructure/)
7. [From Commit Metadata to a Developer Target List](__BASE_PATH__/articles/07-developer-target-harvesting/)
8. [Inside rms-platform: Delivery Monitoring and Wallet Administration](__BASE_PATH__/articles/08-administration-platform/)
9. [Tracing the ECHOES Archive: Payload Lineage and Image Provenance](__BASE_PATH__/articles/09-echoes-lineage-image-provenance/)
10. [From Three Phishing Emails to a Connected Investigation](__BASE_PATH__/articles/10-investigation-connections/)
11. [Building and Testing Detections for UNK_DeadDrop](__BASE_PATH__/articles/11-detection-engineering/)
12. [Where Overlord Ends and the Collection Toolchain Begins](__BASE_PATH__/articles/12-framework-and-collection-boundary/)
13. [What 2.8 Million Files Revealed About unk-scanner](__BASE_PATH__/articles/13-scanner-registry-benchmark/)
14. [When a Decoder Returns the Wrong Strings](__BASE_PATH__/articles/14-scanner-recovery-and-bypasses/)

### UNK_DeadDrop: personas, control layer and attribution

15. [The TronzitVeca Persona Farm: Borrowed Histories and Manufactured Developers](__BASE_PATH__/articles/15-persona-farm/)
16. [After October: Dead-Drop Successors, Panel Lineage and One Hosting Provider](__BASE_PATH__/articles/16-control-layer-after-october/)
17. [Two Operations, One Ecosystem: Separating UNK_DeadDrop from PolinRider](__BASE_PATH__/articles/17-two-operations-one-ecosystem/)

### PolinRider, a separate operation

18. [Following a Developer from UNK_DeadDrop to PolinRider](__BASE_PATH__/articles/18-polinrider-following-a-developer/)
19. [How PolinRider Uses Blockchains as an Address Book](__BASE_PATH__/articles/19-polinrider-ethereum-address-book/)
20. [Three Resolver Wallets and Eleven Hosts](__BASE_PATH__/articles/20-polinrider-wallets-and-hosts/)
21. [When One Assessment Reaches Nineteen Repositories](__BASE_PATH__/articles/21-polinrider-repository-spread/)
22. [What 2,301 Affected Accounts Actually Means](__BASE_PATH__/articles/22-polinrider-counting-repositories/)
23. [Detecting PolinRider Beyond a Filename](__BASE_PATH__/articles/23-polinrider-detection/)
24. [Following PolinRider's Money: Gas, Bridges, Laundering and Cash-Out](__BASE_PATH__/articles/24-polinrider-money/)

## Scope

The published material excludes raw contact databases, credentials, and a complete forensic sample set. Supporting PDFs are edited evidence reports derived from the restricted case material. The series does not claim successful compromise, financial loss, or real-world attribution where the artifacts do not establish those outcomes.

## About the author

Ilja Krasnjanski is an independent security researcher publishing as KrasForge. He studies developer recruitment lures, malware and detection methods. [More about the author](__BASE_PATH__/about/).
