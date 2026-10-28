---
title: "Sample and repository artifact reference"
description: "SHA-256 values for retained lure, payload, archive and exact repository-file artifacts, with evidence scope and limits."
lastUpdated: 2026-10-28
---

This reference adds exact file identifiers to the [historical indicator list](/UNK_DeadDrop/indicators/). Case observations end on 24 July 2026. The hashes below identify retained files or case-recorded samples; they do not establish execution, infection or successful collection. Samples were analyzed statically. The public evidence PDFs contain selected records, not the raw binaries or a complete forensic sample set.

## Recovered lure and payload files

| Artifact | SHA-256 | Evidence and scope |
| --- | --- | --- |
| Joincategory reference lure JavaScript | `5ee915bb8d0363bd92176cc595d7425fd7e7830508d8824d90b5285a3d2b11bd` | Held reference sample; [E02](/UNK_DeadDrop/evidence/E02.pdf). |
| D2S AI Trade lure JavaScript | `775b939e40a2aeb56a741b2f4c1f93e77cac59a4484803af6bed25017d70c5c4` | Held sample; [E02](/UNK_DeadDrop/evidence/E02.pdf). |
| Dscufo heavy lure JavaScript, compressed capture | `63b47a480acca87c685e48bb9e9e0306313b322e724af85fa5a86db014232114` | URLScan-derived capture described in [E02](/UNK_DeadDrop/evidence/E02.pdf). |
| Dscufo heavy lure JavaScript, decompressed | `69cf5e6cc55ccb3ec8a9b43841cad61c7a3832b4e3114a5ff51151bd02ab8ae6` | Decompressed form of the preceding captured bundle; [E02](/UNK_DeadDrop/evidence/E02.pdf). |
| D2S Unix stage-one dropper, `verify_m` / `check_bot_m` / `check_3d_m` | `cc89d2d9435a55e0c79b5d6638f0e76dee5d5f2c42ffbfe13d4018c2498efab7` | Case-recorded sample hash; names share the same bytes in the retained D2S record. |
| D2S Windows stage-one dropper, `verify_w` / `check_bot_w` / `check_3d_w` | `89e916d067e469dcf7738ef71f8e38c3a3662cdc9fcbcfd1affa6892a496cd63` | Case-recorded sample hash; names share the same bytes in the retained D2S record. |
| Apex Unix stage-one dropper, `verify_m` and observed aliases | `3c6130446b8e5973398fe8d474ba7d28070546c88bcdd954e5a7d7bfa4136877` | Case-recorded sample hash; the retained note records several route names serving identical bytes. |
| Apex Windows stage-one dropper, `verify_w` and observed aliases | `10a0956882ea666cf0b873ec79d52425a73213c80325c4ce9317ce5e06a8f65b` | Case-recorded sample hash; route aliases are not separate binaries. |
| SceneBox Unix dropper, `check_3d_m` | `d2eb133d836ec35496f1d170df4fb451eea95f375dad73e4dba36ebd78226c2b` | 24 July capture; matched a previously collected July build. |
| SceneBox Windows dropper, `check_3d_w` | `978424c9b22eef3d72d6e81ff5e10d4b4a7a2a0a08d683ed78b98b85707959d2` | 24 July capture; matched a previously collected July build. |
| July installer `upd_m` | `d2eb133d836ec35496f1d170df4fb451eea95f375dad73e4dba36ebd78226c2b` | Recovered 23 July; same file hash as the SceneBox Unix dropper. |
| July installer `upd_w` | `978424c9b22eef3d72d6e81ff5e10d4b4a7a2a0a08d683ed78b98b85707959d2` | Recovered 23 July; same file hash as the SceneBox Windows dropper. |
| July installer `upda_m` | `f356fea9c672a23d508f4d219cd26d37a4555b1203f2a7a54458617ac6846a39` | Recovered 23 July. |
| July installer `upda_w` | `db1a888a8134978a98c29083625ad8105464c9058b43ab8d9486906c3c927f94` | Recovered 23 July. |
| D2S decoded Unix stage two | `4f863350a68405a7627c08c0d60c4da682c380e1a235b80ce7863ff77af857bf` | Case-recorded decoded sample. |
| D2S decoded Windows stage two | `a427c24b8eef4c0a5423238f1eaa919d9e4983ef427dd2cd7917c48141b2a101` | Case-recorded decoded sample. |
| Encrypted `install_guard.js` | `d24df1cacc01adee4e031b0f4d582448b7462f31975b57f553b7e0e86dddb184` | Retained installer sample; [E05](/UNK_DeadDrop/evidence/E05.pdf). |
| ClickFix stage-three JavaScript | `694626bed2df1f0d0026a3f7ead7692b44c7e73041cdd799b79a025335533cdc` | Held payload; [E05](/UNK_DeadDrop/evidence/E05.pdf) and [E17](/UNK_DeadDrop/evidence/E17.pdf). |
| Alternate large JavaScript payload | `5498038886bab8a8db2159495c015f26e322708fc7a7f3ea698e7b7c06e3d148` | Compared with the preceding payload in [E05](/UNK_DeadDrop/evidence/E05.pdf); embedded archive timestamps differ. |
| Windows agent archive | `be5859f23f0781242d854dc24c102c694dabfc14a159b56429e313f0521141b6` | Held bundle; [E05](/UNK_DeadDrop/evidence/E05.pdf) and [E12](/UNK_DeadDrop/evidence/E12.pdf). |
| Linux Overlord-derived Go implant | `ef183bbb40f4c7c3f4b52994cdba3295f3eab2604fdad99eefa3b67b8d966e8d` | Held Linux sample; [E05](/UNK_DeadDrop/evidence/E05.pdf), [E18](/UNK_DeadDrop/evidence/E18.pdf) and [E21](/UNK_DeadDrop/evidence/E21.pdf). |
| URLScan-captured gzip `install_guard_d.js` | `66a18c587d54b4703e67020c55d3961450ea64f43ad30eebdd97c8b0450de98a` | Recovered response body; the public exhibit set does not include the provider response record. |
| Decrypted `install_guard_d.js` installer | `6039d9ef0777b5d78a0bc46840fe2529a37ee910ff5467a62b019fc9117d0922` | Case-recorded offline decryption result. |
| Decrypted company-wallet collector | `70ea6e2eaab58bdb83b7b235dd6253ffbcaed5e7df0286cbefd72d7650c3f47a` | Decrypted sample; [E05](/UNK_DeadDrop/evidence/E05.pdf). |

