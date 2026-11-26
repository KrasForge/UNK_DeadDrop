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



When I counted the independent paths that connect PolinRider's records to UNK_DeadDrop's in my evidence graph, I found exactly two, and neither of them was an observation: one was a generic obfuscator.io string-array rule that I had tagged as indicating the operator, and the other was a PolinRider-side C2 address that carried nothing more than a bare attribution tag, a conclusion written down as if it were a relationship. Removing those two left zero observational paths between the two blocks, and that number, more than any single indicator, is why I now describe UNK_DeadDrop and PolinRider as two separate operations that happen to live in the same ecosystem, even though for weeks they sat in the same case folder, under the same case label, and were approached by recruiters writing to some of the same people.

The question matters because almost everything visible about these crews is shared by the wider Contagious Interview ecosystem: a recruiter persona, a take-home repository, an editor task that runs when a folder is opened, and a payload that reads its command-and-control (C2) address from a value the operator has published somewhere public. Clustering on that kind of resemblance merges operations that share nothing operational, so I adopted a narrow rule early on. Two clusters are linked only when they hold an operational value in common, meaning a wallet, a contract, a carrier transaction, a key, a certificate, a credential, a build identifier or a host used in the same role at the same time, while a shared technique, target population or victim is a reason to compare two clusters and never the result of the comparison. The `unk-deaddrop` label that my records carry marks the case, not an attribution.

## Every layer an operator has to build is different

Set side by side, the two operations differ at each layer an operator must build, and the earlier parts of this series describe the UNK_DeadDrop side in detail, from the [ClickFix pages](../01-clickfix-clipboard-manipulation/) and the [VSIX route](../02-vsix-editor-execution/) to the [GitLab dead drop](../06-gitlab-dead-drop-infrastructure/) that its implant reads.

| Layer | UNK_DeadDrop | PolinRider |
|---|---|---|
| First contact | Recruiter mail to harvested developer addresses, careers sites, take-home repositories | Recruiter personas such as Hiring777, take-home repositories, worm spread through infected developers' own pushes |
| Delivery | ClickFix clipboard substitution, VSIX extension, folder-open task to an installer | Obfuscated `init` or fake-font loader started by an npm script or a hidden folder-open task |
| C2 resolution | GitLab raw configuration file | TRON, BSC and Aptos pointers to a BSC payload carrier; Ethereum zero-value transfers encoding an IPv4 address in the recipient |
| Implant | Private fork of the Overlord Go client, Node and Python Windows pipeline | Socket.io JavaScript RAT stages, Python stealer modules |
| Hosting | Advin Services (AS22295, AS206216), July to November 2026, certificate-heavy `.ink` and `.xyz` lure fleet | Evoxt (AS149440) and AS399486, bare IPs on raw ports, almost no certificates |

The clock row I keep out of the table because it is the weakest comparison I have. UNK_DeadDrop's git hosts run at UTC while its build hosts are set to United States offsets, and the handful of genuine commits on the PolinRider-linked npm cluster declare +03:00, but a commit's timezone is a setting, and nine commits in three sessions on the resolver side stand against forty-one lure-side sessions built on certificate issuance, registrations and on-chain events, so the honest statement is only that the working windows differ on the evidence available. When I compared the Hiring777 material with the UNK_DeadDrop estate in November, I also found no shared address, subnet, autonomous system, certificate or panel fingerprint between them.

![UNK_DeadDrop and PolinRider as two operations within the Contagious Interview ecosystem](../assets/17-separation-map.png)

*Figure 1. Solid lines are my own evidence. Dashed lines mark the two excluded artifact paths and Stormshield's Kimsuky link, which I have not established. The ecosystem frame groups shared context and is not a link.*

## Measuring the gap instead of describing it

The path count works on a graph built from my evidence snapshot of 14 November 2026, in which records are joined only by recorded relationships between observables and in which campaign and actor labels are not vertices, so an attribution edge cannot carry a path on its own. Counted as vertex-disjoint paths, the NullReceiver, PolinRider and Hiring777 block reaches the rest of the case through the two artifacts described above, and those two form its minimum separator, while the same measure gives the TronzitVeca and ECHOES persona block twelve independent paths across 210 source files. As a second and unrelated method I ran Leiden community detection over 2,218 observables, and every one of the 177 connected resolver-side records landed in a community containing no UNK_DeadDrop record, 176 of them in six communities of five or more records and one in a community of four.

## Shared victims, shared launchers and shared address space

The two operations do share victims. My records hold two developers who answered both operations' recruiters, and one of them holds the weaponized Hiring777 take-home, with PolinRider loader artifacts in 19 of the account's 26 public repositories, which I read as propagation from that developer's workstation. One detail shows how easily a shared victim manufactures a link: a developer's account carrying the loader holds forks whose fork-only commits carry the kit under the upstream maintainers' names, and one of those forks is of a repository owned by pridnet, the GitHub persona behind the UNK_DeadDrop take-home lure on `dscufo[.]xyz`. Read naively, an UNK_DeadDrop identity appears to have authored a PolinRider commit, but the worm amends commits in every working copy it reaches under whoever wrote them, so the authorship field records the worm's path rather than its operator.

