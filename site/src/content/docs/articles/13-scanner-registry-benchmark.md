---
title: "What 2.8 Million Files Revealed About unk-scanner"
description: "Two false alarms in recently changed npm packages, low coverage of public malware, and what a larger static-analysis benchmark actually measures."
lastUpdated: 2026-10-29
sidebar:
  order: 13
---


The scanner raised only two error-level findings across 2.4 million files from recently changed npm packages. Both were false positives. Against a separate collection of 2,122 known-malicious packages and extensions, it raised warnings on just 62 samples and no errors at all.

Those results belong together. A tool can produce very little noise because it recognises only a narrow set of structures. The larger benchmark made that trade-off visible: `unk-scanner` could expose commands and hidden strings in the UNK_DeadDrop artifacts that shaped its rules, yet miss ordinary credential theft written without those structures.

The [scanner paper](../../downloads/UNK-Scanner-Paper.pdf) records the evaluation and its limits. The runs described here used one fixed engine on an eight-vCPU virtual server on 29 October. They extend the smaller development checks described in [Part 11](../11-detection-engineering/); they do not turn the retained campaign samples into independent validation data.

## Beyond the development corpus

The initial corpus contained 2,500 npm packages selected using the `npm-high-impact` ranking and 500 Open VSX extensions selected by downloads. Together they supplied 143,153 distinct files. Those files helped calibrate the rules, including when an Electron launch should be a warning rather than an error. A low alert count on that corpus was useful feedback, but the scanner had already benefited from seeing it.

The expanded evaluation added three different views of the ecosystem:

| Corpus | Acquired material | Distinct files within the corpus |
| --- | --- | --- |
| Popular software | 4,992 of the top 5,000 ranked npm packages, 967 of the top 1,000 Marketplace extensions by installs, and the calibration Open VSX set | 332,054 |
| Recently changed npm packages | 19,976 of 20,000 selected package names from a registry changes window | 2,403,437 |
| Public malware dataset | 122 IDE-extension samples and a seeded sample of 2,000 npm samples | 41,359 |

These are different sampling frames. A registry document change is not necessarily a new package, and popularity does not certify benignness. Deduplication removes repeated file bytes within a corpus; it does not make files from the same package independent observations. The malware selection came from the [Datadog dataset](https://github.com/DataDog/malicious-software-packages-dataset), pinned to commit `438afad`, with random seed `20261029` for the npm sample.

Archives were inspected without installing packages or running lifecycle scripts. Download and extraction time were excluded from the throughput measurement.

Of the popular-software files, 188,901 were absent from the original calibration set. The final scan raised no errors and 12 warnings on these additional files. Eleven warnings concerned legitimate editor-as-Node launches; one concerned a commercial theme's RC4-obfuscated licence code.

That final result followed an adjustment. The first expanded run raised four errors in Live Share and Codespaces bundles. Their Electron launch code shared a file with a privilege-elevation library that used hidden PowerShell. The rule had combined those facts across the entire bundle, even though the suspicious operations did not belong to the same launch path. Restricting escalation to the launching function or a local helper removed those errors while preserving the retained artifacts' earlier severities.

The engine was then fixed for the final runs. The additional files remained separate from the initial calibration set, but their results had influenced this one rule. Calling the final zero-error count an untouched held-out result would conceal that dependency.

## The two errors worth reading

The registry changes window covered roughly 83,000 sequence positions and selected 20,000 package names, of which 19,976 were acquired. The scanner produced 6,215 warnings and two errors.

One error came from an AI desktop application. It constructed hidden, encoded PowerShell that set `ELECTRON_RUN_AS_NODE` for a local helper. That was the technique combination the rule considered serious, but the helper contacted `127.0.0.1` using a local password. Full review found a legitimate application workflow.

The other came from a remote-access tool's setup guide. A copied passage contained the word "verify" and a `curl` command. The command printed an HTTP status code; it did not download and execute a payload. The rule had treated verification wording as evidence of a lure without adequately distinguishing what the command did.

The warnings were dominated by string arrays: 6,142 findings across 153 packages. Recovered strings were screened for shell, process, wallet, credential-store and exfiltration-service indicators. Seven packages warranted further examination, with the matches explained by their functions, including bots, connectors and agent command-line tools. Nine packages retained unresolved arrays, eight belonging to one commercial product.

Review depth differed by warning type. Clipboard and hidden-script findings received code inspection. Five Electron packages also received code inspection; the other 39 were assessed from the recorded launch target and environment. This was triage, not a complete audit of every package. No package was classified as malicious, but unresolved code prevents treating that outcome as a clean bill of health.

At error level, two of 19,976 packages required reading, about 0.01%. That is the observed review burden in this window. It is not a fleet false-positive rate, and it says nothing by itself about how many malicious packages passed unnoticed.

## Malware that passed quietly

The public malware corpus supplied the missing counterweight. A sample counted as detected if any file produced a warning or error.

| Sample class | Samples | Samples with warnings | Samples with errors |
| --- | --- | --- | --- |
| IDE extensions | 122 | 4 | 0 |
| npm packages created with malicious intent | 1,884 | 44 | 0 |
| Compromised npm libraries | 116 | 14 | 0 |

The 62 detections came from string-array obfuscation or hidden-script launches. None reached error level. Parser failures explained only 27 misses, so adding parser support alone would not close the gap.

Screening the remaining missed samples found abundant behaviours the rules did not model: environment-variable access, home-directory reads, child processes, network requests and webhook references. Among missed IDE extensions, 21 contained variation-selector code points, a different way of concealing content. These traits also occur in legitimate software, so they are descriptions of the missed code rather than standalone maliciousness tests.

The result changes how a clean scan should be used. It can indicate that the scanner found none of its recognised structures. It cannot establish that a package lacks credential theft, install-time execution or another malicious path. The retained Windows Node agent makes the same point within this investigation: it produces notes, below the warning threshold, despite its collection functionality.

## Parsing and throughput

The evaluated engine first tries Acorn, then uses an AST-only Babel fallback for supported TypeScript and JSX syntax. In the popular-software corpus it parsed 330,473 of 332,054 files, or 99.5%. There were 1,576 parse failures and five inputs that were not valid UTF-8. Most parse failures were TypeScript; failing both the scanner and the independent Babel configuration tested does not prove that a file is invalid in its original build toolchain.

On the calibration files, the isolated command-line path processed 272 files per second with four workers, compared with 264 for the in-process worker-thread path. The comparison showed no slowdown in that run, but repeated trials would be needed to estimate overhead reliably. The malicious corpus ran at 325 files per second. Recently changed npm packages reached 848 files per second with six workers, reflecting a different mix of file sizes as well as the extra workers.

The useful result is not a single throughput number. It is the combination of a workable analysis rate, a measured review burden and explicit blind spots. The next test asks how stable the detections remain when the code changes slightly. [Part 14](../14-scanner-recovery-and-bypasses/) follows those variants, including one that caused the scanner to return the wrong decoded strings.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
