# How we keep the prices clean

CardChase prices come from real eBay sold listings, not asking prices or estimates. Raw
sold listings are noisy. People mislabel cards, sell bundles, stage fake sales, and list in
other currencies. Before any sale is allowed to influence a price, it passes five filters.
Anything that fails is dropped or set aside.

---

## The five filters

**1. Is the page real?**
Marketplaces serve bot-blocks, captchas, and sign-in walls that can look like empty
results. A page that lands on one of these is treated as a failed capture and retried, not
read as "no sales". Prices listed in other currencies are converted to USD, and anything we
cannot convert is set aside rather than guessed.

**2. Is it a single card on its own?**
Bundles, lots, playsets, binders, and booster packs are dropped, because their price says
nothing about one card. Non-Pokemon products are dropped. Listings priced below a small
floor are dropped as junk.

**3. Is it actually this card?**
This is the strictest filter. Every listing's title is independently re-matched to a
specific card and checked against the card number and name. If the title resolves to a
different card, or to nothing recognizable, the sale is thrown out. Roughly a third of
otherwise-clean sales are removed here. This is what stops a price from being polluted by
look-alike or mislabeled listings.

**4. Is the condition right?**
Prices are never mixed across conditions. A graded slab and a raw card are different
markets and are kept in separate pools. Near Mint means the title confirms Near Mint, and a
graded card is never allowed to leak into the raw Near Mint price.

**5. Is the price believable?**
Within each card and condition, sales that sit far outside the normal range are flagged.
The check runs on a logarithmic scale, because card prices span a wide range. A single sale
priced more than 50 times the card's typical level, with nothing else near it, is flagged
as a likely staged sale. This is what stops one fake high sale from moving a card's value.

---

## What comes out

Sales that clear all five filters form the priced pool that CardChase reports. Every sale
also carries a quality score, and anything that trips a filter is marked for review rather
than silently trusted, so uncertainty stays visible instead of hidden.
