# Math Module 1 — Figure specs (2025-march-int-b)

Only two Module 1 items carry a stem figure. Both SVGs already exist under
`public/mocks/2025-march-int-b/figures/`; they use the same clean black-on-white
College Board style as the `2025-march-int-a` figures (2px strokes, Georgia italic
labels, no color).

| Q | SVG path | Description |
|---|----------|-------------|
| 8 | `math1-q08-similar-triangles.svg` | Nested right triangles CAE and CBD sharing vertex C |
| 21 | `math1-q21-cone.svg` | Right circular cone, apex A, point B on the base circumference |

All other items are text-only (`imageUrl: null`). Questions **3**, **11** and **16**
present their answer choices *as* graphs or tables, so they carry no `imageUrl`
either — the choice content is written as compact text inside each choice string,
following the `2025-march-int-a` Q12/Q16 convention. This keeps the "no double
visuals" rule: nothing that lives in an SVG is repeated as text, and nothing that
lives in a choice string is duplicated as a figure.

---

## Q8 — `math1-q08-similar-triangles.svg` (page 61)

Two nested right triangles sharing the vertex C, drawn with the right angle on the
right-hand side.

- Vertices: **A** bottom-left `(60, 300)`, **E** bottom-right `(230, 300)`,
  **C** top-right `(230, 40)`
- Sides: base A→E, vertical right side E→C, hypotenuse A→C
- **B** sits on the hypotenuse at `(145, 170)`; **D** sits on the vertical side at
  `(230, 170)`; segment BD is horizontal, so triangle CBD nests inside triangle CAE
- Small open square right-angle markers at **E** (angle AEC) and at **D** (angle BDC)
- Italic labels A, E, C, D outside the figure; B just left of the hypotenuse
- Caption centered below: *Note: Figure not drawn to scale.*
- **Answer note**: CAE ~ CBD pairs angle CAE with angle CBD, so angle CAE = 59° (**C**).
  The ratio AE = 28(BD) is scale information only and does not affect any angle.

This is geometrically identical to `2025-march-int-a`'s
`math2-q04-similar-triangles.svg`, so the SVG was copied with the slug and filename
swapped.

## Q21 — `math1-q21-cone.svg` (page 75)

Right circular cone seen slightly from above, drawn as a wide shallow "fan".

- **Apex A**: filled dot at `(180, 50)`, italic label **A** just above-right
- **Base**: ellipse centered `(180, 220)` with `rx = 120`, `ry = 28`. The full ellipse
  is dashed (hidden back edge) and the **front (lower) half is overdrawn solid**.
- **Slant edges**: solid segments from the apex to `(60, 220)` and `(300, 220)`
- **Point B**: filled dot at `(130, 243)` on the solid front arc, italic label **B**
  just below-left
- Segment AB is **not** drawn — the stem says it is not shown
- No dimension labels on the figure (84 cm, 42 cm and kπ appear only in the stem)
- Caption centered below: *Note: Figure not drawn to scale.*
- **Answer note**: AB is the slant height → r² = 84² − 42² = 5,292;
  V = (1/3)π(5,292)(42) = 74,088π → **k = 74088**

---

## Choice-as-visual items (no `imageUrl`)

### Q3 (page 56) — four coordinate graphs, **two of them never captured**

Grid style for all choices: gridlines every 1 unit, x roughly −5 to 10, y roughly
−5 to 10, labels every 2 units, italic axis letters, `O` at the origin.

| Choice | What the capture shows |
|--------|------------------------|
| A | y = x and y = −x + 3; they intersect at (1.5, 1.5) |
| B | y = −x + 3 and a slope-1 line through about (2.75, 0); they intersect at roughly (3, 0). Only the part above y ≈ 3 is on screen. |
| C | **NOT CAPTURED** |
| D | **NOT CAPTURED** |

