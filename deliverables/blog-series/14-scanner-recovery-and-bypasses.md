---
title: "When a Decoder Returns the Wrong Strings"
description: "A changed array-rotation loop exposed incorrect recovery, while eighteen of nineteen small variants evaded a rule, lowered severity or defeated decoding."
date: "2026-11-27"
published: "2026-10-29"
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

I found that one changed line in an inert test fixture made the scanner return wrong strings. The variant rotated a string array with `splice` instead of `push(shift())`, and the scanner decoded it from rotation zero; eighteen of nineteen single-change variants evaded their targeted rule, lowered its severity or defeated recovery.

## Key takeaways

- A `splice` rotation loop was not recognized, so the scanner treated the array as already aligned and returned plausible but incorrect strings.
- Eighteen of nineteen single-change variants evaded their targeted rule, lowered its severity or defeated recovery in the evaluated engine.
- After hardening, eighteen of the nineteen fixtures match their baseline results, and no file on any rescanned corpus gained an error-level finding.
- Across 14,400 samples, the revised engine decoded 3,265,560 call sites without misplacing one; two published static deobfuscators recover nothing from javascript-obfuscator output from release 4.2.2 onward.
- Treat recovered strings as leads to check against their call sites; a clean scan means the evaluated rules did not find their patterns, not that the input is safe.

## Recovery: a `splice` loop returned the wrong strings

The original loop rotated a string array with `push(shift())`. The variant used `splice`. The scanner failed to recognize the new loop, treated the array as already aligned and returned decoded strings from rotation zero.

An unresolved value would have been easier to trust. These strings looked recovered but were in the wrong order. The design refused to guess only after it recognized a rotation loop, and this variant slipped past that first check.

It was one of nineteen single-change variants tested against the evaluated engine. These tests used inert copies of demonstration code and a loader fixture. They were not additional malware samples. The full results are in the [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf).

## Mechanism: the loader rotates its string array before decoding

The extension analyzed in [Part 3](03-acorn-deobfuscation.md) hides strings behind decoder calls into an encoded array. The program reorders that array before using it. If an analyst decodes the calls against the original order, the output may still look plausible while pointing to a false module name or URL.

### Method: evaluating the checksum statically

In the obfuscator pattern I recovered, a startup loop decodes numeric-looking strings, combines them with `parseInt` and rotates the array until the result matches a constant in the file. The scanner reimplements the decoder and evaluates that checksum across candidate rotations. It never calls the extension's decoder or executes its startup loop.

- For the retained extension, this method found rotation 391; for its bootstrap, rotation 261. Both match the manual analysis.
- The scanner decoded 2,139 of 2,140 call sites in the extension and 15 of 17 in the bootstrap.
- The remaining call sites matter: a result labeled “recovered” can still leave a particular URL or module name hidden.
- The revised engine, described below, keeps the same severities on these files but recovers far more: 4,048 of 4,048 call sites in the extension and 1,038 of 1,038 in the bootstrap.

### Method: a bounded evaluator, not execution

What lets the scanner read hostile code safely is that its evaluator interprets only a declared subset of the language:

- Literals and templates, arithmetic, bitwise, comparison and logical operators on primitives.
- Constant bindings, literal-object properties, string and array indexing and length.
- `parseInt`, `String.fromCharCode` and a fixed list of string methods.
- Functions whose body is a single return of a supported expression.

Everything else yields "unknown", and unknown propagates. Calls on unknown values, assignments, loops, getters and regular expressions all produce it, and unsupported operations are never handed to the JavaScript runtime. Hard caps bound the work at 20,000 evaluation steps, a depth of 48, one mebibyte per string and 10,000 array elements, and tree walks use explicit stacks so that deeply nested input exhausts a budget instead of the call stack. Whether the subset is interpreted correctly is a separate question, which the known-answer experiment below tests.

### Fallback: printable-text consensus

If the loop is recognized but the checksum cannot be solved, the scanner compares how many call sites produce printable text under each rotation. It accepts a candidate only when it clears a high threshold and the next candidate scores much lower. Concretely, a rotation must decode at least 80% of up to 64 call sites to printable text, and the runner-up may decode at most half as many. This fallback helps with a non-foldable checksum target. It cannot help when every rotation of a plain or keyless base64 array produces readable text.

