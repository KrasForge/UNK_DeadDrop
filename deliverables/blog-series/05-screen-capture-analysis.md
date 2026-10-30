---
title: "Beyond Screenshot Strings: Reconstructing Screen Capture"
description: "Frame-comparison symbols in the Linux Go agent, a Windows capture bundle, and the desktop access each requires."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/05-screen-capture-analysis/"
kicker: "UNK_DeadDrop · Part 5"
tags:
  - "UNK_DeadDrop"
  - "screen capture"
  - "malware analysis"
  - "reverse engineering"
og_image_alt: "Beyond Screenshot Strings: Reconstructing Screen Capture"
---


The Go implant contains symbols for capturing a display, retaining a previous frame, comparing blocks and encoding JPEG data, while a separate Windows bundle combines screen acquisition, JPEG encoding, MessagePack serialization and WebSocket transport. Together, these artifacts point to a design for repeatedly capturing and transmitting changes on a desktop. No capture session was recorded. The available evidence comes from the native binary, the Windows bundle and its installer, leaving achieved frame rate, bandwidth and desktop access unmeasured, and the symbol and dependency observations are recorded in [E05](../preprint/evidence/E05.pdf); [E18](../preprint/evidence/E18.pdf) explains why the earlier dependency-only assessment did not rule out capture code.

## Frame comparison in the Linux Go agent

In the Go binary, I found these capture symbols:

```text
capture.CaptureDisplay    capture.CaptureAndSend
capture.Loop              capture.encodeJPEG
capture.encodeBlocks      capture.blockChanged
capture.copyPrev          capture.frameFPS
```

`CaptureDisplay` and `CaptureAndSend` suggest acquisition and transfer, but the more distinctive names are `copyPrev`, `blockChanged` and `encodeBlocks`: they fit a design that retains an earlier frame, compares image regions and encodes changes for transmission, while `Loop` and `frameFPS` add evidence of repeated capture and rate accounting. MITRE ATT&CK groups screen acquisition under [Screen Capture (T1113)](https://attack.mitre.org/techniques/T1113/). Block dimensions and loop frequency remain unmeasured, as does code reachability on a particular host; a Linux process needs access to a usable display session and sufficient permissions before a capture routine can acquire an image.

![Why these symbols suggest repeated capture](assets/05-screen-capture.png)

*Figure 1. Previous-frame storage and block comparison suggest transmission of changed regions between captures.*

### The Go symbols identify TLS key logging

Three other matches in the Go binary were `writeKeyLog`, `KeyLogWriter` and `crypto/tls.(*Config).writeKeyLog`, and their surrounding names identify TLS key logging. The search found no keyboard hook.

## Screen-capture components in the Windows bundle

The Windows bundle supplies a separate set of components:

- `node-screenshots` and its native module, for screen acquisition;
- `jpeg-js`, for JPEG encoding;
- MessagePack, for serialization;
- `ws`, for WebSocket communication.

The installer checks for the capture files and raises an error if they are missing (the associated scheduled task is named `GoogleUpdateSupporterNode`), and these checks make the capture component an explicit installation requirement. The Windows dependencies and Go symbols come from different artifacts, yet they suggest similar capture and transfer functions. Whether the implementations share code remains unresolved. For the Windows branch, investigators would start with the installed bundle, task action and process session to determine whether capture ran.

## The capture rule requires Overlord and four symbols

The [capture-agent YARA rule](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_capture_agent.yar) requires an Overlord environment marker and four capture-related symbol strings. It locates files carrying that combination. Desktop access and frame delivery require runtime evidence. On a host, the useful follow-up evidence includes the installed component, its process and session context, display permissions and associated network activity, while for the Windows branch the `GoogleUpdateSupporterNode` task gives an additional place to look for the executable and arguments used. A functioning capture component could expose information displayed during its operation, including material never saved to a file, but the static artifacts provide no session duration or captured images from which to determine what was visible.

```text
Go implant SHA-256:
ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d
Capture task: GoogleUpdateSupporterNode
```

