#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V2 R&W Module 1."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v2/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def table_svg(
    title: str,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int] | None = None,
) -> str:
    n = len(headers)
    widths = col_widths or ([160] + [140] * (n - 1))
    width = sum(widths) + 40
    row_h = 36
    title_h = 56 if title else 16
    height = title_h + 40 + row_h * (1 + len(rows)) + 20
    x0 = 20
    y0 = title_h

    header_cells = []
    body_cells = []
    x = x0
    for i, h in enumerate(headers):
        header_cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{row_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
            f'<text x="{x + widths[i] / 2}" y="{y0 + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13" font-weight="700">{h}</text>'
        )
        x += widths[i]

    for r, row in enumerate(rows):
        y = y0 + row_h * (r + 1)
        x = x0
        for i, cell in enumerate(row):
            body_cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
                f'<text x="{x + widths[i] / 2}" y="{y + 24}" text-anchor="middle" font-family="Georgia, serif" font-size="13">{cell}</text>'
            )
            x += widths[i]

    title_el = (
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">{title}</text>'
        if title
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(header_cells)}
  {"".join(body_cells)}
</svg>'''


def main() -> None:
    write(
        "eng1-q11-biofuel-profits.svg",
        table_svg(
            "Estimated Annual Costs and Profits for Biofuel Profit Models (in dollars)",
            ["Method", "LCFS revenue", "Total revenue", "Total cost", "Total profit"],
            [
                ["Heuristic", "6,837,474", "37,957,674", "30,528,134", "7,429,540"],
                ["Lexicographic", "9,878,474", "40,998,474", "30,528,134", "10,470,340"],
                ["Proposed", "11,157,472", "42,277,472", "30,933,469", "11,344,003"],
            ],
            col_widths=[140, 140, 140, 140, 140],
        ),
    )


if __name__ == "__main__":
    main()