### Where the `splice` fixture failed

The `splice` fixture revealed a different problem. The scanner never identified its loop as rotation code, so the unresolved-checksum path never ran, and it fell through to the no-rotation case. The mistake was in the scanner's view of the code, before checksum evaluation began.

It was not the first time. An earlier implementation missed a parameterless `for(;;)` rotation loop and decoded 22 files in commercial bundles under rotation zero, with output that looked plausible. That is where the rule came from that an array is never assumed unrotated when recognized rotation code exists. The `splice` fixture showed that the rule protects only against loops the scanner recognizes.

The same trap exists outside the scanner. In my manual work on the extension's components, a first attempt tried every per-call key on every array entry and kept the first printable result. It reported 3,898 of 3,899 entries decoded. Over the first 400 entries, 133 yielded more than one printable candidate, so "first printable match wins" picked a wrong key whenever a wrong one happened to produce text first. I withdrew that result. What worked was recovering the wrapper mappings from the syntax tree, solving the rotation by consensus over all resolved call sites, and requiring two independent anchors to decode to the two expected module names before trusting the decoder. A high printable-decode rate is not evidence of correctness.

## Bypasses: clipboard, Electron, loader and rotation variants

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

Counted by outcome, the nineteen variants against the frozen engine split as follows:

| Outcome against the frozen engine | Variants |
| --- | ---: |
| Evaded a rule or fell below baseline severity | 15 |
| Only partly recovered (4 of 6 call sites) | 2 |
| Decoded under the wrong rotation | 1 |
| Recovered by printable-text consensus | 1 |

Across all twenty-three fixtures, including the baselines, the frozen engine fully detected five: four baselines and the consensus variant.

Some misses are deliberate limits. The evaluator leaves reassignable `var` and `let` values unknown, because following them safely requires tracking assignments and control flow. A clipboard rule that cannot recover the command may not see the features that raise its severity.

Other misses expose unimplemented structures: `execCommand`, a different encrypted-loader API or a split environment-variable name.

The pattern-specific findings are still useful when the observed code is reused. They do not make the behavior hard to rewrite. The companion scanner's broader benchmark in [Part 13](13-scanner-registry-benchmark.md) puts this in context: low alert volume on ordinary packages coexists with poor coverage of generic malware.

## Impact: a plausible wrong string is worse than a gap

When a decoder remains unresolved, the gap is visible. When it returns a plausible but incorrect string, an analyst may follow the wrong lead. The `splice` result therefore deserves its own regression test and a fix that covers additional rotation operations.

There is an independent check for the specific extension. The manually reconstructed key authenticated three encrypted payloads, which confirms the recovered key and ciphertext relationship in those files. The scanner does not perform this decryption, and the authentication result cannot be transferred to another sample merely because its string array looks similar.

Potential fixes include recognizing additional array mutations and refusing to accept an apparently unrotated result for a keyed decoder without supporting evidence. At this stage of the evaluation, those changes were still untested. Any change needs to be checked against the failing fixture, retained artifacts and benign obfuscated software. I kept the engine fixed for these reported results.

For now, treat recovered strings as leads to inspect against their call sites, and check how many sites remain unresolved. A clean scan means the evaluated rules did not find their patterns. It does not mean that the input is safe.

## Hardening: eighteen variants now match their baseline results

After recording those results, I changed the engine to cover the structures the fixtures exposed.

### Evaluator and rule changes

- The evaluator now follows `var` and `let` bindings when it can show they are never reassigned in the declaring scope.
- It handles constant `atob` and `Buffer.from` calls, known-array spreads into functions such as `String.fromCharCode`, and `eval` when the argument is a constant function name. It still leaves other dynamic text unevaluated.
- Clipboard analysis now follows values assigned to mutable variables, copy handlers written as object methods, and the hidden-textarea `execCommand('copy')` flow.
- Electron checks resolve split or decoded environment-variable names and encoded PowerShell.
- Loader analysis follows recognized ciphers to code-compilation sinks such as `Module._compile`, `vm`, `eval` and `Function`, including bindings inside functions.
- For array rotation, the scanner now recognizes additional mutations such as `push(splice(...))` and `unshift(pop())`. Other array reordering inside the rotation function sends the sample to consensus analysis instead of silently assuming rotation zero.
- It also follows decoder calls through aliases and object properties.

