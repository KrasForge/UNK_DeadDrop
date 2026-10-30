---
title: "How a Malicious VSIX Uses the Signed Editor Runtime"
description: "How a fake Google Update Support extension installs collection components and turns the editor's own Electron binary into a Node interpreter on Windows."
date: "2026-10-25"
author: "Ilja Krasnjanski"
canonical: "https://krasforge.github.io/UNK_DeadDrop/articles/02-vsix-editor-execution/"
kicker: "UNK_DeadDrop · Part 2"
tags:
  - "UNK_DeadDrop"
  - "VS Code"
  - "VSIX"
  - "Electron"
  - "Windows"
og_image_alt: "Diagram of the repository, extension and Windows interpreter stages"
---


The extension calls itself **Google Update Support** and claims to secure and update the development environment. Inside the 17.6 MB package are native agents for macOS and Linux, encrypted Windows components, and code that selects deployment settings. On Windows, one path uses the editor's Electron executable to interpret attacker-controlled JavaScript. The environment variable `ELECTRON_RUN_AS_NODE=1` enables that mode.

This is the repository-based branch: a project task leads to the extension installer, which supplies the collection pipeline. Part 1's clipboard lure is a separate entry point. Related Windows elevation code appears in both branches.

The July repository review identified five weaponised copies:

- `github[.]com/Lyracartoon/predict-together`
- `github[.]com/pridnet/dscufo-assessment-fe`
- `gitlab[.]com/pulsynk/rekt-db`
- `gitlab[.]com/stefan[.]kano/forge-4626-invariants`
- `gitlab[.]com/predicttogether/forge-4626-invariants`

A sixth copy, `gitlab[.]com/lautaro19/rekt-db`, contained matching payload markers. The evidence supports likely operator control, not confirmed ownership. GitLab reportedly removed `pulsynk-org/rekt-db`; `pulsynk/rekt-db` is a different repository.

The [historical indicator reference](historical-indicators.md) records the dated observations, and the [artifact reference](artifact-reference.md) lists hashes for selected task and settings files. Current availability has not been checked.

