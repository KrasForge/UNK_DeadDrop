---
title: "Historical indicators, artifacts and network evidence"
description: "Defanged URLs, hostnames, artifact hashes, resolver values, paths and IP associations with their evidence limits."
date: "2026-10-28"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/indicators/"
tags:
  - "UNK_DeadDrop"
  - "threat intelligence"
  - "indicators"
---

The entries below are historical. Case observations run through 24 July 2026, and current availability has not been rechecked. URLs and hostnames are defanged.

A value in source code, a message or a configuration file shows what that artifact contained; it does not by itself prove that a victim requested it. The tables distinguish held samples, recovered response bodies, third-party scan or DNS observations, and analyst inferences. Private contact databases, credentials, tokens and wallet material are excluded.

## Lure hosts and captured URLs

| Indicator | Evidence and interpretation | Limit |
| --- | --- | --- |
| `hxxps://nodit[.]org/` | The 22 June recruitment email linked to a Nodit-themed screening page. A later URLScan response-store capture preserved a JavaScript bundle with the same clipboard and command-execution kit. The message is fingerprinted in [E01](../preprint/evidence/E01.pdf). | The retained capture does not establish that a recipient fetched the page. The relationship to the held ClickFix samples is assessed as moderate. `nodit[.]io` is the legitimate company domain, not an indicator. |
| `hxxps://joincategory[.]xyz/` | Hostname attached to the retained reference lure bundle in [E02](../preprint/evidence/E02.pdf). Bundle SHA-256: `5ee915bb8d0363bd92176cc595d7425fd7e7830508d8824d90b5285a3d2b11bd`. | A recovered bundle does not show that a recipient fetched it. |
| `hxxps://www.d2saitrade[.]ink/careers` | The 21 July email and the retained site bundle identify this lure host. Bundle SHA-256: `775b939e40a2aeb56a741b2f4c1f93e77cac59a4484803af6bed25017d70c5c4`; see [E01](../preprint/evidence/E01.pdf) and [E02](../preprint/evidence/E02.pdf). | The page's JavaScript constructs download URLs from its own origin. The route strings below are code-derived; no victim request log was retained. |
| `hxxps://dscufo[.]xyz/` | A URLScan-harvested heavy lure bundle contains the device-check and face-model behavior described in [E02](../preprint/evidence/E02.pdf). Compressed bundle SHA-256: `63b47a480acca87c685e48bb9e9e0306313b322e724af85fa5a86db014232114`. | A capture of the bundle does not establish that a recipient visited the site. |
| `hxxps://discufo[.]xyz/` and `hxxps://www.discufo[.]xyz/` | A recovered URLScan response body contains the same clipboard-substitution lure kit. Its retained response-body SHA-256 is listed below. | Captured JavaScript establishes what the page could do, not a visit or execution. |
| `hxxps://nemesistrade[.]work/` | The retained URLScan-derived bundle bodies had the same face-model markers as the `dscufo[.]xyz` variant, as recorded in [E02](../preprint/evidence/E02.pdf). | No received lure email was retained for this hostname. |
| `hxxps://trixauvex[.]org/` and `hxxps://www.trixauvex[.]org/` | A recovered response body contains the same ClickFix kit. The body is only 393 bytes, so this is a limited capture of the page response. | No full page bundle or victim request log was retained for this hostname. |
| `hxxps://calendly[.]foxtopia[.]xyz/` and `hxxps://calendly[.]optixauvex[.]us/` | URLScan response-store captures preserved scheduling-themed pages using the same lure kit. The two body hashes are listed below. | These are historical captured pages, not evidence of a candidate's scheduling activity. |
| `hxxps://apexsyshire[.]ink/` and `hxxps://surgecareer[.]ink/` | July incident records preserve site bundles and stage-one samples associated with these lure names. `apexsyshire[.]ink` samples contain `/guard-launcher-result` and `/guard-install-log`; the `surgecareer[.]ink` bundle shares the ClickFix markers. | These are historical site and sample observations. No email to the investigator was retained for either hostname, and current status is unknown. |
| `hxxps://validator[.]aavzx[.]ink/` | A 23 July capture preserved a ClickFix page that downloaded the `upd_m` and `upd_w` droppers from `api.aazdias[.]ink`. | The page used an Almanac-themed pretext. `almanac[.]market` is a separate, legitimate service and is not an indicator. |
| `hxxps://3dscenebox[.]online/` and `hxxps://www.3dscenebox[.]online/` | A 24 July capture preserved a 3D box-preview lure and `check_3d_m` / `check_3d_w` droppers. Their SHA-256 values were `d2eb133d836ec35496f1d170df4fb451eea95f375dad73e4dba36ebd78226c2b` and `978424c9b22eef3d72d6e81ff5e10d4b4a7a2a0a08d683ed78b98b85707959d2`. | The droppers matched the previously collected July build. A fetch is not evidence that a recipient executed it. |

