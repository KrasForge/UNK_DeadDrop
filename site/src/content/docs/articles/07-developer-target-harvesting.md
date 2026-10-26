---
title: "From Commit Metadata to a Developer Target List"
description: "Reconstructing the harvester, sender configuration and aggregate counts behind two SQLite targeting pools."
lastUpdated: 2026-10-25
sidebar:
  order: 7
---


The sender configuration pointed to two SQLite databases. Following those references led to harvesting code and pools containing 79,698 and 62,667 rows. Together they contain 142,365 distinct stored address strings associated with 27,698 repository values. The harvesting code collected those addresses from public commit metadata for use by the sender tooling.

## Following the database references

The harvester searches repositories by star range, walks their branches and extracts author and committer addresses. It lowercases and trims them before filtering, and visits up to twenty branches per repository in the recorded implementation. Worker configurations partition the search; scheduler and merge code consolidate results into two master pools. MITRE ATT&CK classifies this reconnaissance as [gathering victim email addresses (T1589.002)](https://attack.mitre.org/techniques/T1589/002/). The SQLite relation is simple:

```text
emails
  email: stored address
  repo: associated repository value
```

The sender configuration refers to both pools. Different intervals, cooldowns and warm-up settings control how the tools consume them. The toolkit names the two pools `safe` and `antispam`.

The database references connect harvesting to message preparation. No send logs were recovered to establish which addresses received messages.

![Two pools, two different counting problems](../assets/07-targeting.png)

*Figure 1. The address sets are disjoint, while repository values overlap between the two pools.*

### Counting the two pools

The two databases share some repository values. A SQL union counts each value once across both pools. Read-only aggregate queries on 23 October found:

- 79,698 rows in the safe pool;
- 62,667 rows in the antispam pool;
- an exact address overlap of zero between them;
- 142,365 distinct address strings across both;
- 27,698 distinct repository values across both.

The queries check address overlap and count the combined repository values:

```sql
-- Address overlap
SELECT count(*)
FROM main.emails AS s
JOIN other.emails AS a ON s.email = a.email;

-- Combined repository values
SELECT count(*) FROM (
  SELECT repo FROM main.emails
  UNION
  SELECT repo FROM other.emails
);
```

In this comparison, the stored address sets are disjoint but the repository sets overlap. Adding the two repository counts would therefore overcount.

The queries compare stored strings without additional address canonicalization or identity resolution. Aliases and multiple addresses belonging to one person remain separate entries.

The sender code configures `mail.privateemail.com` through variables carrying a `ZOHO` prefix. A recovered guide also provides Private Email DNS examples, while later received-message headers contain Mailgun-related information.

The records describe more than one mail route over time. The guide also discusses a shared outbound relay, whose other tenants are outside the scope of the observed campaign traffic.

## Delivery volume remains unknown

The code and configuration connect harvesting to message preparation. The databases quantify the stored contact material. Neither supplies the missing send logs, delivery outcomes or endpoint evidence needed to count people contacted or compromised. Even the repository total describes stored values rather than a fresh verification of repository existence or ownership.

The [administration frontend](../08-administration-platform/) contains mail and wallet views, but its connection to these particular SQLite pools remains unverified.

[Companion detections and static scanner](https://github.com/KrasForge/unk-deaddrop-companion).
