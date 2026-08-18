#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March US-A figures (Math Module 2).

Style matches scripts/generate-figures-2025-march-int-e-math1.py.
Geometry was measured off public/mocks/2025-march-us-a/pages/page-{87,89,92}.png.

Run:  py -3 scripts/generate-figures-2025-march-us-a-math2.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-us-a/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'
GRID = "#c9ccd1"
INK = "#111"
SHADE = "#bfbfbf"


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", path.name)


def minus_label(v: int) -> str:
    return f"\u2212{abs(v)}" if v < 0 else str(v)


class Plane:
    """xy-plane with unit grid, dark axes, and labelled ticks."""

    def __init__(
        self,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        px_per_unit: float,
        margin: tuple[int, int, int, int] = (46, 34, 34, 40),
        py_per_unit: float | None = None,
    ) -> None:
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.k = px_per_unit
        self.ky = py_per_unit if py_per_unit is not None else px_per_unit
        self.ml, self.mt, self.mr, self.mb = margin
        self.w = self.ml + self.mr + (xmax - xmin) * self.k
        self.h = self.mt + self.mb + (ymax - ymin) * self.ky
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w:.0f}" height="{self.h:.0f}" '
            f'viewBox="0 0 {self.w:.0f} {self.h:.0f}">',
            '<rect width="100%" height="100%" fill="#fff"/>',
        ]

    def px(self, x: float) -> float:
        return self.ml + (x - self.xmin) * self.k

    def py(self, y: float) -> float:
        return self.mt + (self.ymax - y) * self.ky

    def grid(self, xs: list[int], ys: list[int]) -> None:
        y_top, y_bot = self.py(self.ymax), self.py(self.ymin)
        x_left, x_right = self.px(self.xmin), self.px(self.xmax)
        for gx in xs:
            self.parts.append(
                f'<line x1="{self.px(gx):.1f}" y1="{y_top:.1f}" '
                f'x2="{self.px(gx):.1f}" y2="{y_bot:.1f}" stroke="{GRID}" stroke-width="1"/>'
            )
        for gy in ys:
            self.parts.append(
                f'<line x1="{x_left:.1f}" y1="{self.py(gy):.1f}" '
                f'x2="{x_right:.1f}" y2="{self.py(gy):.1f}" stroke="{GRID}" stroke-width="1"/>'
            )

    def axis_x(self, y: float, labels: list[int], label_below: bool = True, arrow: bool = True) -> None:
        y0 = self.py(y)
        x1, x2 = self.px(self.xmin), self.px(self.xmax)
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y0:.1f}" x2="{x2:.1f}" y2="{y0:.1f}" stroke="{INK}" stroke-width="1.6"/>'
        )
        if arrow:
            self.parts.append(
                f'<polygon points="{x2 + 10:.1f},{y0:.1f} {x2:.1f},{y0 - 4.5:.1f} {x2:.1f},{y0 + 4.5:.1f}" fill="{INK}"/>'
            )
            self.parts.append(
                f'<text x="{x2 + 16:.1f}" y="{y0 + 5:.1f}" {FONT} font-size="14" font-style="italic">x</text>'
            )
        dy = 16 if label_below else -8
        for v in labels:
            xv = self.px(v)
            self.parts.append(
                f'<line x1="{xv:.1f}" y1="{y0 - 4:.1f}" x2="{xv:.1f}" y2="{y0 + 4:.1f}" stroke="{INK}" stroke-width="1.2"/>'
            )
            self.parts.append(
                f'<text x="{xv:.1f}" y="{y0 + dy:.1f}" text-anchor="middle" {FONT} font-size="12">{minus_label(v)}</text>'
            )

    def axis_y(self, x: float, labels: list[int], label_left: bool = True, arrow: bool = True) -> None:
        x0 = self.px(x)
        y1, y2 = self.py(self.ymax), self.py(self.ymin)
        self.parts.append(
            f'<line x1="{x0:.1f}" y1="{y1:.1f}" x2="{x0:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="1.6"/>'
        )
        if arrow:
            self.parts.append(
                f'<polygon points="{x0:.1f},{y1 - 10:.1f} {x0 - 4.5:.1f},{y1:.1f} {x0 + 4.5:.1f},{y1:.1f}" fill="{INK}"/>'
            )
            self.parts.append(
                f'<text x="{x0 + 7:.1f}" y="{y1 - 12:.1f}" {FONT} font-size="14" font-style="italic">y</text>'
            )
        for v in labels:
            yv = self.py(v)
            self.parts.append(
                f'<line x1="{x0 - 4:.1f}" y1="{yv:.1f}" x2="{x0 + 4:.1f}" y2="{yv:.1f}" stroke="{INK}" stroke-width="1.2"/>'
            )
            label = minus_label(v)
            if label_left:
                self.parts.append(
                    f'<text x="{x0 - 9:.1f}" y="{yv + 4:.1f}" text-anchor="end" {FONT} font-size="12">{label}</text>'
                )
            else:
                self.parts.append(
                    f'<text x="{x0 + 9:.1f}" y="{yv + 4:.1f}" {FONT} font-size="12">{label}</text>'
                )

    def origin(self, x: float, y: float, dx: float = -14, dy: float = 16) -> None:
        self.parts.append(
            f'<text x="{self.px(x) + dx:.1f}" y="{self.py(y) + dy:.1f}" {FONT} font-size="13" font-style="italic">O</text>'
        )

    def segment(self, p1: tuple[float, float], p2: tuple[float, float], width: float = 2.4) -> None:
        self.parts.append(
            f'<line x1="{self.px(p1[0]):.1f}" y1="{self.py(p1[1]):.1f}" x2="{self.px(p2[0]):.1f}" '
            f'y2="{self.py(p2[1]):.1f}" stroke="{INK}" stroke-width="{width}"/>'
        )

    def dot(self, x: float, y: float, r: float = 4.5) -> None:
        self.parts.append(
            f'<circle cx="{self.px(x):.1f}" cy="{self.py(y):.1f}" r="{r}" fill="{INK}"/>'
        )

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


