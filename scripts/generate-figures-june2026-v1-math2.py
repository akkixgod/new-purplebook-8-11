#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V1 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v1/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q04_parabola() -> str:
    """y = x^2 - 3x - 4; x -8..8, y -40..10."""
    W, H = 520, 520
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -8.0, 8.0
    ymin, ymax = -40.0, 10.0

    def sx(x: float) -> float:
        return pad_l + ((x - xmin) / (xmax - xmin)) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / (ymax - ymin)) * plot_h

    parts: list[str] = []
    for i in range(-8, 9):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" '
            f'stroke="#e5e7eb" stroke-width="1"/>'
        )
    for j in range(-40, 11):
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(j)}" x2="{pad_l + plot_w}" y2="{sy(j)}" '
            f'stroke="#e5e7eb" stroke-width="1"/>'
        )
    parts.append(
        f'<line x1="{pad_l}" y1="{sy(0)}" x2="{pad_l + plot_w}" y2="{sy(0)}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    parts.append(
        f'<line x1="{sx(0)}" y1="{pad_t}" x2="{sx(0)}" y2="{pad_t + plot_h}" '
        f'stroke="#111" stroke-width="1.6"/>'
    )
    # arrowheads
    parts.append(
        f'<polygon points="{pad_l + plot_w},{sy(0)} {pad_l + plot_w - 8},{sy(0) - 4} '
        f'{pad_l + plot_w - 8},{sy(0) + 4}" fill="#111"/>'
    )
    parts.append(
        f'<polygon points="{sx(0)},{pad_t} {sx(0) - 4},{pad_t + 8} '
        f'{sx(0) + 4},{pad_t + 8}" fill="#111"/>'
    )
    for i in range(-8, 9, 2):
        if i == 0:
            continue
        parts.append(
            f'<text x="{sx(i)}" y="{sy(0) + 16}" text-anchor="middle" '
            f'font-family="Arial" font-size="11">{i}</text>'
        )
    for j in range(-40, 11, 5):
        if j == 0:
            continue
        parts.append(
            f'<text x="{sx(0) - 8}" y="{sy(j) + 4}" text-anchor="end" '
            f'font-family="Arial" font-size="11">{j}</text>'
        )
    parts.append(
        f'<text x="{pad_l + plot_w - 4}" y="{sy(0) - 10}" text-anchor="end" '
        f'font-family="Arial" font-size="13" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{sx(0) + 10}" y="{pad_t + 14}" text-anchor="start" '
        f'font-family="Arial" font-size="13" font-style="italic">y</text>'
    )

    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    pts = []
    for x in xs:
        y = x * x - 3 * x - 4
        if ymin <= y <= ymax:
            pts.append(f"{sx(x):.2f},{sy(y):.2f}")
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width="2.2"/>'
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


def math2_q14_similar_triangles() -> str:
    """LQ intersects MP at R; LM || PQ. Bow-tie similar triangles."""
    # L left, Q right on near-horizontal; M up-left, P down-right; R intersection
    L = (60, 150)
    Q = (500, 165)
    M = (120, 40)
    P = (420, 280)
    # R as intersection of LQ and MP
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


def math2_q15_scatter() -> str:
    """Scatterplot for data set A ≈ 5(2.03)^x; x -4..4, y 0..180."""
    W, H = 460, 440
    pad_l, pad_r, pad_t, pad_b = 48, 36, 28, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmin, xmax = -4.0, 4.0
    ymin, ymax = 0.0, 180.0

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
    for j in range(0, 181, 20):
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

    # Model for A is ~5(2.03)^x (choice A). Page shows points near
    # x = -3, -1, 0, 1, 2, 3, 4 (no clear point at x = -2).
    for xi in (-3, -1, 0, 1, 2, 3, 4):
        yi = 5 * (2.03**xi)
        parts.append(
            f'<circle cx="{sx(float(xi)):.2f}" cy="{sy(float(yi)):.2f}" r="4.5" fill="#111"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q16_frequency_table() -> str:
    """Value | Frequency table for data set A."""
    headers = ["Value", "Frequency"]
    rows = [
        ["0", "1"],
        ["1", "7"],
        ["2", "8"],
        ["3", "9"],
        ["4", "8"],
        ["5", "7"],
        ["16", "1"],
    ]
    widths = [120, 120]
    width = sum(widths) + 40
    row_h = 34
    title_h = 16
    height = title_h + row_h * (1 + len(rows)) + 20
    x0, y0 = 20, title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 22}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="13" font-weight="700">{h}</text>'
        )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 22}" text-anchor="middle" '
                f'font-family="Georgia, serif" font-size="13">{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def main() -> None:
    write("math2-q04-parabola.svg", math2_q04_parabola())
    write("math2-q09-cups-mugs.svg", math2_q09_cups_mugs())
    write("math2-q14-similar-triangles.svg", math2_q14_similar_triangles())
    write("math2-q15-scatter.svg", math2_q15_scatter())
    write("math2-q16-frequency-table.svg", math2_q16_frequency_table())


if __name__ == "__main__":
    main()
