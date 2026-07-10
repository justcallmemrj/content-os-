# DEC-BUILD-003 — Dependency: Python `jsonschema` (+ `pyyaml` already present)

| | |
|---|---|
| Status | INSTALLED at step 1; presented for ratification at the step-1 gate |
| Type | Runtime dependency memo (master prompt never-list: no dependency without a memo) |

**What:** `jsonschema` (MIT license, the reference Python implementation of JSON Schema), installed via pip, version pinned in `requirements.txt` at the exact installed version. `pyyaml` 6.0.3 was already present on the machine; recorded and pinned alongside.

**Why:** Phase 3 §5.2/D-021 mandates "JSON Schema contracts... hooks enforce on write"; `schema_validate.py` (HK6, step 2) and the step-1 schema fixture tests need a validator. Python stdlib has none. Writing a bespoke validator would be redesign and a correctness risk in the exact component whose job is correctness.

**Alternatives considered:** (a) bespoke validator — rejected (above); (b) Node `ajv` — rejected: every enforcement script in Phase 7 §5 is Python; splitting the toolchain for one library buys nothing.

**Cost/licensing:** free, MIT. No service surface, no telemetry, no credentials.

**Rationale for install-before-gate:** the never-list requires the memo, not a halt; there is no cost/licensing implication (§6 escalation test), and step 1's exit criteria ("schemas lint") are unreachable without it. Flagged here for explicit ratification; trivially reversible (`pip uninstall`).
