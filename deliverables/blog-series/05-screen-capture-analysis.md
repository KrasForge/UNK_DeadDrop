---
title: "Beyond Screenshot Strings: Reconstructing Screen Capture"
description: "Capture symbols, Windows dependencies and a misleading keylogging lead in the held samples."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://example.com/blog/05-screen-capture-analysis"
kicker: "UNK_DeadDrop · Part 5"
tags:
  - "UNK_DeadDrop"
  - "screen capture"
  - "malware analysis"
  - "reverse engineering"
og_image_alt: "Beyond Screenshot Strings: Reconstructing Screen Capture"
---

When I rechecked the Go implant, three keylog matches initially looked like evidence of keyboard collection. Their surrounding names showed otherwise: they belonged to TLS. Elsewhere, the same examination found capture loops, previous-frame storage and block-change routines. Together with a Windows capture bundle, those artifacts supported a more specific surveillance assessment than the earlier inventory. This post follows the evidence for that assessment and the boundaries that remain without a recorded capture session.

> **Key Takeaways**
>
> - The keylog matches identified TLS internals, not keyboard hooks.
> - Capture-related symbols support a frame-difference streaming design.
> - Windows bundle dependencies and installer checks provide separate evidence of a capture component.
> - No measured frame rate, victim session or successful execution was established.

## The keylogging lead that did not hold

The three matches were `writeKeyLog`, `KeyLogWriter` and `crypto/tls.(*Config).writeKeyLog`. Their context places them in TLS key logging. Counting those strings as keyboard interception would have assigned a capability on the basis of a shared word rather than the implementation consuming it.

That correction does not establish that keylogging is impossible in every build. It narrows the conclusion to the searches and samples examined: those matches did not demonstrate it. A dynamically supplied module or a differently named implementation would require separate analysis.

## What the capture artifacts establish

The Go symbols included the following group:

```text
capture.CaptureDisplay    capture.CaptureAndSend
capture.Loop              capture.encodeJPEG
capture.encodeBlocks      capture.blockChanged
capture.copyPrev          capture.frameFPS
```

A screenshot function on its own would support a much smaller claim, but here the combination of previous-frame storage, block comparisons and frame-rate accounting fits a design that repeatedly captures the display and transmits whatever has changed, which MITRE ATT&CK catalogues under [Screen Capture (T1113)](https://attack.mitre.org/techniques/T1113/).

The Windows bundle independently points the same way, since it contains:

- `node-screenshots` and its native module, for screen acquisition;
- `jpeg-js`, for JPEG encoding;
- MessagePack, for serialization;
- `ws`, for WebSocket communication.

The installer checks for the capture files and raises an error if they are missing. The associated task is named `GoogleUpdateSupporterNode`. Together, these artifacts support a capture-streaming implementation in the examined material, but there is no recorded victim session. Display availability, permissions and the execution path remain conditions for capture to succeed.

One discrepancy also needed resolution. An earlier upstream dependency comparison suggested that the Linux build lacked capture; later symbol examination found positive capture-related evidence. Missing expected dependencies are not enough to rule out an implementation present in the binary.

### Reading the evidence at the right level

| Artifact | What it supports | What remains untested |
|---|---|---|
| Previous-frame and block-comparison symbols | A design consistent with comparing successive captures | Reachability and behaviour in a particular execution |
| JPEG encoding and frame-rate accounting | Encoding and repeated-capture implementation | Achieved frame rate or bandwidth |
| Windows capture, encoding and transport dependencies | A bundle containing components for capture and transfer | Successful acquisition and transmission |
| Installer check and scheduled-task name | An installation requirement and a host artifact | Successful task execution or a recorded session |

These observations are complementary, but their combination is not a runtime trace. The previous-frame and block-comparison names fit an implementation that retains an earlier image and encodes changed regions. The evidence does not establish exact block dimensions, a measured compression ratio or a particular capture cadence, so none is assigned here.

The distinction between Go and Windows evidence also matters. The symbol set belongs to the inspected native artifact; the dependency set comes from a separate Windows bundle. They support capture-related implementation in the examined material, not an assertion that every operating-system build takes the same path.

### Framework lineage and build differences

The public Overlord framework provides a software lineage, not an operator identity. The earlier upstream dependency comparison and the later binary examination answer different questions: what packages appear in selected source metadata, and what implementation-related names are present in the held binary. The positive symbol evidence prevents treating a missing expected dependency as proof of absence, while still leaving platform support and successful invocation unresolved.

### Following up on an endpoint

The recorded task name, `GoogleUpdateSupporterNode`, is a useful exact artifact, but finding it does not show that a screen stream was sent. Investigators would need to establish the installed bundle, the process and session context in which it ran, and associated network activity. Display availability and permissions are material conditions, especially when distinguishing a staged component from one that actually accessed a desktop.

Screen capture also changes the exposure question. File selection concerns stored material; a functioning capture component could expose material displayed during its operation. The static record provides no duration or victim session from which to enumerate that material. Keeping that boundary explicit makes the finding usable without converting capability into an unsupported impact claim.

### Artifact identifier

```text
Go implant SHA-256:
ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d
Capture task: GoogleUpdateSupporterNode
```
