---
title: "What 2,301 Affected Accounts Actually Means"
description: "Five code-search passes give a floor of at least 2,301 GitHub accounts whose repositories carry PolinRider's launcher, and the differences between the passes say as much about search as about spread."
lastUpdated: 2026-11-27
published: 2026-11-26
sidebar:
  order: 22
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/22.png"
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
      content: "Part 22: What 2,301 Affected Accounts Actually Means"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/22.png"
---


I ran five code-search passes between 6 and 11 November and found at least 2,301 GitHub accounts, in about 6,900 repositories, whose public repositories carry a PolinRider launcher. That is a lower bound on accounts, and the differences between the passes say as much about search as about spread.

## Key takeaways

- Five passes returned 310, 537, 1,809, 1,908 and 1,862 accounts; their union, recounted from the saved lists, is at least 2,301 accounts in about 6,900 repositories.
- The figure counts accounts only, not infected computers, people who ran the loader, or thefts.
- No single pass approaches the union: code search caps results, skips forks and private repositories, and appears to collapse identical files, and the nested launcher form my first searches could not see carries 4,277 of the 5,418 repositories of the most complete pass.
- A larger later count is not evidence of new spread, and published counts from searches with different coverage cannot be joined into a growth curve.
- Launcher builds, filenames and payloads vary independently; seventeen builds yielded only twelve distinct payload files.

## Scope: what the number means

The number shows that the kit spread far beyond the take-home assessment where I found it. It is a count of accounts, and it is a lower bound. It does not count infected computers, people who ran the loader, or thefts:

- one account can own dozens of affected repositories;
- one repository can be cloned by people I cannot see;
- public code search shows only part of what exists.

The number carries meaning only together with the definition that produced it and the reasons the five passes disagree. Those reasons turned out to be the most instructive part of the measurement.

## Method: counting by behavior, not filename

Counting by filename would have failed from the start, for the reasons [Part 4](../21-polinrider-repository-spread/) describes, so every pass counts by behavior. An editor task is a launcher when it meets two conditions:

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

*Table 1. The five code-search passes after defender matches were removed.*

### How each pass was built

Each pass differs from the one before it in a specific way, and those differences explain most of the spread between the rows:

- **Pass 1** keyed on both halves of the inline launcher command together with the root path. It first returned at least 282 accounts across 507 repositories and about 1,361 matching files, and 272 accounts across 495 repositories once defender matches were removed. A second signature on the two helper-script names added 38 accounts, for a combined 310. An earlier total of 321 had counted one account twice under different capitalization.
- **Pass 2** ran the same signatures again but read every page up to the search's thousand-result cap. It returned 537 accounts across 996 repositories. Only 21 of the 280 accounts new to it had pushed since the first run, so the jump measures how much the cap had hidden rather than new spread.
- **Pass 3** used six queries covering every launcher form, each split by file size so that no slice exceeded the cap. Of 5,480 candidates, 5,421 repositories in 1,809 accounts confirmed, and 5,418 remain once three defender fixtures are removed. It found 1,559 accounts that no earlier pass had returned.
- **Passes 4 and 5** repeated the complete query set on 8 and 11 November. The fifth flagged 92 accounts in no earlier list, five of them pushed that day.

The union grew with the queries rather than with the campaign: at least 310 accounts after the first day, at least 590 after the overnight run, at least 2,204 after the third pass and at least 2,301 after all five. The first figure was a true floor, but once every launcher form was searched it had understated the population by a factor of seven.

Pass 3 also shows where the population sits:

| Launcher form | Repositories | Accounts |
|---|---:|---:|
| Nested inline command | 4,277 | 1,397 |
| `node` command with the path as an argument | 837 | 314 |
| Root inline command | 206 | 175 |
| Helper script reached through `dependsOn` | 98 | 37 |
| **Pass 3 total** | **5,418** | **1,809** |

*Table 2. The third pass by launcher form.*

The two forms my first passes covered, root inline and helper, together hold about one repository in eighteen. Most of the population was invisible to them, and the same was true of the earlier public signatures.

