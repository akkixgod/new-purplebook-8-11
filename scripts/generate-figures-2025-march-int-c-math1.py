#!/usr/bin/env python3
"""Generate clean SVGs for 2025 March Int-C figures (Math Module 1)."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2025-march-int-c/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = 'font-family="Georgia, serif"'


def esc(t: object) -> str:
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("wrote", path.name)


# --------------------------------------------------------------------------- tables


def table_svg(path: Path, headers: list[str], rows: list[list[str]], col_w: list[int]) -> None:
    row_h, header_h, pad = 38, 40, 14
    tw = sum(col_w) + 2 * pad
    th = header_h + row_h * len(rows) + 2 * pad
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}" viewBox="0 0 {tw} {th}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]

    def cell(x: float, y: float, w: float, h: float, text: str, header: bool) -> None:
        fill = "#f3f4f6" if header else "#fff"
        weight = "700" if header else "400"
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{x + w / 2}" y="{y + h / 2 + 4}" text-anchor="middle" {FONT} '
            f'font-size="13" font-weight="{weight}">{esc(text)}</text>'
        )

    x, y = pad, pad
    for i, h in enumerate(headers):
        cell(x, y, col_w[i], header_h, h, True)
        x += col_w[i]
    y += header_h
    for row in rows:
        x = pad
        for i, val in enumerate(row):
            cell(x, y, col_w[i], row_h, val, False)
            x += col_w[i]
        y += row_h
    parts.append("</svg>")
    write(path, parts)


# ----------------------------------------------------------------------- xy helpers


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

    def curve(self, pts: list[tuple[float, float]], width: float = 2.4) -> None:
        d = " ".join(f"{self.px(x):.1f},{self.py(y):.1f}" for x, y in pts)
        self.parts.append(f'<polyline points="{d}" fill="none" stroke="#111" stroke-width="{width}" stroke-linecap="round"/>')

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        write(path, self.parts)


# ------------------------------------------------------------------------ figures


def q02_scatterplot() -> None:
    p = Plane(-0.6, 8.6, -0.9, 16.9, 46, margin=(52, 30, 34, 34), py_per_unit=25)
    p.grid([i for i in range(0, 9)], [i for i in range(0, 17)])
    p.axis_x(0, [1, 2, 3, 4, 5, 6, 7, 8])
    p.axis_y(0, [2, 4, 6, 8, 10, 12, 14, 16])
    p.origin(0, 0)
    # line of best fit: y = 0.8 + 1.7x
    p.segment((0, 0.8), (8.4, 15.08), width=2.2)
    pts = [
        (0.5, 2), (1.6, 4), (2.5, 4), (2.5, 6), (3.6, 5),
        (3.6, 8), (4.4, 8), (4.4, 9), (5.5, 12), (6.7, 12),
    ]
    for x, y in pts:
        p.dot(x, y, 4.6)
    p.save(OUT / "math1-q02-scatterplot.svg")


def q06_table() -> None:
    table_svg(
        OUT / "math1-q06-value-frequency-table.svg",
        ["Value", "Frequency"],
        [["20", "6"], ["26", "1"], ["32", "6"], ["38", "3"]],
        [110, 130],
    )


def q10_line() -> None:
    p = Plane(-14.9, 1.0, -14.9, 1.0, 24, margin=(34, 30, 34, 34))
    p.grid(list(range(-14, 1)), list(range(-14, 1)))
    p.axis_x(0, [-14, -12, -10, -8, -6, -4, -2])
    p.axis_y(0, [-2, -4, -6, -8, -10, -12, -14], label_left=False)
    p.origin(0, 0, dx=6, dy=-6)
    # line through (-12, 0) and (0, -11): y = -(11/12)x - 11
    p.segment((-12.7, 0.64), (0.55, -11.5))
    p.dot(-12, 0)
    p.dot(0, -11)
    p.save(OUT / "math1-q10-line-xy-plane.svg")


def q12_transversal() -> None:
    w, h = 430, 330
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    r_x, s_x = 170, 280
    top, bot = 40, 275
    # lines r and s (vertical)
    for x, name in ((r_x, "r"), (s_x, "s")):
        parts.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bot}" stroke="#111" stroke-width="1.6"/>')
        parts.append(f'<text x="{x}" y="{top - 10}" text-anchor="middle" {FONT} font-size="14" font-style="italic">{name}</text>')
    # transversal k: down-right
    kx1, ky1, kx2, ky2 = 70, 42, 360, 272
    parts.append(f'<line x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}" stroke="#111" stroke-width="1.6"/>')
    parts.append(f'<text x="{kx1 - 4}" y="{ky1 - 8}" text-anchor="middle" {FONT} font-size="14" font-style="italic">k</text>')

    slope = (ky2 - ky1) / (kx2 - kx1)

    def ky(x: float) -> float:
        return ky1 + slope * (x - kx1)

    for x, above, below in ((r_x, "w", "x"), (s_x, "y", "z")):
        yy = ky(x)
        parts.append(f'<text x="{x + 16}" y="{yy - 14}" {FONT} font-size="14" font-style="italic">{above}<tspan font-style="normal">°</tspan></text>')
        parts.append(f'<text x="{x + 10}" y="{yy + 34}" {FONT} font-size="14" font-style="italic">{below}<tspan font-style="normal">°</tspan></text>')

    parts.append(
        f'<text x="{w / 2}" y="{h - 14}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>'
    )
    parts.append("</svg>")
    write(OUT / "math1-q12-transversal-angles.svg", parts)


def q18_exponential() -> None:
    p = Plane(-10.9, 10.9, -10.9, 5.9, 20, margin=(38, 28, 34, 30))
    p.grid(list(range(-10, 11)), list(range(-10, 6)))
    p.axis_x(0, [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.axis_y(0, [-10, -8, -6, -4, -2, 2, 4], label_left=True)
    p.origin(0, 0, dx=-16, dy=16)
    # y = -0.6 * 4.7^x - 5  (horizontal asymptote y = -5, plunges near x = 1.4)
    pts = []
    x = -10.6
    while x <= 2.5:
        y = -0.6 * (4.7 ** x) - 5
        if y < -10.7:
            pts.append((x, -10.7))
            break
        pts.append((x, y))
        x += 0.05
    p.curve(pts, width=2.4)
    p.save(OUT / "math1-q18-exponential-graph.svg")


def q21_triangle() -> None:
    w, h = 400, 300
    ax, ay = 110, 40
    bx, by = 110, 230
    cx, cy = 330, 230
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<polygon points="{ax},{ay} {bx},{by} {cx},{cy}" fill="none" stroke="#111" stroke-width="2.4" stroke-linejoin="round"/>',
        # right-angle marker at B
        f'<polyline points="{bx + 18},{by} {bx + 18},{by - 18} {bx},{by - 18}" fill="none" stroke="#111" stroke-width="1.6"/>',
        f'<text x="{ax - 16}" y="{ay + 2}" {FONT} font-size="15" font-style="italic">A</text>',
        f'<text x="{bx - 16}" y="{by + 20}" {FONT} font-size="15" font-style="italic">B</text>',
        f'<text x="{cx + 6}" y="{cy + 20}" {FONT} font-size="15" font-style="italic">C</text>',
        f'<text x="{cx - 62}" y="{cy - 12}" {FONT} font-size="14">30°</text>',
        f'<text x="{w / 2}" y="{h - 16}" text-anchor="middle" {FONT} font-size="13">Note: Figure not drawn to scale.</text>',
        "</svg>",
    ]
    write(OUT / "math1-q21-right-triangle.svg", parts)


if __name__ == "__main__":
    q02_scatterplot()
    q06_table()
    q10_line()
    q12_transversal()
    q18_exponential()
    q21_triangle()
