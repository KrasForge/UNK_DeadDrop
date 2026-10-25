---
title: "Building and Testing Detections for UNK_DeadDrop"
description: "Three experimental rules, their actual match conditions, and inert tests that expose useful blind spots."
lastUpdated: 2026-10-25
sidebar:
  order: 11
---


What does a match actually tell an analyst? The companion contains one YARA rule combining framework and wallet markers, plus Sigma rules for a Linux service path and a Windows scheduled-task command. A match can identify bytes or an event that meets those conditions. It does not show that a file executed, a task succeeded or a particular group was responsible.

This article walks through the rules and their test fixtures, including three boundary cases: harmless prose that matches YARA, a longer task name that matches the Windows selector, and mixed-case input accepted by the local Linux fixture evaluator. These cases reveal selector behavior; they are not malware execution or production detection measurements.

> **Key Takeaways**
>
> - Framework identity alone is deliberately insufficient for the wallet-agent YARA rule.
> - The YARA conjunction can match research text containing its strings; acquisition context matters.
> - The Windows rule uses substring matching for the task marker, not parsed task-name equality.
> - Sigma schema parsing and fixture evaluation do not validate SIEM ingestion, conversion or alert delivery.

## Match the rule to its telemetry

The three rules operate on different inputs. YARA scans file content. The Linux Sigma rule expects file-event telemetry with a target path. The Windows Sigma rule expects process-creation telemetry with an image path and command line. A detection can only evaluate the fields it receives, so a missing command line or an uncollected user-service directory creates a gap before the rule logic is considered.

The rule set was authored for the companion in October 2026. Performance figures attached to earlier rules in the original case do not transfer to these revisions. Assessment starts with the exact selectors and the test cases that accompany them.

### The wallet-agent conjunction

The YARA rule requires a file smaller than 64 MiB, a framework module marker, an environment marker and at least two of three wallet markers. Its operative section is:

```text
strings:
    $framework = "overlord-client/cmd/agent" ascii wide
    $env = "OVERLORD_SERVER_RAW" ascii wide
    $wallet1 = "OVERLORD_COMPANY_WALLET_EP" ascii wide
    $wallet2 = "X-Company-Wallet-Client-Id" ascii wide
    $wallet3 = "/api/company-wallet/upload" ascii wide
condition:
    filesize < 64MB and $framework and $env and 2 of ($wallet*)
```