Page 56 is a screen recording that stops partway down choice B, and no later page
revisits the item. Since neither A nor B has its lines crossing at (3, 3), the key is
C or D and cannot be decided from this source. Q3 is therefore stored with
`"_incomplete": true`, `choices: null` and `correctAnswer: null`, with the two
observed graphs preserved under `_observedChoices`. **Do not seed Q3** until the
missing choices are filled from another copy of the paper.

### Q11 (page 64, continued on page 65) — four coordinate graphs

Grid style: x from 0 to 10 labeled every 1 unit, y from 0 to 5,000 labeled every 500.

| Choice | Graph |
|--------|-------|
| A | Upward-curving parabola arm from the origin through ≈(2, 670), (3, 1,500), (4, 2,650), (5, 4,160), exiting the top near x = 5.5 |
| B | Much flatter upward curve from the origin, ≈(5, 1,250), reaching 5,000 only at x = 10 (i.e. y ≈ 50x²) |
| C | Downward curve starting near (0, 4,500) and falling below 500 by about x = 4 |
| D | **NOT CAPTURED** (page 65 ends partway through choice C) |

Unlike Q3 this item is still decidable: y = 53πx² ≈ 166.5x² matches choice A point by
point (166, 666, 1,499, 2,664, 4,162 at x = 1…5, hitting 5,000 at x ≈ 5.5), and only
one choice can be correct, so **A** is the key regardless of what D shows.

### Q16 (page 70) — four two-row tables

Every choice uses the same x row (−4, 0, 4, 8) and differs only in the f(x) row:
A → 4, 0, 16, 32 · B → 4, 8, 16, 32 · C → −4, 8, 16, 32 · D → 4, 8, 16, 24.
Written as `"x: …\nf(x): …"` strings. **B** is the key.

---

## Missing questions

| Q | Status |
|---|--------|
| 1 | MISSING — no page image in the source capture |
| 3 | INCOMPLETE — stem captured, answer choices C and D missing (see above) |

Q1 is stubbed in `_math1.json` with `"_missing": true`,
`"text": "PLACEHOLDER_MISSING_PAGE"`, and `choices` / `correctAnswer` set to `null`.
The recording jumps straight from Reading & Writing Module 2 Q27 (page 54) to Math
Module 1 Q2 (page 55). **Do not seed Q1 or Q3 into the DB until they are filled.**

## Verification / transcription notes

- The PDF's only answer key is on page 100 and covers **Reading & Writing only**
  (27 answers per module, and its "202503亚太B M1" row matches `_rw1.json` exactly).
  There is no math key, so every `correctAnswer` here was solved from the item itself
  and each entry carries a `showWork` field with the derivation.
- Page map used (question → PDF page): 1→MISSING, 2→55, 3→56, 4→57, 5→58, 6→59,
  7→60, 8→61, 9→62, 10→63, 11→64 (choices continue on 65), 12→66, 13→67, 14→68,
  15→69, 16→70, 17→71, 18→72, 19→73, 20→74, 21→75, 22→76.
- Every page image `page-55.png` … `page-76.png` was read individually. The `_ocr/`
  drafts are badly garbled wherever the "EliteXSAT | Eljan Ahmadli" watermark crosses
  the text, so all small superscripts, radicals and fractions were re-checked on
  2.4–5× upscaled crops: Q10's exponents (7x⁶ − 14x²), Q14's radicals (2√10/7 and the
  four choices), Q15's slope (−1/2, not −1/4), Q16's exponent (x/4), Q17's angle
  (3π/4), Q19's exponents (t/11.69 vs t + 11.69), and Q20's fractions (−1/5 vs −8/5).
- Q6's list is semicolon-separated on the page ("3,810; 3,810; 3,530; 3,850; 3,550")
  and is transcribed that way.
- The recording shows the test taker's own entries on some screens — "21" typed for
  Q4 and choice C highlighted for Q20. Both agree with the solved answers and were
  used only as a cross-check, not as a key.
- Grid-in strings are scored by exact match. Q12 is stored as `3/8` (`.375` is
  equivalent), and Q22 as `188.6`; Bluebook would also accept the truncated `188.5`
  for Q22, which is noted on the item.
