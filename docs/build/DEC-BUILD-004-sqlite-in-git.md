# DEC-BUILD-004 — workflow.sqlite: DDL versioned, binary ignored

| | |
|---|---|
| Status | RATIFIED by Wes 2026-07-10 ("Yes" to the step-1 gate proposal) |
| Type | Build decision on a spec-silent point |

**Decision:** `state/ddl.sql` (Phase 7 §4 verbatim) is committed and versioned;
the live `state/workflow.sqlite` and `state/checkpoints/` are gitignored. The
binary's durability comes from the Phase 7 §8 backup legs (weekly `git bundle`
+ SQLite + archive snapshot; monthly offsite), not from git history.

**Reason:** a churning binary in git history costs repo bloat and merge pain
and buys nothing the backup legs don't already provide; the *contract* (DDL) is
what needs versioning. The audit spine remains queryable locally and is
snapshotted by HK9 at every compaction.

**Alternatives considered:** commit the binary (rejected: churn, no diffability);
LFS-track it (rejected: same churn, plus hosted-LFS quota pressure the archive
policy exists to avoid).
