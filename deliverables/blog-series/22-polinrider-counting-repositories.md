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

I ran five code-search passes between 6 and 11 November and found at least 2,301 GitHub accounts, in about 6,900 repositories, whose public repositories carry a PolinRider launcher. That is a lower bound on accounts, and the differences between the passes say as much about search as about spread.

## Key takeaways

- Five passes returned 310, 537, 1,809, 1,908 and 1,862 accounts; their union, recounted from the saved lists, is at least 2,301 accounts in about 6,900 repositories.
- The figure counts accounts only, not infected computers, people who ran the loader, or thefts.
- No single pass approaches the union: code search caps results, skips forks and private repositories, and appears to collapse identical files.
- A larger later count is not evidence of new spread, and published counts from searches with different coverage cannot be joined into a growth curve.
- Launcher builds, filenames and payloads vary independently; seventeen builds yielded only twelve distinct payload files.

## Scope: what the number means

The number shows that the kit spread far beyond the take-home assessment where I found it. It is a count of accounts, and it is a lower bound. It does not count infected computers, people who ran the loader, or thefts:

- one account can own dozens of affected repositories;
- one repository can be cloned by people I cannot see;
- public code search shows only part of what exists.

The number carries meaning only together with the definition that produced it and the reasons the five passes disagree. Those reasons turned out to be the most instructive part of the measurement.

## Method: counting by behavior, not filename

Counting by filename would have failed from the start, for the reasons [Part 4](21-polinrider-repository-spread.md) describes, so every pass counts by behavior. An editor task is a launcher when it meets two conditions:

- it is triggered automatically on folder open, directly or through a `dependsOn` chain from such a task;
- it runs with Node, directly or through a helper script it calls, a file whose path contains `public/fonts/` at any depth.

The launcher takes four forms in the wild:

- an inline command from the repository root;
- an inline command whose file sits deep in a nested tree;
- a `node` command with the path passed as a separate argument;
- a helper script such as `eslint-check.sh` reached from the task.

The first two passes covered only the root inline form and the helper, which turned out to be a small minority. Passes three to five covered all four, and pass three split its queries by file size to get under the search engine's result caps.

### Exclusions and de-duplication

Before computing any figure I set aside matches whose file is not a launcher at all. These were twelve repositories in eleven accounts belonging to scanners, cleanup tools, test fixtures and detection rules that quote the launcher in order to find or remove it. Ten of those accounts hold nothing else and are removed whole. The eleventh also holds genuine launcher repositories, seven across the five passes, so it stays in the count with them. I de-duplicated accounts without regard to letter case before taking the union.

### The five passes

| Pass | Date | Launcher forms covered | Repositories | Accounts |
|---|---|---|---:|---:|
| 1 | 6 Nov | root inline; helper script | about 495 plus helper hits | 310 |
| 2 | 6 Nov | root inline; helper script | 996 | 537 |
| 3 | 7 Nov | all four, size-split queries | 5,418 | 1,809 |
| 4 | 8 Nov | all four | 5,946 | 1,908 |
| 5 | 11 Nov | all four | 5,715 | 1,862 |
| Union | | | about 6,900 | at least 2,301 |

## Results: why no single pass is the answer

The rows overlap heavily, so adding them would count most accounts several times. Yet no single row approaches the union.

- The third pass, despite covering every form, returned only 85 of the 507 repositories that the first searches had found on 6 November and missed 395 accounts that earlier passes had seen.
- The fifth pass returned fewer repositories than the fourth, with 477 of the fourth's repositories absent three days later. Nothing suggests that those repositories had been cleaned in the meantime.

Code search caps its results, indexes neither forks nor private repositories, and appears to collapse identical files, since several launcher builds stop at exactly a hundred repositories. Each pass therefore samples an index rather than the population. Only the union of differently shaped queries comes close to it.

Within the third pass the most common executed file was `fa-brand-400.orc`, in 2,409 repositories once three defender fixtures were excluded. No font-based rule would ever have guessed that filename.

### Growth: a better search is not an outbreak

A later pass that finds more repositories is not automatically evidence of new spread. Splitting queries by file size recovered candidates that a single capped query could not, and searching nested paths recovered repositories that earlier signatures could not match. None of those improvements dates the original malicious change.

Code search returns no push times at all, and [Part 4](21-polinrider-repository-spread.md) shows push time to be the only reliable clock for this kit. Without stable definitions and retained timestamps, a better search looks like an outbreak and a worse one looks like a successful cleanup.

## Comparison: public counts measure a different net

Published figures are of the same order. OpenSourceMalware reported:

- 675 repositories across 352 owners on [8 March](https://opensourcemalware.com/blog/polinrider-dprk-compromised-hundreds-of-github-repos);
- 1,951 across 1,047 owners on [12 April](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github);
- 4,367 across 2,152 owners on [15 July 2026](https://opensourcemalware.com/blog/polinrider-blast-radius-grows).

It is tempting to draw a line through those points and my November floor and call it a growth curve. The searches behind them differ in coverage, however. The nested inline form, which carries most of the population, was matched neither by the earlier public signatures nor by my own first root-anchored searches. Any count from a search that did not cover that form misses most of the population. Differences between the series measure the nets as much as the fish, and I make no estimate of growth from them.

## Builds: a new launcher is not a new loader

Counting the launcher files themselves raises a parallel trap. A 996-repository sample from 6 November contained thirty distinct launcher builds, identified by the git hash of the task file. New builds were first pushed every one to three weeks between 2 September and 4 November, while older builds stayed in circulation. Up to ten large builds had victims pushing in the same weeks, so the kit is extended with parallel variants rather than replaced on a cycle.

A build, however, is not a loader. Of the nineteen builds absent from an earlier 67-repository sample, seventeen yielded a payload. Those seventeen payloads were only twelve distinct files of 12.8 to 40.3 KB:

- three builds run the same 12,797-byte file under two invented names;
- three further pairs share one payload each.

The launcher, the filename and the payload vary independently. A new launcher hash does not announce a new malware build, and thousands of distinct task-file hashes in a broad search can come from paths and surrounding configuration rather than from new code.

## Wallets: a population that is not the victims

One more number from this case looks like a victim count and is not. On 3 November a batch of 1,161 Ethereum wallets was emptied in a single scripted run into wallets connected to the resolver's funding. It would be easy to read that batch as 1,161 PolinRider victims, but two observations argue against it:

- the sweeps did not follow the weekly curve of launcher pushes;
- the wallets behave like one airdrop farmer's stored keys.

I read the batch as a stolen key store emptied in one go rather than as a measure of this operation's infections.

## Conclusion

Wallet keys, repository accounts and infected machines are three different populations, and only the second can be counted from outside. I therefore report at least 2,301 accounts as a floor with its definition attached, not as a victim count or a growth rate.

For anyone measuring a campaign like this, the lesson is to count by behavior, keep the definition stable, retain timestamps and take the union of differently shaped queries. A single capped search samples the index, not the population.

[Part 6](23-polinrider-detection.md) uses what the counting taught me about forms and disguises to describe detection that does not depend on a filename, and [Part 7](24-polinrider-money.md) returns to the drained wallets.
