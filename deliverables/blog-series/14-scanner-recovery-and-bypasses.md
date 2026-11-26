---
title: "When a Decoder Returns the Wrong Strings"
description: "A changed array-rotation loop exposed incorrect recovery, while eighteen of nineteen small variants evaded a rule, lowered severity or defeated decoding."
date: "2026-11-26"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/14-scanner-recovery-and-bypasses/"
kicker: "UNK_DeadDrop · Part 14"
tags:
  - "UNK_DeadDrop"
  - "deobfuscation"
  - "static analysis"
  - "detection engineering"
og_image_alt: "Comparison of checksum-based array rotation and an undetected splice-based variant"
---

I changed one line in an inert test fixture. The original loop rotated a string array with `push(shift())`; the variant used `splice`, and the scanner failed to recognize the new loop, treated the array as already aligned and returned decoded strings from rotation zero.

An unresolved value would have been easier to trust. These strings looked recovered, but were in the wrong order. The design refused to guess only after it recognized a rotation loop. This variant slipped past that first check.

It was one of nineteen single-change variants tested against the evaluated engine, and eighteen evaded their targeted rule, lowered its severity or defeated recovery. These tests used inert copies of demonstration code and a loader fixture. They were not additional malware samples. The full results are in the [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf).

![Recognized push and shift rotation leads to checksum evaluation; unrecognized splice rotation falls through to an incorrect zero-rotation result.](assets/14-rotation-failure.svg)

*The failing variant bypassed checksum evaluation because its array mutation was not recognized. The returned strings were wrong, not unresolved.*

## The loader rotates its string array before decoding

The extension analyzed in [Part 3](03-acorn-deobfuscation.md) hides strings behind decoder calls into an encoded array, and the program reorders that array before using it; if an analyst decodes the calls against the original order, the output may still look plausible while pointing to a false module name or URL.

In the obfuscator pattern I recovered, a startup loop decodes numeric-looking strings, combines them with `parseInt` and rotates the array until the result matches a constant in the file, and the scanner reimplements the decoder and evaluates that checksum across candidate rotations. It never calls the extension's decoder or executes its startup loop.

For the retained extension, this method found rotation 391; for its bootstrap, rotation 261. Both match the manual analysis. The scanner decoded 2,139 of 2,140 call sites in the extension, and 15 of 17 in the bootstrap, yet the remaining call sites matter: a result labeled “recovered” can still leave a particular URL or module name hidden.

If the loop is recognized but the checksum cannot be solved, the scanner can compare how many call sites produce printable text under each rotation, and it accepts a candidate only when it clears a high threshold and the next candidate scores much lower. This fallback helps with a non-foldable checksum target, but it cannot help when every rotation of a plain or keyless base64 array produces readable text.

The `splice` fixture revealed a different problem. The scanner never identified its loop as rotation code, so the unresolved-checksum path never ran, and it fell through to the no-rotation case. The mistake was in the scanner's view of the code, before checksum evaluation began.

## Clipboard, Electron, loader, and rotation variants

I tested the frozen engine against changes to API shapes and variable bindings, including aliases:

| Change in the fixture | Result |
| --- | --- |
| Route a clipboard builder through a reassignable `var` alias | Missed |
| Encode or assemble the command elsewhere, or fetch it at copy time | Missed |
| Copy through a hidden textarea and `execCommand` | Missed |
| Split or decode the `ELECTRON_RUN_AS_NODE` name at run time | Missed |
| Use another hidden-window structure for the Electron launch | Warning instead of error |
| Move loader steps into a function or change the cipher, binding or module-compilation form | Missed |
| Reach a string decoder through a `var` alias or object property | Warning remained, but affected call sites were not decoded |
| Make the checksum target non-foldable | Recovered by printable-text consensus |
| Rotate the array with `splice` | Incorrectly decoded under rotation zero |

Some misses are deliberate limits. The evaluator leaves reassignable `var` and `let` values unknown because following them safely requires tracking assignments and control flow, and a clipboard rule that cannot recover the command may not see the features that raise its severity, while other misses expose unimplemented structures: `execCommand`, a different encrypted-loader API or a split environment-variable name.

The pattern-specific findings are still useful when the observed code is reused, but they do not make the behavior hard to rewrite. The companion scanner's broader benchmark in [Part 13](13-scanner-registry-benchmark.md) puts this in context: low alert volume on ordinary packages coexists with poor coverage of generic malware.

## A `splice` loop returned strings from rotation zero

When a decoder remains unresolved, the gap is visible. When it returns a plausible but incorrect string, an analyst may follow the wrong lead. The `splice` result therefore deserves its own regression test and a fix that covers additional rotation operations.

There is an independent check for the specific extension: the manually reconstructed key authenticated three encrypted payloads, which confirms the recovered key and ciphertext relationship in those files. The scanner does not perform this decryption, and the authentication result cannot be transferred to another sample merely because its string array looks similar.

Potential fixes include recognizing additional array mutations and refusing to accept an apparently unrotated result for a keyed decoder without supporting evidence, though at this stage of the evaluation, those changes were still untested. Any change needs to be checked against the failing fixture, retained artifacts and benign obfuscated software. I kept the engine fixed for these reported results.

For now, treat recovered strings as leads to inspect against their call sites, and check how many sites remain unresolved. A clean scan means the evaluated rules did not find their patterns. It does not mean that the input is safe.


## Eighteen variants now match their baseline results

