---
title: "Tracing the ECHOES Archive: Payload Lineage and Image Provenance"
description: "Four revisions of the ECHOES lure archive, a final payload that was never recovered, and C2PA data in its poster that records an AI image pipeline."
date: "2026-11-26"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/09-echoes-lineage-image-provenance/"
kicker: "UNK_DeadDrop · Part 9"
tags:
  - "UNK_DeadDrop"
  - "ECHOES"
  - "C2PA"
  - "image provenance"
  - "malware lineage"
og_image_alt: "Diagram of the four retained ECHOES archive revisions"
---


I traced four revisions of the ECHOES lure archive, which reused the same artwork and staging while its repository destinations changed. The final PowerShell payload was never recovered, and the poster's C2PA metadata records an AI image pipeline but no identity.

## Key takeaways

- The ECHOES repository history preserves four distinct archive revisions from 5, 17 and 25 March 2026, and the third revision added a VBS persistence layer.
- The final PowerShell resources sit in private repositories reachable only with the embedded token, so no crawler, scanner or token-less sandbox can have captured them.
- A related staging repository holds a four-part PowerShell toolkit that collects wallet files, decrypts browser credentials, logs keystrokes and uploads the results through GitHub's contents API.
- The toolkit's fixed, self-identifying container format decrypts statically and is a more durable detection handle than blocking `api.github[.]com`.
- The poster's C2PA fields name ChatGPT, GPT-4o and OpenAI / Sora signing references, but they contain no identity for the person who generated or distributed it.

## Delivery: a passworded archive with a shortcut inside

The ECHOES lure paired an animation-project theme with a password-protected archive. Its repository history preserved four versions of the delivery kit. The artwork and staging structure stayed recognizable as repository destinations changed. The third revision added a persistence-related script, which the fourth retained.

The delivery repository was `github[.]com/Lyracartoon/Echoes-of-the-Unborn-Sun`, reported live on 23 July 2026. [Exhibit E11](../preprint/evidence/E11.pdf) records the retained archive revisions. The final PowerShell resource was unavailable, so its final payload cannot be compared with the ClickFix or VSIX payloads.

The retained current RAR has SHA-256 `7db6789c09e29305c728bf3d7b94c5ef1c3e13eef1b321ee52d3ae3997731f56`. Its LNK member has SHA-256 `a44068e9758262a65861b91f2b00d0a3eca019d3b35543dd60c1c7f2e0ba1952`. The [artifact reference](artifact-reference.md) also lists the earlier archive revisions, LNKs and analyst-decoded stage-two hashes.

### The entry chain

The archive holds a `.pdf.lnk` shortcut whose arguments carry an encoded first stage. The chain then runs as follows:

1. The first stage decrypts to a PowerShell second stage.
2. The second stage relaunches itself hidden and elevates.
3. It opens a decoy PDF.
4. It installs scheduled-task and script persistence firing at startup and hourly.
5. It pulls two further stages from the same GitHub account using a hard-coded access token.
6. It deletes itself.

Repository-held retrieval settings change across revisions. ClickFix instead relies on a pasted command, and the VSIX route relies on editor tasks and extension installation. Their shared use of repository staging does not make their downstream capabilities interchangeable.

### One account, two delivery kits

The delivery repositories do have a documented connection. The restricted catalog of 172 public repositories examined on 24 July placed ECHOES and the weaponized `predict-together` copy under the same account. Those two and one further assessment repository were the only three catalogd repositories carrying delivery kits. The catalog is discussed in the [paper](../preprint/UNK_DeadDrop-Preprint.pdf) but is not reproduced in the public evidence exhibits.

That connects account control and delivery staging, not the missing final payload. One delivery account ran two delivery kits, the folder-open repository and ECHOES. ECHOES contributes a distinct entry route.

## Lineage: four archive revisions from March

I compared four archive revisions: one from 5 March, one from 17 March and two from 25 March 2026. The comparison followed the decoy images and encoding structure, then checked retrieval settings and task tags. In order, with all times in UTC:

1. `03f1795d`, 5 March, 06:17: the earliest retained retrieval configuration, with a DDD task tag.
2. `ded13153`, 17 March, 05:14: a different account and repository destination.
3. `b209f365`, 25 March, 03:54: another repository destination, with the tag changed to WORD and a VBS persistence layer added.
4. `4b6ea6b2`, 25 March, 13:29: a further destination change and a new access token, with the staging otherwise unchanged.

The third revision changed both retrieval and persistence. The fourth retained that staging while replacing the destination and access token. The embedded tokens were not used to retrieve the final stage, and their values are withheld.

A later review of the delivery repository found a fifth archive commit, made about two hours after the first with the same destination, token and decoys. It is a cosmetic re-compression that leaves the four distinct configurations standing.

![Four retained ECHOES archive revisions](assets/07-echoes.png)

*Figure 1. ECHOES changed retrieval destinations across four revisions and added a VBS persistence layer in the third.*

### The kit is reused with other lures

