#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V3 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v3/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q07_similar_triangles() -> str:
    """LQ intersects MP at R; LM || PQ. Bow-tie similar triangles."""
    L = (60, 150)
    Q = (500, 165)
    M = (120, 40)
    P = (420, 280)

    def intersect(a, b, c, d):
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c
        x4, y4 = d
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    R = intersect(L, Q, M, P)
    W, H = 560, 340
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <line x1="{L[0]}" y1="{L[1]}" x2="{Q[0]}" y2="{Q[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{M[0]}" y1="{M[1]}" x2="{P[0]}" y2="{P[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{L[0]}" y1="{L[1]}" x2="{M[0]}" y2="{M[1]}" stroke="#111" stroke-width="2"/>
  <line x1="{P[0]}" y1="{P[1]}" x2="{Q[0]}" y2="{Q[1]}" stroke="#111" stroke-width="2"/>
  <text x="{L[0] - 18}" y="{L[1] + 6}" font-family="Arial" font-size="16" font-weight="700">L</text>
  <text x="{M[0] - 6}" y="{M[1] - 8}" font-family="Arial" font-size="16" font-weight="700">M</text>
  <text x="{R[0] - 6}" y="{R[1] - 10}" font-family="Arial" font-size="16" font-weight="700">R</text>
  <text x="{Q[0] + 8}" y="{Q[1] + 6}" font-family="Arial" font-size="16" font-weight="700">Q</text>
  <text x="{P[0] + 6}" y="{P[1] + 18}" font-family="Arial" font-size="16" font-weight="700">P</text>
  <text x="{W / 2}" y="{H - 16}" text-anchor="middle" font-family="Arial" font-size="12" font-style="italic">Note: Figure not drawn to scale.</text>
</svg>'''


def math2_q08_scatter() -> str:
    """Scatterplot for data set A ≈ 7(2.12)^x; x -4..4, y 0..160; 10 points."""
    W, H = 460, 440
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -4.0, 4.0
    ymin, ymax = 0.0, 160.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(-4, 5):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb"/>'
        )
    for j in range(0, 161, 20):
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
    parts.append(
        f'<polygon points="{pad_l + plot_w},{sy(0)} {pad_l + plot_w - 8},{sy(0) - 4} '
        f'{pad_l + plot_w - 8},{sy(0) + 4}" fill="#111"/>'
    )
    parts.append(
        f'<polygon points="{sx(0)},{pad_t} {sx(0) - 4},{pad_t + 8} '
        f'{sx(0) + 4},{pad_t + 8}" fill="#111"/>'
    )
    for i in range(-4, 5):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="12">{i}</text>'
        )
    for j in (40, 80, 120, 160):
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="12">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 10}" text-anchor="end" '
        f'font-family="Arial" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="Arial" font-size="13" font-style="italic">y</text>'
    )

    # Model for A is ~7(2.12)^x (choice A). Ten points as on page 68.
    xs = (-3.0, -2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 2.5, 3.0, 4.0)
    for xi in xs:
        yi = 7 * (2.12**xi)
        if yi > ymax:
            continue
        parts.append(
            f'<circle cx="{sx(float(xi)):.2f}" cy="{sy(float(yi)):.2f}" r="4.5" fill="#111"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q09_frequency_table() -> str:
    """Number of ducks | Number of days frequency table for data set A."""
    headers = ["Number of ducks", "Number of days"]
    rows = [
        ["0", "1"],
        ["1", "7"],
        ["2", "8"],
        ["3", "9"],
        ["4", "8"],
        ["5", "7"],
        ["17", "1"],
    ]
    widths = [160, 160]
    width = sum(widths) + 40
    row_h = 34
    header_h = 40
    height = 20 + header_h + row_h * len(rows) + 20
    x0, y0 = 20, 20
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{header_h}" '
            f'fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + header_h / 2 + 5}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="13" font-weight="700">{h}</text>'
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
                f'font-family="{FONT}" font-size="13">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def main() -> None:
    write("math2-q07-similar-triangles.svg", math2_q07_similar_triangles())
    write("math2-q08-scatter.svg", math2_q08_scatter())
    write("math2-q09-frequency-table.svg", math2_q09_frequency_table())


if __name__ == "__main__":
    main()
