# RW Module 1 figures — 2025-march-us-a

Two questions in Reading & Writing Module 1 carry a visual (one table, one bar graph).
All other items (Q1–Q11, Q13, Q15–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 12 | `public/mocks/2025-march-us-a/figures/eng1-q12-productivity-loss.svg` | Table: **Average Monetized Productivity Loss at Two Points After Programs Began, in Australian Dollars**. Columns: Type of training, 12 weeks, 12 months. Rows: EET (268, 171); EHP (282, 436). Copied from Int-E Eng M1 Q12 (`_filledFrom`). |
| 14 | `public/mocks/2025-march-us-a/figures/eng1-q14-fta-export-growth.svg` | Grouped bar graph: **Average Total Agricultural Export Growth Rate, Five Years Pre- and Post-FTA with the United States**. y-axis "Growth rate (%)", ticks −10 to 40 by 5. x-axis "Export growth" with groups "Pre-FTA" and "Post-FTA". Legend: Costa Rica (CAFTA-DR) = dark gray, Jordan (JOFTA) = light gray, Morocco (MAFTA) = black. Values — Pre-FTA: Costa Rica ≈ 10, Jordan ≈ −5 (only negative bar), Morocco ≈ 20; Post-FTA: Costa Rica ≈ 13.5, Jordan ≈ 37, Morocco ≈ 5. |

## Figure notes

- Stimuli for Q12 and Q14 in `_rw1.json` hold only the surrounding prose; table title/cells and chart title/axes/legend live solely in the SVG so the item never renders the data twice.
- **Q12** is filled from `2025-march-int-e/_rw1.json#12` (source PDF missing this page). The SVG is copied from Int-E; cells match the known values EET 268/171 and EHP 282/436. Key **D**.
- **Q14** bars were read off the 5-unit gridlines on `page-13.png`. The axis includes −10 because Jordan’s Pre-FTA bar is the only negative one. Choice C quotes Costa Rica’s Post-FTA rate as "about 13.5 percent", which matches the measured bar. Morocco is the one country whose Pre-FTA bar (~20%) is taller than its Post-FTA bar (~5%) — the relationship the correct answer (D) depends on.
- No other Eng M1 page has a table, graph, or diagram. Q16 and Q21 are text-only fills from Int-E.

## Verification notes

- Every available page image was read individually with the Read tool (canonical map: Q1→p01 … Q11→p11, Q13→p12, Q14→p13, Q15→p14, Q17→p15 … Q20→p18, Q22→p19 … Q26→p23, Q27→p101). Ignore EliteXSAT watermarks and red spell-check squiggles. Blue-highlighted choices on some pages are the test-taker’s selections, not the key. Every `correctAnswer` was solved from the item; there is no key sheet in this PDF.
- Underlined targets (rendered with `<u>…</u>`): **Q1** (`place`), **Q5** (`manifest`), **Q11** (the student claim: people usually spend more time viewing a work of art in a museum than they do online.), **Q15** (the Violeta Parra claim sentence about musical traditions expanding beyond Chile).
- Italicized titles and scientific names (Never Look Back, Night and Day, The Lair of the White Worm, Saint Sebastian’s Abyss, Poems, Fifty Days at Iliam, Dos Mujeres, Vagabonds, Agaricus bisporus, Ganoderma lucidum, Clermontia kakeana, Ardisia elliptica) are stored as plain text, following the `2025-march-int-a` / `-b` / `-c` / `-d` / `-e` convention.
- Fills: Q12 from Int-E Eng M1 Q12 (productivity table, key D); Q16 from Int-E Eng M1 Q16 (Moscow “city that”, key D); Q21 from Int-E Eng M1 Q22 (Ethiopia/Cuba “By contrast,”, key A).