## VSIX and extracted components

| Artifact | SHA-256 | Evidence |
| --- | --- | --- |
| `google-update-support.vsix` | `52886aab179f26421678ff23af1b0fabf0a17ffbb534369cdbbac8008cbed8e7` | [E03](/UNK_DeadDrop/evidence/E03.pdf) and [E12](/UNK_DeadDrop/evidence/E12.pdf). |
| Nested native-agent archive | `e1bf1b29e6fa3525d7f32f429290a88d6ea2890e61c06574b8ff6372aa5d0667` | [E03](/UNK_DeadDrop/evidence/E03.pdf) and [E12](/UNK_DeadDrop/evidence/E12.pdf). |
| macOS arm64 Go agent | `339907b44f161f57ff30819f422c552382ff437b3ae437463b4222cfe86bd943` | [E03](/UNK_DeadDrop/evidence/E03.pdf). |
| macOS amd64 Go agent | `bb10adac5b0124efedfe71102c1d5638135ec9e1cde8c8cb3353c5ed91bb9f81` | [E03](/UNK_DeadDrop/evidence/E03.pdf). |
| Linux amd64 Go agent | `a2b9a769df84d9d3a4694bb0252a2c6a5e5f5d1a85a04565362737092bbb3a86` | [E03](/UNK_DeadDrop/evidence/E03.pdf). |
| `extension.js` | `d5e9288693aa745dc89368deac677e7ea1ec81e663283af30838cdae189b7a7e` | [E04](/UNK_DeadDrop/evidence/E04.pdf). |
| Decrypted `detect_malware.py` | `4c3fdd86a59d52a0e29f472666cbf9472b6fd83c38ef2a4b547f31c72b8ee87e` | [E04](/UNK_DeadDrop/evidence/E04.pdf). |
| Decrypted `windows-agent-node.js` | `e5b7d6411d0c95da047185d94fca98d454b73df2e7f46f2753e212af2ca45da5` | [E04](/UNK_DeadDrop/evidence/E04.pdf). |
| Decrypted `windows-js-pipeline.js` | `bf820623e8deaa37092650c7fae594e56b8d81c27b541419006cca2d0536353b` | [E04](/UNK_DeadDrop/evidence/E04.pdf). |

## URLScan response-body hashes

The July response-store harvest recovered 15 unique bodies. These are the 14 retained response files that do not expose the persona-named `diobenu2silva[.]com` host. Hashes identify the exact retained response bytes; some JavaScript files were gzip-compressed. The raw provider records and response set are not part of the public evidence PDFs. Selected lure behaviors are documented in [E02](/UNK_DeadDrop/evidence/E02.pdf).

