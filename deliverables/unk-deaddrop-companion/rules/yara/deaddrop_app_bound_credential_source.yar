rule UNK_DeadDrop_App_Bound_Credential_Source_Experimental
{
    meta:
        description = "Retained Python credential-recovery implementation, standalone or embedded in JavaScript"
        author = "UNK_DeadDrop research contributors"
        date = "2026-10-26"
        evidence_cutoff = "2026-07-24"
        reference = "https://krasforge.github.io/UNK_DeadDrop/articles/04-credential-wallet-collection/"
        source_note = "docs/detection-notes.md"
        status = "experimental"
        revision = "2026-10-26 implementation-context noise revision"
        scope = "plaintext or decoded source; does not establish successful credential recovery"
    strings:
        $login_data = "Login Data" ascii
        $local_state = "Local State" ascii
        $app_bound_key = "app_bound_encrypted_key" ascii
        $recovery_dpapi = "DPAPI" ascii nocase
        $recovery_app_bound = "App-Bound Encryption" ascii nocase
        $recovery_elevation = "Elevation Service" ascii nocase
        $recovery_aes_gcm = "AES-GCM" ascii nocase
        // Retained implementation syntax, not just markers quoted in research.
        $impl_decrypt = /def decrypt_app_bound_key\(cipher_after_appb[,:]/ ascii
        $impl_load = /def load_master_key\(data[,:]/ ascii
        $impl_export = "def export_logins(" ascii
    condition:
        all of ($impl_*) and
        filesize < 1MB and $login_data and $local_state and $app_bound_key and
        2 of ($recovery_*)
}
