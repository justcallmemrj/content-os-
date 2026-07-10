# Delivery markers (SK-B3 — migrated intact per D-008)

Scripts get shot three ways; every block carries its marker:

- `[TO CAMERA]` — anything with a claim in it, or any moment of authority.
- `[VO / B-ROLL: description]` — texture, transitions, emotional beats.
- `[TEXT ON SCREEN: "..."]` — numbers, names, anything that must be read
  exactly. Every such string is a ledger claim with `on_screen: true` and is
  byte-matched downstream (D-016). The disclosure lives in a persistent
  `[TEXT ON SCREEN:]` block — nobody says a disclaimer out loud and keeps the
  viewer.
