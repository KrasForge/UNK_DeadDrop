---
title: "Detecting PolinRider Beyond a Filename"
description: "Multi-engine scanners and a JavaScript-only source scanner saw almost none of PolinRider, while a check on what a repository runs automatically and on asset files that parse as JavaScript reached every launcher in a real-world test."
lastUpdated: 2026-11-26
published: 2026-11-26
sidebar:
  order: 23
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/23.png"
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
      content: "Part 23: Detecting PolinRider Beyond a Filename"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/23.png"
---


I found that multi-engine scanners and my own JavaScript-only scanner saw almost none of PolinRider. A check on what a repository runs automatically, combined with a test for asset files that parse as JavaScript, flagged 78 launchers in 300 real task files with no false positive and no PolinRider launcher missed.

## Key takeaways

- Of twelve victim-published payloads, eight were absent from VirusTotal and two more had zero detections; of twelve payloads I recovered, four were absent and four more had zero detections.
- The launcher names the file it hands to Node, and that trigger-to-target relationship held up better than any filename, extension, payload hash or server address.
- On 7 November the condition flagged 78 launchers in 300 real folder-open task files, all PolinRider, and nothing in the 82 lifecycle scripts among the top 1,000 npm packages.
- Real launchers exposed nine parser gaps that no fixture had found, each a silent miss rather than an error.
- Before opening a repository from a recruiter, client or stranger, read its `.vscode/tasks.json`, agent settings and `package.json` scripts as text, and keep automatic tasks off.

## The problem: the first plausible match was a real font

In one infected repository the first `fa-solid` file in the fonts directory was a genuine 202,902-byte font that a public scanning service had known since 2020. The editor task ran the `.woff2` file sitting beside it, which was JavaScript under a font's name. Anyone who collected the first plausible match in that directory would have analyzed a real font and declared the repository clean.

The launcher supplied the right answer, because it names the file it hands to Node. As the investigation widened from one assessment to thousands of repositories, that relationship between a trigger and its target held up far better than any filename, extension, payload hash or server address. This part describes what the existing tools saw of the campaign, the condition that did reach it with its measured results, and the questions the evidence still leaves open.

## Scanners: what existing tools saw

Multi-engine scanning services detect almost none of this:

- Of twelve payloads that victims published in their own incident reports, eight were absent from VirusTotal and two more had zero detections.
- Of the twelve payloads I recovered from the newer launcher builds, four were absent and four more had zero detections.
- The builds in active use at the time of writing were both absent.

The one detection name a victim reported, Microsoft Defender's `Trojan:Script/MalTask.A`, fires on the `tasks.json` launcher rather than on the payload. In practice it is the launcher pattern that catches this family.

