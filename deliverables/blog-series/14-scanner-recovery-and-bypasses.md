---
title: "When a Decoder Returns the Wrong Strings"
description: "A changed array-rotation loop exposed incorrect recovery, while eighteen of nineteen small variants evaded a rule, lowered severity or defeated decoding."
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

Possible changes include recognising additional array mutations and checking keyed decodings before accepting an apparently unrotated array. Those are proposals, not demonstrated fixes. They would need to be tested against this defect, the retained samples and ordinary obfuscated software. Broadening recognition can introduce its own collisions; the evaluated engine was left unchanged so the reported outcomes remain reproducible.

The benchmark in [Part 13](13-scanner-registry-benchmark.md) showed low error-level noise, while these variants showed fragile coverage within the intended delivery class. Both findings matter when using the [companion scanner](https://github.com/KrasForge/unk-deaddrop-companion). A recovered value is something to inspect against its decoder and call site. An absent alert is not evidence that the file is safe.
