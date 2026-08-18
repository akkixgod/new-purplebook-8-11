"""Generate Math Module 2 stem figures for the 2025-march-int-d mock.

Four items carry artwork: Q4 (shaded half-plane on an −8…8 grid), Q12 (line
y = 6x + 9), Q13 (shaded half-plane rx + ty ≥ −36), and Q15 (decaying
exponential y = −6^x + 5). Geometry follows the page screenshots.

Run:  py -3 scripts/_gen_math2_figs_marchintd.py
"""
from __future__ import annotations

from math import log
from pathlib import Path

OUT = Path("public/mocks/2025-march-int-d/figures")

GRID = "#e5e7eb"
INK = "#111"
SHADE = "#bfbfbf"
FONT = "Georgia, serif"


class Plot:
    """Minimal xy-plane canvas with a linear data -> pixel mapping."""

    def __init__(self, xmin, xmax, ymin, ymax, ux, uy=None, pad=44):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        span_x, span_y = xmax - xmin, ymax - ymin
        self.ux = ux
        self.uy = ux if uy is None else uy
        self.pad = pad
        self.w = span_x * self.ux + 2 * pad
        self.h = span_y * self.uy + 2 * pad
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w:.0f}" '
            f'height="{self.h:.0f}" viewBox="0 0 {self.w:.0f} {self.h:.0f}">',
            '<rect width="100%" height="100%" fill="#fff"/>',
        ]

    def X(self, x):
        return self.pad + (x - self.xmin) * self.ux

    def Y(self, y):
        return self.pad + (self.ymax - y) * self.uy

    def add(self, s):
        self.parts.append(s)

    def grid(self, step=1):
        x = self.xmin
        while x <= self.xmax + 1e-9:
            self.add(
                f'<line x1="{self.X(x):.1f}" y1="{self.Y(self.ymax):.1f}" '
                f'x2="{self.X(x):.1f}" y2="{self.Y(self.ymin):.1f}" stroke="{GRID}"/>'
            )
            x += step
        y = self.ymin
        while y <= self.ymax + 1e-9:
            self.add(
                f'<line x1="{self.X(self.xmin):.1f}" y1="{self.Y(y):.1f}" '
                f'x2="{self.X(self.xmax):.1f}" y2="{self.Y(y):.1f}" stroke="{GRID}"/>'
            )
            y += step

    def axes(self, arrow_x=True, arrow_y=True):
        y0, x0 = self.Y(0), self.X(0)
        x_end = self.X(self.xmax) + (14 if arrow_x else 0)
        self.add(
            f'<line x1="{self.X(self.xmin):.1f}" y1="{y0:.1f}" '
            f'x2="{x_end:.1f}" y2="{y0:.1f}" stroke="{INK}" stroke-width="1.6"/>'
        )
        y_top = self.Y(self.ymax) - (14 if arrow_y else 0)
        self.add(
            f'<line x1="{x0:.1f}" y1="{self.Y(self.ymin):.1f}" '
            f'x2="{x0:.1f}" y2="{y_top:.1f}" stroke="{INK}" stroke-width="1.6"/>'
        )
        if arrow_x:
            self.add(
                f'<polygon points="{x_end + 7:.1f},{y0:.1f} {x_end - 1:.1f},'
                f'{y0 - 4.5:.1f} {x_end - 1:.1f},{y0 + 4.5:.1f}" fill="{INK}"/>'
            )
            self.add(
                f'<text x="{x_end + 12:.1f}" y="{y0 - 5:.1f}" font-family="{FONT}" '
                f'font-size="15" font-style="italic">x</text>'
            )
        if arrow_y:
            self.add(
                f'<polygon points="{x0:.1f},{y_top - 7:.1f} {x0 - 4.5:.1f},'
                f'{y_top + 1:.1f} {x0 + 4.5:.1f},{y_top + 1:.1f}" fill="{INK}"/>'
            )
            self.add(
                f'<text x="{x0 + 8:.1f}" y="{y_top - 6:.1f}" font-family="{FONT}" '
                f'font-size="15" font-style="italic">y</text>'
            )

    def xticks(self, values, below=True):
        y0 = self.Y(0)
        for v in values:
            x = self.X(v)
            self.add(
                f'<line x1="{x:.1f}" y1="{y0 - 4:.1f}" x2="{x:.1f}" '
                f'y2="{y0 + 4:.1f}" stroke="{INK}"/>'
            )
            ty = y0 + 18 if below else y0 - 9
            self.add(
                f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="12">\u2212{abs(v)}</text>'
                if v < 0 else
                f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="12">{v}</text>'
            )

    def yticks(self, values, left=True):
        x0 = self.X(0)
        for v in values:
            y = self.Y(v)
            self.add(
                f'<line x1="{x0 - 4:.1f}" y1="{y:.1f}" x2="{x0 + 4:.1f}" '
                f'y2="{y:.1f}" stroke="{INK}"/>'
            )
            label = f"\u2212{abs(v)}" if v < 0 else f"{v}"
            if left:
                self.add(
                    f'<text x="{x0 - 8:.1f}" y="{y + 4:.1f}" text-anchor="end" '
                    f'font-family="{FONT}" font-size="12">{label}</text>'
                )
            else:
                self.add(
                    f'<text x="{x0 + 8:.1f}" y="{y + 4:.1f}" '
                    f'font-family="{FONT}" font-size="12">{label}</text>'
                )

    def origin(self, dx=-14, dy=18):
        self.add(
            f'<text x="{self.X(0) + dx:.1f}" y="{self.Y(0) + dy:.1f}" '
            f'font-family="{FONT}" font-size="13" font-style="italic">O</text>'
        )

    def curve(self, pts, width=2.4):
        d = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self.add(
            f'<polyline points="{d}" fill="none" stroke="{INK}" '
            f'stroke-width="{width}" stroke-linecap="round"/>'
        )

    def dot(self, x, y, r=4.5):
        self.add(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{INK}"/>')

    def polygon(self, pts, fill):
        d = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        self.add(f'<polygon points="{d}" fill="{fill}" fill-opacity="0.42" stroke="none"/>')

    def save(self, name):
        self.parts.append("</svg>")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts), encoding="utf-8")
        print("wrote", OUT / name)