This is an excerpt, not a complete rule file. The conjunction is narrower than a framework-only match because it requires collection-related context as well. The `ascii wide` modifiers accommodate ordinary byte strings and their zero-interleaved wide form; they do not decrypt a packed or encrypted payload. The [YARA rule documentation](https://yara.readthedocs.io/en/stable/writingrules.html) describes those modifiers and condition syntax.

The original tests compile the real rule and supply inert buffers. They check positive ASCII and wide cases, then remove enough context to produce framework-only, wallet-only and partial-marker negatives. A historical static spot check also matched the held Go implant. Neither exercise measures how many unrelated files in a developer fleet would match.

### A harmless document can satisfy the rule

The additional fixture contains research prose followed by the required framework, environment and two wallet strings. It has no executable instructions. It still matches, because the rule asks whether those bytes occur, not whether the containing file is an executable or whether its contents are reachable code.

The paired negative replaces the required environment marker with a different label. That buffer no longer matches. Together the fixtures demonstrate both the usefulness and the fragility of the conjunction: it excludes incomplete marker sets, but it can include documentation and miss a renamed implementation.

A match in a malware-analysis archive should therefore be interpreted differently from a match on an unexpected installed agent. Adding an executable-format condition would be a possible design change, but would need its own scope decision and tests. This article leaves the existing rule unchanged and documents its actual behaviour.

### Linux: a path event is not service execution

The Linux rule selects either the exact system unit path `/etc/systemd/system/google-agent.service` or a target ending in `/.config/systemd/user/google-agent.service`. The logical condition is an OR between those two selections.

The existing fixtures cover both paths, a similarly named nonmatching unit and a missing field. They establish that the small local evaluator handles the selectors as intended. The new test also shows that this evaluator folds case: an uppercase unit name in the field is accepted. That is a property of the matching implementation, not a claim that Linux filesystem paths are interchangeable across case.

A service file event does not establish that the service was enabled, started or successfully ran the collector. Investigators still need the unit contents and supporting process or service activity. A renamed unit escapes this exact selector, while a security exercise using the recorded name can produce a legitimate match.

### Windows: read the modifiers literally

The Windows selector is:

```yaml
selection:
  Image|endswith: '\schtasks.exe'
  CommandLine|contains|all:
    - '/create'
    - 'GoogleUpdateSupporterNode'
condition: selection
```

Both command-line substrings must occur, and the image must have the required suffix. The [Sigma modifier documentation](https://sigmahq.io/docs/basics/modifiers.html) explains how `all` combines the listed values and how `contains` and `endswith` constrain the match.

The rule does not parse `/TN` and compare its argument for equality. The additional fixture uses `GoogleUpdateSupporterNode-Lab`, which still contains the required marker and therefore matches in the local evaluator. The existing negative tests reject a query command and a different executable; the new missing-command-line fixture is also rejected.

This distinction is useful when triaging a hit. Inspect the complete command and actual task definition rather than describing the alert as proof of one exact task. Registration through another API, a renamed task or missing telemetry can bypass the selector entirely. The rule itself already documents the API-registration gap.

## What was tested locally

The original detection suite has four tests: real YARA compilation and marker fixtures, Sigma schema parsing, Linux field fixtures and Windows field fixtures. The three added boundary tests bring this run to seven detection tests. The companion's separate eight AST tests also pass. All fixtures are inert; no service was installed, task registered or malware launched.

| Check | What it establishes | What it does not establish |
|---|---|---|
| YARA compilation and buffers | Syntax and selected marker combinations | Malware precision or recall |
| Harmless-text match | Content can match outside executable code | Frequency of that false positive in a fleet |
| Sigma parsing | Rules accepted by the installed parser | Backend query correctness |
| Field fixtures | Behaviour of the local modifier subset | Real event collection or end-to-end alerts |
| AST tests | Supported parser-tool behaviour | Automatic recovery of the encrypted loader |

The local Sigma evaluator is deliberately small; it is not a SIEM backend. Case handling, field mapping and event normalization still need validation in the intended platform. These tests check the implementation reproducibly, but they are not deployment sign-off.

### Reproduce the inert detection checks

The download bundle includes the [original detection tests](../../companion/tests/test_detections.py), [three boundary tests](../../companion/tests/test_blog_boundaries.py), [pinned Python requirements](../../companion/requirements-dev.txt), [YARA rule](../../companion/rules/yara/deaddrop_wallet_agent.yar), [Linux rule](../../companion/rules/sigma/linux_google_agent_persistence.yml) and [Windows rule](../../companion/rules/sigma/windows_capture_task.yml). Run from the extracted bundle root:

```sh
python -m venv .venv
.venv/bin/pip install -r public-repository/requirements-dev.txt
.venv/bin/python -m unittest discover -s public-repository/tests -v
```

Those commands run the seven detection tests. The separate AST tests require the full companion project and are not included in this small detection bundle. Code and rules retain the companion's [MIT license](../../companion/LICENSE); that grant does not cover the research prose or underlying evidence.

### From a selector to an investigation

For a YARA hit, retain the file identity, acquisition context and matching offsets. For a Linux unit, inspect the unit definition and associated process activity. For a Windows task, recover the full command line, task action and relevant ancestry. Those follow-ups help separate a research artifact or simulation from an unexpected deployment.

The next step is conversion and replay against representative telemetry from the intended environment, including clean developer workloads. That evaluation has not been performed, so the rules remain experimental. The present fixtures make its open questions visible instead of hiding them behind a passing test count.