### Fixture results

The same nineteen fixtures were run again. Eighteen now match their baseline severity and recovery, including the `splice` fixture, whose strings match the checksum-proven rotation. The remaining case fetches the clipboard command at run time. That command text is absent from the file, so static inspection has nothing to recover.

Counting the fixtures handled overall, the hardened engine went from five of twenty-three to twenty-two.

That figure needs its conditions beside it. I wrote the fixtures together with the fixes, so the pass records regression coverage, not robustness against an adaptive author, and twenty-two of twenty-three is not an evasion rate. The later revised engine left the fixture outcome unchanged at twenty-two, which is the point at which further single-change hardening stopped buying anything measurable.

### Corpus rescans

I rescanned the earlier corpora on the same server and diffed every file against the frozen engine's results. No file on any corpus gained an error-level finding.

- In the calibration corpus, two files in one package newly warned on genuine obfuscation. That package was the only change in the popular-software tier.
- In the recent npm corpus, three files in two packages newly warned.
- The hardened engine reproduced all fourteen expected outputs on the retained UNK_DeadDrop artifacts.
- On the recently changed npm corpus, unresolved arrays dropped from 1,387 to 16. Nine packages whose arrays had been entirely unresolved now exposed license and service endpoints.

Two newly decoded packages imported `child_process`. Static review found ordinary housekeeping in a developer CLI and license-configuration handling in an SAP framework plugin. Neither passed downloaded data to a code-execution sink, and neither was classified as malicious. I did not fetch the remote address found in one package.

One escalation needed to be narrowed during this pass. A first version treated any detached, hidden-window editor relaunch as an error. An AI coding extension uses that shape to start its helper server, so it remains a warning. A malicious extension using the same launch would also receive a warning. The escalation now exempts a launch of the process's own executable, and I narrowed it before the corpus runs.

Throughput was 281 files per second on the calibration corpus after hardening, compared with 264 in the earlier run. That is one measurement on one host, so it cannot show whether the change affected performance. The added warnings and zero additional errors describe the reviewed corpora only.

