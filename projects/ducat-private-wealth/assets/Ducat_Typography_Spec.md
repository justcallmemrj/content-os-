# Ducat Private Wealth — Typography & Brand Token Spec

A build-ready specification for the website and digital materials. Designed for a
discreet, elite private-wealth brand. The type system pairs a high-contrast
Didone display face (echoing the "DUCAT" logo wordmark) with a clean humanist
sans for body text.

---

## 1. Font Families

### Launch system (100% free — Google Fonts)
| Role | Font | Notes |
|------|------|-------|
| Display / Headlines | **Playfair Display** | High-contrast Didone serif; matches the logo wordmark feel. |
| Body / UI text | **Inter** | Humanist sans; highly readable at small sizes, modern, trustworthy. |
| Labels / Small caps | **Inter** (uppercase + wide tracking) | Used for eyebrows, nav, "PRIVATE WEALTH"–style lines. |

### Optional paid upgrade (later)
| Role | Font | Notes |
|------|------|-------|
| Display / Headlines | **Canela** or **Ogg** | More distinctive Didone-adjacent serif with warmth. Requires license. |
| Body | **Söhne** or **Neue Haas Grotesk** | Premium grotesque sans. Requires license. |

> Rule: never more than 3 families. One display, one body, optional one for labels.

---

## 2. Web Font Loading

```html
<!-- In <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link
  href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap"
  rel="stylesheet">
```

Weights loaded:
- **Playfair Display:** 400, 500, 600, 700 + 400 italic
- **Inter:** 300, 400, 500, 600

---

## 3. CSS Custom Properties (design tokens)

```css
:root {
  /* Font families */
  --font-display: 'Playfair Display', Georgia, 'Times New Roman', serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* Brand colors — "Vault" palette */
  --color-navy:      #102030;  /* primary / base */
  --color-gold:      #B08D57;  /* antique gold — accent only, 5–10% of layout */
  --color-bone:      #F4EFE6;  /* background */
  --color-charcoal:  #2B2B2B;  /* body text */
  --color-cream-text:#F4EFE6;  /* text on dark backgrounds */

  /* Type scale (1.250 — major third) */
  --text-xs:   0.8rem;    /* 12.8px — fine print, disclosures */
  --text-sm:   0.9rem;    /* 14.4px — captions, labels */
  --text-base: 1rem;      /* 16px   — body */
  --text-lg:   1.25rem;   /* 20px   — large body / lead */
  --text-xl:   1.563rem;  /* 25px   — H4 / subhead */
  --text-2xl:  1.953rem;  /* 31px   — H3 */
  --text-3xl:  2.441rem;  /* 39px   — H2 */
  --text-4xl:  3.052rem;  /* 49px   — H1 */
  --text-5xl:  3.815rem;  /* 61px   — hero display */

  /* Line heights */
  --leading-tight:   1.1;   /* display headlines */
  --leading-snug:    1.25;  /* subheads */
  --leading-normal:  1.6;   /* body text */

  /* Letter spacing */
  --tracking-tight:  -0.02em; /* large Didone headlines */
  --tracking-normal: 0;
  --tracking-wide:   0.15em;  /* small-caps labels */
  --tracking-wider:  0.25em;  /* "PRIVATE WEALTH"-style lockup lines */
}
```

---

## 4. Element Styles

```css
body {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--color-charcoal);
  background: var(--color-bone);
  -webkit-font-smoothing: antialiased;
}

/* Headlines — Didone display */
h1, h2, h3 {
  font-family: var(--font-display);
  font-weight: 500;
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--color-navy);
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); line-height: var(--leading-snug); }

/* Subheads — can use display or body depending on context */
h4 {
  font-family: var(--font-body);
  font-weight: 600;
  font-size: var(--text-xl);
  line-height: var(--leading-snug);
  color: var(--color-navy);
}

/* Hero display line */
.hero-display {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: var(--text-5xl);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--color-navy);
}

/* Eyebrow / label / small-caps */
.eyebrow,
.label {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  color: var(--color-gold);
}

/* Lockup line (e.g. "PRIVATE WEALTH") */
.lockup-line {
  font-family: var(--font-body);
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
}

/* Lead / intro paragraph */
.lead {
  font-size: var(--text-lg);
  line-height: var(--leading-normal);
  font-weight: 300;
}

/* Body paragraph */
p {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  max-width: 68ch; /* readable measure */
}

/* Fine print / disclosures */
.fine-print {
  font-size: var(--text-xs);
  line-height: 1.5;
  color: #6b6b6b;
}

/* Pull quote — display italic */
blockquote {
  font-family: var(--font-display);
  font-style: italic;
  font-weight: 400;
  font-size: var(--text-2xl);
  line-height: var(--leading-snug);
  color: var(--color-navy);
}
```

---

## 5. Usage Rules (non-negotiable for brand feel)

1. **Didone for display ONLY.** Never set body/paragraph text in Playfair Display
   — the thin hairlines vanish and strain the eye at small sizes. Body is always Inter.
2. **Gold is an accent, not a fill.** Keep gold to ~5–10% of any layout (a rule,
   a label, a small mark). Large gold areas read "casino," not "private bank."
3. **Letter-spacing = luxury signal.** Set all uppercase labels and lockup lines
   with wide tracking (`--tracking-wide` / `--tracking-wider`). Airy spacing reads premium.
4. **Restraint in weight.** Headlines at 500–600, not 700+, for an understated tone.
   Body at 400; light (300) only for lead paragraphs.
5. **Generous whitespace.** Treat negative space as a feature. Crowded = cheap.
6. **Readable measure.** Cap paragraph width around 65–70 characters (`max-width: 68ch`).

---

## 6. Dark-Background Variant

On navy (`--color-navy`) backgrounds:
- Headlines and body text switch to **cream** (`--color-cream-text` / `#F4EFE6`).
- Gold accent stays the same (`#B08D57`) — it reads well on navy.
- Do NOT use navy text on navy (the logo wordmark disappears — use the reversed
  light logo version on dark sections).

```css
.section--dark {
  background: var(--color-navy);
  color: var(--color-cream-text);
}
.section--dark h1,
.section--dark h2,
.section--dark h3 { color: var(--color-cream-text); }
.section--dark .eyebrow,
.section--dark .label { color: var(--color-gold); }
```

---

## 7. Quick Reference Summary

- **Display font:** Playfair Display (Didone serif) — headlines, hero, pull quotes
- **Body font:** Inter (humanist sans) — paragraphs, UI, labels
- **Scale:** 1.250 major-third, base 16px
- **Colors:** Navy #102030 · Gold #B08D57 · Bone #F4EFE6 · Charcoal #2B2B2B
- **Signature move:** serif headline + wide-tracked sans label + lots of whitespace