### Signatures that do not work

Several obvious search strings fail and are worth recording so that nobody runs them again:

- the injected `node init` invocation returns hundreds of entirely benign repositories, because `node init` followed by a watcher, compiler or build entry point is an ordinary pattern;
- the loader's deobfuscated string-array identifier returns 706 hits, mostly unrelated linter configurations;
- the second-stage path fragment returns 838, dominated by the open-source advisories about this very family.

The discriminator is the payload file's hash or its deobfuscated content, and nothing shorter.

## Results: why no single pass is the answer

The rows overlap heavily, so adding them would count most accounts several times. Yet no single row approaches the union.

- The third pass, despite covering every form, returned only 85 of the 507 repositories that the first searches had found on 6 November and missed 395 accounts that earlier passes had seen.
- The fifth pass returned fewer repositories than the fourth, with 477 of the fourth's repositories absent three days later. Nothing suggests that those repositories had been cleaned in the meantime.

Code search caps its results, indexes neither forks nor private repositories, and appears to collapse identical files, since several launcher builds stop at exactly a hundred repositories. Its result order also changes between runs. Each pass therefore samples an index rather than the population. Only the union of differently shaped queries comes close to it.

One residual caveat applies to the last three passes. Their output records no project root, so up to three of their repositories may still be defender fixtures or quarantine copies of the kind I removed by hand, and I would review those figures by hand before quoting them more precisely than the table does.

Within the third pass the most common executed file was `fa-brand-400.orc`, in 2,409 repositories once three defender fixtures were excluded. No font-based rule would ever have guessed that filename.

### Growth: a better search is not an outbreak

A later pass that finds more repositories is not automatically evidence of new spread. Splitting queries by file size recovered candidates that a single capped query could not, and searching nested paths recovered repositories that earlier signatures could not match. None of those improvements dates the original malicious change.

The repositories' own push dates, which I read separately, do show a rise: launcher pushes went from about fifty a week in calendar weeks 39 to 41 of 2026 to about two hundred a week in weeks 42, 43 and 45. A push date is only a repository's last push, however, so an old infection pushed again later appears as new. Code search itself returns no push times at all, and [Part 4](../21-polinrider-repository-spread/) shows push time to be the only reliable clock for this kit. Without stable definitions and retained timestamps, a better search looks like an outbreak and a worse one looks like a successful cleanup.

## Comparison: public counts measure a different net

Published figures are of the same order. OpenSourceMalware reported:

