#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March US-A figures (Math Module 1)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-us-a/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", path.name)


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
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y0:.1f}" x2="{x2:.1f}" y2="{y0:.1f}" stroke="#111" stroke-width="1.6"/>'
        )
        if arrow:
            self.parts.append(
                f'<polygon points="{x2 + 10:.1f},{y0:.1f} {x2:.1f},{y0 - 4.5:.1f} {x2:.1f},{y0 + 4.5:.1f}" fill="#111"/>'
            )
            self.parts.append(
                f'<text x="{x2 + 16:.1f}" y="{y0 + 5:.1f}" {FONT} font-size="14" font-style="italic">x</text>'
            )
        dy = 16 if label_below else -8
        for v in labels:
            xv = self.px(v)
            self.parts.append(
                f'<line x1="{xv:.1f}" y1="{y0 - 4:.1f}" x2="{xv:.1f}" y2="{y0 + 4:.1f}" stroke="#111" stroke-width="1.2"/>'
            )
            self.parts.append(
                f'<text x="{xv:.1f}" y="{y0 + dy:.1f}" text-anchor="middle" {FONT} font-size="12">{v}</text>'
            )

    def axis_y(self, x: float, labels: list[int], label_left: bool = True, arrow: bool = True) -> None:
        x0 = self.px(x)
        y1, y2 = self.py(self.ymax), self.py(self.ymin)
        self.parts.append(
            f'<line x1="{x0:.1f}" y1="{y1:.1f}" x2="{x0:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="1.6"/>'
        )
        if arrow:
            self.parts.append(
                f'<polygon points="{x0:.1f},{y1 - 10:.1f} {x0 - 4.5:.1f},{y1:.1f} {x0 + 4.5:.1f},{y1:.1f}" fill="#111"/>'
            )
            self.parts.append(
                f'<text x="{x0 + 7:.1f}" y="{y1 - 12:.1f}" {FONT} font-size="14" font-style="italic">y</text>'
            )
        for v in labels:
            yv = self.py(v)
            self.parts.append(
                f'<line x1="{x0 - 4:.1f}" y1="{yv:.1f}" x2="{x0 + 4:.1f}" y2="{yv:.1f}" stroke="#111" stroke-width="1.2"/>'
            )
            if label_left:
                self.parts.append(
                    f'<text x="{x0 - 9:.1f}" y="{yv + 4:.1f}" text-anchor="end" {FONT} font-size="12">{v}</text>'
                )
            else:
                self.parts.append(f'<text x="{x0 + 9:.1f}" y="{yv + 4:.1f}" {FONT} font-size="12">{v}</text>')

    def origin(self, x: float, y: float, dx: float = -14, dy: float = 16) -> None:
        self.parts.append(
            f'<text x="{self.px(x) + dx:.1f}" y="{self.py(y) + dy:.1f}" {FONT} font-size="13" font-style="italic">O</text>'
        )

    def curve(self, pts: list[tuple[float, float]], width: float = 2.4) -> None:
        d = " ".join(f"{self.px(x):.1f},{self.py(y):.1f}" for x, y in pts)
        self.parts.append(
            f'<polyline points="{d}" fill="none" stroke="#111" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


def q02_exponential() -> None:
    # Source page-56: unit grid, labels every 2; asymptote y = 6; y-intercept (0, 9).
    p = Plane(-10.8, 10.8, -2.6, 14.6, 22, margin=(40, 28, 36, 32))
    p.grid(list(range(-10, 11)), list(range(-2, 15)))
    p.axis_x(0, [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.axis_y(0, [-2, 2, 4, 6, 8, 10, 12, 14])
    p.origin(0, 0, dx=-16, dy=16)
    # y = 3 · 2^x + 6  (through (0, 9); flattens to y = 6 from the left; exits near x ≈ 1.42)
    pts: list[tuple[float, float]] = []
    prev: tuple[float, float] | None = None
    x = -10.7
    ymax = 14.55
    while x <= 10.6:
        y = 3 * (2**x) + 6
        if y > ymax:
            if prev is not None:
                x0, y0 = prev
                t = (ymax - y0) / (y - y0)
                pts.append((x0 + t * 0.04, ymax))
            break
        pts.append((x, y))
        prev = (x, y)
        x += 0.04
    p.curve(pts, width=2.4)
    p.save(OUT / "math1-q02-exponential-graph.svg")


def q05_right_triangle() -> None:
    # Right angle at bottom-left; vertical leg 18; horizontal leg 40; hypotenuse x.
    w, h = 440, 330
    bl, br, tl = (88, 250), (378, 250), (88, 120)
    mx, my = (br[0] + tl[0]) / 2, (br[1] + tl[1]) / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<polygon points="{bl[0]},{bl[1]} {br[0]},{br[1]} {tl[0]},{tl[1]}" fill="none" stroke="#111" '
        f'stroke-width="2.2" stroke-linejoin="round"/>',
        f'<rect x="{bl[0]}" y="{bl[1] - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>',
        f'<text x="{bl[0] - 22}" y="{(bl[1] + tl[1]) / 2 + 6}" text-anchor="middle" {FONT} font-size="18">18</text>',
        f'<text x="{(bl[0] + br[0]) / 2}" y="{bl[1] + 28}" text-anchor="middle" {FONT} font-size="18">40</text>',
        f'<text x="{mx + 14:.1f}" y="{my - 4:.1f}" text-anchor="middle" {FONT} font-size="20" font-style="italic">x</text>',
        f'<text x="{w / 2}" y="{h - 16}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q05-right-triangle.svg", parts)


if __name__ == "__main__":
    q02_exponential()
    q05_right_triangle()
