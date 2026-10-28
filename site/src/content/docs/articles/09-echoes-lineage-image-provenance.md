---
title: "Tracing the ECHOES Archive: Payload Lineage and Image Provenance"
description: "Four revisions of the ECHOES lure archive, a final payload that was never recovered, and C2PA data in its poster that records an AI image pipeline."
lastUpdated: 2026-10-28
sidebar:
  order: 9
---


The ECHOES lure paired an animation-project theme with a password-protected archive. Its repository history preserved four versions of the delivery kit. The artwork and staging structure remained recognizable as repository destinations changed. The third revision added a persistence-related script, which the fourth retained.

The delivery repository was `github[.]com/Lyracartoon/Echoes-of-the-Unborn-Sun`, reported live on 23 July 2026. [Exhibit E11](../../evidence/E11.pdf) records the retained archive revisions, but the final PowerShell resource was unavailable. I therefore keep its relationship to the ClickFix and VSIX branches unresolved.

The retained current RAR has SHA-256 `7db6789c09e29305c728bf3d7b94c5ef1c3e13eef1b321ee52d3ae3997731f56`; its LNK member has SHA-256 `a44068e9758262a65861b91f2b00d0a3eca019d3b35543dd60c1c7f2e0ba1952`. The [artifact reference](../artifacts/) lists the earlier archive revisions, LNKs and analyst-decoded stage-two hashes as well.

The final PowerShell payload was unavailable, leaving its capabilities unresolved. The retained archives preserve the staging scripts and a poster whose embedded C2PA metadata records an AI image pipeline.

## Four versions of the same lure

The repository history records archive changes on 5 March, on 17 March and twice on 25 March 2026, and the retained analysis compares the repeated decoy images, encoding structure, retrieval configuration and task tags across all four. In order, with all times in UTC:

1. `03f1795d`, 5 March, 06:17: the earliest retained retrieval configuration, with a DDD task tag.
2. `ded13153`, 17 March, 05:14: a different account and repository destination.
3. `b209f365`, 25 March, 03:54: another repository destination, with the tag changed to WORD and a VBS persistence layer added.
4. `4b6ea6b2`, 25 March, 13:29: a further destination change and a new access token, with the staging otherwise unchanged.

The third revision changed both retrieval and persistence; the fourth retained that staging while replacing the destination and access token. The embedded tokens were not used to retrieve the final stage, and their values are withheld.

![Four retained ECHOES archive revisions](../assets/07-echoes.png)

*Figure 1. ECHOES changed retrieval destinations across four revisions and added a VBS persistence layer in the third.*

## Where the payload trail stopped

The staging references led to final PowerShell resources unavailable through the unauthenticated routes. No final payload was available for capability analysis.

Account status was less clear than a 404 suggested. One historical check found an unavailable account whose name was also unavailable for registration. That supports a suspension hypothesis, but does not confirm it with the platform. Neighboring numeric identifiers showed no distinctive batch-registration pattern. Consecutive IDs can belong to unrelated signups; proving common registration control would require unavailable platform data.

## The poster retained a C2PA structure

The poster, identified in the case as `Post.png`, offered a very different kind of lead, because the recorded examination found a [C2PA](https://c2pa.org/specifications/) structure in its PNG `caBX` chunk. [Exhibit E14](../../evidence/E14.pdf) records the retained metadata and signature examination. Extracting the metadata and parsing its JUMBF, CBOR and certificate structures exposed the following fields:

```text
Claim generator:  ChatGPT
Software agent:   GPT-4o
Source type:      trainedAlgorithmicMedia

Recorded certificate subject fields:
OpenAI / Sora signing-pipeline references
```

The manifest history records creation, conversion and ingredient-opening actions across two manifests. Its embedded thumbnail was described as a lower-resolution version of the poster.

The recorded examination reports successful signature validation. No subsequent certificate-status check was performed. The manifest identifies the image pipeline but contains no identity for the person who generated or distributed the poster.

The manifest contains no prompt or user identifier, and its redacted-assertions array is empty. Those fields may never have been included; an empty redaction list is not evidence that information was removed.

Other portraits examined in the case lacked the poster's C2PA structure. Re-encoding could explain that difference, but it does not prove intentional provenance removal; different export paths or source histories could produce the same result.

### Certificate validity and image dates

The leaf certificate was valid from 15 April 2025 to 15 April 2026, and the examination found no trusted timestamp token. Certificate validity does not establish when an artifact was signed or generated. Repository commits date when the image appears in preserved history, not when it was created.

The PNG examination found no data appended after the end marker; other forms of hidden content were not ruled out.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
