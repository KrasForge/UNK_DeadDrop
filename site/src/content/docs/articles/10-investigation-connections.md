---
title: "From Three Phishing Emails to a Connected Investigation"
description: "The pivots linking recruitment messages, delivery artifacts, payload configuration and supporting software."
lastUpdated: 2026-10-25
sidebar:
  order: 10
---


Three recruitment messages started this investigation: a Nodit-themed lure in June 2026, followed by D2S AI Trade and Category Labs lures in July. The collected evidence later spanned clipboard lures, an editor extension, collection components, configuration history, targeting databases and administration source.

That breadth can make the case look more unified than the evidence warrants. Each connection had to be established separately, and some relationships remain hypotheses. This article reconstructs the links and marks where the trail stops.

The first nine articles examined individual components. Here I connect them by asking what each artifact established, why it prompted the next question, and where the evidence stopped. This is a reconstruction from retained records, not a claim that every discovery happened in one uninterrupted sequence.

> **Key Takeaways**
>
> - The received messages establish delivery of particular lures; they do not establish infection or the scale of the operation.
> - Links between components have different evidentiary strength: explicit configuration, exact file identity, source behaviour and infrastructure association are not interchangeable.
> - The targeting tools and administration frontend were recovered separately; their compatible functions do not prove one integrated backend.
> - The ECHOES final payload remains missing, so other branches cannot supply its capabilities by association.

## Start with what arrived

The retained message index records the Nodit message on 22 June, the D2S AI Trade message on 21 July and the Category Labs message on 22 July 2026. Those dates describe the received-message record. Later repository commits or historical infrastructure observations can predate the first message without becoming earlier observations made by the analyst.

The headers also contained a practical trap: an inbound forwarding service inserted reverse-alias information. Treating that visible address as operator infrastructure would have attached the analyst's own forwarding path to the campaign. The investigation therefore separated message presentation, original-sender fields and transport evidence. Public articles omit the personal mailbox values; the lesson depends on the distinction between fields, not on exposing those addresses.

These three messages are evidence that their recipients received these lures. They are not a statistical sample of all targeting, and they do not show what happened after delivery. That narrow starting claim matters when the investigation later encounters a database containing over a hundred thousand address strings.

### Follow the command builder, not just the page

On the browser branch, the decisive pivot was the copy handler. The page displayed a verification step, but the handler supplied a different value to the clipboard. Following the argument to that write led to the command builder and its installation logic. The first-stage retrieval location was assembled from the page's origin, which explains why a search for one fixed payload hostname would have been incomplete.

That relationship is supported by control flow: the handler calls the builder, and the builder constructs the command. It is stronger than two domains appearing in the same report. It also stops short of execution. The recovered frontend does not show that a candidate pasted the command, that the download succeeded or that the installer completed. Part 1 follows this distinction through the verification output and client telemetry.

The payload analysis then shifts the question from what a page asks someone to do to what the retained scripts contain. Each recovered stage supplies a new artifact with its own identity and scope. Matching a file hash can establish byte identity; matching a theme or filename cannot substitute for it.

### Keep the repository branch separate

The editor route reaches an extension through project task configuration. The VSIX contains platform-specific components and obtains deployment settings from workspace configuration. Consequently, preserving only the package would miss information needed to reconstruct that installation's configured destination. The task, settings and extension are related pieces of evidence rather than interchangeable copies of one finding.

The Windows source became inspectable through the recorded authenticated decryption. That exposed a Node/Python path distinct from the native Go agents. Similar elevation-builder logic in the ClickFix and extension material supports a connection between implementations, but it does not make the two delivery experiences identical. Their user actions, initial processes and execution conditions differ.

This is also where published research constrains the contribution claim. The extension and Windows architecture corroborate the public baseline described in the earlier articles. Recovering readable code supports a detailed explanation; it does not make an already published architecture a new discovery.

![Connections need named relationships](../assets/10-evidence-map.png)

*Figure 1. Connections need named relationships. Different edge labels support different claims; end-to-end execution was not established.*

[Open full-size vector diagram](/UNK_DeadDrop/diagrams/10-evidence-map.svg). Sources: [E01](../../evidence/E01.pdf), [E02](../../evidence/E02.pdf), [E03](../../evidence/E03.pdf), [E07](../../evidence/E07.pdf), [E08](../../evidence/E08.pdf), [E06](../../evidence/E06.pdf), [E11](../../evidence/E11.pdf).

## A relationship map with named edges

The following map summarizes analytical relationships rather than a proven end-to-end execution trace. Detailed supporting records are linked below.

