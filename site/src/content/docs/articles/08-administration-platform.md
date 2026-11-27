---
title: "Inside rms-platform: Delivery Monitoring and Wallet Administration"
description: "What seventy recovered frontend modules reveal about repository monitoring, wallet workflows and authorization limits."
lastUpdated: 2026-11-27
published: 2026-10-25
sidebar:
  order: 8
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/08.png"
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
      content: "Part 8: Inside rms-platform: Delivery Monitoring and Wallet Administration"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/08.png"
---



I recovered seventy frontend modules of an operator application called rms-platform from a development deployment at `dashboard.cklomino[.]ink`. The client combines mail views, repository availability checks and wallet-management controls with mnemonic and ColdKey fields, while the recipient addresses of a claim never leave the backend.

## Key takeaways

- The recovered client contains mail metrics, inbox and outbox views, auto-reply controls, repository monitoring and wallet import, refresh, preview, claim and bulk-claim actions.
- Mnemonic and ColdKey fields, a miner-request column and Subtensor theming converge on Bittensor validators and miners, with EVM and Aptos wallets secondary.
- My read of all seventy modules found no cryptocurrency address and no service key, because claim recipients are supplied by the backend at claim time.
- The hard-coded super-administrator address `eros1030109@gmail[.]com` also appears in lure-domain DMARC records and the dead drop's commit history.
- The back-office dashboard moved with the rest of the operators' hosting estate, from Liga Hosting in June 2026 to the October lure fleet, and its Django debug page shows the same `rms-platform` code base running there as root.

## Impact: the console that sits behind the lures

A development deployment at `dashboard.cklomino[.]ink` exposed seventy frontend modules for an application called rms-platform. The recovered client combined mail views, repository availability checks and wallet-management controls. Its wallet views include mnemonic and ColdKey fields, plus import, preview and claim actions.

The backend implementation and its stored records were not recovered. By November, however, two outside records had placed the back office it talks to on a timeline and tied it to a persona. The console is therefore no longer an isolated artifact.

## Method: following the Vite server's module imports

I followed imports exposed by the Vite development server and preserved seventy frontend modules. Their embedded source maps included the original TypeScript comments. The acquisition followed only modules loaded by the application and involved no login or call to the authenticated data API.

The deployment gave itself away. The page loaded `/@vite/client`, `/@react-refresh` and `/src/main.tsx` as raw, unbundled TypeScript, the signature of a development server rather than a production build. The development-mode JSX metadata also embeds the absolute build path, `/root/rms-platform/apps/admin/client/src/main.tsx`. That one string gave the project's codename, a monorepo layout with sibling applications under `apps/`, among them an admin server, and the fact that it is built as root. An unrelated public records-management project shares the codename and has nothing to do with the operators.

The recovered application calls itself `rms-platform`. Its client contains:

- mail metrics, inbox and outbox views;
- templates and auto-reply controls;
- a task board;
- database tables;
- wallet-management components.

The source references `/api/github-jobs-check/`, `/api/db/...` and `/api/admin/wallets/{refresh,preview,claim,claim-all}/`. These are strings in the client, not observed requests. The related [historical indicator reference](../../indicators/) records the exact route forms. The [evidence index](../../artifacts/) lists hashes for the recovered modules and related samples, while the retained client excerpts are in [E06](../../evidence/E06.pdf) and [E09](../../evidence/E09.pdf).

![What the recovered client makes visible](../assets/06-administration.png)

*Figure 1. The recovered frontend connects mail views, repository monitoring and wallet-management controls.*

## Delivery monitoring: a view of repository availability

One view tracks repositories by `clone_url`, displays availability labels and offers refresh controls through `/api/github-jobs-check/`. The feature fits the delivery history, since repositories can disappear, move or be replaced. A status view could help monitor locations used to distribute lures or payloads. No backend event history was recovered to show whether a repository suspension triggered an alert or a replacement.

The labels are `live`, `down`, `fresh` and `dead`, and the view refreshes automatically. With it the operators can learn within minutes that a delivery repository has been suspended and move to a fresh account. For anyone requesting takedowns, that argues for removing a cluster of repositories at once rather than one at a time.

### The mail view keys a target on a GitHub user

