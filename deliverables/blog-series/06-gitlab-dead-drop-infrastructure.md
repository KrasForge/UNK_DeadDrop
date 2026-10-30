---
title: "Following the GitLab Dead Drop: Configuration Changes and C2 History"
description: "How a GitLab-hosted configuration file let the UNK_DeadDrop operators change servers without new payloads, and what its revision history reveals."
date: "2026-10-29"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/06-gitlab-dead-drop-infrastructure/"
kicker: "UNK_DeadDrop · Part 6"
tags:
  - "UNK_DeadDrop"
  - "C2"
  - "dead drop resolver"
  - "GitLab"
  - "infrastructure"
og_image_alt: "Diagram of the config.json history and separate config-alt.json record"
---


On 13 July 2026, a GitLab commit replaced a list of server names with `api.cklomino[.]ink` and `api.dsfmot[.]xyz`. The retained repository bundle and file history are documented in [E07](../preprint/evidence/E07.pdf). The file held configuration, not a payload.

Its significance came from the client code that read it. A client consulting this resource could obtain its destination without carrying a fixed address in the deployed file. The configuration could therefore change without requiring a new payload hash.

The configuration history records the changing destinations. Certificate and panel observations connect one of those domains to a historical origin address.

The [historical indicator reference](historical-indicators.md) lists every recorded resolver value, the separate unreferenced file, related lure hosts and the limits on each IP association.

The later July installer family used a separate mechanism. Its `upd_m`, `upd_w`, `upda_m` and `upda_w` droppers embedded `api.aazdias[.]ink` as the primary store and `api.fallaazdis[.]ink` as the fallback. Those values came from the recovered dropper configuration, not from the GitLab `config.json` history. The origin association to `207.241.172[.]222` came from dated certificate and passive-scan observations, not a direct fetch from that address.

## The payload fetches `config.json` from GitLab

The payload references this resource:

```text
gitlab[.]com/drop-indexing/tasks/-/raw/main/config.json
```

The repository also contains a separate `config-alt.json` file with another pair of destination strings. Neither retained payload references it, so its name and contents do not show that a client used it.

The recovered JavaScript has its own hard-coded fallback, `api.domatisc[.]ink`, and a resolver function that requests the raw GitLab `config.json` resource. No retained endpoint log confirms that a victim fetched either file. This code pattern is relevant to MITRE ATT&CK's [dead drop resolver technique (T1102.001)](https://attack.mitre.org/techniques/T1102/001/).

A payload with the same hash can receive different destinations depending on when it fetches this resource.

![Timeline of the referenced config.json changes and the separate config-alt.json file](assets/05-resolver.svg)

*Figure 1. The referenced configuration changed in May and July. A separate file was added in June, but no retained payload references it.*

### Five May revisions, then a new server pair in July

The primary file has five recorded revisions on 26 May, beginning with an initial set of `domatisc[.]ink`, `coslyintra[.]online` and `valorecuiting[.]online`, after which subsequent edits remove and restore an entry, introduce `api.` prefixes, and finally leave a set of two hosts. The recorded states after that, in order, are:

1. 26 May 2026, final listed revision of `config.json`: `api.domatisc[.]ink` and `api.coslyintra[.]online`.
2. 1 June 2026, separate file `config-alt.json`: `api.onoplainai[.]ink` and `api.migadyn[.]info`. Its use by the recovered client is unestablished.
3. 13 July 2026, about 07:10 UTC, `config.json`: `api.cklomino[.]ink` and `api.dsfmot[.]xyz`.

Commit `c3c71d65` replaces the primary destination set left by the May revisions. The retained history contains six commits to `config.json` and one to `config-alt.json`. The latter is a separately recorded resource, not an evidenced client fallback.

The configuration resource lets a destination change independently of the payload. It does not show how each client handles that change. A client that fetches the file again may receive a new address, while one using a cached destination may continue trying the old server. The retained history contains no client execution trace to resolve that behavior.

Blocking a destination can interrupt traffic, while a client that consults this configuration resource may receive another address. Connection records are needed to identify the destination each client used.

## A July hostname linked to a reported origin

The resolver history identifies the hostnames supplied to clients. Historical scan records provide a separate view of the services behind those names. July scan notes associate `207.241.172[.]222` with C2 and administration services. They record a certificate naming `api.cklomino[.]ink` and a third-party bare-IP scan that returned a Subtensor sign-in panel. The raw scan responses and certificate were not retained. The panel HTML and JavaScript available for inspection were retrieved from `api.domatisc[.]ink`, so they cannot independently reproduce the reported response from the bare IP.

The panel adds an application-level association to the certificate evidence. Further relationships came from certificate facets, passive DNS and reverse-DNS fields. These observations came from research-service records; the origin analysis did not directly scan the server or log in. [E20](../preprint/evidence/E20.pdf) and [E21](../preprint/evidence/E21.pdf) record the source and limits of those historical associations.

The July observations associated `207.241.172[.]222` with C2 and administration, `170.205.31[.]182` with lure hosting, and `23.137.105[.]75` with earlier C2 infrastructure. These roles describe the recorded periods; current availability and ownership were not checked.

### The SSH host-key search found no new address

The saved service enumeration listed SSH, HTTP and HTTPS. Its SSH profile included a host key, banner and handshake information, but these had different value as search pivots. The common OpenSSH banner and handshake fingerprint matched broad populations of hosts. The more selective host key returned only the address already known. That negative search result does not prove the operation had no backup host.

The reported panel response did not enumerate every tenant at the address. Other services may have shared the address, so an IP block could affect unrelated traffic.

### The 23 July certificates added hostnames

The 23 July certificate enumeration added names that were absent from the inspected payloads: a `dashboard` host on the cklomino base, `dev` and `hr` mail subdomains on lure domains, and a `hiring` host alongside a career-themed API. The [indicator reference](historical-indicators.md) records the names and first-issuance dates. These records identify certificate names, not proof that each host served a malicious application.

The certificates did not provide a cross-domain link. Subject alternative names stayed within individual registered bases, with combinations of the base, wildcards and subdomains such as `api.`, `www.` and `email.`. No retained enumeration entry combined two bases in one certificate. Wildcards also mean that a new subdomain can appear without a new certificate-log entry.

Timing offered more context. Certificates for four bases were first issued on 13 July, the date of the resolver's change to `api.cklomino[.]ink` and `api.dsfmot[.]xyz`.

On 23 July, `aazdias[.]ink` and `fallaazdis[.]ink` were registered about six minutes apart through the same registrar and privacy service, with the same Cloudflare nameserver pair. Their primary-and-fallback naming repeats the earlier `aavzx[.]ink` and `fallbaav[.]ink` arrangement. The current stores, a new dashboard host and several older lure domains also received certificates that day.

Shared panels and certificate automation can produce this cadence across unrelated customers. The timing therefore supplements the code and configuration relationships; it cannot establish a cluster on its own. These registration and enumeration observations come from restricted 23 July records and are discussed in the [paper](../preprint/UNK_DeadDrop-Preprint.pdf), but are not independently reproduced in the public evidence exhibits.

A sweep of two /23 ranges belonging to the hosting provider covered about a thousand addresses; 291 exposed services. The provider used ordinary shared hosting. About twenty unrelated tenants ran services on port 3000, while the free scan dataset returned no results for the agent's port 5173 in either range.

Those observations make port-based hunting a poor discriminator: port 3000 was common among unrelated tenants, and the dataset did not cover the agent's port. The results come from research services and have not been refreshed since 24 July.

Part 7 follows the target-acquisition tooling behind the two SQLite pools.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
