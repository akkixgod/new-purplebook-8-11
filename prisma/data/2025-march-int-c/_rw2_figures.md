# RW Module 2 figures — 2025-march-int-c

**1 figure required.** Only Q10 has artwork; every other question in Reading & Writing
Module 2 (PDF pages 28–54) is text-only. All 27 left panes and 27 right panes were read
individually as separate 1500px-wide crops, so the "EliteXSAT | Eljan Ahmadli" watermark
never obscured a transcribed word.

| Q | Page | SVG path | Description |
|---|------|----------|-------------|
| 10 | 37 | `/mocks/2025-march-int-c/figures/eng2-q10-chesapeake-seagrass.svg` | Line graph "Chesapeake Bay Seagrass Coverage 2012–2019". x-axis Year (2012–2019), y-axis "Seagrass area (hectares)" 0–45,000 with gridlines every 9,000. Three series: eelgrass (solid line, filled triangles), widgeon grass (dashed line, gray squares), total of all types of seagrass (dotted line, open circles) |

Values read off the scan (nearest ~100 hectares):

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

Regenerate with `py -3 scripts/generate-figures-2025-march-int-c-rw2.py`.

Per the no-double-visuals rule, `stimulus` for Q10 holds only the surrounding prose; the
graph exists solely as the SVG.

## Underlines

**No underlined targets appear anywhere in this module**, so no `<u>` markup is used.
There are no "as used in the text" / "function of the underlined portion" items. Q15–Q21
are Standard-English convention items and Q22–Q24 are transition items; in all of them the
target is a `______` blank, and Q12–Q14 are text-completion items whose blank ends the
passage.

## Answer key

PDF page 107, form `202503亚太C`, string `M2 CDDCD DCBBD CDCAC BCDDA BCBDC AA` — used verbatim.
Blue-highlighted choices in the screenshots are the original test-taker's selections and were
ignored (e.g. page 48 / Q21 shows C selected while the key says B; page 28 / Q1 happens to
agree with the key at C).

26 of the 27 keys were independently re-derived from the transcribed choice text and matched.
The single exception is noted below.

## Gaps and caveats

- **Q10 passage tail is clipped (page 37).** The left pane scrolls, and the screenshot cuts
  the passage mid-sentence after "…associated with a substantial increase in total seagrass
  coverage". There is no second capture of page 37 in the PDF (pages 105/106 duplicate pages
  30/31 only), and the OCR footer strip contains the same truncated lines. The final clause in
  `_rw2.json` ("in the bay, researchers caution that widgeon grass populations are unstable,
  collapsing rapidly when water quality declines, so gains that depend on widgeon grass may
  prove short-lived") is a **reconstruction** consistent with the graph's 2019 collapse and with
  key D. Replace it if a complete capture of the passage becomes available.
- **Q16 key looks wrong (page 43).** The sentence is "…the editors chose the ______ author of
  *Inheritance*." Choice A ("novelist Lan Samantha Chang,") is the conventionally correct
  punctuation — a nonrestrictive appositive needs the comma before "author of *Inheritance*".
  The key says **B** ("novelist Lan Samantha Chang", no comma), which leaves the appositive
  unpunctuated. The key was followed as instructed; the choice text and the absence of a comma
  after the blank in the passage were both verified at high zoom.
- **Q25 has no notes header (page 52).** Unlike Q26/Q27, the left pane presents four plain
  bullet sentences with no "While researching a topic, a student has taken the following notes:"
  line, matching its stem ("uses information from the given sentences"). Transcribed as-is.
- Pages 105 and 106 were ignored per `_map.md`; pages 30 and 31 were used for Q3 and Q4.
- No question in this module is missing, and no choice is clipped.

## Helper scripts

| Script | Purpose |
|--------|---------|
| `scripts/_crop-rw2-march-int-c.py` | Split pages 28–54 into readable left/right pane crops |
| `scripts/_zoom-rw2-march-int-c.py` | Zoom an arbitrary fractional region of a page (used for punctuation checks) |
| `scripts/generate-figures-2025-march-int-c-rw2.py` | Build the Q10 seagrass line-graph SVG |
