rule UNK_DeadDrop_Phase3_Home_Credential_Sweep_Experimental
{
    meta:
        description = "JavaScript stage-three source with bounded whole-home credential filename search"
        author = "UNK_DeadDrop research contributors"
        date = "2026-10-26"
        evidence_cutoff = "2026-07-24"
        reference = "https://krasforge.github.io/UNK_DeadDrop/articles/04-credential-wallet-collection/"
        source_note = "docs/coverage-map.md"
        status = "experimental"
        revision = "2026-10-26 implementation-context noise revision"
        scope = "plaintext or decoded JavaScript; source markers do not establish collection or upload"
    strings:
        $regex = "CREDENTIAL_NAME_RE" ascii
        $phase3 = "phase3" ascii
        $budget1 = "DEFAULT_PHASE3_MAX_MS" ascii
        $budget2 = "DEFAULT_PHASE3_ROOT_MAX_MS" ascii
        $budget3 = "DEFAULT_WALK_MAX_DIRS" ascii
        $tcc = "macTccReadableCache" ascii
        $cloud = "CloudStorage" ascii
        $upload = "GUS_UPLOAD_CHUNK_SIZE" ascii
        $placeholder = "%%GUS_EMBED" ascii
        // Retained implementation syntax, not just markers quoted in research.
        $impl_match = /function matchesCredentialNamedSecretFile\(name\) *\{/ ascii
        $impl_budget = /function createPhase3Budget\(opts\) *\{/ ascii
        $impl_collect = /function collectPhase3DevHarvest(Async)?\(opts\) *\{/ ascii
    condition:
        all of ($impl_*) and
        filesize < 8MB and $regex and $phase3 and 2 of ($budget*) and
        2 of ($tcc, $cloud, $upload, $placeholder)
}
