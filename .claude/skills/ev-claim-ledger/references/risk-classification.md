# Risk classification (SK-B2)

**high** — numeric, eligibility, legal, tax: anything whose wrongness costs
the reader money or standing, or costs the firm an examination. Includes:
dollar figures, percentages, statutory rules, deadlines/windows, eligibility
criteria ("only Pension Plan members"), tax treatment, Medicare/SS rules.
High-risk claims block T7 unless verified/verified-with-qualification (E1).

**medium** — checkable but low-consequence: program names and mechanics
already public and stable, dated history, definitions.

**low** — texture with a factual shadow: "many members," "a common mistake."

**Project volatility modifiers:** figures the legislature adjusts (DROP
window, interest rate, COLA mechanics) are high regardless of how stable they
look — their `review_by` is the freshness contract. TRD: any market-behavior
claim inherits its evidence tag's weight; untagged = defect, not low-risk.
