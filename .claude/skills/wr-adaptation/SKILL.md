---
name: wr-adaptation
description: "Platform adaptation and repurposing for WRITE (D-047): child runs referencing an APPROVED parent, entering the trunk at draft. Unchanged claims inherit the parent's ledger statuses hash-verified (scripts/inherit_ledger.py); changed/new claims adjudicate fresh; claim-diff emission is MANDATORY. Voice, compliance, QA, and H2 all still run."
skill_id: SK-B5
version: 1.0.0
tier: B
owner: wes
approval_status: draft          # activates with step 7
supported_agents: [WRITE]
required_inputs: [work_order_with_parent_run_and_parent_artifact_hash, parent_deliverable, parent_ledger, target_format]
optional_inputs: [platform_notes, approved_exemplars]
prerequisites: ["parent run APPROVED (locked hash recorded at its T15)", "SK-B4 for the target format's canon"]
requires: [SK-B2, SK-A2, SK-B4]
reads: ["parent run's voice/<deliverable> + factcheck/ledger.yaml", "projects/<active>/brand-voice.md (register)"]
schemas: [work-order, claim-ledger]
evaluation_rubric: RUB-SOCIAL-1
---

# wr-adaptation (SK-B5)

## The rule that makes repurposing cheap without becoming unverified

An adaptation is a **child run**: `parent_run` + `parent_artifact_hash` on the
work order. Facts the parent already proved stay proved — IF they are provably
the same facts:

1. Draft the target format (SK-B4 canon) from the parent deliverable. Reuse
   the parent's factual sentences byte-identically wherever the format allows —
   byte-identity is what buys inheritance.
2. Run `scripts/inherit_ledger.py --parent-run <id> --parent-artifact <path>
   --parent-artifact-hash <sha256> --child-draft <path> --out <child-ledger>`:
   - verifies the parent artifact still matches its LOCKED hash (tamper = refuse);
   - claims whose text appears byte-identical in the child draft INHERIT
     status + history, with an `inherited` event appended;
   - claims whose text changed or is new are emitted as `unverified` with
     `declared_by: WRITE`, awaiting FACT's fresh adjudication (delta scope);
   - blocking summary recomputed.
3. FACT's fact_check runs in DELTA SCOPE: it adjudicates only the fresh
   entries (and spot-audits inheritance).
4. Voice, compliance, QA, H2 all still run in full — a LinkedIn version is a
   new external-facing artifact, not a formality.

## Prohibited behavior

Adapting from an unapproved parent; paraphrasing a factual sentence and
keeping its inherited status (the byte rule exists precisely so this fails
mechanically); skipping the claim diff; treating H2 as inherited (it never is).

## Tests

`scripts/test_step7_skills.py`: the delta-inheritance fixture — child draft
embedding two parent claims byte-identical + one changed: 2 inherit with
history events, 1 fresh-unverified; tampered parent hash → REFUSED.
