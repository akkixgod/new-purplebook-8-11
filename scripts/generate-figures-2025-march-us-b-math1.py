#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March US-B figures (Math Module 1).

Style matches scripts/generate-figures-2025-march-int-e-math1.py and
scripts/generate-figures-2025-march-us-a-math1.py.

Run:  py -3 scripts/generate-figures-2025-march-us-b-math1.py
"""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path("public/mocks/2025-march-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'
GRID = "#c9ccd1"
INK = "#111"


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
                f'x2="{self.px(gx):.1f}" y2="{self.py(self.ymin):.1f}" stroke="{GRID}" stroke-width="1"/>'
            )
        for gy in ys:
            self.parts.append(
                f'<line x1="{self.px(self.xmin):.1f}" y1="{self.py(gy):.1f}" '
                f'x2="{self.px(self.xmax):.1f}" y2="{self.py(gy):.1f}" stroke="{GRID}" stroke-width="1"/>'
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
                f'<text x="{xv:.1f}" y="{y0 + dy:.1f}" text-anchor="middle" {FONT} font-size="12">{v}</text>'
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
            f'<polyline points="{d}" fill="none" stroke="{INK}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def dot(self, x: float, y: float, r: float = 4.0) -> None:
        self.parts.append(
            f'<circle cx="{self.px(x):.1f}" cy="{self.py(y):.1f}" r="{r}" fill="{INK}"/>'
        )

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


def q01_triangle() -> None:
    # Isosceles triangle; base x, congruent legs y.
    w, h = 360, 300
    a, b, c = (70, 230), (290, 230), (180, 58)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<polygon points="{a[0]},{a[1]} {b[0]},{b[1]} {c[0]},{c[1]}" fill="none" stroke="{INK}" '
        f'stroke-width="2.2" stroke-linejoin="round"/>',
        f'<text x="{(a[0] + b[0]) / 2}" y="{a[1] + 26}" text-anchor="middle" {FONT} font-size="20" font-style="italic">x</text>',
        f'<text x="{(a[0] + c[0]) / 2 - 16}" y="{(a[1] + c[1]) / 2 + 4}" text-anchor="middle" {FONT} font-size="20" font-style="italic">y</text>',
        f'<text x="{(b[0] + c[0]) / 2 + 16}" y="{(b[1] + c[1]) / 2 + 4}" text-anchor="middle" {FONT} font-size="20" font-style="italic">y</text>',
        f'<text x="{w / 2}" y="{h - 16}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q01-triangle.svg", parts)


def q12_similar_triangles() -> None:
    # Right triangle CAE (right angles at E and D); BD ∥ AE. Same family as Int-E Q10.
    w, h = 300, 360
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<line x1="60" y1="300" x2="230" y2="300" stroke="#111" stroke-width="2"/>',
        '<line x1="230" y1="300" x2="230" y2="40" stroke="#111" stroke-width="2"/>',
        '<line x1="60" y1="300" x2="230" y2="40" stroke="#111" stroke-width="2"/>',
        '<line x1="145" y1="170" x2="230" y2="170" stroke="#111" stroke-width="2"/>',
        '<rect x="215" y="285" width="15" height="15" fill="none" stroke="#111"/>',
        '<rect x="215" y="155" width="15" height="15" fill="none" stroke="#111"/>',
        f'<text x="48" y="318" {FONT} font-size="16" font-style="italic">A</text>',
        f'<text x="236" y="318" {FONT} font-size="16" font-style="italic">E</text>',
        f'<text x="236" y="38" {FONT} font-size="16" font-style="italic">C</text>',
        f'<text x="236" y="175" {FONT} font-size="16" font-style="italic">D</text>',
        f'<text x="128" y="168" {FONT} font-size="16" font-style="italic">B</text>',
        f'<text x="{w / 2}" y="{h - 15}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q12-similar-triangles.svg", parts)


def q13_alkane() -> None:
    # Page 67: x 0–250 labels / 25 grid; y −200–300 labels / 25 grid.
    # Slightly concave-down through (0, −175), x-intercept ~70, marked (141.32, 172.26).
    p = Plane(0, 268, -210, 318, 1.9, margin=(52, 28, 40, 36), py_per_unit=1.15)
    p.grid(list(range(25, 251, 25)), list(range(-200, 301, 25)))
    p.axis_x(0, [50, 100, 150, 200, 250])
    p.axis_y(0, [-200, -150, -100, -50, 50, 100, 150, 200, 250, 300])
    p.origin(0, 0, dx=10, dy=16)

    def f(x: float) -> float:
        # Quadratic through (0, −175), (70, 0), near (141.32, 172.26).
        return -0.0006 * x * x + 2.542 * x - 175

    pts: list[tuple[float, float]] = []
    x = 1.0
    ymax = 314
    while x <= 265:
        y = f(x)
        if y > ymax:
            pts.append((x, ymax))
            break
        pts.append((x, y))
        x += 1.0
    p.curve(pts, width=2.4)
    p.dot(141.32, 172.26, r=4.2)
    p.save(OUT / "math1-q13-alkane-graph.svg")


def q21_ramp() -> None:
    w, h = 420, 300
    ax, ay = 50, 230
    bx, by = 330, 230
    cx, cy = 330, 70
    ang = math.degrees(math.atan2(ay - cy, bx - ax))
    mx, my = (ax + cx) / 2, (ay + cy) / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>',
        f'<rect x="{bx - 16}" y="{by - 16}" width="16" height="16" fill="none" stroke="{INK}" stroke-width="1.5"/>',
        f'<text x="{(ax + bx) / 2}" y="{ay + 24}" text-anchor="middle" {FONT} font-size="16" font-style="italic">x</text>',
        f'<text x="{bx + 14}" y="{(by + cy) / 2 - 8}" {FONT} font-size="14">height of</text>',
        f'<text x="{bx + 14}" y="{(by + cy) / 2 + 10}" {FONT} font-size="14">the ramp</text>',
        f'<text x="{mx - 8}" y="{my - 8}" text-anchor="middle" transform="rotate(-{ang:.1f} {mx:.1f} {my:.1f})" '
        f'{FONT} font-size="14">length of the ramp</text>',
        f'<text x="{ax + 28}" y="{ay - 12}" {FONT} font-size="16" font-style="italic">θ</text>',
        f'<text x="{w / 2}" y="{h - 14}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q21-ramp.svg", parts)


def q22_exponential() -> None:
    # y = 5^x − 4; asymptote y = −4; dots at (0, −3) and (1, 1).
    p = Plane(-4.6, 4.6, -6.6, 10.6, 36, margin=(40, 28, 36, 32))
    p.grid(list(range(-4, 5)), list(range(-6, 11)))
    p.axis_x(0, [-4, -2, 2, 4])
    p.axis_y(0, [-6, -4, -2, 2, 4, 6, 8, 10])
    p.origin(0, 0, dx=-16, dy=16)
    pts: list[tuple[float, float]] = []
    prev: tuple[float, float] | None = None
    x = -4.5
    ymax = 10.45
    while x <= 4.4:
        y = (5**x) - 4
        if y > ymax:
            if prev is not None:
                x0, y0 = prev
                t = (ymax - y0) / (y - y0)
                pts.append((x0 + t * 0.03, ymax))
            break
        pts.append((x, y))
        prev = (x, y)
        x += 0.03
    p.curve(pts, width=2.4)
    p.dot(0, -3, r=4.0)
    p.dot(1, 1, r=4.0)
    p.save(OUT / "math1-q22-exponential.svg")


if __name__ == "__main__":
    q01_triangle()
    q12_similar_triangles()
    q13_alkane()
    q21_ramp()
    q22_exponential()
