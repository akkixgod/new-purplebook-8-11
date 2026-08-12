#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V2 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v2/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q01_scatter() -> str:
    """Scatterplot with line of best fit; slope ~ -0.7 (y = 8 - 0.7x)."""
    W, H = 480, 480
    pad_l, pad_r, pad_t, pad_b = 44, 36, 28, 44
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax = ymax = 10.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    points = [
        (1.0, 6.0),
        (2.0, 7.0),
        (3.0, 5.0),
        (4.5, 4.0),
        (5.0, 5.0),
        (6.0, 4.0),
        (7.0, 2.0),
        (9.0, 2.0),
        (10.0, 1.0),
    ]

    parts: list[str] = []
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(i)}" x2="{pad_l + plot_w}" y2="{sy(i)}" '
            f'stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" '
        f'y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(8)}" x2="{sx(10)}" y2="{sy(1)}" '
        f'stroke="#111" stroke-width="2.2"/>'
    )
    for i in range(1, 11):
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(i) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for px, py in points:
        parts.append(f'<circle cx="{sx(px)}" cy="{sy(py)}" r="4.5" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w + 10}" y="{pad_t + plot_h + 4}" '
        f'font-family="Arial" font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{pad_l - 4}" y="{pad_t - 8}" font-family="Arial" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q09_cups_mugs() -> str:
    """Line from (0,10) to (20,0); x: Boxes of cups, y: Boxes of mugs."""
    W, H = 480, 420
    pad_l, pad_r, pad_t, pad_b = 64, 28, 24, 56
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = 0.0, 20.0
    ymin, ymax = 0.0, 10.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(0, 21, 2):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
    for j in range(0, 11):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" '
            f'stroke="#e5e7eb"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    for i in range(4, 21, 4):
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in range(2, 11, 2):
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    parts.append(
        f'<line x1="{sx(0)}" y1="{sy(10)}" x2="{sx(20)}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="2.4"/>'
    )
    parts.append(
        f'<text x="{(pad_l + pad_l + plot_w) / 2}" y="{H - 14}" text-anchor="middle" '
        f'font-family="Arial" font-size="13">Boxes of cups</text>'
    )
    mid_y = pad_t + plot_h / 2
    parts.append(
        f'<text x="16" y="{mid_y}" text-anchor="middle" font-family="Arial" font-size="13" '
        f'transform="rotate(-90 16 {mid_y})">Boxes of mugs</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q12_xy_table() -> str:
    """x | y table with k in y-values."""
    headers = ["x", "y"]
    rows = [
        ["\u22125", "91 + 4k"],
        ["5", "91"],
        ["10", "91 \u2212 2k"],
    ]
    widths = [80, 140]
    width = sum(widths) + 40
    row_h = 36
    header_h = 36
    height = 20 + header_h + row_h * len(rows) + 20
    x0, y0 = 20, 20
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{header_h}" '
            f'fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + header_h / 2 + 5}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="14" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + header_h + row_h * r
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" '
                f'fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + row_h / 2 + 5}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="14">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def math2_q16_histogram() -> str:
    """Histogram of April 1 max temperatures over 11 years."""
    W, H = 560, 380
    pad_l, pad_r, pad_t, pad_b = 72, 28, 28, 64
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    bins = [40, 45, 50, 55, 60, 65, 70, 75, 80]
    freqs = [1, 2, 3, 3, 1, 0, 0, 1]
    xmin, xmax = 40.0, 80.0
    ymin, ymax = 0.0, 4.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for j in range(0, 5):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" '
            f'stroke="#e5e7eb"/>'
        )
    for i, freq in enumerate(freqs):
        if freq <= 0:
            continue
        x0 = sx(bins[i])
        x1 = sx(bins[i + 1])
        y0 = sy(freq)
        y1 = sy(0)
        parts.append(
            f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
            f'fill="#5b8def" stroke="#111" stroke-width="1"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    for t in bins:
        parts.append(
            f'<text x="{sx(t)}" y="{sy(0) + 18}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{t}</text>'
        )
    for j in range(0, 5):
        parts.append(
            f'<text x="{pad_l - 10}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w / 2}" y="{H - 14}" text-anchor="middle" '
        f'font-family="Arial" font-size="13">Maximum temperature on April 1 (\u00b0F)</text>'
    )
    mid_y = pad_t + plot_h / 2
    parts.append(
        f'<text x="18" y="{mid_y}" text-anchor="middle" font-family="Arial" font-size="13" '
        f'transform="rotate(-90 18 {mid_y})">Number of years</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q20_triangle() -> str:
    """Triangle XYZ with VW || XZ; a,c on XY; b,d on YZ; VW=35, XZ=55."""
    W, H = 420, 360
    Y = (210, 36)
    X = (40, 280)
    Z = (380, 280)
    t = 35 / 55

    def lerp(a, b, u):
        return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)

    def mid(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    V = lerp(Y, X, t)
    Wp = lerp(Y, Z, t)
    ya = mid(Y, V)
    vc = mid(V, X)
    yb = mid(Y, Wp)
    wd = mid(Wp, Z)
    vw = mid(V, Wp)
    xz = mid(X, Z)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="{X[0]}" y1="{X[1]}" x2="{Y[0]}" y2="{Y[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{Y[0]}" y1="{Y[1]}" x2="{Z[0]}" y2="{Z[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{Z[0]}" y1="{Z[1]}" x2="{X[0]}" y2="{X[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{V[0]}" y1="{V[1]}" x2="{Wp[0]}" y2="{Wp[1]}" stroke="#111" stroke-width="2"/>
  <text x="{Y[0]}" y="{Y[1] - 10}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700">Y</text>
  <text x="{X[0] - 14}" y="{X[1] + 6}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700">X</text>
  <text x="{Z[0] + 14}" y="{Z[1] + 6}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700">Z</text>
  <text x="{V[0] - 14}" y="{V[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-weight="700">V</text>
  <text x="{Wp[0] + 14}" y="{Wp[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-weight="700">W</text>
  <text x="{ya[0] - 14}" y="{ya[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-style="italic">a</text>
  <text x="{vc[0] - 14}" y="{vc[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-style="italic">c</text>
  <text x="{yb[0] + 14}" y="{yb[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-style="italic">b</text>
  <text x="{wd[0] + 14}" y="{wd[1] + 4}" text-anchor="middle" font-family="Arial" font-size="15" font-style="italic">d</text>
  <text x="{vw[0]}" y="{vw[1] - 8}" text-anchor="middle" font-family="Arial" font-size="15">35</text>
  <text x="{xz[0]}" y="{xz[1] + 22}" text-anchor="middle" font-family="Arial" font-size="15">55</text>
  <text x="{W / 2}" y="{H - 16}" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def main() -> None:
    write("math2-q01-scatter.svg", math2_q01_scatter())
    write("math2-q09-cups-mugs.svg", math2_q09_cups_mugs())
    write("math2-q12-xy-table.svg", math2_q12_xy_table())
    write("math2-q16-histogram.svg", math2_q16_histogram())
    write("math2-q20-triangle.svg", math2_q20_triangle())


if __name__ == "__main__":
    main()
