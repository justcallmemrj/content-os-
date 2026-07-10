# Voice pass change log — drop-reel-v2.md -> voice/drop-reel-v3.md

Run 2026-07-10-ben-drop-001 · VOICE · SK-B9 · profile brand-voice.md@1.0.0 ·
register scored against VX-BEN-0001..0005 (VX-BEN-0004 is the spoken-teaching
target for reel beats). Every change below is one line; the per-claim
accounting lives in voice/claim-diff.yaml.

## Changes

1. STAKES — "The rule is hard: you must leave…" -> "The rule is hard. You must leave…" — full stop gives the speaker a marked breath point before the hard rule (pause-after-claim cadence); words unchanged; touches CL-04 (listed in claim diff).
2. BEAT ONE — "Half of that is right: your monthly pension…" -> "Half of that is right. Your monthly pension…" — the verified claim now stands as its own spoken sentence with a beat before it; words unchanged; touches CL-05 (listed in claim diff).
3. BEAT TWO — "Here's the part that rarely comes up: cash gets taxed…" -> "…rarely comes up. Cash gets taxed…" — pause after the transition sets up the tax claim; also drops the longest spoken unit from 21 to 14 words; words unchanged; touches CL-07 (listed in claim diff).
4. Title/provenance lines — v2 -> v3, revises-field now points at drafts/drop-reel-v2.md per SK-B9 — metadata only, not spoken.

## Deliberate non-changes

- CL-19 transition kept as FACT's softened "Here's the part that rarely comes up" — the profile transition "Here's the part nobody mentions:" was adjudicated misleading (secrecy frame) in v1 and restoring it would re-enter fact_check as a delta; voice yields to the standing adjudication. Cadence cost is minor: the softened form keeps the same setup-then-payoff shape and the added period (change 3) restores the pause the original colon carried.
- CL-11 ("The timing becomes yours.") left in place directly after the rollover mechanics — its qualification depends on that context.
- Disclosure texts byte-identical: DISC-BEN-TAX-01 sentence in CTA and DISC-BEN-SHORT-01 on-screen line (final line of the script, per format rule). Disclosure wording is never smoothed.
- All other claim sentences byte-identical to v2 (register was already on-profile: second person throughout, no banned openings, no avoided phrases, both profile transitions' slots respected, one CTA).

## Verification on v3

- voice_fingerprint.py (deterministic half only, D-030): PASS — median 7w · p90 14w · grade 6.0 (bands: median target 11 / p90 max 22 / grade 6–9; short-of-median is doctrine-compliant, fragments fine). Judgment resemblance vs. exemplars is a separate assessment: register matches VX-BEN-0004's spoken-teaching beat shape; not claimed as the deterministic score.
- duration_check.py --format reel-90s: PASS — 197 spoken words (band 170–200; ~93s est). Unchanged from v2 (punctuation-only edits).
- claim_diff.py v2 -> v3 --json: `[]` (0 hits) — but see claim-diff.yaml: the differ extracts zero sentences from this reel format (its line-marker filter drops every `[TO CAMERA]` line), confirmed by a control run on v1 -> v2 which also returns 0 despite five known semantic changes. Manual byte-diff accounting substitutes; three cosmetic-claimed touches listed for FACT's call.

## Proposal candidates noticed (SK-A3, standing job)

- Tooling: claim_diff.py should strip inline delivery markers before its
  line-marker filter (as voice_fingerprint.py/duration_check.py do) — as-is it
  is blind to every spoken line of the reel format. Routed as a concern to
  ORCH; script is a protected path (H6), not VOICE-editable.
