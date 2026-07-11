# FACT findings — run 2026-07-10-ben-carous-001 — full adjudication

Deliverables: `drafts/drop-carousel-v1.md` (8 slides, on-image) + `drafts/caption.md`.
Ledger: `factcheck/ledger.yaml` v1 (full pass, 2026-07-10T19:55:00-04:00).
Attached pre-checked source: `runs/2026-07-10-ben-drop-001/voice/drop-reel-v3.md`
with its ledger v2 (blocking summary CLEAR). Independent extraction run on both
files (`extract_claims.py`: 5 candidates carousel, 3 caption — all 8 map to
declared claims; no extraction miss).

**Verdict: CLEAR** — `high_risk_non_verified: 0` (recomputed by
`ledger_validate.py`, VALID, 0 violations). Findings below are non-blocking;
per D4 they are flagged, not fixed.

## F1 — Declared claim-id scheme violates the ledger schema (process, non-blocking)

WRITE's `drafts/claim-list.yaml` uses ids `CC-01..CC-16` / `CP-01..CP-11`. The
claim-ledger schema requires `^CL-\d{2,}$`. The ledger normalizes to
`CL-01..CL-16` (= CC) and `CL-17..CL-27` (= CP), with the original id recorded
in each claim's `declared` history event. No content changed. Suggest WRITE use
CL-ids in declare mode going forward so declared and adjudicated ids coincide.

## F2 — Qualified parent claim adapted twice; qualification carried, not discharged (CL-13, CL-23)

Slide 7's "Choose the rollover, and the timing becomes yours." (CL-13) and the
caption's "…— the timing becomes yours." (CL-23) both adapt drop-001/CL-11,
which is **verified-with-qualification** (evidence supports
deferral-until-withdrawal, not unconditional control of timing; distribution
rules still govern). WRITE's placement argument (immediately after the deferral
mechanics; conditional "Choose the rollover") is accepted as *honoring* the
qualification. It does not *discharge* it: both entries are adjudicated
verified-with-qualification with the parent's qualification text carried
forward. No text change required; the limit stays auditable for COMPL/QA.

## F3 — FOUND: implied comparative tax claim across Slides 5–7 (CL-28, verified)

The declared list covers each route's mechanics separately; the slide sequence
additionally asserts the *comparison* — cash taxed in the payout year vs
rollover deferred. Ledgered as CL-28 (`declared_by: FOUND`, high risk) and
**verified**: F-BEN-0010 is itself comparative ("…whereas a properly executed
direct rollover defers taxation until later withdrawal"). Slide 6's "still
tax-deferred" keeps the deferred-not-tax-free framing; no outcome/performance
language (F-BEN-0007 usage-note hard line respected).

## F4 — Trimmed slide claim strictly narrower than source (CL-08, verified)

Slide 5 drops the "stacked on everything else you earn" clause of
drop-001/CL-07 for slide budget. The trim removes a consequence, adds nothing —
strictly narrower, still fully supported by F-BEN-0010. The caption (CL-22)
carries the full clause, so the pair is coherent.

## F5 — On-image ↔ caption consistency: no contradictions

Checked slide-by-slide against the caption. The caption is a superset of the
slides: it adds the termination rule ("You must leave FRS-covered work…",
CL-19, verified per F-BEN-0003) and the stacking clause (CL-22) that the slides
omit. Nothing on-image asserts anything the caption contradicts, and vice
versa. Note for QA (not a FACT blocker): the slides alone never state the
termination requirement — a viewer who reads images only gets the fork without
the leave-work precondition. Nothing on the slides becomes untrue or misleading
by the omission (each slide claim was verified standalone), but QA may weigh
whether the carousel format should carry F-BEN-0003's hard rule on-image.

## F6 — Disclosures byte-verified; publish-gate conditions

- Slide 8 final line (CL-16): DISC-BEN-SHORT-01 + DISC-BEN-TAX-01 byte-verbatim
  against `disclosures.md@1.0.0`; "Full disclosures in profile." satisfies the
  short-format say-where-it-lives condition. verified-with-qualification.
- Caption (CL-26, CL-27): TAX-01 verified; SHORT-01 + profile pointer
  verified-with-qualification.
- **Publish-gate conditions for the producer checklist** (none verifiable from
  the drafts): (1) webinar live and free (CL-14/CL-24); (2) registration link
  actually in profile (CL-15/CL-25); (3) DISC-BEN-FRS-01 with the TAX-01 rider
  actually placed in the profile at publish (CL-16/CL-27).

## Status counts (28 claims)

| status | count | ids |
|---|---|---|
| verified | 18 | CL-01, 02, 05, 06, 07, 08, 09, 10, 11, 12, 17, 18, 19, 20, 21, 22, 26, 28 (FOUND) |
| verified-with-qualification | 4 | CL-13, CL-16, CL-23, CL-27 |
| unverified | 6 | CL-03, CL-04, CL-14, CL-15, CL-24, CL-25 (all low-risk texture/operational) |

High-risk: 13, all verified or verified-with-qualification. FOUND: 1 (CL-28).
