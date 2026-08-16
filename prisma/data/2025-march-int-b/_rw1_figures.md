# RW Module 1 figures — 2025-march-int-b

Four questions in Reading & Writing Module 1 carry a visual (three tables, one bar graph).
All other items (Q1–Q9, Q14–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 10 | `public/mocks/2025-march-int-b/figures/eng1-q10-africa-population.svg` | Table: **Population and Population Density of African Countries in 2015**. Columns: Country, Density (inhabitants/km²), Area (km²), Estimated population. Rows: São Tomé and Príncipe (189.8, 1,001, 190,000); Ethiopia (88.2, 1,127,127, 99,391,000); Mauritania (3.9, 1,030,700, 4,068,000); Angola (20.1, 1,246,700, 25,022,000). |
| 11 | `public/mocks/2025-march-int-b/figures/eng1-q11-fta-export-growth.svg` | Grouped bar graph: **Average Total Agricultural Export Growth Rate, Five Years Pre- and Post-FTA with the United States**. y-axis "Growth rate (%)", ticks −5 to 25 by 5. x-axis "Export growth" with groups "Pre-FTA" and "Post-FTA". Legend: El Salvador (CAFTA-DR) = dark gray, Mexico (NAFTA) = light gray, Nicaragua (CAFTA-DR) = black. Values — Pre-FTA: El Salvador ≈ 8.7, Mexico ≈ −1.4 (only negative bar), Nicaragua ≈ 23.6; Post-FTA: El Salvador ≈ 21.8, Mexico ≈ 13.8, Nicaragua ≈ 17.7. |
| 12 | `public/mocks/2025-march-int-b/figures/eng1-q12-lava-worlds.svg` | Table: **Three Candidate Lava Worlds, by Modeled Mass, Density, and Surface Temperature**. Columns: Planet, Mass (Earth masses), Density ratio, Temperature (kelvins). Rows: HD 80653 b (5.6, 7.4, 2,300); Kepler-10 b (3.6, 6.0, 2,130); K2-265 b (0.8, 7.1, 1,400). |
| 13 | `public/mocks/2025-march-int-b/figures/eng1-q13-productivity-loss.svg` | Table: **Average Monetized Productivity Loss at Two Points After Programs Began, in Australian Dollars**. Columns: Type of training, 12 weeks, 12 months. Rows: EET (268, 171); EHP (282, 436). |

## Figure notes

- Stimuli for Q10, Q12, and Q13 in `_rw1.json` hold only the surrounding prose; the table
  title and cells live solely in the SVG so the item never renders the data twice.
- Q11's stimulus likewise holds only the researcher prose; the chart title, axis labels, and
  legend belong in the SVG.
- Q11 bar heights were read off the 5-unit gridlines on a 2.4× upscale of `page-11.png`.
  Only Mexico's Pre-FTA bar dips below zero, and Nicaragua is the one country whose Pre-FTA
  bar is taller than its Post-FTA bar — the relationship the correct answer (B) depends on.
  Choice D quotes El Salvador's Post-FTA rate as "about 21.8 percent", which matches the
  measured bar.
- Q13's table is numerically identical to the Q11 table in `2025-march-int-a`; the SVG can be
  copied from `public/mocks/2025-march-int-a/figures/eng1-q11-productivity-loss.svg` with the
  slug swapped.

## Verification notes

- Every page image `page-01.png` … `page-27.png` was read individually; the `_ocr/` drafts only
  cover pages 01–10 and were garbled wherever the "EliteXSAT | Eljan Ahmadli" watermark crosses
  the text (e.g. all of Q7's middle lines), so obscured regions were re-checked with 2.4–2.8×
  upscaled crops.
- Underlined targets (rendered with `<u>…</u>`) appear in Q2 ("cheating"), Q5 (the final
  sentence, "However, new studies suggest…originally thought."), and Q14 (the sentence
  beginning "Over the ensuing centuries…full-time career.").
- Q8 choice B reads "stimulants" (not "simulants") on the page; the typo is preserved. Note the
  supplied answer key marks Q8 as C, although choice D is the standard College Board answer for
  this item — the key was recorded as given.
- Q25 is the only notes item without the "While researching a topic…" lead-in; the page shows
  the bulleted sentences alone, matching the stem's wording "from the given sentences".
- Italicized titles and scientific names (e.g. The Joy Luck Club, Carnobacterium viridans,
  ningyo joruri, Pipturus albidus) are stored as plain text, following the `2025-march-int-a`
  convention.
