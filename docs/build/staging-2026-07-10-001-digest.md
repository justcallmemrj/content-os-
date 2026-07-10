# Curation digest — staging/2026-07-10-001 (first H6 ratification)

**What this PR is:** the D-038 decomposition of `benowitz-ducat-social` plus the
four project scaffolds — build step 3's first tranche. Per D-079 everything here
is a **proposal until your merge**; nothing in `projects/` is live before that.
Facts (F-*), sources (S-*), and voice exemplars (VX-*) are NOT in this PR — they
need your back-catalog materials and come as a second staging PR.

**Provenance:** every substantive line traces to (a) the ratified
`benowitz-ducat-social` skill (voice, audience, vocabulary, compliance envelope,
disclosure texts — quoted verbatim where the spec demands verbatim), (b) the
package §8.1 sample profile (BEN frontmatter adopted verbatim), or (c) the
`institutional-trading-research` guardrails (TRD compliance). Conflicts found: none.

## Sections (one per proposal class)

1. **`projects/_shared/ria-compliance-envelope.md`** — the four hard lines +
   firm-wide standing rules, from the skill's compliance.md. Included by
   explicit reference from both brand compliance files (Phase 3 §3.5).
2. **Benowitz set** — profile (§8.1 verbatim frontmatter), brand-voice
   (tone sliders are the Phase 3 §4.5 ratified sample values; banned/avoided
   lists verbatim from the skill), audience (incl. the LinkedIn
   write-to-the-referrer doctrine), compliance (BEN-C1…C6), disclosures
   (DISC-BEN-FRS-01 / TAX-01 / SHORT-01, verbatim), and **DEC-BEN-0001** (the
   fee-only hold, formalized as the decision record the rule points to).
3. **Ducat set** — same shape. ⚠ **Review flag:** DUC tone sliders and
   sentence-length targets are MY derivation from the skill's prose ("composed,
   fewer words, more weight") — BEN's numbers came from a ratified sample,
   Ducat's did not. Marked PROPOSED in the file; adjust before or after merge.
4. **Trading Research** — profile (status: scaffolded) + compliance seeded from
   the 12 SK-C4 guardrails, incl. the evidence-tag mandate and DISC-TRD-01.
5. **Founder Brand** — deliberately thin scaffold; conservative default keeps
   the RIA envelope included until an activation review says otherwise.
6. **foreign_terms cross-population** (package §9): BEN carries Ducat+trading
   vocabulary, DUC carries Benowitz+trading, TRD/FDR carry all siblings'.

## What merging does

Activates the four profiles + envelope as approved memory (L1); the loader
already assembles them (validated: 6 records, namespace-clean). Post-merge I
regenerate indexes on main and log the H6 event.

## What this PR does deliberately NOT contain

Approved facts, source records, voice exemplars, calendar/campaign data, any
Skill bodies (step 4), any agent definitions (step 5). The original
`benowitz-ducat-social` skill is NOT yet retired — that decision record comes
at cutover, after SK-B2/B3/B4/B15 exist (step 4).
