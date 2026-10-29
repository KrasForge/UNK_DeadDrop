---
title: "When a Decoder Returns the Wrong Strings"
description: "A changed array-rotation loop exposed incorrect recovery, eighteen of nineteen small variants evaded a rule, and a hardened engine then closed all but one of them without adding error-level alerts."
date: "2026-10-29"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/14-scanner-recovery-and-bypasses/"
kicker: "UNK_DeadDrop · Part 14"
tags:
  - "UNK_DeadDrop"
  - "deobfuscation"
  - "static analysis"
  - "detection engineering"
---

One test changed how an obfuscated program rotated its string array. The ordinary form moved an element with `push(shift())`; the variant used `splice`. The scanner missed the rotation loop, treated the stored array as already aligned, and returned strings under rotation zero.

This was more serious than an unresolved value. The output looked like recovered evidence but used the wrong array order. A rule that refuses to guess when it recognises an unsolved rotator still fails if it does not recognise the rotator at all.

The [scanner evaluation](../scanner-paper/UNK-Scanner-Paper.pdf) includes nineteen single-change variants built from inert demonstration and loader fixtures. Eighteen evaded the targeted rule, reduced its severity or defeated string recovery. The variants were scanned without executing their contents. They test the boundaries of the evaluated engine, not nineteen additional campaign samples.

## Why the rotation matters

The extension in [Part 3](03-acorn-deobfuscation.md) replaces readable strings with calls through wrappers into an encoded array. Before those calls can be interpreted, the array must be in the order expected by the decoder. A wrong index can still return a string, just not the one the program would use.

The recognised obfuscator pattern contains its own alignment check. A loop decodes several numeric-looking values, combines them using `parseInt`, and shifts the array until a checksum equals an embedded target. The scanner reimplements the decoder and evaluates that checksum for candidate rotations using its restricted evaluator. It does not run the sample's decoder or loop.

For the retained extension and bootstrap, this reached rotations 391 and 261, matching the manual investigation. It decoded 2,139 of 2,140 call sites in the extension and 15 of 17 in the bootstrap. Those results are strong evidence for these files. They are not a correctness guarantee for every program that resembles the pattern.

When a recognised rotation loop has an unsolved checksum, the scanner can try a narrower heuristic: printable consensus across up to 64 call sites. A candidate must decode at least 80% to printable text, while the runner-up must decode no more than half as many. A plain or keyless base64 array cannot be aligned this way when every rotation produces printable strings.

The `splice` variant bypassed both checks. Because the rotation code went unrecognised, the scanner took the no-rotation path before it could decide that the checksum was unsolved. The defect lies at the boundary between pattern recognition and evaluation.

## Small changes, different results

The other variants exposed similar dependencies on syntax and local data flow.

| Tested change | Result in the evaluated engine |
| --- | --- |
| Clipboard builder reached through a `var` alias | Missed |
| Clipboard text encoded, assembled from character codes, stored elsewhere or fetched at copy time | Missed |
| Copy performed through a hidden textarea and `execCommand` | Missed |
| Electron environment-variable name split into fragments or decoded at run time | Missed |
| Electron launched with different hidden-window structures | Warning instead of error |
| Encrypted-loader steps moved into a function or expressed through different compilation, cipher or binding forms | Missed |
| Decoder wrapper reached through a `var` alias or object property | Obfuscation warning remained; affected call sites were not decoded |
| Checksum target could not be folded | Recovered through printable consensus |
| Array rotation expressed using `splice` | Incorrect decoding under rotation zero |

The evaluator deliberately declines reassignable `var` and `let` bindings. Following them safely would require reasoning about writes and control flow, not simply adding another spelling to a lookup. That restriction explains some misses. It does not make them disappear from the detection result: when the copied command or decoder alias remains unknown, the higher-level rule can lose the evidence it needs.

Other misses concern recognised APIs and structure. A clipboard rule that follows `navigator.clipboard.writeText` does not automatically cover an older copy path. An encrypted-loader rule built around AES-GCM authentication and `Module._compile` does not automatically cover another cipher or execution API. Even moving the same loader steps into a function changed the result in the tested fixture.

The variants therefore measure more than obfuscation strength. They show how much the rules depend on the particular organisation of the observed code. Their usefulness is clearest when that organisation is reused; a small rewrite can remove the alert without removing the underlying behaviour.

## Recovery needs an audit trail

For an analyst, the distinction between "not recovered" and "recovered incorrectly" is crucial. An unresolved string leaves a visible gap. A plausible but wrong module name or URL can send the investigation toward a false relationship.

The retained extension has additional checks available. The manually reconstructed key authenticated three encrypted payloads, independently testing the key material assembled from the recovered fragments. The scanner itself does not perform that decryption. Its output must not inherit the authentication result merely because it recognises a similar string array.

