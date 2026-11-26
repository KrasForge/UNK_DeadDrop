---
title: "Two Operations, One Ecosystem: Separating UNK_DeadDrop from PolinRider"
description: "Why UNK_DeadDrop and PolinRider are two operations, why shared techniques, hosting and victims do not link them, and which publisher makes each attribution."
lastUpdated: 2026-11-26
sidebar:
  order: 17
head:
  - tag: meta
    attrs:
      property: og:image
      content: "https://example.github.io/UNK_DeadDrop/og/17.png"
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
      content: "Part 17: Two Operations, One Ecosystem: Separating UNK_DeadDrop from PolinRider"
  - tag: meta
    attrs:
      name: twitter:image
      content: "https://example.github.io/UNK_DeadDrop/og/17.png"
---



I found zero observational paths between PolinRider's records and UNK_DeadDrop's in my evidence graph. The only two paths that connect them run through a generic obfuscator.io string-array rule and a bare attribution tag, so I describe UNK_DeadDrop and PolinRider as two separate operations in the same ecosystem.

## Key takeaways

- Two paths connect the PolinRider block to UNK_DeadDrop, and neither is an observation; removing them leaves zero observational paths.
- The two operations differ at every layer an operator has to build: first contact, delivery, C2 resolution, implant and hosting.
- Shared victims, the folder-open launcher, shared address space and a shared swap service are reasons to compare the clusters, not links between them.
- OpenSourceMalware attributes PolinRider to the DPRK and Stormshield links Trigram to Kimsuky; I attribute neither operation to a state or a named group.
- MITRE's G1052 page lacks five techniques I observed directly, among them T1102.001 Dead Drop Resolver, so suspensions of this operator's infrastructure have to be simultaneous rather than staged.

## Method: link only on shared operational values

For weeks the two operations sat in the same case folder, under the same case label. They also approached some of the same people through recruiters. The question of whether they are one operation matters because almost everything visible about these crews is shared by the wider Contagious Interview ecosystem:

- a recruiter persona;
- a take-home repository;
- an editor task that runs when a folder is opened;
- a payload that reads its command-and-control (C2) address from a value the operator has published somewhere public.

Clustering on that kind of resemblance merges operations that share nothing operational, so I adopted a narrow rule early on. Two clusters are linked only when they hold an operational value in common: a wallet, a contract, a carrier transaction, a key, a certificate, a credential, a build identifier or a host used in the same role at the same time. A shared technique, target population or victim is a reason to compare two clusters and never the result of the comparison. The `unk-deaddrop` label that my records carry marks the case, not an attribution.

## Comparison: every layer an operator builds is different

Set side by side, the two operations differ at each layer an operator must build. The earlier parts of this series describe the UNK_DeadDrop side in detail, from the [ClickFix pages](../01-clickfix-clipboard-manipulation/) and the [VSIX route](../02-vsix-editor-execution/) to the [GitLab dead drop](../06-gitlab-dead-drop-infrastructure/) that its implant reads.

| Layer | UNK_DeadDrop | PolinRider |
|---|---|---|
| First contact | Recruiter mail to harvested developer addresses, careers sites, take-home repositories | Recruiter personas such as Hiring777, take-home repositories, worm spread through infected developers' own pushes |
| Delivery | ClickFix clipboard substitution, VSIX extension, folder-open task to an installer | Obfuscated `init` or fake-font loader started by an npm script or a hidden folder-open task |
| C2 resolution | GitLab raw configuration file | TRON, BSC and Aptos pointers to a BSC payload carrier; Ethereum zero-value transfers encoding an IPv4 address in the recipient |
| Implant | Private fork of the Overlord Go client, Node and Python Windows pipeline | Socket.io JavaScript RAT stages, Python stealer modules |
| Hosting | Advin Services (AS22295, AS206216), July to November 2026, certificate-heavy `.ink` and `.xyz` lure fleet | Evoxt (AS149440) and AS399486, bare IPs on raw ports, almost no certificates |

I keep the clock out of the table because it is the weakest comparison I have. UNK_DeadDrop's git hosts run at UTC while its build hosts are set to United States offsets. The handful of genuine commits on the PolinRider-linked npm cluster declare +03:00. A commit's timezone is a setting, however, and nine commits in three sessions on the resolver side stand against forty-one lure-side sessions built on certificate issuance, registrations and on-chain events. The honest statement is only that the working windows differ on the evidence available.

