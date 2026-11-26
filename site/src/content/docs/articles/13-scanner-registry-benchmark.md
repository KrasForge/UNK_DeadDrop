---
title: "What 2.8 Million Files Revealed About unk-scanner"
description: "Two false alarms in recently changed npm packages, low coverage of public malware, and the limits of a larger static-analysis benchmark."
lastUpdated: 2026-11-26
published: 2026-10-29
sidebar:
  order: 13
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/13.png"
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
      content: "Part 13: What 2.8 Million Files Revealed About unk-scanner"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/13.png"
---


The scanner raised two error-level findings among nearly 2.4 million files from recently changed npm packages, and neither was malicious. Among 2,122 known-malicious packages and extensions, it flagged only 62 samples, all at warning level.

## Key takeaways

- Two error findings in 19,976 recently changed npm packages amount to about 0.01% of packages needing error review in this scan; both were benign.
- The frozen engine raised warnings on 62 of 2,122 known-malicious samples and no errors; a later revision raised warnings on 128, still with none at error level.
- About nineteen in twenty known-malicious samples still received no warning, so a clean result cannot clear a package.
- Release 0.2.0 on npm and PyPI rejected 31,964 of 143,153 calibration files, and 31,292 of those were valid source, overwhelmingly TypeScript.
- The scanner reads only JavaScript and TypeScript files, so code started from an editor task, an agent hook, a package script or a font-named file is outside its view.

## Results: few false alarms, few detections

I read both error findings. One came from an AI desktop application's local helper. The other came from a setup guide whose `curl` command printed an HTTP status code.

The quieter result came from a different corpus. Serious false alarms were rare, and so were detections outside the structures the rules were built to recognize. Even after a later engine revision doubled the malware warnings to 128, about nineteen in twenty known-malicious samples still received none.

The results and sampling details are in the [scanner paper](../../downloads/UNK-Scanner-Paper.pdf). They come from fixed runs on 29 October, using one engine on an eight-vCPU virtual server. Part 11's [YARA replay](../11-detection-engineering/) covers a different system and a different question.

![Three scanner corpora with error and warning counts shown separately.](/UNK_DeadDrop/diagrams/13-benchmark-results.svg)

*Figure 1. The error count stays low on popular and recent code, while most known-malicious samples receive no warning. The counts are those of the frozen engine, and they are not directly comparable because the corpus units differ.*

## Corpora: npm, Open VSX and public malware

The first check covered 2,500 npm packages ranked by `npm-high-impact` and 500 Open VSX extensions ranked by downloads. That produced 143,153 distinct files. I had already used this material to tune severity. It was useful for finding noisy rules, but it could not show how the same choices would behave on other code.

The expanded run added three collections:

| Collection | Acquired | Files |
| --- | ---: | ---: |
| Top npm packages, Marketplace extensions and the Open VSX calibration set | 4,992 of 5,000 npm packages; 967 of 1,000 extensions | 332,054 |
| Packages selected from the npm registry changes feed | 19,976 of 20,000 package names | 2,403,437 |
| Datadog malicious-package dataset | 122 IDE extensions; seeded sample of 2,000 npm packages | 41,359 |

The three collections hold 2,776,850 file entries, which is the figure in the title. Of these, 56,361 files occur in more than one collection, so the distinct files number about 2.72 million.

### Method: one rule change, then a frozen engine

The first collection included 188,901 files absent from the calibration set. These make a useful comparison, with one qualification. The first scan raised four errors in Microsoft Live Share and GitHub Codespaces bundles. Both contained an editor-as-Node launch near code from a privilege-elevation library. The rule escalated from the hidden PowerShell anywhere in the bundle, although the operations were not part of the same launch path.

I changed escalation to require the hidden execution in the launching function or a local helper it calls. The change cleared those four findings and preserved the severities of the retained UNK_DeadDrop files. I then froze the engine for the reported scans. Because those Tier 1 files informed a rule change, the final result is disjoint from the original calibration corpus but is not an untouched held-out measurement.

## Recent packages: two benign error alerts

The registry changes feed selected packages whose documents changed over a window of about 83,000 sequence positions. Most changes occurred on 29 October. The scan found 6,215 warnings and two errors among the 19,976 packages acquired.

### Error findings

- **Desktop application.** It assembled an encoded PowerShell command, hid its window and set `ELECTRON_RUN_AS_NODE` for a helper. That combination triggered escalation. Reading the code showed the helper contacting `127.0.0.1` with a local password; in this application, the launch was part of an ordinary local workflow.
- **Remote-access setup guide.** It copied text containing “verify” and a `curl` command that printed an HTTP status code. The rule treated the verification wording as lure evidence and missed the difference between displaying a status and fetching a payload.