The mail side carries sent, sent-today, replies-today and auto-replies-today counters over `email_inbox`, `email_outbox` and `email_templates` tables. Its email table has a `github_username` column, so the console models a target as a GitHub user, which matches the harvester of [Part 7](../07-developer-target-harvesting/). A database browser over the collected tables, including an `access_token` store, has its own backup endpoint.

### The back office moved with the hosting estate

Passive resolution history places the back-office dashboard that serves this console, under the name `dashboard.asteara[.]org`, at these locations:

1. at Liga Hosting from 8 June 2026;
2. on an Advin address by 29 June;
3. behind Cloudflare under a second name from 28 July;
4. from 5 October on `170.205.30[.]27`, inside the operators' October lure fleet.

The back office therefore moved with the rest of the estate rather than standing apart from it.

| From | Name | Address |
|---|---|---|
| 8 June 2026 | `dashboard.asteara[.]org` | `146.19.215[.]187` (Liga Hosting, AS201131) |
| 29 June 2026 | `dashboard.asteara[.]org` | `185.147.159[.]187` (Advin, AS22295) |
| 28 July 2026 | `dashboard.gaganata[.]ink` | behind Cloudflare |
| 5 October 2026 | `online.dokamacto[.]xyz` | `170.205.30[.]27` |

*Table 1. The back-office dashboard's four homes, from passive resolution history.*

The retired bases are gone: `asteara[.]org` and `gaganata[.]ink` no longer have nameservers. The first address is no longer the operators'. Liga Hosting is a game-server host, and from September 2026 `146.19.215[.]187` answered as a FiveM game server, so it belongs on a dated historical list and not on a live blocklist.

### The Django debug page names the same code base

The current host identifies itself. A scanner's capture of `170.205.30[.]27:8000` shows a Django `NoReverseMatch` error at the root, because the home template links a logout route that the URL configuration does not define. The error page discloses:

- Django 6.0.7 on Python 3.12.3 with `DEBUG = True`;
- a process running as root from a virtualenv under `/root`;
- the failing view at `/root/rms-platform/apps/admin/server/views.py`, rendering `/root/rms-platform/apps/admin/templates/home.html`.

That is the same monorepo as the client I recovered in July from `/root/rms-platform/apps/admin/client`, now with a server-rendered admin beside the Vite client. The back office was relocated rather than rebuilt, and it is run carelessly. Django prints its route list only on 404 pages, and this instance fails earlier, so the routes are not visible.

### A database user links the back office to a persona

