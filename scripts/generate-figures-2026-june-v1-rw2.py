#!/usr/bin/env python3
"""Generate clean SAT-style SVG figures for 2026 June V1 R&W Module 2."""

from __future__ import annotations

from pathlib import Path

OUT = Path("public/mocks/2026-june-v1/figures")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, svg: str) -> None:
    path = OUT / name
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path)


def emoji_openness_bars() -> str:
    W, H = 520, 440
    pad_l, pad_r, pad_t, pad_b = 70, 30, 55, 95
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    ymax = 4.5

    def sy(v: float) -> float:
        return pad_t + plot_h - (v / ymax) * plot_h

    grid = []
    ylabels = []
    for i in range(0, 10):
        v = i * 0.5
        y = sy(v)
        grid.append(
            f'<line x1="{pad_l}" y1="{y}" x2="{pad_l + plot_w}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>'
        )
        label = str(int(v)) if v == int(v) else str(v)
        ylabels.append(
            f'<text x="{pad_l - 8}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="12">{label}</text>'
        )

    bars_data = [(3.65, "#6b7280"), (4.10, "#fff"), (4.25, "#111")]
    bw = 48
    gap = 18
    total_w = 3 * bw + 2 * gap
    start_x = pad_l + (plot_w - total_w) / 2
    bars = []
    for i, (val, fill) in enumerate(bars_data):
        x = start_x + i * (bw + gap)
        y = sy(val)
        h = pad_t + plot_h - y
        bars.append(
            f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" fill="{fill}" stroke="#111" stroke-width="1.5"/>'
        )

    mid_y = pad_t + plot_h / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="100%" height="100%" fill="#fff"/>
  <text x="{W / 2}" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Participants' Openness to</text>
  <text x="{W / 2}" y="42" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700">Marketing Message Content</text>
  {"".join(grid)}
  {"".join(ylabels)}
  {"".join(bars)}
  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>
  <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#111" stroke-width="1.5"/>
  <text x="{pad_l + plot_w / 2}" y="{pad_t + plot_h + 28}" text-anchor="middle" font-family="Arial" font-size="13">Result by condition</text>
  <text x="18" y="{mid_y}" text-anchor="middle" font-family="Arial" font-size="13" transform="rotate(-90 18 {mid_y})">Average rating</text>
  <rect x="{pad_l + 40}" y="{H - 38}" width="14" height="14" fill="#6b7280" stroke="#111"/>
  <text x="{pad_l + 60}" y="{H - 26}" font-family="Arial" font-size="12">supplement</text>
  <rect x="{pad_l + 160}" y="{H - 38}" width="14" height="14" fill="#fff" stroke="#111"/>
  <text x="{pad_l + 180}" y="{H - 26}" font-family="Arial" font-size="12">substitute</text>
  <rect x="{pad_l + 280}" y="{H - 38}" width="14" height="14" fill="#111" stroke="#111"/>
  <text x="{pad_l + 300}" y="{H - 26}" font-family="Arial" font-size="12">control</text>
</svg>'''


def table_svg(
    title: str | None,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[int],
    note: str | None = None,
    header_font: int = 11,
    header_h: int = 72,
    row_h: int = 40,
) -> str:
    widths = col_widths
    width = sum(widths) + 40
    title_h = 50 if title else 16
    note_h = 36 if note else 0
    height = title_h + header_h + row_h * len(rows) + note_h + 20
    x0 = 20
    y0 = title_h
    cells: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        cells.append(
            f'<rect x="{x}" y="{y0}" width="{widths[i]}" height="{header_h}" fill="#f3f4f6" stroke="#111" stroke-width="1"/>'
        )
        lines = h.split("\n")
        line_h = 13
        start_y = y0 + (header_h - line_h * len(lines)) / 2 + 10
        for li, line in enumerate(lines):
            cells.append(
                f'<text x="{x + widths[i] / 2}" y="{start_y + li * line_h}" text-anchor="middle" font-family="Georgia, serif" font-size="{header_font}" font-weight="700">{line}</text>'
            )
        x += widths[i]

    for r, row in enumerate(rows):
        y = y0 + header_h + row_h * r
        x = x0
        for i, cell in enumerate(row):
            cells.append(
                f'<rect x="{x}" y="{y}" width="{widths[i]}" height="{row_h}" fill="#fff" stroke="#111" stroke-width="1"/>'
            )
            clines = cell.split("\n")
            cstart = y + (row_h - 14 * len(clines)) / 2 + 11
            for li, line in enumerate(clines):
                cells.append(
                    f'<text x="{x + widths[i] / 2}" y="{cstart + li * 14}" text-anchor="middle" font-family="Georgia, serif" font-size="12">{line}</text>'
                )
            x += widths[i]

    title_el = (
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15" font-weight="700">{title}</text>'
        if title
        else ""
    )
    note_el = (
        f'<text x="{x0}" y="{height - 12}" font-family="Georgia, serif" font-size="11" font-style="italic">{note}</text>'
        if note
        else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#fff"/>
  {title_el}
  {"".join(cells)}
  {note_el}
</svg>'''


def main() -> None:
    write("eng2-q10-emoji-openness.svg", emoji_openness_bars())
    write(
        "eng2-q11-modular-days.svg",
        table_svg(
            "Number of Days to Construct Modular Retail Facilities",
            [
                "Retail facilities",
                "Construction\ncompany",
                "Days to\ncomplete\nconstruction",
                "Location",
            ],
            [
                [
                    "Constitutional Hill\nCoffee Shop",
                    "Modular Site\nSolutions",
                    "23",
                    "Johannesburg,\nSouth Africa",
                ],
                ["Harrison Street Oasis", "UrbanBloc", "106", "California, USA"],
                [
                    "Sundance Ridge\nSales Center",
                    "WillScot",
                    "136",
                    "Kansas, USA",
                ],
                [
                    "St. Regis\nResidences-Rye",
                    "Cassone Leasing",
                    "443",
                    "New York, USA",
                ],
            ],
            [180, 150, 110, 160],
            header_font=12,
            header_h=68,
            row_h=44,
        ),
    )
    write(
        "eng2-q12-green-hydrogen.svg",
        table_svg(
            None,
            [
                "Country",
                "Estimated electricity\nfor green hydrogen\nproduction (kilowatts\nper capita), 2020",
                "Percentage of\ndirect-use\nelectricity\ncapacity, 2020",
                "Estimated electricity\nfor green hydrogen\nproduction (kilowatts\nper capita), 2050",
                "Percentage of\ndirect-use\nelectricity\ncapacity, 2050",
            ],
            [
                ["Indonesia", "0.1", "51", "0.1", "63"],
                ["Netherlands", "0.6", "79", "0.8", "79"],
                ["South Africa", "0.0", "9", "0.3", "30"],
                ["Taiwan", "0.0", "1", "0.5", "17"],
            ],
            [100, 160, 120, 160, 120],
            note="Estimated electricity for green hydrogen production data are rounded to the first decimal place.",
            header_font=10,
            header_h=78,
            row_h=36,
        ),
    )


if __name__ == "__main__":
    main()
