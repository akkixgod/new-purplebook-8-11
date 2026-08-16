# Math Module 2 — Figure specs (2025-march-int-a)

SVGs to create under `public/mocks/2025-march-int-a/figures/`.
All coordinates are in figure units; use a clean black-on-white College Board style
(1px strokes, serif italic variable labels, no color).

| Q | SVG path | Description |
|---|----------|-------------|
| 1 | `math2-q01-ball-height.svg` | Downward parabola, height vs. time, marked point (1.0, 3.9) |
| 4 | `math2-q04-similar-triangles.svg` | Right triangle ACE with segment BD parallel to base AE |
| 12 | `math2-q12-shaded-inequality.svg` | Shallow line through (−4, −10) and (0, −11), region above shaded |
| 17 | `math2-q17-exponential-graph.svg` | Reflected exponential `y = −5^x + 5`, intercepts (0, 4) and (1, 0) |

No other Module 2 item has a visual: Q3, Q6, Q13, Q14, Q19 and Q21 present their
equations as plain text (written inline at the top of `text` in `_math2.json`), and no item
in this module uses a table or a scatterplot.

---

## Q1 — `math2-q01-ball-height.svg` (page 76)

Downward-opening parabola on a light grid, showing height above ground versus time.

- **viewBox** roughly `0 0 360 320` (plot area square-ish, taller than wide is fine)
- **x-axis**: label **Time (seconds)** centered below the axis; ticks and labels at
  1, 2, 3; `O` at the origin; arrowhead and italic `x` to the right of the last tick
- **y-axis**: label **Height above ground (meters)** rotated 90° along the left side;
  ticks and labels at 1, 2, 3, 4, 5, 6, 7; arrowhead and italic `y` on top
- **Grid**: thin gray lines at every integer x (1, 2, 3) and every integer y (1…7) —
  in the original only the integer gridlines are drawn, not a fine unit grid
- **Curve**: thick black parabola opening downward
  - y-intercept at about `(0, 2.8)`
  - vertex at about `(0.65, 4.6)`
  - passes through `(1.0, 3.9)`
  - reaches the x-axis at about `x = 1.55`, where the curve stops
  - (a good fit is `y ≈ −7.3(x − 0.65)² + 4.6`)
- **Marked point**: filled black dot at `(1.0, 3.9)`, no coordinate label on the figure
- **No watermark**
- **Answer note**: x is time and y is height → at 1.0 s the height is 3.9 m (**A**)

## Q4 — `math2-q04-similar-triangles.svg` (page 79)

Two nested right triangles sharing vertex C, drawn taller than wide.

- **viewBox** roughly `0 0 300 340`
- **Vertices** (screen coordinates, y down):
  - `A` bottom-left, e.g. `(60, 300)` — italic label below-left
  - `E` bottom-right, e.g. `(230, 300)` — italic label below-right
  - `C` top, directly above `E`, e.g. `(230, 40)` — italic label above
  - `D` on segment `CE`, e.g. `(230, 170)` — italic label to the right
  - `B` on segment `AC`, level with `D`, e.g. `(145, 170)` — italic label to the left
- **Segments drawn**: `A→E` (horizontal base), `E→C` (vertical right side),
  `A→C` (the long hypotenuse rising left-to-right through `B`), and `B→D` (horizontal)
- **Right-angle markers**: small open squares at `E` (interior of angle AEC) and at
  `D` (interior of angle BDC) — both are drawn on the left side of the vertical segment
- No side lengths or angle measures are printed on the figure (56° and AE = 24(BD)
  appear only in the stem)
- Caption centered below the figure: *Note: Figure not drawn to scale.*
- **Answer note**: CAE ~ CBD pairs A with B, so angle CAE = angle CBD = 56° (**B**)

## Q12 — `math2-q12-shaded-inequality.svg` (page 87)

Third-quadrant grid with a shallow negative-slope boundary line and the region above it
shaded.

- **viewBox** roughly `0 0 340 380`
- **x-axis**: drawn at `y = 0` across the top of the plot; ticks and labels at
  −10, −8, −6, −4, −2 with `O` at the origin; arrowhead and italic `x` to the right
- **y-axis**: drawn at `x = 0` near the right edge; ticks and labels at
  −2, −4, −6, −8, −10, −12, −14; arrowhead and italic `y` on top
- **Plot extent**: x from about −10.5 to 1, y from about −15.5 to 0.5
- **Grid**: thin black gridlines every 1 unit in both directions (the original uses a
  visible dark-gray unit grid, not a faint one)
- **Boundary line**: solid thick black, `y = −x/4 − 11`, drawn across the full plot
  (from about `(−10.5, −8.4)` to `(1, −11.25)`)
- **Marked points**: filled black dots at `(−4, −10)` and `(0, −11)`
- **Shaded region**: everything **above** the line (`x + 4y ≥ −44`), filled solid
  medium gray (~`#b8b8b8`) at full opacity with the gridlines still visible on top,
  clipped to the plot box
- **No watermark**
- **Answer note**: line is `x + 4y = −44` → r = 1, t = 4, r + t = 5 (**D**)

## Q17 — `math2-q17-exponential-graph.svg` (page 91)

Reflected exponential curve falling steeply to the right.

- **viewBox** roughly `0 0 360 320`
- **x-axis**: ticks and labels at −1, 1, 2, 3, 4, 5 with `O` at the origin;
  arrowhead and italic `x` to the right
