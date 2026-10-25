---
title: "Following the GitLab Dead Drop: Configuration Changes and C2 History"
description: "How a GitLab-hosted configuration file let the UNK_DeadDrop operators change servers without new payloads, and what its revision history reveals."
lastUpdated: 2026-10-25
sidebar:
  order: 6
---


On 13 July 2026, a GitLab commit replaced a list of server names with `api.cklomino[.]ink` and `api.dsfmot[.]xyz`. The file held configuration, not a payload; its significance came from the client code that read it. A client consulting this resource could obtain its destination without carrying a fixed address in the deployed file. The configuration could therefore change without requiring a new payload hash.

Following that dependency led from the collector to the configuration history, then to certificate and panel observations around a historical origin address. It also showed why a list of domains alone gives an incomplete picture of the infrastructure.

> **Key Takeaways**
>
> - The payload reads its destinations from `config.json` in a GitLab repository, which also holds a `config-alt.json` fallback set, so servers can change without a new payload hash.
> - The primary file had five revisions on 26 May and was switched to `api.cklomino[.]ink` and `api.dsfmot[.]xyz` on 13 July 2026.
> - A certificate and a Subtensor sign-in panel historically associated `207.241.172[.]222` with the C2 and administration services.
> - A Go `vcs.time` value five minutes and thirty-four seconds after a phishing message is version-control metadata, not proof of when the implant was compiled.

## The resolver

The payload references this resource:

```text
gitlab[.]com/drop-indexing/tasks/-/raw/main/config.json
```

The history also contains `config-alt.json`, identified as a fallback set. The repository therefore publishes destination values separately from the executable code. MITRE ATT&CK describes the general technique as a [dead drop resolver (T1102.001)](https://attack.mitre.org/techniques/T1102/001/).

Two relationships need preserving: the payload's dependency on the configuration resource, and the value that resource held at the time of a relevant execution. A hash-only inventory captures neither.

![Two configuration files, separate histories](../assets/05-resolver.png)

*Figure 1. Two configuration files, separate histories. The sequence does not establish fallback selection or client refresh behavior.*

[Open full-size vector diagram](/UNK_DeadDrop/diagrams/05-resolver.svg). Sources: [E07](../../evidence/E07.pdf), [E20](../../evidence/E20.pdf), [E21](../../evidence/E21.pdf).

### Reconstructing the changes

The primary file has five recorded revisions on 26 May, beginning with an initial set of `domatisc[.]ink`, `coslyintra[.]online` and `valorecuiting[.]online`, after which subsequent edits remove and restore an entry, introduce `api.` prefixes, and finally leave a set of two hosts. The recorded states after that, in order, are:

1. 26 May 2026, final listed revision of `config.json`: `api.domatisc[.]ink` and `api.coslyintra[.]online`.
2. 1 June 2026, fallback file `config-alt.json`: `api.onoplainai[.]ink` and `api.migadyn[.]info`.
3. 13 July 2026, about 07:10 UTC, `config.json`: `api.cklomino[.]ink` and `api.dsfmot[.]xyz`.

The July change is associated with commit `c3c71d65`; it replaces the primary destination set left by the May revisions. The fallback file has a history of its own, so both files should be preserved rather than inferring the configuration from one URL. There are six listed commits to the primary file and one to the fallback. Repository-wide counts in other notes cover a different scope. In reconstructing this history, the queried file matters as much as the number of results.

### What the resolver changes for response

The configuration resource lets a destination change independently of the payload. It does not show how each client handles that change. A client may read the new value at startup; one using a cached address may keep trying the old destination. A failed connection could trigger a refresh, use a fallback or simply retry. Those are implementation and runtime questions beyond the fact that the file changed.

The early case narrative called domain takedowns ineffective. That was too categorical: blocking a destination can interrupt traffic, while the configuration resource may supply another address to clients that consult it. Response should establish whether an affected client has a usable destination, how it obtains one and whether it connects.

## From the host list to the origin

The July analysis associated `207.241.172[.]222` with C2 and administration services. A certificate observed at that address named `api.cklomino[.]ink`. A third-party scan of the bare IP also returned a Subtensor sign-in panel, providing application content to compare with related panel observations.

The panel adds an application-level association to the certificate evidence. Further relationships came from certificate facets, passive DNS and reverse-DNS fields. These observations came from research-service records; the origin analysis did not directly scan the server or log in.

In the wider July analysis, `207.241.172[.]222` was cast as the C2 and administration origin, `170.205.31[.]182` as lure hosting and `23.137.105[.]75` as earlier C2 infrastructure. These are historical associations, though, and they do not imply that every relationship existed at the same time, that the addresses were controlled exclusively by the same person, or that they still hold those roles today.

### Why the host fingerprint was not an attribution result

The saved service enumeration listed SSH, HTTP and HTTPS. Its SSH profile included a host key, banner and handshake information, but these had different value as search pivots. The common OpenSSH banner and handshake fingerprint matched broad populations of hosts. The more selective host key returned only the address already known. That negative search result does not prove the operation had no backup host.

The original note called the origin dedicated and said an IP-level action would have no collateral effect. The available observations could establish neither claim. A panel on the bare IP strengthens a service association without revealing every tenant or ownership change outside the scan's coverage. The certificate's validity dates describe that certificate, not the operation's start or end.

### A five-minute timeline error

The infrastructure and build histories show two close timestamps: a phishing message recorded at 01:08:32 UTC on 21 July, followed by a Go `vcs.time` value of 01:14:06 UTC. The gap is five minutes and thirty-four seconds. An early note described an implant compiled shortly after the message, but `vcs.time` records version-control metadata, not a certified compile time.

The correlation is worth retaining with the field named correctly. As with domain registrations, configuration changes and archive timestamps, label each value by the event it actually records.

Several of my infrastructure notes evolved in a similar way, moving from an early view centred on a single host towards additional addresses and later origin observations, and keeping their dates intact avoids collapsing a sequence of changing findings into one timeless network.

### What to retain from a resolver investigation

Preserve more than a list of domains: record the resource location, file-specific revisions, selected values, observation dates and client code that consumes them. For each origin association, note whether it came from resolution, a presented certificate or matching application content. That record stays useful after a destination disappears and lets another analyst test each relationship instead of inheriting an unexplained “C2” label.

Part 7 examines the target-acquisition tooling and its two SQLite pools. Part 8 follows the separately recovered administration frontend, including its delivery-repository monitor and wallet-management screens.
