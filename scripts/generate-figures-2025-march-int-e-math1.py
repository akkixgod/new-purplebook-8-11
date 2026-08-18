#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-E figures (Math Module 1)."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path("public/mocks/2025-march-int-e/figures")
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

    def segment(self, p1: tuple[float, float], p2: tuple[float, float], width: float = 2.4) -> None:
        self.parts.append(
            f'<line x1="{self.px(p1[0]):.1f}" y1="{self.py(p1[1]):.1f}" x2="{self.px(p2[0]):.1f}" '
            f'y2="{self.py(p2[1]):.1f}" stroke="#111" stroke-width="{width}"/>'
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


def q01_cost_line() -> None:
    # Square grid cells: 10 x-units = 25 y-units.
    p = Plane(0, 108, 0, 312, 3.2, margin=(52, 28, 40, 36), py_per_unit=1.28)
    p.grid(list(range(10, 101, 10)), list(range(25, 301, 25)))
    p.axis_x(0, list(range(10, 101, 10)))
    p.axis_y(0, list(range(50, 301, 50)))
    p.origin(0, 0, dx=10, dy=16)
    # y = 1.5x + 100 through (0, 100) and (50, 175)
    p.segment((0, 100), (108, 1.5 * 108 + 100), width=2.4)
    p.save(OUT / "math1-q01-cost-line.svg")


def q03_exponential() -> None:
    p = Plane(-10.8, 10.8, -2.6, 14.6, 22, margin=(40, 28, 36, 32))
    p.grid(list(range(-10, 11, 2)), list(range(-2, 15, 2)))
    p.axis_x(0, [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.axis_y(0, [-2, 2, 4, 6, 8, 10, 12, 14])
    p.origin(0, 0, dx=-16, dy=16)
    # y = 5 · 2^x  (through (0, 5) and (1, 10); exits the top near x ≈ 1.53)
    pts: list[tuple[float, float]] = []
    prev: tuple[float, float] | None = None
    x = -10.7
    ymax = 14.55
    while x <= 10.6:
        y = 5 * (2**x)
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
    p.save(OUT / "math1-q03-exponential-graph.svg")


def q10_similar_triangles() -> None:
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
    write(OUT / "math1-q10-similar-triangles.svg", parts)


def q18_ramp() -> None:
    w, h = 420, 300
    # Right triangle: base x, height on the right, theta at the ground.
    ax, ay = 50, 230
    bx, by = 330, 230
    cx, cy = 330, 70
    # hypotenuse angle for the "length of the ramp" label
    ang = math.degrees(math.atan2(ay - cy, bx - ax))
    mx, my = (ax + cx) / 2, (ay + cy) / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" fill="none" stroke="#111" stroke-width="2.2" stroke-linejoin="round"/>',
        f'<rect x="{bx - 16}" y="{by - 16}" width="16" height="16" fill="none" stroke="#111" stroke-width="1.5"/>',
        f'<text x="{(ax + bx) / 2}" y="{ay + 24}" text-anchor="middle" {FONT} font-size="16" font-style="italic">x</text>',
        f'<text x="{bx + 14}" y="{(by + cy) / 2 - 8}" {FONT} font-size="14">height of</text>',
        f'<text x="{bx + 14}" y="{(by + cy) / 2 + 10}" {FONT} font-size="14">the ramp</text>',
        f'<text x="{mx - 8}" y="{my - 8}" text-anchor="middle" transform="rotate(-{ang:.1f} {mx:.1f} {my:.1f})" '
        f'{FONT} font-size="14">length of the ramp</text>',
        f'<text x="{ax + 28}" y="{ay - 12}" {FONT} font-size="16" font-style="italic">θ</text>',
        f'<text x="{w / 2}" y="{h - 14}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q18-ramp.svg", parts)


def q19_vertical_angles() -> None:
    # Flat X so the top/bottom vertical angles are the obtuse pair (w = 112).
    w, h = 420, 300
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<line x1="40" y1="125" x2="380" y2="185" stroke="#111" stroke-width="2"/>',
        '<line x1="40" y1="185" x2="380" y2="125" stroke="#111" stroke-width="2"/>',
        f'<text x="204" y="118" text-anchor="middle" {FONT} font-size="16" font-style="italic">w'
        f'<tspan font-style="normal">°</tspan></text>',
        f'<text x="204" y="214" text-anchor="middle" {FONT} font-size="16" font-style="italic">z'
        f'<tspan font-style="normal">°</tspan></text>',
        f'<text x="{w / 2}" y="{h - 16}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q19-vertical-angles.svg", parts)


if __name__ == "__main__":
    q01_cost_line()
    q03_exponential()
    q10_similar_triangles()
    q18_ramp()
    q19_vertical_angles()
