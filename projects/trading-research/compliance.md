---
version: 1.0.0
project: trading-research
includes: []
---

# Trading Research compliance rules (PROTECTED)

Seeded from the `institutional-trading-research` skill's guardrails (D-008,
Phase 4 §8: "its guardrails seed compliance.md"). These hold in every mode.

- **TRD-C1** — No claims to know private hedge-fund strategies. Public
  frameworks, academic literature, disclosed institutional practice only.
- **TRD-C2** — No promises of profit. Never state or imply expected returns for
  an untested strategy; backtest results describe the past sample and nothing else.
- **TRD-C3** — Nothing is "proven" pre-backtest; surviving out-of-sample makes
  it a hypothesis with better evidence, not a fact.
- **TRD-C4** — Never encourage reckless leverage; futures positions expressed
  in notional and margin terms, never contract counts alone.
- **TRD-C5** — Costs are never optional (transaction, slippage, spread, impact,
  roll, borrow, financing).
- **TRD-C6** — Evidence tags mandatory on every non-trivial market-behavior
  claim: [ESTABLISHED] / [PLAUSIBLE] / [SPECULATIVE]. An untagged assertion is
  a defect. (These tags map into the SK-B2 claim disciplines.)
- **TRD-C7** — Banned language: guaranteed, easy money, secret hedge fund
  strategy, can't lose, perfect setup, always works, proven winner, printing
  money. Preferred: hypothesis, needs backtesting, potential edge,
  regime-dependent, risk-adjusted, robustness, failure condition, drawdown
  control, out-of-sample validation, capacity-constrained, cost-sensitive.
- **TRD-C8** — Strategy research, not investment advice: no buy/sell
  recommendations of specific securities, no sizing against actual net worth.
- **TRD-C9** — Never recommend live deployment without IS + OOS testing, cost
  sensitivity, regime stress tests, and a written risk review.
- **TRD-C10** — Educational disclaimer (DISC-TRD-01) on published research outputs.

## DISC-TRD-01

> Educational research only. Not investment advice, not a recommendation to buy
> or sell any security or derivative. Hypothetical and backtested results do
> not represent actual trading and have inherent limitations.
