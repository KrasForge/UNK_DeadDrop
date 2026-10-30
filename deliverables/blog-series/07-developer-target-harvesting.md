---
title: "Two SQLite pools held 142,365 address strings"
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

The sender code configures `mail.privateemail.com` through variables carrying a `ZOHO` prefix. That is a toolkit setting, not proof that this campaign used the service. Retained message headers instead show Mailgun VERP envelope behavior for the D2S and Category Labs messages; the Nodit message used its own domain in the envelope. A forwarding service obscured the original sending IP, so its relay address is not attributed to the operators. The [indicator reference](historical-indicators.md) records the observed sender and tracking-domain details, with the limits of each observation.

### Star ranges divided the repository search

The three worker configurations each carry a single search query, a band of star counts (`stars:101..137`, `stars:138..174` and `stars:175..210`), with no language, topic, keyword or organization qualifier. The harvester is therefore sweeping every public repository in a mid-popularity range rather than looking for a particular kind of developer. A read of the repository column alone, without opening any address, puts this in numbers: of the 27,698 repository values, 595, or 2.1 percent, have names that suggest 3D or graphics work such as Blender, Unity, Unreal, WebGL, shaders or rendering. That matters for the `3dscenebox[.]online` lure in [Part 1](01-clickfix-clipboard-manipulation.md), which looked at first like the front end of a new campaign against 3D artists. The harvester shows no sourcing channel for such a campaign. The Scene Box page is better read as a new cover story offered to the same broad pool, so there is no separate artist community to warn beyond the developers already in it.

## Three repositories carried delivery kits

The sender tooling and both pools sit in one repository, but the five operator accounts that were live in July held 172 public repositories between them. Each was characterized offline from cached metadata and full file trees by language, project type and role in the operation. Twelve of those labels rest on direct evidence. Three repositories carry the delivery chain: the two weaponised project copies in [Part 2](02-vsix-editor-execution.md) and the ECHOES branch in [Part 9](09-echoes-lineage-image-provenance.md). Three are clean take-home assignments whose weaponised versions are delivered separately. Five are lure funnels of the kind described below. Seven are forks of real third-party projects, including two AI coding tools, and one is the harvesting and sending toolkit. The remaining 152 are labeled credibility props by inference from their names, file layouts and creation pattern, because their apparent purpose is to make each persona look like a busy Solana or EVM contractor. They are NFT marketplaces, staking programs, dice and coinflip games, trading bots, pump.fun clones and small "GPT" tools, written in the Rust, TypeScript and Python stack that such a contractor would show. Roughly nine in ten repositories exist to answer a cautious candidate's first question, whether the recruiter is a real engineer, with a wall of plausible activity.

The creation dates make the staging visible. On the flagship account, 67 of its 90 repositories were created in five days in April 2024. A second persona account, dormant since 2017, received 68 repositories between 27 June and 1 July 2025, and three of them have exact byte-size matches under new names with repositories on the flagship account. `pridnet` forked five real trading and LLM projects in March 2026, went quiet for 68 days and then published the weaponised assessment repository. `Lyracartoon` held only its two weaponised repositories, the disposable end of the same model. A byte-level content sweep of all 172 repositories, run with two separate methods, found operator indicators only in the known weaponised copies. Its only other signature hits were false positives that I checked by reading the files: a benign clipboard helper that copies the same text it displays, and a marker string matched inside the word `bogus` in a fork of the real Aider tool. Seven install hooks belonged to ordinary build tooling. The props carry no payload, but they are not harmless, because a stranger who clones a plausible launchpad on the strength of the account's apparent history is trusting the same reputation the lures borrow.

## A public contract repo directed questions to a private contact

Five of the repositories invert the recruitment model, so that the developer is drawn in rather than written to. The most visible, a "pump.fun-compatible" Solana contract with 128 stars and about fifty forks, implements initialization and liquidity provision. Its fund-moving `remove_liquidity` handler, however, has been reduced to a stub:

```rust
pub fn remove_liquidity(/* ... */) -> Result<()> {
    // If you want to Interact with CPI, then plz contact to me.
    Ok(())
}
```

The repository's own pull requests show the full pool-removal and migration code being written and then withheld from the public version, so the gap is deliberate rather than unfinished work. The README, contribution guide, `SECURITY.md` and API documentation all route questions to the same Telegram contact that appears in the operators' portfolio material. An issue filed by an outside user who hit the missing module shows the stub doing its job. The eight forks I checked carry the identical 942-byte stub, and none republishes a working version, which suggests that the complete code is handed over privately to people who ask for it. The public code is otherwise clean, with registry-only dependencies, no install hooks, no editor configuration and no hard-coded operator key.

What the private version contains cannot be established from outside, and obtaining it would mean engaging the operators. It could carry a hidden authority over deployed pools, a developer-machine payload, or nothing more than paid contract work, and the evidence does not choose between them. One limit deserves stating. The repository names a real 2024 launchpad as its homepage, and a second operator repository describes its Solidity contract as written for that site. That project had its own public team and its own on-chain program and deployer authorities, and none of them matches a wallet in the operator set. The link supports contract development work for that launchpad, not ownership of it, and the domain's later re-registration served no launchpad at all.

## No message logs or endpoint records were recovered

The code and configuration connect harvesting to message preparation. The databases quantify the stored contact material. Neither supplies the missing send logs, delivery outcomes or endpoint evidence needed to count people contacted or compromised. Even the repository total describes stored values rather than a fresh verification of repository existence or ownership.

The [administration frontend](08-administration-platform.md) contains mail and wallet views, but its connection to these particular SQLite pools remains unverified.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