def q10_maksim_walk() -> None:
    """Distance-time line: (0, 50) to (10, 600). Measured from page-92.png.

    Plot is nearly square: 10 x-units ≈ 900 y-units in pixels.
    y-axis labelled 100…900; horizontal grid every 50; vertical grid every 1.
    """
    p = Plane(0, 10.8, 0, 960, 32.0, margin=(52, 28, 44, 36), py_per_unit=0.36)
    p.grid(list(range(1, 11)), list(range(50, 901, 50)))
    p.axis_x(0, list(range(1, 11)))
    p.axis_y(0, list(range(100, 901, 100)))
    p.origin(0, 0, dx=10, dy=16)
    p.segment((0, 50), (10, 600), width=2.4)
    p.dot(0, 50)
    p.dot(10, 600)
    p.save(OUT / "math2-q10-line-graph.svg")


def q12_shaded_inequality() -> None:
    """Half-plane x + 5y ≥ −65. Boundary y = −x/5 − 13 through (0, −13) and (−5, −12).

    Measured from page-87.png: QIII grid, x labels −10…−2, y labels −2…−14
    on the right of the y-axis, region above the line shaded.
    """
    p = Plane(-10.5, 1.2, -15.5, 0.0, 36.0, margin=(28, 36, 56, 28), py_per_unit=24.0)
    x0, x1 = p.xmin, p.xmax

    def line_y(x: float) -> float:
        return -x / 5 - 13

    clip_x, clip_y = p.px(p.xmin), p.py(p.ymax)
    clip_w = p.px(p.xmax) - clip_x
    clip_h = p.py(p.ymin) - clip_y
    p.parts.append(
        f'<defs><clipPath id="plot"><rect x="{clip_x:.1f}" y="{clip_y:.1f}" '
        f'width="{clip_w:.1f}" height="{clip_h:.1f}"/></clipPath></defs>'
    )
    shade = [
        (x0, line_y(x0)),
        (x1, line_y(x1)),
        (x1, p.ymax),
        (x0, p.ymax),
    ]
    d = " ".join(f"{p.px(x):.1f},{p.py(y):.1f}" for x, y in shade)
    p.parts.append(
        f'<polygon clip-path="url(#plot)" points="{d}" fill="{SHADE}" fill-opacity="0.55"/>'
    )
    p.grid(list(range(-10, 1)), list(range(-15, 1)))
    p.axis_x(0, [-10, -8, -6, -4, -2], label_below=True)
    p.axis_y(0, [-2, -4, -6, -8, -10, -12, -14], label_left=False)
    p.origin(0, 0, dx=-16, dy=16)
    p.segment((x0, line_y(x0)), (x1, line_y(x1)), width=2.6)
    p.dot(-5, -12)
    p.dot(0, -13)
    p.save(OUT / "math2-q12-shaded-inequality.svg")