When I compared the Hiring777 material with the UNK_DeadDrop estate in November, I found no shared address, subnet, autonomous system, certificate or panel fingerprint between them.

![UNK_DeadDrop and PolinRider as two operations within the Contagious Interview ecosystem](../assets/17-separation-map.png)

*Figure 1. Solid lines are my own evidence. Dashed lines mark the two excluded artifact paths and Stormshield's Kimsuky link, which I have not established. The ecosystem frame groups shared context and is not a link.*

## Measurement: two artifact paths, zero observations

I built the path count on a graph from my evidence snapshot of 14 November 2026. In that graph, records are joined only by recorded relationships between observables. Campaign and actor labels are not vertices, so an attribution edge cannot carry a path on its own.

Counted as vertex-disjoint paths, the NullReceiver, PolinRider and Hiring777 block reaches the rest of the case through exactly two artifacts, and those two form its minimum separator:

- a generic obfuscator.io string-array rule that I had tagged as indicating the operator;
- a PolinRider-side C2 address that carried nothing more than a bare attribution tag, a conclusion written down as if it were a relationship.

Removing those two leaves zero observational paths between the two blocks. That number, more than any single indicator, is why I treat the operations as separate. For comparison, the same measure gives the TronzitVeca and ECHOES persona block twelve independent paths across 210 source files.

As a second and unrelated method, I ran Leiden community detection over 2,218 observables. Every one of the 177 connected resolver-side records landed in a community containing no UNK_DeadDrop record. Of those, 176 sit in six communities of five or more records and one sits in a community of four.

## Overlaps: shared victims, launchers and address space

### Shared victims

The two operations do share victims. My records hold two developers who answered both operations' recruiters. One of them holds the weaponized Hiring777 take-home, with PolinRider loader artifacts in 19 of the account's 26 public repositories, which I read as propagation from that developer's workstation.

One detail shows how easily a shared victim manufactures a link. A developer's account carrying the loader holds forks whose fork-only commits carry the kit under the upstream maintainers' names. One of those forks is of a repository owned by pridnet, the GitHub persona behind the UNK_DeadDrop take-home lure on `dscufo[.]xyz`. Read naively, an UNK_DeadDrop identity appears to have authored a PolinRider commit. The worm, however, amends commits in every working copy it reaches under whoever wrote them, so the authorship field records the worm's path rather than its operator.

### Shared keys, launchers and gas

Other tempting links fail for similar reasons:

- In September 2026 a second sweeper drained a developer whose key the PolinRider side already held, without touching that operator's funder or hub. That is what happens once a key store has been stolen and then resold or leaked again.
- On GitGuardian's [working hypothesis](https://blog.gitguardian.com/ghostaction-x-polinrider/), the GhostAction credential campaign copied a public PolinRider launcher and shares nothing else with it.
- Two wallet clusters that both took gas from FixedFloat share a preference rather than an operator.

### Shared address space

Address space was the hardest case. PolinRider's signal-wallet C2 `95.135.181[.]25` sits in the same leased /24 as the NullReceiver resolver's eleventh host, `95.135.181[.]84`. Six separate tests point away from a common hand, among them rotation history, setup order, service shape and the range's churn between unrelated customers. I record shared space without shared control at medium-high confidence.

## Parallel clusters: the same technique, different values

### The March and April cluster is PolinRider

