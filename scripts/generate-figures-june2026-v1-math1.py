#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V1 Math Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v1/figures")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Georgia, serif"


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int],
    *,
    font_size: int = 13,
    header_font: int = 12,
    row_h: int | None = None,
    header_h: int | None = None,
    row_labels_bold: bool = False,
    header_fill: str = "#f3f4f6",
    first_col_fill: str | None = "#f3f4f6",
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    needs_wrap = any("|" in h for h in headers)
    hh = header_h if header_h is not None else (52 if needs_wrap else 40)
    rh = row_h if row_h is not None else 40
    height = 20 + hh + rh * len(rows) + 20
    x0, y0 = 20, 20
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{hh}" '
            f'fill="{header_fill}" stroke="#111"/>'
        )
        if "|" in h:
            lines = h.split("|")
            line_h = 14
            start_y = y0 + (hh - line_h * (len(lines) - 1)) / 2 - 2
            for li, line in enumerate(lines):
                cells.append(
                    f'<text x="{x + widths[i] / 2}" y="{start_y + li * line_h}" '
                    f'text-anchor="middle" font-family="{FONT}" '
                    f'font-size="{header_font}" font-weight="700">{line}</text>'
                )
        else:
            cells.append(
                f'<text x="{x + widths[i] / 2}" y="{y0 + hh / 2 + 4}" '
                f'text-anchor="middle" font-family="{FONT}" '
                f'font-size="{header_font}" font-weight="700">{h}</text>'
            )
        x += widths[i]
    for r, row in enumerate(rows):
        y = y0 + hh + rh * r
        x = x0
        for i, cell in enumerate(row):
            fill = first_col_fill if (i == 0 and first_col_fill) else "#fff"
            weight = ' font-weight="700"' if (row_labels_bold and i == 0) else ""
            anchor = "middle"
            tx = x + widths[i] / 2
            if i == 0 and row_labels_bold:
                anchor = "start"
                tx = x + 10
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{rh}" '
                f'fill="{fill}" stroke="#111"/>'
                f'<text x="{tx}" y="{y + rh / 2 + 4}" text-anchor="{anchor}" '
                f'font-family="{FONT}" font-size="{font_size}"{weight}>{cell}</text>'
            )
            x += widths[i]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {"".join(cells)}
</svg>'''


def math1_q01_member_table() -> str:
    return table_svg(
        ["", "Live north of|Center St.", "Live south of|Center St.", "Total"],
        [
            ["Less than 45 years old", "21", "12", "33"],
            ["At least 45 years old", "14", "88", "102"],
            ["Total", "35", "100", "135"],
        ],
        [190, 120, 120, 80],
        header_font=12,
        font_size=13,
        header_h=52,
        row_h=42,
        row_labels_bold=True,
    )


def math1_q10_scatter() -> str:
    """Scatterplot of x vs y on 0–14 axes; trend ≈ y = x with one outlier."""
    W, H = 460, 460
    pad_l, pad_r, pad_t, pad_b = 44, 36, 28, 44
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    xmax = ymax = 14.0

    def sx(x: float) -> float:
        return pad_l + (x / xmax) * plot_w

    def sy(y: float) -> float:
        return pad_t + ((ymax - y) / ymax) * plot_h

    # Pixel-calibrated from page-68.png (approximate data coords)
    points = [
        (1.5, 1.7),
        (2.4, 2.8),
        (4.3, 4.7),
        (5.5, 2.8),  # outlier below the main trend
        (7.2, 7.6),
        (8.7, 9.5),
        (9.8, 9.6),
        (10.6, 10.2),
        (12.1, 12.4),
        (13.0, 11.9),
    ]

    parts: list[str] = []
    for i in range(0, 15):
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
    for i in range(2, 15, 2):
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


def math1_q17_xy_table() -> str:
    return table_svg(
        ["x", "y"],
        [
            ["−10", "n + 128"],
            ["−5", "n + 64"],
            ["0", "n"],
        ],
        [100, 120],
        font_size=15,
        header_font=15,
        header_h=40,
        row_h=40,
        row_labels_bold=False,
        first_col_fill=None,
    )


def main() -> None:
    write("math1-q01-member-table.svg", math1_q01_member_table())
    write("math1-q10-scatter.svg", math1_q10_scatter())
    write("math1-q17-xy-table.svg", math1_q17_xy_table())


if __name__ == "__main__":
    main()