- 675 repositories across 352 owners on [8 March](https://opensourcemalware.com/blog/polinrider-dprk-compromised-hundreds-of-github-repos);
- 1,951 across 1,047 owners on [12 April](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github);
- 4,367 across 2,152 owners on [15 July 2026](https://opensourcemalware.com/blog/polinrider-blast-radius-grows).

It is tempting to draw a line through those points and my November floor and call it a growth curve. The searches behind them differ in coverage, however. The nested inline form, which carries most of the population, was matched neither by the earlier public signatures nor by my own first root-anchored searches. Any count from a search that did not cover that form misses most of the population. Differences between the series measure the nets as much as the fish, and I make no estimate of growth from them.

## Builds: a new launcher is not a new loader

Counting the launcher files themselves raises a parallel trap. A 67-repository sample first suggested eleven distinct launcher builds, identified by the git hash of the task file. The 996-repository sample of 6 November contained thirty, with all eleven earlier builds reappearing and nineteen new. My first reading, a rotation on a roughly two-week clock, did not survive the larger sample. New builds were first pushed every one to three weeks, on 2, 23 and 26 September, 10 October, 14 October for three builds, 15 and 23 October and 4 November, while older builds stayed in circulation. Up to ten large builds had victims pushing in the same weeks, so the kit is extended with parallel variants rather than replaced on a cycle.

| Build | Push window | Note |
|---|---|---|
| `5e226620` | from 31 May 2026 | the long-running workhorse |
| `5b08e3cd` | September 2026 | still carries resolver wallet B |
| `d8d23107` | 20 October to 4 November 2026 | the build of my analyzed loader |
| `4de8b6d6` | live from 5 November 2026 | first build with the helper scripts |
| `dc23e7fe` | appeared 6 November 2026 | current at the time of the passes |

*Table 3. Selected launcher builds and their push windows.*

Each build pairs with its own fake-font filename, and the naming walked from `400.woff2` through `500.woff2` and `900.eot` to `700.otf`. A push date is a repository's last push, so a repository pushed again later stretches its build's window, but the overlap is too wide to be explained that way.

The September build shows why build and wallet must be read separately. It still points at wallet B after the hand-over to wallet C, because a build made before a hand-over is never retrofitted. A victim's build number dates the infection; it does not tell which wallet is current.

A build, however, is not a loader. Of the nineteen builds absent from an earlier 67-repository sample, seventeen yielded a payload. Those seventeen payloads were only twelve distinct files of 12.8 to 40.3 KB:

- three builds run the same 12,797-byte file under the names `fa-solid.lkf` and `fa-solid.lfk`;
- two builds share one file under `.fml` and `.lkf` names;
- two share one under `fa-brand-400.orc`;
- two share one under `fa-brands-400.ttf`.

All twelve are JavaScript under font names, with first bytes that are whitespace padding or code and no font header anywhere. Two builds could not be tested at all, because their only repositories had been cleaned before I fetched them.

The launcher, the filename and the payload vary independently. A new launcher hash does not announce a new malware build, and thousands of distinct task-file hashes in a broad search can come from paths and surrounding configuration rather than from new code.

## Wallets: a population that is not the victims

One more number from this case looks like a victim count and is not. On 3 November a batch of 1,161 Ethereum wallets was emptied in a single scripted run into wallets connected to the resolver's funding. It would be easy to read that batch as 1,161 PolinRider victims, but two observations argue against it:

- the sweeps did not follow the weekly curve of launcher pushes;
- the wallets behave like one airdrop farmer's stored keys.

The timing comes first. Counting Ethereum only, 1,342 distinct wallets were emptied into the resolver side's collection wallet and its sweep hub. They arrived at between one and forty-four a week from 3 September 2026 and then 1,229 in calendar week 45. Of those, 1,161 came between 05:00 and 06:59 UTC on 3 November, 160 in the first hour and 1,001 in the second. Launcher pushes, meanwhile, rose gradually over the autumn, as the growth section shows.

The wallets themselves point to a single owner:

| Trait | Observation |
|---|---|
| Creation | bulk-created in bursts on 15 to 17 September 2024 and 24 to 26 September 2025 |
| Activity | a median of two transactions each, no contract deployments |
| Use | about 1,100 active on Base, Arbitrum and Polygon, calling the same contracts |
| Funding | withdrawals from one exchange hot wallet, the first funder of 1,096 of them, mostly in uniform amounts of 0.001 ETH |
| Shared counterparties | services only, apart from the operator's sweep hub, present in 1,152 of the 1,161 |
| Value taken | about 0.008 ETH in total |

*Table 4. The 1,161 wallets swept on 3 November 2026.*

That is one script farming airdrops across a whole set of wallets, whose keys most likely sat in one key store on one compromised machine. The harm is that machine and its keys rather than the amount. I read the batch as a stolen key store emptied in one go rather than as a measure of this operation's infections, and its link to PolinRider's own infections remains unproven.

## Conclusion

Wallet keys, repository accounts and infected machines are three different populations, and only the second can be counted from outside. I therefore report at least 2,301 accounts as a floor with its definition attached, not as a victim count or a growth rate.

For anyone measuring a campaign like this, the lesson is to count by behavior, keep the definition stable, retain timestamps and take the union of differently shaped queries. A single capped search samples the index, not the population.

[Part 6](../23-polinrider-detection/) uses what the counting taught me about forms and disguises to describe detection that does not depend on a filename, and [Part 7](../24-polinrider-money/) returns to the drained wallets.
