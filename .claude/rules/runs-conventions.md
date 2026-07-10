---
paths: runs/**
---

# Run workspace conventions — SCAFFOLD (populates at build step 2/6)

Each run: `runs/<run-id>/` with `workorder.yaml`, `handoffs/`, `research/`,
`drafts/`, `factcheck/`, `voice/`, `compliance/`, `qa/`, `storyboard/`, `logs/`,
`summary.md` (Phase 3 §5.1). Run IDs: `<date>-<proj>-<slug>-<seq>`. Agents write
only inside their own stage directory. State changes only via
`scripts/transition.py`.
