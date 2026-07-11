# DEC-BUILD-008 — Remotion license eligibility + dependency pin (step 9 gate)

**Status:** RATIFIED 2026-07-11 — Wes attested ≤3 employees (A=yes) and approved pin remotion@4.0.487 (B=yes), in-session
**Date:** 2026-07-11 · **Named escalation:** master prompt §6 (license eligibility at step 9)

## Verified live (D-062, 2026-07-11, two surfaces)

**github.com/remotion-dev/remotion/LICENSE.md:** free use is granted to
individuals and *"a for-profit organization with up to 3 employees"* — and the
grant explicitly covers commercial video creation: *"Permission is hereby
granted… to use the software non-commercially or commercially for the purpose
of creating videos and images."* Prohibited: reselling/relicensing Remotion
derivatives (not our use).

**remotion.pro/license:** 4+ employees requires a Company License — Creators
$25/mo/seat (low-volume coded video) or Automators $0.01/render with $100/mo
minimum (automated pipelines); Enterprise from $500/mo.

## Assessment

1. **Eligibility hinges on one fact only:** Joy Financial Group LLC's employee
   count. At ≤3 employees the free tier covers our commercial use outright.
   (Wes already uses remotion@4.0.487 personally in the approved
   benowitz-drop-exit webinar kit on this machine.)
2. **Future-trigger nuance worth recording now:** our video machine is an
   agent-driven render pipeline. If the firm ever crosses to 4+ employees, the
   applicable paid tier is plausibly **Automators** (per-render + $100/mo
   minimum), not just Creators seats — the cost asymmetry vs HyperFrames
   (Apache-2.0, no threshold) stays a live SK-B17 routing factor (D-070), and
   **hiring person #4 remains the standing licensing-review trigger**
   (Phase 7 §7).
3. **Proposed dependency pin:** `remotion@4.0.487` (+ `@remotion/cli@4.0.487`)
   — the exact version already proven on this machine in the approved webinar
   kit; installed only inside `video/remotion/` (REMO's jailed scope), never
   run-time fetched beyond the pinned install.

## Decision needed from Wes

A. Attest headcount: is Joy Financial Group LLC (all brands) at ≤3 employees?
B. Approve the dependency: install remotion@4.0.487 pinned in video/remotion/.

If A=yes and B=yes → SK-C2 authoring proceeds against docs verified at build
time; comparability fixtures (same gates as SK-C1) follow. If A=no → paid-tier
decision before any install.
