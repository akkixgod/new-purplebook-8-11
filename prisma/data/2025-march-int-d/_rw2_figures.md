# RW Module 2 figures — 2025-march-int-d

**2 figures required.** Q9 is the Chesapeake Bay seagrass line graph; Q10 is a
migration-distance table. Every other question in Reading & Writing Module 2
(PDF pages 27–28 and 29–52) is text-only.

| Q | Page | SVG path | Description |
|---|------|----------|-------------|
| 9 | 34 | `/mocks/2025-march-int-d/figures/eng2-q09-chesapeake-seagrass.svg` | Line graph "Chesapeake Bay Seagrass Coverage 2012–2019". x-axis Year (2012–2019), y-axis "Seagrass area (hectares)" 0–45,000 with gridlines every 9,000. Three series: eelgrass (solid line, filled triangles), widgeon grass (dashed line, gray squares), total of all types of seagrass (dotted line, open circles) |
| 10 | 35 | `/mocks/2025-march-int-d/figures/eng2-q10-migration-distances.svg` | Table "Reported Annual Travel Distances in Four Studies of Migrating Animal Populations" — 4 columns (Species, Continent, Distance (km), Measurement method) × 4 rows: Brown bear / North America / 1,325 / GPS; Tibetan antelope / Asia / 700 / RTD; Caribou / North America / 4,868 / GPS; Reindeer / Asia / 1,200 / RTD |

Q9 values read off the scan (nearest ~100 hectares), matching the same College Board
graph used as Int-C RW M2 Q10:

| Year | eelgrass | widgeon grass | total |
|------|----------|---------------|-------|
| 2012 | 5,400 | 5,800 | 19,600 |
| 2013 | 7,000 | 8,400 | 24,400 |
| 2014 | 7,000 | 12,400 | 30,500 |
| 2015 | 8,600 | 15,600 | 37,500 |
| 2016 | 8,800 | 17,300 | 40,500 |
| 2017 | 8,600 | 18,000 | 42,600 |
| 2018 | 9,700 | 16,300 | 43,900 |
| 2019 | 5,000 | 8,900 | 27,000 |

Regenerate with `py -3 scripts/generate-figures-2025-march-int-d-rw2.py`.

Per the no-double-visuals rule, `stimulus` for Q9 and Q10 holds only the surrounding
prose; the graph/table exist solely as SVGs.

## Underlines

**No underlined targets appear anywhere in this module**, so no `<u>` markup is used.
Q16–Q21 are Standard English convention items and Q22–Q23 are transition items; in
all of them the target is a `______` blank. Q12–Q15 are text-completion items whose
blank ends the passage.

## Answer key

PDF page 90, form `202503亚太D`, string `AD空CA DBBAB BACDB DDCDD DDBAA DB` — used
verbatim except Q3 (no page in this capture).

| Q | Key | Q | Key | Q | Key |
|---|-----|---|-----|---|-----|
| 1 | A | 10 | B | 19 | D |
| 2 | D | 11 | B | 20 | D |
| 3 | D (filled) | 12 | A | 21 | D |
| 4 | C | 13 | C | 22 | D |
| 5 | A | 14 | D | 23 | B |
| 6 | D | 15 | B | 24 | A |
| 7 | B | 16 | D | 25 | A |
| 8 | B | 17 | D | 26 | D |
| 9 | A | 18 | C | 27 | B |

## Gaps and caveats

- **Q3 is missing** from the source PDF (the capture jumps from Module 2 Q2 on
  page 28 to Q4 on page 29). Filled with the same-slot words-in-context item from
  `2025-march-int-c/_rw2.json#3` (Whistler / "dispassionate"), marked `_filledFrom`,
  key **D**. That item is not used elsewhere in this mock (RW M1 Q6 was filled from
  Int-A M1 Q1).
- **Q9 passage is complete** (unlike Int-C Q10, whose left pane was clipped). The
  researchers' point here is that the rise in total coverage "does not necessarily
  make the seagrass ecosystem as a whole more resilient to environmental shocks,"
  which is why key A (2019 algal blooms hitting many seagrass species) is the
  option that both matches the 2019 crash of all three series and illustrates that
  caution. Choice order differs from Int-C (algal blooms is A here, D there).
- **Q19 key D** (`behavior: while the`) follows the PDF key. The colon introduces
  the contrast that explains the "striking differences"; the same family is keyed
  that way on Int-A RW M2 Q18.
- Blue-highlighted choice C on page 43 (Q18) is the original test-taker's
  selection; it happens to match the key.
- No question other than Q3 is missing, and no choice is clipped.

## Helper scripts

| Script | Purpose |
|--------|---------|
| `scripts/_crop-rw2-march-int-d.py` | Split pages 27–52 into readable left/right pane crops |
| `scripts/_zoom-rw2-march-int-d.py` | Zoom an arbitrary fractional region of a page (used for punctuation checks) |
| `scripts/generate-figures-2025-march-int-d-rw2.py` | Build the Q9 seagrass graph and Q10 migration table |