| Captured host | Response asset | SHA-256 |
| --- | --- | --- |
| `discufo[.]xyz` | `index-DsOcBcek.js` | `b821063f374b06b4c9afa8c66c86abe6323724c81cb2f337b786f02fe15ea04a` |
| `dscufo[.]xyz` | `index-CkxWQCI-.js` | `63b47a480acca87c685e48bb9e9e0306313b322e724af85fa5a86db014232114` |
| `dscufo[.]xyz` | `index-H6EfDx2S.js` | `6e8503baf235c4a7573dff94e40ffbba9390a126176fb305d76b5a1a6378da3c` |
| `nemesistrade[.]work` | `index-TCXLGCej.js` | `11c77d57227fdde36d8f6a495c8d50802fc47983fc1c3ea22f2edaf7dfa5f20b` |
| `nemesistrade[.]work` | `index-CgHQI6a2.js` | `bc02a75c29de834a313217a08fe54fb4556ed3e30765475e706e8e4d302dea9b` |
| `nodit[.]org` | `index-ZR13q5x-.js` | `bd9363382b9320af118567eb8db80a6be7da753a6f3d17713e4050fb16cefad7` |
| `d2saitrade[.]ink` | `index-BbbVfXCo.js`, compressed | `b2feefed4e90ec5a32d8ef1c9f7177f9f5f079a7968a4e7f15ca8bb7b3dd100c` |
| `joincategory[.]xyz` | `index-CoJPX8BM.js` | `1855a265c426457b686ee7109c7a05f943fcc30daa05fa33197eb04aaa2bf9b1` |
| `surgecareer[.]ink` | `index-CwZVxYHn.js` | `50b1d9788067171e87b52ce7b215aa3215ca61015c1547c674902a5569130297` |
| `calendly[.]foxtopia[.]xyz` | `index-DQhJCyLK.js` | `b5f932f24bb0fc8566c6573227a65e7848e7392fb3714de05e25b9c6d26d2668` |
| `calendly[.]optixauvex[.]us` | `index-B55lftHn.js` | `e92b3a873c1cb5fc8e648a4f6f3ae3f8364fc1229b6bf263da725c20a7bca356` |
| `trixauvex[.]org` | `index-Cj9V8mGV.js` | `ae71993f495bd2a8bb7edf94be888c0043c9d06c7d15e2c2455fcdc158fa68d8` |
| `api.domatisc[.]ink` | `assets/login.js` | `260ae84c3e852d180c94c920d0614a57a70abdcab0c493b902e1ca3c4aae9207` |
| `api.aavcareer[.]ink` | `install_guard_d.js`, gzip | `66a18c587d54b4703e67020c55d3961450ea64f43ad30eebdd97c8b0450de98a` |

The two retained `api.domatisc[.]ink` panel captures differ in content and hash. The Google-branded URLScan response above is not assumed to be the same version as the Subtensor panel files in [E20](/UNK_DeadDrop/evidence/E20.pdf). No login was attempted.

## ECHOES archive branch

The ECHOES archive and decoded-script hashes are useful for identifying the separate delivery branch. The final PowerShell resource was unavailable, and these values do not establish that ECHOES delivered the ClickFix or VSIX payloads. See [E11](/UNK_DeadDrop/evidence/E11.pdf).

| Artifact | SHA-256 |
| --- | --- |
| Archive revision `03f1795d` | `4ff03731d2061ad2f50da9f63dc1481374908d5bc837c86d0c7574d23b23a37b` |
| Archive revision `ded13153` | `2bd4cfd495fdcad6d7b2adaedc31614ca2984ea1246aed7608c339eaa82eb978` |
| Archive revision `b209f365` | `11bf34ccce585fe051abaa8d01ba1b29e2d44727c070b56ab0dd84a9dc9f91b2` |
| Retained current archive | `7db6789c09e29305c728bf3d7b94c5ef1c3e13eef1b321ee52d3ae3997731f56` |
| LNK from `03f1795d` archive | `9c7b507eba958ecee653ff42f13cf4e084f49cd38985d3abfd77ab2bfa40b4e2` |
| LNK from `ded13153` archive | `bbbeadae38bf1406f331c9e42ab49cbdd22f503cd9caecb6b390964bafa1b56f` |
| LNK from `b209f365` archive | `b80028534a414f199992a49610f8d5ffa94f8098d5a820653f68b8a9eb51e3ca` |
| LNK from current archive | `a44068e9758262a65861b91f2b00d0a3eca019d3b35543dd60c1c7f2e0ba1952` |
| Decoded stage two, `03f1795d` | `5e405ef279e7d33d375a7427361bce07936dd2258f02f3991441fb3e1c1cf2a2` |
| Decoded stage two, `ded13153` | `83c0b5f3db2e4ced741ee641a7a775fd949e769ed51ee8584229a862d268939e` |
| Decoded stage two, `b209f365` | `f5c729ce6f06d4c6f6d98cc1e23547c25f1b6207fdc347ed6cdbb60dad1203ae` |
| Decoded stage two, current archive | `70ee2f3ec1370960b225fd86cbe92a9477a788fc276567af2bd8c50e6744ae71` |

## Exact repository-file hashes

The repository review recorded SHA-256 values for two exact files in specific project variants: `.vscode/tasks.json`, `c935808147f0236c81483d7bbeda4b9d602f3595d5d4057f8115d39e222d1c4b`, and `.vscode/settings.json`, `35813f4401d3ad77b618275473a556eb47bfa6f4b7439dd8943b19f81aa7252e`. A match applies only to identical bytes. It is not a substitute for structural detection of modified tasks. [E10](/UNK_DeadDrop/evidence/E10.pdf) describes the ownership-reassessment limits; the original repository snapshots were not retained with that exhibit.

Hashes for the contact databases, message addresses, credentials, tokens, wallet files and image-provenance material are intentionally omitted. The public set is a selected technical reference, not a redistribution of the underlying evidence corpus.