The late July captures also recorded renewed resolution of `d2saitrade[.]ink`, `joincategory[.]xyz`, `apexsyshire[.]ink` and `surgecareer[.]ink` to `170.205.31[.]182`. This was an observation on 23 July, not a current resolution check. The source notes identify the page skins as interchangeable and do not establish separate targeting of 3D artists or validator operators.

The retained D2S and later lure bundles contain origin-relative path strings including `/apply`, `/anti-bot-check`, `/application-status`, `/device-check`, `/environment-setup`, `/design-challenge`, `/complete`, `/guide.mp4`, `/verify_m`, `/verify_w`, `/check_3d_m`, `/check_3d_w`, `/check_bot_m`, `/check_bot_w`, `/check_env_m`, `/geetest_m`, `/track-activity`, `/guard-launcher-result` and `/guard-install-log`. These are useful hunt pivots when paired with the lure origin and surrounding behavior. A path alone is not unique to this activity, and no victim request logs were retained.

The July URLScan response-store harvest recovered 15 unique bodies across the lure fleet. The [artifact and sample reference](artifact-reference.md) lists full hashes for the 14 retained bodies that do not expose the persona-named `diobenu2silva[.]com` host. The hashes identify the retained response representation; some JavaScript responses were gzip-compressed. [E02](../preprint/evidence/E02.pdf) documents selected lure-bundle examples. The complete provider response records and raw response set are not included in the public evidence bundle.

The `api.domatisc[.]ink` response included a Google-branded login script. The separate Subtensor panel files retained for [E20](../preprint/evidence/E20.pdf) have different hashes and are not assumed to be the same version. Neither capture involved a login attempt.

## Resolver and payload destinations

The recovered client references the raw GitLab resource below. The repository bundle preserves the file-specific commit history in [E07](../preprint/evidence/E07.pdf).

```text
hxxps://gitlab[.]com/drop-indexing/tasks/-/raw/main/config.json
```

| Date (UTC) | File or revision | Recorded values | Interpretation |
| --- | --- | --- | --- |
| 26 May, 01:57 | `config.json`, `bb62474` | `domatisc[.]ink`, `coslyintra[.]online`, `valorecuiting[.]online` | Initial list in the retained history. |
| 26 May, 02:11 | `config.json`, `80cbe5a` | `domatisc[.]ink`, `coslyintra[.]online` | `valorecuiting[.]online` was removed. |
| 26 May, 02:15 | `config.json`, `1f5c121` | `domatisc[.]ink`, `coslyintra[.]online`, `valorecuiting[.]online` | The earlier list was restored. |
| 26 May, 02:17 | `config.json`, `52f6173` | `api.domatisc[.]ink`, `api.coslyintra[.]online`, `api.valorecuiting[.]online` | API subdomains were introduced. |
| 26 May, 02:23 | `config.json`, `87b9974` | `api.domatisc[.]ink`, `api.coslyintra[.]online` | `api.valorecuiting[.]online` was removed. |
| 1 June, 06:20 | separate `config-alt.json`, `47b13d3` | `api.onoplainai[.]ink`, `api.migadyn[.]info` | The file exists in the repository, but neither retained payload references it. Client use is unestablished. |
| 13 July, 07:10 | `config.json`, `c3c71d6` | `api.cklomino[.]ink`, `api.dsfmot[.]xyz` | The referenced primary list changed. |

The JavaScript also contains the fallback `wss://api.domatisc[.]ink`. The stage-two scripts contain these defaults:

```text
hxxps://api.aavzx[.]ink/install_guard.js
hxxps://api.aavzx[.]ink/guard-install-log
hxxps://api.aavzx[.]ink/node/<node-tarball>.tar.gz
hxxps://api.fallbaav[.]ink/                 fallback store
```

