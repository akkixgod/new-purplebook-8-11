# RW Module 1 figures — 2025-march-int-a

Three questions in Reading & Writing Module 1 carry a visual (two tables, one bar graph).
All other items (Q1–Q8, Q10, Q13–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 9 | `public/mocks/2025-march-int-a/figures/eng1-q09-copper-mined.svg` | Table: **Millions of Metric Tons of Copper Mined in 1995 and 2020**. Columns: Country, 1995, 2020. Rows: Indonesia (0.44, 0.51); United States (1.85, 1.20); Kazakhstan (0.26, 0.55); Chile (2.49, 5.73). |
| 11 | `public/mocks/2025-march-int-a/figures/eng1-q11-productivity-loss.svg` | Table: **Average Monetized Productivity Loss at Two Points After Programs Began, in Australian Dollars**. Columns: Type of training, 12 weeks, 12 months. Rows: EET (268, 171); EHP (282, 436). |
| 12 | `public/mocks/2025-march-int-a/figures/eng1-q12-story-rating.svg` | Grouped bar graph: **Story Rating: Spoiled vs. Unspoiled**. y-axis "Average enjoyment rating (1 = lowest; 10 = highest)", ticks 0–8 by 1. x-axis "Story". Legend: unspoiled (light gray), spoiled (dark). Values (unspoiled, spoiled): "A Dark Brown Dog" (3.5, 4.6); "Owl Creek Bridge" (4.9, 5.1); "Blitzed" (6.2, 7.1); "A Chess Problem" (6.1, 7.2); "The Calm" (4.3, 5.0); "Plumbing" (4.1, 4.9). Category labels are rotated and appear in quotation marks. |

## Figure notes

- Q9 and Q11 stimuli in `_rw1.json` contain only the surrounding prose; the table title and
  cells live solely in the SVG so the item does not render the data twice.
- Q12's stimulus likewise holds only the researcher prose; the chart title, axis labels, and
  legend belong in the SVG.
- Bar values for Q12 were read off gridlines at 1-unit spacing on an upscaled crop of
  `page-12.png`; each pair shows spoiled higher than unspoiled, with the smallest gap at
  "Owl Creek Bridge" (≈0.2) and among the largest at "A Chess Problem" (≈1.1), which is what
  the correct answer (B) depends on.

## Verification notes

- Every page image `page-01.png` … `page-27.png` was read individually; OCR text under
  `_ocr/` was used only as a hint and was wrong or truncated in several places (e.g. it drops
  "more" in Q2/Q5/Q23, misreads *1Q84* as "1984" in Q15, and omits whole choice lines).
- Underlined targets (rendered with `<u>…</u>`) appear in Q2 ("cheating"), Q7 (the entire
  first sentence, through "a species of fish."), and Q10 (the claim beginning "Bianchini used
  trigonometry…").
- Q8 choice D reads "stimulants" (not "simulants") on the page; the typo is preserved.
