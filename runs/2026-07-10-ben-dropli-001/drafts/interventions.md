# Intervention notes — 2026-07-10-ben-dropli-001 / drop-linkedin-v1.md (WRITE)

Departures from the literal work order / brief, uncapped, per writer.md.

1. **Reused 10 parent claims byte-identically, not the minimum 2-3.** CL-04
   (termination rule), CL-05, CL-06, CL-07 (tax mechanics), CL-08, CL-09,
   CL-10, CL-12, CL-13, CL-14 all embedded with the ledger's exact claim-text
   bytes (lowercase-start claims placed mid-sentence so the substring match
   holds — e.g. "After that, your monthly pension turns on by itself."). This
   maximizes inheritance and shrinks FACT's delta scope to 7 fresh entries.

2. **Duplicative fresh declarations for framing additions (honesty over
   tidiness).** "After that, your monthly pension turns on by itself."
   (sequencing frame) and "Take the check, and cash gets taxed as that year's
   ordinary income, stacked on everything else you earn." (route-scoping
   frame) contain inherited claim text but add connective assertions the
   parent stated elsewhere/differently, so each is ALSO declared as a fresh
   unverified claim. FACT may collapse them onto the inherited entries; that
   is FACT's call, not mine (D4/D8).

3. **In-post short disclosure added beyond the work order's disclosure list.**
   The work order lists only DISC-BEN-FRS-01 (first comment). The deterministic
   compliance tier (compliance_lint ENV-4) requires "Educational" +
   "not affiliated with" in the deliverable itself, and the draft touches
   taxes, which pulls the TAX-referral line in-post. I used DISC-BEN-SHORT-01
   verbatim ("Educational only. Not advice. Not affiliated with FRS.") plus
   DISC-BEN-TAX-01 in the closing paragraph, and satisfied the short-format
   condition by stating in-post that full disclosures live in the first
   comment. Declared high-risk (mirrors parent CL-15's placement condition).

4. **First-comment statement declared high-risk.** "The registration link and
   our full disclosures are in the first comment." is only true if
   drafts/first-comment.md is actually posted at publish — a hard publish-gate
   condition, same class as parent CL-15's qualification. The two fresh
   high-risk unverified entries are therefore expected in the blocking summary
   until FACT's delta pass and the publish gate.

5. **Avoided the parent's "isn't on any form / nobody mentions" shading.** The
   opening scene deliberately makes no claim that FRS forms or statements fail
   to cover the payout election (CL-19 lesson: secrecy frames get flagged).
   The teacher simply asks the coordinator; nothing is asserted about what FRS
   does or doesn't say (audience.md "What to avoid" respected — no villain).

6. **Illustrative opening is a composite, not a client.** "A teacher in her
   last year of DROP..." is a hypothetical scene, declared as a low-risk claim
   so FACT can adjudicate the texture honestly; it names no person and quotes
   no client (envelope hard line 2 untouched).

7. **Audience-behavior claim declared medium.** "The first person an FRS
   member asks is almost never an advisor. It's you." asserts member
   help-seeking behavior. Directionally supported by audience.md
   (linkedin-referrers: "The people there stand next to the client"), but
   audience.md is register, not an evidence packet — declared unverified,
   medium risk, for FACT.

8. **Header kept to one short line.** social_format_check counts every
   non-"disclosure"-prefixed word in the file toward the 150-300 band, so run
   metadata lives here instead of a provenance block atop the draft.
   Validator-counted words: 281; post copy alone (header excluded): 274.

9. **Script execution note.** writer.md's tool posture is read/write-only
   (no Bash); ORCH's work order for this run explicitly mandates running
   inherit_ledger.py and the three validators, so I executed exactly those
   commands and nothing else. The child ledger write is the SK-B5 pre-FACT
   inheritance step, not a post-FACT ledger touch.

10. **CTA scope.** Forward-this / weigh-in only, per SK-B4 LinkedIn canon and
    brand-voice cta_patterns — no book-a-call, no registration ask in the
    post body itself; the registration link rides in the first comment.

## Validator record (all green, first pass)

- social_format_check --format linkedin: PASS, 0 findings (281 words in band;
  first-comment statement present; no link-in-bio; no staccato one-liners)
- compliance_lint --project benowitz-wealth: 0 findings (disclosure snippets
  present; TAX-referral line present; no hard-line hits)
- lexicon_scan --project benowitz-wealth: 0 foreign-term hits
- inherit_ledger: OK — 10 inherited (parent hash verified), 7 fresh,
  high_risk_non_verified=2 (the two publish-gate disclosure/placement claims,
  awaiting FACT delta adjudication)