A later deepfake_guard build used a different store pair, embedded directly in the droppers rather than recovered from `config.json`:

```text
hxxps://api.aazdias[.]ink/install_guard.js
hxxps://api.aazdias[.]ink/upd_m
hxxps://api.aazdias[.]ink/upd_w
hxxps://api.aazdias[.]ink/upda_m
hxxps://api.aazdias[.]ink/upda_w
hxxps://api.fallaazdis[.]ink/install_guard.js   fallback
hxxps://api.aazdias[.]ink/guard-install-log
hxxps://api.aazdias[.]ink/guard-launcher-result
```

The four July droppers had these SHA-256 values: `upd_m` `d2eb133d836ec35496f1d170df4fb451eea95f375dad73e4dba36ebd78226c2b`, `upd_w` `978424c9b22eef3d72d6e81ff5e10d4b4a7a2a0a08d683ed78b98b85707959d2`, `upda_m` `f356fea9c672a23d508f4d219cd26d37a4555b1203f2a7a54458617ac6846a39` and `upda_w` `db1a888a8134978a98c29083625ad8105464c9058b43ab8d9486906c3c927f94`. The names and URLs identify recovered code paths, not successful execution.

An earlier URLScan-derived sample from `hxxps://deep-ai-guard[.]store/install_guard_d.js` had gzip SHA-256 `66a18c587d54b4703e67020c55d3961450ea64f43ad30eebdd97c8b0450de98a`; the installer hash was `6039d9ef0777b5d78a0bc46840fe2529a37ee910ff5467a62b019fc9117d0922`, and the decrypted stealer hash was `70ea6e2eaab58bdb83b7b235dd6253ffbcaed5e7df0286cbefd72d7650c3f47a`. Its decrypted code referenced `wss://api.domatisc[.]ink`, `hxxps://api.aavcareer[.]ink/mark-complete` and the same GitLab resolver. The original URLScan provider response is not in the public evidence bundle. The retained static analysis corroborates the code strings, but not a victim request to those endpoints.

The collection code uses paths such as `/api/company-wallet/upload-chunk/init`, `/api/company-wallet/upload-chunk/<upload-id>/<chunk-number>` and `/api/company-wallet/upload-chunk/<upload-id>/complete`. The server origin is resolved from configuration, so these paths are not a fixed full URL. The source establishes intended requests, not successful uploads.

## Mail, administration and service-route observations

These names come from received-message headers, DNS or certificate-transparency observations, and recovered frontend code. They do not all have the same evidentiary weight.

| Host or path | Recorded observation | Limit |
| --- | --- | --- |
| `dev.d2saitrade[.]ink`, `joincategory[.]xyz` | Retained message headers record Mailgun VERP envelope behavior for the D2S and Category Labs lures. | The sender's original network IP is not preserved in the forwarded messages. Provider attribution does not identify the person operating an account. |
| `email.dev.d2saitrade[.]ink` | Certificate and DNS records showed Mailgun configuration for the subdomain. | Configuration records do not prove a message was sent from this exact subdomain. |
| `email.apexsyshire[.]ink` | Certificate and DNS records showed Mailgun configuration. | No corresponding sent message was retained. |
| `email.hr.trixauvex[.]org` | A certificate-transparency name was recorded in May; the later July DNS review found it inactive. | A certificate name alone does not establish mail delivery or page content. |
| `hiring.aavcareer[.]ink`, `hiring.optixauvex[.]us` | Certificate-transparency names for recruiting-themed subdomains; later DNS checks found them inactive. | No page content or successful visit was retained for these subdomains. |
| `dashboard.cklomino[.]ink` | A certificate name and recovered Vite development client identify an administration frontend. Source references repository-status and wallet-management routes; see [E06](../preprint/evidence/E06.pdf) and [E09](../preprint/evidence/E09.pdf). | The evidence is frontend source. No login or authenticated API call was made, and no server-side records were recovered. |
| `api.domatisc[.]ink` | Separate captures preserve a Google-branded login page and login script; E20 also preserves a Subtensor-branded panel copy retrieved from this hostname. | The captures differ in content and hash. Neither proves that the bare IP served the same page; no login was attempted. |

The administration frontend contains these route strings:

