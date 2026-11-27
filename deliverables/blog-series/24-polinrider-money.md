---
title: "Following PolinRider's Money: Gas, Bridges, Laundering and Cash-Out"
description: "What PolinRider's on-chain C2 costs, how stolen money pays for it, where the proceeds cross chains and cash out, and why UNK_DeadDrop's cash-out stays out of sight."
date: "2026-11-27"
published: "2026-11-26"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/24-polinrider-money/"
kicker: "PolinRider · Part 7"
tags:
  - "PolinRider"
  - "blockchain"
  - "laundering"
  - "cryptocurrency"
  - "threat intelligence"
og_image_alt: "Flow of PolinRider's money from theft proceeds through provisioning wallets, carriers, signal and resolver wallets to payout accounts and exchange deposits"
---


I traced the money behind PolinRider's on-chain command-and-control (C2) channel and found that stolen funds pay for it, gas and working capital alike. The cash-out I can attribute to accounts PolinRider uses comes to a few hundred thousand dollars, while UNK_DeadDrop's cash-out stays out of sight.

## Key takeaways

- The on-chain C2 is cheap to run: resolver wallet C's daily cost is of the order of 0.0005 ETH, so who pays the bill is more informative than its size.
- Carriers and resolvers are funded from drained wallets; the operator of the resolver side's drain collection address very probably holds keys to around 1,340 wallets.
- A ConcentricFi vault backdoor on Arbitrum is still armed: on 16 November 2026, 91 wallets still held open allowances, 41 with balances that could be pulled, and anyone who approved those vaults should revoke the allowance now.
- The attributable cash-out is of the same order as the thefts I can see directly, while the laundering layers the money joins are far larger and pooled with other thefts.
- UNK_DeadDrop's drain recipients come from a server-side configuration at claim time, so no sample recovers them and its cash-out stays untraced.

## Example: a theft that paid for a carrier

On 31 July 2024, between 15:33 and 15:37 UTC, four wallets belonging to the owner of an established token project's deployer key were emptied in full into `0x20e3b9f0`. That wallet later served as a BSC payload carrier for PolinRider's May to June 2025 generation. The deployer wallet's own contribution was 22.82 ETH, its entire balance after seven years and its last transaction ever.

The sweep did not look like the owner:

- it paid a priority fee nearly twenty times the owner's usual setting;
- it sent an exact balance-minus-gas amount to a fresh destination;
- it swapped and bridged within fifteen minutes.

That evening the project's dormant admin revoked all five of the deployer's roles on its token, treating the key as compromised.

The carrier swapped the ether to 74,723.18 USDT and bridged it to BNB Smart Chain (BSC). Once look-alike transfers are filtered out, its BSC history is two real legs, 74,720.49 USDT in and the same amount out eight hours later, among dozens of homoglyph and mirror-amount fakes. Even the carrier's BNB gas, three legs that arrived nineteen minutes before the USDT, came from the victim's own balances, swept in the same four and a half minutes. The infrastructure that later stored payload stages was paid for, gas and working capital alike, with stolen money. How that key leaked I do not know, and that recruitment malware took it is an inference only.

## Method: reading the ledger without touching it

That carrier is the cleanest example of what this part follows. An operator who puts a C2 channel on a public blockchain has to pay for it one transaction at a time, and every payment stays on the ledger.

All of my chain work was read-only. I sent no transaction and contacted no exchange, service, project or victim. I counted only transfers a wallet signed itself on the genuine token contract, because address poisoning floods token histories with look-alike transfers that would otherwise add millions in flows that never happened.

Everything here belongs to PolinRider, which, as [Part 17](17-two-operations-one-ecosystem.md) explains, is a separate operation from UNK_DeadDrop. The last section shows why the UNK_DeadDrop side of the ledger is almost empty.

## Cost: a small daily gas bill

PolinRider's on-chain C2 is cheap to run. Each write by the signal wallet `0x33ff3eda`, whose mechanics [Part 2](19-polinrider-ethereum-address-book.md) and [Part 3](20-polinrider-wallets-and-hosts.md) describe, is a transfer of zero or dust value, typically 150 wei. The recipient is an address that is really twenty bytes of data decoding as two IPv4 address and port pairs. A loader reads the newest transaction and takes its C2 from the recipient field.

