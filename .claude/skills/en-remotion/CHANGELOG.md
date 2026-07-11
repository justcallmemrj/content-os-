# en-remotion (SK-C2) — change log

## 1.0.0 — 2026-07-11 (build step 9)

- Initial authoring against docs verified at build time (D-062: composition
  registration, frame model, `--props=./props.json` render contract).
- License gate cleared first: DEC-BUILD-008 ratified (free tier, ≤3 employees
  attested by Wes; pin remotion@4.0.487 = upstream tag commit 2e8037fe).
- Text-verbatim mechanism = props injection: gen_props / props_verbatim_check /
  tsx_static_check (no-literal-JSX-text + SafeArea containment + exact
  safe-area tokens, same px table as SK-C1).
- render_manifest.py (RM- prefix) refuses floated versions at BOTH layers
  (flag and workspace package.json).
- Tests 12/0: shared-fixture property, paraphrase + literal-text +
  outside-SafeArea counterexamples, pin integrity.
