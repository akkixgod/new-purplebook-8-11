#!/usr/bin/env python3
"""Generate clean SVG figures for PurpleBook test 9 Math Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/purplebook-test-9/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Arial, sans-serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def math2_q07_scatter() -> str:
    """Scatterplot with LOBF y ≈ 148.13 + 58.61x; x 0–10, y 0–800."""
    W, H = 480, 460
    pad_l, pad_r, pad_t, pad_b = 52, 36, 28, 48
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax, ymax = 10.0, 800.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    # Approximate Bluebook scatter around LOBF y = 148.13 + 58.61x
    points = [
        (1.0, 175),
        (2.0, 320),
        (3.0, 290),
        (4.0, 430),
        (5.0, 395),
        (6.0, 560),
        (7.0, 520),
        (8.0, 680),
        (9.5, 740),
    ]
    intercept, slope = 148.13, 58.61

    parts: list[str] = []
    # vertical grid every 1; horizontal every 100
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t}" x2="{sx(i)}" y2="{pad_t + plot_h}" stroke="#e5e7eb"/>'
        )
    for j in range(0, 9):
        yv = j * 100
        parts.append(
            f'<line x1="{pad_l}" y1="{sy(yv)}" x2="{pad_l + plot_w}" y2="{sy(yv)}" stroke="#e5e7eb"/>'
        )
    # axes
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>'
    )
    # x ticks/labels 0..10
    for i in range(0, 11):
        parts.append(
            f'<line x1="{sx(i)}" y1="{pad_t + plot_h}" x2="{sx(i)}" y2="{pad_t + plot_h + 5}" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{sx(i)}" y="{pad_t + plot_h + 20}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="11">{i}</text>'
        )
    # y ticks/labels 0,200,...,800
    for j in range(0, 5):
        yv = j * 200
        parts.append(
            f'<line x1="{pad_l - 5}" y1="{sy(yv)}" x2="{pad_l}" y2="{sy(yv)}" stroke="#111"/>'
        )
        parts.append(
            f'<text x="{pad_l - 8}" y="{sy(yv) + 4}" text-anchor="end" '
            f'font-family="{FONT}" font-size="11">{yv}</text>'
        )
    # LOBF across plot
    x0, x1 = 0.0, 10.0
    y0 = intercept + slope * x0
    y1 = intercept + slope * x1
    parts.append(
        f'<line x1="{sx(x0):.1f}" y1="{sy(y0):.1f}" x2="{sx(x1):.1f}" y2="{sy(y1):.1f}" '
        f'stroke="#111" stroke-width="2"/>'
    )
    for px, py in points:
        parts.append(f'<circle cx="{sx(px):.1f}" cy="{sy(py):.1f}" r="4" fill="#111"/>')
    parts.append(
        f'<text x="{pad_l + plot_w + 6}" y="{pad_t + plot_h + 4}" font-family="{FONT}" '
        f'font-size="14" font-style="italic">x</text>'
    )
    parts.append(
        f'<text x="{pad_l - 4}" y="{pad_t - 8}" font-family="{FONT}" '
        f'font-size="14" font-style="italic">y</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(parts)}
</svg>'''


def math2_q11_even_odd_table() -> str:
    """Contingency table: List A/B × even/odd integers."""
    headers = ["", "Even integers", "odd integers", "Total"]
    rows = [
        ["List A", "12", "44", "56"],
        ["List B", "40", "4", "44"],
        ["Total", "52", "48", "100"],
    ]
    widths = [80, 120, 110, 80]
    font_size = 13
    header_font = 12
    hh, rh = 40, 36
    x0, y0 = 16, 16
    width = sum(widths) + 32
    height = y0 + hh + rh * len(rows) + 16
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" fill="#fff" stroke="#111"/>'
        )
        if h:
            cells.append(
                f'<text x="{x + widths[i] / 2}" y="{y0 + hh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{header_font}" font-weight="700">{h}</text>'
            )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + hh + rh * r
        x = x0
        for i, cell in enumerate(row):
            weight = ' font-weight="700"' if i == 0 or r == 2 else ""
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" fill="#fff" stroke="#111"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + rh / 2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{font_size}"{weight}>{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


if __name__ == "__main__":
    write("math2-q07-scatter-best-fit.svg", math2_q07_scatter())
    write("math2-q11-even-odd-table.svg", math2_q11_even_odd_table())
