---
title: "Where Overlord Ends and the Collection Toolchain Begins"
description: "Overlord build metadata, browser-store selectors, wallet-upload markers and capture components in the Linux agent."
lastUpdated: 2026-11-26
published: 2026-10-25
sidebar:
  order: 12
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/12.png"
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
      content: "Part 12: Where Overlord Ends and the Collection Toolchain Begins"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/12.png"
---



I found that the Linux Go agent is built on the public Overlord framework, and that the credential and wallet layer on top of it belongs to the operators. The framework has no SQLite dependency at all, while the implant adds a pure-Go SQLite driver and two packages, `companywallet` and `browserlogin`, that do not exist in the public code.

## Key takeaways

- The Linux amd64 agent records the module path `overlord-client/cmd/agent`, a `wazero` WebAssembly runtime and `modernc.org/sqlite` in its Go build information.
- A diff against the framework's module file shows a pure-Go SQLite driver with its four dependencies and a byte-size formatter present in the implant and absent upstream.
- Six Unix builds fetched on 12 November carry the operator packages `companywallet` and `browserlogin`, a thirty-five-entry wallet-extension list and a `GUS_` environment namespace.
- The server-side agent token in the current build is byte-identical to the July builds' token, so it survives the rotations that break host-based links.
- For triage, framework markers identify Overlord, while credentials, wallets, seed phrases, the `GUS_` namespace or the delivery chain identify this actor.

## Build: the Go build records an Overlord module path

The Linux Go agent embeds the module path `overlord-client/cmd/agent`, a WebAssembly runtime and SQLite dependencies. Its strings include browser database names, wallet-upload configuration and capture-related symbols. [Exhibit E18](../../evidence/E18.pdf) documents the bounded comparison with selected upstream files, while [Exhibit E05](../../evidence/E05.pdf) records the sample-specific capture findings.

Those components connect a general remote-access framework to the collection functions found in this sample. When I later diffed the agent's recovered dependency set against the framework's own module file, the boundary between the two layers turned out to be sharper than the July comparison could show.

The Linux amd64 artifact is 15,790,242 bytes and has this SHA-256:

```text
ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d
```

I read these fields from its Go build information:

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

### The build timestamp bounds the build only from below

The [Go build-setting documentation](https://go.dev/pkg/runtime/debug/?m=old) defines `vcs.revision` as the checkout revision and `vcs.time` as its associated modification time. The timestamp is therefore version-control metadata that bounds the build only from below, and the binary's compilation time remains unverified. The recorded repository lookup did not locate the embedded revision, leaving the corresponding source checkout unresolved.

![Overlord framework and collection components](../assets/12-framework-boundary.png)

*Figure 1. The agent combines Overlord framework markers with browser, wallet and capture-related components.*

## Boundary: what upstream has and what the operators added

### The upstream files shared generic framework features

The July comparison inspected selected client module and configuration files. It found the shared module path, plugin support and generic transport configuration. It also recorded a newer wazero version in the examined upstream module file than the sample's v1.7.0. The dependency versions differ. Dating the fork or deployment requires additional records.

SQLite-related dependencies and wallet/browser markers were absent from the selected upstream files. Those files were not retained at a pinned revision, preventing a reproducible source diff at the time.

The later diff against the framework's module file settled the question as far as dependencies can. A pure-Go SQLite driver with its four dependencies and a byte-size formatter are present in the implant and absent upstream. The framework has no SQLite dependency at all, so it cannot read a Chromium login database or a Firefox key store on its own. The operators added that driver while keeping cgo disabled, and by extension the credential and wallet layer built on it is theirs.

### The operator layer in the November builds

Six Unix builds fetched on 12 November share one generation and one Go toolchain. They carry no hard-coded server: the only network address in them is the GitLab dead drop the agent reads, covered in [Part 6](../06-gitlab-dead-drop-infrastructure/). They show the additions as two packages that do not exist in the public code, `companywallet` and `browserlogin`.

Counted as entries of the Go function table, which survives symbol stripping, the two packages hold:

- 242 and 106 functions in the macOS builds;
- 210 or 211 and 71 functions in the Linux builds.

The `browserlogin` package holds Chromium master-key derivation, Safari keychain export, Firefox NSS decryption and a credential vault. The same layer carries:

- a thirty-five-entry wallet-extension list;
- a bypass of Chrome's App-Bound Encryption;
- an environment namespace prefixed `GUS_`, whereas every upstream variable is prefixed `OVERLORD_`.

The server-side agent token in the current build is byte-identical to the July builds' token. The dead drop moved, the lure host changed and thirty-six functions were added in between, so the reused credential survives the rotations that break host-based links. The value is not reproduced here.

## Collection: browser stores, wallet selectors, and capture symbols

### Browser stores

String examinations found `Login Data`, `Local State`, `logins.json` and `key4.db`, along with wallet names and extension identifiers. These are browser-store and collection selectors. Together with SQLite, these selectors identify what the agent is built to read. Successful access and decryption on a victim host remain unmeasured.

### Wallet upload

The wallet-related markers include an endpoint setting, a client header and an upload path. The companion's [wallet-agent YARA rule](https://github.com/KrasForge/unk-scanner/blob/main/rules/yara/deaddrop_wallet_agent.yar) combines these with the Overlord module and server-environment markers. A generic framework match would also identify unrelated Overlord deployments. Requiring wallet context narrows the search to files carrying that additional combination.

### Capture

The binary also contains previous-frame, block-comparison and capture-loop symbols, and here the boundary runs the other way. The frame-differenced capture package is the framework's own design. This July Linux build is a stripped one from which upstream's screen-capture, audio, webcam and WebRTC back-ends are absent.

A May Linux build still carried X11 capture, which points to per-platform tailoring over time. The July build has the capture code but not the platform back-ends, and whether it could acquire frames is not established. [The capture analysis](../05-screen-capture-analysis/) examines those symbols and the separate Windows bundle, where capture is mandatory. Display access, code reachability and successful transmission were not reproduced.

### Collection outside the Go agent

The phased JavaScript collection and the Windows Node/Python pipeline occur in separate components of the toolchain. Their functions extend the collection paths beyond the Go executable. On Windows the recovered branch does not use the Go agent at all, and stage three deletes its masquerading executable before installing the Node agent.

## Triage: separating the framework from the actor

Overlord is a public framework that many unrelated parties run, so a practical triage rule follows:

- anything naming remote control, capture, transport, TLS, mutexes or the module path identifies the framework;
- anything touching credentials, wallets, seed phrases, the `GUS_` namespace or the delivery chain identifies this actor;
- an `OVERLORD_` prefix settles nothing on its own, because the operators named some of their own variables to match.

For file hunting, the wallet-agent rule and [capture-agent rule](https://github.com/KrasForge/unk-scanner/blob/main/rules/yara/deaddrop_capture_agent.yar) select different marker combinations. Both remain experimental. A hit identifies content for inspection, and can include source or research material containing those strings.

## Limitations

- The binary's compilation time remains unverified, and the embedded revision was not located in the recorded repository lookup.
- The July upstream files were not retained at a pinned revision.
- Successful access and decryption on a victim host remain unmeasured.
- Display access, code reachability and successful transmission of capture were not reproduced.

## Conclusion

The Linux agent is Overlord underneath, but the SQLite driver, the `companywallet` and `browserlogin` packages and the `GUS_` namespace are the operators' additions. That boundary lets an analyst separate unrelated Overlord deployments from this actor's builds.

The reused agent token is a link that survives infrastructure rotation. For an unexpected installed agent, preserve its hash, configuration, launch mechanism and outbound destinations alongside the matching offsets.
