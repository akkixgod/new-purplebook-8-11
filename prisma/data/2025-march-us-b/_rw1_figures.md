# RW Module 1 figures — 2025-march-us-b

Two questions in Reading & Writing Module 1 carry a visual (both line graphs).
All other items (Q1–Q9, Q12–Q27) are text-only and have `imageUrl: null`.

| Q | SVG path | Description |
|---|----------|-------------|
| 10 | `public/mocks/2025-march-us-b/figures/eng1-q10-forest-patches.svg` | Line graph: **Annual Mean Forest Patch Size for Three Land Use Capability Classes in the Chorotega Region, Costa Rica**. y-axis "Mean patch size (hectares)", ticks 0–150 by 25. x-axis "Year": 1960, 1979, 1986, 2000. Legend: Class VIII (cannot be used for commercial crops) = solid black line + filled triangles; Class VI (severe limitations on use for crops) = dashed gray line + open squares; Class VII (very severe limitations on use for crops) = dotted black line + open circles. Values (1960, 1979, 1986, 2000): Class VIII 125 / 125 / 38 / 61; Class VI 67 / 77 / 20 / 35; Class VII 76 / 87 / 28 / 49. All three series sit between 0 and 50 ha in 1986 — the range the correct answer (D) names. |
| 11 | `public/mocks/2025-march-us-b/figures/eng1-q11-fish-population.svg` | Line graph: **Fish Population in a Taiwanese Tide Pool, January 2001 to October 2001**. y-axis "Number of individual fish observed", ticks 0–65 by 5. x-axis "Month": January 2001, April 2001, July 2001, October 2001. Legend: combtooth blenny = solid black line + filled triangles; barred flagtail = dashed gray line + open squares; striated rockskipper = dotted black line + open circles. Values (Jan, Apr, Jul, Oct): combtooth blenny 62 / 3 / 3 / 1; barred flagtail 14 / 9 / 7 / 16; striated rockskipper 0 / 0 / 5 / 4. Striated rockskipper sits on the 0 line in January and April — the absence the correct answer (B) names. |

## Figure notes

- Stimuli for Q10 and Q11 in `_rw1.json` hold only the surrounding prose; chart title/axes/legend live solely in the SVG so the item never renders the data twice.
- **Q10** points were read off the 25-hectare gridlines on `page-11.png`. The 1986 dip is the visual the assertion ("had dropped considerably. In that year, they were between ______") depends on: all three classes fall between 0 and 50 ha (Class VIII ≈ 38, Class VII ≈ 28, Class VI ≈ 20). Same College Board figure family as `2025-june-us-b` Eng M1 Q13 (different stem/choices).
- **Q11** points were read off the 5-unit gridlines on `page-12.png`. The y-scale is 0–65 (unlike the 0–30 sibling in `2025-march-int-e` Q9). Combtooth blenny peaks at 62 in January; barred flagtail is present in every month; striated rockskipper is the species at 0 in January and April. Same College Board figure family as `2026-march-int-c` Eng M1 Q12 (same stem/choices).
- No other Eng M1 page (1–10, 13–28) has a table, graph, or diagram. Skip p07 (duplicate of Q6).

## Verification notes

- Every canonical page image was read individually with the Read tool (Q1→p01 … Q6→p06, Q7→p08 … Q27→p28). Ignore EliteXSAT watermarks and red spell-check squiggles. Blue-highlighted choices on some pages are the test-taker’s selections, not the key. There is no answer-key sheet in this PDF; every `correctAnswer` was solved from the item.
- Underlined targets (rendered with `<u>…</u>`): **none** in Eng M1. No Bluebook content underlines on these 27 items.
- Italicized titles and scientific names (Agnes Grey, Guy de Maupassant Short Stories, Bread, The Warmth of Other Suns, Acoustic Soul, Voyage to India, Alf’s Button, Forever and a Day, Kiesler and Wife, Pseudonestor xanthophrys, Leptoptilos dubius) are stored as plain text, following the `2025-march-int-a` / `-b` / `-c` / `-d` / `-e` / `2025-march-us-a` convention.
