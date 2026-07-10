# schemas/ — record contracts (PROTECTED)

JSON Schema (Draft 2020-12) per record type, versioned via `$id`. A schema
violation blocks the write (HK6, `schema_validate.py`, step 2) — a violation is
a structural failure: halt, don't patch around it.

Slice set (step 1): work-order · handoff-envelope · research-packet ·
claim-ledger · memory-proposal · fact-record · source-record · decision-record ·
lesson-record · scorecard. Sources: Phase 3 §4, Phase 5 §6, Phase 2 §6.2,
Phase 6 §5–6.

**Tests:** `python scripts/test_schemas.py` — lints every schema, validates
`fixtures/<name>.yaml` `valid:` cases (spec examples verbatim where they exist),
and asserts every `invalid:` case is rejected. Green required before any writer
of a type exists.
