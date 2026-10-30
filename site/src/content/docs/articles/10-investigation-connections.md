---
title: "From Three Phishing Emails to a Connected Investigation"
description: "The pivots linking recruitment messages, delivery artifacts, payload configuration and supporting software."
lastUpdated: 2026-10-25
sidebar:
  order: 10
---



Three recruitment messages started the investigation: a Nodit-themed lure received on 22 June 2026, a D2S AI Trade lure on 21 July and a Category Labs lure on 22 July. Their links led to clipboard manipulation and editor-extension delivery routes. The collected material also included a mutable GitLab resolver, two targeting databases and administration frontend source.

Several connections are explicit in the code: a copy handler calls a command builder, a task invokes an installer, and sender configuration names database files. Other relationships rely on historical infrastructure observations or compatible functions in separately recovered software. No endpoint or backend record reconstructs a complete infection and collection sequence.

## A copy handler, an editor task, and a passworded archive

In the [browser route](../01-clickfix-clipboard-manipulation/), a verification page changes the command placed on the clipboard. Its copy handler passes a nonce, phrase and operating-system value to a builder that adds installation logic while preserving the promised `VERIFY-` output. The first-stage download location comes from the page's origin, allowing the same frontend to work on different lure hosts.

The [repository route](../02-vsix-editor-execution/) uses project task configuration to reach a VSIX installer. The Google Update Support extension reads deployment settings from workspace configuration, so the package and its settings jointly determine the configured destination. The VSIX also carries native agents and encrypted Windows components.

Authenticated decryption exposed a Windows Node/Python pipeline inside the extension. Similar COM elevation-builder code occurs in the ClickFix collector, linking the two implementations. Their entry conditions differ: one depends on a candidate pasting a command into a terminal, while the other depends on editor task permissions and extension installation.

