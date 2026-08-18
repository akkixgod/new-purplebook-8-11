#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March US-B figures (Math Module 2).

Style matches scripts/generate-figures-2025-march-int-e-math1.py.
Geometry was measured off public/mocks/2025-march-us-b/pages/page-{78,79,81,83,92,93}.png.

Run:  py -3 scripts/generate-figures-2025-march-us-b-math2.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-us-b/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'
GRID = "#c9ccd1"
INK = "#111"
SHADE = "#c4c4c4"


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

    def grid(self, xs: list[float], ys: list[float]) -> None:
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

    def curve(self, pts: list[tuple[float, float]], width: float = 2.4) -> None:
        d = " ".join(f"{self.px(x):.1f},{self.py(y):.1f}" for x, y in pts)
        self.parts.append(
            f'<polyline points="{d}" fill="none" stroke="{INK}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def dot(self, x: float, y: float, r: float = 4.2) -> None:
        self.parts.append(
            f'<circle cx="{self.px(x):.1f}" cy="{self.py(y):.1f}" r="{r}" fill="{INK}"/>'
        )

    def axis_titles(self, xlabel: str, ylabel: str) -> None:
        x_mid = (self.px(self.xmin) + self.px(self.xmax)) / 2
        y_mid = (self.py(self.ymin) + self.py(self.ymax)) / 2
        self.parts.append(
            f'<text x="{x_mid:.1f}" y="{self.h - 12:.1f}" text-anchor="middle" {FONT} font-size="13">{xlabel}</text>'
        )
        self.parts.append(
            f'<text x="18" y="{y_mid:.1f}" text-anchor="middle" {FONT} font-size="13" '
            f'transform="rotate(-90 18 {y_mid:.1f})">{ylabel}</text>'
        )

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


def table_svg(
    path: Path,
    headers: list[str],
    rows: list[list[str]],
    col_w: list[int],
    *,
    italic_headers: bool = False,
    italic_cols: tuple[int, ...] = (),
) -> None:
    row_h, header_h, pad = 38, 40, 14
    tw = sum(col_w) + 2 * pad
    th = header_h + row_h * len(rows) + 2 * pad
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool, italic: bool) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        style = ' font-style="italic"' if italic else ""
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle" {FONT} '
            f'font-size="13" font-weight="{weight}"{style}>{text}</text>'
        )

    x, y = pad, pad
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True, italic_headers)
        x += col_w[i]
    y += header_h
    for row in rows:
        x = pad
        for i, val in enumerate(row):
            cell(x, y, col_w[i], row_h, val, False, i in italic_cols)
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    write(path, parts)


def q03_capacitor() -> None:
    """Exponential decay V = 16 · (1/3)^t. 15% of 16 V is 2.4 V at t ≈ 1.73 s."""
    p = Plane(0, 4.35, 0, 21.4, 86, margin=(78, 34, 48, 52), py_per_unit=15.2)
    p.grid([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], list(range(2, 21, 2)))
    p.axis_x(0, [1, 2, 3, 4])
    p.axis_y(0, list(range(2, 21, 2)))
    p.origin(0, 0, dx=10, dy=16)
    pts: list[tuple[float, float]] = []
    x = 0.0
    while x <= 4.32:
        pts.append((x, 16 * (1 / 3) ** x))
        x += 0.02
    p.curve(pts, width=2.4)
    p.axis_titles("Time (seconds)", "Potential difference (volts)")
    p.save(OUT / "math2-q03-capacitor-graph.svg")


def q04_scatterplot() -> None:
    """Q1 scatter + LOBF y = −0.8x + 54.57 so intercept_B = 45.57 after −9."""
    p = Plane(0, 63, 0, 63, 6.4, margin=(52, 30, 44, 36))
    p.grid(list(range(5, 61, 5)), list(range(5, 61, 5)))
    p.axis_x(0, [15, 30, 45, 60])
    p.axis_y(0, [15, 30, 45, 60])
    p.origin(0, 0, dx=10, dy=16)
    p.segment((0, 54.57), (63, 54.57 - 0.8 * 63), width=2.2)
    pts = [
        (12, 47),
        (14, 46),
        (15, 40),
        (16, 42),
        (16, 41),
        (22, 34),
        (26, 32),
        (30, 31),
        (32, 32),
        (35, 25),
        (38, 26),
        (42, 22),
    ]
    for x, y in pts:
        p.dot(x, y, 4.4)
    p.save(OUT / "math2-q04-scatterplot.svg")