```text
/api/github-jobs-check/
/api/db/...
/api/admin/wallets/refresh/
/api/admin/wallets/preview/
/api/admin/wallets/claim/
/api/admin/wallets/claim-all/
/guide/
```

These are code references, not recorded requests. The collection code separately contains `/api/company-wallet/upload`, `/api/company-wallet/upload-raw` and chunked-upload paths. Server origins are deployment-selected; the recovered code does not establish a successful upload or receipt of collected data.

## Historical IP associations

| Address | Recorded association | Evidence limit |
| --- | --- | --- |
| `23.137.105[.]75:5173` | Proofpoint and the case notes identify this as the earlier WebSocket C2 and lure-hosting address. The same IP hosted multiple lure names. | Historical association only. It does not justify blocking the surrounding `/24` or treating every hostname that resolved there as confirmed. |
| `23.137.105[.]75:3000` | A 22 July analyst observation recorded an Express response and an `OPTIONS` response allowing the `X-Guard-Platform` header, which also appears in the recovered installer. | This is an analyst probe recorded in case notes, not a retained public scan transcript. A generic 404 and blanket CORS preflight do not prove that a specific API route exists or accepted data. |
| `23.137.105[.]75:443` | A 23 July observation recorded the `apexsyshire[.]ink` lure page on this address. | Dated service observation only. The page and address have not been checked again. |
| `170.205.31[.]182` | The 23 and 24 July records associate this address with the lure fleet; the `3dscenebox[.]online` page was fetched from it. | Historical observation. Do not extend it to the surrounding `/24`. Current status has not been checked. |
| `170.205.30[.]227` | Earlier reporting and scan notes associate the address with campaign lure and payload hosting. | Prior-generation association, not a current indicator. |
| `170.205.29[.]83` | Listed by Proofpoint as an early sender IP. | External reporting; not a C2 address in the evidence reviewed here. |
| `207.241.172[.]222` | Historical Censys, Shodan and VirusTotal observations associated the address with an administration panel at `hxxps://207.241.172[.]222/` on port 443. A certificate observation named `api.cklomino[.]ink`. | Raw scan responses were not retained. The panel copy was fetched from `api.domatisc[.]ink`, not from this bare IP. The relationship is historical and does not establish exclusive tenancy. See [E20](../preprint/evidence/E20.pdf) and [E21](../preprint/evidence/E21.pdf). |

The July origin analysis also associated `api.dsfmot[.]xyz`, `api.aazdias[.]ink` and `api.fallaazdis[.]ink` with `207.241.172[.]222` through certificate and passive-scan records. The public evidence bundle does not contain the complete provider responses, so these remain source-limited associations rather than direct fetches from the origin.

## Additional passive-DNS leads

A 22 July analyst note records the following hostnames from a passive-DNS pivot on `23.137.105[.]75`. The provider response itself is not in the public evidence bundle. Treat these as historical leads, not confirmed malicious domains. The note said most newly observed names had no A record at the time of its 22 July check; that is not a current status check.

| Date recorded | Hostnames |
| --- | --- |
| 29 June | `api.aavcareer[.]ink`, `hiring.nemesistrade[.]work`, `nemesistrade[.]work`, `pumploki[.]space`, `www.pumploki[.]space`, `lilifindguy[.]xyz`, `www.lilifindguy[.]xyz`, `aitoonforge[.]space`, `www.aitoonforge[.]space`, `trixauvex[.]org`, `www.trixauvex[.]org`, `foxtopia[.]xyz`, `www.foxtopia[.]xyz`, `staging.optixauvex[.]us` |
| 30 June | `calendly.foxtopia[.]xyz`, `calendly.optixauvex[.]us` |
| 1 July | `calendly.dscufo[.]xyz`, `aavcareer[.]ink` |
| 2 July | `dscufo[.]xyz` |
| 6 July | `d2strade[.]xyz`, `www.d2strade[.]xyz`, `discufo[.]xyz`, `www.discufo[.]xyz`, `calendly.discufo[.]xyz` |
| 7 July | `www.nemesistrade[.]work` |
| 10 July | `d2s-trade[.]xyz`, `www.d2s-trade[.]xyz`, `dcsufo[.]xyz`, `www.dcsufo[.]xyz`, `book.dcsufo[.]xyz`, `geetebot[.]ink`, `www.geetebot[.]ink` |
| 13 July | `d2saitrade[.]ink`, `www.d2saitrade[.]ink`, `surgecareer[.]ink`, `www.surgecareer[.]ink` |
| 14 July | `joincategory[.]xyz`, `www.joincategory[.]xyz` |
| 19 July | `apexsyshire[.]ink`, `www.apexsyshire[.]ink` |