Other tempting links fail for similar reasons. In September 2026 a second sweeper drained a developer whose key the PolinRider side already held, without touching that operator's funder or hub, which is what happens once a key store has been stolen and then resold or leaked again. On GitGuardian's [working hypothesis](https://blog.gitguardian.com/ghostaction-x-polinrider/), the GhostAction credential campaign copied a public PolinRider launcher and shares nothing else with it, and two wallet clusters that both took gas from FixedFloat share a preference rather than an operator. The hardest case was address space: PolinRider's signal-wallet C2 `95.135.181[.]25` sits in the same leased /24 as the NullReceiver resolver's eleventh host, `95.135.181[.]84`, yet six separate tests, including rotation history, setup order, service shape and the range's churn between unrelated customers, point away from a common hand, so I record shared space without shared control at medium-high confidence.

## A parallel cluster that turned out to be PolinRider

Public reporting in March and April 2026 described a parallel cluster using the same fake-recruiting lures and the same `.vscode/tasks.json` technique as UNK_DeadDrop, which [OpenSourceMalware's April update](https://opensourcemalware.com/blog/polinrider-rides-again-north-korean-attack-expands-across-github) counted at 1,951 compromised repositories across 1,047 owners. I ran the comparison in both directions, sixteen of my identifiers against that dossier and nine of its markers against ninety-five of my sample and report files, and found zero overlap either way within those sets. That parallel cluster is the one public reporting calls PolinRider, so the July indicator test and my November infrastructure comparison reach the same line from opposite ends.

The folder-open launcher is the artifact most often over-read in this ecosystem. UNK_DeadDrop uses it to reach its VSIX installer, PolinRider uses it to start its fake-font loader, [SafeDep's Miasma write-up](https://safedep.io/blog/miasma-worm-ai-coding-agent-config-injection) lists it among five auto-run triggers, and Unit 42's [ChainDrop analysis](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) shows that worm writing persistence into the same file, so its presence identifies a family convention and nothing narrower. A search of all 104 mirrored UNK_DeadDrop operator repositories found neither PolinRider's disguised-font script nor its loader marker.

The npm stealer cluster published from nine single-use accounts in October and November 2026 is the hardest parallel case, because it carries PolinRider's genuine resolver design, both TRON wallets, both Aptos fallback accounts, the exact TronGrid query string and the worm's forced-push propagation. Every value it shares with the real loader, however, was already printed in [JFrog's June report](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/) or in OpenSourceMalware's posts of March, April and July, its code names itself after the analysts' label for the actor rather than anything the operator uses, and it carries local test endpoints. I assess it as probable reuse or emulation of PolinRider at moderate confidence, and a non-public constant or a shared build marker would settle the question in either direction.

## Hiring777 belongs to a reported campaign, not to UNK_DeadDrop

Hiring777 was my entry point to PolinRider: a recruiter persona whose copy-trading take-home carried a dropper that I fully deobfuscated as an EtherHiding and NullReceiver loader, recovering all 538 of its call sites and 372 strings and reading its C2 from the recipient address of an Ethereum transaction. The overlapping victims and the shared fake-recruiter pretext argue for a link to UNK_DeadDrop, while a different persona, a different malware vector, different hosting, a different resolver and no shared C2, certificate or panel argue against it, so same-crew is not established. What the dropper does yield is a placement in published reporting: my resolver wallet shares two C2 hosts, the `helloipbot!!` marker, the staging paths and the RPC list with the wallet named in [OpenSourceMalware's NullReceiver write-up](https://opensourcemalware.com/blog/nullreceiver-dprk-c2-technique), which makes Hiring777 a live node of a known campaign rather than an unknown actor.

The attribution for that campaign belongs to OpenSourceMalware, which attributes PolinRider to the Democratic People's Republic of Korea (DPRK) and describes it as a known Lazarus group contributor connected to the Contagious Interview and TasksJacker campaigns, and I adopt that wording from their reporting rather than establish it myself. Naming a specific cluster such as UNC5342 would go one step further than the evidence, because Google Threat Intelligence Group's [EtherHiding report](https://cloud.google.com/blog/topics/threat-intelligence/dprk-adopts-etherhiding) attributes EtherHiding and JADESNOW to UNC5342 and never mentions PolinRider or NullReceiver, so a sentence that joins the two quietly borrows GTIG's authority for a claim GTIG did not make.

## Trigram is UNK_DeadDrop, and the Kimsuky link is Stormshield's

Stormshield's Customer Security Lab published its [Trigram report](https://www.stormshield.com/news/cti-trigram-campaign/) on 11 November 2026, a ClickFix campaign behind a GitLab relay and a Django back office, and I agree that Trigram is UNK_DeadDrop and can say so on my own identifiers: the relay is the GitLab dead drop I track in its later projects, the back office's database user `silviattech1129` and the author address of one relay commit carry the same handle that binds the "Silvio Silva" persona to the 2025 launchpad,. The version Stormshield republished on 17 November softened its wording from a high-confidence attribution to North Korea into shared indicators and strong similarities with North Korea-linked intrusion sets, among them UNK_DeadDrop and Kimsuky, while keeping Trigram as a continuation of UNK_DeadDrop.

The Kimsuky link is Stormshield's assessment and not mine. The one outside piece of evidence I hold that bears on it is [Genians' Operation GitPower report](https://www.genians.co.kr/en/blog/threat_intelligence/kimsuky_ai_llm) of 10 August 2026, which lists identities I already held, among them `eros1030109@gmail[.]com` and `apollo1030109@gmail[.]com`, linked to the operator's configuration, and gives two C2 addresses that I place on Advin's network, all reached through a Kimsuky cluster built on LNK files, PowerShell, GitHub and AsyncRAT. That corroborates the identity set and is consistent with Stormshield's link, but none of Genians' forty-six file hashes matches any of the roughly 2.76 million files I hold, so the two bodies of evidence overlap in people and hosting and not in a single sample, and my wording stays that Stormshield links Trigram to Kimsuky, that Genians found UNK_DeadDrop identities inside a cluster it attributes to Kimsuky, and that I have not established a Kimsuky attribution.

## What MITRE's G1052 page fits and what it misses

I use MITRE's [Contagious Interview group, G1052](https://attack.mitre.org/groups/G1052/), as my primary ATT&CK mapping because it fits UNK_DeadDrop in target and pretext, and MITRE describes the group as North Korea-aligned, which again is MITRE's description and not a conclusion I draw. The fit is one of behavior rather than tooling: the C2 and encryption MITRE documents for the group differ from this operator's, and the fifteen malware families on my July list of G1052- and G1049-associated software, BeaverTail and InvisibleFerret among them, returned zero hits across the UNK_DeadDrop sample set. Against the page as read on 24 July, which listed 105 techniques, my mapping marks five directly observed techniques that the page does not carry, and they were still absent after its 31 July revision: [T1102.001 Dead Drop Resolver](https://attack.mitre.org/techniques/T1102/001/), T1566.002 Spearphishing Link, T1552.001 Credentials In Files, T1552.004 Private Keys and T1113 Screen Capture.

The dead-drop resolver is the most consequential gap, because over four months it was the most durable part of the operation, retained while the lure layer was rebuilt twice, and because seizing or blocking a C2 domain interrupts nothing when the operators can edit one file, so suspensions have to be simultaneous rather than staged.

## Twelve candidates that did not hold

I ruled out twelve candidate campaigns, eleven of them reported by third parties and one, a Brazilian affiliate-marketing spam family, found through co-residence on the lure fleet's budget host. Four ClickFix frameworks reported by [Sekoia](https://www.sekoia.com/blog/unveiling-errtraffic-inside-a-growing-clickfix-malware-distribution-framework) and Huntress share no marker, identifier, domain or IP with UNK_DeadDrop's lure builder, and their one shared idea, assembling the command per visitor at copy time, is implemented differently. SleepyDuck, reported by [Socket](https://socket.dev/blog/bee-js-compromise) and Pluto Security, reads a blockchain as a resolver and aims at developers' wallets just as NullReceiver does, yet shares no wallet, host, contract or payload with it, and ChainDrop, Miasma, GhostAction and the rest fell the same way: each matched an idea, and none matched a value.

Exclusion also protects people. A value decoded from the NullReceiver resolver's rehearsal day belongs to a content-delivery network's proxy service, one address in Stormshield's indicator set is a DNS-filtering sinkhole and another is a reassigned host now running game servers, and an address that appears beside PolinRider victims in public reporting belongs to GhostAction, so all of them stay out of every indicator list I publish. Because the persona farm re-pushes genuine projects with their author history, six real developers' addresses appear inside persona-owned repositories as a matter of course, and on my direction-and-date test they are copy victims, not personas.

## Where my evidence stops

UNK_DeadDrop is consistent with a cluster that [Proofpoint](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) assesses as likely North Korea-aligned, and the timing I measured points the same way, with provisioning sessions clustering early in the UTC day and hand-authored files forming an ordinary daytime shift when read at UTC+8 or UTC+9, but build-host offsets are settings the operator chooses, so this corroborates their assessment without amounting to geolocation. I do not myself attribute either operation to a state or a named group, and I do not know whether the people behind them answer to one organization, a question that infrastructure cannot answer and that would need account records only providers and exchanges hold. A longer write-up of the separation analysis is in preparation.

What I can say is narrower and, I think, more useful: the two operations share an ecosystem, a pretext and a handful of victims, and nothing else that I can observe, so the PolinRider material that follows is a separate investigation with its own resolvers, its own spread and its own money. That part begins with [one developer whose repositories carried a loader](../18-polinrider-following-a-developer/), and with the take-home that led me from Hiring777 to an Ethereum address book.