After recording those results, I changed the engine to cover the structures the fixtures exposed, and the evaluator now follows `var` and `let` bindings when it can show they are never reassigned in the declaring scope. It also handles constant `atob` and `Buffer.from` calls, known-array spreads into functions such as `String.fromCharCode`, and `eval` when the argument is a constant function name. It still leaves other dynamic text unevaluated.

The rules gained corresponding paths. Clipboard analysis now follows values assigned to mutable variables, copy handlers written as object methods, and the hidden-textarea `execCommand('copy')` flow, while Electron checks resolve split or decoded environment-variable names and encoded PowerShell. Loader analysis follows recognized ciphers to code-compilation sinks such as `Module._compile`, `vm`, `eval` and `Function`, including bindings inside functions.

For array rotation, the scanner now recognizes additional mutations such as `push(splice(...))` and `unshift(pop())`, and other array reordering inside the rotation function sends the sample to consensus analysis instead of silently assuming rotation zero. It also follows decoder calls through aliases and object properties.

The same nineteen fixtures were run again. Eighteen now match their baseline severity and recovery, including the `splice` fixture, whose strings match the checksum-proven rotation. The remaining case fetches the clipboard command at run time; that command text is absent from the file, so static inspection has nothing to recover.

Counting the fixtures handled overall, the hardened engine went from five of twenty-three to twenty-two. I then rescanned the earlier corpora on the same server and diffed every file against the frozen engine's results, and no file on any corpus gained an error-level finding. In the calibration corpus two files in one package newly warned on genuine obfuscation, that package was the only change in the popular-software tier, and in the recent npm corpus three files in two packages newly warned. The hardened engine also reproduced all fourteen expected outputs on the retained UNK_DeadDrop artifacts.

On the recently changed npm corpus, unresolved arrays dropped from 1,387 to 16, and nine packages whose arrays had been entirely unresolved now exposed license and service endpoints.

Two newly decoded packages imported `child_process`. Static review found ordinary housekeeping in a developer CLI and license-configuration handling in an SAP framework plugin; neither passed downloaded data to a code-execution sink, and neither was classified as malicious. I did not fetch the remote address found in one package.

One escalation needed to be narrowed during this pass. A first version treated any detached, hidden-window editor relaunch as an error, but an AI coding extension uses that shape to start its helper server, so it remains a warning. A malicious extension using the same launch would also receive a warning.

Throughput was 281 files per second on the calibration corpus after hardening, compared with 264 in the earlier run, but that is one measurement on one host, so it cannot show whether the change affected performance. The added warnings and zero additional errors describe the reviewed corpora only.

The new fixtures are regression tests in the [companion repository](https://github.com/KrasForge/unk-scanner), and the [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) reports the frozen and hardened runs separately. These fixtures guided the fixes and now guard against regressions. Coverage of unseen rewrites remains an open test.

## Comparing decoded strings with their originals

The `splice` failure raised a practical question: were the recovered strings correct? I tested the scanner on fifty harmless files, obfuscated under 72 combinations of javascript-obfuscator's string-array options across a current and an older release, which gave 7,200 samples in which every hidden string had a known original, and because a wrong rotation maps call sites to other genuine strings of the same program, I also aligned the decoded call sites in source order against the original and counted those that fell out of place.

No engine returned a wrong or misplaced string, but coverage was weaker than the correctness. The frozen engine recovered 68.3% of hidden strings from release 5.9.0 and nothing from 4.1.1, and the hardened engine 87.2% and nothing, because the engines missed the older release's decoder and lost most strings when function wrappers met one option. The revised engine, with fixes for those two cases, recovered 99.8% on both releases.

To check those fixes on unseen inputs, I generated a held-out set from twenty new files and five obfuscator releases, three of which the fixes had never seen, and recovery was 99.7% across them, so over 14,400 samples in all the revised engine decoded 3,265,560 call sites without misplacing one.

The three published deobfuscators, scored the same way on a 1,440-sample subset, showed a version boundary that probably matters more to other analysts than my own figures. webcrack 2.16.0, which runs the decoder in a sandbox, recovered 98.1% from both releases. The two static tools, synchrony 2.4.6 and obfuscator-io-deobfuscator 1.0.6, recovered 98.2% and 98.0% from 4.1.1 output and nothing from 5.9.0, and further reproductions place the boundary at release 4.2.2: both decode 3.2.7 and 4.1.1 and fail from 4.2.2 onward, although an unreleased commit on obfuscator-io-deobfuscator's main branch already decodes those releases. Each of the three tools also produced unexplained strings on exactly one input, by three different mechanisms, and one of those sat in a branch that never runs and appeared on the unobfuscated original too, so I treat a reproduction against the original as a precondition before filing anything upstream.

The same change also mattered for real malware. On the public dataset from [Part 13](13-scanner-registry-benchmark.md), samples producing a warning had risen from 62 to 64 with hardening and then doubled to 128 because many used the older decoder shape, while the revised engine again added no error anywhere; the extra warnings in the registry corpora came from fully decoded commercial extensions and five recent packages whose newly decoded strings I screened without finding anything malicious. None of the malware samples reached error level. The warning reports recovered obfuscation. Maliciousness requires examining what the decoded code does.

Recovery is also bounded by the decoder shapes the scanner knows. On loaders from PolinRider, a separate operation covered later in this series, most payloads lie outside those shapes: of twelve payloads recovered from its newer launcher builds, only one resolved call sites and gave strings, and one held variant parsed cleanly and returned no findings at all. Those loaders also arrive under font file names, which the scanner never opens, so a decoder that is near-exact on the shapes it recognizes says nothing about files it never selects.

The [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) describes the experiment. Scripts and results are in the [companion repository](https://github.com/KrasForge/unk-scanner).