The later rows overlap the directly captured lure hosts listed above. Similar spelling is not proof that domains share an operator. `dcsufo[.]xyz`, `dscufo[.]xyz` and `discufo[.]xyz` remain separate names in the source records.

The local 22 July pivot note did not retain the passive-DNS provider response. It also recorded that most newly observed names had no A record at that time. These observations are leads only, and do not support treating every listed domain as a confirmed lure or C2.

### Hostname-only leads and exclusions

Later case notes contain more hostnames than the ones with a recovered page or sample. Keep these separate from the captured lure hosts above:

| Hostname | What the retained record supports | What it does not support |
| --- | --- | --- |
| `claude-detect[.]online`, `facedetect[.]ink` | Historical passive-DNS or hosting pivots; the URLScan search found no captures for either name. | No page body, delivered message or operator identity was recovered. These are leads, not confirmed lures. |
| `api[.]ceronetwork[.]org`, `career[.]ceronetwork[.]org`, `hiring[.]ceronetwork[.]org`, `staging[.]ceronetwork[.]org` | Names recorded in the historical infrastructure notes. | No retained page or response body establishes what they served or whether they were used. |
| `ergonia-labs[.]work`, `apply[.]ergonia-labs[.]work` | Names in an analyst pivot note. | No page capture or ownership evidence establishes impersonation or a campaign relationship. Do not treat the real `ergonia[.]io` as an indicator. |
| `nemesis[.]work` | Listed in Proofpoint's indicator set. A 22 July DNS check found it resolving to Porkbun registrar-parking addresses shared with unrelated sites. | It is not a live campaign host in that dated check and should not be treated as malicious infrastructure. Current status is unknown. |

The mail-sender review also used retained message headers and DNS/MX/SPF records. Personal addresses, envelope identifiers and the analyst's forwarding aliases are omitted. The source records do not preserve the original sender IP because the messages arrived through a forwarding service.

## Other domains from public reporting

Proofpoint's 8 June 2026 indicator table labels the following as sender or related infrastructure domains. They are included here as reported pivots, not as hostnames independently recovered from the held samples.