- **y-axis**: ticks and labels at −4, −2, 2, 4, 6, 8, 10; arrowhead and italic `y` on top
- **Plot extent**: x from about −1.5 to 5.5, y from about −5 to 11
- **Grid**: thin gray lines every 1 unit in x and every 1 unit in y (labels every 2 units)
- **Curve**: thick black graph of `y = −5^x + 5`
  - approaches the horizontal asymptote `y = 5` from below as x decreases (at the left
    edge it is nearly flat, just under y = 5)
  - passes through `(0, 4)` and `(1, 0)`
  - falls steeply off the bottom of the plot just past `x = 1.5`
  - no asymptote line is drawn in the original
- No points are marked with dots in the original
- **No watermark**
- **Answer note**: graph is `y = f(x) + 2 = −5^x + 5` → `f(x) = −5^x + 3` (**B**)

---

## Missing questions

| Q | Status |
|---|--------|
| 16 | MISSING — no page image in the source capture |
| 22 | MISSING — no page image in the source capture |

Both are stubbed in `_math2.json` with `"_missing": true`,
`"text": "PLACEHOLDER_MISSING_PAGE"`, and `choices` / `correctAnswer` set to `null`.
**Do not seed these into the DB until they are filled** from another copy of the paper.

## Blocked question — Q14

Q14 (page 89) is present but **not fully readable**, so it has no key. It is stubbed with
`"_illegible": true` and `"correctAnswer": null`, and its `text` carries the literal
marker `ILLEGIBLE_EXPONENT` in place of the exponent on `t`:

```
⁷√(p^4) = t^(ILLEGIBLE_EXPONENT)
In the given equation, p > 1 and t > 1. If t = p^(2n − 1), where n is a constant,
what is the value of n?
```

- The embedded source image for page 89 is only 1190×804 px (the smallest of the whole
  module). The fractional exponent on `t` occupies about 6×20 px in total, i.e. roughly
  5×4 px per digit, which is below the threshold where digits can be told apart.
- Rendering the PDF page at higher scale does not help — 1190×804 is the native size of
  the embedded screenshot, so there is no additional detail to recover. Nearest-neighbour,
  bicubic, Lanczos and unsharp-mask renderings plus a raw pixel dump were all tried.
- What **is** legible: the radical index **7**, the radicand **p⁴**, and the full stem
  including `t = p^(2n − 1)`.
- Because `n = 1/2 + 2b/(7a)` for an exponent of `a/b`, every candidate reading yields a
  different key (e.g. 4/7 → n = 1; 4/6 → n = 13/14; 4/5 → n = 6/7; 1/6 → n = 31/14), so
  the answer cannot be pinned down. **Do not seed Q14 until the exponent is confirmed.**

## Verification / transcription notes

- The PDF contains **no math answer key** — page 97 holds only the Reading & Writing keys
  (27 items per module, letters only) for versions 亚太A–亚太E. Every `correctAnswer` in
  `_math2.json` was therefore solved from the item itself, and each entry carries a
  `showWork` field with the derivation.
- Page map used (question → PDF page): 1→76, 2→77, 3→78, 4→79, 5→80, 6→81, 7→82, 8→83,
  9→84, 10→85, 11→86, 12→87, 13→88, 14→89, 15→90, 16→MISSING, 17→91, 18→92, 19→94,
  20→95, 21→96, 22→MISSING.
- Page 93 is a duplicate capture of the Q18 screen (page 92); it was used to cross-check
  the transcription but maps to no new question.
- **Bottom edge cropped** on page 76: the capture ends just below choice C of Q1, so
  choice D is not in the source at all. It was reconstructed as the mirror of choice C
  (`initial height of 3.9 meters with an initial velocity of 1.0 meter per second`), the
  standard College Board pairing. Flagged in `_math2.json` as `_reconstructedChoiceD`.
  The key (A) is read straight off the graph and is unaffected.
- **Right edge cropped** on page 94 (Q19): the stem ends at `…the sum of the solutions to
  the equation` and the stated sum is clipped away. The value **9** was recovered from the
  test-taker's Desmos panel, which is still visible on pages 94–96 and shows
  `13/4 − 9 = −5.75`, `(13/4 − 9)·4 = −23`, and `y = 7x²(4x − 13)(4x − u)`. Sum = 9 gives
  u = 23 (positive, as the stem requires); sum = −9 would give u = −49 and contradict the
  stem. Flagged as `_reconstructedValue`.
- Pages 94, 95 and 96 were re-extracted from the PDF at their native embedded resolution
  (1736×960, 1720×1002, 1728×978) rather than read from the 2× page renders, which
  recovered the full Q20 stem and confirmed the `f(x) = ab^(x/n)` exponent in Q21.
- Q12's boundary line was confirmed at 3× zoom to pass exactly through the two marked
  dots `(−4, −10)` and `(0, −11)`, fixing r = 1 and t = 4 uniquely against the constant
  −44 in the stem.
- Q17's graph was confirmed at 4× zoom to have y-intercept `(0, 4)` and x-intercept
  `(1, 0)`, which distinguishes choice B from the other three.
- Q7 (page 82) and Q17 (page 91) show the test-taker's own selection highlighted (B in
  both cases); both agree with the independently derived keys.