- In the sixty days to 16 November 2026 the signal wallet advertised eleven records, ranging from 586 writes for one host to three writes over less than two hours for another, and its whole history since June decodes as 4,179.
- Over its whole life from 23 June to 15 November 2026 the signal wallet sent 4,181 transactions, none failed, for 0.0211 ETH of gas in all, about 0.00015 ETH a day.
- On the Ethereum NullReceiver branch, resolver wallet C paid a mean fee of 0.0000677 ETH per beacon at a mean interval of 3.34 hours, a daily cost of the order of 0.0005 ETH.
- Its remaining 0.0153 ETH bought about 226 beacons over roughly 32 days.

With a bill that small, who pays it is far more informative than how much it is.

The value carried is also what separates a record from a payment. The signal wallet's records carry zero value until 11:59 UTC on 16 September 2026, fifteen of them that morning, and dust from 13:41 UTC that day; the pointer channel's writes typically carry 500 wei. Its two funding payments to the pointer sender carry 0.01 ETH each, and read as records they decode as a convincing but fictitious pair of C2 hosts, because their twenty recipient bytes are the pointer sender's own address. Anyone decoding such a channel should drop the payments by value before reading hosts from it.

### One process behind both channels

The pointer sender `0x596dcc9f`, which writes payload pointers, ties the signal wallet to the carrier side. Its only funding is two payments of 0.01 ETH from the signal wallet. Between 16 September and 16 November 2026 the two channels each had a transaction in the same Ethereum block 315 times, out of 1,696 and 1,135 blocks with a transaction from each. One process scheduling both explains that; shared infrastructure does not.

