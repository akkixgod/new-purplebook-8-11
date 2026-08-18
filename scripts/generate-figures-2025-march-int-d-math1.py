#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-D figures (Math Module 1)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-d/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", path.name)


class Plane:
    """Simple xy-plane with unit grid, dark axes and labelled even ticks."""

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
        for gx in xs:
            self.parts.append(
                f'<line x1="{self.px(gx):.1f}" y1="{self.py(self.ymax):.1f}" '
                f'x2="{self.px(gx):.1f}" y2="{self.py(self.ymin):.1f}" stroke="#c9ccd1" stroke-width="1"/>'
            )
        for gy in ys:
            self.parts.append(
                f'<line x1="{self.px(self.xmin):.1f}" y1="{self.py(gy):.1f}" '
                f'x2="{self.px(self.xmax):.1f}" y2="{self.py(gy):.1f}" stroke="#c9ccd1" stroke-width="1"/>'
            )

    def axis_x(self, y: float, labels: list[int], label_below: bool = True, arrow: bool = True) -> None:
        y0 = self.py(y)
        x1, x2 = self.px(self.xmin), self.px(self.xmax)
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y0:.1f}" x2="{x2:.1f}" y2="{y0:.1f}" stroke="#111" stroke-width="1.6"/>')
        if arrow:
            self.parts.append(f'<polygon points="{x2 + 10:.1f},{y0:.1f} {x2:.1f},{y0 - 4.5:.1f} {x2:.1f},{y0 + 4.5:.1f}" fill="#111"/>')
            self.parts.append(f'<text x="{x2 + 16:.1f}" y="{y0 + 5:.1f}" {FONT} font-size="14" font-style="italic">x</text>')
        dy = 16 if label_below else -8
        for v in labels:
            xv = self.px(v)
            self.parts.append(f'<line x1="{xv:.1f}" y1="{y0 - 4:.1f}" x2="{xv:.1f}" y2="{y0 + 4:.1f}" stroke="#111" stroke-width="1.2"/>')
            self.parts.append(
                f'<text x="{xv:.1f}" y="{y0 + dy:.1f}" text-anchor="middle" {FONT} font-size="12">{v}</text>'
            )

    def axis_y(self, x: float, labels: list[int], label_left: bool = True, arrow: bool = True) -> None:
        x0 = self.px(x)
        y1, y2 = self.py(self.ymax), self.py(self.ymin)
        self.parts.append(f'<line x1="{x0:.1f}" y1="{y1:.1f}" x2="{x0:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="1.6"/>')
        if arrow:
            self.parts.append(f'<polygon points="{x0:.1f},{y1 - 10:.1f} {x0 - 4.5:.1f},{y1:.1f} {x0 + 4.5:.1f},{y1:.1f}" fill="#111"/>')
            self.parts.append(f'<text x="{x0 + 7:.1f}" y="{y1 - 12:.1f}" {FONT} font-size="14" font-style="italic">y</text>')
        for v in labels:
            yv = self.py(v)
            self.parts.append(f'<line x1="{x0 - 4:.1f}" y1="{yv:.1f}" x2="{x0 + 4:.1f}" y2="{yv:.1f}" stroke="#111" stroke-width="1.2"/>')
            if label_left:
                self.parts.append(f'<text x="{x0 - 9:.1f}" y="{yv + 4:.1f}" text-anchor="end" {FONT} font-size="12">{v}</text>')
            else:
                self.parts.append(f'<text x="{x0 + 9:.1f}" y="{yv + 4:.1f}" {FONT} font-size="12">{v}</text>')

    def origin(self, x: float, y: float, dx: float = -14, dy: float = 16) -> None:
        self.parts.append(
            f'<text x="{self.px(x) + dx:.1f}" y="{self.py(y) + dy:.1f}" {FONT} font-size="13" font-style="italic">O</text>'
        )

    def segment(self, p1: tuple[float, float], p2: tuple[float, float], width: float = 2.4) -> None:
        self.parts.append(
            f'<line x1="{self.px(p1[0]):.1f}" y1="{self.py(p1[1]):.1f}" x2="{self.px(p2[0]):.1f}" '
            f'y2="{self.py(p2[1]):.1f}" stroke="#111" stroke-width="{width}"/>'
        )

    def dot(self, x: float, y: float, r: float = 4.2) -> None:
        self.parts.append(f'<circle cx="{self.px(x):.1f}" cy="{self.py(y):.1f}" r="{r}" fill="#111"/>')

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


def q03_scatterplot() -> None:
    p = Plane(-0.6, 8.6, -0.9, 16.9, 46, margin=(52, 30, 34, 34), py_per_unit=25)
    p.grid([i for i in range(0, 9)], [i for i in range(0, 17)])
    p.axis_x(0, [1, 2, 3, 4, 5, 6, 7, 8])
    p.axis_y(0, [2, 4, 6, 8, 10, 12, 14, 16])
    p.origin(0, 0)
    # line of best fit: y = 0.6 + 1.5x
    p.segment((0, 0.6), (8.4, 13.2), width=2.2)
    pts = [
        (0.4, 1.1),
        (1.5, 3.0),
        (2.2, 5.0),
        (2.5, 3.1),
        (3.5, 7.1),
        (3.6, 5.1),
        (4.3, 7.1),
        (4.4, 9.1),
        (5.5, 12.0),
        (6.7, 8.1),
    ]
    for x, y in pts:
        p.dot(x, y, 4.6)
    p.save(OUT / "math1-q03-scatterplot.svg")


if __name__ == "__main__":
    q03_scatterplot()