In November, [Stormshield's Trigram report](https://www.stormshield.com/news/cti-trigram-campaign/) described a Django back office behind the same kit and named the database user `silviattech1129`. The same handle appears in the author address of a commit to the replacement dead-drop repository of October ([Part 16](../16-control-layer-after-october/)). It also binds the "Silvio Silva" persona to a 2025 launchpad presentation.

The relay commit, `6b840143`, is authored by "Silvio Silva" with the address `silvia.ittech1129@gmail[.]com`. One naming thread therefore runs through the back-office database, the dead-drop relay and the `diobenu2silva[.]com` launchpad, which was also deployed in development mode. The binding rests on a configuration credential and a commit author rather than on co-occurrence. No GitHub or GitLab account exists under either name. A Telegram handle that Stormshield paired with it returned no result by 12 November, the ordinary fate of these handles.

## Wallet administration: mail, tasks and claim controls

The wallet interface contains import, refresh, preview, claim and bulk-claim actions, and the client references routes including:

```text
/api/admin/wallets/refresh/
/api/admin/wallets/preview/
/api/admin/wallets/claim/
/api/admin/wallets/claim-all/
```

The collection paths and their relationship to the dynamically selected server are listed in the [historical indicator reference](../../indicators/). Mnemonic and ColdKey fields, Bittensor-related interface language, and references to EVM and Aptos connect the intended wallet workflow to material targeted by the collectors. The collectors select wallet material that corresponds to these interface fields.

A cold-key field in the wallet import, a miner-request column in the mail table and the Subtensor theming converge on Bittensor validators and miners. EVM and Aptos wallets are secondary.

### Claim recipients never reach the victim's machine

No transaction records accompanied the frontend, and the client could not have yielded them. The recipient addresses of a claim are supplied by the backend from a server-side configuration at claim time and never reach the victim's machine. No sample detonation recovers them. My read of all seventy modules found no cryptocurrency address and no service key. That is the main reason the operation's cash-out remains untraced.

The routes that need no victim are exhausted as well. No public source has published a receiving address for this operation. The campaign's domains and the operator wallets I knew returned no hits in the public scam and phishing databases I could query, and the published indicator sets carry no address. Searches for 2026 Bittensor coldkey drains found only the compromised PyPI `bittensor` package of July 2024, a different vector at a different time. Any route to the receiving address now starts from a confirmed victim wallet.

### The mail side turns the list into conversations

The mail side, with its replied status and auto-reply endpoint, is where the untargeted list of [Part 7](../07-developer-target-harvesting/) turns into selected conversations. The sender and harvester tools were recovered separately, and nothing I hold shows this backend reading their pools.

## Authorization: the `SuperAdmin` check lives in the client

The client helper grants super-administrator treatment when either a user flag is set or an email comparison matches. These checks control frontend navigation and protected routes, including the wallet page and its sidebar entry.

The hard-coded address is `eros1030109@gmail[.]com`. The same string appears in three other places:

- the aggregate-report destination in the DMARC records of the lure domains `d2saitrade[.]ink` and `surgecareer[.]ink`;
- the dead drop's commit history;
- [Genians' Operation GitPower report](https://www.genians.co.kr/en/blog/threat_intelligence/kimsuky_ai_llm) of August 2026, a corroboration that [Part 17](../17-two-operations-one-ecosystem/) weighs.

This shows that one actor configured the console, the lure domains and the dead drop, though not who controls the mailbox.

Both outside appearances are strings typed into systems that verify neither. A DMARC report address on another domain needs an authorization record at the receiving domain, and the `_report._dmarc` records for both lure domains do not exist at Gmail, so no compliant reporter ever sends a report there. The channel is inert. Git commit addresses are equally self-asserted. An operator burner, a stolen address and a copied placeholder all fit what I observed, and only the mail provider can tell them apart. The inertness makes the string a durable hunting selector, since a habit with no feedback gives the operators no reason to change it.

### The console encodes a small team

The client also encodes a hierarchy. A hard-coded super-administrator sits above ordinary administrators and is the only account permitted to run Claim All, while signup is disabled so that members are added out of band. The developer's own writing differs from the persona layer. The client's internal login subtitle is a Kendrick Lamar lyric credited to "KDot", and the original TypeScript comments are fluent, colloquial American English. The public persona's posts are stilted and non-native.

I read this as a small closed team with roles: a super-administrator who holds the drain, operator administrators, a non-native persona and recruiter layer and a native-English developer. That is a structural reading of the operators' own tooling and a profiling observation, not an attribution. It sits in tension with the vendor assessment of a North Korea-aligned operation, which rests on infrastructure, tradecraft and targeting rather than language. The most defensible statement is that the tension favors a distributed team or an English-fluent contractor over a single-origin operator.

The signup route displays a disabled-signup message. Roles are defined in the interface.

## Limitations

- The backend implementation and its stored records were not recovered, so server-side claim authorization is unknown.
- The API routes are strings in the client, not observed requests.
- No backend event history shows whether a repository suspension triggered an alert or a replacement.
- Account creation and user counts require backend records.
- The Django details come from a third-party scanner's capture of the error page, not from a session of my own.
- The team reading rests on language and role structure in the tooling and cannot identify any person.

## Conclusion

The recovered client shows one console for the whole operation: reply-driven mail, monitoring of delivery repositories and wallet claims aimed at Bittensor validators and miners. Its hosting history and a shared database handle place it inside the same estate and persona set as the lures and the dead drop. Four months after the July recovery, the same code base was still running on its fourth host, as root and in debug mode.

The claim design keeps recipient addresses on the server, so neither the frontend nor victim-side samples reveal where stolen funds go, and the cash-out remains untraced. For defenders, the shared address `eros1030109@gmail[.]com` is a pivot that connects the console, the lure-domain DMARC records and the dead drop's commit history. The [historical indicator reference](../../indicators/) records the exact route forms for hunting.