My own [public scanner](https://github.com/KrasForge/unk-scanner) fared worse for a structural reason. It reads only JavaScript and TypeScript files, so it never opens an editor task, a package manifest or a font file. For PolinRider it saw neither the launcher nor the payload. That is a stated limit of its scope, which covers UNK_DeadDrop, rather than a rule defect. The habit behind it, selecting files by extension and assuming that configuration is not code, is common enough that an attacker needs only one automatic trigger and one disguised file to pass through both.

## Method: a condition on what runs automatically

The method I evaluated reports a launcher only when two conditions hold together: an automatic trigger and a suspicious target. Its rationale is a base rate rather than a signature.

Automatic triggers are common in legitimate projects, which start development servers on folder open and build native code on install. Files in asset directories are common too. What is rare is an automatic trigger that does one of the following:

- hands a repository file to a JavaScript runtime from a place where legitimate triggers have no reason to point, such as a fonts, asset or hidden tooling directory;
- hands it a file under a non-code name;
- downloads content and pipes it into an interpreter.

The triggers it reads are:

- folder-open editor tasks, including those reached through `dependsOn`;
- the hooks and always-applied rules of coding agents;
- install-time package scripts;
- build files that expand commands.

### Content test: JavaScript under a non-code name

Beside the trigger check sits a content test that I would recommend to anyone. A file is reported as JavaScript under a non-code name when its first bytes carry no font, image or document signature and its text parses as JavaScript. The file is parsed only, never evaluated. The test runs over every asset-named file in a project, not only over files a launcher names, and never behind an extension filter, because the name is the disguise.

## Results: every launcher in the test set

The results are the reusable part:

- On 7 November I ran the condition over 300 real folder-open task files from public repositories that appeared on no earlier PolinRider, Miasma or defender list. It flagged 78 launchers, all PolinRider, with no false positive and no PolinRider launcher missed. The ground truth was task files that name a target in the kit's fonts directory.
- On the 82 lifecycle scripts among the top 1,000 npm packages it flagged nothing.
- The content test recognized all thirteen held loader payloads, twelve plus a control.
- On five live repositories of the separate Miasma worm it found every launcher, including two agent session-start hooks and an always-applied agent rule.

Those figures are bounded by their samples, and they say nothing about endpoint behavior. They show that a check whose selection step does not trust the filename reached payloads that string recovery could not decode and that multi-engine scanning did not flag. Both of those act only after a file has been chosen, and the disguise defeats the choosing.

## Parsing: real files broke the reader nine times

The method's other main lesson concerns reading configuration. Real launchers exposed nine gaps that no fixture written from published descriptions had found, and every one was a silent miss rather than an error:

- a leading byte-order mark that made a strict parser reject a file the editor runs happily;
- framework route-group parentheses that cut a path at the wrong bracket;
- payloads deep in the source tree instead of in a root assets directory;
- path arguments with spaces split on reassembly;
- unquoted paths with spaces and ampersands cut at the first space;
- inline code read as though it were a filename;
- tasks reachable only through `dependsOn` that were not treated as automatic.

Eight repositories whose folder names combined spaces with parentheses stayed hidden until a much simpler text search found them. A text search and a parser fail on disjoint sets of real files, so neither validates the other.

A reader of task files has to read them as the editor reads them, tolerating comments, trailing commas and a byte-order mark. It has to be checked against real files and a second, independent search before its silence means anything.

## Defense: review before opening

For a developer the practical rule is to treat configuration that a tool acts on without asking as code. Before a repository from a recruiter, a client or a stranger is opened in an editor or handed to a coding agent, read these as text:

- its `.vscode/tasks.json` and every task its folder-open tasks depend on;
- its agent settings and rules;
- every script in `package.json`.

A trigger that runs a file from a fonts or asset directory, or under a font, image or invented extension, should stop the opening.

Visual Studio Code already provides most of the protection through [Workspace Trust and Restricted Mode](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust), which runs no task until a folder is trusted. The `task.allowAutomaticTasks` setting can keep automatic tasks off by default. Any commit that adds or changes `.vscode/` or package scripts deserves review, especially when it appears under another person's name or inside a force-push. That is exactly how [Part 4](../21-polinrider-repository-spread/) showed the kit arriving.

## Network: the lookups and the fetch

On the network the stable steps are the lookups and the fetch. A Node process started from a workspace that queries a blockchain transaction list or a TronGrid account endpoint, followed by cleartext HTTP to port 443 on a bare address under a path beginning `/0x/`, is far more telling than any host the chain names today. I hold no endpoint telemetry from an affected machine, so I offer that pairing as a hypothesis derived from the recovered chain rather than as a validated rule.

- **Ethereum branch:** the closed wallet set of [Part 3](../20-polinrider-wallets-and-hosts/) lets a defender compute the current server directly from the chain. A poll of the three wallets every two hours is adequate for the rotation behavior observed so far.
- **TRON branch:** a watch on known pointers sees them stop but cannot see a replacement created under a new name, so it needs a discovery channel beside it.

## Emulation: copies that match on public values

The hardest detection case in this ecosystem is a cluster that reuses an operation's genuine values. From 12 October nine single-use npm accounts published twelve malicious packages carrying one stealer. They were delivered through fake take-home exercises on an AI-agent theme authored by the GitHub persona Noel-Codess, which register a package as a PostCSS plugin so that it runs whenever the application is started, built or tested. Its server domain was `node-js[.]dev` and its server address `2.58.56[.]216`.

The stealer carries PolinRider's resolver design, both published TRON wallets with their Aptos fallback accounts, the exact TronGrid query string and the worm's force-push propagation. Three observations point the other way:

- every one of those constants had already been printed by OpenSourceMalware or [JFrog](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/);
- the code names itself after the analysts' label rather than the operator's;
- it fetches no next stage.

I assess it as probable reuse or emulation of PolinRider at moderate confidence; a non-public constant or a shared build marker would settle it.

The same logic applies to GhostAction. On [GitGuardian's](https://blog.gitguardian.com/ghostaction-x-polinrider/) working hypothesis, its operator copied a public PolinRider launcher while running its own infrastructure, so its server does not belong in PolinRider's indicator set. A cluster that copies from reporting will match on precisely the values reporting has made known. I now check every constant against the public write-ups before calling it unpublished.

## Limitations

- The condition does not interpret shell control flow or judge what a payload does. Its output is a triage signal naming the file to read, not a verdict on a project.
- It produces nothing for a package that runs on import without any launcher.
- Passing `--ignore-scripts` to an install does not stop a `prebuild` script when the project is later built, as [npm's documentation](https://docs.npmjs.com/cli/v10/using-npm/config#ignore-scripts) makes clear. The trigger list shares that gap, so a forged `prebuild` dropper of the kind SafeDep has reported would pass unreported until review catches it.

## Open questions

Several questions remain open, each with a specific test:

- The second stage I retrieved on 6 November is still undecrypted and unexecuted, so the later browser and wallet stealer stages rest on other researchers' reporting. Decrypting it or obtaining the stealer would show whether the keys drained from wallets came from this operation.
- The Hiring777 chronology of [Part 1](../18-polinrider-following-a-developer/) needs the developer's own account to decide between a dormant implant and a misleading commit date.
- The body of the Python sample tied to the newest Ethereum-branch host would test the host-level link between the two branches.
- Loaders from advisory packages that cite none of the three known wallets would show whether resolver wallets exist outside the closed set.

## Conclusion

PolinRider passes through tools that choose files by name, because the name is the disguise. A check that starts from what a repository runs automatically, and tests asset files by content, reached every launcher in a real-world test where scanners saw almost nothing.

For a developer who suspects exposure, the repository is where scoping begins rather than proof of its extent. Preserve the files and history, follow each execution path to the file it actually runs, and check every repository and credential the machine could reach, because a cleaned task file establishes nothing about the rest.

[Part 7](../24-polinrider-money/) follows the money that pays for the resolvers, from gas funding through laundering to a small observed cash-out.