[Proofpoint's earlier report](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) documents the extension route and Windows architecture. The recovered package corroborates those mechanisms and exposes the configuration and process-building code in detail.

The message-header review also identified Mailgun VERP envelope behavior for the D2S and Category Labs lures, while the Nodit message used its own domain in the envelope. The messages arrived through a forwarding service, so the original sending IP was not preserved. The forwarding service and its relay addresses belong to the recipient's mail path, not the campaign infrastructure. Personal addresses and envelope identifiers are omitted; the message evidence is summarized in [E01](../../evidence/E01.pdf).

![Connections need named relationships](../assets/10-evidence-map.png)

*Figure 1. Code references, configuration values and historical observations connect the recovered components.*

## Resolver edits point to two July server generations

The [GitLab resolver](../06-gitlab-dead-drop-infrastructure/) separates destination settings from deployed payloads. The retained history records changes to `config.json` and a separate `config-alt.json` file, but no retained payload references the latter. On 13 July, the referenced `config.json` set changed to `api.cklomino[.]ink` and `api.dsfmot[.]xyz` ([E07](../../evidence/E07.pdf)). A payload hash alone cannot identify which configuration a client fetched.

A certificate naming `api.cklomino[.]ink` and a Subtensor sign-in panel observed at `207.241.172[.]222` connect that address to the historical service. Passive DNS and related research-service records supplied further pivots. These observations identify dated service associations without establishing exclusive ownership of the address. Client refresh behavior and connections after the configuration change remain unknown.

The late-July lures added another dated origin picture. On 23 and 24 July, `170.205.31[.]182` served the `3dscenebox[.]online` lure and was associated with several reactivated lure domains. Separately, certificate and passive-scan records linked the `api.aazdias[.]ink` and `api.fallaazdis[.]ink` store pair to `207.241.172[.]222`. [E20](../../evidence/E20.pdf) and [E21](../../evidence/E21.pdf) document the limits of those observations; the public bundle lacks the complete provider responses.

The older `23.137.105[.]75:5173` C2 observation belongs to an earlier generation. A 22 July analyst note also records an Express response from `23.137.105[.]75:3000` and a CORS preflight allowing `X-Guard-Platform`, a header present in the recovered installer.

The 404 and preflight do not establish that a specific route existed or received data. The probe transcript is not in the public evidence PDFs, and these July observations have not been refreshed since 24 July.

The main connections are:

| Starting artifact | Connection | Result |
|---|---|---|
| Received message | Recruitment URL | A delivered lure |
| Lure source | Copy handler calls command builder | Clipboard substitution and first-stage retrieval logic |
| Project configuration | Task and deployment settings | Extension installation path and configured parameters |
| Held collector | GitLab configuration URL | Mutable destination lookup |
| Sender configuration | Paths to two SQLite pools | Stored targeting material available to the sender |
| Administration frontend | Imports and API route references | Repository monitoring and wallet-management controls |
| ECHOES repository history | Four retained archive revisions | Changes to retrieval and persistence |

The [historical indicator reference](../../indicators/) collects the exact hostnames, paths and IP observations behind these links, with the evidence type and uncertainty recorded for each. The [artifact reference](../../artifacts/) gives file hashes for the samples and archive revisions used in the pivots.

## Separate contact pools and wallet fields

The [harvester](../07-developer-target-harvesting/) searches repositories by star range and extracts author and committer addresses from branch histories. Sender configuration names two SQLite pools containing 142,365 distinct stored address strings associated with 27,698 repository values ([E08](../../evidence/E08.pdf)). The counts quantify the available targeting material. Missing send logs and endpoint records prevent a count of recipients contacted or systems compromised.

The separately recovered [rms-platform frontend](../08-administration-platform/) contains mail views, repository availability monitoring and wallet import, preview and claim controls. Its mnemonic and ColdKey fields correspond to material selected by the collectors. That connection describes compatible data and functions; no recovered backend establishes that the targeting pools, mail system and wallet workflow were integrated or used successfully.

[ECHOES](../09-echoes-lineage-image-provenance/) preserves a different delivery branch. Four archive revisions show repeated artwork and staging, changing retrieval destinations and a VBS persistence addition. Its final PowerShell payload was unavailable through the unauthenticated routes examined. The retained stages therefore cannot establish whether it deployed the Go agent, JavaScript collector or another payload.

## Three leads that fell apart on review

Several connections that looked strong in the middle of the investigation fell apart when they were checked properly. They are recorded here because each one, if left alone, would have put somebody else's infrastructure or somebody else's name into the indicator set.

The persona accounts claimed roles at real crypto projects and displayed testimonials attributed to founders and executives. At first, some project domains and authors' social handles were treated as possible operator infrastructure because they shared registrar, hosting and privacy-registration patterns with known sites.

The projects proved to be established companies with years of public history. Their testimonials used real people's names and handles, with no sign those people had written them. The evidence identifies the companies and people as targets of impersonation. Their domains do not belong on a certificate watch list, and their names are omitted here.

The shared hosting fingerprint was common. A budget registrar, popular host and privacy service are not enough to connect a domain to an operation.

Most of this domain family was registered in September 2025 and hosted by the same budget provider. It was first treated as an earlier campaign phase, then reclassified the same day as probable operator infrastructure with high confidence.

Closer inspection found at least six beauty and cosmetics domains, about forty subdomains per domain named for invented Brazilian influencers, numbered bulk-mail sender subdomains and spam classifications. The sites formed an affiliate-marketing spam operation. They had no recruitment lure, ClickFix page or malware.

The "dedicated host" claim came from one passive-DNS source with limited coverage. Another address used by the family hosted unrelated sites for years. The association was withdrawn before any indicator set or referral was filed.

The 3D-artist lead in [Part 7](../07-developer-target-harvesting/) came from a new cover story. The harvester shows no separate sourcing channel for that audience. The operator-associated Solana wallets active into 2026 led through one pass-through account to a program-owned account holding thousands of SOL and handling hundreds of transactions each day. The trace found no victim funds.

The broader repository sweep returned two signature matches. Reading the files showed both were benign.

## The July report and an October continuation lead

Ben Hopkins's [UNK_DeadDrop investigation](https://brhopkins.uk/posts/foxtopia/) first appeared on 23 July, before this case's evidence cutoff, and was updated in August. The update places `api.chestsoi[.]ink` in the GitLab dead-drop sequence. That hostname does not appear in the resolver history retained here, so it remains a reported lead rather than a captured indicator.

An [October developer-lure report](https://dev.to/edison_flores_6d2cd381b13/a-fake-recruiter-sent-me-a-job-offer-that-ended-in-my-terminal-the-trojan-is-still-live-2okf) describes a launcher with four markers also found in this corpus: `deepfake_guard`, a POSIX double-fork, `/var/tmp/.kdm.XXXXXX` and `/guard-launcher-result`. It names `taikotalent[.]xyz`, the paired hosts `api.gaganata[.]ink` and `api.fallgganata[.]ink`, and sample SHA-256 `c7c22e322c17bda8198257342d4034af6250a5c433242461b870879ba9aa285d`.

The shared markers make this a probable continuation lead. The article, gist, repository and follow-up all trace to one reporting chain, and the sample was not independently recovered. The hosts and hash therefore remain leads, not verified indicators.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
