# DEC-BUILD-007 — Retirement of the `benowitz-ducat-social` skill (D-038 cutover)

| | |
|---|---|
| Status | RATIFIED by Wes's slice-acceptance signature, 2026-07-10 |
| Type | Cutover decision record (Phase 4 §8: "The original Skill is retired at cutover with a decision record") |

**Decision:** the standalone `benowitz-ducat-social` skill is retired as an
operating surface for Benowitz/Ducat content. The content-os pipeline is its
successor. The skill remains installed on the machine as a historical
reference; it is no longer the procedure of record.

**Where everything it knew now lives (nothing lost, everything governed):**

| It knew | Now governed at |
|---|---|
| RIA compliance envelope, four hard lines | `projects/_shared/ria-compliance-envelope.md` (+ HK-backed, lint-shadowed) |
| Brand voice, audience, vocabulary (both brands) | `projects/{benowitz-wealth,ducat-private-wealth}/brand-voice.md`, `audience.md`, profile `foreign_terms` |
| Disclosure texts + placement rules | `disclosures.md` per brand + SK-B15 |
| Fee-only hold | DEC-BEN-0001 + compliance.md rules |
| 90s/190w format, 7 beats, markers, hooks-in-tens | SK-B3 + its validators |
| `[VERIFY:]` discipline, ⚠ unsourced header | SK-B2 (`[UNVERIFIED]` path) — exercised in the acceptance battery |
| Intervention-note convention | SK-A2 change-log format — 9 notes in the injected-failure fixture alone |
| Calendar rules (inventory-first, source column) | STRAT card + SK-B12 (authored at step 7) |
| Back-catalog knowledge | `projects/benowitz-wealth/assets/` + manifest |

**Verification that the successor outperforms the original:** the slice
acceptance battery — the pipeline blocked the injected performance-claim
request, refused the cross-brand packet, produced the ⚠ header path, and
delivered an H2-approved script with owner edit distance 0.
