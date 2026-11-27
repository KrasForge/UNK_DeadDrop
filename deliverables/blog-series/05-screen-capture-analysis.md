---
title: "Beyond Screenshot Strings: Reconstructing Screen Capture"
description: "Frame-comparison symbols in the Go agents, a mandatory Windows capture bundle, and why the screen, not only the disk, is the unit of incident scoping."
date: "2026-11-27"
published: "2026-10-25"
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


I found that the UNK_DeadDrop agents are built for a continuous video feed of the desktop that sends only what changed between frames, not for occasional screenshots. On Windows the installer refuses to deploy without the capture component, so the screen, not only the disk, has to be part of incident scoping.

## Key takeaways

- The Go implant contains symbols for retaining a previous frame, comparing blocks and encoding JPEG data, which fit a frame-differenced video feed.
- The Windows bundle combines screen acquisition, JPEG encoding, MessagePack serialization and WebSocket transport, and its installer treats the capture files as mandatory.
- The Windows agent persists as the hidden scheduled task `GoogleUpdateSupporterNode` with highest available privileges and 999 restart attempts, replaces the Go agent on Windows, and leaves a plain-text log of its servers behind.
- The held agents contain no keystroke logger; the "keylog" matches in the Go binary are the standard library's TLS key-log facility.
- Responders should ask what was shown on screen during the exposure window, not only which files existed.

## Impact: the screen is the unit of scoping

Frame differencing and frame-rate accounting serve no purpose for occasional screenshots. I therefore read these artifacts as a design for a continuous video feed of the desktop that sends only what changed between frames. I have found this capability in no third-party reporting on this actor.

The capability is also missing from the public technique map. MITRE's page for the Contagious Interview group, G1052, does not list [Screen Capture (T1113)](https://attack.mitre.org/techniques/T1113/) in its 12 May 2026 version, which I read on 24 July, or in its 31 July 2026 version, which I read on 20 November. [Part 17](17-two-operations-one-ecosystem.md) weighs that page against everything else I observed.

The practical consequence reverses a common scoping habit. Controls that protect data at rest do nothing against a feed of the desktop. These include an encrypted vault, a hardware wallet that shows its recovery phrase on screen only during setup, and a one-time code that is never saved. In the absence of keystroke logging, the screen covers much of what a keylogger would have captured.

A responder should therefore ask what was shown, typed into a revealed password field or read from a dashboard during the exposure window, not only which files existed. The static artifacts provide no session duration or captured images from which to determine what was actually visible.

## Method: reading symbols and dependencies without a capture session

The Go implant contains symbols for capturing a display, retaining a previous frame, comparing blocks and encoding JPEG data. A separate Windows bundle combines screen acquisition, JPEG encoding, MessagePack serialization and WebSocket transport. I analyzed both statically.

No capture session was recorded. The available evidence comes from the native binaries, the Windows bundle and its installer. Achieved frame rate, bandwidth and desktop access remain unmeasured. The symbol and dependency observations are recorded in [E05](../preprint/evidence/E05.pdf); [E18](../preprint/evidence/E18.pdf) explains why the earlier dependency-only assessment did not rule out capture code.

## Linux Go agent: frame comparison in the symbol table

In the Go binary, I found these capture symbols:

```text
capture.CaptureDisplay    capture.CaptureAndSend
capture.Loop              capture.encodeJPEG
capture.encodeBlocks      capture.blockChanged
capture.copyPrev          capture.frameFPS
```

`CaptureDisplay` and `CaptureAndSend` suggest acquisition and transfer. The more distinctive names are `copyPrev`, `blockChanged` and `encodeBlocks`. They fit a design that retains an earlier frame, compares image regions and encodes changes for transmission. `Loop` and `frameFPS`, together with average-size and average-duration metrics, add evidence of repeated capture and rate accounting.