![PolinRider's money flow from sources of funds through provisioning, carriers and resolvers to payouts and cash-out](assets/24-polinrider-money.png)

*Figure 1. Solid elements are signed transfers or roles read on chain. Dashed elements mark bridge funding not traced to a theft and laundering layers whose attributions belong to the public register. UNK_DeadDrop is not part of this graph.*

## Provisioning: disposable wallets and short bursts

### A gas tier built to break tracing

The signal wallet's gas comes from a tier of disposable wallets, each funded over a bridge minutes before it first pays and used only a few times:

- `0xd31a213e` paid the signal wallet five minutes after being funded and has four rows in its entire life;
- `0x461ebacc`, which funded it, is a one-shot pass-through whose own gas arrived over Gas[.]Zip from an unidentified chain, and it forwarded 100,004.28 USDC unchanged into the Bridgers bridge nineteen minutes after receiving it;
- `0x416d9906` was funded three times through Across, one to three minutes before each payment;
- `0x76d6ddcb` paid 36 seconds after Relay funded it.

That habit defeats same-chain tracing by design. Four hops above the signal wallet the trail reaches a person-operated DeFi wallet whose large exchange withdrawals each follow a one-dollar test, a human habit rather than a script's. The dollars diverge into a bridge while only the gas continues to the beacon, so that wallet is a lead and not a payer of the C2.

The tier is also separate from the large commercial payout graph discussed under NoOnes below. I took each side's counterparty closure, every sender and recipient of every genuine leg above a dust floor. The closures of the 219 signal-tier addresses and the 23,790 payout-tier addresses share nine, and every one of the nine is a labeled exchange hot wallet, which I read as no operational link.

### Provisioning wallets for carriers and dead drops

Carriers and dead-drop accounts are created by a few provisioning wallets whose lives are short lists of sends:

- The TRON wallet `TJ9F6EaJ` made seven outbound sends in 439 transactions, in two tight batches in October 2025 and January 2026, five of them demonstrably to dead-drop accounts, which makes it a provisioning wallet at high confidence.
- The Aptos side was provisioned in generations of three accounts created within half a minute by one creator, and at least three creators trace to one root funder.
- On BSC `0xade999f5` made eight non-zero BNB payments, two of which created the carriers `0xe69222e6` in October 2025 and `0xadd1b89e` in January 2026, while six paid USDT-forwarding wallets fed from FixedFloat's hot wallet. Operator control holds at medium-high confidence; whether that USDT flow is operator revenue is open.

Replaying the January generation gives this sequence:

1. The TRON dead-drop account was funded at 15:12:57.
2. The BSC funder was topped up at 15:18:14.
3. The carrier was funded at 15:22:25.

Funders fire four to twelve minutes before a generation's first write, which makes them the branch's earliest observable signal. The BSC provisioning wallet is more than a gas station. Its first signed transaction came on 1 October 2025, and its outflow reconciles to 26,440.27 USDT. Of its 57 recipients and the 17 sources of the deposit address it paid most, 39 slots are service deposit addresses, two are carriers, one is a drained victim and the rest are forwarders and unresolved payees.

When `0xade999f5` stopped on 21 May 2026, a successor payer, `0x5fb6f15a`, had appeared two days earlier, and it was still active on 12 November. It funded a new carrier, `0x779bb1bb`, alone, with 0.0153 BNB on 31 July 2026. On 4 August that carrier wrote a three-stage build with the same shim, main stage and loader triple as its predecessor, and it still holds gas.

### A paymaster that links the two resolver branches

The Ethereum resolver wallets are funded from a paymaster on BSC, `0xe6a869f1`, and from a drain collection wallet. The paymaster seeded resolver wallet C and, a minute earlier, a BSC payload store of the TRON branch whose calldata decrypts with NullReceiver keys. That is a direct financial link between PolinRider's two resolver branches, a relationship that infrastructure alone had left unsettled. The same paymaster paid wallet A's funder and the recipients of the drain collection wallet. None of its other nine gas grants became a resolver wallet, so that batch hides no unknown fourth resolver.

| Role | Wallet | Behavior | Confidence |
|---|---|---|---|
| C2 signal wallet | `0x33ff3eda` | writes IPv4 and port records as zero-value or dust transfers | high |
| Pointer sender | `0x596dcc9f` | writes payload pointers; funded only by the signal wallet | high |
| Signal-tier gas wallets | `0xd31a213e`, `0x461ebacc`, `0x416d9906`, `0x76d6ddcb` | bridge-fed, each funded minutes before it first pays, few payments | high |
| TRON provisioning wallet | `TJ9F6EaJ` | seven lifetime sends, five to dead-drop accounts | high |
| BSC provisioning wallet | `0xade999f5` | created two carriers; money-side payments | medium-high |
| Successor payer | `0x5fb6f15a` | provisioned carrier `0x779bb1bb`; active on 12 November 2026 | high |
| Resolver paymaster | `0xe6a869f1` | seeded resolver wallet C and a BSC payload store of the TRON branch | high |

*Table 1. PolinRider's C2 and provisioning wallets.*

## Sources: where the money comes from

### A register match for the carrier's recent pushes

The main carrier's October and November 2026 payload pushes were paid for with 0.008905 BNB that arrived on 8 October 2026 from `0x27d5cbba`. On 10 July 2025 that wallet had received the entire balances of a family of wallets on three chains within one hour, swapped them into stablecoins and moved the proceeds through Bridgers and Mayan. It then sat untouched for fifteen months before sending its last dust to the carrier.

The public [theft register maintained on GitHub](https://github.com/tayvano/lazarus-bluenoroff-research) records that sweep as a malicious-repository theft of about 44,000 dollars on that date, in which the victim ran code from a repository shared by a contact met online. Its record has the same victims and theft wallets, address for address and on the same date, as the chain I reconstructed independently. That is what makes a register match worth more than any label service. I read the lure as a take-home repository in a Contagious Interview developer approach, though that is my reading of the register's description. The funnel below the theft is shared by at least three thefts of summer 2025 and exits through one deposit address at an exchange, so it is a shared laundering path or a shared crew rather than the plumbing of one incident.

The carrier chain's August 2024 inflows are drains as well. The sweeper `0x204643da` drained forty victim wallets on five chains in one morning, and its stablecoins match to the cent what it then bridged, so the whole bridge batch into one TRON wallet that day is victims' money.

### A victim label that reads the wrong way

A public scam report of 28 August 2024 names `0x1046726f` as the address into which a victim's wallets were emptied, and the register files that wallet as a victim, citing the report. That fits a victim reporting where the money went, not a victim's own wallet. The wallet's own signed legs pay a register-listed Nexera laundering wallet and an operator depositor, and five operator wallets sent it their leftover gas on five chains. I treat it as operator-side at medium-high confidence. A third-party "victim" label is a claim about a report, not a reading of the wallet, and the wallet's signed legs decide it.

### Gas for a drain

The BSC provisioning wallet shows the same pattern at the smallest scale. On 13 May 2026 `0xade999f5` sent 0.00015 BNB of gas to an old wallet dormant since its owner's small exchange withdrawals of 2022. Within two and a half minutes every asset moved to a fresh wallet, which swapped them for 299.30 USDT and paid that into a FixedFloat deposit address seventeen minutes after the gas arrived. The drained wallet is most likely a compromised victim's and I treat it as a victim, not an indicator.

The reusable observation is that the provisioning wallet gasses three kinds of address:

- fresh carriers that then write;
- forwarders that move real stablecoins;
- old wallets with their own history that empty within minutes of the gas, which are victims.

### A ConcentricFi backdoor that is still armed

The largest source tied to the carrier chain is a backdoor that is still armed. On 22 January 2024 both `ConeCamelotFactory` contracts of the ConcentricFi vault system on Arbitrum were handed to an attacker key, `0x3f06d41f`. That key set an implementation on twelve vaults whose `withdrawFromAdmin(token, from)` function lets the admin, `0xc62a2546`, pull any approving wallet's balance up to its allowance.

On my own tabulation 95 of 541 such calls moved value from 55 victims, about 681,000 in stablecoins. That figure sums, per token, the successful value-moving calls over USDC, bridged USDC.e and USD₮0; the calls moved other tokens too, which I have not added. Most of it came after the public exploit, from approvers who kept funding their wallets. On the most-probed wallet, 369 of 371 calls were zero-amount probes and two took value.

The tie to PolinRider runs through money, because the admin's pulls fed the carrier chain's Arbitrum leg, and the wallet `0xee2e4fbe`, which gassed the admin minutes before two 2025 pulls, places those pulls in the carrier chain's cluster. No finding attributes the exploit itself to either operation.

No pull has occurred since August 2025, but dormancy is an inference: both factories still return the attacker key as manager. On 16 November 2026, 91 wallets still held open allowances to those vaults, 41 with balances that could be pulled. Anyone who ever approved them should revoke the allowance now. This is the most urgent practical result in this entire money trail.

### Serenity Shield: a second theft in the same money operation

A second register incident sits in the same money operation. On 27 February 2024, the register's date for the Serenity Shield theft, `0x43a5dd4f` took its first gas from the ConcentricFi exploit wallet `0x5e440f18`, moved 322,222 stolen SERSH tokens and passed SERSH on to a ConcentricFi wallet. In the middle of the theft it was topped up by six withdrawals totaling 32,732.15 USDT from one customer account at an exchange. The same exploit wallet later paid `0xee2e4fbe`, the wallet that gassed the 2025 pulls. These links bind the two thefts to one money operation and to the carrier chain's cluster, but they do not settle whose people executed the thefts.

### Drained wallets behind the resolver fees

The resolver side is paid for in the same way. The wallet that pays PolinRider's resolver fees, `0xf97062cb`, is a drain collection address into which about twenty-two established personal wallets were emptied, about twenty-one of them sending it their last outgoing transaction ever, nine within eleven minutes on 3 September. The clearest case is an ordinary user's wallet active since 2021, emptied in nineteen minutes, whose key a second, unrelated party later used. The link runs both ways: resolver wallet B returned its remaining 0.0293 ETH to the collection wallet on 14 October, the day both wallets addressed the same C2 host.

A linked sweep hub emptied about 1,270 more. The operator very probably holds keys to around 1,340 wallets, although whether those keys came from PolinRider's own stealer remains an inference. A batch of 1,161 of them swept in two hours on 3 November is most likely one airdrop farmer's stolen key store, as [Part 5](22-polinrider-counting-repositories.md) shows.

Three inferences stay open on the resolver side: that the transfers were thefts, that the keys came from this campaign's stealer, and that all the addresses belong to one actor. The carrier side supports the same conclusion on stronger ground, because its thefts are confirmed against the public register.

## Laundering: across the bridges

The carrier chain's stolen money leaves BNB Smart Chain by bridge, through Allbridge Core's USDT pool and bridge and Stargate's v1 and v2 USDT pools, which I identified by verified contract source; the small BNB legs beside each deposit are Allbridge messaging fees. All eighteen deposits of the carrier's peel chain went to TRON.

The real path is a peel chain of single-use wallets into the Allbridge pool. The vanity-suffix address families around it are address poisoning: the first hop signed exactly six transactions, equal to its nonce, and 161 of its 170 apparent outbound legs fall in its look-alike set. The chain's 647-address hop set meets the 87,719 addresses of the NoOnes payout loop in one exchange hot wallet only, so the carrier's money does not touch that pipeline.

- On BSC the 2024 carrier's 74,720.49 USDT was consolidated in one wallet together with 448,818.17 USDT of Nexera theft proceeds, a wallet the register lists under that theft.
- On TRON four receiving wallets passed leftover gas down a chain before consolidating in another Nexera-listed wallet that took 2,978,110 USDT in genuine legs from 25 senders.

I matched every one of the 32 TRON receipts to its source deposit by the Allbridge message nonce and confirmed each against Allbridge's public endpoint. All six depositors are operator wallets, among them single-use carriers passing gas down a chain, a six-chain consolidation wallet and a drainer collection wallet. One of them, `0xc21ed7bf`, swept two dust collectors that the register lists under Contagious Interview on six chains in about seventy minutes.

Below the Nexera consolidation point the TRON web is some twenty interlinked wallets moving between 0.3 and 9.8 million USDT each and sharing four hubs. One hub and several counterparties are hot wallets of two large exchanges; the other three hubs carry no tag and remain unidentified, and positions one wallet held at the JustLend lending market were redeemed through fresh wallets. The web's passages through the tagged hot wallets are a records question for those exchanges, not evidence of more operator infrastructure.

The ConcentricFi proceeds enter a BNB laundering layer that the register lists under about a dozen thefts it attributes to DPRK-linked actors, among them Seedify, OpenFabric, Store-V, Tapioca, AreonX and PolinRider itself. ConcentricFi's share of that layer is about 107,500 of more than 8.6 million. The layer ends at exchange hot wallets and exits through 44 Bridgers swaps and through Symbiosis to TRON, and it was still sending in October 2026. Once look-alike transfers are filtered out, its fan-out wallets have a median of about seventeen real recipients each.

Two further edges join the same layer from other sides:

- The TRON payroll's signer key `TZ39EeGd` sent 119,000 through deBridge into the register-listed Seedify layer, money taken from a wallet that is most likely a compromised victim's.
- A cross-chain sweep wallet that the register files as a "DPRK IT Dust Collector" of April 2024 took five single-use cash-out wallets at eighteen-second intervals and exits through one shared exchange deposit address. On Solana, a wallet that received three programs' upgrade authority in February 2024 upgraded and closed seven programs, at least four of them another developer's, and bridged the proceeds into a wallet that paid one of those five cash-out wallets. That this was theft rather than the owner's own exit holds at low to medium confidence only, and I place the episode on PolinRider's side by its counterparties alone. These are strong statements about shared laundering infrastructure and weak ones about identity, because a laundering layer serves whoever pays it. Every DPRK label in this part is the register's reading or that of the reports it cites, among them a [Multilateral Sanctions Monitoring Team report](https://www.gov.uk/government/news/joint-statement-of-the-multilateral-sanctions-monitoring-team-msmt-on-the-report-covering-dprk-cyber-and-it-worker-activities) that I have not read myself.

## Payouts: payroll, processors and swap services

### GasFree payroll on TRON

On TRON, PolinRider pays recurring recipients through GasFree accounts, which let a wallet send USDT on a signed permit without holding TRX. The payout transaction never shows the real signer, so I had to read it from the permit's user field.

One payroll ran through four such accounts from April to December 2025, partly overlapping, each signed by its own key and sharing 18 to 43 payees pairwise, each making one-off payments of about 467.84 USDT. The first of them received the ConcentricFi proceeds, and all 175 of its outbound permits carry one signer, `TL3NqcUx`, which makes it an operator payout wallet. Those fixed amounts turn out not to be wages but checkout addresses of a pooled payment processor.

Up to four further accounts followed, overlapping in time, one of them still paying on 11 November 2026, but the payroll has all but stopped: the last account's payouts fell from 42 in April 2026 to one in November. A wallet in the same graph with treasury-like flows is an energy-rental service rather than a treasury.

### A pass-through between exchanges

A TRON pass-through, `TDX4sysH`, shows how a carrier-funding wallet sits between exchanges on both sides. It moved about 275,600 USDT between January and July 2024, 91 percent of it in sixteen transfers to five wallets that funded the TRON carrier. It has 96 small payees, and in a sample of 32 of them, 21 cash out into the same two exchange hot wallets that fund it. Its first funding traces at high confidence, through six Allbridge legs matched by nonce, to an Ethereum wallet that itself cashes out at deposit addresses of three exchanges.

### The successor payer

The successor payer `0x5fb6f15a` signed 271 transactions paying 133,753.77 USDT to 80 recipients on BSC and 32,014.87 USDC to 41 on Base. With a sub-payer it reached 130 distinct BSC recipients:

| Recipient kind | Count |
|---|---:|
| Service addresses, mostly deposit addresses at instant-exchange services and exchanges | 86 |
| Unresolved payees, none of them drain-shaped | 34 |
| Forwarders | 8 |
| Carrier | 1 |
| Polymarket account | 1 |
| Drained victims | 0 |

*Table 2. The successor payer's BSC recipients.*

The successor payer was itself funded largely by withdrawals from one exchange's hot wallet and through relays that the exchange funds. A predecessor payer, active from June to December 2025, handed thirteen payees to a new wallet twelve days after it stopped, the same hand-over pattern as from the BSC funder to its successor.

### Purchases and bets

The carrier side buys fixed-price items through a payment service on Base whose brand nothing I consulted names. The provisioning funder and the successor payer paid 34 deposit proxies, all 45-byte clones of one implementation and reusable checkout addresses paid by more than a thousand unrelated senders. A single claimer sweeps them into a vault, a multi-signature Safe and a deposit address at a regulated exchange that has taken 3.28 million USDC on Base. The operator's payments come in bursts of identical sums seconds apart, such as 61.336046 three times in 48 seconds, at price points unrelated buyers also pay, which I read as catalogue purchases in multiples rather than payroll. The service's configuration contract dates from 2018, so it has run since then.

The carrier side also bets. Three of the provisioning funder's exits that present as bridge deposit addresses are Polymarket deposit wallets. Four Polymarket accounts cycle money with the funder and with an exchange deposit address in a loop on 5 and 6 May 2026 that binds them to one controller at medium-high confidence. Two further accounts followed. The newest, funded on 11 November 2026, made twenty one-cent maker trades on five-minute Bitcoin markets on 12 and 13 November and lost every one. The sums are small, but the accounts are bound to operator wallets, which makes the platform's records a further identification route.

### A relay of short-lived paymasters

The resolver side runs on a relay of short-lived paymasters, at work since at least February 2026, ten of them confirmed by their nonce history. Each was filled by a payout from a no-registration swap service, used for three days to six weeks (3, 4, 9, 13, 13, 14, 26, 26, 30 and 43 days from first to last transaction) to pay the same small set of people in round USDT amounts, and then abandoned. I found no operator tier above them: every unresolved source above the relay resolves to a service payout.

Not every wallet near the relay is the operator's. The three addresses with hub-like flows in that layer are retail wallets, and an adjacent wallet, `0xb0fcbf05`, is a commercial USDT payout processor that made about 97,000 transfers of arbitrary amounts to different recipients. Thirteen addresses pass the nonce-over-time test as operator wallets: the ten paymasters, a standing treasury, a splitter and a funder-remainder recipient.

The three recurring payees are person-operated wallets that cash out at deposit addresses on four exchanges. They are the strongest identification lead on that side, although the chain cannot say whether they are members or contractors. No address receives from all three, and they read as independently paid individuals.

The clock separates the two halves of the network. The resolver wallets are provably automated, while the money side shows hand-started batches. Measured as the share of a wallet series' flow events that fall between 00:00 and 10:00 UTC, the paymasters, collection wallet and hub reach 91 to 94 percent, against 57 percent for the payees and about 42 percent under a uniform clock.

The resolver side's own cash-out runs through a splitter into single-use addresses that each deposit to FixedFloat within a minute: 15.197 BNB, or about 10,300 dollars, on 3 and 7 November 2026, with the same shape four months earlier. FixedFloat requires no registration, so its payouts carry an order record rather than an account. The wallet that funded two resolver wallets is FixedFloat's own payout address, so the resolver side's funding runs entirely on non-custodial rails, with no exchange account to ask for records. On the carrier side, a one-shot forwarder, `0x496a0cfc`, moved a FixedFloat order into an operator-used exchange deposit address thirty-six seconds after the provisioning wallet gassed it, and the order's owner is not established.

### NoOnes: a venue, not the operation

One large payout pipeline above the resolver paymasters looked at first like the operation's money machine. It is in fact the custody of the peer-to-peer marketplace NoOnes, identified at high confidence by three observations:

- whole-address matches with the register's venue tags;
- hundreds of payouts on the day of NoOnes' January 2025 hack, two hops behind a consolidation address that [Merkle Science published](https://merklescience.com/blog/hack-track-noones-flow-of-funds-analysis);
- its collapse during the wind-down NoOnes announced from 17 August 2026.

A fourth line is structural: per-customer deposit addresses that are gassed and then swept, which is a custodial business rather than an intrusion set. Of the eight register addresses on lines naming NoOnes, two received native sends signed by the pipeline's own gas stations, and the same test against other venues returned nothing. The pipeline's head paid out hundreds of legs of just under 7,000 USDT on the hack day. Depositors and payout recipients are two populations with not one address in common, one gas station fed every treasury generation from March 2023, and the money above the treasuries is a commercial desk with thousands of senders.

The treasury `0x7058ba20` signs its own transactions, receives batched customer withdrawals from an exchange hot wallet and pays them on to its own deposit address at a stablecoin issuer, so it is the marketplace's self-held treasury using its own exchange account in both directions. The same key holder kept operating collection and payout wallets after NoOnes closed its peer-to-peer marketplace on 21 August 2026, under an unknown brand. Two reads of the same service wallets from different data providers differ by one to three orders of magnitude and are not reconciled, so any figure from them must name its source.

PolinRider was one of its customers. Within the 113 case wallets I read, its exposure comes down to two NoOnes deposit addresses, one of them certainly a single account. They are what remains of 36 candidate addresses, most of which were paid only by wallets carrying public service labels. I then checked 854 of the 855 recipients of the remaining wallets for payments of their own to NoOnes, the unread one being a DEX router contract, and found the same two and no third. Eighteen recorded withdrawals came from shared hot wallets and identify no account. The lesson for compliance teams is that a high-volume payout graph with gas-then-sweep deposit addresses is a custodial platform, and its deposit addresses should be compared with public venue registers before it is read as an operation's money machine.

## Exchanges: touchpoints and what each can prove

Every route from this money to a person runs through a service's records. I graded each edge by what it can prove rather than by how suspicious it looks.

- **Strongest:** a deposit address at one exchange took 52 deposits, 15 of them from the provisioning funder and the rest from operator-gassed wallets, and its first funding was 1,500 USDT from the provisioning wallet. I identified it as a deposit address because its only gas comes from that exchange's own deposit funder, a wallet with a nonce above two million that sends exactly one sweep's gas minutes after each deposit and whose sampled recipients sweep to the same hot wallet in 24 of 25 cases, and because every receipt is swept in full within minutes. Only the exchange can say whether the account is the operator's own or a broker's; it took deposits on Base before the funder existed. Two further deposit addresses at the same exchange look operator-used.
- **Second exchange:** two customer accounts took 128,224.74 USDT of operator-side deposits. An account at that same exchange topped up a wallet in the middle of the February 2024 Serenity Shield theft, the most direct exchange item on the theft side.

A single withdrawal proves one funding act, a swap-service payout proves an order, and a shared service proves nothing.

| Edge | Kind | What it can prove | Strength |
|---|---|---|---|
| Deposit address at the first exchange, 52 deposits from the funder and operator-gassed depositors | repeated customer deposits | an account the operation uses, own or a broker's | strong |
| Two accounts at the second exchange, 128,224.74 USDT through forwarders | repeated customer deposits | accounts receiving operator money | strong |
| Account at the second exchange funding the Serenity Shield money wallet | withdrawals during a theft | an account holder financing a theft in progress | moderate to strong |
| Two further deposit addresses at the first exchange | customer deposits | probable operator-used accounts | moderate |
| Successor payer funded by withdrawals from the first exchange | withdrawals | an account holder funding the payer | moderate |
| Resolver payees' cash-out at four exchanges | personal deposits | people paid by the operation | moderate, role undecided |
| Deposit address at the second exchange below the 2025 funnel | deposit below a shared funnel | an account below several thefts | moderate, shared |
| Three exchange deposits above `TDX4sysH` | deposits one hop above | a funder's own cash-out | weak to moderate |
| FixedFloat orders | no-registration swaps | where an order's output went | weak, law enforcement only |
| Shared swap-service payout | service payout | a shared habit | none |

*Table 3. PolinRider's exchange and service touchpoints, graded by what they can prove.*

Before a wallet that sweeps everything to an exchange hot wallet is called a consolidation hub, it should be tested by its gas source for being the exchange's own deposit address.

Added up, the cash-out I can attribute to accounts PolinRider uses comes to a few hundred thousand dollars:

- 128,224.74 USDT into two accounts at the second exchange;
- a little over ten thousand from the funder into deposit addresses at the first exchange;
- the successor payer's 133,753.77 USDT and 32,014.87 USDC, spread across exchanges, services and purchases;
- about 10,300 dollars through the resolver side's FixedFloat splitter.

That is the same order as the thefts I can see directly, from the deployer key's 22.82 ETH to about 681,000 in stablecoins pulled through the vault backdoor, and it fits a reading in which the observed cash-out pays for the infrastructure and little more. The laundering layers the money joins are far larger and pooled with other thefts in ways that cannot be apportioned. None of these touchpoints has been put to the exchange concerned, and account details stay out of anything I publish. In my record, PolinRider's resolver money network has no on-chain link to the October 2026 exchange theft that the [FBI attributes to TraderTraitor](https://www.fbi.gov/investigate/cyber/alerts/2026/north-korea-responsible-for-6-billion-binance-attack); only the delivery method is shared.

## UNK_DeadDrop: why the cash-out stays untraced

UNK_DeadDrop left almost nothing on chain to follow, and the reason is in its own console. The recovered client modules of the operators' dashboard, described in the [administration platform post](08-administration-platform.md) of the UNK_DeadDrop series, contain a SuperAdmin-gated wallet page. It is coded to import victims' seed phrases and Bittensor cold keys, preview balances and claim them, with `eros1030109@gmail[.]com` named as the only account allowed to run the drain.

The backend supplies the recipient addresses for those claims from a server-side configuration at claim time. The receiving addresses never reach a victim's machine, so no sample recovers them. The two routes I could run without a victim coming forward both came back negative:

- a public Bittensor coldkey drain check;
- a sweep of scam and blocklist databases on 24 July 2026.

A seedless shape search for drainer consolidation addresses on a full-chain indexer, constrained by the campaign window and the stolen assets, remains possible; I have not run it.

The one exchange lever on that side is a single seed-funding link. The operators' primary Solana wallet received its first funding of about 12 SOL on 17 August 2024 from an exchange hot wallet. That shows that someone with an account there funded the wallet once and says nothing about where the operators bank. The same exchange also appears on PolinRider's side, which, like a shared swap service, links nothing. The rest is small:

- **A gambling side business that never scaled.** The operator ran a custodial deposit-gambling wheel behind one of its persona front domains, with its primary wallet as upgrade authority of the game program. A liquidity pull and a withdrawal freeze were live capabilities, but my check of 24 July 2026 found neither exercised at any scale, the coin dormant and the backend decommissioned. The token behind that front predates the operator's involvement, with a first liquidity pool in July 2023, so the token and its community channels are not operator indicators.
- **Persona-farm engagement wallets.** One seat of the persona farm's sub-ring worked inside a DeFi client in 2022, and its engagement wallet was funded by the client's team wallets and shows only dollar-scale tests of the client's contracts. It is working capital the client issued rather than a payout path, and its value is evidentiary: it dates the engagement and binds the seat to the client, as the [persona farm post](15-persona-farm.md) of the UNK_DeadDrop series describes.

## Limitations

- Labels are the largest source of error. There is no public Blockscout instance for BSC, so every BSC label I use is an Ethereum label applied to the same address on chain 56, an inference to be confirmed by the labeling party.
- Explorers cap and page their reads, so a read that stopped at its cap can hide legs. Where a figure rests on a capped read, as in the NoOnes check, it holds within those reads.
- Register attributions, including every DPRK label here, are their authors' readings; on-chain pooling shows shared infrastructure, not identity.
- Several thefts behind the money remain inferences about the key's leak rather than observed infections, and none of the touchpoints has been confirmed by the service concerned.

## Conclusion

PolinRider's C2 costs little to run, and stolen money pays for it at every layer, from a carrier's first gas to the resolver fees. The observed cash-out is small next to the laundering layers it joins, and every route to a person runs through a service's records.

For defenders the most urgent step is practical: anyone who ever approved the ConcentricFi vaults should revoke the allowance now. Provisioning funders that fire four to twelve minutes before a generation's first write are the earliest signal for anyone watching the chain.

PolinRider bought takedown resistance at the price of a permanent public record of its instructions and its money, while UNK_DeadDrop kept both on a server, and that contrast is where this series closes, after [the detection part that precedes it](23-polinrider-detection.md).
