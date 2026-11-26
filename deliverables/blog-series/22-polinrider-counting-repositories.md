---
title: "What 2,301 Affected Accounts Actually Means"
description: "Five code-search passes give a floor of at least 2,301 GitHub accounts whose repositories carry PolinRider's launcher, and the differences between the passes say as much about search as about spread."
date: "2026-11-26"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/22-polinrider-counting-repositories/"
kicker: "PolinRider · Part 5"
tags:
  - "PolinRider"
  - "measurement"
  - "code search"
  - "software supply chain"
og_image_alt: "Five code-search passes for PolinRider launchers between 6 and 11 November 2026"
---

Five code-search passes that I ran between 6 and 11 November returned 310, 537, 1,809, 1,908 and 1,862 accounts whose public repositories carry a PolinRider launcher, and their union, recounted from the saved lists, gives a floor of at least 2,301 accounts in about 6,900 repositories. That is a count of accounts, and it is a lower bound. It does not count infected computers, people who ran the loader, or thefts, because one account can own dozens of affected repositories, one repository can be cloned by people I cannot see, and public code search shows only part of what exists. The number still matters, since it shows that the kit spread far beyond the take-home assessment where I found it, but it carries meaning only together with the definition that produced it and with the reasons the five passes disagree as much as they do, and those reasons turned out to be the most instructive part of the measurement.

## What counts as a launcher

Counting by filename would have failed from the start, for the reasons [Part 4](21-polinrider-repository-spread.md) describes, so every pass counts by behavior. An editor task is a launcher when it is triggered automatically on folder open, directly or through a `dependsOn` chain from such a task, and runs with Node, directly or through a helper script it calls, a file whose path contains `public/fonts/` at any depth. The launcher takes four forms in the wild: an inline command from the repository root, an inline command whose file sits deep in a nested tree, a `node` command with the path passed as a separate argument, and a helper script such as `eslint-check.sh` reached from the task. The first two passes covered only the root inline form and the helper, which turned out to be a small minority, while passes three to five covered all four, and pass three split its queries by file size to get under the search engine's result caps.

Before computing any figure I set aside matches whose file is not a launcher at all: twelve repositories in eleven accounts belonging to scanners, cleanup tools, test fixtures and detection rules that quote the launcher in order to find or remove it. Ten of those accounts hold nothing else and are removed whole. The eleventh also holds genuine launcher repositories, seven across the five passes, so it stays in the count with them. Accounts were de-duplicated without regard to letter case before taking the union. The passes look like this:

| Pass | Date | Launcher forms covered | Repositories | Accounts |
|---|---|---|---:|---:|
| 1 | 6 Nov | root inline; helper script | about 495 plus helper hits | 310 |
| 2 | 6 Nov | root inline; helper script | 996 | 537 |
| 3 | 7 Nov | all four, size-split queries | 5,418 | 1,809 |
| 4 | 8 Nov | all four | 5,946 | 1,908 |
| 5 | 11 Nov | all four | 5,715 | 1,862 |
| Union | | | about 6,900 | at least 2,301 |

## Why no single pass is the answer

The rows overlap heavily, so adding them would count most accounts several times, and yet no single row approaches the union. The third pass, despite covering every form, returned only 85 of the 507 repositories that the first searches had found on 6 November and missed 395 accounts that earlier passes had seen. The fifth pass returned fewer repositories than the fourth, with 477 of the fourth's repositories absent three days later, and nothing suggests that those repositories had been cleaned in the meantime. Code search caps its results, indexes neither forks nor private repositories, and appears to collapse identical files, since several launcher builds stop at exactly a hundred repositories. Each pass therefore samples an index rather than the population, and only the union of differently shaped queries comes close to it. Within the third pass the most common executed file was `fa-brand-400.orc`, in 2,409 repositories once three defender fixtures were excluded, a filename no font-based rule would ever have guessed.

The same caution applies to growth. A later pass that finds more repositories is not automatically evidence of new spread, because splitting queries by file size recovered candidates that a single capped query could not, and searching nested paths recovered repositories that earlier signatures could not match. None of those improvements dates the original malicious change, and code search returns no push times at all, which [Part 4](21-polinrider-repository-spread.md) shows to be the only reliable clock for this kit. Without stable definitions and retained timestamps, a better search looks like an outbreak and a worse one looks like a successful cleanup.

## Public counts measure a different net

Published figures are of the same order. OpenSourceMalware reported 675 repositories across 352 owners on [8 March](https://opensourcemalware.com/blog/polinrider-dprk-compromised-hundreds-of-github-repos), 1,951 across 1,047 owners on [12 April](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github) and 4,367 across 2,152 owners on [15 July 2026](https://opensourcemalware.com/blog/polinrider-blast-radius-grows). It is tempting to draw a line through those points and my November floor and call it a growth curve, but the searches behind them differ in coverage, and the nested inline form, which carries most of the population, was matched neither by the earlier public signatures nor by my own first root-anchored searches. Any count from a search that did not cover that form misses most of the population, so differences between the series measure the nets as much as the fish, and I make no estimate of growth from them.

## Builds are not loaders

Counting the launcher files themselves raises a parallel trap. A 996-repository sample from 6 November contained thirty distinct launcher builds, identified by the git hash of the task file, with new builds first pushed every one to three weeks between 2 September and 4 November, while older builds stayed in circulation; up to ten large builds had victims pushing in the same weeks, so the kit is extended with parallel variants rather than replaced on a cycle. A build, however, is not a loader. Of the nineteen builds absent from an earlier 67-repository sample, seventeen yielded a payload, and those seventeen payloads were only twelve distinct files of 12.8 to 40.3 KB: three builds run the same 12,797-byte file under two invented names, and three further pairs share one payload each. The launcher, the filename and the payload vary independently, so a new launcher hash does not announce a new malware build, and thousands of distinct task-file hashes in a broad search can come from paths and surrounding configuration rather than from new code.

## A population that is not the victims

One more number from this case looks like a victim count and is not. On 3 November a batch of 1,161 Ethereum wallets was emptied in a single scripted run into wallets connected to the resolver's funding. It would be easy to read that batch as 1,161 PolinRider victims, but the sweeps did not follow the weekly curve of launcher pushes, the wallets behave like one airdrop farmer's stored keys, and I read the batch as a stolen key store emptied in one go rather than as a measure of this operation's infections. Wallet keys, repository accounts and infected machines are three different populations, and only the second can be counted from outside, which is why I report it as a floor with its definition attached. [Part 6](23-polinrider-detection.md) uses what the counting taught me about forms and disguises to describe detection that does not depend on a filename, and [Part 7](24-polinrider-money.md) returns to the drained wallets.