MITRE ATT&CK groups screen acquisition under [Screen Capture (T1113)](https://attack.mitre.org/techniques/T1113/). Block dimensions and loop frequency remain unmeasured, as does code reachability on a particular host. A Linux process needs access to a usable display session and sufficient permissions before a capture routine can acquire an image.

### Platform differences across builds

The platform picture needs the dependency list and the symbol table read together, because they measure different things. I found these differences between builds:

- The May Linux build still linked X11 screen capture.
- The July Linux build is stripped of the framework's screen-capture, webcam, audio and WebRTC back-ends, yet still contains the capture package's own symbols and error strings.
- The macOS builds, among them the two macOS builds in the set of six Unix builds fetched from the operator's blob host on 12 November, expose the framework's screenshot command.

The Linux difference points to per-platform tailoring over time. The streaming design is compiled into the July build, but whether that July build could acquire frames is not established. The operator's separate Cortex console returns screenshots of the remote browser. macOS victims are therefore best scoped as watched until shown otherwise.

Diffing the July Linux build's dependency set against the public framework's own module file shows the size of the cut. The framework's WebRTC transport, audio capture, webcam capture, video encoding, screen capture, Windows pseudoconsole and desktop bus are all absent, while the operators' own SQLite driver for reading browser databases was already present in May. The July Linux agent is therefore provisioned as a credential-theft and shell tool rather than a surveillance tool. Noise reduction on Linux is a plausible motive, but that motive is my inference.

A build's symbol table is also not the end of its capability. The Go agent speaks the framework's protocol, which includes a `screenshot` command and a plugin channel through which the server can stream a native library into a running agent. Any capability set read from a Go build is a floor rather than a ceiling. [Part 16](16-control-layer-after-october.md) describes the Cortex console, whose own agent I do not hold.

### TLS key logging, not keystrokes

Three other matches in the Go binary were `writeKeyLog`, `KeyLogWriter` and `crypto/tls.(*Config).writeKeyLog`. Their surrounding names identify the Go standard library's TLS key-log facility, which has nothing to do with keystrokes. A count-only search for "keylog" would report a keylogger that is not there.

Across the held Windows, Linux and macOS builds of the Overlord agents and their Node and Python stages, I found no key-listener package and no keyboard-hook interface at all. This covers Windows hook or key-state calls, X11 record or grab interfaces and macOS event taps.

I tested for keylogging rather than assuming its absence, because Microsoft's reporting on Contagious Interview of 11 March 2026 names keylogging through the npm package `node-global-key-listener`. That package is absent from every held stage, as is every other key-listener package.

That negative has a boundary. A separate PowerShell toolkit recovered from a staging repository linked to the same operator personas does run a keylogger through a VBScript runner. It is related to the ECHOES lineage in [Part 9](09-echoes-lineage-image-provenance.md).

The boundary also runs the other way. Huorong analyzed a separate Windows Overlord build on 3 September 2026 with keyboard, clipboard, screen, audio, webcam and hidden-desktop functions. That build has no demonstrated connection to UNK_DeadDrop, and its features cannot turn the negative result for the held material into a positive claim about this operator.

## Windows bundle: capture is a mandatory component

The Windows bundle supplies a separate set of components:

- `node-screenshots` and its native module, for screen acquisition;
- `jpeg-js`, for JPEG encoding;
- MessagePack, for serialization;
- `ws`, for WebSocket communication.

The installer checks for the capture files and refuses to deploy without them. It throws an error that the native module is missing from the bundle, so on Windows the capture component is not optional.

The agent then persists as a hidden scheduled task named `GoogleUpdateSupporterNode`, made to resemble a Google update component. The task runs with highest available privileges and 999 restart attempts. The same Windows Node agent also offers live remote desktop with injected mouse and keyboard input, a hidden shell and clipboard access. The feed is meant for an operator who can act on what it shows.

The Windows dependencies and Go symbols come from different artifacts, yet they implement the same frame-differenced design in two languages. Whether the implementations share code remains unresolved. For the Windows branch, investigators would start with the installed bundle, task action and process session to determine whether capture ran.

## Windows agent: the feed inside a hands-on-keyboard tool

The Windows Node agent, version `1.0.16-node`, is a separate implementation written to the Overlord server's protocol, so one panel drives both it and the Go agent. On Windows it replaces the Go agent rather than running beside it: stage three deletes the Go agent's `Google\agent.exe` and any earlier Node agent before installing this one. It performs no credential, browser or wallet collection of its own. That work stays with the Python and Node components described in [Part 4](04-credential-wallet-collection.md).

### Commands: an operator at the keyboard

The agent's command dispatcher has 39 handlers. I grouped them as follows:

- session control: ping, disconnect, reconnect, uninstall and agent update;
- a hidden interactive `cmd.exe` console, plus script and silent execution in PowerShell, cmd, bash, Python and Python 3;
- process listing and killing through `taskkill /F /T`;
- the full file command set, including an index of every drive and archive export;
- screenshots of all monitors, remote desktop with injected input, and clipboard get and set on command.

The plugin commands are refused with the message `plugins not supported in node agent`. Unlike the Go agent, the Windows agent cannot gain capability at run time through a plugin, so its bundle is the whole of what it can do.

Two author-written modules carry the screen and input work. `lib/screenshot.js` captures every monitor as JPEG through `jpeg-js` and `node-screenshots`. `lib/input.js` handles only synthetic events, such as `desktop_mouse_move` and `desktop_key_down`, for injecting input during an operator-driven remote desktop session. It contains no hook and no capture, which is the code-level reason the agent has no keylogger. It also has no automatic clipboard replacement and no anti-analysis code, and its source is readable.

### Protocol: a deterministic identity and a polite session

The agent connects over WebSocket to `/api/clients/<id>/stream/ws?role=client` with an `X-Agent-Token` header, MessagePack framing and TLS validation turned off. Its first message reports host, user, operating system, version and monitor count, and it pings every 30 seconds. It yields when another user takes the physical console.

The client ID is the SHA-256 of hostname, user, the string `windows` and architecture. The ID is deterministic, so a reinstalled agent on the same machine and account reappears under the same identity in the operator's panel.

### Installation: what a responder will find on disk

The agent installs under `%LOCALAPPDATA%\Google\node-agent\` with a portable Node 20.18.1 downloaded from the official Node.js site, of which only `node.exe` is kept. The directory holds these files:

| File | Role |
|---|---|
| `node.exe` | the portable runtime |
| `update-agent.js` | the agent entry point |
| `run-update-agent.vbs` | launcher that starts the agent with a hidden window |
| `config.json` | server address, resolver URL, credential and client ID |
| `agent.log` | plain-text log with addresses, servers and errors |
| `.agent.lock` | lock file |
| `server_index.json` | the resolver's position in its server list |

The `GoogleUpdateSupporterNode` task runs at logon, hidden, with highest privileges, no time limit and a restart every minute. It runs `wscript.exe` on the launcher, retries through an elevated PowerShell helper, and starts immediately after registration. Self-update comes from `/api/agent-bundle/windows-node.zip` and keeps the configuration and logs.

For a responder, the plain-text `agent.log` is the most useful single file, because it records which servers the agent talked to. The task definition also deserves a full export of its name, action, arguments, working directory, principal, author, triggers and last result. Process-creation telemetry alone cannot prove that registration succeeded, and a task registered through COM leaves no `schtasks.exe` command line at all.

### The only binary is stock code

The operators wrote only the JavaScript and PowerShell layer. The native capture module, `node-screenshots.win32-x64-msvc.node` (700,928 bytes), and the module's `index.js` are byte-identical to the npm registry tarball of `node-screenshots` 0.2.8. Their hashes identify a public package and must not be used as indicators.

### Build history: assembled on macOS, days before delivery

The bundle's own archive metadata dates its construction. Its 24 hand-authored files carry modification times from 21 June to 20 July 2026, apart from 149 dependency files from a single npm install:

1. 21 June: the launcher and the console, process and uninstall modules;
2. 29 June: `package.json` and the input, desktop and command modules;
3. 30 June: `lib/screenshot.js`;
4. 13 July: `update-agent.js` and `lib/server-resolve.js`, which holds the dead-drop URL and was edited on the day the dead drop rotated to new servers ([Part 6](06-gitlab-dead-drop-infrastructure.md));
5. 20 July: `package-lock.json`.

The archive contains two test files and a macOS `.DS_Store`, so it was zipped from a working tree on macOS. The difference between its local DOS timestamps and its UTC extra fields puts the creating machine at UTC-4. The agent's core files date from 13 July, nine days before the 22 July delivery I examined. All 13 resolved URLs in its lockfile point at the public npm registry, so there is no private registry to pivot on.

Later copies show how the operators maintain it. The bundle shipped through the `aazdias` installers, `8a36b018`, is the same build repacked, differing only in lockfile modification times, which is how a repack can be told from a new build. A later stage-three build carried the same 173 files with only two changed: a command module with the same command set, and a file module that adds detached folder-zip jobs and recovery of half-written archives. That change made exfiltration more reliable rather than adding capability.

### Framework features and operator choices

Most of what makes the agent dangerous is stock Overlord. Remote desktop, synthetic input, the interactive shell, capture, and MessagePack over WebSocket are framework features that will also appear in unrelated red-team and criminal deployments. The Google masquerade in the task name and install path, the replacement of the Go agent and the delivery chain are this operator's choices. [Part 12](12-framework-and-collection-boundary.md) draws that boundary across the whole toolkit.

## Detection: the capture rule requires Overlord and four symbols

The [capture-agent YARA rule](https://github.com/KrasForge/unk-scanner/blob/main/rules/yara/deaddrop_capture_agent.yar) requires an Overlord environment marker and four capture-related symbol strings. It locates files carrying that combination. On its own, a match identifies the framework's capture code rather than this operator, since many unrelated parties run Overlord.

In the replay of 26 October 2026 the rule matched 10 of 395 raw or archive-member views drawn from 192 case files. Those views are not independent samples, because several are copies or archive members of the same bytes. It matched nothing in 1,914 local software files, a baseline that cannot establish a fleet-wide false-positive rate. [Part 11](11-detection-engineering.md) describes the replay.

The installer gives a second, Windows-specific string. Its function `winNodeAgentVerifyCaptureBundle` throws `capture native module missing from bundle` or `node-screenshots package missing from bundle` when the capture files are absent.

Desktop access and frame delivery require runtime evidence. On a host, the useful follow-up evidence includes:

- the installed component;
- its process and session context;
- display permissions;
- associated network activity.

For the Windows branch, the `GoogleUpdateSupporterNode` task gives an additional place to look for the executable and arguments used. Its hidden setting and extreme restart count are a stronger marker than the name.

```text
Go implant SHA-256:
ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d
Capture task: GoogleUpdateSupporterNode
```

## Limitations

- No capture session was recorded, so achieved frame rate, bandwidth and desktop access are unmeasured.
- Block dimensions, loop frequency and code reachability on a particular host are unmeasured.
- Whether the July Linux build could acquire frames is not established.
- Whether the Windows and Go implementations share code remains unresolved.
- A newer Windows bundle reported by a third party is not public, so I have not compared it with the builds I hold.
- The Cortex agent is not in hand, so its capture behavior on macOS is known only from the console side.
- The static artifacts contain no session duration or captured images.

## Conclusion

The symbols and dependencies describe a frame-differenced desktop feed in two languages, and on Windows the capture component is mandatory. Combined with remote desktop input, a hidden shell and clipboard access, the feed serves an operator who watches and acts. The Windows agent that carries it was assembled in about a month, replaces the Go agent, and leaves its server history in a plain-text log.

Defenders should scope an exposure by what appeared on screen, not only by what was stored on disk. Secrets that were only displayed, such as a recovery phrase during wallet setup or a one-time code, belong in the exposure assessment. On Windows, the hidden `GoogleUpdateSupporterNode` task with its 999 restart attempts is a concrete place to start.

The capture-agent YARA rule is part of the public scanner repository. A match identifies Overlord capture code, and runtime evidence is still needed to show that capture ran.