def q14_salmon_histogram() -> None:
    """Histogram of 14 salmon weights. Measured from page-89.png.

    Bins 70–75, 75–80, 80–85, 85–90, 90–95 with frequencies 2, 1, 2, 6, 3.
    y from 0 to 6; x ticks at 70, 75, 80, 85, 90, 95.
    """
    w, h = 520, 360
    left, right, top, bottom = 72, 490, 28, 292
    plot_w = right - left
    plot_h = bottom - top
    bins = [70, 75, 80, 85, 90, 95]
    freqs = [2, 1, 2, 6, 3]
    xmin, xmax = 70.0, 95.0
    ymax = 6.0

    def sx(x: float) -> float:
        return left + (x - xmin) / (xmax - xmin) * plot_w

    def sy(y: float) -> float:
        return bottom - y / ymax * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for j in range(0, 7):
        yy = sy(j)
        parts.append(
            f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="{GRID}"/>'
        )
        parts.append(
            f'<line x1="{left - 4}" y1="{yy:.1f}" x2="{left}" y2="{yy:.1f}" stroke="{INK}" stroke-width="1.2"/>'
        )
        parts.append(
            f'<text x="{left - 8}" y="{yy + 4:.1f}" text-anchor="end" {FONT} font-size="12">{j}</text>'
        )
    for i, freq in enumerate(freqs):
        x0, x1 = sx(bins[i]), sx(bins[i + 1])
        y0, y1 = sy(freq), sy(0)
        parts.append(
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" '
            f'fill="#c4c4c4" stroke="{INK}" stroke-width="1.4"/>'
        )
    parts.append(
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{INK}" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{INK}" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{right}" y1="{top}" x2="{right}" y2="{bottom}" stroke="{INK}" stroke-width="1.2"/>'
    )
    parts.append(
        f'<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" stroke="{INK}" stroke-width="1.2"/>'
    )
    for t in bins:
        xv = sx(t)
        parts.append(
            f'<line x1="{xv:.1f}" y1="{bottom}" x2="{xv:.1f}" y2="{bottom + 5}" stroke="{INK}"/>'
        )
        parts.append(
            f'<text x="{xv:.1f}" y="{bottom + 20}" text-anchor="middle" {FONT} font-size="12">{t}</text>'
        )
    mid_y = (top + bottom) / 2
    parts.append(
        f'<text x="18" y="{mid_y:.1f}" text-anchor="middle" {FONT} font-size="13" '
        f'transform="rotate(-90 18 {mid_y:.1f})">Number of salmon</text>'
    )
    parts.append(
        f'<text x="{(left + right) / 2:.1f}" y="{h - 18}" text-anchor="middle" {FONT} font-size="13">Weight (pounds)</text>'
    )
    parts.append("</svg>")
    write(OUT / "math2-q14-salmon-histogram.svg", parts)


if __name__ == "__main__":
    q10_maksim_walk()
    q12_shaded_inequality()
    q14_salmon_histogram()
