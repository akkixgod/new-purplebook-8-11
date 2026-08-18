# RW Module 2 figures — 2025-march-us-a

**2 figures required.** Q9 is the stony-coral depth table; Q11 is the spoiled-vs-unspoiled
story-rating bar graph. Every other question in Reading & Writing Module 2 is text-only.

Canonical pages (first complete capture; PDF is an image-only EliteXSAT recording):

| Q | Page | notes |
|---|------|-------|
| 1 | 27 | Brown Corpus |
| 2 | 28 | Ederle / Rutkiewicz (dup p25) |
| 3 | 29 | swap lines (dup p26) |
| 4 | 30 | *Darlington* shipwreck microbes |
| 5 | 42 | Yung Wing underlined sentence |
| 6 | 43 | Florida Highwaymen / Al Black |
| 7 | 44 | Howards End dual text |
| 8 | 46 | John Crowley *Engine Summer* |
| 9 | 45 | coral depths table (dup p47) |
| 10 | 48 | Yupno time gestures |
| 11 | 49 | spoiled-story bar graph |
| 12 | 50 | piezoelectric harvesters |
| 13 | 51 | Ghisbain bumblebees |
| 14 | 52 | MFC silver nanoparticles |
| 15 | 53 | Titan methane / IPSL |
| 16 | 32 | emulsifier (dup p54) |
| 17 | 31 | Proto-Nilotic |
| 18 | 33 | Actors Gymnasium |
| 19 | 34 | Auerbach Great Exhibition |
| 20 | 55 | centaurs P/2019 LD2 |
| 21 | 35 | Dallas parks |
| 22 | 36 | Kyudo transition |
| 23 | 37 | Publius transition |
| 24 | 38 | notes slow TV |
| 25 | 39 | notes bat germination |
| 26 | 40 | notes modularity of mind |
| 27 | 41 | notes DLS 3D curing |

| Q | Page | SVG path | Description |
|---|------|----------|-------------|
| 9 | 45 | `/mocks/2025-march-us-a/figures/eng2-q09-coral-depths.svg` | Table “Minimum and Maximum Depths of Stony Coral Species in Caribbean and Indo-Pacific Waters” — 3 columns (Species, Minimum depth (meters), Maximum depth (meters)) × 4 species rows: *Agaricia grahamae* 20/115, *Acropora striata* 10/25, *Danafungia scruposa* 1/27, *Acropora anthocercis* 5/10. p47 is the same table (used to confirm the last row). |
| 11 | 49 | `/mocks/2025-march-us-a/figures/eng2-q11-story-rating.svg` | Grouped bars “Story Rating: Spoiled vs. Unspoiled.” Y-axis: Average enjoyment rating (1 = lowest; 10 = highest), ticks 0–8. X-axis: Story. Legend: unspoiled (light gray), spoiled (dark gray). Six stories: “A Dark Brown Dog” 3.5/4.6, “Owl Creek Bridge” 4.9/5.1, “Blitzed” 6.2/7.1, “A Chess Problem” 6.1/7.2, “The Calm” 4.3/5.0, “Plumbing” 4.1/4.9 (unspoiled/spoiled). |

Regenerate with `py -3 scripts/generate-figures-2025-march-us-a-rw2.py`.

Per the no-double-visuals rule, `stimulus` for Q9 and Q11 holds only the surrounding prose;
the table and graph exist solely as SVGs.

## Underlines

**Q5 (page 42) only.** The first-person memoir sentence about 1845 / New York is the
underlined target:

`<u>Little did I realize when in 1845 I wrote, while in the Morrison School, a composition on “An Imaginary Voyage to New York and up the Hudson,” that I was to see New York in reality.</u>`

The stem asks for the function of that underlined sentence in the text as a whole
(key C: it describes an event in Yung’s life that exemplifies a phenomenon). No other
item in this module uses an underline; Q16–Q21 are Standard English convention items
and Q22–Q23 are transition items whose target is a `______` blank.

## Answer key

No answer-key sheet in the PDF. Keys were solved from the items. Blue-highlighted
choices in the screenshots are the original test-taker’s selections and were ignored.

27-letter string: `ACADC AADBB AADCA ABCBD BABBC AC` (spaces for readability only).

| Q | Key | Q | Key | Q | Key |
|---|-----|---|-----|---|-----|
| 1 | A | 10 | B | 19 | B |
| 2 | C | 11 | A | 20 | D |
| 3 | A | 12 | A | 21 | B |
| 4 | D | 13 | D | 22 | A |
| 5 | C | 14 | C | 23 | B |
| 6 | A | 15 | A | 24 | B |
| 7 | A | 16 | A | 25 | C |
| 8 | D | 17 | B | 26 | A |
| 9 | B | 18 | C | 27 | C |

## Gaps and caveats

- **No missing pages.** All 27 Module 2 items have a canonical capture.
- **Q9 table** prefers p45; p47 is the same table and confirms *Acropora anthocercis* 5/10
  (the fourth row). Researcher is Hudson Pinheiro (not Luiz Rocha as on Int-E).
- **Q11 graph** is the same spoiled/unspoiled study as Int-A M1 / Int-D M1, with this
  form’s choice order matching Int-D (key A: smallest gap vs. largest gap).
- **Q7** keeps Text 1 / Text 2 labels. Choice order differs from Int-A (key A here =
  Int-A’s C).
- **Q5** choice B is unique to this form (“future difficulties in publishing”), not the
  June Int-B wording.
- Test-taker highlights were ignored (e.g. Q1 B, Q2 A, Q3 C, Q6 D, Q7 B, Q8 C).
