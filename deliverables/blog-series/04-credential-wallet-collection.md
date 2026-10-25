---
title: "Inside the Collector: Browser Credentials and Wallet Files"
description: "How the collector selects browser stores, wallet material and recovery files, and what limits its reach."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://example.com/blog/04-credential-wallet-collection"
kicker: "UNK_DeadDrop · Part 4"
tags:
  - "UNK_DeadDrop"
  - "infostealer"
  - "credentials"
  - "crypto wallets"
og_image_alt: "Inside the Collector: Browser Credentials and Wallet Files"
---

The collection code reaches beyond browser passwords. Its third upload variant searches the home directory for filenames associated with seeds, recovery material, credentials and tokens, while another selector includes encrypted KeePass databases. The source also sets explicit traversal budgets and skips selected inaccessible directories. Following those decisions shows what the collector attempts to take and why selecting a file is only the beginning of assessing exposure.

> **Key Takeaways**
>
> - Browser-database collection and recovery of plaintext credentials are separate steps.
> - The phase-three sweep selects filenames and extensions within explicit time and traversal budgets.
> - The generic extension selector includes encrypted KeePass databases; no dedicated unlock routine was established.

## Browser collection has several steps

The Windows collection path splits across a Node agent, a coordinator and a Python browser-decryption component. Copying a browser database is one step; recovering its encryption material and extracting usable credentials is another. MITRE ATT&CK classifies this activity as [Credentials from Web Browsers (T1555.003)](https://attack.mitre.org/techniques/T1555/003/).

The Python source handles DPAPI-related key recovery and browser elevation services associated with App-Bound Encryption. Its comments and staging logic describe caller-path requirements, helping explain why the pipeline attempts elevation and prepares a particular execution environment. But a copied `Login Data` file is not a set of plaintext passwords, and an elevated process does not prove browser decryption succeeded. The investigation found no endpoint telemetry showing what the attempts yielded. Wallet selectors extend the scope beyond browser stores; Part 8 examines corresponding mnemonic and ColdKey fields in the administration frontend.

![A selected file is only the first step](assets/04-collection.png)

*Figure 1. A selected file is only the first step. Collection, decryption and completed upload are different claims.*


### Phase three searches filenames

The large JavaScript collector accepts three upload variants, `main`, `pass` and `phase3`, and it is the third of these that walks the home directory looking for candidate files whose names and extensions match its selection logic. The recorded filename expression includes:

```text
key / private / wallet / phrase / passphrase
seed / mnemonic / secret / credential
password / backup / recovery / keystore
API key / token
```

The selector also includes configuration and text formats such as JSON, YAML, TOML, INI, property lists and `.env` files. Calling it only an “environment-file sweep” would understate its range. Selection is lexical: a wallet backup or recovery note can match by filename alone, without the code understanding its contents. Conversely, useful data under a nonmatching name can be missed.

The search also runs within explicit budgets, which in the inspected source default to:

- 8 minutes for the whole phase;
- 2 minutes for each root directory;
- 15 seconds for any single directory read;
- 2,500 directories visited;
- a walk depth of 6;
- 500 candidate files.

Several of these settings can be overridden through environment variables, and the skip list covers selected system locations, dependency trees, caches and cloud-storage directories, all of which makes the source considerably more specific than any generic claim that the malware "steals all files".

A helper checks whether selected protected top-level directories are readable, and the walker skips any that fail the probe, caches the results, and has a timeout path. The control flow is effectively:

```text
Is this a protected top-level directory on macOS?
    No  -> continue normal traversal
    Yes -> probe readability
              readable -> continue
              failure or timeout -> skip
```

The code is designed to avoid pursuing locations it cannot readily access, which is a much narrower behavior than a TCC bypass, because permissions the process has already been granted can still change what it is able to reach. The earlier claim that the implementation could never produce a privacy prompt was, in hindsight, too broad.

### KeePass is caught by an extension selector

Two of the larger JavaScript payloads include `.kdbx` in a generic set of private-key extensions:

```javascript
const KEY_EXTENSIONS = new Set([
  ".key", ".pem", ".asc", ".pfx",
  ".p12", ".ppk", ".gpg", ".kdbx"
]);
```

This selector can collect an encrypted KeePass database without a dedicated KeePass module. The examined code does not establish a KDBX parser, master-password recovery routine or in-malware unlock operation. Context also matters when reviewing strings: `kdbx` buried in an encoded blob is not equivalent to `.kdbx` in a file-selection set. The relevant question is where the string occurs and what code consumes it.

## Uploads and the framework boundary

The transfer code uses a default 2 MiB chunk size and a five-retry setting. A separate upload-until-success routine repeats attempts with delays capped at 120 seconds. The inspected HTTPS request path also disables certificate verification. These settings describe intended delivery behavior; retries do not guarantee transfer if the destination is unreachable.

Other capabilities come from the public Overlord framework. Its module path, WebAssembly runtime and transport features are lineage markers; they do not implicate the framework's authors or every deployment. The bounded upstream comparison found SQLite-related dependencies and wallet/browser-collection markers in the samples that were absent from the selected upstream files. This supports sample-specific extensions relative to that comparison, not a claim about every framework version. The companion's [wallet-agent YARA rule](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_wallet_agent.yar) combines framework and environment markers with wallet-related strings, while its [stage-three collector rule](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_stage3_collector.yar) targets the recovered source. A match does not establish that the collector ran or completed an upload.

## From selected files to exposure

The collection inventory needs to be read alongside the access conditions. A filename match identifies a candidate; permissions and traversal limits determine whether the process can reach it; and encryption can still protect its contents after collection. The KeePass selector makes that distinction particularly visible, but the same reasoning applies to browser stores and wallet backups.

For response, the useful questions are which component ran, which phase it reached, and which files were accessible in that execution context. The source does not provide a victim-side inventory or a record of completed uploads. Its retry logic describes persistence in attempting a transfer, not proof of delivery.

The next post examines a separate exposure path: screen capture. That finding rests on capture-related symbols and bundle components rather than the file selectors examined here.

```text
Upload variants: main, pass, phase3
Configuration: GUS_UPLOAD_CHUNK_SIZE, GUS_KEEP_AGENT_STATE
Large JavaScript payload SHA-256:
694626bed2df1f0d0026a3f7ead7692b44c7e73041cdd799b79a025335533cdc
```