def q04():
    """Shaded half-plane 4x + y ≥ 16; boundary y = −4x + 16 on −8…8."""
    p = Plot(-8, 8, -8, 8, ux=22.0)

    def line_y(x):
        return -4 * x + 16

    # Clip the line to the plot box: enters top at (2, 8), leaves bottom at (6, −8).
    p.polygon([(2, 8), (8, 8), (8, -8), (6, -8)], SHADE)
    p.grid()
    p.axes()
    p.curve([(2, 8), (6, -8)], width=2.6)
    ticks = [-8, -6, -4, -2, 2, 4, 6, 8]
    p.xticks(ticks)
    p.yticks(ticks)
    p.origin()
    p.save("math2-q04-shaded-inequality.svg")


def q12():
    """Line y = 6x + 9 on a −10…10 grid; (0, 9) and (−2, −3) are marked."""
    p = Plot(-10, 10, -10, 10, ux=20.0)
    p.grid()
    p.axes()
    p.xticks([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.yticks([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.origin()
    x_top, x_bot = (10 - 9) / 6, (-10 - 9) / 6
    p.curve([(x_bot, -10), (x_top, 10)], width=2.6)
    p.dot(0, 9)
    p.dot(-2, -3)
    p.save("math2-q12-line-graph.svg")


def q13():
    """Half-plane x + 3y ≥ −36: shading above the line y = −x/3 − 12."""
    p = Plot(-10, 1, -15, 0, ux=37.6, uy=25.8)

    def line_y(x):
        return -x / 3 - 12

    p.polygon(
        [(-10, line_y(-10)), (-10, 0), (1, 0), (1, line_y(1))], SHADE
    )
    p.grid()
    p.axes(arrow_x=True, arrow_y=True)
    p.curve([(-10, line_y(-10)), (1, line_y(1))], width=2.6)
    p.dot(-6, -10)
    p.dot(0, -12)
    p.xticks([-10, -8, -6, -4, -2])
    p.yticks([-2, -4, -6, -8, -10, -12, -14], left=False)
    p.origin(dx=-17, dy=17)
    p.save("math2-q13-shaded-half-plane.svg")


def q15():
    """Graph of y = f(x) + 2 = −6^x + 5, clipped at y = −5."""
    p = Plot(-1, 5, -5, 10, ux=62.0, uy=28.5)
    p.grid()
    p.axes()
    pts = []
    x = -1.0
    x_clip = log(10) / log(6)  # −6^x + 5 = −5
    while x <= 5.0:
        y = -(6 ** x) + 5
        if y < -5:
            pts.append((x_clip, -5))
            break
        pts.append((x, y))
        x += 0.02
    p.curve(pts, width=2.6)
    p.xticks([-1, 1, 2, 3, 4, 5])
    p.yticks([-4, -2, 2, 4, 6, 8, 10])
    p.origin()
    p.save("math2-q15-exponential-graph.svg")


if __name__ == "__main__":
    q04()
    q12()
    q13()
    q15()
