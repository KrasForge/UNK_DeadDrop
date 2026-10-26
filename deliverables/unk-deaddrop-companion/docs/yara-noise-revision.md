# YARA noise revision validation

Completed 26 October 2026 against libyara 4.5.4. Seven source rules were tightened after actual collisions with public research/tooling and our published exhibits, HTML and content cache. No payloads were executed or submitted.

**Every previous actual-artifact match is preserved across all 33 rules. The seven revised rules now have zero hits in the scanned research, dual-use tooling, ordinary software, installed software and upstream-fork controls.** All six Python test methods pass, including positive, near-miss and former marker-only-positive checks. Inert checks supplement the actual-artifact replay; they do not replace it.

| Revised rule file | Previous distinct actual matches | Revised matches | Change |
| --- | ---: | ---: | --- |
| `deaddrop_abe_bypass_source.yar` | 4 | 4 | Require the retained Python decrypt and key-loading signatures, including argument names. |
| `deaddrop_app_bound_credential_source.yar` | 2 | 2 | Require decrypt, key-loading and login-export definitions. Correct scope to standalone Python or Python embedded in JavaScript. |
| `deaddrop_clickfix_d2s_build.yar` | 1 | 1 | Require a clipboard API call followed within a bounded expression by design-challenge telemetry. |
| `deaddrop_clickfix_lure.yar` | 7 | 7 | Require a clipboard API call followed within a bounded expression by check/verify telemetry. |
| `deaddrop_electron_com_elevation_source.yar` | 4 | 4 | Require builder and runner definitions plus retained vtable dispatch and invoke syntax. Function headings alone still matched exhibit E19 and were insufficient. |
| `deaddrop_home_credential_sweep.yar` | 2 | 2 | Require credential matcher, budget and collection function definitions. |
| `deaddrop_windows_node_collector.yar` | 1 | 1 | Require both phase-one and phase-two archive-builder definitions. |

The replay still contains 177 case inputs, 380 views and 344 distinct case objects, with 76 matching objects. Case coverage and every prior control SHA-256/group pair were checked against the pre-revision manifests. The controls include published browser-decryption source and research, actual article HTML, evidence exhibits and Astro cache bytes; none was removed to obtain a clean result. Own rule/test-source self-matches are tracked separately and are not ordinary-software false positives.

## Submission implications

The original ten first-batch candidates remain the initial shortlist. The seven revisions are now optional, narrower source signatures rather than blocked on the observed collisions. Together with the sixteen previously optional signatures, that leaves ten first-batch and twenty-three optional rules. Removing observed noise does not remove overlap or make every rule equally useful for YARAify. In particular, D2S and home-sweep signatures add context to other detections, while the browser-recovery signatures remain implementation recognition rather than campaign attribution.

## Limits

Exact function names and argument syntax can be changed; the ClickFix patterns intentionally target the retained minified syntax. These changes preserve the observed files, not unknown variants. Text signatures do not parse programs: a document quoting enough of the complete implementation can still match. Public security tooling controls are dual-use, not uniformly benign. No operational false-positive rate is claimed.

The original Overlord repository and VS Code samples downloads were unavailable in this run; no unrelated compiled Overlord baseline was added. Four RAR archives were recognized without decoding members. Local recursive ZIP/TAR/gzip handling is not a guarantee of equivalent extraction on YARAify. Rule licenses, metadata and platform-engine compatibility still need review before deployment.

## Reproduction and evidence

The investigation's `deliverables/publishing-drafts/yaraify-review/` directory retains `before-revision/`, current `results.json` and `corpus-manifest.json`, plus `review.py` and `check_revision.py`. Run the replay with the companion Python environment, then run `check_revision.py` to assert preserved coverage, retained control hashes and zero observed control hits for the seven revisions. Rule SHA-256 values are recorded in the replay results. No case source or downloaded third-party code is bundled in this companion repository.
