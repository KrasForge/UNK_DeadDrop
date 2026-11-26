---
title: "Following a Developer from UNK_DeadDrop to PolinRider"
description: "A second take-home assessment in one developer's account ran an extra file before the application started, and that file belonged to a different operation with its own delivery, resolver and hosting."
lastUpdated: 2026-11-26
sidebar:
  order: 18
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/18.png"
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
      content: "Part 18: Following a Developer from UNK_DeadDrop to PolinRider"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/18.png"
---


I found an obfuscated Node loader in one developer's copy of a Hiring777 take-home assessment, started by an extra `init` step before the application itself. It reads its next server from the recipient field of an Ethereum transaction, and it belongs to PolinRider, an operation separate from UNK_DeadDrop.

## Key takeaways

- Of 28 matching repositories across 25 accounts, exactly one carries the dropper; the recruiter's copies and every other candidate copy pushed between May and October were clean.
- I recovered the loader statically, all 372 of its strings at all 538 of its decoder call sites, and nothing in it crossed to the UNK_DeadDrop operator.
- The campaign name, its resolver branches, the later stealer stages and the attribution come from prior reporting; my additions include a third resolver wallet that appears in no report I have found.
- A shared victim and a shared folder-open technique are not links between the operations, and the attributions stay with OpenSourceMalware, Socket and MITRE.
- Defenders should look for an extensionless `init` file and a `node init` command prepended to development, build and start scripts, not for the obvious strings, which return hundreds of unrelated code-search hits.

## Delivery: an extra step before the application starts

In early November I was checking where copies of one UNK_DeadDrop take-home assessment had gone. One of the developers concerned had also published a second, unrelated recruitment exercise: a copy-trading project whose backend and frontend start scripts both ran an extra file called `init` before the application itself.

The assessment came from a recruiter persona called Hiring777. It was seeded from a GitHub account created on 14 May 2026 under the address `christoper929@outlook[.]com`. From mid-May that account published clean base versions of a copy-trading exercise and several related ones, with names such as `copy-trading-test`, `vaultpay-home-task`, `react-uiux-dev-test` and `smart-contract-engineer-role`.

The affected copy works as follows:

- It prepends `node init` to the ordinary development, build and start commands in all three of its package manifests.
- It places `init`, `backend/init` and `frontend/init` beside those manifests.

A candidate who simply followed the instructions therefore reached the loader while doing exactly what the exercise asked.

## Method: recovering the loader without running it

That file was not part of the operation I had spent four months documenting. It was an obfuscated Node loader that read the address of its next server from the recipient field of an Ethereum transaction. I recovered it statically, resolving all 372 of its strings and all 538 of its decoder call sites without ever running it. Nothing in it crossed to the UNK_DeadDrop operator.

This post and the five that follow describe where that loader led. This one explains why I treat what I found as a separate operation, called PolinRider in public reporting, and not as another branch of the case that the earlier parts of this series and [Part 17](../17-two-operations-one-ecosystem/) describe.

## Scope: one infected copy among 28

The danger was in one modified copy and not necessarily in the assignment as a whole. I therefore read every public repository matching the seven assessment brands across 25 accounts, the recruiter's own among them. For each one I checked:

- the file tree for an extensionless `init`;
- each `package.json` for the prepended command.

The result was narrower than I expected. About nineteen of those accounts belong to candidates who hold 26 matching copies between them, one of them probably unrelated. With the recruiter's two base copies that makes 28 repositories, of which exactly one carries the dropper.

The recruiter's own copies and every other candidate copy pushed between May and October were clean. That matters in both directions when it comes to notification. The other candidates should not be told that their copies are infected. The one affected developer's exposure dates from whenever they last ran a development, build or start script after the loader entered the submission.

The infection came through the repository rather than through a dependency. None of the 47 packages on a public toolkit list for this campaign appears in the 152 manifests and lockfiles in that developer's account.

The obvious strings turned out to be useless for finding anyone else:

- `node init` followed by a watcher or a compiler is ordinary.
- The loader's deobfuscated array identifier returns 706 code-search hits that are mostly linter configurations.
- Its stage-two path fragment returns 838 hits dominated by advisories about this very family.

## Context: a campaign that already had a name

Public reporting had already named what the loader belongs to:

