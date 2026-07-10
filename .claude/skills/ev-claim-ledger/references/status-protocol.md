# The seven statuses (SK-B2 adjudicate)

Categorical, never hedged (D8). Evidence requirements are structural:
`ledger_validate.py` rejects verified statuses without an evidence ref.

| Status | Criteria | Requires |
|---|---|---|
| `verified` | Evidence opened and read; statement matches it without stretch | evidence ref |
| `verified-with-qualification` | True as qualified; unqualified it misleads | evidence ref + qualification text |
| `unverified` | No adequate evidence available — including "the source is probably right" and dead cited URLs | — (never softened into confident prose) |
| `outdated` | Was true; superseding source exists or `review_by` passed | ref to what superseded it when known |
| `misleading` | Technically defensible, practically deceptive (cherry-picked window, missing base rate) | note on the deception mechanism |
| `incorrect` | Contradicted by controlling evidence | ref to the controlling source |
| `requires-professional-review` | Tax-law edge cases, securities questions, anything needing licensed interpretation | escalation (automatic trigger) |

Adjudication verifies the **evidence, not the citation**: open the source; a
tier-4 blog citing the IRS is not the IRS (source laundering). Between two
approved sources, later `effective` date controls (Phase 3 §7).