A local analyst note records a 22 July DNS review of 47 domains, with 46 returning NXDOMAIN or no A record and `nemesis[.]work` resolving to shared registrar parking. That review may overlap with locally held names and does not establish the state of every domain below. It is not a current check. See [Proofpoint's indicator table](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal).

```text
Reported sender domains:
recruitvex[.]us  onoplanoai[.]ink  trixauvexnet[.]ink
contacttrixauvex[.]ink  trixauvex[.]org  pulsynk[.]org
mailtrixauvex[.]ink  mailpulsynk[.]xyz  mailpredicttogether[.]ink
predicttocareer[.]space  nowurisch[.]fit  hyperdevpipline[.]org
valorecuiting[.]online  migadyn[.]info  empowerpharmacy[.]space
nxlog[.]tech  ondofinance[.]tech

Reported related infrastructure domains:
nemesistrade[.]work  ceronet[.]work  deep-ai-guard[.]store
ceronetwork[.]org  culyrax[.]us  elsavora[.]us  optixauvex[.]us
talentnexhr[.]ink  recruitptogether[.]xyz  contactpredicttogether[.]ink
connectptogether[.]ink  notifypulsynk[.]ink  contactpulsynk[.]ink
careertrixauvex[.]ink  cotrixauvex[.]ink  teampulsynk[.]team
careerpulsynk[.]xyz  predicttogetherrecruit[.]store
predicttogerecruit[.]store  predicttogether[.]ink
careerpredictto[.]space  togetherhire[.]fun
predictcareertogether[.]space  asteara[.]org  doxxela[.]ink
coslyintra[.]online  onoplainai[.]ink  raxvatange[.]ink
alphanonega[.]org  domatisc[.]ink
```

The reported sender IPs `170.205.29[.]83` and `170.205.30[.]227` are kept separate from the confirmed C2 and lure-origin roles above. Personal email addresses, analyst network addresses, victim account names and credentials are not reproduced.

## Post-cutoff public reporting leads

Later public reporting adds several leads for comparison with this case. The corresponding resolver generation or sample was not independently recovered, so these values remain separate from the historical indicators above.

The October report also describes four launcher markers found in the retained material: `deepfake_guard`, a POSIX double-fork, `/var/tmp/.kdm.XXXXXX` and `/guard-launcher-result`. That overlap supports further comparison, but does not verify the reported sample.

| Reported value | Source | What remains unverified |
| --- | --- | --- |
| `api.chestsoi[.]ink` | [Hopkins's investigation](https://brhopkins.uk/posts/foxtopia/), updated in August, places it in the GitLab dead-drop sequence. | It is absent from the resolver history retained here. No independent historical DNS or provider record was recovered. |
| `taikotalent[.]xyz`, `api.gaganata[.]ink`, `api.fallgganata[.]ink` | The [October developer-lure report](https://dev.to/edison_flores_6d2cd381b13/a-fake-recruiter-sent-me-a-job-offer-that-ended-in-my-terminal-the-trojan-is-still-live-2okf) names the lure and paired hosts. | The article and its follow-ups trace to one reporting chain. The domains were not checked for current activity. |
| SHA-256 `c7c22e322c17bda8198257342d4034af6250a5c433242461b870879ba9aa285d` | The same report and its [structured IOC follow-up](https://gist.github.com/eddyflores100-lang/198d8a13ba5901ea8ed7c63d5292c6ff). | No sample was independently recovered or hashed here. Treat the value as a reported lead, not a verified sample hash. |

See [Part 10](https://krasforge.github.io/UNK_DeadDrop/articles/10-investigation-connections/) for the comparison and its limits. These values are not a current blocklist.

## Delivery repository URLs

The July repository review identified these repositories as weaponized at the time of inspection:

```text
hxxps://github[.]com/Lyracartoon/predict-together
hxxps://github[.]com/pridnet/dscufo-assessment-fe
hxxps://gitlab[.]com/pulsynk/rekt-db
hxxps://gitlab[.]com/lautaro19/rekt-db
hxxps://gitlab[.]com/stefan[.]kano/forge-4626-invariants
hxxps://gitlab[.]com/predicttogether/forge-4626-invariants
```

The July inspection recorded five repositories with weaponized content. `lautaro19/rekt-db` is listed separately because coordinated creation timing and matching payload markers make operator control plausible, but do not prove it; the original repository snapshots and platform API responses were not retained. This is an ownership hypothesis, not a confirmed attribution.

These are dated observations, not statements about present availability. The GitLab group copy `pulsynk-org/rekt-db` was reported removed by GitLab in May; it is distinct from the separate `pulsynk/rekt-db` path above.

The case notes also record exact SHA-256 values for `tasks.json` (`c935808147f0236c81483d7bbeda4b9d602f3595d5d4057f8115d39e222d1c4b`) and `settings.json` (`35813f4401d3ad77b618275473a556eb47bfa6f4b7439dd8943b19f81aa7252e`) from specific repository variants. A file-hash match applies only to byte-identical files; it does not cover other task or settings variants. The limitations of this ownership reassessment are described in [E10](../preprint/evidence/E10.pdf).

The separate ECHOES delivery branch was recorded at `hxxps://github[.]com/Lyracartoon/Echoes-of-the-Unborn-Sun`, reported live on 23 July. Four archive revisions were preserved; the final PowerShell resource was unavailable, so this URL is not used to claim a confirmed link to the ClickFix or VSIX branches. The archive analysis is in [E11](../preprint/evidence/E11.pdf).

## What this list excludes

Cloudflare anycast addresses, Mailgun and Private Email infrastructure, and SimpleLogin relay addresses are shared services, not campaign-exclusive indicators. The legitimate `nodit[.]io` domain is not malicious. The earlier `foxtopia[.]xyz` parking subdomains `yandex-staff` and `rustore` were retracted as false associations.

Persona-associated domains, private email addresses, account identifiers, wallet addresses and credentials are omitted. The separate ECHOES archive branch is not assigned these resolver destinations because its final payload and relationship to this activity were not established.
