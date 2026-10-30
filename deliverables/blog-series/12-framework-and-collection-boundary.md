---
title: "Overlord markers in the Linux agent's collection code"
description: "Overlord build metadata, browser-store selectors, wallet-upload markers and capture components in the Linux agent."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/12-framework-and-collection-boundary/"
kicker: "UNK_DeadDrop · Part 12"
tags:
  - "UNK_DeadDrop"
  - "Overlord"
  - "reverse engineering"
  - "software provenance"
og_image_alt: "Where Overlord Ends and the Collection Toolchain Begins"
---


The Linux Go agent embeds the module path `overlord-client/cmd/agent`, a WebAssembly runtime and SQLite dependencies. Its strings include browser database names, wallet-upload configuration and capture-related symbols. [E18](../preprint/evidence/E18.pdf) documents the bounded comparison with selected upstream files, while [E05](../preprint/evidence/E05.pdf) records the sample-specific capture findings. Those components connect a general remote-access framework to the collection functions found in this sample.

## The Go build records an Overlord module path

The Linux amd64 artifact is 15,790,242 bytes and has this SHA-256:

```text
ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d
```

Reading its Go build information yielded these fields:

```text
path                 overlord-client/cmd/agent
module               overlord-client (devel)
wazero               v1.7.0
modernc.org/sqlite    v1.34.5
CGO_ENABLED          0
GOARCH               amd64
GOOS                 linux
vcs.revision         056221e342357056c8539585806f76632660e414
vcs.time             2026-07-21T01:14:06Z
```

The module path connects the binary to the Overlord agent codebase. The `wazero` dependency supplies a WebAssembly runtime, consistent with the framework's plugin support. SQLite provides local database functionality, which becomes relevant alongside the browser-store markers elsewhere in the file.

The [Go build-setting documentation](https://go.dev/pkg/runtime/debug/?m=old) defines `vcs.revision` as the checkout revision and `vcs.time` as its associated modification time. The timestamp is version-control metadata; the binary's compilation time remains unverified. The recorded repository lookup did not locate the embedded revision, leaving the corresponding source checkout unresolved.

![Framework lineage and collection evidence](assets/12-framework-boundary.png)

*Figure 1. The agent combines Overlord framework markers with browser, wallet and capture-related components.*

### The upstream files shared generic framework features

The July comparison inspected selected client module and configuration files. It found the shared module path, plugin support and generic transport configuration. It also recorded a newer wazero version in the examined upstream module file than the sample's v1.7.0. That difference establishes a dependency mismatch, but cannot date a fork or deployment.

SQLite-related dependencies and wallet/browser markers were absent from the selected upstream files. Those files were not retained at a pinned revision, preventing a reproducible source diff. Other versions, forks and plugins were not exhaustively compared, and the authorship of these components remains unresolved.

## Browser stores, wallet selectors, and capture symbols

String examinations found `Login Data`, `Local State`, `logins.json` and `key4.db`, along with wallet names and extension identifiers. These are browser-store and collection selectors. Their presence alongside SQLite is more informative than a database dependency alone, although it does not demonstrate a successful read or decryption on a victim host.

The wallet-related markers include an endpoint setting, a client header and an upload path. The companion's [wallet-agent YARA rule](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_wallet_agent.yar) combines these with the Overlord module and server-environment markers. A generic framework match would also identify unrelated Overlord deployments; requiring wallet context narrows the search to files carrying that additional combination.

The binary also contains previous-frame, block-comparison and capture-loop symbols. These provide evidence of capture-related implementation despite the absence of expected packages in the selected upstream dependency files. [The capture analysis](05-screen-capture-analysis.md) examines those symbols and the separate Windows bundle. Display access, code reachability and successful transmission were not reproduced.

The phased JavaScript collection, GUS-prefixed configuration and Windows Node/Python pipeline occur in separate components of the toolchain. Their functions extend the collection paths beyond the Go executable. They cannot all be assigned to changes in one agent's source.

For file hunting, the wallet-agent rule and [capture-agent rule](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_capture_agent.yar) select different marker combinations. Both remain experimental. A hit identifies content for inspection, and can include source or research material containing those strings. For an unexpected installed agent, preserve its hash, configuration, launch mechanism and outbound destinations alongside the matching offsets.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