The kit was not unique to this lure. [FortiGuard Labs had documented the same LNK and GitHub chain](https://www.fortinet.com/blog/threat-research/dprk-related-campaigns-with-lnk-and-github-c2) on 2 April 2026 with Korean business lures in place of the animation pitch. FortiGuard named one of the C2 accounts in my record among its own, so the operator varies the lure while reusing the toolchain.

The Hangul decoy metadata and the token-based C2 are consistent with Proofpoint's assessment that the operation is very likely North Korea-aligned and with FortiGuard's DPRK framing. These remain those publishers' assessments rather than mine.

## Payload: the final PowerShell stage was not recovered

The staging references led to final PowerShell resources unavailable through the unauthenticated routes. That absence follows from the design rather than from bad luck: the files sit in private repositories reachable only with the embedded token, so no crawler, scanner or token-less sandbox can have captured them.

My hunt of 23 July covered the account cluster on the forge, stored URL-scanner scans, VirusTotal, MalwareBazaar and the Open Threat Exchange without a hit. FortiGuard did not publish stage-three hashes either. No final payload was available for capability analysis.

### The closest counterpart: a four-part PowerShell toolkit

The closest counterpart came from a separate public staging repository linked to the same operator personas. It carries the same retrieval header and, in its first revision, the same account and token as the final ECHOES archive. It holds scripts dated 31 March to 10 April that decrypt with parameters stored beside them.

I read the scripts statically and never ran them. They form a four-part toolkit that:

- collects wallet application folders and files named for seeds, private keys and recovery codes;
- decrypts browser credentials, including through the App-Bound encryption bypass and, new to the investigation, Volume Shadow Copy reads of locked browser databases;
- runs a keylogger and clipboard logger through a VBScript runner;
- uploads through GitHub's contents API into a private repository named after each victim's user and machine.

That egress is ordinary TLS to `api.github[.]com`, so blocking it by destination would also block legitimate GitHub use. The toolkit's fixed, self-identifying container format decrypts statically and is a durable detection handle.

It also settles a smaller question from [Part 4](04-credential-wallet-collection.md). The Overlord agents and their Node and Python stages log no keys, but the operator's separate PowerShell toolkit does. These scripts show the operator's tooling rather than what the March archives fetched, since those exact bytes were never retained. Nothing in them shows that any victim was affected.

### Account status

Account status was less clear than a 404 suggested. One historical check found an unavailable account whose name was also unavailable for registration. That supports a suspension hypothesis but does not confirm it with the platform.

Neighboring numeric identifiers showed no distinctive batch-registration pattern, and consecutive IDs can belong to unrelated signups. Proving common registration control would require unavailable platform data.

## Provenance: C2PA metadata in the poster

I also examined the retained decoy artwork. The poster, identified in the case as `Post.png`, contained a [C2PA](https://c2pa.org/specifications/) structure in its PNG `caBX` chunk. [Exhibit E14](../preprint/evidence/E14.pdf) records the retained metadata and signature examination. I extracted the metadata and parsed its JUMBF and CBOR structures, including the embedded certificates. The fields read:

```text
Claim generator:  ChatGPT
Software agent:   GPT-4o
Source type:      trainedAlgorithmicMedia

Recorded certificate subject fields:
OpenAI / Sora signing-pipeline references
```

The manifest history records creation, conversion and ingredient-opening actions across two manifests. Its embedded thumbnail was described as a lower-resolution version of the poster. The fields describe an image pipeline. They contain no identity for the person who generated or distributed the poster.

### Signature validation is not independently verified

The original note reports successful signature validation. The retained record lacks independent verifier output and certificate-status or trust-list checks. An embedded ingredient-validation assertion is not independent verification of the later manifest.

### No prompt, no user, no proof of removal

The manifest contains no prompt or user identifier, and its redacted-assertions array is empty. Those fields may never have been included, and an empty redaction list is not evidence that information was removed.

Other portraits lacked the poster's C2PA structure. Re-encoding or a different export path could explain the difference, as could a different source image. Intentional metadata removal remains unverified.

### C2PA certificate validity ran from April 2025 to April 2026

The leaf certificate was valid from 15 April 2025 to 15 April 2026, and the examination found no trusted timestamp token. Signing and generation times remain unknown. Repository commits date when the image appears in preserved history, not when it was created.

The PNG examination found no bytes after the end marker, though other hiding methods were outside that check.

## Limitations

- The final PowerShell payload was never recovered, so ECHOES capability cannot be compared with the ClickFix or VSIX payloads.
- The PowerShell toolkit is a related counterpart, not the bytes the March archives fetched, and it shows no affected victim.
- The C2PA signature validation lacks independent verifier output and certificate-status or trust-list checks.
- Signing and generation times of the poster remain unknown.

## Conclusion

ECHOES shows an operator who rotates repository destinations and tokens while keeping one LNK and GitHub toolchain, and who varies the lure around it. The design keeps the final stage behind a token, which explains why no public service holds it.

For defenders, the toolkit's self-identifying container format is a better handle than the GitHub egress destination, which legitimate use shares. The poster's C2PA data identifies an image pipeline, not a person, and should be read that way.
