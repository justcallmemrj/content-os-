# What counts as a claim (SK-B2)

A claim is any assertion a reader could check and find false. Five kinds, all
ledgered:

- **Stated** — "Maximum DROP participation is 96 months."
- **Implied** — "teachers who retire at 30 years" implies a 30-year normal-
  retirement rule; the implication is the claim. The classic FOUND class.
- **Numeric** — figures, dates, percentages, dollar amounts, deadlines. Always
  at least medium risk; volatile numerics prefer routing ("confirm on MyFRS")
  over assertion.
- **Visual / on-screen** — any `[TEXT ON SCREEN:]` string. Ledgered with
  `on_screen: true`; must appear byte-identical in the deliverable and later
  the render (D-016).
- **Comparative** — "X is taxed more heavily than Y," "most members choose…"
  Comparatives smuggle two claims and a quantifier; risk-classify on the worst.

Not claims: opinions labeled as such, questions, pure instructions ("ask what
a rollover does to your tax year"), texture without factual content. When
unsure, ledger it — a needless `low` row costs nothing; a missed claim is the
failure mode this Skill exists to prevent.
