---
title: "From Commit Metadata to a Developer Target List"
description: "Reconstructing the harvester, sender configuration and aggregate counts behind two SQLite targeting pools."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/07-developer-target-harvesting/"
kicker: "UNK_DeadDrop · Part 7"
tags:
  - "UNK_DeadDrop"
  - "targeting"
  - "GitHub"
  - "SQLite"
og_image_alt: "From Commit Metadata to a Developer Target List"
---


The sender configuration pointed to two SQLite databases. Following those references led to harvesting code and pools containing 79,698 and 62,667 rows. Together they contain 142,365 distinct stored address strings associated with 27,698 repository values. The worker, configuration and read-only count records are summarized in [E08](../preprint/evidence/E08.pdf). The harvesting code collected those addresses from public commit metadata for use by the sender tooling.

## One harvester fed two address pools

The harvester searches repositories by star range, walks their branches and extracts author and committer addresses. It lowercases and trims them before filtering, and visits up to twenty branches per repository in the recorded implementation. Worker configurations partition the search; scheduler and merge code consolidate results into two master pools. MITRE ATT&CK classifies this reconnaissance as [gathering victim email addresses (T1589.002)](https://attack.mitre.org/techniques/T1589/002/). The SQLite relation is simple:

```text
emails
  email: stored address
  repo: associated repository value
```

The sender configuration refers to both pools. Different intervals, cooldowns and warm-up settings control how the tools consume them. The toolkit names the two pools `safe` and `antispam`.

The database references connect harvesting to message preparation. No send logs were recovered to establish which addresses received messages.

![Two pools, two different counting problems](assets/07-targeting.png)

*Figure 1. The address sets are disjoint, while repository values overlap between the two pools.*

### 142,365 distinct address strings

The two databases share some repository values. A SQL union counts each value once across both pools. Read-only aggregate queries on 23 October found:

- 79,698 rows in the safe pool;
- 62,667 rows in the antispam pool;
- an exact address overlap of zero between them;
- 142,365 distinct address strings across both;
- 27,698 distinct repository values across both.

The queries check address overlap and count the combined repository values:

```sql
-- Address overlap
SELECT count(*)
FROM main.emails AS s
JOIN other.emails AS a ON s.email = a.email;

-- Combined repository values
SELECT count(*) FROM (
  SELECT repo FROM main.emails
  UNION
  SELECT repo FROM other.emails
);
```

In this comparison, the stored address sets are disjoint but the repository sets overlap. Adding the two repository counts would therefore overcount.

The queries compare stored strings without additional address canonicalization or identity resolution. Aliases and multiple addresses belonging to one person remain separate entries.

The sender code configures `mail.privateemail.com` through variables carrying a `ZOHO` prefix. That is a toolkit setting, not proof that this campaign used the service. Retained message headers show Mailgun VERP envelope behavior for the D2S and Category Labs messages. The Nodit message used its own domain in the envelope.

A forwarding service obscured the original sending IP, so its relay address is not attributed to the operators. The [indicator reference](historical-indicators.md) records the observed sender and tracking-domain details, with the limits of each observation.

### Star ranges divided the repository search

The three worker configurations each query a different band of repository star counts: `stars:101..137`, `stars:138..174` and `stars:175..210`. None specifies a language, topic, keyword or organization. The harvester therefore searches public repositories across those bands instead of selecting a particular kind of developer.

Of the 27,698 repository values, 595 (2.1 percent) have names suggesting 3D or graphics work, such as Blender, Unity, Unreal, WebGL, shaders or rendering. That count comes from repository names alone. The `3dscenebox[.]online` lure in [Part 1](01-clickfix-clipboard-manipulation.md) initially looked like a campaign against 3D artists, but the harvester shows no separate sourcing channel for that group. The evidence fits a new cover story sent to the same broad pool.

## Three repositories carried delivery kits

The five accounts active in July held 172 public repositories. I reviewed cached metadata and file trees, then classified repositories by language, project type and apparent role. Twelve repositories had directly evidenced operational roles:

- Three repositories carried delivery kits: two weaponised project copies in [Part 2](02-vsix-editor-execution.md) and the ECHOES branch in [Part 9](09-echoes-lineage-image-provenance.md).
- Three were clean take-home assignments whose weaponised versions were delivered separately.
- Five were lure funnels.
- One held the harvesting and sending toolkit.

Seven others were forks of third-party projects, including two AI coding tools. The catalogue labels 152 repositories as credibility props based on their names, file layouts and creation patterns. It separately flags one more prop for an encrypted `.env`, bringing the total to 172.

The credibility props include NFT marketplaces, staking programs, dice and coinflip games, trading bots, pump.fun clones and small "GPT" tools. They use the Rust, TypeScript and Python stack expected of a Solana or EVM contractor. Together, the 153 props make up roughly nine in ten repositories, giving each account the appearance of an active engineer's portfolio.

The creation dates show how some of the accounts were built. On the flagship account, 67 of 90 repositories appeared within five days in April 2024. A second persona account had been dormant since 2017, then received 68 repositories between 27 June and 1 July 2025. Three had exact byte-size matches under new names on the flagship account.

`pridnet` forked five real trading and LLM projects in March 2026, went quiet for 68 days, then published the weaponised assessment repository. `Lyracartoon` held only its two weaponised repositories. A byte-level sweep using two methods found operator indicators only in the known weaponised copies.

The other signature hits were false positives I checked by reading the files: a benign clipboard helper copied the text it displayed, and a marker matched inside the word `bogus` in a fork of Aider. Seven install hooks belonged to ordinary build tooling. The credibility repositories carried no payload, but their apparent activity could make a recruiter seem trustworthy.

## A public contract repo directed questions to a private contact

Five of the repositories invert the recruitment model, so that the developer is drawn in rather than written to. The most visible, a "pump.fun-compatible" Solana contract with 128 stars and about fifty forks, implements initialization and liquidity provision. Its fund-moving `remove_liquidity` handler, however, has been reduced to a stub:

```rust
pub fn remove_liquidity(/* ... */) -> Result<()> {
    // If you want to Interact with CPI, then plz contact to me.
    Ok(())
}
```

The repository's pull requests show the pool-removal and migration code being written, then withheld from the public version. That makes the missing code deliberate rather than unfinished. The README, contribution guide, `SECURITY.md` and API documentation direct questions to the same Telegram contact listed in the operators' portfolio material.

An issue from a user who hit the missing module shows the stub at work. Eight inspected forks contain the same 942-byte stub, and none publishes a working version. This suggests the full code was offered privately to people who asked. The public repository has registry-only dependencies, no install hooks, no editor configuration and no hard-coded operator key.

The contents of a private version remain unknown. It might add authority over deployed pools, include a developer-machine payload, or be ordinary paid contract work; the evidence cannot distinguish among these possibilities. Obtaining it would require engaging the operators.

The public repository names a real 2024 launchpad as its homepage. A second operator repository describes its Solidity contract as written for the same site. The project had its own public team, on-chain program and deployer authorities. None matches a wallet in the operator set.

The link supports contract work for the launchpad, not ownership of it. The domain's later re-registration served an unrelated site.

## No message logs or endpoint records were recovered

The code and configuration connect harvesting to message preparation. The databases quantify the stored contact material. Neither supplies the missing send logs, delivery outcomes or endpoint evidence needed to count people contacted or compromised. Even the repository total describes stored values rather than a fresh verification of repository existence or ownership.

The [administration frontend](08-administration-platform.md) contains mail and wallet views, but its connection to these particular SQLite pools remains unverified.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
