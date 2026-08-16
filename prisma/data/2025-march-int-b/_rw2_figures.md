# RW Module 2 figures — 2025-march-int-b

**2 figures required.** Both are data tables attached to the module's quantitative-evidence
items (Q9 and Q12). All other questions in Reading & Writing Module 2 (pages 28–54) are
text-only.

| Q | SVG path | Description |
|---|----------|-------------|
| 9 | `/mocks/2025-march-int-b/figures/eng2-q09-coral-depths.svg` | Table "Minimum and Maximum Depths of Stony Coral Species in Caribbean and Indo-Pacific Waters" — 3 columns (Species, Minimum depth (meters), Maximum depth (meters)) × 4 species rows: *Acropora echinata* 8/25, *Astreopora expansa* 5/15, *Heliofungia fralinae* 3/27, *Scolymia lacera* 10/80 |
| 12 | `/mocks/2025-march-int-b/figures/eng2-q12-video-game-systems.svg` | Table "Home Video Game Systems of the 1970s and 1980s" — 4 columns (System, Manufacturer, System type, Approximate number of units sold worldwide) × 4 rows: ColecoVision/Coleco/console/2,000,000; Intellivision/Mattel/console/3,000,000; MSX/ASCII Corp./computer/4,000,000; Game & Watch/Nintendo/handheld/18,600,000 |

## Verification notes

- Every page image `page-28.png` … `page-54.png` was read individually as separate left-pane
  (passage) and right-pane (stem + choices) crops rendered at 5× scale, so the watermark
  ("EliteXSAT | Eljan Ahmadli") never obscured a transcribed word.
- Page PNGs were absent from the working tree (`public/mocks/*/pages/` is gitignored), so they
  were re-rendered from the source PDF with `scripts/pdf-ingest.py` before transcription.
- Table cell values for Q9 and Q12 were re-read at 11–12× zoom to disambiguate the scan's
  `8`/`B`-like glyphs; `Scolymia lacera` maximum depth is **80** and `Game & Watch` units are
  **18,600,000**.
- Per the no-double-visuals rule, `stimulus` for Q9 and Q12 holds only the surrounding prose
  (the sentence that ends in the blank); the table lives solely in the SVG.
- **No underlined targets** appear anywhere in this module, so no `<u>` markup is used. Q17–Q22
  are Standard-English convention items whose target is a `______` blank, and Q23–Q24 are
  transition items with the same blank form.
- Module boundary confirmed: page 27 is Module 1 Q27 (header "Section 1, Module 1: Reading and
  Writing"); page 28 is Module 2 Q1 (header "Section 1, Module 2: Reading and Writing"), so the
  mapping `page = 27 + q` holds across all 27 items.
- All 27 answer-key entries were cross-checked against the transcribed choice text and each key
  letter matches the defensibly correct option.