- OpenSourceMalware's reports of [March](https://opensourcemalware.com/blog/polinrider-dprk-compromised-hundreds-of-github-repos), [April](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github) and [July 2026](https://opensourcemalware.com/blog/polinrider-blast-radius-grows) describe PolinRider as a campaign of obfuscated loaders injected into developer repositories. The injection came first through configuration files in compromised npm packages and later, as their [developer guide](https://opensourcemalware.com/blog/developer-guide-getting-over-polinrider) documents, through a workspace task.
- The same researchers named [NullReceiver](https://github.com/OpenSourceMalware/NullReceiver), the technique of encoding an IPv4 address in the recipient of an empty Ethereum transfer, and published one resolver wallet and one host.
- [GitGuardian](https://blog.gitguardian.com/ghostaction-x-polinrider/) described the multi-stage payload chain.
- In November, [JFrog](https://research.jfrog.com/post/accurasofthire-fake-interview/), [StepSecurity](https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines) and [Sonatype](https://www.sonatype.com/blog/polinrider-loader-reappears-in-hijacked-npm-packages) reported npm campaigns that read the same resolver wallets.

In that vocabulary, PolinRider is the campaign and NullReceiver is the resolver technique of its Ethereum branch. The file in the Hiring777 copy is a PolinRider loader delivered through a take-home exercise, an entry route that secondary reporting already lists among the campaign's methods.

### Prior work and my additions

The campaign's name, the existence of its resolver branches, the later stealer stages and the attribution all come from those publications, and I use them as such. What I added is the part that was not yet public when I started:

- a third resolver wallet that appears in no report I have found;
- the closed enumeration of all three wallets, with the shared hosts that tie them together;
- the money that pays for the resolvers;
- the loader generations of a second blockchain branch;
- the way the kit moves from one infected workstation into every repository it can reach.

Parts 2 to 6 follow those threads in order, and [Part 7](../24-polinrider-money/) follows the money in depth. Where a step in them rests on my inference rather than on a record, I say so at that step. A reader who has to separate an observation from a conclusion should not have to reconstruct the distinction from a footnote.

## Separation: why PolinRider is a separate operation

### Different at every layer

The two operations differ at every layer an operator has to build:

- **Delivery.** UNK_DeadDrop reaches developers through ClickFix pages, a malicious editor extension and repositories that run on folder open. PolinRider hides obfuscated JavaScript loaders in repositories as an extensionless `init` or a fake font file, and starts them from an npm script or a hidden editor task.
- **Resolution.** UNK_DeadDrop's payload reads its server configuration from a GitLab dead drop. PolinRider reads its server address from blockchain records.
- **Hosting.** UNK_DeadDrop's lure and server estate sat on Advin Services from July to November 2026. PolinRider's resolver hosts sat on Evoxt's AS149440 and on AS399486.

When I compared them I found no shared certificate, panel fingerprint, address, subnet or autonomous system. A path analysis over my findings ledger found no independent observational link at all. The only two paths between the blocks run through a generic string-array obfuscation rule and a bare attribution tag, and neither is an observation. Community detection over 2,218 observables placed every connected PolinRider, NullReceiver and Hiring777 record in communities that hold no UNK_DeadDrop record.

### Shared victims are not a link

What the two do share is the ecosystem and a few victims, and neither is a link. Two developers answered both fake recruiters. That is unsurprising when two crews approach the same small population of crypto-focused freelance developers, since someone who answers one fake recruiter is by that fact more likely to answer another.

One detail shows how easily a shared victim produces a false connection. The affected developer's account holds a fork of an UNK_DeadDrop take-home lure. Read naively, that fork shows an UNK_DeadDrop identity authoring a PolinRider commit. In fact its folder-open task is the lure's original weaponization inherited from upstream, and PolinRider's worm amends commits in every working copy it reaches under whoever authored them.

The repository joins the two operations only through the victim's disk. I decline that kind of overlap throughout this series, together with the shared folder-open technique and the BeaverTail, OtterCookie and InvisibleFerret family records that belong to the wider ecosystem rather than to either operation.

### Attribution stays with its publishers

Attribution follows the same discipline:

- OpenSourceMalware attributes PolinRider to North Korea and describes it as a Lazarus Group contributor.
- [Socket](https://socket.dev/blog/polinrider-north-korea-linked-supply-chain-campaign-expands) places it in the Contagious Interview, or Famous Chollima, developer-targeting campaign, which [MITRE tracks as G1052](https://attack.mitre.org/groups/G1052/).

Those are the publishers' assessments, not mine. What I can add is that Hiring777's resolver wallet shares two hosts, the same marker, the same staging paths and the same RPC list with the wallet named in OpenSourceMalware's reporting. That makes Hiring777 a live node of a reported campaign rather than an unknown actor, without showing that it is the same crew.

Google's [EtherHiding report](https://cloud.google.com/blog/topics/threat-intelligence/dprk-adopts-etherhiding) attributes the technique and the JADESNOW downloader to a cluster it calls UNC5342 and never mentions PolinRider. It supports a statement about UNC5342 and nothing about this campaign. Naming that cluster for the loader I hold would be one inferential step further than the evidence goes.

## Chronology: a date that does not fit

The assessment carries a chronology I cannot close:

1. The commit that adds the loader carries an unsigned author date in early June.
2. The Ethereum wallet the loader hard-codes received its first gas on BNB Smart Chain on 3 July.
3. The same wallet sent its first resolver transaction on 4 September.

Those dates fit a dormant implant sitting in the repository with a wallet that was generated in advance and switched on later. They equally fit a commit date that is simply misleading. As [Part 4](../21-polinrider-repository-spread/) shows, this kit is written into repositories by amending existing commits whose author dates it inherits.

The public repository cannot decide between those readings, and I do not rank them. The developer's own account of when the files were received and run would settle it. Until then I neither date the infection from that commit nor describe the gap as a confirmed dormant period.

## Conclusion

The loader gave me firmer ground than its commit did. Its recovered strings described exactly where it would look for a server, and following that lookup turned an obfuscated file into a public, dated record of the operator's infrastructure.

For defenders, the useful checks are structural rather than string-based: an extensionless `init` beside a package manifest, and `node init` prepended to development, build and start scripts. Only one of the 28 copies I read carries the dropper, so notification should go to that developer and not to every candidate who received the assignment.

[Part 2](../19-polinrider-ethereum-address-book/) explains how the Ethereum branch uses a transaction's recipient field as an address book, and how the campaign's older TRON and BNB Smart Chain branch does the same with payloads.
