# RW Module 2 figures — 2025-march-int-e

**1 figure required.** Only Q11 has artwork; every other question in Reading & Writing
Module 2 (PDF pages 28–54) is text-only. All 27 left panes and 27 right panes were read
as separate 1500px-wide crops, so the "EliteXSAT | Eljan Ahmadli" watermark never
obscured a transcribed word.

This form does **not** reuse the Chesapeake seagrass graph or the migration-distance
table that appear around Q9–Q12 on Int-C/D. The quantitative-evidence slot here is the
stony-coral depth table (same family as Int-B Q9, different species).

| Q | Page | SVG path | Description |
|---|------|----------|-------------|
| 11 | 38 | `/mocks/2025-march-int-e/figures/eng2-q11-coral-depths.svg` | Table "Minimum and Maximum Depths of Stony Coral Species in Caribbean and Indo-Pacific Waters" — 3 columns (Species, Minimum depth (meters), Maximum depth (meters)) × 4 species rows: *Psammocora albopicta* 1/28, *Agaricia grahamae* 20/115, *Astreopora gracilis* 5/15, *Acropora echinata* 8/25 |

Regenerate with `py -3 scripts/generate-figures-2025-march-int-e-rw2.py`.

Per the no-double-visuals rule, `stimulus` for Q11 holds only the surrounding prose (the
paragraph that ends in the blank); the table exists solely as the SVG.

## Underlines

**Q7 (page 34) only.** The first sentence is the underlined target:

`<u>In 2011 Stephen D. Simpson and colleagues published a study concluding that ocean acidification has a strong effect on the behavior of Amphiprion percula, a species of fish.</u>`

The stem asks for the function of that underlined sentence (key A: it states Simpson
and colleagues' 2011 conclusion). No other item in this module uses an underline; Q17–Q21
are Standard English convention items and Q22–Q23 are transition items whose target is a
`______` blank. Q14–Q16 are text-completion items whose blank ends the passage.

## Answer key

PDF form `202503亚太E` M2 string `BBABC CACBA CBCBA BCCBD DCDAB CA` — used verbatim.

| Q | Key | Q | Key | Q | Key |
|---|-----|---|-----|---|-----|
| 1 | B | 10 | A | 19 | B |
| 2 | B | 11 | C | 20 | D |
| 3 | A | 12 | B | 21 | D |
| 4 | B | 13 | C | 22 | C |
| 5 | C | 14 | B | 23 | D |
| 6 | C | 15 | A | 24 | A |
| 7 | A | 16 | B | 25 | B |
| 8 | C | 17 | C | 26 | C |
| 9 | B | 18 | C | 27 | A |

All 27 keys were checked against the transcribed choice text and each letter matches
the defensibly correct option.

## Gaps and caveats

- **No missing pages.** Module 2 Q1 is page 28 and Q27 is page 54 (`page = 27 + Q`).
- **Q9 copyright line omitted.** The left pane shows `©2023 by Mick Herron` under the
  excerpt; sibling mocks drop that line, so it is not in `_rw2.json`.
- **Q11 fourth table row** (*Acropora echinata* 8/25) is confirmed by the choice text
  (D) and by the first full-table crop; a tight crop of only the data body clipped that
  last row. *Agaricia grahamae* maximum depth **115** was read the same way on two table
  zooms.
- **Q17 A/B trailing punctuation.** Choices A and B end with a period (`constitutions
  lengths.` / `constitution's length.`); C and D end with a comma. Key C
  (`constitutions' lengths,`) is required because the sentence continues with
  "according to research…".
- **Q19 choice B** is `speculative, though:` (comma + colon). Tight zooms sometimes
  look like a period before `though` because of the watermark; the first full-choice
  crop, the colon introducing the explanatory independent clause, and key **B** all
  agree on comma+colon.
- Blue-highlighted choices in the screenshots are the original test-taker's
  selections and were ignored.
- No question is missing, and no choice is clipped.

## Helper scripts

| Script | Purpose |
|--------|---------|
| `scripts/_crop-rw2-march-int-e.py` | Split pages 28–54 into readable left/right pane crops |
| `scripts/_zoom-rw2-march-int-e.py` | Zoom an arbitrary fractional region of a page (used for underline and punctuation checks) |
| `scripts/generate-figures-2025-march-int-e-rw2.py` | Build the Q11 coral-depth table SVG |
