# UNK_DeadDrop and PolinRider: a twenty-four-part series with indicator and artifact references

Twenty-four articles, a historical indicator appendix and a sample-artifact reference by Ilja Krasnjanski, updated 26 November 2026. Parts 1–14 were brought up to the case record of 17 November 2026; Parts 15–17 add the persona farm, the control layer after October and the separation of the operations; Parts 18–24 cover PolinRider, a separate operation.
Parts 13–14 cover the larger scanner benchmark and recovery/bypass results, including the hardened engine that closed the bypasses. Parts 3, 6, 9 and 11 have been expanded or updated to match the latest analysis.
Parts 10–12 add the investigative connections, detection engineering and framework
comparison. Parts 4–5 and 7–8 are the split collection/capture and targeting/admin
articles. The hosted edition is available at [krasforge.github.io/UNK_DeadDrop](https://krasforge.github.io/UNK_DeadDrop/).

1. [Anatomy of a Developer Lure: ClickFix Clipboard Manipulation](01-clickfix-clipboard-manipulation.md)
2. [How a Malicious VSIX Uses the Signed Editor Runtime](02-vsix-editor-execution.md)
3. [Parsing Without Executing: JavaScript Deobfuscation with Acorn](03-acorn-deobfuscation.md)
4. [Inside the Collector: Browser Credentials and Wallet Files](04-credential-wallet-collection.md)
5. [Beyond Screenshot Strings: Reconstructing Screen Capture](05-screen-capture-analysis.md)
6. [Following the GitLab Dead Drop: Configuration Changes and C2 History](06-gitlab-dead-drop-infrastructure.md)
7. [From Commit Metadata to a Developer Target List](07-developer-target-harvesting.md)
8. [Inside rms-platform: Delivery Monitoring and Wallet Administration](08-administration-platform.md)
9. [Tracing the ECHOES Archive: Payload Lineage and Image Provenance](09-echoes-lineage-image-provenance.md)
10. [From Three Phishing Emails to a Connected Investigation](10-investigation-connections.md)
11. [Building and Testing Detections for UNK_DeadDrop](11-detection-engineering.md)
12. [Where Overlord Ends and the Collection Toolchain Begins](12-framework-and-collection-boundary.md)
13. [What 2.8 Million Files Revealed About unk-scanner](13-scanner-registry-benchmark.md)
14. [When a Decoder Returns the Wrong Strings](14-scanner-recovery-and-bypasses.md)
15. [The TronzitVeca Persona Farm: Borrowed Histories and Manufactured Developers](15-persona-farm.md)
16. [After October: Dead-Drop Successors, Panel Lineage and One Hosting Provider](16-control-layer-after-october.md)
17. [Two Operations, One Ecosystem: Separating UNK_DeadDrop from PolinRider](17-two-operations-one-ecosystem.md)
18. [Following a Developer from UNK_DeadDrop to PolinRider](18-polinrider-following-a-developer.md)
19. [How PolinRider Uses Blockchains as an Address Book](19-polinrider-ethereum-address-book.md)
20. [Three Resolver Wallets and Eleven Hosts](20-polinrider-wallets-and-hosts.md)
21. [When One Assessment Reaches Nineteen Repositories](21-polinrider-repository-spread.md)
22. [What 2,301 Affected Accounts Actually Means](22-polinrider-counting-repositories.md)
23. [Detecting PolinRider Beyond a Filename](23-polinrider-detection.md)
24. [Following PolinRider's Money: Gas, Bridges, Laundering and Cash-Out](24-polinrider-money.md)

[Historical indicators, artifacts and network evidence](historical-indicators.md) collects defanged lure URLs, payload hosts, resolver revisions, repository addresses and IP associations. It separates retained sample evidence from provider-based pivots and older public reporting. The [sample and repository artifact reference](artifact-reference.md) lists exact hashes for held payloads, recovered response bodies, repository files and the ECHOES archive lineage.

[Download the series and linked supporting PDFs](UNK_DeadDrop-Blog-Series.zip).
The archive preserves the relative links between articles, images and evidence.

The numbered Markdown files, indicator appendix and artifact reference contain
the 30 October edition. The Astro source is current; the older standalone HTML/PDF
previews under `rendered/2026-10-27/` do not include these changes and are not in
the ZIP. The ZIP contains the Markdown edition and linked evidence. The hosted
GitHub Pages rebuilds the hosted edition from these sources on pushes to `main`.
Each hosted article has a canonical GitHub Pages URL. Every article links to the
[companion detections and static scanner](https://github.com/KrasForge/unk-scanner).
The preprint is published on Zenodo under CC BY 4.0:
[record DOI](https://doi.org/10.5281/zenodo.23829170) ·
[concept DOI](https://doi.org/10.5281/zenodo.23652297). Current rules,
tests and validation notes live in the companion repository.

## Editorial approach

Since 26 November 2026 the posts follow the house style of research-lab publications such as Security Research
Labs: a one- or two-sentence lede with the result, a short "Key takeaways" list, two-part section headings
("Delivery: the clipboard holds a different command"), short declarative paragraphs, numbered figure captions,
limits stated beside the claim they affect and a short conclusion. They use original wording and the case's own
evidence, with descriptive evidence links in place of academic citation labels. The pre-restyle texts are kept in
`../blog-series-before-srlabs-2026-11-26/`, and `style_check.py` confirms that a restyle kept every number, code
span, indicator and link.

References consulted for structure and pacing:

- [Proofpoint: Don't Fear the Repo](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal)
- [Denys Vitali: developer malware investigation](https://blog.denv.it/posts/i-was-likely-targeted-by-dprk-in-a-sophisticated-developer-malware-campaign/)
- [Jamf: Threat Actors Expand Abuse of Microsoft Visual Studio Code](https://www.jamf.com/blog/threat-actors-expand-abuse-of-visual-studio-code/)
- [Microsoft: Contagious Interview](https://www.microsoft.com/en-us/security/blog/2026/03/11/contagious-interview-malware-delivered-through-fake-developer-job-interviews/)
- [Unit 42: BeaverTail and InvisibleFerret variants](https://unit42.paloaltonetworks.com/north-korean-threat-actors-lure-tech-job-seekers-as-fake-recruiters/)
- [Ben Hopkins: Foxtopia / UNK_DeadDrop reporting](https://brhopkins.uk/posts/foxtopia/)
- [Edison Flores: later developer-lure follow-up](https://dev.to/edison_flores_6d2cd381b13/a-fake-recruiter-sent-me-a-job-offer-that-ended-in-my-terminal-the-trojan-is-still-live-2okf)

The public references were checked through 25 October 2026 for this editorial
revision. The novelty discussion distinguishes earlier direct reporting from
later, non-independent follow-up coverage. Historical infrastructure was not
contacted, and the case evidence cutoff remains 24 July 2026. The first-person passages describe the documented investigation;
they do not invent a compromise, a successful payload execution or a personal
interaction with an operator.

## Publication files

The numbered Markdown files are the articles. PNG diagrams and captions are
included; the figures are analytical reconstructions, not victim screenshots.
The hosted site preserves the relative links between articles, images, and
supporting PDFs. No DOI or journal publication date is claimed for the article
series; the separate preprint has a Zenodo record.

The supporting PDFs are edited reports derived from restricted evidence. They do
not contain the raw databases or a complete forensic sample set. The ZIP includes
the fourteen articles, this index, both reference pages, validation notes, diagrams,
the preprint, evidence PDFs linked from the published material, and a checksum file. Current
detection rules and tests are maintained in the companion repository.

[Scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) · [Validation record](VALIDATION.md) · [Technical paper](../preprint/UNK_DeadDrop-Preprint.pdf)