### Warning findings

Warnings took longer to sort out. String-array obfuscation accounted for 6,142 findings across 153 packages. I screened the recovered strings for shells, processes, wallet terms, credential stores and exfiltration services.

- Seven packages matched those searches. Their code fit their apparent roles, including bots, a workspace connector and agent command-line tools.
- Nine packages still had unresolved arrays, eight from one commercial product. These still need analysis.
- Clipboard and hidden-script warnings received code review.
- I read five Electron findings whose package names did not suggest developer tooling. I triaged the remaining 39 from the recorded launch target and environment. The 39 triaged Electron findings received no full code review.

Review depth therefore varied by finding type. Two error findings in 19,976 packages amounts to about 0.01% of packages needing error review in this scan. That number describes this window and this rule set. It is not a fleet false-positive rate.

## Malware: alerts reached 62 of 2,122 samples

The public malware set changed the interpretation of the low alert count. I counted a sample as detected if any file in it raised a warning or error.

- Of 122 IDE extensions, four raised warnings.
- Of 1,884 npm packages classified as malicious at creation, 44 raised warnings.
- Of 116 compromised npm libraries, fourteen raised warnings.
- No sample reached error level.

### Why samples were missed

The warnings came from obfuscated string arrays and hidden-script launches. Most missed samples did not use the clipboard, Electron or encrypted-loader patterns represented in the rules. Parser failures explained 27 misses, which leaves many readable samples outside the scanner's model.

Screening the missed files found common access to environment variables and home-directory files, frequent use of `child_process` and network requests, and references to webhooks. Twenty-one missed IDE extensions contained variation-selector characters used to hide text. These counts describe what appeared in the missed code; each behavior also occurs in legitimate programs.

The retained campaign files show that the scanner recognizes the structures it was built from. That is useful when the code is available and resembles the observed samples. It does not counter the broader malware result, because those retained files informed the rules. Even within the case, the Windows Node agent raised only notes. Its absence of a warning is a miss, not a change in what the agent does.

### The revised engine

The 62 belong to the frozen engine. A controlled recovery experiment, described in [Part 14](../14-scanner-recovery-and-bypasses/), exposed an older decoder shape that the engine did not recognize. Because many obfuscated samples used that older shape, the revised engine raised warnings on 128 of the 2,122 samples, still with none at error level. A warning for recovered obfuscation says only that the file was obfuscated. The denominator includes 295 samples that contain no file the scanner reads at all, and these count as undetected.

## Parsing: Acorn and Babel read 330,473 files

I measured parser failures separately to distinguish unreadable inputs from code the rules missed. The evaluated engine tries Acorn first, then an AST-only Babel fallback for supported TypeScript and JSX syntax. That fallback exists only in the [companion repository](https://github.com/KrasForge/unk-scanner); the release on npm and PyPI is still 0.2.0, which has none.

- Release 0.2.0 rejected 31,964 of the 143,153 calibration files. When I checked every rejection with an independent parser, 31,292 were valid source, overwhelmingly TypeScript. For that release, more than a fifth of the calibration corpus is unexamined rather than examined and found clean.
- For JavaScript alone, its coverage is almost complete: only 28 valid files, all containing JSX, were rejected.
- In the popular-software collection, the evaluated engine parsed 330,473 of 332,054 files. Of the 1,576 parse failures, most were TypeScript, and none parsed under the independent Babel configuration I tested. Compatibility with their original build toolchains remains untested.
- Five inputs were not valid UTF-8.

## Performance: memory, not time, was the constraint

- With four workers, the isolated command-line run processed 272 files per second on the calibration collection, and the in-process worker-thread run processed 264.
- On a sixteen-thread workstation, the same calibration ran at 412 files per second isolated against 439 in process. That is a cost of about 6%, with run-to-run variation of about 10% either way. Both are single runs, so they fit a small isolation cost within noise and nothing more precise.
- The malware set ran at 325 files per second.
- The recent-package scan reached 848 with six workers and a different mix of mostly small files.
- With a 256 MiB heap, thirteen bundles of five to eight megabytes failed. With the 512 MiB default, every file completed.

## Conclusion

The scanner is useful for surfacing the behaviors it knows how to follow, and its low error count makes it practical to review. Its malware misses mean a clean result cannot clear a package.

It reads only JavaScript and TypeScript files. Code started from an editor task, an agent hook, a package script or a file named like a font is outside its view by design. Defenders should treat it as one input to review, not as a gate that clears code.

Part 14 follows the less comfortable question: how little does an author need to change to avoid those findings?
