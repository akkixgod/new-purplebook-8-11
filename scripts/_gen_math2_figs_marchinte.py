"""Generate Math Module 2 stem figures for the 2025-march-int-e mock.

Four items carry artwork: Q2 (QII scatterplot + line of best fit), Q9
(exponential f(x) = −(5/2)^x − 4, entirely below y = −4), Q13 (intersecting
triangles WQX and YQZ), and Q18 (graph of y = f(x) + 2 = −4^x + 7).
Geometry follows the page screenshots.

Run:  py -3 scripts/_gen_math2_figs_marchinte.py
"""
from __future__ import annotations

from math import atan2, cos, log, pi, sin
from pathlib import Path

OUT = Path("public/mocks/2025-march-int-e/figures")

GRID = "#e5e7eb"
INK = "#111"
FONT = "Georgia, serif"


class Plot:
    """Minimal xy-plane canvas with a linear data -> pixel mapping."""

    def __init__(self, xmin, xmax, ymin, ymax, ux, uy=None, pad=44, pad_r=None):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        span_x, span_y = xmax - xmin, ymax - ymin
        self.ux = ux
        self.uy = ux if uy is None else uy
        self.pad = pad
        self.pad_r = pad if pad_r is None else pad_r
        self.w = span_x * self.ux + pad + self.pad_r
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
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def dot(self, x, y, r=4.5):
        self.add(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{INK}"/>')

    def save(self, name):
        self.parts.append("</svg>")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts), encoding="utf-8")
        print("wrote", OUT / name)


def q02():
    """QII scatterplot with line of best fit y = −x + 1.5 on x ∈ [−14, 0], y ∈ [0, 20]."""
    p = Plot(-14, 0, 0, 20, ux=22.0, uy=16.5, pad=44, pad_r=58)
    p.grid(step=2)
    p.axes()
    p.xticks([-14, -12, -10, -8, -6, -4, -2])
    p.yticks([2, 4, 6, 8, 10, 12, 14, 16, 18, 20], left=False)
    p.origin(dx=-16, dy=18)
    p.curve([(-14, 15.5), (0, 1.5)], width=2.4)
    for x, y in [(-14, 15), (-12, 13.5), (-10, 11.5), (-8, 10), (-6, 8.2), (-4, 4.8)]:
        p.dot(x, y, r=4.2)
    p.save("math2-q02-scatterplot.svg")


def q09():
    """Exponential f(x) = −(5/2)^x − 4, entirely below the asymptote y = −4."""
    p = Plot(-10, 10, -10, 4, ux=22.0, uy=22.0)
    p.grid()
    p.axes()
    pts = []
    x = -10.0
    # −(2.5)^x − 4 = −10  ⇒  2.5^x = 6  ⇒  x = log(6)/log(2.5)
    x_clip = log(6) / log(2.5)
    while x <= 10.0:
        y = -(2.5 ** x) - 4
        if y < -10:
            pts.append((x_clip, -10))
            break
        pts.append((x, y))
        x += 0.04
    p.curve(pts, width=2.6)
    p.xticks([-10, -8, -6, -4, -2, 2, 4, 6, 8, 10])
    p.yticks([-10, -8, -6, -4, -2, 2, 4])
    p.origin()
    p.save("math2-q09-exponential-graph.svg")


def q13():
    """Two triangles WQX and YQZ; lines WZ and XY cross at Q; ∠W = ∠Y = a°."""
    W, Q, Z = (90, 50), (235, 145), (380, 240)
    X, Y = (70, 230), (400, 60)

    def seg(a, b, width=2.0):
        return (
            f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" '
            f'stroke="{INK}" stroke-width="{width}"/>'
        )

    def angle_arc(vertex, p1, p2, r=22):
        a1 = atan2(p1[1] - vertex[1], p1[0] - vertex[0])
        a2 = atan2(p2[1] - vertex[1], p2[0] - vertex[0])
        # Walk the smaller interior sweep.
        d = (a2 - a1) % (2 * pi)
        if d > pi:
            a1, a2, d = a2, a1, (2 * pi - d)
        x1, y1 = vertex[0] + r * cos(a1), vertex[1] + r * sin(a1)
        x2, y2 = vertex[0] + r * cos(a2), vertex[1] + r * sin(a2)
        large = 1 if d > pi else 0
        return (
            f'<path d="M {x1:.1f},{y1:.1f} A {r},{r} 0 {large} 1 {x2:.1f},{y2:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="1.4"/>'
        )

    def label_pos(vertex, p1, p2, dist=38):
        a1 = atan2(p1[1] - vertex[1], p1[0] - vertex[0])
        a2 = atan2(p2[1] - vertex[1], p2[0] - vertex[0])
        d = (a2 - a1) % (2 * pi)
        if d > pi:
            a1, a2, d = a2, a1, (2 * pi - d)
        mid = a1 + d / 2
        return vertex[0] + dist * cos(mid), vertex[1] + dist * sin(mid)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="310" viewBox="0 0 500 310">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        seg(W, Z),
        seg(X, Y),
        seg(W, X),
        seg(Y, Z),
        angle_arc(W, Q, X),
        angle_arc(Y, Q, Z),
    ]
    wx, wy = label_pos(W, Q, X, 40)
    yx, yy = label_pos(Y, Q, Z, 40)
    labels = [
        ("W", W[0] - 18, W[1] + 4),
        ("X", X[0] - 18, X[1] + 16),
        ("Q", Q[0] - 4, Q[1] - 10),
        ("Y", Y[0] + 8, Y[1] + 4),
        ("Z", Z[0] + 8, Z[1] + 16),
        ("a\u00b0", wx - 6, wy + 5),
        ("a\u00b0", yx - 6, yy + 5),
    ]
    for txt, x, y in labels:
        parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" '
            f'font-size="16" font-style="italic">{txt}</text>'
        )
    parts.append(
        '<text x="250" y="298" text-anchor="middle" font-family="'
        f'{FONT}" font-size="13" font-style="italic">'
        "Note: Figure not drawn to scale.</text>"
    )
    parts.append("</svg>")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "math2-q13-intersecting-triangles.svg").write_text(
        "\n".join(parts), encoding="utf-8"
    )
    print("wrote", OUT / "math2-q13-intersecting-triangles.svg")


def q18():
    """Graph of y = f(x) + 2 = −4^x + 7, clipped at y = −5."""
    p = Plot(-2, 6, -5, 11, ux=52.0, uy=24.0)
    p.grid()
    p.axes()
    pts = []
    x = -2.0
    x_clip = log(12) / log(4)  # −4^x + 7 = −5
    while x <= 6.0:
        y = -(4 ** x) + 7
        if y < -5:
            pts.append((x_clip, -5))
            break
        pts.append((x, y))
        x += 0.02
    p.curve(pts, width=2.6)
    p.xticks([-1, 1, 2, 3, 4, 5])
    p.yticks([-4, -2, 2, 4, 6, 8, 10])
    p.origin()
    p.save("math2-q18-exponential-graph.svg")


if __name__ == "__main__":
    q02()
    q09()
    q13()
    q18()