[Proofpoint's UNK_DeadDrop analysis](https://www.proofpoint.com/us/blog/threat-insight/dont-fear-repo-unkdeaddrop-phishing-campaign-targets-developers-steal) documents the VSIX route and Windows architecture also present in this package. Jamf Threat Labs has separately documented [threat actors abusing Visual Studio Code](https://www.jamf.com/blog/threat-actors-expand-abuse-of-visual-studio-code/), and the editor's own [task documentation](https://code.visualstudio.com/docs/debugtest/tasks) and Electron's [environment-variable reference](https://www.electronjs.org/docs/latest/api/environment-variables) describe the two legitimate features this chain repurposes.

## A `folderOpen` task points to the installer

The repository task uses `runOn: folderOpen` and points into an ordinary-looking project directory. Workspace trust and task permissions still apply, so its presence does not mean every editor runs it automatically.

After installation, the extension is no longer confined to the project. It declares startup activation, while surrounding scripts clean up the task and staging files. Deleting the clone therefore does not establish that the extension or anything it launched has been removed.

![How the editor becomes an interpreter](assets/02-vsix.png)

*Figure 1. The repository installs an extension whose Windows branch invokes the editor's Electron runtime in Node mode.*

The extension manifest contains these fields:

```json
{
  "name": "google-update-support",
  "displayName": "Google Update Support",
  "publisher": "google-dev-tools",
  "version": "1.0.0",
  "main": "./extension.js",
  "activationEvents": ["onStartupFinished"]
}
```

The installed identifier is `google-dev-tools.google-update-support`. These names are part of the masquerade; they establish neither Google authorship nor a trusted signature. The VSIX collected on 22 July 2026 is 17,647,582 bytes. [Exhibit E03](../preprint/evidence/E03.pdf) records the package, nested archive and native-agent hashes:

```text
SHA-256
52886aab179f26421678ff23af1b0fabf0a17ffbb534369cdbbac8008cbed8e7
```

The `onStartupFinished` declaration gives the extension an opportunity to activate after the original workspace is gone. It does not prove that every payload runs on every startup or platform.

The extension exposes its settings under the `googleUpdateSupport` namespace:

```text
googleUpdateSupport.agentZipRelativePath
googleUpdateSupport.windowsActivationMode
googleUpdateSupport.companyWalletServerUrl
googleUpdateSupport.companyWalletClientId
googleUpdateSupport.companyWalletAgentToken
```

The deployment reads server and client values from configuration, so the same VSIX can be reused with different workspace settings. Preserve the package and project configuration together: a VSIX hash identifies the archive but may not reveal where a particular installation was configured to send data.

The nested agent archive contains Go binaries for macOS arm64, macOS amd64 and Linux amd64. Their hashes match samples identified in the case's comparison with prior reporting. The Windows branch does not depend on dropping those binaries. The encrypted Windows modules and their recovered hashes are documented in [E04](../preprint/evidence/E04.pdf).

## Three encrypted scripts inside the VSIX

Static deobfuscation recovered three readable components from the package:

- `windows-js-pipeline.js` coordinates collection, elevation, upload and cleanup.
- `windows-agent-node.js` implements the JavaScript collection agent.
- `detect_malware.py` handles browser-related key and credential decryption.

The Node source describes a Windows route that does not depend on a Go executable. A detector limited to native-agent hashes would miss this path. The Python component contains DPAPI and browser elevation-service logic, including App-Bound Encryption handling. The coordinator attempts to obtain the privileges and execution context this stage needs. The [Acorn analysis](03-acorn-deobfuscation.md) describes their recovery through static deobfuscation and authenticated decryption.

The recovered builder constructs a PowerShell script that requests an elevated COM object associated with CMSTPLUA and the ICMLuaUtil interface. The identifiers are assembled from numeric fields, so searching for a literal GUID is less useful than tracing how the script builds and calls them. It then creates a delegate at runtime to dispatch the shell-execution method.

Similar builder code appears in the ClickFix stage-three script, linking the implementations across the two delivery routes. [E19](../preprint/evidence/E19.pdf) records the relevant source spans.

The failure paths show that elevation may not succeed. The VSIX pipeline can fall back to RunAs, which may display a consent prompt. ClickFix retries and uses a sentinel to check for completion. Success depends on Windows version, user privileges, policy and process context. These paths were analyzed statically; their runtime outcomes were not reproduced.

### The extension launches the editor binary as Node

The source sets `ELECTRON_RUN_AS_NODE` and invokes the editor executable with an agent-script path. `process.execPath` supplies the executable location from inside the extension. The code uses the editor binary as a Node interpreter for collection code supplied by the chain, rather than its normal startup code. MITRE ATT&CK tracks this behavior as [Electron Applications (T1218.015)](https://attack.mitre.org/techniques/T1218/015/).

A process name or publisher check is incomplete here. A legitimate signature authenticates the editor executable, not every script passed to it. On an endpoint, investigate the transition: the editor launching an elevation helper, then an unexpectedly elevated interpreter with a collection-script argument, then access to browser or wallet data. Decryption remains a separate condition; elevation alone does not prove that a password was recovered.

## Recruitment email in the clean repository

The weaponised `predict-together` copy has a clean twin. An email template stored beside the clean version shows that the operators also addressed designers, project managers, founders and builders. It invites them to review an open-source market-analysis platform in Cursor.

The template describes four steps, taking "about 30 minutes":

1. Clone the repository.
2. Open it in Cursor and analyze it with AI.
3. Write a few prompts.
4. Send the prompts back.

The message says, "No coding needed," and offers payment, a Cursor Ultra license or a place on the team for useful feedback. Its repository link is a placeholder, so the template does not show which copy any particular recipient received.

The public repository is a working FastAPI and React application, with seeded demo users and green test and coverage badges. A static review of its full tree, including dot-directories, found no code that would run on its own.

The review found no `.vscode/tasks.json`, `.cursor/` rules, `mcp.json`, `.devcontainer/` hooks or workflows. The Python and npm dependencies came from ordinary package registries and had no install scripts. The documentation showed standard install, test and run commands.

The repository's `.gitignore` also excludes `.vscode/`. The copy with the folder-open task belongs to a different account. The template presents the clean repository for inspection, while the weaponised copy is a separate artifact.

The email targets people who are not being asked to write code. A developer doing a coding exercise may inspect the project and notice an unusual task or install hook. Someone told that no coding is needed may instead open the repository in an AI editor and let its agent act without reading the project. The retained weaponised copy used a folder-open task.

Other editor-based routes are possible, including devcontainer hooks, workspace rules or instructions, an MCP server supplied by the workspace, and a dependency that runs when the agent is asked to start the project. None of those appeared in the copies reviewed here.

The review covered the public repository and the retained weaponised copy, not a message received by a target. The exact repository and configuration sent to any individual therefore remain unknown. The public reports cited in this series describe developer-directed assessments; they do not describe this non-coder invitation.

Before opening an unsolicited project in an AI editor:

- Use a disposable machine.
- Turn off automatic task execution and agent auto-run.
- Disable workspace-supplied MCP configuration.
- Keep wallet keys, SSH keys, browser profiles and `.env` secrets off it.

## Inspect the extension path and process arguments

Repository-only review can miss the installed extension; a hunt limited to native binaries can miss the JavaScript Windows branch. Preserve task definitions, editor and agent configuration directories, workspace settings, extension metadata, script arguments, process ancestry and any resulting persistence. The extension identifier and package hash provide exact selectors. The editor-to-interpreter transition gives responders a behavior to investigate when names or builds change.

The companion repository has a [YARA rule for the recovered VSIX manifest](https://github.com/KrasForge/unk-deaddrop-companion/blob/main/rules/yara/deaddrop_vsix_manifest.yar). It must scan extracted archive members.

The companion scanner covers JavaScript. Its `electron-run-as-node` rule reports the recovered pipeline at error level because that file writes a PowerShell script, sets `$env:ELECTRON_RUN_AS_NODE` and launches it with a hidden window. The scanner also reports the extension's obfuscated string array as recovered.

Setting the variable alone is not enough to raise an error. In a benchmark of 3,000 popular packages and extensions, TypeScript's language server, SSH proxy shims and local helper servers launched the editor binary as Node in sixteen places. None hid the launch.

The repository has no process or file-event rules because authentic endpoint logs were not retained for replay. A manifest match does not establish execution, elevation or collection.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
