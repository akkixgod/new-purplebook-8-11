# RW Module 1 figures — 2025-march-int-d

Two questions in Reading & Writing Module 1 carry a visual (one table, one bar graph).
All other items (Q1–Q10, Q12, Q14–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 11 | `public/mocks/2025-march-int-d/figures/eng1-q11-copper-mined.svg` | Table: **Millions of Metric Tons of Copper Mined in 1995 and 2020**. Columns: Country, 1995, 2020. Rows: Mexico (0.33, 0.73); United States (1.85, 1.20); Peru (0.38, 2.15); Poland (0.38, 0.39). |
| 13 | `public/mocks/2025-march-int-d/figures/eng1-q13-story-rating.svg` | Grouped bar graph: **Story Rating: Spoiled vs. Unspoiled**. y-axis "Average enjoyment rating (1 = lowest; 10 = highest)", ticks 0–8 by 1. x-axis "Story". Legend: unspoiled (light gray), spoiled (dark). Values (unspoiled, spoiled): "A Dark Brown Dog" (3.5, 4.6); "Owl Creek Bridge" (4.9, 5.1); "Blitzed" (6.2, 7.1); "A Chess Problem" (6.1, 7.2); "The Calm" (4.3, 5.0); "Plumbing" (4.1, 4.9). Category labels are rotated and appear in quotation marks. |

## Figure notes

- Q11 and Q13 stimuli in `_rw1.json` contain only the surrounding prose; the table title and
  cells, and the chart title/axes/legend, live solely in the SVG so the item does not render
  the data twice.
- Q11 table cells were read from `page-10.png` (left pane). Peru is 0.38 (1995) → 2.15 (2020),
  which is the pair the correct answer (C) quotes. Mexico 0.73, Poland 0.39, and the United
  States 1.20 are the 2020 distractors in A, B, and D.
- Q13 is the same College Board story-rating figure used as `2025-march-int-a` Q12 (choice
  order is rotated; the key here is A). Bar heights were read off 1-unit gridlines on
  `page-12.png`. Each pair shows spoiled higher than unspoiled, with the smallest gap at
  "Owl Creek Bridge" (≈0.2) and among the largest at "A Chess Problem" (≈1.1), which is what
  the correct answer depends on.
- No other Eng M1 page (1–9, 11, 13–26) has a table, graph, or diagram.

## Verification notes

- Every page image `page-01.png` … `page-05.png` and `page-06.png` … `page-26.png` was read
  individually with the Read tool (Q6 has no page in this capture). Blue-highlighted choices
  are the test-taker’s selections, not the key. Every `correctAnswer` except Q6 comes from the
  PDF key string `DBAAC 空DDBA CAACA BDDAD DDDBC BD` for form 202503亚太D.
- **Q6** is missing from the PDF. Filled with the words-in-context blank from
  `2025-march-int-a` RW M1 Q1 (Apollo / “ongoing”), marked `_filledFrom`, key **A**.
- Underlined targets (rendered with `<u>…</u>`): **none** in this module. Q7 italicizes
  *him* at the end of the Eliot sentence; that is stored as plain text, following the
  `2025-march-int-a` / `-b` / `-c` convention.
- Italicized titles and scientific names (Embrace, Apatosaurus, The Time in Between,
  Without a Whisper—Konnon:Kwe, On Earth We’re Briefly Gorgeous, Psydrax odorata,
  Cestrum nocturnum) are stored as plain text.
- Q27 is the only notes item without the “While researching a topic…” lead-in; the page
  shows the bulleted sentences alone, matching the stem’s wording “from the given sentences”.
- Choice-order differences vs. sibling forms are real: e.g. Q5 “expected by” is C here but
  A in `2025-march-int-a` Q4; Q13’s correct pair is A here but B in `2025-march-int-a` Q12.