The new fixtures are regression tests in the [companion repository](https://github.com/KrasForge/unk-scanner), and the [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) reports the frozen and hardened runs separately. These fixtures guided the fixes and now guard against regressions. Coverage of unseen rewrites remains an open test.

## Accuracy: comparing decoded strings with their originals

The `splice` failure raised a practical question: whether the recovered strings were correct. I tested the scanner on fifty harmless files, obfuscated under 72 combinations of javascript-obfuscator's string-array options across a current and an older release. That gave 7,200 samples in which every hidden string had a known original. Because a wrong rotation maps call sites to other genuine strings of the same program, I also aligned the decoded call sites in source order against the original and counted those that fell out of place.

### Method: known answers and a checked metric

The design is reusable, so here are its parts:

- **Inputs.** The fifty files were drawn by seeded sample from 1,325 eligible calibration packages, one file per package. Each had no findings, parsed as a script, was three to thirty kilobytes long and carried at least fifteen distinct string literals.
- **Grid.** The 72 configurations cross string encoding, rotation, wrapper style, the calls transform and index shift. Only the string-array transforms were enabled, so control-flow flattening and dead code add no strings.
- **Scoring.** A produced string counts as wrong only when neither the original nor the obfuscated sample can account for it, directly or as a concatenation.
- **Misplacement.** Set scoring cannot see a wrong rotation of a plain or base64 array, so decoded call sites are aligned in source order against the original's literals and names, and sites outside the longest common subsequence count as misplaced.

I validated that last check against itself. Twenty-five correctly decoded samples gave zero misplaced sites of 5,402, while shifting every decoded value by one array position misplaced 4,240 of 4,903. The held-out set described below also exposed a gap in the reference sequence rather than in the scanner: class field names were missing from it.

### Results for the three engines

No engine returned a wrong or misplaced string, but coverage was weaker than the correctness.

- The frozen engine recovered 68.3% of hidden strings from release 5.9.0 and nothing from 4.1.1.
- The hardened engine recovered 87.2% and nothing. The engines missed the older release's decoder and lost most strings when function wrappers met one option.
- The revised engine, with fixes for those two cases, recovered 99.8% on both releases.

To check those fixes on unseen inputs, I generated a held-out set from twenty new files and five obfuscator releases, three of which the fixes had never seen. Recovery was 99.7% across them. Over 14,400 samples in all, the revised engine decoded 3,265,560 call sites without misplacing one.

The earlier engines were equally exact on the sites they did decode: 492,474 for the frozen engine and 638,574 for the hardened one, none misplaced. Their weakness was coverage, not correctness. The scanner's median time per sample was 15 to 65 milliseconds per release, or 32, 36 and 60.5 milliseconds pooled per engine.

### Published deobfuscators and a version boundary

I scored three published deobfuscators the same way on a 1,440-sample subset. They showed a version boundary that probably matters more to other analysts than my own figures.

- webcrack 2.16.0, which runs the decoder in a sandbox, recovered 98.1% from both releases.
- The two static tools, synchrony 2.4.6 and obfuscator-io-deobfuscator 1.0.6, recovered 98.2% and 98.0% from 4.1.1 output and nothing from 5.9.0.
- Further reproductions place the boundary at release 4.2.2: both static tools decode 3.2.7 and 4.1.1 and fail from 4.2.2 onward. An unreleased commit on obfuscator-io-deobfuscator's main branch already decodes those releases.

- The published obfuscator-io-deobfuscator release also timed out on 144 samples. All of them came from one input, where self-recursive function inlining never converged.
- The two baselines I timed had medians of 290 and 1,045 milliseconds per sample.

Each of the three tools also produced unexplained strings on exactly one input, by three different mechanisms:

- A constant `JSON.parse` call rewritten into an object literal.
- An obfuscator identifier turned into a property name, which is a real change in behavior.
- A constant folded to `undefined`.

The last of those sat in a branch that never runs and appeared on the unobfuscated original too, so the program's output is unchanged and there was nothing to report. I had first described it as a change in output and withdrew that claim after the reproduction. I therefore treat a reproduction against the original as a precondition before filing anything upstream.

### Effect on the public malware set

The same change also mattered for real malware. On the public dataset from [Part 13](13-scanner-registry-benchmark.md), samples producing a warning had risen from 62 to 64 with hardening and then doubled to 128, because many used the older decoder shape. The revised engine again added no error anywhere.

The extra warnings in the registry corpora came from fully decoded commercial extensions and five recent packages. I screened their newly decoded strings without finding anything malicious. None of the malware samples reached error level. The warning reports recovered obfuscation; maliciousness requires examining what the decoded code does.

## Limits: decoder shapes and file selection

Recovery is bounded by the decoder shapes the scanner knows. PolinRider is a separate operation covered later in this series, and on its loaders most payloads lie outside those shapes.

- Of twelve payloads recovered from its newer launcher builds, only one resolved call sites and gave strings.
- One held variant parsed cleanly and returned no findings at all.
- Those loaders arrive under font file names, which the scanner never opens.

A decoder that is near-exact on the shapes it recognizes says nothing about files it never selects.

## Conclusion

The `splice` fixture showed that the most dangerous failure is a confident wrong answer, not a visible gap. Hardening closed eighteen of the nineteen fixture cases without adding an error-level finding on any rescanned corpus, and the revised decoder misplaced no call site across 14,400 samples.

The fixtures guided the fixes, so coverage of unseen rewrites remains open. Defenders should check recovered strings against their call sites, count unresolved sites, and not treat a clean scan as evidence that code is safe. The fixtures are published as regression tests in the companion repository.

The [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) describes the experiment. Scripts and results are in the [companion repository](https://github.com/KrasForge/unk-scanner).