| Starting artifact | Relationship followed | Resulting evidence | Limit |
|---|---|---|---|
| Received message | Links to a recruitment lure | Historical delivery starting point | No infection outcome |
| Lure source | Copy handler invokes command builder | Clipboard substitution and retrieval logic | No terminal execution record |
| Project configuration | Task and settings select installation parameters | Extension deployment path | Trust and permissions still matter |
| Held collector | References configuration resource | GitLab resolver dependency | Refresh and reconnect behaviour unresolved |
| Sender configuration | Names targeting pools | Harvester and aggregate database analysis | No send-volume measurement |
| Recovered frontend | Imports modules and defines interface actions | Repository monitoring and wallet workflows | Backend and transfers unobserved |
| ECHOES history | Preserves revised archives | Staging lineage and destination changes | Final payload unavailable |

The labels on those relationships are essential. “References” is a source observation. “Resolved to” is a dated infrastructure observation. “Shares a theme” is a weaker similarity. Replacing all three with an unlabeled line between nodes hides exactly the distinctions a reader needs to evaluate the case.

### The resolver changes what must be preserved

Once a held component references a mutable configuration resource, the payload hash no longer describes the entire destination-selection state. The relevant evidence includes the configuration value and the revision or observation time associated with it. The July history records a destination change; it does not show every client's response to that edit.

The origin analysis adds another type of relationship. Certificates, passive DNS and matching panel content support historical service associations. They do not establish exclusive ownership of an address or identify every tenant. The withdrawn earlier-phase hypothesis illustrates why shared hosting alone cannot extend the campaign timeline. A new node in an infrastructure graph requires an explicit reason for inclusion, not just proximity to an existing node.

Part 6 examines these observations individually. In the broader investigation, their purpose is to connect particular service roles at particular times while leaving ownership and current availability separate.

### Targeting scale and administration visibility answer different questions

The databases provided the largest number in the case: 142,365 distinct stored address strings. The harvester and sender configurations explain how that targeting material was assembled and prepared for use. They do not establish how many messages were sent, which recipients opened them or which systems ran a payload.

The administration frontend supplied a different view. Its repository monitor and wallet interfaces show functions intended to maintain delivery locations and act on wallet material. Corresponding concepts in the collection code make that relationship technically meaningful. However, no recovered backend demonstrates that every harvested address, message and wallet record passed through one functioning pipeline.

Keeping the components separate does not diminish their value. It lets a later analyst ask for the missing evidence precisely: send logs for delivery volume, service records for actual workflow use, and transaction evidence for financial outcomes.

### End the trail where the artifacts end

ECHOES preserves four archive revisions and a changing retrieval configuration. Its final PowerShell resources were unavailable through the unauthenticated routes examined. The retained staging can support a lineage analysis, but a shared account relationship cannot fill in the missing payload's implementation.

The same discipline applies to the rest of the case. Source can establish a collection attempt, authentication can validate recovered plaintext, and a hash can establish identity. None alone establishes victim loss or a real-world perpetrator. The research becomes more useful when a reader can tell which kind of evidence supports each sentence.

For a follow-up investigation, I would preserve a compact record for every relationship: the two artifacts, their identities, the observation date, the source of the relationship and the strongest alternative explanation. That would make it possible to revise one conclusion without silently rewriting the rest of the case.

## What the public record adds, and what remains distinctive

The public reporting now includes [a direct account of the UNK_DeadDrop campaign](https://brhopkins.uk/posts/foxtopia/), as well as [later reporting on developer lures and overlapping implementation details](https://dev.to/edison_flores_6d2cd381b13/a-fake-recruiter-sent-me-a-job-offer-that-ended-in-my-terminal-the-trojan-is-still-live-2okf). These reports matter to the novelty assessment: developer phishing, malicious VS Code extensions, credential and wallet theft, and the broad Overlord lineage are not new claims of this investigation. The July article that surfaced in the refresh predates the original evidence cutoff; its later update does not make its initial reporting a post-cutoff discovery.

The strongest contribution here is narrower and case-specific: the retained artifacts let readers inspect how the clipboard builder works, how the VSIX configuration selects deployment settings, how targeting data and administration functions are represented, and how the resolver and ECHOES archives changed over time. The October follow-up describes similar implementation markers, but it traces back to the same reporter's account and does not independently verify a sample. It is a useful lead, not independent confirmation. On this evidence, the series supports a detailed technical contribution; it does not establish that these behaviors were first observed here.

That boundary is useful to readers. Novelty can attach to the evidence recovered, the level of implementation detail, or a particular relationship between artifacts. It should not be stretched to cover a campaign category or technique already described elsewhere.