def q06_table() -> None:
    table_svg(
        OUT / "math2-q06-linear-table.svg",
        ["x", "f(x)"],
        [["1", "\u221220"], ["5", "\u221240"], ["10", "\u221265"]],
        [90, 110],
        italic_headers=True,
    )


def q08_table() -> None:
    table_svg(
        OUT / "math2-q08-age-table.svg",
        ["Age group", "Proportion"],
        [
            ["Less than 18 years old", "34%"],
            ["18\u201340 years old", "23%"],
            ["41\u201365 years old", "22%"],
            ["Greater than 65 years old", "21%"],
        ],
        [230, 120],
    )


def q16_pool() -> None:
    """Nested rectangles: gray inner pool, path of width x on all sides."""
    w, h = 420, 340
    ox, oy, ow, oh = 70, 48, 300, 210
    gap = 36
    ix, iy, iw, ih = ox + gap, oy + gap, ow - 2 * gap, oh - 2 * gap
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="none" stroke="{INK}" stroke-width="2"/>',
        f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="{SHADE}" stroke="{INK}" stroke-width="2"/>',
        f'<text x="{ix + iw / 2:.1f}" y="{iy + ih / 2 + 5:.1f}" text-anchor="middle" {FONT} font-size="16">pool</text>',
        f'<text x="{ox + 10}" y="{oy + 22}" {FONT} font-size="14">concrete path</text>',
        # left gap: horizontal dimension
        f'<line x1="{ox}" y1="{iy + ih / 2:.1f}" x2="{ix}" y2="{iy + ih / 2:.1f}" stroke="{INK}" stroke-width="1.3"/>',
        f'<polygon points="{ox},{iy + ih / 2:.1f} {ox + 7},{iy + ih / 2 - 4:.1f} {ox + 7},{iy + ih / 2 + 4:.1f}" fill="{INK}"/>',
        f'<polygon points="{ix},{iy + ih / 2:.1f} {ix - 7},{iy + ih / 2 - 4:.1f} {ix - 7},{iy + ih / 2 + 4:.1f}" fill="{INK}"/>',
        f'<text x="{(ox + ix) / 2:.1f}" y="{iy + ih / 2 - 8:.1f}" text-anchor="middle" {FONT} font-size="14">'
        f'<tspan font-style="italic">x</tspan> ft</text>',
        # top gap: vertical dimension
        f'<line x1="{ix + iw / 2:.1f}" y1="{oy}" x2="{ix + iw / 2:.1f}" y2="{iy}" stroke="{INK}" stroke-width="1.3"/>',
        f'<polygon points="{ix + iw / 2:.1f},{oy} {ix + iw / 2 - 4:.1f},{oy + 7} {ix + iw / 2 + 4:.1f},{oy + 7}" fill="{INK}"/>',
        f'<polygon points="{ix + iw / 2:.1f},{iy} {ix + iw / 2 - 4:.1f},{iy - 7} {ix + iw / 2 + 4:.1f},{iy - 7}" fill="{INK}"/>',
        f'<text x="{ix + iw / 2 + 10:.1f}" y="{(oy + iy) / 2 + 5:.1f}" {FONT} font-size="14">'
        f'<tspan font-style="italic">x</tspan> ft</text>',
        f'<text x="{w / 2}" y="{h - 16}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math2-q16-pool-path.svg", parts)


def q17_table() -> None:
    table_svg(
        OUT / "math2-q17-linear-table.svg",
        ["x", "y"],
        [["\u22122s", "17"], ["\u2212s", "14"], ["s", "8"]],
        [90, 90],
        italic_headers=True,
        italic_cols=(0,),
    )


if __name__ == "__main__":
    q03_capacitor()
    q04_scatterplot()
    q06_table()
    q08_table()
    q16_pool()
    q17_table()
