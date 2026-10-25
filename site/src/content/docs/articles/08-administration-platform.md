---
title: "Inside rms-platform: Delivery Monitoring and Wallet Administration"
description: "What seventy recovered frontend modules reveal about repository monitoring, wallet workflows and authorization limits."
lastUpdated: 2026-10-25
sidebar:
  order: 8
---


A development deployment exposed seventy frontend modules for an application called rms-platform. The recovered client combined mail views, repository availability checks and wallet-management controls. It provided a view of software intended to support the operation beyond the endpoint payloads, while leaving the actual backend and its records unseen. Following the imports and interface actions shows what the application represents to a user and where that evidence ends.

> **Key Takeaways**
>
> - The recovery followed frontend imports and exposed source maps without authenticated backend access.
> - The client includes repository-status monitoring and wallet import, preview and claim actions.
> - Frontend role checks do not establish server-side authorization or operator identity.
> - A claim button does not prove a completed transaction.

## Seventy modules from a development deployment

The administration recovery followed imports exposed by a Vite development server. It preserved seventy frontend modules, whose embedded source maps included the original TypeScript comments. The recovered application calls itself `rms-platform`; its client contains mail metrics, inbox and outbox views, templates, auto-reply controls, a task board, database tables and wallet-management components.

The acquisition followed only modules loaded by the application. It involved no login or call to the authenticated data API. The result is software for displaying and managing data, not a dump of backend tables.

![What the recovered client makes visible](../assets/06-administration.png)

*Figure 1. What the recovered client makes visible. The backend, authenticated records and completed wallet transfers were not recovered.*


One view tracks repositories by `clone_url`, displays availability labels and offers refresh controls through `/api/github-jobs-check/`. The feature fits the delivery history: repositories can disappear, move or be replaced, and a status view could help monitor locations used to distribute lures or payloads.

The frontend shows the monitoring feature, not its effectiveness. It does not establish that a suspension generated an alert or prompted a later rotation; those claims would require backend records. The finding is that repository availability is explicitly represented in the administration software.

### Wallet management beside mail operations

The wallet interface contains import, refresh, preview, claim and bulk-claim actions, and the client references routes including:

```text
/api/admin/wallets/refresh/
/api/admin/wallets/preview/
/api/admin/wallets/claim/
/api/admin/wallets/claim-all/
```

Mnemonic and ColdKey fields, Bittensor-related interface language, and references to EVM and Aptos connect the intended wallet workflow to material targeted by the collectors. The same application also provides messaging and repository-management views. The substantive link is that the payloads select wallet material and the client contains controls designed to act on that material.

A rendered Claim All button is not a transaction receipt. No backend implementation or confirmed transfer was recovered with the frontend. The sender and harvester tooling should remain distinct: their functions fit the wider operation, but the source does not prove that one backend joined every component into a working pipeline.

### The SuperAdmin check

The client helper grants super-administrator treatment when either a user flag is set or an email comparison matches. It controls frontend navigation and protected routes; I have omitted the mailbox value. My early interpretation was too strong: a hardcoded client-side email does not establish which accounts could execute a server-side claim, especially since the helper has another condition and the backend authorization logic was not recovered.

I also revised an early interpretation of the signup route. It initially suggested a broader operator-account workflow, but further source inspection found a disabled-signup message. The interface supports roles; it does not reveal how many people used them.

## Connecting the client to the collection analysis

The strongest relationship is concrete: the collectors select wallet-related material, while the client includes corresponding mnemonic and ColdKey fields and actions intended to use imported wallet data. Repository availability is also represented directly in the application rather than inferred from infrastructure changes alone.

The harvesting tools discussed in Part 7 were recovered separately. Their functions fit the wider operation, but the frontend does not demonstrate a complete integration between those SQLite pools, the mail views and the wallet workflow. Actual sends, populated backend tables, completed claim requests and confirmed transactions would answer different questions and require their own evidence.

The seventy modules made the client inspectable. They did not turn the investigation into an authenticated session or a database export. Source maps preserved comments and helped explain interface intent, but comments and route names are still statements in client code. The analysis rests on the recovered modules and their relationships, with backend implementation and outcomes left unresolved.

That boundary is useful for later investigation: it identifies which features are visible in source and which conclusions need service-side records. It also prevents a compelling interface from being mistaken for a record of successful theft.
