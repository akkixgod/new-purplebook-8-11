# Math Module 1 — Figure specs (2025-march-int-a)

SVGs to create under `public/mocks/2025-march-int-a/figures/`.
All coordinates are in figure units; use a clean black-on-white College Board style
(1px strokes, serif italic variable labels, no color).

| Q | SVG path | Description |
|---|----------|-------------|
| 2 | `math1-q02-right-triangle.svg` | Right triangle, hypotenuse 20, vertical leg 8, base b |
| 3 | `math1-q03-histogram.svg` | Histogram of 20 lengths, 5 bins of width 50 |
| 8 | `math1-q08-scatterplot.svg` | Scatterplot in QII with line of best fit |
| 13 | `math1-q13-transversal.svg` | Transversal k crossing vertical lines r and s, angles w/x/y/z |
| 21 | `math1-q21-cone.svg` | Right circular cone, apex A, point B on base circumference |

Questions 12 and 16 present **tables as the answer choices**, so they carry no
`imageUrl`; the table content is written as compact pipe/colon text inside each choice
string (see `_math1.json`). No other Module 1 item has a visual.

---

## Q2 — `math1-q02-right-triangle.svg` (page 56)

Right triangle with the right angle at the **bottom-right** vertex.

- Vertices: bottom-left `(0, 0)`, bottom-right `(200, 0)`, top-right `(200, 150)`
- Sides
  - Hypotenuse from bottom-left to top-right — label **20** placed above the middle of
    the hypotenuse, offset up-left
  - Vertical right leg — label **8** placed to the right of its midpoint
  - Horizontal base — label **b** (italic) placed below its midpoint
- Small filled square right-angle marker at the bottom-right vertex
- Caption centered below the figure: *Note: Figure not drawn to scale.*

## Q3 — `math1-q03-histogram.svg` (page 57)

Histogram, gray-filled bars with dark gray outlines, bars touching (no gaps).

- **x-axis**: "Length (feet)", ticks and labels at 0, 50, 100, 150, 200, 250
- **y-axis**: "Frequency" (rotated 90°), 0–5, ticks and labels at 0, 1, 2, 3, 4, 5;
  short tick marks on the right-hand edge of the plot as well (as in the original)
- **Bars** (left edge → frequency)
  - 0–50 → **5**
  - 50–100 → **3**
  - 100–150 → **4**
  - 150–200 → **3**
  - 200–250 → **5**
- Total frequency = 20, which matches the stem
- **Answer note**: the maximum length falls in the last bin (200 ≤ length < 250) → **219** (D)

## Q8 — `math1-q08-scatterplot.svg` (page 60)

Scatterplot confined to the second quadrant, with a solid line of best fit.

- **Axes**
  - x-axis: −14 to 0, labeled −14, −12, −10, −8, −6, −4, −2 and `O` at the origin;
    arrowhead and italic `x` label to the right of the origin
  - y-axis: drawn at x = 0, labeled 2, 4, 6, …, 20; arrowhead and italic `y` label on top
  - Light gray grid lines every 2 units in both directions; plot box spans x ∈ [−14, 0],
    y ∈ [2, 20]
- **Line of best fit**: solid black, from `(−14, 16.3)` to `(0, 2.3)` (slope −1)
- **6 data points** (filled black circles, approximate positions):
  - `(−14, 16)`, `(−11.8, 14)`, `(−9.8, 12.7)`, `(−8, 11)`, `(−5.8, 9)`, `(−4, 5.4)`
- **Answer note**: negative slope ≈ −1 with y-intercept ≈ 2.3 → **y = −x + 2.3** (D)

## Q13 — `math1-q13-transversal.svg` (page 66, duplicate on page 67)

Two parallel-looking vertical lines cut by a transversal falling left-to-right.

- **Line r**: vertical segment at x = 120, from y = 20 down to y = 300; italic label **r**
  above the top end
- **Line s**: vertical segment at x = 260, from y = 20 down to y = 300; italic label **s**
  above the top end
- **Line k**: straight segment from `(50, 40)` to `(330, 320)` (slope +1 in screen
  coordinates, i.e. going down and to the right); italic label **k** near its upper-left end
- Intersections: k × r at `(120, 110)`; k × s at `(260, 250)`
- **Angle labels** (italic letter followed by a degree symbol), all placed on the
  **right** side of the vertical line they belong to:
  - **w°** just above-right of `(120, 110)`
  - **x°** just below-right of `(120, 110)`
  - **y°** just above-right of `(260, 250)`
  - **z°** just below-right of `(260, 250)`
- Caption centered below the figure: *Note: Figure not drawn to scale.*
- **Answer note**: w° and y° are corresponding angles → r ∥ s iff y = w = 160 (**B**)

## Q21 — `math1-q21-cone.svg` (page 74)

Right circular cone seen slightly from above, drawn as a wide shallow "fan".

- **Apex A**: filled dot at the top, italic label **A** just above it
- **Base**: ellipse centered below the apex, wide and flat (semi-major axis ≈ 4× the
  semi-minor axis). Draw the **front half of the ellipse as a solid arc** and the
  **back half as a dashed arc** (hidden edge).
- **Slant edges**: two solid straight segments from the apex to the far-left and
  far-right ends of the ellipse's major axis
- **Point B**: filled dot on the **left** portion of the base circumference (on the
  visible front arc, near the left slant edge), italic label **B** just below-left of it
- Do **not** draw segment AB — the stem says it is not shown
- No dimension labels on the figure (32 cm, 16 cm, and kπ appear only in the stem)
- Caption centered below the figure: *Note: Figure not drawn to scale.*
- **Answer note**: AB is the slant height → r² = 32² − 16² = 768; V = (1/3)π(768)(16) =
  4,096π → **k = 4096**

---

## Missing questions

| Q | Status |
|---|--------|
| 4 | MISSING — no page image in the source capture |
| 7 | MISSING — no page image in the source capture |
| 17 | MISSING — no page image in the source capture |

Each is stubbed in `_math1.json` with `"_missing": true`,
`"text": "PLACEHOLDER_MISSING_PAGE"`, and `choices` / `correctAnswer` set to `null`.
**Do not seed these into the DB until they are filled** from another copy of the paper.

## Verification / transcription notes

- The PDF contains **no math answer key**, so every `correctAnswer` in `_math1.json` was
  solved from the item itself; each entry carries a `showWork` field with the derivation.
- Page map used (question → PDF page): 1→55, 2→56, 3→57, 4→MISSING, 5→58, 6→59,
  7→MISSING, 8→60, 9→61, 10→62, 11→63, 12→65, 13→66, 14→68, 15→69, 16→70, 17→MISSING,
  18→71, 19→72, 20→73, 21→74, 22→75.
- Page 64 shows only the scrolled-down choices B–D of Q12; page 67 is a duplicate of the
  Q13 screen. Both were used to cross-check but map to no new question.
- **Right edge cropped in the source capture** for Q18 (page 71) and Q21 (page 74): the
  screen recording cuts off the last few words of each wrapped line. The visible text was
  transcribed exactly and the clipped fragments were reconstructed to the standard
  College Board phrasing ("…22 trees. Each sample of wood was cut…", "…this cube, in
  grams?", "…of the base, and the length of segment AB…", "…what is the value of k?").
  The numbers (22, 3.000, 0.250, 32, 16, kπ) are all fully legible, so the answers
  6.75 and 4096 are unaffected.
- Q16's exponent was confirmed at 5× zoom as f(x) = 24(2)^(x/6), consistent with the
  values in choice B.
- Q3's bar heights were confirmed at 3× zoom as 5, 3, 4, 3, 5 (sum 20, matching the stem).
