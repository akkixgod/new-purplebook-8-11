# RW Module 1 figures — 2025-march-int-e

Three questions in Reading & Writing Module 1 carry a visual (one line graph, one bar graph, one table).
All other items (Q1–Q8, Q10, Q13–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 9 | `public/mocks/2025-march-int-e/figures/eng1-q09-fish-population.svg` | Line graph: **Fish Population in a Taiwanese Tide Pool, January 2001 to October 2001**. y-axis "Number of individual fish observed", ticks 0–30 by 5. x-axis "Month": January 2001, April 2001, July 2001, October 2001. Legend: Cocos frillgoby = solid black line + filled triangles; wavy-lined blenny = dashed gray line + filled gray squares; Indo-Pacific sergeant = dotted black line + open circles. Values (Jan, Apr, Jul, Oct): Cocos frillgoby 0 / 10 / 5 / 5; wavy-lined blenny 0 / 0 / 0 / 4; Indo-Pacific sergeant 2 / 3 / 21 / 28. |
| 11 | `public/mocks/2025-march-int-e/figures/eng1-q11-fta-export-growth.svg` | Grouped bar graph: **Average Total Agricultural Export Growth Rate, Five Years Pre- and Post-FTA with the United States**. y-axis "Growth rate (%)", ticks −5 to 25 by 5. x-axis "Export growth" with groups "Pre-FTA" and "Post-FTA". Legend: El Salvador (CAFTA-DR) = dark gray, Mexico (NAFTA) = light gray, Nicaragua (CAFTA-DR) = black. Values — Pre-FTA: El Salvador ≈ 8.7, Mexico ≈ −1.4 (only negative bar), Nicaragua ≈ 23.6; Post-FTA: El Salvador ≈ 21.8, Mexico ≈ 13.8, Nicaragua ≈ 17.7. |
| 12 | `public/mocks/2025-march-int-e/figures/eng1-q12-productivity-loss.svg` | Table: **Average Monetized Productivity Loss at Two Points After Programs Began, in Australian Dollars**. Columns: Type of training, 12 weeks, 12 months. Rows: EET (268, 171); EHP (282, 436). |

## Figure notes

- Stimuli for Q9, Q11, and Q12 in `_rw1.json` hold only the surrounding prose; chart title/axes/legend and table title/cells live solely in the SVG so the item never renders the data twice.
- **Q9** was not listed in `_map.md`. The y-scale is 0–30 (unlike the 0–65 sibling fish graphs). Wavy-lined blenny sits on the 0 line for January, April, and July — the absence the correct answer (A) names. Cocos frillgoby peaks at 10 in April; Indo-Pacific sergeant runs from 2 (January) to 28 (October).
- **Q11** bars were read off the 5-unit gridlines on `page-11.png`. The axis includes −5 because Mexico’s Pre-FTA bar is the only negative one. Nicaragua’s Pre-FTA bar is the tallest (~23.6%), **not** 0%. Choice C quotes El Salvador’s Post-FTA rate as "about 21.8 percent", which matches the measured bar. Nicaragua is the one country whose Pre-FTA bar is taller than its Post-FTA bar — the relationship the correct answer (B) depends on. Same College Board figure as `2025-march-int-b` Q11 (choice order is rotated).
- **Q12** table cells match the known values EET 268/171 and EHP 282/436 (same table as `2025-march-int-a` Q11 / `2025-march-int-b` Q13 / `2025-march-int-c` Q13).
- No other Eng M1 page (1–8, 10, 13–27) has a table, graph, or diagram.

## Verification notes

- Every page image `page-01.png` … `page-27.png` was read individually with the Read tool. Ignore EliteXSAT watermarks and red spell-check squiggles. Blue-highlighted choices on some pages are the test-taker’s selections, not the key. Every `correctAnswer` comes from the PDF key string `ABBBD BDCAC BDCCC DCCDA BADCA DD` for form 202503亚太E M1.
- Underlined targets (rendered with `<u>…</u>`): **Q4 only** (`cheating` in the Joy Luck Club passage). No other Eng M1 item has a Bluebook content underline.
- Italicized titles and scientific names (The Joy Luck Club, The Argonautica, Empire of the Sun, Utopia, If I Ran the Zoo, The Spire of the Church of Our Lady, Fifty Days at Ilium, Lophiodes monodi, Mustelus canis, Tyrannosaurus, Leptecophylla tameiameiae, Passiflora suberosa) are stored as plain text, following the `2025-march-int-a` / `-b` / `-c` / `-d` convention.
- Q5 italicizes *him* at the end of the Eliot sentence on some SAT printings; it is stored as plain text here, matching `2025-march-int-d` Q7.