Public reporting in March and April 2026 described a parallel cluster using the same fake-recruiting lures and the same `.vscode/tasks.json` technique as UNK_DeadDrop. [OpenSourceMalware's April update](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github) counted it at 1,951 compromised repositories across 1,047 owners.

I ran the comparison in both directions: sixteen of my identifiers against that dossier, and nine of its markers against ninety-five of my sample and report files. I found zero overlap either way within those sets. That parallel cluster is the one public reporting calls PolinRider, so the July indicator test and my November infrastructure comparison reach the same line from opposite ends.

### The folder-open launcher

The folder-open launcher is the artifact most often over-read in this ecosystem:

- UNK_DeadDrop uses it to reach its VSIX installer.
- PolinRider uses it to start its fake-font loader.
- [SafeDep's Miasma write-up](https://safedep.io/blog/miasma-worm-ai-coding-agent-config-injection) lists it among five auto-run triggers.
- Unit 42's [ChainDrop analysis](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) shows that worm writing persistence into the same file.

Its presence therefore identifies a family convention and nothing narrower. A search of all 104 mirrored UNK_DeadDrop operator repositories found neither PolinRider's disguised-font script nor its loader marker.

### The npm stealer cluster

The npm stealer cluster published from nine single-use accounts in October and November 2026 is the hardest parallel case. It carries PolinRider's genuine resolver design, both TRON wallets, both Aptos fallback accounts, the exact TronGrid query string and the worm's forced-push propagation.

Every value it shares with the real loader, however, was already printed in [JFrog's June report](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/) or in OpenSourceMalware's posts of March, April and July. Its code names itself after the analysts' label for the actor rather than anything the operator uses, and it carries local test endpoints. I assess it as probable reuse or emulation of PolinRider at moderate confidence. A non-public constant or a shared build marker would settle the question in either direction.

## Hiring777: a reported campaign, not UNK_DeadDrop

Hiring777 was my entry point to PolinRider. It is a recruiter persona whose copy-trading take-home carried a dropper that I fully deobfuscated as an EtherHiding and NullReceiver loader. I recovered all 538 of its call sites and 372 strings, and read its C2 from the recipient address of an Ethereum transaction.

The evidence on a link to UNK_DeadDrop points both ways:

- For a link: the overlapping victims and the shared fake-recruiter pretext.
- Against a link: a different persona, a different malware vector, different hosting, a different resolver, and no shared C2, certificate or panel.

Same-crew is therefore not established. What the dropper does yield is a placement in published reporting. My resolver wallet shares two C2 hosts, the `helloipbot!!` marker, the staging paths and the RPC list with the wallet named in [OpenSourceMalware's NullReceiver write-up](https://opensourcemalware.com/blog/nullreceiver-dprk-c2-technique). That makes Hiring777 a live node of a known campaign rather than an unknown actor.

The attribution for that campaign belongs to OpenSourceMalware. It attributes PolinRider to the Democratic People's Republic of Korea (DPRK) and describes it as a known Lazarus group contributor connected to the Contagious Interview and TasksJacker campaigns. I adopt that wording from their reporting rather than establish it myself.

Naming a specific cluster such as UNC5342 would go one step further than the evidence. Google Threat Intelligence Group's [EtherHiding report](https://cloud.google.com/blog/topics/threat-intelligence/dprk-adopts-etherhiding) attributes EtherHiding and JADESNOW to UNC5342 and never mentions PolinRider or NullReceiver. A sentence that joins the two quietly borrows GTIG's authority for a claim GTIG did not make.

## Trigram: UNK_DeadDrop, with Stormshield's Kimsuky link

Stormshield's Customer Security Lab published its [Trigram report](https://www.stormshield.com/news/cti-trigram-campaign/) on 11 November 2026. It describes a ClickFix campaign behind a GitLab relay and a Django back office. I agree that Trigram is UNK_DeadDrop and can say so on my own identifiers:

- The relay is the GitLab dead drop I track in its later projects.
- The back office's database user `silviattech1129` and the author address of one relay commit carry the same handle that binds the "Silvio Silva" persona to the 2025 launchpad.

The version Stormshield republished on 17 November softened its wording. A high-confidence attribution to North Korea became shared indicators and strong similarities with North Korea-linked intrusion sets, among them UNK_DeadDrop and Kimsuky. The report still keeps Trigram as a continuation of UNK_DeadDrop.

The Kimsuky link is Stormshield's assessment and not mine. The one outside piece of evidence I hold that bears on it is [Genians' Operation GitPower report](https://www.genians.co.kr/en/blog/threat_intelligence/kimsuky_ai_llm) of 10 August 2026. That report lists identities I already held, among them `eros1030109@gmail[.]com` and `apollo1030109@gmail[.]com`, linked to the operator's configuration. It also gives two C2 addresses that I place on Advin's network, all reached through a Kimsuky cluster built on LNK files, PowerShell, GitHub and AsyncRAT.

That corroborates the identity set and is consistent with Stormshield's link. None of Genians' forty-six file hashes, however, matches any of the roughly 2.76 million files I hold. The two bodies of evidence overlap in people and hosting and not in a single sample. My wording therefore stays as follows:

- Stormshield links Trigram to Kimsuky.
- Genians found UNK_DeadDrop identities inside a cluster it attributes to Kimsuky.
- I have not established a Kimsuky attribution.

## ATT&CK: what MITRE's G1052 page fits and what it misses

I use MITRE's [Contagious Interview group, G1052](https://attack.mitre.org/groups/G1052/), as my primary ATT&CK mapping because it fits UNK_DeadDrop in target and pretext. MITRE describes the group as North Korea-aligned, which again is MITRE's description and not a conclusion I draw.

The fit is one of behavior rather than tooling. The C2 and encryption MITRE documents for the group differ from this operator's. The fifteen malware families on my July list of G1052- and G1049-associated software, BeaverTail and InvisibleFerret among them, returned zero hits across the UNK_DeadDrop sample set.

Against the page as read on 24 July, which listed 105 techniques, my mapping marks five directly observed techniques that the page does not carry. They were still absent after its 31 July revision:

- [T1102.001 Dead Drop Resolver](https://attack.mitre.org/techniques/T1102/001/)
- T1566.002 Spearphishing Link
- T1552.001 Credentials In Files
- T1552.004 Private Keys
- T1113 Screen Capture

The dead-drop resolver is the most consequential gap. Over four months it was the most durable part of the operation, retained while the lure layer was rebuilt twice. Seizing or blocking a C2 domain interrupts nothing when the operators can edit one file, so suspensions have to be simultaneous rather than staged.

## Exclusions: twelve candidates that did not hold

I ruled out twelve candidate campaigns. Eleven were reported by third parties. One, a Brazilian affiliate-marketing spam family, I found through co-residence on the lure fleet's budget host.

- Four ClickFix frameworks reported by [Sekoia](https://www.sekoia.com/blog/unveiling-errtraffic-inside-a-growing-clickfix-malware-distribution-framework) and Huntress share no marker, identifier, domain or IP with UNK_DeadDrop's lure builder. Their one shared idea, assembling the command per visitor at copy time, is implemented differently.
- SleepyDuck, reported by [Socket](https://socket.dev/blog/bee-js-compromise) and Pluto Security, reads a blockchain as a resolver and aims at developers' wallets just as NullReceiver does. It shares no wallet, host, contract or payload with it.
- ChainDrop, Miasma, GhostAction and the rest fell the same way: each matched an idea, and none matched a value.

Exclusion also protects people. All of the following stay out of every indicator list I publish:

- a value decoded from the NullReceiver resolver's rehearsal day, which belongs to a content-delivery network's proxy service;
- one address in Stormshield's indicator set that is a DNS-filtering sinkhole;
- another address in that set that is a reassigned host now running game servers;
- an address that appears beside PolinRider victims in public reporting and belongs to GhostAction.

The persona farm re-pushes genuine projects with their author history. As a result, six real developers' addresses appear inside persona-owned repositories as a matter of course. On my direction-and-date test they are copy victims, not personas.

## Limitations

- UNK_DeadDrop is consistent with a cluster that [Proofpoint](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) assesses as likely North Korea-aligned. The timing I measured points the same way: provisioning sessions cluster early in the UTC day, and hand-authored files form an ordinary daytime shift when read at UTC+8 or UTC+9. Build-host offsets are settings the operator chooses, so this corroborates their assessment without amounting to geolocation.
- I do not myself attribute either operation to a state or a named group.
- I do not know whether the people behind the two operations answer to one organization. Infrastructure cannot answer that question; it would need account records that only providers and exchanges hold.
- A longer write-up of the separation analysis is in preparation.

## Conclusion

What I can say is narrower and, I think, more useful. The two operations share an ecosystem, a pretext and a handful of victims, and nothing else that I can observe. The PolinRider material that follows is therefore a separate investigation with its own resolvers, its own spread and its own money.

For defenders, the practical consequence is to cluster on shared operational values and to treat techniques, victims and address space as prompts for comparison. Indicator lists should leave out sinkholes, proxy services, reassigned hosts and copy victims, and actions against a dead-drop resolver should be simultaneous rather than staged.

That part begins with [one developer whose repositories carried a loader](../18-polinrider-following-a-developer/), and with the take-home that led me from Hiring777 to an Ethereum address book.