Recovery also has a denominator. Reporting a file as recovered can hide unresolved call sites: an array may decode successfully in direct calls while a wrapper reached through an alias still conceals the URL of interest. In the variant tests, the obfuscation warning survived even when the aliased URL and module-name calls were not decoded. Analysts need both the recovered values and the count and location of unresolved sites.

Everything above describes the evaluated engine, which was deliberately left unchanged so that the reported outcomes stay reproducible, but the obvious next question was whether these gaps could be closed without paying for it in noise, so I changed the engine afterwards and measured the result against the same material.

## Closing the variants, and what that does not prove

The fixes generalise the structures the variants had stepped around rather than adding the variants as signatures. The evaluator now treats a `let` or `var` binding as a constant when no assignment anywhere in the file resolves to it, which turned out to need care because minified code reuses short names in unrelated scopes, so each assignment is traced to the scope that declares the name before the binding is trusted. It also decodes `atob` and `Buffer.from(...).toString(...)`, spreads known arrays into calls such as `String.fromCharCode`, and resolves `eval` of a constant function name while still refusing to interpret any other `eval` text. The clipboard rule now collects every value stored into a mutable variable, recognises copy handlers registered as object methods and follows the older hidden-textarea path through `execCommand('copy')`. The Electron rule resolves a variable name that was split or decoded and counts an encoded PowerShell command as hidden execution, while the loader rule now links an embedded payload, any recognised cipher and any code-compiling sink, whether `Module._compile`, `vm`, `eval` or `Function`, through bindings in any scope.

The rotation defect received the two changes the evaluation had proposed. Equivalent steps such as `push(splice(0, 1)[0])` and `unshift(pop())` are now recognised, any other reordering of the array inside the rotation function counts as rotation code, and the stored order is accepted as unrotated only when at least 80% of the sampled call sites decode to readable text, so an unrecognised rotator falls through to consensus instead of silently producing wrong strings. Call sites reached through an alias or an object member are now followed as well. With these changes, eighteen of the nineteen variants reach the severity and recovery of their baseline, and the `splice` variant decodes to exactly the strings of the original fixture under the rotation proven by its checksum. The remaining miss is the command fetched at copy time, which no reading of the file can recover, because the text is simply not there.

Closing gaps is only useful if it does not open new ones, so the hardened engine was run again over all 2.8 million files from the earlier benchmark on the same server and compared file by file with the frozen results. It raised no new error-level finding in any corpus. New warnings appeared in three benign packages: two of them carry genuine obfuscator arrays that were declared with `var` and had previously been skipped, and one has a copy button for a `curl … | bash` installer. The retained campaign artifacts again matched all fourteen expected outputs, and throughput on the calibration corpus was 281 files per second against 264 before, so the extra evaluation costs nothing measurable. String recovery improved more than the alert counts suggest: in the recently changed npm packages, unresolved arrays fell from 1,387 to 16, and the nine packages whose arrays had stayed entirely unresolved now decode to product-licence and service endpoints.

The newly decoded strings had to be screened rather than merely counted, because hidden values are exactly what the scanner is meant to expose. Two packages newly revealed a `child_process` import, and both were read statically in a deobfuscated view without executing anything or fetching the remote address one of them contains. One is a commercial plugin for SAP's application framework whose licence code downloads an encrypted per-customer configuration and parses it as JSON; the other is a commercial developer command-line tool that calls `git` and `npm` for ordinary housekeeping. Neither passes downloaded data to a code-execution sink, and neither was classified as malicious. One change also had to be rolled back in part before the final runs: a first version escalated any detached, windowless relaunch of the editor runtime, which raised an error on an AI coding extension that starts its own helper server exactly that way, so that shape remains a warning and a malicious extension copying it would remain one too.

These results show that the evaluated bypasses were shallow and could be closed without measurable cost in alert volume, which is worth knowing, but they do not show that the scanner is robust. I wrote the variants, the fixes were designed against them, and anyone who knows the new rules can choose the next rewrite, whether a reassigned alias, a sink the rule does not list, or text moved out of the file altogether. The fixtures now run as regression tests in the [companion repository](https://github.com/KrasForge/unk-deaddrop-companion), and the [scanner paper](../scanner-paper/UNK-Scanner-Paper.pdf) reports both engines side by side so that the frozen evaluation and the later hardening are never confused.

The benchmark in [Part 13](13-scanner-registry-benchmark.md) showed low error-level noise, these variants showed how fragile coverage was within the intended delivery class, and the hardening showed that such fragility can be reduced without adding noise, though not eliminated. All three matter when using the [companion scanner](https://github.com/KrasForge/unk-deaddrop-companion): a recovered value is something to inspect against its decoder and call site, and an absent alert is still not evidence that the file is safe.
