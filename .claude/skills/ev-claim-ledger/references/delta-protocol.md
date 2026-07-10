# Delta protocol (SK-B2, D-006)

After voice_edit, only touched claims re-verify — full re-checks are the cost
the delta design removes; skipped re-checks are the risk it guards against.

1. VOICE runs `scripts/claim_diff.py <pre-voice> <post-voice>`.
2. Every hit maps to a CL-id + nature of touch (`edited`/`added`/`removed`).
   A hit VOICE believes is cosmetic still ships in the diff — suppression is
   prohibited; FACT owns that judgment.
3. Empty diff → T9 skips fact_delta (validator confirms emptiness from the
   script's output, not VOICE's word).
4. Non-empty → FACT delta mode: re-adjudicate ONLY the touched claims; append
   `delta-verified`/`qualified`/`incorrect` events to each claim's history;
   new claims introduced by editing get fresh CL-ids marked `declared_by: FOUND`.
5. Ledger records the pass: `{type: delta, by: FACT, trigger: "VOICE claim diff"}`.

The worked example: VOICE changed "you can" → "many Special Risk members can"
(CL-07). The quantifier is factual weight → flagged → FACT re-adjudicated to
verified-with-qualification with the do-not-state-a-single-age note.
