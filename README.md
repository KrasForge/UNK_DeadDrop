# UNK_DeadDrop

An artifact-based investigation of developer-targeting phishing, collection tooling, infrastructure and defensive detections. The case evidence ends on 24 July 2026. Later public reporting is assessed separately, and the articles distinguish static capability from observed execution.

Read the [twelve-part research series](https://krasforge.github.io/UNK_DeadDrop/), the [Zenodo preprint record, version 1.0](https://doi.org/10.5281/zenodo.23652298), or the [companion detection repository](https://github.com/KrasForge/unk-deaddrop-companion). The latest-version DOI is [10.5281/zenodo.23652297](https://doi.org/10.5281/zenodo.23652297).

The companion repository supports defensive review with a parse-only AST scanner, experimental Sigma and YARA rules, and inert fixtures. It contains no live malware payloads or active credentials. Similarities to tradecraft reported under Contagious Interview and MITRE ATT&CK G1052 do not establish common operator identity.

The site source and local preview instructions are in [`site/`](site/README.md). The Pages workflow builds the site from the article sources, paper, public evidence reports and selected companion files.
